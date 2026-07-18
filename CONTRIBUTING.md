# Contributing

## Adding or fixing a map

Each map lives at `maps/<mapname>/`:

```
maps/<mapname>/
  map.yml                  # metadata — brackets, play_count, author, loc_status
  maps/<mapname>.bsp
  maps/<mapname>.ent        (optional)
  locs/<mapname>.loc        (optional but strongly preferred)
  textures/<mapname>/       (optional, only if the map needs custom textures
                              beyond the base FortressOne mod install)
```

sound/ and progs/ are **not** part of a per-map package here — FortressOne
ships one shared mod-wide set to every server and client, so there's nothing
map-specific to bundle for those (unlike the older `FortressOne/map-repo`
archive convention, which predates the unified mod distribution).

1. Fork this repo.
2. Add or fix files under `maps/<mapname>/` following the layout above.
3. If you're correcting a heuristic `.loc` file, update `map.yml`'s
   `loc_status` to `community` once it's genuinely hand-reviewed.
4. Run `python3 scripts/validate.py` before opening a PR — it checks every
   `.bsp` parses, every `.loc` is well-formed, and every `map.yml` has the
   required fields.
5. Submit a pull request.

## `.loc` file format

Plain text, one location per line: `X Y Z name`, coordinates in map units.
Keep names short and lowercase, matching how players actually call them out
in team chat (see `maps/2fort5r/locs/2fort5r.loc` for the community-authored
reference style).

## Regenerating the derived files

`README.md` and every `map.yml` are generated from `data/*.json` — don't
hand-edit the bracket tables in `README.md` directly, they'll be
overwritten. To regenerate after changing `data/rotation.json` or
re-running the crossref/harvest/loc scripts:

```
python3 scripts/build_metadata.py
```
