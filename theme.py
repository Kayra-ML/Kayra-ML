"""Palette, type stack and shared SVG chrome for every profile asset.

Two themes, generated from one definition, because a GitHub reader may be on
either. The names are paper/ink rather than light/dark: the light theme is warm
stock, not white, and the dark theme keeps that warmth in its foreground so the
pair reads as one object photographed under two lights.
"""

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "light": dict(
        bg="#f4f7f1",
        inset="#eaf0e9",
        ink="#101510",
        ink2="#455348",
        ink3="#68756b",
        rule="#c7d4c9",
        rule2="#dce6dd",
        accent="#008f36",
        accent2="#00a64a",
        heat=["#dfe9df", "#b7ddb9", "#77c881", "#2faa4c", "#008f36"],
        void="#e9efea",
        wordmark="#101510",
        ramp=["#008f36", "#16a447", "#38b75b", "#65bd79", "#8aad93", "#9aa79c"],
        tail="#b7c2b8",
    ),
    "dark": dict(
        bg="#0b1014",
        inset="#10161b",
        ink="#f0f0e8",
        ink2="#aab2aa",
        ink3="#7f8d84",
        rule="#1c2b23",
        rule2="#15231a",
        accent="#00ff4c",
        accent2="#63ffa2",
        heat=["#141b1c", "#163823", "#1f6f35", "#29b84c", "#00ff4c"],
        void="#0f1418",
        wordmark="#f0f0e8",
        ramp=["#00ff4c", "#36e65d", "#52c86c", "#66ab76", "#728d78", "#65736b"],
        tail="#38483f",
    ),
}


def rel_lum(hexstr):
    c = [int(hexstr[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def on(bg_hex, theme):
    """Foreground for text sitting on `bg_hex`: whichever of the theme's ink and
    its page colour reads better against it. Cell fills in the calendar run the
    whole ramp, so the digits cannot pick one colour and hope."""
    return theme["ink"] if contrast(theme["ink"], bg_hex) >= contrast(theme["bg"], bg_hex) else theme["bg"]
