# The melon that "would not harvest" is the environment's own rule, not our bug

Closed 2026-08-06.
Recorded so it is not re-investigated.

## The observation

A one-unit micro run put four MELON tiles holding a full six units each right beside the shed, and the unit spent the whole day doing survival waters on distant strawberries instead of collecting $6,000 of melon two steps away.
That looked like a serious prize-model fault — a ripe crop outranked by a survival water — and was written up as "worth more than the DROP timing".

## Why it is not a fault

`kagg/search/router.py:243` gates HARVEST on `age >= info["first"]`:

```python
if held > 0 and age >= info["first"] and (info["ongoing"] or _one_shot_is_finished(info, age, room)):
```

MELON's `first_yield_day` is **10**.
So a melon at age 6 offers no ops at all, whatever it is holding:

```
held=6  age= 6   []
held=6  age= 7   []
held=6  age=12   [('HARVEST', 1500)]
```

The environment does exactly the same thing (`reference/kaggriculture.py:395`):

```python
if day - tile["planted_day"] < crop_data["first_yield_day"]:
    ...
    return
```

A HARVEST below `first_yield_day` is a **no-op that still costs the turn**.
Our gate matches the env rule precisely, so emitting the harvest early would have burned turns and collected nothing.
The unit doing survival waters instead was correct: two dry days makes a tile a WEED, and weeded ground refuses PLANT for the rest of the season.

The micro board was the artefact — `planted_day=0` read on day 6 is age 6, four days below MELON's gate.

## The one real consequence

A one-shot crop CAN fill early and then sit idle.
Yield comes only from WATER inside `[(max_day + 1) // 2, max_day]` = ages 6-12 for melon, and a fertilized water pays two units, so a fertilized melon can reach its six-unit cap at age 8 and then do nothing for two days while occupying ground.

`crop_ops` already declines that trade — it only fertilizes a one-shot when `waters_left < room`, i.e. when the remaining window genuinely cannot fill the tile on plain waters.
So the case is handled, and no change is warranted.

## What remains open

Nothing here.
The live blocker is unrelated: the harvest reaches the shed at h19 because the return leg only fires on an empty route, so it cannot be sold and the bank stays flat all day.
See the reverted-with-numbers comment in `kagg/search/schedule_agent.py` at the return leg, and `scripts/where_the_cow_goes.py` for the trace.
