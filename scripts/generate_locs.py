#!/usr/bin/env python3
"""Heuristic .loc generator: parse each bsp's ENTITIES lump (classic
TeamFortress/QWTF QuakeC entity schema: info_player_teamspawn, item_tfgoal,
info_tfgoal, teleporters) and emit .loc entries in the same style as the
two existing community files we imported (2fort5r, 1on1forts): plain
"X Y Z name" lines, CRLF endings, short lowercase phrases.

This is a heuristic first pass, not hand-authored — every map it touches
gets loc_status: heuristic-unreviewed in map.yml (set by build_metadata.py).
Maps with an already-imported community .loc (2fort5r, 1on1forts) are
skipped entirely; never overwrite a real one.
"""
import json
import re
import struct
from pathlib import Path

MAPS_DIR = Path("maps")
SKIP = {"2fort5r", "1on1forts"}  # already have real community .loc files
CLUSTER_THRESHOLD = 650.0


def parse_entities(bsp_path):
    data = bsp_path.read_bytes()
    # BSP29 starts with int32 version=29; BSP2/2PSB start with an ASCII magic
    # tag of the same 4-byte width. Either way the lump directory that
    # follows (15 lumps of int32 offset+length; entities is lump 0) has the
    # identical layout — only vertex/face/leaf lump internals differ between
    # variants, which we don't touch here.
    if data[0:4] not in (struct.pack("<i", 29), b"BSP2", b"2PSB"):
        return None  # genuinely unknown format, don't guess
    _, ent_ofs, ent_len = struct.unpack("<iii", data[0:12])
    text = data[ent_ofs:ent_ofs + ent_len].decode("latin-1")
    blocks = re.findall(r"\{([^{}]*)\}", text, re.S)
    ents = []
    for b in blocks:
        kv = dict(re.findall(r'"([^"]+)"\s*"((?:[^"\\]|\\.)*)"', b))
        if kv:
            ents.append(kv)
    return ents


# A handful of older maps abbreviate classname values (not keys) to save
# space in the compiled entity lump; same schema underneath.
CLASSNAME_ALIASES = {
    "i_t_g": "info_tfgoal",
    "i_p_t": "info_player_teamspawn",
}


def normalize_entities(ents):
    for e in ents:
        cn = e.get("classname")
        if cn in CLASSNAME_ALIASES:
            e["classname"] = CLASSNAME_ALIASES[cn]
        # Quake's console font renders high-bit bytes as gold-colored text —
        # some maps store display strings (netname) with every byte OR'd by
        # 0x80 for that effect. Un-mask so labels read as plain text; for
        # already-plain ASCII this round-trips to itself.
        if "netname" in e:
            e["netname"] = "".join(chr(ord(c) & 0x7F) for c in e["netname"])
    return ents


def origin_of(ent):
    try:
        x, y, z = (float(v) for v in ent["origin"].split())
        return (x, y, z)
    except (KeyError, ValueError):
        return None


