# STATUS — qwtf-live-maps

_Canonical short summary of the working-tree state. Keep this accurate; it
is the next session's starting point._

## Headline (2026-07-18): Phase 1 + phase 2 first pass shipped — public

Built from scratch this session: a community catalog + asset source for
the maps actually played on QWTF Live, distinct from both
`FortressOne/map-repo` (a legacy archive, only ~4/101 overlap with the
real rotation) and `wm-qwtf-maps` (the unrelated procedural map
generator). Public at https://github.com/wmwm/qwtf-live-maps.

**⚠ Note**: minutes after going public, a commit from git identity
`wm <wm@ozfortress.com>` (ozfortress is a real QWTF community org) edited
the live README directly — trimmed an internal doc-path reference. Merged,
not overwritten; `build_metadata.py` no longer regenerates that line. If
this wasn't Tim, worth checking who has push access to the wmwm account.

**In scope**: 105 maps — the union of the Discord `!maps` rotation list
(101 maps) and real match data from logs.qwtf.live, cross-checked against
each other.

**Assets**: 101/105 have a real `.bsp`. 100 harvested from what already
existed locally (`wm-fortressone-source`, `wm-qwtf-client`,
`qwtf-bots-playtest`, `fte-demo-harness`, in that fallback order); 1
(`box4`) sourced from maps.quakeworld.nu's public archive after confirming
an exact filename match (flagged `asset_provenance: external-archive`,
distinct from the workspace-local set — weaker provenance, worth a
playtester's sanity check). 4 are genuine gaps with no asset found
anywhere, including that archive: `elusive`, `fracturex2` (likely a naming
typo for `fracturex`, which IS played and IS present), `h4rdcoremini`,
`nightshacksb5`.

**Levelshots**: 55/105 harvested from `wm-qwtf-client`'s existing capture
pipeline (`tools/build/gen-levelshots.sh`). The other ~50 are capturable
by running that same pipeline — deliberately not run this session (it
spins up disposable game servers; a bigger, separate ask).

**`.loc` files**: 101/101 maps-with-bsp have one.
- 2 imported verbatim from existing community files
  (`FortressOne/map-repo`'s `2fort5r`/`1on1forts`) — `loc_status: community`.
- 25 extracted from the map's OWN author-placed `target_location` entities
  baked into the `.bsp` — a real in-map location system, not a guess
  (`loc_status: author-in-map`, e.g. dragongod2 has 87 named zones like
  "Blue Double Dragon Doors, Lava Side"). Mid-build discovery.
- 74 generated heuristically from spawn/flag/cap-point/resupply entity
  positions PLUS author-placed ambient sound markers (lava pit, swamp,
  wind vent, ...) reused as landmarks — a phase-2 quality pass
  (`loc_status: heuristic-unreviewed` — still flagged honestly, still
  needs a playtester's eyes, just a stronger first draft than pure
  entity-position guessing).

**Cross-reference findings** (real match data vs the static rotation
list): 4 rotation-listed maps show zero real recent matches (`box4`,
`fracturex2`, `nightshacksb5`, `picnics_b3`); 4 maps are actively played
but missing from the rotation list entirely (`castrum2`, `fracturex`,
`wellgl1`, `xpress3`). Both flagged in README. Fixing the rotation list
itself is outside this repo — it's a Discord bot's own data, ownership
unconfirmed, not found anywhere in this workspace to patch directly.

**"Most played" README section**: real logs.qwtf.live match-count ranking
(top 10), zero invented content — the phase-2 answer to "make these maps
special and ours" without fabricating lore.

**Hosting**: GitHub (`wmwm/qwtf-live-maps`, public) is the source of truth
+ PR contribution workflow. `wm-qwtf-site` (playqwtf.com) got a new
`scripts/sync_maps.py`, same off-disk pattern as `sync_downloads.py` —
every download URL points at `raw.githubusercontent.com`. Wired into
`refresh_all.py`, its own tests updated and passing. **Not yet deployed
live** — committed in `wm-qwtf-site` but the live systemd service hasn't
been restarted to pick it up (that repo had other unrelated uncommitted
in-flight changes at the time; a restart deploys everything currently on
disk there, so left as an explicit call for Tim).

**Licensing**: attribution-only, scene convention (Tim's explicit call,
`LICENSE.md`) — `author: unknown` left honest, not guessed, for nearly
every map.

## Explicitly NOT done (assessed, not oversights)

- **Mining real MVD chat text** for community-native loc names — assessed
  feasibility (a sibling read-only project has a text-extraction primitive
  but not position-correlation), concluded it needs real MVD position-frame
  parsing built from scratch plus downloading many real demos from a small
  community site. Scoped as its own future project. See `docs/decisions.md`.
- **Human review pass** on the 74 `heuristic-unreviewed` `.loc` files —
  needs an actual playtester (Tim or the community via PR), can't be done
  by an agent.
- **Running the levelshot capture pipeline** for the ~50 maps without one —
  spins up disposable game servers, a bigger ask than harvesting existing
  files.
- **Per-map custom skins/lore/descriptions** — the deeper "special and
  ours" work. The "most played" ranking is a first, honest step; anything
  beyond real match-data framing risks inventing content.

## Key files

- `docs/superpowers/specs/2026-07-18-qwtf-live-maps-design.md` — the phase 1 design.
- `docs/decisions.md` — 10 logged decisions (6 phase 1, 4 phase 2).
- `scripts/crossref_logs.py`, `harvest_assets.py`, `generate_locs.py`,
  `build_metadata.py`, `validate.py` — the full pipeline, each
  independently re-runnable.
- `data/*.json` — every intermediate result so nothing above is a black box.
