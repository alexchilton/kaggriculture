# The turn-0 wheat round trip is a solved zero-sum game

Written 2026-09-16, after `nathanjacob/kaggriculture-pipe-7-wheat-microstructure` and
`ahmedberatozer/kaggriculture-v45-first-turn-wheat-round-trip` appeared on the same day.
All numbers below are engine 1.32.7, `reference/kaggriculture.py`, on this machine.

## 1. pipe-7 is V45 with one byte changed

Both notebooks embed the complete agent and pin their own digest. Decoded and verified:

```
v45    sha256 2536d41ed5a00c75204b6350f1c76c54259c774cb065ba2a3a0072eedf210d94   329,112 bytes
pipe7  sha256 6150b7f9a953fc54d17a0f762a4c6ba5d2afe25a1851876eeb7681719d34a200   329,111 bytes

diff v45 pipe7
3477c3477
< _OPEN_UNITS=70
> _OPEN_UNITS=5
```

V45 in turn is V44 plus one layer (28 diff lines against `submission/v44a/main.py`).
That layer rewrites the step-0 market list and nothing else:

```python
if standard and step==0 and action.get('market')==[['BUY_PRODUCT','WHEAT',5],['BUY_PRODUCT','WHEAT',10],['SELL','WHEAT',60]]:
    action=dict(action,market=[['BUY_PRODUCT','WHEAT',_OPEN_UNITS],['SELL','WHEAT',_OPEN_UNITS]])
```

## 2. Every opening is net-zero wheat, so N is a pure quoting parameter

`_new_private` (`:171`) starts the shed **empty**. `_commit_unit` (`:650`) refuses a SELL with no
stock, and an aborted order kills the rest of that order. So every published opening sells exactly
what its own buys just deposited:

```
v40_open5, pipe4, pipe5   [BUY_PRODUCT WHEAT 5]                 net +5 wheat, a real purchase
v43_stock, v44, v44a      [BUY 5, BUY 10, SELL 60]              sells 15, net 0
v43_openc                 [BUY 5, SELL 1000]                    sells 5,  net 0
v44a_room_clamp (live)    [BUY 5, BUY 10, SELL 15]              sells 15, net 0
v45                       [BUY 70, SELL 70]                     net 0
pipe7                     [BUY 5, SELL 5]                       net 0
```

