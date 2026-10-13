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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_NkvK;td_}mYb-<kV1hb-|BBH08vR6#2c2Y0o1Az-1!;!1B9`tLi_omrI`Zf<TKS$%k}R!?m9ba%yvM})h%x%t0-^MCx)fBWZe{<r`1uiyM%|MV~a^`HOc%a`B$^69tVzWL+joB#4p|Ih#V-@bg~%a{N4pZ?|l{^$Sx<?H|S&0l{1kAM5+*VpfU|Mv4YFW=n$dj0g}zfJeYi}O$2<?BEFcKz|k!}tF9A20jQ{Q33Q&wuql^!V%K(}u7A^4A}Jy?&#9@%7Jq`uT^SK7IXwZ(ncUytL-qzy0-k{pIUF6r=v__4nhbzbxJl-~RjGe_8+3*FUtb=3|QcuZ};xpL6j^_aA&8%Hbn-e~x|DUw;4L$M633<wrjM{&nighrKWA;lql*5>D{PPv2hA{5(S%t+jmlUSuuB2jNlOuD^YL`{LVA<pOx48Ng_Uay0ATRd?h*jB-!qbLO3f->%p1zI^|u>yNKL18Xg}jt}_Dg8uyZ{@0xE6o&HT88qb#woL|y01R%M$?enU>#yZkZ=0Zuw*lid1N(Ph$9)*j<D(wq*fw4|lezI|>-TQ>hhg50(ckyS&m5Qk$)j!Kb0uxE{h{~W5r#Y4(aySQ9zInxg~z{nm(u#V+v1r;TK~ZA^R`zBZ0dHQ??>RAgy?h4=2%m*ds2SB`?2dXcZp?Y#$lJc_~~b?JJ@Ho?(aXH{@~I(`<R7q<Buil9iK|(eb@<tg$3`bUC@f9BU`tARO$olUr`nbJg27?sr;zi6#PF|d{O069xc&x)MEz_ysluw@DY1K-&WqEa#rwL_QZwW!($HXzX^ZEKJNG5UH?h>Bd<UHc>VVC-~Qe8*Uvxv_{0BR-f{Q81b;9SWPsSo`J0>DQG6Tj?)rG|e)O@uHZ(1F`1+~b;m2EAI`E43<N2@N>hhU79}T9g+}_*KwE>;`G6@s(KgX<O-6iz+GaoZdaDGpX_kJzC+t!mu`?wv>T<p%dJ7MSKvp)G&R`C>_+M6doi*|?q*HH4V!Al>ZfaY=!VZQLar5ILhWA^D~K|g!AJl`XFm)Ylqk3NFa*xw87f-G<mcb;BegzbdmlUH+f2vVyF+{AOEmCTjI^CwsHtjkCT8%`cU>|nUtAN=d5U;jfLpg~soZUr@wnzY>aVV?j7<bBxTLlrTu^^s4SH*k6nZ-DPi`TGrCiXJC>oZ!#8G{?LSzuGFygx<jbKn$0a{XqctuSOy46IlQ|&d?Dd$K&q=UnE?UE{$7+z6eVmNnfQN4&NIIUStE}CsGU9&r05F&-xsMDcJ|c`=V|ez?G4CdF`6p0YBE_@W|9XlF?q6=sW_W(OXw=1^&qFlbs`eXQP?7F*LMKi{WXNnQ-wbV9CVCS7fQ{u3O{a7t0A=i0AqxXl|0pBwR*rpz$N9{cVUERyjhQ{!u)+4LqXG^N7wnmMCtjnSbDqmtYcn(;eJEKN$CqtMDM07xwtOE@vqG`|{pwiwiQ5<kKpiec-hTA5`PUd5oX5TQ~d(h|^i$F6nQ5u$xuoUENQwgkppcnO$Q)c~j?I6=}5R!X&=WS_e9TzgOZIDIWxYAQgU9`f<6hIdDa|SM_9v)_Njd+N8!oLC-kNn5n545`5ful;+fGuL%GK5Gw%_d3mn=9Ci|AS*a;0E`&XUj)ee%)`?^$0WQG@2{@0Ed}V)69e5svPt1bAl=jb^Sbg$2-~IafOV%?1A;3@%XK^6(T%Nr4<HKWf&I60Lr*Qt-D4*>7W$<?p^`;=5SEm2K)w2CLI3MTYc@kuJDs^}NWxGV@om7wUBt30pkr6g>+T*+5Lv|&q;Qd@!9P?Qplji2+oc-P7{oChXKi&Rv{q@)X2y7cg2GQr8n;1YRf&^TGCuZT!-Rw1A-j4YGl=y&g{^HeAs}H}QJNWxO&iE+mjMR^k@~vRwp8~S@l-|7&)VVDT+O9+_Jqy+ExYaOEX15_YS;4V$=5vm~SC!P(>KXI6(wW2}^c2|h?sA!>HGS+lOqzt$>0*5MM^YeNrw-Wt54#}I3-kogt&ls1`*Y!XLwOF_{(3Z}llH(`w*jn({kLfP51;n+^+zxeaMNuN_4*5V0K1AQ>?M>DKN*xC3f*gfzuYL_MRmfD-=^=ao$+JoovB2A(ESfMxr7>Wy!q$#*RJ1xFHz=AHUp%ENGvY%q!mZflH1u}?p_usat48UD-iJy<;-t3m*M6=5CjLZ@`+KI+Ly!lmSvV|zYe(<pW3(omR(j_|GKxkMp!m*Z7GzHiYoQ8UYW)>cA(%fDT(}oSA(irfeG$Q*gwDi^y%}f1oQy7pQb;;I@Y-Q2F{Zn=IH)J+h1InVvylfh`qo^*BUDeLb=l_Q)%?dD|=<TH9)Q#k49HfbO0i8dX;Dn(D9P?k7}oKKLf*bc98Lc$T8o!wYk`l)r8W}S7#HIK;`0`fX+NCUE<0CcMl@G)STp2-Ey~*H{4{JD9vxOxxB|zDSC8}{Wup6;-?>e{P$m$>vGwv`cSWz;pDX(+Wi-7VDF~av>EY&Vz`qd*t35Ef?J754ei~pFAwLhuV2|Hmp^JidE<85h>|&nG5JA%Vo}bOtXm3_x1jm%>bi1wARoIHuX^aq1Dq3k?vL~h0<q|C#JNwqc_EZv8-Q9LI$TrpIv4i8onb91rI?{cu6GvP#)nc0Z$F^rk4%>3Zl3lb^q)Wb>IH00wk8j&EaJOIAnH;TL+=kgQ^A3?5r<Ohs^<y-Vi1scw{iFjg2v+kFHu-VUv@M;Dm)f@8Z7+T-r0A3m{IhjzzWlY_kJUwf;+b^U(4;XmE^%kc`p~3N3x=X1yE>2#Y2(buhlPV>OEgHEVnQ=0xs$fDpBr<^Q~a`HzgglNqv2Nk0b#?HH`P!@fqN*CWS>lP^VQYf+HZ?fl|tBYffofFc=biEB&$~$Gu6y2|!(wM3aP0@9XA>6-Vg^5|BITZET-9aHu#D>`ZF3rub6RZ9S04X#P?x$}t(2Canc=2=Cdm3I6eZ=zK7}k{824`TdvyJZ_gZHHy2phCcd{SY99a_a}3d;vcfB>&r{jguUeBsE0q>dFtXkuT9|sXy51zyW!E}mu(^<MU{+v{|Mx_sn5sQOFv4@?HutV<@L8miI)d3Bs0u%=X_3<E(Rx~AbjzV1}xg<HnqC$nuSelEDYQSQwsLjc$SsmiSRm(8K5VC6}3o09L}ebkNNTlooQ)j0WK0xYF8O60sHVnp~-C5CnUu>oiOg8TrwGpr2aN5egpKoXz@x+wPy9~A=%Rzd}gfZUIs;i8}eU9!s8$Hb$MX-+*%R@+CA%7SoRFwVoV*q|MUBHJVW`|SI;eWm`GE5wxC92gO`j~fHq2!Wv5s8M`oWO3ex1cKqVy6EDK5UD(x6&G~KtC7YKw)K}Hn{nnMpVu_6+&8GVJAJXv*up+1TF5zOL*j$+Iheu+x3&~6zWCX)78!>cCA&a~%F7)Z<b(q(d3la@WJVJw$O0squS|8`g6XfKfQfEC?Q5E$uB^FZ&&V3n7WIHWd6ilS4CYbGN*Wi%iJ#t!q{6)P^uWPrRupIxRQN?3`l)B1F)B*z=Xz(*>2&xKIA(Y^nPS)iaW?JgBZ%i0vnM}yLfh=we7+F@cue!OdM_?k7fIpqY&p|)8HTjm&f;Yq>@$RLre)m*;J9Q><!{G-Y|qqiZg`K7)O;&NFm3s9CG-x7J<F8R0<RuMl6%p=H9z4KP4QDq}$6j;nEbOj~%RKf#IrBS+bh!;zkCO$~87Eh%h5bevD^6lq3#pEwTu3{=&VEevR@BISiLgj*LKfTLMR%%S7$Cq=QWK5@oGk8f#`{GY1rL9ODhXS#|k;=4}F@96f)%5$<*Wa#^s)!=;7Jdcf^>Xc*a97s?!~1*92HZpnH2KJaC1{Z9m<ZP8GUnbF@r05XuIFYIE&PEA3wcR-v><YnE5D9%B;L>BrvWIjL_C2mQ7!DGcCLghT)LM+lwBi(LJ7-aH4lSrx!gam!Ap)7S4UaMC1_f<=gXEQ3+&<;eU+}BBb$TQb?ot%oiao-V7fr)7w8`WYWiZe{??STCw;&57Sa2`fiufzs67!p5@mDjrVQHzMc`=El*`Uk9?JEpGuc6UOEj+9yE79`N-iz1^sj9;;aru>4I;vZ84>69doR=d_O;Z43S$RL?^;(;^}U3^m&?5rL+94&Gsyu_F$|!2lX9u7q0Q`SKw9xDKoR(1%`{ecpzgEdZNS|l1^2hOepJ~T_rekKOAme}xZ@ue<9*152~vJ9fNY`}&|u(gs7rMPhTZ&ao{!s*rN&|9FDRg-O<mtt?g@1XAXc&YMyFcYiZC1S&s(FAzsS{5lHz25rEf|;r7eqUS&J_?>;820JL_XjW$?_ufz+;_L_5@mKBpD7@<pyHHsq9;S0g|UoC^E)6m-Rk(vT0#)`G^fS)k2V+gkA}MXO2{<)M^xkh?P9VciRo!g*m5;(bZmI7M2g#ks#>!3!TN^>se0C#;I|$uo7?d`iH!vFPIg4X@my0*hZ%b(@v0^#L=pU2>xQ_Raw?Z&Xx{n53>gglz2{ZN;1Su^BfbKHkGInxAuwM14(Oe(fkrvSNaS8klNitU;X)*HT_nn1;{Q=hPQ!fVdIi2tav2zRBX3@@dr@0QHZG5oojbK(#1TvaZ@Q%_jvRccOTO>3$$Y2`ooQF=L<r@7rf@zK}m(-q}gw-lJ|%13V%LG%Tvf4-6|vjBfs<H@er931-U58>-S+QnIeT%!ZXN;2eg;>=3VsGxCXPojr@QSKoH5C#erMFz3R0etAPfh7pSuyolBMxz-nPPS$Td`4Z{W@cJ^KF?dc^;TARy!<WC?y|t#TEr*xfLT*t5DA^*GZq@nLWi~9KD(n7;^KfHET!Wbd?WU5sG^$8ys{Dp<OwZm8dH&Tn{s{yuNOxfzn3%JKevlS*rcz=|@t;ar2ZyAh*3tT(nAZYcp1PH>T#Sgs4YF$bPqOF6$u8Y1KQi%#RyIPlvzX>Ct|Xy~4?su3*q{9;o!<*h9E3BpZq71(ZqI3SBO6ud_JUWF^hH+|DKsW_Kj2<Ks&7sN*pC7@^xC3nJR!+l^HNH8m+&TXN1NA%2qNQdalp0u+LPPQ@_VMzt3t6#FkleWGj|$QI^~-l1Dd0~T)@bx`qhI)k&V$~h$f2YKE&Pt)S;=%Mg0M2_Wcs4-yf{3=QZ7pf>~OX6l#ySkW&N2k`gp=%a&jP2@@uXrQSy*pP{tg0ZxD&iJb|c+A64vpxVXomgqFF3|U=N1!yr*-H(1WeMUn?j}DMzBU+R(8>F&>MUGvfv?o4aXVle4wMF$+81Mp0j?K&ahX><ZFpsZ;oN0autAs+i7jK+>nlKO*KvD@0y3#`Qo^xm^Lp!Je@lxoOE;XwfK@`d0Iwb_JL%QJD#N$9-<62%s^b$~N!CJ~%lga$k7`8>}l(!%XQ|Vi;*=OXiykA&3nRm;ywXyA;7-CJhVw5{i#rj&QGJe8NVW}C)k;s&Rakds<Q_4xm6GA#pOD7;*mM6Blfnb$}jua+EGz)&3Xhy|rNS_{~MlPTl>#~)q&1G4LQ>6zlE~?7=Ag><N%jA^|v>um~sfK5TWzXbvP;ob%Xlfp%kaD%L^jb<mJS>Zc`i4{?kzBK;3V8{(@S5D|7%OG0K2|Esb32lnPtY9@Hcx2(NSu)TR{-=A8fj(Dh@$&IQ)zm?hPrn3N!n5d%plHe44!|yT!%dh;O=(ol-nRR1%IAbswY}-x0S_v&^Fn$snQP83J!6?Ai>my?{Cy8;>O5rHl?5OyNP=B4Lxuc5@Ya`P~}Kk+W77;FisP{#8QcoJIr`HRy_#>f=bEPdyFwwwrqRoTS`U2Yp&kzSfT=q%%ZQ>Qel-u0H%Sdjo8>!^>~{?L#;l&a6gPERGC8N87M@qM1evv(Fhbhf0Cjq3hnU8_Ib#kob+p1PLu2GP$(eR>;!FM=;09F0swl$3se)o1>_Trm7vKk3jQ>Ia__69of)wWZ-sD=4$nj#>cuE4YS)mGz~JTUR8EGaL_#A>s%*OZ&TJC>XtE!sNLH2!T$#oybtHY30ion(u`@{G#*HwVyCua^XXJ@qdtL8EBexR(;Od7(cs*a;8x}Vr*1;O`MjryM=8q32VCR1+5nlJ1@VXnz>`ni7BxRdoWWX4pvQMn$8fysPFuJdji}ckLk0tL$kyA_EGHIep#VpRWWjftTQGeXBtYCIcQBuz26KYz+UESJujd2h<nxx^IjlHcj3q=CW{l~jWKBvJOP{B8PEK$=nszk4gFNQa0PK5>1Az)nWKy-qm$MD32Iw&iJ^#pgG<CG%ii!ZTubn`N8TN2gN_J~nu3Vejl=J#6zhGu(Q3(zw5Tz!fjA5$zgfxC)rxqTY|QA&V5A*mq67bj*+3Jy`TKD%uULE6ooOk=8#TS4qcORadqJS-tnKve?ug%`FQhS!xBflEN_(~RvytDgzG)!9cuSK#^Xhws5DleDIyUJxntR7#*j<S`uvok&3J_He&kT=#<_RTkv_`(^x(lK_-UwioFJa%s=TIm{Zo0qaSFtEwsiKriix$`B@t2yCY-lFw>(Lw+{Yuf*0IGW`JD%28ncM3jL`_njbcE5BNN(=EK9+;n(C7he@o>|jYrxa=up(K4L>BT7*Kh*YLTsw~$qnxG7@f}+Qzf;n$NPD3UJn4l+tqyl(q5`C$NXk><G0X;msR;c*N#LQqCCi2nmZiDHSFc$CugDxX_b-CORHKNFf-Q<=`EjVsFekFw=DFlb97gR*-RMhPzLN%~>Jla|oK=ihzqPj;T%M*g#2pAm!W)f$tzzCy6RZz`j?*nFePk{4op|}EebETZQBC}EH2J<8;wr2TG0%jHi=V~|V;3}aAx-BBQw*lDs-+d4*?|*jqLl>-xtHiz1kiD(2-#N<4j3?VjrQjQt!J{yt)5&)`_M|c!)Ayo(L7IVW?vSmK6Eq(jV;<wE4^`U{V9We<>EeXhet*EEuW`^e#qYYEC|DXTg<%vl8ZfBN6dHKN7zNsOXRx9!a%(d6hmhw$7qiMS+3-wuldFA>r-Z~Gxs*ZYwhYO{g&MCh`NTopby1xUprAZ~mU5#Q(6Jx!KZqV6Lpp5z$B{oG)qV^T{piK;!%wyCPy`Lz(0QWir5c_Zll-)&Q4nJooFJdcbRGHSx;_#s?hGJtujV%xX`*v?0!Og?d|EeJ5&e}f>g2L}Qh+6RBx@4tdS)<$+ql*t46eMdy_`?nb~qg*f<=Z=G%JFY-hZDd%=JkDj3x&yv}D6xHW0-T@J*R1)aAM&qVDfIr{oayy#Ve>RuM3CbaJQ;ybv=-FBP>&sbhRyvP+O+^-NEYcWke0Nn9zr?(uZQ(jc|2`(Ej!vCL?jXEm3SQn;?C^f4JEEllSX^zaTMr|;+%2>l5km0Ss3+#Bg|?IBg*gc8=G3ORK3{azTVK#Q7fHYG!84RSqP-JVJVq_QPc%uxr_T+D`cd9ZGL)Jk3FOQ;|e!7eNx+{LiDM79eg3QFRI4~*f8tb7BZ=Seqt@h-g>G_(3N+BLVW=}0%lPzO1Zab*2_IRC}|V@M3ze&vyP03>aS3NtnfD+Ks(M8zH}04`Xe3UK_@!V<l!B+23^ol+B=8dA4F^U9&7J`)`25)`82jhWa(>cJ3lECxT!SE*Ns7UuvTmchy(5L6UR$7J0Eq?76jWnig;!jX?kxYK}36bV%7J2=sYCrVvBEh#rv!5*O!Y<hUb(!1RAOEw(j%$CH?(q=T$(c1czyqxNp5Ej+5c6LE%35h&JLa!`|t`^OpoB;;1CE|tK^R@RlYQh@Sg|}S9S>wU4(;A1AWN_@sm2ZX82rP%e(t_{vm{Y=c*BC~qlUZ?<q;q#tovb7~4=iVQ_q$yuAts$zW@meGTSQl#ZJ`D#K(N(9o66J7UZ<cF7-*4TQ4lJP_2TquJ>p+Na6LNUqY6036~_Qaz9xfhnQzjiWUAw87tGZHR~M2TW3X5y#WHA4329JXfwJX$m!J!-w-OYN9q*+PWEt5#o>R~DDNnG-{d|SpK0M($CwANE^^f*CIa?aazY<7{r}R<d@Uo0FqWb8MEvbr{iwN`)2x9P@2m#9u?L>)yO|CY~K$C)ii=@T{<s_>DcUxLzf+nU3iS!uJ#we<{sk$xe49jv1v@<zTRF4lCkZlQEU@<+(f}Yc5TdY<+ctBv7mG4Ed>q>Mk0mCZTNzyQopwR>nQ%smJ^aF2IE=R2v3dJWa{;-5kOYmt>I|s9OiLy!0uc&f-l&Zr$b5INZ5FaTzu^#<G>KGoL-=JVIL#pFp4<icU0TEH@GX(^pN&>qXGwomHj#MdK$g9vIi=4Yk&FKV`O|XXqncM^Kvn^8(C*~SRdj#_D?k40|5&Ls%;>k9rcEh@<Q9A7dV+JPKCi7J+8_%dQ2w1D7^st4-{3s;b7TRhEmesSw*s*64mqLXZ5~Mhz$l;?yK&qWb%eFV0Y65ejb|)mBS^9_{R00#uT}zY~BCcE1MIhZ+<<AjZp*<>Lm^$(@8rF7{tEi|QI?w3DzBmdH-qwUFRj!2mOSF(qMC!)u`M#*PtH5uOs@kc-5=|x(_kD$X!a+y;Xqf2@X{~^s7dbeNL+dD(1xXgpS!GduAn3i7zQ)&}Cl>CDV0NyTRuf|r2Yp9`tIEOi1d-fw*U67P#fJ}wJ)v?OCE(xAvACq%dN#_3u`pv1<T-H`o(NdmBxJjBNf?<MRgEvm$f{md9)_WH-A8ElGL^?9_5m}SvNDhHVCn(_MrGrPS%54O=`#{EPIcMjD}SUO&moi3%aqdvAw`wog2#{vB{YOWNXjiyE+1YF$heO<6lN4pP0TXJzWU5ln$U*b<IHi>B?kc_ap>wF^l`Eiw5rpHIsu14k-#<zp@n9|ORb~_s)IoKi1|WfS6qom0wyp6%LtlM#d@g*$^77Jdnw3z@O+k#tYd(;FB$xdDoBY6sqjMZ<7`((qVm;7E@I(N0tMHx9k~~BAJH0yOaq{%|NE5)@$NHR*hAoAWMx-k@tH(WLx5V+%q1dkQ)lizxhRAQD)D{Ilz_IK2?)bZG^FS_xFAI(EEQF{m$CO})K)4*548AO$!#AW%^Y-)5fOkp!P;xYt~@zs>Zj2F3ORE1Ss!xVPzKd7p^|TXEOMBifqFJGr_PJjH3Gc(UYt+tt$bg1!41X)>Q4n^!s!!CFM=g{-FE3UZKeSB=Ui0eI=(&YoM_w<T1ZnxvU*~V5uGD}QE?mK0T<z}ml)kvZfTttM^co$P4*?nST}!5fEPm2;c0Y2(2mmhrQG&N*jV%0g`9JzTS4*x;Rr<4iMHpWPE4ACK159T37Md}cG4;%jv<mp6_p?I_h}8{w0M>tmBoy4b8Mf9%-7>>rt#s`b%wRBM5MV_aL#sQmvxg)yIjfcA!I0esc%ky>D|EEC!HIJ??l-orqF$3!Aek)c2u)jyqB^ODq(2r(3qs=Tqm9+O`;8SC>3*<>G0uIMA`mB5__c!3ok^WlnqKgM+0&T0+(E48@ZjdTC5Y)1u<MC^N>)#ju4E=Ul1g;P~TEMCRYthtno>Cb1a{k3|zpki{;exS|ffOVEU#B5t-%7JR_kyStI?6S60=KZs#QN8ZPEh+_m>#55g|4Df#!RIAFe?$*K66(mJvst#FGDg^vkV24&X5nfxmgK~zxaRqvq6r%as|U8IO7^qEg7G#&Ly8pf>0$zzZ@q&0##loBi^wLw@90nre4JoHlWSsVpGt8Iq&!BkA#L86?!$F`^t_h+PjO|?ks22kTrLGUDexxyZ8vHm~rX>F+&!wDW7r^#G}-qxqG?CY%X1iBP_LK*GhW^7@+cR8`GS=l|PD3va`^~pgFnA}CI8$czuBouN(h1GtKPpubGo}x!8lw`$yjYIn)=EU_fFlrJp<2oliU89zgk6ffCLx;%y@&tTCs0oid4n_L4s`6{^1ozy?-?%TcfO1rKSYlB=V`<ZT%uQ>^J7y?>T-%B~L<hu<{A#M?is|w5ZZeTuAShv`TW16p7-O^Ce+ckvH3F1XDd$|+q?GebU07KdF>Fyzs<ONcF6$25o&Y15zZ=lVZaF2EHrXaSdOo8q2<EFdymL~{_A%hCp^yV;Ptf*L2`*Wj`sk|5<CIp4(f;TGx^zM|XSh|5{4L)(jqa7$%A-=Bh}E|+`b@MPRP(mF`y)8Rk43S37LpqXv~Hw|r!EII&3`DuB(4?n#Cq?<u&lnIzHv@}Mn{_@oo(PKwyl+Uma?=7YxtT@h+8B#NOyQqGNWuSf_?dA8~J`Hv=)q^BZ8O2U#$#{k}Bwvo*wr&C~;v5L2IJ0+rL6HM!vpZ^B)-<f0}V+^a-V*W2mwk6xM8)#r9u(rbG*<QEF1AEyFgX*p?R4*CH|zNhBu?oN1G&w{HIUMni;h6UfYT4svD%Wc-ep`7S$cQ^6rwDT=njb1EafQJ~fEGAkhcYF14b=V<}88UKji5+qT3?y1h)e5ypCRqU3n$N9^Py}VKM$L52#DpckIj+uZ2RTZbQZUf#xbpe-LCnN5p?veo5Gy<Y}+#fe=E>}|=#?>5{zEe$8l#GvLsXxb+E&s2~!Pqb2b|+19CSZx6A5VW3dDi3$6&G@wuCkDY6{+3S;;Z_+jZkqqi)bS%bx)1OlN<rUsd^vx(EFi8RlkjS?k=&{YSrz`cz^-y&LiE^VR|#vN|46FKXPAC8XmhdyHl^cW4r!9$Y<bP03+jtk#)Q;kI@U99Ui|Od5E*BWD-z(<ETh!h(<dR9nHn5*}yiZRMz#L&0nlf-_{b3&H;n8g{NjawU01L<2f-YtDFVKlr(-}0^}jaRJG&zujvR;od1fh?zuxuUo4*4z^{v6y|qg!)#YDgECvK4EC)hPKG@UpThFD`JmIS+NCKn%8J>gK#MGD855j^zK@hU>k5H>l#D{4Fo-2^{rU(q}XRK)Cgj?ChC6bW6!03P+{`96^F;>u)hbRCf#IwA%)n`;|@by$Qe9y@u1DGewb}HU$qE#+{SYr(ObeyRlG|Yk92AwwE$h$sXDG6$shk(2Yg`<E@QzKPcdP19dw5Dy^oXZJ^<W=WrtbRrU+6)L2uEE=UQ016SzIf*>=xlVAvS7Wa)ygMlE9>2IT13UlE;M<bO-cNs4xFYs$zfv6byU~;2@7kXLaX5dp3LCos*reTp0eOcu+9Xf`%}Ut7J(1$H-Gf>5j{OTUTPiS>QPHQfFM+)2?(2p#hgfiWcPE{<jAVRkTYX9B1X!NDwu;b_VvbGoYNrRn>3n>sVp?sWB(XVtvQdShE;>CiZ_&~*N{=vEH!&;Sngo0dyvOXphSmL4`62#`O4u8IvqgSeXOdlZ7yF890`8>nOTjGf>4UXHbxYb(C3~|wa@{Yd;%}V1$rXMHAz^dX9St(85vKYEh2WvNEJ5)&bVEb*7k5&YKxF45yUi~wu!m`Byy9Bc?gECuAIOE1OnQUtxA=Fu~Jg<2dKkXamT0H+VW7uPt}qzCnmZN)*oIhOKG^kd#SqZjHMeR1mwUFl1LRA9pR95+qK11d;qcUOpQoJO-foI4nOdl42K+he<|r|LOW8BROqpy=7|Ji0WKNoCC*;@keQ>V_?f<M6*c~*B{*~2&sq($>}F)FX{!}-fPsd0@YIMJ%rXAfPSySIka)gad&NSKsKSW~H)dja4d-Nv)<G<kYrV^3VTxhVCW)T-mLG?*Y30wXb!Va|Ju0bWUYds4Zo)1J@ou_e3Bfgrk<>!Akr%^bCEh&X%9;|K>nwhgt`(x3>;Mnd*+X9WrAO@1ze`P|sd!HV^v#8$33BBrwNmW&!PWEp(xCiT|Hk@G>s@(3AP)o2Fy7aI0#{!(R@E}~J*^GkMh_F2pM<551}3}}6Qrorvtjt_&p9LM?m~>K$~)Da6U!B1F4o%ikv?}R1`)}#Qg*|_5%xPym}!Fj`er-G*}JN2aN2t3R>xxjY{**TY^qBt@=<m~XV!8%qp|${Cv|CkwLJn7L**Ro1amj&o33<pWNgxa3|m(j1CN@<$^bv*5$0nYt?mp0{*JwJv1*m=pUt)VpF(v@)#cd(mO7sSk;7pvn1g4OH^K&DS}UR3GXicRq`}VA&RN!o+`L`v`5ZqjzRQ1A_r`I;N+OZLMfFIFraJP9Sj$DDJ_(_-_4Y@DRW_Yc-*{goP<}>$x=_y`0Hy$8MttAmtQBc?eNwqau>gU)8t)_H6NNolXboFNCHBRzH+2Oyo5G;FEhbT{kZHoDUY5yBVp$fHC)C7-b)Y_@bK<vUjxP$gXUheY?H#|#=3Yj(W2*1YpV4-QB%j@weN41!j?>hw*C(fGz)`aM(4yMbQ%g}w71^o6VqQj?vr8DY*;1}R+=J1lzA!ll113~)|0L=I_x=C!`wu^U_qT6f*SAOOIc<4=;p;}$Nz2O$IDsk$5agvTr6HajdxwFS=EVXL1v&?KVJF4kP)s@iB&g!wvfKl;V3)pF2``CgpE$fjF|nCywMi;Dz{;lWw#kR$0iZ;SB`Kj;aDNXt*<58F$d|P7<n~F2^Bw8;L|he{lFO9q-Gl%GydpUnSeD`p+XbIgNa9!*^zW8=%;h~P(LU_49g5cErKtJ*kpIfsh|^|h0w5jfl*MvT`aBpzLFls9v|iXs82>k=NlShz+~ydIlvdY}sFz$n!th^$5?SDQvxVlp!(kwg+OR*<xbo6VRs_2ERCONt^517096%Zl2*um%P)H44N!mx9ogy!@ou4eQM&8iQZsoi7>H3l2gn?O#kNvJ$c|Z#|H)A(Xw>Q<^6Hc{X9DdPRmGp^xoBFbN1c<MVo0Ec8+fW`br>V!cU)+Bf{;9gE{NqH)^p)m9Y)QNE!y%@dREc;^c$tdc$=xlsv2s@~;{0KCNa=RS6g;A`Mv@qM0j4E(in$f4`*HKi2699<o=9TsgMf&9yq~j(K}csz^CG~@8V)UhSg@mhBLR!d=!lbBlo=qZAx0T&p7zce8qHF{jbbj1`$P4H7VoTNPA^>OCr(q?<j^e0O9H<`_A9wd27a~BT*?W&vOe%p4LzKai(fqfEO`#L!v<y^**+IB1m;P){e-!x-1;dk)7h!H8x?3$cMFuFdM8QcN{LcOV;z7_bHkwr0(pIU=6&MSI0m;<kFWp(VC%p53z_WU7d+22_mEI?E^Mg=d0b|%vnXENWp14I11Nw9^4s?o&li>?PsPzRGm5m&z-orsmFnd#zAdbGxs3k?7M$tE#|^4Ay!!tyYabA{?K=@Z&1FjH4kraEy!$5z&vp`Kc>bn5Zv#MRVO2I+Na(G%g?W$|Ver;#rjFPDA8)OXdC~V@MpgTfy6IkH$oxSU7$*Q+@g0VsDl7jd+(>o%;rGC@Yh=G*xUKVrPEN6Yolzex9Ns_v$CtnU|Nhf||Ih#BpTA7zU%zR-en!*x)ez^zK0JeJe)+oThirSTA)?ZO6%EEPCR*Ll&f{i#wXo`K5R=@O+?zB1V93vS`{cR0^EhhierhO7++naxe>uc8G7ha}a~b-49p7+)7xyEjjd|u;r>kJBLV@;OgW|_eKYw?J+&}&N!%v^yZq&bCufM$GMsJg8g2iUNW?fB^Kt*8v=oWK&-$&?nzD8SbF%9$Ad=w%r=X@j+uaoIyrMT$f7R#ntjn8g`XyJRk_Yx;!y>m#v80_cY<02j~kmJ2y{xxKU7-6yFxOaiRZ@-_-P>O}#hC9N8&+L^gkkrnZb~uh~atcUC2{IJ2tO&x1>c!xgXO-vdj0l6adL@^8TSc!DO|aa*um)i(qyyO%COTbM?0AVzI#OwjHXU@jPTOla&_=xp_D=z+5q^va+zoE01-tEITPJT1s2EJUPp)6wZ+;hSeg})U51Yw5s+1bDg&la`MobmYDAu9&HM(k)1`OOOcaMiC@&kOUE{N&u9^b!EDOVl!JNVv@>0s91wkPcG^n~Hm?d|-uR!!#_JZ}S9A}zja(hn3Pn*AWAORjrVg>p~zU+^B_sZnKVdBqDTLM|LI@Y$^@-oyU7)o!8ERBs>L)k*G<k9u<d&U;|_?d$Dv|4e;dljh37Ip21oMd#Zp4zPvJ(;!n_^gae4SA0JsUssqSC({^9)uWkHW-$cxLvd1dF}rOsC!L^1d!Yd+U`s;y%NK?v)2xTg+`NJ&KgPZFLV1o<IHz*aXF=fzfd*);bH3;VY0u`vCeYG@5^ne0JPRR-!qo@sMG-aHPRrcpJF24aL+WH}#EM-vZ|>wq_vNAFyQ&G-$J^S=)x2I*uEfVo!k#(pa}<YwvH(#BM0eHaQC_1mpz%-y#aoZ}Zc^*a2`Ui+83pzZmS@f{&$Hsxd8v=0$W%!h^8Is{Oa14viN+t?JR^$D<z0{U3F`@+S0h|n{w`=$RN0Vm=>%1O)WbKEQuwNdmPnT_y(|$K(4no4Hg_W725k@HG7wV57=>)+$AhM~S`P8vl)hZTF%{b}$uH`e#SMeME}tLR6&b@Nx`;JxGMn@O<3uVGZ)2F%F))3xhp&B17M87jSbgg{p6F(Vou9#k_1xgCs;wD#S=&o=z0;T^ifrgVqEJcA!?%~{b%@39iLR$jAj<kI&K)JBk=sivv+J1^8LY?Ixl+}`Say5S^V%MEz@j3(M~75o4$Y(wmXuYp0Sf`3ja-+yj%d(JV|XEw1#VEjTaHJdMUDaNs>ek@Lk5;V6dkQ{!=2<-H&p8ck%@w6&+CZ^E`oKebL2y@q8+iNfKwK(8R{Y*eo>i{lp{r<SKC}<B_3Q0B`Rfx8w#WMwrTW6BSbUWl=qvAAoAx<6~=el3|d*FhNfd{3=*oMzYVIZP+*g|bW&n=9Yind$&zqWrwRl{pl6P~K&fp8d07c`peQ*Ia`Qe`g`-`z(T-I9v&)c{pC!wHVx;?BFy->A@8x!J7mp!bt{I^a>v-n``I#};2rC&N5392R&Rayb0?#vOM(7X5mdM&cw2bH5=ZJK9rAt@WhH!uTbvxUpE)U34J?siK2(av)w{70P1mF<|p3AK>{<5;Doyq}lg|Q;?w6D>&4xz7Xz$40|>e(#!%!Hwh9`OYlkc4~Uj&7__;iC<$S;s$j6jPo|qFIuNOs>P2&l*#zcMebMMH!*O*KU_OdI{4eAg(y*R*>qZ^mWMHMGyAC3Zs5AB*_zG`P#0Ln__}B(<*I3{(sxaw5l2=H(4L|P;}kN7H5%gNphX2MfH``WRinn@u+?4^M_!_i-*vwk0u<$LxAf!ia?5{w8Hl^Ofe@~b8N9&H`Vf$(W=r=UL>fq!Om(97l|H%i45wpsx<3i8>yUL7wxa+O6)J04D*LI`+OTpqcW9KUkK`VE^)c-Te-W0q?sq=Mh89Arf6@klcUmc7-&l;vBKAp^@(m5D!G~p{s<0z!ADp}I#gh+GF2}^)ER#PjCHJ)5JZEEwa94Z--{^Yf^(qM6=3R6evAgkQZk~bP``6E-en-hXwZCkOrneNS1{q@KBNGI?H4%_2nNW+)WXorE+1{~VdwTfgW)320DU4CA+*^|I9f=3Dl>U(GLMpZhx5`FRq~jD1;%(&Qnq+O$dz894rOL)Y_g3o?V?;CHKepP_lD_#CkuWP{Q`JNKsOTMXp(ifPd87x^O@gfCae_du?Asu0m`ovXIH22*&13eZTk|eO4Y>_AL09)hRP;H{&Z;N7yv+0e5{>{>)Y^0rU}*h1t&$&j`;GhNkZ{^_E-`5X4?Ujm87;q6tw~)Q}X1R21Rs$2<K!S{wxOF==hSH#N)^9MC3+kgtD-XUM48geoKTMM{<El*2yUI5rZz3q}wOBIH{%kW<54KHGnD>*pq5K&`5zvWlj}-Xd!X{ZQCsr;uIG5VzLO1J&T?-k6pe9gMO>*g(!1clDEF~HZI#1R7kNMoEem2?W#x(W{^YV8WsWyq+K-xR}|jEGjJ~>ibZ&Y<Cw3x7*u&};OfzuR+HE9i$bGmO{&}%>yQkt_>dXy5g2pBpH*In&fjD?96J7Mwyd-*v>#Y?O0Lj7;qj>b={cL1w$zMI*L10A=t8RttViPPw^A{g+SNjs0!+pps?aJeLz?FMtMr5J6KG}CN#2;%o;lvSUKg&5=g@_7s6A0ZtwOk!+5Rr^TzeU`O{jYDiXB!Fkuo_NBTj=_*G}Fkp4y~2pv0XQ?a>%zd)S$(cxw6iN>U4^sZzcrU>p#{fv2Y3o>VHbGR>-G1<AKW8){H76w;359a<v$vL}Qc0v69DoQ|ZO&5;h3r<4T830TOCJ7Qib)s_l%5MoQoW1?|hv>t3HghSgxUW7LB;st8qAqh*xR1suiWL;onFgfF67_@kZ^5#6f0cYI3YG&ZM03b)Y>wM7DFK1GNd|z1{2w;n{FfAe9$r~}MfMkRc5v)w3VdbSOHg;2}pAwE;LeicpyKx^o6><EEyCh^B$B*Jm%@HX%>KP`2V;O2sA>CqmzQ@vt(VUoKNUbd0Aasg+8(<SqfZ?JXk&`aL+we2;1k%`W@<RS4Vh3A)<Z;IZY*EzK($2ZuJg~f7SdU@gFDi6${K!tG@vXz@>lDdDhXR#MghW6vz9FziTKYlp4}V}_7~==qnHbpn1Du3zA&Oze4J-p*hwr5q8Zml}NEG1_vOJ5T=tR~bFEs_&W_jrYZTt)~jII!bk;*a>D49pp&J+}^o7@!|Fmk;HjW39o2F6?$z;~Cn60pox2Qi!UO`ub&GHJ0Rt-Cc7k(aK|+h_QKyy<VM$?IGM+7*H?HC76>lUyrxFLkif<JoJH_m7VI1j?&8$u(<eAT~5sVth{$qPxtejL;WOAa64m#ZqTkAgL?Ie>N<47pb|NH7;cM{)p(~#)HhR&~E_<#aWrl7zncbko)M`Cx*b?b0gob>5_66L%@qryZq&7BI{ryX?jMuRtlWl@EDwrp~jB}@4n_33IiI?w!5JcTDrd|40WoIgL)c0B5objHM87&N!3kc3K&$9a2?T-M+3kE3M*)sbav8RDuh=uy(pO&A`92{Q>thYMrYGhab4um5Qk7!T0m%5*S0dRg=Q968q_WDx5nFcI(do{gh9=ShUUa;H&T8>*H)J7bLKG0q3b>8YooAskaaclxn*5BL>84VhaYLdP!$$8{Fj3d*JlppVHhI}ok(KZq2_#-Rf&nNWmF8DS5**Jv8G*Pm8K?(P~2thE~@pB{11GGnVbTt;d#gN2Y!8ZjcS_c%xJi&Ej5W3vwen*LXj+T)JWZe>wtBgTr8psz0xwH=m7bPs!LwdYgtmp6jpAikO4iNsaBO)dQw)qj^9zREdI)$62un)ayQjP^Qf{1rfyM2na4lA;LQGS94@lSOlnreOmK8_WyR(<p2A|1aK*UiZMcgHQh>BD>p{plOPPiiTbR(x96p$k2Q*liV<{&oi!mGr+f?ckVzUi`v>J3XNQSM`C`B{ZzaKv)2^AiOfPo=(c|z)uOfWbW%d~o|UAP`$-^<_!NnO+23~CJ!Q8c<j)5h7$O2T!uVTRBrn8>KNaFke0QO^VZMEGuOpD%*5;4blI`B;4eou6u;L9D{U{&hUd2N-5pkRK6%Jkg|DHg{J@*l1>pwphYDgqDkTCx%8fSQ>Xh09R<&pq{Itl?|B5b`!vsXLwyp9=a2joKcggK@EgVLZQ^6Nyll;g<}n}RGm#X3^LiC_8KKjZ+4jCxONy-&l;$27!!?75(BE}QJUoPu>^c2qsy#2i@UIMC83EwmmqSd{Y`Nz$!=KW?7oO3Bp?Nr=m$!q-N-xL#MnUpQP@DKc7kAxA(8qI$nTK3EogSO6fPM3>D9=K!bRu;FE?n4si~R02NlhB_l}*MaArL`)E$FUh*_@Ps0U&Yi?OmkF;Tq_E}FRiLpPp@)AZCvK$7+**k-47H=0D$wkMuEW}oXSAx$J`uZSliM|Hq7fCs|Ue!($d!13;5eFvaWI`OQ{&!MqXf~G;@SuZ0$hHq*FPlW74EaOsEEN$Ff-zOp)5v1&=OS&Ux@^Hjm+6AD;+oOay38VZ_r9{Z05yIN3P1!ip=%oaB`sU_B+^MTI`Q4iCts}B~SiXwteHCs$omnp@%wsKTInV$`1P-xN7E&PmFDx#dq}Q7)CvU9H=<Z2T3~)}yQ^6pSN})Bq<SkprHC0A@ln%nA8Hr4*djU!hX%xrj0%~|@vDRbap}L>cr2-9-xXg?@64vvw(>Gtv^+%_SJsOBdn2|M@xlybA8TS>8n60kxTF&k1cIQ!6h(0>>j&q^cxl@~}un)@DrexYHVK8P(8P9zlj9C?thmV3`X1R}&tTVtvG|J>iHm5!4mF~4d<~@zW@7TI7!Kf|)8mBuc8ZB`WfTU5i4t|Ot5Z2ozk*Fa3H{z83JZHqzZ7R~uE!Y{6E7iXcmx@KyJGIt6{)q)%ghB_-e#R+1LZ}r*yVmhVdB@<jma0j1U+e=TRb8+MV+x55uTzKX+(%MAth`D|y@N##l`E^-w<c<y(x4rfM5cw5hmQcCiFvDzy%5?|A@4z#8d&N+G5xMJyL-HP$JY`V`S8U&{_S=Af+#gZNpv_4h)P^>+aa*ZQ$>?5-3Fi2%oq$?c<o?5f^<IcUO*2>&*dd3;IS-m4{(=>LT+$&c~V>V&t-p!D5MU`q}ny5_Iv%bs<He2A~#OV<Gj4fo6bM+jzM4OlCZtt5)grmFr`~(8_V_=TpV~%B5Xsk2&U7`I&-n3<VD8)rLS0M(bpiAfmHWw9a-4K9b>`uAel{+>qk0A_v;J26O`hYM4ZSOrqv9D#k|6NJ-d3AZ5mU?6`<%kMbh|JPJ@>IGFNmndBaRT3Nq<0OHEY^BhK487gG|Hm#lCreU7+D=gu>fT*>ih0+q*@(QS>RX;cOtYrnxy6oq!;5!Mh{?X!TRV}gFL*469Cx@u_z%?aX<jut-%*H_c)*o}_J5W4+KDj5||WY{JmD7aYc&5H~6Uk8x^^-@%~DVBSIDFJ~mss++9JkmE)WyKaS8+!u;C26teB73Ucw&ZgHDS-`rOB7;9V>#MPg_3_NUuK9j>kJo}hL{qKr?#a8q1L!0r5RT7g)R@)FbiC`&KuM=by6XLIM05a@cj~5e_XH7w{6Nfb-ANq6q!;FNe7jM;tXLFilzw?zX6Z1PF%E)b!H-1k5HDZL_>~+v<`8o)jwr=LN}!ysNYi~L}E9tbzjKGfZ^l2jTVanZHdY%Ie*zFx#=?kQAV2R#MB~Q9M8F3=Cg^-&oa{yFfq6wFeBbMR1>iDON>!n@F`6P=Jt$Anm^d)FT42jJxX5_5`A~6Jj7N*lo$>;!4e;Y!VK#KDnviC`XWj4iZz^$Yk#&Hva);>veI?35F<oNTJI!6tqss!UirB_ltJ}3oL0IQrC;vhH=MuJy5C<{vsY!+XsaQm^vD%z=@K<n$2qTa7-fslLY>>ye{p=ax;;sKlSlybve*Qg0OE8uRQAaAZ7xa4#61Gn8b$u4=OhoiJCTf}Py(b9*NI}pIz!Vo9X)l!wLLA02t#8ZB2v1%-#1}UHT`)M<F>^()HQgT!*>4Qm`*7{H+(>uNikUeyI)^_;rCE@54JQl-}g&J=8wz&0Z11(t(GK4rA*&PTj*mrQ2~tXRSn~qp+x$2sBUZ!J`AngT|iZV^cz%yw$;YrMm#4jg0@bi3q%^x4k)(`ZS*Y3HNt&ajCk7?T?|8p9?8FoYnJljpK;M}KaA&O`|lOrALP3avesWw;jh!g*<C9s1P*^hQ4QdXd$%%Pg-9GwO_fTyRU;E%akRLKz8{wSm@QL{{Sd3ja)&iu^24$i1szr;B<2sfiSrdsL2ni+51R=n!)<i}OBF-XPeL+vo@5|13W;psI$H0Sw}fWQsjyz3jJ^*u1K48h;o?HwCv|+h<kC3kHiYuGx{yyYrvrvMCJY6~sxD_tG4R@&$9|l27M+}_1+w5tmS6}|kF&yPI8g6Nu7&B~o}vt9PwXO-(m|FkLovVypYtcYb2?oT#!o9vc~B;p6&PHTx&&ErBI=9`bRI&gRG}`xb{y8bih2JiVpSG0tN;Q<9g%H99sst-kZ<8xXCG(W_7-5r4y)Ff4B-on!@&>}6+a{cC5zLZr({iGV%g@-?18!|cvux5s}Oxa_{EHei|$qPMnh0Y<sXu?-*J5FRA#w09n7*-P9fDR5PLJ|6Wd&mLLovax`$0Mar)o>D7-(zv}P#^@sEa$6haWJ8#9dU#|${)|AlG}xdlk9M&uDW8H7b?<<uUn=Y8RcOaLs#y%+{$WO{O%6>o;KVw`H)Rbd@wpU;@`g8Q0YU|_^H#k3AMN+$Uzg53I%KKTK0&Py#7vJn;?=d3bhpO{7okqS|eK=l>o6L~U%REDC)Hd-aXo##C&>JmG^vZ7=>Q3CIwUykud*lQ>!g-)zzNwkQpym#zi3y}#;CL;>a)npj02#!pD9e)VVlB>o#_hHBZF(exj#64%4fv16&HlL4=3eY+IUxt}n!lQaKEm0B@hfk!kBsx+;8$NbO`qWM8;fIW2!17=qd#b+=FxS0KYe)#V(6^PU9NBvfktLmXU>RlMNvWjAdnzKg!w1d4n5X(X38VltyAD*@&;f<%_H_!gtRko<CVVynBcViGYkO!hPni=umPOWf50VyF@wye-zpAg`a0$EAaK9(Y-B409JJ#MA87@sl2Uf8&oQ#5s51B_xajj`6WikM99G!(edhb#dO;R&U_V~e>58D)F=|=gss{2BI0=GSyw;A-$Lzv?F`x98xaETsjPB-C&?>_V7qp+n(nDHokzgGn(V)`tuKLc*9sQY$MyQ(S2us&Gs$daA7NjuG;$Am7H7$aLlp}Ub$EJ#%cXPaFLLvJn_FOP#%M_(b(P0Tb08=6KvNL+&xRwe@7nDd3TL!qxh4jGeJ4%HMA=37^1I}~yp@|nz>HZPuGLTot$>MIo%!~$GOIJjL^(cGaK<a`V-n23890c)okC&WTVnT<_oY(4`sTMi$W2oFsTRi^C_B%5|}$auC}uNSpDg!!W`AU8<T9GE*U)ud}}JJhxiL$k;M7OhHS;w^|75cP!^3RMkzP(uQ~qmog@TggfY4~6oEJ+c;fRYs*0h}@`Lc8+2@6e=9iId(!fGscLkh5U&7q0LwQ2XS~Ca;Jh?n=$czfnIrZdETZS&TtB5*e5crSy5Vg(zji!bdCyz4||Td^^gI{Dv@WqA`OMiM<&Cnvt1b;#09-$J=dX~WZ2X5nlN22jrj=uH`di(w$-2ip&3F$tJmPb*0x%?)DuCP!_C)u=*?*HuBLGpp}WX#`3|o{aF#}HzxmF*dkDHlzKTd4lvvb-kshvXybd$>V$;AX2PEeyLSB^CbvcCs5Ol!@O)V)YHwlce*9$WedJlMIX)Z><pt|8XuRrI<P+Rxh{BBhJWF`TLm+fSKSuogos+2B`r^#RvR~d{uQJQ+zR<$}&*Bq9Fr2^Aa9aZWfCefMxk~d+JzgL5$XX=V>;6)*AbCL_FOK?gu8*;_dPzc=6TA1K)QJtH(J&RgKFcji8-0*?$qv=a+AS=d1wGM`RmlU!!jQdLavR;M6T#bgpI?AEikTv#H+?xUhH1>n!TV|B|fou~nk#3NwQ|WZtz`JeWQv~GMXpgi^2x=geN+nhjvyOQ_W8}2^djOo2e^@q;rILFHm=egVV)hV=E{6*~gc^_#ck6VnM*;?stB;1ELite!LUeiy<*{rQGPLJ#kVAAoJO}$2x|)6(O!QX6?bj(?zyE%H9F>9lGL8K<onF;?=1Q?>()nhr63ZM;V^D>krJabde(STV1HPN~SSNGNhEFnEpiC=lZa5561;TYZBmrKc<iGBEBMnpkaT(?sJ`=6=QDfhr>fBF`7#USR>KT?g0tS!NB84=ww^-OMlQh{TG+v(2;DwY?@J{MdVVCE)k4;4lqsi?A${``h!N6drxh74&jZu{jB~Vqg;NVhGp#+NGK6DtPqMX2e#3^hXvQliC!F6;ma#cFIOcHA&g61#CIDzvq<dAXND!@KpIW0pi5x*wTE>;1)<M;A7sw&p(Du`h+7SX`GlhVy*NAV`McytQh$IPz<b>KY2@eNacW9CxA<1iH7=1eMc;YkUXR0Ph<5=Ci=`_vAA!n>N|8J8su=J2fLc|#%Z#28$`ipD2}6Lcgs-L<T>HG-{QFNk$Ujd&^|d?k8;pgSft*51zooe?s*HhpgJG{Cy6fQ_3Yw`Zr2mD117jSJ<HE^17IF7BxZPRfQv7E)8T7AfSeWc0F7CtXdehdn5ZnH@E@;RzZ(a_bRs`PhMCa|tx9j(_&KOr00Y23iL-VNk6Q;DKm2#cU)|<JK+A68@MdLyrpA!0kP_7+)cfwNJ{UW$_xU23kMl*VHF=OT|s0y8r+n;Pdakz{)iWmSb<^Sr<nR-5S~nJgu<f54llHAW$YriG1=#2Lz)8gAa>z#f~D5!p2!9(%dC<WWYW%J?6kGuMNTHUa^O&x@M*~4mdbu@#V=3x_z(+C}-fFWJpcvH?XNF*$fCbTwVtMv!&H<9iHLeQDf72%H21Fl>qu&3GTFqor0B~b?XVQ^H^z)RmbpJsCBqYremevblVnWg-K;ES3um$iQ`SnrS4h^s<}0khSxD9@1&(kSe2j70EgSNCt!N@LfgX<$}Y<kAy#wDz$CYd!XApHOL@3;Rq{6(md%~$LbQsSirDEi09dxOUeY(!+kF`_cM!DU^;?D@#f~b&EYn2GLaz!dzj$dhEG{QCzXPjLym0ano#g&watb9p%;>uGvx|Y@>)KVW5Ls<+alg+ydA;to6A3dj3eid3pE%jGT1jVcs?~7D3y)tTbm$y<bH^{%u{41Z`+a1GsF;TXH&3TntrKeXvJ@sLOXxgq!`DGkY#j?hC^|w`G)20s@cgScu3pzh(;sUhKNdn8yetgNKu8U%U_&L^LY3|!ANI=<{rdWOcTtQmQ?mY8gup}rXF#AzbWs}%xhM9L*szNc&RDrhtidr}X1#Ak5SLj`ndxGMS<l#C+Kl0TQ-^`)4T1_sld0>uvMmB{#It>fY~RgA-yW{&bk#GsU`afjItba!bebG9g-bB`n96SCab1Z%`Y7TAAD=!m=s+jP^XVPwYNcrC!2xA=S#5oN3cU&h1V|$#*s)SYcD&ay3hypc%%T1cMXv*dWgXs_cm=k<Y-9AQnhI4sO}B?BdCBn5b7$X}B@?Kj5sEvZD73AkrcmOOX7+RBJJX3Bz^xK(ziDOXNw&{@!s`T<u<z3py?~M{!iqG5&3Yecd(kC<{1RgPj~D>-a7y`X6p~Xl?q0++3f_o}Bch8pO_=fmR-)ThBCP-Q(>mdmK>ZLJ0L4#9+tsprWrcT&1c}|r-{bw!7Dc%vrP0%mxolf@R%LkwR;H&Erj6~O`W>Noi`brAWURbjsIKbHkeQ=gQOv{#DQmzUGrwl7WfNYuF;D84ss1cU_yV`J{1!O3vs&YvaQt-*Kssip|Ik?IPDye`5vY<AOZHo-jD;RljffF~x@Z_3D9I@u7RIj8dt&nr3l`_eT>L>Ur*s{<R<++;7q-xZL-}PFuaJ?Wu9L-c>Cs~9USO00Tmj6duQYq6lEiX;bnc?b4{{<<ZPCH&6bRU$8^u_qGo*t+df*ulW~$-yq*xWTSKif$nN^|}_}C@zYDNK0_w&15s{yJ|u!;xKjDQ;y6IiN>A6JADRnaSxvvRHhaFb-j>G4hKRQXF4DG~X4%McpP)DF$tTv|B?jgBF3$&2@MhxEJ?_XST~w*OGKie3fQ-C-NV$~|2mC!tprJx`G{L*b{qvEP??s5EwFvr#4&UkJP|Hh+5-qE-mdG-_NFh~=AsP7P1rkvfsFpJeeL3cuLKXaR&%z7>KPax-j$j^3*xEEg4LoNo!@Hm&okai!m6i9Mr-i_E)!cvJmpxuQ?&{h@Uk$3Z2?Q-?|Hds_nB>{)3Xq^;eCJ~fpUoivRZ7vTD5Am&0{fOtUh&HL4I{Pqz(nz#nm7@>^&1?`?$UAV{Prd}3X-_mr3$a<6Ng%v5OQIyv~RK;;lq$C1RKvOh|64hErTa<i-Fnplc58f%@waH;^Y4F>@Ub-4dYN#o{I*o5P<#wRJ`3=OGNRv!Z?z=uz(y3mr@O9q3j=4eC`2CZ6B)^EiIQ$}QcS<?3$2sj!)UucdYgxu^zG1-`^dG+a_4OCW->_fYe;EF$bT3VRrf6f|zV|lQN#QhRv>yUhczE-aZH0+J&t94f_$uu-#U;^RTh;Q=g%Oo>)2jV6H5WB2#!^6R-S2jH|AN<;mP`5)K2UEKcArq8H1htTQPEB$sl_DmA;$Usx%8GFaK*hpe|y8OGpCO26!PF|D8RJbRu-b6#2R?f+$AK?lXARcKfnI;>GP}k;X@Ot`B2nw{qgl@a(@Nxs<{K#<<Gp~)Qyw1a1+F?{0=zpx3JpfBA#1rXbIjP^p#S|nppgeq)l@$>&a*M-{js5GFWP#5;rm}J;HKjSn7}A6kbdUx8oms-E%F>?n`bxOY4x>9}epW%vb-jFaH$yDa4iEC#m18`#2i=3+xCHPX$l%ALZsrt@d26nq`-a{7g#E{XuekG4A<`>IuIE9bf)@`}Hq3eGoZ6Pg3h`VVizP%DuPIgDGIns)~5i&vkX>85)$qnwsGf7oO}gc%vsk9;Rw_3B8_$Q82x5N7H}&^z(OjvHVXz|M1hNH`9H+g^2sM3qzxdzUG`I7I56H=<7fea^k^ELSOzbzyI*#cYphG=0E>#0;I>_%(Y>EZL^W$s9R&})tl{cN7+A(yX0`qY*$F28A6T1%`5x5IZ@j0{w=#m#dqX;p-}F(17sp_BpbVX*8;TE+~8kFwZQ7w!yl!lCWhPW=(t;ac(SSJPE$yu+tmdivzYje4AEqBd?OuuS#u%M{U^fAT=;Vx$rv9OWL`whA8JC_u210a%GNqgy2?yNQG=XF+=fGY0zcCOT0d`5Y3pLHojW<Wcg_7d{_U^V>o1SRm@YZ5Oi%x3=>megG&L$yS!ghmYopo}*<;cM1vqFnneVDwfKTq~I+R3>d@U?p+Z(l+`a0lv&-_A;Mw(xX{zxoT>A7+*^je#Slg{e>5WJtsSR77C+MpY68e!!nVFROe1n#MU7vgrd+Q_@`-U^%2JAAMAn$!D&hc=^en9G`1o@i+%y(h1CGVJ|<#;o$kk3QQvNWC{b@0sdWOcY*<#|>{v)nid*)gCX}(?KsN5Io#%5$C325!p^UYv)SUfz@nlR<oAM20p)&3v_Llp!-&`&TMitn%T&{#))N0tNaus8i1k0JIfqJ0R4tG=ARz0-J`y6Q4#=rF6_~h>7LrmlNy8qiM(s95X>kf>j>tG024$)JgD>0W%NYNOZ}=aju=I|{Y@(5c_rOL%XN~)D5K`DO(C*d*Ia{9#J%M)@N2)VP@BQ??Ml~34mOLRSy1BoonslSqp5&3yzrYnm`5)wj0H3?(%Z&;jm(~Q+pq@cxZh<Jc=&04JWx&zz%!@&5g7anN7^Vbu|-!)F6qoD_tc3IR6IL${-->0$!eh3c)Xft-)v@eaOmx@>cU4y`u(iIGI?Ct+=QaFQiBP-V`rw0nHjPFJhqpMnip`KDM}Nf|A-<&v*zt3dZ1LrIap<D{c+m;R=3^uBCEesE|tNyLZ4Pl!Q2g?6H#P0gs)L^6y!lOYu%sdvB}FE)3ot*L_-AY@bY4WpIKW4?pB4NMk)e&$Oj5SAXWH2T1VEUz395^T$IM|+F53nSjhulzc~*B=siVf#3b6{BA;-Mgb)@yP?^UNdmGa45#EU}Wg$%DH7w{pY$EE0m}o5PYz!)l9JX|A3c&N*Cep#-a+f-G0e%PYa@Ik0XP^O#Q@DY6Ko0T}Bgce(+eE2y_WAk>`ej*1bJ6#Hke8X@9!hbQ11Pl3nCOh~yn@rV2@@$WelNe-W171nb(hI!#c6GYoz=!#s@CO2Q6vlBv}jtR*lllSA)yM!%@WKY_@_CNI4j<^(W?{+XviHAI0Gom>=rB8Hgy?m&zC1bNqXSqm2F$u3n0aRpxeOpw?tbbe^t9+cvLwOwKXa|cdy1Bm}W1VCTk*8qle%(9%@5v(bHmj6ysuTx7GoUdMgwznn=Y#Jvr)`rPb#cb9DFuZ7XPp--up31x~eYgl=-9EfhpaTX-HHRz*czwn{>H%jtwYl%rRHwPGXDRFQYG#$70jg7-75J_09>8af$MaG7?YRtr<urCnp}ih1eVwiDzq*h+-&I$g9JoxCmNKFL9H!^_}cA%F?2W|HOP%%+zOKt4xFqxH=q?8C^2s~T0pi?qOKMqRMqq6X0_3L!QZCRhhK>4S956Qqo3UA;2SB4&Octd7nJRfqde7|tx|@ei#-4WFAw+CtB~r-JwX^7pEx^TPPPN$a^wiIkhx?j4V*%@f~qgE|2(V5Pim<lPy{zWP;MMF=ddm)p&q85-(|OnP8~ai+9;f*u;wYZcm!FbTbNxMM<xho(A-)IgvVRt6Sel#`mTiy9g+cN#R?q3<FX=bRrWNJ>y&%eo6-0}|eLzsL_>AQ{DlrvqGREovXZMqoD1_Ve$vC<==0Uxg1i_-xwe4gCW8p4%<9lZ%qqKiBr#1RJ3XmKg|dsfK=ofM!vSUYHJHPc;#eF|;yZk3e0%*~B?u9k+xjk0)lFCmDv70B3vQn#C~ddU7#vNI3L0olsqY-NTRBDq(bN!b+}Ut)tL=i;jjN0noh<_1o9iUobTapM6t9@mLR3ycZO0K~}zVE01}0DN2;OWw}U<(wZnEqOJoKP*PG%4#v!VJo$7baiC!)yxFgpFL*CNX$jC;D1fP`rYM?VhG^?dRpwTj_kLFe=bKp6Q8joBsqTV5t5K#`f_wuoKGap{F-MA!9v4fVKt#U;<Q2jmVCNh!yv?+Eq_I$hAuNwbBP*cv7*mJavCG$e)P0exHCD?r=FK4b1iu4$izq9cmm!B^90+5-jl45m4If4U3aIl8_$;dWdlxTSr!*#V9#K`RSLUaIS%^|=y;(2cHOhbiM_YhS`QGu>=9iF-*_^_0mgx@mMY53#ZOnUW!1u$j$OSuyjT6y>gEUX^do^mkthRkuM-(hWs49}kR43{uh-@vXAx>H3)SM}bKXsyfbT(z8Q!CFvKI4%E^X?%hL<-ue(=82P+PQ-h8g1CDDs~@*!=<MH5^RPWYxCr+lO~<8j(X4=HAGLU1LAoxy;3!<!W7deGe>#D4KO;}m{{#PCXarq>QF00PSKFbuhP9($35%H=;qQ&1Wl}XpZD&S0Se)KFS=j?xYHP?Qx4mitOGN!LaBv&&LPp4iY3zb2U(~>&z$ut7CTIe!hw-RhufEcQc;Mxl?(i`^-|H}p>k>DsdRcbsgN0nhfIveCi;Nw=yWY;MHX7jy=j&DC+$2`*gP0Fd(omZUu+au+(ffTwzyi&n2Hj*qt&}ZYHcE`emv0{vYqEYo53_MNqz7kVx<I{BF+zL?F9}n+?JePE>$G+j4)-?O!jRc-K7uKG9+Mw#-r*vaWouK*L`=1P{lB`felq*;U;;$Q_pR88Rf_fP!jDhi0G|i1XI3P41AIuDaev|VP98NdDqke*pFqyt<hEPE=!$Q2D_H!U!fHO1@!hl+=h2D9iqI#;qscEdyjWbS96b_<aXxM2J2v>i_+fGwB-|W*%K<mT_dm{Y|IUUU#iIIa_7K+#>$ErQC0$#|7jvWV60V|usW(ocRmzC?3!6Ej#L$ah(J$_$aT%47D&?SKG=&=P{33l)mCt-MB!>4k7KrgSa>PVrm3h@(eXeQ%x2R)_pV9X(A#L}%z)V`qBWyVZnJAUIn@@_bb-{NR`(ev%iIdD7k`=i>dJKDh_i%eqC^jdM8w*MJpLpDWr4VjPe!ZRuXR3=<`a5<rNfEdBiHi=hhYl36M+5a4Qtp52+ISzqM|wMSs=G<vd)j(LRMJC=tU&$TWX80LBQ&+YEizdnctP^rFo^RO5rj-B1P3Qu|y_^$zEp*I0`G*KEodAp<oI@_T&iNbhqHN>ts!(gn)&wo2{cllH1Vfl2GjKmV~3&@~)#9D)h9H(5#CJfZ>cdlHW(@{ofOY?Yc0Cg57gnlHZV3+Z{5JNek;%=#U<P{#VyU4LN|8GJQ!Yu`VbIjL28sL8}7L5n=)TWelSp*QG1|(RB2TTrX#8{Y8dpQb8PT%XWpWb4LlOqmyY=a9->NMEAfYn%T>!F9i_S#nRqJzhDkDF@^Ap<&yXkl-u80N8Uv!Gg-FXut1ELsNqa#P9J8`ZL{cQz#gJ&>c+%9dVp;Vl5L=iL+E4`Kv<ptI`%;OFbh+mI>aynDz)PjHgtUgtfW{fxWqD7pQexQth9`10?;QTw&JJ87<qIZ<dU-7r~zeK^Nf1>hx0#NDh(HUWE5iub`&}yF6*m{i?T_39M%jW5oNo0r?rTo%>(f?;M04(=3?oh@HsNwL{0-ne?Hqt$TkmsrSbY|$S;9jxf^<e(M5Cue0h>SPkON@z$xW}HL89usnMg>Oj=Z%XHWqvhDpx%vyM%)sMd!o!N!L=R?!1lp-N310*5o!4U5bf10M;kwpv-+j;<`o%~B4o-+#Y~L_ZO$7#lU>H3DP-vFaMO9Vfw`2TDw-+RP&av`)Cyokl=?Giq{vs6OPrS-W6I2Wae0HOmD1XRDwO2gTqMTs3SRWnVE$prT{hS4>*g`gmYuL-<@gJcwX)5iKipEZkfK826YF3){T|``ILX9+p><)_IcsUEnVSedA>LEisF~x|Cc-qAMzG;TCx7Efrx|BPT+>M8L}#{-PH)-4wP;&g!8wh8Oc#dzvm4dB<WmuBx#>Q6Gh*vyQb%RQPCZqpazNpq7f7A94blu}p1@v+dXRyC1&y?_$NkMea6>1g1_d(m;oBKOIupP;d2w0x4w)i=x)RtZD=yh4$zYo-_?H4GNx2@FBn%xPS58udlyQsr;tb7x|@B6&kj6AN8^-bee@@5Ol(DFPcy;nfmLX6=0<!<HKiQ&~wr_YAl(jg_LFl>tGkXW!Kdg*%Z|heLGSg`B`s)rj=>hLuXNSlI@nq-9V<|zV>%^=7BkG$X|*2>}cgK#E~q9ODEjwmx@|HR3pz6(Ohz>a^2k3AT$b-31g0N^`AY{GiQ(b*i8F0Y^DHdit<v19EB3eqP8{1Es`zbnoBiob2pq(7Oj1x@PmRy!o1;%mG6JZ7jcy$_BoTi4Aadx5N1R{!GD-f^>~YQyQ3QyU@F48E{O_K(Zfn~R;yd-<)XH1P6Ve>&eew5z#Vk`w53U`GqYQJHCg+0UA}7+Y%ht2)OuV5J4|^DH;-ix2Hff8E!@}A83Q~cA7<aq)@v-iEF7Pp6(1o6jN0zpR~T?giM(|ZL%wk|<dM@l1}+08d7%X{mbq)o7`olP>wJ*Js`oTlELks0E3G~Bz@xcG!jF<r4(-m6;i9DOyg4Xx2!{}K!SKu1{iDPc0ggArmaJQrpc3LnMx<5A(ZZdWw9#KKsj>)0)hV#4*}W<VPD&sJN&<Z$$Z3CRWYmBmw@d`BvSnv&B>q0_-ge<0w<)(zJ3_&6Mo?7LI8VmwF9+aqyW!UF@<)1qRW8eYUAo{z^3n#Y3BFfvYXkg?*8C|R%Hh+bRVbFsTjO<c`qW)O(6lXI5|QDo%s*ANQbD)${9pVfUYABM8Y1=ONKi2nA16X5S~1qMR$z=Y;$?;rz8++%5@<3g)zm#22tRviCUt3`uKy19S<;&INo(Nrq-eUHdi>Ha&a$oxG$)krKLCO3FI9z640NQJ+xyF$7pO@H{O^I=?Qv@wl`AUY8EU1T)(vVMVyjj@flr4FF7|V7g#;K_SFJI^`qu~L;t>EthFu=FX)}UYt_KmFNS|Oz;SeHwu-H?bzy*aCIOr8EH4N#+^1kCeiJh`;+nzZAJ2Fxps9g(59;(`|+g>Uz#Oo!o9(FvcxsxHb-nUJi-9>J!2Oj8L%8+%{x1FxNBXO>H|2ueys5Q7yRNsd9C@W=yA`u}R8mUNt1ztk1@ay45qgF%+gF*&TBn#a*8_ZE?gXo10)}bb%ATq{D1by%G`0_V?eYGz5=hvS;eSVev(V|b%@w;!{QTdba9`G_5Kz~{Kz%Rzm?=(~Aw~#|gDgo2lk~={x+SvOKvR?IDRzpAvx|8ygyD;P<-2LvH0A)ZU2y#?@Kp?|j?ODD-Ur4S1{ErEpk>js+P1V8M=5AC&fXxwC?{VS7f)1hQ3~kqAUyDMv<+Pj->1v%-pN#mceJAwzq!P|T&q2E6l3*kl_gqu^6mU0)4uO3RDTKWaa>*-nA?k}>8-MhMf}E`1y`V27R)}sFUR+|iH=@!<6z9Mgn~yqn74{t2SWSrnFVg9Iy>%BnZE(NvgXV=YEPIusQ}%tQo)!B3$a(;}vV#C(6k08k;3DJ~M4T1cMK0)7K-PYEu0A8xcxLrsFw!K-CkhDGj|q+4j9wI%j}EB=;BEkhHL0fp-u0~TkY2jk+&kq<wKlxk{JcUlh8!HuyrEJ^(Jh^8`LGUrdG6!GXq>E-5uc@dVGS2q0mHuFl}SDK5pk==)cdPYoRK1&@JZBEd40jwY+*=W2+@$3$LF@nPo2PC096wl4Tnfnp;{9j6d;k|ju4!B8>LdzM0-&T)vib*uQTmWH%Cyqzf;>wwGk<(QKc%51*f>INWR61B%At<SEW=ixBSB}{zF4kr8-VRutdeDSlU|D^N?#v1#uH2|57aUx-Ro6T@xtZ!4lX;2!)lP>%rSPnWbhj7R=IGxPa@^ji1L$g>p%pY7-*qFs18{xvA7NNwBb4^MGt&`>{-NokN>v*C$5p*9tJAa57pSyBghxlrTn6*;=8ab{~A7Q+y!#F3z-0R;fC=mf#fVJvtFPL$4#JCqTeO6e%A^sMKPzux)l=-`A{!%yw-jM15p(g{Ww0Ox;D<m{+%vOwLI8+$cPVbd#zTL$XI$7c0<9$6^>q#t)o>J7pSTKZbKp+0v7ll1@!3glyI{HMNQsz=ep4IsqeGA;E>3>;04{qzqC<9Dj+3+`<()b-M70Zt4&%bW%BzkT|oaZPojn?Qs7=uP`CJ%NWMk#;(7(q&bnQo1(F3+5K1u`GAT)zXdwujwzCEicwEV4HPn5yUdk%eo==Z`}2j$&w5!yP7j!8o9jAR-=0Td{A}LOw5U}K1)Jz4nC*yvRMD%oRy1Fp0q-;)1@FueDjjIDjv0K%{|nWn2S(!OSZ8ojy|$lQxf0WJ!f4CgT=U&<S=K>!r$nc$W9B7AXs5}zb#OoT`apd#2uE;A)?@M>7ckx-I4nM_kpM{u2PL38ljbv4M;Vsk7P3D!y~B0x0nH6A0>@aM(deTu<bI-*4wr_*(rQxMkC0>p%xq2sV9p8yP?$TLseGw>K$cV|HU=#CM@iH?FE6L?SZrsY&<4_kq9SyG*HzJOEPRjbCM*&BOl~O~Ai#qWGPGm}+6T9mND&~=skStPsN6`#$UN;x^=?`+Mg3_iQc%-Do|mwBSu+~Y<-T3HT6_;4Mbw|GD_n*80bld42=FEE(;Dh-v{>9Ux&VDl865dhR^w(ZY;Tc#)2*UAq4UUvazBck6kDu_F$SOj?^!GKeE{jeZ=6I^DX?J6g^f5c!}_;j*ob!y@0ai~7qc;rSxJ4hK!YXe6&x;MXENGKvxe7R0d{yNdI%+efW>pkqMP49TkJmWymN==pjXxC<~76~3gsVEZiWs@AH9uwK1U__NDpN($aRiUKkR5!`+sL>mhgrA99rp(1C?wj)OXUz)}ai{5^cukB3(nF2gCeHseUO9-FPs_P^gW_>_gTXF#zu~x|H|<A1+I^0EP2xooRyL{*=JJ9~zm|%KEQBXFLPxySfH!4g-C}ho+L*nz0(sJ9EozbRswrL)u@o_l>M&w~Fl>dH+=1VIP_tI>kyPq)l;>SNIm&#L&R=Q!BIIZW}ab+Ga)FTF}M-!41-jS2<`PEF2194trye22m;fVn*<<tADXN0$iANXxmD~O-?_NE5`2My4&Tovgg*&MitwfLIy&{ZA@X7;T9J1$deeWk!@?0;eALB563iJcc+!r=iI6n^aGLGEOn$X;Fc*08@FAU&w0N#nE8P8?$9nWeHy(4B3-{ad+XguE4!;AV>=Y0GAyCJ3;GZ(pVqt5#Hrx(ca3}#5oWL53a_IEP1X9fokN$q{HcSKipWoh>C0{PhOWyAO9VaW0V}e)LGL=iUdP}P?c~BGXDm%`sF~zAO3sjkC95XM>rZW)KdL?)Qx8<iNTb)bv>ULv_1WwiO}A?-b)hQE!<C<PQHZlfO{90U$a8;jEZYQ@gsoGcNM;uJy$)2rF_cST_4gKZI@twH(698v$fT+Y*GNyW8A-;1RR}pZX5S{-Me>tK1wn}ZfFQ(uU-K?u^PntyAC6-zf<OM|zE_K(H@rI3KcQvvtd#I}O{))htm7dmbAsFORaE3f;gfy6!-bzXu25*6FnNaulXnfbfq{fXm6%8oT|eD6@<{Lm6}|g$v?}vKc<o`Et05FIxsh&;vh)u)FJ)?2ey(!jB{x#@&vm01#1@|8u<*ZW0p9jL!y(i^g_+MTrEI`)(>U*$VqJTv$$iGnIrWAU$y;Sw?vCB7vWB63V$ySX0@{Puxk^tIT&f|~<9BDB)fvQ?&Jgj$ndnS_X3?-*`VFD!+d7S?J_{A>`8y%En@kUQyMl-DwCuefeX(q=TP|hawPC8j`%FrK=RI|BKlj89vzm8yI?$-37s5fr@$=id2zEk~eZx|hd*+d4B$Q_M7C0|SUHEN6<K+oGHwcRtU1LgVL9C@Vj7>$UjmdHaCH8ucHg*$vyraXrtT&b%##R>XM5<N!t`xjAgxcNp2%LE@{n)A6gi%k3J+Oo0a|-S=ESv65{|t>n7B+zwk<)ec8sVW3ISCU88pIKRg3%+CfYV%7<`_Nw3@pB17cun5f-jh<%ZQ8cYvJfPypNgR3hKalq~%+o{0_}!W%^+#Tmf66T?eEAa6%l6v(P{R5nqkgm7Dy@Rbq)*i|tHI7rDx!igY3B39HRFg=n@=O7YJ?g!@E~OVE>*0E+urC^y({a&7vQ;AsS4Bl8tp;;20-g@%fLQi4hV(u9KPIZ^TI_mv(z1)iZ$QQ>^|D#6Ym*(X+Du;*hDaIKxO4JTS^ro~Cc<%<L*ytxEo<V>66@=;8tQjNutl7NUXMR6pB(bko(5dK(%l#O{@%nJvmvJ?G-hTw=+2n{yTP3VG446B(!XMoa_taP5IvB1Mr6$aa~{j;t?8agvfIPaO&8AjIy8Uh7BlRe^T?v0?Av|s!>nXp7G@HC)iEi|2){zSvvB`WU0#wS;r#S}6p+z*WAUNN1jf;%Pw40uY&;mu8D&<%%0NVyI2D%xu*665IP;ywoRDBoK_u&Z}`Id*wn63l^h>w*H3c~Xqi28vPxY2v>#>+n+U^Q>E+jOma&jB-_YEzdgOB}zy~jnMEcY(Y_&VV7=SW+=<0?iPbLsYVt+$dwCFxbwKT7~Lk)B&?`Rp{#$*IpUuE*r-(nt@rLSn^UV+w})?_){2J66z`VEec+ca<xN%Ax87u^mr37%(f7Iqxle8kH0-2+4NFV5c?#JUVl2V^1Py-umMJ9z)^JleSuxhG&TSNA5WEB+^s&&CG{vdnWmLVbWs-Xa$Z4GL{EKRYHMOiw0|2fUKNEh0Q|_xW%R(fm_m9x(FI77)G^Mku)bkb!FOlXd<6>!yt$<FL*gmTeKKZEEc;QjLQdIPU%GFQNx;80{b%>45m_<Mo>o3F6FRcxz>70|AvX6JQ+x%O-8j4DBNRna!M=sf8XDl>e=-^q{LK;XsgZp(KZm(-z>7EUdC5qdlI;D*c1U6oVOkWRbCY4YaZ^<JUO;KNZEOc$ms}C<{Io{``GcNBE?8YQNgEqU%#EEIK6iu<O1Do|e3qgF#x<crUNJNN~5%D$~xgX{*uqPrkJO454p`r*RAQr{;8ERBKHWz)@n1`F`LBWD*7)nR^H#WZ}M=athM1CJD7#w&_A=rExhnzP?6OEt%Fw*=ntZIQ3fU#bTchrk$jW^eCGw*7(aM;NNN{n1ECv2R`HcuCD57c@o2NQU8t|4=+taaFeXK?e+j@UWef=>a8whnGgyhqz#wunnrInXJEg$)h3L??bqUTqvJ*c}4Qzv9GP`a6*n8JlI;ACykufK!$km7AvB-~xAoCf?XAVfULUdT;FssNzoRbUAyP+R#s+uLU^jL8{r6B$hALwmI#PMm)CQG08YZIv(T7{D8ISJe~2e4U6Xeyk2-!aLAOk>6Kog0&!})TJm_Ha3yvV&-U9}NBu<E*YPRbu(2J~bP~r9^nTN+-f}Yojn5)ursdJPBx8l}7x1%aKMLM<qXI?jw$V?zK+IJjvx<#EN^eyk?;MmE(HFax{zKJoOUOhm`Wy?%I3g4f<O7*d1|6{2uVs4?3dJ{BD1hgXkm38xkz|jSv5<cQ-k~VV1(2@Hlab>hj9shRd9M3aXzHQ1vWv}xbGw^SR7pp>sc2aSFiHW40p`<Js`4>OGYXTjxyy?3j|g#{#-KNu7rPwr!W)8w=yozzX@BW3mLBg0Y%D4Fv#)kwCqE}ZCvp#{VbUT^&3E;>EN}02m%#otH%WxwQZ(oYD-PA@=m;1iJ*vC+*;H|><uTNwi=MRH`QZW@zNoQ$F(gIl6ee0+RjNes!CmLXd4)P1BO5Tt3GykAm{!wz_X8y&h5g{0fQC4Rl6Lgsu|62xNYoffFMwPKb0r~c7d@l0E<J}*&*Z<zJcr5y#!iXe$;_#7z5ez&#W35wNlKrj-So#0Q8ogAR4h`_bY<jc>zDRnl3&B99w&-6-}co}Q{KRCiKCaaz%)eY!}*rLIcl9>6<B<uhdRw>0j3f~YIW2JK?q~y*Mqx|hZ>BxT2d_HCLWg8Id3B$^$JCaRsdae*X5#S`#!>{sVozxx$wBE-#@Q0vUEX@^YNSa`~Px3j1!mI8#5gix(_N#9;cAicf01>C5&oUg`DX9OL!HwXir+(FT8aZWa(-Y>tXYW)k%E2kv4MyW*A7Bg)IvkJ3VHc=Bixh-Rp=RbcNqPxom4lR09sb=yjqb9ev?c5B1N>T+Vjc`kzb%rHuD)RfSP>-AN_yvJ!2k=92HFX~)JGHusi{_b<2{7C20Ykq<(d!OF5;r&tKNybmL)O^W2n7?%YiZbS`tJ41tWnH=VC+e|l*U+()LQ^+f;A@2gTJyZM7fQiHz-InrrK0m+y^y%}f`QiO5xXg#V`t`@xpYf%pyx1!rWpOv+{*q5kri+OrWnUr9nLvvw_M-T<uo>kVKVvt@Wxn5z6fxf3ZLW)0zG>y+M0=sM?sOI$@6JE=HiSe!+v%6dQ+TWX5YONKoG)$lKl_qTkkq#SyHv6%vRm{Ajf-dY#cojX1#@1NJ^2$Zsno8_Y3(d;rRut3GhDd^>)3H0#<(M2{(krMPd9z=5Nc(1r=!-UpX&;#3AH1Ze`<zC)fCNTcEF|hIFVb({O#*4Q%Hk>uhqG1hOlVi@UhsHM!kcMF>TFok1`m|5QgJ_`Td6<zx&&lPyYP7)3E~{Jo{_gHCJ$SL=IIm^y)3}IO_HjaUUE>ciNmYx6-{CLbbo`Enc@@YjA7VwD=A<Q&BTjrlUqOB)dldgDC6AFR=LV@Y~eZq9ac^ZUK9VRZ$klq|gYr%LqUwF{2XkOAJiuo86cY@`z;eiAFK!iL65z;}d`kiKyR0c>wd{=<iy)9H*L<l4;dm@lG@HuE1?dP~g-PKSrH@T~v7zQc_|?&^xAVxXhn^{^6%jKd#r~-MXh%%^I<GFRmsVX+mrFaf+A$&eKDv$I)-FlpdhHHd8Nm5YD+%iJKVB$zF7xFGT^oW*TG;I3E!7W6EbyUv{0EzUPG;yn%-UQ@V+H2XGzLq9bfjVE<Yo*=A^t%3V{cqiX6>aPut65#9FL_kLTiIpkkcn|i;~z{^GX0cyT<GqqXIEvhZb3u47nmNN2%Nh8(5IZ)UtzyK#%lZZ235R)mQyfpKYpFaB*znJ`ODD)1A+P&t28Sh7v?6M1#(JxfLiW?p^OPhgO?7H?J#29E6q3W;nxw=TWl&d{?$;`B_h`AOH6YFJ>5iSkQG*c29*i9i9cm!uh+~~sm5SKBk9-&KBHAqfJ_MkH!^>2T@UVnK!Axl&SXmvv>^Jr>ioqMf;iLY~rJgx|p2fL*<>!Q@@b$EI+d!{xPwEFWOkIYJj`uk8{19{Zg%SDem<vri788^4RTvT(WE?F$QOkW??%Z2Yid#Ppb5v~jc<1ysp8FPDS^Hdq8v&t}?!cK(33x8QVxib?h&tvt%D2Q=FqV^K<9l!zsI}Pt-R!DXKd-o@SAg2Dx4$)NT?W&dFfurSHXvl&O7t3C9fgB!HlgTV*h)ROX(()W3wj{u$``(UkHbHH8mKy-l7qsezExZyix+PW(GeLWY0~^}t>vj!wwbTq(8}bmvB1o#y?bj>XRcsnv9ET*)sdg9Qx<0Hg=BKvX;)S{|QTHs`Y6Se0bA%XRyAHKeb8;RApXv$*MWfg+gApePdiFjtlw{K%%bJQyaSl(@uo*;zJ6T2u7_t9_t5FS>Z+u?Xr+qHm&^A-Pq)9DIVnVGJ!mtlz8MSKci?+SMxIXMFE{Mw6{EgVr>jYI}dmdUj|K<63zOQmW3*=?39kyOXd$?O^o<?W-<kW52Hc{YZ0jVg5=f~@(7W&0IF6*2Yz4XND3O-DS0Tp5Y(l#S$!+dez-IRh0;KMsrZ4sdWc2V37*4nzHfz>0J-*yS22L&Dz-nZv!ccYqEpy?Y+A|#0y#Ubp%U@Ah=9_p!x*<N0rf|%Vpuvt_z27!Jk3byyPia%2N>R>CEbE%k2OAq_$eWNl`$QPQZ7`k(@tls@j{r>g!w`*AWyghoMI7V7=PEpVsbjGa{h<b0#=2Z9H-(z0jE{KF&+kVKXWv3hHq$E{~@q@vR8Gd!7vg7?MzO6i%2#ivOc(@1+`d2#&R;FvmHeerrEkGFYFzrtTb3ng9{|HRXN))d3&$V8;+z_74p%Hu>GjzWN)JyaW?7%vwL|B1ld%%Z$BHXzi-|y~_+jLWdKbsBS)`v}O1oidnOh-909u%|tKrhU0nF(<sJT<@ZBBNT?y9W*fpO*Ew%_(1ZJ?v!WyV+x-a(66m5EkV7I}xx_i!VgdPaD$KfxVo8zA!?9MJn4d;DZF0gu@Q)YCy1YkePI>%Yz*1?c_DmEzrK~*mtgb8X{yqS7f_(M;)xBf(%lRWdU52@@I^Ov`%Xd=+HD@MWD6E;}W;8JQg0EoY}TvQ$%{Whp*t=T9LZ_<A(AZJ|CBu`dCF@+V*bJ-^Z*ha!58Pk9ozW6~M$arD~!`=Ph?<>}H}j*U4Xnml&B^*vnK@nTkkepq&N<R4GC|Us4-lo!yYG9KvkCH}HL*T&MGPZtM7QVKta0l+GmteBY&Dw=-NZ*M^-OD5#a>{hK_Iy7t<%Bbh?{)8Nu&8|8em^t_oqh!Ncu)OE2P7voR{jW@j%#uBzkv=5AMxWqdVZl-H?UD=@3=R$_wO1>?3k`d+1V5qye0Cym|%V_o|b8U5(QSM`EqhIz6*xiUNwksHAjA>{iR~DxOB+r9pyNm7>=v)>y+?tBzu4&I+fa7!Ty{?HmPWZyF7%2j8AOtK$f1cMQuXC8>E0c9`1nJDkW*pd|E7WAH6dt&aEl7=!?5NBjiw>;gU1&Vsr9|s=?N{3KCRcmb6@(mGO^Kp!`=;MRT6=xP#>-K^u1ydXNE}UDDKNOtnrz!9T8aQ9P7bE>T&8t^Lq&kjyLMc2tszxY)H@X2Sc63FK=J|*{QPu7MU|@hRZRoqby%Z(`$XyV^ABPdaTRHACB#r9I<oNR^_J@sdm)*0`a0D)+53?YAiyNSB^ye~t^AcP?91}N8(}9d(uBaK6O`M09adK(aqu8MI-X}?1$}}?ol+0o_Z{jAG6U<_150ID`!}GXkV-0b1$lurLL*G3=w27#TYFpe)7e&kR0k#ky%LEae|d{EzSgZ}znA;Qdg0=V3ORPEhyDzs(j6~@LeP&YPwOzrZR8?KAgsd0zvMY{L)i=TF)2@8#Dy|Rl`Ufc6o*i_kcQ=1A`Nx*UNs!rwNrUl5)<r=o&`CL&iE63oUut)<Xc~v(_&Z_(l(XKv>WcdPI}!~L5Or~U*97*)T_Cu;p60{Vv*E3y>6@{CP9ai4V8m50{CMupMrB?9SZ=xTwSIfb2^2w48cPOvX}-sWpF<V&0LVOPz212&(`)Ggv3!;lN9uVT-^vRP1=pK9783zq%8I9k+)QbsO<A|P+;lwete$K5%g^XGZ!<j-PGl!KUmGVqa!{>xs2U>h4^mjE8FM+z)mavC)8^p@GICM0rOig+`IW<m0MSB@0BUSEcBYT?|%3mn6JdM^6udIQqf@<pmfI}0VJQ9XA;6I^66l|q0u}V*L?&uRjS-k)?BiSUx-TaZ+ck2{jJagN;`!2JzG+D3Vai3gXKhV8xa??2Sni>fQkxMP3ATxd;yP}Ru0iEO{SnkZ{sSLK}W5kyl8mQm3f#dV&I-Ywnele^%<l>kxYYdz%yUBXJEzR_Q?G<^f`4<u`1a$Y&9Q=%Wk#DJ2GgWs7l`)uqBd#A+QPSD&=8P?01emtw**St0&f98dYseqp~r69Q_NK-g;)w%C@uX+&TpYLxwQY!t=OB26>xO_Sg)<y#e}5FSCGn%ALkB`h}fyvHF5}WerbOBZNP=IkN1c2-|Wl+gRoLb8^^i_>}@wkGFs;2x^|c{=&r}^Vr;JPqx2AjR9cQF~fvx3f5qTN-x`72irGye>8Yx@6Nl4fLGwI5y{=S*yVlUz+d%*qxz;*v0)~#;M|2i232|%U|<3wns7R8(vmvVQL0X0K~I|zjIx{|uTNw-cUF%QQ!@Hys_R@zGpg2-q0cOYR2-!|Hjl%P=nCxgtq^-rTcMy62qN9%V>h8~>NX)FB6}dEm}FLzc=|$-iE%P-lF~5eML~-qvhd6?X+sThCdC7sDevXBLAq22vW{|rh;?cE&@~a*%-GqrRxHub4ue|broIbhh%-_zhi`?18{5Ur*Zte~xb6#TUs`4FgZ-*5LOOtOff4?LA{AnGQ29Au1sJyItb_ymLcdB<7GX`;t@{}FK<Hu&bRFy{Zye=}+M9{iZZWd;I<O^yO>z*!b@{v;piH`F_)Oo2uw{Vtg-KVcR&tuz-WNJgAx%@1r()hNs~nSu9VI3;H9X%~pV4{!7UsG)uf6Z(EEdHdSuadQWGTg?>_d_#?R*$6uS2Y30jh^mBx#lSfHIR}=mF?TPL!)iI==6hnq;Rrr}#WGrDzL|+ckCstqROBYFQw5vWn6={;Mn2gzY*zda$s6For|{j_1Fl*a{~8Ts6J0y$hUL8%(X0iQQu69f6T<TG2+|D1$GkYxYAYlfZLAbv`D~^rC1o#cN%^O(n;7+2aO#+f#62q{64wT#3COH;{9kS*<2w(D63<ZcVunlT7Ug?t=dr;oLCgigTU5xFOAxV=DrI8<!#VgvY#2a858<ta~A_b6J~ScTsv85*1u;d%xO&0-|e#pT_dVU}SAwX$s>5GOC3ZujM?}ag<vMd$(lOwNF?&%-<VxZmS2qN-90!1_U%7t4z4gVNufLAtR4jQAVMJ+&2eOW<Nz}7Z92+-6;IbAb*x=2(awW{v+pY<bC{TGTyG(U>8L*9-chY3Ks1lY(DBCoHI>=(4#Q&)G$-1phY6B`c3wJ&M>81TN8tPo7sV_y=#g=qsaAlXrLefa-q_`k}kSk26Lx&F7cj?&`YMeCvN5*9JL5aiV}Dbrwg-8mQd*qaI9-<V1kvBXBt$K>v2k|x}%?$JPMX|Dd6MGFh0BNQM+iRVwDQ<fN?>*;zVh2UyyAnD^2Laf$g5_zN<LO_8J#Gnl&OF)*W!EgbJu4tLFF1m{6;ek}(mtHYv{rh8z`0b5;L{h>#Rx1ZP;FW3Dp^rN-`XGNn<9ofdt9vqp_2M>Q<C25_ZE8DUCFF4da%VE260LFiy?1H5FGkwr6p?GbT~X9pvk=_U=A?re)8N|i{I%JUxuyVO%~XGqn=_olJIlbaL{As?C7R&xfXfK+8!sc(_OB+P4+ogY%&LF$~N)T{@j4VPRU2yKAI&%3TZ7JBc)WvS+&V!vMRGe|33D1ZfX+C#zhwOAVyNwg?u@`jBIOV}I+er=Yzma1)Ktj6=aSx$!JOk?U?w@t3E>_09_Y*YA4lYm|aI#y)xxY92z=oZdh>|HcDNSC2=yLwC%85=hM-L3aR78_~`5f1ATFf?-}cZUH|PA~?Zk}g9pB*Ne4(Kc$|jgw`MEXu$}cKuDj{`_mKZ7X#Wc;!Gu7qc@r<y4LllBo=GVux1G?P$L1m~<AHsI!0YGpAsO#%kUYC<qJ1#{I*?V@KBsYp1Av6Vf+_VvA8A0)I(jSsbeIhIT$j!Y<y_kI7jKaYy7-qTbI_(3ZC%qP{bAU&?~zAKvHO=`uQ8LdmT!h?)(ntdC|pzg?HmJ+8}a-pH>Dw7sE_?af><;nPMH+{51n0Sy@btY&5?{UBOAt!05DIkJv)k=w}IV3bvO*_*zyW6cl><EC~$EN`U9WU$b_-x*TFgL0~(Gp2zRfvHGM<nar!4LZ~xht6eqnnE?$xOg?31J@E6`tfA<psOGcRRbiF%FUslbWQ-x+=lDE`I(*r<lcP!lB?WcT_J!Pp(KSM@(wnP`hDQTMb$e1!h01hDoA$PX~?1gMSGs=Ff_W2#~I#w`NeuXeQ5JK4hNTKc#dN`bV>1ss0dIkoa-G1J-78YM|KvPo^scA=v8r9R{i2DF|fj|aBJ^_9OSBNUXwsB^g|R!ezk(jv%N<J?>PgpO9Ha@9|DP5nzvw&=rF57N|7Ug)mjsTVWJPt`$b@Ptsp!H!f(+<AI%6`8hRQP4f&zax`wuN9};@$twn7=l}O<{Cu2X1vN#K4mjwI5;X+l2-kIJykFKuk9{0&8J?JKrq{;H@id!t5A$Ri%1nY4n<uHbiz^*lkNiL8k+X2=5Okb?~RTD-c#7ucDTJQCPIp3GHq}B5?JS7xotifBbM3irnt^K|ivn+a+hTYQyG>_;7%s*r`QR!e=`iAuwN@R3jutN4wbX>RY1b?G431Hd<m=ppQ18(HYF(aCb6Kt3`#@FAs^eM%$+D_v3Uu?qS^2W8L8#p;ddL~M7s2r~IhIHs(S;gp~SI$s~sY`+EDk1w($(l*df(3;por7FF@?B1?gd2}}fzwWF(61fImyFyuX%2fYQ9c~d4l?Vc7v!{nM1g;VX{?~GF~bz*>A;+d>ODWx6IAHB-E`zb;P3EuG0zuyf_O`vQUkxbOasfpk}dnT&yDOJ(!6-G@CV-TWp)RQwoQ0?JA4<LR=~rF7uhfEUx!;6lto!M3ckbOqEabonDzJ!)JPr|zWl!ueYamo`p)Z!1KQ6#BtQ#^oyf&a$rs@tmlJ4nUPPJJPh{N59A2Ns05?Z+p2EU})Igj{Yt*S+?lc2$L2w()I(>!qq)1#*tkITxYb}*|ovVNki@mav2VyWmUt=}wTMm>cJwvF%yZ0E%%~PZJSj|nB;PaQy{q=Qs7Zz<twrgYku`o*w+mOoVCv58B?mL@Nn+Z3MJsoDXIP8UIq}VpCqpZ;HqdI0sJKLgXCTr~!*Cw8xi#cjNP!L-u-0L?9)CQ;l5+ku=5>>lRFdn*S&<LsLu?(4eg%(sswFSUXRV=x3iZ86Lb68~m1apy&*OJClbiP;q>It}cnKG9ReaU(D1)tV}qaCSex!8t#s!{%UnbTL7sP7+ScF1K03<P{Dy4--k?XWConJv%xifCwqaA3SNNg7G(2fu-;8N}R}j!oxT9w$gw5lq@`Jvy~*E(E_RvxIU?81%FbZBiM$n6k4W59u*lmkSJTmN_pZW)G_zY;2NJ$=Kee`))4@Y$&A6;eW@yJSl8Pw6_?awD54p=2F+WLT<MLu1=k3n(4M{X4cgCN0i6TXv#rp0~>0q3!jsd!Me=&zDuTb*9^SNtTF2oX)DA6EfBr5(kc-*(X@JfKawz!i8J=+f<M~8E%D!RtM|Eio0n~pW4hRbxk$9H%kJmwMzdLLRq(-nB?#u!Z)PV5%!SW^4S3ca!I&Q)b>-3g!1v*`&B;gv)(<+wRJ*KCY{j}Q{F*`>+g6M>cEeExjm*K6V+r=-aX8jmS9hIk_YV+m0PE^$2EV$|Op-}3wu7jn8I{gU1)x2n6oeN!6KGCHF)u7g9otb(Lf@3w=5|%I_2F`focjC7Cp~?BOtHdDg5OiArO6O$@m*93$Q?F65t2)7u7hbRb&xHe4uxy5%}5k2WPSUtN`JAYnzAybB9Ko_zr!-{>;&mypcBRdF7Q-a=Z?1#f<&>go8)FHP%bhEGDX3g_^lkb@y>NxZNTf&so_<<nvCf$k*}*o+)O1X@Xw-P-QGDxXD`<1B*mFwlhESwb$mmD!mB$?ay#r?!>+LppJ-+SN_$%N`yiGQb6-Y2`#zyb_f((rRi?5T!OK?VQ0c940KIqXu!Sc@K?sS-MaBTNy2QQNcqzGd+rpSsu3z%eS#ny6Df%?WK;mMv&c!$H*YDSFuQTPHMaPV&%|~h4j0GnEToGI+!dB?KAJ}zuz^Vh&jJn~O{7gi(i8p8Ib<YrTH+JC%;)L5T4!`KE4FT)lCci9WIN1aBdzrWSMvfN~rzC;gEhCV2M_J6pHXH1<dse)<UOZEn!C<}tlY4nok#4oeNG&>)@N8k|?nd`;ipRTk9R`{r_MY&G1T(b(+kqkQ_PNvo28SMZm@a44nKgnd(q<eswjzLDoZvwg_QT^ncz1n0%8&1Ue*Njw=U4N?`zK?W52a|=A76hqKYzHZ+4HvML;RcOakWlG!T>}bMU(D88h5)n54Sk%`7QSPM6W`0tD=<>HlbWwxC`f3d{%3n?3&px*dykAAtI6wl%1Y_bCAFM`Tpx)Zu;QW79hZ9cuh?|XY>;o3EIDNO!V0lf;Xi9c`Z4f^gsXh^_J0{pq<>Cp;eXH-#+#w&=0eSquPt!4)@5)Zidi5{>$$_{P^A9zI^iM-^~kQ2X;SY_Sd$1u7Iq?c1g|9tCzszq}xx#b<h%f(VR0Em}m-B8!*=G&R@4*leD#KT6_nbsi;hp^^+xf!n;QRM>XrmFOZ>n_-$%ydbx<`jO;dzar%p6QplLtW#rUZfmAGwk~3$Uv9E!TBCl8z2{;1bO(BZ`PXIC`iCoWE>gexUyBtpfZ7{JP=X{&-q!6&V+^e7XaZ%O5%0W(1@wcoav?IkI0^m<S|M1hNAJ^;gZrxLxChF*E3R;_J_i>7-ug=p$Gy|jGVAV+=3)~dy3rxK{=T0SVVl*dv(RscU4SkzwkP#m~An3<PrLl0?bs%aleRc2#9u7?DCgvT$bySNEgHr0XKQyP@u_=oAMX6S}c|g%3xb3s={kC33**>i$#eOY*xd7uMuLQoC+T6)J4_KDW8u121zRXfazA)h!7R~`@g?Ml79J#=JNqCcxNZhF@s(q#Dvv2W>$=`<Mgg`EG!HoA)*=Dg>n&;;{<5YLEoYkg%ZlbCQi&w!Rg_oq<@A(#}_%}s)p+zyM7^x9G-<T(Q?LSMzwl1_W8aMK{zh1Au?1FX<-V~`Mn`N*RIl!p8FZuh26Xzo>e!3wdiyllQ)MrDQubo(Fn#{#JYNEH7i~i7B^bQ!Hrv`ZfE4z=iQS03#4DT-acwa|elHxwU>*x|9nu(Xzk8agqsV$1}Y$UP=?BHk!$-x&~QT?d)5{1Gxw;wPs@IRBhp^h!KP3TV(GGwu^D6=1Ifrs9=MRFDq^1Kd8y1_Y>8g1AY68%-8c?aOUxIAaGr=l7Rp#N(BDRxD$k*(txf`^PQwNKAeYpB8F+7`*vQvleL`{}kt`4j+kh<JS9f!TMK)q>lLzw~9aL{!^eV0)`nQ&GA7g{VsRgqOILp+M%gV3NrFF;ZBa$zgYLx28jcNg*pe=_zaLucHl>ty#N>2+s72^iD1Gi+5bsIW08>6ZRU8{Y?^kwp~**3hP}0c)L`J1|Qz3q-iew6K=59PpY=n!?vScBIiYubcw$54%FFp6?#1E4AHzH%Lfz=NjKG1d4RC?emk<uGu+d08`zvyhz7>*Ay1`C3w8G$->F;9p;8%N*M556sL8pTq7E4U+i}M*E%kn<e*gOV+ckt!wnwjT)wysL3jS5;Lk&9l$iY~=H)h!8)%`u@1@3|{66=RdlWZ=?S5rJfxM5(hV}@#m@2Nl;BalJnbjo#<vr0|l>Wx%mn8gTwQCT}+AAjXyj*je+`Ke$I=ojc8feKerHhcYZtw(+y!m~Lvf{$Z{?rTlHM8CieEEld|E6{8Y_#o)Z(A47nAK&k8v5T7!{8^NLTOT&D?foCZ!_VY}c*l6=#oFO>1|T)IqS+Xs*dY~0>mKlFS^wIc>2;6mB^cYH1sO?NTEYY@4f1y)pyL!@h}q6I<m&-@5!m3&zw;!??S(xCvP!{~;Lu_^T#1<l!HUvLMk+wAIKzS>Co_=o__AZ)xz1>ahrPH7l<kro$3!}fREpX6T#zsf9J>hbAbFvJa%iD(+Kr0<X^*EQJkAB<`sB>E4J#T>Sr7aktb%iEl|qa%Zjl1<iAahNQ`O#0`uoU*C4hWnlo2Wqb;YI?Fhtq1C?JEA&V=sHu+)6CzbSRha%!QDhFIPm$w)E@lf>bAAN71mZHRSk!|bsv|A*S~da#YUDRX<iJq&Fg&xwmAI;;9F1+9;vh*uP*6pKb1iaw#0B$-HG!~B%G&x!jXR4TMl+mINbo<2ytpjBFC+>|OjAV&u6)Js?_i>z22Wdkd;+u>%qX4hSMwdHW=t%QCJZ9J?C;g&NP>MkxoWQguEn(N72Tis=pTUpuYmpub^H)4zJE};e<QPgH}y5AcN3_|w`B2xq*mcrf;F2Js7|8XwBbwpjn=CRQe?b!z2KnPDN!fEALC;4gwU3?i)P!m(9vBx^ZStYargp3J-L{!nVXze=Qg$CkXs*|&>wuF4R%D#SGo1nF#u-iW7_gGf!-bcokU>}fhnbjsxRL|a%1)az8Vqm$YEWLk|+j=^PUDpm3aX6CG&aYW@gZgc|yJ&IkI`LXCbggCtKeu<M8!GB@o}+8WJcn+SZ=djGoIfZs=(>oi$a<<lf+A78;%#lzdQK0xp0+8?aj+Ap88P`TaLE#~%0VTy>${rj$p?|p@$I10GZ0PF%Wz4R^?fcwl?17+tp<WofRvv~+jIpP00=~rz(sbP1c20D3xzaiBp1z;X2bUixFm_hiod)?THG!#*LRnCP(%KM+QncUW`BmE=#H0x4d_ReH*C=Lo@Ei-nD65GQNvuE?Z>3N%4HWU#AWJw_c-qymDzH831$P&Ogn(=J3BTimSmqCTMFnC5S5b0C94?OZ<DBC;JGF1@9rjQ;PC!0w`<tBHR#~RNa@{J$AsYpuvDFoPT$8LfaUl3^1-W14P)+)FqR>B2|yyvZ?-_0j^;`c5P(9SC$9uo+qeKy7kMjfs&&b0`MPnI-S`BXk)=aDLXql1Op!+4@g)Vd-y!3k;&=E#tOS}$1?$6LyQqjDb~zmIUG5$1rZ&5&%gY^G7amn7+YMtrchvoLd%4z8_c<S$0b^7I!S8v%BL9MI5%8w<vNzHm2+;T4(M2J@UJ-`dY)ZT(??IU_vLj4WxL)T^V6)ZyfbA}un*{906&hK@MjiipTyGBB;she|AAw8FLxMx6NR^1$n>PNYmjJN8MNpK+<D{pZ^M<z{>k8eV=&pp03yQ@l6+rNc3J28Q1PW=v?XeWFw87xbqa9XFIL^S*WC~GYd^ue{9qH72QUAic7^nOL0;wnmSt$YNb<+~S)+JI;;2l3j9~sh6at$~AtGN*7iOw!We%Rco#;j34-V;lE_J$WMAJ7BaM}iO=3jtUA*PZ>&y`9JgUWdqbe`(YP7#jbLk?QDQ$g~VGn{x~x?{n)EWDo85NNdyM!W!g3OX8Sj5bk;DFTG41;^}%Co9TCR&X4RbLl_gI1FmAgo43wx1S0Klc;)(wT%t}6yA3H*81eBI09TlU9rq=lO7VBAN?~M&w~w`>P+>Ad@obvbbWw{_w1a@Cnr1VjJIf}5!CAjsYb|j-%=<EdzY4gZ>kwNNsb`7{LBt1GFa^E?1|}fZ32)M7U8@?ql40Af^Xo*yZi~>7QraxiyU>pj>|(b<@IjZ5qDdf%a;*xCE%Hw)%Mm>EQA{2yiZy+qT*O$8bW=f!g046*B=vP}`)KG)vIck*-t%RnRH=eu9pwUpxMQy+=Y7^x+<?bttyto56@z-8K-b8!gjxB&kVs=2zxbkbYnpf+bbC&XjwWW$I~QFP3WEZFOSwW~4q{SM`MEuPj6`X(+ve+8$XUk`wZ2e_k~BORHbS~aauEy>aRlk_z8htWplnWi<<W8~MuUDISRbNi0Y(#MY^m7BX~uS6$P|V2Ls4Cc`DRsp(92;*i9k)v&EINCBP~Kj!$kS!WA?qAMxr1X>uRNF1f^(;eaNY#J&c6z?vTgE!YMC;PO=ysnPXy7EV8ZaW668NwzTHF@0Xgqq&d;}<XacaAu2>Uhz;g*q?`&U4PxPHhmV*U1Hz+g(kl$`zM+*l$YR<UflO|ysC24v`dJWG?1xU~E9W%Ie5{p;2kGAWP%9A^^g@fiTV0mX58U(lGu-oG%9SZPt<gfZA&-?AS^3dv9Ne5eA<wQ8Of{G=?~*_gWu4mGMd_(0S`duw<zfd4_?8j5J(g_+BWvqQ2pDmTrHVBj@0_bMMy`$kVkI6U5@UhHe<I!AkE7fkZx8!<^gj9WCj1HJ$Ba40&BFvG;g!&mRD#7(Zl*6<PC7}<kQBy_Lq>GM^O2_rbpgWQ2X!j<9YluDs>2yLzyHX2UEryYUv)+d6??-W_uYH8XIk!|J>bnpJ>YW)S_A;w$n$heV}RCJwCXoi#Ldm`1qCE8OuoCH9r)C{l^DQ={B?)A2LfLgaO*1px9!fFJGIk<_ez9t7FDir6RY5;Mc7G{NP@srnC<Xd+JXU&bu#p<q@Z(oQz5JZZnjh{L_aTi*eB~jz_*xzTJmGD{D0hi*>WVuvFs1wp_a^A9(hEVL^F~jlPJT}we$afaXHgfjjjw250C7IBs)(8F#tN($XGnwr#=x1d>phJ4S}RjAni)4n#hntf|vrn4xGN*4Mg_Zfog(In2+mHG9fa{dD)i)-x%$1hS+y1Fwv(TTK1>`m$R^kVuv|8J#dGKU-S4tU$^#{TSy-T^bf(20A@%e)Kl?&h3EVBP)q~V9z8GvBgt_guLQwPyw^I+&kCo|!gfM(hW{uSd7-JBnrgEyhFbc?(rYz@P$~+x9*j)LLuG+<*2BK7%PRWZm$@&p8$p^0NyBYa)$?AkI^=NdRQkzgLg3qwDE>OHSZyGg8NeO(kadMMiqNN-A6O2pp{yk%lCybE&)tlYZ!X%M&7smap|%`<>e<Si8qZl}cz#ht9G6$-b8;brNrIY&I<82iQ=-E?2D)?<usG`}?Y$N5UHmGKxm+mAb3L?}p&0WTH#xTTj?cG2TX<r2TD`90mMPQWR3nFsf~=!X$!)i08db3Y+=(UQpqXQiPg91>woX%Lr#eSI>kY+j^9SKwbEZ<|LI>^jdB9^HW72U!&r*rkMvF9qTLH}~A$zia19;%%dQ#K&9MH6RWxggKUSoCCRPox+fm8X*R6}+(F8D<u2XwpV)7|6f3X$E`ZO*hj%X~@+@<vUVT9nr<=d5&g6wdqOqRS&m);NW7K9uvEpmOM|8-9>qPl3Hoo7V83W^7vcPErn?@V7x2WKG(<WQvV&C9h4s#m|Bhqy{CNJ^t=7;9XYVwvjAr__3qwl>Vq?2;S<{AqbnmXgZLR>@%k|gd_*uHI1O4$>o9jCuwiv$MhU@$nXpu*6>n=q@Qt%UpNO&6jRIcqzucuzzfuqsYHW5Bj~c~rFmLF4cGnjX1(NyYXHlh>lk1x`+!qVY7e)gs-wQ!amlftJ+D7?U8j7P_iN=Sj&aP%*6ye~O6><Kj!PGStuW{#q970HLu)N6eJJZl@O!ygGmY%5Hdx$D(pTcvy#Ej=xdrOtzGbeP%2*P;E||A60b(WG!tAYYz_tNtQWSwlBggI}va1TubZy9e;hDJ)2|W|`<eWd1C?2Ra){VdNi_Cw(5CXxz@QhZ9thz39pU4$|xhZJlLk6&tb=J9RSjJq|&<SKNFov}*p*#DaQ(*GfMAJ5a0VmG$j`fO(tqJ{Da!z>{P;q?O7sw-OJWqiOzpM#b3wuE<Vp=3hl5fX-k2aZJD4jA+ql-Kg54bKNK!q}q%KRD)*?W=@^uPtxM)%md4g8JDlpZO=sly{z*HJc+8Nx|i;K9fqzN-HDT_cVFh2IKrZ0lMX$USCD?kH2#hRj%sq7IJJuPQIJ`p-u23FyZN*d3rh<E7KV-&KkXs{_=V2J?pP5C9Ys#>P?Dx`m=B6e0!4Kg^QqoeUGGnd2W}Yz!nHw}z!CFteuD$<N#ejhU`;hqZN^?hb<fnd^Yt|7%l1_KR4kCWsognh1d;lnrMiBVR}%+m@#<q|n&RL)68Et3Ev2-kG+07jhOaP_p1O3$-CnKKJF%&-=%>KjLIF6pfPEh&h+9y93AI?suVShzP*G*V@&lLaE<)x-6tox(~L4_l2@rTyOCiIWY1*5$<%9;E!R;_ZL@$uBS>XA3NWRU8x`_Yg-Tac@eeFQBDKj{2xDQEaWnb$*lF{hxGv)0rav`aOv4`tVRyu=t^gM`jf|YF2kgD`f(KkO_)i+vxmv=$%0?b$;_(O6c>5q(MSy5K?gJkdvI)iL-m*IvkXK!Vx6iB#>g~(`)|xLtm+}dMIj@{tZop07mvYhGRddsiaw5!b8BT}A>oov=aTM;+*l~a;G8xnnB(`sbJyHhI&xsfp^r3HCIAMHs$SI3C|H@9jT!t9W&fj&mybu+hdSxxhU8{ws>B%&rADV`&a5$$B(a#^p#4$Dz^~CHioW`}7|ka0A8!Hg=Ci**NM}#aaX6>6sLz1S*fTE}q0b+F&Te8n=5TisKppA>v)cjY!soySyy=m4oGO>duKjjU`v^~y7}!0mh1$hz4y*HTxgTfl(j{nJrukWH(hI%<OI~PRItCmKFUgNDQx&;#qNW}Rh+kNuoY{p#bSKm3+7*~Z0o%05DdG<$!ubdTV0RgFV5MbR<&obno@H?W%uzvJJ7TC?<_LexJr_SINxUMjXJ%;_<#oz4TW&>h3*^)lMLp%mX6_<c>49+PJRb=s{pq#5(Fkmw_3Ak;;-=cMp|?Yhwqe~kMlFz~0nP>%F9H9?6T;J$em}>$$}Gl^$tH*q#l~V;zk8XtKHd!ASn2qvE;@B{VfV<L)dFVLjU9OD(PglfvWzmHvO{DY;Qko6hKAM0_-X>MqPu{ynp&>ebSbOuroQH@OwR=5)?8xDjcx>@wRTwH6*B6p+dNqOMDxx2_5A+rW2RiQWy!SCepM&!vQ?QwH0;`EW|FqPko?iPuKTuFFyg~vZ+qhAGEb03_dpLw5H|cQ41wX(Bh(a6fmg;G;w+f-$5_q}1~UspHZ!w);6zQ&J8~l!rH!<wLILX>*F3{k6-!<I!Xn=qrqe%^=2HMk{OkZY3sZ=jO@mn&PIgHM<37dfOK=PWO%dN+d_uuYZP0WnPyhH_dIG9F!;_hArAOba5nPce<9@Ie0T8YP&1iFec+3Uw^1eUbkw3ou_R}BV%nx5c_S@qv`|bVLZ@-(Lzt}GJ7$3>J>o?7deysVXVm+;ToBhK6aQKBNC3Ck%{4APd_2-|j-~aL$C>C9Z@w8(xHm-CG1HBge4E`Jw=3ReGP$z3gDR2XD1O!0JTlxThn8z^IylSQW;P7X_2XC2v4gaG-Auj&xy{}>nJ|bb;+TXF`a<q+3qXLD@<By}&7B(nj)!f@|9F7(e`DY0K^W87`>GxlL`{{=n{@eTe-yeR;6Ei$kXOxBgh(BVpP0E`SOcxH<3BqoZ4k!x2REQ=^|G+tP^*)tZuDTG3n{(nZT2=A~j-mC^2-*xd6XE6&BV5xKwsOTl9izWKRsZv^Uw-}hfBziNAOG?h$l4!5-vKI{q}|WAM+??kBPSR%5#G1mj?*z>M8WWhLq4C2zN+d+=b}AqoeMaC^EmA-oVoea`rN>g8Y%jGZ2IVJ*-EF%v6G<^uwG&j7@=dRyGo`&RAoQnV8x#Ird3~KO1CY{&2f>MW>w{Goz!MrBAB!F+Q8P*B4!927?-eP0AyF0C3XeK!Dsij&$pF_W<$MwCKxE^FJyK*c%$Q{dzN1WYfnoDV6m%ycPwKc@l`_?plN!?^{Cc7w<L?+Mp-}qxy|*(x5s6b<>9sRLdPa<&qz_-!i0%M3Ee^cB0mbqX%omFd5zi4v9__yc^%gw*JGkVX=ooo@Z(-EyhfE#u(FgZACyGBkCwUHS;rpZ9dtjrlUhA$^vt4U*bvK;uy)5O&7okzG()BjCk~p|s3;hPjx5@wl|VhdI7W(NBku$`>j;K);aEn$^Tgn1-)ynS;+U~s8nbiw+>R(#QW+}P-fZ$ny-PwA<XsLl$&DMi8@DF-rEM~l%KlNW)!Ls%mXbm|EUN^#ejGyO24&l*Z>IIuKu0282bbFX6}!4k9c#(^bw&7gc&i)rM#k#;h;VN%HH8SbrxNUO=~y31Ul7J<>MplCS>^6TTXn-@VwB(h?Ob|prwtIO6p7P-F>Vn{4Os-JQtdO5@y3;QbE1lBa!nFVDPsczO0CKL3y7cbi?+8<-iIe<9rXr-OjS6ZF<sXN!?9VR_=5u^d2gZl`0I1NU|ZdGi0&fJlo@i#cPmr*3YZ)U6Euy==T#+Pak`MLai@Y|=8y7c2R5raRf9O>ck7zR{1*zxEKXaCb)`TGjk!E-_Ebp5pT&|r?85=okn70X78^F?goxePXn&GA4*j6#hZ8N~-dB3DUY0g`=_@hi{9^{wFm$#VnOwx@TsXFsh6;K~X^z9%sbPbWPB?_~F>Y*C2jv*jq@L`K@Fs$;>v1AK_ftc#(ou4RJ}F6Yim@(<M5aa*Ru;~qj4vWnF&Av%Yc1!^E)h_BC*Lz=)aIu%QRk!!y1GqaB-2bwTbWf|gA+`(KzIv0>=b$Dp4607o23*u+K9cl4U8>p3)6_l(FK2sFJNjA?ZBLd&^^WIP+q=fLB)u68po%)jrlX$wU#;6N4N6I%0;xr=kinuc;@RTACm}kURn!|u3VG~qb<t%7<P$D4oxf(;u~z<!3N;ySZ5c$oHNJ~o1xxf@-6A#+=I=7wAsxg*vq>_Fs;{h(M{u;<T5OdSwfi$0xZwN-g%HbDLTI3J+ru80)hty{cwH~PQe(0$4S^}5$$%AHm0zrbz(^Il6%~uk}4Uhlwx`4D4`2GjWMkcuSL_`6^NOQ)2>z+r)g6CSM&xWW))zvtn_2!vOl-nvkJaoqTrGMr6a*IO{EWofz~v}SuiAHIy9K-v$%8BVT*lFu&_~h<#Xvp$5U*g=8L!HaX;GG6Ej}NFt%rpU#MY)@prP2FJHy|NqB241EXsC+O?erxvY$q6MPuUtAxc|cM)fu7X)#BvMNOaCOyqE5>DrQ*Otz`9djo{j*>Arc+|{Fb;9Bpijh#bGie<#xSH>sr-m)ag$hXHCWf3t*jl4o&ag$%6W6IpjY9T06vl}$-kbr7Cuy~C=RR7wwHqn(fSFVbm$%tDCWw6fgU3jBb)>xkw{WK$P4AZ#?mOb?GNzl4lrQ-E01j6WGgC0_cFtvzITR&^!kEjRrww#?s(G%@<67npX-P3GB;D+SGg$<#JaKIND;fpa{SbVi`{L@1Op-6_`R_7Ox-X47l_jI98@b^zxf%rrAR>Fd(yQzpN4^t><j@#ik&~LrhQT{Go|GjTG#?(L%wc+}7|L@WQndOZ#+nU~xrSjpXqV4y7N6T~26d2UfIg9{N?Gte9BrU{L&P0UjvcR4tcE*S1z`j<cu?u&vjx$geI59&2TO2FD3nhCaIlYeX^+8gqF-PwR$8L;vainm@wU0C=0TR8X9A|kI_40TJ?gM(^A(a=!iC;i<dP)mzYps=UU@ZPuHuUwTi{yzgiSsatQF6*tAaYmKo<gC{eIBBrlN>!<4qJnw|7w@uMA<W_nlY+pN~-juzA|wOZb8o28=EkxlLQFQS5iH*o2J2WdaaOK_<#`8?SRZa|$)8JJOt~^#}>P)IM=^P6GMvv_!P|Sg{-=JI#f#|AfGJUa4e>x)s>%45(dYVe!vRxzh22;ZAWLtj*v{_m%ydO*~mCGq1+ikZ?%dDI6wwyLx~5_RR$nd#@S$cQEpjmj{nr+tK4}@kP!Ei`3kc;aY01zFt+KBd^HUg{*NJ4coLVoozb`7?$>EC<UuN`X{%VwXEtJVXY@Bz6F?Y0qP8{)u!TS5Va#72rE9t-eaO%*wB#BR;C^;Y{fZ3{yWdY$*1j{$8ECfpzD@VfGHz|OOPpbaEhJ#){vYeJK-W8I1Q1&s!7KvCmBLbYlYzA@cs`z)yz7F$lC5}@vd@4hQ>-`m^da><V<a*4V`re@z#*6#agQ>Cr;i5UOA<eBH0KX!(C*)IEu%S-!Q4xo>}j;50#^G(Sg(euW+N&?%AJBJu5+RtwSA>mgM{KJq@1<I8XN2vy;t&sl?On+M6xn4YS9efVY@B5v?Nv7{M{VQ9UBPI<w*k6)jXxV10`DSnQw2QV-z)kNYv-WtFIDn`M$kU;qfrDFDg1UbUdiHf=>cGQfO;oB(oabSzv(kNb?~&xusome~9VNUlX*0!)d8Eb>!B4P!Gd5jUM7tN~q1)DO_RZbBxRaEQ4Up-?UZ43TnTe$N%ijX~R2p_aA?3LNR!h^Zb85QCE!E08X_jed{%Gq0Txi@6d=CWCS6Lz~Xk*w2qXMjW+eVj`GJwqQ=c9{jp>tTZ|8Q(x1tt$53LPaE(*%(>l7WxYc+GMfRS*zD^VW*L}w45#!p6o+nuCb=AsuLj4HHg?eLfj=-XjOB|Do)|Ox16+GFXu$el-w=P-AI;X;&k;pi1n17e8D+@3+-HPzYf0LSWE{*e=3&TpPw4q1%02Hl1I)wN*FZr-1G`Okmj;YZY7n@I`~1IS&{JmuPwe860%?Dv=QM2y3Mb#G(xjOQ7)Qw;xX}3j{L5bxHQ6L5?mX0|Pa|;j;{hs(r@5hn=`ejL@TCcHS_5M1xXKM<Xe2hURl;-T>|GOH^RPX2H2t_$B%D1)vG<)eP>qZtKqBNM`^fV+JbM5WVX*e7jiW3F(ZhhDu)WOV)EWDt3sf=mVSjBbJdbmd5u*mReUT9(f<ZJTR(JR%t=fYUb^aG_V5|z2%wz3wn}J)Pd52-E>fCU*=sls#0@8|h6bbu7U1bqN_>esZ35Zk7bHl^J=n!e8pV!rVtRfiEo)7-PgNvyet&0#MSmuU&1)qPtp53a=q3G;!@Zn*0ppNr2cHueX&z0Ol;RsHXu1U*Eb*!}L_S1vm%z64^98Z9L3ca0QS-8&Lcn)kub>?@q7hDLYrataUt@xTC;80rAPja1O<PpsZ<uP%?^zg`%X76KQtBSVnp_5=aL$->?*pjR(dV0nVLgy?H)-=N3bBNV*Da^#-JUTn(c~B20sq+w?_ctQxXIF0?)f0)Xij=`*;2*kdmvZ$yPp>$ikfMrQI^ckY`RjR}WoaC-|2H&MJ&%*&B025nT;%b?A`am7BfJ`M6aU=sw;ZX}paZ_Q@|@SVIs>rT;i~kQK%=_!{zY}^d0u;BanyLC2y0AnP~tLe9OK<o_76_{4tt|Nc!elzRhs8c!Y@#R1(6u?seu6yZc&jjY_Ql30G{uzHr~UWRGt8o)h%NuogY4fLCDmTOq5DarKP1j{(k%_B#3HQ>In=fWNZ<tmJhZ1>Ks}|Qe)2wO{ibosD{^tWgkeXn3huz2|B?@9OJ6WR(FDpyU%Tyk^~b85#JQ_$!mG27!xYX%w_G1qX~k6c(8noZah-9mmW+>S&)ur|AGS<Hi}0;8;=D@Sl~Kz983zprF`%tvT<YSh6jc8`_ZTh=16J0@3|;-k`JX$Kut2Fyx1y~O~>J|^L2jW_-3dLdh!55?yr^(W;EJ|0i82O;7Ql{T;?hx*wI2TZ&kTdLfy44Y5|UD)C7rOf?EIsTIH6gMB+(K1$%VfLEL(Cw$7wVL&%}SiumKGiFY=@0Kw_2yIgx0GXfc^%s6Tp4VL=6Uk%Sj`yzw{D&tqB0$QF8l(VRbI(>j$hv;d6z;fcp!<}6Z)h1knIq-8CEuIA0oR?Xy@KXL5aeLr^m0{|E7fi-5<|GdYUILS&Q8Zl6%$c)Wo{87=I!5TA;A3-LhDo3NwIH@6V!6k3{pVWbBpsxQh)rwP-I9qkzySj83QwvBmqjl~E}L}7{5l!CG-$jbg*v#`duKxEL+-xB#35}9(TTV9y(c^Pb&v_(KT`my(=EX%q7@Rgq)+r?f*pe)Y&7Ld>Jft#pHfGfG0HLx1x4aouFtH!InT#MeLOYMIS<Hn<MJt3_ac|OWA<b@*bwzzND6$F-dQAgOPS9&xwQ^2NJuuU=V@A=ivI|$2Umqm)XvZ7V_iGLJPPN~dJ#TU71ep&vPb0kxEkKj$8UbN@d!3?@5uFNaA8)I2)ku(qYEi4V7d|b6sk&xe~}|1h<O{+rAlC!e4b>l@F11`FFmmHHubg2>*!_poS;oWw>9pyxKCtOB}Z7&Bx(!kmL!2M`+e-?sr1TM5dh4aEIgFuNe=QXP7Z^n1l>t2>Lk#o$}o}Y-A`W2mw1$LQeb$@3LJm?d@>sb43Oqv3MGkp1kr?utN7cNA?zk)Mwpkgv?&RSwt3q-R!~<(?S1j3)pg?dUFb02=Gd*-5NK?MsA}G$(qr(rOFbJ8Up$6GA*P_AyzulPT(>`B$YJeDN<|%vIF=;u5j{=x5T&zi@Ekw#6L05f&PXG9>5>T55hY$eG@cirkv2DU8gy@vIJ{wze^{g9xM&oON7513zkQ5fpg?AM6FnaXN`wx29Nd7lLw!m=w6D<&Cbs*2+J&c*!|H9a&9mlS4qeRMU!)=DeUJ6GU5E;?>&(#7WA4Y8Wr$)-Cl93_>BMRAgrS6H{W8dEgZUgVS1i*}C|-fCG*lsM4>(VQ!Wj{!P{8<b-`=BzY!qD3;21A7Q-=~dRYC)P%0rc*bS$;#k&rgO7@SguPzN37iC>UC3ma2)LYLAIkf8d##FRwtD{V|5sO1CSQ7C&)IS<O3dFn;!VG--n{xubRUxqCqwDIrjUMa)g)4jql^|qg-Y1w&#SmLs>%R|QDmUb!bG(+x_9DXLCT#Uio_I8e=no$;%&J#kmpz0X|9oKVNd!VrP9SJ0ch~K43L7$JzICs+;&~8V{Ak^8Qpw8_yF=NqlM0)0jr~4D7E&-@~KUM<yip}tO0mS3iK?p%zAaG|FRpy1)Vj0gj4L`!1OBvVBrY~?ph-BJp+#ZFV_VfbAEs=16>a}gk;sG{uJtiG2_^C3T!DqcOBuk08VxVCSFD*TMN;qpzpTr`=D&NSEFz^R3$j*B^jeY%30maVaI$=}uq-Ih~^j4-R<siFw)i7*L@sW@ywqc*)d3N!bf@EI+L5vFNC8nN<GJ*vDWHVzOh^8{tUTRZT3;$5GDt#pjFwB&)z1UAGi<8C$kMOFU{^YdElEx@EvqW$Y7G(qtfMMokIp?s+$Vl1(NJD;Ls}<#&V}yI0<r-v2i`s@3S8U_t*3o%a=ArXmTEb7u1&Wxe<l>&C#dI95xr3`y%(UEbVbLNq1S9sO%+t$+EWRw|GCxP&nP>_^IXgEgBe#ESChxMFj*v}QhDcz5y*iJ!!?Y%l>Gx!2=16IPV-MVBqDdw7XAvSz)0~-sdHHg>Cp*C8>bt(eyyj|+i9TgonG0xeNFw+c_ok;~qShq<B#}yBaSK|RBYA^JR;Ne6;_CWFU4A5TC_|od4HipDHzEh-#?EdTUwivxp>^)w;8j-%hOWLrnPif)u-+dabiJ@zP=Hr^g-V$dcY?;xa#IM!1|)H7rIb81<~2*|i=*-~rC3*`dF)bOOP)!2uNgsUbXSC$Ygu$U;#6A^hrfAHLh`sVN1~oPv#NBP9Q;F}yNR3NJqlZ&FaxIurkWC99z5kA>V=fDzxLT++D=r{o9AU+BUI&*tB!UE8Z6znLFOMU4cictJ_%e!zW+R@1!82^#58n7L=1)Ie6=UZ#9b}Y2y&6?IjPgqG)zSuN<RJo5v`6%rHF<}M5*2j=CyQ|<4|{y(XsK54Q7;SnPg++XQ}lG#THrUG^g=$%L;*;vHbTZgR0CP+mOiU86gJN5u1rfCj2IO)A01Tv)%G>0`FL2zhEe5Y-uG0BEH{&JwFSZ4q`vV+JcixHf0&|qqV7TI@-=MOOn90EMr{wc6ca)bhz62p31BUd`ZvY^?hIqqmc8*D`2C5d&mPv=2l2da$uY#<gLM{04O<7y@w}B<vhoJsrtD<=pUU#E?LnBLtPR_0_&-;%s_Z(^ZiVBtGDWyZ5iLg@*)~0JuG!Dn*x2iME4}ZW8CXcA+>a6&Nr_wWZC6jDAatFK&{2icFN^-z&7iUxFVkuxmPmPW)b1+g}Y(p>CXi2I;L!DBJ`!KC%W8EX*iPDae>)c5oQ+AMrezEAqFjL*!N1oN*N%UQ{{*Ne-Y?%Jmd0)F$rQtAgalcAyz1N-zZ@&I4Ox%RwnMGvaV+k!|NjBg>2Zy2+FJl>w*h6<VGlovf*f7YLKPWS0SyGk5mC2*`;AXvN|`Pi3BjqDG82$0eee0v(vX}sF4V{j1}aelV0$TUS3Kk4I`k<-n_EH##OxjW4W1al=DYX2+0#OFk`Vi)hTt@Z4XPnU<?mgnD6WU_kVo*`Cote!=Q(b<(g#KS4wpesILL!K`c&GduVO%6Px9U2|Ed%3uieP%!W!7VaD&W6?q;XzW)?F)p{>^yOH)a+G?T>?<`^%C}<>Lntp>2o;sxFr6Gp0WgLwdFz!Eq`5KWuh-F7lIB`Sv6qRmN67z_v5Crigcj@J36b`6|R4$GzL3WvIc%;gm?q!Lx(jnO+y5WhEsvqgu!8YVi8lP2k2f3^U)kWre0mdJuqKRqZSOFa%<=%cU-YKx8D$>U}{E9A#-g)93@rFQ(BXL=Nk5Q0kWop?eFDX;#B}OGGXXYP)*IYa0HPe^HUQNm{2pAd^`JH2oi_GCHwX}LhU1s7C2u1d_-+IJy)B=Xe<)Z^*-DDnKy@uj-@VJcI3?AI#`}D4yeU}wYf>O%6XcbvLm$!(TovA~p-NwC+9^ke;ec)1g=e`bOhrGBbn`+yl5`{A7@Yk0937}ojNiNa*;|$H`$5v4?>J2DPUf_sE>LBwMN2W$e9=)YeLtv{)C)fwA!hB{tzADpnj5&H=IrfDUyZA7e?xfPA5HX+FBD<SXyAUHGbG;34MphLnna%VE_}X}6oseau7sESVbavoa1-mxvQ5ia&6g5Rw%~=@wIAnY<o*YuznS3OU*35SxNb5MNSBuk7a}+ysF8y|_I?7mNCN&T;`Xr8S1h}YUC(<}`r@WX#(}od`$&EW^I*&;&&{*Vupb&+RF7?#m9D0=XjTyi>ITWy!uIhWNqgKZ#bBp2gUbd3MKvLFJ=@GuqBA2$My*$!2aB9nV0ZtvWzzVT~aFrONc(_b2ho(i95=r`T&gOIcyBs~yK3&$ehp++)=Ia7@snZa(_6LnTq%Aj(Yawn|Ljq;5uFZQYpRdUFd{E^A*KKLIouX@s7n(P^ajfVAgzdbOv0hT0X1xy*hSW>qMFP|dbizL-635KTdAduYDw$<Ir&sY@@zAN6BFYNB$K<2sG^kEmRi~x9VyG8rwMJiFLh^6rDkl=d+(=ZC;0YCfk+=W)W~e&pjWw{ZP3wMo38p3kkQt+YzRi9fWWV<zD~K{g8czMg_m<_(oWac_;_vU`QjD_wBF$4`Zx~MAP<vvp*PMHoY50_)RqO!Xc;3)F=a_at92JPPat}4^?5}gtyE+mADtKjS%|ysB&Gjii0R)8TD|+m`$6#Jmzn9SuD^2)mrE@UYen1g8p)wwfv*&0+7q_seo>nc<{rc?T)f!LT^N}Hi0%uY6ajDDcmJvhJCvbX6*<6i=o+hw<5GjC(q$E*PP$1V?o>`fiHF9d{mkA)h&y-BV8$~-~g8TTc=sj!P)ojBqa#FRAC<^3c++-L7AX#6<zcNKem-2w{U8viscmgoY`uq*h3tT#0#=g{G>`Pu^#6;DJHmMlj2FAFmoSUpjfiXJFijeLk#-(x$def27L}xSVpa-YDec8a+_D+N!bKulnjv4(MhFu|5?({&^8WI@8wB79R8g;Rn#aI}XN}^Vs%ou!Xh((v-E%rp!>4i9!`b9XFW2jw3#*DdL$=vJ1i+Lh^Vl3O61<9DRKTr6gKucAvRaG32R#o*zBo$nEt(HDfjovmd#*pjA<#p}Ivwd8O1)<uv?uPrr+<L%Dv>`@r$cmVW{fY@Z75i84G3uPQ=a%J_2kJ7sKrf8+A0QKyY-#d*>1FKb_A~XKfJ!8hr${Pl*JV=4Mj?Y@Ub9IToA=jzR*82ba2b^i*+K+PoK;)OE9gZf2~dU$5;&Q_*lR9P&FK)q8|uUbfhkwAKW7nniC#*Uki1{cI3vZP23Sv0U?~?OpW09@-3G_+sX9U)1^C7j9GR^pwzzyKXN;HnIK*sz*wIuQVk8ioButsquo2bHLmW**g2bRn!7{}sntEr#Noc5!{NoxW3?dUA{kxY_Xqb+aql!NYc-3(ANp^-Q9v!2dJ5MV^7Bgz7fNM>_Z4Ne}dz$5j-^lj8=&da(VS-2#16IDOJvy(T<n1PbIf174B@QT%{$uEqmix$|@_^cIH0YN|b|<%INBCo6Ddq;(z?0t^Z~L=|izZB3iy3zd`Lz#?-|>W)uHhpI96XRyc=!U-hbUpb+;Lhros2hp<QdOop8mwmLu{jRG6EWiJ_YPRf+^2baszOkd5JCT?o@yuJ}JVpXqRnHFnWMPz*v9-+7C83Okh*DqMQ>sF6V8(RM45MJ6PnZ9|9H;<c_#U@Q{Okd7i-*l_CL9BM|rrq*$&pe0y9o^$yXRGd83!4YdM8KUc4%Zkv8^LR%h_g0bF+9C=M`n1TZJUGZaJlTKKn^aw(zCwW#!_My+>1YN#bLV_dcnPYI_53c)|I7WVE99(4Y0D-fnQaeBBJHV{g9+LFR7!lTi%Cags^|yzPc8u`Z=agUE*J=GB=Ng$oW+CsHRBsrG=xGx*o`aUT(<sDPioIsc5<Kw7w+yU?U1^rwBOOf*?+~U2@ya*QxzQAuT;L2_*+^t2Ja;;qmzHX$#|KP6Cm}+_B!Y-yihIC?+3gWCFT;pDN%}%pa2a^u8P{^H(Qipo{v5_XzWs4jr@;5eXR<R(!yRPL@WYKpDH1_h$jQrSq@L;dOnNH=qv<4Yj}(R_M_qcX&2&y?)+fW-bBF{8rPurr%Wlh1bj~dO*(S79u@o%rNK*AqmO&_qs`-e{Yz-ww^WyKNp$a-5n!{*B*_bFURS{3IoYT^f2eCKEhG;h6mi12KlGf6&2T{d?Aa=8^H6vPLrE@UMT^2vEnU?#3=u_)B=g0M5&JU5V-8kqg&l!N;^$I9h5-*MIotTD2C`3?jZXQ34@-W1>n*a<miYLM6qz^c{fC*@|zs7Sf-v~YP068vFmy@eG7Bz4WQi2qe#d^`CD|i)-SVrN|V>nV#89eB7^$)<3Fw5s(w()WoR{kkC-j#A}X{do>W5Hv{hf|GVApr>%QJLaZA1^F9X1PT^ES<n51J&ljKeX;*zmbJZY&U^fab`N7Gu=axpEY{JBtL;+0fXJUjdU7x+8DosG&1%dp=u!*+4!`}6@qq5PV@0KP528sRn~Nr*Ow`5%=F7E;r#|b81fG(p4u_=xfdK7aIC;@2Bh)s@%c)&+Vj5et{r#<US^r9>NA9_8=?%gn6&_`;=M_mW2SOzCnJNSRd{=yd|sPLk58sm9l3_CV}dha<YK$ieYBg}o|^E~b&@tZ6^9~xX*i1{s+uTkk>j?_s1M!7+%OIGkkz1E5)E(z#xbREz09MooXi>TRmeYsMd-^tsmD5}VHKY2kVx0fB!IP_WtLNVwHR{~7><xg0Anqk=bO>qu)-UiI|;iRiXc{)Qw0$?zMf<X!047P78pGzqX&usASF&SCrO0pvExcN>~v__&BurnNnHlDjlvAtea6mi#1X_JT!vl^5c7UuWJeit1$8!k$#^D>M;Huz>?C?+!QzM7a_FZYS^o-5xisLdGs0}Be^@;i-8bN0HxJuG4rZK0w_BA`JtuR{WtRDlC1N$Ug{&{owSEcupXi;5e2ypEvz8<Ukam1^%`TCKU1{}vOw2uoq~$y{OPFxHXBj8~zsAmw?v7wT*Jp@Q5Oh&Yr?k%k7+UlIHF2{m5n+D}d<&H(X$z0Rni1o&qK-6&S@n^l=l!pLJwDdwRGqlg)3Q_*EKa>0QF61*5|jJ0IrnF}k9^U4fT;IQ+e}<XB?k8{>)6>G$@A4=JF0&b1xnvxFcpR7oA=Vm_irCF<+Mdhl+b+K;Q5O>{FZf=X}S|^(XvpxRHvE-477_ddFP%Wn3lgFMP87zE@`l}A5!D7V0gcSv@#;?x5YV=EN%Cug<c9BB634o!VOAxr%hl_Pjj**icUcmD4HoS`iQblO4~Jkc40*(AovHK4~PcDOoz2;=j*c1JzUd}m;MMwe!SMFDFr4P%#aIzw^kZND8z6ZH{zIg(UYt&<hp%wahU(W7nfgj)`n!b@l-EO!@F^s_Wgu}?qLHU^i=O!oz}CpU)+Bf{wdi)TnbyOF@<Y8$!1AFAWL5U$7MZMYL%Op71f0#>tAaV=XSPRR+nKiYcq3Sc~wxh8M2UoE+1O%2fN~vE?5ux(HFqS={Ci2P^-GEc*!PnzYO;;65YmyPs#HYejJc;PO)KtxeX&~=ZZ+d7^5r9&J#}7+gvN3>v<EZb=U38`MC~pmOa>Sno5y<F9E0KJaSj7|HrrAe){8^`QgVquy2p||F`#Fzx|G%N+m`*jIIADeHzwv%(xoVqn7z~6QIKW9caESY(cxS|HeHiolMRe^ZW;?^5;qndOY!eXK$)pE3l7?n<Hr**LG!CrJAMmoE65~@!!4fIbpW@l3NGZ`g-<<LvCR6)&KS7UjsjdL>!NpiXW%@IvV>6><ST21yAz7#qy+9d+VoDvr9&PCdZ!U79Vk<=*>qW{rUHo?|*tML4^P6hF2&1IF_xi;XebIGuf!I4slP>L+yC+c*aA7fX+x*Y@GVI$>0Cwr{911?WZ4G{p}+x`P^F_e*Nk9pU>5<qslm&^GBFZf6wrKAGMg>4b=h18g_+UJ{HGjNaE;fJbQ+FWe*u^=-B_yzkd1k=l}illmGaaBRT?Yi2b$m)Hc^Xn!|jKw5Zna(~j9syjGmNT(V|gEc4@i|3l)-)1y1KpVrFn-?D4kd<WQ)sOZ3`2MKiH;qePHzZd$fvF@;$`ts-K;S-~AcI{pM&dZCAclf+F4fnfUSE^Y+0TJ*FI-{KVIb0HCI+0odVY+6)-F^;biLV4YSwxxu(vg@SM}ODelV$B$sh}Sx#!!w67d@U*Z8lH&I?Jv$Vzh%?1<;Au*7;dryky6(zQuXE*C|aRsB6Jdty{Z~YXq=!-XhY#68#4A+5pIZT#MWX@_fF>OaFm6SwlyBMn6S7u2nAn@Bu-`rhO;%W!Gy`kMPQid+_Pew0>jWBRod6>j_;5G_+Zgc4!XQ*Vr-)YYcBRnQWW%J!_wR@6Ywx!p0tYrfxP3yj&Cks3M}yqqgbjAx<=gjwHwcbS`C)DabTz#Rn06a))?~rOKEb<6<<93I)DuPRO>X4gSq%Q(X<R)e)2ZeVJBy%kmIkHxIHU`b)soV(eX!tk$^g`Gdi}#i5!0$~O$ML~28GlqF~f+ms9&tooJ9S`9vadXgpZwSdiWpYyM~f;61mZ$^|v;~oh&0aODKd_L*vbiO&3hM(Mw)MA|dfBx<L{qI65@tAg0i?BQ(2>gF8`R&7ri`YWP<wVx5hkSABHcE%sMCa$kcy~73q+<?KL)J;%A)9ms2QWpmt))2cV;xnQJ}LEjC!@KqBX2n49>_G*9)bDL2ch&IQb;>Bbb>Zse9W`L(Gak|4@FSD-D!vt7PizFbRgh=CbdO9B|MEoPn!~6SOi)Pw!nMOr!hoqCwYMVe*_;s1xJi=C4*H!)Fh$q(|Mj6j1wr@$m-g}M6i(^<EUy;UF>Mmc7&x1rUqy6RGM;ntqV4dYre})?Ul3dtp5u$F#N4Aqty?mX@LA^p&qf&KVcJ&qKwlEUgAkk*fO`pkx({h_m?>klioaiX<Vg=MZH!nx|jE}lju2wfiX=w`#d5~E%cjrU5+{JddCMd!?C|fYBf`a+=meof+9rQ9t1voR&zsKogv&{&~dKfIpJ<&cW6#jCTS^EWxw?k($l=CITkIsM60_LYjbr-<~7szLzUAY*0eRA;hrw%z_uvE&{7$P9B9UoMfq^gW19E8(ut;Jk#T0rnC9S<z}Fv|<Q?uSx?9x0e*5;%_b{1qK6xScNtysoNqSWsDd%KZycedP^P2x1^CBXmZX8xpjazBym=xD*Gk!4GC4-B^Rtlp`5?!{<lLbb(sdz%pHHH3_sFs6?*|AmZ;UB=^1rO8yR4@nh3-piJm_|h$9Di=|8o6qCH|r>PIA-X+_|aSR3+%#js6ShQ@qE6kK=Vt>zxRK<+3v6u|DlF{HphRi51ZHmXdjN5F0yP!&_V9Qx6sRNC&YoA^!P1<ij)MtJ#ZNKw5-2vZuzn6%v0p>ziAoOBBq78z%F=yCjt;v^MzRboI;c(I4^>vJoETKegt!PP7Sy+kcl@&;*C&cXH#GeLlOgiFlh-n(0gEgNu}*R5&w>RI*M%rprCS^-DOFX*A#6sCI=>@7Nx4%TUaM*fTA{4P7x3!vG)16#2SlN;QW&_J2z~N6zA{3E4a6on$Tc8T&zr6jH2pnZ%^#qs=tp}dg!o1)L!$BO>5E;Ess$E;U|h&?#{4MeYC%^5hGIzRXj!7Go7Xh{5}10-A26)sSUBtZdgqYlWf2@@O_`C!J*ldEy_it)JrH_3%S=^!_oI$8ZaiyD&`cv$%TRhMc%*36X{Z9=9*<RlVN^A=r5VJ?a7wW8(q;Ckorvxh7YH9lqOOjU_>;wtjD^C@`m<-5iXZ#6X9mM$8H{anJI182l9waikcbVV?;V3v|UF#DgxM~5b$F#bF@72UTT7a@dM@TV~NanFg!%P8$7R6t4$tw?R$3sE``ewXvvNkTS=1v^RUS3ur{qh-gn8+gY&yaAuDip?Mbjh1vy$T={^s-zZV@&5Kb#N9pP!4hX{)v*3{%16!LYD^LO}b^Ef^G5-+cPfaft%hVdz}Bcf5aDRNE(mK>*k%wd(^Ztx5-WNUQ9o&49_(2)?pHOSa9`n~X(%BHD~@$NJ+G^gm~bXIJtLnVenrwyMHuxsS>Sm*MdTd~$QKD<2rJWmO{3`yv)ZW@|*wnuiF5_&-(CHy4$GK16|1FRjHBCg(}u37RZ>XKoUew#-!43p)(mUHdsRa3v}*4m!uMYcW>uH*R!agHFfR09nGWeHU-{CO@<^7s<2Pl-p&4OS@@TO~*wLD@#(B0FGIbEy3EnfQj%ctm@}x^Id#KZZ5;w1$7;ZynFFIR(X|(SDXw@}NmR=2B$|FvxVw^cX=eORBm#Hz*n=SV(dOkzE(+2-aGaoERNAfs{WZ%D(0+k`L_I{(?6M6HR35ad#iJFB4>t)Gx4$U&}L4Uw6DLxr2UGd2H({%R@$3Rj87Ne@W08IEL5C^?uIMV{UNM?wF<{OyD&46zul?s)p(W6k6{E^xtG?a9b3OwffnNykQA{p&zu2YHrd#{kCP;hb$}UyIs@-xUK=-gbwtsOG$Dwsz@OH_AgAF`r)x`7D?@vo|irp9dDgyeIR`LeuBu}>;@ntH6Fjauu|rj3S+6k(+5iKCLPRbQyFHDxnWz&Gkx}|pF)%~Y@g!+%IR3}rr&wl<T$HKUdRW%v`9nMCv8>IE+i0h5BbW~wQ!2^Wajyb$C-#;=e!yWD;_$G)k{=we^>z_DqKsayeLTXQOc1#K@d#$uOar3L{s7Qrj<OAF5>DFHejrv(L(Q%{qTcF(C_1=iPk7Hqc@PA74GW=lwghCE3yq8YVcsQu0sO#3U-~6iOL4P0`?monor@<uSmePykiuknpANOb8q~cUPZ(HmM9l{(K*X1VBL3dPgzCy&ZE$rLTUsjqH)jcl~KSy8UVvS_F(Yl!4CV895cC(nHH}&^i0zdL~2%Y5@3&bJ;1#I0}q@s2#AW7sK2(huN|qZPQ^{ClKw8s(-*IQXl@v>qRS04MQrOR1-D^~zbc{gsa^5xZ;Y>KZqRo?!pzSrF})@)i^qPaRgfV2cKD@b7**Ll4VTJrQ1mZkv>44^HZCj>H9uxME15%dWERRQ5x2l0FITF`n?bnNqYOpHf^i@Nr`?pTf6k>V4KmLjMQkC|q_Y)}MjmYN`t0XeWpW8}{ec!?CI@}B3rOD$=cY@Gk5e3Hl+Apd=UigeH$*DHvS_xjZPKlZc6yx7Hlmk{$>0`u-eZ)i2F@VS5s!P>ZVLzgD!_3cL!8uXI%7|9Y@wgEYrPUMFd>JW@L+8zn7Zpx0aR#mSkFTc5=2ASlTiap*3pkkz+$g`O0Bd`ZBH`vw}pU>$3Rz2H~femUTc|z$c~;Bnv`R`1dIsg7~9yl2~p3Km(~?a_X^EcY3SA%(v_ZG5UtP^CpSiQOr{bIo$+h|XUcoIZ3;kY^EyVk!yJEm_MvN{QBMMAmvqFiT=Qj6M<i9|QRY(3a+ZcLCPysM&mop`(9?4inqTZ!%~6&F@RC>@9^#-8>#54mJz@=Ge`}C)jO|*KJaG^cowx2I>Br~Ox3_s-<c*_9Tx*$VYbJxR9|PMWXC;cxD0Dt70lQ^VDm`_KeNSX<c}m80SG|g_+=jujO{I*wc*X~ZTP5_JK)BG^>rfgBx)8W4GUqW*oi(+}!;Xs18Wo{`(IocED5V=B8_tNM6uII@v#d;JQsI9~A!|zr`=uI!;qp4bN)}vu8I~l_)*-MbM~Y=W?mmqB3ginEcl)!Y?}1R?52C}6W;BL1+>g-SQ|dOB2U{rXPh%W<xC!TKJ9L6gN*I=hR3)&qoOFP9K%$Rc*51GAHPK_{1yd-{g*9H6xfHIMRxm<Sd&AJ6QYX2aK?Gu;T(MhIw#g9$=n$BVOP%G;ha63)Uov5AeYE=Z<|T)YspQ~Vk7=F9)2O8J5eKU5`YL_gS0A|cGSUX}xY2iedh8s!>Njs{JZAb&#NTzz^{6|tx*?L8C&O6h$7hF)f#ie5FJ^)%*(>8y2>^7a^6M^2p)qXJ&R{LB9VozZM+xtkOdgCZ>Sc=ZuUw#<5#1|3;`IqXhCKB(m1%@N5b`C&)w#%Gi6RRjv7Yd$NahG2y%PAYvMjP1wD)FpJ;DSq$HIvv7bkgj3W>2UJV`2|t|=Hb3hNH0B!tVd>yTmVBDVhFOhLc(HlH<083QSn*8SCy-i+Ral~5l)ayv&}V%LT>2Z)-<D6IC1G8=82)0~s>tDKW9OeO}^fraBM7<mruO`FtjGM{FHxQyObJRq1-HmCOEnJ-pfKmnSA-3Cv*TW=@{j5p}hE8DDUdwI`E7|T#fCKvt!u3D7SjH=);VH}ofEyUR!U{xN9hj-xe#7QK0*kEZi?s1{k$5n1ipQe$CmR;Wmr#kgOnLLZS$bH%Nd<Ht}T|qyE<=0aX=BvB7M_eTV78_I-eJ*6^uBdqbvQK?7ZDDedtTjv*_ApW3Co$^?T|sWl*$XOhBl3R{H*2pQFk{Sh;{vUfoTeff1SfJnZu^p8@Rh2-QR_lT)W`rz&|DoeS!E7eNX!zcjOTc(fnC#}?fBw{Y@R@PTq`w+%++e<KPYPKv7Vi+KX`yV#{TEFypR^R#8w@4pbAvZHc^m-N3f{aZ!jgsZHucjaIW*SqKy=vmf(2NOQ6Td3r*106m^T!Z1cL9w1!O}oC1Wy-i2&)wiV#|t~3$nD$IA0JxbE1M`$`CtcjN-uS2eVk4nvQJD?M6hEZT0_U@(t93Se6&a^R+CP=kl>j3Z6rXj;R?TjDTRyL9rIqnB!Nz+Q7$l6jmt7k5An!J!eL#_n8^Jph$&$X#zNC}tds-OV_gV$)n9L>m=j#9r};Q)`3%7BL~9Cgf98(4z)A$~;}jH?UbnB{vzq7D58AM7o~np4LuQ})M6Cf+&%+%a80NXTK_<}r<`VA_+-@GR!R$L{@~dP4fadGf8{G<9+Y@h-6lUTfFFw9YyQl}u&n21J4`*-)XwKX*Lji<2YuoX{F+SR$1WNc0;;4)B*Gu+ybyxlY@2tt$3W`+}lWZQ7V98NPsy@e5HD3?Y_GZVPM(Eho9aber?6)3b4EKDP@?M20Bc&c~4F1m}KVN&AERI)~F9L#*94CwwNTdPs`?%xiD1^O~q<xyT4VFV6u&Ax60v7~cJ8Y--JrB7dS?*JOztzN%xSQ8|ZII#>g*eX~0C25ZSwXkuDTnW2v-jK%Jm(`gI4XM%3oM%UcrHNjDF)4pm>y_SSPqShKC5hcj^fn$`Rv<UQrLt_;Zy~hj+seGB_5SQgi&B}LyC9x;fN(cpNS#^{R#X^KTak}ZA$LT&bWzRL`F$pL@D=abeqynciEnf$fh6ga{cIZ(NyoVzer=-RXj+kRgqkhI?06{;Ga(~64PI-Evi;r1fP7r?#tf&O)tmn_?&SCAU;jHibUuB*Q-nc|;-6f(VzuEyDJ56=d_>jrNOC;&{9|FZ+THMI>Y#o!?RFb^tHN{NjiB1AVEkmI%4AO;l&p>J6+W__odmuI=ErPWsK8L2uBj7rX?0&Rc!D@6!bD;ER(;ou&<vvp657^6f{#2sml>$UGG2&ZF-?lC?`xpZV1zXB<q-nJpPEUEC+1w{Y%>6xz0{h6eI%r#@(@wHlkSr7$DBnc=5BFh*5AA~tnkm)Tw+Y5slnk^3gBO_XWs&8>1A0~*Xn*8b3MBR_wfsE?r*KX1w%I#mb5bG+YJzz#*t<=p6b&l#r2Sh(DtgdA>+LTgs*MT($i#9?7x9Tw{DEMv>kznj{1MI6=_w^rD0p!n@F-i|4B<U4a$?{hUw{9kuPHFyc|*_t;v+0BZ%hqv=7!gZElla{m$MFBL>K)lYxuvY`PD`mMT*BCytS_=@~v|9H0VH^odnEhoz!Wfa${$%fKi@mDkG(cH7t96ya%0DAAaF1U>R^l@1m6uCVtwhZICC3A)Zc8hu@8<rNY7%NBiV$qwHl-+(EKY4jR6;<^)DNB^;xN>@7Z80YoTXWPz{*)j77#XelZg(u_NF={fUVx~HsediVrdkgxmH{$HDlw_iva1jmTCU?Me<n~=bnoPe8r5&m(punkXQp8B8mrDWW+Tsl9Wun9txZ4Em<QUi3T5I`8B>$E}hs+*ZjM;}pHr-Vsl`kSs%-#e>B??Osll+a8s@tY+MOQKj6*)1w#;yu2y?s^oas<rQSqJMtwKfXN}(?+Q4v@*w!g*9)eS1w<xQ1vRk?`)=1CK|j-9Bpdv-WxCOvF$rX*+BqHX(O-a?+k94ri0TVuJ1$z%xQ0!da~|)=$Gfxf)UZb=reA3p70D(k7lnKb3+?oqXrFdPSuQY=M*UmP~BxO2LrXP)~bh>%*9%AQYOBkYsS{l2cDN<@MS%JGTu#FHrjp4$~Rhx-}98cqP9&?&>^-A91!rW$hHB3^t$iQ!e?IdRiqy=@hD>%o+6GC#96gW-7<_xVXnzf4g}1VFjdDCI7o?1nWmq!3N#;=VNwy!K~9T!DZbRk)FYEPMpKIL{1C!ot7bfD9d}wZGtm=_OVj8Ms51$pdxEKe=zpsj#AV2}COG!E5v$3OZGpTgzO`|&I`Ht9Vd>R;0A&DdzP~z2@-R{Vsa=LuwF|gS>6~r)HnA-Pr*D%Xh9qGaHn;&?SD#Mkd7kdJYENXeLm01fw+>e=QEbpssgxE!x=G{ECjcj_76LC!2gZjDNzdjAmT~M0$Y@s)YZ_5oqu7`yU9yK<H>T}Kqb8BWzeY<xXO^A`zc*1(%pn!@Fl6pl>fIWPzH`aMx5<S(UN|0DfY9ml-FPY;dkG~kV7X<i3FWMyfELkwgN#=L{z*;FKHX>T@R-_?ZdYV+EES%7_&IwE<ZZn3!K4p#q7{iIKbSEBa|LtkR(GGHIc|CaAVzITN~DzJE9O+0&ynv>7B?_<i<()eJ*remJq4A6q-dFjj`{_XddONz3)Q9ckY2_V?$9(onLdP64o+W=ovtK%;A|e4=j<i_muV7Hh7W^NIV91$rKJPekGB>^%@;1y{9m6hyuQSZ7;y`o^YdkMEa}qy1yf-?hF!&cW<)b25quObXd5MGmzQS_qx9Rf$mqBaCHeO8u85n#WfS`q?>2GMM=lqj0niD(SrQ2jJdGjo1H<j5C>OwJTgxv7GiV}nL=VBEMIRQDLy8@P89UWnEXW@vprATul-W>oOZNrsq8aaD*yse9Pz3v997hsp^Q`x5V5c%gp~+#CA#a*XU%$+P;0s{eWl1jJwArwas|fpX=LMI)H2g$ah!3N5>}po|$o2t#9;-ICKBItn(GMDW9SkC^!|{}Ejut<MluUe|qQ_1o?o_%5kMVAOtkoa@)|)bQxot}Q(yo0O63XXH4F$p>X>iHHGNEYUke4itmOImZO@Zwh!>gazw$FK)WR6$5d;-@{&}-0+Uw+L?O?36?fnN0QoR8jxCoLt60@%~Vu!Bl{2iz4AaCe&fvg*O~Yrg6b1UKztP}XmW`zv*G9-Sda|2-Yu3<JpEU%z?3A>Y4!%ygo>pi71q^s8t=m!@Y_3Xo$`|0N+FAOvdz&Q@a{O}i(PgOG;{qO^5+XADGM6oEwZvTR*id)#z!U5QS&nB|p4)ifGAKk1VDwBZPy#2GzpRTjt$d9<HwO{3%8w*}Ss?)QEVuM{VNw0sdil4qyE0fr3BL)-&{nRKJ8*xtqZRWMC|M_XA0jQ!&N!|+daQ2>pr3A2pg2z&un&jww87#xr&++iXZBwzWF;ZDEbSTot}ndGcpK#*QrhuX`Uk24_w<w8Iq6V?be-eT39rrQ)lND+%77|-n|!PI#dkWN>W{3(1&RIL8o#RfHW3<FJ(A|T`Zmd#3D(EmR^mmc!UXM0<cO3k3QB2y+VVk<&3^}2RW%x2-(^?iRl^nZN&?WaG!nIC>U`1^LLd%pkr?RWF@zAbHS=8Y!f`b}eFk2PPS1ct@)G6UPXH0LPn8-!4cvB4$J179g&6WX<fyYT#qZz{`(T{HUydF{O~M7xFx^5FKHi~Q%GU%&t5u>?9oLN)vqLE2ch4C5l}d;XAc=(kU87;~*L3#*MuGxZoD{^i?;RCiR0<YS#w@w*=%`xX$V+p-!lv%zq$jo4!iV~79w*Dt^R{J(#G@*n>)FN7V~{g&BZJMCOkHW%yDV=bx?_`K=%6EOps)R}1RnVbI`8}45)*3;%6+po#@*fnjw1MXBr&;)S3jD`QqJ3c%DIO01#eut&8%Wu=OrV~eq&d9^2>4X_$!(M8ak+;PP4a3qXc~|VXl%BM0<P~f5eAk-j*brF48-Nay)HlyM(9z$u=W=;6!40zkbfJ#VeNwu~829cczNLHgIn>)ht`Y5;+>G@A3%Er6KmGp8Z$JHdn8*9+UZ*s^Td#joJ|nx2Yt&`wJUv8oAo>l4KL$v&agEw2!|?9O{yS$**3fyr6b*gHwaQ5?J|O7FNIhV1+4WqTO==(Bz^4P#x`}xQ@EFyur-*5nuRk=0;b?650!6JCiW0PB1)jCfzW3*PHOzpNJ_`G_PXCL=ZsxVy&ZD;Jr8L<7#=sRQ?(JO4$QLH9CyjH!p^x61yG1TAUlJ~n8qq3`4Z)W*efBMGnEY+npHSFAE|^pcQ5I+)Uyn72K{4Y#Wl}A6UCS30$j4pi&%`>IzR)VGgOf6Vo?r0H!ewG{7bd5vCc-^J_yvwYB}MGTW!u00kg6G%9ATS0o!m^$O!i<l9`!%}_Wu6&&nIMGR8<ZQbeeMyWu+fy;>R4;K1Nwv?NOl$<X^!l+ny-Cf}~8?y!6gsvV0|XnGgA~9SnKY*vmzadb&m5cXOwPZ0SQ0jzGFuA}lRzs?F}eH1vYi07_a)#^aQacbKPP$`_eII+2n$IOjwVE%ldm4u(x*9?&kp{AxyXcnqgRjyqT&a85&;3~ZP63GPn<$(Z^pTcfE^>q_-?+12t-Xb8Ox7t0#CK*HGR(#{{#Fe?d+r3Gcd+>($ceH0A(aVF>)-qd0pe?hw}EWtG&quXQA4->S{IIw{fyarPNiehTU?%e(m!9%G6XxE2=PqeGp;B6?)1gW8e+k=r*_Vf`Euxo{8irIO*0F~{tg$UZvzqvvzVS5a9R%>z}MBFnByzPhql2b}|Ph-*3ht?iF_WPSlSMgCn3NRWWKs^scly|a#5HMo@3$U1WgvU^p*HwL{*QOh$hDruhGKj8hPz7Q{jW&g0AIdgr)zBA{r7W=#3c76y_h7PJnVT>Ts&PIKlU)Dud_3P*v6$$m5hnLxN2N0KDnxY}9qB``=<w`>jjl{dI;!FM@%mE>{pMYlV@`WdE4+P-S)zi)yth%zW6vn8FAlt$w!sB__^dYMaW4CCgMoy++9M#SI-ff_Cx9L_@tE+wJy(0~Aed)&h=OG(Yv9!(oY%gdX%J<=CXm*6hI_i41KZMqgy8T;ULTc(b^Mfhf36h6oFvAObo=x&s)&>iMFl7RH;17bLs9<v?b|=!AAo<@1vwwRGO2S(=EbQGRdvLz-$e`GnA52)^S@(WgqhpT`;=6N4;Pr}=~NaeQI5eb8GLnyb2HH?N_q&6QOYSEu2MuhAz6$7C7EwytJuds8W0wTtlRulFbDJt^pC*8tOVgY{@mns{M7Jn)=}_r%+P)9q_^l7*oEbcoNNWg^8v5<LbzidZ?-$cHhrkUpRER;>%%6tcyyFgUF6Dm(0Qwfw*Uvndf9pz_B?*eAZN9J(2#W)__VCYZEpFo>-{Q2(=w{q9g7<TnIpCn0V=imLInLxA#5F-muFI6M9tHh@Fl>51V+L^ht54ou%*gKI^>G8To7e<>Y?ZSbH{#m-P15b=3_-pv%BcYO4<|7;1w*d{qdeQK{JIR9n;zZI5e$Sk<{Af;}TwHN}8RX*|}kB1bVoKui)NVR!Bq9*3>tAJZ{7?-Mx3K{yvHXdl4wbuLX5%T9cS)5aLl!6iT*7J7YJKi2JqmtI&v%sf9dsBB@dYGGjE4iOY2x^){q7#5%hnTv=9+0A|ol<fxmnP0uT?LsSO4b3RFq>bqEqAvdr1jsllv(LmamX&wq9r}9KfPXh$H75rcQ{SX@VrbsY5PFb&CgovILvFHz_865zJ;W_n67!5v>>1{>z!47#+xS8&;n;VeXM_O46xceH$KaYrVW>EVK7r+igwv1MPGG=QY!U7^F8<G%_beYB{c5V=53~6X1R~D!HoMvDUx>ulMS=exUI+o`lYSalUF8Y1(Lu*oYKRxN&aL4Icd%e8YOwSFh$wpWp*rU{V;K_#hRkge^nh~$EJqH|$jHp9XEwopqVY;ylS4^&uad(A15ZTnlG2Wdf3uXy;tEOGKpUG*peS_Vgg=niMN)1?t;~sBIk_&+>Ry*1Rih>0Btg(>hBJGiFU`ZC=gP9XmAxpil$h%XGVvUwP@VhxOYnD8U^Q5YofRKmxPW${q%G)^CjuzV2P(L&8W?p3L6V>{kfBxnONXa@&AbgVWY;v*o@FiTCx)I~uJf^zkD2o|7Lz6=#5Sy!8R3aUn&txbnlUr&iR_l-j9Og3j@GpF#G95n>%06iz@64Nja;zS6sa<jhwwVS{P6CRDRK;s<kQIv70qUm;?7EO!w$`d4)sIw_SSMZhXd=x9y-MXTZ-X(g%gZ(28ttcOaYgzbyVMGFfY+BP%7Hc55WMmA8rAX)B-LG0mP<lEsyzQym&=hAHDZ91=Wy1ou|J=a^7vWYTrg=<W)O<TP=GP+uOhYR>yPWf93Mo|a|`6Kk4!cxY#5DS=yok*n!&)j?;J)XNFCo^`#no!UI3B#F|7^&soN`j3o4<E=Ir=q2n^ONlG@ieFMU8R=;N}X@+^^%eX{qs!KheY2V{eMy*B0t3uCFl+Y73`z6vA->c&g}bHkvRC+qDMP=r8R*u%x+q0_VBRIc-~$zffWN{f%XXu)o(kJicnT^MWTs7oYvF`QZonYmc0p4T}~mBM=TE%5gfjKbmoRXP0_b;<elEQhF(B@n2(5Q{cwngA)UH#!nMW4908+Lbj*qv$<=r-J<T_)54m&jxRU><QBn{dGv7xWJBQGOM_S;;MmC&sSv2wwgd0LQjCc=R8ryzv-19>~Do0P}(89@7bQRDez51aWq9h2oG-K%Ge8{U^QI%-2j{p25%m>uzkcaiu;)9$cclpbRT)7QsYI#yH0JyXe9%G1;SOL6(LEGv2d@eAx(?UKPE>b)1@r!MnB*YlUfpTnqDu@>F?|jOASd%Alw(qp<EPM$?u$Vz3tD!Ht%qJ$}p;AU>een!T0E2$jFdAMC#W-;6AHaNiU(JvCxkAxOoS;byDTn48pxwWhgQ{iI>}Hz@Qt#oG(*`NU~9;NrXRmdW_6;IEJ_kavwao)i$h2<t4Az-6bXkgXbib`JC6&9%30Hfdbh5%yKQZ+G=ufiiB*O^fWSVi^=m9civ-^&;)J}q5h4VZf*+){;Ee{RmMrpxiX>$$MpHRoi<kn1}0=06TX|RPf|xUs>%sy?DaeZi%hG?>sYM3&iZ0v^hFt?3}8?3)ShJMdJ3Tm_x`UUcKFRaVuLaXF%3N{G?@c}Gxz$~O_;{MO^5)|Uh+?@Co7CVrD29*@XHU0@t8xP;E5vi^vn;LLN0Sg2?Ts6@8!0^uhfrnjB<yW;P&i8*F->7W8c=EVhM3}8PpLVl{utC&QQ)=z7=9?teTw9KX_C&k3mn*vHg9qUo}Sw13;i)#g`FThFEn|e$HnjhDxEGX|~evXh{qwOh%b#Wpj!Uo?AQyyT}_y;i1+t(H=5}t3C#{Cvtu~Tj9EVUTsar*Rw=SDPi_6NSTGjOo}IZ8pK{2zNrxKB+_ItZ<lqj$-|Bcei|#Ee^@25yLUy|Lh;&5k*h;A0m(Eu6|$!kWU_>KPO88dF0X@6V*x5drX7-j$I#dAGKtpv$I=O%vfK?J0<46WviH;(%~i%%o{?JH1iFw2cF4Gzv}7c=AgXXh6&3%b7FE1W2H(FrHPMaZdH5*$f+aVX_b(Kpfm54;sZBD<TdaAbbfsI+v++5qoeMmmrOq-UJV&YLC+Qipm6DA(2HwkP80ghT-|gwgVT7lpa>w;Q5d<}e=CD`QQMC<0hdd(@zH>7~&w`~cW`bJ+Utu3*0V^t@;bDi08%Q+BV{3ElKmqJB$~wm6!(e1nU+)G(r?EP}7Ukspyk(IEfgf{{9`sK(g#<IgT%aZA+j$8~iDM_+02NfyWR4q=ZKswT;=|Y}%J7R2d-M1LZ5~l&S)<$$ppS1|4*dKePmeX<vswxuNh@oKA5(@d6=ic#DBxvh8>D0KzI$nSF;Q!K(qpH%I!^KVu5YwaM0?@KuX^FPjCK)v?G|1sW=s^c7h_VtnQ{!4XIf8?)3!NTY|s9(Oeym79keBgcHGQq=|p9o)@++qK^5;k43mA7-^4BCTU)V3nWd<n2h(<8(aFLT-2pCrY75sP061sRM=r8LWSc0;w&#;#Szify9W3Q1yxh0ZN8;8>dno1M0mFqkizj-GOM`5sP&Gj_1YZZvQtw78`;wrflPVn%ay7}p28J9p@p9_^sLG#YTm(0QcnSA&9WsgC{TvEL6onLh;IIb$C1*SA4+c3t&jn;$L@tDxORTHOs$*m7Fh47{LyPr^CTRYn=33MS5DTzziEig&BBvM2_0<pn%e!Vd22jZQWO0!{oYPg9*CM~Sr1y|?utvo}&(zl;*NQ-;z-)2^n*Br#+40Bfuy-RNu`8)7?$IU-nhf&b?6BHe8x*R|XECNen@LO}4C3AfmLRJ1d8jRwqI%{sr^)m7Snma?%!NC7-?q{z&@FOM(@c`ak$env=_nj=DqPyZD_qC0eYTFdtSL)$Jv88<7|mu3fyuo$RM?=0WH&Y^@wCyRc^$V*LJemhITjWqB6a3=HCI`uQI)E|AZZ!k&U|)!>>^mh%I(@Tb+*cLkb8t|vNJc0KF+ZuQ>k(_h4ytlq-c*Z>42qYsp)H@cALS^fKH{5joZH}Jo<8dvuTa=jSvAiB>aow6ZlI~asMo3A4A@rLkC}=0`nJT&uc6hoT`QU8FQ)$E9Q0|OpoC%2om6rbDnkH6waCB0^cJwUKLm|p7(d26WqIf#lsKs>l`e046$~bnD8N^oZ;bbgE$8ae@!Ib-5Ru_SL-LNSReg)5H_`xL4gR-9&6GA4i&~R(p{E=x1luakg^X_r}9h<Ib>6ZG;9x~Dac@<eP_6Vv`6=jJ5_!0aO7btp}=S|YWH25WQZ(DQiH=1!4lk*YS!Pk?0;ysZw|1rhT!?2;jGaxH6sJYz)hgXu8O~p33((9D=&2)i}|PfC_@r?7>k9^QAp_<w<U*jn9VtxaGsi&#N|m1t9OBPt0#%CT_Cr&x0Y3hiO^zxxPNDO=h;=)1u1*3w}(lD03Jw*8$(RiT&i`o4k{xCpgio*D<OadM><GJ*dF}>$CO6>9>hiee&WmidRLwDOdprnqrN7>tVJcbWt~DkYXxg^3nzKs?kabv^X?2{{w|3H@~crWEMUG)qZjLq6J>B2mn^p#I%P+2cGvErmPE#T{~>@P(28%q@8iF%4OE}dXhqA7sc{o{c&}iRa_^YnbmPL-J%h@Hj~v)N?10%CP}-3SX4AAU1RR3VQx<JturA>Xp-=jl-5BrHeay(&u~+c?sYI2TvJ-_-7Ig{l6P4MGm@q)Fsd~H(E@jjK7ft_|=iDc+$z58Ctc!qPQF$raIi1{&RcvL^yg-CO7k#@=AoMpL#DPp{)jn<T(T)-{8vFI^)M!VX)F4(f3@yo};f<rkQ*!E&dzP30=HP&?2_`9f&ukJ`WMS;*WUmeXJ)<>DS1Z#fSdz$dPVF&?5N=5+xMiv<CLh)U9L4IMWetD@fOQC*Nd6LMAU9N)yjhA=s%AOoGRkH=Ls^Y8ych>7?wWsX8W9G{C`0ijtbDG}{gDkhMw)`|o~G#hFTT0rVUe!H?X;Zbqcvh|QdUV$H*s}M^smzSzo=`~wLYg6rEnEw(bwRZEcv|A!$toJkisgXKf+uCP85FPJe+PdH|gU+6)f8b=-$gW?cI;k7HY~-csL+)GwY<cL{0!ah<}8UULkp`x`z0akN2Q=@54tp1mq8{Y?yor{2e~uz-^Exh_^Is90q=-klG8IX07GeM%lrqc(7#aC48A$xBwXKlyK2eM2@{bhlwd%<kJGV!|e>>BUlHmb-}Q*le(^Mde9Eq?5_*o{$E?{vR_C+`Z3~-2X|XdB*-LCK4+UIUxa_01op)Z?2l>YdG2X1UdETt70hUJPfvn(Tce|z8=yn?0peX<d<)u3Imx?iI_{II_atl_lOz;{R_?>!JIk~0LQzN*8%(ZzMF1Z$V||`WMRbWOcX*GiEQlQ?M$}||+ZXlc=l<i{gN<!unoi?${8$J`fzs0QZ3{(^GW$M9Go3PF`BlAVQ`?x|c$q!DefPn4@VZj+%ImQ_lMgKa;jk<uH^^e75D#hH`!H<JC!`q%KCzt-C@^>gsh_jgjJ2UH|4|1YIHqAL`?)E;QBKCX%gzr*T3)S{)(+r&ul?00$`bpUu{HGF=fy#ME1SkARkq8dQVj5b?&Ov>QKG&}P+cTO3mg#et;mQ0g7doX&*Iiz^OaiqxD9(5o?;jilsL6a<1&m%Evm_n`2(I%m}*SnZ$61am1+8^sEMl=F2khuoCK*VNflk;wGghu8$WNeD)$b{Mih-mafv*WsOJrrhR%eD#4|1Om<X9jJFAJoWyrOLIp(*~XUVa$fpn;vE@X`w5ckk{_{*^LYBqqnMqCd1irk6!;$BcK%do130{4xcvrS(wwx{4YZZg=H<PpP;V}L{Klg2#H)7>8LiOh9~pLZ@BlvJlhg|vcc{w9q>p9q?)+y}fcy=$cpWyR8xX8vPeL`EAwS=X1^tIEcl07#JQ#`F!Jjhbq->~m(>ndG;neh83~nWTno`HC9zf@v3h=aTtwlk|AJa6GU8q0<$N)zzYCa<garxQsO+dKHw;B2IXa)p~dolXfKVTDEh3OS+?+#j#X;@!{v}O=v}GxDZqNFem!|XyStzA}~)dzvochb2QOS&j7?|KuM01lRHLO@A(|~{$z0@?CfS-3^L~40yF{n*)k0s^$Vo5k+qZ-El#znyp$>2p=o?FeF(XAoDMlVT_MPUrUT3o<@}F1PGY+7VPGm{E_$=HR3Q6t-PJ_NooW8BPZ(Z<%tn#71p^8#pU;C6nc(Of?kHXw9x*?~8FAA|oJ)nvx<(SW%gd9Aqnl)OknYR0$jG=4B}4b|uIQ`5g%q=ncRRW2n7%9S3&IeB+^7q%&@wr~o>q5HkNIx;PRT`hfB{4AHXxCP$G$4daZD#<E@J4#6lV~a2Y44%d1Uu0%@NTN52}6iOpLShA&tvCb_ze)HXM|&gKDHvCWtROal7X(C59gMs7_=~d-GU$brWJFDad)&`>e2Ap5mnDIMl}ar*ilA2??@M$kdR0A@F}~1Py*jNLcM|3cg|C%i^XOlX6#MnJnhXqj>8joPpN7=qC|9KIXOU@bCTR%#NwvcXE|!&!F&0@T!VD+WBtbWAs~}P6S9j=!PwbKI1)^qCMH8B$8G@U^L}H5G>eD^{U<GR0ciEOC|9j&X#5^f~ku6ipk@pS{iCZCT*N*+hE&AODAqgvP?1sJzY_OhA!w|0W)#W6S*lRCv3nYUaC3@-zS$694vj2r7k}tdqw!yon)3^WZ6>JL`S%u%!&RTR1&q$>HE0D_?{V4r6rpEJ}_WPORw9ve=t!WQ(K?w^v!=27ux(ena)qBal6Fb`nu1NX>axgqvD8o7zXPqU%z?3PT#+M%ygpE?MsHb{i~SUm!_RxN{_|rPD?^XN(Kypuxr3|t!7Uqr)LH(h|<vMoiUJGpddwBsbTBV8t<m9^U6iPC3GfeMhrZl=O<k%A~w9HlQ_-YR^=x&6k~a^SCx);-xgHpzu)^%IgyEAk!18oMqlN=A?9`2%r%-{m!1Ey0&57cVjeFeX8)vuJ5iiSz%inrExd>B6A;a&czwo>VW27Evx>`=V5T<bc<F`s@wqI?GXaBG%@L>+>Y=U3lyM;0iqM?BE-a@cDB&Bv?~ixnk8i*I^v5^z!;i1?zFjK8@4tTg-TeHIHB>x_Bj<korg2A(HQ!W9llvF;=2%3u{zd;SLp5}Btp5D-+xNdbmOus00l@dVMPm~Ui5(oQHGy&U>X_+cbX$fwlr>EI_t1p6V;y2HrH8K4#ktgaa*-mqK0kx;$bP<GkNfofU;Yg0e!f3*KmGp8Z$EwiBY*w&?Vs<V7SOp54ZXKrk+3?MG-i+I=r&Zbo+r#@Qk7zl4`w`8<U2O52YYl3DU412=U>14`t$$(<=bJv*m&+%?)E!>e*ceuHBM{;Y_S)hsMhw=q}o4?iT^mz*iC<o4dpl((=me2UDG7*>@qzrwrr{z?r=LkMP=93Pko%3aIjj?BT!QuYs3-;l7~$C<jfvDd{z(_0esciFkizzYVO73=IPWRq9^4nBd4Ai8?t1(y1c_#X#SQ)$s3%<CA#RmmVrHb^E(3B-?%LC^+v}_qB>xt0qF0_r*&ChM^WhKA!Hl0^lB(}yN@k_tglwl4rYyb0^>7(3E=OZ&0oHKe6GkkrP2C&NtKdT*;jQfvNCGUi%M8J^h~q&M1v$A^Q&??hz|(5HB!4Ax)f`OcmVGk%gsnkBBn?{&ZwS7v+2k`|IpPBJMYo?FVrh#%eFmBHf*JaY;c|CVgcRhV@!G}cANXF=wR~3hK^Fy|DwQ5%aP$fO*!A>T(3<pg}{bJhH40Enwe2X4nJuqYMca)(sUG|#!aTt<wbauw<ii)$A@n^%!HHOdpfnUC1}Xwq>W(T;+EV$5c~M5DzVQKU^gP9?4nmVaByBi-f>@_B}i;g^(Lcx`Ovr}vMe(6)Z`|r7V|p(^Kb9(f0uJpO%=)(C@f|X)%VVwxP3TrO<G8Y+U79sx_6$C>k6Bx?8I8LEhQ9w%wZY^od?tUP~ZT1#Qd2tjVd_}(;a_o8M_Il+}Ddk!MSrX4GHO*#6!lb)=E4wHS{Ak9(hde!O;-NiN=I*8^{<sQJ^Y=hlDulgTZ@cfT^i`BJ`>m7H{p<Wd)`&LO7zoN|^dVx+zv-I3l~LA#?yKb42dq<X_y&#YT3Fqp0Ihcr+Q~lMMel23CVNh@Jro5==wV$~mUx-<J$>(nC|jB4ACkP%LzPCw8<Amz-WbYTXd6tTfpUcI!MKr$nKm%6DU>ANFZf6J_?r4m%Dc?M>Csou(;0RNw?*w95U-Ym7r?B@_83Ah8kE(OhDQOj*dD@nh_JPgkBb>al-ELawQ4bQDKny*!Y~Z6S%^!)Fy{&54Jdjimb9J-32ac&0hQz)VY0A!3?&$;VhaNP=l1gH_1{R-Dtlnb*GND-cHB?FTb2vRg54X;Ck5_??|2zEau`s^@_B=TbBohuWU6GW@%+Q=Y$5MztLFp-3#m{}xTD1M_npzA~wE;eZDI6-3HwU@dMA&Et2T(K7!#=0$j5-GH+Q)M=`EK~MJ!!P0@jE*WTEhSe?6bU?V8j!|wZaE(h~P*6P!B<~ZjW2>X!Y1~q=H=ympRVdz~Utp)RLk#_d|DMli6=)wpya#Ln0^TvJ7{yICw|%Y;o7mzJdrdVw`-~bCwed0<eBfqSU)QarxOT7#n#%-U^%3J%6#vmqNwxInJeEPlu_5URJ9xf5)_;GbE%RY|8QqC#8P$rLg-7_QQh1^QWJ~jfSgM;s^cy($0u-M)ik|G7wYy8e(;65%2Z%l64!x`g*(lw!+B~xVjOzUf_cz3mhe@&!k2)<&qC7^L#_Y5FWlaii9q`-x71@FWKdtJ=aCzmLQ_|61VDZ#Qu3HED9wbBB-j*24FwHcD9KZe^@sW1#-KxL;B5Tkiu#4BVT2A?nO>5F0tz2{fxyAr>zB8-@AMI~!%KWKqLuzW)Ee`9jGGjL|G;ZQWp5FAl$SuTev(xLhA*<ejZQ^$GfbS^8X%-End6~|Xpdcqtr1YTwke|%|)!z>RT0ceFrC*;G+xBFWVU0)>;v5qCL1RVZH~y@qDpH~!N+Tj|12V_Jc&~FKWb~1iG6CMS_mk#+I7H#8TQd)}&uRfTH!@_jRFkn;^RUQpXd7IzH^A<OatK1kTq3~3!eE~=0t_NVh|5P22<0e<3Bmf!<CL*}$ONpfwT5$prUAjR4NfSP2Y3LXm>y}OIYyRJFy-oXbP|GHq|W;>+*KB)0#q~%45-OL*(=e|6c8*bNa`^fkO*QSmyR!q%(>B!0H-E4%TX4VS~zw8eZxE@5UBv2XrJnPbn0?6(}jJbgH0eCNJz{;^)#brPizCGu?Q{Lq9_Z5iCS*tN;QHD00@~+Z=x2__vgV%+7YN7xdYnkA)kTd&6+2b*Byjuyx9p@xWtn_&ocXG{wt87phd8YJ)IZXo_=}MHO~?Fl8N2JH=QtaaiL#LhB(jZF`ZN0a$I%{YoRIU5hTymNhyPhvWG-kmOz6QL6isT7}ng=Gx-URbl!TX24V-CXk@0OILBOS7jLm`{RVtouFIfW(FP}>P!$6-S7h3S<g$HQ8`{-~beIuyhkgK}TxN4pm$v~?*yZI^$&Ktqw74QSfL-cZb;pnA0%fqZ-VOxl@7$d8T*E{N3#>RLj}Ny|+=8kr0LWy`F^0)=tn1borO$(gV-u3s#smN%aHO#wc8o1_!dmYyZxNZ72r_B=JOG~ng%t_XijPjknq>(s=TtfnlR$>)F=Yd_nP$g@L4bf}VaRKGdIn1$j7#MS1iMHl?&rV+=c_?e*w+CRCVj0Y3Jf*36<oLVNfy0cQ6mWK<bv#!O?2WR?i#TLUSD0%a2~?OXciP3>SP%2GA`a{IYq>{8bQN#F`SA9!NcZL5$99B&UyZ3>olWYYP+M%%T*<0k5QML*9w>1S6}1Q=Bxs73@`NbNZb+Lds=`?X?vYsQ-fs*K<9b~BGH)q@MK58YDPH>o$l{c`n}#a2`%O{G|dh1P;?ZLLQH})CNKwN#}Ba$YP7dO_MRz3;W{@^cVU(wnW5Zj0y6kSl}hJsLH-)^R2%wLhXy;Zs(Y+Y?tDTw0i8dJVGw+f#s{<)OF>)Mn~RVQ#=iq&2ec%CA9Q0bKmGoF%(TM9jg;wj@Q7{Si&6K9sA(*CwFB9xr-`6F%||LjcT6XusnFD?f}SI&nip+wLfEjeaeL@bM9B>77!z$xw#AxWIGN7ck*@>CtM5jE0}wr%_e;K|Y$?nju~SEBfDO&|BPzKB(=b2lSg}30JtX(U>Zp&YvWu7=`JI+vKQ024VN|79G;k<GoYKFL5wE#ZpdE9VI)uS76}LGhOI-T&dA`GQwczd-*AA3nR??&XMBaTZ*`Vc4(Mi<iOJ-MOv>->taB4@{Wytx}WvF2S2U#~Yk$y&E%p4MKy&q=zer04%31Yr%b|aN%cf+}No_{aH+9?tEq`2WTDv5E1rnJD&#&xGjiLX)rD?=9o-R7#n&4elXqUr+1(cf&I?BY&yjEX5B`mv^zRqNn7fximscE=DW6~E4?UmSz}?q=3n7Z40gsCy)0Hwz`8#4%9;U8sYu=OGA%Vxgz6D8y0|@9UO=#g0lLJvaw@l3}bSBq(_Je`yIEuqSX-)5;`dGU!>MnQ4%caj%cvglX*CgsAJnt8IwT4}~MFG_X*H{nmVD4p@XIija6S?`kU1&>2Y>@CZHs!{)rCj<;i!DSj7C>N}AxRPTQnxR+^%Nv`%1Lr+m-?SvZe?RAuZu9ra_X{|Dkd3s!thc?9XS)DJ;y;bI^lWp|h<NwVi&jZA=n?$|Vh0xA%{{I+kMC4AjmVuSk2>MwE#%*9_)I|wCIBY7RSp&SwG+7KUewC8c!WJpon8OEMlUyfdDMhZ?(exrydQ+IWQi#|R!gZ;FSNL)?kWRwQMdEYMw@#pWF`S#W)aoctn8{DVr#CBnd`xofE*omCw=Ax{zcj8Li==p6z)LB6PmSB$aBK;z*We(MBCU)wbf`n<xGYZTM3wDHOVp|rp+v5<PBMC5gdm^{oq0k$KM+G1lsNF1j^3P<qd)Ys)r`<Az<D<Y;g~`WVf7e<Hn_epb&5D0wN61*MeJ$;YA?lRAl?{#S53)^fW*_<9h2hz;(x;54#j0Py~hwHtZ1rffNukpx=be{-2;@NV-z=&pLCa?<Xqs}TpG~7wYSz~k}3ZwU1vloTN?bl+>gXCsSFUK!3c8B?Gib+LQXC5K9e}~isqT)wC2_OSQc5W)O!HBUNV9WW3Jtj^I5$VrNrA6o+KGZcFh$xV!BREJj7hG>mZyy!k-B}pUpx_j`^$+9t%iFT=)c2&}YW=!Kx?bBOCqEV=g5_jRKNEOe+$2*(@b+jA+fcGF~QLOmSLLj2>jjrE<T~<}=NI8NbSZ*}_a0pdWjDZ5Lh|X8b%HF0AtHD9Qk|ovm!Ms<Y!g0HG^SX^q@kwY>{lRV=52zYpSidSNyGWKFdIW5TwjPn?AHSj{dlG0d)^HE?)Hv4gbj`RrfTt$+_S%Wb9}x$8B*&1#?eB#Ut24#WUp8W2(cL@#}5rEVE&O_1Kfo*vg!a7z#SlHgxt#SJV~NX305c0@4bs2`mRO@zX(IU-bWQ^><w-Q-ZKVrwFM&`sg?r}c24su0aB3rXEW@gmSI<oQ*MVax?_lOCCb$925lbr@xS#yArhokpKFNp%_z=a6kt9p-11x@b8(0i5JNN~<o%R0>Tg)f7c#F=u^xtwUTxNU$Ph{uVL)`uVXegz_`R9n5Qy-4W76LTCV@b~*3Gt3$5ggbEAtd#;o8g`RkAfVLSFC5DxSV`9ZbF|8DYt=AfG4W*eG#i&iLCM|B<#==rfmD|?_11q1o%xUtRURE3;waaiP@7q>FSgejYrT#C2rczeHW1wqaS2;Ru$`&AZWb<s<y?4U~TOFCgjn?byxMfmYIDF>-Rp6uOf(=4C@ivcXRJC57>~CZ-0giVvB<OXTI;l5w2n;6(b32HX$_DRDty7f?9<+t*A!&MyG8WPG*CvMus|{*51Kj~lP$3V$e^q!e=Q=%8SU0AuMQ(f_l<!>tEe(;6A#cwiUoR+<`HK?THCFac72o|NHkED`*)MJjyxPh^DuG>RMsF~OlL!8@)@`c!D2P<5&U1o}yRW|YL4KX%)Q%z6ZW9weWR%t`MULcpSM#P;H7J@OT0Bk7!{I_cMjB<x(c|NHz_IFNr;<|*$&FLHuhU@h%&GWhp59p~2pu%vG}^Kzs|SvXn+EM5a5xi6B_x)I&SiMNLXO|K`7uf~lLNLqsj&4f(0lb|_1vDnT2{SyOe>(_ik}{)=M1@4u<W^p2c}yBh%zN606%Z%r0x;;vDQH)003gX9jYpjfQjYYr0mRfN~3=0;{s?uRp?XM?gL19%xKCp0$lu~`Wi2|&Pf`8Io3juex*2MbIxT5q<Fd8TZ>9V%z9${o_^N<B+x@0gRFA@t}FBx8Td<tM}D=3lkc3y+MVtOK?P|l0aaC6L-3sk|FLaQ&V)iKauwwEq_?PRg#c(gw}=T(H?CiUg$|mWqjw>iDL$F#X;m}@>LN2~FlzW<Dm+`KQsO%<>k=A)2k8-$cqY={0T?%NWp))sa6eL^$4b_gw<i@(2j+Q=+bGhYLei)GSk?sBg>_<W;4QLWIgcpWqfI7_N+)b>;H@%dMu4Kaga8#vw=0uwFwG$kj$9kncl&rio2TcRIhZ4%4RA(j>nNk$GL*Ks;DV7oy!*>PziSExbKbA>zxZH^%c~)HF4q3cXRQ$jgVHc42XS1A4*hG~MR=ddk`HIj)`&04@2_&<Bml0@PCRQN>8^Jp`qP(6=_m&|Z>Wdy@dS>On=Dv&nPAhyv=gDopr`TE9aBVEP)2yuX(d5R$#ov>|Ft<B`$Y=pT{ofAHgcF<!dUR8kuM}~dfPjbF7HD0#+`z+|Dw>NQw~uNg02f7GZ#X<?GN+&^W*;U?cwk=jOwS+KYlFC|3b|KnWCH%d{YIbH`{j}Omxb;<X2kcO@&Io@stmH_b%bu9%j!3Hsot+;PLRC{s|)@<Uao~%%b09D8$thPEk_1r~@A!5E^RjGVLv{R9&x=R>gL{hmH>!_?kKJKBZ(>2Eo?)$4?5`y*EPkXc=b!iB8?O^koq_Km*hyxjtay+iwYd%5~qLtxvq*s~Af&8dvc!WXteW>uCercmuVoUN?Rj#$<tF^3z=bVFvW$H6k@-R-tI~GE6EGgA4Jn=gw6^g#8KH?9o{}r?je5!Udu;#-ha+stc+BA@8Hz<Qj|@4ZI16JPU%BiON_i|9mOW<1`L^Y_>85Gq9dIgrFz)9C*n~!}cA70hC&idNIBbp8M*Xq0X71GKC`xstuYQ6I{;tb!XEmIw58*lCm!6<FVt7ZQzyniIC2h@hx7Gd&AXj?n@d-#~cyLu>A0IcK^xbPUmxo_A!Cjp*|_2Ob3&ZCUI?MNgvToch=%0yhNq#cUuY+o69sl86iMmw}T3>ThgWEWisCw+;;BGd`@)|V}ytCscqrr_G|us@Z+)O?0(K|{%;Kuu1-+H#@;5*znDA^Qc5`4>t(89*b;R;Nof8O>sh`4v^2TEjbqM>E{Wyy!BJ;H5Hl}{7~y`oS9#=?G0<j?gGk2Z8_>tQb%>A2P)UWTG1D+{4m!lhvxcM;IvueyHLr`x!MMy3Zl3p-`n3lVr+GbBOQSEKQ|DR00E!nO8@H$<Eyox0tV1Jkg+A4k&Uv^6n(AZJ0;wFJsbGO9@P~-fC#9>n`_9K;7k!D5fiM=W!?}^#CGN#~?ikOjOa=}KjRJ!wHipLzm4&{a7JJ_M*ie8!FY555bPFtdG24wjiomq=3+uQKJpaf7Sj*YyVKC})hciAvU$PgMCS#8AO)?ib%`zl<@MsViVzYvB=~8L}WTwX#vWjJ{8+$3M9s|ARtBytuTbTEPTI9(z5MGi65&;Qx{S#($^on@XxjQicP`B~Xsd6+j(r)iC3?|FaeDi*1zJL3eDHms2GA-&~)uFzuMUFpOM5FbCAp(T)1KBl6Rf#V`^vkv<%oOwMX*v-w_p0i-lTGW!r)V!a$0bCqJjBunS7^Vu{Gu~^!czTXs{6i#lf7W=_OnVH@;5RLDrql;>f=3SIKx7-#UH&e`Lc#3HRhkNF7x}h?rlwoHBwUh0eCA<<pfUg`Uo7uKvTqb7Uz}0Ol|0U!KM88TzUd3pY3f)s(l^OD>7w#EGq5Dl0R~&7sIk0)Aju(e}4CmZ@>NY$2arCmtLRk@sj=a{_D5j&ClNu#=<jv;JtlA^J!VvraB5NtNMzeTD(U5z&tA9iAXJUyMF)1l`c=MG*bn8UeZ+8Z~MQq9|B7Jp$E{s7Os!oIv?%g*!{czP2n|eXAJiPE!e9z<N1Zp5rsASuK@w4x9C<*Hb)uqe`xtbz=3s#h05;(ztw%suim%W3QyvfJ0*Al{#(paYA3e90VFGBzhKdf^M&Z(8lV3YOhElYleGEs^Y-r_HJ0Eld>s~)2L5B&GEMk4H%g1UUe#-CNLGj<bnZE)B0y)7;V<7lGKfbUy&VqwSSOX5`^U#dYVx+KM?COgxYxd=v4(!`|NQHhUw{7JKR@}8f0@|94(xvI?5~|>uQ~o=F?_5=ZKwRa`t}oXGj*F0eNw!7Y^YSgSkLG9*nW*;)vjst9dM_jCRC<eO6Y7K9tDYC;=VFF?2@_sIePeXQBwEXyR`y_^lk1<!}MX-mACIOEJ0LgH>qF$94@7&+7TsCG)&jEL3?aSIN+5)CrfHQW8Glr@7jB^JXsfl2*;SCVO*Z1sx{WW`^{f=m7}U1<Qnyw%gjipz+amy{pt5#e*5Xy!(QG`_d2EF&U&3)mT*7D60yWOZxJD`i++QJWuPuNHq{))rk(Sz5|$Xv$r?J(xuRLpajkN3fDZ^dHVm}ImtC(}JhDSw+=EY#ru7^19^o;nUC+8vk~x29c0{+2Zd4{k0#TY<wau5Fwa>oy=Xy2jla#C*JG%Jg0!Y_9SM_<+wpp&%!UQUlRYZ|-=Tb(_F=^CjoC6NU^xoVp@`?G9aM6m0GHPrp(bDwUx42>Qw_$&Rr4_kg#{20M=^OX)^$?vHnKkau5~98qd@+X94&ah1Fp8<C_4XLj5~MXKC8nX}et;o{F2qOJK|8s*j>Wi<|NPtg``;g;c%IE^PzN?2X@RtW4(Gn)w+|=IheX?mQY5<`Oe8o^!z8zzSbH>?i+5!*m>MDg`q0{R9yov=C*>2#v-?;huqmTWv@YhIVDi3>GNlLTe4mB{m1p9mrSjxburxJ2`8E=H%;3S%5bTv-8dm+NX^28$+Z`033GqLZYL1?4oW{_fCJhVC!Xgk@umxT^e;UVpK}}QzWlgNdhetSThSdYB0MdDJ|Ll358ZZec2dD~3%tWw}9pk8KVNC@8Cfka^<2p4}@23)AFIHHcnvyU`>JSR^zyq`IETf6BhQIY?w93>p4N!n7B_}CsFo=TnFL;S3ITgs<77Wq4KSs@#y<*t2tS5AdFlow4uY!v1<^Al0?Pg50AWCQY`~^=f^qY5Gjydf*f|{A(*xw|v=QNK!qp;p3NN>0N)8NCytdT~s7jCeoZ<J;oYTThYQS+ijx`gz&lj@x24o*OJhiKi9)dL!bWL}>YZMP~I%y@=-x|{>s(uCCD@Ozo3)}@6k|Bml8@6TnWGQO_;^fIc&xetW}H~zPXN8(~r|N8CQKi|W2%K7M(Nu3L4%Hm%^ReKGM<m6bqH>RHRn*Sa10=6KG#7fPGHgne6o?b_>CI1-glEI!~I~CB5#c2HI(E_8~RID0jKK5DfgBZc@fu73#%-DjanaIt&CwFhq&;^y>aT@pG7knd9-D@}=6b@6xA<pODhvbi7*mRlDFVH^%xj!{o#@nBpyf&d4nx;AmE}j`WxEFl>n!Vyp7i<N_(|@S~cOk8;-v9CTbcs@GLhNgc9OwFkhaO3yOf|HIj1!WJyfe4nPKaY9>G5kcy$A>qQDa+wiBHQ09OjlEyUv-FX_T>yY8BTaNMKv7zY_sIsrf=I|4t!*5u6tRK+harPY}YsU`s&a85ju%Cp6<u%xqS$;a6ZN3ly8E8W@O&BbCYgzW0Cb;m@wW9;OW6+#1tqh?gZ%aU^}$*5!$%>LcGbN(p($6~sw6H8@RMPoTnRB>VXJ0EJh+!L2_z*K-RSl`tE&e0GM}yKOnm43|_>H}cV23RO{ZH;)<WZzw020!-Uc8Lhqe9h=tVZdzHX06~xH5z)>tJVUg<u~{Qi3)!<oo|lL>oN==yF4t|;+mPB2>kx+}cbSkHDd~E-E_GA3P}4L+(?>CFTo&%*J)vqcHCRZNdVNR1O|xjU2mJ+VpJXDX2QDi~28#P3w0BI~_GIVcxPB3f(WFRoeJH(*fV&o+Q?JUi@3Oc<R6^}g<bj*%9=mxcs+4i)t%QCJ6*Sfr4%!*iKEnmjACWDi1+rNC<Bd*Zkrf7Q%*-AJyFc+6o`;Y^naGi_=pLjRy?pjO=zc<UI6+{hfM5iZI1drfJ1kS_H^>jj1%k)ha2v!_hXr3=Yq;kIHU%(THX!tm5q`vBR#ps1I0*ch!z$Z+pcKtuqoE!o&aKQLy8?JmY#{<wD*~KwGT||wE4b4X!<-Ta*XbjXFUq+teG@(<FwH1^V4aeCOfHd%Bl==8+5{MdBm!8g3e9QSBio?6EKCY^-^wad(dl4#wPS#_Bg23sYVvEAJc{$Avh!2oPVNEcIKhvB)sCjD*KqJMe`j7~>my5VbU%o5ghyrSvJizz7%;i4VdxF4?1c=K2<HX}1cSDK^-!X0m5@s3n|~Wx8Px6tNK|RrM_A27vF69H=AMq;PjIW_Swh(r!1=1ThEuubV=lFe#ohM%1HMbpD3Yq2%?&_Bp>PLiwaBgu`Dbgb8g}!DLXMI3hmR(rqStF%{_-|h1-ralNU2dbi56ERgs@9p%QL81cf2f@gML(bTB|OrA=B>17%b13t6OuoKPTmN)4RD?Or4;sFS9kg7^J$tswX*tD%RWToEP{u_Jv9-f4At_EUn=#exZ-EjB4J|KI^vE)<^g%nYmpg?Jh__?s|Zh4$!O15^;;*kPzJMUp@%3(G@L|+l=R>4}GO7MaLS`v$Mx-1Y(U(11ym`cHdnzrY3Xkj->_<9Vo;4qGA+WOgW{G(X3CBFZRmnLU1tbJLAE}=|=Ew*?HOI7%G7mX0>w<p{6=StyIW`Jz<VITVkKXDQ=LN=ZhI<Shvo30SD{Vqb7RGDZ$+EhZPVazLq&Fa;sSik8*YRN>Y-d*L{^kgc^yI!s|_ob0W{e1za^Z0G*&eL2oZ5@}r<l#!CUMQPxH8ygb!$t`|@Ozj?37HptFBt@>Yw1ZolNIwg~kTPU&^=;VAwa&4;#D5FBEBUYTI_?up}!u}QsWxRyko|UM%@8X`aitwFBfjEU(2u?)fp4ls-076`0&HyD325%nhu#Lwtllz$IjM8-h<$nH1V~6yUH#3O{F}S|H=#)W_OqZCvR5#n#j>HvkW%@P|tQeE&xsfs#5AQrTR8rC9hIt{jb(9s^5O_bLdP^|1E5?~hCC+=)DM!*uOnAo2*|Fcbt3v$PnuYD#;;A#-rd5Vf6$#TYj0_k_|3XGq&1z$rUB5<p%Q@RwNhqSDv{0IcxTOktzfv9E48pZ4WhgTIi-Q+vM5w<CIajX?kvuH69BS&>%1x$}7tb``F;<zaftUr*D4R)5U+o33jZW#Ow3s->p+;HG*Ll<>rcpyZ`YgL<i`ga(8yB*xKruo^cOR5s;Jn8ug$<lUYlToQz@HL!JptzT7~-U6*%=*4pqUCVL5;Tp1}5Z|6P~Rt|57(TDtZcl`1L#lOO%6wE-B;Mm8_#5uYkpla=tyaX?v2PA1(xPJT|(@QsGDRs92Oqi1_GPp~*TBy1LiLZo)M7Z9;@e_tL#$xnAL|Dh+=bL$}h?3!)gh;^fAtj>%M_p)=wt;7oZhw@nR5EkVa9cbNNc&pvcbG%iQr?AlW-0s1b3IwGtxk1{!FmIO3}E;%xKer~axgPxw_r2JyPYL2oefak($Oe0PcvCgXe+#|j)_P2)4BxGsW-XyLYCXr1<!a0)*&&3{tUF40U=v!-<Xd54ctsev16B$vS?r>c`ubL{iFR)BbDPe9j$RCE~Yf5hObdNx3SkXejt4QX?yj|8rC=WX-=xW@N{$Z6U8KZP*h#EM(_EO|(8qHubRXv50EQLrdAzYS9riIJvKonVk>SZaC09A)oog68aJ-GV;t|iSU|L^u^OWy;bb{<4nA>(BX8Mq&zy{C+9EDyF&)+fdIZFWyTmEjQNp*W;(O`;VRV^k@m7~ljV$akd^#>~xRzWuvj6Wv-~h=RgLSW$K9HQ}03InX!1V1p+6hM_s7PI9M!2!ud6S+}NZlMo0{AyD#`I?G)JId)6GG{IQbda6&uIh7n->M?!tcs`YMIil{=n)t*X>5F=8sl7z1fnsR%-Jbq6hiBOVD3{7(lmA4VTi0Cwx1%%~B8hp@N$3&4Mdm`F^2Y>IdQHaf5&+;#_|#pLLSx0IoxoaLJ5Ye7juOi;3pyBC)HxL8Ik{#tV`x|W$m^qi40-Bn*kYJihRxAp?_Bh;MA3(kz)pBsBtrv`RtbDnSr%C!*L$<N9$^AlV<E?qi>17JfW#seo+K5~))ZzM(P;;}5yDm3b;vL%5nKOorl8+?o6j1hW`TxC>;CFUYepTyN|lcvxfze(ybf!LogD_(7lma}Fz%H@8Yp()e|dE;u`*&gHq`2ezor}Q#nb$)@vHo;EzF??g@uJfGZ@znZFig0Z!$M+gOHBi?mi%1QZ}b-<XL1^nm{q90|y6Qi(9HF3D`Jj{VUt7>TG#0WEh@N1}7IeV{OG2rE;SJI?R)YRbGplb_ZCMx9{O;yS&;w<3=s6#wZ?Ix!H$gZcCrOkVycz?i|kW>al;S1+Q#-KEa-K455p~$_M0$C;>otpZfI1!t^1T08A)8K@?G1foz716?C)k-RDXzD#mv^hg>_ryqHDCg)=J|O-1L%x%0<FmISA&R40xa2a+VBF+$~>NkoppReM5l>>QIYFb$C=0ECnua|?MgfnK&&j1swo)e907Irfl#1Jolt_n-0VxeX_z!7LRR{FqN2Mw!4gPWDGf5X8iOdnY+<TU?ugbDf{n8l)(&1fPmtBt1r6XnMA$h*JtEUA{DYt6{4JC*a`Vav|581>FA#!dBN)iRZh>P8n&EBP1CS8bvj3<2m45PaPFb<>o<Wv<%~@I_%wud>mov`oy$bkY-J7r$&qSp?SO-%EvQ`URwZ3n(nwgkL6Y?eM@W0s;r*E%=z*n1q}ofFutQ3HlLFVS=kaT4K!+CxExBle++c#DED)sd`cc7+|ZB-qmH?X14{`%bk3uY-)2*RalSYI*%-PbMLS`2Ft`3v$1RhL#(5gvxB=WWUFk(=j=s%f8dYhlCtK86EQAlD1j@5nUf=jlQzw%T@6n2Yxppl~<EnFX$yBObt)zX*4+W27Ogi3H6t_vRDAZ}`Mu^H9wXC20gK8E@5Vtc2cT8xFgcgy?2xJV70wwrM60+;k2wkV`x&D{tY5tmWRc(5sD675z1@cQ&6!{?*Q*H}v*fS@&^mLo^taHI}9zeIXON7BFE!4-5=LC6wU;X}r{5r=MA49C&HYa@js0>MpYt8i~=QUC3a$z9vZhH@ZNK)a~1#na6O|2$Um{YXtn!b@kj&+PQDgdE})$fC6u!&B=yBgBcr;e>o2gvi|Vms04i#Bas(M{x@SYM<aIqC^SSq;0Rf{x-wOWb6o!O3@%_Hvr4Bm@Vw)+dQfLaadDM;S`4z-T43y&(a9%rcP*SiBle;3k*lNma;qfpfAabxvp)YFTxF5ru(-dvk^|o;h&e(z55;Fqv2uAZeC(jiMS%6Y$;!UI&%D2=EbiD0dO4izBP2WH1kh;h55>pYa$|(a%cVUqPx<o|Nh0MAz4ZO0}r$^Q@`UCm3S=$l)aK+g)Wc5#EPJOxq<wCcoMNkvlDOUAyZg62tuchd}MVr#3~OnWjU9FbPJ_DW-W(w1E&|5npIZpYiE|);)uIhED<5E9`>U$^ikO3vH6;9GVuLfG9RH^U-bvtI?rig8aRvxd-mceWd95x0mbusYGcq?rbexZM=1n3E3E$E7(9iT#{}ZXlSa-+$XxsT{jBH`;dE3$nxtfo2(osYoP{mKbSqCF5wILAnay}WA;&j5fY7rJ6dA`d%J{z3^~5MA-i}gdxSrtyQ0zdH}TuPCiv*=)v#$Xk=#|j7x&%SWJ=U@sVI#B^+1*2qJ(%sDsUhZ<1sDA_}naVGT@GHSckwL<1bzY`~bdUnnswPp{}EBSTofAxNwX?ntVt6v%jW*i|5@u|BDZ`xV$k5!<m>~BmOgmMM2I8a4BH)uZ&vZqEc8J5f~{}ejpS1iVEW@mu`c`xY<dLd=_b)-Yz%L<ys%*sa`iy2U)jJ^^$^20oR~eC%u7i0stcXBaD*`(P7jzEG~b%2c2#oet9w=u5fh><xAl2@M)O0L7pJq(y+}II50v!E^INiul+X4E+j>FBpVf>g>Nf+V6;=h_j^bo<D(Ve%i=}$IdG2Qb_R4&1(xRbVPMk9tXMZawgXM+*M)EYuTAjVFC;yPW5fY?ZL5hCh=k1LWa#9J@Q=%Roh>iAKzo%k?qsec5M+UTM{--kZlBaZ91;u=DCr7$&<X-;u<4j9s+^TDQB300wOV^;>F8ZZyo)NO$qP|2{<vj}qsbIS*^DZ}c#okhTOUQtDlJKyHTv^&|MBg?7B*UFr`b4uEG&dW0eJcTgu-I(zOxxknQ-%}7PYC3m~Xt)$F}JhWe49cWeL5Wvom^TG8j(BydvmYeCk4*ia93ShlY7B*%*l<goK4Ends*sq@KrKGj@fxGe><j;Gn8`=!dCirbv6J>n{5z7`SycOFbNOE|ioLZ1D|UGscF#<h*i&Z)?+O5Rpqt1-8o_Muqu3Pth#u0R>edV$8q+0pE&@8z985`~EC=<~3hMni~_RDp`i77_*Gf?JJ~&kAaOzb+gG2(*s&km>py?CLKN1TJ|Uq)Le#1MRW(*CE~aEdL>g2{3twtQU3yjxY!aM&y&ZUCCyBP&8p`NO2mswDE$*e6hvGd=JKlbFP9<Lis2aOM)4;{I|eeCtiLZ}>hoRxWmtMOKS1FDoAXzsJ5r*p;N@M0RkaGZDeIhU`Yw^mGB|phj6Wo4zOb7QfWCCq5^$LArgu-|l|w|YbFU7+Es^p^jouxBOLUdSp-)9mmVN|onU0gkm$(<BY34rmMQ5~wiglEbfJIGrEDgg36>K8cjj3Zk8$;D--RI1@+bp_eG5}tH^6Y-;#VYzfCDYg@5At}ocu)btCPmEQ2!e;e<r`~44lSr!MZD}Fucb`IY$0k2S;i&ZV97#Ls=xX0bM`p5{tDOP3QlCAi-=|}nC$?wO3sF(B1<&MO%LB=RF|Z^N(tAr{OWv;et)tKf$?3`Jc8FOM5*o0?i_M(%QSRU8Ia~i*3?<_ZtO>q(=?4wru!hXgws}IXD9?AaqFa)*FDeNG>PfGhk>c=o#>s>Qg`gfVJp6x;9I8ozdpftX@*`J#pM=FC-jLukM3iFvJNBMefU*OL`JMm67fjk>b+4`b$NM)ZwxYj(<0-^K9nTc$Gf6A2bWDu{M`-5sw3g9o*4uM1nEf^*Pu1DNeDlljhQxmr{t12Ku)2j84$P%Fh4$>keY*G{!*kEU>+zDmr=1qGnykN4<76KSe6)_M$%*R*eN$;yCqN_4NA;L*%`j*#37oy2=II8Q95xl8o$nCJWEo8^Q^bSV9z^6@XFDfADL4AF@8ab2w4`AvI9P@4T0egNvfXvIr91xOo@?<c6Ivj#fL|z%`Kd<(Y)w~3cVxd;q36wx$K5+4OUtF7>Y#%PohX4%TSF@oIP)S-0C1Tpc|whR8%tsJpa)UZh<6^mXK%Uyg}3|_oE3LRR%qaO0|0+Sd}Iff?4($g4^8A@^Zu3#Uz+hO$u!5Xeojrn3poi#LIM91tO`SW5Z2E%66;FokGijyg8wS3R-me(id4A@k6p%gk#vrK5-k%mbxYyZ}r4W^zT0Jq1gShlrS!5hLquOmC7ivU`WsmoRwA2ZoTHKxJu>cTucum0AoVP|824jufs>G*rd+S23>LWVhpolaeue&9Yq%eUlxhq_!4Fh!(e+YuHU?0|L@;EW;#()<RwFj{8gODOVhJ1W#M80mn9(-BSdv}^*sso%lU&L$s@E9Er`->>76lf*(e;57Jk^ewDEe=b9rTX-V!A5H1P%={PUAOYb!8{r;|7>!&c?jKGa5dvXPXIci$F!pdRjhtl0;PV|NImMTXfg?mrCwR3C5FYHpcfA8(A_*#ZBim`$)yQ54M-en@fPBcls(Ke=-|+3lH1NU$`w6<CMbs|bP<X#w>~K;IM=<~GNW;?s0YF)WraLiwn`&($2H6nj$^UWcvA3<(~Ha8OetK2K2yWn}R%;}icRzB|ngl7H+_)0*15R)UMtAQq2dpea)1WSoJvm4r(h(vQ!jn^O5~Z%e{kceNFnGVvu_5n74Uwbv9F9dw!Z{n4)c@$I*t{`h8o_|dlP+oN6m?futpznh;&&lPms4>FYNH_bD4toafp<!m1Td&64q=^TZ9<`H6AFcAI=%vVa-gm!J=E<C^Dn@Xr;*UWxF94hY%(XL(mU;p<1|K`4BIhN!&_J^?OdUn-vB*I9V4S8hZ(6G9uFVVl>;h?I~mEqy;k&Pp1H5i-*kk80?c({j){QIvTZvXn#!z_g8ytbs51Hxh6DpatHYT?5Iuz&v5hPgXhGYKas+NtMg^xuDcxM&In2Rddlx}vIo{Mk1l=@4t-#LkN0Ub!EJMTY+W_Rqim`ltW;{V)Ia&+tUVfjzES{IS!}H8>y>a5F5kYX!cpdi;x+f6>DChkKT$Pltw-9E|le`p5Qr@^5iXo9}=-rO4<&+MelyoN3#qS3pGgC(+n3o*kC9FTai+KA)w=bWfgk(I=oC8s_D=uDoO4;4-jA$s6{Eb?(WBD?iy|E4^YGhK8{hUI}!vEKUzbj)8t}yeI36l>?Z9p$m2V-4{jka;RVR&2QOnbG3(dkaxv7StLUrL#pMMzyI}bzx;aG%g5=ykL5lUAHqN>(c(VdRlj%g77;ZR^%D&I4zRYveYT}PYyMTi5~DdqL#MIU$mzN-b|#Sz2s$<vBOhFLKfxI@>W6#q<<Yc$W8EV>MkSd_O}>GAXbH>O&~S*FB2*L?9C=hSYhQiu&-H59LMeqEc65`jy@*b)t7e`@ZS(7RkPVSRh)^Wlxs=K|CXIECbHI_z*_*p5pO`NR*W6Yt^Fu>2XicAeiyNkV8}=8Zzf!=lL7pKOXdk{G#6j=W@n>IE-TL05{2)2=DBFr~$EqAS$B<T$)}Z22L74JM&)^%_M8-7Nu?9EtAAfm&{|~97{J1H1QFn-_WK<<Tm;CdO6X&BWT6LyKc0ZUXsENsT$2hU}XfhY?s`fbEZvI0X(|O<kW&$=ZB+njW9bA$pE2;NTqj{`j`)Tv}Jw{j1{VBY(924RMOJh?Gj*-Z71`m#g0J@55)4-1!Zz>dy9eo02hX0vV68&W3I7ok*bh$JOi$o^G7G&xCu_@OgFn*}FP&NUtkNEiG3b2iSE0Nj&={!~&x+Dw7hVliJ1Nb?)Y+Gs~*vO7?EaD-fOHJ{`Wx(s>^se8R02{y81sfaA5RlX%VxYnUW9)g6*fARZ)|c@rQ)A?&h#m;?Y#c_odjBO6uB^Spqn!$5ZVQHuL`>edIS`}D8lp^yN?G|;P+JrA7_IExWAeW$otd-DytL47*>ySQwD+|1Ml-DaO%i*K)6g@D=v{*Jb_+BHe|&O#JvigI++ZN{?P65nZew?7D%8AakxsUDFz@^rO9u@&yF;{Y$m#)&Lo(g_IzT~K3qi=O@sxYIo&(#;!gS#9XPKwgrG=89iSIP+uVtkwzHa>M^WYZeKHhCysgF6u0O*HJ{qv6>|9F?_l=IP>M|Uoqev*F$+e|)cbef?-3%)VSIj`w|VqSzUIgP~T62hG8fb?|35wI8->{`K|RY(&H9XkYId5m&%v1(j2hIXW|7y*j%evWOyKK_BuToVrE@F_6|^aJ#lK)QOXntlAbF@r-d@@_7J;p2p%=Mpz>>Ic|`?IE)}khSLnz8EC3w6ys6$4}cW%e)_M@E5cE=lZaTt)RK@n5i@ejA<Cr7%+(q$eh@E*=eCIJ$~!WMd2YinCLL@X+@7a-11}B`?X-kb#Tj=5kdiQ)@&yPK&Sb_tbdLY!3WNZff#2VU#5*1P53JKlZBB;fHG5060B)6XP^S)inCmhVtOf)H2%J0e@fj`nIU^iODd<?UDrZ^jkJ2j7v50vu!xxQ3<#+dH6X;8EC=N)3snF0xXA0=fU;kl*|}kj@_qElAK@!xFK+qn0_#*$6zL*+UUl}0?A_geA5E^XXA~N*5w+L6W7C?%M5~=H;Nd9Qu6BkM>(%~hBSxksS+`7b3q{h#*y;+G>vPoGt+XN0*_HKVo97>x!8DQMZpt>ku2T(x@$Am!WCgD85~&{2yy80wT$)7#X=A2LXGl@n6PbIkpy*ccf6e#9=v^3<ez8tj-+vNy%jjtLemISKfKU*g)2xKC@3sz-st<OENW#rbkKJ_Z<sXV21+f0^112>C`qT)qeU$Z?Ky2b+Gjkz@(k-8EOP`emI1FWYX{oBJyw*-b);~ejlSH_rUx;3~?3_rF4Wc{7@(wvyPA~)0&G&NDX$3)~gHJIG`ZSEM8uayh?fBF{gaBSCMuU{Y2)yYq0c*x59PoV1;ch<xfc}a>Bs~SXcp4k#0D{~Fi9g1LqMnCxw&NJ@PV)<sV>IndEq6^h-(PMd#{zyAy`9lVd4%XG|9pWlxE*Z)ctP?4tSy74FXNGIkW3L0gvq{KK|*yp7&hw|;L?$BpsY^zniY@YG`boOAWGt$XE|Mi^ZZOpM+4HgF_LC3{4}k$^-=JE*B``5VJ|_(G%Yobf^mzBZcA_A&R$4H6?aT^tFcWoK!>MnNl-cGoBuhq`Q{?^A@^2f+F<1o$C@9*ntHldzkr;H=Luzj;(!Zn(4@=#F_)!_2t7ukfWiwjMU;wUQv=3uc+Wx5tL(awj*ix<;d)jy=8WZEKAMQX-7jqA%iF*b;_`Cx^+x|jEv`v^5SQ9P8}O1e1x6ssR)aeBLM$^a^D8LUbWK_M34PRg{uf_3#AbTem?*iD=X11djY0aFW!CPV=94kEfrMc+mIIu~{kwXE3n*W|%}sg<*C(Kbhs1ZNnraRtlHcf=t%IA7jLt~xhRrd!PR4FGS$VH(fH$E7mYVW7e8!znq;5)FI0P|k7RhY{p4L8i81D+FB$jmgdCDr@><0N__0;BqR?Jm4#<Ga#8Pt+<)jSIS4JH$e=Kdl*Vz0a$gzv)6Fdj0U&JXWroz~5c{JJ>!b2LW_p>y51R^;KrZ!oFe6YYg0MGrD_v;IBZr#kyOtARy0@mC6&g$kbh*BO<zOjgSEXK6;tok0bobY<o=#|=hD;P0#Qm3T`sxus}V?kdybcNU%k<k#bCq1`eYyxnYPnHK)9Ljv^&c07xT$4x3v<{Hf7PeKYz+fu+TI;1gXm1)%9%qkS|r%3pcCE@nEruVU6t6#}rcak|Ha9zIMCC5cGQcMlyl(Luby+>&TiW#wm5FPn|b59(&3lm~x_<k^(@REBSIMY5<dYE(wTJF48q6b;^X;(}Yo}QlY#UQ{(t%xe}HRpx8nESmW?*_b_zFh=s$aE7vCo}`Kh+{Ha>2|}E5!*~^<pS6CGe&u~)J`*A&rDV3^j#aoSv;#G<%E!dRF_ix%sKnd&05(`uGvP;x51Tg@z9wJ@=1R~MLH?oz;FVt;oo}Bc5>2;=vb|kT|qa3IqIcSDQl$`X1>ifR*d5?Xqf0f5j78Xz9|_tY(?A*^%*BHvqSRLXYTJ9t4*>%3_|qQN(t+$r2uv^No3D0Ue1XVQ0nvh0)<(#pP|-z=H<q^e8|l@I*~f}9R!rt;2F&6ya$!n1`gtfuRE4;5`f<d(9FjWM>qA(SVR(An5Xz!&jk$3NH`bV+*rw`F1)JW8c_fHc?e|C2OU;N@t9i2JXQgVtrEdKW%hWIp_gt%bvy}tm5;)Y=n=QhqY>@VvqE!vAdXG1PuzrY=-UJZV9#>ECi1|co0=QiF$UD7rx!#tbj8VyaUGL!RzqieQ^1+ZUhbF{u$rBYQSPuH(4Kwhns^k9z}bzb*uo}W26e<%^EB9;qE+rriNcC9PC29GQQ$rXJ-$XI`IG&sN##~RS}?}Lh>684zB-?KhDsWm=$*OMxglw@=yRBWDG>tZ{4+eCdJJ~8H;w{{qh+EEiVT5&3~VoCLwTYjb@{RqtKEsgn3m^RCQ3ziQP#96^6ceyhj}h4#hV;#%-dz{k@m1v-Pfah%nz%@q^MG-5=wA-?elCG328QyiQzd+VkL0xERnxd=}azff@EX?YL=xaVr>&LbaJFv_MlV$miGTV?9bj)T@E)F-|*<uVJNq(evKJB)|^niHHk`C*l-nqG-?P$VDC;-Oqg599OrjuDKu_nE<OssV0kjF*TOZU1=*~mkxcdtBVgubw3`M@d<4pAruEPm#3P)A!9+VRligrYBX!JE`;1%7tlKp6Kc>>lvMJ;w)pvUuz7i7Nm@GY}#y#Nwjc97Q*BYi18A=Ia<*5w@`VTk$3ylpHe-0BYiTQ-r-M}7O4H&Q~Dvd}QBzv?=ai9RktJ0U6A{&fs>}wbD7(XCn#t4^c4&%Do3ZBo&%?wIvn@ft*$(^gU<~3%SPm2jkZh*k;ME1*L4!cvOmUu&UiYhEP#NK3O_p8HrS4k)!a?m;|_(4J*BjbBuMVaS6xdCv`F_&3CxD3B+Dqo_oBTM`?SX$u&WEp-l2ONnJ+&pi-rW<WV^4|R6XTABG%od3h>dK4Ij39+}`;6{4nX9nD;&pFx6Hr%}w<JNHS!9-kMbSZm=LK<8nv|UjAXm`&G;fnD1eCpyGLJ}UcT$W%v=y65TB%YY%m~VQR;D-(2DtXAgj|OJFtmcqz@#Rrw&~2<UeC8xy(j30uxz5V)#u6H$3Bf9nfoBah1rl78s6tt)Rw{G46Pe{9k{xJ3-H@goaVlCVEZsXMv8895;Trl1x{I<6Il!7kyhDAVTy|cg#JuaOFh@#kP^2w%2Z$)JUl6M*>_2)2UKst0Rq;|Bu#a%jL6yUvS}ZrS2G`(F@~jBbkclM*s3Edwiqm;F_tdYQ(54cH?a}td`r@p8{NC*HodACMnNG376$&&;KeKr5*uJJ3*-thu>NMv(M2M!9qINAYic9~tN7bLB9*%_uhn+GNS_R8m{&#UEN8jgYW*`*&ye4DpL|b756f-uM%?1K!j}!Dok4z2ALtFaXEm1N5Dk)CvKL+nw}~~l+mO0*=t_{95uwJcdGQ(1okJ`cy70H5<*s!vP~~c5aSZEhBGqiYZPPh9$tzVrTho|^fwC#n`7zM7qms%AzbXBJVO%8lz%tZI1T2U9)X<C44>7a@56Gi0DaP|1In|M3PnKb;<ce{sotrq|Ao^k&a>D04#=%t&da-YoMPc~ZsV4}<_|(*mV<+<nZx&Gq!MGNogN`3mZ*q%WUZgFQPZf$|ls**DR1~>POFU1FY<UH|2D$>JQbB&fc(kqAPahZVu9WMLS_0%{RY4p4AqzBf>Cs%q?KNnA^ECgQ`qHAs;7j<Cyrx9ezRl{#=K=?|ztOH0ea?CExvMyDS=x1?bk<#X(r{krX(~{p_Z8e(2*9D6#}Jopn<L*tD)u0M8U#pS`1e9-D#dL$O5}OQl17flFgLf@N5MO4kBh1-SMs4_q^k6Up3%G^m!TRuHN_T5^<6rovNxCJpv6MxK6TSiqV65{#QNfD<*0j(+A*EUE^ENrWh2EL^5Nj*r{w}W(=khd2p9)Q8z$+xbt8EZWB-;EWU0G3uP;j4y&G(KJ?U^S7&!AD^WDeVP(*~>tusi-u3q{|&3mo)ii!OIx>k$Kq!e6k$J#D8m$3velXfT%5!6Sbv*qLlFHi9@_@`bYC;Itm`|Cu@SZ89nxTnjv6K@{_n_XgR*4mZRjIgdmIqS#%FE*tB@1`Nv?-GoXAMJpToyL2)cUM&`^6AHiK*^q#s@RLubP5pOF!i!xrso12-%%T2qU()2*R&G|9z|sX)r{~-L$8LTnz1xI`S2_~hJ+r$c%sfv6{>c+DQ)iRz*|<Ei-;kY#7_ARx^?sriesJn#7VgWL&0bt)ux22o6WbyC!VteYfX|F+O!VthI}rbWSc@!CR$h+QP7yIm&}kDE9v-?W6gUk=S)NEb!~2sv~j8yO4fUUx+z|zn7A={5R-dEc5SoS1Iwk0GCnc`9D)lZv2>K;+~$yC3T`^aTyag5)!Xkk;mq(CvQmtvD)N%Hc0C6?*ao*kiH%E}7{JJPBtQH25~%OIo9BP=p*ELS_gkN-)4QSya`-vzIGPK9qJL%7%@^ITrICTKBFrZ`>z`5ay4$5h(OESmDTS}1VbUDLxbRJ<wcad6GWGXO>c~+5CZOdC>*RN!jR4R>B?BA|iesX(*a_yODm<BVLEC+w>VVmoAm8EBFmE?|f_O`1pC)i%j4YPyQH-zsHrTEuMH>`5-JpeUYfoUbW5M@(O1$EuB@j@0kxvVh4!1J^R5e1H6^8*!CkffI`7s~pYQ8Rf`+sd(JbqzOrynC0T?X4yNSRnjQO+AozL3A%u7_=PesbE!Q*kG2iF7Y(^gPFfhs4`mcF2?ln6N8=0Ls_Sg4WUB+|7p!Q9YW1MPrJB#2baf-#g1T??#T>)Cw%F{1Q?TAYUP%w~mYum0-x8R9o^|#oaDDMw^ED{qO$gk0*=TC=s2;=lGZ`OGEK!`?g7)pW2NRGaW0z>{YO3b6X(ac(sjf-!aM#;!R37cs+k-Y|i-TlU{XyCwNxpieTAi-@rhojh+mrA}N<@OJjQ0sQa=n6|+M7g;lc%IFD|UyK{=1{chQ9F9!pZu4c)Dj3(b}f0Xk)@g2Qaj0%0=dA$hV$_77g=0l#C_fpXXQUl+&vWYSUI7H2f7%gx>z_*kU0}Ry5zP}1w`JS%`$vtq~*4s-wO@=<Emq1)^Ls2Yf%tLv>zX&skOcmfQ_amHX<{73jRjfM}Wpr`LA_HZqmpcvN#&vk(=dA{4PYgmM=}==^0(rMuT~~OJ>uv4jatB#*Y&Bkv%{z1yAJe<LrxG`^oO7f|GGyuFb_Kt9ZJO{IevD+GWaCo|ol9&+=ZSe-^u3Vjl*r8F&Ol9VnuM0Dv?H^P<c18lKG7pvsS7;nKIYlA2BjGfeJ(xiE@5bU(HF&rI{I1~<PI_6vfSIQ&<BKpPn9)hV#l%HR5WNfIPUJtGW+{cOoN6H`1!tYHxoG0x#xLCLpR|a3`;?XMifC5y)sB-*uL{yfao9NU(1bTEHt5lXHTDt$5rpeU7fl@-v*6WnH>OgvF4ySipA76KUC8=AWPV;7^z)|+ty)!G0TiGK-9Rk?~bD82OD#U>a64NV(tSrk0)^cc%WX;gU@nX=f;eqnc;XEj!O|346B{JU>|4h42nR<>Hk1hBah9~eDT`oJGOwN{8tWISE2h0sb{w~)ERj?Mp3p{90D`f2vmBB>$fL929XdMR~w2$gcqpcGxQGULO$eSD(*gr=n6D}l~9qjNo%}bBaIJ^TF1@b5xd?8z$NHq0{o8#5{l+FM%iD_U{R&cb}$c={;5P2XhxH2$LHZ$UZ~dq9zvG5PD7`rM?{pPgbq}!Q`rN*ajx|!r!G$I9+rbn7=S4*_8g{>bk#KZO#|5XEHO%QjN3=0R(Xuy5d1*Kg(Q`L+ZsbW_#sQ?Y(Gc7yadBw)PP<65VSl1Pf!~=pHafJ`ezEgB;kqd@Vz;2zi$ohwiqPjpBIm!$@yr#A=f~2+WN?uK{V_eBoX|n3*v?R4Q~#}W_TH6#;7UcP~YSkJ2l@5ddEzZ2!iowHc(8na$#clww&`DY+cF{oSW?*WhqS^nR&G7Qt7f9v^4_P?gCfHHJNJ+ygUS@QgB#=+s4u!!<}srvJcB@5wg%Eqr?%jY^j$*f1;mcQU9J&QJXyi>nuZXW=R>I(5c-43-%P>`_RMroXy?OZ+*{Kx)hUVT|xsG)EZoMC#mmZs56#GbUVzRmuU5NyTx4I^_!0y^sjFpGaV@%=vtuz{aI|FYXj8<H-=N!#g_ihMCGwMVAa7(rqtzCR`o3giE4ASyb(<7Kd?O!jS;_id>H;JJKcY&?%l)m1379l`6$s#&i3>A9Sf!61*V-q5}qFwBI`$OBPb1TuVi<{(tNJK{kHT{nB$Cr=!6$6AF?pFC5<BZG<{A{LSC3h%Gf!-NPW(`fMlFHL^MWMa{AoG2IF!J15FXHJGNF}rZJ;;0XzTkce!YMG+awKv<o$Z-inMBCy%WNO^N%GD;i{z*!6vXKJ>r+_}eeP{Rkg^KKT1~;d*)h^~c}C=aDUiPyf-lef?&zvB#RPDm0GhQD$JzNB8o=!8ZtD>9oNm&jVj6V-wo7g}d<jif=CYLtL}?1$phWFHF1kRlcXTE?nf_fBi80>sJr65OML~(J#A{!@O1a>{y>?ZgfJpJv7{$(VEG+UeQiH7xe!9$47++ke1npWpu^S{`j+Rf*?88q==mr!@YKx4vP#P{_UTC{q;}(_4{A`?VsU^hy#0Ev-o4Dp=%27W`%oLX4eXQUG?}EF;|q;i52cyn#33ymQgU))94@D?}@3zHEq5F?vx_V0l72AwtXf~o?ZbQ@*RJEhxMe(Pt&vJH_Dsd$kV17Y=!4FX-FjFGV(S+qeIdfCGP?p*10F!q}*Z;FLf;>4h_j5yaDJSSq;IgwHE!}crMo$^Kvj9Ko{!xyD#d?<WQRG6W<c^<!sIEAn%F}tH|p*hOqyazyI}bzx;Zb$H(cuk7e+)UpS;}EpZ?3O4=oPdI-I_`UzIN16a19;iF?JSv7a6V2RP3qM^%tDH{6@_r=a?@c}_U#v%)X%kC%Jo{5Jq-oTdw)4GXu2k;ox?&pXp-FiN>gtlsE=*>)>35v&y&Doi?ufF%^dNo95lr9JRwMhp^M1R%=rp}|bO*S?X5;d{9Jqmm~ms0t{q;I2f4mg4^dviDC0`n!|f|ZH@cW9W4tm(6Fal@2v!~TMn2XeuzVu-Uq`|$lGQhKM3KRZ@ZEpc7vpH$8pcB9J>i}mGdkWgfurA4awh0H8mCZ_ugIejpZ2r<Gha0C`2DY&ML=+_THTf_v=yb-q9(=pBDOk@wH;8FkMFYoXF@%4o4t1FIRBQ*=|VM$X2O#GO`y^j|&mU~<Zp9+9$kTf-(ay`^Oae4wPE4kbBt<U{r$fL$yE_&1{EY9vK`C|fO!#4BbQ28T;9v@A^J5sAVFy4BhH2`C5CF60*Cp*mJZLC+BK{}Cg4J7Bp&|1uwbrQp-F%Q7kGryYgw;jWomE#T;2%J-ClY#AuKEdNjAQ{tqWfwISYF();Xc2jO3`pV!<zhu6CzMx{uIKtOm03w(EJ-^bfko!&*H2NGKh6X_!<$>I<1c8Jg>AeNFuGlfF@&If!hsFs77d^ZP!w}BcIWm>2oG(&=fGow06eZ@1Gu3a4Wx(;ZV!f1#nZ<af-V)BQM1Zq0V><)h!KpTe{+Rc!uA;I<ksXqh>V~NyyJ)gl+#LgkHhSz52HPLCJYFdZox+dDRX$h<>fpOD(@5#Az;M$7ho~t2#=wx-&ge+zc<}5Hask#l0g(KMHMIpkBmeyK9p_L>Y*>j@do4ilmiff{A_tzQ=H-jsK)s`jCTDi^YL<DC4!<~MwmQ?J=v1-7u!nfG(OVD7Wh0yE89ewX058><?;GU3;mW|mt#(QPxp9yj9H?B#k`-Rn1-HFL|+_uH?4#m_~Vn?Rm4fU<pz5y@x6Mp=Z;PVpa)Gn7QFAw)t)*Cwb>n_U>W98HxA)+?`t*&Q3mV+X^p4c)AbzKRu+l_hhKSpRJt?qQ>Oj3QVesFSOePUU!MmTk@Dfld+2|=?ilVsdDzrH|M>Bb_b1>Vc0tZZZyw#b6!YTLhgy8ZZQk<--<Z>>o~Qqbc>!DSuJS%}sl|sYXY@2!5<oN<>{`KBS6C-?S}IEufl=Bi9xlH^rN&r{kn=E)3-<Ak4umz~iw>U>b3i{pe+ewiS`e<|*Ns`r&m!;UG8jHi7<w)W^QL})U0BX*$yQ)EAMmAK2v5x8r|p*5rVlsxi`C$Beb~fSKqPw1bhRtvqV?7hs{js8^s@aj?0Njwo1N7H!Ya{W;M0m8cev%puJ@~|jO*ZHcOq^OWRBQQ2vlnGg$eo@C2Sp>mse6>M5{2G@KxYJgpo+lp;J#1Y+Y<59dgB4E=Z9Il?gt7-?2ZX?y1a><yeu^?5=*Yk~W1icm>OAbH24Q1m<xSHUWpG^(vBD`+8jDb#5AuUYyyvVRr?3c!aOu-bQl8KycR7H*!2K6`_B7Vejt#`)IP#DNssY3+mXkCNa@!nTwt%lx$Z!6E~BHnYHz+iqJ?qHA(PhQowk0fJtigy@+AhZlw*0&aQ+j+xiH=45o=3cT=|Ub=_!)%3ya6VWkC!W8=Ft=ysM@d`E#xvuGe~%rxE%^+tOlb58>Vx)uCi^ZhUy_C_TTtW(zapM;1W9TnUUrx_gphv7NRN*McYi$AIQV22zd+|2aYO%2HGqb&FY+<gz@Uq?hGGg$fz7r+iETSlut6|*(nR$JpfM!)PCh`XUr>~y=^NW&PpvN#=N^0L(Ibo0FeAIrjq+taZ;4dbf@aQ$ApH#In+7_xxqDc=|T2Ev4;>Cf|?<YNwZ+hn#?T)~Cm>D9&4*s#e&7O7OIPVi&NHiK$*;27^t<MGMDwz`>3?#i|Ar)v`%Ko0GuMA3JA(;p#iDh^N}b8bgl04k6;n)U9{bYDEO4e}>KXfQjWD`x1o?qqkWk(KcR^t@rBvS!7jIE}6V2Z$<odvZ?U<2*mp($S^*ZKSZN12L_(^-<;Y*B``5VHH{P21F<lE=w*5ExmzzuR_r=)vc!S%K#9bQYJyMoNxZ;&}OCh@|ABymFUR6#L5YdH9v+m^-vsq0Us036KXSgIO@uqfAW|fb6L9R>0`eNpmhW+3Z<gb)PNTpMtan;B<#A8zKzzZq1#sc@~l}+KAMPG-!BB^%iEOk<MMJ={6?EdEw0Is6PMbl&hrv31ro3x76R!#XeH03oL@nGrfbU5HRz+x^S}6-E;a?f#t=#E%_v1Xo&(+*6ZJLkj3p(_$dYDZ24rY#2{@zscTr39b*c3rfA4_Y`g1ldz#_g()nsj;8vaIKZ5_(Y0@3H^@E%r8jS8{`vG{cj@FsKsJJTNC&qx$%3Qmbrhd^4*BDwvB)7l5Hf{rm8Do-{UNvwFY8|+AQkU$D47awEJvoV%MJlLQbn~NM$0IlxOpBiSvI*D$t79a$`!rm$&W`DRtoMLraH#-(AU}9MbJp-Y+j$JDza$%C0RQHDVOOhG~nYnuS)0*;hpX#J0teZYUbidNfES&Jv+s??fr9@QW0ZT=Cv<3uJPIbYL@k&@4iTLF8rZu{lKcI)@81Gua;QK9<L~A+iaF3SpuChmdcj2G@`e$$fEyP>)iflJK0HDSH>ySWAg<Yp&GIf(Wr$PkiXCw)?rGQ_Az6|w9cz%$7GpoA9pCZBSJ;@yIotp4d!%(QKB7EmjLV=<!3@4&-&*GJFa3M?^mjU6y;KPG0TUC-w<vvupe{|?s?paroI9VNP_i2<Eg{APpAT&m;NPoGnp^x+OZNPKs+cU6YOhe~0y)~ah-%2+ZQ^=8xqFnYtW#OuS$R`p$o73D*yW;X8Nh5@gqavW<XU@5PZp6xV>2Nyd+u%~Bd3Zzya-_eZqSltm@~w#y(0tBza?*n6$gGr4K({_Q!m#ozuGCh{x7h}FaU=x|>wME*^VjB^(uB21CgBH9ub7z>nQ`9FvD&l(<od_hvy@=I+J%(oH9VB_jdOn5smkwji|3otdw|X4EJYS8>miq_tLlrvg%M=&){vf^(|Hdn51k6y!}Ftim_8Q{{ML*QY#v58RnB-b5?h$3<UWWj{4p>iL0oW8V=bEc;;I5`fZOlqAy{peN?x;MPzu&&q>(oBpc1z|h4Ofkp?7UWV?4mQiUQ(C^ay|E(Foh<S)my>5PzoECvL(x^lgH|muER!6FcA#EX@tk7K7S;SOn4>?gmd3Vf$x}$tbDe8N(8Arm~ki#`jix&oRm!Ch*&{4_y-jq>i24c#17_;bl-qBsEWxUAn^HbNQCUQAKgSoX+tmNFRe9Un5Wa$$r(Oaw33_A_4&s_lQ|6bv~DqJ45Bw&P?Lm(2`k%F-(@4XpeKo6`oK%2D{oDN1?#cGSQYihM_+OwinWxJgt$sd|64<?xkQEn|YQAPLUOqHE4<*d%0m@Zs@xtxXol8W8N-n2(*W-s<Ix*VSZRG?!b3PD8%vF=h-fa(M%<iICZ$QO7PfOVt1*arCi<wi^u}hEK5;D%i;^ljugutbgG)ul>Wp1Y~_1k6u?D<C8-&8-T!ff_MTdBusqm8F-r4T7@#PH1RFXh<ZMl%RmpFds%)z2mAe|H%EXgaX@2*YLhD!-qM+~*mPJz@NGVJNC!0>~4Wnu1Wwe_VOzZ;6z@}x`m~ucE2+kCnpgiYgvRfQ#G>my^g0Z2QDHm9NT6%dgh3c{TZcocuLYo_ty~otJ2mikj4KDXu%XXrcEJ3q8HN)Btj&qJnt}{V}9~0aP=$h!A7+7bk1q8Nbr4dzwoR5|&4ivzKRr*zvT7!|PW*=Mb%hj#}%t`NNnf@5^*w<sl;GYbJ;zg)6AAMCmx{>BB_#z~a0YF6#l;|;$)fV}FPK;-;Vf(2f*evFlueFFH%bHufS@I;g;H{>7vF;ASK_WBRb*OL#5nKOsrl7y~IiI^qU;;^q)@}4b#f<HP74)9}<aUmH)~*f1p_@|JC_v3h1P#Vmcw1R5$gCDb5)9X0+=5Sa8kCJTnR(vT@Uy(Dt)fSUJdKsZ6&M)~?c*BVZ!)KBgD{8Qwl$zUF>gsJC9}UQU5_HO1m_HVlr()m7x2)ar)}OQS0pKW4`s%gQY@utl4vV7mEKfEWtcmbmCpzVP6xO+FWu8ac6p;MaZGG+JvMA<<t7AQJf^nxiNjpy$ecHv^)wlFs=a0Nw%3!+RW}eiR4k=#B1-||@4PFH5dmQaMY)_h7W!4C)_6FDu}|+xW(CO}z&zm#WE69Q_@{tZL$@i}BdQc)@_7+IabG%6yO_Hs#VtF@Oh<VoF=WR?)&dc#RS;I407d3cov1u#qUbKTj*QBR6zP9~z4MUbFecw6-Q~k^uU4H*0$?}gKl5tFF6lEs;USA@7@J?(K|<QWO3}_A^I2|#%|oiQ`sxT$(PJxM`#e>fF3Z5VPOqxpQMgxu55=#B9wVP=hIuK`oXp{tezSh=B6})0T?R*y8|m^Yvi@p~n~3vn%y+dtP155=C@mE1B+K$Iw^}zG)$HVUz$eU<QQ&ghyD|1SKJ=w=X`dg>@Mh&>h~rtB{)XtxGrr$gnkiaj-CoDCz6*UKmzJX0J#&@Ql!XKyh()lkBdah0*CxpqE?ODB(6&HB2!_3(B>Bfc*N&1tC$^_7AI6=PloiWRtCz48_fuetQW!Bi4D9lw!7t_nN-5_Uwmp@l)9TSOY?b6X&O7nu4B(;p$}EP7{G7))xKdOvHkY$72p_~!NAOqHIyaEx*h#s=`>+)FHm*fzPEC$3nabJ?mjr#NQo15PcRUKz`I6<F&|RqmBKZu+<*R}T_(K-V>CzRvjN5C?An~3133aNaX%wP-_Xgr8uT4>ahgn7WT;RY5IodU+&pA&%yBTM;OZ%Kmw2RYEd<=Oi(CYV<=|9MibFl3(#HHKj$Y+8Igp}CBQm1RW7fM_y+QU(M&ogP1CpgLBEz{<f5h<EU?YbxBlhZxnv8!4TE0eIM+4zcaZ8wKd@Er79DfnpSN}B|a=b6p^o71st`kvHn<!()1Xsf(lr#LsJ(VlED5>2^{Y<9@^g8P!D!%Nw%W*P-WKChq1VrVckDUVS~Q56^-NE<FG?lpBosq~&RiF1o^_rX3Ck|C#gh6dT~OP{xSueAv>WhuY}Z1L`>(m@lfeGYuNx#T*4^tMChioi}1Q8y<;_uLGyEQ5ciHNK&r`nbRFv5a-npo?F-v_AasJ>kqUyPW5&3o&QJVGXo$){p&PZ1xM@I7O`dC5k0Ksv<7~(>I;dT5V>Gm_@g7^L7h!Qjh|N`QBaDu=v>@9|E;>ul$nx4EdYXbiWWTKegPLExpiUl4ZlSnczv*Wv_s$;p+x=2|Fk;k<T5CeAG>ckDydlZ<X2*F@O04qz*;X4g?qfF*xM5#Jh8Ts!$-Llx1e4?0_A>{A#T>2^s@diT(5=E^xn8S1D+gTGpvg!k9a!6gj8xO{JXo>JwhFs+p~kDg<>1o#!!L=><GVzlCa6d~o1Xs-kUAlweBnqtrgH61hxHJMW^NGgUr9@lX}cZhNYr-5}@jUf_<4mndfKOd?h(o<TNjvx!VamWQ;*yMRuDkW5bPF$oC;q)G!exg8USYyoLKK!!EV3EgkPwd2oh1?2#~0tpN<$qNs|avy9PU18nFrDBZ8H1{aKB#kx>WsIWbdR9Pn=sd~tA0sURD^J67{ukd<^JrKX;PX_U_0qdyWOG)@&H-_yWc07jX}>BZF8Ad%Q9p;Kql%3M$7HQ1bDmznpHY>*+vR>4@8j&<S7ASC1WXezT=8UlsWB4P&W;t?q&_GG?*g*Muugur=?KtS_#=$e4kkzM5|HrmF4`hL@{+dTG)dJQ%So~G#cP_B*>vy*$_{McLmJ66*?k=C#5UOOJjMSMdsyK+)K+@IXvc#4jRI%v*(F3}a*<DaV+xI&uHM!el&jJ`twO;_(z?op{N(0`>ww<ix=-!@wdJY!g{8J}j99=1x22E>vvAX#YMy){f4SVWC538ib&(6&GFEZ)Yb7q)f6<f2*zU3!t2DrbW(9=4zT6-*ufCbtd=wy6Co7mlCL>$5l6z-C_1&o2m;$kOGHqtbG{E|opG!wnj_UYiZ*uJZtsU?-Fi%74-+%vq{&=#bjojR6WR8y|JBnU4<aelBCB@v*{be&6D>3+0vuks^XWw{Tn{CH2$__SW%HeuFPiIPjWi=A+hVOW~_C5^N>q%v%Q(>C8#cFVROU@v5T=u16K4=TNYKQ{o)YW+IoZ?%un#a^_X9hz8uU4st+AxJSe`^h5zgMgeec5@L4`1K&le*7i$1+(NCIIuw9&@fUYMb&+qH;*A8#prHTguu2{eorRU&WGr&sRz!MNrVJx0lG=3~^yE^SIuIqW0XFX9WZuE=)bv8{ubnnt8Hn<g%vgZFE}<L^6x`ExDS^=wj`%Wr9;u4K)z{6pOOFW}sW0x-*MwLp}lcc!}Ubfjxxi*So31^;YW*O6+l?$5bQ00|`?%p;*QXH9^37TYEKHK%GOEhki!7B>J8}RcXE5T|<Ez2hZ7-uNT`>a2z)qfJ;(`vgH(D2K%&e&-3&!UV9<8EkW+dWjlPgLfN4#VXW@WaO;yev~@Xw6ZT=F<NFX*yzOUHD>C%OY_!jhbuhWjifqgUzy!H&OwaVyz-m#;K2?@IX67R=1@H`<r}&k#HK|F?{yr5G-XUG`eBpRp0V1a>@T#^FM|^xc=e!gI>_ml3X#{{=*VBXd%Fb@*Y}RrsFbh$sZ0ghJ;+bysnz)3TIF^OxI-0>?1_aCs%%%pbeiKSyVWOKK%4-atC7a7B^t80uG4TDxIt0e=Q4<Mua-H(ao+Kg;2C#L!b(A2G5KPtPMT|G)UL^-<9A3=&K?;<lw=7Q12t}A#cxvnhb3D)7IGS0$r-8Xttmv)rGI;FczKe+R731`OKF@b4x~z>(b_?O_miDbC^v1<ZEGoh+i|S@(m_iAKovXRM{*+$B5XEq5A5Qk`<K2<^gUe+$13pH6_Yrkh)D^7ii@alsSBP1KN%4a4z$FJI)Zk0UV1`clqS)Vnav@OIRfXMdn&UJfQx`3L54B1syn)esd_@{>G?z0O%0PhCm}M@&iyr-bF5C?9?5pHR;;jHGTVqmb>NMq<BA>QCW@+F?``v(D>e%7v?<(l=Qdf+BRJd^}>lJNI!zsj6R!cBiHi<k@1;)1&`lft$O8q-$P*02Z>nxvWb_SddBKGqjs5T)hTjcgQCUk$T9j5+OhrG4u$^$|@6XYWV9?XG0S)0z^k5b0ToqBw=jq*-br612N)D3*Tk*{<-<qZEuAaT3Jirw{_5A*x4Zyz%qDShW!q3`@z?44`V;b(dAnvQ=h(Ee-a)_9|rsG+-zdom`tShyfsKL_SE9+l--+>2j4J`8`AmM}twW(;c-SWcTGOOE)%^}O9O+3;1W+AtD+5*mI~h?*ZsonS(@SK?hR9DSIw`)%o^=*A2&qBB|0GswKkmRtjLnvPuNUDi*TL&YdGzbISIyMT0pB&Wg%^BpD(@R;KDK{|$krij-aXEni0W0ZSAI{xu@-MOCUehJg%aNn>-a7D(7m&;ZJ^j#JDJDT&ugJk#`@B8zi|Lw=$e);W3`0(?=-?xjy_WtXSzlYBwTMB)G1MDNL?y=^Q`Yd9Xn1Ma}04{zBe1i}mLmOP{!9XizY(l%Xa2H-*@y+cJk82jcAg_J)MfI*vHPiO{uOG&L{pw*BvL#01^gDdbVcsgdWvsg^H##9^9~!RAXw4*<XVFeQJG%e=<D<e-hdq<SE)UD-s&D=AXWs-vam>>aJ1d5J?JFA=8CCq-KmYpcpZ@Fjzx>-j!xIq)_PA#8$4*1nB>GJW<zbm!EAVyI<6p#VJ{Eo`+_N;DGc>H9V63OnKepc!3yEvmd<Wbq#jXKxON{RNOd~zL0z#Jd!e=xzJdW_!(ZlEW%bM=V(=Pgb!b8Ig7}u4z2^kGk)+i@_4%fLS3#a_#@H0j|VQ2{A;FUlp%jzR!J$mT(#(T2fzmL8LlyI^<^{~FE922a4_nY5xspWLa?I7=pM8`&+KLKMed4OO3{@1_#^6OzQAE*01mLYI{wTIF;#C^Q09+TuPBK+g(Cm65>6w`;hY9f&V-;2!#$(*90%bY733=j9kPIK`ALC3}dyu)Spvv1E_vKRN@%cE)i#=1v%j7m~3nLSSV&=R(up`l5lrWXBa+A*W7ef7OR*Q+5!qO2L%(M?dn5jazqjyjLp=9dT{)*n%OT$AMAvXsg>CYasEIpE-$?9JVjPt2EuQ$7-jh~uyC_35*3al@2v!~TNU26Dly>WH&I`|$mxV~rRX_E&W-zPH{tNS+Sb;VIm)YTxZKq*bIfsOmw`S$g8WHOY@yJ$p=Z9cyqS|M8di_y3S$f{&YW7j=h-Gz7r3$C7{kapHWmg?&3kvireALFPh2spG`jqsd&n2eRUiIgGcP|Io&C9yov*neGe8v&UEmx3Szx>OIKMAM4nD+I)VG(G^JN3omUR-MYcj*t8DENaQ(#2S-D&B1OqX;75%&6$(eNu>i2(e<qbgKiN1A(w`=n(q>^1Yp&RWES*0#<ywSm%p`aH1D6mTk4<GX9x?P=33o6^=Q*{ZV=$8{2e^X8%tWw}9phNULq?Z6M>)D(Bj9lzn{w()39#{dU9hofM+8Y7qP8VGFvi#s$z-D8Z+#iBGBw7Qx9EW&&&J`LDE0;<-a*$(Jld&1=C)wiNCb?1n*%XUwkGZ+!lWrHzY1!)myfd}HC~v$o=Rut&8sgh^jmgajydf;eJ9ZjYk!l(p5rw1j3RoMAidp+QGh=_x!7|~d?+{AlY;G4iaU37D%8AakxuK-67T#NO9%I$mg?m>D90h0?tRTNAgqN5+17Z<JzdX%ZDnB)aQL&#Q|r<~1**h%n)cVSQWak}{`Glqi*uGNz5cg^sti}<{`}*|Ki*|J<$Uz!(VYutx8Yww1iObuN^&gO8?&7An*Jx|MJU?RNNg^_pE>t%PY(_Oi-Eze73^7slqLHbyxjy~d5m&%v1**Cn#we=7$NV?8yD>3ALz_AA!!Sr5_3R5Kz|9O$h4~2$FCdbwAo7C&1EoroG|p9R{Kr;0K2d~L>ULN_I$t>gQSX<79aokX}e9?Ya{rJS^jf<*u+-QH+0NYngd2;hWcI^i!X3+qL-Z(+S23K=l~NG9^#;m4g;T7^ti(<KXzRbQ0H!TqX|sPm=Qt&aMo-m1VE?x!mNLe62S+~i-8zt9$%*C5>5Cj_}PS!NPsd)i)%G4*7US8m;rLmS$0Udoq`|b_Z|CF>YmCB*;`stInD0677A>nVJ^P#279n@^;8BV18P94+rScI`kV^Xl4RT0b0aS}B_}J-_1wZnP&In#kAN0Z_qC)fK`EdqljL9}%4zY|wVTHb{TGvScmNt)RW)j_dB>(Tsftz}QUJz@?svK~tbDKbR~s=hHAz`wcG4^ATgDbsxLlv3-fpE0iSDngFx$+cz%Zt%9d}c<@pTnG2$g4d4gtvo5n$uZG|)emX?#baOtWYpk<8>U42>LnB6ANq)Kw^U_QU9A7?p^cPGaAG5>LeFD207Et$Tp^4W84isIl)h^SY`Sb|}{<IkM}qn{K^iC$Yx>R^)vMr6ysW8aarMG9f&ORy?$3PTN|#<<o8Hv$6o0p$soAUR7-DbX#p1(-^$7H!JRjzFyN!aw8HM1D0mU^<u#wd>2L?MGzr6a1_H@Pd5d*mIWjKzT}w!f*QEcsZPWA>f^G0@0&6;049K@im@t{9R~gdOb?r}5{F|SbGX~jQCl+?08USSBVL|{*MQ)PL0XbAwWz1cF1uf!ore1xY?!`Mb{?6#$(-mcH{oLeU5wuG=r29e1vR~COcURZwg3wuISSS^LX)fU$Tm2u2w1{AS*}LQhpl9v-KlZuNPZyQfclyhkK&}3GOh}5$wSt)LSK8nmebPF9`!vejm+PfR@?f#kVQ5h#7QATnOZNzgA!IXE<-52fqNf&_~V>zH9<2=u$Tgw2xjQQ`8&-ww~qiagGC+?R=jbn`7x}ir?>VCW}0}GkWW1hxX`3cdhj1}S-N<BV^j<X#z4zPsf0H*P!YhwPNG2DeKS(y(ONb9w~CXU(K*XU6L?C6B3r(^4QL`RFBeg0nB&#rn$!$&sh9Z`{AxO0mS#d9b)MG6CsntZrZpOhz`U=4=dv}I{cDz4qkEb+#;gXujB<9dmi@cBgA4dxzrihkfuVU_sTA_RY<xAP+$9%mdOhpl<{jfhANyc)^sSQ%-A%IC>l)xq=m4aq3=W?$9aPJm688v!%cyd2-U2+WeZVkR!dZ(yPstv)F-g4H4d%t_rhQM5lAiu_I+n#1T#gxm2uz~D-(WJqXzni(BlfDFK;SOy3FG0&=~(bi)@j}BsH%YFWrh9>Jm<PdEpz;Z*<ey#C)x{1iW_9+W}SPwPjymoR_lsD;;-~9bHhC)zcb=%Ijodh%~E)jHG_-dl4Qy?6uhq$<h|cGNp!kE14x!qxvMOO-&2Ssq%E9VW`nnz?JUy*f2L{;4skbn<g^EyRCt1i=1WTCXC$k(rGQ#==wi$Y&ZxhcW&h((QEpM3!P=|B0*_r>{VD;wlgt@`>+<z3IWC%}Tb(vPPl-Gd*b>0F%cPXIGv>|aDRf!PSci{P`?ANqm)<7mTcM?=I2^-qtIx!N5T)XBqKg8|CU{M<&xr{&U1u^>n#puVpiF_F)F)ix<Y{M~X42CI)AFc*-O1~jDGkz8Q@T}(B!vrJo527?lBqLLI(nj}yWcyKs$kFh&MjC&CfV`1LGwBEtz_U}hLUX^eN+Rfdk|nZCF^FcmOC}D#dr=$J`=%9Q9kzBA!R>v&h>L6R<=t=gf!m<R|m)g^fHt%{S6gysAr-+xMj!OCMQ3Q4#-LgIdtzJax^TQM;JtE8Rpw;!wWe$hUORi$E+6m%r~XDiS2<~+BgGDW<X@2V?W1g^Ky{O9^L#>rQ>P^fW=EHAajekbOKD2GylE_bJm1;h>d}TM-eO$lKPHnp)Q&P&8-!S_rQ4%svyGD)8qNkO@N;Z2YxGnyB|Xw-I@&}o=I$Bo*QmG4lppIQc-ZoBfOwXCY%hreXZ{2A&}Vu=x92kz0^A9ffrb8RYB;%KE#s@y=x;x<w4$6aST7AN5XX;jnI{z6`C{vL3w(8;wFqk-zKOIhpc#D!a*E{vbkZZW9VsmdO;*YSDf4!*D)DqHFQQ%2Arwv<&HTHs~heZ<qqTf_UuE~#AEFQ&Mr&Wxw_d$+%!*vO+#CydzH|*sQi_akRHg0W6<Mk?4v)~ubNa&1mu$=wiA)}m{oh{bI<ryL!rAfDL*&7eiq{rOL`GuV@_Gb6Y<AjS9{|qx;t7X+QG`&B94LWh14!jVx%r#R-3omV_1G>o@Gi`WCbM{g0eWh+=DVV{C5&iZPNBJZ<qDY+QU|W0goj#Kdct{rb>Cr9MkEw&$C@!rg=%GpXiX!l@QOfgkw{2Jh{9H1eOJ;S(c&*fKK@H$&q5&gHFk0+LZOMKU?`8(Ciy@Fk4qza+_*M%Hs&_J+O*kd9a0wJ}K@Gkfq2mP!pZ&pRgM?iB?!pam&RTE(apWcc;@T%q>(V^1Htjx&gBg1%;2WR-6JA;F{4!5<J-y3iyVhU-L5BohT+S2<2qc;&e<xAb^oUzC16J-L+EVG0jU8j82f&lrq`(b1J>WvO+;seYdBJFyWn!$=+jX+=Kt$hz6H?tqVU<UX|!=o|<9ZF5$+9q<zw!a7?hIUlqI)19Z=XVADmJX++hua74Ql2MX}(D*dWi;lapM|CY)Iat&+7SnqgSfV*yPS~2XlIgf=0LavMmmDCk|-OG8M+yW_s%}VHcI%9HiE3;4$h>^rDcv>V&17Kr?IzsR>9ur(`_~COoAVclj4>X18<>AO$i?gy?fkmz-?~e=HYl=3F^mu~nkkD>s1S-U062zAKw4d|2tD6p#WLno4yFlpXFxnbc#(e&hTL#OU@3VICSgVLBFN^~9tW?spEeNkOtBILalgRJlRz~tQ-DuaR=VcB*%gfwkepM75Ru0=>JWsT-a&*7RoYRfLJ;DP~sZ(UQ!ZUu|l2TJ<saZJ##i>b41@Ph0^2S`~GXTw}^ESCEY}v~xGxC&GEJfQy8?veNuPVC3+`6m`M}T-bz{PnJpPszSYtFND)DnAi`#mtuhxuFk)Tgd<WbPl%3Y(--)h5t++v`dBs>29fFIIAp&(rCw>|>wyoJ=s1;lh;T3sfa@E0)f%vxbHmzUf@GNAm;C$-UUlNh}=zV9ackLZF>2sH1`eCvv_6`&ytNwrb0&g`h}d8_n&mm|3`ZlhjDBF>C`H;GxT5#blQxtw1*2t5lgB+b%+0R6usg{Q_GOvH#CV9n&5Y(pN_!mc?L~=D8aqNyVbyyy>|V#e5#Cjc(F%n_ktHq*$;5YmZ+lJw`s$^z%|8<C(#A{MJBikqsA|)P+OLja+&acAur+{s_bF#(Y=X%_8k?gm^_^QnC`ja;r7QQAJ#C2YiB583HZ0y&Hg!gCk#fnzsB^`jy`zyoaXdmO&B#_oA)gHZh_UU4K1IYSU&yPQE(`>gOUSK;(13wj+NSnog9MSZ8G0v4~cD9(CIz3uzZIwW-elRIYXwad~hfq10gEQ-<lBu4G&+w3E<yjA5dv*2gi>wF7FwB`+v3kYO&hvpCc$IxOY>M8AMiC(+LXPvWET(zFHKc|=qV3~sj!TP4|#^IhDG1LxQmm~zuB%Q(1-dM~#4vrrQsL}k}E?8@fma2z{Xx_Ez_0!7EQ2u;Ju(Irz^yJ4)LKUj*|<mZk@+B*5PoD;e$*;6E}18K8W90z~Mf}dTwwU=>wtx2bO!+uWPY-t*}s-#g?EoPFy8?$=zxxj%icC@)vKj%F8^oN{iD(ycrQAkdo_c7$DpkUDlBw&s=2SFc0T)J(Jd?u(CkNjy68-d~93#GLbkMf@OAPM>}^_tD+LD<}4CB>AfJ@zEM68^elq^iDzY882FK0|AC%1<s*iJ^2zWtTpUW5q(}u4dC&rtTegQ2Ihr<-a;?Xy*Z!4O^ng`O6o^xo~ju(^7#809|IO-vixaX~U$Nf~J({h?u9U=RB`3s-M0agsVLna>BW=%y%C#MDZJPZ%%(cyJ+c~H1D;ZOQyUA_`NL>qf&%*)P$Gi<}wulJaC5$9Kon08jVg8?eg$0gMY>~7^0uhyuVPijCBU4i!-{kj`#3AF~~9%d6-l`zuN;pC!Jz_fb2h(WUJ^p;MJI2T?f|Snv*TD-fVdWW)6~Cmc=Gq;k|m~MYsg$<VRIdX`my|x1wpQVq`3_9ALL<*j@8UnG;<3dv~$S(x!NP2tYBsqF$}b@|e};l0~ZJ#!3-|uBI%}uZ=0sA1`|azYcu>uuItYj5P}GL*}Dyn#u%kv3k+fhKTvghcb1$nhrF$_>aLM=Purz^HYVgGiAw>9I;Pu`}`uUHp?D^+lk%t15R+8RFkrr{xQ#~Pq&@B@DyRG;BoI#Rh#de&$`M=gtqpwkQXDIvd4I(U+^R;8A^BY34)KSN=SI3ElI7<?>T%}Lm3s5JHlJ}=S=^TFpp^7=Ne{Z5-0RtpfrpZEv7L|eqbpsR4L;&(oT$VS0u{_Yl90HCa_$|<!}M!tP+q)<z{SJMy6ETq9x4|m|$Bux|WvvO?Zg>wXWbmz*it!L?+pce6S6BMMMJ^(=jgC+@t)~H1cAU>x=>#Sc%yoq9x0JjI@OMJ#EwZUwm=RqhVcu&vSlORPKsP&{-ur;l}lJ(7!sT{VFZH+?UsMQ5}MrDsUSdleL~XdwO4fM&15y10rPF0H;d7pbtrlCKH9C`Bc=(`a-Ab<0x%XP?;jj0nKPwC%-><1o$<oo#k*+9TSz1jgNQHu=<e~{RJCODu`=ef_#V1H*mYz6U198yXb-AX=LeS2YIv{+hE546f;%qH-;}$TR{h-9Sc4?iqWyJmyqtsMLsQ%DUox!w_9hluK*CV2nYjG>vH=nHp}Km{eYt4x=-!@wbjA+g{2&Gj97GAZA&4;W+BVDYy$a0{&Kl#Cq{9r%d^nN#fqcftA+OB!8|?wMz9fe3YG?#Q04d{a1=jK+1$s8-F%!R)fOxmK&Hf<n()1|O#N<Dc}y|w^8I-uE$7b<dwu{N?MEs#l|8k#@}^3Ls8Y)BzyCjfJekNw1M;*c$HyeN27TpUAE`H(?k}6sSP8bTB66GCto_F8<7_*QQFai9Q<~xHc{+0kEPavCXZSbjZluZ{H)r+@2IM>HO*u1h6{+snnuD*iM*WU`shA1MY@m9;z<I2trpr_0thdW<yC)b<c{M*hG@B`$o3ril9lckK3VoS*wGZFQ^OJfzV|8**5*m6Z>s;=paF{3;5~BqU2>6yVVn8`#+4on0ci;1s66YB?G-|!QM4x9U#Cw^;^)?jIc4HpH3nFHiI;>;rW_Ox-YH8&1x$A9o+bTrriMS)Vj?w5s@v>!tQ&KHM5Cs+Mt~}?jo4M+!yY-yGteBvQ)JK7u1~h5EGjeW_=v!~K?x(~aH%eeNYC(|RbklzVeA0OG>uv4T0s>VDUCj9z$&Kv6y#R;S+ubz_7+QSJwtSh`4uZqC*{EBR){`x?04Ug}!F-;lhpE~Nd1s0LPp;PCsTE2BUc!@;Pl%f|-1@{dZADn%g!vsceK4xh{D;1PjCL}z&Mvq4l8w0lZy?u=>E^x~G%ae`r^>R&ta;?w0Dge;@H()i?z=Vn`&3L%hYZK__2N+kh?A}`sgmP&M#Hyr&PzckQB<##76nLHJw13u8__hD9kW@>&CV<!rSiN_pNnU@)dk~Hed1Ua`VMKnf*BAnD=?ea(AATg=;jCR8gXaIGjldZEunV|e1EZ+fYEl;L_$4g2d=y)*6~n`T*q5S9RUdrRc&5`aZ_Sma*)R1#T*}`bV(Y@;^d4_gqa20L4D5gJagk{=JcKh=F<0~x5mrYv5)%>A<9mS)BpLb-Zd0#^w?X#U7i;ln6TK3h(M`7y^f2SbyR#~7SqqnHN7R$b>QGYH_`X_oCx;e!CY<d*@u%f`*?S>Dd9qzt%MH~a`$0#S7;Ti@r!h23RCdXEyh+Z=?)(A-Ta-hE8hS&g&t`@@eGgs;w;B89m$u&0D>i^8ZZy=EXpG6AU0@H^g2B9&7mn8o0cPF)@kUJ9*cb~D60mgs8za#FFJ9JrY;$b9?qgp*h_o!Smg96P)qWJ)8scUVIRE249zi}jrFGqjAQtQC>b&=B!vf@U82WmDj;84G}eaKtqMe9T)16bSRXwYq%q_e&iH6r{WFE0k??MIIO=(8qi+cAwmv#!(H5_v$#PupwLM0^^{Fp_{D5zeM9`?oNmT-*VZZ~K9xpr3NTfyVYS_ElPR%zzsY(UAAo!G~7Q|G|q(Vf(E$7q*TdKX((ZIHk)+N$<-#pp`;dDg}{yEXw0cO$x4PECN6FrYqxi-K%(;Q$mp<|@8Et2|S*(<_@o#dblBg>Y0DYQoWIT-ctpiJjA6+gx;<8o$9oo-?F^T2>P-L6Q7V4d%;^}N=<(q*iC3ZVxQiXpGFie5p|0|wSIH{vB#u*9lGi+PW;Tp{H&3VpXe9NKxx8=jPpQt{3`4l!)izRr-LQpa=Xnz_JtGApg#x$c%uz1(iMi2b>K^I<>#_3dM(BV~49E6naci`ad2dO5Qt1!s%m8ELtQovrq9YFan1%<P+{rDqu~n*KQd(pOmqhW&IBN0@(?m>%W_GIHxLHn9^Xh!hYtlQ?d!3W(d>Ox+vU&M^!$MSQGq?G4N{X3#F^`#=6JOJa=RCNCiuuwde}(u#}~w~DO@%|QENWlp*c8oGUd=JoyU$KQVW?ML|VvkBX`3t{y8uRs1CKL1$>GtBLgS-yTV*z9A?B`asd(=u7N)(D)Vc>M6=*CE*8d*^x^D`jj#yS8u_USILeWgUrY7QcuemS325?PA7rix4jI|NHO%{{L(5v)2')))
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
