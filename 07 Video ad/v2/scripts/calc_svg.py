"""Static SVGs of the ad's onboarding calculator, for the pitch deck.

Redraws the two end states of src/Calc.tsx at 1x (u = 1):
  calculator_card.svg  the filled-in form (Trip to Japan, ₱150,000, 5 years → ₱2,500 / month)
  calculator_list.svg  the "keep going" list of firsts
Same layout numbers, colours and example as the ad. All text is converted to outlines
(Geist, with Inter for the ₱ sign, both bundled in public/fonts), so the files look the same
in PowerPoint and Keynote without the fonts installed. Shadows are left out (PowerPoint drops
SVG filters); the cards get a hairline border instead.

Run from 07 Video ad/v2:  python3 scripts/calc_svg.py   (needs fonttools, brotli, uharfbuzz)
"""
import io
import json
import math
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / 'public' / 'fonts'
OUT = ROOT.parent.parent / 'Presentation deck' / 'calculator'
EX = json.loads((ROOT / 'src' / 'timeline.json').read_text())['example']

# colours from src/lib.tsx
C = dict(paper='#F4F3EE', card='#FFFFFF', ink='#0E100E', ink2='#3A3F3B', muted='#8B908A', line='#D9D7CF',
         accent='#0B7A4B', accentSoft='#DDEFE5')
BORDER = '#E4E2DA'


def peso(n):
    return '₱' + f'{round(n):,}'


# ---------- fonts and text ----------
_fonts = {}


def _font(family, weight):
    key = (family, weight)
    if key not in _fonts:
        name = f'geist-sans-latin-{weight}-normal.woff2' if family == 'geist' else f'inter-latin-ext-{weight}-normal.woff2'
        tt = TTFont(FONTS / name)
        tt.flavor = None
        buf = io.BytesIO()
        tt.save(buf)
        hh = tt['hhea']
        _fonts[key] = dict(hb=hb.Font(hb.Face(buf.getvalue())), gs=tt.getGlyphSet(), order=tt.getGlyphOrder(),
                           upm=tt['head'].unitsPerEm, asc=hh.ascent, desc=-hh.descent, gap=hh.lineGap)
    return _fonts[key]


def line_h(size, weight=500):
    g = _font('geist', weight)
    return (g['asc'] + g['desc'] + g['gap']) / g['upm'] * size


def baseline(top, size, weight=500, lh=None):
    """CSS baseline of a single line whose line box starts at `top`."""
    g = _font('geist', weight)
    lh = line_h(size, weight) if lh is None else lh
    a, d = g['asc'] / g['upm'] * size, g['desc'] / g['upm'] * size
    return top + (lh - a - d) / 2 + a


def _shape(text, size, weight, track):
    """Glyphs as (font, glyph name, x) plus the advance, CSS-style (tracking after every glyph)."""
    runs, cur = [], ''
    for ch in text:  # Geist has no ₱: that one character comes from Inter, as in the ad
        if ch == '₱':
            if cur:
                runs.append(('geist', cur))
            runs.append(('inter', ch))
            cur = ''
        else:
            cur += ch
    if cur:
        runs.append(('geist', cur))
    out, x = [], 0.0
    feats = {'tnum': True, 'kern': True}
    if track:
        feats.update(liga=False, clig=False)  # browsers drop ligatures when letter-spacing is set
    for fam, s in runs:
        f = _font(fam, weight)
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(f['hb'], buf, feats)
        k = size / f['upm']
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((f, f['order'][info.codepoint], x + pos.x_offset * k))
            x += pos.x_advance * k + track * size
    return out, x


def text_w(text, size, weight=500, track=0.0):
    return _shape(text, size, weight, track)[1]


def text(x, y, s, size, weight=500, fill=C['ink'], track=0.0, anchor='start'):
    """Text as one outlined <path>; (x, y) is the baseline origin."""
    glyphs, w = _shape(s, size, weight, track)
    if anchor == 'middle':
        x -= w / 2
    elif anchor == 'end':
        x -= w
    pen = SVGPathPen(None, ntos=lambda v: f'{v:.2f}'.rstrip('0').rstrip('.'))
    for f, name, gx in glyphs:
        k = size / f['upm']
        f['gs'][name].draw(TransformPen(pen, (k, 0, 0, -k, x + gx, y)))
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>' if pen.getCommands() else ''


# ---------- shapes ----------
def rect(x, y, w, h, r, fill, stroke=None):
    s = f' stroke="{stroke}" stroke-width="1"' if stroke else ''
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{r:.2f}" fill="{fill}"{s}/>'


