"""Is the release rule a PRICE THRESHOLD? Prices he sells at, against prices he passes up.

His season sell totals are fixed to the unit and only the hour moves, so something decides "now".
The simplest algo that fits is a threshold: hold the planned quantity until the quote clears a bar.
If that is what it is, the LOWEST price he ever sells a product at sits well above the lowest price
the book offered him while he was holding it -- and the gap is the bar.

Compares, per product per episode, the price at his SELL turns against the price at turns he did not
sell, restricted to after his first sale of that product (before that he may simply have no stock).

    python -u scripts/sell_threshold.py mtmr_s1
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def episodes_of(team, limit):
    seen, out = set(), []
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            if team in r["teams"] and (ROOT / d / f"{r['episode']}.json").exists():
                out.append((ROOT / d / f"{r['episode']}.json", r["teams"].index(team)))
            if len(out) >= limit:
                return out
    return out


def main():
    team = sys.argv[1] if len(sys.argv) > 1 else "mtmr_s1"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    agg = collections.defaultdict(lambda: {"sold": [], "held": []})
    eps = episodes_of(team, limit)
    for path, seat in eps:
        rep = json.loads(path.read_text())
        prices, sold_at = collections.defaultdict(dict), collections.defaultdict(set)
        for t, step in enumerate(rep.get("steps") or []):
            cell = (step[seat] if seat < len(step) else None) or {}
            for k, v in ((cell.get("observation") or {}).get("market") or {}).get("prices", {}).items():
                prices[k][t] = v
            for o in (cell.get("action") or {}).get("market") or []:
                if o and o[0] == "SELL":
                    sold_at[o[1]].add(t)
        for prod, series in prices.items():
            ts = sold_at.get(prod) or set()
            if not ts:
                continue
            start = min(ts)
            for t, p in series.items():
                if t < start or p is None:
                    continue
                agg[prod]["sold" if t in ts else "held"].append(p)
    print(f"{team}: {len(eps)} episodes\n")
    print(f"{'product':12}{'n sold':>8}{'n held':>8}{'min sold':>10}{'min held':>10}"
          f"{'mean sold':>11}{'mean held':>11}{'p10 sold':>10}")
    for prod in sorted(agg):
        s, h = agg[prod]["sold"], agg[prod]["held"]
        if not s or not h:
            continue
        p10 = sorted(s)[max(0, int(0.10 * len(s)) - 1)]
        print(f"{prod:12}{len(s):>8}{len(h):>8}{min(s):>10.0f}{min(h):>10.0f}"
              f"{statistics.mean(s):>11.1f}{statistics.mean(h):>11.1f}{p10:>10.0f}")


if __name__ == "__main__":
    main()
