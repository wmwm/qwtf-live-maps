# Decisions

## 2026-07-18  loc-generation  Decision: use author-placed `target_location` entities where present, before falling back to heuristics

Context:
  While building the .loc generation pipeline (entity-lump parsing for
  spawns/flags/cap points), discovered that 24 of the ~100 in-scope maps
  ship their own `target_location` entities baked directly into the .bsp —
  a real in-map location system the original author placed, not something
  we're inferring. Some are extremely detailed (dragongod2 has 87 named
  zones like "Blue Double Dragon Doors, Lava Side"; well6mini has 57).

Options:
  A. Pure geometry/entity-position heuristic for every map, ignore
     target_location entities: simpler pipeline, but throws away
     genuinely author-authored data sitting right there in the file.
  B. Use target_location where present (grouped by name, clustered by
     proximity, emitted as .loc lines), heuristic fallback only for maps
     that lack them.
  C. Full geometry/room clustering from scratch (BSP leaf/visibility
     analysis) for every map: highest theoretical quality, much larger
     scope, not achievable in phase 1's time budget.

Chosen: B

Reason:
  Matches Tim's explicit steer ("look at the current loc files and go from
  there") extended to a source we hadn't known existed until mid-build.
  Costs nothing extra to check for target_location first, and produces
  clearly higher-confidence output for the 24 maps that have it.

Reversibility:
  Easy. map.yml's `loc_status` field (`author-in-map` vs
  `heuristic-unreviewed` vs `community`) means nothing is presented as more
  authoritative than it is — any map's .loc can be regenerated or
  hand-replaced independently.

---

## 2026-07-18  asset-scope  Decision: sound/progs are not per-map assets in this repo

Context:
  FortressOne/map-repo's archive convention bundles bespoke per-map
  sound/progs (individual community map submissions historically shipped
  their own custom sounds/models). Checking the real asset sources for our
  rotation (wm-fortressone-source, a full FortressOne mod install) showed
  sound/progs are one shared, mod-wide set delivered to every server and
  client — not a per-map concern for the maps actually in our scope.

Options:
  A. Replicate the archive's per-map sound/progs folder convention anyway,
     for structural consistency with FortressOne/map-repo.
  B. Skip per-map sound/progs entirely; document the reasoning so it
     doesn't read as an oversight to a future contributor.

Chosen: B

Reason:
  Bundling shared mod-wide files under every map's folder would be
  hundreds of duplicate copies of the same assets, and doesn't reflect how
  the modern FortressOne distribution actually works.

Reversibility:
  Easy to add later if a specific map turns out to need bespoke custom
  sound/models (the CONTRIBUTING.md layout already reserves the option).

---

## 2026-07-18  licensing  Decision: attribution-only, scene convention

Context:
  Map assets here are third-party community content (many different
  authors, no rights held by this repo). This workspace has prior history
  of asset-provenance sensitivity (wm-qwtf-client's retail-Quake/TF2.8
  audit). Asked Tim directly given that history.

Options:
  A. Full per-map provenance audit before inclusion, same rigor as the
     wm-qwtf-client audit — airtight, but far too slow for ~100 maps.
  B. Attribution-only, scene convention: credit known authors, no formal
     enforcement, matches how the wider QW community already treats these
     maps (and how FortressOne/map-repo itself operates).
  C. Defer — flag the risk, ship without a policy.

Chosen: B (Tim's explicit call)

Reason:
  Matches long-standing scene norms; this repo doesn't claim ownership
  anywhere, and `author: unknown` is left honest rather than guessed.

Reversibility:
  Moderate — a real audit is still doable later if this repo becomes more
  official/high-profile, since nothing here claims rights it doesn't have.

---

## 2026-07-18  map-scope  Decision: union of Discord rotation list and logs.qwtf.live real match data

Context:
  "Complete and relevant" needed a concrete definition. The Discord `!maps`
  output is a static, hand-maintained rotation list (101 unique maps
  across 2v2/3v3/4v4/5v5). logs.qwtf.live is a real match-log site with
  per-map filtering — a much better "what's actually played" signal.

Options:
  A. Rotation list only — simple, already bracket-organized, but static
     and possibly stale.
  B. logs.qwtf.live real match data only — reflects reality, but loses the
     bracket categorization the rotation list already encodes.
  C. Union of both, rotation list as primary, cross-checked against real
     match data.

Chosen: C (Tim's explicit call)

Reason:
  Cross-checking surfaced real discrepancies worth knowing about: 4
  rotation-listed maps with zero real recent matches (box4, fracturex2,
  nightshacksb5, picnics_b3 — fracturex2 looks like a naming typo for
  "fracturex", which IS played) and 4 maps played but missing from the
  rotation list entirely (castrum2, fracturex, wellgl1, xpress3). Flagged
  in README rather than silently resolved either way.

Reversibility:
  Easy — `data/rotation.json` and `data/logs-crossref.json` are
  regeneratable inputs, not hardcoded into the repo structure.

---

## 2026-07-18  repo-organization  Decision: metadata-driven bracket tables, not per-bracket folder duplication

Context:
  Many maps belong to multiple team-size brackets (blitzkrieg2 is in all
  of 2v2/3v3/4v4/5v5; dragongod2 in three). A raw copy of the Discord
  rotation dump would require either duplicating files across bracket
  folders or symlinking them.

Options:
  A. Physically sort each map into `2v2/`, `3v3/`, etc. folders (copies or
     symlinks) — mirrors the Discord output structure directly, but one
     map = N copies/links.
  B. One directory per map (`maps/<name>/`), with brackets recorded in
     `map.yml`; bracket tables in the top-level README generated from that
     metadata.

Chosen: B

Reason:
  One source of truth per map. Matches the "community catalog + asset
  source" purpose Tim specified — the repo needs a single canonical home
  per map either way, and generated tables read better than needing to
  cross-reference multiple folders to see a map's full asset set.

Reversibility:
  Easy — purely a build-script concern (`scripts/build_metadata.py`); the
  underlying `maps/<name>/` layout doesn't need to change if this were
  revisited.

---

## 2026-07-18  repo-identity  Decision: new repo (qwtf-live-maps), not a fork of FortressOne/map-repo

Context:
  Tim linked `FortressOne/map-repo` as a starting reference for a new
  QWTF Live community map repo. Cross-referencing its ~213 package
  directories against the actual 101-map current competitive rotation
  found only ~4 overlapping maps (1on1forts, 2farms, 2fort5r, 2machr) —
  it's a legacy dueling/pub-era archive, structurally similar but not the
  same map pool.

Options:
  A. Fork/mirror FortressOne/map-repo directly, then add the missing
     rotation maps on top — inherits ~200 irrelevant legacy maps and that
     repo's git history.
  B. New repo from scratch, scoped to the actual QWTF Live rotation,
     borrowing FortressOne/map-repo's package-directory conventions
     (per-map folder, `.loc`/textures layout) as a style reference only.

Chosen: B

Reason:
  Tim's own framing: "complete and relevant for the QWTF live community
  rather than an authentic archive." A fork would ship ~95% irrelevant
  content and imply lineage/authority this repo doesn't have.

Reversibility:
  Easy — no shared git history with FortressOne/map-repo to entangle;
  nothing prevents pulling in specific maps from that archive later via
  normal PR if a genuine need shows up.