def ring(cx, cy, size, stroke, progress, color=C['accent'], track=C['line']):
    """MiniRing: track circle plus a clockwise arc from 12 o'clock (no dash arrays, for PowerPoint)."""
    r = (size - stroke) / 2
    a = 2 * math.pi * progress
    ex, ey = cx + r * math.sin(a), cy - r * math.cos(a)
    large = 1 if progress > 0.5 else 0
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" stroke="{track}" stroke-width="{stroke}"/>'
            f'<path d="M{cx:.2f} {cy - r:.2f} A{r:.2f} {r:.2f} 0 {large} 1 {ex:.2f} {ey:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round"/>')


def check(x, y, size, color):
    k = size / 24
    p = lambda a, b: f'{x + a * k:.2f} {y + b * k:.2f}'
    return (f'<path d="M{p(5, 12.5)} L{p(10, 17)} L{p(19, 7)}" fill="none" stroke="{color}" stroke-width="{3 * k:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _clip(poly, x0, y0, x1, y1):
    """Sutherland–Hodgman clip of a polygon to an axis-aligned box."""
    def cut(pts, inside, inter):
        res = []
        for i, p in enumerate(pts):
            q = pts[i - 1]
            if inside(p):
                if not inside(q):
                    res.append(inter(q, p))
                res.append(p)
            elif inside(q):
                res.append(inter(q, p))
        return res

    def ix(v):
        return lambda q, p: (v, q[1] + (p[1] - q[1]) * (v - q[0]) / (p[0] - q[0]))

    def iy(v):
        return lambda q, p: (q[0] + (p[0] - q[0]) * (v - q[1]) / (p[1] - q[1]), v)

    for inside, inter in [(lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)),
                          (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))]:
        poly = cut(poly, inside, inter) if poly else poly
    return poly


def hatch(x, y, w, h, period=8, band=4):
    """repeating-linear-gradient(45deg, line 0 4px, paper 4px 8px) as plain polygons."""
    out = [rect(x, y, w, h, 3, C['paper'])]
    # 45deg gradient runs toward the top right, so the bands run along (1, 1); u = (x - y)/√2 across them
    s2 = math.sqrt(2)
    lo, hi = (x - (y + h)) / s2, (x + w - y) / s2
    u = math.floor(lo / period) * period
    b0, b1 = (x + y) / s2 - 1, (x + w + y + h) / s2 + 1
    while u < hi:
        pts = []
        for a, b in [(u, b0), (u + band, b0), (u + band, b1), (u, b1)]:
            # point with across-coordinate a and along-coordinate b: across=(x-y)/√2, along=(x+y)/√2
            pts.append(((a + b) / s2, (b - a) / s2))
        poly = _clip(pts, x, y, x + w, y + h)
        if len(poly) >= 3:
            out.append('<path fill="%s" d="M%s Z"/>' % (C['line'], ' L'.join(f'{px:.2f} {py:.2f}' for px, py in poly)))
        u += period
    return ''.join(out)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{title}</title>{body}</svg>\n')


