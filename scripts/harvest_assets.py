#!/usr/bin/env python3
"""Harvest per-map assets from what already exists locally into maps/<name>/.

Sources (read-only, never modified):
- bsp:      wm-fortressone-source/FortressOne/fortress/maps/<name>.bsp
            (Tim's real FortressOne install — 179 maps, the canonical set)
- ent:      qwtf-bots-playtest/fortress/maps/<name>.ent (opportunistic, optional)
- textures: wm-qwtf-client/content/configs/textures/<name>/ (already-curated
            per-map texture harvest from an earlier project, opportunistic)

sound/ and progs/ are NOT harvested per-map: FortressOne ships one shared
mod-wide sound/progs set to every server and client, unlike the old
FortressOne/map-repo archive convention of bespoke per-map submissions.
This is a deliberate scope decision, not an oversight.

A handful of maps aren't sitting in any local tree — EXTERNAL_BSP_SOURCES
is a last-resort, explicit, one-by-one fallback to a public map archive for
those specific names only (checked by hand against maps.quakeworld.nu's
own "every known QuakeWorld map" listing before being added here — never
a blind bulk pull). bsp_source records "external:<url>" for these so
map.yml/README can distinguish them from workspace-local provenance.

Writes data/harvest-report.json: what got copied per map, what's missing.
"""
import json
import shutil
import urllib.request
from pathlib import Path

DEV_ROOT = Path("/home/wm-dev/Development")
# Priority order: canonical reference install first, then whichever project
# tree happens to already have a copy. No single tree is a complete superset.
BSP_SRCS = [
    DEV_ROOT / "wm-fortressone-source/FortressOne/fortress/maps",
    DEV_ROOT / "wm-qwtf-client/content/configs/maps",
    DEV_ROOT / "qwtf-bots-playtest/fortress/maps",
    DEV_ROOT / "QWTF Bots/pub_iso/fortress/maps",
    DEV_ROOT / "wm-qwtf-maps/fortress/maps",
    DEV_ROOT / "fte-demo-harness/base/fortress/maps",
]
ENT_SRC = DEV_ROOT / "qwtf-bots-playtest/fortress/maps"
TEX_SRC = DEV_ROOT / "wm-qwtf-client/content/configs/textures"
OUT = Path("maps")

EXTERNAL_BSP_SOURCES = {
    # Confirmed present in maps.quakeworld.nu's full archive listing
    # (checked 2026-07-18); elusive/fracturex2/h4rdcoremini/nightshacksb5
    # were checked against the same listing and are genuinely absent there.
    "box4": "https://maps.quakeworld.nu/all/box4.bsp",
}


def _fetch_external_bsp(name, dest):
    url = EXTERNAL_BSP_SOURCES[name]
    req = urllib.request.Request(url, headers={"User-Agent": "qwtf-live-maps-harvest/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    if data[0:4] not in (b"\x1d\x00\x00\x00", b"BSP2", b"2PSB"):
        raise ValueError(f"{name}: downloaded file doesn't look like a bsp (bad magic)")
    dest.write_bytes(data)


def all_in_scope_maps():
    rotation = json.load(open("data/rotation.json"))
    rotation_maps = {m for maps in rotation.values() for m in maps}
    crossref = json.load(open("data/logs-crossref.json"))
    unlisted = set(crossref["unlisted_but_played_recently"])
    return sorted(rotation_maps | unlisted)


def harvest():
    report = {}
    for name in all_in_scope_maps():
        entry = {"bsp": False, "bsp_source": None, "ent": False, "textures": False}
        map_dir = OUT / name
        for src_dir in BSP_SRCS:
            bsp_path = src_dir / f"{name}.bsp"
            if bsp_path.exists():
                (map_dir / "maps").mkdir(parents=True, exist_ok=True)
                shutil.copy2(bsp_path, map_dir / "maps" / f"{name}.bsp")
                entry["bsp"] = True
                entry["bsp_source"] = str(src_dir)
                break

        if not entry["bsp"] and name in EXTERNAL_BSP_SOURCES:
            (map_dir / "maps").mkdir(parents=True, exist_ok=True)
            dest = map_dir / "maps" / f"{name}.bsp"
            try:
                _fetch_external_bsp(name, dest)
                entry["bsp"] = True
                entry["bsp_source"] = f"external:{EXTERNAL_BSP_SOURCES[name]}"
            except Exception as e:
                print(f"  ! external fetch failed for {name}: {e}")
                if dest.exists():
                    dest.unlink()

        ent_path = ENT_SRC / f"{name}.ent"
        if ent_path.exists():
            (map_dir / "maps").mkdir(parents=True, exist_ok=True)
            shutil.copy2(ent_path, map_dir / "maps" / f"{name}.ent")
            entry["ent"] = True

        tex_dir = TEX_SRC / name
        if tex_dir.is_dir() and any(tex_dir.iterdir()):
            dest = map_dir / "textures" / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(tex_dir, dest)
            entry["textures"] = True

        report[name] = entry

    json.dump(report, open("data/harvest-report.json", "w"), indent=2, sort_keys=True)

    missing_bsp = [n for n, e in report.items() if not e["bsp"]]
    print(f"Harvested {len(report)} maps.")
    print(f"  bsp found:      {sum(e['bsp'] for e in report.values())}/{len(report)}")
    print(f"  ent found:      {sum(e['ent'] for e in report.values())}/{len(report)}")
    print(f"  textures found: {sum(e['textures'] for e in report.values())}/{len(report)}")
    if missing_bsp:
        print(f"  MISSING bsp (no local asset found): {missing_bsp}")


if __name__ == "__main__":
    harvest()
