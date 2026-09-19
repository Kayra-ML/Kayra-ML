#!/usr/bin/env python3
"""The five profile assets, drawn twice — once on paper, once in ink.

Every figure here is a real reading of the GitHub API rather than an ornament:
the language map's offsets are the actual byte counts the API reports, the
calendar's hex digits are that day's commit count, and the segment map's bars
start and end on the days a repository was created and last pushed.

Design rule inherited from the first version of this profile and worth keeping:
the *static* frame must already be correct. Animation is decoration only. A bar
whose width animates from zero renders as an empty bar wherever animation does
not run, which is worse than no animation.
"""

from datetime import date, datetime, timedelta

from theme import MONO, THEMES, esc, on
from wordmark import wordmark

W = 1200
M = 56                      # page margin
CONTENT = W - 2 * M         # 1088


# --------------------------------------------------------------------------- chrome

def head(w, h, label):
    return ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
            'height="%d" role="img" aria-label="%s">' % (w, h, w, h, esc(label))]


def plate(t, w, h):
    """The page itself: stock, and a hairline frame inset from the trim."""
    return ['<rect width="%d" height="%d" fill="%s"/>' % (w, h, t["bg"]),
            '<rect x="20.5" y="20.5" width="%.1f" height="%.1f" fill="none" stroke="%s"/>'
            % (w - 41, h - 41, t["rule2"])]


def caption(t, y, left, right=None, w=W):
    """The small mono line that names a figure. Left is the figure's own name,
    set in the accent; right is the one fact about it worth reading first."""
    out = ['<text x="%d" y="%d" font-family="%s" font-size="11" fill="%s" '
           'letter-spacing="1.4">%s</text>' % (M, y, MONO, t["accent"], esc(left))]
    if right:
        out.append('<text x="%d" y="%d" font-family="%s" font-size="11" fill="%s" '
                   'letter-spacing="0.6" text-anchor="end">%s</text>'
                   % (w - M, y, MONO, t["ink3"], esc(right)))
    return out


def rule(t, y, x=M, w=CONTENT, colour=None):
    return ['<rect x="%.1f" y="%.1f" width="%.1f" height="1" fill="%s"/>'
            % (x, y, w, colour or t["rule"])]


def bit_ruler(t, y, x=M, w=CONTENT, bits=32):
    """A 0..31 bit scale. Ticks every bit, tall ticks and a number on every
    byte boundary — the one piece of chrome that appears on every figure and
    ties them into one document."""
    step = w / bits
    out = []
    for b in range(bits + 1):
        bx = x + b * step
        byte_edge = b % 8 == 0
        out.append('<rect x="%.2f" y="%.1f" width="1" height="%d" fill="%s"/>'
                   % (bx, y - (11 if byte_edge else 5), 11 if byte_edge else 5,
                      t["ink3"] if byte_edge else t["rule"]))
    for b in range(0, bits, 8):
        out.append('<text x="%.2f" y="%.1f" font-family="%s" font-size="10" fill="%s">%d</text>'
                   % (x + b * step + 4, y - 15, MONO, t["ink3"], b))
    out.append('<text x="%.2f" y="%.1f" font-family="%s" font-size="10" fill="%s" '
               'text-anchor="end">%d</text>' % (x + w - 2, y - 15, MONO, t["ink3"], bits - 1))
    out += rule(t, y, x, w)
    return out


def foot(t, h, note, w=W):
    return ['<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s" '
            'letter-spacing="0.5">%s</text>' % (M, h - 30, MONO, t["ink3"], esc(note))]


# --------------------------------------------------------------------------- 0. header

THESIS = ("I'd rather speak the protocol than drive a browser.\n"
          "No Selenium, no Puppeteer. Just sockets.\n")
DUMP_COLS = 8
DUMP_ROWS = 12          # 96 bytes: the sentence is 93, so three of padding