def dist(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def cluster_points(points, threshold=CLUSTER_THRESHOLD):
    n = len(points)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i in range(n):
        for j in range(i + 1, n):
            if dist(points[i], points[j]) < threshold:
                union(i, j)

    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(points[i])
    clusters = list(groups.values())
    clusters.sort(key=lambda c: -len(c))
    return clusters


def centroid(points):
    n = len(points)
    return tuple(round(sum(p[i] for p in points) / n) for i in range(3))


COLOR_CODE_RE = re.compile(r"\^[0-9*]")


def clean_label(s):
    return COLOR_CODE_RE.sub("", s).strip()


def extract_author_target_locations(ents):
    """Some maps ship their own target_location entities — a real in-map
    location system the original author placed (grouped, dense clusters of
    the same name covering a walkable area). Where present, this is a much
    higher-confidence source than anything we could heuristically guess."""
    by_name = {}
    for e in ents:
        if e.get("classname") != "target_location":
            continue
        o = origin_of(e)
        name = clean_label(e.get("message", ""))
        if o and name:
            by_name.setdefault(name, []).append(o)
    lines = []
    for name, pts in by_name.items():
        for cl in cluster_points(pts, threshold=CLUSTER_THRESHOLD):
            lines.append((centroid(cl), name))
    return lines


def team_colors_from_flags(ents):
    colors = {}
    for e in ents:
        if e.get("classname") == "item_tfgoal":
            netname = e.get("netname", "")
            m = re.match(r"(red|blue)", netname, re.I)
            team_no = e.get("team_no")
            if m and team_no:
                colors[team_no] = m.group(1).lower()
    return colors


# Author-placed ambient sound markers have no name field, but the
# classname itself is a real signal — the mapper put a lava-pit sound
# there because there's an actual lava pit there. Translating these to
# plain labels is still a judgment call (hence still "heuristic"), but
# it's grounded in something the author actually placed, not a guess from
# spawn/flag geometry alone.
AMBIENT_LABELS = {
    "ambient_suck_wind": "wind vent",
    "ambient_drip": "dripping water",
    "ambient_lavapit": "lava pit",
    "ambient_swamp1": "swamp",
    "ambient_peakwind": "windy peak",
    "ambient_comp_hum": "computer room",
    "ambient_flouro_buzz": "flickering light",
    "ambient_light_buzz": "flickering light",
    "ambient_brook": "brook",
}


def extract_ambient_landmarks(ents):
    by_label = {}
    for e in ents:
        label = AMBIENT_LABELS.get(e.get("classname"))
        if not label:
            continue
        o = origin_of(e)
        if o:
            by_label.setdefault(label, []).append(o)
    lines = []
    for label, pts in by_label.items():
        for cl in cluster_points(pts, threshold=CLUSTER_THRESHOLD):
            lines.append((centroid(cl), label))
    return lines


def generate_locs(name, ents):
    lines = []
    team_colors = team_colors_from_flags(ents)

    def color_for(team_no):
        return team_colors.get(team_no, f"team{team_no}")

    # spawns, clustered per team
    for team_no in sorted({e.get("team_no") for e in ents
                           if e.get("classname") == "info_player_teamspawn" and e.get("team_no")}):
        pts = [origin_of(e) for e in ents
               if e.get("classname") == "info_player_teamspawn" and e.get("team_no") == team_no]
        pts = [p for p in pts if p]
        for i, cl in enumerate(cluster_points(pts), 1):
            label = f"{color_for(team_no)} spawn" + (f" {i}" if i > 1 else "")
            lines.append((centroid(cl), label))

    # flags
    for e in ents:
        if e.get("classname") == "item_tfgoal" and "flag" in e.get("netname", "").lower():
            o = origin_of(e)
            if o:
                lines.append((o, e["netname"].lower()))

    # cap points
    for e in ents:
        if e.get("classname") == "info_tfgoal" and "cap" in e.get("netname", "").lower():
            o = origin_of(e)
            if o:
                lines.append((o, e["netname"].lower()))

    # resupply clusters (ammo/health/armor), attributed to nearest spawn's team color when close enough
    resupply_classes = {"item_armorInv", "item_health", "item_cells", "item_shells",
                         "item_rockets", "item_spikes", "item_armor1", "item_armor2"}
    resupply_pts = [origin_of(e) for e in ents if e.get("classname") in resupply_classes]
    resupply_pts = [p for p in resupply_pts if p]
    spawn_centroids = [(pt, lbl) for pt, lbl in lines if "spawn" in lbl]
    for i, cl in enumerate(cluster_points(resupply_pts), 1):
        if len(cl) < 2:
            continue  # a single stray pickup isn't a "location"
        c = centroid(cl)
        nearest = min(spawn_centroids, key=lambda sl: dist(sl[0], c), default=None)
        if nearest and dist(nearest[0], c) < 1200:
            team_label = nearest[1].split(" spawn")[0]
            label = f"{team_label} resupply"
        else:
            label = f"resupply {i}"
        lines.append((c, label))

    # teleporter destinations
    dests = [e for e in ents if e.get("classname") == "info_teleport_destination"]
    for i, e in enumerate(dests, 1):
        o = origin_of(e)
        if o:
            lines.append((o, "teleporter" + (f" {i}" if len(dests) > 1 else "")))

    # thematic ambient-sound markers (lava pit, swamp, wind vent, ...)
    lines.extend(extract_ambient_landmarks(ents))

    return lines


def dedupe_lines(lines):
    """Drop exact (rounded-coordinate, name) duplicates that can arise when
    a point is legitimately reachable from more than one extraction path.
    Deliberately keeps distinct names at similar coordinates — a real map
    can have two meaningfully different callouts a few units apart."""
    seen = set()
    out = []
    for (x, y, z), name in lines:
        key = (int(x), int(y), int(z), name)
        if key in seen:
            continue
        seen.add(key)
        out.append(((x, y, z), name))
    return out


def write_loc_file(path, lines):
    with open(path, "wb") as f:
        for (x, y, z), name in dedupe_lines(lines):
            f.write(f"{int(x)} {int(y)} {int(z)} {name}\r\n".encode("latin-1"))


def main():
    sources = {}  # mapname -> "author-in-map" | "heuristic"
    no_bsp, unparseable, zero = [], [], []
    for map_dir in sorted(MAPS_DIR.iterdir()):
        name = map_dir.name
        if name in SKIP:
            continue
        bsp_path = map_dir / "maps" / f"{name}.bsp"
        if not bsp_path.exists():
            no_bsp.append(name)
            continue
        ents = parse_entities(bsp_path)
        if ents is None:
            unparseable.append(name)
            continue
        ents = normalize_entities(ents)

        lines = extract_author_target_locations(ents)
        source = "author-in-map"
        if not lines:
            lines = generate_locs(name, ents)
            source = "heuristic"
        if not lines:
            zero.append(name)
            continue

        loc_dir = map_dir / "locs"
        loc_dir.mkdir(exist_ok=True)
        write_loc_file(loc_dir / f"{name}.loc", lines)
        sources[name] = {"source": source, "count": len(lines)}

    author_count = sum(1 for v in sources.values() if v["source"] == "author-in-map")
    heuristic_count = sum(1 for v in sources.values() if v["source"] == "heuristic")
    print(f"Generated .loc for {len(sources)} maps "
          f"({author_count} from author-placed target_location entities, "
          f"{heuristic_count} heuristic)")
    print(f"Skipped (already have community .loc): {sorted(SKIP)}")
    print(f"No bsp (can't generate): {no_bsp}")
    if unparseable:
        print(f"Unparseable bsp version: {unparseable}")
    if zero:
        print(f"No loc entries found at all (no matching entities): {zero}")

    json.dump({"sources": sources, "skipped_has_community_loc": sorted(SKIP),
               "no_bsp": no_bsp, "unparseable": unparseable, "zero_entries": zero},
              open("data/loc-generation-report.json", "w"), indent=2)


if __name__ == "__main__":
    main()
