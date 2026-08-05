# Fable: what this project believes that is false, and where it lives

Review run 2026-08-05, after the `Script.claim` combined-chain fix landed and after the market
measurements in `market_game_framing_kimi_2026-08-05.md`.
Question asked: not a general code review, but *what does this codebase assume that is wrong, and which
file encodes that belief*.

## Headline: `--slots` defaults to 8 everywhere, and 8 slots cannot express the leader's farm

One slot = one chain = (with one narrow exception) one hand.
Every entry point defaults to 8 and nobody has ever swept it:

- `scripts/beam_chains.py:50`
- `scripts/search_chains.py:43`
- `scripts/local_search.py:48`
- `scripts/arena_gate.py:88`

`data/chain_search_local/best_beam_genome.npz` confirms `slots: 8` is what was actually run.

The arithmetic the genome enforces:

- one `ranch` slot holds at most 4 pens of **one** animal type, so 8 cows + 6 sheep needs **>= 4 ranch
  slots**
- that leaves **4 slots** for crops
- the largest block in the vocabulary is `WIDE_BLOCKS` at 8 tiles, legal only at `water_every=2`
- 4 x 8 = **32 crop tiles, maximum, under any search outcome**

The leader works ~101 crop tiles (41 strawberry + 20 melon + 40 wheat) plus 14 pens.
**32 << 101.** So more than two thirds of the tile gap is foreclosed before a single generation runs.

Fable's recommendation: raise `n_slots` to 12-16 before touching anything else. It needs zero new
representational work -- `BLOCKS`, `RANCH_GROUPS`, `WATER_EVERY_FOR_BLOCK` and `decode()` already take
`n_slots` as a parameter (`chains.py:312-313`, `n_genes(n_slots)`).

**Caveat I am adding, because Fable's framing overstates it.** Our current best genome produces 3 cows
and **6** crop tiles -- far below even the 32-tile ceiling. So the ceiling is real and binding at the
top, but it is *not* the only thing wrong: the search is also failing to fill the slots it already has.
Both need fixing, and raising slots alone would not have closed the gap.

## The combined-chain fix is barely reachable by the genome

`routines.py` can now put a pen group and a crop block on one unit (`Script.claim`).
But `decode()` has **no gene** saying "share this slot's unit with slot j".
The only path is an accidental coincidence at `chains.py:660-663`:

```python
unit=None if cell in RANCH_CELLS and len(group) == 1 else units[slot]
```

A single-cell ranch chain on shed cell `k` resolves via `unit_for_cell` to the same unit a `grow` chain
in slot `k` would get from `working_units()`.
That is available for at most 3 of 8 slots, and only when cell choice happens to equal slot index.
So today's fix is currently an edge case the layout stumbles into, not a mechanism the search can aim at.

## Flat prices are encoded in two more places, and one of them gates land

`DRAIN_UNITS` (`chains.py:59-60`) was already known.
The same flat-price belief is duplicated where it actually controls the search:

- **`chains.py:533-534`, `PRICE_BASE`** -- a static dict feeding `cash_curve()` (`chains.py:464-529`).
  Every revenue term is a *constant daily rate*, so day 3 and day 27 earn identically.
- `cash_curve()` is not cosmetic: `reachable_quadrants()` (`chains.py:372`) walks it to decide **whether
  a genome's land order is affordable at all**, and that is the land gate inside `decode()`.
  A chain arriving late, when wheat is $54 and milk $244 rather than $25/$160, is priced by the gate at
  the day-3 rate for its whole run -- so the gate **systematically rejects the late-land genomes** the
  measured price ramp says are best.
- **`scheduler.py:150-171`, `revenue_rate()`** -- same defect, same flat `base` dict, used to rank
  chains by payback.

So the codebase fights the measured ramp through two independent channels beyond the one already found.

## `seeded_genome()` never uses the multi-pen vocabulary built to fix the deadlock

`_cut_pen_groups()` (`chains.py:188-217`) exists, per its own docstring, to break the herd/crop deadlock
by letting one slot hold up to 4 pens.
`seeded_genome()` (`chains.py:750-753`) only ever matches a **single-shed-cell** group:

```python
g[slot, 2] = next(i for i, gr in enumerate(RANCH_GROUPS)
                  if gr == (OWNED_CELLS[slot % len(OWNED_CELLS)],))
```

Its `plan` list contains exactly one `("ranch", "COW", 0)`.
Every search starts from **one cow**, using a seed that structurally cannot express the animal economy
it is trying to find.

## "Select on win rate, not money" has silently degenerated into "select on money"

`local_search.py:253` does `np.lexsort((money, wins))[::-1]` -- wins primary, money tiebreak, exactly as
CLAUDE.md requires.
But the pool is 4 weak recorded tapes we already beat 16/16.
Once win rate saturates at the pool's ceiling, **every remaining comparison is decided by the money
tiebreak** -- the criterion CLAUDE.md overruled -- and nothing detects or reports that it has happened.
The guardrail is switched off by the weakness of the pool.

This is the direct explanation for the arena result: the search saturated win rate on tapes and then
optimised money, so it never learned to beat stronger live play.
Measured the same day: pool win rate **0.450** in the real environment, losing 20/20 to `contrarian` and
18/20 to `rancher`, for the same genome the search scored 16/16.

## `working_units()` pre-judges SE as dead

`chains.py:236-258` permanently skips units spawning on the SE shed cell because the leader never buys
SE. True of the observed replay, but it hard-codes *his choice* as *unreachability*, so the hypothesis
"is SE worth it at 14+ slots, funded late, for one extra 4-pen group?" is never offered to the search.
At 8 slots that also discards 25% of unit indices.

## Objective: right in kind, wrong in calibration

Win rate, exact simulation, best-response is the right frame.
But the pool banks ~$18.8k against our ~$40.5k and every member is `heuristic.make_agent` with different
dials, so beating it 16/16 is close to a foregone conclusion.
And because the four leader replays are byte-identical mirror matches, **no tape in this repo represents
beating a genuinely different strong opponent.**
Fable's suggestion: add an adversarial pool member, even synthetically -- e.g. our own best genome played
against itself -- to reintroduce real market contention.

## Priority order Fable gives

1. Raise `n_slots` from 8 to 12-16 and re-run. Zero new representation needed.
2. Fix `seeded_genome()` to seed multi-pen groups per animal type, or the first sweeps waste themselves
   rediscovering the herd from one cow.
3. Replace the flat `PRICE_BASE` / `revenue_rate` day-blind revenue with a day-scaled ramp, or the land
   gate keeps rejecting the late-land genomes more slots would let the search find.
4. Add a gene (or a joint move) that deliberately shares a unit between a pen group and a crop block,
   so today's `Script.claim` fix is reachable by design rather than by coincidence.
