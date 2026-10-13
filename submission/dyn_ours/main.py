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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_NkvK;td_}mYb-<kV1hb-|BBH08vR6#2c2Y0o1Az-1!;!1B9`tLi_omrI`Zf<TKS$%k}R!?m9ba%yvM})h%x%t0-^MCx)fBWZe{<r`1uiyM%|MV~a^`HOc%a`B$^69tVzWL+joB#4p|Ih#V-@bg~%a{N4pZ?|l{^$Sx<?H|S&0l{1kAM5+*VpfU|Mv4YFW=n$dj0g}zfJeYi}O$2<?BEFcKz|k!}tF9A20jQ{Q33Q&wuql^!V%K(}u7A^4A}Jy?&#9@%7Jq`uT^SK7IXwZ(ncUytL-qzy0-k{pIUF6r=v__4nhbzbxJl-~RjGe_8+3*FUtb=3|QcuZ};xpL6j^_aA&8%Hbn-e~x|DUw;4L$M633<wrjM{&nighrKWA;lql*5>D{PPv2hA{5(S%t+jmlUSuuB2jNlOuD^YL`{LVA<pOx48Ng_Uay0ATRd?h*jB-!qbLO3f->%p1zI^|u>yNKL18Xg}jt}_Dg8uyZ{@0xE6o&HT88qb#woL|y01R%M$?enU>#yZkZ=0Zuw*lid1N(Ph$9)*j<D(wq*fw4|lezI|>-TQ>hhg50(ckyS&m5Qk$)j!Kb0uxE{h{~W5r#Y4(aySQ9zInxg~z{nm(u#V+v1r;TK~ZA^R`zBZ0dHQ??>RAgy?h4=2%m*ds2SB`?2dXcZp?Y#$lJc_~~b?JJ@Ho?(aXH{@~I(`<R7q<Buil9iK|(eb@<tg$3{G2QDbt&~*UO$0io^@wb%)1yAp(1uZ`+^@quyE54|5KaY#-IrXu#2wq~ajq!6-4itXN9=OnXcnoX(H{q|?xBdRR>pv-f<n_lNuit+D+rPX1`uT?+fB4_aEAIZ6;16bE3=ldwe{=IXif_Ynx4zxGAAM>3$h5SS>!)&uA5UrNzbnp<=e~NY%V+9*G?=n-*KDWJ#&hmHDooJ-9J7*j_sZkXe9SPx`8_q>`%Uw1TTdSC<90Z6S3BqKgq@Sm`s7<##p`lvZ=U?p*&Y60L&?APFMR|8n#(;z`NH>>LRhhl*{7Gq{OsZKoW<x}W}g>6`Up*9e=oEPvcN^yd3t#fv=fd`Ud`1ZNUbJt6VHuSGFKALpIpteE+ZXmIC+GygW+y}@UNeK{SS3`23h6171RV@(sJL2eIksN_hAPQDZy;$BcC*H;Pf8e0N<JN_Zz$vJ<j!%SfuOH9Md}dYO634dItmiFkDvl2Lal@8ilY=WC83rLq~)hkG~Tlk#J4AG!zl~A}n_#eU*ARd~YOpkqw5Q$Sh<(D|xRy>vIrHWFHvsi@I$9S4QULwQFt%{8)>_BUATCMtfnR^9YMZZ(TtZ_#?AVc8>U+O{2B;+1qEu@U+TAxcC&XT;k&^veb3gt#R;+<peLpbNv!DH_2oYE+aS4_z~3pHbf1p9HCDCD4yE}9#Q9cMCTn#6gSn(Kk&y(FbTft4sM_yjQht`co57Bd;DFOG8F!Od2hDG1&K)VX%){t@Y;kAs&V5y!cW?*8~y~u>8x*;^tV3P&8qUQ?x$BmF+zyUuCbrIsq?OiG}?1v65nU71D(L%D{+jJ4+21t3co7-xZKwqxFX!Eda^@nJrOT$QsbbYXPjot)Km-!KJGh8b85BM1ONkwm4J!7JlB2>JBhNa)RYt#!k$6LLI6MOL^6{Am*9g0oJUE%vcIPeJdeUBW<g*|`{z!qKKY#QetrEV>zRNMV5o<)I1qX+PhR`+;juaAfyLWXIDc)FPj>z?_&bPtQ*h2J(|_P<+5Q}yk8|-n2{JsDy1W0fU83_&s>gVeo;I?`2pc)=@!jtsyAoCKel9GI>8y`Qb8~Xe{_gSq?enjnZhyJ{`s;rLwv8f#==07^44@N10xrQ5vvB8b_L?tmM|^)ue84z=@oK5nhu_Z~{QVwhd=zy?>PJcWR<Q9;0a<*O?%oLM+!h9HS0a|4h3a?QYM3Xp+Yp?r;Mh6yIY;2DN@{E6jCow?Okxpw3ha4zxy;g<K6V`@O+xB)F~0jFDUhyH2kicbU6AMndIIQH$eqLexp2LqJcn$5J(|i%dtj~G09M5QTQvQLPy71%BNzy{={AUZ{RKRLUBMLg63U3549X9M?j^uqZj|q$GU3N>)A!cS__6fPR3bm<{s){~LJc|I{PX&2*YCfVDDx(p0n$Pw7MFR_iX&;s?QAf2FALN-gTTBMi1>$U<~N(maPuDsf&*Fk#3->UsWIbQmRYJ)I^<q_YTy1_c3Elp>)!4fVcEd7rBFgDiqy+;Wg6eufr7`RB=QSh4Jv8{Cb+L)|NQ#Xr_Zkv&;#Ipn*IpOSmWv&I8S<*qx%zWe{p4sLB<OviM+r^*BUDeLb=l_Q)%?dD|=<TH9)Q#k49HfbO0i8dX;Dn(D9P?k7}oKKLf*bc98Lc$T8o!wYk`lm3h+8S7#HIK;`0`fX+NCUE<0CcMl@G)STp2-Ey}$H{4{JD9vxOxxB|zC3<v_{Wup6;-?>e{P$m$>vGwP`cSWz;pDX(+Wi-7VDF~av>EM!Vz`r|*Ry{Df?J6w4ei~pFAwLhuV2|Hmp^JidE<85h>|&nG5JA%Vo}bOtXm3_x1jm%>bi1wARoIHuX^aq1Dq3k?vL~h0<q|C#JNwqc_EZv8-Q9LI$TrpIv4i8onb91rI?{cu6GvP#)nc0Z$F^rk4%>3Zl3lb^q)Wb>IH00wk8j&EaJOIAnH;TL+=kgQ^A3?5r<Ohs^<y-Vi1scw{iFjg2v+kFHu-VUv@M;syh~Y8Z7+T-r09~m{IhjzzWlY_kJUwf;+b^U(4;XmE^%kc`p~3N3x=X1yE>2#Y2(buhlPV>OEgHEVnQ=0xs$fDv{`k^Q~a`HzgglDSdr?k0kv;HH`P!@fqN*CWS>lP^VQYf+HZ?fl|tBYffofFc=biEB&$~$Gu6y2|!$vM3aP0@9XA>6-Vg^5|BFs9j@}J1BZ$e!Oo;cYl<&5+13MzjOH)Jq8yWPY0_E{hwz>~o8TYsht3DnD|s;-l;4jTz~gplQ=_<hYv`jNiRJZye}6JZDgGh5y1u+bOxR04j(YgBou@9&^V$?HfcA~dup1sde%U4>QdG&v_m4n+oBDi=z4W8h+|Cg{QeJ<1lz4dnLo&lGch2Wz>0)p)3c?o;X~3dwZd0r4u36Z`#=^jTFr{FRjb~X2o(Qkwm;rhMSW$~4#Nm7@`Is+{(3zHY7T_ZBly;S|60i?H6q?F*eL_;K(+T4a$|aMrNa}C1;x|CQix#iMRBKkx9+Ews!Dq&b?qyIUxFP>#Bs~66UzZ1V&#fgvpxv{Mg=Np+EymQ*`#-;L$1{YFeVN>1hlw(^XA5dXHh9T+1!$urS$2Abe`NLvq99G43sgc9&9aaruhNcjM$>(Jd4WK<6l7GPo;ma&6DuMSo6%Q@$&*zl80wR#AHgh6=qSdF;g_fc3+<NCVIpadHN0w)>`Z&^gn_h-FI^^wHEG$i8pd*o6!1@N^lx`1j`ji>4_MJ11%Z+7G!OKS3|4t5i9>3Gq$oPIxMni4Q$_<qVC*p8U9sYlOa{ms^x0+lp@fy#I;~H)N^-nG41A=b_gn~-8{PY#m<0+7)9zAnw5(0Bd^9M%h-k=Sqa7wj<j1@AhOb#un^R7Z9BO-|uw{;s7oH@nfD97ZTFvFl%)!5!$3LpfGkP1+nqTVsATF21vH)f2@hy?p?UIi>VHNSCz&wHs)jMxx8dWx8MuEkwLRV07PbECiR2ro_hj_7sY2t$fYw=VH0@1#VDc^psQ%wFc<SM4Z1-9>7_1-UFE>te4_S3uEWTg&7dVD#@Nyc<aID?m@v@iaIQre2daVQWQ9H~ru8RItvO-;Xlef{k!sfs8fZ{b%!UQe%K^_#jD7~bD&HsB^wpvgxTEJ1@*$3(C$mofLgh$oc9a6LDxXyFe`SjbDtqXm(pT={jBBk_I~KMg>MCE^KmiE3ddwR0t8;nKYnqU;(O6iQeYt9ck~%jN!g4PJ7zxH`&0E<w|>JzusgSzs5(=&N+~9N8Sau49kC?35vz0n-ISzd-*8P}3Ky^|zjsJ!$)`cZl8(4xCv&L+y#+ktmyEH)Yr+C;~^Lrd)QW@=&f%oyiW;TcUB*-kq6nQgUg5rGIU+3FoS0ZV(YR%!oL*-+P(vx38rZR2Vy0de^#&s_!KPzFh957&^CBpGgjgieUiFdz4FM4Q*yu1Ja6L0gAv6Yo@Wn19hJrZv*ZgDY(DI^`pw(xEGF)UwZH>!5#m&81F+aOpx+>0b~=+fCd9^LtUyXFzn`U^L*TfEHw@*e?b8yZR+~Ia!;sB0I`bAH#*hIR)pDrf8H8}{6(&gk`yNcEPYe*DQ#I)%UXQFS@)-_-&t#FDuZYK4WxGcB-)`i^f}$Fl`nEtu_33#ycz*=;8fVRr=TlVl!km@wiYy=%>r${+SZC+DOy#sC=aEigWQ$*4(nc!6wV8i5bsOc#wpS|EzbQ73tsqGsju@{Jz-UxPoAmE=2HT;jYS_1Xn5ro6<GYDs@tq|tq+))?UEDaw|5SJd849o#3Xg~A!KXsXe-{lkIlFl@$nvx(fpiaB<gGO@@q#~k`)sq)WB3DV-4zbxR&yo!ZduYKBvA=1H_F8M*zwL@=X@MluxVP0H}Xdj6j>c2dYJ(l6BRdX+9|kxf8`JO!osJN?<uciWvh1c;7yI^M(BR^3F~Y_a1eF8sHI0pkYx(eqdNZVs!H-z0tj<OfXYc-cXgsl9F}xWj3sI0p~CzW`}r9oRLpV>+D&az52FeJxP7AfjJk}^UE6=GK^TP;6<#~&$YgYbFzNx$(Kl{hS!$?jlpxW3b(Lv7{2`7?yWU#Z8^N;7IKRkK*<)dbgRy{F0)|?Ray5(oQE4T;u_2xXg8J2rBOvvQ{^{=V|w;($n&qp@lPONLAnd$z{H#-^n<jhGnEo!ivLu~IyfX1wT{;R#Jm>p^3<)2<zhr6Zje>ef08{nPIl>D`H_h?w6YPZoy9bFaU}^=d;mHM#{TR->HJ=3;vk%%b#s>Sb9+vs8`-Erw->ycq%XR%NTD&Y`vLa?QhjqGz<w0Kq1P5o;|WRbnwL_#yM#B9JKDT9L=YKwivzCJ*Ph&dmftg#UKNT}f&qh|p1ISg(kb8c7|<N;<pM@l)vq2bifoJ?Lo`uD_aXKMpbkx4F6s|Jv+tKU{r+HOJ+J9*6wK19q)>arg`65FmXx50TebuXNSH85EcHGj`3$A?4sZhONbF1i)mA}W1l2Bvw?wCbWytEHDnN^g>VEX2=`$KCdUSv!8_}YS*&vl2EOP7;r9JWaI-{;Wsx7Lo!hjc0a%^7SKRg)Uf_Z!$<V^ERSS1w7y?Ep7(}aPj0Fp|0(3KXV_nbpZ8QMV&h?hdIbg5a@2%<;^*C`=*9nuBICLRa!8rSk7qL+YD3)WKBnoQ=O#;`3)r@RGGm`dMz%|0WC<^96S$-G;pt&MH(#1L!36{FmFD%RIZmGKjH3QNsUjzp#mjI*@>n^I0fo)FS;S~>ygvOKZX4Fsz+bfhpTqFM0ML^CR0L;Ca>HF5#fSeLC-Z7$0~oGLwdaZy#?2YL0FUM8<(p!K+<Of@_!EPE!WgNnQ9L{sx9g_Ns}rPopl;$c}l)HkFGiR79!Rme-Qh1cXx$5<(2^|4Z6p4*Yse1h(Puz5oJN8*I!zXG72&`2wDMiku#no86AHPp4MPtuk$U<Pq!WAOar<vQ$90C%@rr`!gqDfsieQa#avyR9tVgSN@0O_g?#R&a<D1_`Dve1D@(5jRF|vnl<I-%Zr3Z|H%ukQjrfgephU(#Cg(fpMDnC6-Ez++oJsvFb@65L8OO-eZihvSr&t-%=_HUUT(!#}XA_WEOq3mI|vR0x%6sZN$c=s>j<D8fx|Fh5KPVp~@68&p;t^B?=UZiAJF4`I8h?QD}!xw$DTU<fLEAa++Lche83lW+!M9Ll1}W768y2UZ9%zEg+w0tOQMVQShhvlY3t+?aYX6cq@c^ba*D}P%lPVQM-ne1O_i(r*bkZB@!B8Qf1TKcV?65N0a?9MY6I?;L0>ssUzvL3<xDRi=9CdH*SQ{+$|}VIwMc?+Ut5R8o8YS09QXO!t43!-mth4u@2UdH~J88HGh0K0XzRoiSWA5gxB3zW^ekxBPrVyBLl_&m3?A0*H}XUhtYkNT%@n2cr1B0ikw>NmPr#;DrRw}Ez{{%iu&W0Wd*Zqijs0BpHR~p?&{XQYm9@?(IgGuZ0v2NStt@{?mym5@;MFOfC|3RV~LusQ6+j^d@;O1b1E#54guq02ci=kJ%%SH)InJ(tS7kh9H$g9UwnzRqnnp$+mfiBwnvOQQ{W?XHoxB*Ff`laT7Z_Z=jv1R_?Tj`3EWj|%kA3$h*ARd2}uPhzBn;sQgDcx_1SG>2-0ruWExX_+zMhpT581;=3xnu0;&?IFTAkjFubn32wVbUpJr?yTK!Det<F9Qx&qI4KYR~PnWQxp^@2#Dr&0nPB9G}X=tKfyw}<=X;<_Icsj?vV-!J2ToCKg;vb{(*kV|_u&SBQz4OmYaTvb&G0D5UhRE98FL|{8zk$hIO8}hTEekHc%km(2DR*nMmC!!2oy6*&mTlv-En{MF+<)*_Ey7;PyVh2k~!evh(i<aU1A5n?|K%_DyQf0Y@(FA3H6%;)#70h`HavCx*zyv)BBo)9@ljuuDL?bgi3+Un5wL-;DCT0fHFp-abcN<Kvgt34R7<3uYtIOqns1Zd*>?XHlYQb^a@hd3|Ng+5)y`Umur=o5*5vqa3<I&c#0HU`w71cc&S)LH=M!@I@Fq1fA1x6Sps)A}Jdmk{%djgzy3&j<%n=9qa6`74nH<%|;u{Fzg5-_tEI9Iz-2UiJ2&}|XXy$!(5|L%imdH=J+AG%;oTqW+6hU{&H{mxNVW<1$ODh1!D3?79Eold^nu_u+;n7$YN3(^d1bBAn=oS^yO81ooMeW==w09)p-OBW~1_WJ`SeT{>*DSp@OM8VQ%DGZ~a(SSj9rqIAE#wgIPJA)N<kz13gKZHC7x|mgt$%bdLn_TU4JS8Ol$fXQAw`E8sF4TC9$tMo#u8Zn?00rd<w3HjgfR6o$|3UNs8PZ|vKaTtnsrF-#=tnPxAAYKBhaza$hRzdBFV*nWnB=EDje;1%-~{<hrt8Qr*Y%NDac2ODdo{noNE4mA6F7q9=hM2;is-L=Q74z(lL9QkBUzJB*E545+{U#IVQ}Sr?d5#pw!`Tl5iBx{qFE8F^#1!yVXjXKU^F>sp(PvkvVka$fN#o7p)S`I5p{pxIVFdn?*(vAvWkGAqmx5*;Dwkuda0;IN*&|tl3junt7m$GykmQ1OX5n|b&sbbmIkSH-S<i-jb%pLJgd2sl)`mArH{!VX<<6Apoe!5IekaBK<H2SsN_oM;@(JyYY(XcCzP-jRmh>M@Atw`1zOZ>vnd%$Ymn>V>h@F`AeAklVvahX=3+Lq%Y${}qgLuVUqS_;2zFul;4X&EC9+*0QBV>ud|(V$WaS$OJx{vHi+Ab8pqbUD(XP2|O-H&ZhC0ZRj3evc!}%}vA46i$_A8IX10ZQrRG6_@SRufNBP#Y-0dT<zRe<BK7MAE;B}o=X>6Dt_)R4LbnpX}r^_k#Em!J?GZ_LCVQV)iZV=?$)zDm79v^WR&unblPfuN#jIwtETAe~fKC<99!6pnmU!kq?OqDY`p-@%DKJW=Z6X-T=U3ib$<VAI1Zmfq!_U$WsKXSO7EmNui2j@H(%<mFV)gs`ZdwX+LCOGxA)5_)AxbhT&(<qR;8EfFu=p0B;fQ4`jnF1+O;&KeJXoz^&{B!gp5u6!$$MqoJ%mKJ=U$D9(ryT&j=oy>}>B%QmH>SQI^d0;uayWj0P2{Gx!GCSLg+akK^Yzs9|0fMa-+Ekuq_BsWfz(9)xi-J&TtQV(O>k<DFg6q)%A639Pt~drb@--Q3%Y2hAB~u+&yI`&sxVn(!7=y(sDV9NVN=Sq93Y0D1y98Zuy_KMF?07GYAj`<^@tk_DPkDkx?&mA)_TdT7IkDSLuYa`H$=T9S{*^#tJf)8shnHof5!FY3Y)MtrTtuLcKoEoHL<m@RXeUYpY;v_>2AUKETqHFvC?{DJxZBby6ErbRNTkPzHbzmsP1S8#XIPeFpq<HyqI!JDfNV?P0*mQM7WAAh+hVoq!2<%rtb8wuU00%W2^dzvPLhU!1dS$um}0_&p&xjwaye?XP$)iW@rNaRT7pl5+BulLOO#D|enpkzqf{O4nS)yJhxka*iS_6gQpfP{{00S!8B!e&dl*p&4~U3LpD7>+RT9|Em}&nicce<`LSBUyS>)VRYECDhY=S)`$mAY)pKY0XI5F2i+9QyEcQ+x&irAl96Hm4|wHww=jnZi!7&9=*Hkq$t*?2~cLBLuqrH3sv=0_pfw$N5Xu&kaX#*RIcxD+bPkRZhwMGhYw0#fZfTDHB}R1=sJwL2m4%+g2vpc0sH?pmU}5OLk2E&}PsDu0gP3hhw|!_<+N(Xh6oTt!9g(0N8D_Qg?v@U|vYsd6RcU!sL{B2qVI&-X>WT?KxNRMk!umS{4WxbG|66An7!N5f2SNNWZ3yvV_E99l=QEJ(6&&MJ%Q13~Yt^fkT)J+W|K1haF!w3-;3IOsbfTvZO9Cy3;hyH0-WDL#Ba><N|QC;|U=j>RSA*0WJQjD;DCAkT@j@I=7cCL!C6OTx(9sA_ycMppHz@-Pgo>pnuWm#I7^u@9Kpl$Cjm2U8aiFe)2Q%mQSQNS~3QajMHEU-={Tcn+DIUZ$Kb2q~%r7d(bcD4`(~LQ-yta{2IbK*oK<p)jL(YGRf#_SI*e(u6kb9%qi5E;$Ggi9=WappTQCpjDkl)Co8YiUhV%2rV=tUTP&hP#px)N6Z%@yW&bj5-@=oSVqv4D%MLiNahD$+e<;#gXgn^WE}&%eaYZwR6$BqNQD=IA7{HV5|ytuauExE5-7Ni?Z~~5`-s*sWEuc9{ok)dh<Bgi!X5$_BP+WSi_av28UoakW-bwVn>us%$weVdP>JtrrUbO@Oh6cRq9H}c!38NQVX3Iny^Os-qqb5hdZ5MMN^bl3Xy%}UjEDf-3D#aCcIC-AQ$LLcP{@(1&-#$_hBByz36*^7W0AxB4AirkIdxvFt`XqP_u_nFZ{_>C3vMtbP=6{Q6HcFCdJ!zq>$Xd;X)^_|Kj)$%*YWLH=S1U{&_bFjlGPJ?jOZK*jEdU;54Z?-y~OCYa!c#HIFh2|ZL%*p#=7}i0=y8C4o{;Kf_9X~FXgsJ!p54{F65j$-3pQq2uC2QPP9E2bz;&C^dVxxPsjw-wUbsEaSV|(s;K;szfWrrr^U1Ms4QlTn`8S-WWFA6GmQ_gt~0E4B_hqef^)VbyR4gZ+T}`i4<SR*OMP?tOYa8OKIz;*d?(5#F@^3M3s!=Xw4<8M;=PoOPzgg@hsGo|=Q{BuX%cOqL#dd<OotDzBFgq3lGrO<Sa=}{rEF00IU0~#5V+(T+sN&t)nc8XE{NeGnTLe>b%bC{{(>N(h5DBAF}Z43VvSGAn`8ORWZ(jRT`Z@j*BbHT0Mj>3h{!Bo<{1gy$r|Zjyt1l>bUP=B*Kje9;;y~_dJuMTP07Dk#R2pEOisnml-7|AX@y&KD11z?GAOea&g5U22%>^QuX+bnK4t2(=psctq0f9uq3Nhs(lBN{P9B5QA*~U_p_E`TsSUz<2#AKT<Dr*|&*CTmT5U7D52j+`4ie?;J+?)KxIZKHYpO+3H-H+43W6u$%N6!$i}n9`PisrP7*6ouI8Ej%^tL{gWnX87C(xzf6Ut~0H)9Lqy~~Mh&C2dUMX7Yjtxpbez~nAs-2f`NC83ZTDy;T<d}_Uj@)SK%p(HErYaH4aF(<B<fl-r)8P_@C=^C|^eB>fE89GGnmnYyGLQQzwaVXNSRh3_RC%ETE{>FWo1(c(@!xD?~8B3eyV{TeQ-Z4W7<l0u`Avz#-<X2NAS4@wecaw?S0znBg-8v(<z!;n5{zHIYs}Z2AN;&7kCZ(Kj>cYyxh+&IzQkCUpa9MZY_5>Kg{M~>?cFQTTw8=Kv(eoK?K`>vv;hmFmwvPdC4TT&)dxEx~N^r^I)JIoc9;dWYjP^$l(4`ZyIm4}b<Zt=TX>_l|Rvwl5M6AAr(PyIVpqjVU-5<djek_XRvyj|CpmifvJasv!Y5qeICULEpC)Rr>hGq2y^^J4-GdkKN>1+c>v2Cr)vy`PxSi{$JLfj&`LAt|>k{M-t5$ww^+sOArp|xNP9TB`F{%U1tlvF{V^z^vLL5T}f2wD?`-ToDtG4l2On*Ye?_|uFlqfaOe9YdAXps;4UEVlpRGbLI;jZ%{`Z5g&9#kRDVz7~;*NFq6D;7prDy>;`)HyR?8n?Po!bC5GDAmew$%y-#on+gueN>Q{Go>Lj=jRLKPmstVnSF>umI8O_x&G<+BmLQ4Rb5C{V=2ImCtzx%qJ<eZV?B$K3KQ<q{RiQE$aLfcGsH!-XbsO*ostdT}IvH^%b(aLdrV$X;<Nml|bGe%0Fs|mn^qp#&qGWs|OZ_>nZ25m>4#s{Fw>xQ?GXYBk{doGT$g?J2sJM{Zbd`lHtVr#q7GKrpZG?)`SwtIAse5WHp5zD+PSyLkhu#k*s`_orb9afoR;zAj#sdsscOL1U4%3^VR)RDZ{*n8F((u@w*`0dj9ozK>LOuiU0vH)DjI85*d5m7*?C|*Q$U~e}C6j>S8%IS-Lp0in=x8oZ%?7qPrLwN~Z2n?>`nHyMbPgD#Ej%^bseOb|8qbMIS>-G+rlj!;6Ce*Urm7v!e@#b-;`~>1b<Z7Q`eO0S27X=q>aAT;sV@H_V=*8YVL1?T^1+^#-+C^k<_TXtK@u44&+r_?CZ@i$eh?P)34)M~e}r0fB0fwb@LYkkH$`A*KVwBBC)~<5E|G-n1x5$t@TWKRim`&WJVXH?A)e*6tv;h#gRiHe;d@RN8NfVYwo~z56RmOq#2RDJr{hfhpkWT&Ht4kRM&9-DN=Z=5JOt!LC>#ZJni{Fn(i7Uuqcv^Q=3GuVB(FM0WA!r<&}KlGa1Gw(gDS^t^2Ix6L1&|@lm+WWtyVrcTUqax(;_NXcA?4hY)ax6b>KABNe&ZhuA{o%PgqzB6<Q4!@MH!rSB1n&^OOZof^{Y+-JcRJu?T!{zxku5kLc;)@lxvmSC3li0R*8UO+eT*EapTCB)gxpCP!8khMXC@5iwGBRKXmiv9CAg;+zKg-lWl7Ol6_59{a~|YR!2pHLMzBRlK1@y@rgUW~td*!*T~}-Ge-C0wp?}dH_3{$X5<$(CGlm?qgMbZFBi*;7IV}&&+Ck6ogV7wlSihgg*C#s)Y{F<P&%?F3=N6u1UfwJtN3O&&YTJZ4t3UMyj|eaK`Pbw6=%KQd@*Xi6Ex=v`y3nAd#C~%tJ7Ab>##WAP~@&Y*nfZjFpm-KR_MEiaS2l)|Q7NeyWy)IWf_Fu>SC3SxUnN-b>YOXDr<qAs`2akVLA`=m>|b+paC9;sc0%XKF+;YEseyarlAXWH{v5`%6hz6WWo2q(YAsHBTfE3vkIuFLCzLhs+!`#n1G8tElleEy0=Fe%5N3Wj7;ZO<S#y0}M30gQrH+V2<&(cB<}whs5*c+A9`<L={d{xG@vUYd9xUv<_mST<cvP3sVe>Hc9lvxBNJiO)Gz9tveG%=}}1~^U^fTb`y3<h<DQ!O9-w}jHDK_jl38hEAi$5SJsr^Txao{bgdBOWCwVt&K~m0FFj(9{#|M!O~rc}pl>b|O^_>3sg+{C53Zi)mj>m(`Zv~hTJOpO0(lsChVi}z6uA1Tv8tA-?`drSH+q=J{3I-eG%(?<m>@-^o(;oaf6f_6cNbz@Ro<!YoLH_9bFtR8kMy}qF^EW>m9iTaj<DZx!b}tF*Eici&fZmJgVWYKw>lmRU_;gtXH#8Lk&m(?I<uDB8I9%lKdDRWtL+hx7%JyrCz!iI-*ly;BV&^WWZ1gO7<kk)RtESfk1!wOXmw{0@OSK$i&d*^|7@<^{}ifQsxHqSu+;esh#U@U!5loJyb(4K(^?7Lo)K^pAq{q>cFwX!<mT;S&*%7Q@m>C_x;Ks!RuYK}E~-abG}Vz;#9A&I^+^bwt+ziKtg`8p`o{Yzf$}o~)P;Hm0Wbv!GvfOeXRS!H>yyeYiUkPV)p#EnpD66fLTlJEDzPtyy{Rjx*%SuVZ83>rg-jDJ^|DN663eonJfS8wtONBKofE$;b9_;_JzFlIZ14C@Huo~R9aDXG{*1OeB>C*d>|>%;bDXAby*@cj1CEm2hZfbgo?41hs>n_i7V|RFoL$1G&6aWn;vS4X^@Yhf7%-uV`zKK!xbOd$-+%b=yT5(=y1qSH&uPp13tu;~PFh}8zzI}2fFLhzDGl-L*gFioG%ps2D9|~;3p*+PhGNnIAVC%XmgOF(1-tacN_a^``^4cLiiyost4&hL0ai9`w@p424*(@vEJ+E)g8O^G$>u8aK)$4nC$~>JobO1#C*rEulw77<?<NEo;1$Wqz_Ju)*e>{_LK4Tipntc_V=nJWiS}WS?NGEPFGbDghx}L8Mw~W769DN*r!1C((&xb#3PP8)ruD*B!uY=_O<M9(;Wo!uq_nz*M7`wt5r+Q~l*j_dn=Lf&9S#F|)Q0_;#+8>|vLevMr>gVFm;XN7-~iHaKq%g3heB%bO42^+>=b#K?fhhcHS&gbb}QetPuGtGCk)I|eC&74$^%-!xf#28y1l9Po^Y!D;_!>ks-#ck+tioEBS3s@+?*7&+J^FgIZZvj{o?+^@K4oM<sT<Xrmr*?VoTbM9}Y3yq)NnV!pl_jPVR28jg`A{5$6x9LrS+prr;5kHIl^83otFQQ_QVU-H)4BHjpE_@kA119|T0?<NcgP3_?0%nim0H)^KP6#DX358wprsMn|07qRaqM4Kd1K^R#!)&}fzlZWMEA+#jkpw0LJFb9&)IKXIDECWmH0UK02nvR}zvGVrT~=2A}JmGyy-YUtsVT>R<@V99f^9X2rY$o9F2AuvzU?I+Al<<?JWna)nl-Kap5x?7+W)jLTlS4xyR8tVXbni~#15XkG(Gw&0p#xb~^dV~cS09*gXU&v$+zu<YMxrc<Bb74z0$m245okj8DE_36wA3y;_kl((yc)qYCc`A;knNg&D239l7u2e5~@oizf%VqpGu;5HLK5kI0;nn|tS^I#nZQqITX)aSjcQ`3X;oUz$c(#);!}B-gc^d#i3#+opLPBr7EzE<&2!pp?Gj+WF|9ESC%!|JNGOF5-)J^vqL*@^<z&HWmitjK4RayBz;YO<455EVNT_gJi!)=`}baIOI>x}wn;qd<PKfe6+|M#E%`+xo~|NLb#|N2ey^)s5juZB1$_Td>+^UK#wKV;i$4H1<NtY|QXG12OVb{;p|tA$l>gP7#L<ldb52Sa|w+b7S}oySpA_ftbz;tqpl`pY4%k#T4(o6FGW>-dHXytp4JZOk**I$Z^06$-TP8WcZ%`uV#%<o@aBAAb7ucBB6Fdi~`cH+q{)6D&6CHS21U1S$gSN4J>M`#wUq^EKLfi)om@=A#g4Ip-spc%4iqE5$_*w^%mKYJ7GhL<`^Ry_Yx<>zzaT#b7`G9vAU|fgJDs@~<H)#0ZNW$Gr>mef#}vhEgo_Hrx>&d}gm~fuwfMw8L>^lT$!CN|2$DWknE9R4)d{JgYosXG9pZ)hoH&+bVjMXoBVbg*6CUAsxuBFwyD4V#iB#(veDIwCSMJb=qFbfi~(*uzw0jjqqbc;BIg`E!b@z+d6rBK*eC%eRBQce)GFv^E+6)eb`LiQKi(FE$qPiHe#xHMzIdHuhCVbG+^LPxqCcBkssh&bwNyL_xS#WO1bK&-@*5OOb4_6wmo5grzZ@jZg1zOwQ4%g;CUO+5^3>WlYXEW(d-8?U2@%{DwKPw|AO}bPmL-|%PU?$5pv;xfzNJL@gDZqt#%8Qrh5C}u1<1?eAJWsciscbZ(nbZ`)BIwnlx7q&iS?zEjr&;aeys!o(7rfqW3WXx#Ig7`MSasIhn>-svgapGK(RgABvNzi`i|9Iq3v7+6xUp0b3HnU%oIbnPxp?=H?YN`7!RT7s_*_!a0?TJ_`y*2sA)zo%2N}NP9LPHi4ENlyJM}=2-|y6s|s4FN&zqc3S2(-%%BXA5te<BUbFXd2=T>x-SnU-&IYxKHk<|uIBZkawR@y686k#pQAVglm&=7AiAqQkMbIo0gZ<uDBgO!cavIYPEd&u$SAOPusm~qd7c%g&P#n1MW#y9knf+nT<SlUO*H=C<{43JF7JA*Pgqaryc*%s@^?Y2qRNJhODCxMqaMDQl)_gvv_!ge>1Bz?fDUbSw7C-rH)wkpmw}Kf#wcVnKOQu_)pCgUru5|!j;Yv=Nq$k!EN&S5b@}|juE-cJ(M7Cjli8#P7$;JhcpJm4j)CcmJ$&tBvaoFJ!|Get@kBQ>?EDNStmg)ARc+0{%i3O|>z&3VQDj5^5rs->9=^RquR|<;Pjo$P0#VjyaqcJ~joe;ZnO)DU$Y4Fr&XuYj#<JUsp4axU0~QtOJvyW!b7&@gu%xV#4Oj>OZREPtbwq<+8p8{bEO3MJ-EuqvEpiNCS3NEQ8Zxl_q3CFp8}1~xx}jPph)fhjdtOgWa1pFyog*KL743*E1)Q>Q%}^Kl@Qccnq#P*<z1rp?EAil3C{Zah+)x<3w@srr8X=m|ro7)|1d%^?sxZFWX3)waH8dStV~|i4{cTWPg#w$zrIQk~>mYhrPnLw6I#nPr0zGr=1xjr*$jeHg14YS!kem0hDje;yjdrB+pIwHu{47}p6eHd5f+?3@eJ{6*yLb%ga?J>ZSjRgj$j^+yMp(%Jd03qlaNZ)a6?mROGeUnbwnWwrqGdeaK1Za>D_y#}HiY}zuiM!+b$LLZ>S0%?L4alVylwOTB>;~&@LX=4@t2iF?NkncD~uJ9r+tmKbqIZB10GQxRnKO*XC@47^oTFefF#@#cXVTg3LkA~%{u<MqnPq!63voCWO5zGeAbv!y>ob4FUklNzIMCR(My;%0dd7aw}MnRrLRNoE_$#BRv7i0AxWMf%hz^|+!Pb6nO12N^8edTrd8E2xykythob9Fwm6G~OOoqEEvm1iCX*Zti%0ESpFadcUOa?eeKg@19s*p?Q3O&nr4_!XVTw7?nq!OIx~Z10j8>I~@*+W<4R%&@xJdL6Ok_}(Ri#-E+eqc~x@dnjS7Lw3WSBp!+2`9(8kMP>`a)2@bBW7s-^$%3B+Wb_H#+E{Hbr}Tog9^p!$4a)i50$%tWR{iP|4L)@JDdy3qHa+(xC!lm8p6WqR#jWV60=UgdiGRtVKpM|6W8H7n}p7t^iYq@?$hOmXZ-gh5DVV@h$@~MuX<VV-j7Azk&%L_aOx!Y`@5fKrlcirWS@~cKK*?4?DN_84MSB2Iv#H2%*hx!qGzNQ<=$QlX;ZPJDiucsFKGFEHK8KlCs4MLay`*btp4aW0P%!X&2@Cs3E1Txi?G?JX!FY=oi3C0=kh1N0Y3>eY$zlozMI>GhwArk2MIR3s8QYIJ-K9&(_d-Y1@}zRjMwg_z2(UG*mVr@~1;9#{dA5;$!VpT;GO2GEJz~FE}ZJcEp#5O%jUVv&V|aH`@-NtR%G^qNo)ZnUW{hG$^72L^vnw@MkgTM#q=rBpyF*Cn7gWBb0@8^fEz__FE$CIFbuYvQ9>sj~H~RB;7v2#YrvQH|w#{sR2~6z@Aj=fkp~UDs!svLkp1uXxna~5T~%X7n4PB>{;}zdF=8<81!3ZFGQKslDze;w{h9FphAl6;LM;DYga{TFoPT-*RT*!AnmFlxT5eLo`HKAQ7pnE9LIdk#h}V-16PmMw3@t*UlbZmYf|ODSchbA#fQvrkHDB4{;cvsbp9sG;n4A4vt^}iq5Z(BQ*wpw36DqZPtV!Bw54Wzx~5A_Ll;_IU_BCNzm<x~)UFo76ksy;P=!`$8PYW0U!@;(pFk_CPV&aA_RR6t^}29fJcllvL+yzQY8Aq*%=UMQ=i1AlZ9>(HSM0Egh?L3E7;zfZx_0tT@zf^G0VVFdXphDy+r!RO#Z$}ASCU#VO_lO30poxm4m>sO_M}pgm1$NjD@eX2+E9avp^$bY@6Zz2mpviu5U_YI;dCVJY>srOJf$Q!PQXHD+!6CiskT(8gAiLv9utl8qV-@qAspHk@*=c}7cWo?4@p=mrivgFBkKYqgUJ~m!=S}OlsD(;4LIZORWk$61pqnHUFU<IemRpG<on9vKmc2mg=q=-PTq)71tcSsh+t(J4J$8Qv9X&%{giO*5|Z{**^T?ysfgoO+$AC7IDQmgYK}<BQO__D9LrF93h5Th^F5YEjON4?LuzH|2BA~r+W?z@0t^@Bh@5l@-iDu%Cy>U5lNa(Y5j)uWBab^SV2h%*mUhnN=7Hty!g>q?e^H^6<41Nfjc*-JU#CbOIuxj6A|wKW@eP4B($Wu#fA|9f!x%r<&cwjpAK)Z(3sDR!ZeSVkI(#p^(1_7%M4||fkmXqvMJKWjd8sMDHp@#NXya#?VRVHcj8vA9K*>C!cBY_U-Q=#&fRXDpXnaAuG%)760KU7lm4IcoI*8e%ZvvfKl}U>oY2B@vh`e-t-af+@<V}B5O<w0B(5?`Csj*V1o#a}nd#Qt+9?xErynl4uCs1C+Nv>H#1F@m8661T45Zz@yWrV(P0(qOkD3&_Q0!dvt{<C4ZyGYIDtZ^a3_eVq@Hy&hmg?<Y_D9*}U#z2tehulZkJ~0IDo*VggO_!9r7y@2|+T|}t6IllvNz*gJwNl{ZhR5K13^jf<c=t8OP#Dm7w%rYt(9-=yVW?Au9Mse35pnCFu9@ZLOR8=nQ^25-gzJcwJQ@HVP*_33q_dOmQX#yO=|#!J5LvjkpHfAOFgly2it8eehB$<>(gH%ey0(>hEi|*p(x7gEzct>r)5%kuAPj0oG&Cn(yOHu6y0)@ppEHM14qfj#UmJzBgRHBW&n@f9A+o4^Is8ZqhN`f*;lCVwxIS|z55pK?=tL6J4mIbytV&FDEu&)KysCn*iZ$&Tt28xPgyJr1cTug6<bU8h%;XeE4bMBCKk)0TYgE%jXGX(KZK+ATnC&xc6pCb#qeki$TnDV{<YEzB=#`ckMF+@VR9*6tUdxg)rm%8Dg$(HFOtq@a(vz~<b^MNkW${=3lpwwckh`fSnn#sAFm;PE$~^w@1!wku<8YBpW>T{%W`d)eD=Rj?@e~%5ge%59Z^K<wkOHKISr0<aS;{oD*usQf=J3IUJfOkC97{P#S&ZR0*rrmS5Swifq}8CCK{9NeMk$)P{{8qdNvQBJ1PlzR%M((MWP-u5Sf<ru?ZWj4`(6e=Na~vAW>9N@h@#OInl{c}RuZnO4Ksv3!9+&Ag`>o3ih3UKC&G7Q`+O0c1$T)z%g5>)==@Xz4Pq4*_OIhvKEN=;g8Ya8<cTKLvbnoL!bUS&w8awMA+%hyJ25n>!P2-30=PoE2K8JGt!%(dwwnO9Jj3f+^3a{I<cyj`4Qe1{5(=djO*&3%E*xu+rRr?DVUWr8wAUzMdb7h6$F;+#de%UF!<cAvk{D1$kJ2QUk0szM8C_=GS=@!4D+x{fxdf3r?Qe=(Np`~`XZJ-UApt3{L_bg>?MB||CdLN(kHQ8@wG#wm42jf#Kz@hJZ9%iMrEtOMPp?K^6fQy+c)3ASOij(~J*a55yLas5gfr{mq3#%*Ld<gQMm-RNSd5kRiHYicaM8s5AG+~OoTjHX0+O^h!8SXsyU`?~wmtFWG5cIs327ohdqq4EIjRGu0Xz_%_6v>y1CDne>pK92(urqneh!VD5;P4G&w3g8F?>@acp_vUVi}jRVrk><`aTiah#+M@UD6#nlZPYj(k=i!-X0~yNf_maDkVY|jS$vOZOX=(MlU76(>FI4;!a(y$?w*5Zyk}{!}3*B@2hb8>CAdLVIFHy%Yg<kB5;VEvXBDde_?UyB)#5bIeBAkMt4t&Vt{ipo(cwuR0^%>C2!d}uBkHOqjV4^%}8Wg-3w59NTWDD7f{1Pi?tpT57qsoE){5y#ARmOk+7bZoxb^Uu0J|u?9o6x!i=oJ%#B*@&$zE(#B6ni*K%%8w>yurLiEw0cbp5o&Yjv+g?&)IHYL+u34<|P%6RVcV9ctBJbV-kGs}IHWSs#XqERMCvN`QRuXL{!GVf^|e#h2z2}X4Z&^X;m(P)X203?m7b?{RJfw0~#i9`kIzY(YO=Q$&$Zc~wNZo$roT&ezrxKu2n-l?_r@lP!9A{07s_A^fD5kjpf+O>`^$~y+HwNy>A`(hs$sp^777*j}ec%3?2=RT71VdYgy>K!a{s9agqzBN(vlm_j<Br+|eJbVQBOw3z#?1j*#3V9E@)WA~riRpK(+1=ySJHD2{$cHcH@o%r=7euKUN}|JYKvd$2+YW(Mo+_Gj={ESBX2xLH!fOZf5v22h_X2uAdM+<P0gq*gdw{!46mo;J%ahu=e=hq=L?LxhCe^MfwcqQfRgK;E7rAj_9_Qs<-gN$ncMSSMmxS#Fmw*Ulgel!R+gP^0;Nrl85@8#PMKGOi)|rbPB`-4WFMY*Ai@pY_45Yee>&U_;?idTM2gz)rTtCt|x?f-DouCxIB;rKQFs)`FEanyF>)F+_Y}1%Bt^h^XDU!y&avHSsm${;w$s1<!QIJW0S!$|U7;)a#xtNlmykv!2>2t(II(MF-<Vuc56R14KjBaZjO`|gKSo;lrqA0WzkFbWwYM%uh9TW6}wXR-A)>TU*XigA+bhP+ExW1ZR$8K~)hS2R_Qpu=zBEvQjLBYjhZ(dxm|2l{asF$L;O|jeyObG~lQ7w>;;gP<XDl4{t+1MK(C`pSw7ui$owk4kvNC|A{TcQv<8q3jUDwO<F`7%SKS!cM&G{lr>Jhd$)2(`u~Db28oFLZgZhFRdkb>5)1sgnu`#Ci7XgzuNg`r~?qzHL*^smmP=qsWwcNIIx26lVydP&7@D_zif3b>gCZtTPkAdW5oMB^q)pq;-fxt^O&~6S^twK>eN?AriZBt@}bg1`HqHZM0YvXiHR9$@$AZ$xWXTh%(YdC#Dwh;&{&OGM`OsewLYzfQi8cff@16p_+iDUt)~vf=_8WFt=w^()__Tf7!*K?@{`ikm$Qh<sr5jqQr2(36}UE6lPc_P$Bx6)fY*USFGW5T>G=tkd@`5kd>~Jg%}}H(t0NmYHfh-^2*Qcp$w|O;k44dDE)E|zv29)*8Tpvn!PHkMq3RjrAMw%OP8prI?j2W!zf#X7V6xt{)^+Y)$K{@n?wSbm&GQ~1Q4gQp|VG=Z*xgXChifq)+q8XJtukC-HBu*g%Ti@xK0!!))|_%>FB8&uI*`2L>L<T5Rua5{k{o<s_D<87`H9Pp{~Kx9JccZ$8<^wy5R%LOp3w!-~Iaf3%`fLd$6Uc`MzH&GJjnD4?w!WX|*IVDrNdU+Cm@0i3(t3uWA^_3?<UHLv>?=@L_1>?gFX`q~D+tw5>J{H{v;Q5wvw8T_Dnkc0jppXrpIIt`Y9bV#M3F=wcW$^ho|yT(guH|BQ=<`(ZpM+kda{{vh9dkhT7b3V)p@&hA=CA#nI3ifRC7+`E<WDn#OdYN}Mqts0pCi=)L=^!>2p$84Eu?1xxImOHHRk{_1EDCn>%Au)f*O`NZA3VO3pdDu)q8E&f+SgIJ3eiD+Y^CSbAQAlJ1*U@^vyd^YaPKEXQWb}QQ8Ne1}4;L5eKB?p5C6~rQw;`0j)rEYLIUO+6F<~e;R&_aJih<YGJoe+Hv*_eZEszCIvIIkzdYlzT!-0BFaxF{;_Y`F?dtw)vln%0V8Hxcu_?$oCozv-(Fn(HT%7Ze&tia%!)FsH06H#Ympz{z?r3!Tkw&SqgRm}TG5v#J0VFeH<>WFL;@&K?shI|XpI{P@|wzmK~c38E>WC&kq91ez<sQ4inC|R8LJSA%i6U#PtW)IX&!NaQfScT{V!Y^h#Ty(FRHyVOMD*uqA{f^^Xr!vd6>0p+vatf(lf!LctpV;Pl6bcba(LHR6iPQh~N8$Y$rZr1Zh<`L}q!5B&-I!r)KW4xY|1VT?$Spu(H6oA5$sjCBE2s8oJ?{%oWCCC@?!_=5Bh!=9tavk=72{OXt_tfg`+UZf7u?tM0s|wqDW-M6Q8LL#5#-j7^vMs1b6#qxkd3hDIA@h1`@}R#h*XGz1gftvpU9IDq%ssWw$Um9?mX{NQJ2^OmK7!Ai4u4Z{c?;y!d^o;DRg2zOQJ<&<-KDETZl|(G8s{Tt|r51MQ~*L>-a->mRvQ~xer4Qh#}dKAnrNS3_K0IwE28|RDjOu|1!+v5+2o?X^E1MID8_NCDD-*+VHVM(x+}x4?koK1C|E^*;D;}fVu8<T0=s>g}$v+<;dP^h%D*61Is82Pf8^{-cu2|9X@CV#yr*ENgxHF*>#}Gh7Kr9x35!}Wfeg^G2ycr7zrifTH8a5dCHvNu`IH-dyurair1~s{#AVihfCO{hWkBH?uL?@*|GM{$Z%;YI<ShJ;bat4e8@anifc_nDU$(+<LE5((R-JwXp)*)vd0h3eAuQaOE=25Roxfz6S(csyv?A09>NsY-=DymhD-ENbGivHeD|3rAB8PV!i-1R`@JeS5z}XJ{TXm;Mcuc9+Eq<ChV{X6N0#iwP1<P&JtlOq#2DEc3f+y2VnM1pINR(}7<zNbczGP8I{FHMZepf6*w8fULE;*murd+o#+)y#9SVI7a>$s(a;T<|FyFd5+o6!-kk4f1w0ZFi6JpC5P+zIAAQs?K!olsTislZ@Am?Lv!9?7<2v|GSI3X4?%4}>xWAho9*>d=}M0jX&s4{JbAlbB&L&me+dcCOKA<Q3j0l7hv=D^%>sU}@(+o86F7@9>6uxM2p6K_GxfT%CTP^fCygBlX>9hHnK-bz+Ncqo)N?2)y=t1>F3K;%Z{vU3#Mp-|z7&ao4^nK4FOE#ybs4{g5cKZwKIkUJIB+Kh?!3-rpP%kwtvaE4Pb!#<H|&5F{}lfLa*rE^p$eAsiut%nRqR*5{@6=^7BJ~A0ro$bo-ATH<~>$wi?B*UJb*M#YMY0O9Hzp<|VvaSC756uu7TD=Abwzk#ErJe}V9B#hOLvKclcQuW>2;D_?%XfGsg0nPo`^|Ue-9ykd@>N9Ypv0msjP!7A<8_$17n=rFIUqSt5%Qw6uFEMDfS?OLXlhAGxk+Gzy<V7+(0jluOLH*-2GtGEdHp#*hT6L4=69p&Co>61ylf}?%YwnyQ>AoiJWU3ZxXNJMiPF@wwyM>My5_JXEESlZ>Zno=F^SIfm%Is+{Jk11JyTb711}0`o0D8XU4m1R*^n!qhC<+m*1`mbi|X9O?OD_^f}s$%;f4={A5C9s16eU9s&z2jyQGk<Vcb{Rm-Q+n=4vz))=>`ChODut;@%W6ps^n$-!h}z4`iEwiFAWZol2+E2HtH0pCTa7Mth`XLQn&#R4TEOn03ta86&6N-vi*J{KK+&ES20tz?48<6|;v}bU9q`A=H3`xLc=lJrXd8TzxbQ70Qn?5TestD34{ckfA+?gB+s!;W^mH(AD(QV4}AgZof|H`u+Fo<ERYWmuc*`>GZ1BGgpd5lg>9|m00F*8iOkQEbT;u^;@4^9q`?>$2ysFHhhxV0%clZbHibnDiE&QAqnsjCI5BT8)=yOkIOLE@R?|>j~e?1Rp)+k#K@@nQO~f{5ioe97Ad5ey~V<AnWV`!q4DyB1}~(Hf_GAv3cEbVeQYXf7)@>`P!0(}4h9B0%{6KIZH%gPD1oY?1qYXk3MEkd_MyWV73Bo(BTixCkd<Q746dVlk*m_tWs+DM5j1~6#tEE{A%~39Rsr_;%4r#DiTE{vcCiZZ9lw{yQB|>KS3wMuv4{rdos@1iJBl~4#iLX3K4yL`r~~IAj&GRq8#9*@9*3duHfK_q3r|Y8q#|%;mMBU~+^2Q`6yDVw&$ujUFo$O?&l?JPC&u6kRx~~-oS-AA>8@q1tr2YfdO@r+YQ$3!;VaP#1l=*IvG#rz=!}rbwdr$%rvcVo1#H|Lxjj3DtdxFsZd@prbWvjxba78Ta8foTvXGjxwMZd%C8L*xI_YX!J?ueQ%<QPK4NuVUkz0?5%f}8Bn@gZ+b^No>W$L_GHqbh#34>~d01rgFDP|*y8n<p?mhi_!8G2N>25#@c#rO(=tbI}*EsNJ+HPHGYzotI1TPkh}-30&u0iS>O1y-(6upE0M&$>8r=+@9q;Aw>&f5?qu0)a9~O5~F_Iv^M&7<^cyD|Qrd6gJK>k>)O;BLnuC=`jahd2I+j_liAK)ipD{alpYLi!V=R(CvdoKsf{VBtvRSzky9f$!0*f;qo&0pDnF^>+lT!jvAZJQ|`VYtOU^KN^qw=>=dl@tXofboySUZtU89*LaoDHG94@RrrWk4D@-bTxdP%|P8@GqE_K&ZP|dBOG`x->c_%GR!m9jq1~}ZFJpt3J7up_{P<C0S2(g-D1}3>x6!uUoUCP6)tCGLTux#!`7ot_vRK!lF0l>1I^^(4+-tNngxr3k$uir8RDRxvDW|<~h7J5}!`Nd14VR1RB`5jn|;)Ros=p^?alT#?+VMf=bpIr<LU)Qd3g~)1qi~D`v$?J8uok*COQHW0J{=~_i)k->pQ>}(GUU>W(p+o1;n>&87j-?5V*zY4dM8!NDxOqCoYMoH4m!&X4SwiP=8@>*TV(VB4LeUYjqAAj4h38+rarL@3n*LZ5`LPh%;ALT82106B1sf{S7OHd?`LJJ>=-1cJyNhCknUeL#A_OK1I0FJzqKn#C$UU)_#D-mraK_42VhxV*GV6USg1F3j%1jq4%zDQD(q;_zn>q|UZxB>CnoM2Km2DAtBcAO;WczL|`u1>Dr>ma91xw=L)IrE*rqkq@DO`fd$5eJBkLybG(MJ&{`1tghK?gcPo=@*cS1UzB4-P21%WCWEQ|MJ7AV3-^!H$(Gvg5suQFwQmVh;6pD0&?rEbH*b#4E7<WgDYc)l{hBX}Ud3$xDWZo;&--ESW$JjZoYPMWJmSHH8wNG_#*0-<eMA0B)6N`%No5PqKaP6J95<gngf;=mnHq5muxbY}Wfo+lwv<<d+cRf5ZTwhf~UDqmZ1carYvoQSe4&91&f-X~L8juoB(25@G$XpVkSl1nP&-04RP++OC$}D=WNHBuMN|{vPj-wkXOaDUF_f%w^lMvntCgurfWRFl}rH)$a(!Tg3L{B4g$KLUmPlhRhu0iee@{NLd5+nE5qpEt~MNjd@bXO!a3;!WX!$<+s4Ooz)uWgyXMk0Mao#{fEXvcS@2oia?c|ShC+rWi0fdYDA0>)J4PSKuJ#NurPLw-V>X5Sg<%x=Hd@>Ii>5+wW|H*y0C>N9Lg`dc!i7{b)77pOOF;)_X497;0j<qeWlqml_Zw)qjMKcevlJ^YKsnDr$E34-6+N?ogp0r(gV+cFjEbmC&j9$z4ES3%&Zc<z{f6uS2GH5x}V?eS`AQzf>k_-W(3@zn7~q1{J0{NsES^hoRxD8fSV*EPLFR=r^;WdNQubTTZYhRrgmuF=F-YJXmkvLOJ2O6JEZ5GxG#9>vi*m;RrD&b?he}^R_^HnISIY0=y{5q845q;js3pFL#44Zn~gHL_(I@yvH9Dx5Vb;prcvXfKrG)3bZU6|j?{^a{UnS3Q250*MhhUE@~sfWkegu}bo5>oVY#R{<9tgHw`rYUjVt{oOY9jvTx8z;!<*_)%N2cE?+>lZI1Va7o;plo-`f)4X3t9FAZ_h7^r@+==%i`PxB%Bb12Grs0>lG~Z{Dw#<F}9S(Zn^d#t3EHFKGA7>cTxPH}$gE`j)0MMAn;BFRVyOjiS5`qAHGaA|(-k0-B;xl&IE1+M?tugy93le(+8KuT2hXOM~AI_R`fzQbSGo)oFaYDYpX!&Tk;jM4DuRa^Ll#l1}w{g|GAOb<7RA#_ylpBl$)A#o-reyHm=MJ<e%=qL#%xSj#eQ^9>8mp#SjQudly2{)YYH{=@K3rF&`mGesNw_Pw{cP70?nqx}%5!o!=VY%5F*diK&>z*lLvDK3fj+Nzd^E{v$8n^x_oskx|GF_r>i>wdSp`xm^%v|Q4c@PT@>u=|7xrIGg!jf!?6Ni8Oc4>8X7&!xBgfGh6(`P&<IojG-Er;rC%Ljk7cwz3cnCDy=;<}M+Do|NMq`}y^!PoH1S4<DLH&4;3f>yNKLllv=hSIr%`E`R0?r*53Ag_|ID<#)h&zlGH<7xCP3Lrd`Xps$ot*2Lm(ByF05Sx-L0|0eflkik;>l(>;;=@FJI!%}|?r|@D@xE=r4>z-?2c3*PqSz3q0{%}}7V7~gFefg)rPa&@SK1uy%-N(_`UtmXwcq(|3|0p+4YPIKj)hxSY<Y!WP?hlgVi*e6iR8ROV==k#I+pmAQ>4V7md6HUh3)}QVQtrKt9!vpqR#n8Cey*!4&(NR@*3=A_xbS3`!5cjR@-S7aOX&41jDqQfJDUFEr=P#Oi{*d%`G=oAy_xRoEkxY6T^Jfw^fl)!v4G=lMPCP+kP{DP68iFg`Td6<zx&&lGynN_6CgbXXRZzVYnzP}N8K7*uik8rJIelP+$D!=X1hWH%@Ar7ZeH2f&56=}_ix!nD!wD%3x#sO9Uv2dBiY#9yB46O<_7;dss&cZ9{wmbH8I>~N5|db!;?)#cbY;P-L5VGnZ?9!WQZo4;~VMN%bE+3?mrP`=E9%rNXGcMAoC(}{!kObc6|bWSGLx1(p6?EiW=lZ;x-)G6Zn}P(E53cN?R9m?cB-1y=(5z@o#^<UVnKk#&pSfWqSHQOBWE_rKwSw%0h#gTpQJ<$R3k6D8NCp$$VGc0(^2;*P$e8<ZEH++TN(m)Yk#Wd*&B%G}8Q9^haW$O3#&hq1W0poOD+2hv5B8#^P{F(gxjl(+Dds2^$!#BXCa*yb!mu)kfZh_g2`H-r;+_*PPxLJhT~&!(7(9@<dBB={<S9lVR@<G-j1Qe)QSaLF&EfdCye0VxsU;JZ^YXsve6ftM+)&o(_6Jf#Bh8i#RtGi^z7;Svyy%4y<NdvzoP3Ht_kKT%c>a1l_lib!L;J(ac8nHBKy3TIHu8(Etn`-dW}-0_ZoiG5_>{?H=`oi;@7~b77C3O!w4gp41=|NaS5(g<wV@Sw}Ee1ehQa;z6B{E~6)EUg}qcal|Ov?Qc>c&nxL3TCS5UMj17KZ3>ayy5<^;BJM4ZfnWP=h1v|BZ&$iTa<Ewh&4Low?;Oiu9ZdzS;f3Gq!903dVJx7Dk={1$Yh?Dc+lDnj$Nes=z{5}T<AHK&0G>JBkHFwxIMPOei7mQXa!F@Kxu;HypyJt~^FQU0OI8EL#^cpI`(`t%gF|nJRTn-w((h*tmdWGF<|Y)al^RUw9Xm61%*=@W=drz9)VzS>Oi`K;{YMlLnl*1P(F3I_&cP~M>yOj!x4P}N7g_zCa;Xfq75cPd3g&JAorog4A$*ORqaY8OS?m5pk4;|Yn5K=dBN`%DhnE*4{LI=aaJMQ9HBu4KLq1Rt0;$6H(K@m&?M2sR=b|)z*UmDt#7Z9c`ptP5K<_C+BPP)n7x{#9B!sZwfyz9F*xQhPkMK@>DGOmDuVF#=VG~g|#6)9RXJb%d<gle{QvjadHjxevm%G%l3-CLDm$MG4I|B_^oWc#n19Fg;7&#{N+a^ktv(ML8&@an6nv1^ogS^ZH_fU$f96+IM#zbd?=M|i`O_)f5@q78r9@E?vsk=-*D^6=G?5sA{QnfBGiXvI~rbW{l#cq2u3kg*)ZkAvM!9UHB#98sSjb5ctKtt|`z!^YcX17?$wyDcld%ipgO40)-uWZ}OUH~cn1KkF$za`ol`K#Im!=uWPsI5`yxqCJ4z%+Z=G+7g&8a)KR@lYFTi=GzKqZk)!yR{B*)LWr&(L^c^>d8^hEUiArn4`lNXj?%${6_TRDR8QFBXpA+ZJ{7a+QReruqrCzvQ-koTTUnJp&Y#mtQ8xHri#3iHSR)L6uh5d^$|F6)X>S8g3GiEwOW|MF6|m)SIkS_ww)k{!B!%C*Xg3==;Uo7_el<t8(szn3js`EHIpnSXEwcT0P;CX8m(^@VIM|DT-B%&UZe#^GwOo<7Bz@gQ3$cQFu^*=Ngt$Zo*-pR>*|$p7BTbtV0Cm(s5;z#!f<9ukAG+#YWUnd(iVE=Jr%t7m%mpnofpRUO<K=gN~GMhcJFvhZJzj^8`KGS0W0NgBk#^o_SLWADnejsz1(i@%+OFzWYPl@j5DR(6ZFuaUaQb<gh}YF!yOYkJT%owqy_?|urja!qny-yUDVKsxznK84t*EFIOqI0K~jSHTGm|v8<6m}`$c~60?8;YJRRUlYf<|MHUhJ8wx55WMNv>}|0;aI!DrJxZ|E1$_uOu=om`Z>{<*f_CfEpFu*^VsOEvTx1T>3s^ulxqd#Z_$jG>hQdj#t8%_hzP>$oLMc|0-WJjpPu1UTCZ*DQuv*OQBZL&Bl2>4fSE>>hs1RtckH6IOB+YaNB|TXZxG34rc>sNcT6{(`Ad`0Se+ipP4O;=Q0~3$pT^TY1d0OHrcKEz3n>l-5KU5p^A?fRd78axiA@<H@Hhi31HY;mv-%e8GDGN=ty&LIF%gHAT?`Gelcwsxr6Iy!X2*IN!vgj;g_9NOc$dS&cHi6670z@u99lk2z9=^tf2^1S0w+Ag>Vi06XV+;ccePBaMY33}Jah8d(9Q$Cx_Yj$OX)qwb4jt+863F>eOZC-@!6TSQsmybL)U<3JeuZRDNlYWOe;P(Yn$z-Lj_-@ACxI;Am@^N6Ziy)r)y%tDk}>&<%ku2BXIINAbq%J+`1Hot^y%;pr1vrKoeFOrR1Xk*?}1HK=IMK0JuY@CQ59He=Q->XsUWwq_QI-+11LRFDOraDnSL1b%54ROjMr{+vi{HYV=qq8X!omzPY@)?gTn0F63AyUvzoo;CW)6N~7&}hSERk8ah94<WtkYF?1Seqwjoiyo$b<~62s3Ce%9T3lp>6NN+6{eU*nK{ZEZh+C*#>8sZF?sY;Rfk$3a*BpbewFUUI__ClMmLvMB4}d8`@DCr3{VK?d(j0Gz@5f8opRXDWF44+6-q7Ka}J5VR4kFcKgdEAdgiQGvDjf!6b_6mI^4bll!`*ktz6)jt(S@(50y(JPo>klNrlWnJY-@#Hqi%cN2hB+E3(jH?oF%IKWXQo!sfxa*^3sP`C_BM;wG9!vc=VE##EHh9j)FSQfm`g_2Y@wknKGG*$k$6N$P_S5i2Fo6mfn~YcFts;kM-Ta;YMjXM`!EX0mSs=`MY+mLUNfG#*vYiKF3=y6(G6ger!i4Q!|i3pdI0oqBG&%P2=?fRbp3K}2sABbf5VV&IePNI{mw3;VjF%Dbi(z<w+nZjG*TcUkJhGT5~&{|c=TD4@6Z;WoUJ=@8`=4wu*T+<Uxhx|)0ZB)2o4HdqH6U6l5grY)b4%brjf?izswVPkF({8B|umpcarG*(v3h_Vu>{7)140b{Mwgw;_!y7QqBV%N-SaippUL<D+bM6PQVwLp?q_rYG2f&!-csJ4PrB??#bcpS3@#KKE?HcdsPijD`eU^biXxpz(4hTcX)X9mnp5v>_@a+_V-$*H!WrVFGFwYtwZS>{%Fz4*)AS68MJN1P=*6D4{uBqG*6<nbpNC=0}Gd@@?iey#I~G@sD>D;-Ys9=V=3I1E$JodE1VZ&<@lKv*8w6&1~4&jPt^lXZUN7P7)BMlT|1-%?w24FXnoRg3av&HS!RFU>1mRSK8!5h<#ci6t^QO!hikz)@Ja_8Im_4+T>QvL{FArn?2FT_<ZQB?K&d-E18dlH7()mxN+>w<H|JmUkV^P@$)lgl1h-01Riuk^DYF@Bf}KY}bWB6zrbslKh6O+U}5%Oj=mCLWlGS^uM|;YRCb!l<7-KiFH9yU_`$14q6p}jt~pzFJl<>xGr7skEWw%<a#+%>n}1)lM3Q!Ted4~ojXcM9i2?0g7acGAi4)G(ac^(eJOyrE|&H-`UP{Ki7A9%ESJQWpxpk}I`S?;naQ&4h6Q50L=9&`bNVogZkt6f1NIPIQ#U5=(F1H_kZc2896~3n0K)PF(6I;Fhgp~k)gguvP^lfKu%YV{U?s&;!6lZt`ZRrXXQgFC6M#M$u@yfx#>k`VAeWToMhz&_nrGD0Kb-&JQfau*Bcm8Qu%plsaamtoT$D}P<FIB3i74B}JFP_wZ61iH0iWLMH5W@4h0l@cCUP1u`t#XFLbiG6D~;DzLw*VL%H7Z#j4q-R;LDTrdD4qL0Zu6&tWouQNsS)0X40bCJc9~YF-&s4pLJ}aMYTR$2{t~|v5FqZ3RP<A5ICH%Zdhc_82CtNwbjbnc64PyZkBRz{r>w^B>IV1#n`A3uMr>%h*j6H?KlbkJWygv)n*<cpmoBn?lc1Gn^BYVL-ir|&DsS!IzVH0s#zx3KU)QTI4B06;HqKkDEo?00u>$0zGBj{*2e=Q8^Y(};XwqWi)dM)W8vl^z_`bZSlI3z*v}^6^RT><w9b?4?*e}z=o=@?Z;4s_)urSz5?xVg3%9^qZ>b2&8aWa2B?4Z~@E5(X>87w%a#jzeF}#?^+S7EY$U7FhaaD~4iux!dopr2DqQXaO8)Z#D1hrJu{E!pajAd$LoNd3h-~I5te-|qTE^@b7BrtVykp?=1`{|I%hI*?f6i6vcSQNDeW>q5yDYQqI@T6&oX;AQFf)4@C!2OHwetrFgO651bzQ`}7s?e~l`>2;yq0=lJgP;?Jd(nh)$<$v5tpF<>86Q3agPxPdQDezGEu=IfSO>f4ExWG1$fl^4=-ZL{$j^EUG_6e29y*JvlWey<?glay_qD&XGY`yhL;gzCXGbe{A&z7*Tsq-azf{!vp&EInh~|=0mFwoN2BA@yOc-;FtN-koo;iEe$7b56VKW6tQ<Rr7<S3L#7PYN8Zjo#e*IcS$o4etRvS{rig&!0w66Ot8tbG4NzKE+7vCo<8WteWpfiNQq3jV`<s>fTb+a2Aw08<gxbxBl^iXK*?vs&FsFBi3Cb0Rp6a;`Sa2JWEir!7rlotfR*tI680>+)TrV0%eCq}Jmi*kQ_JxOpslFyKxvZ{fa{&KTes`7rx-wq9fDW#RY)t@sErVAOW!zQTZ0O60AR81jvyA&;EaF>o0$$qOxrvCLgt#?bBVUFU-&R=uaeV##`0T50W}2OiBm5`L6~a%gvk3>PJJ=gmQpLpX$>3x;35?jI$t2yna^wq)J11eFjsG9s-?ju!63q>cV^NtHz~s!oAT&F)n}a8d#(P!i}1K~DQiBclckxn&|~l`T7KBk}iX_qGf7xJ|iz+7SwlGlHU`#(6Sce>nh`+YPsVmp{_`t8!WH>(T`$l9x7EP4K;XTN~hCwB}FoP!69atwOP6-Wsoq)2HqNf~IZxl86jvW&WwEl?uA0=l|j_@wzm6(GaOGM}mrx_&5<d(TcI2wE|<L5ic{0@bw^5l|Yk0siyAHK=|29GpS1hb^Uj+&yv=xPg(<~Cq>is)Z>?aah7#mpgEy@{{aYOf2k^rVxS|%+}>a2yg*Gt;C~O?ZjW2js9aGA&rmD%v~E!A5L>nK34A(aaIv3rD<r_cx@wIP*1tX|7molKGVJoWO`8$Kay^LXMEV3%3WpHcgT<ce1THAFz(KEQsbNSjmiHa+N$iw$+xE-}*pZR)K<!#c@=(=w-S$#(Azm+u^|0en&7BOf^}cQD>@IR+J@7#1QiiOnzU_4F9f@<r``^JsM6JPvqWU((M_DNw6p0Ao&`3oBEbtP7g<lUh8nq%q7!)#yB3bCh*<g-B8$>U3unsj51(7jMBItXc$CtnH>#KFaKfnI;>GP}Pj~0EBj^BOrj>?~W_kfql0Q$?)2YxYjey5o_zl9u1QVE#WmfQ(q(Z=3?koBtHvKj(X(4CZ@+=U?@;qG_m1SkU<L6D>J0|FWLYR~cw`a*IA;D1c$j2wTpYpM?3Hg}^M0&I@BdXEbq7IX+bXK1?~`&tyTEvMy#NLTBu`eejk?K`2zCzWs(dJfVhmjolhxaXSMr+~XbbO`KoNFnTXkV{^n3sGP6+W4b46y#+6?gf1zu|jma@Zu87y%Ci@qBsY}*nHHntFY(D#%f9wc#%%u>#e)sX@mQPA2ctNVcDx3owDyc^{mkMN7e(-l^p~SqtI%R1Q#K{AmXghE^<My0<!kQbM+ai#xtuAgOMgtK2boheoScWX7r-Cd~`@10Cxj0tVul;@UCZthxF3T=H4k^s<q+O=I0ffG34NI<_(oXif-v#%ZGK~%X1$eM&o3yjQA|w3v0N@3K;eUuT1K>kBD0}rruwL;*1pGgioTT%IgcZW(!05LWqXMJU+Koe(D7F0;rncXgEZo3e}qMpa6*scZA^7+bETyCfbW)sCGpfd7Wv0x;cW<{hiugs*OlNjVe`fEI7qwMe;39B-zw=yeg%Fx#b^*@gEwRD%Eikf+Z?G#nRTIo`+mZDu|mH`Ilm$*L9gs>6$?K4wk?+LMW^RT@T*Y$t*RKv0#?g!UbHPZu~r6DwIp&RGSb<hbdiu%uS`HNrHvVng?VH+mB_E>m1rVyFM{$zgB<|g_F_x*wyGhq=Yeo%GL@Uwfo@voZ<t?cX6h5vP#v_wFIX?@6n0a8G0Q#JplqPqDc8TLZudyg>AC~`@Uu+WVUNNA?hQOD?~+0W9lx-#=N?XWO7Ez=SJZ{q?=T&7?M50x>$i;Iu^q?GJfD3+$qx#`!Sq*%9ftYlyquRA!M_rsi{@804_vS)Cm~j3JEUMT<@nuA!U#<;`mEM<QA^bsndl|bW?|Dp_9sygv6OWZL8krY=`>~dW8w$UB)oRHg^5RCC!Oc-4u;Q%kIZQ$OlyX`7O{HcTACVQ;d2_YM_we+GVc9^NTtR*`F^|e%8wxa(ci#+g#Vl`u02u<7e}JrbVq{DA+_V!E8tTql#XwwW9g*40xycD0pX%Q0YLEb<E&9{$HprJunhK$2x<P>b3pc%9WU&6GmI^=9=$@%d!r-J0&`09WyT}LOV^yt%Liy*9Yp0K{$d_vL2K7xPb8v!C~=XjRZ(SI4A+#nKYlVI?AvNw~+m@=^d_f4`^<15je*3j7A@QA@>udbhtDemR6J6euN|=U}ke70CQFtfWq9_Oyx`61G1z#u`yu5KT4wJd3ia7$6`AJg*K2T6cwQhysnCNW8r&bH(`n3XL3u~00AD1kf9|*&_1}eM2Y}`PPL^WMCC>@M&@Zps&~_pDe6yCk%F2I^1Ou2%bL-EF8A%q)#7{bD5CycUEwO!5BQpYMSw4PpVm-!qs8K;(FN#Z%HYV4vKlvQVS9_@n{E}|37tnSl>1TSq}XCbj4=QOc+Xm)?*m8&e&ZyXN`VDiE^Nes8P>lI!$!Pwc)x^?xtNV{%u4F31sW_#ui$VAJCo5?nl-%k3b4aF(L*Q!1T3CQ7Tx>?+G6){=bbw|2feCBH?JY~P$>VPax-*L`si)c^EoQXM|voWL9TO*`e8?-+W$L4vxG0?=g>-T9H?YNp}vzwwhm=rmS{6R7wH-bJs9RsO7%-==*ELVhC*#bW*@TFhyi$?(WS%>_;6XO1t^?n>r4{__ooE*{m{syR@Q$7I^!8g-_<o>a~S9&J~Wlg){ND7-kDo&qZ7f27}EZty>DbKyH#x8$or@24*SsL&?#0TA#IA2yu!EGCWZ!{pIVvycH5vi(>5#W)`B($2yT#GyvjiXVc}2+bJ!b$G>A&+7c+u?UHyyI5#YkCL)%s=ZgTpGTrqb4*4-|zl|8qHHmca>6fzJpZet3w47ae5N1nu3jci-14DUm7csQo%x;w3`KIc}wpdX0bW~n2E0k=$1*tqS&e9rr|!ORDwcZYV7>C@;X5b65W*<0^MTG?F{8QY-{m0=0(UC@VU`Ly1ZCQb#PziZ^1h%kHYR(KsXXsXt)?Hsz?<xd@?R78G4OkZxRH*{T2SR&{_4_J}a4SLrB_BsZaXeSpgIb&&hL(L?|QF4YPELk;4UVm!a{89Dcn0la6MjE}grQLwVt<PrHXu4fvsS8zM9<KbXi$a_=Y9hU(MV|YMW7#IKBy61mMKZI%?{%R1jiFo$tG~CP)5$Jqf_|kRMkZBNxJG({%}6p9tU}1SG5a>rE|Q-_DhNXK2LvJR`<izNn+Ijt`*0j%5&ZEt_q|#Sz2ViN{s}FUXQhO<Yg&E4V;v7knG@WGuc9I^3ZLxj9WMODafL$jgvmQRn7nJa4GbhCs>DQ!==$llkw=0jsOa5~qg9y?!fOxPTn(X!$&GY#l%;>bc_~xF@^h6FFS(JLf36$FAhz%vhlT%53-Gr084jWTDa?F!DP;qWo5p$16zkeUP3|*p&Z#$?NZu;ba(C=rl{F0Q6O*396VM*K&Q*G%;8G2-9=|*5tj-|DbcTp0&O~PdG>eAi(r*Y&-_~hF^;xK3&)*5T-DG;e+Z8;Fr)BT`=!<1@-Et}Wt_@QK-e*z@JnyN4`?)7>nAN<q(}6}My$}u}j-TJwMX(c^>>HN4+%u0XBcU|2x4?Nx>cVdm8ZS@ixj|UG=o(W>3t}y`VQeZ&ZA_LcD6!Xjw6UAW;~gE|WxcWFFt)O2CsM7-cctL1A=K`!N8rqR>BmmhCX9MQ?13E|pHpz3VcB$d`e$eqvakufh@7sg*9Z@V$Vr$$&>)Tg6pS9B1f1rwGRNrYXJGODx`?4a7JR`>T}E7lUkgXa;eE{fR!|4dBQ4(w<#%W<E7K1{;R@Ii?K&V0fD__ioP`Doi1=!>uH58Lt`bYkT5M-xy2w=)Riq11PgrffDMYh{Qi^{DBHSl>T!Nmg1W?@1Lb<_qlWWtb1WzLX8=0@*5=ZSxDKu2{lM++{kR}vN&xwjxzpwP*Dew%1iVEkuR|$3o$v&|HgFPRMfNSlHZ8*_VGc8UkE?*=l;msuwBWKzimycpHm1-=GlmtYCDT*U0jJB?Ph49BBq-@ONVqQ2fm7VAxGz3SqLTIpwZbBDaVpz=-Is=rZWTo>wjRhX2sxa7=?VoiG($JY<!g<fE&M>+z&=4s2nd}iyb8iH_r2XR8$%G|hfu{jAYoY1X^d}nTE>Uq0Ha@x1ET)h-;eKE=_loIM72GiiV8ByC4sUKMgKju1LdtEBSJ7Tmkr+oO7xyukNBQ0gf?d7i%dyMrl3)(3TNf0N%#&iAHc*rrNE82^S%;T$pJ(0rWK4(LVU(-FYkAfIFHu4|YJ`SoVGD}F47+suGDBG|b+;J2Nj0(nLatnZ!kx#x#ppJXCSgTo3T6Fc&Jp+Q$40FxXuWrr*_>Lnx;=aYwN^Alrg*nR?gPJcDQ~K>zV#+Uy-fNBjK0?`$bE8SpkXHkY*<>d%~Qy>5Mv4MCus2Nw@fJ+u!ft$$%?Udb#9{|gWx3qp^t^8q$y4nFQe*hEtA|cKu+U?=U-GKtf^&f8US#;_?hq{oN`~4Sr#Hey?=yOf2rDep(&kJrJlD?c!@Mu85c`qYz1_}#P(T*@X1HL#tV<~m7<~-RIYxC*0o7ttV3*c#w-G&SbrIgerat$P3N4{lzqIb-R9rw)lgK5Ly{B=IC9AzJ7b{%LkG{o7ScfC8Qib?aC=?zO80DtEK%GZ)hTUsAh7W=WcqqgGpU5acuO9+Xo~vMW1(wfUVV5u%ke%hopE`WU^gcD8MN75CQeL?rD%$M9oVe*SqS1=))hi;L?S|@jEJ|{$o(*ffjtqS+4+xQ4;4iq0kJ5y&rqY{vAO8G#ys3i4+<7k!%#ZPzp?o>Ibso4A@ciJ!QjAa3c=>nIOM!BnrH+CfRW~pVO0yP0F3owyrW)3YrMIBn|W8Og~LuJP-5hQIbq{ewt2dMd!W`!Iheq!a}AkmWv#;&JcFBmcErx%7JLd&v~_S};yv2_vPE2~%7IQPENp1NB|7m_@@nH)!R`=X{uL+Y(%*@s$k;5y{-AUM2b{9ZsN6K|1{b&!H1Wn}3A^7+(R*u8Koxgdr_0&X)P{ZneJ#LI4^qvpB(Z#{w#{jWG~%%Zk4eTU((xEq<_D}r=jn`(ZCEt#=k>y?f<vaPO|SF{6^K*Y)sn{pg)6a}c(&i(I_f9NzK&1fhK=o@rjs~^p!b_j^_H6%XnYnKGcAwSB^fJ(zkr`b`%&<=8x<&Gw~c<%1!ArOnN@5QQhKZUc;}$Rh`!jh^dG8zTS6vk(dSr5#u1@_ARowtGU$NCel6RJP$<61LIFI7gbd$jjwE}ujD`Fg@D4>;E`W4po{St9VeDGf&U4+bLQ@a5m0fHmoZH=uqDng2O-0KxfKduS3^1R*Qk9QMno*dH&0SWMe?*AuGzPuNyx8S{7v2ygM7NW%O8ZNPvGjO1U}H(SpMA9hJNY>QI+1%o4U-mWYQC%2WqEtIy9D;Hxk)1YmZCvNSaGOEM@PUI=~3Oi&!&o7EsvodUG${o&JP#R@I{T~iy<jWr!djts!}D25AHfA&MVaE7}<b9PLNM|#I%~$yB{bKDeMQ|1T@4kl(eH4kM+UmMxw?@dI97@m@5fkyXYB}b?G^jdM5ux<~dXzFm_7xPG(Mx>-D$KDTdkZO;Y+K?WRA5h_Vp?q+*eZrYj>qTfejqll&S+^*B+q`L?f)n(_vAOB}tV1*RcFAI`S~&Qa_9s=(qKJ=AG73ow-^Qmdm*2tpVmzaHF$Jk(&k)skWnH}SB%&UqX8s8=XTv;yd&yDk?s+xHPpO=X!l&4tHR{r-84k);cIoR8nU-~X5UVVt<s-k9mI(0x!@@;HU8zS}k5E@4!=D&$1(U&5=fMSIfPe&MaVAWK)HSPz>|tWM(FjkK8yFvCE~ENofW*y%CjG*{(1?_Njrpey|T$z@wZq8f1cMXwVj>F5imdZ>S1=5n^n*8gNGC}q5Vt1675>rN_pmz8KUHJ5xZO*=Nmu(`Knynn&vu)twDjC>Hv3|5x)I>kcB<$V}YZBisp#<(mHaU*KD+Zh_1%j7VB+h)3f{Bqw1nL=J!4S5%!?U~wt223Q*=(d!{^ZEJpr%#_>%@6Ni!DT+=)vrIk{){g*<;7n4D2uxh_m_NXGF?n0Df<d(&IDRiu@}X+h0Q3}_!+xFF7y3%q=@nMZgXA4@=YrjC)x|8b*Ho7cz6D>w;?3@*-pPqp2A!8hj{+>=X`0a|Jj#(f~2<n-=&gGk=>#{Xk0wAFLr~9FPQVH?8%>SNu_pWPHSg*D^=GOo8ihWSjUe0FvcDE^7p&1f4b>|hfpiCI~}z){ajZ_O{g8Q{8KYDs-|czvjZ;0$BEoR=5JqbnL-*2e67x9GlWG8hmXasH0m96jA?6zdz8UwhA<re%kMw@_}$;WeDdetosJ#w;Mrf>uDODvBXX#kp;vE#$5FSRi2LA3y3^*Ixs~qC5UTxcZ}GbQT7z4=rp0%_nTndJG95LNA=y0w7(`h=eu2e@hu@~Q79DxYaSPZ>tctQYCWS`0T}A*hi5ZoMUt(ZN-|WVOkVhnwPc(`-Ph=g+7@q)SNJRY}$^)1mM}ODa<v7)>luWDkig%ikcLi=!f&!<W_%Z7I>!Qk&kdhKBg5EJ@!)5;T^AA6L`f<G;@76uFYSxIgdvP_{NE2GSk5j}9aGoAQJ&t~ZrSt&pwV8UkgK*BBO5DU~PWGbnd?^axHPaw-!1;inA5%Vy`m*cP^gS=+;0-(+n9@zmJAmt`79C-O0{hnz$u>iCRPLHm9aU48f}3Yij_9_}zW3XD%_0Aq+SL1<23{`84^Z=^o2kuuZc%MfUJxsuvXqf8Od6>c&Vj;K0R}k9nnaxOf|yJZ<)xXI{Pfwk_{HRJL!oy_)b2GG%y>VVWS3o_jDDf|Row8XS=tQLV%N3*AjUwm2vvWj&(%f3rCjaFOJ=5ZMa;Eum{>21jBsgarkRq^z-|h;z#}+2;zk$dhq#PU^$1<6szGu(vIm{<sDJzG_4>=>30a~tK&u;4nMYGA>)dM%OnjX~<Z(r)JlHL@Sr?^Fufx-u*)z4Vpw*xMcw|;G)Zd5t8pxx@UM_mnDew7q&A7Sk<)WH1b;)AcW%~NCUM_qG+Dk2ak8ouu7>^+z&zRdwo2SY!omGbE6m}vMUiiz}$(@;4c^<15MnQ}d61A6*?*JAE*lBntvqGx--@88v1Tpnjc8I1zZ&$4Z4;(GuLPHjOxLEd*3*_*qnoMRfLsSx6mX_xTu_XZ}-S>8Uvk7X$v)llXzMxe%Y~huF(JirRm<ifD9N5rCU$<+htEFbR+K`7R7C};tZogj9u42>Z;y5IUPPMxb*Y#n2F+a847BAF&iMnUeRwLl2oFl{l+jXd&nv?S|_*7RgC>q6n8H_kV(6jfEp(LCBSk_crigS3HhRq-%+{rRRz=-`XT#ah5eB<-7KJ9bihPIjVB~5B!5)*2*5Qcpy%cxajU$pH7#`R%eaY0nh=5NG~UMHv;+w;)M`7h7M^L>^3Ss*WK?XdMC+QZ#S^E5isC#P=Hwuu5S3rIydJU?DPwa_o#aarfI=%puCSMXsv45$eEm$n&68|I4x@1_)703Y6|YKsU3u#4huu-4Wk4Xhr){I*LFJt**)@V-4)yBpQS0!`mo5+O;vC=Ov422&A|_E1kn%=Yr~6vXV-fz6_#F$nZSQLw$QRs50CR|i|UoJ+-IT6)+|?;DkoLcY*M#n7FLW%cfN>i4g&zg@%1=k3u8#WB)~bBcoApfhfrK-7C<HmADp{vPuJcR?iN+V(?6Ej!&nCnc#`j2{ek%<!utl^ySA@onY7L|~LM#KT2s(7)PIurggcwgLP2YXQQDhiQK*m;?F+`bS`5R-$mNf3Ee)<%aNV4vpaBn4$YEpkAV1U<cMYCBh0c+XFu26XDMF_<nbX+@_lv{Ml^qwmxiPBdD)mXFAH6@t~O92YO+4%S?z9;i>tJ7a7&E-aT*___VCYZBF^R>tQD|-_0HymAhkkgRmgq--&>gT6`gre%g?>4(#O&^o0=;EK=Ey0Uso|Bph~VR|A5LgUqC3T^{66Zzr#jZh`h?$G&sj(-0x^xgy)OJL+I16=aZlEDPYGls{uMq;*<zK!>LJDgv!N9+$X%<+1SS<jl4Wn<CP~J$wb{){4~aA2*cW@cFpJ)W<6N(zbV#{yt`9kwdaUdCV&|tpFybDOD3iI&Zl<V>c7MxlaBnyu`@V!d|AL%2Y%$1MM^@ph^+y`I6cY>+FVf<q&2AzJc%i<T{<Vb6dxc3#-92p>!@G;QKBGyPe^Rxi;+NKtZh}@89H!)V0^99my2pp9YsM+bHLgrRUA`L5%3OpstJUxEO~rXuRpAFqW`QqJ3b5!zJE{a5G)A>&gbLJ{L0dR`PARlZ+^521DJ&1-JvzT}HD%nQN=NjB+1S8~w6p!0twDv0cF^V@yLExw1GNAbB1%+g)_8K<Bcs;nq|vcTIct0vw-v?{!Voal#jV#Yho&10i53`t!Udd7Z-~Uzx0nBS>dPHsin!U7;pprSQOYY(Z*-WJhHNS#)3>??U78E+ty0YroQ-H@Vugt{~*lYDyG++c*6l(%S1QHeQbUb!~#EK;mfHN`b+B)@0i@(NY8;adI$~=Q6DW94Z2I-nHYJYYnNIqTZqC#u_AY2a*?n;OD0sDyme~uWA|?ufrPU+b2q=pMMa$h^t6@D<Os=(UFBeueV&E*bB*|)7Poa$=;8I00AZmF4<5@Zso6ZVPBR9-UvH!ktPH-ouJ(2>#({SiGv66(eXSBE9etE>XdruzVA?1kQrFV9#|^N+P?u6g;Y|hE65A15gK7KMfbV@-`d-%pU$@WqdG7V=#@wW`O90R@wIL(`@P&Z)(aO`RLHSQJ@jW7mF{>M6oP(Kd0K}_ZX*{_0$~*{{w2?u8_Hgwk4bs*A}*9ks%#kppg4rWg)}VB5^1Qb_p0I0uAR!el9*s`^eo6}bjF|P<BUzZBH#MToEF2fkhZB*rrmJwb<*p`3PPk?`}!Wip<c~J4Id{r6^o?S>2+frF$p@9Y^WTh5x^gN`4pTB>sSEj<?1r^nA0hYWe6TRki|66DTDh_Xy$^Hg(6^He73glAS8~$nxvo?<myInY0_?-<rpf#C1t5+kG!QiL}j0!g91yZ_v7<?j-YQFn7NpF?WQg-{lRL^9Ubv8%4O{4E5vtGU)e?v0CrmOKcQX=fnUK637Fq{;oi*;tK7P3d#_9pW}(-#efPunz<ed1m3Ifvmx>O{0Hr$)2_X5*Jd+S!kxvKv4UOi}xb7pMsZ!;RvgVRq{6bWUf78SI?Qex1P}(89@7a>NQ{bCO8!RV^+laWBJs=AA08~`4YBIMm;R|@&v~q}UX)*;RdK*`{3_5BR<we7buFS(!5d-%GvMr(&sm~x4iewsu1D^T1Jp(Hiw@2=`q0gy<idD(3VXOH_Tz0EH-jPB3L{<9cfGv>>41rBpS1AvZV!w0jX+5&tSUs`+(x_@%8kLRl<LF<=^wu+bR<@m8=hi7O7&3&B7M{m7GRWJMvd3l+?hVjidYJ{pQ|>g5(J$<ri`5s*D{FYN8X^3_&5>mnMc9^e*~Ti@pOeFG!><&edb|Z(K~VGj^%pJ<naAc%d$Ro{Y779Yju|FoQ?LdzRC?LwI@rFs`=h}ldw1SV1iS)wjY#gs#V+p)2mY!j9Mw0iiVZV?1?MjGF{skB00R>c(S*}!la|z>j#7033wqj&V3g$yd3_?wxwCqdn3B;qQ(fm$no+fu41H!Hq~a*$v3VSRL|0&^Z-v;4+6o1oKoIF3AG--{Q@05b5!nMN#U!($#M2jwOpKFxlaz)zFA7=|k%ecDNgHa2GbtY6OnEQ24br7Lkad&`M665OhpvghX2#C0wPJ~eb{NzeH}zd8L!6O%IeaT5+}JK|zV6??$8}#&`_d|VAM96k5z+yK3ykm|6sZuigUZkOD!{NsXC)li7y4C_vIuL!Zr#VY2SOKPpzB~qdE+Q&)ZR?Ac8ig%*MThwY?6Z*uFL1;0A<oW!)N+Fge?QCFHE{pwUX1!_P)@03Tc|6JQeeHS>>2K>?kp*sp0v?`i#!&w=mbedF_2KXR#>$$a-NaB1<VAWgn6}Y3IXmc^zUM3s60jB1x;n2b7r<Lk~b#a-v*C((!%2)FeC2ImPFhDMedw+^(@BXjNd2QOg3clU0<~@n2oBCT!Q)(SwEkgE1rua6JDV#a1x!=c?(2?Oov1+F)v}Ozajj?+A=^(~36wMj3oTU9%rLnFO8_s`D{<rWZw%DPHUPZ7Mmw%N{q_+n$0GBNaZa=1T1SxPhGO%xX0egO0b+cWcUxm}F`{a2Nc~2<L_=SDfqg#SLkm99t0x+_(&>Cp_kLf^&k=V%-aYoy*$vx{K1&kf`8#+xyiH6cAk_{4|y?1|w_hN>dmgkWnqPcrE9#j-%XC*t;dGu6@GNVgBBjb6Y*=RZ{5*Hz1(#SY^U>4vUf|4;gvPiZTi%<i0tOGW#h)yMWMq=|<sa2Klp0Lx5#}_8&QKBk$u!lks-N2D>Pl@$lrCR<LLfVe?TB;hbp_gdT;Fr-qqA1uYV3)o-%*bA~D9+L{>T+sqDZ?Ojt08bz+ZLjwf?kPDUem2}bVGMGEHbBXtCgkCb$J#jPl;HX7VQk1}hI9-@!vV=-^fMZ=-0~4&2Jky|>T#r*y)gAr3<WaD!O93BehVj{DkJ?2m6{}Q;2aF5i6(>rI`+{ssS!qHS4s7>a_g%$Nw%54m(X0{au<n3MB~(BaSv9|3#)Mj(l#GeEwMlt4FyyE}nydOpM1-UmBRInX9dn&YC^dG6lPQf-?6l|;oHc4JIjUj7HGnHU$_P_Za;et52fOF14nhZG8{j3gj4Yb*YmbO?JUbZSOgCw`bZ1)(QL03uRG$AR*rlF=J431_zBi2xp4_Bx2>Hmowwg0A1*9s=N_~qICShKq?EH}G4pQeFrDi=KZMfv>KxhLre%^KUvCw-TE=x5J75nvipFvvTLIEt8(;f=0uf^J!NTNkKlQ(Q!Si<Ho@N2WwwNz~@V>O=V&2lm%XBt!Ix@~fOW&d$eVw=KWngsMZ(6J(e$CZ9*LAP-3V(+5KLAnf`+tp*D$k@06=x)6ive-~lh;Ue!fT5W)xjPJya)L4Nlyn(-ArbyQkG4_!Zk#N8WKjk-vg>aG_UB(?ZCk06z$*tLx|p50DW`IbkW6Ke6FaneZb$Q7$E35sM4kPEpE(6PG*<JLKtWh2HtruD9y_{DSUW}Sn~=Ua6kCh}5%^0I%i>UtH?;FP5_a*XeoW3{h&v*u67_zbg0{RB5%ry^`%)Gx|L{KNPM6W)5=w4;LDXzmWqmZ;`R%%d?r~ja^G1GMpzRHXY;Wd@37<Bq;2!=q2x!3YXEifJ=?Br`X)OyJ$&q!Wi`+)u2BWOP%ii>r9czYA7&o>1VR<7(CWD3c{mzgY9+XoRoiPop2uww4B9C8)ZP20qICL(<(-f+~#>K1Q9JrRq(2pm(2VDhus2U)VRBjIaq;mpj<~CgS&Cm24Aou3$mt5rr>k0wX2qh^5k$13R)b9fyE~?%E5Z<e3Q9-iPPD2(2DBAN>hoRAJJkIde%P-dB=|h{>aX7d<!*d+lp-YN4L`8sV;au-9=((-GIkL0R^pv}{L$8X<vg#LKiGdYvg<E?c<RDjF^O^*5p&z0+@~ahGp6xv<c+VM#T@sMJ{}4#j(!2$GM2A@wQi>b_tk#+!3=@5D-Y){XYX#vs5Ppj;`e;Vj($LeWXvhzR)-|-H`;gE}Z!K#3sYD9rIT`z5l*L&XyCm2b4i~CI^v?9wd31GM_qb0+=|MM{Bu$oISKMOh47r<EAXtwpDTgt91a_@SOmcxV*$$}YXZm8@ubMCtA!f>J(R!~R%=x~oC9R&H;VGdwV-4PdC8B(rZ0+~Gm}SwkH0+)xpm{_uVE!SiiAo2{(l@NfP$HxIf)%odqT{-CC-@tcNdVI>z@!kc7;qzBjv3KhoM6MmF~0u3rB5l2)pioM|6&ssmp860-N4By(lb$tL*;OtH>5-V$|^<=y>f;^OkE0OR|(mVO4dwr7Az<<=^W(Zk?(S9CER$-3!HXZgMRHuzGURSNpskHiSprqc92;oy&$IrBntc^Ok)LgjTxpePY32yRPXtjo}fb4?WQ9i0)L0Mi+R4t6U1BUlp6TeWg1u(mTcL#eQsp;kmkjcg+K6yFS9#fv~9xE+u^&|v;rPZyvTlO|2o{tpe)M5QScoG7nMp$!>q?=phohz@a6xN=)3(w(sy1*9MFE|Apu%Q>_jeZO1=pHxST+n^CHT$ej?*e=J5J72Dmwr^Ar{)qz2+tTBA<oa;F)13xeBV*6Ay>Cq?3lVvV-kTWhJz>s$qVSnQRRJP?Bk`WmZY-*TWt=@~*5-o3|AZk`&&$7*i61fRcr?ys-AyRc|GvRxbNkA+!k*oIU-KVef3ci-8J+Dy24?CCJ8#bGZzBgM999c6`nAJs8C+SwL8Gg)h=xHj?hT+C7Hfr8jN;a<N<pf*4akQj*_lc?Hlg7MHrgGNX_k7dZ*E3}|8sx1J9s$$8NQ+#1{ox>vgCzy+Lyp}YcqVv7-S5Lsr%apln=u6JCFZi?;9PLO&%f&X_Q;qV+%bdQtM1B7tvqLU3U?AXI(d7mNZii(#%WQehS42Y_gahNHNzzDKKllw)%^>E+bZk1$@;E`dieS=i>(Qxgb0PRmnI)8C!l0*hXp_p|#gv^5c}S1Zx?Eszv&?xRF?(3$U}KY%O2+m!-FJIQU_&8g4*xsu<w;>XqP@lVq=kn&HkZ226>_^3aCPcL(@eKrGqa}7KcYN#MpF(-8`w}=UHF`w4Ay1F_gyljyJp~BW{p{&NLwKmXo2XZl~#$kiKf--`;ml+Oq{Vl7yQu%Zi)YnTfNWC+q`U(9Mi=f%tfMoU3NcbH=502tAY>qD?u=)elt5kU@m+PY{0Yb2*&&XsVk4>2fh!lZB9lauzt`XrrKqFVk_2d;nx)6*tTN4u^WymXk-qi980htkHfLny1MIRyMKUi16Ws2Gx*hwW|B;Tu^mJm&8T!<Dgf;nr69b>nLu+oig{r{>e!BQ68fgZHn*#ytq+$=<ka6sKI!T6V~Q1K68xS@Elq}4i|?XRK<=>liI7}sa~(`mse^3!bSPYdZAPMKA?w?BRr-rH)s&Sf6@h$e`W=>mXD3Jx1D!AyaDk`VI(NK{5G0C?-6S_tfpU>SkSPk@#Bb%ejd!loY6D)EP7SZ>)nrV6iF{ox;$|vAfqxbS>-NqmI(xB3Cn?Shn}imZuj3mM6kgqFlG|bD8g`9+_(U@sP}<Y7-v_ajnENvF+4l)ex~KY_uQHX*2wt`-he~ga1L(b5hb=rQ3PMOsE;0tF)g|uD#!Jby+ZM*8a{ZEz&XUtoOwp$~1`-#WbuPYnzka`ddz~roEIMXHZ9YoVW-K@X;ELcn5w=3-{lKoP16CcFX4DPO<YywPO}sfvuX~1&yRi#D5GUMzari}NZ3tNZHu+^4!^s|~-^;wsH*&m~I3)?>ZW)2JJIZ1%w%K5>-LvA=_2QYr3<mQJnB2>wigc?zMrzTagl7vwcQ?9+Q#{_S>oCw1vG;^eB$%lU*bWSVx6h>(FgWzM!*n^T&a4q!kv8M7u@wRI;sg(}upb`p!Mp40QGR^)^XpHaKEIkD-ai@3d?-b`{`mT{`T4_L&7QY4AL8FMkE?Ym5(XghD4KK!(zx5rdAP-4&u_8UCwdj4TNSO8unFbb!d*DO;<H-oWY^4o!5%T^3lWigpzQSYn}hu2&-Y*da?=N|wg3S>!)t2#IisJzNYMVBW1`Qd5WFG%&uhu?r2qN1ueXfu1nuPB46Uln{`Rpifqs}p9MxX*cDP4Yb~A+j@n3%b;m7a(_T`g5|88CgJFxpHv%j|8a|L8Awo7V;UcCe!C*6J`u7j4?i{_lUz(iB1+JLcccmBHlnxw5=)8aeeOhsj)te-5=6W%=nII3Acet`_t!*5et)5}FfXJof&jMHBnlS0PCE+ePT3Z!Cbl$<%+jC~D!6nVv(NWc*YZwgrqcmj|iN#uIQQb&K++U0l>XoHFUIOp4pCxw8`<zD^7kBh1fRt|ECioazYp&cpy5CDJr`G=oA{kUF_ck7<oG*L%SQ_$K(yN^>ueRZB5q8S+d2CGg2S>UEnUtsFxId>{?6QeoVi_Y_<Xz1HagN*p_0YN`TDvgE9t^-kf>8pb`@Ni&CH!<%3uA^FX7?e`4{h>MKj!jX_FG{t-%>#-S!EK*?@3-|T%Jyk3DfVme%LN!8c_r}8)aFj+dBCz{)`&MC@@1AX@`VY<uy77IE5v(q=g0--OTwFkMB+|OQSB>DpM8s8O#U`3Cj@el3ue5Z$~KG5(mX%s8K=6N<*YXCa}!lfSiA}jDZC`*e$Tf+#lI=a3oVL4#Ym0l`NllaYyVjywsoP6(YTSn{q=hNWf!z_@TN#5*(`&l$N@&xeaYWHoH!q8@zV_vS@d8cp*|bZeC@<a(_}8*Q4_trT=a+5qIbXmJvGP^SlNB7jau&}VR(1R$NM_+k`(v(T}PJ?(M-Iwesrq_OKnk%XCsk4U<XG-NDjW>it0zTmnamrx&457f&ZE04Rvg>Z9;#VkRgkOMVb9z3q16`Et0c{kmq$!(hbh3)M&%Lkm#=x%{u_+#pOAhJr&hp0R30{Pq8b4jcgsq5IkgbseO8$T0;#U*S1KWo&vz0+)uYH%BKLRL&W0)56r%^tQOo}{G~6WC8FB)0^3`qnu^NpFGN+kC%nY13<WZ`1(QVXkCDRaOb)w~yEPpmObS`)Nl#f@e;sY8Y|Yw5L~y2Gq<3neU%cb8&S|MBn6TGy>~E6Tv+bIiQCRO1z}ux#H2CmNB~5ebpKyb<ep0oq9=09r5;-rLq)YUbcc9L;tI*?NXNcwvSw5g}NV=)6$^(S8_uG+Op5dO3+rZ|uLNqXb4|ytGTBy74_)gt&4wcIIy7triMorG$6m`J(-;O(mX{q-+_50V?->xB?vORiztImb1Q1GuxA8OFaM-Il~y)nZ!ukP<LFK`!xkyt-unq+f9zMA3@!VLq19Wzujd`|_+7=a8jr&F$@oK<QXS8t>m!z@Pdi^|#o`}ivtb97{n%ufY#K)*o$2voR|vf1mOYd!Mw5T4DU5qumobYE-oCHe(+V7YJwTY+YKzz0EJhNc$p|M-4)i(TA=;LoD`+xoDHZSVgO9)2b-#5=|_FV+s9GXSZv70t#7#SW=3TK9lY%lg;mOs{)fFTvOrEyzgH(h??MX^_7Y0Uf9KLd<ryAzu&Ji@*kF{+%aDZZGUHkW~t<1cw&W;Y!Rb2v(F{GExC@#Tgb9Ihlcs$Cn-Z&UHpZJnY3yplp}yI406*q*Bbj=YoV`;MhfY2gwT+ltT-R({5Y@NP9db;c+e)*C%JTZCKH8%6j1UU=^HOs}y3Caf=j)Pef9Ln5y<}(%(leECJ*rql{2_s4F(DfFa73MFAO{bS89nhNb4C{Y|N3mQxFLG{o}mNJf%Lm?RF@`>5wjYD27R8)lDX`9IW-*Mn`;O_|&C?O|y1curg_(OK1ZDQJBRMZBUgrC2oDQ1l6{B*{ej8s?|eeNNmDp;DoZ+J?jc_4GmF1+CID<EB*M0XZ^gr(VKhS!BiHC>vOz-3~X?HM{Q8t1X8^Zzc3=XyajB2)CTUP<L?wB13eS(OggF+UhQ&+{(&Ezw8;XyAfM#cL_D{h@v)&)BWCHU=X@j5Sbzfu@v@(Z~=Br`;T)0t|RIqHjj;-XwNqA210mJ5l$<|I>}cf=;F(Wf|{5*jXl;O&MKi5AY@DsB%+F@MQhjbE;JDDQk|T2wI$@kRrdAk+61i?h28cszsIs-_dYVV1p9!5%d9qmqI&k8Ea*Iz7X!;JW$FE!+}6`U?7DWSh{KVbc7DyO8`N*x-9?LQ*NNAHp=&iG__@71-B3}N^Bi3}<~ekueEWni<NQI9LDxl8Mb=Xd5)_Hz6>n>!)^mEm^|VcCj)R>*&4|f&flHQ<RSqhtUEkGIPd<o*j&BF0o`GnZUWQAmtnYIfsw7BlZ8Z>#0;K#@+NLYW06-v`1TM1UBmkuLS}3GBBe`g%G#kEGz$Hl}R{Z5H(&Bb`xxTy9gBtQ5)Gh|=F#9tMMR&XmY(PJ%ykUc`_biLx#(Wpgj~eFUY(FODRW7?=AudzbyT^IwsLYnzOE4RFX4(N{-`TNIu_XKC*it~BfT)x_E?LFMew#!E1J5m4e|I-g1Bds2xn0A~tw9GjMoRC-IwlM+fTikuboxI204%@Hmk(ZDY8Z2Wgs}|4O8^pSezOJ2bTn6rfB+QoJb5L!+QtQty2x8;Q>{y0%h!#w?8Yb9j4U1M5sFk7Vv02SjxQ;w{SF!T6u-j{VkOX2Dp(%|+eJkLvCH9r?{e>8H?`SKU0&|ky6~tv*=`u~xufo{+sn0%y3hI03>c##2!7847Wo%!i-0$+m%WkpK!CpQjxGxM^@=duW>exVc@N5bksV>0!u2|T0-LSo2W)rQ+$3N}uF%LLHtP7-<9c)07AFvy{|H=a9ugcnMXE&1-n8*Iy##>$ErOyn9w$BRoHxAvSXbx<MRz51Tu>}dsQ`jkR5+maCQwKVZjYsar40se9__Gd!f^(cCR2zK<ICyt=}4#Ei~1Ml#W>|35J*Ki$Vv%7ubY+twl0x+0`K@K`pA%ml54o>U(JOuPjq%6^26pvHD-<a@t#=Pvp2k8`G6kSJ`#l3SO~b<zwYdJ?(IZ2@H#}c`%9xXz|i<_j8sSeLZ)Si*_>kld7oRSAbV)XM_QX67uFyTS`x=JgK*DFf9YlF5Kq_B*i65hbADuh8N!$t9dH!`-n?~oBM@na!z<Tc<Pvpq*lkFe!ibNz0Jy>&?6@!aREob_RSF|JynU=4g$k1yif7Zbri)sfq8$W8)ij$K-B~sf49@!9T5E~xVcwSs{8hjOU5D7JNIg?r2qHeff+_GFFfakJPI!|x>sr;=l?>Z<onI#sc3Xswl+tFA-i3aQU>Ca;f)Bcc6iotAlxtOBY>|IbS&rbLk7DvzQLO0;<s!y%q?-y-6m-RjA*ru(+ebrZk~P4i@SZOlrAieP>nIl(#2tGrIq$Qk;s!iEYsC_es~FV#1iD6+CCtkIg+v<L_{A5cThqkrpxbk5bTl!0-nr<aP#6^WTgnv@a}bl7%FpfTV<bwO-8Ns(Le4slsP%<Xl%(Oouo2QVl8a!7h$BdU_uVL41Z8vDE02~_F&gyy!1@q93ox26V@t(0PBXUqLZ&FBAByTq%r~p*gI*3hN(5?RZvIwF8fg(K8Yap&AG7b}G!g~DSXV1WBPc~%>_bi^?O`NzcZWPS7EXB)bdtsB$Q%=sVv%iSA4}dFwxu=aeZSP?CC!P(C*QhY4pAY>L2NLeBjr>;X%GunJAA~<7!V#^lU`wf_YJMgK^D`-2xM|oMWs`X)6asiVn1{;Upc2y=3}i)JV^J}hgylapch*7-RiQ8e&C+ZpW&VlQ?5+WX^j@L4SB50$jXmS<KX7(33+y%V5-4{d6xu|DC^YbE=o^5(Sl%XFBdydz_*OZ?Xhet7+G6aLcoYyELE)Oc;{T5F>-YT5G(N*kr)dk{uAl`ejMfYczf8-qxZ>|H{nk(KW5B1ZXPBm39p2fq!KKSax;C=a?(j+hNLid95SL4o{v05s0$DVKd4i=?;tXKRvpg3`Ta-E>jF=G{HilzsMs40x$oYyJ=1az?E!B->H(ia&>{fXMxLi*8UwV(qE)}CB5rPeFDM{+Ve;Mm?7*kqt;7H}<gYu_JrMZ1fLmV)xNUdV+^L-=yjLQGv#4@~n^*-$Ey7NsL=pt1!fc1v(iRMGtdpT<B?X<!n+jnSaI>XqA^LgA!#-IL0=~rz)RG^IrTzc7`?BRoj$_#$!b2^YwLJ2OFo|X)M<!8*r)%f`|Kf6{s~TMy9v&Xq4M}#M2x0(qu92~Lxc7-r;Nzg(Xb2>I0%=!T)kKCI62uhnb>Q^fZXmMP4pb9#!hBqpk_nMn&da_e_{M05GsM1Afr&o#(6UDjxSWMO6g$k(>47^;{F=uH`nt8p+(P;&pnnLC1TaG)p`MEGD?Hz~hhiF__UM5b7)g!`c_j#T;=R^kepWbz7Pb?TGyF%v$O}!~)Kr^wG1Ss8mR_qNgi=wk^<ZQ|9x4l@vmW+sT~^WOzRZ1*-3Zc5NE&XVs-E|P)ggytr_xV069V6cMDf>o#cBh|%mD7Nhpa2CQG`Ct{J?T(4P`AEk(|wQdhTYFd~?z6Yz~#a3AN?;Q_oiB)OgM+!}E(G;<&srpOXt2OcK;I)Nw^Boe~}HG0>%>fW=u)Y45FY@8VZ^%;iE^p6j8-48@q&xXH1tcYMAL+QJjF)9Q5{w@jH1ry4nA6l5KBN^ZL~)2NCK;7%+V2hALFe3~+3wso31JJmVzS#KzIn?DHenlqIu7dmLK&jTLw7?X|*dX`GOHd>?^+zMz`3E7kV8^8l6*OQvI=YXcoEAut^@EWV5ri#~o4xGwgrW&%ValtPNIiTA;pY9$<SBUJkZgZyPS>{tpkT+_=)S|p@IcKG_qj26I7hN7nvc@Tt^P!yQ1eHTy-SC6_dJ61y+O&rMG-K1kcan1Ggue~KAZya*B~xsKD|v15Eq)f9AT=oA?D2Px0q?T<wvA+2!;c+Zr}RfHL-1Co4nf!iM$>_mWS=>$AtX8Iu4x1XO)d}IKS_HVKc?rPLxyMQu!ff^B>jwA{K7eKqL^BiCuLaP1zw<@OeGrh89|p-FU`{eYPjyFH|r%wTmxA4T*m-o*$13@QhT@^RUP%+j!TaH?0NmE>pJDTyk9Fvag1Y5wsuF|QEER>aa_6pY=uD|5e0cjA6jcs=|fpZg5S%{nrUQbwZY<MlD-nR=KY62$t_S9_bqeXRK}9%b-}!q2@osc7G`gK1GWuFlcESb8aZ|+kzG}IrfWm)3(w4bNa&fcC+GaBMDakav2Og8Uu6CRh7bt$g=e%<WYu+<`$Vqz%S}NWA2NWIth3Hl!!qWwhE5=JfibLg3EkNTodT1;CYrVZ3^;L~cdS=TY)$CLl5@(tfQsYGzCa#P<9P~P_+?GdTG$I>5z``3l6*Vvd$h^)Lg|!o8eQa}c))cD0V<S<ROZ)c$ljBLpa(9fHoC{wZQyTIru0Y|P8}Y(x{k7m%n(lE0uM&^@KyEC?;3FgDEwA{V_VnCK<+VHaz~k>He|+96m@W%epPv))qggEPe4CL!0rJ3884j<{;pDFSRJ6=G?+JRhXA0EFgA|D)-4o8p%5uR{$Z9>?_`)j%^d#-V`CusxHT+AftfYEPJZS-Xv}n#JFKnSbaxQ+&s+!G{$HCCvR}kPH9^#{)kFv+p=>xC8TmpA*|t1=A%(_f9-=NTT=n7E_Rh53yO6VZfszHMS*Q(p^0_a6e%?R6{Shadp=gxMM$EZ<-5odvcfSiwLqq`fz1FTa6-xca(`6xz(tWTUyf2j1;(CkE$bpgfiEyW*1b+-$zQ4F4bUjsC`Plhh>`DbeS=)NR&x@#aj&d6K=KuIfV<DGeOlGYoKdcYf2%wjhf=kbiV>NOJM^`%A)1N%Ha~USJ(~qkVXu?bio;^%{PZs=gPG(lMrntx>k49qf4mzMY*n?y98>+utpJgD@5$jZ4Fh-{N+ka!0VO0+qE(#erW_5%3yLb$4lSw{3SM+g=oLeg+3kjEWI+t`$<i<iV2IsUv!5qI2p1bD8(vbr*4t=DtG667nRP~~MM#0L=Y|P+?DEl9EynH;mKGaDkHzYShQzg!LC^b4gb7qa1B#FiR2JMeJ27ZkuQS{Z%#b`E}|9A^{H=q3lLOOeTj>9>nMSTWr#-4e>2z~zWb9NKsF^9X80P0X5nB5LA7d{6z;7yOT<5amscI~%=+DCYr#K7)hEz~Y%b6A~!%l$ZWmo7o;GR@ColV0!@Sn@*i(lOv@cu9VInX1T@6E*cnK>WfI<;*S|qC1&J*RH@U3fQJaP7!}75za>#0K3bW11l}lDv$hr@hpo2V2%p%+7UzDGDrAh?z#9$N#YfGJu^$gD6dnV*>Wq2TOg;dDC#LcHggxrN)LoP=lMuD=})iajYeSetXI!*5jWM24ZR(5v<>UVF=~M<4RAKFcnSD7o)Dh4^!qv1Rc0}UOg2G`C^i<$`rXUC_3>r^$4bXXb<wGt3%f_|tQIh{ZtTEIk1m6?lx39plpP}L0QbkhH8iX~##a-772O4t)zos$rb}6MH}y4NWqKwcx8@RKZge9Mt+m4nuaHq+-R8mKCz@~Gujlt~A2a2eElZ}A_NzK+m#xYiqG8uQGn2ISh2)RUb=|kcf)O7Ud)pH?mwAFTx(9kdg0SIdVF(PL9-*dq3cNDj5NE-pKgM!?Fql~&vYDCX11D;F-jN%@C~c%Y6$)7AxaJwQs#xms7Z&-}FrEIPG@k-U;%5iIS(rlHY#PkMaI#B6822e&UxH&8Xo~pm;u8vHYJ;XrdHToa(i2ea8J^5^D?R#Vjo^w*8TW&&2!L=UXhxg!!(%RZm-qegj{NcMx1av_W`6hrvfmzW*>CT^e*4}0{Ka;$$M{I*UB78w^kdC873*o$+w2$ihr=&KDVe)9;%Ctut3UsI{r;E7K(XjLjHexov2mqi80fXwXYl8kFz@<ff;w3{N`V`IBOm}$-qHv7!#swu=2a{02ZuicK6uOYYxo}x3UTpg?|l_x@DT~y*8Ywim!oZT8WkvH9)BFIwy;4NtLENz<8ZW)$Uj5)pYMLjPrv{2+fP5t@Za9w|Nih(o|xgWI-@M?NBj|+ZBpKxV7hR)P7rpRbU;xErb0AX`UlRTtM{qQa@B=M+?*4S(W;U^a15=NM$l%!nFu$J7~z_>u$3zY>KOg?srsLP{qpP2|NG~F{`i;AK-T^c`VLUpB<+5_JzB8V8actBiSWMdcASn8BMOF39P;^G^i@?qIv4F>>s-JAoX2Tz;mpmS*5?L})JW0iW79`(%T_v7j-3pZfb|lKzz7{f-BmILqAL3l2P^ixH?8^_Q@U+oZjOu8G^;9i>!dd062Y9U*9Nwh7BNHMz_^4R10cJ~EU_y<4nDiLeZH+cG#l#eGr>SPe<8Em!5bYn-Lw26SbJJJ0E=DqyJH#qh_4#D08P_7u1B@zxg}ZjHp=?>&uy+RzCA9hEDx`h7dkd^dq#@t7A8zAO6U&i7x_^@PMbjf$ZO1Qj<t<t&g-}ixgHY@N<;eyf*<#S;Wes^f|aFQ`Jg1~eYDKo&N}uO@1Xn1oz&`4qh}T+!-iO%gta?PX$}PwrWrDQIC0RtMn%CWbY#&ctpw`v#W7MG8+j+lSw}FW3&%40ohJrA`(}$p7RQYB(wLpY=XOM~lFCrQ_GXhu>Rl3|An$UZNp9T8-MBTuFKv^dRQ8X0t=9fDvXm6!VOb@>_2UpKHz?aieKW1M209Y)I=Iy4uh`XX>R3zOuPeg0!&}{`H!@b&M}&KGsVPLbJ(XaOOUL?9`hqY<Q+K)D$trgz+Nv8K6Qlh0Z|Bl;J8ghKrAV9xjB$%tYRDo$m1>`fj5n^dn-f)3lWUS_N*Nm%P-;!?UqJkfU$nh_@;*E<>!>#vWU9jPjOn^I7>>;f#UC6X$$JaU$6ufG1>5SjLv$B$rp%B_zFV2fSHR>@n4oD?KCdbXi_?W{jXM<#Gk=snJFr>ZsT#x~zgyQl=D$!lW^vkDtSbdlXw2ntv!_Bb{w$X4VIK~thFnM9w%D*CCq(SVM*EZ0ap(s<Kb&X@_rB7L^|G|lOJ9j8=N~hehM}{~$mAkE=fbhAG*r+_N^>06P7NE3biyH=k8xwGIw;4GCiP@@gf|g%U5^v_xt|(>m5!1l^hrsIQ;c;<Br-Lku(EI-Wqc8tin(A5Uu!vUc8P%6JNcd|qc%UCi8?1;(A8}UBbjDe+RCiz8k}IN1;Sh4VW-GD_oSwz+AO8O(MIgWZD4F+TbM>XjxP99d;wE~Xb0vrgzhOuhw}0@3o1sm(>OlWZOot1uC>gmKDw1xRxY9~K9{FTz%ySz`ItnQ^U_*ybmgK{7;RD3$FNIOa%f_S5Z_?)4mJQs$2z<4<(xr|*bMa+lW$4?<{oSwq|I&~!Cu}af@!_3i*6d%B$r`v%o5665MX&8_RfRkNzw5I@0rE*5)eEv=!f%@a0<o{JWj$+i)go_v@wM}trJ6vm)zqPl~l=4r4-9UM+sfnX^d%ocrBXdu0YIeoOZRsI8Br4zoIu7F{=QRWu+e*m;Jfro>lM#69tz9C>;rwX)1jv478>(&VnHs)1kpspT(W44qNPdf`yI3E1yd*I-X(^HDA0nkNeTio|y4EhOs?+{6Y;YjK7nGeEBNwPr_Sc85mX5*RJh6$Yo`;oZ!P)UL`E%x{EmLyda44lT|4aFzIQQk#IWayS8-h?U*|ua+Hk0!J}qYsuLE+P>h7aok{C}!PR{4JT+`VE>u7oH!<WK!qytya)vF6p14j;Y80~1p)gL2@#YLrJV~pCJNMDbt=&kO2h5~mxV+8IF+t?(A3R37t0V0VxP?32XnMb_aNiM6moeRZq<q2O2XMH8n3;lUw{tF&%%LbT6vkZkJZ+%EQ_XXI9@jE=NK1-gA?aopoXH|^<%whCU(qPY?uXzD-4|D9WRiSY&wrPR(tT;vsVo^)-N+4($<-)001?^qm0o4<IP#r1B!|ZEik#F`HVodm@uV!#p!x6^We(F*#ZaF6kfPNOG1hE=%ry+-LA!irv-sR@GpK_+1N4bpRmy_*;b;Tp8zSy-a_o4WVl~{sDhMN>!GlUCpDl>~?CZdHJy?QcLZN&DfP;O!OM47{6a4~fvC<Nymwk2ikGIWDH4n1%JQFZQ)-i{$>`{kRo3D_}5-#-CB9|md|9x23@ye?Sa}{6g*aFwuCv5VeV6AwbT@}<h2D%XF>i2{0H5El<8*icry1k1Md1VM|z3;>t_<W2KfX&nXUcwi&Fkp1S$ZgtUjbgup#U^AFE)#%Q3Nlfi+jyPRnNz4y-I3-@tw%`UrS^%Va}vmRrzN7z$BN}3*=a6>{U-#*^GYR4)UCj7XF%;L3yXhl%9V~E40nq2U~L9py07ftY~smEnRzw7hJ-`vPT?@g+tvHaw{I?x*n7>`zk`vNygYd1+KwJ)i!X9USfu8j4A)Y7_4TR>9eG8*E@X|<XxOG@>1^9kz_7GOLn&DG(LcG>tYuZ-2x~o2@h!lF3s7fptu_@ugQy+xKv?l9_8t@E!iI)~wlei-VJprN^51zDPCjktJZ_U+2VJ*}0!$exT!KuggH!C>w}#{-*$Ef%z-fpCR!uraImr-eS}Oz>hxdQ*sb<zWMAmj+i+7bXGBj2i!^AP6B4=tdZRo5+h_{AhE!J99IdSqf@X9Hz6v;;D815qT#Zf$t{Dw)j_RM;(eW)Cjiw>j)c!e9CcF+E7>RAbjYaQy4v?Sk;?`il{z<ILAo}FwKOeLOn*WPRqZ<sy)1iZ!6iD(@WzzB}<jp`BU)tMDXsA!>j0_#)E$726HmU;*ec-)WqE~`XM+bokT0s}x`P60^9^{NGBwrMNskpbo#<OGmYqhsMRdfaC;e@>*zw#4Q~Kyoee5@1R!WRag5Y8abwiMZ(uVGZb7qJDthbrUklghR}=2!(PPV2G3x^Lws9ZVcMK3bnLFP~b?%Mojf+fEb*-Sb=oWZS;H8pLy+sSj?3`G8v3hAKG-T#(sYEG2*B#6BEH)vITPj_Tbm8W2MPypZc1HZN*#0d)k2iVb1MtD(fApk=YCo#b#f}Fw4NaV>qR+p*VCKG|A<7d^I?pw6TL`5B!0FVJu&K@WhzeAK==fK?BwY`-b?t{%E$&evT;GA~<&z&L~6P<vt^%TT9YrB;#O)F%Lt&dqU4AQSN!a8DJj9z6J^!8rW^RyEI^QQiH%v+~@xtgPuAQcw!fi6iE9UJ*R0yP&oNcl_t$hz&J|&z=g*D=U@JssL3Wdap$2veHwwI9}iGTJk1RqOo!=1fiF#n(;5(4$5n0^LnE<)trDIyXYZQunuqPFqv^-3BH`>YioNf&fofzF0TLl6*+-to;n@S22!pjpZ5(Aeh#m$Eh3#b?r_R_HU7(7g5BqCl;dz{sj2Jbj?Td^U5e%X!vAV-AY1JN-sPn&Y17lUFWFBje+YH<S%{vTRRp*AgMehk^7LZo7qe$2v>MDyE!iVfRNI;xoo*Nz(Mu$i%{k*Q`V->-O_I&UU9$ZY-XkCO5!7?}GEBO5D_3Tz{4n=2=gAWh019hCIu?x>3f3D;f3P*67bWK`Ts$-=^x1SyiXU@|X<9Gt}Q|Rsd%EEQ_#&cjRsx!Z<z2HJHHT7{<YQ@(C0f*9>ev<1PBadiSD36I7riVwCG<zQdTUE4m51j<d8M0M8#+GDV(bF?_5ISdpu%;3Io<ppjOJODs=h4|Q&x3k6Nu7uAyuT4iKf8MKsGdl4Riq3i1OL!vyOgWvd3we9gcMce(g6oF%wNy*EKB2v{lB59>Uo?D7s+Wq=OT|E7I6TtAK}%AoA~F3zvW1+1|9IdmFK*^)fs@z4p*he1RB+)_b;kT&-2<7i=)O9MOb5sgA$i%;~4LzvVU;mci0>K!7D^ztI|Ao5`KXiEQrLAPYn!!aEpqJVS~kP0PuWwwecS2r1AuytZo@Q>HP2+3__-!WTI4ZDlIML@%Q6bAwg8bQcqw=A!CbBwS1`6SLe_&k{WwfXhQwsMm4-HEc-x8#k8D)NYDvJ;uu#|wz?B++<k7tlq8r)i1?<UPhQJI#h6f8W-e=A98C}m#DnEybmNh-z4Ty8%7Sz}`xhL@uu(h$+ITEL!UET!<6u$%F6DzKk&PQmH#{h$-;YLBFh@$`ea}UylYA(30&0>W<;7N^Y&s5yov-r~$2UW5(31xca(}gSFr(2v4CtIO0#CZm=Q39r!HyP!d8^8u66&sXQ44THqb5iM6WjtA&?>h?B@$0^D%hj*4&v6Evvnp_8bS^oR>U7iO}w)K1_(}H-R0W5m=VZOWyVp<Xt31h{c3nN+7}@tP#M1}70~i*pqxcb)ae84Iz&$k1eOy&9`5XVs5apm%z>ZFXz?V_=Df^ug_rWjh}#1PtPE2RykIhhF(-LI@Di9DjiTXlX3m`5@=Uy@*D*o|1s|L1GEDm9uLZFs5z9TM>p#~bC+Q$fL~L5S?v_lX0S*vwS9nrAxGZ`>a@nLq=GV#Cr9tBjDb&He-a8XQA9D94CJt#^h)%q%?>*VUuY*kR{+R+uoo)$E5v`D@C4HhF6YLlaVWTNuQjZv{_>?-*j8T?pC@2!wa(!m)&3Qg9>f@=2&Urwt8<$VPx)-_J9kVCP!G@^!LQ>$X^v)u|TgrUK$*pyGK|-=&Jx|l}RQyM1J-8}lqIP~pAM4r~=219@){F3=s;JKEmOUcR$JOwLK7RAFjYqJFdq=KEgA22wMA$8R8(m0Y0n?4Zr%+Wo{EHkBLCo8jE>!}<<nttZg$Jqhf9Zjpx2dmHUPmv(=LBs6x~*}q#eE{PDmlWECQ(~Rw<HOC+3#a7Po-DBiU45VWZ|JKPjZlFadH?mCFo9KQ73^uRfdUF?|$-HzQm)1lLEtIR^a&C=abnmV1P6SQz%K)BZwwMT*cqE3}H7ZGs3)_rA<jtw9VVzv4XlPYVV6Lt*#Tt??Q(GH^*+xhCpL8L{;-1l^%n~UFz9*_~J1f3NZx@<%OpY;kx}1Lk??KQYz|T#IYoKkLYQlhbWzGgXj2>pLjb@b4D7;OP55bjwtc+q4B%`jkLL;)1Z5U#NiE#{KFa*$3>%PJd%#M{_SJ@0tGV5o9OvCP$G2D<KPCY9qLp1p?!^JFtOeD(=I%f99D0WZJssva_D02{vr)I?|ZDj?Lt(DU1x@t9&<m&EJGAyI(aDdNGDE<Ck!Pt>z6@R8_ef`xnh})Lh%Z8rJ)L8d%$@b6wZh+g#yNh`}Q6!WTW7M2FG}znL3ovsS+CSQy!`erDLf@kA$@O#o&}OggWRrPyB-HS=gAW6S|a!fCSa=C8i{DUuk0kK`kHnjzZac%6U-M%u_E)4~tlr_OGen`!Z|^p^blE_evS|p6(Tfski+sP0P*`#1fa4T^=$Hx3o)frx|je<nS{A<zfuxwzqQ})r_*Bbe<5h1y#=&=(wKC+5?5P??@mqMEovQ3i^Cx#<`o;fOb1l2BFRd1$Azxi5ZKYBhoWJJl&rtbqPS_`>_(pS8RsQ3m_i94nhd(0)acbs4_3S7Rz|PY4{Q5T*|n1HhqB;LL}2(<Mt@@w5Jy^Zi$2oRIhDQ77wtQ>oMtI!B3Ux3_k0PAz4by6$1@xcxmb3Q^Hw$`Xm+^R{2JTgn>VRL3ZBTY3%EN3Mh6S*9n`NCpD8|qPH?lDF@lbtA=4~ijRauu?_nS&$Eli6eRls2x3%7FERB@lo2HGCz~1TKs1%9_EMX&TKI>eRp~2PfMKST?ZtjlS)4R3c!XE&^e3lPmNZ7WnI(dIuqY#F01PuP%Q=TlMn=*WKpOG`TdgSH93$N0EY~1ITGTeQxMCY8w~o%cG7p{i(h`1JE>Of&B^UQBEvDme%^h5wVy5Me3yT(^AsDeIWu9IpWbtJwm-#vJ&O}oX%GtR|8M*yqGkKTYbcAfeGDHFc?A3X+9i}ybOur{HGe=4T9DCq46HO|qKZ_7)n&!+5%*&V4J=p;!SKsv&<~3JqO!O(!%3MH$LlVKqxHml=6SXb@Ac<50i(Amj9LXC*vN}Bi7FX9d>hdFzLmBdvYp_^Kx)C`rH+FW*_}bei3$1ha2CuqGFm&||$|RGVh4uabq3ea!f&#qSD^$vyxDzyfmYYH-HXw;xE2ZSAF|S!tUmTT}DaE=f&10APTJlWFd(8++qq`#1T+5=<5vSUUIQ-3n5|YP_ITH2UnN_9R<lr9)-A&vC?@`$Lgc&$RFx8X*^WZ7}P%osE{k6{q({`eo-aIes8lfteTy?ZV&|vAl4Kn{=Y1oFC^hw|<^8M#IEf6ESCZ?eyB4Q{s=c_$QChlsHMv#kC&q<w@reP}TQ1bByh-h_8Dn&F*B1-jMFt4Sv9EZAtjE;?eY%rrt%Oo2kKTEAoD7MH#r#X$6TUH3%jOD*S8B}HV*oH(#&j>NFj@V2@GT}GLn}(;yo$Z#76L`lG`vpTeV@oS35b^yE?D<*PbP)R?))t&pvMI}uAFWM&)6sU8S&{^{Wf|kbx5Gmbq{G$D_f%#@;7fWAukQm}7=@faUI7~g+(RBXGPgovk^|!`A#V*n1whGx>ODM3D(5-&OV!T>LjUL_a><H580wNZ5?D`#Wd_1So9}13TfJ4sY|Ho_mKV`5>0zmJ*%av8CAudO9^+nr3aO<lbG~_fA<HiJLZRlX1ZpjAwo@*z1GZU*#1;9R$i0%OHj4;nFWe0)Pk$zG*D+;N6QM6<J<;WUO2d)Fjtk7riZHW?HbPtU3o&R}!@gGvR>}a;oGM2I_=`Z7;~AGXj7bnH0#Qwl46#DF`$h?K!AVK9vNCZem32LX7+x0{FJ!|uMo?xgSQlKlAvZ!vlnqDwQiCj|z6xoje54BK$Sw^7lGVBSOeBC=PDyb53)ox2nVr5(LybhpWvn0%o%Di#^zu?VX&3=*_U4rpHm>6JAIr^bqntmALP(yNff<YCsZOcGZhKhr1!H)~!hB!%zyIUg&;R<%9|k>iEY~E<zEY}-Kz$7$4`Okm+Cyu5pV%x<OxQ{ATsX_YU^Y~u2s3_{t;qBE@cpOYsn&bR+l{oZ(N+_6cxMsAKtUq`)ASpJ@YEqSFAXu2E#qj!fN}o;%-4wQK`c9Z!igKQr>JzJl9)$Sg&>G0xl1oMqi{eyq;hd&39`#v!y{GhbT3Pkl@7@s(G5?ORQ*WL4z?kG()g^RJIG}<s4g<!3o!mL6-`VN#|r2GDfjk+@lJsyRgpf<;a7A?^v)CSh&KdM9Er>FdyIlSD^tr(c}bZ<FEJ`nIWzwVyyn^|ubI9q_G(gwLBP<U$nP9uTx1SssioC3>M|3DKq#`W{njIvqZTk!E*~8j>n8K?>NOOvgU4muX7Jz^-=}xw?7OUJ5|mQjMXSj2xx7Wx>`Wa(?KbXp^Z>W*=>wO_JNI=MJLJVh*;LyWl_-=shrhP;PXO(LPI8IfA7^MjKemdJQExzT@&ZRRQU{s8I5IU#^5`v%8UkBYI>A0@73MSJ@l~0oW6aU}%CRq;*u{szbSIS_g^2mY7TMjD+JzVind@zUGqS2s$!w-Sz}Lnj>x3*Ly%^r{qO$|XD%iDQkIK;Lq^K#fYR<yY$06f`@#K)w&g3I;v}V2oL0ZRAy;_`xnxoj6bLqEZ)ltSGGpT`)(I;_qBfv!+JCVkjJLSa`nl_AhOm5sU(|JsKfyN^L1BEDjbg8Ef=g_09Z_EJB$)SL)bXDJD9kn_}nOh8>_p+5729mO-N{{e;7P+)7?d6fKfm2(?3vlX~1y+a^gsa3D#lvNKIW#S*lt|K#b2gvj-{t6u_UW>&J%kldFkctIOPz+OwLfU&A#J&NTnll#8WJdbb#2~L`FusT=YuL2xNb|s?G#;8ywJSSjblY0AZ+KIjP;W0H0ynkFr;1*FA|_$pcDQvkvL{v&eL5IRmm*#IlYSKiib|k6j4_2JtiM5r$KensyZ#*6+^v1t2O%a5|V!_S2>Xw=0>8D1W%~=i@g2UH$&A)Z>)iRZCdx!OE5JVfXo>E^KJI?Ap5-!SwWN`(s1e@zPBuQ<_vBg5r2OdmtvId7ipdnd&6+@hT0Q*z2@AzOv9%Xtzrl8#`A{eImfgE;;2BRm3ydRXMdfG-qn#1P{AupYbHX5X|7NC2_PUuU(sXlJqGil`n`;PSZTsfE1iSE_5+H*36=3+oIOVqy10c!^|We<?$>7zuhw|#o{tPE6gZ2jk4s%nw~QE)K7rFq%I0b`^fZC>gGd2PBqfQWf&#hD^32NAtdUbozf1u6eWqj@-YD7`6WqslMekYTu4Wr{k&~)@L{T6o<0iux0Ll6){*@^*x|9cm??T;9#S?&G*5_}4Uf|O4GWMkgV_)(TBPOa&v`NMIHZaCj<=kXN3XIWVR)lmXF)o#3(3_5oCOVr@2R%6L?aKznws#`@m;<Noa?I%8FzgDca;FEP){wv$rtM~j*QkrtEXKm9R1&r7WX9lALoB)sZ?Pw;PA|l<)GxxZ97F9QGG@%}O6Fc4Ud$8W6Jy!lEJ((j{dvL{1zM_Vt*YXHw5qB%BB|iQYqj)=YV@{wF@{_>F0X4xp6%mOEC|)UbvN7}=GFsNq75-}LsrC0>{m?Sso1}Qk5T8eJ+~~cJW!Y61$tqm{{WewWJ{ChOD|(bx1Xu^1XLo4JVjDbyDpPTHVPRO^O{Y%*u1~yvr4=hfy=0D$QB}S;;h<IUO_J^Nq{n3kif|V#$I!YYEFj;-cTnl2u!(>{W*)sOY~B*gyj8l#u+IVHNbk30!z6N`P7DL={7iiPt_6fD8M(K;K*z(vBl*>Ib*!k$026(!;Yrf5F>%uBw@;=hK;Cp9^z;k5+nvq3YIB8(bPK=PC`R<<R8~4VGx<{=-<7ZLc?^V998^Lz^jI<PqH&i@#q-s+<96VvY1gr1zc+aZga2+-P0^L{6@C#MQ?3U2@^z`7_jnH?a_G!C2uzg%n3BTFL6MD^dCc?wA@Dyl?T*zqd~t!vOBpwJHj6mOEEXN2A=%Zc-x;vTr^?QTFkgx$gh29{EjEYbPXR#;NXFr!owGsK12!g<&M+3>14d&BhPpy^YkZf9%37nlM&EB^eJEm5=?ofk{f{Q%u8%xcc%jU@JSJ#MZ0Wsg3$vU0>%Oy(0;JNVFH`F73G}BaXD}MrGn06-N7PP{SdH-Aa}$)f`=UR%kvDjs1yl+8iBx1AjNW(;oIYysdtFhoUtK=X{Z$#`nh^7b=&lV6Wa2a6pZyo<j8Ak!xR*#?}{G-n{>horAH7#J;}2=vJZV0C+PCk5)vFi&m4mbe{kK$#4++S<KQBD2MC-smD>41-vMT|_K>7k#)z;ERF+lAslPpRv}1(NKBxTRzE0~8IoHSxG7EXnq<X_hL{FQj@f@_wokk(XQtUNjmf(RuzGYxF>`Jrb9_eUmc!w}Gh*!RW&W)zP<N{~d%0?nH;knb<ytGt1Jw9LpItdXXCJ{swQ``eC%x;gEc^O9JNzxa(g3G`I&$yOrjebj#^5-!A@$HYJIt9KzK9ikU8tx!_h97P;N|6Z4LQY;rBlS$rXVP047)>XEd!#TdIqK45ZKiWFvpyNto<k%+D81%~Saw^6qH|{H&o-f@ilty_N0O>{vJ65=RLw_pW@{)hniqdB4OP(j&>Ti1%Em--sfu`t<(!s=JczwPHbk=lx2$&>m$a6KJ%}nE1hJcStr^i0E1iR3?y~rS&9vMPM4wv6IX|xda(;+>?Z!c0dCmazu2(?8l6Yxs@5D4LLLq{JbMyFVl!qb4-2`BmQ9KDgCw;)t1x!Gz{WYF@`9|oO2gq@ex}03iv8aK2kP@VzEY^!AUBRnx#4-wx9>bA}%HTnttA7BNgjqiSvW=I!u<}pA@vf9(OG6D58w(yoKAdU{3kgWDh{_bN`gmc<G0QFTVd(@e8K^cF{-Jdj`;9DQV!H{<iZj#soar8l{H)O%Ciw{r3mEL)ZKTtn)5iE6q>-`z2vrNg$i}B#t`M|ia+;5?X~JL7sj{Y{yuM6fW2RqT3GX-f!H|DQ@zjo?&%NN#fMW%IGa!w3kIz@K)t>i#ckRF{@G{F(Ri7bb-4JD{#jFKj74J>j95a<$I~f@qt-{;u<n!80dVDgi>c};89TS`ZBNyA9?xWq*_SA%@u9LLUsW=qjOT$?tQPo6QiyXIYMt$fu=7wpghpYzWl4yV%FpepO>t!Bw<z&uyuR{JAEJ9!INj=s%4Xf~EheWz=CIPJdEVG=_tHqd`z;J{_0vK!QJl~A=h85oE+)3EoPz15UoGOUG@%1EA07kcTvB2m#89h)804Z^rIY}Z!j~!RKVW&gWZazkwNa`}EZ4_qE?lX3FBaR>*;WG4UfSC6KBRk5FE2y*SOU5&4Ji=h$V<*uo3l=}rmP0@N$of}c%B2Bsoe^e3{ln_H=)M8}x_Q_haxmj0y4|Xj>N%NnF0;&cED@`*Eo6OxuJudM|3vRh<a0dPp0y+?fVAVQYj%k=>`JTWV`A<xBrWHuS;B<lJ<C7|_%(KZbaw>%xjsXbf}o3HI;DLUz|f)xsEM0hi3s~+;9ICPNn3af){GdJ6?LRJ%&LzZJ@0@0>+!KZr|QI|o|dJmU~%g0h?1LamYCe1&AC6*edLSY14O-d+GgT9DlxcsS;x-iNS?0_+fn_iC{X$igQ+Mq-@KPjzJL3eDW@%3qJ-w-2G3vA;kT@_Ow*lUi<X7jr8?C#V4z)u$vgK1!L<AZDe{7xbxDJ*{g4`u1;hItq?HkAzb($0WNEuME%Z|85Rn_w5^hkkJ8c4cdYY3hQFIEjK+#Nr(MObZQrfQRvkNOS0l`1;d_XiHW;(1*J71T5?%|q-y!1yf^5eBWO(`(ZV1``yyS36FLLr9RxDm&^i=JeKA=mAbi^Kc}zPS9Nvo<8dji-8P8s3f5wC^V*bPpQ<p{IJ+>a?D%{o?+^@K4DW;!@aJjVWB)Nj6IY0$K9%KQ8OBQmfp&tf(#|S^rv_IJdLivbqeDS(};r%BzC1&5(rzbotP7KiCzYbisPikG=ptPPZwJgId*P#Y;As`(?O)k?1xqd`h0L@Z*4#bBYZE%xxG^J6A*s#u!~;cAjvu-sW2QT+f?Ot-Ee#&d+s-v+Tis(^QJ=dkHu-=aIWw{Xf3__R}BV%nv`_fqi?t|G&Ne`t5i8R4OsjVQl?J>C>>TW5(5>9<|J`n*bH|??CfyVGG)o{WtDG>11-&nCCx8l|NTv(Bp~!J9|^*T7i9B+#E^kxV9_9D%C8d=d3W^j{oj;&k3{Lm)ttQ*4MK?9C8Djul}zu{~GuyB;t6)RQx#I*U{KtU{{EEDtMCrEtV&>+FL)Jnq4yTGdcD&xA=$?MQ=V5>CeBveE-v92_pPgH@rI8$FXdE4gVRyoXJLwb%=Y49%{#n$1@%x1awBiV&l}uP5%BbKmGp8Z$JIm>Te%m$>-kc@as>%|9q}?9aYBJoIk>R`g?}=`>4h2Zm148*03w=^07EJLlQ?<<JmLZD|^UTL&yGq{`JeRKmYHapZv$a9MKVIL+r1er?$EF(H!P;q(!xUpLWcC;<e)B<&rh~VwoTB`yUcto*vz?{j^qo|CU|T<~zWaL`4TiJxHJn5077v`MuC*jdh33)R#X;51$x~vup42cV1p}yu;_cX}I6*x>C&o3W$Jb&>7{-&*73F(}~my2-7tS?)GyiOME5J$s*DOkdDOsIQqNxo-Aw6N(KEmF@|znxajeeYO{ID*I9P85u+XCDu7PJw$9H2<0U(O^)1fRy-sNoL0t=uYTep>TqA&;^A?c?mgqN_*9JiT<67iCkmvI~UiuHr$r?K1Gx{mwajkOkhYtukHtjp9FS}lodW2VA+=EY#ru7^19^o;nT~FvjprOr@v_o^azQ&eeSYvpj$z<E4?^*lodw;Ii7B=?KGj+3R;N_wSKot>n9<@zJ4{@R~bR<CrpmQmUOhKk$D?W(mlRLy?ELFzj7#E{)R4DLOb3(R7ZSZeCo9b$it&W)N@5{8xTb76Tx_OW-(O&|t7Gv*<WVOa^&mRo-Ee_4}SH5A8B~lxjqbxx?*rsIIVAZc&)@tza(~~TLuLW$5`<#E>6{O+helwyZ8uv)J37{H?;PXjOr}NFRH2madq!#1s|MPF}?|&CkiN~~~T7=~RLE!&$$!{M{T*MYSE+?{fJ>-j1w^2I8COSVS#=EoOCLME_8nRC64%wtDIDjddZ7s!lAM2>f^hv4LI~mP=9eKkU_duqh_6W>}J_x1%kV4w2p%b+6;$xl_j)s8!eJFzJ?M_3Ku&|}ZpaTK_GpQ}=DdA}xdfJrm!XnUWum#?GK8+z_JIMp=|0DSDDL7(`D;cZ;q9zG-pU(5tV4OhFMpoA*CW4LZ7)Mo$>S9Newj(TEFf}-fr_z+uYhAEuT=QLaYOkDqXZ>H8f#Gj`8LfUeO#|dV3-ySF{t26K6lI)V@DfjQ!j`!$j)by7yT8nVnDpl9OXDg{Eb6st(Y?H%okY(e42)^g+2;{?YN6k}>vGI#*E>F#8IJu;QmdIV<UWj$5ELQW_8{=#vzi;?>I~rqgN}0*&k1)MyF+uLGD%CRD*LUUke=p6&9P|7C0gC3SevUuGOwAwAF7-Nv8Ju@4EJ<72ew5ShL*}W<UliyEXs#_9@D(%l}<D*i;Oc{#xw_?1it>zB=2xv(cPl{_1m|9zK6+_^T`XjPtpW%O46(9NI56N;=M5SoY(yCm=_Tdb>py-YTQao$E3JkoAHCeE*V@Two({nlIXH+o-8oRO~n&(t||1dM711D%#N*M5B~rTFL;>tr-C`4U!Z@)#xyG8;P`Ws*T_}FyIDuU!!bkm#gE>iUtkxOL;cwbjOX)R1)5)4{=NU>&31>S_zyMovpN2Aeb~enK>KjabdhB<f(~*YzJ*?HJ0T9_q{nX=RHP*E?SaF<r)B+ZbIXriXPzR5|4qxN7BMZ%1$M#vI}w1WnlHra=M<tW!FdrR<(bC^@*|kTb85hqflRzH5^sbmJDUP)7?K$9gGo!sf!+h_ODb*miTHQi(@|_200ouP>@G{9yryWAF*z_HwJ259-oiRj0~EEXa*BW;iM7wiCDvHH0_UHc*|}kBq&R;MUctS!)Px4(;bLXlViZ+pdwXK<R{ed<(nE(8qV}41Y+93+XnBkR2tQHGa(9N6>ZARQjTo6)sNyNop6N7A;P2^|>o)3bNNtF9cEf6Nm}CRKf$#f74GztwY*8*ErCvheTFAZT8jim2(tt5pRxzjWO)eB9DDwVIo=BG>GuJGmnGEv_LVwA$ZBMq0-sp<HfYfhlFnl<*qco8M0VATZWj)qClsB{wjBvR`n+P}4J$CcZ%S>szK9EObQq;@<A0yHUq3t@_Q4zo<g@7M}nWN>A_fiuaj2|dxA4_DugW)0S-QanpT5a;cYu~#Aa4B4dKudPS*h-oVn1@AHhqY-9^1e%k9-QAb3R!`(Yfpk5D#+1#N%wis{k`aLf^b^F=?G8TJVaRZu%;&8ppdVFoWH|go5$(dmw0*Y13ZtBGK^1&9TAPXO_6gVu;e)PV-BnQc7tb#AzPy(?&QDbhK_^)u0h6@(eH)NR5nd@jCZGrp*ck-r?X;H9V#&tI&JurfL$Y}$2yny+={if@!{p^=XpxtWk^DYb<@zivpurYl+X(TDd8u{ml>q)7+~$l6mj()b<L7TQI`y(^xHg=VVErMwVZ25ubTQ*x7PMNFS7NCa2?M-h;sy)r5b1mC`+hv;m>n<lE;^DeM&rHZm>$R*eXHd2+B4J7uf-$nnUHM&%`&B#v|G*)_qf~`7x}yr#1W&f9rUb%_%4zjrOygk_S!lF_$V!fI+5XrpE|+SyI)_xk1q|!9tQNi0ryhN3hna<izN}38efPQT8=ok$hms_7}WCm}nwXkGuP*eVHJGq<(>2{92xY`nuy~$sP2g%41tsSspUNszQ}C{7Zt)z%jg5uJ?169&>}6cE>awVFIVQr(n1DS2a{8pwN0Rp#LUAgWIBLtkutE<PA&s3;m#FRCAN|>9;MzK4e)*-|eC%z;zAqCUl^8T}qOhQAGmjw|`;c)DMqkvq);U^t|+;=y>Zq>jUA__Y*|+W;XyKsqy&Tg_SbLR2WMQo<2}=H|bzjo60bI%njRGp6Rn!{S=~{Vf!2pP)^5!H~r4bCdXM_@<Kl7r9~R5K546xb|Hb7d&pO=u7y*SCo|7iJkCV)I_K43Sn<$dtX`se`@;$dQQ=xT<wZf7k5Z2034&m{e+{vRB$^7ZH?8D}bP-pdumNKQjTU;B?1vvbf_@(_O|(Xt8NGq@tZ-j1pag65UXg9+P=g1XbsZ9@SFr1pOjI`T6|mp%(0mG)enkSV<sG9S)uf7Rn0w>j^eP(mw?w(vi_TeA0qeetd&(-pcOHf26jCEN5siChuZ#lz(Eu3su?K@U4|dp(<e15Q%(QsLp=X+wAX2lElK^|f>jCZ!7<k~6K|oZrME$k3eeFnPbt-OBmGpO6p1yefLvzE36<uzaDPmhkDYy+={8b5^Pwk3le`9<_bA!GE5@vp0iRm?YSv>YTt%3yEx5F<j!>G#cX}DB|gQ9;Sqs3_UvT<R7sQEG5S;-utBePIeiMRz0dAU+e-VDOE9%U#p7K{TKIPIov{c|o|X^?sLC}IntCY`N-H1c4B*JnS+Dw9i)>kqUDGdbw1T|oM7I5%Bde4OGqqip8uJm(U#z9CWpmPNCLZIf<QwA15swh_HtOa`~O^B$vAHE;%rj(FV5c3U{`R{@Uu7~-U6(;0h;V+;MPUF(&AfeAU}ga>O&!PH%k3ZO!h!+IWqkRTemo{Sn;vW|XS0v3DiQ);DkYI~BQzbyo8JO;XIy5UFk@LJ0xM0WJ7(4-veC16A_$JoZcO^AA?ytJ-Zx>snnN<+8CkgoLff@p=VIJq&ZV=|R!=!|CzI8)xsZBqbJo7XYQ9p?DkvkzSpjd~I|yQCwA<(e;pIwGkuk205Pma{a3F*#z1eh#smgPxwF(EMV*YL2obfS1JL@DK-$SWi`c?h$Jk`&)yYV{F%=<cWir=)83wNk2ZHzP-)!B5xc;;#$i@TQeDi{TSF5IV(|gMxpaz3D_-@Qt7E<?0X_>%TqG0yXsYZ<u(kKZ7OBd#WOxQ+$y2(1j2>RUWd|9(1pNVkvWff>a3|%9(Gi8)~E>mizcyOMk(D8*>FZ2rN|XOnq_4&lM4S^3Rzo1*e}%(442mdR<hvQ%djMYwhn<kIZ`b1ara@|S0G=YxZ9sCeGi2Ceh?joG@~)B;eLeno>I55JlH~6e;VV^!%a9>+o2O|Qo^u2q$+`><)j0=0}_4oviAN>uZbQrFPK7sF0Apo%%yP6w1N?u+8c%jl{(4Y3?dK%<%->!vQ3U4K!?C=T<R=$KICXZ{gMe|>!a1LH!nGKOeF``dQ9s)o<=2&k2p|e*H`J|zWTtmmytG*$Bn+*(_`n*Rlj*t<1y2JBL1#xu1DRG)eVu%JQ>D1KR!Eb3?v^celZhF$zB<sN&uiUm0x#J3XNf#b_Q#4?LYyRJ4$%RWb$BSQ7==Jf8_$@jObqR5wB19G32SQsZ1mEfsijDuFgdkOB7iMiS>j}MKVVK>6O5Dm1U9DpuIP%>k%e^ITlVVxj4zIQ%H<;;Ym^vbxpyjQCN2{B_UjvU55-?7qRsZXA1hQxB0A5${0wowC=Bt^k(!Xtc3dbk=r@)61z66IY87*Mq#yAl-X$GoaUU2U*()^VKOnO4lEpB!N_xHZ`!1Olle3o#AWoh;sL>wvN^RM&wR1^0t(O^>^6Af-FibwV7x(}UfE_<+sk`S!dQk<GP&><aMhxmW>f`-3FEL-Ya!0=0ITv)JiG&!Cr%>4!v;&EagPhNKCW_G`ZSG9wCwsmIMt~K%H&zpMefVC=QGe*?+W@UEWe(DFkjupJ>n_}u-Krw=yM@McSXhfmwoD!X$zBsWUXPku!o8IK8aaJ=n8UU&R$T78<GEuxLJGcfEi=18y9G;<TMq@AUKipaod*!gRfKtj#?K&qDBT#g68U&$trW$LSmLkWjx1Q4eXi*ZO0csWb*{V<65anWUf{-|3Oh>kM-<q{lNp|G4?;V<%P7kCAR9Y1681MwuyoyJc32VeuF77Zd+WPfpeXo6>X&Wv;@bCUIINvUTA{0rl?z-W}DZ=q%~{;;S?Yo_AX?bv#kKvccqCqS7E-3>`{_7JwnqFVNJXwc^z`?dsJ$c+X0<mGmHZ3uy;2F;P_Bibf%4oG(oBbTL*ZjHVqlpX=nVvwz845$Z<a)OPW^tMAnwlSv_-^)8vH&8geDzoku%4d#+6#LrS<rR|O3i7`#Rk=4eK~bd>t-3I}+MR0cd`;izM-+Q1UT5AiF?U|d}Y$1L9)5^d-&_+W1-)|@(SnX*4lGV#_C;Ew6~K|&7WHjimk1=F5vhG#JkK6dZ_)DzMV&XaEqr>T=Oh<Axa@LIbTrghdisAMWjHy{#p$%YCY{<-5JUz{AN=Y-Zs!xE{4K%(C$a)7@ift@Zr%XQkGYgMt2+7}e1YSYF<$?yeqj9-YNU<k2fa$8_SXgSFRrrVrnot}+T^SNDEA~Hnjc0PtYCph=}O4=Xf*EyW_7-H?VIpH%w)k9MBXI^`Ao!3M?%SA@`d3g>H3NgyX!0_%zV^eE}6!{bFx+Y8H@KqfnjmkN!(!m;d?VHu9H&{!iLKD+!$_#xxVJvpfoK9QVJri`xHoE2}uL+KdoAy<6>a`>U61CPCi6}wN4;-TmrA44092%>T=sjjoNaf2Uhqx?HYF54rEQvj-RzfIH%c`SnC>A2ziPKH@JWltiDSNIdk4ZoQT49NyClxrIY56*+G(3Pow?mJL;5{6%I3+c9aKs!_8uc?C0|@$gl=~|Vb;{EVU3|>?a)S6{U_~WRXFY#DcMfY;4QGAd|0?rj@Wv%#>n;%``PB~K*lDVp#)nKEULr}q{}3qt(&9$0XX}{Erjq1EuPJ6KPjnI}Y8eWBVURAYdj?7i-v+Q(*aNW{X%Vb7@i{bI9s$>BWcQ=p3Ra^-nggXjoBj~EFZYomf52X@^QRIeuM{Ani4osY`nGkE*~b__DA-b-BTcK-aC*x7%;r8JV(#xz6xc_$)j``LopzGdf@Go4K=~%>f4C1jd}tqJ&`hbuzD+RBqGX^Q7`(u2FN-W69?-MmK>H)dQXsKcspaoEIE8D1x6R%mo0AerP!r5^!QO2$rD#x@C+*)VQqhC{S#N&{QEgNRKqi)Bx`<Dd;tvFSU5CKM<Bw>jPERS3LcxpsfJfQtW(e<bkrM+4`TF}OeNBPs&Kr9E7aw79d1GpTGdH|OY+*`oznpd8BD&~bS;PND&964nC{jHB;H`Z{k#Ci&r$GnW>?B}5>!eN-l^Z*A1&s1kQyD2mtYO*n<2~rK`tS>90n30ZdKayPF!9q~ZG${P4Dob&I{a=-Efp5FINB#~8)Ywx;trCHa?tR#H779IDd8ABWN-1&3Lrx9A`65isLru<MoUr2kY?PWOV63_(miE$)59mwf_&Yl_W#;cy!}GbAUH<61rw=>+=K+q<OJO0i|~(&g>85e^VI*eFD2uq<<j~2giR2lY-`x@ks6>wg#f}3U8fD2SKZ8PI{JvpIwedZ)8BNB`rcV3dKXgaqJ(C8iQg=7SQ5pm$Zk;?6Yuerb=RXXRjqxu6aDjZ|MBg?m^MOPr<FN=EUbA$y>j_lg{oKSeP=VBGST2w;%HNQ_uhDMk8R&E$_@fpN*j4Se`j#ZG##7{aeXH$U`~6()RT4ZL%%$i7L17gMW1oQ^Mq%RdNg~@m>b#v8#QQvbE;;HJEurlfa)%LIT)yQwN^d6WG>c{lQQuQT{E_ZKJdH@gD>m(lkslaveE8SR=&|n{GO-m6}4@Gf)24|;DCT{MYatPq}P3a7C!TuuOj`3iANdB@Dy>BAkL~~>Xu<l3Uf_<av)%?gsD2Fz(Go6$~66)RiOE}43mm*4su$=OYx;PrXHEZF`80@=Z6p$TQ%cJ>$uaRnTeiYT$)CAK%Ge#-4jd&ME_gOATC3$HNmmRjaW^NYzyQ~@vV)E)q#h<3`?)(11JMv^ZnIHl81@<Pwg_Ss$IZsO6P3Tw~1{bIDMN8F(e7Yu)z)By83iN&+~M*ReK_%9m05>yLGr~iDHA6N~N^;(M=kMJ^?scwGen=Ixs$LNP0F`u#970Kt{WYSks8w8pXyu>5@I<x-o4>8a0U|{xw?qIkWUk_`QjOVh*XGhaq#fQt#GS^qos4zD+LV@xt-I0)$SV@5WQ<*h?sR0n068O(<st1+<9f8)Up1@K0)T_US%zhsV^Gbh{#pW2x}u!_V1UAaCQH4<>z}6Rk)z`N514m@AlLx4Qcr&2iHc05NJyQX-`!Uoof3e2#p7vbce<Thz=#?NOyl>M5ukBt^?Kbkr}9)I-)%TBt6ihx9V0aEGSx$@C$la&Y=`>~tmB184KVJZCTYzf6;uGJF`E${~r~EiE0$e!R6XYQAup=KuP9;q@hM#E4tyoS!e7V@a3pFPIAJG3+YlGb5TIiQuDfLE9)fySzMe7^UB)MMlScD9N{vcSYO`E}Ph|c(;k0K61GL4S-JQ&5}rP;Asqr9~f>gMY#Y*+gg4xm_ZYnBYFrPE&8yK98&BU%-E^sVnO~W0R`1Lqs)eyTe>f37tMGN!$v2-gd*4<<2aH)n`gae13Q%|3QZ2940+RB`ub%S1YZE#E=zI&r_F|aTt(QAJ1@BWrQs*aLVOsdV^_1vN45{}^H{a9^%(`si+<41>tGOR9ge4TbF}z5q-5gz6g_q#ai`Kfc#L=JW32`Ou-=rZ%WYHYmv-&TkWfBnYA6s6NrOukmI*}*hrDEIwA`8QYYJ@77+(FvwtddaBy+sd<rBDuf?k7m{PJsFYND%85A>pc=X~@oJZULm6u_P?h8<MuJK(N}fV<P&msJm@U-MOmAh>BCgR*{0++V4i^XLpY`tRxJW*9&Q|N71Q4f+1<W2O`31zj?{pkGA`x->nbQh*$j`Y#Fb03lc#aJCxrXxcrQ9E3bv5T&ilJ7Xa7q6j3Kmu2hH+T*5+>q>OG#VoHZs;1G{`AL`DrwvEwB+lq*tFl05$fNyaYZ@KzzAdQ6cfa?0c%?WAq~(kFkvuyM4lrb39^xJt%%mG##r7`NuYzg%JKD-3VC)z7ABKObivnm|O_*f_N8k&vdN%0#!{C5K;SLkQAo<FV40rnd#+u1)&m?E<0)q6~I@Dg)e4GghC>H_>nXpE%@fNG*G~K2cLW)=v!FX;z38v1wfONW|<WJ#KqGI*uE;gv4V;E?P6ag9Mw`^AOg8u*Ux%7}%KHJ-pRB8sb6`3+|5nB<Osn@l0Vm1rMuJ8Nfq5tFCZ$JI<&HV7=!QZz_-Shp|Z@-(L_ibrwGjB8**KZmdd#w2qB`_?Wml@dBr8!4o-ynoqj14Y%9{5TLo6xQ;+=b^?d{bFQ?3&px$ZPL?A=))mkO#NlT;xCh{QCVbk0sC%5~|^^2-3!~Wf&J(-}8rrL%)4$!<cK0Sy*jMnyJSK@h{&#q`IS0Bp>Ufir@YC*tdW<-ImpenGJ?}ZNwgH7(4vWzkd1k=l}illmGaac_Hk;?zhbT+G*#Svbk8F9&1sJz~@c3pNJXAq|QWh&)odq*l_=Xv7R>n*nUmE$F6Df9dM^2f+m3LWi0$>-tplPz!Bf^@jEPyU4EOMHJvy@bVeRFO()D48}?GWjJz#YXc(48$-835rSzn2Bd=Ja=eyQK$A-WX-T-uvq`rC9fsX#JJ(tUq32vATpbK?;?vv6@#<+Js@h#n>&!OH9a*b%$<Yue~SimLf|LON%e*5Xy!#v(k_d2EV-Fp3#@)_BET%#^a=jkD$1JQ3V{4qeHjce3K8HRUH_TM>kvWCv{rD*6ou2oKI@c}_UM(P2B%dY3zY*PF120k5_)=kVifXAqIJw;5reEp$03`b+b7bt4IP?Vr0EAXs+_PsyXt6>JD^ikNab^2c{b~CTtb{@4&FQviuHwLaiac}2RM!qm<J!zZ+4t@0A+%0l}`I2yn)QDDjYzV%j>9cQf!{l$n{)EB~a>1lph_XQY_<F2C42l`|DU)ik>sr33KtAq5e<s$!^o3Sg9h{T_^!$Qn7A_NuyD&LTH4*L+!Y^<HDk)+wF5CX~hg8kD<Otj3>Evc|X0ivf@u>g#xA*tIe?B4mqN;LepwpatC@cLq6F=s#_A$!ZYL5z4ApZ(Z+4e;76(nWC=B0NAljSS9%Y4X>?O@2G#$GOZ)YC2czMDHWWJ@24a0JrL5@Bg!Q*Cw!rlA+C22j#cG9IUVyu&;VQ@+Ry(utJ3!8s>_XsN%fb1-Zg^MG~%=2tVC!(%ula@@fJfpZ$#WMI3jPjG({NXFD(*&0oST34#C%dVDxLPO|nxLDT61ro+imv;V`hFM8qEG;Mt=9Yvs>7!uKk268f@TL~)_zT))VF|AJ7~LL=ewd(r#(@o_;5C>EP!v-$cIWno2p&omK)XH^e4<^&25&=YCP)n(+#ZaivZs%TfL$vzQ_Rle1*mMFEkw|U{>>F)3EN|+vs#n;AmW~3;B7|?kepJwdm4+LKD74evEScZx{8kqQh?D20qS`mqP&v@gn$wIUx3B5BRqz(ysqjqy*Ax2HB>U7l0kH3gDMasYP2Z~`%tz~tA@UqEM<v}P|$5txCfK%%G`u$P>u6>nB@AG=i~Xlip4}fjWD?nJ1Ui-S0Sp?=tv)eMTci6Y;<Kx(oqf1kJq1C=r`}W9CO-xTH)<u%n}tW=Dm$#9(zV%eR1I3v<)uc!)LW2k8|0F8w@1m)gA#s)%o1fIRW&biN}QZ?YY`>2f;kMLli7SSp%;Q;k@?sOoJ!`Hi5LpGu+eV9N3l?Bm{>)^7^POtmCK5`*Woj<|HwOq}!*LQAMPDC@MJdzc~!m7>e@OZ{Pm;{s8>LF39=ll}VjTGA~YjsH!7w{VrPg#+*)dng1R0BFx-w-lwEGe7L|&Pp7g-iE<2f$>6IqoSTVGQPM+jj8abVaFrt33CUsvD9L;qTg5*9(SWcxWZmYcf;pgHpnn7wW+e#M@#iM5<EMsqvyOs~V}|Z)C%r|#z%DFj<YX%_o)37<7s4I$c(dIhw&_C+{%ke)Tpu>E#iOH~>LORhgU(w;yahNo*2~t*u;=kx205z*godocz^7$BZgb0zUGG;JnwC+;?pWL)$Q-eq2vDib7b56q3SsNuygZZoB5I!2gf9UeBrp;VI&|(yf-O}>(jixz<$@@?Qx84opF8%m>z;-gG9N2)n%zZDR??nu2Craw?T`1g37RPk>6q3Qz@cfqilo*)AD8etQ_}48%+3v4BhbS=d<FN`vO*e)wx+(}<8dRF>F&K-_4iRE*o#0Zel4hD)0)IYgAk8;qENCu+8Mi<MBJ~fUxh}DOfBT86G@dKkQt+SOkA$psJ9`tA=cRq;mWdl1TcecB1henZF*jD9ilSWo%2a@RNuu?47qv5cNDlZiw4rhO!H6>Ih7|;dKw_mt>FLa?}yN^H${TkamsrAB1H70h(&)W&FBC)49}@o!f5c3Om8cy4|d3t!p(G#-Q0l8KGMosz}?p{{&_@{GlSY^xBzw_vSqaTlQCQK5Ec+Y*^q>Yq{}ouv2%kcV@N|Axw1Ij=QIO@(7gg3%fg1+)3H1cQKL>+anbLKA6k>L`{_yFhC5Er+Uw=DW_oU5O*X;;!5*c?15Y;0ud3yZ(TsSN?K$93WJDdBYN5R<4bzQfxMFgJjJqrBfykyVj`8j^Sujh$TQ%*<{Y*})?HlX{Eks*AQEI?C9QSxzl3WO6vD(olP!uG{XN`q47io`d152{_9?YDm3R&uXMc$oi6l=8Xf#1!MS+nF(oF`Sy1cW@iciQI{Qr^b7cC^sGhWeR#H}fJ}pQzUV{PQ<QKuXqG0^yT{XOoMyhcDsE)QuSL<}uYRM_J6!8JZj_f!JK#q7v!od?rItncPxCv08^L;4qiDhkxM{mFf7AQ1(d!d1v1IlVkOmOYM?7u+21pauQHHq$*x>gRD@r4p2W;VAqA*vb9zXseYuY#5(E1M-yo_=v69zc^iy@U0$yF)@VOPi!0Li*risW1H8UWQ4XxZhTx5_*Ql0fAgS(}vRo4SQRVrsx?GN|s1XC4JcqMxjs5wYl*iBF=7LF^GJ{Ywh60Rne-)`kUw>Q==J+6zo?9S?ePpspVZ&(rLbq!f(+mdIedjPDLF)MS+V5E+^8$#>k7;!PNZnrHTTlsQG-t;@LtwCGk<`A%dFcakK_8b5m1l{B?32C64MxTKIv^Y5>$NdISQtwU-d<4k^;IA#P&Z}*m>UMgJXvqAfFcCi!X7Rj51pP3r*fT_O%Ch2R9bx8MGJOQeY92v=)zbtM_nSZi{aE#$jrq`^}Nn`sub3vZ-Kv`U=$VysLJWbs7ubTXE{WTEP+7Pg;=yf(*#I)z0r~A8M}Sx)~>8k8b$8`JQd`x$5+Coc{X?(WKWou=&wTp#RYaelUc<r6ju$DdcGoCw$%j65PAaiJ?Dus{!Op^V1Fz0fYJ`(eb4rkO@VJBilZq4LU?c+SH@lt1*_r8?*`y>FnII0h3zAbQQXH&M@}4+rTfSul^QP^-gRmtMk^WkD-f;{tq4hijD>q$4QX0*{xLZknJ#5%H~ImOnADPx)AV|IPJd^QSZYX80^z<;4&|cAN`B{@>urA)wt0u+Q-)C`1JjUp48BMILPmz{AyU5v0{2<XN_q($jfHl^$IUy)t&=LpW)SYhDnpUsNxa-n0|wm?=6snlM3Rj%O(Oik(_>_&!!g8Vko(}tt+ruJDld7x?k+JY7(6Gb%;&tG_7KYu2^7HYXO?TR)mD>>QzT^Lq^FT_TTGs>xbq&PgeGu<2=#B=baPuc@K-$ot1?b%&Xo~8IHu3f?X<ZvFfbw0nDE_feUdt=QB_VrW3T5SSY%p7UdLkPb=DUXqc6%BWdM7Mr}iX6*HZ{pxc7e*vBPiX5gU|Ah-v6qp~)N&oVnM>Zo)M7Z9)Wy_L6^MJy~G{Dh)FfgI|6~jK>@T1y2;Ar)Pf16mpp}N+94nc`vsOex-htW0X701h;1&x+Vgu8vC~P6ibM+%b<<`smviAa)xr|@~seCW7Xt*{=uWNc?^1bj_vP@{i-=i7ytqVE53}#GQ_Hz@^d~LF;oieOtY1SM@wQjVKT}@E1Oe<@Z91t*hStr3J<lGiT02&T=g-qJ(2U{*$UU?^J;4{zMdswN(r-nLCP#FW>P%S(;)WJ@J)q)Cy^$LdAqEGO&)es@Y7iN{KG1d-MuTy7K+ziid-F{2}q{NsgOOTAd@A;b5aGyaCsek8VgVvGVPEIJchn@mr1nVKbB7Dl;v&+5nv^}l)b0UXs$B8@{H8lCeVdMutUbxq$MM{1yO}7s;KxcwW#84GWh=0sflhJ&%;O27c9BCynmq(4V>B(Ol^`;-eS!gr7PWno{i5@?OfmiEp?U=;W<h@KS|G+t(0uUG4NhS!$7Y#`fg7@4kJ7*l{>Egi6E#!G>5&aj;d`4I^-FN@SU3>dKN5oF%#Sp_zL?d3s_MJ4G%k1+(4p19$TAZ2MS=9QPwdg9|j|v`g%7QI*rx&wJ0a&=PipY2>h6n^q_yTDI}N?<^nA_-_A=|N*p`k2B@HtCUe|~Y&*5&5Ff@)QHEcH*qg@}X!D3F%Npg50DXMxa^U9&d3vn*p4CzSNm^M;{FpLysVJL^LIE#3+aMi-_uWgwi-}s>lO8+8)p3f?cYULcBH9Z-e$@-VWweXXYq#)9F=L{jy%>}F&6H!XJkxrDoVLx$Vte+NWlE8s@1QL~wBu$@OD8Jxv}W6^3aWVTVVLZr{3dQ8-`a{T$}C0oJeal%i%u4%=nin{Q(L$W0l+zfK5~&2BHKh!wmqK|%lb;t>tHEA;pM)KJ`%T9+CwQ14;U`YSv=8eTpDC6g{ldfA^19QmU=f**_Q+*omA<FkgG`!HZbI<iI-FNM^*kL<07~b#7nrJ>ySz8?&nZ2q9~;31BW%}FFD&`e=x}Lc`hL1B61<jTw+~KRvjBthxu8t9a^kUG(qzpHP@mxfLMTyOLRLI6FI$DuCImwSl%_uF@QqWCyR^x;he6*ycYSrCB28FgEcA+dZxY(xmE-!1!j{Y(CjB_$c{f&hrJsKiCsxuagR1x&}5JYXNT3++MrNvK8rE+*-T;*VG#E=umn-1&qHmg6xB1AIZd9o$9gYFWiH&w`?i%%fo_q5nr4zTj^tyYOGn{|Q{mDMUg0{1?Xz{vWldS4>!AS;#b`ET2u$w1p~40|B)hRWiKmSg&Fi>j5^6a6$g!{>5ven`tGUWLjjB`y21&~RcjmL>V;8|1R&Lj(sk2p{gWMxzlbyL~^l^?QnM#$bDYUQaAw_$PNe3)FOHE%Jwc8AS26QTgY~21;;nA1tn@ww^Z-fZIA>m&XpTJ*|iu-3N`xx@}96I;{6_~#$dtPJ7;8ZQ#&zMt9STVQzV0sL9L687{ob#;nrf|+27x*5j@v6Xz@w~tDoZ#N=D;|E3U*}-4V~Dle#DotS<qQvh8^k$a_-i8Z?$)3cy;?tE#ro*agRrTk3<^Yu_E?i1aHuejk?yh_ybYyUhm?JgI+bT?$RV3Lq+xp?O+f|=?K{H_q&>QK+^On|ha(SL2?a)zQM>QbBtv9Lk{TSA2$tZcRI~oRW&cC7eRF_~H3ZKG4QGvpsTmnC25tg9c2)d+Ovoc?Sb3@YSj<1&M;VgH!&oeQjzUV`xGg!H!)(skg!9zIBrZ>CSiK9RTRlm9?E<;Iy|t`5OoSHm!~HwMJI}7VE=bvPy**4K1n@vg+!$iA=2ESzbx;{G0OetaUI_s#IMP8%!uIG7IHok}_aH9%_Y+_C*SqSJXZpCr9`!X5W-ThgE$bBWSu0qRTR6%4c2~JWop)yt^LI%skYA00VFB}X8ogL=oG63KxMaD_&?!5Dv%7W|wInj$`wsyWfmVF;eINgAZJ_#uMk`uwOpTks!+QmjlzYbnryCcx?io}reB{9HVF%3CfYOdsFq@`*A>a^<p0a2IgLMgC2z}DW?8bPn?qf#Ij=h5CPbI3%l$|JyvZzaVpQy}k#DoEYP1WOVa4Dk>xM=#vJm)@nP43cCWL*RVi^@yU&gtZKtYRyR<^>`Qy6D?|0-?Y0AP!_otM+Mwk9L%x(b%tNr$#&Cqz18?VQ5J%4R0JRo|03K+_S_4Fb4;8O)yE>duEfkA`4?bCwp!9?-{LOx>}h=!IDItb83%Cgm6nr!7Wo=G5N3-;3!u2ENcKP0IWmcMDmw71G%BX<jqo~QZ>stmr*w38Omy$;l(&uao7B7(}*xoMj47PVdZm$?vHH9G13%t_cTT4fAP%~4~ujqZl~oeAFUB%ld?*3x{0f6qJNdn|3zJ^uJt*sD21yai@pZOWXb1^9xnP<fD~34{SoFGaH8-N=izj#xk(=ns$khhK=)q0Y43iNwop@!!ovZXn^`BlC2|7bLHr|(^a{yi)iuPYe7py}dmlc+As~NnWy9o4;P3GH25y5qLA<45<1p|uh16cyG;1x#Hp&h@#e*eVFX7A7!Ue!+r-X}+B695gIZRC9BA*t>9d2h3AHh0ktqX>goz!)8(}Q-<W`AAy_W#;qm;FKt(vJ~uJh<CxB0(mB@;Tcy`6B$|B(N`TV1G<A&vQ?E@iM-Au3$!+dwLSQ+Zr9!+yEWA4-oI_;#<&O%1PdB({Z0vy(eMgm?WVnv~nN*-dUb~7m7ln*kE$yD+2h48SC?0DxynNxx;&8WkKvHF`_2x+rFqjKldNs9&BtQ({vi2<Htfk3Y3<XZ(AsWl-c(=n(34Y%dhG^o7%?w#>?#K?Yj@YgV&XkS6+|hnS5aR4~JzTxj_~qg?LEo-iKj(J|WFG@QLkwK!L#{Nd26>W~>cu`HwpIz%dO|+0RY!jdC*9U3Pvj((-Dpv~~dJd+o12QI^=(jIE*XJ}(a9TiG-|sj^)rm12MgbSJm8i4yf)g6bkMTHt_yZ$(B75S-V2e-^j)ny=K-$8Ffl@D#(Cpv0+V8kb>AYEeyo%pdTC!c=1lfAdKcs!Y>QMNM42a2Y1G=Ojo~Nvh}yuZ3_O-uQW&Rk?RqHlk=mic92~L_Ke~G;}6JB%W!J$3)0P+F4BuE<>(0%rU=>K1+_34WvWWbRlchfVhXo!(WD_SF-`sHR5v6SL9B-7x#i{S%y_L6u58noNfAgu{{OHag)KmB##(&90MF;pETxqp6>Q|Ph_q`{JeA7prkr2Dx?)m^EYW6`b5xV<v!qr>0K**C@YqhH1i+(A~M?e$-2JOUR5^c1VDmZH>Pj+Y}8bvWuG(4&LqDr^+SM^%p^5z%U9Hx7fie8JD1Fdo219%h2wz*2%WBAtgaSClbb!`$7QSu(W{_z7IDIZtk%P$n6x8-*Rq}SThblnERLn(iw{3%Z$c|l!-bgAhdI&zM-v~+5P^Au`8|i~o}-CwdIlgy14?q7oZK<Ode7&;_a}=RVP`kvVvsTS7N7~p&z5QEs9zwZjjW}#XmP4l<)uvF4o%~e=|jk^<8;W`=?Xy(G#y}$DCd97aT3#o4+B#vbJ3fnr2^TH>#inB?o9K4eZue>WHyStEf`Q}`FtLn$OK2<a7Xdd@QC>-&WM{%;#?|R)-{s2U0$9{9Ni?NgLGe}MMlPbC>gqscST<fE~J=syxYlD$MjusUl4{6<VIb9g_g+?_O!ZtddzpzcS<h80}L2?w*iSXJoZ&tj$=9@a}h%?rZ|JZJixoC$|Jj1X^x1Fcu?)5XJVY44{2QHu~YcTw&9?J9aJNYGC_RNiQ7GQDKYf0M|C1|+MCD1tD6ubNkPuD-e-l~@)RdE$DuaXKb5<`Pe_oBLZ*h~3xWS@BWUnLLc(fyQ}7K7UlupTn3TI3%VaT69>rTP;S99qML&t?@iDJ$hkx%kXLd~WzLTp=dj^G1f>%}K(av`ZAEV#;bRt0NK{sqc^cnBT6z$0#C6TlO0;4Gpf?&aJs#oncr!weSUMh(PakeyT5lmIgS4<u+)zVNSGHK&f+XmY{S~_t{l4X)9=;?|IG;~4#3Ydv|p2$rpIbj1H@lw@M_&&Lm;9%*CEOq%I*(<`o?j*AWBg>Y$COX3PWKQ(&ppvL{PT$8J#`nyaDlO6M_kjUZT6*2S{ey}6nA-YWr*HnNxX|X$$#i}~joT&e*4KTGOnb907!^mv!!TG^`TEWKb^8A8W2O_OZeKFg?O(;*zBKLpQhF>_cUlrEQZir&gk1x!Yc+c^IXyFQL6nA0?~H-m0tG43N)20=)_6B<omVdUEuk|(Gh*NYJwNGE5wYPloy2MGwkkiNp%}}Py{dG)`?jD$|NY*F%85(_izK5zGWsg_4Kc6FX0Flvy6pUq6<9-n74vu*G5aSK+==2u0*(;{ZQ(t1pMYpK#p^S63<FIOpH*D01T(cc$4f87kI!XEo(UMlYK}mqP!DZIri=s0R)ps4bzwOrK?&dReSf?oe|-Dxr$4@#AAWqD_w7;%e*g8`@8;)!tfAsb969&vH;p@Ttof!=n%uvzH^(BP^)LEw8LFY1WA*2s-@gClu>>k`4gkK_EgG9>NbKNXtqF{)SI0~rquVmfp{!xrzlSEo9qSNtDLr(RF3zRalZzC=_4yf$NA~mmdfcb)|MF*0_w)Uk`|0;ze*5YBANlLIZ~uG`wSdljXz0D|iiFk4q%nIuN4KGh^*muNld2SZd@$p&BHyubJ=mjTNMUU9KmYpW*Ps9QFW(LW#>R8Ea<||4^ZS4Nt8ro*V2ix~MYXn{Ce{9FO#H`z#%}s!Y$(UUn2r&A?wTffXP4=5v1L=$aEIIRDJr|Je(K}QgoD+B9)X(TSR<A&kUV74CujEP;j@Cc2;i&6hWQ%)QFAXIH&3Sq5j`nq89DXD*pMaL)#V+|Li4vYO5Wf+F40BjwG8aho8J-0{>EjAuQxhg64e1C4M2ZaKCR38I*LL+4<Xy2rB_3-+kI>aWPP=Yb}(zi6BwWQO8|fOZ2t1?<8wvUDUH_GORAK#%D$>=k(E(%UR1);p=X-CCmJO2m|vCCL3}{at&!U0(4|;I!~=NWSZ+pQ5-~*raz^zunoURk`G>B4*m;l6f1zF}Tej_4vSBMVWP|H87Ypc4A7j!>vD@5VMF*2NHguGt{uc#iT8<3=Y0CK~=Xz~=DFik&GE_rQ)69%Aa`;I@QR5_Vl%}HyHEuGEE-%8PyggCaIzD{UVJ4jH-qWd-EkQ#bCv61#7PsX7f!N1aRf&C`0J{+(Wf#4|frIlB@{arZEJ0#}sy7+k%ZJ7-k!6vgrzSU1wV2oOpMQIQ|GS)<YN}ASKw&Y9sJ?gZ#O=e0YtlkG)Ha84*S+(ETvymkWhd5}Z7HGfV-C|W=scL#hXM!CBj(SHX;jH+nC|#v%h*jY<-T4V3eKIAX-G)dBpxzewN~Phsi7aS@yKIx4~~XFPBbQj+d#(9i2_v_JS4<X9}M0r158cj6QNhluy|{)E-NsN5yBDuRl?K{(oL}v!x7m{4WR=_nIm!+C;#GJE;h1b97P?6!lTI;pJe#gF|ZoELG%nzkYE~;R?aak|Gs39lOCEH76EITg<_%WJF%l}xa9QeQR{|iWu?h>uv_N=IVB1eRlXZ5{jg7?nkcg`cGz(sX>Y22?lev5p#moeqgC!tUSk|GE1AeQ0f~*Mj^+|eWXeMJj2~m)d%E(hQIGvQ5^_yVqoX(q>*aw=ZVO2SA3m!vYfe1uY$Vm+?zt7b!ZXbY24-543K7%HOFqWZK@v<88LUbsu;QHV&Aj$CUx6_4Za<iLk==@UON)Ae!|&`I@s-kkP(25{KbNA(IMnuhmEqroo$~yhGOFdU4@F`j{<mmK9hjf<@RdoO3kNjtuOL!h18Z?}Xdb`wjF$P|F)zXc>js=fpiWcO3wpX=2$l{EcF92VGOTWirUSy&bc}LSfoog>gM#W=AbFpF9a|j*Pve$~y#Z|(u0rt^{Q^6k9b)Jw{P%oDt3dk*;yqvs5b%y!#VBsFx$Sd(*u)l(*lVic*=N+CsEwD=-~%_q`nql{#kGS~&|D_)s*f1AqWF(?N~)zl=dlbbjtxmq*unGdvHtrbZJ7_#%jix_%cxe|EIh(bmBJGhAX}O*#8TZ9qTj%|7ohmeQS@ZrtleD#p4PzFIY8_gcj#q3$VTa&)#j1?XH@S`xW6HeJWP^>c+_cG66G<{G-jXWFKbeG>ww?hugDf8_-R!?hRZA0oRW_A0*j|ca@{)E_aGV4_O`@WhH0iL<oNaXh>x^;?^gZ&7g>WIfnB_=)pE*rY+954Xyu{<$TbG2^POQO_-KD)Q|3=?8&XrVZgE(Ll^MH%p>Y#0^7N+XMQ$N(o1I?24O#ULY!kPe2Yg2%PP1qr&C7JA1O+*HBBclYhx}yzul{}r(E2ITF8%tn*tRE|3~NN95a*E44;m{Pzwu`^Rgn_?P#O_w8<05$#(SL`A)}A9lnL;ry`MDq!yyV!-I{r*eO3#&xsf5GrJ9V*nukS(L)+kzy#aPNltU0Q<`MxO76$v25nvD@LR>zIKqyB+ObFI*9;b};LndH-tu>q*Gz|!jZE!-VJir48#q>xM%`vi+f+<(8qmvNqB6Z%6;jXeU6`-PFU_ea{%3g_vrhs5kK~j&=fJ6`rxpaI<WX_F-1UNOZS&p)>)WWIz?;GYRfk*}DMEg|Vqf?ionJ(-b9c%*GKtf^$s;3z}dtw_fjYVj|7DZVgOw@8CSE><Q06@rmdK0yXzCRCE(vCpw$Q{sL5BUrvZ`M4iyzU@O<IPUM!X=*cd6wBf^Iw4s1ucSI?CHG7_Vml6u6d5YmrU#)zUhRaiwpf~GQ@dKkLjH1mgBNxSPM-#k05!jPD&Y6lszQUvIH8e2%<bt$FSy}p2<&mr1RE8H4r=CL?bgL#X06uyLgLj>o?%za$N@1iZ(b2g{l~!xgygpB$w^e+R&~>q{EDuJM;q(<uaR-y1WgD!Y(hTN^WE?qQw=t0qj!Osylu>7bt_R^>!dYf9K|$=NcwLSYX8|d3?By;uch00YD~ejxkK0V_mn#D19C@9Gj55HYNZFfg_Feuw!hY6V`fvd5g%rM370_=K=TxD6B}3R(y0S)+|eCIj7Qrm;^FRk0~3d%``hM3<3l+3qxMh(=%B5U|cFsAlOAZaX$wpIA0B#!oCimFzIVGQDCUKt>C(?PqOIsiW)&+Cl_R=Y@!nnao30~@cQb4hVu|MMzf&UP$$E9mvQkv%PAtp)d(7{i{Vr>2p%?{ia4M0b<XoQTc;WIQrjJ6Ual%3dyKl|yjHm6zWN%cHfI%xV|bybN8*m~-qQkHO55x7ni?!i06Nz@5Q)a*hbKD%Rx`?B=yZRl((m=YNoX;rp=oZ2hoYm16k-ybF@ZTCJAR05P@}yKviD3O3fH-Tx(l-e$qeOI6Oh3ts#H363-Z^Pr`pi3IyBgMRo!EKa_1Ae3F!P$41?f<G(MocSPI(0-du!iF#a7FJD?>A{Gc0i`RVuXW2O}*Zlp}NgGX%pUW~d=L``GCs~yNjJxv7dX+BaJx??&KO@*dD74#fI)x2nf6T*g#joU+iB1&dp$CzkqvMtv1!pU^jj(i<BUVS$T9DwNAykGJyWlLcOiJdx118iuvA5qCAn1=aT$BOO2?IF1*R!4nIm0iU2$nUfS`*9JV45KQ=qJcvh;*|b{jCjqR0_~W?)FBLxskqH4S>n>C&+{Fgs|9zzxOSinvyvY5C-UxV$p$TVicX?7UoyKQqXjuChEqGrE<?_*E<+6yILNxGiS#oPW9E=>>-{jx_bVfFN)Yp9vm2>AyBp5E^Za`m)=r7QC&dk)QAvz5G^GWGHm*BON_>s_Um3a(=r&gkZYE687gZN9j{auzWEXduV^mB5(T_EytXc=x3H()1w>yS7srYq9{o)w(cQ>=vx`1F{Lfs<~yICj!C60*-=t3QIJr6-B6bn6lMIn}&cwe^^EOt~1>A^YJlMG`uAwj{z|4U2YfIWeunpP$ulR?i4%}j%ojC+0TCQM`BCPZBqUTs5!ekdGarGbSq?6>AKbHE}zQG~>sc~?`3hR#UBfJf;0A2#PDb-W#;O!2#DQs0Smp?d$rz`aa6OmelC7<!5tYbVrzZ?B^SbiEAfNNbgO%+uqFJhUO6&+2?(?yWLUoou839{+DHc^)8^-6ZO@E`)ZD^Z&<SBO-UIwG6DRM$peXFm3}Yqb^GD!C_Mg%^KicrpaP>@vD@i7Pd&y#vDHAn&dhuODS^Aj;0rx(woA}l|sap5UxuVyuz2GfpijXE)t)6zI6i4i{ad~rB+9I!c2Y=KD}At<71L*ciB*Dy=8Ir{iSj3SR}>k0$xhldurU~hGR=$y#@!76lrCgp+g-)$7OL!C#q~uTB2612qki*b&}EhA_M_t=*$!1`GFY9pu~a4boAz=9Q~o6t!9K~0nWQI2*(t12&=~+w88a-sZ+%1sC5deDq>d)P<tsh1M$Y_yJ|{S1SFo;?wAz!7ylFfb|@~Z={<%pVMS9-1AH5()MYvu=^mgA9izCJ{G_`CCFcU)=F))vt-ZA_lT7(f={h4y+0x+W<$ffFNo9Z-4Mvc2ZkNcp6>@5c_nE|@S2WKYr!}wM$Fj(3rQQS3^^y^67<28GoX_f|C?(#m@FdANvTLrm5z}>Q;vwdeT?gUx5&lf*`D_+aa?EFq@K``X;=(7Gf<7~@4^}-fAKB=S9&;%fY7~$RVp@^F%VsHoV?=AlmGLt1Vv5s}V)P(GE|vR@HlJz!%lK9P%NAz30R7nGYrF8$FyrUpaAB2iM^Of#?QCV6Rh=F00SH}rN^9iSs_k9as$w}E{CyDD(+jKdCu^z&7!$TFec~jn$7*(giD7mPt%1WsiXEhF&u9O#ZUuaxS#C4+$X&1bZC3l#Cs~9GcOV7;(}0NjCwl2iD|O3IYl8F+_Vl=>f?ImnmjwSJD{f$^LMrYfu_J;ZNB!trXd)DL%@Lu3n?fGe>L!O;6<ZV8gKi49KdpxYRfTA7SxD+0iWh-yA<wU33}Y^coAk&eJg(#YuEQwvGsc<7=rsDYNvhL$IEQSD>M%d6)J4nT3E(9EQCf95rc!81sir6@i#hAlYaQYmLV^`3^S6lU*Uyh-A(Wpf?qFVv?2eEo5<&wIwaa-gULA4`CsbIF-*cU$FZ9G~1GLScC^4)o91|-hifN@FY`xZiYbedkC`N5^HED6<HWrp@s@%Rd7+CqtWlodl^s?d*sa=LUdEd4Y!eVvIDfNFDG?lUn9s^zby2{aMQ?>xPBb#T-?!6l}*y_j>ZnR!s$1RiM!r?myr~)5F7i<vHiMM%7qpJ1tWPc-z32?lVAwjRx)JeUeLtr>TnA<_5R5o~LYMrWF@SrVZ4@uKwl(C4ezcx8USZz?d8R!mZf(m)~{j0)*IoIi#!n!eKEpp@gpnUHFXlaOi40(GF`FcT-%wLqyuCcOrs`&0Fv8i;k$bNBK;MG<RQVHxjGkSwLoILQKwQf_*M?s`gb)FM++<o=E5Ay3Ar*;gncAJ>+A)~ZjDRLy&yP7w(szK2N(c)=p9u61sG14egjvgPs1CCWEJC&SjNN$|keVqo2XHLa8^YqR_LFl0QrqPx)Sv_!6+%#whfy0?lDj~5vbS}gD6>|K>&5u!{nH;d?NrkO<f!?bxtLOIo)w1fvV_E?XSN!xaJ!i<Zf@RM&JTTo7K$Iyl0r+`4Cv}g&kF^de0RRy5?NC*L1WYXFCS_-?QyTR{9~VITsY0L1b{{~>V@6Y+5#Zt<)z^5zbxzU%%&``N^ee?7n{zHhAjQkw-da=|V%8Jm_w=*=CxIU77-W_EcU_^s$iQDBJo2kOoP6gr*6wsS2r5WZ38<>l8iMaU_>XOaawZf?k*grLC%r{oD+EB}xkXHPx^ev)EOgN19K8$CO!3J?PphISP#2j=gHgi=Q{mY<l@i}^S(nfVJV=k2#50lp4#2pHE3>O8g8PvQJyx=|ygjLSIxx>`+(wZG6_P&f$Fe54F02!418<T2%6UY|9&IvdR61d618<cvGXfOVB?PEYx?P!cgJ}+VaOB#kzT3wG+B`ki%)uN9ZGbaMTSpn~mZ7x81s9C$;oV>U`CU^mnDc&}|HTJWTwV>qbFubkK5LCQ7?g%VIf&y@bm(8>F2egvmV7vKwnltWet(q<CjoGMcH&tJNq4;)(VxClN=G@!c|$#nk0)@P++@MJ%LJPqrkw~y20e|R?wBIVf-=IJPAdsoO0M&0|F6yA*e_Bz@45+{wvof^62^izjeH?_)7##eba@w|H|`Xq{TGEEopOkJ5OiGtnYj?+ZGV{GpC9*+Zx4s3VN^ej{_$gB{ugQ{$Q0$A;F~Haz1hC=V4_pzCBM=lZz@#!ji-FryLSoK_Aq-UupwVl1CNLA^iLQOA@})@VHW)+Lm{r7aEg-3MIHF?fY4BDmuYWtrRsW}v?{jqJ#>7?z}L)y_bDaAG6=TTKYmik?!6JRN6R<^NObDHr7w%f0UDqt$@Kvn-+oKzQ?C2|Y<=PdU&UCO(YT6-AzOy0T2C9`#v7<z^}6xPFeVEWlb`Mi2s5A`uMw#!vkFC<mtj(o7+i>lJ$J4WBJ5AlW{=L=Ii*#d5-t#(F%~VpP+d?32zejvCf8uRXy8pi<XI53OjO2F`R7Y{9;b2WW3!bhn1S`wAp||S=fF!|8n*8s44~AC)Qj<j@Z4A540X;7l_?xqP;JocnBa28uREJo(Frkgk(6~gACDbxYy+>nPlR;7jBoLh+#9ZLb6?UxI_8K_hUJH!v-?jbcRHU#w2ukI4)sYHWjdIQG>L07OZtdzy0aE1;Uy|<zuQuv*j%RZ$p`@gyB$=3-I6XPFO&Jk;I?yb=5wl(7$ZE4Pi+e~w_o%BgCCDIXZLe%^M7lQaCL$jHug4g{>9{ZkW#|QUN2J>!<MM)Nka3NSkLkWpry$LZX9!7bV)3q4~{wuf|z+p#0dAxy~-oEjDa?D97HlM-+(^etwVfFhDs_#jhTjtbI>71o;4(;(CLVssd-&g4#s7UaPz#s)UQ2|IL+(1S{i);ojT6~22i{R*|<d=X*s@_XB`@WEA*+Rbk4&q&{Q9z7D(j)O$7@?fj>l)J}F(r-FH3)yXZ@d41}?09nOu^E^#l`bH{jIWioI`XcQPcu`xV$s4VpTwAl03$A$v@c~OTarCVUxi`j1MQ3R%?Us%U|;Q2=uz*^2m4}(#cJDl+W`jWl4G#PV@Z<4vlX_g_;gGYnF5Sta0OP5j;ATvF_kX0;m-PlW6^%&?iUv)HU*uuOQ)FMx&f$)+nkO)Yi>z^>2qgTY6&fSRtfVz#3PL-pPk#>8BVK7;S=9~9B^Znb$Ou0DIl4()@st)yKEpq(PA{wn93=trVAIPprs!DtjqF=T>VWya0Pt%EjxmQ)soore+K1F-cIW8e;<sp_vxI+8I<rkgV6PD^9Q{DF^oa_Z_x1UwwkiU^}P)U0!R3Gmt!x<KuE&k|*$(J=OsWJbAb(!D4b#H4ztdWx155QY_DkpG?*GJ$O2AU$ivpBB|W@<y<3ohly=h72U`D|}XQtj)IUXdx|V^L{Gmi&=Jy%?75n6B?P`SZJfeEaREKfakCzV!NRkC*JX_g}yLZhroTFczNS1Mlq{norBRHq}vJS=Cnz)#5ec2j)=;Pef{=+x7c5u5@{7rI{+&^OB~ze%t?@{SZ*%4?Te9wQzmx*7;}`$L`<#Zwjw*J7c&XXu)2!8P6|#jwr0re+>vYy+yZjvN_6-|3k|k0uHP@EL46U_^s}1e)Yc1R(KM>+$q5e@ZVyVQaiB)4j@@6`vr?;oG(NN*ZBOOU;^qFnxxI2pSOSisIdfZ;p?!VH1HqGmTAJbxlvl&^{QTDL$X2?p>xkU6#+Vv41f9dkwHA-=<RUW$2zIh+&?}xQj@n;J>r1}!@c$`jWzUh|L0%7{QC3%{`tv&{L91+c3}5wXMgQ9d(H6|i{WD}YCGlU)wiFBo2lE3=#%2rV?(6^#(F--$M$O+t9DJB?|?fMHK8))QbK3@@F+<968DwaVVBJ1&(XuDi;}w6-mMidq;GR?8m14suDpGRVF{u_yGi}}=Wr=K)s85EqG7tO4ccQv!U3-YI$2Wd8S4f^f7jlV<;l7bL^#GA4de18Rjsl1-EaP~s~lDBAlInZTxLc(1^(Jx=}*7^^4m|p9`^Eny4NWUch>9dvV{9FmWU<Rd5Z{fUGy6)ECY4Hv8m=THtn2$m9WHUPS((Q&K1p)j%$^R1AIWxv0<PszU+F<;*lNd;vRf@G_Bv5_Xv+s?RwUYlFa!-vm?5FbfYpU5{S~=s%^gXtbO*qKi8{KpQL2n*wMu=7eKn^xvI~jw#{<A7A8=ctRjkxJC`zYj!C0N;~a1(ruXJ<kx$H*go{>0lu=_-iI%3%zQqlbzYY5nEUm}|Gu}_9NZ+`RuZQTw$gFXHmJs!|;EOS&b^w=Dfl*97t+&UJmLRP`DKQN#_X7+ubRj;%4%*4hbu7k>{O8}^-~av)#q(@VgF3MJNDHI|bU61VzkN7yJ|x;klp@*nU?RbR8Ya2z#M-0DT)Zoj!PF1|(1+Hh^S}Z0I4Pe<p54b9flV20qIEIv1e5o5lqo$x=le7ys5}!dEtMyif~BeH$+wZnV+Ie7hG4J!(y;1BO+yq4+wPzMO^E-QRCDxX<1~i;G-+6978ZfPf-UgU`O`S&3u>Y&C~IOpK0Lx%Gprt11(42*`)AMd)PPAqIY3oNVkUx(>=;K?3u_|yH`!JU9@nX<dOwu_d$Gdm)RcrlQio8O2OgMxXBkb5HT<nFqgAG+X@CMuDLF}5gFzImf5A&U$*Dl*wqS_X{V{5`>=nbFWj&!wgh^9YdKFZ3FYjk3Y&T<~1yMTF=P!6_q2Ijga?EMh5!B2K$NnaXJ*Ro>8HM#OL3+F8p9UWuW{ot8y>NpyeWNt%P~#5GiJBKJ(j}zFomA&EcW?r-J4EY-tRB!fB=h>LXuDOxV8%1t)8!o4mL{YIhu_OQwJt4W`FDJ$d4Db|mGO1$r<YMJ&V48>xbeS5JQ5e1`qyvY{`nrJQ_e@POzK=XQx^XUs@iL4Bqzt>y)pHi*Zl987qA6kBvxuhw3)Nk_VhZ6E&0b_mkjm{+o^zdEJouuj}{o^ref7N^Rdr*AH)cL5A;;_XT}yZ%|veIJ-K^>hAyc5j?=ggzu+5@>R!X~pm3Nf4skyJJ|uqx!=}rGeu4fG$o;9wGT#2&<h2Ra&@|OiaPiF0!M)(~*X$K<x?n3Xp8iV}xC?1z_5P2yr%RMl6JlRm<T%$SJoHEsWvZbyWSo#(<ej<oc0wE@NsnKn=|w<@h#K4aOMF^3;4ruR*mcgVOrwltRI9iaK?2)q{hbK#NzE5x`F9EdjNrTo0D9)|dV&!41zQ3V&%j7HIH4JLVrH{~4Zi|IS)kZN)xbbJ9H~s^_r3pf4}W(3^)O}l=GK@_L%b}BiX-W}wk}UBRUi4jQA)@|t{_grsljR5dIA+jBiYB#2PnMq4Q~C(xt?3tsD#<D<+C%)-fhciX1Ju9x{;6GQmBfOyLrq|e?vLJ6kytp%4qGy@7S~^chkyB1qgankBD}L;TfX+jm;XFTF9Oy^1MX6;f$Ltak*}z-iFkMScf<)xyyvqNJ-brb*Y=Og_@=rnm&qY<Farc?+I0tslh_B)ayG6Zkk1-J?Jk``y>-7J#bk`GEm$Pp}k|;wkJCm$MuU?j3z~z>qF^f1l+aooO)HBeV4@@q7rI{A`je5_t?!tQKgJSZzc3=sGzZ~aL~@6_8BgK{)lWDEs(|9A8&LTi>xqcV`la+*!_vm@H~VR%0!NYMfV`p=;gELLH84)!wCX21q36Q#CeE--eH+azd?RLE)YE4hT9;fIxP6|TEjgzuqlAyvH_ugjPN54v$A49!a?B299G%p1EpvN8x8d!ac*S}*%iQhVha(dS`pxclL?RcT)~~D80M5XxK1C5d{NGI>6`E=foVqR1M8IBV{(a99MKn((I&tsBoV+`RcKDr9@z%nWnogV`&L$wicSZ^s~rQZ9T^5BQIlV@<WZa_m7SjwcXAIn#|eH6tadbIy@rFA`8)F>TOV0^qx(UeBRncomxU-)!hp$T4MT5WWiMo?L^wA<AQ-d-tcMb1tAtcK-~8Lq%Aj^HK%z>^KEi4yiZwrmHTQJ%eu7&a&l1Y60M1vvHJr*dA9JZ)Ebg}7AMjm*Mv+wIY;FK53WYmBt3`HQ$Uj?a)v%jK6mpELKYTP16}?{D@|U;4D%j=aLQ0LgNwl~kA%tD(TAo48y5nWJ9Q32g(^_>|4ViX7#$b8QT-}<x{W&SGo8HaEV(J84eVMJ{#UR!FRXxcGRI%Px=e)qTu`g6w`MX8WW@!y~@e6&NWmNNy_F1>Rwm!mF$;|B{X?H;aa@Pa2bbwx6mWW#fhlJp6|MEeQjjm{!+-5v4edsGyDLU4eo}E2zBM@tR8eoakvHR|#F*TWMcPuq{=s+3P7Zs!6V#+CfjAnh3e6d$n7lMOf-x&`+PB(&g%g)Ot$508pFsq$=2sPCqYNbLh><M$!*%JF4PH}_GJYUQ>!@70O3piM>9yQThP6_6QKdgWd@wLoZkz37Dc$BNdSCWzxz3!_VBGgEv6kcyyoD+E#F5s%U0q6w%33_`eksk$ZGF}R3jj}F!=jEx6bG?8P_|1Down298Y1RKaBv6ZB*D0BV+(MDXKqu!bl51N{Kp7QM9kJpx#ozR*752ACDB~sM_N+wBeHZtXRfO+63dAYQLU1A)_sm`y1rXv2a|S4RFnIG|hiyELncT-rXOylBDEIS68at$)yqQTvh{5&kMW+mcWV*!UrMlU^b|kKVE7P}$V8xhB&yAG1czEZzp^}O&H_QvMt)r~ShQRv~)mwt8T`|s7DskSUPC1fRV!|_C&W`=gT@~WT)+}t_7EhhwHmx#@sz{iIVPwEa`WG^?YE~P|?D{p*Th7_eN<tAGrG?To#4T0G`<3eOW)QAbDMOLrUmUzZBSQUE$hmrDh~#0h<xo@4R&Fw-ym+Shj<L#Y4a6*fM%hei`f4wLZFEXMrNzW44mHYhzRsgAF^wAP(P!B;Tg*0T*tn2g1&R?Wy8EC61Lr+PDQw^*S}TNd0sfS*>j^Nw#}Fqq%g*RX0?kx_32M9*FfbvvobYUI`Iox!QPEQX#INTeSfU&ZbV(W4u4Enkcm*tWl=JPWP1}<U{cs_W<FV0ImI^<jN5!H{Lc~YU3Qg95(AB*@b`z$tZxbR+x|i-1%k>IxRcZLk7`m07UJ%956(=`Fbxfub4V@8J0cXm4xov7dY6&_<xx?Ild-kDgqH#F_XV;!$3D9>L)DdBod6daXvm~G)bjgv?^K*;k9Q5=YC*>FWRdbX*0X!F0V;XUqh;>%w=N|EevA;ERCLv41_9k)NFo|p;63&@icrNxB>>_U*Mc-P>MBDfnZ2cJ6p2&#ubcgHmdDT?8eSu|iN(pnLLH;l-UsH0Mr+WlS!-^IHUPUrD=Iyd3LV4IxL099B^be~<$rz<eL)5_OwU;7S(`W{hsp=_|WGO^y3E{F-GA&$Q2cpOVR4+@B1gJW!>f}hV?7`g+a4l&*`G2=RTlyXdweujt3K=hB$iV#w?LB2=V|lQJvOX!sZ?k*)sSJl855*yUYZ9%n7^6xd#Q-M|LB1=UFlKHh^X=dLn&{T@LKGA}!iuU(uL;+T%7MQ51sgQkHw?`wb&@*;L?8sp$+|UNn}k4s3W1Wh)LHH-$gx}cr3uEe)>C~N&Z*?!Qjh7A$MdPA%Mo>_*2E|FNMF=zOYJ364HQG8@AmYsIXue_K)F;NoBSu@+`8uaza6E~5J}9FPC}0WE;1Jal|Lq!(rYq)mjD1~!l&+{6dEfw?F821+JOQrb(C0+S<u1AqRycx&&f5L8AH3`M_wQGW5`oq!xqEDGHi|(d*`B$C5k?T1a`v9A{iQhv`XNs%Cg7;x!#-A^#~Kd8Vfm=TrB0)10)u)@Fb~-wx%%Ch)z4$jS#NNu0w`FiP-vwGX?$D+kDn2H48LETK88+S~KbpR;qmb$jx{J=XF?1?CdbOz9=k<f^n}L(m=5T|I4d;iIow{v7uH!{59QZFP`RajbG(&ZD9^IC@d@-n!&hsXuI2_ev`Rr8-#T9cJ~4ClCn8vBhMnU(gcb*9XL4fTHI1aNx;TI>tESsRcFh4A;a*DGB~-&8EY%HD3u!(&|#iDtnymav^&76ynPQ(+vU~f88>QiHAeB!%FR9`b6fiKg-im#b?0z~SC9QuEqG<y^9lB>V+dU=Rz4t4L<s=G`_!j57N!r$1Ykn(38IM73S={6te~5P?><**Q8B*TIpo>_=EW>BE}U7(Xev54&YeFdvLrZFr8;rcIFKX}jS(v6Od@g&uG$ldW9OKJfoX^|0U)IOm|Mt`3G}kHVwA`wtX`0y$gzj?8=xNHx&Mq;&uus%4Q8pp;KzLGFv<j`ak4);f*>aL+dIi=+v3^`oa_9o)*wZJCHPeIBIz;mLesM~MVwMV>GGxFTMb(+H~|L-mkYV(Ea3h}5VpFWN<801cFIVT93jbw&?u^L8_xmfdg`cfDmM>0qh%OJ)nV^O<l_iS*C(dkf;4MtJ2hIo56$D%P(Gef^x6VQ(sak|c`UbD>04S`R%P`RX3m!vDQF;=fbkvOu=$)^$jX*zX`oR9!{t!Y{bQg@N4cL9<x}zy;f97x7<J5599T;Dp>rOE{5G2kjPt$u&&JRlDcT9EgSqvWI&PU{G|toT#tq=6=}Ip`bM$Q<)2K>YJ=vnpVj+AGB~YHt^7_VanmU<$c#l>D%(ZJ_8dsg8OQurgY9;McekgbxW76@qqPR_hMWIehH$qg_sAc`^A5^nQg1DVIxMM<VB(#WBMj&Hw6ez)8l8{}OM(8?i&-K4FPxIH5t7_95MOpO)D3D*GqR0=im~vZS!=5?GrKj7RXPpa<^8mW7T_OxdX`w!bJSWKe`|9@}<kvaA_!wgCwmISJM`cJ-Tx+f`Ij@OImkR@VciVgTLy`)=E`XalZ)!D>!knUA*Yu4Xa;#&dQ2_`&tbQLngH3b_-qnznK6Pw$IzXNu7u$(WU$klCif$tJ#QGxb$Wc!q%4*mh6?7CgTH+=v4NktBw3pLVB_TMdwLVE?5@H4FKFUyX1x72O?F|X=W0r|jz~a?#0ynuVPpU$`3!IZZsdGZZP|K<Vj3^8w+?z9$@yvnymX<x&hRMXT07<jNYZTRBnt=B<@H(jEMSzdEL%EAUT^w0GC4+f549Ap4{fx($ihfq={t8l^@}x``C%V2SRH{W~pJz>-KEV*{M-C@>-|i}tiSRx&V%jbdGWpdGh}>zJ>)Kr}kr?LhKLl#`J+&$N%rqS;gh?=ZPBG1Uq78%yi}*rQ`ixHxwC)+yGkglbUSSu+Rt^XNU1*a$=g_q11VpisnU8iWSd9)96XfqT%{_2m?juFdzr9@NPbEr|ac67kYU8boOvuL2T)_tF;gWRQKtoeq=04G7?z&Mp-iO?SLY7}=*<|H7Sqn9g`@!r9bqQa{2Vpl;9J7xKjF4y~+|e2n*xMxxWXSR54cWz0*(3ZB-4%_tzlq=WHNi(`uZB&FiR7;Gy}0krCR3uOOGRl6s0XS97bV0CQh@`R7>{W=#^+{{lL2>p!#V{17=Q6H;0N#((=@{T40Ro4!<wP?$Ax1I(&RhhpZzrjTs-gQ`Cojf#pR7j7|z7>8u6bgEDCZ)fJ*_Re`VAP7nQ==h`>m(@&lR3S5z2RxpW&e#?4N0<g-ZY^me&{F4y`fPxZQyI>@?(s+SaG3b+Q%I_V9B695q5A7Pwqhz_H!VR8B6J?M1%@XM0{afPd6C|?49hfl-24e|u>mWFM%z=09+abb(8eeJhVb|ERcBiX13Eqq(q1EZZ1zTZO%86T|xUluR2&w+Ccw=<xNDzG%a4+E1<X2rVcu^nhizb<_He{F)_ej({W93u|EYg<jEKqO=?CqpM+gnwMl>uh<^1=_2WaVK*nfglUyJCfTPcKf6T;*el~KuK4~gH{k&gH6X=QRS?JiDD9`uGQK*OGocQ;$2iJO<stK@y9J&98IPu%4Sp%#(NB9+4?AAR%uDvtkIvJ`;TuAwy@DcJI%)NV__j23c$<vClnTQ_npmX%7mL&wWv*P#C+qWKDJHAC_DImDNE?}oSo4#lfiI0<`qHL;!_veRLn8qJ~Yg8$;L<=AtWqR$wWU7A@w}=nz1XiojK~O0S8shLqAMCGez1%U3b|(!N9GnS?b}KbD^Z1V2f|)nlU!?CFhkJd|R7NgNR&GDzIJdFe=RNd5UIH4=AV#5n~1p2>4cH+yEhd-S=m~Gq3q7(%hIhRmn0u#h7J;ZeJlKd<<+%s+&!Im>$rQ!t5ZEG3n^3*0M)|pyo16Dxy2cE)l=Q*DINN;78#BjQSTK#Ko5Ac%D4&ENNyUY*syIP$FJbLg}9%q9EexFqc=Yf4K~~Rt(2LH;O+w+A)y9Wc_^+Q=jkhFT>KS`2h+K*qpy2-H{S)1uyS1tg2POO<Ct;(|3tfmch~6Wc(pX^M&1f0Q9A+mVm=_H@$lzuN)$JoqKioZHbgWYV__1T%xNq4t*+mvh*Wx%XFMPzQny4O*8kgFFK<gRIH<f1T1R0V`&&Rs9+PhZcH8X*%+!u>po}J-Dc4(lL7DolxO!#FILg_DVfGLd637u#e)hEHYs8bM-V&&F5g%aa%e%-D&l1ac`aosW(!eM$TBYJ21^#2QvJ<`pR>og^;ftSS8yT|T|_i<!E6VZRdO~Q6<MN5ZhH70qq-#RRZ6&~<yYr(^!t-_2#oKd<`KMRAxdp`cIS|TTc)9-%78RCvZl_WcVj<_oTh1fGTjH6C7iYzJ3}D|iCZVVyzY7Crb$fiJq%1`??ms6mbzm<4qNfn1m7~v|MdyJOEdJ+C@!~XI-yVOd2}BWlyw;4?!&KQA~Iril88qNSMQCos>{nWd}EOLn-&>Q_Ms%nKHe40Ik;?M;_q%aRvig<^~@kBAV^QTxCX7EO+xtbY|OOjJ0+LI0dfjG&49pFfcf$1gwz}i^OqvU0P{eJxQvP=n$a9FdGJ`*$FjueG?E^h$4<E++bx0eXi#D{%FggbCl1lvMS$N!kJ5>g(fD;9<5`j#oM*iq27BHqf>(~-{K%B@kMRpiM98v`lpXMKZ3qm1NK*CO&ym-sU`mW+w5!vHFFrg%ZEoR=jpju^ROlTs4`+ve&Sf`rYp}}V$51RHcoIeWScYnJ;_P|r<5mZ$0o@=4p`w~8;Q5b+a0?`Pw1hk(=MAD(xgSl~s50nTRI1$r!KyT=5X`d25ZvZ=mX{mOE+)a8YEocZM@tb5!Mv17CSIn?DiBEp9UE>UQnp)V?i5-M<jn~sRM4W!m%hm2h#!*8A{@g`_KDkAw$wGzc&jH~qJQ^!55?}6rG#-gGo%cMt5imT1w(>n;H<2AcI!1?#Z@Xl=VE#o0T>fP{%@0QcpW}c#U^!rHt3407h{+ei~GBE?<l$;__9d+#+NXA7zW#GasB4~`hWlSG1G~XA}<+I<gemHUYeeDDGL`1xGV{w7$K^&tM5suU(O#4Ngkn<XhD>2OYe+<%SPddwD7~$rH$8{p35uC^Ohiar-?W4;GduLSzCcoJe|a88MZ3F_MtYylZ~Wwy!*D;1NCt4W6eHT9J@mhEi%l0asOfXr}}uaR&&b?`*>sY&JOrD#cYCwilS(y@I#6N9~oVU`^lZ#$!^b7LV~5at-w0eUPTa`NDHV>0{W(~Ft<5|6rZMJiea&Y5z0peey-*qrP!OY@H%W=W=QZrgoBzI@p+0uC?ku98K3wk@!e@|ko;qZn%30bwGv#E2C;Yy15J@4C*usXtt4F9kbZnF-IU5_ds`CTx~r|ol!-6diqJ}&uDzzf=%CBI?~iunk8i*I^v5^z!;iLQ-yZGiZ|}c;``!FJdaj`3evqMDziFPaW6hT+DQEi#*c;Y*Pv<D?Gmj9{f`RZ~V7^kqCbVk{cj5UJ-&8^+yJq$a;!t^Ch<5Gb|N6JzT;%`X+_x;pk{rkW5Efm}u3C;n7)i4sk4zjIR@d|;`u95=R5iLXJls99aU`t<gVO-=85s``_uqg0aQoM<9%dm#=d~rh91srkR-uArR0|&#fc^8YHq718nn^f8(M~-_qyPTn!$ngtIM6YZ(G^ww<IlbcNrzYqCw5j0_sab+EHd=}w}1Zi*FXK&?|=EXe}*R_4(xHw;*Xt%uE7DBfSX~NT`TZ))#G2p{EHU8Kiso4eL6Ix<Y26)(Lc7|lYfhA+I$DxDMdyH()LUr<V@Q>y#gY_KZ(YU@$9g)eff3t@cAq?rhD?Vi#`GE&@eB@b>$uV2A6>~O5U(PtaDF3T=~f!Tj>?kFf@$4@JgVQWpR2iat!o)<2_kltQ^1;3|*+>@4hISmqY!kZ+^>uo2xyvgS;!w$s!s07*Z|2{Qa+g`{mceUOrCueJuB>_z(t4i5B<quKK-`w}_~rsGnfqcYw7W?z1iZS@W+7mKe<`8aj=&Mo!m#u``K$K+v(V82R9``w7mNQ9s;+FOR168|xn7F)GPaYVr-_LrYlJhK57b6rrNH;K-wrS^MgHf38=<7D_4Xu%nxF?L~BYT{ZJOYMWojgKUTlLWCmW&ZSh&F=?!8oCA(z&feTj`NVulxaPKEnI9UGL2LT#Tih_^+pxbN{gnca4e|`RK>P6hAP#z`jz9aV>elxb<p;@`N7+_{J67euIfk@~v<4NI3c{36dIsOXCNieEjy1TE|M<)M`+rCs<;P9Ai@HNZC8H|&x#XXJoH!q4(W)~=vireAK}}4yJI0B%N0YgDSGC9ScJm+Fn9c(SFcYwOA$j%~>)?_+SxLQz8qH%J+fSR%?=iZ9?oZ*R<(LpBSQ?vhaEwHrGk9<`1khDfn+AT=cvGQp?C29HGyKn_lISNJ$3gnjq|2pQSR^tbwjfLAk4?E2f$>AVg|Z2FeZ<EfSAcEwTZz;LNawNI&?Q+oHk2=*9Kg@XW!q8{!A5qBV-XJ-U22LiE(2a4r+59n1lah!F4)*`hJd6F5d#$-7-P?i#E#MMx4w*5nHnQEMf5<BXX7x!)%!1raAoZ!9_>^hb6YTMBx3Tu&4CzI)(~YvRLaV)g4&v>$7p5m9+Ur7>CBvE=B0&x%dX2Yr@g18H=1GXZ<5$^oQ9rJMDG%$w_Bhw_~Vn?>%kev<pu+pZx^EqcN@DyQ=#TXi*&NJgL&u2SUPCH*&U*FLsk!H9FpnY*8vK`S_ndJji=nx^&Hq%7N!G-Kg&F|E-jP<O?;<me=RFj@pa>0p9i-%_wjDyN`1^J20%Y->Yso7_{Y0Ur<{-8Ji2q?^ppH6*k<xkqtgrxTJVio&UsD$6Z0Z;$!R1umk{P$2c)MPj)29$VAl%vtU{Vt=-43u%VU(Ai&f*IF|;Fv#RyQ8_j7Cu_VEvN=9+LQhfj$)pdX;W1k%-8)$HTfjTszzk#}<$3?C;9J(sw7Q$N5iY!8{;fvi0r@WmjJrKQEkKYrS7S?2w4gTI*NKi7v%Yz57I$4sR;U`)e^#(+s|K<32O%T5bz>G4}{E(#CH!9<6FPb+%d;g%n}-me8Su7g{~j1UTdvt~OX06NVVX8m)N2tIIL48%C|_%dz8Xu?;)pDc_-0+gA0l3-1nIRh0SSDfX76w^zYr1AG1`%~(k$_&|CT2eX9?z$EVY^2pIzVL>UhegDcXFy1$r~x6yWH~5bS)lr_$3<S}29*8c%+3vKl<%WY{s><odvVKm7g(p7qDU9n^QyB~Wbf|&`)G27J)_Wgji|lm9h=r9CR*)u0S`yXcC|CCSg-b18!<99$+~5dTPTt?##UFjT%V)fZlw*0&aSK{+dTik45o=3cT=|Ub)9MmjAwT)Co6D$mq_)H<`v&j;L<D_NE<U{Izx)mp2*yT1x2@l|7*S<M(@I?^ow=M`u>xsTSiB__rqz_1B8O`oMt7AeYbUxRDG~RL=tXhdhDiKFaJ>ND1h~MA26vI(5FU-?W3&E1Y#2po0$tKly3QSTl%alz+ouEOG{N%<+XMivi=FGo+QF0{X+D@W#>eaY!KZsmUqaxa)KF{ZoZeJPAdo^9ej#m(5GR1)u6B6YsaSsA_VYCF&d;CM&M0{30N~e;eh934tM(r0Q6T3BIzm6#nad@2N2{gNc=G_6!komvmM8HcbZ?A9HVJxYPoC5`TlYvITrA{=<SR?$|FQi`R5Ca!R=@ZzzdQWU~L&ReHo8zgJg=3AWZh<3KFW*!LV7!0GE!017&rx*Q|IHr_t4T08tX}Jj>}Coabj+IvS9^jgd5S;iqY}t&f5Sy#63g3VR7MrfI2h6pUM3bX$4@clJUus<>mSTa9g!0XjToOM=Qd-~7*^%{LdR54pD@(*`S#IM)0a*3{Fz`UT`nJWnVK6bD>rgC<?>kGU*eMCdUR1r%PODWX&)n;I~N!+Q>bUS-#fbab><4cD`xF=s6Q^3g>6?S5e^U)~0m5SN#euQ&QPYH>~SgSgZV+JKj&DKG+2wi?v27h;)dnO{M%rfbU5Pw1o0^S}7QAvV*y#ze`LJfEXwYYfuYEVFj^G@p#Q4I~Vsu^iw;?%&lTTtNByZEn&_xIO_bJS4tD)l_pJk^Dx_Y#rQuWOPPiH*Ai<buxCl$;x|O1H1_xu+)^t;WO@pB6U;Z!Xb!Rvq)|u@U-^9!+2LXC9$N_&r??MW;e(etEV;>v|_HZF_uL<&!Co^tL9PoZ!no)H1`+j5qst3Abb~ghVhW;bbfe0>$Glm<k!W)pQAZi2%YQ3wIUA}euGK%o@g&5DSD8ZoAvMMKGoURSq&`0iN8|FEL8C1zs{(%WwKJPKT9)G?hGmzr7JV1Ic_jI0)JnXuf$uD$t^{@a#xuazq9ZZAio}83+<NK;O%BR%e3%+9TKQNu;W=wJZ@5XGS^@pe-ct)+Li)#(IJg7t4yQ*W>%qyKSjcqED5*QHNB4oTm4D~yOYcrf$Q@1E;%lmkz#5nr<A>f?>$N*P|S!egy_fzoO|NHU6>Fn!}o*PgqPgwz?t@;(!-=f&~oR!5<SSOPrG8O@bvVAF9rcVYDH9$uQ@N&#oX^5c{kwY^z9;8L#CVXIiVS-MI4jaO1B%PjM!#UD;K!7pE1g_rFNR}dS<FJr|;Sz&f-}mDJO&sq`H*iXU^GwZq~|na?Lh!z74K~i-*o+kWcy>D$+^u28I)G4gc12wv&@)M8|5S><YRO%uz3uN?9wlF!OD;v0@yDLBmA<iKuz7^G(UHVJqThsLwconH`d^K68J^SZ$I8Vi2OYR!Uf3Ed{WXNg{i0@p4X_fKs2|7bwh{{S39%GcPyR<wI`P(TUW#?;xPG2G3wl=RK&rHgFI>eBH5(lK}iyfM!01IJ&8K#v+o~!aT*-dM;pKM#8z^=Eh1kb>UV0)`0ro&qE-CKIpJIipSJC=CKM`Y?TP^DYM6u483$Cs^dxEt9%rGM31<29*t;^o)wzY195D6ec~pJL*FJS0DG1LHjxJo-PGLBjxnGvJ-r~Jp({>qjO&<;vl=?%n*z>M_HxIxfYt1DjB<wsf%fb}*Tkb>1kP?e#TGX4GN>cAny10$6s>Z1N)%R<ampDbj{^5G=<ziw$)D_3O)9qn(t<G_MocVb@zwd<GgQ*hMDNV4&J9VMMW4e2Oo<RM=bz#E)MK!#y>S#s94!-VP-F=FV_<tB8_E+Msmqs@SnW;>#<V=oGEpkBi?XIok!LTrJIr%YDc<B@W8N-nkF<xa>b@T3V}4jICPkGxl~97yYoBMkNJz7pObpLq5-WjgXNml!N@sF;6C@)GP_ryW5o?=}p_3!UvIm{|x3vG~VSo0X>T<Zb_=ZQH4nw(R^=r)7vF3#8tw~hE!iK8=q)|g40(*CwV#3@)<~YAQOQCTqbMaC51<R9Zy%w$+Ey!jijbyTK7y&acqun%M;v-N_Gp&clARgf?3?|xnnd}CG8mVKR+GpHqX5FTl|1p(bmQ5iislMCO@RgA8#$@R+HSPibZ$wkez1A?D$WTfUD^G1O(0{n`UubNw_;Z+GNz5m_?gsYQYQTU^QE5cdAlai`iUS2OUX{Mo6xm>8V_&<F$M^vuGe)>na~RjvR`7gIZe~zY+gwtdPVQW-HLo$td|FIUasvczC$e82bJ(3KwZt2;Q&eHWA@(LKyI&o~yGlX<k%QJz!4DGh7#ZIKE6P0o$qj&ej=9YG!DaYmQ~45w9a-YH!O{vJAj|NZIp9c);O2SrHQi_{lK18hKkLokWVT48P*+}rW&|m;+h=sY$y|jE7O#7on}E8)yd??p%p$WSEQ$^iJTHi&(xmKM0J(zBr+J%PA)xGqlzBu-yOUxBqOI6e(n^&IVMb8avoghTFu=7>CFD8;fT0y+1|~I0wM}Q<_Ikdp>ODa}gk=+@tv*loKK5w@$=nASF3g6!(C|LDqP7ecXK3Bv>%i3&T!7z};xzZA1KWrBF;aA+lb~_bDsal;oXA=rkF?503R7GpAoORVTI#v>hLpIiQKkaZ;NeN3%f3rWJ)n9E4iK<zCTXgBWkk+)mreU1y_)&Rj4>?5qLb#6!d4wwvBh8!jj?pGp2`BpyorrC=UbA--00pdx9L^IFbWDOurTnC1}|o5kk|l&Ss+)4f%P|QjxG{;?MSz0SW_b@SjFG|5vkmbd9AkdMfzk&!@Md&XF1E|R_mXkdWQVI`{a8vdRT6IH{uq@6~1gJ?F{mJ`ao~UJ*%-ChiH)GlD+UsxJ|6V-G<biLsx>-j0iPm&5O^7?i^yt(1pJZEqASZfht!ci(^=46RBqFZJW-?NnWV}+M32R43tfo&X0kv9hFp0_)X~#4C5lX2bQ5$B49b(r-ojXeu$wRct9R~Nim-9$f=GLd$J5$C0C47?cBrx2hkVPkP|-VF%GVJ(2ISuEDFQNPCY>=#;2xk96Omuc(aH?2*$Mt9d!JldXro1@*-`ae5z0!qx7MGrlQDYTH<+XWXmhyHP96(l?w6;#-nY`e)_m@ccom1)Dj>ss|woS4_Tm@OONI<Zm&V}o2U8b)Rz`524BLD<TWL#_H9-_J{LH!{f&05=yT4K&t1iN%hIkBrL*qBlZNv`Pg8*+y|3WTLI4ikJchV*+Z_2GQn3g5(;z?s!@n0wQz>r4Q6kSXmNarahPk=LJ__DZdt6jyxsneZBUPm*^o-^WxeV3NsVTNds_)VvmA$z%2Q3yl_o<tH5_RvmC)O8ND@WaP)Q;&)c3A_~E*mN4kPinZKP?y7nT}ZsM8G&e+AvAitsBXU82h)RAWPlNd3{mR?%iO^>q&=u!N8gKnD0K;h9V;5Zk<6wcJ<O%YTj$TS4`{&(6w4*CZ*tVJJxo&xr`-%nY2TBh@d_aoh>IfczKGK!9VpHInmEg+g~SI#yS(r#XViVop}2g*z6Khv(~PhW`uPm%2_}5f3YbAcsC8PewSdB{AdS!>@?oXy}PPnkxxH91WNX_RK;GLrc;3MhN+hoGd&mJ_>S5D6J2lIxu%^!@F*%9sAhyu8hSMx)r_U#$%kj@F(mW|#uIgZs!+AlO=)vi2i~&UTtp1HBzDSo(5<6~P#o*jCr-*87z#%Fs5T{B-E6)sKJlC-SZk8Z(57{8H{^5iB-<2<GSR}qh=Rssy<~>OSV_m99BbZVIcFMLuWNIAq>WRxP_o_&)J^d!#l(%tgP7bSvTK{o9#}42l<|=n;1FCOiKU|y=Qf8FQ*hHU=89{gtloaV31^1Ckd<OQRgsspwd*<H!8W)RN^D%(!~jOVBl+3Cmq2~z-8}z`54E|xy5IUto!%8yki*Yu$I)B>6#XlsZocS#EsYF>6=6QnS^tcR*WE59iq5JjNhy344U^^|#)WS>t@UOplBvIMQb&#gFaa%BSSP;&Z3KW8DjDE#P#hDL#ZE9MRpH5`3)=4cR0qty1o;l1hIzZ$6U198`!s<AV`Q;pk79i7x50KTDcYde=>{!)TYCbd9SgqSQ{ojLErEd2i+oz3bhw=XpsEqltT+r<I!VZu&5!v&SMzn@+y86R;_(ZMI{g^2=rY)rLdwKKigMmy@`e26c0FvX^OMs)o{BqJOQd^Qqvts;JS5)kvO}gcz=T}^1W>+q7POB3=59V@i0aW4EE-c3B;F_-{@z)(c{g(0rdD8a<(H6(0Qm|5y>(=Ss02gyq}r0#D(-gKG1@fD?|=6{e>_>#Mv3S&KF7yoSsIE*+qX^X{M2ronCVyvX0L)Ro7)2U#;a{?`;Jj|5N}et!Rz@uV{^twpY*ExJHfL$R|LyG`vwLwZS-U~6-l{NTN=}|M%|ZvshAboFRYqHz<G3&+?`Y8?03s<dpQ`ObTvyJWHk9+`=gxaiSOvWVpQk@&+A3_RyO!~GavHAyqAhDkQ(^Dl}(f>z#(c*#Aty70=}h;7+|1Y_Wf1h%J+OlNbZ5-w%%UiX)^RNy#(TV8;W8<V;;&2{zaHUWU2sfxgX(7GtV%Msbbx+D5Hx@78xi@z1(RCH?G4QKW{Zadtwk8NrxKS63DyN>bk;%TyJYHmpjOkW2^CUY~G=x_?X_^J(akT<(wl$k|9eUw=4L?Ytw|!@M9zcB^#e&=v-nmI#0~wqVI)Fr$lBZcLr)|(<HQHr5%}VBsXNZ^@$$YN?qVl_c70|H7Lz^=yU05cL_t=i@qo})X~?{Aa{rfm*w7eg+3q*e5$N56FZLmrlLW^!EtwAmf7ErVj47rz|Z%EyP3d|&OOgF8oCMZU|0%5G@=Ni=#@bt!}guu0!059|5|P&W1$HZJbU_FJg#~#?&{PP`Zj31%IpA`i!}$uQ7opm`JtM|0a?O!#YpW!+_nz;i&<uj0iwpOeRmW!KiHT<RA(KB7jqx5c|3vh#{>0(9(<PDIyYt<%?!uWa9oPOU|8+!1^YO2XHWz>PX7n88hLD<=8M-x-?0TG<-c;!x(eN2NIko?q0Y$DF^aOq;t-g*MxfG5T)#c>F^Gi7xY|%0BD_EipP_d+7xEzwQ*rk}L|32*tb~fJO<Lpi8fkoR)H-hdj@b1+04_l<6X1U|kWe(YG0OgW28$|nwu5<~^iL(KKr@<DJ3bH3@<P1^@DQ@Zbs9P~JtCqUC3K)-oys2gjdQI>IdySr_plsv!T?NhvF9+2q^qXMZyLb9XNgggW86L}waR1shTsP>E+nZ0+}0T4!4Fw7XZtzw<s}#fqXz8ihoI#Fc!Ju{`HT{#)jw0{B?(VthwsgK`+aM0x5XeK|Gan<P0mN_4Y>xI)7D4M45DG*Ac^2lT@WwiZ+LS+Hp9ypGe%7jhx#VZ*s1we&^u<LL=cQevw>ool?xNYx8<DQVCzzr;M{EgC`)PT$jqZnmr9q_psf+Ob{DupuE|_u;N>AGm4d?}+%}f>818I~kbPKIi;#sT86}RGWlOyj`V;*mi~9GJirVZESZ5i6GfT?wgih@aSg@z~-iIE}=WOnNe(QU_(xsR@>k=Bkpw{53J4t;PL!GfiqT6BiyhN+F+b!nuuHSszpnrY)nCVFAK-UT#=+9yUT^pz_xG|i%F1GZ4CMu8B0jmyPGNmrBvZ`+}NK~7n<&9us|AFm^XpH#9<HPV*+3EgEb?+XgAIMRg$w!G^a<-q>?^q}mFEH%{lJNYf5LrKJ8$oG!dnLOomgaK>?zg3v!W?G|L?^sp`H+RVEol_Nr|ENw67s@4QpV2tMe1|j1tjCtA)+z5lGEodHW-&<7-))k-LbU-GmRO&3)uOOzsp7Aqv2Y@p<SpM^j2i7IC*SEXiD6dT+tw##IEoA^P&Ik$KQVW?ML|V^TFS@3)jp0uRs1CK96iEeEN^Z?dvy#jXl<URiSZ2k1_*$KDw6|4!%JMOQ#Jkc^>#m8Jp0qE!>6ISA28HAL5$DFUV`3ePP<Qukt;$b>Sla{_BU~U%z^og@}s>kAB&u9OkXUXUF<HbE6Z&?V;i3jMhxn^@?`txuEy&KRzlvfV9j$ETb!q_Q#)n69mbzCPnP581A*hbXa8Y@NfV8>#u+MuiyXjZ~qKWL>$=Tn#CVG4P8@sH!Ix3GP_pb>#E1Uh`FMyPONax(j>;vu#AGSo<{%Jeoss#u4(ffaHkY;4#=G`w(T={^7IPekni~OJFF*Newv;&zfs=wMxHj!U@JVYNkbwTmyx#t8Xc0>D0vs)u+BZ%Cgm1;c&Te4acD>e;SE3s$!Z8@t+nX)#&fy8n3sd;0J>1e-+fVECWq2gpZJ!TFK26R2YFX?SVdmfF@*iU{Qa+g`{mceJU&kMeJq2Y{lXz-Yl-`KSJE!Y(?jUZ)labE9l){;4Idp-$*Q?i1xt+P6b)VGOVQYOxG#2Aiw_9;F&0@6Ty{U%_Dno{@dmyenAT0KJAlWic0Wf<>DKe1CA3vTLvLp4Oi(;tY|hTCef7OR*Q+5iqjWjguT45YBKor~Fm)caZL+bEkf@2(?NQ*{xs=KmCVd-?bHEXV*_*p57nm;z7pznSxI@ESWKExaiyNkV8}=8pJdg`!6+@f_+K2Bik<vSL{MoURYKiMQ|D<x>up3>5SgbEsgM=dMEG<&aFJxxnGBMp}$mxTLM2Hc7fg`XGNx?N`M8AFr+9D=^=8dq;o{niIXCiwr1&{h4e|dlZkFO_WUtMto8>v}v4@;UNVB*Id?tQ$NvE1WQ_*4K~gQThPl<T4PiPIBUS;^g|Z+-43LmoBua?ztsVR3d>$sZFK8@8Dbhsqx*^!R8R-jQ0}f$`Q0tpONgD;bYdKG|U&Z)3g64AO~|Yalr%hSp-ftdkfvjd=jRp83^`zwH>#tQ>c+K;WE8n+$AM^a&nM0?C->E4!$vQ0q!%L5s-KV?Yu=C>JXlIib9obUoLPsmw|OV@cZi2rM#BzkZ6k{Bb7e8Q$Dt9e+W)ENtVIfYI$*j3ET=6Ao-3w`c%WfTEb2u{*b4LU?HFJqI2e1mJNM8^8_aXdp#&aC<P6DxN;Z5Ok@~jG9#@3sBiUM~q+${hKSq61K-sC$}c|L1YAF;2lQ{pqy5^dmLszeHiW0GhslubPGNzNSVU}E-&YSP<f|_2mvF`zW|FFM|ccn{l2Qt_`T_dvEg9>l?<X_DXKs*cw{7s@u6&^Ru6qKjyD+BryPI?<Y&v%n&K2MKsC<iVYKUCnU9zIDiIX@GQ#9B?8%mtzt~n<r}2?Kw!r5xTG=MbG;382FOSz>TIjdzx*T)bd%DNtW6Tm2Eav?j#WeJcBKqRMyJ;olz#pI7t|Cs-EjQRxiSN~$J$G~}06l2pvEY4YuJ+VHsLk#W1<Np(x^W1ndtb9Lh%#UoNNYUhp04M>wz5zhIQ+`%qtcy;pEB*Qm13Ba#2U~(|N1<*h?EaU-b4S}b;ocA%EPAq`Nxlcygvc|unTfNdh_VcrI;6|KGfnPZu6c$_{N-0^*sGg%nR6pca`^<OD#TJIish+k^rK?VAl%1y23iC(^6TQ2#nHB@o@PSDmBJpgq(+YT(FOSbRet=Uv&7Cm;?F&`b%J8)`D;yzi!N0einH*m%;FH!q9V3m^bwU?80(hOSS^T`G7C=LU>{xKW(?fHhs9kU#te7>%%6t0wU34rmI~U7p=FBSOsu!qL=NLVb9~Y-t4Rv5LSr}1D{s(xWg?!cD-L!Wn2dryAyGPAalfaLZDKcFHF$SC}Hd1yu6b7B3gyfgs%b*B8)_W4xM_EVC!Nd>5wbVazTnzs7&zr`;Pr7bx&o6EXRtRW_R_Im9#0G!7Er^oAa%eAux}tun9OctyhuM+SlVEuXEFQ^y19U4ZADQ!y|kJ_coF%27<GuzLDc`sR;es3ww9>-$#>`PJvSLT2RNPHHnE<%UtwCp=7(-nYfum%&e_nRfI;`sY!x2lLE%0158q@??nv5b}Ma2bao|N+15t@W-v|UxSO(#uj@ubR0g|q2rDf(92?)ILASHK;yVglnneR?W2W(Ds5jaZnR^-_(5>MAn(v3vus14!V4bqQ|0G28=&0a+IL+t)I1JBeR>IhKTl`7Y2Rq~#;bx}CZfZbgA7#NO;O=`E|2iTnnZeR$xBzxQ*)m%FshF+lw%Qu^G5TfCK->*|VyD~PMjFP*mBr~Glb5Atr<?B;_*fP;+@6l*X&7HMfa~|#y{W+o#gGL=Px-#!HxMQ)O@E&EBp-9Q+a|NE;tDPdPp>YX#)eHMvPh*ub%GyDwi#5j1IKuG8jnvFw$;sSa#yZ>KV6&H0CH$IC5pb|oBjxCQ*nR-nR7eZ0#Jd((X4lmru*WNZIC|^LW9`}T`@zybtk)1jjW6ppyv$}l{G6K#c6Z}I6zdv+mmw&ALsd*mX0pfZzF|G9f)bQt&b|Fzy2Uj3aiMPHy}cha9MIeXz2~ydlia~sctomUj~5ilrjm5<$Uu$hc+w4m#=&yszgWjC00&wtobplsfXg=3;39Lo=}^~!%<h>{FBG@n9I^dPapeL0IefnQ79FarUty=Fw&!zC1KZ%^lh|O4c)flmuJmt^3g=h`hFoOU*4vSAD5T2;y2nvYH>}5oVe6Zb)J`SDUg8mun<V^K`VJK<@^fjGhI`bu0bDlp8v(ybg?P;HHJuPZ$>HF@f`5hn5eILXDlgcMwT=SGay4_OTZc3zl&O;uS=~5`FjWC)}OO!0T%IPswQg#)$lj^YU@yD7KlDShxf2*YE+Olh{dmKfH$E7*qQe5enz5DQ*cV0It0>c7Rl{5oYp>o6?BZ*P<gV+NMgmC-C#$eg9K7Yx%e1!o{h0A;=u;h*j(h00%&!I{?srV)=6}GwE!Ui7WP&NG5f<E;uNdXy4kT{0Tatg=otvjb?jO(kqeW|q`Eh>Uy{@~$jsHlpVpM8`&1`2Vcql*qWhI*X5oaV-gZW=EhVA~4_GSFqctF)a;gh{j90?aNW>?vH?7gd`~f{I$9UHY2H$U?BwEX9hkLY)ca=Tzy9@vH*FS>`Xd&LRS7f`{0RS!jUxx&0D(pHHlc}53ITa#6KO;%FEd~4{^kt|=!t;atn_1N*{uBvr?@8ux@6?2!8iqn;72!LN5(*S;VK@<udls*Zg9~BWxC{sn1|J@5*{YIcD)*t%{i8$Aa?iSw#L4PVyHBIUC@h5!2B9%(Mf%Hq4Sk%KZv&o7-=2XLV;VZ2>8<%3`c}HRm_m+h6y>rHDhpTrLq3u4*_`Hf+7*`%Ng5$^92Ef-KXcCYb0b!^ONY}r-v*a5&BG%ykR$yK6}7fhmTygzfaY_ylam%iM`opb0=o6d5r&m#aiz9mzRfnciz6v$Sm&Gen!h&RlqRfAG6_F;dd1A7$c*!Tj@70WAlE;}o}~oy)h?twui>GbZ=CbfPE~%NTRh*C-UDnVXDPB+Sr55XT~%KUE{q_Hw}$lWoX&etdFWKo9-bfF!}Pgu;J0RcVDm7#sdC1fk=VjKCHFyO;g5kC3F3l#8f($i7grTn1KfT;55a1)RPvf7gHo_IBaO6~2bH+(DU`>P483b38sh=ZRTL0EqDS~Mk4D%=&kD`Bf%r4MK5-Mqp>GouzC6p>n%Dt{U}<iMwiwj*!y=I8a5s3O2-`n%Oh!o!&lr|~GnKvEF}}CjdyY}=FoEBmedwAPAa(5Q##3ye3onB@BB^<j?9vqmpUbx-jw*`t<#dimLHZc<_!@cQPxh-Ol@kGc6cGrBxJS%lsq?v<+!-pbc4iXihL+4CjA63WM0=bwuJDBFG1%4KI0^-hmWj6HF%11Nu)UDh<Y|r6<;zN<b}t3X*vzv`aEh#;tU*)k*vkzIb3@-H!EGk%81r^nL!douRh9Kf4)eomaR<ITLLrXVKF@YZjAkmC#HqubRf5OP61z(UE#>kiSVR_}W?70NS{7eWcBEMLpi|YHrt}~7XDi<WqW~@<EJ@9%>;8`;wD;74gXO^%icy-!!T?1nB-qe7A!ln6txA5wRAp0DuiVurRVJRaO7pwF6k5l!5Cw&guq>MLKuTdEIN5Y+Zx~H8FQeV0U}6_g1~x6j#*_oXKyaqm1m!s|lilJ_qhZWT6O0YbOu4}F)6&a}DO8WucY9jS658CD>^-K&J^25PXmGjLTDB9lWC@z(sTtOGaGY~oa-9h({FvZYK-Wa?#K1aREg-NhD~+fc<b1SLai9P;tkSQV)EbOTHT&3dU#@l?U`~2B%k;;P$G#pb2LEI*6fZ)p`RJ?i(Ty~3!51NU3;-%}phS;}thUJab7DM$4cku@!DcbXe62+sS=QX*&5|d{1#dOwi*<Jp4icHku0w@0h}in4GX?#<&-vU{0ux9=v~HshDrRgStf2S&C%1FtvvzG54&9W(MgeM8B4{wi!rRJfL1wiel3=+0;ud_W)1Yj$$;|VvhM(nKZ52H-<Y}xNuE5A}Xdl<;ev>(68-zLZwygo>iFr#(DVhCc>3S5IB{*l`qonEkxqycTJ#F(gxgtr~dnhx`lwv7GlSEswsr05QD#P5dtb9f|a5})ndFh@WvdbH7iDP1m>#<==D>otd;xV<gPaNhtN9MfYtf$GaQ|&FAx4oWpuDXHHp<*d@6Iluvf9G9sj0gxbD9Yv3vCyw7wZ_9KjD31nGAl^-0Oko_AfuQY#6JbR8oEu%9#N$blh2FziTl!l+Qr;8DQ?+GW;)6%i6J{CvKEL?t%9)X1Sm3p>O|!^6GeByb!1dlq)7h@?45@chcWps=`J6Rd$sCh5&*j?|Cv`ac1fQB3J+OK!`S@N4ieH1R*H81n9p(>Y#vgb)mKN5iXK}5+vlm;bXf+@b$V6(j>5ePd?<c3^ceX}Gt5hg=41}H^qci_7ui$6=`uKq+(?&Kk@Z(=+(evrW4^2HX_6i{LTRC3Cs~$%xz)PisAea(13qD<i~^V2-i@)x@u4q`OZ)t2hBqr8Lmbc2^fyFjp7H(0(oE4J>-IX9^<C%_xwI6`?wPBcrYt1zKrDiN9a)75xHd_?aM8-}g|-D6LNM$NCCNVqx^|TGIk7!u`7rLRq^wwmTD^p&xSs-Bl){MFVPKaZ4Sq2vP)a$+u<fZVomP*QVXGw9ao&kHX8;e)S7tFx<mWub!Ih$VvALXuLHHn+I)cBl*13Tk$4<%}-iM{Yw{a~(b82#Q$yC;ExFqO9mC_aYx#Llw&X+9bgzicm5XomiE?*T)z#p<;PM5CWW!zqC28r+7PpDHZO`{OyyEhO&d2NaUJj^P}=K=>l$kDDjea?CE+08h!UE1elqFtPR;$z5DfmXk-O#eZCoP%wTAuioEM?Mo&Af&_|mO5S2y-?yx(H@T4d!9+7Ji$p0Z<#i?j7ZT;YS%p}pPcRqk6qP*Seb-1&Bj-ZYr8pwg6E*;O2J1nSK1_aJkM<Q-<*zJ)AyuqD|c)9LR;naI>os$jrL@Nk!Z?oWV1uQ7u=UL9bU?AHPa|4@_GG47DI!XNqLM?imJfyK-zFgaj&TxN~QOlNt|1RyASrEkPJD^Gc?F<U;4bwd#z27DN6w+V2gK0l@6L<?Q`JE%_Y|Xq_-V1R|IyFh`Ko$y60wqWf}ZCt?>>0)W`jWk7cZr23`ExrS;*5?+Is?+2uTEU5Gg&4r`#5vwrOVVzXcH#wlXuFHtP{Q5AU^n7-+p)@n0j#4Ngvo3~q-lY$gD%=hlHhQ-hR_z<Y2d*zqhXUN~Aru&6(`Kjf`Z0Us-lPnvq%>+-fE_(%34PQ5~OV~k)iG1#8<fCpnd<3PcdaKlii22JWAay93b|AR;kHI0gCElI$Q-uN{r7SZWWe4m4=2vUANzfRuO6;c}ae@1#x=KN_)Ur-}62{y)rN}vjZz|=ySD)~bRn2UTR3WHC=sb_{N-y9^`Ylwm;)4U9QWb4`q6AZlAEowrmB?js+IbiCoT>5=iifIjcH2`0?FKoI_X2lZyhJf;XA-eW@eHzIn@waYvOJ_c-UW0Lgk*ARk4Z=<AXOT$$?cdpWD7{^0Wz#<PUwCUt{s17D<}u>6-Z!^NnUsumiu7a=nCsTE)`=$rnyJ?C26#AC}R{Y*RukuL+44B{}^crSa}+r^S}6>nn%OB0H3G&te4&uBb&2Ib`FRuC8K|JPWx3Uak($AiTXJ-9aU^BI3{a7ne+4l{*0>h-7fdbcpqo)z6$$EBVd|%;fg2YOO27Rc6O}DCiOunco&d0hIR70O-F#v!XIIzb}%`5mw<$ichMI4k(aaur%9^jSWb$aFJ9B6%%+1kP<CJgAJRys$?oH5C$_<M=PCZD*ux6np|;WsMmrYVZxlFV&n_V<lZ$-X8&hcHboI8*pj?&iX%z}alGar&<R>>jTnF?9*L`aLuPsl-FD$i<W5fbBxGjZ5n1!3>RP*Eu`OD>|Eh$uEtBYLFma&SXUn_CZ{)?VG#&(y@Sfv3bG%FzV_2mYkdG*cA=A!_qI$6OaG8x&bmE1cEs_#bC#uSLPlW8+crUBN!{9HPsa#Y7Bdy`}LZ|#7$fq5EQ|Ni^`^T(4dZRF-oBXfK#*-`YWA-_Z2Dk<ic?k}6sSc$=}nq8aQJ^RM%+H5<HQFgE~Qx4bbc{)=HEUS@lH+;v_wfAADUQa4BoeI;$EmnimTXF`e<FYRm^FdqCRYMdwr>@3x=M>+P)jXzdJ2My(c(qDB)P^av`CDrc`@Ld)=*!N_eE9mFpVWOGJC@1HFaelX_Ly^>QQMSn5|u+@-N2Cn-%{2N=oc*e{wkL2d%jW<DT0D#y}d-{W{3-WnaA}u6t(BZJS!mRaAE4P-UvUt)6A1qBbPN@Z=>5{Ad*?cZ^_kUMi*<BEfbuQYN&zmr&yHbH3Qx1)SX#e8}bRj$4dkk3hW_7zurw9uD4omP-2f8J*FA~9!QwF3B@vAs0jkr+uEzq0_q&PJoGctCDHc;s!Hqa?ivc*IC##se7)G7g5$W^09=wflr5(KGuWq%d!DC<@!AWyZ3%KuF5BU|70M1}31f9{hFhP+p{>gaoUjiY9p8tj;%z^pT9KhIW}|(6tb@sIR%Bx?04B(FV|u2q23Ct&_NlV$F*6@|DS&6-JjJh^tw~LC_V=ln@DAyc=L^T<3J^J6fmgMaIO5~mIp?JyU?(bMN+ST|x}F}qS9W$gXS0@Dfmw)3WmBI%7teI7*Tf~%#IY<i*U=0HGaz7AU^X>a^_x%v3lrV^P+nvBEZJO6p{J$Ij)Ctl)*&!{kD5rRlk1dU_9PK;Fo3P&t)m2igkY*RFJinY_bNF^<M3kE4^p5cy=8H7MkvC}!c${6nB#fo#?j33Jq^sIVnuI_m%(En_gzGkuNbHQ^Lf5Y(PeFPvRepWx3q6Hp*JpOVo?!pSyVSO!xTy=>|D+5^{4b2hA4(h`*5;fAMcLTA6zc88SpXkyN{^5qOM?7U*sKAyh6+>Oo|tT2QE1%p$1<%1~YWZ7sdVtlna5vt}5(y(;TM>nYw7{d#F`9;SG%5<15m5qq&^PPzD05#w>FIUi9eibKz!)XI~{p5^n`i*&35dQ>Q7<6#2CEF-rqC+V2MJQpXNQe^)_|m%3v7qr#0-S+8hw8crdmvRZ=CvPtBLDlopK&^P6~Q|jM2gL+!LUuXG5voqjy5V4;JLA424*&?^cF`@fw?J)JPI^?ZIR~``RnIIn_@L&$~$=Y=Oev~p!?$qO}ZIpMiD*bqFp>E*wjeMo!DQEaM0*Tu#R_w0de3;*VefyZ{Na;J*3Vr9#V((m=4nNC_*L3`Af%acRx5gX2L=D|#+><fE#li*A`Z+MS@u)1v;$HmX@nQI@w1g2dG-Ft!z;fCgS#rc5uIKHR$%d~|)rOJqlhE*^Le%_7>I4(Iy%O(o;poGZ-ET`TMK@-M5uM3`o<ZhSw&WV1({$uA@3MZ%94bbk`9;}s-UXx+BsmpEnC~!QfX5WC57IFVG)27bII9U}8l&6`((#YK>(2E&_e+>Ahx>*#f-5psyj->-pzo^C-_e{O9wfupc;BB7{ck`1_RDWS!iS#^{=Qutw)bCu{5^ag*;42e9AF<|b&oZd)MpX9#0>1&2XOIA;2VSh8QS1l4+dH(V-wo7g}d<jif?X*cwDpi1$phWFRFKas+qRmfBi82>sJr6kS#G1r{Cdg4)a#wEo0qXxzPzR`_OP@Mr$U?Jd1Yf+0p&?A0HK#I_#Moc6nGvSAFY`Kl>&aiesLZ*jX{$YhT&0$f)Aq{`uEm|MXwK|K;EQ8J>tZu*WrvKXw|rCed$7C=bi*T7j>t9{(a{^Re(l;hv@GoS|X;1Y<po{;~a@SV&yc<~!g{DRvEjTVizAXBz406%ewt7e1q*;c<k&jvhY0U)FR_o_5ji6CN5~z__lwO~`1VvPL=abGXhuSvch<ho3R(2}45=2d@M=Symq*>(N8MH{O%={(ba4poEj<sfYDN<(OdYyWjklOD(5UZU=c+Bsw<o{0SI)$pifI_rLz_mtPNi`8eJ8u?&Ipt38y)A@1W{^_V1Y5#b+KKf!=CpqM_~RTGH}_+D%_Nahp`UFKZTV0gGMcAAS12s$<v;2kczpM87glD)VGUmi{CH`YDEV^orQ$?S2;hnBGQ3=K^ZHMQtZ(~cQs?W^zoxn2z+5@pT6j&6bqj=-6^bkup&HorswvHpnK<C-M@mZenAF~RIM&H)G4WN+@Kd}6*Nobr)KL>zy8uTP(SiyNkV8}=8(HjoQuRY#l!+K2Bi9c#qEu)nHv@xArFLGpCa4o~5ZRr_v_A*~{<K~)ce&e9Y2tx0~w>e*wO>sW&u`H#Q6zyF666MWp1yQn)vq#*#NJ(m3Qj}zykE$rJVlHCs`3NjZGN*yQG9!=)rJ&+ZD%wfFU{D(HC^S}Yj$aG&wo;}7oxQ*pjQtv^2{#eKM)8_MgjIKaBUwCQr=++IE#-?>RMk3D{JUAMH6)8$C0zYcJsZcnAjRk-O|1+s1`pL#|kp48mlr{^CSaZb|Wa<2|Dc2%gV<x%lAGn0*cx)=8@ra?{O1OhTI?t&M9fO%vIlvVxW+sA->=?%)9x}SrIm*%P8Uc^%*pyRWN`Q^u>w=9<J0eKx5VbAgficF8NG1~vf9uP5m8mhdyhRTLc{UE`M6ov@@eaCP;?Yh8GPec8Mj~MB+Z>2-vNdrp5hhJp`BhNUy?mS<sqw<}^;9}DZ(e<Aq2IFWa?EM(={t#LSo@nK_8h07XB5%91nKQoi~{`e$;F;?;zPN?o)m1aQrx+tQ=#TXi*#CtmU!pKSUR`|wNx+9K{*b|bnk1H0bwmf$hO8)?&*3CY%2?cfWx0<o?4d{Do`c9)3m>qm8$r<@vqN=Tb#3G>Gi)QRAsm-_var!{_!r;Dd(d%kM3MJyAA&eBG^4NQj%lI-k9Z_*YrOzFGA6lMq+ab{>-_DdwOsPSPTqytzge8q%7Ij;O!;=%VU(Ai&f)9)l{Z|#Rz$C-nd{N|3GK12}xV{l$Znh0s2cIMW$8FK7QRer_EOCZZ3o2<AkB-wAyd#2iS$}A<8(AwdVuA7$jA+wD|bPPup$EUK_z*%<`Y>!zQ+ZzM*5L(i|`%Gt~FWSbTwl6TR%T(3T#*MhBRn@DK-ebQt)wqQ@O>`LXMgfI4@x8%<zR#*7dOfU{;hApknf7iRr)ln6d>UJS%I^Y}77muSLQ!Otd)L;{paT3oAXv8Jb$!3>ad&ay+w?G*edzwg+eQukD5$llVD%4v4jwNPLq4Ri5@H`s%PtEVy`8BhaS-3FEz)8|y6mL%K0o*Q|=DLGkruICmuf~wI=e+0CUy00Z=2}%J?nIs1*QBI4uuH8Il=)ahp!voOZs;W_Y%{w-&NmaD+kODAHbidP`VdZ<ZzuJhAsY%Kbvy)y?-!itC!sYrL^>!<5NOXT?h1q5n1%@$A?YNt=jjyZlL8v^ta|lQ#hyWXJrh)#kOyfHWWtv3;iDV{+VQA#o6PbI^p{_!)vmZt`!>B~mbQ1gilXxOVM=9*XY25?NZ}6OEMU8#8nb%dtutT{<$&p=;-E`|EJBd98up;k6C^ZS|)W|`6lnLQMwBn&PbK2I@EuU^npOpp33}tv}@v35Dr`u}Fn8x6py;*TL^!1u<k{gl87_c-$t``di;kz*ED1r#lfuk7Kdb%mdwJaF<_a)B^5Y)hhPIVf_S09)4d*76)0WbkHRg6`s>@e^zV0ze$l{g&xn8V$Ej@p{J0C0Np8}afqyaohU4APQ}sYN|icG>;<>@?ipV8is4vh&E?P3A;rxd|T&=wkGaM}O&&E~x2EW19GOv;|lQ$x*PT5t>|$N4CLPMZgl~$#OMXK5QlX>`skKNAd&d2GrNAcoZkKlyOyfOCGYW75duqwValY_Neb+X=MJ+wA$9^g)Fl9AWjMy%G7!x9+a@EaT!AC4cz<K!yo5#s|lJ}g2fcbL@+}a&fjUixqSqX87%UEu;Ptl&5vPCJ-xMGFw?}dgna68z=bAl(u4n)%hJX38>3=CFa}ySN+rChfr<bYb`k~J?wgSskJhT;zg3*<jLum;n!r;k6xs6SZ9o%odAW!}!yK;`*Q92MOTEmm;8)Y}vNRL=sPnWgKB>CRG_BE41m=AWJeRGx>|e9Y8r{>pF=jRJWt6jvwd~*39bCZo`VDUR3k=QcN~MthW#g+U<u18k)9YCWH}4o9`q&4Xqi>yD=x&n5Ue^F`LI)r<WpMb6>7ZKfl(<I-Tt=0H^A_M~?E{9n63$xuc}n)UjY;CoZZI!aH|=|hl=Sqc)3GeB;Bw3eL|_sH{sxl?Mst6W7_nFV1Oj(qPZ$qJPRD|GvQFz}M^yzZFDvwC;5pYtYMJ9N%m$O{I?-N8QrsXjH|yNfeX5g!vszaK5`U#<nH%mY`JEA8%VDM5YL>#ItQlMsmn2iJq2PV3An*OgNutvQ8bGp?%3WnK{GLKAA#LH@G8??zY-gDk_%l^&aEQCnBd0ysq{0(CG+$C8KO<SSEd|t~Ll<LKa7O*jEc+jSigJtM4Ax#17I^I9>Q@Qaon+1kT$itR$#Ky%-RiXYc}nDwz?J~UT_&ZxoiT4VPoc|V#yWhY+Lt}<z4SIg-wG`~#o-u^TYV-DgeVo46I~QwHo<F>eNIfM={l34(oCi^0%ZyWr9R;jCr>-`G?Sh#n3hKc>`q?KOlgp&n$oROBq?0*+6)FDl1!a}($Nz&-TmH?R0Vt1cW%KNGRcn54VurPZzTf<Gn8!W=%X4)-GczTDOopjwcM$JEyi<5@|g%;it@3~4k`PYbFQBov9et{BBc2?xH>={pqHV9>2IirLp>Aq!7V%HHaYoebU;>0$f0`&k)vVZJi;JS%P`+&8(zr4F*Lv6KW4SiXTB-LO>7U`(#9EJG6NzD9s4;}o0o%J_UPu9DjioV04!co0hwFOr4wMHocZ@fn6oC#Lu?EzJc?k6kkofn3w6;XXl|`oya&#EPz4dDo*vJSZUX#VIPhBm-2E8h=+<l)@l0Y1^W1Rjae#ptm5PEx9^nODGT~&{?Q3;E4}r`UKu6ON?WNW+54^x)s|rF7_932R=v^BjDi89mievZ@Jrb_-XoRlxtk9$Z2+Gsz6E|TT`ZhszIAp~G6At1ql+6uO9Yask(+eUIy5i)<xQ@v<tD!TBGT=;QFL%swSlw{PD0dj&w`U)^CLU`iaCTX`&ehF6;-+~TY#Q1s-K&JgMdh!Yg!Dj09D^QTV;}v=e$}LMA|Rg}v7Ly#$E?~rpL@oy8VcQ=N%^_q^|Kh4Skj9K8*|Dco`^pNyV@H^(cRH9(GFJD7I6%0FQj&P5+il_vf8}e9>el8^DI-kA}c7t5R}E~<sOu|;lGoBYLm8)dAqEC)*iM340tS|`C+xlH&x10=9o^eeV*;=GR;de{X~a+u7r4=B^;ZI<H_YsAh0Yz&9W3l0Cd8iPmUDJ9&}13)26J4{n^U*fM(yIgW0;$lG{{6QXWTW?}1eW%Y!Xc^ht4lfGkChftu)C|AgJJNwmU(id!z$a5)e`zB`>(VQ!%^k>CBL&<&V{C@6e{wc-@00N0E*lHkdvP{20~{hF82?nE(xK`1Ai7N=tp0s)K+^5uD%?5>p>k7-_-V041Crj*IPpHt~2mK6%B>bpH%gbD9-O!gjA;~xC~Ml`tGYhCz>@~T8{^VAIMb_q8=B<+*-gkypw{i@)d7@&J51e-3(Oe3nMg(KRfI8cCJSLs*H3J*r6`nOazkZV{o#(Kxw0^D_T(~4oY&3P<55OQTisHCpw>t4?5<Q7O7Y*s?o(;1VCTbYH5K#U}I!P6pH8UPzB)DeQ8@tELh!w;X!0U2uFexNB#FAqo7TAY>D3M_Ixd4F8kUQ@Jbq{kCnhlF-BBTyk0lOVR-r~RDIUEOq`B-6Ua*abp2htbxsGUoH2+%j0+e4n+8$67^9d0`Z&XQh&+Z9#aQSxwBWnnZpVw=$Bi=|;OgJuh?kSzhKQ^Q)rhuyWW2<9VWum81Jj=A3Q}?hzh{N}VFZ6`t|ymXw+@OU=p|C{9gUDu54{mN(`?p8;q-owvzVVar}lnUSZgVkz1t+K^49e^t>P=GJ9pI0D4e0WQv)`1IsmUUQzMqn6mC+wXyKKFr_Rr#^L^BXj?7R@fw!sy2bn+g?w~R~<&^da;s&e4b8cWgq*r=VXGB3>T&xU!W?PTd{P8oi#Mn@J;8cJ(?eAPVU8aPGac*0ApsO6awvJK^+w&IFa)m*w+FDu~l1EEd)gx+h}fg#mvIRo1{j1jbR(u01sUbD<-=nX$7+BUZu+9*me=}q5`r@?ibjSi2Z*?>X`PJkiI$+u`C9=G|$}_Nh%io=1tF~DCYB6ZFG~C+w`ioB*lUiSbO|Z=`r$|rk|G*8P5!^<F^KCi)^^yq%Is{ZsgLdu=_0i_D2|YH|D$AZWd{GBg88TlaiGHmRqecjw<4EJKz(f$`EL|?cD%;931(=)3oKU(y#m$;XO1pw+xa1xEE~=w}}y@==$qvQkymta`N3lP(K$r0V1FKwH^7x&~&22#5yC}jzzTM^QhY%SxCExsZD(bpmMddh|7Z;38e-LpE6A6bS2|rp`C=rV+<2TwLXr4t{qSdE_p$Tfedr0oyDP6(P1g~C;A1HI*EQBcoH9tm!>V?&Lg5~U~s!-*ec0>obTdh95~0mz?7S2S;oOt)O)eTpM{$EAS%1QVOKUchvV4E(#8AZ6ev2bMQ9pMjxL$X+6`j`{lQYyCO>yP($>kR<($x6$(|x%9Y~w4;yCz27X0ket-XxfYfU=M8}@VRW=qq+RV9tGYB7@p-k8;!&jk*Iv7^nU`Z?#xr$6LGQ)&O1i9&MvypJJI1qF*fAOUl{ISBd~;?iw%<TF9Fc;rum*a!^&UMQ`lc$D|F2T9O>sn={i55ndaD=DT-?Xf56mGIXcBUSY!RIA8a^BG#BQ+{%hN(`k#D!cS)94i(&cQu>NGIj5`gVGn0D*x4CLpu++Y}gV_&R@PT&V_@MpOy+-0O&GH{T}EZOB*KD6f~toN5ni;J?D9SQT_DYAYARqkQ2^@Wxo4}A&TFSdvp5p*+om=q<OFPTr%Y~!0&C57?mQdqb9s8H<zgh;DI}2;0Q(~(P(s%XqSg~8T>P@!4Um~=KY1DWvnwWU7XRSb-ah~i9wdB$it-i`Q0A)Iq4MZ17!cPBwIz-0k6jF>N>Cn*PLvL^=8X6FmsU9vMe^?3h&h;FTy22CqJr!N&_8vz7<Vd6(eJb<p8@?!|s|-%ADZJ-@A)tmNv!XLja2574>RemdC6%mn>2(H&%)$bTws(er-&7{&?9d_;u(5fL+4AXRJ|hA2J_x(^MvSi`9#+Hbl%{K9s53)pVf2#eWPAId}2yoS!O`oheJ6<cNKO+vgW)wORHU+)nJCA8>-(q?(k~^pAN?eY)-3g{KHh1&@1|s@i<#eAZP~BDA%ag}fNyls(2P{emY+$xynBPY`@uRYJlOZAof<e$U~<8p^1c+!5Z&KWF-%gn2~sKG!fSlQ^OG0;OTRXfcgx@&ik8p-LIIk#=H?yCPXeSQ}ipFoEStE{6*+XO)0dDmP=(GBTyw7A<L(zy#aM(Y3VPZ^A?5uXP0n0=@#-A~MNl<b!S4D<T@Wn2vG5<{ss@rjZw;TxS%}z)H*x5iME%W27b2?`fOP|Kf{l9u4aPe4g{OqH<SUg3c=02{*2%gZ|Yy?N@2p<-WY8i|P=}RDs*zn5^~8+0*;-GwSwt8xSGW1~^sv1${_bG?^$A&8MPP))zWeA4h4Eg31(G4roThI{E#<Bfzgw?JS3r>X@j6Y<#?nhSiU}=r7oKQbAn%668C4zJc4#o*>>**+mZ=Pa{hwJIJHu*akZWpqQy*zcGB7+6p=t?O5>HQH+j#y@Yg6F7j!COo^P+z1=#aeFcD^ML-ykT9?~ru~{}h>IW1R*L`aLudNQoFD&JlW5lA{YFi2!HVawKWfRC3@|Vj^J28q|U7m$DE>;}<UM;j259aCdH-e3*Q?N9^geu1ufus0=%H}>!?B?SnskUIj05T=+)P(PyW$JgM%43RYm+#LTX*qv>*z*JEXg^Y^sqCq>l{Zx~M3qv0|NZ~@<H<xe8jz<oIX))AHRvn<`bfRObbr~5#!9e#6_MNAX6-j#A7|TfjIx6;oYD+m&(oPZVCjp5KEuCJcOzByxH+?LFd*MiZ_1g8t4MXn)*O7DHR^ZlOT|o3W&_m&2F_zGHC>(}XT4o^+daW>%B%V5q1jB~+?;KX@94c^ROrjht9|%Zo}bj)8LN|flF-mQS?6*$g~LR-kQgm+K)|<@5d+E@%f7z~y!)Q7lsM1Gp;7DYCHg!=A>PXzuD79xwj1*pUJx<E)L|V{H@nl!Q%fV4&s}e$+g2e`PsAO`b&N(AikB@DoRVr8f+(n1cjY;M-ON=--L2;gX2k?eq&^DNG@wcQosn~cMBjR=bw4HcxKRSDQ450frknl~;FHFaUvF!#77(aP=wi;#NN!{g?gcos-tMkhz|i7zw&lyjb`TuC%|_jlw4Q9C1wg?*4d(MaJxtYJ$U95?e{!`BPpwcA@DiS!d_vr$;npXvX)D44C(Q4t>4Q;~=0EfWWVDl!b#}SUmu$=hcmug^OgHz{plMOdK2?@IX3Znd2Ji!%hu48Eb>FSo-=|`FI%GJWuNRLZK%8`iNtGPGGa9~~b6yHUiK2R?v?xHr>gmBN+K8sH?3m43Zgyq?DV67a`dmEItu7ds>J!JZ(054l70iHuS%KNShOVB}L^nTh*N8hyo|&^TY6-n#;QNck1dO($CKBo~J8<Pav5tpg<T~Cu>Ig`1sA}^fjGGekl7lo3FXs3lrAyLK7AI$fBFrq{4(fA`=b0NvGpF}7Fqgg;y)|CGj(yyB2vK%ooc_;e^{$~{qsQI??()3gz=XwKL<CCx>2+MptfS%^vzUHnuIVk2t^)@Lx{1EW=R~j%59Vrv&pw=_*~h!1O$is$Y$be{kh>3?yF#mAjbEfIQ<#F6ZZWoUNq6v=@8<86UHJyMDfCDKif4H27iT$+=}5jD1`sSU)qr_`XHgbm2eCnuqSxV(Zw^h-*t8rWvra>&^jPd`L0L5@MXk~`e9?((G<C^f^l%n+!d}{&$0Dasfm)I$oF>0<3H#tBW@wJ-Y^*;`U>w6YM9Gk0At^lI>=HdjQvvzXqOmr-ZdD)><HGIg!usgJAdMl%aK=Z|>Ypj}jD&Zy!%@#$8+}7?xAoB>i?(<TO_t+&ukA7VtxtUc<Oh6%B!WgwPO1_h4Fev?^my5MMj|a@SHs@bc51%)NmVM?1;M8@wIHTyCKVzQZaJqm*i!AKjs~`Uv@Vg>`{vOm2&XG*@Xv|X4lt7rXy`iEnCN+=%C!OBndShi2^}MyZIRRu%U%&K>?8+e7+JQ|OQAK|&%vmF2W2|1srWH&8J9C->U0aUp9coa>2^gr1nYc%t>?A=l`doDQwTkfPz-sURrCsy9x$+$xe+g^f+bchTFiT#<q9dMQRut%;n2=g-teS+l!|xmafo57_H~8~l{%h7*USaJlUZr?&ULqR>g9I3MeNV@n-BZ>uWuhS9VxT>T48qoS;X$E)61DHDL7jc&q&Kf>}<7<Q`5S6WoF+rEj`O{(e%gpm%hp}Fzlz3IKuq9#Pl#fkda$|v5B29L8O4FnZ$8(RY2V4X6oL+c8+17DdJ;=Yj0qtF@ttN-~aJ<SrTIeH+c!UfCUq$l~!b|xK(ULXa?FBD|6Cq(9rGsGq3M&KmPX1Z$H9^pH0}lT?nJ!fBo_I@cGY5m|<>@%<}b{!Db(8E?GGvo|ehFwMO6^#p8z`zYf6$-#gdaSSe!@+O>td@cN2xF6&5Kv-m~)u>8WbYZo(~TZC|t|KETA_x}f?-?OU')))
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
    fertilizer=bool(_V219_FERTILIZE and day in (24,27) and obs['market']['prices']['FERTILIZER']<=30)
    # One watering tour: at most 2 entry moves + 9 between tiles + 10 waters.
    # A hire request by hour2 leaves at least21 callbacks after confirmation.
    crop_workers=1 if day in (19,20,21,22,23,25) and offset<=2 else (3 if 26<=day<=28 else 2)
    labor=_r53_labor_assignment(obs,action,fertilizer)
    if labor is not None:crop_workers=labor['workers']
    count=crop_workers+int(fertilizer and day==27 and labor is None)
    extra=[]
    if not state.get('committed'):
        extra += [['BUY_LAND'],['BUY_SEED','TOMATO',10]]
    if fertilizer:extra.append(['BUY_PRODUCT','FERTILIZER',10])
    extra += [['HIRE'] for _ in range(count)]
    if len(action['market'])+len(extra)>MAX_ORDERS:return action
    # No assumed sale proceeds. Reserve 3,000 for parent obligations and price
    # movement; the qualification separately requires 12,000 initial liquidity.
    budget=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+count))
    if not state.get('committed'):budget+=4500
    if fertilizer:budget+=10*(obs['market']['prices']['FERTILIZER']+5)
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

