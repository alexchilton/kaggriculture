# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
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

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent


import base64
import json
import zlib
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_kBvLyCj_}mYb-<f(lL)LPLCD{adxP{dPF}RYhuz;|FaChG>_P^_#?#!ypaC39>$m-$Tm7b>Ou)8WgJR;o9&CUPqoB!>f|J%QO^S}JlzkTz6{`0^7*MIrfFF$_s%ctLd`{s|AZ~n_a|KI<|fBW(eUw-_r|NO82*T4MtFF*g&H-Gv4KmYBQUthob{oBvqynJ)}>-E!@|82TI{`em+`w#i~_1DjT^*`me>yJM^{(S!9<)6O!>kq$PzfphqI*Ly}|M1hNub=Ym>+PGD*8KBtf4yFR`T8G<q5byy`*CPrru@UV|MB-<){px7LF*bk=CS|j_}lx572kCK#rL5czH;|*?7RN*`wu^U_qQ*<^7;3#Q&+z1eNhizR(wi0!5=?;dllwqHo5py{5`kpZ=c_O`1VsUrS&(}Rl9$1x$f42f4g44`|{s^y8ih3Gcb{Iz4!>e%=zcf_fK>FrP!TlNKHAUZDD~afp6P}cKh`C`fK^q+cJ@5{|{eBa`=YFA3r{MTWrZzr76DK!{K}HJL<3X<9CiLl-_h}ZPLQpUwU7^njJoTkhuPj|7OqA;d{5c+RS_XfZg|PS0q^Y?RMFZz!;SFy=J}bcH3nxzdu^$F0ssPzwL4tzx|AL2m8#{{r$JoUtB)$AG7dn{Iz7g<AcVYLOVgQu;2mtzy&26x(*=v+QfoBK3iE(@FbmD(DJKNA51>3_@T-dIxe#3Va9$Ac>cgP#xG1cQ20+3FZN?t>wgnI#lFAyzg_>6@*%H3{&@ZN^WXl%_1Dio{P@HFT3&JYPlCUgad?3r?|kOw85I8v&)piC?0)sjd4F-@9`m?dKb1TDcuGr0Rf(%SFVI_EK2ztb!IYJ|W;=~GxNz@LVS@hmn3b%%R~{epF~bDs_tbdrH_f|kJ$bZ`+u_Vz?VP(4c22(QlW%1eugj^udGbqVcliGwO8&Kf=_A<5T<#&{6u!3<Pl;{JKD{i^W)GL=EJp7#`@ZneM?et!ywEPl0vBQD>E%TTNjN@vHCKlqwVJ?9JU3d&TuC^8ay8GojC8Q!<PqEphP!>>UqAi&pX%@ovdVWWs0qHL<-QO5L>MdY!ww!&g4xhVK55>-={>vwzBA?TH+U&}oOrlL2N6hc%rWq*t-?&`9Srcpa9P<00u+2T3Spnf0@!hejtDs(e<wsD;hJ=5C?fPlSdv8gDVGUwy^-KWE*+E%`k(!-<h}N+??Et;ePFyF>b3z~8JU;YuDKoXV=WGkOx+_H?S+ZXBP<%dbw^9<{>bc;og;o{(`c=I_V$@8JgqV-D?SA*f%o`{EOp&=YaIMyIl&9@T)za(O){B;%g7Bhegw78hNxkcBh=|%#V!u$5p|wNbl$N<aZ}Cw1An{(li-`~;0F4^xPM)R2f@6s$LG5ImGJZBz1bEQBqGVTRXqE^YZJbx#*Op1DrvWF_!AJPv%X!@-}+!TtIE5&pI!;Y2q7}N#(wgq&bunoXwQX7e4n)rbON7O;ut9(1b`qFepUK$xvx2JMYvb>WQW#zB3|00#z8^PIL(-;sTdM`+;^1b)M~E@00s~%0TX$7uKgT#5@lJbDJd?5J%f&g0DjhqWF`SF!50ZQkCJ?4pQjEykHRNrL10SzaVJ)ve9w2kzW$Q+Oh5=Q)WcaE2tAi4ul@S)*qrmg;_WG%zc$JzJD&_b2T^Ydx^!jw4_qzV$HDnH7tfO*!&9ld`ybmSI`5=<j3?=7Ba4i%k<%XE{T{L_Q3dbk!s3|D`j|8~C+F<%9`D~i|N80nm+P;;{%2s@C^Cq?@7%-yIuRt`5<D>rckX7d`SNze_ou`MjPn<-mRf!I{oKLd?{UUQQD>xnm6UG<8~+rL#b@d6jiAnLVbFFZV(D3^e#fnbc`~~V!O04aoim?v1iq@IwpKuw$Cb_`7NMuWo_CkaEUoEd*J08mq)r#(yFZcw={j}5?jP)eL@&@2K(|8f9PZDB>kZ{OWc%xJ{3ATD)@=YQV*gt-{fAHc`uZan2)OAsh<g14Jb+!n6!sFzh@T9~4~6das9$cB@1mO3$6wR;*3S5`^v+ZwKj{7ePA&n?{rdg)68GJtB|v_M1l2O(S@8%hOPvko?k<7KSrB2j0;B%T91q5mA=y8m00(>W8BSt(QDerpEVEQ{bV#E39KHQN*=420qkFq+gk=NwkHYO>rO$2!$crAR*nxsqp=9I>?g=V51tvJ`cKGw_PoF-&N{9`>?P(q(tVfN@Xy82QVU8|BwEe~1Cq@e|nC<ZbUr%eSESlurr_71bOQ`IX?H2R6{x}+4MfCs(sp(asc{0aK+CQqDO5zL*)7e2r@FB;1=bz?+Kvu6wV_2OQR3eUxa{@Z^taOPh2i!e~xl(hITXoCbD%)_AX~r|Z$>#DNQzhlmLG}YyIEbHq`0+n}S+2|FvfE+mzB0hOmJGZ9feq~4^qMv!LQo8Ma#UdUPe5=h5&fFI`}O7F{Pp!Kt>p4Y4Z3dJZW|gh=P+h5=ua$4o|1J-Ve1zC-d$Z+?hfRG(Bf4OeR%*_V$c1Nhe2o*{fjt>X*Vy#<ZB~I>qCcYYS62~{>kOi)zRRc6}17Nlx*7%X!#?P54qc)ed+x7%|2@Z?~<*_!|aLx?h$Faq{7g>L+?;<B5g>a6s78@K7a%Qy6rX&e?icA0@HTmF8Xw%@lh$P*p*=M&GwMK3%QJ<qXbr%9=!LPAC<<r74%vbmaQa@F3O9y05y`eA1p#bBPw2k{C=&DPgC#OqG7outPwI%cTkC#PMjG9!@ntsqfL|R>w_bS+^KQ8&tuOZb2Z5(@`XA9QjrD$c?p#KWm|Jfg@WOX;GfbjJM>JFcmdF4B;g_<zWWL{Vr@`5L<BU<KryR)>cFAml&v#K%$hPuP3`kQ_oA6bv3zE4SPrxu5eE+OJ9{?4f4m<$A1$wBuyE9UKW2b`+oes7;_j`XuYRO}*9ZRn$sDBshwSS5@)8YNFHJZ`DM0Hwc5z15CR+h^Z`5hs@aXZ!Hq($IHAcRFgyP#I<zwunAEhR5jsTJJ`rD(#iTn(z4D-=BpOYna!O1A7Sv;iKd?W$tu;DH62uvN;V=q}IflIX25xf9504$OP2jU1ll`zcLCg?OrI}30(1j@B^tOTILcfY3PT%SY~i)6x3f)cr8{E)iPtnv(S-=f7UanPF8vxj6)LGWp*qQ@9i=xu0y8QhM4)EC8p-E#{$5DxdOV__LDc#AP_^ZuXTx8oVA!@fpsvBN|b+Oq{U$Qrx^x`LfihAKO~!hdA;2?85U8w->n62Y*Lp{{a%aTd~jdpSElTnaL(P)r;;g^3lBSjFfk#J<T&0}S<v&yS$>CPWNly6#I<|AcnSh#-+n#u_m-Nou4$cfvqgMpiBpx|*)*Spi|WJ_-1zHlVk=5(jXBh6XIBj^esV^qI$QN7kvll*A#maZeO*TBtG^tSO@bQ7v|u@2*&JNhV|74bANSNC*gpWzaemPq#{Pyg^ud<bn5Gg_IlJ`$x<IZG;JDsnA%~rdWy@)ICJhVM#)aD*^fOuD#)F*3_nn6U2ntMkQ>SV=#s1{VE`XL;_ZG`7(3xujcWOD)WrqhP2?8`aX!uWw9(kGkW}!$i;RE!=12-_)%aUL57~4w=#|18nKzcVpgFmC|{>?7-)8kQj|joSi&^%L4t*FDyx79PsTKDKYc0Ya~X0K)7Jvq_pN&G7cdtp7gYNhTW+#a`yV~Noa4M<I?J2EOH#rUe?lE=MJ_m0XAO>2rnignn}YV1-@m^8c9kSO6os|$C!lSo7m&i27u6m8y=DV$A_basb6t$tsE&zXT`mdkeGyN{c;RAdR)xYJn6QeL)FulGL%G`LC`aP`E`Az-3`&&x?-HfDPHN{$_`julDMZ;d8YGm1ELPw!*p_SU^SZg@XmLf8g<OJ;VS5T}S!Td4j?tIM>N&DGcrCvkpX`(lngP=VLVrL%1W4J7rSe-tNWWNq_(Sh3ydNAmvwViy6Tu@<Hpgzt5J*r2jz&%C=}cmwT%S6V9i+EJqo2JyGvTD<Y5~jW+GZ2ZRmt2SZflqkac;l&(%NrdOChE(cCd`Cbrn_LO9*_q)=DvSZmm8!9B>cA0Gc<>mMRt6%&rEc6~Af|fgjdPV^s#~K0Dq9+&xkxe~W8AmA!E<93j8-piF{0{&6whhg_H-rR)O8CYk{a2Hu9cR2Nm)&EMwvxD8oq99HXsqDR_M^?l`@P-*~T6`OB#DvYfHvH}0RHR2sUULr-4q%s&F-kUN_Y0IMe)8YqCq(5D;&iX=A4LbARKx)@dq8;ivpVL}e`5{-y8gfd^s}UdvPE~w+3c6x-X2=I-YeD1LEYRjlU9I?4BQV`%Asxyx2e~WrFRXPyQnfBjLcA|&8>dL?gfRCvEO_B#nY_+t^@N3PK6$1tn@<VYHWqz6py8EU6jkwys&2E=<vU<zwna^p-`+U@=8cLf43pH=hl;GdqpfoCJ~rcK#K(I$M)PxyktlA-E2<q?M^;RbQ1DWXjCF_8;abXT3e)hplAHQM4G=dX907<4$TwO1Qa-JE1EBs<F#_$h9w-fkGSXFhrun2G<W3Z?Fewj&D1qe&DP{~5;7#-F%@^|L%R4(s+<TM)YJf*1TZV-Y`GH|IhSANR^hP%w7-6QYyrC+MB_-?X%WPQb0?uJb%ntFII3szO*2c3qd-ZL{8iM*@19L8{=a)A$WEipjz>8RbpX)mj=Vbl9k1vt*46iQ(x`5}D5^iDFE`0gBty61y%5r$gt<4r?eUklI=~kWZ8)m~2Dsk?QI1e{w^fH(^&{igyOQVXUrYdR($Mo#okmp~G<DWplf^-+gfr&Xw=oe{GXDTJe<o2ojbZ|&2Y8|criFqyH<*8d4%f*OD+#su_|0a8Gob1xQ@*@*(Xk{Z*4vXpJ;z|-K;sA6MjQ!dFr1N{BiGy&4*3DVQ&+R!~W@MuZ-Cpo&lBVR!B8A4p?g!k6NA=B#X!=pphF)7VjVC0zYhFs}?h@Wa?r8Jc5J4E+Ee^O=Uwd-zSANe_dQ~V^2?h*;dge}}N~e6sVL)@VmkStKRkL`oD6%nn4ADdp-G|s4fI2k6xJc8VX5TMy`u)MmdS1udD43;HNul<L3ps&l<!IuTEx`g3CQK5`vyVtVLur=-oB%r#I}<>)RZtf}h>PJZ(P>~Avbv}W&|;#xAN^?hjE0K78X(C=<RxP^NM+ZF9J@s64Sc@NsH=}^i|VT|;02T%o0s<w55~7(9$yDJ)BF-v359Ym-Z=X-VIV4iq!J!<rG@A{=g?Ayc2EQ2rO+!~YF0IZD3ZZ-N(f$ubiq-y|3F^jT3$rQ5>RTvTFUZ~$^6q8wle9Iw;&2r>07VaXXLQFUsyTicFVN2vF)80VokVWlsiww`dX<ne!@;+sTs<V$drL`wiaMh%1Ou*LOM<xCLmpwC$_qQV3mfB6edM93x1ktM#bv}pB|$|E}*jMvX!cxU0H}zCGjpUs>=HyuO8FO<dqDx9+#A<hG&Ik&*XGaaW|dlC?2Jda<#GaT1r7YEQ^O)fm9)pT(hPMc?q`gn%wCaD`l)cRw~SMJCd4D(9sX}Lumg<oRIua0Q3`@UuDjSqWeHoX?hEWx?b@~+END0AkJ(Io`1Ythdm15?sn^x+aNUsf8VK8*M#~rMS9Q%+4QKQ4$=e;@xUOF)P?VC)a2pDNNhHBpYgAWO7#srWET2jFqBZuNV?JZZZ9xG6Q{(Ih>_dN_&HW32?TsfY1ex!F;;e4d+1n7#lLG#-tJhU(u>TZuhvXq6+-}yfhmmG*i@Bxn<_(XIK8kwj2l!rLgoP|gsns&LNU<@{5*e>qG}24@X7Xh$djD(Us>*w>*>&tKi8)OZDQ!j5Pkvxbi)f&6S)N>6ODbK$twzeGk<dLtEHV8u|;l$K#vZ?MBU@XXew&UkdnIKW$IKmhNV72BTTAky8F&-68&njm8D2ZmWf)K1}b%Ae3t2;BxbP#NaDtgu$a3g#gb;^iC+6q@5Ldv698c8hedepTHPBK_Yl@W8S+LSBC6((4<}mZ|0oeg_n9!d8_O(B|92!`o1$aD450E(thO3!1>i8cuabrIRTGb;?M8W1OVKh3qDo~f&ZuR2+)D9&+?uRla7|J2&EySgTEJc18h4FZ5IUNqv73#(tpp22{LKBw8$mv&ksDCEH@YiPb2X|suZt{(H)u|61=1d1Tuh+2z|mv4VL}CzmArbwI?r)R5yQooQaieNnf5G+DrtMfs51q=LTBy!EdWEaJ+1}l_Ij=kMURgu7Ms9b#g5v(4S*;mK%bB#km8FIGbV+Fs41V_HijVW=1!(D)yJ(M_M;_LJTV@Y3Mrr}f%?J=TMonP%80-vAhuY>_Mz3ugk9<Eqo6D8eD}lm;FL+4Qc=%`6nZKp$|3TY4uei4Aa;AWUoNiiL6Is8a{v7@`^QNDY9-r?bfdVmXX6}Z4c>rtqrp{Gl>nfZc0^eSlSKr!)0M|(HM=1{8|qJD3l5oP0B+?dFn=P-z$N-l5Ve&*E&kChu%H}tzxPU7qLH%BNLRw3b>$-rQ4oeyDnu#~*Fcz{p09#y$2EUBF+t8VCI*<`8G)<;cuNuuril7uhDZTjIJ;J;ipd1UU>YX0(JyBM+LbsJaPoq7A$pm(+}JeYz=&<(mP}DM?jL?76&@*whRG0AgydA6?IvO|unIidS{5Pnwm71?*&<5>g53xx8v!U1r=-9LqfAs#mSpb(W_eG*>u#Y+0`_C2q`0D&QR(OMEGf2T`A!0679-<oTj}5`p%A&P2D<C{?;Pwt2#5E-JN%(5&&1{4UX91zR@mPh^<l=7{h(6#j7rf_D9!2Yx*dB`VvPxP(NB<OV7oMAi`@kA2FIAkIIKfua|F3EpDtaTFrDuYm^3I3`k(mivlEp^qva@!g4hB^&6(5!Fa4rOy6y~C6gY0(qW%yP8R%kGNhBL!$!>DBVeypE>LZsjXu+0Yk+@jmHD;GMu)3~}^8p-_C-6>g6y!NJ7XAkj_G3tgE#x>7M5H2)LE;y^7y|gI{u_!iVH-M6G=Ee>L}S{W_B0Br3WF2mGrg@Nfm|0lVpW;}=Is^l1|v<h;7;HOmVi$SKr5oZ@<p9o`c4Y41dn7*##~SRg>V}eErh|9_p_JOiTekqgG8{%Fp6f?tkV1MQ-QhAD1g!ApoP|C*vkf@I0C*YQ-Qi%dqdR5edm-Mg1#3(F3C#!g^o@R)qxjc=IEuO7AZH3uS<3bQmmc{1M=4EmA!>4_0v5fj#&Gn7HHo~nKT+1?bod4Qc_aY^_)GXXQYMcyc8bZLFDuu-2$P};G<M4A#i&mt*Skw3Y<_vOH?6;uD)>#LltP%vdyMsIIBUfhs)H{8vj(bgsL*?fSQZh&~^>hjgNYw>x2jugd*65C49RWHrKj#fkZ(PyzqfBT#?mbApAS&CNJKl7lUS2pGLdpw#OW4ix>(TM|zB`5f3N0*#8(Zf3`n)Bpv_@o1(&uuELo9AC9QlV+Ftkqh^hczgjt>w}&KI9E-GMr^)UL#wI5hia0ajN=$4Lbx{bt6{8#Gr_?h;%WHs>%5Y;4=_%TyW3uuA5<+z?F|gD@>BmQ9)M-Q|%K0f38l1_)GodbEmJ|l7podVgG(CP|`CIPVC0he>>Pli~Y1<g-Xl<QEUQTs42+QJG<GCPqgiIYGc2^cPSIb^dQUF8I5&^;O`6_uF7GbUA!dosPrSa(2X<|c)Dmb|03avtM1D2#<dB690%qfYwYm5`r38lE2&$&CPP5_df2bPq(JJzm~5VJ}wb+f&=&77;wwot_sK-6lfOyy~2uT#*o3p6vZFb5U4dU3j{9sw>PdLA8gQAL#FnqdGGUz5?aOepD6g3@ul3MONLs|$&SG2E+?Lm9M@gghs&#MlzLOH>6{ObJ@Vj`spUkuGzO=X7p;P7^FsKVKua4^MbfiQRU31*5%A&K7s_p9GfTDJ9c5yeuP)sKWVUi=v`7AOb%Gf*3sMLC~;6<4+<%ldJAB*rOo9BI#*CLCC7W-PTT-poytEB1J{CF^WEIsxZqs!?K_P?IBLI&*MV|gjWI=Sj<1Npyza57OOT79uOF2<-11g`UjoMu&^3*k`)X@WHbrG6xAgR{lHt5OG2xaK=Db7zbxU?5_}pI$HDYmqAt?&E2<nHrL1sI4b*}^L^z60tjDjAdV7cGH>gO=u;zH!!<ayLKtvY$Ooc$GbHHxKOruu0cT`H*@hUX4BImABH97%h6YL?u7WcsWY;)7YiMa;i9D#tly9qhk!~Wcwc(Tpu)v&&2lrQ_hn1M;Q$$S+{w=?bw0@i9dJ8Ypb0SXDPg|-@kW%V>LcI=r*rBFhKBqh#hYWV075L@TbvhAX#n!ubW&Iy@imLK8=mB55^*AgXui0c;h0Z6w%`Ew*wXg5h1rjEQ$hBXM~Iw)!{&3dI*pMewVNx5S0FVTWIk*6D*=R1|&t^$umDo>|cNHl3o-1HUJ2?re!onb~d<fj6jUF66(j;o_B79>+R`IJTPf%NuP!x~?Ao~*YoSJ}DVSWPTV9Pu5att!{f6G3tlTqh6q6kk0c@Pry~lu3U($JUZ^=-Fr<#=MLzkmtTx7$TrwlhEwOwOwQmR5gwuBdB_Lco=Th^$DR_%2d9R*aysD$`U)qQ>k<O8D)(pU;%<iG|WhFIMrp1ul$jEJcms9E>jm5gbr282_6$B)WQ%d8YzcFxqNtCALBUUke5+8HQC7+<LWa{X+p(yk0;0NksPFl#G9*s(8ozl&{R$%<OEy=MXcIrc^2XiFSXhnsGtD}9p)>FU6mxF?U%p?Ec0hdRo$gp7W0Fz?WLg4!Shx^QjP)JzPRr*${8ifqr(5dkF#AFiLzH4xrh}!3A9_saOCd9eMDavGOc=={_j`o!~4W=g${vpk=0L$Rb&!D4FP0H+m(o<O`W;><f0HJD5>|wPXc;&CLj!Z#*pga;DQt-tyEO$UXR|Nkxi*oFVNy|C5L@{G;`2FMhyV&1Z#v5yYl3msozEeDCEf1XLrbXLzz;;cuKzYv07n%2I|?&oH{R7*NE=s-{QPsZ*};(3vLA_P<$#N6Hb$0!VfH=>ozv8X$S?dKj)$%*YWLH=S1U>(1MvNGSw5if#_TajEdU;54Z?-;lt>*a!csEIFh2|ZL)(n#=7}i0=y8C_D-V{f(VqxBjvV7!p54{F65RwZ3mJM2uC2QPP9E2b*j(|^dYLiPsjw-HGWo^Zw!$%@}~TdzfWrrr^U1JsQhJ&+gSUIW4<15GmQ_gE*Px!4<c>2f^)VbwXB<T+T}{N0U<-tOL}ucO78~NKIz;*d?(5#F{$kv3s!>Cv!g7{;=PoOQ1L>We8yxn=Q{DUWfBdWL(P}NOotDz7RojflGrO<SYROvqHIv|ei}hh5$$xsbt~k?&T7$3P~XFFkIX|s{Wd}rCZ8Z^U7-%5d`zxvl~}8j^43_sG8veFKNriQ>9s}tG{D$R6CN_lmw6^acd<sJ7q6@;_T0`%0ySLBqY7*9zYc^YTvNL5Rb#+>K9fc9Gof{4LRzU79SR@ws|>oVg)^O2rdFt+%&TremCu+uExOncPuMe`QE30^l_rc?kCMk2bx3LiVJM|kOfrM88Ui9AY)$B;+Os$bfKJ;CuY;+PxPwGFd5=v|p~BC|`I`EWB->x(P(g4ce7VAAYOzp1?=Eer6~hUh8>hisg)Y;lvgqrq@C3RPJVF`k;bv@Mx_3FTty$SSsJN6ax%J6Gj+fj;Ot!z0I}!@Ap#o{Y8K>4XC{Mv7l}55OzQ&P#5p&*pITtmFm{FZmh^|pR$ww|yH=skM(B%pEg;3iaw+4!YW>p2(-U;rxk-u?UW?r<^pK67~qI|}}rumke);V{~Q2w|^6?upbh#dLTR7n*R&gX4kBDX+Lv`qK72re+jR=NKY;LmCVCo3n;xvsPzkEql~3o8p8hP}i|)s>f_Wo>-h6JP}McLSQ(EvKl`Ci_`O&u6p+!F=`3bWTdyJ_fvp6LJ9U3EF-u!4->B8(nqzo6_?z+8;eYmrls$47ci$zvWw;(Y+FTZdB?FvHBH8kBPQ}YS&h`X#{8Zu_%_WLUIFvW{p(Q)a9V2`42^4#I<6cIPaYpmemi`cev@#=wXwjvJD)?{<1QUQkE!TomtZfZ;Rvx=?*VSW|ZtjurI$XBj31$)_O5?MDUXMtCgWiQYC!SeB&MmB`!=MXiXGu`&Vej$k+F4{v)HuPcyEJ9-(wz4AoMD!kO)|*!~xvDbWII6ql4~%dib8rlrO5wTMha0?A4IX8IZGJ(fSdBM_m~1adK*gPd6*7{7I8zFSV)h>|csqTE(+PGzJw3bYwsMg=5X&8q1lJ1w9t<6rSxdn9VhJyn^TPn8HXhuyODIDdJump6+3*nIF-g$i51F%yuWs^U}DHNYFFF3^(eNW`7gT@nDBMnFW58`*|k;A)D$xLO0#Z>ni-lJSu&_2;;<<^L;lF!qPIZAsId30NZN$J0?oo;CSF#f9ANs4Qe*MQAs*xT-#HBUF^mBHD;b*;8ZjBt?J#s@`xt^nNH2)$cc+yG!h~T6H@!9$)~w^GNq}nBEMvQlhc2kKDkMhR5#A?$j&q*si}2@)>wHzsPuDWF7CzWAp-NhsSS69^$Mjl>`*uI4V*ao6(L!M{{v%GO*1lm2<sk^B3#Wx3$EhbHE^N#i`j&?IVoRcuq{pDr12$C5>O00C|WpRqc5GYdSj==f9%;dhQU@7mH^$@ay7NXYG<ob@>+=ivht1%Yl%S5B9YDr{_{?p77HXq<zu;49`JqV(Lrl2Vp_K9|+m_N2paN;=?oo&lN~?Qv`<gB~~<W!mVuM5=h8iV01tZe|l4|7%OP6Ln{0e;#gk$=`*S{_<AZjv*%=w0n8I-I~DIW(ef5RtT6_CI?mJ&8s@-lgH9W7<Xs=HlmxZRLqJ}H!cah`sgWWrJ)zA!TGRe)&gFzd@~U$*RzD*FZ3cu1*WhhFsB+9EU%Yb`bT+z5S+HKzYUPu&mGy2pEuvy&7n=OerWAfr2ToI+<S?-&IjZaZgoU+Gq19*sPiF9PRY<rrPg(FJSZ9LL{VCxRiogf=n>c#<ho0UYFSQPE^{6!-KoBa@1cXh)Voszmvim)2a%5Fu$eFPl5hG<s70f{z`+8$8&S{YEO&ZO`R2CZRvHuuOtvQdShE;>CiZ_&?*N{=v^fY^GSngo0dyvOXpah3g4`62#`O4u8IvqgSeXXjWZ7yF890`8?nOTjGf>4UXHbxYb(C3CSAqQyk3A`8==!qoNB;k~v5oDrgWUNM8nhbg3roa}rtI~=dPQSL;h!Q?bvuK-;3&0>ZiI|64=<3ReDnJyVE!3*i7a02_C3Ao}f)#gpstqj<IsB9?31?zL`(XXv#j=rx3%q}-+s9a1F+w^HOdyFoq0tTw*|l98OXaN>`^VIXVbr9a1%mJcr^#@|v6q*UpeFPp1u=!5DQb2|pcLSGk>20zMGqM`YAT=U^j1;eZ(1TVxBaX&Fw0`f{p(e$6>@!n7I*N}h+4`q&el%Vee943zFcF)LXD`Bi3%`gVs;JBWXjY*%#&-C%VS=ORncaLp2(ITZ?b9S&#ZN4qG&uSon&5`hRtpQE(sBCx?%}oHHwAQLbH(<!($@e1mMb=3!Li&ev_^hqJZoG4AogeUg4!j=Fxwbnm$vJo(AZY3&j!S%2R5h*x!Sz=lLZ-`Jeus^@-NI>wrKW2A*NOuK@+Fj%uu)W$JiZ8^C$mvCXIwsz|31-ZKeuP3mba{CVf(k8~R#Mmps!<<6<z3PBa?LHo#qyIg^Yty!s`Vetn0FHRh3qWSu+ILMp3s<dv}Bj;8}NCC9QS_W*Yohfocc8q1#8#^PG{Qi-;2EN+I0I8aCGIfH28#FjqS}!tMXuxW%D{+BGO`}(U-}0F6F;G@_1_2SrUb$F)$~L;@BKuF_tfdO<>;X%i&w!EP&=1VPGZGqMr!TGN&+QozHBrQ1XKLpSYm98(*Y$j|o>tN2f2w=qIP)Ztso?5(q?b}13q>r-qG6o`!P&z3qrobhPC0D60TQSqBS>5*Ob{SXfcYZ6Z*f|RbfrEi!J=4zKthf8kr9K!<|(uoEhG2(VrZDU6q?OZPyrT`307D!;ZiTlWG1mJ3rYlPs=+!EpAjta`zOa2g%=L5O8Lht<oJ(l?qzg4rW)k@8U1lccG->D$3#!%I1k-kyv=C9QL_8cq9WB(OHpbL*{Q;+T*iL0OBnUTQm#PUEYat-FkJ=%CRCC5ByI!u{r~d&4?lkQw{Kt9w?}IZZ3%qg>qgc|OS}p=fm+ueB%Up2A)Xz3hk=*o#R3tRIR|)QC&k}T%qjpZr{ce5$pvcVEq$>PUJ?;8aR`KB<}%e2layqDl}+1ilMlrMK#5j8Qf9E={vL3$xyn3{FKOe+?VAqgI}+lF$S5}FmZ`hD2>}LpMRIzsEQcBP^*t$d#IY{u-!1c)OKeiceAo;-RG-OfO7r<4|CROord`bhKspi}i*=p!c`yos&@QcMy|9%~_iswKmHbq=%`uuNEt4TpFS&k%;lBj6uE6nT3(cE+!$2POOMj+u<u#P7nsf23>OAswyw5f`fHWKsinrOJkQ%&_wBb2BMaT5-%ZbSXYvi5j>{h;un66(5P8gV__}K5diU)cBb2E1HbbC|nJq1+z!{HB|RY{-7x2Z3S+Z}hAv&vN4P#!R+DXh0Y+<zH<R9$)faiV1UN|zwEq}}-85YtU6DZD1UOhvfl?iSlvxhofOK3!0h?q5tnBC10qsh1a^Sz<?+`=GiRH;@0HW32In5n~wyjN;=xoJ9sgUSgX60AA2=XaSUh9r7CqOl0OpoW!CG08zd$%2f08cFxdfHVSSOb6wnDsyDQFXC-rb;mSO5I>IJ_W<d`U_!qMO$Xze+r-evTPLY*0ZjXxI;gnpQ>ItC8b1)n>F!Px9xyT?ePtu+z%t7VWPw8>aPR-q@Kv%h2AnnvU$tYL*lR6sf0CYMV4lxjz>(emr6Q{;8xUF@B1sDMB{>5L&WYfLid8Rprg#2=0OEn1NGJCB+@!~FX<MazafkKeSzV~Fluw-~DUZxpPBvuAiGt8n?FL&|J!g`m>`0rrBnb3ROQCh>L|G%>K0WsUY6XDZbrhe|QQIM*;e}nLBC*g$WZ_4vF0E8A+7L$d9-g;X&2dM`JZ@p&fc>VwJ*7}(LeE(xqejmw^?nQyj2f6?_0osaxVMwX6@_)jORJR{~(<-}0_6LT~IzQ+n6zkU+xzNJl{o{Xp`Skzipa1*+{$Kv(%VhrTo963xG<{zUWlrqNGw9`)pPPQj_QM(?${bkHU<_lTHw|qSZnjqotKJ4N$&JLlIrA@uJdC$*o~v7hqb}^HhO)#h0n0R(Lr^2*(0VMFq0iUx4HtNEKT_A2Pp-A53dSl_THnPae*E<FcXw$0)6YNr^y%$J{p<Dm%R6rLHkl?^Y}Ops6&DHQ0M@T=F?aWUgl?;9wDlI#FrVh55NZA8BWZY@OeagbMGv=F|IBK6b|XX!-|NkiIN|D@EBeJ?KmQ&V>wtkA@BQ-AkQHKt#g60Nw)wvOel|lX3VIvv2oFB9SGGV>|7F^eII_tpAQvS_Psp+&2q&rwgJYgmKC?3-4BF}yTkdTYy-GB}a{s{^gsp@Q^i!BhbYZdMB|7OyZZX<)(3(1JujN1+^(NRq1*8`EF(Pm`xUCWFwvTO{9zCF3FcChvPI15aU9kBbEYdz~CU1dKiozCl;QcdVq<BWL4z;flNTYOL;7+-FJVcQn;8k@&OlSA_{)0-b>Zsqr_kK(Vv;MX{VSlG545w~y=cn~nI?vR38_*Jo>Rpq5pcv8Y2Qgi8?Vc(mc&b0adw{1#)tBX!Euh%AaKONKx2i}F`*f?(LN%t|zPPKC)*)Z@<c6E~!1CMI+vEP3`ns;lm4kEs*@+gNe^zmTEp(m+nd+i99ss%G`x*JV!W21~##mb(&73lbA)p_sjH-*-ZHqbS1U1^c3_t-}62f1;Ff5s7J!IzQ6?Ek>?yVQfbELvKm5V+L3P%VuKx>`zMJGagHXn9vmL8OFyXWRv2uT#KK3Fe`c+qxR<~H8~6@?#C>sg~Z?7De#CwHbV4<+AKO@Th%)?TjK^`demK4x0<%xRyaI0VrDMZFK*Ri8(Bjmm(=LlG2jJ>I)XttTg_L<nRQ*gIIBIlny5ic{yMK8hk!C27d_?_DnS-^(T%e{u7SC^naOJ=P(tCv;woaB2CwpjAs{L&l{O<oQw4-Aqd1tLj-IUApwL6l6e$wu0E)iG&-pJ&emhNEKrgvYB5Gy3}ep#CsR{atX&&Y{#U%sAm>;`2D(keqdK*443F4)-=d$(gTbWsY$$zVOGb$bi^LM_Ayyl_UK`Ctm}B9n;Euh1{2nEgSV<aWZ-3OFVXc*W0EMcq5lzuN@^ayy+p4=tYS~}J8c3{)?sn(C?Sp9URs%5&#cH`J<iUR>K(?i+l!vp_OJsM73s}3q+)VtCVjA^tdb2_2mo#5`qOnpgI*fL3y~~vgYw;SJOV9p3}9D1E&^IHu>7HDO_dw&B=@YLnkI-$6hwPo6H9OrtYe)cABq+2h`j-v@^8&h7y0mu3Y4TADGI&X<{~TZ;94kA5i{IS7`?YmqjwA;+R&zq-(&=lKX<ACzT0Nd%3?G$9b03NQ2qREP+f)6n#84(60_?ddRaG?gqu25ATR<wbL<65Z8ONrN}vNpu|W>9$8BgM)%5H#4CQBOEuette(<MUGWET-E^f^+q-!%H$YCAtoM1XLx*DM%1DIj;Ou*ram{s5{1}y~r!Pt6OJBXH%dixw}E-zo{iq#OJZ@+G5+telfcwUFymj>>Yeet%<JCgt@;wW>ub;dbX7PV6o{;t|p#FX}h*VZBQm0fj2%~L&f<(`=^j?u%rK-iHGP2ACq71DaN4K?f2=Z<2^Ge<N_5@E=781q?UN;SmcIlL(SQ#jV`QpY7>LIlL`1}z9uEt0+txx46*9av%1M22K^f|Op{HF7IUux46WO-S}{JDEdOL)#|n;~t8xJK47^QYlHU6Sb(ml7~zZE-d)8Z+-p{40)vxdiBxlVt5E}@kS9f(fn2To`(74M8AzKQ0t~zaxz*~8n=sVbT-&oP1qtOLoks+T~?J-J!~VDbLpb})m(}FC6iA6uoj(fLupi6a_R>`>ds{;w|y(OjF1HKghc3|huRd{?R6$pIt~N9<|GREI<h{|!a`+IQ*|G~p)be>>qv(RKvm}DMesQzD}b?%wR(YQaIx?hP4jyZWn5hjWVr$W9cqoy;8@B$6y@l5V#d4X!x#;k50B|_F|rC~cie{*Ag=u)XZ^qcnQ~efn%U)}9XssY-e)je<QbrE<cfnfl?g`+c}`{8j!ouKAMX%c+M*;L)2+Z5Z%Td^F9^BPE2N;zOpQ&p5vE<#=A$l?w!q%dI`Cw{U!p$%F9~QdA{<S!4)^Ki8FoI++suU3Jw4VSj4nW}b>i&md_7w*>*Z))f>o)ynBpURpVLs;S;(IbEfWI(NQ!*5lWct({>TKNTEDua2-*=j9(Fz`{>~mNqSb8Mdb0Y{c8H=@U}Q>CToas#4iF)jtizwhpc@@ul9PD+x}AvJ{fzJv*3rvsMA}4&P~k`}Fi9~PW%6OrdXlv81Q#c@bl<GUM&|)gc>;S<tp^&(EvYoA!VfJJ4WMniRY9Du;$BP^!Leu2v*xkOS6tA4DjOWi1eWBjZ@rDnwgnZsYX@frrC7TvQiB=f5V?khS_0`o4Z#(K_wWqd%P3$G(%?Ae3oHgzOB=X)w1Cy*b^Hp@Xj+r1?Zw(2gDXCyfqQJl-0)|W7ow9jSq_Je|C+5KZ403XR*I6VYEO7PYSVd6-KBjp<I^==YPz@3QUdFdIQy-XN2YeQP@w>mv4<+ON=t{P`Ti=gp!)<`Sz?lRTeWA7_oLTU>f$+c;T&pDR8W`@Ze_NaOFY+J25l1(Uc5Yql|Q6Rj>d@7pcb){cZ#PrX$~lH=S6!oM%f;ArYfFVe!h~_f@!MMY6%zz1aaW0X}1BDimXhtYFR<@Ezw&Vlm~^hBYB6G$iD0eVTXXla|x#-X=igJI_1eC!Epi>GUJYzS4y>|LJEY~Qu3H+oENR(+6k4=w$Kux9lLlnT6jppx-eDom>5|X7#U2?_!tJQ6r#L2ukOJacdwcmcrF0Qk!~d)H1Nxr)F9ti76$^@qO3wo$anHaj4B`*p+p2L(`Z=v5}J+O6pE#UW0#P$r)q56$4(U+zv3<l&BpPg_)>F3N{$+YiQrg<+EeJXSf1~(G-5O-rWjHy>of>$A>Rhr1QcMnC`aU^OYk=Qj68ufHk`cBdWqP<)*pG?aRFNt^{}*aE;kP>Zx_~M82F2-njF8flWBbGaQZs=@z9|_B@-bL5R7jKtdW*}Q2fIm7#PO*!FDDF_Wl4Tp*4tNSaG+?fY;%B>4hMSULz7kc!Vs^q9{6%b;wIiwY6DZ`al~$!wjP<)L*2sj08&N5w$Y~1?whvh2V=^uR-Gr;-!Hx*9Gw1rL6=kv(-V&CVdm=)T&Hc>`3cw%|zs->+|**z94U6n`-hp7lC$#x=W3fLZKwrO5IBx?DTl{n&i!*<EDV}Do%3E8XAZVjg=VR(|_nL^C=_rRT9YC3`VikSr$m@%JH8K%iTq4E@zDk8NNRv`nd5Rvn#|}077wA(=rBvEI;Hvy7q}7aQEEEw`;nj+{F;^BGi_CIhx2i*hq(-5w4X2CpSC>=VPexqrtncIflZ3#<RU`s9u)tFA77QDzu-TMvsX51a-|UcUn?K5}5)9)gN3(wB*qM@PNV!8m5z-be9U@l}zJFrhLf4wf&ST`hn5eG*w&|c{Ic!l$90`+SRqK%xj^UMV1D23;eC|ww+F%;sjw(Goqn6@!E})-_W&{CHtH?jB@CDgZbJhtQ}+#&3tZIR}PUC<jdhlS};_F#SQ=E;KTKqLwOj+2ty~5n06>I-(^)|qH7ry1Lsv0gjKBR%~&O%$s!bYS-XpBeI)+_-(e=FKx%m2@%({bUtOb`COR`3ZfZ+S;>B#AVWUtaiySplx8OQpT_+cd=&G)?%qTiQ{-Wyomh@VdWH5!58!9wEPiLxCWtN_l)vn`r6fBER`BQ@UB0%n@nrI$X_Q2FF$|&>r#}}O0f5zb=o6MwURm=oOH&<3{e&Z=DCJ9%Jd)|h-s2~MM3$uoUoU@eaUa^G<z0Bc*33)(+g*ldTlCl`Xaj;FLJ|Q;SAV{l0H-lu@I*n2^bN&4IF-fTKFa!(?sml{mk7R<uu~??nW9`EA2>V_JKS=7D=4MbIfQX{e6`D5AURDyWs|_=RKEXsry<elmYKj^h@F&7|WBYs&oCSA@H_ONB8|eI00}Wyo7WS{>Sw6rp!-D*X0OW}#)v~#}Lc&HfTeQUz-XZi?v^z00s=?B@3j(-8ZwB>T4XtdzOtzZ<wmie@TJq4Hu;h%IL=9>nWD*Lc7EL-%>m(d&kfrKux?zyX_O!7mVS2N}6vws0sCw2weZ!b&bdnfQMUT=XmyadjD;Zs8tytWJohu1V{J8{?J8fo)`$l%dB4_tSBq0GQutYylBJD=r)+WXV`j5f}O0^RNV+@JZe?WeR%xyulv!!ss=ufXkUKB1u7kIfr2TV=P>^-Pxw!3%i<b*Tp;i2vroI=cU?M6KigIJ7}^@)k<eQ?pl{U5sVOq`~tHUg5gH^DYLt-H}AqP9Kp<T3kPR|#n%K`%u-5jm;@rU5(<p7sll0RxVAU+X&nh0=*<ZGH}oof0$+63==W`7wM`BX}ZYA7UAovSMlD?)p9v*@z%zKV8!8H<O1WZpkhHJ>DKA#7P+ChbkpP7L5?rPHoD@nMN-qz|%K37vfG`t;z4!bZ;Gz-NW)#RPU>B`{~SjIbj}aQOkh_Fd}e>owASu;eTOq=_I}0WI1^kZAN!biei9sGM)+siBt-$=_PO3I<BcQ;-hpBCe27>THOm!dPt)<J{M5KLyNT@6A#t>q%IX`ki=zX+>x-Jmz}=(a;_OVW$e*FJi?5u!OV?X?a#QcV8m>7h1YU!Pxm&DvO@IHp?91Mz0RH5RE2#}zBVP(UI~LSTgrIu^I*)Xh&+503^U7plw_R&9->huN3s*`L9cYL6*BK>9Dc{vbqPjw3D7v*NzrJDlK>=*s&(*F1c9*LE{Q}1>Aw-D^yfJvrfyS_Zf?QOh+L`ug}78KqTZ>s_VG_F@FEmCaP~7!=@CM$DB87-FUmUxueDT7vio5l7^&)lMHo{^ba<UQT<1QL@?qswO6nafa;RKc)xI@R^OOedz$7v)q&$2C_)N@Ob?k-ErV4ovy41i@_lfCut=Zk<)jPhHz{rO$=JB)F@e88V3?<RwI3Ox<#chYcDo+(nx^x?SPBUXLY~i(o`3Tbaz<U8bAU&6tpn%7+#67@WCJMR1+2u)X-9MN8C8CfzD3fZ}l-lq0)2hbq`-|K-F^}`|E^j*j#5)Fkp-aN{f=fUIGQyN@ooy`JUvP2YL5Z*p#UhwaH|xyBj*=G{_m{q6p+#SVR0dMrvvp))6L*XS*Mnp>QLZ299Nn)k^iEKUUlMU5XP8zq5Ek<a^Y!fNS+;3R8CQU!>l8`jKRFFr`paC=&EyR;`6$SwzbrLXEsQvC>s(ApP+qdat@JtKBAq+WP;w>5qX|?VV@9_%j;2u=c&z;fKT#CgiAPvNWVO!%j*bcX!CF_ZBkQWA5i}==KRR0cAY5NfuVXhlB17o*FR5fyJdt6Wh@jwNu{SR+*#8_v2GmPY-KJRX1*QZ9zNi*R$M8tsOqCT|z-;Ud5R|0Fo{Q|McH5HA38Vxz^es_{9gXE^GZjkyseG9s(yTLFWEx^hG@ja)5`<dgl9Xmx#TU9fSi>xE;W}?n+tf*g1mZmVb;9>cWc_iyLf^J2=hWqnhEZfnJtQ4e7K$^3Q7D=wNc;vo!a8x$KGvCuU_C-vvJwqB7ScMzp;rHt=?UGGcA$PwjSz|5xYm6k9|MMu?>1U23bZ9EtK|G;pX8>`2t*laq7ze#cyT=EcA4)cHb2WuN5I73g20S;=TJ?+(l0Sab-|}J9hloQDrx>;o4@Sh&-W;OO-S_JrScG44N+n^-~>y25DGJ_6Q~gV%<79I$t%`yI<EcMYRJm+QOHWy$wG_}DQUfv2(>mqcX{Ra_D}}Z-@vVOoy7yc*}DI}u2!$grqNbHN@<ZR#L^{drVdEdHiuE(aV?a&UHuouXQSJb(l?0&FE4vdpamcfXG3L=Sl{N7kW9QIaGg<PUwTIJu)7n<MhX=`s&Jj?MXVz<ZPU?HGhDmVqJ%K?^&udoi~D^O23514M=5UGi$mRlrzvdb502@S5^Tc<l$jKR?Z5l=^%s5*h4)}fQ}2DhRAlzJydQvUfm3QpU{tE~eYA!Ch2!<Z$X(Saju}X#FNf-;2I0Zb%H0E0l}En;C1^`+9BRa4;v#43M7ltP5$%9-+t5bNk{l!4m&J&)ZPCLpWay9lr?@65FYXx^1^2^vPL}^(!TmwL`5<fg6&3tC4V>Mzk^<oHM-;UHPPlg~<5h^n|I}2dlsh#t02U{UtK|D($&cAG(bzAsiYs?m<0U^Vi$Ty~RYG3=kefIk;S}s<q42O-fHK@xC#Y00ApImGQ{PDjGNX{F2Ck#^etFAh#*7N<@yY1>5c$UzV-FV>;y$U<<0X&ALAN24pVftWk~teN)G=WwI97EzVTys*)-?9xq_gDYOe~Q7PO<<)7<!x)#=?PGPjV?t=k^pOFneMbnRE`aa2W~#KKPs;;hodzk}!T+Ny>vV!K}dGn$#u8k`GbmW1!;@QlSd<2)5&}o>k22M-i*CkYR-nDB6f@6XyA`J%)S=&pP`!qqesIJ9b!=#$*OxXdDiPn5gI>875hL_B`ck3KPdRH)apiO~J#e_*R9e1Hvz6JY00Inl~DPLMp$Ir1g&DTc<M1wdY`#t#S&f9)Z|<L7&*>dK3x}N>M#*dWqBf_E+Kk8Kx~u(T9IDY@`r+VBMBsY(Hke5&sjaIpP)|u^Ny^<YW*QrIk~Av|jgxCo%!B824Hjkdf)hXI7jU&WdrSY1f2xn0-ED$_wgidVPTr+Z59};3%2oqX=?qNBZOk#5gatRLDYDbeyxskbPpBBt$Ai!2#7*m`~)%2vQk}7Tai*0C%4EsHjKm0LzM!@I;BbhkiN6A7QVdTogL7o+Z&DvGU%rgDpfPG#QL2Kv$DtwBk21{dN2yJWH+`>)eMS2gHzUND%jwX$GDKUfO&<J}NNh^nMv;atV#<&9p>GNE|+q%8}?u32pY+A?Z^$sfQmjh5^fif$XXNKEPb}I;|lg&_dr<s$yjCHAIGV-hpM5g(anu9q*}#+zuZ!17n`*?<9}{(Cj);T|);HrrXyk%(6<Lo|y3242*;lajEU0#XMwA@K_dEyFEx+T*d2FXz!}Ng2N^3Lc{%@D0f3i%j{TtXJoiE6&+T^&TldbDn4W$EycB_p_IV@#Bg*L`slq&RV+!(D%s-)XFhCGl%*Nv+p6vd`3c<iXx?VfKM!Gw>+4ToO~WO6s5#w)7q<J%laIodCSk^-?EPL9oQUbKxc&^dwW99YL2at048!_dxg$$<+9vHXgB}vP7-EcU4TY{oMv)*@{hMuODGa^2WV}2MQXPGTKo>F7{A*|$^&oMLO;~vdbYadH&JKls203I*LOE1RNSJS39qmxaZOCUbbK1Okh6%0Z45+VEP!J1jDdFIDRYh@!W{~qSykH{kO$4l+YM2lU8D%y$p|SZ4%xt-PTmn2aIaHapJCJPJ$syy}ZoOR8?hoceT|jP-q&F~kT&g+O+H$CEABJX;11wsV#>80=Ga%~wFchj8_MnCYd`AVNino%L2p$S$4SQrQ@T!bTDG<3)IqV$8b|_RfqI2woZf1-TR}1+O_d}bn>JQ@ZHsnqPwKiko{Q|x4=<>WxJDlMZ%&<>nTC<|F^rUaQR_PoS3Lf?xaqA%il2stjc0C#j8IMecRcE_0JctW+$9k<pJIS!8=QUxvUK;Ze`fIGKzig{N|3fo`hE}h^fvsz`a;YbRG>4n7^U#~o;$2PSE<$&a-SQn?iQp`a+<x<&dG`=>jeHf6Iw-NI3nM*TyLcUD?!~5oRSrnbQ-r)It?P0M1t92x51Lw1Qf?9$VXqfvB=jEe%F<knfI)S`b6$VWkD<2ix%u6w`pHb<5ii@x{;^=N^;9Wc`c9L%B(5?TccL`)tgUKwqOLhC2}=d0r#h<CLrkJG{UvY0B!904OV88|-N1`N+U6t|P?y-0WH#iAr=bwIp|vo<;i5V>ar+guj9@6lZMfkBVMo(<+CWx}iE14T_bw@9YZ&*H_FcUSiMbjLg>{rewIOTlskrw93~1~Z$+yfX_xso;U?SZhQ>W7Dw1Icqz^4evv(X-Di4fF4DwRsCBxW7+e8$LWclQ7|DL+^?kEN1(2$&Mct77&Liz<f;K7<;N5O?czu15j}k*kk}p+ebF210at3+1tF7BaNwaF9cEKRgHf7`mE%8BEkx!|m58UBCZ+eH@j6`(0f7Z92WG<;;~}(WLXuRwb4>oW`IEJ4-teVg1%;R|kAI?XgbAoDH93wm_Ly*t~EUrV51Xc1QxeM9F{M^+p<{{^K&tHGC#o>!ZfLLDjjR968zvP1z1h9RY(!YLP;k*;_2^mPwjy6B;j1Xy8K1D0ruIsj$m)+{dP(hSB790_Bhp<X~X1(>#-=-^Qp)hZ3kNT5NEss89mMZx1?*QBh9dKH?NM4p}KS&EPt^7r81OT_%aO2|@E0WSqeH7;?xsZ3SSTubh^lmWW>yXcw#S-tl{R990!-b```h8H;FO-bv|Jv!i$uTRb`i?_=iIf;w;>;`oLszcF(u;c*xWZ(}Bvx$vZfODY0qW{IM-nr8Q`ty!Y-RU@#x2V6*6cPQkY7=tTV(fFirf{vu7yOy=KMzHnk1+mVk5l=;guS72pbjPH|+51_bGeRcUrq2zY23U6$uyJ$b_Ush0Qu^7saiLt&C5=hY#Xa-DN!gIdLTbv^B8A+Qj9wP%l&fj=um@!^v!li~JVC=pZY?4%A3IQNE`g@i@nfIM)OoRNpmk6a2Gt4y9*A~R%tjJ5Zr#Ex;lo53dQ`XuZtuax_zHoneNrARi`PIk(E1^NrarM-DsBqh1poj6pMUoQR<2R79D5_rx;S#^*3eGhX@wns$c<tGfig)-<dZi#AQ&YWd|0F_b`)_GHqJ7U<}RTl1NNEeF$Z3GZ3sU1iak`-H8Z_&z`-GlFHdIB?Sn-?IRp13LuyLDflWopW<a>%@-p~8TU!0r!5Myz8k^2j?!F<c1kmS7aHl=&6s+{DTTghM$4YaoI)>Lmt;1b19Vzvu+O{AoOe%Z10^(jy9B*1Kb=Oi*&8?v{ypADxCoN6Fs{C{YINY8+0n@7&+8&lrc3Gwfv6^EBCb?A<_E0Qc%EPUzlE2BYZ0<xCqE*yX#7?FGz_Ok7lD?_l?#qz5gP;ws|6~YK?5Hx#GEKBB^s2D(i<d^j;&M{+JFptX3nw4ZN$x);r%=MfjIK*RyBHY0u3hB{k=6DN_xre$*XwROkuWo(5S`ThiIY96m2?KDS`BBs@c1=Cht8olcl=@<OA{Ee-zRp6ig`G2^K^>UI-yoCOJRbtgwEqOd>s_U*0B(Tq9bHQQ>4oZ&%b)(>UC{2{jnzUV<EJ`%fi46gw(JKHdLZ5ROv4AVZSWVudknX7sUuOCF`$62uu`k1_Y`^7qzjFdtxt%4Z9fOjFqdz8XV(g*85fjahdg$nJ!kC^^E<c%^2=Cbr^WwAgFLOnYx}U+amBrJlmJZ_T60c?cu6US3QFZmc+xUgOJTkr^zu>xCE1rsq97`*Olm_k0MU+_31N%4s?P%pWczKR*Hrm98h+b)z;Ui(5pZ|fHYEq9V=C2$9o;4@a{6j9O~~-^g2LT*5QqbS77^O8>3g%RH))<x;;$EONNJ@JNw2gnLrJVP}~Vcp=}*Cg%Y1Mv!5g1nNI8gZk1^JO)EQ3vVHCoUMH}GeV?Z21(aM7R-_qh*851?i!KS|mk{Ishyg$kr<Bh|Avsm!?nO+a;El*QBD#3fgefmzCAw`T!unr7trK1e)DNKnQ2dm%T`jv;R(PjKkl<?=ot+La6CJUb%eFsfC6!kcWqL{#+Sm@NlMyPlh`q=~ddmCl=}PPjnK{bk!%S(AQUvUo@(a{jHsNI(^Q4ZMip`SjF7Q#ye*%YeRtuUFUcN5)N5||m8yX9dDM`C1LQrzb$bR3Hu@HZ%Q7l5Z7LAz$**K-0!q_!>18m+-!Gb!OTRuqKlzu|js`i^}xfYsmsI}~Z6EaNHb+S?}Jz7l43yf00CV=_$m1fT*kywI{&RsP5LC*TA{Wy400znpZqZq41g>=M6k1_*xOf^=XRHmZ#%3C-wvr07n9=ilM&G^3Q=6$zoH5wJFQ}KwIv2BCO0n1DAgNRU%DtcvdR?Z9lZ<1y>J-$g%Du1aW*&$zC8RDRsLZNw^ODiXw(J=%rdGUVkV4ZiCzTm0L_8*E=(W}6^J8XkkZKsRcB*dwr=P7b#DAtrW_WKeKmB!9&HcH##3xOBG=5NnJ!3v?5MtX~)u6#4lso}XgQWP@wldSYZu@>6}Ex>Eaw?aT<nqeDs^j;NVxhOB={F9($(>i||m-S7S#WO0>!*3Elt@oSjI*o%$cc&ha*u}PltJ%BJI8a)<4Si}V>oaLmGA^g}jXY*HU4Rro@sIbr<M_`<d}!i|R$~Ms?iaLsX06~Jc$<1zI(<vJ8CvR1s{U1kp+-?G2N4g)IgwxpqJB-EC`vnPF>6u46@u!4{yun!fLkWVt);<l2Ycyi1g4=v{OT3HU4`3$0_Qi7S|TkkLGkYT5=p0ey`$H8_d2Ksec$(Q?va=x{^9V4w0S9IydLMYKT*pvm$O}#ahq>gJ_a3x?|yy##c?R?5BFb&AC>Nm>CY5x?AyP+&2>^3iWwz`K;s?WJY|z$V$idf#{$ksyG?OPG|N_%IdqvrC7-k^IZe$)O?$B%4_o)U-Q9oS6{F>nzJw3dn}yvcROp7he`!>L6A5H7fqMvIzJD*h<p*3p@6X@fu<OjJV>^Ycwi-e&EuNKSWhhMsUNm<>2=t^J@7T|;KYjZAYJU095^6pquCG77{!H$#z+E+W;JW;oH=Me0va)T0rj_3T=lvE|yIjO`%MC5T+k?JR7+I5kzmdFX4o5xt4F9{_n?XiH?Nj1Lrlm(%t_;iVF(AT=N#S<<W3PLzA=!P&t!HT+68p<xHGui)fA-~{0zZYg^7}0Gn{^*YWB-61A>ygvN&chUJgL>5>ou_Kl9As@sk1*Qi!a7Ke^EW*x1i(8$G2ZUx#@$*`FR3aZwuS>LsGoGjUG$^R8}>?n|`jV63_6Q4A#^Pm$-~%m!cazIq@(Ts|(`wR=a+`A7B5=kDq@2?k;iv>E|DQ`t)X^ueW<#+YF7W#hUYaSmbawhp!_+iygYxfBF4~AHVzCmt*+(cN4QbzQ&wn`)Av>6{pV*saG$X$F*TU8n>b0qSS7selvt3fSaTAb(y17+x?&HA{GB4AJsw{-wu$etdR`p?x_g?OmnGz9n}KMPY)kTO-+n|*&%SZ`0$ESRhy>J9=EFta9=Um8X2NVu=qwg_Ohr!B&<)AkGZnuI+8IyF37xyUOp6Eux*vV=gQVPPP&XsMb&_u+uMdio9;f-DOta7QK{l$ew+IpxH-)I<^1ih*Xu8j#h5NRM@dh)XH)co2QxJ)J6P!8lIv626bW6@X9W06Hoxx5M}Tkc>RNzAopLQwT-$uKnff{`ch9y$jz*f(iatcb_0dH!4JZA|yOqBmx>#OKNtD2mj<9x-P;Ajc0sqs4^l?L2ZRA~eF@<g29TL@h)#iP{L!;1$!DZDbPi{1m-qqGKeS1NmF{`BPqf@pHQt$50yN<eL2!$Ks5w4q3H(1muwa1HgMbKILf(yGX;@ng$BHKx4?Od@pu$pbnYSz-n!1s4@iL33ibKgqV+e{8OGaK30c&SXQl%Ik`3oUebXPFlW;MUN_{L=%rd(;;$0^Y&*!Y((N{-e!2sZk~nnY+dsyNtH6j$p2cAVH|Zqc$JWMNibc)UOKTWl@CL-=sp|R#FbM{32P-F>0UM6f(7S?I{@V+FKq2h4$MDwHXZEu5^uPU$Y2R|0R~*IhMhCf(l^53%}WedGxYIS3u1o-C^9<2nZ9b!y2IDe%C7C@um6oKzlSm$DIB_SXF^RX%u<bP@yH4=w&o_>cj{-m>oL*Qy!XRg+**UULmn>HnTc7^mbT%-lHS^e%4^^IW8A&LfKcTMT6e+GE*EZNP~dqvAtYW;NNkkC^d)vM-&m7HE%D`1Ep%V!O~UhkJJ9Ky6v_XSwEffmkf9n`m|z><!%6-2ot*@e2pHWAh4NP>;6QSN?tpdrfRPv8X{PS*X$zv%-Sk&w<-)ZD$UnJK2U@K>ACmOI$A01MOQZGN-uuj%QAJu$_)7W&3PC=@5(_VCeaob`Gj*MgfP#6PCLfX+mP~(@J@Uw3t=L!8$tJB6R|ABOk!EvVo+h^u%+ukKpwJfTDi?V6eg6h3-C993$qTYI|B_^oWc#n1452h#c<5nw@s7_XWy@{pkE4gG#7pE2YHzZ?x7SkIe<djjEUX?&nxn5n=p|A<M;9(drU1?^y8eYkdmKnV_8w_yP|NA#bH`lYz_#0{0cQuFm9F#22ngscEtJXwvC>bP+mfA4#2rOjxd9}l5JC$TlSoC5?!PRPM*uQm7jA`IR}LIufHWa{P?Td1;eAdim1a+>4JL&;=nX}*)&-{of<I#zXwknDsP^anxkM9>p-;*aMZhka7jTbo#`nv&n!Pa$KauN<F|s0_KirVQv_6N%;#n)+CpEGbV%ocUR8L*MV%z5wwzAbPB?lMSXVL<78MC3YuttICU`%?(j9Q(sG*ZF1(#_T3Y{?hS=vCwu9%mHZ973rf~`dOuG2-!5x?6)43iurH%<%=7D9@^Y9{GQ&TM+w0OWI&G+N&*!j^=LVybZ-ypRcuX4JLoZTKIpq7W<ds{VD5lRik-JVEZ47NslWEP~(n!Rj!ZP_noGhT+VT9zSRuYWUnd@(+3nJr#xbm%mpbnir4vO<L_-%81;w&gXbcZJwf@8`KG$0PDzYBk#_T>(!s)5<FmOz1(^2%+OGKVA2i}j58&C6SR|{UaQb~gXzz$!yOYMHZ*5R>huGdtun9xqny;lTh!Z!xznKU41E{DIOqI0L3V-qTGm|v8<6m}`$c~60=*?J%N*cJYeo17HUiUXw%>oBMNy4wKNUXU;JazdGxP`O-`vKjom|noeq7sc6KsTrP-Y;!yBPWl0-8n1c40b%2GvAJ#?Z>hI|6n2W)tUtHJ=iuJf4_wo-G(s`p>q7HH%@^_2gpUkZ|a0nu5CWvxi@^^}OiVgf&;iT8sVR+hIrmbnip`_Vx7_%yGhJpESKkWp+XJ6{OcYxAK^$iK2|BTR@AH9Ic5mM(H|G0VO46-(bw#$CFQ25(gS)LV*2x`GWTX)QA98gaVj~ii4sFW*D>1RArK+dGB}SY`%#_%|(O9kSZkjvl?ZdB*-@a<3l}n9&@A!>2a~-2}C?fz(OH30Cvvt!rM%n$NmcC62dx%G_nGUgfR!W9lLx1N8Jy}s$jLwV%`j*PY^Ybw}`UBc@1wk#(_}p+sHf9rQ~50pny8hfX|}xy>~^RbxLC*=Mj~sdi8o5n1#5p)|>V6U84*baI^)8eD57!ZGH)Xm(3|0XPNF`UnCp3&>pp?27EsZi(Gkw*f<f-H%Rjoe^(=Q%Zk)@1wp|wg!&(eOm(6Vf@r>yV&IfTPR*I>_ERUyM`u$eI<@i)<TD;wFmJtaLT#X(I^EI$rky)Dq0xq|oMQJ;I9z%PAi-w1u_j2)I%ygR>!=64%R%&{Iv}1G(<|lQDoinrGINx7s{o_3ZF|+8T=M9rs{XA)<P;5={3+dwb=<QqD{d~WM9{>l@Ofuj8K4l(_o6EwfIE$GI_0pP=`%0`D<oIA=NuA!sjMM=e~^VL^vqc=N3p}CC>$7Bbhv#jCl!U5Te(s%Tlf?`9x9hco=T^;VhWjoc*w+fY@!d?j!xHtR%D^Y+?!S@WYW$<h0TL;vllHo^TkGi#Z9zQWQ(g6f2k;;J6gSWqSi#Q>emyE6We+Ivl&eDk`&h-B34Qu4&wZxrp<qV;kM-Ta;YMjXCx$}R;zCV=`MY+mLUNfwB=OKi6h34y6(G6ger!i4Qw|GD=^9PoqBG&%P2=?fRbp3LF8!_Bbf5VV&I$XNI{mw3;VjFT)U<gz<w<oZjAzRcUkIGFW9v#{|T)SD4@6Z;WoSt=n&-<4wu*T+<Uxhx|)0ZB)2o4HdqH6U6l5gru~wT%bw5!?izswVPkF({8DL6mpcarG*(v3i24wy{7+Ns0b{Kachylny7Qr;Vb{!Rail8kLzH%6M6PQVwLp?q_rXSvf|RBDsJ4PrB}z>5cpS3@#KKE?HcdsPijD`eU^biXxwjnJhTcX)X9mnp5v>_@a+_V-$*H!WrVFGFwYtwZS>{%Fz4*)AS68MJN1P=*6D4{uBqG*6<nbpNC<|0-d@@?iey#I~#GBCjD;-Ys9=V=3I1E$JM*!?UZ!N=4Kv*8w6&1~4cLBLol68LM{;R?&MlT|1v{GAi4FXnoRg3av&HS!R_{=L^RSK8!5h<#ci6t^!OZGZjz)@Ja_8Im_4+WF@u_s4pMY{#3T_=kpB?K&d0c;%=lH7()*LGrex1<2YmUkV^P$7(!gl1h-01Riuk^DYF@Bf}KY}bWB6l^`~lKh6OZ0?YeOqy87^ux5G))_$cm_C)1ITuv@MeHi?Bvm2g2$FyfF~&)c>(Ukf(e%5Fd@E;a{YA!MQc)W1kamTQWk(5$qmyY=^j+-RL-)XClG)p)FQp3C#nK)>zakE__=Nb1C5!lCk=tjjBkv*@nJn9GSRjZ?6lo^Zp%1g@wpsKtA`js+bz|agI>0st$u`i%A@rOIFe*=~9J`o(m}aSv6=EO&)zWb)7rH)yMpCd8Tw<B4Pg62?R$7KE0jiTxQ}J_Oj2*fTa!FZk)C)2#YDQi8!}%XBm4*vlE()RpI|>~Um)6zARoA4E4QpGF2%}v<(^|yP=8<+9(dlhhbHQ>^*&LZ}B547`JD*M@q?3of(s+H{;+H^K+>Ncl=pw!VzC1}sCcT;y0Fm;+8dblS6yZ^8Cf%aVGpL{u!z3s4S#Kp;HS6P%VB<rfs_22N(2u4LfkO)GhD9cYfv<#CTdjd@M^{$dW;q4d@4sK=oSz6rjEx%c8ilcdIdu&?fRo^FaZra&m{F^Hg@C+fzRi!thulBbuE^2D8M{+`E5QcYI_ASkFaQMC{aQ!aSBw(q;8^|?6Nj}<92nUUz6TE%AsAgmtO`8`H=6*)J!a&-b{GAAHVLPOWrn16o@9p>I0QipH(5YS%)_rfBNu|`idtE?1>Sl~WmMM4i4-r9;Btn)=%q<Fg>RCxdMIw;1vS>5rb|WUu-J{OYAjHeN1@rQV{H;OI$8%OYx*H-rNZI|RDUy;sf~fO{n~!_!}tDOtQfe+zGkle)X8NQ=n(FwLuwQ1t)7q=r959zmKvB<jijT{sayh#rXeOW!IKHT1ULitAHMtb^%p93-}L$-zm&Q_!?y0DUKoW=vv3T8UKZ{}6AB(vha7a}t8`?1d<+bFP8vszCG)(G(oSF<?4oziy81GiqTZozN9rR#>)pt-LQ8w-ENo8l)$+I-$Ti$o@6OIVFiQ>jD^aH$tzd;XlErZ8gj@YmQ7eFI1ePMAN=_H9o4XnaM&Tl1P%*CGvuAqd{7)ZzX`cqZ6qrR(Aj+VjP~=!tr{=gtvRm6COmUQDWgj{Cprnv+W4NZ|`v>_lt5QThXVQ;hz8D9(jLIkY2lJ^eY_YO-bfW^yL|E4)QR69kP>J4Wbt}DG)b7ZM;4?~^+Atcpd#)e0G>LU)c5AO5Yrn2bca4JSCGk*NkBVS}DUaah@!-LLJG}sf`%-$!pQqHr^x4^pilvvO-4n#$BZPoa*`0d|14=0qw@zZn_h^PpZ(3=<g}Nj!v!JdrcWfC$x4L(o3z8Z2o(78*>xE;bwTB*dH1|lFQIfKu{Sz`|lGL3y2W1H15Q07xeu24vlz7el@n-0^Jy?QTg&P@>R>ww5Yhu<#f4QUz7Z}&3z@BFJsvtNhfea{%^MxRz{iTsn0fx*nnX<~JnzfPk`?P!8@Os>)+&=9H1;-gdO;Kw*8IQjlfXVHKTmO|m()+7&S?=r71t*dhA6V7yy}nu-;9ImRPw`L=-zKd>v1HyFuZz>C?gE0AZTXOh&1Qx8sqT~ts-@@u;xF;KG<sPNsQ^ckhmkxuks{H`rJl6{W2E9PQ-tvKAajjC8$hY*?a|`**-JC2O9Pencd*ZrR+Ud$1Lqe-(=|&sG}{u)3HA98z!3XORqYak4JoSj{`TfYViF?zd+2q0zM4j*b4rMXS}mt_WLk&Vs>Mm*+aU*w{hnLI00!1o>wK^t@<GXV1hJ4|mxpcIj3AcGK~yEutCx~6gxDP{_EaY_LBRtKYeh>9gLbh3?|2hpx2xN>XHEc%j8+HA%R-uls(9<Rc#3P~dPy*c9gk}EV~C#jZBu7=k)!It13DWr<W2Q$r|aKHtSR1u4jv+E4KCQ!w;=+`s?DHKLkM_AN)BLwmk<v8dbrW36(PW&)<6`hLO0F^WEA=wdM$!=nTarmjA9Z|-TOSge8#V@*2(_-`qQV+uNjYX>s568*EjE|{LObCcbN=izbw7x`ECHxec_ukdb_m1<4)p=w(kCmtRwuEnGmA=?xe`$E|mBPhrT-}^BAQ1gFKV(@+YXI@f7<Aq+@zv<OHkDM|Fg?xm(Q;0BFQpd)(QuszPYpLc8AB3%^i5Ijzb=nnPzr93v8G-wCZUsS>i#x{ofoq`L^lJ=YW<1q2IH?QdT+iZic+T=GI!h@YZYpdTHYAaUw90q6@M6C!_w7nfM>jfmY5;WjYF=A({Xg*`_$R#PXyD`om#?|=nQ8{9AaVtLUBOEKj*jeXy#XNA5$a@D=ApCI56g(8ZiTL?)25wV0eV+$nz$=VOkl{utR$*f2V28%>rM8UE8F(Fl(QDx#P%wc{X+zr66CiPUnyPj45(Mva*Ag83J)<#I1pI0cekb}eNF;s9Ux}|fS6V`z*&wYFt*OGMv;<I!wtl=W-OxPE^GV|s>B5vuHdVdwVE>eUOK8c#Rt*?8Ut<LBRxfc@i_ykn>sS_v$pmc!)+7L`Cv|+-70)!~s5rR{1qf`ouXfKN4!xg#Sb*BC49s^1fb!vO5ZX5-Fsnnja=o1(3$ae~n)JNX|sg%~_mO>cDe`xHf)SyYof~Wu#%RGys8gfCW5j5q==H6nd+q%rB#6_Tn2FpPkH4;__t_N@HWR{xASTIZLgaWQlH+~*374ji*woHhm!>p`7=B83uBteyC8vNPn@?)*yI)^q-flrLuC-gHmZ!%gRyBhI@lsZLFURt46b{~A7lU*PwD^7<_mWn#+k>C{Qtu7J4LNDf~CqTeO6g?eB4%A|@u={ji-`A{;%XV!ilyzi&gs2;7Ox;D<m{+&)M9%2x+$cPV#EYtBJF-VuR}9eWyJ8qe#t)o>J7xMxKZbM9$<mXV5-3f|bZpi%HMO!5z=en^F9B^^;jx9v=KYkYb_`NR9Dj+}*1{D!b-Mb9Zt4&%bW%BzTsO0)ZPojn?Qs7=F9RXe$r#4i#;(7(q{ojcUZN3U+5K3k>4364zmqtle<`|ZicwEVArdlNyUdk%eo-tT`}2j=&U#rx(hitsn`_=!-{nT3^laYGw5X*91zqSRnC*yvRZ)etRy1Fp0q-;)1@FueDjf);jv0K%|Agx50i&~XEEV7jact9m<TtI$)5_(No)bnp*XDZIhRd=Jx;v%(WF0dvDMA}I#vOS3xz`8kD>gW)PqHYI_qc%Z4#8pZVT}YxLO3V^W0|ygv0}!sR<_XQvFRPICJ$(Ca1l7h@{D#GeWA${rF6JH8`d|Inrnn4BVcB8A^>w%7=Xgu*-Yh2-2<|u8k#X+!9Pl(vUqtpg~wt$1BHN(rsfo(3%oRn_B`QxWH(`n;Ae76*#H3^jF6!vL(o3BwM1q6fmpPqAw(5JGDhYJII4HklBv8;Q;~wQ4D!5$Ey9}7fG+p#$`#Ce@F=4GTwQf3)K>SJe?@>Vd7su$ccaA$qtONEW6I#jkFq2->jZm?G?s1^Jpi3YF4W{vG@saFMT{{31$fU|A;JSl2Y!1Zno5B+S1xSCff?2%4Z}vf0e8QIkGYtQam-5UUIp41Nw45=3HyK1hLttE_6o4WJJCa^(*rD?>k8fcKGb3pZ|9vmJO{lh88@#X_E5<4pn5WNQ2OX?Om(uCNIud-SqyTWW7JkU8rA;4Gc-&1L4FRcKE{DcHWU&$X=LkAB4&v;<8zU&p%86h{-jjDl!k6R7-T2}LuB?LYd{!)_Zjg>{D2RarCLM6dA81UB5;38VBZgoOloCKP@prOf%IKz0yc+%KH@`D$!yJ7jpv=Y<u*DIoG2FUFWUP?*0Nj0CW*XDsqU~3O%9!6B@)u6ILRw~i*1T!;Q6W5x^K4)nlrttqLwLWV}ND`>3FLgG!PaJg|>#hF-VuDl*lk6_}A6HSSbLmo;tK`r7R|=pU4$s_kX(E<+ZZ$)zC&2+nhoMLdI=OVV2<*7V^lG7^{(OYn9=BNDdFjG+lS6l_lcbsu%PNk=rb_g)rcjDGD36U6{{#zc!fpfb{OrE;4-@y#yj%zdC#C-AF6Dt0H4N6uK}hp}h<G5G|k9yVAs|;PZEld=n97uiXl-?FCKM`n8=ym%IF_gOrNMPbl8Yz3qms%Lz*ao!$W}vbqiKI>27X;1WIE!X;-cO>d}~<Ty&skc1_xCdo@kZJR%;J{%JORLV%B*S549u(<Wv>>63NYb<r4%D}^wpLJ1)vqnv%ceKd!*xhKIz>=_a3KYrA0>2@F>NkdRDXjk9f=(w}kqHu%ei)flRpCPB2{t3iSg;Bq=f>>YM9)Tk5~&~v(H{`hvhQo&C2Ss)W$(jrj79Lr-`w|VG4zI4hx#Y9OrDhz-mYo&0grV&BxO!;FT9G1yeNFKuXnic6UP+_%@Zc?@L=+;;WjXkkf;(9DWdDA+eRJ<o}i+4KaN&qJ_xTp>_s(%A|^M|Qc;%v0q3Pm4a?6}PQ2tsYW}%y6oc5pa~u}_H!Z;1-e)+35~eWo*`<^XIBpu}JyWb}4>h^ZxH+fZa3XoDOv~M|dsWsjv`<WW4o^UP@H$rshJs5q#CrS|sk1tR7}FUdo;VYo3D7JWmP>yjbY@$p5!Gj*f<1pH<ere}0dH6EFrHSf_oFYC&2`JA?7KEh6?mUXDe%0f4({ikxM5cF&Q6;cmGnY5h&X<JTNlAjXtHlu>T=IKvW$e%%-#a$B`NK`O=!G4p=}0X@uF)?DJ_V#)P}LCD77(JuAszTZ=}X<B9C`;c$f9=kHgr?qMb;!D&JUwcXv=*upWUk@1-9*Rhuws>#zrQaC}a|eTHSz-RYm9QOLq3@FH@$u3jTN6e1^K0zrc~0#Gn|gc5L?%gP+1r=Nkv_v<2t{#ft@Gj$np5q>Qk9f$WZ^IJh3IFGb^E0o`%xvWe-423ITOSJ2NGyqPBgK-ubC?Mji(YkVzKe<XQF>A4%iRmI&SyYiOL_J}(L#7bT7D_4p8HjM7=y3@erxHMMKMUms+fA-bpAtNc0BmHwf=e8=C#BF((N9WH2|$`qFg+(KUj4q(gQvhV6e=p5?_MR?86^9}3JmsqECQ~zGq&MG-^;W(sknTRpoBM<K#ZJeb6h@($yBPbI8qW25vC}Pq%hjL@)g2|MM&A0$HlyGU@F_iKWGS!Xob)t6WxR^xWurUDRc%XP032<c^V5mOjTj9E!#iq8l<5!!-VsmS)E~YU7#UQ@H5%So#x&MdP$qQuagN&!~#zPYSu#2sp(HN%w3}59&CJarCCfNbHe?=Xzmr$sVcZ*62O3`gdE=7R0iE}ScH_@Ag`jmrXn$pPA=|aFpu)R6$HC_$CqQH)+NClShp@HAekq{IBlRP^?)Y+JF^Zi<v!24^~snHxx*+|h1c?|174zpbkqn9&%zcIg&B6~_GN~$T<UHyc#~>m0fbz+0EIh`dza8{B2B`I$`s1_Va^fv?8io}DrmiTm)V?JwYoig1GQE(M5cJRMD7E>bSZDDvcB~uL%mG;28_PfEy#UxW1wLt1#DPavdvS-wh&_p?k8yQ>pz)NGGGlig_9Ly?dse{K?cD~074%NO-WOnDqcp_+gc{MXMmi>3D3W%Mp#qJ+B5**dhs*iM>yraDzhv^f_nc5t^QKA^FmWPt4cj@q3{xEt}-r`#@Gtzgo*953gMHFdW{zz<%?a8ZMpg>TGu9pu@14(8M6q8V*O<}`sIUHeFc~|7Md@#tchxBNZMcl*)7>DXDq~A=-^rWK{`P^gT!?oZm)}1=`IS<7mE9wIyH(8mNj06OoI+;CY6{L@2w+OKT)T6ECg!I^9^rVIdJDSFfM@-?8YR&XEsgCREBBQ6U~*c1Do}R2|=LB+B@hSMMSKVG3quOxgX{*LMLi6J4Y~VhN37PAUeeM9cp+xHWz)@n5&v;Cc&a(7!yZ{G&a8`#}MLjLViOk=;eFe9oT#thh;ZL6OCeeFw*=ntm<VIpsHT5b`*YSja$}lGw*6eZP>{Kl8RjUChUO9HcwY#4`g>KnG$$)t|4>Lt996dXK?e+j@Sa+qDTQ8whnGgyhqz7Tj->!uIH3g!WPzFq7y$QuQnd^?+yVbQgMbY{hLTrjLkA^^hqah036HI$W0Sra1l5`+-_`^u#L?Wy|?xRRFR-{-kUv5ZRjV^*8&{%AZP4q3(J>k+njbtBSKp6m}HzH9awSodcazAo?!UchSl$Wf-bx&IQGf<?Mkmu0UfnnEekx5suJ6RXB+3Oqkf`(>-ZFs*VqnfUWj7|dgJI+lej08G&Z(J(K_|9La7V*Q?!8u?~@_Ie#cfa>*yz4(d8<zPsPq2rB|wtcMfWT=*wKo*P(K?B{ZT|X^w@)8>#FM5_nA6f(}@0u(I9!g+!ZN+0T<c$nbrtN3yBPSm?C@FHqFc0*F@TX~>ZW#;#TEJlC!&H1$vn*~MVOx!uhuDt)8vPqb_T7^MKX0Q2c9W%QT^8HK~x++_*)M<lpTW6-<8i){&br3^tlbUPWV#JY62N{?#;`jnL8*_S7<lb=(J6UhS9Flkk#=A(LTk+*ldOJMw(n<T<)Dc*8~35W7=bOek-9u>;_^ryHt@)!!pMNeAp{BXq!Uxiq{7?LV-3Uw?l1688+;I4Dxxk65ku>%;i1PPEw?5b(K`++it!Upb5z#AMx4LW-9SRagTB<)@wRxB=rYLZZ*i=I(gNS;HcXYyQRo<rpUW2Z!KJ?0dpUVr<XqJ-_<B&D&@Zu(=092><xs_v+Wurju?^-KFOnXh3{j}t|^W&3ibDQ{r6#L-JyU>YLy;rx@pEoz-V6=-*($1NPq0!$@})VjRH_jMX0#~oaDJeFWg(vm9?x7Dyr%Xu65sMici`~c{KyFL}Q%l8pZO=aOWO=`z=_Wps4p`#0WeUJZmzu+(T(>8JOyD`)Ap!=Xg;c*J-dADo6fq~qmJ|{!}65e$!+LP9H@NV4&S-KhxdDsqO^#b3noXuQ-83y8FVH3f|PLCO<xeM2M_c~+;ecktOE*lM!I{w2Sdc7e@k6k#`Lq+m3m$O~AjwDmT4dWeERjCqP2~tU*tc;ndx#YWB+OaXJ%)LqC{Rb{k1rF0;<by!`U-{7M6bosU_hCfULXlt?Bc(t{jp);EXJ~LPlf(RN<7Y5)>Vr%nL9B*_3*hujH9kWg5@&Q<%H#R`{QA?U&#&f}_pjhG9}?u(A76jQmzwfouf&qY-H7{3J~f%XB9gd#g;-_+4yxFT;-7`hDA)KIyFo7V{dS}n?)GkTUBvQDD;Fo)3#FN+v*37l{;{_qWbE1AyG$^`TlI&W{q}Lb*wp{*OFlt%+WvE?h*D&?=mU+5XZFQzQ1JtEUX?xh6E3OLuFPpQD{rOh`cyOExCQIjaUaIGBVRth`})yMA3THtso@z>YtzqlrOkx95eqUkL!+vE=2AD{Qhc1qEoA=o^#;cj))5>&06WE~FV8VL)k|?6M6RR6L^Fhe^<RGf;m7a(_T`&D|L%0dfJeyw*>+(SbQ+QF)C|3Po*#$Sek1NNBWXID6XRBqH$$kTx4o+C_G`^!?V1+<0xU6VRLV5UNHSx0onts;{rUyg10MdG+FEpYDIF~!8nMF0;+Pcr+jbcNTqGtxA}WXh9DTDJ6CxRr1U=FJ<&=(fC}VsAkRcIed02XHejR<Twaam;St*(6?A6mWBk#D|ri%4XJ=SB?RoBIbCn0+z7U{gB!-jVJ>E|DQ`t;*^J>IQ*YSsJ?Yo+4qoskBwb|0rGiSIl;ge4sP1<SqxhH5kQa(CXGW0bgw(VW0y4l?nYe>C(+$_GwgK%Ec1Cu1Dm^@l4`I(&IoZXMO4qh3&k{#v5TW@wHUTvKX@Y8p&%^DOcZ-P_rhdt0wLBt27`dcU2(8$^@xY7TQVwOP;isg1k~Hp5evGV*FkyV2sAS12OD04G_whto_DeJJ9YH1m?5KKmzrG5On2r~(pAc+HtIevBq;Wfv%;@~8e3w*_jJHUodyb?rYWi{C6lNnPnZb&<R$*F^FXjA_vhb1fVu*2@YWTtJx#k|dO(n?h9Y2$+tz9fbKMt`Sr{LYE(EFqw|*L1%p9-~M{N{_=Q2mZ<j5igHxuw$ySq_gVuJU*`~cToF<Zc1vw(Mfu9>@bs4NOv)>0i03~ZnUxGx>Y;cA@~E+wiyn1KHojdmZf<+IsOC&vvRIs$zCNtu3EzSCQp>0#{1pn2WAMf^=JwL&=_^c)l%X?)oe0$q{<3y*{~}fs$BJ}O5aWbI?Iq+OfCU0}8s5pQdg=ao_a}j1pZ>}Y(NyT|s@1)Lqvcy@NIef1%U*JU)*O{;$t-4wFM`X`at|R&BmkcK4v23yL2Y=J+vL#~wCaW}yb>_FC6?qeL3@V-8`=)*b`3?V)Lc~?as$Q6L#kx$7YW)`Y#Lp8h9tJBFc#vUKCCb1jJDh2g`z4^k15)a1N@eAgc$U?4z*LWYaW`O>YW7@nb;qL5hqA<_C7K+Vbev*nu<$14o}mt8AOCTS(XMEvHyds<P4T?d|v*heJ<S4HdDTiNUa89DySC1un%P!wKkE$%=?tu3ykZ-?%RT5o6W?CeXmZCF1F{Pl`~nMkLUX;_p?A=*4km~m8*xlmF8)5_DxPwrfm~NR~C?pvT=UAerlm#yyLRYY0=9;tZ3iEbQn+(cKK{GIx@@`2i{Goasa-(Q>6?M3Sbw--C(WxNg7x^g86Niplnd!G2wlCu68%7i3OUzvBW--cu^d}E)1q3B<&$hirD7m<tZq|tpl4yxnL0Jhe}*~U#s|#(pLvtxtvSIWEx-CZ|@tGTS9)&l)TWLi?!_Tck1`AufJV)6h7>NY>!^3NRgI#Q)KG~odxRzqTU;`In{ml_m~&B3nG=&wjVN5)af=eDZSES{9v$ShVvXr+jzf=Zz~Tb0;7~69<Ka?{wrx{AE<f1k8Qv{{#q0;;$hm~3g&?RfPM%}%t~ae_2XKvgl!1V=FkW}jv2b&DCs5o19o7YQzEQDvpwKLJ`wI*kMDPP$Zfi*!Jo|rZ|lP*HhN9t+hLS5<3WMB5A?$9mYEQzv{UmNFEXlSy?fv=@M&3(+nn-s*Ta5azMDNZDtE{724RuBzY_t!wD>_J{j?zg9oWkm=nEqxSQ)Y%13pM_NjNo5T@45}4l<LDwNQ{ly`AJm3b^~a(_eP%JJ&r85i*}EvR%8Q4pvf;1gR6T04_@TGe$#Nr!@z}W}2@e(Awj1iJLqgONdU+Y}>FYB0b#0S8#5vGTi=gL-`G#k4sE_tfDV%dpGItV^)heBpZ~+ykgS|U}Bn5)lH<WmAf-`Gtryt<gda@j7%-;_$ewsMI<xOtAYZm6rr9ksSUBtZb(-SVK(3!_`XlBA9y>rb^N%nu1ixV=VkrA?^3Ya8LpUXR!$BS)GzY>n>>-aCe*aumqPs0;L>Fq<$SUnyqP|T5#1Klb+OkK<4^`&Exi=R680dp4~%fQ#5)mgrfYUx+5Ob#LWbT-zIk<$5#`KasJplTcObgUX!a*_ZFQGXZW3yvU-k^x-H0u=D;Q;rX=o!?7N-Lw&x2;Wi|!TZToyLmn%d*8Y0qAO<8$x5u8G<__-d;dDFSaG1S~~=o>v#IbC~2SleI_$>CDJx9N3{N6ke=69k`AyNR5!}sLUXX4y@x{XguDfgyeKRR@!JLS9{hKgdAE;iK1`&rr$$adws>m%Td3sO%N4G98LQdFu2c}Y}+RKcmO0$4yN*4rgeZrMS#v*Wn6Q87gbZ#+XCHK_d)JJ@&XY2{B%P_m8$wvO?TjRSfhOVMCtVN4`LT_6=_2w#84#KuJHHue&z$$1nmkINZdJ*FdV=vz%3f;x2*(~F6?&l02E<=D<bW0^99Ovy$-9Z(J**08y(lO*ycV#luk)@?z{PP1zUmj!GX1~tf?B1Nl0alx`Lg++KUmYQgm?(_^iE-`sr)~Ju2A}p<0PdkH5S{o?h#Lvfs;nySi|3MKK$@)I)!UGU<+&VIAmKmA7-4<mPM<=MR?I;y?1dwV~{=`IwZaAL3$_q>PrO_=`g*Tu8(6EER^jg032p?AqtME13uOM$e*{M%?>}PR!V(OYW^R%y};?&1hRSWt#Z*UVpl7tYAF4#jWol8tQah6zOsHQn5&CAznAuF^{0f$cD;M7y;d}mrp^eu#N@5R<14;k2#&fScc%C18GWwjWRqR#a=E7S%~-L6<=$+`9WqVEIJB0EUs<@R}t;TSq_pCWKot|_SjjfLsT}`IY_K@dY3!T=Lou?ftib`)o$wY+8(T^+!5~{qh!TyzCwIA^_9)(03xSV_Y-cl5cn1JkAT{(SLWUPu*xl*w)e^uff9Pr+IK&E56o90Qh9gqe5vSL3}Cq9kN{NA%rlA66$x{&-_U3t?chEFdn#q@C@n788!v>N_&<7JzWuAv1DgH$FR4odK6<n-aiTnp$b;Dvps)u(O$4h4bKCvBfY(baXy}$EQxc+gKa~raqXtY~xVz}uI!xCv@IN45B3hC998jStreQST9k1Inuwrpn;eH$XoI0pjSL_;gXpiJ!x9Z^?owHBWm2V!_5(&8wT!i&%@<1o{H^)}cBioJD)#@*es+Xma(HO&xenO^Wo!PUpTkATvPQkg5A&j(iJg#y<?xd9eHG^<(fd10UJRY7jr-6!oVds3PzTi$-!;|#{;V*8UD!VAcW|zx0R=I+l9CjODr4ZBOE#OLen&+>-aCyf(_;%V=?Jto?Kdc*OppQ+W8c<N_5S!}@`{vKv4$!?j?<PW4fxAXTbK`QA_k{zW>PbKKO{;>xOd`R#3w@BO^en)@1jsYtblR*Wb*RP8_6!!AHX|5iK|)?($dc-;q9i6&^vzV)50s`%ttCUBSqP~(40&wHh9A)tx#?RW_M)~zQ6&&Wy2r<ELfh1BLPRC@P)IS0tZ3=<g{Bf?Ro*16V9soU7Da^JnPbw1D&R~^2RKvS%WZ>nsgh$I<pLq;()OWiBJh#1vumwbB9a{jwZ=_-7YYey#99vj6f$aTM>Su$Z{In(FUWamoxBhBtGWp30MY|Sx(~`si0MD&_k0~+)K%S|YoFKtV6Drodl+{q=wc9a9qcG?3}toNn}=3cF*@`*uqA;#a*)Dx>AWPKOp9muOW%jEWPs&`SyQSfa+-VI7fMVa&r%eSV%{vP?UIKbWfnEPI^S5I(Xad#CaX8Eyzk{S6vY==-$_LVDMf_rLzX7(G8ite!;E7AsE0x%d6D>lGLvHH0O;jSw53Qsz3-QrY^6D;_&hT$XA6GYHFhMY3QRF-Dj@cniqbazt1DJ*?Yby>u&;kGhD3>s=bxk42`2Vjy}Pgh3!GXTOs$of*<$J(fsJn3&_>rN1uy7d_CqJLxN}l+KIYC8ooKSeYxurRB}Z7<;{tozQ*dCUlc!ZhiQO4D5ObYbt!iP=T{imHnt~uEYT6In1^+X`wPDJY&pJJ5L!KtbP6P%vE)?ns5qX{9oS>vw_d=l8vX;2+qVzN*D#+UQezgMyOw|Y<jRl6m$lAKv5=Q7_R0=I#%XzHhD7WwRZpo@^pRjP4zc=RGRu5X0bacWE2xvN1J8+%DqNKq?N*%MJjD`rgZw{==eu~g6AO&B#QTUlb{w%BVXW5<oSI*nW`}omh#9OfiE{bM6ym+Q1DB45VeAGiYXWICnM`7ftU#1~Jt2|ouAKCjk!<4aI5dw0}4({yTLk#;wzP&@#1QCvlh4z(%&h50%o!UIadly1Cm`abhsdsReBCIINz(F7`OcPl~q&vW|uCsuNMoOY+Q17h=BB}a|eqQo0SJr2MuP+1f?6OB4o0XbUs)Yl_1p$c@#lL;QmZh{Zp%DhQdoI1M0wvpXTeL~mm~dDbz~uresEI6G-!EfAFiy(0MC90{LK+xyRKm=K^&=)hQV$WFVS!J%&LmX(y5q%^2Prl?^cl(;x0M{#up}DbksjxRi5a<EY2F6ib4CZDiLi~}l4(R1uK3kK#QU8c5OAiOG+er~U4AInAyLfEe--RfPtltpRkhxm-U3hV6F7u~VqX2sDU<>fm8F%wg#wc>uTge>NO=aSM2>Q=9#S@3a)lhU2N^%_x&T<{y$_eAnn;TMdcD;jEm5He6--(W1zFdEX-uck!kEb$Hm(d|a~SxwSxQT)ww19O&+}$U7m^f>xo_PzxxTUmxTtbX@hwe-c^&9jk)q>byR_t5ICrsk(c~~&2EXkJDp6!?+yHd9-YZdTs3}A^OsIco=1g)9BcPli3_K-W30}x_zt5v>)Yca#>lRs*fsO3?n*i?l*I3(DDj9I<f5Zo~GdJ~6juDcn407g%mcQ+Iy6c#9nwKbbfABM>V28$PViKt63iZDI!^2}o*9mK<sDl!c7>9C*Q6K{UNTN|3%ISu7KF6Xi-qeptN(^yR;#4NyPejnJvm&CtGj(5Vf~jV`&$-iuZn(&iTObhi`&DTj&31mfE+IW!m%6->KNom;L!q3Txnjbnjf$v;e+>c}F#K7~%us$ow0K(A0H;b|9qA%>a<{=KE77tyePz>_A(XC7?S5FFNRi24p?$wI<bDVBP(^b}11kbkk@~pf7h)T9C;<+g%kVUXdaZHwX*dTi1~T;H$p$`GLBOd7NF=3~LqF+Bf10@s*M0LdJqO6W`T8YSn!y?~0KGs-%RnR+Y#8<Xz=w+}SOBE)D!N3F?6lJpMFEQTMATtubQ_N|y!8T!^?3Tw=7kszF3<2B$9CwF>I+d7pIRB$I}~|t>u-+iEc6}auI<pP@~^DC#g|fGm097|-Um6zWz)RqfL!Q@D31JT1(#=gj|yUQ24a^aUhlsI616mM!5-0JR+W$<M*!=oCK$m)!P{?Y<hyGHqd8D+i!S<TM%dEO)2OJt4}}^vw59uy&`WPEYWuB33g<Z)`(c#TRT#S@*cT2Ls#5XJ^wxQFb&c=1Pe$oMH<<-ZmS305V(ARIp;jO%k4q(oF?<Ae%|lFbf%Lf!xa4PAQ{AtcFcKkV%8Si<uVc&k)~F?Ko}b|<AsJ&0-hw5f{+ev<_q~{9)v`3~o+hAqL@!|eA*+ds`^writP4;gqx*t2tcRlMxpgP_8<j}_(?-0c(ythBBVUdg)mxlk!^APZ{=TJ8DUQ{461V@wCM+&*Ts*pglT##EqEvs%;X3aLhyE)o2|aYP849^`DUe+?U_UBZGs#)7ppv9>kc&sY%c+%c<1sIA+KC1F#UZe7+dAbrY=1-vZ$RD0EQDTC(*l+R{uQQ@f*Q9BQ<#VYb1LfZ{8Ua*W9v4wk*(Z^CbpY*zQ_~ATk6yj`1N5L8Wt8^*~fcsWdDyQzLS+b@Cq-}H(<1F!j;<rxY)D;qD{QWesTUf+{&mcO0!XP9Yzn8T1UgI2VkJe@wo8i|105j`-7ywypA~F^~^&8m5}I%Tz-`N5PrCvA)E6u$Fx8q<1gj_`83G4d5ZHCRvx4V;?zo`Zs2mW7kCST+hErDDYR=u;)-IuuH0K|sZ88l1pruVSCu>vgNf=It1{nmBt+@zK{eRD$58Jt9|XW^^0`EpzkKhnue-ajXbiGl8|$xyX=vC9R6ajp+YNW$*^JsuJbCQ8Fss#HFFfVMwrL$@g#sT{B0JjI79KO<X{UNN@$_8GQR{&Q*gD}}ze!+qe+^O?$q|#V*=<wtP&R``NIj2b$lNQmVlpZo0EVi9#g$WhVTGH+BKs$pY;?SqG$Nw&Z{?q!z>}9LbJ@_BoTpdtX)Q?Dkq(v%Ubv?kC5V?feRYWn{6Xr5TxP&Pz&}No8&K~UmgOvU<vBkQm1__VjF%?K6KVb6H_#=6pc+%6={(Eh4CpEbNxQ8_r*^J|=r*N}P!b7)p4OpFDn%D_ayH~4Jx1$tfx*o(sfEPsVHtysO;R!#+uL;C?InQ?g`7D2-*G!l3fmF&EJheDJlwIl)b*B-8=`=#Q)iN98s3_jHFf?GC8{$Xa!|X#hT7`V<>X|rJ}|!TlBvx#1Mf0x%sM&R60kt*L$95*TEa~<tzO@cBur%DjQzRbk2Y{i{CC_cc5dG0Wt-%fuI6Aa679UQ`#rnSY!+LYd$3;#208Vc*$D!3;d5XEo^?ksCICo%b2LBjeRyqiG7^CWf)4Z4F6$GUrEUwqrVz)r72}QFa8$)2b1>ytg8h0Nj<wd+T_@Z91B4sEx_X+Tk4dhVr%(mPb`X^?quO|>!n0?bf$$<{63g!VMmd{&Q-YM+Rgt-e^A_3fcf+0ZJoqtJ3R41p`=XX+HLU4&QPCdvy!?ztE=Rczrm2)9w#+vacfpPyk=vhj(z`09#G1Ot%G`)R6E&>`%LuX)RDgk^7mJ+0n`^x^-q8nAy2fsj`<g&u#~@l1rD@_vZ`{T^*Qu%j_em#lSG7$troTi^s}?#lJ)gkQilT0N=M+u0SkI9Z`GrkF3$WMm4GFTX?)}J}r*plt#y)(anGGnNVA<b;ph!$&871rcgeKkPe9ljq8f1hMTRlRh&BXz|-mSwHXB4FyB)Aq+|J3Rd_h#ee*4k|gWBRv#$wz0&>F%W{$s8ksi%lOF|9HQCzy9+&Q{KdL%*fAtl={qAB=^A;!4(~BEzSFZT~`OJIxx+sF`Y@YM4Xv;bCzEB3?T_)7k(i2w*BGohtAp%)ctMp%QA+OJqVU8^EThe@nSNPB#^shq|EMciMiNj1EO}>^x1mBOkv7_`2b9S<x$tURRbga=1^3#g|W69j>9P)@6dG^Xo}cN!Y2>R)COjUl>XcI(w!b0KHFisoCass2(Cz*am?6?06uVnxLDW^kL%za_4UX;{`K?gPoF-&nqS^O4a<Be4!i#N`m_1{!=22Yu{D9=-zbkObSe;j5MdO3uLH5#?S?$u*07DX*j^Le{?YA;R!Z1}a&6%*oL})-tv<4AW`AIhmGgrLAwFPndiu>l{_^qt*H3Qx;B^+DzGrwxO+RN84H#?LzjI8K*%T5qq~&-mo1L^A|Mv9;$JDB-=WieI5@>T-j8JUU-dHE#NQiER(4+m!??3$b-QT`^^XK2qU2g|=KQH#rwi~MenZ;H_&CsjI`Eh3LH{u#&i8yFZj0+_+g<=dC>vnsu+po#R+BGfy1z2KKg2|e(60P3db&lhZ_3IZ%4n6!ewKcs`Lv$;4o5tw$#W5))LhLef)~dkgl}5=)tIgQg06vj_s}<lMq3foQoPZ|)8Ir_nX9RKdxz;Ynlh7E<smJNoW;`jfYcBWd$9h~;<*jm%Q&d<jYxL~+=!cN?)6YNr^y$a-dc0fr)TTKydSZc=1=@X_BG#$%^bkG1=r34d5Xjp$g|Y!t2G2Q0iJKVB2`uIyqb>ZSp+_Rsm%;_qL7=@r)Ztx!xFV&)mv`mXQ7t+IN%_nE(43mVrl^P)1x?}R0o{k--p;<<+j<qX@3bHjd#Lyg0&I)CUiM~cb0>2wU~Mn!M;ox=GD{hGwS=fwJoB89;k}-7<jnFV;jJ_x38bbdnU$u`{)t~q{x&QpWMq*uW&D`RW`xbsJU`zUr<t4Otb*%vlSEBe0SXQ&yd>qe$G1T1zA0+-EFM86JB>8>#`@3;=vfl9bwP^JIE26b^?Lnf7k<;^MpLA5Eb?#ZX@JdiU-I`aC(cJ&B6Pzx7CkITXtai0Sv#@PH0_;aHffzhd%5Tjtwq#;0eYH=Cs42ZSR1uyOhV)C!ie{E<aHhH^Sh2NAvKwJY5h1=4SU+6qRqw>d*}_0h7b&V)e_Z@YA;bxYxC*>>jD2~lFQRk!nO(hX+lIS78YgIgDvn7^|nZuA~KxUXGk|Vr`(|pyC<SgCCYFBn2T#%HhU^cssN6!c4=Z)1RL2pjv;u+=u-RCIJFQNJg#k#&^!fYJ-O>_Tht%{c!o%<2OgMxXIVkDz4%LCrjdM^w!Oe6P^s3Na+3&A+U*H1aVvv*%x%HMjr(JyFe;P7?&O|EhX|8GR(c{*R-j);8|pu^rV0@-=~ud)TId(=xU6$pYKj%?H5~h!B=&5(re+k@y97XWsizFSyi*CwTt6q=V6E#?Z9{}@N4rG!il*BV-Pawcv+XKGZP*#289;{Y7Y<1`o$Xt1yL7P2Gu+d08`zxIQ3l5EAy1`C3)Sfz->F;9p;8%N*M587sA;yFBC!|$x8sgsO6dJg{r>g!w`&NeY>!^ws&nB|4*aLmhZ=N3kb|*!Z_KdGtNVM*3)}@^B-Rg^R?=M6uBLE<@U_5T#|-@o-&29SM4%<iDURzXXO%9-B@n4lFN+cUg06PJKK{y&93AZ-^IO3j&>zqbfih82UV8nwws%$2qq8|Qf{$Z{?h7`)M1Q~zELVSEE6{8Y_#lY1(A47nKfd4HVy`nH__HYgwmxiP+xtI+ho5Qm@V@HIi?ze&Ts~@SMN2M1mP1m8);-|Uvi`L>)9W7B>ln60qb`!Pw1f#*mgDb4K&&Z#5VM_a$h-sgA~3X>f9L6X+Y5UPw26W%!6A2dxC$~0f)!<tj8uSJafSs&PG+F!_hrYvbDhx;4|{PFDBC4Fj)`;{snW9Vxu63WICc@<LGnTcdC)@Rv}Y9o(jHGqc$^FF^vRiR8&<SsvL5(7SOw?Ss&p86*&+qv6Oj}(qpH1|^!JgAIsgsEC?ixJ>WWP(V2HA@PeAJ?{rlXVVX66Oe^U~Z<<vqA3$e61(qd%tA&JBFKI-|B+7Rp7hS_6TLk~5r^<W!yQ|9)3j}_Wtof8*JbXN6U3R)jS5w9prDHe^k-F!mBMKY28WGj2|zxw+j)Eu-??~NFso<2x8pjG-#+?2{VAO!~P)Js?_i!A#aWdkb&(BWpfX4hSMwJ~q#t%QCJZO^N#$(A!1>MkxoWQguEn(N72Tis=p`$5_0mpub^H)4zJE}{M$k)>vFy5C?63_|w`B2xq*mcrf;F2Js7|8XwBbwpjn=CRQeZF~maKnPDNqGjb+C;4gwy>1y%P*WtQvBx^ZStYargp7%FL{!nV^6NU@g$CkXs^77$bcB4k%I0`oo1nF#u-iW7_gGeJfk(!cU>}fhnbjsxRL|a%1)az8VqoE<tY3eVdt*9?UDpm3aX8YX&aYW@8~1IyyJ&IkI`LXCbggE@Hn(@D8!GB@o}($pJcn+SZ=djGoIfZs=(>oi$QqMDf+A6y;=N(QMHsd*&v7&pNC+`)EO3hwHp)SQwClT?^2i5M&~e_Njxtar(<^34LG*ntLzTX#ErSLsO@MWu%FA>`wjZc3lgLE&j06PKp8G=gGSXsZGOpo+1bmJ}=EPs#BJXXNm#d&loth!RLDl+ShuNQ@AiCpaXaf3G<&he6F=bg{HYT)qj?yp}XZtZJuQb_3192U?-eb)>M`b$PUV_=kQWnjxcu2=a1&i#H<Mxxs$)d2PammUt_S+;XD0Xg5`nx{~yTo_2T`-gBms#iCSVwi?6|Phgk51nQ7=Y#X`TD@C%l%^Rk1&=YcnLtJ%<p7Csf^}I5kmYzNhdGAR@)T-aua#OX(}+ui}kv3mi_buU6JKGJ;spgLQIh`-ti>`#oZyLo&t3EL99fQN_ptRV7sVFAa*$%bY1SS>*g-Ismp5#TNfUcAKMLMK6lh3b$hwiQTI6?njv3Q<-l(!z(V_iP7x5J^}06Fdk66I-O)ucy<YN#n^8){B=13)FR~*{bF^N6OklIs1c2=>o0|l#$i);{#6}(edf;vjd(H$3?jHd>%|n7Dr)ZIg>6teEM-Sn*e??G~#v`3OP@XR<&=tx*(Paod6BKOIWWM0`6dtBM>I&_^?NAi(tij;Ts~pxnIIsQEWJ*b5gg9LQ9jU*2Vg16~6sLd#BBdycSSiQn^`a8c)FskC;EgXuCm0e*a(yTLySI?miOw#BcG%pg-m6g}-cv(+_DB~z9ncEehk6j73L#Vb=bQb_y&1=bPKVHSe`(aV5*mYz(c<VQWEyUm%{fMh_qlZnbcc3)q}AndX$*3aC3#CT2=~17mtH3S@Ps=JzVy2}=P34<Aq;xa0aroZ%^hbq0ug68ymI|TE;1*F-NuY55cqftfGf-ahx?Kdr8u-z#VoQ%+sEopsI-{DbT-jydXU9Q)<J+wO$(RNon;f@+^k!ywU)S|<$amJrvf(TI>c6m;+bYb5Yho2O99}3feDaw!ke^d)vC6rWZ1U(`Z|%YS0QwylqQArF7#sryV$J|e9$GNa1n^2T&n_Oi~N(yf&vd-6tlyM=1gB`4>6vi){UN1gP@yEv|!om-1gDXndl7gD7@#(MyXN_#5&3a264v@M$Y@J>97Hh&swp>#3}~$K7p>0g$1($ej!uFHevB)<<>m#I_UPCo*d1*o_8*~C=>=I`bOdo$}xypOXc_W1TYe%&0YgU85!$1V%8U0PLj$7!#+q)MJ`hzLWUrJ-FKtB<CJe{uQXcl#E8o81M5R{EWlvGlq;3PIL)c<3n8J9KPc)SG2g4IOL#f#D3hnjt@&FmshCBmXPD{Ue8|3+^FS2jVjZLu6`vIEun$R*v|o_W`y3L{Sh(ax$VnQaBScJ0ibbxK-5+^J)s|L;_x)0nSTrZv=~ZuBEQe_j<rp>?&k<WHpfZSct35bkY6}Q|u1T*i!1IPyCJ~EyUj!n#si4wn#`$AG`mi55nQ)v_5%aNBChwzr<3p{8ThMnb`q%2hiGJXo&!6Fb4^ys?&}l;!(gk@e%-F_{KHT8u><RmIonWd3gn5?)mM80q<}ON4J<)<8Y%do(P(YZB*y*vbDi~Q?R|CM9S1c8*DQ)LmoiTEC1duB67?BtYB=!^O{C*teR&;w<&*SIGmp9=@Fh6F@Ic^^2CrP7(mZTCWj)E|K(caNXQiiN9b{sOY5T1`bMW_mp?mp;8x$ht{d{)2B!1w)E&g%kCef+93W~bP_4Y}{$vpv&#4ebGMKI#FVL(n1s&_<qzV=4f&NTOB$QAO0;{2hnPW(WWDt{sM;A&1-{*MZ2^Mb!FAL~Xm2=1y();5`E&UPZ+t+{`FAOA$B{Wr85`6s9Y@{;*(xW1SK_BmH+S@hQYjz}1ziR_Ny?kLzSz1o+r8)JlF0mbR`B1U3ilL_;R%394LQHZEk;AEBQCJ`P+#+l@4qp@NnKy)2)Yr9d6B(0IR$3CS;7gACc}w8ukT1J8bmN@TeZdf0C;r)USxFmYV=FYs||*SUoXPM`%LFbQxCiJEpQL9ge4-V*k+0Lep-jlgtjT+S+?pcD6WxO8WGm(a{~qU#I)RWS0NVlzXk5V|+&&QI=sHiR5VrHQP^0~3IzEECSU(C_OqiB9!l?xXBRka9m#5*wxMycg{M<?c(CBRP(yUkHa<GHW?fB21zgNysG9aQaQ}{}%tubXB7(!^6WP8<1q*i690*=NcJ{hkG4zKy<3UWK$jRZAesiomZ?jn92-d4tvPD$Qgy$)6@>Ech*o@l5x4&M5gC%M%gtNuFmFA>6=hnnmzSwWloLftTI5psN;?6C-XVEkYgl49zz{hB$O#J(jEg{Ix1A0c$9X>3imF4mB(DNlO?hqdc;tSd5xPK+j<As+n_BxF*_|!*Ky0#;czaIV?IGzQD?=rTQiL+-#>1pl7Y<3F~_GV!zWv(sk4`yLznfIU$=Y1Ia_2ZRjy>vW}OE><uN85`135AcWvZAGr$zkZ4wd~`!|3GPOc|4ZO<V^n^)#*65cfyC{0zT{UkS4piH$)SL1?TL~1}kItXx9SL^GxE_0?QS!Og!@FQy4&!U2DIcKHwlW^u87yccop2jJX^C6t)1ero#;qRUNdJ3&|+N_3RG-I>EcaXB!gue~K9BZ=XB~vYgD|zk0Eq<1pKrJYz>+yGw0q?TFwT)C+M~)p`r@BThL+}=-4nf$ZMbmwh$DTQ*A*MKJe`z%POs)>xKS|yiKbGg9LlR}^kcO8kq}_~r@WMH8s+L-oCzVcK1!kU}Oe7lg86lTdudUMpX}IpEx9TN7TmxA49OR!7*#lNPsejv!s*d_@$0fyn{<{9ube-~T*q^KTaExP4_FhNrOKL+;aa_6pErn4V5zBW-;8|-?2|QU#f!}P+x?yBzwE@#+lDZPRrPY`hGv&-O*G;7qiC!1X9GO6&5_Vtq);DO`fYm69u%nS<cM{oEh3UCA^t$lO+=qmo343zRpGp)5)Eer>U-?BQC}0SHU|)E~Dn%Dvm$^?zioe_xl<_VjP{}&$WHKxxF3Z#eN)i}^T9?qBeNYN8`Dr2>8{l{o=XuAHz{J*sek?hsyp5+gzU(I`5NbqBfeXK^3El~NK`i81WHOR($9<1Bng1u95>BIsJd_T&E+GJga)HVO7!BQel9Kbl{nSQU*t!k;jmnf3DaWWo^j6nVHjx=dNL;|d$Q{0_{`p;_CVz#13b0)3Y8A*mW=rm9L)3;&Sc;+!meH>&AG8w7R`=d2xCq!BpaA2g)4|_WiU_L%#G3~5hV2mG18WEE>TIFz2*o%7`VF&YdauC*ir)A~7+(TOxUFF=3CyhNM)FhhLF=R|j$w`2ru%!K!{s{Q_W#<PkNqOnf(gQcttMg|2`0n&z{nR;Ot$3-1Sz&P^U`#&(W)=Yws+>`UWKH@Cx}IGB81w|7oYp`?eqTm_D7sehPq5LA24Urb$8$x-2E;z9Ss3m_gb9VR4nuh&xeIXM)$#XFtbqJiR&#sLjy*iC*qZk8u~G8`TpXP&-GMk^<n3Gv9A<FU2X3GKQE$QI7(XJoB!h{jfGr>F`1U0{J1^f3xIA^3hz8Sp3}%N7+v}5W80QtQd{ykp}(eaqyW#uEcRqkD(7ToRkn%iCGxN$M%kc)n8PnPw!I<M%QZv>dKa<e(*+D<+OYk%WEocVkm2f%kuFv@h`)cw;5L~~({ni=$H-Z(G75`uNvCs3_e7E_ls#}x8`PfhJJPueZY&x(Fyqii&ni>xg2z*@&S%7+%*@6N5Qy^dQ3uNhj_X66bechOGc<wUj3-i~(=%t*n2CQ_aBk42sDstlXc9$V{ah?&v+|F(fVbV*Um*0Zr-wM4Q(Dw#z^2}rw~Jun4?kx&F&=ZcI|;-M^>x|p0CVAUU<2Oth&s-BOSIB{-==+pr%4Rp9@au_H#UdW`M2DUGk56{oG#P+EXe2+z5+{LXo5LL4h^4@=w7BOverc1HxgpLu#7je3x~W-rX%%*(F-rrBIk79l~Cn9j97go`xJa=nO1q^_Zwt+695@gkcf^*-<CN-1alX}&mt1{#_Lj98WMJ$Ma&jJQ2+vIYDJ+-`PG=aXia)R)j1bNLN0%}A1^eNnrFS9jmxU3259KEkfUvQE{;(P{9}M6fdxLmQSr3nw58wAv92;PFyxL2f<3X7SJt#%=B<yZ0(eL|VyTOv++5f_@=LYIm-Rmf?sjw;tfefYOi}D`LkCDa26v(H@iD%dfRO0EoGd_=Ywujjs{5Ot^Hrvc0n$}2F$zXE0?}GKMC%H_^VR<yETW<L=KXqp|MoFcE_1SEnpeN7cXipSOv@Se$ul!an^8z2=v>!*TP!^AVX?P8adVj`NW*j>p(AJkepGV6@aYk1s-3_q<1K0y-uYuJ=LdtC1-g`(Sw7H=rso~G5sXAe+Ebwtb&hMEVe^P(1MjHHtzrKAU1|FSV89RT{aHyutY;ej!O)pY8WQ&@UM>DH3^YZ2NAXDnGqu6drEdJ=bLmc3dsZhi-Aa$RStGb2Q^w6;D*~`p2?EdN{P5Tc-r0SBybFK4{r1xzZ{~+D@b>NTHvRVc>)Y?<=Px#jJ-SEs?fOmgavy8HsVGY;Y-Yc(KOBA`s<7Ox4nK?LSbh8R_4{8Q1F@g$FrIcG#>Qoi@tN1^oI!qLD!S{B3Bq3OD21+k4p{&gb=$b_5Azttniq7m9~}M+_~0$mDdB%KsGP;0z4w)P!AB%)Tl+h9T#hWzX;h%bcl>d*Ji-QLteSNoT1?`%ko@PnpYhZ0zx?*o4|DtX*VljClU`#TWpO*=SlILsc|48}cH*Dg_yRsYFesuhLf$W97Wk6FKznR@o>}FB2)3LPkCC0y6MYP=mov{MpP6Jd57ywCw$P6&j_4Tu_4WA6pTGS2^S{3h=#M{rx~=wy(071lB<X$gO~itg!^jB+9d-9@x8ro|3en?x;*ihhqOYo!&$(z1Tjv(-;XF<g2xo5ov_3a*q(+L=9-F3eTQSmkW9($8psAPB14if=>aH>i5RKILIDW9_z3E%mXu)kiZ*yFv4pLQTT4#6}mk1JU9VxK2w0;;C-^V3H*Mr0+v&61kHu&t`Uh+2S-)yM2&jd&0{DsVJ2XA!TfzDEUVC`wv9xQg%?~bLfBkp790yG`qxD?cy=ax~>+bHXLKexHQF3z~DvY5G++3(oI?HOUEo9FI_>CeR3i~J}cr%hl&<mFvAz1fBx=XG3%Tt9|}Vxd_4;K#lAbd8FVU}Y&WJg7!`A1xD=v+g!V!smW+Cy#j46qyC6upyQwq2Z2GnggJOk-wahI%X9W+@jc!g_E?(rUwwmNOADv9T8`tz>qGC!RU9M82s$pB^EjyGuF#ab`Brg5d}jk9|PN)O&+Ot3y9#k%lIYvX(RX3)&yI!O+Zo+JL;BN1JkG|Quu`BPypAD!;{>oYa8{=wC)&a+r#VN5_NyZu5MGuTJq*q5#t=*>PCx@ahN{Bz?(}=;kWIn1bbXM)`#};he4RS%k559xrNVGy6~77!L@%om!8{cBLFI_;dCjCTg1si76FPX`@CDcyQAHlsEV0flSJpn*g$MjYjXbrVpIG=>FtyE;fYyC4YVK?6^>_2*OI|-Y}zOO-~grFTiiYV`kXJ4R=3rlyGk=<hFtP3y;O_=W`DvAOru$O)dX0aR$Xh{sr;4sqx{){9o<e@AdcyS8e>auVb23>8L_Su$dNIZ$4!q4+4i#<vWGn`pxkjCdE36ihMbUO8yh7{QmCOH^!#w5CEWXJE7r@>MlXFO=9GWTU>b(b79Nvq_?QdFjnYs-uNlp8SUWY;DAEas5IV*Lt*U+;Lz>i+-4WhIuy8$2<mY~BSV%f*ih^uCcPU-(--|@1M&eYKfupo2A}=qOC*f-?=glq=P<tm|Gj-DDr!!IKq|1}K4Ob+UOlwz}Rb7J<OqDNqpE&Hoc;%kdl+;e8JTcmcy|@jGEo`~cXtvP>f2yf|YEb0BoQ7~Y#pqCyx@JMeh;|ysr#gB0GupM5ISoU%w94v1w0-9CR0$a3>n9(R2y<RqdyB5qlM16PviTTxiAoMlED-`2Y~H~J;OJOq7rvY`$gzK+zFqPy>EGOg&4aYr%_G>$yF@sw&+AZ|#x+UoR~)m1G8Y8Qorjw9AbC<$X~BDDA-Dv14h;I?{3M)$F$8Rru+yT*?I>+bVNdJC(Ag#TxJ4yZGE^zW^3cUW7j_zB?i*fgrnxH+GaIK}tuRj0r24Pu4Mwabz+_pW!^UNQZn@{rkb#%v79GKnX)1j%3$&&&kb*%K)1kpsp9Pky4qNPdf`yI3E1z&KI-X*KGGDwk5A4y-o|y4EhOs?+{6fVh46u`BYxyefPvTc&(Gyj{)~@Y5$Yo`;oZ!P)UL`E%x{EmLoEwN3lT|4aIOu7Xp>8?>y0&!g?U*|;aFpo40i0%5suTCdV2Xs#oC(Q*!PR`fIyG!TE>wULH!<WK!qys<ZiX$2p14j0W)!l|p$tq6;^yp1JV~pCJNMDb?bJwz2F#>lJiN`$G5KGhLO;#BI?~>NTe#DWg7v2r?mOb?GN!wWlrQ-E01j6WGgJ1A?VQUb^Ak$!e=*@ZPaEj)RP$V)$F<BILW*KoNIJ*`XR-)9bmG|fS2PN;`yu#3_r=xOjwD~!^WSAQabE~@DoaK~Hgdyb;xY;jKy2@PrB~TIj(jH$$)Pd4qOCNQ4TE=X+$2jhXg)kfQ^V9lF_h;%q-ga+j5Qk|a}C3I&@P|ZEIzl}4C)}y0DU5tShC=KINCr4hA1GMyfzb4xuZK+1@!<lcu?u&vjx$geI59&2TO2FDAX7LaIp7RX^+8gqF-P=R9d3+vainm@xHjJ=0TR8X9A|kTH+9vJ!+w9^A(a=!iC;i<dP(5un+4xUU@ZPuHuUwTi{yz)IZ)8tQF6*tEw}{Ko<gC{eIBBrlN>V<3*JGws%n?h74h?_nlY+pO5wYvw7OzOZb8o28=EkxlLQF$m@5o*o2HiRss-9K_<#`8?SRZa|$)8JJOt~^#}>P)IM=^P6Dy*v_zEjSf3jtJI#f#|AfGJUa4e>x)s>%3}{nj8SRfvxl-MO;ZAWLETKNH*({rQvU*=$jjv(Zkh)ViO!9X1{`&Uj0*SrXjQu+pdC7}mN3QMYk+S$oV1y=W?#Xa1wO53$s?d?o$k&AoZlgpYJ1t9R+l~T;r9B!-!K#nn$*pEBtNKP*>xqhQ0VZ64I)iJqsrVU0r-%o_ichikm?#%EJR`J~sYe)EagLDx&a-gxX*=g}o9sI1;$9SB%2?kLY)KuYVduUzEGEfLxQOUYLnN?j(lN?OhEUU5A-Fia|AS98v(6#1w)<MVs-%#ivC<eOjtLbxQ=4f+XB|SkH6&}X)~af2led9aPHCk`HbTd67nu-_;&J3ROschK)_d(k<)~zHAT_`%+~~A>_GeSiN>E(ukWi#0`F?y)!>0nylRftAWV2u@@wB`4W{Zfy?C~eyEvEcK>xckGaExzMk4Uc=t2jbMFw|2apJF~1`{%K|LU_RAe#}={foa-inMDy800MIgKr*gZEvTMNTTzb;FyA02fSei~3zreCKBM__B2~5}Ha`NAYmt`#Q(_@=`_xdw*o;d=K4%DPK-UuW1N5$&kVz&SVy;Cfl&Anhq@<VMa|Lo^(DqfRr7eO2N7^xBsz(FF;N-;$WPxs@-=qG_YbV5Ft^|^%V5IrbrgO>i^P`UuM{Svy2<DP4m=mxEziu6?I8OW2*EDP^-ZI|P2K*0mZg*2z?@;N>W`HO*`#OeM2Id{ZDSZvaq1&Lz8OP(R!SSSx9W;C34-5=r`Qn2o#?1Zz*B;#$us+x~#NYKtvvu}!M9~((xwCLa8S*ao86izrk~Sk52Q!R$81mf{dOnGg%lpj$^Dy=`P|(o8ZqwbR0i%-|1a5*l|L+*|)S18&yLhBP+TZ9oO&fy3$yci4Xl4S&QSt{aH2y#T^0!1yHpz)Q5B2HO2ps)*fJ)+NZs=e-Odkq-X+oUVfY>^&a>E!Ji4AO(@SHh&*M!$RY)>6cKW-HXXOB_reWwjnBclkAC^gAG@;naD9>7ExtUYSuDC<4+FkmQbFY`Ec#=htRRSbRDKQ|Vh$2rM}QG?pP$cPcaAes`ZJN%NC<w1!${|h%TR+UKRvG%ylz%9_c!?0C#Zn#_Yo=|21X+=AVg#Dqevfdzk$ex1)#3|;v;bCEPh_uqr>uNq$5sYZh2mj!~#Z-;fMF<frb3?v@&%a*JZsp`qboMy-@Gv`2$9WpN@Er2zN^YTW1gA;Yfn}vSR$6rX>A`U3Jbf{aCqO@i-p;QqTxV}Q2ezU*^Q+nmE(B9kA9tlzd`%E=D6Q!yxy~{2h-QWIn7Cnjcw|Yl_c5?lMO*jKNwAzDTg78+N!ArTJ!1!<a~23|8sYCb#Ok>eX5w%jogMQ$sE3o(c?i$@3(@Set2dA8i9}aL%3w0^4_&rPxq6<b&p4luqKaHP;DCnt>v^7KX&kZtH#Ai}kCWjdIqm0M<nhBI4&e18yc%&6|J?Am9I4fy1HQNNoY%KH1F+fQs`QvZqq_9|MRn<UUVCD3)Oex@YfN!a;xcU<<K0yD4^I3Jd!yfZg(z%Qn&(c!FHnO8kr?u+fdLS1QIRohu-FX%p0BPp-ou<!o&c29En_F0A3lRY$kdZeluAyerKLRne*7vVh-z5s2@EM@Y!RxK54HO099l+FW6ugrs9)TuhS!B<A4sW~mQxT3I>AUB<EqM5cY=+(&uy5J1QQ7n-xT!8Yk8;`6DrHhW$lZj34(!muzZYeJW{q#J(!ZRARW*C1qU*06pw&59t)7Lz;)<2m=u6Z`QS-p<Hphr4+`n`qfr&ik<xhIb5ZIfA4;8onq)|Mu~jIWj>BQ+>-@y=%}^Wk<N<`-Uo9QXXtWOlI%kZ)ldki*%vDCPqlIAJs&c1<x@%q30vyq(2@=5sw*UsT$}Lfe#FLx~_UOEWxb^02ok^93kVA(R@yAgU?`(hpg40)bx%Mt*1Ts{aanv#zEcJQ68lH{zMF<I0#;-~Rv^*OqXHgS%`T)BQ(bEEf<;0JNJG&mLO}GYg;O8=0JPEWpFSA_XrTj7C_P_xv!_)&Wn2ce}Ngfcq1SUtLXt<o2GiSFv6R+uYjL<>B$L6{WlRo)tL2OCHa*yfykG052I!F@{o7S$oB@=0Y0|eX^o>UJmi(ZgiHtCT0buxBo(0D@%b#Slu&V<mr+<l3OL)sRi6L0H#Pj>L@AQQZQqySQ<TY^(WD<o=3pXkQ~I|f78Xv&w=BL*uzrH(XXlw}$Uio~^CpILizo{x+Acxs|^9+2zC<x{ZkMJ{*8?8$PlA?m%56!<E=vq<okGM{mBYaL#YkZf4b)3iJl{}Eabt_qo`ouARix^{+n6waabBD||As`I*KkI3_JHN2sZ-~4Ff5p3e#k?Yam!mKC}cFW#I7gAWjbR+O7RFw|@B1c3J^EReSmB29hJjq_+K`Q-UdSK^m>T8wP(aZ2TL7RYXYusybpUA9Aj<BRj)E3e$NdjN?``F7<>6Nb{0GKyfcqq%09OPM?90pAZx|3McNuW=aVItMLpS+eY@hIV>!0?zAIR5teWHt;KAkD!PN)q)5q6raK@wY8Q*iFieFfV6mQxX(y^R{=apstGA`{GNh>%{T9&|$#Mv0Jkt(AW%7)x1Zg$KY|7dNv-ucnpU^OhH3=;ps!TZhyp(!`hXUiaHo^EJ@xYdYb4VN@v^PIez3P-p<pUkw)^;B@wD4O1!*lJTE{aZEol^=-wc4c*7$9utvpk(I^^^q$93>`xw7Kfz0wIdOi-62p#k|xB+X2`jmcXKSwi|*zWsj7oJKEtGCHE&zgHVbTM~-k%pZ2J=WiLAu7bKGeb*{xgTSeA&N1bJd}E*6Q{)!h7y|f%OI-_=5xSYu}nvycm=xBP=&BP;5-cqXGEAn0pr7cdyf{fQE)+nW4zEz9ZKj_2@Uuu4^@WJvDBhRLfZUda7r0M9dw*0{)FsV*qEvlx|D{11l8{)rX+G-X=4IGEg$%fLfL!Dc~I8OQ!h#ni&&TTuc_esGHeN<jsINtN*VT^?iGfqxBV<l%gz(T5|@=-9x@KMv`cZP8FHWG@G}ABVhrZCw{slTjIy9~o)EGHRnHjcxSq?}1BJEkNFXsp{4P}r`g~-@xtrF2b~{oAq0R;cb#AAL8H=7H(lb9i-Jd9R2|(rhu@cBvY=+MZARfOCLI~;tfjhgXGB3Oq%Xq$N_z~t@%D8qmeSs4~B-1{}?NR7yPcLBH5(yWmUfZTD9$+)qW75HbpDNQCeAWv?vXq!B1{&7z($d4HgtPYaNh~s~@{J4$1AhR6?7X+r*w_CQQ0zRe6E-zZY9_@*Z)KWN4zi0^4a3$H9|?(K8}=EVXBUqtNcIH~#Hf&7V(OVFBS_#+HZ#_NXev|fr8Z@?@OMS4(pRzo!%QjLi~XdsIB8t)2(Q}dPfn{WX^e6+O9b~|QAW@J7-n9Ua}Jw~jHE4qG~@@iT2a0^M!3gWu0e*hsBLI*#WqfE9i4Y&9y;%(CH%BppopnTF78=cOvmAxJGeT<Ov@b?7A-<UFk(;2Jbjvw#h0aA=I6*e6HP%VXXhqm<o1uv<Xv{t5wZ!(5D5&hSLe}onAQX`{hrLs94QTO?19@%G^wQiEJCDdnlm#nFJDggWCxgBeb-l**IcbJ(Wgu+a{&zwNdzC`-t=@#)Vc(KBvJ`1Zb2(^BySMO>huU$TwUL&%a243Wyn*m!D1=tM&!WU*x4=P=iWY9Xq~$^c-2*cp{s9DCYj_ctoH{9T`#N_6yVifp;G3=ouKiv+!R8w0ZH6iDJ4&hdCijg;;6h#Db`hK9=p`fCC{Y1*NmVvx+_A>wJbUvajLC|!{0n8A$i=GBT>(tSyj4C4*sFg-Na4s9)+z>n1NFSQ%wml51#T5^+HP7Klj;S+D=r{o9AU+BUI&*tB!UE8Z6znLFOMU4cictJ_%e!zW+R@1!82^#58n7L=1)Ie6=UZ#9b}Y2y&6?IjPgqG)zSuN<RJo5v`6%rHF<}M5*2j=CyQ|<4|{y(XsK54Q7;SnPg++XQ}lG#THrUG^g=$%L;*;vHb5RgR0CP+mOiU86gJN5u1rfCj2IO)A01Tv)%G>0`FL2zhEe5Y-uG0BEH{&JwFSZ4q`vV+JcixHf0&|qqV7TI@-=MOOn90EMr{wc6ca)bhz62p31BUd`ZvY^?hIqqmc8*D`2C5d&mPv=2l2da$uY#<gLM{04O<7y@w}B<vhoJsrtD<=pUU#E?LnBLtPR_0_&-;%s_Z(^ZiVBtGDWyZ5iLg@*)~0JuG!Dn*x2iME4}ZW8CXcA+>a6&KIvQWZC6jDAatFK&{2icFN^-z&7iUxFR1DxmPmPW)b1+g}Y(p>CXi2I;L!DBJ`!KC%W8EX*iPDae>)c5oQ+AMrezEAqFjL*!N1oN*N%UQ{{*Ne-Y?%Jmd0)F$rQtAgalcAyz1NUnpTNI4Ox%RwnMGvaV+k!|NjBg>2Zy2+FJl>w*h6<VGlovf*f7YLKPWS0SyGk5mC2*`;AXvN|^(i3BjqDG84M1ooD2W~Xn{P$Lm?87s&`C%xbwy}Xo88b&~yy?AAXjjMS5*K#x4DCdu&5RxZmV8&v3s#EH)+a8vD!Wf=lJtkS#m2z1G@@fED5UUT>9^Ts1``KoBV!~E|_rO^WhNGbxM3~aMY(<{OyYC<cZ?WDi-fpCQZnl~zv^$F!MgkhkmnP64#Gejpd1;uRY@J49{)-z7U_wTu2V&{Z6EEDbIYqS@m8Cr5A_P%7Nltpn7lq{MAy<n-N02_|A|0uErh8eUv~$Sjh;DeIX6lD>cCZb*lSWt--9fIKL4}X`UV!n3xn^RTI2b@jK)JUcjCTqwsS4$B4!<HiqPLcKN4#N(;!s<bz+)WaSshw-%1g==dYMm&tC{&n;5FAydCfFlu~(B)2m%TQMPKI_<06wZOFgTeQJ1MU1jdkk?YADW-n0OcatY_aST~tyS1*!yEjlixHpBn606x9#X5VGWlAu=dDq2OBu;o3VW@qXUinDRAqX(I7Pan8c-np;C*r6XT>Z01dr$i;pIsCQdcLH!0bdpQ-{y0PP39wZdjCuo#6Zjv|NF8K?;>gq}*`b#-EC_5>=|uCORrmo1`N~w%G3Mxf<=__1+~VV0y0b=)O2d3&i|lSn{XmRm%=I?F8Cg{<WHyx_0BGZpbz+i{APjG5(dmC<nd{onLuL4KQrr_+xn^PL<B;*ecydVTSMs4YTDRT-5v}8>UM<cu&0*@yx%B(3>L`PanU+9E*^@ZB5u&1wolxS;o$_J|P5ebXCO2}J={zRANMe!TfnpHeyW~-abLdglH>UXJ>`%Z}y0Y%EP+A?M%q_;pd)Z2k^GI1!r3v^xi(J~4HtR^&z$qT%1vrJu0xQHSzEz@x;^8vA9GcivN(Jf1Ih)V%?{f4+8*y1%9s&a>psov|rA|ZCyB~DwkiOeIaD}*C4a<|gx;F2re7>T~^G>A+T(_kmZ;GxdUTEIQ#=)Qu7`5|G#)3$7n)OCU7*a2Z7YT4H&<X#TNE|aS=jkqqs$`bhoL<Fq#Y3lNia06w9+Quj)1W#lRh^dZilJVh)jD~33CX{etDHy-b0bknf+tk`Mc)4ByPfK!ch11ZHLbnrQ$RCzBH!2PAOC#&`Om-pfsiHapKr6D2ifm^$O@tikp@J6_q}Dc^=5a|h%e61A5$G=`$W2*#O5xXoT2u@UY|Ml?$Yom#f#Vhtns{^dCpPgfH)~oS>+yR*qUGGqPJxv6j1QW(wc~nL7MARegFvg&{y=>d&YiVRKJ$-2P<9lX{mBB*nYqeIH5A$i__m|N)@-Tr=C_V(Z2fZ;ng}v-Sd%QbpmHm^<k+?>6QsY)+TUzNm*QtcAjRSeoz^JiJ~OaQ&0fcX_{FXnss7o>6HmUx6hPIL;OTrTY~%est7h~<kM`!E_zV4kLd~IT-;<A0~lFf#lJE|MvwA<?^USFsdxb}%=-Kd&<j{P9)=6uA7fwg8X+cXPV_m&_%$%bRVB@2MF@<+VOE5+7cnxFW6+z9d?rGfQ42gc?d{73#<q7N_?QEy?s81Y-%#WVsc@&qq1KRr7^dZBhnT2~mMq4)s9X@W>TJZ|Q$wt|3}3M)s!pGXQ>kBsQ#pp(#YD`g*Okn?KD?Od!DqIz%~g<1Is5a3@af8^d`zLLk^$1Hs@{ksV+*g<(x-~i+s4HxZr!-Nt{r)__e(J#l<U^raDSLv4;YCyyvPk#5w);i5rL;-{|Z7yos{<6vb=OaU4~B({387Y$OI)@mONj289Tc9Og$&y0!id4l9JeUnN+q=NP(CaUDDO!{WYIe=G+K8Ms+{75MdK%)t2%Z{GgJCC&T>+q)K4yHJ7O7e1_l+b>f1+lq=bvvq-!|FC|Mz-Y;jIkz!E;tQRS;lM541ZMc$dgX8y99U+ebeB%j@%+@kfTt1XjzDs=?Vm3eQSgH-P5r|C^rc7$ch-%{@PNrcoV$h>tnc@>oy))q?G+aggag7oNkqM9f-ODL7R7J{B#UBN{YPk9&JHsT4j?vDYr<Eax8MjkFmL}jb2b<76&2mFfWcyn5))kcyLF9P>D__+foX_CY?PhT~fu#2(4mgbdYv_`eyvU*IfZ}X4=$BY>C$}d@_+w%z=GH=qC%-k`_D2yHO_;O}Gj100YwsFC<B1Si!$%T0cp#_n@CBv^QNnz=qqJ^1n{N2XGor{my@{KL*hb}K1T+tQ64rr+Ql5$A2GBb55?k24sQ^EG(t~HwF58@7>;Q*=(f9_m9&B)!pr&p`IVW;l&f9vaA~RWcu*g+E1S}%R9dVDqAqV~PJcBJNMFOBkpwJU&sa$pR_PA#19ila7Y)D}miv5Ltu3k&sHvQm)wmc^NV!aPJa+=yO0R{58;>W-yoUlUa5r9xn@~n>RL!ZS7x_GsO1V_j-$KXN$T=y|?jQq?vxX9iC0%uL-W_}Q8fLX0QWZ9K5BCNxdWmR(WZ4Vvm7~!+eDZjX{llooGH8O+DLf$i}-Y^c)(<X{E2Q6`@QHZe=d(D_7c;Jt38CVUw(k!`0I+hw<Ax!<@m2aSPqe&>az!|o(kxEQ>?sT>;E!9qs514>XGK7dn1Qo;-w}1<?+aqdSh7oy^)P=6#GVs7NuH{;z-;$tw8^%B1{y3^r;QQk<*_ox`2C`@P;YOnri69N+<YhF{&h&gHy_JE{a1yvj3d544COy_>Iwv#hlVR;SM8kv9XTFPNw`C|gCzk$f6WXa*%awK{se&cTAe2Pad_-rqh7zB7@%PeD0i6%cVKky_Oca-@h^JVOX=%uT*c)U+G#hZsf~9duYiZblsANG9yII$o5h=0KIT+?Hs~6Zz%l$y~$!(nT;{q<{hsf7%9Q2jv3_q`W1r#iam&W!^Ov4fsA}Bcbj-N((7-HN_0EQXGli+jG2OM3%1hm>;<GGhlgr0eT92cp{$<-W-8n_23K?=%Zy=c-EyedB|qwwf49H}Vn9rU^S2VhB<<?}Dwc)1HJ{}deWN-4H9)IYJY;4$RGsm8F7faHqEMDePR7nU5e+#(;APT-P(YIEW5T6eME$U-Kzo4~9%Go8<w?x9N08ognXpTMwy!S3BgIt@B4jNd^T8T<E8b`XqgeA?v-K|3a=`S_Y9`~{r~YdXs7%M><d`sJ1IeuEzj`Gpiu?HKyp3l0r9RNyxQQh4|Hd?g$0dEa-}4txe)W|^w$GlZ-gqK>qfwE(Q)y-Ay6rgCd1BYUG&czd0E-kM2|Po`BJxrVM|f-+#_V!P9Qw42(Vn()+h5;i&&hXQ<QIEf^xnkZ|L<F3u93*E-tFbVaL)u3Dw4R8ZSF{N<5%%d)S%o*)f$UlQc=*vB+$2zA`6`t&nDA&y-fVH1x7E^k)7;_UCj*v(IV=bNMo6+8|!W*4C3A-DLAXb=D1rIpBo@5HZ=$0-P7(FMW2Z{k8B~CLZNrdRJ<4QK{bZFws$A}Y2T?Vy{!VKDd#?EfU5yT^0hF%R2^L}7tM;USjbvAv;cqWY}7z}*uBywfJ;=9^%=%*i9{|ZdGG~lf>!fdF2SUnfrH{f4458FcyW}HN~Th&56Cv(namide&Vl}pftS`{DehK=Y=$(mtjwjo*mLvs`c6@bBE|F$kY4v<e%sqyr<vcY@m~gyj87RTN#=ej4j$l96XNXb|bWu#Fw9f(<TJ!)lakDD{VSfyK3za5m3y;B?5#zF=jx>il_3<BG|Ms^lFayvpEK60<;MAQFH8a~ZFu5R`b3vy2$QQlIhq~vqkHqyvV)X8^j-B0)JRu$SoBDSxP8SZtU`htfH}AEP@83RV%6W;FC}a7!!Sffj@Ga{s^K2*Ro@FU@sSq^{7)cj_?#?|yI4plbio76a;n9F+-=)rC!LoiwVP#a-Z;NwgQQG!Qi>(w|K;(|IgrAdaKbydwp5|mrRF#4>Pc&0t^bseWl$UE7>B5prz|ap|8{qDXsSIn=&evt1d&s0AvHTHj{CJK}QwmHpm?2m0Zml#3L5Sfte!?;DqGwTIOm+L@;!yj6FD}36tPM$F<EdV{g7>YR?Y^Iw&pqt$gRbaZY}2}~_KW)u!#^ckh)d;aHKuTFC)q3sh*ZhT|G2EjO09BtvLc(1r1fiU;@r-5>k?K#T1l${m(8$#1ibgqLO<9KpFP2P%8ze8J~p>0j)PjBWmQNvnfsx?f01Y#E__PfHvTvW<(y(e<#HQF)Rz^pdogNOm}V#Bs<*jTKG*ZaSL>GBnbTNr4FQuqAa0ryk$o%yaOON_SL^=A+iySp@n(Mb@eb_UqwV<Z_1CxG@sp^;LWfcHAD<5cx{eu_f_ly}QEmbq*uMkKw}mZeSN1=+2c?seS)-7DC*}HFtw4_({_pHfm6QJVadC4Yt%KUG3@bUa+?=z*csu^L*FC48c3*Pq=vtr7{%}b0YrguwzWi(8r;y0v5ghU3bYDkfe}P>g;;G<C{;yb`)M{`2yl8gG$j{_x(A+8_P6)mDkfLvYfBF8W#}Y*HpWV6YWEsb@^>yxNkZ&gIG}a+*4tgj8FCJldSnAiQ1&fVGA2<2?zx?$3FTeftW2@iZAHE$Z1OEEc??0cbT}PEVHs_BppZ=c7{XS~67h$8;<qzN}3#krW&7hV(b~fM`Y3QQ=<<DP!{rTVDKKYM79UTy84eYO-=dZcI(H!P;q(!x39~Q}e;<ZNPWq&nGVaXWBbF3j3<>{Lp+fU2a_ix!XZN39eVpJwzY=8t!@bHWUx!Mb()mV4f-+cLV^zeysHM_trrRL>r#yfo8n}&|vt}B%hpcn;s2AxsP{2VR`ew#=@fRInKFl|4Fvcy*coh+gj02xBekE6e9@5!?EtW?k<6T=$Eh3gDYsm_<Dyq0BGdn4LGt^y83?6mwS310HqS1;i_-RqR*_0#3qsQj$m$2G#dId2i^DT#iA`CkBcKdwb?&3Ha@<0bOIoWNpMx$wgOG;~qg7f)Y6y&m+4UA#Q>AHGTJ0p@+XV^q7IWQ8a`o4II*<`8L(Eq$*>pGFhBwgcX?+u4`<T(2$cnxSXvW}UzrMB#NR8tFW0n~vP!EMDkHf~dT6DT~bSrQsUhiK3D_#A7T~#={tAp>a7Vs#J3)wngopZ$6ufR*<cZXyWh7w8~qS$IrUCi7nB*0j?IK#)>qn#%<3Z4E8M!i}Y8%p=TvJ7MjZ|!7A9MWT;lvuUtxK@bS}=6nvixmK^sv|GFzEzsdb(#P>7qktz~E8W1(*ll!eteZEbNPi}5$F>d?6{{H&<4<WsGOgpL%SdtBdtUs6h_Tj`uY+>7SN@~}Gw>X^|B{ppG@nd4V^%-u`F^8#P!ldqyO@x92nBuV3l9l(dj;aQpltjHVz1-K4cXM$MWEyIZdVA=DP;Lz=IGq}<J{$QxW=!E|2+-b#2dLieG(@QfTmB2s|M;Ity-!c>PUFzi1B4eA0Y-x@@ZR%j4AIg_l3o8F!G}-55o1KeU=<MWM<}Xvo~H(P1j;Y6bTu&%Y-Gncs#@q4yNR?NVd;XY!9F~daGXBZ1)Ih--@>LgqS<%W|AiSC{??ZnC0}Nm21qUziv0?`3pRBqY9xKaOFYS`SLU`j`osol{%H=xq<1D?x<YAUQLi71?&baLB>MeeU`*4;K1s(@3;p6<mt#)5-fh9maO`iAs>_sN&S7kSpq$XQ=70~M)!Y!5J_t7$v~#N%OSs$E9hwt0Mp_hAsb&3y^fWJOjzvo@(K;=~zg!)XdCm0PP+2mF|7?wCxTniGur10kv^>Ef!I*JmQ9j)BnC3k%BccgKWSrSDrU~vOK=iw&Cx?4_?iTfLZ*Tv44U;M7lNS<;q}kP!q*v9^Yfgs6dtvH1ulYYQFQU-t#$hGZOqJGUNfD_w;|GIXGFU}yr7&J3(c#)WSzwf#it*z_PUv5WBsiFu9b3g7{sHD)@G$L91#>{ZK>vu1X;kdM@#iM5xvGYDvyOs?V}|Z43%x|Yz%DF@-?J4M&*!@e9J;jpd;iCq?G8)v?`r60bNuJ}u!${za^aZiB5P6v-P=A83%%TSLL8DwkKZz=m`C8-1BZc6%lg~qmLI#$JVg%Vo0d^6Vp^CB>_GQ-B7j3RUx?MuDa1>H^CIZAGmj7CM=(L=)W9SI4R&KBUI-6$HU-wO6EWZi(`}Fgy$8mXRNC$Xh3~khqX^{(1(nn6E=!`krU-vAtt}z7C{@*7!a7j{`LwBWihv-AwU5Uo7BIX*;Gdk?xnXN0=Y9`f!M(M-e+J{>VrAN56qP=Ed1CKY{e8@GFNYPP_L_HWT9cM&IfMc*K9QqxcZQYfqy3GI7@1lqkttG+=@d!e@9CH8HtKCiZHRSt!)kJvWCOl|@B2ip3eBc$Q7$4S4MO2s$i3zQiN5dBfH7HCF(;o*E)*mO^8QVpNSE9(7X+i34D$;@r^vKzPquO1sDi$LP;Y85d^okEG<E`YAR=I8J=Q(c4zv%9aJfXA2shI`cJt873TgW{kVj-v)XV@MBhuNH?K;{~5x^#efFFaIqvetJQd9GbA1G%ZOJu%-;UQkz;CZD&X!5{o-@5~FDV*b9OLoNAN}3FqheeiNwP_9VzDtH4oZmGHS%I@_Pl6pP$kBR9_j%C$z36a)a9Y9X2v6HQL|F8&rY7H@kVAu<zr$af$LZOZc=_B1cpf9!6`yZ9BKdUN8|Oq|$#Lq(99H@52G0;fwnj(X$$!laMF;_0gN!Ys#0#IPY?|sA?@kj#bBf|kXQZYgPhu!^+VCj>yGBlrbuRC@6>Dwd!^_jp^OV5Lkc1BFrlEOfdt|36A;tqz!cP((Gf3Srz}k^1;?g+knkA2-uE#~GuX!ZHFj?MfIoFO}HTA1*A?tZwWa|^*I-Y+J=Lj-O1;!9imeAC~pXb^irf}@z9p?s&6iby7sEwctqY!`{IH@_*P5Q`eLt#0hTw?t*#ati5ntOV`KLECl>)32_@i?lVC31Y^Af6l83=`0T^ukQd5Hzc#%9nEklVNgyBpDDHZlO?M%~8ooxq%Z%sV<`QYQE%nZaeij8VHFd(e${xkIIn=21feu+r_Wt87!|mUY5N<KdQW@b(O^xBQPq|7{k9LkoX_NYsGFqX6aEgxOsKV!x3g^ntKX%d;hGC=>*nUZ}x+a>*|rd&n-;GTK#Ow-B5FXqNB5nYVy%O{kA9A$0RHHxm_gOzpeq^gbsMF%Q<p0sz_e^_AgA@`Qfo_7D;V~o|itD9Pf>1jUIgZeg??i>;?fObr!$6xKZYq3S+6k(+6tmCg017PZ{ctxgkc&(`)u>he8-L?2qFS$mv+{uHJds<Up!RyT?bhv`|9TCv7FjE-Vjo54+0MwQ#ELWajyj#+hke=e*Pks}4Fe(MwcNe^>z_DqKsaI48*CQBILO0}#yTuOYaQL{s7QrlmTO58~<*HfXD$lR|HUefNV$(9q-Mfz~MXqIZa%CG6`3lyHmQE3yq8TIyi4u0sL^33i>5naBp80`?monh)8}ugI{q#9|bMn$$oIlWY8&Udh7#mMFIR=+$lhitH(~2On}2ds9%1;3YKvm%S4Td`E*&*w-8k-n__RN0DO(_c7C?6~~roVu45_N{;gPh?xUi3^4G(>w=J`Xo>o(WBb~XtLoINq$1+4vU+>*I)LVe(<-{$FcrkMj?!Tp=Ju;lIG@@Tk^aIMhvo)92ZX`=#1T_L^3rtdcUoNrvTujuS%y&+v(u2J49P_QLPp8Z>}BJl0?qGZwzHBNL`P<!yby5{8**c%s=673Ydy+PWHc9tB5>kN+4|>vw$fnh>`}xPLd_~$`DNsy2CvV4j#Z|IAlDx#{AH5NSG#~z({S>+v<NrFGe+sk&vT7S%-e=&0a%*MmZnWURZ$*~^VLR5axp2|;?8@Fa?!vUBr4o-H`;CCz+VMO>|=<Nnl5MjCyp)j({im>0tO}|i4z{It@ToOJ*sdDZ3^po2ttZy=z218U&%W9aS2%LwNL+)7NYG*hW@q?u<;n^s+5Kw(Zg#klMva_vqH0OtQ&w)xg28~`!*r!dh+tNVr^a_$|?<E8pEp6(+i>%y5i)<sE)~0qM<XUEZ|IeFSktrNR3*@D0i5|Z_hq-O*HaI;Ovr~7M4uD4C;ua$~?+!s9Dz05U1ow5c)~Nat?ZWjs)|I{i-?2k^p8A!^;U-WW<80@^g=9!O-8@{kfJrwGWeOx9%b7nCH{8w{>3RjiFdsYk6q%Bm<cr1KT2JB#OQ$xIL`lx^+$}^K^`TPh@3z%Efg@y^^imD8aHxrHs0~#XHAKCA5@4IMCURP#TiB5P2(d+c8g^wVletj;h8QS)hN>B!0>$Wg9{h&WNHExnxJPs7%sPVQ5Q1V@rtJrFwng@;b;!7Cd_ylq6Etp_nH}ie)zLK8pJa<O>jY`?IC*fl#0iqQ8&`G{z;|kI>#zt2UMgTPW)<V<36B3Fm4%gnv!S7nXlit**2Pa{yRC0*hW&-oNQJ(FNuOODK?qHC&fl6t0<85JFRX!PuTsC%GL#L{gw!uv;^>$q$6c5V(g+o#obr9FeDA5@CFLw7T`;C4Y{o<nUIHX`9E>sHEu;OR4PoDxKC>AGr2%#s*Tf(RX{g;2c8f7jJ4jX8Lc$*LBTxkvkH$ArzS>yIAYSM~jTX)Puz@W`ZeUD&tcL2y&*V>n=*6F>KS1U@fj4C;($e3GJBf9gHk$MvC&QTnwC1(JMaU^$9<QJoR;jX_Pw<(j~;zxyWLPA`2mLp75zi<_I9U68NpMEVA;l_hxlH!UPb<!igmpCwX-UiBm2-Nh)HlDF`)c<_=~g#JjTVkm1uJw*KKvLBI7jpEXJe1F@9W{neq`jDUodNFP6PJ4aq(*M_0{MO9-IR(nO4jds3i&dK;y&dC-g6NBvk!toP~-i9`pP3kw9PqRVXg<TPnZQY#Wjc1=&0Rcr|4!Rn=;ch{pBv9C(ldf#DDzD|e7h$kMS&>})3b;#A(lRPz!;ElPYqc0<cYsxS2_6jn<qeZ~=&(i7nAGD+s}GFamOfb_6Aru14bElikuZ7pbe;LK?fDdQ)_sDG2uq-+FvwSbaF5tT0x&fwANq8}&>v9&`(>Z{l+wcNA6aXd59}d>zE5J-A-00zm$MgCWk#gnB7W3fJ8;67jmAYvD@jX5wFge*eBAaWL82>_d86KgkSmcPjG(zXX0pmOvXD9@68g?jM+3X2Vbk%&4+%Aa_P16`63L_0)P7L4*kegKTVU`Ib&P<|?O7o`YKg5n>_8RRlx-#;iGN^WuipYnjN2BMU*KHlXLS=Pz%0SSqSrW&kr$eQttoO9r(5Rpg3cOtad46jj$0Sf$yqG_^<8N~%2k-}B72mi&yEmjL|_sx3top@{~c9(<#s^lxD2DfI_%x3ejFd_qRO<hkY+%&VCz8V)KKA`QS{o<MbaY24Sg&tTImy6TUKTD%w<lK7ZPaDlz{pj?d0saHgyb1+Y)UNG+<!(8BH6b8Tryt%eN~W04`D~?vN*=j=6FI%K$&buPB3Ybs-$HeD5f<p}*jRy`*?;>bPa<`Z&qNdq03Xrc3w;IgHyprcu=_d$OCI#XR`fz5YwjI6pW~zBQbtPF5e@<`v;*?OK@LSLdLTsVv=yN6_XPie&ibj)#14a-^OUS|b@rB-8<^c%#Sx{*r`dx-=cvX?w2M#6D_YP<5(J9}?xG7vL{`rHP^)#FEKvfeq#4B(pKz<~-{JYMeaJZKD#QA4<FOG2}Txd*4^HekZ@q@v_GdYq!k_p9w19ks>Jb`jhLtChA!(^uf=|a|BQbLM{epcRw1NS~H~3o@m!KWgw>s>=<cO&S8}f)`4r^tWL?lS~3-ynD|oW(BlbXu|4K=+QRmjpxw2R7B_iKa8%s1ubNY@C81HM^}a|<2XcPk7-gvL0sY|6ScO#VF$F>@UnV)kWqDFI@>Sq5>`Ao}Mu1vY9Y#a35aCXoZo21jx=&5nb6s~#g$WS<N)$V(!0AlO*Fojc0UWm-l28Qi;pnv~sj-9P<(Sf_pYa$#(9d+-Uva2Yo*(GqW7bcna6blCREl%f)aR4muzu8V*7yCdGSLO^Od_`K5>b+0?EsFQrn>2D$mHQA8uR-Pf#NSMZseM>j>&8)%U$%EVlMGStAL_sq3{m|>B72au(I%N0DFZ!5Sx(}!CDiaL(|3)kd;PuKiaKeH9EvIQ2MiJ0D=2*A1U$&?BzOtDpB%E0V0|h@g*fOTNjx=i~)p#E#*1Vw4My-m%Ptx?$ZM1{vJhvy=QwFv@OzkBUvp-*6IwjX`%*)`>?}@_Ccu3lxpnT1mi5q=GlS43(WSi$O_&8zbX#2-*Yqs68)4~{+@$VxF(3#>>aW>DUroAK^+(D-6nH_29<fz->o7QJ?NkH_LmUVMydK`W;mu?_(UoGK(N<!2wXh=h-T{al=CQ*q__`wl&x-tu^tyWF>sKtzkkx#6qxS3q33_`5f+y>?)^V=!)rtbrZn%%SqH9Ti~f~$^k4M$Y9n4E#p4g&+E*0$R=Ii_w3y9K0_LMm>NHWgu`}1GD7<S7YRw)~4(poluR$x-yI&a#cmiDAxoE0_w%louwn3gC#&9}K8-72fmg@?e6z!X~jj|g>fd$D<IB410q7oSGl<<5W(zEzz1sI@skp;>TRLIym!=b1qNK@+2XXo5?>87!|>G2V0BEIfZ`+se&-F_jd1RNvYf{D~b@<Bpha*Ay7Mfk_X$~8QRd2)W*c#`qMa{2mvMka_swl!?&NDa^-GXQahE|mt&t8QjC9bQC*ml7tCNnpB0eeWy-y$U&VQN=R7#4ncmD+yCogt4g5i1+x)(&teesus7~iGKUsf4)5!(?&|`v@*w!g+*;B87^O|P?svb?`)=1CfvJ<5N&F6-V3kZvF$rX*+Jn-i65`$?~GoV>Vne(uJ1$z+-EPCJhJY6@RsNDei0SF=reA3p70D(k7lnKb3;2^qYeykPSuof=M*WAPu*oN2P3hr)~bhD%mq_&S|z@rYsS{l2cFki@MS%JGTu#F7utQ&$roB`-}9uqqWVlwu_3k$91!rW$hHB}ox1PO;$uGNt4QHt;!(yjJVpH!NgBwhxMdiV(pi(A90<54VJ?noWRMz|I=e~5A_vJS;%@k=7E_NR;mBF1mLWpkL$HahZ}IeU+!N8vM9&m1O-njpu_WZ`2~Gi`rLCp{mm$|g;273M7bZuG1rnh6`o(4Cz*S#{rB{9dB<!&r{_1SU!$kcza~W3EF5rfubGGT*#I_KezD))LlFVP&iUtr^eUhB#dAi%GJ&~FY0k_WGf|B*LYM|vrDMNj9lg6P>YfTmi1n!g$VGmn}o(=k!aqNq%X#Wpu?@*hV*qA3>J%?O3CZkBhACXVLMoT|umY!*>H{ndo_7rp*WbRh#-5QI&bIA<0NoqV^I36K@80h2Ocq*@Yi3u;Twq>jd5v!mQ7BOyv)Kvr1Nlnf^-DeW;nA(zVEMx&G)p&gPIeQD_ZM-wLqz`nWX^3Vqm@xu#1#|2cQlFzaZh9mi<EtdmPfEuXv!Bf8$oD6!6c}Yi%`BApRLY&6n8`sWv`j-sAp)r`WG$ry)lwoyFZBs`Xd0i)147aTr-Q~$S5hEwHV@2m_OkfPG>N&thry|AkLcaf@_OvYTMMHm{+4O}pHKW<U*bmhw*|TRiLcoSUgu8%-z`%WGmjDDkHoc6xHxQ-MqPr5kr;nkWI)=xk|uk9RTRPC{KX!?yY<@ik;^q-fGt9=i$p8~mpdd=U{JXfjR6>KYoo=m15IR(C>MBK=OZz4;H+aXW2Xd)1<s>X5tOuyau8}3=)Ry`)ZIO-6`hz4iVA;>xJasNp7lNm?Ea-_DLHa6<RWt^;g?xZNdXMDEFA^hD;uD3>0LiUykOmzhVv(js$n#VT@4`b+1|R3W7S5%r@uZg`awglg8_kcxQNot(IVZD=7{f8^w^1Hm`X?9G2X3@2^xf|dZVMRQBCPo+O;o3LN1&sj6eh;4Fg#KC6pH&LXf2qKxbm9DSSI)P4!dI_Bk(;%$rJ=PvGwf;Qj6R<=4E_M5mk{l12Z{Io@4F&{D!EfIVFduBTLDz+DkBZl}2~s~+}#&Q~2O+9pbcT6jy`v#6W%=nOfc>FMZZ7(lN5`px?d`Tp%=rW57bTrymnUq!XKG<}#-fE*L$F9||^Ay^x5UKw*!+C7;ZP&!-?rIX4#V<7UPSRtB0W$V(~<EC-yN*=n!%&9D@rqS5>NtZ084M*rC&gf~YvZ`drP5opy7#;7vEvOoIzxR81r8u#o<zV=c1v?E6Fl1mJ;vN{7q8nYs_Ab_hf(i9IF3Mt6>=*YRhJUJyR%cvIm}Nvf;0v&NHt71p;DAKo4ilCj`O5bUANl>pn#peX)$lQWBUr#6GhK(;%Q%lS9sylJK)(`Z?Kj@N)SQ~z6hn{?ixwD1><2m1dFGMERg~l@d`eWweLSalb=i(#pea&JVw}ga*~bg8{>SIi!(91nZ%b0Cxzko;%EUixMQBD|*PV%(ARPO>?~jN6kGJ1``s2;~@Z-VXw@W4R_1CxG&CmNbv$c&kiizttjV(Rae2Eej7GcW_Y3sV2qp)uc!V$)Xl{^D{rG!mr*B0)=^DDlo3>|jO>=)!!_r4JA8Y+>4+ix!Nw?Dsr|I1?uG<byi^k)QPW7#rng{-CcT|$Q6KDA++wZ<&0Dkja;V<h<3w|6+ENtJ;6@dsW4`fytaBL)*vWPW%)*KXyphTi^P{`}?Fpa1>slmGbB*m^s#`+c#$c3P|k86j4b$6D0u{BdXPCt@BhseRAf7&l`#HVn96tf%!pwqFymv1{6V2b{!+rU+nW85jMTDSR;JI7T}@euu@Z%Wu=Orn4)EZpFi<>8uiC!{KR{k@t=YUA59EdF$x7l%7Ou<lkx}b=NB9*w8q_8-Nay)LhQmw9((S=W=;6B@N?ux=_dGJ}F>ijC=QE-I5;qOycbz*NA*fZghGm<X__SpML-4x1WAJ%;WuZuTvU3tye55>5tvVHR@n=o*qKIAN>Zy_5!fsxJE6CVW9S8Z<{kGu$Wa&DDgiHJrb!?3NE0Y=duaq<6Zx7MOue1@5&vc+V%7-?S=J+<`DXf4LzQyT|yChwm09i+u4`<T(5=*kFq6U57p@svAD^+7TI~!Hoc4mo5UEf0mY)7OBs2!q(P&3<~i)pdp)<vndM8uB|jsY;IZMelBUnT#SN3c4f_*{G02&c>JZ8T?c?Xy`C~xJxKEk%hh5k5MaAiH7rGd+uA?s;%4*OgHLqt1JhO0_Slp|~X_tu*jSxtIBTz{Jd2!j}uRo+}pe0AxCNw8ECo_{hn2m4zufM;({^R2b*%wu1LIZr}96edN#+mprhqaGD)mC6sm;m`#aLTqP3ZEdo61MofGKeZ)$z7)ZeQcUS9yRuI(W9PjWcS_Nso@rSSA-Cd4wMK93tLaKJ1`BsKrw(&mJ;MRdE*`CX_)ebUyvB26bH^Z5kxrsWu1dz)0hW9^_gGISpAOSl*n-h3k1$-Xp@2MvOdB6Ng%mTe`RYl6>43nUM#y>{s|3Xui;`@BNs^WI=#&KV;bfcfw8oJD3~P@5}uC&I6uw=J;R$?K;tiHmxU#m;$w7sEMj4T_8A8@ka5=F96)(X&Apx5AEIh#Lp|-dP_Th^6&nl;C1W6UZE$-qy2+kCB5HN5wM;RGjTfM@eYWsC8~Qg_h^1bSq0VY`?VX5KhJm*oF+fpDiR)=Bdiv1XqsOjzbLlERDoD{pYn!j<fr#=>7Nh}2?0*3k(~j^M%JO;jo9T1Y4O2t70%{UOCpD<&Fgin<!mtlz8?}xRB=a^UOYC7I6m;7ZhQ4I0FgIZu=;C}HCb^R3`FOssV)4jNV@2-6j*4FBRfy^|I{Jp-z~R{mn@pK9a#W4;<MpQ&`o+60$DH<_Hgx+KvqS}pd2geb$DUDGUmSQhZF33u@L6q!<J9fp1_McS6`wDt6rVdfCm<U%@tE+wJy(0~;8SOJh{9edx8BtuoY%g7We{b+28`BthI_i41KZL9d*JX#ULTb?b^Mfhf36h6oFv90bo=x&s@RfuMf4^9H;2a=gG&DP_V%yW2M8Z_LC#07OzK>cd2#APRUHNEcd)`Y=5(sd{GXT?;jeb{J|)$4!}U~px`ahKl4Gz-2J@U@rc88c5?uc=N;$>DMR{l!B8w5A#PDrw75n%{Q^4X-TAQB==74^I{t;N1mB3iXpPPy+ry1SNIto6H8M-eO^b-97yRe+MlC8jaKHxQ92zSim&31>_rgt^?v(?~peb~enkF;^Bi(DBGx?UBn65!xiFIz9ep2u$)<g6CZ)v*o(pO*Ew%`HE6y<b#kT1FMSV{wBZbHsKcz?U{(h@hV-1fYZS@=WTBh*w$@z65xXz(_bfPIFHZY^gGm4!Pni7etwrvWdIzJN<3Pes<l{QD|Crup+0~UG!un?Z;;D3YOP?e@&a9nZl5cX>9?pnbxaFYVG5339mDymQK&?+^{tQJ>0`raBnRmqoGG@>Ki^DH{xRM-n&(QA4PJz2$bU2f;u*>NldgF@IiMIO14KkV>gp%*|qhn(1?+#g&c7rp-}`fV-$;t%XJ&|Hl#MhI=dlUS=LwpX3$OKsGG7)&kKx0R0g|qK0%G@yI6W3H?R1L0+(jdK-!o|{0W+#@<d8c0|dGi{9pb35L)l1NFO>*S+8G&h@KQ}<aeb(8~}&mIrT~y4L*{oQbqN_4mD1=neMTh8<5$1T7L?-`x?eSkBD++Q2PuQzz#&Vj8=a#W@{e80wO3Ik`R&fi^eB*ZV+V*X=o!?7N`4sVqg%uSD<5A*l>G#kLMw3)Cnst`hD?3Yf^SUJ?YzU$LU#ny?m~jo*P(`jj%wlM``K6lMVB$YI$QcBVJ{D4)_Zh<%Xv1XRk`bK4V#@n5ZA)(+YbavZ;$>ygN-6%o6ZcO}lbGlT%vz2D?EE(N<5C8n6z>J>Hh&4g&G0cC-l;1qt$5V<F8&+9TV*k}SRlvlgmyk9uE`cc&WJ7cG0>cXMRcEO`{?NmUX7ArJ4J_L+i|w{fl=EwrCQyUe_sd6BJ8RO^5K`I{pkCF?AK@JYgP$+gJ^j4Y-4n;VEq$Op{e7n&+4!O&d&o)U@Fd}KRO9o(`wv0{d-jxd+GhhX6YcIh~ZP*X`mac3U&3xVm}Kq*u$0oyGDcpd?VL#m`TH_!=1NB}iV1%_Kl9$RzNFxE$sMXXgWd=-%(f?kI5m$v~C*yZKQXpOK^w74SEj$LX68^8<56vn_hXb7PAdW~v%26O7JDN7ciA64G>s%z26auqRx$@3`d*4UqqNqGb;ZnBs3Av26bV<^BF_s?Rj=xc!M0TmzY&2x*?u#ZeO>uYF)KhdvR#xzBN_0Ks@NKpK}z4m*SCA@en;q%gg5Ote@Z&4!@o17j0457W6MN%6V=cNy+1)W$nRGtPB(o6OpHy{-2>wt8RFNVhaU|}pZczZ!v*OyqNNZh#9e{RSQ^9;GY>VyzU3!Aifz;k*woON|xHaTwVl0fl+6)l=g_0d|5oeL$+9JPVOE{0PqAu|_C(epazxlmXWzD4$apiNjDpbCf|qb@nWo+Sx2HUxr27h=%{E)ziE^-e}27VI{fTf4GGc@n+J?-WwM9$yJ~=GowFkUe2qgTD?5R1etkOr{ODP`Naa!TE}G*j5uTLg)$5_nc?K_&2@!g8i+~1KRxg?<u1JA3YQ(Qw)RfqBg#Yy#Wf^!WFL#;N@WO=Jg62Kpd;LkC~pDIO<Awf=AjfUbwsK<V1`ZGH^&B;3QfRlI0i+cdHuOv*`R|dNVRz%9w7r{2x)JB_T%Xb>o~4%^va0kgNkjZlNT}MbDJ{&N<iH{w!?s4$r0xqe|zcVdWSAkN$;>h}T0Xe)aV4vznFs5jq+R?P-tOZ;;<6)qc$&+>2F)A_I(g!JI|}x*^OtD`kiT4`rf5_=BfQ$V`W0h|3^%vXfhF<Caw7@p|1|YEdwFPBWQLYCY`&mLU=gfc?uXnPTguCfTM4u*O+UBaXJ1L|$>{Jw_Qz;06)$-neb%ws7FDdK6S;oYbT$qiS$WpP#&GlVM<BLMk!gyV(LHbyTCWn}DZY&qJ`t#E865#p>s*vn9q)lrc*2^;AdgNrtYc5UOzR|0)fK-^?R6D3cJ=(6d6bH6S>1uaDh?Y3$pC2-56j_r!v+!s$~QZYKtye3v+jIfx0KC_*sL{E#VRBWI*Oz<2UqZX5hc9VN#ocbMvJ&pvcb1Y9)sZS5(RFk_cN9RX6ALqg*WY0TwYA$Z0ryZH=)N9pny^z<BG-xvE;bCfUu6bObw5Yk<UWi{pJd_G~|Z|(kEOP+&-i4PMcX-?w7lY_@#7kOhSfYVwY+U3QN&&R;_L{5)qBV3oxD~`zsc$R1>CCu&xDY38`NdZAm!^}&=2o)lhL?SEZ&9WXddDv0KPUFq<5358+_o`@5C|-Ffa(Ra)7@7X1LdTTCJeClUN!1R+<#hmNEC6NDvO}Kl82Z{>2GP3nSh}E7%(|g0fTiqG_MSqaxyty;GummJAQuw74qaB0c8mlOM4hatV&cElqV~1P(EC@XCi-PO4<1EVu%zZP^Mz6|aB5R9wMm9)i$!acj&uulHvUG%Z-J?^)LDjf=Sc7TBs}AuQnC%lz<W6d18vyoyFDE<jFPle?zsLpf}94D9CnjB3bG+;kY^micW#F8SFqH@OmIs8B<!OsfITHRJ8Us=1BnJYY;BGmD8NldS;d$h7>sP{YrbIcGFHdeqMV$cw=A;w?qkl;!|utZkYGZX3$)~XJ1-$AvEYOopn^u4%y1)U?bM1xfEPPO83qtyZysNu&7+bmYm^%T1n;fOfuA4b>9O{BRx1HCW@Rn$W6I#6qOdIr1-$HQ162&(cQ4H@CSq;Zc<dBc$0<JF^^JCVXfOQuRWJOOQ5Qn5-NGxuj4OgRQ%veNQ;vZ{w?T4Vo0Eq23@l59B1hiALxOO|O^udL+~jGlwprCQ@gBS|n@1@|+)BJP23wRmiVAWtFBevgEY8p!;L;~}a2*1`V+NhxA~8d@&7o|2KI@frhM-%)a(cqkd>ehFFRe6iQYsuUT$q%2q8qq0&{T>w6J$H^b>KwtZYZ)Z3063%lo3HslQd{x$WfauXU~ty^hwe~a3hEta6i`}nb+Nsp=d%;%g{&uYS>+Jw!;oyki_$RJVpoPVvxDYxtfhSHl_~qvwAnQ+MZ}r=09q#MQsqR0Nj@7M=mBb`eent8X{PEUn>Xk32B`yu<?iYxeD`I<oA|z2a+DssQTxb`a0x#38)&E&3-_$pC}SL{#YIMZYU#mC3Vp|+9g4=Jsut%mQ!m3Bee-DMwVw&g-HlO+?>ENK$SiZwPiC@&s^p-dEOpto*<>Sa3}BERysAZMH*<DD$;0*kAW^7l_AbXOM7gE>lik;)-jhBWtpsp4muR0*_0qKx%Z9;8}yL$#pYy|Hd+<0<Ce*o;q)R0vw}>cPM)qNBkMG(Y7rRaEF;vJ&yJ5>gj-m-U7M!PW_FHJkDyC-=B87}IhJH9RW6s%#;k`N>@g-Ck@PG(d~F10GXNRTY7`P;`&WfWU#@R9t&zkK;^2mqd{KM?e@Uv|pS9{^$lG)9-U}9B{-X4Fja7S7#cn?(PGwoe-0p+vG3){XJJREvXPw!Ev)Z`G^+*s`MNW+8{hj9o{cT@$@SXfRM}r+htlcIie8?zmclg^N&H=+;6Nz`X$gD`l`Uxx62!9@gO)X_mq(QXD8vDP4vOh+;%Zltalx8hX_Ce|tf2kqMYwD1O{e3hA87#E#3^$nd=-zRssxKanJZvQt7)?g)zDtvgfh9?5a9ASTftymz`umoj56$+)K`z!19UpXzH8P@RWWX4>3G~=i@%J&IP^5w3rS@Sl|8yT^$m0%UvG6$xNq6JE;&2YLIcF2jQxlW8JSijfD$ru}B=NNi<TmHlvg$YxTFejk?+oueyXv|iWzRM5FqIC#)F_c#h{>8uwXW7drL+K~gdLJ01hC+!_b3V5qXFQU(x~5qxai+cP1#@Xs#Bh-;}Uz+&xtT=Q7LFyE09k+!MfPON#3`+$}Q%+{eqakOJafiY7`6$gutiKizUB_IJXQumiq{uvLiUVYj;sgqRYMi5I_-V#W&yg@!!@4i%)p4qUFZqwF$txS1?JrcTDrSabfG8f!)GK4(uLwz-$dD?MMZ)Y5Efa62Rywi#9M=m+*zqCw<IrjQ8q3X5{SHD|r4?qRLF^g~BL{x`g+M%Jf8xx<A-dJ>CYFGHP*)rhm+H?o+trE-gjYML@8qycF%6&Q8ZFwz6(rAd{f$uH7dP`Wp}OJ*Kp3pEmetM+q8@pL%v`v?ESx5UUx6mgLg#&d}m%E%hiaORfHMa6s1t6_mYaHi;|JDE70a*M^~<@e-!1m1z_#N#r@F_LxKnx1=Q5GFKH7_-X-;Vs+2b0>A>mIs{H6e~B}Y8>$W7EJZ3+vz&7oWiy`PoW>bmjDr<-&A&E{Oai5hq4*M3K3Dkq$c7vvO+j~0Q*{0p-(2yqNLS)^TF&y(8c{MSt0bqJxWFa)SLys;^snk#pHp*E$Oy9NYj8}KeBS8cqJITQVU^JzVXgru3O{fjPPdwy^zonymQDn;=RwWPW6E17>qhb4fNsq!gx=IR0dye#5k^~u6sqbP0#M#xgXX+<AHopOH@M1O@+tRoaOWep4e|u>mWHjrz>ySkcVXMBH4WP+d+-$SmF%sAPfv>n0Hd7}J~#@wv3uumDTRxCnizMuol$y(+n~iP7&ms3&(%$j%0Z+2b>Z9pYpYrI3n>aeM!fOpZL5h4n1s6Le9+{J@Q;(oy||J4G0i*^J#DtjIP1BJ813Ha$>45lbX0Q#bO<{@K&$ItL3=4@akotec2a$vgpFgWfT9%2efWE4{q<F-`iOde$(64N!6T-m&vU8BB2jG(?~#=?siVw?nvHK8pT2$WKi?i~Y$K#}8lU6GLc|GFcb0EkC{vW#_c@yBl!?2q`Z}B1r~Ja}=;`gd559w$mC{dMkL8(NU<nR~Mj^RD76gTuMC;xMQhPq*%vkD)?R<cF!6QihoV{kO4ejZVTJ*p%4Rh7cP4R`YD%M?gelV2sYOOT9zw^EJSD&am>}$r>(089#|M0DBI-68sEt4xT$O5{PTiQg43M@hSkQgm+K)|;mBL?W2>b^e<O#7U#)Y`^v*vs$~M_9z-FQ*chVN9w;O@7QDFnz*YVhUiBP`W>6H>uqrLC#517*`l5gmeAE56-Mgr^5md#SKyfAx{bF3BaWx9wCD3OxHW+BqlP+YKCtaa!p*09c`pga{Or^uc_w!SW5*&C^WA6GAzCF37`TI7jC{H3F1AS7yQXGtg4~F9iHcG)7OjbDL9Us49g`6!LT<NAO`zXD9`gWoy)u@QqUpN-MMT~o}5+((qf_cn=}r6dSkLk9&o4h{*pdC6w5D~`Hy{}6>ZUE{aI>PDI0SF%0R9glM;M3{Hf8h&zWUs>e`m1A;2_dvJ<vBD{7$&rd{-%OD48W_Turv@dyFLKv&pQS2LkWvYvt9GS-CtR8Rwp=-EMf>fupL+L6F(+0OYb>E3S^kW!t)ho7@Iq1B7wnn>xxoaoe}84PBKz&yeHp2J_y(L^^rl#g+HlJX^|VT@4O^EvSS$tp$IgUwhIWOTfRQUaQ?Wg0pP5lHkRYbh<Ro61Icxlg!5)A(c_5VGJny=->6LXZPZ2bd#D-XC+E#Ju0bz*KTu^k!)}J@(_es|hlH%QXMbXa251W+Q&v!uACE_UB=QsJVA(D82k-WJD7u(H|8qks8UxF4_#exc`D4U#3L{qrEG+wD(s<lnkzjm>;}bv{i@EU7=R6@*iX|T}(r7EABFF`pV07YyhJ|FD4*bhUc*=DWzjNA-fL)0H%0#z&yZ<Bx(TrS7VOIfOt6T15je9nvV)x=CM=#$hNAWR2h`yjB+r1(TT%5cc~ThFf4U~TiTn)0-Ku}AxZwtv)+q@9pV&kGlz0E);yIpzfVZePC}-JWa@zDX=7LLLqe)(caz@@Q(YE%#Mp+rny+L<OCCR4P|F$O%!_^!(c@!Y&koPpZ(!`0>U}3ynHmg=g9NXt$Tgkss69r%^=T=9pkFs^LEIPb$rSC$9;I)z)IFo}4#H2tZmL)9Hm5Qqbm5sU9E7UUd_gc(F;g&k+)YbEAIS85Q=JcN`)JX^Ee4iJrfH`uDp0irEg)bf?s+0NrR2!}c_>PyH{tu_(q@CDFS6d_yJW8jN4b+m5{xWc>YC`9*3&4_zk?c{)?IubcNniTW2&?bv)=~>Olf;{d)p7T=3{E>bKS7{ui_GyKPQuyf<muL+|jQ49GMniUsNfMh=*aYuJZMp_v`fi+s8~NN^ibo=*_>1-F#_U-lcR`tbnv6l$K<u4hXvjTv2NFWOCY0;DRVUk=_{txdjRjq%{(@F0JuyIwP-q?OQ^Nfo8<O1A2bar50hsYdVS3+-+5ULPNolC)+*gc=v5VCHDKh57h;kP!vfnzh^W^?i*rWm(5%w$GG?z+vC`+A%ux}wv43wgBI<?Ng^@Bh>o@JcC!!cu%E?U8<f&93^YZ2CUHR!%+%%<FKq)qK9?nPCSdrg+3HHc6xxbR8Ap+=2+hswB5O(_628^@{&*Muc>C?AKi<p_Kfc2IcB!?#{`&U2`S~AfsCW!VZvFaA<8~ZtzNz#c_b=?tv6y51i~d`Ns?_FKef#s<_rE-rKoQL;F7>)UV-xj=%?=Fw&v<KfRPr&pEyJS8dW-#gXhPYs4l%FLLj&gGTxvauNHJ0$pK*PU9{1z>zkCbQe!f3jKmGp8Z$Ewi^}oHn{p<DaVvG%EwVhg6PE1;*#{+R23tI3=6*4{k1fy9Z-?1SzSk7ZeVOa2&KY#i4=YRk8?XW3qJa@x$`<-v!|Krcbe{9ekc8Q8=06(mp{nMD2j-zYc%){6)VuLXqBly@gO_9wm)8k^x)}x`ew&PPoU|o67$C(KSt3~<&vA?lKBvv4A$CNqF#LdHJ1tAFl6^#usGyJ3GUOaA|PHZ7MH_kG0;)Jo`^0lkW`*VfXWoeYWJ$GE9i_Xgk*vU4(BXH4;%MxF2biAZSeb(}h{;qslm-X`)^!yZnY=f3wiN9`-uH`rN#T44XtPzb}eC98)^W6#g>)ZRsimX!_qOMmnDdm!VRo5a5cjo+|gr!5zw0ykQDyLfbCqlnPY66493eg1M0b}_PiRi*4;K?D>Q&cw9_w5f|9j)`Coc}`IPPS~@vt+kc>c$4NX{r#=b3MkKjA9S9zlsjtZEV;QMg1uXdbAV{{@astKF;;p^fCi%(_@H%pkA06W#rM5Hkrl?;0Q=Zk!ajx8dqN6Mmce!@N|6mrb9S5*}A8bDqDhv+f3RB_APG7{R6R&pH+eNyWj0bgp5-33I`s{r%+Pd*JlYb7gRmS=q^6ABZ(w{44E{!Nu$NQj{o}m>+3&4o#gwp*Ptk1@qnmycJ9RO!-;Fs!X?y}fN|H|?}S`b*dk;n)|zc8WAI}R(=g~Xjn;<(2hbyi&x~nQDOZ^8^<yK{O|av>UL0o4os(%uNT(zoGF}l@0*<L6)vy7_WA+Y?hQK+r{{GuQ#?XlZl@L56#E~8h-b=ktO|=mrL(Q;w!>UeeKaCN35dBrc6c6%Au@b<M$Cw(L0+16&lqF7r#l2i?WXCv)Iu3>Ak?|PG(5ho#HF$&Q8K3~XG~BD4V_N=m*&ZkVGc~>O)-($RI@fn%N83=HS)1Lu8>hjx4c68RK;DJIl$38-O25$4sHU{+(;LF_B@su}VV$NaJyhV$V5rCa?P_j$W+fAeBOv7vRlHo@gG>R(J;ZxY>zcLBv7<&}r>W@%6h~p*HIQ>{aeLsyXBCUg32vQ@q(aU;w}RJVra8g%ON&RbpgVDQkFj)+(Z-thJZYl%Df8Obp#<W=yZvD1MfMNoEv*g(4!^T=#OX;pH1!<t{#>pl;~CrYRfhi*@W^vq%BU8u-W4kU_}`)_VIYmt%0HD!oePH^@UI}8Tthl>b7&sF^Ng1HKQS*tQ|d;JMPT+)S@L^YL<kTK40g%j+A^eL31mK@5;{h?sbDcKwLp>QEF!#5z>cksf~RrIsoqek3s*aMiGG2d&JI=W6FYl8qg7xf1c4i{1qdR?tYQ>5*(CM3K5Sx($2&FE@a!|@O4RGh=+=RoVSQb<DB{||Dv0+IAk=$|Fj4$RJ0;c9pYv#B>IvcuNgUY0^X;+z`y;EC52(xN8%&KhJt>`8oP(e9geNM%pfq2IHMc3mseyAZ;Mkd?=*f#&ySoH5qJgn<An-G8W6OGwjbu72vLpM?n8=@Se?xHg7!}<@<mj|4i8>eQtg_GYmm&OLI)JkGE3yTddRm^3A?nICr<|C*5a6lN?zRs0JxGSEvMqa*p<`((GJYXFqRZ^wyH$VxMQWW#gcdJQwUp-_o7SX1THWCQ9F3vmd}mlKJ=)*cl=)NJhSb!oTO1ZtWkP9SXxzk$JiY08F;$4LW~bNh)m6O%+v)7)0bfyw(<~ZD^D;dnL8(lhNa=y`sUq^qeh47=DbmRN`n1@#Cp+|N#554+kkAhrD;mG?XIWH{tbA9x_-Mn9IR?giog1B<_q5Um@TR?=H21^du}<BZd8mC>3%I$FA)}?5jLn*dMaDJT;F7%ob~ltm5YogFeHa!7`@9NZ5FylCK8ircMS(sD)^8rCjP*k%VEtTcI5)5u5FFd!gz{a02M~(3k#?73WGSUgF0Mu=A=pLgydT3|W!)se*TPVJnp%;)5>1ak0hNNJ9^=r6AQp1z_>#z+8;JvOYGSh-Wnrm>Q}^FD%u@nd3SfrzslG?2E|D=^*cUq31hRpI#0(uzGkW&KHeebHwSvurvVN5)HAb#fqXz&GjrsH@YUX@>9;~Dtf!dKfpiLX{8A#r&c~Z&GL72w7mVkvzJn8c+Q)K490vQTg1iRSNd6Dhumq%Um9HA(gs5*Sp35^vOlntG%l@k`t4H70~bd!YRDSn7Rb*^4W8B{zxq?xi@7Ocvlyg<jW=AQ1x5B#I^m_v;VJK#i5F{O+-=2E-Zdu<msV5@R{0@X}5KnR7f7r?b5+bv{|?c3Rqk4DtHjGj7t=n?TSo0Gb{4NAf;FDDFc#2=!?72EXfQrD_`c0Ac9qp9`A9Y7A}CY9$JW;$5p#MyCtJdN`1SDgo6rYw#@N}lIjx5g-a95ft!ki<1^)en&&jrFi&T&N!X_mlAD%^dR*YSEjH4AA*caYKT%U!=HojI{&v2-JoilP*w#Xm)%QRMMvc?F|R$F^fJRmP(Tcwuw&M&teJQRfC5hvhp^Pw<s10?KIaB+^6+P?zvv=9th3kir<t>bK*hj8gcAhpH<NN9Rj~-9ur&QWFWqHF~xnBQ^X6aaV1<A!>LISL~A~oaK6>+oTn+aUNLHGwmZt)SXHC+7<I|HrEtl8kulET&1wk8@IqIP1Qy}FrzNzMgw^R5HE5IoHm>&&5^2PDPhA77W|W1{sr61N+3S6i@Lo<!(%f(WMMn_{p(N;A0&_ri{Lqx3Mtd7%_n3kVu5$yG6J`mLImWFfKz~ovnRFTz<gYPTw4pkMFV5~doLlbvK{o)MFN!h{e2m7&vlmCfL)e>%um{F}17imaAc3EABj!HP8}mM9npNUf$8^JXL?-VAnfpXUAr`#af%?(Y^vIrcAyrd5rV}wjXd+5MR}d6`i#9l+&)3+nJ@gl%Yy@_Ei9{sZVu9&_PiO5&xPjx<ccZ`oh@Qp!CErrE6sCaKsiTy-hO+t*H(Y{gn4fj5*dE*-l00IS&c|HWMH7zvPRk!3XYtE0s!Agoe3M~9>0iibu-w_kjyX&n`qr4%+MJRlE>8NK+2OfbaDR$x2g)!j`AvT!uf8N|&=jZ0{b}<hvnw*5kK<N2i=yl@<oxC`)G$GVtect%KO-$>4hfCj53_u~GBWD}F<&-&kxG=i;o2)tpqF9oRJwaoqwg89zc>R^TIgouy3?e?*NE7ap$j8!bJ0i}9;M)mDsLA9L}&A47k8RtR1E>qk2R&N+y>VP{8dnRJBB!^2y;fx;u!Q-H*?myfM8%kT_X{@Su6mhc8MzBLLqZK4?(DR3O#*A=#-jxUw#uTc2w%<0V>#&3}ZDRLBYfSOVi$fJ%OWIRwf~nLC*@!JcE>sdwuLCOk>|BM12un?Lx$EC@fy30d6vMw&pW)NFh8?gfE+US5t|G&S<=VN9g$<Hs>Yvq#dJ7F|cTg)roYWdjG?~y-Yhya<!KjdWsrBCX_O7ucHJ-y$tF|Yn6G-Gtr8auOT4MYGz?}tTIoX#Gd~d|8FjNrXH5vBqFRX$aRkM`^R7-&U7jn46Llih0l5<ZUZZ$&j0_;aZd^T7vNo{>0EemtCXaqvq+-G96sop<a!-TDRNDYrWcuNn!=rxg0z+pZ%fs%!k44LWD@o)5}$j%bpnoy@z}KKRflQ9Onwsoyjfk}W0Grk*-&eaWpVZWrE%?8q%`XST1we_YS`w6V@qJY1_yBz$x@u5LmfiLWpPR;szOd$fmN*tC32;8lHvCv!~kXJ%oF1Iff%Zw#DT|j^!A|~L7|_mW|U(AP`fb*#}sl1s>dL-!R>{qQ^dNc_428LT~`ZGdr2?@A;jprYD!iF9G=$hm=yOH{~P{xDAcNHCx$R!MZPT69`*r+x=bgdk^@whW0W?Na&(uV<Xqs}TpHBAwYSz~l1cd~p=Lz-S{i)3+)%_YrwkCI!3c8B?Gib+LQXC5K9e}~isqT)wC2_OSQc6N(|Z8AUNV9WW3Jtj^I5$VrNpcio+KGZcFh$x!n96JJj7J8>mZyy!f**apUpx_j`^$+9t(&(Tp0gS&}PQQ!Kx?bBO9sDV=g5_UILOqOqLON*(@b+jA+fcGF~QLOmSM;iXLRhrE<T~?lH}O8NbSZ*}_a0AP9SWZ5Lh|W(+zU4y-cbDBS&+PW5yvw^>!f@g9KCm8Zl*Zmrthg{>-<)4|sVaXr1T8pE;HGl(%^+tMc=!g{D?7nm4k*U%a`Orh98+V*_*FY8vo2b$$JQ;*#Bn%`!%Pko|7xNrwz05A=RsDGjvzO<^c47DbR<6uvZs~)(ehkZ#fB(mZLRt2Q;I}(2(7;@B5&ZQti4b>b~DYz-*VXba*s1=Mgkv-_9aQn}CSV~oh=9Yz|?xDO8=mzrqD#iikg1AYKOv2+j-tRh$GJ|5AiHuI8Pi&+*jfZo{wx|yCvszlT9G(D9@*kyDmt!i0rj%-mM6#H(K7Fo3Tti5(q8k1Zaq;^3u`Go0BgGxeYmwa%(nLbq{G)a`@5QS_uHl4A|M7dS)98hscx`~T85AXkm4#zs#Y8c!6ojqU8gLC&kQoW6O|B*_ZrsMgQcacH*9HSCpSjFw@|<2)93r*La3}BERzg^;jya|NFN3C1-oIm@YhTwmI&I1pAa`W*Y}vhc!v<R&nZk|M>+85>Qd~HE=KxjUqv(<fLOSs_k7-oZSf1=}WHAAbcQQ2Pb(%V<HFO9JXZUhEh?L3(?@X;zl?xuUh3p||dW<rbx%Jm3hX|_;YBvMj0ZmXLQ@(#ycrfQWJyTdWrmRG6d>@qWT>vc&k&hv7&mmtgD3bY$652J^-cA+Y{UkOOR~FeVZVSBH%0ViDU1vsbFo%-|{<GF?s`)60G^);Xf-t+UzV}Xko#WJwA=Yja6Fy{=wkt(`<a$^0rdBm5njl&{O>e{Db2&yDWy;ax<9EQZ>SU+ZQVrROQ@gLzT=C4Q_-3BoSt!{YG~YDpuO_Ppj*6QG?I3VC6G|ndeuvIwc)voD-njWON;H!LwmhkU^(xSJ^=0+kp1)dFy?9J3py7(29;W9ExmK|3xrPU(ECPryB_;qrZ|9`$5%{szK_vhHa=RV6Cy;=N<=mv~%ymkme(2)@Xg?L`Q`znVNO{a?$}<97{G<9gUT~e0Gyrp~Rv`UKameJH%Mgg=a<{h@m1dar#P~h^tp7=%hdKsX<^Ek)iZ3$omk5viY6s`u`93K!=aCg*3GDk1fvPI4A^6UN|JXJtXF{PAxe9W7(o58}LI5<LTg0TH8`rPFLI+LG(Yp}M6rW7=v?`(ib&;7g7`J;c6`rkAIqe;nbqS5YgLa5XJQH#50F0ZsGP{Z*xF4y|V<l_L+mnhX<np`<Z4_xxspr#vENg=6!aA`w@D|yxoJW-G(I%5dr4zO`@KzZ!BS2AILVyaT)0Ig#m}rm(N3M-7yL~*M&C_$u9L$m6{y(F%b(GO=8A@ARaKXqP-u>mD-!%n;Iq%o`Uwkmd<<$^87i)j!v(|`%L1`G2gE%f0hyFG0BD~LJ$%iv%Ys44j_gA@a5&+j{C!V#Cbl1BP{pm}kbd-af7u3V}cml`CO%|-XOt9%;+KH57(9`(gjwzxmC?mY-w348u<T{V`|Jodm{UU|)uA9(l8#&A_VJvvl$QP0~z3rVzmscTr<4!@^e^KbsDTk;BLDwaUnF}G__J{d>`?!C;Jsh5fQT;Uf$B%{iU#N*7Q<QUpZ>o^=V*Ad6iB6f9{7Q?wsZi+`p7LSu-X&by!|a*BhI~y8JRZK&KVd|K+~+@rS@fF>g|>RaDM~6Ab>PDTLPM=xroF|Ls_S*qs@Tr=(D5MyUo!{Zr<4rKAlO>}_(>tV_d>`XE#nLz(W(2EzAPdKXn>j|*9UBT`z@hQx$gV3^@&gTD#p@`##KBF*)lxUdfEUtUO?@t*NtC>F<GFP{B&19m;wFxq)y{8=t+fCaK#+<Zn=_$u+c!{gF}broYJaJ30Hc~V2M^ys6wZLXuOYhlZz>yTmK?J>nxgCW*lQV`SZy;yxV0Q`e<ooE@fZ_bu2(n5;<^pmxi`G@aHK<B6UZ6#X9%-Hbb2=LuFD$79AUOEhb2r@iWb)Rdi;{Tu5Yn$H!yGJJi5)?K2vkPuxqqB=^p#+uWBlB93_!lq&h*=j{HI$(>&05ba|EdPAK{#(fSZBTeGkm6AT9o9=bR*>s5$+i#l`xH6Y%eA3m22yLglZ?~jNlFOv9F-q;+oB5pTBs%*K<5T;)&F$A5`QXQ6aoGKw+x)-k?O&ashE~1JfPXOy9^{5_($LFP#rPv?Uy@+?B^I9i1oY8;8x~!|$|rE6PJy5<UQ&YX$H-TC<d)*krh0>j#U%*P$Gdf?g~`}Pg;_Dv;cyN*1humcq7<AQ(J3{rh)SBc%n{I?H-!4d0uqmTO;SrE2%vM_*$O|33n6{BDC{i95%a8L8E{EG)kV&Uvjtx1W7Gl*9N?8;0VnW#h%_hVm$>`L$6yzIiIIUY7OlgHk@_3%)phOw&#TPd4H<|6gC}-!$BvW5s-G5n-umcEfZr|(=cI%NEZs2MjXjFAv@{EAkq<ol$O2f)*$7xLu5pLtJ%CHH7ndeoj`2-0c{t4`B%0=Euor@<g8JrCY62Ce#}TsZWUhUBDXSjqe9l)LofWo{?gg*NlW8!wB-<k*2<ZAJ%;xA--KKMQV#J<q<D*mMh+3rG-eDL_Hlg|E{my*<_AyhgrnF>w%D<|md|8Vef3y%p>jy)~1|#&bYmzGKUX<gPZBLjf=GW7-A)wk-<!&dNzKu`OUUX7Q2s3$zr4bO&esTFlXZD0v`o~oFeF-Of0mtoUSvMqHWTa8jUJ6ylduniom0=4Q>PWJzVTp|SA*}uT{;hkz5u$UHWOx7&%99^~Q@k4cV;E?P_-^7nF_@_haW8<8AD>Hiy7JlHmZaKOAiW|}#+Ra+i!8|_hjcMs+A&ezZ|ui+|9JcDr$64z4_}&aw#Uo#+v~4yznh=GL4Sqk_5fo02Ia$ou1&QQSWxw~LbY{`k%4(m!c&l1=yv`7gDYL0T4^TN^}N=oF0A%{XFmk^_Cs@?c`aODx^*(z#j*Q$|C_?A+s+v72U@Vt+KlHHKF8qI2(t#vnBJmWo!1<f$N!<_4*>+$?G-Ay55!aVHNSe<W-C1HUG9|N1^8bvOR1gM0tb++l>LH5EzTFBgKK>I4{!kW3r%w7+vn}yKWZ$&Td1KMpAPWHvSqsCZ4Q(calPu+SVvW=Irp4Xb)GYs@YlC@IHpNuzy9$DBEfcBha<i;gid~hhu7Aiv4$S&U;g~%*Ps9W?UVob(?kJwVD}4Tf9*72%|RB+*JCYe$KuB&wx5XmmD?QVllstO!&U;udOobj_G>hzc1@e_fRh;Yc`|WO!WjEt-X#i$`^xOF5#{pd=;70KKiv!LX7?Eex4AbBnTB0g-XX)P|50h&By0V1xRjpyM3f5A&{o$T=&|9sfL8*YEUCMTHC&;;YwyYOWF-e;4`UjHae0yr)>!-Q*L&Gj8mM-VYt+sylMkI5dTn;|r{911?WbQ4dwD<I>y!o}>y>d?CH)vnM8xX6MT8qJ`VAIfflA)k)L$53b<R^tSYk9Mu$Wa&%=14DT@(hG;tQzP3m&PIE)V^OZ_;{zdEf3B)vjm4C?lIcG&`c(M>mp;BHJd-ciK)x&u(X5?sL5wsYc3dja^p!1_6|5p4j<3YTGQ=N?}ryX%M1lwR0&WH<vU+G|xPTL3*#}7J0XPNw~s8#IH0qRbXlQ>|5M0`P;BRL1~JdDdWd<D%y?v`1$ad7!@_{&$5SpF7ROtc@V%QRUiygPkZYzq$NmDQ2t26Vf_FB44r}ZuuFAvvlfeS2><o>*VlhM#N)IMJ~kD9n<KO!R=^!|U-H|B6X!$XI7G>gT@MQqgrQ;L*-orIn${+nO*-Z<HC^-cp|vSCZ~#35$0yQY_pwGmPsTB5UCcWh<9!`v{tM7uJ`D-p%fw4dwY;UUXKMQ1ZA|f)i-V&fxF^3{tNKyX5CyfiGbcdu;eRF-7Cmh^jiEnHngyDLMF6Z|3%nHjG>-Wqmnfmh8byx}k1);*CkIvmB<A8C)$=?x01uGZSLKA5iC`l;#!=N`mk7K~w(f$*b!sZnPo=UxS&npS%CsOoL-@V}56r%^j8nxL{??ZnC0}Nm2B=n)(q5DW3q*DIPk4zZIjP6o77UxZKSs@#ea5h7S$yXbVbYY9UYQi#%lp|0TfG>=f0UT?IRc(q=ojz09CO-r^fEKUvA;=T&uJceMq#~6kf?6Sn!$&MStE^)F5F;E3@FX))3`%(qIyNkZ3&%jC)GL49Rzyp4$%rA%j`D}$-F+RaBd|dnDGqvbU6pMrP-Uo;rB96txF3j@g3i3-k-}#Wqe)x>19;QZ0`zXZ2WH#SHs1o{_XAUU$0?0<$UzYq|Sx2QSq;!1iXe2a&j!*8&l7D&Hssc0b3A8Vx?vjjyc6^PoJUK4u1@G$>71ToeHSEVuXD2Xn|2~Dt?U91p5^6L5$${A5Ud}W^6$tOXOzWle;&#=7I|8IF0-83%(Jl?ll|_`h=<C5a;9XLxM#xY`RS77w8{>M46g~;qA{&Uh7T`O;a5O7tahG+zUQ`&0g_F2(|*_>AzHgACOj7@Besvx<uVEA@;RJj&ps&Lyz=BrW#s9#=FQB(V1IsC&bZ?^!PObSOiXpc%-er#HVEg4s*+oUFS5!G|E^;wTf#IB(SB`--!Te)O;b9f2R<N2+oTDYG)3wr=DP6uq7bM42*<>`k!%kWHu|<a2qg`1&U2n!3e~Gk;-I#-}`TS__OP;hbhAsx5jiD;$=xx97)f!b$Mc4_sI8+QbHbb1@Zn(4dT+)6R3(9$v%EOK;e~d5a>_N_1wZnQp<)dAKhB^Zd*Pv!{gM{jePW$LKBqS&0~i88_LO@0GoAGMr$vA$EG#8n^uD<z`~<?M6@#u&k*fzY}UxsLgp%wV<qC|X1r*L%XJ&|Hl#MhI>cegT_$}-va?>UOWl+$6adXo<WWo;*HC+ZO-O)D4HlB6USCmg(<~b83;zUZOfr%3q&U6!ul{}rjT+OoJ=sk-u3y9;G$}e(?@E6m;Ejdn)T{FByDXp(l~6n6Yv5+O$8H{qs{0#yE1_RQ)qiyrfp!M9&u{_sM`X)rfh^Y7c%jo+WH~+?GqZ=m?oWJ%=OLsoCXyd4x(BI7FP}XRx}OjoP7s(WAQ-_U&O-$B4$D;f4e|qWfn4!6+y*h#VZoQrHQaLpn*tav8xZ=(2tVR5D=P*h90Y#MVU=w@kX2@|(NH`Q=T_#B@c>E1n?eMtRs=ZVWWr-US8%5(hB>9Aty4E5UzGDq`X+ozV46|-z&a)Om|P<C*0kmCqfLNONFso>s?eOKJ+ckD%fh5!AFZs^6rB!+S33q+J2DJN1}48|$)h+=Dl<MM&Ey_%j*t5oSnX)a`W*gS=I_jlY<-fdb{!Am9N|%!6e~ob681^10T_A%mGcbF4blfjWdYTo#D^+Dk<Lf`HncLR?Fo<_(h`NRqKIOyk73O{ExRA+RmXLNnkIlyRqx`a;>E{YY8OSiZOsQHlb{nMRT`Tc1d76s4&Z2!;T96i)*Lm|;Sp~eW5N$#Ma1*27q9%~ZNLb2dAS-<BOMYguE^bBm%5f`V6pCaS+WNGsPcAJU9&>ww2whnp0`%F=5BvX%4?T*ldYH=LDwQ?Yj`n8b^olU;{<G2@0){9=^=qPFH~swyG75YVGUvMCpt09s3sQevu>MdeF(3TdfP=t?1EI-t_Nu8K()Fw5VsHwsj1!m<()tmT}3dtk9c1C;8m*JaxBz5JA2%Q7}oeS$PuX}_tk}4YFg3mSZeUlfjX<N*hSI9l*suQ&H5zcVXrnVME}CZG9F!=ZUk?KotI4xk`jPmRvh;rXsSch>Tq1>5$33MCH6U->IIp3zFKi+k=Hq|j$pld)Fp38BbXchumVEF*OFXCZZ*r%Q8Er+rb&{^y03BwK_ih;c)e-$O(asdpr_^rffF<!=>4Na+Y|J`csZUmN~`Ftm8bN~^#V%hHt!YL2HCl%W&P`rK(T>cr(~9K3l$6l5t^^ao^3UORa97W#FEk!f72^R*xw?d%<5#^Hh)F-l-Yw1If}F?P(tt$8vo1Q2?f&O%320EcQAPKB8QDQjvd^`OmCB}swa2kN6Iy%BfObOL}|fQ;6<+s!d$u}*QLtWzIJ4$fUnZGiD1Q;_|1(Vxp;`>xgmp!E;mg4u&tvE#fD7#5tmznsa;XZRA_MCqh2?XH)3)wUQ&+z&RuKa$JQ)t-xg2v;5Mx?jH>jOhC*b}M*0^rqGVQa%Ix|zlv~c(&Pv7*9i@d5EyPVx$i0;+>1GhFRVhP}0bCq@Ktn$LRmk~rWr)O8vE@*6%T}y0rCWIB@s6>|d<(=ZfL7N`?)hpjfNgYYJEcXnDIPOQV}72?Tw)?L)Md}oXSN(|@~m+wx(XyARI>I#Uj@#4jB?b#Nwii71^fP#u<Hp>yT=eGHI2>)MFPc9fa+<y6)-R%d7SWUZGD%z@ljP%fV8jYAy}d$3v@{tTdrgs{dff|c9hiZDL&hi4E=B+kmIq@RqP2rqDM)hOhUv*&kD`PfzZ{xK6VqPv2PP1RJoVW73=W|^HgaV$QVAAo?Z~e&=n^)Ms-Z45)GYEPXTAjd%10DKx*naM!Cb}etY(zYof6+0%zBrVhNIW8PpMBm3fruMYA-XAvVbor}LAC<s9_%9INCP`&Dz4JpoJ=hUgNql8A*=<>wv|f}y{)`*SUMHX0@@O(e8A*9uRj9)n%vjiLBhYk6p+9Rrph1KSfBPoB<jT{^EEDmNIgOid|a?lZ^_hV^GkKl3z-zcjpMA!1deTVviVYx9$b9aUsCc1QoPN~DQVIy5Z%pI&(>ayg7<D4BwtLK>EWl$H?hO6AGI<#jNIECBVg5J`lo!+TDS6w40W-+9-P=9Bw(`?IC*fl&MoBB+p)GOqdGkI>#z2R4=mTPW*uVgNR~rynY82(wTeTDB&U3X3hOSW%2n0ukb?(yL<TW-{CU-LHv$DlY^<;UTP;x&)YT&8YO|i(imIlYPP1no=hj>MtT0P|nq@+1exnLPQ9pxuwo>TR@I~(l0$Q9<-k7(r`{Chj)5Rk361FB^{2)HMKT7v5Wbl6kBR9)oGy48GW~>!^~kqb`Zv;^4R3R5y#dw*P-pGdWKM7o>US*{<w%-2-f|WU`kQR_+0{mn~99Ni&AK;*z^Nfi)#l8z|c|RIOZt_Ba2#pqC6(oM`j%AiXVA>)Q=%geH~W})XK0oTI`*RK9(r@5E9f0FN<Vo0Fo+!pDN2Di_v;-R@Wm;0BJ1bSaPwHm+zN&zQU8FBG#J1OC#{?U^7CzDZ36Cjw530AI=o?TW|AOqtq)<`Doo=9V*SpJy<F7@gq0m5uDdyEwQu1@b;qgD+<QFaz}%u4*V~#t|eAJEDMHO-SF3Rqs?@hzcqf9zqN%q)Sz&%aOeeN!=e3Zllo2Orfm?iVONACnK!5I<C$Dmdq6>@1K0*`iCc>(31By9&MVujN?mzRU>JW<5+xV<VvWHT<!Yk}I820xWm*e+b_ZCM$L-<mx;)D~rAAGvM(Q1!vDwE|ZcCrUkBRVIe+{Q__253$Bv-aQpFz)he$a<v^#Sq*lmOwoPkoYKVSbQI0A>uIpmHd!Mm2-B3er{h?sKse6{NeJL#`cYT+H+0;*ph<r6M)s-1%c7OM=!^Dg;N!|0IuR3^6%p646(1;ha#PI!ERUOhZJ=4>94#+(N2KAX%+dn?yQa^@0Rdj6EdC00jrnzh~5TZpR4e5KDRfKju@1QRWbhv-!~x1VOLgfJsi<78hUOT<2%y{wRzq!FZxqL64Cant!b+YLfzLlb;%&)v#BBQ)F;-xR6ZFBIbWYS*z=*#PeNbr;K#D5gLmKZlW5u@f>ijDUNEFa`T{*N``S%9rkWWJ&v$+iD269N7JIV)uILT&_rDg72Fw1uB~t+O?TX1$C9U&zNNJ#Hdaqz=6rdPf`)PlNY~K~o6pIGylIJ^1R6Ck;0@)yKL)yV)blx4J*D>$ZfM9=QO8_Kf#rN3THjH~Z_}l~IN!VXYz*CzgPpKIms?<|<Ce)b<2()TyZ~;RF18|cH{a$ljjFoTlRf4v7QzQnLfzRku5bLNsgrAmH(5o<Te}vf^VB)IWGYoIN76>)hl<8ACLK^K>dPc(5bCsaLqKJjSk{pKPGy564BMH5J0`S7T8BvJ19JLCffD>B3A%OZWUkZpTmwt<G=EJ!sy59{l-ORt`uH^{3hfY!DYpeS{FakU{dk-6th2RorarefOT@V-J<!LH=LCO#UxEIe{5l5^A49C&HYa@js1itu4bAl>=QUC3a&aE7ZvPH{NK)a~1yNJyO|2$U98<LGn#7RPS$2#xDgdE})o)~HxQI^8xf&A3r;e>o*vIqZV!zPoi#B~)(M{x@SYM<aIqC_>SPk2sf|lS$&f8?A!O3@%_Hvr4BsBlD-X@6+LaadDM;WS~z-T43y&*+?OcRj`SiBle;3k*lNnyrUffceRbxwE`YFTvz5ru(-dvk^|o;h&e(z56JESX*vpi!2HiJ}@z6Y$;!UI&$Z2rveBh-VR~i=%9(WH1kh;h55>pYa$|(a#&*UqPx<o>l4MMAy#=m1<G>;aS(F&k)2Kj>Adbx4X)0AiU9xn6^uVOn$WkB6nKmx^~w~Bo6rd4}sc!Pi=}mGffK$p#qGaQ%uC3=<^`bAHEu*KI78^t$PO644(q9SJ(xyl>>q>7y2O2IW#>u0n=+_=A+#TR-;2_1o?YS_YT~b`$*CAZ!g#RQ;E`K+`3x2`gH3eGpaE(SFnM4xFp>+(6LmPxli|)yKWSY_bxY?kmc8DGFdrJmLm-Wc`!XfUBVagL3+&;$Lym5BP1FLcl5pl_I3#a8FGAi$93^^@CZRfcSWOZVB)uZO%Tf2t6|e(B0H;mFYddu$(*L?Qc)TM>VYc3MG5hORDwWewqt6G@wr*#WWXKYunvJg#$UV)_yK&yREIDDLtRJNux7aVap4$)H2IGBXMarr7tgzS{udu=ad~5wg)=d|Mg(UHO@f>e;A*_+Um178MMtnUGA&Z9{J<9S6&1!+F5L#5Z?lse`6$vly<Kjg%hfmvZ)SsvxyO{ZP<WD}NC6w5SqQxaZ~_P+{3DE24G~(@HLM=LzXq*r?|%I;pq_B01m#oi*NjigyAARL@s@^-vcN+T5^iCWsC~}2QT7ojd?VS32u*lfx&xz~63*R2ju;=U06-Qmvd?0347W34i%P6Cfe#~(PHx1y>A@RlE59y$`+sc)-+mz}HXI`k&}myu<TxbgEvG9dUxa^LPTXvHSp?dQl<^mHIsYKd<9mwR8n*MK2IA0IfJjIese@J!Sc6RmRZ(rLgo$D*qpsE3J8MI)LS|hQ3Qb;!iUGzg-y6-ADB5FGv&DN1W##xNBvy$<+O*KO&;94ygDq^-%1*O!{8(7&h8pbh{RySN+<j*=nlka^RnKWtJ1t*$Est%}G0G0cUdr=%J!fZl%!DeOmUu-|wfN+NHrH}YxDW2~TsAS1F9<0IRXWg*Lr6W3y=LqR?N^Q(XTU*K6U`4(&rFdvN!MNWPcSm;YL<Ff;#{mKr^w<Px@L?GeaU%g2H)1El^~*rlqzVKJB%vtd!A%jRO|`LKE#-T0|LGk88^T-RQLT^bj;^`6{%uOoQq@`p5nYRG7z7k=6eimOzMwKewZE*i^B9D6B_Agnr>$|so3ivO+*|JUm9fU0SbjDDe5$UU=&+S;~DL^2c(&akh81j3`#^%O4#)ilo3Rz946(ebrhE&*EHc++D2R_M-T>5k*pIhBF*!C_hndm<u^cy0Ndry$XlfJQNa_s46AAtaQoCb+4Nl^HDGY`HW?{M@^xX~9e`))0wUlrP3I!-i3D+oy>;%@;eaJ__oyYiBLa!8(m3=9*2yZ1z`xQF?f4S+qAAVX$G$L&_ByfN4-$E(d5fjt!l2qo<hn5-%4dV28m;@BS$C#fZ+oPJ7NSfJ<H?Iv^nFU^qfJ8N@ow?x0K`9vuEG(`4uQ)z)`T)yP=1Oi(m{esnTpv$)V{HdOS%=3#h6s;^5N&~ac=z;E{heM$V9&nO+hf*0cMq)4aYB*Xp);AhsXFUN#>MNqiKoK`5gWJWI+KVv8Z_juUUvE+nwDxl-ZVP=qMK;`HQTnvpCz>k0PgO8lTMDK@JF~0mjZy2twi}M=wEpp1Elf^K=gbQ+YPgJEP^`*pI`ec{NkFO!NPIrtZ?Vyfos*E$&TV3x6Jmhq_+w<EvuIFd|rzI6w+l!j1Bui#AadjZcdV;d)onS?{lkP#c`Tn4-I1@l^+(U41B6hYu2oE|eghh%4v#H+|*hsxkl{p+^yroC-)eevm@?3I>}?5l4V|pcGg}$`Q?Ij@T}El<C7kVt^M(OwD7b=8o+sKp8Bkvl`_^_@Wb6WbPt~@1YRsgqmm^G>?%aNy^Q$-ZFxH-V_Nc2SC1Os^Q1@1vwsMSxB-Bc$YT#gg+!nTkhw`>r+S{M#S0G4Z{~79-%g>KckX)(GL}RN6bUm;Tdyj3f&s4vH~y^R0y6#kz$nr1DyzW-un2*K~Sz6q##IBV|1Q*Xh^9*dPPfxGXmQnUX**bgpDeLp1-8}HW2Sg!}(yAJ%->mx3jR@@LDk);uOxGZ5=HFFc9!kCYhX=E~`Mc6f`}!DL~n7mAO-GIMDbev`Il5D_{B|D+InvHjD7^I(Z*%W7$&IM02X1@`(Q3=LQrTNR|@D+02kKD63MF1Qra5eu1;H>UpKl`6{jt`N<HIAOd(sh?>7mw&6Z_PnCJp`PrZ=t{aSFl&*?<pmpykx*+(nNF2bIFnbsV+pci^=KcDA|MoG{i4q4d8RFot;tgJ!zHTY27K@xL2{9ERs<W%_>4;y>9}Gzz(TQk5l!is`jDgEWfq=B+!q%mY*PFJ*D--gTAVQ~!H}K$}pY&1HfKfc1#Az9}D!=xje!!Exm~_1Rw%7ypaPMPXJ6M*wga0fh%YJeHVfd%|xTRKe%M3$zWAx4@@)yNyf`y8rXr_WglKt-)?S%Wuo!iN7*n0Z;@)0b}kD0DR?N!IX3A2C(B%m@1OJAE~F!8B5rWh7E7`b{>Lg&f`QYyVEyspF6Wo`sdLpYGB5g!I}4Z(se?q%HCA0%+6SwT{W9m-Nud#4JoWULJ)@E8V~BE=@gnPyutxOD9N_*}XvmCyFJB)rR2TahUfN3s>66*panOaZDv*LdF_?aCi-zy0*boB82K+p=$uHu<;LU*CQ=KaZXz=%63GA=hu3=jvGVB}%?oq&|DAS}*Awg?-KuCRs2L{!7bOO4x*UZQ(9Fzv7!pE@aotenA{3?+ekcUHn}C_M40R?az<H_dh+BK$J~u{CPU?8_SlVMP;l6?-E4(_NfhvwY6p;Y#?c;9;42`zP-aSO{!Grk3aAd2o>1sHL;k+eY|>?SHgp_hQaz@{`}?Fpa1>slmGbB7<)Ug`-QQ;cABgP!X-jp##+?-{BddRCt_AX2@7v-jGOQr8>($E*3*0++pme5*)?sx15RQ@u?7<DO!eYSv_9DLASOTAwT|)Zuo!*$bM)}()GVT-@vw_Jt?JnD3EOq$ZR$b;zcfnTr9LjDCxab%yc!4R6@@T1JhbpippzvLSujQj^mpw&S)R=G!=wpasN-{=l!7zXzWeoVIbD4XgLaT>#H5&{_?}F1<fq?%`R)HV_btn@9Lcdighki0tCo}oHX1X|9GQkPtgh)x^zWA>sv2Dx9_}95IFeQbaT-8ABje%W{>!h2y?mVR`&jPj@IeQZ2Q2R6UG+vMZxPY>P(Q(d;s7Q++-F<RvgRojEHRoBSj@%F;_+V%T@;H@4lbadT#VW5<DviZO<E7I?%N%sl0=(kmwi68gd}WeC@@WtB#Oz6G$5JXuD;yodNpL1lz|PqtVyq0M0(d%9nYh-`8701=EvYWC_3$2O6BH~cCzM~=P2Ur_1u(q%a?>}LMs;Zq2b80rq8~`4O6}i`wP-kDcIMbjF1bo58n@<pm*x{v#+W`eQ!a0kd$wfV?;PsRpystNUKOtQ1PQ6ocP4I{|y`(W16*CgG2bwe|vxbcd7IHxG8s03y6qdRG~hX{PT|!=c6pDbS67?KP)JyUCAcDII;F<Mw=8i>6pWKyZH}oOtFCjm<g=BkOq5<b#SSTtn}PNE#<L}?WfJ>_ZVG4m!|O2ay*6;_KZ!5HpUdsxi~l)0;VdeAp<{Zys4lzcE<^X7yf5b-Sg9i;~@QM(qYmpED}KwTacyL$EJjefbgLPLVM`F?%CsyE3h>Btwag}B<5JX=92as8=@1C*yrcuvTdn}U?V%mv51F^E;YsWmcgcv)4P6ODr@{+7i?^pGC+EUh*b&?jB&<AUczYjTVH0de3>yaGDHsqc{UCYTD|v?2rJfJ;?Yj(F}DRnIU*kJ+Z>2-vIXof5hhJp`ISjqv-23O?3-iqv??)~bE~|x&~MpwIp(zYw9`g2to=<Adydo4Gm7Y4f<$!-@&$i<a{DYeVYb|0Pwm~`ZR`$Bh3XY8w`r+);+-F3>0q&DcZgO1S!Ta+NTz#V_az8xApp2Fo^nsub6{IpI1L>BEc4X5v{14#@tvmqwX9Ud*NuOD9^5k9$GeU7^l_jVeEhJffBo^}pYJlAaz1+V=+1?cF7mHni^oTeL^3o-!8c|(=QaIL%!`l&r;*rPLVa@?i=Iw20^kCJT`PF73RPgCTZVuhk5O(eevE6L&~6YGBS6vE&#^7o$3GC0Yr-5HJ|*UWet`ZG$hL0PrH@}X&Z$hIx|_>j_&8zcxkAgE`T=%fdnnuvwCnkRF9vlgEiFF&@zZw8GVg~Q{KYK)xjt-SD`>1cW-84A<JUzL0!$$S@&&eDc3NmlkKcN8@pMSdBsvUyTG8VUxBS@kekqf29o#ZzgirwNGusIPwQ0UE>z|{<;(_yGptzaGmr46Y6TS-8U|}Q@0Ql6C1Z!Hn8K?lc;w%@WSXN4jyFYgN_Z|C7>Yffp(_B(gInD0677A>n{VKljhJJ-bf|O@KNTsNO6UJmY6|yI(wXerTUgrj0{o>5d4QrIyqfh<_Um<62%QY7mpPHgb7sc_avsYyA?*98|@^n3;(0Glgz2+U8)+8ocZEpeeM#*-yGptyz_E#G*GBwF~WfDs$f;7eySGZiCquy?%4T;XKtS8&-_P`9Li5z!Rw()hDWe9O+cP=LiaDA6ZvykQ$-%;SwEE-4~GhsDDNztCj+=B&0w}Ss`z8^*x!l>kTb;|nwlW0>$M|$?dX`TaQe(;=TC5(Ny)qhldutNh8Zf1Jyrdu!fPwWkV^>-gIsd>MrMt<z0tV#r86Azo2%LkNh`E*<QtSrD`D8oxjRaL#Qb{ea#Xdi=j_KL;*p%*SYCzAMrsBN*lL(WqZ%)oT>y&QE~K@jQSQw)PX4dbf@ef?fLJ~a>_fLDsqAmtANZ#qoCn(+w-JRfto+fM+Xo?;M5Pj@Yz#-^K}Aa_CHkMWbJ=b@bKIL5ov{KDiIO*>P|T~p4rmmA5kfZs)LXY^4XA$rRFUSR8OM_T}1kh}nE%b@AYcw`$SQ-lOzqAgd3Pn`~i%{m6SbR--o(~`Yr#iKZluD$|@l6dD?PQ2heKhx6Dfb?x_pqUFlO{;Bv6g=Sd2XRu^OOP>5OO2yo!Qz_H(i>Pfb<)(JS|pVtLu`10jRbacKI)%Cn{O@@9}-?gQVdrAaLn~Ftf{9x^$V$)xRy{uCl0vKu}m7$A9Go{SjJ<h33#(W*F&iaHZ^Dqhg2LywaRcC`Q~Vj8X{%I5zZ*|<*SIu(f!I*zPt_YATBRwHgCjb)Z&^v1#zhzI03IYQ{)5ULp69=FB~w_GQR>-P1ls=m(WL@_kHnIIcyqr4SJF*IiADY8iVvT%dDS0O&DYH0*SL|EC)D|`*$?~7ht@89~*q`?-}jt)Z#zlJ5<dj2j<3abiLNWO*lqpB(}TeAX_ITx0{r=Gg9wsHlYJ|ni4g929{6(Zc1D@gduAd$?f!=);|0fZ~Laqk#zcbPAcB)2HIjZ&E{%R%vCnVvWVvy6pM37I*RWNCKHV2{vsz~uXY>6=fc)69uu9;4{unV*3Ay>x(M!bxJHYSbKSUBLE%DRFsbGe?S&*&4Kj1Hz&+ikI<+|~az(uGSB{v43ZAys8I`uAQ_A&cc|=N%LDiUa>E$%X4G2d7?5o<4cuO)Zqi9#|DwX254xYN&*W+u!*)kiv-E3!>R`#z$0tE(kJd2sdP0Bjv%ERMNf&xt2QUE79tT1L7Y1H4$N)Yj<NceJ3vTR$vBCB7EV3&@08*t)Z50B%689AheG)fsn_@JXa0Y!b-GJ*~%|9N#BzzUNwWe9yRoA6Y7Jv7rkRJxFKj9KoTS5g95{b*NQ6P_BKaJC>sN3Dn|(>3RX`jGp*Be4eDn7&;EYsl0HJ|{E-4TfVfTj_SgoDkbgYUKj&^)t$NwzNWr#4=}EEvIwZV8-HEB{?O8?W3xW;%Cm;e{R;wc5=-&a=s0&Fp7t-WS~v@8!Ey>@dkzyaE<TQbGDO{M?}YJrThrGmCMoolsZ!@wJ`H-w$WZ3NkQX4|B0x%sPj#Um|-j8rl8M2fSDbVkUo=p$5?He1Y!`Pw^qtXUo8c&lS!s}ZV_)zAb@h4-xmqYn!gM+$1^WCR@OuE)lpg0$?YIZv<A;$PUk(S#5HgbKYTT>j8y>qR)9x7hB&&pb;bjd*up%A*Lp5sU`9r{;O53sHFe=tfz|-)-_JuJgFfi6I(os>I_9woSZtN)?Wv>3lMKCdBdX(B-m54RengMBbsmjqkDe8pv;%Q$dVS(1j6>fhC<uC%<TarM4q?>X5Qj0SEj_&;qM<8JZj9@gjI$a#V~hgMRQ7Vmw1CyFbc}L`8UOa|L)XM3Q3TFzJjE8e@G__)wwkBGW(BRXZ%UX|lvK(&A&(07G3fC%GRU9oS4}Fn0@8vp9!6X$W_8v1+%wow`dfQG*SSt`!(=~+OfF}L;rY^Iu&cc>6zUr-4{af282Mvhdm-D&6B(&Xm(@t^UJ1s9JkK%_Dzb;NC{3YbFE=F2b5Td#WJzP*ENfu2hph^?9w}pfSS_wYl^T^;fYU3VXS>Qrvz1JE&f)qhp<`zW-KDBxa(NRdA`3vXEJP73o6wb$BgL`<ovN|4L+4?C_MY-^xViX-N1qL2v1N5@%=oM3gp938M8d*_tI?xjKOn+-ciL9M+(KqJzdK8zwJLMrQFsN*k7+#?t{E-3W+jVcvTqo|GB2Zz`Zoa%C})}0J7bWJfD#5*?7U2Nhd_;XF;Cqy_A|3C)6D;vN-qzlkZx4p?P<wMXmVpR^q3m=fd4n5rR830X-*^`B?^_NE*NS*-1sjzHCX&POt2)k6JB=%JZyDPz^<k=B59!L(JsY-0vxVNPihitFtV|)-^b(RfRGp?T&g*Y>uRfIJ|{0TEU0ZRDGn!huGX5@m}NFCt|qww0+$o{DUUhqP8C`L2H7d9@YE1{la<x44&z-VnScyI>!{!d33-f+k%1Lmp8w<qz&poWX8qtY0J5n~iNcO7vD<)Qg%6Nr@XZ`=q%LstxcQoHw3o<x^M{}H=5I1vBvPa+FETR<6WXpby5D53!Ul`eaYaZvZA&uTnaO2YR^<LCh+7aSrCHaxfKmm$N%J<jT0GekC=-R0`6ey$M`N(5tdy$t!IYmYNM-WfV1R3%P{(x$00b-O226I4Y9r0O?e&CO)jfia21^%8V|<?Mee9Fzk;x4*T$t{7p(TB8b!8c@&5)bH*MSQhxCp&11zPS)2RIKiSfuboCj;XMM&O*pIgz!%-)Pl^6ezgJ0qD;}HNA8B3#l?&V=V=y!2^UspM00Bc0hO*93WubOx{xW%7~=wF5Bus{xoxf8EIDvCMVq^g{?Z$UW-BG8H43w!IVXYd7ByWzPBV#xzW8_ZquuxT@=+(;7Q;g4PMOBK&b(UvOs?jBj<0H{ahq;+EGu>z@kRhuL_|3GZeWS^IC1^i!{2BmUdNT&XSVLt=0fTB?b9?_xbN+^swCaZpbW-D}3cn+S=nc<$>modsaj_4$&a_9eeSSaGO{Qx{ZlDhpsfC85e0xix-~}-TK3_oeO^(TKZV`0#&X?7RRvGBvP){+cuq(lgv*AxHOGv7^<3*jUNMDJ4&UTbDI(r7{*1i11v+W2EdZEPaU}^{SZSt@PIrTi()+Aku)7CxMUf&N-`Md(z%HP4x+DTAt!v!V;o!opBEcnSrmqkoqB>$j89G7ICgS_@NN$U0gP)ATHyFW^(MF2^+VbN`BZ{9M(JbyOi_=^w8Zn&D2G?jX`ro7iUs5sj7Qs=pY(Cz?n*ok2^K)+R28(rAF@y}mnO?)++M@hH&64=DIhIckG%vC$%{r*aNDeYd@gX{;~Q<Ny3aXJKD!iW7E9Ykl+?M4KN`*pJxv9c^1g~X3jsJb^BCgNZFA&%Nc9%vPlEsn4F6szO{KsLM+`jASklPx80O{{`zSg`?Qu~U<=WzMj8v7L&@-BM)H2vYr>xf^$+%00R5sVr9JE;I+^23DM%2CIo>*U8tsHgFQ9GtH*<}q_yKK~uLp~gw{IpzPXF6u7(E#HBX~QI;w(bNkg6Q9pf-H46=k-NZxp#xlt|uMt1p{Z^W4`-f8j6UJyLAQ$+0{#5sd=w8S24XEK&Wc5k(7eV?O5C8=2DIT?$8eLAA<Twq^_LY;N>Y^2LIG+<U~J%Y=50-8S7Lk7x#4ec53WnV6#gd&3d<To)Fe{C};iH|HbA6;O#QR`dxxi@}nK_vD0`j_wK5SMGyV>5GdKxQWbk~npOZp{H0!2%*9;5+dFyyO!vHT=bC;2L4>GmpqddrY3S8(bS;*K$sV4i$B@t?7*EvssY2CGcb&~$Eq2RllL;~8lGrKVLAQ<`LUF89pFSveU?>>vquO<Fb+h@l_{?#ZW~|8)L%Y(!-H^}4ldw`K%0vqbBMKUm^|BEXV<jDba;$k1<(#Qpy)KXKu`W*4LdkkBa4*HH6caZlkzsO=$gXWR{a?9sQN~ARfJ1PBB$kenklQ3sOk+*Qm@BS{vU>adCY%}mLRO0LRLEWO&aUTx2ixFQIIVGM69X9ej^t<mUIO)<ck}!&KGf#&>W1nwb$VA^Kn}sC9Y=EwPV}#gd-<ZwwKPHvR)qP)NBuJ@UU$2cC|akcB&G0GG)$U<7@584w1RFZsFQh2d6QCZ6k!R7v%*67J!B(5tWZ*ahehI;sH|p!IjIs(CN9wS&!<vc_9@S6n5X64ZuSK6mdZ{`;Gr04D%oWipYv_7eMbr>D7Lae6W$h=z-Y&UbN7^4#Yam(ob)1}CMF$jXN0GUfHdt5Ba%)Uv1RjvI?$JVUHJC@+PruC!Xh_6Ml9M0wxy60v7n%w*_V7Ff4N=o+UgAAv{9$xFV-^UURvmRjth@@x4UeCDGe~;M*tC$FJA?%qrbVEj|rlRF$IgpME!`n35UOT)@9y}B(^EnS6ule<QhOiLSSnhp&u%ekUgok>a+^1U4Dx;&+_}<{f{3{7PZj|I*rfqF<Ezp`px!jlS(|b8z*KuR-)Cbq{`;@IKJ_68r!~OlpWNWlrZpm{?6c=F~%p&=>AUdw9OTwvd_MOfm|6qDNIEpF7=Sc^sG_$WnU_0g*F7MZV+%D-7I$J6ghw0vfEw`Mj&0yl7|URzSsUJXKLa*daoE2`oQyo5WbZSK;BGvJaOlxvIwNey>Dd`WlCg-q7pG$;DCT{DI*3*Z<c+36`ArqUlAI5;JB@~mzb6m&AOc-TyH~B&S%U+dBLCvQ-qAS|1I|;+}VvTf>@-IEG2NKb=x@CZ~WlYpy$cWZqyTMyhtE{R;$1YS8%<py|n5epN+5o%RzRBWZ`3aclT7{mXmXi6!V2lcHFMu;I2)(JVSbsRFZ5_iZO7Bcj!DZ<GG}JA!R8sl*yfe`qVU=ED2&qX5`2X8E$?0LbfOtc%6N8vTF@WGamYUbJ_>OaPgvpi4Ar1Wi7}ZVj5w&+gxe%4+EbnYs_?oV`r#nrEn0}-Irzd_oJB446*F<ec}Eh@Q8C4@(gQk!aEq2f+mcpW+<j(kdd&R;I{y#KgPe7TfSI~LAAx6J{OOx-iy0Bb%hQK8hA200On%NLD2<^scnADr4c)phFme^x=^gG!~SBr7^8Klackcl#gY#;=FqoU$Kk~!25j?AfcNo0y&%1wC8^Gh8Amf!@iZKl%r6*LI}O1;&fFQ0o><4}|3G>o53<w5@7hQyw$P#cS7y=A^evF4wPCTy6DNv2#cJoDx!#`A9$dx5NRT+LHu{CA6;Kmphyc!o%*EqU-+kQ9725%ek0QU4mQ}CgHE>7EIsVOGdApPba2x2Y0NjZN$cP^#*_+M~N2RWCFb|ZFsrdP5Mw4n~=K)h*1J~FXLNvHeL#N<HL}Q~A3zTzH@x0%3*7|r;7aw&GLqKPR-BjLs4xC5=X_|b%J@y7mY>XT}_E9MV9^*IEFpzN}X&&H6#-Iy+$kG7Y&yg=LAsiU3URN&xP1wT|)CRMs-#)GWnL;l~cnUkbVa|E)TZ6l;lnA-o#iMBQC0cLDHT0XdK4N1KpZW$#gk$Q0ctLo>IRo+wUJjSBQHsdWH+jZR&9{OWFjMS-I5(P~6Vt3*m>5u<Ze_z=!$ccPNNKizl;JaVWaiPP8l}r>P`(JrxQhuP*JQ4-*YcQ=>ZD<XY8$3{40pB_x;`wcMTj<&91jPhvZY=My?uV#L;ZV7<7~q3*I9<z%#t#wo>NT&7VIgG_fdWGIh(tmar&OGba5n4lY|Tr6yjTT7pCuGs56%6S39hjmuU5NyT$C<^_!0y^vAc4nU0i7bFENm{wyZVwL!sx8^dYeVmth2>hM?{u<GC?Q_|}y&-oUEM723u8VIJ^A84D1kBDD9J`8`Aoq)g8+wNidfmpPeeAKTcXZv~mj)hY30@EEJiOr7+3G}1d5M+2ae8ltI-~g89&zatDOE1kg&J2idalwQkOJZBnYk^PA=M*K_gn6Ef!Sajv<~;LA>Zn6#Vsv$vhjWV8_vIJ{nj&6zY?Z)FW9IIH7yk3_a^>`Bpq6kr7i#Xj6&Wke99t2Z`u1f>G`uCT-~0Z2=zsh1_g{Yd5kCBU@b~S)hw}dGkAH;EBby1I_@npv`psZVk2POa2pn;n%#fas>*XbbZw*4RX~RmM0lrekCbVk{cj5IF-&}%(xMuMS@~UTFn0D=}a87MqxX8c%`eFFvR}ZrgI`M$XFT0Mzyj3{gSgT}ibV67?H2js(n#uZI(M~-V?*8@12OQJrN`d|P3*H1BaI7K`iwQ~kzFePcyXCM*cmH4h^KZZY<-dOa%fJ0+F!pg^j|&rj>@-;omcpz(56kS{=dVi}{~~5avf7fujY-oEL&K>F#(J9XWBWbnkhrGJcfd(hG%+CC#ki%<bjOoD$3fch=XY2Ey8JXfYkt?b=~p~$n!(L?UXzA0F)kzTi8I;-tx@upxM7`p@<YnO^)N@*(%;Zf>cJa;4wBU!%lb^w?~UhjeKC^;19-Yn$KQQXO(huj?#H^Nq0706+d<wH`BRa_bPR#|FaP-4-+%e_FprPZeILsJV!zZ!sY~KM-j$F^^7IfgZ}k(b+y>x@L&LttG@)vaQNa?UIf2Do?2Hos)zBlcIB?(s`iZV*!raTd{^g3a4qx4sJ4Utp`B_R6o)0ZyV;UOPE>j<YV&P)Xab~xxFZa1#4L=uUfx#YX(hm_4mUUsI^Qdi;jZ1|5L#$?wg3->UR9-FVVrZUuj^4{&&rLbAd`Y;_q9Se`8bTgx`s`cWFy-5@zo0>ZoGGgi;VjTTe1Cb8-l^lyj+OLBT-W(0mC}aY=()opbGeEk6bEOiifX1HGYglA>8?9YdrPD(j6ez;frUunttpfD^+V7WG2t$6gl$H1Omi|5*@G$g#{c}c_xFGQdP4TqCH1#ak_AVvq=f+{e$3(CNB0;@FfKDq1w1uK_7zWY9cp$s9debG+-+9U=k6-xQDZL`J?a#aW_Fq!kKEXhsC+mS^hjC8N3!t#%<2w|w_aEa!1r1Sa-6)$4)b^$>y=-S7^I!|$vH7J0`p~^#IR}11F-GPuV%Dl$8e;^JXj!bPNhu-wk!Gsk0*iTKJ%4b)KsW-rE-=<)aNlEiQSWn6^)!w3{84~>&H~)7lE-PEpr5tm?u&{#Yp}<6Z8ykZUK$Ipj{TW@k+qxb}b?hg7ygqHjpwi03ASi%gw!=+b>}?v=N<yehpshxQY!3hB6kA!Zx@)7~T|5ALGlp)LKT(v62O-Y@Z`OFNXfj6=JE^W2lo`UHc&NcQWvfBL*-^D{(yzv!6bU_UO5NK3uv59~Go1;em#i^FXM)Q$%Ti5$9ik#f&37hO&NN{bu~$bi>%Nl7N~7QC<}FoESVZZov3Zwo&V#FqxlI8gDSJPZ{wL@XnT1H8mGr09~BV!)RBsG9NGZRU#nyWvs|!*pn@VezC2zPUE9*Y+=e{w6aB$X|1YiTpq8#w9s$abvfp=_jGQ@$CxE5Sj_u5ifQN>MfAmichgFrfj>UE9X*_TT5hnXZr-btdhX~{fNapjW5N5*T<xiYCz{<M3VWft?pKF!y7x8uf+z!aV6?_l?&*3CY%2?#fy1x7J}Nnx_$kx=S}BG(Nv!$n^RLf?i!J$ZR4eqqC4?{-RPxs!KmPgt1mVLj$oc5aqdS*kUYz<+i;sfM`|aQxb2`=Y^gl5#U<=+=-e)eg-EcvOp5{gZQU-%vE12gB2cu3)WoaTXN;}2FRYj<R7K;&bR^oBNKK{`auqN!u;ZtG`=m+R8frVKMjCK6FaZcq7)!keM!^a6j&$Uk8)DN%=%UK@T3Jm81zSIlhiFy3A-4fgM;Rb)P8how~o7f6yHIJFDc4b_&y*e5Uz`==LwqJ%lkKcN;vsyqeBsvUyTG8VUxBS@kezA~o9bD{A#0`SX5!(rYFKxasK|iAepo8=BO6rS9@I@283OtA~5=oQO)RP2T7aK{3Tyd5QQiMLG#N8h|{risnC3Q~+qiZ?AikxP5^^=vfA)CP~SYDfRos}UlkE^f=U^A^(k<{AP<07wf(?ay(%+3wFE6~Fud<FM55*r3`v8KL}<8hTReD~hn{rAyigj1lDycX24X-#6H)!-K0O(@x}b|!8n(dcUHR~6Zfc50Gb&7@!PsQ8l9>U$Bxu-!@<5}jQMSGLsxfEi2^Iqs%x<Lh$B5S7919KuQq{=~+2Y0&K~ulSAvmuAsG+L%d~8KQ*tMCP6b2y`p>zvla4wBC(M_g1H@?>`9<Jv!p9A5Mcf01m@*nw2p2-IhX9^}!C6LAaUev6~u@*+*Ia2)O$m#=nk;N@lS187_bwP_~R#e=25cx~;Z!dyIbBGZ1$}pV;Ykw~>Z1a%FKk$mC_I+3Dtc1wNLA4Y#NFcpAo64dD8{c5iBMLNR0k(Nn%J_zi>!OVgj{-NnZo?zYKntGI&I!c%XHr?FvpiOf!^Y@6V$l5Gan?7%VJoyOyng>7{+o7|Oa-%r;jHh>)3O^KrK_@+NX+LV~TK&0G`wg6NhaWw1Qqv^hQWE<p9gwSASKv&w&Z{5l6RHMP-1?YLhL}ks2M{ycm@e2@D@b=`KjK_I?rlq4x_1g$pQwL&NZR?}T>90SClfo*p<_(BYBs`K_=h%RuQaZh<L4im~TZVA(gdqt`<$TmXhc+uYm9K;%Dm6!<BvvnQ%=Iy>sfWYh3)z^smQdix14>sO^$SVp)Swky?)TV`0=N_bO+u+^G&Sf1hwdHqBniW9<Y%KfYPhTwc{}SyldmG8t@kTE`SLb(`nbHDa=sD%QHyJm*~F!G%I~~JOOXPsNrhl`4=%@ZDd$&Uo#~pgd<^=i^S&>>V2aIeuR%gmYBKT|kLQ55#zcM1JEK8KQ?8^Nm?0G!TLRAL{$1P=eQjtx(B6B-96hxNiuf{Bv$28S_ZywDbtqE@M5mtPcUZYJ3Z@#Y-7^wfY&M|-xtTWUeukP*uy0D7I)uV%7RhZWoYp=B74&@BP<b}V$Wq0d-GD=)g9LI!xw02?o{h0A;=u;x)?7i5B4l+7{?w2V)|qR2h4vuA6*f-^?e@bR;%unXy4k^A0rbjh<QdA$b?jQDjtf=Hq}nsIUy>9t$jsHlpB9a$`&4HwVeRq}gZq_7X5oY<jdn(^EqkE~4_L0z<1HYlaVmp-j922$NW>?vH!Z@&`~f{I$9UHY$lmXfB!b0h3wyMTca<LU+Xw&hx4(i5XhGVtS7f`{0RXM;Uxx&WChR&Dv!$C95futMKO+mcEd_ug^kt|=!V`e}n^{>U{uBvr?@8ux%U5JCnLYTBql^K?OBh~4<A23F;UGJhvMhtLgTaRvSvH#_smOh(^zZ1{vfOp9gl4iz((V%>F%nAQWI=F?T9N*OT|)rpCDedx(zj<|#h5b9XZ~tFhrX3=E+&B^8%25LgW|zeJ&;c%d^RVlop!~>L$X2$-$o@g#m}5`{oII^?b6{@&bPrOJ@XKS45mnbLq+Q>6}4LveVzH7?d0VB(2-dwBY<vRa%5HISzM{Dm~XQU&*E4J8n^kTz2=b3H>Id*(?r4#o^CHQDKe$JpJTO&0m$`_!DT6fe6<THQ)_rA=No73v~!W)=l9MxrM&>#!C4M0*2Y7!RM*89gUup{&8;E-I;Zm<RH8YRgNNrwcOiW)9Qdsnqt`r)ZZ4cLUnI6L&$)dNQT1bBMh3Xxp2lJ`^~F_*)qtnp&qJ`<Jd?aA$*>ZvQAlHD=0Rm<dn)1aBt!4oh{kw;bCue|kLVHp%%c&u(X&ERY9RhhuTR{Bap>Cwg%Hn@vL-mdp-7q=sw@VU{jeyYIbaQ*D8kpz9FtL!yEBd?;7nyNcZ~0?2AyM+JIv6xXCJyI2Fx5gyYUoT_`u7cj!0^rBtLY8gXi)s36zRLc{w5DQE@&7J-$YN_>=vrN##TUqeNh2gzO<^HPrcBPR|Vdtv#RXT&HwlV$MXFn{%S@jOa1g)!rBi){T~jHq9}V`!TS+khbJ$i`1pdYMOSp1Ix(FvrJ%$te-3*Q}EZzEd_H!uqDxHCNCKCW?9RgJ#1B0^=Jt5!)meny*pAKj#oa<c1??BBAJ}1!){f=x6TrLOT{DQ@+M$H7Jz11h$7q-Ur=_WSazUO3!J9xANFS}-vgt9Eg~pMo~R4=k0Z4A6mx^+!4`^<j>p75g&8E^&N-n^YZ9qSAj8y6Q&p|p)hJaSo^(O;yT25gyRr}jg@>^0nKCs>=^!}SbZT!H4l^&K-DO~c4^W0REwjdy0s=8`F4qL6IWLplqfjGC%u5f9ugpxT!1B`4%UmfGhShg_n!*xd+nCHfrp7(^|BYyGx!0Pi6J=tFdgZAX);DmRb6irL39S2=;8uXgMDN4^D_cDru&*kOs2b>dv{Z4R0QalXtD1Hij7)Xw*n(WHx*Xs(dN<4P$B@UqCMkyBWH1viLaq7etMbu}G;YBcA$be{8gigQkBO|dp!Rd(JH!3jPZhylF~@wZMI2dH++wzpC&>k8HRXv$q&`6~NN6Ry4i#1(V(XvI6!iB#=W|yHN+8<Mx{W?6nDKG2g5C3<+|H5D+O=Uoa#O4t1*lmGpaBUBZ!4?ynALztQ{noHTkxq)gR;>sG0(diewKH&RTRUJr?GN40;8*;jaZ}mP3Dws5XKN!gd|?Kq!yAHSeB1Rp;v-L22MztpPvheWzcmtZ<DK2ls$MdrA%3lQaDI72Aj%Xs;V$d4$IPI#Pg;DT%4!u>7}|n!j?WIHmM#VwKQWB!XF+}Tl@4`u5)DG8BS}OBsbOWuX)?+S>>vq2R$a1GdH23fOL1>6$^;KAcLw~&fW?gr&9AeoWj^AIVID6WDj5>@CCYvxq<9c#Ht~kl<W}|>o6&`h$FZ!9k5%>E|UU}oouBeev%lnV<KyTi`1(4Dky)Ed{bv4&zUGf3NGcM(jG+yUSRJ$s5cC{cgZ;U@XV`aC6j~K&FRm)T(L`n3s70ef)+-om$rbAey&nD^XGgPL*G88GKx?L7Psf^lEk=ey6yt!I=w1DNAX$(#uC5Wd5nCfDdeR@L^6k4`ppuyi)@PEgcckIZsfzO(D<u0ZbHhtG2hkpG)a>hA)QdTk}QqC+-mJ?R5p{_0iUx{MuE$1?*_@^_|R9UrHy(tg`3rfAy8*&8Wf^4&nS0e?WJgub$=X7>n`+(Tw0c7_smsJQx+0<C>23~j;z82T$>~zxM*?qLf-)mAsD!Z^3)##T{~*_oLipqa2R)1l1eN?tsug3*iV5iN@2wGFR;sx4!xKYDCLx6*!EO+PRm2fuvN0>IPb)}D}aaQi=!AO@^c>J;Hp8r*d5NoAbb!@Exli9>D)k$V<#yNZ=_P_+PD^>yEHkvWGZVn9uhQ?O7)2R-0>(-=S!AzLU$$5hZHOz+pY>G;15|irb}DzGH$PRbHsP<ClsO<t$AO9^yI}Sir_G-D4z=)7#l~M%<yy0lg~fKx#!YGB@@o#Gz1?*o(jzNeRcQ`^5Yy$dkk^uwmI^dpc)+|ey`N&n(l=XR|@BF1lRLS8fEfLa(K(Mxn)EOS5mv~sp;fxR(R~H7R1UVtm`$tVq9L$q5L}sJy!}onp@JQspENOv%%(c?3%_Vbz8Yx(-+z*uh%KgjcK$eJBUPAZKGTr^1a}`r0MWdcB`32K@`tx7_ul9%uLE-lv39Oh6mDyOA>m`y-+H>=Um_1BHVp64~1mNX`Z1$cKg!jZQg5rfK1#8aP?ZmIjVHf1Z$rIUv4ft4xpv&P?{pJlSEg|$<RHc{g-9%@3h7@^pg|!7e1D;&iZrlYnRrCAHFA?S!S1&oV6L|ls2qGR?hmd|BFpu!8@afmA^!><VRKHWst>B=d@Ov+9GDrZD73Jqns3^z+t|3mo+Q~^~Z-mE!``><UT|GCN=FXgp5xuH|8@h^pIrPaBU`dl6BcDsA>4RfnCB5N=)Q)M<X9~)50S-QPo?eHbl%{J^`si(e(Sk#eWPAxh?VToS!Nb2r1{7*$F#f2Qa@{tIcA@fK_5Y{fG<PFV!{*x}lbJ>QfQs&M8ICDST5Y=e_!jm8@!J%ajVq8^XtVj8}RAPvUH$niU@$_>`(>+mj8LQv4{j&#Oc(lhe-Iq~}aGuScNXqVkxq-5}@jULb#qmndfKOeR$+Z$UO}vzbUmmWTAeyMRuDkW5bPF$oC;q*?$rI~|j6YyoLKK!!EV3EgkPwd2oh1?2#~0tpN<$qUiKavy9PU7^j#rDBZ8H1{aKB#n9vrG%p8dR9Pn_&CY(A0sURD^J67{ukd<^JrKX;PX_U_0qedTys{*&H-_;V)U=hX}@Y2F8Ad%**%Acql%3M$7HQ1bDmznpHY>*+vR>4@8j&<S7ASC1WXezT$5zvosUre_?Yr0B|0fO7tkq&h4A}DM*zRVA7Qj~F#CCzh=Y%J(f9a~*Q^CANh+vV&U&3sTGM9Crh_+7_D};S(a4s`{^4i{w!!w-DZr=LqzWIJwv-D-I~M$F6d7aJEuk8di+masQwrqt<+jeKTh-=inF)r9)>SSfAU8iA2LuJzeQN)&tv|&tEIo{4!~z$%Erm>%1&roo@Z<~m%jKpmDHda^%TUmsu!<*Nt6|Xwi=ITqc9-2&r2!^HDIm7>75|`l_07!Y!~CdzSivMRCD*Ez+&e3#??ze1)M&M{Wi!i`0p7m+TspFERB0!BlVf{t?SQwDcN#nY{`>#q$CE8>1mR92b9^k>QS_=IzeC+BDYusHFPqU=39_%MTASM*`^F2`Y&(uocJL`v7S`)|I&%grZIO^Oe8<zZ_kpBd&l)o&3Dd+aRtM8tat5j6vM&|$L3_+q#}hcGuFP`h6yK87Jf?0tGZ^!CwMsqYgei9UTZ;_)y<&an%g*a~`1+oo)QucF7P88U{+Jo|m~)*I+Z0$5r9oodz>xvpQq~R-VJ-XqDp>4$zEUD4f@5aAy+p^RR6Fd{;(8m3>TqM86%d5BFt=Fmbe}7;8{K9Ak(DA2NG{wmx~RBpzTg6^H`V$Afl9G_%Cq~rDXBX}xHdEqfEt%*9~5{#h!(t?16*&lE}q1&Hqu8msydMQbTflxWKZMGueY^VE(KI1bRp+w<UOJjd3{}viQZj9fm{5}*_N*t+f#5HHybKTa)7cq6rlV1WN6Rx^e|p~AxSOa=*eX}oUlUupsW_G?#*!PQxmi$Fo8GqVdL2Quur@}XH+XP^aWqEBaihOxow4P%mruzxo%84^wkJyQOiD6mOZA}BZCC+44kL<m9sUeNzVR06*Jc%@9})$cz^&xpesbGwh~96dpqa66tv_-sY}uIgQV5dgZIkLZs%;)a?>u0HK{`B)92!uZl#mBnwdD3g*G^vieLr=%nHn=27rDOqFiC3n;(;Fw4J3;%gOGv%GfdR{l$U;M%qym2_<QrI?A486b`Pgb-Z=d5|AcK)#gPsHf2dA2WcE$Oy5DWlB5ePPR<BLm|1vg!3J|Y&)hhg>AI(ZxumJ+t?^QE?Bl+Ri1HQV^nX5Kcd4GNjU;sow$oi&w{HRct>a>52o*J!MM^U>^q&N+&ZQ*XF~8MDihVd~tdDm`J`c{@?7w>)>AR0{yW*f=on0glQv^Xw4@`=RgGV4aOrQoRItDXzN&>}}0+iH%VyP;AcJmddEttBP;Ct9iIspfaQR6FQc%w;~$xzz?M8Yfu0iNdQxN|XN2q9l3EfGiGtF(*BUa9kqXRdqN`pBGtKkPT)btz7Vqra=@#mhl4%1_~ssq|H}ISq{uQ!Xt5TiGP?j1w5&QfO83{UY`6oU}YGr?0boqS+a6ns(UFgXq`<k!+Dp<CxI>wGNc}R~?ekq7e>g<4lkOFz>Edn`YaOQtHT^dVIBwI!#tLAI~k+J#)U1uQVCur20lgaJ$9Q+x43d^ZUoQkC~2?F>|djX8tU~%(ZE%v%GlCfWH=)_BEJlywOY4Figfh855)`To5f;1Ctbw5^=23#V;NohQCUy1|dT;hBXSrqRo*dNBrS>-fo!`_bP>C81Fp^4L>T}$dBwyFrgbh`#HQ}$Yy%KExqj5n0!Sv{R-v-nF!gE<Bm?vk$k+%f+usF7(3+`8_Id+kpz#VD;Qyd!UW(QQ@lPr$1u<o@w($QB$#Q8W-l1SKmV>f*YkWYVY(b>8`cP}$XM}a*@}RUr$T2%bAEU*3}4-Se?IiT{rLMYzx@awem?m7c5%$!fBo@~@Ofl2;oE<pbA)w0)?BiRMX(Vwq$dLZ;(x%m1|cZ4VYMCxv{J?<v}+4@;q?{Y+~(`JX7LO1s%KwR@A_0TZNLBeVf^D)53^7NF%qQT;ZqLtR-puAeO0;939<Rm&`?HeCV4W8cIw%o{nsBKa7?2sQT699coQ_fF|$f6CS;!ba(%A7S;HdZfPeYVzy11`|N8we|Ms83*vElAE=>Hf(_}TNc~fV2SZ4P=e_h)67cu3H1>FfZCQZN$4K*eh>uJ7^?e`Ql;+i(!0Vh#WPyomf<AgpFKTq~tXt!QSe};za5dJ!P`23zz)6sa^MZec}Xvp*8y7E>VqY23x<;2h7I``zwl*b!>#;5=c4T~DQ66j=Ey?Ct84gKDDPuBbQaom8SOO{z4))(bfg0=5{y<5VuoO8Gx<Xth%*r4wxOzI_a|K%Tl`};4y9`^Eay6<BdedgC^C>287$Gd9pNZuks(ye}iVOl`>d$_Cq4H>$<i1Sb81Qv6#Q%w9<Ll?zDjl%`>Ghfftsh5ZT%QtB~z`AdDj7ky_nT<mE&=T&Np&<>TMic#M+IFJscJ<{x*Q=oiq8t*~Wlf;95wucQN;;3)=BMW&U>*@&TocsavXsirCBWC_ndiWk?DgD~cgvTAGaM2{gyXO8_35*3al@2v!~TM{1ahXV%7n8(`|$l`TV1Um_E%*czPHvkNY)D4CMg`NYV+zbq*Wv+D9L}26?&q2HK~ADEqP3{7He<_|M_q4@Bc2f^By<lE@}Z0<p)4vk0t;7<HY%Bi|Tf=WB0>?f~teWBgcugM>E=_ut~=p#@o$*Xk&^E9Keh__JuUqW2}SQoo%J(9$ep#b!<OvKEKE43LNW&mo|@6-LPkD`fp=Q@tli;qaiqrqQW5XqsE&GY9r8BfJg8@lj@$IHXH}(PZK<6v#^LHR%}6*Vjr6lD#8?I3bX!!OL%=psb!CTE1}8-i8-fUa|~uuiG5d}mzfAQvSS>Jc*y8d=Lkc$^#VMuV^iXMDU~&TuM0LdJ$)cOL&T+o2gYbGBDG31{H-rDSiZ~{`^KUNf;=0CxS@#4PrQS!mw2?3ddzLXP>u-J`Zfn*oNNi$ON2>NR(@sDbT1!gM@pJ7IXRV>%sW6|TIjdzx*T)bdwM>i8P@(Li9N?@=ov-yE<vKY)m{L9d~$K$oCZ*Cu%~?5D~xvT=v1g)(Q=!XT_xW6F_sP{KCMj4b5M>$GTr+cRX|t^(W$NRlzY0K1KY|v7~t?{nWxsJg@Q|o?=<bNWu+><Zv5->;Fj4e6?Xk^3Evm4ul@DMkAJ?)bjtbY&7(UPP7%Yug6MG%A(Z4;vNvWq=QaIL%!}}xrIFZNf+TY$-k$y!0^kCJT`PF73bRS}HF&!T=<yik=HkaVZ8H@uU@=187dI~0$3GC0Yr=FEJ|*UWet`ZGNEm6=rH@}X&S|5Qx|_>j_&8zcImz^!`T=%fd)OupwCnkRF9y>SEiFF&@zZvjD$hpn7qk55`ml+upl9cpsWb<S4Gi_1GEQ42_|D;e^!PQhw**gz7@4EPz^4^G?r_VGU6*vsxtrZc;F2<CgirwNGusIPwQ0UE>z|{<;(_yGptzaGm#LdX6TS+PGhrkW0C>_~T1|^J{iF<LfShxd9a3&5`QneA{(Z;(lDemZ(b1KZR8F(Iu7v^{X;zCbyg|V$Ts@Tm$$%Qr>NWtwm_Da^tR&g?_1wq{P8q(+b3M1P(GQJY`Xiu){C6!OO5n|J$|N~hiSkLjb?xRcL;uC({272tR#lDKYu>SGO{$_*Lln?&B6FSY3@hKO{nbW{Oij{-m|g6OKbA4I6fW22sJB~bL!$dDE6g@MCoqg@YRBD_ZG2sm4uam<okKvfk^ubJK>t{#@g0RS&7x76`Yy#7dm?iWI@A^9b@s#POBj`;m`-Bfe-cN-=;&sBIPG+Rbq$`=tf;Z?HhsCO7<TBmC~>aqv72taL?f|V09NFE2&HB+of=Jrk20$|h*mtbX3l+Dy5-Yt>9eu`nV}3XEnZb@>~vdgQO_8>vo|a5hQ40YP4W^FEdZ8g$kkK9Abb}_9Yqi!I&c)jT2D6xxt0YZ|Gwmz0fHL1aFR~L`0C@be(#$yH2@}nri!sD72yT`1xyc{u@Z-4A9J|d&rw@57XVIA!y;auhHHS}ia}bEv8Sk~$}YQKpPhz48*G@qQg$AhyUCnnEH~j}0bPvV@#rr-(gij3Wz4nSj<x^`Avp@xG(wZB@yIqfs|Z-a996E+$%n1$p53W&=}3Mc^8Nan6_4VimNKpiZ^=W}wL%?xzLwL{(H`|Z42jI&nO58SypTmUAH+!^Lz#9h#Dfw>GcL*}y@7=jJ53GdM#_F!`n(jWL_k3oLfvV;xs3vljw@1ju<DFsu8(0&J<YRUIMT#*gk<G$z=eKl(k}m)%hE-n8^d0}>IHf-N;SHv!GZvaa}ws+{+W^cj^?N#msN!4j4N5biog{rRMGO~ZBP+$dAZa;L(8rf*JM$MOTEmm094cQvOE&{sPlF%K4ZB}<E-IM1jl`iESIgh>|e9YI@#02Fs3c=RfDsOwd~*3{#yX>`W<ZWDZOWGpwmi~fB&%Y)tqr%9oKhj*1=6I#)m#Oy5{g&C)v51Osv;6z?;y4I87-UK7%%>DLW<Z5kikqecimrcUt?9U#`%xmPnqGJ#K@Jc(WT&i`6dso<bo#mF9FTiz`bUL;i?7qR8H0GQnu>FR~H#N{c{bE^PYZ@y6*`@K)7n-R!Wb0M=!d{0trEx=1Z8`-Qq-Qf(#L3rVUMWaefed%90`#%)&2ib&zF{3~<AJ-xd#;%n)qlv~Ymbd(l@OUIII$u$(buN7#$-x*0nut0}LmNU7lG=<+Zh=rCdAX{dGx0~%O(+Ym3{R|FqH$3FD2b+{nf`{fyr{ia2qqe00OLX{P%o5G0znP`?<4>7V_Rl`imaoX_=lR*CW8Maw_}9bZ_+Xm)blUt(qpLzs*~g@!wKL|;<_vUs$XJh#)XK8Qy_X&z=scmNr$`#ZGpo<U0Rg4bY@!bW%qF-+vQvr499?HJRNBFG$X_NgP?`=diSe{ES2F3!f_ZmTg6`zl%yjx_E-BqAMRUS+pG|KcV!_lIC>=dfmEG?hSyQlQediXeArr#*+@Sd!`c^V<Fa^oBjy|e^U_I!Nn}Tmy8{irFG{D1n4oSii0Yp*4_1WWOKXcCYb0b!^OGgMa-v(D*$AjcDoG<+i6=|hssy(=6$J{0-0gVpGN+~sT_aAaJETl#lL~0r4+iU{_IlP4?5d6oi7Te4>rB{jVfm^$HD8~~6A}bmDIaZrlgIxCL=9fwtS1SN4UQ*(iThyczL87Gi_l1zNro2OZ3M@Q|aEFk!cQpTWRU{}`tymHV&U;W552igH&yQ~7`&>BiTLEDG7~<#_Wf*l#Vhi)+Z|iY@ff=QUf<qqh16?B9WZ3O%bw3Y*%oadL(~-QT)-eyfz+$TsK@Yego@D4<8zCwW@~%2w_z^uas`F@suJo+XqyY%Z)9VvAVI2B4LG>tP)d3Ul;c$%24c8pQKhx6-A`!ac<i@y;$vCT_Gm<gjOl2>3%yC%#Y{w{f7~i*NAG#(U?<R0|S-Q?uoj&5Gc^YgY*(zbH#J)upuAD~nfIb|99$(`R{mFjSq;eu4pByMnA^nb7mUlk)j6jwC)}GIGu5%)>q!y9=<)lJ9(S8hewKs<1ucPImJ*KR2;TYInNZs-zMe5RJ#dW)Zh2>x7S*C17)=#1tD9_T%T_SVCP$v=5Cb1s#W?6@;J#1C+_jo+>!)noEs+6Y8A)Q|NJlo}Ans;Pcg$_Mj39>v(JT(=flgpc6SXls?Wg&_P=7iy%94VF^=oA{JZBq~Xvz6}w&8|TQvUQau`>4j0JdV)bgNq232V1D<b7FwMEH#dSJm_5ignzI}q{4!UTMpKEHxMDdJH1e0ZlUs!-~FY~ua|`&C_IF<;1q}e*Nk?8;K`;~zBi2BnwQaTB{7jbDCe3MpJS2%A%qNi<awFwwv!suXkL0?gnzVVl!>LEQ|YCC6>6pGyFGn=2{Uv|<{ney9{m4Cw71-Aee#LQsf1ti)C+4@2{%3@<&*w`V}d1xso<R$sCg#3nl8#rBdVqcBif}nPyj$z=~d0!4o0RLuvE5>>qRq8dB@uV>~eF{OJVoDc|17~Qe{M_q;BXdQ_kz;7C;&9RbtQ68Iy}!nT3i#j3jlz(;`_K01GSB34)*TnBZ!|3!l^d8SLJEpeYP54@cHooR!rAEc!cne_U8zQ<Q0Bz7yPr#AY)iP@(>kAhq15{hZHT-E^S!(z?dj1wuE65zDYL<@2B1GT7aGpS6p}dOb`5U=*llrI4oYKzN;5&C9HcL<SbO@{zCUM%y+$FLU@=UgjqAtD>l|a##jqVxpaqqx((foNf%x5gv%RQY10GCAFf=6tj8-3Ph8p2jHZo^^3XCC;-|+=WTL@(6Xmdrras9R|=PjMq*R>T~#%Q$#YrSjR@~_fQ$3!J-um{=bESCsHycB?|X2V5Bs+E2|!)v$oxB;_BDB(s%@I{w%4=nRgVz*R;;EV-=EVi?PH((o6I1R;liBa3uGd5t5?pzuZD~nzUf>zM>F`$$-UUlNh}=*Ud%m|VwjyYrz1oJCvv_6`&wWDwu;B92cXC#8_n&mxKp@(l9Va0kz4~C;K9RTNo1EisX)2hD@B<!*Dl0elsI<D&H{T1v4hWe71JgW(ilfVlEol+=E)f&3&q0Qye+vDrhFc&jc(F%n_iW7q+qTBuZ~{}Jw`s${PI$w%bCG-{MJZpksTA9c7<cajbwQhH=pI#{*1Hk#(Y=X%_9A3gc?PGPO=>Ta;tT=QBhiM2YilF83HZ0y&FM~gCk%2nfB~e8jjy0euw7XmO*mx_QIv%HZdv_U0^*;YSSk|PQE(`>gOUSKqPFxwj+NSnpTpSIcI#=u}W5a9(CU$3uzZIwW-elRIYXwad~(mA(mhPP=@K8uH-~4^n=iNjDeo0+{Q7`wF67RRVOHQk6|vgvpCdBHY}(9#GimtC(+LXPvWC<(zFHKc|=?b3{STVTP2&1^IhDG1LxS+cyiM$%Q(2Ab}#nmvrrQsL}k}E?8@fma2z{%w0MJ?LOsW|2wlI)(Irz^yK$<Z!B^_a<mZk@+B*5PoD;e$<x!+<1BtCw90z~M!k1mzt(S3ot;?o)!+uU-Y-u{Ms;o~|EoPF)8nb%yxxj(ab+p+|Kj%F81cjU_Ds3P$VMb1)_A%tCAR^I+6kv`wM>!uuT)J(Jd?u(Ij{Ip58-d~93#GLbaPpou843O_^_tD+LD<}4B?XPCJ@!<!l4iGKq^iDzY882JJ%eL(DnKq$E1`5qWt%;XW5q(}u4dCZrtTegQ2Ihr<-a;~X6FHy9a*AF`O6o^xo~ju(^7$p@LXmop#$AxX~U%6f#!thh?u9U=RB`33Xr}Vl&C!!azdK0%y%CWMDZJPZ%%(cyJ+c~H1D;hN+x~=7`QDKqEdu))P$Gi=28s-z;A~V8^Nd~GKo$S?eg$0gMY>~7^0tYyuVPijCBg7i!-{kj`#3AF~~9%iIh}BzT4zJC#_(8i0eO>WUDAI;MJI2<ptKknzJRb=4*KdW)6~Cmc?dF;mvsDMYsg$<VRIdX$WPUZ$;BL#n@D0Il%74u-oF3GAFq5_wHhur5^G45P)KMMZH=Z<uR+xWqVZ1jkO#KZA)3AUmH`NKVJ3<Kppx3V3)A(8EX{Whs;Oabd3q(VfCV`4H5H~4`u3hH7#av@gIXj&Rx7a=cfu~XG(J?NnW4u^!Y_vZJIm=w-dYP2b|zGsV-zS{bQa}pL9BR;VHsW!Q<Ygur=Q~pEi}12yOXeApk~5VUO`jzu-yqF_iA&69gYum5}gcRgzkt-&FXphB7K9cZB!q&zV9ep%&4^%{9!*Bu?nPz)2V{T1;b_1iw=Lr&7jk#FrRlu1J;<S_T&`OklZ^tl<L8StTHq3c}dDicCwkMN66`FhQqs&}uCAoA40%YhA&CfUiKdh)l8>`CuFNiV6lUrej>Nxkve}X#~J1nHdE%uoAPwBuke67-<Rhd)lV+zxd*sN5i@RpXdCnsN5A<ptDML!i@{!pnr8v`&ImPxi7CNmpTkGRp2%_CTl%&_Vm8|jJo~Z21LlT0Zx^EK_8M9O{VHZ^Qov;m9?Ut7?ArWHH|5B91wwqh44FkM*vWx>Q)Y`)G<+s$@q8|9jPCARbTMwq?)w$DbLes=Oee>><Qv6m3{EQvoz9hvIjhxhHbE&d<u#xHWb6Br!A3#(T)YD90lRnnM-K%<RYIY#uTwR{nxECoL2}3TIGWgr**k~9-3wI!+Jn6aowl(|Jw3j{KC?9IYunnskWt%LbIUbT-bnoA%D5twDSSl>H;dXGqK{y_o|h>crZ_wzL8W!t$?KgCS*6hOdACVR5tf<VmBWMN!9-f29SwirzU*wtV6#WWgJt_x_p1$NKg6m!=4{NN1c(1L1j;^t&OR&9jaFH`|tmcA5SK-QE5D_$?-9Xo<U#v*GDP>ru)lgG*+VNtIXTxc4NQs0yx`_W0W0~-;^l$dY;bY0LxD#{22a?x*NH$$IY32g8><fdUMK5{zU38w&vjLtWm#XUn*vTQWvNuFK`}fx##i}IdAQ<+wKX*OJ2=S4^d`{*XDeAd`IsUqe5S1Ue3d}^8BRU&RBljlZ1xe$vPXmDeWcdfy8Km0|LIKj2NI8TlW1`WZn0CrQ~x)j(u8hFA?A=y%;++xZZ{$oNmlxctNEMbAxrz++3O6=r%xz91`&>a>=041<hsi1s7nwspcMtSBe!<Tg*N~&z13U>p6p2kunq2jRJ`bXs3Q>JlP;)x87=fN{L}@M7L@rfFMul=J5nfq;bjD+uAG31L_C5?D8|R6xqvpf%vSqyK5FO2>6_B`7*H`1cz_4@v$U7C!1XXq_0oz_&iS!Q?(Zo$P%faT&=_9D&+RP%q6FZ5I1SK_32pJ;;X=$@_S$U08gd)4}Fmp?KxyUSZ<pn8*>4OK&~5;sC_m1S=6#mm1U3V@5qP&`~c_SbpS@)cWd_dshDRDsfy?8#lry*@LT~+CCBd!Yj5YAmx5-YC_^b(2#|Stdhm)iqG<s;X0w*tl38R)m2jUv7teGn(ZyBs#IY=N2-3s@Gaz7AU^cJepeHra&5yt}HqKH)=Ddko&F&cZ{$f=C<Kn1^gwn?juy{|b<00O-j<=420Mh=c+Pnz3rWCs5AdSO|$vQ~BlC*xs$r+&tGYh!a`JCf<=El)X&OHsxCE7)AjhA?1ANL(Xl${u-|MTg&Ybe-ApSRGsJi(XcX{K+1?5*Qs<_8t^mqofWbA4<HIvqGp&k~V%?8s{4y*`}u*2lXe=m=NDY|ndK_PdW%yP}z3SzRO+Q)EDI<LWwY{>t0MV*ouu&m*8ghUal{@;=9OB&Q6+*p=8^z&yZ%B<q-ixEhn9py4rRj_%O#t{h~tPD7{uR_y&i`7Ef%tP&-B(TP(sbxB3^@cMKjN7|dmVwO*pR+6EcCcn7{d%q?2WDbjLtT{~`9K$!1xsYKY$ur<)5>Y}^2Kds(ur}OhRV)wVi|y)E`sji2j3K%|Ba><M&lGw_!aLaEBIoUYz9G2VBH@r}TD*oP6L7sB^%(uur%(VQbKf9|a7`0<s?<Zn5(jcDUS6CLEsLnpuy?hcns0tOlZskF{3Z?R#Z=93K7z@Xb83UFS6*rgVB1G40%@gf9&HkBx}pY0o9K=JGwDEAu5*p8orjQ|KmVQa^0R8pG1A#q3jMI`72%6cvOk8AWlOyj+K2t@hx&I=AoCh;ALEvBHZ!J9M=kq#V8EP?P{h^0&iB{)LhE1Y0#ZJOkSv0V!0W7{SCGVjfwjzacu5khGip&s-s3D+NXv{u-&MrK4Oz%XsV?U3cZ^H5Gc#n!&G8(%Zr}I4$V$I+E<UAmE4SM%!fLMHd>F_-zJ1Jer1a)%h2H#Uv74_>zhkzf;A~N-Ag#o(v(>&nO?%^&o_y2X>@0;v^Bd=1`l@)qxSmeph~w`PF2fu>#_;?_sdXaokPM)v)5Z-*0hOAYse6NnIfj9zh>sO6Yk`@@6xju#{^#FiS&9+d<Rt|A3uX^1t;ksMo7jrb6tl0`<>b?#q1*Roa@*g2{QZ~TeuNJ{o3MSmuqMC%`r{wr^Pfc~!`vRJ<Lftr%|6y#Qd35#D$_P=jlemI#}7Y#9YW;2cdoawQpP5<YYTVb^%dV->W#Q&@r(Fj`GslME@nKp2;n0CzyJR4{|_aF0on')))
_ROUTES={0:_PAYLOAD['base']}
for _rid,_patch in _PAYLOAD['patches'].items():
    _tape=list(_ROUTES[0])
    for _t,_a in _patch: _tape[_t]=_a
    _ROUTES[int(_rid)]=_tape
del _PAYLOAD
_SETTINGS={'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': False, 'front_run': False}

def _router(observation,step,state):
    if step>=144 and not state.get('day6'):
        shops=_get(_get(observation,'town',{}),'unlocked_shops',[]) or []
        state['route']={('BAKERY', 'YARN_STORE'): 3, ('BRUNCH_SPOT', 'YARN_STORE'): 4, ('FARMERS_MARKET', 'YARN_STORE'): 5, ('ICE_CREAM_SHOP', 'YARN_STORE'): 6, ('PET_CAFE', 'YARN_STORE'): 5, ('PIZZA_SHOP', 'YARN_STORE'): 7, ('SMOOTHIE_SHOP', 'YARN_STORE'): 8, ('YARN_STORE', 'BAKERY'): 9, ('YARN_STORE', 'BRUNCH_SPOT'): 9, ('YARN_STORE', 'FARMERS_MARKET'): 1, ('YARN_STORE', 'ICE_CREAM_SHOP'): 9, ('YARN_STORE', 'PET_CAFE'): 10, ('YARN_STORE', 'PIZZA_SHOP'): 6, ('YARN_STORE', 'SMOOTHIE_SHOP'): 11, ('YARN_STORE', 'YARN_STORE'): 12}.get(tuple(shops[:2]),0)
        state['day6']=True
    if step>=648 and not state.get('day27'):
        state['route']=2
        state['day27']=True
    return state.get('route',0)

_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 30], ['SELL', 'WHEAT', 30]]
for _r42_tape in _ROUTES.values():
    _r42_tape[0]=dict(_r42_tape[0],market=[list(o) for o in _R42_OPENING])
del _r42_tape
_IMPL=make_agent(_ROUTES,router=_router,**_SETTINGS)
_IMPL.chassis.diagnostics['terminal_rescue_errors']=0

def agent(observation,configuration=None):
    try:
        action=_IMPL(observation,configuration)
        pass
        return action
    except Exception:
        return {'farmer':['PASS'],'hands':[],'market':[]}

_SHOP_PARENT=agent
del agent

def agent(observation,configuration=None):
    action=_SHOP_PARENT(observation,configuration)
    try:
        if _step_of(observation)>=718:
            view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
            units=[]
            for i,pos in enumerate(view.positions):
                units.append(['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'])
            action={'farmer':units[0],'hands':units[1:],'market':[]}
            projected=_IMPL.chassis._projected_shed(action,view)
            action['market']=[['SELL',item,projected.get(item,0)] for item in PRODUCTS if projected.get(item,0)>0]
            action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    except Exception:
        _IMPL.chassis.diagnostics['terminal_rescue_errors'] += 1
    return action

# EXP-154 modifications: Ahmed Berat Ozer; public capabilities credited below.
# Dmitrii Gluzdov Seven Turn Rescue and Kaggle engine contributors, Apache-2.0.

_UNIT_NS={"__name__":"v28_own_unit_model"}
exec('# SPDX-License-Identifier: Apache-2.0\n# Extracted Kaggle / kaggle-environments contributor code; see NOTICE.txt.\n"""Exact deterministic unit/decay semantics extracted from kaggle-environments 1.32.7.\nSource kaggriculture.py SHA256 bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e.\nNo interpreter, market RNG, policy controls, or replay content is included.\n"""\n\nENGINE_VERSION = "1.32.7"\nSOURCE_SHA256 = "bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e"\n\nCROPS = {\n    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},\n    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},\n    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},\n    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},\n    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},\n}\n\nANIMALS = {\n    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},\n    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},\n    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},\n}\n\nPRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]\n\nFARMER_MOVES = {\n    "NORTH": (0, -1),\n    "SOUTH": (0, 1),\n    "EAST":  (1, 0),\n    "WEST":  (-1, 0),\n}\n\ndef _shed_access_tiles(board_size):\n    """Four inner-corner tiles around the shed, in NWSE order."""\n    half = board_size // 2\n    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]\n\ndef _is_shed_adjacent(pos, board_size):\n    return tuple(pos) in {(x, y) for (x, y) in _shed_access_tiles(board_size)}\n\ndef _new_plant(crop, day, turns_per_day):\n    cd = CROPS[crop]\n    return {\n        "kind": "PLANT",\n        "crop": crop,\n        "planted_day": day,\n        "watered_today": False,\n        "consecutive_unwatered": 1,  # planting day counts as unwatered\n        "yield_units": 0 if cd["ongoing"] else 1,\n        "max_lifespan_step": (-1 if cd["ongoing"] else (day + cd["max_yield_day"] + 1) * turns_per_day),\n        "fertilized_until_day": -1,\n    }\n\ndef _new_animal(animal, day):\n    a = ANIMALS[animal]\n    return {\n        "kind": a["structure"],\n        "animal": animal,\n        "placed_day": day,\n        "yield_units": 0,\n        "consecutive_unfed": 0,\n        "fed_today": False,\n        "cared_today": False,\n        "fertilizer_available": False,\n        "pending_care_bonus": 0,\n    }\n\ndef _farmer_position(farm, idx):\n    """idx 0 = main farmer, 1+ = hand index."""\n    if idx == 0:\n        return farm["farmer"]\n    return farm["hands"][idx - 1] if idx - 1 < len(farm["hands"]) else None\n\ndef _set_farmer_position(farm, idx, pos):\n    if idx == 0:\n        farm["farmer"] = list(pos)\n    else:\n        farm["hands"][idx - 1] = list(pos)\n\ndef _farmer_inventory(private, idx):\n    """Inventories list is [main_farmer, *hands]; grow it if idx is past the end."""\n    while len(private["inventories"]) <= idx:\n        private["inventories"].append({})\n    return private["inventories"][idx]\n\ndef _inv_add(inv, item, n=1):\n    inv[item] = inv.get(item, 0) + n\n\ndef _inv_take(inv, item, n=1):\n    if inv.get(item, 0) < n:\n        return False\n    inv[item] -= n\n    if inv[item] == 0:\n        del inv[item]\n    return True\n\ndef _apply_unit_action(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):\n    """Process one farmer/hand\'s action. Invalid / illegal actions are silent no-ops."""\n    if not isinstance(action, list) or not action:\n        return\n    op = action[0]\n    pos = _farmer_position(farm, idx)\n    if pos is None:\n        return\n    fx, fy = pos[0], pos[1]\n    inv = _farmer_inventory(private, idx)\n\n    if op in FARMER_MOVES:\n        dx, dy = FARMER_MOVES[op]\n        nx, ny = fx + dx, fy + dy\n        if not (0 <= nx < board_size and 0 <= ny < board_size):\n            return\n        # Movement onto LOCKED tiles is allowed: a hand can spawn on a locked\n        # shed-access tile, and blocking movement would strand it there forever.\n        # Tile operations (PLANT, WATER, etc.) still no-op on LOCKED tiles.\n        _set_farmer_position(farm, idx, (nx, ny))\n        return\n\n    if op == "PASS":\n        return\n\n    tile = farm["tiles"][fy][fx]\n\n    # Shed operations resolve before the LOCKED guard. They use the tile only as\n    # a standing position -- the shed itself is always owned -- and three of the\n    # four shed-access tiles start LOCKED, so guarding them first would make the\n    # shed unreachable from those tiles.\n    if op == "DROP":\n        if not _is_shed_adjacent((fx, fy), board_size):\n            return\n        shed = private["shed"]\n        for item, n in list(inv.items()):\n            if n <= 0:\n                del inv[item]\n                continue\n            room = max(0, shed_capacity - sum(shed.values()))\n            take = min(n, room)\n            if take > 0:\n                shed[item] = shed.get(item, 0) + take\n            del inv[item]\n        return\n\n    if op == "PICKUP":\n        if not _is_shed_adjacent((fx, fy), board_size):\n            return\n        if len(action) < 2:\n            return\n        item = action[1]\n        n = int(action[2]) if len(action) >= 3 else 1\n        if n <= 0:\n            return\n        # Seeds live in private["seeds"] and are consumed directly by PLANT;\n        # they never pass through farmer inventory or the shed.\n        available = private["shed"].get(item, 0)\n        n = min(n, available)\n        if n <= 0:\n            return\n        private["shed"][item] -= n\n        _inv_add(inv, item, n)\n        return\n\n    if op == "PLACE":\n        if len(action) < 2:\n            return\n        item = action[1]\n        # Animal placement: standing on a matching unoccupied structure. A LOCKED\n        # tile is the string "LOCKED", never a dict, so this branch cannot match\n        # there and PLACE falls through to the shed path below.\n        if (\n            item in ANIMALS\n            and isinstance(tile, dict)\n            and tile.get("kind") == ANIMALS[item]["structure"]\n            and "animal" not in tile\n        ):\n            if _inv_take(inv, item, 1):\n                farm["tiles"][fy][fx] = _new_animal(item, day)\n            return\n        # Shed drop: orthogonally adjacent to the shed; obeys shedCapacity.\n        if _is_shed_adjacent((fx, fy), board_size):\n            n = int(action[2]) if len(action) >= 3 else 1\n            if n <= 0:\n                return\n            n = min(n, inv.get(item, 0))\n            if n <= 0:\n                return\n            current = sum(private["shed"].values())\n            room = max(0, shed_capacity - current)\n            n = min(n, room)\n            if n <= 0:\n                return\n            inv[item] -= n\n            if inv[item] == 0:\n                del inv[item]\n            private["shed"][item] = private["shed"].get(item, 0) + n\n        return\n\n    # Everything below mutates the tile the unit stands on, so it requires that\n    # tile to be owned.\n    if tile == "LOCKED":\n        return\n\n    if op == "PLANT":\n        if len(action) < 2:\n            return\n        crop = action[1]\n        if crop not in CROPS:\n            return\n        if tile is not None:\n            return\n        if private["seeds"].get(crop, 0) <= 0:\n            return\n        private["seeds"][crop] -= 1\n        farm["tiles"][fy][fx] = _new_plant(crop, day, turns_per_day)\n        return\n\n    if op == "WATER":\n        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):\n            return\n        if tile["watered_today"]:\n            return\n        tile["watered_today"] = True\n        crop_data = CROPS[tile["crop"]]\n        if not crop_data["ongoing"]:\n            age_days = day - tile["planted_day"]\n            window_start = (crop_data["max_yield_day"] + 1) // 2\n            if window_start <= age_days <= crop_data["max_yield_day"]:\n                bonus = 2 if tile["fertilized_until_day"] >= day else 1\n                tile["yield_units"] = min(crop_data["max_yield"], tile["yield_units"] + bonus)\n        return\n\n    if op == "HARVEST":\n        if not isinstance(tile, dict):\n            return\n        if tile.get("yield_units", 0) <= 0:\n            return\n        if tile.get("kind") == "PLANT":\n            crop_data = CROPS[tile["crop"]]\n            if day - tile["planted_day"] < crop_data["first_yield_day"]:\n                # Ongoing crops only accumulate yield_units after first_yield_day,\n                # so reaching here with yield_units > 0 indicates a bug.\n                if crop_data["ongoing"]:\n                    print(\n                        f"WARNING: HARVEST on immature ongoing {tile[\'crop\']} "\n                        f"(planted day {tile[\'planted_day\']}, current day {day}, "\n                        f"first_yield_day {crop_data[\'first_yield_day\']}, "\n                        f"yield_units {tile[\'yield_units\']}); should never happen"\n                    )\n                return\n            units = tile["yield_units"]\n            tile["yield_units"] = 0\n            _inv_add(inv, tile["crop"], units)\n            if not crop_data["ongoing"]:\n                farm["tiles"][fy][fx] = None\n        elif "animal" in tile:\n            units = tile["yield_units"]\n            tile["yield_units"] = 0\n            _inv_add(inv, ANIMALS[tile["animal"]]["product"], units)\n        return\n\n    if op == "FERTILIZE":\n        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):\n            return\n        if not _inv_take(inv, "FERTILIZER", 1):\n            return\n        # Active for `day`, `day+1`, `day+2` (3 days inclusive).\n        tile["fertilized_until_day"] = max(tile.get("fertilized_until_day", -1), day + 2)\n        return\n\n    if op == "DIG":\n        if tile is None:\n            return\n        # Removes plants, weeds, empty coop/pasture. Does NOT remove a placed animal.\n        if isinstance(tile, dict) and "animal" in tile:\n            return\n        farm["tiles"][fy][fx] = None\n        return\n\n    if op == "BUILD_COOP":\n        if tile is not None:\n            return\n        farm["tiles"][fy][fx] = {"kind": "COOP"}\n        return\n\n    if op == "BUILD_PASTURE":\n        if tile is not None:\n            return\n        farm["tiles"][fy][fx] = {"kind": "PASTURE"}\n        return\n\n    if op == "FEED":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if tile["fed_today"]:\n            return\n        if not _inv_take(inv, "WHEAT", 1):\n            return\n        tile["fed_today"] = True\n        return\n\n    if op == "COLLECT_FERTILIZER":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if not tile["fertilizer_available"]:\n            return\n        tile["fertilizer_available"] = False\n        _inv_add(inv, "FERTILIZER", 1)\n        return\n\n    if op == "CARE":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if tile["cared_today"]:\n            return\n        tile["cared_today"] = True\n        return\n\ndef _decay_plants(farm, step):\n    board_size = len(farm["tiles"])\n    for y in range(board_size):\n        for x in range(board_size):\n            tile = farm["tiles"][y][x]\n            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":\n                continue\n            mls = tile["max_lifespan_step"]\n            if mls < 0 or step < mls:\n                continue\n            if (step - mls) % 2 != 0:\n                continue\n            tile["yield_units"] -= 1\n            if tile["yield_units"] <= 0:\n                farm["tiles"][y][x] = {"kind": "WEED"}\n\n',_UNIT_NS)
_PLANNER_NS=dict(_UNIT_NS)
exec('"""E182 modification: Shop0909 last-seven-turn physical closure planner.\n\nNo engine imports, policy tapes, replay fixtures, RNG or remote calls.\nThe only supported market continuation is SELL; unknown execution abstains.\n"""\nfrom copy import deepcopy\nfrom time import perf_counter\nSTART, FINAL = (712, 718)\nOPS = set(FARMER_MOVES) | {\'PASS\', \'DROP\', \'PICKUP\', \'PLACE\', \'PLANT\', \'WATER\', \'HARVEST\', \'FERTILIZE\', \'DIG\', \'BUILD_COOP\', \'BUILD_PASTURE\', \'FEED\', \'CARE\', \'COLLECT_FERTILIZER\'}\nITEMS = tuple(PRODUCTS) + tuple(ANIMALS)\n\nclass Unsupported(ValueError):\n    pass\n\ndef _get(obj, key, default=None):\n    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)\n\ndef _settings(config):\n    size, turns, last = (_get(config, k, d) for k, d in [(\'boardSize\', 10), (\'turnsPerDay\', 24), (\'episodeSteps\', 720)])\n    if (size, turns, last) != (10, 24, 720):\n        raise Unsupported(\'requires pinned 10x10/24/720 terminal window\')\n    cap = int(_get(config, \'shedCapacity\', 100))\n    orders = min(10, int(_get(config, \'maxMarketOrdersPerTurn\', 10)))\n    if cap < 1 or orders < 1:\n        raise Unsupported(\'invalid capacity/order limit\')\n    return (size, turns, cap, orders)\n\ndef physical_state(obs):\n    """Comparable own physical state; market prices and bank are intentionally excluded."""\n    seat = int(_get(obs, \'player\', 0))\n    farm = _get(obs, \'farms\')[seat]\n    return ({k: v for k, v in farm.items() if k != \'money\'}, _get(obs, \'private\'))\n\ndef _commands(action, n):\n    return [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])][:n] + [[\'PASS\'] for _ in range(max(0, n - 1 - len(action.get(\'hands\', []))))]\n\ndef _clone_state(farm, private):\n    f = dict(farm)\n    f[\'tiles\'] = [[dict(tile) if isinstance(tile, dict) else tile for tile in row] for row in farm[\'tiles\']]\n    f[\'farmer\'] = list(farm[\'farmer\'])\n    f[\'hands\'] = [list(pos) for pos in farm[\'hands\']]\n    f[\'unlocked_quadrants\'] = list(farm[\'unlocked_quadrants\'])\n    pr = dict(private)\n    pr[\'shed\'], pr[\'seeds\'] = (dict(private[\'shed\']), dict(private[\'seeds\']))\n    pr[\'inventories\'] = [dict(inv) for inv in private[\'inventories\']]\n    return (f, pr)\n\ndef _clone_schedule(schedule):\n    result = []\n    for action in schedule:\n        value = dict(action)\n        if \'farmer\' in action:\n            value[\'farmer\'] = list(action[\'farmer\'])\n        for key in [\'hands\', \'market\']:\n            if key in action:\n                value[key] = [list(command) for command in action[key]]\n        result.append(value)\n    return result\n\ndef _validate(schedule, n, orders):\n    for action in schedule:\n        if not isinstance(action, dict) or set(action) - {\'farmer\', \'hands\', \'market\'}:\n            raise Unsupported(\'unknown action shape\')\n        if not isinstance(action.get(\'hands\', []), list):\n            raise Unsupported(\'hands must be a list\')\n        for command in [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])]:\n            if not isinstance(command, list) or not command or command[0] not in OPS:\n                raise Unsupported(\'unknown/malformed unit operation\')\n            if command[0] in {\'PICKUP\', \'PLACE\', \'PLANT\'}:\n                if len(command) < 2 or command[1] not in ITEMS:\n                    raise Unsupported(\'unknown unit item\')\n                if len(command) > 2 and (not isinstance(command[2], int)):\n                    raise Unsupported(\'noninteger unit quantity\')\n        market = action.get(\'market\', [])\n        if not isinstance(market, list) or len(market) > orders:\n            raise Unsupported(\'market order shape/cap\')\n        for order in market:\n            if not isinstance(order, list) or len(order) != 3 or order[0] != \'SELL\' or (order[1] not in PRODUCTS) or (not isinstance(order[2], int)) or (order[2] <= 0):\n                raise Unsupported(\'baseline market must contain positive integer SELL only\')\n\ndef liquidation(shed, inherited_market, max_orders=10):\n    """Use actual post-unit stock; retain first parent item ordering, then stable product order."""\n    items = []\n    for order in inherited_market:\n        if order[1] not in items:\n            items.append(order[1])\n    items += [item for item in PRODUCTS if item not in items]\n    orders = [[\'SELL\', item, int(shed.get(item, 0))] for item in items if shed.get(item, 0) > 0]\n    if len(orders) > min(10, max_orders):\n        raise Unsupported(\'actual final stock exceeds order slots\')\n    return orders\n\ndef shop_liquidation(farm, private, prices):\n    """Exact original final worker/drop and market rule, with current stock/prices."""\n    return liquidate(FarmView({\'player\': 0, \'farms\': [farm], \'private\': private, \'market\': {\'prices\': prices}}))\n\ndef simulate(obs, config, schedule, *, final_liquidate=False, detailed=False, preserve_final_commands=False):\n    """Exact own unit/decay and SELL-stock transitions. No claim to simulate shared prices."""\n    size, turns, cap, order_cap = _settings(config)\n    step = int(_get(obs, \'step\', -1))\n    if step < START or step + len(schedule) - 1 > FINAL or (not schedule):\n        raise Unsupported(\'outside 712..718; no day boundary or terminal auto-drop\')\n    if any(((t + 1) % turns == 0 for t in range(step, step + len(schedule)))):\n        raise Unsupported(\'day boundary\')\n    farm0, private0 = physical_state(obs)\n    farm, private = _clone_state(farm0, private0)\n    n = 1 + len(farm[\'hands\'])\n    if len(private[\'inventories\']) != n or n > 32:\n        raise Unsupported(\'invalid/unbounded worker inventory shape\')\n    _validate(schedule, n, order_cap)\n    deposited = [dict() for _ in range(n)]\n    sold = {}\n    snapshots, rows, events = ([], [], [])\n    executed = _clone_schedule(schedule)\n    overflow = 0\n    for offset, action in enumerate(executed):\n        t = step + offset\n        if detailed:\n            snapshots.append(_clone_state(farm, private))\n        if t == FINAL and (not preserve_final_commands):\n            action = shop_liquidation(farm, private, _get(obs, \'market\')[\'prices\'])\n            executed[offset] = action\n        all_commands = [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])]\n        demand = {}\n        for command in all_commands:\n            if command[0] == \'PLANT\':\n                demand[command[1]] = demand.get(command[1], 0) + 1\n        blocked = {item for item, count in demand.items() if count > private[\'seeds\'].get(item, 0)}\n        for actor, command in enumerate(_commands(action, n)):\n            if command[0] == \'PLANT\' and command[1] in blocked:\n                command = [\'PASS\']\n            pos = farm[\'farmer\'] if actor == 0 else farm[\'hands\'][actor - 1]\n            xy = tuple(pos)\n            inv = private[\'inventories\'][actor]\n            before_inv = dict(inv) if command[0] in {\'DROP\', \'HARVEST\', \'COLLECT_FERTILIZER\'} else None\n            before_shed = dict(private[\'shed\']) if command[0] in {\'DROP\', \'PLACE\'} else None\n            _apply_unit_action(farm, private, actor, command, size, t // turns, turns, cap)\n            if before_shed is not None:\n                delta = {item: amount - before_shed.get(item, 0) for item, amount in private[\'shed\'].items() if amount > before_shed.get(item, 0)}\n                for item, amount in delta.items():\n                    deposited[actor][item] = deposited[actor].get(item, 0) + amount\n                if delta:\n                    events.append({\'offset\': offset, \'actor\': actor, \'op\': command[0], \'xy\': xy, \'deposited\': delta})\n                if command[0] == \'DROP\':\n                    overflow += sum((max(0, amount - inv.get(item, 0) - delta.get(item, 0)) for item, amount in before_inv.items()))\n            if command[0] in {\'HARVEST\', \'COLLECT_FERTILIZER\'}:\n                delta = {item: amount - before_inv.get(item, 0) for item, amount in inv.items() if amount > before_inv.get(item, 0)}\n                if delta:\n                    events.append({\'offset\': offset, \'actor\': actor, \'op\': command[0], \'xy\': xy, \'acquired\': delta})\n        pre_market = dict(private[\'shed\'])\n        if t == FINAL and preserve_final_commands and final_liquidate:\n            action[\'market\'] = liquidation(pre_market, [], order_cap)\n            prices = _get(obs, \'market\')[\'prices\']\n            action[\'market\'].sort(key=lambda order: -int(prices.get(order[1], 0)) * order[2])\n        for _, item, requested in action.get(\'market\', []):\n            quantity = min(requested, private[\'shed\'].get(item, 0), 99999)\n            if quantity > 0:\n                private[\'shed\'][item] -= quantity\n                sold[item] = sold.get(item, 0) + quantity\n        _decay_plants(farm, t)\n        rows.append({\'pre_market_shed\': pre_market, \'post_market_shed\': dict(private[\'shed\']), \'deposited_by_actor\': [dict(v) for v in deposited], \'sold\': dict(sold)})\n    if detailed:\n        snapshots.append(_clone_state(farm, private))\n    return {\'rows\': rows, \'states\': snapshots, \'events\': events, \'actions\': executed, \'overflow_units\': overflow, \'farm\': farm, \'private\': private, \'sold\': sold}\n\ndef _ge(left, right):\n    return all((left.get(item, 0) >= value for item, value in right.items()))\n\ndef dominates(candidate, baseline):\n    """Preserve every baseline worker\'s actual deposit prefixes and shed availability."""\n    if candidate[\'overflow_units\']:\n        return False\n    for new, old in zip(candidate[\'rows\'], baseline[\'rows\']):\n        if not _ge(new[\'pre_market_shed\'], old[\'pre_market_shed\']):\n            return False\n        if not _ge(new[\'sold\'], old[\'sold\']):\n            return False\n        if any((not _ge(a, b) for a, b in zip(new[\'deposited_by_actor\'], old[\'deposited_by_actor\']))):\n            return False\n    return True\n\ndef _value(run, prices):\n    shed = run[\'private\'][\'shed\']\n    return sum(((run[\'sold\'].get(item, 0) + shed.get(item, 0)) * prices[item] for item in PRODUCTS))\n\ndef _walk(start, end):\n    x, y = start\n    tx, ty = end\n    return [[\'EAST\']] * max(0, tx - x) + [[\'WEST\']] * max(0, x - tx) + [[\'SOUTH\']] * max(0, ty - y) + [[\'NORTH\']] * max(0, y - ty)\n\ndef _return(pos):\n    targets = _shed_access_tiles(10)\n    target = min(targets, key=lambda xy: (abs(pos[0] - xy[0]) + abs(pos[1] - xy[1]), targets.index(xy)))\n    return _walk(pos, target) + [[\'DROP\']]\n\ndef _proposals(run, actor, prices, max_per_actor):\n    """One/two resource bundles plus direct carry closure, replacing a baseline suffix."""\n    owners = {}\n    for event in run[\'events\']:\n        if \'acquired\' in event:\n            owners.setdefault((tuple(event[\'xy\']), event[\'op\']), set()).add(event[\'actor\'])\n    proposals = []\n    seen = set()\n    horizon = len(run[\'rows\'])\n    for offset in range(horizon):\n        farm, private = run[\'states\'][offset]\n        pos = tuple(farm[\'farmer\'] if actor == 0 else farm[\'hands\'][actor - 1])\n        inventory = private[\'inventories\'][actor]\n        carried = sum((prices.get(item, 0) * count for item, count in inventory.items()))\n        prefix_deposits = run[\'rows\'][offset - 1][\'deposited_by_actor\'][actor] if offset else {}\n        future_deposits = run[\'rows\'][-1][\'deposited_by_actor\'][actor]\n        obligation = sum((prices.get(item, 0) * (count - prefix_deposits.get(item, 0)) for item, count in future_deposits.items()))\n        bundles = []\n        for y, row in enumerate(farm[\'tiles\']):\n            for x, tile in enumerate(row):\n                if not isinstance(tile, dict):\n                    continue\n                xy, operations, value = ((x, y), [], 0)\n                if tile.get(\'yield_units\', 0) > 0:\n                    item = tile.get(\'crop\') if tile.get(\'kind\') == \'PLANT\' else ANIMALS.get(tile.get(\'animal\'), {}).get(\'product\')\n                    mature = item and (\'animal\' in tile or (START + offset) // 24 - tile[\'planted_day\'] >= CROPS[item][\'first_yield_day\'])\n                    if mature and (not owners.get((xy, \'HARVEST\'), set()) - {actor}):\n                        operations.append([\'HARVEST\'])\n                        value += prices[item] * tile[\'yield_units\']\n                if tile.get(\'fertilizer_available\') and \'animal\' in tile and (not owners.get((xy, \'COLLECT_FERTILIZER\'), set()) - {actor}):\n                    operations.append([\'COLLECT_FERTILIZER\'])\n                    value += prices[\'FERTILIZER\']\n                if operations:\n                    distance = len(_walk(pos, xy)) + len(operations) + len(_return(xy))\n                    if distance <= horizon - offset:\n                        bundles.append((xy, operations, value, distance))\n        bundles.sort(key=lambda b: (-b[2] / b[3], -b[2], b[0]))\n        variants = [([], carried)] if carried else []\n        for xy, ops, value, _ in bundles[:6]:\n            variants.append(([(xy, ops)], carried + value))\n        for first in bundles[:3]:\n            for second in bundles[:3]:\n                if first[0] != second[0]:\n                    variants.append(([(first[0], first[1]), (second[0], second[1])], carried + first[2] + second[2]))\n        for stops, value in variants:\n            route, cursor = ([], pos)\n            for xy, ops in stops:\n                route += _walk(cursor, xy) + ops\n                cursor = xy\n            route += _return(cursor)\n            if len(route) > horizon - offset:\n                continue\n            route += [[\'PASS\']] * (horizon - offset - len(route))\n            key = (offset, tuple((tuple(c) for c in route)))\n            if key not in seen:\n                seen.add(key)\n                proposals.append((value - obligation, offset, route, len(stops)))\n    proposals.sort(key=lambda p: (-p[0], p[1], p[2]))\n    direct = [p for p in proposals if p[3] == 0 and p[0] > 0][:2]\n    chosen = direct + [p for p in proposals if p not in direct]\n    return chosen[:max_per_actor]\n\ndef plan_terminal(obs, config, baseline_remaining, *, max_simulations=64, passes=1, proposals_per_actor=4):\n    """At 712 accept seven actions; positive physical delivery is mandatory."""\n    begun = perf_counter()\n    fallback = {\'accepted\': False, \'reason\': \'\', \'actions\': None, \'simulations\': 0}\n    try:\n        if int(_get(obs, \'step\', -1)) != START or len(baseline_remaining) != FINAL - START + 1:\n            raise Unsupported(\'planning requires step 712 and exactly seven actions through 718\')\n        max_simulations = min(256, max(1, int(max_simulations)))\n        passes = min(2, max(1, int(passes)))\n        proposals_per_actor = min(16, max(1, int(proposals_per_actor)))\n        baseline = simulate(obs, config, baseline_remaining, detailed=True)\n        prices = {item: max(1, float(_get(obs, \'market\', {}).get(\'prices\', {}).get(item, 1))) for item in PRODUCTS}\n        current, best = (_clone_schedule(baseline_remaining), baseline)\n        baseline_value = best_value = _value(baseline, prices)\n        changes, simulations = ([], 0)\n        n = len(baseline[\'private\'][\'inventories\'])\n        for sweep in range(passes):\n            improved = False\n            for actor in range(n):\n                winner = None\n                for _, offset, route, bundle_count in _proposals(best, actor, prices, proposals_per_actor):\n                    if simulations >= max_simulations:\n                        break\n                    trial = _clone_schedule(current)\n                    for i, command in enumerate(route, offset):\n                        if actor == 0:\n                            trial[i][\'farmer\'] = command\n                        else:\n                            trial[i].setdefault(\'hands\', [])\n                            while len(trial[i][\'hands\']) < n - 1:\n                                trial[i][\'hands\'].append([\'PASS\'])\n                            trial[i][\'hands\'][actor - 1] = command\n                    evaluated = simulate(obs, config, trial)\n                    simulations += 1\n                    score = _value(evaluated, prices)\n                    if score > best_value and dominates(evaluated, baseline):\n                        required = {(tuple(e[\'xy\']), e[\'op\'], e[\'actor\']): e[\'acquired\'] for e in best[\'events\'] if \'acquired\' in e and e[\'actor\'] != actor}\n                        acquired = {}\n                        for e in evaluated[\'events\']:\n                            if \'acquired\' in e:\n                                key = (tuple(e[\'xy\']), e[\'op\'], e[\'actor\'])\n                                dst = acquired.setdefault(key, {})\n                                for item, amount in e[\'acquired\'].items():\n                                    dst[item] = dst.get(item, 0) + amount\n                        if all((_ge(acquired.get(k, {}), v) for k, v in required.items())):\n                            winner, best_value = ((trial, offset, bundle_count), score)\n                if winner:\n                    current, offset, bundle_count = winner\n                    best = simulate(obs, config, current, detailed=True)\n                    changes.append({\'pass\': sweep, \'actor\': actor, \'from_step\': START + offset, \'resource_bundles\': bundle_count, \'estimated_stock_value\': best_value})\n                    improved = True\n                if simulations >= max_simulations:\n                    break\n            if not improved or simulations >= max_simulations:\n                break\n        if not changes or best_value <= baseline_value:\n            return {**fallback, \'reason\': \'no positive physical delivery gain\', \'simulations\': simulations, \'changed_workers\': [], \'changes\': [], \'certificate\': {\'stock_value_gain_at_initial_prices\': 0, \'sold_unit_delta\': dict.fromkeys(PRODUCTS, 0)}, \'planning_ms\': (perf_counter() - begun) * 1000}\n        final = simulate(obs, config, current, final_liquidate=True, detailed=True)\n        physical = simulate(obs, config, current)\n        if not dominates(physical, baseline):\n            raise Unsupported(\'no zero-overflow dominating continuation\')\n        delta = {item: final[\'sold\'].get(item, 0) - baseline[\'sold\'].get(item, 0) for item in PRODUCTS}\n        deposited_gain = any((final[\'rows\'][-1][\'deposited_by_actor\'][actor].get(item, 0) > baseline[\'rows\'][-1][\'deposited_by_actor\'][actor].get(item, 0) for actor in range(n) for item in PRODUCTS))\n        worker_change = any((_commands(new, n) != _commands(old, n) for new, old in zip(final[\'actions\'], baseline[\'actions\'])))\n        accepted = worker_change and deposited_gain and any((v > 0 for v in delta.values())) and all((v >= 0 for v in delta.values()))\n        plan = {\'accepted\': accepted, \'reason\': \'joint physical dominance\' if accepted else \'no improvement\', \'baseline\': _clone_schedule(baseline_remaining), \'actions\': final[\'actions\'], \'expected_states\': final[\'states\'][:-1], \'simulations\': simulations, \'changes\': changes, \'abandoned\': False, \'changed_workers\': sorted({c[\'actor\'] for c in changes}), \'certificate\': {\'baseline_rows\': baseline[\'rows\'], \'physical_rows\': physical[\'rows\'], \'baseline_overflow\': baseline[\'overflow_units\'], \'candidate_overflow\': final[\'overflow_units\'], \'sold_unit_delta\': delta, \'stock_value_gain_at_initial_prices\': best_value - baseline_value, \'baseline_final_shed\': baseline[\'private\'][\'shed\'], \'final_shed\': final[\'private\'][\'shed\'], \'positive_physical_deposit_gain\': deposited_gain, \'markets_712_717_unchanged\': all((final[\'actions\'][i].get(\'market\', []) == baseline_remaining[i].get(\'market\', []) for i in range(FINAL - START)))}}\n    except (Unsupported, KeyError, TypeError, ValueError, IndexError) as exc:\n        plan = {**fallback, \'reason\': str(exc)}\n    plan[\'planning_ms\'] = (perf_counter() - begun) * 1000\n    return plan\n\ndef _effective_action(action, n):\n    return (_commands(action, n), action.get(\'market\', []))\n\ndef _recover_observed(obs, config, parent_action, plan):\n    """Bounded cargo salvage after deviation; never resume old positional commands."""\n    farm, private = physical_state(obs)\n    positions = [farm[\'farmer\'], *farm[\'hands\']]\n    remaining = FINAL - int(_get(obs, \'step\')) + 1\n    room = max(0, int(_get(config, \'shedCapacity\', 100)) - sum(private[\'shed\'].values()))\n    commands = []\n    problems = []\n    prices = _get(obs, \'market\', {}).get(\'prices\', {})\n    for actor, (pos, inv) in enumerate(zip(positions, private[\'inventories\'])):\n        command = [\'PASS\']\n        if any((v > 0 for v in inv.values())):\n            route = _return(pos)\n            if len(route) > remaining:\n                problems.append({\'actor\': actor, \'reason\': \'unreachable cargo\'})\n            elif len(route) > 1:\n                command = route[0]\n            elif sum((max(0, q) for q in inv.values())) <= room:\n                command = [\'DROP\']\n                room -= sum((max(0, q) for q in inv.values()))\n            else:\n                items = [item for item in PRODUCTS if inv.get(item, 0) > 0]\n                if room and items:\n                    item = max(items, key=lambda i: (prices.get(i, 1) * min(inv[i], room), -PRODUCTS.index(i)))\n                    quantity = min(inv[item], room)\n                    command = [\'PLACE\', item, quantity]\n                    room -= quantity\n                else:\n                    problems.append({\'actor\': actor, \'reason\': \'no shed capacity\'})\n        commands.append(command)\n    action = {\'farmer\': commands[0], \'hands\': commands[1:], \'market\': deepcopy(parent_action.get(\'market\', []))}\n    if int(_get(obs, \'step\')) == FINAL:\n        action[\'market\'] = []\n        action = simulate(obs, config, [action], final_liquidate=True, preserve_final_commands=True)[\'actions\'][0]\n    plan[\'recovery_steps\'] = plan.get(\'recovery_steps\', 0) + 1\n    if problems:\n        plan.setdefault(\'recovery_failures\', []).append({\'step\': int(_get(obs, \'step\')), \'problems\': problems})\n    return action\n\ndef terminal_action(obs, config, parent_action, plan):\n    """Canonical guard, pre-deviation abstention, observed recovery after deviation."""\n    step = int(_get(obs, \'step\', -1))\n    if not plan or not plan.get(\'accepted\') or (not START <= step <= FINAL):\n        return parent_action\n    if plan.get(\'abandoned\'):\n        return _recover_observed(obs, config, parent_action, plan) if plan.get(\'deviated\') else parent_action\n    index = step - START\n    n = 1 + len(physical_state(obs)[0][\'hands\'])\n    mismatch = physical_state(obs) != plan[\'expected_states\'][index] or _effective_action(parent_action, n) != _effective_action(plan[\'baseline\'][index], n)\n    if mismatch:\n        plan[\'abandoned\'] = True\n        plan[\'abandon_step\'] = step\n        plan[\'reason\'] = \'physical observation or effective baseline action diverged\'\n        plan[\'safety_failure\'] = True\n        return _recover_observed(obs, config, parent_action, plan) if plan.get(\'deviated\') else parent_action\n    result = deepcopy(plan[\'actions\'][index])\n    if step == FINAL:\n        farm, private = physical_state(obs)\n        result = shop_liquidation(farm, private, _get(obs, \'market\')[\'prices\'])\n    if _commands(result, n) != _commands(parent_action, n):\n        plan[\'deviated\'] = True\n    return result',_PLANNER_NS)
# EXP-154 integration by Ahmed Berat Ozer, derived from Dmitrii Gluzdov E182.
# The preserved v27 parent is simulated on a private shadow only at step 712.
_PRE_TERMINAL_AGENT=agent
del agent
_TERMINAL_PLANS={}
_TERMINAL_PREVIOUS={}
_UPGRADE_STATS={'planning_calls':0,'accepted':0,'changed_steps':0,'aborted':0,'shadow_declines':0,'errors':0,'max_planning_ms':0.0}

def _parent_liquidate(farm, private, prices):
    # Exactly v27's final projected DROP ordering, in the planner's private state.
    view=_View({'player':0,'farms':[farm],'private':private,'market':{'prices':prices}},0,_IMPL.chassis.cfg)
    commands=[['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'] for i,pos in enumerate(view.positions)]
    action={'farmer':commands[0],'hands':commands[1:],'market':[]}
    stock=_IMPL.chassis._projected_shed(action,view)
    action['market']=[['SELL',item,stock.get(item,0)] for item in PRODUCTS if stock.get(item,0)>0]
    action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    return action

_PLANNER_NS['shop_liquidation']=_parent_liquidate

def _shadow_terminal(obs,config):
    seat=int(obs['player']);chassis=_IMPL.chassis
    state=chassis.players.get(seat)
    if not state or state.get('last_step')!=711 or state.get('route')!=2:
        return None
    # No delayed weed/structure intervention may depend on an unmodeled future.
    if state.get('pending'):
        return None
    shadow=copy.copy(chassis);shadow.players=copy.deepcopy(chassis.players)
    shadow.diagnostics={k:0 for k in chassis.diagnostics}
    projected=copy.deepcopy(obs);baseline=[];states=[]
    for step in range(712,719):
        projected['step']=step;projected['day']=step//24;projected['hour']=step%24
        states.append(copy.deepcopy(shadow.players[seat]))
        action=shadow.act(projected,config)
        if step==718:
            action=_parent_liquidate(projected['farms'][seat],projected['private'],projected['market']['prices'])
        else:
            market=action.get('market',[])
            if len(market)!=9 or {o[1] for o in market}!=set(PRODUCTS) or any(o[0]!='SELL' or len(o)!=3 or type(o[2]) is not int or o[2]<100 for o in market):
                return None
        if any(shadow.diagnostics.values()):return None
        run=_PLANNER_NS['simulate'](projected,config,[action])
        if run['actions'][0]!=action:return None
        baseline.append(action)
        run['farm']['money']=projected['farms'][seat]['money']
        projected['farms'][seat]=run['farm'];projected['private']=run['private']
    return baseline,states

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);seat=int(observation['player'])
    except Exception:
        return _PRE_TERMINAL_AGENT(observation,configuration)
    previous=_TERMINAL_PREVIOUS.get(seat)
    if step==0 or (previous is not None and step<=previous):_TERMINAL_PLANS.pop(seat,None)
    _TERMINAL_PREVIOUS[seat]=step
    plan=_TERMINAL_PLANS.get(seat)
    if plan and plan.get('accepted') and 712<=step<=718:
        if previous!=step-1:plan.update(abandoned=True,reason='nonconsecutive callback')
        try:
            result=_PLANNER_NS['terminal_action'](observation,configuration,plan['baseline'][step-712],plan)
            if plan.get('abandoned'):
                if not plan.get('abort_counted'):
                    plan['abort_counted']=True;_UPGRADE_STATS['aborted']+=1
                if not plan.get('deviated'):
                    _IMPL.chassis.players[seat]=copy.deepcopy(plan['parent_states_before'][step-712])
                    _TERMINAL_PLANS.pop(seat,None)
                    return _PRE_TERMINAL_AGENT(observation,configuration)
            _UPGRADE_STATS['changed_steps']+=int(result!=plan['baseline'][step-712])
            return result
        except Exception:
            _UPGRADE_STATS['errors']+=1
            if plan.get('deviated'):
                try:return _PLANNER_NS['_recover_observed'](observation,configuration,plan['baseline'][step-712],plan)
                except Exception:return _parent_liquidate(observation['farms'][seat],observation['private'],observation['market']['prices'])
    if step!=712:return _PRE_TERMINAL_AGENT(observation,configuration)
    _UPGRADE_STATS['planning_calls']+=1
    try:shadow=_shadow_terminal(observation,configuration)
    except (ValueError,KeyError,TypeError,IndexError):shadow=None
    if shadow is None:
        _UPGRADE_STATS['shadow_declines']+=1
        return _PRE_TERMINAL_AGENT(observation,configuration)
    baseline,states=shadow
    actual=_PRE_TERMINAL_AGENT(observation,configuration)
    if actual!=baseline[0]:
        _UPGRADE_STATS['shadow_declines']+=1;return actual
    try:
        plan=_PLANNER_NS['plan_terminal'](observation,configuration,baseline,max_simulations=64,passes=1,proposals_per_actor=4)
        _UPGRADE_STATS['max_planning_ms']=max(_UPGRADE_STATS['max_planning_ms'],plan.get('planning_ms',0.0))
        if not plan.get('accepted'):return actual
        plan['parent_states_before']=states;_TERMINAL_PLANS[seat]=plan
        _UPGRADE_STATS['accepted']+=1
        result=_PLANNER_NS['terminal_action'](observation,configuration,actual,plan)
        _UPGRADE_STATS['changed_steps']+=int(result!=actual)
        return result
    except Exception:
        _UPGRADE_STATS['errors']+=1;return actual

agent.telemetry=_UPGRADE_STATS

# EXP-154: aurax7 Reactive v2 day-end storage guard, adapted to our v27 view.
_PRE_ROOM_AGENT=agent
del agent
_ROOM_STATS={'changed_turns':0,'added_units':0,'errors':0}
def agent(observation,configuration=None):
    action=_PRE_ROOM_AGENT(observation,configuration)
    try:
        step=_step_of(observation)
        if step%24!=23:return action
        view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
        carried=sum(max(0,int(n)) for inv in view.invs for n in inv.values())
        needed=sum(view.shed.values())+carried-99
        if needed<=0:return action
        planned={}
        for o in action.get('market',[]):
            if o and o[0]=='SELL' and len(o)>=3:planned[o[1]]=planned.get(o[1],0)+max(0,int(o[2]))
        result=copy.deepcopy(action);added=0
        for item in sorted(PRODUCTS,key=lambda it:-int(view.prices.get(it,0))):
            qty=min(needed,max(0,view.shed.get(item,0)-planned.get(item,0)))
            if qty<=0:continue
            if len(result['market'])>=10:break
            result['market'].append(['SELL',item,qty]);needed-=qty;added+=qty
            if needed<=0:break
        if added:_ROOM_STATS['changed_turns']+=1;_ROOM_STATS['added_units']+=added
        return result
    except Exception:
        _ROOM_STATS['errors']+=1;return action

agent.telemetry=_ROOM_STATS

# Incorporated upstream attribution and change notice:
# E182 Shop0909 + terminal physical closure (modified 2026-09-09)
# 
# The active public parent is Yusuke Hayashi's yhay81/shop-router-0909 v3.
# router_parent.py and actions.json are exact original bytes, not newly authored
# routes. The parent credits aurax7's Reactive Router for sale timing and shed
# projection; that attribution remains in router_parent.py. Original payload
# LICENSE.txt is preserved unchanged (Apache License 2.0 text); it contains no
# named copyright grantor and no separate NOTICE was supplied. No additional
# ownership, endorsement, or upstream replay-data rights claim is made.
# 
# Local changes: separate main.py/policy.py adapter; bounded start712 planner
# copied from frozen E180/S78 and modified for seven callbacks, exact Shop final
# liquidation, strict positive physical delivery/sale gain, and observation guards.
# unit_model.py is an unchanged frozen E180 copy of Kaggle's extracted semantics.
# The following original E180 notice is retained verbatim for attribution history.
# Its references to Thomas files describe E180, not files supplied in this Shop
# package: no Thomas tapes, trees or policy are included here.
# 
# ----- Original E180 notice -----
# Kaggriculture: Last-Mile Harvest Planner
# Attribution and change notice
# 
# Thomas Tschinkel is the author of the parent public state-router policy and its
# published decision trees and action-route data. Source: Kaggriculture: 93.8% Win
# Rate Public State Router, notebook version 3, scriptVersionId 347936183:
# https://www.kaggle.com/code/thomastschinkel/kaggriculture-93-8-win-rate-public-state-router?scriptVersionId=347936183
# The public notebook identifies its license as Apache License, Version 2.0.
# Original published main.py SHA-256:
# b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522
# 
# Changes to that source for this distribution: compressed route/tree literals
# were decoded into readable tapes.json and trees.json; a read-only planned_action
# helper was added; descriptive headers and local data loading were adapted.
# The original parent feature extraction, tree traversal and agent behavior are
# retained. These public routes are not claimed as newly authored or trained by
# the notebook distributor.
# 
# unit_model.py contains deterministic unit-action and crop-decay definitions
# extracted from Kaggle's kaggle-environments 1.32.7 Kaggriculture engine, licensed
# under Apache License, Version 2.0. Credit: Kaggle and the kaggle-environments
# contributors. Project: https://github.com/Kaggle/kaggle-environments
# Source file: kaggle_environments/envs/kaggriculture/kaggriculture.py
# Source SHA-256:
# bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
# The extracted unit/decay definitions are not a newly authored game engine;
# market price dynamics and the full interpreter are not part of this module.
# 
# Additional work in this distribution: a bounded last-nine-action collection
# and delivery planner, observation guards and recovery, a settings-consuming
# factory and entry point, standalone examples, and deterministic packaging.
# The full Apache License, Version 2.0 is included as LICENSE.txt.
# No endorsement by Thomas Tschinkel or Kaggle is implied.
# 
# Data provenance limitation: Thomas's source refers to public replay data and
# an upstream provenance.json. That original episode-level manifest, replay IDs
# and individual replay-author identities were not supplied with the public
# notebook/output used here. No names or episode lineage have been invented.
# Notebook-level licensing does not independently establish the missing underlying
# replay-data rights chain. The package supplies usable readable routes, not a
# reproducible reconstruction of their original collection or training process.
# 
# Packaging note: source inputs described as byte-exact above are
# normalized to UTF-8/LF text with a final newline in this standalone
# notebook package. Route JSON values and parent policy behavior are unchanged.

# Final public-entry guard; measured separately and compared on captured observations.
_V28_CORE=agent
del agent
_IMPL.chassis.diagnostics['v28_entry_errors']=0
def agent(observation,configuration=None):
    try:
        return _V28_CORE(observation,configuration)
    except Exception:
        _IMPL.chassis.diagnostics['v28_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_ROOM_STATS

# EXP-155: prvsiyan V221B finite tomato investment, adapted by Ahmed Berat Ozer.
# Original public source is retained under research24/public; Apache-2.0.
MAX_ORDERS=10
class FarmView(_View):
    def __init__(self,obs):super().__init__(obs,int(obs['player']),_IMPL.chassis.cfg)
    def inventory(self,actor):return self.inv(actor)
def projected_shed(action,view):return _IMPL.chassis._projected_shed(action,view)

CROP_MIN_PRICE=70

# V219: a finite late tomato investment with dedicated, observed workers.
_V219_PARENT = agent
del agent
_V219_FERTILIZE = True  # Builder changes only this flag for the ablation.
_V219_STATES = {}
_V219_REPORT = {'commitments': 0, 'hire_requests': 0, 'confirmed_workers': 0,
                'hire_shortfalls': 0, 'plant_requests': 0, 'confirmed_plants': 0,
                'water_requests': 0, 'fertilize_requests': 0, 'harvest_requests': 0,
                'confirmed_harvest_units': 0, 'drop_requests': 0,
                'tomato_sale_requests': 0, 'budget_declines': 0, 'lost_plants': 0}


def _v219_fib(n):
    a, b = 1, 1
    for _ in range(n): a, b = b, a+b
    return a


def _v219_native_day(native, day):
    tape = _IMPL.chassis.routes[native['route']]
    return tape[day*24:min((day+1)*24,719)]


def _v219_qualifies(obs, native):
    farm=obs['farms'][obs['player']]
    if len(farm['tiles']) != 10 or set(farm['unlocked_quadrants']) != {'NW','NE','SW'}:
        return False
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    if sum(s in ('PIZZA_SHOP','FARMERS_MARKET') for s in obs['town']['unlocked_shops']) < 3:
        return False
    if any(farm['tiles'][y][x] != 'LOCKED' for y in (5,6) for x in range(5,10)):
        return False
    if obs['private']['seeds'].get('TOMATO',0) or obs['private']['shed'].get('TOMATO',0):
        return False
    if any(isinstance(t,dict) and t.get('crop')=='TOMATO' for row in farm['tiles'] for t in row):
        return False
    # The investment uses spare land and new worker indices. Avoid taking over
    # any native tomato or land purchase obligation on the known own schedule.
    for tape in _IMPL.chassis.routes.values():
        for a in tape[432:719]:
            if any(o and o[0]=='BUY_LAND' for o in a.get('market',[])):return False
            if any(c==['PLANT','TOMATO'] for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True


def _v219_walk(pos, target):
    x,y=pos;tx,ty=target
    if x != tx:return ['EAST' if x < tx else 'WEST']
    if y != ty:return ['SOUTH' if y < ty else 'NORTH']
    return None


def _v219_home(pos):
    return min(((4,4),(5,4),(4,5),(5,5)),key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))


def _v219_request(obs, action, state, native):
    step=int(obs['step']);day=step//24;offset=step%24
    farm=obs['farms'][obs['player']];private=obs['private']
    # If the planting-day transaction could not complete, abandon investment.
    # Later purchases would miss the finite day26..29 production window.
    if not state.get('committed') and day!=18:return action
    if state.get('requested_day')==day or offset>3:return action
    planned=_v219_native_day(native,day)
    remaining=planned[offset+1:]
    if any(o and o[0]=='HIRE' for a in remaining for o in a.get('market',[])):
        return action
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in action['market'])
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires != expected:return action
    fertilizer=bool(_V219_FERTILIZE and day in (24,27) and _r79_tomato_fertilizer_worthwhile(obs,action))
    # One watering tour: at most 2 entry moves + 9 between tiles + 10 waters.
    # A hire request by hour2 leaves at least21 callbacks after confirmation.
    crop_workers=1 if day in (19,20,21,22,23,25) and offset<=2 else (3 if 26<=day<=28 else 2)
    labor=_r53_labor_assignment(obs,action,fertilizer)
    if labor is not None:crop_workers=labor['workers']
    count=crop_workers+int(fertilizer and day==27 and labor is None)
    extra=[]
    if not state.get('committed'):
        extra += [['BUY_LAND'],['BUY_SEED','TOMATO',10]]
    fertilizer_quantity=_r70_parent_fert_qty(obs,action,planned,offset) if fertilizer else 0
    if fertilizer:extra.append(['BUY_PRODUCT','FERTILIZER',fertilizer_quantity])
    extra += [['HIRE'] for _ in range(count)]
    if len(action['market'])+len(extra)>MAX_ORDERS:return action
    # No assumed sale proceeds. Reserve 3,000 for parent obligations and price
    # movement; the qualification separately requires 12,000 initial liquidity.
    budget=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+count))
    if not state.get('committed'):budget+=4500
    if fertilizer:budget+=fertilizer_quantity*(obs['market']['prices']['FERTILIZER']+5)
    for order in action['market']:
        if not order:continue
        if order[0]=='BUY_PRODUCT':budget+=int(order[2])*(int(obs['market']['prices'][order[1]])+10)
        elif order[0]=='BUY_ANIMAL':budget+=int(order[2])*{'COW':400,'SHEEP':500,'GOOSE':300}[order[1]]
        elif order[0]=='BUY_SEED':budget+=int(order[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
    if farm['money']<budget+3000:
        _V219_REPORT['budget_declines']+=1;return action
    state['pending']={'step':step,'first_actor':expected+1,'count':count,'crop_workers':crop_workers,'fertilizer':fertilizer,'labor':labor}
    if labor is not None:
        _R53_LABOR_REPORT['labor_requests']+=1;_R53_LABOR_REPORT['labor_hires_avoided']+=1;_R53_LABOR_REPORT['labor_day'+str(day)]+=1
    state['requested_day']=day
    _V219_REPORT['hire_requests']+=count
    if not state.get('committed'):
        state['committed']=True;_V219_REPORT['commitments']+=1
    changed=copy.deepcopy(action);changed['market']+=extra
    return changed


def _v219_worker(obs, state, actor, role):
    day=int(obs['step'])//24;step=int(obs['step']);view=FarmView(obs)
    pos=tuple(view.positions[actor]);inv=view.inventory(actor)
    targets=role['targets']
    # Actual cargo differences, observed on the next callback, verify harvests.
    previous=state['last_work'].get(actor)
    if previous and previous['step']==step-1 and previous['command']==['HARVEST']:
        _V219_REPORT['confirmed_harvest_units']+=max(0,int(inv.get('TOMATO',0))-previous['tomatoes'])
    if role.get('needs_fertilizer') and not role.get('loaded'):
        home=_v219_home(pos)
        walk=_v219_walk(pos,home)
        if walk:return walk
        desired=role.get('fertilizer_quantity',10 if role['kind']=='fertilizer' else 5)
        if inv.get('FERTILIZER',0)>=desired:role['loaded']=True
        elif role.get('pickup_requested'):
            # Never spend repeated turns waiting for stock that was not bought.
            role['loaded']=True;role['fertilizer_available']=int(inv.get('FERTILIZER',0))
        elif view.shed.get('FERTILIZER',0)>=desired:
            role['pickup_requested']=True;return ['PICKUP','FERTILIZER',desired]
        else:role['loaded']=True
    todo=[]
    for target in targets:
        x,y=target;tile=view.tiles[y][x]
        tomato=isinstance(tile,dict) and tile.get('crop')=='TOMATO'
        if tomato and target not in state['seen_plants']:
            state['seen_plants'].add(target);_V219_REPORT['confirmed_plants']+=1
        if target in state['seen_plants'] and not tomato and target not in state['lost']:
            state['lost'].add(target);_V219_REPORT['lost_plants']+=1
        command=None
        if role['kind']=='fertilizer':
            if tomato and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
        elif day==18 and not tomato:
            if tile is None and obs['private']['seeds'].get('TOMATO',0)>0:command=['PLANT','TOMATO']
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif tomato:
            # No later production follows the final day, so watering then would
            # consume time needed to harvest and deliver the final cargo.
            if day<29 and not tile.get('watered_today'):command=['WATER']
            elif role.get('needs_fertilizer') and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
            elif tile.get('yield_units',0)>0:command=['HARVEST']
        if command:todo.append((target,command))
    # Final return has priority once only the exact distance plus DROP remains.
    home=_v219_home(pos);distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    if step>=718-distance and inv.get('TOMATO',0):
        return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv.get('TOMATO',0))]
    if todo:
        target,command=min(todo,key=lambda v:(abs(pos[0]-v[0][0])+abs(pos[1]-v[0][1]),targets.index(v[0])))
        return _v219_walk(pos,target) or command
    if inv.get('TOMATO',0):return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv['TOMATO'])]
    if any(inv.values()):return _v219_walk(pos,home) or ['DROP']
    return ['PASS']


def agent(observation, configuration=None):
    action=_V219_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V219_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'last_work':{},'seen_plants':set(),'lost':set(),
               'targets':[(x,y) for y in (5,6) for x in range(5,10)]}
        _V219_STATES[player]=state
    state['last_step']=step
    native=_IMPL.chassis.players[player]
    if step==432:state['eligible']=_v219_qualifies(observation,native)
    if not state.get('eligible') or day<18:return action
    if state['day']!=day:
        state['day']=day;state['workers']={};state['last_work']={}
    farm=observation['farms'][player]
    pending=state.pop('pending',None)
    if pending:
        if len(farm['hands'])+1 >= pending['first_actor']+pending['count'] and 'SE' in farm['unlocked_quadrants']:
            for index in range(pending['count']):
                fertilizer_worker=index==pending['crop_workers']
                if fertilizer_worker:targets=state['targets']
                elif pending['crop_workers']==1:targets=state['targets']
                elif pending['crop_workers']==2:targets=state['targets'][index*5:index*5+5]
                else:targets=[[(5,5),(6,5),(7,5)],[(8,5),(9,5),(9,6),(8,6)],[(5,6),(6,6),(7,6)]][index]
                state['workers'][pending['first_actor']+index]={'kind':'fertilizer' if fertilizer_worker else 'crop','targets':targets,
                    'needs_fertilizer':pending['fertilizer'] and (day==24 or fertilizer_worker)}
                if pending.get('labor') is not None:
                    role=state['workers'][pending['first_actor']+index]
                    role['targets']=[tuple(p) for p in pending['labor']['paths'][index]]
                    role['needs_fertilizer']=pending['labor']['fertilizer'];role['fertilizer_quantity']=len(role['targets'])
                    if tuple(farm['hands'][pending['first_actor']+index-1])!=tuple(pending['labor']['spawns'][index]):_R53_LABOR_REPORT['labor_spawn_errors']+=1
                    if index==0:_R53_LABOR_REPORT['labor_confirmed']+=1
            _V219_REPORT['confirmed_workers']+=pending['count']
        else:_V219_REPORT['hire_shortfalls']+=pending['count']
    action=_v219_request(observation,action,state,native)
    if state['workers']:
        commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
        commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
        for actor,role in state['workers'].items():
            if actor>=len(commands):continue
            command=_v219_worker(observation,state,actor,role)
            commands[actor]=command
            name={'PLANT':'plant_requests','WATER':'water_requests','FERTILIZE':'fertilize_requests',
                  'HARVEST':'harvest_requests','DROP':'drop_requests'}.get(command[0])
            if name:_V219_REPORT[name]+=1
            state['last_work'][actor]={'step':step,'command':command,'tomatoes':observation['private']['inventories'][actor].get('TOMATO',0)}
        action=copy.deepcopy(action);action['farmer'],action['hands']=commands[0],commands[1:]
    if state.get('committed') and len(action['market'])<MAX_ORDERS and not any(o[:2]==['SELL','TOMATO'] for o in action['market']):
        quantity=projected_shed(action,FarmView(observation)).get('TOMATO',0)
        if quantity>0:
            action=copy.deepcopy(action);action['market'].append(['SELL','TOMATO',quantity])
            _V219_REPORT['tomato_sale_requests']+=quantity
    return action


agent.telemetry=_V219_REPORT

# V221B: labor-only ablation of frozen V219G; not yet publicly scored.


# Crop workers own their final routes after commitment. A private parent shadow
# does not contain these obligations, so terminal rescue must abstain there.
_ORIGINAL_SHADOW_TERMINAL=_shadow_terminal
def _shadow_terminal(obs,config):
    if _V219_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _ORIGINAL_SHADOW_TERMINAL(obs,config)

APPLY_TIMING=False

_EXPERIMENT_PARENT=agent
del agent
_V219_REPORT['extra_fertilizer_days']=0
_V219_REPORT['reordered_market_turns']=0
_V219_REPORT['errors']=0
def agent(observation,configuration=None):
    try:
        action=_EXPERIMENT_PARENT(observation,configuration)
        if APPLY_TIMING and int(observation['step'])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT['errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

def _v224_sales_first(action):
    original=action.get('market',[])[:MAX_ORDERS]
    orders=[list(o) for o in original if o and (o[0] in ('HIRE','BUY_LAND') or (len(o)>=3 and int(o[2])>0))]
    for index in range(len(orders)):
        order=orders[index]
        if order[0]!='SELL':continue
        cursor=index
        while cursor>0:
            previous=orders[cursor-1]
            if previous[0]=='SELL':break
            if previous[0] in ('BUY_PRODUCT','BUY_ANIMAL') and previous[1]==order[1]:break
            orders[cursor-1],orders[cursor]=orders[cursor],orders[cursor-1]
            cursor-=1
    if orders==original:return action
    _V219_REPORT['reordered_market_turns']+=1
    changed=copy.deepcopy(action);changed['market']=orders
    return changed
_ORDER_PARENT=agent
del agent

def agent(observation,configuration=None):
    try:
        action=_ORDER_PARENT(observation,configuration)
        if int(observation["step"])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT["errors"]+=1
        return {"farmer":["PASS"],"hands":[],"market":[]}
agent.telemetry=_V219_REPORT

_V31_CORE=agent
del agent
_IMPL.chassis.diagnostics['production_errors']=0
_IMPL.chassis.diagnostics['v31_entry_errors']=0
def agent(observation,configuration=None):
    before=_V219_REPORT['errors']
    try:
        action=_V31_CORE(observation,configuration)
        _IMPL.chassis.diagnostics['production_errors']+=_V219_REPORT['errors']-before
        return action
    except Exception:
        _IMPL.chassis.diagnostics['v31_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

# Apache-2.0; later cattle transfer from prvsiyan, Moon (2026-09-10).
# Bounded livestock substitution; confirm owned animals before redirecting workers.
_V231_PARENT=agent
_V231_CAP=4
_V231_STATES={}
_V231_REPORT={}

def _v231_new_state():
    return {'last':-1,'confirmed':0,'reserved':0,'pending_buy':None,
            'carrying':{},'pending_places':[],'sites':{},'milk_credit':0,
            'requested':0,'failed_purchase_units':0,'picked':0,'placed':0,
            'failed_placements':0,'extra_milk_harvested':0,'extra_milk_sale_requests':0}

def _v231_controller(obs,action,state,cap):
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat]
    private=obs['private'];shed=private['shed'];inventories=private['inventories']
    positions=[farm['farmer'],*farm['hands']]
    pending=state['pending_buy']
    if pending is not None:
        gained=max(0,int(shed.get('COW',0))-pending['before'])
        confirmed=min(pending['quantity'],gained)
        state['confirmed']+=confirmed;state['reserved']+=confirmed
        state['failed_purchase_units']+=pending['quantity']-confirmed
        state['pending_buy']=None
    for pending in state['pending_places']:
        x,y=pending['site'];tile=farm['tiles'][y][x]
        if (isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==pending['day']):
            state['sites'][(x,y)]=pending['day'];state['placed']+=1
            actor=pending['actor'];state['carrying'][actor]=max(0,state['carrying'].get(actor,0)-1)
        else:state['failed_placements']+=1
    state['pending_places']=[]
    state['last']=step
    result=copy.deepcopy(action)
    workers=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
    seen_harvest=set();cow_available=int(shed.get('COW',0));occupied=set()
    for actor,work in enumerate(workers[:len(positions)]):
        inventory=inventories[actor] if actor<len(inventories) else {}
        x,y=positions[actor];tile=farm['tiles'][y][x];site=(x,y)
        if (work==['HARVEST'] and site in state['sites'] and site not in seen_harvest
                and isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==state['sites'][site]):
            units=max(0,int(tile.get('yield_units',0)))
            state['milk_credit']+=units;state['extra_milk_harvested']+=units
            seen_harvest.add(site)
        if len(work)>=2 and work[:2]==['PICKUP','SHEEP']:
            quantity=max(0,int(work[2]) if len(work)>2 else 1)
            center=len(farm['tiles'])//2
            if (quantity and state['reserved']>=quantity and cow_available>=quantity
                    and x in (center-1,center) and y in (center-1,center)
                    and not any(inventory.get(a,0) for a in ('COW','SHEEP','GOOSE'))):
                work[1]='COW';state['reserved']-=quantity;cow_available-=quantity
                state['carrying'][actor]=state['carrying'].get(actor,0)+quantity
                state['picked']+=quantity
        if (len(work)>=2 and work[:2]==['PLACE','SHEEP']
                and state['carrying'].get(actor,0)>0 and inventory.get('COW',0)>0
                and isinstance(tile,dict) and tile.get('kind')=='PASTURE'
                and 'animal' not in tile and site not in occupied):
            work[1]='COW'
            state['pending_places'].append({'actor':actor,'site':site,'day':step//24})
        if (len(work)>=2 and work[0]=='PLACE' and work[1] in ('COW','SHEEP','GOOSE')
                and inventory.get(work[1],0)>0):occupied.add(site)
    result['farmer'],result['hands']=workers[0],workers[1:]
    market=result.get('market',[])
    animal_orders=[o for o in market if len(o)>=3 and o[0]=='BUY_ANIMAL']
    shops=obs['town']['unlocked_shops'];prices=obs['market']['prices']
    counts={'COW':0,'SHEEP':0}
    for line in farm['tiles']:
        for tile in line:
            if isinstance(tile,dict) and tile.get('animal') in counts:counts[tile['animal']]+=1
    cargo=sum(int(inv.get(a,0)) for inv in inventories for a in ('COW','SHEEP','GOOSE'))
    stock_animals=sum(int(shed.get(a,0)) for a in ('COW','SHEEP','GOOSE'))
    milk_shops=sum(shop in ('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP') for shop in shops)
    if (216<=step<=227 and len(shops)>=3 and state['confirmed']<cap and not state['reserved']
            and not any(state['carrying'].values()) and not state['pending_places']
            and not cargo and not stock_animals and len(animal_orders)==1
            and animal_orders[0][1]=='SHEEP' and milk_shops>=2 and 'YARN_STORE' not in shops
            and int(prices.get('MILK',0))>=int(prices.get('WOOL',0))
            and counts['COW']>=4 and counts['SHEEP']>=2):
        order=animal_orders[0];quantity=int(order[2])
        if 1<=quantity<=2 and quantity<=cap-state['confirmed']:
            order[1]='COW';state['requested']+=quantity
            state['pending_buy']={'before':int(shed.get('COW',0)),'quantity':quantity}
    # Sell only additional physically harvested production at an existing sale slot.
    if state['milk_credit']>0:
        stock=projected_shed(result,FarmView(obs))
        total_planned=sum(max(0,int(o[2])) for o in market if len(o)>=3 and o[:2]==['SELL','MILK'])
        extra=min(state['milk_credit'],max(0,int(stock.get('MILK',0))-total_planned))
        if extra:
            for order in market:
                if len(order)>=3 and order[:2]==['SELL','MILK'] and int(order[2])>0:
                    order[2]=int(order[2])+extra
                    state['milk_credit']-=extra;state['extra_milk_sale_requests']+=extra
                    break
    result['market']=market
    return result

def agent(observation,configuration=None):
    step=int(observation['step']);seat=int(observation['player'])
    state=_V231_STATES.get(seat)
    if state is None or step<=state['last']:
        state=_V231_STATES[seat]=_v231_new_state()
    action=_V231_PARENT(observation,configuration)
    action=_v231_controller(observation,action,state,_V231_CAP)
    _V231_REPORT.clear();_V231_REPORT.update(_V231_PARENT.telemetry)
    for name in ('confirmed','reserved','requested','failed_purchase_units','picked','placed',
                 'failed_placements','extra_milk_harvested','extra_milk_sale_requests','milk_credit'):
        _V231_REPORT['cattle_'+name]=state[name]
    _V231_REPORT['cattle_carried_pending']=sum(state['carrying'].values())
    return action

agent.telemetry=_V231_REPORT


# EXP-167, adapted from Dmitrii Gluzdov's Two Coins, One Sheep (Apache-2.0).
# Reserve only physically available stock after the final parent worker actions.
_R36_SALE_PARENT=agent
_R36_NATIVE_LEAD=Chassis._sell_lead
_R36_NATIVE_SUPPRESS=Chassis._apply_suppression
_R36_SALE_REPORT={}

def _r36_native_lead(self,action,view,projected,route,step,next_sup):
    if step<288 or step>=696:
        return _R36_NATIVE_LEAD(self,action,view,projected,route,step,next_sup)

def _r36_suppress(action,state,step):
    _R36_NATIVE_SUPPRESS(action,state,step)
    due=state.get('r36_debts',{}).pop(step,{})
    for order in action.get('market',[]):
        if len(order)>=3 and order[0]=='SELL':
            removed=min(max(0,int(order[2])),due.get(order[1],0))
            order[2]-=removed
            due[order[1]]=due.get(order[1],0)-removed

Chassis._sell_lead=_r36_native_lead
Chassis._apply_suppression=staticmethod(_r36_suppress)

def _r36_reserve(obs,action):
    step=int(obs['step'])
    # The final planner forecasts its own parent, so keep its full window native.
    if not 288<=step<696:return action
    native=_IMPL.chassis.players[int(obs['player'])]
    tape=_IMPL.chassis.routes[native['route']]
    end=min(695,step+_R37_HORIZONS.get(int(obs['player']),2),(step//72+1)*72-1)
    if end<=step:return action
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    view=FarmView(obs)
    # This projection intentionally abstains on ambiguous animal depot returns.
    if any(len(c)>1 and c[0]=='PLACE' and c[1] in ANIMAL_STRUCTURE
           and view.inv(i).get(c[1],0)>0 for i,c in enumerate(commands[:len(view.positions)])):
        return action
    stock=projected_shed(action,view)
    market=action.get('market',[])
    blocked={o[1] for o in market if len(o)>1 and o[0] in ('SELL','BUY_PRODUCT')}
    blocked.update(c[1] for c in commands if len(c)>1 and c[0]=='PICKUP')
    blocked.update(c[1] for queue in native['pending'].values() for pos,c in queue
                   if len(c)>1 and c[0]=='PICKUP')
    debts=native['sell_state'].setdefault('r36_debts',{})
    for item in PRODUCTS:
        if item in ('WHEAT','FERTILIZER') or item in blocked or view.prices.get(item,0)<2:continue
        available=max(0,int(stock.get(item,0)))
        if not available or len(market)>=10:continue
        reservations=[]
        for due_step in range(step+1,end+1):
            future=tape[due_step]
            work=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
            if any(len(c)>1 and c[:2]==['PICKUP',item] for c in work):break
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT',item] for o in future.get('market',[])):break
            planned=sum(max(0,int(o[2])) for o in future.get('market',[]) if len(o)>=3 and o[:2]==['SELL',item])
            amount=min(available,max(0,planned-debts.get(due_step,{}).get(item,0)))
            if amount:
                reservations.append((due_step,amount));available-=amount
            if not available:break
        qty=sum(q for _,q in reservations)
        if qty:
            market.append(['SELL',item,qty])
            for due,q in reservations:
                debt=debts.setdefault(due,{})
                debt[item]=debt.get(item,0)+q
            _R36_SALE_REPORT['sale_reserved_units']+=qty
            _R36_SALE_REPORT['sale_reservations']+=1
    return action

def agent(observation,configuration=None):
    if int(observation.get('step',0))==0:
        _R36_SALE_REPORT.update(sale_reserved_units=0,sale_reservations=0,sale_errors=0)
    action=_R36_SALE_PARENT(observation,configuration)
    try:
        if configuration is None or all(configuration.get(k,v)==v for k,v in
            [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r36_reserve(observation,action)
            if int(observation['step'])>=288:action=_v224_sales_first(action)
    except Exception:
        _R36_SALE_REPORT['sale_errors']=_R36_SALE_REPORT.get('sale_errors',0)+1
    _R36_SALE_REPORT.update(_R36_SALE_PARENT.telemetry)
    return action

agent.telemetry=_R36_SALE_REPORT

# Ensure the Kaggle-selected final callable is the exported policy.
agent = globals().pop("agent")


# Public capability transfer: lucifer19; Flexon is the same Two Coins asset set.
# Apache-2.0; exact functions from Kaggle kaggle-environments 1.32.7.
# https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture
import math
_R37_MARKET_PARAMS = {'WHEAT': {'base': 25, 'I0': 10000, 'T': 400, 'below_func': 'sqrt', 'below_target': 0.8, 'above_func': 'log', 'above_target': 0.2}, 'CARROT': {'base': 35, 'I0': 10000, 'T': 450, 'below_func': 'hinge', 'below_target': 1.0, 'above_func': 'sqrt', 'above_target': 0.7}, 'TOMATO': {'base': 60, 'I0': 10000, 'T': 200, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'sqrt', 'above_target': 0.6}, 'STRAWBERRY': {'base': 120, 'I0': 10000, 'T': 100, 'below_func': 'sqrt', 'below_target': 0.7, 'above_func': 'linear', 'above_target': 1.6}, 'MELON': {'base': 250, 'I0': 10000, 'T': 300, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.6}, 'EGG': {'base': 50, 'I0': 10000, 'T': 332, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'log', 'above_target': 0.2}, 'MILK': {'base': 160, 'I0': 10000, 'T': 122, 'below_func': 'sqrt', 'below_target': 0.6, 'above_func': 'linear', 'above_target': 1.6}, 'WOOL': {'base': 200, 'I0': 10000, 'T': 105, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.2}, 'FERTILIZER': {'base': 100, 'I0': 10000, 'T': 200, 'below_func': 'linear', 'below_target': 0.4, 'above_func': 'linear', 'above_target': 0.4}}
_R37_PRICE_FLOOR = 1
_R37_HINGE_GAIN = 8.0
def _r37_shape(func, x, T=None):
    x = max(0.0, x)
    if func == "linear": return x
    if func == "sq":     return x * x
    if func == "sqrt":   return math.sqrt(x)
    if func == "log":    return math.log(1.0 + x)
    if func == "log10":  return math.log10(1.0 + x)
    if func == "hinge":
        # Degenerates to linear if T is missing or non-positive.
        if not T or T <= 0:
            return x
        u = x / T
        return u + _R37_HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x

def _r37_market_price(item, inventory, params=None):
    """Floor at _R37_PRICE_FLOOR."""
    p = (params or _R37_MARKET_PARAMS)[item]
    base = p["base"]
    I0 = p["I0"]
    T = p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _r37_shape(f, T, T)
        price = base + amp * _r37_shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _r37_shape(f, T, T)
        price = base - amp * _r37_shape(f, inventory - I0, T)
    return max(_R37_PRICE_FLOOR, int(round(price)))

def _r37_similarity(observation):
    """Empty tiles cannot make two unrelated production layouts look alike."""
    farms = observation['farms']
    own, rival = farms[observation['player']], farms[1-observation['player']]
    if own['unlocked_quadrants'] != rival['unlocked_quadrants']:
        return 0.0
    matches = total = 0
    for a, b in zip([t for row in own['tiles'] for t in row],
                    [t for row in rival['tiles'] for t in row]):
        sa = (a.get('crop'), a.get('animal')) if isinstance(a, dict) else (None, None)
        sb = (b.get('crop'), b.get('animal')) if isinstance(b, dict) else (None, None)
        if sa != (None, None) or sb != (None, None):
            total += 1
            matches += sa == sb
    return matches / total if total >= 8 else 0.0


def _r37_quote_priority(observation, order, stock):
    """Revenue exposed to a small rival batch, not nominal headline revenue."""
    item = order[1]
    quantity = min(max(0, int(order[2])), stock.get(item, 0))
    if not quantity or item not in _R37_MARKET_PARAMS:
        return 0.0
    inventory = observation['market']['inventory'][item]
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for k, patch in observation['market'].get('params', {}).items():
        if k in params:
            params[k].update(patch)
    rival = observation['farms'][1-observation['player']]
    crop_item = item if item in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON') else None
    animal = {'EGG':'GOOSE','MILK':'COW','WOOL':'SHEEP'}.get(item)
    standing = sum(max(0, int(t.get('yield_units', 0))) for row in rival['tiles'] for t in row
                   if isinstance(t, dict) and
                   ((crop_item is not None and t.get('crop') == crop_item) or
                    (animal is not None and t.get('animal') == animal)))
    # Public fields do not reveal the rival shed. Eight units are a scenario,
    # not a recovered hidden quantity; visible ripe yield increases the stress.
    batch = min(24, max(8, standing))
    now = sum(_r37_market_price(item, inventory+j, params) for j in range(quantity))
    later = sum(_r37_market_price(item, inventory+batch+j, params) for j in range(quantity))
    return now-later


def _r37_reorder_sales(observation, action):
    """Keep quantities and purchase barriers; rank distinct contiguous sales."""
    stock = projected_shed(action, FarmView(observation))
    orders = [list(o) for o in action['market']]
    start = 0
    while start < len(orders):
        if orders[start][0] != 'SELL':
            start += 1
            continue
        end = start
        while end < len(orders) and orders[end][0] == 'SELL':
            end += 1
        block = orders[start:end]
        if len({o[1] for o in block}) == len(block):
            orders[start:end] = sorted(block, key=lambda o: _r37_quote_priority(observation, o, stock), reverse=True)
        start = end
    if orders != action['market']:
        _R37_STATS['quote_reordered_turns'] += 1
        action = dict(action, market=orders)
    return action



# EXP175: bounded public cash-response probe inspired by leoprovorov,
# Two Coins Mirror Counter v1 (Apache-2.0). No hidden rival inventory.
_R44_PROBES={}
_R44_REPORT=dict(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)

def _r44_before(obs):
    player=int(obs['player']);step=int(obs['step'])
    st=_R44_PROBES.get(player)
    if st is None or step<=st['step']:
        st=_R44_PROBES[player]={'step':-1,'money':None,'probe':0,'matched':False}
    if step==0:_R44_REPORT.update(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)
    money=tuple(float(obs['farms'][i]['money']) for i in (player,1-player))
    if st['money'] is not None and st['probe']>=100 and _r37_similarity(obs)>=.90:
        own=money[0]-st['money'][0];rival=money[1]-st['money'][1]
        if own>0 and rival>0 and abs(own-rival)<=max(5.0,.05*st['probe']):
            if not st['matched']:_R44_REPORT['probe_matches']+=1
            st['matched']=True
    st.update(step=step,money=money,probe=0)
    return st

def _r44_after(obs,action,st):
    step=int(obs['step']);player=int(obs['player'])
    if not 336<=step<648 or st['matched']:return
    # Positive all-sale probes avoid mistaking equal spending for preemption.
    if not action['market'] or any(o and o[0]!='SELL' for o in action['market']):return
    debts=_IMPL.chassis.players[player]['sell_state'].get('r36_debts',{})
    own=debts.get(step+3,{})
    if own:st['probe']=sum(max(0,int(n))*int(obs['market']['prices'].get(item,0)) for item,n in own.items())

_R37_ADAPTIVE = True
_R37_QUOTE = True
# EXP-168: adapted from lucifer19 / Harvest Nocturne, Apache-2.0.
# All rivalry features use public occupied tiles; no private rival inventory.
_R37_PARENT = agent
_R37_PLAYERS = {}
_R37_HORIZONS = {}
_R37_REPORT = {}
_R37_STATS = dict(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
del agent

def agent(observation, configuration=None):
    player, step = int(observation['player']), int(observation['step'])
    state = _R37_PLAYERS.get(player)
    if state is None or step <= state['step']:
        state = _R37_PLAYERS[player] = {'step': -1, 'streak': 0}
    if step == 0:
        _R37_STATS.update(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
    state['step'] = step
    _R37_HORIZONS[player] = 2
    probe_state=_r44_before(observation)
    try:
        if _R37_ADAPTIVE and step < 648:
            state['streak'] = state['streak'] + 1 if _r37_similarity(observation) >= .90 else 0
            if 336 <= step < 648 and state['streak'] >= 6:
                _R37_HORIZONS[player] = 3
                _R37_STATS['three_turn_calls'] += 1
    except Exception:
        _R37_STATS['nocturne_errors'] += 1
    if _R37_HORIZONS[player]==3 and probe_state['matched']:
        _R37_HORIZONS[player]=4
        _R44_REPORT['probe_four_turn_calls']+=1
    # EXP179: four-turn reservation; retain stock, debt and purchase barriers.
    if 288 <= step < 696:_R37_HORIZONS[player] = 4
    action = _R37_PARENT(observation, configuration)
    _r44_after(observation,action,probe_state)
    if _R37_QUOTE and step >= 288:
        try:
            action = _r37_reorder_sales(observation, action)
        except Exception:
            _R37_STATS['nocturne_errors'] += 1
    _R37_REPORT.update(getattr(_R37_PARENT, 'telemetry', {}))
    _R37_REPORT.update(_R37_STATS)
    _R37_REPORT.update(_R44_REPORT)
    return action

agent.telemetry = _R37_REPORT

# Export guard: normal decisions stay identical to the frozen screened policy.
_RELEASE_PARENT=agent
_RELEASE_REPORT={}
_RELEASE_ERRORS=0
del agent

def agent(observation,configuration=None):
    global _RELEASE_ERRORS
    try:
        result=_RELEASE_PARENT(observation,configuration)
    except Exception:
        _RELEASE_ERRORS+=1
        count=0
        try:
            count=min(64,len(observation['farms'][int(observation['player'])]['hands']))
        except Exception:
            pass
        result={'farmer':['PASS'],'hands':[['PASS'] for _ in range(count)],'market':[]}
    _RELEASE_REPORT.update(getattr(_RELEASE_PARENT,'telemetry',{}))
    _RELEASE_REPORT['release_errors']=_RELEASE_ERRORS
    return result

agent.telemetry=_RELEASE_REPORT
agent=globals().pop('agent')

# Adapted from prvsiyan / The Soil Remembers Rain, Apache-2.0.
# V233: bounded, financed six-sheep SE discovery investment.
_V233_PARENT=agent
del agent
_V233_STATES={}
_V233_REPORT=dict(sheep_commit_requests=0,sheep_committed=0,sheep_hire_requests=0,
    sheep_workers_confirmed=0,sheep_hire_shortfalls=0,sheep_budget_declines=0,
    sheep_capacity_declines=0,sheep_purchase_shortfalls=0,sheep_feed_buy_requests=0,
    sheep_wool_harvested=0,sheep_fert_collected=0,sheep_extra_wool_sales=0,
    sheep_extra_fert_sales=0,sheep_rescue_feed_requests=0)

def _v233_eligible(obs,native):
    farm=obs['farms'][obs['player']];prices=obs['market']['prices']
    if len(farm['tiles'])!=10 or set(farm['unlocked_quadrants'])!={'NW','NE','SW'}:return False
    if obs['town']['unlocked_shops'].count('YARN_STORE')<2 or prices['WOOL']<220 or prices['WHEAT']>45:return False
    if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) for x in range(5,8)):return False
    if obs['private']['shed'].get('SHEEP',0) or any(i.get('SHEEP',0) for i in obs['private']['inventories']):return False
    for day in range(12,30):
        for a in _v219_native_day(native,day):
            if any(o and (o[0]=='BUY_LAND' or o[:2]==['BUY_ANIMAL','SHEEP']) for o in a.get('market',[])):return False
            if any(c and c[0] in ('PICKUP','PLACE') and len(c)>1 and c[1]=='SHEEP' for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True

def _v233_request(obs,action,state,native):
    step=int(obs['step']);day=step//24;hour=step%24
    if hour>(2 if state.get('committed') else 1) or state.get('requested_day')==day:return action
    if not state.get('committed') and (day!=12 or not _v233_eligible(obs,native)):return action
    planned=_v219_native_day(native,day)
    if any(o and o[0]=='HIRE' for a in planned[hour+1:] for o in a.get('market',[])):return action
    farm=obs['farms'][obs['player']];market=action.get('market',[])
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in market)
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires!=expected:return action
    initial=not state.get('committed')
    extra=([['BUY_LAND'],['BUY_ANIMAL','SHEEP',6]] if initial else [])+[['BUY_PRODUCT','WHEAT',6],['HIRE'],['HIRE']]
    if len(market)+len(extra)>MAX_ORDERS:return action
    stock=projected_shed(action,FarmView(obs))
    incoming=6+6*initial
    budget=7000*initial+6*(int(obs['market']['prices']['WHEAT'])+10)
    budget+=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+2))
    for o in market:
        if not o:continue
        if o[0]=='BUY_LAND':return action
        if o[0]=='BUY_PRODUCT':
            incoming+=int(o[2]);budget+=int(o[2])*(int(obs['market']['prices'][o[1]])+10)
        elif o[0]=='BUY_ANIMAL':
            incoming+=int(o[2]);budget+=int(o[2])*{'SHEEP':500,'COW':400,'GOOSE':300}[o[1]]
        elif o[0]=='BUY_SEED':budget+=int(o[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[o[1]]
    if sum(stock.values())+incoming>100:
        _V233_REPORT['sheep_capacity_declines']+=1;return action
    if farm['money']<budget+(3000 if initial else 1000):
        _V233_REPORT['sheep_budget_declines']+=1;return action
    state['requested_day']=day
    state['pending']={'first':expected+1,'initial':initial}
    _V233_REPORT['sheep_hire_requests']+=2;_V233_REPORT['sheep_feed_buy_requests']+=6
    if initial:_V233_REPORT['sheep_commit_requests']+=1
    result=copy.deepcopy(action);result['market']=market+extra
    return result

def _v233_worker(obs,actor,targets):
    farm=obs['farms'][obs['player']];private=obs['private'];step=int(obs['step'])
    pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
    access=((4,4),(5,4),(4,5),(5,5))
    home=min(access,key=lambda p:(abs(pos[0]-p[0])+abs(pos[1]-p[1]),p))
    distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    cargo=[item for item in ('WOOL','FERTILIZER') if inv.get(item,0)]
    if cargo and step%24 >= (22 if step//24==29 else 23)-distance:
        return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    missing=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP') for x,y in targets)
    if missing and not inv.get('SHEEP',0) and private['shed'].get('SHEEP',0):
        return _v219_walk(pos,home) or ['PICKUP','SHEEP',min(missing,private['shed']['SHEEP'])]
    hungry=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('fed_today')) for x,y in targets)
    if hungry and not inv.get('WHEAT',0) and private['shed'].get('WHEAT',0):
        return _v219_walk(pos,home) or ['PICKUP','WHEAT',min(hungry,private['shed']['WHEAT'])]
    tasks=[]
    for target in targets:
        x,y=target;tile=farm['tiles'][y][x];command=None
        if tile is None:command=['BUILD_PASTURE']
        elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal'):
            if inv.get('SHEEP',0):command=['PLACE','SHEEP']
        elif isinstance(tile,dict) and tile.get('animal')=='SHEEP':
            if not tile['fed_today'] and inv.get('WHEAT',0):command=['FEED']
            elif not tile['cared_today']:command=['CARE']
            elif tile['yield_units']:command=['HARVEST']
            elif tile['fertilizer_available']:command=['COLLECT_FERTILIZER']
        if command:tasks.append((abs(pos[0]-x)+abs(pos[1]-y),targets.index(target),target,command))
    if tasks:
        _,_,target,command=min(tasks);return _v219_walk(pos,target) or command
    if cargo:return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    return ['PASS']

def _v234_rescue(obs,action,state):
    if not state['workers'] or int(obs['step'])%24>14:return action
    orders=action.get('market',[])
    if len(orders)>=MAX_ORDERS:return action
    if any(o and (o[0] in ('HIRE','BUY_LAND','BUY_ANIMAL','BUY_PRODUCT','BUY_SEED') or (len(o)>1 and o[1]=='WHEAT')) for o in orders):return action
    farm=obs['farms'][obs['player']];private=obs['private'];hungry=carried=0
    commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
    for actor,targets in state['workers'].items():
        command=commands[actor]
        if command==['FEED'] or command[:2]==['PICKUP','WHEAT']:return action
        carried+=private['inventories'][actor].get('WHEAT',0)
        hungry+=sum(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP' and not farm['tiles'][y][x].get('fed_today') for x,y in targets)
    stock=projected_shed(action,FarmView(obs))
    shortage=hungry-carried-stock.get('WHEAT',0)
    if not 0<shortage<=6 or state.get('rescue_today',0)+shortage>6:return action
    quote=int(obs['market']['prices']['WHEAT'])
    if quote<1 or farm['money']<1000+shortage*(quote+10) or sum(stock.values())+shortage>100:return action
    result=copy.deepcopy(action);result['market'].append(['BUY_PRODUCT','WHEAT',shortage])
    state['rescue_today']=state.get('rescue_today',0)+shortage
    _V233_REPORT['sheep_rescue_feed_requests']+=shortage
    return result

def agent(observation,configuration=None):
    action=_V233_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V233_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'work':{},'credit':{'WOOL':0,'FERTILIZER':0}}
        _V233_STATES[player]=state
    state['last_step']=step
    if configuration is not None and any(configuration.get(k,v)!=v for k,v in
        (('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10))):return action
    if day<12:return action
    farm=observation['farms'][player];private=observation['private']
    if state['day']!=day:state['day']=day;state['workers']={};state['work']={};state['rescue_today']=0
    for actor,previous in state['work'].items():
        if previous['step']!=step-1 or actor>=len(private['inventories']):continue
        item={'HARVEST':'WOOL','COLLECT_FERTILIZER':'FERTILIZER'}.get(previous['command'][0])
        if item:
            gained=max(0,private['inventories'][actor].get(item,0)-previous['inventory'].get(item,0))
            state['credit'][item]+=gained
            _V233_REPORT['sheep_wool_harvested' if item=='WOOL' else 'sheep_fert_collected']+=gained
    pending=state.pop('pending',None)
    if pending:
        funded='SE' in farm['unlocked_quadrants'] and (not pending['initial'] or private['shed'].get('SHEEP',0)>=6)
        if not funded:_V233_REPORT['sheep_purchase_shortfalls']+=1
        elif len(farm['hands'])<pending['first']+1:_V233_REPORT['sheep_hire_shortfalls']+=1
        else:
            for i in range(2):state['workers'][pending['first']+i]=[(x,5+i) for x in range(5,8)]
            _V233_REPORT['sheep_workers_confirmed']+=2
            if pending['initial']:state['committed']=True;_V233_REPORT['sheep_committed']+=1
    action=_v233_request(observation,action,state,_IMPL.chassis.players[player])
    if not state.get('committed'):return action
    result=copy.deepcopy(action)
    commands=[result.get('farmer') or ['PASS']]+list(result.get('hands') or [])
    commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
    state['work']={}
    for actor,targets in state['workers'].items():
        command=_v233_worker(observation,actor,targets);commands[actor]=command
        state['work'][actor]={'step':step,'command':command,'inventory':dict(private['inventories'][actor])}
    result['farmer'],result['hands']=commands[0],commands[1:]
    result=_v234_rescue(observation,result,state)
    stock=projected_shed(result,FarmView(observation))
    for item in ('WOOL','FERTILIZER'):
        scheduled=sum(int(o[2]) for o in result['market'] if o[:2]==['SELL',item])
        count=min(state['credit'][item],max(0,stock.get(item,0)-scheduled))
        if count and len(result['market'])<MAX_ORDERS:
            result['market'].append(['SELL',item,count]);state['credit'][item]-=count
            _V233_REPORT['sheep_extra_wool_sales' if item=='WOOL' else 'sheep_extra_fert_sales']+=count
    return result

_R46_SHEEP_AGENT=agent
_R46_SHADOW_PARENT=_shadow_terminal
_R46_REPORT={}
def _shadow_terminal(obs,config):
    if _V233_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _R46_SHADOW_PARENT(obs,config)
del agent
def agent(observation,configuration=None):
    try:
        if int(observation.get('step',-1))==0:
            for k in _V233_REPORT:_V233_REPORT[k]=0
        result=_R46_SHEEP_AGENT(observation,configuration)
    except Exception:
        _R46_REPORT['sheep_overlay_errors']=_R46_REPORT.get('sheep_overlay_errors',0)+1
        result={'farmer':['PASS'],'hands':[],'market':[]}
    _R46_REPORT.update(getattr(_V233_PARENT,'telemetry',{}))
    _R46_REPORT.update(_V233_REPORT)
    return result
agent.telemetry=_R46_REPORT
agent=globals().pop('agent')

# EXP182: finite-harvest wheat/carrot input planner; original adaptation.
_R51_INPUT_PARENT=agent
_R51_INPUT_STATES={}
_R51_INPUT_REPORT={}
_R51_INPUT_MAX_WORKERS=2
_R51_INPUT_CROPS={'WHEAT':(2,4,6),'CARROT':(2,3,4)}

def _r51_input_forecast(obs,route,expected):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    pos=[list(farm['farmer'])]+[list(p) for p in farm['hands'][:expected]];targets={}
    for y,line in enumerate(farm['tiles']):
        for x,tile in enumerate(line):
            if not isinstance(tile,dict) or tile.get('crop') not in _R51_INPUT_CROPS:continue
            item=tile['crop'];first,last,cap=_R51_INPUT_CROPS[item]
            if 1<=day-tile['planted_day']<last:
                targets[(x,y)]={'crop':item,'birth':tile['planted_day'],'yield':tile['yield_units'],
                    'until':tile.get('fertilized_until_day',-1),'watered':tile.get('watered_today',False),'water':[],'harvest':None,'first':first,'last':last,'cap':cap}
    access=((4,4),(5,4),(4,5),(5,5));seen=set()
    # Native continuation ends before the reactive terminal closure planner.
    for t in range(step,min(712,(day+4)*24)):
        tape=_IMPL.chassis.routes[2 if t>=648 else route];a=tape[t]
        for actor,c in enumerate([a.get('farmer') or ['PASS'],*(a.get('hands') or [])][:len(pos)]):
            if not c:continue
            xy=tuple(pos[actor]);target=targets.get(xy)
            if target is not None and target['harvest'] is None:
                if c[0]=='WATER' and (t//24,xy) not in seen:
                    seen.add((t//24,xy))
                    if not(t//24==day and target['watered']) and target['first']<=t//24-target['birth']<=target['last']:target['water'].append(t)
                if c[0]=='HARVEST':target['harvest']=t
            if c[0] in MOVES:
                dx,dy=MOVES[c[0]];pos[actor]=[max(0,min(9,pos[actor][0]+dx)),max(0,min(9,pos[actor][1]+dy))]
        for o in a.get('market',[]):
            if o and o[0]=='HIRE':
                counts={p:sum(tuple(q)==p for q in pos) for p in access}
                pos.append(list(min(access,key=lambda p:(counts[p],access.index(p)))))
        if (t+1)%24==0:pos=[[4,4]]
    return targets

def _r51_input_gain(target,arrival,day):
    if target['harvest'] is None or target['harvest']<=arrival:return 0
    extra=sum(arrival<t<=target['harvest'] and day<=t//24<=day+2 and t//24>target['until'] for t in target['water'])
    baseline=target['yield']+sum(2 if t//24<=target['until'] else 1 for t in target['water'])
    return max(0,min(extra,target['cap']-baseline))

def _r51_input_path(obs,targets,action,index):
    step=int(obs['step']);day=step//24
    ready,start=_r62_input_start(obs,action,index)
    prices={p:max(1,int(obs['market']['prices'][p])-2) for p in ('WHEAT','CARROT')}
    fertilizer=max(1,_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-16)+2)
    # Tuple: penalized value, gross value, next free turn, position, path, used,
    # wheat units, carrot units. No state reads from the rival's private farm.
    beam=[(0,0,ready,start,(),frozenset(),0,0)]
    best=None
    for depth in range(8):
        expanded=[]
        for score,gross,now,pos,path,used,wheat,carrot in beam:
            for xy,target in targets.items():
                if xy in used:continue
                arrival=now+abs(pos[0]-xy[0])+abs(pos[1]-xy[1])
                if arrival>=day*24+23:continue
                gain=_r51_input_gain(target,arrival,day)
                if not gain:continue
                item=target['crop'];new_gross=gross+gain*prices[item]
                new_path=path+((xy[0],xy[1],item,target['birth']),)
                expanded.append((new_gross-1.5*fertilizer*len(new_path),new_gross,arrival+1,xy,new_path,
                                 used|{xy},wheat+(gain if item=='WHEAT' else 0),carrot+(gain if item=='CARROT' else 0)))
        if not expanded:break
        expanded.sort(key=lambda s:(-s[0],-s[1],s[2],s[4]))
        beam=expanded[:8]
        if depth>=2:
            candidate=beam[0]
            if best is None or (-candidate[0],-candidate[1],candidate[2],candidate[4])<(-best[0],-best[1],best[2],best[4]):best=candidate
    if best is None:return [],{'WHEAT':0,'CARROT':0}
    return list(best[4]),{'WHEAT':best[6],'CARROT':best[7]}

def _r51_input_control(obs,action,state):
    step=int(obs['step']);day=step//24;hour=step%24;player=int(obs['player']);farm=obs['farms'][player];private=obs['private']
    native=_IMPL.chassis.players[player]
    if state.get('day')!=day:state.update(day=day,workers={},pending=None,placed=[])
    for x,y in state['placed']:
        tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('fertilized_until_day',-1)>=day+2:_R51_INPUT_REPORT['input_confirmed_applications']+=1
        else:_R51_INPUT_REPORT['input_application_errors']+=1
    state['placed']=[]
    if state.get('pending'):
        pending=state.pop('pending')
        for actor,plan in pending.items():
            if len(farm['hands'])>=actor:state['workers'][actor]=plan;_R51_INPUT_REPORT['input_confirmed_hires']+=1
            else:_R51_INPUT_REPORT['input_hire_errors']+=1
    if state['workers']:
        changed=copy.deepcopy(action)
        for actor,plan in state['workers'].items():
            inv=private['inventories'][actor];pos=tuple(farm['hands'][actor-1]);cmd=['PASS']
            if not plan['loaded']:
                stock=projected_shed(changed,FarmView(obs));q=min(plan['quantity'],max(0,stock.get('FERTILIZER',0)))
                if q and _shed_adjacent(pos,10):
                    cmd=['PICKUP','FERTILIZER',q];plan['loaded']=True;_R51_INPUT_REPORT['input_loaded_units']+=q
                    if q<plan['quantity']:_R51_INPUT_REPORT['input_stock_shortfalls']+=plan['quantity']-q
            elif inv.get('FERTILIZER',0):
                while plan['path']:
                    x,y,crop,birth=plan['path'][0];tile=farm['tiles'][y][x]
                    if not isinstance(tile,dict) or tile.get('crop')!=crop or tile.get('planted_day')!=birth or tile.get('fertilized_until_day',-1)>=day+2:
                        plan['path'].pop(0);continue
                    cmd=_v219_walk(pos,(x,y)) or ['FERTILIZE']
                    if cmd==['FERTILIZE']:state['placed'].append((x,y));plan['path'].pop(0);_R51_INPUT_REPORT['input_application_requests']+=1
                    break
            changed['hands'][actor-1]=cmd
        return changed
    if hour not in (1,2,3) or not 12<=day<=28:return action
    planned=_v219_native_day(native,day);expected=max(len(a.get('hands',[])) for a in planned)
    if any(o and o[0]=='HIRE' for a in planned[hour:] for o in a.get('market',[])) or native['pending']:return action
    parents=[_V219_STATES.get(player,{}),_V233_STATES.get(player,{})]
    # A parent may retry after a full market queue; its headcount must remain native.
    if day in (12,18) or any(p.get('committed') and p.get('requested_day')!=day for p in parents):return action
    if any(p.get('pending') for p in parents) or any(o and o[0]=='HIRE' for o in action.get('market',[])):return action
    owned=set(range(1,expected+1))
    for p in parents:
        actors=set(p.get('workers',{}))
        if owned&actors:return action
        owned|=actors
    if owned!=set(range(1,len(farm['hands'])+1)):return action
    targets=_r51_input_forecast(obs,native['route'],expected);plans=[];total_q=0;total_cost=0;all_units={'WHEAT':0,'CARROT':0}
    stock=projected_shed(action,FarmView(obs));purchases=sum(max(0,int(o[2])) for o in action.get('market',[]) if len(o)>2 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    # Units act before market orders. Preserve the native next-turn pickup,
    # after the current parent's actual sales/purchases, before buying tour inputs.
    available=max(0,stock.get('FERTILIZER',0))
    for o in action.get('market',[]):
        if len(o)>=3 and o[:2]==['SELL','FERTILIZER']:available=max(0,available-max(0,int(o[2])))
        elif len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER']:available+=max(0,int(o[2]))
    next_native=planned[hour+1];native_pickups=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [next_native.get('farmer') or ['PASS'],*(next_native.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    topup=max(0,native_pickups-available)
    plans,total_q,total_cost,all_units=_r68_joint_plans(obs,action,targets,stock,purchases,topup)
    if not plans:return action
    state['pending']={len(farm['hands'])+1+i:plan for i,plan in enumerate(plans)}
    _R51_INPUT_REPORT['input_hire_requests']+=len(plans);_R51_INPUT_REPORT['input_purchase_requests']+=total_q+topup
    _R51_INPUT_REPORT['input_forecast_wheat']+=all_units['WHEAT'];_R51_INPUT_REPORT['input_forecast_carrot']+=all_units['CARROT']
    changed=copy.deepcopy(action);changed['market'] += [['BUY_PRODUCT','FERTILIZER',total_q+topup]]+[['HIRE'] for _ in plans];return changed

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);player=int(observation['player']);state=_R51_INPUT_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R51_INPUT_STATES[player]={'step':-1}
            _R51_INPUT_REPORT.update(input_hire_requests=0,input_confirmed_hires=0,input_hire_errors=0,input_purchase_requests=0,
                input_loaded_units=0,input_stock_shortfalls=0,input_application_requests=0,input_confirmed_applications=0,
                input_application_errors=0,input_errors=0,input_forecast_wheat=0,input_forecast_carrot=0)
        state['step']=step;action=_R51_INPUT_PARENT(observation,configuration)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r51_input_control(observation,action,state)
        _R51_INPUT_REPORT.update(getattr(_R51_INPUT_PARENT,'telemetry',{}));return action
    except Exception:
        _R51_INPUT_REPORT['input_errors']=_R51_INPUT_REPORT.get('input_errors',0)+1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_R51_INPUT_REPORT
agent=globals().pop('agent')

# EXP182: project the final hour's actual worker actions before automatic deposit.
_R51_WAREHOUSE_PARENT=agent
_R51_WAREHOUSE_REPORT={}

def _r51_close_warehouse(obs,action):
    step=int(obs['step']);day=step//24
    if step%24!=23 or not 12<=day<=28:return action
    # No speculative product purchase/worker count model: these hours abstain.
    if any(o and o[0] not in ('SELL',) for o in action.get('market',[])):return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={k for k,q in demand.items() if q>private['seeds'].get(k,0)}
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:c=['PASS']
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    post=dict(private['shed'])
    for o in action.get('market',[]):
        if len(o)>=3 and o[0]=='SELL':post[o[1]]=max(0,post.get(o[1],0)-max(0,int(o[2])))
    needed=sum(post.values())+sum(max(0,q) for inv in private['inventories'] for q in inv.values())-100
    if needed<=0:return action
    result=copy.deepcopy(action);orders=result['market']
    # Grain and fertilizer have native input obligations; other products do not.
    # Additional commodity sales are bounded by actual post-action physical stock.
    for item in sorted((p for p in PRODUCTS if p not in ('WHEAT','FERTILIZER')),key=lambda p:-obs['market']['prices'].get(p,0)):
        qty=min(needed,post.get(item,0))
        if not qty:continue
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
        if existing is not None:existing[2]=max(0,int(existing[2]))+qty
        elif len(orders)<10:orders.append(['SELL',item,qty])
        else:continue
        needed-=qty;post[item]-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
        if needed<=0:break
    if needed>0:
        native=_IMPL.chassis.players[int(obs['player'])];reserve=0
        for t in range(step+1,719):
            future=_IMPL.chassis.routes[2 if t>=648 else native['route']][t]
            for c in [future.get('farmer') or ['PASS'],*(future.get('hands') or [])]:
                if len(c)>1 and c[:2]==['PICKUP','WHEAT']:reserve+=max(0,int(c[2]) if len(c)>2 else 1)
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT','WHEAT'] for o in future.get('market',[])):break
        incoming=sum(max(0,inv.get('WHEAT',0)) for inv in private['inventories'])
        others=sum(q for p,q in post.items() if p!='WHEAT')+sum(max(0,q) for inv in private['inventories'] for p,q in inv.items() if p!='WHEAT')
        # Even if every other carried item deposits first, this grain reserve fits.
        qty=min(needed,post.get('WHEAT',0),max(0,post.get('WHEAT',0)+incoming-reserve)) if 100-others>=reserve else 0
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL','WHEAT']),None)
        if qty and (existing is not None or len(orders)<10):
            if existing is not None:existing[2]=max(0,int(existing[2]))+qty
            else:orders.append(['SELL','WHEAT',qty])
            needed-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
    _R51_WAREHOUSE_REPORT['warehouse_projected_unresolved']+=max(0,needed)
    if result!=action:_R51_WAREHOUSE_REPORT['warehouse_changed_turns']+=1
    return result

def agent(observation,configuration=None):
    result=_R51_WAREHOUSE_PARENT(observation,configuration)
    try:
        if int(observation['step'])==0:_R51_WAREHOUSE_REPORT.update(warehouse_changed_turns=0,warehouse_extra_sales=0,warehouse_projected_unresolved=0,warehouse_errors=0)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):result=_r51_close_warehouse(observation,result)
    except Exception:_R51_WAREHOUSE_REPORT['warehouse_errors']=_R51_WAREHOUSE_REPORT.get('warehouse_errors',0)+1
    _R51_WAREHOUSE_REPORT.update(getattr(_R51_WAREHOUSE_PARENT,'telemetry',{}));return result
agent.telemetry=_R51_WAREHOUSE_REPORT
agent=globals().pop('agent')

from itertools import permutations as _r53_permutations
_R53_LABOR_REPORT=dict(labor_requests=0,labor_hires_avoided=0,labor_spawn_errors=0,labor_confirmed=0,labor_day26=0,labor_day27=0,labor_day28=0)

def _r53_labor_assignment(obs,action,fertilizer):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    if day not in (26,27,28) or step%24>2:return None
    # Do not preempt a later price-gated fertilizer request with a smaller unfertilized team.
    if day==27 and not fertilizer:return None
    count=3 if fertilizer else 2
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    for i,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(positions)]):
        if c and c[0] in MOVES:
            dx,dy=MOVES[c[0]];positions[i]=[max(0,min(9,positions[i][0]+dx)),max(0,min(9,positions[i][1]+dy))]
    access=((4,4),(5,4),(4,5),(5,5));spawns=[]
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    for i in range(native_hires+count):
        chosen=min(access,key=lambda p:(sum(tuple(q)==p for q in positions),access.index(p)));positions.append(list(chosen))
        if i>=native_hires:spawns.append(chosen)
    groups=(((5,5),(6,5),(7,5),(8,5)),((9,5),(9,6),(8,6)),((5,6),(6,6),(7,6))) if fertilizer else (tuple((x,5) for x in range(5,10)),tuple((x,6) for x in range(5,10)))
    choices=[];remaining=23-step%24
    for assignment in _r53_permutations(groups):
        costs=[]
        for start,path in zip(spawns,assignment):
            distance=abs(start[0]-path[0][0])+abs(start[1]-path[0][1])
            distance+=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(path,path[1:]))
            distance+=min(abs(path[-1][0]-x)+abs(path[-1][1]-y) for x,y in access)
            costs.append(distance+(3 if fertilizer else 2)*len(path)+1+int(fertilizer))
        if max(costs)<=remaining:choices.append((max(costs),sum(costs),assignment))
    if not choices:return None
    _,_,assignment=min(choices)
    return dict(paths=assignment,spawns=spawns,remaining=remaining,workers=count,fertilizer=fertilizer)

_R53_LABOR_PARENT=agent
def agent(observation,configuration=None):
    if isinstance(observation,dict) and observation.get('step')==0:
        for k in _R53_LABOR_REPORT:_R53_LABOR_REPORT[k]=0
    result=_R53_LABOR_PARENT(observation,configuration)
    _R53_LABOR_COMBINED.update(getattr(_R53_LABOR_PARENT,'telemetry',{}));_R53_LABOR_COMBINED.update(_R53_LABOR_REPORT)
    return result
_R53_LABOR_COMBINED={}
agent.telemetry=_R53_LABOR_COMBINED
agent=globals().pop('agent')

# EXP193: deterministic HIRE spawn after native unit actions, then next-turn pickup.
def _r62_input_start(obs,action,index):
    farm=obs['farms'][obs['player']]
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    for actor,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(positions)]):
        if c and c[0] in MOVES:
            dx,dy=MOVES[c[0]]
            positions[actor]=[max(0,min(9,positions[actor][0]+dx)),max(0,min(9,positions[actor][1]+dy))]
    access=((4,4),(5,4),(4,5),(5,5))
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    for _ in range(native_hires+index+1):
        chosen=min(access,key=lambda p:(sum(tuple(q)==p for q in positions),access.index(p)))
        positions.append(list(chosen))
    return int(obs['step'])+2,chosen

agent=globals().pop('agent')

def _r68_joint_plans(obs,action,targets,stock,purchases,topup):
    farm=obs['farms'][obs['player']];choices=[]
    for mode,first_crop in enumerate((None,'WHEAT','CARROT')):
        remaining=dict(targets);plans=[];total_q=0;total_cost=0;total_value=0
        all_units={'WHEAT':0,'CARROT':0}
        for i in range(_R51_INPUT_MAX_WORKERS):
            subset={xy:t for xy,t in remaining.items() if t['crop']==first_crop} if i==0 and first_crop else remaining
            path,units=_r51_input_path(obs,subset,action,i);q=len(path)
            if q<3 or len(action.get('market',[]))+2+i>10 or sum(stock.values())+purchases+total_q+q+topup>95:break
            quote=_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-total_q-q-topup)
            cost=(q+(topup if i==0 else 0))*(quote+2)+_v219_fib(int(farm['hires_today'])+i)
            value=sum(n*max(1,_r37_market_price(item,obs['market']['inventory'][item]+all_units[item]+n)-2) for item,n in units.items())
            if value<1.5*cost+50 or farm['money']<total_cost+cost+3000:break
            plans.append({'path':path,'quantity':q,'loaded':False});total_q+=q;total_cost+=cost;total_value+=value
            for item,n in units.items():all_units[item]+=n
            for x,y,_,_ in path:remaining.pop((x,y),None)
        score=(total_value-total_cost,total_value,-total_cost,-len(plans),-mode)
        choices.append((score,plans,total_q,total_cost,all_units))
    _,plans,total_q,total_cost,all_units=max(choices,key=lambda v:v[0])
    return plans,total_q,total_cost,all_units

agent=globals().pop('agent')

_R70_STATES={}
_R70_REPORT={}

def _r70_parent_fert_qty(obs,action,planned,offset):
    stock=dict(projected_shed(action,FarmView(obs)))
    for order in action.get('market',[]):
        if len(order)<3:continue
        op,item,quantity=order[:3];quantity=max(0,int(quantity))
        if op=='SELL':stock[item]=max(0,stock.get(item,0)-quantity)
        elif op in ('BUY_PRODUCT','BUY_ANIMAL'):
            stock[item]=stock.get(item,0)+min(quantity,max(0,100-sum(stock.values())))
    next_action=planned[offset+1] if offset+1<len(planned) else {}
    commands=[next_action.get('farmer') or ['PASS'],*(next_action.get('hands') or [])]
    native_need=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in commands if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    quantity=max(10,10+native_need-max(0,stock.get('FERTILIZER',0)))
    if quantity>max(0,100-sum(stock.values())):
        _R70_REPORT['parent_input_capacity_declines']+=1
        return 10
    if quantity>10:
        _R70_REPORT['parent_input_guard_turns']+=1
        _R70_REPORT['parent_input_guard_extra_units']+=quantity-10
    return quantity

def _r70_before(obs):
    player=int(obs['player']);step=int(obs['step']);state=_R70_STATES.get(player)
    if state is None or step<=state['step']:
        state=_R70_STATES[player]={'step':-1,'pending':[],'roles':set()}
        _R70_REPORT.update(parent_input_guard_turns=0,parent_input_guard_extra_units=0,
            parent_input_requests=0,parent_input_confirmed=0,parent_input_shortfalls=0,
            parent_input_errors=0,parent_input_capacity_declines=0)
    state['step']=step
    for request in state['pending']:
        actor,quantity,old=request
        actual=max(0,int(obs['private']['inventories'][actor].get('FERTILIZER',0))-old)
        _R70_REPORT['parent_input_confirmed']+=min(quantity,actual)
        _R70_REPORT['parent_input_shortfalls']+=max(0,quantity-actual)
    state['pending']=[]
    return state

def _r70_after(obs,action,state):
    player=int(obs['player']);day=int(obs['step'])//24
    for actor,role in _V219_STATES.get(player,{}).get('workers',{}).items():
        if not role.get('needs_fertilizer'):continue
        key=(day,actor);inv=obs['private']['inventories'][actor].get('FERTILIZER',0)
        if key not in state['roles']:
            state['roles'].add(key)
            desired=role.get('fertilizer_quantity',10 if role['kind']=='fertilizer' else 5)
            if role.get('loaded') and not role.get('pickup_requested') and inv<desired:
                _R70_REPORT['parent_input_shortfalls']+=desired-inv
        command=action.get('hands',[])[actor-1] if actor<=len(action.get('hands',[])) else ['PASS']
        if len(command)>1 and command[:2]==['PICKUP','FERTILIZER']:
            quantity=max(0,int(command[2]) if len(command)>2 else 1)
            _R70_REPORT['parent_input_requests']+=quantity
            state['pending'].append((actor,quantity,int(inv)))

_R70_PARENT=agent

def agent(observation,configuration=None):
    state=None
    try:state=_r70_before(observation)
    except Exception:_R70_REPORT['parent_input_errors']=_R70_REPORT.get('parent_input_errors',0)+1
    result=_R70_PARENT(observation,configuration)
    try:
        if state is not None:_r70_after(observation,result,state)
    except Exception:_R70_REPORT['parent_input_errors']=_R70_REPORT.get('parent_input_errors',0)+1
    _R70_REPORT.update(getattr(_R70_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R70_REPORT
agent=globals().pop('agent')

def _r79_tomato_fertilizer_worthwhile(obs,action):
    if obs['market']['prices']['FERTILIZER']<=30:return True
    farm=obs['farms'][obs['player']];day=int(obs['step'])//24;bonus=0
    for y in (5,6):
        for x in range(5,10):
            tile=farm['tiles'][y][x]
            if not isinstance(tile,dict) or tile.get('crop')!='TOMATO':continue
            birth=tile['planted_day'];until=tile.get('fertilized_until_day',-1)
            bonus+=sum(until<d and 8<=d+1-birth<=11 for d in range(day,day+3))
    if not bonus:return False
    inventory=obs['market']['inventory']
    price=max(1,_r37_market_price('TOMATO',inventory['TOMATO']+bonus+10)-2)
    fertilizer=max(1,_r37_market_price('FERTILIZER',inventory['FERTILIZER']-10)+2)
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    extra_labor=_v219_fib(int(farm['hires_today'])+native_hires+3)
    return bonus*price>=2*(10*fertilizer+extra_labor)+100

agent=globals().pop('agent')

# EXP216: original adaptation of economic feed and fertilizer-sale concepts.
# Conceptual credit: Steven Lee Hans, "Lord Momo Returns", September12 snapshot.
_R85_FEED = True
_R85_FERT = True
_R85_PARENT = agent
_R85_STATES = {}
_R85_REPORT = {}

def _r85_feed(obs, action):
    step=int(obs['step']);day=step//24
    if not 10<=day<=28 or step%24>21:return action
    player=int(obs['player']);native=_IMPL.chassis.players[player]
    tape=_v219_native_day(native,day)
    expected=max(len(a.get('hands',[])) for a in tape)
    farm=obs['farms'][player];positions=[farm['farmer'],*farm['hands']]
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    prices=obs['market']['prices'];changed=False
    for actor,command in enumerate(commands[:expected+1]):
        if command!=['FEED'] or actor>=len(positions):continue
        tile=_tile_at(farm['tiles'],positions[actor])
        if not isinstance(tile,dict) or tile.get('animal') not in ('GOOSE','COW','SHEEP'):continue
        if tile.get('fed_today') or int(tile.get('consecutive_unfed',0))!=0:continue
        if int(obs['private']['inventories'][actor].get('WHEAT',0))<=0:continue
        item={'GOOSE':'EGG','COW':'MILK','SHEEP':'WOOL'}[tile['animal']]
        bonus=1+max(0,int(tile.get('pending_care_bonus',0)))
        if bonus*(float(prices[item])+5)*1.25>=float(prices['WHEAT']):continue
        if not _r86_next_feed(obs,positions[actor]):continue
        commands[actor]=['PASS'];changed=True
        _R85_REPORT['feed_skips']+=1
    if not changed:return action
    result=copy.deepcopy(action);result['farmer'],result['hands']=commands[0],commands[1:]
    return result

def _r85_reserve(obs, state):
    step=int(obs['step']);player=int(obs['player']);native=_IMPL.chassis.players[player]
    route=native['route'];key=(route,step)
    cache=state.setdefault('native_reserves',{})
    if route not in cache:
        # Backward recurrence preserves field-before-market order within a turn.
        reserve=[0]*720
        for t in range(718,-1,-1):
            a=_IMPL.chassis.routes[2 if t>=648 else route][t]
            pickup=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [a.get('farmer') or ['PASS'],*(a.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
            purchase=sum(max(0,int(o[2])) for o in a.get('market',[]) if len(o)>2 and o[:2]==['BUY_PRODUCT','FERTILIZER'])
            reserve[t]=pickup+max(0,reserve[t+1]-purchase)
        cache[route]=reserve
    dedicated=0
    for parent in (_V219_STATES.get(player,{}),_V233_STATES.get(player,{})):
        for actor,role in parent.get('workers',{}).items():
            if not isinstance(role,dict) or not role.get('needs_fertilizer') or role.get('loaded'):continue
            desired=role.get('fertilizer_quantity',10 if role.get('kind')=='fertilizer' else 5)
            carried=obs['private']['inventories'][actor].get('FERTILIZER',0)
            dedicated+=max(0,desired-carried)
        pending=parent.get('pending') or {}
        if pending.get('fertilizer'):dedicated+=10
    inputs=_R51_INPUT_STATES.get(player,{})
    for actor,plan in {**inputs.get('workers',{}),**(inputs.get('pending') or {})}.items():
        if not plan.get('loaded'):dedicated+=max(0,int(plan['quantity']))
    return max(14,cache[route][min(719,step+1)]+dedicated)

def _r85_fertilizer(obs, action, state):
    step=int(obs['step']);day=step//24
    if not 6<=day<=28:return action
    market=action.get('market',[])
    if len(market)>=MAX_ORDERS or any(o and o[0]!='SELL' for o in market):return action
    stock=projected_shed(action,FarmView(obs))
    held=max(0,int(stock.get('FERTILIZER',0)))
    sold=sum(max(0,int(o[2])) for o in market if len(o)>2 and o[:2]==['SELL','FERTILIZER'])
    extra=held-sold-_r85_reserve(obs,state)
    if extra<=0:return action
    result=copy.deepcopy(action);result['market'].append(['SELL','FERTILIZER',extra])
    _R85_REPORT['fert_sale_turns']+=1;_R85_REPORT['fert_sale_units']+=extra
    return result

def agent(observation, configuration=None):
    result=_R85_PARENT(observation,configuration)
    try:
        step=int(observation['step']);player=int(observation['player'])
        state=_R85_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R85_STATES[player]={'step':-1}
            _R85_REPORT.update(feed_skips=0,fert_sale_turns=0,fert_sale_units=0,economic_overlay_errors=0)
        state['step']=step
        if configuration is not None and any(configuration.get(k,v)!=v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):return result
        if _R85_FEED:result=_r85_feed(observation,result)
        if _R85_FERT:result=_r85_fertilizer(observation,result,state)
        if step%24==23:result=_r51_close_warehouse(observation,result)
    except Exception:
        _R85_REPORT['economic_overlay_errors']=_R85_REPORT.get('economic_overlay_errors',0)+1
    _R85_REPORT.update(getattr(_R85_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R85_REPORT
agent=globals().pop('agent')

# EXP217: planned next-day service is required before discretionary feed cuts.
_R86_FEED_CACHE = {}

def _r86_next_feed(obs, target):
    step=int(obs['step']);day=step//24
    if day==28:return True  # No second dawn follows before game termination.
    player=int(obs['player']);native=_IMPL.chassis.players[player]
    tomorrow=day+1;route=2 if tomorrow>=27 else native['route'];key=(route,tomorrow)
    if key not in _R86_FEED_CACHE:
        positions=[(4,4)];wheat=[0];access=((4,4),(5,4),(4,5),(5,5));feeds=set()
        for hour in range(24):
            a=_IMPL.chassis.routes[route][tomorrow*24+hour]
            commands=[a.get('farmer') or ['PASS'],*(a.get('hands') or [])]
            for actor,command in enumerate(commands[:len(positions)]):
                if not command:continue
                pos=positions[actor];op=command[0]
                if op in MOVES:
                    dx,dy=MOVES[op];positions[actor]=(max(0,min(9,pos[0]+dx)),max(0,min(9,pos[1]+dy)))
                elif command[:2]==['PICKUP','WHEAT'] and pos in access:
                    wheat[actor]+=max(0,int(command[2]) if len(command)>2 else 1)
                elif op=='FEED' and wheat[actor]>0:
                    wheat[actor]-=1
                    if hour<=21:feeds.add(pos)
                elif op=='DROP' and pos in access:wheat[actor]=0
                elif command[:2]==['PLACE','WHEAT'] and pos in access:
                    wheat[actor]=max(0,wheat[actor]-max(0,int(command[2]) if len(command)>2 else 1))
            for order in a.get('market',[]):
                if order and order[0]=='HIRE':
                    chosen=min(access,key=lambda p:(positions.count(p),access.index(p)))
                    positions.append(chosen);wheat.append(0)
        _R86_FEED_CACHE[key]=frozenset(feeds)
    return tuple(target) in _R86_FEED_CACHE[key]

agent=globals().pop('agent')