def build_header(theme_name, u, projects):
    t = THEMES[theme_name]
    H = 440
    since = datetime.strptime(u["createdAt"][:10], "%Y-%m-%d").strftime("%Y")

    p = head(W, H, "Kayra, @KAYRA-ML — 18, Hatay, Türkiye. "
             + THESIS.replace("\n", " ").strip())
    p += plate(t, W, H)
    p += bit_ruler(t, 74, M, 560)

    # --- left: the name, drawn on the same grid as the ruler above it
    mark, mw, mh = wordmark("KAYRA", M, 118, 0.95, t["wordmark"])
    p.append(mark)

    p.append('<text x="%d" y="%d" font-family="%s" font-size="12.5" fill="%s" '
             'letter-spacing="0.6">@KAYRA-ML · 18 · Hatay, Türkiye · since %s</text>'
             % (M, 262, MONO, t["ink3"], esc(since)))

    for i, line in enumerate(("I'd rather speak the protocol", "than drive a browser.")):
        p.append('<text x="%d" y="%d" font-family="%s" font-size="21" fill="%s" '
                 'letter-spacing="-0.3">%s</text>'
                 % (M, 312 + i * 30, MONO, t["ink"], esc(line)))

    p += rule(t, 372, M, 560, t["rule2"])
    p.append('<text x="%d" y="%d" font-family="%s" font-size="13.5" fill="%s">'
             '%d public projects · AI Provider · CLI · Automation</text>'
             % (M, 400, MONO, t["ink2"], projects))

    # --- right: the same sentence, as the bytes it actually is
    dx, dy, rh = 660, 104, 22
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (dx - 20, dy - 26, W - M - dx + 20, DUMP_ROWS * rh + 44, t["inset"]))
    p.append('<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s" '
             'letter-spacing="1.4">HEXDUMP · 0x%02X BYTES</text>'
             % (dx, dy - 8, MONO, t["ink3"], DUMP_COLS * DUMP_ROWS))

    raw = THESIS.encode("utf-8")
    raw = raw + b" " * (DUMP_COLS * DUMP_ROWS - len(raw))
    hexw, asciiw = 21.5, 7.35
    ascii_x = dx + 62 + DUMP_COLS * hexw + 18
    for r in range(DUMP_ROWS):
        y = dy + 14 + r * rh
        chunk = raw[r * DUMP_COLS:(r + 1) * DUMP_COLS]
        p.append('<text x="%d" y="%.1f" font-family="%s" font-size="12" fill="%s">%04x</text>'
                 % (dx, y, MONO, t["ink3"], r * DUMP_COLS))
        for c, b in enumerate(chunk):
            # A printable byte is ink; whitespace and the newlines are not, and
            # showing them at the same weight would flatten the thing that makes
            # a hexdump readable at a glance.
            printable = 0x21 <= b <= 0x7e
            p.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="12" fill="%s">%02x</text>'
                     % (dx + 62 + c * hexw, y, MONO, t["ink"] if printable else t["ink3"], b))
            ch = chr(b) if printable else "."
            p.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="12" fill="%s">%s</text>'
                     % (ascii_x + c * asciiw, y, MONO,
                        t["accent"] if printable else t["rule"], esc(ch)))

    # The only motion on the page: a read head crossing the dump, once every
    # nine seconds. Everything under it is already legible without it.
    band_w = W - M - dx + 20
    p.append('<rect x="%d" y="%.1f" width="%d" height="%d" fill="%s" opacity="0.16">'
             '<animate attributeName="y" values="%.1f;%.1f;%.1f" keyTimes="0;0.55;1" '
             'dur="9s" repeatCount="indefinite"/></rect>'
             % (dx - 20, dy - 4, band_w, rh, t["accent"],
                dy - 4, dy - 4 + (DUMP_ROWS - 1) * rh, dy - 4))

    p.append("</svg>")
    return "\n".join(p) + "\n"


# --------------------------------------------------------------------------- 1. fields

