#!/usr/bin/env python3
"""Scrape daily contribution counts from GitHub's public contributions fragment
(no token, no GraphQL) and write data/contributions.json with derived stats.
Run daily by .github/workflows/update-profile-art.yml."""
import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "BelalAboseada")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "contributions.json")


def fetch_days():
    r = requests.get(URL, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day[data-date]"):
        tip = tips.get(td.get("id"), "")
        m = re.match(r"(\d[\d,]*)", tip)
        count = int(m.group(1).replace(",", "")) if m else 0
        days.append({"date": td["data-date"], "count": count, "level": int(td.get("data-level") or 0)})
    if not days:
        sys.exit("no calendar cells found -- GitHub markup may have changed")
    return sorted(days, key=lambda d: d["date"])


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    i = len(days) - 1
    if days[i]["count"] == 0:
        i -= 1  # today isn't over yet -- don't break the streak on it
    current = 0
    while i >= 0 and days[i]["count"]:
        current += 1
        i -= 1
    return current, longest


def build(days):
    total = sum(d["count"] for d in days)
    active = sum(1 for d in days if d["count"])
    current, longest = streaks(days)
    best = max(days, key=lambda d: d["count"])
    monthly = {}
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
    return {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": [{"month": k, "total": v} for k, v in sorted(monthly.items())],
        "days": days,
    }


if __name__ == "__main__":
    data = build(fetch_days())
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    print(f"{data['total_contributions']} contributions · streak {data['current_streak']} "
          f"· longest {data['longest_streak']}")
