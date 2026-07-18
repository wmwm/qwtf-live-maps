# RESUME — qwtf-live-maps

Last session: 2026-07-18. Built phase 1 (scaffold, harvest, loc generation,
metadata, public repo, homelab sync) then continued straight into a phase
2 first pass (box4 sourced externally, loc heuristic strengthened via
ambient markers, levelshots harvested, real-data "most played" section)
in the same sitting. See STATUS.md for the full picture; this note is
"what to do if you're picking this up cold."

## If you're starting the next session

1. Read STATUS.md first, then `docs/decisions.md` (10 entries — 6 phase 1,
   4 phase 2 — all from this build).
2. STATUS.md's "Explicitly NOT done" list is the real remaining scope —
   each item there was assessed and deliberately not attempted, with a
   reason, not just skipped. Start there if told to keep going.
3. Things this session deliberately did NOT do that are easy to forget:
   - `wm-qwtf-site`'s live systemd service hasn't been restarted, so
     `sync_maps.py` isn't live on playqwtf.com yet even though it's
     committed and tested.
   - The Discord rotation list itself (source unconfirmed — not found
     anywhere in this workspace, so probably a third-party bot's own
     data) looks stale in a couple of spots (`fracturex2` vs `fracturex`,
     4 played-but-unlisted maps) — fixing that lives outside this repo.
   - A real GitHub identity (`wm <wm@ozfortress.com>`) already pushed
     directly to this public repo once, within minutes of it going live —
     confirm with Tim whether that's expected before assuming this repo's
     history is only ever touched by sessions like this one.
4. `python3 scripts/validate.py` is the fastest way to confirm the repo's
   still in a clean state after any change.