def build_fields(theme_name, cc, repo_count, peak, opened, private):
    t = THEMES[theme_name]
    H = 296
    cal = cc["contributionCalendar"]
    span = "last 12 months" if private else "public only — private work not counted"
    rows = [
        ("contributions", "0x0000", "u16", "%d" % cal["totalContributions"], span),
        ("commits", "0x0002", "u16", "%d" % cc["totalCommitContributions"], "authored, not merged"),
        ("repositories", "0x0004", "u8", "%d" % repo_count, "owner, no forks"),
        ("peak_day", "0x0005", "u8", "%d" % peak, "commits inside 24 hours"),
        ("opened", "0x0006", "date", opened, "the account's first day"),
    ]

    p = head(W, H, "Activity: %d contributions, %d commits, %d repositories"
             % (cal["totalContributions"], cc["totalCommitContributions"], repo_count))
    p += plate(t, W, H)
    p += caption(t, 52, "struct activity", "sizeof = 8 bytes")

    cols = [M, M + 250, M + 360, M + 470, M + 640]
    p.append('<g font-family="%s" font-size="10" fill="%s" letter-spacing="1.3">' % (MONO, t["ink3"]))
    for x, lab in zip(cols, ("FIELD", "OFFSET", "TYPE", "VALUE", "MEANING")):
        p.append('<text x="%d" y="82">%s</text>' % (x, lab))
    p.append("</g>")
    p += rule(t, 92)

    for i, (name, off, typ, val, note) in enumerate(rows):
        y = 122 + i * 33
        if i:
            p += rule(t, y - 23, M, CONTENT, t["rule2"])
        p.append('<text x="%d" y="%d" font-family="%s" font-size="13" fill="%s">%s</text>'
                 % (cols[0], y, MONO, t["ink2"], esc(name)))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="12" fill="%s">%s</text>'
                 % (cols[1], y, MONO, t["ink3"], off))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="12" fill="%s">%s</text>'
                 % (cols[2], y, MONO, t["accent2"], typ))
        # Tabular figures matter here: five values in a column that do not line
        # up on the digit read as five unrelated numbers.
        p.append('<text x="%d" y="%d" font-family="%s" font-size="19" font-weight="600" '
                 'fill="%s" style="font-variant-numeric:tabular-nums">%s</text>'
                 % (cols[3], y + 2, MONO, t["ink"], esc(val)))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="12" fill="%s">%s</text>'
                 % (cols[4], y, MONO, t["ink3"], esc(note)))

    p.append("</svg>")
    return "\n".join(p) + "\n"


# --------------------------------------------------------------------------- 2. calendar

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
CALENDAR_WEEKS = 26


