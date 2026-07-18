# RESUME — qwtf-live-maps

Last session: 2026-07-18. Built and shipped phase 1 end-to-end in one
sitting — repo scaffold, real asset harvest, `.loc` generation, metadata,
public GitHub repo, homelab sync wiring. See STATUS.md for the full
picture; this note is just "what to do if you're picking this up cold."

## If you're starting the next session

1. Read STATUS.md first, then `docs/decisions.md` (6 entries, all from
   this build).
2. The "Next (phase 2)" list in STATUS.md is Tim's own deferred scope —
   start there if he says "keep going on the maps repo" without more
   detail.
3. Two things this session deliberately did NOT do that are easy to
   forget are actually still open:
   - `wm-qwtf-site`'s live systemd service hasn't been restarted, so
     `sync_maps.py` isn't live on playqwtf.com yet even though it's
     committed and tested.
   - The Discord rotation list itself (source: a Discord bot's `!maps`
     command, not this repo) looks stale in a couple of spots
     (`fracturex2` vs `fracturex`, 4 played-but-unlisted maps) — fixing
     that lives outside this repo, in whatever bot/config drives it.
4. `python3 scripts/validate.py` is the fastest way to confirm the repo's
   still in a clean state after any change.
