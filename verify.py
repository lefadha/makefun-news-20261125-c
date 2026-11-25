"""Local mirror of the gate and of the judged craft rules for arm 3.

  1. the committed entry.png is a whole 1024x1024 PNG under 1 MiB;
  2. two fresh renders are byte-identical and identical to the committed file;
  3. main.ts, run twice, ships exactly those bytes;
  4. no ink in the 12 px border; light paper 70-90%; colour 8-25% (the paid band
     measured on this competition's live board, 25 Nov 05:35Z, is 8.8-15.8%);
  5. every one of the 48 cards carries drawn ink in its scene strip;
  6. the page reads at full size: the date, all 8 region chips, all 5 figures and
     at least 44 of the 48 headlines; and the day still reads at 300 px;
  7. the page's own arithmetic: 48 stories, chips summing to 48.

Run: node /opt/data/runpy.js /opt/data/ocr-venv/bin/python verify.py
"""
import hashlib
import os
import re
import struct
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

import render
import stories

HERE = os.path.dirname(os.path.abspath(__file__))
passes, fails = [], []


def check(name, ok, detail=""):
    (passes if ok else fails).append(name)
    print(("PASS " if ok else "FAIL ") + name + ((" -- " + detail) if detail else ""))


def analyse(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    m = np.zeros(lum.shape, bool)
    m[:12, :] = m[-12:, :] = True
    m[:, :12] = m[:, -12:] = True
    return dict(size=im.size, light=float((lum > 200).mean()) * 100,
                colour=float(((sat > 40) & (lum < 245)).mean()) * 100,
                edge=float((lum[m] < 160).mean()) * 100,
                arr=lum)


def main():
    png = os.path.join(HERE, "entry.png")
    raw = open(png, "rb").read()

    check("png signature", raw[:8] == b"\x89PNG\r\n\x1a\n")
    w, h = struct.unpack(">II", raw[16:24])
    check("1024x1024", (w, h) == (1024, 1024), "%dx%d" % (w, h))
    check("under 1 MiB", len(raw) <= 1048576, "%d bytes" % len(raw))

    tmp = tempfile.mkdtemp()
    a, b = os.path.join(tmp, "a.png"), os.path.join(tmp, "b.png")
    render.render(a)
    render.render(b)
    ha, hb = [hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (a, b)]
    check("two runs byte-identical", ha == hb, ha[:12])
    check("committed == fresh render", ha == hashlib.sha256(raw).hexdigest(), ha[:12])

    for i in (1, 2):
        out = os.path.join(tmp, "out%d" % i)
        env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out)
        r = subprocess.run(["node", "main.ts"], cwd=HERE, env=env, capture_output=True, text=True)
        check("main.ts run %d" % i, r.returncode == 0, r.stderr.strip()[:120])
        if r.returncode == 0:
            got = open(os.path.join(out, "entry.png"), "rb").read()
            check("main.ts run %d ships the committed bytes" % i, got == raw)

    st = analyse(png)
    check("no ink in the 12 px border", st["edge"] == 0.0, "%.2f%%" % st["edge"])
    check("light paper 70-90%", 70 <= st["light"] <= 90, "%.1f%%" % st["light"])
    check("colour 8-25% (paid band 8.8-15.8)", 8 <= st["colour"] <= 25, "%.1f%%" % st["colour"])

    # every card's scene strip carries drawn ink
    lum = st["arr"]
    cols, rows = 6, 8
    top, bottom, gap = 172.0, 1002.0, 4.0
    cw = (992.0 - 5 * gap) / 6
    rh = (bottom - top - 7 * gap) / 8
    empty = []
    inks = []
    for i in range(48):
        r_, c_ = divmod(i, cols)
        x = int(16 + c_ * (cw + gap))
        y = int(top + r_ * (rh + gap))
        patch = lum[y + 2:y + 36, x + 2:x + int(cw) - 2]
        ink = float((patch < 235).mean()) * 100
        inks.append(round(ink, 1))
        if ink < 40:
            empty.append((i, round(ink, 1)))
    check("a drawn scene in all 48 cards", not empty, "ink %.0f-%.0f%%" % (min(inks), max(inks)))

    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()

    def read(path):
        res, _ = ocr(path, use_det=True, use_cls=False, use_rec=True)
        return [(t, float(c)) for _, t, c in (res or [])]

    full = read(png)
    small_path = os.path.join(tmp, "small.png")
    Image.open(png).convert("RGB").resize((300, 300), Image.LANCZOS).save(small_path)
    small = read(small_path)

    def norm(s):
        return re.sub(r"[^a-z0-9]", "", s.lower())

    nf = norm(" ".join(t for t, c in full if c > 0.5))
    ns = norm(" ".join(t for t, c in small if c > 0.5))

    check("date in masthead", norm(stories.DAY) in nf)
    check("at 300 px the day still reads", norm(stories.DAY) in ns)
    for fig, lab in stories.NUMBERS:
        check("figure %s readable" % fig, norm(fig) in nf, fig)
    heads_ok = 0
    for place, region, desk, status, head, src, utc, scene in stories.STORIES:
        words = [w for w in re.findall(r"[A-Za-z0-9']+", head) if len(w) > 3]
        hit = sum(1 for w in words if norm(w) in nf)
        if hit >= max(2, len(words) - 1):
            heads_ok += 1
    check("44 of 48 headlines readable at full size", heads_ok >= 44, "%d/48" % heads_ok)
    tally = stories.counts()
    check("48 stories on the page", sum(tally.values()) == 48, str(sum(tally.values())))
    check("8 regions on the chips", len(tally) == 8, str(len(tally)))
    chips = 0
    for reg in tally:
        if norm(reg) in nf:
            chips += 1
    check("chip labels readable", chips == 8, "%d/8" % chips)

    print("\n%d pass, %d fail" % (len(passes), len(fails)))
    if fails:
        print("FAILED: " + ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
