"""Build v38+our-tapes at a chosen SELL-LEAD HORIZON, so the horizon is the only variable.

v38's `_sell_lead` pulls a sale forward exactly ONE step, and only when no town consumption falls
between the two -- the book is then at the same level either way, so selling early is free and puts
our goods in ahead of the opponent's. tetsutani's build reaches FOUR actions ahead, but it is also a
different chassis, so "v38 beat dynroute 10-2" is not a horizon measurement.

This varies only the reach. The guard is preserved exactly: a sale may be pulled from step `nxt`
only if no drain step (`k % 4 == 0`) falls in `step+1 .. nxt`, and never across a shop-unlock
boundary. Because a drain lands every 4 steps, a larger horizon simply fires less often rather than
selling into a refilled book.

v38 carries one `sell_state` with a single `due_step`, which cannot express a debt owed 3 steps out,
so this adds a per-step debt ledger that survives turns.

    python -u scripts/build_lead_horizon.py 2 3
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "submission/v38_ours/main.py"

NEW_SUPPRESS = '''    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold early.

        Extended from v38's single `due_step` to a per-step ledger: with a horizon above 1 a debt
        can be owed several steps out, and one due_step cannot carry that.
        """
        debts = sell_state.get("debts") or {}
        remaining = dict(debts.pop(step, {}) or {})
        if sell_state.get("due_step") == step:
            for k, v in (sell_state.get("suppress") or {}).items():
                remaining[k] = remaining.get(k, 0) + v
        if not remaining:
            return
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept
'''

NEW_LEAD = '''    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """Pull forward the lots the tape plans to SELL within LEAD_HORIZON steps.

        A target step `nxt` is eligible only when no town consumption falls between now and then --
        `k %% 4 == 0` for any k in step+1..nxt -- so the book is at the same level either way and
        selling early is free. Products WHEAT and FERTILIZER are excluded as in v38: wheat's book
        never fills and fertilizer's never drains, so racing on either gains nothing.
        """
        cfg = self.cfg
        unlock_period = 3 * cfg["turns_per_day"]
        if step %% 4 == 0:
            return
        tape = self.routes[route]
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        debts = next_sup.setdefault("debts", {})
        for offset in range(1, LEAD_HORIZON + 1):
            nxt = step + offset
            if nxt > LAST_ACT_STEP or nxt %% unlock_period == 0:
                break
            if any(k %% 4 == 0 for k in range(step + 1, nxt + 1)):
                break
            future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
            planned = {}
            for o in future.get("market") or []:
                if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                    planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
            for item in PRODUCTS:
                if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                    continue
                qty = min(projected.get(item, 0), planned[item])
                if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                    continue
                if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                    return
                projected[item] -= qty
                debts.setdefault(nxt, {})
                debts[nxt][item] = debts[nxt].get(item, 0) + qty
'''


def build(h):
    src = SRC.read_text()
    lines = src.splitlines()

    def block(start_pat, out):
        i = next(k for k, l in enumerate(lines) if re.match(start_pat, l))
        j = i + 1
        while j < len(lines) and not re.match(r"    (@staticmethod|def )", lines[j]):
            j += 1
        lines[i:j] = out.rstrip("\n").splitlines() + [""]

    block(r"    @staticmethod\n?$" if False else r"    def _sell_lead\(", NEW_LEAD % ())
    i = next(k for k, l in enumerate(lines) if l.startswith("    def _apply_suppression("))
    # include the @staticmethod line above it
    start = i - 1 if lines[i - 1].strip() == "@staticmethod" else i
    j = i + 1
    while j < len(lines) and not re.match(r"    (@staticmethod|def )", lines[j]):
        j += 1
    lines[start:j] = NEW_SUPPRESS.rstrip("\n").splitlines() + [""]

    # carry the ledger across turns and declare the horizon
    out = "\n".join(lines)
    out = out.replace('next_sup = {"due_step": -1, "suppress": {}, '
                      '"r36_debts": st["sell_state"].get("r36_debts", {})}',
                      'next_sup = {"due_step": -1, "suppress": {}, '
                      '"debts": st["sell_state"].get("debts", {}), '
                      '"r36_debts": st["sell_state"].get("r36_debts", {})}', 1)
    out = out.replace('"pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}',
                      '"pending": {}, "sell_state": {"due_step": -1, "suppress": {}, "debts": {}}}', 1)
    out = out.replace("DEFAULT_SETTINGS = {", f"LEAD_HORIZON = {h}\n\nDEFAULT_SETTINGS = {{", 1)
    p = ROOT / f"submission/lead{h}/main.py"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out)
    import ast
    ast.parse(p.read_bytes())
    print(f"lead{h}: {p}  {p.stat().st_size:,} bytes, parses OK")


if __name__ == "__main__":
    for h in (int(x) for x in sys.argv[1:] or ["1", "2", "3", "4"]):
        build(h)
