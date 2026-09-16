"""Tests for transcription and the FR-026 confirmation contract. No network.

    cd app && python3 -m unittest -v
"""

from __future__ import annotations

import json
import unittest

from llm import Completion, Provider, ProviderError
from transcribe import (
    MAX_IMAGE_BYTES,
    ImageRejected,
    NotLegible,
    confirmation_prompt,
    parse_transcription,
    transcribe,
    validate_image,
)

P = Provider(name="t", model="m", api_key_env="TEST_KEY",
             base_url="https://example.invalid/v1", kind="openai")

GOOD = json.dumps({"legible": True, "steps": ["2x + 5 = 13", "2x = 8", "x = 5"]})


def completes_with(text: str):
    def _c(provider, system, user, **kw):
        return Completion(text=text, model="m", finish_reason="stop")
    return _c


class TestImageValidation(unittest.TestCase):
    """Trust boundary 1: student input is hostile, and validated before any model call."""

    def test_rejects_unsupported_type(self):
        with self.assertRaises(ImageRejected):
            validate_image(b"x", "application/pdf")

    def test_rejects_empty(self):
        with self.assertRaises(ImageRejected):
            validate_image(b"", "image/jpeg")

    def test_rejects_oversize(self):
        with self.assertRaises(ImageRejected):
            validate_image(b"x" * (MAX_IMAGE_BYTES + 1), "image/jpeg")

    def test_validation_happens_before_the_model_call(self):
        called = []

        def _c(*a, **k):
            called.append(1)
            return Completion(text=GOOD, model="m", finish_reason="stop")

        with self.assertRaises(ImageRejected):
            transcribe(b"", "image/jpeg", P, _complete=_c)
        self.assertEqual(called, [], "must not spend a model call on an invalid image")


class TestParsing(unittest.TestCase):
    def test_parses_steps_in_order(self):
        t = parse_transcription(GOOD, "m")
        self.assertEqual(t.as_lines(), ["2x + 5 = 13", "2x = 8", "x = 5"])
        self.assertEqual([s.index for s in t.steps], [0, 1, 2])

    def test_tolerates_a_code_fence(self):
        t = parse_transcription(f"```json\n{GOOD}\n```", "m")
        self.assertEqual(len(t.steps), 3)

    def test_transcription_starts_unconfirmed(self):
        self.assertFalse(parse_transcription(GOOD, "m").confirmed)

    def test_non_json_raises_rather_than_returning_nothing(self):
        with self.assertRaises(ProviderError):
            parse_transcription("I think the answer is x = 5", "m")

    def test_steps_not_a_list_raises(self):
        with self.assertRaises(ProviderError):
            parse_transcription(json.dumps({"legible": True, "steps": "2x=8"}), "m")

    def test_absurd_step_count_raises(self):
        payload = json.dumps({"legible": True, "steps": [f"line {i}" for i in range(500)]})
        with self.assertRaises(ProviderError):
            parse_transcription(payload, "m")


class TestLegibleVsError(unittest.TestCase):
    """The distinction that stops a broken vision path looking like bad handwriting."""

    def test_explicit_illegible_is_not_an_error_type(self):
        payload = json.dumps({"legible": False, "steps": [], "reason": "too blurry"})
        with self.assertRaises(NotLegible) as ctx:
            parse_transcription(payload, "m")
        self.assertIn("blurry", ctx.exception.reason)
        self.assertNotIsInstance(ctx.exception, ProviderError)

    def test_legible_true_with_no_steps_is_treated_as_unreadable(self):
        # A contradiction: the model neither read the page nor admitted it could not.
        payload = json.dumps({"legible": True, "steps": []})
        with self.assertRaises(NotLegible):
            parse_transcription(payload, "m")

    def test_whitespace_only_steps_are_unreadable_not_blank_working(self):
        payload = json.dumps({"legible": True, "steps": ["  ", "\n"]})
        with self.assertRaises(NotLegible):
            parse_transcription(payload, "m")


class TestConfirmationContract(unittest.TestCase):
    """FR-026. At 87.5% accuracy roughly one line in eight is wrong, and the student is the
    authority on their own page."""

    def setUp(self):
        self.t = parse_transcription(GOOD, "m")

    def test_transcribe_never_returns_confirmed(self):
        out = transcribe(b"fake-bytes", "image/jpeg", P, _complete=completes_with(GOOD))
        self.assertFalse(out.confirmed, "FR-026: the student must see it first")

    def test_confirm_marks_confirmed_without_changing_text(self):
        c = self.t.confirm()
        self.assertTrue(c.confirmed)
        self.assertEqual(c.as_lines(), self.t.as_lines())

    def test_correction_replaces_only_that_line(self):
        c = self.t.correct({1: "2x = 18"})
        self.assertEqual(c.as_lines(), ["2x + 5 = 13", "2x = 18", "x = 5"])

    def test_correction_implies_confirmation(self):
        self.assertTrue(self.t.correct({0: "2x + 5 = 31"}).confirmed)

    def test_correction_to_a_missing_line_raises(self):
        # Silently dropping it would coach the student on working they rejected.
        with self.assertRaises(IndexError):
            self.t.correct({99: "nope"})

    def test_original_is_unchanged_by_correction(self):
        self.t.correct({0: "changed"})
        self.assertEqual(self.t.as_lines()[0], "2x + 5 = 13")
        self.assertFalse(self.t.confirmed)

    def test_prompt_is_about_our_reading_not_their_work(self):
        text = confirmation_prompt(self.t)
        self.assertIn("what I read", text)
        self.assertIn("1. 2x + 5 = 13", text)   # 1-indexed for a human
        self.assertNotIn("0.", text)


class TestTranscribeEndToEnd(unittest.TestCase):
    def test_returns_steps_from_a_well_formed_reply(self):
        out = transcribe(b"fake", "image/png", P, _complete=completes_with(GOOD))
        self.assertEqual(out.as_lines()[-1], "x = 5")
        self.assertEqual(out.model, "m")

    def test_preserves_the_student_s_mistake_verbatim(self):
        # The wrong sign is the entire point -- if the model "helpfully" fixed it, the tutor
        # has nothing to teach from.
        wrong = json.dumps({"legible": True, "steps": ["2x + 5 = 13", "2x = 18"]})
        out = transcribe(b"fake", "image/jpeg", P, _complete=completes_with(wrong))
        self.assertEqual(out.as_lines()[1], "2x = 18")


if __name__ == "__main__":
    unittest.main(verbosity=2)
