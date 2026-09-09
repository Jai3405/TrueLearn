#!/usr/bin/env python3
"""Build a PQ-01 test set from REAL human handwriting - no writing required.

`make_worksheet.py` needs someone to spend an hour copying items by hand. This does
not: it pulls real handwritten expressions from Google's MathWriting dataset (230k
human-written samples with LaTeX ground truth, public, no auth), filters them down to
school-level algebra, stacks several into a single image so the page looks like
multi-step working, and degrades the result to resemble a phone photo.

    python3 spikes/pq1_build_dataset.py --out ~/pq1 --pages 20
    python3 spikes/pq1_build_dataset.py --self-check

Why this beats a font-rendered fake: the strokes are genuinely human, with real
variation in slant, pressure, spacing and sloppiness. Fonts are too regular and would
flatter the model.

What it still is NOT, stated plainly:
  - The stacked lines are unrelated expressions, not a coherent derivation. A model
    cannot use "step 2 should follow from step 1" as a crutch, which makes this a
    HARDER transcription test than real working - but it removes the "does the model
    silently correct the student's error" question, which needs `make_worksheet.py`.
  - MathWriting skews academic, so the filter keeps only expressions a Grade 10-12
    student would plausibly write.

So: this measures the CORE capability (can a model read multi-line handwritten maths
off a degraded photo). If it fails here, FR-002 fails and nothing else matters.
"""

from __future__ import annotations

import argparse
import io
import json
import random
import re
import urllib.request
from pathlib import Path

DATASET = "deepcopy/MathWriting-human"
ROWS_API = "https://datasets-server.huggingface.co/rows"
REPO = Path(__file__).resolve().parent.parent

# WHITELIST, not blacklist. A blacklist was tried first and was far too permissive:
# it admitted set notation \{g_1,g_2,g_3\}, Greek letters (P=K\rho^{1+1/n}) and
# absurd exponents (418^{163}) simply because they contained a digit. A test set of
# academic notation would produce a PQ-01 number that says nothing about whether a
# model can read a Grade 10 student's homework.
_ALLOWED_CMDS = {"frac", "sqrt", "times", "div", "pi", "le", "ge", "neq", "pm"}
_CMD = re.compile(r"\\([a-zA-Z]+)")
_CHARS = re.compile(r"^[0-9a-zA-Z\s+\-*/^_=(),.<>\\{}\[\]]+$")
_BIG_EXP = re.compile(r"\^\{?\d{3,}")      # 418^{163} is not school maths
_SET_BRACE = re.compile(r"\\[{}]")          # \{ ... \} is set notation


def is_school_level(latex: str) -> bool:
    """Keep only expressions a Grade 10-12 student would plausibly write."""
    s = latex.strip()
    if not (3 <= len(s) <= 30):
        return False
    if not re.search(r"\d", s):                 # school maths has numbers in it
        return False
    if _SET_BRACE.search(s) or _BIG_EXP.search(s):
        return False
    if not _CHARS.match(s):
        return False
    if any(c not in _ALLOWED_CMDS for c in _CMD.findall(s)):
        return False
    # More than three distinct letters means physics-style symbol soup (dQU_{el}),
    # not the one or two variables school algebra uses.
    letters = set(re.sub(r"\\[a-zA-Z]+", "", s))
    if len({c for c in letters if c.isalpha()}) > 3:
        return False
    return True


def fetch_rows(offset: int, length: int) -> list[dict]:
    url = (f"{ROWS_API}?dataset={DATASET}&config=default&split=train"
           f"&offset={offset}&length={length}")
    with urllib.request.urlopen(url, timeout=90) as r:
        return [x["row"] for x in json.loads(r.read())["rows"]]


def build_page(images, rng, width=1000):
    """Stack expression crops vertically into one 'page of working', then make it
    look like it was photographed in a hurry: slight rotation, uneven lighting,
    blur and JPEG loss. Clean scans are not what the product will receive."""
    from PIL import Image, ImageDraw, ImageFilter

    pad, gap = 60, rng.randint(30, 70)
    rows = []
    for im in images:
        im = im.convert("L")
        scale = min(1.0, (width - 2 * pad) / im.width)
        if scale < 1.0:
            im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        rows.append(im)

    height = pad * 2 + sum(r.height for r in rows) + gap * (len(rows) - 1)
    page = Image.new("L", (width, height), 255)
    y = pad
    for r in rows:
        page.paste(r, (pad + rng.randint(0, 40), y))   # students don't align margins
        y += r.height + gap

    # ruled paper
    d = ImageDraw.Draw(page)
    for ly in range(pad, height, 45):
        d.line([(30, ly), (width - 30, ly)], fill=225, width=1)

    page = page.rotate(rng.uniform(-2.5, 2.5), expand=True, fillcolor=255)
    page = page.filter(ImageFilter.GaussianBlur(rng.uniform(0.3, 1.1)))

    # uneven indoor lighting: a soft gradient across the page
    grad = Image.linear_gradient("L").resize(page.size)
    if rng.random() < 0.5:
        grad = grad.transpose(Image.FLIP_LEFT_RIGHT)
    page = Image.blend(page, Image.composite(page, grad, page), rng.uniform(0.10, 0.28))
    return page


