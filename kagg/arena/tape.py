"""Task #55: real leaderboard agents as opponents, replayed from their recorded action streams.

**Why the synthetic pool had to go.** `kagg/arena/pool.py` builds eight of its nine members from
`heuristic.make_agent({**BASELINE, **spec})` -- same routing, same hiring, same sell cadence, only
the crop dials differ. It tests robustness to crop mix and nothing else, and we now beat it 94.4%
with the shipped agent and 100% with the ad-hoc trio. A gate that cannot lose cannot rank anything,
which is why `LATE_SELL_BIAS` has no measurable effect in either direction: the pool is saturated,
not the flag inert.

**Why fidelity is the wrong requirement.** Kaggle publishes `configuration.seed` as `null`, so a
recorded game cannot be reproduced. Measured 2026-08-09, replaying both recorded seats of
`90976060` under the same env version it was recorded on:

    recorded p0  $128,518    replayed  $50,071    61.0% off
    recorded p1   $70,886    replayed  $84,562    19.3% off

That is not a bug to fix. The day-0 board *is* deterministic -- 25 open tiles, 75 LOCKED, identical
every seed -- so the tape's plants land where they landed. What the seed decides is the weed spawn
sequence and the **shop unlock order**, and unlock order swings the season's wheat drain between 390
and 660, repricing every sale. The tape still plays a competent, legal season; it just banks a
different number than it did on the day.

For an Elo gate that is *sufficient*, because both players share one board. We are not asking "did
this game reproduce", we are asking "who won". Re-seeding turns one fixed matchup into a
distribution, which is the randomness the pool never had.

**What a tape is and is not.** It is open-loop: it cannot see our farm, so it will not contest a
market it did not expect to be contested, and it will not punish us for anything specific. It is a
strong fixed schedule, not an adversary. Beating a field of tapes is necessary, not sufficient.
"""

import json
import pathlib
import random


#: Recorded seats are truncated to the units a farm actually owns. The reference ignores a surplus
#: unit action for movement and work, but still *counts* it in the atomic-PLANT rule, so feeding it
#: more hand actions than we own blocks plants no real agent could block. This cost the parity
#: harness a full day; see CLAUDE.md, "check that a harness sends what an agent would send".
_PASS = ["PASS"]


def _stream(steps, seat):
    """Pull one seat's per-turn action stream out of a downloaded replay."""
    out = []
    for step in steps:
        s = (step[seat] or {}) if seat < len(step) else {}
        a = s.get("action") or {}
        out.append((a.get("farmer") or list(_PASS),
                    list(a.get("hands") or []),
                    list(a.get("market") or [])))
    return out


def load_tape(path, seat):
    """Read a replay from disk and return `(stream, team_name, env_version_hint)`.

    `env_version_hint` is `townCenterSellInterval`, which is 12 on kaggle-environments 1.32.2 and 24
    on 1.32.6. It is the one line that distinguishes the two economies and it invalidated a full day
    of tuning once already -- see `project_kaggriculture_ladder_is_1326`. Callers should refuse a
    tape whose economy does not match the one they are measuring in.
    """
    d = json.loads(pathlib.Path(path).read_text())
    names = (d.get("info") or {}).get("TeamNames") or ["?", "?"]
    tcsi = (d.get("configuration") or {}).get("townCenterSellInterval")
    return _stream(d["steps"][1:], seat), names[seat] if seat < len(names) else "?", tcsi


def _jitter_market(market, rng, drop, scale):
    """Perturb the MARKET stream only, and never the farm.

    `farmer` and `hands` are board-dependent -- a walk is a sequence of steps to a specific tile and
    a PLANT is legal only on tilled, unplanted ground. Perturbing either produces an illegal or
    self-harming season and measures our agent against a cripple. Market orders are the opposite:
    quantity and timing are free parameters that the env validates against inventory anyway, so an
    order that has become nonsense is clipped rather than fatal.

    Two knobs, both applied per order: `drop` is the chance the order is skipped entirely, `scale`
    the fractional range its quantity is multiplied by. Quantities floor at 1 so a scaled-down order
    stays an order rather than silently becoming a skip -- otherwise `scale` would smuggle in extra
    dropping and the two knobs would not be separable.
    """
    out = []
    for o in market:
        if not o:
            continue
        if rng.random() < drop:
            continue
        o = list(o)
        if scale and len(o) >= 3 and isinstance(o[2], (int, float)):
            o[2] = max(1, int(round(o[2] * rng.uniform(1.0 - scale, 1.0 + scale))))
        out.append(o)
    return out


def build_tape_agent(path, seat, jitter_seed=None, drop=0.0, scale=0.0):
    """Return a fresh replay agent. **Call this through `AgentFactory`, never directly into
    `run_arena`** -- the turn counter below is exactly the per-match state that `run_arena` used to
    carry between games, at a cost of 17.8x (`docs/arena_state_leak_2026-08-09.md`).

    The counter runs off the agent's own invocation count rather than `obs["step"]`, because a tape
    is open-loop and must stay in lockstep with its recording even if the env's step numbering and
    our call count ever diverge. If the stream runs out the agent passes rather than wrapping.
    """
    stream, _name, _tcsi = load_tape(path, seat)
    rng = random.Random(jitter_seed) if jitter_seed is not None else None
    state = {"t": 0}

    def agent(obs, config=None):
        t = state["t"]
        state["t"] = t + 1
        if t >= len(stream):
            return {"farmer": list(_PASS), "hands": [], "market": []}
        farmer, hands, market = stream[t]

        farms = (obs.get("farms") if isinstance(obs, dict) else getattr(obs, "farms", None)) or []
        me = (obs.get("player") if isinstance(obs, dict) else getattr(obs, "player", seat))
        n = 0
        if me is not None and me < len(farms):
            n = len(farms[me].get("hands") or [])

        if rng is not None:
            market = _jitter_market(market, rng, drop, scale)
        return {"farmer": list(farmer), "hands": [list(h) for h in hands[:n]],
                "market": [list(o) for o in market]}

    return agent
