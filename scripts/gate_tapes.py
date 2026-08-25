"""Play our agent against REAL leaders, replayed from their own recordings.

The reason this exists: `gate_pool.py` is saturated. Every member of that pool is
`heuristic.make_agent` with different dials -- same routing, same hiring, same sell cadence -- so it
varies crop mix and nothing else. Measured 2026-08-25 it returned 95.0% for two different herd rules
with nine of ten opponents pinned at 100%, which is the gate saying it cannot answer, not that the
arms are equal.

A recorded leader differs in HOW it plays, which is the axis that decides ladder games.

Three things this harness must pin, all of them learned the hard way and all recorded in
`breakdown.py`:

  * `env_config`     -- the economy the tape was played on. `townCenterSellInterval` moved 12 -> 24
                        at env 1.32.6; a tape recorded at 12 and replayed at 24 sells differently
                        and its board diverges by day 6.
  * `recorded_shops` -- the shop draw, read off the recording rather than derived from a seed. The
                        draw depends on how the board was played, because `_end_of_day` spends the
                        same generator on `_spawn_weeds` first. Without it, four real games missed
                        their recorded banks by up to 2x.
  * the seat          -- `tape_policy(replay, team, 0)` is the NAMED team's action stream.
                        `..., 1)` is that team's OPPONENT. Reading the wrong one is the
                        `farms[1] is not the tape` trap and has cost three wrong diagnoses.

LIMITATION, stated up front: a replayed tape is OPEN-LOOP. Its actions were chosen against its own
real opponent and cannot react to us. That matters least here of anywhere, because the winners on
this ladder submit fixed 720-turn schedules rather than policies -- an open-loop replay is close to
what these agents already are -- but it is not a live opponent and must not be described as one.

SEATING: our agent always takes seat 0, because `kaggle-environments` gives `step` only to seat 0
and an agent seated second replays turn 0 all season and banks nothing
(`project_kaggriculture_seat1_has_no_step`). Seat 0 also carries a real edge -- identical mirrored
agents score about 54/46, not 50/50, because seat 0 holds earlier market order slots. **So 54% is
the break-even line for this gate, not 50%.**

    python -u scripts/gate_tapes.py --agent submission/main.py --games 40
"""

import argparse
import collections
import importlib.util
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.breakdown import env_config, recorded_shops, tape_policy  # noqa: E402

#: Where downloaded leader games live. These are real ladder recordings, not generated games.
TAPE_DIRS = ("data/seed_scripts/top_guys", "data/seed_scripts/leaders_2026-08-24",
             "data/seed_scripts/leaders_2026-08-19", "data/seed_scripts/field_leaders",
             "data/seed_scripts/downloads_2026-08-21")

#: `weedSpawnChance` on the ladder. NOT 0 -- `project_kaggriculture_start_state_is_fixed`.
LADDER_WEEDS = 0.005


