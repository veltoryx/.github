"""Generate Veltoryx Technologies flat vector logo files (no font dependency)."""
import os, sys
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)

C = dict(blue="#0069FB", sky="#00A3FD", graphite="#111418", white="#FFFFFF",
         steel_hi="#9A9EA3", steel_lo="#6E7378", silver_hi="#D3D6DA", silver_lo="#A2A5A8")
THEMES = {
  "light": dict(l_hi=C["steel_hi"], l_lo=C["steel_lo"], r_hi=C["sky"], r_lo=C["blue"], text=C["graphite"], x=C["blue"], sub=C["steel_lo"]),
  "dark":  dict(l_hi=C["silver_hi"], l_lo=C["silver_lo"], r_hi=C["sky"], r_lo=C["blue"], text=C["white"], x=C["sky"], sub=C["silver_lo"]),
  "mono-black": dict(l_hi="#000", l_lo="#000", r_hi="#000", r_lo="#000", text="#000", x="#000", sub="#000"),
  "mono-white": dict(l_hi="#fff", l_lo="#fff", r_hi="#fff", r_lo="#fff", text="#fff", x="#fff", sub="#fff"),
}

def mark(t):  # in a 0..100 box; actual ink spans x 4..94, y 11..90
    return (f'<polygon fill="{t["l_hi"]}" points="7,16 32,16 49,46 49,49"/>'
            f'<polygon fill="{t["l_lo"]}" points="4,20 49,54 49,90"/>'
            f'<polygon fill="{t["r_hi"]}" points="51,49 51,46 63,28 94,11 89,19"/>'
            f'<polygon fill="{t["r_lo"]}" points="87,23 51,54 51,90"/>')
MARK_BOX = (4, 11, 90, 79)  # x, y, w, h of the ink

# Heavy wordmark glyphs, cap height 40, stroke 7. (shapes, advance width)
def rect(x, y, w, h): return f'M{x},{y}h{w}v{h}h{-w}z'
def poly(*p): return 'M' + 'L'.join(f'{a},{b}' for a, b in p) + 'z'
RR_O = 'M8,0H40Q48,0 48,8V32Q48,40 40,40H8Q0,40 0,32V8Q0,0 8,0z M9,7H39Q41,7 41,9V31Q41,33 39,33H9Q7,33 7,31V9Q7,7 9,7z'
RR_R = 'M0,0H40Q48,0 48,8V17Q48,25 40,25H7V40H0z M7,7H39Q41,7 41,9V16Q41,18 39,18H7z'
HEAVY = {
  'V': ([poly((0,0),(9,0),(24,29),(39,0),(48,0),(28.5,40),(19.5,40))], 48),
  'E': ([rect(0,0,7,40), rect(0,0,46,7), rect(0,16.5,38,7), rect(0,33,46,7)], 46),
  'L': ([rect(0,0,7,40), rect(0,33,42,7)], 42),
  'T': ([rect(0,0,46,7), rect(19.5,0,7,40)], 46),
  'O': ([RR_O], 48),
  'R': ([RR_R, poly((25,25),(34,25),(48,40),(39,40))], 48),
  'Y': ([poly((0,0),(9,0),(24,16),(39,0),(48,0),(27.5,23),(20.5,23)), rect(20.5,21,7,19)], 48),
  'X': ([poly((0,0),(9,0),(48,40),(39,40)), poly((39,0),(48,0),(9,40),(0,40))], 48),
}
# Light glyphs for "TECHNOLOGIES": stroked centre lines in a 10x10 box.
LIGHT = {
  'T': ('M0,0H10M5,0V10', 10), 'E': ('M10,0H0V10H10M0,5H8', 10),
  'C': ('M10,0H2Q0,0 0,2V8Q0,10 2,10H10', 10), 'H': ('M0,0V10M10,0V10M0,5H10', 10),
  'N': ('M0,10V0L10,10V0', 10), 'O': ('M2,0H8Q10,0 10,2V8Q10,10 8,10H2Q0,10 0,8V2Q0,0 2,0z', 10),
  'L': ('M0,0V10H10', 10), 'G': ('M10,0H2Q0,0 0,2V8Q0,10 2,10H8Q10,10 10,8V5H5', 10),
  'I': ('M0,0V10', 0), 'S': ('M10,0H2Q0,0 0,2V3Q0,5 2,5H8Q10,5 10,7V8Q10,10 8,10H0', 10),
}
GAP_H, GAP_L, SW_L = 7, 7, 1.6

