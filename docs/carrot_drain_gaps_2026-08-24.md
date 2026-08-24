# Carrot drain gaps closed — 2026-08-24

Two gaps in the drain-11 hard-conversion measurement, closed with numbers.
Method unchanged from `docs/the_optimal_carrot_2026-08-24.md`: `scripts/the_optimal_carrot.py`,
handover d20, `corner_the_book.plan` replaced by a forced tile count from d21, tiles `0,16,32,56`.
Both tapes replayed verbatim to the handover, so board and market are real; only what our agent
does from d20 onward is counterfactual.

## A bug found and fixed en route

`scripts/does_the_book_reading_win_games.py::_find(ep)` took `rglob(...)[0]`, the first filesystem
hit for an episode id, with no check that the hit was a real replay.
`data/seed_scripts/field_leaders/*.json` (and similarly-shaped dirs) hold a lightweight per-game
summary — keys `team, episode, seat_in_recording, their_money, our_money, actions` — filed under
the same episode id as the real download elsewhere in the tree.
`field_leaders/91108446.json` sorted before `top_guys/91108446.json` and the script crashed on
`rec["info"]` (`KeyError: 'info'`).
Fixed to skip any hit lacking both `info` and `steps`.
Diff is in this worktree, uncommitted, at `scripts/does_the_book_reading_win_games.py`.

## Corpus scan

`scripts/full_corpus_drain_scan.py` (new, this worktree), log
`data/logs/full_corpus_drain_scan_2026-08-24.log`, CSV `data/logs/full_corpus_drain_scan.csv`
(copied here as `data/logs/full_corpus_drain_scan_2026-08-24.csv`).

**2,364 files under `data/seed_scripts/**` scanned. 2,164 parsed as full replays (`info` + `steps`
present) and scored; 200 skipped — the `field_leaders`-style summary format above, which carries no
`steps` to compute a drain from.** Drain computed at day 29 (or the final step if the episode ended
earlier), same formula as `does_anyone_read_the_carrot_drain.py`: a shop selling ONLY carrot drains
2/tick, any other carrot-carrying shop drains 1/tick.

Drain histogram, one row per seat per game (so up to 2 rows/game):

```
  drain    0    1    2    3    4    5    6    7    8    9   10   11
  rows   454  562  918  850  740  402  228   94   44   30    0    6
```

## GAP 1 — the 7-10 band

**Drain 7, 8 and 9 all exist. Drain 10 does not appear anywhere in the 2,164 replays scanned.**
Not "rare" — zero rows, zero games, out of every full replay on disk as of this scan.
Whether drain 10 is combinatorially reachable at all was not checked here (it would need summing
achievable `PET_CAFE`/`FARMERS_MARKET` unlock counts against the shop-slot cap); what is measured
is that it has never been recorded.

