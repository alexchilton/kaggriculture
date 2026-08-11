# Competition brief and environment rules

Everything here is quoted from the competition configuration or measured directly against
`reference/kaggriculture.py`, which is ground truth for every rule question.
Read the source rather than the README where the two disagree; that has cost this project time
more than once.

## The competition

| Field | Value |
|---|---|
| URL | https://www.kaggle.com/competitions/kaggriculture |
| Prize | $50,000 |
| Launched | 2026-07-30 |
| Final deadline | **2026-09-30** |
| Merger / new-entrant deadline | 2026-09-23 |
| Max team size | 5 |
| Submissions per day | **5** |
| Env id | `kaggriculture` (also a `kaggriculture_beginner` variant) |

Alex competes separately from a friend who is independently running MaskablePPO with an entity
transformer; they compare notes on Discord.

## The game

Two players, one 10x10 farm each, 30 days x 24 turns = **720 turns**.
Start on **$3,000** and one unlocked 5x5 quadrant.
Buy seeds and livestock, plant, water, harvest, feed and care for animals, hire day labourers,
sell into a **shared** dynamic market.
Most money in the bank at the end wins. **Unsold inventory is worth exactly zero.**

## Scoring — Elo, starting at 600

The environment hands the framework **money** as the episode reward (`s.reward` is the farm's
bank), but the competition ranks on a rating updated from match outcomes.

- **Winning matters, margin does not.** A $43k win and a $4k win score identically.
- New submissions start at **600**, not 1000. Anything judged against 1000 reads ~400 points too
  harshly — v4 at 526 was genuinely losing, v5 at 613 genuinely winning.
- Money is a good dense *training* signal and the wrong **selection** criterion.

Field movement, measured from the official episodes index:

| date | episodes | top avg | median avg |
|---|---:|---:|---:|
| 2026-07-30 | 864 | 1,152 | 670 |
| 2026-07-31 | 928 | 1,427 | 1,175 |
| 2026-08-01 | 829 | 1,581 | 1,348 |
| 2026-08-02 | 793 | 2,627 | 2,319 |

The public leaderboard on 2026-08-03 read top 2,723 / 20th 2,464 / median 819 over 615 teams,
against our best-ever submission at 600.5.
**Any target read off a leaderboard snapshot more than a few days old is stale** — confirmed again
by the next reading: the daily episode index on 2026-08-08 read `median_avg_score` **3,067.75** and
`top_avg_score` **3,192.89**, against our best-ever submission at **1,123.5**
(`docs/the_top_five_clusters_2026-08-09.md`). We are roughly a third of the way up the field, not
close to it — read that file before treating any older "the gap is just price realised per unit"
framing as the whole story.
**2026-08-11 addendum:** the 15-replay sample above is now superseded in scale by
`docs/the_ladder_is_two_scripts.md`, measured from 2,744 ladder seats: the ladder top is ~3,210, our
best-ever submission is 1,257.9, and the field plants 108-147 WHEAT tiles a season against our 24.

## Baselines, measured locally on 1.32.2

```
starter vs starter  ->  3512 / 3512     (+$512 profit over a whole season)
starter vs pass     ->  3508 / 3000
random vs pass      ->   120 / 3000
random vs random    ->     0 / 0
```

**Never tune or evaluate against `starter` alone.** It sells almost nothing, so the market is never
contested and every number comes out roughly 2x reality. That mistake cost a submission.

## Inference budget

| Setting | Value |
|---|---|
| `actTimeout` | **1 second per turn** |
| `remainingOverageTime` | **60 seconds banked for the whole episode** |
| `runTimeout` | 1200 seconds for the whole episode |

The 60 is from `reference/kaggriculture.json:128`; an earlier note here said 12 and several
design decisions were made against that wrong figure.

No *per-turn* online search. A network forward pass (~1-5 ms) fits trivially, and 60 banked seconds
allows a planning burst at turn 0 or a shorter one every few days.

## Action space

Per unit (farmer plus each hired hand), one op per turn, 18 ops:

```
Movement:  NORTH SOUTH EAST WEST PASS
Shed:      PICKUP <item> [n]   PLACE <item> [n]   DROP
Plants:    PLANT <crop>   WATER   HARVEST   FERTILIZE
Animals:   BUILD_COOP  BUILD_PASTURE  FEED  COLLECT_FERTILIZER  CARE
Terrain:   DIG
```

WATER / HARVEST / FERTILIZE / FEED / CARE / DIG act on the tile the unit stands on, so **routing is
a first-class cost**.

