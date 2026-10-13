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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_NkvK;td_}mYb-<kV1hb-|BBH08vR6#2c2Y0o1Az-1!;!1B9`tLi_omrI`Zf<TKS$%k}R!?m9ba%yvM})h%x%t0-^MCx)fBWZe{<r`1uiyM%|MV~a^`HOc%a`B$^69tVzWL+joB#4p|Ih#V-@bg~%a{N4pZ?|l{^$Sx<?H|S&0l{1kAM5+*VpfU|Mv4YFW=n$dj0g}zfJeYi}O$2<?BEFcKz|k!}tF9A20jQ{Q33Q&wuql^!V%K(}u7A^4A}Jy?&#9@%7Jq`uT^SK7IXwZ(ncUytL-qzy0-k{pIUF6r=v__4nhbzbxJl-~RjGe_8+3*FUtb=3|QcuZ};xpL6j^_aA&8%Hbn-e~x|DUw;4L$M633<wrjM{&nighrKWA;lql*5>D{PPv2hA{5(S%t+jmlUSuuB2jNlOuD^YL`{LVA<pOx48Ng_Uay0ATRd?h*jB-!qbLO3f->%p1zI^|u>yNKL18Xg}jt}_Dg8uyZ{@0xE6o&HT88qb#woL|y01R%M$?enU>#yZkZ=0Zuw*lid1N(Ph$9)*j<D(wq*fw4|lezI|>-TQ>hhg50(ckyS&m5Qk$)j!Kb0uxE{h{~W5r#Y4(aySQ9zInxg~z{nm(u#V+v1r;TK~ZA^R`zBZ0dHQ??>RAgy?h4=2%m*ds2SB`?2dXcZp?Y#$lJc_~~b?JJ@Ho?(aXH{@~I(`<R7q<Buil9iK|(eb@<tg$3`bUC@f9BU`tARO$olUr`nbJg27?sr;zi6#PF|d{O069xc&x)MEz_ysq(vfhVRMDEyW^M4?0Q7}ol4!e6oP_5F9(e^UO)>yJNPzy18Te|P=$^AA7%@V}SW*8MNRAI!uJARKc3=H^Kh-v%3Ye~))R`qKE(W@#zcPvs6jp2yNBR~#D8CG}R9&(!&7FlFUJ-cF;9(cH&In4teTW+m(HmB*j?m|=qRduqJ*o95lNo;=#e?QrI<cFx@iJ13v@$+xnK*X7jSJo%-wJN&<fl7H=A`Uu!FmwSlZh3_qerD7YiPcMt(*~7K2fw{n=cbR=&_~;{qjQzdPF318Gq2%f1MQ}|xK6y1)hak0@z)d_iTFG2Vh<<W4&$^6su;JtpY7U0G{lUL}`t?85VH9MQ?^aL~d`ZiFANGk@U*3lu<Wmv0S|9nOc>|~S@CNwKl)vBLrRZ_~ro<Orm*$wN;a6LQnb12JV1nVYvOfqA{M9IgeIg5B#~C^z<aqp@5Q&6q(xst@&=+C(AnB{r!{K`)!HaBg`9!uL`&r3*?OC6LU?Tg#cwf|Q1Gq9WFRxv5JK)D!93GjvM>5(A6P-u+GJ5NZ^#323eX?`J?`$;lHim}wnJzr7GPx~21uQ@K_=+rb-F0gm{9-x53-MgP1kFt{nS{&84K#iPwZ9Ef!zxFp(?5#mtAR(<c^=Vu#}dU&HS-Vr@e)jeZ@PmU=m+EeaTOi}^THl~*QEi4e_!64ZE-<zk$hUkvk$yB;e%@2IFH1WcI$>e0dYF(+a>+24|cPvysP`^l~9ZjBC~7kCvWP!t0Il|T$sf7S?fS2@b^j_Bjtkt5TwGdN<S|5H3zN;_o|-k&{|K#OPka<DCild88bB%LxPX{j?$c3?KJ_w0AeLzA}`OipTka~EGso7#f7kE(6JD}xjK=|B)}#3AOYu5lCSLVsRPfW@QGOvn9}~a6RS@?=eu8Df600#AOsld;Vce>p39ThetdXr&Us+*_7u)v8|9OozYP8kqTUod^2+odxLUS92j}BlJWqlQPo?hezigN2yp!rNo}{OZEHc7IPJ4X!d&sUt6}+Ddi(`uFW76E5oU^}synp-r>!;gauD|~JAAxP7$RPT>a}xvTM38_>@Wd?KxtqP_%i9s(pAsK1&R@J*YW3mwa|eIF#~B|*oss%cQoa>z{8K;{pQXDuf;zW_LEDvxrDvh~9k&|h$?P@+Co4F1&V0@h_^OiHT8UyFS2~kegq{L>-d!%Uw5E?;he?x=I$ezK{zwX>>(l|e|6vy-dV!t*x)pNgaDOgbZz#_p+h32S8qywE>o$NDvHuoL|KZcVzWxXX0&cnuqF#Ri4`5dWg}sC_;wOXhL!o<F@0T0pyQuW{@!RyhwKIM!y)%`_54!&WCznt|jyM0j{@V5X?<LB-$!37G5Q)WQp0wgfT5>xZ%-zcZb;}?yZv`U$p+fo1<}%#;2ZG>0Rz5Mxg$zqPtsLL7%u+emA@|}_`}W_m%SuaH_jcC^%LcA3g%VOxcwUwu)A+^?6g(y+kzep?P@yU?!F^Tw=hvS;eSVdI9su{#^ha2l8du-IdD6oi-JfXtiz`zMGF~uA<OM#u)>v5(%AHo3N~2d^*(=+v0dn1VG`fnS0}zSRt3-2vj+eB5R6CXX85pLsgNzqMj`_~5&Bcza%#((`I-95jDi`Mjbmm#<5?2nmdl2EJ<|Mc3mb=Bd;U?2WX?~N<<vpgV%cFzr$GLD2KmG9IzyGpam&;zLhkCsXC$Htu?!RCIdpEtN&FB#n!<`%rp8XRL+)6|}XzzY~c{qQ4{mMqU{80nS8@Jm=l*~Dd$q)Jyi*l}H-BOUe1<iL?*Oj{i`Pj91)k9w%;GEcVf23~^h(&)R&VAa=3!(hl0Mz=>;hLJ)xv>B33~Ny-#SAray|dspK9o{;`vEO~WU?%G^Ry44|NPlkFJN=BHF;QN5#K!mQJ1P1dVlDd3J$D|IFwRXJy!q_gMh@ljl*9MG#(FliNZ4avZL`)EwR|sVByd9&b~{&jG`X}R+t{V_ZtBf+_`o6T5gxEBo98yd%3_ok`*N^fI=fG9*X>at$tBc@A;x(xrMP2a8Y+qi5O3uZw14@De0(9z3c0HBxwq&VZ6_d&j5EdDJ=4VI;~O>90A!5lu~9}b4uHS!I0ov>6aZj?oAR-0D_q$nk003UpGgrI7&y5fZR!MWBb&BL&b?;XHugz#h02C>w!c@^Os^#j>)(*X)TCDc+Z|q@Q?RH=Y#2$yciD3@5c<_al5psQQW;X^wE#R^7_EPKbfNx|Bzi>UtS^*>?I#ZJ^b0uQy1rXZ3-7a`$jt04UZnbY!eYFs$}H*M<BmVeLlus`cZ0b=ZGIEufIJ?ygYy*nPHYY=X0`jF*q3o;fsefV9_?WsnvDYENo(9Vc<TPQn1Iyv#bP9gx7J*06hV$s6`Uua6XlM%$G;#OiMcpaFKZGxyo1x*oPkqO*y+hAt~1BgmDMulF3*k^|x8^8=&7si&tW*HLGV2$)3*OGh;>fGAI(<kpD6g9{;GX%LBXT){-F5?pepevS;uXW9sPrpWnCR8Dhr1Aa1e4L~Yu$1vMfYykxurv{8~QJH5g`GW!HkkS5OsDj|txSxAysX~#ID>At<ZKp<QSGOAFc9D0z66_JR|=qtqJ$*L0!^-0u^U=}BI6l2ElOH_h|cFX86k+jDeUNuQ}ragDUKw8F^E|bHWwCq_8W4S~M_@_4dx4RNYdx4Axtmuw{z({wR2YN>atGtxNA+<qL6rEaJGa1<_qX8i>c9`$3SaC@v1LO_*>@q!0!b)tN)~8z~Io==!K2p(pE`-XB?)^{90tJO>cd0m9)}~lK8kAl{G-R=P4ih8t<6V2h*Q}|{DJMt{wf#@nGRMdZPZCx@28nE~=JI9c;9t$-A64cVy$xy2FZF#8m&;;VfU@-XmdNXN$;X|riuh4r9zllcowqWLDjPAQz+zURD=4|A5*}zOjnbV%yja3C@j-&Mcq#>fXkW&ZZ$H;5CVv@n6;t5?+xM+{?-wu^Di>7y>0NHJQm-LBzMSJEV>%_A!Anxw7k@%2ZAIcZ6o?IuRHnU*@tcB1rQg54{&tmAMHG>@@GBs%r`NFhjamx~@9#Ama1$xe<Rc4~ph2o*B3PHpn0sHu6G~#Zo|{#)@CPO=<R#_Ng2+*>{5r~!ct4Au2B5?e@dUa=wXl=gxe~H)>0Sy^c8v@QB`k~8JPfwwa{s&rFF9IV9c3YxplR8jFI$!@u#02#Rl0hPYz|)6vBzI_$`H+f=>nl&pnn9Y>5J9+Tc63EwDQ)wKJNzy&Mcpy_C)YVl+Cf5GHeqRfum7VE<00sDA%XXWC!Uj(YR{w&P+HdxwOF2zqZ+gb5$}ohzJ{IM4a32y-fGp*HQ~Aj2$e!Yh6Xv_YwkMF85Llom;EVBnL#rFo5QL$EC7{HnXb%X~nMqMc{`u(^%nwy3dZc0e6oS+~4B*QDtx33rEN=J@}R2j(=Q?_aPT1Ncp`0vWaFugMqi9F4YwncJsG+K5j#n8i$p?pn#G#b$wsCC)6c?SjFZWooZz(!fe1lZ;e9!B3DOAijx7BzA5>Xwk)b;ExzEa`_t9$tTi>2!888`QoDW<?NA%~obJ}j7rCm~kW*q_jQ}}tD(u@+&=o66Lq0HD3mVU6fi_=lYsIe=ttwfRhf>l(?#g_JbuUN?=Y>g#_a$xP6lt9n=l+HTFMO=j*ZHiTuqw_c&(vk}DFNHYqK^kOymE^QEPhedZC1M02h7ZN$%*pYI|snLQBgT!lDhg3vbA@#6>r|hX55VUcn`;De$Fux^)-3<wWBP_iU|^GV5*U^26Z}IOL<LU8a`K_Q(ve7;zooc0ObMsCW~Lnr&VtN)ITalpv~R`)uK?zx@ylfpA>}LiQ*Ne`+*Q8upA-9jDZ5YZ=b#SLjHVtXD5k!kGeq(@Q5VPu&5$GFsvXky7`md=w4GMm?<l7s7hl=$-4S78&<l2a~Kk{L%b%=$S0<C_AJg`ecQ2~q(0cdoD1vu<qZuPMl4qFB3A3?T3^IDS-<t<OQci7>&t+~;5k`^Ti7@ZU;b|Q)|$4q9A0t@xkU}2WQ$n3Rp(om*|3DFtotL*!;Kkn4Q39sn@Z-=s3NJU@*Bc2J$pCg`B&rkClIh8-Gy;rV$Kr!L0Z(AN{KPWe=21i9FmG!N9%uLUJH16>Q=^bF(MK-$g1f-$(|c0yL7Mo$iy33*$CCnVw$_Sl7uQg038KmfA*hrelIj}5YEuLIm`IDJ*Ux)Y*eA!3tmmq7hPGT(3sf$fO`R{zBv(KKMLT`Ym27wgd}&(ODWx5!kfq)ZC)E9h>W|%0oUqlPi{ZU@0m)k3dJhHfI(2t+-X$lly7<rXpZ)B0VAvGR}U6NHb##jnkb_C5PJhqho&wU^#`EY_e-39f3UKi*K{`uW@%MYs6FCBP7M@GO3=hDTY?27Oqe8=dLNN|hSGWmI01Gfb|!#otDr7|Y8S&>qSL@KWOY#$pv6RWKl;)184VRZIzW<*Xi>&&kjf4gId+NCp7?y7QCA<;7S&f_zzZljHZSiV9*l3nJiZQcruikT5(?#Bym9tv!a!62NhLh!N(<3@&Y`6Y?Vtw4OQBb~)U0X*Q6z)wln}fQ>4IYuj{|v)Yk3jTOF*dwYbk3@Ci72Y*cPQz-hwDhrEk4vpOM4zeqrTg-YwJC#<q82h&ADgQSLky>uaUT_z63OrDiBcB2xy&*;;^2DJLOM2<bR2oq%*%p4jRJf>jziQkWFcEcj`n85OS~eR_-<xqxb{%T}s3mt`SNl^(pfs4DM+yn0M8lUFj(dR$Vb8lDxFJ(JTx#octGsd<z_%GJiwYbgcsuq+<x8&ZWta?P45<R#d`YjUS!tdz0(SgA12?MP}qL3cpdJfZy~aYFK60nkrqq?I`%itYnVrRn_|>e|&OX-gR}gE+G>c>eKn9rh@IyW6c(ZiCbm{CQrfo@l|{Ru=C;+ho(GN;^m^IK&Bq1XCBjzfq@%8zZ;blzztVChFBU^uSq2jKNbvl_P0s<GaJaI8FQ#OC?6`Fyrl5^&}7oDkWd<F~(TgvhAU7DHR2;xq7=}i3%_>i@sV*g;f#(m<FacVq;U)<82BJwfgkJ{V<+TWeS;Rpb)td1q#JPBT)4GNs6i{w8JOc=OKS`(ywJXO|G*;p@3Yo6SRq;heLP^0O$=bP)+<6kWVyLf+o8t_|yE!y|0#bX2dqU6~a9_JQH=O7o)7GT|-I&gO{&UIT@A`35_tRvgz(Svq|)$$$pq3Sy?7<Wg4s0k@Q&xgp!-Z&LD{!H^OM{mJ~~!ktcfXb-fpj+)e<1s~;BO^?Y@2SlozM2W!Y1eF(UkKR%p*o&Tjoc-?2h>uxNwH~rs{lx>QU0b_v5KCzl>tRaBI=)OuW(pOVFmb@E9PAzrIq=_mOvpCb1>2xba{c+2(g4s1iNjZ~GsA&y%b!*=>#zE+4l7??K_O{Y26bUr<AMYmloCa?|1>fkgL`~PI61^_I7~Y^c6&6T`fN`+{(Fu+o!xIzgpsW<u6Wn=@Q;L``zQo$m&C9fHNmNhUBSxJm@DVzj-){{Vn(c8dK+D*3^(lIMOtIJm?kcwB_H6(}DFOO~q=FP*oR~2wI7H3*?6xrkX*YK=jj29v1+gD3wc-i$u!KkfRSDD=Uf6ONURPcOE&;JmGqw+{ekSZzXCDP!f#<s)z6YmF(wd5TL8Q=ADS-}=$8;EUA_1}6!~Jq`-4BXXS&;khm+?PN0#Gj5UZfkyr9B(xFl+DztS1ews;UG4y|g1LLzpZgu$`_*KC9Uc`Popv5?gb~^aF4!M}hehQ3fvEcY?sJ{A%${xA1~;)8PqSd{soTgC!;5vZs(m%W(dWC`ADvQkfE|vRuPxf-=AgiXN8==DY<t4Vf5Vf}RAD3gD?p^ra%Akr|!^^ziIjq2ebKGlOZE$Vb1s4W?JZSilDix{T=6<#IpNh$16)lUp*i;JEGhl@x}g5FDmnP!X|HQMa22)xhHMXlq#j(c7Ae>K=_OPY8A+U~~kSNu03)Ba9MNK{b=T518dW0nWRH;tJT!m2&2a%toaf%#*0tn&mqQm{|;*tKF!BtArxxwutE724LrZ_d&G0|JmUWU9cvu68B0&_O`-)=O`;Po@^tPf^Sp?kHUmbC*SSZlgeyN-;4eQX$H2rL$*dv(0p)=d5ohzRBcCqE%Vo<ixX!1{Q;A{#zET@zw36QU}>}zhEdRHz@R!)Xy6rN6lm9-!HT-bt;y6MLY@O%%qquZ!!y}UuJ$>e5)yypQU;ydG9(ihYP`ne69;wIMRh)ag7O4f%8g<`$9}~BAbNld>9F-5NB)RZ`!PuLqZh*uKh?HF5j1Q==ZU75YItf)^3$G1L5yK=f_x^^b>x@p`bey}Gl0asn%`igiO$^#9KrJQY29c=^jE&9lgsW&0hZvAtVyWrnZXcl<64I>xbnXCaz1g};dGD)78yp-tO!<m|9z$~*Cz!qnjEyyk_~&=Kom#7H)W<!m+Oj%y1(z7l0(q<0=OqxMZnO}$)P&%Ld+b!RMaA+j`4NLE<uXbGd)4xvAwb-ai#3K$I}r@gVeh2d!>`cGNWyt)m%zS;kusE$7GPSFr8P>!#jwazN1?p^e22&awT+eZ=}Puhg5+RN?403<j~dkdts;oEo!#elnkXc$n|h_dnyf(%9c<uM;%aeF&o<D!MgELD|MYOp@L8ZyRdw47sKWf*)EVMD2W$7For9#@(qNZC*9=5yYynv%<9u<*W9+IBi$539pp&Hk@fH4{1^L=Au(wCl}F+MkhCc(%-Aff5a7cR6??1zxL}1U!0}fLOZ2XiB#WbTN=<NTNZkU>D~Fo;OmL)2P>7B<W?~Pi2SdoQ82m6_rCuRgoCADV1}lR=P*F4;lXVl2PO2-Efu#-#M?NayP6IAcBv7gE;6xvuD0T6)q}*5qdxT1`>ERVi?{d#C*>I3ETM|1<o6$%|YwK6?a;j%SSX9s2*#)5`B=Qgmy|N^_S~P=l1{lbeh!<|p*WTl(32RUn-f|IVjR(I@YaCLN!LcV-z7<L%up9<U3%<`|P6^*#V;G@MX2n&K&fQ6MvXbmPu$<l9?{=Mpm~>*9o$bYK5nXk*g&L>;!Bz`xDo-<eoq|qaphbd3L8vs=i_@$1h<^#e_2__)D&QPf90MHrnhdsOzDbvosgA2%Fjos)T}X0_!D5vZ%b+<Wq(ONF%9ih4f-bn;N>Dg<yq89hWn}kwPCeJBJi#LO^A&dc@Py}_*lnlRKicc$Y-uR}N+2<w(npQM%QDi4>Z3olq$+AIBG5-5h{1Cr1S~tW6D0yRx!N!TO$q`ok{TD3ldKBdZE2MWnwTae(qlv$qp04d>b9&iEXy&_&g4W<Jw9YWwk2?Z#q=Z#dQO*Zv0C-u0fAvwz8A%=E77?G469%#Ny9*bMiW3xF=4{c54=^m9JN{~6rZ&C!xBC%!KXp(9L(M&$|gO(qRR16st)(eK`r=0e5B~adh`paV|aLegM!5jsg8#|j3|T$L`0>}6cB_e3G8Ofw11U5Ql)euuR@C~a_%ZMrxQ>%!5$K1au2-EwoE;om}?;I5y-#0n~-Bg?9Z)<C)=Fb4eO>x>9h}w8JJ|7%vZ5&Jfp@SV6B$Y!xkFzqmXP{XsaPuR?iY+$DT=C3KeEZkm8IYhmQ^csdgSM+um%d3CxMwosf8D=_7tn2~0S5Em2;GxNcDwfplY)KSywd_Natm>d4DzSldyqqM~-_Jfjo);wV6PTNA2Oxf1d((Ly>AsT;HB`=Z{i0>4G7YNrZIG?`4?_Z9952OaUFVWu~vwE}ux<ls0Ct)o~LBw09Tl|}V|p!Zh#8efB+Shz2O*|}a?O^i((^c@kdDhJOKL~_erCqMQSA3h-VgvxQ0fPXv3;*xUf*(e{z!i+_b=fqifB4BNkknP4LVPtMpHNGGtt9n&=7>3q$AEDXHR34Mq2h42B$~?w{sS5}gm5nE60kTM>&q&ZX)n${f{E>P*hfGc{Q%)Cz6jg!?9z!OS&=3kCDYrzqe0Vt^<38e0m{B}6G0PbH>N8JiLK}9EGsjJr90Z8Op{sw;$H`96s!k*71RMrM0^2Br7Mc++wUQpF4g%>T<_nQsaU~)Nn7|AyBWOw$>!lhb^MkMLr6B9U^I1Z&jsf1jWbiYpASEiK!VAHVvt1d9%2yk?h=o516kNx4<X*^qL~9r_4S<^d?^hzkyU%c84}pu3m0gL&XA(gT0cuGzmx#Pgow@tuq7Wvi#P>B*0@`*aAPhUvkfP(@f)tgoR8;9+#@?S%Td5R1(Bf|;w|#sxbI?IXL;&stYp)Tz^5mSUpGE^H<jB=$eaLx38C1iBO1|~6$YFj4>e<YkIxkk&2=L~6aXzuP@_pR}Hy9JBKNXM(r%y1w2$tw|+ojjEnF83Kb5W7&`1Y)GqH#-TAx#y@>WMu@bdCf@#chBGT!gz`Vsu-%rFC8$Nm24P*_Rw+-TW;9UI<Btr_l*PJ4)l1a@!+eW6f(9a?YJ@1<415BM?<5+MbI#F=+<+5HaB=WP<A2Nvn)FhDaJ!RDQ_cr!|Pv;#qoB7Bj}pv3({oUyrw$#)nte8P>WIk>*~(Iopw4)=fI?awWTmkfG?MzB&D+cLQsmbZ#KN6J?W_LiddYD?v%xQO#!YUdl$OgrTiNW0IP4op_Qoi8j!oRLo(f!-rQ9W&00F?3FGoyby&_HYoWV4ahABTyl+V<aW|(u})AI#Bh<!Lqh#JLNF$OL6FcweM|Y6Ts17Q#wX>?v3zDSZ~?zAmQ&MfjrehZ>6<1*WR@@UjD+rFjr1>GSye;2os-0CxR^(A*WQ0U2)nqZ<ln2}fcbtVr{ZTy>&S+*!Yw)!J|<WhlvxXB@~=z;Q9+?sy@M*BGId&Xks_YZXFjFSbkr+p7_%NHk3s5?)(GNIO0byJ24Ot}L_^r|&`ZT<aTEZpwi(_BQ!#M|iE{QH+oD3;pON}C)gq}IK#fBM!ISXi3VXE0`v1JAwWVGRCwOq2CUX^fTc66Zud~7v=u+?rWweKzv4!#8<;1pTW%r<>RJ!EWCkHuTau=~~0F~U5P{<7xR{K3ZwO&MdiXN#@k`?zg4(*GW6W7bYs7b_(>zwd(jao`Ra*>)09U}M36Yve8COqyq6zSKh%CEf>+;by;<G#!S%2C~6iADL0rA_lOH?1M>n4tu6Z7cE+9S}S6tErMJrpM2_$wY2}poE!joe^AMjLmZYA;7QI2vAm~oO5B5QqDJZVP#>&uthnk%JMR}tUGXf0*qk(Za^cu<&;?3WSi{h`HZ$8n6KXO&Ph4j$AGtnLJpukLEBFyxMXqaqpL2DQ(7rT`=bZw(h1p|;Z{BJw|wU`x>sT=k4k+aR^P(tGtqWX&D-kkkKhbH7RB;eNNym|x{)fLx*XIr|DgzzxK_*)>%9}hvigGh#yR~N9c_|ywt=JAwpQj@%F-sR;cGe}Zjsy|-Qh*ajIzB5_T`st<olt}S}=x=2woC@wK6nHs-RDLdfeln#DysYt%<^J{|e0*`TBm%e`Iw0X~vb&CzOVcp~`AdShHOg+kf$y5-p%csY#i(4BL=mTUtzCi^xPIk(@MercI*Wy7}W94H3#sAT!fB$e9(8@jGJXyX>@01&3s%DB23osf_eSfmXxItbp{ZSv6gprv=nz{3Cu#kVNgdr#f@<sS<%!v0Jtt=Pxhz@<!1gn-AWqP?-xjW&#paRh-JY4R{091zd8SjJT7!O9Eii2#D%&f84OSTupHpS94(cPBl$YGCq=}{v21f{J$~>W50;ooixpvfF*){JpEPVS(7hRT*z&@%0d=aq;^w_uj=zQLdEGUqK&B3JvA0jas&vc>V4cp?}rjq{Wj*gyTo3rRkt(a0S2%;k91Fm>CI3pK^hDH$bCU+c<j#XPQCJu?fL^DpMiG)jEomX*73ePMlW!7c>H$cA<n9jNkH+9qavjt8tp`MG#9641KXTZS=W0uf3ZG&TT47T2Mp2{o|^5{KEf!C=ftF}auyg<()fi5kcSvk)sE-CrXxgg{wun==MFJ_v3O<!zb=0D)-I`3mw%D57!ZuG90)o2U{A|$J(p7Rgs+|;35@n<cn)F{Q(sy?2n+fILCD5GLajOxAEps_u0YzGA~3X{v7(U^Ze<&nNJ91kqXTmI)0=w5SV3DJq5zN(&+^(<pHZ#B*Hh8(JtvC{V4g7Bsd%r6R=EITjWOucai)IIFb8fMblP|$@A`P9B&cN`0`ejhjsiMOjZ|sr32o-lnzm_kE+-t4SDmA=`WXpmGayX325<90m18#f;+?agv(Z(`g7u<SE1#ULtar<45fv-D(ByeGCGm?oaGL5Qhlw@UQC;sREUbkJt%eJDGJ}_^LgJ-)%7Q1sIun%cPYIV;1U|Um{L#}#^z`s}sda#>M=kXLf>4nrAZ!{Ib0P(j-OpK*BdZES&WzoN7%4ldU=GsQ*Bf(jPJ?`J(r7NGvd~zM{bM+_<~)`fRt>T$-cX`mLq<`v)a<Qcxr4RtK^`}O5*<!GfSpa`D~B`abO2@dv8ukdxqLNnB>3@XW;H$vLMaa07*S9{pL;^pLI-H_3A`8==!qoPBw>}F5oDrgWITbkh}a<`RooOf<91bA+rwq4EkdG15Yv3xCh7u^$W1QhAsD*4asmqw2xv>TDpdx?N=eBdpblfj9iM7z%R>=ARZGI0nCL!Oe|WJhrQrharRugbmTrs?kOM<VB2{Q~ghSSC*A`Rp0mQyDH6j@`DQST?{J?KA9CGaarKGC~?MOjVp~s4vClZJSxMZZ4ID6?sW{#TTXZpTX)cBj0;LL45Yc<TWn~|}mtyahZ1{&VMQzL3H$M{=2RrkL`;`wsz6$?S43MVSun2F^zoRcY92eDAD^)8QvDTYOxBzodoejLiCl|QrAor$9KsHBp4X&Pp`3A-f3yXlH01lK4=QVZEeUJQ?wc=LcOYf5mgv-nNAR)})413Xk`4|(O69<fLNE;W&+;yn$}Hy4T~$d#wmO0nMuSI_fHgYsYf8|yo*cjW<rJPbU;cwYkwTz%D8Rm;@(v^IbnJxpYN5|%<5nDACikfKu0hT*S2=ZvJg3o))L?^JhAELVuRSZmuy`rM@$L?q8j*$oRv*zY)DrU~}zo9!TH@2axFY3rR^9ghXDA!~`VsV=F=N7)gbS<CH=#`620)TQ;+_6SG}m2<EY%-x`Gy3)~+u}K3mY+YpxJZc&%1N@Xnn2&L^x-$s)JNC-Os#UgsHrMWd3e_!DmuC-H>U;)74u`d14xUlo2pfoLt%PpR2)K!m20K$bXIUe1^LDZ4bNsaUF8@{C8^;MNi9`k$)gvvM>c}f%Ef<aYB!te^+aC>9*>p;M<9(Gt`56J~LOp{3m;!_u@qLT4R;1bWN#z#B0tD`AypN1e6!v7HHEbD`*cZdz)D_fh3WMslm_)HcrU{pNStc`yWm!<3P!k*0f%=TjiQkqvz9`(DEf-L>cl;)sdl}u1slGdZM%x{de0F2@G100yPE)sDpPZ%vN6GF(i)vd>Ek!9+WTy&?c^PTWE@9MWOSuAZ4@RH*!sHwbm{7(2lc*2e_y5c9Km7RJ-@bia-yW^!wB`MUuNzq>EiWtJ1gacBke9ZUhIn@D9R^;S7Yjrb=p5jMofLmVG3fx1po)LXau3vkUHW1ryd<K1;_wc|#Ad41CaL5AE1S04CLf9ifD$d1q=aI@{XO7hbCr1@U(&{t+b12)cckAFaaC+eE>o^|69NqIisWQqS&B1k7kpA7iDO;Rzgy-pm-nPZ`>@A$C|Z-3qUQ5M{wr%EPMe_#fOMo&7Ry2D^I!}Gq03s+dSNSJ{NI!&E%~W%n`10eT3th;UUK~i!+!}%WP#(&7Mk}Chk-n5!~RU;%1bX<5$NJm)p_L0f1hn|0BJZN6mPRbAvJg<X&-fVioDErezL$Cc|$w9mG9c8>qmkU24*Qf_Pb`~0WIL%jNLrl-c)-}IMse}_(f+`(kJq5>dWF0Aig$kP6}FWLwUfQrXJsZasOfXr|PQmj}s-+SDFj4CGEx!hnQ|sCE_*VWh#0ncemKa%3ZmL^M}<TrQ0D>@QBJ9Nn+>)n3mWn=2ocg$IUAn$PwLmB8jmN0wVJ9e$FBWA)PVJivTZcIJ5v_!H)Wk1S~S6BTjBnW`L-M7-g_|+B;`xG)o0Hin%oI57ir5yt9%yy>OwQI89-bL$e?+3H%P(ujDQn_|-ylDJSsC`oKpu^l(Zpe)R;f<T=<58<=@y`&`5jm?!D>6XvFJ>!-9#XQ$?FRG>-SEl`T;og|ejB}yHQbpSfe4Tl~G<n`&9_lZ;E7~D=h!U7C{t^eXLWU_}}@I2GpLqg5Du%#O0ahbi&qIhwaxpCSLpa3GsZ{J%yUs#en6-U#|DAGOys~Kijs+YU?wy@siGX5J_aHbm{H>lR|>i@s2eL&c@??m`Cmnoq;oD`(+?w=q$+ew(=`J3{*4FI8qRoP@Ap|{=^=0ReF!CSAHI$r;OytO{&Mc;oJRqaRWrhAPc^9NmEoB(jecNl`Ito)yFBh~GP-vi68k^O?<w$2wiImP;QMt!t!c>nkxU;g_4`%nM<KmV71{xX?={igZ)8BO0;L!1-)@C>T?<?E&&vhB5oh)M@mG#JB}Xmvw7kDKk)!m77HOmbgxZ_fOKAwT2oljrKr<EW|osi7=!hru%a<q+4%IJB0{W$5#De8UA^+>ewt=9z1qu7a@&1=@EFiXT7y{M{XL|Mc?@KYe<;QU7|q{_>6+y-lVG7Mt~&bu~!>6@m4mTg>TwAEDd%8g0GBG|XS~QHZph^N~!vPNtKU;-ZIJESqLEKD!a3h41y=OPq-H&LRC`u%CaAi+I35j`x1~*N_!rgvE~I-Ua%;{eCt>DHeJg?g$S)vsbo2Qafkb;W)C%DIgss$WX|#A_ym{7lUJ-Ri3jmA`IH<m0a#^6}?I{!E*n?8icKo4rEuD=yYMR<0U%jNTo5_bkONKZLj4(8}%mGKLw;l_%R}IH@KY^?6!|>oxDAuVleGKxqflK`CYL29W35HY$orhQfkZ=cHn&*F;zUHSclrz=&Df~FmR{bJszUS5AdzJAf~f>eE&kFTy@m%;Cnx&gIRyup0K~u6NXc_xAW6lHJxYhybWlHwD_(`KTwQl_Jf!%x$aRF%01P8!FzzGMwO-I6)&I&xp2V1XSb?&5Buv@yM;<qy?t<3C%HpD>dE~(?}6pFueZnjGxc>%nkxtAeA|f@oo}l+z!o}BgG_bN`xt;+@%@Z^U15rxOk*rnk7iDp#SqXB#Yxr0?6$?6bb=b~g$AI2EeYW-Ul^85vmP>Y^9q{$828o-<vCK}oXSO?1%)F78lbh#`Jxk~J(~}kKuZrwxZQK}EQBNqS0AhwMbv0JEpwaisEWc5sgtb{D|X$yxsw~+mxq$?swP|?Z)-1C^LkOa5+5@Od*-yyQ5*uw0z@4U-Bq7Qd5y||#zPSlZ#~|-Nv$&{s6+^46xcgho;klf&x%v$r9O%xQzdE0_s?A}^`FZo8h>!}j3_pjcRki8tS59{jc{rCyP#E3WkbfL6IA_C58q5m;j0>2B3-)lvP5J+hqgM}+=+x6v^|W=Ku8s16tbBg51QU;ImCNY`f>@!RBXp2zo=&xHw^x|e12e8WDJ++BG$CYY|;aa6RAwRjbT>D!1To)zV<O$Shn_I^{wl8qMI3Zeg+fPbAz|4wr1dEZ7<RFPGgcNvZ4QoLM1g1-(I5EAr`+Ux}G+HDC@I0ca)GuZZECOu4h(cupVdUN>vYI+3iKoYkSxMi;DCf9a51wG?PA9QdY?ZEChfya$V{=qCqc>;e|*RxIy`DIUa!)IR>z+9v1-(8Cd>MbhOG1camG(P^}Y0CJLfGuO}wB2-dOAkq^a+cEpwfPFc8SsEd5~MP*7-jueGnZF7;8cyKM0sFWFQD2(3QrqLUX5Y1>)-fuF3$e%k^7~gF(Xl0QanvSh8NT`bbHmI&bflcDlNr~BY5WTD?OTtZ^Di9cfo;mgcrM4O5WhKyoqU1ox&HGptj&|8bJ5u@2E<;*=mMjB`k?wcFl*_Nam)pf%Jce|+W`shl<DC=aXU1S7tYm;Ztj-EJZxPuFJkOvRp+6W~B5McHGM;arBhuxSE?r$4!u{>n?QEO6JRnc?uq)Icz_NSZwt4>&fJYp7F1OD3%gUm5DhI$7#)`<(zDC<Rgub!?k0_6-XS3Wh6NWZ=#208l67GpRy0Joqk2bVs9sk@>OnEYiW=SG4xejAKYfP!$IXtZwWrPY}yItz&B}|)uxZ<E&L8_b5*CBToJ=g;)jQY)xBu|j#Yr95niV4<CtF#IE|7|DJs%n_rWPRL2(RC+VoJGPV$#tR@)mKuJNe+g^qxP-OAA%t-9zw4^ns5vc0j}pL0x6o(3g6Q(#hhr(vBhrPRLfUJt4c$8k)X~7JF7WdBzg!YGN{X{(yWJVq;h&)w7;4wvA<+8%pcb5^KB@N%2ZB$A*kQE#O1bc<?a%aW}c869rRF}qP@LNj!MU2pe>!m3SURoC%Rpz<Z3GTBRKR0A7LHoP=T?^RJ{mMXZ!^)*0EMX5DhNYBBPmqFQSYK&Vf=_fT=_IF&Z38$%vvt{m#{Rmw_0gLG$4;i7v)p!Gw?dkOC04U*tp}7$6f<3qv!ze6+cTo!k2ihKoD{^od-A&}KK`Xd(5f%;d4jJWA#r&P!WV$zui<7~@Sz+2REuS9*myl$oiq$u`2Yi*kL`kkZ!N8>R=IEci|I3*aRI-AII^N!H;$-8|{eXMUTRuu`bU8idgWD8EjeU7f;bYiPZ+?MtvKRTooygzs}2Dw`1b)1j4P002qxv34r1Z^Iv%CRFPeoD@Mj;>*J(3B~W(V@2efZ3j?RlG+YY)C!DD$&+gu6wv`9oRf9<vlw)v<4bZ9j~}-aksGBE%ECH&nV?AfEfIDc$pt1^C!@?q47ya3ZlB=dq?YcR_1Ngt0IFDEPpb7mBLyavIaT<fg~$Q4ZMRT}Q&`-K$s#!REPB>FcKIR<`mM4TqReSY-ul+txNKWcA;orZW>AW?t0Fa+K@O2?SO_SPcGVDEQFsr}z`cwp7U2<&W4`8MQ029Ot4C{EO<u<@3XP^Usd8VeLo&GHLuR-~V9X7FR(T;hf0N~K==iVMveLHDeqhxpxkC4Z$D{VA=WJfuQZqhX)1{`N3#~4&9*MKxO2uSqR|{bZFd2KOLaVe4X`1h^(hs^%pp{i8d1F?4=6LIRUAQiuLl@4W_Cy7>3gK2}`@6(*?Pbt5q3Xpec34G3%H(K_I1OrDJ9(#gYLn)G5_ev-M`M)jVP~r1spaP@NiCSBO8J(6aX=6Uo|<-hQmM$wG^>^sB;OKks6oY0NIQ~uXo>90o)C5jSUi_-I+AuaM><rVQW6{|U?DT^h<T+{TPoB+h%F_LiN<-+da#`k4s8p05!%Fy7pR4YBrFwEMUaV+b%Bw=<cyDD(BdJ=oAdMroN@Q6nStj5fE?+r^FdF)oJkGxePwYVfGx_xw1j*oZ^Wnqk`YQouriH?m6xvA*iE5+N;q~2Nqeg7#(nHm#PKWcl8|v6KZ-9kN2KJaXP5|%WvD%cbc^Nr9!n!eb7G1iwX$@B&?)k5fK5OFhKq7UPPznd!_UYQNMpmv3;CCb9c=xP#~l~2MNwNzJLhuq!18usJ%)k5sL;vrBRiSKw+^STQzQ=^3RE%?5&^;ZhQJzW=?BF>{DFaCj2~=gVqotNa1y$OD25d`unc$|zL#ET#OO65QG`dx@+^v?6IqA6)D&Qw<)sg_@iWXYx<U{}D$7WqWFApFQ&6yOa#v`;$n_dDz93#27;{|!-(A{Dz%pAM#B9<xfljT;q{WW3?$%61Ub;SSpWzGgroX8suX7P-R|vk;SSi#_a;?<8)WJ@VXRk@#KRWIcD6irq*Q}v|*w9#s@jXe1?lPY;LSHz6yv<+~OPytbq^=zQ*|6MQq~>zgxRBxdBchKR4>G$#zXc!^XJsy9AjtAV?xSm;7y@_CjeNVNOUhjg0WU)B@|UBDtb>iD=^5c#DR6SbV{kr(8b2Dm`<i1Y3}`&t?uJTe>HeZH)Tu%a>S^?dxOGt1%yRQ3RX33-U{FcIbwo=Z4FC@)te|1i*-3Y)5MIgjqGV!-EL_`9siH*~olR54b&*Fy970)X0ij)8+seEanptFNP`AL}8gJX_<S9-N1~nrZniH?xNcjz2TUoNtnZqcDuJ@d;jl$YN*451CmUZP2Sya9pexwCMRao5cUk*N8pE;C=VT>?zB8h2-n)6*&B__I-Q892{RY6$Ans$v<nwl&^ahJ8bsMbgFKkyx9atfq|=N-=<`1RE_s%fG#qv58u)FfWa_8B$`MY70IBXtX|1J-qNv4}48O3RF*1LQBNE_q3>Wl0%RSh=A>2K02MT2*H0Nm=bWen-Kw_$z-(5MKny-Bc6Jqsktbx<wgf9{>1)GyA`BxX30msaX{>!O_i?6`S993X4g?72}?_;Vvpj0n);(2O;MyWg1#+VL~r+_+UaF&|qPXrJSTJ#&8^LQ>jmg%{B<qYS7If8MaQN6wO@!e*BmuRCpKy28Pt-38_ai!Qfad)9SHy;d+F9FM}T>bxm_Ks5L-D(dY_I8)q*o3D?zz8A6|6BBS2IQDQYkJrDR3;k&VYz6j2OyTqI2WAzPmeyV{6u?h?O*YPYLV3=V+enbHBM3ZXS++87IqnRz*VhQgMS}xk17#h`JY1{<?T%lcqdaj06Hee>(O#oY-;dL!}=uTL2MoppyH4rihg;I+q9j7%Hjy1?qbvE5F$YgukYm_j(*<p&~+F?{ZYoNYiOf))445*?<X_Cvw67ZFbF0<||?!wNMgeLx6g2<irH^r?ayJ3;D`y!H%fD~AwA1IM_Bkyz*V*~w1VFRVw34$?(MCv~vzeDD>pxN0{xM1|BS0gV97oiKh+@L9@re^jYR5aV&J9cuynf35ccMMJ;X1R8w9*99K#>)D{MD;$nXyX14-FPNW(^DG(N!puWo1NC(XcAG|o_O+@eXgs7G?AdaBA$pG)dAB09tcnS1;>B^$Gea99e_gV#IrU(hsI6`ng)qyy^Q=AzNryB5wZ`lj7wRuv~hQRpNMQkkg}gH>5iPq!x49B7l0mbj}qb}jPgU35+RF52y3S{W#devmlELVo0|)9r>@rIcWb)0j>zs|`6{aSRk;0hX1$y+kF}`fKm!;NIK)m_NP+Obu())RUT?CTys<W;yC+34z&ROD1%pH?h1T?vw`?8PR2lJ6ItY_yBr>h;1t>kFQ5>HOsNtc-T91i`>V8s}3N%RKGBfT-SkKE&-+VdOADuGxXdoV8M%G~FMy>W|+*dGSwz|S=Ik%_Vokv+A`smO*&V^p*PHn2fJ}6(Cl4-Am!I&*&JokApW>rKUJ_?4J<vvQX&HxY5D3c@Eoc5qsy4MPs_cRW_W9zyEqq+oWobIG(w8TjOl19}!_$h)wSZ|j^qJs3_h*SFWoDoyEsYo}sU}r?GRR2O;Di%@i)LQ%aCl+`S3LQB68K?9Jp;i>_TE`dV9fQ|eswUZeu@8(?b-^NxDI_|)P93guA4&PJ@+u|u4i-67uB>X`ny7h7gLYsNnHEwWJ_39u=B+yRLTFQkya!!sV5$4W^t;yV?(ym!UrS)*!x!`Tx7YCtqSOo}(cw5CDsjbahrlXN6-~Ny8+=YPV=!#twS)Nx()qx90X-l+mzSV`$Fjsdz+EN^xxv}xNp0Ofm;EK8kUA)nYS)z7@AcEF#_s!z+&D3h^YSilI{(Bw27RGR!uEnoKm;<vly04EEZbjjao|CTunol`m`*qA%*Bq97a8}LzG9(8UxQQzQr)w4WMLC`j0M+&WHwQ*AL$(3uP^jYP>Np?aUy4!Rx=P5^9u9z?CM#zX-pYcfTHUZN#kER4O;rkT+z+s4Kw*D$fUn4HB~K)IB)A*Oi55)vcj$OIpQLnJI_#ZCC8%)R32kSw>6HYQ5krw{RTf#6xxYLSVLsB&jOB)3HrfWSFa=Ms-+P$Cx|~fTKphfUrn!LH##Ci==LwEWK=wnVVj7c;9{{iFD}@B9YhAyOHtjXSndU;1O&dQ7D&hNNZ(AA6<fe;><ti<q{W_#?5TF!lFtdG1UB?7QHULl<!Cb%O8%*QnIY1wGhAdEVoEfg+LjW8TH}(GW?01+x;$9JEO6mEZ&2IRNreRBJo|OR_e*5`alJy{wkhY-<&K6?WJ*0G9aI*IGlWqnnkGp620X$#anU~3nTcRMLRqpB4LKIlI>ez?|CH$o-IR8qeou`MiQTx?eIXwMhL7(yS}Y2*B`T}r{AHiyrq2jO8EK*uQ;T?UJm+?q&n7lM%S=bW#NdL!jCkizO~BGGF-CR4r!*ay+cPR@{$QKG?BdV&D1A*x^xdWM5L*pVVmROgOMDOtGprM+5dF;RizLY_)^Iwm{n={B%JNajO4rFkj1Vbly^{#FHb8fI<>&TL2G!qiTIpVtez}L=aQ;&3et%ufUX@j&t%j7+BUh-UOVm^y=e*8glr2IFb#7Px#qrtd_9XR9A_2_HViRZrh|}3n*(2Atxg;eM_Xu2T6#18)lRWJ1L^6^>36M%$CyEj43{Bf~^wbU4_OvJ>42^w=Na^x^--JQc^yg8G+ZN+c*WhUm+xdfII;8~N@Bw8e#bEvKetrFg-$UU&*wWN|-!B!JKQ8|VAYI_JT9O!*GJPLyp^xE21u(K#HH>4166xEay0Jm{Ftl=a0aXRkZ%_%^RvU*K@tn8_+B%Ug5NSj^pxidJ(X%Ai2=`?%;%!@WF$@`cB>yU|S;~ul#zn*ZFrJg`zgKvFkncXoT7N}_zfKcpcdeulIQ$VsHGnhj-O6|sB5^=9RVw9HjZA>W(c&ulepvEjwoEnlL#!gp9oBfs56fZ{bXb*;m_Otu&Q~}Ey;-O{Y$l)#x77(ORSZc#3CYxXl7Y-9B(j0)XuV(F5}Glm!g_r&`aaAIV2iPbiwkw1)ba6>OXHy15X#@`LO#iy4jAf~FcciCx|}h^z-wzB`*G4)baJK^$bu(Xf+0*j&I+U9K)olq7N&!HiZYlzv5QPf2U)rd#Q-0C&Y$qk>2ygLKdm(7L78AyU~o<95@gAVs53Iqc?hXeg}MaWaaivv=KZ6HRawZe0tgg!M79Ze0N5TwzJ+I<eVlRITYw!qtXg9-gfBD>2SZF${E!TkEKYl#k~M{iWt%&*2kNHaVO4yrLi7RQ7c(9%x>wB`4M8E5e@N1P$MLOGndRDaFw0gsg;cLV?9HH0Y;!#dg$SkS9yZ0q>3{p9@cs<bnx!bjKN>bt2tlxJ%rLeeGvJ8-7pghr79g=2kw@fY5EiACQ+u?Y_k|}i0k9bNVi=H->B(tUycy1lajI!og>{&HK4Z!Y?rVC1ff3sj(>mZNndGAga_dL><Ojq#FSS(2Mp$&5v&xWtVj3kxDnvm7)mNBL<jDw98HyU)Xq5nWp7*GzOY8v4ijwg}3A~4XImRDhuc4e2I<cN5(IT?)-m!x%L?$$uj3_`?lVP+XI5Pcp{2@F`t{Usyham^VkZed0_nc`4o(5jpd_F!ZK<D&-8D??`kLt~|L`g^-K9S0j=tv1|_}C%oQ#YxHA2Nmk%Y%XJss28|T=zPyAtB&G-&U$}WbZXZmUP~MWt4>{rIH@+sfgSTA2b7Fp6c%;kOI)`I#6Xp2Nb5;*D1`hilCmD@YxKEgc5PB?V-gyWlr!|7FpXpNLpOQ>sDz0s=k85CG1ke{hlayLrKl-SbJw=xHJ_VSjEn8G72g_WF9TWwWgtz$pFN0bQb#Py-QUzNzE+T;|FIxY*Un_8|B-o?hE+|-1cbRX3#$mVT$YTPhd^MC3>hi-Gmpu`^=M%!j>js#-r^0UKN~(>9e^047jzT?%P4_s-_&n`e3;uOLpQW?KFcP6S`PpjBE{s?nXwjAXOclZFVUPy}4w(JPuMFeT6_bG1DAuXd3k(aScvbnFw@a&KK4Wg}w$kWK3c?R8vTpZ(W`3P{?t}XEJlzym*EQvE>Y?uT)qN3vemn;C59-bBAV-^D(?&BJN!Ttet9{5DOV)Ha4NL`3%f#Iec6qJTy5}nYKfaY}&~o<JoS#UexXo=8w97+#pGFVD7k7ldiSxP}@Qb%_0X_v?`5>w;*Of)E8nXR5k2D4GH*;N=6lLB`YC36v`X+$Xei48I@8Xa-(wDIg0I2sBlE**a_Xt7$dG0@+0ntHedB0#NlnooeFAg#>D#tdgamOd7E}P!zq|ypUAXkMQQ0t-*&CiIVu!B>^b7rLk1+PM4s)6G!!x)nGCDWc4c@F7xa$xT!(g&VNcI%!gRef<|FjqSXY19R)7A7W(W<fUV{T$+iK-fPXuWWH(%$WH>1V7n#Ns(?jpP8JG>IXSsJ<h<~#H5A?O<UDk61IVo?`HdbqanI?UXQO#`bOkesIoc~M%|<rE4)&;=hfwWOrnBrw8WFU&~jJ>Zq4xflV1>W1gM{+u5}ZQXP8yHWL%nFJ(Wwv+v3!C>pDQo1yrCWA>_WiakUY3f;9)#^lDb666V3QSLRRH=uUL}&U--h@g1UJaI>sVlmH7lpLVNiLu+!70gX$Q4gRA#g)$VS>X&b#CJJENU6SP>9=b!w15TrZ2UDtQZs3IvDO<QpnaY?knxfdKD6LH5v-*D2Hl8*4R^VZweUD*bkC#nNjWsvQ5B5x<RH+rPFBx@3w(Y5s+u2J<>8EsDV@}l~_s4I_CL|k<;$)0dP|OVc9&EO70<GN+7R_*+VS494`0}YCuBVt<$+42^d7KJ{pD!<wqF^(djLe$Ff<-(4NCV4$=Ma9PDH0YWis~(OV6-U#E2a{`>WDR0i(LH1^wcdR6P0E5)Ko=bN!gEOR)GK^1<Mb|S+1t<SCw_-@)`oy<8KKFMr>GOe(=;V?`U2-oe91bB&(|GMjqG)(=+WteODOtjWVjeUcvb3Zv^WK{jAXISb87(7yo6w=JzVqv#T(qx;^czHsD7g9#SJE=>BU7q7UHWf9DCbttPhlC&p1B0FBnl$}3MpZhLKvmI#gG)t)5-5KA&|!><asu}er?7FzO0j7M*U`PmRq5z5Nvw?sn!h091kT5hL&j;V0Q-F9v<$UG{F*?!SOxfw-^=5us#vqDAco0UL<93qN;jJw#hcjT(J6QzGrtzpf%6c@H%$4BnM(<e!%%peGpWplCna1`5jZnT6s0BZQ#$|(?`n=`T$VJL!?Tv>4TZcDV{ip48lMzS(2>-1*Rs~u2)2H`Al4Z*;;D%6mFNY6?wHhAdp`?wM#$va^tr*)0PC&-Hg1mGo}EHgN<TX{E|g2Us4)q;xThXCDH{@5NKM&Vq>#Ik(aS=ebTzFW_Mj|gcGTF0CusP{tw+S=V+V@OCD61w{@Ld;bzUqRXdTpqLA64F2cq2+vynuNTemPv_+z3BJt|xSxA)*;e1$;PJ}Hlu#cQw{X#J31Q=ix^6*q<M0sw%3&%gTuE7vGkj=hm*T^u=dYiK9%w8D-*<VG=pK$#>Z^2r+=5R4KGJ}lA|JBm088)unFbC=MO0sGAKm;<l8HUyu0#U85anwj1>;NXzOmnSpm_Q4{coPm3iAvLAnz^0;PGa%e>c^UlAmR7%Yc!qyRjZNn%ci#|J0_bxkxYHhX3RZg7ttY(BW2HG(9m8v(*5NLhj+J`TZCj8PCY8Nh0dX%UjyElrx@#$@=GIUeUdNEUla?l7Rem}H9B$8^fa%o>Z4XN*yDU?LSj{m5liVr_dnlGJ<>A&<$=_sHHg}>6(JE>xVyDvpVA;-kN#9g&_hrc3LC}WRZyACVJE{z`OcN~&y(+By;-%5BxSZ7d4y;D;!pTQ;lKYRzDU|RqqwCVoE(V6LYgf5KWVOA;{XXyH^}5?mB+SexL??BB;$+WiC7r>kR>K)DJbsPPp>ycX9luz|(ga5A_mLf<Vjd3MJe^{-PN>z(QkbADq4T&6Uk638bu0v-=m=TS6zQ_U^RM2xdR-e$f2@i8SO{(KvM?|MAvLUm4V7pMRl19O*e^@;>+9#;MKQum$@*gv0uu$C0f8#fMQtqPp4dxb!!AZRW92Hb2FG}r^}ZEBTxLCGri&G3J!5}qGlu(39R{8^2r3*+rmpA8wg|it&-Nj*eK!|<d$_98RnOppCGl|TAY?PsX>!aIF2UquD!Y-#btU@fqlgoHeEQ6w1Dznxr+1{Qm7<{s2bA4qwe|HW^ePY#AdQq@$4V91@m|L$yt_;>hx$7dy$%qTb$Daq71;i=jnS)WDpc__-5#doCBs9{oqc1LOrVBFDDH%!(6)}6LWxhB+0T*hOeb~#w@S4Arj?y1**^CPuM=3pzE4y10!pq3E7A-$>wTo{MVAEfONjA5VgS&?Ddn?KNKVzbdlAzpcq1~7h%VkVVaf|wiEdkou>RLi>x5SV^+RX?6h9?xSIh2|72YWlBz7l%kM~Dg6y=hXMo&NHvTfN}mE{#!nVwRZHnxN6cZA|CVtaCtvGRVQx~e-vW{z@2F%uu8tO0w>{F=3vO?cVHJgH-*`m-eA3*6T7Tj1QzYK?Qk@z*r~>6o4VLt~*kCCM2@ph`|G*>9yX7J5)MB1Q=6qG5EPB&T#(7`sOAiOoAKSez$w@dvq_(sk%s)qZnb*g_Ky<(FN&LPn0dP8QFlM~kU@fl&%@1u&n!((IW^63h9~xr-)0$caF;MF+1_AYg-T6l0ankPZUrfoDLNsfN#!VpY^$c~>W9R*7EVW0%0I83j1q&+m4v2B<>8Djq~L0&Y-DV5us8ToFoCMXyZG%DD!>O_C9($2X}{<u6sFMC9u&LufQpJ2Y=|Y2_R=I)=a{FW%1`((_K-7d&;@{zKg=dKFlAhiwom_jG}rgkDwjJVnk7g`e`qeqZ9D(%6~JMwwiEA@I7`{OwtYS|LEwsBuvsmTv|+H9UPs>O{tVlEr^0{9+rU1rSd8RtRFq&9DtRdasJGTvVKKz9op;w9c=_m41^Y_KY4bGVlK3P4%bciaxFPht_2r2bCaC9VW5wZ3%F*XQgqFwssr()Kpe<(llmVfa{-um<x3Q;sM1s?^nz5+ei3l;u=_Egfi|Iw0mZC;U1TpdRc6JOVb%5>rJW`R-~jxQC<g86~{S|k_bQnP0=VyRBIt^QSueS@PT4Kc&C8ZCWp19!EXn9>1rgYp{D%mG``)G+kpb-HxOqcO)^2b@A^<lr+U4@*Ln9k<_2Bk_fPJT{38D1@QbwFDdor>=d?dj%VHj^Wf`~mh6QKPfB5d#*Iyie!+vr9Vfd%gy)^xqqK$p~-rHO!h0~bPeh5_I;muRF6($BfducA<tF+q`mqdGQRm(#cMpV*GtM=2>T-2->O98QUzuVpY3tnSdF6m47K)qSmeL{uO$oq#zMLUtC7L&w>80Y)v(p!GO75D!9?G3xmoI18s$b+k)0Ml|?S%`)bYv4t5mykeD%JGi<{QA?U&#&f(4^5=zLs7%^$Jd|9{S~;Y<_=t!Kl6rDH%`{VO%S{CJK((E!fKa`cy76&C3t(#S4t^sV(~YUHqF7TC!gVelY2ABV5xmd+{m=_2+NgWsXvBOcrhv5j(_ZR&$TeSFS+$BtwUmeIIJHqU;WR%{8Qkk5LbSmq<*vR<7n(Jup>k~6+Fp*l$$5D+H<{XmR&OPGbugy2g&ipxaTjbC;S$4eEIY3*T3BKLFD{ANv*eqZTcZ8_ufVirhqxCD&kE)*VUD0Xix@gYKBW(c(Tjjjh+B`n5xw!^m-OX!Suo%P5<%J&)?m}@<09j!%v^yO!xH`BJSHR42>%Knsb&|z;U;tuLDiUi3c+Yefhuq{=<*o{q4({|NOfNkRF3G*M|MI%|?o&ZjG&1Z??xBW&bqplEXE#T_J&H2sH{fuk7pQL}|bKx9lPn-;wWyLb=}#kcq&NZ0zn`3(!(?gMS^>0;^*Wf0UY<7;dwp<8JZc$)=(^O(BhLR~LZHV&XS4M3c?&jdbi~&4oz!p9nK^;m>s>V|-kYc@a5(s0m@aK7qe0TkAOKDl-*D4RRuJ8xHLW{7esM{k%n`t&6#K?&RR!HTUQEx4&MmzdROWy5zhvJ^i1h3kdGg)Tm5lp}|b9jcQY5k4YO8;Go%LzN>BlKDn#wP!curwXk$;Z`5Y$>wx1u^9wl|X?`vGBe77W=gPg%Yi$}%I;;0X@O~y^aX2MugKoTOgq4?s4UE<ixTgkQh}+p}Bk#g{D{M;d@V(w^PVWmI+Kk3wE^A(SqNSPip1j`4u=fWVv&tVo`fTeU_1^TnXR2E<QFtjHH@qoTk42SLd%S2*2fd&`@Nl<9oSTY8WIO4sohwxbR<o^H%~~oO`20>T(6wEH?pw(^v&qqDW+VF=CzdI#@>7s#0EQ0lEOQhA^c&ike|o@nkNUzzNdWM<ut!g(dulUJY7hz}@~*K$Fr$#HBbX}!Ob`k2pw35^(GxW<^{c`-VifK6H>r^4m2?j+*GU$mjGDhTg~)DQa}7oj_m;=Nul=?{Z3fS`D_tWw*err(L5b^kj%BcprUKUR!f*Cq9=)tE7SO~<ZyWbDGJD!>!y2IDewS6?;iviWKshx4&z$Z@VDK*-X`{fz7F{j5q%))3Qzu4H@$As~pYq5htAS$U@oJuZvzgVwp|``T3m+Zn_p=7e<Z)$l6N=VK4JP!CotZjjX2kyU*j_GbUchmtC{2j|BZ>&knzxtefl?LcV3n=)$7%Ol-FDlHto}~9R0i7$eOfUEb2oraM3LPPzDCVakO$4Ib$_DACNFbL)5g~k4H2xv%Zm|yW^EO?TNQ>HsR-yHA1DZcRN?z*9a)$5qU*AAQ5wH%XPH@IB@cZ4<~$6b_Y|QKlW2>Je8M>rLRj!XWgbK9ZAiaIcqhJ;g)ouVu%P>}iKrW5qOq*AF{m(d*wVEr0MBomNC$_@UFz5c_#ME@SqIgffd(v2;RfOXImk<l925F&6Q#=8=j$uzmt`HzMc?~DUS@)OD8*F{pwKpBqBFwt3QpT5Or*g0z5Hg6Y3_>DT_&Fur?nM!RvT-nT9+3^kt}@EqG^p{x4oH#gen*}OE81rpXNy7ta#f-uTm(WA$LUJ44^QxTdZW;)MczaU!DXd>4B41wryoEfE53MZUfif5^atARqcY|QRPU~)~NK{y&895n!RkAtcg&K9)jO^s13D6PmAeMjElA1S_e4ltx&jVA{7Vq<fvzsR-a?c(cufUt)Lx#BYN=^IMuoly2*{UP!J_;;dy*m6%}#WDhc5&rxW&2j$Q@Uij725Mc&C8ccCl_-p{c52%I=-=wwX6W!i;WElgpTc8#$s=B01jPLRW3D-piybkTBj^0tusBnQb2FN1@H04A`SNtTl{n_e~m`5YyU);Ei=4<jS4YE%g?(gLFyb-{j%8bqrogxFk|U>)S757ISHkTRxq^~yMlnE8FMIyxs*9qvD2IJ2b3KeP@td~P0T3qA9m3f}w6->a6+3*-AHt>-Q!Qf^wicRZ#xPkhe}>IA%imGZWccV{U3>Q`|UA+WSwZZ~&kXs9PL>46ExnbPhFdT3CuRcJTDB=pwdjtLzen(8D{1A$Ul8CZZ(PHMg`YG}mVY0zwkzKdX-bAFs4DM5WL>n?x|NO;@*B0qS6WE2;k4sfNlsC@(*f!R3Q&%e*2C@8jn6+YnLvuU3<^b6>FZnxM@E=peiT-$FGY=kaYW+1$!8u|?anngK!VLF68)kH|f(8_>40(JRj6X$?++!Cfdo|ti-WEfTgob82c7Q?LT$;H4S;n3G~LUjdp4?kwBgwe4HE4hlbjzae>IvR!qK=(e>Z(m=3!PF>x_Dv1NV?9vuUQo0JS^3VbJm%S@C{gN`<svakYod&Zx(-x8Nl7s|7&G_r<kOYJfrgpzX1`v(;JpB)B|vMT0H&gvqG*B{qOCJknOkYz`&|{BZ(>nL)!;Ftx(oiSMwwm-@(sZFP*<VH94SJ2Tr7D45&aU7R|tE6opZeKHq+*j#zGN>uskA-tbo#EOdW2=E?@Ui_eHYSSS`<(H-qRC{0`(TqO5RUh8&J@AdLMs^3HTMd>92Npw2Vkv#9FtUA$<W(wNA3L{+U`nV$w`Axf?FX1#pZC<6u@Z2>yvd&gIsUqUu!a|*{<raRad$wn@;G4H7X-w(qg7wjN5PDBq5(mciQ)u{Ed+V))?QLqf5sz@SJov5E6vbCg!IAxJjbEYW%)QR%Z*_4S+tvmzyj7JvCyN8?*DQKrow={rh=MGM2v|+QV*nJcZm!1Mhuo-Tw&6BfEnsmZC>OpVR5Iw05i08%hO4YauQ%s}G9OVr+!02paVzuj-Jo>4sL#+@wMMEaPO7~(N_pB?Un@cMZG_m4+-n&-@D1`I9=z<C0PGg)-Ic#UL4$Qy`r55fvheTg0mPp?pWT6T@bJnX^>@X<`2SyehZeIdQMIq)^F7V6NOGS@|%B7K~(&^o#LS`TyGBF;T=mWN+)3u-#S!gl$rd8^nwDVA5^I+WUMT^dSu~A@g6U`#o;%YTxDoW^%R__j}wTZ0y@kDFLcAo!i2GhJG^}&aTl@e%*I6tVh7dXIhTXK52RFTXx!jw@n*|&jomp)j_kbn&ukE-Xy(Qrsz_uVBz6~oX5HdKX$o8<XUJ-6Lulp`}hNwmWtqPL0>O!;Cl@JV*0AWPzfeO*!IT~iBSKb8%*MpwDJEOlZT>{^z8g;od@(A)cP8{Wxui1G@D%WHb>J>E54%{_jS+nG-rtb>g%N_$JwmQToKPpAxcjlhDiF*gW)sUoM#odW|JD=TJ1SqW7Br-}T4u~uoq>Zl&w`A`V4Yi6}LQdI;Z0zEMz*ENe;AW5tHU@uBR0aJZcTfwOkg{yfyj@bfY;iWvArlL|s#{*d~n@#uJyC!WzZ=<0z17@d)){Hv2&93d_R9jHf1yYAv-DjLEb1S@F{AKQ|E7OT1&Jv!95<M6a5o;gv_>&Bj1>!b78Lei&*7-!5Pw4%X4kvn#T+bUEhAHSy0QR3ZtYIf0ED!98isrCqf!wyqIzMs?Sz#5U7m>7YsV%w&0js;JMftL3epjZK=9R80h0FMe6jjT_5}6z(dz~%dD6Cxj411)9f++;qlOuG~-GbAulQoqR0v5h*wvGx(ZbPR_Lb1DB5{_cayN+h4(9=pnvo0zChBM+wejlOte@_^;>%t%kcF%Q5enVDmcgRR4Ev#FiLwW@IUtJe9<N#XA^d+Ulx}Yd9B42q2tqMR#hz0bQF^qa#m#+9n)6p|>y_~7_7a68W1#z@3+ZDFX9VMiWPNq@8d9fQ1-2<0sW-p_@6hK@TOM4srf;rH{6v8i-OX5pVZhvbXc^9F~WZ8DZ0x@2qhBKi#eV9eJ&7zk9dx);78x!~F0k$znwt+4Vp_5erVR-`R*aPjuEKG&!5W@(l)Q(fw(Dezhl47ag63bkDnm)R-(lVk6K%b1*ik})|<k5AIOUiPi29#;dGwSId&i`<!G+gMBQH&kfQRs-ctgkLE$|mh`STlq~l<nf3)*^;B55&`ePw(}bi=~Ug=g4#uISm;7`D`O0+dTA@#_OvgzXW>aZs-k07tsmu<w^QH>BXJ^r<4!YsQSI6Mvq!EX;E#SK?STBCOO~FIyTXwS|6?i8z1UeMGs_!Dm8To9L`ubEHY;dd?d8mYGrLZy0RcQOF6iH|NSZw{Y0!{Y}AO?2#^KDs%zMGoCJR!C^4mKGmj9^I^kA#8UgjqsLA=E`jGo(?SdU0ps_pEEEDXXt%5!r6oXH2)v$GxeZ?q&ijHMpF=<)r<AIS4;dAluAcE0Fw5-svaB~r0++#*8Z1)cAXOr-GSYAn5=SlW=fxi&+jg#fK#4P^mQgRuIuBfzyTi~s?RD@-XoCx_60WW9xi(c4tQ`jmwtB2AUUd&_dX}VP89gE$#s>T9EeH4<;I@Tsp;iI*UvZfz`S}JOO$O&x5GPN<zwqM)te)!(MixmSGx!Wufm^!&g10BNsbVy}Gz10&6q?9EridqA+su6?~+M`Q&(lo?0D0ni#hX7~b{>68{zWzd`@|#{?<d;%aXxP?$)XS>SX%>z_&<Vr6XhOMU>aT-VfR&Dn51)ZS&q?E`v1FbWQkoI0gI)BNT~}XZQ&daz?MQv(XT1fQR;FnWoki72wp$)|1DT5Z+TYok2j;jTe<kX(qm{c5N3s|$op7sPDr)^ujXYCCbIGa7b#qsP&?rnMj5)^DfA&nzoIUDeGwsu`nF6FK%1aq?6iOtE+SVMmNVbS;F4eHj-Ec-(wDyt04+<6u^M)%{zW*U##8rye=S=o8OgG~|m=Og9|6xAW<1N<hj&59lsR--3Bq~Tn4=d4Gt!|~4i`ud|5u8RjR~u#nchL3ImL{>z%x>+~WbM~=`L0p0y(At|>v0k6Fy%4aJeEBeaHp5Ia9>Mj4DgJ6n0-52ud(#9aD0MRe1sS<YP)k^VZbRR^43WV`Nq+ZM^5V)xD1%&g%-qE=B_Pc=yvz6^Fb1;-qT>QWW6k{wD!;gkLDf;KT1M5v^ztFi;}wY=Ag(S9750q!!KX=j}lh|INl6fvTj*|N{Aa7kya%~3wL7DMt`}a$|4w5r@*FW_o^T`DS;Fy3G{^^r~RdoQ3HnDG7+@OmYubc`1`bb+l71FrrbX52nEL(K~YiTJQ=UQ9DvL1hFibOAL;#7xh(f}>4Fo<OB<{v_+GuO4e&2o^QU+yhfkAMp;$6+jn~ELQ+EMD)3$s`M2536|5VjV1>Mr~fAN=iT^hY;h}4%OLB&XXoCuw0#aPc;ficpEml;O*dXT9~pvj<AQ}<{f{OqNf)TM#C{yW%bNo&?8t%1{%qUn0-@k_rr%epSmoKU|100gqXR24=s(2-(p?=N#+pe7;kzXxu&$E|5puBe1(sFiwJH>h=pty=j6J{>Z+*w48Y5@29mwZ;hRUmui<M*s{Nc6r>U%?M(-9z=8^eS#^4Lx}9bVo!Af7Zh6HpjWiiFr*jD`;PY{cFMYKd*%e}$Vhphb}b}%sA{`zd#Sh(ub0Gn*zu_5PKMZe-!^r27rC(>c%XABL)KN_cDnYC#JS@A@8BV#*5E=>eH-GVtdtFkM1*i?q#^+pcnQJ6uZJ6rS`i@(3K>L^EOg^+Fh`*cq8B<?hnk3j$QUOP^u5pH%is9*)w<xHUw``a`Bm~qi#|!m@4k6Q<xjqQz{_L+{blI`zZg5e(@dS;LJlRV1Wap7?gX)DWA8u6dev`P4FM_WPRdX2!jO+}_q%fflmU$($Wi$Lfed@KXZZ$wA-MwZKPGfWj=$P9RR?dIyHO1RHb-2&$Au3II)t7xv|W#VEehF|({e(jt94d=GUBiHozUZxN;nHW2kDYaf{|d{b4~42z}+A^1ok<k5cWFAC9lwhs4seL{Lvc<a<YE+g1(SgA-Y|7af#*Lh)N$(oC9NQKI+(2*mGoKH6;qXNT=`h)?M(l!TrJynitBj>{X6V+4r4#R_Oa9>jCJ>4g!c#XthX!i;!OsaaL#-xu918S^MF+`ixZLnbn8ENRud^C?HrrCNy?4dQn_HI;0MOy8#&1q@D_R*R#Sydg*3!@02gq+VE=g^9s!va&S2FhDsqtw{))M!#eQgxsMN{ak5rMe3tHoHC$u`4EustCiUD$#H|`r@2^5}Mv8F4Cs9-7^#xnAg&}<*L_=a8pW7-wbpm?<R84R+93oMLYE5`hfJBBnLU8JBluA((?L{$EyCRLe&a^+>96{;+PHivMMx>xdm8v)voZ_+~`4%UVZ0b8+l~Tdn@(;uK4-HL~>Np9(5*43fX=_o>L#`zi#7&I+OR>=Fy3D6^O`v=SOJExz6jp++2XE_SmYT^}FiUIU0<KRtejYCs$|Z5CO^Bq!l&(MKrc%=+!NO+E1G0tf$1=%v4sD)YpBS}YE5L}t$!LA-YIGk`!WcniYlV*5eeiuw@qy&KIMX^=rRwNff>WUP=tS%cy^fro009?Kq<kEqQj5vLw%LJwU$YW2+qIn#^^wUHqN1fSbr)r0Ufo7AIV0tBqwpZoO{!K5$sS={tUxavi(woYKX4B2lxc|l7|uOqOHXD>IyI>fvRTvA)GAs47a}U^1dMQn1Q%+q_fw*fGDsP5{3RlC3s>mW>B1+vsYA5TN##gF;>@15Rqu1Q!~F-n!i4ZHV;Ex_yZ+*m=0vJ)ipHX4_hTXC11kRf7U+ySrbxOeMm;4pP{?rYGFRgHMIDCh&lf5`>tzi&Jz$<~uIprddme@Hvw1($qE;~!Y@(N7wj=&gMX%Oc(R_IZywiLXyfa6rbfC#PX7C;VFI1Nv7>S=_oxw@<+J0{3N=(lQqb+xH&3D6PSqI&n5}mS+nU@ryohIYf!TsFp1NFrq9Kk7BkI8#nz<7t?u=ub>0wf_Elz{F`n$K7rWmtw=$o|;$4%fK{G&i^i9AkM#qmRCj`-xIITpA8bt4VD?LXr_MvpErfIV%i6VeV|E@}=$pSyG+Y7_i_UB~kOdyqv;gv7LcJ8%Pt1iqHjKS4F$A@IA7dute}PxutA?01rmU(2^l&AKY3ZMSwu3+R_lBaw8cd^Ry$?yJ^W3^{1&wK}`pFUc%;O&1gWE`*!7O@jZAHQGc$ka24tYe9gZiz?ZyFYpA=?VsX>x0`xIuaO6i>jhnTwy+!g(w~FqB&LbDf{U~x$Y_TH77=Qx2XRXlp0i*-JaS~0Xz=ACoHsZhx>)(c9Bi=c@U&6;+%*HroCH2(;4VI)=aJYn>$!IIh8eV$^*x{Y%A(Q|D7SAP%Zhix8vHQ65&K;hEUR9%;*AROslz&jU89FF^^fv1G9F^oFJ(R^D*EvT0u%l7!|DB;(!WZ&$Xr(s}RI;H^-$^4|hcYlrv>Bg^bPa_b4D%<Y`lU2<<G~<9p*AA34_Rx(0KCuWQsM`ExGdEI6wb4CrU`=kQv&;bXk=0=>%Rh>@eHKz>Kd>)4D=Bnno4GC#%et8%q_RkiQq&GX@Ak)H?o%9Dz<Or{Zn;^eQ0v%6f2RCHpNL^;ahAILj%uGt;~MAZP1))n-z6yK^p@EH%KpD<)DGEa43X1?2SPhM5XkL8Nt7<{>ADDaADS=Z7UTwIsHVg7`uP#ZkN}}o?Am3Rcvz#83-A-F@;%%TUf{=PhzY_wyjl$_aQkv9Mg2&omN(#bE{s^4@7RW)RDq~Tc#*%+;(9;=l$AX<^$5ZL%YcIY4j3^bp7h=t#>1>?5>K8?NEryu!Qz5=tH!8TJK5|r-IMlHS$eFn7wu@yp9?)RqNMw4qfi@rw&poB0nLfFSpejx-KUy5%i!3tjOvHz3Tvb9fM1>lM9!eu{6D*W|HG5IYSbbtePaRKecWCsQPeBJy0nljb7W*ZouN!XR~WG-LA3Jg{m+QSANz-A<h~#k>1fF&;7-*Y!g@#woZW}nOWfXI#B(_P%eel-&@e>WEV6+ztRsQld39QBR#=pBpC}<A>`bceVb?($xk8`1R?qZf)Mw8&AWungR<;>IF7Lh{`i~wUM+^+@aj<igqF#(Qo`Fctv=wfj)$bo32wtzQIQvgPxkc=7k=WnLZNxW<Q*PN-Zk6?1`-lgVj@L!{dC*NBf%3?^zO&es>}!BwTEr4hET-hM!Gr5(m&w5l&N9)xyp%`+(^wo*NtKjTX>Gc!vCfPc-#97hfx0%W<I-=vH{0U<Gg2zb?u=h_Zc_m)EiDDZ<T4eJ9e+i8iw|XNzdU4Xb)cJDm_tfsfJjO-<@?<XAomLL&OtjqB8-SMZ<FGH-x5d>olVJEL5=P?}XfLGCkn!3LeJOviE-U#j?3>xs-j^hN%MYGbsh0_te4t+!Hs<YTnuDK%<gg2nP|z&u{A@*a=Pc4NG0_nMan9P@36W;JhSt;kOBmmnZbxAS_;VjVYxCv6k8}HWj5dCd(C+*y}yo*iGc|jt=j#-dJ)NTUoRdsaEB?Qt;LgYIoNoaOS=AW2b5pMm-_+zz&YjDY(zDY`Q!BGc*cW*aTigPS@3Igoi@pBupS^5JvzCMvqVePIFnAWAyYhu=svm#LyoLzF?*<BQC<Pg`?x}K4yL^r~~JbmT!gfJ2aP->4%|k1#F3S9gqgV32`vaLIVXvd^K8EZt^Eri6v$&wlgtZ<SL6Q(uJretTx{iqS-<z#XkcP?h`#OK~Gi!DDG#W++e%OwdqrWrxAdS%vW%UqxPf}8Y=op2`T|d6AGs1M8&J$S9<Uic!oknh4bC31UrLdpICvxo{vSqwRXlfoM@?;7AF;#FA|jS<`RgJGi{E`M=_a7H5Nxo0wTf`#gP<7TUWk9_+t@LHs*0LFC3W4PV^5Nf+JcXG}uHpp$jfCtY!+G0ZLP{(s`c70uNJF7;MY-&$<R_=*%$Tyk}Nt7+n`=2o(HG_K2ssH-cW$e(~#M!V<B-(}0?_&~$406Ag2hsJI6kpIm7cQ^=ffKQNkm#dN9)?wABH;3*-8H#e0*Hyjor<u=HxXs@YAjH8o_`xwlld~XH8uHNzG*yVLeFbCGH3kpc)Nij|vC`t{aiT}>5!%Ml(vu=GdrbF&9%2naDJnMj$C?Op+Lc_DL1w~<oUAldlp)8lWTMXW$8d(4#S1v%|&g0%<bel+%u%a@Bvi>pWh<o;9qgEBP-n+|ePOVzq9=?HED;gqGyjvpofnU0mH&t2RdXu4ECVc}&-|H6SKDjZ_u#*BdEG^mQDP&uSu>|)MH2C#frj!g=!%g92#aO#Kw^5Km@DhN~$3j!m6sL-pQT4W#N$wdSr*XpbFRBsN)Uq}W0JvWKO!yH_xv$DB3z4ASKSHa&RPDUbl+LPB&s!+GM4GFNi={EP0y<%0`>aCv<fC5Wg-7{HQPB%3S3gDT+N3bnAvQW=76DPLzYIsev^Joob53f?KHk-C^KbQPC@RGvNs0v=xnz%>vCx2_gJ)q2X&~_o?$>>|y{>tsdp1OtC~lAHlr}mL*mxN-eLbj|R6=3AC68P*MSbb9(6uqIKD?aec%PTfxV%fS8<YGD+Uzb9C#J<xG{wFSY}WfM1o18F3ZXY55g}4W#M^A-ewf3+o`}%w{Kv3|iXxDJSQOi5s8R9QT=ZRI9&V-w1q-TSC>`bB*!-Ftv52b>`F*TlaNsqCVDo7la^4tCG=c)aNb|?Ass&a6#(FW{Q7@u3-dw-UysOp1VJ8zPF>=A2uyHEeJYB#&Q0t`}OyJeIhRn6H)?o{t!OcHAV&`xRJ_RV+I=C_M9&LZwA}&?sK&KQIHZ<T8o%ktvwQ;OqcL*^5iW76`??h5$Y?fhvP&$DFPFZGDZkl$33)~5scw@7K-EXGoy|pKxiaV{-<?Lx{LqCDO7T~A{sb*J_SiV%-=Cnf^@z{dLB;yq6c#JFa1J<JRbjHUvESmT8df`>UAyd|-S9*mC#HsCS$>V{-mDo)@+i!0j^%G@Z$ER?^#&%HCNgPAa`%R~M%gqclK8uW*mPhN7j1|IPz|W%nD0thA3KX&1MnCBSF;{`iDmDr!y;Xg@b5LSLU+h}?4^_V{ArrOeb1Wp|h)_U~4`f0abiiW2mhD9-6yIc_0G>lahVL^+l090+LjDbShoUSOK)NzdMvjXxcCBjXx$ak?sfXIiE;bX+?QTX<B^~XiqGcJtC<Pz}m``7+%Eu(lC``uYE-T7EBE)qXgWhCb>~g>hZwL~i+sRm^{iVZLdb}I3v83G3zS@DE{G0%t$UUHjNsBZ!-_`4~yuI690{hq8BoTf~(V!!&I8>vfBVdg5sP5ipQ^l>8$54+hdeU;|hYM)<qQ>&YkQAj;m}qfTsS?EpcbyaG73y@1Y``EV$frDFT21TS50r=$_JeN%8sZpA+R=;0`e1Y;QDY>%0CFMBm4vWe^o+{7^c+e(lm8;~94ZeOJ0*H2GpEM&`rGFe!)*5^DSeW5(;q`b*$4nqu}DSJm64yVU)qOBehs5~oG99S+gC?Tc>}v8j$YCN(-5H#=UW2jsC9l-VDXI}>NJ}Lm`W6>)lnw|A&ik<5AH%9YB1hvNwJ8VcvxQNyp4R+D-<PK0d&z_my4S1`v|9|vP_)j!sDub|GdV?(gi)v$8X;6|I7U_PF!kl%yd}jKBz2toI+OL?V4|wFsfY@a-#Py;Z@k8J!x&f@YY?BrK?e_hs`HeC-Ln@+RO!*VIXA|wk&My^q6s)t8$%puOoWU6@LHZvaKOe4LJOw*NKvJ^o3JB)ITqCIooCHe=-%6GTy&c6-Lo@CzZU*O0=1pOTL$;9UEiV+*>l<zu<CM;4mFVJ_uz7E6aMFVj<-6K8&a~DUv5+To#D95jEWH3=Pg@a+tquGu=Rbx$lEaA+M~4ybI9wOzl4dCK6|KTgv14{QUaUr_ZnEhxf1GG9U8l*B@Vh#+RD%Vy}FZ#odVeOFlK3E+&$ceT6h<0xhc8i{jhDW|V9EjNKrY`F=Z6#CUtRxh`V)rj?5m?S<01(^+u5JO9|*5EA`tr(Y&d;jQ{ZJb(LhzO>c<>`OjDQrrITQpu*sZqXk!E}q#JyFtYl%z0Jz<WIPyQoAyzwX?jHs_Tl)aOD=PW5<0M<Boj!``y<+-SojjsFm5Bj#`_3t}CP_)Q(vGsTmqoQ#6;^0hi+AL~bGTx39NMAq@t;R_C%A!lH%4$6{9+^$t45v^B#$%3w4@7>@tt_aA=z?r&c{`Sb5i#}0V#?5}OtT*1*1IaJNitGB@8sM}A(eQ+e*X>-opO7~_6)&91(c-?-j!L41>;yd6>Ma@*1jvC33>>dFOqO2dkz~aNhZ&O=~jy&bK1?(kOMOhq^LL=NRBLJDij7r2WF)*cXc4I=wBa+D{8pWI^vJPd8PXIC`qJ9tM0nCr1ziaJsoN87|rd4~zJI%<u0=Fqafm2WX7<K-2QRPWUNr@Ff@0haTGJpE{ho3(ExL%KU>z-OQYsA{UxSDLF39a47DPjgVPY<CUN58>RdVu!YOugJeIOk3!Zelbid(nBm6b0~_X^=VKd_d5TDW64s*>!6Ao)>cP1|AMf=_ckKz;#rMj<7+2{cDM2o1r->cTK5|s;NuC&9f*+blYd&`)$4Ekbg~W>itdwFBjzpsQJ>()Mh=msJ19Ch!sy+%E%WcjZ_QgKw+x@1Ds?{BF=b0Os0tP(#%VK`s`c$V)D14&^sh*_nHf4ydO=n%Pvqxzfk=uZg|uzZ3b$w>)L-1W1v}ts=w0b>LTG%uJ+_5Gt;^v=2|#Rtd~VbxHL4=Oi5^9H-%i_5u6=yqYLvxT*jz+gf3OpAUPe`gU)!=zy0-k{pIn5EKwPt)eWi4qp6j3?zILczRn@?xFS>@?3UWBi&Cf8;pxrnnc7&;>d${XGAkMC??ZhJ<WXZU7d`5f_k6o%+}!qZQO%jUWU=freSKIj7rq1SrIx)%xH1%s$B>U_%<ZMkQ)QUWD#LUNI}r*m{AKOr&P=R4kJSsKAjS!a+DpiH01E`{G`y2pA=Ulw-Jb-4nEER_L{p)+t5$*sj+SqsAqzfSEPKfXa(GltCbO6!DhV!2%X5U-k^qzLdpo|_1hwH=ZU9JM(5f4@@JhhwmRL2+1nnITY-ppe+cnhHQZrm_$U_v1AgM;TU$1Cav1xR19Fjz*+Fgk2`mny3pW1GV7wW!5-Lq(`5%5#a5n_PtI@C_h$$1!jsw)^2jbgtHMw}q%+55;)l1+asYbq|qIXq3nW)KnXWEmk~#QqnqMm1Qz@p)OF_PKCF+f4bACbck$3AI`X!#<Q{)T*&B+V%qD`mnFKAS!3`H)2Px6I6}ud1&SQm*?a8zRLY9ke9V~*m@D|;clgQ8lCBrQ@3f`M1hwDq@o<2AFrQU=ojy}taDoQ(i5vI_%Iy?RD}IY+l-_Q^TmO8QwlDC5ARg9MT7#_MR7M+YwMB*R*ztQ+a-t|6nIQ{-=3@8jcQ_nrf)2XkR)Cdhp-ESsR&7XsHY-kdwF>ZVs`7mW>L`?1p1*U*xuJF{z&PogRNZ7rD8HIJ?y9Vjmk(NUudFY=+4EmdiOi^``6dsu3_c#_UMJ;7-_{hML}=S8MjU#>b)_WQ{8uek9mQ+AQEzI`yr#2oo=9$l2k3m4+cAC_|=ihj`y?pw(?*iFiIKX;UYBXU+pMZnXVn%fPMV60Aa+#v_BQh0sR8~BQP;5QMlGW*Lvl0LwGiaM(}aW(ES!rFVQcs1M8d;VFjA)0Uz>-aOZk_zq><j(@hQjY&LjXA2zWO)Yq>w9p%h;P|WTFy)e6FCd7&G)cnSajA~i$9yknqTGrz>r+nS@u#=hZW{-`^-LbquSdj1UM8HZdz7R=2ZAe=O_HqXL!Uzc#scgr94-#Aw4m-4~0l~&WX40`P4|1rtlh;VMK>M;|-?{E-h>-bQk?q<Yb+D2OGDtm^1#nTypD`NJI;}aNL(_Z}fz}?6OWeNlSa@`DX4{5M5$WL`zJhaWMe6pC8_I9^d|YDcV-<aA+q+4BAG5N^A=#ij<`tV(029-cs)-_<x7?kvn~C0BCw~=QVq|JzFH=!vDk7PIb{Z5=r3m$WNo|OAc0;;y2(tm-!1sM}ozC02t>edq)nJ-XI+qaeeV2mW&Tz$C8+LM_pjMLiZ}LRy+H2E}WD4<5gG-lfl=I2b^Je-WMs!<H*Tr^Rj6)eT-t<x!OV}pSJ}|=J67NK~nXcJ&WrJ3q3mJMV`L^6iMwByyq3+@W+=1vWquHO#wbfllxsR!he%Ui%cO$mgu3(fgrlE~oS)2}#JP(@fF1lBsb6MDMYbutzragNBj?caKx+dy4;S0ZFqzJr$5U>>ed0vye&S8?TOxDE_q%$L%abSn8P?NDzc;Gs=AT>g=qcVdmI<Ss+q49W^60Os<Uun;qT<uv`5OQcWC5pc7n|=>z?e!HKFGu~lHbGP%aWrkEz~DY>vTd7aDFTo<Ihe|GnbrXg6#+W$+HuXbhEz>a?@)AO4HCHn$qPX6^V1C#RjTS&H4Ti{VU6<b6Q$G7KZsq#RiwR@5JQpZ$iko3Tdq&+g=Es{>s04t??*y_0FwllY$zqS@>jaBFUtdOgq^rZ69St~P;T>eSY3_8!Grkdc%Fq7^a&nyN<DPncc?4K46I`hER|*L-++ojDyh^J<OS9UjWC&_dtHEU?QPXhXIuSI9heC8N+g2(<t@_qTDO+{UhW&~g^MdH<k+Pi`ZJ75cf1S=K|iWIt-~a@k&7sSunHIdlIP3~WiQajq&#^M7s@16wu}K#975qj8kT2?G}P65)o^InPUT%mOt3e47UVQK<4^Q)#wJ~nZ+&G>i(y$v+f*vkZn*b4>2+fTA=0gVeUIQ!ujZnLkCU5<MN;eZy0MO!1RY8?R1VSz;E%n03eJUfECBR!b(wn1=@iB?1P>j^VjAd_!Tl&Sb3w{N5il=4TibUK5=UW8QqT)>btAYmX*bSt43*%LvedIj-clW+vd_;!fu+;?@p(Q+(6<fDT+F<7Q<s<iU^VBCj`$emGIsM7;=8G@Y@-JNJFWPiP_Ko+uV9A+%x}GL@8*Y9Ze6v#SEdNF&}-Vh`{8?Fz7o&MyMyOTMTcd8(jA8ckbGvINeHjVr-S{5M)PP~_Yu%ksd7hIbIC4#Au7ec>0$l$w?Ypn?GWDgY)RcI@J*x*mJ`KoL|n`s5QTdHDk@ktncJA~1w3wAIYhTKnSv6%jjLP+9kq(`qTxkX=3%OcfqMek7SW2-XOId-G7Z83&wSmUffb9}Blp|T=hQ*Ps$|!&)qEr_yVV}=$e?|qDt&XnmPiJMz$UD#l!r;N-#PZQ9@%cJo>+frRJARQ%EtI{^e<$3>zO?(+s>|Y>l7Fa8Nx^l&*K^y<ZVjXV>1Z%2Iw!n%mU&mcN)j&7k19Y>I>$TH9T335dPri$g+zfY|FW9W0mXA$ziwQR|-%)-U6;5sCoYS3m1pXV{@lH+5QqW27pz^3=^^`Sc4fVy=-$GY~S4d(cqE2JMSg}UV*ztBzNOtm-mGOf7KI?>YG-@hMB;Ea~Jv;ROwlOfeDCc!s)b0OX^TZsXBoLJ#9uX%5sLhK9S|zSv^Wj$>^J@u5&5Ps9H;gKC=)~ag_4dJPtpiE3nhILhMCtg@R5Xh;)yS-GsKO+k}XS?17YGl37vW=?g_B#>u=%O2eEN1ucrm!ZXLD4K>7>6c2EwyqDVs=~5lYI?4qi)}`%3*F<15V`tY|u|z{V3~G&=`Yx0q&Pcr+z7-N~Y!^3Q_ix|hx-Y1GX_dVX_N%%G=>Wn7M)(hkREXI@<>!1AVA!Iw5)SMO{VGXWgf(He?ql2op^Gulb+Dtnag;M^Zzfv1#mLs{z?K9y$w3U)<@0iYGU=Y-GkqVzmI2lmCS9po$!TVLU+6rAG)+;Sig~-Na!ej}l$g}i@O)!^M(6cgnCsrW_P&?1SQLL`y)YG#r4)~{4@sW1^I^EW4zZ2}s2)m@q*dYr%1nx(2cRoCQLZBC_`Y9ilAY$9;`7XuqAfUX*VqxXDlo^WWr5hqDoX44udY}Vw(IQZ!NUH*7!n0Ip8t+wE139m)%3#lE^umXFtt`Dc8i&J1V*}PMH_vi48EYQ*$<se0?!H6`ItP@i=xRCuXX)4l^ow?j~nc5Pr-?i3ZGVUCH8*YK+bh$wVH@Q$J^+;HRVQ3GPNJL3;t(>bHkJ?&UO0YhBQx(tq25eT!z#W9`icEIl*YL?uEe4Wo>%hMd@isRB*lR{b~mah^`TS8p{`hk+pTDDU1)us1{nhmh)K0QEn;h-I7(;K4IxFe{amWtse9$sq};!5YTw6GT}OhMM;x~j67yV8HEyZ-yBGp{S={HKxn>nqwq6>{8^?Uz_LI4kDRxW_wl32c)MbQT@=lDc=AjuShR<*`KX6*&NK-^kHW}P!%U%q7Kya#H`)6+!<2GuO$_pFW(T(Rt|<nMBG=!cfr0?Yg-ZKMy6AQp%$?e~#CtYEFPZ9|xS4x!)FLP;O5j19F3d7nLZv&vv97Iw306v;X;4kB$0@1mj(%S9C|K5|fR8i7`0TPr?V^>6RVu^-#s%?;6Q#v{LAIr=G@%OzwtKGouHq=$Yh3hb)`)aicfh3*Dxiw2n%^&DLak0p#zfrOq&yoKa#SGARsAC(LQ;$ooMC~Exy~e%8oR^Eltw9bTJ#Cd8a0+2)v(|iz?B|lgefVxRBPUY-Sbrkp@Xpv@RC_Z7R~szN5nav9gJ|Mn>1Xyvn_@wRU%O;&wmu`QcuC1AypIKo5luDZc;ded}Ll*%^8>iQk7+;zC{X?Ft1T|en@o(sdJ7}vmTH(Tyk|Fv;i7F@4EU}=)Dh@rJ9F|{d&F6Agyqr02a(?4+YoPVr@($(W0Em8#XR1VRIPxwOQ&~s<xG}8qf1)IT?~Ojj40pHo3mC|F|fzP2n$10(u?jSdqcwO24$ATR3;IchTe^U53u>>M>DdY}^2Jx84g`Y^W(jIIK&+(9D_K9R^4_!5DZ-x(vOL2!EeP+o*jvPL@5gC<7bW^)~_g^RKbCt<*{2l>-r7%+B1DQ#nRRrZUKh9a=rNqxr65(pg}l&i=vAoPr%1t9eVHAS@Ic_YV(`9bG4^ouc+lNZ%ZaEk=O|{3VHHaj3={+W8y_yLeMSCTB6k9g$OsdOuG=Ti%L@`p(pSDGQc=c%O5p%jj?kCAYpHYBsF0KAP?Pc3ndExGuAKBfl=t_J%^XH*>{=Pa9Qm4}Tj3G+_9%nwg>WgJ|)zmIaRF$U4$RZX<7lQC8t)Z~DrPHA5(jo7(-bypbZ4!9x3fXGjeX%BhOZm<Cn^rXn?w$1lV-=um$gI+x*T3e{la;?-~tTuWr=$CKTIu7W&N4UkAGH-~=GIRP|t8?O82XL=5hd-L^6u5yEQg#c=Vk`#i-JJ>Ml_kj-=Rqp@@?^U#@AlYfBA&UYO?Rl!h(C9WEXL#%77whr#q0Q?!99*8^IgahnCB++}B0#lpu6G#p+}7V5*;#0M%3a%`SH)#n^^32>zzVm*t-TL&kgKkFO#->l4^bTX)e0`p_8t|y=M2Oy3CP}m2qbE0-hw@%!>kG^MUDVgYfTV_i9R^*7lGZig76#&zeN{)G$U+j=xJ0m<cC7*8rsr*Na&@v7Pb9UB8BsujQudm;w+3^66_0y3soU{XL{>Ay1K4=+$W>-pqosRCd;oYZn1QR+|4TxtjCp<!x%mSyVfKoxj>q12UPPjeX;IWO&Ey~Gv&2tz1I)sd|%d*R?pAylu(?p25-R<QNB&K_WNGUvglbFc25(~Jfasc|B%&0rGsVZ8`fhek<op@3fV)^aoxHT{Ef;afN2+CQV3WKxREc%jA$-SuwmjDUw_}yrxeF(JBizWu?dUI8`qX@;N%qPnJC4fa=6YL(xHE46{Ck<IYS|)E(NlygzQHpYbH4h78IIv4s!9xcR95ZZan4%PCKnZzjh>FGIHOfIqbbe`EWox$gGoIkkbMZ1^yAHv4XnB3{#k=19K{>_xwyxP@(H~(~%E>zr)+bJYVDq;w^Pb4gBgd4J->ww(Q$JH?n(3^Ww?EA9%x;*&Q(2HsR^*@Lg<L0S_l$WWTh39d2b%7G>cm_zr`MN~NS>*5fl!BY9l-^8ZTo-F_kIJFg=SXg~9i04*eTA{RF$Uxa^LPN2<s5oKCGk#Q$;czqfJ+#Jby3JVib192*?QKxdb(+s=?!EG?>^cC8ZB5_5rMqBQ!wN&PHt^z(R_R2~gh`|JXjn%MkIZ&eX4513|-eV{?PmSVZH8)*?&tE?G*Vo-$ShOA4u8sA_!YnmxLn@!2u&IZ;?`%eGCfq#sbePrRuos?@V%xNivO>R)>X;qvY>S?mthG~In|OLI=BV{RL2R9Huiqq48=wYAjKq#fRP8pwc<7=*Bcz_kGGy)*T2L9)763z4vE<4rzOcH^VUhh4%tbn0OBzqn`Cj>}C*bB~%3L<|CFj`}d|C^RcBG=^VjJ$MM)~7qPG4Q3zJHL}A(t625b&+&asvXl!?K)Zwmj!6qM;4Kf$`ELX(X*5{06FK5OZTXHl1gAoFH9AFlo2-=+w5k5d5ah63Q`Q(9=4!NoDY2%Fc#7q{nDoE-<)R=Dd)YJ*;xDu}MlLV|$zKyS*f^p^!3%{~h=8q_7>)-eP>x!owY#OI_y*x!nr5I(4FHrrWNWSySg9Q64*^DF>wuY^bd+d`?aV>oVi}E}7C@Gw?36#;i}Itq=>eK=jf|t3=#H)9Us8NWw%W&e)#|{%8ZY#DB-F-sk3RUbab&>0%G&BGJAsyPvZg&1SJx!3X=5Aed9XnVldo7d{6z;8}MBV}5|tl}Gaf--p*WCnFJ9Kj;us?Xo_x73;R}YYK5}TQT0)4M!C;G6z$RCD@P0;aF>3-F33vKR~zvtgELP{OU$CNhZPA4x)}`R5~vefcA`15MJa=pgA4Iys#j3Y)3f>eN$qa+f~ulhsz~$>hB|;^z`{L#R@YCeov*ACPS>ncTp)Ici8+yNG`Rx4yLKpLAHE46t2NGBT=-F_3gVV{l%JU%F2|AKt4774$Hu^6QqZMP8bWgz*B9VJKjbJ62-=DlAEbOxyT^M6a{bMw{qOZJJ)Ho0k2D^hFA4!GN!*ozOEK=GnJsgKZ}BOd*>9Ly;!4@6laD_LW|4S@eK(IukJL-?XYtVyT(3zqL~dS?P=NXgIG$;eHr=e`-CRlQ+>`?naXAaFI$yErMJcb^xmz*7M>IZAtWXj83WYn68C1~rR3Ue3u98be#u8?$!RI3=+hhniHprT7vH>JzhA$-&Xji+9W$afAEjwC7MuWZMR1)6TcPuQVAs_Fs}4*v>V{|XGZED$-khb^JwwRd*o7a66K=ma{Gziq1gw9X{IZPUWDnHuW!~l+IbKYhk_2+Mj6m8QWic1qY_QkvS@G(6@l0U`gZTzb?&VQMy44;dwdhd7vxT9%8{NYx9`Dw57-)*vd%`CY%+v;K2Zq4g=TZw89D3Ygx|~&K)(Eahn{n9KiU4|Xf(KdH50CfY-Szb-Kfe3<^`}ptU(FBipNwTbl%idKeEr${{Nb)<&)b?0@o$>P)jAak0}y!>O}YbV-0kK(+~Tn3x7h0wy$aE-idIV4gmP`+E}UQSS*>-lYi7S-kC^j?h)6zAc6$2FLH_dR`>%hw>4R5WfB>K2H8uU5(NAC`X#dVJ(PvW#-jM$1wd8ox|NPt6TSj++c5-iqR#j$y``DL2Kg=SIYA<>_+#@Ty8AAW~FTelr<9C1i^2winH!p-8*!`5*U)%1v0<sp{B{f5@UILGkZa)#%K}+mKbIx2~qA65uz*x6Cf8Bmf($=nN@f~ocqB2p|PnPHj?;Zgh)vO=CK!)n!x2dh^<szapvfDJq=`W5+A!A~fkyB>{Qn55j&YW$=z6L&uykbox;0S~_g)9a<0mzUfay?_IqrYqIay$vN!Nh)?^KHhHLcr#7uYTgkMO6nY2RTK>-?EO-jud|gfIt2G!%v@nT(8Hwbx&=YsH3MTXl<h1$0?$|I!_PL42*t*RVRTga8sx+F!l1BJC(SJ(VXl>=lN1J^lhd=Mtt~ypdTZZ#=>RSfvCOo)xjHhI54G~n0ElzQ7t+QN~zcW(42C|rYPnYrCQ<U0Y!`8w$Hxz+j<pc`?Qu6`?dJx0*sHm68L6nb0_mWU|BM2#2XO#GD{ix!h~a3I0u{+;=Q?Z<O1_0;Y~s!ai^xJ_LZj3zQr#le;bw)0=dWqGu}^So5f~no}crKQ{BySR-5*@iK-?nUIm8~UXpUZ=UbrS-xTGA7R8`qq(=07W1i@>|11&Py3odG+{oYldcFR#3)(q&Q>2n?mcdfw0Hf-@<nJF&oR75l>4u0bdN7etpABigc4DPzG8gZtiQZl=`a^5cJ79pG8srJA>^{~;t#^|!yu0M%eI0p8iu?Soqf3ZrCSF=Ux>bXvwkXE4k;opfgQFoN2VZbS^`qKL6bjqie!#rI|4j0RI=0w0p+8N?kj28H%zm&19(vyv$yr3m^ExQ$2Io|2v|(RJ^jC@I9f0%V@|?|{ifS-`{;U0`*cHJ>wvJ;69x}SrK0QyZp$3m@TO?0U0boz=r`s0gQvlQ<;_-n8X5U#>3vMs|(wET^QEhvH?X6NxMdkJvqAJ}JUgB1U0-4)_Nh0^hNMUs*huz8Dnhp^rg{<_Xr>w2Njy6=bX6+&(IMXlEJGIa+-f>yywA2(#*lRfUH%aW-c1_JFtal0E?NTWke0Zmlrn&S_xWQUKsoGW#+m3dLoEJ^fCHl%cP-oj!=<%>KMDvC$A5b_X-BefQ0m9n*?Z__Aa8Ji=U~^g_8W_KaJe4jj)ZKS{r*1iiN@aXq`{{k7Cg*O7I$->7#~s78)cc+K{p;&**APzG9=*O*=fYJe_*bP5HR$9c2V?Qxm|>e&_xG3=xC_EatRFH>vbi8%P4NifhJnG38LAn+rvhb+Kn9u9Dc4cXDm9I(H&TsZ79;pYW$l1{{FRG2I<iORr-C`4U!Z>kDqKm~?DfyJ9{G6)&*snwK8_i>uQmA+{Q^6%T)2X*K(jsIgP<=%Q;YY1e80QJE^b2bXHoubeb~gd_kRcvKa&^Y9pjl7YlqJnfYjKEW@Ch6hg2A?d%&k<{cCfk*FCP6U~G#PWF%>62@|k1$lr;8j#GRgW;@%EuLtZ!V1qON&XXj!7xoy)Dg{@9LyPHfC1w@`D@rdJsQ|g+3=4{!%s|HD%Z`2LI-?;T_TnZ`wo7&#6X`TkDQ4euLBcR_>>|8_<b?{#p@qh2H!cFCJ)V;AI2VlTlQY{ktY|o8J@9+53eK%n3NgyKMGC|xA}K;lReLw-?;{tM0P>MhMyNd06`NMT5M|4vfDBGL6S_OYQuERNrqnUZsf9WkVtIEYBgrI85{K)3)bk~^A=b4Gv&XXhA8N<z!8Yoq%<cL1Ftm9*CoY!gtm?ZIv_6I+UQw7*EE;Vn`h-@JWFmbH^Hb_RC+>$(snAAkLt=n>`XKRwR%w}WQ>yTQ92vAzFJZAPvSM+R4Xn^^hnwk|U3cl#mcya968bf?@vtt0Th3spySM<6A-c<Gt|xPCb(c|YWo4sZ_6*qFh%L6egc^86QJcl-es3@^2;D1)Oc8`w3VTDi0K2CB$GHI45p@xp$3{=IXB&6}Av~!Fr<G%!<f{>M@nu9oO-!A}9_tWimCy<hGA0NTQAN|Dwd;5n8i;qPPR_d867u0H`}%clg4T+{Zu^+uV_C6#9~oPMeL%uxR+~UkJ$p|UbRNr#f#sI6^!`n5>**kNT{~37;Ydz9zh>19>bLFgqQ$lA#B0IOwVDz9+}@pTsHn?%j;<Z^9J*1yeZrS<{-DU9>msTm>!}6_ibU~>x3y90IX&Qd+NLze!A_uN#N@lcB}>RE2bI*W?`o<iA4EdOw}Vp8Kr~G+!zESL_qhyJ5~Q}a8VE)KQhq9J(-mX@AP`Lg7uj(V08)D`6w;iLTr^Xf4c{x^k|Yu<{_+-Sal5=+-(BiK4fzjh7lU<}{TYU$J6;AhpdVG<utC>*mPK%5zKiEa4Rdj}ACvMbmtC+Bm#ORB<GgcJX3Om*m<>EL?Etdx?AWMSl6`V)DWFe4R7xI~tYT!pO`?K<=a#I$yPK$i!~4J7u3_iapo1GDrFUZ;6NVSSQguE$eII`Smfz>g2d^$QjJZF;Scc#w0Esle*#c!cnkz*>01A1Yyb@e(;{r%s<gK)+)+Mjy>&97j;}dK~mJam@MXC!iMH+p_mlV`~hm3oQ-{A+b5@;$FtPg|jq9TIW<#51vxp%Oe+U%w-FL!KRcvPKiH;nn*QTNyF<yuGG=X_`ej8PE;zvlsq{0p{4z?;^~-bi~OK;L&q7lr(KMHp_gDe;!P2W7s<jxbH(dYwOk%~taRw!3U@60jpzXk-x^b^Pmby*X@)6Nt=z1THlX2@ahiRU&3@+W4DZ0>J(jK~Wlylb&|Y8{U4bD|CaRyAnDsC>Ezw0KqFN98h}`D5M3q$5O!327@<`c33sxI0H+QDMX3!<#hRUq*L!j{R{JAobnF{q@o;Tr39eYO-le<mq<N<cl;E6WJp8FHQe;C=0cb!I=c}0VRNGzvqt@RPb}@(8(y${Ko4vm2|{cv1YGT3clJB?b|M>i9U|NPrBNGTX#6)us-u4)(=x<t&M|<z&#hCCJ+$K^txb;$Ymf&miDQ~UxaXz6^fGmbr|W5Krr*suKeE3JVN8q;xQYR9-a5Mxh_u7umFq8Zi8?v#Hl$2p#K&6zTwxA&+?RYR#ow(eg^?ZJKGu#xg~<%XvuRq>MJ-Oz4g#WTn$3*vESm@hXZ>!iwZ!!>@5==KD&T^yLu^%~o+&N_5g%Z|6!;Dpn1EO(yh)pNt!nH_hHbmfuM-KoEkZ|1X|qW0LO({Zi`@#r2VFvnCV?o*wJI>S$UmtpNAS=`F?p;g*7SvP5o0;hO$8|my5hu;)YrM~qoFg&8sJfQ&zFr-r3#95lnV^vj=h$g_gPbM10J8XVu{C94C;LXT_ej9X664vB8_eQ;)~L)Y2tOz?Kw3%nwUNBTy#+=3<~@$<qC;8h)GT5=l1k55~a;<o3CdfXB|h>`a&s6((qu|2<aNhMKDCf5v0HSZj>#8vN`RQN6V=g4f=gxeTbd~7)_Y5rD7YW8QXm!Qxwt<MRg_Sn^pBeFNYl^0yQx=f2$>pv<MXq6Xlza+4pi9iGpCPtCgY=l%g&6A*Yh|FcP}ELmnFor@RO{$zpV5j)_UJ$hNYNCGQQ}(wg(WUuyD_=0xL@Z(T5ls1W5KHki+maw?!Sh=r>iK4NAJ2#>BwuQ0&-hF0bvi)mv7GP$Xu(y7MjXF*u8A3B+@oYN@tu~sG?q<iZ_twdbV3oZI?by-F~aL?z@aL<P+SElH+Mhn@7JXU68<wvJ+aC7#AJiAUX)nLNBO9Dxhb!u}LrKg@~K`^$LiybK7TSnyeShf|6tgR~{V8kt!D%NzobFR)9xjF)fm3WLuj0F<^iFAKIj&ggvJ?!Vv`{c`;@F$obGv*vO4-=GxS3*lt2^L4WnZ9T_=_D~jQW!f98PN&PN1h_o1qg#5)T!Ke5E(wJ4rk!}{v+pgfu}xx)fq8V><x$9ckkJrX}O2?fHxoYfX^Xl5ddr>&(krD0a|0xs^3%*H#ff*6p*|y`R;yp;8X8bVgMWR*B$B}2z*_@t*->!wmWO?)J_xLD-pt3RJp=Utb(H!VJA@{2?A4Lw!>>_3kEpW$<VWsg3jelg|G^^*;2I-{k-I1pR5M~-(m)8$&bbV$K97LM{*p?{tzB&$*kp(M}$c<BRMjOGCW;7|Nj@4GhNl_%JA^;$Zklo^F$B>pmU9k#lwA{`a~%3anNow1d=|1v@5M@B0~-dVhZ>=aQbdH5ZP-7stGz_KCVm2gvc!CWnU6}W3<B=V&AF2M4x(S*`o$r&cYsw9p>otz#S%j&Eo@o-P&VrA$=6kKLketm?4o+PsR5Yp6}a3F%3|A^uP>^B*%rk5(GQ(Uh6PFE1W_L+X=}T{-a>zg{E$5s?E9>YUvkCuhkGjsVLZbFft(zl?BpS5Bs(*tLSrI=Dx^o1ZgHD4YyHM&wIh@ki)T4=_i{Bfp0^i`0Ko4wSi=20C(6!))m$$LZ4=SU^%pgvX+cU&gMBicQZ=9xoCGbhf3ds+H(A<XDf4RJZF{R`9%?NTwa;a$%PCi32GYZxFVHKi4OM|=+aTZ;;g5%_g1)f@vA)Ma-l5G_0VF5V$5sY<k;3bKHmmy;fdL4^}3E*rc8%ZjT|xxvW_|>x80g)RK*5xCzgzZW{x>NO&K!VI!&FO>Kys3Hx#?gAB1<!nM#!l9kkcy0gri%Nyh~}OC??#Ez%5b1vIOK?8*KO;DM9tNln{xK-1=x`I>xqjnz?8#cMwYPUSCC4cXPW;1`7)(Cwa2caNhhM0Q)ZIn(ki^C>0B8#Q5SQC_#4v(nj7IPZ^(E{`Nx;}pvIP|kCL%Av1r_(6U>1@<~^TEl;uv1#EuNjY@F-v(ijHEHvbDK^5Dyf*n3KMPKf8kBJM_`An|cUgVgMzXBo$BwR3`lFU1c&k%~AZ!Ao=|D=d&z#l}k{oo`G=hRAmj~{jq`i$F({s=v!!vYP!%G#Ce#R|+;T$+oOfAckGA!=`FHldW5)Jx{pv$V4=4k;nT=&zP^^zm50W5p2V}P;j15Q1uJ=~6}j{0uLCC7gDy#Ca6o$_7Yua%=X#xW;byQA(XwI8TBE?oe&!k~|cf;^-Tt+lB1p{ygp@8xFAG_teWU~w}^Ux{1u{zIVT7O0E+mbq>!V@dS7VBX3Eh?Q^)v$wth+XkdbQ3M{19J`aqt|~m!wITO~XXZX6^i0^3bN*DKc%ar;H~z{mGXDWX2n74WGg>LK>blH*B3Jz7rl5@v8Nf=`S?8)@8FN`fCy=?o7}mOk?(Bn3fyrMJP1^tloH)-r)+;8qCiG*;IptkI#qnidAdjf=JOwWNvL<LP>;<uiX^|*Nz8&{H+GKj6bjmo5F7i-3;JSnW70N^^^J_F@?@2<?0~b^q-DB%E@HZ+`dZY}e4v$=2N7+PX2q$rY2P1p<s`}@5jW_}nek;JSt!rf<_n0lYqfAj7GGi%<Iyg?hs=UzZKO4a(pdTY(cYywkmre(NS1B^A4p46z%p0~t08mI68%JU57K)-!h!i0IFiWa;GEAUmj(>!)F_3)R8kVBK%$i;&KXV^6X1dB9*4AyhI|%w`t^;oWuT2TrFJhsZAZplZA_S69Hk^%&d?AHwTb{m<LSr)zQ5P4k`tWRfXWH&v$XUEV$%4}?)P_9y+?PK;?;qd(h?C7wG)iV8=3Kt+4jhBK--V_jA^`hdYgd~JrGDe-vXDmUKG+W47s_gJy~Stbz{vYVxYJRBKZY&eUtAHoo+_<;?0heFrGlWWZ9U-UMbtV+ISqXCfBdAekjpS8v(}Rz)(30^(924}rDw;n8aafcE1m7>PafO343paF$5jY4VI~F79wxsh3w}8#GpkxtT;!2QBQbaf9nc)?!Lj)b)nBg9G7#yAb*e5HBh&otzcI_Os)r00g^V1tx<UM1JO;PPB%huu`Zz|;t(B35giAV|OS&g=W1$#>bK0O_j^78*U2|jU$blJ$KGIm302n-~dQm^4U}a`DX7EFl{f|0cJ|0~k>ZFq!lAEEa5@$S=8l9dwv&Kx4#A1Gf_D3B9zebZN`s(LmG@HzSyal|Q&;9}-ojpCr;hfT<J_9ym&%9uSK7aT*yNU6b!`(>$b*K-_ZU>kPp9354rbpUws$3$w_S-@2BRoxFVE3>VY8SIPtj@pXew?{Wm!Nf-=4Y`<FZc>9d7*jf7;rSaBtO1PRpiQvntCK4eqo7nW)}|8olK)^S6~(eY||pAh(DAF=OYY&-DS*ym6mChM}EI}mc;=uM+JH9h@ozoBm6P<T>PXY@rt~jnWbTr*D23zxfR7NkW*I_^^_l*xr=0_2g056d?cLor`PgEBd~eatLM0gn`*~~-VQn1hIQi@wLq2zI2%~J1pFIM2v1x3{T%Bmvlv4rn;=FM8;fQA?q%Nkcr$=wrQ@Tz=+w=H-6MBa3z%6qcHpH)m%&=fGRl0)4v}?$`(xl58de|Us|mo0?gGkcYPn|9rL4M}`kJpYJrj^ybBQrGx)F%h+F^xP$f&Pw^I-84%{TAY^ZU1tnR3mRCDTg#Rh_iUR%H&+uxp>0N!t2C@<->o?%QI)h!2as?TMSqJV6@W13e%?*zmJ31cpzKP*XewUKwwQvtZI6V>v$<%q$Su%*^tE6E!{W$c<o>HqxF71*~&i^9);6EOq${i+pRCPXADvPXQ$HvjgBPOd)PI4Q63D*(D*2`xLJ)!7&UpMSOSh2?aB?LDQu?{o`}#38?lAPiDH69(}V$a7Ct!`@vQOK)4b#qs{r@F&Dhc`~G-G{`mIWPk($fKYRh%Z;!X^xA$Ma{ce8#V!PO5d?fR(-!w1!vF4kK^|b13_6z&N;TNKm%-tICvuKXhpMSo7|I1^bSaco6(~ia1xY98U^jhpQ_;XB{cl|Lzova<Dzzx6=5CAD}=>z;>9>ZAks+IPG!=C{kyk+_|{Er5OxcIa8zKSvUh=grxf5(o?(Kb4b3KTMrKaN&g*r1G6b8owGI9f>LpCSCucfaJP-+%e-rypkcZ}0DafA}d+%<x#9Q5N<i{)o*sDQ`|NT{v7P2)j)>peO`WA(|}x1Lx4y`&4GR>Ov%L&WXopRmmSXhSp0XXfxnUgquf<a7|m-$`u23jQ;vm{m;LC`Ss`j{c}Kn{L5z`YkvrR2dHe4c0b=9Em&)foM6yIc;9wAPREE51;Zx}`Ft+=s;VEIi}tW}F5m#p<FvPM=H^f9a|1_er0Dap>7%!0E1fFGPKHXrdWl6~gpQ%^DwzUNmHmi=6?@*BR(*{r-L^0{$3<$IRh7GSQk!v!V9wTS16xarm?3arT*8h4kX>b#*cBiLpWWL&-&P))4fXb!V4$48klF3vjgFh{S$+|$JuMx8#jg6@v5bAhR}Ec&rs*BmqgwOak}P@~W&Ql;HrE&59+y>?hu6vr9h<m4BSm!!6DAfVbO-f|{3sx&O(1{dHD))*+Qu^HbzFyBkBJ7Qp?w6wk9)!J8dXNY%2KX;P!jb%TIOzN9ea#-(Ea32YW1kmGmDa8Lo83i+8w7fhk^;y44FQhIA~s@qF@v{vS^c50`>Uf7%7g8yc6WCBN)<!V;TL<6N8_9v&ABdW5#-E%+BF+JEB-gWvF0#v&kd%E(uYPcRA1`H*Vx^+?wE*w#iT``$xT2YkwM9N(%9?tP<e*aR`+glx?HFnbuna9f^1yTx#=I?CLgktR?T)72(_At!~sC8LR6f!o9iF6e8T7O0dVJV|^%nK^UW{yWH+%mAeyd)eVn{QGWZkbLqLAHb9_KBu)dyxJ4{AWD%fBwa-Mx8&}%Ri7KkeHAyt3j13GZwI=s3Ab!R#+TK2SAD)<X)Ef*kRpEHXbX^+^$7Y4%4-Syzy@lrEuh02{ZFSorx{EkdX2>PqtxV-BU~(u-&@?KaSCxdt=|Z-~oeGATKgypS*sShU4dRgBt!p0hUnm^2IBhM~l>#X==JL4NQz03D7EAW94+m63t|M<-Y}k+!B6ee={YmOL^n;!sPPBx3U+KkqS=#8Ouf&w|j~PtE(Aj2WauJ_%;n-FhD(EGpISy;5h7CqK;SkQpxUp3olw(Mfda^shn+UqD$BF#hPYuCJN68WTq$I^D#=0aDnHo`8SvZd}zKBf4T(E_&wVXG*L_qDGe9x3oo1e}^os%x;>NbUuOfxNQWma_!PB7I1;Vtm6Q{<g{Qd3fGmQvtoBlhApFt)HQOd}pg7yK!{fT=;W19KWe_Y|W;dHI?J6(ibd9G~ho=Fe!?TIN(A-O4K~7tt1<%Tp!bnXjLGOd`yAX)QRqa#1RbwkYdk*d;1CG_gd8Z?Jg>8-Sx@on82H&LBr@hI)(1x1@h_4>k|dW;c&uFYgk;v|iUmH;rqO%dj|R31uz_usjcY=RxwM==g&7%;I_p2p$;p!}&=#1!D*vCt;^WwA)eIn8Kdci6O;H?s1Dss${5AishlBgf8qf#<V`X7EN<kAZ9jByINtKrb+c*(Ho4IRe;H|(vOYH{@ilUD)@qlf=dFFjs(jzl|B>(TGJS3!H|sU&|s?1;?7lvE%rUZ!bahh&!ra~PqB%bFW#ER{b*-T%y=Ec*q%Lpp@tR4-^oJ0d=>X6;jOU@jH>Bt*LEJ{vNBpu@L?>k5*BmaMVxhB5XAY(suT&B^fb#zIGyudTRQi4%$*Q9O2**eQ8O#m35#PWMnd7vq;<gHYQA@#8nz%8Dj<!U7;+9_YmII>!xlwPT&E^A3fbpS7$?Sfa|S4$q}9Tm`)K9XZlufuW>PU+-e%{RAoBGO9wXh=k@g1M!kun3y<b+i?}(?%m~K8&zToczI9x%@Ou@9<IhRT1P?Q)7V=jB1Hqhaz=D9wPYneNwCB?9ibh8W2WD&UX#If<OXcT1kL-2*}i>os-NxrP-zsp4FzBKAomW--y<c7!OY7`uRi0t`Fud;U>`A!^?Lt}VFPHHL}2JhT>QkH1Ye0Yp9hv}(eD9?RJ(dvg7Yc@dU8iw(pT|To}d~UZH)IpvB`b4fOWx@M!w1M&s5qCH_cDzop8tz~fgb~o-L8X(=7DRvcb>O=mEWt6MP(A^`!9L!lJqEvteu1@EX^GOyzB>EI+vcX42U&Wa378`5m_u0hsKctwS4d_F7kX=vOOmAjKCJ6_<<*3_iZ6C-fots(Hu+GnRy@zH3hEpKT?lmb`$6}biXyU&H&F!L-bIPLGK96>cVZ2EK1K<^=4pQ~;R{+AFuGvmHf^y+vERXB6EX^y2|z3bnJCX~yw2&&Db%R$NOPvvBP8%r`^3>X3FN!e64B;k#d47BG#A4D69VITrIID;R$#X?pmvpo#XmRYO2-d|JH>ghHiIwSSN3l<@nogUyc%Ca!Xb61aG2!n>iy;0Hy23ky=Ls+!N^Nq9z1ewM~}0`7day=Qgcs+YpK2ZdR2vvydqy0vc_pNY}2xIw(TfjSlXkZ6s-E_pWJHJvZ`-{wVtT>7GS~!s57`$n~I-7)Q)%{toRgrkBM?&LqkGanR>La73T=~?>q}9pSE)zx5=)9u3JU{ri>IWL8jEfDR%B#LvoVrgo}9KG(-ZcCLN=kWC%5_6@rVy`#<<pGwU28YrC(-yUH0E8Y_)q;+Rm8GqssEbk-rnTSKxIYptrBIC&d*<&;*6WFvG8caizxC>}?C!=ze!X1&)wRF29;2T}vP!i`S5XMZ;JtOUii4s}RclJCd&G<+)HJlSK<PBsgs5>LBpZ?=dx%pQLN-eT%Rw2la11jqPB^@#N9%!(sav`{^P^(p3Kv40**J%k55?#FzWRidVCmPr<Y0U$7^03_pj)q*nHv=#Np0P_uU0?4V+v2YnZ?lYP{CsJiwV)G*)xfXc|FeMhU$WIM5jLo=2+;oPp26Qb^KS1xg37KTVA?8|yLb(huM9PWzJy#$%25n!3TG}EgaHL}+rg}6$3{GCGK)UEQ`aSB;ymmq?=1L%$492MsZ8}$DKR@~yanzQHiC`|-f;j<u@axvG(&V&HeNDr*;w|GnZNUF9=XN)h^$yj@YzBy8v#(>AWnkVhoYL1&9J&pf<Z?W|8XQmB*g>-g{=mR6mM=bdV$AFhaP85c0qcW(L;PKTG+SpsM-*)loI49=lp*hOpApinC22E~aWKP}haulRq34q*_q^W>Fb`v20|gBY>^9w98ZbJkLEt9t^Z$-PPn`)ov5Q9vr2UPa)3hNdoP4KBlV&Dh93_9?LgWAQFMmzcWRsk@^H85Yjlj{52dE^T=7tWY!}OuRmnOt%4T!DdDmRRwk=Vdi3D23ccTITB!}iqC^y5~MaP}C*-gnwSH8P3-iI9`*BhTaT>;X)K!P=uXj<Os?4+Dn6_A-xCXY7kEP{q)P{k5_1JkCi*j2hJTMMjJW2GNvQ-QkzCY7a`(`Cqt!u_{zDkG02b25y1o9fqx{bHm-D_k=PFNGsY=B<v4$l|>BUL-rgbAWkvQ4G#;WL!^~{URU$6ieN;0KKKU@E~aX<E<%W4nH%yIeE#)%cB?jrqO-@rhlkmLI?mJBh3AkzS8@x5BREaECM_$~vC^X3PY;GO=jn@aJOTPC^mcw_;W~TcIj|Mgncvl3a3PqQ`nW5#;%kC{LupMv$#ssAM>H#x$HWcO!y`+Yy^n#dD%!e-PJ-nO*(x4mOR}!$=@~l+owGn#(+GdhAy&_&FcXLK=<Jy1K|P$L&O><K--x82UA=i!Pb9i3QU;TOf9SGZ%GL8cz2baAiYjvHfCC!lujhG|rE$dm-_TU`JWhs-<g}l2k;e~<IDprW@M^?O{By(Ka->#+4*1^6b6(%-48UfGtI}fvjq1|-7uBWbdF_eCQR9gstTDwwiOaNcjCWJnKREF_?2Z256{4_JX`VX?zd#KZL}JLN1_nU5MMcK2!D2T6c)q*Zcn@<@c>+*Yw~U>1e)tRqAyZE>Q7So=mX`AP`|+!gAgW=hCorUtu|=p_KGf=~b7&b!jXf(gp?-0r8eSKceITV`T24VE=maBijH@bJ-3d1CKDS{?5=<mSd{fXTujQd)OsFg~m$fgBCI|-N!SXS>@krTTdN3trK{}rO3l3!1C>{ZAJQg5ff$Pw5Few0+^1+kH#*L*L9u(5=N24m3Bc<`a=c3d}K9o8EHOY|jVyjR#9f!lt*ZGO#o1r%7$pZ+vzgjw&(P$qAbj}!oCtc@rnX8OoM+?EcRpm|zb=SJ61vsKn6C{EOZUGEvm0O|`i6=P~?9q7#aqG?5I+H35A%_kt;*X;y-q`>H1gEd=a_wEr2xO=-<EUjcSnBhBH9Q;bix3j1j9--sXn8hJ&Y~vj^Z|AqqNfD{%ZVQkcXmBgn{W;0z|Up0coJxHUS_$%OZj8O?STVUhN%Z$Fd4&`lRO}J2~3Vg(Qr94XU=YUCSKF)7@>oLkIi)%CVlePg4mLX<sQ@ZpKFnmbdV+@HmzNEOD56)2MD+;JgFXB7QG<3Y|<g~>tyWGpz($j>fm1Qoe7~2x%(0mhqNt3C*Icgp6uY)K_+<rOaY`$w*;q%R!G#6KGBZ}b_|BF(UdQ#M+{bcN*!s&D9bby6p3rOKC|}bJRcYJ@zg};JRsMN%co%7i(KxG*^}j9L)3dADezT#XOZA7Wj^EN);hc(A=$8=r)haA{v)&=Top1=J3ph3b?prED4av<MfgxvROfZe9+BtcYIs8*zxmn5BiO{fBiEzBg;`M|?3TTaE~K!4=|<pFs45-)MUIFd=50)uDuH40d6K=tgH-yz^uW&B)YmGnqnF`xf;Iu&*0|T=K9O0K9AQb5s4b*hk_5i&_pz6!(kov@05ET|@KBZ~Imoj(ISiT-bSJT>lR%#;!$higKY1-*;!(m$f#ESLaQyA_$!r)fK$?RolqBjAL=z&e;%{4qu$z<_VP4MCrX(oZ=56m-L0uKK_r;f1*NNkIp~HZiW4C5Qps^XEs(Ft}kHO<E^=v$R@fZ$;n1Y7#!qbOv-TsInhqWsy6?HJ;SdzR)^fb{!l+L!nbNt9pyq%{xBaP&xOCnT9lz92jcwT@;+T74-(7i$8@P<YHVU3F8qER#+Nk?4&_A!2e0-5Da^n4sB5jyB`a0Av3^(p<(zD6^c*zWsj7oJKEtGCHE&zgHVbTM~-k%pZ2J=WiLAu7bKGeb*{xgTSeA&N1bJd}E*6Q{)!h7y|f%OI-_=5xSYu}nvycm=xBP=&BP;5-cqXGEAn0pr7cdyf{fQE)+nW4zEz9ZKj_2@Uuu4^@WJvDBhRLfZUda7r0M9dw*0enIvuY)sV&T}nehg6j7YQxdtav@wC8mJfVKq3k{7JSc1CsTZY(MXXEv*HrL*8McJb#=oz7r3`yd_X@+*+kTd&W#<WEiOb3^4;hDB+NHSD47pEo_?dumF$Qzn+c}PEMp;lgPYBt9s%H#zT+e0gfx_B%B#;;)ewQi*eLgbd+)ZmhyB#TmP-laJI=9orj7858>6ss%?oX7u1fcT$SPA4SHpAxy5RYF6Ap~`Sz@1%GnHOG*Wjx<B{0MU{Wn4R(zQ73~l4-ATdlY)w(+e24M8XBC*S0B(2iVN@m~^n<r^<8&pY_I&EG6cOfrd4_wDj;P;jBG<5{nG0d?Q1`z#qUMJMZl@_Vqsn6g!XWgiXzpnn^LyTbZVmgY4o}!>~2QM?#|5hJA+T*~McDl6?ULF)E~&n0hA42om^{&5U&*n#xprsZCie{6o>I^pz~YFjLC*Vn3-YP8t_H!mD=rlhZ0o8l&9I62U!Klo2!lhMAY;oWmv~BWVjD4f%nsR+Mj!5$<u8Ymgx=Y8zTyv5k{kN9SFcht7Lx2|q0tC}OITi+h$9({Z@w4z5ly({jg!MT^i7jM$ShPcIX)__CDC{2X~_qA3XF?A)Y`-2SndyvuGnLN;L;B7p(+>O9&G)0#l0-;<e{Bc%b3J#d?eCY98mMTj&_b7ltS<;&@w>;RLi@A?Y!nyWP?`jly9E}+37iQr@0o1Tt|T9*KjL@I&BEofzq<P9QOogM*;tLqze`H{$>40*~mSS%&oh#Z(3JG*6k?d_9=*13CwS6w9-y7~rXl1a|OdVhe>^}=dF0bcDDDrHXG2^v4kO(7H;ki@N(Qu5T8*DR?oj>^lFVqKNyu}gg|c_!t(W(1|tT@h-oWzp$~Q*A{Y{^mgm$>YWxiF)qLs?u$8@DGLVCT@cFC~SSg44fjEYD$24@RWb37gEap+Gm4lJ5fz<o|kovP?bxrI@%#<uyo%BnSZb}Y(q@?Bybh^{_~s`h>=|r)6fwSF%+8f)t)31ceO|($VIB>q)toIFcozu`S=4wv^pl0A{r(UrFt)z*V0*zL)}3}$HqT4m{F!>l8up{rPe1DTV$croW{#7D+F%F^535fsxo_QLn5PRgcw*yY$hU^@SEgK!_(u=cFV^Jykm*|f}xzTrIi$j_<jfW{48ubi2V?23r;H8lx4_|)~3GcXgkX+NdnuljB(-H;h_l9;cDl5DzhT+B|V4N_kk^pLe3wrfQ<s~ArBmxTOl#YfpM0Qw+5dApyWXH9-btX^Bnu7>gNKXe{>SLWJMngbx9lvtf#^<1L2{~_cPtC-l}7^Wqc3Ii)fhiu++J13iRy~-IEB9aj!px)Y6qX-@Lw%WtV%QQ1ev+wH7zqDVNs)+pI(4ihNGwUddFOMTD~#?uM18KNGm?n6jyf(3i5F=yE@$;Yeb~1!iYOm{~*{p)LA_7__Wm-zx<xWq@c-l_LWDMWD;^jLRFwB#0G(s3u2-SfSi~qlCHOq$FBdnYfe6x}HG{uZxTqvSAw|D6<x<3ohJ{8=)l1hNFF{L6%Zqg|t#WQU!Emmxck!>fC%L62L5{Bsl&B>@DHUPT!`XMk3@gR*;8Idci+>c`2PVjDR+K^U4YvSMmCf<z}`~&L2e~Bu~u1jK%U)r_^D$JuLZxF+5~pzOVb=|MBhTfBoeTgC07TYm#MODb+=wz6Ov7u{crfp|!nFY?db`>?C+DoaJCJ8!AzR8NbU`<avDf{!{Q&>%HXdM%veCtBE?ivxs4!ppk%S`VB&O>X4e3h8W70aWrDUxc>m=Yee=SmK{Ce#0}X~RJu_~%p<Bo5X6(*rI(vgIG`R<xj3=}*=4Tbkt%n(mnF(dhh&fFh9^p@exzpy+mJtLd{)sN<gyx67n$z`7=M_GCZ>sF1$2Ovd;7t7r@)e`NFV3$E4n0l=ZSa38v-eg#AW$CMnRsHsb#0Uq)efg7?r4;nSTUcbM2JZOkWmzH7Ua&U}#X}caAYGGKaI&(&`y?nTbOn6xr8)>k-RQ3m7Vwj}DA=lX-ac8j9D!<1%hDcyNpF)4Ou^T~;&+N-6K6Rb=^G-XdytrVgQY8}~YTfZO);flK9``#Ovr^5UXws%?u(6v~{#Ut9VofObJAxkT@eGc=zcTSdvJH=sCqfg>8JgUnwXnHnW|^p-{qfvqZ?U>~#!^O^DZs!Y={=IDLp*cVRh;=^FNlS+?5#C&3l>~2c!LX3pW^)|p6SyiZHHq#&AYvYl1LY9$U4DWc+*@0sf?AowLW$1KL)D&4YXJP2$knzEIa!6@s@{u@NGv9$At>dU(ElxwtQS8jQ^xLuOC}WYC)IiASlQ_B&;G&M5NaM_%@?r{28%8`PH}06}JSM$BW0C)XLKHr_)KiCZ=uy@;W&r2pP{3BYs_(ImS{<XzEr!o~*-8!rNm)~+NBBOAT-uiQ@<`XfsV(CLICabdE5r)IRbq_d;WE7(nif?`B<aUFo6qs@a`Z&|bXnIP!U`yuuM6O%PD9k%A2jliw%k0fg}7Y}36#CMHt(r?z9QT6L6r+!x255BimoYMXx`|?v7!$Uw)0NLdP#Mf^*%@#QZI=Y2~aQ43ICW#95XNH=`M+?WS04yUd408L#JknC@c6LlaH3upgL()otEy3p<bZX8hv>Q$-kAWoJb6FBT-3$Csh1J-u~;Gq3WbJ*1*0tt^4UEn3@bgW{m#%Hv4&y{oaSHAj%MFIQ0+TTb4U>1~-q0zrTx1G0OIfG*5}WVK{k1?TNi!bM9TH;ZurMu>*MHc|-G@W7+|6R3OsIJ=CzXzs^PP>PQHv;FYB{6CuMi*Qfjh5D=oT=&|=6gLzT?UPeExG~uU}&cR^&0Y%`1%6Kr&o}&p}+`^)ITD3&?>$8VfYdm$&M}`y%oJG~gr7oviMhr=x!09Drb2S=zn!x%&qyQ$8l0;EKfm~;KW@T#D$f>1YCV>1tQ!)*26zz-&?&G_n_pEVOvkkk*N!320D3FtJlVJ>iWPKI?$`l!0$^*i8p>C(*3BWMx^EW^*aOrp%`%;6kFL{X(6ICbLq+)y<7~`sPZn7c;#^^9BLb{U}m&!5dO-Du(oz19&9-Q{}Wdmc|I}v`&fm3%mX7q0uc7;^A(*sd!NMH=pcC*84)WvERV_{S(iCT3sWALdV7F~w7*b`N!7vfmz7vWfrp>`1&Gv;<BbFU9C=85o$v21S^BxBD0JmHH1EmgHvRdGOCRn;4jRB++7TKYsadfU7hL#`W_*R><h_Hii|glgZq8}1Kt>j5j#h8VdaD`F=0D<<$%>|ephsB_w$Tb5TIsLSvIy)e>$fJ{)brOET9m$9SU&(wPYDv?B<BB`idmq{fXg$#;$%_d!J-e2=sCEks|WmGm~3lTVRR&6P-pcj=SKp8Gb;A8@0uen4ur$Yp9s1p|ird-MXoJHg%dMQ~#@_sqvj1-F+U_D8JrCf-7YD2Yj8yvr<>Iiuh;2TeHWVV*r;_{)KF<$E95VQGVM^kNxkw9#cFlAE1MpQcwaWoAH5`!iM%M_nz>YWKEp`kkRk86}Lh)j6&?_N%!VLDQdD*h<oRm0UM*%_vIbc}ZHJgp2_%&4IPt~CL-IoO2mX_gy)Bir|)x3;K+2_j7lSox~<=)8iGx0?j!1e)HLIG{lKkD*Um?jwiF18Td`pkE@{o!p)s;g5->m>XOJPkw8>?av}EnlNcCX5200*FH3U#}i_@hL0q0@IX%C;R{S3qJ;T!$7$VkGT!i!XFQX6`V%(~v5m^f2xuVs6tDvcraV*04ZwBgCAP4;QvrVXqzKQVUA8&F=m8D^V*w6mKiJ?fflb|ta!%y9oVWc_L1(h=V3DhS2v|grJK`R}Lk{}oc?MfliUdH7K;S2kV!6uj?QzZ2J49>F*pR|B)Cvs!T)mdMZTi6pZFx)z#(E=i<TbTn3JTPB#gBnaI$?#<BM70M<XIirhdzrFboput367v=j=_aLxb9=(82OoTaFM+O1kRdD?fjtc0JB<qNYX1~L|6wZ%c|tm-yS;JF~Vn`Q+{z@r}c-NYh(tQg}i4{y<sGxr%lv&4qE0;qYz^$_L?zE@W3D6GO!wUrCD;1bTl=*Lzo)GE8jrpMpIyNfirAnBaxZ#-05syTB@BMA20!(ga{Fn2qKCp?g1BOw@1vp3?uR+=?h)KW#EBlT+6jaza>fea~S{l_Qz430^c8>$<8bdcaS~94>ua6NCageCoiLsdZy<y>8%Wmrjx)uQW%yTb?LD-(>a-0pA2iyArc^zUh_jNyDdY}IkWU<o6u6lQn0imN!2@92B9RX<|8_@HIx|5i@%qKD(HM@4x<reW1_fJMLflFPD?``#NHqqqS=63);o<$T1&$oL=_K$*v-1ujA)6K&cQHuS^U6eTJ8s;Pp#veAJ>05KSaKE<DjoRX8?NFE1+OWyfn6VVj32q5JADYdHgiW!w}<c0x--do&=whKH%sACZN^+8qd9aBlOGz<hV#(POj!y)WAJR2~toN>qV2U;8i$c8HGoW;YdYg@SxAtKLAU@ET4bb#>-t;`KRD`SIV)ap$3YL1&<*gPBn&w1SD8QWr|mQys+e$<rev{bOM(QRGSO`(7KELMiw%$-2`UEndyAabPq*-*60nB`~-#t40i7}(rM6XWBd-%$k=~`s)b-=<I^rz2--0@&Bxa?;V<Y^S<_KoU#74z(=V@t_Z$3R$UmfbYRAy$UT|o@u>!vtkjA^m=PTK2&-=c+cHk9wnPsY~&k(Y1h%(e-)&j7K_a<$QnaZu5j0}!e;q7(ud2J>=KABc^<Qlq;3C@6#i|tPL(QaycYQj_3N!sXC9E$Lz;VhD<YND(~j@ve)K6D#%!!*=GR)ca$G{6lQ$CSeLGLO1)GH1M3A^!{(p)dEO9_yTjRd}*PB3(C=0M>q%Sx)KIV$4loI6@);jJ0&0Z$^8=3U74oB<yY|f>>cr6-40pdXgysqg%RIVDy}f9w-KYlsL_tBoU&=jw{`;)1hfMA0tjAbs5w)3NvW;89TcXM-Y#28G1E9%=>|n9c9QB)Y<eU<C!!bVKDHqljxNNiyvysp`U(a{VOo#(tx+l2(zL7Vf9>e-++JJJZuj+m~j%_ZdFS4oXk0wS>`*Ih}GB@vc5pq`X%UpqIV|pIi76KT9On%+VRyjyF?mxrPcE>G4~jfmh;psVZ!mAWuOH78aqF_JA(aOpCL*?&_yww(mo4dXwd`I#Lccmg#9t_EmWGMEj$KmMvTjfI?^0w)klt=_rL!2_*kD)b>dP_%TiUaIQ4c!$;~!POzzL-+@I+_@<s0fqTV}gGjSc27~H$8V`p<D&sT@-sQy(HD1C>)R1}(T-b*LnzkSS<(-tjJLi2Hh=P&B;Th>{o=}xdk%R=o^ooX5|&@RH{oqK{{TK<9*c|p#)q`}sHNR7vW;r$NM%80bz7UxW|wB4H)dMR{>$PH-;Hz?ViHi11o&B>N1It5vvXr{pEBg#4{ZP)bKg%z2A;2(HCAQ})e9oD9uuggC7a7{yA`Xd<m@mimz6qsl*LoWQ?T4@lW5W{WUh-2PGPqM<0>-NdTVg3VOTz=768<OG1Q@u0|@5X7`_Y)GjhYf(xQ@v|-TF=&gasOfXr(_FpDQvCA6t3+gn<W8(EP44Km-SewRc>BZR2P!0f2~cN+u3eeU53f5&CGq}RYBQi$U*|Td}z5J?21piU_IzZUjQGc+Z4w^t?IJkC7aCsGTgsNbQ>2wCC^v*aX`vB#fAaqHjJp9D<TDBjIJ;{PdHg`bFF-?=S`^AUAHsm=Q_k$_F%thDn<6a1e}`l$X%`eAK!la>5p&bhad02zCGUm-`;=y_B(zml^E$Tw*I5^X;{}W<7!ZkTISbHfC~F}p!v421?|fI8~31eGC6C^^B<(jpDQuw@x=d~y{U4oz&<W+j-+*5+m&IJYL?P-Rv2%`fA_lQgxT&(ZXICj>)9U;xq;1B|JRp)4g3@maXexwew^;>XzVYrD?~gMJjwqS%adB|t)EWKE*bfm9DABue8h>OHy?@g=igtx|LL&=5&o+iUY+dYShl`~{|sQxWTVD9#63k1wd2L(84nQxIwN7Raq8nHfB%=Ce*fjSpMGrhw~w&ob8mI{^{3x|K3BVrD&uU<A7MWIJ;VEb)M9owR0kYu*cEp9SR9)niKDCW>>2KrJ!Gt*WB)(@`sLT3|M$;N{^MVc=m@kS_Seo++g$r-4)ZzEqFTRCJ7z!eT5<An$(nt!%#Zi|4~Z{NkM7uhS}VVQ%dTnj9bikMq64EIB+!M2$1lkIUg)#Ny2EDb%b%l%PmIRdwRibDFE2XY;q%@!-0yZ>sb&EMM8GrXjB@7Za7mEqL}~?u>6!(1`#F>)z7ptU5orQQM`C^){at%cmbGW4f_|JBLpd&7^mt0O**xXzEW6r>(GGGIKqq2b=VyWOk{!SL7U$_+r!<M6t_4T6ZtXs<5x~xQi%0`Y^c&1;10er#Epi{o^Z6bx{Rie`4IS|r{S@)IR=N1Y2Lv6P_MOz1U9U+!!YeQC!KX*l`i*&y@EFyuCv+ju&}K>6p*dV%W6LnCF}%@avTf4$tbO*qKi6vu8++)Py4f`Fa!~}JiikRo+NPt2IMEn7k{|=nxs*kwAk(lFA4K%Y9pW*TDr0hti_thL6!@w+A={!h_&1+Tbv4LVM@;tjWm@Ge%R_wKJjj;lF9BDJv3EtXTI06o4+i@dhi3XK-!RA$sSV9hmY^MMQ!;F@>Q^pnHTd}HNtVFZ0yf8e&cE&o(r|LW8Br3AdnDWhPz^-z`J|`Q`Q}&}esVKXi*fe<`M3A?zYD3vW7<(I!t#J1@c+5ww+|;SVhbIY6Ir_+^2Mp!C>>%Gou3oq-Pv%HjyX&XStoUeY|<4Rz!c54mg2mRbyQ{gq}1!3jOM<Myy1*{Ak$EL1m;5@gwlUVA??)A3EFt^G0zG|L%{w%6hZZNry)vM*ivKAfq?&+)E4!W@H7rRZAy4y5ok5o0`EPa#t^Zc<N@~o5q$U*95Kd~3|0YAlZ3iY=Xq){PM~Nbt7{Vz!A5qBqpC%9v7<@b5tc5P8l1&bY0BxfF4#1#`7S%PSI)k({x8hH@VCB<RzIAk0rH=Pdc;EigiSb#GEOgei6=Q>%iI=6LfN3*U*<qedh_(9ag`<(^;)&)Uf$16qUR6>#x&{d^N2jP&~M&#Ip(zM9UsgL$Nna%)l3<3A4W(BiV$sk5cu#}%?)vNhH!&H$GM8<gu9L1p*c~Rq@`4q{nk%NPxGSYShVC4t?p8+&D9~9*G%6JRZfFg)7E%~d%Bzh+oB9ZOJy8#pczLN<-<LXY2NcnCz_T;#+fZ+nuAXQUw>$lcet<UZc+dG?b|=!!(__&<b~WPX#zMU=~Z>4oReYkUYL5$YyNl4i-?H2aac(;Zl$GTQe3ai_`zV83@#E|DU32nblEmf78vEG;t4s|6#7@9S`H>=$5ye2e*lLUJWTsj!5q*p&_7~h8WnMH{JF_%<f`G_tfS!Jn4$aPM{m(DunWtf{%i%t^ZBj<%`Ywg-v9AtyTelahZ_3X9RImKY+?(beK=;i$g&wh2e}X5LNB+S5C?M7<F^bdQWE&~z+vFivi`QY<;SiwPm#m_re#!%m=@*&yWstu2tZWL7h?5u3Q?Beya<x=%;N+35zOH^HQ>rXCf*o{H$s)2O@TEGNeuYGq$T7)?}7CtmA3mt{5$UHD7FoNg34)jmnBhNQ?$vL9GH+=l&WfPVV$S}irQ2;ML>|m+UMgEYb;)Y^H0v~+^{uLoWBRJ;NDtlLWA*eu`+EjimJ1{J+XJI{yt{up~DJMd(AsGtw~F?JVpV8pD1RzJHtx#(f-Cpj7%+5@f2y#bebmc_w>tk8}&A%HpDu+VKq5SvH{<~_kE%Uhh|f@C>N1ZFQITP<X&?PN8fj8z?dwnm{a&B7YY&-dH*I)q)U;RYnIVWhWQ1dzhv6BCtF5ubVXl4>NhnQKAhT7nn;0w5z*MP9_t>;8`=j(xLl%5gq!IeyLsqkrnFrj$Rjc-YG#0s5$S}`b{*}g2w;;!z>mSq(elW9sR<6o50tZyB{JW^@DTNG@Vrv3HhJK+@7)2o6fQ%cB|BnlB~1p*!y>E0+O!6F-z7s2&hHw9tiai|C&3OC<Y>L5`#k9WUUWD?IIZAxgr{vDA}o4XQ<HB{$k##6-{G&#<MixHyu9`Sp2tWT#;3%Nh(_I}$T<;Ma-8}xhgE*N!862=t<e#8@?Ud9M?wJCAY;qu_rhl?o2EL(yVJzboT8J{S+S`Ol^6=0HhfCJu94GYoy&V}#ai3=@bdKYJSFflB%#B)X=vWr9@%M1=mmk4@RQ`r3{rOtuy$mMxO$JeX33+dONLSUZ63)mOqTar&b6agP5r7{YkQs-+4@Adj^`i5IfBem4KxIlB~-ca=eaz|<4d?cB_1(1SfyBOl^}5hWgCTy?0`|tq4Lvb;u}ii5$zT0zA4uH7}ng=8vcpDbv(=F6cmp}`&mxOgC_ZyOO++SAk#6^V+6e{sp{t3plFz2A;}d)c3r3=SZh^sVszjHQvQr6`<kyvKCol^3*I11G?A&t-F?))OprlRzrZejEzdxG-SM*I4*F5$v8}5t4;f)qp-LM5B|&H47+x#a`#DRGxxr1lW15aIfz#Ymu-p5q8mbdeXuTKEf0LoXZBaDV>Sr_Zh9&%ke$X<ixk>x<+m>M;vaF=<c2N`Hx(0X?I?%f=CCSaGB7yYVzc6v?hsUy6B(+<5UiwgUymg-Sf$-`32_k#58-S41c>M0dN||FSjHL!oA1Jw-bTF$;WtctYhHWj+^x3O^3Q^9meU1kxr(?mJe&=PA<E$=uAs_V8A`Mlav{gyFkU-2m<SSR#!YRs=ndd7WXCiu?^J*}xc<3-zFHybyVFiS!a4ntkq9DyjDM#`IK``CFhS)<AO@-H+R`Nu;h^tT7fU$x`3%yJB!w()ozmJzDTBFR2-avX*xUUybf;D=t$ToDS!Gq1Z4hhsN*mX)KDjWC;*l&1fK7~uaA_3R(j!}?mQpGjQz432)6%G4aqFn4n=Pav$b>GE3WfkE&k3w?_sS%ur#yzuFMgjk501W%sgTb2zJM2et%;Y|1TD;=WGfhhnsaeTMfIZ^%0QUwAJaEb&ASzm-{@U8UcBHa86*s9$`nxPoU%dXIxnabLE;q~+v8|&N+=eaws)Wv`cEz*5F}|X?LEixhGe57y^qRaZ9{ZhEL4xet;g^<SRAu)xTq?ss(Z7(<Vl;c%xUfLf{Fv>mWDe1hStzSS+yaNZT&X5+2H{$dG87pL#(@l+c2l<gIhU?9$UJ)#v4v2R&Q?Ggd9cCjv!7#?$tB432U>)g9Q4&LAbmHSn=UOrPH~)3HuH6!bBS5s5UBvmqS?Z>Nw+H6>2W&Sh+ZxxgInBrk5Q@`ID<q-Jnm(?Egbl(0LOg{aZ<DCj6KD%g?`qq^-93NgdB3hgSDk#>aIrxP@&0TJr6-h5Di^VMhz@kM?WqBi@o+KwbDAZJ;~7D76LXN16?)U@FRM7tz{A-J9<`VQjYZ!Fd~>^Y-8UhL_JepT30OHD>PfBp<81}S9*Fuv_e;$+!)m{nMyQt#<K;SDevXBDFCU>>loz@bNubuhpvf6Jqes$(h<XQ&6hzPkyM#SnM*axSsKEa9I-?{hgi-*PtQ?kez9LQM_CfUOJZ?&h=WF~rz$`9h&7D;twGK)wrf%H#6e7S-nx&ZAD>U(-sX9cH;y84t!1LEnGC{y3~Y;>l_)x+(D|?g?3PKX^wcr-J(0ELDH+#Y^(ww{8wSfZl``t$86O;OmC$zr;X-GxLun}JLg22*oX0$M*3>EwJ1RPBRD}LTlh`k#lx~P@I3tcy<cc57vND-Th5s#utSuqzmud)x%j*CuS#a%TSdu_nhrpg3DVF)T`!Mb+kS|c&?a!9J2SR;6hz>)V(HPcnKSFy?soPi{Y@w__jdAGVCY-D7&<QpvVOSngmB7++(gEH9i9UK+d;g}_M30#lOrby*)_7g!Qn+SX!3a(54MT%Uo#bu?5r~0u#coa6CPxsULtr*8b(T9Hax|fS$%L`>(dyTmmmE5#l7nkKrga`qqmsr)9H_GEtMqYSec;;5NE^uGM&Iq}v2*CE-@K{unCU+ef7dnFqwdJ+hDc_f3}c-ipB**^k`ETYm<gt2uZ&M60MMDrue&IP#;{F0gSEJJpa9DqCA?!Yc`&l5mnq7>a)EM2bg%e`*C+fK^3>N<rV;u;$d?dT=OT+GiY$c0dcvn7nInMoO5nT7vdC)C-ka6+2ot~@3n!LboaEIhB*wb%B&mqHreM@4tUH*J5H8EELx!!3*!qVv1^w3BeAXys45V0E_g6=HGkOzNLVf(m?HqZDT^rUMAZjL~u-YriY_xGsb56#ua!$4|nHW?D7LKoA<T<oAZBoC<e3}j7GJ0F_fM815oZ63PzF2($1!xX-8$9uDy`dy9-k?vfY_qEE<vk~1EJG=oT=)yPYEe!zs)ECWaagLg5NCIQRe2~L-hs;#Cz0S`gQd~9$AwxSSGg^HnnosCc6}e5>eK^e@+|5i_hsAj8R)Ec1^pD3Ur#}pukPX=ag_vEY*1bFxsai|qT>C_KK048g~>s()-YYz!$f_b#H=H91-UV2FQ~+g$p1y$ti5)?j4{`Z3$#{pnu=r)oXGjO?Ms5eSE>R>tqUPhBLgTwb9KyQl{su7F-xQ}p5v_sc1?q}<BK1%c>>{at<)qkSF4%-ps2COdUm${-~sX&`=8tLLR#DsTXoohDo{DwL_rcB!J=Zn!IT)cEw0YMxz5juHd1_Ag5yOmfgU3-G(lTa)Gbc4&Ff;)8a9D&3J?x^7qZRSR)Fif(nOrAFyBS?C`p?hq3MXQCSH=f4!QO{DmBaPfKIR(MuBzMyPE=Ve5flr)5b)aAk~7c1H4n4h79YpGk#!O*+^RCxF3)uO)GsOYfI^@p1I6v@<IX)xf1Zsqn(^R*QSmkC0wGbf(8r>UZV+fG$UU+O8s_)13X4510J$))G=3WU<u-f_!VU^t}cXQmhTOTHuM*Ku(uRzP93*Q*&ipFc<Tso$8`N5A%}6B$26*fX-_u8vzP}TyZ3+U3F!yt$+w2n)X5pdyTl@Rtz8S#I_n%%GL@wp5DB_uLxm3i-0_evPL9-bLTjX9iBv)$(Qgzvz+aNUPM4nLI&IIjs@O;E3yM;;X=9>f_yRh{FGNu=gjh1UEwCZ9oa6%2ZO*e!&&H|w+%7B;8KQJMA48rKocnzx?GN(n98P--v3A>>@R^|MAu0MZuf4g>YoeazA|w2~JO>Dc80BJMc=w~RsWn52{E2p5lO=Nas*aIH<s4S&U=6(X&Fa(}tR+*SiD@-uhCZG!7Q1Ior!DNB3A$w)U2~Jy1V_b9`>HwhS`q?@T5F6%lpyB^j!}lvBG3;Gja5kW9y2JU@@0}kT$U#_E8hi{#GX_uArz=()loJS3lZ+b>85)gr~A~DJ=c`SB%lDTu*A@l3Y^Zgd>vF89>Ad6p+`mV9*$U?k{UZWVvZ?|`WcS_1pPe9{S}8g<>`ekK4yJ6LHseWq7taHo<E;EhqbGQv%c?tm3cCF;}WrTmxz-5Y6o!aG}TSxLnaR|k)+>$2o!&5aU<8WbxdYcN%ErC6f>14ItdiD428ZhNEg;U1Eqy;1K2C<f!K_+2-ceT9GWhVfa^4}`_XO%tI;9NfzqE%e+b-{`$&;LU@zDCQ;CvS3J}r6h;J!<+q%f?V+<e^Y$?x?rqyaVJ>`97bDt0~_xC6Y>?7Oiply*(JIQK6vQTKCd=vFQ+=m@Lv=1_9rc`6!CKzW?GSChTUSPJDMV1c_=vi@~{gGoSkl3r#^7kB^!ZpF$X77;ANr@z=3Ff(A?>3oIG^osz_HPxb=t2Lix4(p_HYx-l6U#AO#3xGe2ZFt>L*U}^M>JEXr<6#c;KhBwqil6Eg!j0}iGhQB{r!`^roeRP4L$#hkFdDBF*U%M8(t%}Fr~L&&N^@rUG%T4;s2uMR~u;*DIS0D*1n?1x60MipaX4o5-^{2Qm2W^jh(pyMtQ2KjFckQu<ZHq9&}oL_=U58Wxy4^i&jFI_-U`UL7pIncse~DemAC;3JY5t?UT2SvX@112gyb`X!zQi6BzB3aEu<ZxA<rU5TSUH1;P?k=h!-<rKn^`Gw#r(=gfEMp0c{>;S*><zV1`|e{Cw>ej#ZP93$R>iPS`HLIP)U0&em}_{YV<Hav-W>VMjol5x{=>HK`cCJ0fsHSG9E4bY)N0AYx((+16}Ze}(eeMDuQ5+;%9Z@NZ(@2nEN3n_I`LNmR@Z<aVLiDFe`x2TMX_xQ@X>rt4h*1p?`{`tB8`1W8-8=<b#${ary*1Vx!xqPic)vNTrvzbnrXz(g=w5h#&Z@jq2w(l5a2LUXljl7<}Gq`1%4o-)-z7rKNr@dk7$-4KUU!F?~MnwOj&$!`v!ZS!cn!RSs4Q+sp8Z^K;RWrt&Q=}|Fb(g&y4Ai<>s~%o57i-B$nfQjT8CydicwUCVm-YO~csFg?X!j{A-)JR%&r|k_+BQK!huAW3K)|;m+Xe{I>%Kn=pLxw!k$%L)ql{&Eia1ITXVo%w%P=N|xh6k35HMH5R2@^`ASE(ontskI(0p8mNkupZIW6L)_);5Fk4)kiO)0|jLkNqln(?G{+-cFwL{Bg-O`|)Y&LoWP38n&~|E*>amm$}h;Mn6vtR_dc1@fl&*2cx^z{6jLrC0L-lmW2${^}&j!$ke3b{SUHF5ot$bGGT*#I_KezD<T0l7wN{;0ADAeLA7%dAi%GJ(1B4VZ6@WI$X6xu|Z3vQd<1zCXGX%0GzB^2)r;I7#}tyJ)0|7#<4FTqg_R;X+&*}Vq>0k$sTgun6@L0nnV)+8ZG^tS$Zb?-b6t$hg8tRkhxo_cWW&A&LtDyCKvK};do#HLZ{Dn<EeD)C6v5?<(9D~l(T{YT14{=GF}b%Cp9_ybf3AyV`@vfU6IAHRCw~?=j<(zxAD#glRnUiRwSDIV8#f{70j_)-F=ScxakRi7_}uSky4Vcm{VmwN4`H<+`!l^YG$GKs8S{M6jTn9qGcL7>K91rA!{iuRF~32dKpu=L(}+V`Vdk%IDI*Gx{~aHvw2{ivzPo|rb$d0J`7IfkVNm6mJVb;-dY$nU${*3e|^62`Vu!{#4U8r&zH@yq)Yb~OojCrb`|rP5zUZ9@KLy+ZIql{UY<FO(r?ouqvJl5<lD!)B5nqkP3%{^+r&*Dxm<t-KqvHONhCP%G={_v47Zn}TmYkOEx#Ddpoz>8Jp_*yeOO2iDRvBI>{N5HAb*sAg6f=6W<$*_-50crX1s@CqZ4345$um~97&+fv);3Toyru2CWldmylF0d{W1%JFMw^ACAompX2U+NBJ9VV7hL|*@DpVrK8(__t6AkE+Xwi0tlHT6i~{CGKWON6Fo?7c$5XmFTKpVRGVy(i9y^h^Q|TT&#=G^gR)YXoZ_3o=wkh>XyY^*BD4#Pm6bOf;!6ggJgrbE*Ua~Y=?o9VJ1-54luYO|NKIdhUIbP}V30y-#uR%M0`86*!(bcC1deOggK6)3Pw3ILkU{4pr4l4B>a92dY-D&R2st41r`Km(@+_aBDS-&Ojuhh+XbcP)L_jGhK3?PGl{pS6KeE;?_(~0teE*W0Xuc8HAnx0W9K#ocMmxOqL5UdS2Ta9@%?Vd~yLLM%N($?jjF%WrC1QN~5vUO?ganr?hB|6<=mRA;4(`fAcq)YD8h9h(mXY{mHSs*jy(SEWujgEKU7F6TA-}^nhQk(?R@<seeo}C5<7&0&qaSse;(v7ZSdl&0h!8H9HZDkQK_KW)u!#~wU0W_{A%rb%_@C8^s8+83)a6qDPhlya2eC0=mJN<rR&1AP{lCyRJL3(W+YA<U(&V&S%3ju{pSR>eYi&b-)Zc_{)MJ$S7Jhz_&Q|DbkI$crnr|>CJvHEit8`RJ-3^YZGfQ<87HY<5S|Nr=0ddMrE?QKaaHG|rUOqsZdtq9H3>)JUnn}uW7_x<tE|MBg&pZ@q}e)#d=@7tyB`Tpy--_6hawzRdGH=2y=H;s)w)_jQ)7#7dV3~cMtoTIRB5JD}+2A4b!e5Hg<XxA3*!t*P>sVpOQ&FmNCwfDXd?HVe`gWGQ|@}GZx{r;E766gpC)$msYX=B+kjEk)A`9s2?-#)cr%(ccWtTrai)MJGBmv0|Z-BBr$k9AVT?|yvjTR@y{%WA~T2E)BJVvjY99scKEzx?|1|Ni;OfBeh55O!eqTV{Xlv~x|_T&z!zwWvnm^QPNR#0+FoXQH`hZvJm<xPQS|Pn&;izb4;f*R=T#xKj~96TtN{7XCBu`0xnei0}CL9hSx}zfI4YP8=aRBM+OV6K0GJd#PPU-WDq~3`?WrU9sa*deXL$SFF+VU2CFaLtqJS06Iug-#qI;M}OCz%jL-gH_Qgmg*ra>N$DnI+`FInmhRE#P;UphMzm{kGu8tv;1c!!^!qQr{q*Z$9`C1noznPjz5Yr0jO;$HQJ1Cj^bpa3=r<Vt7$DKcHEN>_!@DQ@@0>YVL+ANYH1r+UDkru0fS?~E^?<=;*K=()seO0@pAJmxCgvT$V^q7IBBouw{?HtTqp{%&6t!L`O3;!Oc-B7q-k<B$FauKhDD2ld{Vx`~nb&SRkJ_e}(qQ`=16QE9w{s~YUzoI>G|mBsK6-EN7P-KDNw`F6M5{bD1Ygqh*|)f1^0#4sLSYBFU{WnaS)hG<J=P!w#f<xuNwwH@Enie1A9tZY6YF65LaVF}PRam!e!(*fmx;w)n4G4X2=@r#7dQfy6tNeVZU6d1s%Bhrgl+P4ax*zI*@M}5)c^e3`}^NNpOAe~RXH@!Y0f>Am42LwA9Gmy7-em>M};boe+8#(d!qOXk}_fQ(mR96@|E0WKIF%CFyv8VFBd)P=@xz8&7B&ur4L0o0_kRnu(YtLHoF7U&<j=rC}}Afk5fM0VV;I5Ut|X9L`vS^oD)H`)L+&)7&eW0K)V3*s~OGVF`N=P?qGqyISp+xuwB+CxIYObW9qMLjiy4aE7jL!SIa-4A@nv}ENkQf31g>AJAX{WtRyg&7L)~ZOG29TQ84JonV@HQQ;T){1?{r11lN3wZjVJjOwc~#zy?zA8cYQ!im4g9bNfRC52XsAT^|ZQ(XL{Hx1lr>q=pV|4@Oei(?>+Wt`(XoX6Nw&RJP9+B4|VZ<_fWd?J?9@t;u~5anCUDwj%~ePAT0zjYUr%T6^@^?{6+$#YY7xz-WX3^*j(!-pK+&z=-`Xz+&1F9z$7PSM`}*n{JpIDj878AiA<a6^Icv+7yO;DBGx2LtjjmvcyIx=(Z``gUNPfZo)LE#`!!<a{bHm@qAy!Vxpf$nB0dQmCDeo5Y=gPqz}QO!?P1Mx-uo{sD|gq>rXB8n|ED~Iqf~I@b)ogi3%3;-bOKxJ)^L`IPh-T1{d(*v)Yiyx$MIY1`_gWkAR@+eD3I+0D92GW5WCPT<y7oV4mF}3YMX)fmercUi*5cL6iZTKw9G&?&)$4Y)cCgg2NwqeN-0K@l)pgxl#;sk{CnM?bFMsB2qpS6`c6r9ENHPMfvNuZ~uIM0RCYY<b3qXq|POo7pFc{)e*OT7cG2aPN%xe|BiVPW^Om{Q&Js1TwtcBQ(2@$IR?9A@YNa4%|xdt=^;2qDW`b2N)hdZWHADiWWJ59Vjur#Kv*2IZu3*Y9MCV&KLQK05`^pcbCcKcQ^UJiN5RK2L-)0l-lAV%7nU<}vK1K52fXGB;f{H{+3pbA^q~fSwi<k{51ZKH(NRuykt^dt=dB{%0vsIcW$R_w^Y|@;oYewCL)Ky7)3P47x#h>M_p1y|%cx>^EN&2Fj@V8FsMO{Q5%e>Kuyt@=o=JTXHBW28mjDkE7zqa*I`<^OmMSCZkSoq|L6qI8ho1A#9sAjJPs0qEj}<x1?xH6vX-_zVSFpVH$9viY%@l@oOlu3^(6nAfQfr@&OL(0rX?A*M=Z38j=;0o|f_rOOAq_=aQ{V9MxDm^A_uj4g`zR9ZMW7VF7Syq6O=6-!h(|q9DA^wEjNMEk?$_3@LL)||7V^}Iq)HLUjL|$MF4t|;+mPB2>+FVbWm!D}m_av@qi)JJJ+HV9Q5o#c`6M~2?_w#2+`QsD3S62+18HNXc_@gS$`dI)4G`#7@PGC9LulBWBEjr9Wxak8B6?E9qCb>obO0QN=hQ1<H26rSw-wa~JLE~>X1d32Za`)qX=N?o?rRwTJR-`OLG3eK06P%bGFtt~n5}sT3y7d>NJ2!?Wg4H@xj~dMq@j&mS)A^3nt?&+UV)BfVZ-g|Se}QdQ75dp==a4Btx4Ja^rUaY9j9mQ_3~OXJvXo>8)1Q9k5c1-CmZHh)$+z@M!d@Q9B?Qyq7F^9&|Z~>>Bcf#F}Xs<-4*sgWK$Q%cz2pCm?hw?ns()WCa2Z*4R(VTqOG1NHDDc%d%P`4E(Eez?PwDy3KHbA#zLBlv`4mqC0TqAW=>RvEcL!3?@l#}HCpz-@8-y?S@I~(ld5I{LLS~b?ehyMZ{u7$T4-NG{mi_Zd6BJ8RO^5K`I{pkCF?AK@JYh6$;H~kmvCk3MvQm!nCh0JEN18oO%9bnY_4umiF9;6lcA_gZmFSItwR=Yn9JP5zwn95bo@vt`=o)qGjIOMv3ks<cF7&sW*R^_2`C;?6|cELRw!BrsGlmZ>q2hXTC0XsKT=g<opj-&i8LGZDwV&y4aUGOFV}o)w4b8I73q8IQY+8_USFmt2i9Oi@W$6`RLe7vRCi5TE(!gp^88m_E=N|>hyhNX!&$e+{(Mf#<7aVm!K6)@K`0tS0mit$iqxX7KduLJd=N>`Es(=LGTEfCVKjcB+qH~o1_SH9a~P2zb$om6_bicl0Yv7<v^oH!Zm;kysDv__v*Vv3Fj%ulYG32L^Z~h`kIRP2vqVDn$=>4zqhfs>kPY(n+L#|KjHL!|FR1$ZDv%VY8#4jS4TEBythZM{5dv*t4;PPzPS1u@xz5Wbhjm>lEk5p|1-q#}S}Ox|VXT>>E|J*9aB3-J=3=FKUgtbj3hU9gz~4_W3X20&<@96JCFj?(9HK^+K%nYEEZU%H0;Ig&=t%U8-9B_{SJo(vqW1uv3i8+EE8)^S8@vs&CrnH9*CB!80z00`tl}1ms|HFvUy&`_Y64{lJpuZj^F$f{rdNKjzZH5wX@~H>XM4(~z&8=a(G&q8Jh+W3V=st;)o|r^18_PRym{Qh_7TS@?qjASCl1QeedLi!jTa5?I<*m_l??n92v><#gd{=6!o9ABG%Y&+m>i8vm$I}Q{eVYIYDvgxdc8cSzq3ayH6$s4a9=2ga#3U@zjMy@wm%Eoyu<M+!>E#hX-GQ;-=lvaBSZEOsb2$u`>bXqy@Za&LObH)<{jkLNtI(W2=`)@p~&zgUT&uWgKh|OzDyY+$wrwb5&q!mF*4KP7~(R>eemQ~+ps2;m%LtgmzWd`o|9DOb6!t-h-HWb3Sjp$%eB~QtI5SF60&j9)5y3jCeK&gd5=*-6SzTy`ZsR6xh)*{s~&+>87DR8%7`8u)92@Q+FThJn2>2q_-?j7NgdUwDkq?^*Ygl8GOZ%7W3lo&>x+re7iEkxfIY=idy=8+DTFHA`@f3V;WzV$4ay|MH1w>{WDW?<-0NdEVH*23Ap%5u$v?54tS|zVh8c>%FFz#4V-A6WCyLP1Ge2Ysxy%_Q5b&M6m)i!vQa{Qu${l8c+p`Z{69H9?eOr5qCB)ffP)C4N=8z6KLpgK#R*0>!YH~jR;8EE;20cB;_V>kp)f^=Z0D*!PUq)mZV%1IgIiHOfDus5Y*-FEsB{7^Z8D*lC%_%~7Zt)oGB5xdphg!=-d&n5B`WV=r$ocVXh3oQpwKW-E&k`}EgxS9!Wfm4QDW2$Q5PNC(rb57zNR!39UDm-S4?8OOX{>zyVU@`4-W6pF#cMA`t`5-zB-7+n$evP=$r9o@sRCoTybeB%1*i;}c1Q*uLtnegBwFtuODA;7ayNtsuo7O%-cx5ZR~cV<Mrv&n=t3gcA>(S&l9AkksKOOhRQ#7(RPi<$eE;gyL^qD-;iKpamfT$4zfgz<PHhUNHpwV&vF44^m2N@L#^<PZF7SYsI?IUg9HpM0q-V@lN;cvccrT-2pjR7xx2GS65uTRH9oPRv5Y!-=!(LTK)iwkj@{C0I&dm@#3zoW=32q5|g?*F-tf+*BhaD<zAkiR?t<A9m1+dE~>ll*{gON>ry&DXj#_If9l#}!GmPHl>e#}XF&_CG}63hs5ftH+a=Orv9j-7A=R8UEiIc`L@omz5;4`Zh&!!JVY&EpHSc|?_EjdDkTKE8E1@biN_J=T2BYAJvut*j+}Oc}aVl+8t<fR~+ZkdDFo?xo?yM6K;fkDcP`IK}6?zR^Yz?S&t|>V@Aj+C}KKTX?0IF;UQ7j7j}w$}w1;X+1$s+va4kJ^RZtrO3~B(3T+DaWki-6P0;dvu#!dRlN5wO!iTJ6St6WZN(O4mZEwdOxuM;Cks<_2e|a9EnJ5H;G97pxyTBUZK5dKo==KpeI@91u#}(ha^FTDiCZh}p_GRQ3>W4sp6E3$4YHL&)dbBDd>uGTy&I|QOM;S4s&qui)g%WS7;@Ca%c=XLDu0r35!?vkCEU+-$Ru|6b0`>56jJno!y5FLob9kb807do7m#rgxe#V9v92boj*Y3q{H)jxE!HQRp!tuQYf&3OEWpMkx}A%OoL(%~S3>|S@0#TpKq2ds#YO&bPFG=Gi~Qb_-b2#C8WjgUQ(uQ%D*}}Qv&j)?_7gQ^#~-W1-i?IBuB5KGN1H5YGRT9o!)j}7P^dPa#hChRCNYUHh<h7Yf~eBxp|(_t>Y2-&CePbry%(f17w+VJ+e)WEx5z<FGf5gp@-fh*qj1EjaA^mxa2><;**fO3rYzC*(13?xG@CI5CimV@VS^r$-PoMO(?*Ntb=)!uHJp9qSXhvV)S27WTxFd`RjLAmq-B6R^V#vSi(m~aw`<eX*(%RL?h&%d&fGNmILDGqrOMS5+Sm1vqCLi>1D2kprmv0KZ3aIBI+a2;ZvU$A=*#uZrZv(xLImKD@Gpu_;4ewV{j-#P40(GF9ejZb%wLo}ud!rssuu2N%&8`<nA?3YJ%+m=NPs`idDeMTIA@Lve2>(4Rba(<-rspnaPRgN4?oDSbFkPk#M*6Q!iS7<hKIim;v6viHIaCCYtV{bt)H-Bee~x+*wj)61tLUytVs_zR2audcUcbJhSID<%05V)$}=_OkWC%Zusx8bAcKYWo#6)39^E_cRQ1Kfk%z5>0;9>O-FIn{A+jV%4Gv2LOK?-FS%2TM|DoBwIl#smg6D&Vvqr<zj0_k9H-R3zD*iqu<dHP2ywrUx=AZ7P3`yi+EEYaTA*FBJmK@GuHs@@@d1_)3mnSu>-UZUFo+Q3@f!yBST2>t<LW}v~{+;2SXIEVpr0lug9wre2cpxQi3^7@Asn*pxsEinZ@~}g%ga8&C=^!Oxd-Mk!QyTSq5EuRXi7)%>U3JPceOzLX`kDx{7M0+Zbqe{c6|BiEoaBAGtK6Z^yEBOSyCfFKuSUVJfcZL&UaU7xl)+_OvfO6qlpVp@UAv1~5*hFPhX9H|E57-@kN>tdP<=w96)iWW#!cYiy@E-~y<>vYjSE}%3@R5sa$xtc17>SLX-6uUP1C**a0o_ES+s${x`Z!;KIvn2W4u@QF(YTkUcvLH5>;l(P83F2)Fr%6RAx6~!T`ah>hU(Xlu-v<H2q_qbDz8>cWEiIE&_r@<)vunbaFdZv6V&h0ucsX^zA-@(BF6v2QsBq`?SGFJ4(=K?ANnXqaATlgILWlv?P~?H;xuh$*D)~Sz-d1g9ExIn567Ivq@Z$g|VNLy*B*!jMgw+txTg}Ng~fVwZ|kvxFx0FmZ`3od{_%`6svodH2@X>)*)~r`AeLE+)!ciW+_ssn&q6!D4X#NWi`(5VjQfvYyP!qL>MTe48@nQ^0`9yM>gabX$rb~nxgZ+_~wd-MY<BV({h%N)`+o5StU8$#ML#?ze?x-qOMif`kYpj!c~w(UxQ<^<nu-k7yT<h3agC%2y+cMQTU1TaJtppq>l$xuxulsdoSO#cRxy7s3}L`;egD|tdrgnIRWq>{t-rch2*j78sbwv-h<w~4<F$WkUzMxVe%#Lcldk*w?UpD-qNsf82Fh&YA<Y>wU%QWWe1<)!IG_)@MUV@0${XL!bL|BIrjb>CZ=$aPYdJ@w=;;3U>&s91;fft>bkn=K|5%(zb<_He{HeLejx?v$A~u`+-)_HAd^7(oNbzX5&m%!*cUgjKc<=Ixu?B&8DBnEFr&>qJqg}zjgD$=fDYXUh<A1IEod+0B=5HAxKFCyldy42l28;{xetHuEYH3RMIljaFuC#-0er-a^?5E8(Iu+f;XSglAa;}(QIqv;U(}zU`;TuAHnx#zI*rfqV<8{~N=wVPEfhh@?E4(ebjpO~SM{DvZDW4pW%l&;-3Q;n>q^NhugCICKCt|U!?KXvAd8VgJfwB+!>~P{kY*hC#CATQz~B+2e$HMq)`qtHM;(0Nn1-qB=cf2ZIT`CNJ3km{d9_wrJAm`O_E(=MOYCdL*3fsK7YFgJY#N_b*)EexF~9@5lUv$EiTW-<b&(h?a6rJfA|nO}&g;HEi(7lmS8D0wHtc11ieXGp;?y#Y%P=Ojs3t$=4|qahsxgJX`6LQers=1mCazw%43pY(5~QjmRdj{dLbwiZ{JhPo+&e5AQ8XgOCGt$7o;O??Iujxi&$P&6B4i@%tR@DRA=et_nBPX9CCADJ(xGa)kTq&R+(YBxFT>KS*#PPqaXIKKawp!4dqK4<!>Sqz+&6m8HhsO=o`U1J$zWfSM+`fT0S>WG8uL6)cYC}iGS?w~-nnd0Qk@nR(h8>en=}r6B51O5AMnETu9ZHN6-!H+`Hy`O8EyPzU0-UiDjRbGAVIDh(>HuJYO2w)&zWUslHZp4AwWuIk{Y(<D{9OOrd{-%OXkB((&O>M@xTIvPFFBiSBs*_&7Se&GS-CXRZu#MIN?E7>)}yM+L6F(+0OYb>5g(1$5Qddho7@Ip%tm&LQLtyoaq0fi4SIoz&yeHo<nud(L^^r0}!JDB{@z`?igXc=X2oulf{j&vzu`-$e4Qz&;;aX%QSS<FObqk)>2xuIMu51Ql@Z+rt!)2A>`I^I^^thg&+r-4lqZQ^FQV|iRr?JfvJ?a=*`knf$Yb1R}&?7run}<VR#KP8%5q03@EgGJ`YZ0f}?M^qj+g}#QYRz#7!r0E)_288cEzPFHa_pZj#YKx-ZirBjY}l4Bf}OqOS%QQp`Hu?c}Os`mVSy2tx>Rqb|Tg%j5`qTHQT8=DX=TB^TiV1`NI1fJ7P|`>HI*F`baPh@lr#oIzk7;9XSZk=?5_M?^<FsP@q_G0x71G%oYlDg0#Ha8SYys*y&SAin6t?Vh`o7<$;FI*~c;&12!!O^A`CAm>@{v%+q9ij$h-P#f!?%H7{5B*;b~Q$zBF!2h)oH25JQVYRy{_=bfqi<@Fh%3Y0RvY022;;ol(23qr?pG5TdnAf($zxSInJEnTy$yKI3gTg1lt19wn=evcE(Qkb^5g_%T8@3?&jQ3=U_GFKeNLm4b(Ub>4uwXaUt9F}H8T2eKmBfQMTbi{9rYhzuCXbhDX{ZsIv~j9!gKZxzowy~*GRYM5bVUUkx}bjr%)~uU<ffFIumO*Fsp=?vpIl0Cu=GWiy8Mvr72#iZl39Y0WlLQX9pQR1C;E3#Nz^*0@8b^RduB|PmT30-z<?<&y>8$B!9;ybZGEoOH~&>!X!GY}IzOSt?GktE>pn-Oz1bIxiX-A-7_6&&{pS5TegF0`(}_~IFB$6guVQXrns$CEJr=7wEeRDV888IGt^wDznmw7Eo*B3xN<*i2#z1a?f)r_`hOJ9$yqmVpD;NEi(3zkaG4Oz%pLD5+*zlT8;xu<#m7ma1jOEE*RXW~%TTr3@e(yu&L?(holF=U-eU<x$nAc@9*JyrScK*i-tRcXPdAy96{gVprL~$Yk$B2Tq@E*EPKs1};^%*;cfu@MhDlS)oncAG=r5EDI=dvWv1Po#|N1#%uhqfY9#(`ujLUZ=Iu$+>hgm3u1Ki-i)zWw&oAK%OmKfccUcBurv|N8BB^YcH}Q1K*=ocr~g#vM7<d{Ze+?qArOV-eB%7yY*k)zHnc`t#3k-~aMh0u?w10N?8tjZHKpc5txP1jf~?W2TSMZ5ifJ)-dhgLlfeTb%?o?9=b{w=Ths*MT+41{0zn;`}ux7?$h^w`7@~d`TorP^!qQr{q+5h{Po+nf4+xWK<7R*^xk$w!s=wwm_44O+fc=No-mh5Rf;`6nDJPV@7TB=?9nl#FgE$0fBo|7&;R?EZ-)V6<GEY8+wc7O{XhQIII#_|#a@7-TH8;PYX3AQ{^LMnH~ld-l;dDb#|S=mO_RK{%k;R|vZ-pg!|nJKm0edq^>Jpx!D>N|KuvM15la|I9x~~ZGkf&#SwUO`@Ks~Od=3AoxfhR{r&EK7o|LnUoO)tx$dc{q@(yRA`CA$#Z*U%$=%Vvl2KMO9?+9dn<Fdrp8yzo+>VT03pua1h)@6MiMWLUEkZsV?tD)HKKDGq1zFI{)m^I=FjL-ZffWLb-fBE+DxgzV7M(gV(RZ3cAU)8n9%BVRnDq-o+GtJ%;4U%}wugd8lJ|O7UNbPdyQmi530laT4HzP5Lm?8l=qk0<6rX&CSLsviSyhrE1P_L9N+x9Hku$3CJ!F8I81$3v6G3lk)ZSJq4gUK5kI!aOhivlw(M~442<$RNKy*9lR0vj3`sv)RpW=0t~{G_3%aS}L6(@}&PH<?D47vWLfo+xY`AHL}@6Ha#T>D0=WpdpWwHiCVNTXO$E?BlDd#6C}e-H4E~i(cWt!FdUJ$9;X4AhAK!n~d(|L*tgnvdGX=lbfho%<K5izrDZzUCvE4RVZ7au$V<u-#d5W_Tj`eX(1hIo5Q&4-g!c<D{Q8+6Kl=3lu-CFhiMpe9!%>)fdl9f^Jm61s^m0Gcl@zs>?W9UUoQ>?=g!GAB&2H+4;imoEAhzG(2v-7<T1GiM?)Yd8WX~8AY<r6fvOB165^;22Je*trl#_V(5q%xytP-C6_~~d;fVe!Vd@9zrdWyLi0r0@&;g{(5xI+#e{nAt8`&|AqK-r1(PWHIGW_cpSPkAFdIl&+Fbzp7=a`m%Uoyx^4^0h=fHloRvC#FM*wHpza(eZsbwjkW(quc>t@D7K5`~H?-;I@i*r!oVl-U<M>^P9LH&s7(nx^znffIz$D)%R^F%FrPOyrw@#70y{bBQG~Wg&aUkFoDPU3u21$Nn7&xu&MkQ5=Q!@<1lHg(QLxpH-MOCmwb-lIm~w+zMXdndSroGc8Glh-u~}A7kkt38sk*RwWZyaZdMUUi+G_Kp1(qAI!YSZpFN%MZLh`cXp2WN@+i+o&(;WOVMN;YJ0xQ@bAJ-dHzlr)pFQ}BC!zvTQsE(%+GoF%B0SP0~+{O5Gk*LwYWJnkKcJl%lz+{7vX_*1I{8)r>W`%J>4$^O9uwKWT1H&R<}gc0pV&oM!BiLH7<ccLG>(<yidT6t&W1HaZAPCfVK-)p?Hgaft}6{G4vDudp@I8pnU}K9<T)nc*m?_6gS!2_PIW6Vv9%YHP!I!Gip%O#>;5%ftz7{UALCv+QBMlE)#gwM~quh{6{+_)zY8ySOyixhNLI#;Q97g|NW7+%!lb^bSI`|R4Z;49^t1-;fV^6EzK8Vscs6<Z{XYuP<-Ynda`fU?k)jOYhdggAoh$q^s*jgqjb+|^T_@)s`n?{-w;P0CdooP>a;A0@)&6vv(NIEH7UGxz;EwYWD64fw5lJ&<&|qrNk@Bu#Zx1>ZXN7<kPK;iTVgE3G}9Dv{Q7&uN7}u2tN#9rtU-^!E?(DaIpsSxtx12ha?t_g8Uxh%&ae`Ew7;<_^QX2Asi|4FIIP3UjNQP{xQQ2edeieFw-C3@POsmFta=BwiQCNszM~MQSu~L5Wja%Wf}A{&(u4j(elq`8e?J6h{S;}JetlYO+mlU(H6l@nb4ch1jTMdG__La-NQr(Zjfk`j$Q%RXz0Qr0(MMX!1bEZlPn!GT5QV31%{<gTs|DQL$dJ)eO~z);!y?0>ZE(rn0J|H?AqW|Bi2x4^gMG>fFo+N#E+0i8l%pUf1nW1CQ^xus6R^J48qN)x1_Z}8IH6P?-~ohUdZdZw7+Ffel&ja#NeFh4I`7ADS6P?}P|+|jpe6@puS7#rK(MGFsmEwQB8Y`tI=&<_=SD*UoSN7yM_E{E;ne;24fB*hqyluJeX8%#smsw!7xs+~Hi2v)Au$8h(~O=yu??8UBD7$OqAU<5YPpds)d(&CAY?whiCRS8p9d>xN1%4(4rs53d<K#?Yo1hIcMzuWW+!0b5>NU(%j}=|uRw-^7Qrs|bY5h8`sGpAJV)S5CUy_sbi&ZZg?=>|;ykCvbWU~4aoI7fg{GWGkUUo>r3@;{9ujF;0u5FKQ68vcSaVO$<R?7RdF!DXh#hdEk(rX>9CN8%yv4Tl8}M<tE`w@C8=QnfRSeKvk!cr_%l2t)XjdcBVMfdy`T>Y?naxRE-UdWrmzPr|H?kMe;)>h=cByOC9Y3B6l)=_|I}o71b92sf4HF?Ou;P?FKHNre3#zUFAd@x67$(oLu3KZ2J`Wm>O-NoF699z3k;Z!1F}BbNYrVg`MPyzg$fWJ_0DJ-zRwPI(J~|a^mL;^DQ|UlV0vV>qlnvBonjIGg0RozZA+PD_87zG;E|n(`>>{1Gp92$|uLezFUk6Z_^tGBOFx1>uaNX7?S@e2EjUcd-3$jx-(TRt+Ys40KeRV;@c?cV$Sx{`KlVQBexOkuC6cOWU1P#~4a4H%E51UU#oKN{W=lPqh(~Nql?T#`pSCx=GMqP4VD_nA4eT`F_vkJs9ywKAlaYuOXX#p;!?R9!h4VEPUo$DQlL}T*9lN|x88Ral^y1!HD_j=zXw3yS-G&jUU(NRPSF$vC?z#NbrKg2eu(cT8xd!`VD>)b%yg;|1RhH|S3$lw!IDxJFp`D@HmZRl4W8tlBP?y)|(^9kJqbp9xYLGVEuAJASb1#Mw(E<!dK{|<~D(2@jx(2cqL^!xWQ(+U$eQl{I%Bes1nM%^c(rm^7F4rHUACW7`fAE^x8F`bB}LQ|g#dXAuKUbMjpVZ+A8?V&#rB{Q&NOtdxG7HfLpWIAg{z78C(z8eJ&K=f?hFZq_Tr7(lUP93EIHZ<FhsN@n%!~Cpc#rEL#klYiiqdum}E@FD*cUpq|xCl^&QI%rRz@ZFrO8-Jeyyi}UcFbYw5C+Fo+~$-lap}|N`3}$3g1cW_J5YvMNssyydH1zsgO)o*CsCU(nO%|5f*cjYsU2mPA?H_@p@s<@WZl$6`WcBab4a-LewgL^m616mi21VFjZ~i94d>o@{=E!qr$peB;)c(tB*qz<(gH&p*PSLMzDE783|$Cxo2v#l6Q<~kstXuLf3tbAi#yFRDyD$w$C^@Bt%K_X{wk>39YdT{{5qq4aSZyqn^|jJKrk?&?vaSyER=u}$3z8mp$@v9haeP+g`U2m5KB$GuUiThJ1T|r;2i8phOwHEpy1*Er6q8{p1@H}E0d7Ppl5|<ra?-^y*_pmrm=4mqOJ?Cwjn}46ppacz(N`JTl1MYU=f}uLgLN5tEogoXCz_3BlP?aoAZ)7-i}eG_+2!q??k##z5ik0UZx!;x!Ow%Jw=VR6KcS>*HHqxUIulfwaPr^>2XCK+7QoYb-pn7R+*<xw$Xo&|2LOB4-m_467^aaLOaL#|6{Nbkvr8|23A%h=w}@mw}F*W7bW=Mu&IP*4e&10WHG$>RZ3C|Tcl`X4j*()a-Ec=6uD+c(~C^$O=0FrA!17i*QE+x;mgrLIte!yiO)UXI)UcJaBkXCtD`(&CO-+E-mLKPG0C;NY^b%~vbg&G(ztdklHzp%FQx1~HEwgmu_drxgM&zlv@*`np$?(rvN)v^RkkNBQL9#j61mbk$>@C%f`Bq~<_YoqKn!J2;=p4%dUH~a{?N}>GeWZf=iL~DV+uKh)ngFa;QGSUDdKe0It5h~v8x5By%d{)cw_WkH6<$o5>IP)Op5!9{|SFP6qnWX9z&S0qN%0<z716BGM$Wc4^W1VQQS;^(p`d*bAfMjX+Zzh-ddMQru?ULoe`yMY4G!MKN7>FGC+(5Bgi?oOXS=NIkm+5OybZhnrDvFnpf{*S!A_R?*Zs~$p|)#xpqs=XZ2E)5^q;{l4Km&HCNn-={hy>5Oc|{gK+u?e<t*NHVY{^=Cek4EFd9q;S)?jpBdK&tDcyTZ1hKuxs(hw3P=Vqtw`Wyvy{LwqBY~nc$s)H#c4?~dXOQP%Kb*0&ouvK{3`!t3o~7Se(dqJU3h7j@$+!Fu*$ciC<D-TwzAEt&W`s0gswcLHF9g!_AYEyv78S6K8Wk-h1K|zHPr%)3EP%FaT3;JHM_vXFuR7<z~Ldq4$`*gvwvB)0zS|zx0!n6uGjoFt9|N|EW(955Cec|Kt%l$z4WD(x@D*}L3#&!dR$Y%Ej{c@f`5?}H?UM8759<Y5y6n7esnH05emEJh)}^zArEVHlS8eFt%>YGH-+1u*296SLNvE5By|tPi$J%K=T|X?F&D&5dSntF*YSSWVU+n9<4k098hzR%)oDDOL$*bAn4eYZqUG=eaFYKht-2gjDKw>2QxuiOob~Co4si`3!HSgmTg3G1=f|=T%Fh&cFt0^+M@SP1p#g~6<-8ZK4!MRCDlEwFxlYm-dg8SK+GbFc7*-aJi4_yYv{DeZUTeTLlxAiWqc*vkw778_3rjUsZeJS=tbFD&r^$1AS#gNeF2kL?Z(9jru{!3I`o9dCN?8Sufv$aB<><62TY%h=&9i0q-VGaUbz}-RTCcC;mPv8p@SOuxfsdjKHVEm&+dQUG)p~idzmdfRINr&Spx0^Yq~6dWFq|OF?I2Pr8@w~MPE{^=&=#_Xr0FrrSVY%fn;asnHmKbUbO$s+g*^QJRpG&$>-0=v-I%f#x$%8azIOq%G(<jzygi3}y`V_uFG^_FSlK&OeD{;sRJvJYzql>%YAXk+1a_Sny}=w#9{A5%x2fi%AX2G1&j~v2zWUw=`E`y{JBC=hO-%TZQChDQIg;yL&6`@)plE_<@ia9LhYR@_X_P5PkB{F0$EuT^N=`K-H%{%oPJ_iWr{bG=dS{^^bkKa$Xv><c9yls)8nlDJ;Y=u%kXRl%m*M>iIez2j$0*TE4%qUf!q&S$@70&pb9?@3S@q&Et$>CretMXmGvr#qvgaBem~IIm%9NM@{Jfo$x<}y0S_hQ?0Eqc^sH#8$CYE!PvNP8yjryUF3!wc}p-*MI4<O|+qbbh_aPg1oYrNn(CusoYSPMb=mEw@iIhP@j;^l5{Eh-H$>xuDu`dR;zKo4~cvdaCtuFzj(;4cv#`PCjyzH=IDce)z{6{M*IR8?sW!FL|~$F@N^6AGosRgl}0-lDD*0-*8SA|^cDxPA>5I%sl^-i2tU_++A|RnZivi_E0KsNsXD@NAt*iSM|qOK1chq(@BRnMi*JVBEx&*;N$5{YZr#D_L9Ko>V*?nCCTaqez1aNuTy(Src3r)`_)&x5$3wJfdWeHkmXkov^imx5}6q0gCDp0#qp7u1vbYG>1Gma&1)K?c)J$o}O#wV2*?~z!{~jql|XTP}<^x3r6<v?l1rRt|=JIdB4v8;)5wJuZG~cSo<@dwMHBaO2eQW#BnJ)^sjLj;e94cKAbsQBfcoVzsiM^0JuIo@vMcUyWWlHPhTpfqa5VCp&rJ^6F5$8vS8h1f=v(8PJ|+Zp2kmiOc7;48R1Q*l>{v%*Lk%6*XD5S7b%=~-Golt$YFK~W5Jt7zL31>ZSPFFybIAAcM8(}i$af1IYd1Ox-NjsTnO>DKg{pXkNd~Bhr`n_s-H&x_^~km3pEpDigHfyO%;^hY~Oh>(JAwiUulsy6)OG4Q$Fn7yM$|dm^~BNkgutM$HRB}Cya=Y`~1f+i++=#5LZt)MM>qN4t#h(XsETzw70lYb-hkn72Ek9IzD9JYv#cFl#*c?1Y7GLKPhDQ-U!*FWt;&dI(6UDmqp|N4N#Nh`hbmZza{i3*L{DsKJkLDVl2&QT*bqXEyGi-rwwr94b-lB-S}k~lLd;&Pj>}`8PJc{h}4u>g`&;NFsVokF2uv0J68!2_9tkwM`!Jv(yC4g7l_Unixyv~E~o;8ypML1YcO6k@FpPgEC^aADr2eq^QAnG(>V08*~%2mz<TNsf}Y%S;3Y2&+jkHKP-;c$#rQ&a?yGNxI%kH;6pk#YHfVNCa5>}GolUFggqXQV%DSA7$Bs9)fmhxqLONf@w|GhJ4Oh3hFKHkhb3`b^^25*B{U?(<ozEfK#{^=B`lO699ZW`=#I>0veMC3iS&NhK5|y^!Z7EP}F4OpAgaCov4l2NINtcqB$$VpQ+qpOMIn_yw5gx{;wuPJ9ulfJMkH?y``#HDyzcom>IzbH^dz(1_V)8slDdA+Vm#K<jOVsrwq4`U!XZZrq(&Pd+jyW&7B$m$yN1X*h%)BIGg!|=Q<&j&)K$|%ZA{m!&Kp*ecAwDKUB^9E^OvA)E=nx~%8j@1zbi~foye=vS<1$CMdEQ^@*B(fm=Ji}HjlO_Roo4|9C|-nY+@g-O9AC_{4voMS`czXo=iwG;s*h0%q;i0!f(4?$A0kShl&<3LJ0F8x^d&|H!dSEp=SFImxEJfWV?3`i88{>~3Jjju7#=%R7W#f#?0M^BLjnH0sKb-eEwJpxY&Z5O0@Knjtm8iL{38osEoY;L!Klj}&iDX*$zEKVj5)?P$z0?#%aG{7qd{PZ%?iq;OQ{KvnI2!rDwer!?4_)F4D_0>IvO=>VcrXBktfqYcu5vW1SHV)PngZoE8<P(?!*8<-Nr|!%F)P3yS>9Om@Gr{&HJ7C{_SI?T%2jiw5Weohx)P>IsRx7jn)r_2oS~(WY;8BCB6vJFWa6lQ_QcY=|sTXtE%TtHmw_<qP^%Gmk_n`5KALmq5b0Wi_Yu`OZAVb?)wr>_JXzB&nj`q-^e(qq`efXkN1?}3=7Q`fAqrS%Nmx{n18~$%<td2w>2TwNJ;Gn;H^BB6F9}|BXA4@O%dN&oL2@jwW03?m-6Ft=?SQOwznmz_H{_F$dvK1sI((X{>Y(T49j***Y}(J`Q1Oh{r1xz-^>qRdVRLXOZMCQuit(*KYv3Q3(xR@_x26Vr)6E6>L{?R>MMq7@fz_1^QeR;BDK)%`u!VMx;(YgOcm^TNmE_F?f=ex2q^J~9zgS2xIT94e6)*W_wW8Uh1a;9G29QdV6WPY=NCRl6xQg!1_YemqFXuH9A(J=q2&(&2i6@HD!&i>R`)f(df#R%Jc(cKl;8#UZ!t@$o!9~gkgSybf<-gV7ovk}eEv@`0rd+_(&o?4+rNL*Sc13kby!du_>X1FG~wIaC@t=KRj;ujSs{whx#ygU0G&yOzkK`1ARck_b~x-~om6V>A0Hd3$=j+P@xX)OUi+5D8v42a^RHii{rP|Y{Nz9WWnu?Au=};Mzjm6v=J<=n@Ua%Po$~YQ+fT&J)NMxeN%88jp;7^3J)h%a`!$YLyQa-|z@3VkP?>Tmp|gE>6eNC$`^xOFOXl+D=;6~vN!@Gj)(RNXx4AbB(}!JG-oC@I1W}>gq<;N#xRjo1N0dO(FkROM?Xe-@fL8*YEUER3b%UY5YwyYOWL*d%9Al1#ae0!e)>!-QH-Fhxj;eN$Yt(BlGb5b>e{HVxr{911?WbQ4dwD<I>y(B&>veWn!u=Ra#1iYgMTEF6`VAJAfx6(>RC5@ccFw;_SYk9MYv?@Zie^d2waUc-J|O7WFwhoXcD-it$PRUJ4?aDb)^E&vgvY3MJ?lnE=KP`A5#2tzQJEA8L}_l-HeY(yKKtIE>(!`FQnGIB=;D_PAYJoZ)#p*$X1QJq6R1p95k<zGOBp%Gq*0@B4mcFkdvmwQC+17SMJpo8sIjR;OVelH;)coJhW!baR^);i@269wZ`{Y%Lv&(f*0?`Qi27Ra#TZgMfJ>^tD5jp)+ha&ekk+7-n1+`70frd55FcR&?d0Y<7UM?#^Kb9(e}9PLc{Zm(9oT%N1=0dKocogBKAboo5^W<&k?eXfk>EfLliYS<?a^c|-j&H<YKQ>nLu=D{-~f7@lusnj?qiL>ri?bxx|nx@$@@CWlpdh-eHs!}o{5*1%9BgM($w_i+eqXwg9k@LuvdO*SoNc(Aqs_UcTj*P#Q#jHIeM~j8bg1YG%Pd=i$Gw(7I^9WX&mzfHBl9mHL)Ha9^tGRRu8NKNaw}<v*&qgz$Bm?peiIW6TwDyjH9ZBH4*%qY%2zj>(o@epGtteSYdT)O2QziLnzDx56r%^j3&k!{??b#DpS)mKmn$doTRM5APUyM;3b~qR3LL(FhuMA7&Tk=ieb;Pp3o)2q$w-C3M#sn_p=kWn=#RXD4pr^7d*AlZ{Bq|=CtbwYG#IGf0M+X(>(T!!g`k=z1{LpgAWh0MjFLlxWSsfQJQtAafjwa&5IW464K*Ns&kq<I04xmqIE-74`>{cd3{#2-Kt<P;~DPhat>@u6H<f2?`57^mlm@8JHFGrKbMut_`3Gf%cvITJ`@(*_}?NPiHlAB>$h+Jd=Jwp=c899buOGKi+=@G?KL!#lVkDTn0n4@{&&m^*n%(;D>Wn9%vo!DdL6}<{9~|72789>R6sixqw$+Z3ygA8v1*+8*k`>DVg$bjdMf)fV+)#QA~*A%+`U0V7gT=7Y21fj@Qp}yui<!5I7}6XIG=wXl0SlB(`7=xK>rBj{?ud{Z+~v`+JtIon(8RHcxLF}Uhw&A_KG)MuoW0j|D_7tg|xDI|Hs?YB}%CYv9B$1oa+-FdL)T5)zBI;PDn2D&fI!CA&!xx$FI@!A|OOWjcxrUJ}nz?m|K4AI%ig<QN}W=Ra}c8fo-+^P6YU*<_od>JB0v7a9#ueJ#%<HK?wVTEdhyVU?d!z(2P4VvsuB0UxA@4P;8=VU?3ijR3`KL-v7CWKfC^Vm@<5GYfPshUY10~k@Q_#mnW90k9^-KCFCJj5GUc(;52PLfeNFM?BnMH6khoTxBlc@&n;|J!fe>`*%@Z<w&gT4TvAQl$VYD}R7J_%JZ7lBp`2g}Fl|R=wD#h6Y+94MX=SAX1U;%pL_5Rq4AK6^W{pfOWX}?LULxLb#?6+vT(?ngLux~;LmZaeWkPDCr0eCn)J@q!P16ibAH}qBS-6k)gsREZU?ExR^&JH_&7#pB^cSdol8KZaxU3`@DDH>Q-Z5?4lbws>`b8{8lOoOaq4Y8W?pk<Gy(-VX%i<1E3AIC!2X3Z&?B=1UQpTaT68be%&{$VEXlGFS3>QFuM7E3;$YSk}H#&_)Rv5G~GkX~9{={c^9zqIbB1giadys1M^4asC`w7wE1c8|Xf)PyOJVZe6uuP@jAU_}%2p(_4Z4gr(7JPZF;hr1V6u@xVfY3ii_z{O$Sur5tAn;=jt8DXuQZ$2&hI)`Vw=#$93gA7lg$Puw2ynv5gvWfY;7(Hvb4nasr;kLwDCfHLP56|+G^6x^bxQ6rxkM_C=!?l{6JQjQ2w<%$G^c5gY=iEyFe%u5E2~IFr-R|ujsez=3<Hv=$*)=RD9)40&QFOuxd)u%1V08=JDRdy!@<k^oq3V1k1V~>{UFW}9+j!fLKG@tz~r)qp*OIy7cx{LoEsnz4B7(LLy59gLMoka{%vSwP`ei(QKe-cVKo!QnjgcOdpdeQ!L5#G31wFR=d0ctPUV`9xzsKeciZm|_%1=CNUCx+Hvkod!X2R1BD*f+pRKiO*v%sfIY!nWKAMP%UaxKW%iCZT?DBFUrAFN(T3nG3!Y*|!&!A@A@v>YF`cdU+t-7p+OuHXrusmn3Zq42PoRrs1@8)7Lb%L(G%+~N?km~-bp5z3oSZ}LyUf|o<7b>m%-J)l+w1&I*g+9(Qs(DBItlM5&AK|NH=5~>^yC4C%>j7FiK(8)K#4UnDLU6Z#`5?$fSF}uSGoF_|^p&a<9cxU_&K|cBh&4V9ute(EeRt8An#{F3mKr>CpbYDaicxSe<&-`~vpz|_*ek0G!NIWaj0Yd58^OC}=Vg;)s03b^)y_SHn(7d>QXv=iggNSLiG2>IxIt!~FJ_!!-8$z59IRK5n&>U31are5RzQgOTIQ_Ct!61a%GKd3NlA)c_f-xNY9vw$uQx5ui98DzaMj!Zbb|f_y}gvkkAgNCF9ozlSr@(Y@>IvUUO)-_=Di}@AUpT8>VF*)s70{rluSZyp~zyOlk*kHwXG(gj0&laSaF)-Z+g`V`&%TG@e*=-R-)#<i+jo{!gn48;uK~fI1!C|X0MC_2yulu1C%@%ym_$0HXg@J?qjAiO4kLH`}re{9nw$U%p@Yj;QIEWQwBjYU1IW5-E3bw5?8>L>DxrGVoavzM#@|~yz|^pNkx|%=7reSQC4I_;Qff|Ey2{T7-uS#IPX!X97!uN;TbPy$A0Io3h`rW7PfDTr_OMjRvAWBBuv9FGGHYA3mI88tBqxL{Tk^l=WJ&sp@@#sLTMV}mMY}^N_BWM2-m8Vp~&zr4ql)Uq5dl5T)i?x^03%)sHtZwH<?miJkxx~SY@^bVirK7Y$i2*wHLrPI;Ee|V&W8s8f7_O=TVoKMh*4ov+SBJW}7r@T*$5h#RwJMeNcjd^B$uVHgFQH6+*cHe@fW(1eo7rh?AOSXLKZiW-7o0HQovsn2=jec(%6uOWpXW=qUi=*Ygl8Q4R*Wq>O7<vW|Yd0v0>U`S#SN?Ma4yxDd$k*yt)tg&)zQVo@d`;-hDUChI`x>Runa3DelO2@xjUOZST9dWE;DH2h@@-AYd{h+^o9lN+NtCR2%q&WNjkGv&S9HZ>r%1RbN?VeY>@`_MJfxEz7AYfrHR=(`N+h_K2$%H*V363`I3<jCmxxy5o0dU}qN@{9edIm(^@o(ronjW|ujI;-+?kNCpa-x@lTkfmXJlelh}L^cr#=S(g<7kdnLkvEQ_Z>?pbZF~&2ehh3+WJGzo!*%(*YO376z%n_dgt^fme;AgpDY?zlJp!d+MGFD1BAFZWc3BglJnX2Tt8qvAhgG6vjMAkcYT)$ROOdN-G=s@h^%P376e6{Ra9Jvu7A~&?QDgzCm!(JoR2^1za->-H;O+;wmNcLIzuTWJeGi1%c@SZRjF&NF;C_Vmo-(qrJlH~6pA_S_***PKhC`5t;*h>IiB?#QQKgV#fD?!y-<3`nGdGj@_V0d8bZdDb3JM=#Mb)L(glk6SK;Qg=4Vvs5hUSzy$(;fs5CY|7-I}gVLLfkeK*?L`EO!;;*e(6i1Y=q2sXh(oRB~{s$MnhL`Bc*7h`Lj2;uCwMFY2|W_7bTEilNbWd-~TLo@EE1Tq=)E{u6O-U32~4j?!p|B<4vcp+^80nG1o+9}`UJH5tE40Dv>$Q+H7cjTM`A0&8*YKmnFIN-W1L=wM_~=TMaA<eJTlp<VGKuaEjM<f*S=i(z6JHb;xSbJ52VMIS-}JK<%K3=Ke9CGb^cS!97+@6GCZgb84cg&a#Rmh$QW5{p=Pl2k-nQ<!N)rycA@2v=p-A;X|VZ2iNTf`035K5LYk1sWo)`>P|Z8FdINRX%>?W;}xPI;<sjb{Je=6qZH7xK|EopxA-`<<-5!%82FIP^%yQnr^fgPxH6NukyFHFozlx78VZ8U|c)2-EC68$=tLJLOOc8`+#^!*_^VGXOUTH0>zvT92|HpZmFUqVB?_muWYlbv*o>zVR%LvoLuCLwG~^G%8d%>Fi##<c`a(%9bi@7zK5sn@@n&p8@0F^qj+fLW*?HdEq(ezCIR5Ob2!7R$Ns4nyt3{21bfyogf12<ACM=a1OVZE>eCww(}!dNFroMaQABA4vKcZ~(9ObkpDVSf7~kz2a_s=~Vip+}&a7lK6`dRB&L0z55}c}1oj7V7NRo)g2$gdt5jh4|?Fq%Pb4<d(G(?&J5K?~3E#%1rdf8erO5_q&FGx`2*hBgaP>=B3f5xllHk^<Kvs7U4V?K2lWdhSU*&iK25EJ|Do#eD_acu_9b$(WBkfOj6d@6d8^cZ=e>DihhPAQ;t`O@&MhOHKyfP;g}g<NwMaQ`C+TU}2jp6?<%Wu!@tkYq$?6xFzm=YVrPbyPT&n+KiIGK{0@uy-T!afGGo6Vq-%nl-hZ8ZF+3=J9GMAI~UyZ2=@{y5sgdmRqg#Ev+r9vU&<L=gW%}G!RU{_>OMad`>Q8WlOX)(5QjoawzHkG0>%>+|P;fDS3!+LqjHvI_4@4EG7KVIgdhqn@t7A`QH3zW9W_)?S$3A-1<u$w@fk`=V^H325{4Kr5B+&`ZkYgRHdz+Y*A;i5I%?!D9>hjed9MxolHKwM=Jv6+O;r^tIp9SQ>k*blJ+S-6g-YG>3CaF+$O=IP^YCEAu4OsvVQgts#zpK+|C@_F`+dQT0|-%kTEz4l;AH($gWExbe*>6`d^x-`D@Bmwdswbtoi~J$S+Y*<cC;Hxh=3^&z$7a({0YP&IQML0NvIu5eB2QP#;5{6XgAU_4^O<>l|Nv46%0GobdIdG9)RkHP@G%*F>eug@L@g?LGV<Nrhh*z)hVuwVFs_PSLJw`bG{p)-lqk0E8Y^zYm_lCOQT0YDi0;I<`6;AkUAB?L?<9+O%;+H<5c{eUWzLs3#C*HSCTGI*J=Dag&t>C*Mul%W0~T5FFH6pCmE~u>y4;Whl7<qm|J1h6MOA%S0+*@oG4Mn_QMBRUzL6&dHwCIiX>wWz_*j6b2IR%^Avg=D>YR%bsh)WMWx>q*>xMifS-Tz<V2b9aQonz(?Gn+(n=+j;x-N!8{y>V@jib#$!xHKPz>A1*uMXQl^U&U0)L_)uOV`v!+g;V2Jf2hm*W-ca_ORcpn-uZI=j{{Ave8?zGHx?XH(d4D<IN0=4^|+7x|enhq7hBp5xXnC3mv210~Ie4#0Q#-|5b_YCS8J_TT}unS@<2LymFv`L<GXj*gvqS(mHN4piQMu&<C^7oqN9=I>}k)r3{Uas?}5~azwv$b@!@zzBqWMgQqU<37VNxE&Ip{Xu&pXf4o-6$OIL+(K#%dfL+vT~fPg&N5HVD^N%gfHZSu$w84*+&INNHh}eXpIT%?Ggqu<oNQ2?Bc2H5&nqoibmVt#BckW;G?rw!=}YVa##6Y+;?Y_DN)m<qBI87166{H65<7^z=2GR$Fv;dbF;|FfIGfn9Rh!hzjzt&1Ne$*8ex8hx{k78%~1Q}!Z8ME@*VNd{+a?Vo_F*7FFw@b^2Q_#XJUGd_|Fs;1vw+YrGU}DGHQj3N?~n8V5C_2flTBpDvYaKx(yoRW+yrFS)_G(yWBvRYkicbdfiAJWZgp5OA0atT!Utv^ajES0EqC9Fiti^hf&wCxcu=Rbh>@`<;j4!!qqX9FM+?qr(xa(d4hOL!!}#szzF%cu*KBA_S-1CkQCjKY*d66zOC$m(M}29?;(YZk5+&$ix=7Fz&VE78PG))SeoC5fk`K`V%_xE4m71-7ry<!Ho<Sdkn|vq5eMM4ttL_+5;B*Qp_4DdKQ8BWw!G*9?N!RSlev;WkOlG`$!!h0eNqE)NH9R4q$}h>D+sK?rem(Ca#q4bF^N;xYVDn+qjw?kE~=C!FGR)o<CZOsCQ}q;GpY#VJ%+MueH1aPv?OiT=+Dpn$F~Pt*l3}hX5;v=un-Of;N|-h3X8e>&So@a!p*B%)TTCKzVT8Y+oofb9elr(CG>jE&ghxRU^pG~ilA%psS9l?=9q9F8s@oVV<e6c5*DgtqMwJ5dLDbt*cIB&9QD<JgR17CAEus}BJH8ByX>D};MUbF^>EC&P*P5?#W!@#7#sSM^U4jrtxcyvL@p^6*e-V%73TLmMYE^}6jX(XF#`t#d@C|;fDpg#`?KJg*L)ReZcLo2WEq}f%rZi^uaFWx1~w+u%_cug4`@kYc96-Kbo5kf*`q*Ea~UQT(H&%$h~MJtl}tVGqwoMm{R<G{VoP*9Pab!cG&2!4tDZ9`5icsC^iL2`5OH;w%d6JET!vgLhGU=`#h)DQ7|39<{=SH*&v*HkVd>TU0EGu^&R>!4NQt(Bmv<Rf)hghotaGyIyF@C>;OK2K{*a{k!frkQ`qEWPz+t+Z-aV054iUZ1y*m81M9LpEdUpga(N!9UJ{3J#`VqKgI!+#6;$DoVnfurmozV^|)=@$N7B$_mGz=S5u!&qZrjGe+3{|6bpEK)jv*?z|0C)k)v-_nNtLXcbOk<lo$m8AOK?Mk#6fuV*2p$5LZ>$M9w4iDg@v?)wmNFHyg{UcH8JBc}B@0cd{^rBa+2h>$D_n~!IFX4iBAU5iwgb#6IUA0OEYT!4J$#Q*U6S@HC0x_;tMfVf{mD86#&=Qk2wt-grM5e}bI8Fh)6h|6K$;s_Q)kh;u^&ZF(=<Mr?t{z{PFszgp%8?`t&?6}_dIjcB&PQs2BxxiqIX71-LW5st@vt!Z<*%*`UKyl8G30Hms>QQ&?ojhx{nFUI*f4l;a4#c8L>J^#3O~P_eNRO<>eW^G06N)i;O4xP?BUH?~3LeTsATBcQ+iXj)c2<W)Kt*q$gcmgVxX{A^dnYX4>?fl1t(MIfb5PK;SCC{P=W2Y7U0^OOaxLd7wmGM#U1%XpWdXc&zJVSz>e=NsrBAr`(Y3mOyzlC@~vlXZWHMhiL91!0(|)>BPxs{5p^EEJ+Q{v)&GaJ?|93D@SjBWJ>wR_yr{*WLZec4*0k>1cpB(se10`$m>%uB}OvZ)#<|*A0DALw{XTr^P(Rr^p2Q^v%^2<vKzWJSY`2JC>9Ysi6VV0Lp3^a_Pq6RtAo^lZjgddQOy+a{6|B$1(G~kLY|TH22rcrk0xwX8T2eF)$V~{Rhm=?X4zv1ZgV@!%ME82lVDCYDX^`hr3i*#UdkjBFVkfeh@^s!4L1=f+pRKp3M~in=7bU|Xwl_MUu1E_56NZ`j$tSJ#BD5F>Y8Z0)e|q#zx%w0V)x5Z!nm9nQij7-Dx<)HAwe^6R#rW`^_s8ZDwUseF+Gd`j0qwCx5+lV4j-vvlR7^ebj8(+G0cj^{oT5E6kQN}StNerOPD<jgYC7re)E3)zkmCf=|oA9mkcTLS8*aQP0zZNg^LATmV{7@5Y^e$_axLW=MRP?kI+iAAWFBTcgDbFqi{r8_+jhP#_LVb<(1`mOOU+N#2a|<&rkZSt-vUrPU5r-Ta{n?P#fXNMp8Q7eOv5-dbszoW*;n$-64n;8D_t@|1kVheY{z#xn+iZyfJ!b2mG62Ho-zgQ8ZKdA;p1@j4s6e<j(D6w`VFL!P4ATU>$0&A_z{T1=J@2eN$MN+Z;oRPt!5Quvo$f<)Z>WS96e3>`hsC9kwnrBzPdgK~0VLJVhatk;TJ|PyCbk?ld<@{;@+%YijRW2`);5SUiS-rbv;KaR%B}5-x2>KR%akO69Y?EeUVk)mCK6#FuPEXeCb9UQ=Ln&}H8DN4xUJx8HvH<D2>6N87S*k9PI9_g}yLZhjs;SI}`k$WX4|G|$+v=1Y{6vwZ~Y4Qsupa}@TOM~G>`K=>~(UnyY|+O>td@cfEzDxs2HGy4T`sJt&kyLRz^|9^AevK&it9Q#99bUnLjITB$c&4xTOacEdw)0gPq?{HAn=*sYL_sGVPv>FUf1ITA&JUra<+aE6S@4tSy{p(i`vk;>5+LB%l2#0yAP{A^)g%1nB{`prM=I&_CB%GjVr=FwHfB*5}qA3_0=$OgqimLwcXWxXRL#%}pJ1d5J<$f3z8T$X*KmYpcpZ@Fjzx>-j!xIq)_PA#8$4*1n;DAiP&9Ka_75KX9@h@WjMGM~_?pc~X9U4+{FxJ!PAKUNAzr{6ez60)*BBKLod!`R^rfr{I0TJP!L}SNzc39fJ{5pF0e3ly1J$c$ipMZ8~n3v<a@{WCj%fK2XZ`dE!xhEg4{A7=<^onU18pd9DCD6&TI6W9S2Kv46o~$oc4qys~F4XaNUlh&Dp?=jjzh%G8)gIbG-WBI$kqmtdsg_^<{@1_#^6OzQAE*01mittE2m_@=i~D$2{ocu2MAT5!PcZO1z}gP?*_QsS`Bw!?jOG*#oyJ-tr|Z7hnM6Jy=-60{d~n(Q1ZT{sAMU}IN7MR^b&v2Em1HV4`3CZ#B`j-0!y#&lP*GfP<Wb42ef7OR*Q;R*r4)A9(M`JcB09aUnt2|z&9CD@Hbe#?LXmLiQYz<|G}blF0Y@@tZ|<giV!k9?b6c^@4-LtnHGTFiZkY0I*k6$TN&&|Pd4^n|efWM52fb6rpM6zz>wAmxgXGMkY%9VYt8(BRLs~^zgNjQ9Vag{xgKuCH8Pi<H8r;Z#{N?@qKctTG<EGq2-65iqQI-5$^3Oj`oR6|-)tMsM{a~V?CMMe*<HXvd$y~gv+T(b;`44SO=Ya#53D~@lJbR3Fa7mu5q~1e~=CO|Lr_Ja07+pd4r|{BpOo$UKjZHZ?Mk3D{JUAKx=qjpB13zlKsZcm}^a+$1{%2B2^plO_ApL35<<cxH5}6QNkfrm-rd*4__@UlH*#x{k;^U7iz&84=L}~-1^H^=@k}Mn>$`?=$;OFGBZK;W1BRj^ih=+_WHN_W~0k4nKyMA8+Z2VpqY-~6~KvIW@feH_dvFAl%$7uLlU&gCUjggxodLYQNaTww1{g*_zvi1^>b}Ep$Ef_WuF?rwSK#VGDh%zB6W#v~vZB5i;w6b@P$^WW!X3jG6(n7yw*X5Yg-qX?>&9L@2N$fdJL(eFpcL~zlEzlVJ@yYG=;EdyPgMrMqi&2HUjoqQCQ1hZiI@#L6yz^r$9W>zV4$-<Hs|Pd=$#n1Q00m(!1R=M^Q|{?{4s0t6(}BaEWu97>7D|F9zSFe7mX)gby78~igIk>Yc(-w-KIRkypdU8%&p&?r<6Wjx&PQ(^-MMi3N&XdVGx?~|X@&+Z_{J>fyr%z&c@etgG!mOj2y?Cj($ft`z+zyqYXy5&Ax$iF>=1zEG0M%ws&Ua6+L6Ly1Srb;IkpA+_y;<3O*oXpr^Fo4571u%>FTX&_VMe+3=X}>ySWU8j}wNTOWeGvA7B@@hs^Fk)}9aeVvxwv(&FPEKW(=x^M1I&U(E8K>%%6tg66(srqUcRreQ>5z$7*xb7Jddr-iok_^me=g@@!|qQk(a6+P~7%a2{}*Mb?>!7XD(2nE1dvz-tCo#qR({y9nnA2=@tVw`z=nKoiH;j7?J7Dgfg%1k{;u%^wNfeMf-&T>JD>7`84`1_9iDRoa}hU_gZshnnaT?+*^(&`moctgp<B4WxjAf!^%fDmJ{9F(stQ2p2ABCm4;%6@TX=Y}=P_t7VRgs+gjxaGSGtW!-<q>Jo%)!8eucX$7NG`Yf_QE0qI)L!$BO=}Vpt#-PAhofY>+8I`?SNp4t7@3-6-7?876iFLnt1Dct&rxr;(uPE5SJsnlo_}Bl(?pKDDcktEPBjF^vpbiQ6}Y}jq<Tp6iti|JX%-EnjhQl?Aw_9VWbVO&qFcfLHQx`TcVSfe#X4nu|4Gy>qodvX;WX+2LP2;=vl7O>+d4?9KG-252{$u6cGInwe<*eo!1}unnA8mDQzOLoQPyVyv5AMx%!L$6w|u%SeO4CWFqGk?rK+m(T00F{{{&S}65*15A$sAmb0SGLi0&B6JLFtB!3<0{-^)>_6$FtEKE*KT(=fhj(AV#^<5L3>0(hku4N?vx@TS8AtQnth!1FPOyZr<J`YQ&J^c3jgX>6DS2yz!B{umdEdLGKzj$^z#%`Z%j(X=zQ+%@HVf4Pwy3;131c19oN5u&I3^99D>cC-cH1<4DrwhWrSj7PRXGDS!bCi`*)3DxOf*sNoKOGm<ivO3voRy>N+=xRKGD2aET<#Y|s^D`|S4M^X{NSe9u)3n;wN5KPLe-I~yy#yK4wA45X#w{+oExmy|dm$NB+%eUy#x}_S9iFl!LFJrp{^!u<n~T(k+*^@pgOx`dYkmxC>gitn0&*svCzJ(>11_{dlP>qiT$U~(^caZ(3NO$UQ7V#64H(1WJqJOrvg<}VI$EoS>sis5GnRk(Xd?c0zp#}rZv#t+%gf2v8~q!#xF-2QTxthxz)R8;7=b8T4eHnnvCOp0ub^1dHD&21^ik*eUwq*Zo9SI+qU1`R&(X3q2I*^-S-X3hPsZE^5{A)O4sas(@9GgQpnUx{H|Zr@pMVw~65pX}syUEIexql$4sJd&IwP?gHpk#P8N1zN<-M)}-h>WVYRcpA8FxaFx+!tt5X7umB)1WGTKnK(yepiNSkmd|DXVz18{~`CQ=1D~F<03b%Oaj<P)p8L^C<i`m`pI5`-}95z4CGpz6(3Uc*t}*KfIrHS~olL>*C<g(Ht#=&UNEjk%tSv!K8Xmv=@>TJ;=<>`uB97>g?;R1{UGOUnyi3DtPi=XH?oUSt-|_r5P!A1{I9bm6_8VHy9m(zpu(y;w{PKmZDv`t4xdES$GPNUyrYacFSz=cC(#jTKK;X3Dh6h@hm1DH>o_CYcP*L2`MmbO98v+kj9u*rcr-0t5C$BBH>Gxgxl+y-p7KiekFt5N#=~eb@_Ui92d<<F*TG^%3i|v9;Fc|X2cdkbmRlhJ#pYJOo)}?`@w9&OYU{xO#4vjVbURJx$|C$9%R+0T`^U7dV0bag8(13BC5#OoEPe1?)Q$o8}M@ab`h*0(@prC&<xZfj>&AL+YM7jY%{5q3tZdJ80FbgJI#1KGgX<>cWn@7@vM@R6G8@3T}tsY=j=Z>Yh^pRW*a%*23NwxLuWF`C;bf->7;lA!wI;Cf9pBh$w@P!W3^It1>FedsFzBmtd&}r`8L~FF^<EaVWR&;)I8YvrexT#6>&4vXPm&y4#`)axxZtqHpv1p2+><BC9JQO0@%qUkv+F~IVVm)sn72V6lTqShFa^HmmBNyAvf#jMC#mk5Kvl!XE3Mp9#mc%IEWv<?pVf20Ddb#Gao}7-PAi{5lL)ep5kjg7cej*;aqTYV<nrq@Tz`mK>hFMA&@~IbXXn5V`?4qSOqM$N(A?m+2cuuUb+$0@g(q7J_<jgN8CD(MzlxI3eD+(I5xdLaTCU&Zxa-NJ<9=`$ODINYHn!97*Lm<UJ%jH6(={wbxg)t4W02#0cR?Exno+uYIZtCxx<1$d-kDg;!!XHXE&Z=3!8Wu)Dc_F(_nLoR=GPR3M<Mu<&2U?f%_Qr_!^buPxh-Om0JO6!59xCCKj{!>U{1QDrsn<cji{-hNR7+&tU?lL<pGk&+vTeG1%4KI0__=mWehfG6eoHu)UBC<%y2e<;zN}b|(g7TApW_C>7a7S<|M-vzOZ)=DDa8Z*s6PZ<n=4+QU|LUyt%JKdcs$qDq}gD8cEq&$C@5q}fa+hUYMemB6*LME+8xGr7D8l92_dS(c)RwN1#-$&q5&gHHWh+W+&gKYLGgIow=)!=q1!q1>|iHD>Hsb3*mjBr0KH!&Ly%s38!6y*o`YVQwLFoZp?L(72Vk_$d5><;k>O3)hSmWV4b+GTAqbfSH%kZW=K05h$mb)<a_uk8l<S6YacAc7s8U)G<%(Gj27rZqv;Fm`X3prjV0V-|cDmN=SHPvh<i5_kjO5qN(LxYnV=CC?$xMr#2YqKiv2)G&WfLIZUu5<`Z6b1AA;WV8EuRG$Lt`?9nd8fdUw>N?&S<Y%sF1uU*Jv{D6=dBV4LEjO%JEcs?gLGbpKTE-6kYcdpi&*O+BKEhZ?r0Rp!Z*)NYd>`s+h;tkm;s<7Y?dy|#juMXo~C82=GLF=gC2MKwMjPHRJWuE`!2EaYXTxR{?GW@cse2K!2Eb-f5X@w7vW%$h;a3n@>^St?*ZnPE2d-I2%_2zFfTO?AbD=$Jbf)v{AGrHeouEGY3*S*b6KwV+pk_35Xky#QJMF$C<7sOF%Qg$wYTtVm4yiKkUQ1(K~JR+stNihP^R%|M1rAmb`BPi=xnc_GY;M%7WavcJ|&<ZjGlbWR3rZaDQJ>ORKo}eGXvWe1GpC@}C`!s@N?t=^$W<y?Rc%NHQTLz0Wv~KWq;OYu4z;8=&n)}j$?Zf;SDZ0@~&^T%pIAw88WG#?KT4f`JDJ~Ka`ZG~2^;~;HO5D~cQ-Nvl@TAaX-zB9UP`w2Q2v|3hG}XN_B4@kHrhSlJ&3t6W7?xtuN%KiztB$PLVz7wDSh`qGWr1Vf#73O+ElFc;bnlki^r~VQ1%(t?82Cqn7qc`-Y=FTmkSoN%`kOUJ7m2)fq}wyBsgV?{;&1<mRPM&SR@?a^eKMqBUKOFUoaJ(>_0Lc}Lw?_V@;w<nEVsQIaf{;$UpAC>2KhaGpf}{6)mV;0G)QvEUU((kCf49?L+Z|<D?w^Tgc`Hv#b-o!4zXnD!rz9LyVkuxm8+4(F|4zRRI~NAP3Pn!uT%kTO=B7c%BD=`$3WMPN-8J(rt}Afagp2u%TOy3upI7FLoZ4{#Lx~rAdkMJ7|(a)R7Z+ES%$5WE5@mIZsLH0=!<E{37_*A2Uk7l#lBe<h2dkTo*)$CQ&TsNoy;S=SwtZO<649cI(|^S$t`wyk+x7iRVa>8`cObqQRFf$@jNxM<rVN6=n9ld1^ETz(Y9tkeO$P^Qm#X436Pgn1#R$$EYQrQM{^ms*P!{$)BJPlON$nRFX2b>ni5s}Hme_>3mn+~M!Qz@Ip@jeuHw99Y1fI;S$E+{!+D{nsX&q5S8!(`0EccKLtMITj(iWP*n|9O5Fml!-wUOw6u03hk>?pp8aW=r+}vUx1@EXmE~>Iz$%l@Ss?rmBM)QVThHB{46k8<Kcj=JI-dvi477LyG)J;E$x_8_Y>x-+EqwYCs$8;vUtO0A6jTCdphl7)!mJ94m$1DXRU>qQAn5660jpRj){aaFyrS9guz9?z;Zm{L`q{F>n;LLl>cOPp*5fO5?&LAPXdg&`Q@3r15CiVm9S}ih@QgFE)YrEWB#uC6x+Mzr|P#=lTmXjO2JjKi4pL&g)=;x>HuM;g}or&e*o-W@`ynPI8c8RH3YgbM)!nzXWtRMTo*pvdin}%4wOE5})v;#hN8t>)aT~)Ejrym~zC3{+`VlPh9DL{C`)XR#Qo(ph%M{R(Kt~c&n(@r3G6qOBBGr}hgy&8^c#?tWQ!?W}l5_$yVi8?=3sM_hKw7IJTZ&__FB8FTNJLNm**3m;Kj&<r2C*=+d1*3gbn-Z>WHs2PXc+L{6HA!Y@(>k~t^0|1DZ3;!1XklSQL1VIBGDBjlq~lMHHSe*UGYzfRwYfdg#;IB;S?>kvrg)WN;>P4bOzsicwasP^ESE0I_{a=!2riJs(ou?Yn?s5zxak;k#Whh@Z@=G!Gs9oVN->_Q$V=MV^&IeE8{7&dHZE;q03+X#{OsRLpuY2Np8v&%+FV}UZ+)gt?}{qO;pepDXf6PX{*_TTUv$5gMh3!)FrVnGe@4aYZkG~8XVsLX6uydvNple6!Z)4Pdb1SC)ZaI$BS!(4fR-z)liz_h0zeCu3~)Foj)}@*Czz9}@MO{jZTEeu17=@>e1}iNyxr^x;w_bZn!tfEvRJZ5F~0WOV7rzSZBXoVgBHH6J%Q1V1>f%}@rsX@KtSn5J}po>+|B?{)d*=;90n|%BxK9x$9$lx`MU7!|FvoH_=QECevDXj8Ei`-Wnv*kId3reLjH2Q9=6r_$!Q-?#ht7r(!H$F^Bfl*5^s0eAyXP)!ma=UC|^4ZT1S6#Hy<)Y^=JwfjVTHeZxjxH?=0KA8#!)ME3mloOGrh4e1(ACIx<33f+2fSZOLmDcf0HuZ5rnHzx$s*o-AskM06UT<72Wc4aKAF+a`5>YBx^IbgTrkSHYIeZGn8_)i$<$$0$39H!0oV_57W&Ipd>Gde!}%;8~q3f@Pn50|S{hdNQ1fq+F^kjp<pV?#sSZ%nI!nR?Q;dJi1Bl&M9*CyJfe%91Kvpnk5f1ntZSQQO@(kcl2H{D)fQp^&)&L8~nVP4|!tVOGOt*4Se6qCdw4x5H%-aw7>xY-%>^lFi<c1{wi?gd%hwh_rP&mZ!hsQ8Ty!B0&%?!MX{hU59I~_BFrE%Re-nLk8q}$XPCxRvF=!u(ZwZ;43wo_?lgoO*Wrzyw;G^5F$j&MLyc_-<lSm@UEx8lx3!nc9c0O|)p$8J@6b_vOz-ZVO5DhD&XFR?kfo2?75w70X~JjtF_M9jjZZOjF0mP%C+2a{_d=#qA~Taa12wg25?Zp-j?6Za8#3JbM2~ExF7T-Pm}l1-lx95ix%9NVgrV(4Ulbea=xb?^JH&*`a&Nmr9}osURo0k^9mjrC(V*erxVtaQ?C(c04H`n==ljClOyEf8p63}2-Gp~AECnGNQ3O%+${>+p`_69xqJNBkEjN;}(1Z$}J$)`7SG^Z^b?ORz8#G>Jb^y%9nuFpf7E{~&P)*~2EMdE1q;?^0TZjF{EHlOcQRCLWJBpegY|J65vyQ`yxewSpp1}FzfqFp?KFe*L8#9h(hT~~CE=6E4takQ-eVn;7C;}a){{vZ#JT_1B#cQMQ*aDLBUpZ)9h3+q;p559|XXNP^McHC;2+Uj~Q0XPE-=6pwL_%a-Z72>AUZ950&^w$9`H+XHxceZYE6@a1LPgdlt?_z|G(I?L9XEeR?0O#nm!Ovk@IM+zD4N?CWq&<`MU^_+!8}m<rxI158BMAkpND68p<V-c2wCDf4V{`E5mAm3I#97rWe@zuxz?kcx;V9aSPnX20H(OubC^cbRnz1*4Pf81#3;!zZXcCe<uQIk@B<kal2ih2YYg$=hb)=1{T%u75)6Y;19tU8(DDF0L2c-KMhVmEpDFZ`geS7Y_vXC)zBRbpVvvx3UOb8>=cDz8Tm#K%>mz3d(XeljMDV9Bh!^rVyg4A7;bn{&qo#;MeUoSG)O;)G9WzlP2*#t?KrzkAg^A(Ya?WqCbty}5Znl4vr8IS9=Fz50rORs2)(Bj?3tS=BWUevr@(`3t!C?_@8%ui(ceX{yJ}j$6$U>8h5=YFkrCtjCiGGqr{d-D9ZT1MPvkbwRC1rR*r*;P{*i(G(Ll5V3Hg`Y2^*vwdQcRw82@POSYjD+_q`r%x&R8PR?J#>@qSf2&7IS&mZ$56&zrKCUbfk2kYlRN<XR(2<4OAE07*1UmTlzl}mB;FURR=GbQkPd*)wdWVs?E{zMliAe!1hEmM*QOOVfd@;bpNHgcMsDK<fzT$qeL$`+t2HFER>2Dn05k5cz#rftRJ<FpftR_lHC<c^SJ`|+tN#6jxz?L6JD@<$im!~G>YKU^f^Tdd0`$YW9R%L^*QeXl5y$~(HLFH>2ntwjLR_$G)27b*jj;^#*E$t?EJ^y<)ZP?a4q4`F4PQqD>7D`Jhmb<CGJbEXpl`}*Z2MT(Es-1Z@>KZBYgPz;P2ao>*f8|AAb*@N469`{YT^W^_#)Q9&5g;&^V$;nSnhY-OCFH-ynpg(*~D34}7JJO=#B^?!xOUzPaQNan0fv<h9SfFzwn``JURkaFKui^~3P5Up>r1#KnV0zwA;D^H$-rV||{v(Fx)9&~S4`YbNV@MLYFe(EIlv9~B-zT4o=X(G^Gg<Ilbcg5+3}B6d~`_u64PEHZfbw}1Zi*FXK&?|=EXe}*R_4(xHw;*Xt%t|`2m74Bh~T`TZ))#G2pTv1jhR=8(r5@TpsM!{H5qkn9_C#DkDwD}IWQ;IkT<jxq|_L)3+dIfOEcl`Ms){`zjP0yO&C~tZrPn%}26`t3mA(4#B$lCyo4oPd2ybEwx=bmhna*I8@)U}W}G$e!Y2B3pvH3YNPTJ(G4xm;h&%fWO2U8v*lzNjygLusl{d`rxivo*Jayem4aBCqQh!v0_W{@1_#^6Oz9AE*01mch?{;gGVm#C^OgX_w^bA@t_zCs^?gVA+O-kB+Hi)!eCqB}Q|KhA#7^XzV-O7dxxP2L$~Xi!2B(yPs@(CLX?c178kI>n7G6z++UqpChJp>-o?U+Nz<UH#2o6C>}31XJ^*F`re=G)exCcx*Y7+CLJIV{aF{7I*-~m+1N-()WqucDDdrEO63cazKzB?;0VI(&E1p>%$I}<Rw@GAp<ynvrq8~`4O6}i`wLng$OW^CA<hEr!}pg+>76?M>{v;)#C4s2QaNwfjV?nh)|ab6LXmZr7OCbJGP7`*nC>&=^ua_T#0bB@5m<<%;F>a`Uq1wG5fec3M%ZRg$25~Okv*7#NBxh#yubg)*Aud@t~i2?)GWA%B~1}9@na76K3>dN?r|x6DgdrQ($sj$^-%l7=?Sc?<ZjcqKKGL$j~aWq=uxMzIJ>Llj|q$o+subU<&PA4d^8R3NUiR`c<Y7M0F1GfjK?XT>@bhFv0h~c=|svkkem}kYcXHeNer9DJOE$M{A$MEb_{1$jyqT&a89L72DU5u1dk_yWK8pwUDQ;lb)~YPMdax*Ac-H8ixrKWP+m>Cp6ka{W+j2KB<*|z7MZ7CKSf>sI1}^?Z*H-Uzo1<fw(&~9=yol}5Q6pz2R4vfG=M5VQOwQQo!c)VJhb(m1CI>?@VJT%;D&NEkRm#`Js3(APak6lx>RUJ%_@@xsBE7jMlgo{%@tw^+heGcTa)`BGJ-Pjjw1$8PAlC#4zr&=jP~f6Fd$sI1s@fp%;5o-m-9fVyi-JkfDz|kfW?d>JchD<U)5*)-gLv*@UVbN22rpSRiGF=G7`o3P_|L4hrSrc8;t8y4nPF*v*l?`af%n98t3yc+V!u@$IE?{2#S6gVe%OEWJ}6lY%8tP_(&gH;PV)*Y!hXgwW@}f$LlXG^jmgajydf;-Q)2wW{C<G^L~zE8hS<%eR1I3v=VaQk56t_5hv-E8|<mX_v+1_J31AB9yIY-@V+xwd+H$6W_O5!WtdCdIE2%^uh|$x8L$haHJ)-$*K=T7Stt%1e&zL1>CVJYnfBL8G0aI~4QQW#eI8sy%7-KGq5ti=W4Ht5VN?J7<HtYVpMZbZ1vwwRd35Je%!^YWYVi@bdCwnwV@{`fp8hB11#H2)%KOZv79Xyh(bHf_0MTHuYXx6jVV%@zsVq$dMro&bxcmy08e=g+&ci$|*vCIQ5Y~h*I($mZ0sR2|C9p7SLAZ`zH)btAi@cl5VE8y;=(#A&oB9EEVL7iQTY=$xz?XU<JTZ@-wp(JGKHT6hR)f#=VG~;ck?1kg)vk<-)>}uc0ysF)%l6B#=kZ%_c2)}rt3-!^Pb+%d;g%n}-mj`Mu7iu+iMT<KIbu5@P^rxqCg^9Buyt@=UP*lst-@%+SAho+Mj}CnPCZGmb+M6j$Q5U~AVn%vCiwh)$NrSMr!qs9V?|E0yZXsW+7!;<6)dmK`PRx1n8#Jv1RR>yt4M0?>v56SxoJFlac1X+-4*EJ5x#<Z8_5*|!C6z^$nm&Tg#PV?y}SGGqsdCAKq+}GsAJQb#6+uQE_$L+vR&;=+)N^7*4D2oLL=?eB*B|W0prmDCaKl;B8FkRl{O?gyArN!>mvX&m?m=EP1(lRb)z9FgWWlVl@=V1jqlQ++gV=m9R)7UqJgwA(|9w~8|{hAJq-}(R`7q#_rqw|8<jw?PFdf75+ZtZRB%6>W^@1?hUYXZVeGpt{-o-I9de9tGt*-?H6XK(vfvYN_dSe%9TAnxVCgel06U;;8Lj?Q%+_>UZH@aF{jz5u?uI_G)9r2}4P)fW;&hP7%Tlw`&G!m?EDIZMPsj2!jISEN^?U8!)Zm0-$O59Ld|&Vz2osj3KhJxTk2&0Jli5~r1s8^=R~JuX!zL41q*9?e!H*@|4650IW4t?!$0rNh>Si{%E7!iCu1#zJIkcM+Mc?sFe}uHDI6#5SxgBi*s6gUq*1Jd3eeuXP$e#$I!R&;tn4#aglijICR>lj^^M;AaniY@YG`a#DAgbW)$vK6O^ZZOpN0;iik;0}9#I)MhN0rlGe-I~yRb<T@5TQu8EV&@G^ak#|3Ps0Mx0=Q;13-96nFPghzWJX+o0a0rSH2Ndq9gkfD<?SC{212MLvip0d`vt~sLkZzs4H*&$zyuVW$B`)kNqlu))BBMl!{7I172_#=~2s)u<J(pHd?EOZd>uovt~8<Xd-5PzYvr!Z&SvP%gb5u8*L)BxF$nRTxzE}&r7%zNWgkn2&DI*l{}Yneg*ZJt|?2`ppQDw|Ke-9*cAL4LnO5~qZI9U4tQ%!)YrT-mXtIjOPYllkfE_9;Ee9yMJ>_SrPhP|y#sRV&)Kv9i}*5CleK|r_#1t-btp3nM4z9-dssC!D##kd;@366o6rI5OnZ1gBT=X+I3-RU0%<ji<n|j*YahT0I>v0MJlSL<vEt2cup`ky0x6_ie2h8I##k2dV1sIGE^<f#w7NroYM2e{B)Yv?fDix+d#i+){oxLAiq&b|>{zgXiDf19420%7cCDDmg-K>o-5c63NopKq=IY^3Ys%Aos*{?qZu$t({Yo>laKck>J0sVY5>bT*EEVa|8W2!9)dfGsD`9CQ;*-~#*63pXfF71(ylVx6@3&AAt>v`CJzB=Q${zXMg@5|%pTPyR5O3Klvfb<efENF+LjpAwcAbjJ)J^J~3K5{6ktE!f0)7$tGSnmC`9c28tm+bfiUha!By+fTYQj$qL!q*Y@SR5q1&X#XoQTFfi&w_Mg)nVg280KL4-d9%RY@|H`%vlr(V=I#XI)9+WOb<Br%_@Qmcj>v&=|EM{pG%fKF-Ux0nepx&%lZ?4V};Q)_e|qE8Sd7AxAcfa@hx!g{%G{pGf#@PIEi$ipz&2jSxDHihzorIp_Mh5i8rJ!|9xFgG-s_;Sm|gk^Y8?T3ag1w<bzJ^EuneNeiMQvr;|*-TLGR!^*R`Qd=?KW*gkakrXtn^G$orUz=}A6V@h~gdaS;VrEig#(6)-YSRjk>mOs!QiAzv7gC<r@KDY-&iQGlD!<Pyo^ML;0XCDf6j`jShg_<zsxJl?Mv%o@Lwa^j=RK%AbSh{M&yVh5`dm2hTQfeec^KVPIpfVpY+;^~`yjIL$H0sPalt)}wP@;#s|u_EZoi+0V6|B)dCihRDOj74M%v7SO5FAo%Hv6f-n9{p@c`#43Wy)kBm9|1BW$B*g=XA9{Fz>#xC!IXw+RYgp5<&!?0`eCG&e+B3~Kvf5lC~m8$3~j?VmX&qojss3`@Y7%3kgm-&^fH$0&E0z;Dk!bWIG9I(ByBDYnpsmq8to)I3Rc=?a6-<y#U*6~*~-I>)0ReGGbhjXd!u`&E<5i2y!|2n0mjBWAJG`CLx!43$?qGl_FUOJ)(qFj;D%J<b_dctZ6U>}qcug#t&*L|gJ0hW;4XUPx>5v_|UkWhGI&mx5(%=2<2<MOIMOpec6j<%Wg1q3@F5Hj{OXdAqD3&>ps`%6cS+`C+xV1K%B?5XWnuXS*auGnGu@)Zxx5!DDBM-KBz-a(NRhA`4KnEJYD5i!UfUQY?GWscKGB`VafFmG6O302dLKq-NB0|Hl#9duqYK@?Z<aD9vMGfT9!<Z0MYjvo(oUCBI>+vZ<<9?rM}O6Hi*D`Q2X%tz%h;g2G2w7EO5|r7#hkY&x|!jHa2F(QZ;Ou?r{zo0ef?$^l^@I8$tb@|>5+ZgHs5Fy^HR#)f95TwwWW>E*=~s>kZPJuPPmZEj5V9#i8U{QpKYxZG<k+lgAT1kLi)3~M_$&N(i*&IA>HOmHipYod2zV4bZN5ZIQLMpO-QK3b|cPyicN=~qo^4MwJ#eQdceSGx`{C%v0x`eVprUyl`oe=-<~7opaC^i}!jMw++ai;z4902Mh<qQ^v5TjcvWF`mJO?Wc-hvzTMP)*_B9Yi{vo$&=)Qx0>?Bx;qF5iOgizp~4wNZ2i-jg8ts;eC{fN2_zv}x6ua`Gqw*_(0l%q+d1-CyEY7mZc1UJ05vNSG#F#yZDq9}vsw^IFkF9e3qI9pP&V3R=6P4c&+@LeiXIvAG*%8*U}QM7k85<l$(*tc!W??r)`0TFyd|ZS%>J@;J&Mc{oHOuI()9gYz(a$cwt1Uek)-TBlo@AAv6P}oqOI6edQ%mZVeVK~J|i4B9pK`;bWac2<&Cz)F|oz<*s!IQn-F~QnA+MW4s)F&bKY>)(`4AG_Lj}tUQaq#-9YG2v6Q-rECr0e^R75X1cVtB<#Os+=vS3m<KYy>KD{fM6(oBA^Mo&uQOphEp8{SD-KJ!Zs8Wc@=SBR)ed$2$V(yw0x9lV{9p#n8kR20Q3q+_^L0EMH6q!GDqVk-HqPyTaGAb)lr2hr>&O?gBn0%LXmk-CiT6HoBfZde;%&Qr@q|X3_hb*RHY<_76326r_MLU1YXSoeF52?=Tt0PE7kF9|1^HgoRECc5{y{djk;a&wk6u%mJjC`gU=A}e)GKX9G&HA~E?5W^%85~7!q|2+w`l~f=BF?)p-_`asNsk+$v{0~<EX%*#YTa;Dvy<BapD<HKfy-_0#@OTd(3i%geSS2<o0X3tj%R858=^DM_<mz)rf89MdmYRAF7%09T8d`(%vDZP77}<M7Qw!btil9bn<QVjXl3|9+X4+C81{ye<R1fFJ4*VT*q*X{7<X1uRxCrUUcyq`Pk}8;VZ`h(u*;7IznBv!rJQ5f_EeTmt4GVQRg&vC@5GxkfQRNQvlu4wa~|X1N>RPoT+YHEd=N_=!CzVH+(3?FC*=<B!&2bexE7%~H95LuDr+}f67-=;>5BZ^@hDK|OO|s&ccl)9<TD_buL>sM4_Pp$OIPqRZm%_i#CPr|)Tx%HQHb*08;GC0Hbns*W)<agfde1pXxE%R=REoBW}MkB?Q=5GE>1u3G32R0tKV0q{~$lk!M4W`mu{OQp9v}uQeqEFov!I#C~>7|4@d1i&!kbF;3S8)Oq*Lqq-Z9!>z<TPPWObzu4+N7Ov0LG<15Cs-5f%}bI^08;G>x<Z4x}5XEyt9PRFk4ds4TRyET2Gt@3)E;@p@<d$PeuH03t3*&*Kx?n{~uFJ-ryX%rOsynZ5!p~1|gJVq%+RbY4^ZMdYk*VGNA(tFM%&Mm^-2m4S+hMeXZ8f3RGectB1)+Wf5r2rGK#k-?Q2Tic{Iq>D?lIsA{+YXs40y{}W-JA^Fb2GrQ4E~+g_=bM!<Nm_OGS*3hE`IIO`tZZ|gfq+Ra-Op;#GDa_HPFggKlXpI*)MqG6tVJ`D3<)Fio6U=-*irEwV5$u7Tw0p+bzsVK?)q^dv{sG;%9$+2-MQO@=NYB<Zn{b{X)3>)N*6C^g@eCmJQctf+ty*y#lI+uN&AU?4ZO%K6f<oQ8yhvf>KqzRcb@T{N)pnIuuPi5M2Dn;E>xA@6P$DLV=J{mYI#R19kxOtF_uBXbe~-_S28J!2MEPrJz}AS*Jb;WA2<%<eb7cm2%#zPk70yX0}GE5Y!=bp2v8l7w{zg7OGkC!GTYyincvbf+@w1Qv1A0<T5$!yo-9yRQU+SLsdAt?WuxxgPg~Efjcf<qL{TaiCCq02HCL9CNdRS9?~A~0y+soGC8%!BqS7&Dh=4=c1#?y1*G)=8P+r>biWDLjz6;%lmqw*BrwP%FFXv(eXwnGg>@g7iZLS7+@t)GG}<_nF^ZP!Spn6d^CZiEjI;!-JPptJUwlu^qhVcu&r^NYOYe%2%~>To2gH?<(Z4#U{i>9>+?Urx{T!N(DmE4zleM1Ad3phVMpgQ5m-}VBkF$4Qh5e)vFipI0#gp-+#z<H@J62?q`k)lN3&<M7I{DqEBS2^2k1$d@m>j)JK*GnnXp8*FOWK0dBvo@PC&kVeuW3?d)4>}kJFtNdX(ZER_i?ln+hDu%6#rA~VTJEdTj>R(9SiO^3Y@WLmk^c7MLz9~DKv7rdRu2uu1fc`3I!uc>na!Wlbau|1A2q&KDGbXmZ#zumfFTKVgVc6mO>)T!cB9kdGdw)<#N-O6sob+MJ{N|SjEw=mAGjCMNb}MyUS**(f|{h6%hLRa)Z#k`etVHQGisPtY8wEjBM3P?wtkIccW@!3dGvUw3#K-0PA0VE*()hs^gQr$+7#lcEH=fJPoaX|NZ~@<H?pba&xDVIX;%`D0<b9-=S`m6mv`Wm(6Ib#Nb!WuFdV9edBd)wjIYPJJ^^hhwJq`ohb#D)kwG-zT@fI`!H0mCzY8_g=yjztHJ3lIfK-3*_Vp>pe^XCAqt#RSL3;Jif_qk9#glS84L-$TBROp!xY;5tu=`KUa>y(W#?r+e0|SP>OPMh%VcGk0L&|U%(>2}ZOS)^$|13C;K+b)DQgGx3zmI<6-)L#Unz+cK|!<LULtcd#D%@g<9Zv4+H+%`6%cf|F!fk(grD7M=E<s&%bKpY(QPph$t>cx<Z3dbi?z#^2~J5h)Ij)CEXwklfo^r`&MdAC`2^tOC4vhD_7I|9@1_pdTdg-JvB!-bQ;h%*Buw3eVi_;g1Oe-9?bT=jbq-w~`Wfkx=z9WHrS*1q4Fzr-JZD?JUTjanaolVGE=e8AmQ#Qk?9;|Q&(p(r?S<U71i2@d?eN_SWrwnavAQ?Itxw|6*5w3F*oTdd??Y7awx3b0$j}$F(LO)c!Q?h8vN0C`6Xd!vJ=0eMt3@sQR9W_znUA~_z%y{3;#bbrq$WB0`&3MLhjhvFh2wDrh@7s#tJ+E&@$v1P^HLD76BRP05dd;sPY>QJJG-5;S<9`!EJUTUsZXDaXS&sE;u31&SQeV=Xa<8B5HKq+n;NY8O(=ndiEe%<uQ7a<Y%ZtJ)6!<g!1ovH5E#ElO(fLGb;>V$l887Mz}E5BQG!51FjbouG2WDWl^mpTcroh-DNvH$vN$;-6k%rJsj(Z(@jP?mXlD7I2If++qPND&;IWVUE+WcTjMM-5Jm010vNk%|ErhRI+P9j}8y7RNs0g<#s+*Z%3MCYFuIBdoQ+f?U6vL%`IN7g{cSq_EE|=L1_!#-!N7P+WSFoxt@{TE9A!ZdO#S6j%mmHK(gD)L}89L>QVt)h5g+O6f6?VI6j?;upU9|K))GD3u21f7k6=}TDT+U=D0|8cJmbm~gdi3|Xa5KcSuaYB)w*shajY*}c)0Ah5eA@b$rGXpmcLR2*V~3-^tDwhAT`~Sq;l`<~SF|||rw~(FEx~BnB=STR7~fLpoATW$_3xZPJuTj^vwWi28E`s?*w2HY+JvlZk=x^#(EYV`nEF>8^46j&4+!;4kdF{}FbDc%Z90EHN*O12>haY!$~#$=emu8OH}LsJzS8lOGyEHY#O)R<cGqt{%<sRxeav*E^qp&kzVm0Xcdku`pXJ4CI{vjl`>&x}<BeXThVC-%$(Z0`;eu%W9GKg9RF-3LFMjd(F#J_o!U!3fF|1KwIc<(CIpPo3^LEQ*!&j+l!$|l^X!ubfYJMbjf(hMTiFdhh^kK^Gx22b&8#Ba+&SXK)AoD6)at+XFI&ztJSwCeC6{FDnqHH<u0@4YRoC+h%cbG81V~W=Y=@<r@B3^f#)dVw*QSJrl_{ZOM=X##|B}|vYeZv~T6&WjDE?W`McU9=`XwDB0lHqH-@6U(+w;zA|<+mT<!_NnQ-!2Z@`>#L#9zKt3Df9^ru#d31$C^v(vxr?{2KMX&xcDXT4MKnnZE&pz1Fe*?3GLd#U3h)PH@8DPu37woy!P1_)w@2`Oxy3jei;AttA|<0mKcfC@9;H;d8_c2vF@(i=!BSkXt*+?HIrnXMLYHE=>GeUj|xj2_Dl}DJS?NDzV*kSeG?4DF;7eEtQhXKuWVRkRPk^B{OhlO`mf*r@^AkPPedHp<C?`EI}Kfv=r<*lhh=uHz}Hoee-X3!SoooE&(d_x(6D}jv7Sc%*nUqeB(7=m9dM@<y9U55F}mwBjr8;i2wB<-pV83pIKp2?51-#JYq}>-yXf}`4-GG1Tvy&EWHeA&qn!9TT<4xFobr>y&lvTDp&^KaR|1_ZtB;WN=%L>m@5y@qKKdR|!pZW~!}_9fOtALdZ+^?AmeVP>gS;ye9UFQ61dP4p0e<=WU;p;YuZO*SobLNrhQRsN9!ld7_wlZJOp>>V@Q<sXV89wsOdsy5i9`l`FE$$_bBcy8bFOGGJlq#M&BX@<9UBYq4wv1}zCClvUfhE(kEZn->mK1TDoMR$_BiE3OW1mbh9-%cTJ)!B$BeS})%X5fuZ9qbvSwgMH$eqQ;7naQ>O5+jUm}25e?;wZO_G1hQYz<|V0IhlfP-tYH+NG$F<%l+`A8%pj=#Rwr_a8{4O6}i`wL<l$OW^iBhCWt!}phtHDX}cU)8zz-g@64c{*r^r*OxreYeMuR*}}Ass}-5>52Q+BtK&H>@m%Ctig@^$6wyx|3iuiK5oig)Ey$y5CGF2OaA%CiSyAG_U#nO?gtYEnF|S}juUH-CUfx~$cjJaFy3zdLmSh1-~eW1x-TTp9%CKc#&RpE_aHxitYiCW^Z7kSS0J4)ytH|A>jq0>(>fd@k>?B^91X#W6eSmdA2r@oC>+7Y0>Fa*nN$+}WaBtUf0|%Qn}tQJxnc{lbpF_sYZ0z7lic+WTtaj_HkHwM#L#ag+`%B7=hTLd!Az<g;0hKq6TwDyjAIcG8C~ie<>+>efX8)g%Be3Uz{c-&!N#T?5hQhp+LrLZ7-L5ylZl4E^<})u)EHadq6dOJ8;5hE*c*^|2VF1mXr}_1+k#;u5is^`4#YUwnz)w;lcucvDyZpRKF*HRcwzc_DxH}(ufDX<Z`pM@=Ct?pokTON{Y?^kj?>UHis)T}^mZ#o0si>pV$V78q1<3k3bt1%?%dI-Q1hZiI;}%Xyz^r$9o&Ojs+Z@W9EW7O_chCauofa@TjMGBbUg>Qm4!jT;m<NptxF3Ps1o04+F#2`Reas}*XO}4&RMeb`ri_&GF+AW^N%0@c$evv^U<3}cP^aWhJOVS>>e5^$+2W_%yQ0a`k$B=p=e7ZvAG0)=G?<QJvam`1_rxUuxAxgmh5Zrb`yZ*G0M%ws&S%fD$~GXguFLzT(FOSpflHmq%C|(%mMuX{Uwkh)2e14ziyn<W-E0!m%;FH!q9VC?KkxU?85dCWgN)b^8sHBk}6tSeEj35?KWkvjo>e4`Oo!X6I(&w&@oeK4j7Rc>U(7@zQDnWUUph&OOIcp158kOh=V#h418MA;|{m{*mX%jox9nMCNL>uMhFGKS+kuG0G;Lwv;H|s1Rppr24b9fe3_n0G~uh@XA?#u0m>vTuGO?y)6>de2FN*Q*&*e23VxK|ckEB8dnz+zZ)r*8G`s6sD6o-+x%k2x?7_m-QyGv9r~$2R151qQb1G0vl5JnljlAHLoUA<8a|;_m)##-^0$NDj*OIaXrGTbPl7p2fr^Q>>ZXPrAUrf&70cdbl)u_GZ9h=sqDq49+0T?H`-|5b<^1a$$ZN$jbBxQ-&Nw27H8Cy)@a(#|^yOlO1y1%l*Y%_}j!<eRa+)dfW*H!o+RG!^A1SAtgfQ>iPK>t{#@g0RS&7y%sGLyqFG;-{T%suE(SE1P152Kr5R3d6RiGBY`JQ1U#6!zh??g8dEcuupT#=hIk>#Abdp<JWn$gan3y7iKs#2y1!k@q2#nuK*~<RCuEgzz9*@z9z%ZENY4Pq(Gd$^vADGQ6~SRk5+tZM9`gWAM)2thgKcdQCUUjYwn+SehZ%iv@%5T^Mx~L4@eQQ4DK6-4x_n7L5G+l4k}8YT!brIt}BikIVYKZ_3mFm;jn8#;R0y82A@3J#5BG9FBd=;ch=iZOvQ&I6e7|czGIL1A;3CX-US^qMj<d?0$WA8t!kfVfsqhd1US;bE31{gpUPuF?z?Nzw}5K)byq?O?*4r0xX2&C|J`7O|Hfx+u*DsU<vbNxf(4Wwvv5zr^clt`GIr;>T6a!ij!K(xGKCQ4_Vg=eeL;LPD@97)c3G7GJj`UZR_(w7TJ6dCxr}UYP}E-N?6sn459P}?tSdxk8`@!1kEhLVhUs;n4t^j?=;`sJ_5)L7I{Ee@y4;{$FQcJ-r6siY2sNzKJ_@@LX$S>!GFwU>Eii~Q86GG11%e+65iB6MF0ysi2`l+%}9+$Yt``IDo%Dr=PVyh;3*Y~Z29swpozG=TtuN^j#rCoQZvM*UglTutLb=InhAZ>d0H2rRNZEp)@UdK^S%b2%hp`>uUTe|?rGi_vl{p^%Gt$Q_V4NrF5r9p2DkhLhURspQpo?Z@zs=amt3&v^{j)NcZ?5x?1RnGw@xl}H_2kJYk)VQ1CW|BIDE!*P%U>#+#>`oqsqZ~3-Gk|0mEDgXD$9bC41b)B=Kf9m=~*?_B};PdivApSQb}sIc5YRFo^<xgUJM=xxYw^*sFd5fxECLjE5tqW5GLFr**TVssfgm75X#qoa-XB%<&gygGqIrXfGrwZjhOqb?)gt)k(owtt$eFztXeJ4fmA%&WNw&uu^U{OW{%03@(aGk}20v@V-`%_kQCf(dhyWAX!S~uCf?@Pa&3&ws3Bl4c>0HvrG&8nW{B7#NFtT(;jS6;Rzm^FDa3qk*wO50&3Bri!m!WqyA=={f|FIxkYgXYp)6mJa%#Qs|4&$GG_#?%h$W)xM-Sgb=v$qCGtpMO9108lTzN!m^YiJ&}A`W9X?X+%O3Y$dYhncg_fS;a16(-J`)E*l#0uVE($Q4;5ErUCnnT%oykyXCes;#G6jNCpKytjr=5A4NlzC{%cBBzC$DFwG)PlT=~gL{6fSse1_KaDrp`d==!u%{e(y-Cf<5ayw_pvKWXI<Q&F9d!l7WL6O15?MQ4OT-L4e(qted%7?$p2*<2fYxOaw1Q`PgTNl>N*(*Uybu*)AOs(tI0S9Uu?T%TU7fH&n!-o{9S4mK}4OocuI8AS)&0(7l7m(XenHVGyZhm~XQUFXZ4DnqTlAvs&mg-<0Aewg+x$;|wsF0g;7{{T!>!%Rw%Cbn{D<j;j>_7B8uQ%q`~92{2L4{QDxzSrg_VHU<_RMX*Fj>N~21x@ZzKw^l6P1Lr-cf(TPjkLO1>0e&tV_^kl$ehhJRYc`B{Cb5NiZn*V0z`%@3MZqDD@PaOxa5C)nwYr~&KxPY|qv?qDQtOxpUSP3R1)&G~5Kl7nu8k0t2YFY;G5m-g3D<cvLRWfLXwm=#<>~c_n=lT2o1i)zvf_aW2XPq6=7y<`p{MET1(66{adKl^$7Gz<&>2M;aHg`CJLWj7Zn$HVJB;t!vkzSpkF^sxyDVMj>SiBt(>x6}4Q-X~RYK#U@>fnmdLSc?L65JokN#x8YEn57kWY@-PDI{gR_&e7J>ypmh3?Lz{M_*RS&U08=|zN%Ib{(~#2<rQ?Tw@8?r5242P<ofI0m*CQoB5fk-B_YZQgE=VfmSPmMLA46_j8I%Hs5L56ax|-$_8VN!!P~UDiKq4_g5SJeJV>uv+AsD&;A2OsCgA&vtd0<|UbaqC-AcLOjnBj!nh!<nksESQemWS&AY6I^oYJM~Y<+Iwg~7Q`W=&Y~_1Evv1JBY+Y%|ZK@$Dk0Z4Az$${}!4@j|q_{somLkVMO?0k*!fx0kT46!OEf;IJ9Ec#_oldJTw@{hL@BUKg2FyYf6h6XQaSBv`YepMM@MKdc;2Va1&C6(aqL{!Sl#@-1(=iEw07eG+^1MuT*Gi4YG%rmsIzd`f%4FZqsq_-d3I$d5-JUMOgm*e7dylDc5B`568eHzRF8oA!Rid|fYKC>Ygc~1{_DOrfF~O34Rq##>&^;4^O&4XR5mnQ|5$#eOD8R3)^s8ot2P0GcTPhpKHLMw9z2j{G?z*{Y#jxAvJQf}ZxiTVDQdjhKFXwe~3#1G-E1~P@jLF5V%tA#VMiRT=X^|`qfQ=RE2*J;IOmMZ~htK7J47G1R&=jVZha+n(&dO>97P+3hKQ3&qDcUsB;|Z=qLc5s}s1S=u5L@oke$MBvZaPqsX<cLN0->A3Xlqy*^Z8G187yzU&)UUfts<tpFbdSOQc2UcAiU13CT3PmBEO4U8Ohglqg|h#mpS|_FLRUmRZ(<UIc$URJkiF=(fuZKPB#Yk2oFT1PLbgX&-isqN==!iX5|bNrzR~Gz=uoA8*`!005qS@+vKXSWiO}9$WvCa6m1i2$fnZ2s^|`L>#{N&0pjTZ7w1iUdh#x>InUBjOYG6@_rN$G=5Os&pSsSGxqmn-Y?4Y<n?UDnuP5cJ4kL8ESjj;?Pp7l8kA2#6GQmiO3sa6SP?gNBSUSVb8X9W&rgPOE%?~su_hLIIv2*}{F|$z$fp)T>jtUZ-$oUTJYk`8;sx7M)f+CG=G`G8AX5r#ZQX{>_unla0hc1T|lU<Uu0@-x0Qe|>%y9jwv0of(@3v5Zm{y!siOnXd7Umb~97K2@y=WdK76^nlJrsq-=^LeZ`x=G7zdR1GJV!;ZmJ$|Y582L=o&r6AnX9m~tTLZO4He7I07Y;Eua_LpreU^UvBMiG6^IdH>i?q8D;uVES$w~mrt=1Sv6>+&8@Cj072(;YxZU8<Gj(p*1+VWTFSAL7|9-5k421x+ii?)W_#E4RK{q;1dO`8ch`R*X7pNpITk<b0wj{IS0I#FU`osn(FB3kiz)NPL}q+P_+ral8ux!PI8<-v`FQiFw08K!f(l5w%nPD0}`hKZtDAICt~4yXl}yr9HDhPl+v;!vyTu$21~{Q^pzL_ZHaiI2uh(-v^&5m7ZTxZN^rm1IB8cX2ZgoMT^L%1yH@<KQalz1ZT<LQQ-Sm0jPkE1R3caqML2;{9<76dl(hGz}+5mrP~thOvVFU@2;opF19D>*UjNPUx;=Pm!<=q|H`w9Q+{*es<~BUdHXUCY|OD`#E*9rD@=*l15pzm`MU}%<9eO0tdp_(dJV9ob%+<A9A9pwExURAvt~C$B?Ijf<+&YfH~eA1bqx~>9#rYnV?!c@~1&;1crYvl-5!_%6r;_B<R1?Yc`(;VRMU>6jP@5*pu{1`0I|5s`?VDRphPt46V^AKe<RHhSDLGUHUYR6$_oanoVb!x_8_`=?h7f|LU-zod;YtY>6i4FJBnv!okT;O9d_fbeW}o4|I>E4U=jLno^=8VxFp=^Sr*Oe)?_@uJ&Ze3FpEx-+jao#c#;HIsN(UqNQ)ryw`dznerOo_qIrkN)gsk6JC~^%TxsLz#TGh1f!B@G&)JN%fq`2{u$R`h<-xz{zB0*))|;C&gjxQ-oy9AAj?$bVN(74ZV&vNbc*!>vj13;t)lCIS7UZ{9aw{FPPW8)v*j6>IY??*7MpN|_v(=s;S!*eA5}r6fsQ=iil(iKk+H;bfZeKLcg-hdPH^S#-NiCXo8s{y0LAc%dbKXgV^*6>7O9pSD@7E#nzBT{Hl{p(yzCYHI`jd+E@9s@)+o3SnUA_@DigfL>P1%@BIYk2%GB*@I?&+aKL&@KyLflbPZi3}lqFAc#6H38^NY0FEPD)YCw9*dIKgdFP0DKe$2_M#-FEK6Q-r00$GuBcZN76p>nbY|+S<!PUW{<c9^;jM!IPw9DBZ;;2tKYVA>oO(B(*-j=kQ?-WmHV=2yf+|GyPA(JfeA@YnYWuoX~rL(lB1Mn8q~ufu*=mrHtE1J2A#xkt`#u4K7@mz;Y#*!v&bLN<b==o3UvbnNn?wmNZLXf^FsKT3YTm;UV(Zx`G1%Ux929nPfBa!8Ys_5e-~S$GBi~kMdj7$cs^~GYV*6C1!_+mMs4<(h}<Tv`y!K@x?WdhIIix&-qzVxhpO~XO--P8`sl8|LUCftF-KLUtZHibqHpvz-@3$)_Ugb>3#Vbb^E&wh>&RmoGSf-J|r!gOcaXdQ&B7H3!SQuqqIpuWr{2ZG^1gi{Qlq(;Mb^jmcvPPOjJTPKHf#c>PKGm7i>JKAg+B0@*O_k!0l#F5O1mMq6dzrk)@Lz<k50$gB=4<%v7=87`{wx1s#lbEcomwM#sKhLb@jx`LsZ$M9%5nZk^G-0zl9rAPh*Y%k8t+ESn$o1B#04KDGbXRtMu3mU7H7V$p52Erkr5g)HZ?3FHg;%jKq>7{#qF&q5m)D~^7z7TSvk^Yr)|!A8_6SQ=nLmE()RQT#w<a~~&m^Kp_?Td-gNnG$zu!uQTH^}A8!F~zjY_vekYoIgM8`2lpaAF0$-_SD+Sn<^QiN-4kp{{Q^(WFi|4$kUn}ACur3^p$^oq~2h<zidWhCD^`-$Zc-3_8YH{v+X!W*+CdiX@;-o>C7Fl^hH9S;oqpckt%!KoY^-RkngBB<;=uYq`G5k4!+JB^*i>ZVkRiFf$9MR=dqTWE>DrO-Y&cCo?tlT)%^6(Y^HE-&bG&Q^j<M4^kwGNK71?BPwMTA)yX|cXy~1+bGe(sVWM0}j21W`;9JUw0p*Nk-(LmZea}})oM+_FsP*;|eV(BZ?`00x+fYQ?jd=_&h?rsOu#Tyl-D&2jrIE|$uD8)`s}QLt;*R7xMxzVG%a#dFNwo|?6jZFc@|?eJ=BlIa)^i54VuB`89|dX}(4_s&$hkqHZ@tyJpAviAD1p_e1wne#P5%k-N#n_{x3yOb2vj9>G3RF_H?jx!0vuXzch@XnXz@AQ@?~N>2oB$7qi#uBPqxqkpkSW{^Ld^grfM(bohAN1xmt&(RwxO02~SQwA#T!e>l4?s6=8uB=6BTe!Kg~}ANm3^+R4Z|yWHkWHs%7nfm}DHoBL|ew5VmDD$5?T=8<Ou_yNwt>%f+}@7C<^Q!zaqG91s>i$@V4PP)RRN{-(d4d2c=F9o4QQN2=H6d+;s^xze3MAKMy%w{b&JF|e4%JV*bE}rRD7mQ2wiDOylJEZvvW<bEKz-(SaS5Io9n;*Dq#GNJ2%-I;Vgx)dm{l#JeM%z&n3H6vAxbmJ@$3ro49d8|V1SB|AwRsW7O^JEQK^lh_b9|7}C21&&lQTjQW)^S<^*P7$%#EX&(|a12OW%v$8ZTeRKJGh&C_6Du|L3!M*HEz0V{ZX>d0uc}!eTEX0;T@+Ixc3`QSpsgOg}T%^p;51frA6xMBn3cBG`uqbG5-|A5PNj<K5AwgbQi55<X1G-G|Lxp;fTPFVdAMOu<XH7+bldJ9x}@^LNUwd;{DRdZYoxGd%W-vmD2CBwr2#2$q;?z&yaSD2uRz*q}+#>+r}oho)$3T8@xer=e4NEcUgatQwS}R_PkP=)^Uex@0hVIEy-AFYV1^k<+I@Ey)v3li#?6eee=9G{<x{)}JOYj^P`kWXQ0P6drJPi5{b=fP87uSQ}oqDiDcr;dXUlee__E#*kw;<D+Ty&lGw_!n@hwsOPPXz9G2V`sk2FTfBxQ%W=Ke_89%vr@jF41HM5LL8B%oRSA%W0S{z)yzD$9kruJ5Vee`?HQ)TCDi!R4;8U7f5K}di3K0pnoKqWYsrFJw1KU1Ymq_b<^Jo)<(-k%N=R|7<m`MjTbe(HV^gL4K+5qoNbAZ)^j*-r`Na}}WuLu`*l7ljgEL-ZO&>HRMVAQ{ZGM(2{{1~^4%b78Cx`o-#0|VxCyCNNeb-usW^IHE(m$C9GgdRvJhP=)ydId=j7+A~Ph?i8s5~~(1<~`1Gg_P4M^xgV!Xy++!cv3z}#XI*n#IRNSIzxs^9nYa_<^tczth9RPx?4K+a=YCk_UHP|hyDE5w~v{Ql-Yf)FuVUOV)xbQ<;<28oGprHq~#)Zw%W(3Y2Casvu~P~o@Kab`s4gdUu78>_R~omVg6lWdYB)`$gRKF#7>wXQb5#9;<&jgAZ~Lrb#Guh$1u<o@v*|SH!#zfLA#*u|M<Hsi7|qkyo6l9f{D{gD>7ExDz+jt1MQ2IIq5cN==S}Y*Y~#{fBWUPAK}B#CT!m>gwgN6{`h<N{AVT1Ft<l$`TEUZvyU~Gteg=~%VgbJBXEx5@xzZ_hhT&6o$GC^l(7lz+QMCUeZ@DIbtJA?{33o>eqq|Riy6-?Lb%BP@4x^1{{u;3s73')))
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
