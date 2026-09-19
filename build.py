#!/usr/bin/env python3
"""Regenerate every figure and every project card on the profile from live
GitHub data.

Run locally with a token that can read public data:

    GITHUB_TOKEN=$(gh auth token) python build.py

In CI the workflow passes the job's GITHUB_TOKEN. Note the query asks for
user(login:...) and not viewer — inside Actions `viewer` is the bot, not Kayra.

Each figure is written twice, once per theme, and the README pairs them in a
<picture> so a reader on either GitHub theme gets the one meant for them.
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import assets                                            # noqa: E402
from theme import THEMES                                 # noqa: E402

USER = "KAYRA-ML"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets")
README = os.path.join(ROOT, "README.md")

QUERY = """
query($login: String!) {
  user(login: $login) {
    login createdAt
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC,
                 orderBy: {field: CREATED_AT, direction: ASC}) {
      totalCount
      nodes {
        name createdAt pushedAt stargazerCount isFork isArchived
        description
        licenseInfo { spdxId }
        repositoryTopics(first: 6) { nodes { topic { name } } }
        primaryLanguage { name }
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""


def fetch():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set. Try: GITHUB_TOKEN=$(gh auth token) python scripts/build.py")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": "bearer " + token,
                 "Content-Type": "application/json",
                 "User-Agent": USER + "-profile-builder"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        sys.exit("GraphQL error: " + json.dumps(payload["errors"])[:400])
    return payload["data"]["user"]


# --------------------------------------------------------------------------- project cards

# Prose worth keeping, written by hand, for the projects that have a real
# description in them. Anything NOT in here still gets a card — built from the
# repo's own GitHub description — so a new repository shows up on the profile
# without anyone editing this file. The two kinds of card are deliberately
# identical in chrome: a reader should not be able to tell which ones the author
# could not be bothered to write about.
CURATED = {
    "Rove_cli": (
        ["Go", "Wails", "React", "TypeScript"],
        "A local-first AI agent desktop and CLI: multi-session chat, Kanban, terminal "
        "multiplexing, memory, skills/plugins and background automation in one app."
    ),
    "ModelAudit": (
        ["LLM", "AI Forensics", "Prompt Engineering"],
        "An open framework for LLM identity forensics: fingerprinting model behavior, "
        "testing transparency and detecting when a model is wrapped behind another persona."
    ),
    "RoveCode_plugins": (
        ["TypeScript", "MCP", "AI Engineering"],
        "A token-efficient skill, routing and memory layer for AI coding tools, with "
        "domain-aware plugins, deterministic routing and persistent user preferences."
    ),
    "KeyLingo": (
        ["Python", "DeepL API", "macOS"],
        "A global macOS translator that turns typed text between Turkish and English "
        "inside any app using keyboard shortcuts, while preserving clipboard and input state."
    ),
    "SearchForge_open": (
        ["Python", "FastAPI", "Next.js", "Google Drive"],
        "A document search system for PDFs and files stored in Google Drive, with a "
        "FastAPI backend, browser PDF reading and keyword/page-level search."
    ),
    "fast_f1_data": (
        ["Python", "FastAPI", "PostgreSQL", "React"],
        "A full-stack Formula 1 data analysis platform for 2024-2025 data, built around "
        "RAM-efficient SQL queries, pagination and interactive driver/team analysis."
    ),
    "pyutils-toolkit": (
        ["Python"],
        "A lightweight Python utility library for common data-processing tasks: strings, "
        "dates, file I/O, configuration handling and logging helpers."
    ),
}

# GitHub reports a custom or unrecognised licence as one of these. Printing
# "Other" next to a project says nothing, so it is dropped instead.
LICENCE_NOISE = {"NOASSERTION", "other", "Other", None, ""}


def day(iso):
    return datetime.strptime(iso[:10], "%Y-%m-%d").strftime("%d %b %Y")


def render_card(r, index):
    """One project card. Curated prose if there is any, the repo's own
    description if there is not — never an empty cell, and never a visibly
    second-class one."""
    name = r["name"]
    stack, blurb = CURATED.get(name, (None, None))

    if blurb is None:
        lang = (r["primaryLanguage"] or {}).get("name")
        topics = [t["topic"]["name"] for t in r["repositoryTopics"]["nodes"]]
        # A repo tagged "go" whose primary language is Go would otherwise read
        # "Go · go", so fold anything that differs only by case.
        stack, seen = [], set()
        for s in ([lang] if lang else []) + topics:
            if s.lower() not in seen:
                seen.add(s.lower())
                stack.append(s)
        stack = stack[:4]
        blurb = (r["description"] or "").strip() or "_No description yet._"

    meta = [" · ".join("`%s`" % s for s in stack)] if stack else []
    if r["stargazerCount"]:
        meta.append("%d star%s" % (r["stargazerCount"], "" if r["stargazerCount"] == 1 else "s"))
    spdx = (r["licenseInfo"] or {}).get("spdxId")
    if spdx not in LICENCE_NOISE:
        meta.append(spdx)
    if r["isArchived"]:
        meta.append("archived")

    # Dates, not "3 hours ago". A relative stamp would differ on almost every
    # run and the workflow would commit every ten minutes forever; a date only
    # changes when Kayra actually pushes.
    foot = "0x%02X · %s → %s" % (index, day(r["createdAt"]), day(r["pushedAt"]))

    return "\n".join([
        "#### [%s](https://github.com/%s/%s)" % (name, USER, name),
        "<sub>%s</sub>" % " — ".join(meta),
        "",
        blurb,
        "",
        "<sub>%s</sub>" % foot,
    ])


def build_projects(repos):
    """The whole card grid, two per row, ordered curated-first then newest."""
    by = {r["name"]: r for r in repos}
    curated = [n for n in CURATED if n in by]
    rest = sorted((r for r in repos if r["name"] not in CURATED),
                  key=lambda r: r["createdAt"], reverse=True)
    ordered = [by[n] for n in curated] + rest

    rows = []
    for i in range(0, len(ordered), 2):
        pair = ordered[i:i + 2]
        cells = ['<td width="50%" valign="top">\n\n' + render_card(r, i + j) + '\n\n</td>'
                 for j, r in enumerate(pair)]
        if len(pair) == 1:                      # odd count: keep the grid square
            cells.append('<td width="50%"></td>')
        rows.append("<tr>\n" + "\n".join(cells) + "\n</tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


# --------------------------------------------------------------------------- figures

FIGURES = ("header", "fields", "calendar", "segments", "langs")

ALT = {
    "header": "Kayra, @KAYRA-ML. 18, Hatay, Türkiye. "
              "I'd rather speak the protocol than drive a browser.",
    "fields": "Activity as a struct: contributions, commits, repositories, "
              "busiest day and the date the account opened.",
    "calendar": "The most recent 26 weeks as a hexdump — one byte per day, "
                "the value is that day's commit count.",
    "segments": "Every public project as a segment on one time axis, from the "
                "day its repository was created to its last push.",
    "langs": "Languages as a memory map, sized by the bytes of source GitHub "
             "reports for each one.",
}


def figure(name):
    """A <picture> pairing the two themes. GitHub renders this natively, so the
    reader never gets the wrong one baked into an <img>."""
    return ("<picture>\n"
            '  <source media="(prefers-color-scheme: dark)" srcset="assets/%s-dark.svg">\n'
            '  <img alt="%s" src="assets/%s-light.svg" width="100%%">\n'
            "</picture>" % (name, ALT[name], name))


def render_figures(u, repos, projects, private):
    cc = u["contributionsCollection"]
    peak = max((d["contributionCount"]
                for w in cc["contributionCalendar"]["weeks"]
                for d in w["contributionDays"]), default=0)
    opened = u["createdAt"][:10]
    files = {}
    for theme in THEMES:
        colours = assets.language_colours(theme, repos)
        files["header-%s.svg" % theme] = assets.build_header(theme, u, len(projects))
        files["fields-%s.svg" % theme] = assets.build_fields(
            theme, cc, len(repos), peak, opened, private)
        files["calendar-%s.svg" % theme] = assets.build_calendar(theme, u)
        files["segments-%s.svg" % theme] = assets.build_segments(theme, projects, colours)
        files["langs-%s.svg" % theme] = assets.build_langs(theme, repos)
    return files, peak


# --------------------------------------------------------------------------- README

def replace_region(text, tag, body):
    pattern = r"<!--%s-->.*?<!--/%s-->" % (tag, tag)
    out, n = re.subn(pattern, lambda _: "<!--%s-->\n%s\n<!--/%s-->" % (tag, body, tag),
                     text, flags=re.S)
    if not n:
        print("WARNING: no <!--%s--> markers in README.md" % tag)
    return out


def update_readme(projects):
    """Rewrite the generated regions of README.md. Everything between a
    <!--tag--> pair is machine-owned; the prose around it is not touched."""
    if not os.path.exists(README):
        return False
    with open(README, encoding="utf-8") as f:
        before = f.read()

    after = replace_region(before, "projects", build_projects(projects))
    for name in FIGURES:
        after = replace_region(after, "fig-" + name, figure(name))

    if after == before:
        print("unchanged README.md")
        return False
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(after)
    print("updated README.md (%d project cards)" % len(projects))
    return True


# --------------------------------------------------------------------------- main

def main():
    u = fetch()
    repos = [r for r in u["repositories"]["nodes"] if not r["isFork"]]
    projects = [r for r in repos if r["name"].lower() != USER.lower()]
    cc = u["contributionsCollection"]

    # Which figure the contribution count is depends on the token, and the API
    # will not tell us: queried by the job's GITHUB_TOKEN, work in private repos
    # is simply absent and restrictedContributionsCount still comes back 0. So
    # the workflow sets COUNTS_PRIVATE when a personal token is configured, and
    # the label follows that rather than pretending to detect it.
    private = bool(os.environ.get("COUNTS_PRIVATE"))

    files, peak = render_figures(u, repos, projects, private)
    os.makedirs(OUT, exist_ok=True)
    for name, body in sorted(files.items()):
        path = os.path.join(OUT, name)
        old = ""
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                old = f.read()
        if old != body:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(body)
            print("updated %s" % name)
        else:
            print("unchanged %s" % name)

    update_readme(projects)
    print("contributions=%d commits=%d repos=%d peak=%d private_counted=%s"
          % (cc["contributionCalendar"]["totalContributions"],
             cc["totalCommitContributions"], len(repos), peak, private))


if __name__ == "__main__":
    main()
