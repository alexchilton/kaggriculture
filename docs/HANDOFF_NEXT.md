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