def heavy_word(word, t):
    parts, x = [], 0
    for i, ch in enumerate(word):
        shapes, w = HEAVY[ch]
        fill = t["x"] if ch == 'X' and i == len(word) - 1 else t["text"]
        parts.append(f'<path fill="{fill}" fill-rule="evenodd" transform="translate({x},0)" d="{" ".join(shapes)}"/>')
        x += w + GAP_H
    return ''.join(parts), x - GAP_H

def light_word(word, t, target_w):
    widths = [LIGHT[c][1] for c in word]
    raw = sum(widths); gap = (target_w - raw) / (len(word) - 1)  # justify to wordmark width
    parts, x = [], 0
    for c in word:
        d, w = LIGHT[c]
        parts.append(f'<path transform="translate({x:.2f},0)" d="{d}"/>')
        x += w + gap
    return (f'<g fill="none" stroke="{t["sub"]}" stroke-width="{SW_L}" stroke-linejoin="miter">'
            + ''.join(parts) + '</g>')

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')

def write(name, content):
    path = os.path.normpath(os.path.join(OUT, name))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(content)

for th, t in THEMES.items():
    mx, my, mw, mh = MARK_BOX
    # 1. Mark only, tightly cropped with a small margin
    pad = 2
    write(f'veltoryx-mark-{th}.svg', svg(mw + 2*pad, mh + 2*pad,
          f'<g transform="translate({pad-mx},{pad-my})">{mark(t)}</g>', 'Veltoryx'))
    # 2. Wordmark only: VELTORYX
    word, ww = heavy_word('VELTORYX', t)
    write(f'veltoryx-wordmark-{th}.svg', svg(ww, 40, word, 'Veltoryx'))
    # 3. Wordmark with TECHNOLOGIES under it
    tech = light_word('TECHNOLOGIES', t, ww)
    write(f'veltoryx-wordmark-full-{th}.svg', svg(ww, 40 + 12 + 10 + SW_L,
          word + f'<g transform="translate(0,{52 + SW_L/2})">{tech}</g>', 'Veltoryx Technologies'))
    # 4. Horizontal logo: mark left, full wordmark right (text block height 62 ≈ mark height)
    text_h = 40 + 12 + 10 + SW_L
    s = (text_h + 10) / mh            # mark scaled a bit taller than text block
    m_w, m_h = mw * s, mh * s
    gap = 22
    H = m_h; ty = (H - text_h) / 2
    body = (f'<g transform="scale({s:.4f}) translate({-mx},{-my})">{mark(t)}</g>'
            f'<g transform="translate({m_w + gap:.2f},{ty:.2f})">{word}<g transform="translate(0,{52 + SW_L/2})">{tech}</g></g>')
    write(f'veltoryx-logo-horizontal-{th}.svg', svg(round(m_w + gap + ww, 2), round(H, 2), body, 'Veltoryx Technologies'))
    # 5. Stacked logo: mark on top, full wordmark below, centred
    s2 = 2.2; m2w, m2h = mw * s2, mh * s2
    W = max(ww, m2w); gap2 = 26
    body = (f'<g transform="translate({(W - m2w)/2:.2f},0) scale({s2}) translate({-mx},{-my})">{mark(t)}</g>'
            f'<g transform="translate({(W - ww)/2:.2f},{m2h + gap2:.2f})">{word}<g transform="translate(0,{52 + SW_L/2})">{tech}</g></g>')
    write(f'veltoryx-logo-stacked-{th}.svg', svg(round(W, 2), round(m2h + gap2 + text_h, 2), body, 'Veltoryx Technologies'))

# Favicon: mark centred in a square, transparent background
mx, my, mw, mh = MARK_BOX
side = max(mw, mh) + 6
write('../favicon/favicon.svg', svg(side, side, f'<g transform="translate({(side-mw)/2 - mx},{(side-mh)/2 - my})">{mark(THEMES["light"])}</g>', 'Veltoryx'))
print("ok", sorted(os.listdir(OUT)))
