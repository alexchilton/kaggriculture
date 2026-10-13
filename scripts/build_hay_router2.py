"""Build submission/hay_router2: the measured world -> tape map.

Same three chassis edits as build_hay_router.py. The only difference is the map.
His map was an observation of what he ran; this one is the argmax of a 13,312-game
grid, and it uses four of his tapes instead of ten:

    tape_98   default, everywhere not listed below
    tape_104  YARN_STORE paired second, plus YARN_STORE|BAKERY and |ICE_CREAM_SHOP
    tape_101  YARN_STORE paired first, plus the PET_CAFE worlds
    tape_108  BAKERY|FARMERS_MARKET
"""
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "submission" / "twocoins"
DST = ROOT / "submission" / "hay_router2"
LIB = ROOT / "submission" / "hay_library"
PICKS = ROOT / "data" / "logs" / "picks_vs_best.json"
DEFAULT = "tape_98.json"


def main():
    picks = json.loads(PICKS.read_text())
    # The chassis refuses anything but 13 tapes ("Expected 13 complete, 719-turn
    # action tapes", router.py:213), and it falls back to index 0, so tape_98 has
    # to sit at 0 and the unused tapes have to stay in the file.
    rest = sorted(p.name for p in LIB.glob("tape_*.json") if p.name != DEFAULT)
    order = [DEFAULT] + rest
    slot = {n: i for i, n in enumerate(order)}
    assert len(order) == 13, len(order)
    tapes = [json.loads((LIB / n).read_text()) for n in order]
    assert all(len(t) == 719 for t in tapes)

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__", "*.tar.gz"))
    (DST / "actions.json").write_text(json.dumps(tapes, separators=(",", ":")))

    src = (DST / "router.py").read_text()
    lines = ["SHOP_PLANS = {"]
    for world in sorted(picks):
        if slot[picks[world]]:
            a, b = world.split("|")
            lines.append(f'    ("{a}", "{b}"): {slot[picks[world]]},')
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
    print(f"wrote {DST}")
    print(f"  {len(tapes)} tapes: {order}")
    print(f"  {sum(1 for w in picks if slot[picks[w]])} worlds routed, rest default {DEFAULT}")

    # Smoke test. The chassis validates actions.json at first call and
    # kaggle_environments swallows the exception, leaving the bank at its starting
    # 3000 with status DONE -- which reads exactly like a catastrophically bad agent.
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": 11}, debug=False)
    env.run([str(DST/"main.py"), str(ROOT/"submission"/"shop0909"/"main.py")])
    bank = env.steps[-1][0]["reward"]
    status = [s["status"] for s in env.steps[-1]]
    assert bank > 3000, f"agent never acted: bank={bank} status={status}"
    print(f"  smoke seed 11 vs 0909: bank {bank:,.0f}, status {status}")


if __name__ == "__main__":
    main()
