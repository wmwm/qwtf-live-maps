# STATUS — qwtf-live-maps

_Canonical short summary of the working-tree state. Keep this accurate; it
is the next session's starting point._

## Headline (2026-07-18): Phase 1 shipped — public, 100/105 maps have real assets

Built from scratch this session: a community catalog + asset source for
the maps actually played on QWTF Live, distinct from both
`FortressOne/map-repo` (a legacy archive, only ~4/101 overlap with the
real rotation) and `wm-qwtf-maps` (the unrelated procedural map
generator). Public at https://github.com/wmwm/qwtf-live-maps.

**In scope**: 105 maps — the union of the Discord `!maps` rotation list
(101 maps) and real match data from logs.qwtf.live, cross-checked against
each other.

**Assets**: 100/105 have a real `.bsp` harvested from what already existed
locally (`wm-fortressone-source`, `wm-qwtf-client`, `qwtf-bots-playtest`,
`fte-demo-harness`, in that fallback order). 5 are genuine gaps with no
local asset anywhere in the workspace: `box4`, `elusive`, `fracturex2`
(likely a naming typo for `fracturex`, which IS played and IS present),
`h4rdcoremini`, `nightshacksb5` — listed in README, not invented.

**`.loc` files**: 100/100 maps-with-bsp have one.
- 2 imported verbatim from existing community files
  (`FortressOne/map-repo`'s `2fort5r`/`1on1forts`) — `loc_status: community`.
- 25 extracted from the map's OWN author-placed `target_location` entities
  baked into the `.bsp` — a real in-map location system, not a guess
  (`loc_status: author-in-map`, e.g. dragongod2 has 87 named zones like
  "Blue Double Dragon Doors, Lava Side"). This was a mid-build discovery,
  not something we knew to look for going in.
- 73 generated heuristically from spawn/flag/cap-point/resupply entity
  positions (`loc_status: heuristic-unreviewed` — flagged honestly, needs
  a playtester's eyes before being treated as authoritative).

**Cross-reference findings** (real match data vs the static rotation
list): 4 rotation-listed maps show zero real recent matches (`box4`,
`fracturex2`, `nightshacksb5`, `picnics_b3`); 4 maps are actively played
but missing from the rotation list entirely (`castrum2`, `fracturex`,
`wellgl1`, `xpress3`). Both flagged in README for a human call on whether
the rotation list itself is stale.

**Hosting**: GitHub (`wmwm/qwtf-live-maps`, public) is the source of truth
+ PR contribution workflow. `wm-qwtf-site` (playqwtf.com) got a new
`scripts/sync_maps.py`, same off-disk pattern as `sync_downloads.py` —
every download URL points at `raw.githubusercontent.com`, this repo never
serves map binaries from the residential box. Wired into `refresh_all.py`,
its own tests updated and passing. **Not yet deployed live** — the code is
committed in `wm-qwtf-site` but the live systemd service hasn't been
restarted to pick it up (that repo had other unrelated uncommitted
in-flight changes at the time; a restart deploys everything currently on
disk there, so left as an explicit call for Tim rather than bundled in).

**Licensing**: attribution-only, scene convention (Tim's explicit call,
`LICENSE.md`) — `author: unknown` left honest, not guessed, for nearly
every map.

## Next (phase 2, explicitly deferred, not started)

- Levelshots/screenshots per map.
- Mining real MVD chat text from logs.qwtf.live for community-native loc
  names on the 73 heuristic maps (an idea raised but not pursued this
  session — could sharpen the heuristic set considerably).
- "Making each map special and ours" — lore, custom skins, descriptions.
- A human review pass on the 73 `heuristic-unreviewed` `.loc` files.
- Sourcing the 5 genuinely missing maps.
- Deciding what to do with the `fracturex2`/`fracturex` likely-typo and
  the 4 unlisted-but-played maps (probably: fix the Discord rotation list
  itself — that's outside this repo).

## Key files

- `docs/superpowers/specs/2026-07-18-qwtf-live-maps-design.md` — the phase 1 design.
- `docs/decisions.md` — 6 logged decisions from this build.
- `scripts/crossref_logs.py`, `harvest_assets.py`, `generate_locs.py`,
  `build_metadata.py`, `validate.py` — the full phase 1 pipeline, each
  independently re-runnable.
- `data/*.json` — every intermediate result (rotation list, crossref,
  harvest report, loc-generation report, final per-map metadata) so
  nothing above is a black box.
