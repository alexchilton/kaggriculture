# Short handoff — 2026-08-02, end of session

Read `CLAUDE.md`, then `docs/HANDOFF_2026-08-02.md` (full detail, current through commit `dae2a23`).
This file is just the state and the next three moves.

## Running right now

`mix5d-20260802-123217`, systemd service `kagg-train` on the Windows box, log `data/logs/run.log`.

```bash
--curriculum-mix 25:0.6,20:0.1,15:0.1,10:0.1,0:0.1 --curriculum-resample 25 --curriculum-symmetric
--kl-prior <mix5-20260802-120823/latest.pkl>  --init <same>   # update-50 checkpoint
```

**Always launch through `./scripts/deploy_train.sh train`.** A hand-started tmux run gets reaped by
WSL2 when the SSH connection closes (`deploy_train.sh:92`) and writes to a log the tooling does not
read.

## READ FIRST: mix5d is REGRESSING, and four of its five rungs are dead

Measured at update 211 (2026-08-02). This is the answer to move 1 below, and it is not the
hoped-for one.

```
upd  wr_farm  wr_pool   ev    ent   clip   money_med
 40   0.652    0.996   0.124  6.6  0.116     32,651
 80   0.603    0.863   0.092  6.0  0.112     25,902
120   0.587    0.784   0.222  6.4  0.142     38,970
160   0.589    0.757   0.118  5.3  0.153     32,188
211   0.589    0.753   0.206  5.5  0.115     32,282
```

**`vs farm` peaked at 0.652 around update 40 and has sat at ~0.589 ever since -- below the
0.659 baseline this run was launched to beat.** `vs pool` fell 0.996 -> 0.753. It is not
climbing back.

Per seed day, which is exactly what the per-day logging was added to expose:

```
day25: 11,697 games   wr 0.612
day20:     988 games  wr 0.523
day15:     695 games  wr 0.491
day10:     496 games  wr 0.484
day 0:     423 games  wr 0.528
```

**Day 25 is carrying four dead days.** Every other rung is at chance. And the mix is not
delivering what it was configured for: `0:0.1` asks for 10% of *slots*, but day-0 episodes are
~6x longer, so day 0 supplies 423 of 14,299 finished episodes -- about **3%**. Day 25 gets 28x
more games than day 0.

Two consequences for the plan:

- **The aggregate `wr` is still a day-25 number wearing a mix's name**, even with the mix. Quote
  the per-day rates or nothing.
- **`best.pkl` for this run is near-certainly an early update** (the peak was ~40), which is the
  trap already recorded below. Prefer `latest.pkl` and check.

Untested hypotheses, in the order worth trying: the day-share is wrong in *episodes* rather than
slots and needs weighting by episode length; and the opponent pool still contains nobody who uses
the animal economy, which no curriculum change addresses. Do not add a third delta before
measuring one of these.

**The op-axis decode does not address this.** It refines *which item* a unit picks given it has
already chosen PICKUP; it cannot help a policy that has not learned to plant, water and harvest
from an empty farm. It was also measured as no detectable change offline. See below.

## The two changes that matter from today

**1. Symmetric starts (`--curriculum-symmetric`).** Both seats get seat 0's *entire* position -- cash,
crops, animals, units, land -- so the only difference between players is what they do. Before this the
trainee got the seat `rank_seats` ranked, which is ranked by **final** bank and is the richer side at
the seeded day only ~37% of the time. Effect: `vs farm` 0.598 -> **0.659**, `vs idle` 0.773 -> 0.979.

**2. Per-seed-day win rate logging.** New fields `wr_day25`, `games_day25`, … one pair per day in the
mix. Needed because day-25 slots supply ~83% of terminal episodes, so the aggregate `wr` is a day-25
number wearing a mix's name.

`kagg-log` will **not** show the per-day rates -- the print line broke and was reverted. Read the JSON:

```bash
ssh -i ~/.ssh/copilot_remote_ed25519 -p 2222 alex@192.168.1.128 'python3 -c "
import json
r=[json.loads(l) for l in open(\"/home/alex/kagg/data/jax_rl_runs/mix5d-20260802-123217/log.jsonl\")][-1]
for d in (25,20,15,10,0): print(d, r.get(f\"games_day{d}\"), r.get(f\"wr_day{d}\"))
"'
```

## READ THIS FIRST: the decode was destroying the evaluation, and one conclusion here was wrong

`play_checkpoint.py` defaulted to **per-head argmax**. On one checkpoint, same 32 games:

| | greedy (old default) | **sampled** |
|---|---|---|
| WATER | 0% | **5.62%** |
| PLANT | 0% | **2.50%** |
| HARVEST | 0% | 0.76% |
| raw FEED | **0** | **18** |
| bank | $2,998, median=mean=min=max, **zero variance** | $1,305 (min 54, max 3,534) |
| W/D/L | 0/0/16 | 0/0/16 |

