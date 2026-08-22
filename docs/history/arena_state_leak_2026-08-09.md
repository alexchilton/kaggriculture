# Task #54 — `run_arena` drove one agent object through every match

Date: 2026-08-09.
Base commit: `b85ac19` (`shaping-potential`).
Environment: `kaggle-environments` 1.32.6, macOS, Python 3.12.

## The one-line finding

`run_arena` took an agent *value* and passed that same object into every job — every seed, both
seatings — while `kagg.search.schedule_agent.make_agent` builds its `state` dict once in the closure.
A finished season therefore walked into the next match and killed the agent outright.

`run_arena` now takes an `AgentFactory` and refuses a bare callable.

## What was and was not affected — read this before re-reading any number

The hypothesis handed to this task named `scripts/gate_pool.py` (the submission gate) as affected.
**It is not, and neither is `scripts/arena_gate.py`.** Both were checked in source and by measurement.

| Path | Verdict | Why |
|---|---|---|
| `docs/fable_market_shape_2026-08-09.md` §4 | **CONTAMINATED** | §4 states its own harness: "`kagg.arena.run_arena`, workers=1 (closures from `make_agent` …)". This is the only measurement found that put a `make_agent` closure through `run_arena`. |
| `scripts/gate_pool.py` | clean | Calls `kagg.arena.pool.evaluate`, not `run_arena`. `pool._play` builds the candidate *inside the job*. On top of that the candidate is the path `submission/main.py`, and `kaggle_environments.agent.build_agent` re-`exec`s a path into a fresh namespace for each `Agent`, one `Agent` per `env.run`. |
| `submission/main.py` | clean | Already rebuilds its agent at `day == 0 and hour == 0`, with a docstring saying exactly why: "a process that plays more than one episode does not carry a season of pins and pen reservations into the next one." Fix (b) was shipped in the artifact and never applied to the harness. |
| `scripts/arena_gate.py` | clean, but by luck | It did pass live callables to `run_arena`. Its own agent is a pure tape replay keyed on `obs["step"]`, and its opponents are the module-level `kagg.agents.*.agent` functions, all stateless. Nothing to carry. Updated to the factory API anyway. |
| `scripts/bench_agents.py`, `bench_arena.py`, `build_script_submission.py` | clean | Pass names and paths only. |
| `scripts/confirm_late_sell_bias.py` | clean by construction | Walks `run_match` itself and rebuilds the agent per match. Its docstring already documented the trap in both directions. |

### The pool opponents are stateless — the bias has a known direction

`heuristic.agent`, `rancher.agent` and `contrarian.agent` are pure functions of the observation.
Measured, three consecutive matches through one object, seed 40 vs `pass`:

```
heuristic    [33188.0, 33188.0, 33188.0]
rancher      [37121.0, 37121.0, 37121.0]
contrarian   [33163.0, 33163.0, 33163.0]
```

`heuristic.make_agent` only binds a parameter dict; there is no per-game state to carry.
So **only our side was ever contaminated, and only downward** — a carried season makes our agent
bank less, never more. Every contaminated number understates us.

## The measurement

### Raw damage: one `make_agent(thin, me=0)` object, three matches, seed 40 vs `pass`

```
game 1   $114,028    13.7s
game 2         $0     1.0s
game 3         $0     0.9s
```

Not a degradation. The second game dies in the first seconds — 1.0s against 13.7s — and banks $0,
which is below the $3,000 opening stake, so the agent is being invalidated rather than playing badly.

### Through `run_arena`, seat-agnostic wrapper (the shape `submission/main.py` had before its day-0 rebuild)

```
seeds=[40]        2 games    mean $115,237
seeds=[40, 40]    4 games    mean  $57,618
```

Exactly half. Matches three and four bank $0. This is the assertion in
`tests/test_arena_state_leak.py::test_run_arena_does_not_carry_a_season_into_the_next_match`;
comparing `[S]` against `[S, S]` rather than against a single `run_match` makes the seat effect
cancel, so only carried state can move the number.

### Fable's §4 configuration, re-run both ways

