# The clone opens correctly in `jax_sim` and then never farms

> **CORRECTED 2026-08-28, same night.** The first version of this file, and the title, read the
> turn-0 spend as the defect: *"$3,000 gone in one turn"*. That was wrong. The bundle it plays at
> turn 0 is index 39 --
> `BUY_ANIMAL COW x2, BUY_ANIMAL SHEEP x2, BUY_PRODUCT WHEAT, BUY_SEED MELON, BUY_SEED WHEAT,
> HIRE x5` -- which is カワシギ's opening, and spending ~$2,978 on it is the intended move. Both
> encodings choose bundle 39.
>
> The defect is the 719 turns AFTER the opening: it buys the farm and never works it, ending at $17.
> The op census from `data/logs/rl_smoke.log` is the shape of it --
> `noop 61%, move 37%, plant 0.17%, water 0.19%, harv 0.02%`.
>
> Everything below about sampling, the vocabulary and the commit layer being ruled out still holds.
> Only the reading of the turn-0 number changed.


Measured 2026-08-28.
`data/logs/clone_greedy_control.log` on the Windows box,
`scripts/control_what_the_clone_banks_under_greedy.py`,
`pinned_round27.pkl` with the 149-entry `bundle_vocab_teacher_pre_topup.json`.

## The number

16 games, 719 turns, GREEDY decode, commit layer included:

    turn   0 day  0  bank med $22        <- $3,000 gone in one turn
    turn 120 day  5  bank med $23
    turn 240 day 10  bank med $24
    turn 360 day 15  bank med $24
    turn 480 day 20  bank med $17
    turn 600 day 25  bank med $70
    FINAL   median $17   mean $17   min $0   max $37

Starting money is $3,000.
The same checkpoint reproduces its teacher to **$126,541 - $150,255** in the reference environment
(`data/logs/corrections_all.log`, `op_agreement.log`).

## What it rules out

**Sampling.** The RL smoke showed a median bank of $7 under PPO's sampled rollout
(`data/logs/rl_smoke.log`, entropy 74.8 nats), and the obvious reading was that the $126k is an
argmax property destroyed by exploration.
It is not: this control is argmax, the most favourable decode available, and it is no better.

**The vocabulary.** Asserted against `ckpt["vocab_size"]` before the run starts -- 149 against 149.
The checkpoint NAMES `bundle_vocab_teacher.json`, which is 151, so the assertion is load-bearing.

**The commit layer.** `train_jax_rl.py:515-518` overrides `to_sim_actions`' unit ops with
`CM.resolve`, and the control does the same. Running without it would have decoded the same logits
into different ops and made the result evidence about nothing.

## What it leaves

The failure is specific to the `jax_sim` path, so the suspects are the two bridges between it and
the reference environment:

1. **The observation bridge.** The clone was trained and measured on features from
   `adapter.state_from_obs` applied to a REFERENCE observation. Training and this control feed
   `jax_obs.encode` a native `jax_sim.State`. If the two entry points produce different tensors the
   network is looking at a different game.

   **The 300/300 parity gate does not cover this.** It tests the SIMULATOR against the reference,
   not the ENCODER's two entry points. Straight from `CLAUDE.md`: *a gate only tests what it
   exercises* -- now the fourth time in this project.

2. **The action bridge.** `jax_act.to_sim_actions`'s `gated()` is
   `jnp.where(want > 0, jnp.maximum(drawn, 1), 0)` over the `qty_*` heads, and `MAX_QTY` is 64.
   One bundle row selecting a purchase, plus a large quantity head, is exactly a $2,978 turn-0
   spend.

## The next measurement

Dump turn 0 in `jax_sim` -- bundle index, `qty_*` heads, the market orders produced, and the bank
delta -- and compare against the same checkpoint's turn 0 in the reference environment, where it is
known to spend correctly.

- orders differ, logits agree -> the ACTION bridge.
- logits differ -> the OBSERVATION bridge.

## RESOLVED: `jax_sim` is exonerated. The clone only works on its four tapes.

`data/logs/what_breaks_the_clone.log`, same checkpoint, same 149-entry vocab, and in the
**reference environment**:

    tape                    base   weeds .005   other opp    seed 9000
    92498144.json        149,599            0           0          300
    91907974.json         46,839       46,862           9          105

A different seed banks **$300** in the reference env; a different opponent banks **$0**. That is the
same regime as `jax_sim`'s $17, so the engine explains nothing that the SEED does not already
explain. The confound in the section above -- reference-vs-`jax_sim` varied together with
tape-seed-vs-fresh-seed -- resolves entirely on the seed side.

**The encoder-padding difference is a real bug and is not this bug.** It changes the live farmer's
op (1 vs 17) and two quantity heads, and it should be fixed so the two paths agree. It is not why
the clone banks $17, and fixing it would not make the clone play.

What the clone actually is: a policy that reproduces its teacher on four specific games and has
0.0003 agreement on a fresh one. Not overfitting in the mild sense -- it has memorised four
trajectories.

## Consequence

**RL from this checkpoint is blocked.** `--init` warm-starts a policy that has $22 by the end of its
first turn, and `--kl-prior` would anchor PPO to it. No value of `--ent-coef`, `--kl-coef` or `--lr`
repairs an agent whose first action is fatal.

This does not touch the imitation track: the kawa and Dusta replay clones train on recorded actions
and are measured by agreement, not by a `jax_sim` rollout.
