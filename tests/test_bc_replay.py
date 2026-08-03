"""Behaviour cloning from the winners' replays: the four properties that decide whether it trains
on what the teacher actually did.

Every one of these pins a mistake this project has already paid for.

`test_plant_actions_carry_their_crop` is a **correction to `docs/HANDOFF.md`**, which states as
measured fact that "`PLANT` carries NO crop argument -- the crop comes from seeds held". It does
carry one, in every replay and in the reference environment, which refuses a PLANT with
`if len(action) < 2: return`. Believing otherwise means either dropping the crop head from the loss
or -- worse -- training every PLANT toward crop index 0, which is WHEAT. This test is here because
the doc is more likely to be read than the data.

The other three are the recurring shapes: a masked-illegal label is `-1e9` and swamps the objective
(`bc_dagger.py` reported a loss of 5.3e7 that would not move), a rate computed over `MAX_UNITS` is
padding rather than measurement, and a conditioned head trained under one trade mode is untrained
under the two the sampler will actually pick two thirds of the time.
"""

import json
from pathlib import Path

import numpy as np
import pytest

from kagg.il import bc, replays
from kagg.rl import jax_policy as P
from kagg.sim import jax_sim as J
from kagg.sim import ops as O
from kagg.sim.tiles import CROP_INDEX

DATA = Path(__file__).resolve().parent.parent / "data"
REPLAYS = bc.find_replays(DATA)

pytestmark = pytest.mark.skipif(not REPLAYS, reason="replay data not downloaded")


def _unit_actions(path):
    """Every unit action in one replay, farmer first, as the environment reads them."""
    for step in json.loads(Path(path).read_text())["steps"]:
        for entry in step[:2]:
            action = entry.get("action") or {}
            farmer = action.get("farmer")
            for act in ([farmer] if farmer else []) + list(action.get("hands") or []):
                if isinstance(act, list) and act:
                    yield act


def test_a_replay_observation_is_the_state_after_its_own_action():
    """**`steps[t]["observation"]` is the state the action at `steps[t]` already produced.**

    So the state a teacher *decided from* is `steps[t-1]`, and pairing `obs[t]` with `action[t]` --
    which is what `iter_turns` did -- trains the policy to read an action off its own consequences.
    That is not a subtle leak: WATER, PLANT and FEED all act on the tile the unit stands on, so under
    the wrong pairing the label was illegal on **100%** of rows (FEED 0 legal of 9,097) and those
    ops could not be learned at all, while movement and NOOP still looked fine.

    It also explains the parked BC track's headline symptom. Given a post-action observation, "what
    did you do?" is trivially readable, so offline accuracy flatters -- and at spawn a PASS leaves
    the state identical, which is `P(noop) = 0.9920`.

    Measured two independent ways, both pinned below: a MOVE's effect on the farmer's own
    coordinates, and the number of hand actions against the crew that existed.
    """
    deltas = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
    after = before = moves = 0
    crew_prev = crew_cur = turns = 0

    for path in REPLAYS[:6]:
        steps = json.loads(Path(path).read_text())["steps"]
        for seat in range(2):
            def farm(t, seat=seat):
                return steps[t][seat]["observation"]["farms"][seat]

            for t in range(1, len(steps) - 1):
                action = steps[t][seat].get("action") or {}
                if not action.get("farmer"):
                    continue
                n_hands = len(action.get("hands") or [])
                crew_prev += n_hands == len(farm(t - 1).get("hands") or [])
                crew_cur += n_hands == len(farm(t).get("hands") or [])
                turns += 1

                op = action["farmer"][0]
                if op not in deltas or t % 24 == 0:
                    # Skip the day boundary: the crew is dismissed and the farmer respawns at the
                    # shed overnight, so the position change is the reset rather than the move.
                    continue
                dx, dy = deltas[op]
                prev, cur, nxt = farm(t - 1)["farmer"], farm(t)["farmer"], farm(t + 1)["farmer"]
                after += (cur[0] - prev[0], cur[1] - prev[1]) == (dx, dy)
                before += (nxt[0] - cur[0], nxt[1] - cur[1]) == (dx, dy)
                moves += 1

    assert moves > 500 and turns > 500, "not enough turns sampled to conclude anything"
    assert after / moves > 0.99, (
        f"a MOVE at t explains obs[t-1] -> obs[t] only {100 * after / moves:.1f}% of the time")
    assert after > before * 2, "the two pairings are not distinguishable on this data"
    assert crew_prev / turns > 0.99, (
        f"hand-action count matches the crew in obs[t-1] only {100 * crew_prev / turns:.1f}%")
    assert crew_prev > crew_cur


