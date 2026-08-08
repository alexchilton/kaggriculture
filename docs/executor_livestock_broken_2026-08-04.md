# The leaders' own plan, run through our executor, banks $0

2026-08-04. Measured with the leaders' allocation from `docs/episode_teardown_2026-08-03.md`
encoded via `P.leaders_genome()` and played against all three hand-written opponents in
`library.opposition()`, seed 0.

## Result

```
vs opp 0: mine $0  theirs $31,777  loss
vs opp 1: mine $0  theirs $4,762   loss
vs opp 2: mine $0  theirs $3,633   loss

win rate 0.00, mean bank $0 against their $13,391
```

Money and live animals over the season, mean over the three games:

```
day  0: $24   animals alive 1.0
day  5: $0    animals alive 0.0
day 10: $0    animals alive 0.0
day 15: $57   animals alive 3.0
day 20: $0    animals alive 1.7
day 25: $0    animals alive 0.0
```

Order volumes, per game:

```
animals ordered      29     (the plan specifies 14: COW 8, SHEEP 6)
wheat bought as feed  15     (the leaders bought 967)
```

Roughly 88% of *slot*-turns were no-ops -- but that denominator is wrong and is corrected here.
There are 24 unit slots against a crew of about 5, so most slots hold no unit at all. Measured against
slots that actually held a unit, `jax_heuristic` acts on **57.6%**, i.e. a **42.4%** idle rate against
the leader's 7.2%. Still a 6x gap, not 12x. This is the fourth time this project has taken a share over
`MAX_UNITS` rather than the live crew and read the result as a fact.

## What this establishes

The failure is in **our executor**, not in the leaders' plan.
The same allocation that banks ~$100k-$144k on the real leaderboard banks $0 here.

Three distinct defects are visible in the numbers:

1. **The herd target is not respected.** 29 animals ordered against a specified 14. The purchase
   gate counts standing empty pens (`housing = max(n_pens_free - shed_stock, 0)`) but nothing caps
   cumulative purchases against `herd`, so animals are re-bought as earlier ones starve.
2. **Feed is not bought.** 15 wheat per game against the leaders' 967 -- about 1.5%. With
   `feed_wheat=2` and 14 animals, one day's feed alone is 28 units.
3. **The stake is consumed and never recovered.** Bank sits at $0 from day 5 onward, so the $3,000
   went into livestock that then starved, leaving nothing for the crop economy. `PLANT` and
   `HARVEST` are near-absent.

The animals dying and being re-bought (1.0 -> 0.0 -> 3.0 -> 1.7 -> 0.0) is defects 1 and 2
compounding: no feed, so they escape; no cap, so the executor buys more.

## Consequences for other conclusions

**The seeded CEM's bad start is explained.** `data/logs/cem_seeded.log` gen 0 reported
`pop mean 0.03` when seeded at `P.probs_around(P.leaders_genome())`.
That was our executor failing on every livestock sample, not evidence against the leaders' plan.
By gen 15 the search had reached `pop mean 0.95` and `delta +45182` -- well above the uniform run's
final `+32142` -- which it can only have done by moving away from the seeded livestock region.

**Task "find out why the policy never buys animals" is the wrong question.**
Livestock loses money in our implementation, so no optimiser -- CEM or PPO -- should be expected to
select it. Not buying animals is currently the *correct* behaviour.
The prerequisite is fixing the executor's feed and herd-cap logic; only then does the RL question
become meaningful.

This also rules out using the executor as a demonstration source for imitation
(see `docs/entropy_diffusion_2026-08-04.md`).

## Caveat on the op census

The diagnostic built its op-name lookup from every uppercase int attribute in `kagg.sim.ops`, so
tile-state constants (`PASTURE`, `COOP`, `EMPTY`, `LOCKED`) collided with op codes.
The per-op percentages in the raw log are therefore mislabelled and should not be quoted.
The bank figures, the live-animal trajectory, and the order volumes come from game state and
`Decision` fields directly, and are sound.

Script: `scratchpad/diag_leaders.py`, log: `data/logs/diag_leaders.log`.
