"""Grade d28-d29 against the REAL price book, by replaying both seats verbatim until the close.

## Why a plain rematch cannot answer this

`rematch_the_losses.py` pins the game's own seed and still gets a different market, because prices
here are endogenous: they are set by what the two players sold into the book all season. On game
98428765 the recorded book paid **$270** for milk at the close; our rematch of the same seed paid
**$1**. Alex, 2026-08-24: *"dude you have to replay it in the same seed or shops -- otherwise is
stupido"*. He is right. A last-day pricing change cannot be tested in a world where the price is
different.

## What this does instead

Both seats are driven from their RECORDED actions from turn 0 up to the handover turn, so the board,
the shed, the bank and -- the point -- the town's book are the real ones. From the handover the
chosen seat switches to the live agent and plays the rest itself. The opponent stays on its tape
throughout, so the only thing that differs between two runs of this script is our own code.

`--handover 28` starts us at d28 h0, which is the window Alex asked for: *"last 2 days"*.

Replaying from turn 0 is deliberate and not an accident of convenience. Hand ops are
position-dependent -- `["FEED"]` applies wherever that unit happens to stand -- so splicing a tape
in at day 4 puts every op on the wrong tile and the farm collapses. See the note at the top of
`scripts/handover.py` and `docs/the_shed_destroys_the_harvest_2026-08-08.md`.

**Known imprecision, stated up front:** weed spawning draws from the env RNG, so a long replay can
drift a tile or two from the recording even on the right seed. The control run below is what makes
that harmless -- it is measured in the same drifted world as the treatment.

## What it prints

A control and a treatment, in one process, on the same replayed prefix:

    control    the tape plays the close too -- i.e. what the submission actually did
    treatment  our live agent plays the close

and for each: final bank, what reached the shed in the last two days, and what was left standing
priced at the town's closing quote.

    python -u scripts/the_close_on_the_real_book.py 98428765 --handover 28
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
US = "alex chilton"
ANIMAL_PRODUCT = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}


def _find(episode):
    """The replay file for `episode`, anywhere under `data/seed_scripts/`."""
    hits = list((REPO / "data/seed_scripts").rglob(f"{episode}.json"))
    if not hits:
        sys.exit(f"no replay named {episode}.json under data/seed_scripts/")
    return hits[0]


def _recorded_action(steps, t, seat):
    """Seat's recorded action for turn `t`, or a no-op past the end of the recording."""
    if t + 1 < len(steps):
        a = steps[t + 1][seat].get("action")
        if isinstance(a, dict):
            return a
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _standing(obs, seat):
    """`[(pos, what, units, price, value)]` still on `seat`'s tiles, at the town's live quote."""
    px = (obs.get("market") or {}).get("prices") or {}
    out = []
    for r, row in enumerate(obs["farms"][seat]["tiles"]):
        for c, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            units = tile.get("yield_units") or 0
            if not units:
                continue
            animal = tile.get("animal")
            product = ANIMAL_PRODUCT[animal] if animal else tile.get("crop")
            price = float(px.get(product, 0) or 0)
            out.append(((r, c), animal or tile.get("crop"), units, price, units * price))
    out.sort(key=lambda x: -x[4])
    return out


def play(path, our_seat, seed, handover, live):
    """Replay both tapes to `handover`, then let `live` decide whether we take over.

    Returns `(ours, theirs, standing, book)`.
    """
    from kaggle_environments import make

    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads(pathlib.Path(path).read_text())
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    steps = rec["steps"]
    them = 1 - our_seat

    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, our_seat) if live else None

    # What our seat actually emits in the close. A plan that never reaches the pens and a plan that
    # is empty look identical in the bank; they do not look identical here.
    ops = collections.Counter()
    cut = handover * TPD
    for t in range(30 * TPD):
        o_us = env.state[our_seat].observation
        n_us = len(o_us["farms"][our_seat].get("hands") or [])
        n_them = len(o_us["farms"][them].get("hands") or [])

        if live and t >= cut:
            a = agent(o_us)
            mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                    "market": a["market"]}
        else:
            a = _recorded_action(steps, t, our_seat)
            mine = {"farmer": a.get("farmer") or ["PASS"],
                    "hands": list(a.get("hands") or [])[:n_us],
                    "market": a.get("market") or []}

        a_them = _recorded_action(steps, t, them)
        yours = {"farmer": a_them.get("farmer") or ["PASS"],
                 "hands": list(a_them.get("hands") or [])[:n_them],
                 "market": a_them.get("market") or []}

        if t >= cut:
            for slot in [mine["farmer"]] + list(mine["hands"]):
                if slot:
                    ops[slot[0]] += 1

        env.step([mine, yours] if our_seat == 0 else [yours, mine])
        if env.done:
            break

    obs = env.state[0].observation
    farms = obs["farms"]
    book = (obs.get("market") or {}).get("prices") or {}
    return farms[our_seat]["money"], farms[them]["money"], _standing(obs, our_seat), book, ops


