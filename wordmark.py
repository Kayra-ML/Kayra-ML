"""The KAYRA wordmark, drawn rather than typed.

No webfont survives GitHub's SVG sanitiser and no installed face is the right
answer, so the letters are authored as stroked paths on the same grid the packet
diagram uses: one stroke weight, flat terminals, mitred joins, bowls struck as
true semicircles. Each glyph occupies a 100 x 140 box; stems sit on x=10/x=90 and
the cap and baseline on y=10/y=130, so a letter's extents are exactly 0..100 and
0..140 once the 20-unit stroke is counted.
"""

STROKE = 20
GLYPH_W = 100
GLYPH_H = 140
TRACK = 22          # optical sidebearing between glyphs

GLYPHS = {
    # Bowls first, stem last: the stem then covers the seams where the bowl
    # terminals butt into it, which otherwise antialias as a hairline notch.
    "B": ["M10,10 H50 A30,30 0 0 1 50,70 H10",
          "M10,70 H56 A30,30 0 0 1 56,130 H10",
          "M10,10 V130"],
    "E": ["M90,10 H10 V130 H90",
          "M10,70 H74"],
    "R": ["M10,130 V10 H50 A30,30 0 0 1 50,70 H10",
          "M50,70 L90,130"],
    "K": ["M10,10 V130",
          "M88,10 L10,73",
          "M44,52 L90,130"],
    # A flat apex, not a point: a mitred point on this angle spikes well past
    # the cap line and reads as a different height from every other letter.
    "A": ["M8,130 L46,10 H54 L92,130",
          "M27,94 H73"],
    "Y": ["M10,10 L50,66 L90,10",
          "M50,66 V130"],
}

# Per-glyph vertical nudges. Empty today; kept because the flat-apex A removed
# the only case that needed one, and a future glyph may not be so lucky.
OVERSHOOT = {}


def wordmark(text, x, y, scale, colour, opacity=1.0, extra=""):
    """Stroked paths for `text`, top-left anchored at (x, y)."""
    out = ['<g transform="translate(%.2f,%.2f) scale(%.4f)" fill="none" stroke="%s" '
           'stroke-width="%d" stroke-linecap="butt" stroke-linejoin="miter" '
           'stroke-miterlimit="6" opacity="%.3f"%s>'
           % (x, y, scale, colour, STROKE, opacity, extra)]
    pen = 0
    for ch in text:
        paths = GLYPHS[ch]
        dy = OVERSHOOT.get(ch, 0)
        out.append('<g transform="translate(%d,%d)">' % (pen, dy))
        out += ['<path d="%s"/>' % d for d in paths]
        out.append("</g>")
        pen += GLYPH_W + TRACK
    out.append("</g>")
    return "".join(out), (pen - TRACK) * scale, GLYPH_H * scale