**The marginals contain the behaviour; argmax over independent per-head marginals destroys it.** Same
mechanism `CLAUDE.md` already records for market orders -- nine independent "probably not" decisions
compose into "never". `play_checkpoint.py`'s own `_greedy` docstring warned about this and was not read.

**Sampling is now the default** (`47c86b2`); `--greedy` reproduces the comparison.

**But the decode is not the whole story, and this is the part to keep.** Sampled decode still loses
0/0/16 and the bank *falls* $3,000 -> $1,494. So the policy does produce actions from turn 0 -- just
not competent ones. It plants and waters a little, then bleeds money. A conclusion written earlier in
this session, that it "does nothing but walk", was an artifact of the greedy decode and is **wrong**.

## The autoregressive decode: DONE

**Status: implemented, tested, and smoke-run.** `crop`, `item` and `qty` now carry a
`[.., MAX_UNITS, N_OPS, K]` axis and are read through `jax_act.condition_on_op`, mirroring what
`condition_on_trade` already did for `sell`/`buy_product`. The op is drawn first and the argument
heads are scored on the slice it selects.

**Checkpoints did NOT have to be thrown away, and the earlier claim here that training "restarts
from scratch" was wrong.** Only three kernels change shape; the trunk, `op`, the value head and
every market head are untouched. `jax_policy.migrate_params` tiles the old `[K]` kernel across the
new op axis, which sets `p(arg | op)` to the old marginal `p(arg)` for **every** op -- that is
exactly the mean-field policy the checkpoint was trained as, so day-one behaviour is identical and
the op axis learns the deviation from a warm start.

That mattered more than convenience: `--kl-prior` loads a *second* network of the same
architecture, so without a migration the op-axis change would have silently cost us the KL anchor,
which is the one change that has ever reversed this project's decline. Verified end to end -- a
deliberately shrunk pre-op-axis checkpoint passed to both `--kl-prior` and `--init` trains with a
non-zero `klP`.

### What was verified, and what that does and does not prove

- `tests/test_jax_act.py` -- 7 tests. The named gate, **`ratio == 1.0` before the params move**,
  passes. Also: the op axis exists; `condition_on_op` really selects a different slice per op; and
  scoring under the *wrong* op slice changes the answer, with `actions` held fixed so the active
  set and the op's own log-prob cannot account for the difference.
- `tests/test_param_migration.py` -- 5 tests, including that every op slice of a migrated
  checkpoint carries the identical distribution, and that a migrated checkpoint still passes the
  ratio gate.
- Two short PPO runs on CPU completed: `data/logs/opaxis_smoke.log` (clean, `clip 0.000` at
  update 0) and `data/logs/opaxis_migrate.log` (migrated prior + init, `klP 0.002`).

**This does not prove the decode helps.** It proves the factorisation is coherent and nothing is
silently lying. The runs above are `d_model=32`, one layer, sixteen turns, and exist only to prove
the pipeline executes.

### It was then measured offline, and the answer is: no detectable difference

Two BC runs per architecture on the same 17,975-row cache, seeds 0 and 1, six epochs. Held-out NLL
on the `item` and `qty` heads over PICKUP and PLACE slots (270 slots), lower is better:

| | seed 0 | seed 1 |
|---|---|---|
| `item` effect (op-axis minus control) | +0.015 worse | **-0.028 better** |
| `qty` effect | +0.079 worse | **-0.041 better** |

**The effect changes sign between seeds, and within-architecture seed spread (0.037-0.079) is as
large as the effect.** So the unit-head half of this change is not measurably better or worse. An
earlier version of this section reported the seed-0 numbers alone as "net worse" and recommended
reverting; that was noise read as a finding, off a single 899-row holdout. Withdrawn.

**Where the change is inert by construction, which is not a seed result.** The op axis only buys
something where two or more ops read the same head:

- `crop` is read by PLANT alone, and `active_unit_heads` already restricted it to PLANT slots, so
  the old single head was *already* `p(crop | PLANT)`. Confirmed after retraining: the PLANT slice
  moves, every other slice sits at exactly uniform 0.200. An earlier claim here and in the source
  -- that PLANT drew its crop from a distribution averaged over seventeen irrelevant ops -- was
  simply wrong.
- `item`/`qty` are read by both PICKUP and PLACE, whose teacher distributions differ at total
  variation 0.900. That averaging is real, but PICKUP outnumbers PLACE 7.8:1 (4,332 vs 555 slots),
  so the split slice has the least data exactly where pooling hurt most. Net: a wash, as measured.

