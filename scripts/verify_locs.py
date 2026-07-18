#!/usr/bin/env python3
"""Sample-verify every .loc file for real accuracy, not just format.

validate.py checks that a .loc file PARSES (well-formed lines). This
checks whether each loc's coordinate is actually somewhere a player can
stand: walks the map's HULL 1 (the player-sized box clip hull, via the
CLIPNODES lump — the same hull the game engine uses for player movement
collision) from the worldspawn model's hull-1 headnode.

Deliberately NOT hull 0 (the thin point/render hull via NODES+LEAFS):
that hull has no thickness, so a point sitting exactly at floor height
— which is exactly where spawns, flags, and floor-level loc callouts are
placed by convention — tests as SOLID essentially at random depending on
which side of the floor plane floating-point rounding lands on, even
though a real player standing there is completely fine. An early version
of this script used hull 0 and flagged ~24% of ALL loc points solid,
including known-good entity origins (info_player_teamspawn spots) and
100% of the imported real community 2fort5r.loc — the tell that it was
measuring the wrong thing, not that the data was wrong. Hull 1's planes
are already inflated by the player bbox half-extents at compile time, so
a point at floor level correctly reads as empty if a real player fits.

CONTENTS_SOLID under hull 1 means the coordinate is somewhere a player's
bounding box cannot physically fit — a genuine accuracy bug regardless of
loc_status. This does NOT judge whether the NAME is the best possible
name for that spot, only whether the coordinate is real and reachable.

Supports both BSP29 (int16 clipnode fields) and BSP2 (int32 fields) —
the two variants actually present in this repo.
"""
import json
import re
import struct
from pathlib import Path

MAPS_DIR = Path("maps")

CONTENTS_NAMES = {
    -1: "empty", -2: "SOLID", -3: "water", -4: "slime", -5: "lava", -6: "sky",
}

LUMP_PLANES, LUMP_NODES, LUMP_CLIPNODES, LUMP_LEAFS, LUMP_MODELS = 1, 5, 9, 10, 14


def _read_lumps(data):
    lumps = struct.unpack("<30i", data[4:4 + 120])
    return [(lumps[i * 2], lumps[i * 2 + 1]) for i in range(15)]


