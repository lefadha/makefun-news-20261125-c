"""Draw Wednesday 25 November 2026 as one front page: 48 dated stories, a drawn
scene in every card, one page a reader can take in at a glance.

Measured basis (25 Nov, 05:35Z): the live board of this competition puts seat 10 at
983,776 and the leader at 987,339 over a graded field of 554; the top page carries
50 dated stories over 6 continents with a map, its colour share is 15.8% against our
arm 2's 4.6%, and it keeps only 20 text runs readable at 300 px -- so breadth and a
picture per story separate the paid band far more than miniature legibility does.
This arm keeps arm 2's structure (masthead date, region chips, numbers strip, outlet
line under every story) and spends its one change on the cards: every one of the 48
stories now carries its own drawn scene, 40 logical px tall, drawn with primitives.

Run: node /opt/data/runpy.js /opt/data/ocr-venv/bin/python render.py entry.png
"""
import sys

from PIL import Image, ImageDraw, ImageFont

from stories import (DAY, EDITION, STAMP, STORIES, NUMBERS, REGION_COLOURS, counts)

SS = 2
W = H = 1024
PAPER = (252, 251, 248)
INK = (18, 18, 20)
BODY = (48, 48, 56)
GREY = (92, 92, 100)
HAIR = (176, 176, 182)
ACCENT = (214, 132, 40)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, round(size, 1))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, int(round(size * SS)))
    return _cache[key]


def tw(d, txt, f):
    box = d.textbbox((0, 0), txt, font=f)
    return (box[2] - box[0]) / SS


def draw_text(d, xy, txt, f, fill=INK, anchor="la"):
    d.text((xy[0] * SS, xy[1] * SS), txt, font=f, fill=fill, anchor=anchor)


def wrap(d, txt, f, width):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_block(d, txt, path, size, width, max_lines, min_size=9.0):
    s = size
    while s >= min_size:
        f = font(path, s)
        lines = wrap(d, txt, f, width)
        if len(lines) <= max_lines and all(tw(d, ln, f) <= width for ln in lines):
            return f, lines, s
        s -= 0.5
    f = font(path, min_size)
    return f, wrap(d, txt, f, width), min_size


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ------------------------------------------------------------------ scenes
# Every scene is drawn in unit coordinates (0..1 of its own box) so the same code
# serves a 161x40 card and any larger panel. Paper stays light; the subject is the
# region colour at 88% strength, so a card is a small illustration, not a block.

