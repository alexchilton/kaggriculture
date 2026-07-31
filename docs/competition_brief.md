# Kaggriculture — Competition Brief

Everything in this file is either quoted from the competition docs or measured directly.
Where a number was measured, it says so.
Where it is inferred, it says so.

## The competition

| Field | Value |
|---|---|
| URL | https://www.kaggle.com/competitions/kaggriculture |
| Category | Featured |
| Prize | $50,000 USD |
| Launched | 2026-07-30 |
| Final deadline | **2026-09-30** |
| Merger / new-entrant deadline | 2026-09-23 |
| Max team size | 5 |
| Submissions per day | **5** |
| Teams at time of writing | 223 (2026-07-31, day 1) |
| Tags | `simulations`, custom metric |
| Env id | `kaggriculture` (also ships a `kaggriculture_beginner` variant) |

Alex has already joined the competition.
He is competing **separately** from his friend, who is independently attempting
MaskablePPO with a custom entity transformer policy, and they compare notes on Discord.

## The game in one paragraph

Two players each run a farm.
30 days x 24 turns = **720 turns**.
Start with **$3000** and one unlocked 5x5 quadrant of a 10x10 farm.
Buy seeds and livestock, plant, water, harvest, feed and care for animals, hire day labourers,
and sell produce into a **shared** dynamic market.
Whoever has the most money in the bank at the end wins.
Unsold inventory is worth nothing.

Full rules: `reference/README.md`.
Getting-started guide: `reference/AGENTS.md`.
**Ground truth: `reference/kaggriculture.py`** (1054 lines, pure Python).

## Measured baselines

Run locally against `kaggle-environments` 1.32.2 on the M4.

```
starter vs starter  ->  3512 / 3512     (+$512 profit over a whole season)
starter vs pass     ->  3508 / 3000
random vs pass      ->   120 / 3000     (random burns nearly everything)
random vs random    ->     0 / 0
```

**The bar is on the floor.**
The built-in `starter` baseline that most competitors will fork makes **$512 in 30 days**.
Nobody had found the money as of day 1.
Leaderboard is an Elo-style skill rating starting near 1000; top was 1406.8 on day 1.

## Measured performance

| Metric | Value | Note |
|---|---|---|
| Env step rate | **1163 steps/sec** | single-threaded Python, M4, includes agent compute |
| Full episode | **0.62 s** | 720 steps |
| Episodes/sec | **1.61** | single core |

This is the binding constraint on any RL approach and is why the design ports the sim
to a vectorized implementation.

## Inference budget — the constraint that shapes everything

From `reference/kaggriculture.json` and `kaggle_environments/schemas.json`:

| Setting | Value |
|---|---|
| `actTimeout` | **1 second per turn** |
| `remainingOverageTime` | **12 seconds banked for the entire episode** |
| `runTimeout` | 1200 seconds for the whole episode |

**There is no room for online search.**
Deep MCTS or per-turn planning is structurally impossible.
A neural network forward pass (~1-5 ms) fits trivially.
Any expensive computation must happen offline and be compiled into either a
static schedule or network weights.

## Action space

Per unit (farmer and each hired hand), one op per turn, ~19 total:

```
Movement:  NORTH SOUTH EAST WEST PASS
Shed:      PICKUP <item> [n]   PLACE <item> [n]   DROP
Plants:    PLANT <crop>   WATER   HARVEST   FERTILIZE
Animals:   BUILD_COOP  BUILD_PASTURE  FEED  COLLECT_FERTILIZER  CARE
Terrain:   DIG
```

WATER / HARVEST / FERTILIZE / FEED / CARE / DIG apply to the tile the unit is **standing on**.
Movement is one action per cell.
**Routing is therefore a first-class cost**, not a detail.

Market action is a separate ordered list of up to `maxMarketOrdersPerTurn` (default **10**) orders:

```
["BUY_SEED", crop, n]   ["BUY_PRODUCT", item, n]   ["BUY_ANIMAL", animal, n]
["SELL", item, n]       ["HIRE"]                   ["BUY_LAND"]
```

Invalid actions are silent no-ops.
Only `WHEAT` and `FERTILIZER` can be bought back via `BUY_PRODUCT`.

Full action dict returned by an agent:

```py
{
  "farmer": [op, ...args],
  "hands":  [[op, ...args], ...],   # one per hired hand, in hands order
  "market": [[op, ...args], ...],   # ordered, capped at 10
}
```

## Observation

Both farms are **fully visible** (tiles, crops, `planted_day`, farmer and hand positions,
money, unlocked quadrants, hires today).
Only the shed, seed store, and unit inventories are private.
Market inventory and prices are shared and visible.

This means **you can see exactly what the opponent is growing and precisely when it will yield.**
See `docs/economics_analysis.md` for why that matters.

## Sources of randomness

The environment is deterministic given a seed except for:

- **Weed spawns** — `weedSpawnChance` 0.005 per empty unlocked tile per end-of-day.
- **Town shop unlock order** — random selection from the remaining pool every 3 days.

Everything else is deterministic.
This is a much friendlier measurement environment than Orbit Wars, and the design exploits it.

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
| `townCenterSellInterval` | 12 |
| `farmHandCostMult` | 1 |

## Working with the Kaggle API

Credentials at `~/.kaggle/kaggle.json`. The `kaggle` CLI was **not installed** as of 2026-07-31;
the API was driven directly with curl and basic auth.

```bash
pip install kaggle           # or drive the REST API directly
kaggle competitions list -s kaggriculture
kaggle competitions submit kaggriculture -f main.py -m "v1"
kaggle competitions submissions kaggriculture
kaggle competitions episodes <SUBMISSION_ID>
kaggle competitions replay <EPISODE_ID>
kaggle competitions logs <EPISODE_ID> 0
kaggle competitions leaderboard kaggriculture -s
```

Submission must have `main.py` at the root exposing an `agent` function.
Multi-file: `tar -czf submission.tar.gz main.py helper.py model_weights.pkl`.

## Local setup

```bash
pip install -U "kaggle-environments>=1.32.2"
```

```py
from kaggle_environments import make
env = make("kaggriculture", configuration={"episodeSteps": 720}, debug=True)
env.run(["main.py", "starter"])
print([(i, s["reward"]) for i, s in enumerate(env.steps[-1])])
```

Built-in agents available by name: `"pass"`, `"random"`, `"starter"`.