def _final_money(replay):
    """Both seats' banks at the last recorded step, as the recording has them."""
    last = replay["steps"][-1]
    out = []
    for seat in range(2):
        obs = (last[seat] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if seat < len(farms):
            out.append(float(farms[seat].get("money", 0.0)))
        else:
            out.append(0.0)
    if out == [0.0, 0.0]:
        # Only seat 0 carries the full observation in some recordings.
        obs = (last[0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        out = [float(f.get("money", 0.0)) for f in farms[:2]] or [0.0, 0.0]
    return out


def _pick_leader(replay):
    """The team that WON the recorded game, by final bank. That is the tape worth playing."""
    names = (replay.get("info") or {}).get("TeamNames") or []
    if len(names) < 2:
        return None
    money = _final_money(replay)
    return names[0] if money[0] >= money[1] else names[1]


def _load_agent(path):
    """Import a built `submission/main.py` and return its entry point."""
    path = pathlib.Path(path)
    spec = importlib.util.spec_from_file_location("_gate_agent_%d" % abs(hash(str(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("agent", "act", "main"):
        fn = getattr(mod, name, None)
        if callable(fn):
            return fn
    raise RuntimeError(f"no entry point in {path}")


def play(agent_path, replay_path, weeds=LADDER_WEEDS, team=None):
    """One game: our agent at seat 0 against the recorded leader at seat 1."""
    from kaggle_environments import make

    replay = json.loads(pathlib.Path(replay_path).read_text())
    leader = team if team else _pick_leader(replay)
    if leader is None or leader not in ((replay.get("info") or {}).get("TeamNames") or []):
        return None

    cfg = dict(env_config(replay_path))
    cfg["weedSpawnChance"] = weeds
    seed = (replay.get("info") or {}).get("seed")
    if seed is not None:
        cfg["seed"] = seed

    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)

    shops = recorded_shops(replay_path)
    ours = _load_agent(agent_path)
    theirs = tape_policy(replay_path, leader, 0)

    # The recorded shop list replaces whatever the live env drew, on every turn, for both seats.
    for t in range(len(env.steps), 720 + 1):
        for state in env.state:
            town = (state.observation or {}).get("town")
            if town is not None:
                town["unlocked_shops"] = list(shops(t))
        if env.done:
            break
        obs0 = env.state[0].observation
        obs1 = env.state[1].observation
        try:
            a0 = ours(obs0, env.configuration)
        except TypeError:
            a0 = ours(obs0)
        a1 = theirs(obs1, t - 1)
        env.step([a0, a1])

    farms = (env.state[0].observation or {}).get("farms") or []
    banks = [float(f.get("money", 0.0)) for f in farms[:2]]
    if len(banks) < 2:
        return None
    # Livestock stands ON A TILE as `tile["animal"]`. A farm has no `animals` key -- assuming one
    # returned None everywhere and reported 0 seats at 6/6 out of 3,224 on 2026-08-25.
    herds = []
    for f in farms[:2]:
        c = collections.Counter()
        for row in (f.get("tiles") or []):
            for t in row:
                if isinstance(t, dict) and t.get("animal"):
                    c[t["animal"]] += 1
        herds.append((c.get("COW", 0), c.get("SHEEP", 0)))
    return {"replay": pathlib.Path(replay_path).stem, "leader": leader,
            "ours": banks[0], "theirs": banks[1], "win": banks[0] > banks[1],
            "draw": banks[0] == banks[1],
            "our_herd": herds[0], "their_herd": herds[1]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="submission/main.py")
    ap.add_argument("--games", type=int, default=40)
    ap.add_argument("--weeds", type=float, default=LADDER_WEEDS)
    # **Without this the opponent is whoever WON each recorded game.** On `top_guys` that is Seb,
    # Sophie and "alex chilton" -- our own past ladder seats -- which is not a leader test at all.
    ap.add_argument("--team", default=None,
                    help="only play tapes containing this team, and seat THEM as the opponent")
    ap.add_argument("--dirs", default=None,
                    help="comma-separated dirs under data/seed_scripts, overriding TAPE_DIRS")
    args = ap.parse_args()

    dirs = ([("data/seed_scripts/" + d.strip()) for d in args.dirs.split(",")]
            if args.dirs else list(TAPE_DIRS))
    files = []
    for d in dirs:
        p = REPO / d
        if p.exists():
            files.extend(sorted(p.glob("*.json")))
    if args.team:
        kept = []
        for f in files:
            try:
                names = (json.loads(f.read_text()).get("info") or {}).get("TeamNames") or []
            except Exception:  # noqa: BLE001
                continue
            if args.team in names:
                kept.append(f)
        print(f"tapes containing {args.team!r}: {len(kept)} of {len(files)}", flush=True)
        files = kept
    # Deterministic order, so two arms see the SAME tapes. Never shuffle without a fixed seed.
    files = files[:args.games]
    print(f"tapes: {len(files)}   agent: {args.agent}   weeds: {args.weeds}", flush=True)

    rows, errs = [], collections.Counter()
    for f in files:
        try:
            r = play(args.agent, f, args.weeds, args.team)
        except Exception as e:  # noqa: BLE001
            errs[type(e).__name__] += 1
            print(f"  {f.stem:<12} ERROR {type(e).__name__}: {e}", flush=True)
            continue
        if r is None:
            errs["unreadable"] += 1
            continue
        rows.append(r)
        mark = "W" if r["win"] else ("D" if r["draw"] else "L")
        oh = "%d/%d=%d" % (r["our_herd"][0], r["our_herd"][1], sum(r["our_herd"]))
        th = "%d/%d=%d" % (r["their_herd"][0], r["their_herd"][1], sum(r["their_herd"]))
        print(f"  {r['replay']:<12} {mark}  ours {r['ours']:>10,.0f} {oh:>9}   "
              f"{r['leader'][:14]:<14} {r['theirs']:>10,.0f} {th:>9}", flush=True)

    if not rows:
        print("no games played", flush=True)
        return
    w = sum(1 for r in rows if r["win"])
    d = sum(1 for r in rows if r["draw"])
    print(flush=True)
    print(f"games {len(rows)}   W {w}   D {d}   L {len(rows) - w - d}", flush=True)
    print(f"win rate {100.0 * (w + 0.5 * d) / len(rows):.1f}%   "
          f"(seat-0 break-even is ~54%, not 50%)", flush=True)
    print(f"mean ours {sum(r['ours'] for r in rows) / len(rows):,.0f}   "
          f"mean theirs {sum(r['theirs'] for r in rows) / len(rows):,.0f}", flush=True)
    if errs:
        print(f"errors {dict(errs)}", flush=True)


if __name__ == "__main__":
    main()