def report(tag, ours, theirs, standing):
    print(f"\n--- {tag} ---")
    print(f"  ours   ${ours:>12,.0f}")
    print(f"  theirs ${theirs:>12,.0f}")
    print(f"  margin ${ours - theirs:>12,.0f}  {'WIN' if ours > theirs else 'loss'}")
    if standing:
        total = sum(x[4] for x in standing)
        print(f"  left standing, priced at the close: ${total:,.0f}")
        for pos, what, units, price, value in standing[:10]:
            print(f"    {str(pos):<8} {what:<11} {units:>3} x ${price:>7,.0f} = ${value:>8,.0f}")
    else:
        print("  left standing: nothing")
    return sum(x[4] for x in standing)


def sweep(dirs, handover, out_path, limit):
    """Run the control/treatment pair over many of OUR games, one CSV row each, flushed.

    A sweep that writes only at the end loses everything when it is killed -- 29,568 planned seasons
    once produced 0 rows here. Header first, then one flushed row per game.
    """
    files = []
    for d in dirs.split(","):
        files += sorted((REPO / "data/seed_scripts" / d.strip()).glob("*.json"))
    print(f"{len(files)} candidate replays from {dirs}", flush=True)

    fh = open(out_path, "w")
    fh.write("episode,seed,seat,quadrants,control_bank,treat_bank,delta,"
             "control_standing,treat_standing,standing_delta\n")
    fh.flush()

    done = 0
    for p in files:
        if done >= limit:
            break
        try:
            rec = json.loads(p.read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if US not in names or len(rec.get("steps") or []) < 700:
            continue
        seat = names.index(US)
        seed = rec["info"].get("seed")
        if seed is None:
            continue
        quads = len(rec["steps"][-1][seat]["observation"]["farms"][seat]
                    .get("unlocked_quadrants") or [])
        try:
            c_ours, _c_them, c_stand, _book, _c_ops = play(p, seat, seed, handover, live=False)
            t_ours, _t_them, t_stand, _b2, _t_ops = play(p, seat, seed, handover, live=True)
        except Exception as e:                                               # noqa: BLE001
            print(f"  {p.stem}: {e!r}", flush=True)
            continue
        cs = sum(x[4] for x in c_stand)
        ts = sum(x[4] for x in t_stand)
        fh.write(f"{p.stem},{seed},{seat},{quads},{c_ours:.0f},{t_ours:.0f},"
                 f"{t_ours - c_ours:.0f},{cs:.0f},{ts:.0f},{ts - cs:.0f}\n")
        fh.flush()
        done += 1
        print(f"  {done:>3} {p.stem}  q{quads}  bank {t_ours - c_ours:>+9,.0f}  "
              f"standing {ts - cs:>+9,.0f}", flush=True)
    fh.close()
    print(f"\n{done} games written to {out_path}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", nargs="?", help="one episode id; omit when using --dirs")
    ap.add_argument("--handover", type=int, default=28,
                    help="day our live agent takes over (28 = the last two days)")
    ap.add_argument("--dirs", help="comma-separated folders under data/seed_scripts to sweep")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--out", default="data/logs/close_sweep.csv")
    a = ap.parse_args()

    if a.dirs:
        sweep(a.dirs, a.handover, REPO / a.out, a.limit)
        return

    path = _find(a.episode)
    rec = json.loads(path.read_text())
    names = rec["info"]["TeamNames"]
    seat = names.index(US)
    seed = rec["info"]["seed"]
    print(f"game {a.episode}  seed {seed}  our seat {seat} ({names[seat]})")
    print(f"both tapes replayed to d{a.handover} h0; our agent plays from there\n")

    rw = rec.get("rewards") or [0, 0]
    print(f"recorded : ours ${rw[seat]:,.0f}  theirs ${rw[1 - seat]:,.0f}  "
          f"margin ${rw[seat] - rw[1 - seat]:,.0f}")

    c_ours, c_them, c_stand, book, c_ops = play(path, seat, seed, a.handover, live=False)
    print(f"\ntown's book at the close: "
          f"{ {k: v for k, v in sorted(book.items())} }")
    control = report("CONTROL  tape plays the close", c_ours, c_them, c_stand)

    t_ours, t_them, t_stand, _, t_ops = play(path, seat, seed, a.handover, live=True)
    treat = report(f"TREATMENT  our agent plays d{a.handover}-d29", t_ours, t_them, t_stand)

    print(f"\n{'':<26}{'bank':>12} {'left standing':>15}")
    print(f"  {'control (the tape)':<24}{c_ours:>12,.0f} {control:>15,.0f}")
    print(f"  {'treatment (our agent)':<24}{t_ours:>12,.0f} {treat:>15,.0f}")
    print(f"  {'delta':<24}{t_ours - c_ours:>12,.0f} {treat - control:>15,.0f}")

    keys = sorted(set(c_ops) | set(t_ops), key=lambda k: -(c_ops[k] + t_ops[k]))
    print(f"\nops issued in the close (d{a.handover}-d29), our seat")
    print(f"  {'op':<22}{'tape':>8}{'ours':>8}")
    for k in keys:
        print(f"  {k:<22}{c_ops[k]:>8}{t_ops[k]:>8}")


if __name__ == "__main__":
    main()