def latex_norm(s: str) -> str:
    """Comparison form. Strips the cosmetic LaTeX differences that are not
    transcription errors, so \\frac{1}{2} and \\frac {1}{2} score the same."""
    s = s.strip().strip("$")
    s = re.sub(r"\s+", "", s)
    s = s.replace("\\left", "").replace("\\right", "").replace("\\cdot", "*")
    s = re.sub(r"\{([0-9a-zA-Z])\}", r"\1", s)   # {x} -> x
    return s


def self_check() -> None:
    keep = ["3x+7=22", "x^{2}+5x+6", "\\frac{3}{4}+\\frac{1}{2}", "\\sqrt{16}=4",
            "2\\pi r^{2}", "y=5x-3"]
    for s in keep:
        assert is_school_level(s), f"should keep school maths: {s}"

    # Every one of these was wrongly admitted by the first blacklist version.
    drop = ["V(\\tilde{\\beta})", "GL(V)\\times S_{n}",
            "\\{g_{1},g_{2},g_{3}\\}",                  # set notation
            "\\frac{418^{163}}{(197^{4}\\cdot10)}",      # absurd exponent
            "P=K\\rho^{1+1/n}",                          # Greek / physics
            "u_{0}=\\frac{4}{(n\\pi)^{2}}dQU_{el}",      # symbol soup
            "g(z)=\\frac{1}{f(z)-\\mu}",                 # \mu
            "abc",                                        # no digits
            "x" * 60]                                     # too long
    for s in drop:
        assert not is_school_level(s), f"should drop non-school maths: {s}"
    assert latex_norm("\\frac{1}{2}") == latex_norm("\\frac {1} {2}")
    assert latex_norm("{x}^{2}") == latex_norm("x^2")
    assert latex_norm("$3x+7=22$") == "3x+7=22"
    print("self-check OK - school-level filter and LaTeX normaliser behave")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, help="output directory (keep it OUTSIDE this repo)")
    p.add_argument("--pages", type=int, default=20)
    p.add_argument("--lines", type=int, default=4, help="expressions stacked per page")
    p.add_argument("--seed", type=int, default=20260909)
    p.add_argument("--scan", type=int, default=1200,
                   help="dataset rows to scan for school-level samples")
    p.add_argument("--self-check", action="store_true")
    args = p.parse_args()

    if args.self_check:
        self_check()
        return 0
    if not args.out:
        p.error("--out is required (or use --self-check)")
    if REPO in args.out.resolve().parents:
        print(f"error: {args.out} is inside the repo; keep generated images out of git.")
        return 2

    from PIL import Image

    rng = random.Random(args.seed)
    need = args.pages * args.lines
    print(f"scanning up to {args.scan} rows for {need} school-level expressions...")

    picked = []
    for off in range(0, args.scan, 100):
        for row in fetch_rows(off, 100):
            if is_school_level(row["latex"]):
                picked.append(row)
        print(f"  scanned {min(off + 100, args.scan)}, kept {len(picked)}")
        if len(picked) >= need:
            break
    if len(picked) < need:
        print(f"only found {len(picked)} usable expressions; reducing to "
              f"{len(picked) // args.lines} pages")
        args.pages = len(picked) // args.lines
        if args.pages == 0:
            print("no usable expressions found - widen --scan or relax the filter")
            return 1

    args.out.mkdir(parents=True, exist_ok=True)
    truth, k = {}, 0
    for i in range(1, args.pages + 1):
        group = picked[k:k + args.lines]
        k += args.lines
        ims = []
        for row in group:
            raw = urllib.request.urlopen(row["image"]["src"], timeout=90).read()
            ims.append(Image.open(io.BytesIO(raw)))
        name = f"{i:02d}.jpg"
        build_page(ims, rng).convert("RGB").save(args.out / name, "JPEG",
                                                 quality=rng.randint(55, 80))
        truth[name] = [r["latex"] for r in group]
        print(f"  wrote {name}  ({args.lines} lines)")

    (args.out / "truth.json").write_text(json.dumps(truth, indent=2) + "\n")
    print(f"\n{args.pages} pages + truth.json in {args.out}")
    print(f"next:  OPENROUTER_API_KEY=... python3 spikes/pq1_ocr.py "
          f"--images {args.out} --truth {args.out}/truth.json --latex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