**The market heads are where this technique actually paid**, and that shipped earlier as
`condition_on_trade`. `CLAUDE.md` records the numbers: argmax over nine per-product marginals emits
zero orders, independent sampling banks $1, and the marginals themselves discriminate 12:1. Nothing
in this section bears on that; do not read a null result on the unit heads as a verdict on the
market ones.

**So the durable value here is the scaffolding, not the unit-head conditioning:** the
`ratio == 1.0` gate catches a silently corrupted PPO update, and `migrate_params` means an
architecture change no longer costs every checkpoint and the KL anchor.

### If you anchor a KL prior to a MIGRATED checkpoint, read this first

A tiled checkpoint has all 18 op slices identical, and `kl_to_prior` scores the *conditioned* heads
-- so `KL(policy || prior)` is minimised exactly at op-independence and pulls against the
specialisation the axis exists to learn. Measured: KL 0.000 / 0.026 / 0.099 / 0.315 as
specialisation rises. `--kl-coef` defaults to 1.0 and `--kl-anneal` to 0, so it does not decay, and
the running `mix5d` passes neither flag. Retrain BC with the op-conditioned loss rather than anchor
to a tiled prior. Not shown: that this would actually prevent learning. That needs a run.

### The one design choice worth knowing about

`sample` and `evaluate` now share a single scoring function, `jax_act._score`. That is deliberate:
two copies of that loop is precisely how the ratio drifts, and the failure is silent -- no error,
no NaN, just a gradient pointing somewhere arbitrary. The test pins the property; the shared code
path is why it stays true.

### Not done, and pre-existing

`scripts/eval_policy.py:41` and `scripts/train_bc.py`'s loss both argmax / cross-entropy the **raw**
heads. Both have been broken since the *trade* axis landed -- they cannot broadcast a
`[N, 9, K]` mask against a `[N, 9, 3, K]` head -- and this change does not make them worse or
better. `kagg/agents/neural.py` had the identical bug and **was** fixed here, because it is the
submission path and shipping a decode change that leaves it unrunnable is not defensible.

