# QWTF Live Map Repo

Community catalog + asset source for the maps actually played on QWTF Live.
Not an archive of every map ever made for QuakeWorld Team Fortress —
scoped to the current competitive rotation and what real matches show
people actually playing, cross-checked against [logs.qwtf.live](https://logs.qwtf.live/).

## Most played, by real match count

Not a vibe, actual logs.qwtf.live match history at the time this was last generated:

1. **`ff-phantomr`** — 398 matches (3v3/4v4)
2. **`ff-schtop`** — 355 matches (4v4/5v5)
3. **`ff-destroy3`** — 343 matches (3v3/4v4/5v5)
4. **`japanc`** — 340 matches (3v3/4v4)
5. **`rs_zzr`** — 320 matches (3v3/4v4)
6. **`openfirer`** — 317 matches (4v4/5v5)
7. **`ff-swoop`** — 217 matches (4v4)
8. **`h5rdcore_b2`** — 180 matches (3v3/4v4)
9. **`blitzkrieg2`** — 171 matches (2v2/3v3/4v4/5v5)
10. **`egypt3`** — 125 matches (2v2/3v3)

## Map status legend

- **loc status**: `author-in-map` (extracted from the map's own built-in location entities — highest confidence), `community` (hand-authored, imported from the wider QW scene), `heuristic-unreviewed` (auto-generated from spawn/flag/item positions plus author-placed ambient sound markers, needs a playtester's eyes), `missing`.
- **assets**: `+shot` means a levelshot exists at `textures/levelshots/<name>.png`.

**Levelshots**: 55/105 maps have one, harvested from `wm-qwtf-client`'s existing capture pipeline (`tools/build/gen-levelshots.sh` — a disposable server + spectator client + Xvfb framebuffer grab, camera positioned from the map's own spawn entities). Re-running that pipeline to fill the rest is a real, larger undertaking (spins up disposable game servers) not attempted in this pass.

**Loc accuracy**: every `.loc` coordinate is checked against the map's own hull-1 (player-collision) geometry via `scripts/verify_locs.py` — not just "does the file parse," but "can a player actually stand there." 69/1887 points across 16 maps are genuinely stuck in solid geometry at every offset up to 48 units (most "solid at the exact coordinate" hits are normal — flags/cap points routinely sit at pedestal-top height, confirmed against a real, actively-played map). Flagged for a closer look, not claimed fixed: `2farms`, `dragongod2`, `etf_miniheros`, `excel3`, `fo-spiderx`, `japanc`, `lotus_b4`, `nightwatch2`, `quartz_b1`, `r123`, `sanctuary_b9`, `smap47`, `snowlake_b7`, `spring_b4`, `substation_b2`, `volcanic`.

## 2v2

| Map | Matches (logs.qwtf.live) | Assets | Loc status |
|---|---|---|---|
| `blitzkrieg2` | 171 | bsp+ent+tex+shot | heuristic-unreviewed |
| `egypt3` | 125 | bsp+ent+shot | heuristic-unreviewed |
| `genders2` | 63 | bsp+ent+tex+shot | heuristic-unreviewed |
| `poop` | 52 | bsp+ent+tex+shot | heuristic-unreviewed |
| `nbases_b1` | 47 | bsp+shot | heuristic-unreviewed |
| `5speed5` | 34 | bsp+ent+shot | heuristic-unreviewed |
| `dragongod2` | 33 | bsp+shot | author-in-map |
| `rs_zz1` | 27 | bsp+ent+shot | heuristic-unreviewed |
| `desperat` | 26 | bsp+ent+tex+shot | heuristic-unreviewed |
| `preskool` | 25 | bsp+ent+tex+shot | heuristic-unreviewed |
| `2farms` | 23 | bsp+ent+shot | heuristic-unreviewed |
| `mountdoom` | 22 | bsp | author-in-map |
| `qu4d` | 20 | bsp+ent+shot | heuristic-unreviewed |
| `etf_miniheros` | 17 | bsp+tex+shot | heuristic-unreviewed |
| `ftactic1` | 17 | bsp+ent+shot | heuristic-unreviewed |
| `optics6` | 17 | bsp+shot | heuristic-unreviewed |
| `etf_egypt` | 14 | bsp+tex+shot | heuristic-unreviewed |
| `2fort5r` | 13 | bsp+shot | heuristic-unreviewed |
| `castlemania_b2` | 12 | bsp | heuristic-unreviewed |
| `etf_xpress` | 12 | bsp+tex+shot | heuristic-unreviewed |
| `1on1forts` | 10 | bsp | heuristic-unreviewed |
| `lostfortress` | 10 | bsp+shot | heuristic-unreviewed |
| `cyclonr` | 9 | bsp+tex+shot | author-in-map |
| `egypt` | 9 | bsp | heuristic-unreviewed |
| `noad2` | 9 | bsp+shot | heuristic-unreviewed |
| `wc3` | 9 | bsp+shot | heuristic-unreviewed |
| `well6mini` | 9 | bsp+shot | author-in-map |
| `disorder` | 8 | bsp | heuristic-unreviewed |
| `drgnfyr2` | 8 | bsp | heuristic-unreviewed |
| `ins3` | 8 | bsp | heuristic-unreviewed |
| `lotus_b4` | 8 | bsp | author-in-map |
| `alchemy` | 7 | bsp+shot | heuristic-unreviewed |
| `substation_b2` | 7 | bsp | author-in-map |
| `fo_labs_b7` | 6 | bsp | heuristic-unreviewed |
| `h4rdcoremini` | 6 | **missing** | missing |
| `vertex1r` | 6 | bsp+shot | heuristic-unreviewed |
| `r123` | 5 | bsp | heuristic-unreviewed |
| `8-1` | 4 | bsp+shot | heuristic-unreviewed |
| `smap47` | 4 | bsp+shot | heuristic-unreviewed |
| `sunnyramps` | 4 | bsp | heuristic-unreviewed |
| `spyder` | 3 | bsp | heuristic-unreviewed |
| `volcanic` | 3 | bsp | heuristic-unreviewed |
| `2machr` | 2 | bsp | heuristic-unreviewed |
| `marics_ctf1` | 2 | bsp | heuristic-unreviewed |
| `neenf` | 2 | bsp | heuristic-unreviewed |
| `utumno_b3` | 2 | bsp | heuristic-unreviewed |

