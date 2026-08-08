# We lose by overselling into a book the opponent is already filling

2026-08-09, on `shaping-potential`.

Artifacts: `scripts/what_we_should_have_sold.py`, `scripts/less_or_slower.py`,
`data/logs/what_we_should_have_sold.log`, `data/logs/less_or_slower.log`,
`data/logs/opening_0_vs_11.log`, `data/ladder/losses/` (14 games), `data/ladder/wins/` (36).

## The finding

Across 14 real ladder losses, holding the opponent exactly as they played and re-pricing only our
own sales **downward**, **12 of the 14 become wins**. The gaps were tiny — $715, $1,701, $1,969,
$3,361, $4,266 — and the recoverable revenue is $7k-$33k per game.

```
  where the recoverable money is, summed over 14 losses
    WOOL            +135,250
    STRAWBERRY       +57,433
    MILK             +57,163
    MELON             +4,447
    WHEAT                  0
    FERTILIZER             0
```

The prescription is consistent enough to be a rule rather than a fit:

```
  WOOL         0.7x  best in 7 of 14 games (0.6-0.8 in 11)
  MILK         0.5x  best in 4, 0.6-0.7 in 5
  STRAWBERRY   0.7x  best in 6, 0.9x in 4
  WHEAT        1.0x  -- no gain, ever
  FERTILIZER   1.0x  -- no gain, ever
```

Wheat and fertilizer are the two products we sell *most* of by volume and they are correctly sized:
their books are deep enough that our volume does not move the price. Everything recoverable is in
the three thin, steep books.

## It is genuinely LESS, not slower

"Scale every turn down by 0.7" reduces the total *and* flattens the peaks, so the first measurement
could not tell a volume problem from a cadence one — and the two have different fixes. Selling less
means growing less; spacing better means the same farm with a different sell rule.

`scripts/less_or_slower.py` separates them. Our own contribution to the book is known, so the path
the market would have had without us is `base[t] = inv_obs[t] - (our cumulative sales before t)`,
and any counterfactual schedule can be priced against `base[t] + cum_q[t]`. Four schedules, same
production:

```
  total gain over observed, summed across every game and product:
    downscaled  (fewer units, same shape)   +254,293   best in 16 of 56 cases
    spread      (same units, even cadence)   +87,343   best in 16 of 56 cases
    both        (fewer units, even cadence) +252,611   best in 17 of 56 cases
```

**Spreading alone recovers about a third of what cutting recovers, and cutting-plus-spreading adds
nothing over cutting.** So the answer is volume, not cadence — with one clean exception:

- **WOOL is a volume problem, and severe.** 91122388: $5,278 observed, **$23,794** at 0.7x — 4.5x
  the revenue from 70% of the units. Spreading the full volume only reaches $8,614.
- **MELON is a cadence problem.** `spread` wins it in most games (91125047: $11,831 -> $17,115).
- **MILK is both**, with `both` winning in half the games.
- **STRAWBERRY is often already right** — `observed` wins it outright in several games.

## Why wool is the fragile one

`MARKET_PARAMS["WOOL"]` is `above_func: sq`, `above_target: 3.2`, `T: 105`, `base: 200`, so

    price = 200 - (3.2 * 200 / 105^2) * d^2  =  200 - 0.058 * d^2

which reaches the floor at **d = 59 units above I0**. We sell ~200 wool a season and the opponent
sells 140-255 of their own into the same book. The town removes 204 across the whole season, so the
book sits far above the point where wool is worth nothing. Melon is the same shape (`sq`, 3.6,
T=300, floor at d≈158) but its drain is only 30, which is why it is a timing problem rather than a
volume one — there is no volume at which melon recovers.

## We can see their play, and this is how

We cannot see the opponent's orders. We do not need to: `market.inventory` is in the observation
**every turn** and the book is shared, so their selling is visible as the book rising. What is
hidden is their intent; what is visible is their effect, which is the part that costs money.

`schedule_agent.py:2487` reads that book and then ignores this entirely:

```python
n = min(have, reservation_units(
    prod, market_inv.get(prod, ...), day * TPD + hour, unlocked_shops, have + standing[prod]))
```

`reservation_units` prices the book as though we were its only seller. There is no rival-supply term
anywhere in the agent. The same missing quantity appears as `OPPONENT_SHARE = 0.5` in
`scheduler.py` and as Fable's `contest` dial in `docs/fable_market_technique_2026-08-08.md` —
three places, one number, never measured.

## The ladder agrees

Twelve recent games, same agent, price actually realised per unit:

```
  product       base |  OURS-WIN units   $/u |  OURS-LOSS units   $/u |  ALL FOES units   $/u
  MELON          250 |             984   150 |             247   111 |           1,050   153
  WOOL           200 |           1,950   147 |             398   127 |             896   141
  MILK           160 |           2,082   205 |             321    73 |           1,405   161
  STRAWBERRY     120 |           2,711   182 |             562    78 |           1,366   154
  WHEAT           25 |           9,115    45 |           1,693    49 |           7,124    48
```

