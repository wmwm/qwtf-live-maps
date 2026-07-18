#!/usr/bin/env python3
"""Cross-reference the Discord !maps rotation list against real match data
from logs.qwtf.live. For each rotation map, fetch its real match count.
Separately, sample recent match pages to catch maps that are actively
played but missing from the static rotation list.

Polite by design: small delay between requests, single-threaded, this is a
community-run site, not ours.
"""
import json
import re
import sys
import time
import urllib.request

BASE = "https://logs.qwtf.live/"
SLEEP = 0.6


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "qwtf-live-maps-crossref/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def match_count_for_map(mapname):
    """Fetch a far-out page number; pagy clamps to the last real page.
    total = (last_page - 1) * 50 + rows_on_last_page.
    """
    html = fetch(f"{BASE}?map={mapname}&page=9999")
    rows = len(re.findall(r'id="log_id"', html))
    m = re.search(r'class="current">(\d+)<', html)
    last_page = int(m.group(1)) if m else 1
    if rows == 0 and last_page == 1:
        # could genuinely be zero matches, or a single partial page
        pass
    return (last_page - 1) * 50 + rows


def recent_maps(pages=15):
    """Sample the N most recent pages of the unfiltered log list to find
    maps actively played that might not be in the static rotation list."""
    seen = {}
    for page in range(1, pages + 1):
        html = fetch(f"{BASE}?page={page}")
        for name in re.findall(r'href="/\?map=([^"&]+)"', html):
            seen[name] = seen.get(name, 0) + 1
        time.sleep(SLEEP)
    return seen


def main():
    rotation = json.load(open("data/rotation.json"))
    all_rotation_maps = sorted({m for maps in rotation.values() for m in maps})

    print(f"Fetching real match counts for {len(all_rotation_maps)} rotation maps...", file=sys.stderr)
    counts = {}
    for i, mapname in enumerate(all_rotation_maps, 1):
        try:
            counts[mapname] = match_count_for_map(mapname)
        except Exception as e:
            counts[mapname] = None
            print(f"  ! {mapname}: {e}", file=sys.stderr)
        print(f"  [{i}/{len(all_rotation_maps)}] {mapname}: {counts[mapname]}", file=sys.stderr)
        time.sleep(SLEEP)

    print("Sampling recent match pages for maps outside the rotation list...", file=sys.stderr)
    recent = recent_maps(pages=15)
    unlisted_but_played = sorted(set(recent) - set(all_rotation_maps))

    listed_but_never_played = sorted(m for m, c in counts.items() if c == 0)

    out = {
        "match_counts": counts,
        "unlisted_but_played_recently": unlisted_but_played,
        "listed_but_zero_matches": listed_but_never_played,
    }
    json.dump(out, open("data/logs-crossref.json", "w"), indent=2, sort_keys=True)
    print("Wrote data/logs-crossref.json", file=sys.stderr)
    print(f"  {len(listed_but_never_played)} rotation maps show 0 real matches", file=sys.stderr)
    print(f"  {len(unlisted_but_played)} maps played recently but not in rotation list: {unlisted_but_played}", file=sys.stderr)


if __name__ == "__main__":
    main()