def _read_planes(data, ofs, length):
    planes = []
    for i in range(length // 20):
        nx, ny, nz, dist, ptype = struct.unpack_from("<ffffi", data, ofs + i * 20)
        planes.append(((nx, ny, nz), dist))
    return planes


def _read_models(data, ofs, length):
    models = []
    for i in range(length // 64):
        vals = struct.unpack_from("<9f4i3i", data, ofs + i * 64)
        headnodes = vals[9:13]
        models.append({"headnode_hull0": headnodes[0], "headnode_hull1": headnodes[1]})
    return models


def _read_clipnodes_bsp29(data, ofs, length):
    nodes = []
    for i in range(length // 8):
        planenum, c0, c1 = struct.unpack_from("<ihh", data, ofs + i * 8)
        nodes.append((planenum, c0, c1))
    return nodes


def _read_clipnodes_bsp2(data, ofs, length):
    nodes = []
    for i in range(length // 12):
        planenum, c0, c1 = struct.unpack_from("<iii", data, ofs + i * 12)
        nodes.append((planenum, c0, c1))
    return nodes


class BspTree:
    def __init__(self, bsp_path):
        data = bsp_path.read_bytes()
        magic = data[0:4]
        if magic == struct.pack("<i", 29):
            variant = "bsp29"
        elif magic == b"BSP2":
            variant = "bsp2"
        else:
            raise ValueError(f"unsupported bsp variant: {magic!r}")

        lumps = _read_lumps(data)
        p_ofs, p_len = lumps[LUMP_PLANES]
        c_ofs, c_len = lumps[LUMP_CLIPNODES]
        m_ofs, m_len = lumps[LUMP_MODELS]

        self.planes = _read_planes(data, p_ofs, p_len)
        self.models = _read_models(data, m_ofs, m_len)
        if variant == "bsp29":
            self.clipnodes = _read_clipnodes_bsp29(data, c_ofs, c_len)
        else:
            self.clipnodes = _read_clipnodes_bsp2(data, c_ofs, c_len)
        self.headnode = self.models[0]["headnode_hull1"]

    def contents_at(self, point):
        """Walk hull 1 (player-box clip hull). Unlike hull 0's NODES+LEAFS,
        a clipnode's negative child IS the content value directly — no
        leaf-array indirection."""
        node = self.headnode
        x, y, z = point
        for _ in range(2048):  # depth guard against a corrupt/cyclic tree
            if node < 0:
                return node  # already a CONTENTS_* value (-1 empty, -2 solid, ...)
            if node >= len(self.clipnodes):
                return -1
            planenum, c0, c1 = self.clipnodes[node]
            normal, dist = self.planes[planenum]
            d = normal[0] * x + normal[1] * y + normal[2] * z - dist
            node = c0 if d >= 0 else c1
        return -1  # depth guard tripped — corrupt tree, don't claim solid


def parse_loc_lines(path):
    """Split on ANY newline convention. A prior version split only on
    \\r\\n and silently mis-parsed any LF-only .loc file (found via this
    same verification pass: 1on1forts.loc uses bare \\n) into one giant
    "line" — not a real accuracy bug, a parsing bug that looked like one."""
    lines = []
    text = path.read_bytes().decode("latin-1")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        try:
            x, y, z = (float(p) for p in parts[:3])
        except ValueError:
            continue
        lines.append(((x, y, z), parts[3]))
    return lines


VERTICAL_SWEEP = (0, 4, 8, 16, 24, 32, 48)


def classify(tree, point):
    """A point solid at its exact Z but empty a little further up is a
    normal Quake convention, not a bug: flags/cap-points/items are
    routinely placed with their origin at the TOP of a pedestal/stand
    brush (confirmed by hand against ff-swoop's real, actively-played
    flag: solid from -16 to +8 relative units, empty from +16 up — the
    same real coordinate the live map uses, not a broken one). Only
    "still solid at every offset up to +48" earns the STUCK verdict —
    that's not explainable by a pedestal, something is actually wrong.
    """
    x, y, z = point
    results = [tree.contents_at((x, y, z + dz)) for dz in VERTICAL_SWEEP]
    if all(c == -2 for c in results):
        return "STUCK"
    if results[0] == -2:
        return "on-pedestal"
    return "open"


def main():
    report = {}
    total_points = 0
    total_stuck = 0
    total_pedestal = 0
    maps_with_stuck = []

    for map_dir in sorted(MAPS_DIR.iterdir()):
        if not map_dir.is_dir():
            continue
        name = map_dir.name
        bsp_path = map_dir / "maps" / f"{name}.bsp"
        loc_path = map_dir / "locs" / f"{name}.loc"
        if not bsp_path.exists() or not loc_path.exists():
            continue

        try:
            tree = BspTree(bsp_path)
        except Exception as e:
            report[name] = {"error": f"bsp parse failed: {e}"}
            continue

        loc_lines = parse_loc_lines(loc_path)
        stuck_hits = []
        pedestal_hits = []
        for point, label in loc_lines:
            verdict = classify(tree, point)
            total_points += 1
            if verdict == "STUCK":
                stuck_hits.append({"point": point, "label": label})
                total_stuck += 1
            elif verdict == "on-pedestal":
                pedestal_hits.append({"point": point, "label": label})
                total_pedestal += 1

        report[name] = {
            "total_locs": len(loc_lines),
            "stuck_count": len(stuck_hits),
            "pedestal_count": len(pedestal_hits),
            "stuck_hits": stuck_hits,
        }
        if stuck_hits:
            maps_with_stuck.append(name)

    json.dump(report, open("data/loc-verification-report.json", "w"), indent=2)

    print(f"Sampled {total_points} loc points across {len(report)} maps.")
    print(f"{total_pedestal} sit on a pedestal/stand (solid at exact Z, opens up within 48u — normal, not a bug).")
    print(f"{total_stuck} are genuinely STUCK (solid at every offset up to +48u) "
          f"across {len(maps_with_stuck)} maps — real accuracy problems.")
    if maps_with_stuck:
        print("\nMaps with at least one genuinely STUCK loc point:")
        for name in maps_with_stuck:
            r = report[name]
            print(f"  {name}: {r['stuck_count']}/{r['total_locs']}")
            for hit in r["stuck_hits"][:5]:
                x, y, z = hit["point"]
                print(f"    ({x:.0f}, {y:.0f}, {z:.0f}) \"{hit['label']}\"")


if __name__ == "__main__":
    main()
