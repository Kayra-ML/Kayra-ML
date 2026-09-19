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
    """Current-year contribution calendar using GitHub's year-view geometry.

    Past days are always rendered as filled cells, including 0-contribution
    days. Days outside the selected year and future days are left blank. This
    mirrors the visual semantics of GitHub's own contribution graph while
    keeping the hexdump byte labels for active days.
    """
    t = THEMES[theme_name]
    api_weeks = u["contributionsCollection"]["contributionCalendar"]["weeks"]
    opened = datetime.strptime(u["createdAt"][:10], "%Y-%m-%d").date()

    counts = {}
    available_dates = []
    for wk in api_weeks:
        for d in wk["contributionDays"]:
            counts[d["date"]] = d["contributionCount"]
            available_dates.append(datetime.strptime(d["date"], "%Y-%m-%d").date())

    today = max(available_dates) if available_dates else date.today()
    year = today.year
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)

    # GitHub's rows are Sunday -> Saturday. Include the partial week at each
    # edge of the year, but leave out-of-year days blank.
    grid_start = year_start - timedelta(days=(year_start.weekday() + 1) % 7)
    grid_end = year_end + timedelta(days=(5 - year_end.weekday()) % 7)

    weeks = []
    cur = grid_start
    while cur <= grid_end:
        weeks.append([cur + timedelta(days=i) for i in range(7)])
        cur += timedelta(days=7)

    year_counts = [
        counts.get(d.isoformat(), 0)
        for wk in weeks for d in wk
        if d.year == year and opened <= d <= today
    ]
    total = sum(year_counts)
    peak = max(year_counts, default=1)

    lab_w, gap = 44, 4
    top = 104
    gx = M + lab_w + 8
    right = M + CONTENT

    # Use the full available width and derive vertical pitch from the same value,
    # so every contribution cell is a true square.
    pitch = (right - gx) / len(weeks)
    cell = pitch - gap
    grid_h = 7 * pitch - gap
    H = int(top + grid_h + 88)

    p = head(
        W, H,
        "%d contribution calendar: %d contributions, peak %d in one day. "
        "Past zero days are filled; future days are blank."
        % (year, total, peak)
    )
    p += plate(t, W, H)
    p += caption(
        t, 52, "hexdump contributions.cal",
        "%d · one byte per day · value = contributions · peak 0x%02x" % (year, peak)
    )

    # Day labels.
    for r in range(7):
        y = top + r * pitch + cell / 2 + 4
        p.append(
            '<text x="%d" y="%.1f" font-family="%s" font-size="11" fill="%s">%s</text>'
            % (M, y, MONO, t["ink3"], DAYS[r])
        )

    # Month labels. Put each month over the week that contains its first day.
    for month in range(1, 13):
        first = date(year, month, 1)
        week_index = (first - grid_start).days // 7
        mx = gx + week_index * pitch
        p.append(
            '<text x="%.1f" y="%d" font-family="%s" font-size="10" fill="%s" '
            'letter-spacing="1">%s</text>'
            % (mx, top - 12, MONO, t["ink3"], MONTHS[month - 1])
        )

    for i, wk in enumerate(weeks):
        for r, day in enumerate(wk):
            # Outside-year cells and future dates are intentionally absent,
            # exactly like GitHub's year view.
            if day.year != year or day > today or day < opened:
                continue

            cnt = counts.get(day.isoformat(), 0)
            lvl = 0 if cnt == 0 else 1 + min(
                3, int(3 * (cnt - 1) / max(1, peak - 1))
            )
            fill = t["heat"][lvl]
            x = gx + i * pitch
            y = top + r * pitch

            p.append(
                '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>'
                % (x, y, cell, cell, fill)
            )

            if cnt:
                font = max(8.0, min(10.5, cell * 0.58))
                p.append(
                    '<text x="%.2f" y="%.2f" font-family="%s" font-size="%.1f" fill="%s" '
                    'text-anchor="middle">%02x</text>'
                    % (
                        x + cell / 2,
                        y + cell / 2 + font * 0.34,
                        MONO,
                        font,
                        on(fill, t),
                        min(cnt, 255),
                    )
                )

    # Legend.
    ly = top + grid_h + 32
    p.append(
        '<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s">0x00</text>'
        % (M, ly + 12, MONO, t["ink3"])
    )
    for i, c in enumerate(t["heat"]):
        p.append(
            '<rect x="%d" y="%d" width="22" height="16" fill="%s"/>'
            % (M + 40 + i * 26, ly, c)
        )
    p.append(
        '<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s">0x%02x</text>'
        % (M + 40 + 5 * 26 + 4, ly + 12, MONO, t["ink3"], peak)
    )
    p.append(
        '<text x="%d" y="%d" font-family="%s" font-size="10" fill="%s" text-anchor="end">'
        'filled dark cell = 0 contributions · no cell = future / outside year</text>'
        % (W - M, ly + 12, MONO, t["ink3"])
    )
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
