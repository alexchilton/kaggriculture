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

## The one thing left, and it is an architecture change

Fable's first recommendation: **autoregressive / jointly-renormalised decode instead of independent
per-head sampling.** NOT DONE. It requires new head shapes, so every existing checkpoint becomes
incompatible and training restarts from scratch -- flagged rather than done, per the standing rule
about never changing architecture without explicit approval. Approval was given; the work was not
attempted because it was late in a long session and this is the one change where a subtle error
silently corrupts the PPO ratio.

**Why it is the same technique as Ender's, not a new idea.** Billy Bradley's 8th-place `ender` used
two things: KL-to-prior instead of an entropy bonus (**adopted today, and it is the fix that reversed
the decline for the first time in this project's history**) and autoregressive micro-steps. This is the
second half of the same solution. `CLAUDE.md` records that it was struck off for answering the wrong
question -- it was assessed against the spawn deadlock, when its author built it for **action-space
explosion**, which this project independently has and had measured three times.

**The template already exists in the codebase.** `condition_on_trade` in `jax_act.py` does exactly this
for `sell` and `buy_product`: the network emits a `[.., N_PRODUCTS, N_TRADE_MODES, K]` axis, `trade` is
drawn first, and the products are scored on the selected slice -- making `p(trade) * prod p(product|trade)`
exact rather than mean-field. Mirror it:

1. `jax_policy.py` -- give `crop`, `item`, `qty` an op axis: `[.., N_OPS, K]`.
2. `jax_act.py` -- add `condition_on_op(heads, op)` mirroring `condition_on_trade`.
3. `sample()` -- draw `op` first, condition, then draw `crop`/`item`/`qty` from the selected slice.
4. `evaluate()` -- condition on the **stored** op, for the same reason the trade mode is: scoring
   under a different slice puts a different distribution in the PPO ratio's numerator than the one
   that generated the data.
5. Consider the same for `buy_seed`/`buy_animal`/`hire`/`buy_land` on `trade`.

**Test it before trusting it:** the ratio must be 1.0 at the first epoch of the first minibatch when
params have not moved. If it is not, `sample` and `evaluate` disagree and every subsequent number lies.

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
1. **Read the per-day rates once `mix5d` has a few hundred games per day.** Day 25 accumulates ~6x
   faster than day 0 (episode length), so give it time. The question: are the middle rungs
   contributing, or is day 25 carrying four dead days?
2. **The opponent pool is the untouched suspect.** No opponent in it uses the animal economy -- the
   scripted farmer has no FEED, no CARE and `buy_animal=zeros`, and loses 16 inherited animals in four
   game-days, 32/32. No curriculum change addresses that. If win rate stalls, go here.
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
