"""Tests for the provider layer. No network, no keys, no waiting.

Every case here corresponds to a failure that actually happened during the spikes and was
initially read as a capability problem. That is the point: these are regression tests
against wrong conclusions, not merely against wrong code.

    cd app && python3 -m unittest -v
"""

from __future__ import annotations

import contextlib
import os
import unittest

from llm import (
    Completion,
    EmptyCompletion,
    Provider,
    ProviderError,
    TransientError,
    TruncatedCompletion,
    complete,
)

OPENAI = Provider(name="t", model="test-model", api_key_env="TEST_KEY",
                  base_url="https://example.invalid/v1", kind="openai")
GEMINI = Provider(name="t", model="test-model", api_key_env="TEST_KEY",
                  base_url="https://example.invalid/v1beta", kind="gemini")

NOSLEEP = lambda _: None  # noqa: E731


@contextlib.contextmanager
def _env(clear: bool = False):
    old = os.environ.get("TEST_KEY")
    if clear:
        os.environ.pop("TEST_KEY", None)
    else:
        os.environ["TEST_KEY"] = "supersecret"
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("TEST_KEY", None)
        else:
            os.environ["TEST_KEY"] = old


def fake_post(*responses):
    """A post() that yields each response in turn, so retries are observable."""
    seq = list(responses)
    calls = []

    def _post(url, payload, headers, timeout=None):
        calls.append({"url": url, "payload": payload, "headers": headers})
        item = seq.pop(0) if len(seq) > 1 else seq[0]
        if isinstance(item, Exception):
            raise item
        return item

    _post.calls = calls
    return _post


def ok_openai(text="hello", finish="stop"):
    return {"choices": [{"message": {"content": text}, "finish_reason": finish}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 3}}


def ok_gemini(text="hello", finish="STOP"):
    return {"candidates": [{"content": {"parts": [{"text": text}]}, "finishReason": finish}],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 3}}


class TestEmptyIsAnError(unittest.TestCase):
    """ADR-015. Silence scored as 'the tutor held the line' -- the bug that made a broken
    step-down look like correct behaviour, on the retention path."""

    def test_completion_cannot_hold_empty_text(self):
        with self.assertRaises(EmptyCompletion):
            Completion(text="", model="m", finish_reason="stop")

    def test_completion_cannot_hold_whitespace(self):
        with self.assertRaises(EmptyCompletion):
            Completion(text="   \n  ", model="m", finish_reason="stop")

    def test_openai_empty_content_raises(self):
        with _env(), self.assertRaises(EmptyCompletion):
            complete(OPENAI, "s", "u", post=fake_post(ok_openai(text="")), sleep=NOSLEEP)

    def test_gemini_no_candidates_raises(self):
        with _env(), self.assertRaises(EmptyCompletion):
            complete(GEMINI, "s", "u",
                     post=fake_post({"promptFeedback": {"blockReason": "SAFETY"}}),
                     sleep=NOSLEEP)


class TestTruncationIsNotAShortAnswer(unittest.TestCase):
    """PQ-01: gemini-3.5-flash scored 58.3% against flash-lite's 85.4% and looked like a
    worse model. It was truncation at maxOutputTokens, with finishReason never checked."""

    def test_openai_finish_length_raises_even_with_text(self):
        with _env(), self.assertRaises(TruncatedCompletion):
            complete(OPENAI, "s", "u",
                     post=fake_post(ok_openai(text="3x^2 -", finish="length")),
                     sleep=NOSLEEP)

    def test_gemini_max_tokens_raises(self):
        with _env(), self.assertRaises(TruncatedCompletion):
            complete(GEMINI, "s", "u",
                     post=fake_post(ok_gemini(text="partial", finish="MAX_TOKENS")),
                     sleep=NOSLEEP)

    def test_gemini_safety_stop_is_distinct_from_empty(self):
        with _env(), self.assertRaises(ProviderError) as ctx:
            complete(GEMINI, "s", "u", post=fake_post(ok_gemini(text="x", finish="SAFETY")),
                     sleep=NOSLEEP)
        self.assertNotIsInstance(ctx.exception, EmptyCompletion)


class TestProviderErrorInA200Body(unittest.TestCase):
    """SPK-1 reported 22.2% leakage over a run where 17/26 attacks had errored, because
    OpenRouter returns provider failures as HTTP 200 with an `error` body."""

    def test_error_in_200_body_is_transient_not_empty(self):
        with _env(), self.assertRaises(TransientError):
            complete(OPENAI, "s", "u",
                     post=fake_post({"error": {"message": "upstream 503"}}), sleep=NOSLEEP)


class TestRetries(unittest.TestCase):
    def test_transient_then_success(self):
        with _env():
            post = fake_post(TransientError("429"), ok_openai("recovered"))
            out = complete(OPENAI, "s", "u", post=post, sleep=NOSLEEP)
            self.assertEqual(out.text, "recovered")
            self.assertEqual(len(post.calls), 2)

    def test_gives_up_and_preserves_the_error_type(self):
        with _env(), self.assertRaises(TruncatedCompletion):
            complete(OPENAI, "s", "u", post=fake_post(ok_openai(text="", finish="length")),
                     sleep=NOSLEEP, max_retries=2)

    def test_does_not_retry_a_non_transient_http_error(self):
        with _env():
            post = fake_post(ProviderError("HTTP 400: bad request"))
            with self.assertRaises(ProviderError):
                complete(OPENAI, "s", "u", post=post, sleep=NOSLEEP)
            self.assertEqual(len(post.calls), 1, "a 400 must not be retried")


class TestCredentialHandling(unittest.TestCase):
    def test_missing_key_fails_loudly_before_any_request(self):
        post = fake_post(ok_openai())
        with _env(clear=True), self.assertRaises(ProviderError) as ctx:
            complete(OPENAI, "s", "u", post=post, sleep=NOSLEEP)
        self.assertIn("TEST_KEY", str(ctx.exception))
        self.assertEqual(len(post.calls), 0, "must not call out without a key")

    def test_key_never_reaches_the_request_body(self):
        with _env():
            post = fake_post(ok_openai())
            complete(OPENAI, "s", "u", post=post, sleep=NOSLEEP)
            self.assertNotIn("supersecret", str(post.calls[0]["payload"]))


class TestHappyPath(unittest.TestCase):
    def test_openai_returns_text_and_usage(self):
        with _env():
            out = complete(OPENAI, "s", "u", post=fake_post(ok_openai("2x + 1")),
                           sleep=NOSLEEP)
            self.assertEqual(out.text, "2x + 1")
            self.assertEqual(out.output_tokens, 3)

    def test_gemini_concatenates_parts(self):
        with _env():
            resp = {"candidates": [{"content": {"parts": [{"text": "a"}, {"text": "b"}]},
                                    "finishReason": "STOP"}]}
            out = complete(GEMINI, "s", "u", post=fake_post(resp), sleep=NOSLEEP)
            self.assertEqual(out.text, "ab")


if __name__ == "__main__":
    unittest.main(verbosity=2)