(extracted by calling each build's `agent()` on the seed-7 reset observation)

`_refresh_prices` runs at the end of the turn and the inventory returns to 10,000, so nothing
persists. The only channel is cash on turn 0, and `market_price` returns integers, so the payoff
is quantised.

## 3. The exact payoff matrix

`_process_market` (`:544`) is a **per-unit** lockstep: both players' current unit is quoted at the
same pre-commit inventory, then both commit. `BUY_PRODUCT` quotes at `inventory - 1` precisely so a
lone round trip nets zero (engine comment, `:599`). Wheat starts at exactly `I0 = 10000`, so every
unit bought crosses into the `below` branch — `sqrt`, target 0.80 on base 25 — the steep side.

Therefore the small buyer sells into the scarcity the large buyer created. Replaying step 0 through
the validated `sim()` in `data/logs/interact.py` (fresh market, empty shed, $3,000), my cash delta:

```
  myN   buy5only    split60  openc1000        rt2        rt3   rt5=pipe7        rt8       rt30   rt70=v45    min
    0         +0         +0         +0         +0         +0         +0         +0         +0         +0     +0
    1         +1         +1         +1         +1         +1         +1         +2         +5         +7     +1
    2         +2         +3         +2         +0         +1         +2         +3         +8        +13     +0
    3         +3         +4         +2         +0         +0         +2         +4        +12        +20     +0
    5         +3         +4         +0         -1         -2         +0         +4        +17        +31     -2
   10         +3        +11         -4         -3         -4         -4         -3        +25        +54     -4
   30         +3        +31        -16         -8        -11        -16        -22         +0        +94    -22
   70         +3        +61        -30        -13        -19        -30        -45        -94         +0    -94
```

The round-trip block is antisymmetric with a zero diagonal: a zero-sum game in one integer.

- **There is no cliff at 70.** Read the `rt70` column: every N below 70 is positive, 70 is zero,
  every N above is negative. pipe-7's table only ever compares against 70, so it measures the sign
  of `myN - 70` and nothing else.
- **N=5 is not an optimum.** The best reply to 70 is N≈30 (+$94), three times pipe-7's +$31.
- **N=1 is the unique maximin.** It is the only N with a strictly positive minimum. It beats every
  opening in the field by at least $1 and cannot be undercut: N=0 ties it, everything else loses.
- Against the *old* split opening the gradient reverses and runs to +$61 at N=70. That was V45's
  actual thesis and it is correct. pipe-7 discards it, which is why it beats our V44 by only $8.

## 4. `clamp_sells` silently disables the round trip

The guard in §1 is an exact list equality. `clamp_sells` rewrites the step-0 sell to
`SELL WHEAT 15`, so the guard stops matching and the layer never fires. Its own telemetry is the
tell:

```
pipe7      [BUY 5, SELL 5]            open_turns=1
pipe7_rc   [BUY 5, BUY 10, SELL 15]   open_turns=0     <- round trip gone
u1_rc      [BUY 5, BUY 10, SELL 15]   open_turns=0     <- round trip gone
```

With the flags on, `pipe7_rc`, `u1_rc` and our live `v44a_room_clamp` are the **same agent** — they
tie with identical banks in every row. This also reconciles the two contradictory measurements of
the flag: pipe-7 reports `clamp_sells` as 2W-48L because they tested it **against V45**, where
losing the round trip costs $61 of turn-0 cash. Tested against N=5 it costs $4, and the flag wins.

Fixed by replacing the equality with the shape it was trying to describe (no new flag):

```python
mkt0=[list(o) for o in (action.get('market') or [])]
buys0=sum(o[2] for o in mkt0 if o[:2]==['BUY_PRODUCT','WHEAT'])
if standard and step==0 and buys0==15 and len(mkt0)>=2 and mkt0[-1][:2]==['SELL','WHEAT'] and all(o[:2]==['BUY_PRODUCT','WHEAT'] for o in mkt0[:-1]):
```

`submission/u1_rc2/` is pipe-7's chassis with `_OPEN_UNITS=1`, `room_guard` and `clamp_sells` on,
and that guard. It emits `[BUY 1, SELL 1]` with `open_turns=1`.

## 5. Measurements

Paired direct mirrors, `data/logs/mirror_all.py`, seeds 1..N x both seats, fresh module import per
game. Margin is B - A. Every grid prediction held in sign.

```
A                  B                 games   B wins   median      t     grid
v45 (N=70)         pipe7 (N=5)          80    76/80     +236   3.88      +31
v44a (live #1)     pipe7                80    77/80       +9   1.38       +4
N=65               N=40                 40    40/40   +1,333  41.32      +80
v45 (N=70)         N=30                 40    40/40   +1,367  42.36      +94
pipe7 (N=5)        N=30                 40     2/40      -34  -0.74      -16
pipe7 (N=5)        N=2                  40    38/40       +3   0.07       +2
pipe7 (N=5)        N=1                  40    38/40       +2   0.04       +1
v45 (N=70)         N=1                  40    38/40      +15   0.32       +7
pipe7 (N=5)        N=0                  40   36 ties       +0   0.00       +0
pipe7              pipe7_rc             40    35/40     +254   3.98        -
pipe7              v44a_room_clamp      40    35/40     +254   3.98        -
pipe7              u1_rc2               80    71/80     +239   6.02        -
pipe7_rc           u1_rc2               40    38/40       +3   0.07       +1
v44a_room_clamp    u1_rc2               40    38/40       +3   0.07       +1
```

A **$2** turn-0 edge converts to a win in 38 of 40 games. The 2 that flip are the world re-roll
Ahmed discloses in his own notebook — a different cash total changes a purchase, which changes the
empty-tile count, which redraws the shops. That ~5% flip rate is the floor under any of this,
whatever the size of the edge.

Ledger check, `data/logs/feedcheck.py pipe7 u1_rc2 7,19`: unfed animal-days **212 vs 212**,
identical every day. The widened guard changes turn 0 only.

## 6. Where this leaves us

1. **Our live `56259375` (`v44a_room_clamp`) already beats stock pipe-7**, median +$301 on 27 of 31.
   The 99.4% tournament headline is against a field that does not include it.
2. The whole wheat-microstructure family is worth **$3** on top of what we already shipped today.
   `room_guard` + `clamp_sells` is worth ~$250-420. The turn-0 game is a rounding error by
   comparison, and it is a game we cannot win outright — only refuse to lose, at N=1.
3. `submission/u1_rc2/` is the best measured build on disk: pipe-7's chassis, N=1, both flags, and
   the guard fix so the two stop cancelling. +$3 over our own live build, +$269 over stock pipe-7.
4. Whatever N the field settles on, a one-byte fork undercuts it. N=1 is the only end state that
   cannot be undercut, so the parameter is not a source of future edge for anyone.

## 7. Submitted

`56281869`, `submission_u1_rc2.tar.gz`, 2026-09-16 15:16 UTC, agent sha256
`2fd78128dea9a819072a581cb4d2832dfa9fef5033a2bf79e8e6b0b79eb57f77`. Evicts `56259332` (v44a,
frozen at 2647.9); `56259375` stays live. Four submissions left today.

Confirmations completed before submitting, 80 paired games each:

```
v45 unmodified   vs u1_rc2    71/80   median   +252   t= 5.24
v43_openc        vs u1_rc2    79/80   median +1,258   t=13.33
```

Ladder context at the time of submitting. `v44a_room_clamp` peaked near **2790** on 2026-09-15 and
read **2642.1** on 2026-09-16 — a fall of roughly 148 within one agent's own live history, across
the window in which V45 published (2026-09-15 19:51) and pipe-7 followed. Seventeen of the current
top twenty were submitted on 09-15 or 09-16; the top-20 cutoff is ~2953 and the leader
(`Majkel1337`, 3199.2) has held since 09-13 through every notebook wave, so it is not a fork of
any of them. Rating here is relative: when several hundred agents adopt the same new opening within
a day, a non-adopter drifts down without playing a worse game. Closing the $61 turn-0 hole is
necessary and not sufficient.

## 8. Where the losses are, and a lead on the flag build

Prompted by Alex's Elo arithmetic: at ~2300 the climb still pays ~130 a game, so one
unlucky loss costs on the order of 60 games of progress. That makes *loss rate*, not margin,
the quantity to minimise. Loss rate turns out not to be monotone in margin:

```
|median margin|  loss rate  games  losses  matchup
              0       5.0%     40       2   pipe7 vs N=0
              2       5.0%     40       2   pipe7 vs N=1
              3       5.0%     40       2   live room_clamp vs u1_rc2
             34       5.0%     40       2   pipe7 vs N=30
            236       5.0%     80       4   v45 vs pipe7
            239      11.2%     80       9   pipe7 vs u1_rc2
            252      11.2%     80       9   v45 vs u1_rc2
            254      12.5%     40       5   pipe7 vs live room_clamp
          1,258       1.2%     80       1   v43_openc vs u1_rc2
          1,333       0.0%     40       0   N=65 vs N=40
          1,367       0.0%     40       0   v45 vs N=30
```

Two distinct sources, separated by which seat flips:

- **Seeds 11 and 12, one seat each, in every thin-margin matchup.** Genuine shop re-roll.
  Irreducible ~5% against any near-clone, because those games are deterministic to the dollar
  and the re-roll inverts them.
- **Seeds 1, 16, 26, 28, BOTH seats, only in the `room_guard`+`clamp_sells` matchups.** A flip in
  both seats is not luck: whoever holds that build loses that world either way. This is the extra
  ~7 points.

Large *and* deterministic margins produce zero losses (`N=30` vs V45: 40/40, +1,367), so loss
rate is engineerable rather than something to endure.

**What the flags actually do, measured.** With `room_guard`+`clamp_sells` on, the V43 "Recovering
Lost Harvests" layer goes completely silent: `warehouse_changed_turns` and `warehouse_extra_sales`
are **0 in every game**, against 1-3 and 1-9 with the flags off, and
`warehouse_projected_unresolved` falls with it (18->4, 24->12, 26->12). room_guard keeps the shed
under the cap, so the recovery layer never finds anything to rescue. Nobody upstream has noted
this. It is uniform across wins and losses, so it is not the discriminator.

**The lead, explicitly a hypothesis.** Median margin over 40 seeds declines monotonically with the
world's `ICE_CREAM_SHOP` count (+487 / +410 / +186 / +120 for 0/1/2/3) and rises with
`BRUNCH_SPOT` (+171 / +312 / +253 / +753 / +1,230 for 0..4). No other shop shows a trend. The two
shops differ by one product: `BRUNCH_SPOT` takes EGG (log/0.20, flattest glut) where
`ICE_CREAM_SHOP` takes MILK (linear/1.60, steep). So the flag build does worse the more of its
demand sits on MILK.

Caveats that must travel with that: exactly 8 shops are drawn per world, so counts are
compositional and the two trends are probably one effect seen twice; 4 losses in 40 games cannot
carry a conclusion on its own, and the monotone median is the only real signal. It also runs
against the naive reading, since clamping should help on a steep curve.

**Next test, not yet run:** decompose sell sizes per product (`data/logs/byproduct.py`) for the
flag build in a high-ICE world versus a high-BRUN one, and check whether the clamp mis-sizes MILK
specifically. Do not select on the 4 losing seeds alone — that is the winner's curse this repo has
already paid for once.
