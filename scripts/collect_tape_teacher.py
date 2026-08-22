"""Record the shipped agent's own trajectory, once per latch key, as BC/DAgger training data.

    .venv/bin/python -u scripts/collect_tape_teacher.py --out data/il/tape_teacher

**The teacher is `make_agent` as it ships, not the raw recordings.** The agent is the submission
candidate: it selects which of the four tapes to replay from the melon and yarn-store latches,
re-labels `BUY_ANIMAL`/`PICKUP`/`PLACE` species from `state["herd_split"]`, and trims `BUY_SEED`
counts on the melon arm. Cloning the tapes directly would clone something we do not run.

**Why no rollout loop and no jax adapter.** `weed_chance` is 0 by default and random weeds land only
on EMPTY tiles (`reference/kaggriculture.py:_spawn_weeds`), so with weeds off the board is fully
determined by our own actions and the teacher's single trajectory IS the dataset. Nothing has to be
corrected because nothing can diverge. That is stage 1; DAgger's corrective rounds only earn their
place once weeds are switched on and the student can reach a board the tape never saw.

There is no jax-state to observation bridge in this repo -- the parity gate drives both sims from
one action stream and never converts between them -- so collecting here in the REFERENCE env avoids
writing one. Slow, and it only has to happen four times. Alex: *"the tape agent will also work as a
teacher just slowly."*

**One seat per tape, against that tape's own opponent and seed**, so each latch arms exactly as it
does in the game the recording came from. Forcing the latch by hand would record a season the agent
never actually plays.

Measured on the four recordings before writing this, so the size of the job is known:

    steps compared          719
    identical on all 4      146   (20.3%)
    first divergence        step 72  =  d3 h0, the melon latch day
    distinct full actions   2225
    distinct market bundles  584   (49.5% of turns are empty market)

Four genuinely different plans sharing a 72-step opening, ~2,880 labelled turns in total. Small, and
because weeds are off the target is EXACT -- "did it learn" is a byte comparison, not a metric. That
matters here: `docs/` records that a 0.788 bundle-agreement score was meaningless because an
untrained network scores it too.
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
STEPS = 720


def _opponent(tape_path, team):
    """The recording's real opponent, replayed. Its seat is whichever one is not the team's."""
    d = json.loads((REPO / tape_path).read_text())
    seat = d["info"]["TeamNames"].index(team)
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]
    return seat, acts, dict(d.get("configuration") or {})


def collect(key, tape_path, team, out_dir):
    """Play one season and record `(step, observation, action)` for our seat every turn."""
    import breakdown as B                                                     # noqa: PLC0415
    from kaggle_environments import make                                      # noqa: PLC0415

    from kagg.search import schedule_agent as SA                              # noqa: PLC0415

    seat, opp, cfg = _opponent(tape_path, team)
    cfg.pop("steps", None)
    cfg["weedSpawnChance"] = 0.0          # stage 1: nothing may diverge
    thin, _economy = _plan()

    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    agent = SA.make_agent(thin, seat, router=True)

    rows, ops = [], collections.Counter()
    for t in range(STEPS):
        if env.done:
            break
        obs = env.state[seat].observation
        act = agent(obs)
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        mine = {"farmer": list(act["farmer"]),
                "hands": [list(h) for h in list(act["hands"])[:n[seat]]],
                "market": [list(o) for o in (act.get("market") or [])]}
        rows.append({"step": t, "obs": _thin_obs(obs, seat), "action": mine})
        ops[mine["farmer"][0] if mine["farmer"] else "PASS"] += 1
        theirs = opp[t] if t < len(opp) else {"farmer": ["PASS"], "hands": [], "market": []}
        pair = [None, None]
        pair[seat] = mine
        pair[1 - seat] = {"farmer": theirs.get("farmer") or ["PASS"],
                          "hands": list(theirs.get("hands") or [])[:n[1 - seat]],
                          "market": theirs.get("market") or []}
        env.step(pair)

    bank = int(((env.state[seat].observation.get("farms") or [{}])[seat] or {}).get("money", 0) or 0)
    name = "%s_%s.jsonl" % (int(key[0]), int(key[1]))
    path = out_dir / name
    with open(path, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return {"key": list(key), "tape": tape_path, "team": team, "seat": seat,
            "turns": len(rows), "bank": bank, "file": name,
            "farmer_ops": dict(ops.most_common(8))}


def _thin_obs(obs, seat):
    """Only what a policy could legally condition on: our farm, our private state, the town, both
    banks. Dropping the opponent's private state matters -- a teacher that sees it teaches a
    student to depend on something the real environment never provides."""
    farms = obs.get("farms") or []
    return {
        "step": int(obs.get("step", 0) or 0),
        "day": int(obs.get("day", 0) or 0),
        "hour": int(obs.get("hour", 0) or 0),
        "mine": farms[seat] if len(farms) > seat else {},
        "their_money": int((farms[1 - seat] or {}).get("money", 0) or 0) if len(farms) > 1 else 0,
        "private": obs.get("private") or {},
        "town": obs.get("town") or {},
    }


def _plan():
    import breakdown as B                                                     # noqa: PLC0415
    _, base_schedule, _ = B.TAPES["kawashigi"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(base_schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    return thin, B.env_config(B.TAPES["kawashigi"][0])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="data/il/tape_teacher")
    args = ap.parse_args()

    from kagg.search import schedule_agent as SA
    out_dir = REPO / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    print("teacher = kagg.search.schedule_agent.make_agent as shipped")
    print("weeds   = 0   (stage 1: the board cannot diverge, so one trajectory is the dataset)")
    print("out     = %s\n" % out_dir, flush=True)

    meta = []
    for key, (tape_path, team) in sorted(SA.REPLAY_OPENING_TAPE.items()):
        print("collecting %-16s %s" % (str(key), tape_path.split("/")[-1]), flush=True)
        info = collect(key, tape_path, team, out_dir)
        meta.append(info)
        print("   seat %d  turns %d  bank %d  ops %s"
              % (info["seat"], info["turns"], info["bank"], info["farmer_ops"]), flush=True)

    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    total = sum(m["turns"] for m in meta)
    print("\n%d turns over %d trajectories -> %s" % (total, len(meta), out_dir))


if __name__ == "__main__":
    main()
