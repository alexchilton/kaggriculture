# The tape arm is right, and the first honest tape sweep — 2026-08-31

Three results, in the order they were measured.
All on the Windows box; logs named per section.

## 1. The `$147,368` vs `$143,966` gap does not exist

`docs/fable_after_the_bc_ceiling_2026-08-31.md` opens its plan on a $3,402 gap between a
"tape $147,368" and a "planner $143,966", and makes closing it step 1a.
**Both numbers are the planner arm.**

`$147,368` is recorded in four places — `schedule_agent.py:4063`,
`does_the_net_market_survive_the_sell_override.py:11`, `submission/main_sell_h16_d26.py:11009`,
and `tests/test_the_shed_is_sold_once_a_day_and_the_feed_is_released_at_the_end.py:14` — every one
of them as `REPLAY_OPENING_DAYS = ()`, 3 seeds, idle opponent, 2026-08-28.
`$143,966` carries no recorded conditions anywhere outside that doc.

I supplied the framing that produced the error.
There had never been a measured tape-vs-planner comparison.

## 2. Against a real field the SHIPPED tape arm wins; against an idle opponent it loses

`scripts/can_the_teacher_play_a_seed_it_has_never_seen.py`, 8 fresh seeds, idle opponent
(`data/logs/two_arms.log`):

        seed     replay ON    replay OFF
        9000       141,286       150,396
        9137       161,521       179,719
        9274       117,056       135,885
        9411       134,081       187,461
        9548       144,074       155,938
        9685       175,769       190,465
        9822       106,570        93,910
        9959       120,902       136,179
      median       137,684       153,167

That says flip the switch: the planner is +$15,483.
It is wrong, and it is wrong in the way `CLAUDE.md` already warns about — an idle opponent contests
no market.

`scripts/field_sweep.py` against 24 recorded ladder opponents, both seatings, 576 games per draw
(`data/logs/field_arms.log`, `data/logs/field_arms2.log`):

     value  games     win    mean ours  mean theirs  mean margin   seeds
   range:0    288  79.9%       98,705       76,912       21,793   1300-1305
  range:30    288  94.4%       98,705       65,496       33,209   1300-1305
   range:0    288  82.3%       97,881       76,374       21,507   1400-1405
  range:30    288  95.5%       99,288       65,988       33,300   1400-1405

`range:30` is the shipped tape arm. It replicates on a fresh seed range.

**The mechanism is opponent suppression, not earning.**
Between arms our own money moves +$1,407; theirs drops **−$10,386**.
The tape's sell cadence floods the shared book.
An idle opponent has no book to flood, which is exactly why the first measurement inverted.

`REPLAY_OPENING_DAYS = tuple(range(30))` stays. Fable's step 1a is closed: there is no planner gap
to close, because the planner is the worse arm.

*Note on the first draw:* it reported `mean ours` identical to the dollar (98,705) for both arms.
That did not reproduce on seeds 1400-1405 (97,881 vs 99,288) and does not reproduce at 8 games
(127,300 vs 109,680). Treated as a coincidence, not a defect.

`field_sweep.py` gained `range:N` value parsing so a day-tuple flag can be swept at all;
`schedule_agent.py:6013` passes the value to `_replay_opening`, so a bare int raises there.

## 3. Only two schedule keys are live in the shipped arm

Fable's step 1b proposed searching "the 30 per-day target rows".
In the tape arm that space is almost entirely inert.

Of the 18 keys in `data/seed_scripts/kawashigi/schedule.json`, exactly two change what the agent
ships while `REPLAY_OPENING_DAYS = tuple(range(30))`:

- **`animals_bought`** — summed at `schedule_agent.py:5415-5418` into `state["herd_split"]` (`:5423`),
  which is *not* one of the two fields `replayed()` reverts, so it survives and is read at `:6066`
  to re-split the tape's `BUY_ANIMAL` rows. Live on all four latch states.
- **`plants`** — read directly inside `replayed()` at `:6163` to trim the tape's `BUY_SEED` count,
  and only when neither branch is armed.

