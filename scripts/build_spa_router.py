"""SpaTaro's world-keyed tapes in the E184 chassis.

Same three edits as build_hay_router.py, and for the same reason: the chassis forces every
world onto tape index 2 at step 648, which is correct only for the published set where
index 2 IS a shared continuation. These are 13 independent seasons, so each world keeps
its own ending.

Smoke test at the end is not optional -- the chassis validates actions.json on first call
and kaggle_environments swallows the exception, leaving the bank at its starting 3000 with
status DONE, which reads exactly like a catastrophically bad agent rather than a broken one.
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "submission" / "twocoins"
DST = ROOT / "submission" / "spa_router"
LIB = ROOT / "submission" / "spa_library"


def main():
    tapes = json.loads((LIB / "actions.json").read_text())
    index = json.loads((LIB / "index.json").read_text())
    assert len(tapes) >= 1 and all(len(t) == 719 for t in tapes)

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__", "*.tar.gz"))
    (DST / "actions.json").write_text(json.dumps(tapes, separators=(",", ":")))

    src = (DST / "router.py").read_text()
    # The "exactly 13" check describes the published set, not the replay. Relaxing it
    # lets every world he played keep its own season; capping at 13 routed seed 11 to a
    # tape from another town and cost 47k on that seed.
    old_check = ('        if len(self.tapes) != 13 or any(len(tape) != LAST_STEP + 1 '
                 'for tape in self.tapes):\n'
                 '            raise ValueError("Expected 13 complete, 719-turn action tapes")')
    new_check = ('        if not self.tapes or any(len(tape) != LAST_STEP + 1 '
                 'for tape in self.tapes):\n'
                 '            raise ValueError("Expected complete, 719-turn action tapes")')
    assert src.count(old_check) == 1, "tape-count check not found"
    src = src.replace(old_check, new_check)
    lines = ["SHOP_PLANS = {"]
    for world in sorted(index):
        a, b = world.split("|")
        lines.append(f'    ("{a}", "{b}"): {index[world]},')
    lines.append("}")
    src, n = re.subn(r"SHOP_PLANS = \{.*?\n\}", "\n".join(lines), src, count=1, flags=re.S)
    assert n == 1
    for old, new in [
        ("        if step == FINAL_PLAN_STEP:\n            state.plan = 2\n", ""),
        ("_POLICY.tapes[2 if day >= 27 else native.plan]", "_POLICY.tapes[native.plan]"),
        ("if state.plan!=2 or state.last_step!=712:return None",
         "if state.last_step!=712:return None"),
    ]:
        assert src.count(old) == 1, old[:50]
        src = src.replace(old, new)
    (DST / "router.py").write_text(src)

    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": 11}, debug=False)
    env.run([str(DST / "main.py"), str(ROOT / "submission" / "shop0909" / "main.py")])
    bank = env.steps[-1][0]["reward"]
    assert bank > 3000, f"agent never acted: bank={bank}"
    print(f"wrote {DST}: {len(tapes)} SpaTaro tapes, {len(index)} worlds routed")
    print(f"  smoke seed 11 vs 0909: bank {bank:,.0f}  "
          f"(hay_router 135,963 on this seed)")


if __name__ == "__main__":
    main()
