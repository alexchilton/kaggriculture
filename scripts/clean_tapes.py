"""Strip same-turn BUY+SELL of one product from the tapes themselves.

Buying and selling the same good in one turn pays the market spread for no goods. The tapes carry
these -- tape 4's turns 4-11 are `BUY WHEAT 16 + SELL WHEAT 16`, `BUY 15 + SELL 15`, `BUY 13 + SELL
13` -- and executing them cost a live game (episode 108326043): day 0 closed on exactly $0, the
day-1 `HIRE x3` costing $4 was silently refused, and a farm with no hands lost two animals.

Doing it in the DATA rather than in a runtime wrapper: the tape is then inspectable, the fix is
verifiable offline, and no code runs per turn that can swallow an exception.

Only the overlap is removed. `BUY 30 + SELL 30` becomes nothing; `BUY 13 + SELL 30` keeps `SELL 17`,
which is what the farm actually disposes of.

    python -u scripts/clean_tapes.py data/tapes_clean.json
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "submission/hay_router2/actions.json"


def clean_turn(act):
    market = (act or {}).get("market") or []
    buys, sells = collections.Counter(), collections.Counter()
    for o in market:
        if not o or len(o) < 3:
            continue
        if o[0] == "BUY_PRODUCT":
            buys[o[1]] += int(o[2])
        elif o[0] == "SELL":
            sells[o[1]] += int(o[2])
    overlap = {k: min(v, sells[k]) for k, v in buys.items() if sells[k] > 0}
    if not overlap:
        return act, 0
    left_b, left_s = dict(overlap), dict(overlap)
    out, cut = [], 0
    for o in market:
        o = list(o)
        if o and len(o) >= 3 and o[0] == "BUY_PRODUCT" and left_b.get(o[1], 0) > 0:
            n = min(int(o[2]), left_b[o[1]])
            o[2] = int(o[2]) - n
            left_b[o[1]] -= n
            cut += n
        elif o and len(o) >= 3 and o[0] == "SELL" and left_s.get(o[1], 0) > 0:
            n = min(int(o[2]), left_s[o[1]])
            o[2] = int(o[2]) - n
            left_s[o[1]] -= n
        if len(o) < 3 or int(o[2]) > 0:
            out.append(o)
    new = dict(act)
    new["market"] = out
    return new, cut


def main():
    out_path = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "data/tapes_clean.json")
    tapes = json.loads(SRC.read_text())
    cleaned, per_tape = [], []
    for ti, tape in enumerate(tapes):
        turns, units = 0, 0
        new_tape = []
        for act in tape:
            new, cut = clean_turn(act)
            if cut:
                turns += 1
                units += cut
            new_tape.append(new)
        cleaned.append(new_tape)
        per_tape.append((ti, turns, units))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(cleaned))
    print(f"{'tape':>5}{'turns cleaned':>15}{'units cancelled':>17}")
    for ti, t, u in per_tape:
        print(f"{ti:>5}{t:>15}{u:>17,}")
    print(f"\ntotal: {sum(t for _,t,_ in per_tape)} turns, "
          f"{sum(u for _,_,u in per_tape):,} units across 13 tapes")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
