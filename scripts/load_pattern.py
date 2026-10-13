"""How he LOADS: one pickup serving how many jobs, and when produce goes back.

The walk pattern match (`scripts/walk_pattern.py`) held the tile SET fixed and measured order only,
so it says nothing about whether a route is feasible. Feeding consumes a wheat from the unit's own
inventory (`reference/kaggriculture.py:504`), planting consumes seed, and the market reads the SHED,
never a hand -- so tile order cannot be chosen on geometry alone.

Alex: "does it still get everything done with picking up and droping all that are necessary etc for
loading in 1 go or so? and the waterings and feedings or bringing harvest back - these are extra
criteria needing taking into consideration?"

This measures the loading structure of a day, his and ours side by side:

    draws           PICKUP ops per unit-day, and the units drawn per draw
    jobs per draw   how many FEED/PLANT/FERTILIZE follow one draw before the next
    deposits        DROP and PLACE per unit-day
    span            turns between the first HARVEST/COLLECT and the deposit that banks it --
                    the latency the market sees
"""
import argparse, collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TPD = 24
DRAW = {"PICKUP"}
SPEND = {"FEED", "PLANT", "FERTILIZE"}
GAIN = {"HARVEST", "COLLECT_FERTILIZER"}
PUT = {"DROP", "PLACE"}


def ops_by_unit(blob, team, days):
    names = list((blob.get("info") or {}).get("TeamNames") or [])
    seat = names.index(team) if team in names else 0
    steps = blob["steps"]
    for day in days:
        seq = collections.defaultdict(list)
        for h in range(TPD):
            t = day * TPD + h
            if t >= len(steps):
                break
            act = steps[t][seat].get("action") or {}
            acts = [act.get("farmer")] + list(act.get("hands") or [])
            for u, a in enumerate(acts):
                if a:
                    seq[u].append((h, a[0], a[1] if len(a) > 1 else None,
                                   a[2] if len(a) > 2 and isinstance(a[2], int) else 1))
        for u, s in seq.items():
            yield day, u, s


def summarise(seqs, label):
    draws, per_draw, deposits, spans, drawn_units = [], [], [], [], []
    for _day, _u, s in seqs:
        d = [x for x in s if x[1] in DRAW]
        p = [x for x in s if x[1] in PUT]
        draws.append(len(d))
        deposits.append(len(p))
        for x in d:
            drawn_units.append(x[3])
        # jobs served per draw
        cur = None
        for h, op, item, q in s:
            if op in DRAW:
                if cur is not None:
                    per_draw.append(cur)
                cur = 0
            elif op in SPEND and cur is not None:
                cur += 1
        if cur is not None:
            per_draw.append(cur)
        # latency: first gain -> first put after it
        g = next((h for h, op, _i, _q in s if op in GAIN), None)
        if g is not None:
            b = next((h for h, op, _i, _q in s if op in PUT and h >= g), None)
            if b is not None:
                spans.append(b - g)
    def m(v):
        return f"{statistics.mean(v):.2f}" if v else "-"
    print(f"{label:6s} draws/unit-day {m(draws):>6s}   units per draw {m(drawn_units):>6s}   "
          f"jobs per draw {m(per_draw):>6s}   deposits/unit-day {m(deposits):>6s}   "
          f"gain->bank turns {m(spans):>6s}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", default="3-12")
    ap.add_argument("--team", default="SpaTaro")
    a = ap.parse_args()
    lo, hi = (int(x) for x in a.days.split("-"))
    days = range(lo, hi + 1)
    import scripts.breakdown as B
    reps = sorted({B.TAPES[k][0] for k in B.TAPES if k.startswith("spa")})
    allseq = []
    for rp in reps:
        p = ROOT / rp
        if p.exists():
            allseq.extend(ops_by_unit(json.loads(p.read_text()), a.team, days))
            print(f"  read {p.name}", flush=True)
    print(f"\n{len(allseq)} unit-days, days {lo}-{hi}\n")
    summarise(allseq, "HIS")


if __name__ == "__main__":
    main()
