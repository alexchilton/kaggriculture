"""Clip a turn's BUY_PRODUCT so the tape's own later HIREs stay affordable.

Live loss, episode 108326043 (us 39,385 v Taeyang 54,604), same farm tape on both seats:

    step  0  we buy 43 wheat (BUY 13 + BUY 30), they buy 23      -> we are $447 down
    step 23  day 0 closes: us $0, them $67
    step 24  both issue HIRE x3. The ladder is 1+1+2 = $4.
             `_do_hire` returns silently when the bank is short, so we hired NONE.
    day 1    no hands at all -> 1 FEED against their 4 -> two animals starve and escape
    season   herd caps at 7 against their 17

The tape is a plan, not a budget. `_do_buy_product` re-checks the bank per unit and will happily
spend the last dollar, and the engine gives no failure signal for the hire that is then refused.

So: before emitting, look ahead over the rest of the day at the HIREs this tape schedules, price
them on the fibonacci ladder from the CURRENT `hires_today`, and trim this turn's BUY_PRODUCT
quantities until that much cash survives. Sells are untouched (they only raise the bank), and the
reserve is tiny -- seven hires cost $33 at mult 1 -- so this can only ever clip a purchase that
would have zeroed the bank.

    python -u scripts/build_bankguard.py submission/v38_ours/main.py submission/bankguard/main.py
"""
import pathlib, sys

HOOK = '''

def _hire_ladder(start, n, mult):
    """Cost of `n` further hires today when `start` have already been made."""
    a, b, tot = 1, 1, 0
    for i in range(start + n):
        if i >= start:
            tot += a * mult
        a, b = b, a + b
    return tot


def _reserve_for_hires(action, observation, routes, route, step, cfg):
    """Trim this turn's BUY_PRODUCT so the rest of today's scheduled HIREs can still be paid.

    Measured on episode 108326043: the opening bought 43 wheat, closed day 0 on exactly $0, and
    three $4 hires at step 24 were refused in silence. The farm then ran a whole day with no hands.
    """
    try:
        seat = int(_get(observation, "player", 0))
        farm = (_get(observation, "farms") or [])[seat]
        money = float(_get(farm, "money", 0) or 0)
        hires_today = int(_get(farm, "hires_today", 0) or 0)
        turns = int(cfg.get("turns_per_day", 24))
        mult = float(_get(_get(observation, "configuration", {}) or {},
                          "farmHandCostMult", 1) or 1)
    except Exception:
        return action
    buys = [o for o in (action.get("market") or [])
            if o and o[0] == "BUY_PRODUCT" and len(o) >= 3]
    if not buys:
        return action
    # HIREs the tape still plans today, from the next step to the day's end
    end = (step // turns + 1) * turns
    planned = 0
    tape = routes.get(route) or []
    for t in range(step, min(end, len(tape))):
        act = tape[t]
        if isinstance(act, dict):
            planned += sum(1 for o in (act.get("market") or [])
                           if o and o[0] == "HIRE")
    if planned <= 0:
        return action
    need = _hire_ladder(hires_today, planned, mult)
    # What this turn's own SELLs will raise is NOT counted: they settle in slot order and a
    # BUY above them spends first. Reserving against the bank we can see is the safe side.
    prices = _get(_get(observation, "market", {}) or {}, "prices", {}) or {}
    spend = sum(float(prices.get(o[1], 0) or 0) * int(o[2]) for o in buys)
    over = spend - max(0.0, money - need)
    if over <= 0:
        return action
    # Trim the DEAREST-per-unit buys last: feed wheat is what the herd eats, so shrink the
    # speculative bulk first. Orders are trimmed, never dropped, so slot order is preserved.
    for o in sorted(buys, key=lambda x: -int(x[2])):
        if over <= 0:
            break
        px = float(prices.get(o[1], 0) or 0)
        if px <= 0:
            continue
        cut = min(int(o[2]), int(over // px) + 1)
        o[2] = int(o[2]) - cut
        over -= cut * px
    action["market"] = [o for o in (action.get("market") or [])
                        if not (o and o[0] == "BUY_PRODUCT" and len(o) >= 3 and int(o[2]) <= 0)]
    return action
'''


def main():
    src_p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "submission/v38_ours/main.py")
    out_p = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "submission/bankguard/main.py")
    src = src_p.read_text()

    anchor = "_RELEASE_PARENT=agent"
    assert anchor in src, "release wrapper not found"
    wrapper = '''
_BANKGUARD_PARENT=agent
del agent

def agent(observation,configuration=None):
    action=_BANKGUARD_PARENT(observation,configuration)
    try:
        chassis=_IMPL.chassis
        state=chassis.state_for(observation) if hasattr(chassis,"state_for") else None
        route=(state or {}).get("route",0) if isinstance(state,dict) else 0
        action=_reserve_for_hires(action,observation,chassis.routes,route,
                                  _step_of(observation),chassis.cfg)
    except Exception:
        pass
    return action

'''
    src = src.replace(anchor, HOOK.strip("\n") + "\n" + wrapper + anchor, 1)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(src)
    import ast
    ast.parse(out_p.read_bytes())
    print(f"wrote {out_p}  {out_p.stat().st_size:,} bytes, parses OK")


if __name__ == "__main__":
    main()
