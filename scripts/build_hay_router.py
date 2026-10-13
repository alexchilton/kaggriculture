"""Put Hayashi's 13 live tapes into the E184 (twocoins) chassis.

The chassis picks a tape at step 144 from the first two unlocked shops, then
forces every world onto tape index 2 at step 648. That forced ending is correct
for the published set, where index 2 IS the shared continuation. It is wrong
here: his 13 live tapes agree on turns 0..143 and then all 13 diverge for the
rest, endings included. Splicing one world's last 71 turns onto the other twelve
would replay orders against inventory those tapes never built.

So three edits, all mechanical:
  actions.json   -> his 13 tapes, index 0 = the tape covering the most worlds
  SHOP_PLANS     -> his world -> tape map, everything unlisted falls to index 0
  forced ending  -> removed, each world keeps its own last 71 turns

Nothing else in the 960-line chassis changes.
"""
import json, re, shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "submission" / "twocoins"
DST = ROOT / "submission" / "hay_router"
LIB = ROOT / "submission" / "hay_library"


def main():
    index = json.loads((LIB / "index.json").read_text())
    order = [name for name, _ in Counter(index.values()).most_common()]
    for p in sorted(LIB.glob("tape_*.json")):          # tapes no world reached
        if p.name not in order:
            order.append(p.name)
    slot = {name: i for i, name in enumerate(order)}

    tapes = [json.loads((LIB / name).read_text()) for name in order]
    assert all(len(t) == 719 for t in tapes), [len(t) for t in tapes]

    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("__pycache__", "*.tar.gz"))
    (DST / "actions.json").write_text(json.dumps(tapes, separators=(",", ":")))

    src = (DST / "router.py").read_text()

    lines = ["SHOP_PLANS = {"]
    for world in sorted(index):
        a, b = world.split("|")
        if slot[index[world]]:                          # 0 is the default already
            lines.append(f'    ("{a}", "{b}"): {slot[index[world]]},')
    lines.append("}")
    plans = "\n".join(lines)
    src, n = re.subn(r"SHOP_PLANS = \{.*?\n\}", plans, src, count=1, flags=re.S)
    assert n == 1, "SHOP_PLANS block not found"

    for old, new, why in [
        ("        if step == FINAL_PLAN_STEP:\n            state.plan = 2\n", "",
         "no shared ending tape exists in his library"),
        ("_POLICY.tapes[2 if day >= 27 else native.plan]", "_POLICY.tapes[native.plan]",
         "the expansion layer must preview the same tape the core replays"),
        ("if state.plan!=2 or state.last_step!=712:return None",
         "if state.last_step!=712:return None",
         "the terminal rescue gated on the ending tape; its own preconditions gate it now"),
    ]:
        assert src.count(old) == 1, f"not found once: {why}"
        src = src.replace(old, new)

    (DST / "router.py").write_text(src)

    print(f"wrote {DST}")
    print(f"  {len(tapes)} tapes, {sum(len(json.dumps(t)) for t in tapes):,} bytes of actions")
    print(f"  default plan 0 = {order[0]} ({Counter(index.values())[order[0]]} worlds)")
    print(f"  SHOP_PLANS routes {len(index)} worlds over {len(set(index.values()))} tapes")
    unused = [n for n in order if n not in set(index.values())]
    if unused:
        print(f"  unreachable by world key: {unused}")


if __name__ == "__main__":
    main()
