#!/usr/bin/env python3
"""Phase 1 done-bar: every in-scope map has a map.yml; every .bsp present
parses as a valid entity lump; every .loc file that exists parses cleanly;
anything missing an asset is listed as an explicit gap, never silently
dropped. Exits non-zero if any *structural* check fails (a genuinely
broken file) — missing assets are a reported gap, not a failure.
"""
import re
import struct
import sys
from pathlib import Path

MAPS_DIR = Path("maps")


def check_bsp(path):
    data = path.read_bytes()
    if data[0:4] not in (struct.pack("<i", 29), b"BSP2", b"2PSB"):
        return f"unrecognized bsp header magic: {data[0:4]!r}"
    try:
        _, ofs, ln = struct.unpack("<iii", data[0:12])
        text = data[ofs:ofs + ln].decode("latin-1")
        if "worldspawn" not in text:
            return "entity lump has no worldspawn — likely corrupt"
    except Exception as e:
        return f"failed to read entity lump: {e}"
    return None


def check_loc(path):
    for i, raw in enumerate(path.read_bytes().split(b"\r\n"), 1):
        line = raw.decode("latin-1").strip()
        if not line:
            continue
        parts = line.split(None, 3)
        if len(parts) < 4:
            return f"line {i}: expected 'X Y Z name', got {line!r}"
        try:
            [float(p) for p in parts[:3]]
        except ValueError:
            return f"line {i}: non-numeric coordinates: {line!r}"
    return None


def check_yaml(path):
    required = {"brackets", "source", "play_count", "author", "license_note",
                "has_bsp", "has_ent", "has_textures", "loc_status"}
    text = path.read_text()
    present = {line.split(":", 1)[0].strip().lstrip("- ") for line in text.splitlines()
               if ":" in line or line.strip().startswith("-")}
    # crude but sufficient for our own hand-rolled yaml writer
    top_level_keys = {line.split(":", 1)[0] for line in text.splitlines() if ":" in line and not line.startswith(" ")}
    missing = required - top_level_keys
    if missing:
        return f"map.yml missing keys: {missing}"
    return None


def main():
    errors = []
    gaps = []
    checked = 0

    for map_dir in sorted(MAPS_DIR.iterdir()):
        if not map_dir.is_dir():
            continue
        name = map_dir.name
        checked += 1

        yml = map_dir / "map.yml"
        if not yml.exists():
            errors.append(f"{name}: missing map.yml")
        else:
            err = check_yaml(yml)
            if err:
                errors.append(f"{name}: {err}")

        bsp = map_dir / "maps" / f"{name}.bsp"
        if not bsp.exists():
            gaps.append(f"{name}: no .bsp (see README gap list)")
        else:
            err = check_bsp(bsp)
            if err:
                errors.append(f"{name}: bsp check failed — {err}")

        loc = map_dir / "locs" / f"{name}.loc"
        if loc.exists():
            err = check_loc(loc)
            if err:
                errors.append(f"{name}: loc check failed — {err}")

    print(f"Checked {checked} map dirs.")
    print(f"{len(gaps)} gaps (no local asset — expected, tracked in README):")
    for g in gaps:
        print(f"  - {g}")

    if errors:
        print(f"\n{len(errors)} STRUCTURAL FAILURES (these are real bugs, not gaps):")
        for e in errors:
            print(f"  ! {e}")
        sys.exit(1)
    else:
        print("\nNo structural failures. Phase 1 done-bar: clean.")


if __name__ == "__main__":
    main()