Seeds 20-27, both seatings, `heuristic`/`rancher`/`contrarian`, `LATE_SELL_BIAS` at its default
`False`, 48 games per arm. `shared` reproduces the pre-fix `run_arena` — one `make_agent` object per
opponent, driven through all 16 of its matches. `fresh` builds one agent per match with `me` set to
the seat it actually occupies, which is what `scripts/confirm_late_sell_bias.py` does.

Logs: `data/logs/task54_damage_shared.log`, `data/logs/task54_damage_fresh.log`.

```
arm       opponent          mean $   win rate
shared    heuristic         4,534       6.2%
shared    rancher           6,001       6.2%
shared    contrarian        6,788       6.2%
shared    POOL              5,774       6.2%

fresh     heuristic        97,101     100.0%
fresh     rancher         102,850     100.0%
fresh     contrarian      108,707     100.0%
fresh     POOL            102,886     100.0%
```

**$5,774 against $102,886, and 6.2% against 100%.** 17.8x on money, and a pool the harness reported
as a near-shutout against us is in fact a clean sweep by us. 6.2% is 1 win in 16 — the first,
unswapped, still-clean match of each opponent, and nothing else.

For comparison, `docs/fable_market_shape_2026-08-09.md` §4 published $16,146 / 14.6% for this
configuration, and $24,535 / 27.1% with `LATE_SELL_BIAS` on. Both sit between the two arms above.

**This does not reproduce Fable's exact figures** ($16,146 / 14.6%), and I did not try to — §4 does
not record the precise call, so `shared` is the pre-fix `run_arena` semantics rather than a
byte-reconstruction of that run. It reproduces the failure mode, at the same order of magnitude and
in the same direction.

**The `shared` arm conflates two defects and cannot separate them.** A `make_agent(schedule, me=0)`
object placed in seat 1 by `run_arena`'s swap also believes it is still seat 0 (see below), so half
of `shared`'s games are wrong for that reason alone. The 6.2% win rate is 1 win in 16 — exactly the
first, unswapped, still-clean match — which is what both defects together predict.

### The shipped artifact, measured properly

`scripts/gate_pool.py --seeds 6 --workers 6`, `submission/main.py` against the 9-member
`COMPETITIVE` pool, seeds 700-705, both seatings, weeds ON, 108 games:

```
win 94.4% (draw 0.0%) mean $108,180

opponent          win       ours
mirror           50%     59,271
wheat_only      100%    137,876
melon_heavy     100%    111,038
strawberry      100%     86,213
cow_heavy       100%    102,514
carrot_25       100%    118,715
small_farm      100%    124,491
straw_small     100%    123,299
contrarian      100%    110,199
```

This is not a new number and it is not "the fix helped" — `gate_pool.py` was never on the broken
path. It is here because §4.1 of `fable_market_shape_2026-08-09.md` spent a section on the
"94.4% vs 14.6% question" and resolved it as *"not the same measurement"* — different pool
composition, different era, `mirror` and `starter` inflating the high figure. That explanation is
partly right and misses the larger term: the 14.6% came off a harness that killed our agent in 15 of
every 16 games. The 94.4% is the honest one, and the fresh re-run above reaches 100% against the
exact three opponents §4 used, on §4's own seeds. There is no pool-composition gap left to explain.

**So the answer to "what does the shipped agent actually score" is 94.4% / $108,180 against the
9-member pool on seeds 700-705, and it always was.** The submission was not gated on contaminated
numbers. What was contaminated is the market-shape investigation that ran beside it.

## The fix

`kagg/arena/arena.py`:

- `AgentFactory(build, *args, **kwargs)` — a picklable "build me a fresh agent" instruction, invoked
  once per match, **inside the worker**.
- `run_match` resolves a factory but still accepts a bare callable: one match cannot leak into a next
  one that does not exist, and `confirm_late_sell_bias.py` depends on that.
- `run_arena` resolves factories and **raises `TypeError` on a bare callable**. Chosen over silently
  reusing it: there is no way to rebuild an agent from an instance of one, and from outside a
  stateless callable is indistinguishable from a stateful one. The module docstring already claimed
  "Callables are deliberately not supported"; now that is enforced rather than asserted.

