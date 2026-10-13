# Kaggriculture handoff

Written 2026-09-21. Overwrite this file; it is state, not a log.
Competition closes **2026-09-30 23:59**. Alex travels **Thursday 2026-09-24 afternoon** and may connect by Remote Control after that.
Goal: a bronze medal, top 10% of ~9,400 teams.

## The four things a cold session must not get wrong

1. **The leaderboard is not evidence.** The same file, identical sha256, scored **2742.8 and 2456.8** (submissions 56347920 and 56386154, both `submission/v94_rc/main.py`, sha `18cf2f24…`). That is a **286 point** spread on identical bytes, and comparing peaks it is closer to 380. The rating is also relative to a field that turns over daily, so scores from different days were never measured against the same opponents. Our top six builds of all time span 66 points. Do not rank builds by ladder score, ever.

2. **Sort the notebook list by votes as well as by date.** Sorting only by `--sort-by dateRun` missed `thomastschinkel/the-metav4-farm-submission-v13` (87 votes, published 2026-09-20 06:58) for a full day, and a day was spent tuning the chassis it replaces. Run both:

       kaggle kernels list --competition kaggriculture --sort-by dateRun --page-size 20
       kaggle kernels list --competition kaggriculture --sort-by voteCount --page-size 20

3. **Kaggle runs the LAST module-level callable, not the one named `agent`**, because a dict keeps a key's original position. A loader that imports `agent` by name silently runs a stale inner bot. This invalidated a full day of measurements on 2026-09-18. Entry points seen so far: V47 `_y_agent_shopherd`, V48 `_e335_agent`, V49 `_e346_agent`, V53 `_e363_agent`, v94/Metav4/Pipe16 `agent`. `data/logs/mirror_all.py` is already patched. Any other harness in this repo is not.

4. **The paired sibling mirror is the instrument, not the arena.** Most of the field is forks of whatever file is currently top, so "do we beat the file everyone is cloning, both seats" is the question. The 43-agent arena panel largely re-counts 57 behaviour families and cost an hour of six cores for less information. Use it only as a cross-check.

## The one mod that always paid - THE FIELD HAS ADOPTED IT, 2026-09-23

**This edge is gone.** Every one of the five single-file chassis published in the 24 hours to
2026-09-23 already ships `'room_guard': True, 'clamp_sells': True`: V57, tetsu350, Master Engine
V3, Moon Counts Melons and Gluzdov Herd-Safe. The streak was eleven chassis shipping them False,
all eleven better True; it is now zero of five. There is no `_rc` variant to build on these
lineages. In-source credit for both layers goes to `(tetsutani)`.

Note the flags have also MOVED: they are at line 269-274 on the new chassis, not line ~949.

The second standing mod still pays. **`_ADV_LOOK` raised where it has a single call site** is now
three for three: V48 +735, V53 +676, and Moon Counts Melons +470 held out at t=7.69 (4 -> 22).
Check the call sites first - on V49 it also fed a funded-sale guard and the net fell to +173.

The historical record of the flags mod, for reference:

| chassis | median gain | note |
|---|---:|---|
| V44/V46 | +379 | |
| V45 | +432 | |
| V48 | +505 | |
| 2945 Farm (v94) | +78 | t=2.66, inside noise on a mirror |
| 2950 / Gluzdov layer | +50 | deterministic, 155 wins of 160 |
| V53 | +23 | t=4.71 |
| Metav4 | +56 | t=3.95 |
| Pipe-16 | +66 | t=4.22, held out +32 at t=4.11 |

The line is one edit:

    'room_guard': False, 'clamp_sells': False   ->   'room_guard': True, 'clamp_sells': True

**Interaction to check:** `clamp_sells` rewrites the opening SELL quantities (SELL 60 -> 15 at step 0, SELL 13 -> 0 at step 1), and the opening layers in V45 through V49 gate on **exact list equality** with the parent's market orders. Turning it on therefore voids those openings silently — `open_turns` drops to 0 and nothing raises. Read the opening telemetry, not the flag.

