"""Photo of the student's working -> the steps they wrote. Slice 2.

Implements ADR-016 (a multimodal LLM reads the photo inline -- no second vendor, no metered
per-page bill) and FR-026, which exists because of a measurement:

    PQ-01 measured 87.5% transcription accuracy on real human handwriting.

Roughly one line in eight is misread. Without confirmation the tutor coaches working the
student never wrote, confidently, which destroys trust faster than admitting it cannot read.
So the transcription is ALWAYS shown back before any reasoning happens.

Two distinctions this module is careful about, both inherited from ADR-015:

    "the page is blank / I cannot read this"  -> a VALID result. Say so, ask for a retake.
    the model returned nothing at all         -> an ERROR. Never a blank page.

Conflating those is how a broken vision path comes to look like a student with bad
handwriting.

Model output is untrusted (HLD trust boundary 2), so parsing is defensive throughout.
"""

from __future__ import annotations

import base64
import json
import re
from dataclasses import dataclass, field

from llm import Completion, Provider, ProviderError, complete

# Trust boundary 1: student input is hostile. Size-cap before anything else -- a 40 MB photo
# is a bill and a timeout, not a maths problem.
MAX_IMAGE_BYTES = 6 * 1024 * 1024
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "image/heic"}

# Bounds a plausible page of school working. Outside these, something is wrong with the
# photo or the parse, and guessing is worse than asking for a retake.
MAX_STEPS = 40

SYSTEM = """\
You transcribe a photograph of a school student's handwritten maths working.

You do NOT solve, correct, hint at, or comment on the mathematics. You only report what is
physically written on the page, line by line, in order.

Return ONLY a JSON object, no prose and no code fence:

  {"legible": true, "steps": ["<line 1>", "<line 2>", ...]}

Rules:
- One array entry per written line of working.
- Use LaTeX for mathematical notation, without surrounding $ signs.
- Transcribe mistakes EXACTLY as written. A wrong sign is the whole point; do not fix it.
- Omit crossed-out lines.
- If the page is blank, out of focus, or you cannot read it, return
  {"legible": false, "steps": [], "reason": "<short reason>"}
"""


class NotLegible(Exception):
    """The model read the page and reported it cannot be transcribed. A valid outcome."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


class ImageRejected(ValueError):
    """Failed validation before any model call."""


@dataclass(frozen=True)
class Step:
    index: int
    text: str


@dataclass
class Transcription:
    """What we believe the student wrote. Unconfirmed until the student says so."""

    steps: list[Step]
    confirmed: bool = False
    model: str = ""
    raw: str = field(default="", repr=False)

    def as_lines(self) -> list[str]:
        return [s.text for s in self.steps]

    def confirm(self) -> "Transcription":
        return Transcription(self.steps, True, self.model, self.raw)

    def correct(self, corrections: dict[int, str]) -> "Transcription":
        """Apply the student's edits. FR-026: they are the authority on their own page.

        A correction to a line that does not exist is a bug in the caller, not something to
        ignore -- ignoring it means the student's fix silently disappears and they get
        coached on working they explicitly rejected.
        """
        valid = {s.index for s in self.steps}
        unknown = set(corrections) - valid
        if unknown:
            raise IndexError(f"corrections for non-existent steps: {sorted(unknown)}")
        steps = [Step(s.index, corrections.get(s.index, s.text)) for s in self.steps]
        # Corrected implies confirmed: the student has just told us what it says.
        return Transcription(steps, True, self.model, self.raw)


def validate_image(data: bytes, mime: str) -> None:
    if mime not in ALLOWED_MIME:
        raise ImageRejected(f"unsupported type {mime!r}")
    if not data:
        raise ImageRejected("empty image")
    if len(data) > MAX_IMAGE_BYTES:
        raise ImageRejected(
            f"image is {len(data) // 1024} KB, limit is {MAX_IMAGE_BYTES // 1024} KB"
        )


def _strip_fence(text: str) -> str:
    """Models wrap JSON in ``` despite being told not to. Cheap to tolerate."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\s*", "", t)
        t = re.sub(r"\s*```$", "", t)
    return t.strip()


def parse_transcription(raw: str, model: str = "") -> Transcription:
    """Parse the model's reply. Defensive: its output is untrusted."""
    try:
        data = json.loads(_strip_fence(raw))
    except json.JSONDecodeError as e:
        raise ProviderError(f"{model}: transcription was not JSON ({e}): {raw[:200]!r}")

    if not isinstance(data, dict):
        raise ProviderError(f"{model}: expected a JSON object, got {type(data).__name__}")

    if data.get("legible") is False:
        raise NotLegible(str(data.get("reason") or "the page could not be read"))

    steps_raw = data.get("steps")
    if not isinstance(steps_raw, list):
        raise ProviderError(f"{model}: 'steps' missing or not a list")

    lines = [str(s).strip() for s in steps_raw if str(s).strip()]

    # Empty steps with legible=true is a contradiction: the model neither read the page nor
    # admitted it could not. Treat as unreadable rather than as a student who wrote nothing.
    if not lines:
        raise NotLegible("no working was found on the page")

    if len(lines) > MAX_STEPS:
        raise ProviderError(
            f"{model}: {len(lines)} steps exceeds the {MAX_STEPS} plausible for one page"
        )

    return Transcription(
        steps=[Step(i, t) for i, t in enumerate(lines)], model=model, raw=raw
    )


def transcribe(
    image: bytes,
    mime: str,
    provider: Provider,
    *,
    _complete=complete,
) -> Transcription:
    """Read a photo of working. Raises NotLegible if the page cannot be read.

    Always returns an UNCONFIRMED transcription: FR-026 requires the student to see it
    before any reasoning happens.
    """
    validate_image(image, mime)
    b64 = base64.b64encode(image).decode()

    if provider.kind == "gemini":
        user = json.dumps({"inline_data": {"mime_type": mime, "data": b64}})
    else:
        user = json.dumps(
            [{"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}]
        )

    out: Completion = _complete(provider, SYSTEM, user)
    return parse_transcription(out.text, out.model)


def confirmation_prompt(t: Transcription) -> str:
    """What the student sees before any tutoring. FR-026.

    Phrased as a question about OUR reading, not about their work -- at 87.5% accuracy the
    likelier error is ours, and a student asked "is this what you wrote?" in an accusing
    tone stops using the product.
    """
    lines = "\n".join(f"{s.index + 1}. {s.text}" for s in t.steps)
    return (
        "Here's what I read from your page. Did I get it right?\n\n"
        f"{lines}\n\n"
        "Tap any line to fix it if I misread something."
    )