Market is a separate ordered list of up to `maxMarketOrdersPerTurn` (default **10**):

```
["BUY_SEED", crop, n]   ["BUY_PRODUCT", item, n]   ["BUY_ANIMAL", animal, n]
["SELL", item, n]       ["HIRE"]                   ["BUY_LAND"]
```

Invalid actions are **silent no-ops**. Only `WHEAT` and `FERTILIZER` are legal `BUY_PRODUCT` items.

```py
{"farmer": [op, *args], "hands": [[op, *args], ...], "market": [[op, *args], ...]}
```

An agent submits exactly one unit action per unit it owns.

## Observation

Both farms are fully visible: tiles, crops, `planted_day`, unit positions, money, unlocked
quadrants, hires today. Only the shed, seed store and unit inventories are private.
Market inventory and prices are shared and visible.

Per-turn state the env hands over for free, and which the live agent reads rather than predicting:

```
obs["farms"][me]["tiles"]     watered_today, yield_units, fed_today, cared_today,
                              fertilizer_available, consecutive_unwatered
obs["farms"][me]["farmer"]    where the farmer stands -- no dead reckoning
obs["farms"][me]["hands"]     every hand, so an op cannot go to a unit we do not own
obs["farms"][me]["money"]     so a purchase is never ordered against a bank that cannot pay
obs["private"]["shed"]        so an animal is never drawn from an empty shed
obs["private"]["seeds"]       so PLANT is never blocked by the atomic-seed rule
```

## Randomness

Deterministic given a seed except for:

- **Weed spawns** — `weedSpawnChance` 0.005 per **empty** unlocked tile, once per end-of-day.
  ~40 empty tiles gives ~0.2 spawns/day, **~6 a season**, and only those landing on ground the plan
  intends to use matter.
- **Town shop unlock order** — random selection from the remaining pool every 3 days.

Everything else, including every weed that comes from our own neglect, is deterministic.

## Configuration defaults

| Parameter | Default |
|---|---|
| `episodeSteps` | 720 |
| `boardSize` | 10 |
| `startingMoney` | 3000 |
| `maxMarketOrdersPerTurn` | 10 |
| `turnsPerDay` | 24 |
| `shedCapacity` | 100 |
| `weedSpawnChance` | 0.005 |
| `townShopUnlockInterval` | 3 |
| `townShopSellInterval` | 4 |
| `townCenterSellInterval` | 12 (1.32.2) / 24 (1.32.6) |
| `farmHandCostMult` | 1 |

## Engine rules that have each cost a day

Every one of these was, at some point, written up as our bug and turned out to be the environment.

- **`first_yield_day` gates HARVEST.** MELON's is 10. A HARVEST below it is a **no-op that still
  costs the turn** (`kaggriculture.py:395`). `router.py:243` matches the rule exactly.
- **A one-shot crop is demolished by HARVEST**, so it must not be harvested until full.
  `_one_shot_is_finished` refuses while `room > 0`, correctly. Yield comes only from WATER inside
  `[(max_day + 1) // 2, max_day]` — ages 6-12 for melon — and a fertilized water pays two units, so
  a one-shot can fill early and then sit idle. `crop_ops` only fertilizes a one-shot when
  `waters_left < room`, so that trade is already declined.
- **Ongoing crops yield `max_yield` once per LIFETIME, not per day.** Tomato is 8 units per tile per
  season, strawberry 6 — not 4.0 and 2.0 per day as the Object Types table reads. Pinned by
  `tests/test_production.py`. Do not re-derive from the published tables.
- **Animals have no `production_count` cap**, so they produce until they starve. A goose gives
  26 eggs a season against a `max_held` of 4.
- **`consecutive_unfed >= 2` removes the animal** and leaves the structure
  (`kaggriculture.py:786`). Not "a day's production forgone" — a $400-$500 asset written off plus
  every remaining day of its output.
- **`consecutive_unwatered >= 2` turns a PLANT tile into a WEED** (`kaggriculture.py:753`), and
  weeded ground refuses PLANT until DIG clears it.
- **The shed holds 100 items and `_drop_inventories_to_shed` DESTROYS the overflow** at dusk.
  Carried inventory is uncapped during a day and emptied every night.
- **`SELL` sees only the shed.** Harvest 90 melons and never DROP and the market cannot see them
  until the overnight sweep, which is usually too late to fund a same-day land or animal buy.
  `BUY_PRODUCT` and `BUY_ANIMAL` also settle only against the shed; FEED, HARVEST and
  COLLECT_FERTILIZER only touch the acting unit's own inventory.