This also closes the `workers=1` constraint. `scripts/arena_gate.py` pinned `--workers 1` because
`ProcessPoolExecutor` on macOS spawns rather than forks, so its `_GENOME` global arrived unset and
`make_agent` closures raised "Can't pickle local object". A factory ships the *recipe* — a
module-level function plus picklable arguments — and builds on the far side.
`test_a_factory_survives_the_worker_pool` pins it.

## Tests

`tests/test_arena_state_leak.py` (added to `SLOW_MODULES` in `tests/conftest.py`, so `-m slow`):

| Test | What it pins |
|---|---|
| `test_run_arena_gives_each_match_its_own_agent` | Two matches, two agent objects, one game each. |
| `test_a_factory_survives_the_worker_pool` | `workers=2` with an in-process build. |
| `test_run_arena_refuses_a_live_agent` | The trap is loud, not merely discouraged. |
| `test_run_arena_does_not_carry_a_season_into_the_next_match` | The money, on the real schedule agent. |
| `test_a_path_spec_was_never_contaminated` | The shipped artifact's freshness, so a regression in either mechanism shows. |

### The revert check

Per `CLAUDE.md` — three of five past fixes were, at first, covered by nothing. With `_resolve`
returning its argument unchanged and `_check_spec`'s guard forced to `False`, **all three of the
original tests go red**:

```
FAILED test_run_arena_gives_each_match_its_own_agent           - 0 agents built for 2 matches
FAILED test_run_arena_refuses_a_live_agent                     - DID NOT RAISE <class 'TypeError'>
FAILED test_run_arena_does_not_carry_a_season_into_the_next_match
        AssertionError: the agent banked $3,000; it did not play a season, so the comparison
        below would be vacuous
```

**The revert check earned its keep immediately.** The money test as first written would have PASSED
with the fix backed out: an unresolved `AgentFactory` is called as `factory(observation,
configuration)`, dies, and both arms report the $3,000 opening stake — equal, and meaningless. The
liveness guard (`assert once.mean_money[0] > 3000.0`) exists only because the revert was actually
performed. A green suite after a fix says the fix broke nothing, not that anything checks it.

## A second defect, not fixed here

`run_arena`'s seat swap is wrong for any agent that has its seat baked in.
`make_agent(schedule, me=0)` placed in seat 1 by the swap still believes it is seat 0.
`confirm_late_sell_bias.py` handles it (`_ours(..., 1 if swapped else 0)`); `run_arena` cannot,
because it has no way to tell the agent which seat it is in. `submission/main.py` is immune because
it reads `obs["player"]`. Anything else driven through `run_arena` with a baked seat is wrong in half
its games *independently of this bug*. Not in scope for #54; flagged rather than chased.

## What to re-read

- `docs/fable_market_shape_2026-08-09.md` §4, §4.1 and §5 rest on the contaminated harness. The
  direction of `LATE_SELL_BIAS` may well survive — `scripts/confirm_late_sell_bias.py` re-measures
  it on the honest path and on a disjoint seed block — but the magnitudes ($16,146 → $24,535,
  14.6% → 27.1%) are measured on games our agent mostly did not play.
- §4.1's resolution of the "94.4% vs 14.6% question" should be reopened.

## Suite status

Full suite on this worktree, `pytest -m ''`: 32 failed, 1077 passed, 202 skipped, 14 xfailed,
26 errors. All 26 errors are `FileNotFoundError` on gitignored `data/` fixtures absent from a fresh
worktree. The 32 failures are pre-existing on `b85ac19` — 21 in `tests/test_router.py`, whose fix is
uncommitted work in the main tree — and none of the failing modules import `kagg.arena`.
Arena suites specifically: `tests/test_arena.py` + `tests/test_arena_state_leak.py`, 10 passed.

`scripts/arena_gate.py --seeds 2 --slots 6 --workers 4` was run as a live check that the factory
lifts the `workers=1` constraint in the real script: it banks $14,708 against `starter` and $7,888
against `heuristic` rather than the flat $3,000 / 0.000 the spawn failure used to produce.
Log: `data/logs/task54_arena_gate_workers.log`.
