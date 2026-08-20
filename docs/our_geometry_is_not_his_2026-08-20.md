# Our geometry is not tetsuya's, and the schedule cannot make it so

Measured 2026-08-20 on `data/seed_scripts/downloads_2026-08-19/94345389.json`, tetsuya seat 0,
seed 959074148, following `data/seed_scripts/tetsuya/schedule.json`.
Raw grids: `data/logs/geom_2026-08-20.log`.

## The finding

The boards diverge on **d1** -- the first day anything is placed -- and never converge.

    === d1 h0 ===   14 of 100 cells differ
       OURS                              HIS (tetsuya)
       w0| .| .|w0|w0| .| .| .| .| .     s0|s0|s0|w0|w0| .| .| .| .| .
        .|w0|w0|w0|s0| .| .| .| .| .     w0|w0|w0|w0|w0| .| .| .| .| .
        .|w0|w0|s0| .| .| .| .| .| .     w0|w0|w0| .|C-| .| .| .| .| .
       w0|w0| .|S-|S-| .| .| .| .| .      .| .| .|C-|S-| .| .| .| .| .
       s0| .|C-|C-|S-| .| .| .| .| .      .| .| .|S-|S-| .| .| .| .| .

    d1 14 cells   d2 14   d3 14   d4 20   d5 17   d6 20

Same op counts, different board. `PLANT 90/90` on the d0-d10 grid means we planted the same
**number** of tiles, never the same tiles. The count grid is blind to geometry by construction.

Three differences, each with a cost:

- **His field is a block; ours is scattered.** He fills rows 0-2 solid. We spread across rows 0-4
  including `(3,0) (3,1) (4,0)`, the far corner from his pens. Every water and harvest we plan
  walks further than his does.
- **The pens sit in different cells.** His `(2,4) (3,3) (3,4) (4,3) (4,4)`; ours
  `(3,3) (3,4) (4,2) (4,3) (4,4)`. Four shared, one moved.
- **Crops land on the wrong tiles.** d1 he puts STRAWBERRY at `(0,0) (0,1) (0,2)`; we put WHEAT
  there and strawberry at `(1,4) (2,3) (4,0)`.

## Why -- three separate causes, all measured

**1. tetsuya's schedule carries no coordinates.** `plant_tiles`, `build_tiles` are `[]` on all
thirty days. `scripts/extract_leader_schedule.py:248` fills them from a `tape.json` that did not
exist for him -- `data/seed_scripts/tetsuya/` held `schedule.json` and nothing else. The extractor
prints `tiles: tape.json missing -- run scripts/extract_tape.py to add coordinates` and carries on.

Fixed on 2026-08-20: `data/seed_scripts/tetsuya/tape.json` now exists, 242 placements over 73
distinct tiles, extracted with `scripts/extract_tape.py --team tetsuya`. The schedule has **not**
been regenerated from it yet.

**2. `plan.load()` strips coordinates by default.**

    TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")   # kagg/plan.py:46
    def load(path=None, strip_tape_only=True):                          # kagg/plan.py:49

`strip_tape_only=False` is passed by **nothing in the repo**. So even a fully populated schedule
loses its tiles before `make_agent` sees them.

**3. The live agent never reads them anyway.** `kagg/search/schedule_agent.py` contains zero reads
of `plant_tiles` or `build_tiles` -- only two comments, at `:838` and `:868`, stating it derives
placements "off his own board rather than off `build_tiles`". It does not import `dayplan`. The
coordinate-carrying branch at `kagg/search/dayplan.py:532` is offline-only and unreachable from
the shipped agent.

So the three layers are independent, and fixing any one alone changes nothing.

## What it is worth

`scripts/extract_leader_schedule.py:166-168` records the measurement, made when the mechanism was
built:

    the tape's own tiles bank $11,638 against $6,794 for ours, with 2 refusals against 17,
    and our chooser is unstable (one run in three banked $2)

1.7x on money, from coordinates alone, on that board. Not re-measured on tetsuya's.

## Caveat

One board, one seed. The $11,638/$6,794 figure is from the earlier `new_leader` work, not from
tetsuya's game, and is quoted here as the reason the mechanism exists rather than as a prediction
for this board.