Wins and losses are indistinguishable in board state — same tiles (97), same herd, same third-parcel
day (11) in every game but one — and differ almost entirely in the price realised on milk and
strawberry. Wheat is *better* in the losses.

## The opening is not the problem

Asked separately, because the shipped agent replays a recorded tape for days 0-10 and it is fair to
ask whether our own planner would do better. Six seeds, weeds 0.005, same opponent:

```
  OUR OWN OPENING (agent drives from d0)     0/6 wins   mean $47,756
  SEB TAPE OPENING (agent takes over d11)    4/6 wins   mean $67,181
```

Our agent driving from day 0 loses every seed by $20k-30k. Keep the tape. Caveat: our agent plays a
schedule written around the tape's board, so this measures "our agent without its opening" rather
than a designed opening — but 0/6 is stark enough not to spend on the distinction.

## Two corrections on the record

**The first version of this analysis was wrong and said every loss was winnable.** It searched
scales up to 1.5x and reported wheat as the biggest recoverable line in all fourteen games
(+$165,070). Scaling a sale *up* means selling goods we never held, and nothing checked inventory.
The sound version only scales down, where feasibility is free.

**Market orders are offers, not fills.** One replay records a 21,216-unit MILK offer. Any model that
adds the opponent's quantities to the book is wrong by whatever the environment refused to fill,
which is why the final version perturbs the *observed* path instead of reconstructing it.
`data/logs/cows_fixed.log` already warned about this.

## What this does not settle

- The opponent is held fixed. A real one reacts, and cutting our supply raises their price, which
  may raise their volume. Read these as an upper bound on the easy win.
- "Sell 0.7x" means the other 30% was grown and then wasted. The selling half is cheap and ships;
  the production half is `revenue_rate` in `kagg/search/scheduler.py`, which is a separate fix and
  is not in the submission at all.

## Addendum — the contested instrument, and what it says so far

Every local number above and in `the_planner_prices_the_wrong_market` came from `scripts/handover.py`,
whose seat-1 opponent is the weak player from Seb's own game. He barely sells, so no book ever
floors and a rule about floored books has nothing to act on but its own cost. That fixture reports:

```
  HOLD_A_FLOORED_BOOK = False    4W/2L   mean $67,181   destroyed 1,421
  HOLD_A_FLOORED_BOOK = True     3W/3L   mean $66,926   destroyed 1,506
```

Flat on money, one game lost, discards up 6% -- against 55 of 62 real games gaining in the replay.
The two instruments are blind to opposite halves of the change and CLAUDE.md warns explicitly about
the first: never evaluate against an opponent who does not contest the market.

`scripts/vs_tapes.py` puts a real top player's own play on seat 1 and had never been run. Partial
result, flags OFF, handover d11, weeds 0.005:

```
  tape        seed        ours        tape  result   margin
  oldleader     11      48,827      57,809  LOSS     -8,982
  oldleader    101      55,159      59,427  LOSS     -4,268
  oldleader    202      67,241      75,419  LOSS     -8,178
  oldleader    303      65,177      71,988  LOSS     -6,811
  seb           11     116,500      18,017  WIN     +98,483
```

**We lose 4/4 to `oldleader` and beat `seb`'s own tape by $98k.** That asymmetry is itself worth
recording: the schedule we ship is copied from Seb, so beating his tape measures execution on a
board we were built for, while `oldleader` is a genuinely different opponent and beats us every
seed. The flags-ON half was still running when this was written; `data/logs/vs_tapes_on_off.log`.

## Addendum — what the field does that we do not

124 seats across 62 games, every lever read off the replays (`scripts/what_the_others_do.py`):

```
  lever          corr w/ money   top 20%  bottom 20%  OURS mean  our percentile
  sell_orders           +0.384       542         300        546             65%
  feed                  +0.359       376         268        391             62%
  harvest               +0.334       324         253        328             48%
  care                  +0.327       385         268        406             63%
  hires                 +0.301        12          11         12             14%
  buy_product           +0.255      1156         750       1068             49%
  herd                  +0.258        17          13         18             69%
  tiles                 +0.149        92          80         99             42%
  plant                 -0.050        95         105         85             24%

  money: ours $73,977   field $68,091   top-20% $116,407
```

**On every lever that correlates with money we already match or beat the top quintile** -- more
feeding, more caring, more sell orders, more tiles (99 vs 92), a bigger herd -- and bank $74k against
their $116k. There is no missing activity. The whole gap is price realised per unit.

The one lever with real headroom is `buy_product` (+0.255, we sit at the 49th percentile against a
top-quintile 1,156), which is OPEN-3's buy-wheat -> feed -> milk conversion: another way to turn a
cheap input into an expensive output, i.e. a price play rather than an activity.
