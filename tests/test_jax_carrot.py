"""The carrot fleet must actually farm, not merely be legal.

`CLAUDE.md`'s standard for a scripted opponent is blunt: "An opponent does not need to be our best
agent. It needs to beat a policy that does nothing, by enough that doing nothing stops being a
draw." A port that runs, emits legal ops and banks its opening $3,000 is worthless as an opponent
and indistinguishable from a working one in any aggregate -- which is the failure this project has
hit repeatedly. So the gate here is the bank, measured over a real season from a real start.
"""

import jax
import jax.numpy as jnp
import numpy as np

from kagg.rl import jax_carrot
from kagg.sim import jax_sim as J
from kagg.sim import ops as O
from kagg.sim.tiles import CROP_INDEX


def _season(batch=3, turns=J.TURNS_PER_DAY * 30 - 1):
    """Run the agent against itself from a pristine board, returning the final state and op census.

    **`batch=3`, never 2.** `jax_sim` has two players, so at `batch=2` a `[B, 1]` array and a
    `[B, P, 1]` array broadcast by coincidence and a missing unit axis is invisible. The first
    draft of this file used `batch=2`, passed all four tests, and raised on the first real batch
    size tried. A gate only tests what it can reach.
    """
    state = J.reset(batch)

    def body(s, _):
        a = jax_carrot.actions(s)
        counts = jax.nn.one_hot(a.unit_op, O.N_OPS, dtype=jnp.float32).sum(axis=(0, 1, 2))
        return J.step(s, a), counts

    final, census = jax.lax.scan(body, state, None, length=turns)
    return final, census.sum(axis=0)


def test_the_carrot_fleet_beats_doing_nothing():
    """The gate. A season must end above the $3,000 it started with."""
    final, _ = _season()
    bank = np.asarray(final.farm.money)

    assert bank.min() > 3000.0, (
        f"ended on ${bank.min():,.0f} from a $3,000 start -- this agent destroys value and is "
        f"useless as an opponent, since a policy that passes every turn already beats it")


def test_the_carrot_fleet_completes_the_crop_chain():
    """Plant, water and harvest must all fire, in that rough proportion.

    A census is the cheapest way to catch a port that is *nearly* right: the melon port's whole
    history is ops that were legal, chosen, and never completed a chain. Harvest is the one that
    matters -- planting and watering with no harvest is the exact shape of the failure `commit.py`
    was written for.
    """
    _, census = _season()
    c = np.asarray(census)

    for name, idx in (("plant", O.PLANT_OP), ("water", O.WATER), ("harvest", O.HARVEST)):
        assert c[idx] > 0, f"{name} never fired in a whole season"

    assert c[O.HARVEST] > 0.02 * c[O.PLANT_OP], (
        f"harvested {c[O.HARVEST]:.0f} against {c[O.PLANT_OP]:.0f} plantings -- the chain does not "
        f"complete, which is legal-but-useless and is what a bank check alone would miss")


def test_the_carrot_fleet_hires_a_crew():
    """Crew is the measured bottleneck on production, and this agent's whole thesis is a fleet."""
    final, _ = _season()
    assert int(np.asarray(final.farm.n_units).min()) > 1, "never hired anyone"


def test_the_carrot_fleet_plants_carrots_and_nothing_else():
    """It is a single-crop agent; a port that silently planted crop 0 would still look busy."""
    final, _ = _season()
    crop = np.asarray(final.tiles.crop)
    planted = crop[crop >= 0]
    if planted.size:
        assert set(np.unique(planted)) <= {CROP_INDEX["CARROT"]}, "planted something other than carrot"