@pytest.mark.slow
def test_iter_turns_yields_the_state_the_action_was_decided_from():
    """The consumer-facing half of the property above.

    `iter_turns` must hand out the *pre-action* observation, or every row `build_rows` produces has
    the label's own effect already visible in its features.
    """
    path = REPLAYS[0]
    steps = json.loads(Path(path).read_text())["steps"]
    deltas = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}

    # Turns come out in recorded order, so the i-th yielded pair carries the i-th action. Its
    # outcome is the observation recorded alongside that same action.
    checked = 0
    for i, (obs, _privs, action, seat) in enumerate(
            replays.iter_turns(path, winners_only=False, seats={0})):
        op = (action.get("farmer") or ["PASS"])[0]
        outcome_step = len(steps) - sum(
            1 for _ in replays.iter_turns(path, winners_only=False, seats={0})) + i
        if op not in deltas or outcome_step % 24 == 0:
            continue
        x, y = obs["farms"][seat]["farmer"]
        dx, dy = deltas[op]
        landed = steps[outcome_step][seat]["observation"]["farms"][seat]["farmer"]
        assert (landed[0], landed[1]) == (x + dx, y + dy), (
            f"yielded obs has farmer at ({x},{y}); {op} should land on "
            f"({x + dx},{y + dy}) but the replay records {tuple(landed)}")
        checked += 1
        if checked >= 40:
            break
    assert checked >= 20, f"only {checked} move turns checked"


def test_find_replays_matches_both_naming_conventions():
    """`fetch_replays.py` has written two naming conventions and a `[0-9]*.json` glob found 126 of
    156 -- it drops every `episode-*-replay.json` silently, so the teacher set and the top-25 cut
    both change with no error anywhere.

    The negative half matters as much: `plan_*.json`, `search_history.json` and the seat index share
    the directory and are not replays.
    """
    names = [p.name for p in REPLAYS]
    assert any(n[0].isdigit() for n in names), "no bare-id replays matched"
    assert any(n.startswith("episode-") for n in names), "no episode-*-replay.json matched"
    assert not [n for n in names if n.startswith("plan_") or n in
                ("replay_index.json", "search_history.json")], "non-replay JSON matched"


def test_plant_actions_carry_their_crop():
    """`HANDOFF.md` says they do not. They do, and the crop is element 1.

    If this ever goes red the crop head must be dropped from the loss rather than trained toward
    index 0, because index 0 is WHEAT -- a real crop, and the wrong answer on every melon tile.
    """
    plants = [a for p in REPLAYS[:8] for a in _unit_actions(p) if a[0] == "PLANT"]
    assert plants, "no PLANT actions found at all -- check the action format, not the agents"

    bare = [a for a in plants if len(a) < 2]
    assert not bare, f"{len(bare)} of {len(plants)} PLANT actions carry no crop argument"

    named = {a[1] for a in plants}
    assert named <= set(CROP_INDEX), f"unknown crop names in PLANT: {named - set(CROP_INDEX)}"
    assert len(named) > 1, f"only ever one crop planted ({named}) -- suspect the parser, not the play"


def test_encode_action_keeps_the_crop_the_teacher_named():
    """The label has to be the crop in the action, not a default."""
    for path in REPLAYS[:8]:
        for step in json.loads(Path(path).read_text())["steps"]:
            for entry in step[:2]:
                action = entry.get("action") or {}
                units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
                wanted = {i: CROP_INDEX[a[1]] for i, a in enumerate(units[: J.MAX_UNITS])
                          if isinstance(a, list) and len(a) > 1 and a[0] == "PLANT"}
                if not wanted:
                    continue
                labels = replays.encode_action(action, len(units))
                for slot, crop in wanted.items():
                    assert labels["op"][slot] == O.PLANT_OP
                    assert labels["crop"][slot] == crop, (
                        f"slot {slot}: labelled crop {labels['crop'][slot]}, teacher named {crop}")
                return
    pytest.skip("no PLANT action in the sampled replays")


@pytest.mark.slow
def test_the_top_seats_demonstrate_feed_and_care():
    """The reason this track exists.

    FEED has fired exactly zero times in every RL run in this project, and `jax_heuristic` cannot
    teach it -- its `buy_animal` is hard-zero. If the replay labels do not contain FEED either then
    there is no teacher anywhere and cloning them cannot possibly move it, so this is a precondition
    on the whole job rather than a detail of the encoder.
    """
    ranked = bc.rank_seats(REPLAYS)[:8]
    assert ranked, "no seats ranked"

    counts = np.zeros(O.N_OPS)
    for ref in ranked:
        for _obs, _privs, action, _seat in replays.iter_turns(
                ref.path, winners_only=False, seats={ref.seat}):
            labels = replays.encode_action(action, J.MAX_UNITS)
            counts += np.bincount(labels["op"], minlength=O.N_OPS)

    assert counts[O.FEED] > 0, "top seats never FEED -- they are the wrong teachers"
    assert counts[O.CARE] > 0, "top seats never CARE"


