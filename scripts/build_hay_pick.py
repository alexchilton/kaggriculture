"""A test rig: the E184 chassis forced onto one chosen library tape, every world.

`submission/hay_router` replays the tape Hayashi himself used in each world. That
choice came from however many ladder games he happened to play there, against
whatever opponent he drew. It is an observation, not an optimisation.

This rig makes the choice a free variable. HAY_TAPE names the library slot, the
router uses it in every world, and `scripts/tape_grid.py` runs all 13 against all
worlds so the assignment can be measured instead of copied.

Not a submission. It reads the environment, so it would score whatever the
grader's environment happened to hold.
"""
import json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "submission" / "twocoins"
DST = ROOT / "submission" / "hay_pick"
LIB = ROOT / "submission" / "hay_library"


def main():
    index = json.loads((LIB / "index.json").read_text())
    order = [n for n, _ in Counter(index.values()).most_common()]
    for p in sorted(LIB.glob("tape_*.json")):
        if p.name not in order:
            order.append(p.name)
    tapes = [json.loads((LIB / n).read_text()) for n in order]
    assert all(len(t) == 719 for t in tapes)

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__", "*.tar.gz"))
    (DST / "actions.json").write_text(json.dumps(tapes, separators=(",", ":")))
    (DST / "slots.json").write_text(json.dumps({n: i for i, n in enumerate(order)}, indent=2))

    src = (DST / "router.py").read_text()
    src, n = re.subn(r"SHOP_PLANS = \{.*?\n\}", "SHOP_PLANS = {}", src, count=1, flags=re.S)
    assert n == 1
    for old, new in [
        ("import copy", "import copy\nimport os"),
        ("            state.plan = SHOP_PLANS.get(tuple(shops[:2]), 0)",
         "            state.plan = int(os.environ.get('HAY_TAPE', '0'))"),
        ("        if step == FINAL_PLAN_STEP:\n            state.plan = 2\n", ""),
        ("_POLICY.tapes[2 if day >= 27 else native.plan]", "_POLICY.tapes[native.plan]"),
        ("if state.plan!=2 or state.last_step!=712:return None",
         "if state.last_step!=712:return None"),
    ]:
        assert src.count(old) == 1, f"not found once: {old[:60]}"
        src = src.replace(old, new)
    (DST / "router.py").write_text(src)
    print(f"wrote {DST}: {len(tapes)} slots, HAY_TAPE selects")
    for i, n_ in enumerate(order):
        print(f"  {i:>2} {n_}")


if __name__ == "__main__":
    main()