## 3v3

| Map | Matches (logs.qwtf.live) | Assets | Loc status |
|---|---|---|---|
| `ff-phantomr` | 398 | bsp+tex+shot | heuristic-unreviewed |
| `ff-destroy3` | 343 | bsp+tex+shot | heuristic-unreviewed |
| `japanc` | 340 | bsp+tex+shot | heuristic-unreviewed |
| `rs_zzr` | 320 | bsp+shot | heuristic-unreviewed |
| `h5rdcore_b2` | 180 | bsp+ent+tex+shot | heuristic-unreviewed |
| `blitzkrieg2` | 171 | bsp+ent+tex+shot | heuristic-unreviewed |
| `egypt3` | 125 | bsp+ent+shot | heuristic-unreviewed |
| `genders2` | 63 | bsp+ent+tex+shot | heuristic-unreviewed |
| `ff-siege` | 60 | bsp+ent+shot | heuristic-unreviewed |
| `nbases_b1` | 47 | bsp+shot | heuristic-unreviewed |
| `dragongod2` | 33 | bsp+shot | author-in-map |
| `3way2` | 26 | bsp | heuristic-unreviewed |
| `japk` | 26 | bsp+ent+shot | heuristic-unreviewed |
| `middleskool` | 22 | bsp+ent+shot | author-in-map |
| `god_well` | 13 | bsp+tex+shot | heuristic-unreviewed |
| `nightwatch2` | 9 | bsp | author-in-map |
| `drgnfyr2` | 8 | bsp | heuristic-unreviewed |
| `haste` | 7 | bsp | heuristic-unreviewed |
| `cyanr` | 6 | bsp | heuristic-unreviewed |
| `minitf2k` | 6 | bsp | heuristic-unreviewed |
| `rmanor_b6` | 6 | bsp+shot | author-in-map |
| `caverns` | 5 | bsp | heuristic-unreviewed |
| `42smooth` | 4 | bsp | heuristic-unreviewed |
| `beyonddarkness` | 4 | bsp+shot | heuristic-unreviewed |
| `2night3_b1` | 3 | bsp | heuristic-unreviewed |
| `echo_b1` | 3 | bsp+shot | author-in-map |
| `snowlake_b7` | 3 | bsp | author-in-map |
| `bastion` | 2 | bsp | heuristic-unreviewed |
| `shank76` | 2 | bsp | heuristic-unreviewed |
| `anaconda` | 1 | bsp | heuristic-unreviewed |
| `elusive` | 1 | **missing** | missing |
| `qbase1_b3` | 1 | bsp | author-in-map |
| `sanctuary_b9` | 1 | bsp | author-in-map |
| `spring_b4` | 1 | bsp | author-in-map |
| `vengeance2` | 1 | bsp+tex+shot | author-in-map |
| `box4` | 0 | bsp | heuristic-unreviewed |
| `nightshacksb5` | 0 | **missing** | missing |

## 4v4