def build_calendar(theme_name, u):
    """Recent contribution activity as a hexdump: one byte per day, the value
    is that day's commit count, and the cell colour is the same number again.

    Only the most recent 26 weeks are drawn. That halves the number of columns
    so each day can stay close to a true square instead of becoming a tall,
    narrow strip. If part of this window predates the account, that dead stretch
    is compressed and labelled rather than rendered as meaningless empty cells.
    """
    t = THEMES[theme_name]
    all_weeks = u["contributionsCollection"]["contributionCalendar"]["weeks"]
    source_weeks = all_weeks[-CALENDAR_WEEKS:]
    profile_calendar = u.get("_profileCalendar") or {}

    # Keep the exact same 26-week layout. Only correct which day cells are
    # marked and how strong they are.
    weeks = []
    for wk in source_weeks:
        days = []
        for raw in wk["contributionDays"]:
            d = dict(raw)
            visible = profile_calendar.get(d["date"])
            if visible is not None:
                d["contributionCount"] = int(visible.get("count", 0))
                d["_level"] = int(visible.get("level", 0))
            days.append(d)
        weeks.append({"contributionDays": days})

    opened = datetime.strptime(u["createdAt"][:10], "%Y-%m-%d").date()
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=1)

    def is_live(wk):
        return any(datetime.strptime(d["date"], "%Y-%m-%d").date() >= opened
                   for d in wk["contributionDays"])

    dead = [w for w in weeks if not is_live(w)]
    live = [w for w in weeks if is_live(w)] or weeks

    lab_w, gap = 44, 4
    ch = 40
    top = 104
    gx = M + lab_w + 8
    void_w = 372 if dead else 0
    brk = 30 if dead else 0
    lx = gx + void_w + brk
    cw = (M + CONTENT - lx) / len(live)
    grid_h = 7 * ch - gap
    H = int(top + grid_h + 88)

    total = sum(d["contributionCount"] for w in weeks for d in w["contributionDays"])
    p = head(W, H, "Recent %d-week contribution calendar: %d contributions, peak %d in one day. "
             "One square per day." % (len(weeks), total, peak))
    p += plate(t, W, H)
    p += caption(t, 52, "hexdump contributions.cal",
                 "%d weeks · one byte per day · peak 0x%02x" % (len(weeks), peak))

    # --- the elided stretch
    if dead:
        p.append('<rect x="%.1f" y="%d" width="%d" height="%d" fill="%s"/>'
                 % (gx, top, void_w, grid_h, t["inset"]))
        p.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="14" fill="%s" '
                 'text-anchor="middle">%d weeks elided</text>'
                 % (gx + void_w / 2, top + grid_h / 2 - 4, MONO, t["ink2"], len(dead)))
        p.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="11.5" fill="%s" '
                 'text-anchor="middle">the account did not exist yet</text>'
                 % (gx + void_w / 2, top + grid_h / 2 + 20, MONO, t["ink3"]))
        p.append('<text x="%.1f" y="%d" font-family="%s" font-size="10" fill="%s" '
                 'letter-spacing="1">%s</text>'
                 % (gx, top - 12, MONO, t["ink3"],
                    datetime.strptime(weeks[0]["contributionDays"][0]["date"],
                                      "%Y-%m-%d").strftime("%Y")))
        # The pair of slashes a drawing uses to say a length was taken out, so
        # the axis is never mistaken for a continuous one.
        for k in (0, 1):
            bx = gx + void_w + 10 + k * 9
            p.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="1.5" '
                     'fill="none"/>'
                     % (bx - 5, top + grid_h + 6, bx + 5, top - 6, t["ink3"]))

    for r in range(7):
        p.append('<text x="%d" y="%.1f" font-family="%s" font-size="11" fill="%s">%s</text>'
                 % (M, top + r * ch + 25, MONO, t["ink3"], DAYS[r]))

    # --- month ruler over the live stretch only
    #
    # The "account opens" label shares this row and is far wider than a month
    # name, so it claims its own span first and any month tick landing inside
    # that span is dropped rather than printed through it.
    opens_label = "account opens · " + opened.strftime("%d %b %Y")
    opens_x = lx - gap + 7
    opens_end = opens_x + len(opens_label) * 6.9

    seen = set()
    for i, wk in enumerate(live):
        d = datetime.strptime(wk["contributionDays"][0]["date"], "%Y-%m-%d").date()
        if d.month in seen:
            continue
        seen.add(d.month)
        mx = lx + i * cw
        if mx < opens_end:
            continue
        p.append('<text x="%.1f" y="%d" font-family="%s" font-size="10" fill="%s" '
                 'letter-spacing="1">%s</text>'
                 % (mx, top - 12, MONO, t["ink3"], MONTHS[d.month - 1]))

    for i, wk in enumerate(live):
        by_day = {d["weekday"]: d for d in wk["contributionDays"]}
        for r in range(7):
            d = by_day.get(r)
            if d is None:
                continue
            x, y = lx + i * cw, top + r * ch
            day = datetime.strptime(d["date"], "%Y-%m-%d").date()
            cnt = d["contributionCount"]
            if day < opened:
                # A few days of the first live week still predate the account.
                # They get the hairline, not a filled zero: a filled cell would
                # be a claim about a day that has none.
                p.append('<rect x="%.2f" y="%.1f" width="%.2f" height="%d" fill="none" '
                         'stroke="%s" stroke-width="0.75"/>'
                         % (x + 0.4, y + 0.4, cw - gap - 0.8, ch - gap - 1, t["rule2"]))
                continue
            lvl = d.get("_level")
            if lvl is None:
                lvl = 0 if cnt == 0 else 1 + min(
                    3, int(3 * (cnt - 1) / max(1, peak - 1))
                )
            fill = t["heat"][lvl]
            p.append('<rect x="%.2f" y="%.1f" width="%.2f" height="%d" fill="%s"/>'
                     % (x, y, cw - gap, ch - gap, fill))
            if cnt:
                p.append('<text x="%.2f" y="%.1f" font-family="%s" font-size="15" fill="%s" '
                         'text-anchor="middle">%02x</text>'
                         % (x + (cw - gap) / 2, y + (ch - gap) / 2 + 5, MONO,
                            on(fill, t), min(cnt, 255)))

    # Where the elided stretch ends and the record begins.
    p.append('<rect x="%.1f" y="%d" width="1.5" height="%d" fill="%s"/>'
             % (lx - gap, top - 4, grid_h + 8, t["accent"]))
    p.append('<text x="%.1f" y="%d" font-family="%s" font-size="10" fill="%s" '
             'letter-spacing="0.8">%s</text>'
             % (opens_x, top - 12, MONO, t["accent"], esc(opens_label)))

    # legend
    ly = top + grid_h + 32
    p.append('<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s">0x00</text>'
             % (M, ly + 12, MONO, t["ink3"]))
    for i, c in enumerate(t["heat"]):
        p.append('<rect x="%d" y="%d" width="22" height="16" fill="%s"/>'
                 % (M + 40 + i * 26, ly, c))
    p.append('<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s">0x%02x</text>'
             % (M + 40 + 5 * 26 + 4, ly + 12, MONO, t["ink3"], peak))
    p.append('<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s" text-anchor="end">'
             'a hairline cell is a day with no byte · a blank cell is a day with no commit</text>'
             % (W - M, ly + 12, MONO, t["ink3"]))
    p.append("</svg>")
    return "\n".join(p) + "\n"