def test_a_masked_illegal_label_contributes_nothing():
    """A label the student cannot emit must be dropped, not scored.

    Scoring it asks for the log-probability of an option at `NEG_INF = -1e9`, and one such row
    swamps every real one. This is exactly the 5.3e7 loss that would not move.
    """
    logits = np.zeros((4, 3), dtype=np.float32)
    mask = np.ones((4, 3), dtype=bool)
    label = np.array([0, 1, 2, 1], dtype=np.int32)
    mask[2, 2] = False                                  # row 2's label is illegal

    logp, weight = bc.head_term(logits, mask, label)
    weight = np.asarray(weight)

    assert weight[2] == 0.0
    assert np.all(weight[[0, 1, 3]] == 1.0)
    assert np.isfinite(bc.weighted_mean(logp, weight))
    assert abs(float(bc.weighted_mean(logp, weight))) < 10.0, "an illegal row leaked into the mean"


def test_dead_unit_slots_do_not_move_the_loss():
    """`MAX_UNITS` is 24 against a crew of about twelve.

    "Any rate computed over `MAX_UNITS` is wrong" is a rule this project wrote after the same
    padding mistake in three separate places, one of them a BC loss.
    """
    logits = np.zeros((1, J.MAX_UNITS, O.N_OPS), dtype=np.float32)
    mask = np.ones((1, J.MAX_UNITS, O.N_OPS), dtype=bool)
    live = np.zeros((1, J.MAX_UNITS), dtype=np.float32)
    live[0, :3] = 1.0

    a = np.zeros((1, J.MAX_UNITS), dtype=np.int32)
    b = a.copy()
    b[0, 3:] = 7                                        # change only the dead slots

    la, wa = bc.head_term(logits, mask, a, live=live)
    lb, wb = bc.head_term(logits, mask, b, live=live)

    assert float(wa.sum()) == 3.0
    assert float(bc.weighted_mean(la, wa)) == float(bc.weighted_mean(lb, wb))


def test_a_conditioned_head_is_cloned_under_every_trade_mode():
    """`sell` and `buy_product` carry a trade-mode axis, and the sampler draws the mode.

    Training only the mode-0 slice leaves the other two at initialisation, so two turns in three the
    market behaviour of a warm-started policy is untrained noise -- while the offline loss looks
    fine, because it only ever measured the slice it trained.
    """
    n_prod, k = J.N_PRODUCTS, len(P.SELL_BUCKETS)
    logits = np.zeros((2, n_prod, P.N_TRADE_MODES, k), dtype=np.float32)
    mask = np.ones((2, n_prod, k), dtype=bool)
    label = np.zeros((2, n_prod), dtype=np.int32)

    base = bc.conditioned_term(logits, mask, label)
    bumped = logits.copy()
    bumped[:, :, P.N_TRADE_MODES - 1, 0] = 5.0          # only the last mode

    after = bc.conditioned_term(bumped, mask, label)
    assert float(bc.weighted_mean(*after)) > float(bc.weighted_mean(*base)), \
        "the last trade mode does not enter the loss -- only its mode-0 slice is being cloned"


@pytest.mark.slow
def test_built_rows_use_the_current_observation_widths():
    """The observation width is part of the checkpoint, and `--init` refuses a mismatch.

    Building against a stale width wastes the whole PPO run it was meant to warm-start, so the
    builder is checked against `jax_obs`'s own constants rather than against numbers written down.
    """
    from kagg.rl import jax_obs

    ref = bc.rank_seats(REPLAYS)[0]
    rows = bc.build_rows([ref], max_turns=6)

    assert rows["tiles"].shape[1:] == (J.TILES, jax_obs.TILE_FEATURES)
    assert rows["units"].shape[1:] == (J.MAX_UNITS, jax_obs.UNIT_FEATURES)
    assert rows["glob"].shape[1:] == (jax_obs.GLOBAL_FEATURES,)
    for name, arr in rows.items():
        if arr.dtype.kind == "f":
            assert np.isfinite(arr).all(), f"{name} has non-finite entries"
    assert rows["y_op"].shape == (len(rows["tiles"]), J.MAX_UNITS)
    assert rows["live"].sum() > 0, "no live unit in six turns of a $100k seat"