# ---------- the filled-in form (Calc.tsx Form, end of the START step) ----------
def card():
    W, H, pad = 860, 840, 52
    inner = W - 2 * pad
    X, R = pad, pad + inner
    years, months = EX['years'], EX['years'] * 12
    b = [rect(0.5, 0.5, W - 1, H - 1, 32, C['card'], BORDER)]

    # header
    rh = max(30, line_h(30, 600))
    b.append(ring(X + 15, 44 + rh / 2, 30, 5, 0.75))
    b.append(text(X + 30 + 14, baseline(44 + (rh - line_h(30, 600)) / 2, 30, 600), 'New first', 30, 600, C['ink'], -0.03))
    b.append(text(R, baseline(44 + (rh - line_h(18)) / 2, 18), 'FIRSTS FUND', 18, 500, C['muted'], 0.12, 'end'))

    def field(top, label, value):
        b.append(text(X, baseline(top, 20), label, 20, 500, C['muted'], 0.12))
        vt = top + line_h(20) + 8
        b.append(text(X, baseline(vt, 42), value, 42, 500, C['ink'], -0.03))
        b.append(rect(X, vt + 52 + 12, inner, 2, 0, C['ink']))

    field(130, 'NAME YOUR FIRST', EX['name'])
    field(262, 'TARGET AMOUNT', peso(EX['amount']))

    # when + slider
    top = 394
    bl = baseline(top, 20)
    b.append(text(X, bl, 'WHEN', 20, 500, C['muted'], 0.12))
    b.append(text(R, bl, 'MINIMUM 5 YEARS', 18, 500, C['muted'], 0.08, 'end'))
    vt = top + line_h(20) + 8
    vb = baseline(vt, 42)
    lead = f'{years} years'
    b.append(text(X, vb, lead, 42, 500, C['ink'], -0.03))
    b.append(text(X + text_w(lead, 42, 500, -0.03), vb, f' · {months} months', 26, 500, C['muted'], -0.03))
    st = vt + 52 + 14
    lock = 5 / 30 * inner
    knob = years / 30 * inner
    b.append(rect(X, st + 17, inner, 6, 3, C['line']))
    b.append(hatch(X, st + 14, lock, 12))
    b.append(f'<circle cx="{X + knob - 16 + 19:.2f}" cy="{st + 4 + 19:.2f}" r="17.5" fill="{C["card"]}" '
             f'stroke="{C["accent"]}" stroke-width="3"/>')

    # result
    b.append(rect(X, 556, inner, 158, 22, C['accentSoft']))
    cx, ct = X + 28, 556 + 22
    b.append(text(cx, baseline(ct, 20), 'MONTHLY CONTRIBUTION', 20, 500, C['accent'], 0.12))
    bt = ct + line_h(20)
    big = peso(EX['amount'] / months)
    bb = baseline(bt, 64, 600, lh=64 * 1.1)
    b.append(text(cx, bb, big, 64, 600, C['accent'], -0.05))
    b.append(text(cx + text_w(big, 64, 600, -0.05), bb, ' / month', 28, 500, C['ink2'], -0.02))
    nt = bt + 64 * 1.1 + 2
    b.append(text(cx, baseline(nt, 16), f'{peso(EX["amount"])} ÷ {months} MONTHS · CONTRIBUTIONS ONLY', 16, 500,
                  C['ink2'], 0.06))

    # button
    b.append(rect(X, 738, inner, 74, 37, C['ink']))
    b.append(text(X + inner / 2, baseline(738 + (74 - line_h(28)) / 2, 28), 'Start with ₱100', 28, 500, C['card'], 0, 'middle'))
    return svg(W, H, ''.join(b), 'Firsts Fund onboarding calculator')


# ---------- the list of firsts (Calc.tsx Row, KEEP GOING step) ----------
def row(y, W, name, years, monthly, started):
    RH = 132
    b = [rect(0.5, y + 0.5, W - 1, RH - 1, 32, C['card'], BORDER)]
    b.append(ring(40 + 27, y + RH / 2, 54, 6, 0.15 if started else 0.03))
    tx = 40 + 54 + 22
    th = line_h(32, 600) + 4 + line_h(18)
    tt = y + (RH - th) / 2
    b.append(text(tx, baseline(tt, 32, 600), name, 32, 600, C['ink'], -0.03))
    b.append(text(tx, baseline(tt + line_h(32, 600) + 4, 18), f'{years} YEARS · {peso(monthly)}/MONTH', 18, 500, C['muted'], 0.08))
    if started:
        ph = 8 + max(20, line_h(20, 600)) + 8
        pw = 16 + 20 + 6 + text_w('Started', 20, 600) + 16
        px, py = W - 40 - pw, y + (RH - ph) / 2
        b.append(rect(px, py, pw, ph, ph / 2, C['accentSoft']))
        b.append(check(px + 16, py + (ph - 20) / 2, 20, C['accent']))
        b.append(text(px + 16 + 20 + 6, baseline(py + (ph - line_h(20, 600)) / 2, 20, 600), 'Started', 20, 600, C['accent']))
    return ''.join(b)


def firsts_list():
    W, RH, GAP = 860, 132, 18
    rows = [(EX['name'], EX['years'], EX['amount'] / (EX['years'] * 12), True),
            ('First car', 6, 300000 / 72, False),
            ('First home down payment', 8, 500000 / 96, False),
            ('Retirement trip', 30, 400000 / 360, False)]
    body = ''.join(row(k * (RH + GAP), W, *r) for k, r in enumerate(rows))
    return svg(W, len(rows) * RH + (len(rows) - 1) * GAP, body, 'Firsts Fund list of firsts')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for name, s in [('calculator_card.svg', card()), ('calculator_list.svg', firsts_list())]:
        (OUT / name).write_text(s, encoding='utf-8')
        print(OUT / name, f'{len(s) / 1024:.0f} KB')