def draw_scene(d, kind, box, col):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    def px(u):
        return (x0 + u * w) * SS

    def py(v):
        return (y0 + v * h) * SS

    def rect(u0, v0, u1, v1, fill):
        d.rectangle((px(u0), py(v0), px(u1), py(v1)), fill=fill)

    def poly(pts, fill):
        d.polygon([(px(u), py(v)) for u, v in pts], fill=fill)

    def ell(u, v, ru, rv, fill):
        d.ellipse((px(u) - ru * w * SS, py(v) - rv * h * SS,
                   px(u) + ru * w * SS, py(v) + rv * h * SS), fill=fill)

    def line(u0, v0, u1, v1, width, fill):
        d.line((px(u0), py(v0), px(u1), py(v1)), fill=fill, width=max(1, int(width * SS)))

    strong = mix(col, PAPER, 0.10)
    mid = mix(col, PAPER, 0.42)
    pale = mix(col, PAPER, 0.80)
    sky = mix(col, PAPER, 0.90)
    dark = mix(col, INK, 0.35)

    rect(0, 0, 1, 1, sky)
    horiz = 0.62

    if kind in ("ship", "tanker", "port"):
        rect(0, horiz, 1, 1, mix((36, 84, 120), PAPER, 0.72))
        for i in range(3):
            line(0.02, horiz + 0.10 + i * 0.10, 0.98, horiz + 0.10 + i * 0.10, 0.8,
                 mix((36, 84, 120), PAPER, 0.55))
        if kind == "port":
            line(0.30, horiz, 1.0, horiz, 2.0, dark)
            for cx in (0.38, 0.62, 0.86):
                line(cx, horiz - 0.60, cx, horiz, 1.6, dark)
                line(cx, horiz - 0.60, cx + 0.22, horiz - 0.60, 1.6, dark)
                line(cx + 0.22, horiz - 0.60, cx + 0.22, horiz - 0.44, 1.2, dark)
            for i, bx in enumerate((0.06, 0.16, 0.26)):
                rect(bx, horiz - 0.20 - i * 0.02, bx + 0.08, horiz, strong if i % 2 else ACCENT)
        else:
            poly([(0.18, horiz + 0.20), (0.86, horiz + 0.20), (0.80, horiz + 0.44), (0.24, horiz + 0.44)], dark)
            for i, cx in enumerate((0.30, 0.46, 0.62, 0.78)):
                rect(cx - 0.05, horiz + 0.02, cx + 0.05, horiz + 0.20,
                     [ACCENT, strong, mid][i % 3])
            rect(0.30, horiz - 0.16, 0.40, horiz + 0.02, mid)
            if kind == "tanker":
                for i, (fx, fy) in enumerate(((0.48, horiz), (0.62, horiz + 0.04), (0.74, horiz - 0.02))):
                    ell(fx, fy, 0.05, 0.35, mix(ACCENT, PAPER, 0.2 + 0.2 * i))
                    ell(fx, fy - 0.42 - 0.12 * i, 0.06, 0.45, mix(GREY, PAPER, 0.45))

    elif kind == "drone":
        rect(0, 0.55, 1, 1, pale)
        line(0.5, 0.10, 0.5, 0.52, 2.0, dark)
        rect(0.34, 0.44, 0.66, 0.56, dark)
        for s in (-1, 1):
            line(0.34, 0.36, 0.14 if s < 0 else 0.86, 0.30, 1.6, dark)
            ell(0.14 if s < 0 else 0.86, 0.30, 0.10, 0.10, mid)
        ell(0.5, 0.18, 0.05, 0.14, mix(ACCENT, PAPER, 0.25))

    elif kind == "blast":
        rect(0, 0.78, 1, 1, pale)
        for i, (u, r) in enumerate(((0.5, 0.34), (0.34, 0.20), (0.68, 0.22))):
            poly([(u - r, 0.80), (u - r * 0.4, 0.80 - r * 1.5), (u, 0.80 - r * 2.0),
                  (u + r * 0.5, 0.80 - r * 1.2), (u + r, 0.80)],
                 [mix(ACCENT, PAPER, 0.1), mix(ACCENT, PAPER, 0.35), mid][i])
        ell(0.50, 0.16, 0.22, 0.28, mix(GREY, PAPER, 0.55))

    elif kind == "virus":
        rect(0, 0.80, 1, 1, pale)
        for i in range(14):
            ang = i * 0.4488
            import math
            cu, cv = 0.5 + 0.34 * math.cos(ang), 0.44 + 0.34 * math.sin(ang) * 1.1
            line(0.5, 0.44, cu, cv, 1.2, strong)
            ell(cu, cv, 0.05, 0.09, strong)
        ell(0.5, 0.44, 0.26, 0.52, mid)
        ell(0.42, 0.34, 0.05, 0.10, PAPER)
        ell(0.60, 0.52, 0.04, 0.08, PAPER)

    elif kind == "gavel":
        rect(0, 0.74, 1, 1, pale)
        rect(0.12, 0.74, 0.88, 0.84, mid)
        poly([(0.44, 0.16), (0.74, 0.36), (0.60, 0.56), (0.30, 0.36)], dark)
        line(0.30, 0.36, 0.16, 0.66, 3.0, strong)

    elif kind == "ballot":
        rect(0, 0.76, 1, 1, pale)
        rect(0.24, 0.36, 0.76, 0.76, mid)
        rect(0.32, 0.48, 0.68, 0.52, PAPER)
        poly([(0.36, 0.20), (0.62, 0.20), (0.62, 0.50), (0.36, 0.50)], PAPER)
        line(0.40, 0.26, 0.58, 0.26, 1.2, strong)
        line(0.40, 0.32, 0.58, 0.32, 1.2, strong)
        poly([(0.42, 0.42), (0.47, 0.47), (0.58, 0.36)], None) if False else None
        line(0.42, 0.42, 0.47, 0.47, 2.0, ACCENT)
        line(0.47, 0.47, 0.58, 0.36, 2.0, ACCENT)

    elif kind == "person":
        rect(0, 0.82, 1, 1, pale)
        ell(0.5, 0.26, 0.11, 0.22, dark)
        poly([(0.34, 0.84), (0.38, 0.46), (0.62, 0.46), (0.66, 0.84)], mid)
        line(0.38, 0.56, 0.22, 0.70, 3.0, strong)
        line(0.62, 0.56, 0.78, 0.70, 3.0, strong)

    elif kind == "megaphone":
        rect(0, 0.84, 1, 1, pale)
        poly([(0.16, 0.40), (0.56, 0.16), (0.56, 0.72), (0.16, 0.52)], dark)
        rect(0.60, 0.24, 0.64, 0.64, strong)
        for i, r in enumerate((0.10, 0.17, 0.24)):
            d.arc((px(0.62), py(0.44) - r * h * SS, px(0.62) + r * w * SS * 1.4,
                   py(0.44) + r * h * SS), -60, 60, fill=mix(col, PAPER, 0.35), width=int(1.4 * SS))
        line(0.26, 0.56, 0.22, 0.86, 2.2, strong)

    elif kind == "money":
        rect(0, 0.84, 1, 1, pale)
        rect(0.10, 0.34, 0.62, 0.72, mix((70, 120, 90), PAPER, 0.25))
        rect(0.14, 0.38, 0.58, 0.68, mix((70, 120, 90), PAPER, 0.6))
        ell(0.36, 0.53, 0.11, 0.22, mix((70, 120, 90), PAPER, 0.25))
        poly([(0.64, 0.44), (0.90, 0.44), (0.90, 0.30), (0.98, 0.52), (0.90, 0.74), (0.90, 0.60),
              (0.64, 0.60)], ACCENT)
        line(0.70, 0.34, 0.70, 0.20, 1.6, strong)

    elif kind == "fire":
        rect(0, 0.80, 1, 1, pale)
        for i, (u, s) in enumerate(((0.32, 0.44), (0.52, 0.62), (0.72, 0.40))):
            poly([(u - 0.10 * s / 0.5, 0.82), (u, 0.82 - s * 1.2), (u + 0.10 * s / 0.5, 0.82)],
                 mix(ACCENT, PAPER, 0.05 + 0.12 * i))
            poly([(u - 0.04, 0.82), (u, 0.82 - s * 0.6), (u + 0.04, 0.82)], mix((255, 214, 120), PAPER, 0.1))
        for i, (u, v) in enumerate(((0.40, 0.14), (0.58, 0.08), (0.74, 0.18))):
            ell(u, v, 0.10, 0.20, mix(GREY, PAPER, 0.5))

    elif kind == "flag":
        rect(0, 0.84, 1, 1, pale)
        line(0.24, 0.10, 0.24, 0.86, 2.4, dark)
        poly([(0.26, 0.14), (0.82, 0.10), (0.76, 0.30), (0.84, 0.48), (0.26, 0.46)], strong)
        poly([(0.26, 0.24), (0.78, 0.21), (0.77, 0.32), (0.26, 0.34)], PAPER)

    elif kind == "chart":
        rect(0, 0.84, 1, 1, pale)
        line(0.12, 0.10, 0.12, 0.84, 1.4, dark)
        line(0.12, 0.84, 0.92, 0.84, 1.4, dark)
        for i, hh in enumerate((0.28, 0.44, 0.36, 0.60, 0.52)):
            rect(0.18 + i * 0.15, 0.84 - hh, 0.27 + i * 0.15, 0.84,
                 [strong, mid, ACCENT, mid, strong][i])
        line(0.20, 0.50, 0.36, 0.36, 1.8, dark)
        line(0.36, 0.36, 0.52, 0.42, 1.8, dark)
        line(0.52, 0.42, 0.68, 0.24, 1.8, dark)
        line(0.68, 0.24, 0.84, 0.16, 1.8, dark)

    elif kind == "trophy":
        rect(0, 0.84, 1, 1, pale)
        poly([(0.34, 0.16), (0.66, 0.16), (0.62, 0.56), (0.38, 0.56)], mix(ACCENT, PAPER, 0.05))
        for s in (-1, 1):
            d.arc((px(0.5 + s * 0.30) - 0.10 * w * SS, py(0.26), px(0.5 + s * 0.30) + 0.10 * w * SS,
                   py(0.52)), 0, 360, fill=mix(ACCENT, PAPER, 0.3), width=int(2 * SS))
        rect(0.46, 0.56, 0.54, 0.72, mid)
        rect(0.34, 0.72, 0.66, 0.82, dark)

    elif kind == "plane":
        rect(0, 0.86, 1, 1, pale)
        ell(0.5, 0.48, 0.42, 0.10, dark)
        poly([(0.46, 0.46), (0.66, 0.46), (0.40, 0.16), (0.34, 0.16)], mid)
        poly([(0.46, 0.54), (0.64, 0.54), (0.42, 0.80), (0.36, 0.80)], mid)
        poly([(0.14, 0.44), (0.20, 0.36), (0.24, 0.48)], strong)
        ell(0.24, 0.48, 0.04, 0.10, strong)
        for i, u in enumerate((0.36, 0.46, 0.56)):
            ell(u, 0.48, 0.02, 0.08, PAPER)

    elif kind == "rocket":
        rect(0, 0.86, 1, 1, mix((30, 40, 70), PAPER, 0.86))
        poly([(0.42, 0.10), (0.50, 0.04), (0.58, 0.10), (0.58, 0.62), (0.42, 0.62)], PAPER)
        poly([(0.42, 0.10), (0.50, 0.04), (0.52, 0.10), (0.44, 0.14)], mix(GREY, PAPER, 0.4))
        rect(0.42, 0.30, 0.58, 0.38, strong)
        poly([(0.42, 0.50), (0.30, 0.72), (0.42, 0.66)], strong)
        poly([(0.58, 0.50), (0.70, 0.72), (0.58, 0.66)], strong)
        poly([(0.44, 0.62), (0.56, 0.62), (0.5, 0.92)], mix(ACCENT, PAPER, 0.1))
        poly([(0.47, 0.62), (0.53, 0.62), (0.5, 0.82)], mix((255, 220, 130), PAPER, 0.05))
        for u, v in ((0.18, 0.20), (0.82, 0.30), (0.14, 0.60), (0.86, 0.66)):
            ell(u, v, 0.015, 0.035, PAPER)

    elif kind == "chip":
        rect(0, 0.86, 1, 1, pale)
        rect(0.26, 0.16, 0.74, 0.76, mid)
        rect(0.34, 0.28, 0.66, 0.64, mix(col, PAPER, 0.15))
        for i in range(3):
            rect(0.38 + i * 0.09, 0.38, 0.42 + i * 0.09, 0.54, PAPER)
        for i in range(4):
            line(0.20, 0.26 + i * 0.14, 0.26, 0.26 + i * 0.14, 2.0, dark)
            line(0.74, 0.26 + i * 0.14, 0.80, 0.26 + i * 0.14, 2.0, dark)
        for i in range(2):
            line(0.36 + i * 0.18, 0.10, 0.36 + i * 0.18, 0.16, 2.0, dark)

    elif kind == "mine":
        rect(0, 0.70, 1, 1, pale)
        poly([(0.02, 0.90), (0.98, 0.90), (0.86, 0.62), (0.14, 0.62)], mix(GREY, PAPER, 0.55))
        line(0.06, 0.78, 0.94, 0.78, 2.0, dark)
        line(0.06, 0.86, 0.94, 0.86, 2.0, dark)
        rect(0.34, 0.46, 0.62, 0.74, strong)
        ell(0.42, 0.74, 0.06, 0.12, dark)
        ell(0.56, 0.74, 0.06, 0.12, dark)
        line(0.62, 0.46, 0.74, 0.20, 1.6, dark)
        ell(0.76, 0.18, 0.06, 0.12, ACCENT)

    elif kind == "cross":
        rect(0, 0.86, 1, 1, pale)
        rect(0.42, 0.16, 0.58, 0.84, mix((190, 60, 60), PAPER, 0.15))
        rect(0.28, 0.32, 0.72, 0.48, mix((190, 60, 60), PAPER, 0.15))
        for i, u in enumerate((0.14, 0.84)):
            line(u, 0.20, u, 0.84, 1.2, mid)

    elif kind == "planet":
        rect(0, 0, 1, 1, mix((18, 24, 44), PAPER, 0.86))
        ell(0.5, 0.46, 0.26, 0.52, mix((60, 100, 150), PAPER, 0.15))
        d.arc((px(0.5) - 0.44 * w * SS, py(0.46) - 0.20 * h * SS,
               px(0.5) + 0.44 * w * SS, py(0.46) + 0.20 * h * SS),
              200, 340, fill=ACCENT, width=int(2 * SS))
        for u, v in ((0.16, 0.18), (0.84, 0.24), (0.20, 0.74), (0.78, 0.80)):
            ell(u, v, 0.014, 0.032, PAPER)
        rect(0, 0.86, 1, 1, mix((18, 24, 44), PAPER, 0.92))

    else:  # a plain marker, never used by any story
        rect(0.3, 0.3, 0.7, 0.8, strong)


