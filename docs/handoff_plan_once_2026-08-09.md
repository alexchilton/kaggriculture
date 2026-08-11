> **TARGET SUPERSEDED, added 2026-08-11.** "d0 and d1 are exact" means exact against Seb's tape,
> which was optimal under the OLD `townCenterSellInterval=12` economy. His median bank halved and he
> has since withdrawn from the ladder (`docs/the_ladder_is_two_scripts.md`, 2,744 ladder seats). The
> planner architecture change (one plan per day, at dawn) is real and still stands; exact-match-to-Seb
> is no longer the same thing as exact-match-to-the-field.

# Handoff, 2026-08-09 evening — the day is planned once, d0 and d1 are exact

Branch `shaping-potential`, HEAD `f5b1e3e`, working tree clean apart from two untracked files that
predate this session (`scripts/diagnose_season.py`, `submission/main_replay11.py`).
Nothing is pushed: `origin/shaping-potential` is at `e482451`, 180+ commits behind.

## What to read first

`.claude/skills/matching-the-tape` — written this session, after four consecutive failed attempts at
one defect. It loads automatically. **Read it before touching the planner.** The two rules that
matter are: restate Alex's instruction as the target before writing code, and prove the code path
can reach the defect first.

## Where it stands

```
python -u -m pytest tests/test_each_day_matches_the_tape.py -q          # one test per day
python -u scripts/breakdown.py --module schedule_agent_1455mh --days 7  # the table
```

    d0  PASSES
    d1  PASSES
    d2  sell 4/5   money 561/659
    d3  sell 6/5
    d4  care 6/7   sell 30/32   money 126/1311   owned 50/25
    d5  sell 28/26  money 860/1855  owned 50/25  pen 9/8
    d6  plant 13/14  water 16/17  feed 7/8  care 7/8  place 0/1  sell 17/19
        buy_product 6/9  money 1481/2565  owned 50/25  pen 9/8

`d0-d6 work 334/339` at the peak; `329` as shipped with the care arm off.
It was **274** when this session's planner work began.

d2's `sell 4/5` and d3's `6/5` are ONE unit sliding a day and reconcile — d3's money is exact.

## The agent now plans each day ONCE, at dawn

No replan, no urgency trigger, no idle top-up. `tests/..._match_the_plan.py::
test_the_day_is_planned_once_and_only_at_dawn` counts `_solve` calls and pins it at one per day.

Getting there needed four blind spots closed, because `interpreter` runs the unit phase BEFORE
`_process_market` (`kaggriculture.py:922` then `:928`):

- **the crew** — `_arrivals` + `_hires_this_turn` route the hands the turn is about to hire
- **the goods and the animals** — `PLAN_TODAYS_PURCHASES` credits `buys` and `animals_bought` at h0
- **the pens** — `BUILD_THEN_PLACE` emits the placement as its own node on the pen's tile, and
  `PLACE_FOLLOWS_ITS_BUILD` (in `cover.slot`) refuses it to any hand but the one building it
- **the morning delivery** — `WAIT_FOR_THE_MORNING_DELIVERY`: at h0 an empty shed is not a shortfall

## The two biggest single fixes, both from watching rather than reasoning

- **The feed was drawn twice per pen.** `DRAWN` contains FEED whose item IS "WHEAT", so once the
  FEED sat on the placement node `PLACE_DRAWS_FEED` added a second unit for a feed that eats one.
  A hand sat at the shed hoovering the drip while another placed cows empty-handed.
- **Hands walked over hungry animals carrying eight wheat.** The route is a visit ORDER and
  `_live_ops` is consulted at STOPS only. `underfoot()` in the tour walker now feeds the ground a
  hand is standing on, out of surplus, from BOTH the depot and travel branches.

## THE TAPE COLUMN IS NOT SEB'S GAME — this cost half a session

`breakdown.py` replays Seb's ACTIONS on **seed 11 with weeds 0.0**. The replay's own
`configuration` records `seed: None` and `weedSpawnChance: 0.005`, so he never played this board.

Consequence: `tiles 50/25` on d4 is **not our defect**. Seb's own replay shows his tiles going
25 -> 50 at d4 h23. He buys that parcel; on our board his plan cannot pay for it. We match his real
play and the tape column is the artifact. The money column from d4 onward inherits it, so
`d10 2203/6397` measures nothing clean.

Before treating any tape row as a target, check the raw replay:
`data/seed_scripts/top_guys/90494364.json` holds both the actions and the observations.

## Open, in the order to take them

1. **d6** is the worst real day: `place 0/1`, `plant 13/14`, `water 16/17`, `buy_product 6/9`,
   `feed 7/8`. It is the last day before the tape's own economy diverges, so it is worth more than
   d4's single care.
2. **d4 `care 6/7`.** One care. `CARE_WHAT_YOU_STAND_ON` buys it and spends nine others — measured,
   shipped OFF, test xfail(strict). A rule that fires only where the hand has slack is a different
   arm and has not been tried.
3. **The closing shed trip is uncharged**, so a hand can end the day in the far corner holding
   produce the row wants. Four fixes tried, all null or net-negative; the working version needs a
   per-TOUR reserve, not a per-day one.
4. **Label the tape column** in `breakdown.py` for what it is. Every conclusion from it inherits the
   caveat above.
5. **Never built:** don't dig weeds outside the geometry plan (`DIG_ONLY_IF_REPLANTING` gates on
   global `plants_left`, not per-tile); don't plant what cannot finish before season end
   (`_pointless_tiles` drops existing tiles, it does not refuse new ones).

Everything else that was in the CLI task list is now `OPEN-CLI` in `docs/REGISTER.md`.

## Measured nulls — do not re-derive these

- `RESERVATION_SLIP` 0.10 -> 0: whole grid byte-identical. The sell bunching is delivery, not the cap.
- `CHAIN_OPS`: byte-identical. `COVER_PLANNER = True`, so `router.plan_routes` never runs.
- "deliver a finished row" and "deliver a finished product" in `materialise` rule 2: never fire.
  Rule 2 inserts before a LATER job and the fertilizer is collected by the tour's last jobs.
- `SELL_ROW_PRODUCE_GOES_FIRST` (drop the `fund` gate on `Job.funds`): no change.
- `END_NEAR_THE_SHED` ranking tie-break: null on d4, a real loss on d6.
- Phantom-crew planning **without** the other three fixes: 317 -> 273. It only pays as a set.

## Housekeeping

- Five `while pgrep -f pytest; do sleep N; done` waiters from earlier sessions were found spinning
  forever and killed. Never write one.
- `data/logs` and `data/seed_scripts` are now excluded in `.idea/kaggriculture.iml`. Do not delete
  `data/logs`: it is gitignored, so deletion is permanent, and 92 log paths are cited as evidence in
  84 files.
- `.claude/` and `.idea/` are both gitignored, so the skill and the exclusion are on disk only.