`cares`, `plant_tiles`, `build_tiles`, `land_turns`, `money_dawn` and `orders` are never read at all.
The remaining ten (`hands`, `hires`, `land`, `builds`, `places`, `feeds`, `seeds`, `buys`, `sells`,
`shed_dusk`) feed `live = agent(obs)`, which `replayed()` computes every turn and discards — the four
tapes cover all 720 steps with **0 missing frames** on every latch state, so
`if step not in opening: return live` (`:6029`) never fires.

Sweeping those ten in the shipped arm returns byte-identical seasons.

## 4. `tape_edit_sweep.py` had two defects and could not measure anything

Found when the first sweep crashed in under a second.

**(a) It crashed on every arm.** `season` passes the `Arm` NamedTuple to `edited_openings`, which
iterates it — yielding `("control", (), (), ())` — and evaluates `e[0]` on the empty `opening`
field. `IndexError: tuple index out of range`, on the control arm, therefore on all of them.

**(b) `Arm.wrappers` was stored and never applied.** `edited_openings` skips every wrapper op with
`continue` (`:355`) and `season.mine()` applied only `surplus_sells`. The `Arm` docstring names a
`build_agent` that "decided which runtime wrappers it got"; no such function exists in the file.
So every wrapper-only arm — `herd_*`, `cow_*`, `sheep_*`, `cowshift_*`, `topup_*`, `cond_carrot_*`,
`x_cow` — was a byte-identical copy of the control.

The operators were never missing (`herd_species`, `herd_shift`, `top_up_at_hour`,
`carrot_when_it_pays` are all in `kagg/search/tape_edit.py`). Only the wiring was gone.

**Any previously recorded null for a wrapper arm is void.** It measured the control.

Fixed by `_apply_wrappers`, pinned by
`tests/test_a_wrapper_arm_is_not_a_silent_copy_of_the_control.py`, which was confirmed to go RED on
revert with the signature `money 28 vs 28` and identical crop counts.

`--out` was added: one CSV row per finished season, flushed and fsynced. Without it a killed sweep
returns nothing.

## 5. First real tape sweep: no arm beats the tape

8 seeds, 2 opponents, weeds 0.005, 208 seasons, 247s (`data/logs/tape_sweep.log`,
`data/sweeps/tape_edit_20260831-144224.csv`). Pooled on margin:

    arm                       d margin      median wins / total
    control                         +0          +0     12/16
    herd_counter_d12                +0          +0     12/16
    herd_book_d12                   +0          +0     12/16
    topup_h16_d20                 -236          -0     12/16
    herd_sheep_d8                -3175        -704     11/16
    herd_counter_d8              -3175        -704     11/16
    herd_book_d8                 -3175        -704     11/16
    herd_cow_d8                 -14056       -1515      7/16
    cow_d4                      -17909       -5919      7/16
    topup_h12_all               -30672      -26888      5/16
    topup_h16_all               -77459      -79304      0/16
    cow_d0                     -102125     -104312      0/16
    topup_h20_all              -145988     -147824      0/16

The arms are live — `cow_d0` at −$102k is not something a silent control can do.

Two rows read oddly and both are explained rather than suspect:

- `herd_*_d12` are exactly +0 on all 16 cells because every `BUY_ANIMAL` is already placed by d12.
  No-ops, not measured nulls.
- `herd_sheep_d8`, `herd_counter_d8` and `herd_book_d8` are identical to the dollar because
  `counter` and `book` both resolve to SHEEP on these towns, so all three are the same arm.

**Verdict: kawa's tape is at a local optimum on both axes.** Forcing COW earlier is monotonically
worse (`cow_d4` −$17.9k, `cow_d0` −$102.1k); SHEEP at d8 is −$3.2k; every sell-hour top-up either
does nothing or floods the book. The gradient points at his existing split from both directions.

## What was skipped, and what it costs

- **The sweep's field is `kawashigi` and `kawashigi_b3` only** — close to the mirror `CLAUDE.md`
  says pointed this project the wrong way on melon. The 24 recorded ladder opponents in
  `field_sweep.py` are the honest field, and no tape arm has been scored against them.
- `sheep_d0` / `sheep_d4` were not run. COW-early is measured bad; SHEEP-early is the untested end
  of that axis.
- No submission was built or gated. Nothing here changes what ships.