# --------------------------------------------------------------------------- 3. segments

def build_segments(theme_name, projects, lang_colour):
    """Every project as a segment on one time axis: it starts the day the
    repository was created and ends on its last push. How long a bar is says
    something a star count does not."""
    t = THEMES[theme_name]
    items = sorted(projects, key=lambda r: r["createdAt"])
    rh = 26
    lab_w = 210
    top = 108
    H = int(top + len(items) * rh + 66)

    lo = min(datetime.strptime(r["createdAt"][:10], "%Y-%m-%d").date() for r in items)
    hi = max(datetime.strptime(r["pushedAt"][:10], "%Y-%m-%d").date() for r in items)
    span = max(1, (hi - lo).days)
    ax, aw = M + lab_w, CONTENT - lab_w - 96

    def px(d):
        return ax + aw * (d - lo).days / span

    p = head(W, H, "Segment map: %d projects between %s and %s" % (len(items), lo, hi))
    p += plate(t, W, H)
    p += caption(t, 52, "segment map", "%s → %s · %d days"
                 % (lo.strftime("%d %b"), hi.strftime("%d %b"), span))

    # month grid, drawn behind everything
    cur = date(lo.year, lo.month, 1)
    while cur <= hi:
        if cur >= lo:
            x = px(cur)
            p.append('<rect x="%.1f" y="%d" width="1" height="%d" fill="%s"/>'
                     % (x, top - 18, len(items) * rh + 20, t["rule2"]))
            p.append('<text x="%.1f" y="%d" font-family="%s" font-size="10" fill="%s" '
                     'letter-spacing="1">%s</text>' % (x + 5, top - 26, MONO, t["ink3"],
                                                       MONTHS[cur.month - 1]))
        cur = date(cur.year + (cur.month == 12), cur.month % 12 + 1, 1)

    for i, r in enumerate(items):
        y = top + i * rh
        a = datetime.strptime(r["createdAt"][:10], "%Y-%m-%d").date()
        b = datetime.strptime(r["pushedAt"][:10], "%Y-%m-%d").date()
        x0, x1 = px(a), px(b)
        lang = (r["primaryLanguage"] or {}).get("name")
        colour = lang_colour.get(lang, t["tail"])
        p.append('<text x="%d" y="%d" font-family="%s" font-size="12" fill="%s">%s</text>'
                 % (M, y + 14, MONO, t["ink2"], esc(r["name"])))
        # A repository created and last pushed on the same day is a real event,
        # not a zero-width bar: floor the width so it still reads as a mark.
        p.append('<rect x="%.1f" y="%d" width="%.1f" height="10" fill="%s"/>'
                 % (x0, y + 4, max(3.0, x1 - x0), colour))
        p.append('<rect x="%.1f" y="%d" width="2" height="16" fill="%s"/>' % (x0, y + 1, colour))
        days = (b - a).days
        p.append('<text x="%d" y="%d" font-family="%s" font-size="10.5" fill="%s" '
                 'text-anchor="end">%s</text>'
                 % (W - M, y + 13, MONO, t["ink3"],
                    "%d d" % days if days else "same day"))

    p += rule(t, top + len(items) * rh + 2, ax, aw, t["rule"])
    p.append('<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s">'
             'bar length is how long the repository stayed open, not effort inside it · '
             'colour is the primary language, matching the map below</text>'
             % (M, H - 26, MONO, t["ink3"]))
    p.append("</svg>")
    return "\n".join(p) + "\n"


# --------------------------------------------------------------------------- 4. language map

def kb(n):
    if n >= 1 << 20:
        return "%.1f MB" % (n / (1 << 20))
    if n >= 1 << 10:
        return "%.0f KB" % (n / (1 << 10))
    return "%d B" % n


def language_colours(theme_name, repos):
    """The colour each language is given in the language map. Returned on its
    own so the segment map can use the same one: two figures colouring Rust
    differently would be two figures, not one document."""
    t = THEMES[theme_name]
    agg = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            agg[e["node"]["name"]] = agg.get(e["node"]["name"], 0) + e["size"]
    order = sorted(agg, key=lambda k: -agg[k])
    return {n: (t["ramp"][i] if i < len(t["ramp"]) else t["tail"])
            for i, n in enumerate(order)}


