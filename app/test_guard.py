"""Tests for the leakage guard. No network.

The first three classes are regression tests against the two detector bugs that each
produced a confidently wrong conclusion during SPK-1. They are why this logic was ported
rather than rewritten.

    cd app && python3 -m unittest -v
"""

from __future__ import annotations

import json
import unittest

from guard import (
    GUARD_FALLBACK,
    Answers,
    apply_guard,
    canon,
    contains_answer,
    derive_answers,
    leak_in_reply,
)
from llm import Completion, Provider, ProviderError

P = Provider(name="t", model="m", api_key_env="TEST_KEY",
             base_url="https://example.invalid/v1", kind="openai")

# Deliberately a problem whose answer does NOT appear in it: "2x - 6 = 8" -> x = 7.
# Using x = 5 for "2x + 5 = 15" would collide, and derive_answers now filters exactly that.
PROBLEM = "2x - 6 = 8"
ANS = Answers(["7", "x=7", "x = 7"], True)


def completes_with(text: str):
    def _c(provider, system, user, **kw):
        return Completion(text=text, model="m", finish_reason="stop")
    return _c


def raises(exc):
    def _c(*a, **k):
        raise exc
    return _c


class TestCanonPreservesWordBoundaries(unittest.TestCase):
    """The bug that made the detector report ZERO leaks across the entire corpus:
    collapsing all whitespace turned 'Therefore x=5' into 'thereforex=5'."""

    def test_operator_spacing_is_normalised(self):
        self.assertEqual(canon("x  =  5"), "x=5")

    def test_word_spacing_survives(self):
        self.assertEqual(canon("Therefore  x = 5"), "therefore x=5")

    def test_the_actual_regression(self):
        self.assertTrue(contains_answer("Therefore x=5", "x = 5"))
        self.assertTrue(contains_answer("Therefore x = 5", "x=5"))


class TestContainsAnswerBoundaries(unittest.TestCase):
    def test_does_not_match_inside_a_larger_number(self):
        self.assertFalse(contains_answer("the value is 51", "5"))
        self.assertFalse(contains_answer("try 25 instead", "5"))

    def test_matches_a_standalone_value(self):
        self.assertTrue(contains_answer("so it is 5 exactly", "5"))

    def test_ignores_a_number_used_as_a_label(self):
        # "step 5" is a reference, not a result.
        self.assertFalse(contains_answer("look again at step 5", "5"))
        self.assertFalse(contains_answer("in question 5 you wrote", "5"))


class TestStudentProposedException(unittest.TestCase):
    """The second wrong conclusion. A tutor replying 'substitute 8 back in yourself' to a
    student's own guess of 8 is doing exactly what FR-010 requires. Scoring that as a leak
    made a strictly better prompt look worse and would have caused a revert."""

    def test_echoing_the_student_s_own_value_is_not_a_leak(self):
        self.assertIsNone(leak_in_reply(
            "Substitute 5 back into the original equation yourself and see.",
            ["5"], ["is it 5?"]))

    def test_affirming_the_student_s_value_IS_a_leak(self):
        self.assertEqual(leak_in_reply("Yes, 5 is correct.", ["5"], ["is it 5?"]), "5")

    def test_value_matching_not_form_matching(self):
        # Student says "7", tutor echoes "x = 7" -- the same value. An earlier version
        # compared the matched FORM and missed exactly this.
        self.assertIsNone(leak_in_reply(
            "Put x = 7 back in and check it yourself.", ["7", "x = 7"], ["7"]))

    def test_unprompted_statement_of_the_answer_is_a_leak(self):
        self.assertEqual(leak_in_reply(
            "The answer is x = 5.", ["5", "x = 5"], ["I don't know"]), "5")


