# Changelog

All notable changes to this repo. Dated entries (no version numbers yet).

## 2026-07-18

### Added

- Initial public release: a catalog + asset source for the maps actually
  played on QWTF Live — scoped to the real 2v2/3v3/4v4/5v5 competitive
  rotation plus real match history from [logs.qwtf.live](https://logs.qwtf.live/),
  not a full historical archive of every QWTF map ever made.
- `.loc` (team-chat location callout) files for 101 maps. Some come from
  a map's own built-in location data, some are imported from established
  community files, the rest are generated from each map's geometry —
  every map's `map.yml` records which.
- Levelshot preview images for 55 maps.
- A "most played" ranking on the front page, drawn from real match counts.
- `box4`, sourced from the public maps.quakeworld.nu archive (flagged
  separately in `map.yml` — not yet verified against this repo's other
  workspace-local maps).

### Fixed

- `blitzkrieg2`'s "red spawn" location sat inside solid floor geometry —
  averaging spawn points across two separate floor levels produced a bad
  coordinate. Location generation now always uses a real spawn position,
  never a computed average.
- `2fort5r` and `1on1forts`'s previously-imported location files were for
  a different, larger map that happened to share the filename —
  regenerated from the maps actually shipped in this repo.
- Every location file's coordinates are now checked against the map's
  own collision data. 16 maps have a small number of locations flagged
  for a closer look (see each map's `map.yml` and the README).

### Known gaps

- `elusive`, `fracturex2`, `h4rdcoremini`, `nightshacksb5` have no map
  file yet — genuinely missing, not present in any archive checked so far.
- About 50 maps still need a levelshot preview image.
- ~74 maps' location files are auto-generated and haven't had a human
  playtester's review yet (`loc_status: heuristic-unreviewed` in `map.yml`).

Contributions on any of the above are welcome — see `CONTRIBUTING.md`.
