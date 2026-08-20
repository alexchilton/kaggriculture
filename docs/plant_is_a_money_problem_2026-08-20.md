# PLANT is a money problem, not a planting problem

Board `data/seed_scripts/downloads_2026-08-19/94345389.json`, seat 0, seed 959074148, d0-d10.
Instrumented by wrapping `schedule_agent._solve` and `_refresh_pins`. No shipped code was edited.

`ROUTER` = a PLANT op reached `_solve`.
`PLAN` = a PLANT op is in the tour `_solve` returned.
`EXEC` = the environment recorded a PLANT action.

    day  empty   owned   row    pins   chain  ROUTER PLAN   EXEC   his
    0    25      25      13     13     0      13     13     13     13
    1    7       25      0      0      0      0      0      0      0
    2    7       25      0      0      0      0      0      0      0
    3    7       25      3      3      0      3      3      3      3
    4    13      25      4      4      0      4      4      4      4
    5    7       25      3      3      0      3      3      3      3
    6    4       25      4      4      0      4      4      4      4
    7    0       25      18     18     0      18     18     14     18
    8    10      50      4      8      0      8      8      8      4
    9    2       50      0      0      0      0      0      0      0
    10   0       50      19     19     0      19     19     8      19
    sum                  68     72     0      72     72     57     68

`ROUTER == PLAN` on every day. The router and the planner are not the defect.

## d7: the four missing plants belong to a unit that was never hired

    tile      unit   stop#   ops                 planted   hours a unit stood there
    (8, 3)    11     0       PLANT,WATER         NO        never reached
    (9, 3)    11     1       PLANT,WATER         NO        never reached
    (9, 4)    11     2       PLANT,WATER         NO        never reached
    (8, 4)    11     3       PLANT,WATER         NO        never reached

Every stop belonging to units 4-10 planted. `hands 10/11` that day.
`_router_acts` plans arriving hires as vehicles before they exist, because the unit phase runs
before the market phase. The 11th hire did not land -- `_do_hire` fails **silently** on a thin bank
(`kaggriculture.py:691`) -- and its entire four-stop tour went with it.

Seeds were not the constraint: 18 STRAWBERRY arrive at h1 and **4 are still in the shed at h23**.
All 14 submitted plants landed.

## d10: the bank is $0 from h2 to h17

    hour  bank        seeds held
    0     1164.0      {'STRAWBERRY': 2}
    1     56.0        {'STRAWBERRY': 2}
    2     0.0         {'CARROT': 1, 'STRAWBERRY': 2}
    ...   0.0         -                              (h6-h17)
    18    95.0        {'WHEAT': 9, 'CARROT': 7}

`BUY_SEED CARROT 8 / WHEAT 9` is posted at h1 and re-posted every hour until h18, when all 16
seeds arrive at once. Five plants follow in the six hours left. `hands 7/9`.

## `REPLANT_A_CLEARED_TILE` never fires

`chain` is **0 on every day**. The ten tiles the d3 harvest clears are never re-sown, so the space
bought by harvesting a one-shot early is not used. This is independent of the money problem and is
a real hole in `router.build_nodes`.

## Consequence

Do not tune the planting path to fix `PLANT 57/68`. The binding constraint is cash at hour zero.
See `docs/the_sells_land_after_the_hire_2026-08-20.md`.