def build_langs(theme_name, repos):
    """Languages laid out as a memory map. The offsets are real: GitHub reports
    each language in bytes, so the map's start and end addresses are the actual
    byte ranges, not a pie chart wearing a costume."""
    t = THEMES[theme_name]
    agg = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            agg[e["node"]["name"]] = agg.get(e["node"]["name"], 0) + e["size"]
    items = sorted(agg.items(), key=lambda kv: -kv[1])
    total = sum(agg.values()) or 1

    bar_y, bar_h = 108, 56
    rows = items[:6]
    H = 108 + bar_h + 44 + len(rows) * 28 + 60

    p = head(W, H, "Language map: %s of source across %d languages" % (kb(total), len(items)))
    p += plate(t, W, H)
    p += caption(t, 52, "language map", "%s of source · %d languages" % (kb(total), len(items)))

    p.append('<text x="%d" y="%d" font-family="%s" font-size="10.5" fill="%s">0x000000</text>'
             % (M, bar_y - 12, MONO, t["ink3"]))
    p.append('<text x="%d" y="%d" font-family="%s" font-size="10.5" fill="%s" '
             'text-anchor="end">0x%06X</text>' % (W - M, bar_y - 12, MONO, t["ink3"], total))

    x = float(M)
    ramp, offsets = t["ramp"], []
    for i, (name, size) in enumerate(items):
        w = CONTENT * size / total
        colour = ramp[i] if i < len(ramp) else t["tail"]
        offsets.append((name, size, int((x - M) * total / CONTENT), colour))
        p.append('<rect x="%.2f" y="%d" width="%.2f" height="%d" fill="%s"/>'
                 % (x, bar_y, w, bar_h, colour))
        # A hairline in the page colour, not a gap: the map is contiguous
        # memory and a gap would imply unallocated space between languages.
        if i:
            p.append('<rect x="%.2f" y="%d" width="1" height="%d" fill="%s"/>'
                     % (x, bar_y, bar_h, t["bg"]))
        if w > 96:
            p.append('<text x="%.2f" y="%d" font-family="%s" font-size="12" fill="%s" '
                     'letter-spacing="0.4">%s</text>'
                     % (x + 12, bar_y + 23, MONO, on(colour, t), esc(name)))
            p.append('<text x="%.2f" y="%d" font-family="%s" font-size="11" fill="%s" '
                     'opacity="0.78">%.1f%%</text>'
                     % (x + 12, bar_y + 41, MONO, on(colour, t), 100 * size / total))
        x += w

    ty = bar_y + bar_h + 44
    cols = [M, M + 200, M + 330, M + 460, M + 590]
    p.append('<g font-family="%s" font-size="10" fill="%s" letter-spacing="1.3">' % (MONO, t["ink3"]))
    for cx, lab in zip(cols, ("LANGUAGE", "START", "SIZE", "BYTES", "SHARE")):
        p.append('<text x="%d" y="%d">%s</text>' % (cx, ty, lab))
    p.append("</g>")
    p += rule(t, ty + 10)

    for i, (name, size, start, colour) in enumerate(offsets[:len(rows)]):
        y = ty + 38 + i * 28
        p.append('<rect x="%d" y="%d" width="10" height="10" fill="%s"/>' % (M, y - 9, colour))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="12.5" fill="%s">%s</text>'
                 % (M + 20, y, MONO, t["ink2"], esc(name)))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="11.5" fill="%s">0x%06X</text>'
                 % (cols[1], y, MONO, t["ink3"], start))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="11.5" fill="%s">%s</text>'
                 % (cols[2], y, MONO, t["ink"], kb(size)))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="11.5" fill="%s" '
                 'style="font-variant-numeric:tabular-nums">%d</text>'
                 % (cols[3], y, MONO, t["ink3"], size))
        p.append('<text x="%d" y="%d" font-family="%s" font-size="11.5" fill="%s">%.1f%%</text>'
                 % (cols[4], y, MONO, t["ink2"], 100 * size / total))

    rest = items[len(rows):]
    if rest:
        p.append('<text x="%d" y="%d" font-family="%s" font-size="10.5" fill="%s">'
                 '+ %s</text>' % (M, H - 30, MONO, t["ink3"],
                                  esc(", ".join("%s %s" % (n, kb(s)) for n, s in rest))))
    p.append("</svg>")
    return "\n".join(p) + "\n"
