"""Do the top clones replay カワシギ, and if so, until which day?

Alex, 2026-08-26: *"if they do that much more and different 1 of us is no longer cloning - cos that
sounds a big difference - maybe they only clone d1-12 like us...(?)"*

`data/logs/clones_vs_us.log` shows the top clones doing far more than カワシギ from d12 on -- 371
harvests to his 358, crew to 14.7 where he sits at 12, PLANT 17.5 on d24 against his 6.9. If they
were replaying him all season those numbers would match his. So either they diverge at some point,
or they never cloned him at all and the identical crop mix is convergence rather than copying.

The test is direct. The start state is FIXED -- every game opens on the same board, same $3000, same
NW quadrant (`project_kaggriculture_start_state_is_fixed`) -- so two agents running the same script
emit the same ops on the same turns until something on the board diverges. Per day, this counts the
fraction of turns where a clone seat's op list is EXACTLY kawa's:

    match      identical op sequence for the whole crew that turn
    partial    same multiset of ops, different order or different unit
    differ     neither

A script that replays a tape reads ~1.0 match, then falls off a cliff on the day it stops. Our own
agent is included as a control, because we KNOW it replays the tape d4-d11 and then plans -- so our
curve is what "clones to d12" looks like, and theirs can be read against it.

Compared against kawa seats from a DIFFERENT game, so the opponent and the shop draw differ; that
puts a ceiling below 1.0 even for a true replay, and the ceiling is what our control measures.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
KAWA = "カワシギ"
US = "alex chilton"
NEW = "data/seed_scripts/daily_2026-08-26"
OURS = "data/seed_scripts/ours_2026-08-26"
KAWA_DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
             "kawa_2026-08-24", "leaders_2026-08-24")


def op_stream(replay, seat):
    """`{turn: (ops tuple)}` -- the crew's ops that turn, farmer first."""
    out = {}
    for t, step in enumerate(replay.get("steps") or []):
        if seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        out[t] = tuple(tuple(o) if o else None for o in ops)
    return out


def compare(a, b):
    """Per-day (match, partial, total) between two op streams."""
    per_day = collections.defaultdict(lambda: [0, 0, 0])
    for t in sorted(set(a) & set(b)):
        d = per_day[t // TPD]
        x, y = a[t], b[t]
        d[2] += 1
        if x == y:
            d[0] += 1
        elif collections.Counter(x) == collections.Counter(y):
            d[1] += 1
    return per_day


def herd_of(replay, seat):
    last = (replay["steps"][-1][0] or {}).get("observation") or {}
    farms = last.get("farms") or []
    if seat >= len(farms):
        return None, collections.Counter()
    h = collections.Counter()
    for row in (farms[seat].get("tiles") or []):
        for c in row:
            if isinstance(c, dict) and c.get("animal"):
                h[c["animal"]] += 1
    return float(farms[seat].get("money", 0)), h


def load_kawa():
    out = []
    for d in KAWA_DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:25]:
            try:
                r = json.loads(f.read_text())
            except Exception:                                             # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA in names:
                out.append(op_stream(r, names.index(KAWA)))
            if len(out) >= 8:
                return out
    return out


def curve(label, streams, refs):
    """Best per-day match of each stream against ANY kawa reference, averaged."""
    if not streams:
        print(f"{label}: no seats"); return
    acc = collections.defaultdict(list)
    for s in streams:
        best = None
        for ref in refs:
            per_day = compare(s, ref)
            score = sum(v[0] for v in per_day.values())
            if best is None or score > best[0]:
                best = (score, per_day)
        for d, (m, p, tot) in best[1].items():
            if tot:
                acc[d].append((m / tot, (m + p) / tot))
    print(f"{label}   ({len(streams)} seats)")
    print(f"   {'day':>5}{'exact':>9}{'+same set':>11}")
    for d in sorted(acc):
        v = acc[d]
        print(f"   {d:>5}{100*sum(x[0] for x in v)/len(v):>8.0f}%"
              f"{100*sum(x[1] for x in v)/len(v):>10.0f}%")
    print()


def main():
    refs = load_kawa()
    print(f"kawa reference streams: {len(refs)}\n")

    clones, ours = [], []
    for f in sorted(pathlib.Path(NEW).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        for seat in range(min(2, len(names))):
            money, herd = herd_of(r, seat)
            if money is None or money < 125_000:
                continue
            cow, sheep = herd.get("COW", 0), herd.get("SHEEP", 0)
            if (cow >= 10 and sheep == 4) or (sheep >= 9 and cow <= 7):
                clones.append(op_stream(r, seat))
    for f in sorted(pathlib.Path(OURS).glob("[0-9]*.json"))[:12]:
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        ours.append(op_stream(r, names.index(US) if US in names else 0))

    curve("TOP CLONES vs kawa", clones, refs)
    curve("OURS vs kawa  (control: we replay the tape d4-d11)", ours, refs)


if __name__ == "__main__":
    main()
