# qwtf-live-maps — phase 1 design (discover & build assets)

Date: 2026-07-18

## Purpose

A community catalog + asset source for the maps actually played on QWTF Live —
distinct from `FortressOne/map-repo` (a legacy dueling-era archive with ~4/101
overlap with the current rotation) and from `wm-qwtf-maps` (the procedural
map *generator* project — unrelated concern).

## Scope (phase 1 only)

In scope: repo scaffold, per-map asset harvesting from what already exists
locally, `.loc` file generation, bracket/metadata organization, a validation
pass producing an honest gap list, and getting the repo public + synced to
playqwtf.com.

Explicitly deferred to phase 2: levelshots/screenshots, mining real MVD
chat text for community-native loc names, and "making each map special and
ours" (lore, custom skins, descriptions).

## Map scope

Union of the Discord `!maps` rotation list (101 unique maps across
2v2/3v3/4v4/5v5 brackets) and real match data from logs.qwtf.live, cross-
checked against each other. Anything played but missing from the static
list, or listed but never actually played, gets flagged for review rather
than silently resolved either way.

## Layout

```
maps/<mapname>/
  map.yml                 # brackets, source, play_count, author, license_note, loc_status
  maps/<mapname>.bsp
  maps/<mapname>.ent       (when present)
  locs/<mapname>.loc
  sound/... progs/...      (when present)
```

Bracket tables (top-level README) are generated from `map.yml`, not
hand-maintained — a map can belong to several brackets without file
duplication.

## Hosting

GitHub (`wmwm/qwtf-live-maps`) is the source of truth + PR contribution
workflow, mirroring the FortressOne/map-repo model. playqwtf.com
(`wm-qwtf-site`) gets a sync step, same shape as its existing
`sync_downloads.py` pattern, to serve actual downloads from the homelab.

## Licensing stance

Attribution-only, scene convention: credit the original map author where
known in `map.yml`, no formal per-map provenance audit. Matches how the
wider QuakeWorld community already treats these maps.

## `.loc` generation

Baseline style pulled from the two rotation maps that already have
community-authored `.loc` files in FortressOne/map-repo (`2fort5r`,
`1on1forts`) — imported verbatim, not regenerated. For the rest: a bsp
entity-lump parser extracts spawns, flag locations, teleporters, and key
items; a heuristic namer produces `.loc` entries in the same style. Each
map's `map.yml` records `loc_status: heuristic-unreviewed` vs
`loc_status: community` so nothing is presented as more authoritative than
it is.

## Done-bar for phase 1

A validation script confirms: every in-scope map has a `.bsp`; every
`.loc` parses; every `map.yml` is schema-valid. Maps missing local assets
are listed explicitly as gaps — never silently dropped or invented.
