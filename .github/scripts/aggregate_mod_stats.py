"""Aggregates mod ratings / favorites from labelled GitHub issues into stats.json.

Each issue created from the "模组评分与青睐" issue form contains:
    ### 模组
    Community/testmod
    ### 评分
    5
    ### 青睐
    是
    ### 社区评价
    ...

Only open issues labelled "mod-vote" are counted. Every GitHub account keeps one
vote per mod; editing the issue updates that vote. Closed issues are ignored, so a
user can withdraw a vote by closing the issue.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")
STATS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "stats.json")

PATH_RE = re.compile(r"^(Official|Community)/([^/\\]+)$", re.IGNORECASE)


def api_get(url):
    request = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "Mercury-DreamLab-Stats",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def list_vote_issues():
    issues = []
    page = 1
    while True:
        url = (API + "/repos/" + REPO + "/issues?state=open&per_page=100&page=" + str(page))
        batch = api_get(url)
        if not batch:
            break
        for item in batch:
            if "pull_request" not in item:
                issues.append(item)
        if len(batch) < 100:
            break
        page += 1
    return issues


def parse_sections(body):
    sections = {}
    current = None
    for line in (body or "").replace("\r\n", "\n").split("\n"):
        if line.startswith("### "):
            current = line[4:].strip()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    result = {}
    for key, lines in sections.items():
        text = "\n".join(lines).strip()
        if text == "_No response_":
            text = ""
        result[key] = text
    return result


def normalize_mod(value):
    value = (value or "").strip().replace("\\", "/").lstrip("/")
    match = PATH_RE.match(value)
    if not match:
        return None
    if match.group(2).lower() == "mod_template":
        return None
    return match.group(1).capitalize() + "/" + match.group(2)


def main():
    if not REPO:
        print("GITHUB_REPOSITORY is not set", file=sys.stderr)
        return 1

    latest = {}
    for issue in list_vote_issues():
        sections = parse_sections(issue.get("body"))
        mod = normalize_mod(sections.get("模组"))
        if not mod:
            continue
        user = (issue.get("user") or {}).get("login", "")
        if not user:
            continue
        updated = issue.get("updated_at", "")
        key = (mod, user.lower())
        if key not in latest or updated > latest[key][0]:
            latest[key] = (updated, sections)

    totals = {}
    for (mod, _user), (_updated, sections) in latest.items():
        rating = None
        text = (sections.get("评分") or "").strip()
        if text.isdigit() and 1 <= int(text) <= 5:
            rating = int(text)

        favorite_text = (sections.get("青睐") or "").strip().lower()
        favorite = favorite_text in ("是", "yes", "true", "1")

        if rating is None and not favorite:
            continue

        entry = totals.setdefault(mod, {"ratingSum": 0, "ratingCount": 0, "favorites": 0})
        if rating is not None:
            entry["ratingSum"] += rating
            entry["ratingCount"] += 1
        if favorite:
            entry["favorites"] += 1

    mods = []
    for path in sorted(totals):
        entry = totals[path]
        average = 0.0
        if entry["ratingCount"] > 0:
            average = round(entry["ratingSum"] / entry["ratingCount"], 2)
        mods.append({
            "path": path,
            "ratingAvg": average,
            "ratingCount": entry["ratingCount"],
            "favorites": entry["favorites"],
        })

    existing = None
    if os.path.exists(STATS_PATH):
        try:
            with open(STATS_PATH, "r", encoding="utf-8") as handle:
                existing = json.load(handle).get("mods")
        except (ValueError, OSError):
            existing = None

    if existing == mods:
        print("stats unchanged")
        return 0

    payload = {
        "schema": 1,
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mods": mods,
    }
    with open(STATS_PATH, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print("wrote " + STATS_PATH + " with " + str(len(mods)) + " mods")
    return 0


if __name__ == "__main__":
    sys.exit(main())
