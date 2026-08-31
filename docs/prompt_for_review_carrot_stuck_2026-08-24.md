# Review prompt: we can see exactly what beat us and cannot reproduce it

Repo: `/Users/alexchilton/DataspellProjects/kaggriculture`
Branch: `corner-the-book` (worktree `.claude/worktrees/corner`), off `e2500-shopprice`.
Background, in this order: `docs/where_we_lose_2026-08-24.md`, then
`docs/fable_where_the_money_is_2026-08-24.md`, then `CLAUDE.md`.

I am stuck and I want the mechanism attacked, not the code reviewed. Where you think a claim below
is wrong, say so and say what measurement settles it.

---

## 1. The game

`kaggriculture`: two farmers, one shared town, 30 days x 24 turns. You bank money selling produce
into a town whose price for each product falls as anyone sells into it and recovers as shops drain
it. **Scoring is Elo. A $1 win scores exactly what a $30,000 win scores.** Ground truth for every
rule is `reference/kaggriculture.py`.

Our agent is a deterministic day planner, not a policy: at hour 0 it plans the whole day for every
unit, then executes. It never replans mid-day.

## 2. The price mechanism, which I believe is fully established

Price is a pure function of the town's inventory (`reference/kaggriculture.py:192-207`). Inventory
starts at `I0 = 10_000` for every product and moves three ways only: each unit either side sells
adds one, and the shops drain it on a fixed schedule (`_town_consume`, 6 ticks/day per shop
instance, doubled for a single-product shop, +1/day town centre).

Define the deficit `D = I0 - inventory`. Since the 2026-08-15 balance change CARROT, TOMATO and EGG
are on a `hinge` curve (`reference:43-47`, `_shape` ~line 61):

    u = D / T ;  f = u + 8.0 * max(0, u - 1)^2 ;  price = base * (1 + target * f)

CARROT is `base 35, T 450, target 1.00` -- the largest `target` of the three. Verified against a
real tape: d25 of game 98495047 reads `market.inventory[CARROT] = 9261`, so D = 739, u = 1.64,
f = 4.92, price $207. The town quoted **$208**.

`market.inventory` is in the shared observation, so both players can read the deficit exactly, every
turn.

## 3. What beat us, read off his tape

Ladder game 98495047, seed 1640915609. We lost by **$29,384**, and every dollar arrived on d29.
We were AHEAD by $542 at the end of d28.

    d21   0 carrot tiles,   0 held,  carrot $96
    d24  10 carrot tiles,   0 held,  carrot $208
    d26  32 carrot tiles,   3 held,  carrot $343
    d28   0 carrot tiles,  76 held,  carrot $523
    d29  sold 76 units at ~$498                       $37,848 on the final day

    holdings entering d29:  ours 73 units / $5,607     theirs 100 units / $37,842
    our season carrot:      11 units sold for $4,714 (i.e. $429/unit -- our PRICE was fine)

So: abstain from the book, convert ~32 tiles late, withhold everything, dump on the last day. The
book did not collapse under his own dump -- it closed at $498.

Across six downloaded losses, five were lost entirely on d29 and we led at d12 in all of them.
Only two of the six were carrot towns (drain 11 and 6); the other four had drain 2-3 and closed
carrot at $50-59.

## 4. What we built

- `kagg/search/corner_the_book.py` -- replaces two constants with the deficit projection.
  The old rule was `CARROT_DRAIN_MIN = 5` (measured over 12,096 seasons, sound) **and**
  `CARROT_OPP_MAX = 7` (never measured -- no pool opponent has ever withheld stock, so six of nine
  arms in that sweep were identical by construction; `docs/carrot_refine_2026-08-22.md` says so).
  `CARROT_OPP_MAX` is what stood us down on 98495047: the opponent held 10 carrot tiles.
  The new rule projects D forward to d29, subtracts what both seats will still supply, fires if
  `u > 1.3`, and sizes the position so the book stays above the knee after our own dump.
  16 tests, green, run against the six REAL observations: fires on the drain-11 and drain-6 towns,
  stands down on the four drain-2/3 ones.
- `kagg/agents/morph.py` -- our own shipped agent, parametrised, so the opponent field can finally
  contain a withholder. A heuristic cannot do this job: `heuristic(filler_crop=CARROT,
  hold_days=6)` held 66 units, carrot never left $23-28, and we beat it by $166,256.
- `carrot_hinge` added to the pool's `COMPETITIVE`. Note the old gate score of `94.4%` was
  `(8 * 1.0 + 0.5) / 9` exactly -- an identity for "beats every member, draws itself", saturated
  and unable to move.