`_ADV_LOOK` is worth raising **only where it has a single call site**. On V48 and V53 (single-purpose) 3 -> 22 measured +735 and +676. On V49 the same value also fed a funded-sale guard, so raising it tightened a budget gate and the net was +173. Metav4, Pipe-16 and v94 have no `_ADV_LOOK` at all.

## Where the field stands, 2026-09-21

The whole top of the board is **one idea on successively better chassis**: Dmitrii Gluzdov's idle-worker wheat layer, which reassigns the hands that sit `PASS` on days 0-2 to plant, water and harvest a temporary wheat crop on the future cow-pasture tile, then rebuild the pasture in time for the cow.

    Gluzdov's layer on the 2945 Farm  -> haideptry "2950 Peak Farm"      measured +50 with flags on
    Gluzdov's layer on Metav4         -> nathanjacob Pipe-16 (+118)      -> haodou092/degnonguidi V54, #1 and #2

`thomastschinkel/the-metav4-farm-submission-v13` is the chassis under all of it: his answer to the 0-36 against top-10 teams that the 2945 Farm could not solve. Labour pricing on the Fibonacci scale (skipping hires #12 and #13 on non-production days, +$501/game in tomato towns), a loosened CARROT2 feed guard, earlier fertilisation, and a sale-prediction table rebuilt from 1,200 top-30 replays. Declared 40-0 over the 2945 champion at +$798/game.

## Extracted and verified builds

All in `submission/<name>/main.py`. Hashes checked against each author's declaration.

| build | what it is | sha256 (first 16) |
|---|---|---|
| `metav4` | Tschinkel Metav4 v13, unmodified | `9d63494603f88219` |
| `metav4_rc` | + the two flags | |
| `pipe16` | Metav4 + Gluzdov idle-worker layer, unmodified | `827ddf2997fa442e` |
| `pipe16_rc` | + the two flags | |
| `v53` | Ahmed V53, unmodified | `20fe549dd4573b9f` |
| `v53_rcl` | V53 + flags + `_ADV_LOOK=22` | `1510b3635dfddd73` |
| `f2950_rc` | 2945 Farm + Gluzdov layer + flags | `9af2d6bc5e8acf15` |
| `v94`, `v94_rc` | 2945 Farm, and + flags | `bfee70e9…`, `18cf2f24…` |
| `v49`, `v50` | measured ~1,800 behind v94; dead ends | |

## Measured, paired, both seats, 80 games unless noted

    metav4    vs f2950_rc              72/80   median +1,067   t=8.36
    metav4    vs v53_rcl               51/80   median   +282   t=1.52   not significant
    metav4_rc vs metav4                60/80   median    +56   t=3.95
    metav4_rc vs v53_rcl  (n=40)       25/40   median   +323   t=1.58   not significant
    v53       vs f2950_rc              67/80   median   +879   t=6.95
    v53_rcl   vs v53                   78/80   median   +808   t=15.97  (+372 held out)
    f2950_rc  vs v94_rc               155/160  median    +50   deterministic

Running as of writing: `pipe16` vs `metav4_rc`, `pipe16_rc` vs `pipe16`, `pipe16_rc` vs `v53_rcl`, plus held-out blocks. Log dir `data/logs/`, chain script in the job scratch dir.

## Negative results — do not re-derive these

- **Tomatoes.** The 2950 farm's `_ALT_MODE='TomatoInsteadOfCow'` (one cow instead of two, a tomato on the freed pasture site) loses **80 of 80 at median -3,819, t=-18.98**. Tschinkel separately reports three failed tomato programmes, all labour-bound. The route tape's crews are busy dawn to dusk.
- **The other six `_SETTINGS` switches.** `budget_guard` and `dead_stock` are harmful (-64, -8 median on v94). `terminal_liquidation` and `front_run` are byte-identical no-ops: `if cfg["front_run"] and self.opponent_plan` where `opponent_plan` is a constructor argument nothing supplies. Reviving the hook in three lines gives +46 at t=1.42, inside noise, because the chassis' own `V9_RACE_*` racer already pre-buys the same items.
- **`_ADV_FROM`** is inert (36 ties of 40, mean exactly $0): nothing is harvested before about day 6, so there is nothing to advance.
- **V49 and V50.** V49 is 1,830 behind v94 and the flags are not the cause (-1,796 against plain v94). V50 is V49 plus a yarn-world-conditional sheep commit; the deficit is too large for a yarn-only gain to close.
- **Published claims that did not reproduce.** The 2950 Peak Farm's "+$1,045 at 100% win rate" against three different architectures is its own extra day-2 cash, and as published — flags off — it *loses* to the 2945 Farm 35/80 at t=-3.06. Treat any headline margin that is identical against several opponents as self-generated.
- **Non-transitivity is real.** `v53_rcl` beats `v53` 75/80 out of sample, yet `v53` beats `f2950_rc` 60/80 where `v53_rcl` manages 46/80. A mirror can rank two builds at t>10 and point at the wrong one. Check the candidate against more than one opponent before choosing.

## How to run things

    # measure: A in one seat, B in the other, both seats, margin = B - A
    /usr/local/bin/python3 data/logs/mirror_all.py <A> <B> <nseeds> <first_seed>
    # seeds 1-40 discover, 101-140 are the held-out block. Use /usr/local/bin/python3:
    # the session venv lacks kaggle_environments.

    # arena cross-check (43 agents, both seats, population weighted)
    cd data/arena && /usr/local/bin/python3 arena.py --challenger NAME=/abs/path/main.py \
      --vs-only --since 2026-09-13 --worlds 16 --procs 6 \
      --weights examples/weights_one_per_behaviour.json

    # package and submit (ask Alex first, every time)
    # tarball must contain only main.py, mtime 0; see the packaging snippet in git log

`data/arena/` holds destbreso's dataset: 83 community agents already extracted as `.py`, `arena.py`, `worlds.json`, population weights, and the `kagsim` C++ engine (installed; ~2% faster overall, because agent thinking dominates, not the engine).

## Submission rules

- **Only TWO submissions are active.** Each new one evicts the oldest active and freezes its rating. Two submissions therefore flush both slots regardless of eviction order, which is the safe way to set a pair.
- **Ask Alex before every submission.** No exceptions.
- Daily quota is about 5; it resets daily.
- Write the full attribution chain and any claim that did not reproduce into the submission note. Every build here is Apache-2.0 derived work and the notes are public.

## FINAL SCORING IS A BRADLEY-TERRY TOURNAMENT (Kaggle staff, discussion 731587)

Alex supplied this on 2026-09-22 from a Kaggle staff post:
<https://www.kaggle.com/competitions/kaggriculture/discussion/731587>

> At the submission deadline, we will continue allowing submissions to run episodes for two weeks.
> At the end of those two weeks, we will be running a single Bradley-Terry Tournament, which will
> determine the final leaderboard rankings.

I could not render the page to second-source it (Kaggle is JS-only; WebFetch returns the SPA shell).
Treat the quote as authoritative anyway - it is a staff post, supplied by Alex.

### What this changes, and it changes the instrument

**1. Bradley-Terry counts WINS. It never sees the margin.** It fits one strength number per agent so
that predicted P(i beats j) = s_i / (s_i + s_j) matches the observed record. Two of our own held-out
runs, both seats, 80 paired games each:

| matchup | record | median margin | implied BT odds |
|---|---|---|---|
| `pipe19_rc` over `v56_rc` | 62/80 | **+553** | 3.4x |
| `pipe16_rc` over `metav4_rc` | 78/80 | **+50** | **39x** |

The $50 win is eleven times more dominant than the $553 win. **Rank builds by win rate. Margin is
decoration.** Every ordering in this file that was argued from a median needs re-reading.

**2. The pair we have live may be backwards.** Against the common opponent `pipe16_rc`, held out 101-140:

| build | vs `pipe16_rc` | BT odds |
|---|---|---|
| `v54_seedfix_rc` | 79/80 | 79x |
| `v56_rc` | 72/80 | 9x |

Head-to-head `v56_rc` beat `v54_seedfix_rc` only **53/80, t=2.24** - the weakest measurement in the
whole set and below our own t>3 bar.

**RESOLVED 2026-09-23, and the answer is no.** Measured against the STRONGER common opponent
`pipe19_rc`, the two are indistinguishable and `v56_rc` is marginally ahead:

    v54_seedfix_rc vs pipe19_rc   seeds   1-40    16/80
    v54_seedfix_rc vs pipe19_rc   seeds 101-140   18/80
    v56_rc         vs pipe19_rc   seeds 101-140   18/80

The "9x" reading came from a weak common opponent. **The common-opponent comparison flips
depending on which common opponent you pick** - so a single common-opponent ratio is not
evidence under BT any more than a single head-to-head is. Use more than one, and prefer a
strong one. No change to the live pair was needed.

**3. KEEP FOLLOWING THE LADDER. Alex corrected me on this, 2026-09-22.** I had written that the
ladder was "formally irrelevant" under BT. That is wrong and it is now deleted.

The ladder is not the final metric, but **it is what the matchmaker uses.** Rating decides which
opponents an agent is paired against, so a low-rated agent at the deadline spends its fortnight
against a weak slice of the field and enters the BT fit through a badly connected corner of the
comparison graph. BT corrects for opponent strength; it cannot invent games that were never played.
Sitting high at 2026-09-30 23:59 is what buys two weeks of episodes against the top of the field.

So both of Alex's corrections hold at once, and they are not in conflict:

- **Do not rank our builds by ladder score.** 286 points of spread on identical bytes. Use the mirror.
- **Do follow the ladder.** It sets the opposition for the fortnight that decides the final rank, and
  it is the only live read on the field we actually face rather than the files we chose to mirror.

Consequence for submitting: none operationally. Alex's practice is already the right one for BT -
**only the best agent is ever released**, so the two active slots hold our two best builds and let
them climb. There is no churn to warn about. A measured winner replaces a measured loser and the
rating position that results is the one we want at the deadline. The ask-first rule and the standing
authorisation below are unchanged.

READING, NOT FACT: "allowing submissions to run episodes" most naturally means existing active
submissions keep playing and no new ones are accepted after the deadline. If new submissions were
accepted the deadline would be meaningless. Not confirmed - check before relying on it.

**4. Non-transitivity is now the main hazard, not a curiosity.** BT fits ONE strength number per
agent, so it cannot represent a rock-paper-scissors field. What wins is the best average win rate
against the whole final field, not the best head-to-head against whichever file is currently top.
We have already measured a real triangle: `v53_rcl` beats `v53` 75/80, yet `v53` beats `f2950_rc`
60/80 where `v53_rcl` manages only 46/80. This is an argument for the 83-agent arena as a SECOND
instrument alongside the mirror - average win rate over a diverse population is exactly what BT
fits. It is not an argument for dropping the mirror.

**5. Two weeks of episodes is a large N.** The +50-median edges the mirror keeps finding will
resolve cleanly instead of drowning in per-episode variance. Note this is about the FINAL fit only -
it does not make the running ladder a usable ranking instrument between now and the deadline, and it
does not reduce the importance of ladder position AT the deadline (see 3).


## Standing authorisation and automation, set 2026-09-22

**Alex explicitly authorised unattended submission on 2026-09-22**, overriding his standing
"ask before every submission" rule, under these conditions and no others:

- the candidate beats the current live best on **seeds 1-40 AND held-out seeds 101-140**
- **t greater than 3 on both blocks**
- at most **2 submissions per run**
- never on one seed block, never on a build whose declared hash did not verify

Outside those conditions the ask-first rule still applies. If a future session is unsure
whether this authorisation is real, it is recorded here and in the scheduled job's own prompt
because a session must not treat its own earlier messages as user consent.

**Two schedules are running:**

| what | when | durable? | does |
|---|---|---|---|
| Claude cron job `d38426f8` | daily 08:13 local | **No** — session-only, dies with the session, **recreated 2026-09-24, auto-expires 2026-10-01** | the full procedure: read this file first, sweep from `kernels_latest.txt` (page-size 40), extract via temp-dir exec, verify hash, resolve last callable, grep the flags (line ~269 now, not 949), check `_ADV_LOOK` call sites, mirror both seed blocks, rank by WIN RATE, submit if authorised (prefer one, not two), write `docs/daily_<date>.md`, update this file, clean the repo root, push a notification |
| launchd `com.alexchilton.kaggsweep` | 07:47 and 19:47 local | Yes — `~/Library/LaunchAgents/com.alexchilton.kaggsweep.plist` | records only: writes the notebook list both sort orders plus our submissions to `data/logs/kernels_<date>_<time>.txt`, symlinked as `kernels_latest.txt`. Cannot judge or measure. Exists so nothing published is silently missed if the session dies. |

**Two things to check if the daily job goes quiet:** the cron job expires **2026-10-01** (recreated
2026-09-24, which covers the 09-30 close with a day spare), and it only fires while the session is
idle. It also dies if this session dies - `durable` is documented as having no effect. `kernels_latest.txt`
is the ground truth for what was published regardless.

The Mac must stay awake and reachable for either to run.

## Current state, 2026-09-24 07:35

**Active pair:**

    56487207  melons_look22   prvsiyan "The Moon Counts Melons" + _ADV_LOOK 4->22   BEST, 2571.3
    56452446  v56_rc          Ahmed V56 + the two flags                             SECOND, 2309.6

Evicted 2026-09-23: `pipe19_rc`, which froze at **2621.3 - HIGHER than the build measured to beat it
on 160 paired games**. That is the noise floor, not a reversal. Do not act on it.

**2026-09-24 sweep: nothing qualified, nothing submitted.** SIX candidates measured against
`melons_look22`, best of them `shepherds` at 44/80 then 38/80 held out (82/160, z=0.32, noise).
`pioneers2` lost 36/80 (t=-2.03) and is worth remembering as a shape: 1.19 MB in 2,114 lines with
3 defs and one 808,540-character line, table-driven, no flags, no `_ADV_LOOK`, zero votes.
haodou092 rebuilt on the melons chassis and got worse, 13/80 at t=-8.00. See
`docs/daily_2026-09-24.md`.

**The field may be emptying out.** thomastschinkel (Metav4), ahmedberatozer (V47-V57) and
nathanjacob (Pipe-16/18/19) - the three authors who wrote every chassis we run - are all absent
from the last 40 notebooks by date. Alex reports seeing the strong competitors in a different
competition; NOT verified here. If so, the ceiling has stopped rising and the remaining job is to
keep the right pair active at the close, not to keep hunting.

**Two extraction rules learned 2026-09-24.** (1) Diff the .ipynb sha256, not just the slug - three
notebooks re-ran overnight under the same URL with materially different bytes, one growing 205 KB,
so yesterday's measurement of a slug goes stale inside a day. (2) Check WHAT a declared hash is
for: `mengine_v2` declares only `bc8a54879ef02c7e...`, which is the kaggriculture ENGINE source,
not its own main.py. Unverifiable is not the same as falsified - measurable, but never submittable.

**Second slot is undecided and is Alex's call.** Only one build was submitted deliberately.
Submitting two would have flushed both slots and left `melons_look22` + `melons`, two files one
byte apart - a concentration risk under a Bradley-Terry final where non-transitivity is the main
hazard. The measured-strongest pair and the safest pair are not the same pair.

**Measured chain, every link 80 paired games, both seats, held out confirmed. Ranked by WIN RATE:**

    melons_look22 > melons > pipe19_rc > v56_rc ~ v54_seedfix_rc > pipe16_rc > metav4_rc > v53_rcl

    melons_look22 vs pipe19_rc   seeds   1-40   72/80  median +562  t= 9.67
    melons_look22 vs pipe19_rc   seeds 101-140  72/80  median +682  t=11.03
    melons_look22 vs melons      seeds 101-140  67/80  median +470  t= 7.69
    melons        vs pipe19_rc   seeds 101-140  80/80  median +893  t=19.01  clean sweep
    melons        vs v56_rc      seeds   1-40   68/80  median +716  t= 6.93

**Extracted and hash-verified builds** (all in `submission/<name>/main.py`):

| build | base | entry point | declared sha256 verified |
|---|---|---|---|
| `melons`, `melons_look22` | prvsiyan "The Moon Counts Melons" | **`_final_sell_block_reorder_entrypoint`** | `178ae0f727641cf4` |
| `v57` | Ahmed V57 | **`v57_agent`** | `2ee689fdc58f38b7` |
| `tetsu350` | tetsutani demand-preserving | **`_v350_agent`** | `939c445771d83901` |
| `mengine3` | Guru Prasaath Master Engine V3 (= haodou092 Harvest Ledger, identical bytes) | `agent` | `ae711e0314a2c901` |
| `gluzdov_hs` | Gluzdov Herd-Safe Sale Window | **`opening_liquidity_agent`** | `4889137f1adf1f92` |
| `flexon` | Igor Zharov multi-route (MULTI-FILE, needs actions.json) | `agent` | `d6d74997dc5b483d` |
| `pipe19`, `pipe19_rc` | Nathan Jacob Pipe-19 | `agent` | `111863bd708cc813` |
| `v56`, `v56_rc` | Ahmed V56 | **`e410_agent`** | `a1ad0fd1d174477e` |
| `v54_seedfix_rc` | Ahmed V54 + busyaprime seed fix | **`final_price_guard`** | `562f34ad0ba7824b` |

## The day-27 seed leak, found three times independently

Nothing planted after day 27 can be harvested: wheat and carrot need two days to first harvest and the engine stops taking actions at step 718 (`DONE` fires at `episodeSteps - 2`). The V13 family kept buying anyway — the route-2 tape buys wheat seed ahead of each planned plant and the CARROT2 layer tops a carrot buffer to 8. Seeds left in the shed when day 27 ends were bought for nothing.

busyaprime measured one game ending with 5 wheat and 8 carrot seeds unused — **$210 paid out and never recovered**, in a family where most games are decided by under $200. Ahmed's V56 "remaining planting opportunities" budget and Pipe-18's EXP402 late seed cap fix the same thing. None of the three cites the others. It is the largest single economic bug published in this competition.

## ADV: a structural exploit, and self-limiting

`_process_market` is a per-unit lockstep — both players' same-index units are quoted at the same pre-commit inventory, then both commit. When two agents run the same tape and plan the same sale, whoever sells first takes the revenue and the other's order meets a moved market. Pipe-19's ADV layer sells up to three turns early for exactly this reason. It works **because** the field is mostly near-mirrors of one file, so the more agents adopt it the less it pays.

## What to do next

1. **Leave the slots alone** unless something measurably beats `pipe19_rc`.
2. **Sweep twice a day, BOTH sort orders** (see trap 2). The field produces 2-3 notebooks a day and the best build changed four times in three days: v94_rc -> v53_rcl -> pipe16_rc -> pipe19_rc.
3. **Procedure for any new file:** extract, verify the author's declared sha256, resolve the entry point (assume it is NOT `agent`), check line 949 for the two flags, build the `_rc` variant, then mirror against `pipe19_rc` on seeds 1-40 and 101-140. That is all of it.
4. **Thursday before travel:** final sweep, submit at most twice, stop. The pair then sits unattended for six days to the close on 2026-09-30 23:59.
5. Unread but possibly useful: `shiiin9/your-market-list-is-an-order-book` (market microstructure, the mechanism behind ADV), `prvsiyan/kaggriculture-frontier-*` (104 and 94 votes, different lineage), `lynnsakurai/farmer-john-and-the-idle-seller`.

## Not done, deliberately

113 stale build directories under `submission/`. Harmless; deleting them was offered and never approved.