def _r51_input_path(obs,targets):
    step=int(obs['step']);day=step//24;now=step+4;pos=(4,4);remaining=dict(targets);path=[];quantities={'WHEAT':0,'CARROT':0}
    while remaining and len(path)<8:
        options=[]
        for xy,target in remaining.items():
            arrival=now+abs(pos[0]-xy[0])+abs(pos[1]-xy[1]);gain=_r51_input_gain(target,arrival,day)
            price=max(1,int(obs['market']['prices'][target['crop']])-2)
            if gain and arrival<day*24+23:options.append((gain*price/(arrival-now+1),gain*price,-arrival,xy,arrival,gain))
        if not options:break
        _,_,_,xy,arrival,gain=max(options);target=remaining.pop(xy)
        path.append((xy[0],xy[1],target['crop'],target['birth']));quantities[target['crop']]+=gain;now=arrival+1;pos=xy
    return path,quantities

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
    for i in range(_R51_INPUT_MAX_WORKERS):
        path,units=_r51_input_path(obs,targets);q=len(path)
        if q<3 or len(action.get('market',[]))+2+i>10 or sum(stock.values())+purchases+total_q+q+topup>95:break
        quote=_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-total_q-q-topup)
        cost=(q+(topup if i==0 else 0))*(quote+2)+_v219_fib(int(farm['hires_today'])+i)
        value=sum(n*max(1,_r37_market_price(item,obs['market']['inventory'][item]+all_units[item]+n)-2) for item,n in units.items())
        if value<1.5*cost+50 or farm['money']<total_cost+cost+3000:break
        plans.append({'path':path,'quantity':q,'loaded':False});total_q+=q;total_cost+=cost
        for item,n in units.items():all_units[item]+=n
        for x,y,_,_ in path:targets.pop((x,y),None)
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