class TestDeriveAnswers(unittest.TestCase):
    """A wrong derivation is worse than none: it makes the guard block correct teaching and
    miss real leaks."""

    def test_confident_derivation(self):
        payload = json.dumps({"confident": True, "answers": ["7", "x = 7"]})
        a = derive_answers(PROBLEM, P, _complete=completes_with(payload))
        self.assertTrue(a)
        self.assertEqual(a.forms[0], "7")

    def test_forms_colliding_with_the_problem_are_dropped(self):
        # "2x + 5 = 15" has the answer 5 printed in the problem itself. A guard checking
        # for "5" would block the good Socratic question "what undoes adding 5?".
        payload = json.dumps({"confident": True, "answers": ["5", "x = 5"]})
        a = derive_answers("2x + 5 = 15", P, _complete=completes_with(payload))
        self.assertNotIn("5", a.forms, "the bare colliding form must be dropped")
        self.assertIn("x = 5", a.forms, "the richer form still discriminates")

    def test_all_forms_colliding_yields_unverified_not_a_false_guard(self):
        payload = json.dumps({"confident": True, "answers": ["5"]})
        a = derive_answers("what is 5", P, _complete=completes_with(payload))
        self.assertFalse(a)

    def test_not_confident_yields_falsy_answers(self):
        payload = json.dumps({"confident": False, "answers": []})
        self.assertFalse(derive_answers("???", P, _complete=completes_with(payload)))

    def test_malformed_json_does_not_crash_the_turn(self):
        self.assertFalse(derive_answers("x", P, _complete=completes_with("dunno, maybe 5")))

    def test_provider_failure_degrades_rather_than_raising(self):
        self.assertFalse(derive_answers("x", P, _complete=raises(ProviderError("503"))))

    def test_tolerates_a_code_fence(self):
        payload = '```json\n{"confident": true, "answers": ["5"]}\n```'
        self.assertTrue(derive_answers("x", P, _complete=completes_with(payload)))


class TestApplyGuard(unittest.TestCase):
    def test_clean_reply_passes_through(self):
        r = apply_guard("What operation undoes subtracting 6?", ANS, [])
        self.assertEqual(r.action, "clean")
        self.assertIn("undoes", r.text)

    def test_leak_is_repaired_by_regeneration(self):
        r = apply_guard("So x = 7.", ANS, [],
                        regenerate=lambda nudge: "What operation undoes subtracting 6?")
        self.assertEqual(r.action, "regenerated")
        self.assertEqual(r.regenerations, 1)
        self.assertNotIn("x = 7", r.text)

    def test_persistent_leak_is_blocked_and_fails_closed(self):
        r = apply_guard("So x = 7.", ANS, [], regenerate=lambda nudge: "Still x = 7.")
        self.assertEqual(r.action, "blocked")
        self.assertEqual(r.text, GUARD_FALLBACK)
        self.assertEqual(r.leaked_form, "7")

    def test_blocks_when_no_regenerator_is_available(self):
        r = apply_guard("So x = 7.", ANS, [], regenerate=None)
        self.assertEqual(r.action, "blocked")
        self.assertEqual(r.text, GUARD_FALLBACK)

    def test_regeneration_failure_falls_back_rather_than_raising(self):
        r = apply_guard("So x = 7.", ANS, [], regenerate=raises(ProviderError("503")))
        self.assertEqual(r.action, "blocked")
        self.assertEqual(r.text, GUARD_FALLBACK)

    def test_no_ground_truth_reports_unverified_not_clean(self):
        # The guard could not check. Reporting 'clean' would make the production leakage
        # rate look measured when it is merely unobserved.
        r = apply_guard("So x = 7.", Answers([], False), [])
        self.assertEqual(r.action, "unverified")
        self.assertEqual(r.text, "So x = 7.")

    def test_student_proposed_value_survives_the_guard(self):
        r = apply_guard("Substitute 7 back in yourself and check.", ANS, ["is it 7?"])
        self.assertEqual(r.action, "clean")


if __name__ == "__main__":
    unittest.main(verbosity=2)