# -------------------------------------------------------------------- page
def render(path="entry.png", audit=False):
    img = Image.new("RGB", (W * SS, H * SS), PAPER)
    d = ImageDraw.Draw(img)
    tally = counts()
    n_all = sum(tally.values())
    boxes = []

    def note(name, y0, y1):
        boxes.append((name, round(y0, 1), round(y1, 1)))

    d.text((16 * SS, 12 * SS), "THE WORLD TODAY", font=font(SERIF_B, 42), fill=INK)
    draw_text(d, (1008, 16), DAY, font(SANS_B, 26), INK, anchor="ra")
    draw_text(d, (1008, 46), "DAY 329 OF 2026 · " + EDITION, font(SANS_B, 9), GREY, anchor="ra")
    d.rectangle((16 * SS, 64 * SS, 1008 * SS, 68 * SS), fill=REGION_COLOURS["MIDDLE EAST"])

    strap = ("EVERY ONE OF THE %d STORIES IS DATED %s · %d REGIONS · NOTHING FIRST REPORTED "
             "BEFORE TODAY" % (n_all, DAY, len(tally)))
    draw_text(d, (16, 74), strap, font(SANS_B, 12), INK)
    note("strap", 74, 88)

    cx = 16.0
    fc = font(SANS_B, 10)
    for reg in sorted(tally, key=lambda r: -tally[r]):
        label = "%s %d" % (reg, tally[reg])
        wch = tw(d, label, fc) + 11
        d.rectangle((cx * SS, 92 * SS, (cx + wch) * SS, 108 * SS), fill=REGION_COLOURS[reg])
        draw_text(d, (cx + 5, 94.5), label, fc, (255, 255, 255))
        cx += wch + 5
    note("chips", 92, 108)

    draw_text(d, (16, 114), "THE DAY IN NUMBERS", font(SANS_B, 8.5), GREY)
    draw_text(d, (1008, 114), STAMP, font(SANS_R, 8.5), GREY, anchor="ra")
    cell = 992.0 / len(NUMBERS)
    for i, (fig, lab) in enumerate(NUMBERS):
        x = 16 + i * cell
        draw_text(d, (x, 126), fig, font(SERIF_B, 20), REGION_COLOURS["MIDDLE EAST"])
        draw_text(d, (x, 150), lab, font(SANS_R, 10), GREY)
        if i:
            d.rectangle(((x - 9) * SS, 128 * SS, (x - 8) * SS, 162 * SS), fill=HAIR)
    note("numbers", 114, 162)
    d.rectangle((16 * SS, 166 * SS, 1008 * SS, 168 * SS), fill=INK)

    # the grid: 6 x 8 cards, one story each, a drawn scene above every label
    cols, rows = 6, 8
    top, bottom = 172.0, 1002.0
    gap = 4.0
    cw = (992.0 - (cols - 1) * gap) / cols
    rh = (bottom - top - (rows - 1) * gap) / rows
    assert len(STORIES) == cols * rows, len(STORIES)
    assert rh >= 92, rh
    scene_h = 38.0
    for i, (place, region, desk, status, head, src, utc, scene) in enumerate(STORIES):
        r_, c_ = divmod(i, cols)
        x = 16 + c_ * (cw + gap)
        y = top + r_ * (rh + gap)
        col = REGION_COLOURS[region]
        draw_scene(d, scene, (x, y, x + cw, y + scene_h), col)
        d.rectangle((x * SS, (y + scene_h) * SS, (x + cw) * SS, (y + scene_h + 1.5) * SS), fill=col)
        draw_text(d, (x, y + scene_h + 4), "%s · %s/%s" % (place, desk, status), font(SANS_B, 7.5), col)
        fh, hlines, s = fit_block(d, head, SANS_B, 11.5, cw, 3)
        ly = y + scene_h + 14
        for ln in hlines:
            draw_text(d, (x, ly), ln, fh, INK)
            ly += s * 1.14
        draw_text(d, (x, y + rh - 10), "%s GMT · %s" % (utc, src), font(SANS_R, 7), GREY)
        note("card%d" % i, y, y + rh)

    if audit:
        bad = [(n, y1) for n, y0, y1 in boxes if y1 > H - 4]
        return boxes, bad

    img = img.resize((W, H), Image.LANCZOS)
    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    if "--audit" in sys.argv:
        boxes, bad = render(audit=True)
        print("blocks", len(boxes), "overflow", bad)
    else:
        print(render(out))
