"""The opponent pool must be seeded from the params we actually start training from.

**The bug this pins.** `train_jax_rl.py` built the pool and called `pool.add(params)` at line 1780,
*thirty lines before* `if args.resume:` at line 1811 replaced `params` with the checkpoint's weights.
`Pool.add` stores a snapshot, not a reference, so the pool's anchor member held the **randomly
initialised network** for the entire run. Every resumed run therefore spent `--opponent-frac` -- 45%
of the batch on the day it was caught -- playing a network that cannot teach anything.

Measured when it finally bit, resuming `day0-long` at update 818:

    block      farm         ranch        home         pool        bank_fin
    15- 29   0.000(19g)  0.118(17g)  0.000( 4g)  1.000(46g)     14,541
    30- 44   0.000(42g)  0.057(35g)  0.077(13g)  1.000(70g)     12,224
    45- 59   0.000(39g)  0.000(33g)  0.000(21g)  0.894(66g)      6,006
    60- 74   0.000(41g)  0.000(24g)  0.000(14g)  1.000(80g)      6,783

`wr_pool` reading **1.000 over 80 games** is the tell -- a correctly seeded pool sits near 0.5,
because its anchor is a snapshot of us. `bank_final_med` halved from $18,332 and `wr_farm` went from
0.254 to 0/141 in 75 updates as the policy drifted toward beating a random opponent.

**Why it hid for so long.** A *fresh* run seeds the pool from its own initialisation, which is
correct. The defect exists only on the resume path, and there it presents as "the pool got easy" --
a metric moving in the direction that normally means progress. `CLAUDE.md`: *"A gate only tests what
it cannot reach."*

**Why this test is structural.** The invariant is an ordering inside a 2,700-line `main()` that
takes a GPU, a simulator and hours to run; there is no seam to call. So we assert the ordering
directly on the parsed source. That is narrower than a behavioural test and it is stated plainly
here rather than dressed up -- but it is decisive for the exact regression, which is someone moving
the seeding call back above the resume block.
"""

import ast
import pathlib

import pytest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "train_jax_rl.py"


@pytest.fixture(scope="module")
def main_fn():
    tree = ast.parse(SCRIPT.read_text())
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"]
    assert len(fns) == 1, "expected exactly one top-level `main` in train_jax_rl.py"
    return fns[0]


def _pool_add_lines(node, arg="params"):
    """Lines of every `pool.add(<...arg...>)` call inside `node`.

    `arg` matters. `main` also seeds the pool with `prior_params` (the `--kl-prior` anchor) *before*
    the resume block, and that one is correct -- `prior_params` is loaded from its own flag and
    `--resume` never touches it. Matching on the bare attribute name would flag it and make this
    test fail on the fixed source, so we resolve the argument's identifier and match exactly.
    """
    out = []
    for n in ast.walk(node):
        if not (isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute) and n.func.attr == "add"
                and isinstance(n.func.value, ast.Name) and n.func.value.id == "pool"):
            continue
        names = {x.id for a in n.args for x in ast.walk(a) if isinstance(x, ast.Name)}
        if arg in names:
            out.append(n.lineno)
    return out


def _resume_block(node):
    """The `if args.resume:` statement in `node`, which is the one that rebinds `params`."""
    for n in ast.walk(node):
        if not isinstance(n, ast.If):
            continue
        t = n.test
        if isinstance(t, ast.Attribute) and t.attr == "resume" \
                and isinstance(t.value, ast.Name) and t.value.id == "args":
            return n
    return None


def test_the_resume_block_still_rebinds_params(main_fn):
    """Guards the premise. If `--resume` stopped assigning `params` this test would pass for the
    wrong reason, so pin that it does."""
    blk = _resume_block(main_fn)
    assert blk is not None, "no `if args.resume:` block found -- has resume been renamed?"
    targets = {t.id for n in ast.walk(blk) if isinstance(n, ast.Assign)
               for t in n.targets if isinstance(t, ast.Name)}
    assert "params" in targets, "the resume block no longer rebinds `params`"


def test_the_pool_is_seeded_after_the_resume_block(main_fn):
    """**The regression.** Seeding must happen below the last line of `if args.resume:`, so the
    snapshot it stores is the checkpoint's weights and not the initialisation's."""
    blk = _resume_block(main_fn)
    seeds = _pool_add_lines(main_fn)
    assert seeds, "no `pool.add(...)` call found in main()"
    assert min(seeds) > blk.end_lineno, (
        f"`pool.add` at line {min(seeds)} runs before the `if args.resume:` block ends at "
        f"{blk.end_lineno}: the pool would be seeded with randomly initialised weights on every "
        f"resumed run. Move the seeding below the resume block."
    )


def test_the_pool_is_seeded_exactly_once_at_startup(main_fn):
    """Two `params` seedings would put a stale anchor back in even with the ordering right. The
    training loop adds snapshots on its own `--pool-every` schedule; startup contributes exactly one
    from `params`, plus the separate and legitimate `prior_params` anchor this helper ignores."""
    seeds = _pool_add_lines(main_fn)
    blk = _resume_block(main_fn)
    startup = [ln for ln in seeds if ln <= blk.end_lineno + 40]
    assert len(startup) == 1, f"expected one startup `pool.add`, found {len(startup)} at {startup}"
