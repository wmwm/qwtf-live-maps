#!/usr/bin/env python3
"""Build per-map map.yml from the harvest/crossref/loc-generation reports,
and generate the top-level README's bracket tables from that metadata —
no hand-maintained per-bracket file duplication.
"""
import json
from pathlib import Path

MAPS_DIR = Path("maps")
BRACKETS = ["2v2", "3v3", "4v4", "5v5"]


def yaml_escape(s):
    if s is None:
        return "null"
    if isinstance(s, bool):
        return "true" if s else "false"
    if isinstance(s, (int, float)):
        return str(s)
    s = str(s)
    if any(c in s for c in ':#{}[]&*!|>\'"%@`') or s.strip() != s or s == "":
        return '"' + s.replace('"', '\\"') + '"'
    return s


def write_yaml(path, data):
    lines = []
    for k, v in data.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {yaml_escape(item)}")
        else:
            lines.append(f"{k}: {yaml_escape(v)}")
    path.write_text("\n".join(lines) + "\n")


def main():
    rotation = json.load(open("data/rotation.json"))
    crossref = json.load(open("data/logs-crossref.json"))
    harvest = json.load(open("data/harvest-report.json"))
    try:
        loc_report = json.load(open("data/loc-generation-report.json"))
    except FileNotFoundError:
        loc_report = {"sources": {}}

    map_brackets = {}
    for bracket, maps in rotation.items():
        for m in maps:
            map_brackets.setdefault(m, []).append(bracket)

    rotation_maps = set(map_brackets)
    unlisted_played = set(crossref["unlisted_but_played_recently"])
    all_maps = sorted(rotation_maps | unlisted_played)

    per_map_meta = {}
    for name in all_maps:
        brackets = sorted(map_brackets.get(name, []), key=BRACKETS.index)
        in_rotation = name in rotation_maps
        play_count = crossref["match_counts"].get(name)
        h = harvest.get(name, {})
        loc_info = loc_report.get("sources", {}).get(name)
        if name in ("2fort5r", "1on1forts"):
            loc_status = "community"
        elif loc_info:
            loc_status = ("author-in-map" if loc_info["source"] == "author-in-map"
                          else "heuristic-unreviewed")
        else:
            loc_status = "missing"

        bsp_source = h.get("bsp_source") or ""
        asset_provenance = "external-archive" if bsp_source.startswith("external:") else (
            "workspace-local" if h.get("bsp") else "none")

        meta = {
            "brackets": brackets if brackets else [],
            "source": "rotation+logs" if (in_rotation and name in crossref["match_counts"] and crossref["match_counts"].get(name))
                      else ("rotation-list" if in_rotation else "logs-only"),
            "play_count": play_count,
            "author": "unknown",
            "license_note": "community map, attribution-only (scene convention)",
            "has_bsp": h.get("bsp", False),
            "has_ent": h.get("ent", False),
            "has_textures": h.get("textures", False),
            "loc_status": loc_status,
            "asset_provenance": asset_provenance,
        }
        per_map_meta[name] = meta
        map_dir = MAPS_DIR / name
        map_dir.mkdir(parents=True, exist_ok=True)
        write_yaml(map_dir / "map.yml", meta)

    json.dump(per_map_meta, open("data/map-metadata.json", "w"), indent=2, sort_keys=True)

    build_readme(per_map_meta, map_brackets)
    print(f"Wrote map.yml for {sum(1 for n in all_maps if (MAPS_DIR / n).exists())} maps")
    print("Wrote README.md")


def build_readme(per_map_meta, map_brackets):
    lines = []
    lines.append("# QWTF Live Map Repo")
    lines.append("")
    lines.append("Community catalog + asset source for the maps actually played on QWTF Live.")
    lines.append("Not an archive of every map ever made for QuakeWorld Team Fortress —")
    lines.append("scoped to the current competitive rotation and what real matches show")
    lines.append("people actually playing, cross-checked against "
                 "[logs.qwtf.live](https://logs.qwtf.live/).")
    lines.append("")
    lines.append("## Map status legend")
    lines.append("")
    lines.append("- **loc status**: `author-in-map` (extracted from the map's own built-in "
                 "location entities — highest confidence), `community` (hand-authored, "
                 "imported from the wider QW scene), `heuristic-unreviewed` (auto-generated "
                 "from spawn/flag/item positions, needs a playtester's eyes), `missing`.")
    lines.append("")

    for bracket in BRACKETS:
        names = sorted(n for n, meta in per_map_meta.items() if bracket in meta["brackets"])
        if not names:
            continue
        lines.append(f"## {bracket}")
        lines.append("")
        lines.append("| Map | Matches (logs.qwtf.live) | Assets | Loc status |")
        lines.append("|---|---|---|---|")
        for n in sorted(names, key=lambda x: -(per_map_meta[x]["play_count"] or -1)):
            meta = per_map_meta[n]
            assets = "bsp" + ("+ent" if meta["has_ent"] else "") + ("+tex" if meta["has_textures"] else "")
            if not meta["has_bsp"]:
                assets = "**missing**"
            pc = meta["play_count"] if meta["play_count"] is not None else "?"
            lines.append(f"| `{n}` | {pc} | {assets} | {meta['loc_status']} |")
        lines.append("")

    unlisted = sorted(n for n, meta in per_map_meta.items() if not meta["brackets"])
    if unlisted:
        lines.append("## Played but not in the static rotation list")
        lines.append("")
        lines.append("Found via real match data on logs.qwtf.live, not the Discord `!maps` "
                     "output — flagged here for a human call on whether the rotation list "
                     "itself is stale.")
        lines.append("")
        for n in unlisted:
            meta = per_map_meta[n]
            lines.append(f"- `{n}` — {meta['play_count']} matches, "
                         f"assets: {'yes' if meta['has_bsp'] else 'MISSING'}")
        lines.append("")

    external = sorted(n for n, meta in per_map_meta.items() if meta["asset_provenance"] == "external-archive")
    if external:
        lines.append("## Sourced from an external archive, not this workspace")
        lines.append("")
        lines.append("Not present in any local copy — pulled from "
                     "[maps.quakeworld.nu](https://maps.quakeworld.nu/all/)'s public map "
                     "archive after confirming an exact filename match. Flagged separately "
                     "from workspace-local assets since that provenance is weaker (not "
                     "verified byte-identical to whatever QWTF Live's own servers actually "
                     "run) — worth a playtester's sanity check before treating as equivalent.")
        lines.append("")
        for n in external:
            lines.append(f"- `{n}`")
        lines.append("")

    missing_bsp = sorted(n for n, meta in per_map_meta.items() if not meta["has_bsp"])
    if missing_bsp:
        lines.append("## Gaps — no asset found anywhere, including public archives")
        lines.append("")
        lines.append("These are in scope but no `.bsp` exists in this workspace, and a check "
                     "against maps.quakeworld.nu's own \"every known QuakeWorld map\" archive "
                     "came up empty too. Not invented, not silently dropped — genuinely need "
                     "sourcing from wherever QWTF Live's own servers get them.")
        lines.append("")
        for n in missing_bsp:
            lines.append(f"- `{n}`")
        lines.append("")

    Path("README.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