- **`PLACE` and `FEED` draw from the unit's CARRIED inventory, not the shed.**
- **Atomic PLANT.** The reference drops *every* PLANT for a crop when a turn's requests exceed the
  seeds held, counting the actions **submitted**, not the units that exist.
- **Market orders pair by slot.** `_process_market` pairs the two players' *i*-th order and quotes
  both from the same pre-commit inventory, so both seats pay the same price on a contested unit.
  Orders past the tenth slot are dropped.
- **Hire cost is `mult * fib(n)` in the day's hire count and RESETS EVERY MORNING**, so it is paid
  30 times. 8 hands is $54/day; 12 is $376/day; 14 is $986/day; 17 is $4,180/day.
- **`_do_buy_land` ignores which quadrant you ask for.** Prices are $1,000 / $2,000 / $4,000 in a
  fixed order.
- **Three of the four shed-access tiles start LOCKED** (NE, SW, SE), and hands can spawn on them.
- **A pasture or coop sitting on a shed-access tile does NOT block DROP/PICKUP or movement.**
  `_is_shed_adjacent` is pure coordinate membership; the only tile state that blocks anything is
  `"LOCKED"`. Confirmed by `tests/test_pens_do_not_block_the_depot_ring.py` (7 cases), including a
  positive control that LOCKED *does* block.
- **An unaffordable or unfillable order is refused silently.** There is no rejection signal in the
  observation, which is why our agent re-offers every turn and why any metric counting *offers*
  rather than *fills* over-reads by up to 11x.

## Version skew — 1.32.2 vs 1.32.6

`kaggle-environments` 1.32.6 shipped a "town rebalance" on 2026-08-07:

```
townCenterSellInterval        12 -> 24      the centre buys once a day, not twice
TOWN_CENTER_DEMAND_SCHEDULE   [(20,4),(10,2),(0,1)] -> DELETED, flat 1 all season
MAX_SHOP_INSTANCES = 8        each unlocked shop gets its own town slot
movement onto LOCKED          blocked -> ALLOWED
```

Late-season town-centre drawdown falls **8x**, so every "hold it and dump it late" argument in this
repo was priced against the old ramp.

**The ladder was still on 1.32.2 as of 2026-08-07 evening**: replay `90751101` records
`townCenterSellInterval = 12` in its own configuration block. We upgraded, measured, found the
reference tape damaged (its `BUY_LAND` orders fail under the new economy because a fixed script
cannot wait for a better price), and pinned back within the hour.
Measuring on 1.32.6 while the ladder runs 1.32.2 optimises for a game nobody is playing.

**Check that field on every replay you download:**

```python
json.loads(pathlib.Path(replay).read_text())["configuration"]["townCenterSellInterval"]
```

Nothing in our code reads a remembered literal: `kagg/sim/town.py` reads `CENTER_INTERVAL` from the
installed env's JSON spec and `CENTER_SCHEDULE` via `getattr(kg, "TOWN_CENTER_DEMAND_SCHEDULE", ...)`.
19 tests still fail on 1.32.6 and are not fixed; three of those (`test_sim_ops`) are a real
divergence — `kagg/sim/ops.py` still blocks movement onto LOCKED.
When the ladder does move, there is a free routing gain: `_step_towards` and `_mobile` both refuse
locked tiles, so every tour currently detours around ground it would be allowed to cross.

## Kaggle API

Credentials at `~/.kaggle/kaggle.json`. Never print or commit them.

```bash
pip install -U "kaggle-environments>=1.32.2"    # earlier versions lack the env
kaggle competitions submit kaggriculture -f main.py -m "v1"
kaggle competitions submissions kaggriculture
kaggle competitions episodes <SUBMISSION_ID>
kaggle competitions replay <EPISODE_ID>
kaggle competitions leaderboard kaggriculture -s
```

Submission needs `main.py` at the root exposing an `agent` function.
Build it with `scripts/build_planner_submission.py`, which inlines the four `kagg/search` modules
plus the schedule into one self-contained file and verifies the result imports and runs — a
hand-rolled `main.py` once spliced a docstring over line 1, failed to import, and banked exactly
the $3,000 start.

The older `scripts/build_submission.py` was deleted on 2026-08-09. It copied a *single*
dependency-free agent file verbatim, which fits `kagg/agents/contrarian.py` and cannot express the
planner, so building the old way silently shipped contrarian while reporting "submission verified".
Its gate was "beats `starter`", which this project's own notes call worthless — `starter` sells
almost nothing, so the market is never contested. Use `scripts/gate_pool.py` for a real gate.
