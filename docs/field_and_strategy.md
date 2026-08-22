# The field and strategy

This doc covers what the opponent field actually does, and the strategic positioning question that
follows from it: which player or script to target, whether board or turn capacity binds the middle
game, and the arm-classifier idea for building an agent from downloaded replays.
It merges 19 source files, listed at the end of each section by their original filename.
Every original is preserved in `docs/history/` after this consolidation.
Status banners already present in a source file (SUPERSEDED, RETRACTED, "unsure — needs an owner's
eye") are carried forward unchanged below; this doc does not re-decide any of them.

---

## 1. Field composition — what the ladder actually is

### 1.1 The winners are open-loop scripts, not reactive policies

Source: `the_field.md`.
This file carries three added caveats at its own top, dated 2026-08-09 and 2026-08-11, saying its
absolute dollar figures predate the 2026-08-07/08 move to `kaggle-environments` 1.32.6 and its
"five distinct signatures" framing is superseded by `the_field_is_a_monoculture_2026-08-21.md`
(see 1.4). Read the caveats before trusting this file's numbers.

Six replays, five distinct players, checked turn-by-turn:
`senkin13` — 4 episodes, 6 pairwise comparisons, different opponents and swapped seats — units
identical 720/720 (100.0%) in all six, market identical 720/720 (100.0%) in all six, banks
$121,538–$145,034.
`syouya tobita` — units identical 720/720 (100.0%) in all six; market identical 716–720/720
(99.4–100.0%).
`Dmitry Larko` — units 701/720 (97.4%), market 689/720 (95.7%). (A different doc elsewhere put this
same pair at 93.5%; the source notes the disagreement without resolving it.)
The leader `somewhere after`, four replays, 2026-08-05: every derived quantity — land days, herd,
seed counts, fertilizer flows, crew ramp — is byte-identical across all four, in both seats, against
four different opponents. The only variation anywhere is 107 vs 106 `FERTILIZE` ops.

Every player still shows 30/30 distinct daily unit-routines — a genuine 720-step program, not one
routine repeated.

Caveats recorded in the source: `senkin13` and `syouya tobita` are a mirror match, 536/720 identical
action dicts between them, and neither is confirmed top-ranked (a strong mid-field agent at ~$145k).
The only confirmed top-tier games are the `Dmitry Larko` pair, the weakest open-loop evidence in the
table.
Zero `WEED` tiles across all 720 turns of all six replays, despite `weedSpawnChance: 0.005` — "the
winners ignore weeds" is untested, not proven harmless.
"manual player" ranked #3 at 2,911.8 — a human cannot compute reactive per-turn decisions across 720
turns under a one-second clock, which is independent evidence for the open-loop finding.

`senkin13`, episode 89541819, final reward $145,034, gross sales $220,542:
MILK $58,505 (26.5%, 235 units), STRAWBERRY $42,942 (19.5%, 309 units), WOOL $40,112 (18.2%, 190
units), WHEAT $38,632 (17.5%, 855 units), MELON $24,489 (11.1%, 123 units), FERTILIZER $14,698 (6.7%,
271 units), EGG $769 (0.3%, 12 units), CARROT $395 (0.2%, 10 units).
Animal products 45.1%, crops 48.3%, fertiliser 6.7% — not the "83% from milk and wool" single-episode
figure that circulated earlier.
Strawberry out-earns melon nearly 2:1 (309 vs 123 units). Seeds bought: STRAWBERRY 44, WHEAT 34,
MELON 21.
Wheat is bought at a loss and sold as an input: 1,055 units bought for $47,594, 855 sold for $38,632
— net cash on wheat is negative; the return arrives as milk and wool.
Fertiliser is a revenue stream: 271 units for $14,698, from `COLLECT_FERTILIZER`, one action, animal
ownership only.
Herd: COW 8, SHEEP 6, GOOSE 0; BUILD_PASTURE 14, BUILD_COOP 0; plus 304 hires and 2 land purchases.
No goose in this build.

`somewhere after`, four replays 2026-08-05: episode 90016067 (seat 1 vs haoran huang430) his
$160,593 vs their $157,959, +1.7%; 90018004 (seat 1 vs manual player) $134,780 vs $130,777, +3.1%;
90020633 (seat 1 vs Savko) $137,667 vs $133,335, +3.2%; 90023239 (seat 0 vs Savko) $123,443 vs
$118,437, +4.2%. 4/4, mean bank $139,121, mean margin +3.1%.
Land bought days 7 and 10, two parcels, never SE. 8 COW + 6 SHEEP = 14 pens. WHEAT 66 (50%),
STRAWBERRY 44 (34%), MELON 21 (16%). 318 fertilizer collected, 107 applied, 0 bought, 445 offered.
Crew 4 on day 0 ramping 4-6-5-5-6-6-6-8-10-11-12, flat 12 from day 10. DIG 103 times.
Op census, four replays aggregated: NORTH 4,943 (16.8%), WEST 4,392 (15.0%), SOUTH 3,716 (12.7%),
EAST 3,428 (11.7%), WATER 3,404 (11.6%), PASS 1,427 (4.9%), PICKUP 1,356 (4.6%), HARVEST 1,352
(4.6%), FEED 1,276 (4.3%), COLLECT_FERTILIZER 1,272 (4.3%), CARE 1,232 (4.2%), PLANT 524 (1.8%),
FERTILIZE 427 (1.5%), DROP 320 (1.1%), PLACE 108 (0.4%), DIG 103 (0.4%), BUILD_PASTURE 56 (0.2%).
56% of ops are movement; PASS is only 4.9%. PLANT 524 across four replays is 131 per replay, matching
66 + 44 + 21 = 131 seeds exactly.

Funding curve, day 0 to day 13, from `data/seed_scripts/new_leader/90016067.json`:
d0 $3,000 (BUY_ANIMALx4, BUY_PRODUCTx16, BUY_SEEDx4, HIREx4, SELLx12) → d1 $42 → d2 $141 → d3 $217 →
d5 $621 → d7 $1,719 (BUY_LANDx1) → d10 $1,278 (BUY_LANDx1, a $2,000 parcel on a $1,278 dawn bank) →
d11 $3,236 → d12 $6,828 → d13 $14,622.
He goes all-in on day 0 and ends it on $42. Early revenue is FERTILIZER — day 1 hour 8 sells
FERTILIZER x4, before milk arrives on day 8. He funds purchases from same-day sales, running at the
edge of insolvency the whole ramp. Wheat is not arbitrage: buys 967 at mean $44.96, sells 1,131 at
$46.49, a 3.4% spread, with 319 units going to FEED.

Public meta, 2026-08-03 notebooks: live prices STRAWBERRY 280, MILK 263, WOOL 235, MELON 54, WHEAT
58, against bases 120/160/200. Three clusters: pure cow ranch (3–10 cows), melon IPO (16 melons + 2
cows, day-10 dump), staged economic herd (`C0x` family, strongest public code): 8 cows, 5 sheep, 5
strawberry plots, 12 hands.
Hands cost per day at 6/8/10/12/14/16 hands: 20/54/143/376/986/2583 coins. Twelve hands costs 376
coins for 288 extra actions, about 1.3 coins each.
Value per action, measured: melon in-window watering ~$250; cow fed+cared ~$95; sheep fed+cared ~$86;
`COLLECT_FERTILIZER` (free, every animal, every day) ~$85; goose fed+cared ~$32; strawberry ~$37;
wheat ~$17.

Our own reference tape, Seb, is `data/seed_scripts/top_guys/90494364.json`, a diagnostic only —
beating it is the goal, not matching it.

What the field says about our numbers: ladder targets go stale in days (a field at 2,700 in four
days keeps climbing); imitation learning off daily top-episode datasets was checked and rejected
because they are ordered by current rating and on 2026-07-31 contained agents near the $3,512
baseline while we banked $43k; self-play pressure is bounded by the pool it plays, and a pool of
frozen $18k-policy copies plus scripts topping $27k demands nothing.

### 1.2 The two private bots beating the public meta (external notebook, 2026-08-09)

Source: `the_top_five_clusters_2026-08-09.md`.
This file carries a SUPERSEDED banner added 2026-08-11: `the_ladder_is_two_scripts.md` (1.3) is the
current position, measured at population scale (2,744 seats). `counter_meta` here (Seb, rank #1 at
3,201.1 in this sample) is the same player whose median bank later halved and who has since
withdrawn from the ladder — see 1.3's "why our schedule is the wrong target" before treating Seb as
the build to imitate.

Shared verbatim by Alex, from a public notebook ("The Two Private Bots Beating Kaggriculture's
Public Meta") plus companion dataset "Cracking Kaggriculture's Top-5: Opening-Move Data". Method: 3
recent replays per top-5 team, actions from the first 48 steps, clustered by opening signature.
Snapshot 2026-08-09.

Three clusters:
`v23_fork` (three top-5 teams, ladder 3,117–3,131): 5 hires, 2 cows + 2 sheep, 7 wheat / 12 melon
seeds, 0 strawberry.
`sheep_first_hybrid` (HealthStone, rank #2, 3,132.9): 3 hires, 1 cow + 4 sheep, 5 wheat / 5 melon
seeds, sheep-first buys.
`counter_meta` (Seb, rank #1, 3,201.1): 14 hires, 3 cows + 2 sheep, 14 wheat / 3 melon seeds,
aggressive labor.
Three of the top five run an identical opening to the public reference agent `kaitofukami v23`,
confirmed by running v23 locally in self-play and matching byte-identical opening actions. That
public agent is a hard ceiling at 3,117–3,131. The two teams above it run nothing public.

Cash on hand, mean of 3 episodes per team, days 0–5:
HealthStone: 3,000 / 14 / 14 / 18 / 26 / 214.
Seb (`counter_meta`): 3,000 / 562 / 353 / 656 / 481 / 766.
`v23_fork`: 3,000 / 22 / 22 / 152 / 417 / 694.
HealthStone front-loads to $14 by day 1 and holds it four days, betting on CARE compounding from a
sheep-weighted herd. Seb keeps a real cushion, $500+ through days 1–5. `v23_fork` is in between.

Final state: land quadrants `v23_fork` 3, HealthStone 3, Seb 4. Cows 8/8/9. Sheep 6/4/11. Total
animals 14/12/20. Avg final coins ~$100k / ~$100k / ~$57k (Seb, still rank 1 in these games).
Seb banks the least money of the three and is rank 1 — the Elo lesson: a $100k win and a $57k win
score the same.

Notebook's read of the edge: `v23_fork` is replicable (copy the public reference, band 3,117–3,131).
`sheep_first_hybrid` needs a redesign around CARE compounding on sheep; the $14-for-four-days cash
constraint is severe. `counter_meta` needs to fund 4 quadrants and 20 animals — "the cash trap is
real (I hit variants of it four times when I tried building toward it heuristically)". Detection is
cheap: the first 48 turns identify an opponent's cluster.

What this means for us, from the source, read with care: our best submission scored 1,123.5 against
a public-meta floor of 3,117 — roughly a third of the way up, not a neighbouring band. The daily
episode index's `median_avg_score` on 2026-08-08 was 3,067.75, `top_avg_score` 3,192.89.
Three things flagged to check rather than assume: our `seb` tape may not be this Seb, or not this
Seb's current play (we beat the `seb` tape 4/4 by $40k–$110k per `scripts/vs_tapes.py`); the opening
we splice from a day-11 handover is worth re-deriving, since all three clusters diverge by day 0;
`counter_meta` runs 14 hires and 20 animals, against our hires measured at the 14th percentile — that
lever was mismeasured, not absent.
The source stresses nothing here is verified by us — it is one notebook's clustering of 15 replays,
3 per team, with visible sampling noise ($57k for a rank-1 agent).

### 1.3 The ladder is two shared scripts (population-scale measurement)

Source: `the_ladder_is_two_scripts.md`, measured 2026-08-11 from 1,372 episodes, 2,744 seats, 40 GB
of replays (`kaggle/kaggriculture-episodes-2026-08-09` and `-08-10`).

Ratings: THUNDER THUNDER (#1) 3,210.9; Victor @ Tufa Labs (#2) 3,149.8; median episode in the
dataset ~3,079; our best submission ever 1,257.9; our submission of 2026-08-11, 845.1.
None of our games appear in the two-day sample at all — 0 of 2,744 seats.

The field is running two scripts. Median values per player (5+ games): nine accounts —
Haramball forever! (n=5, bank 97,828), Natalia Mawyin (16, 94,116), Mohammed Nomaan (23, 94,006),
Dmitry Belan (35, 93,921), Ueddy (25, 90,219), THUNDER THUNDER (111, 90,112), Efe Can Celiksoy (53,
87,378) — all report WHEAT ~143–147 / STRAW 37 / MELON 19 / COW 9–10 / SHEEP 4–6 to a near-unit.
Seven more — Changyuan Chen (11, 93,674), Mohamed abdelrazik (32, 91,682), CemBas (13, 89,846),
SHAURYA SHARMA (32, 89,262), janson (24, 88,990), tao wu11 (10, 88,462) — report WHEAT 108 / STRAW
42 / MELON 24 / COW 8 / SHEEP 6 / buy 266 / sell 305 to the unit.
Not convergent evolution: two shared scripts.

Timing. Script A (wheat ~144): 1 COW + 4 SHEEP on d0, bulk of cows d5–d8, trickle to d19. First
PLANT at d0 turn 6. First SELL d2, median sell day 21.
Script B (wheat 108): ~2 COW + 2 SHEEP on d0, cows d7–d10, sheep d10–d11. First PLANT d0 turn 8.
First SELL d0, median sell day 21.

What separates us from all of them: they plant wheat 108–147 times a season, our schedule plants 24
— wheat's book is starved in all 87 recorded tapes, closing at $40–59 against a $25 base, the one
product the market never saturates. They grow their own feed and sell the surplus; we buy 505 units.
Herd: they run 13–16 head, cow-heavy (COW 8–10, SHEEP 4–6); our schedule runs 21, and on the analysed
loss `SHOP_ADAPT_HERD` bought 16 sheep and 5 cows. Nobody in the top 16 owns a goose. Re-posting: the
field re-posts the same `(item, qty)` on the next turn at 3–7%; we re-post our quota on all 24 turns
of a day — we are the only agent in the sample that does this.

Open-loop, per-day action hashes between games by the same player (one differing turn kills a whole
day, so this is a strict lower bound): Haramball forever! 24/30 identical, janson 21/30, Dmitry Belan
21/30, CemBas 21/30, Mohammed Nomaan 19/30, Efe Can Celiksoy 18/30, Mohamed abdelrazik 17/30, SHAURYA
SHARMA 11/30, THUNDER THUNDER 7/30, Ueddy 5/30. Most of the field is scripted. THUNDER THUNDER, #1,
is the most reactive — two of its same-seat games were only 1.2% identical, diverging at d0h3.
Victor @ Tufa Labs is the opposite: 97–99% of turns identical across seven games on both seats, with
byte-identical season SELL totals. The top two are a reactive agent and a fixed script, at 3,210 and
3,149. Both work.

Does the field adapt to the board? Range across each player's own games, every game a distinct shop
draw: Dmitry Belan (n=35) COW 9..9, SHEEP 4..4, WHEAT 142..143, 35/35 distinct draws. Mohamed
abdelrazik (32) COW 8..8, SHEEP 6..6, WHEAT 108..108, 32/32 distinct draws — 32 games on 32 different
boards, exactly 8 cows / 6 sheep / 108 wheat every time. janson (24) same pattern. THUNDER THUNDER
(111) COW 6..11, SHEEP 4..12, WHEAT 132..152, 108/111 distinct draws. Ueddy (25) COW 6..10, SHEEP
4..11, WHEAT 142..150. Raiden.B (27) COW 1..15, SHEEP 5..19, WHEAT 55..120.
Fixed scripts sit at ~3,100; THUNDER, which floats cow/sheep, is #1 at 3,210. Adaptive herd is worth
roughly 110 rating points. The gap from us to a fixed script is 2,255. Do the base plan first.

Why our schedule is the wrong target: `townCenterSellInterval` went 12 → 24 on 2026-08-08, cutting
the town's drain ~8x. Seb's 16 recorded games split by economy: interval 12 (old, 5 games), median
bank $137,747, COW 5..9, SHEEP 10..15, WHEAT 19..28, STRAW 41..45, MELON 18..24. Interval 24 (now, 11
games), median bank $77,737, COW 5..13, SHEEP 5..20, WHEAT 20..36, STRAW 38..43, MELON 14..25. His
bank halved while he kept the same low-wheat shape, and he has since withdrawn from the ladder.
`data/seed_scripts/top_guys/90976060/schedule.json` — the plan this repo matches op-for-op — is his
interval-12 shape, asking for WHEAT 24 / STRAWBERRY 41 / MELON 17. That is the 845-vs-3,100 gap: not
the planner, the watering, or the market logic — the target. Seb floats COW 5..13 and SHEEP 5..20,
adapting more than the current field.

Best tape to rebase on: Dmitry Belan (35 games, COW 9..9 SHEEP 4..4 WHEAT 142..143 STRAW 36..37) —
near-zero variance, a pure script. Efe Can Celiksoy (53 games, WHEAT 143..146) is an equally clean
second source. Not THUNDER: reactive (7/30 days identical; 1.2% on one same-seat pair) — a sparring
opponent, not a plan to extract.

What was tried on the crop dynamic (`SHOP_ADAPT_CROPS` in `kagg/search/schedule_agent.py`) and why
it is off: `WHEAT<->CARROT` and `TOMATO<->STRAWBERRY` shipped, measured 0.806 vs HEAD's 0.871 over
232 matched games — they swap toward crops the ladder plants 0.2% and 0.0% of the time.
`STRAWBERRY<->MELON` produces an identical 54/4 split on every board tested; no shop carries melon,
so its drain is 29 everywhere. Shared cause: the headroom model treats the town's drain as a cliff
when the price curve is a slope — a melon past its drain still fetches $229 at +50 and $166 at +100.
The fix is to price the marginal unit off `market_price`, and it is unbuilt.

> **Unresolved contradiction, flagged for an owner (not reconciled anywhere since).**
> The 2026-08-11 rebase recommendation in `the_ladder_is_two_scripts.md` (2,744 ladder seats) named
> Dmitry Belan or Efe Can Celiksoy as the target, not Seb.
> No file since has used either target; `REGISTER.md`'s OPEN-10 (this exact item) is not marked
> closed.

### 1.4 The field is a monoculture (2026-08-21, current largest sample)

Source: `the_field_is_a_monoculture_2026-08-21.md`, 2026-08-21, read off `data/action_cache.jsonl`,
1,010 de-duplicated games, plus the live Kaggle leaderboard (5,724 teams, pulled same day).

38 of 58 sampled players share one opening (turns 0–71, before any shop unlocks, both boards
identical, weeds need two unwatered days): peikopon, カワシギ, James Holland, u, Michael Timbs,
StackKnight, Syed Gillani, Bruce, Eddy Despradel, Lucien, Galaxantic, SCLim, HKmgikao, NCK, Utkarsh
#2, Khalid, Ueddy, ReinFARMent, Moshel, TIM, shiggriculture, boatlee, Akhil Chinta, Gekkotron,
automatylicza, Jince, Matteo, One-For-All, Arda Ceylan, hetspookjee, DeeperNet, Dmitry Larko,
RicardoLópez, yaphel lee, ych~sun, Thomas Tschinkel, Atakan Aldemir, katya barzova (unranked), at
ranks spanning 7 to 1288.
Unique openings: Ryo Hasegawa (1), tetsuya (2), Arman Tuganbaev (3), Subramanya N (4), Xiaowenhao404
(11), Seb (15), Kostiantyn (16), Efe Can Celiksoy (18). Izzoudine (5) and Kobe BRYANT (10) share one.
ReCurSiON (13) and Victor @ Tufa Labs (21) share one.
Only the top four ranked players are genuinely distinct agents. The same opening spans rank 7 to rank
1288, so the opening is not what separates them.
We are in the big cluster too — we replay his tape. Most of our ladder games are near-mirrors, so
every arm measured that day reads plus or minus a hundred dollars: against a copy of yourself, small
edges are the only edges available.
Consequence for any opponent pool: sampling players uniformly over-weights the agent with the most
clones. Of the eighteen in `data/opponent_pool_ranked.json`, roughly twelve are the same agent — the
whole "mid" band and most of "low". Effective sample size is about five. Sample over openings, not
players.

His (カワシギ's) d3 decision reads the opponent, not the town. 26 of his games, 325 pairs: where
opponent melon>=9 same AND first-shop same, 0% diverge at d3 (0/21). Opponent melon same, first-shop
different: 0% (0/144). Opponent melon different, first-shop same: 100% (16/16). Opponent melon
different, first-shop different: 100% (144/144). The shop draw makes no difference; the opponent's
melon count decides it outright, split exactly at 9 (`melon_branch.OPPONENT_MELON`). This corrects a
same-day earlier claim that he "re-plans on the shop draw" (65% divergence at d3) — that measurement
conflated the d3 shop unlock with the d3 melon-count decision; this table separates them.

Nobody times the market: SELL quantity against price at a fixed (day, hour) cell across a player's
games, restricted to cells where quantity varies (an earlier version averaged over all cells, 86% of
which hold a constant zero, giving an artifactual +0.00 for everyone). Median r for Ryo Hasegawa (8
games, 556 cells) +0.05; tetsuya (8, 289) −0.06; カワシギ (8, 599) −0.13; Arman Tuganbaev (8, 411)
−0.11; Subramanya N (8, 428) +0.10; Kobe BRYANT (8, 349) +0.00. |r|>0.4 rates 31–44%, |r|>0.7 rates
2–11%, consistent with n=8 noise. No evidence anyone sizes an offer against the book.

Not established (source's own list): whether anyone is opponent-reactive after d3 — the <d3
divergence column is confounded by players resubmitting different agents over weeks; whether the
melon read is really about melon or about how a melon-heavy opponent sells (either way it is
opponent-reaction); whether the clone cluster's 1,245-place spread is tuning, later divergence, or
submission age.

---

## 2. What the leaders actually grow — crop mix, the rebase-target question, our own losses

Source: `what_the_leaders_actually_grow_2026-08-09.md`.
This file carries a SUPERSEDED banner added 2026-08-11: its central conclusion ("we do not need a
new day-0-10 tape", "our schedule already matches Seb's build on the levers that matter most") is
contradicted by `the_ladder_is_two_scripts.md` (section 1.3), which shows the field plants 108–147
WHEAT tiles a season against our 24 — the single largest gap to the field found so far. Seb's tape
was optimal under the OLD `townCenterSellInterval=12` economy; his bank halved and he withdrew.
Read 1.3 first.

20 real episodes from the top of the ladder on 2026-08-08, plus our two named losses (91229682,
91231728), read directly off board state and raw action stream.

Method note, load-bearing: the final-day tile snapshot badly undercounts annual crops — WHEAT, MELON
and CARROT are harvested and often left bare near season end, so a day-29 snapshot can show
STRAWBERRY: 1 for a farm that planted 41 strawberry tiles across the season. This doc reports season
PLANT-op totals (right measure of activity) separately from mid-season snapshots (right measure of
concurrent tile occupancy) and final animal pen counts (reliable as-is, since pens persist).

Table 1, 40 rows (20 episodes × 2 seats): 35 of 40 rows carry the identical signature WHEAT
~103–109, STRAWBERRY 42, MELON 24, COW 8, SHEEP 6, land days [7, 11], identical hire ramp — 18 of 20
episodes are the same public reference agent (almost certainly `kaitofukami v23`) playing itself or
a near-identical relative under a different team name. Only `Seb (allegedly)`'s two rows and its two
direct opponents' rows differ materially: Seb runs STRA:40/MELO:25/WHEA:22, SHEE:15/COW:7 (episode
90850170, bank $88,007, 4 quadrants, WIN) and STRA:43/WHEA:25/MELO:20, SHEE:10/COW:9 (episode
90851845, bank $45,892, 4 quadrants, WIN).

Table 2, our two losses: episode 91229682, seat 0, vs Shivam_2212, LOSS, bank $61,427 vs opponent
$94,412, 4 quadrants; season PLANT ops STRAWBERRY:41, WHEAT:24, MELON:16; final tile snapshot
STRAWBERRY:1 (Method note applies); final animal pens COW:13, SHEEP:8; land days [4, 6, 12].
Episode 91231728, seat 1, vs As Wasti, LOSS, bank $89,433 vs opponent $98,581, 4 quadrants; season
PLANT ops identical STRAWBERRY:41, WHEAT:24, MELON:16; final animal pens COW:9, SHEEP:7; land days
[4, 6, 16]. Both loss episodes carry identical season PLANT-op totals matching the totals baked into
`submission/main.py`'s `_PLAN_JSON` (STRAWBERRY 41, WHEAT 24, MELON 17 — one plant short of an exact
match): our live planner, after the tape hands over, adds almost no new planting for the rest of the
season.

Who beat us: 91229682's `Shivam_2212`, season PLANT ops MELON:24, WHEAT:108, STRAWBERRY:42 — the
exact same signature as the 18-episode mirror baseline. We lost to the plain public reference script
by 34% ($61,427 vs $94,412). 91231728's `As Wasti`, season PLANT ops CARROT:40, WHEAT:79, MELON:20,
STRAWBERRY:18, TOMATO:6 — a five-crop build including CARROT and TOMATO, present in zero of the 40
leaders_0808 rows. Beat us by 9% ($89,433 vs $98,581). Neither opponent that actually beat us
resembles Seb.

Table 3, per-player win rate, 20-episode sample, mirror-match caveat applied: Seb (allegedly) n=2,
100% win, mean bank $66,950. Yvonne. n=1, 100%, $78,814. onlysmrtsumx n=1, 100%, $68,167. Mohit Rao
n=1, 100%, $88,958. kakuteki n=11, 91%, $73,584. BHackers n=7, 57%, $74,377. Wufang Hong n=3, 33%,
$83,969. Akhil Chinta n=4, 0%, $68,611. Leon Christians n=2, 0%, $65,176. Dandan Li n=2, 0%, $86,232.
╰┈➤ˎˊ˗ www.sleepyai.org n=1, 0%, $88,917. venks n=1, 0%, $34,500. ArturoSirvent n=1, 0%, $105,743.
Knight of Favonius n=1, 0%, $92,656. Sasha Turutin n=1, 0%, $89,872. Yoganjaneyulu n=1, 0%, $109,728.
Seb's mean bank ($66,950) is the lowest of the four 100%-win-rate rows and lower than eight of the
eleven 0%-win-rate rows: ArturoSirvent banked $105,743 and lost, Yoganjaneyulu banked $109,728 and
lost. Money and outcome are visibly decoupled.

Table 4, mix by result pooled across all 40 leader rows (dominated 18:2 by the mirror baseline, "close
to uninformative on its own"): WIN (n=20) seeds bought WHEAT 1,993, MELON 477, STRAWBERRY 839 (60/25/14%
mix); animals COW 160, SHEEP 133. LOSS (n=20) seeds bought WHEAT 2,163, MELON 480, STRAWBERRY 840
(62/24/14% mix); animals COW 160, SHEEP 120.

Table 5, land days and hire ramp, WIN rows: the mirror baseline is uniformly land_days=[7, 11],
hires(d0-14)=[5,0,2,1,4,1,2,8,5,7,8,14,7,11,7]. Seb (90850170) is land_days=[4, 6, 10],
hires=[7,7,7,7,7,7,4,8,9,10,11,12,12,12,12]. Our two losses: 91229682 hires(d0-19)=
[7,7,7,7,7,7,8,8,9,11,12,12,12,12,12,12,12,12,12,12]; 91231728 identical. Our crew ramp is almost
identical to Seb's (front-loaded to 7 on day 0, ramping to 12 by day 10) and land timing matches
closely (our losses bought on [4,6,12] and [4,6,16] against Seb's [4,6,10]) — a lever already copied
correctly.

Table 6, selling patterns: all-win-seats pooled table dominated by the mirror baseline's larger
production base, not apples-to-apples; isolated per-build instead. v23-clone baseline (kakuteki,
90849277 seat0): STRAWBERRY 32 orders/32 per ep/320 units/$15.1 mean; WHEAT 40/40/305/$37.9; MILK
46/46/214/$19.5; FERTILIZER 29/29/212/$59.7; WOOL 19/19/148/$248.0; MELON 9/9/144/$98.4.
Seb (allegedly), both episodes: FERTILIZER 214 orders/107 per ep/638 units/$52.7; STRAWBERRY
92/46/567/$19.2; WOOL 90/45/487/$200.7; MILK 75/37.5/386/$111.9; MELON 33/16.5/264/$85.4; WHEAT
13/6.5/148/$36.0. Our two losses: WHEAT 463/231.5/1,658/$45.6; FERTILIZER 244/122/550/$54.2;
STRAWBERRY 92/46/534/$169.3; MILK 102/51/438/$166.1; WOOL 51/25.5/294/$58.7; MELON 19/9.5/152/$172.6.
Our wheat order-count gap (231.5/ep vs Seb's 6.5 and the mirror baseline's 40) does not read as a
pricing problem — our realized wheat price ($45.6) is higher than both comparisons, matching the
existing `we_oversell_into_a_contested_book_2026-08-09.md` verdict that cutting wheat supply gains
nothing; the source explicitly says do not read the order-count gap as a new finding, and points
instead at MILK/STRAWBERRY/WOOL oversold into thin books as the real money (recoverable by scaling
those three to 0.5–0.7x).

Table 7, op census: all-win-seats PASS 20,254 (15.0%), WEST 18,646 (13.9%), WATER 17,830 (13.2%),
NORTH 17,415 (12.9%), EAST 13,378 (9.9%), SOUTH 11,101 (8.2%), HARVEST 7,072 (5.3%), CARE 6,246
(4.6%), FEED 6,213 (4.6%), COLLECT_FERTILIZER 6,083 (4.5%), PLANT 3,294 (2.4%), PICKUP 3,004 (2.2%),
FERTILIZE 1,654 (1.2%), DROP 1,330 (1.0%), DIG 494 (0.4%), PLACE 313 (0.2%), BUILD_PASTURE 293 (0.2%).
Our loss seats: PASS 3,258 (21.6%), WEST 1,992 (13.2%), NORTH 1,753 (11.6%), EAST 1,328 (8.8%), WATER
1,168 (7.7%), SOUTH 1,072 (7.1%), COLLECT_FERTILIZER 836 (5.5%), CARE 799 (5.3%), FEED 765 (5.1%),
HARVEST 659 (4.4%), PICKUP 658 (4.4%), DROP 351 (2.3%), PLANT 162 (1.1%), FERTILIZE 155 (1.0%), DIG
61 (0.4%), BUILD_PASTURE 42 (0.3%), PLACE 41 (0.3%). Our PASS share (21.6%) is well above leader
average (15.0%); our WATER share (7.7%) is well below it (13.2%) — we idle more and tend crops less
proportionally. Consistent with an earlier footnote on these same two episodes: our two actual
opponents plant roughly twice what we do over the season (174 and 163 vs our 81 each) while passing
far less. Not explained by crop tile mix — idle capacity: turns spent doing nothing instead of
watering or replanting.

Table 8, final animal pen totals across WIN rows: COW [7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9] mean
8.0. SHEEP [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,10,15] mean 6.7. GOOSE all zero, mean 0.0. Our
losses: 91229682 COW=13 SHEEP=8 GOOSE=0; 91231728 COW=9 SHEEP=7 GOOSE=0. Every real herd — Seb's
included — stays well under the corrected saturation model's 16/16 flat point for cow and sheep, and
nobody fields a goose.

Table 9, season PLANT-op totals across WIN rows: MELON n_nonzero=20/20, values 20–25, mean 23.9.
STRAWBERRY 20/20, values 40–43, mean 42.0. WHEAT 20/20, values 22–108 (mean 98.9, bimodal: mirror
baseline ~103–108, Seb 22/25). CARROT and TOMATO 0/20. Our losses: STRAWBERRY:41, WHEAT:24, MELON:16
both episodes. CARROT and TOMATO are planted by zero of the 40 leader seats but planted by one of our
two actual opponents (As Wasti, CARROT 40 + TOMATO 6) — the field this sample describes is not the
whole field.

Cross-check against the saturation model (8 melon tiles, 16 cows, 16 sheep, 8 geese), mid-season
snapshots day 15/20: v23-clone (kakuteki) WHEA:7 STRA:42 MELO:12 COW:8 SHEE:6 at both days. Seb
(90850170) day15 MELO:18 STRA:39 WHEA:1 SHEE:14 COW:7, day20 MELO:7 STRA:40 WHEA:1 SHEE:15 COW:7.
Seb2 (90851845) day20 MELO:8 STRA:43 WHEA:1 SHEE:10 COW:9. Our loss1 (91229682) day15 MELO:13
STRA:40 WHEA:1 COW:13 SHEE:8, day20 MELO:3 STRA:40 WHEA:1 COW:13 SHEE:8. Our loss2 (91231728) day20
MELO:3 STRA:41 WHEA:1 SHEE:7 COW:9. Melon concurrent tiles range 3–18 (cycles through plant/harvest),
bracketing the model's 7.3–8 tile estimate reasonably. Strawberry sits at 39–43 tiles for every
single build in this cross-check, including ours — the most stable number in the dataset. Wheat
concurrent tiles are ~1 for everyone at mid-season despite the mirror baseline's 108 season
PLANT-ops — wheat is replanted in small frequent batches, not held as standing acreage.
Cow/sheep counts never approach the model's 16-head flat point for anyone here. The model's claim
that a cow's flat-max value ($1,164/head) exceeds a sheep's ($897/head) is not contradicted by head
count, but sits in tension with Seb's ratio — the only consistently-winning build runs more sheep
than cows (15:7, 10:9), while our schedule and both losses run more cows than sheep or near-even
(13:8, 9:7). Flagged as an open, unresolved tension, not resolved in this document.

Answer given (now superseded, see banner above): no new day-0-10 tape needed, based on (1) our own
planner driving from day 0 loses 0/6 seeds while the Seb-tape opening wins 4/6 (from
`we_oversell_into_a_contested_book_2026-08-09.md`), (2) our schedule already matches Seb's build on
land days, crew ramp, strawberry tile count, and (3) `geometry_of_the_herd_2026-08-09.md` already
ruled out pen placement and walking distance as the cost, on these same two loss episodes.
Concrete next steps proposed: test shifting herd allocation toward sheep (parameter change, not new
tape) — explicitly flagged as untested and in tension with the scheduler's own per-head economics;
investigate why post-handover planting volume is near zero after day ~12 while real winners plant
double; apply the already-quantified MILK/STRAWBERRY/WOOL oversell fix.
Gaps flagged: n=2 for Seb, n=2 for our losses — indicative, not precise; herd-ratio tension
unresolved; realized-price numbers use market snapshot at order time, not confirmed fill price; the
"idle after day 12" cause (hand capacity, land, or scheduling logic) was measured as present, not
diagnosed.

---

## 3. Kawashigi: the board, the algorithm, and what generalises

### 3.1 One fixed board; he is not replaying a tape (2026-08-13)

Source: `kawashigi_one_board_2026-08-13.md`. Carries a note added 2026-08-22: a later file,
`marginal_units_and_the_shared_book_2026-08-16.md` §9, found the shop draw is endogenous to which
agent plays (weed-spawn RNG is consumed per-tile before the shop draw, so a different agent's moves
shift it) — this qualifies the "seed's only job is the shop draw" framing for a fixed opponent
script but does not overturn the board-is-fixed finding below. Not reconciled in either file.

16 episodes of カワシギ (current #1) plus four of our own games. Hashing the opening observation
with `farms`, `step`, `remainingOverageTime` stripped: world hash dc0d81c5 (1 distinct across all 16
Kawashigi games), market a7e792b0 (1 distinct), tiles bb3b18da (1 distinct, identical for both
seats). Our own five games carry the same three hashes. The seed's only job is the shop unlock draw,
first firing on d3. A ladder game has exactly two variables: the shop sequence and the opponent. This
retires "seed variance is ~15%" as a claim about the ladder — that figure is about `kagg.arena`'s
randomly drawn boards, not the ladder's one fixed board.

He is not replaying a tape: pairwise action-vector identity over 16 games on the same board runs
26%–82%. Distinct action-vectors per hour: d0–d2, d4, most of d5–d6 are 16/16 (modal 16.0/16); d3
drops to modal 12.2/16; d7 modal 9.8/16; d10 modal 8.3/16; d16 modal 5.0/16; d20 modal 3.4/16; d24
modal 1.9/16; d29 modal 2.8/16. All 16 games are byte-identical for the first 74 turns (d0 through
d3 h1); fan-out starts d7; by d24 the modal action is shared by fewer than 2 of 16.
The 74-turn deterministic prefix ends exactly at the first shop unlock (`townShopUnlockInterval = 3`,
`kaggriculture.py:854,878`, first draw on d3). All 16 games drew a different 3-shop sequence at d3
(16 distinct sequences listed in the source, e.g. 2407: ICE_CREAM_SHOP/BAKERY/YARN_STORE; 8785:
YARN_STORE/PET_CAFE/PIZZA_SHOP). Divergence is the shop draw, not the opponent — same-opponent pairs
diverge as early as d5 h15, different-opponent pairs stay identical to d9 h6.
The leader re-plans around the shop draw from the moment it lands, reaching the whole plan. Our own
`SHOP_ADAPT_HERD` starts at d6 and reads only shop presence to float a cow/sheep split.

Two structural constants: hour 1 is identical in all 16 games right through to d23. Hour 0 is the
most divergent hour of the day from d14 on — a dawn decision that reads state, then a stable walk.
Record: 15-1 across the 16. Single loss 92445172, $88,448 vs Yusuke Hayashi's $89,993, a $1,545
margin. Money range $44.9k–$150.0k on an identical board — the size of the swing the opponent alone
produces.

### 3.2 Kawashigi's algorithm — three phases, with a major retraction the same day

Source: `kawashigi_algorithm_2026-08-21.md`. Carries a RETRACTED banner at its own top (same day):
the middle is NOT board capacity, per `the_middle_is_not_board_capacity_2026-08-21.md` (3.3) — he
leaves 6+ tiles empty on 85.7% of mid-season days and could afford the seed on 100% of them,
`corr(wheat, free_at_dawn) = 0.274`, `corr(wheat, ever_free_that_day) = 0.507`. What binds is the
turn budget: 53.6% of his day is travel, 31.9% of work is watering, 5.6% is planting, 43.4% of days
have zero idle unit-turns. "Plant every reachable tile" would roughly double his plant count with no
turns to do it. The crop-mix half of this document survives unchanged; the claim that d14–d27 needs
no row library is not disproved but is now unsupported.
Also retracted: the sample is 213 game-seats, not 228 (167 episode ids sit in more than one directory
under `data/seed_scripts/`, so fifteen games were read twice; the shape of the tables is unaffected,
exact counts are not).

Measured on 228 game-seats (see correction above: 213 distinct), `data/target_rows_kawa_norm.json`
(6,840 day-rows). Result in one line: his season is a fixed opening, a wheat-fill middle, and a fixed
close; the middle is "plant wheat on every tile you can reach today", tile count a property of the
board (later retracted).

How the label was wrong four times: the executor (`kagg/search/schedule_agent.py`) reads exactly ten
keys — seeds, hands, buys, sells, land, plants, shed_dusk, places, hires, animals_bought — never
builds, feeds, cares, harvests, fertilises, or clears (the router re-derives those six live). Removing
fields from the label and measuring distinct rows at d16: nothing removed → 127; movement/watering
already out; herd species COW/SHEEP/GOOSE removed → 127 (the herd algorithm reads the shop draw);
the six derived fields removed → 125 (nearly nothing); sells/buys removed → 80; places/animals_bought
removed → still counted with herd; seeds removed → 10 (the one that mattered: d16 47→10, d20 53→13,
d25 170→60). Species normalisation removed 15 rows out of 6,840, all on d9 and d11.

What varies per phase, 228 seasons, crop multiset only: d0–d2 1 distinct; d3 1 (2 with seeds, the
melon split); d4–d6 2–4; d7–d13 6–30 (genuine per-day variation); d14–d21 6–24 (wheat only, count
varies); d22–d26 34–60 (wheat + 0–2 CARROT); d27 17; d28 1; d29 1.
Day 16 distribution across all 228 seasons: WHEAT:5 (72), WHEAT:8 (47), WHEAT:9 (31), WHEAT:4 (29),
WHEAT:6 (20), WHEAT:7 (14), WHEAT:11 (5), WHEAT:12 (4), WHEAT:10 (4), WHEAT:3 (2) — a contiguous
unimodal run. Day 22 and 25 are the only mid-season days with a second crop, 1–2 CARROT (e.g. day 25
top rows: CARR:2 WHEA:10 | CARR:1 WHEA:10 | WHEA:11 | CARR:2 WHEA:6). No melon, tomato or potato
anywhere in the middle.

Proposed design (partly retracted, see banner): d0–d6 library rows (1–9 distinct, lookup); d7–d13
library rows or small tree (12–30 distinct); d14–d27 greedy planner, crop pinned to WHEAT, no library
needed (this specific claim is what 3.3 retracts); d22–d26 + 1–2 CARROT, trigger unknown; d28–d29
library rows (1–7 distinct, already shipped); all days, animals substituted by the herd algorithm
from the live shop draw.
Not established, per the source itself: the wheat-count-as-board-capacity claim is asserted from
distribution shape, not measured against free/reachable tiles — "the single most load-bearing
unverified claim in this document" (and it turned out false, see 3.3); the d22–d26 carrot trigger is
unknown; whether `seeds` is genuinely derivable from `plants` plus the shed; Ryo Hasegawa and tetsuya
are measured separately and Ryo is already known to differ (no geese, Q3 not Q4, wheat 70%/carrot
54%/tomato 25%).

### 3.3 The middle is not board capacity (retraction and replacement of 3.2's core claim)

Source: `the_middle_is_not_board_capacity_2026-08-21.md`. 2,982 day-rows, d14–d27, 213 distinct
game-seats (see 3.2's n-correction).

The count against the board, per-day table (day, n, planted, wheat, dawn free, everfree, h12 free,
dusk free, seedcap, money), selected rows: day 14, n=213, planted 2.11, wheat 2.11, dawn 5.76,
everfree 10.16, h12 5.76, dusk 8.06, seedcap 10.10, money 14,949. Day 25: planted 11.25, wheat 9.80,
dawn 10.27, everfree 19.52, h12 11.37, dusk 8.27, seedcap 17.73, money 71,740. (Full 14-row table in
source.)
Pooled d14–d27, 2,982 day-rows: planted == ever_free 8.2% (planted every tile the board offered);
wheat == ever_free 6.9%; wheat == free_dawn 7.9%; dusk == 0 8.2% (board full overnight); dusk >= 3
72.7%; mean tiles left empty at dusk 7.48. Correlations: corr(wheat, free_dawn) 0.274, corr(wheat,
ever_free) 0.507, corr(wheat, free_by_h12) 0.327, corr(wheat, seed_cap) 0.921 (not evidence — he buys
what he's about to plant, so this is downstream), corr(wheat, units) −0.273, corr(wheat, money_dawn)
0.388, corr(wheat, unlocked) 0.078. 2,738 rows left a tile empty overnight; 2,738 (100.0%) could have
afforded the seed for every one of them at dawn — money is not the constraint (wheat seed is $10,
mid-season bank $15k–$79k).

The h23 read is biased (planting is back-loaded — 16.4% of all mid-season PLANT ops fire at h23,
68.7% at h18 or later), so `dusk` overstates the empty count. Bias-free version, min free-tile count
over 24 hourly observations: mean min_free 6.18 vs mean h23_free 7.48 — a 1.3-tile bias. min_free ==
0 (board full at some hour) 14.3%; min_free >= 3, 58.0%. The board is never full at any hour of the
day on 85.7% of his mid-season days, and on 58.0% it never drops below three empty tiles.

He was not idle, per-day budget/idle/travel/work/plant/water/dusk table (selected): day 14, n=213,
budget 208.0, idle 10.0, travel 105.0, work 93.0, plant 2.11, water 30.44, dusk 8.06. Day 24: budget
271.0, idle 0.3, travel 143.3, work 127.4, plant 6.54, water 38.18, dusk 9.63. (Full table in
source.) Pooled: mean idle unit-turns per day 5.01; days with zero idle turns 43.4%; idle share of
budget 1.8%; travel share of budget 53.6%; WATER share of all work 31.9%; PLANT share of all work
5.6%. The count is bounded by the turn budget, not the tile count — a property of his routing, not
the board.

What predicts the count — nothing well: corr(wheat, tiles freed today) 0.598, exact match 15.7%;
corr(wheat, HARVEST ops today) 0.277, exact match 1.2%; corr(wheat, WHEAT tiles at dawn) 0.197, exact
match 0.2%; corr(wheat, wheat planted d-1) 0.181, exact match 9.7%. Not a per-season constant either:
grand mean wheat/day 6.45, between-season SD of means 0.71, mean within-season SD 3.57, within/between
ratio 5.03 — the day-to-day spread inside one season is five times the spread between seasons.

Killed: "the number of tiles is a property of the board" and "plant wheat on every tile you can reach
today" as a specification (applied literally it would roughly double his plant count — mean 6.45
against mean everfree 14.4 — with no turns for it; his day is 98.2% committed with a third of the
work going to WATER).
Not killed, still unverified: whether d14–d27 needs no row library — the count is turn-bounded rather
than menu-selected (consistent with a planner producing it), but it would be our router's turn budget
setting the number, and nothing measures whether those agree.
Holds: the crop-mix half of the claim — planted == wheat exactly on d14–d20 and d27; d21–d26 carry
1–2 CARROT and nothing else; no melon, tomato or potato in the middle.
Correction to source doc's n: `data/target_rows_kawa_norm.json` has 228 rows per day but only 213
distinct game-seats — 15 duplicated, counted twice in every distinct-row and coverage figure in
`kawashigi_algorithm_2026-08-21.md`. The effect on those tables is small but they are not measured on
228 independent seasons.
Unverified: whether our own planner's turn budget produces a wheat count near his; why he leaves 6+
tiles empty (turn saturation is consistent with it, not proof of intent); everything here is
Kawashigi alone.

### 3.4 The opening is a tape; the middle is two regimes, not one

Source: `the_opening_is_a_tape_the_middle_is_two_regimes_2026-08-21.md`. 213–226 game-seats depending
on the cut.

d0–d12 is EXACT with a one-line fix: `REPLAY_OPENING_DAYS = ()` → `(0,1,...,12)`. Per-day differing
cells (`scripts/breakdown.py --tape kawashigi --days 30 --diff`, seed 11, weeds 0.0, shop draw
injected): d0..d12 all 0; d13..d29: 10, 11, 11, 13, 12, 11, 11, 11, 14, 14, 14, 15, 15, 12, 16, 16,
10. Alex was right repeatedly that "there is nothing in the logic to change or decide we are using
the tapes" and "there are NO problems till d12" — a whole day went into debugging days that contain
no decisions, because `_replay_opening` sends his own actions and none of them arise. The machinery
had been disarmed on 2026-08-20 for a reason that no longer applied (the agent was pointed at tetsuya
while replaying カワシギ's turns); it reverts to `()` if the agent is ever pointed at tetsuya again.
Verified on one of four branches: `(False, False)`, the melon three-quadrant tape 92498144. The other
three combinations are untested; `(True, True)` points at a three-quadrant tape that buys its fourth
parcel during d12, now questionable.

The decision tree is two binary reads, both already implemented: d3 `melon_branch`, opponent melon
tiles >= 9 → strawberry line, 0 misclassifications / 67 games; d6 `q4_branch`, YARN_STORE unlocked by
d6 → four quadrants, fires on 15 of 100 seeds. `q4_branch` has never measured as a gain — its own
docstring records −$4,626 mean on own routes, +$465 on live routes, −$2,749 on unselected seeds; it
is armed on Alex's judgement.

The middle is two regimes: depth-3 tree, dawn board only, `my_seed_*` dropped, split by GAME, 64
held-out games. Selected rows (day | sets | base% | tree% | gain | multi | base% | tree% | gain):
d13 | 3 | 68.8 | 96.9 | +28.1 | 20 | 25.0 | 70.3 | +45.3. d15 | 1 | 100.0 | 100.0 | +0.0 | 12 | 23.4 |
59.4 | +35.9. d18 | 2 | 98.4 | 98.4 | +0.0 | 21 | 25.0 | 48.4 | +23.4. d21 | 4 | 64.1 | 70.3 | +6.2 |
41 | 4.7 | 6.2 | +1.6. d25 | 2 | 76.6 | 75.0 | −1.6 | 51 | 1.6 | 1.6 | +0.0. (Full 15-row table in
source.) The count is learnable d13–d18 and dead from d19 (+45, +42, +36, +13, +28, +23, then
nothing). Which crops is nearly free (d15, d16, d19, d27 single class); only d13 has a real crop
choice the tree wins (68.8% → 96.9%); d21–d26 gains of +1.6 to +6.2 on 64 games are noise.

This reconciles the capacity finding (3.3) rather than contradicting it: the pooled corr(wheat,
free_tiles_at_dawn) = 0.274 measurement was correct and pooled over fourteen days of which six carry
real signal and eight carry none — the same trap as the `farm:0.445` per-opponent win rate, an
aggregate over a non-uniform unit. The d13 rule, board-only, depth 3: `my_empty <= 5.5` then
`my_shed_WHEAT` thresholds at 29.5/34.5 select straw+wheat / wheat / straw; `my_empty > 5.5` then
`my_crop_STRAWBERRY` threshold 41.5 and `my_shed_FERTILIZER` threshold 24.5 select among straw+wheat /
straw / wheat. With `my_seed_*` included the tree reaches 98.4% on `my_seed_STRAWBERRY` alone, but
that seed was bought on d12 (a decision already paid for); dropping seed features costs only 1.5
points, evidence the board carries the information independently.

Where the season is lost, full 30-day grid from an exact d12 handover, ours minus tape: season money
−$11,544, wheat −89 tiles, sell −126, work +236, move −315, idle +171, buy_product −108. We do more
work in a smaller radius, hold 89 fewer standing crops, trade far less, and sit idle 171 more
unit-turns than he does. d22 alone is −$4,508 on sell −72. d13–d18, the over-planting window, is
exactly where a tree can supply the count.

Not established: three of four tape branches untested at d12; one seed, one opponent, one shuffle of
the holdout — the +40s are clear of noise, the +1.6s are not; whether feeding the tree's count to the
planner actually fixes the 158-vs-112 over-planting is proposed, not measured; the season grid is our
shipped agent against the tape's own game and says nothing about a contested market against a
different opponent.

### 3.5 Does the wheat-fill middle generalise? Ryo and tetsuya vs Kawashigi

Source: `ryo_tetsuya_vs_kawashigi_2026-08-21.md`. Sample as first reported: 228 カワシギ, 145 Ryo,
117 tetsuya rows per day — inflated by duplicate episode ids across `data/seed_scripts/` directories.
Corrected distinct game-seats: カワシギ 213 (15 copies), tetsuya 106 (11 copies), Ryo 109 (36
copies — a quarter of his rows). Duplicates land in the same cross-validation fold (split on
(game, seat)), so this is not train/test leakage, but it silently reweights duplicated seasons; the
purity/shape means are barely moved, the distinct-multiset counts are approximate.

Answer: two of the three have it. Kawashigi and tetsuya both play a mid-season of one crop with a
varying count; Ryo plays a real crop mix all the way through.
Purity/shapes table by day (selected): d14 カワシギ 100%/2, tetsuya 100%/2, Ryo 81%/6. d15 100%/1,
100%/3, 86%/7. d18 100%/3, 99%/3, Ryo 53%/7 (his lowest). d26 92%/2, 98%/2, Ryo 100%/1. d27 100%/1,
98%/3, Ryo plants nothing. (Full 14-row table in source.) tetsuya is cleanest: 96–100% wheat d14–d27
with no carrot phase at all. Kawashigi is pure wheat d14–d20, then 1–2 CARROT d21–d26, then pure
wheat d27. Ryo never gets above 86% after d13, dropping to 53% at d18.

Season crop totals: WHEAT カワシギ 67.7%, tetsuya 71.6%, Ryo 68.0%. STRAWBERRY 21.0% / 19.8% / 14.7%.
MELON 8.1% / 6.8% / 5.6%. CARROT 3.2% / 1.5% / 10.2% (Ryo's separator). TOMATO 0% / 0.4% / 1.5%.

Openings do not agree: d0 カワシギ MELON+WHEAT 19 plants, tetsuya STRAWBERRY+WHEAT 13 plants, Ryo
MELON+WHEAT 17 plants; all three have a single fixed d0 (1 distinct multiset). d1–d3: カワシギ plants
nothing, tetsuya nothing then MELON:3 at d3, Ryo WHEAT 1–3 then nothing at d3. d4–d8: all three
STRAWBERRY / MELON-then-STRAWBERRY / STRAWBERRY. Planting ends d28 (カワシギ, tetsuya) or d27 (Ryo).

What this changes: the three-phase structure (fixed opening, scalar middle, fixed close) is not
Kawashigi's quirk — two independent strong players do it. Copying the middle from any of them is the
same act: pin the crop to WHEAT and let the planner fill; nothing player-specific to copy there. The
opening is where they differ and is small enough to hold as a library (1–9 distinct rows to d6). Ryo
is the wrong teacher for the middle; he is the interesting one for carrot, if carrot turns out to pay.

Correction recorded: an earlier read of Ryo on a 9-seat sample showed 87–100% mid-season purity and
was reported as "already looks the same"; the full 145-seat sample gives 53–86%. Cause: a shell
`DIRS=$(ls ... | tr ...)` — `ls` failed but the pipeline's exit status came from `tr`, so `&&` did not
catch it and extraction silently read one directory instead of 31. A pipeline's exit status is the
last command's.
Not established: whether the mid-season count is board capacity for any of the three (measured
separately, see 3.3); what triggers Kawashigi's d21–d26 carrot, or Ryo's carrot generally; whether
Ryo's mix beats the wheat-fill — nothing here compares outcomes.

---

## 4. Day blocks, the arm classifier, and the library agent

### 4.1 Day blocks: the season is a decision tree with a shallow root

Source: `day_blocks_2026-08-20.md`. Written on branch `day-blocks`; `bundle-head` holds separate
per-turn BC work, untouched.

Headline: a depth-4 decision tree picks a strong player's exact day-block on a game it has never
seen, 83.6% of the time at d6 and 58.2% at d12, and nothing from d17. The unit of decision is the
DAY, not the turn — the single most important finding, because the per-turn BC student trained the
same day is per-turn and cannot express a day plan at all. `submission/main.py:13580` builds
`_AGENTS[me]` once at d0 h0 and reuses it for all 720 turns; the route is planned once at h0 and
executed for 24 hours, so the teacher's action at h13 is a function of a plan made at h0, while the
student sees only the board at h13 with `GLOBAL_FEATURES = 60` containing no plan and no history.
Two different tours can leave an identical board at h13 and need different next moves — an
observability gap, not a tuning gap, and DAgger cannot fix it (it corrects distribution mismatch, not
missing state).
Measured consequence, `bc_bundle.best.pkl`, real environment, 4 games: W/D/L 0/0/4, student bank mean
$438 vs teacher $141,812; turns with orders 5.8% (teacher 21.1%); PASS 83.7%; legality clean (0
slot-order errors, 0 bad quantities, 0 malformed). Held-out per-decision agreement was good — 0.888
bundle agreement on trading turns, up from 0.000 untrained — it learned the mapping, not the
trajectory.

How big is a day library? カワシギ, 228 seasons, animal ops stripped: d0 2 distinct blocks (84.2% top
share, 2 blocks to cover 90%); d1–2 1 distinct (100.0%, 1); d3 9 (46.9%, 3); d5 13 (37.7%, 6); d7 35
(23.7%, 16); d10 46 (16.2%, 25); d12 47 (19.7%, 26); d15 97 (8.8%, 75); d18 182 (3.9%, 160); d21 204
(0.9%, 182); d29 212 (0.9%, 190). d0–d2 is one block; by d21, 204 distinct blocks across 228 games —
every game unique.

Can it be predicted, held-out games, depth-4 tree, 150 train / 63 held out, split by game: d3 8
classes, 56.7% baseline, 83.6% tree, +26.9%. d5 12 classes, 44.8%, 77.6%, +32.8%. d6 22 classes,
26.9%, 83.6%, +56.7%. d7 30, 29.9%, 65.7%, +35.8%. d9 34, 25.4%, 73.1%, +47.8%. d12 43, 22.4%, 58.2%,
+35.8%. d15 78, 7.5%, 29.9%, +22.4%. d17 123, 4.5%, 6.0%, +1.5%. d18+ 131+, 3.0%, 3.0%, +0.0%. The
cliff is d17: from d3 to d16 the tree beats a constant by +12% to +57% every day.

The criteria at d5, root split from 64 candidate features: opponent melon acreage at 8 tiles, then
market wheat inventory, opponent money, shop plant slots, our carrot seed, their cow and sheep counts.
Opponent state dominates — the market is shared and no shop buys MELON (absent from every `SHOPS`
entry), so melon revenue is base-market only and priced by the opponent's acreage. A d3 melon
commitment (80 a seed, first yield d10-12) is the largest irreversible bet in the game.

Shops: identity is useless, the abstraction is not. 8 shops drawn with replacement every 3 days
(`MAX_SHOP_INSTANCES = 8`). At 1 draw: 8 shop multisets, 5 (animal,plant) classes, 4 "which animal"
classes. At 5 draws: 792 multisets, 71 classes, 8 which-animal. At 8 draws: 6,435 multisets, 173
classes, 8 which-animal — saturating by the third draw. "Plant friendly or animal friendly" collapses
6,435 configurations into 8 animal classes. Each animal product has exactly one source: EGG from
BAKERY/BRUNCH_SPOT → GOOSE; MILK from PIZZA_SHOP/ICE_CREAM_SHOP/SMOOTHIE_SHOP → COW; WOOL from
YARN_STORE → SHEEP.

Measured nulls recorded so they are not re-derived: stripping animal ops changes almost nothing
(Kawashigi d8 3.2→3.2 blocks per group, tetsuya identical every day, only ReCurSiON's d16/d18 reach
1.0) — generating the herd by rule still shrinks the library, but it is not what makes a day matchable;
variation is in plant and route work. More tape sources do not make a smaller library: across 76
distinct players there are 52 different day-0 blocks and the most common covers 11.8%; one strong
player is one block per day, the field is 52 alternatives. There is no seat advantage in selling:
`_process_market` settles SELL/BUY in per-unit lockstep ("both players see the same pre-commit
inventory for this unit"); only HIRE and BUY_LAND are handled in player order and those do not
contend — worth pinning since the parity gate never exercised this (300 episodes without both
players selling the same product).

Four wrong field names cost a session, each producing a clean and plausible fabricated result:
`row["action"]` (labels use `act`) gave "1 distinct block per day for all 29 days"; `obs["unlocked_shops"]`
(labels use `shops`, replays use `town.unlocked_shops`); `"MELON" in t` on a replay tile (tiles are
dicts, not strings, so melon was always 0); consequently the first split table read 16.0 blocks per
group — not "features do not explain it" but "no features were measured". All four now raise instead
of defaulting. Blocks-per-group is an in-sample statistic and flatters a finer key: at d18 there are
182 distinct blocks and the moving key reported 2.1 per group (~87 groups over 228 games) — why the
tree exists.

Not established: the library is Kawashigi's, so copying it copies his strategy, not necessarily a
winning one (these downloads are selected losses); every number is measured on completed games, so
whether a block still works against a different opponent is untested (and the opponent is precisely
what the melon signal is about); `HERD_GEESE = 0` was measured while `SELLABLE` held six of nine
product names and EGG was not one of them (`main.py:9961`) — void, and `SELLABLE` is now complete, so
this asks for a fresh measurement rather than a hand-tune.

The new #1: Ryo Hasegawa, nine games downloaded 2026-08-20 23:02 (episodes 95029938–95381518), six vs
tetsuya, two vs Arman Tuganbaev, wins seven of nine by margins 1,760–14,163 (nine selected games
cannot support a win rate). His first five days are a frozen 120-turn unit script: d0 8 pairs unit
ops identical; d1–d2 identical but 2 turn-pairs differ in market orders only; d3–d4 identical; d5 0.8
differing unit-slots per pair; d6 34.8 per pair. Every move, plant and water identical across nine
games regardless of opponent or shop draw — in a five-day window where he varies nothing else,
selling is the only thing he varies.
Shape comparison: Ryo Hasegawa d0–d4 exact, d5 near, breaks at d6 — longest frozen script, selling
free. カワシギ d1–d2 exact, branch persists, tree 58% at d12 — structure carried across days.
tetsuya d0–d3 (d3 at 98%), lawnmower, tree 3% at d12 — reactive routine.
Repertoire (9-game sample): PLANT WHEAT 1,157, STRAWBERRY 312, CARROT 205, MELON 147, TOMATO 26.
BUY_ANIMAL COW 85, SHEEP 28. SELL orders FERTILIZER 672, MILK 415, STRAWBERRY 353, WHEAT 323, WOOL
174, MELON 95, CARROT 73, TOMATO 34. No geese or eggs (COW and SHEEP only). Tomato in 3 of 9 games
(26 plants, ~2% of planting). Carrot in 6 of 9 games (205 plants). Wheat 63% of everything he plants.
Sell figures are order counts, not fills — presence/absence reliable, volumes not.

A fifth wrong measurement, caught by disagreement: `what_differs_between_blocks.py` excluded the
market column from its total and printed "IDENTICAL" when total==0, reporting Ryo's d1–d4 as
identical while the self-consistency table said 78% for d2. A direct hash of raw actions settled it:
day1 9 games, 2 distinct (7 vs 2); day2 9 games, 2 distinct (7 vs 2); days 0/3/4 1 distinct. The label
now says "unit ops IDENTICAL — but N turn-pairs differ in MARKET ORDERS ONLY".

Wrong-pick cost: is the tree's miss a near neighbour of the right block or unrelated? Against a
random block from the same day's library, カワシギ: d3 exact 83.6%, wrong:real 7.5, random:real 15.5,
ratio 0.48. d6 83.6%, 1.7, 3.7, 0.46. d7 65.7%, 34.2, 34.0, 1.00. d9 73.1%, 22.2, 23.3, 0.95. d11
47.8%, 46.9, 40.3, 1.16. d12 58.2%, 35.4, 48.7, 0.73. d16 26.9%, 67.9, 73.8, 0.92. Median ratio ~0.73,
but d7/d9/d11/d16 sit at 0.92–1.16 — on those days a miss is as far from the truth as a random pick.
Exact-match accuracy is not a large underestimate, the opposite of what was expected before measuring.

RETRACTION: the "frozen five-day opening" was a nine-game artifact. At 9 games Ryo's d0–d4 unit ops
were byte-identical; at 83 games only d0 is. Table (day | 9 games | 48 games | 83 games): d1 identical
/ 6.4 slots-per-pair / 6.7 (PLANT 95%); d2 identical / 14.6 / 15.0; d3 identical / 37.5 / 38.5; d4
identical / 6.6 / 7.6; d5 0.8 / 12.5 (—); d6 34.8 / 95.7 (—). Self-consistency at 84 seasons: d0 100%,
d2 89%, d4 86%, d6 38%, d8 18%, d10 5%, d18 2%. Highly repetitive early, not stable later — opposite
of what a flat blocks-per-group row suggests. Probable cause, stated as hypothesis and not
established: six of the original nine games were against tetsuya, so with varied opponents his play
may move from d1 onward. Second time in one session a clean early result dissolved under more data.

Ryo Hasegawa's repertoire, 84 seasons: PLANT WHEAT 12,293, STRAWBERRY 2,639, CARROT 1,718, MELON 996,
TOMATO 257. BUY_SEED WHEAT 6,832, CARROT 1,151, STRAWBERRY 916, TOMATO 143, MELON 90. BUY_ANIMAL COW
766, SHEEP 411. Presence: WHEAT/MELON/STRAWBERRY 84/84 (100%), CARROT 45/84 (54%), TOMATO 21/84
(25%), GOOSE/EGG 0/84 (0%). Melon planted every game, only ~1 seed bought per game (90 across 84
seasons at $80 each) — a deliberate, tiny, early commitment. Q3, not Q4: starting quadrant NW day 0;
2nd quadrant day 5 (72 games) or day 6 (12 games); 3rd quadrant day 9 (24 games) or day 10 (60 games);
4th quadrant never; final count 3 in all 84 games.

The shipped artifact: `data/block_agent_kawa.pkl`, 3.0 MB, 734 blocks, days 3–16, カワシギ. A day
ships only if its tree beats the majority baseline by >= 5%, so d17–d29 are absent. Known bug in the
ship rule, not yet fixed: d0 (85% baseline), d1 and d2 (100% baseline) are excluded because a tree
cannot beat a constant that is already right — but a 100% baseline is the answer, and the rule
silently drops the most certain days in the season.

### 4.2 The arm is the whole model

Source: `the_arm_is_the_whole_model_2026-08-20.md`. Full 30-day seasons, held-out games, real
environment.

Structure: trunk d0–d6 (tetsuya), identical in all 88 games, replays exact. Arm: crop + animal mix, a
handful per player. Within arm: op sequence + jitter, the perturbation space. A "clone" is a lookup
table keyed on (day, hour, unit slot) — no board state at all — built from the games in one arm. Not
a network, no parameters; plays a full legal 720-turn game.

The board must NOT be in the key. Keying a unit on (day, hour, x, y, tile-under) fails completely:
board-keyed, held out, work ops off by 402 (79.3%), FEED 0/85, CARE 0/85. Board-keyed, table = that
game itself: work ops off by 388 (76.5%), FEED 0/85, CARE 1/85 — it cannot even reproduce a game
whose table was built from that game alone, because position is an OUTPUT of the sequence: one wrong
move puts a unit on a square the teacher never occupied at that hour, every later key misses and
falls back to modal PASS or a move, never standing on a pen again — hence zero feeds all season.
This is why 86.2% per-decision accuracy meant nothing: measured on the teacher's states, the same
table scores 79.3% error on its own trajectory. Per-decision accuracy on expert states does not
predict closed-loop play.

The arm is worth more than the data. tetsuya (88 games): no arm 25.6% error, dominant arm 16.3%,
oracle arm (7 games) 3.7%. kawashigi (140 games): no arm 21.3%, arm @0.05 threshold 16.0%, arm @0.03
13.0%, oracle arm (7 games) 6.5%. Both players reach their best with exactly 7 games in the arm —
probably the real granularity of a tape. The modal tape averages across arms planting different
crops, so at a slot where one arm plants strawberry and another plants wheat the mode is "plant
nothing" — the whole of PLANT 66/212; animal cadence, identical across arms, transferred untouched.
tetsuya oracle arm, full season: PLANT 191/212, WATER 885/854, HARVEST 411/443, FEED 353/353, CARE
352/353, COLLECT_FERTILIZER 363/353.

Kawashigi was never harder — we could not afford a tight enough arm. At 45 games his best was 16.9%;
at 140 games it is 6.5% (7-game arm at threshold 0.02); the threshold sweep was monotonic at both
sample sizes, so the limit was cluster purity, not the player. The 45-game sample was an artifact of
`MIN_WINNER_BANK = 60_000`; removing the filter and pulling 2026-08-14..16 took him from 45 to 140.
tetsuya appears in zero games before 08-19 — a recent arrival. Three earlier readings that said "kawa
is harder" were reading this same data shortage: board-keyed 72.0% against tetsuya's 86.2%, 34
clusters from 34 games, 16.9% against 3.7%.

The arm cannot be chosen at dawn. Purity of the arm given what is observable, 88 tetsuya games, 17
arms: d0 shops predict arm 35%, planted-so-far 35%. d3 41%, 35%. d6 66%, 40%. d9 77%, 61%. d12 85%,
84%. d14 85%, 92%. 35% at d0 is the base rate — no signal. The shop draw becomes useful at d6 (66%)
and good at d12 (85%). Survivable because of the trunk: d0–d6 is identical across every arm, so no
choice is needed until d7, exactly when the shop signal arrives, and the choice need not be
irreversible (open on the dominant arm, switch as the draw disambiguates). Expected cost of a 66%
pick at d7: roughly 0.66 × 3.7% + 0.34 × 16.3% ≈ 8%, half the error of always playing the dominant
line.

What this is and is not: a classifier plus a replay table — a glorified if/else. It plans nothing. It
beats the planner on d0–d10 (6.9% against ~9%) and is exact through d7 including the walking route,
which the planner has never been on any day. It does not react — replays the same turns whoever it
faces, which works only because the seats interact solely through the shared market book, and it caps
at roughly the teacher's own strength. The teacher banks $94,906 mean and sits second on the ladder —
the cap is a medal, not a win. As an RL teacher it is strong for initialisation and weak for DAgger:
queryable at any state, but its answer is "what he did", not "what is best here", so it cannot correct
a student's mistake. Good prior, poor corrector.

Order of work proposed: (1) arm classifier, 16.3%→3.7% measured headroom, the only step that makes
this shippable — everything else confounded until done; (2) perturbation in `jax_sim`, which scores
an edit exactly; (3) RL from the tape as prior, KL-anchored, terminal reward, gated on win rate
against the frozen pool. Doing (2) before (1) means hill-climbing a 16%-wrong copy and confounding
every result with its defects — the same trap that made the care-bid change measure as a null.

### 4.3 The library agent — built, and it loses

Source: `the_library_agent_and_where_kawa_parts_2026-08-21.md`, built and measured 2026-08-21,
continuing 3.3.

Headline: the agent is built and it loses to the shipped greedy planner, 0-2 on seed 11 — $68,445
against $109,270. Not a candidate to ship; nothing here was submitted.

What was built: `kagg/search/kawa_rows.py` (schedule: library rows at the ends, wheat in the middle),
`kagg/search/kawa_library_agent.py` (schedule_agent driven by that schedule),
`tests/test_the_middle_is_planted_by_the_planner_not_the_row.py` (120 tests). d0–d12 the modal
library row for that day, strict, no greedy planting reaches these days. d13–d27 the modal row with
planting replaced by a whole board of WHEAT (`["WHEAT"] * 100`, no seeds order — under `router=True`
the executor sites one PLANT pin per entry on ground empty at dawn and buys seed for the remaining
pins, so a row longer than the board can never bind). d28–d29 the modal library row. All days,
species substituted at play time from the live shop draw.

The seed provably does not matter here: recordings carry `seed: null`; `breakdown.py` injects the
recorded shop draw every turn and defaults `--weeds` to 0.0, removing every observable effect of the
RNG — verified: a full 30-day grid on seed 11 and seed 777 is byte-identical except the header line
echoing the seed. Weeds are 0.0 on every run per Alex, switching off RANDOM spawning only; a tile left
two days unwatered still becomes a WEED (`reference/kaggriculture.py:771`) and that path cannot be
disabled. The ladder runs 0.005 — every number here is a clean-room number, not a ladder estimate.

Q1: d13 belongs to the library. Both boundaries, seed 11, same tape, weeds 0.0: library d0–d12,
greedy d13–d27: ours 138,515, tape 150,076. Library d0–d13, greedy d14–d27: ours 140,057, tape
150,076. Delta −1,542: putting d13 in the middle costs $1,542. `MID_SEASON_FROM = 14`, matching where
the crop-shape measurement put it — his d13 is still mixed STRAWBERRY+WHEAT.

Q2, Alex's three candidates answered separately, d14–d27 totals (shipped / library / tape): PLANT ops
109 / 158 / 112. WATER ops 648 / 713 / 580. HARVEST ops 299 / 299 / 295. Live crop tiles mean n/a /
59.0 / 56.7.
Candidate 3 (route) is the live one and it is exact: the library plants 158 against the shipped
agent's 109 and the tape's 112 — 45% and 41% more — waters 65 more times, and harvests exactly the
same 299. Forty-nine extra plantings and sixty-five extra waterings bought zero extra harvest —
over-planting relative to the watering budget.
Candidate 2 (route) is NOT failing: live crop tiles run 59.0 against the tape's 56.7 — we hold more
standing crop than he does every mid-season day, sharply contrasting with the previous block-agent
attempt (22 live tiles against 49).
Candidate 1 (the numbers) is not wrong — absent by design: the middle carries no count at all, so
there is no wrong number to fix. The measurement shows our router's own budget produces 41% more
planting than his budget — our tour has slack his does not, and spends it on planting that does not
pay.

Q3: where it parts from the tape, and why d0–d12 does not match. The tape's own row is the row we
play on 4 of the 13 strict days: d0, d1, d2, d4. Full comparison table (day | phase | ours hash |
tape hash | same? | modal% | his rank): d0 YES 100.0% 1/1; d1 YES 100.0% 1/1; d2 YES 100.0% 1/1; d3
no 65.4% 2/4; d4 YES 98.7% 1/3; d5 no 61.8% 3/4; d6 no 46.1% 4/9; d7 no 24.6% 7/21; d8 no 22.8% 7/31;
d9 no 22.8% 5/25; d10 no 20.2% 9/28; d11 no 16.7% 7/44; d12 no 20.2% 9/42; d13 no 20.2% 33/35; d28 no
36.8% 2/7; d29 YES 100.0% 1/1. Game 92498144 is not the modal season from d3 on, so post-d2 divergence
cannot be read as an execution defect — a different plan was chosen on purpose. Cost of that choice:
at d13, before the greedy middle starts, the library agent is already $4,644 behind the shipped agent
($13,546 vs $18,190); it finishes $6,548 behind ($140,057 vs $146,605) — roughly 71% of the whole gap
is the opening, only 29% accrues across the fourteen greedy days.

Q4: win or loss. LOSS. Library agent vs shipped greedy planner, seed 11, weeds 0.0, both seatings:
seat 0 library 68,445 vs greedy 109,270 LOSS; seat 1 same finals mirrored. W/D/L 0/0/2. The two
seatings are not independent (finals mirror exactly), so treat as n=1, not n=2 — a direction, not a
rate.

The row library has a defect, not cosmetic: `places` in the row data is mostly not animals —
STRAWBERRY 2,794, WOOL 2,218, COW 1,936, MELON 1,653, SHEEP 1,496, FERTILIZER 1,204, MILK 1,039.
Kawashigi's PLACE branch drops items into the shed as often as it places animals, and the extractor
appends both forms verbatim, so `schedule_agent._outstanding_places` reading every entry as
`R.ANIMALS[a]["first_yield_day"]` throws `KeyError: 'FERTILIZER'` at `schedule_agent.py:3862` on d1.
`kawa_rows.only_animals_get_placed` filters it, and also changes the label — dropping the shed-drop
cadence took d13 from 58 distinct rows to 35. `scripts/extract_target_rows.py` should be fixed at
source (not done here — flagged as Alex's uncommitted work); every distinct-row count in
`kawashigi_algorithm_2026-08-21.md` (3.2) is inflated by it.

Label: sells and buys are execution after the land buy. Modal share of the day under three labels
(all ten keys / minus sells / minus sells and buys): d22 1% / 1% / 2%. d27 1% / 1% / 1%. d28 1% / 13%
/ 27%. d29 1% / 98% / 98%. d29 is the whole case: 224 of 228 seasons play the same closing day, but
hashing the sell quota reported 212 distinct plans for it. `SELLS_ARE_EXECUTION_FROM_DAY = 13` is
Alex's own recorded position. It does not rescue the middle — d22–d27 stay at 1–2% under every label.

Modal coverage (share of the day's 228 seasons the chosen row speaks for, after the places fix): d0
100.0%, d1 100.0%, d2 100.0%, d3 65.4%, d4 98.7%, d5 61.8%, d6 46.1%, d7 24.6%, d8 22.8%, d9 22.8%,
d10 20.2%, d11 16.7%, d12 20.2%, d13 20.2%, d14 21.5%, d15 14.5%, d16 10.5%, d17 12.3%, d18 11.8%, d19
11.4%, d20 7.9%, d21 3.9%, d22 3.1%, d23 3.9%, d24 3.1%, d25 1.8%, d26 2.6%, d27 4.8%, d28 36.8%, d29
100.0%. d0–d2 and d29 are constants and need nothing. d3–d6 are 46–99%, modal row defensible. d7–d13
are 17–25%, so the modal row is wrong four times in five — exactly the window that costs $4,644 by
d13. A selector for d7–d13 is proposed as the next build, now justified by a number.

Unverified: one seed, one opponent, one tape — the head-to-head is n=1 in effect; whether a d7–d13
selector recovers the $4,644, not measured; whether trimming the middle's planting toward his 112
recovers the remaining ~$1,900, not measured (49 extra plantings bought no harvest, but the cost of
those turns if they had nothing better to do is unknown); every number is at weedSpawnChance=0.0, the
ladder runs 0.005; `SHOP_ADAPT_CROPS = False` confirmed, so nothing re-aims the crop on strict days —
if ever switched on, d6–d12 stops being strict row matching (`CROP_ADAPT_FROM_DAY = 6`,
`CROP_SWAP_PAIRS` contains ("WHEAT", "CARROT")).

---

## 5. Decision points scored as selectors

Source: `decision_points_2026-08-16.md`. Script `scripts/decision_points.py`.

What was measured, and why it is not the separation table again: a prior analysis reported a
"separation" table (a rule cleanly splits his own games) as if it were a result. It is not — a rule
that separates 51 games perfectly and does not beat the better of the two branches it selects between
is worth nothing. Each decision point therefore has three arms: always-A (play branch A's tape all
season), always-B, and selector (play A to the decision turn, switch to B if the rule fires). Every
arm is a recorded tape on our seat; our own planner is not in the measurement.
Method: 96 seeds × 2 seats per arm = 192 games per arm, 1,152 games total. Both seats always
(`_process_market` walks player 0 then player 1 per unit, so a tape moved to the other seat loses
price priority). `weedSpawnChance = 0.005`, the ladder value. One OS process per game. Opponent
`data/sweep/frozen_1186_opponent.py`, a built bundle loaded by path, carrying its own module copies —
no arm is ever the opponent. Win rate is the score; money is a diagnostic column only. Noise floor
`2*sqrt(0.25/192) = 7.2%`.

Classifying his 51 games: `data/seed_scripts/downloads_2026-08-13/` holds 79 JSON files; two
(91304798-0/1) are bare step lists with no info block and are skipped; of the remaining 77, 51
contain カワシギ. Counting his own PLANT emissions: MELON 20 / STRAW 34 / WHEAT 120–147, 41 games
(episodes including 91889284, 91890202, 91892046...). MELON 12 / STRAW 42 / WHEAT 117–130, 9 games
(91891131, 91892982...). MELON 20 / STRAW 33 / WHEAT 159, 1 outlier game (91918341). The brief's
"42/9 split" is 41/9 plus one outlier. He wins 47 of these 51 games.

The d3 rule separates his games 51/51: opponent MELON tiles at dawn of d3, by class: 20/34 (41 games)
opponent melon min 4 max 8, >=9 count 0, YARN by d6 15/41. 12/42 (9 games) min 9 max 13, >=9 count 9,
YARN by d6 1/9. 20/33 (1 game) min/max 5, >=9 count 0, YARN by d6 1/1. The two classes do not overlap:
melon-heavy tops out at 8, strawberry-heavy starts at 9. Threshold 9 separates all 51 games — stated
explicitly as the hypothesis, not the result.

Representative tapes, chosen as the game agreeing with its class's modal day script on the most days
(not the richest game, to avoid crediting the branch with a lucky board): dp1 branch A (melon-heavy,
41 games) episode 91919278, agrees on 20/30 days, his result seat 1 $79,486 vs $80,026. dp1 branch B
(straw-heavy, 9 games) episode 91891131, agrees on 21/30 days, seat 1 $67,971 vs $1,142 (opponent
collapsed — used only as a source of actions, never of a result). dp2 branch A (three-quadrant)
episode 92498144 (given in brief). dp2 branch B (four-quadrant) episode 91907974 (given in brief),
seat 0 $88,763 vs $49,859.
The four-quadrant herd is COW 6 / SHEEP 10, not COW 6 / SHEEP 8 as the brief stated — read from the
final observation of 91907974 (herd COW 6, SHEEP 10, tiles owned 100, crops WHEAT 142, MELON 20,
STRAWBERRY 34, CARROT 7, YARN_STORE unlocked by d6: True). Note 91907974 is itself a melon-heavy game
(MELON 20/STRAW 34), so dp2's branch B is not a strawberry-heavy tape.

Splice validity: dp1's two branches are byte-identical for the whole opening (72/72 turns identical
before the switch, no difference anywhere in d0–d2) — the selector arm is one season with a fork in
it, exact. dp2's is not: 170/216 turns identical before the switch, first difference at turn 96 (d4)
— dp2/selector is a hybrid of two seasons and its number is a lower bound.

Result, opponent `frozen_1186_opponent.py`, weedSpawnChance 0.005, 96 seeds × 2 seats: dp1/always-melon
62.5% win, 0.0% draw, 37.5% loss, mean $89,381, mean margin +990. dp1/always-straw 60.4%/0.0%/39.6%,
$90,871, +1,067. dp1/selector 60.4%/0.0%/39.6%, $90,871, +1,067, B fired 100%. dp2/always-3q
52.6%/0.0%/47.4%, $86,455, −1,420. dp2/always-4q 19.3%/0.0%/80.7%, $80,196, −13,701. dp2/selector
62.0%/0.0%/38.0%, $86,896, +234, B fired 16%.
Paired comparison: dp1 better constant (always-melon) 62.5% win vs selector 60.4%, delta −2.1%,
paired W-L 31-35, sign p 1.000 — NO, and untested (see below). dp2 better constant (always-3q) 52.6%
vs selector 62.0%, delta +9.4%, paired 19-1, sign p 0.000 — YES.

Verdict dp1 (melon vs strawberry at d3): NO, and the test did not run. −2.1% is inside the 7.2% floor,
but the number is not the point: the rule fired on 100% of the 192 games, because
`frozen_1186_opponent.py` plays カワシギ's own schedule, which buys MELON 12 on d0 and holds 12 melon
tiles at dawn of d3 on every seed (measured directly, seeds 1/2/3 all read 12) — above the threshold
of 9. So dp1/selector is byte-identical to dp1/always-straw by construction (identical $90,871, 60.4%,
0 discordant pairs). This is a fact about the opponent, not evidence about the rule — a delta of 0.0
against a constant the selector IS reads exactly like a measured null and must not be recorded as
one. The mandated opponent is effectively a mirror of the player whose rule is tested, and a mirror
cannot exercise a rule keyed on the opponent's crop mix. (The two branch tapes are also
indistinguishable from each other here: 62.5% vs 60.4%, inside the same floor.) To actually test dp1,
a built-bundle opponent holding fewer than 9 melon tiles at d3 is needed; none exists in
`data/sweep/` — the `cand_*.py` files there import `schedule_agent` live and set module-level dials
(would overwrite the arm under test in the same process) and take `(obs, config)`, raising
`KeyError: 'step'` when called with a turn index.

Verdict dp2 (four quadrants at d6): YES. +9.4% over the better constant, above the 7.2% floor, paired
19-1 (sign test p < 0.001). Split by whether the rule fired: fired (30 games) always-3q 3/30=10%,
always-4q 23/30=77%, selector 21/30=70%. Did not fire (162 games) always-3q 98/162=60%, always-4q
14/162=9%, selector 98/162=60%. A clean interaction, not a main effect: the four-quadrant tape is a
disaster as a constant (19.3% over the season, 9% where YARN_STORE has not unlocked by d6), but on
the 30 boards where it has unlocked by d6, it inverts completely (77% vs 10%). The selector converts
a 10% subset into a 70% one. Two bounds on this result: (1) the selector reaches 70% on the fired
subset where always-4q reaches 77% — the 7-point gap is the splice (the tapes already differ at d4),
so 70% is a lower bound; (2) the rule fired on 30/192 = 15.6% of these seeds, vs 17/51 = 33% in his
own ladder games — different populations (our seeds 1-96 vs his ladder boards), not reconciled here.

What this does and does not license: dp2 is a real, measured, positive selector — the first thing in
this line of work that beats its own better constant rather than merely separating his games. dp1 is
open: separation is perfect and the mechanism plausible (melon is the one crop no shop buys, so its
price is set entirely by what the two farms dump into the town book), but no measurement has been
taken — do not carry the separation table forward as support for it. Nothing here says our live
planner should adopt either branch; every arm was a tape.

---

## 6. Allocation bounds — near-optimal region per crop and species

Source: `allocation_bounds_2026-08-16.md`. Carries a SUPERSEDED banner: `allocation_bounds_pass2_2026-08-16.md`
(section 6b), same day, same script, narrows every band 24–32% with a corrected cost model and adds a
per-shop-draw policy this pass does not have. Kept below because pass 2's attribution table is stated
relative to this pass's baseline (V0).

Question: given the game's constraints, what range must the season allocation lie in — the interval
each season total can move over while end-of-season money stays within 1% (and 5%) of the model
optimum.

Headline: the leader's MELON 20 / STRAWBERRY 34 split is NOT inside the 1% near-optimal region in any
of three scenarios. Pinning it costs 1.78% of the optimum when the opponent sells nothing, 3.9%
against the leader's own supply, 23% against double supply. It IS inside the 5% region in the first
two scenarios. The reason is melon alone: the melon book absorbs only ~30 units of town demand a
season and its price falls as 250 − 0.01·(surplus)², so 20 melon tiles (120 melons) is near-optimal
only when the opponent is not also selling melons. His strawberry 34 sits inside the 1% interval in
scenarios 1 and 2. The herd answer is shop-draw dependent: under this game's draw (SMOOTHIEx4) the
model wants 9–18 cows and his cross-game modal COW 6 is below the 1% interval; under an average draw
optimal herd collapses to COW ~2. His measured play IN this game (COW 10, SHEEP 4) matches the
model's scenario-1 optimum (COW 9, SHEEP 6) far better than his cross-game modal 6/8 — consistent
with "the leader re-plans on the shop draw".

Results, all money end-of-season minus $3,000 start (Z). Base MILP solves reached mip gaps 0.4–0.7%
at the 150s limit; pinned leader checks reached 0.4–2.0%.

Scenario 1 (opponent = leader's per-day fills), Z* = $129,045 (bank $132,045): base/[1% range]/[5%
range]/leader — WHEAT 93 [15,185] [0,229] –; CARROT 16 [0,144] [0,194] –; TOMATO 22 [0,68] [0,85] –;
STRAWBERRY 29 [15,50] [7,64] 34; MELON 6 [0,31] [0,45] 20; GOOSE 2 [0,15] [0,21] 0; COW 9 [6,17]
[5,22] 6; SHEEP 6 [4,15] [3,20] 8. Pinned MELON=20,STRAW=34 → Z $123,989, drop 3.92%. Pinned
MELON=20,STRAW=34,COW=6,SHEEP=8 → Z $118,148, drop 8.44%.

Scenario 2 (opponent = zero), Z* = $190,247 (bank $193,247): WHEAT 65 [2,148] [0,181]; CARROT 7
[0,86] [0,135]; TOMATO 2 [0,38] [0,56]; STRAWBERRY 33 [20,51] [9,62] 34; MELON 27 [14,42] [6,55] 20;
GOOSE 0 [0,10] [0,17] 0; COW 18 [13,24] [8,30] 6; SHEEP 10 [7,18] [5,24] 8. Pinned MELON=20,STRAW=34 →
Z $186,856, drop 1.78%. Pinned +COW=6,SHEEP=8 → Z $161,856, drop 14.92%.

Scenario 3 (opponent = 2x leader's fills), Z* = $56,125 (bank $59,125): WHEAT 110 [47,197] [31,227];
CARROT 43 [0,130] [0,165]; TOMATO 40 [16,64] [6,74]; STRAWBERRY 9 [1,20] [0,27] 34; MELON 0 [0,12]
[0,20] 20; GOOSE 16 [8,22] [5,25] 0; COW 0 [0,5] [0,7] 6; SHEEP 0 [0,3] [0,6] 8. Pinned
MELON=20,STRAW=34 → Z $43,198, drop 23.03%. Pinned +COW=6,SHEEP=8 → Z $31,545, drop 43.79%.

Base solution detail, scenario 1: hands 8.1/day mean (leader measured 9.6 units/day incl. farmer), 2
land parcels, wheat bought 142, fertilizer collected 335 sold 145 (leader sold 249), sold MELON 36 /
STRAWBERRY 232 / MILK 294 / WOOL 164.

What holds in all three scenarios: some strawberry is always in (min never 0 at 1% in S1/S2; 1.5 in
S3), and 34 tiles is never harmful by more than ~2% except under a double-supply flood. Melon is the
contested resource: its 1% interval slides from [14,42] (empty market) to [0,31] (leader present) to
[0,12] (flooded) — no melon count is near-optimal in all three scenarios; melon allocation is a bet
on what the opponent sells. Wheat is wide everywhere ([15–47 min, 148–197 max @1%]) — nearly a free
parameter. Geese are never obligatory below double supply but become the safe haven when everything
else floods (S3 forces 8–22 geese) — the first measured case where geese are the right play, against
a flooder, not against the field. The herd tracks milk/wool demand from the shop draw, 0 to 28 head.

Shop-draw sensitivity (scenario-1 economics): actual draw (SMOOTHIEx4) Z* $129,045, WHEAT 93 CARROT
16 TOMATO 22 STRAW 29 MELON 6 GOOSE 2 COW 9 SHEEP 6. Expected/average shop draw Z* $93,073, WHEAT 85
CARROT 42 TOMATO 29 STRAW 16 MELON 11 GOOSE 10 COW 2 SHEEP 5. No shops Z* $53,038, WHEAT 141 CARROT
46 TOMATO 23 STRAW 0 MELON 13 GOOSE 17 COW 0 SHEEP 0. The draw moves Z* by 2.4x and reallocates the
whole farm; melon moves only 6→13 because melon has no shop (demand is the town center's 1/day
regardless of draw). Any fixed season allocation is an average over draws; the measured leader
behaviour (fixed 74-turn opening, then adapt to the draw) is what this table predicts a good player
must do.

Ground truth: rules/prices/growth imported at runtime from installed `kaggle-environments 1.32.7`
(byte-identical to `reference/kaggriculture.py`; the worktree copy was stale, pre-hinge, and not
used). Opponent supply from episode 92498144 (カワシギ $149,998 vs Yusuke Hayashi $143,436, seed
1240813987), re-run through the real engine, recorded rewards reproduce to +$78/+$0 (0.05%; drift is
the 1.32.7 repricing of CARROT/TOMATO/EGG since the episode was recorded on 1.32.6). Leader's measured
season from those fills: sold WHEAT 522 / STRAWBERRY 223 / MELON 120 / MILK 279 / WOOL 120 /
FERTILIZER 249 / CARROT 20; bought WHEAT 423; seed buys WHEAT 144 / MELON 20 / STRAWBERRY 34 / CARROT
16; animal buys COW 10 / SHEEP 4. The MELON 20 / STRAWBERRY 34 seed buys equal the reference
allocation measured over 51 games. Shop draw in that game: d3 SMOOTHIE, d6 ICE_CREAM, d9
FARMERS_MARKET, d12 YARN, d15 PIZZA, d18/21/24 SMOOTHIE. Season town drain: WHEAT 390, CARROT 156,
TOMATO 246, STRAWBERRY 624, MELON 30, EGG 30, MILK 588, WOOL 246, FERTILIZER 0.

Model: MILP over days 0–29, decision variables for crop-cycle starts, animal purchases, hands hired,
land parcels, sell-slot units, wheat/fertilizer buy-and-collect. Labour constraint uses lambda = 1.254
(3477 move / 2773 work unit-turns, the leader's measured ratio on the seed-11 tape). Revenue modelled
via K=30 fixed-width sell slots per product with assumed sell days tracking cumulative book room,
each slot valued as a lower bound (prior slots assumed sold first). Assumptions stated plainly: walk
cost is a flat average with no per-quadrant term; sell timing follows the demand curve, not a decision
variable; within-day cash ordering ignored; own wheat/fertilizer buy volume re-prices the book above
100 units via one feedback iteration; full husbandry/watering assumed, weeds not modelled; shed
capacity and 10-orders-per-turn cap ignored as non-binding; animals never escape or get sold; goose is
modelled with nothing forbidding it; opponent behaviour fixed per scenario, no Elo/win-rate objective.
Known biases: revenue is a lower bound under fixed sell timing; labour charged at the leader's
realised walk ratio (a better router lowers it); prices conservative for high-volume products, so
milk/strawberry/wheat are if anything under-allocated by the model.
Run facts: full run 1,975s on 2026-08-16; MILP 1,140 variables (300 integer), 573 constraints, HiGHS
via scipy 1.16. Wheat-buy price feedback triggered in all three scenarios (S1 bought 142, price
$42→$46; S2 bought 466, $45→$54; S3 bought 101, $39→$42).

### 6b. Allocation bounds, pass 2 — narrower bands, per-draw policy, best response

Source: `allocation_bounds_pass2_2026-08-16.md`, 2026-08-16, same day as 6.

Headline: bands narrowed 24–32% from modelling fidelity (daily-water maintenance + geometry walk),
essentially 0% from solver gap at 1% tolerance, and a further ~25% by reporting at 0.1%: WHEAT
[15,185]→[23,135], CARROT [0,144]→[0,86] (combined model, 0.1%). What width remains at 0.1% is
genuine economics — carrot and tomato are near-zero-margin crops whose lower bound really is 0.
Per-draw policy is the actionable output: optimal mix swings from SHEEP 20/STRAWBERRY 9 (YARNx4
draw) to STRAWBERRY 28/COW 9 (SMOOTHIEx4 draw) to GOOSE 6/CARROT 37 (BAKERY+PET draw) — no fixed
allocation is near-optimal across draws. MELON 20/STRAWBERRY 34: melon 20 lies inside the 1% outer
interval of every draw solved; strawberry 34 only under smoothie-heavy draws. The joint point always
costs more than 1%: 3.7% under the actual draw, 13–15% under others. Best-response iteration: every
quantity except melon is stable from iteration 0 (STRAW 26–30, COW 9–10, SHEEP 5–6, WHEAT 79–85,
GOOSE 0–2); melon see-saws 7→18→11→12 tiles against opponent melon 120→42→108→66, a contracting
oscillation around ~12–14 tiles per player, combined sales pinned near the 188-unit season cap. MELON
20 is the exploitable side of that fixed point: the best response to a 20-tile melon opponent is 7
tiles, not 20.

Corrections to the tasking, from the reference (1.32.7): ongoing crops do not need water every single
day (`_daily_refresh_plants` weeds at `consecutive_unwatered >= 2`, so watering every other day keeps
a crop alive, and unfertilised ongoing production needs no watering at all — only the fertiliser bonus
checks `watered_today`). An ongoing tile's obligation is finite, not to season end (after `max_yield`
productions the plant decays; a strawberry planted day d produces d+9/11/13/15 and is dead wood from
d+17). Pass 1 already charged per-day maintenance for ongoing crops accordingly: strawberry_u 8
waters + 1 harvest + 1 dig over 17 tile-days (0.59 ops/tile-day), tomato_u 6 waters + 1 harvest + 1
dig over 12 tile-days (0.75), melon 10 ops over 11 tile-days (0.91, the op-densest crop per tile-day).
The 19-strawberry-weed game (93593633) was an execution failure (idle turns existed the two days
before die-off), not a cost the planner omitted.

Item attribution, one at a time (S1, actual draw, opponent = leader fills), 1% band widths: V0
pass-1 baseline WHEAT 169.6, CARROT 144.3, TOMATO 68.1, STRAWBERRY 34.3, MELON 31.2, GOOSE 14.5, COW
10.9, SHEEP 10.7; Z* $129,045, gap 0.40%. V1 tight-gap: widths essentially unchanged (169.7, 144.3,
...), Z* $129,046, gap <=0.05% — the pass-1 1% bands were economics, not solver slop. V2 daily-water:
153.6, 127.8, 57.6, 30.1, 28.8, 12.6, 9.2, 9.4; Z* $127,578, gap 0.20% — Z* −1.1%. V3 geometry-walk:
146.7, 113.7, 62.9, 32.4, 28.6, 14.6, 10.1, 10.2; Z* $125,807, gap 0.88% — Z* −2.5%; implied move/work
ratio 1.43–1.47 vs the tape's 1.254, so it charges MORE than the flat model (conservative), penalising
crop-heavy visit-dense mixes specifically. V4 combined: 128.7, 97.8, 50.5, 28.0, 26.1, 12.2, 8.1, 8.4;
Z* $123,827, gap 0.09%. Combined effect: −16% (melon) to −32% (carrot) width at 1%.

Narrowed bands (combined model V4, S1, actual draw): WHEAT base 83, 0.1% [23,135], 1.0% [15,144], 5.0%
[0,178]. CARROT 10, [0,86], [0,98], [0,144]. TOMATO 22, [0,46], [0,51], [0,65]. STRAWBERRY 28, [17,40],
[15,43], [6,55], leader 34. MELON 7, [0,23], [0,26], [0,38], leader 20. GOOSE 2, [0,10], [0,12],
[0,19]. SHEEP 6, [5,11], [4,13], [3,18]. COW 9, [7,14], [7,15], [5,20]. Pass-1 vs pass-2 at 1%: WHEAT
[15,185]→[15,144], CARROT [0,144]→[0,98], TOMATO [0,68]→[0,51], STRAWBERRY [15,50]→[15,43], MELON
[0,31]→[0,26], COW [6,17]→[7,15], SHEEP [4,15]→[4,13], GOOSE [0,15]→[0,12].

Town demand caps, actual draw: WHEAT drain 390, floor_room >5000, no season cap, price at I0+50 22,
at I0+150 21. CARROT 156, 842, 998, 27, 21. TOMATO 246, 529, 775, 42, 29. STRAWBERRY 624, 62, 686, 24,
1. MELON 30, 158, 188, 225, 25. EGG 30, >5000, none, 43, 41. MILK 588, 76, 664, 55, 1. WOOL 246, 59,
305, 55, 1. FERTILIZER 0, 493, 493, 90, 70. Demand-limited: MELON (188, the leader alone sells 120),
WOOL (305), FERTILIZER (493). Labour-limited: WHEAT, EGG. STRAWBERRY/MILK: huge drain but a cliff
just past it.

Per-draw policy (combined model, opponent = leader's recorded fills for every draw): actual draw
(FARMERS,ICE,PIZZA,SMOOTHIEx4,YARN) Z* $123,579, W88 C12 T23 S28 M6 G1 Co9 Sh6, MELON 1% [0,27], STRAW
1% [14,43], 20/34 pin cost 3.70%. rng11 (BRUNCH,FARMERSx2,ICE,YARNx4) Z* $81,286, W96 C19 T25 S9 M7
G2 Co0 Sh20, MELON [0,23], STRAW [0,22], pin 14.62%. rng12 (BAKERY,FARMERS,PET,PIZZAx2,SMOOTHIE,
YARNx2) Z* $103,883, W74 C37 T38 S3 M12 G6 Co2 Sh10, MELON [1,26], STRAW [0,17], pin 13.69%. rng13
(FARMERSx4,ICEx2,PETx2) Z* $73,048, W65 C13 T37 S29 M13 G12 Co0 Sh0, MELON [4,25], STRAW [20,44], pin
3.66%. rng14 (BRUNCHx2,ICE,PETx4,YARN) Z* $65,629, W94 C43 T10 S9 M12 G16 Co0 Sh3, MELON [0,32], STRAW
[0,29], pin 12.23%. rng15 (BAKERYx4,FARMERSx2,ICEx2) Z* $63,876, W81 C33 T30 S13 M9 G13 Co0 Sh0, MELON
[0,30], STRAW [0,32], pin 12.31%.
Wool-heavy draws (YARNx2+) flip the pen mix to sheep and kill strawberry; goose becomes the herd
(12–16 birds) whenever the draw gives neither milk nor wool demand (PET/BAKERY-heavy draws all have
COW=0); strawberry >= 20 is only optimal under smoothie/ice-cream/farmers-market demand. Melon's
optimum is 6–13 tiles in every draw. The 20/34 pin costs 3.7% under the two draws closest to his real
game and 12–15% elsewhere. Z* across draws spans $64k–$124k (1.9x) with opponent fixed — most of the
pass-1 "scenario spread" was demand, not opponent.

The leader's measured trigger against this model: on his 67 games, melon at day 9 is bimodal 12 or
20, melon+strawberry always 31, and the switch is the opponent's day-3 melon count (>=9 → 12/19, <9 →
20/11), zero errors. This matches the model's derived structure: best response to a melon-flooding
opponent is 7–12 tiles (his contested mode is 12); best response to a low-melon opponent is 14–27
tiles (his uncontested mode 20, inside the band on its cautious side); the BR fixed point ~12–14 tiles
is exactly his contested mode. What the model does NOT reproduce is his constant melon+strawberry=31
(the per-draw optima put it at 22–42) — labelled SPECULATION: a fixed-labour-block swap (8 tiles
retasked between two crops with near-equal maintenance), an execution constraint rather than a market
optimum. Consequence: the "optimal fixed allocation" question is moot — the leader himself does not
play one, and the model agrees no fixed melon count is near-optimal against both of his modes. On the
fourth quadrant: he buys it in 21/67 games, independent of the crop swap; this model chooses parcels
endogenously and lands on 2 parcels (S1) or 3 (S2) — tile budget was never binding at 75 in the S1
base (peak concurrent occupancy ~60), so the 4th-quadrant purchase tracks demand-rich draws, not the
melon/strawberry swap.

Best-response iteration (combined model, actual draw, start = leader's fills): iter 0 opponent
120/223/279 (melon/straw/milk), our mix W85 C10 T24 S27 M7 G1 Co9 Sh6, Z* $123,484, our melon sold 42.
iter1 opp 42/216/297, mix W85 C11 T10 S27 M18 G1 Co10 Sh5, Z* $120,369, sold 108. iter2 opp 108/216/303,
mix W79 C10 T20 S26 M11 G2 Co10 Sh6, Z* $119,185, sold 66. iter3 opp 66/208/306, mix W85 C13 T15 S30
M12 G0 Co10 Sh5, Z* $119,606, sold 72. Melon is the only strategically live quantity; oscillation
contracts toward ~12–14 tiles (~70–85 units) each, combined ~150 against the 188-unit cap. SPECULATION:
the symmetric equilibrium melon is 12–14 tiles per player; proving it needs a simultaneous, not
alternating, solve.

Residual model risks: geometry walk overcharges movement relative to the tape (1.43–1.47 vs 1.254),
so Z* and bands are conservative on labour. Peak daily harvest in base solutions is 170–207 units
against shed capacity 100 — executable but requires intra-day drop/sell sequencing on 3–5 peak days,
which the model does not schedule; an agent that dumps everything at dusk would lose the overflow.
Opponent supply is the leader's recording under every draw; his real play would adapt. LP-relaxation
bands remain outer bounds.

Run facts: attrib 2,734s (5 variants), policy 3,294s + 2,150s (first launch killed by the runner
after 3 of 6 draws, remaining 3 in a second log at time-limit 250s/gap 1e-3, gaps 0.1–0.5%), br 1,802s
(4 iterations). MILP 1,104–1,140 vars (264–300 int), 573 constraints, HiGHS mip_rel_gap 5e-4 targeted.

---

## 7. CEM allocation search — incomplete run, unresolved status

Source: `cem_allocation_search_2026-08-15.md`. Carries an "unsure — needs an owner's eye" banner
added 2026-08-22: as of that date this file still reads RESULT PENDING throughout, and no completion
was found anywhere in `docs/`. The same allocation question was answered by a different method the
next day in `allocation_bounds_pass2_2026-08-16.md` (section 6b). If this run never finished, that
file should be treated as the current answer, and whether this file should be deleted is unconfirmed.

Design as run (status: RESULT PENDING at every results section): search dials were `fork`
(`MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`, 0/1), `m`/`t`/`c`/`s` (`CROP_TILE_SHIFTS` for
WHEAT→MELON 0..24, WHEAT→TOMATO 0..14, WHEAT→CARROT 0..24, STRAWBERRY→WHEAT 0..7), and `g`
(`HERD_GEESE`, 0..3). All bounds pinned by 13 green tests in
`tests/test_the_allocation_dials_reach_the_tiles_they_claim.py`.

Three findings changed the design before the search ran. (1) `CROP_TILE_SHIFTS` cannot reduce melon:
the schedule plants melon only on d0, d6, d7, and `LATE_CROP_FROM_DAY` is 12, so a MELON→WHEAT shift
moves zero tiles; plantings reachable from d12 are WHEAT 109, CARROT 8, STRAWBERRY 7, no melon at
all. The only dial moving melon is `MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`, which converts d6/d7
melon rows to strawberry once the opponent shows 7+ melon tiles; turning it off holds MELON 20 /
STRAWBERRY 34 (Kawashigi's own allocation). (2) Win rate against `pool.OPPONENTS` is saturated and
cannot rank anything: measured on 2 seeds, both seatings, 24 games in 30.9s, win 0.8333 draw 0.1667
mean $146,050 — the shipped agent wins 100% against every pool member except `mirror`, which it draws
100% (same file playing itself). A first smoke run of the CEM confirmed this end to end: every
candidate scored `elo 1.000` and the held-out table was four rows of 1.000. The fix: inject a frozen
copy of the shipped agent as `pool.OPPONENTS["shipped"]`, keeping `carrot_25` and `melon_heavy` as
guards (CLAUDE.md records melon going 25→12→25 from a mirror-only sweep pointing the wrong way on
this exact dial). (3) Two candidate files in one process shared one set of dials: `m8`, `c8`, `s4`
and the zero vector all reported byte-identical tiles/bank/collection (MELON 12, WHEAT 132,
STRAWBERRY 41, CARROT 8, $132,959) because `import` returns the module already in `sys.modules`, so
the second candidate file to load wins and both agents play its dials — silently turning every duel
into a mirror match with no error. Fixed with a private copy of the agent module per candidate file,
loaded from source under a unique name; pinned by 4 tests including a deliberate reproduction.

Routing regime measurement: `cover.PRECOMPUTED_ROUTES` covers d12–d29 and `scripts/swap_one_crop.py`
unsolves those days unconditionally; unsolving costs 3x the wall clock (96s unsolved vs 31s solved on
the same 24 pool games), and was measured rather than inherited. Seed 3, vs the frozen shipped agent:
zero dials SOLVED $132,959, MELON 12 WHEAT 132 STRAW 41 CARROT 8, collection CARROT/MELON/STRAW
100%/100%/100%, WHEAT 97%. Zero dials UNSOLVED $120,047, same tiles, collection 100/100/98/95%. m8
SOLVED $121,887, MELON 20 WHEAT 125 STRAW 41 CARROT 8, collection 96/100/96/96%. m8 UNSOLVED $115,261,
MELON 20 WHEAT 113 STRAW 41 CARROT 8, 95/100/98/93%. c8 SOLVED $132,902, MELON 12 WHEAT 125 STRAW 41
CARROT 16, 96/100/100/96%. c8 UNSOLVED $117,482, same tiles, 96/100/97/92%. s4 SOLVED $127,232, MELON
12 WHEAT 135 STRAW 37 CARROT 8, 96/100/100/96%. fork0 SOLVED $158,786, MELON 19 WHEAT 133 STRAW 33
CARROT 8, 91/99/99/98%. The shifted crop is collected at 96–100% with routes kept — the dropped-stop
worry does not appear. Unsolving costs $6k–$15k a season and buys nothing measurable in collection.
The search runs solved (also what ships); `--unsolved` is kept as a flag with the measurement in its
help text.

Search design: population 10 (+ baseline + incumbent, deduplicated to 11 distinct evaluations per
generation), elite 4, generations 8, 9 seeds per generation (redrawn every generation, none reused,
none shared with the holdout), field = shipped (frozen zero-dial agent), carrot_25, melon_heavy, both
seatings, objective Elo expected score (win + 0.5×draw), holdout 24 seeds never used in any
generation, 144 games per row. Common random numbers within a generation. Resolution limit stated up
front: 9 seeds × 2 seatings = 18 duel games per candidate, one game = 0.056 of the duel score, sampling
sd of a coin-flip duel ~0.12 — with 11 candidates a generation, the best sits ~1.5 sd above 0.5 on
noise alone; only large effects are findable, and the 48-game held-out draw is the arbiter.

Generation-by-generation results, held-out confirmation, and verdict are all recorded as RESULTS
PENDING in the source file, with no completion found elsewhere in `docs/` as of 2026-08-22.

---

## 8. The fourth quadrant / land economics

### 8.1 Is there a narrow path to a fourth quadrant? (first pass)

Source: `fable_fourth_quadrant_2026-08-15.md`. Carries a SUPERSEDED banner: `fable_fourth_quadrant_reopened_2026-08-15.md`
(8.2), same day, retracts this file's closing argument — real ladder seats show a 100-tile quadrant
is worked with the SAME hire count as a 75-tile one (277 season hires either way), so the ~$21,960
marginal-crew cost below prices a plan nobody plays.

Verdict as originally stated: no path at quadrant scale, closed by the fibonacci hire curve, not the
bank. Crewing 25 new tiles costs ~$21,960 in marginal hires over d12–29 against a measured marginal
crop value of $6,039 (wheat) or $15,298 (tomato, best realistic conditional case). One sliver
survives: a conditional partial planting of ~8 tomato tiles in 5–26% of games, operationally
unreachable while `cover.py` cannot seat the harvest jobs it already builds.

Cost and timing: the fourth parcel is the third purchase (`LAND_ORDER = ["NE","SW","SE"]`,
`LAND_PRICES = [1000,2000,4000]`, `reference/kaggriculture.py:96-97`) — $4,000, SE. Earliest covered
turn d11, alongside the third parcel; d11 currently closes at $12,699 after seeds $2,380, animal $800,
hires $376 and the $2,000 parcel, and adding $4,000 still closes ~$8,700 (d12 closes $16,246, d14
$21,799) — no scheduled purchase is starved, so affordability is not the question.

Can the crew work it: working 25 wheat tiles in steady state needs ~35 work ops/day (25 water + ~5
plant + ~5 harvest) plus ~25–28 moves, ~60–65 unit-turns/day, ~2.6 dedicated hands. The schedule
already hires 12 hands/day at $376 = sum(fib(0..11)) exactly. Marginal hand costs: 13th $233/day, 14th
$377/day, 15th $610/day (3 extra hands = $1,220/day), over 18 days (d12–29) ≈ $21,960. Against that,
wheat $6,039 or best-case tomato $15,298 — the crew costs 1.4–3.6x everything the quadrant can grow.
The "use the idle instead" escape is refuted by measurement: d9–29 idle is 979 turn-slots against the
tape's 383, yet 16 tiles a season die holding units (11 with a HARVEST job built on their one safe day
that was not seated), and `cover.py` contains zero references to `max_lifespan_step` — idle turn-slots
are positional, not fungible into located, deadline-day work.

What it would grow, on the real seed-11 book: wheat (+25 tiles from d12 = 3 cycles × 4u = +300
units), marginal revenue via `scripts/optimal_release.py`'s season model: baseline optimal 531u →
$11,710 ($22.1/u); with +300u, 831u → $17,749, marginal $6,039 = $20.1/u. Net: $6,039 − $750 seeds −
$4,000 land − $21,960 crew ≈ −$20,700, CLOSED (even at the ladder-realised $45/u wheat, 300 units
gross $13.5k against $26.7k of costs). Tomato, conditional on d12-visible shop draw: 0-visible (31.3%
of games) 32u $2,183 / 100u $6,324 / 200u $10,324. 1-visible (42.2%) $2,773 / $8,179 / $15,121.
2-visible (21.4%) $6,178 / $15,298 / $24,012. 3+-visible (5.0%) $16,043 / $41,423 / $62,588. A full
quadrant of tomato at 2-visible grosses $15–24k against ~$27k of land+seeds+crew — still negative.
Only the 3+-visible tail (5% of games) covers costs, and the shed's 100-item cap makes a 200u hold-to-
d29 dump infeasible.

The sliver that survives arithmetic: conditional partial use, buy the parcel at d12 only when 2+
tomato-stocking instances are visible (26.4% of games), plant ~8 tomato tiles, crew from existing idle
(no 13th hand). 2-visible: 32u → $6,178 − $4,000 land − $400 seeds = +$1,778 (21.4% of games).
3+-visible: 32u → $16,043 − $4,400 = +$11,643 (5.0% of games). Unconditional EV ≈ +$960/game. But
tomato's risk (two missed waters = WEED) is the same seating problem in a different costume, requires
agent code that does not exist (conditional BUY_LAND, SE routing), and ~$1k/game EV is under the
seed-noise floor (~15%) — could not be measured cleanly.

Bottom line as originally stated: marginal crew for a workable quadrant −$21,960; best full-quadrant
crop value (realistic) +$6,039 wheat / +$15,298 tomato 2-visible; full quadrant NO in every bucket
except a 5% tail where the shed cap and seating defect both still bite; conditional 8-tile sliver
+$960/game EV on paper, unreachable until the router can seat deadline-day jobs. The same
crew-seating defect that (per this file) kills the fourth quadrant is already costing 16 dying tiles
a season in the three quadrants already owned.

### 8.2 The fourth quadrant, reopened against the 2026-08-14 field

Source: `fable_fourth_quadrant_reopened_2026-08-15.md`, same day as 8.1. Data: 60 fresh episodes
(120 seats), extracted to `data/logs/fable_field_seats.jsonl`.

The $21,960 crew number: RETRACTED as the closer. That number priced full cultivation of 25 new
tiles bought with marginal hires on the fib curve; the field does neither. All three 100-tile seats
run 277 season hires — zero more than the 75-tile seats (264–277). Plant ops d13–29: 100-tile 100 vs
same-script 75-tile 107; waters 616–628 vs 649–655 — the quadrant is worked by relocating the same
ops, not adding any. SE utilisation: ~5–11 planted tiles (of 25) plus 3–4 pens, weeds 0–4 — half the
ground stays empty, and extra unreachable tiles are worth zero, not negative, because nobody plants
what they cannot water. What the fixed-ops quadrant actually buys is slots the full 75-tile board
cannot host: every 100-tile seat carries 18 animals against the 75-tile seats' 14 (the +4 are SHEEP,
in SE, from d12), plus 6–8 planted tiles of headroom. SE crop is WHEAT in all three games (tile-days:
wheat 110–129, sheep 56–62; nothing else) — consistent with wheat's own starved book paying ~$45/unit
needing no premium story. What survives of the original answer: nothing at quadrant-cultivation scale
was ever the play, and the seating/deadline risk still applies to whatever IS planted there (weeds
1–4 appear in SE in two of three games).

The selection problem, mechanism measured: not bank selection, not a symptom of a rich first half.
The script family emits BUY_LAND at d6h5 and d11h1 in all 17 cluster games; the d12h1 order for the
4th parcel fires only in the three games ending at 100 tiles. Every 75-tile seat had $13,173–$15,480
at d12h1 (ample for a $4,000 parcel) and did not order; the three that did order held
$7,953–$10,425, the poorest of the cluster at that turn (they had just bought extra animals) — wealth
anti-selects, so the purchase is a deliberate conditional in the script, not a wealth effect. Before
any divergence (d10), the eventual-100 games sit inside the 75-tile money range (16,363 vs
[15,253..17,282]) — the d1–d12 trajectory is not already better. The trigger could not be pinned from
17 games: not yarn count alone (100T draws yarn 2,1,1; five 75T games also show yarn=1), not
milk-carrier count, not bank. What is unambiguous: the parcel fires as one package with the herd
expansion (+1 animal by d12, +4 by d18, all sheep, all in SE, wheat around them).
Consequently the headline gap (100-tile mean $131,344 vs 75-tile $89,229) is mostly the trigger's
selection, not the parcel — the script buys in games its condition says are good for an expanded herd,
and those are exactly the games wool/milk print in; cross-game comparison overstates the parcel
5–10x. The cleanest causal number: the within-game pair 92816217, a 75-tile variant (s0, fp a014,
$120,160) and a 100-tile variant (s1, fp fe64, $127,645) of the same meta-script family against the
same market, same draw: +$7,485 for the expansion package. One pair, not a proof, but it agrees with
the bottom-up arithmetic: 4 extra sheep on a wool-friendly draw ~ $8–15k gross minus $2,000 animals
minus $4,000 land minus ~zero marginal crew.

The buy rule, if adopted: conditional, at d12, as a package — $4,000 parcel + 4 sheep + relocate ~8
wheat plantings onto SE. Never unconditional (75-tile is the majority mode of the best scripts, 14 of
17 cluster games, and the field's top-vs-bottom split shows tiles/herd do not separate seats on
average). Trigger, since the field's own trigger is unreadable at n=3: the draw must support the
extra herd's output. Given a prior calibration measurement (8 sheep on 1 yarn floods by 61 units, wool
$35; on 2 stores $243), the defensible trigger is 2+ YARN_STORE visible by d12 for the sheep package
(P ~8% of games), or, per the earlier conditional-tomato work (8.1), 2+ tomato-stocking instances by
d12 (P ~26%), in which case the ground takes gated tomato stops instead of wheat and the timing lines
up exactly (parcel d12, plant d12–13, first fruit d20–23). Bank is never the constraint. Expected
value if the trigger fires: ~+$7.5k (within-game pair) against seed-noise of ~15% of an ~$150k season
— real but small, inheriting the same seating discipline the quadrant's own weeds (1–4 even in the
field's games) warn about.

Corrections to the previous answer, stated plainly: (1) $21,960 marginal crew retracted — it priced a
plan no one plays; the field's marginal crew cost is zero by relocation. (2) "Extra tiles that cannot
be reached are worth negative" was wrong in practice — nobody plants them, so unreachable ground is
worth zero minus the $4,000 gate. (3) "No path" becomes "there IS a narrow path", the one the best
seat in the field (One-For-All, $143,621) walks: a conditional d12 package of land + sheep + relocated
wheat, in a minority of games, honest value ~+$7.5k per triggered game, not the +$42k the raw
100-vs-75 means suggest. (4) What the original answer got right and keeps: affordability was never
the question, full cultivation is uneconomic, and the cross-game bank gap is selection — the instinct
to distrust the n=3 comparison was correct, just with wealth-selection replaced by trigger-selection.

---

## Cross-cutting notes

- **The Seb/rebase-target contradiction** (flagged in section 1.3) is the one standing unresolved
  item across this whole topic: the 2026-08-11 population-scale measurement named Dmitry Belan or
  Efe Can Celiksoy as the rebase target, not Seb, and nothing since has switched the target.
- **The middle-game capacity question was answered twice, in opposite directions, on the same day**
  (`kawashigi_algorithm_2026-08-21.md` then `the_middle_is_not_board_capacity_2026-08-21.md`) — see
  section 3.2/3.3. The later file's retraction stands, and the reconciliation in
  `the_opening_is_a_tape_the_middle_is_two_regimes_2026-08-21.md` (3.4) explains the disagreement as
  a pooling artifact rather than a contradiction in the underlying data.
- **Two allocation-search efforts ran in parallel on 2026-08-15/16**: the CEM search (section 7)
  never reported a result and its status is unconfirmed as of 2026-08-22; the MILP-based allocation
  bounds work (sections 6, 6b) did complete and is the current answer to the same question.
- **The fourth-quadrant question was answered twice on 2026-08-15**, with the second pass (8.2)
  explicitly retracting the first pass's (8.1) closing number after checking it against real ladder
  seats rather than a hand-built cost model.