Of the drain-7/8/9 games, **only drain 7 and 8 have "alex chilton" as a seat** — 7 real games (a
duplicate scan hit doesn't create an 8th). **No drain-9 game has us as a seat**, so drain 9 cannot
be measured with our own agent at all — the corpus holds 30 drain-9 seat-rows and none of them are
ours. Games where we ARE a seat, drain 7 or 8, grid at d21 (`margin / carrot units at d29`):

```
  episode     drain   recorded    0 tiles      16 tiles      32 tiles      56 tiles
  92086977      8        -70      -4,513/2     -8,791/3      -8,730/3     -10,138/29
  92003395      7      -9,958     -8,691/6    -17,499/6     -16,795/6     -17,825/36
  93589061      7      -9,371    -22,272/0    -86,200/3     -86,200/3     -86,200/3
  93600838      8      +6,778       +123/2     -2,410/3        +119/3      +3,635/36
  91108446      7     +11,763      +2,720/3    -5,081/0      -4,009/2      -3,137/40
  91118031      7     +82,245     +86,989/0    +82,169/0     +79,372/0     +78,201/18
  91133805      8      -8,488      -2,689/3      -461/0     +13,282/0     +19,233/28
```

**Drain 7-8 is not a clean "yes" or "no." It is genuinely mixed, board by board:**

- Two losses where conversion never helps at any tile count: `92003395` (worst at -17,825),
  `93589061` (catastrophic: identical -86,200 at 16/32/56 tiles — three different tile counts
  landing on the exact same number is itself a flag; not diagnosed further here, but it does not
  look like ordinary opportunity cost and is worth a separate look before trusting this row).
- One near-tie loss, `92086977` (-70 recorded), where conversion makes every tile count worse —
  best is 0 tiles.
- One win that gets bigger with hard conversion: `93600838`, +123 -> +3,635 at 56 tiles, +$3,512.
- One **loss that FLIPS to a win**: `91133805`, -2,689 -> +19,233 at 56 tiles, a $21,922 swing.
- One **win that FLIPS to a loss**: `91108446`, +2,720 -> -5,081 at 16 tiles, and stays negative at
  32 and 56.

So at drain 7-8 the policy helped once (flipped a loss), hurt once (flipped a win), and did nothing
useful on the other five. That is a materially different picture from drain 11 (one clean, large
win in the established table) and from drain 2-6 (uniformly costly). **The 7-10 band is not "the
same as 11, just weaker" — it is closer to a coin flip, board-dependent, with both directions of
flip observed.**

## GAP 2 — games we won

Filtered `is_us=1 AND team=="alex chilton" AND us_won=1` from the corpus scan. **Two of the
episodes I initially selected, `91100032` and `94253360`, turned out to be self-play fixtures — both
seats are "alex chilton," `info.seed == 0` on both — not real ladder downloads. Caught by the sign
flipping on which "seat" counted as `us` between duplicate directory copies; excluded from
everything below.** `94003432` (drain 7, also both-seats-us) was excluded from the start on the
same basis, per the standing "farms[1] is not the tape" caution about mirror matches.

Seven real won games survived, spanning drain 0, 2, 4, 7 (x2), 8, 11 — grid at d21:

```
  episode     drain   recorded    0 tiles      16 tiles      32 tiles      56 tiles
  91125915       0      +1,069    +10,401/6     +1,778/3      +2,421/3      -1,867/17
  93595439       2        +155   -11,679/0    -22,261/0     -23,094/3     -30,069/18
  91034266       4        +532     +2,273/0    -2,188/3      -2,714/2      -3,920/20
  91108446       7     +11,763     +2,720/3    -5,081/0      -4,009/2      -3,137/40
  91118031       7     +82,245    +86,989/0    +82,169/0     +79,372/0     +78,201/18
  93600838       8      +6,778       +123/2    -2,410/3        +119/3      +3,635/36
  93608944      11     +10,136     +1,308/3      -260/0      +7,965/0     +11,973/30
```

**Caveat that applies to every row here and to the established six-loss table equally**: the
"0 tiles" harness baseline does not reproduce the recorded margin — it is what our *current*
agent does taking over at d20, which can differ from the recorded outcome by a lot and in either
direction (`93595439`: recorded +155, harness baseline -11,679 — a $11,834 swing before any carrot
arm has acted at all). `docs/the_optimal_carrot_2026-08-24.md` already flagged this for one game
("kind to us by $4,193"); here it runs from -$12,901 to +$9,332 across seven games. **Read the
paired arm-vs-0-tiles delta, never the arm vs. the recorded margin** — that was already the rule,
this just shows the bias is large and not one-directional.

Judged against each game's own 0-tile harness baseline (the fair counterfactual):

- **`91034266` (drain 4): a real win, harness agrees (+2,273), and 16 tiles alone flips it to
  -2,188.** This is the clean demonstration that firing below the proven threshold can cost a game
  we were actually winning.
- **`91108446` (drain 7): win, harness agrees (+2,720), 16 tiles flips it to -5,081** and it stays
  negative at 32 and 56. Same failure mode as above, one drain band closer to where the mechanism
  is supposed to start paying.
- **`93600838` (drain 8): win, harness barely agrees (+123). 16 tiles flips it to -2,410, but 32
  tiles recovers to +119 and 56 tiles improves it to +3,635.** Non-monotonic — the *weak* arm is
  the dangerous one here, not the *hard* one.
- **`93608944` (drain 11): win, harness barely agrees (+1,308). 16 tiles flips it to -260 (small),
  but 32 and 56 tiles not only recover, they roughly double the win (+7,965, +11,973).** This is
  the one row that matches the established drain-11 story cleanly: going big, not weak, is what
  pays.
- **`91125915` (drain 0) and `93595439` (drain 2): both lose money at every tile count tested**,
  consistent with the established drain 2-6 finding. `93595439`'s own harness baseline is already
  negative (-11,679) before any arm acts, so "flip" isn't well-defined there — see the bias caveat.
- **`91118031` (drain 7, +82,245 margin): never flips, at any tile count** — the win is too large
  for $10k-ish of carrot-policy risk to touch.

**The risk is real and it is not simply "small below the threshold, none above it."** Every drain
band tested (0, 2, 4, 7, 8, 11) produced at least one arm that turned a real win into a harness-loss
at 16 tiles, INCLUDING drain 11 itself. The one thing that held across every winning game tested:
**16 tiles (the "weak" arm) was never better than doing nothing, and was the single worst arm on
4 of 7 games.** Going further (32/56 tiles) sometimes recovered (drain 8, drain 11) and sometimes
didn't (drain 0, 2, 4, 7-weak-margin-game).

## Best answer to "at what drain does hard conversion start to pay, and what is the risk below it"

**Not measured as a clean threshold.** The established table (six losses, drain 2/3/6/11) said hard
conversion pays at drain 11 and costs $10k-$20k at drain 2-6, monotone in tile count. That still
holds for those six games. What this pass adds:

- **Drain 7-8 does not extend the drain-11 story.** Across 7 real games at drain 7-8, hard
  conversion flipped one loss to a win (+$21,922) and one win to a loss (-$7,801 swing), and did
  nothing useful on the other 5. It is not a weaker version of "pays" — it is a coin flip with real
  money on both sides.
- **Drain 9 cannot be measured with our own agent** — 30 drain-9 rows exist in the corpus, none of
  them ours.
- **Drain 10 cannot be measured at all** — it does not occur once in 2,164 scanned replays.
- **The risk below the proven threshold (11) is not confined to low drain.** It showed up in every
  band tested, drain 0 through 11, and the specific arm that lost the most often was the *weak*
  one (16 tiles), not the *hard* one — a rule that fires small when it fires at all would be
  choosing close to the worst-measured option, not a cautious compromise.
- The one board-independent regularity: **when hard conversion (32-56 tiles) does pay, it pays by a
  lot (drain 8: +$21,922 loss->win; drain 11: win roughly doubles), and when it doesn't, going
  bigger rarely makes it much worse than the weak arm already made it.** So *if* a gate decides to
  fire, sizing it big rather than small is the safer half of the decision — the dangerous choice
  measured here is firing weak, not firing hard.

## What was not done

- `93589061`'s identical -86,200 result at three different tile counts was flagged, not diagnosed.
- No attempt was made to determine whether drain 10 is combinatorially reachable under the shop
  unlock rules — only that it has never been recorded.
- Only d21 as a start day was tested here (matching the established table's method), not the fuller
  start-day sweep `the_optimal_carrot.py` supports.