**Why it is the same technique as Ender's, not a new idea.** Billy Bradley's 8th-place `ender` used
two things: KL-to-prior instead of an entropy bonus (**adopted today, and it is the fix that reversed
the decline for the first time in this project's history**) and autoregressive micro-steps. This is the
second half of the same solution. `CLAUDE.md` records that it was struck off for answering the wrong
question -- it was assessed against the spawn deadlock, when its author built it for **action-space
explosion**, which this project independently has and had measured three times.

**But the two halves are not equally valuable, and the measurement says so.** `condition_on_trade`
-- the market half, already shipped -- fixes a failure with numbers attached: argmax over nine
per-product marginals emits zero orders, independent sampling banks $1, and the marginals
themselves discriminate 12:1. `condition_on_op` -- the unit half, built 2026-08-02 -- was measured
as **no detectable change**, because only PICKUP and PLACE ever share a head and PICKUP outnumbers
PLACE 7.8:1. Read the section above before spending anything on the unit half.

**Step 5 of the original spec was never done and is the one still worth considering:**
`buy_seed`/`buy_animal`/`hire`/`buy_land` on `trade`. Those are the *spend* heads, and the failure
mode `hand_prior_heads` documents -- `buy_seed` firing on 29.1% of turns, bank at $0 by day five --
is a joint-decode failure of exactly the kind conditioning fixes. Unlike the unit heads, four
distinct heads share the one `trade` latent there, so the averaging is real.

## Superseded: the turn-0 result as originally written

`scripts/play_checkpoint.py` on `mix5-20260802-120823/latest.pkl` (update 50), 16 games per seating:

```
seat 0 vs scripted farmer:  W/D/L  0 / 0 / 16
seat 1 vs scripted farmer:  W/D/L  0 / 0 / 16
policy $  2,998  (started 3,000)      farmer $ 30,292
bank by day  d0:3,000 d5:3,000 d10:3,000 d15:3,000 d20:3,000 d25:2,998 d29:2,998
ops  N:53.73%  S:37.39%  E:4.44%  W:4.44%
     WATER:0%  PLANT:0%  HARVEST:0%  FEED:0%  CARE:0%   raw FEED count 0
```

**100% movement, zero productive actions over a whole season, 32/32 losses.** It walks north and
south and never touches a crop or an animal.

**So `vs farm 0.659` is entirely an artifact of the seeded start.** The policy is not a competent
farmer that is merely untested at turn 0 -- from a real start it produces nothing. A conclusion
recorded earlier in this session, that `vs idle 0.979` showed the policy "maintains and grows a farm",
is **wrong**: it maintains a *pre-built day-25 board* and does nothing otherwise.

This vindicates the standing rule and it should not need learning a fourth time: **prefer a replay to
an aggregate.** Every seeded win rate today was consistent with a policy that banks $2,998.

**What it implies for the plan.** The day-0 share is not a coverage nicety worth 2% of episodes -- the
opening is entirely unlearned and is the whole problem. And the flat animal gap was not only a
symmetry artifact; there is no animal behaviour to measure. Before any more curriculum tuning, decide
whether a policy trained on seeded maintenance can ever transfer to turn 0, or whether the opening
needs its own training signal.

## A pre-existing test failure, found in passing and NOT caused by the decode work

`tests/test_curriculum.py::test_the_behind_dial_actually_puts_the_trainee_in_the_poorer_seat`
fails at `HEAD`. Verified pre-existing: it fails identically with the op-axis changes stashed.

```
assert b[:, 0].mean() < a[:, 0].mean()
E  assert 32615.9 < 25498.2      # the "behind" seat is RICHER by $7k
```

The dial is **inverted or dead**: asking for the poorer seat hands the trainee the richer one. Read
that test's own docstring before dismissing it -- seeding the trainee into the richer seat makes the
position winnable on the seed alone, which is *indistinguishable from having learned anything* in a
win rate. This file already records four numbers that turned out to measure the setup rather than
the policy; this is a fifth waiting to happen.

Note the handoff previously recorded "382 pass, 2 xfailed", so this broke somewhere in the
symmetric-starts / seat-pool work (`9a65b92`, `d08cdcb`, `dae2a23`). It is not diagnosed.

## Both critic-side gates are dead — do not use them

Under symmetric starts these two are structurally uninformative, not broken:

- **`ev_signal`** fell 0.618 -> 0.152. With identical seats the true value is 0.5 on every board at
  t=0, so there is almost nothing to explain *from the state*. **The >0.5 kill criterion does not
  apply to a symmetric run.**
- **The animal gap** went +0.0523 -> -0.0093. Both sides hold the same animals, so animal count
  genuinely stops predicting the winner and the critic correctly learns it is not an edge.

**`vs farm` is the only clean signal. Baseline to beat: 0.659.**

## The session's repeated error, stated so it does not recur

Four numbers were read as findings when the setup had changed what they measured: slot share vs
terminal-episode share; waste count vs waste rate; `ev_signal` under symmetry; the animal gap under
symmetry. **After any configuration change, check whether a metric still measures the thing it was
calibrated on before treating a move in it as a result.**

Also: **`best.pkl` is selected on cumulative win rate and therefore favours early updates** -- it was
update 38 on one run whose settled rate came much later. For anchoring a follow-on run prefer
`latest.pkl` unless you have checked which update `best` came from.

## Next three moves, in order

0. **Re-run `scripts/play_checkpoint.py` on every checkpoint you evaluate.** It is the only thing that
   caught the above, and it takes five minutes. A seeded win rate cannot see a policy that banks $2,998.
1. ~~**Read the per-day rates.**~~ **DONE at update 211, and the answer is "day 25 is carrying four
   dead days" -- see the top of this file.** `vs farm` is also *below* the 0.659 baseline and has
   been flat at ~0.589 for 170 updates. Whatever comes next, it is not "let mix5d keep running".
2. **The opponent pool is the untouched suspect, and is now the leading one.** No opponent in it
   uses the animal economy -- the scripted farmer has no FEED, no CARE and `buy_animal=zeros`, and
   loses 16 inherited animals in four game-days, 32/32. No curriculum change addresses that, and
   the curriculum has now been changed three times without moving `vs farm`.
2b. **The mix is specified in slots but spends in episodes.** `0:0.1` delivered ~3% of finished
   episodes, not 10%, because day-0 episodes are ~6x longer. If the day-0 share is the lever, it
   has never actually been set to what it says. This is a one-line measurement before it is a fix.
3. **`--curriculum-resample 8`** plus the now-wider seat pool, as one board-diversity delta. A
   restarting slot re-enters `seed_states[i]` by index, so at resample 25 each slot replays its own
   board ~7 times. Cost ~1-2% throughput. The clean fix is permuting slot->board on *restart*, which
   is a gather inside the jitted scan and was not attempted.

## Smaller open items

- Per-day line in the human-readable log (~10 min; the print block uses implicit string concat and a
  conditional expression broke it).
- A calibration gate, if a critic-side signal is wanted back: bin early boards by V, measure their
  realised win rate. Not built.
- Dead artifacts from a mis-launch: `data/logs/train_mix.log` and run dir `mix-20260802-101135`.
- `scripts/stage_curriculum.py` is the gated staged-ladder fallback if the mix does not carry. Unused.

## Repo

**https://github.com/alexchilton/kaggriculture** — private, default branch `main`, work on
`animal-economy-and-rl-measurement-fixes`. `data/*` is gitignored so no replays, checkpoints or logs
are pushed. Suite: 382 pass, 2 xfailed.
