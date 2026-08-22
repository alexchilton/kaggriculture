# Dead-constant audit of `kagg/search/`

Measured 2026-08-17.
40 module-level boolean constants checked, each by reading the guard that consumes it, not by grep.
**17 have a branch that cannot execute.**
Nothing was deleted; this is the report the NO FLAGS rule asks for before anything is removed.

## The one that matters today

    HERD_FOLLOWS_THE_LEADERS_THREE_QUADRANT_RULE = False    schedule_agent.py:2761
    guard: 2796  if WOOL_SHOP_SETS_THE_HERD and HERD_FOLLOWS_...:

Block 2796-2814 is unreachable.
`MILK_POOR_COW`, `MILK_POOR_SHEEP` and `MILK_POOR_SHOP_COUNT` (2769-2771) are read **only** inside
it, so all three are dead.
That is why the herd has never responded to the milk draw: the rule is switched off, not mis-gated.
The live branch is at 2816 and reads the yarn store only.

## Other dead branches

    constant                                    file:line              value  what is dead
    AT_RISK_TILE_OUTRANKS_A_FEED_THAT_CAN_SLIP  cover.py:113           False  the at-risk greedy pass (1404)
    SUPPLY_LIMITS_EVERY_DRAW                    cover.py:170           False  the ops-based supply check (1319)
    DELIVER_SURPLUS_NOT_THE_ROW                 cover.py:240           False  the surplus-count arm (655)
    BANK_THE_ROWS_PRODUCE_WHILE_REAPING         cover.py:274           False  `funding` always False, reaping exemption (719)
    STRICT_FEASIBILITY                          crew.py:126            False  `raise InfeasibleDay` (626)
    SHOP_ADAPT_CROPS                            schedule_agent.py:2624 False  the `_adapt_crops(...)` call (1621)
    MEMOISE_SLOT                                cover.py:148           True   unmemoised `slot_now` fallback (1283)
    BRANCH_ON_THE_YARN_STORE                    q4_branch.py:60        True   the early-disable return (292)
    LIVESTOCK_ENABLED                           plan.py:327            True   the CEM gene-zeroing block (340)
    PLAN_THE_CREW_THAT_ARRIVES                  schedule_agent.py:236  True   old crew-count replan trigger (1861)
    LATE_SEASON_PAIR                            router.py:665          True   both `else 99` arms (667, 676)
    HIRE_FIRST                                  schedule_agent.py:1057 True   old "hire two a turn" block (4966-4977)
    ANIMAL_OVER_HIRE                            schedule_agent.py:1081 True   the `8`-slot ternary arm and skip-buying (4636-4637)

`LATE_SEASON_PAIR = True` means `FERTILIZE_UNTIL_DAY` and `LATE_TRUNCATED_PLANT_DAY` can only ever
be 26.

## Orphaned: defined, never read as a live condition, named only in comments

    CLOSED_TOUR              router.py:230
    TOP_UP_SAFE_TILES        router.py:429
    SEED_BEFORE_LIVESTOCK    schedule_agent.py:3265

## Confirmed LIVE -- both outcomes reachable, or no `else` to be dead

`REPAIR`, `COMPACT`, `TRIM_A_TAIL_THAT_CANNOT_COME_HOME`, `MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE`,
`PLACE_DRAWS_FEED`, `LATE_SEASON_TRIAGE`, `FUND_THE_DAY_WHEN_SHORT`, `HARVEST_WHAT_YOU_STAND_ON`,
`CARE_WHAT_YOU_STAND_ON`, `LAST_DAY_DEADLINE_WALK`, `CUMULATIVE_SELLS`, `LIQUIDATE_LAST_DAY`,
`SELLS_FUND_THE_TURN`, `DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND`, `PRICE_AWARE_SELL_CAP`,
`RESERVATION_SELL_CAP`, `HOLD_A_FLOORED_BOOK`, `LATE_SELL_BIAS`, `SHOP_ADAPT_HERD`,
`WOOL_SHOP_SETS_THE_HERD` (its 2816 use), `PLANT_THEN_WATER`, `REPLANT_A_CLEARED_TILE`,
`NO_UPKEEP_ON_THE_LAST_DAY`.

## Not an oversight

`DELIVER_SURPLUS_NOT_THE_ROW` is recorded in `docs/REGISTER.md` (OPEN-1) as a deliberately-off arm,
measured and rejected at -$15,272 over twelve seeds.
Dead, but on purpose.

## Note on `HARVEST_WHAT_YOU_STAND_ON`

Listed live here, and `docs/wasted_late_turns_2026-08-17.md` measures a hand standing on a ripe
3-unit wheat tile for seven consecutive hours emitting PASS.
"Live" means the guard can execute, not that it fires when it should.
Those two facts together are the open question.