| Map | Matches (logs.qwtf.live) | Assets | Loc status |
|---|---|---|---|
| `ff-phantomr` | 398 | bsp+tex+shot | heuristic-unreviewed |
| `ff-schtop` | 355 | bsp+tex+shot | heuristic-unreviewed |
| `ff-destroy3` | 343 | bsp+tex+shot | heuristic-unreviewed |
| `japanc` | 340 | bsp+tex+shot | heuristic-unreviewed |
| `rs_zzr` | 320 | bsp+shot | heuristic-unreviewed |
| `openfirer` | 317 | bsp+shot | heuristic-unreviewed |
| `ff-swoop` | 217 | bsp+ent+tex+shot | heuristic-unreviewed |
| `h5rdcore_b2` | 180 | bsp+ent+tex+shot | heuristic-unreviewed |
| `blitzkrieg2` | 171 | bsp+ent+tex+shot | heuristic-unreviewed |
| `pineapple_b3` | 100 | bsp+shot | heuristic-unreviewed |
| `turtler` | 87 | bsp+ent+tex+shot | heuristic-unreviewed |
| `tfc-demolish_b2` | 59 | bsp+shot | heuristic-unreviewed |
| `ff-shoop` | 34 | bsp | heuristic-unreviewed |
| `dragongod2` | 33 | bsp+shot | author-in-map |
| `ff-mortality` | 26 | bsp+tex+shot | author-in-map |
| `turbo` | 26 | bsp+ent+shot | heuristic-unreviewed |
| `tf2day_b2` | 21 | bsp+tex+shot | heuristic-unreviewed |
| `ff-aardvark` | 15 | bsp+ent+shot | heuristic-unreviewed |
| `canal_b7` | 13 | bsp | author-in-map |
| `ff-2fort` | 13 | bsp+tex+shot | author-in-map |
| `god_well` | 13 | bsp+tex+shot | heuristic-unreviewed |
| `excel3` | 11 | bsp | author-in-map |
| `fo-spiderx` | 8 | bsp | author-in-map |
| `nbases_b2` | 7 | bsp+shot | heuristic-unreviewed |
| `42smooth` | 4 | bsp | heuristic-unreviewed |
| `ff-ibex` | 1 | bsp | heuristic-unreviewed |
| `fracturex2` | 0 | **missing** | missing |

## 5v5

| Map | Matches (logs.qwtf.live) | Assets | Loc status |
|---|---|---|---|
| `ff-schtop` | 355 | bsp+tex+shot | heuristic-unreviewed |
| `ff-destroy3` | 343 | bsp+tex+shot | heuristic-unreviewed |
| `openfirer` | 317 | bsp+shot | heuristic-unreviewed |
| `blitzkrieg2` | 171 | bsp+ent+tex+shot | heuristic-unreviewed |
| `ff-mortality` | 26 | bsp+tex+shot | author-in-map |
| `ff-aardvark` | 15 | bsp+ent+shot | heuristic-unreviewed |
| `fo_smartbases_b2` | 11 | bsp | author-in-map |
| `fo-spiderx` | 8 | bsp | author-in-map |
| `etf-bigzag_b1` | 7 | bsp | heuristic-unreviewed |
| `ff-raiden` | 4 | bsp | heuristic-unreviewed |
| `impactr` | 2 | bsp | heuristic-unreviewed |
| `ff-ibex` | 1 | bsp | heuristic-unreviewed |
| `quartz_b1` | 1 | bsp | author-in-map |
| `picnics_b3` | 0 | bsp | author-in-map |

## Played but not in the static rotation list

Found via real match data on logs.qwtf.live, not the Discord `!maps` output — flagged here for a human call on whether the rotation list itself is stale.

- `castrum2` — 1 matches, assets: yes
- `fracturex` — 1 matches, assets: yes
- `wellgl1` — 2 matches, assets: yes
- `xpress3` — 5 matches, assets: yes

## Sourced from an external archive, not this workspace

Not present in any local copy — pulled from [maps.quakeworld.nu](https://maps.quakeworld.nu/all/)'s public map archive after confirming an exact filename match. Flagged separately from workspace-local assets since that provenance is weaker (not verified byte-identical to whatever QWTF Live's own servers actually run) — worth a playtester's sanity check before treating as equivalent.

- `box4`

## Gaps — no asset found anywhere, including public archives

These are in scope but no `.bsp` exists in this workspace, and a check against maps.quakeworld.nu's own "every known QuakeWorld map" archive came up empty too. Not invented, not silently dropped — genuinely need sourcing from wherever QWTF Live's own servers get them.

- `elusive`
- `fracturex2`
- `h4rdcoremini`
- `nightshacksb5`