## 5. What we measured, including the part that failed

**The opponent family reproduces the SHAPE and beats us.** Same seed, our agent in the other seat:

    swap_from  tiles@d26  held@d28  close$  deficit    margin
        14        30        135      211      743     +12,194   over-commits, LOSES
        16        30        135      402      913     -19,844
        18        29        130      286      818      -5,828
        20       111 units held ...  282      814     -14,117
    Mr Carrot     32         76      498      975     -29,384

and on two non-carrot towns the identical configuration loses by $24k-40k. Same parameters,
opposite sign, which is the town-dependence the deficit rule is supposed to capture.

**But the acceptance run flips nothing.** Paired replay of the six losses, both tapes replayed
verbatim to a d21 handover so the board and the BOOK are real, then our agent plays out. Control is
the shipped two constants; treatment is the deficit rule:

    episode    recorded    control      treat   flips
    98495047    -29,384     -5,313     -5,313     0
    98460892       -614    -11,885    -11,885     0
    98494953     -3,472    -24,350    -24,350     0
    98499540     -1,940    -11,229    -11,229     0
    98501831     -6,070    -12,887    -12,887     0
    98428765     -1,783    -13,942    -13,942     0

Two things in that table:

1. **Widening `CARROT_SWAP_DAYS` from (25,26,27) to d21-d27 is worth $17,788** on 98495047 -- it was
   -$23,101 in both arms before. CARROT is `first_yield_day 2`, so d27 tiles cannot ripen before
   d29; a third of the old window was dead. That gain is from the window, NOT from our new rule.
2. **The new rule now contributes exactly nothing.** Control and treatment are identical everywhere.
   The decision is latched ONCE on the first day of the window; that is now d21, and at d21 the
   opponent has not planted any carrot yet, so `CARROT_OPP_MAX` passes trivially and both rules
   agree. Widening the window destroyed the only case where the rule differed.

Also note the handover harness makes us much worse than the recording in every game (-$24,350 where
the tape lost $3,472). The paired comparison is still valid; the LEVELS are not.

## 6. What I cannot explain about his tape -- this is the real question

Alex's challenge, and I think it is right: if we cannot reproduce it, the model may be half a
mechanism.

- **Where did his ground come from?** 32 tiles is a large late commitment. Did he stop planting
  something else, clear spent one-shots, or was he holding empty ground all along?
- **Why only 2.4 units per tile?** 32 tiles at `max_yield 4` is 128 units; he banked 76. He was not
  even filling them. Does that mean tiles were sown very late purely as inventory, or that he was
  harvest-turn limited?
- **His deficit reached 975, ours stalls at ~850.** Deficit is drain minus BOTH sides' sales. In
  that game the loser (us) sold only 11 carrots all season. Our own schedule sells carrot on
  d21/22/24/25 -- so in our replays *we* keep refilling the book we are trying to starve. Is
  abstention on our own side the missing half, and is it separable from the cornering?
- **Is 32 tiles even the operative number**, or is the whole thing about the d29 sell schedule --
  how many turns, starting at what hour, at what order size?

## 7. Questions

1. Attack the frame first. Is "corner a hinge book by abstaining then dumping" actually what won
   that game, or is it a coincidence of something else -- crew turns, land, a better d24-d28 harvest
   -- that I have mistaken for a market play?
2. If it is the right frame: what is the missing half that gets 32 tiles and D = 975 rather than
   14 tiles and D = 850?
3. When should the fire/size decision be READ? Latching at the first window day is now clearly
   wrong. Re-read daily? At a fixed day? On a trigger?
4. Elo, not money: is cornering even correct strategy against a FIELD? If both players corner, does
   it self-destruct, and does the answer change what we should ship? (A mirror match is explicitly
   not a best response in this project -- it has misled us before.)
5. What single measurement would you run next, and what result would tell you the whole line is
   wrong?

## 8. Reproducing

    python -u scripts/does_the_book_reading_win_games.py --handover 21
    python -u scripts/find_the_carrot_algo.py --seeds 1640915609,700,701
    python -u scripts/where_the_game_is_lost.py 98495047
    python -u -m pytest tests/test_the_book_is_cornered_only_when_it_is_deep.py -q

Replays are in `data/seed_scripts/losses/`. **They are SELECTED losses** -- never compute a win rate
from them. Prices are endogenous: the same seed that paid $270 for milk in a recording paid $1 in a
rematch from turn 0, which is why every measurement above replays both tapes rather than
re-simulating the season.
