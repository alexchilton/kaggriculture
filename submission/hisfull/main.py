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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_NmktFzE_?!>n-|qKT?9L?{+w3Bm-J953G>EyoIV^D4!(n#c7Wdz;s=_@o!c0^|)I5^p+{_b`)tM3Yp=PEkDk}OvfA_!r(|`Zx-~BKD<$wO}|NN(a`EURHFJFHA-Jd`G<uAYc?d5m>^`HLl|Kq=Z`G+q*{<nYnm;dXZ|Hqe~|I6=w|LcGL>z{xA{Qa-r{qnn)-@X0u_0yOCoqqf6|9!dtjGsRL{L3HX5BcK{KfiwYuig(|zwy&gKm6&_k6*s<yU%aGd+Dox{>vX<U;q5|KNREm%jaJo$MI!)KYaHefBp0RQC~l3pYQvi?|*vy?fY32-*o%M>rfuP^6ul<cm4j?AAbD)uU~%UmtVh5-TAWX`agVG@hNhGKYse|)tFzkqs5=%?|FOu%P-%4`0kUK(*B$7s@*=gT=&{q|ML3!{g?m#r`I1p{{&2=TrWO?FLVCsm)oZW|5EIZ8d6sd=~!4`O5od$p}l?j<@M+Cr*F$dmi<3`9m&Hty#Mk0Cm)M#*{U_gt35n??`=opwSNDd#}!I%dTnji!q&fZUB8wce)u4B{onsveV!h^cfXgb?>#=??)#1_5-j|2yWEeUGAQqRtM#t8yI$t<`_(cJiDhQ{T`za>+s{~cu+MDWufLuC;_@;7n1%24*OK+t2aP?2^#sAff(PUS7nE%1J^=N#i3NTCY-d5ilXPl9%dbj(F!{LRhbCXh^EtJj1D-#yjrxTt2MYhG;l+L**8bm&PpRME+u!d0$@!4aKmPdo-7kOr53fJ}^23im{IBH|cl#vxiy4O(`0>GK9-cw*&+y#+<@LuOAAj}Bd4CCFoa%9T{Z#Jo`%_vvszwYIdV$gE@|gx-4W{heHOFbJgNyJUH6|E;PqmV5_saXne9SPx`8_q>+f8$|ttXH6{dPEWR|n_rgq@S``V?DP!|QTtZ=U?p)jRy}L&?APFJt)LN0+;VoaB2;@f2-i_0!7&ZT4_Q&Z2sk+4spu9|1w^^Q2vn1unwQ)60tx5;;D5HFt*~wVJ?9JU3d)TuC^8ay8GojC8Pa@(At)!#zImkDq@2Pi=SxS>>A*v;<$)a^Hr1B8;{7;SL^hf?4S!pEPga^gg@+u`?C#H+U&VoOrlJ2MQ#3%rWq*t-(y_9Srb8xvcC10Sdkwg|Sa$0qSu|M}!=YzY!vla7~6Mq`wkL66>d2CLr`i#EV=yC>iuW`(4R<?OET0V50hgiGFC?25@C$Ufz1m>jA&7#ls`h_DHI|sG@U)MWeUw(b9(BGW%4|5x=u(w6=cs?lV_-T4h$&d<s|s@BJsT)NR*o<=_{~30{cj`Xy*?mdPYsMsA?`5%fMAqJ~Y5(BOX+yEvdnG(;ZJdB+mPO)c{m{&)!{!8bj?4g7;~`?>}Xf_Y)@pBwU5<mcOab1W`MM3Qf7c=mzUW_(eL8y9g^(r(>!%B^#(i)DD81vyba=!4y?ChzKYdMy+~LS*$C$H|*E@2W_nJr^d4ebzS634C6OW2Af#0D?65Rq4m&w&uVU;a=5~9opIxiP9!54hnk4X~xV=#gO3Rwxcws)_P3<Fo0MIn8?d>?dM@9QI?gOl5@$|XE3l3z|T67%p|}i_#y-6agwj>^W1^wQTW6x2uxXj+=<mE-}C*?pZ}coOh5=QwZmB)2tAi4Z~c0CY-|tA`Eam3h4a^|d~yKXfzLtIn}ROgnEnG-%kgn=KEcKFB*^eo>hAW(^%9+TQX|Hb^|X;iM%c({kMDL5)hp2i@8`l|O=o?dG&iT<?B6}!fBEI-PjA0}{rTtr3~U=k2I~9HO$?wDA_14+iPdoD-RwPIz8>-IDTx8&{Ke~~R^R=8?%?0=amGh+XXJjBm2U+b{}hlVX6fD=L7UscpzTJ)GO|$rj@u3MWOf^ZlMNiZU_R#vd`(GhQ7s2Kn=i>Kx@=+*dJ61$54p_Nn!fKkOqxjQbTPi$BWaMXQwQw!!68WW0zCnAE9B1M{kaIep_fLsdVMl${{T$A{%>lY@6PMz&tLv$HeB!ni{AeL58$pc3cCYkXio+e$2_;f(=S)Y_o_Jc{jZZj$NSO;Q&A4j?E`|OK?@7MHE=orcaZJ@ZUdo$B<cE&=UB7Z!6@qp9aPwYNW6dUv-OS-1b|dbdva?ZdY9dVYLOnYD=~TR{-5e~OjJNuV*uBa!|`Ax&|xLWiyyGm0|l=`$;>z0l)CU#ela+BG)W<gO?8b796UXN>heQ-THJSLDDYxYIaox<JxH6^;#+-v&xQp#p-+uQ*H8ff!eV;r1*1LKrNO<Dgq;OD#mG41DBk&!xqyw90n>of=kS#9;P#upm*9p#<Pmz_9$cxOUX>@F8*evh8uD+ooA?;UA!CAz&_BQWr6E*|!nBtq&{Dbgrp3KLRA4gM%Sg}##!}32(rJJH*+SVyvP3B`x`vDIu8&v##M;4}#_h1L`d$}YxgY8;SoB7VTI-#Xh;?iDReP3kG|Ymmm)1<OI}{k^Sg9wv)HFMAGp_p4iJzK!&BRr}*5o}IRzxlDAy!DSv%^y3sSu|SoDHLL(}%u6JS;e=$2j73l71w8GSQb(5h(RuXPtj%jp&KG-q)xCEG!gHpxk{*RfhZJ<$YU3?#apr7F(bZy&pk871%Yqi)aL4t)>dS+YTF1jnOGUF#L15-$dLRbF+Oho75J;*@AzwSbZ8*N2yD;-lsGa7#IfriNC~&s2HdOda+XV^2DMm<`$%5Cd)DsuJMP3NvDeU046BnCZ7K~O*eT6RoUYO{^RY8#E@(wU4lcq_hSYNTCZ4Y6gRI2ef4|3aeq($^uv$;anDw1eo9PVzkW>DhiQ&EmO{;?aOw<To!kSsaV2{iMjG#bj5HIi><A^%DK}aH%XO~oeM;p)ZGpnkJ6xX~P7`M+oJ@k|d<2$F1V^DD{yZatH)wpP4klSnv6NNi2>2Ni5lBmerK&@29rvb^QF;EmPo=A80j>$5j!MT$FfDxLdwRj`2iPpckX}3`3!R4C-iHK;RBDw<jId>y>eFzax{f)Hc#S+RtqB48MO9#D!a@LqTs_O=>oNqqtC;t9`_I=Mcp3o!IPoT#@rCLQM|Po|M#@`c=gs(!r`3@_AsUg4(si}{Z;d=qoCFKsL^dXW1X4^II%$dTwpgX;C&aoqT^fEWMc02+><Lmcnywkvi?H3QL~sapzlSPWwpo4ZjDhrwtXifbJzdYU{;XY}0({3h#;)%aO%W0r3b343#aT-9m&a1)R+RXRb%3Jcz#8*QI%m#kK(L8@+M5$qoW73@umY78no0EOsU{GRxd1?D`bZ!ixlScF%j-w11|@<?E4g@9*4$Xy6)@vPrri^nN}JqE^aix7X`LfYB<EXOS+Hf+fCz`Q8v_1B?$UDrGjlj?j_S2YOE8^)<EW2_^bcysUOu^CRq%b!-uw(lH*X~#DN<e^_2SsIA@D9a(_w{@RVCz_;K{-=CO0ciWCJxpH%|4L`Ah~C(V7{bIIV)woAKOUapnt2)A5RnqBJPCTdT`UW5qF#S~IxDQ)>>Nml$oJmXaUX0phQ{=r#C<&!7MDDl=(AVirlYRvOSw4TAAd&`)=B{Gb_uyT?cT7^BV|00E*x>ehALPiQRRN>^5Pz~2v9`A7;!+bd92av}O%e4zs|3N=1bHW{QqUJ1>#^x%wmwng}XQeDlO3x>Wq`UJ^Q;R=)*$Pn$A_C|3tqNHQy!`&a?gEjJdd5Zcey?=60(^U<aE)e<y`XN9k+$6Xk-S)<S8b0|~I%(&6KWK17`OLk0o(Fqu?p>eZRiL02jhfP(S-E?;K5eEvS#N|#!@4>xa#A+?yk<5XvypRs;4nGqbe(_*?!9Xj<aeJ--5cq{*F2_u{j8?fUS!IpEsCLYJB=yIfPE(;T;8WRFkVqE%XU@pH{yCcghbQ^%In=v96VB_{HDwKoSg_S79)A{P7wrm`TGTU8**WAw3!t^P}B@q_;DTT)=cEDxB8gp`>n_F&ae;@6v)wbmDiPf0_PpX8g()+C?2ilWh>k*S|i>*;pJ&faElrbcWYElV)4Th_Q7eSOGUe?{|0iQpVE33R@YtUhg=z>1dgg3Ubt&P72|LUDPl!P2*G1nhSuIZR0?RvjwH1qqa;G<&mcup{R`7jPs(>y-rdVH_^EXQ`u^4fuddbw8{!HISp^ldMN*tFT3JLW0q>8RydDenpJ$8M*y5y-kdu>{1;>>u?Y7e@-xV_JOSV>py$^x7#qjYyoS6AJC&m=+<2AE^WE~^1+p0vqk+IHKKH5piIx?Z0V28h)DG&fb8Vc8;K7x5^>8I{#RRaJtS0s4aMOp~9NQvC0J@Y(YzY#qzU#;VO1l)k-kPHJBf%Ar7_01<K+~u9!&R^-Xl1^C2jUNtH(xz_t)OkuI#W~^1KQJVP)n3fOc=b3lV9^=O)Bjvu0AWuxO5J>ku^xtT2ya$-pSLMeBWqP)=Tz}^QZnvJ_oC!Mbiq=4iTs;vAcXJgu#00$d&{%TCyPI)3`G#`gx;K4H&@3HRBJh&!^g@bFk_%S6*5<W?pSj|N5MFeXRm<<a?$d4U>8AZ2jhEaLJs;xS{;~57BSs#s(+hl+6B&Q?HOVo2bHnNEJICFP()#nT=IXDJtINd<yK9Qi3Ge-1gcHM1V3?g0xj+b74(&{)&I%or9yiKfd;MCswppT&*^Pp8<q52N$>B*LobbqT?V-QhwEMwHRnfh6M9F{{FagHZFv^0yUTb0&7iEc%Qa~pCDlpX&XW8-d7iJS1`I-N<{^hNR1`~<>k9~e^{oPi+SHpGtdebo5fw5~k@X=42oj&37?_eDf5zDD&Y3Fgq_r<ks}}>sct*86)tzY40R-=G{T=lf<Ie55Ghv$?%M6(TN`or8Ec@_JM4X&&P~HdWCfPlmjr(b=gcioabA!nFqhd!O^iijt<8y(5BABX9=?tW~5v*tir5&Q7j_I_xs*Iz`40N%LSUBe~QVy`FGKjLrjXo=@OF-m2aidBa5>WvJ)Jw1yw#uGe3>wgf!Qs(&x39TPQD<ge=XIr#pIpa!Hwr^-aS6K4nHqA!m|)2Unzv6$oxye*>U->D6w@iuuS1^U$n<yfQY6;)s>D7&1vF6*^;S-g(MxAj8E4xDTaUA+D{ZcvODAYl1?2p6S|#Zh4}wPCB+p|fE{f~rN%F>i2d3y}dex+|r7Yis+6pwmXiUVTF#;D`_?p~l4fHXx7%TMTi3z?kB7$T_pZ^J9QF>KUX75zg)6|Zy`tAw-pG;t$X{0rTVdjUXBx@@M*KSxi+KZG3{C!v=3?s}XY(PXg?Y&h~1uc<Hp6ZhjL686;eoSQy^08EU^KXm^RcDGbkq!~meM7HN4F)k_#t9Y@jV)r271(DLK*%6KdaR5eQp?K#D2<ftsNU6PN2PZqKdUTrPZQT$n5gR^vlyE7DOkk_05Bj1ukjgI;kr)Zp!Rxov14Ny8GGy<Vo-veUQFn@r$f=@>48!{@KYU2mKfuzBsAd8WlYfiNOy!}y#b2Z0EE!)5O2wxwkITK^jGB1=xw#U<6w5LJaahgZpmgi(@GAI{u0w01CSxZ^`)^T^#Q~EWwwWYH5GYLm{Jt{xWpg7MZ@W~;v73-#+RYkvAb5mBRAX9l2FEV_P+a3pT+Rj#9cjo1Vlcm&*$0Z|0ory1zsI+DzoI={Xe|^;Sak{`nMtJ67pX}9}HZ3$s^jpI)-)MIQku%wDV%MxySP5O25xbP+CGSRMXHEB;q_yrY!8#ZL1bZE&ZYljw#KR%TbW-P<3ov%Un=UuDS?M_&;_V;#%E8^<$zk*S<WRyijvW7d&kbUpD5IbZ++?2KptW5?NJaq!05PUlg%6Vi~GO?=I6xBH=`^?(WEitG~jhdcV59Lv6~BYXN#io-1DP!{28?rDprw*akpwBJd$ZWw>`udb7TmwPPi<Xs97ry^jnGx?7AC3~a}*AO@s`IXpv6GGW0;K{!UxIeDww;domy3b+-_j;+`}8Y)xj7r|Fe`TmDLfFou}{xrBQ^t>}*K#Hri6&l*YG>^;UwiXw+lV}?H^z`}TBmg&%?L{lOh4Ze`zyx%##C6l^sL;DtQ2=C`hM;iVVZ2u_SWTzVzx~~x%sv8kjvws6-!PNT#nDcXiv8y6C`uPajxrFh5s7ZhLJ~RlDSPBtXbhL+Js@$Qg47FXRTz69i>L}~V7qZGRn97~bA^ckCTKw*Z2%scL?0cZ;FopPn7#s21_r~ff*Sw&_VuhCjv!#Ex(yZ;C&ljni0XN9!{Jv_dyoQOSOt1RU`-{n-b_RV763mz$IY|K&Pof~gMcll$Ua5@z>rmjNL0tvCz+Yq6MWV;Sq+c9R4YyG=pr<-N_h4Xo34G+0J|e?48EZ&b8{10agR`(yRLe<37p^g(xd9bPyt5OUpsB&i8hHYAC9Ue?yZdd&7*?IoZ_c}foHH6mu};bjMMq@dhAKPEvDN<Kf#*8V=7=ym1MGrADQ{AV>?thMsU39)2%BOrtRYalQyWLF+|*?S0KbK^J3-tydH`o;J%;NiqoKM1G;)$I>!Mlvb);xFe7O-a%qC@QW<tfi1odmV0}D|&GEF7hXl7raUT8=bk`WTP?tbFaxSd$hso&}TEZ=~)mD3t0!L4-m);Of;j}QonBro6D2?j<DG0w?2FFqv@CIYQ7xpQBl1vw?K6NC>PX==P@-Hdq4?JKkS!h3d)`kMrL8Mco8RbrNJJM%F_%O_6m6_Ia9m8NbX~l+Gg!)>5=!t;|`ni(sf_=Cl*Kv*YhbhCW7r@!b%CAY6rBSpA(<l;Z^iI4WB8Qy}YF(7<`lCQN({5u8o?8uHiG)SG7PH@ws55rfk~WBSlMg8!;NX<Di6gM4^Ax6{W<svkXAC;@81Ty(1tE1(!cqcnZbQN1Zdy}Y=NmFKPLU1aI^MJnJ(Xt22;>onDMU4>bbakHs|L&dTj;_W1Qn=TG=+FD*9Q)vH6!&@zV8qqFtq+Kp2V`cCLY%H?JZ#H6|VbZkuGgg3RWrT0T{z%eboO^(qWE2d57q$;gv+q1c&4AieS`-2t@6VIfJNKxLM`kcd;Y+jt3IRB~Kec4G#C~=9kZZ`t-}^n2lmCBfEJRHJe;d*_AsjOiwXh#L=T^6fVW|{2?=~9I8M}O34v!w?7QK-JpMJ*N%jIO<zw7>`|f&<5XLWOdg%aXr_i8ezl83)Xd7^8O{)ROR8!iS%;i;wWfKgV3{BMvGlI=a|w2s><P!|F$vS6El4o+s@yGNfzK(KXI;relnjYLjDHqhdQTvVQ-T453KOA}-=!@IEmM#*W5d(z2f%>j1rEtbhG{;5fkbZ)xha910?WnF_HHa~jzK*tZ}+M(m^OKquuhYc^6xe<-rc9`N3zq&(wn!C$@9IyBz2Y6+*}sN_%aOjU|EAqInb-o5Tvcb#`MH%BrGVoe2u-`@V_N7k~zSEU3^~`O9PnRY07IFW5u{Tt3s_SdN4B$+?+_z3@zbnrbEqR%j=R}&|WhxS~o%}SyZB3)8gy2TTq0?OkES@`phGf)8vh*Vz8$PT{@Rzc3mk>!c;HIeKg7wkL+Id>ql#pm0*+-akRw)(N6}Qw1rvav>vh9Kq5%|yTX*RNr^!zg76tnz!AZ&ilr5a>!hmrYVX$&$g$+mp!B9rcCjpdj1M#YOayYEopD5hQ)PAa+S<Yxv<LVZ?RXU+n3-=DBE7lQx~+<vUOPM(>KK?<qlhU<4l)4&DKit!sZoW75vpY544%3i2cl7L5}YmlWeG=}z%Zb=v8kky6}CoxN|QfE>Owv7QE?0-#*WpVTOLZca5SQ;rMm%noiy<fiPrX+x(}&V!7ji|LssH#VBCr-ZN3`4w8%kgl;BQe8VIVAaDk%~O}2;W!`XQi(ken8Kiq^IMd$tmSD|a4Qxalr*Ba^JOjF8lJcDpS6J&8J>3BUU6mFMhC=tGPMj<=VKv>dft;#B5Pbr|pNEHyJ=h1Q9@Xasj^Q*EXld%Q`U@c44PQj@7U{brR$*8Gw!|zMKS&SF%cOM?^)6SJJ?3{TC73)VzMQVHZA5A@^oZxN=E384u)(n*bO<5r+FcvELzo=~qLf9~(AH&tAtRPS5_wCi-Xj!5NR9uS^1Y%NBD&?bS{4ldGY1@Dn{n|hU3f$;GuTCVWIDMNz22hiOPzs|0cW`${a`3SN>JWO3EkV9l9M#Cf;E6Z8TX2wXOi|o@_LiWZNp(S5b@Jvh7)xKXO%*e;Ck;Lb0*ENClHww(hEPNq1PMFexHwU*DxRp<Xhu+MP}o;Mkm0pQ<~ML7npsZen2Alntg{T>TV)`qeg&)dp-&`fF~Sde?m7xE1*_qMA8<z3K%4_kMlGfUnIrCE)C$)(1}lp6B1B$6Yw>%P-jf0lw3brJ8${+UO{Su9QmN1Y`il5QIimtS3qA6cAd1jtBypa+g~x-+k&qH+zED3@10&*-!8!A$yr!yLQ(dk3sc+snL*a(!?u;}f!}zIMHC_J3a$Sc<>yT>j^Ifl%$=z(&7*!)eA+bc3K>jKr&<Fy@<bh^=)N*+I+m-h57Dim@#^9l3<%#N&<2wXvIn`^rz7Xl7Mz3NL^`*ETA^?k}gaq?FH7eC9i6{YxOVkv9%L!X#bcq^8L%cAbrt$O2M6Eg;aKTvvms1@&+;5}t6?((l6J+FAp*(UGPA8vzt;ESJVR}*r1Ri);?f_#`Sd0vLgF9y5f~0Vk2-929$a+h^GJqMXe0KB(J+(Er%a@@okus#QC$_L*M;F8DRbmZ2;WwR6b@4>mx(5$#X>G?PlIIvH=dS{A8wdx$xw4YP3Xc)XZH+{SEzg$Z)yHixGcN%zooG75^*Lx0J!eo3k*+2}+t2Ue<CjqyWl2cO_o;GTqI_sJ>-ivnz-Rw$Ub-x2ZmzNt;t%!1nyFzqcIB*CS+@TSxKoay_{HItYS~kc1$>uPB8ADlzp<dgE0I1PyAt-e0whRpDe{yAyDqpBA{8fEe{@!E>ETQbAI@*ewyCmsGJ~uMQC+%RP7<FSS5mRNfV(w7qTJ|Qhim#IP<M>*oZbFjI(}jOYx%c?iRKo$O_!4OP((`mxbf$zjc3mg4ETEq5QX@3Ze=~=N$};@%}x`~kn}cN1hVl$$0DQcRP;!+;7<B@jGrXJwQgGYH&eMM-~=#1pH!|iL+c?lNm}5iP8CH99fICt^T<RvSf3{*w#=kW<J7?uJloVM^p&_cJHYHs{FG8P9`LlGu?jq)0)%m?)tZrVB2)@Nl7#u~DB*7iWN|@?s5w}IV8Rq|!hy4_IFoL+wJCnflv{XmQdUQfmWJrSqlBoBd{bptM6XSU0R`Q!^>Cus6u*96jkfNY+<&ss;*dgvDDPj6?SLer>kk!BwUG7dGg?38MA4K{N5Hw|0sAwg4pEhR+!5Dq2SygTf<ygsGrOIJ%?Y-W^I-EFASDoip;n~<!5rPcQ4Yta?pVFU9^%sJZ{9G>5OucxWDI~2KLa*a888KmG1y4^Q?Eu7E=rQI+AzfeKJn<6riw*YBgb@cuyf1)l!IbbZ?~XKQlExQD-qtxO8GRVsO`CKTYe1&5l#f;WeVlKDXEf~HSujyzIk(3JtIfT%f!5fW6;J<<kXom58gdN#f#LGtQ3kXODg)wDEB~ZlvosBj7PHzc~3j!_10(Y_^kwkPbl|1p(fI4=&H8IM?b(ZLI7c|!(>ZLLTjW17*ir2(%sme(8ZW>pwvcD?Gg}hNL$m#{QV<prV_~?34tbwET@4zD3}wPHRnu>Lirh?TVC_?@W_`MRp;JU-T|;aP<6;{cGH#x%;|k(EvwU<h;&(;1Cx433D_g8!AZ8A(oITh)tHpB6Mq5o?J<G_0l?>$8Xe_6vRj|La`e7cOWf*MnOsUnv2j}4)&_O9IO@1fj{n7n&NK`QJ1L-{%_uK2*2+f3criBBYp^DDwV5picq#5uPQ2R?bUuq^UAOMz^_mDdOz1WZ0iOB35CJuaHJ7Id=Sz@KF38<;Mx=?fnj6p2!g$FZkWj7`*B8a=!Oe?*#S(wAHMwFKDj};7NjSa5^dBK1?kO^y(x~AGp4Qg`Zl{5=(KMFkw2)wc(od7pTJVL7)pnYDyrB#dHXu>4p}VCYcUmAH+oA-PN~M^+wRw9YuTf*F%Y7=w=K(nQe^pcJ_id;e_r=Z<^CH$Wp`*g@B3Wk?-jE-h5BFo~h<8l_OjZy2<`y-!Cl_gdORp1}gNx(_6^Q}?$!0aHM8w*pUqrR$6W!jJ)`=uUHp2sg>B|y49Op0_+$Q_$)QqiN0Q@P*kwoNeckcE<RZ&@dH@z?4`SWLVj~>^|{tJ?2#JlLKGX~L`7@UJknV+M;10E^OYeoZ!<k@Q^<8<P|k*1CpGpHlOmZhYr<hAGW22X?5qMi0L%;|(jg6=VIZB_C+D91>oD6$hI9tozfK3*&>9e6?!j$8w|6HH6HpD$1U;gfazX6TnH65Z$)0Xdh6a;y+|n8I{{Nq~QfJQq`QtqYc<e*z!xIX|U3&3$uLy5G)e%~$B$--3PD$3C5C9|v*D6C3~1D!LzIk$s}nM<7#Hb)_RWW;CyViB~Qw3kI1^b>4vI8FXQ-Ejdm_{d={WezQc@R6C)KND3d&LIn)OGxB8kw!d-kR6`8Du>x_7(KGLuJ6^w}zymZ<aR;7(nPf!-oI9>dTt}GQTmgCR!G${=HeJk-dTPM2Mi8WQ0$?EeVwaklI0W|C=g2OyU?DiJ(1WB|4br<)&vpx*ki|Wfb*j5@<`tdh&V}@goK!;ONeF};8`2tJR`X|Mb21TOhW=4!0|@Qg4D(_aAtMslx*s*>UkjlD*G0ejZC6YW6Y8h;Es3vJXw3bA;{gwd`|1~05!cGi?k+jC6p@ru&GlH79x~;Y3?$(<GB^e4fZhFGZLvTA8b;k*nzh{q%>)R$Jt%NMxreG~#C9+#fS{R&6kcHe5p}f7Wp(mN4Ow%~5;v^KTcO}yegd^^&)!!xZ=9(rD&BBwGD6T$z?CCTf0G_##@QKstnqGGZYvG+W_UOv`}MdP0!QQie*h@nMJ*4|$xtUv2gObFib0=Ajtp^6rSfXYzKx6}iPp3cJA8@j^#p8J!~VN`Zh|03bTsLO4v;yxfDLG5wG8bn&$^>;op?v&bWUJov^=Xk%h~7-REcNy)lS0$-WPheJ?D(gx-P>_O4U&oWJ=`;c!%OKwUoc;e1OI{je}z{4FSNI+!j<QXzuA(qx%S;dtj!z<T(;SX--+_YnhGvTBN{Eb9ZRl3K933h$F4-!XAC99|$M6GF>XiE@6;@8hjJ{58PmNXbpY|&P+GF-OjSBSk-@1rQ4fqYeuqZ!&3|mJxkR?+z=s9>K(Yz8$vZAR0sRCh}YI^zoF`oTgnQgeB^7oqFY3*gxT{H{Mm#3Sx*xYIH$@1z`y2FU4j5i>w+o3k$?x3?tcwRJC{T4)G07Y$v-fUms8^X)}X9C3|;SpfUhBln=vx)C@FW3hta$#73C%h-niou06iYIm>g_14~5Y>Bfkl}j@?I%)PHAkq4h4L)m>1LCApTJa&Pwc;6AKBpcIjUSJ*F~|McmX&q$j#TeF=1Nz2Dn6rAh7xJn#V*(z#FbdNP0tI=Otd4|uei1tZn0FpvLhDNSD$SZ7-z%Y>gPeTx7t>C@5J60A@^gI6XMx~H-*iLZd{zZbgXLfu&-MN#MeDLPcjN#~&aSu&@lk+|eUl&!X-|nXy3n}Dlh2_zT-+5m3t%l6%e+kf#3ceCRh{a~aY34*Hts362<rgzuF9qeysRVnDZn1Q!6^rYx^y#t3OQvIBR8^#j9@nq;`-Qn3-cVNsL-MLMYGw65yoS^2RPQ$3MCCO>rDa07uutacJ&o)-8AXfQ=-c9U-rTR3uFmJ$ngLW_k7#IPeOl7zo^k-urap;!nS{I<T_klSJ>gK+oJV!rRO)%MgR|EF)~Gp6iqR364~XTltK%+w^vc%WTpnPi^L8V3jLJLYf8x|E(AoMqueMB0&^lM1nYLOorXRSs6nWHL|N5l}wHbUirnV=_B<F2=fl>iyrOB&|c@>r3nOj@Ji{B}g#kjiO@&msCHz#E$(<WwPdH@NUaccsr$f&kDM%k6UP3fJbcB-KPPoI&iW};1`Q3&<X-F!^8&~w|CYFD@IzINyKGF>j06H+{0LA<Vp048udOwkWUi_FUfp`3L)`r<bq7U!iVzKagIbEZS?-=#tBo3gMMI4kGZCI!7;A<q6nuN|P;^RTlW*scD<R;d(>^-6ZB-vw7UNhz$0gWf6G<_!)VH$oI;%5fD4NJ{~dbG;qOHjW(+On?9D4?lkY*Y7^>*9&VSL&=ee)~mJiKvvx*`Mfo-Au~$U9C+AIwidLdJ`ZrY&CnCg&O&B$a56931P7z0S+oCU>L#`pm{N90B3%jjPaGw8V5|AJHmXdfGZHJF1v}$2qS{1LwFDmP;zbqL{iX<V=#S9(+GJ<Q(XWl?_@;-)3_`D@(>Q%Z22IDv2tm9VktujVg;`N;zXUHvCOFP(+ftD;PGyFE_qNVC!VE1~#HqbRPozwzRI93+&mM(jHS<9ksNW=6312IzPK&Z`&y?}*jE3}GuhimD(e`WHo!sO^<|oQ6niYl6vS?ZxEHhOqU)?-g5MCMWs*TiU4YUY<<l{^?ua#T3cPhTso#|V;!uM}$&au$>-P{p&1Dpp+^))D;slvpkSUP7D)JAaC{M)}0oNcfIf~jNT!tct+&zycpXSlccG3r@T|M2jK!4lOyMQ=a6WzGH(SzSwV-nPvEW$f0h3h^V^6G~jwKiqy9epGN9L?6?*CdGex&?{Rg%=cjEVKw?~NiV-OHSXCNvh#-{t#6j5#%m%-aDe|?R8y_&ikJ0iwd(0M&ODV%p;M|t+sec%Fy+K{GXKo=<K8SHp`jzhlE0pp<)-cGCkVtGSpY;9Hl(R?p%wUG=Jm3gl2p^6sMo24^+^UP+=f!QOfi2&4U&AKR6RP)DqG7T{6_XmskIf>tPR7pS)p3$;`0I15x8u&@6KIY@TYZgOQNvViz03LDoe36y4m$*=c01YK^UzP1?oVIxtLCvG3n&#q@RJwYjxa33#foiA?d>U2VmTFh~em>@gph~e{ALdeNaAG8%K>OF+!^&U}WMM;>4K%*A<zttb5ZMiE>P~MpR0t4zyT%<Yu`1Atrr~mcpoPTkk`KKfV6=`KRjlQD_FqGCS@n!ow6uLWvXTrDiJ*FooxVV5wy<SMy)Ny0f-&t&9HlZ)(LwK~w#9NFSigj~)Xe;851`IRVaCzh~{u^Y#J6LG|(gh&{jRH3nI42ss16(w*LtzvJ3JatE$|j5M9ta|u2o%$hLpIR3$^s&ZEU?{HtWZA;u~oZKbk)TDkOkn?S&X2ER?ox`tg|Cf*cfBxxz{O|wupTErQfBvrf`UTxMHsi-ji(DlFNx%HujZ?N+`K0K&33bwa40EEPE|W{B_tw*S{x*n3mZsO`gLR%G{vFtN<l8r|Mt2S&M8sU6%uqHFjerbkz)vOP@FLJMPWn2&=>o6wcg6)S-m!alv$1NGy6&bC@#CkTzQ5%&KK=B=pFVxNVE_2~`sXX`^=&epSnRscgLc#i$%yqnPd%<1xQ-B8eX#X4s8W5JE3gpVX?Jyhk1dGy$qcqKvrl!Sk}a&>^KOJ_;YYtEGp8_Ksp4M@_LpCEktP_(<Go*g8nQwR$JFCE4CQ_M<BX3};Q4L1Gd%drUfBYX_7-7Td^l8SlZ#-@CAfabvJ~E<MA_h&SGSxY7!ih&{p#EBwo<PW%^BT(s0|`&KxHo53$xhyqE0%}I#-(xP`k9fmILkFo8bN_AhH<mBLa6r*r=x7_PKBC*G1dnumu#_b5*e%S<?aPl{{=FZ_rt`j413N`e(#Zii~0(>ewQnO9}MAoeKAOQh^|#<P9RAtM|Bs1Et?FP``uk{oEeg%587h-{lFzY1`ZNS)GEr^Yo~11KO0R@@vu$G$We(K`fVC_u>ZCz~)bg9^j>On<Ma&G*Eq6IAGwrdsjG+eR{34R=oY-i-$I;KJrykC5?qA^}BQnEWi8w_J02?qY@HmYjc_V=O9`P{@KL=j?j6TY@&|e{tP6RZ)fD|3RC1{nRVwWG;>Nmhq%8~p?4Q^I2Lp9Nqn?nHh=<-Tt&QmGAvnEKV;_SB^sAj?rjvxbEG0Tm76~c3P%`J$=W*Ci%*S@Y+gznSr3Zb?zMXsLZZUeciPO?s%{l79j9gOZ7D)l1<v#bQA1nh=B<OQ0D27$CEwM!Xg0U4qg{$m+Ct0txQzJRAb3@A2;vcVf=RxszRva<0e*wgNw9VA7FRKXpb`?uD6n_1JZpY=o)xFATYD5mrb^l*UcYy{w12N|%gDaCdqxzS`QEblV?UwmZiHLU-vzIjE*mm#gV719NRSTMl)_hXe<EGFjkYYa;BAu*S>gRzZP4*BZWEze%qnE7ejQR9i9^J=5`DFVb1JsWN)9mQc5N*ruq!f#o4SZSmB>2j0mga#C2%pU?iiTJ<GZi@m@F*2U6x(}7>~M{p-2aqa6$%y{YmC!?Jw$jr!k3&Z0LVPp^}@2?=R|gNa$14ssMEYk%}uBca)Jv?k~Mf&u3OtVLidlm2x?iW%n09uN`3rEGqKVgxDeEW-^K;Wz~Lht8>h}5od89(d3u$@QSG#xIy`DJ05`+ISbg;kBfjf6Rede`l;rIyVyMosnic56NzXK*=2AM>|<S(55=m6T4Z>#hPv5@-<0qr^-wDG>br}rQiY4LOi5w6p)h*yyUuUUM!FtU!VXnN5czZNzA_B9?|NHhiKb&)3=-B4ejC)#AfIS)>8!-;K8Vp4>1GUgn<^lTz|R~<fl}X1_OcS_z|rJDK{n{t21mOcqn)Y5@Q@)bKTGoh#YnfiV9DiIueEu)gV<!%i)K)WeY|Ue{LC0^gp~}Chuv8L=S`8VSi5(JBCQJBzYd~jJl`=#q|0m8hVn*)`#bL2*>`PuK%VMhS7?O*+wOVa=lx3n9&zBg+`7tNb{2JTIRH$1jgqGy<2PWDV`Jk!U+CD(W`$=)hBki0C)863_aq$M+#n-aUvl)fxPHU8Q7m~fiDyYBGPw_9J!?#<Msz%_r!qo?uibBL^b#g+KwNPk6{))&6+<2_ey|6d>{UbH^?@|Y*AJcDlpL&?S7{^p|NUUos#=)bWPQRzF$^bLqbiY=<T_D{8XKv}BnQLd(fX~=AA%{bK0>cPnsAhd0M~OAffP+?$@f&Im_<<+iqnUsm9LCem4@;rL7feDb#u5#?h;I7a+lSmSx?7E?ew~7e=S$yc*$g#KdjOCx1n?{Q#tj6p&A$xm;14|+tgTEgGO$2@<VNk_KrR|DjkObQEQ78zK?87bir}S)n=0zmyfWIbZWp@ZK|F^)ER#PjCF36N^I!4sWSgjM5znTfz+44)S><v4UVm3L{XuB<7!-0A!apbK0K!9#rP|j@NpZG0Aa_?P6S#F<56NzP~-2%T5J}d+jR!h#hwBBMy{b)XE)(!A@!-u<gv-Tm&^y8m%gZy#|$hm#y2Nrix-4k>3nm&nN~L0D@?m6*GJ8X>zezD>47H;{u2EGcu7E;ALD3}b+}D8Pr8el-_=Z5Db)KK$mjx;UnkD4PvNU;Xrr|4i&&MWi%B2h+nlDxK49^5Xyq6HKvI0HI}zG%!=IT_R38_d6hS-U%fl`k#oyJ(s=!Vd!I77w_LGWQfsr|Ra!-Ro9U#Iv*@wTHK{q<SBq#Cy>-9wJmWPD0u#es*DAG=4gdIn6fl1cMZ1WLC_gvDf7+jpx(qprpJD(ar6$|Q<T6>^Mfyre~6@F+TasX{REEM7tmhfV#5uExgM%FwJ`63MZPi4zfo70lK^=ohAa%@3^6x)L{gHo(R6RDvZ<fL4~LO`KLib7v~a(NHWz`ZI_EW#t4=X}k@<m!6^SC7`TR(YMcC{#^rapk^PgLiPnOJ;aPV9X7Fb$KB^f0N~K==fi=Wu<+g{lKbIa)s^*kB660yDC7mXRSV6%cZ3^4y`VzJ(6I*or=lSt`@=+U^4Zgl2%zWq-nmtNk8Z|f!<b~<h_yWGl!B(Ey8tr4uhOS>xmMz3UVu*J~p|zjy7nUQ1#*!JFFriWpXq|Tqd`!oxD>#wMlb8i91j2(X6sP>`XO0wfuY~sRhf@DBmI&2Ly58sp+t9my4_{t7};z`IhJe4=RQv?a1DtP1#p{Lf9c-@m#{`NZQ$|bf_YwBsfmMLT22N>XmYBsZa+Ywv;?39_PjDQ+Gl*v@hgEXbUo4pe7HAEERJ_kcp8E!pLB9CdM#m@et+BMS26lxJTE_z;gjW4%#46nq&=C<xFa_@2eUI0@$K0OiRdj_D0MuASpY{##ot0!^%rn9PB2kpJI2%^}w~Kj-84)e#Ko9GLG{{@ugNpN>&ZVOmNH<e3TmSF+pM0vn@nnY6kIR(ZyVy#bUC(Eea9QW}u3L`HwZmTxieK++?_0kC4ugAe3;b09q{b9|=@*;QxiJjbc65e%AZlEm*Lq*=W6Fz;tAC4D8?_Yf&obkBYoJ4r@>(Ly{v4hdj0^wo8W#m6SL{$=l!6>tFl}n9L+j5Ur!3U=p20)hwbWm4t<dNll*oNiZQ5H0dIs1A||T9xjf_>%OLFD~PncS4n@wSB1KdU)`f(b5iEO;$PUyva&7Fqx{>%ww40>YNMzFhWyAAr+6sTfvg&x1Y{bq_6vJ!JJZC-hC)5auJoaiDe>>Y1X+5V9Ci|_441wU2G7=<vGc;H7(q&ZD0GHM88EG`rG?&Tj$T7fvfyL>c*xiKn-;7~q@bN9l9QQEp9!e(6`l$91lDn5RKPG?=Ccn5Z{f~bc#!d?P=?{M*d>|tj+gBja8BP=<s2^SDU**SL%4607~s}s#$Z)!P^8AHT9&rEoHb<YAT@zbK3+2vQb+*oJF6J`T#T%{4ZMFM&@?<3UmCh0DJnAw_L195Gfl=)n9@EU)gyvcJ~)+z3{5I0HKWrwwZv1vfAZXVFv=j(8wx$7hOSgp>CX4${Zg}`TN>oso<?UvlZ)cCp<C^?X|Cca)2@mCqsH!rZp))wz-xe2aZC=M>v6_zPNAxlX*A1}PFWQ45J-Cc|FSgjq3@a)ZT7H;JI#$ex<dNiX01`)03$h2`HtY4=m(!8$?E_>X_$vIvSyHi>{wbwqeKU<6hNGrS67fC4)kqPpKL+hJgLN&3<ADj@+MMhP*jJB!8l%gMk^NgAu6dT#tud2m)Jj8&+zU@N=K>d94Q3krB=YghL=oBGuI}?T^5g7nkv_1(-EKy7uRM<-Wb01OooLPhQ|kN=v?cKA1)VQWW<-q3Woj}W(>vk$gw2#PTa)71O~hI%-4;k$f7!W36ow9EAh2;=`&zS@S@)a8bh6}UpWj@gFf+T3JvF!f#Hs%@PD63ps`zg%HIV5DUgF<X+c6z?IGlFAYKKJ^N6kAeMS-=8CF++2?uYlOdmt!+l;lE+2LM~IczS*185+umn!F8#x?s!L_ON1WJu%zyndMaD`$(BpGhA)j=F19Ud84v0@D^8nlcIM$89Wyf%k9HFI+-tOn{4#1FW^YYKwhj4^4qtGhwpYX0)eUXnQeuh)_dlrVlklsR>*G<!LA+y@G9StT$=4UI%avjbrv(*;?#Q)%zvH#au^y%vS~1AUpBb`JhWSI#|*5sYWc~Gz%cv2ey5H@k-4S#Q}^6vQUL5!^|2Axi8PO(e7Iik=LF!1W%^UwQ3rELWtaJa+3>}r{1=5*7blu;+#RCACqY~VeT1Ko)&z?D~8@DGB#*&dfnQ!s3Unm=-Hd>GA7!^nbgp*qnE%{rrCA+fxuB^#_HH1*sno?>vjqkyKpxF4ca(A>x-q$dTnI?@dp}=fVP-s>dgscW!h{ONtQYEB>D(YksfB=rA*I${3z6<RH{M%&y*mPh{7dU++yf0_Y7Bf&^qG9N*>5Ew+KqZr5l7lFWMl(gJ+Ob=E3GFu*Oa9R>N7Ku}8lA><6R})~ZF_bg9m$?>K@EJ+uKD<}>lCpUe_f8PQDpXnq7oI{tE>Um|+F50KuMA=hQdnvq?!kEdjZx4>+G2gTFD;;gXjYGrbiTu_K%MV1(6RM}CA&j@#0BA;-UkGaBfBq<k5ew8@X!L6rW9N~RD)Feh*vs}_`oRcRAD~fs?i?>%DsP6OdrL7pbjOy${nwHo1c^_n-ItNVZomRZihrE$CwhXPu;%=4i4M&{~D2IUbBMA1AgEf}X=33|`2X-74hO6;Mr;xD4as$Y6(sm8B^dv8`L>18=vPcQpDi36+X%FmZY3k9kG={j8ZN%h&i8Q!;^%m=imKR?NQ-CKN3k`?aIu?N)ma;WKXjWc@F_9v4EeEBo7gr6NwR}<aGu9IwDWcW3w05ov4dZWvp|kb&Ok^Km-=;9*R~ztGj9!}M+`#Y$xBVCU#(cpTUF#eMb=>0Xn8%=Y5&!9<(5KaI{bx(#@F<c}dyIbS_bOIvq_7R(sO1bCwa)G;p{a!PrU4!&fP~76CO%c@P651!wJ}TNl1Qs5@Y+Q1)VgLGh}22uF#S_cja=8-4_dc|W%b*Xw>lqe$)ksDGb)03DF9B<5(YUh(F!R^o60B)cfqQ}y8Gciuygn)EDS3&o}w03VU(gY?pS4`$-D>+L~1)XH8@XH8MeTf(G9a@x-CYi5OCu-RSB9B_n`OTPX6KpYp#V`?w-|=CdR$W75R1_!2M=)bYR$!k52-{p4YHvUuY&vL#s>QPMc0lvQYIgak3dND?!vC`7C;Eqr`-p8Hq#3O%a+kaE1kI94#QU<)SI&w^5H5MQLV`m|^?028J}OJedL+FLsOKJUGt#srn2hSs6bTqD^dfxMGb^?x*Dfwd-Vh7UKn1>^`Uf_fpA*^~hjdG1+;O1kUj?HY~mA*N}2u*r+wKj!Aj?fn-`UYFLvP{PSOKm3gm@g@hC0VOR=%<iOJs9>TZZanDgyTU~!`JLa=wybYS9pwOb@QOBUycv&0Tj(tOlJ_;xrFI!7-7pwlLOPH$4xV-93Sn&3U1`Q|Bpi#;}<#<&>SJ|pcFd(0?>s<aP>#xPnCPlgIT8*)5;at~`5RUr^=7U%b!TsM2&4MYOTgIO_JL=JVoa1inMjyNK5h-3;lE?~Ly_6ry@<&H0s)i+_=;bjiSMdw=mr`{=qn4F|2^fRK>|q2R6=xso(pc{ZEULaZL}jP;q4LSe;n;*Vfe*!wBxXN7no~oopSBEU#h%)yy4l>-RC^g}c4k~1*`1|d#mXhomBV^$f(u){YJJxxJ0wKF?pF@qO6r8b8XynG>yAjF?^B*N<0$iZIi*k}U>J7m7K&Gdo@&}P$m0uAYSc^1p2Fxp90UoCC~dXIixvDw{!~A;N@O#svp1&?Ic??@&??44rV5M~-;K0D8>rDV7Msdc<=9KgR^2k=?%>ZV3k@h{Tyj9M{=n_S`MzVn+B{jnw&9ZUjHH>P{(`O9G<0{t2RV&J)W?{9R?I^yMt7abaA`c%wa68*Cvc=~zK>rFcLi9sh;wqxxItt&t3cGsW~wc1IH|0>gK(FRLY;<l;>w9yID}P(xD;dVDk4%Zrf+xt+E+;RCIU|&I8&g)hOA5zCIuT|jfPy&I83&*{cD(=RQgd2hGvnoN*RyC{NZ|b_4tyTmXQ4zhb5OWPACk}&`;=UX;Lki%IZU2s^Sl@h^(Atoct!v+py(DQW5jX&zC+r|EgHl_v^0n883NFN{9iG`-qmw^MLL4Rbb@Zb5FNw{YsCBvQa^VOBG3tqsosbnnXebQ`1FQ^3gg?bbf<-#weO$*G8E%65}_+Q#R&xi)+LbA0VEo7CCkS>DW6qJy!skc4P1whN%rC_!ro}*;lhq73y*JWyE;pFEhQrz}y!1v~e~X<)9~ySU@-EGu*V7S|($k?CKswE;&zII)V9fa1pmPsKVo(oJ|k|-R8VK_n~B+GQrfjiPIWS0(u;nz;%j~O$_k4JfaRedKnqSTtGhV?OF)8u})~>YT#zbu~OPwvjBqZne}dbNi!JUlU~K#B_j`R9xosD(=>%vTthFxc-U5%eyje|n?2E&;&dJ;!ZbFfrdjTQO+vStqmbmTmO>Gdemo{Oo#^eB#}jk1=n{sU=BL1r^GCsuldWuCsCM~SB*SDZJ@knxoi71wT_2b23^i_A^D!YWbYy=}>3r3x$VUCHaoX||sWC_POHAcJmMe|(B|pA8!$Zf{n0b_K^2WK-{E|R*r-8`8`&4+PC;Pa2pA6kpz7sRdm`te9-iqCx*`P22|Cu8KI`{u#wg|JQF-oEawx;?h^1`;08ltM=cAO{Qz7Su}7ZJ^~Zo+$LPS_Ccmc}q5c?wRej*Ro-7joFlJcg8c6)Uy^$vCeL%k=@mAr7r*H_~3d!e!jZ@!sr;OB4tu*rxcF5SWP~{VkWo0io(Iyr3*&abT2P>JDY}5o|yq8c*SKFwow%1{gA%98jfnlhA}17g;9{>YJ4TLl88`jVU&+dY1~RI7p+qw~l%ePyj;6uyft?h?ch`>f#Bb$Zq#RY5qAsW|8QAO^T|I9|Bqe8mThq&>j{^Ph0W0L!?eMYPJhsvUt$}4i%DcOlAs9w|9;#RVDK~_)#HrFvG*oDU{(HA*~pjsz{jiufprshlENoxJF2*|0qakRcN@-C7&~xQ2YtcsgN9Nn%d+7LrH{a?d^W^N@<6w8inizS+3}yL+fBqg6XKpsWPe;K{LRBM}NS9U!Y%X={|w67a<)O`6SL+44SCi8fDD^r_kvu2qrL#<Pxu2Kn9Ideh`=O<;IfWQ6V6w5=m~`3E5UA2#ZBG!O*(aM0D1q`jn8f5~Q2Zz!X&NDR`R|u2iHUyszp}7xHqRQl5e#M9csxOZ@_~$b>eDW|JF=Q#5?qTphtAdX-+)MPr0)>%|r9(!qk0WEHR4&E*@}jD?zAeNE%|k5pN!W9Rjtr{qOg61C4~Ox@2B<cdgCF^L5=rKl{EVk_W$O$l{J`fOA2)JU9#x;kLAvn{J{RlG-Uj#^EMABI=i(teeJWQu3}LNr=Fe}#Y@Q#|*RI#J18*cQR65G<C)DWjwHjhofy)UCCCH7{qdH)gZH*z~5$#m~aTRj#>`2Eyh^wBMXAvf>X7*z8Si1H$YjObN$L7Zsty!!fFNF_j{+_(hhW7Cu<xG1uW#Gs6_d_0rD4V$7ayJ?1h#4>7aUvRbjT>7t%=P6;ycn~ELu9IR}4IxtqQ&TPBeR<$3KX=GkfL;dDHfyJfMHsn+o?VEUdK^Qs}N_#dRHdG1=b4I@0J1yCZAik*(=*tL_rBr;pGEx&Ah}?nhlJP`2Z0A%iQd(82$ZG03_xSQg1iYk!dD(brvei^mXS3p25w4U~OB@H1$V>(MQ`g9X&z$Eda%0tE-1_vXX=S*Z(m9lOV%LR5=Vr1KYFyDxx5Fi++D|V^oH~X7<I<1_<>oA))CEsCvS531ct5SjvrbGvE5Ivov=2>HJ(`HxO3~5D5(dOoT$XZ`*99_Ws6CdGtd<hs5mI!Ujb>4&g%t!N3JT<~JgE?IDx?B|Vv4A_BVq$hyep5q65lX|u3&w`)BwCQPFM{Z*_{i9r6^HTAu6aYoggr$CA6FX{chj48wM6JHq{+Y{ovPgL(pYTJlQ}Ihc3)9;g)JcuFE#{V<M-YZ8$=2mfNJ_&a_IRjZRDn6>)1L1GY8)8D86Zzs$|4exE_^$tmyzFSu`t^8NWYUO%``Smr@=Su>=*rXfV!tW+x2LBvTY*G+|5;y)VWZtDG#Jg4e!QgT5_knlJ(U9`;e-G6wvEr+MpU{1ru4y5kP3xR!JO~G3nex+(Ir=hcNPf|{47K~ynku;G9<IQ;|G<wcuNAiq2#e|xMA*bpFqG|YQyG3VV_f9a>(a#kony}%urpd+(2Xh*x=XgDwWkwH#s#TeW*$pLF!vIIBBvT+O4WgZk=!>L#-4l2a5#A(;viY+H?Uk!*OW6|E49wGY;;DDs*imDWa)ZFk3BkpUFp~``JWTt5HIhPvB4GDhIIw_&RfWImW`hr2(lO26uci|RlnU!vO;4i>NlFJouOG4JA`p~O#cOYd7FNRLUXJA+ZT33jWiX)Km%!4uQc?jBbI<I|luvAX0$5at|FNc;#}`!Kfyhj|6xSq<FdQ>jT&ZfJppW@?6!nO+hG88uu&njWL7-2pK(Efqn@vgOJtkWvbXwVV`QlnZZSOS6W&#i-9a4lV7i-FwG)_}@LZj;hPtF-3fHC$#pY0HEhf;)es`KE`)YK?|wP1-5A?>NybU6>tnMSt}5$z~L8zp3aKm4_sB9WCk+QU32w_B05ZNkB=;}0n9i*?<=*`C{ad$pFXGTr%bl3>_N16KG}rieH{#t$mONx3iGw6-u0X?3Ap$*MX99E;W1ig}v0HqH_cPJQk8WBiWfSCV;tOmV(Ep{FXT$U+xova&P^ZR(>ncMT=iRo+kNG9}QUxUHdky5`;%#7B}$`L32+#E)smJ;IG(a|Ty{TT!QIleAT`=0cP+&1sy+XXtBNs^E<CmlV|t(eio9<s-PHK5!j^s7pLikZu^58olb2zrf(;+vT9~L>7_3JfLJA+V=S9T3pA>FAI0zJTjxVJfwx&o3@t1M-M~f?P{z-I-UYzR5`+g-Uq*_=reI2*F&O+c}{_hZBE3`d{o8W+Ye5K_#Wdgij~(Vje5!s!?WJ9LX|H*LJCz<kC^)JwFlL3dJ5@2=k(xlftU&I9`Q?aHH7>4hsFaWN;H@bA}dQr9SftOk3#!PV$~c0L|r+aDrol5XJaZv{@SF>Y|;C+B2R;m^-hz-2+0GL=rI>om1uTH!bYhG66)6UQOvDUFfdRvgP8ydLs<e|JppoFysvVR&4*1|BgnIVN||V(Sg4BsfzR&fsF6QA*XT1g`@Wi~^jv_WA4-f7nJ^Q^LUOIhycTd1ufA@-bjO%{bYA<6>RCljWu<}$jZhSWrX;1`Xx36xWK`0_VYyQwQ;1YWJUUpQd6Xu@!Fj~P9}=2iz<gN00TH%<v12bAQW4^KavdF0Yto%ytvCQdEL-%H@Re_qoqY3SA!hDuMbb}=(jE12Lx|Rchj(}}t0Fr99+_xGDH{Gg77A?P=LGjjIvQG++|5a-G_ajFFO=puxve=4E}qplT=~Fhp;T6rCpO$*>=w$3fN-E%QR5lb)vA&vL8L8I3yKEg+%9c*tq}I`Fg;!)6`k0%4Xb<!DqpuQVaIW*4ctzV1p{Lbla!(qHv8th(0bWTwp_3Yd`z{1p`5HFtmf@SchfecBBnO+mNz@6Aa1H!+Mi~$3cW{auoOy@47E6+4aCZl2l8ffQ|9J{r)>YHiUY|mA%@Y*>b{nHc9x8=I3I(BV67gcV8MVBVfD~)J=#sRP?YDz_HNBopfdFOVo_O%s}FnITwj>dkQ&X2701bbS{y5=fsa+Pn`$WGwR&xp`opj+EROXUk98Sl$17&%3kP%PxAkWb)w$H1e2o)Z5Y{x>a0Xba7RbxP$QBQBzVv?CALCaL&R~`;`8@XHTqse}*|Azz(j$)|eDwzeFn#5E%$Ly@K+P8W34&wvRM-W-0efq{81xet!)pXMDI6F}BZd$1mpT9Z`Io!fYlivQ{nr%MslscQej7KACHUrCNKCS~wMGVN?8p-Yr)k-EsH@+ROyC7|h{S|ECF7X&kds!_A66tWk~avpJ=$7Z@4aJPc(ca4FG*n{<$38Y{zh^=$yXm|Gbdr&B%fiI<J@uCgcx$Xn~YT}m_pL4Nf~n1<*3r<5ZxPz(x*^P(VykeszOK4B8ctJ^hnCkx|W*O)fci-)gp{8QYEk#N@Qkr^Uh+{Pef-p8!W*@JwuwxI>DiyyE*Z&9bZ_3Moo2i3AVdiN>UlqlDrH#YH?=~G##qm3@_E{&vI2^2c1BTO5f$r-aIuG5QF%p2(OM2T^;*;H`%*%QE$5ChB1n6pbnAj4zib3&;7+$5i~S3H1Nw%e4SagO|y`-Y;l|we^k7K8AlDSlw>qUFWPNyrP@WD{FOHjb;oG*3I4JLc|(|5KeX0;*e!)92x$P5k_{;3_pX~i9aA2kQexfL9@Fp?{^s0Iu3sgA7Yk*a+_LL7+|h#@ds}aVNi|dcRDE`1!MxtV8y_}*J0`NY6QKYHiO+!hAL`E5eq_J8vLK1r$`>`JgIC?h=0cRx(kxWaS$jK;Fv2J_AzP#hDNx7Xjg$sFHj+Vh*)%2l>`FkvCleAZr86`1u94?@7)v{s{WloGBvQO37B~!cs{?uvna(G6Jq%bWw5+l5XfP>6mSCrgkZX=P7n+hRtM0a*<Arbz`s3Tn+@vAs19pB)E{J?#2E)GqavGJ?rg@iBW^qQMgEb1iO(v1kU@69Q=WGUp_*<c*D>+KR$}U7vT+L{!Zr%EfOR>tvns%FMYWFNL-^AniClxE{;=SdXs!*IZ?0Kw->vJJb$%q-~6oUw&c&qOTJG~!RByTGzU`el(+Sy_|#*_|N7xR6jzCfjV0hKG2uJBH^lBl*|YCIjx$Q9=RUnN{JqP`xqMA|AcIfd9If~6~V9)->ME<))q7vr*_t#N5+HmfVuHQ<F9)pn8cRG~@_En@Gt^>(qV2e!a5!hV1CuYrF;`~m|!39}`paA7SwagV>f{^1XI=q@RAh4zxJ2A-#jt9<6yOp_a$|9-&7Xekqp>k{UvJK4IGg_*pll>KE;eK1cF$~UqMup+8px}$pM%FSl|WC>$^o`xo3ew`^3I1G<VNl;HX=yRc@$+$|&E8x_ZM%3omLEbKt&M-w=Y*e+mYohh-IlOwnL;R;S^#)GL%w=yxgDF=}ieegs$OHzwxXLze8lRPMuzFu4IGH>wx05c*7XmFblJH=v`et)M*1K{)3m4jbZk{&3g8<2XaHbQFWm;RymTs~mm}ziS6ab#kn^P*HtpC7!f354}g!)y*#*<LD*E#mBy>0AKHnLBkH}uMN!6;>y!A@uKNs9P7YbvD?6wS`_&`>n%wo?#4l@N*BC^lUWI~PKm@X$%=JDM-!g$0m(CA9PBd2$66=!?pKsviNf11yOp=h+wkp;;Fy7sD`J(sf}U;vx#+K&F<*7p|KCmY4WdrF>;I&hLNz{AaIpfZKs-IEj|41Xa<xmJDE&!gn+WM9M|Aflqb4VNF~d_gOAVH!2caaa*}iZx~@=xelxMJGX5$Q|X~Q=C1a)-BYG+ug~RjIo70W6lA2deQg^QoJ;j-MP~hVewAT7{^P@1R8oM$;Xo~e-NrVd?l!w!QkAzC?fXzqsRxq}(X;Lh>uVY9H9I`VN@3v5k}Nd<&+G6^(igfL7XuD(>S6&{Q=v^%3oFWPE~?)o6AFQW*YAJ*;m7a)`rYUKC3|~~+hK-EdSIODiFZ_)d>LflY2+_8G!%4z?%2qWy!peBR=d{Uqc@VUOSPv6Z7HSJlw;J1E)w;BiwtSKWJ-N_u8KZm2^Wqw9C$F0UHV~O6V!ZlaK)hjwu748rbG1-N+|>%C6ppSNUDNpD%6KIG{72`>lUp|rbH?6_gVaJ-}GLk;3K8g!XG6L>*)7M(XN>hQ-S9#$3<Nw9bOQ8X~h$5>Ws>~4L}rnk6+#JeL|`kg<!|2(wdC?gIVI&FyFh#VQp!9g=ZxD@^F$E1?SV#T5bL<E>{BdB1VP;oonBs#@Z)mwk0eyr}@I`f&v}vbF(Sr6+w{UQBYOlst)cgUUb8R5^9M;802PykKgT1D^H|um~G#3U7|}8Vg&p5gU1<p7iLL}!K!#^Sc!ya5w9dUR^l6P=J;Z8G{F*(UK%t>1B>PS6)3nq2T-?-exVAab{;&K7v71t#@|ru<4T7yflA>ucm(p+av8Smh!M6alRtj%S$)HxE0$aR!|j)Ge{I&`qjAc`e~PNk4^nWkI`>Csu^R!%mbA@nYj3{zP>ytUKs1lcw$FF<tJFDj<jqo=kHbZcp54a0*?Yu%4%asUvj`X`OQ}4_vSOYu;U-Cnn-~nO%P7&<eu1F(fM+%wV4uN>g4S4Refc;i21Ype3>98410ff5NH})_3~}_cZf;2>^LWBv0z;cxrI2)l7n)hzS0H|E>Zajw*5iR$vRouR-gZH`g9iTe_U4A`zcfTQ6jg}!h*`&5WVmY+c=H_Si4CuMl*ePUGqJDR(9m}rM9jNqsePB|I;rmBN=mSN0y~a3JH7p2tv)z=6*nLF{Y#;pw|}Wm{lxJMg1RX)`ue@puIhr0$-8^1nNyE%=`vw5O^edbJ9Si0D44VCGfbd|c<Ft#^ULQyefs4y4G6aNK~nnl$In0E*wM-PS3$_W$e9S7rk+tP5nJUlIBmsLQcGH{)VVc<Mi4FZcxs_hG4Q{ya=pr_`i1(6*NR+43hNja!4}BEb0W^as)d(gj>URl95%nq0HXRgvEB>G;a)$&>t}l}j8c6>2&cF9v8B`hN4bSk`>?jR60WZwe_1^{9{?W|xN2Xf^5tWOub<Er_3)XV6btitlbUf|QNE5UxV;_=R7_EfVb-rnR2PdAouKMG4wCjkEVAx1R#vNT$IyKM-@NMStLAacH^~fT(<0nuULs)ak#TrsMj%${it_0?5#H9J*BUE;0b#-YSM2@APd|Ns1L8mZ^uwP%eY-XP`1<<i8(FU_3Zv`AW_=F;R1i|R>U}PXoNs69Iznvq!Pb+eEXSwCkbtrAk2Qji?bY|m3{02PIYt1NqUr{$=<9BTXyIje;!?q`1llhK`^&GoLJJJ!@!l^#4Ot<EKI(DY#F}s0A7?bog6VFWu^u$BSGGV_YmuS~BOEHUNyS`BFszVeDYOM%R%*<vOY#mzgn?MU#xA_A)T=~ODz_hMgNS<0n9Ih>m%CY#ho~BPu*7xOzr4Mc1MS?KfOId!TMzCAKt+qLs96D%(xAY%u>};J2OdS;`Q{H$Y2aZqY318JZ3Njt^v{TP5*ful)I?V>Q=2>N3kbe_QgIz1!VDr}tM|CX>7?H=P``uk{oEd^%587h-{lFzY1`Y?^vgUi@U%X9H*c=Ow(AF)5zYM|WQC}wrbWZx)=!8Y;G%+)s3N;k*mVhd_}#s$n8iN5)-xj2H2W71ZMs$DtE5^{u7mF_u>9`x+xz{qjH(1#RNLkT7i;&TXfgO_7Y8^(=Vh{KExN#pByn$N<m(Dk<YZB82!feYlCe_EpyUeUjoXL5_#`zLYsA!wTYe#4J{guQs~<9R^TLs6ov~M;JVz>mQ@Q!Gpm2mi1+1-ez4&bB$mXTAwe_IL?OwZQAtWkXeW##&Epk=i(s5df0z@Vv#^k?~4dA7lw+?<6^WsqQU5$$mbK5%FmC2+Ntc;J#h|djzR~3f<j=w3X;=AhWobS}mHGeH{UGJS;RZma}31ld3q;6e5yper;fo|<l6qzbXGG4#8C_zhoFPo_T;_ewyY%Z$`r9XDjvThS?<-N+OY{<A7ZO+OB>5xq+e3jBmq)Rtn9#xQ@>)!LazjU=h$HQ0@5<T)9W)-qkzYd9o#35n?h`w6FIThQnx^C*3A!nqr782MM8N*Fo#GX1_o%8_X465q8ZFR@M)ZN~F?Z;%{^_0d1+F(5DW)|%{RV6B0qg3Mn@Ur$7b-mM=L`63AKcY~{&BON>^*SV4Y1g&ebpnxU%{c1#I*r_4dYkIbtf<0zf}Ja6Mk>qhFMeJ-!VVg`+PAhIf@Y#LLs&H%Z{A^5k%Bdy{Gu0LZd3y|DBo?zBhVsM-z`5b0-`psE`iE_s^KnvlQY^X5|D{Rv=>R@f{S1u>uNXbWi^C}Yc6Z3n|=6Akxx=wq(ZM=mH{DzP|yMRB4y<C`>wN##h8#e)r1@(f9{kz>Tt}Ux0P;aI=00iqi&>qQMBTz$yr=FD>1tdVzgCz8Ef693J4?cGsjV&)OVA;tOPo6bQg3j%0T*H@1vb**XtoeT0WD)E#(c$80mHwEV=yZm8z{<=S=OzmjMc~k9SRwpBaOVu#y4tusbW@yeYC3c%JJN3K>jY@LCU|XFT6AN2JT^dWI@Cw6t~~dDoT)6#baV6<Q&{wtL?9dH)iCM;v%Ax32P+okbm74ggcoqU7ngZ^=G{v9XJlF9vI7v%)hYLmNNh6DpL1dlHUrZjkb;FFE>Ktika<iX~4b@hr(iCih{iXN@V<9Ezv)R7R-qwfn7&Uc!U|h${|yMI<_eT!%bd{9q5PFlvHC>-%VyuOB+Ut?_Goo6+hO$^Y*Mn^x7r<R<GA9*SW&*(Xp*k|fuOTGZG`O(r=Q7LV3%ef|(kc_j~{HEEiPzK;gia}<FTO=-#ZRHm3kQ5TBShozOTj8>I~@+Lu@4c0E2MGA&sB9ptUF3oy6Mrx<mP5W!P630s>!~CpR7NvOmv2&TqsUHj-ypXuukG<V;!&1*Pa-)+UYE!g#^vO}_I4qJL_B_FHOmzNm$<<Vw$8hKiKEgiIsR3iPsd@@gXZ!^)*11(W5DiZ2i_y$~6jADeb0C`~Fm)&<MuTH38BtWI-?$oAsfSq&nh%d@XEFW?CVbq6BtY14vlD?}fK1s;hGzBhRhz}<cAdfGtCOQ|<RXK0b`y>kQlBhI`9mh87gh58WayNlF}^t|Tf89TN^el_u4Y=<WUnx7-IE;D+*eEwJX!FU=nue40@|Y(N0Y3>ZMu2VUCjKhX2MFL-q%1z7ohw)adv$QUtL2RrEOotsx)0p`Uv0VG&QzNil;*>#{dA5;$uDb(e49<fp-RBRB%!R?T9ZA+b0x%S05`P;an0Nc}Z$Nsi+kgnUg2?G$_;oBAk<b_^TOoqvK0*67RoWPsDBur`pc;lTA>h9iIq0j^qN9tdrU1BZ@|wq|GU~IH{$_W<7U4HGnD>)F-v}K$QZM%bY6w&_d(@+ICnd#3?M{#Z)6W^;wLpc^>jb81$dYMvykAC3)-D-p1wFf(9wJ2WJMQScfK3Lp8`rxrTnja0sqAyoYDtUX>^o;StVrzUE?b#j=5`M{8QEyiQycs;0HLa$l@9G`Qj=Gdv<N=7ztzybzzi$#OV!{IA)v(!S7sVAUzPLic=6yujpK6(HL8Q=hKo($e6CRu|MBNwD8e#bjz%7un#nK2*{wYlbw<_c!SW-6qi6s*}8pY<=cXa;ZhQPR~KML1{iwqE<m}Wwx)2p6h6Xwh2`)Ua`X}B2p$tW5i{0>)OdX#Z#L!2b8$;)E><$+r!RO!&A%8SCU$=ERFIlf^k3)2cDV^`%<~c%CfqaC6aH6rrDrkNYak%9om$A)hC1<0v69DoQ|ZOtxAU~Qc8m31T1969jRU^*Om%(5MoQoW8!gMygqCvghTs6UW7L6;st8*kjPRoR|J_D*&vJzCTC&{gBA}_-dv<N5R7|t%?vyj0OW|f96BahLsdDGn(X_k#(@B~XbaO4@}0dAvkOQnl!#zu9t|rmU2(9Rq<)GVyM?4ZRd(Yxb}Hid6?aL<IL;r%ms%AmSvB)A!7*3xQEI@)1ch18wh)D>8N`o87jtzMi^=x3C`3e?fhrE>Kh_v?p*>S`li_YXLOMf&P{OGKXtB(HBv8$P{}-}0iuGLkS?_nZV8No+ob{3c(~-$Bu!FMQSq=SBk(b9|4T@w)a%AC<$2P@w>2RTv5{D>x`@4Gmi+=%=nZyaAbu<)AqO+))MbxB{u<$Uc$&)_`CZvKUT?BMs@QcyI#W8u^Bou80k+%0L>5urTQ1|hxdsJ*r${bky3p+_xwpHERV1u@n0{d#Cr~`)l$P=e{DAa+h8l41W8nN~Zduuz>#K?w1J;<)~p^+)^@4*CFdYl|~5~>WkU%5OxUd<UhFN}&2r1XbEXNZ&m)9PAU=#AzWHK?)|e9RvY`C5O|f^~@$w9`a#GSlfZ0X4qDGr^v~I&O>#7>3Jy_QBvi&RGi&GTs!*FkBY9B$M9pvONRN>D#KD!(}~X^08zH_l*(*+}g|-tcnea)L2!^(sq}#hHM?ACeX>pYlcD!34ncP6=R=^k#)C$_fG_xhUel-LpLNvWhTKsa(ii}$yf?g+UKKsM6k*Sr_zw2N#&$wbQ-6YcnbJWo?8z_8AN(Rp@-Dam5M6e`JTLAYBqFBgM8c5=uBvGQJgk(tKBxuRXk<dHSvE0L)-G87H|?^5gb#$=klAeS5t^6W%|l8VN(`#Jj9J&yT2^!d+56+0-HT7;yrVlX5~NknD5Z{HfxRY1{leK%6A0UL_hc(NnQs4O2a&yku`%9WXIA>8YMb-r2yj0yt;xEaiDM8{$va4=1C>KWDxKLlUI{cgQ7Z2494-|Gg`5@4^c@)F?J|Azr_B*dPa{>Rys=E??@paFSP;|HoRn7nz=S9?y`8y(p0%7n~nfwxVSb;^2YG-XEH3bFg!kBL+4s={F1o<BO|^<RxtF>Fk>jLM~)?_cj6`vCNS8wXTEMUMHbc3OPKU>Sc$K#OP>Ktf*1WZ&=~4${mNmO8uW=zQ)oD+3=DT9h5!3R0*&3`Q~oXhNP!#-OA8W$Y7ZfY1Mw<&oJVZ^?lY43$gsNlOE{W)W%?K*-)5}U%ntW@%wcme9zX+Oy;M2(GOpP-BBRkJB|{<);Pu1QUpZU6{7m}banxO-@+vlW5vjJ|(3D9~KW<|w47`7ne&G^IV**@^9AK^GRa@*MduR&GnhBHDHlsb=LfebsMT8ncGkvHbN=@JjC{IHn=@o2qW4%eU^*VraXdJWO%GP3cs@^XlQ06-7W4<c52HA<f&Ietx(ZPzYPc>o@r&$2WKCtZrj8|%wC=OsmkcBEd8D`c{$bEUHjdtIHh`jc+A$T%%u2s|U6Jq9Glbc+)JoUDfv#tjOBj*eP{g_O{33Jb=^0eS9UNQ7Ok+DIG)9co*MIFflLeJi0mod>U&ZLHh9lZpuGR>~j4+M@XGgikA!F~-AT(?uW*oC_ZXwb&_Szjz|)@vjCk3Z001hmC8Q*TZnE7NAPNV3eKC(%cMiu5q^E@gW5<42(;rBW3Fc%}rQL=-N;;ub@1xo5b-gVqr*R`NiWxkXSKF5MvfdC>+L9z27jG7mOafi-S&w;Ij@jXm<^XFni?uvRVVrb~53ea8`W=%EeJFrSH6{bZJ?%7|v#NAn{%((#x3{1VaYeSq}747n~t){N|;eLN*Qyai?hJSd(H7H7qxYTSK)?5PxDSdk^h8C7<a;xoeCmdGcZ<zud}97)Q>l3yhbb#Uvc7e{y>4>gI=)-0EF8|UN+!iu6E$Kvf(2deu#d}%AjHlsSbkhkUaeclJzr_KSBdZ!gH^dWELku5{(vAA31d&5y@1Ii&F{Ro1+7?~7)I!2p)q1ztVkyRML#vh%+#um#lAPY<zIM8C0yzEj4nk96rJd~m4J+QN-xkt;=7~@j95z_-E+TilpTdX%)-h3%g0UmLzG#sYuSO|95`__P=S&0=!MT+3H9G13TTsdsk^F<ZVSZ{PBiB{Xv+PN|`jL{8-&eq#Ak$r%Do5YM?Zor>0dPkOX1H&KO{$K1H^A%%st#csMK?YdIJP5U`_)i}NKdpA}KU*7zhmn-qV>DF1m$6zSiEV&KEobnkb#_+?O(mQ+jqo@FB$Qq>0jffH3IIN=k69v_M0!nu*CxWJ)-}^Xq|P#j`JZ}f<hs^=(7H7&tKX-*)%jpc9zATEQ6t1_0dS6%P{?_WR>(=(R7zR63s!B`-4FMXokKujQCA`I6!owQgAyfj$4VPb>P2WEQrx+z!+E02um#7AZkR38ZZU#|fE&lTO3;+J2fYt>@)sXibFJKR_pFXIGwzkH$hZ4I?l+^Q0|SSAfD%adyoOEtLNi$!dR_W<+H_*PO4T59vKcQcfz%-TEP8FD%!Hd7i9^RtF`6}Uh81fZF(9<%qATUMQI8kJX=VtRVf(ZQhIFhvnFARwc8}sbI?fxa`V=Ku8b21QO>B3#WQ~ySr}YB0>tuQs;{})OKF9#~Qp$!k$zW|U*?E%;&haufEWPR1ka}I%sWq~WNqPE#W?D09ShE=X^IvY2d9RLzh7%%USQ35Yz|$HYLb%^?&ry_HU4Lym=CfqH4Vsgn(4yl}$Dr4ESsVI}eM5>q3Md*cTT68pEB~l#n5xpayzEU_@%D%Y4JXi`QR+eEh*d&Z*(ysgAfK`8TmmR-u*J_NMY-%^jj?MXUDuBgj{6DbgJ=!G{of7E5-Ofs#-BJl>d}Op<8JImAG`7qDPCKW$O>A`lppHyM@K5Eh9#ru<uNQ*@eB2rQiVXH)|G+@7=y*^VFVr*XCLd*Snvoes=hcxX{Yv~^2y2J*n~BK55<lorawKJQ$w$xwhU%PpW3Io+2qw!e;I0aW?UWFouz2S>Lt;Y!<uY@3tPQveb=TtBxJ$vR}SAw>V&`|AP>gtj!2>JQ=T;=Df4(aB~c_`7<TIxl2?SEYT7l(;|o@5)J)5s!stF61PP5eZMDdY75qp3R6n(9WHYU^H>VLf?dBEGD#k*m3XB)ujkH1=$k8-bo61z>*h|V*-819v;Lj=x4Jc+@b3l>&!0p2czhl4JL|MSL;hOS{rJ3XYg00y!ba%lAIgLfs$C!Rr%tI?jR{#@xzF{0Ljpw}9y&@I{4!O+$^6TU7AeXpeZX6nPm$RZot^B6i_J)&U%R4N0`6wJ}IH$LqD33$vWr$Qk=fb2W^<w&VGq8PyRJ$VZD1tKuif+itG@(?mH`Zt<7>&bZtKGkb`AQ`z#eiuRORFUEILsd|aaWHoxoHU{ka1XYIpl=s01XC()Rv~%f~l-N2&Rev0k6o)V#euk;?50QUN;qSq5KT$V>qDdXMIoaI-l{9m#KuP5V?<N<vb7JZeImP-aYqpt8TFLh$tHs)VNgL)Hte)d7^J5#56U5gry^`(?sVtxMz&w8+LJ&Nh~pbGdyKuUdp(}Q1JocxoeSi7a)(lW7Bgrk!gbluZNi0K!S*Y{hNKo`&6YK=VL}3SpG88`wPr%aZelPr%_gV;)n$Vgg(Pod#RN(_Q|g9LF6j*w96BiKZhG}>w_vh?#bB%G0<(!+jAdE);tqTotro<@+2_G6%#mes*_C>@Yy}0G&_138R%SqK<@2YXt}ZGXyR(%X2{V~+HSJ|g6x^~ZhT2|8s3v$#oQ%F4{jbWDD@LJg?wB?d%<|vR^@)HB-EQd(GrV1P=sl0OjfgO0-J>HK1U(RT|k8*B>e%jmdbRgc5it+F{hL+VaREI3Jf`a6bw1pV&{dBmybm<OvaK(pQ!lx62R8=aoNt0<)$?s6Y|nW_6L>pSDl<}l=K>>EkBVOb7a57bPr?!(>P!9<EwK%bbO7uNZCJaoIA}p350kWs13Yzg;$KSkGuEj(M<(CG3SgahYC5a*zK7OQX}x6IU=Ch054|OFnb!Kq;6nqs*fTsbvr35s%mh@dGhTGG5CC4(L4_)yoct54dDiA3?q`K;It0OI4^!_ht1VvNSRl|Vr!C&^Xl+kA0Qm!(25Qu?FB7d*^M0U&91>jfnb7vif;*lnJ60Ia!DKzst3bM%rX`SM%ktAP(~=h1{9+46g~$7?QLs-A+yN}RoXWRm56bXmGhwDSs5?{L4(|w;^(S&snCjp#HxGis3!p>A%rqJmr{?2dP|~Go-m5+4j`2HpYvlDiSE~=sQUOJpd}!dDuWK~VUdKj6^}ba>QwJ$yA&pi7aibGAri-gr@(Z3=g3l>GQX)G)kX(1Jp7zOE6$PDim|DRmRbKQyncO1sFa6mgoOH!f`nFuh6}0kIfDtspYWWT$+4!XO)fB$M2ObjZb7fKcbLvm$Zn7Yj1D@q4)!FNvWlE4qk0iE0}Ocd2ORhX`o)&+6Bv6D(t(jr;+(~xiOQ`})*NsOomPWj0<%ai@k$0{&^YA>aT#BLED0VJl5#4M<aVNvoo0ftSTq<6t!qt0XH7a#34tp?x(N+TLDin9w^{Q_WgEi#svdPAIOl2SDHuY;44~H3FFA`$Xp?9*xuG~k!>7&F5lo_e=~ZtuM##2aT){3KEI3J4Ijh}ozLCvX=-buTG>-pB-L*P)UR!!fUW7$b`+UaK{TxBAh(r~WSWuse$}%ao0?yZz(0ioMHkDJ2<XWh!14cXBy82cPeDvn1)ui}gc$F>fR~bmAc*ZYeq~-HhNZK(CbU&#R72$<_5v-cQVrk66I&x=icH=CO@p&~bX0R`2@4wjWri<)o%H64!at6ZWNp$0!E}ebcmAYSCoNa?d;1Nuz$W5gP9$*ongE6W%F_j*&xJ8z{7CuztF<Dz{-oCclexTdRNIl(pOl5o?SY}CQwZdl8MZM;n4P-($6*1^JFxm2SOsrg;+4i)pLO-V2$Q-1G(#?GWi_4^KNT)EyH*xZU2y`lB_iQR`C>s{0i+t^OTCEqMdsCs-mr*B6N&0vdq$V&Bc>~=g<Aid=&M8`?jH*<9)zo$F@#S3!cr^!eu<_Dl3#q2gCd9M)TdA>@I1VI-nTqqLu8{zrInPnh#tOx__32a7N^UoGbSUM-E(wdy&1C1&xV)Qgj!UYvpI(nRbqe~&RUr|;%?UuM3!czp!S>{!ep-rWotS`8fLGvXCYmaEG{Ll$0;7|q5{L`9EEy}WCuB@cd#of`Em^=Lr06y~vZYQ7s|7~v6G&fqQVrr%=mr9@6j5$RbOxFzR~~OAzF`WH!TN@&v3F;jun;t|I~NB_v7x3yVNhK<L10d+XF2!z-M()(46I*lDmk3`!7t^8n9H1avVj;5U6^CSEro_$q;2ZQL^?m)eT3dDw@JlaX_a0ZotV-n;?_n6Y&QU4aBb`TGB;=Wee$@cq`-5#;Jzs;_vhbu>EJ%$#fH?wie|`qO+$#dbEy=ogNW0{MeC+QI`JQkY&Z3OHJ(%OHz}o{Ga%tygQ#71_iqok<?z(<%W1gSfz+LOA+XOYCwPm)uT;6^G<5duNh&GLT2YK8l9uvdygBcLM$ftANS<t`NKn%-<OJP7G!0*Ex85vl<q3v5`o&s_j%;|XX|6Ftznq5YIbIJZn9&2F%2cLdc0&o)J-|^Z$<)S5gJ`EA`ikjZD+L}zgf~f|V*ac_dzI?iQnrLO1M_s9c<LQDw%3@X(jYK%!fkOQ%w)F;57Rzijid&l2-y984lLkc1>x#JDwG9j#hf^aR6NgWbsF6~QXUYx_lO}Ep`DBlUb`){c#_pVO;Q$+sxMiHx-WC3ub-sKALf_YDJY-3_5@U@5cp%QG><Q+Py&&Hc4@3hz+gCLu()#6L^mIE>?phurw7AYWnfwBnS(&zQUOz)l`xx<>UvC?N@%gN?eYb*g8JQQk_`hO8akwyRW7KMFI$|Z?t~842|k=NLI6wbgFe{>AS6i<!czkZG&MB?V2xKI=tslcHZRTtZl=*~KScY;&}InP-w%Hc0XWm-HXpL~L%67Q1Yrc>)7;jOtF^k6NyAH#tZ7;rpuD#-gTv`7zR#cS)PB2J))qb>E%&oaOO<s0u|{U$;}L94TN{ChM~c3N`!Q@sdMl-bG|iVMG&v;&QRog!7Iw<0Z0;HgovW0aP(w-pF-*yi9h|wh#pjXyQNE`n7tC{Y+V;T@uDrEkC()*4t0bmbKqB3S@fo7kmee+5(`A(Ez;;YIe4ne+gNHl_Zp53?EZH{A>Lq7@?d^<fM2>|zFq39=VI|h~_~u_n%FnzzTpsAqo7wE7dE1<|R0nz(6z}O`Rh;o;2_uz-7uKetw#5BekAy<X?dn{m7W5^^G9Nf!Aw|b1ePW6A(V^aHeACxkQz+BLXF{Pa>Zwuxy>MgP<4_3JImZEy1cV`Qmk1OVqPJk#hsF~jiV~RUAFIJGXRo_4OoeP+UEe3cTMmh#RuoAUFR<>@6I8lvJ@;mft^n6~XaBwbrw4GT1LT<H*e{`fN3Oo<qlibP)Lo#%1@UbPu2|AjeOT0Jd>A<=_b3zsx7LU*)<31nvC!JPCkLQ~1dg$z07m}oe4XPW9R}bqhpJaZxyr<EG|yo51>>c!!*q-DqFb3t$4Ye%nvSSIOi38O(F~d>15j04tE{&-nMZ-LPMUY+RBNq6LT?IK2-C6`-aZ)di7Ll+bd0G<&44v`0KB7AEsZ_B$u}+*f#uFiBp=i$0pZ9WUERLJjaXF<9q^Du7emo2?vZG|g`cBZ-p4`2y5z1s!pVTWpLuC5M|CsBlKX5{-!SD{q{TE@@s`-xuq3k3+yiN9)ub5Dt1f1g$#tT9kSKnPZEw4@-I7A-!2_#!(M)s%*9`Rb5)?pgUBXJ^BoDY`BKriU9A?E*6_I?}s8Di~GW#~6i^&x*(2mstNgByEq(Y1~v5q$z^A;D5BqkMNe$*BzVkD_aL2?w!QKjCnZOUAk@YwACR8ij8UBVFMOjAWNvDpyKigKG+&C_Zm36=;v?$4-g+*JEJc>rv$(#$<6JNA3G-geQK5j2D$bJDUPjza{!mU_lbss4NYI9oN@Fu-V(F%}r%5I|K!SlC$gUal(bcI%!m92ueG>d&BybD<tspQ}47KoFnNOfkR}HH|M1saj08`O^CpTr7`I$YWVPoWXCK3$Z{tY*vp*T9{Emah1ZHFQYG_nJv2#6t?Kj_ew9pR1Cg?i)=N5eH0|~8!mpC;m@Ccxw~p+m<-&1O#y!@T6Ia2iC&#^A?U}R#X7vMkrq#RIZg?J0j_?-ClPel(FhYulx)#NJ=b9;{b45(UU-8r)T1@EH8eX`gLlBY`w{^slxLv3_#4Kx`CffGLO5&*7y0w*ax5!ecpgJ=cT=#6uuRjtO+!WgU>xalg-(B>ip1^|TTO0g73`vi3k1o{on#onrw_c~rO@1|raii7jsPks>68@}$IDmW=$-NWGXg$!#Aq5O#d4jyIq~uwUs2;KO*Kjh-f{LCTawop5BTpk9KVc00TUr~<$w0)wkju{4!Z_m?=n7bo_+-I==p6{-T?bdHrax4QE#f{?l7WqQ0X3DV~@kT&ZNKiLTH8zfJQbM9-RWoO6w}L_*y(s#rzX5QpO{y*M@>*_<<RYsmp@>IPEBJ2<rIIKn?t50($~NS#v+MQt9o6Clq~)5jjcplEPrutsak=o^2_xLrqJC#0^iO=FR=&IyDlAut2lPtrKm7(LD65w*>;2h%6=E)F(BT^6E8wR&4%uOk{B<LixcY?g8F*sEAoRcm3+>7$hPXUv8BSUbRG;3%NW?O-+GI?Lz+%nQt!C>RLq9Vkk?#5-D|RY$Sth{b!1a*)>&ysg(5fhu$^vTw_&f=dv>Z!)uaQ+A!E6?DQZq1w!m-7;sH!S!3hTU?OcSVN4ex*RgLd)b3ci*lmi%>yaF=#kZHaN!`qc#r%j_aL6n*0e%7G)bprK^VW;Z;*6vK>t1@>xI`v^)eEHC`7)5g-wGwF$I%2v$rnXSHRXze``6)08NJ5pV4LJ<cT+Im#KVe`T6%Qx-g508D8?K%VkJjoKIYWhJOgx!K?G5})%U!V-VZF2x0O`fqgP7pY_T0<732)-+DAGz^nAxJpmL?sg|??KuB7&!XXGjwkFOG5if_VOb=e!6{4C+)N?(wI+I$z$0en89H7>Sb8O5mTl3jswA<C~^XF46DSFdIPPK52n>R$u@gp%$CA`&u19*~hGqOz@lpxXXVuYdT%9YBlgZhJ<P%T;gA)5Vo^@@rhlwab4$ASvX_IvE>&p1PBrB3bOn%L&<E2Bn_!B++;yKLG1$3IaANW37B=R@6yo)$=qo@x|+8mH=0Huu1FBLdNu5==m`Mk9z7kPoxowId(8#l6IS6ilo=57;@LM=i3{1b!&(CPifK&oRpc1i->+Ut_%+aDhTTb40v(XM6ArYs5M|!p-4$Dd01{IT~hDi8qq8U)AlxdnK3@jeikmY+0{I4zK*%m2p$(!(*UKllV$1qI@*8+EkvQ(32`o^lgL!i-`n|ICnq$9Dk7W2uf0Z<Z|z+wA4?eK-cU`}g^84}1sf~HCn+M!tf@RjP@Fl>Lql<<E9x$ODshhwtHPWM^+9;(q>va*f^ix>q&|t#%XyyM`g{7K@}KHQz-l<Tk8t+ITWHRNDuOUXmX=UHp77fdUqm4n$h`8<!u1fq$`Y5Vl>e*7`TftI|LhUyxe1sylPG`$n9$4{=gnF;kO7HOfQ;sPvh|L4WJNI3zAlhE*j<Z~4yt1=RL2;%n4tbKg1mAik@p+7Z8ah3p=IB$A-CPH)9pRFTrS6&bdCCWlmo9#gJN(k6_yXb@^yYyndIX?KCDFrOdYJwWw6_5Cgizhw@agP|E}APEIv5y9aw?Bo_>FZ+qI1LnjNlWRSExQ=|&m|=yiA|wF}*hi-8X~#hd`Wso*CnniP2fi|TjB^eSK^_WNId`0@L{e)oBQ-|8t)npBiaTGYeuX#Dspv%VL}-*3iZ7l-MgFn?ZFyMo;#F_Jh;De{N5l#&C=@#chre*NDfLs~DHx*DF5qOVxOu`9q$BbU7<SoZ4RibDZx2Q}MF$L=MzQm6n*Y(=1wR3y()`ersXz`B#`7OhRDMEUObx%zM4^j>-3L#NfkACB!h`pqJ=XJ$lN;Cah2PFG2K7c^d4e?*(gq7rBWA%)K4S1){@kdpEj95_`alMy{ItLqx(dlxvYEq#6PjAU~XP6czM75!<gHp><s8bl&ult<7|^DS!Zdva!5!a{RGCA{b-5HdbDn?lVG1Q{ODRAsX2*gmJ}=}#yj(<cNnZZ`P%-R`vVbm@lK_AS>Xx+Eb)uzx>zoRN277QPrXi<gF#7+N~P2T6=?EAfp;b9^y4nqUb?X9E)d3_yx1wE_kC=P23RM!y^d5;zZH%nNT2TElOsBWu+=p+WZRak7s%-dZlhwjD9THf0jZ@2zxi$aKYJtADutGH(0JIxsX&8KQF)6YTzoEVksk?1<UiHS^|k59LT#2Q2egZ2Npyzm%L)M&2yJaZi3f0u=W#Z}uKB-@^4lz$^l)$x_PVu`HSAGq|ac;>HC->oPJf_WLh*J>WSF2iRxuprG?mT8BK&h=CCfJ~f3`zd&dO9THBO07D%8+?rb;$vm6zm%z}bRvjT7$%SSX>(9rp$^*ZB0T?StVeC_sWOv)u<c=8l)7#q`uK&^y#ZdGh+9PHiZ;|1yO(4y4ASN!3Q#{J!vDujz*X<JLI}VQ1JObC}I{5D53PG^^06TU!d%XQ%t@3?RP-xWN`|(SmB)5O5&+WwV34*RE_4)d}s_Rx^QB#l<4a1#%=G3!Wx=h$h)10*BO6}zrI@&Co4D;b3{&^q0{POuvpMLpV{qp_Yy{!*H<Li%~f5Ne#lftipihYqY5j9OEqY5Cl%4M+Gijkz2v|OokYYL4ZTIliALZcGie_!Q#l~V-@^%XB4;W8z442xg|WZ^ll=3mvqOI^fbJut4CUuFO~{hL_th2&(fAK~>6y_YkoJ|cw2ora`jAMo`5QEs8sKCJDnTkGq`UslIE8No6RLGbtGW5%za&=pnenZ^hU^Ldj>Z(UJzj_R&Gq5mR#_&5PEhFQNRQQ<32T!LEhI2hUovB<*CSP!kf9Ygm4eDkWOPpJ&TH^~fT(*o6Ho*`i2k#Tr+L?Bk_iu&j}vE9~l)fy{+`^u~ARw@4Dr=PyR0q&oE`r%KXzTKLCe0}}%4F&3o%IA8qnX*5C1VU<7z0XAz^X*JsM~JOH*m}|#<oL805->LYu?X<t;W^fEU}~DqF#`A#l`mjbU3Viy3opYHm)dnD#C|c@Uw+jkSYRNJ_kQ_l$O<v^QIF#$n0(v*ICEiEM0eASHJORMvIVl5XB0&h;ZUJXDkf5bF@-Ekp)K&TQe$3S(snQ+47mD5bm48KUL~43x&2TZMATKqTsBsp+|7~<L>0k<C9ZqV<?Xc`Xy@Jpq=z2fdT=)YYFTte%?g;51_i#2Euc`muX>}AH65Uoz{6(JI<|Wn2(p9dpAn5DGKzhuiQZPGkapO;4t)Eh;yOTV8AQZZ?{SIKNxx&Deh1(Cxjj^s+upFh%M*svwzsS4mw8^`X;t%X-dtU5*AFx!n)^Y>f=^E_i-y6ipAbF3ML{OfGIj;5>l*X$yL(p>i+y@6SVXF0_AegVgsI3^NjV}Gp49KsEwKFV^V|FVvy7^uSQO9Z1{W*tqG&PrXBP)JLg!_&=_|TmiX?GwXXNV&Q{-e(%>#m&Q_`@K#GoV!<Bi*gzW8J`7;D57id%jmUOpL?EUO<fbMwNHXq~ZFp*%+_f>XKqv!HN<LHVn#bG`WN<;doxAhq?N$n9RcXCWjiTz#jYd@Wj4;nHzhih@F>62?TklWoYQo3{>ri|yi2@?DLK33J;z+Lgwn*Qtz;%ZSenf>#xX0M5QCoZ`Fc>zwZ=&XsyCZ(Z-5T_sOY2?=B<@uO~CKfK*~e1UH5Q52afNitr)w<sw~eXrG5KK$bD8BuI5s|uw&c2%-&6TQv7N~mnexEVdk$^_|<O(}fU%1fk6H(&o$kelm1>D-Bg8+1I3MPbk*&tX;}TlMRZSV$Zq-o>I^!Z{V&u{v$)nIUJSvKA896&b@#UBsUJTb=X(;|!|gyKQyHz*ODdeeK6&;q{cp1=nCa>Sh)#HC1IPTcecRKX_UDi@M%vOrjzi`X5oK<mTb~i+UXrZKms5>^gx+wPPGjd!0t^FTG85XI4~UJ;BbEvLTga_ZL5}9bpFzo!wg-20=4X8X&A{jknyeszSk<PJVF<FDt5n8<g+1;}K|)s#}&H7XgtPSeHQbJ@s%Gzcm?c@Ce96BHD{IZ^1>dk9D=1>atqF#5I>S)XhHprj#csB2uAOFUx=sLMZ3}e33GG`F+>fMPW>-oJu?nkw2H#Km{0V-}Sa~4Nb?k7-ZB#v@eQQJassWOJ^l!_d$%dHZNnX+f)Hz1b*f?3Y7Y8vX_-W2ab+{u0<J0_v(GLGwoG9WJt?rQn;mzK^Y_6?t&$kU%k?|b#I)hy~r{^A@=dE3Gy>zun|@=Kpu8y1)MiUwgS&{okAglsS8`{LG+C0JLZUVd7aKsm4+4p>?7~m@_?d?GPy!41lV@Z`#$eq0`Q0f&*j!t{<5>EgUbP6idd999XBS~hcGs_sq)2L&1_b9W@KpNM|?t6l5kJL(ajCgeDx(qe~Yyx-bb<I$t0d7naJcmjP<NBrMf@yw4TZc6~1=Awb4tMPylhoL63+;3y|xOhl?NVffYtwj%a-!&GPj_=QksMjc+qry(0Pl{b19oTA18qeZoUA3?~}_D(R8rI#G)n8>z`82gBmg`mN6&f+?@$VKfv?Q_=U);ChZCkfJFq`JT!Yvnc99ar&^d@|Dr5(oo(csI$S^MYBke5KLrpm(`_NPsd2@^tx$(Emz`r$z+(H70aR&Z$EY}Q#tj6p?4P&m;14|TWDA+c}8w@@<VNk_KrR|DjkPKQo^1mIF5-<9xl0>YV#NleZfcAM>;iNtTt6oA?l330LD7EN(7?8X&o_|`Hvz>U2qO$vjnCNMZ;)tY$YR#3iTUT<0|zqt3mVOG3_kIU%`Zr+mHkZJ8pI&5Dbtho5|3uUcPFx_}s2Dn0&Qy^o?9hu+DD6(L(BzB@utfg!H0HzMl*|QZ&XlCuNHlgk0$jYTVUKE1T>UrmdTfgPQw_>47H;{u2EGcu7FJ6XR%-b+}D8Pr8el-_=Z5Db)KK$mjx;UnkD4PvNU;Xrr|4i&&MWi%B2h+nlDx7D(}QXyq6HKvI0HM@`l~P#Ab;5Jm+jMbM7;@~|C3@ptvHB2vwDBU4tA+D|HK1xDuN$vq7Ub%0b)*?wBhpc@@ul9PD<^?D+9n>RvP*hg;@6ln)1!j2=kz$EKrw)u#nZzkzl3NB7+>9JYQolgy*iUsvatvyhsz~nNg3O}?EIe@ku77B3+OL#HW2u^(#BWs?Ad=Uoyr?Ro5&1p&A`n9)lIkuoditWLfK`GXuiPTUHa#F6L-w_;wD-Q4B8Ms#^ibZ&Y^PI1_m|Rh8;Ofzu)+(<P7lo>6Ew0=b>+}q+c*zWp2#mSmuP!gd=Wntc4jun%wyd--v>#Y?O0Lj7-{USYIadXU_VLuGYq_*Ea-r1)wMP={w^K2h+SNriEUgcfw91+xP4oRt`a!n|^tS3GZwp(WIh0&#5w6p7knK*IPn4)tkXxDU-=gO_+MsPh)r(i`u!@M3$<Y{bncTW|@=o#8Cd~mQ?mV?ev&#0cGu80a^7ECX7A#Ane2ZWl5X6C}ro;YIF0!($u4RejTcQazs2Gy8BYTH7Wnc9PVTXXla|x#-X=kg_p^B7};5Y#bnQ=#|SIV`eLLG$IQu3I1oENX(+6m#%zK|E8jk$P%nmi=3RLm7YCPp?0BZJAA7{j2&LzFic=?w(q9$hm7&jkQETAJLm{(U)<n(X_k#(@B~XbaO4@}0dAvkOQnl!#zu9t|rmU2(9Rq<)GVyM?4ZRd(Yxb}Hid6?aL<IL;r%ms%AmSvB)A!Lbarr;u)`dA^UO5p#87iXrv3bc5FevM(fFY6>u1lt<)bNbok|j68uf4xGG@e^Kn<+8=qp;{;n2wW_S=Ty7p%UfJ@ihQFxL$>UcJHjQr|&e*0%E*%O~G9ih8V0@FXMq2to@sD_5U>NfU+nE{I#{*o9ZXu3g>9&)C*AaW^g+`2DBcdWaLY8My6rIRE<gKLuyINlQKv#Z7HH@JUgt5vp5-3?j)Xo$X?3+9k8ZdUf28}O>mj=e%7Qhd>gS50yuR4g?WNZS1Ta`(R9ckTdH4%I1#=L#X7v!7%rklLZMW90=_|jsfP&+BK((qCTJ3XJhCV3xd*8bovQ#>?W7Q1E*4Wtf@oftoogcvUCDI<)96Uf^PMzOV77D(#a@n0R5hl|u*&Kego{CGt4apOVeQ0TV+gyO8sr3Qj(e#mWf{S!mr;kl9T&<#nsi%IYz+%A7Pn#ev_B~8x=*G_>`7#@T3F}3*7;NABeLt{Ym*>*QnLd*9TjiD|La!^mBN9fi;L$}(^mt5UMrhq{u3HK3gc{Bh#ps<35NoObBr9yZm(~FXcA+m7oeo753!su+eCa#M;8sZSzN(%_>8v5Smwb0BWOM`|5{<ZP;gHN8~1YuA!;-NWu?Pkhv82ZMNea;+4IrLYzK)pE%>nB@RGoM@bl|yV%`EvM53x=w&gyFv(e1tx;l!sxAFmxh`X-m!dA*&Lju4PmVoL5yaR<WgBW0R&Pi%@jC-ow8iF0MI}gb;j~nZ82qB^x@|GSQLoVAHzNM4IT(Kf^?!Mix0~q--JdzlOoC74damX_b*WKiWW-WAl9pOnOaQN}0w|P7Si4r!&{CQp-rnZ1?d8ik8Kv{9S_jB48etmgpW;`oL5!$}sbIC>Ef(|BQzztge&^j%{99sregEU@<|s;;gO5a5opC07+rifsiwnGVLsmAYrr_d@vmkNU$)&QclvAVt5>E*Qid2jZ}naE!d_=h3(TQB{TQW*KbKegNNZ?U`Rurj`~O?m;#GsN<Fn*g#O?-+Rz6{T+_@9Y7C$V8bhII6YOOp-MZN@CGZI*GW!i2El!i_c)%Zo*oz(WC2%#gOPpCg*4RMTry8h;R9Mizk7xS;!<6OtivANxCbe?8heE){Gh4L97TRGnT&#Cu>Rf}RVHbpNjb;t*xte<0fSG7FfopkwH?-twIAO^dEr}M)z{n#MIxU`XoYz`dE0CqCY=&vFsrIzfDB*dt!=$l-X?8tppuJI<s5(gurlLn_v5UtN;FXOnv)(M>!mf>UCjMN4IGuJk#f>C~X|r?tCT@@b5LlWY=#UOG?{lM(fbpY{fKuxOffiFD@h_<Fkhg6pcJ?gBeo)KU|6q=1+@d!M*JTinujrDg*`vce*!gDG!o%G%IACX(ek2CLm|E3G^VCOi)9CgO!+a)C^D`TQBOOh!&ra)jvFAkCcF#L`pM9>Wgf$V-T@g>j4(otv02hR3{lqcQu=>ao#f8vGWNmQ@jhzxS4HD2s3Hez*stTWw<U_3DQWh*7)ZN%AA{!wx_RA&RkTZEWbdz=i>529zp-sXVKU63Yl4y*$cIi_#&Lny%|DC?DxfpjDT220LP4BHk**&aYMdiK@wZB5ex#f>`23?C&+pz~QD{!pSbs~%PdXwekeYF|eJ*kNS&dGc#8YD_7w4|53W&606#*mM)L6|ZlQE3e?K<gn@fqX8ahKCkQJtiKi+qv8t;2?|2%$OpwoR^)x^>VH~IwkDUNL+zNwZW{NTkOxMuVBP%b&c0@?N4_*S7{;o=+HYZ#9r6I?Ww}PC|{bA>8^y)m?LMrj(Id@7et;u3Wr(kHcGb401we9al`0Md#?zxMrx%1m|5Z_nB65n;|wQ7qb1G)uq3MX!7mB|VXa*fnF`W=L+A9@HKV0o=OV-8LOmmLrN$TH*06|vqt@2PKe51@QRl$P&p4+?__U^G*FHX#coeU-RZMdC!+l`niVGG&OQFyaHR=eRd!^*Vs;ivbJ6L2XT-nsUHBs`E2JOHkG99EMd<6JR%v%lYh47{dbq~7Kz*6rs(^sk4yH{-td@X~JFJH_9g5C^GYKD^da2(K-c*R|Zz$z~dJ-U1wd`>T81MuIB=MN?*NGF8oNsN&7R`HWz+jIx;kcmPraCUc6Q;(13cu^G608(<znlk&NZd%RI{dlq4Cgx#Y-s8>ZpF|h=Sg4Y)z2E{6LPVI-t+Q=q#|thEe9$56rBnn{>1KVo*iniC<MA>!EVSurkh(ysdbW>Dws6P5Z#za-XT|*^oum7Wh1v<q=UWm^<P6i=1;S$9QNEE~J=-yjCF2QDD4han{HLHj%XnEEdYOEKOg;)R882H)4GSaA*HtZ50Z?ABBCP9qghhsMo>Fin$D<J%kDAe48%Ni<3_R9+gP$mh?C24;5LxSI0SCtf{9ui%_mK_F!U&!d#2+0md@!!BZuFrWACMt*`<GNMN>5}uCSvHf)X-ZL1>FBE;sENUxNegcdx04NgD>jE(Hb2YyQQ&W3z$uP1Bj9|?YY>V>ToRingB{*JKqw7xMQ(A+DwCve=1#8@o4rLZZ-=sB^gg`%Lzhj<Fa&SSj88*JXpIdaN!1TP~Wu)g$QY$`*p(ii?V)C45f&?_Br(_r!}OM%IGqsDUuF03mqClG&D^X<bwshuuXDw)ao+|?ITR4TDc)dPTGe!wW^{rm7zDMNod?@0}OLk!^C$REfxjR5{*@I@$xQq%Vz|l%rwu5nMJ%fJ~(~g8sR+6v0rVXBOqdMIbg=S3z#Ng={Jp0UGQm42j=xzv=o2v^?kXEKd({xj*ySTrSY)V3Zletz)7{}AQWcUC(t1InN<@>a#w1@8BQvH?zqzBqo9@HocL#=1_;4#A^5@)J&JbH8?#oO48WTMtR0jhklE(&7A!6@4wEfh{2FGolxhpZK*Mkm*#7+C(oXegk_#U?3B!_0ASOzUX{t?V*+}?ySbcOxRVe`qh?UFIb!6kP<pul@NyX2aJvzLqPLE_f$4g#F4MG&8o{$#I8ZPeGJ@@F@J?wd~gjZe40mY8vs4|{zZ=;C%rgQr&<&>Sx;2sJZU)$vxG}WKvn~md`SH672OygFtJl|+0Na@N?&lSp~I@(NrRGk$gIX%w4WO1tAhx5}S1|WIaz}Oe}1aR^WrPC(NK2s<$j;nhDxFRs^Jpty!@qI~X9>?vuj|FQPMf;$0lvdZo9T}?0&ZGL|1yLs%y$&HL=-y0)eh}-MBAiHWCLHF9TT$8b=-t4DqR8GOR)uIKnFwx-4`<y_@j{)bp*K)GLaQt`BW~hMt3->AxN{mCQ+W)uWkW{Id~MWanoe|s$=542_I%yPIzI&=`l!aJ<75lS7D6&UOvIQvmh9|A1!b3@W~sLJEnbB+A87E3BlZWC^h}+WF=Fg#%a6GRi`Xx*y5DeE^Cds58VaYwYRtUEL+*51JdlmZW@Kf@8fUn@&y#H8;m2GTCIXj?hG&B>1)NA8Q!@X-l8CcMKgvWiwwU^G@oo?&<>I2CV4i#%LNp;?FD^+D07IP<hJstKFepJ9cxz?-I4?d~+a?4t9K|D}%WUYpI>fmLIDmM8Om6)YGd+7^H@ox+IHwsV8$S3Vj1SJ~a!D9J)idDbABI_h!F8!ikmbO!m4Jsf#7M#LdV9yAs)9)`Q;H4FLdrT*P&%k=6GCV~&O*`pBI_JAvE$wX>aoMxXr^}iLUn4v5EFH!gy>*vpr2>{E)w9aDH`>GLJ&fA>on1R3uz&QaIAQ^=w7YfXqahrY3?Qxa=;#i01;C_0kiC#Q%F^D%nm^Q#17Y^&>?c9U0~;B%rdKg72cl`8!4rS8nKc7qp*=xfwMwZcFuq!@h3c|RB6O;$Rn0A8H>`}tzD^V1e4>yYyjQzXF^6c*yCjq0diK1zCxS#?86-WVO9&NM9=MplVHTx6#xUC#Nmih1iQa5eewklJ7Ulj;zV_(f|Hbyed62@L@G?#8`oDT#EMjc!WHe7+WB>~N`Sk_dvr96?f}aMVUmQ<3S%vRp)2fFiWZ_18*)%sWK`Ze^<WDrBTtM;1?aq41Z^VB_X3Px!n5S6;rVo*HB^TLy0zI=WG)7Xwq9JJE>|WvB~DuovxzG_3+!epq?77v7KcxyfKeSOqt`1uBtb>PK8-PT!A7tmqN&6r1*H64nV)%fri4rweOsxPUVX12PJZwXY_lz9Y*mg%Pla+jV$ckXd1=3sKnlRKYoYxaJywNS5)-BMGZ0aYOej5V)$W+5^ZG^P^0E4(xmAp>=H+U16nD?<bh-Gs1KQI(L7^rL4$VuPF0x(+jnnKmYJ;9<->vDQ!dqzgqk6?sWv>?DB>kjy<1xkIRKq0)>oI@Oq0b{c(XGc6#*@g=omR_7fl2#F)dS3FBwRNoW|TY!Gg>SPO*!M)_G+!F9wzS<`YGUkT3m)=7T6b@SUs|}jb(^hweZ>$Uust)R#PF{lo7m1iA!XAB^yKUE*bBQgHKN3QOuShiI%DB+=IjwoH@^&IiXqog{iY?z)YZDit!}Ow@r>=>Kd89nbQ`<DXeTHXF#p2UQ?%m5((a3UCH&So9sMGEXl-#oWKPcHd41OMB&JouO8v1oSu=oM`L@)p~bY^#<J-kH;iX{bPAK#Pt>;{1llG`*$J0`Skfh4(<is7(9~@<AVSM$SuGvP_^XodsSsrXh4rG2h7`x<`6yWd`l%3Zs*h|9s5+wpxMRHe3=^^E(WlOF5W3MKHO|$1x4+w=eQneSp8CPBXN0l$oOq{zSOQ&!Z`0F}HP^qH`Z19z%}SNiBYkX7qZiaGISOtjWI(o>u-QD1%wcX$k@|F1ujZHM%))4;U+g}|VL>3|+oi!BqfOJk`rEPk>pwKbXX^bT8rTBet9NQfV-8#HqP|QsW%WE<QlT*MG+b=|`wp5!xRu9Fe~Z2L@DL20eHD>HCbKFFLpodoe;;P<X{HfW4l~Yke4=n{7;@S;Ai9DNnp+dX3iS68j(&C|(Z>X@EKRQ%VAC)?=k@0V7i#N~KR?W_L(HUtos#)<8*(t%cCM2zq3X#cX9PQ@AyHd;)>gej&(IvUgrx%0a~)OcAtqrMDc1x{m?YrcsOXvc(+5hCRCW6Q*n5{HNsb&@^oME@{&rv1G*h}MLb6&o)e_73|G&6orMqXinL<@z5y|eEb9W_KnGyDYnE?ugLS)x{sb-eRW|ftun8Go;-mh^HXO0RO>E>Rw;Y(#E=oTZIP6T){DrxOtFp>Mmk6w<o9c@l4?cx1qB<5T~0a)d!*}gsclWuJU<DB}7?8|4i+esZ0r~+V-sdH&^-oS@r;ESt}N!m4Iq7S=GNCgrrb=k+fK4awZJE-xL@`G*j*c!=$fGNS%>)7U)$}RPRPf|h{;&DStcg00V?5d(^>Yh-Cd4iDRNF0B}^ZQtz)DI5X8v6&#uR%$sCK+KSqwYcZE{qY5dvx0YP|0_yk(~YgNFNM$I-ja3O>Un6Yx#u}S$p)N<ZVI+a&GIF(OMP86mE5xIV}xf*!_|)_@W2_zL%aAD?BfjwT10OD}3yVF{MC!b%EUIXxiEs89bu%Wo(a8TcR_mna#HsbPgkh6X=plmU2l7$J{lPFIHJ0AsUi^M_Q}zr@6O9dXZj8zONG(hLYGC*owi`DODsl+HYi)44@E^xA$Uvg>tFY1(ea2JjtdI|C^^AoQ~`YJZV9hg{*TF4ejhpOFilgNj=ZIM$uSg1JhE`@7qRqegEHw%Fn+$ULN7lYr18J)>5bAGBB=aZ&kPO#06s*1^wx#LZk`AZi)M}9tp*QUCvRs6_=ECe+%-kM+rlr?8Hc3Vx9FNqAn|u2Cg@#kbH_yhk{wu+oS#;mAtwqqY#F2P6i$hh*02O5!}ntdfA6PG#(Dd?Eb>r4zS8j4vQh_?x_%rs&#23frTStNTvJ<jh%ha(+k9OY}w&dd6f$zoR^N!mZEKSKZ$}<>PZDUI1rqsNQ<Q{+!H9{i}zI;vsxqiP9Lwznkr$9I%o@(9r9;U3~S<4i+ss}PYd9khksxR853xMTfBhNzWVyb(idSeoOux(gKJVLRza%~G9oEO&O6OmalkR2MlUPY4JuA7jFICX(UA@bAsAo<Oi)>P+}<!*sI!iawKNqoGwE=^#!&?gwu^U8ZSpOMMLoI05Q%;?R(~V3<l<Hx`Tterp#eolbYBv!bFR%1xA1csyz_O*-C=~j0Gm2So;dlP;&Z??u=?gEUk$A}$LeWV1O*1ZWtt_UqD?%Tx|mBQq>0i@gB5MJw!2MKfqU={FN<i#rnfF(WpVxk+yRk&0aHvN(sVXbp4p}xu^MKEN3mj!=%{Z)$}w*%zrWjft~mHKQ&5OoQF}7`af>R-<5~dZQS&UE=X=UrT+rnAA61MjcE%Yl`Xr)W$Y3GfN}Q|1nsrt;EwDEAyO~SeY^te{G;7-vGqWX$HYdd2I=9MK)CzUbBw5jy!(c$%K47H>?KK)}5+*VjmIXVik4l)TVy7<r%^&lgZ#<aSqi997=28ypEr$0Yv}81#3h*pV6q}kR)cZ9zECo!+NGZluD>5|~@>g^stZ<C9ilOqfydT(HpWgX4`qFB?YeD4JbhBYqG#Bth=9`fWchQ+fpvnPyG>7MpMf?5R_lKKihB>AE*A#Z8!fltPN0tuk#bUo=b(~ov3Z5<~5mN#qT>a)9A`q>^045?P8Ht&u=7*{DhpEVz`wjt@t3kE3pgER<_a&;o#6Abz&EGOEi}mK`x52ohyg@2rttQvys61TJDn_0j=3$lTq&LYBxhw~gK3{|+mD43{+Nq&c@rNF?IBw0fCLn3UojekGz)K-CQcZhwF%^j$5SAk=E`>)i#vta-a0nRdoBC=r=Ri4kV4!p2EjqrV#ygtIU=noKro*x%uQeXCKWsgHFxAD+l3o7XR^{!}VPCMqGUIXg!~%fpFUp<0%V0RBxXFfGi+X`A_lWUkBjHO9t2~ZzmnWY4n=c3z*N@}>#Aqy&Vb57xp)l6suqvjRc&jpQQwsow-=D)2ds*Zir{v_dLA@gy)q%eZkg~ZSTG`sRPCo_KVz7;YRi^+M5MnAZvq@lP{cE(f`=t`s9$rEioBPRiawJS)wx2ia6dORceMWX2Ig^~E6q5Sf#VS@kdycka%!@l_$|luO4IXolo}2sCt!z(3CBE__9dpp2V=hF<ENv@=8093g<L*&&Ar97}XoXNI8v6@bL8pVpJam4CbKXJ2t+-*78ry>yde?q)J@upsOVRBRWU+y-VX!5W>Cs|RZ|JGls0uKjvC-_AWEM-c(z%-^KiO$lw*w0=Ju$&tZWMEq=#-C8`O&JNIyJ*>N#!zXue?VWGb^vNdzoN8=a7Kn8PPo5uQ8!4T&=s(Gvm=ZV{eP1lbT|5Y-W9GrGi;wrKe4^^YqT`1D%vHi<e3%QpLL45WCIuYUe_;j3x02y)S}Eu87h*-@tI)ZS$9^X7p~T{U5eJtlBqB?<Hi*)O)48n_LB?zr<6ctuvEV32b~H@Um#Xl|r|Q977>`h7i?Ct&QTme3#I1GA`Anp~o4cF!B1lSkcnZ%I+dWrbq3`-sd;nTzwb63XU9R{`(-AEb)<ZBHfeCuUIg^OOd1&&^$>v(?D4voxk9oqH?#ZpJcK~=V@r-#n!OD2zyDWV6sH#LY<58Ak;<A6YY($F=+lkCX*sIHP-Auv~&33IlOx-L;R;<HnY&=s_OVf8w6MTf<}t5jQU)NaFGgqD_bbI(5wJVbORv=QF4UgL8Krq6SqwX^d82``{>To=4<vk-CJ=nq~$SEm&8%fG7{Jd)=S9NxKH9o`-k_52ziZ)Z6i@TuhSMWm4j%#53n~hL3O<m<%_^Z8*xXatj|6V4OLXGuCUXX-hEOE`73DEQoe?w>zrw;JIc-T<QAUNM}+^Yz8k}ca-MzF0Sd;_V)hUia)7i#U#c#}0PF_t$GT5oylSf$(oesC`=`f?<vZzYy$n$2NKE5cV5vO8zzQiqLo*ZNvi}jojZw5$m$w|WibZKs)b2Yf4hlrWm7m6<ZMYNL1{z0ik4%K~PQKl4#~iyxbt6hR)f*d!|2oJ2=jf}Fr0WkaGp+QQhXZL`2D`^sqN~)L=p_z)t}FO30|Tw5)Pu?Q(UI*!O2jhS3v#$KRUzlyQtX0VgR6zq#&8VW2n3yCC=h>FXhGclv%cgP*{_z=PD982zy9^}FF*ay-@ff{1M7jVX$FgW79Dj5Tcal7EveKiHTDPA+?CUL7|UwcWqMSe$hB9p$6!NJ$`B5>L~zK%|EtHg-ZG?djw;jVBjNAVhFw^}yzlv%;E1ZDDC`{=2<jM?weaJrD`c8v*eyUM;Ie`YTB?AokY~E$W^0qZQ1<3yuI$G*eGp_JDomI8@c!1(*VfkVjuA(I$H?NJtdf{1NNWyL9@{V@2G*z-^w9qFTK9P<ZDT<cQMBz$wXV&2GiUkWajz|%4)8prUOQ({kh{~L&1#d&;CVpVct!#OZNTntM*l8<LR-QLbA|Sti*8&|_9O}!Cg8>!L@PrgxQ=A4m)W03LV8IlQ67eN{cd+Q_MO}?$-d>@L$}>AM-(lCrxdvWR)y3xqx_{|%0o*h*#M#bG3B?v|NY~O!9fFaHT{BzB8pH1#hCcVkADpHD7)H5pDztrOz+=3B0(DbkINqhtCc>xR~%|BXS;2O8@^4M{M<+Xz7q<qm?8B)&R>Qf_2dC2NYsVT)0J!RX#R^WcI$LCZ)@*$`ny9p(iNA^#9}YKz=pTguPx+d#EgG}u7}cR)p*i5X1_%}^8#FN;T|>kt^EC^R99lz7VnvNk@?~_1w-pH_5b$UEeH_cO$-OvXW*5f8$w#P)#HHgBOLtXKc{d*>;fGUp3MeB9Q{;}Ri-1{lkk_o(56-a3LRmEW){o!ss;^f@OsP$;NNE`d7!qt$bBsEr{}{OF8|UHchFEi+9GBg_sDM7CZOas=nj`sDBk4p*z8O&>UOU2{RT%gWsDu5_c?Sow{BP~VPXS4&GP(*wb&qYc6DB`%f1wHMEjTe<TxCGAcUCKg}r~TY8|4pgcFTy_L)=vZs{@+EX@F#()6mx<_R?N@k;*w?bom0zfnJbTQ8B}+b`dK!vUX@wcbH65pe8lo(Z98(iKtc{Z^^fMzw+=sbw!$^DkWY@u_u3RclUsz`^VP>ua83dDqW@e7DQI(J`zfbN%=}hMjR{%Kxfek<wg+zlb4LwFjW_8F(Sn$<+V-%fFB$>-$G|&C(u=_^XcyfpgVjt=@ahc6RpU-*A7Wc4ckvT326O<aeU~GF|mchTL<Af3W5M`1tA1Pwt8;(u~IU!aVMzEKyg~f}*-eLs+OzF<vJi#xU#mDXI*_*-cQ(DKwtDqV^J1&BdZWb$>@o?sWg=wYifzlCm_`ARfx5C05H6SwNm6<De?fEK=%<0@6DB-PZBW8Y|=1KBnLQ#QA^u`rA(@=>PS%pMU-O<2L=r+uJ`+D5{%O_jx8#4R8so7uWvPJyuJ5A0f8-VC#tv{_$yUYmVqndnh&m(r;Z+JX&24`WOKaEM(QHlAwnXqJ@{?kIU$K=du1_u;2fst9`&guJ?ZVX}me|V-Qe}<CO9|x4%J+=2}(MO*2*tCHBe|$kKr?Di6Y;LYq`9r38lxS(d_jRCyU3^XhV~gArlW*Dv-8Z>!C2I?gW0+909^0p_x?D%5V493rY!8!Yk1B@2WgOnWT{+POCYY0-qY9^4Ipe->R)vw}sXL4j{$3n&U5uPVlT^9NW7e%VY~+V#jcL3R-R81Ypiqu7U<Xwzb<!G_(Hz_-gT<$#kl2m(vJ$0Z0N{f>e99enTS7c^df;r=c!7*5;XuBKn+d4W$$@OJa&iod#kpc&CT4nkH%g75Ku6jjRkKZ+jUrE}#yUES8YIy(IB-qj4^eb`HZnBwgRUp%yF{E)Abf-o#Rso$kDu>9M%`^WvWjH>KbRHWtx7YkLQXfgP)ivt{?^D@~K8eI%UQpo2S`E!LSa<V8f>|o}UeGCD9p0rIY=5Q?L;uGRvtP%4#&ZI=Vd@?LqRzGCs=7l5CIvb)wd5%;Br*iXWLE#94c34~Idh==0k<Cj%SL;EM+r4(LLP%7&`aytk6q1h9Qj`xektZg4o9uEc-Mn@1o4Xc=lJ9C<Lzvsv(XJULZTn<=Tt<9u5WK251QZ9DS|PrxzRvl6w_HHe^49g<*;VcYm5@LNNp$YRSU<fTaD0Jo?NJn&YVnWydy7i6)c0C_kHatSUJ=D+zBkYrU3VkgL?>Ub(kdG=ZboCBGC?|IQwo2kh7;-1%~zll1nas7Fn1#11|1J$QJQpRL(D2<tA1THME7!tJ29fKmT*qRc1#b9dS*sH?12S#MaFPb7qKT?Rwq5eM$zD6Slux&g|ZJ{`<g6#Kc#UoHW-h(nMJcVrLMx(NYkeH%i7=6^-g0F71_}LM4^(KhwpFdbx1Tyt>r=M1fs116Ny#pG;)9IZK6H1q6+H?cCHi&sVuv{`FZUKJ80-oY&697%|vN{u*x|ud7rLJ-A6R}6*j!IsRnLPzT1vRphc=CGk#nIBxzt(#5rEkBnb|8@f-Qjc4mM~B%(cJm%&A_k9D<MKC*hn#5I>S)XhHprg|l*WKyA5FN=^6LMZ3}e360;h0%N8b#`SMlb)`M{Hu&0^5@cp@c@JEyWUo{q3PHbgN)?X`=Un1(|NPFbXH<^AH--Y&ysM{rwRxo@H59zpwxGhy{rT}aFiT$3)X?OVBJSM)5fYphP3=l3b&L}C}X7aE?9E;)puIAZXPnVS9%60#6I3NL4IZoHo{5<$iwcefb*uvR^WNAQz&FGyv^kMAbQ609dkswyv}B*dP9o?_K|mOc|g%dlw6@+1tD_J`#$eq0`Q0f&*j!t{<5>EgUbO3g|rlTIu>=?hcGsF{4vE@{cKivW@KpNM|?s|l5kJL(ajCAef1?re@pgR?u+)%7MaAeBomq3hp|3uOsS?kqTjs82o=6|zqQdzm`nk2#X-M=Y|Ey;Xa-G#J+Q*4Z4Ipgq*=ax==}bkZ}DwLt5+odzaMN`RST1wtWS6-hT+McYD)hkxlYug#ztx~$-%IAw0`UJhhWO<h|sH#CLHA<!1WwOAVpJJzMKUsi8Grf9I@N5wDOhFs?t#2B&f5&+Qqa;`VdTHa+lSmSx?7E?ew~7e=S$yc*|s%Ulq%u6mLIvE>k)64?}Y=Brf-3Z}+yal=_U^=;Vjm6zv^-a#T7F1KsT`R`@=$G0}I!C0A2rAj6?A_z3$*rv{AGrs^p~o$(jISm#!mLNqunW=1prQADW=&Vgu`z|^5~84ZrDWJFP+esVS5B_L)sXg)lqOTzdonDB89Nr159W+wu{0GY0u49)80qs>F=xxLR|@<qzgH*!V8I=cx+3#m_KCXY?#qhvndy!4ZyiHgQ}cT%=^LCBTfpd(eyw6e)wVcNQ*GpM<*m>zht;4jf1fR_X`H!+STS%-7FdD30X{H|ugN})d1Kt>m!{5o-VeF|S)LmQ=Szlc?7x|sA4KIb$wwl|8WLo3Gs0FvTkU4>!$Kw;p6K^PUB6hS-U%fogG#oyJ(ipWLRZ8}*=YCox{6&RV5C-*cc)Bz%#lYRKB8FZuLOL7t)zg|zoZqr663;XD8f+B6)MA&g87no$7%r+lUG@~S~J;B9EEj>2tx$~(3RI#8wskH~H6qsD*RN;pfA_vg6!$KiWVF@p$8o{a0Vr0$pkT1fZKPvk%+MJf;tzUZ^w_^($q}VRb3`(&MO{9iukdtx^{a)4(Tyc00ufV-3Q7pnEoacPa#pEh;16PmMv{reYxF}RjYjNeiSUY5J#Y<**L}1Jfe|32wK7W(taOn8ovSp=xq5Z(BQ*wpw36IBZVb9sTv{|P<UCXVdnGCHis6CQkznzN7)UGbFD`|bGq*c}oX`1hE(hoW((A%n$yya_s=6HL1U${=sLAG3JK2f4pL2hNXhm4-<XoI#1RWDw#!zv<DCP!n$WpeA<$veeUn=}WMxbxH=%_`f&&Q!xw%g<MmTCgmQ@-2dKKoAF>nhtwlxyZ`0x|Su9Z;1xipkheUj_e)Ulzr7FgdGAF&n29Wq@ArwhbmG^g5v}%WX2t-UMbg>3Uv@-OUYy6abCQhZ%+t^_JzC%Z4Sl@)Z`(NrDCoKGBL727#U2?#25xG9-_RtNN*q*_vo4#crF0Qk?v$KdI;uBYO?RE8V3T{qAg5I$anTe%q}3QP$Ghrc{HrNbj87LlKLrf>=u&tQrV4j>{P_@PuwLT<2Zj7UuspPWYtQ{1jjPeo<h2%=J{SrBj)PF6hrE5=?1S4WnW0V)D&R2C|BfUNbok|j68uf4xGG@e^Kn<+8_D2<E-XqM4V)(>sn^Cyt2bs4S!Lglj~OwHjQr|&e*0%E*%O~G9ih8V0@FXMq2to@sD_5U>Nf!+nE{I#{*o9ZXu3g>E4%u*AaW^g+`2DBcdWaLY8My6rIRE<gKLuyINlQKv#Z7HH@JUgt5vp5-3?j)Xo$X?3+9k8ZdUf28}O>mj=e%7Qhd>i?y^*uR4g?WNZS1Ta`(R9ckTdH4%I1#=L#X7vzWjrklLZMW90=_|jsfP&+BK((qCTJ3T*pP4Z^cto^|~Q#>@>7Q1E*4Wtf@oftoogcxq?Q$`pICy=)pjACoEERfW-<G(sA4;QJsJ!@RZ@Z%BD$BhS>L!sXS5Q=AIE;SHT^Fz+j^)C#8hu22FLpLPlE+)Z?aJ&5FXd?Syl{7sgTss9$VR#JA$JF9SgLmI^42=QJ&$hdv5?a2$Xbg2}kb`;|Jwmq*8oJePzU1mAG6f7FNr(WAq1*EC0C-VhNe$D|PWn%U5=*8zB~wRa@!R8+8hVD&*>p|h7kf0sLrmFk-`l(vnptFN(6GQC3}^7kQ=A|SYDPRXhZSmL@>99>jV1e>IgE1XZ*GBla}?H3wytJAx9ls2*rM{~@Rb$}RbdIke>?aHeP$^S!x&-cL=w}Mn)5?eB}U!Cs2Dh}s$i^QOS{G<O-&Y|=ytt_e?Qz@b0i5N_zp9Dh1|n6bgpHhBjdrQb)|_k(V>5Zi9(Gma?(iILg=y%gIz1)>%7t`BXxeXfiB19`x2P+nzocOjisC#WI><KT)RpwBPp}p#~&zK7N7EO3F?c0d01MadsOKIQ@JR^%;TY0fadWtE>l=tDH9yZys=XAJ5OLSLAc_qt;cXT7oq@3Vb+0=GnO*#ERG0rv>ALb9S=ybFvC(#(w1Vl4z_DlC&Wf7BC-~2Q>4Q7X_S(g`{(PoB%#5>@Gmf=Ax}rWQVFKOVwqA;Z5N?GIF2^bK@!(AGlLofD1ydNDB1*j*+{o;HcSb8f{Dz214oO~q&gn(2O;)i$9xG~4eb(VmX9?y(DkJTDk2pY^zY-@KEW_$IliL*M3PCZT<)O|u<^_mZLx)R7!4QeotQe;U}@L|(ORQfgL|%~-Zo$++D*_|p5F~Ec^aOu<cyX?3ua*8u!T;GCmiRs7S;-6sVbXcnrx~)?KDbw-s~`GtYDg5&l+fNR3@rU5`(GeQCjTcu>^Q!W6P{JOSrIWBb|vqmmp53-A!>L$zj^;+`fq$Bme}K<_9{Y!_52KXe40#EF_@RIzgbtlt}yw>O16Z8;YGhi?J_i8T%j1@r+yaM&Y^)!toVdGBta2m<K!G%vyN3TLuU04AYOqAQ)4t`e>f|C~g|v{$ZG(3Do?|hTup?6YR6oI$rEK5w<<@PCjOzYbs$)#G^746S2cOU>d*$;aNX%3^c4h@<eeVbP`!xoI+!#1Wkhkv{6ESmXE5!CnWh0tGJW}O9yo~c8bVGh>ZPmOE=_99uD24-9UPxJxXYkFoF*iN`#ylBd%Tgl#MfqUdn%`FKjNxU4~YZe^}E;>ri$Nt5;FEuS4ypGaK!Ext5}~BMo3g;1H*)LKf?-CX2_rXftkmQUSwAS|pT2yqLO9VY5>cAK#@h;-h2`Cd^1gTEqL#dPh|pp9`qrnZ-(viFfKes9OUXWHFf;QAAervg5ekp6iZI`Fb=ESC~<4Fl*=5`ZJ;{7%^L2<FQ=(r<<LttPp*3=%p7zuj}BpRAFC~uT04_SHfV-ar>@g9*o)bkf+arVOG0~lC3hpBQ(m}Fj~_-3WBVWSSi3|mUszfcL~rq!%5L#iIV^<g{pn<i$XwHXO~2xf^^@|DgAZLNU7JU$S}81&xl;9@rAfGETZ41we|5&EbwMjHE`}TPU#Ukttr{Hk5A<t#cOSqjy(M1F)nho1&b)A5a@{dbcEi%67pfiRZi+1EV9(CY--+`sCY_ac3={j22v3`0(>Ustp@f&Xj6r_2VH7lsgH^2ccs~fS8WV@ErX9QU(5r6-V8}<29o$_9FUZF!%c_4DlZK!x_ldaO)Fyq@868)59TLGBZTNljDYo4?UP~KbOZ2^h(a!Kc6U-!kB{YeQw-7oV{*-!68ocOTFuD)c(c1E=22eW;?1X@L>Kv3h?20q;Q9|jLzuFyvt4D!8?Fqz$Po5YDT0Y~v$kC9C`EzscpDoQ+H^HYSs)cX+eaolxML)^9V4rg;{K7&vHiwE>;$FrEd?iXhH2>nAu;bL-^i|>?U=@r@dPNgPJuN3ub?~2cv~A<nf!oEJ_|7!Z(B<V3**h#MJ-kRPhPJgEbF<#B11S&skf4&(Flo0P3W$Tqw8D(9_ziqPZULV^axvcto5^igJS}Iu)fv%$cAPa1kVZLkB%2U7}r-f`p}IJ$Pl*umsBoFPh>hKV#v4D&|4G*JpNn60n|%z-6pN|0y6>zUDS)CH99hOOJl(nFq`@Y5EW_KbFn?u;aKuD0hGXQz9k6pKw`PtOoNPnDqU95X!aRyHVHAM7*B1>2|{b*vQ%YQ!56wbShp;2;RbI|-?iz42qB)wb;9?HvVKnsrHH)tIrS;0HDr{^=rScKk`6Wt85+VfG))%dg9W>=O>uP8;xh{EBSfZJxFN?)+J`u`ilQ=+p}W%~G;Xv3hB>QY;=7I3iUMVc#v-|Rc^A9mGXha&n&-sKB3>IGoIY@kaGK`WuQtyS5HYwKFr(cCOcSv5o5rYa_%x;i^ZG1Wf<O5B-W!yT!>#dX)^ef5Ou)Ic$R7k$IHHcBLEkeg9g<|K)Mhd~Df79bNVm@dQikW0J`)8$2y6?X7M9jgB$K|eYwY)LzkdDxO_f{i%clAsfF}wZ7f`rBmdmQQufIiyzw0rp$(BHV3zK6?|AoP+Eb@$twZW;IKV3np9%^#O5cIe|I=dyJAAz|pxx8kg0Geh1g~E;&3uTVYu=<FSDy#yu6)XS7@h6oxABQckM~Fx_eircRz^k%Dd^b0l;CRdH$U%sP+-tO6n1^A8y^Y;#FAUX&jh-xJ&|&>xxpQs8596qk#%_10h&`z35iDy*iIL1$>6{1mv{E3$E|j613P0b@1eo`Ujd}IaD{vjR<K;<TmrxKIuDy5DYb8yo;yDwFRY#N;o*FpCIQvS|sY)(>ZAMg1?hAl@jW-?4b#YH5XKm5zB5@4kj;s$8G>h~O2z6ZD!^s7sX=@TNZJz(}+6qTd_qe_GDP`Tpz|^=Uv)15`+xTWZClHpH?3BIFlMxlU(JM+@^}N80j|;dEv|^2X#GSznlLN23H(IL_(mBW8jg4u}!}A0xgrKCp!MzoiFQwqKL{Fi&)zIxKo`zNEos{eG8Xrb;{!*Ol100#g#?&=SQn2};-qlWpT-?-opUCt?U!;8LUP~)s2U(rwmmsU3)jfEeY?b9gZOMmM8K`7wGfz}?c?l}}>NB#%tFY!{NnV%7{-Dxls*{&m&}f{t{FrMTl>HK`jt_@5-}1w%6Gn7cjrqxV$ekvS1llTD-hyoF<P5j>*~CrNDlsFBDJ7b<B8R6k8>~X$F7u$D`7M@?qCNUi(lM~b)Q5|=OnFjMF$#a?$+sayrt?J=lSCRY)Hz`&xIYoYdZdB3>Q9XG;+Hhov^fTJc_kZ?Gcd0Xz4U^$5Z{sYBzUTRBYR>uyFd`Qv>Co9KKKI62+rwpOBg>@{oq)hVOC&pUFs5KOc87);GqoxZZN#w-f^fsVv;bGu8FgdvKkv?^ptHvyfMgZDe`M%ouj5dJz79LcBml0B%!k@vn5e|O$b7Eqk!l6@ry*yYid({pa>BBaqBdZ;|l>U1e&aPxaeN3-e{QkcZ)#?E9*MGeJZQ169i`2JExFpN11K1{D~c|N1@i`2q3}s<d}<D|0=vcB{otDbTwil{byk#s{)LL_VSzoN8(R-O+nvSQ_v<0A<@g!+Z~aq+6t4g!K@SADQhyRSnFWVfyr&inKFtNhXdlFkN(iB1y?-<?0&9b7MY@$brMG{#w6^P-qe8*wGWYU1DMGyGBCVU09iXun?WR`sc~~IkSb)vRG!6E)0a&x>Ij*Dg|=|a=;)0-z@`l%LJ3hML2i-Vs>fA<!cub-T?irniG^(7sw<<Idi;ernJ2HNzy#j?g?0r`>{y7`ZW3N5mm6nA_{6q4q=~cbQe85}ytZE4<1RldIC4%q9<zD#OHk}WN3Fi?Ie!&YGphq?^nK2Ek-xh5`_#tNJs%;eh|UyKOHgNk%5qII4mgQZLRyge22_8u-UTD+&xSqQBI#BEdi08^1?DAedi9s~dk~~eyh9>Xg?)XFLYR#SVEcKTs2(rWy|?NF5$NyX2k+lat~;wcqgzD%W?u2AnLC(u8XNjCr|EX{(=?cNny-N%6dTTs3@0J04AG~VEs<@=nLe=$qYEu=x+!o09-&b^x2a-%iyK7cuH54{9<v^vY8>alappgssDnLray=$BJ_+|d$WVP20=SP<`3ao+!_lai2J{-BZ^@y0`;2GXZ?_5wnQ~$1PJwG}ap|ntY>c36>yfQ(Y*W;PikF@FD&p0@z_7PwEw7YrPPPlYG4$@1aUVIx=hPs^!65-Mr>=7k5*MfEZUFOwv(hqCXLH7_y4etl@XfbPX=dsg8Q_`I7R63p0ia_*tpsjUf`+m``~sS(o9yIRtTx9q>QFrM7Cb_>g(z^I)M^6YnR9AV_h@VnIk=q`lvy?%B=qrYj~<Bf`iWYygizvSiPqtgBTJRZYiDPOU+u%)Y><Xl(z6OxMAJ|W)22di4v2t=x-C-oo+lAyE1IT4lde9pHDv6J3ZSU*<}(P!o=2ZL$3ZYh>nl0I_QU?pL;Kb!eLnSrU*QV_^f~cP0r3{P3_qr)V{I<&HT7d6Bc1KSK#%mXJ&j&aujFyKnUDe5Lg~-81)ci2ImhgCjJ+Cpo;(brm42~1xQCUckR+LgdyEcr`|5AU>aYLNysWABE1#f}gIA>1jK*AU8K9%ybx|+6xsj0dzAVGd_Q)TQNrYs1MF#iSkB^0E>yt8c_I*W4)XaK2jQfcABOZG0O{bw(4w26DvhIG1>}eQsVqG9qgRi4o6~uNtV2(_~=%;ZK9iZ^~(>zdHozpZ-uW>jy1&N-VNCXfJc6PmTCdKaPL}V%$qXaA%e>;iISFQFG>bb8jDO1yss9k>6?!7|djGrX+=kU^}{cP&s#{3D_VU^l);5-mcgB#~%ngz7boDM7|DLf}A3%=Gq;{vdv->{fOJ8Z{{d%q-0oN6kTW_4`TXsi^5gE0bPTSe#}BP-XA6huZnSa3OZV6=(UGztG^BrX%w4P!5+=EGuh-GuNS3=R1g<xsgo;*GT%Jie(y5k$JvWloyaQek(LNlLiYb77)Su4)-6$73o(5d%nyw9(^2pK*a)(GSkCeUhqdOnXR3da@n#6_VtxOj5oc!lOfqjN^h;3Hc*1lkN#UrYCq+Da|DSwd|vRQs6#h*z6xLzXsWwnsn}2R}U}!5+YabxJS1;4edZeMf|hBAE~o`z@C+&)n!VP+qTA9e&G_=VT`CPozM}T+uAp^7F#m$a>;6+rlkR{ykC+$UlfVMk2$!T8oyZ6+QLwyWo>qWr4pCFdR%U-H*IY!8XmLyy5YyDEp?~V%;wt*8d;Lk9dyYh>lbBkF?S8szEvhqsPiOnqE?xUY3^+)b0o}@Z!^dh*d!DQwqkH)krgqKw!c~>Yb(YY?9CWop@wW}G&8Q5Cyo|kiSv|8TX3Os@V*Cuka${xswVr^Qm;CLna=~SfkGA$F+u7oX>J?c)d6@PD!%~S@$xu`-qS5Rw3doEmx1vPBUZT+PyH}jSd=v=<j_Dkm$*>tkx;nXC5nYx5s?Wm{DXdPAvYBoYK)mD)>$7S>a)gT_x1i1+G_FPP=Jkkd({7zey4jV3iUPTP|)nV?Bzu8GzfT+mwg!;4+o>;f8pI(Sk-Web7_75sgP!?6`&+C%#k$I`QQmPt9{VZ3uLQo?eA2ToI#)ZU=(7A;llg5=A3Gd(2)gEYH+k&{3r3RN(Hz;xe6la6tc0@z<Yv;eDS_YgI_Dyl0Kqs^>GKsz!FAdk=InIbyUbMM77AD8T~I~&9dNcz>$}J2=K@OI`!}mEDmMjL}0O^Cwldj&ZRHK1bg!WS8dbj9D@@|KPffeJI(oV3^jBx!Nhv0+~AS80!^AUmo1V?2`4ZlM4f;EG1YbvY|zp3-mP)qw~mgbH5Ki%mIZ*gl@up$nCj%)9*YTc2P;zGX;eKZCDMWM6OZ)pWL8BP0Guw-!%s9ryEZP~bbyy-e;u*Ty5z1-LQaA0m!r6b{0?Pq)8J=aeUp{%npVcNI`FcN6!mit=Cr9aylM}OCt8<3N)`c;kTT2RnI&$wwyRa>D0o;KzeCdmQFgCxUBXD?3>CO(BJ%{6?9i9t$Jw)#3idXEjVT5&Ad%L!yNKOBn;{j^v}s`6ZG2u_Ga1HTA(cn1kpf$ieO0D*AtU-}`#W!wDRXVY!?gdXBLA@)g+bzQHSSNOR|;`G#A}K(w^(Y^YMvO1x~jr~6g^>6?cL-tv3*f9n`WE1VYwGS^W0EhsLzyT^wnT#;0<Zl?7mbY{$9h$R`s&1rhkQ(4FTLaR#lF>wazz=sL*fgpMf;zQa|r4&JjUe(dZ8tfSH<ZIK2e5oo~HgAjhZ$gyfcG@<~u?E`;#tpjj;_>FY&RyzhQB=zJS}4MyLOA-aqbcas&c6xY~iWsoXd1gsGrq+psWWBu?({;`t3fBXJ$?aVM$x&N9%3Ka_BGCw)nB0M0A{n|x64Dwy&Xr4GKaGeXuJlcv$#M^bm!qf#N?G^j|5rMd{qW-WVi80(EM0K^bw$5V5y6|>$4`0%JR=S(NiCjVN&1Y4B2}JoGr-YeLu*;FixQIXu)jiC`s#^1jmeq_53Egr?>GMah^5*)wtZ5Fdf?@O&#`%s+0~vwnU71UL;5jdaWKp#Oql*_wjFoV2S?xEq?(k*k3?GA4Bv2oaCV)J74KU(4@s=H5R)aQ81zibF_WiB(nqQK)AO{Z~%mKf;0x*7~C(5m1ttPpu;DV0-0+N=Arn@H^0wN7h+poSd_Bm~`JL96BYs<T0)b1c1cdeRq3&H39=8MfyaR>097-S|`xt7%mjIGcyZ1H{-KT<qt8IOz9ic<&<zfZ%l22xZZPJhZPgg!m=as+?Lwt1h+&{}L@Hz%QBo&oSNybN#^PZhW?RR+Hz!;Qy|zDCo(Un=_c@EX*spInznf+ZH9H@UU8p8@gpwkiWt!KEyr`hdp5dVPj2blLpvn9$-*h!Ux-u*wjxbM)-yes$#}5|NTGV@oH*l1}kWx8();6eyN!1|Wsypn&cB=nGZE7L7iH%u#GZD6EQnv_{1T*-_Axs<Ug{Y$g^}G^Y;I(7Wd**Z)->9oe~n!B5yH(}Kz+dN>TWGCe)?Oga(yITjk_lWpf=Y&>pEFwnTRQjBS4&0tECokMq9YjGMPhnHZ;lEkWqxk+`;2MT>WK-?$ZyOzFda`KN3s`W(}v-cyjNL?3z%|jyF!U{vut&MFVMn(CnHcd%Ia)5=ESO^%fro#mW3_hp6Po!34W5KyiIL-IUNOTG)ubQNEBwgxzZqyXkPdz2Zc`F1X8G{5JauA0VF31DI_)d25!n1^V($gmuCh3CK9w*yg#(!gs6cPp`)Fjm-ZZ-n<Yryj?ziM-)#zV%=ilSxUYl_ntT#AHQp~;qHmf(J^fk~~5ZZJB@U`>De{o6mU{~+`I{_WSV-@koy(45Dmp)Dxm`0-k3qowIZ;Pc0noI>g80qr{{d8;76>6o^9_zU1EY%5p)8u$@YV1p&d6@{4qTak1i0tFvykl+6P_Xl_#R~3i#$@?-+5`8xk1F)c{AbF#r+{%e0)mI{zxe~bNX=oy;*SReLhVUqkvIM*do%<vS%y2?nL7HUtiGDV2R%!NnJEp~ZiqEr9I;l7((zWp#)hT_Zpr(Sjg6E7@LEJts|4b`K=Iyx&A`$|~7k3udi&hk3Zk<j(GDsla!j%5$`yCDV>0?01>5s`TU87<QB~a<*q0fBnY!v^{iK*M|2Hxs^t(WNfo2NH+{qaX>z`ksQ-6bp0muXIP<JN2}(3J@^bqXKf4y;PwlH6NHd##SkuBy7aTk=YV@3h|rx!fMQH5P;V<&++P$GdVzXy46Dimw#FsVj4gx^7z(BN1>K4jj*!VN<P19#`_wzL#r);v&*7YH<JtjCvf|m7mB%E3dL+mXc8*qFu`QqCJ}^2JXVdr&|Uu>}@+}SF37hYmxB;n!}!V!=Y`M;Ex}_&u|-BT86=vf;&9-BTPHK7|arEn+UE<N9}<#Q@EsGGV4+VoCnKin=%ne0SG|6Awmx#@6Q%>BaRK8KXG>=@3&?}UG}{OHuhCqY`rL_8)cis|4GRk%HgkB6|)#`2wa%u)@2y_f~85bZKC}ki6yJoesL<`GTNK&*aVB#e8?}LY3E!J{jpn_2f)=(_03oCzRdtmo#FSXb~l$L$WkqAGwTq{AwyBlBs+fK7GH|WrhOnvdP9k&v(}OjDT5cia9KX|EQ@Pw;*nTw<NJzGC}WWoQ{qCRBI4jE*Js-6&vlJcai|@+c`JOX!uM}mFV4l=FW-K{K11;{hz?Y5?!N4)QseqWg&;|pMJ;_E;*HcB;l)kXZW!xcF6VO#4=p9y4O!w;FH&vD4QpQu57*n`WX)2D)PLj-tnG5h_33z~#};?2&lR7miH=|ghQQ_c<Fn^KKeihM(sdog)3o_+oRVF)dfGb3ODnnvSvTEu`R)TZWR5yBN%~OnRGAJ|<$A!B@0q&%<?C-hopHt2-+un}>krfTc9-eRb3J4^^Rf7Uern*NkQZ0?4ZHfu-6Uaz|N7U@zx?z+e|*FDe^u^4J%IDX)_-<v^)(EuLY8hC-J9d%dZ<4dzkk_=0O!6*arfhe*td;xFwP&<i&Xr?KWGZoW%|>EQuFYbeEf+V)nQ%pXsbXewlGO6vOr@yMxr(_)KOKqrpS+9GHx`P+!f7oppl_XNeZZfF0|lt{XJfM{lJDgLbk`~Ae8y*@-cheL%e_A=2m%`tRDW>VvOs2i~jo`Z*TwnSd8VCa}Io>QI?oQ(Sd!iom)fWwVsSqXW+Ygw-X}pPHGlQsOAN}d1&ic`0-uBBU0Q?V~As0YtBcyEP9^P<rnBfbnnZ^Bl|+HwPkWUmnr?S_cN(=htq|($4F<Wnn3D7&^j`FIrx(Z1(hQo<h`{huQZ^nzUxJt3odOYekhq<1xMhzqWcNUl|(0_zCT!gMLDzAem(mjH+zs2?2Rk+3NIxpDe1~qBxaj|`goc35xLc(9^2YAEF#;<VC_PAVX&Hg%W66&!jePk*1?v^s5^(ATWPh0dF4iqElw<}G3BR#@1#7u>*ThhKyBERjV0>qyLI*#P9?<SzI~zr8{OH(4g7$xu+gWl%!q&`S{s635DD?1E*4EePt>}#uL>iC$i{PclZws{mRfWTu-hWwWR&}Ox)=2FW92O27x#Y^dR&CDo1q9~X~+y2VGJ*4j10KwS^%DzIw~`}(6jet|8gVOSI1xIQp>$=`?q6%f6v(TR%9l)g|rHgB45|^QIC>GA<jNaT*E}!w}lEjjZQpdhMPiFD4jSNjw!4*VY={y-xn$83tPcNwO{90Rf!uVG3VAX(7EVuH@BZXHF8gx!_KnoE7ae*7qzG_++<pY`<&_qa65ag!Y?$Bn1rizn8TuPu<T#-Tn5)@rROXvf?^rk+~SXE3#W{Ae=?bc-^V(AlD+FhL9XvXU&!aP{_3?5n?oJZDz@<|F2Y1v(?M%&N)f3qWbbRE6Qpq3+vP3Wxey+UEoEvp<icBSKi>te*JAXnIu?W*q$!n*<NHn}U+Qq{Zf&w`(S#$RzEc^QY{zyChJfR(^+)?-3v;=f`&&qmZ0dmo7EMM)h=eiN>n2eF*T3xxx+EIb_z4lWKhW_Q=$vTl^tyn&?_>%DM&2OSvCBzQwHR^H1WxQYfm`4CQIA&`nQu>;Vuqd8ys2@s)G%<GX?8>Bv-@80?xZ4+-KU95_rE10r9x@k&NT<&`rRVBKb?c^d&TRs%A-IhBU`tEuj(L%M};_0lgP+1FMV%dnxk!+tnFfpBtcv!)k~@Erv+MR{i~GC?fcnp(8eWvd1-3U7h+`z@s(VVJk#IzOQM9H>J|fQi3+z|7rju!E<J2|y{FU<9i@~8+@qY16gg3^f)!%`{zyzuejiz(a}D0lgxCy=io>$z#AP~kwpI+q8bNs#D4~i1wnA|l9vrq3@?EEkmW*`^foO7&!uUiSEK1RJnt(ulQZSp*HURq^C5<*V3)%IWQBFOQLlgyq(ae7Ln>rSjY9r5e5jmpxLQk0vG7~<d_t;rF8aHcYWD=t@Lf;+&HZJM)gZ81y=jOEamI&Ulzw!2$r_+lte(cg+O<2sL|Bp^-A5)*Ftmg*x1iXMnH;<7I&yelie=$;dz>)69(Qak?%+QdQsi_RMk8^5MvEU&^0`Fy#F<`iJqL>|f1~@Sh{Tp@QEdmQL%Ejf1s|JG1odzxL=(`BUx#q{2Er()x_7>=3-0TNW$dK?J00LLqE2n3$5tsmT{QmnaiaOZ(Q{e*+zMD$5qCY@C3tQa}b}jAxas2_4Po2?@vKk0)bc+6hfM!Z_&X`Wuhe$@Jkc_Ff0eb}M^35jB0qb*VOnH7{#(B=5<nVJ4%Wp6K;aZmK`s8BZkZ>AX`lp8?+?QXgi-gg!ku_MwTAK>h{glzTd>`uHzJ2>ACivsCU!~$d)&rH@iE=B*rw?xB+1@qEbq)(^A42Rpo(_{#^}{_GC~0jbY|PxpvrktN2bxx&x=M;dfVMyZOeuPwnjlLJK5|>hR29R%-hNQO7MqyreJ&nDsxuJJYQDKL10df3j1P6H`<Np|NUw`!PoQ(vZ%LtnwJpKINBsrrLq8AsqKLMCBnxqa(vIrQT#q#$6BG*MkfFqDzQrya<3y;Uy>ftNzYGgG+752=3WQ3P#J$Vf>{FT(X$8e4l@wEo7Xj}VIE+zBX|`i>4rl-x@S|_(%`c@9vX6hY83pyF&y>YchWr)e@InaV`nJ!CB`%8+MJA>AJD=4e`Y>MJ{Mq1@OUaEyGB}u=+rp_1F4?h>7P)lKRE$4$qGA9vWui-O&%i$8%7S^1j3+Ai`(^Mg4Zy~^gCmVr3Z`oh%{W{>%AV;?!+P%o>*VPQ?4zFij@Rl*4REq3Y<5bjT_j+cZE_};o(H3=Yb)Hw5%%bprncioaH57x{*>;;KJL}m`L8amL|nou+j&EF8v`)T_vWh!fIE%RChf@Bu0|;gtdKF`p0niAQvE&p{vZo=7?5jcw+5+)Nr5gfGIh9PeIz%~Uwha8r<?~(J*n?Jm#$(@W$;_mNb(&XGBF;b%Rs;Sj3{VDHF}qO(;CG=`b0Y%sNQ#so4sguL!XGmvL>3rvc<jIjY%9JE*!1j=GE)>+VtyQBiDVz>%W^Mv~Eca=SdMiX#2D97iqmLhT)F<@3z_1jEZCo`<8O9i91}5*$=nYMu;BK*3)UlSL|?8`2@SmkXe#R7=#oec^__3z6nf_<G&XpTV8wKhHhv%Z%@+P^6>6H*ij6&_6ccQMC4i}q*8}2BYp#h1ilLun?*DtFrc}ycmTPZwC2bT9pbSz30wN;3*C8H1wM4ETPH?4+Gd+L$IG?3wPLi;33hcdWc*Awa_EiF&s5*#aT89Qnl)(lY`O;0zK`3mpd$;*e`reWL+@=bgk?Wylgls;sm-?^?39QoZviPDuLMpfH3p{96<EmFT%=oUxbpSvDrC<We3&tr-IPZTY={GIuff!@Pw$);<MIwCdXH*uM^yJa6qTMtzX+K&EsH|=L{%v@6vds58bypRp6{P*tm0<t6(vadR&-^pYEjAQnICPLNZQKD8cuvfiUQ7@l9q+B*T9gma{Vjpksb<^W{O!(MjOZNSW!h);<P;N8`;1tzcvH6VHoY<vzwYVN38!5I=#cxpckBk&_YxI3}?oXd?eNL>2TRF$RLVq4#KdViB7sDRuH||tWLwMQ}I4))m5N!FU3nr2~eUwN|9uugVqFeBE$mv%edO-x-LWUpH+9fw5$9+wee=dG^rqt_P?t5^&dMRkvcjVMfCv*0ou}p?m<WhsxPCWboE>;?`@20hd>)b2*1=h|F2=2w&Sz*kq-)6Cd>9PED+-*%Gqd`PG&J2vlwlmD~PVS8>1VI0Na=>+dvnG(T+zzSg0{x?17GRW1@jYWeg*rsw1@x@1snBl@v?8^G55>+bUUU8_@)yPeym5jt1V0Ha+_wx0L0oE_!MCr*L4?t<g?Jk8w_)KqoZE_8N3KDrxBf){2rvvWzOQ&V3$tr}3TNLo*jTPeaO56DbTB?8PLI>XX5uj*Z3(0w?Ny8JsjQI#oM@?@H2}#xHXNAf$b;X4lOnZC9u@lV-HltLI=7(_*Whu`V;ToG?Zw!NyAkAN3yk<TRA?x2ZhCwAoZ1@ReK!JUfSabY&@GmSOOt>;3p*XkzZ%0JoA};)EPtx$-7ry{(G%h5(gVQblw?FnO30O(FnCsZ!R8WA!Qb!`3CdMnLoMRLeiGqjg2-<>*uZ1y@koM>#f(5-5rQ(iV}~ti3)kvPnK5A3lW`onn$nS0hYDfN{?m;iQL`;c+$zFNh_UtaV;&4;Xk5IGi9YwOp@`z1X6peke*J;TA;eZB@&Vo?Z1nh?r3@{LQaGxjS@~oYg~_fG7&8?P<9+Bp!?1cyo;f3Y<7Boqeobq7;LoCFGKpsFn+xUy=fcu`Im?+8)>Tr=R~G-^GrB6W*B{8!Us(rbmbHaXN&8-fs1T18JoRi|RvRRxRRqMw4d?P+BI<gMud$d<k#{&VT&$`?r5m+3;@k7x_!6ureL%KKu1A=rkM0Ky(ENFB&NwOFj6S^4IFf#DE$Y^qMq|7E9)NAxD^fAM9q|DPVyi3`vyZVmopl`SoVYHh3ih^`Wa_^_KpA<+wXYReUVcT!VS2zF75XvxN^3Cd(YjVz_j|y??22-lCSx5>yq+bIB=e4eQW?**H`tj6&)%t@=!_oIV<(HT}!bngX^d>Hry*B;{gFonMYy6w=?)ZM-$ZHmBjtwt(kH4qsH35$X+B?|c8CSkN+uejU)wn#pI%1T>C}8FkQbDAuPMU};ffbp->EMMEP+`68EyG+nMl+o`sd-qb_g60NE%Y#nz4|1fmiwl1;GR)b~Y8izjMn~J`-#LHT{U<6D|xe$Jn(_tI@f*0<5`5XeCqn8P~T)oCN+8WvkTJaTOz@Y7e_X^`pE3>yxVzT9qIFFpxF_;C%Y*PwiEZvw{dfj8_dyq_P^bpigvR{@~+P3SFZc2#H5-y>F^cfP08{&b8;>d7qtEh31BNP1qz+@kf6g)|+g1o#h&WUWI5aLco<Q2)$x*bj87;m>+i(Nw9DUhi(yeSAuN&p4Q0sTU7)A82Xm;u9WnO0R}^TO6R{C(QvW7he7%JVVh{$)o<oN@$2sTN{J<;x#$?kytrU;pdz2HCcmJ_zG&5GRsXHq`3Kk0M*WK)-0oU-q&rR>5C3vN&VvE+AOiku6c=xLWX>iVqRa{ZnRRERA0?M9RyN?w!(zjtVaATCArRW?z9>tborr!q<aMT_WAmKkZ_9T!_V82&iZN0P$>TA@Sti19H-<7GeFXyS85u#qriu>BK-pilO;^-eYui4pw{(em;eh@74rR!FWBO{zc}AU1i0vTZiE}kBNrw_>IYA^it*UwF}+aQe8ccQApzRv$)<0!f?l;zT9We*0(Y#EVtuiBHkzNv_C%i_iy!&zkmDn>-TS#H&Ap+xc>CVi7tQh{kq+jiVeE0GrMm0rSG0m_M@calSiO7@BBr!-UldlGv@T9OxeQ=_8G6p@SISY$TkV&GJa=lHdFs>T52px^Fg4<1aZg_cN>i<s_j^m>(?P0!MHylJjn7j6yvGbJ~<xSvA*+bRVPRv$gD`2VmXb2(G?44Wc)5YbPp_DF);46g&{8zdZb*ne(@;Ou@7>~3%Q_ts9!>P^&$jxABz!>MI}CwcfpHGEcZ^Nn~1{(#@Kz<v1_nrWn(QwR!-#}N52!tUA62L72T0@%23W6>1G@U_pH$8$F3vw3xJLApeX6Lbh%g)XJ=FfOlz<G^jaA&Dh0}_2p}L$3glU=upE<{6H<&BSrM)>DpO3NrSm@c#XS}9u4m;b^wQ1dXd*e3t>bB%LRx?v9G;-1iW%ybrk6vsG23e&AI9xroeB6X!wYM=*_G4v3*HF+hL1>CTj1Vbg;IeP;K(P@6K{-l{j&7ou@EpIK~PM1vY$F5%LTZ#LA_R-=N}8P19?tBWpy|}aOmq8m0~8|gHnI<<&ImAsg6%;XgmE<sqLlI=8L<yR8y$2DPE4ASHic{_1@ts#SB0K`r|bJM<Y|EszRdB-G!%EGQ_O<wkwW4!~h}^7x?*5W2^Cctxr|O!{TqIR9KCZ6)^fi-9DMEWimDD<#hl6_i7kd&$ouU_nQ32$g?>vjWg!1u_8V};$uqFW?AGu*gns~ObjpPlrlycvtPd?Xe^{1%(CHBU9~8TY7pi*2S4TthDolAQ}vQXPJu2Ouq?k97vk;uWr*|$7=VeR1Q7_`)nF}bk16c_EvrCq+}jCF2s^QEN~Be$9>Q<T-8-_t&nQ9MDQ<{lH<}C1vq#vkb@dAkG`?d43&Fu%GL0`khI6KJ>B&rK@g)n)4{KVw)`Do@L#PrUKq(}JKfY$~xFpJML@tQ~Gl~glT%pV0*UkH;4q?O~$72c6GJ85!eazVo_aA(UGHLUmae!m&{)<bRTexNSaW$uVKNdO=ppqnRb;@e}9Yr9=sF!33JsEDj%#A>QLF6@D<b5*N7k0m_A=d}Yv(I%cYj5x1Fo6#5XW3k0Y{4@6B4#_|Uv&f!Yb#oBufTn}&%%9H1y>76zc~Z^#Gmj2rt32zhokH+9g!m`<iSN#DB;4KeiaR0_I7wmyQFr|qO1w+Se8(S1gB^8rw|tx2Z|=P;0Jkrf*Ry;oy56{k&y(>LU=4f&aoiHupn&?;nIDov&a>3v1LG_gR8-D8LyS6>zNeF5-L-~Wr?t?kEJ>9P?tgrToYkju;u_;<}Pb09a~<2U=CZVGY|tR;`3&T^2V1O3oGh`P#+wpBT-ZcS$L`@3f$mb<Y+SigIjs7X1#-(0>jBYSVt@Hph+GXmz&9TA{aMS=_=G$YubdWfU%)FqKFpk5xWDoOzCQxNG0SL$ir5IQo!VLWu*~Ni`YqTq2LNC<#BuIy6KM71gExJQS0@oOVq`=!KTc%+$?L-cvk`?_lEvkaY((7T`68T$|-CO73&S47DXdUFz8h=DB|uRH2qT(U~UBJ;$RXg5%h44jyL@sH|aT;sieT-tS&R4-3Y}&s$HCJvSANxDAz*UZ-8uM>xoH9Vt`Y@B|PqNKUuRGFF!?v*EZHvE3O4J6_OaJybc|vQ9Y-rM${Io326zW(8cMd`o*fzJ^nvK>x_TcCrtL#IA^DDb*HC8QX=vhOsv8(ZLDmc?`*rcRtZ=d{0d$2sJ5`2z~Zu3qY@J$RGC#igd5zUJ92HKr?Qr7B8QU^vlDp3bTd>VQ<dpYX{zV6sjGwkC8*$-x?9Hg&Xn2nBwJFaW*=<l9%T2+si=-hX{9i@sk15QtfvN?VJ6SUgeDC6mx((GT_YtubDE=wB%F_I<mLvf=b>q3qnmB|cw5Y*GT1)k$<B*KmIc655&N*`G$+sY?$Rv6_!MyODcVyFyO(G>g6+ux^sM&GIyFJ^ANw|k8X4v1w31u<WAoNb|0>ls1?@Bnlj5$px!V!IT2r^#5D^T|%hv!}A>e<|>ag1M`kO6vh@&2o)X7ttu4fa(IPvi>bcE{TPkLmf6q{M~8c&@iC)77;i*lZ%UGseY=)3@6EnjX<2`y`gC(P2?nT!ctjANQEWXH8Kr+!SN%vl+VNVtMK;G9X&<JR6Sr5(d5>SSb+qi}aBh?BFKo3r5c)ge7R^0x5oCA<IjiP#c~VF51s1qEd3B0~a4)wP}5eC*5m9Hp$r8$W?rHualbx`iHgvxKl2B#UX}OQh4*NG_X(n;lC$7zn}?sWu1Ya0zfNW))9EXWwb02C3e;sC5h_lg08B(~x`pY0Q|y*q>+;VKxFn|8eZjkkiZpQKwL5YVKLR4{-DoafyD4aw}M!Ni@_9XAki>2w931#L5P!(=fZPI%|R9NMWe=x-<|l)^_e(i_++umg}+*g<<s-te!Pf;&FQomLG3|?YIfHg!R&tj7?aK`+B%8rqp(0VnH=-_GDu}=>3_*uqi14$A$kB6&A$ZXI0C=F&O(q2ULFKsCpU6F&OId=b8@*n+F;)kAW`6_xLkk-Qcct%XCa&w7JtPT~8_DK44?kn+?a{r)G<<wQ-sRv~k>}a!xQ)L7|C4w~a|ueH0z-kvp&(Nn_P?N_8upd!$6$kZ?~NiMvu|qy$f=Eu|3Ko%AiW<qN?vDv4nBE0z;ryA$0au6@anRC&Cmcu}1|>W+(ck}~ZOd>m2~9iEubR3<|R?2ANMj-Y+&o>QQDf{*q5w16_$Sy(<zPimxJ!qDk8VA0ehj1I0=i4f(AHHMNtwYsy@u+XGx+nC0l0Lo~nZvBPd3K7q8sJ2+K=#X4NysdU?R<>kUEi-NH$5iIF4jgP^q@<0J$Ta{nEe+^nmCEAG6F)maK$w`n7{9#J+QRgsC3i01AQUOCIY0vRhn+fj{(suqm_s~7R`Rr!T>y8>2{zfx=36t7kZml(>8u*e44O1|4Ry;^(oZNF`8^d|B|4_Lx0TRQH9)?b6EZ*rr%}4bJh-aPin#fRGGVZQ<`gU{ZG+6+G>@;4e`e7fcvX4vkfA&Wc52F{GCXKTkpaYe6_j={^6<zn?pZkx4BI|$1`S}cSP>>1oz~s8fEzc>tMBnXdVYJjQ{W*YwbMi~?73-csReWy7;i>m)rtxB1mUekFiIgm2O`)OozXCBm8(K`&lJi?7Xo#RDA>eFF&jQmZZXsHVZnK!T^FAi1#hX>Ob~BTb$WhI^dc+-?wm7)CnXS8=8v!%f{0C2h~4?;O4K-#zG6&xlNDc<TQWtOiBq9_$1C`nwAV!{^fdxu?-sThIN!sOo1SQ}n--k+*HKc$IyNcMX@*K6ei9?B6x0jUz#vjiAuCHgz9-1f7w@Y~?3~qEYFMyP>U*ST1bSpDzz8l&hLAxJ@UoZExu86*S_L`Mz~UjWRHw7)6RWQ@FWn}lj{GULmz9biv>6Ht=TwooxD`ih!%4`3dEvc4PB^qGuZA=n=#bDf0w$1LY8Kw`@`+sAyJ;OAD{4|CU~UUweIXB9Mhs+PlW$qH(k-=dk(^MYfP)qr8^Z?E$2!dR9Va4lzc=8u<@*+16&|>9@nH8|7KL)_;#hSZ-?HbF5UVUeJevhM`qWSB>RWOK+KMjBe33T=V+%b$KqF8sc=4R-ic86hFvJ5~aA>==-J3#%!b88%Q<jM0A7*uSus^2NC2XxsFYO-|TqTi})!{gc8aYGo3!hx?3KGd@+3S)>8f84J6}7>A<U`8WYt+`b+fcdCJM{3Q1BNKH`>4$^CqY0h4_zxNmL9#Ep+!*$yb$XXR~|eo`;V%sQeZz;6`-{}4Ktk$!K)~_3Y|qXK~J<4yws`E$8E9OV%hmLd6Afc+N{{nrm$#vKt{5>8=a|B3O*i)`H*uGK-hW^tT)vpfHCqs-ku<pnwwOykuNixVyJJvapXdqME4A;H{Uv+8;zhf*7cC%c}BvBSxVL3zUm#BT9X*r>yMS{{Zcrpk7nu63dW=kCs(#sY__F=4F0rP^hG+Sy`J_LnGxLA(U)5F9WNqzDN(zqww7>V_o+;oUU<|t8v#Y$$I>D5R$CW`0dpaBSUDW<p|G(LUgO2+z2W{W_Os1onUYQZVm1^Q;p(?76VW_tvgY^oYohWv$3L>I^IDK#2N9WjaCv3pLPs?O(Q2yiAOYGW4pMjXx1EX_CVIj#tU+}6Gj(9ADhsv(U5>uSB?{xtvoILaZQNYgXYLd-0tS*l$W1+I+hFmnS35VfN~y8a3J?XZw}uaE19CTae%B<4-Vk~(@K%|%>P|z`F@D1fA;NFeodnw=1QH@7Ztmv9Q+Iqv4LCJb!zHrEGPANnA2)SOmgEJ;fsqHxz<fPU3Riz4Uo-$3s0CP6AVcSN0e;Jz*xeH|VF0I>LEA!Y<GB!EL^StBJ?ZtKYNGt7n3>@L?Qgz#UaVz-{}U_lk|rN57kS@3?My4mq<GFU{#XOjRX0H1BDZ=t)<h~)#A#Z2=WxWCs6c{0)O5@f!t00D(g&eD2XIT#dCBj?`Y`<Qbrr?)OSpz}Ke_omiIrGr<diElUSEMKBF141`Op2_Ajk)NJlZ49?1jKF+-RDt>BHPFzJSx4!K*f#0RmUr=x&;v>OR9&DGxIzqLp<<ry2sUZX#+fWFm>!hsfzN4IDc166PYucAx?Q2pcZ6A8lz6o)tt#FeWKUA3@iwoYU!)3v7z<0c<hzz;VGP;!zE~dxmmNdF3&ZjVKtJ<<9clromSBr|u0)IU$e7f~XinY#zo&6;Gys=yg%?Iog_jbWkqmLQ|3v3Ea+Syr#{<n0!N;n?wbDh|mWK1Tzrk0xjTU6JdW+(9$HWP|Ky&)v?8b<CMt8cut=QYZ9$9ReHp>VzbrE&}k-R8A=3$vi6L5y^mkYU8>hGcZzr&#@*;rWnUCY^-GfkDaySa+(I<ovf|r96q8Y07*q%OzE>>py^a>0aF5X@#myzkD<w7Qja2)0bbo2D7H6VS>&Az@^A$GL18g@u;dphT2|#C5RaYB0HJ(IvocwOeLESlz-Q+?HetG%14zon-D-lwvW9#Tj3j%*oQa+E8*5M&~MgLZf3L;jzhum_lyz&%IH&>_2ujM5yIR5*hodAvJr|!unoh+o{HI!27ZJs1FZlL&pVpCDjQTeVJs$Oen=4oi6$Jc})0Vt3#O5MNl6;miUGKP<OMK~Lz5q<cvT_)vyo>J7mM(LD?MoT}uo`;)*wx|QPK69ZI(Jaap9HK!^+>K-|R2PZ3iBPn(DmqxLVI@jvHtM<@1YTn~Pisaj*UKa@iFi+9Q1BZ{``>)!d#4>eE&{jcCDgxj<Pi-ThC*8tN@MPOTCjX(A$4?&fVUx3T`lU;(CGD?dqd+|tC~|TC+u_;%dJC2er6j(L&>Hqu`mAhmQYNe3(Z1k#FE%cQ&gO#Uft%v929a3f>(~wvC_5D>jLAMeZ>`vVGF&@5F-NvQeE{xij8}??o$}A(JF@Yu7Uq0*KnGlG33{t453i6R7?6X@kl8>MbUJAw_lr^1S(_mqC|FTzaEtc2644=*UI}?YXfa{CEm6@qD|)od^<zkrE8Rjqugk{i!m@@beV%l;pK;ynN}3SZa!u&i@jK}b`-zQZmUO&5Z>SD!TW%=zd%(1w}f(EkkMX{!&RvYz3*?WUHR&TG+T~-u<rPcv}CB-1hE0(JCPVKUphFc(_+uD&NkJAr|r+d{@1^L{^h6t`P;YsQK@GGm9~ETXZ?6B>OCdv=r;~~%R5!*SK0A8mV32JuUVQyyYhMF{*uz6;k2)?dyvSQ)|UG|w$+I5cpGW6+$P}y)h1gtG1v#6AS|mx=5~_cwH?BC_hI+Bm|B2Kz-0v~bu;a{k8pt8{1csNFb>KHe$3zf_@>K)P@_5Y20q-s)vrr3{2e2X@X89oYD@O8pddOD(b!<E3YHVnLVg=~#kci5ph|sS&}>u*L8j83-b9Ic11EfKX?la_A$xCdG6}gl{n@NGoe!Q6#4%tLD$psjyvR(FtUtvqVV8{R%K~5)=#p#9o<t!82Yh{xxTYuxb+~Ii)&4xXmnpHHrg!~rcQ*FD-7v|%<t9Y;-!VrNQiJD~l3v*HifRS?DGx2Z*aOV^$CQ5*o*Z8c4w`6^_1vMWBzyK*jy^{nGO^yjc|^KY_#c-)3|1n2F0Vk;TF!RcjwgManmSc}K%o_Br2fbG%kZO~Je&lIdVf(CCdu%)D37-8mjlV3k<EQ2PX~C2q<M#@%f42D&}^$;1S^=AZ%%v@hhrpuTw`EupT%ZxC-V+mF9OUfPy=5|`8Af8@t%Jd!!K@GFtjcsY>`)2_iA(40Q(FMBdCR9SWcD>jBxN-0i3N2K@O_p3+E1oIQmH;x2%e}E#WVLp-rvIDmoTpLMwq3xs;aNq08kaxudpo$UQ3Xr{_}}F6z<{WzbMQT6nhQ_sAO8Cg|ifcn=$1^(c?WW@kcAx3!q>IQU|A$AG(=TiecXb#{JE8$ADEt!&+fK;_K>AATvswDw{6tT`NRFzp{mQF#AeGS>;jCKI23jnaJxj>c}>(q+O`-sz=ISR@+46!y~)yIq5s@85p?`u$t=%a3-yt(Us%w_m>fh9f{Hk9{)JX#}#bc_v<_X;?(Z_nT&$s;!xb*;w{+HUGkOAD>!xR)fWyevV!LUtjYS{kwi3<g;BSl8#{|DecGiF`!IvRsJ{aij<fu+(nG1sy#UWguamOq4+<v{0qstzJG+*C-PA>q56mrC0E@g>%G6riWX;2{tfq6YFF0whMo1rMSdsxFIID_NL0cj{y~oa<MWq4Ke`*mLx}n_KB1b`jf(T^7S=@+J*`X|yTILa)5^3DdCpmKVH6Ql=Q>BF4gCS)mW_#i`TE;WC)WG*x1WFg`om<t-KE0*xgJuf_gMTtKQ*}C!4(z5is7900ZD)PoiO*uH+=tB%$lkXV*O_*=hoM7L^qA@UGZ`1>yHL^EI>uf;)iaM4Tq0sdfzr$jC}s6UZmnD{y|erMAp%j6qG-_6e9ZvN^iS)Y~T|rAi!hopGq<NNYn;04KB+5iH_WENRLl#Ps`c5qFe+T8QK)qtPrV0)?9q>x&9t6KJ%bK1k)zOAH!Lhu;nWs;{E$nmMcT{)^9D&JDzXRfB)m{?VlfuA&WP__j^C0Q=q>e@g=*Zb9LUl-Z3!=9ej81iXE^H7j<R31mC-&`odNx`1mg25hYZeqai8|s2W1>Jg4==(1&o8n|WkZ1+rTdpH%Vp&qMHjCUrAVC%1rZyk&+FFA+OK>lnUl@zO_m5;^ig-di$XhA0cC`uVxw(q_E8a#bzyg>T4e6Ca|J!HQ8rnGwqeIS2U^JHt_#EWDH`U*D~_rdHqe@uG@Ue)T?UMpbxhYuB)dY$t=Y3kxa1YW6Lw*;)?`zJIW_-YbmrV=I}Ijvd2gHgarnVrvDM+RMhLfbXO{ysKU44q#$wWAW($+dcaWr?64*y->|D(-yW{7dP+&%|zdH^LWXq>DHE_IuHr*pf1%*wp+LMRbfow;+Nb_Dp>ed%h#F%Yq#|!quj^SwZqk{C$0YC{;xuhi!gRG+F4jSZ$n0ZU#J`t1Ky;LR~?lBdv%oZ!7dqz*E;@UwT7v0pIL^hw<0q^6rqWEhfeY_m{<d{!lY-3YnUi|K_o9tbadh&Gu*T&cM1C*jw!6R20`Hozb{hG7q)_lYQN60Dv9T0XJodH0WG<|DYZ&^43ir3c9vydq5hVXpyUY1hns8)*%D4>#_jBNH*BFF#E9S0VGfnGz_NeQa~WKtm7cTU{Kq8X+~SXE3#Wzq{$w%>zmIkLBzxD10;;_N?hRF3jXKJ`g}yPP4(C@<RYcdK6``vsYE;5&Rh2P|YC+}<hnGR_SZpa%vmuvy<Vt=qms0L^`(-A&2}>G_Fb6=oQ5@fQD)~}}TX$=d6>}qqg!)cpWa#IKwL(CAF+ro|r0<5dPEoB(sKUp-8x1|oii9!P>n2eF*T3xx?kXDA_z4lWKhW_Q=uBgYKGP_%dp1_T2JQVYxZQ10opasXHdME3p<Bl{->{nP%BiNaI{!JSj^zUT@%ERaGR01hoy#&H|M1%Fp&T9_Q=ex(<Obz*?6eZUg#i`~Q<9tw_g{>g5Tx4sQRg9EF*MXe!W3rQ$2ql?DRZH#gxkQ{AAsRzB$QNNspxk_<#L(R1*2SC%7KzPV#$2a_nW3;z&O|ZIJ2xe2G<0#wltO+H#;pUij#T8un1*$cKr-C0^_L1@4wHYpi|eM3Ntw1yJ<Ny`UCW{x_j;;{$f$G_mArjZ)@rdkER+3*T6u3K{|aYxlLm_T_0lHouIz-lf>94^MP+RaSm!?8SUs%TWI@?^Qk9E1>tqFvW&A{jA~t<Tny|PC%V&60w$V%%{52IMpF5TwKkgu^;1T4IMV3lXP>lPLF`Sz+Jm%=;8vdPU85=Uke7|3HzK<pIv7Qf0NjMyOxT#Yk7u8*By?8vuAv!F!Yu+NDz%Ct%@U~zvaH`@ij+)M5jE=V2Q<jo#Bj>Oehg{3N<6Fi=2okKz8k>!cta>A_gpNNJ%P>@{w91CYg>YakJ`D_hrVbqV{vQR{*mN!2MnR=&0LQ)A8FLC9WsQ-4QW^gj&ULx$6h%=e%l)8Xgj#cD-bHhtbDJI+@~}rngywpq|8)Oya;%|z+sFMV6z>Qb3g-RlOKIcZ+@v#vwi%lt>0Z=`mEIh(y4z1$DpXEy1wnRA{$6<tKbM0f2UMlh?_u__cc91R&L1`LNY73)I5`rWyeNZ<kCGQ3;E26iUH7+i7vf81N)3C3+A1Mo+t$Am%+C*02}8Hjx<`S39daf<8b*Xd#33aQ-}=K$tzFUM?Lu>$?8cBa5CL0F@Ek`Bw(3sW+NA31f#1nmTu1+d-RLH3CQz^gA+Am@~3n!_HnPiK38>VCE^m6b%iUFr_UJYdu!;a$@(sWS4VA^O=>C(%;_bh@CSMAfLWC953*3Bi*jF-#4#~Z+D{d>wJArY4tHE;>jwI3@B06gup>u$x4W?zyv$%KgWu>0#AY##kUb%!Njk8d7FlF~N;1QueOB9Q%=$#{Au2V=UNm*)i;V({E8krJtRcwP>LuU;ap7pCs))t<V%V1P>kg-6I*efbcawzHEhz;yDdGohOgZUJ&2DRyZsZbMJ76}Or9*Iawp$_t)ut;FHL*nnI_3}Sld*L+Zy45KfFRiICIO}7%pZb@sHasamw;Hr|4rbWlhjuP4{o@}->EdG`O2X0(uYjlJ=d|YW^{tA7ZZX0@y!R`uAB0JGf{g7<iF}@|NP~YGTJ^~BgI@F4K9xeYHHr%;Ghz`sg+1To@pPwOd{LI!4H1DcEvKqv>AD2Y5wfWg*9Yg18S=&%5arOchJSQ)kdLfL#N40BgxMyIcm!?ik!AB|6~}vOSAhqFr?>o4|&>rxY=Fnr916Lo&1V^@{XW$ZS7vq%Ewp;<+Vgox5jW&Fgh@t`aVu!lrSG3H1{5g3Q@4G_Nl39t@k&l(6|n|Qs~8S8=pJ|ATqL}J=KLZY*}j0PUX!dcn@p)pbO9HXyPKS9It7(&30a*X2XCXl4@BvNuyS3AE-pZfumIqqMiipuACU(Dz8M>@WTQ@`R=7k&#rQ{!%fk?Wc8DOa2*MJd*wUD>|)zVPSUeAe*5UUC%8~A<4J|1>uIUslqxk`UJEV_-OvIqJz3M$#AQ+d(LNvbG}iG5?O=ma4HPLVCpIIC$OsLAae@Kd2@VAA+{k(BB$}K^&cun#Orouv5Eyimtf)^~pav3GKvAmDK5|9lVp{H^)b7oR0zy03To4b9;`~b3na>ki^aA_C#p-V_fGV7<DJCcT%7=nkRZgq(I|c)KpMO+Yem~w})_vvZ5i|6?jZ%0B7ERv+GJkMu^n;BBVbLQ(9)ML7?8HdTwSh^l1;*2;@6AI#MiA9~^g{H=J`qzsac^TiczeA<ndE&n=e5<mbBi807LY}}w4q;IVXF9H(WOK(j06K)U!g+9O1X)4T{f-+!{2Oaszl+ui`9mLP4w=0ANg==Fk0I9y^cihZy_-ycTo)86S`^^Rj%fDSl7Zny#5tNOpg?zjmA|={O)$ZjbX4c0*IhX_sr&B<&3;^SccJ_2YVVcz!h?vD$S(MR?r=WsX>-HNwLu&3NZLUa4C|8`gC5+Ff5tY@<22kK^`oR?`pBY{oPo9y8tACnKg}}464yZ<tqyxfM#yA)(VGIP!&#evYVJx2m*o;0nRpD7i%!6HyS?}$Rx*`jew<MS=zDf4K`Js<@@c=s&i9bW;Y(XEvyJBdeIBrtaJIihddT80j)G4h*cLH_{}p9JZhA=QL>T`0|c>dLRCir7!rIq9M*BP^H~tTboa{YpA*{6WZ4b6aEx|S0tuvIMX_@|&W+pz7OyfG1=u;jnWKntOaR0b$Oe~S=IW%n6875Lm@$CN644_`JclqiSo$qx-KvwMgGwf$?&;QO%g{TdsSaRKjKXWy77bcmi_o6JyCA9es{v%N^nE`4K?7aC$8002FbyelPGp;4oEw+9#4Z3>=CRSjK@3Q}zfAcZ80KUX$8d95l4(--9Rv35V>r8xH)&l&EuJ)VMh_~wMKE+TEjF=+QSPXy5=DeVn^+}%TD-Y_tzL-UVE{D(I;PDoaRT4XRrVVu6AiP}YRa-w-v0jgy_(^Lkj&h<0s14fVN@(}X%B@B4gvO}$T%??Glpo)Qmsj%I}5-}Dn<Ahe3)`SG}hDyZ?1vcJUrEa6YP5}taUkQv|2=UDH`UnVYon{6%dc>s}-u(7V`u{oaE#5;mU|%Dw3sN6B2SSzy#)uH1)%)^Ej=97sm2~aOI;ijbUDF_Z)aGI6xp>@Dlzd15$RsR}^FvI#fY%7Ty9&qJ;F@tN&5+6kNZ)kf);hA9sh*lsg(wq>%(|k}h&Mc7@)QmuxOJ?9DYSC_F2(to4B@q@=i3hF5V>pBD-9`H?xw${dEZ^csSET<xEJ{(EfG&Z*#3M-S#ZBAP-&iU}Z~Bm6ioq8iYCR2-VFmGUi=qlCq^G&V5$yfYRrI3$y%)xl#7zAdZ?{nH?S|Mt(I3VC0}(Qo;>i{nlt(X-6HoC!Mn##!Ocqj5hiYKS!Os1r1;ev|<*g3+%@!)Y;ho`kE9fCPt@&Ay7#g~l}T(25Ej55Rh}l{&pL&H9Me=?P9;$hk&^^3z$(`XJD?1`|@P_3EQ(i(c~1S0th@#!YA5`&W@$C)pyV>=#<5^o@pfXhEtRMjXax6Gd3{1+a29bBs~-FT<z`V5X3VVhEb-B4oCI;^0itkWc!kw`TaN^T|YpK2^=c5Sm1Ui^cmsynj&K3Z(_Y+NYUGF*|et5bLv8D&xPbeiL%ARGP14m(9~vkNlTH4vPyunLeMqpJ}}pArBa=>P<NaEdjX7nb#l#a9LT6#y<8gu@_cvc;df@Zt0s*JhqQF@uJsWAxB<)ALdSKOd^PR8~jQz?hpE`5FQ=*Dbrlp(l**H-4d+$D~y7n?g!5rM$Wlh>pq*wmf_|V611+zl<cwU&0v};*s58E24m<2k!*PM#MDT<U(*@pgj{cVThi@q!M4!Wi5a3%+x@qS3LZHY(W{aQeFVqK6}-P*Bjd3xo2c`-ld*Y4rIfi4pUZ0b$3nhJHWnw;tOA2u!wZB!#T*r3?2!+qZwMZbx6TGW7>dm_)>E<cCt(QVBbIr_2k$G;zwES$D*(Z5_<ha-<@+6Ydw;cI6nXit$EDe}nZ6%mA;ndnU5;bb-M$`0<9mVe(bCyBOOF7|xmXT={m3efsat~}hDUNqkt6F)epFSP`eUy*D`Um{8aN{LfciYBo@k_;xuqy^Y%-;2&GyBa#p3uRGknF^Y&9ZC)l?4ovK3m~6@oqg9>A<EEh3dxFE7&mpI|R*qCej!;H=}VscMfws}wdYB${o-sz=Ou4pw{(em*675|#+-SZK2`IM2b9dr9e|_0KWA5WuEm*SVZ&3q5j+ZYcsBdGB5CmLP&*K-wYuJyvrRgm+^%G^-#XVJ=q1;8UJr4Qh6YFNbj_)XM#cn%b?8DJa(E*k!cKp|c<T`x;AAl{zo9i@hmB6Alq0nZPhh3VWbdfRm2h(k6OD;Wdr`XSB6z0L+Leu(LZH+p{Jxc*f=hb-a?p<u<BfD(K;Dw%OIYIH1Y!XR;DTk^NahbnIenrizD;2^eJ8c1Tp*7(snLb=(pH+$YiNl}5M-xcj+9q)NuX^X}fW{oo7bS)^C=Du_CQ2t2UoFxu@d7%m%ekr@GAH=6@CG(B5h#zgaJ(JHN84OnnvFUgTMP)K8f9I~2$!289`b|X-4mL;flOrWq)RWtyeWC3gTc7=Y8fPf8hlH{~kpFrjIL2ojb_opX<PO>SS&T2v#wZ#PD-vM7GD6^-H#zM=^Kl$~R5fM8(VF@JJpT)iY_{!hE)j$6J?bom0zgYn5v6gSYeEY5X=?|Qv{LOa|YFnyx-`1IdQ2U;A&ol?5$l1waSG#)tqNVPCFdA;g<epT4e*pMC17sVX(}5QhMZrIbVK`SEt?NIR%UG_~s4{!Z2Ot*)ci9*OVfE`9!Np$)2G&V95(a-fWUzqN=xMJy-YH_#Sm+8qEu>jr*{n0}J;&)SU0pC8qvx9Hz(ZxT)V{cq?WOAhrn0sat_w;jk+)*5ANZumLmjrf$}J-6`btaJ7)P+beAo4TI)xk{(ZR)gkZYAli{#Kbh}%Ywh2-B0Pj<ukPzEZ>v`xMpueKh?-qsnoD*#yt%0&PUW6@ZLjLvUxj~;z6ZHX#hZA|@Uc>2b?h&m)mDh4inL=)PJ@I2Bzn_jENPTR+@Fc;!kT-VPlT0Ok{I=6l#sm3|crXwS|%8R)rpE9`7T~*C}a*KN?;mgIeE$C~(*@*@Jv9}nD+YLhmF^RDdTO{X~vzV#QsM;{EOCi7udUB%S>$6XKd+o!^s&PV3U#<{}_XAI2y4lKd4c(TbLWtl2Wl=#P1Lxksg#e@#j!Fl?Yb`=MOGJGK?0NNWXiBS>yocXllLC4gtaRl^?#dqCXFBAL9MGi;M-A>C(14cm6zO(1z_XW*^y4%>-E@vLwxC^7b6qkoZ%#i_G`5~@e{S}qa89lQnD6*$HFHQopOM)9!F`|R|7f_g6ue9b4Z4^o!+}hZJzYjui7`e+T;S(Jjod#&L!8#9bPA#J9^>;>Q(+oU>1GnhFPgTN8P;H_*R>Pe@ltMkoNo<Egcg@Xp(ipoES0#&xogxYOq2t%u5MfoAPVv4K40OP7-vlSWA$m(R9u&99$K{5vifyQ0_GVh=5rQfPIZkWY`GVdlyiwC^+W5LeBC2Jq4d?6(zK}X3Ys&#EZka>L0Iw-xLnIP>Q5+k+MGyJU7yf{9Oh){g&ri)XLLI66f#CSsm+3ZS)s!7y!+~4zWjlP+-$f;5i*xs;@15b*Xgm-W1Q~rpkTD_hH$ifCS9w#9Pme!iV3Jw4D$kQeW%7Hp%@}kmmJPg6@~FV56o%s1q%K10O8#f#GEQJuY}sJJ9O;Nn6o$TyZF`9ye7uQM2<=Lk34Bs>*^jRi=WuNTZnZ6O^ganu~ZiwL1^#l+Q+#hH4MqP>xFMj?%ab8CdO&lXLWtl_tyZ@<-mk{udgrx2>tG>KAG-t!3w=kQiB`8R*XVi|Ek${BTy$C*V`-LuI{tou2m%nMB|7#gLlQB@PeY+7kAsJP^`7LRZAjYkY;#jrCwh0k(Ac1!&AbuwXdj44o$VakTE7SJ~;tW00?(mi<LZ8k;Ao4;(Wy@P687myem=GQ-qZ)Vw^*?c%SMla&o*w7@&~C)!>Md8M?V{Od;N>vTvN3fJK<C28#~YE;PY45kdxw4uEs+@uqU)s)O#hZmEXc3_fv6rA^J<VpC+c;K+b&w+2O6g`tSBgLT3*`N8$JYzmeqms=gTz{4X+idkr$p?jN><q}<ZYNCoNleR%ZqD`Lz#I}sGR+?2O>b%H1MTwy#)Y)<xSP@zrcB2&eTBfDo_w)txJ8g1myZXGI3hbu58ya!oPMGb!LSf^dtC<U5I?<J0y_8bO)6t4$>*tY$ndk+H5o=yacfL5Q;+4=&xN*`7R)U6T8Hb_5uG$(c8#p_DlkS6=_X@1i>YWT4<>sE-=_dP8-`^}v;6$tMJfb7Th$gB3dFSd0AQko&R@|zAhh65$NgHdz8rMUf3c*iQz={sj*iymm1Q-q>tRT#}FY;7qch&%%8r|dnGYrr82i<*FF7J_&I2D?kX*};zU^-UWvi`OB-gHw51hc_uroYHvjOVGE+^NvDWNy7x$C*az1gXua#hnV}NkVvzs<udKC)*T5mEKN;GNesfz7t<S<gPNE3L;bkOk``;&1+Pi@*4k;<dfEHUIKN8-CLZrY-Fq46VE!*@*kt7Zt6Pspt}R18ptZUCu&)lztGwB4XhGd>ISOV$?7&o(67hGf=srt#36GJM9~_nRpqrsS-@gBX4_iRz~OVF-;;{zts^$s`9iL4Xf%po&w@=!u}_@JUU)qiX~Tji+j-EU)O{AYd<84Pv<_0hm%u*KAu^xhLfCL%?Xa`@&B+qS6a+5*^a1CK5C9=I{7_W1S_Hf`c-qfdZ#Fu|{3UMOfQJK#JTIzBoeE`5)=dM4o+P{0#9b@fZU&e_d>Iuoob_cSI^5fJx2%*?lvy_wq)vr4r{Cy?^Js0sgY!q{Wdti+o2pW$KGBK|;ytrGHcV-WuF5grhEmjys~S%InBX|D@+XlX2N%mZtNQk25Rkp0N&$<PM34bXuF2i0@pt%v@3>MeyeAOLer{$y)R&X=XvxFK6WidbEd(HDN?1Q)-rnx)5mv>cUr_L-SCH!qK1P|KEfiTi=D$7%Yu2#!C$JT#ezS`hoeIxMsaGYz%jl@>Wf7l4Oq_<B9g;m57Xl)wrVyn9I#?&5B2GhRU$CSSuinC_>oa8})^`{faL#|B!FVcp^IUUQ5=GUGzsWT*3^@@(5X=h|JClW_$|I*?^mD#4=nb%Eqtzo*i3EerutgEuh_LinMR~}?a0^wYVRj=H*3ZKc%u!B7*vJAbcRRbYrE$TVrGOav`u<+5z8K)MmQUglukk#*Znk44TjD%;t!`|hsK;nvF0>Tbq#YA0@Y9WYlg(y4`rv`JB&9cbo6baK5eb5rnt)(@O=IuZLyBWdr6Ea*$t$ldc40`I3!qK)h#6q~mOCERyWthpK7Pw|Ol7pI1{g<$7DM>Bm@1&1lA@MyA6mpdR3J&3p*Q!DI`6UB7Rmdlz1wjPU_FxOZLy9$Ky^5#prk61@K=1DxEhQkYZ~^v05-R}jm*Ibv2|j>p#ogU<O`V7i@XzMGcHQZaBO+%PmY;H(STIlF5NawvTX=Ne1{Zoji;V0exIbiktuf1snb2dN^F=1*sD{#VVe3EviPRgfLl{jqYc&;D0&KG=H2QJ{3XcMG`j7OXc+4@Aj$tlgCyL@S7)f!KoK;NN=UrZN*JXMh-ib}tHz-|3df}8r+aP2aV2BOF$o63@7_nfGythpLXp#x{Jc*T2^z|=)SH{u7A7ezPIZ9~p$!xHjE31!s>igo@ymF?t+cr-!vLNb^AF!LVflP}L4RlBZKI3WDOcuM(cm1;T|=>dm0=Z{WG$Vb%WyZR93`^ob8ok}Kyt<T4!pdxEE8M2VzRE3^)wHzWWM4T(^inHWI={$glskKG>@+k#AhKSc)xh9p6-p!G7$5WOYnF&ks@}8rx3D7GZxqlcE#3tqbe7M;riztq@h?Axx&P4eA%*F>BK|$9dz}8-lxH@Aa^c2V5PPVs|oCvaV-VDE<@z)uB^gNL46@?NJ63C2fwL^yG7TSrTr2z6QJ^hpU7Gn9#K>a#Y;v}Z6Y1{O@J8vPI~|pe<;K-<AbJ9JM~fuN_p+zd7Btaj^3z+V5V~t@$3Yq%$y>tY$lL$n+owv|1^qvX3|EJ>Hng3sj?&O6zQ{0g<d8v+ihw?Au`A>77ctiz71E{M#pk;S%9rI$6qo`!WPt%%}z8UV|MddjJ{HTGf)VGNdgMuS?YK_0lU6<UzM(6eiAt?*KaMN#t*7YAWay@K$MNefWsHmH!srDq13%v>^;)b<EVhwke6~+R=?4Pbl#Zg`zKdESHhssu&6QQ)ZV#Fo~X=mik~mJtW^qf2p<a8F+h{^YP+4{%XLWTtpSrsZU~FhcyZ7ZmCx(w*j<wn3Ui?VpAQ8B&xx;1>*QM<tujq*WTbS~C?2EwWKZjC-+%&8@O#@{i$1pS`ryZ`^d3bG>AE<!TF2e&?ImnBD}i8#zhK{1-#RmpU35X_6%~vM=t3$K@Gw*#dpxtccv&(`Xrj`uc8=|DyS3ewLMz6D@zAptx6Bkp%nx(?<G+9Z_8mnshXm8sCG50J=ItLJTt1P7*0@2K9Brv;e)N{bQlJ9pt#<|0<Wui8;w3$Z9@f_?gWhK_q`b{WZJoQFdJqCMwD>t>SVBj%&@ZLN%sdi-F+H>fs<Q0qX1o`>jJ=&gx>Q`n@HFl}s*1INwOIwTnWnrA6P^u~zbJbHJykSMPt+MW6tAd=-WI#3p`GlMmy+30Ky0&ScZ%XSt)j|^xV%8XufqW-O<U>nrB~Nueh^(?=NhQ)D~!(Rkv;_}86&0H66r`N1>Drvg#v~#-#Fx>`Agk180viMe11LxGFdNOj-DD4EvOZ7YNjz>+S^RixzJyw)u6Pf*%Ad8MBOJ_4(m0!%zW@?&H_}@PSazTe$*T_l1uwzMx!rg?Yo3TR9HrBQMI|lF52fbWm=>1g6KBXm1E$^?upl`)F`Ogr#{29@agfux5dVdcmX2gmzUQ7*tEs=2be5evj3|iNeRZf`rRr80>Zj%`aNGcQpAjlF@F!^I`0aJ1`(~x2d7(huyvGv5LF7n5hevgD&CbRt-JX)Kt)*-?Lf_Wx&&c9zb?mJ<T|Nww{jSak*=F=&0;kl1?zwT<<D+Y8*>_jvctRM^Sv_Fp;euc9bN!=aK0f+&t)m7YQ}ztI{{8no;YxGnSImNd{E{$)}@#`!^t69lhjWQOI4ex?E9GK#JhQXVGXf0)pI5i`%aC}f#lqjB`(Qpl;b=P)`XdxydpvV4QR<iUd<{0YOX4PqBE^?0}m<6yC)^YKwhV7Np%m!dho~K_PKAeJMy9&i26J>Ri>oayo?h6KC}MjOLZEOFq(7A+Cu5Pz3np;%CRkez9QX<*EZuF!j&@H%>b*7-q_(-9I5sar{U!_#-Vz0ae+U?aAsTM8Vz6eLu<{CLfnB+DQ^&%qWDV2>)gMvS<n0u!t2~mZmw3MN)|{vrRx9Z7ooB&RM%*2KR3vH0?(GJExn*o&zu9m;n`b!t+qF#D8Ou88>%orKcQ8Lu`{2im7z#y2B0=V{eqL)Tm>GHhG#NWbmUf%A41Cuby!=1hi6~W$%?6Ltqq3fLLL_Q-lhg8Ku<F-nk#=)dSgTH9)?`&cX=LU=O2d42~KN?u?~aXIfXhzEXjs_Bm<3;gz)v4#n>q9%Y;q6)>b~JUo%#_!}TeoWEoMz?Xt<sEjf~wwW+yD_|peOeb7SCMZ-*|tV(0|MoyU4WC>B5rJ@2!waQCj;XEW#Po6tx;<!u{iI#|n&Dm@%L3FZ7Nsp43p=?We(;efNvb5@r%pECSxkKALn6K?|X(Y92P423YFmRBNST9!av-WxQHou2qhLH7LFvfbR9OA?ai5l_pa7krbdOOwr9^G2n#>!DqWthu8A79>9J;QcWCk~_YbDRcR#CA@NN0OZ@#VAmH1x1V|d7^`_eQ>VBERzV8Ixtn4HkIR9QAdI^iDKeWvR^zLu#jEQSRyJuP$1#Jj;MOi3)shmjDjB-biqFOQzHc%w)v_1BQ7O1v;Ra~uK@U_o2x<Sm+=#3Cjb3_pp&m;r#Q^iJ=qeQg~z;7T9+Hv$jc;CB}RG&(88*c4pg~cx%sSIofOE;)6i6bQuEpbe#B#C3P!|lMxl<&xNFKu;7q4RwCUJERZ>f4m}0#)>N!2M2>kKfJv<1itE(tu-zPD1DJRkV&{a~SkuKq_fdMbB4wFz7wkobztuhjSO&*r>q^}umaxX)~x^|e&0W83ddXCfPcPJt0AW{IY+{)$-+hs7|h}0UyA_d$h#24|?Ppiyp(%U{cq3Cvuig)f+{fz1=^m}{%>?5q(C(s)W40JaON~4A~F!4!>xKl4FBcJD?p^V(^%_9C)!Y^*UIJzfjZTMU$)WSn2x%xEE%Ii`f6Hb(a&$CKiFmYyg6Y56*6s(&C-u-!sW?#q3;@FckB#VU|-0D0Cs`o8OL-UBkbsWHg6Hlv@a;?UBHgeJ8rPMM^Q%V$6hhPLkR<!CX(;k+pf;4xPt(<;51aqV<IWI~Rt&X@*nRDFan|jA6d7P`5zUaJdOQ7w31%<aqSonO6ZYS)tbd74Fv~ok+0R`h)3aYOSWG`&P-NU&4@Uj*a8TmK_i>zB^8W<6ZGrRqrh4UAoianZWU(YfG(>jN47xCtn(O$E|k*t(8?r*IvdEr`{l(|}(6<v%=rhtUtfdI`RO*%rA$@+y_W}7F*sXFHf|Lb2r|MJuS{O#MNLm75RL)l0$PW9rGRrI@ezU942{%}Ln`5<{$hw(6*)z++F2~R5uQz`t=a#FHooYKkq_c0CyVMo3Xay0^Y$mc>k&0evD|3({k6vFfSED|LW>X^DcoOq#Hjucr)mr58#0Fb~fkAZi(ne=!b3NmvcVtR#T*Ctz{)di1KfFIv<xiC!R6x=rZZ2YoK!!<J^D!U3hG#^=jAehTEk&e6u7OXn}DfAw<^*qn2Q;T5msT!w@nuuAu*)ZRS$YE{iQ-^0Hdt-5unnkm<r?uKVVq7-{s7#Eo3HoA#8?f0xA7{2DER>Z9u(+Sa_fC<hJ)1&x6hs*wO;#nc>fk=f@3tq@y-W-Iw886lyVH6F|69(sZ@DhfB?&Qt{rkb=Oxbq)l1)`5`74o-#^U8L$4dO*(Hvh4j;3gU=^WFDi#Oy}pps?Vmt^z{ZXk{H;Kc;`g!Mlze@Kz+94dv^;0ole<uYvB;Z$r>Q?Kg}1iE6i)&Dqu8GaOPBhxtL;=ih{iH~dXcu@QzMcI40xj*&kc@O1C*VmP(?(<!JaR5OSe{-U&C%TTDVO1f_dG`YIY{G`YgaO}VDb+DqO3d>d-1J9r?}DLq8JVGcM-Wj>XslhIfrSL!Sq#fbrGgO-K0k$*Qb2@->dnKsgCUN7KFuuzW&Tb0OJHbItIm~<=a}qO&_qMgs8{3hxDvCLn`FM*{wDXvz@MHEY`FYOLnuQbglLPHaoi)jU7L`a*WgT6rPA>xkH=<b0$sO{r|&m7WmRKf!n@?r(%oEr4wfrmXYaJi^B-PSn8+LkF8xxdBJN-6vpjLA!t~Z4N#y-|sTI}QToccn*0Ios#&qo7EnOx8<{i%JObd7z>K8)y>BPD501CYXGT*=b`t|!a>g#XoqYwS-+b`dK!(pM5&adK&eUUT4HBBp{vLLp~W!%{cm!y`oT&d^Q6dFOa(Bo4J%_>I!|5g52<y5IceZ_0lvm!fn42!@9WZ?zJ=6}<|O99SeJut+YUuJ+l{XenZ3rWwue}vZ$xoQD+9a?~tI}Mh#BwXh8{0lcHwGV51E9(0C@t4)|PI|D8Ll6W0@j2_CAJL8Cp}KzI(@J~Ys7T~)S!hHPM8EEqPj}Nzi+ew$GiS-3QEX9KJzRxGUWM;jGW^Te-+nql*RQ|*{Oi{rrt$4A%ZktSkYeY@;{W-ns)1Sble(G$%xNExbYS1Pd4GJv_kYENtNKvZe}=0-DnOtsDniMf@Nw|#j|S9k*?J+YPwR>rPB5n9#of1!iW!_gsu!vFiGR=(*O9doCxR3YFG5N_@qJYD*uY6tp*V$WYYnP>Bx(bho*$+A2+glc{R}OF?24)yXk=(pNEt0G=s+47)#v(qy!gC=22EYI$LJuG<um1D_PU37|2~zG%CO1xTZ<Eb=UepO|9E@*=f`5miWE=HgGz&Be?My8(-oy6L`E{%ip%-#-j(WLeSvBr1qpw5MFohhnDOyl!Xruu(nmv7>`yg>;CW7q7NQT~s50}&XhmtaC<3V>HlK&!{Y>fx(+;|iZoFlNu`H2MMC%y7Z1K`ZnF=}bLEc+3V}-~BXXA!*!KKZ3IpC_|;tSu9)g~!KCxg|!gwi*b4{{FjDJF%ZVq17AQEt6kZ@vQoo}G`~ruuf(XPB!+J+`%LSVXpy!P<q@p<p%pmep)6FbCg1*xe^8xbkBwnY@!7!(}#dY;j_1!J*pA#;1Vqq&&Q<tsH<d8Op}u(*w49_7_f({=oM_RagMrk)2)Kzz=kC4(~ST2xIz1x3(1Kfk=o4bupTWo~U(eUlqplrRZwBNd?*7>bG5UPwiIhWR&}Ox^`HaH3ZjR-2YYRaS_IDMt2-brEti!<?u9!kO6N}Hm;7!fW0~$HNY+zY0^6WVzr2=Z=YH2s<$FDA!1Dv=M?!$Xd??HO%xxPD0{)=uJtU9c*qPlEz(=UzK3H9t1WU+c*5_Cl=FqHV4~WubF4~QHrZ>Qtz$qT?r%zKl^(-n-wHd+vae8oOUj~h1mwd_Hf6C1D>CDD_P5>-%W+>)LeiEFGYrgwW&fh*GPp)7J!hq~9nyGni$A6<oL2bzlgTXnKGx}z>|G}csJIKbH&j_Q>Vf$d`o@gBn_op$0bOfags!HjCkd}rRjn*){g^WxUIw{iv87DShFt2AD@D#+O1am4>Y08ktT8OY902J?aeUvY<VziH-K|Yl%#9!t>N}N@p`Rz#3IXvB0q#nk=)0k<>s;#+s_?PzMnm1SB4G^nx=B>P^>6!vX^Mt5enQ0U4|F^RI@4I9{|kcizFYFW8{7^I%rCBE`}%SVQaF8=yO%+TP`_>}=SjNuybr4Ahpkd&Sm*v_`PN9=H*^U4&V_w#{haz2=_0%MOyBqEp@NJKE{3Sf&(i@}?>AtgN)V31mDPoIA67zFx85+7OpJYH+Bx!zin5|BKz9B0B|+5x$H0Q?jt!Cs$@Kqg4exLhJi#SDhaOC4%81x;8lDt6aD1g<w)-)#A=HE)(g&<QV8fCTyr4NhSoBg}Qno)dtePmTdu1q}IG4VH1Kv9U^yBR>&r}p%(b&1nJMs^&RW-Uw@R<5M8!$I0n1t~vgyAiITo^@5!X%H;{TJiw1@yCi)VcXr3=N6Qn}W&vIHxw54X*!~2&Gw5DlpuPpr8_bjeb`sZ<IVIFv`WH;VHR4MsTZBgq)%P#<}LlnPr-@P>pob2%X?@v#B~lT!ZUa2zYm|ESp_%()0J<XEEWJ?&DJ-s{wpB71=<4fPPj-GmqY~Ri?CmTz?=CMNd8KnN|bgicRP*NH1OGejC&2`Y@2_R3I_Qyc1;u^35jBK~1)%E@o|^?K95PF(f^bcd(J_<n>}y>-ywk;7BIXAdnU%py}83SLoPCdV8_fW;eHf$_V{O68Ze>lje1(qCqg(AyqNBm1ld`D2*(vRYFlX>8}zx7)9Y6+=SXp*qFJGXP>TQI;m(4NLfLIZwtycYXM>2NL)-%Hyr7DaU&@5V!i#KG$1xH(Q#5ehO~q;p4EJFD>y-OFJOGU(I)GjP%M@`fzEBWK{%Y&woom2qk~CbG{v*{rfvU7);I;M+3L+)k2N1@)UF*e1mO>9SO$)9A}pL<IY54IJm_dUxXCLJDphUpt{AXSX-@PgR5TsQ-l2FA@P2{A7?DC|J0|CV25W(B&o5Pey^nvjyIBCZnY33znU+`Z?ur`Y>)Spn0-mh*5WM-~?^K3{xCyjvji&6$YG(ODNVXyGz`{h)*|CupxpYs-8b5QQVgNK{qDybjz&_*3f{nyxTXAH+48ElS*f@7^q|wU07*_XOHDw=V&-5K-3dg}Zc_o|ss3%{^Up=V-PNthd$IqRM1T3@7_UH1zV03ln+3i$kkACqt0eK#AaH57x{*>;;KJL}ml&mhTL|nqMu5e}Ylv3k-Zw-CGS<7bd>iA@%-0^Ta^7$+rDs4pHA7r6*yj>ewQ6|nLu4%`3*zK(xnL6CD^n@Geuf6O4r~65($3y>(`y%dB8T>AZAU2Ds_3R0$^LWg5T4enJD#;9swrFpwyY3SW_^2K-d(qUHCrZ@&AmzIYfHeg9+I?*tATAuOBrjP^XohVWzwU5K4wBHi{<}#+>z0(qoD}hcGNi*_q@_q0hCA}V+h!MvDDE-rYRI`J?r=F~KipdTz_S`BcBh3scB*qV+*Ce6((3B7V*d%1?nIq^hoUkDm>|c0FGjY!_Ph<<&~o0Mq`Bqc-F>j57;NnmQk8k+S|wEIhAyKk!1@?dg@KSp1O_DE$Ar5Xhh~}3As%a!W|)t@(4ChBc0;E?XQsv~h=FhNiUi|PO>F3Po!=z74u>_#rW-l*M(Ae>8}hg*X#MLc71^`t{FZwl<KUk)203`J{D)k}KJ?!9LRj{Lw$%>fklK9v!A^-_B?5w8#J%5>NsWQYp9B`tsI^&dxbpSD!(iH%nlYK(lt&J1hy!o0!PK!&@0`~;@eU_?k7{m5RMj#Rg;qow0+}{Cx9kM4<=e-zzC!+i@x_T~jPktWRorYThy*F$imt3x9c~TgM_ZrPK-T@u?I?hc$k06@Qet83H85nXT>lDtq=y2fnPQd`<G@{o>xV&6l{hU=`$je}%dgGAZ5T#-`0S=;J-X_Dgih};HApcgA+!(`0K*Bi1tJxMPlwBfVafC{1^SpMY-f62ZiyA{ZO&S`SRJzWSu4Tj%DogXDJ4LO`Y1(`i4Iy5(1{QW=r7}HpX<5|#eY_E6KPlZeQM*)hG|kk9BnP~2K#!=7E(tiqo_V0AwbpQ=^liHp!zZ@N>|Ut^4`X{b_jHMg78b7^Zy!lz&So^ANkOrngE6cV!T8-8x7OREQVtivcn}XbAMD;m2nhp7p1L{ZJ>+8=yV_;EYx!-_CUwEG10)HGKLWV6D~1Nu%HRBl47ZM-e>xGTO})PBbos8NkmH^8hA50Anb$OQkJV46me%egTGF<MmrU4n>l>~ozNWHYtZGWL@gbx6(x&g8C77N`#kPW<2%1SSuS**hLoiyQW!AUi%B5WCxb;D8;utPPSpD{IB8&Xs&)k5l|=U6FLMJRq<yev*Ucr0_SBk5pTFwWbFhg?5>gO5x`IV$Ibn=Wf{kBQjzYbMJ~<8L{B0`FFl{!K2Ye-0Sk2C%9$i_Am}MCJ=n6c(7@C+nH^9Bh6-h!4uUvT(vEEk2dP9IpEU6+ophY>%3H@!rQL5y_;#hsk{jhZjuMyBZJk?DJ>}XvPdO13@GjhZhn#YDw0!0x(+Nv)^sJ0T0Y?2Sihfg6!r<i2Y)d-UjVBB*?IO*YKc$`hb3u1{SYn>O{0|p)h4kt*r64$F^FSaPDABvJlxCPOATh%h89ZLNVB4!i}fAcF)?haigXZ27fAc}%&ds=P{iN|6$8uT&2Vb?UKqEeBUVo<b%T+$NNa$)mJQs6L_rPn~)<J$i8^WWpU*fDUzJ9A@$q9Bp6>Cqv4oDQL&w_82oKw4?SqWVynRf{;D(Ld7yl!}T&$b*6>6MPA92F`z+@}jl0?7n!TzsO%og_Y@8_t~$1VU6r9XU3$U?IT;%$fyTjQ~p{VnHW$5gI<%y(PGIwFH~E11d}YAeW!p0hA^Zh)0?keejo38vt=8+5&_b;8`5Q535Rmr9i%Eg7HO`*JZv#yW#tr2w^|<;!=)4M{Y!=O7PV}apsG-wOHN^HScewO#-TD{6jGOI)n|I;^wAit>0gG{6tGQE2gtA_DHm(%{Bqo)P~Vnr<E<ICISpsF1w21;_@c6mP;a<;-}?u}f|fb->ws?7Og__TA`T*BMjbR9iq-F^2v$dn8mlW9fGipsDaseQM5O6*$xD?s12<NBQxA1Zw5qbOb=(d7!_aZty2LtLy(@`p9QuH7D*E0MFKg|B5il|3LiqjThHdZ*Ubyq+a|n2jUMA>r^%}Ylu_-AY8hZrVK6tM%-n24%`y{4(qZY^`r*#Zw!7<yEf*4CTW|m&}82TP0(;7VlHI(d^rIofV9dI@GCEZK}Yz`Hw&yZ76H{5DBX7b-ze2+k110JPByQHIPe<-T<>q>|_8Ie~dM+<i}i(@Q%Cad;^gu7EfQ)_rt5SWx83X}x;g#f4Ht+PP`t5LgMjrM7Q`1`cS$F%d&K7F5Z|FR<_jx$1{ROe%(^yQC7_ZBhxumAOUCvMwJZ^g0b_*|bzUfNL0BR{Ha^#cB)HGhsja{0FFD)`Gr7H3S|1q4hx(j|%=S1X=V^&#D9tj%nUrSXe~NPRgHzEdL6QN^WQjP>-w>?<&f74RuX_<FFpOQaL+r(G<M3$eHh0R_z;FrF=~B%a)Rz)pJABCH9`@lSvh$6HgW6GIUxi1z;0<|Sty;ng`<@iqAQ6i&Wd6G#Ok_J9HynJ9Lp6~lHN+;jed(Z#Xb?9v$g>SU69sS5epsUB{P9Mt-1Bjwq4v`HlJ#KrK(C;$Gf{_*#3zkdDx&3aOcegoH^{x}xpZ@%AI+fs2Vw{>QB*1q)JGx~Ux+WXORSZv<;i)_6QXz6Cm=}ED#hiBk3uHxZ2xi68k5%^zxS=*eT{@LWtSQNN}Xp70pkR$H4>r#Z(u_$`4;~s((e*j^SD{JVkQ^|UAJho$f=htdCkZy`usV~J98V94d6wYh-y>93pSn6D0+-nQZT%^Th7ipR!1B2Z1awsUP=ocbh-6H{j$CAEdQO{09Qt;vu%e@l;B;w<MF?OGI>>BJ@*;or5loO)I(eGz*SB-B)UG&wg5L9B7JJQ(<?pdMFk6n%Fm(dy?bx{~^savsD$j+z?tkYim>9t~5R8W&~@gb^9%FJ1;upE<{6M}{raSpE4Df2X<G4ek6#XS}9u4hFa^wP~HIwDb#t>d|mqClS<9G>Q+x)bV_rk6vsG23e&AI6Yj`u=>D;e|Eb?E2&S1#d)9!$%}!=)3n<QSWaBIPyvKBoJeDyetWKEMx#k5ERpf?5EC16#<57Q1t}U|NEqd+&KaD$>9LOp|4|9ikWy1O8w23J8nIuIzFvL?Q|WbwwKauFYe+}lc2_?cu{v=Pu|j~dxxu1l4D1jd7A&Dk*QLfAW<&v!c#1xVAf9Cbvqv=^$`^c{Cudf)p)(ur)tY#2{qIEtH#O70R5nDpUl=WnHu%-bo9Z!8phT0t)Y6nrqD48YL1ZNjJa#9D^F12m|nA4T(}Rm&vO|Q!;6`jjF!dh*DtIY3xNc)_%>CYEXs=-<ZaHukGZm2lI!Apw`8eMpe_b1%kOA~*sp#uA3XvFVB+X01afgTSPPp>3cG*H*6|<rc0yUf&Q6;`W0k3g@EddYj*Rs)dJ1=n8zS+F=CbYV5%w!aeY(EJcWhuGIJiruedNb*&QvZvnJGoPWSRD1O-t8WRt$UyRY(JPd8B;CSH2yWMDdEqC2?Rz(dmpUbQ%2WbKle<j2Ps2EIC(ZPsgf{Iosj>gU|CN%@Y1U_TFVllH5oF{GmF8Kj4pJ4?BfJk?t-Ew<&p?|No2au5^zK2h>#65Rv3?c5fwFnGtvx05df;HH`zDWA|TN(jvkwUXN=c-TSdpQvh`ral=qnG4JT=I7YoD3(?7N+hy(q`YSf9;UXWCxxTQ+WevGLV4h>H_g8<D1cwQ9dOz##vP&zL(Kj*M1^=oeBiLHec6$ZxGkg{9vnjY*2;(go;3xis7tlqYkqVq;kLIZ8i9#M+dV~@#%;}?}zD-XFf3$vClq{j`zI6Y_d7J%##`U*>=!dO|5xp&7yhWUq80|=4Cxn|KgbrB;fV1W)LOzcfE+Xy2)rSEe4lV+RSYDyFK3570D%Zp1d9b{VrM)i6N5IUsMEn)3FaU+QubIlDh6iL%wZmb!LVT1=CEEIOV!r><gpy-$P|j>lrP<&KcqjydH%z0t`FtbWo!S*fO|G&wh=8X@(z|RCychu6Rqdt_6m2;Ss;0xn(ISyA_X689<(Fw5lh70(Z%{;n-E$R@5j=`GL2sd02&y@G%ReK)nYvq8>ATXj!koGRV@w$={$fj_vPOdMN<`zmqeoQm%1O}$N7REYmZFjYC?I;*DwPGmMu_`a&{RrGCb<#VhyydMiw=g3c=y?Pw|c>t8JWPetd=LB_l5P!mD|nMu;NlIiS9djz#}@<<t7WXfZ22Pi1)acso4lNc*ri^)7<isxCBeNjaq`GJuI_&`%<lsEd~&K2w7BKZc~QQq%JRpXc_;opTwwX!+losbLiHkL~O=x`0LQFa#IMo)8im1nfMI4)u56#>UGT5(8Dv%NTM>>6Q8Vpi^OJITakZ|>B~@T=rW2$K$y&))U*iIhZV2<?i&>7;>q(;J)UQTsM?2V$bl=2`5&?nDlY-0UN9DU3aWsM(<2nM!a-pGT1M5tn{;bPX$LX}xLqI-+u%4SpiM>r6i^v(y3hThv=K7$r5osL_eKIUq`4wTZz2%9jJ8HfSR8<UK{*hXNHPJ%j*^<?+=cBqKcIE%z989E#@%L<qMOBJHFv-EF|%du%xjfOUW2`n5AH8=f@oPF%_HedP?^*<O3~C9Vvj_gY33>}fh(1~gt}}f?I{(TJR#?5N_NA(@W-sDTwT6spbEHS-QDGm0ZOiHSNl)76^zRk4K<TPMDR4p>oC$iYgNQZMP*uC4~J>kI#qb;6|U_DEN*|&&u``CwQGtSqWCMn`8D;=8a0tJ@fxQ+-W&TlfjwdClp$d!U}Ifg*PoPX6ST{16DB^{umk#hW_GM3MJc$RXM*!ZFkMzh5!{&bnCNW8PomZS+fy$K3Kxr%j(|=$F!?a%<xW9!-@C=6<($B5Q$ScxUrK1ncC`maQMygLEz9kayTf5s`+6Jdv>YCq7rQ+Elkj-N)WAYyu3qPo)%`P_BUgeEsAxD2uw9u1LjRQ=7>X2ucqg5QZ0Qu*1Upr!Uy|Yv@1$m$>+UcFN*-iVINb_#AC%YgN-a_%5+;YHRAo39P|>NO6l`)v=Vf@V%KeEvmOp%;GH@?aDP??N{-?YK<tbevi{Pr1(2mO~YkE<HML<6iJDWRejsFxyv1K|Q0{Nn$y7d=+(-J((so8p!-$Nx)@pjuyl-QD8^%C?cIH#g0J(@%q$8;=9M@v-#AHA#{FysC6Pj7{E6?bB#Xd|C&4^ztKYT*QG?Jg~WFvW2Eeou9&3}mPV%(Gi%?-R`7L9dd)YU~2IRZjTGX13hA6XR@S8BS-h#68&Pn8VOfKGCGzMAfw4{G_)Guq>mkwut10^0Mp502M&?09AsWm|W#J)#c+6H^SjR%_)Rw5_>P^S4hdR=nTA`oIGi$Sb!ZVxs-(ms;K0)c$Wf3YnRTK;3X`|dtfN`{c6ydBnt{*YSHPk*Q!L&_qkHR_!vFEKHMqrSdbcUxWQ!8wz}Z>GBB=qY%ysC`vDv^(G|T^8W$jh?GZC#y=xOyG(Csy1h3YcO{wqVl$ffrb|F9}YOe$`;uE8AEcKj;hG?kjCO;>75mqW1&Y8lK5>P60NSM+|P&QuHsq<V3N;qj=z|?(eq?REcB@$*SmAFRBb&?b(1>=eA=4(_4J}hjfMT5<eD^Ik-N~>D>>!{&BHYp)zP4!m3h~rhOb_9|G5E7@Dl_gO*66oif_f;lH&M4p-7hE@|wuh3r-Yq^4gUBEXc-c$oTu>rcE43CC<?|R=fO@OXh}e8NOX)T-3AV1D->N@LX|zJ1(NI`8+5MF!DlNPg%wm*PRos7p^k-;Ssj>(#(kW4-4XmKI)vgE}LZv7dWY}iMj=HM3nCAj0UdYLoK?9js@lA`Ca-=pcDxmHxeoN67U|Mrq>|0L6=6(y3YkS5$yem|saqQ^Eql#^HEVvD4+3QKDQ5FDReGs@#Hs3lkP*!vcQc@7y&JfP4ghc=aK(+3|^J!~^B&UIk5M)8U*u?f*-z6zpdwOUWdbrxCUE%!qmYC<1hJ*puxuoO6f=eSZy*Bht!TT-C?;D??Dr5GkZ(i>eBES2vVD)zL=>3?=lydfZ8_C)zx=?cQ5Tp}`sKiRBB{CmDfGrQ=xD6q%;}lU8yb>xAS0p?_RY&@U!~9@T?+y{q+MkY@F0yZJoM45{BATG5yA*Y|ay`a<wdMEiT${XFOa;HbgNC>)T0e!cD&LJZc&XBK56pbXJqbW;yWg2gk(5#MJOZC!k+xu;bVOPlv&4|!a=RtE*&~w}o<aAP+u)O-5yZw?tZ-b<DBEF{()7}78r7uMBu4ngbEQVVCXOnRTJl?hQpxy!t<D4NI~vWlHjv4mHVey0n})CD|K0a*_BE$`H;X6&>As~wF|87`Ty7=PV1wFVCw|DA<2bC|=A_3_z;at)&hhSDzz4xbLU@@L<MZa~50~3&zuHWDB-v0TW<>$R+WZy?0s&wR9sC|5T~r@N$UIH!ek({I<Q-yTwR<a@p~N~JyuC>C9V8kn;v5Y(e|wp4p6N5e;0Dn(L<wlInGQL+T6^BSu2nF=(Jdfcgl8EH8Mk^M`GeWj&&m{KsRd3(wR46x0_UBfQyIeqDf(&(k5m)&#o8rQL+HG~DP>lyJBpTb{Du?q9-knyjd%;pQRaL5qzy~rNjtxzMVGp&+!D!R6EAIQTN|rdlNTQcK^`mv)AKk9T>XuF(Ev7}7C`n9rE|N$zI6iZ-4iciXr|of&u@bweao=RCOWHn(%VDTMe$D&F~b8oN~eUrSV&Tk(+!x$aSl~ICNMnhG%JRrc;+(xSO=iBwlZbW<2IdZA~h!BG_AaIIJ(T5|F(aq*_U^uZk&2cAcSI^*~L7@Gri%zP+4|)3AJz;i<{k(P>I>^I#qJKy#hQ$1j88FU&f_FQ4jcdw50`a?_ol<(KO+#R$qDP&0tTPjY=#>BQ=jrRMt@sp_e{J1%GQ?$ju=wm3AW$<`79)rc6TzOa#B%LVg74R$`2{R0q%8p`#O%i~L404Y~c8#2_{GJ*hl^_+_3Wk!P*Fo@sQCLauR_JPi<`u@EOYxBHe%wtzHsJXp>L`63!rBCplydQEeuq$blHq-Y>p4Es=g2DryGik--Jdo}Q~GJ*&BhO=}D^!Xs3AFd1jo~0b}SeV1Ef}BdENe-cgNh_SS+}ScE5*?nOWg?8KH+@^v!xnzG^}twrcNI8O4bFNubxY_)DnhCUEO$6~Swk#0ZlC(3ETqXS6h+ex9FPI#KLf=|ACgf*80H0evsX}U7&&L&;#UH7Z;6shQAv8Mv>um15v9b_RI8YWotitki{dxZ?wi12UafgQ7$wKec9qTp#!iXfaV;pyCQ*?Y(}<Gm`}7wHX*Uv_RIb%gRc0jj_C1{?wZTKXK2H>F5+3Ul8?vn5tR4B7SGl=TRem)q;eYYp7mE5cR4zlG@)UzpVI;;#Z4vFHNVM1hwgJ1OVPK;I)~o+!N{cL&CZfv@Z@DlcY9~>Qx@6-Er4lh@q!;x<aN<N~u>WJbOvd+8Qe?PJ@sNj}IzRlEhnoZcX;gW&R5FB(REX#c<Vx<)AS7<cu~fo?MBYP)I$8w{to*Lg<<pFd_HO58hfCQqda)k3&UDW`l|7O2ukC;L<=mbAmAD4l3@L~c=O_dk%mf8#CbYKP_p~CuEJEz(90BiCrdl<$m6Xxzxr~OKvlj5C^hVgdDOMJDBj~$rOdW-cuAIEnn%jMBDmg!B#FEoW6FZ!@O(U&ihzd9b@hHb~S>;ykb%F6LzUGKUI)&b52xfr+sRnU?Z^AuX_bH6mXcI%ax2M$_ZFJw9jqXUu-H(UVmtiuAQe=rHTl}V!7umB*9qY0xJ(<>lM^$jm&3K;z^~)?Q^&*3_ugz5U{Sh*{-?X=TOuG)9N@$cXthX@^{Ed!k5aql4@G{eeK6jR3FY9EtFi$ifToP@KH5NPGC`j>%KYxSu^lp{lu^_X(Ag52#6g0oT^>(0Z7t(C}@X0viSJIlHDHCW0#OXv%+hS$hE%rXv#inHNbohO+|Mkzm{qpnw{N?-cdbG2Fno>=w`52yhILSKtZLi+)-jknX{y1Lea&LBZF)L8lK6{?EzNYk9IQJ>+h$GUMt>u1<Z8HKn$bmpR$DWjguOq2MM_=7#OOSQdA#=MX@VW+JyT`D{T<|PVB;cEZ+_uSxI7T=@Uiuw|=`aq;hJDPv{rINKgV4e@^aeiNzs;}7G5j4PVDL)nz-mk8tf1;SYRK4NJ?)zlyFz{&c*Xbaen6Gbx*)bF`h2FyJ5TMy^9D}%*3;kx&qMZ^;PehgEVE~`*@QWGLJ%#0k(NN8$M-j*KjX=i`_?hVJz<xO63ZfB7U_~}%$`K0fd+higDPf7leginM`X0;F}zH2^lp0B?{;VN1kq7Wa_qSY(fxPM5rx#?xut{^cDy1gy+7rtr|)<GPXCzlkD`n7i@`w?4WXVpbd4&_G0WL!d_(fo$2ZSNdI|sI@`u4nq|fCQh}!De?)&+q@1?6N<0t0XkV4vj+<zH<)RTvkKv7LQp~oe7v~0fuMs`W;?xc8kcPBQ3r|O$F0mtl{U+pQlkZ(>f6USbu-l<!Rs~z*&?fqrWf$KzonFcDgYb`Lw@-N=&?_&7XB@2c&WV9agD&nlrC1(*wfVkeq3@#&xgJPUcdJe4V<kJB-#TbGfRMHmC9Sm{yvqV<Wl5k_fUjjobz3L-6He+HWfd;o!QyfpbloV0hS>zrT_|yB-8!qbF5p~eeo_C06NEaC0)&-@!2LEBhYo6`--0Vy!>UP!gT?=3M?C8?54mY>XTMNNrYrNaw{U6rKs;pVy!LOCP)bXW0ISvOKO!Wpb5o8m1ks&+{t5A&YQ&BVa>((I?tn!W~ZMq`S_{1t4p^@7)l==PpuRs0%ox1(|cG0wb`{ny@IR108*mnXtjX#bx&qT{K35&?~etT$BmNXMD8_Qm==D%>==cm@46-_appCi}**VjD7@@}64`AFAkq;ptF=KA@43?>symH(t&k>YBVbBNJYwFmb<p)aI+DE<#E|4MSMA0Od0M0`{wXg(su$W<G~cJJS1;fk{-|AzZ3wJTeHXUg{CBEJ*;7ps<46e{5n|6tMm@%j6oA3ap{r<Qj8UCxfU+({j&p{fr>1(JpmRGVN#jTFN%Ec$_piUo0Q6BKm{Vep|U!$gI2u{Ld$32^mmk8j@e^uu;*Z8I)o4dS8fS~Is!hXtHCG7iyoGY*x8s;0EfefPDmw8qK^w~sf(pNRi2KmGRe9sd96x4-@R(~s-)zu(^eeg~e0s;;zMY^GMu)Rb6>{PEQz7PR{qA-4Kp>w!E^{b_D%8bgB|Xu}UxJ!x}6=wk#RuaIV|Dt{hEh!$SPKQ6=TgP!__!T$bFUDN{xa=rKKPvZ^PAESVF9CuyS`}VuqIbre8P!=rRO6-*_P)p)O?a<@OeQlG9qm*D!A<I%=kE$YrW8Pc}buc1~@%lAg;ccZ}C7Ob{|D!dCwgOuyxiOLQ%3>GE7ealk)uw-5vOp8UwAXr|gL@M+nk~5E_;W<yZUF4F=!#ktE-DQQd>dOpQP23e`IFfE36_FiHj`F%J@QYG9YjAy{1qxcGAxPSKBn4k*iQ_6dr<)&;9pIG(9-U4je<zOW1@Zs-}|LMhLzjivA^pJhSRsVo9UN%Uf|Q3$-|<ECYf@pOhofI2w5fxzQ_AfR66JXD0+aavPU9V>WT`tMbP1QkFJam`}9^brh5Cq7f*e%Kjf>VA`A;p+IQ(5SpMbv`{(_$&Z-Vql&Izg7t3m*XfgP)ivygY^IB{gjIM+tIpq5p`E!LSa<VG%@nGhZX$%p5p0!OZ=5#LR>a*NntP!&|?pcX=`D9qKZhpwj%}eM~H|}i|%5$V5IF-9U3kpXVT*B5mx0_F!j%;3P%~}tN-0p376+)uI)lUYDqnUM{ma3ePsXQ?~UMB4Xv_hntw@rRq<LXelZ4S8ffZEpCE*OrYawk5nBR)3>-c%d{iUmxO5Z_hbmVC=*0{*z(y52jxc%7gU638H#&SMzcmv^*|FVMX|iXv03{?UGKRdts7UN%wv#ltJ2*v$9VwGzh(-3}w%MGtAOswx{Y?ndLHIzc*RQwmKhW-%sTf>MyA+n&+fiG&+;K8#hV(v=ResF1Dsb;xTZ4iRHUjLi}*so0LmewiI+LS37Q1$I@&a90<xr%%=<J;J8r;9}U^G0^U}cVGLOEc`g7aVa(!kGh$mn7ZH2o2`-NP4Sm?ys7J*#w04Tq5p|OB{vU0-qh=mXnfm>ezpljTLLDyql`52cpGh|J+q<)>j`$Q77b}Ed%XF1?Fc(yQITx<5GsfGW}-AfSUDV3Rew*{sU9OLemxB@Pilc1l<&6V5onRBC5|5#0f`z|7I7c1X!`_*yZUX1Xs<UwCKAyevdiEiIL5l!O*UE0Vd9$08tQHzep9xR)GevdYm`+;s&BC=qbWBOM(^V=*mY=3P`WAlZ!&_&pGz0Y0}OT?MqAT{rek{yGSXWgt0Eas<jvyJS&7+W5VI{gOTtZ`Dj<x&&m2dA(l``*SqXIDC_CsP*m$)2IogHxzMV3p<!4g3wWvZJBi-+UHJ4xgD9_XVL`r{MXMjQ+<J}VEXU1S7tYm;Z9L@?jZ;EUMp651&LI%SdXMPM~WIW$FN2JTkXNC$lRQKW-`OudK<f$HZg?c4~$UPs&ynhM6BMv;*Ti5u@&Z15(2Ot#9Qsn7a((M?++}Q-k)LiwmS>c(Hp^YE$32{lnJqbs*bcpt~mmK{qCa-vmV$G9DJWDc>$zvGXv&NL_%EQxoDkD_++T-3wFJU?b#1#i^4Fa|Lc*s?+YZ~l<6-LcyXc-{Q@{QBrcOE4T-D&lT<o}P8O{?l*a+CE555+V+*=9|tog~+ZTGZT0O(r=Q7LT@Xef|)XypRaJ`e?#Y9s*p?Q3X;orRD2cu#z~li^3VZO=~Y-8LcV}<xPS*8?0STi=+_2M2fqtF3q}}Bem1(rv3F?iSsR!VSZICi&DJfJh)8d)ISU%y^y#(&ZFJz!jj)Ja-+o$wJF*=`{bx}90q#US*-A5WOJg$hD)xd(m;koU-1!+k(LgO)u!qxM4j;$z*v`FsX;V2EnP-4|4~G#3(kRRm%!AaP8ki3tz<-1p?>FTd}u%{YS4UmOqhi6S1{q@J|qFc&byrm1OsHkYBDrymydQ1Y3KGagW?O4qi^K;g>7~djuuj%>P#M+%xB4bz<C*qA#{qy`0k`^@q&;my+cT<nQ3E_qr$XxlV?zK-!MJ!WWiseKL9TYXm(;8O|lO6>E=myG4s2b2`h#ATmu<hfb#3a+4U)WZ4GUdw*4knrR!qSNBBOc(%IW6o(`=X0{}>hk9C!S9Rr1dPX=LBa8d>Bh%XOYCscpe9xI{&T@xI6N$OZs)C!Eu$&-5;6zTvG&dD+S%?!HH@g+Hl&tGpRVs~F7l!asTHbId#aw6<Fk_$|-P8OSwD7sUUUZ3FNq?R6=^)mR>0IFEfp48R@RSHZlbE@(~E0F_e+hL&)r?7+<Q;XoVXECzoWy%*}&>z)p7Hv*T^44#?joY~e9a3x;X9lHMr!G=MGsvP`L%(G;1Xmp1!z*yFMih(i2$v;ab5UF!Zs6+Cn${+-6BmW5X|1l@7weA<u6W4|j|hyp;cqT4#OH6a91b1-Tehrpth66kbxN+#J>l`Vo$5K8mv-vZr)$0SbdjOe1+7OC?6*@fncCG=wj^y2m9)y1Ax-oBUHU=y35>StB=7gyo;lvv-WRUZbC7LQx=)m-Rghbm?E|CdI@_RaLe+~`?68W6l*!Q;aV>6LJ9(#gYLn)G5_g{3qeW$V*qQ2hYWev}QVZ6#Q@%wo4hZ7FQ`2E%D;HT=H`lU6@-5Nb8dMBP+L66OyRxtLgs?-v;<<#=k+ic-=}<*VNpPHih0M4k%`4^FQl$<;Y$<t6JkE>P$n6Q?(6N#ip$)!xftoxdvQ*3!K_*5v2_u8anHa;M#Y2=g7wHWI<DOkJ1J4BjInr(HMPtC6NfrCPYH=WdE!x7ggnVaj#Nq;y3MC>~nMcFQOIMuiCaIqy$8I5MFO}W6kDZD*{)xLJWE_{T;!ACcl&pG*nc!H4+EYolv^?KyX~fc;m}*F)E#2Vtk{m0EmzDwy7v+kaObOmboRKGx#)*?x@-K=V-1;M*cbwJzjEIv=ZC%TPmRGhIYvC^{baMU5$)@og!<qXO$)!VqN+u)`5R9(~Yow(g6#s|^28OYGv7MQLeLTR`=oaD_mhN;Zcpb5qUTMVmH6kj)BV>6NMbU{IL*9D|u$$$j4|L;aG{cxGK^UtnBY~1dMD0vL!Li9xr2%8tYtZ<DcxhnFeF6NWJ5fvf^s0lHO~xiLxmB68*pb%VHWRUzZqD1Md_jKbZ@S6rTm(8*f-gN*3bm6$D-ADou+z)4*CcN}&DtNlXNrfW+iKUWp@Foau@mD*k`U8vd&&r7;RNzFgHh~#mIac!cKp|d<>4X?w`YwD8Gbw>`nd5RbE@=P07CJs%%ui`T7JlVbmI#{;OVuI?=(zFxr-ur5pI`1K@+KhxN!JNte#P@osy?8U<N0q^mx|56YyL`V?fKZ4RENamhV9tLtQ%rqFzRr(9MLVVYAyYxk`#m6N8Er9wXZG_yBlPVNDGa)7E_q3(XWyl{ibLUnLVvWFg(-Bs<!O(b)`Ld>DH)#A!?!@HpC37n*EjnbEN39}H*m`Ba=U49ZA6fQK0}=0nw6-&w`a$;2qF{^r)KcL!!;v86Wi>1JO{gzL;-ZkbhVjuMQaQY|4yU`Hqnn*Nx;c8*ku$}k=oI<&<4rBeNr)s|5gH7X&_YcWWjziI4g^4O)s$>N%DS*M$8jwEXY-)bhpkbBCe!8Js5WISxOEl1HyH@?Cmp^z3iSfsWgbjha4E-3NEU}-6mIxg{|`m&hxp0?C8jg>1MQlU?0vt9L;nUvlh;}29Wt55m21o~CTJgq$uKdSzL>0Oj{<`GdWO7r*`mnm$nya|qO-dOqhJ5Op!k+^BvT}%Sxg;^6qPFl)zv^cWj(`=LYU`8JBU}2J_o}{hDa2@Q>DNu-QQbb@q@TSOy9n+{)Gmp>LFGWIzhXGz-NK>AXdSw%oz+#zLPiq&Ub2ra6)<JUDG&zHM11OHhREgRId)djj?lw$`bb^U2eh){B)})#q@cTdZQRjRWT#MxrSCx-7Hqh;*1}ef17UUn}*}uRrWktSX07a@vy>#xW(y;N&7HzSGZWuim+np$bYp^t^f_SabufaW6WwZ^L>2?z|mZx|_OD@wBmYk83=m7u>+_jQw@wDT-?!sDxELCVTm148)X|qv6^=5}j2d!msJ!>Gp(U_<@NgT=}M`^X|#}Y`CjU}`8EaAd#os1^_T!OHiHaNw-B&V|5>3tI>NZ<u5(+{Lbr-iq=(SiT`Re^skcY-jAlF0oF_B*6*8={>f!^|&&8OI+i@r-*UN8!3m!toW2GBts8S|&Te%({5ETLuU04AYOqAokJ<`)I2AEN&Xz0b*L73Do>Fg`i1C6C4vNcn{I?<3!Ild`SdykJOXT^~iOau%;$jF5-#UfgUgx;FRzzpEwvg8#(iAWTk!**<YL?W9J4<gM_#dZn?;3Rv{LWk%*;T>MEv_&l|f*WFth*e!Zo;bS4jn?%Zx*KhYi~1WOp{hpHz+){GJ9u4Br^nQkv7#nU%87xk`FugO2G>7#WhyN4yMs0P^K`_q}tb~;?^Q`@lzFd}e>)1@M-^?H-V<E^zB;XNsf0Zzs8R5VD$QfO5#dAW{pt(_qsrFJlJMk3T2UU$~BsRH?2L=BH9R(ni5OZRiRcfdgwcbV}(WJNDKecSE14(XJjM<a0s8np(q4Q{<Z<GO+ov(+`;#%+AM;kil+(I<x9aUu4)O>SEi_C@*XluUyqjK-Wf<898PF^48{`6?V{vpXr-N&`F~qdX0xJ?*0?$QB8f0$^s1mtb+10F5)86pf8I3&2vTItITg2!wTaNn|QW2M(6g4<L|j%jm1O$;mL=&`y!uvGEPLcdV-4ytUUGuvYwI2D?$$z}e3@$w%0-rjFM!K9z|S&$m@h^6-zxxX2Y8tfH7owIgcY5qkSd-G|jzImvji$WqL*tD|e8=qZiafk|Y#N=5JpaH5#|8rTaVQdNo{bg6-*KBlTa<YynAxjAsY47$C1LeC3%H*~5QNaCY$Kxg6&cOn9-yms{M@@?=n{f)t}jn@t)C`dDe=mm^$^j`gwY2S4d@Q{f@?rU~cQp=7{;e1mR(g0F&t(fxmqlQ}DK>d8PJ16ErUEb!+=buDIKUcyeY%jP5gwPSD?CNZ1+4+V`0WVU7qg0DvLfx!27duK(U_9UEj)gWo3sMJ2h0l(W$u8~~`0dBY+N`*Lq;qt?xe`1<`Fu;oiJW0tsz6xG2g*0It7ku_v1T5A3Z+vZjsJ^u<~lju$8fif{w6;#l&^wN=G)#=!@`*KZB<KC0MspF@yKF`Dt)fVNho+ROIem2)kY{mYSMRm0}X>q(qk<;_@SfVj~-zU*R_2)aJWq15Z2!M7}?Y<jo|r7{9W<_3K`%G=Y2iQKBnU%HH4V|EtR#>CEDi|=t#S?AYBwMJpNlm4Ah@-9W1Q_19Jxkv(yW)HEc2uYiDg2Fq`%w5XEcS$FY6d>0I(HfuO+Nzco7Xz;3zPOo!-yDzR3*>2pIpTh2M}HiI#xI8Uw331C}uvm|I(wHUfiShp>369<peIP{5%2pyltb;37}IuE+mVIIenV;j;=Wdxei8A%7El{O8b9-5{Ja>jyi*r!Z7YegCb01|FftKE>JD;+~Dz2d1%dFb8gB^o#60K;6=F!3Em3rc~wL}w*kyu7R385#jC3(bXM_7Sg_4^AI&8#!}x9ygo%2*?^-HJCB+0yYX*`d#B#H+&k?!FziaEr}oOt{;s|=jqmYG+S9wVkY2RS_Bb_GaM7>&;iZLi6q%9t(i<u%7Gq8)9tIUmFYP}&_q=b0^~yUg;fqHBFbpYTD3O-FAT7DP>Miin}b)deAqk{Tg~__%yB8%7KVz3VIi>n<;$g<+R-EzK6DADHJ4IM6d%*%n-H@hfbKEw%|~HW-4ft{SlKOISvF65Ua$|bRQx>J)xA}fdn5-s-}1s~5Q-obhO~s%aA@b@wMWlxY|ld@yy`iDpq)F8v&xFPEs!EMoX-EVw3NvWxX)&Cj|q*h?UD{k2S`%T=6TLbU0%`BxMM8ONt#Jiy7J|<%9vDKn+cGr(_<vC=fzhoPSpf)%34GUBySxU`|6$mPVk|W+l1L?iYexKb58(Q38pP7z<fBeFG<hyyubGOV4bCCyL67mhBr^K^QJzZK@>_xk3on5x))I;Da5*|2rrUb1xK~w237VvMmKVypt1L6H8EPvFM=E6qgVH&XC+wF(J?3<p;Z@~(K~Ub^{sNZ&cL(GojE&((Xt_<7QZ&^QpyuOV)7+Sot<Ehu`Vxxh`y>_>RfCI*-Bf+$B7tM#}b|`GGYM5N&rt9<5k%5aRo0zVt>%6(X?3@Bgig$e#|Xe#D0mD0*Av|Zuw!g$TuBUXQCw@@}RTbfo?=L(JH&vIKv%%>SPxaKPI&>UAScMyBPc^;4|_NlKBsoYMed#S>~0o#k7ZucYAnJK`x2`mg3tG;sf~-a!E!280wNR6x@A<AqUdHdyDPoW%c>nHuHzUCLTXsCO?<WVaQ#gf8qr)!S$!e>e&;!+r>}7In7Yk@WB^RdvH$ITf+FM!~w4eG0X}KZb)5%Eai=@1U$4MBnpN%+B*(~7EIQd5^-=AQdXLR;z4Db5HSmq7K*JGS?8>I9FG>zjvZD<GXdOhRJs-nF;Q7cm=3lq`tuauRpPlVN25JZ2tsIXoi2WFr8a~RjtvhN-K)(T4O6Wyt=&XIPS~T;Bx0f{V3wnE3aL<z+49Gq*y(yy(nOBh3+%^?NoDP?!uwNVBefb)CpI#E6*jUda8@YIE*Wqn{)8tx?(R{s(%d2^#aNWlZtqHUBbXourUU4vKLr`tWRI7L1jt!2{)*Sn=X%bL(a-+qoAp)l=yoegFp-ai0n1&)nTf##yY(>j1Oyv9V%AhLMr{IvQ<ag~;*=2tFibrh*M+ELja1&kmG_n^`)v?Q@Vv;Wbi|DwaLf+Hl7s>a<1T=qD@az#8=?~%GErE-R9{E!U@MIyPo+u4?Yyl7Z7<CC0*qgxw&beeS#_T~)J6)L<1_?KwNK}5AH@~wGG>BP;xzCud$+=~z;32WQ>ndXaa2VL7}b$7TD-DDGN*3R2v$U_l$fM|q`w<GGY?5g2!+u{l*;S17Z@Vt2N(Xn*!sp+iD>jDDE}e`&A^z~{>ulX06YU0a-h+xROu%%omxKw5tYP*YSdP#4iU0wzlhv2R?9TEXz|UwMU58X?zt_uo1Z(NP0SM<YQo^qG{ka~1v_Y*W(!gq^nCV#DmNA0Lc^ccbCs%cwFoDc`b#y)V~W#LJ(wJ<$NYzmajx*hu$@zwUxyrNxt1p|q;gXaFsG4los^hS@>Q78YRq`C-B+uuhbexAehRpsR+pie1@;96R*!7!V;Q1eExb6z7u%(X)iLb7Ti_<88If(DYz%$4WxO|zGC7q;F<XWtTFNlE2Z?Jqb6PobLbGxUWw2?$OtW9A?j+2&Pko^boy_0NX^Y|%Rwa@%pk7w5Da$~K1n+OI3VRufoo9))mzZJ`xFEyc>b8X_z!>w@BY>3CGg9|xY!5kDm{!+VHXY=K@odjlVe<NkS{a0hTCpUYa0!T|RN{4ga{COGVYdMhT0hH5=TOF9)qIyqYY9}=i#i%o9h>K)WF_cJrN`7B*%mo<Mg;)Ic=H)1V$Wkto#P;Mqcv%qtNCev_e1;EDH&YG$uD1ovG<aAr+``lU4|di(~&ioyD8(G$cbjv%juCmx2Mw!8kHUeHxn`-TVVLv?s;Wgx^tmEUDYe`<;k%yS{YZn^>J7b2>EttaL4G}bgce<uKxDFn&MMNzla8QMfd8Ry3v@+Ed#`bham!LmZsKk4;Nv&+5YzfG>LF4kDdM=d+p&Nm<IbQB85z5RThSHxGerL%-qvVBd8o^oG0@{;n+0g#Bo4$1s^oGCWP1Hqmyyk@$4r}5)Dr9g43*vfk92>HBJF1xX>dIx%t!L`pHZx*r}vXw<iaK?dLlAf~lTdaz?hJOo@`yXKmH1{|wDxPgp82J=cGwj$;y?kupxegh^iB4VGT1KYfB1Nwp`DboYgsS%RAtTn6W~l5V0kF5+-ey&~P-3yf__SU8ZDc#I}7;Kewjt%KpJ^RK6g%r<$Iw)K895_2x00IYK9He`?fq`Mu#IH&z0!{eX<e<jJpI!~PwYXW1D!E<?XXhNaZeUW-h?ZBDVjH^^cDw9|V%rWNe8RL&1LXET3A8bEPdnc(7Fetc)9ormJ(WPDRBDIAfPB*3WSX|V^sWze_Kcx&$sL4D*;Bf~08Rj2jeNu3^<#JrVXn75)Qo3}9naa8c{ky}P-KGFk_?>DeXMaDE4Z}UrOEab7b_=jpSvZlcM=vVj3c5y?zU~;k#bQkPR)?8o?ZC+1FL{J-iYMTE=~>Cb`~9)?kf3OVk6kgQl!>n%P_GMizt#6X0tb)ueA(M`HkL+>(gz=Je6q{!1--^djRm?7lT}}m1hNbrm5xnbNyv^Qkd)r~{j!X<sxML;$+v*w(ozzJqcqTCN|UQ}s(5p>W635-MIp#<gvvBxTjp12qFOyj8AHlbhYB&prR0!%WPsqA3@SQg?WAau=K^4haugUkd%qYoGRJ}?m;sA^-@YlXKE=mS`9<N5mj_MsKJVF~t(FA242-MiTZJ?{8N$d+?fr0!c~@ay;^J*bLh)sn-V|)b#{?>AD8>>KtEZ0!b#95aFc|e<+PuPJ)JvoO9~H;C_FgGVIrff+17aDtR|Ful#A1$NPn{;usNvsun*vrE%J8#e#Iw+`k%SkHlpzuGCp3AEL6;YZ@7OZMsd6kAUpVWmlol23xBEquomzh?(9MCMHHBa-E#i@29N)aJA`W+?T>My%bqRvEc$v0T4Q$kMTgdc~KZ}qFY;j{Ve)&EFPZa<`5C6boGbSVh_k0D%fAa;9rH8?EJo9on1}mkJyn<FE1V>Vmp6@iZ#i7Y~8lx<EH%L3Nghr0QL`OO$Bx8UTFhyqJM|;C$0n9c#*3wlC&9uh>Z%0)`*e>3EYQ?u87R%%gL!=tgSw0@cKAXx<1MZG!&LlePT)Qdm;pcQX<J+3MvIyM)c7co>Z}L0U=a2{gK8ejYH~DI4(K=R;!y+hPN_(ccGOGH-vuUfrWagSk)pVHEe(Ss2L>ajU+VHxHZfJTR5>^&xM8KsG*%vUyBp^*@BlVqa&JrtvW+)S@_J}UueM&jzef9hAHcBfFK82tvbu4O6X8&$chIw8KfM#l*h5Pv~nTrdW{PClPy2Z{oLpz_u$txW#L}ZCmby(fbYR3iErhQ0LZPCiEx)MpVwmmU32a@QM0?vuAz!mDINphnvpP_NLUFk=Ajmf%%jC@Asz1Hko%n-OLFFrD!j=tVMCcNBu&`!x&<1=v9QtM{D#V|g^l#I?)0g$B`Vx?<BqhE!?61#++l;U9Za;la}CyP#mRhW^UGE}gZHx66cW4qjDUxUqeA&4%UZbGc8>jFB+ax+rdE(+5LNI8Ix#oif%3##TM{IS0O`2P6{E|rqj`J^4crr<0UlDix~vdXMv_ngCOKYeX1+QJZ?_$X0q0+zP<9YRE~+J*{DsZ8=4W$SccJL9?TGA@6ID9zQv`ug0Q%fXu;wO=AhJhM13!_D7HuF3W0=f=T&qMSpLel@D;4mr9H7ubq{t%sReRYR_=-sfRxZq@@ypF~2W%E_cUky$gtsaJrA9?3Wg&a^}j6yjzsvkSXOXo2t`S*0pGadG&y42CbkDCE@5qiG3BwgUrQ5>L_j9W5l%RZ^26#CDy4HF;O@u>N7|>3gZ}ca{(H=eDUpfe!luC)Qb#cTaf$L=B>L`s$+Ir?SiDUaNXgEiZ@>V<Qnw{$@Uo@u+89#+xrL6&Ic3|HQy7lXTBnRi#$e<CiMZnRsY2UQiahJZF2~DOnyKC+Fm4Kphzx=7GNqFtcTxddb(e!as%BV%UwLS9j?$AmQ{acET@y>T>Skv#Q(&GPO1^-SiUb*fJK^b&<G**|=W8QT?dfF(bRuoQYLZ?nry?V*RU;Ju>?_=G7fDrIG3Y1dln$%Pr&P*1jhK2wyXjjyY)Uu~hP9mMWIQg>vHBy#K%fyWftTuY|^W)Ugm6MMHTZQRsBzSf;`6md?9zxFt1=Zex28)96}st`VO!YAN6yVkS1eHBGksGCgceHV!@h8WI8KGk2Oj)7fHKS2}mo<cpnwb-TInDijm5B{XPeElZb#m5)35;i{lRb%SV09W-jlyb&0)w?zB+Wl8|=jC!8#^_UPVZdO@oq4D6H@wr7^N=rIAx2|1Tseaa3(P<O!JPCFCvQJ8&#Y?3`u3{-~h`%zXZRG=P=Tt^J-A@RA5n6HukUp3RhEH#szZ6QNH$m$LvHf9Hy<svhp@gQME#>6oY9jq5E}gc{Ojf13@qNI{pYxYzC5wh|(njZvqPKiA(5W%*&b6aE8Y46DO1)V0(oos{fC`MBW*<{4H&^||FNGt=mH$3S4ohg{d=JX-WXCM#_4D#0sT8yniDVjZDx~mNd{b27cJ+iz=IBzUE-q|~?~C}B!~_gJpwb;nrRK$$4(f8}3G&Xc81#@JlS$E@IxF`dx<dT$7Cx4FivKiBSXLTdO*Oyhrr_#Y&>%5ZV_z!KE>fp&B?JW{nw5chO+^lS=h9Y7k!)gkS}DlOWOH+ZRfj#_#G&1NHDISNEUuEY97pQ1ILcZ^+FF5p36&c6-TZ7U@i7shyU`G5B!=hp@QPl^Wi&)Yb=?sqg}{y-acicmr@l-b)l{xPvD3=leN-xOD`>=0oQ6W{oQbPj(=AJJD^lq*!vED?g<%}IEWY{xMPg}Ddk6=C0j;7U0}vUwC+j|W@fvMnNI(DM``<mLE8jO~qa{YXfZC6scg}fiqyhzlD5NqCO-uN#568C5<&5`Mr9{y>@Tf*8&=gmG84I<s$jQF8O^fzN8p8bszTM80;yQF{8c|}X-o`lg*9rbVN8gktU4M9)X&cb5=j<oDHCUn<)skpIZd3v+z(AWRjbQR)bU=rY53$bnf}FleQ@;6b>2$$n!_7j%b&>NsCu0PIPPr6_${P$JZY0`X{HttzORA`$r~Y66{M#=-|Ic5(AMXWgr_Oi>$MDos=?FjAYBdReNo8IU{r^hSJPl*B%QHP5Pvo~N`D3v7DLn{>SR!cQ;s3Q`+in>iIER$!^O5j(Bzfi}*KG+ps5*ASwt<15j$*Dg*Kt!N&Lm@M0U`mH6=ca$C1I5)(-kM%y6lBgHy`t1KfdXc9Sd<`y3D8dx6Qtwwsv=nI08I87S&{vtW3dJbI9-5h8Zicg|v{{2HciE{n%q>O1W5&K@?{@Q_X8r-o(6t55D#EM!@rsvhAEVL2grjHk-{XgC_*#;2F^e^b>o3Ga7+CFr(8`+!J=0E6wL*b>kYdCs7GB0axFkR~h2LZM18>-u^riqD)Go@-)5cce}H(@9mCBjy*Ray8q5OqKFzix5!Pf3Zoiv()5(4o^G@OX8mKzZ-4#k=NE&62Igw|4#uQDfBa(@r*O(X`_yR2RQmYl8R^pCe_Z}BSc&wxyy8$>J==Xh-SE9+l5d~w{q9g`LknsDasOrbQBNLDf<#>?wL`rIkEXra61Pq>^kkQ>+TWe(k#4wdMu-m+AZFkEGD2P%%or%>=+{201{d#R_B-3N7vA**-lGP<jlaLvT1zaq;yvLm4qx4rU}!_8PTzi)1>pg_ci{lX47?KbKuD{%CRp9;ZSphwoTd%23v@_$su~P&_7gi+MUHSi!e0VIE4@MyI-Uy6ELQD}%SZ26h)%X$*emNzl0a=&ko!;IPwx+FxcqBJOhE(pXp5L}yhnDsbpa)>L3b>{tMg5s&&|#Rnr^=u-*0f#x#rjb`k2FTbBl(x{v|fhyIJ1<;i-$YnX{|&f?f8tk_|e()F;E?=mH_cv;^$qdsPRK%CHL09JZj`F>~tQtwSa{r5Qj|kX{wiFf{T5R)TrqAbz_BG{1lU^{3yzQ|Eu*9)0Rx-+uZ28;$~<RCW_^9BZBlk7?2s@$3Cos?A0{A0QhmTrb>nOAKuyTKD;>bw`zHPJF<j>i_F&o?>;k&w+fm>%7r9tRz$Y{62<@ac0VY)UHUit;%1-@TuAZ(C!Spkm+RVfBy2XB+2^m5nj)<$9nzdBSKJIby{opUUu(FJ<9*WtxE06*5ACYy|~ElME_;F>V!5n1+)A?h5zH@hufbYJyfNl8OiUJx!g%nqM<7IL{*W7tWcX#yiP!jVbKp%R2+ztnV^zWNInl$<s~YdizR>BK980z>G925cmH%GPid?{Jd|B)q1O4YfGJ1D;VC(TP-&=YNZVw0U!yx~tc+m$m~H<P=>O%X-+sQM{y+Wpw_ktyah?A6+uPsoSkzEd&v~Xh4S)&11=mnjiQdoD#|W|22U|~M@y}0lJ90#K+Cy#0wZp<OnTZL%ImZZ~U?HtmRRBGV5G}lne_Tq}2Wj;WgZ=%Vy0`}n<a+PdpT>J4KSlxVIPS8Y_wDZxn7I}a4Q0W~pu}F;0$I}TRp~)ERA`fml$4-MA<I%=kE$kvW8Pe1buc0f`}(zA;cd0sy~f!E*&0No`EM>8t1%rGNf4sCw80X8Ua~+2!nD_Vpo4o8kj_ka>%rXs=w{IswJ2Ov8Wi|8wt%9p@hb7lH-Cbq-<Qp#m0XX66J!U`j}c)dGKyoUiLNcC7HrsM34FWkRt^YPlVGs4dt9R+((jn4-@*5Oc|imA7w+%+g5mV-?PmIAo)`GE0PnEuuJo(x2bvMh;~->NB={chM^UMq|D)&uUI$mo(^YM4i=o5s9$ncW-hRE-h^gLw@WoS~%n$i0sQ|;mllEP@2bO>N{{DIYth1`S6(y;;!NuB>C|V4D?BW1t=)4x2L!+yqNDldaM*du3ikz%U3OkrNr4~bkpJ#0oi#eT(x%!Ma7;D5tj(b)jUOpL?teYP)bMwNHXqygEp*%+_f>XKsv!HN<!8>fNbG!LG>B#1#MyvIp$nD;SS0N-ST>WIgI2u{!X{qW5nW_`hu}wC&m2TcP`AuG{L&<kFE+Wir>ueVdlTLgxKCUA^HwfNT90IBXOtBE(Ro|9;-&?MdX?g2<@9dIxf=WmrgJe37VQgRC7C62@_x>n~Ottz)`@L0}S?YVO{>R}L53h(~Gv6Dij2_a(!!8>8dSz7Eka0KK>eLC+DVtLGGdG+_m+rpgq+nRLErGcc2{-6`7^~W(D;;7{AzSn7q7S;4Lp+!fW3z-yDz;<tU(_=*+G9^Fu&XkLySj)yow7FR5%!G+7sKX`feDg*`r6lI;m0YBYp=n0)Xgj!yD2FZwnmya#b4I(rmlAylc>ms{wE5R+&uhvQ?Em!qiHMt*(MNe8JI|_TBni6+h{ZGnH4oyPq1^fN=Reb<IT@&N7z9}b77;$wQnX$1ca5&ab5d#Vd^oW;+NR)+NKt`LHTYw9)T9A`o{Qi5zwT8WfAxBiiSvVxU1i^hc+_<WFismA-fDNf@7?k-SCkWEGDkGtfB7q;Wy<gNhy;Gy+&Dugb+eO2jGhoY$%N0$6>Hb)0nVyQ{~@e1d%_Nu8ap5>^O|Jhz(80_84TOuRc~qGM><z#ig?nv&SH2TY8p+n?6-Q7=fQTjsm4|DE6`v=)jS3&<$88(t!0C?LynCP8rhjGb!9!OQDXD?svhO%ddX$x^@4M(qHNspb*D+w*>i_G1v$z86XdbvjWbWB3psyxlN&v!SI%nAA=Yf&v(ud>GGnQp`;D14md_W^yL9X%TRKKdL@L&Js-!se+j@N4m{Ue*Z9lMqE0RcAXLdx<mp($?HIz`+4RR$V)e6G;hB-4jUVv|HA%uf2}iedsPwg$9Q`fXWqGWcKU-uH&yq}J@)*YUtTCm!@Q7~nA|q7!+T-3wFJU?b#1#ka4Rq_bYRFaNXBzB*6-G^IXc-{Q@{QBrH}QOnZ!=oGBKiO0WYem8nA~K2!b34lPqtN40w~FKq82rGQj<vzhQ*`pTc1A!B`+jGuRfY^l!pM<b5wy8O=<ah7OW)B?3!@KZqwS!S4OK!LwS>+&IW5&(<1FdFp=Uet4p&k=Sc1Jx@mtsSK@rjWSCzS%c2zTI1esUIrR@ibT1?>kMn3Zx3Hx8jNEAPLv4!o&OSLR9fyJ5brvi97}=a?vf+}esWgz`&{uqfW2B`6W3{Pz3Q=eL1u)j7SEmpSPOF*G%zqS7>Vk8i+9fb`C|yQ_V=Ea^RjA*&8Xp=EiyAZ^9up>E{1r_2xDQEyu=8#w0>J>8u$m0b+U29&L)y80%%J!R<mel@q+y%ggrkMjr#h3zCi7V`A8=mAVu+%mF}^z~Tf89TO79SoYG&Hl<ft%h-P9S>+&4@QJX!FU=nue40=k<RN0Y3>eY$zlUCjJ$X2MFLKG#4-7ohw)adv$QUt2>PrER~7Rq48z^bx+#sdV-?il;*>#{dA5;$vNvVaGsW;FCcZ6`WK-JL1d3UJ2FTwa1F+MVmdF?*~dnt-#2fJh`Vqp$-t?oE*d7%%B?`Uy_sf{PlJsc271!SvW>-6BKFZCc=&*xxggrWU={(q8laY?FlYUYU#0AFN04Fpo#_UNo_q)rNHDerz$_R5;=gj9Tp043QKq~wFpjo79(q3rhE|w{ZZX~(dM)yZ~fNWxSd<jA;oraW>AWC>LN8XgDlE5^jlX$aK+(0yaM-XM6n2ua9Q#-7sZw42Cg2hX>Ia4aZ#w6*6PZAv3|(likHmrh`^W|{^s&ReEufO;n4BFWy?y(O8bFTr{oIV6CRJ-v7WPeX}3;&y4G7yHyK)8(0U}nemfPDsa;)VThjJWNvmub(lp=Sr5|*kz-X&Z@}95lndANKec?Ji2ibF_`$UOa1-X^kCNg@ivklrNRK0k`4y%YrnH-G~*W%W-lXr@zHfathap$Q$T2!`&ovDtemY=UAwP0O4<y!>ffFKS$H61p=a*>sFb1h3G-x3|JLB)`y9oajyEBk6s2s;EUo=Z3#Njuw=4ppR-1jh+j$c#JEyi%?$Rq7zbmXgQB<GgrH-<}W-9V>Ye+8vA+sL4YjOT}CfWMX8KFfy2&i7^aXJVbeOk={Ts?%6dn@LT|pBi+hgG!e|1RI%@?76$^@qAg5I$anTeEG{6aP$Ghrc{HrNbj8VTlKLrf>=u&tQrV6B*r|x)pSVjx#&P*7zSO2j$*Px_365o`J(YAz%k#aKMl8*VsfIM#(hXiC%CVAoX(_;PQLf0zl;CZ|8F>O}oH%(U|DxEztv~X4$64Lah&ajA*0n5Xd1Z^S7XG3_C)cl>Y#QG&oVibtTsjn}WI_@F!T5@>Mq2to@sD_5U>M66+nE{I#{*oAZXu3g>E@S$*AaW^l}3zTBcdWaLY8My6rIR1<h`c=yIEfPKsSCyGmNPcgt5vp5-3?j)Xo$X9Gg5<8ZdUf28}O>mj=e%7r;-tjkUB-uR4g?WNZSHTa`(R9ckTdGZA~~=DdB%7vzWjrklLZMW9n9_|jvgP&+BK((qCTJH0%6P4aHkto^}zrg&(&t#-{C8b})&J28GF2{GNar;IQbP9SeH7{%UaSs<xv$A4{D9xl>wd)By+;m0GQj~fp%r%JyCAQaEaTxuYw<%iryH@+|go?aXIPQ#RxyC{Me;dc2GG?6NZ3x}`7>KO&wDR~M5W^iIkk7o@$0nb%52DCie0Edcd`5vS()U`t(>Scrp-Arg2HoF~@tE9*@F{nu4F`_+>4}d2X*3>XDZQaMP&`j}EiL+$-RWiXu7ScUVvZIX{oz2k2hp|UPoW_&^kE2a>p~*&;84YXx!Eh#@PsKUIpp3)=c$gt$K2*K+omKptOpMa%Z*I+ccVIRaTWT|(ZuZ4QxX%3LmRZH-D8U#i)e>R^c7(#9>5mC)=SY>P4C9fZLrbh*D%DR}Z5ee@qY~o07K7CJo5r3dk6lWfEUpQcb-KCcNU}!ot!5$&xu<LzTth@h#=}<IaumIE<0~u@3TcspMQR&Dmu#Bsf)Za0mX;!^;}S2bFN;a<X-hrRSh><675a2G+f{FwN$Kq|{y^oj`jmf5pkIZ|)7lg9qv{`+-bGnw9udW&G>@NgnZoAEo8ai?jg_Cj^Q4v(iJPX~#Uwypm^C5fq@_$piz6#O%{GY-X5;}67A9HhN!n@**TD{*0)^NnMFiFZZ;EW#F^yU^^Z0!IQY2(}7~lnlH02qoS2jTjES8D&w003Xck^sx9VB;6lQXC{fZ}LOm8eaymz|93Zo`yFCz#0M_i(gmO{(buzyD(&b<S78wOB53Rry$B1KnO~pd##GLH;qG{R<3JR^%%NP^6mFOXr>{4I9sF(H2|ihS77e-H9@|21|n~h}RnZ8r*YLM%#dyZZ|<=d5Sl*<T5>B$r(9`9st0=T`Q>;Pdm=*F04h!QiV2CDK^`lHX9{WZ+4h;&{`JPvj*}Tjftw0#GyQLlvcZbEP+JXSTbwR5-#l4$!OxwB?!xDgHzl~aw@x>-Zx=_1YW>0{XmLzT6n7)9r({*75LY3CkUe`iQK<nzeDP_A=)`I%={vlas0s&&$vf&6t2r89AD8WQxiz1WwH~@tc!=cWpKdGF#SjjVlS<*kEW{6;-=9ZAg1M+K+R862%2;>!7)3n^Tl2gVcR3o<a749z7p0%M1w^<5j(5{rU6_Kp3@V@K<6H3o_nmcP9kfI^I`0iplOhRHbN;E`KT&<Lh=u>kV{>&bh3A2r${lwE?XmV_UkR(r89Y4bmw*h`-yffAy~plKU6&tvSy4(cO6q!&vbh!DW1N$xu|!YdJn<Fnm$^GItj3(71aPce1AH#*-nRReQG=Q07e9kb-Gk!wO((sc)YbXBfKYNF~F%<o{9#ESPHG`C2!d=uC+7dqtp&2&Paq>!|Tp^NL3)8i>Tod#cGe%Lv;i$rz!6paFE4aW;_sC(aTQXc6+WvIwk1QNL+zNt-)-ATkp@fu3*G$b&a=i8=r1?uF^vEiJ^B~h`nx;+g62rQNB7Q(_jgsF=x(roAYSQp^03+3WwS3PD-}Y01we9Ps3<W`zQ*sMS`UOm|5c`SllH*;|wQ7qb1G)uvDs!!LJGeVclI4nF`W@gXQ!C2xQwb`s!_RGR!u#QzUn6d_(RXtLisz?ezw%75|vQZqzk!_A^fM5w@(U<8_QrWg^A%ZIzQe{Nph$as>ygD5g^Fh?;kV-o8@zVf9r`G9E0l6tnE==$a^cN~3sS5}B@25j+B%DCWKf_CknMmEs3oYGA34sp=2;*@tIt4xBH8ZZDtE^FrPYooWV>`1l;qnRvsUh`=hZ9eule8+=WFV=!#vwSx%?(hMPb0V8C+SN~+%cijX$WTKG!nq8IDvg1=Y-xP&3fRtP-ro8>Ap;k9^Ki}-miFr_$w|VpVCy~+5l`sk03$6hnbc89pI@?)xzTr~9ixlA~)gqWsH*3wsj#3mD&$qc_p-s<%)B#fAvtwkki#rB>`!TXMEAAiZ9NllO1W!;t-%@cRXPA~M5Ek=+^3Ck(+0SXLnTMZ3=@dxg|012aPEPkR+^wU($qx+Wt00v5w)fPqFeZIl)zTCIb&FU$vKXRDpDS__3SP`omL*5E5lWDn^xfV-!{CziSc?vR=qUK3N7%!4ZC?%?E)zI}wYNS-Hg!uQczzOpm%M;N1~|icUk|g7>G((uA?ANeWvz6H_IU+5(k?AX7sU&Y{}vGg^=DiMOY6YE+=0O?^#W`So6N)7S=$B7ro9M6@tXE=Y@c>ImwZbgD6sc$jZQqUTdp?KA^M+6tRa5Q<&~e$Iqx=uF{L<9t<4EwTXVA{Xjruvx=vWPEpQVDkJC8xiHZmvpT~8=H;y_Fy4GPH$CP6m(oSUrn$j6b2c(rY4Iv|%rU`P!f`ZtmOgd{t8U+9nZd0q>kfSRdLoB`GsZ4q3-RUJ7H{<}rT+}e}9YzaEfw)9xC0)F{tKAtI0WAy7g<|#*ua^%_A8;Evb8{XyoB9aI8eBD)G4TR63RwDG<5)L*8q>jhdloH;AMCCljZEk1)_F8rSy5sp;9Ob+5sEV$6X?(Z&B}=+*(|M@Oi#*z9!S&etFV>nIYrP!RS*K?LiB~z5-1|dXv|u*HvlgTuy#<KKxUhRSFn88JQZ8b_$|zFDcKf=iiTk!u>IxBrJUN)Bo{t(38podQcM&d)8v~Fvmt=)G49PrVN~4`;DA`!EnQhQPkUal53yAIJlfU0Rh4@r2Rh&K!f6nSAQgtRgw}9q=i#+S&u(nbLnFNEIf0;^JC3u;in=Y3A~u}P|Fg7|$ql&AW^#`Sjj!#J4oU||Qqbmk&P!ch(bBkMEYC@rNmRP><+aL~R9u@0kgC&TB(UejS1nG}1aZn*L<%Ht9T@xSo&Zkpp_JQ%*=LF==6Q2Z09Og7Eh@l#II=HE&-1*$_W59)rD(f!j>d*JPqFi+KA%ApN=A=Chyl76Q6(wFx~T{+l3N8wwc-X<_B=*6a-pEH_hvOQTFozl8{?x__oQbfSk%!mC?26z7n{*Lai&%0d(ObK%$+$qhS9PiqZYq5>{7}TJ!0}DOr4!zkFhQ<fr!4UUFuwH3E4_p#>a^mSH}{bEiz&N#YzBA8sk;i@^J+(LSlc=sL`}p7$e9odw$F<TEu>dl>&#uT5kDawa7OeR%fCm9`c~G-GOdIHqk1();Pl*ed=Tv6F(-kFkQH0@VglNDBv^l5R&;1mTH_m`dQ|cvBk89i+6i?Qb8_?0hZ$15aI**5^_mK02u0$FcjQ<g&_yhz<Z1B=VkTz+cxuu!6qI*T_!)5&0)x0qJQEAGQsty$m-b>yW7Q2z&XuO*6_g>QG0Ms*IUB)sl)-V2r<kG3~oqWf-L2Ytpq%@AtVZhH`+T6g%(WKm=bYt7E)H4g5p7Cn-DPzk`{`s7g^`5c^r=x(2gBeM>7H3Z&bP#3^7qzN|+9|Ec){l-&NwdEk~n0PzXY3Zk;ZEZ>2Vb5RMHG7u~DP8x2#fF0I`}LQdGD(j;P{C}5VOa|)?Yj@k0ZpV;YoRMJF_+6(N*j7eqfufqFNVk5O0Q71Mseib&dDR5RO%`O>mB>sdaJMQjLvC`ZkC&gHl(QfZbbt9M{2c`q)rauK4*<_EGi3G@5G5(6z&*ys1j?vHl=$rLb^5}LeN-&X+g#pW5#F>e~1-tby^#lYPJ7U&UGDd9zgHx4}+2WKD1TaiJ9M^@YWQ|nb!j<=yD*J5^OYpqNsdU7R9&pSK#gc>q3*#<;p({vM${V5+8!}N?z*JvH?O-d7BTuDC#qGSU1Z^+O_X3PxqPFC!;aPQ`JJd!Bn&UJCO|?(wZ6C!I>M~}6Q{pu6FnhPcv%qeqN>i!5W^q(S3K-RqGFrT{Lo%ms(g;>Wtdy9ffW*KXJ2MYSNeG3}N0iFzwHFv7<p&r3zS#Q4R*7izCMf?R2F<{j*Z#`~qyRhv7IL7`t5oSHF`ZgJ0}++Pglg1QsSXjcXupWuGFHnpw`lRryhV)`;_kUEx0|0kpiRsZ9BRVg&@{wylLb3yoMsDB8}xkkfhso@-a^Bl)pM1qa<vF2mikLI$YYArQ$3g*tjGL^j&ZK=#IT)Hm|uq+X}OjsFr;!*4=|^ZaGjKxQSw!o(Q3?ivE5gztcNLng?<XSpH`Qlm<9F)1y+x2>th+B?k&7H#TVP9h}ALdy<6ZWr5TZJpKJ_$xMjRIjxsrwM=@K5BwETaxCe=AICEM#b3(In3uUlrz)Z7Ws_rDrw@-bc44us1%xR0_6jmjYGoW5puPMtwi3IO&t_ph@ik)YPwU?M;6SyG5-s-l6D8Lx=)gyqE(=$@{XlxHTSeRDVST-HxhVg9A=3(;siCP(ih+45EoNx(<rBvc|eRBH@m0`C55n4aXO6O3<U)6k<N^1#J){8nCQXQM;qhuxMOQpxu9@!Q-bw&jM#(47?CSuQHOr7H(bfYzCoU8e1fA>TC)+rfW#>p>Vgt7OMc&C6`0$qk5)6<bPm%AzBoXCl0)ywITKDVdS3mTOk1ve8iAX{Mg+3tB|T)K0iK3&x-@#V>}Fj^T`yY+Ec5D58pX>iBr+;pt|ey;xZznbDxM!$##c18E<ox0JO%PliC<$Iv^X&55tChV<Urkm}5KR}ZRxANHO@3Ge&9)fAGuOd>&WL9NiNQcYfAH&Q&%`}3_Va9nfPZW+#Q%)QQL|5=Zb8A9)Jw7@aryb9J(j?K~1TQ$vx)>PLR9@p0aDodx0+E|PEv}!;q=KDF`gFr`FxY;slP{R+$t7oGJIa(OIepevz53749QK5z0@HK-SL!$>(HSY@1WcIZ<=tTEmHN{sc#%|l5=nPon3*NGS;1v+PAlmqTH_)P7u74$?Y+R*ri6t9X^F>Z5(8e0Guk>Bt~&pEn#gRES7}@CHzP6U5(>a7mu^G$=uf)a5sY)%FETt18t_+=Osw<NIk6@%78yL3Cx<2!YTXy9$J7p-Y0bDwMWix`mB1Wh-kvf3_#xCdOZ~z2<Ft2@3IT(Hi`cQvF%@0f1us%t7~*tON{_`wO`K{YD)Ljx@PwMo69gV-z@I_=G1eyqhg&Yk^^2C*pem(HcbKWHd(gi-yxDCEK!x9_c5?RjBiS(A6TLK3DsHy`Yn6o)*?RP%60V?YWa;aU(OWFWly7yIS=J7W?ER8Q_@;OQzL%brEWF<zTMr3}R`}QzV@jF$>H+n-VE0>n?;~*VNY9tOJ!fNS)F^%M@x~{+++NUYjMP}5`!HGcB}pL5&{65w<duZ%NCHXet=})pXsh}n#gTjqC@w7}VK_<yJ*G6dN~el9M?02ml2jCe{6?ruBerFJg(j-igOo9(JawoLQ(Q_8xkm;Fp2?u1L)K1;CV4IZwkSt|p|kgkK_hc4Sb`a_==bfL;_6d;43%FL?s$37MDO#S9olM1kjuchdcIXi!;>M5%+%fw$C!5&_9ZUfb|e&EcIi#QR(wpLl7?a|F|m63Xi(>tXbXc;52np4JVw1V>i<!3tZVO;vXo=*csL-IfqO*&GD|Gx81~d@@{Ah(jkhUarJ)QzJ4QSU9UDn_;Yb-0F@Hjn=NNQ(f%uLsQ=BTta`A<;&Pr)f(SEyMMA@nJrvlv^2wGDJ#?m4l3C8iw`zqpaKSFYsV0Q~xJ$t-NTdD>&YPl_BddQze$ON{yu^GR7pMj?efS`weV6hn!l7V}^g5$sW0?5+CU^<?8xg3L)(nwxGs}X`DDM`<Fn%d&fWIT;gmb@FJomfI6M_{5Oof48UzzUcmv+$$6VX^>bn;mQEs)lCT<AArLDk5wb?>@ESTM&z7a)%*O4e2Z&k7A!q<);C6M>J;=opr9=6!-9RI-K!s&0Sf9?f|<$Mvgc6o$7PI25i1{$wxwK)Uo;-7BGQ<@0ni8sK^t~rY-)GiE5%u(_uyXt?w!mRpTB;!^<eTk?4I$SXrC^0e3)TU%(WT_%oS}lykNzO04FYfl92nBRcB)l=8#-%JtuEP*xm#ia1qbSk#`(cHN@t^1K!RtJFLT_w!vc7Z)`7<3|lsi=A->ZaxW%SF%}%w-RUOu$Z0IeG9Bj`);PXpp{)UA(CcoJ6>kWBheOxg!A{U@)fv3-84yV^yM=&?zSuaXs<C@mynUq$h_B@eTx|aSLMY=#?#T)`^SWr8xPtkIct0d&RS~SthX4(hnSMlnJNIXG()U(O=$G1a9CoO(34UetX@vlQt4#TiLeSY(o=>C*7C+-OM7gW+w5zw`91~FWz$WFRdroJ2U%`LD%(Y2IsqvM(6QJ%V{k#$oP<Bt_aEOspT(t8(mLO`<JT0Nr9yI-<40DRmF%8#Sna2;4NhAa!V@1QicP@MHorrNh+f;+fhm<qexq!i4s2&U*Ifqc?+~TAT3BD7n{zpM^P~1l<m67H8gBlUaqX=)KL-xR9px5MVQw?IAxGljvRN@)^)L^s7AU<*hLUDIko5T?^r)QpY1d9oy|O~|pvA#%rqO{(qn#Tkc@(eGFuOR6#2N?>l2xk0lNjR`%V78tj6zP`JeroEWIHg>CGixU-_c?uT_rUMLTuMrS(CRKkMke4p1zmr-e>tRe{P!!6zH%o_+p(UdH0kDK-3^=r>`#ReJZ<b?zO6i*7AZFF*Xv><dDnb7>|0!WxV;~QgP8a{!fh5GD-KGRaI(bJ$|VoorxzY;~ize%yYK)os#9@adJ*x2Gr%DVIKI)05e<0sh50hEBsT4Er#6~dUcmB0}@W(Om@<J51&=#K9H%kf$64~P{)?BxUP%DEzHLC3XbYW-HsXAmF7&Wl5$7da~JDhjqH)x&oQs=m?@1^hbnl?L85LMH@EgZ5o-9Fk#x*KYmcRpFSAs!6fTq#*XI2PE@ebZr8Cwej)lM|8sQ6tLZ=zWG7WySbl!}^t*Bva8{2`HM%SQoefXqJOa1N;O0nUsX|mOq=~-i{ap>*W*a<M7xzp^K%ofYS(z%-^U+j#m+suU*p_q^@VMjA-S-KRge1OW2Rs}t(8*NL<pix8SeZZK#CA!BiQv!Eq%=2`s$AngKv&u>ejmPGU&MnGPS`yN^b?wSZ@w3i?PMe75DX80*eNq7}UMi(=6)Sl|pq3GB0~e@LL1Wo|LI8}wk}H1nK};}QdfWV^P8z)lS~rO84=d^ob9o6NH1%vLCnr}D=`V5Vv~^~(D$|Yc177`{zdS2dGz612GH(>T<(q*{jd6Fb9nH}gmx&kZ#hRCf$o2<PAec|A)!E0C%gq&q@hjxWG3LJya>f!dIp2vgJlRN#MFYGlNeT!pMFN}#$_lCe6)zQ4zFj>elVQ4)sf#n)!u}%eC9wi)qf8Y&mP+J{5g^p1&ok_u;WB6~K_-)8Lv<GPKQxQ@;YEBb^A!JSn8&Q7y_zC_(PY7uyP&~iEYiMIT3)1l-^vpT<}|Ag^LmXO_RbZrmLf^U@U&9wm#OLIbgT}0zKKJ-`y#<kyI5R2X*rbCm2m{OjBK_7{}SRg?z{QfZ{lMjLXM+h-bifEYwZ=ilFMjli|YC$$`yf)JmQW`Sr2}hI;yT*-D0Q1z5A$Cnpe<>rDhF<+&Mv4cdT2M;ufmXXN3Q&y$Zwla#?&)0*cVmTK5np0s~q_p$6bLa8K5K^5Qkx#E^de$M?T`1X#Xr&PJ1T<QxP~OVmK;JT_98f<YHju!g29{EmoYTm5pzd#e(tXdQS|IuuBaE5D3|;8@~hU)#n<`y)Hyegofbw{wm|r_>Q;mg;ScF#(<T|8w+B#nSbMmzlN!{d&%RvO9()dQ>fm&g4dczyb`kohiUA#^`_!Ax&bP?FBh~m8Q(|-IDKuJ&2oygzJK)j4q(n2nL-hDiD=77((1%w7vLO*%6miTSHI%zyA5RUw;0dzkEO53)W?w(GiZ}si)G>gRn(x68@6P$Rd9BmA!cy#%5P-di0*iZ&#|wVDVGB5f0x(u*JjwYsa?TGW2i`HPh!K;qORJ&2sGdmSBmhV<&7I7zk=K=2~+dH&vQVGNu+F5^z~T_AFH?R%ta|ak8z;UMQpUF;Dj6n?6ai5ErJ)e0qP|?CWf6cgKh$z{6uvP&P@{6ht<M6OV0}kp){w3%PB;lljw+J!Yl^jRi?WQMofkzBUz3%p3UNTTjabJP)bn&iNGNHuYz-*^D!ILQrm=5r9COvG+HlKiC6dIz7cbVVAjzea>Mwt}%NOm5>u~^$psUp()%(yVmRN&m$q;q@*iP)4P7RI~)7n?wI7*a}%Qb@0=rwsKIlK+ytv$s?jV>PkHKTQX62_Kc@Wl*S~&#F*s;ouBPu`OzQK;KZbGYsqC{)nT8Cek8hrlTn+xm<qw0ENT16q4z<;@-S^WC-%BR>_SyCC4uv*!k@g?=Uxpv`<l!Vp)I&8Q0vhW@d9?M_mcn(KrYF0BA!1Acc02{uMMA9jan757Z1&BsL*%8!jH`k!iQ2m*A>|h1YR4>gdpntT;Cd17QBUC}R#<EKCYG1+o_`m^uWnf|v>_uBV87{tECJriaDZb5nhDw}qy=FUO!4(L`K$m={f4*)IyOAb4Td=TNg=DsN4PEFFM*+zUX=<Ri-l$u3jxcD)C0|2Z;~!*JBQq(0)KjcYQsfcJE9C4%0~;&w){P^#;prFc@5rUDPx^)?|g1{CiHY0+xU)y??If_Io#Y*Vl9)2t?_Py_kScb$L2)ZEb!siN{HwfhR=?};Rb??X|34D_o_}Km0cA+{}!b?W=`F>b;yLPG$m*X*Q<(~G(7nUMm~CbzkmPrr{BLfzx-(T`}PPa{rdLH_up^?=%ld^3`|5I$C_v2WtxRWM0~&HYO_(#N6f~u*Q@z2T=)5@bw?#^j?>Sv>;LO(o}ziT4}^TS>qOEytR!{){5}ShajMFH)UHTXuF74+c&ge1&=w86km>B|fBy2XB<uR|5ngY#$HM;RBSMs1b!2PzUUvDi_T=Aif2DS1>u++`UR>mNqW?0T-%HBebBKR%<Nx^hVfgc-hgm#?*MU4OQZ&qp^XwMTMGQTyGZ4GLL%C^H&xbtcBIz-ThpBU&GYf2B;pAQ7@|T}}`}vOb{`A}5e*Ni(&3u1<_#F%Z-`7K`oSuvS=cfkOJGi1^STUT_F(BzLf3WKQ_=eyA85616gV_EV%DIg#95IyHy(>OXef!bijs>WQS^O{**`)J)rjKo-^~d)gwTo2!#6M_?uE?4mlCtoJmqKL!K#A?J%pDX%1q7I^{Zp3i7>U|IfCqW(A0dj+B)?)KtI9>7k)cf?rH)YLuchLH&-M3s^_d49B8D~}{v6K6R0Uu85Fg*SyYh4f*IU1}IPZ9Wi~gVgetY}-=VHj(4e<TmkLVQW??-&eVI5onGIWKJ|8u^3bVUt-chXjbh5bFiH&1;k1fSm}JR()DZVXXzK-Ca}=Q*v8g+4^fFh?HQH+rqDichLY{`W)haVB*$zqIn_Ino72yhO_jtz-DI#Y-RMN#w{Ud2h*lSs>T)AwPXzaA`AMUb!it_{KM6vxyJU$zT;Lp`3{2gWL!C6g$HaLae-$C|^Hpx31o~?eU7Gwo=vmjWkZ|v28=gBC?$f)-J501gkmrtY&XLH2D6>R_1On&d;r6k~ww^m)Xd<$BAYAarr6WJ1GzEW*52xm{{6ae0sokFaE+QY!rMiI?{*}LUwj_13%Df@J%;(mW-NV>#4H?kq{5+VxkOsqPD$%RTxva`XzUhDi*%gK(gh)+RZ-6D39?B{ctsFS*gEx%%I2Zg7&mv9Co7>L5(6$fdRy2%*ABLvkP3z!`JW<w6iv>WRK4A?S&+s78Oi3zb^XBdd>BY1kxBn+Y?#wNx}?gtW@<DRxvD7VWBRG(Y$m*J7Yfqo|rZpPb5qZR{j{=<_?Yt!+c(bSGV}%NX0d9V6oK8Ao}j8l6JOucDmZj+Z;<g-fk{79=Jx7r$YY|#dpn`k2m$)Bs$Zz8f>k1ZCB%~g&l2HBQul+sgfS5nT8n7aZV;C90ue)-5`zTqnWjyT|Daj%@OuTjf36dpkqYECpB}9ID>G2^VDIeO3~jB;D9OsX+$3DNQ^hXi#=~8(>e!Ho`@B;@%7vCK|LyT^{=t4E$;RSH&wz2Kb%l^K1L(i-Uz+Km$DJ`@k&K>A68UtM);>`!@8QX!FZ9wmaaeq==?a0wpajE6|<2D@Hdf;?O1V-lYxGVI)q_$qUd-)M5bf7vn>Wlf?K(Qaq;cdT>QN+_A(O`!zrN+qV#d#ZPZ>z@wx`M;~>)_Fifw1I46|ZQk5@_;fW-*Lzx<NyVQ50cg`C1W~1p`)KT?D1><JvVi5e(jEBx~kE42(WH$@D48o}FO?V&U(3gLXe0i(n=IOlbIF7a#Kq}5!vt=d5nN^*{@Tlf@3p})*dsM9fOmntPlSv@=h;+tPx})s>`E<uSigC$W>~WOI7hW$0ur1Lb_QKZPSdx6xm}8LrAICMJSV`r)fwe?|ikYeytG=J48$j!7q}pdWaf)@^ztQPPd1Cb{v~dBWk~oy*kC9DMnJFQV*eX6!Up%q8$6yD$pr7V8nOG&02tGzJCM4SV!Rd&La+K<En(TuVg_q)BQQEFke*-y7!EAg*2m2f)jW#xmBD*9I8mdQph$1a8n#C8ld5;ChdMwmdlNhW1m~@b#d4dEm6%TR7S;fpBgZ0rlqs;AE+w{beHbqi@4plxkpJ@v}kDdzN=i9%kKr0I4=ONvNJy#XYIk9+5W1hyI8`Kl<0&Zt_j(mECfbaf`5zQkQc-Ew{R}2k=H?GM3G0xJbImJVYgrqg=SqFxj(Zi*wPErFeWT@)E0*rEX^L0wMmbud{I>6sWFwQMM&TNTP>n_M1CDhxVcl*H;N>g0^N#IIHsq_Li0<&?>-~X6JRU6xWDty4fcT;UD^ato?pWlEWWUIdR__%RCCpbvB8VrOB8lt}-pqa|i8`B}|sX-wbWwZf%1nTn5CeA@yB}CgWwieny<2;v8^7=W5C4<&>F`9LKaxrj7m}n_VtLf16+rnXVY-C+lwbo{**Rf<;%0yjR_}M4DGEpg>D8Ygp``}hy@+4A}C=H8jk>oIGp%pq9#Xw10Ght)qKAwHLk~mP=m|)8Y-wRME0`vx2Nqkx%q$Zdl+6Gg#xs}a(|4`Ewn;0&twjV>PJrK`ovFVi{-vEq{ck!hN>2<N}2@GzlCyPD6&N*KAs0Vj@=$9#9DAD(iWN~g#?$NxN+qvd*f<l2DGL(3o(y$C1V<DvYQ8_?<4^rr8JGjX!5GqwB_aSw2Ole7^6;v5$R2S#rMToW9I*d_DX|ZE+4rqXWP>;T)H@}o_$T9xSW)!rSK5OKMGUU$;_<k66yCwz^UK9gYWKycX^I0v;?$gd{-{dk#8ID9UI8ma&J1a-NRLUaP;VF&(XHHZMfTm1z9qk#|XIxn@?;86=RsXn7zNG=!ICpTQ(aHu-+CwuAmyfb%I!H6Q|6rXwt$}0I#qW5dp40#*(|zyb=gvg}*2N}ga#ejWx=#bmc1g8IzxtbiJdZdyQ9~wwO84Rz_vVW&H<wl-E@9Q~aAmR^VV&>YR~P_y8lz3xkulRjU<T&&idFc7ymr7W>h}j(sKbEV{6dj-m=x#&BU6Vv)=Y8({cW^s=&~hA>hW;tD)v++zmcyb-{Bz><7sngz;=3i+yGRP85VofIt4?<L?c<+H-Nop>daRg1r}Gny8u{2kgrvi<pOcxXr)A?MfRaZQ~K8(PRYqr+O~f;Nod=Xy3R!rKZH8RH?ympu78-hUh)B$#d)<wug-q!qKIciBBRnlB(Pxquss>O?8nZlj7^OY7$G2CaPx;?BIA?AMIaXOe-k+8B=r@+gF9~6ewPi`)N{~8_fvEHJ=cD|t-1hNFV@lLtkL+G+w3bUl9D4<jr10hlTtF*$9Rntb9*$n);*AGdy9huQrSfEOvmVD64^cue(=k><A8WDN-^z5URjzyyK-Tx8L$DZ)l^kr%A-5!V*6&J(5<1<<fW11XXP=iWzpC6n9ZJlG7R1&$0QkI^Sp>XPn%CS1)tl8$&Nbt75(HLLFXz9iPRivU5_UfPu!&7)|hSzMrXPyZ0v><B)=Js@lAH&fo)AK+DGyHHt0&B7t?Ki@)&@~$d2{`v9GWSEI&JyH<#c&?AQlgcmhzhyVY6WHr*CGF9B*^+98r22~^@l6~s)sIW2Is+Cj9F01O>1DFVi~Jzb*Oj)={~lWEb#Wcz6ed!M`;Lpkg}A<cs1$`7|E6k^Cp>M894qZ^*!LcNS96^?FXid28%Eu8FhK~&b)f=kmd^?*xH)^v4onG`^D%tt+qZ9GETk)l)sMT+W)EyyB_khXOxfZs&*_*tz@<h%__XQ{oZM~8Gnd=x0~=!UKy5k6^w8c19LMX5r^$TwGc#g!W+>YpeI2<>2ZK|HD<0^6*6s`*}Ef4W%X?FCSUlQqTUWMAhcB{4FMLq~<Yj}x&BpQ92((8l3x_&HVLM+~L#5G<O$2W0->))*%n3li!QfMMw=&~Oo#%Z)LicB>pL8Ru@XEE4iDf@nfDge&-xNtJx!-o|=_@Fp#kN#0jVh88{X*11Iw91F-IUfNV?FSU)(fF<yblI&1~VI&yXmg|#d<9e;j)$%2>aU~eOdRj?;%U+Er0FBhgm)<=eBd>IrJfnSM!q1Tg4~$lG7e%GRM9h~7{4)oj<#$-u!ZEz@6-G>t6cayf&mF(J9dKisY>Xfw*~h_N8{Q;FUOOz4uZGK>21_#+bDJ9Vox#?coTkztJ)ET2Xb=S${DM)C$2rXZN?y%0$*>XTC&Q|(lI>7ZGBUF}YgQhBBrvn4F_cMlEd(uUs1HChH(G0jLn^2WCpy_(OezEc!H5878?K8r8Ppq%A53JD^UX%UQn4&;zulDbf9?f+zx`PaZpzDStxC6r6(L10`dkaqAIs-G<gswcl|QtEAXZy&;3&16pL)ze=0?d%J`51Vx(QVs1z<?<;dEH%+0JJ{{L<Yks~Ku&H^s6Wbm17ig9Q>u#foC*dR{uY2`pY^FbdU0t%N7Q5+?v+3S@&zFmrWMT?u>bZOj-zW*M!_IPo09;9%+Zlyy^G?jG%G4Rx1Wr!7P8kfu6-MKKDmSz9z|buB`BVqNVL_=5o;gQXwy=?@y{Vrrow1MMEZO4Lf3b0XUW<J`E+C3XS8GS8hB9=E*tCYn;|@;flhViU(;do9*)O5t}5*td`2;yT`>ffBWN>~Mz<D(MAPK{sW!i8YLJM@5x*V}Zyfq@b~Sb357-QD;NaJ<4vEIDzkmmi>IMrFNLLR#TRh^7hxi9@Pvlgk+Y%4bU5HYEiXA9SDUDP676!$T%??Glyu*+N{awJFfsUX|%{=@S)^>XsoFZ-dqE>W$F+Uq5IwnYh6wntrj7=H^*@2j^P4@RzN%^ZA+m48F{%<jOx*q5yMm@OTQ*0<X(UYEE#F)hgauuS_v<V<p<%)M`aq*vfA!B@LWV&a$EK}%i=ivUQv)y=}-m5S$GR9iIVmtkWMl!Pr>!;m)+O@cy}00xuXF^8cEP5=_03Nx86FE&DDmzxrPOWXJwYPJusD&6xYh|DlXddB4Iv1GDlgN)3DZ2Ly(WF{qx`c8r!sUDmc~AgZa*gW}R#S1ayQS=S5Tl`j3i3)3s8*m2#A@xSqxatnHY=;suAKXj&aS#^Bq+n$SND@*m&-PJ6$76#097GY@gxLJ~de;>($!vu~Ug(d1FzPqHNt4Lm@*`%XW~fEdB(x1{0pm^)9xu@>P05U}okqv~v-F-<)5qC)2bu=yRpy)w=Ah_>koPF%>jMwRl@y_)qwplb^zgi$r*EvbI9Ud5in_Nm5AXFmE@ky|I(Bc|*ZTBh`krfup$svJff#%B{nSnUO{aW->|QH?Lds48Hll80gln(QKEwtwQ_OtOpmaO;Mz2A@o1=u@>!453LxxLCaJ!^a23tx$R(tYey)6thDY0I@!cr854@_EaBr&DXNa=IN?O{!1l?#RZ>CpD)qI++2Hy!}T$rT{#Fn0l3PUw;%&>Sy_$7G4>&`7tGp;zR&}^BXCRKjN-9lyondR^$I!i>iaP7q{bwInD@!A1mpgo&kEtuk)JZnl`ZYF-O??=ioe1r80voTtYPGw%e5Y}DYgtZuaKa1J*H%jRc{8<RKZp)GBlV&FNkErqbH_C;{BS=Fel`C%e!hBVM*-L)`=OSQQ!Tyi3%P$7SXGc3Vj5}$`!o7UL*6lExV}mc_(A@ib^SSAwHMQ^3Rogl`8sS)T|1F+rkTkK*bytVeFAlrf&!y&$qz_J{XG4G}cqG^cP_W^COmdj}JapV0_tW6ITF&+wl9G1<H>*@b>X)!zl9dUyn<(?+blD=1PjIJ-ZyoYP)?sipGxu<D;dsZ<Zbbm~*up{`!$snp3w1K@892k|Ia8o&2b(Huc9|Z&t>N`89Av>H+n6P(9H|Ide}@;@o9Q(V88Lvxvp<NoM$pvDs=wkgBU3@?|Tux+?^G{yl(Mds;*)tzKTG{lCCownTrvFTh#nTUXT{gH|bQSV=V7idB!8^AfE17W}*<dJ@(M>s)EGF*wh`lt)SFqxH`*y%4~r^DwxaX$w7ai*6|b9C`1<=$0UYVL;j;`#n~36ohy4Fm<aSAz?07#o$w(Vhw6`iLa+|C)CRQh??51k0~hD<ve7x%b~L${rehAQ<XX|w2QqdLlX`WBbmT3OA33SR)CYv!`df$MBz1#0B5wdTL8?6D6q3To!he|FnGr11$DfV!{s)rVk+q2ZMNIhyEvf9@Mp3TMv?tlLUin6?WT%{j|mv$(052w+!#T9K6Ts@0z4)$>Xk;g2)O&XMWjl`!1M0jv*Y9o<yoXx^eTutf(SgY=P=vtE*LHwagiATUN@TqHdLN1FJq$lv}l!9uLdl*d6eWx8z`hPK@M5XK;Yx*X1funx5yIIHYQNms45x&PqKhDN4rA5ML@s?IZ1Nbt52YE$Dnta%lp$4K_}T1PG>ctjM`!X@gIP%5|la8MsuZQ=b!v`%ZP}bov;Lw?9bv}e|+UXzPCUA{rj&!{r=qoSkJY5`{ny@%};;e9QAL0fKdC|toyz#41_xNWO$}IAVtpZEOxc4_g}Qs{ZB^2&6wPiD)0{g-&cTa({noTf}$w+Cov4?s-q3#*K!%_)tXgikNE)P!r(3&gCMMaeKWZDE5X1v2}i=<&xZ^a&>B7MRmVF;jG8N5!KZ~Z+bf%O#(mFmdTUn~OvmWCraJIY*(|j$u4H@ddVr~HJ%#InQcC2lnCk~VDe_RKJ+E?$$hyAL(ly2r>@VMS{g_TA2S{{q@gC$_CDI}}bPnRS(Q_sF_rjCiaXyrRiZX4JZ^x^x=Xtbs2Hq8bECl5u0Ee+?tV2fUH@QcTKA5&dm9I9Yelt9Mb6!Lpk|Y%amp-Bi?L~MV>7JF>s<G4dF)Yl5cox_7^NLnaFTc&LpGm5DNwn$6h_3QtZpo(%Zgf{w^O)S~9!mIfF>MR_T5xt^#eW<v#^Qd%5J600ti%?{`Q<ETsxzuK%<EDJ@Pd(?X!!aZlipwZ@Um*0(9@SIgyQ|clPEV^S+1koa#RQrJfJKpsAS;WJGc^nw8By8Ab71sXlIG2?|?n8(G5*$^^*7S8*EZQPlJ`N{K#F|!^cdg+>ryibm6GM-2)oXQl28+?hbhN(vf~H^V3b|NMj4yB{kP2^YZ45Geu+D>5li!E(+)5DuDTppH?%66!aO1?VsHDviz@xJ8QwqgwUXic`_Wx6xq{dbd4BeRKx{-KDEgGGc?4qJ*86!mG>B*ubB$dcuF^uKz>o#duG^zrC!%gaK}rz?RmL%C=ps*5`~_~+^|&Qo|mChqcBkp$hx|5Ie;j{U&efeXJVW&>5tW?HB)h2u4U@cUd!s&F$tJwq?qrsm~*OYBw@?Fpro8jEU6z_SMha^0EN<5XG+te!YgRW@Un1gNd{rbL*Q~P<ETHO*lBYjO?7=j4|153wHJDlM4!>=e5a5x(n;+W^venr-p{+Q4(7`rXvocmYZM`Ky(Mnl&vD&7c6yA{9Uc^nHrx=7cFbhxRhI+)h*B{Db&6qLps(-Lye1SwMCy{mS*oHizUP5CO};>(e;y#bn}V2AMdpoA+jWP|{h4$2#(fvRdYae7xR}T}3ICBN&1zlU!({OjyLT(GPN0d=pedH>q9X|HU0ugG*QACa8F#zzoync|po58V8je|AANAukfOI)9;nC|WOaMZ^`>Ic-J6*6!?~~NvMz9s55VyZ-_T3273Fqzh3b<?dD!6M?2?EhLV#(lL@h7~XsP@I(HX0Ob8*SB+$QPs;9$KlFmwY6pwcGTR@NDZV>XJiKZ7*bu35`!qfD{12yRF4ao~p><+KM<|F^ZGGgb43Sl=W0$C5srB5G_8Yx`><{?+^wkq;NGjqGX0{t{YQ{cdG0gXC`0~W~;%X!?g=da7%=c!J-4;oO`^f+_>tXJ8yfcAvc3hoKk61bGO<QnJqXoVEe5@5msR+BJ5zDFin1NyDhtd<;msN#x3yhNRna}nrG<Vu4K7H7oL`=qROOgkdSE8=K!%iqpX!?)rmSU@=j4=C<%4;oCa2e7Khy^MZT74Dfm5o!TjzvS^BO%ucrdLDc=o^IB+K{c3+{e@z2%Fg)g1xO0Ql@Ddg#B#j^GD$ihtYg2ad|uVlEtIGf^?&`!8<(h63BhG-dwp~9}(8ZDbRJASuXO`Ex|z%s4=$)H(o?#V4TU($)|0w>yi=TRLgNK|gJqVt_gD1dy}TUd6hMjp1BC&z7WS!-Mrx!gvr6WkuCxu=TT2{If~SVfw1U*&R}GDJ3YEixd__y^s6S2ORCmsl#{%`~WYsWP3Ll-c-NkgwcS7QyUtnrSlfF9!8gVQ#6!Etzj`6?3NHI>Br+3UW&&KS@~6QRx=R?_@h;sQTMd$wS)A<#*x`hy+%qT|oqGfQjtg;(49&Q(pHUl7TXVs3ojiDq1_TSM!Od9%&7bQCL@o!9D2iK&TM1O7V$;R^~4Zc98=s$Cl!ODuA+D&JhUg@v$J2?W}Xi+yha_#tK$>fl>Cr-A`9<VFSm|jiyg3u(ys_v6F^e;?U?8!JY-1mtvndmBR2EG19IDPxkbnm8r)pa!CtThiM(8fHZ-9q*G}=MToF5!Pa4CMV!S_$P_Ft{`3Loi?9G8K>Scyv{@{?El_W|&w95ZI_58N;|63L$mV%bX=<tDHCamy9D0%zTNi<??!6gc3h`xBX>qofk!W*o7vHjaPEl*!Rh3#Qflj~M4JXsust5NU-7h0p=Gs-7TE;{_HVF7E^4KuBCAuo-d^_q<2QF<`#yLTBU^P%8OAaoU`>fjAlR-fChAJ5>UKc?IED0y?PNBa;68ylGTJ=4FSdL3K{h_^_q(@60MxNaUS8b&Nu~63fa!yyZ_lN^oUhQpQoL*_JFZ~$hg!WKw@mz%MIc&29ufKq|SjOEhXLM>ki_)=5BAC&6I|?MehN4)en;n-u7#Bh#sk#s)1v-EyASIS*uy0vXlh<xx)c=`s6Wfan3^?b+(1<*h!g;PuD+#6A7U1NXn5LW@A&BUOo}J0ZQiYObl2}WEz!m_|M$<>87YPQP;f*5R5#j5x+VYT-;g+nFX>r3A*4e|6&QYF4*wO+lcR$awr-i|rrG*$e{Qh2SzAWIgmQR8buLV84ZuWB~d*VEJO>b<<sK;wyezcU@q`eax1k??ElWk`_BH;<RBt<xR!_GvF5s8GDu7Kcvm3j0lBgL_$B9SD|<Q3XhyD%lr1yHGa1P(BW%N>vA-SEn5AHSuXQ<?4h0mf9JWf49&mVN%Fa~7rhShU((U44phd`Y^c8(Axg5>z6WOhoUqHt&EyfK5prxW!8Lu-5yoDJe@N3>IH9u0|tCsD?c;z}2<6jn2Wjv2|p@Q3E{5<hz*DlYA%2XI!+HLEQ2#xYN%hzy_r34r#YiWLpsk22UwU8_!Bv+&{^RBU2onQ?Gl1vDh&Wuvd3+hf>BD68y?*Ag|KZh=a8aiXO<Al()G9e+iydX184u4Q|~ACHcSTkc_(@7RAX#>LBqBDnXPs{1HN61o|n<)15TqSdmfRn7~5xIF_{o6KxWNoNnajak8G5$j_9mhY(5&O<m|h=)6?^onc#)s8RMlb{LP8mArOi2EbYB?TdKMY`MLlGc)mn(G}?w8po;3_KYn<M|FOa4HY6{J*}GwTowvEi9Gi*+MOtns&KwhE^h$qYa+%P(`A`lEqlfJr9B!q$xO6ReY!jID+KCU$OfKNUOU&(tGX;Dmt65M8pW&-Z&y!;>d`Key5EP&xnL;z{VLJGCyNMSnzTz}kzXZO*W_dH{3dZ{z{5Xkxn^(T`+jY;fYxPDyq%O)G$~jmglHJ~gq0{H2vmFIf>{nNq26E!;I$I#2#KtuBN@%Ji@4)=(+MeTz2SMKB^jR_1!}4HOpvh&H0Mo+UWJvyq;s_Jd<4kK+!I}5(jKpM>O5Ye<d?LYWIDO^>=_fRMDnGjl9Oz?VUi7|z&nvv&1&kghiS(pr_pIEuHs&A5pIM6I@)_mH7}Z!=*-2e<f}++wHRd}mj@AXidb1vabsA`YkZgj4wo;13G4OS9GwSBT6?z$NeoSUL7nd^{S(SwYn9I<VL2Xgd);X%ZDaGhPDq!FDWHFG1#qL12@Q)HLr(gfYsQHR6{9Bcnz*T?Es+=p_lO{$ADWz3<Lne6Zc{>h446!ELs%Hai)5at0N!TD?z$vFn4bhFZOEB_PKm5+#kV?IZJFB0NcO8!MMX7@F56<?fFj=a8@*nOANKJ2;K!_X8bvMTwmP=jM$7E&C4?>uinl{puy31hof+gTx*+q)0!AfprJD&z2db$%o>^POE9n$8ujg0&#`d@0`tC}hnc|^r=vj;VM~Y(JhdKW7-~agjJBnmZDWZKy*lC>>J3c<Rd?E{NF@Z3<*i+s6=q-z-K!w1&QrYrJfL>Qx(vat2eXVlfV+K>o+w9bsdABnFLWqSH0i&eAEo2Z?VxH8PnMWdkq=!B^4Gl5fnf79rvA0v{c#5kSp2p)xP0=#2Hmh(n)1kIw!i(BVl6{7rDw?OKa10!ZS5yY?tKHzw&NRwP$&}X@+pO_-QU9eSMH%aqbL9O}6oAqsOMqLpCFy8Yv4(fmiiB|&J%*!T;9`I@TO}L`hHPRvfL$y%j`(OI(C`d|y4(hzi;i$i)>oE;r-o7qYRj9NX$+T+Hmh=}WJqZ}BrWT;1hNGw^~v_TdQC1fpZuA#_>{Dk^ca_)RW}%JcU5ne+w2QF`yL_D)|Ek9RBs)X3^nfWax0lOp}Zux4|L@ac(Rk=wJtM?X^yEcFyni7c;M4w!$!OWk8!E%YXEH8YP$nW9WB`l)lp^yW8M7DjRF8+9Vh+%ryM9^#>FVKr*Yly3JC@g$;StuTXu7G1aA<L384`W!EY+jyNQ!F+<Y6L+N6ornC3iLHwGgpJLWg!7=&CdH16CDV=>Z!(yh;H=3{85*8|F*-L972GzMjd_kia|WvWxJNFh7C0P)~ThAca09MsG+IQZS(1U5y<*uc$Y_U#qST-@AHnPC|WCx=KbQa?2;%M^U^co&Z`FNt^a{K6Jt>#AK$<n^8IAt#V?Q<k_UuTc*3JXjMZUvk>N{2S1kguI$1|7vb3fTA;PQv(kf%6Csphhe-<^NxpatcB0TiQQ$V;8i&g?Ro4f|40#XYiGGV*W=AstTaSXG=Y}2NYZJ0+h-Vur~Q1zrxmYl#yf;7Wwu>uh359?jh)WLk$NX_7G7Rs9H}Q47x+VrX7=@O(eULs^;X^}z#Zsy@@9Fd9@&!cx{NRES+l%^@4Ae|P1Q<N$pUFhs@8pZ5h}|<b&b}JONY=U@NB8x&<pz2EI9xip1svqD|<7D|7IK4P>lHb32jP~ocTPx1VuVC0JRb37o61Ys?CTjJQHf7BWE5BMawIFR9kL_CtuOYikWP^&32bcAQg4~^HeASdYXCBT&bVh8=FS=Fyz{x%kv-`;4oZHP+Dt@b(-u3BGe&bNjB^w8EBm3gKy_7=1yr_Chh5Uc=9Rzny@;Yu1_VV%6J-Xvq@et$&s|IO)Xv0mp&lsgBF4<YRR&|S~PZV<fK_mk`T37TF{@=YrIquE>j})<hgSuj?09CXoZN_oZZ&VLnoV5^eCMcO16|Y-8p_K%&OkV+>zpiJG9$@`P!bBMpB*Cq^=5q0S5_*6;s)E-J{q_rj_w~7-k4b-xXnO<f<L7FaNF&m(+Hpw^Qry(XFN3oE+IIhPfQ`@daMhGi>)Z;xIZt$7!HNY-i~_lI&b5MuBRtCt@^76P<ingZnxxGKtU#;ZmJtQ#+m2bR;N~C?=jI`^Ccnt9IKOOGLE?3M8D^5moPb1^bwgQSc*!E;t5%YNTMpMmH_3b*-tH;}_z36~I?+u7;mq#ZQ=-{PzQbPQH+x;xJ`+vNJRbk9ncAt~P9umm*UoMtTR(!kUT>RJh-``K(%<)W<Dl>MB5Kd2Iqe;;}LXBjPusQi5gNHRU95rc)={bnc+4s3kK@v0ghRnI1aj{dn#k9t73gR8+AalUTSeljs5H>YUL?m+;oWfLB*yNhs}F1y`(88HuMR56k_eZy6nKFGIxoR+vKg7GOs`$Flo9I!HQ*)W0jYvb)iA9Sk_KuLiM50rv?(MEvyABJ-B?c1%vlvz?>j4Qy3MpSB47y}yn08P**W7!9$0-MN9%s9_CEe3ByW)Jv+!mu2dxB6r)6h=0}ai(4*^?g?5NzEtY4@X$%FKFzc8x)jKS6V>3$qLLS(?r~xh+D8D?tDE)R;~7jYi!WnkaqLMNlEuOfZgoEhss$`aL-UBkbsWHg6Hlv_U2VpBZ(5=iN2z6)rj)3s1}3ur*+ovR&=RgpCs=9>(wtUbLG>i~rK^%kYa=mK{T%nerd~5jD(4ERFY<5u8VIXj!Q%Z9F227~w>uoQ4xLJ(w4y`X0R`!L>a4G=RWB^W!}GZQ5UqtQUS&EM5tOsIZH|Qp7(t68n$_5{uS2<k!QtFR<hgaW*X;Br8+DEMx8BaQaIH<=T&v28ZoxHEMM6M90O^pH7opN*`%JBiO%~&Po%;y?>z{x7<>&wT%lAu5F6@<t(ve`C>e(l&=r^%^%e$8R^@gVN$@Fdx<7qaVty{seo>nNP^7x_Uq@>F@uah;bV?+u<k^C6sW<>Fj)P;7MJy{7Sj?~vT0`kW!5_J;ln7aLsc(q!N8Cl7fN-Ra7kia*O(RaF;^mq>EC0+@cUa{G&%a&+~!6P5w$2VOr3==*Dx6Lsdzjo8`!;G-XF2xSbM^+&S`ZCR?Bd>u)><&r_UB!L7pJ&xVMbP+Ep;Jau#4O<KnD2vYy!G^W!!we-r#Ms1;@aBN+H5j0E*=AXCdS$X?V;bJF85E)Y)@Dys}o>BJ`3ipN>O(<mGUTvGCZ!V%4W5Ze3ImCPiT0V9{Ak`uix!X>lGw$Ioq-4x<r>G1O$%n2ahwQ-0@2`Rhs0lL_!~n*TkGF@q<irela+jqKl++Od~?xlv{yDo9$SV*{`~RT+)*q6KE8+|G4}ig|l-I6kdZXYPZ$Pu<xf+v6rsq&Yv)JLv3sSasOrbQM7|h=aj4eio_2;&G=Xhzfw^)TkdYieD}PkdZgRy>Qs;UZoWc*V2i&wQPvZkNA6)&CC>To1?JhT4TA{-(#cv&WU{=N=Q+5!j_Te8LmM($L;0>CqNLDRyD<X`3C^<^mXl8fBb<Da3a_Vt2n*GmhjRx*oc-jPTMf$moA8&w&`Ph^m5%3__EpeGLvg7s<=hK9YrRSOyX|jsZw&nD{ecaaf9(imD1;Dg5i^eW$ZoeTq~<j^lU1&CzRB~s*_lAs?Z@f+4Nh&<9GLLY!fPFFu1E*V6|l2+x61oJywb1-GJ3?t2QK|uNh2O#>Qg;&sKP|oAXDVyd&$NW5ULb(uY4o1(5KLJ?B1<ICIaSN&e}{1co^Cjf;sVLiOS6m=&pgx@85s@>G$u{*Wb5CANtp~U%vl_!$K!_-^3TkB4>hYnpQ@&L2Q-lxU&~7NiAu;QqQd^G=gZM=cg8$m5u)YtNgjjsd|O>ir3O-Rd(te7J&`O!Us!?_v3%}!b=s-YCSN-nqOvsKK*}Uy;qW+{rCv46>`%C>^ignDR+7+YhAd^>-jI-oYX#S{avWr>&IVK%R3ptI!-|h_{ZlA<DZ`~R0Z+8SIX0JdqY)#jtZ|yjc!|%jq6bjLTuxvUq-p;ho%1JNsRP85Y~)i&7msk2G?xc;G_Lw`8(i?H$DHhSgHMLK#0@dt-@8A@CP~M^xw4Os%oUG#P+SO%&Ai%njAy2$66$3xTVX%@Ac)s{Pf$;cX0lv-~RUNPd_f#|9*S>yR1S#!ndI+r?%wMBMlSsJAMNSG29Ugk$y}XA2H3CdGWx5CY0BL#G$IGZmv&sWIx@2dg7V^7j7gtGBOHM8bub4t5waKHLaD2FSSGG!d{=M57O@+1N!}+H3#N%0QE1SpE#X`bzj|~ELaPiSa6#g|J?R=oWUhViqD=f^66Z3MWbqzgdVmoY@-0@ao)FZ=FLZ^Ti>u|6IVEXD2im|cZqE$!=O=+KngFRW2h>l>5$alHICQX`*Q10-D=BPD|5lMt*tW8<4?j8(8n#G_^rLD9)Ydb2Da8yB#P36LsepoN}F1$p-!4ONz|dP_I)$myhh}p+R$j9QN1Algv@S>H+q?$sT361SZAY)e|Fx&Hnmz?7<}_$RIxYop~>4Qz!iOJbK|n@Ve!?q>>|GGCT^yqN5TY}sOk>t7yD5#b-Layb<hXxR!lUiW0~_f$}(3^I*cL}xnGZh;i~wQ2v&oFI9e^Izj|~v!B_*rR<TK@*oUgh)RyM@{4P<Do9KKK4RP)RDHv(8OC6cR3?}|%#`vo$Qc<BJi#BOxiXUGbBgL^1(Q8KQNNFs=-#jt+DZaK?WO2-R?P$@_Mu93;@<?cWZ#H|R(IFwtTSK)y%Z(ej8&}nX0z4zcImKwX*V^7c+s&_z_)H;?<Hz+&!=P*%{LO5=HJAxR>kw*7ykb|kv12WH6(sqWIpSkzlieVzA@6@~G8KAZEq;$d%pL1P1)5}x=I(O6leSC|ta(6VGN^`N#g?Aa*#-!-I47V_4x5q@Ad3(;`asYmN=cH<@eBT~HHj5~z?$s+YXZnMAqA)X=Bh3)H)~mT5)18w;~Dxh*zMuA`okSxJo2}*H_?22`jk)D7OWurOcH0z40*PbyELLR)rTX1rmCsB@<J9IXi=RL?A=^H)a)$(*ta0a8t9Ne%xfO=Uua9hS@Z(@d}RTI##|nYaxRi3yJX6PY{+%wA13R0X|eSIv)bG|4*jC%hohEo?@PV3UKVQ-=QjV##43jYkGETAqpSvt_?(N`D3rLq))vUHcDxOF3pX_pl^#Q2+2d_=ExRMUk*!?qIFZ}^c$=P0IYOV5K%8c*OCpi+mg@-zP#gAani8=cYi;9Zt-$WXne3<!(v9BWp;OJ?fb3Z75k^QeO>JdXb?xZn^KNyYc{l2_fOT#u>jX|+cEl>D9gbA$n$Z^PEXhInY%)+At3oeuxk@6Ra|Q9{daUtz7~hUnNtY!v$Q87nUCS}sv=HZES@MVqP{FEi!ehRE^D&9ZZn{C87L^;K^bd!FeWA&WRs9cI+d0Q}h)R5L!CS6z`*m2y404^qyxvj_*l{TD$Iy7lHif7{dw3T`+IoiZehv7?Va;WoD=dOj-utR=V+sHXna9CkhlAIxW%&|HJh;#gS192k43bJtf>6+mqZwrzVYJpdGT!){d))Feuc6A3({MFh*iof@WM-NoSs?yzTzEI%IF6(1&BoHO6oUT-Hnnl!pIh$9rD8BuHb&ulj~nD1Lzp|;rTKco!WmKlO}u*LSr)qMuxZ~DEbP*u8`)l^^tU<)^7qAC^DH3G_DuZi7{>Oj`K9`n@dhh-1Yq2sB)fw3BYk>6Ba>K(XPj<!k{K;0?Kvb9iit&>2EWhuTYL?2$t_9494DI>hk6$$P_>9R0){j_*~?Oi<~Wfk7*;1qj&T}EBR&w_GpjFoNf~;vc@5$j@3@K~CrM(vggTsQq@Fldq+t@g?&nky5DdmQgq_TOKwh|WAFW-|jifWdObRB?w;T)BKjHd;$4GZ~q`d*Rai-_n*QD_~;^}!vmm)d;FeDj+Np_UaZs%M^yGe{C0EwD{W?%!KtlB)+r@79$ouAh^gH4JdlHqeX&xwvT$<(cCrxADNDUL66UtGUmfaS~P1oN@zQ_$OBoR?m?Of)zxsz<2;QJ2birB~ZKR=yJ_=+GEm$ZsD*-7uBsLkeY4gXY6y+Hy?65)*swLsF~1+ggxdfXp?N@nE}r&1UhreaxWv!u;qPx#VU`<%gq%QYBV5g;Pc+sv9eE2aBQRiv~|yp7E6;uS18T{pS)K6ViQoTXI+<b%jR`{u2EGE4cE2(#yW`{mU~e<F4e*Ojwy5BCxBnsv4HCPUvi>7)f=#%+o~a(!}+n530UVOX+ME<}j%^ZqE8>w69s9Z}G_qjY@`;lt$Pjr2515Y;hdbC9U3fVii6dEBI&gZ2vCd+qER$$ge9(37J-+#I3-XCP}{GVU*A)DmO@R&DLupgwXaGqN8Wn(1}`9Vi<tFhe(hJkc=DpQXSnWov{pd@9NfsMW2J#-=tmEc-!z}xTD6ZYLwkNgY5rWaHwre5}9o!n_<<HaAITK%+zbAooTmyj65SWXu6+6q_R?%{M~gWneNlngF-ES%^3n<9D2tqFg2<3<_V{b%hFkB<Iq=WRfUsO>Jw}VGfvCuz7eb)I?!LlyiJ3g435?2a$JxYBOVA#5NVGvk<zP#Lum0)N*N*F{V}jLw|rH%xE<G9PXi;`a|agiyYfdJDq!cnt-~|5Yf8DzV-2v3&oRo;raAM*$L+!46&rl2nRS-z*Y0ES=Bhl(%PP^BXk2F-P0bXJQw4om%#ppZ)}~zY;^uj81J7>KY>s^i9m8F0g*VEXvEMK&AD&t7wU0UDs>gwFpJ$=NW@upXH`i7~0xZ#j{mrRx=;z>63MjyyTC-=C&4Q`K(;nV8n^O8}&7Tmg0CAZyLYn6SjBjvFBx&a!XT|H@N6h7z#h8~jOf~av^<Ux&%J9+z<DP6;L~sERDv}_wgkCk*xjP0uyCws!Z-5EJeJ&mIk{Q2;VEc^b&xsWKE@|-*0In%70YYL@_kFCyTw26MsmV1GGoZ4F`T>4rjMRRSL(G-&$W|6$h*ZV$PprT$-r2s2S+ps-u4>9=LOmX71%nqWZZ<7(o;X9a=!Mx;dFHhcVrfoWwJsy}k3pCcQAD7eh518LlX1rEyDI9$qB0j8V@i-Fc-9-Op7}$9Pn^EpKK9iwx9N79Y}z6j4@(AYNhXAxEtNg+TKJ2S$FJj@6i1IFisT&5r?b)yvdg5Uqs7v;Y*P2XlMN95-|nt$$#Ub!{ZKy~-pNPpsza*?+q2=7qn{l6CHwCyPm`y~DkOj`p0ON$n~-{@tBQ5WL;}eAMJODI>N7^QEfk!gvmk{>BHr4^JpbUcV&WHQ(nSUa2EVj)_W=v78^@wgQE!nV33KkMwNX%`QfVSIV7V&vhO4$!b*Y1Iv)OVmkWet>l!Hz;4)E}J<P|YK{z$tEocG#|^E?zjL$-p3=AHF6dB)3NDy(9xj`W~g(#r!u6<ro!!)!o<diGHG5IJ5m2+^n)AM+l7hC>;l52fpnv%Td*`}42ABp3tKfY#Rc@6(xXZ*`EOT7$Q8+b9tq3R|LvJD+#0XJ!DYT%0feVyhVGJq=rWMtBsGF8QV=!!h*r)<K9d93Jf0*uqfw8rfSLtdjytNQbiAVt<ajd)(dI3EaqYieaPe>}Dt}jxX*Hg~RI`AtrQeC(JO~UJE%5-H<egnFNK#G>1`aqk_p0a*G(6w9jx%cf3N7dHe^4BbC#f?an`g(`393L_jp<MebnmQP5ZTAo==gb~{t%i2`<*&T1d?V)qG!Z}dG551L$*iVcO$5%V6UnK>_sQ<`!3<+nVB1!4$nkXi>s;s2{gR=6GE)8dm;%4Ux!*|_9@YR4--?4j?PSX%Y~tdJRP9wKNte1!HH^nTZ9R+?v20_t%QZH*!CG>)@4Aa?S-Hexgp47t(4f>YZO)8yTCY={$fF#I;-S&xU2@XLAkuMg#hMD2zcn8J5)h*y&HcBDnpB8j1LiMXCQ(~(<ZA7s)%$w%et(fIZwNS7Jy45ioMl+1fDd*~5NTP=PLe0aE9niPmhONTe!y))VnL+9?=_%RX>Gouf(s~}*$3`75lJq#V`$O#28vUyvBMIY>TS*8nsya_WbI<lqrI`R=?45K{}STY4RpTuT|Rb2~=&4u9#`==e47X})wq!`b&ITop~c?4d#k<+l^)NDV9Q!@-p3&4Ryb50wdUT0;>$)`dzx~`hj>N*hdRus^mK~%epm6_2E)aXPA_!(h&N)jMr!FWC3(Pr>MLJgp|zlXg%Pm{w-P2MVWILEHhc@%GFkz=+%#I$M;K1S)KyZ<Krh$Y;$1Ogat6zMl*l>ARbo+;Sb%wntFN0!UV@eB8fj5fGKSQ@l$hkHqsY^x|MF3hKbUC=1ZXx`ioXdLbxDU+d0d0u@+1-%gK0%Kd+FbKjqBGEe^Y{?J@qg`LRd99YJ78WvYKVZ{JGYv(<i)gLTC??n-)1zVYQe^{ehCvcO-NI=o?4XFGnx>r)!ls~!Oo*r6-nqUZKLN0Lo!@&m_Q3S9zZ}zWV~=M%Vp_nIWXAdVh90T^G&Yz?Qdt~~7KP_AgWxaCfQD(Zl|^W+SU~L@$(Y^(_WkVEWl7sF0oZd2j)$ETc1cXing9T806%J#kOKve7_ab7^7(rFefIh#L+a2SFlE|oK1i18llgyoyj>-lIi^q;DwXe&Yy#H(DBPqpR6+pHlwgVokrEW67;eHn-}N_mBXf&2GF+xXgzwD8G&*nw<T4L7kANDCnV%KTB4Ob*%zpj}VJ+sH7pZ1OeYY9)Zw{5tchXkBrX|BGyt}UJ(MPKwQG}!HG$&HpbN2MLD7ltB){IPTd^9E7jtOio5M1%Xi8xUW#Ef~hHeg&&WhW~>GCZ7#!oqoLgwsB3RX;YQDp9C|DNm!j=q_6xc9)N@AU|~kEM|{dD#uqEG_M#EK1_@U=5<9@p?$QImOi!ZnbA0-9r0(}(O4q(=hBKQpO^W(q10Ir=Id7BJ%Tuv(dJNSn|(WTG8=={RU0q?>j_5<)2R<9Z-?NsSi)b%AcN)DY4ff8me@`4j>5SI?Fw@&OJf>KiA0{{h{W$QNScrFui5={A6kG1{QMukM1od#qkSe@13=~x?OD|*0?(owNcu5BU>8I*Zd<7MXhsfTV9;H<1PyMw*r7kF4CR_zUCbtjwQqBR@k#&i#X_G2o%NFB0~UR7yInD?NXfWT-LQP1>G>7LTd2~HGPoI5yZK$#+h4#-0WL!;0B<PIZ$*>V*_}BWs?9%|!tG9(9rOnCBuvM@8xqHkVo~801z;Z5Z!1l%7beN7Pwud;nZ6aIqzn<x+G&i6Q^V(NYgkji>vwC&!Pc9^N@sKQy;0q;8TuZ6^@sH~LLcXkVn|ooRIynE8J39Z^oMhv=aWwg-=(NSQkcdl|2d{MG>H~bWVA_t;->!J3FTi4Fez=8o|`?>C@{i}6ctDzP#<1=&02>Jg~by6PGF1I&MK#yVWh=!Ps<{&p94bOjP?TzK=Lt5Q09#V7}2A(Ee&lN{Vm;exH3A^&3JUVG^NHLqx(N9LS(BTmnO=?rufbpM}vF7a_d1~R~V*#ANBZ9X)=S&-ZJgv?{tXPIMI$%j}N<5Zyr16?LK{`lGLt`g~<~8DxC0QdgDl>C;)@T2UgmiFVv!e8X6^Q;lP?LW+Y+q;y>Chj*qcn@y$4gFnS<gDcT>Civ9!Rvita<)SqiK56owl%nQpBj~s3)(IE``oxC$D1Eb@|_6aSS=z&%%(rva-!@HDo)c9Bv4YdAw%C7OTwJ5uoG^AEE6>_#4PBxd7olhXiC){)gTpFc|Q;tz3ERiiqf<aIkyUqpWS)rJpTeJm0Z92iUU5-U>;ceHimgqf5LP3kF4Qk6{H#B>tP!ThQt{P=I)Vh>jTixhmVm{KviztbzqZN@{OSPk82~~rgQQ~vW>s9JQgRv+w(N0mYH-bTe_Hcs)WoPV`M$shLJf!pLYXUH%<~eq20!51BP0WtEZkUE9I&Fo~s-FJFcuJ%8tAh8iJkWF-nhANd4=pDv##BJJ4P*3x`&(_TzH8G43gfTy%HjLy1>G1;tM9SzQ$agpJoCIe<#S}gIECXCuRoZ38K9ejsT%dM0^=RsXM$j%5%H~t1TDlMdeZu-)$y8f6+WC+*|d>XluQ@SR$#n}N5Ncvqz+M*h8*_S=fOO}*Itsp>Yf)TWM@_dZ<hOL1+7_Fn2*V<Hj|cWXeo>VE`8$OY{}xre$!ar!)7bF5>BsP9+Q=d;eAeJcr+gATF_S8GqVODy6fDjh1U(C+&DBCC!3hllQpQ;DC*gz1q|cRzpQuH4@0Addq&C$c^m>bL%hoF>$O&Vr?mp9)Z*Fgz4j$j-GtbySZPSlnj5lIP3RSDZZ(2iaZo*lIP)YF-Svr%JS<tZT0T9crTd)bA8vnF4>|ee5>_GOu;hx%34;Qf@Cj2c&D?cv%GC$Glrj*okgVEgTsS8wz@YjMsn&-rjjgVUf>Pi55#Q&O#z)@i5?0m8Ma4<zG>v=yDlqcywI^O>3G~>gZ7R5Q(Je6cwv(i!kO)e81ZJ=*rgd~E_B9TP6Gh<*TXALbPK=)n&(xUrJg%`)tuthAsB0w>oiQ4zkJD@Yl4+*}uL+p?f&}pbA8__<?o;|d&f<(XvixzT*A<JMrsHcat_L$`vr&3`;?xCnhTa0(pOlz!ZEJVL-RWr)CopXeHDW1Nl|%QrQ~F$i?X?diYjz2y&i6WP-xk4ylT9J;xj#a|9X^YUm~qS_iX#i3H`eA%9DcsPI8X|367WBxN3L*$BmK^3{lR;mt30}7>p?$k*vg)tBgn2RoZ}jr0>;Be9%gm(Mejb1a6M<HZ@7QMIE{@3XV&kM;ds=!i}|1zjw&NHO*vB0(uywCtWAN5jh)*XFv#O6pXPsk405u)&I=bWABbeoi>Xi~C7#c&cZE^f4PxB1=94_Glw^OQ^8BhRj(IPyGPGQescreG)i@*jA?Ax<iJDO4G(Ymgu8Tf&*o~D)%kc}PY;&hcCV{n&C<M9wAP)9chZ%;!-94R8OfX|Uqtu~mAGtwb1i>-~0yG)m&1?_`20Tg!F}y=S?<J~gyJ<G6Ou@%_^7jlP=K1ELc^*xK^v!c(x8Qzh3<Q!p`-YD4d224d!o%j`F)YlJve;H8<Geb|)eA;Ll4H@2q@7mDHj`|VQ)tiT&DLNd^=E=>s`bC*q^ImHuMD~6kvLdib9@Hju0$=fQ5k;q2-u<ry?W_Vw{!wOpte)VZh-q(dwX|5oZn=SDi0pdqyn3(kBe0CQ_^9EV;WT06ubA`HTF8P#KP$g(zzfx5fAXgG>GS}?h)p<B-Ht=38dSGgh~ja&}o@%wqL|w#xHn8PgUDHdg2OCI)qED82+%t|J2P;8U!X$t0T!QeCq0MbrnQ({#W{>qUM!8T5^g<XjK^45x=hpJYqc4`bQyh8vVhbk-kN>r<M2r{KG)1wX=aVl>u{v3gR;JEfMFrUIy*gUd@=>m#nv&*DEt1X2}$?C#0g%gs>2LvJUp#j1LN)m|#U13ymNvWLq3z%{tmM`iSE)@#6db8DYD``UzX71Z5;xSDCnYmW_6UBU}3#bl?~ZXTG}H=DERY?Gl8ad|x)Y0iVb2b4p99s^<3IP=2%#93Yx5hP!c1q?b_^43Kx;04r6@E+R%S2Zhpm=H{kamx@5b3$Gq^VYcVl391t-aulGQ^|f-*7TP2<Pi{0$Iq^w>?5>FR&DM*X*yXPU2gFj}+B!B#wk-VmI4zz*nW7~IrCo<T;MoQmQ#WaZ3R`UhSR4id1@<n2iA)(uD0`5pX)Lg=(LoFt?QAy;u+;a_>tNd##XePF@Jsup!(bM=%Y~v>K2(L{9`kYc>rRm<Fl_k1==XrhnicwORxegp%KdKMtPIGO4B}vuO^=6P5sKBeIk`l=Il<wRrXbTpiV@L(&F1PgQ7ch%EG`Z(bd`w19Y3m9Ef^wg$Y4>S9Lp~-)G%A09>cAUiy^;K0bzNP82ET&BZCXA$8exGKMFP5$E==h&Q>x}n~J#943M2V(7#M4Iu(9^EEu-rgUm#d1w5^)(5dkMBZS_D!U^M!lb|gK)u%@zxj(ce)5WcXYgU}tgPCm2HfJd_AWxTSrsT35e^95V?vV*IIojq3At_bMRdEH*W>eR>N1V4&;Mx%uRO7{pMUqozv-Fw9SGu$%4hN}dMyI`N<lkq`ag=;{9ouN#Q=gW{vB6r&_NH48<*nFyGkIRV=A)o`-S~n#1%~NXs?{c!gk0LJPMrecv1lcNoH?f`b@3DSE&W)}ndR_!D*LkzSwKF(i*htNP01}y8}0R2fi=^<MJSUg0fw1-(WY!Ch0AJjex7sNY_N(3GE8%f7%7m_(xPyz8(skp>eN4!TZ_>95kG?_QkKJR*@xbVo27=!oe??R{yu2SA)v#G0H4B+P~9Q;V{ip7Ct9BfoX3ShQ~3z~=?7l{4&jtJ@fZVV9l8X^)LJx+^KnqdL=`>TxrAN`&(YWS8^cV%H&Ql6e5;V5*@!#CQT2hJn+xDR1;KMq;AKxF#Jp<rXByr<_nfRbXpJ*ss3{Q7(_!8+ubT>s#D7KQ<<$FXJVydJDcheLytPIW+B7`ujN`Ni5M<`@`9I=3C9Rz-8d1JUEywx4Z^r_3_N7R~l%{|bBYWyfiqiZc7d+5pHYKBJ;HxQK&@>D=|2B}xie~pbU=O=}GGX(vhep3_m*~uf7oXPsOpfC|?CDlW19EcoCwf?v#&Q~FH^^rl101W8j2Ko3DyN~Hst5M9eYSWkg0>J5#Dx{aqqWUG)r1)T?$-At?|M&VTnWKOc4K)OI_rwMbQ%O(pD<0_EHT-qg6yDE4<rZ;CJhNiuI)E<U`YrQj{EI|&L+FaA!jOl3aLm=oN8*rXSGk2@7!4HQJxcN@*@N|SqN@2&R-ouX_4h5-3A55>;UJ!i<Z8wlIDS!GiDc_d_o$G4ss2^r@}bU>Ty<q4hfZ|#X^nn2kHBV5J2KF=6c<c3Lv<+!fmwriU>kARMlZ{P{LRc403B^=CXLx-2l2lQ0<TZq3U2qoHWUH1P~S-BA2-qzf6l~mg^%qO<e<b%toaeC}j1fn)(+~#HJra5!;8_)Ng?Ga*1H3>r9<-dVtcTO>ttI!&>DD+bU##KKwBQSQ_i8S2k;x`A=@wBkQZV;S(jq1qN~c8K2u4gSDzrnOl80cW~~P25j@AEE;ikjGupmld^-QX>B1KQYD|QGF1%*j@4p)p!pu#euVw7Z#aKUz_AdMJ8yoxpcgBNP|+Ql6l_NM446#UpnR@Mgu>=2fepp|4@nBU`zK6u?|OGbliz$tOz!c=4Ck&0CHO9b>zc3lPqeezDv59*FiL6{^Y{v{ZOb8?5%!W!d?A!RPr2#^x9<fZLXcvKHwO{}gH09GHfHtqGZ^}L_%)`;(lJ<rlpH|@&<)4zt|7wbc=>JM4w@%m^ah6%Zm{Xr(wpcq7~Ye{QnZ-`AYI-CgWpu%n7CRk4Vx;n5_nM^nS#V$Sm-hCpjcsjZfFeauq*3NQ#j_uheBaN>fKTQA2oR;=b>=VbIt=E0mxh6caqe6SGKp0e`q`sLioU}2$>})YDq|p)lYx`WYiWedbKB)uOoE*bY5aKwvT>t9mQT@fZrygq_p*eRHm%={xG&xX|)&lLcxx}6#lWyt$G5Kym`OMk*rsKMcqrpl!c|A(!di33T7on{@NWmCFN%=GEM+-bLfsm9Ii~5C(oTY#67ETk}pFa=HHw*?aJsc*Us5#LKm5`a{izdJ-cy{a)p@+KR#rZ;SsI^cb+u=%oUNHjnAfaNO)6$-NQ`$g@KjVSsg6==xiw)d*PlE)OsYP=>Zd&{2jzHvE2EHOo?)o&K4QwvE@_|A26pxe@4;r?#ia$!hgqTJ~^#R?m{E{57@?9W(Wl5&FC-p*{uE+l&_5T-DEPbG@=V;v#FxF>be|wuvFqmS^FoZ3(XBBJLJM2I9g8IqwSUyE)*Vw#g#$P!SocD{Q<^pU1IOX^&fD_M7tJj@UV2&uECsz26L0H|2CV9c_A>|j%l47n{lvtuROtRNF^w3jv^m6LM~n!qT4J_=X3Lp{^q4flO$NhC0AgR6+C*|l(|^piQ4~D#l~Y73Im<}=9BvrW=TAXO9U`R^jd2&?w#jT2Iit#{K*aN8-03}C$$TuSTkWgh|I;j=HkA0kL-VGN-{UqSb%ZY?mNC=T=13>bAE7K!o2S<|8iH5<bEIjU%wr^c<|r5JHX*wS`WU*<rawE8SNqi$j~z=Pfg5X+0BpMSDdjrJz<_@xp=vTmwg`wMJc}BTzD7Km0)sB(&CN!j@SP{hHZBQi2Gbd-$OGiQWIpl=vlEvtjswF1ikaaU`)7(StFiE!8ao9t{%I&@G?9e<NbP57@|TuTn=d5^^}f%u^;L>$*++es{U35UsZ75N4)wSt^@#3=S0jiQt)z=fMkAbcGs&K9(-=5woY!xjCm`;(=Q<;M|!ZkhyQiB`{29Jf?(s9kX3jz3jadM>f-)?G4gjBwWTvd1qLvB!`8U`_37h+PI*E{6BDAqe1=xHF?xhR`fN6_fuG)_3LU|BH@eu5fGj9)mFcDF;xKvBr7_vu8SgnG|I;Xq7Hw{DXy<NDJSE33tbvy%HCBS?>?j7V-m7!rPN?rLjw_sY2Y&p7%O~%j$~bAXs6H1KgdqH<GpG^XQ%UK=GvDxZlit0sMLr92;YWy=+KYN+t!RglIRnRlq#ymUMf->E8D}^sD90g&jpt0~=fZlhB?6Vq!wQ=}M+u402xbp%=YS)q>!n{oT>F$)2lzp0U`YNhhQrdz*0~>AIsGoEt*}7@F9dt@M>a$_0J|;t@54)|fO9{&QIP~FEF^D|0$Ii8YXbc|tgp8{5}0u=rSsH>H#TGI8-=vbt7LJf<FS-kBQ`J{;*-FKy}ITPiA2cvprvzCeW2#T$j~ymQ>avXHv|^sp`|Z83R`^cC^W_;dMUeZ$Sj-(*|5;Gce90If?s8~SKY_oyL&&^K2~mj*++rlJ^@Q_9tPWyo*qPI42i=M1MCU6(Aanem_HsXWz$74cy)8(F34)yZa*+CmU2)VFwD8h49>^S{KQ&t*+S?aOe*I;NVg_$8_70~(MnPq@y|m7?Pp~<m2gq59C!l3sw-bXjvg>hztB0+WHH(#(qFJqeQXmb?S>H16_Yd&^it{%S1C_W)2K15XaZBQ=V~};3!DXOm&Ki!HWyZdj2(fFI!Gmo2lz~)>HQ4D>4{Y>$dQ{%+d+B@)$tVD5KQ1Mdp^$zw?Xv`s%R-K1-8g(bJBm%J1l-{UbFR2eVKrn%n~fV(%KZ7&DS1UF}Zk^4O5NF9Rs#do~&^yL?aF`sZqU*1)dQ0LaToa{3ldIH$V(&9r68ETIx$F;&*pv8`$?>ev#y+o_W~k6ruC<aLuB8c`UgS`OgQWgBM9fk2H1aZZ^4O86DRgvcDN+9+Sk>4Rjw$bP8%V(!f@fAy$7!GVtf34^2$+x&kGz4W12B(ONzD<L)fX3K=0sJ;R*)(TIc`Ur;GQ$qZ98yGFl}Q-`AOFWI?YF#M}1>x!xVbKyT&8Ip)jKdyHVMG^>;2Ml;|ok-lmIMXIDDJk;kOCFZzNtcZNz;22Z9+*M7*>=rpulYvL$mW}|J5B1b!kQ)zsXm*KK>s-v$9T|SeJD^l;p?S*7mbda2gPU>zC;yEO~S`s<IIotu9+7vwR!Fh4`{7sq}(moh$=ow5dmg3o|=n#17dgc(4gpaz39cCN`%6dZlZgF>Nn@Y%MczqX+B14P@D)4Nh3m^HP4eP+NUon|5N=4SiLbJ!gb(T^XwbK&;p0i$AD$IPUDQ{Iaq{h3{**Z!r{gZV7*D8RXPe*<9zzwXZmV0IM5`!D5MJRm@qFtzKXOKV$h#-E2EVgQ%hOgt5eihX03qYLsPUU*P%KSL!!yJ_b82;5!{v2UtT<+wxza5m}`uDJEP>!SL*RNNTW;FXtc+PhH`6A{Oz`!^B?mom!kNOXe|c2$7sU!Yjzu3stEA&8&BLP;{+cS6YZ%&wUv>zjP{xx(PSl)|FCQ)4G{Emcr7h6kJ%Uyfg>0N08WKKQCp>`P`RicfXwUyCS(8cw_pGC^Z)+mw@VWj9D|0QYhaw}m3JJ2d~;eqkmQdwiC_AtciX(IwhrE-8IrV18TyC&CgmQKBd-ZJ{`&t#n`V7vbThonM4zWb#75lPgD7K75aQJ#6$b$99n}0OovMFPnD;65IVeSdkklN{bOR6f&;Yd|M-I}ml_)R$TsHsyo38Y44=Ifoe)RiI=#a}up==Au=%QIAU0rZ#sf36&ISW<F91w+3;XlIbeL~9gUr^O3zMoUhxq7*V`JSTSwWU=Mo{{Wt!r5Jx{h~ds)uy^)nGj(2FlOTO)}Xgt^9DW7Y)kCWobd_G(jqV9d$TFL{XjzD@j+GLs!rOIzMuAl5>|e~-r~6jufN-!mS+ombGCiUb%`!XnEUU)A3V+|x-iuzo^?@rB@%8tT%B>O#CP7z@r%LH1WQ1A9}tjXsKJxm3KU$QL%6$*zW4(&D-Rw_;9^$);qn(Lbe%(+@ETkJx{C6&ZAXr<O_}=fbEIF8b45_A|M2`__)pm?-^7%Q|8-=^#VVYS$YR^T%O;-rMxSNOJ(MF|9bn8Ot?lz&eU&$7h<sQ^<4LRj0u|iHyxHG~#TIT10%j2~OP12Ck5#|Cn8B@a6gMsyT9@%>vEP3|;{nfUIKV!G2L)bLX|M9Q)CER3_)HY8T!GLEIwYJU0fspGMKf29$ReBYhrrOLR)Zj&$%Wf2_Nb3vl_xNRi+OWsqr5yMgWV1_c_0S<>ho<4*MDiqVkmkLeIvFzKBA4gHi0y+ftV~urQ=Z^kB^<naov`3e&CP|nlF2JpF;O=jT~5&fE~W)u6+K%bFbRH^^KUHvhqR1zZAA{`@nqCC(dLL$W1xXpTE~+6C8VQ;`86<Nh7|c%cR4!)M++mQHn#Y>L{al81~bW`Ze|W?c1M!`t4iw!{;Nit(T1R{ZHTif)h!VeC&&!$-HTK8OeXrYn?$IQn|IUvgK#9mll3txIv<iFy8tINZCvB2U*cG8sYvsEP6`fP`?-2EUTz;9mA6APuX%b1hDR-f9<a#ofV6C663h)8$ADt_S$irs{f7Fe<3yD&ws*eUV8R4ss4!&o>!RLM}YG&7QORL{(uWC^;OpPF0%E_)$lW}-u_b2_u}F2IPdTOe*ceu`a$PeGwv(W-Iw)T^}hzN4TgP%h0_v!3gh26HMMd0=`X+j`KRxT`R(JR{eAxD|M{=?_y2z8_SClTvPVAIYrn7QZ+|NhaTw4YSLg4e_`9?60DpM)KQY`^zkZph2uJdgdPE>A=?+zpjnuNCJeT|PoBZA0pwSlE6(svDa=<s2v6i2a5BgwIfBuWXe<?Q2i)XRtcPloc{aiRCW;zX!x?KihoO;ZtFt-nGvwcBotB0>uFFsBCnAkdY50}<THbE62B{pzk$omHFRHq&5lh;2K2~n#tul0~uy2wSBuzPN(zJqDkH#AkUf7j=)7{|<8ciWV;8<k?r^?-=v0O-eE7JD~6bhm>OmuZ&FS(Qd;P-#rtc|2o;-%rTTDvrSA*yno4?hnV}A5S&wBN+V`<H#OY$0Px&I<8?udPcY)9D<V1swB`A_75Z){|cw;e;Pj~Wo5!NZ0HKZ1~8@~!lJfB&;L{}5`E*?K~pLRAfiAX0Hw3RDHqGz^LF#tphr+ZJFVE(UTynG)CUAL8IS859l3oYos-#~Iv#X|h8Auz^ihas29$5sszLDY`rml*Nrko<yZ4RJK`6ztVa9g*A>M!A<{D?4)>-_m6*=vmydH}oWu~5W7xe+l{(NNA*%kUv;%AJmF!KML-`%^uTp&8B_4Hv&L-3o2HhZkE-z6d<WszhIQAt145Q679ZOx1R5nfkj5gE0Q=oY0OQKF_2ypTQIo%%ky@s=5;{=`-otz-DI#Y-P?739bVd2dP1O5oyn0X>X8<I%tfj}(58)knXAlfe|Pq0gNagFFX$i%jXbtQS#AM6c`ChaW(IXXoo{bF1I--!NB;Mr>=>u!!tS25T2uK7iHiTUN8xO$Pk_!R|>Ep=83#(azyAA98F7VrzH7I?BeUfPYDOcvssd2vlO_9*a*8_}sI<aI*SX|6X*YQOS&a*~Lx#K&$ugZi9g^CSZ1JizpvtLOiKUb<yeyp<ZfLn8=6LHRF%8J?td{S{WrIiCuD{PgV%!QUzhKjhr@N0Zum_E7WIT<$9&3mfUtTdaaf4@(}Ed*ePW)Rd4KO7xVB9Wd(h_&NuaIR9DK6VNHY#GOP5n`f-?>k^qE}I{LWGPd>#Ufr%r#Dhfa<>t(`v8pP=G#y`GBeg5r7!)xio#$#96p4(=12gm&NzOK(}ApLpPVu?IhEcKR%Mx}~5$revj_~K0*Kac(6;iBn5Fh$v;^nap^uv+u}p&qD2kMCMMU&rIr?8o1`{iC;)2W+EM*p`fG&BDcV0}M9rCrIIGhYHz@$862S*LrjjtdDo6y%-=#+fI=Ch$df(#6@5X^a0^k!$wsN$o!NK7z#mU2(ez>$F%sp+i2U%Iyi_bOUzT1uiu)70g(NLe~o4L;%1+4(=?T+x|Hv4FBMq`@5Gm~ktX`RCXf5DpcpZk9xXI7H_agm*wS{h0MGBc-u4or&dn`55|C2%K@E4H0mhZ9f5`3c+J!pTz8h`BWRecc6^zX@uG_``_LIHL1ov>9E&@QI@8$&Y><%gHn)&vfETq8vy>9p88^@;fsxi3^mxmmZRbSBgnGvjKfl6~tpAz>b-pp=O<7NeBko?mciLQ$Gy?T{o7d%_3Xjpe7qL037t5`>|yd{ghUCHhH-i`u@PQ2c>%tIuzs)HCF?JiRT4|U`oS+9VtIoey3b+Bl06pw8<`hIF;N;DKi498V4Kv}Ngnr?t?iCzIk{}S3-SYnO=U!d=ogjqK2-2!$?l&F}+jlN&qwo^PmY|4ttE#!h@WID1xgL)O}ynvBU9Fp_r$Oh@xm~dOJy`pI>o><*|u$}GLL#v_80=uk0fhFq`O>+3bX~>ImB<y||+=CRRm*QYiqOa2s1hSlh+4z=C_Bl#!+IU+`vLzNFu6k67DANL?nSHOikJx>*Wru1L!Xw8V7Jrc8_5>wk>JH|Nv&fl02kWDAhV=aW8>Tx;di{s?p~~mxt8C#{-c!l@`1of@x}r3G>|ByL`2+Jh<Sbe|ran)6&kgDZynv;Z$H<2}lzsP4jG7+7z@w(2y<%vndz#q;Xdma)W-7^3ibQ`5)@&IJH)EWy`kF*PD|{xI(aAo_#jV#VTYDBx*XRI$7r{8!{5Z3ssybW%A0QEJkDLAA2`fo%+9+_PT?IY6O*o!E|2d07O<Vt~@Bs(En>tFOzkvSR*Ka@&vZcs9bnN3X!OnHEI1hyT6QjRDKr_?Fi%o~Hr#gjXOuY@*BT$!rY!V#Qx}s`T`3`NLah_x-l>i*Xl1Xd57}dJoTnwBNCK}&U{T-TqEj32RMk=|aBMa<O-cOlsc2OTVe)dUIb|l^tqAkeE4{qf-&n_iaGPNuhwG1HrLBjxJGEmZbo3JtS7|%XkNgQZenTc8t-wPluNg6f*Xz-4wT}iYJrfPF5tM~q-f{V8pmSNkEp>*WIvzl#sC8#%m%~v$&DCS5JQsvJROrUdnN?PmzcFtMPGowvsKM#3nMcW^ea$Z*fu^wwa=Dm9^0U0X14owzv*ojV=K12bK-}4;?+752=3WQ1t>psnK_9@MYvVszhMoKylFG8%<I$(@SO0%7lb3g;Ml03(j-uzNdBm4MQn^90-`mBdAs*v9q@bfTiwk8G<UK9gYR8oq+=d)U>uTQ(PzR6{f#vO@ba6+PhQi3|UWXDGC$fdj0#OKb5iUH8n7F~LK2KE_OJD9h)zu^PWFN43+0BoE)IC9g<{*O9BGY*%JvL^@wwCPo_PM$l#KI+NuSf`%U04IymW=ELqA_2>6lQVfQ95A}C4VrDoZjXNPKLUz8;^agPnfz7yE%tG*ehY-^(n{ndOdk(dCi@|*^S$|=1mI3%v`ITNX3hz0gE@`o75*Tv9WaaX{Xsj_VL-0FP^2Cv1-ih<)Zva@mfS>t?QIQRR+6M150|cDPemHDFijI_0>Pe;x{k;8PD>Lz>Li|f(;6*C`b497+S-S`XzI)t9||n4e0Kq`h9F<Nf2#w;g`<_Gk`~#Ail+3BdnWk%h}S=wB(!cxC+JBLKZI?^o7p5*>mQE#?<ULiHAUKBi16&Gd@j;%B-iU;ct~ciI>VG`>$$z+D|UEnZN35Q_}G7ilBElX<a4-%X!D*={PNoKHgrSFdAmt-%fq|-U`H|7Iwqt|(NJiWFkBs+_F#2x1d<eLP8iaNz<}mP@qnqYM@lHq?*xps$sW^3U+9;Yo^V6Ax;in}9EEt5Xyjz*HdiY~g-)=8t6>IchLJ;Wq<*G{FVCBB;ndWi*|X^yNc%o+!;+3HEdOj3b_~6@qYzg8K)fp^p9^YGLqFIh5g~5@B_2-#r;8e)*ySx==CN6%TYPX8>)9$~5et&tKIL%&8_*CwA2Bbd<$LY(QT8|J{k0A!dXH*uN2L253Z-Xl)DFHs?|8vZfK*Big}77Nx2yZRW<Y<$UBgx69j~H#5lOd=R{d$2^s`khl$_r7duP^Bk&4gJaN;9U2sp`3WX^!>b*_OSW99l+>_>Vim|04Fau^5h+M{I{2HRdHq2-S)gpCuF2^$9A9f#fBmWK{o-hDJvgSAi+LJLs=Fr1*{+c`rY|Cw;vFvuhdww(^iSX0(`bjrBLY^-ZpKu!ZzNW-w|UV){pEPY8S0ZQnj6iFsJXiY#TLM&jsjMYBZbs38PS@qacp;s`q@nOR>sU(he(Rzoiq-P7MqmxloA5ajWjZx?~2nj*;Wi*yvaQk9;Z)2<-0?iB|{8HEaV>iCz-`Yn$C~TQ5+i6%J$4kiB685{7Sq#T4M%(BLqHFGl(d|mW-k7Ytfi4cCsgHoLA}?qhfsS)yp@C&(3?rbfBY{2iFeboCilu@}EOYgFR?)#q+lVFreKNiibvE#BH2c{Hxutfl>cy9~f1;88<@`^N#*GUjGK#T-eIx^skexGVeJbe`!hGQqS$2qb);mIWoAs=)T3U1Fa_K??s<v*TrUA3Rm=#j}%V1H*#?2cW!@ddY<}mdJqf=rMe0h?VH@@x-;FR{kn%%gUm<rR~OnTf_&!7WVOp9%U#+uhqePIk&f)6h(ebfWlV9-kgf`HpIOq<Q^0lyON+GdmCdUT~WF-tjk|K*q6FZYF5#oW0WZ{@|r89H3b@-C9U2$Wb-8oDb4v`@JAgGNA6s*JVbRDH_*$JPbA20-(0t8XCqezhR<a!@LKf*UC9qZ}JX2@FL5XN$OO)-fI!*(9HfuLwenP7%puU=h|Lz_{m(Z_?=<IL{^#^RT*-wa$wj?}B(iw9vAhh|DVf9#RT+UZIGDpCDRqODt1wa^h)9yo`e3Z@vKK!(prBc0F_nh;p8KKP``jx?}M*-rdat{Y@N_&OX*Ip~Uby=+s+Zf?6(WeyIr@n`P-W&URkgpMU)&zKfj=PH1OtCa?@PnI0X&^K=LUy?xgc3ZzvfEX0RmTeW!O8J(gnJZYIU4GNx2@Jm22@chHifBp8~)HS>t{Y8E&4OXUO-Dh9^f=;t>3`A3a@S>5<u{2%>UC|l?nHW9;gI<%Hqh%-avXJA;z7KZuyBEF3euJiQT)dCmM}GCYL3s*+`q0&=I;nQs<L)3+@vPBYgLz<%8;Vy{%Mk{qbM4%IaTLR)6Yl*>h0_+bYnEWDP?}55U~5>17KFxOGGWY7tF-Dfy>j+wjLq~f!)6MQrjP+L<Vd>3nl`^2w@7x&>K@Io&2!_-wtweW310}y2=j)U_kI3Dv7e=tv9Foxr7Sn&M3@l;jrd``)$U4L7^@o>U@FGCZV5w3Gr~$VnQB|<?csK>O(dtP=31xOARG+iw5?05GuyZI)l~1_Fywnz$@Z3bNJ$TN7{mAx!$-uj2Lm2_c?*xVe8vE;$jj>6UA@LO+8){oTJaTPz^Lshe1!?8Rmj^XG39&cLLNEQF_?m5_L&M|EDP7RS%%$X7<`bzYV<VJSh6omD|fq$z}4K9L7!!4LXGM(T$I$Ew+fMi9D-;F0A_VQQ}8G;33+)l9L2gqwO=bCKFEkXl^hlBXwt^`c%)<zjH**$Q)_rt5S)}i3X}x;Mv&9-(b=d0LvEQ_Rb%(U)=d0!+GE|2cs{1wzw8K!<BXsv)kDn2>mL{3^0?vl|H>cf^HsTR&vhBZiR99T+8+7rvegUxi)#Ly2<7tItW_wMEL!7zamLhLK+v?KUZTiwwc|N;A96vr^!(rACEl0D7Yz}8IWoReCee}N(iUUAY6WJo0zShCUk^4_3G`dDG<9FSRA0R`i@P*&1NReeDCI4l+zp(bq^29Wd~f3xEbG2N>p#26`xSv4A5Fq220BvA&2I~@pTNL~{S4e5k6X92`3BI8jbjNJv#Eg65vr!H+Yi5W!!h+Wf#xu-6OaVS+PP~s88$G{`lhklY-JFBbTdWHltDn9Qxqa~pK)8?>_nYzC)>mU@VVH({~Le(R=)+mef#rIzkRbV#-g#p^}l{UrsYq5Ud7u|AxqmfiVGUw!pll;Vcl4nJuj5x{A4Pq5BvN<)<5=u*Nl*Lxaos-dJliZyEEK#LKF2Y0hY!ulbwI{cMD%*q5TJmD0AE)$KUN_=A#JRb5l(sNhFWs7itKZ#fC{e_4fyt?fhC_3({#aYlEhURO4Xu-NIEMzYh>ya?804jC*Y%;fo?75yaNdA;nVmL2h}g7*vDxMVi+@NfZZSyW_FY`V#{gytriNeh|AT5&(fQc0cOaHSA}#$6C0uoGm_%ey@)Y)f8B0#;@B7B`cQllg?&v&kB8iY+<S|F*d^O!Zg5g{$g#SolzM$u)X%vYmLIF*(eh#zyy~_@EP2;9Fv<9W{(-;67FLvYgnRb^gj5-Jr(e-X9^g4>1K;Sv~b_o>D3YE73Kxx;P4VK_2f{uG`$?653{}Y@nL)-*870ZGQ6;+hb_gfU+_kBIebJy`GR|Y71jq<h9jRu&mJ;%4$Lx?$HEbT<UBFS%6{sMG8&-oa{RFPC-zwlxq||<+TjSnsjstCikf&YO2zpo>KXe?$J;L5PDfU{_fmfLMUB3+XQ;s`u5ZtK?OXnRpLkWuj_p8fr}<wRnksD?63TfOpJMeBQ&?_`nhceF<wH;`^u8|ZErC7Mku%T3N|DdBkbd&EPiAYGObupvy#&DZ8RpOPqd`Jn(+C+cH%H2G#@scE>l1W9=3<>ySYGuy`yBc_%`-9Tn6%0mYsqZAFo`e)$SH-kkXSVs`aB0e=A_4@-o+_@Nx4*Dum(<n-_#2cfPFzDJpl$T;&@5~j(IgE3;S$}{r#TxGB~d7gu8@YjyA2;s;wTPY%Hof%JO$SB|a!ThzvZMrR&)v?5k#d4TFYpZ2TZNxJ#yk=GSnZC0lwjQyzXvsrs>-mabJ=4MGT|E&|j<qABvtf5#=E=n*9&j=v~Ip>c&SgRj8%w>m@%gHn#=Xv_A~vFc-P@9_A+r#h2<5gNug#_qqkq)Ub?;E#2o?)_LeN&x9e+%uKA1~}eA&Zb_HVtg{(dYK#X{DKf{$Mc2V#C};rP7j!8pKE{C-Y3Fg{2bBGvbl8Hf=%=$W;^2_b&M11U9>)40q=A_3f@^2DlN<b=M26R{|n6=*vf0-N_f3#qd3a;)sY^IA|c$Ch4L-<vh0H%Zn>Y-fmu`(p)JpJ56f{K{ei}+<iPpFHU^0v7ckyQ9F`c?NPr}SgCg7>Nf(6L&=cyx3jc|^yu%Hb0nH6A0>@Zh;W$4Qz7wjX!##?y$B*SdFG)sVo2`iiELdRx3iDtyRWA(>$d+me#DInPD4FKF<>e%g#c>7-lM2tVM4=139~^B9z`s%b5jF)slUu4z5a7X(3@saij=`->NmGSkYE45>0u37@i%iViyJ^d)OVd;&VVOXl7uiLpn=8=e`MGkU&<Gwy)SvgzK?Uhf-t(^rh$WxXn%ZtO?XssXz!*~oM}D?#VOcN559K5B(a<I<c;uw-gyU<%7E3Y402B~CYlYDSARWXVJZLGUri?rYY{Y>X)<_7$M!bdXxXH)dti}Y}%4+ZeI(=BL;Pj9!a%fMt7G8S;*b$xRNqSL$9nZZpKH^TUW*gk#ox3~-qic(_?kV<ESWqCj89FGVdK*){pe>S*^-var+~=qov#L>@|35>sj6c}VVXXnbP|2pk1|p4YU1VT2(Pn-v(ltF4I_~s%NLohTLAEr4^*OJuk-Lbk-lC!~et$zjg-`V*z6<B0v>dZl0EOr0OZ|K97+2Ldd6xqs7#rUDIzgQR<93Gu3%F@ot$p{%dFoYrZ_>;m<u%AS&}|ZdT58Qr)TVw+0E3J`Cx9jpvmRfNvM$KT=Vq9!{(chsAnh4BKoUX7Q*V2!gcN%81L_U7e3q+Bxl)+S$5&YIJ*9PI^aE-|Q@`0<Omx?n+~4L0GdjCFRivT(GZhXMtU7jzAW<Aa#dEX@qw6Tspsrd9SjGT#<P%NnKCw`2DqI-UWkXp*sqp@WMXcQ{W*UZ^N?mkT1r)31wsZRcM?axYG)a+5&M05eP&1V_g!Gc?2cxF5u11V|GYzvF?J&1nN0X*r+j8H4#ceN*`CZ?<&Q5Xf6o2JcUtxZCQxhK#FUdJy9NRI0EwR@rVZbg^#ty!2+$g;lX#3j=le*d4!>|vF6P2Vz19$#RP@@R^$>avXjXCy-CP@4wT7AJiqpv{5H%TJ}7;J+rA7;D!@vrWCS6O+0U(!s0YHpb>>Ek^uWe%~2q-O$eXx-!thtsF}^_C02@C<yMZLRnhEpShr!3L34Z(WsD*UxZ_T)8J81#O&1yPg4rBrBUYOwtkIgY+n}eMD$;?38SMN;)BY5CJhap<!T@JjYT+-1PvN`kdh;%@ko7Wk|`SxtoYCqNFIC5o+?Bad%G&exnlPOe_3iPl?Ag^)IZTOfNut@H#h{6M{=sVm)ykWOZktF`Y?~PML#+K(lCCZv73TmB~I0Rn9`{pZH7IO_b6DKCa+tzU?|3XJ3pO6lyQ(cWqi4@V@6id&CpG#3qxOw%(D`w7SkLfv>t-K_`SJoIihG7h|8$a?-T5l{tB4sa%(;ZwrE#WaZ_U&}_&o8ybT!49wywYh$Kq?izUeRmDo^b^XpG>?Vpx43~G=Z<jR9z3l*Kb-hm{Rmv;Whb*I)ejZ$-Gu5!;4D8_ioPzrd%cfsve1+i|OPj!p$hm*M;BYD&6J!CwgE&-4Sv*1sI4z`j&FblAVDa<1(9j=CzF?&;<5a+}g=^sOIc9z<xC7^zR=f-CcW5nTu9u;3J6(&zDM$n0gajC8VW<Eyz82#g);%^M>oBVp$C+3jHf6hsbYYs4x-F%QY__mnh|hq+ebnP3I*k!P@jMIX20KlzPoEMz4FNW?SRr)Gs87l=G@cYeD<+Qi%p8U~;eM|46xn%9g(U+g&o;ULiDI8g=Vs5xX5d<<%{JX=6qR;5G?!1Q)1$cvXJaPxfBYyWQ)%rG=+Yq~Oi>)muCNao!^S_Rkg_?Ci$&?cQubH<q9Ftd_}B)JvROiKiD5O13<fAosrKQD1lv4Kbz!ih+Q0gShBBC8E?iB$u!Fd(GKqj2fr6jO&Zo5YM$k*z1$Cc{)SHM%1M+v_)@f;WGOa^Gz6(BlYmZqGxKpS;PK?&k**Z<?9p)zrcuFYX%}r(UHxAVvq&`q2k8P1R8O>tD$6%f9drKs{e*1`Plf5m$9N0gdkSMH+vpMTTk-cw(x}&jUQgUBcfA`s#4!Of9SB0xZ_5p9IAg#J8;aSv@6<J}oZeO-hwny77CVDM;un&4gT=)KGzrtf8U1ArNC6xUi3yyfSf9kB&1+CBFGMiKHN@e96==HTAo~NfJ3Lp4wNJUevZ8~kJm-%Rb(U1NP3ZGmJG@N`zE0&hM=P6`cI6H{@32ykJi+ROnJ?(}Mhm)nTc6V;Gp{b4vfH1~FQ}XO<ikH!iwzkDKAh*jn^8B0DW-V&Tt^)wqTU-gh!YR*HS#4JX)JVkW8|K_C7HjrgIJuUEj#PM429Au2<uSGdoiOqFYP;bjM!n|8Bhkqmi;CWmGWr&+>(JHjL+pIUECQlfvkH!Wc|8TIHXNxb$9PwN%)j^5P}Gvq@+T4;xn#qRxiFNVgJ)?Aaif0)_v<;_(KpcXBOBszqI)d{(#8M+n;%oANdVm@jZhfx?_rCkXe>QHW?1HWzWVTTw)1^1oe6oD;A<@QGsv7ClD!USiG3f~>YKKU{FYhF`&|u8h?EiWjy>``%rde6fKW~uKgxy-vDpD{ad7+&H!GgIhyT@Bgqtz6XGt|orB(fn&9BQ5i|RAuHN}C+LF6#c=F<h_yje|DK>=W-`D57BPe*{UQI2=@i|DIpZaijgh|f9q2%St|>&AOY$S#cR<N0pT!upePFhNuoZe*6&OvkW|$lxPBJ7yc=8hjEc+CI2B@g5!ja*en&$$@S;EF5USL!I~~d9`t@;B*Ku|B4fH>EBVVS8SHD*&v<31*a@4Dj%MA!-wN|6|}dWyG^#zSk!x4pMWOrv`?3-PgDQ!yL87A`#0HX{X;ewvoF=YyB&}!9-DYfGC`4#$AmUNU@eBow0Q2NXg;p%$*Y1xrmW|u^$Hb;Q$Mtl$A!a{*_t@pylWrz3q2&~mvF=8esar697FJ%*QOd(tqe52i;PwMQ}!j98;rj|oJGy;xrcuPiZ~pjUwng@cZ1Aob{#0ARe!u|zEON@J5Rp+A!Oo;KIg(Rju-`qdLT2(paV9WKO8SY;rM171@IaY+W0YZB-!v`F6`exbZFXg0i-MQWaPLA^U%BdJl9G`Zgq%iSlEo5+jAQYwoNUK30Rc@jM4yN!1fs%UHO=$8HLH%+--a6uMBaY#^iUbHZ9Y+@P;5E{yv$TyuW-H%g=WO8_TNwoYfBO<mU|NOzr{Qm{g?c#ja7y*5lnC64<{NCYkVCiUzH)V(CUlN5B~AN_QW#sdV4gS^CkbCoOk=xPeA&YHVK&NmDw9iKbPhP8Kijx**Rh-02wEfI&`>PkF_(x<0xeC=p3Em+k}&ah8^L^x~;wF!~{>ZM_sgZiKm#Ft$_AsO{j+q0~F|FEY=m@qn>Y;<rT#G_LRe^IM8xc6yVXrYooE&k|9t3;?NFq~qzz$j^0LI?5uyhf#f<DB8(4c1LY%;66_e*O13o4HB*q|9M%MBRTQZwOQ{lj1%Tyj6fApK_&^|8n`ncR#fa>BpAHLX{MTBE)3ON=5b8}5&1evXiOIFT$rUXu7|q!IjNvAsR!0lWHKoZSEH}OsUOGpsN{4{;J+H#bkBuhTIHu8dWyJCBQ&*$g#dHml|~#9gvp#mjc1Z6;Wb7M;+k=g^k8geknFfQ%L;h8sW;#E*=Y)g)um?iPr_rz?#w9ED?Bpc7UVvO1>a*9HYdjjczYw|>0YbcG;8V@U~f3VYVTjl-GlvIVpHO5)p{NpWNNMvwbLKheNqa;G2W`XsRqMI#ResHR=6n0B{@{fbU$Szr5o+mx|sD?+}U?{uxObu)(jyl8usraRNbclAA|?I?pqmhR7yLqYDmxakvBV)JA1^g6KZEKW)UYHY-o+eC!NfZN71|}SC2Y)2XPl@Nq)?LMrjsadNCu}mTD^7c7}zXH}d0|&n{h~rxYd5>aQ3l_j-Fh5R!NOk7%Y+UBmROQ9?c^`iUl*PrXS<qDRxc_)nb>1IUS4Mtebyz@-w!e!RE#v#J-;?6QY$nk7TmC2$MKy@^LKBT($)nr)^8FJwOl_8))y^-n+l?|**VulsuB(5ELT5-;kdBWvb2$9d03N_M>%u>tq<acqs%)}w}11uKYG#W1k^DKiaDM+%#1h|*)Ub5|p?gNz3BHQ7^<2v`W~=c<BT6Z}|p@GLub$?wnZ=R+Gl7sggH!xs1v2s%Nn+9W~jBOD+N{D}HnHVoyYo@;5}f79g-sIeV!Z|sxsWhzE&V`KuJybP?iB(e&o9j!~DS3JxlIlu+Ov2A@GQRN;jm@A62o{=8g%sg|Jr=W9f={<qxAr198IfGoD{%ls800++lD(W*<66g_EURyUOv?X>SW2>@6mL;s@iZUiqFuRYCr!ckxfxSTmGi;jcJl1-v?XQ#ZwGyU|&z*Pu-R^8|5E<np`<9CkU4O?MQLYT$R?0SErz=ty_){KQS{4WB^!F)$-~Puh1}9JSvLUAscp<l+%h9KFLoU?kZyt-!PHdwue=%5_^hv#9PHQ>aZ9CrhZEEV}_Jw6u9FO`B&mV^Wlzm(YzJwRyYsc+#_4O#SV_I`pwP#d|_^fYM^EFRMgfN(G^>vhjy!h^9D{;bQcXyu)v#Jj-#m&O{3@r<sL6_2Nij_&c*WAV0i%Sy>t;@I)<b9W!4#iu$K7*?W(w-QWQ(glj9Q^t|r}sk8g4&EqY3@G6(J$Uu5+V_Wgg*p^HnrMf=*)__WCVW3UK7-A0VUD5pq2LWkW5ZHEab5i_^Zz+HC+FtA-|wGJZ~e-04y-NwFx144Xnd^oE6XXczo<k7V35o@<RznpnMFqd$>Ak2Bxz^_S}8XKUixTcKewOKhE8baGzp91^OI@&wRrv1~YwuECSLt`q)2HQ0=?Szb<cg(1<aP>=tRj)Z%gn3Kp3r8BD>`0!&`=nBTtr`KRB$RX=>b&bReqK=J;kZ+{^<f~Z#S#w}a;A)a~0(q(dIT7N~ndEbK0in&v%va#spTE1e{NpgE$_VL!TGx?L>Iyk|i{&)WzDbjcSq{t_}tSvpUCGjna$ClUl9Gu}_`!h%*vLcog32C(IHQE!y2LJ9$zL09`=RZMP%Bg*e{=pDFCvaTx2ZpUW-{cRtq*7mHP51VTR_e`b1nBhf15L3ZU#1Qnt0?gA|M!3Y4*&@L7y')))
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

_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 5]]
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
