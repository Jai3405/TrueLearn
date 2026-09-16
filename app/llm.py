"""Provider abstraction. Implements ADR-007, and enforces ADR-015.

ADR-007: one thin interface, more than one implementation, so the model stays swappable.
ADR-009 gave that a dated reason to exist -- 13 May 2027 -- and a commercial one: a school
demanding in-country inference becomes a config change behind this, not a rewrite.

ADR-015 is the part that matters most, and it is enforced here rather than left to each
call site:

    An empty or truncated model response is an ERROR, never a value.

Measured across two harnesses and three model families: reasoning models spend the output
budget on internal reasoning and return empty `content` with finish_reason `length`. Every
harness that did not check scored that silence as good behaviour -- a broken step-down
looked like a tutor correctly holding the line. In production it is a student who asked for
help and got nothing.

Stdlib only. No dependency earns its install here yet.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

DEFAULT_TIMEOUT = 90
MAX_RETRIES = 3
BACKOFF_BASE = 2.0


class ProviderError(RuntimeError):
    """Base for anything the provider layer raises."""


class TransientError(ProviderError):
    """Rate limit, 5xx, or transport failure. Retryable.

    Separate from capability failures on purpose: SPK-1 once reported 22.2% leakage over a
    run where 17 of 26 attacks had actually errored, because OpenRouter returns provider
    failures as HTTP 200 with an `error` body. Rate limits were being scored as the model
    failing to behave.
    """


class EmptyCompletion(ProviderError):
    """The model returned no text. ADR-015: an error, never an empty string."""


class TruncatedCompletion(ProviderError):
    """finish_reason == length. A truncated answer is not a short answer."""


@dataclass
class Completion:
    text: str
    model: str
    finish_reason: str
    prompt_tokens: int = 0
    output_tokens: int = 0

    def __post_init__(self) -> None:
        # Belt and braces: nothing constructs a Completion holding silence.
        if not self.text or not self.text.strip():
            raise EmptyCompletion(f"{self.model} returned empty content")


@dataclass
class Provider:
    """One OpenAI-compatible or Gemini endpoint.

    `base_url` makes OpenRouter, a local gateway, or any /v1-compatible service the same
    code path. That portability is what let the spikes keep measuring when one provider
    rate-limited us.
    """

    name: str
    model: str
    api_key_env: str
    base_url: str
    kind: str = "openai"          # "openai" | "gemini"
    max_output_tokens: int = 2048
    extra_headers: dict = field(default_factory=dict)

    def api_key(self) -> str:
        key = os.environ.get(self.api_key_env, "").strip()
        if not key:
            raise ProviderError(
                f"{self.api_key_env} is not set. Pass credentials via the environment; "
                f"they must never be written to a file in this repo."
            )
        return key


def _post(url: str, payload: dict, headers: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        if e.code in (408, 429, 500, 502, 503, 504):
            raise TransientError(f"HTTP {e.code}: {body}") from e
        raise ProviderError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise TransientError(f"transport: {e.reason}") from e


def _parse_openai(data: dict, model: str) -> Completion:
    # OpenRouter signals provider failure as HTTP 200 with an `error` body. Checked first,
    # because otherwise it parses as an empty completion and looks like a model problem.
    if data.get("error"):
        raise TransientError(f"provider error in 200 body: {str(data['error'])[:300]}")

    choices = data.get("choices") or []
    if not choices:
        raise EmptyCompletion(f"{model}: no choices in response")

    choice = choices[0]
    finish = choice.get("finish_reason") or choice.get("native_finish_reason") or ""
    text = (choice.get("message") or {}).get("content") or ""
    usage = data.get("usage") or {}

    if finish == "length" and not text.strip():
        raise TruncatedCompletion(
            f"{model}: finish_reason=length with empty content -- the output budget went "
            f"on internal reasoning. Raise max tokens or simplify the prompt (ADR-015)."
        )
    if finish == "length":
        raise TruncatedCompletion(f"{model}: response truncated mid-generation")

    return Completion(
        text=text, model=model, finish_reason=finish or "stop",
        prompt_tokens=usage.get("prompt_tokens", 0),
        output_tokens=usage.get("completion_tokens", 0),
    )


def _parse_gemini(data: dict, model: str) -> Completion:
    candidates = data.get("candidates") or []
    if not candidates:
        # A prompt blocked by safety filters lands here. Surfaced explicitly rather than as
        # "empty", because the fix is different.
        fb = data.get("promptFeedback") or {}
        raise EmptyCompletion(f"{model}: no candidates (promptFeedback={fb})")

    cand = candidates[0]
    finish = cand.get("finishReason") or ""
    parts = (cand.get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts)
    usage = data.get("usageMetadata") or {}

    if finish == "MAX_TOKENS":
        raise TruncatedCompletion(
            f"{model}: finishReason=MAX_TOKENS. This is the failure that made "
            f"gemini-3.5-flash look 27 points worse than flash-lite in PQ-01 (ADR-015)."
        )
    if finish in ("SAFETY", "RECITATION"):
        raise ProviderError(f"{model}: generation stopped, finishReason={finish}")

    return Completion(
        text=text, model=model, finish_reason=finish or "STOP",
        prompt_tokens=usage.get("promptTokenCount", 0),
        output_tokens=usage.get("candidatesTokenCount", 0),
    )


def complete(
    provider: Provider,
    system: str,
    user: str,
    *,
    max_retries: int = MAX_RETRIES,
    sleep=time.sleep,
    post=_post,
) -> Completion:
    """Call the model. Raises rather than ever returning silence.

    `post` and `sleep` are injectable so the tests run with no network and no waiting.
    """
    if provider.kind == "gemini":
        url = (f"{provider.base_url}/models/{provider.model}:generateContent"
               f"?key={provider.api_key()}")
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"maxOutputTokens": provider.max_output_tokens},
        }
        headers = {"Content-Type": "application/json", **provider.extra_headers}
        parse = _parse_gemini
    else:
        url = f"{provider.base_url}/chat/completions"
        payload = {
            "model": provider.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": provider.max_output_tokens,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {provider.api_key()}",
            **provider.extra_headers,
        }
        parse = _parse_openai

    last: Exception | None = None
    for attempt in range(max_retries):
        try:
            return parse(post(url, payload, headers), provider.model)
        except (TransientError, EmptyCompletion, TruncatedCompletion) as e:
            # Empty and truncated are retried too: measured, they are often a transient
            # budget artefact rather than a deterministic property of the prompt.
            last = e
            if attempt < max_retries - 1:
                sleep(BACKOFF_BASE ** attempt)
    raise type(last)(f"after {max_retries} attempts: {last}") from last


# Registry. Exact model ids, never "-latest" in production config: a provider silently
# re-pointing an alias is a regression with no diff to review (02-test-and-eval-strategy 5).
PROVIDERS = {
    "gemini": Provider(
        name="gemini",
        model="gemini-flash-lite-latest",   # TODO: pin an exact id before production
        api_key_env="GEMINI_API_KEY",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        kind="gemini",
    ),
    "openrouter": Provider(
        name="openrouter",
        model="google/gemini-2.0-flash-exp:free",
        api_key_env="OPENROUTER_API_KEY",
        base_url="https://openrouter.ai/api/v1",
        kind="openai",
    ),
}
