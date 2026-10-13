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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_kBvK;td_}mYb-<kV%hAeRik!*rIR6#2cgS*<h5U|i<aizBl{r5emJF_Y?+}zwevU)gItEcHX?5>Irj|g{jbMt@w=KuJo|Mt({{BQs1U%&ak{^?)->p%a?mmk0R<<oD!ee=i5H~;0I{-6KzzkT_KFF*d*fBKjI`=9^&m!JRBH-Gv4KmP5PUthob{oBvqynJ)}>-E!@|82TI{`em+`w#i~_1DjT^*`me>yJMk{`|%H<l*ao`RfnAUcXU)`1&!Qe*WR7PhY>_+t=GSFRl6K-~M{N{_^!d6r=v__4nhbzpTa&-~RjGe_223>j$mN^O)lPr{iz$=UjZ#{TJVda`?*K$FcAF%kMw@_}$;W{L1IwzfN8GviC(jd|B}+;RJvD^z9YR&$Ep2>t7YyJ%-j&d=Vbi?fTp2w;#U!R4#xwngNVvC`Yq?uDT=lVU&BS9h?{cH2ikGe)r|yf4cto`ZKWBa_jhjzbxp_pYNaM{7YddPo6<j&S2YQa0tNQwwc^MeZKx${`9s9%6J<vUNf+N_jTNd@jSljF^+BHr8AiukG6jAhJP65-5C9SfBepI`JX)6Ha=I<Cfi?n-yLDNvmNcMo95wLMN@eEH}6tfzjs?avq<X)?7nY%mB6NM7y5n#&Pj;A*KCe8CA%l(_q$)aE_0VyW@a3Axr^U^#=3)jX6yd`+vzVZ-K~#V_%{ApvflBjWZs9JAXr%Nu72Qxk_}x45PfZ8K_8#3EGT$-Pc3NqRjCgqA6NWP<$fL)*>mb+XA!)_U>oD-s2nK#Cwt&R=ixD|^}h+9V&C@r->&~j`H<Hif4qMC`EUR3`s?Q(e*EEoFR!@!C&6FL#26rSaz1nOI*NaW=Wczwcfb15xUr&nT&|zW9ezBerT?xtKc4&QtuCLb^VML=%3ZUaMjOw$_oy&I|9i|z*4-<QkNKEkg7bT7y!V^t-L{@Q+Q;p1=B{?m-3dD<-}TA2vWnN`)ZRS#rL#NyzlM^3?O*x`1T>d>i1LN+ErqaR8?#R@i}~5Z<vEMdyUe~XeDo2T#y&5!3$nmP*m-(+5wsJIPhQQ{AxNzza1+msRx(!-&YxV(vo0eYY&dy@u!G@lANbc#zy60hJcF$A-3n@gFKM~&!#)wl%KNZ`hm>G8^pQ`RH*k6nZ-DPi`TGrCiXP{BN-WZKX^v?fezjGY3B7{>ei$w*`#^y9uSOy46IlQ|&d?Dd$K&sWNF-d7E)7M5z6i@5Nk63?4&NIIUSxyeCo&7!?@Hcl&-xw&6WIsG`=M?dz?G4CdF`6p0YBE_@W|9XlF?q6=sd!r(OY-4wC<10KG`|qcQ%dI+GlT{6~ogi6XD`hz;cO?pU6_zUAM-;FP0O$5YP2X(A*@GNw|#MK;uVH`)r6BRyjhQ{#87;4LqXG^N7wnmMCtjnSbDqmtYcn(;eJEKN$C~tMDM07xwsEmogN7zPvZv;(|mZ`L>E@A9!uT7uC3N9^ohL)(w9G;&j%xOZr<M>}FMYSNGE^p%@`VX4lwH-qd+lMH=n7Fp2N8)`3po^GX~e<%0kaq{6RCKQ8w*2d)VBs-Eo7T2I7Fo76Zc=ozOOGc^@Mf{*)-(wtiDH37f?VkKZAFVD4~!%m_sD>Ws>g|KJPu@Jz|I+4sIz$N%10q0SYuk7>Gf#*^9#4HF*X+Q47>XYyJ?$_5}vYrVD0fu@wivywO^5nH&A0C@?9$36Rh4a@&`DEvl!RH|AO~E;@O#gwaW&1cdALrtE5@dKPb$9<`yF}-mRFCl_J#A!>5jJw#<GbHOb|tFd{ajca(^(&r=H}#_{oUjJ+vi_D-Trd@_1FIhY#T)e(f6I37(ge21YCkAX5r4=>@{EBj`;qR_<(W#;?+{C55J!~`1?K1_$ca()UT5AtzhGy0<!ol-Mtaixh)LZu0$+73)Szq)i6(Hw;?!L!Lf7ZbB@4QmDJYC8S}W(nZzRW6xj3ba+#$yee60+nuOHpVtn^UQXpNY4%q#JU6AMndIIQH$eqLexp2LqJcn$5J(|i%dtj~G09M5Qw`lqgpZ4|jM=%g@(`^v-`UiLbyMig~C6p0A8I&Ii-AjPK+$i5gWx|iYrthtt@nh+osYHIz{R5m_LJc|I{O9%0uHSzzQRYoH1EhsWEH3k;6-UyN+u305UKXfv27!4i5b+Py%x^ZA;pRUO1P8M6iBV!zQe(!qEVERpbjZE<)V}>c*=42WuY0>|gk=NQmO=@sC{i!Wm1%rq2MQjOlE^Q3HK?c+nBcyG{qyTjpFY1zKo5ZXY5F59V~wkC;5_MJj_yyi{l%3j1{p7yB=Q0uU2Ci?2<1+zOr_B)uk4lW)&RL~JQ`g^(E*6W=~bdRK*vkkKdPO|{R|A#*+Iq&BFB8^*5+bIR^~}VU!6@<0+ow%0y^`obcrhm+&zf!Qgf19b<5r2+;Ed=qBOtB=JFm>mFUqy_TyYQh@XD=@!x-0uFK`J+hOYUGMv1YL%aWh4eZ_Ynl__dPz-l+^m_JBKyWJ&rJ=q1_2uFG_4O+o<?=@jC~w?u8&NXnFeX3fPb|v0l66Z#@)k7TU0ql14&-Ck;#CiQd4O|b&;60UK_C|Wi#YdbH!p<pYXea0Lx*c>UgyI8w==9or4%#N$o0;G+xSpQ;q3>s{E^AB+|AQIg#PnqU%i0M$=2jyl|_8_2t-|~V(9&$XDT?bHsVl9UG-c6KnwyB?=}v9LC|<S;3W#n=*y1AM|H<yPlJU&+dKO%4>O8>6j)(;@ZN6(RB-3k<!iZJwvs&fDDUM0^GH^dumB2;sCX#y`?dN-O}*!fhUFH<M!-egK_wDBalRD{|E8p)Hl?qx?~$ZGsD|-AJ3a&4)ugb<7wWW1MQ{XUJ5WlQZOtid3kE}ie@egX$Z>CyZ~_q5B+(?H)BCzPV#QH9f&}EwK!>Y*>cFAmM6ffd(VF5*O}6zwBBS|Bu_(u6T$;2N#38(A&nEbf_e1A{>6N?~4$AMx4B&CQw5d_ty*2dJkHqr&z`sA4qZI#;U0q*ZA|~u5A4fg>+0IiJ=Xq@k7eM<)X4nmn9)D~T5h<!<<oib;zfFBU#$NhSYHsI<A1SZDJxaVhfFYS-mOJNjvUD*x83o~shcsZ(Hn*wOb=NFxVq;<8KA2Ll$Hud)1W$z5am)Zc0j#J+65?<^m3+*XN9asTI}31;cuKp<SP9sN9|}!nyFMW)*6D<C2j!B<SS0ngS@9d7-$jd8VyZQ(XAjAq&fqg+MfWl&65NpgG7=vDsISWdyXV%DAkgkv$HKB_@D^k0=>0#xZ^tu)kA0ckVuy(`wPy=zL^gQIcm-&qBw2QPh5yLx6GTCpJQt{hB${O*NnWKL<BX>J_VNOOa4E>BLOpZnK_*s2A~vI+5R)gXPB7FbQ9puNoX}B>8N)A82^QKdqr*hf9&32jB-xqv+zA6|8DF|g4r|h~XEluF5-H%H+UVczN*wJ4G9Iv^I|>3L-Dw`^9T}|hQWA&M21!wLYH`hEWT%V<guvKgzPn<@C7BG6H|Vp=^g{_Nv2|LXZk6PCgBbWoMen%~DmS|KkC+7t3e)aVakQ*Wv3xWry@+VYVxt`<M&!r4_J*%nQ=3yxkQ{1zrLbj=kr$pMtbhy>*;>uz%gn*Qn#Vt?%rkl$(wblD`yeit#j*fp>G4k@uiGUbcfu;-M}c_+8LD^Q$~3BM#Eb%qS%t2k<eo}+ps6%UcMkDl3Dd*}3D)AN6a=Du8B@OfT&I})Wyn=bg$r!ox9YuLz+9+YQ0=F8xyec$i1he!j+2b(lyC+wNoimF38l0ZiQ`ZpHaJq5_A<tA3YwaJ|N8pdRZ<mEMBc)mfV`ew!|FG6Eik;l*KEK|q(GC8ELegDsg8+YT`ptpeGyM6iQ#%~R?)&An6QwSlt&99N4fIrC`aP`E`Az-5=+Dr=n~b!PHN{$$ik(2DMZ;dGANX=ELQU{*p|!v^BTP5XmNFvg<OKBWqZDCS+c+`j?q`?>N&DGcwNUHpX`(&ngP=VLVrL%1gPnY)%sgc%AU0S);mP+2M5k9pP}|d@JN)+v70h%6BL1?QBy8EQ+X)Yr_N*t=`GQ?YVXcWI4QZbz|z0A*@SadGB=0_8)ihD+wZ+h_uJP}3o48qEWK-8Mb-Bb0$(ooQVgA2tIs3{M8z<G<~_=#vW7OZs{v`nuK-2hhc(k!;eoo(j<*4Kj}+YB;`&i#Z`=z<$S*zkmEewlT#WZ27bZygy#TU_W<Z01x1lc86&QB&w|PEpLzWtcmA{~Xk~VdHU%4mLC4gAP<{O=AWh=sLz&~$|LjEFGM@fp40hYcg`INRSs%0&H;H>-8)$gn|HI>0L{|%&e{Uq9<HuO2&t(6~gRk0zb#Jm~-a^O_hx2K>hR+NT(V73-Cp3MSnzS`D`UnyEuvM3Lwq=Vd*`4`r`ASs*|CL!LJw2f1wby}SJ8y39qu~J{>vwFg+IG;RIm(8aHY#WO{9?<a0Eh@11MOC+1=~^E!GutI6%5U!+0P{vg<%mh@>O;uZ-qBXPc^{i`Gvebt9HaR;$4J!I<mK0nvLq`eNT`9SM#dV{>2NLOHHB&TTzyV`p$3Q>5sm<q2jrV9ekq?;y#Y}Fs2G7Zdk<8LLM7{}J=1(r5OODqSD5YxLX^OAgcLId3h=&t_T~%u^W~kLB<?-x1~tGVl0d_viu}N^g2d?NPkN(!O_^Y(th}KrjU^@P>dS0c=>pDSNX!oLnm8k$nAX{|ID7SN$9j_bU;}e5tml_EG-MdDSiy@}t)FXs5$9z6){`%hP7SXw0~&+pWEE~<<1l>ryWLxB+S+n>$t~m-HGq;WV(C_$Z(U}?5~{N9k2nuEX2dm^InZt@nM<RJq^8Pm2*>p7-H_*BjpLs{z=Cua#({}BOXwGAQD-V8#uWdllyz`ODrz0A|A~1m;N_`X8Oz0pNZcT+rvD~;Zk+7Wz49XyZ)jyBR6C1l?&3-ks`vnO6pa1Z|D^MKp^1ZVhStql#?S3Jjc#P43f*4tYLdR_$|8lv#O?>&3rO|Ni2(ai0Eb>%G>s=DxociZ>FyHVMDA$w+7Llx+$|2cR$qH^`&oX^RC-k?RtW|Sf_mmoqe`cI(_=t$w3iDQSyjJ!uqd)IdJNG-5#5K_8-O}Ab-AcN0L{K%;`IB2mG!))yHPMptCB+P5f^f5pjc9ZCT`ghEFfXRB(c={h~zVr);qunup_ZE0aRNBbrDp%7~T?{29_bKi>d%ECaU|<kEYLPsOZrFl59kaGG>ERcCg5?OO*D+=j)8R`lz<3z6t|gK*_OrdH?WWd<*9Bb&xa7FJYBXDEH!xvriKSq5?=N;Xzkgh~9G!EoEp2H6UIJz0##-RU?QZ8C<7?;B`nB9GiF?$ZK57i-=wVN-bDRS!*(xe;UKKD4p^aL}4m@>oxm~9G3SBD<|`AnYK2zy%R&M30I7A=c!m<D^<o%*eNVELpc(eGBD280&Ge-33)<D$7$&Vq|5TeRyPo=($JB@q=;t0PZQ0kcn#^(W7Nn6RAXJXQnk4(3vsIS;KfB%c^~A}V|tmql7ZIak}}ostg!5voDM4PrV~xgqZCrEHkMvXDTs$<@lfB8DkPF?)>I)c!4_VVI~`-CjMc|Vg?VmAQu7JA1H$GB?H`E~lK%;SenKOy%o$O1A80B~@7GY*u0Bay%77WfnT^5okC*GPM*-a3Zk=))q^98S^GfwZ3+}eEcn{hpn>JP2L0Z8fP8cMZy72vtIz`+Vxy`2ZGk!NwufCxN&O%}go)W4YNlP2w9R|i};+I$|F>;3)Z^x=9fk03x`Ff8r#>$p$4}D9iD0t1)+Z{_(fRS1B)mkd7k_f;wFtrgIo2njfQ)sBwrx)&r@q{W<$UFmu$dxEiC?*<#qUTRiR7Ig3KG{AG`ID1=Ez4<gogE4V<eHtJO$<F8!dn19Z+L-f;<tc&qOlS**+s#h=1=Z@wX`!Mw&AT1?$P0ys6)LNWku~8QW6-ve4Wb4u#`w>gh`c6ci)*!qF+t+!xYKNGJz}8Sf!4n&oUsC+$?qmN!+**Msv5MSn7;C(QB{ky=dfi0svh7un4c`t9!%ZM#MT;L*D2^z}5Wm;RNjbA0@);J`-MdW0}3_|Bj?=Q;ZB4161~j)m&o@0USp6RdSKOn&PqK-6(QusaqyZRH>N7nYK))TPf;~Tb32ft|>~&nS4S`Yq+ah`>rt#LPwJ{e6z8)m1dzxpt=8eH_7KTcmpc<Mvo<Gx<-}gb@9dU2F<CkKsp4BiyeqgaP%0Sm{130rLdmh&U2hn#C-83){bsorfo~2dfFZ_>P&&J(AoTcYrxQKk81&1#-6KB(c@!^#U^l9u`Rc610YHX&?h7nr1;{*j7h;EYSw4BjUh<8xsz#3^>HhR{b;EbPnd@#L<*=%puX_Jmc#J6@*;2vh<%!|eQ5PFVYfQ_DCi12-~I4CIAxO7RMZP1g`P?Ybcj5r!=Muhh}|CUmy7FuP^8L&+<(7}|8Ww4a>@20-9Rqw**J$;gEwG3X>e6lB>?E99Z?y=WD$YwbVc%6&2GrghWeA(nnR`^fLl2V%%6xdaOu7i1a9R|i+^+rFDN%1p3uctMHD+&QW7qE3R$!a=l_UO6aXTXDUmA6HH;=G1FWFvaj9U=TaeR`i2)|)Ng$~Jo|;5oDk2)0;aNZr&#o0JeljsLn1+db^t;<&dL@hne88Z~h+bVT_d|^+GGaHmB~uHI+m2sJVMq$WVd@1H5jz!iyNOT@EFO=xmIV;Kt*NN)(a7?IU^fCrM}V2c87nZtC{YzuGuiuqS>6-iyjv))fZbdvXRgR>RJy@DiHfaRzLS8N#lX4RjXJnWD1vT_i0*9wcK&xCM9cf%9sbY-YvL+#uQX(DE9`HMvNGezHc~10MrH6QOz3p--Htt}%*OP+=qE@su+1H^HFARHgJaBN9QC1UI|6K(PnRxEnC<rmO!^uJZBzWN+lhju(NY*jL8AeK>P(@5SBz1hU3Ug6>LRx$Q-26~4s<cA9Fq;tWH-6m=Xgp;{E<r;bZ*O#OkAk(8k0{P)Lj?V`2Y&a6KE+niUA$_5&whe0Wze+)_)xNBU0_hAkmLr3_tu-+YUw0unnCjnqI2msWHh<dm05XhQSH)nM~J_U#{yTvEt4E68CC;gOMgWcPDTJ%g?8EqZQF#`JzrPyC(%$f=99@p{{2JL%5A=9m3$s``OF+#BGPuK_XaW7)7%pSn2)unZjJ36u@Y5&_YW#>}3N{90A{ynL=HzD<bOtzH>?rLEj7Do@5mPLq{iv>c9&zbM#VCi<COX*Co3IDOS()1bN5y%9g~Hvg;mCM=T9e>$>liP8!RMws}@_DJg~PdP*OYLDIr>UO^A<AaeSSZh_FB@KMQ?(8axx4%Z%11x_eoEvk@1SKsf2p$fF9*=AERl-3~E!`1DnG(aj_Ld6_)K+VN$XqN};#z(Exb-siOLJ{o3^1)pUn@eQ7K%$@|UiiQmuE@$a5PF_;lNayOi$OE1PorIP+nSDaQw(*GBN<25zlZZ*?0*c2LEE1^5)Xi+O;KUSW?_W@AC9QlV+FtkD^vlFzgk$Lca<br9Hmogf>T547HD2M)YNB!BVB?*bi6SWdq_PPLXO4YhxsY>3en;m;KMRl83clgqUo5dn}BpuU7-vtbx=6+Q3-b%aET&;N___>`tU@li>D>!#wyq&RDw+puULAQdw$7=gPhrt*jd_)Mmkzszmk_zJrlyBde+V^2rVIzhe+s^CDGNQ8I&`?K(<7@aC^S?9!E`BgSzmRi#TgM_;p(2kdh3JJ-PC&P#S^dFj!jfeI9d4`0g6R2z4?mu99@_PO6iYWaok9?CyTI>m<aa6U*#uFK&zIs<SQBKm`c4T4+;wn%V0VbOHk{5-bWrrLkU|Uad#`O9-w<2Ygfk=eXh+;K<ixur2dVx|B?HT<wCnTHxwJl4A@OtE5;4%_$)b$}3Q|eD4x;!Sz;x!m;DMG=eN6yT^0txjy9y7P+6Vu-k_xJm<u2JH7tVUMFWuL-|hviSd*^Y8+mckw#P>{jnugQF9T2J_11uo)aNp*`b{%5wOYCh8bv55O9&yxS*V5Rp4$*t4z?uG$D~5Bia~6^)^+vWu0MJj)8V2CyMIvAp^24feS3ACt1*Qx@?Qpss|4U472jRD0W?m&Lv=21v^O^1`;%y0Ah*>6NY}^t;*%7)k2~8q{UyB@M#G?4Ql6L_AXI2>G>5^j*n7xxMvP(!5`uyMJLvyUq~Ip!}A*yEM`b`JnUgaAv_==Dt)GaAXG_UH)E##tK5+)r3-l#T4a%PSE)IjfU*hpkRX$L;C;4b>fyv(18I*y{@vY#94lgfZcRMd=G1OjH#JJ9ePGPMB->=Zie=*&H3k7|wUi#V(3l^EWZObp4Z*T{mKZzsOyW|gFhhbAXB0VnbO=bb^Jv-jW>ZaIPSoy%#4}4D@q<cW!ntdS@<POQi@FG;8>{>|f-AH~B@9zXUPi;(j&c<hwL|9_o!A#g0m9pwP^HS1kbj95(uqjjm_6SY^>!8bEmBoGRam0QWa7TBa8Eesh#w6zy&<g?(DNb($8l&K#j+sD!a1ufst*Lcx6;@68uY}%eG$yg_0no$Y~rBrh;UUoc%C4VTkbmfv8VX(0kJ1kj-v$p+c_4Olv~e6`7jn{EP^~I&cYJ`Yny~@H!cYybEB&91sPe@tIESLw66OI&0ePRn8ZF{W>Z$?F&<1^K)|SMJTVK9MIwDhg2t&Xn|$Su)Z;m1a(bC^x*(*e5?t^YGNFWqPzXu6CCcT)%K;hp5r@Kz;;D&Q#@JV%c}f%7uzQ?2Zo1?kKqL-b{ewPEc7j%Q8c`?UFenn(Mj^D&jCiS)^gwkGNFOm@i0q0h5lO%VW?&gXQ>s`m)gYN4d~GiUSr4Ai5|VWc@b)ExpHT%VQ6Uvx2!5RH%1Bhc+Q>yL{7InTI<_PCLhd74!;onJ)bxM95+UAwh6{TLT#T&jN-RE;2x<sWOPaYv<ZbHA-6t1?FhM20ubC3iwle`?*olS|9S0YrsD!1WO7}AM{*2m6rRaece=E7|<D;2_4l*JFa3@%Mjo6hZ=S=-J8bBdOu0HES&Kt_08YWcot&c?x^D|J-X6Dp+vARZpH~$vr6MHM)*IjUfF@gG10hw_61k;OPiC(u|dQF=tfc-fa6}gUY&pIa>w}ckbRFSNn*keTJNMKal26(_lxa%cGx0PF3=f#l}C2x~`$uZW=-xA=3kaTz&oe;F6G=3?!JrXw7ymley-04=3d_Xt?QFWs2xu_G9W}pud6MjM_sIHx~%7|l#q)|oXhx~n7gE%dorAK8kW856uXCm|Uc$;Z_cy*m&tt$~}?iHM~9oc2wq|+`}vU>;_ieBoQ(_eZwu=Yvk2I4zWHi;>8-&n8`l%yTiY!>gOY=lY}+B!5QsX5n)CrOiN1071m9A-Lvcok8$|B%F9>B7PbQ7C1DlF!kA+=9R**VsmGC#@Fi1a(0S7s)&%)UP81WAX`tgcj;s%E#oYVTm<9DQ}MDGn0V}_;azGnqF(fj{{8KG$A6he3@q?bSG=1fAPwy8q)2YBwoYCJc_&a{_8>5#Wf}WUKIz-_cJ*aKT}#qHl!79(V_4$!OEb_S~!z`Wg>_Q3cczbRQZ&t)1r$M@q|9}DTSt^UP;54^*DJ9Qirrg5QkEN#iTX}>meW-!j6YtDn5&&0BE(%@IIJ|i91M?v-j8*72^Jk)UT-)N!<Wy94ZK&gfCavqb=6|=RK`0^<p@|gX1)rtI*r}RF-|66`nwsf=?);J=}~fjQ1`lwlyoe2Nk8#CAU5~$N`hPh;;*~<d%d&Zm6)@@A0YiBFa<rNQIKDxUX?&U&NfaUIs=@B4%9Ygr{rNQu2|D)MV%oxnG`uZwNKvamS%ZzgAU#?VaGB8~GdeWfoA5>JCdR%4aNXnvc0@4SB~5C6H@dk%#Dj*pWX?m0U4Be%?(catj0{%yjFF-~wZ8misROeyv7;vMS}A3!9X3zNrf<3nPXt%1Kq0m%(M-f!h;c1oL+T8rdzU#L_0)WJk|uv<1O@^@ev&%Go{!yfqYZ0PP9dek;Kxi&Gz6b$Oi9N-^3WJwTUE$mR^U>XE<YJEzgT5?gsx>Jzd07Dk_mwu5TkR(F2{XZW!wmd`?R1A*3!RPog1pr-i`MVQ33VxCy<ofwwY7t}Y->CfnBlcci^9L2V^GS5<$Hen54(+P2l<Ob;uFG^;V?M1LJzicDl4~5o(F?2-mlK88Yp;1x=ebUq89tR~ZOd)7Z6n6VpXvWCb_iO$mqvKCAu8cmRG;|DAR)fNt?XuYZ7oRE70&0|+lxfSb4Jo#z#q_m^OhgjNNdsrvB<ii3Kfcirq1*&AGo6E+SpgZpBWAwKPTN#)NLGrXt?-=6NN*HqHN4CUNWYp@)5UpOKyAjq;<p4z)Si2)GdG_q5oi^=W$SVN@?tM<6#cRJ;H?UkxqxFPAVF2dsjS<8H&9)`CD+M_JE^-Q05*+)s2=yn4V%l=6o+v&2d3{-(-bA+BU$Rtab?T@SLR^s4{^Jbra2R^M9`0?zluC-@`H*CxlLDD$ij-$ZffyWecnc>IGshb5tX{9#^Oni0O3@<k9+9-P@<~e#yoeI*lV@wc4j=l0Cwk*?&&bS8EPd+W8ojUFDMO<-I?8~SKhH*e<9>E@GgLn@xsVD-j~Pd1<nqS-;O-QSyeI#D86x2q%=gMorsR+;?!(ln^P+5de7!B)~9c4iAU#vLE6Govz^*U7^U%?n3Pq{0%J-Vzc2yv5M!#^@%-0xgecB`MOXLSA*L@D&urk=#joDlC6(&(FESPbf)SPjAtxW~Y57mjrPMs(rzc1Pqx~74gV@B>m(~x$f<8eIvhj~lt4_p+X#}1tkoKks4DDyEXyk-j*~TT3kiEd@fE@nxrd}~t(3XcN03^h-ytdV6RBQ0{R5X0g$sz-oC(L##-fN;&E`V5L4El7OsUI}Vf!hY1Hr~j)K3*vaYMF<Cya<J(fKF2*Ra$yNn|ZXRZQ7j635VoW=V+{cMgrOl2otWs+k8;vm`%QT=Pc-Kbd|DTy{Og7Cub|`-Evw)#mX);d7e#4{Gtw=raH-CV$F3_*ZT<zYoS7`;R2q_;N_~2cxj%p;7PE~1f}~^!X*}g5AHXA^z;!uJv?4&9pLIwOFe)fRHO+An})@lNP%Scd)DO0s=|;nV>cp3%8n|SgEaQ_#$24!Am5ubnv1C{G}dGPF`Qa+9!m|Y23ZwvC{eE=qo`SG_SUf6!CLnqkDEY=4yPW#&L;Ae!x?lsfU^5qRbSg&z8W|Z{Q5Jq8XpCr6o+k$C@7)NJ)vr$12p*rUW^O$M3QTguu9JeGSM?Ko<Lhf?2wTvZVH@nyDF{i;j+{gAyFcTX+CWebpc4^CKvM%3|(D0fdvQzv?W`WDg$Gsq~s4!hq2<0Pqnq>p@^TVC1FlXbRVogyjYgfaDn$yb=w(BH%17^fgvQ3Dl|I6A?vnli>dekV&9n>k&K#@v_Kqw;5Qi#Irjci($$1^q#&u#V@1sq3B&?iGSW+&z4Re7M@{iFecvi-{7p-6=C+@;8fMwe$XL@>E93wJ4e#Ko5jB`&{H>j;``;n)e7W|Dg&<Ld6BTaE#PS->$rP=FSSZ(em&d{s!=g<RJ@G9+4rSBIpIPh9L{WNFQpvnD4YS>ZT@vEmbj1>aYZN1?g=`})hQ~_0dBBx5B{<hv{3cy1L^;_39;&m4yz)zr*rWe0HIb&`Jq^$|7m6mxm8aB7vA+jb&+|)z@<06>>pQJ?<pF^_3_QblUjqtUebrc1%hdO@Hh>#FOk{o%mO>hs@K#KaqEgR>;jcgEjHJ5@F|I1_RCi7+SBSY-YuiWq+@%;qB+p9O4GTxue{sT06YSSF+d<CWRb_+I);qU49t&VY))Hq^T~d*cvLiaPmfIPP<@b-&rS;YJ2uKW-bFdT4-Jox}($SHzNdq!$U1bbBY8op8{FX<Uk8!lRGYI%Q_R7VoRknXN*Y1A`)h$(*XAfBFd<H}ghqYi1o>ATi8;EJGgl^9WxQUPkJ5xJnStD}ucCqJk{IvKk|5M!?#|bNmL<SetBQ2Wh$SYzk7mfNPgwEF69}QO7bV_~WeU(7@83F1-J%a$40)!dyeT%bJq}laJ<rc*P1nz3QkBm<g_GF<oY#Ei<7sKAv71V4BgX*@JM6p7q372|VCNqg;Sx}x(6C2in`i#zr-<CPPDBPYc7f`l${6{wTGP)g8eRuwhwmT&G?8fY4qE&O8rf$7HIZXqOlHG?E)wZ5mic+e`P8AmOGSZw~!l=!bas}cZj6U^+$vGG>p^Ez_Q6ISP|Cir?`0=~Hefzq;JzCFc%livoH?mGzURJ;fR5^ekFKsCe@$A?;47@Zi7KkX&Ilv1$DgK6H(g7er75^>EJx~jF>5G-{l8E++!#flco2gctq>=-yY}#&{d?+3OO0-y#5{d=)_kfelRpx<wNgGdY-*h<Nk$z9aRk10#Ou61o2r$4al9PdDDbBE6@JWRvj&(u*Zkfki-jfpT!yenAXiZ*<n$HjUudIzYZH6WQ(vePCEC;2}gE16@E^AHeg{_3~e^Z*Y<fp=Ij<HB-bq$Gn$@L=)|0O7q1&%jcXx=*<2J)y4`!kIzFTG?%po?!+=aDb}eYU{?q~U;2yv+`U)Zmq*ebm`0@-o}`$pUNS4ejh!zH6VZUkOean5FpG@0yhdw19IncJp+5Q|&$BRQto>51my>pUAhVFN;Tj_}aKRDQL9~<pFb=dVKrC{g>fK)m7ymCrYNTG#6q^+KnF$G2Ns}#B0LKRP;{nZn2G(yK)id5355;w?n4j5tTKP#Lx>cEwNL~tx(;Mn^!iFBf9ZK5@R0(MC9ZBoJ9;mI%Ap_0bbT{XaU569rYUtSY$>=oZO<!08tGw%3$-fch1mgmI`hZb7|aPsyDQFXC-rb;X*%gn!+ZBW<g#O_#Lue$z3w=r-kNHPT-aGfsbnF;gnqb>Iq=UbFdvYF!RXvxriY!Ptxrt%uVIiPidLXPR-q@K$E&#pcK_RNh()LlsX#g0Cbug4m}Xa>(evu6Q{;8xSe{01sDKZ|HWU(WDmdKd8WCCgqm|<OEt*jGJBmx@!~FX<Fp?@0Ys4BzPEV3uq1gZj;5JWq<scfGt913FL&|J!g`m>_-|mrnQnaCpjyML|NpY~0b$#|6XDZbriAWrQjo&Ce}nLBCt-%?Z_4vF0E8A+Ws`-3-g;Y@2Z<2|Z@p&fc>VwJ*7}$ieg9)rwI8XQ?lp$Y2fDyG0pN;%VF;?S@_)jORJR{~4=lSz_6LUBIzQ;-6zkU+_0huN{o{Xp`SkzypZ@!Q{xARhWitQzP4o3Tn!c}wI4Aby8C3Jj&rLsM+iMLGl@6?EForSF>V|e6H`}X)Rd0is<i6zIocR|+e#YB3&()pBQB(I*Ls{YugJt^5A+C{eXf2z|(C6#;h6}v7A1Q6jGuJv@1!ENowC@@eKYsf8yF29m>E|DQ`t)|A{`GqO<sCPAn@kfdHtRL(YLWyh0_#_|nA7_{LbvlZ+Iov=m{0Rjh_syZkxaZ!rjwQ8qK8{7n`SjWyAh&=@AckGoQU<#A^l>opMQ^wc)&o8_kQ_l$O<vSV#jgs0)5|pKbxTx3%w0@ga@D5D_bC`oipul9NFX)kd6{$C}dd?gcH?^!7<M&&)FFf25t39F88*IUL~4fx&L4d!d6HJvMWq<y0F;s5}kCU(im+z=yaX7*K(kZdK2uQ0#YOV7!kM|+)fL2+sC#}-X2gfn0B9BzqsH0F4+7I7H=OmlXp}pHD(Jt@ctPwRXn3uhuYWZs!<v+aHrfo9-_z(@U6Narn7r||3Rf(b=2?Rdq1XwS%2G}u)ot2hEun<^V3>2ooDd84QPq9_^wGmP>g8ygP1P4?ok!WJ=LG!J-}0=%F^<R7f^&;IAGwrTUES=eY(|dq0&@uU)<G6?vSr~a{tbIVEOIq?Q#E1eO;60%E3AR>_m&sKdU&v7CKLZOm)%w7=T>y{fvBFVTzngV=PsVW=@&K5YP|BN!7*dw#A%uf*S3G2B3f~3E?ka7?w=49x`+D3Yz>F_tp#LIa1-A%0-_Ag(CzSpta8Vq7$S&n-7~nOAku8-E;FSgd_@AAFLNe)Mz^`bDQs|ioy@6ldTaecHO+WlN;Tahm!BACR`tHYcE&xdQrI&A2SJi=CsdI90JM$L>&;_Ri8(Bjmm(=LlG2jJ>I)XturU6L<nRQ*gIIBIlny5ic{yMK8hk!C27d_?_DnS-^(T%e{u7SC^naOJ=Q0zCv;woaB2CwpjA<2L&l{ORQ*v8-%Lv3s~TD&UApwLL}WmRwmRC}iG&-pJ&emhNEKrgvYB5Gn%-(T#CucvatX&&Y{w+OsAm>84F0-&eqdK*443F4*0jlN(gTbWsZ6|$VOGb$^u->&_Ayylw)SE5t?PKAn;CX~1{2nEgSV=-X5eLQFVXc*W0EMcq5lzuN@^ayy+p4=EPhXPJ#7L})@O0<C?Sp9URs%5&#cH`J<iURsvgF&+l!vp_OJsM73n=Xq#|=@CVjA^tdb2_2mo#5y3}<<gI*fL3y~~vgYw;SJOV9p3}9D1E&>`du>7IuXq6l8B)7VuS|^B16hwPoPfTzTtYe)cABq+2h%E)2vT)5%7y0mu%9NxWDGI&X<{~Tc;94kADKp$q7`?Ymqc<8Mn$f1b-(&=lKX<AyzT0Nd$|5y19b03NP!;`cP+f%ro5ZD)60_?ddRb4Fgqu25ATR<wbL<65Z8ONrN}vNp$$^lY_pvG*?Xrz_r1GC#hP3=FSq2m%-S2`amtTD^w~M=Y4C!*s2!&Y3J15A`jKM}&$pCp+ofUB2BC-{Do<TE0e=xR0)()a&Jl{S?q{}N^y1F)m``fSE**0}~K%VMhSExaNW%s;o^Zq3Ok2vsLZk_R$l|}7T4uC6+6_KZXjka|NePsh4Q65##X1Ql33~ls?FVKJ_+!J?nV}%MIZD`Fp{<))=@?;Xtl0;;39magtm{PrScv>&Y2o=6|yVTK3m^J}%#X+}%R5zusL+&nmum@Hc^_w9{o*>KDc8%N=6Req5X%q7Q+fJrc)iAlq`nZRp>rS>fi-b#(>qIT8ucRiE91M#`?OUHe1VdgtgkF6#;TRqQT+dMiQZ%I%zNcY|InkP9i`}}ZmamLfm4@;nL7feDR&%&W^bkyBP?uGuSr6Mt<@CB}e>GQPf5~K+Kdjm3+fW*nshs*jP``7D%WdDv-6bT=JRvta=%F@6dwZQ6m5#$eTRMpqzK*O<bh}W=)l~3DaOev@!aCBS0%Mh_dJ&?|_zPgHW37ZB8eFVJMl=6jL>U*H1EsD2Q-|_nG&q)$5k-aiovZOK12IN}=EGwWU5vki2_N?%1t4s{$caEOKqjUZhGus8XmbxcxAz$g7kLKg8@ULf&2GZcLh4hQ$zzjwl*~Jvm$s;q#|$hm#+#C|#S22N^a^z-GgD)eZG>qT<@%^0rLDO)Ob<L+@R#Thz)J$UkqAeVtiye}dD5NF{5CUTrBIJG2%`&7ew{eGI)%^H(0Xaxmta+@E~fYh-{&+`HX-t-Lo3Gs0FvTk?NnUfhCeb*sMaqyDS~#ymxoOfiodhRipV$H4xp?gwH>0U6&RV4C)YG6q60)YC+qNMG3Z9em*gZKziuZYH%cRvg?02YL6P=bBJ4Pl3rw<3MwyQobg3lWKEcIFE!{WkvC*jkRI$LGRO^983QQ_<s_;V#kppPkZlMsTu(%hKMR4p{^sIU8@<kZ*pUPf{GN&bZ>sxQ*vTZ?y6x+d>K`GX*iqv2RIYh2uA)r9oRYPz^;XOP9_cEebghx1z`I?JCmDdKY9<6CLc^$tfG@90=%6+j8$>53)nc*IRF*p2K<%Q_{O_sx<<G*IhO4~yFfmNsE3f&VPkJ_J}vw3Mt&G>Xpmzstyw7S50B+h;-6_cr5Ercn+WbB~|t<o~2X}-ToKj=PzR#u(ljaluP<E`s;;ktMZT{wr@6BX1dgj<>I?-I|omqFWvsu!==VHFW6lcO=>G^lm$<elQFO_~Er+<DO+jZwCTovDhamY=UAwP2bm<y!*A0YMyiYTE5dr6McStXfu(d`q;U1{Fgg?MU9CC9*GjLf9c-@m#{`NZQ#P=}>t}NpPHih0M4k=9N-ysZa+Ywv;?38s|mp!FED8v@PUCXcI49pcWpIuvAPHK_*7l1x5ywGd_kvi-#z0&eI!k#@(xC2A&H5a-_S?2R;3ACN;?SmBoPowkQkJ67rqA5u*x7Mko=%$}}2QUb<pqH--8s;n*c4?WwXG_pwtE$FI0cLdJ3YD8AGjk&>gHVInw|q4pHgEtcndER7h=i7AHE%F+!&r^vSfHUR|~F3J%(=@PsRKO;{djSVL+<X<9ou=PhCcU-_0MQttZoXgDv%iD$Z7zX~LLMO+s>|`3>I-I^vkvw!LP{~9{1O($70&AqD9~A%a2L^^Qez2X1fxSP#N$3`$7*^cCGT?RiUV5Psqt}Q;5gsASvnYyAWF7KSQ-E!jmp;(O&oIO23PBjDEF*!Ec|`3@LBYDoU7-OZ*K5%Df_Q0Q%yj{LcWEmD%WQQJvq|3sI<+d37CX|qTQd=P>H55VhA+sQ{-&C|&PAYIA^1{brBFM`wNm#|2Rl8Uy(W48=(tayyo!@tvxWv@Lt`bz_aq^@%Y4cRec=T1HiJ<tb(RH^x^nzy!*X|#n#)<^LWb{;h(2yS$m|OJ7JyKkmAQ<8Aj=QAkFI@U2;4n4^6i=~DR(ghya=_+UydfS4mOgeXM}5|z{w4d!TA_!{Alp*YmT8Xpz&<G8!Dlt`-{R*rwTc!r_m$g)<In}%gvWm-9)B<K_v;-5iNN%06d_uf`&<FC*7q&cqP+|l8GU*aBV-OiWXsXHcb`RMIH@t2xX-Ogm!gpEAv`tW|5^q-2#7WyltnGr#L|v)Qo6oPP}#_<u`O~WywBg4x=2p-gCY-3Tp>hS2Lem)|EqKQTcNCkroV9VR6HMIrwmW=1?AnF~ZP^B&Ho|&UaarnCMzY#lU%01z{Cy+BH^bYO)B$UDocRS|7>(z;~F*DUceTcRYXK*H_o5rispshMU?_lXx-PXV@qd$s$LM)GfFUSl7wLBD&BkEi;M^kiV$9<R!h9C1p%u<%S9w(9@Y}RhgwHWwq=09R<tcQ~s17z6g-JsV167l|3+Zi!#bQ{_zE8_MdUM$R;zXSrs$E(an_=o8Nc}i%G&2<DR$SE-FX?(!#6<A?GY*8d_{&LN9apU_u_yU}27>oTMzqa2#w?sZWT_HVD#c(9IwjwoaoI&0Ie}eoPW7JPZK?L+bK`)FYW-a4eQ-^;o-bJ;J`1!4HzUrnwo^8X%%*bcLpkvzL{G>uSRcp-(W8QE%ZWv6`Zu2mFcf-Pk@~1ZTlr;?450`UW~b)j)$-g@yg=c$N<^%&;IoA^>@!NwsY5u8^?N%oc62gm(xn7wt|AjcTwo?t%cW(5^u}S3@fsFq7>jfGyAPx|Te2CoDOmCQ*YL2$_UJsYR2H)0zv%8f2+Dn{F6nvOVoJN|@g4FvW50Fshz4P~R{n8l5BtRMDd}$>n1S_)12XS$7t9VdqLh6Mrs2<WBpW;#QK~u*lhc5lKiu3M|nNlt{agce;tOf&Qbgfl}=R!5Bj#^&gPmA#+>M>})AqF#6N0kr#!F&;?#@&=gZsGkXszn(gi#J2~OZdU&Wi2B#3ST)R;Z#2^-9Wqo3zdLLXgasP*IJQJtssf~an?M<-FPU~(oiKuN)JbBDM*HuEANYGvpPehLDfN1~^gs1(2W59sp-PigKK%sQvS(~3jW2Xd7gT%95Mt%(6)Cisk*@sxhrL0)mxVyejL^dKw*-w{rN6zHoh`Y24K##Xa32_oe`JqaQkVPYewNsn2ai-Br3GnpI&4svAS8MXSHQifBWcRRq71jGH+<rQ<UQU?DTGVo&0gMP7Vy7&mK=@x+TsldwH(5^JSewz^lcE^loQ$V}K_ZnxYkJ9BwvKD6jQA)Wgh?|JnO64#lpfM3j?V?u@X%td$HYT*KdDOv8YFR<8FwVC=VhmFzMSiiP8oYN5RWh;YcO-8R{JyVD;P0bUE#Hy+tcmNqpT2pbm$%DLa%eDHdSF?l&?+6v{%Al%$72q`#c!4Dk2Xb1;fm8A0=65fQM+5$&qYMd(bQ0YlX~v8i(JpbzOo{T>>;tcTzN3;v@h`qiP-e6hR=Yw@V^XLHcjRDgAlQh^gCDq?=o?Ga^^2e<3avi>P;Mt$q9x3%m%04xIgrQ+k9@D~fil<BRf+!D}s5lk9%j2S%#8U=hX?5*=Qr4%fMlq<mO;m6Cb~iySIfR<&<U)I6m@J1~h%3n>pD0X`G+RvmjGw5dYggDy3&)O}+5U2Astc=e92B{1^gi+TL)b^L-THA6{sI1Y$PTyfhWu*y?KlP=u`pVQ133|n~ZU_OF$KJZ>Z4@l4DB`DyrEO8HTmx)4daCUi8Tlddpe~Boh4$7q3HKq1@{j{pF`~D&~PR!%Hyvv);Kk<%1U+9vsz2FiMfs8PvTW1@~_7_|ncu*p2L$L^^)6F__v7_Wg#{H$QSZLALAeDhs_iP<m*u))U!Sx`SO_b|LI!E{G3%wJR;+I66$Qh>941~qJ!hAiudX{Y(Q^pmb=sHEx_)kuQmi{tVbTfIwOg;)S=`Tx7RSP4|+d3Ch5|o#$a4UU|xJc*DGn8D(@n`~-$C%M=jiYH)1|Dm_!A}&0cH$A%5LxZBfTLrAez4Zn>&UulX#~v);*X9NKM2=X)9cucj>r(Y{Yxqt6;EW?CL$=fSnSP<3-&(;kpcBmRJSRXdx0qdfiJ2B(lI>JH&bQB7BCxo0|X^$vF9Rts@=Baa{?)W4Sh=#Vn<^++DwI#e=1*Qh&1aA7nz2b5{;*}r39hYxFn?+R`G={57saXT)55~)HZceA%Qs0ex30B5?Oy-uh6$`$~kqpqhS=8QV&T7m4)IAVHAp{2@<~nkFZW$w2yUWB3O@5maIfWj)k-iaj4ZlWqLw4r5&i>QzJxTH?DPG$j5-;<GYO(ivn$l$|^a3*(bT_GXhaYn&`yTB3>NNxn1VFiOtV4(-AN+xF9ei-Z@kgu=GoeQC;vUO$X-oj7pk6*yb<0`13tVUlS62cd0zYRzs8+4miOQAB4gT>jWx9KePHGN%D#{oQ`XMwi>dsd=#?Mb+Qm6L`qukBtoqX&|O~ny*-pc^*5YWx)-Hi?%^+-PiozNUstnNWz}e_A*J-l6>8}cHC4wsuX7k>i_k)y+tq(@e73qhNqv(@0Q0ig1eyTibT(A>$n|Y5Ny)@L0@oTv{-x(654$^&jHFNkq!QPOV#GQ_(>5JFb;GqiEs6+3V;>??y1d^vVNf;wc@*Qe#W>V8c$&j@{@|ESDM2@UK$%G~SpU0UUw`5EP<RivG&SG%OGW07%l`pL7dWk!Bu1r7-$z^MV>nR(jO<kn<CvjD`gW*pY!E&St=wHeRe|&yRD!nE#^FXhCoY1vPNWM&8qp3Yw+(IdEXg&(eOZin+ZJ66Lxvv7e~N3C^5UOy(QrSE=Vbfu72Y4@yAQI~Us2(&)5O_bD=7pHe?(CY;Ea2>GG2v998gV_O1V`d6JT+)xQf0Xmi(A4Q;q!+tH^SPHD2<=vKR#&RwX3n54nl+6;45K7Ag;$2`IyDbplHjL()$|GIgG0ATtVyY~VUt@0YiPX3VLuUZ0G<4>JSUV(j7KLft2Ie7xk+IOsNn^0&H>Pco+ihB_t;1;?r`XG}5h+M36HoOBkQoT&w};7OKX2vd)<!e}^9?@6wO>ENEC3}#R4B9qcVmM%jvzz3i6C%khyT@uDmD@}P&CYTi%T$8#4S#l!kj0|)hLaJ1uF2Qyj*1L*%|0rTr7BZ{=0!1B>Z9*OZw#Sff;aO)NXWaG{V8;%t)|d?83ys6U5EB(YBm*Uj)1IefO<`i$=FaSax+!>A6(6e*eL(odjE9TvRr5weP)Ow;lC<A(eCt$Zxi%flvQ<tY)hiHtGw2iBT#rH_LMgh3O)+u$-~KARKf|<UDGKqAhK&?L5Ud+BjP1t^IO2aoHHX{+BvvExh@1?<qO@{qkJj_P@I)p67UNzF12Qr_In9bU!&xy-HSMaf4ztf^OnJe5O)oGoVw+-G2OK4nd=x=${YanufH>!+mI~Pji;i<v8M04Iql8F>C`h3C3iF9P89^#TQDYme65!7B9u;+o9bj2eGM*@b_s}oL_#^B!l#@ay*0Us9L{{EAcCdxWgeH>_1?Xxrj8+6kroWCqglEZBW1agj<bW8G4GH3&GtI!$z)PFY$43R|oc=GvOfKP3y_uFM35mleQdtrmDWMG?J0yMTCiU<`#xP)cFpxdf-v^lMUZ*uA1YGFbN>z^Ry@tq=&O5M-vhbu-(&If9k=x;eW?;-y{hb6-0GeF~s%+?h!gTvOg;`b+)Dsgvn}Lx~BCfSPw3w&N2_DNLYr6+Yi>r9u3hiIjS8%w5U23@B6Xk9wshJ&X?~DwWrlJF@*cnbnLB)s6qougkG?X$KfH;oMLLa?%sfs44nI(Jt;LL|@in4U0d|TE1AU}cI9?jbf`sX1`asB-XtZBGJ4>hNo@WOYWdGb-%(j?4yl)c}pf)g=)7T2Evw^r1BJE&dNlw(*QEO%tdPTZuOX3%3o7fXzht)bA}$S4-1s)Mu5E`^~tmyDOkL8_y#5a=dmnu85ZqaGx#!3ir9fo{zC!rGzG*C2<CNi2tI3JLSAtFs*nIS%<uW=@+I&oCjjoB{Qf3JYQZE+rh?uBvG6&<t`uh8Il4y^DagQ;id1A*0O3CNwsmftf9bk4uDyCWk81b_kM9J2_-L+pX7&+8x4ts0+vqk~9bAj!QM^TH6k_EyU0)a)3pv(wKM)Vg^KgA%;R#!yeR-fbXbeRPk1_62e2FykU>51zwd=DFq@oDwmz3*bapXM|6&z(9Mi7;%Xs3;(loJRsTU8-iF+%pw?zgykDSK9$lWdX@@hMf*JOSOlww@mY(!&*D9T(LgB-nBW^upK(b2Y*{(=KA@h;Ru<C4Ah6iy$?^w@uXeSx=^t>ia*GpqQLjR3*^_Ok+=YMF1(9r5NIIy*?Rxb5Kkmhjnbsl;%TD+@i+(qavvRl5xD-oQfk=t*+Gw&XPu92@IQU@g#bz!83Ya6e_%)Qt&u*w0+d5Vx1rFC6Sp#TJ3@Ig~cO3F<FBkc9UjD+3;URj!p5iqE3c+Tt3`7zYiJvYA_RX>?YK;mUP*<Th6ww@}bOXF!Wn8Z~E<4%;Op0!o2PSiDrC1I(+^i)TcdWcDMroZG(nB?!(VCk8<q8oToNZXv`0_qZ+lFWu&@iY_yH?$TeI9yccCT`E7mJtkvxD7XaApB_hQX9yMF;T69;oc>MYz^bS(!Q)$Au(5@p|Fl}s5WGcJr(z+fB}vDBKejX<$fUB1WcqGWa?Bpoi^}p8~79fc{bW3EfazoNTpJVmBg%Lp3fLL?fxDBC*=pr=CM?A4*^pGc~#6FV$tPr!G}--65?*1&h<#ZAaeE5FjOc%%0P%tZ=pPv%|eFu91e1b?uX}KA46BuPlJixYPkJ6rR(?KuaBcLa9^ge-=@>6TF+c57EL<ej8$Tp!)Xkv@UyfN5!P>gc6Gpa(;n+&&e`xuW($;Qh0P6zVX8p5ZighmOO*WAU2mje>OU^ST*GIgwLWU>8&sY9$q^%?>PJ1pQb)kxky@mXX7&~fyJeCl+l0o;6B@jbG78>FT`KJI9QU!Qs9`j@oj^Gx1UVQO>@?S;>9;Ye(xC*ZiWVGPDk_vf@!N+EV^owAxQ{r6jYC$7O*6QT?nSOjN0&)rZA8%g1sNxBK874JPFn@o=PRdWs3qdp1lq+az<2y!9!FKhnq37kOvWM_n0HdT+3YCZ#1@ZE!TXr`wV)21hd91r%5ThEN_ZTG!rPolWiC7^;gX8LnOUMJEpeaP0Z@2Xb3Eg+q`@4XwLEVq<eeCUD_GI^q;P_cq^7%;wYEmE_3H((&ZrSjMTD<JFA#Lcq{iC&S)emQCfBCV4W0&AcNMU4bL95y6tYtK*|~9{T+&62NzlbT^}tElkjO%6%GM%<+?9-87V4y{Y4xxNWihj(#x^`b!$)pCA}$|0P;4%Nrq%IdpUc#Fv237qP!k5#3IQI7c2mqo5;bn!!Ytv#L>YQixCU<T!NvFrfvkN}9xaR4U^USCA%CVmv0Ex`3f%<&00EzW_XAe0QLr3)BhR`xa_H93PT*;U9e>D;Vgi9ONlN6CH##5~B^Z2Iq$_q5aTGSrGLhykp(6wKndvbHUU_W@KKF_}RMj;zy>Y<7A&W0hX3*_}ML;<N_asAVO22_kMagDBxZ(0L_&-}({np_bevTTO&QtEbA*=+@=Spy=J?s>$^sHM?c%8>ebF4as*FvqsT{0aj^`_glAS+BNd$|JQUQQfuS}t|hQc%sUp)|aXA$cb)O~R`DbOt!wo;?B6s~6fHmQZ$CrU<c`V+JO<RTTD6EM3aOt*es1$*^qhL>Hn})KtVyrvbpSo%NEwsow6(khz1P4X^)X2vY2*GR!hfv@G<hu=0zSM#JKAQu8~o8pR7IAJIwfKPIP8!o!TNOFz397{0Du<qDD2_7?a1ypz}KZaa}MGouil)cuK*J*$;;2B%sLXT0$EHA08Zp*MH@VjW8p7_r|+c8H33IB@fHiq$%yRxe9og0h6p<2HO96vfuD5QL&5WJOb?%L>oGdgJPKZ8ZI{Ch}t;w86{5zzl@cunIO*qAgVEF7jc&EYYv8pLZ9<2s0(?uSEz<6mSLvszevHv5<RWFNqDi7~zbStHc@{<7L+SRs?aG^^}<|R+#mS{iV$q?l*N9c-|nWa5R~^o-5lT@J2k_m&o?rT=ebXs!mrugA10#!>NOi%}l4sF;ln%laHzFMjqFd=%bG!PVn{VGlLFvf;^wzk*-#Xh8`SHc9+%G*Qd~{KtO;rQi2^TRb<C|9i#B>GQ}L~?@;tQKv>q{jfq!a`(zuVSJhOg;%T})Ovy`zhn_q8#w?jY4UJIT2}Pl89W{j#pER?dBj1@$>;P_+X!}hoJ5REG?h{@ou!Mb|rsxHfToG2J8En@3NZX4p3FMa$<Nt^OKo6&s&qg6RRpahOOrzk9$T%Xpc+-R_FJL9QZ6(6`Uq7uAUJ29>p#f0*l(bzfyH{3tr$~_4o%}uCA8k>TOHvv={g}(PWoK2ES72p&N@3dA4yxY~inoaE$wkJ>`-SSN?hKhZ$`!>-e2}sR>@o9e)><~<WgGLPj+yGul7ugCTg!g}=XO?WoD+_}t^r8L?DQWR3*9M6&L{#^a$?DTE0wX(gQ^iRLQoeCqXQ*5rNhG5HF{5M-eJMwJei9>$mNu-L)WVIo9n_Bns6w;?BW$Na@2LQcrHC!Ox+8NQh+Of`Sg`$&s36F&X3MrH2FbJ1gb4Mc%1?P8+4->t8|8R5J(R^1Hw!-e4Z4mqV~$WIx(|K^a3Bd1YXT3!0CQ|w`(;(6$)1IAes?ygJJ?pRq^ABP@*b&WpY-|H2`jsj5s~MNu4TxsUjsJUvC*gqnX;Fd7Dcs=b+Is1TJ~;e(sQ-cjCU_smt~s>Q>RKz`8qZgIKwz3*;p9s-ov9a%L#}lsESK5)YNe&TKZy<l+l~*Tv><&qCA+0h&gQivqEHGtjBw={r&<GWL@!{zKsx+ZZi?aLTtr5JPT;ZP3wsRfOfD;*9f8g1AlV{Apb2H(6rO=;0#s?mxV#{<K`tr}aK)UB+=x3G&oo68qkk05^M98V6}>x1mo>Wkn}VW5xxz{uzk5P!}K`Q2gWlYB~P%5k8u@2G$s%jQa)co>^VE$K|G87F*xabcV=!lj?;PDXCGE*FjXpaZaQp0#HCxG>Q_{T1Z=ze1$N4px6)IDd4rqVQp#f+reJC8cAxXDZe_6Z#U(3puqVJ#F<EwOi=E-K2*}FUa#<V-o1{wLD%^Gn|ma`h<`ZzA#Ha`IkLw&?N8LQm<MZF#%;b~!5Q=)zWep{7subQKiq#AepI@brax1(v2XwOHrGkvG-k9P0#$f;^OS9ci9yd^nhW?U?KZ_F(Oz5C^3a75m2}gp{WLWfH7mwaKy2Obc6a}Q*O-<|`Vu}+Zx(i+P@y#P{-sgTP9&+tB=I4}`To81mLG7%y+40@!>%)@j_nlk;A$wqwA@w}qM^hZc+uP?B+!#`ykkGV{`BedtNG<a6RG)7)NuXr^=EQ_1@5Z31J~uxyy4W1leKUY#IF1fIPbTx+T|jiTW)9x-X8RoQp%cG{Eehdb1>`4XZYXb-V8EWYM&A}GA%vAa%EWRkKq(vObWN-AA8+%EzIsqZaquukl0@i>j%tF|FbXu6!<B`mER|+->myM8v6(A2oX;OPx2q-=1HygT(6pCmyG;QO3(d4a(prF`HSiazXcs%KED0>$xR<b&d-z7dRy40AChwKZS-IYn6s)P-t==_U3rEEWw54ZxWt7gyA0mw36O`WT3te~XJHgfFWk}eA3y#4-CZpI)6YNr^y$rXUvDAezU{)$sG_eqXNd(IcPsij(1e_LFq6=i|I6<`{P^A9zMT2bzncK*F*tK=*gxBBq&Vu<*n0J5d)!g>qj8rUu9@u$2{c2fQMh?!UpFU8``!P^E>iI?^1V<f_uBz75jc{K-Mwo8T54|aucKOEb?o6osi}$KHaj}*79XB$D!S7Y(&%<|0mv*Sej`IP*&N?U$6nT4h;;vnFf$kaTt_m-#|4=ek@JU|5Vq?R_*~gq$4OV2sVHiY6N%e!Xiwm0dO+*<Eh=qY%(ZhT2luYIKgYlQ^?Lo~u^7`O=auQ{|14cVaF?b=Whx5|W^!#*n<9Hm+Moaj%_j3*bqny#U0sKgsFAOQrE7bmHd9{*9PgQ5$k9miYte_qLY1B?_d>6=X*lVu-Vee1nT*BZl%x&1@um@0UJ^DiT1ViX8h9aYXRD383-7J4DZRt@dapUXFL-D(8i%>8dF6?gX3~4|dMCr)A85=ffBfjPt%KBi)AOFGZpB35rFh)%rc^x^RaWisqCFk-f&#(A-4=0fDi)FLq_cLeR2^8&wq`YJschi;JGnsDb_u#~CF{&4N28gI>}#A@rnJgWL81W|I=r*YQ3TL$Xk-5A0oy(53l}8;!1ux)J(=#Q%{-|=D3Hjz#tOlVLb8rvt_UzeB*cR{A6-UI)V$QM3gd`TwA<gLLY`OBJ+xdWS&TAj{@N5GyLHVq7)9J$9s|Gj+X}TAJm0Q#jpSgn2$}^YuHQM9!8)1>Si=jy*@JoXvcgzE6C=HC+}FtLX}1k)fR6iJR)L3~=GOz|)Brqlx*vhTzi_0D0ux(wwd9h{jB-z%7(vCeL+5|WBbTfOijBvsdG^g_RtJaP4y!JFbfn+U8Z48?mCa2kS}Qe}&^vZ!>X?}k`_E&0xu|&o$C;uuA^IOtL}=E$y+jX`syGL$Y^^^|yWi@z+g@b#cgm$Q*jDJ%iYb`80dyjY?1u0)YL0?DXlAYZ6FoM0nPZwZzK&>!U>#mwjPNsStH9l=Fw{szKo9vqK?tM@-$(1ny0jNvmz|5!_+2~8%n~bk;OjT%VF10S2#uITTU_K5&XEwpf(I(|7-DZj`aQxs@ue(;iM)md-G@y?-4GLvWu1*dg^|OSu1x`We%nMkI9%>h$1cF%0A9{IsO}6jU~vjJ5D&;fUSi~!&~KY4RnER&UqQbt>u4_e-VgFJ6Wl{7u5ti{wiy$h5uR6Y+BRV#1;+2?KlYgBu1MWw@>y|OTVZFlv6iZJc~KO}!Z$6N)+lz{n^{Pxf^oA1GYI}^jwH^Cw{7$)g#sFKM+D9Q3NyRKO14d1#@h4cNl=m=IC*8;R`vo&@gL|maQ!XO*2rJgE*KtFjzn#ZO3&S^aR;W^%cjYi2-WBz_>G6!P+Ro0m>$KrSlg|2fTP|Dg^MOqaZpc=dS+?$ImR3vzChaw+Tk~%7f*pxts9}6+-M60QPLKk$A?u>5tpr!5Z-b+VGrf#RbZ{yNHkUCovd*e%A(-?46Bd8iKB*2#uQwpU8vQ<6n1IX7`tL#`nK%^ISjTE;k!;3Ek`GB3%O5nklgSxI9Lc^0;`#1IXScGWdo4UQPOCAvk3bzGUBR6mGB}hFq%;p?6;^vw2DHA&4mfpK~DN0UGoGfV_H|QjI)TD-v_Isb3)bO{u_ofOM3jEb*SNU^GI9hnfFxi-e3M+wRBz>-#2MJcPWu_)7rh`F|~Q(du~uC;03Idw~f3zL)lk<imM2LrS)>VxidpUJ&{QdOfb%rc2CelgL<t(yAdX#w+?qq=<v`~Cy^Qml)}ou0*rD}^L0@}Bj!$nW;^s<1mm3Z;{-_w>T6kd0c=3R+wK?n!3!j#xbSp<E3HNCBiIPc#@T-VeHKMQvHeu|fP?R*ecsR?pnr3_#ddO0^7?UYzfG_ax?q`s@Rn-mF9>KB<>-a!5cX6PAsIs}1NI2i<(o~M1J-d%nDTgH#(9!qSP5{p7p_?hv#uu>1BZk|U(*TI71%xenynH>$0n@gD%Ls*-M8py7!m;8`%u4qef<Sfqwv``H58BaK*f7O(H3OoJGb(fXP2Txsauwd#3-$aG9v0aPyr<+#pGbj+{cqoR}u#rX2P5OdijF)0+f~jt%U-ZifW3Y31*14&QxV?rFrjnRdBwEMIBXx$B^nS__G>idL_s=0OLblg&uRH2<dUL<OxLdOF&*B>;ZPp@xt3on@1W8MHs^Jh%~YSN{=yhxE;HE-ACOI$y#HzJY(JrqEGNUkhh4k!g(2TIL3i6_S?ui)79`{6rg}Q&w$UOs=s&fqIF7RBIglRwR&ZK8kmJBwbq;U@?E107;v-&=#=jrUu}K~*_h2K9A}yCU|%E~xzNVErv`jK42xW_gV;C`Jvd176n|Hv*2`+!cXdR;GK8ukiA;5(euBu>k{aTaMNZ9`qWDuM%138YCOWn94CFH&SupP&azdn_ojTpp0H&QgIHA#o&8lMeQ8-+B3LwE|xUn`*&N^w*3G1i_y-`E-q&gs;7t<?M<0?!sjWTnTH{1ZDvyF+>u4D4(r>YLMLgW+;nfxi;i*?+yu8eLjtwhkoiuZZ%UKyYe&iA4VCV)GQaXRI&oyj^d11pqTxaS-aeW_R?eSeUJD)h`*uVS&oq$nI1S#-F42`CkXm|MBPFIz7aJsv8TMxIKicasX4fq2Nocx<8%*p5!uf>vaq#oU`#sejVWLxs(QakCdKI`hRwfyGTUi)4$d)r_eqp*vc=JEYbovg+3pts&ca{<9fO^ODpDA0k#tpef?~qSjvE0K;v`>E%*IGS3K8M$Kg32GU*nU@b!eHfTJmo)bsIA$8q%mk3o1LmSvo6&7xi=R5V>c9&6(%m5|P4ugo^Dn>Bni^ae<*^z=Qi5K>DMU{6=Er9)6HryIr<?gc7iDj^BS^g7RAy7bX@560)C(|LyD;zGb>AClK*K{@a_(^VOK5eiLHo7S7ElpcKA(uU&GTb!+3&O_SAo!(<oGy0`3}~#Zm=R?qQ2C!G@&m?Nr3tH}dUWSQA;hkk)#6B15r_!%#E4wiENX!yt?q-pC<O&f^-*mFr%DvA=J7aY3y6i6@@$%lN);UsWWj7U-E;4nv<<zDhRzI_og!K@>f|=Nwv$tBK}{D(9cp!-ak9*<@Otr=xv#EFCyqEvcqU5pU`Rx)eaPcaGEf$X+xTR(n*Cbm6KOu7_g6Zc=sj{hZ*Ul<pgRHBf8MZ$oq(`Buq!H>!=43l+a~M$$Sq`rRg7Ll(!Qm(=o$p9?y45$%bNLJnO>S#x~dc|<0Dd3EfY&*a+vIOwt%Csa_uwhksb=B5M)n|&`oy>PP<OlR7wa~_`2CTDkQlLoh}K*?rupqiY@OtnxR5ZD+$fIr~nwwh$H!Zgx>!>Vc4z<gDBWN*CqK4S+(6EBbl_YZiNo%5$Jz)UDS{RXerZ|loIQLqQHoJ<sGyt039I~&|k(d>TzAV;y;>>o{{V2Os&7jFik3mqixx)uyyVzA$4>zjS9|--GJyGxI{C18TF+A;<{Mc+vpd}fhML9ez9B<UxIS`taapFgff$5+YJlEc!?U$gy!^N7Tq?BUIy$Tx~6VS+@lBB#vs`Sx;TVRRsn?N37}&Sv=6f|6{<rFBcM_{PGLjWC%{UIrGiT=bM<NZ=*~*Zh$aAiGGZ%!YK)Ob*Fi2R%Z(aPrZvx~r++yA!==)2p+`nBc3?-LBjU2Yy0|Etw8vr15E4<gi+5U!7}`7#PXj)^*K018E()I`(@o?wVD#s+jf8CT&{rC-uZH{*=#{&nHyB++C%~5{>GPx)djgzNK3Jpb_mUbtYR#lYwRr{=uwt0xd_U{hM2l*DxDsr9sACm9kQJ)b)FE&<W8JXGoH6i~&}yrdwe9H2g4`_S;QIadt4Q<{v5K)#BVHpw77(khVcT&M{CS|nl&Z}<LO|<;Tis~{)HkCh=ZES;?jLIx?C1cE-Kl1oVE=3t^x>cwe1fZnt)uKKMhR4OEc=Q{%UT}~jBE&>i-!jhj4q;Og^q=rivZ&uGh$)8cVIu8gwMnBO42${vcC)bg`jVoEWagY@mH6U%Sd!Zr7he7Z@r}=ENkRM$d?FsIm2J{!ls+TR>@gCl*aI49&1n2r6TWG?8a3!7AWeYkaX6uHi-%!t!<Pw{SeerQS(DiU^AAfjd8a9+J5)L_x@e17`VvYW|6?u$weCI5bmc#DjVvpo=_mAEMZa98kkj$Af(V9UBZ*5A*MmWlL@{AI0N?|zWep{7b=zC^!g&dl&V6*w(g@|R)tQpa14S@816+A$|X~O9kc?hbYy(^3=Dcs8b^&K^R$rCj9?w?qPOh2`XZa6TB2`9>LWkvEzq<wO?&7ps!p=q^0*twRNUA8&dxkA#|`-_QJ)>H+=V!j#c=6_Tm4c|>xXLOnIf7?PF1d(yBdT>VKQONF|PizXL{!BQ6HOWpN7p8AWczT%8;W_B3ab7=D0<&MO<^KhHdVKGs>d1j}(4Tut=CUT(R=~gM1NJDPo^9*~>89j00gt6cqf2`Baa$ShqX6aRH_xtm~4fAQe5VL}#_Sm0m7t%jQII8s%JVm<`-P*H2rT#5yy(wO5n1U)SZkM#1)ycu1|sMX<w^$8hsl_F%xBUf#leEuAsIGxA~f?QFfq(#yi}30m<HV!){F&V7Xer<BNBCo$w3M?)Sttz+OaV3HSF5M!CUwv3_M-Mh{QNvwKLgT<2dvb56LLk~QfdnEiQ3FXl43>hv;>du>kB8PAYK^F|aeBD1vToK@SGi=GaWeF-FZe&DSl^iYHiAfv%<&r9kU{sv~o0{FLg5abCQlKQz7lNGjmqtbn7;?)*&?;MY)<)v*)9!5-?s1!P`?Mnz9A^YYMUC@hy#8_kF1H(Q{a5}-@2|>bxvxtXoJd~UU^T(_>TPX+f6<yh#X~uKo3skWl6h;qE>54i3kaIF<x3(moR#^fs#YrKmY)BMzr^d(=tV=Mz8ncEM&jc{=tL{Vde#bzkw(1CFv8b^OjQC+2Bn(1M+4z!FU_Pb4b=7D!9Gh`vp#7JoSqa-*He#Q`o&q+b%ExD^8E)Oko~2qFp7bW6mxrjnezfQ34#ATaJxNjO`~!}B|Jl|)YG~_twU_p$|vyckio@%&#jOE1M8|aMp*y)pj<oxV92n`<2G$Z5X<!-q7&&8Oeq{fWDgd5suQ@N&;kd&qNRo*y;$CNyeF|!)@|D}CtycL$^*4)A<08k+jZMZ#f5miB-X=@M>Tgc#Mb+^sk6JtjrG6-ol6<AuKKpqwRa@W74Lrs4-vHn7mDiJ5FcfwY)~X3ghL}039!IR2o`=l+-TH_2w_mjAc|z68)t(#3T+U*(7`&?L=;5EIEkR|eI8#v<JVW~f`5Mf>C@*|$saBHBpv_t%{wZ8^W6hpCIjd%OCR{f*!i7i>iiaRC`lz?T3d1_h(#NF|3%iTe#>eINI`c}esULve1yB-ofDu8Xaqry$`1%+*sDFuH|Pt=6@dRSp)+#))vl>Jc-!2KY6!47;_5vvd|1#S^qisXdhBaa$hMr86Cz!$v+9!(f3@#~9-magS?D=Pms}Ez1mm7-YM%n`2GJp~&mo1d*Fi3Mg)T&W(QD(6-cXQ}^}84Jg~STc?ZS&oEcZrK`iSBj7-REM$F9PjBO9wJQQ$>7eXqCff~O7c7k<#ZP=;l%a&*eR@6@wG-yc~IKv#AUK#W4GMG{<u{DO$HLc7QXy$Z<M56{(Sq#DnxJ`6^hMEOJk!TK?wv76D0;_}fUbpYHAz_2FuRKUBQ6&}({H=BE>e5uxkSDT+#XvUC(!<jc!3Msm!b1fg%fiKT}d>D<BwKC$fbT6#oA}e6n7rZj5=RP8C)tGvJ6^b)bgcClAnkug^*qSX2=?ftm67%@nR{5zD*bAU)f}`OOi7HfU!h-@NGTae@Q*WbGikfIIilN#SY2<aL{psciO80kad#N@e1vRQv#j)TNmleskIFV#i-|?!H3g(u77{-5SXsT4lNeGsx_!LW9i+Ub%EvX=GV&q?ng<jWXKBa2{<vUmc+X$hs5_COyTPL&BOvZv)S_>C&eY)}Uc&Sh>iBoMtBps%7{V_L{nkESrHftV`Eo?uQNv?Bf^X&S>sQp?2Mifp)>tk1=`;ZdG2r64Ebky#H?{kU|B;UoE*2yYWN7oXZ0=-8kVrS@e<n#mxxQHU<;|P^nOcu7y4($7ym5|x4?S!b0Os)_WEsd$WC>!(YHj>F1DW4mK2a#@4wPHy22<u`6dg)jU<H-1db8x3jL+r<J?kQV(GE>s2NrjNjnx>{!(E_*-QBfyggexStP;<SX5`~mO%827H5s_QCLZ?m_KG97bqJ>T>M-mce_Oz{fpR*nAKj;-Egm)Rk7~9zO7nd|AQgu@_7A?CU3n3p+@#nWdXWTJG(oHeyDXD=%hHIC(63;K{Fl2weQ2ALeYsl#V^K5fnC+pkuD2$)Y`<WKCilJZ=y#%uz@vka+wbqK}%QN7e=A+=9IYOlaP1Z4k@A#ikU3y?7evWkpC)I2Fxs@w1JtvH|+|4!L4VPsdbazU0$~tCVQiOJzj9UlybFUB77lUvFr(``Q?{NX+9fHH+!x{;Ygm6#-x-)4$V|A2a8Ezr_W79ia=N{19;39C0<r$4W`a<p}O6hQEI4rFuwfzW5M!?MGL;&WjFaU+Qvzf}5x(8%Qbz)<{f`61m&GYhd3XjEh1`2H;O(-ft7kFJ2?Z(3Q$Zo<C!O!HDvH=1-7$HMThM;|LYl##A0-b70Lx{?aWQ@$yj#TfaB~#R&rXmG39prflo0m1C0bTCfm8-?~;88^Vxw^tts2}h(|B3)#@;<Gh?naBnO`{9Y$CSa5A7wRe*24A{$v539x)VB&TqyUW$VsuqiWp-63h<t_Lf;3F4*bSRG?fAiwp`eV12e3D8-|T|=kR_BA9FDq<CvAyR|_;)l3u~#5_Tq|tu$+R?G<2$ccO<-0ti?<mn^#Z4YbAX<IX#Gcn*41jc#5;?4eNpLFH!Xp!Ct(sONK3l8^LI7K2>p81=)BMz#O%49yaLke@><y>XzD4Tbtn8reFOfmx!>_*|rGDD+^MKPlBOrJ)-S1{n&q5t)6+S|bMFeMXlOKj6b<sTQDco~<)Y5ZvDq*!M#tlUiB-73hp-AbnTYfX!i`kND73GFvlN<9TOpxs6T)Ct^tZi}t>ewd_{0eIxImsypmMlS8LiiG;K%PVx%hVw)Hmcz$YS_S<cP=1kkHs9Ou#7$CSodhsd;4TOb5A<SWK4ALMfrC-bl{&n>)R!4vfvkq-rskq7MCvwHu{h#i3d9CcZHMCL1Hm8t*kZ~JRm}R(yg*@^k#%g5ST4i`2lEcF>P1oINW%W6?>IMBm<TgtkDGaz}io(Wi7v^)`uMK8CAiX=Zi%g$JFM&wcug>0jH`2=Ps>s+5g{TZmXzzkPM9Zi3t~7Bf`21ZX-$aDjYq!Gds6kV;er@N_<t~5fAf+Pm6Jq*uTfL#{a>5cp4|>3gtZvY|4zSlTxI{a-aLE}<(;I3gIgXMuBw@*_N%Hzr+vbm|569F4l`_)kwJq%iEN*=^yGGOP8cSWM3iEK~XI&KHtWgu`9WC<QUmVLefhA$<6eyCJ1%9ss)o%>tQds@H1)WZIK@;>V{V+1As=_tW6KqD3v0xQK&W+i(iFT3vBvL^TqCX%Aao^XxOV~Up%if3M7>nSKzq#+#V(1O84)srHnLH~cyj|1k10L&mNXnexHhdKoc~SUeU+-|?Cypx=nkP)&;lbox!);(7AyFkJQbgBJw~ag!JV8b8ejKgJd=OrH*yd^oMNDp_o1-lK1I|mC8kV1{oOsEN)ckYZC<d{G=Qu3<Z(4x2z0Yt6^-p2uvr8!(aNIP`d!|^|9%^!*adS?+;Y9LQnU=d__o}R6XrGw$9G-yo;B~Ij69t!Qi1qm0S!Z<yF{U#_JaHyE6QEf%ESLU5X!^EJBdX6r1$+KZ$n7T61KzISVLUB+??+!Oo9mWK*>`Q2D)2s&Qs8+{9o)}7al@?Uot+LeD(QuA5OMtcwl0F5&}84R)a9OeWElyinY{(hOHvnpo6vZ9LeCAt;zie(Qd$sesSRUOQEFqdTtSJw-lL7(L>}+x@Gk3(C5N$<MLUsdRlX|)Zw;Y#cRd1U-b+7rsy1QN6JihS;P{+^`wYvbyVE~IqmYG7;6>zgUA;zlC`3-e1cC-}1fXE_2qoY&mz6n2Pd@{T@7F~P{juN+X6iEHBK%r7Iu7q+=C^`6a2{#-Rw%zib6J^w7z$UwmT1=jX#kuM2jeU>P(Z|2qjlvbe{z*rV%B0i6VpYmvZx|mh<d_m^GzX|EtFFHGZ5iE(c=>IWF>&&eiq6Nwwqj=J|%b>0ocfV1(!H#PfDSoqMwwY5`Z+JV0uney!w5m2Ty@#C{$E9-@Qt(Gf4J{6&URKSOi>aXKcfXmYQjCQgQhrK?!dzffzZ{=D2(mlc`i=aik<5B1};nNnx~g<tu~_i;%K0kBfQXz*Kgkf6x#d(F&o#Cb|h-aEW0xQ|Js(nv#{y^E4KCn5x2HTeg4JHAq8eh6(3AvpU1*x<Esq;AgT&Jk7lk^pf_AUndimhy|Vo)U1W3Q`4Vln7c&9J=pl<O0$?k=7jr!(cCMhQ&n)sB!B@=2|2vEsSLW|um~x)L0(0BO+{iHom||<U>@arD+qS=jxWb9uS<eCux?#YKr&B?aoRvpY9LMgcV-=4%6*=7>yt4Za)(i_3a{l^2fRcH>8KGJo`o$a3N!4|?aK^hxzyca@FvyB0tmTs0Sb2>_ZFkuM4E&Zl_`|<!<-}T*^iA{RnU6xF0(ncYIS?~25PNnh)nTriQET%=~CWQWqs>ShI*Ow4H$i|Taf$Y#z4bP3fQo;WSgguZ6U@I+)vQp*MBmlWWXA33MVVZ+SR#@f((L}0E9jknv$kCRlJO<x3x@i&j2}%6P|xjjj*PcwP^sr_2Os3k8sL;Rc2X;1oi$ATK%PJ=Y^(pR+W0*Lg6LSTxDD=jj<Kb2@~6A6~ZSU^%^fc%2$etUQoIEDO%Sig|QB?(HXM{h+_R^IQpfv0X3a-Qd9Qvu6CP$t5-u&DGo_eEa1o`d+dyb1`HiM3tLD7iDz)X?!)bM%`4rrA+khqdsL^i(Sg9m%aG~oLCvHR3gaz#<f19+OOJ)Fjd}Iq<t)ehymZFpU4q@1<Y&-kcbPabEtaAw_H|&h-e)0*Z&_Cey%C8BkuoCQW+V5*90vA8gl6YIhCNgifds^&*uF!JipS=n?;7)PGd(C+Pz^)rDF4Rh*W`#rT!qN*V+Df)uPFqZPvemD#%Q7u6aYq=KZaE;umUjFi}8+n5v}p&`fcW2triYDnLvq=3+9B4Q`zR}0`7rYFXdnYug*1Ou9dY8Tks5S{@D>bhg<L|K+)F0jfwYY`(%r_RFwmrQdro~fJ=1Zr{vYfv4Y(p!2Byt%%y)5Ns+NxhW$b51P(Z5nNhiE+6^vnCuri0%@TIMnWFdBo`5Ruv`&|^r>PD71o~QlqaLK1T}fj3Qf-^l4r#<=3m%h<Q>5cDuFMZui_X&-AKS2K-p}iWR|SVmS({$z6)F&?wyPzN2MSkWH}P!0y>--2lzkna!VMeSK}{!d3_<TVo$4(&Gtl@fGG<yHtxGai2!8=Ti}s`7Z8s`V#BLk?qzlAc1v0DHD5UgO_3_R@i4lFVYw15!{kDWm)S}O^kc=Zj0YN^H31!d$i~U-*7okvmlZ66!4hb2)&m2kiXc-InH{czLvRnY^$~+l4F2dNgs-5S$UxlU~YAd_gOgOi@8AX+Jw3~{SWdNfTfEZvteWfZNlQg3+8JoMTDF28M*J%uTlX<br0WZ8ENQiDHW0m%o4rA%@ZotNpazFcO2X^vv0(2txfEp$(($sucugmiGZg&anUvra0_$@_)j<DiTjgF3hG18;Dd!J1ew^|-UJ-X;g%bg!Cpy7)e%NIjZluluy#Z{$B6d&AmPMlY$(=oCEgPb6r@`!0Qt#?0AB2w57z6ofEV<>4yFCOcI(Tzlnk@Nz{g)mnV!gkR!D(lj7DD_PKi_CMVJYejU=$*`*8rSP@pHmF8-J7KJN!m?+3=w4`07%6m6-`%0eztyTA13)VjOuZsX!C7f9W~_*?3OrsNefIvgg%^q5;#Y#^QQufZ}d>7*(|_RqDZZdIw1&QjQo0V7xGYp@m5QUMcl;0@;c{j<fC4pDA5X_i|)Ey)NJ2JI5m}J;xrc?SM~enHAa>$=y5*&<Nf}>+z;c#rS`^5hlTEg%96(^WcA&y`F07T+EpPZdjAq$g)Q2X*7gf;-33{?8pV3pd}4JH-)^MMT!0w{Qf6Vx!p2UI8K=1_*Ln9kq6b~!_irxS8WPoj!ykH`C`m_OIMqY_^D>vSUAF!wQ$Z=?{aaOG6kT^x$-AsXo2j|vduiISF^0{(CFA`EE{6pU(_!R;P-d{Qtk)?PLN4#ah-#A}c{0XjfruMX!`;r%;9Mq$`P(+r4dj>mKFAdE%4*2F0Bz6I{xe`AaYnbLJf6?buRneI{AzxA{|YYiA+LV@@%3kXsVOh^%12q;jkv$$Q<LdpB1zd-NOLC8qKdsJ{#n?Ja*dy{8{{(IZ%2w4Z|^qOMJ(U6a&e-)P+E673yyc^AA1`@qMz;b%j7A%Rey-*Zy)DNTm8?z<P#*d?LU`FHbr)eKG3*$W?$?E6+bZNRoRn2;gU-2%AD5D@>Z&@D>lQGTd<BD_hF1X^5yfpuOHp?!9%E(*`1DBn|`h<q$bpkSpKOQ8dXy?m)QZA;^RbaA@jGdw@e`o2EJD3vKhjng~QikR~q#WI>xj$!#&DiG(#AU|K;}|e*ErlU%vVC?@q@Kc<}6>ZP#4E(GfXR&Csj2z~iXfZ^V6YB;9Fq&fH4(W(d{(wzqiQeyzc+UDM)Uz?q7gsWKfkk|EhW0vJSDzkY$mhljtWwiX?E%5e+WORS2rI3|TgxLrm7GKm?Lh+kr0O5g0pgpfxhlTS2?IZtFA${3#jWJpB)9?AolUq_#7?Q)!IR!XK-d&N7=$h!i!DM5i#Py85l{&i91Nk~bF6+!Qqvf(m+`uT^SKK-~}k9X^yS~Y9L+P%1%Y@`XT-Nz|n1~^X-p&mzn!BTpF_S#In+(9_!P9<()G$(t}dA<|{@S16mIpBOi(2psfMSa<IYWkiRa_|No4ovAL<{iLwREv(VL4o~iiDa9hIVyKesgA0tOTo>vC`WYLXW#p6z2=aAO>OG^P6IC&<p-$w(#_OnJ-4W~C@+W=Pg%;y7bcBV3+F&#s{jL>WKAN@ctK32i1O0ROMd$7pZLY(Z$qJXNYw5%7tDA+nq-$<pp1T@`cvHSs9D+!)MD4Q{~*Rdvj|mxrO(wx!lhj8$xCLYbw$jzaF|#xi;Qq-Xr`Hx(7<jAxxgbhJK{zc=9jpPQS}I2s;WV9I<g0y@u+|M>-GA};|W=!GC->vQkh3nE9=~A4NQEUL*#Kqs65y$wOJRXPOrn$o7pq9v7ptT|9E6pGSuIP`Wnci#$GOZ)G6=zcFnlC?d77HGj+*g*=73ruwE{F2ii+5dyjBsC>W0+AJ3TEOPi<4Fr8I~=@fP%6khnt+R2@nSa}|+7e+yh6B4zTknaE%2-s<OC$mDT`{&)C1cI3QD?3C}p|`76f(MS4Z=oRzK3pt&$pvzFR81zcm?0_&E=$XEgxHb*lkR&vzS#t|;aP3~NMF#Z8@BLD!047(HOvI<9S&@0qp#aF)YVcmTy4lh6pJ9KMz>$DXjidmba5P#M5o$ai0k^WzL=ldZi^S{zC_)#XsZ$MTh0+;fbBZePR+@A7<{TL7!-|Se+)*PAn4iq$WW3^e=KV%F2y-KO~Ymo5$<FeAz;M*53WWvSibRjS)cZ~a6{Wn`I08JFo_AZS_s2Flx5Vau`k;80^|Cyuecy8XY)5=N3Ro9jqQ18<@}fD<N3bI{Vb4|wRYHg5$)k_rFj~i>625pY1>4Bmj$Gv9G)MqpIYb_@3^dUTJ+Krt1I|09R^f{{Y%@7qz&`Mfp=31E`TrZRJBEf0@y`yH&|=yk_J|fV1C;rh#nMpOnBd(tKE%iVu7Y_EQydLUKEG03xlZ$NqeZLB4&Gec?x27>%eAF(HI2!p(xni*D5}w^wq&uF6UA)nU)^*+xtdkq>vvpQ89GqVp+ZWo%;Rj>u=Yv@_BpoLUD|=;+&$OH|UI8ClK}Cn9Zr~yT8Z0z+Dgtxwid~QOiy@&`C+E7UKtl9W(suNM*<SU3^=4FcBD~4DoOg8uVZ7C|H@U9ov9?{IvjK#KW||70dzs0sRn|n3X78>&LZTx!e$*&7l!|95Zyk1=LIQ2kgK)r$ktRW_!Sgd?MVr9^dcoklS=qgFl-M-qwdrYy|c7>r6*EGaeMP`#>+uZkY*jB0M#}@gk#I*1HD|1D}@lxXmeFcRlQ6=DXQrqjGmFZx9yb`#TY^Qi~r%(oY-G)`7j8fxa+8f<-FZG2nv)mxRL(?P@@<agdpGtjmKO>h0t;(k;-w?AUj%dm18SK38PBc1Inoq=F1mk7WT|l=5echO|y=4(QM{Uqzs`$Kw*WuRInWot)XWVN*nUxQDOc+**;k{o{u68$KVGnEF^nU)uI=(%;9dEOJOTD35u?rWL@%G^J{yNarngXY6L8H`mEug_jtaTG-1}RGErMW}ux01ym_QJzr8AVx8TPt{lQ_z&G%HpIoQ&c5dtVabY!>CX~)41bpA6V7D_|G1rEj94M%j<o!2!B6aPxX-6`J_@}|8%QnjSWa)V`eGntMEvV~aJ1)kd3>t5GDU2m-lV~3p;c$s}BHT>Z?7Ff+tIvfDy_I}h?j$41nZZzZaRKf?beGZWPv+X{E~DJX)JDJT8L+z%TWnV_${5qoMy@PQ2S}a=&2|^vE6}+tY`8TQ%U#o+y#UAO-g{jWb)4{pUolby-arUgivB#WNnYnL$yX-p;t0~2k<B=;LszKDSSdVk9b1qZA=y!xK^7fY$GgyYyi1AJ>DsTf=S{BmtSbmPw3-q{-}X(vhqU(kij9|}eqEa&Dv&suwo+hlpEcRGO|%pNNSqu@<+)7j0EdbIop<fH=2}Clrl@x)y0Hd{+=1i;Ao%&|hKedx^{1K!#_O;~`Syv@>E|EBF5)WE-b#p}NOWZ3@9QnsC-y=z>GXA~bF%j%AwYmhf=f1(l3V#JUD%i9fj7cVT%-wsO(!U~`8uqwM&jT>d~`g|!V3BXk2<9uy6-#G6=Vk1u?LpQvi5I4MIn_`>I(7#YlKFaOwqkAz_<3c>Zh}<{-_R21bQVBLH_a<X?(3)%YHBSjrGFC6%}&qQV;zZMx{Gm28EzsRi4&ilH15dlt5U8i~q=T=7zEt=wnizyod{Bk}6xq04NTja3KxLvqT!|>b+_>v}>pGt|TVd8$Anh8lCYc`Z!~guE@8(GN;9`ETnBJm1#HJd!6*Uv4Rlk*1o<+aHv;vQNzc{O~oRqb$Z=cM@)haB^xRSX$0`cUOolq!a5cJdbzqxJ?3-@V;O>n4rDP6bjsj<6q>mpWuXX|7oV-|I|zxRuqG+!1-ZHrT$;2SXE}ySa7kI}*&}bM4pG_X=b*sS>HYXTpCjno24*g1Uc0HwOMkGMb4N#fjB**f`3mvf)K|9A1Av`Y{7<OYLf}`hLjvZvUbuJj!z#C~+TJTugjwh{ZQuRyJuqL1XXV|&^QEH0GC=8$Ljp)XGtVT1SLD;denX>qG_LyyXsT4XqpZ1P7rzjd;{WJj{r0ay4=C*r-uG-t-6`-*qz#r6#cf1f%pMShdjKjbST&j3nD7NWZdy4+w=|i861|P9Tm~Jrit?i2MOWrws)&Jm0@)VPiqvP23Pmyv!U4~G-JXFJi`ygj+tBCKLB*<M*Ra)mBrdzv9`DGYeWEITbHJ8J28O^UtgDoVNwL2<_Ou?^ZmgbIe`!>;Ese^?_;K_TGQIW8o|SE9*SU2H42BG0q=n~kjSTWOrR=d8gnI+@mtJN8@svA_WAqC<=VJ8*^U4~YtVRfbadTwZMG>~;T(+^w_2=ZU+wdy|s2*<tR}j=ZfBl7vL*}u$)1GX9i5dgIs$+%;*%Yk743%ECxem5(?*3@-$ljfI69KQlT_cjaak0z$!huiqgroYVRk2|vu;AQ<J_c2K7GPikBAReIZPJoD)KRKVU_not5sb2&A+JwlId@i%5>qnzW~%F4N;9g~lA+Hmgj5`*JT{NRkLU{Q^sNwkQCp#)69^*R<6}3WZR$25A|iVrrI=(^lz93=k%@6KZ<5k5=S4w_BC_zzF=;~$aVEtBoGI_+wn4g72eOWGfrxc!`_MHJ*v#13wN@<A&<=xI<EFj~Wr#CUFNc2$2{*Qjo3Hz~?{VE1)V{RJ-Us_tU4(Q1;Q}N42SqBx?4a^{z6vmG(OC%x_Jw|xq%6Xkuv_;r?t#$780b3KQQkPp8MQYPt=(c|>vdpD0-NL@hU@ZqIY60o&+wVP4`Isy>kE^vRITJRv%N2Lo<f?YC{M+_T~;|J4?9XsYHE1Cu|A{o`Yp_LZ(e)f%ULXnKeAq!ipWxmN7;uYPulq~TwaG*#{yIjrAX2$@d0Hf#n1!Lm7FM7k#v0DFEz<db58MjW=hc(9Jg!i2wD}GW7M)h>|_<Cb^KRXtO?t7cJyFj|6mM>0vykON3j)5{JCm+VS5)iwKkYqD-*lL%sT=j-L#^OzEK8WP}l5-P9}lpgz9`up6Nx=WQy0iew#{;@3O}Y_O_?s#7KottGN<;KW-rBI<s0$#GvDC^shDLMocobAGiztXM}UZlq=44`r?K(PmZk!1a4f0)Ds@_I>9-?XtC~vz|LiDdfi3oX-HIXz3u&K2MUO;5q=uW7lV<tb)_kc56Gw%TD+F?SjSOrDeT>nRo6aY=`eq9%(<-|^eU<Jgc}ghc&swvI)_C`lZT8vW<?o=5^~=hNSXZ<p<O^|zI3DTGlTqDrXj$xKl`tow~_bpqse%?VuM{2&3Jh7Oe<Klhp_pmhj7j`2||y;$Wy~ip@J5PwCX>y_j86R<=UDU<lD>+Z0%iB3>rnQze58B0gwxo_LX$e?J}4<wR4I0Y=mAi)je@D_u!~SP*Rk@gE(E7WwL}ycYtGETLTlUlswa*np}@lQq>*(yyQ`^tV;nOXNK|FWsllLD;29$hzE=d;uR-Ki~E9XOIc|`7Y=OqT=!kYQMT8(=+UeZ>9FpAOC?l56<IaEU&e%5os^7;xV1@nHZbI<K$@%iM?{3A7$Z2t0v&UmNhmdThm$FdQtY(o6Pz__EIF!S!8L#@J<14EQgW%*ya&7Is}4d3V;kTlvy3d7@oSHWb38j3;Y>GaxO8V*3{k2?qEw#$D%ho-f;&U1CcZa~4W8Vja0vOxytbM%Fa@M4%SwHV6eeL_qwM^U>JC!p9HnMGAZ@th>Og1%G=AQ7^|8=<A1+HZ4;B0MdY?gB;X(l{nA08#uCK+~m`I{UIg>YRTv)>9Fz{=$)U{M?D`PdD=go35Bxf2^=elijeP#b~QDU3IUz!B;I?%BqgU6MAX+gJe?qctv$w9gdo!ix8qR7~|0qAbM7qZw;Q;2X_mw=&}Gr2nqkaB`C@RW2JdLa@1K99Ch`)-^pdt^}tHnQt)0`})$V{KchlfWwnBD$EJxhbb|jF3!akP|z!dTvMaUB{%ez(k$>gP%DCJ2Y1FmOw#RC^qgN9v(ZoPFOod?VFIkITTxr0ulH}63gOHjW@LOITCj9rhZJ$Vu(8;rxNvko`SZ#6%qBFsrynEEdTI6=T4W=;Sx%2eL>W0SY>@Q+xhLfgzj-&X7fh=T%hd@g=}x;iV2@Ks^A{}H3(?H@MkqML+J<6;%O}l9LbS&q>J1}-Ug$r!pq+Dl^tt_P#8D0`(b$_MJ9uV_WjO~8XlBW6`e5+tO!g+Y9fzch;7iJ{y20l!_yS1!N$d_;T*V@$k2}`y9Zqbd8is7kyLID{iJgOXy!It_s!4r93c1R>z7>R2I~p|)CeUh1d(^JVbt#fA1<oi0TAA+Xi-73(@sMc1t{9{REMF_Z9LBK*2^!}<LN`2*Ks(wJi~Jw+o4N}H$+8%YT;b(FzC6hzd5qA(DanMwnMLq%d+YhUx|SgZiQQWALJlcUGtg*a-kohIP#|zT%PScDtONsh+Ptpz5fzO)Y7~Kdqjs>6;g^E0j$=VAPf_IaNaKhyK4pEIS_t}F8XLj*wWC`sA$L!h1NB+rTdW3OK&Y|`>jL@=Q$bsVU)#L7`r6c7Y-MyLiEn`)_HVwUH7<8M(IH}nIuh?Usv2>=?uA>S0GrAD=CLDd<1r_NlbEqG}#WQ=4bk1-LIN35+P>FYteeIAI$l_tR=0UpW!K?IAaaof+eDSn{4g(y_jXuvo!3UCZKslFJS&5tBFbn%hETj$50}p`+^m+hoa-Ubtm{6l}P~8F2JM^uo!S7Uyd2kT%2IT#4*19zNJqoj@5P&xBtZ^EG}<cTe^XhQ>1626o<;;I&Vma{wu2(J@m>M3NdvlkX<EYKPp)>$yu<V(4=#ai$}i8sg-c!F)wi1X$|_dBl(h%`zFm{?<LBI1KL4mo%Dj77LX|LuP}`j)HP<9!aN<AQ&GL=XL^DPUALQ#d<gs<-Y(|(B2N%+sZ(m;SC?sESy-}V-}bqY-9wrePZs{b8@|l$fYG)IPj83sV$%wEIPoI;rTy!0D}%Bq3rE3s7+h2;B@MG4pMe_5<HDE!uSDPN50bv~I^ux#GY<*SLSiR!aZ~a`_~CK_ZO)4*)B1^wJDJ1l(-`39NX}DOn2;KXQ)!JlmCK!G;4KJlgITAq(4G{DD~dJRa&N7rGOu$L@L{o6R`Ng$Cg^LdhJDL{5~XJdRe1LvL%Dfs6d$X(=@NYY^1Z*l?(V{(?Z|d*tiKj!sbL#Z`TT@UJ=}d~Gio#8=CP;4tQLp8@Qf7OrgfAR`h8T#>}Y3O^vq<fo#NWW({nLLtp^HX>x6s#CV|=jH9%q{c1)sbw+Y5W7Y!OA^*oj#bFa{X%BZ#g7^;dTS5EPT)pZVw?4MvR((zi-c#6)ym4A8yZeFI$WkX+bo_)cmwcuz+Dq1eK;ht)gKVIha)g|it2bmpmnE?X<{}f$rK;U**mb1*3=ln!8v_Uv9UYaD0r1gW}K-COlZcN9f^DK`Oq^k%f?Y17B+BO%0-;`NGIVKExT8B2N3|>sx*^r0y7_G|%1~<!`7ZS6FRSq^bNvULPZ_|CZmjpHxQs(e~$Gto$Y)7=W7@xH8aL49S*SSJ&w*szCooJfrwrghA)cHr0$IfWVL1_aUYO4#Mlas-^%=o@brgYZ~yvwXH>l0}!!~!i4y|mIQ5jWAadVN2VFp-Hf_UD2>+Q2RG-*Kz=xp|wHZIWZU*n_!9w6DwV_v}WqS!`AC!G0wO=G1RyCkV`i&w&ki)*Zo^A0Tz*(fq*o;kC`lNCegoI>c1FtWRvkx-I;gLLA#xj5l_}Q3Z|6!IWbO_Umyt)>>D0oox3H5N-hL>S+eQy3tIMNiep9sG}K`&PxTLJ);za7daDXPDe2>EJz*OQBFeNl-TBWRkZcta*3S!`^YCfeSS=_!c2nSQ>mrN5Nq*WR0_x)Ha`)POKq-$X)1M)EuRjBYp~5o6fI<Z`>slVv8I}`GNmGrPffqWGVtsK>0zJ~#sV(zR9okcw-JIwv9X)vW-3rFG6*t7!JGK49Jle#by{t}>(Z&=RlS;w=`WG5t3}*QB`EOEqF~+LIYnnL*61X~nPHRA;_`KTLxRGqJ56#s>|DdHu@9eUW&=ulTK4xKmJ)McMn3yKp-J~tpYv0uvKhh4R^?FXt#JUock8f)Cq+RBiOEIA0JXZrz1esvxpv#am{hJ`^3hpxT8b(9G{->VVzbW0Ki;q3um8Nxly?>#Gom&hrD-!3oB(h|aGeNSq4R!V*VO^54ooxZhG+6K5!EK%oTb-2L&)9Og&&9$ZhtuZp|dswtbd#QvW($m57h5v-sT%QUQC>l1ah~GK-wK;F&Eoxu-EQc@#=c<OkoCt`36kx<xxet)gB|Y=upD5g`v9}-NPv!@78q~Xo}c-!Y2~U)COz^hQQnRQVSRydfZ{UoK<Jm2(Cz*aoE_30D5tP2U*w;kN4o+_4Oz}{`K?gPoF-&nqS^O8OwYqMZ5m^`m_1{!(Gjuw>2N)-!zY_bt)1DAo3`hbO+M7+s%2n#bM8HvDYVh6{1@et(33{<=VnsIKSevTI*!j%>KY0G3N&nk$j-+^z@s9{N>~Oub<rX!K*DmfY0!nntsmcComGUf9II!vnd2`NdNO%ay;pO{_X26qdP%6xi>?rDzm?R?Mt8^W)VlV7rh<sk(J#Hp@00B-+%b=yT5(;=Fh*I7s3wge#-2hZTDOOS&QwGnxR)OfyYU=--zp=CHA5@XD%?&6sk60tlOQxZoejJYuB{+7jUMcGEvq~mgouZ9swNHtY5!ChU($3sjcbdBBC?0+cd`MFOEqeV`7()Q)dNIu{27~oNdOw20n_sVofCA2!uC<ECxIQ$dDv*J!7e(&$V_ro&?%pVn5FLHseVlU~{=wKk?(Ds)Ln-oTB1ySx0C`ia!LvpML(~r%ykw*W=x~r#4O0(bE*PHqq|m6j5KDr-x_;Mt{MolRy@@DbyF3dU?*BO5DU~PWGbnd?_0GHq#&@K72sXkC94a;j-&M)L#1P;0-(+n9@zmJAmt`799qq)N6lePPt=K6!VKxt#I>zqD64qXW#p6y^6AZT1$%kTKsYW#z$TWd^5GVlX)JnESWXp4TyZ1rHp)G!Z9qI1I`NZ-rPBIf%%f~CLxiyQ&Uv?O4Dcm#4jd)8<rCSxyS`G-cMzl#b#-qpYx1U-OX}VoA$YhswOO61&0(~l5)T2TcG0K6y=2$#h_xOM)Z7Rp6IpzED_tf(8g%o$lv~Yz5cQb+BtYrq>^lw!BXS^qw2oo?_W-wkF@ydhKMYBFp*H74Qal1Vx?&^7w@Qv-d-;HLu=7HV1S+)<O!_oKGsI9cat!@yX5129eGKL`~0q>ONeMDURpo8RfDCrD8{pq$R4nRqah>*UvNeBquNUp3ftU%z`Vf!ndA+1Y_V-Zf0~dXi-kp*{a_0`^u8^Uvxt!Abx_g`&Z*RB!@iK{Q;Fssfb-(=oXwt!YA}HQtNo|g6~RWfj$;TOGP=}0Jx{Hn29Il7Bu`HPU{CI++ZN?h0MsGk@qq_s-&s}*ZZH1Qm(dbYZF_<3tx`=z<@Oh%D%}%a;#P(NncIR%BKOBgVRa^l-O1gW4iP4Wtn{R(tgXL}HdMA|?II#L(=XCHwa_o#aarfI)D%qEYdH2dN$lBnP0c8*cM0I_QYjjId8d-5x%5xC!CF75+Ex$Sj&_Nh7fsS7`pP>{XWLci@vt*Q^M))RP&g#rR9EEz!rJ@o$S%)tPseRwb6O!97{7-+l`bvR-FJMaZaIfaWqe)x?R}#r=WdERVEo^XJBDeg_dE6b*Vo^!A)K;3dVQ<Tg{x5TpGqHU(8)&*#^Sv(!#1z(?=dfM7le^mKV+I@b3wkE;t|3P1A`qiR5N@}1<DwK3^J!vuA`h)Y8qE>q#DC4M(~Tu+5!9cD;INgWRJ{m1#>`uKtBX3TuIsN_2XKP{5*tbb7%w~#|+)qntX}=fE`#aT)|eL*&gsg(3hd9#ruDJzq`dQZbI;9QT}ax*u=K?e+UmhlNaJ0<Czz0htC;+)Yyt<V}xRdR2Z#$z^7&XYjdX8J+7BvY>O6TBxz|06R<SM--&>ZQ~V%iJKK=22kb>)gERlmlO(qn_87=21y_PYi|KGBW)=i1N-r6y0J-7}3yPe~K*r<Cj(z7kqahyl;wDhGOLiO+=`>O)X5Vu`!Z2{`BD{m-g$l}{g~n+&E&`-Io|5o57mVwZGut+-XgFm(@O!Wd&aG7nG0M0_3dAQODMCzDdpGItBNvtc@{v(Ss65man^wROWy_*~3{E-|x;w*C^U?mM)G^Dcg*qByd3Piu$s|k?hwFXR^Ch(**0l|@$Flq%YRBurHtMF#?fLdFw0S%yE|%!5>bn%QK87M*QJ7LJ8f_^0gjSMdB7F_>Q|dk^?uSsR&_-=TVt{)3An}4$X_;|Ts_=ju8MIR`VX-W-VsVrWtk7<Uo9UWecj?uZ!=bkl`Zcuiur7pK&S0p!xB!tMy31&;Cv$Cemr-tIWussA4A|X>Ew;Oa8hAueo5ksVZ!j<j-7APp5rkL@dqcPYyQclexd7J@brGA#Mo+Y78+ZdDJgEq$m1CXcs}XeZWkf+uOr6Fa>kwy^&<YSTCI}KyMbo0S>v$I$h<B+@&brzX^5H7``gLuB){4Sz`<UNjS+RQ`8C!yVK*D8Kn?O-Ldrua09?Oe?<(9Ja{!MP{=^%DpJ5<EsNKQMyX4MVqx9#qt#kK3iYr)X9ni2fm-kol!sLOedt{w9nx>3G;!k2OWpva)>BB~<msRjv(MDdEZwNdLiJ>YuUrZmUFPM~JQ<h#HnOUNn*mDH~9YN{t6L_){6gHq2xG)*tVB~{k<xeQejq_(yi2u1-?ekyI#6=VP)5KRIX*>Ms8QhO~F(wvc8G*g-l-z(sfBoZtB@)l`vyS!ZAUFty%`44IrgLRnw8HS=eUIsRxUsc|)LDzehMQ~%ji|0oTb8)sGlkzH;U9b?Bsq5Y2ymM4$%k3qY4LmdL0J87w*r-^NeR6Cmpie+lN*<T2Vr0KfqJn|vmaM<Ko2Y@q`+vDz!_KWi2RBAa@5VYN3@?DC>U?ziKK=kKzt5KsUR`P!bAN=f48cnP5@~+31<G_ZSBiiD6!JWICAiwg1(3SPTWM3ROJ2*@jkD~=C)kWE9qJK^R2O23H2RJ&DX9Gp8TS;w!w+I5&{Qf|9|qe+MFg?S;ehXQ?_f8z*-c$u?%2BUs5;qh81uQK?yuX+wT`;a`Opj)qap}?&jS|u7i^1wH?5bwk@i4<zVD7M3i<VlFx+NS;w^a(%6yR>VVc7AI)4J2t>y=8ciG$|U`MXd$RalC_}AllbJ!Lq5Sjl7TxuQ?96Cj+M9ki_@jrSA0Q*-2MQJ=vdfGW}c>A%g&<%?2O6a(tSe#M;1h1%YK<!PSkQUq?O94w84BkB2Vbz4=3@lBi5GBT!)8*5VPQ4fPFU*T^%0D2GigJ*Z5`bPeEdgv@BJ~8`@l*7XAq^$haMQn<3t^t<>_X&+&5dfz8ujBnv9xDzc){`kJ+OTw2(hscaJ7Hk+27pTiEQ9?h-~+lMs0wh@!uG!j($R>Wr*3FV*q)dTc;p<Xvardn;sX|AP-s+$25a*&r5&lW$F-5*VEWczngP@WPcgLm>3;!6$9S9b#@~VX@|or*I(okb#mBkNSVTjkGBB0!W`_lFZoo8zgtxbBRjl(tR004lNpL<)3m0GTAZRC1Vq&|n;G3%HW3WY`rTS<iR)qBmkE3-;DWA0Y*nP5DJ}#NA7H^0_zoDDfLJHINt<=8YV1meZM)8|6A8O5LPttzvq<kkKSr>N-3q}6T|$Z`fhfwgDloRlKdCH7@X$vwd8{bb^o4Q}V>!}I1t|);;>3{D*SYPZp)<)E;8A$bmyJ@T3W{}<3k>3py_TH!SyOQX9-p;hiN{q8>U{!TBg+zI<^Mt=jcxqmi_)!W;&ssNIW;<(m_6@YbWtb_3j8hQ3W+(0NloSV_Vh6lrOj@euV*1=9Y@sqLMckp@L<>o=^DvJFhs-=q`&)alr4g?Iqj84%c&R*`h8%1h@J%)O_;HzVjHI!+kGKZ6w(hxbtUGTRrNtHhaDvXH8D4Tt0j%J2o((z<(rS$_i`GEf?%wxm7)=pqAm6zr;_$C61uxX9vcg%ya+nUVsvDViAk}@wz7{U?+x41n)AM2YVwliMB|fhT`-5J5al2?n9q@NDxfrog{vJtVrC2okFH6tFu?nUR^}j!X=4O3xv8SksmAGNL0GXLI+?GW(<t+?Rwf>#d+S53L|o7dE&A8$vW$M<p3k4*o)1&5OwnnL7P1X_tjx&Dk51#@=IjZ1cAa3V!Gw921d=H0)aEWqPd(9sU~DfJJ5a#4jL7Y=Y%3U9TUSEBh+8aGtm$~?T%9p;bp#MA@feX93ncy%>HdBk<@R`c*w3T)$(J|bPcT1b%sFlzCMXH7gqEZdERJ$BebI8#Nn(biFm@a=q7$BvJVmGr5C%V}Q@QUTGJIAY&cONoSI+AKPksEVGh(RN8xFbe-m^W^au4kRZ$9b)pF_|h0N6&Jr(+rew8o-U|4~KU-27fpK=Q)myZhOJPrX}-0c^-$cc^<H@O1&Vz7lZT?yR{}J56}6L<nb5<q9{k3XWQYokWQw2uy|94zHyx7~ohZL(fVII+r&U!YbfqOVvX3^OA>svK|C{iy5dTKNd?{*M#E#<L=9rBRP&`e+Un?WY+S?Bf=z_ksO&s8J@14|No0SoUUqgWq5daWH%()c_N4b(78s&;^B^ugLb1Kkn{<pU1?Pl8FEMvQ^41O(|5ap$X+{8P0$JRaa~F#L}ocJ`;y=rqaDr=`%VQW`qV?q9yQ={7WPo=Fh{2c?lAFd9v|rI)*f>U>7#)DAvhAi42gt#D!#AqeBU05X@J_J2WDU-IWFXtAlQlbT8H^r;S^ffPDsx19|a>XG<8!`ZPvw5OTSopt%eXvMZwmCkqLRIERfE6*td0AMW6dJ_eFLiNHZa6xQ(iM-V0WT9FCnzKiNzOd>azQU*{F84J0!IxWgW@uCPWC`ZV(c%b_)twPZwcHqYs~n^E%3MZ2>(RQe{=mg7%7TbWbiIjaoMFN%oc^2&TpE@UuCP}5My6{&PebhyVrmyQA!XFa98x5B-PU*$2E3uSq(hZZvwV_xGX$F|<_`8H?^Ps~oM*LB=7WjdT{<d9L2b<`=j?bb}ADmH*Sv1A-HbIkE+%8=RCY3l4$=g4Qhq1bKyAiQhNRH|I)puIj1c+6u=Ixgs0D)HKAk!El!pjjnkPxfyB51d?2YTBLynl`V@*W|-%td5#0Ui&$4Du0=3$gai(zbNE@Zufk;dmLRMvfH}NnU-gnPbop(s0mYx^19`mmClaBd4F7Vc_hgir%=v^a-I`Z4t;gQ5Ay3Nu-9qR8vfIaO$*;i%AphfHVA{PNt>5Uu@SE1waK^mS#W~XpoFu>-#rGr%j(-Ul4T7)c66Q6AGHj@Tb()tVG|fl2U3!K=Cp>8<e<Bz5fn7JJaGRc?QQ&+o`Vh<o}t4UUaFAvGj8z<=fH_#YFVC?VR;vLfqF8PXwYW_T~@s`PYbBwx}V;xmmF~oVA*pW1B_)KaOz3z;dWGY)OR~BIrg*X^{1}ul<)F>tsKQMjyc)d9d$>k{XoTW=>o7727N>n<RN`%twp5|WgQ8AFE?wZk)72Bi<?RMO5B?F9|9$}KwaFo%ym;4OQP2W^HwH6tb|*bz4Z;)HXu!kBJgPB*quanRpFVg4Y@BoGxs5(XTqMG^QRKU1GUDw@mGG4`41REAlMh4(Mpk3*JbV#x#BN31#NuD09LZjI#&(Ln9CYEfy@QQu+}AXXCHJ5O#Yf^+6FM-#ChJaUNNyXp&v`mDenR*jxYNHc|?upDRAMJH9>1(FNj4<i$qEC?YQsJCesV0Q^sj@k%!^|*Chm~P$p8DU!x&=PZEM2xS-nT9$UA8zfqaeBV{;sc;xCj$|f>HIEf297}>*D)jz*$#1WwITLF%3T`L2*$85<RWs2I68B0;r!EyRk<%L%N*$6%X{TKne1N3LSbUOIEN|9l8fO^wl-mo14fI`C9I0{?0P!xqiqyYJcSyH`|VFERC{3DEwf#l=XuoMMm*7Q30nfstI(^c-Uwr<niLC`;Q9dP@9ZA!>~5ewA>QNvafA&`W!;cR5&3n^sV^7Mri8k>2Dy0~!FhiBV6({}Gd&f*117My0GHss0YzI^|@e|-BRPBuf)D4C6zbNRYEa18E#7n+8M0PK6MU2Q6q`i-Z{LK>y}U^{qUD67Tw7N3y=BkvR8PDcs;7`A+WaYg8Qs<iU4^S#)W3WBn>^?;ujQR^J#H1N&;@sq|vF2k72T2FphAFvTXFDnI?o*l<(<PeUobhf8Id2Hu0OlqeeS0T`ZnG`&GnEakB_~o3;tZGehkw+el#NZutKy$DM$L2Rwf4M%(K%^tqsk&f{O!K$@#w^3C9x_}MGIGr72Jv_C7~Ce4e0r|v;}|)&Rz?;QF6neG>7K}qg<=fOX@i0}ejhw{&5fla2WA}lNMmIJVDPBwMg5F|m6_R?!4FaPKk9h-cyxWJlTL0(Zic2xobga<bb98@8Z$`}i}?-OA9W1;8cm|;tDlR}Y%>4x7VvI9`wN70_VgTwb4rW)4A_i4^MVoj{Nd;9CdOk9cP9bVp*}FX9bhhe4s5`i9%;v^a*6EPZwIxH@HB~m-NRa_UCidNI{%jYapo>vg4Si4pT#D<;484?h32JWz|ruM{P;3ekt-)^>XCr>g(b?FT{uK{GL5cXfmsx=O^ci&{!k*Ek1zmsmoW!cTBcPV`TgQq76-r_738%ehPq{r@W<S9@spCoEAo0~mWEMYr#!ReRus2DPF+#dQ+{mbE|QfV2zSo&k#N$VUdtPez~))6p5r2JsvR48JLG5^){SG-0$Cd1Y+&&c@NYaJJZ<UsbF8b(VhovVf*4V3ESB}VmwD^s%>a&-j*sf1Q#TiOkK9=;U}oLeftMa#25TwHDDx>hMAiZBkAZ7wSbdDICIBnC3n;6p<(f^Gvg&T?Yre|#Oh9hUCC1$7Mj%>ihZSBSqrSS$gT+rY-@ISXKfis<lxwyunO54b>ZDz^Dsza2UHi;T($*J}KRVZS-xdo-d|2#lPuyJQ3DW2u=m81BhM$EYFnoH1n&K(&%6LPZ1(W_5%lW}zW`W3NW|j|}sOfn}ZUm#Wk@i$5V4dTdXV|J@smotj<XgjZ`iIhd3LuG}9RO!x3URY(Fbl)UE(u}Wr+9q{j$xoF;=7AaD43}Ynl9z(AD>H4K(%LhGSjW}=$kcyD>7x=54Iuz!j+&IZO#vmx!_&i_s2W($G6{p`s17V;S0!qd%R`8z5n{{ck}ZX+r=K^Bbj&org_niHQ!XMr&VvWU)UcGzYwKl?$(H(MRTma|M~joUmgR+qU$i8b}Yumm5yPc*J7W+pJT$j>yHWQWbG&gZUBye07!XDAK(x37{;1ct+XE;{tWowEz_^ze>5n>#h<<RRgA$$By3yzJ9b=-w$W)+ppbd|akSdP24$?8d)tk}(Ly4>hwwk&{gR)4|K+!zewg9Ey}$qc;io(?!((+uS=f*GBR1Qlyg9*i;c%TG>^A9uq7Y1lXtMMVoI_XdQ<>$e3z4`vCmy3!C4b-;S}%>D&44ozZXPkhHEm%lR}9oK`s-8mKmYpW*Ps9Q`+)xVm(M`f{t)^OP}wBye!e|gu+|zm!JvuozU_9Lju9gYhEE*w`CRl>RX;ix?P2R&zyX}cX>Z}o&7aoi29DH7(dT2+M{mnkI#rIH43&WO5{tkH9Yft!G6kY4`w<5#_PjT(`WjQZZDDSXi_|o$DtGIoHscb(oUPXeww4w#L*T%;gdGDQyUHxFD?koDySIJ5tvoav>g_YZKskRQv)jQN9XH*x{32L;S~>uWUG=+T8T*K@8oB^Y(>tz5wdT1cS@br_`uWdot}nhlE~_jLuay@%HgS7Kis}|7Oe{+14(b>AQ9w?cK>o;U%x;dgjb+a3xDL4<6Aem3`v`&`_k!Uys*Hk_rCj--B<g*%%-zm9_89M=`^lZu>QSR-7A3=mSe}HnJ5Fg11rw$jGJQC4(7Z-P!6<ZO(I%|~>hZ-fQXCt3C&*bxFr*8|GWwk-20!~|i$xa4jP=r(ox|sLM6r^}P{H<QlSk@Z5~3jQa-d0W+{oRyHNh`!lc7}hk9w`v{xq_b6yjl7CBXIL5Gpq)+eUpet+xg`67f2?)aI|))otonOWv<5!nea)-KaM*R@X;_dvmENM7TYbV2?}3`cV3UFh)~%x!uVscPHAa8y*v*{Pu6>(sMg)fIy{4oCb_>i&$#NB0!aDpNWh&uC$vIRaBE}l4wd98yHY(P3~Vn{ET0;y?ydNJTdF2HyC89!tsphx;7Y&%?iaI93aVi3(d!0pYsLV>b6647jdS{kW0Q>naWqd<WQKPX;eP1DhZ3zg=~#G6$~?fls`MLS>34`#38?1*F5IGP&j6B+FGnD1yX3t<#Ds8LNfj=mh5344ycA)N8YyBupuWz?8Zj>lhkqO2R%QWXbJbe(u?)7w9!jni7DqFGnj^<v(3olB0lHBv8^;z&`U~l9M(<^8;o?qA)JqKW2-tS$B-uVWOsx&5p-RT6ZyHH8iJLMk|Xp<Ns3d9bx9;LHKMSxa2{oR5t)j)U<+SsId67}fZ99xo++a?Kb?s>Ctc9hZ3-iqW?I_Htm+z^V5$YeTi{`*$UFC>rli^|rNGff?8R+hY++lNMm&x#_)~lVQ-f#+<}`%vDMp9#@-+)8Mzqs7KGki^pV6+h%&9)Ql~-0SqAfm`r%J#xUqAVnM40o^T5xpbqEr}dQP#(>OH^`bVu=vnVDk<(07u6<yYS_lL5|oA^%j$FN&n^^Y#yY|ZXUs2-X(%*y{?OH8rLM3VR6h7%3Kg&c^>x8gXBrk@dfXh#q|;pJTT~o^OJB2#t=MC!cL25x1+Q%g*~kkLyDK&;}(@v$xx*f%R@&AUD#=iX?=Jtn&z%R%xs)?wZb?}lj^^sHyAOi0Fz~<9~+nbx#gZ!@C6eEmjoys36^OpeJBjHrZLWfAsN%5!Bn5covRL8?0bTRjlwIROD{T}ViPrAyfu&e(axTj@j8aFJ$w8@4J(YllZAZwD(+9hTVoj*Rnyn5?L5e3Wwe~&!&qJ=Eatk4IP1J1i1U+GDH1U0X_k?2I_JB#bnfk#J0WtEjKRU9W>%^b7ROMGgu<Ok>wv-4eD6FpY(XwmKpHnO<Q&4*8r^b+EsCDFPEBeQvd^I~PK@#93{X5ttA#uF(aNpeNSO!Bq++<d&CW4F<m(?iM!Ksb?G3nvJKbn{zpQZI5l@#f-F&2c!QTgPxPq9Of@!yNE|bimC@~bqT=qO|pu<zmbA2AyGIvNzieVw?W*3~vB5>u2W8+`ZD9G-I;0xUsS7&6Bd|A(bmx<DSY1FAK8CBiL4UfsyC^!HS+4GfNW$!rhoj4?i#_)=q)KoSM-nsFlEYYC(@EBzd(^JJzp8JrZ)ekY&Y=F!)4C6t&d}g!w+-@_dgFFNDiCk66g7@KQ1LYec?r?JKc%5Q3+`%dcBcQ>9N++K!i2m&Bz;``Zf@4CVd;)-jeY{J141N>+0&B6-5~Y`Yb@q?9%}q5Avh+L?Fh$lehp_BXhgF-ekjxS;^wuJmBuW2$Sl98&s|j-zU+mZd*V-p+@}Xd@c%EGq)Hw#a5a{Zk2i<EbipVzJL=kj*7bWt_5Y~F%i8b)~7$pFkr~SQzFKA)F=z@{kw8a|5eg}(9$S7PU0I?KgqCB_pI;S(IP@}pd&6!${kibjr6G!JHknc`QM4OKl%R#c!TnPJ52#n{IN|vZwf!)r4+Eo@7|J;--9X}ZE6z9R(48C+<*}vJula(^_YJ3d|ht!?IVUoA2_m^+qTp+Rcnz4TeBQJS*@W{0tJ<b+i<czRL%{>{erS|IURTVn&ihNzj8mG~)P0P~RwxfVyX^)0du<E0Ka;sU(s=g7{dZOZ6fC(3%&fr>YDt-o0JK}+`;#2HBCd!2k4GC>!>e0ehoFnAF^DLZv+Rl00Cc6&0ZW#rbGE%q%nNkO**tu^F$w{&kF5-dH5DBcBbc}M6A=I>12rdrq|KL;2taFI0?Y<W8DraP9tTcv+V?ssF)MnbyS%(mB4ar)pwW@OB<Za-UQ(7sKjnFaNMdpj6cpUi+lWOgm^<Mi>IVu+&NDc4`H#+T}{n^yB5){`u)FEj}z8~My@Tq|FWRE>N*({h!JngQ%*&^OBd;AG_i>VXQIwF7(9OE0+BhsrgD~?dnLiGgJr<jk${&_6*5FYTjAM;&SiJG=qCRqdqfWVvrkc{h93(9QMR@5T{%s0phAg4yh!e#Wh&uIRfNR@4g&5wZOTI40blvv0jKQ+`aHsca;(;31V(6vPU0KMxbWReMom}?OV<ubq!DJSNixdOQ{X!|PE(iTC1BOMzt)uRDoaPndW(nYt??@@o|wG(17R|3goFiw4F)43Y^`O(LSqqa;;1arw2%n8_oU$>5xCZ~PsYZ|r{ZyE1t1OA6Ox4WsVcc?~YGe8uZeI3Ir1M`mIl)i@I&~4Bpm*er(;CRx;4w^mi2L^_*eDT2(V`hJVYmWvESRd>g;_v#S**g0<qG*fY+*vrI40)IPjF4_ENt=<3gBiv=4EgQ}J)cCm=ly1Yc^LZ|C}?P4x9RTEfYC_}0ylA=|91>}>P+B?T|81C?Qis)rVT;i<U3WGG&2F?DER{y8vmbv`D>yko8-iuhx+ts1de_@Kqc`sH*_!^rVj<aG$BrFKx`dXxnT^A#0IuXc+Q-?Yr<<Dwx^D!AGeBxv&Sg*zS9P(kx>Llgq&m_c^-#n4`3n;)*iKSl;t3L7%&vJmwB8zV_$TEDuzDnuZ@N0aZWN~)S$L6GGat9h^EBq4!@*Tdr+dz|H2K7RiTo3tUYcsa0@i=Fl<$w8}1gpCzM%0TG5UoVSlKrEMf>BvgaTHaf*3vcvu)6BCYiEx|)ww1S8t>!9RF#F;$~=5kdsZ+>o!}^RL&lTeUe9ojnddJj@Q%ah}F5Jcs<bl3OSo!D-SpX<4a`l@{H8dN7<hPhX7V3D8fWxAQ9t*V!A-fvu>{{I2$b3&GUX$6cuvUlRlzN^AN_u5*k$qFJFlCT^G>9$C`teGF_>(bhe55-exPR`D2Hl66H-&)7leoCU&~M)-RUv3f3rnK+zBXU9Ab>ft1H9>VkfMkM|0>dm8iBGFZmGMEhfLznGRuAb-V73ULDRFO*u9MCX-J<qc&jU)E|hNi0LaWY&ar~RCZJbqZj0la>MS0irXpBw&`BefcI!1q?3^ZHh205&^Zl^zplRF~ers4hLvYfmhW8c!5qjVTUFT&9g<yqn7Y!HM5tZ}bPR5QVKu^V~`J1!}M$5<@;UFaW|WDl&!*7P|q!^WD|Pdzh2T6M(Y1W$dK$!)GuEnR=3mQpu^bw3Nr+k6(oZQ4LEyfgy#AEkf1up;lj=L(52N>{+1+^@|(T@Vc<<11S~Latb0rCm4xiTvgfXPOx$JxeZg2U?L&nn}R-hEe{oALS>n`tbK7bK`;;xmXFbmN6PlngDEKs((&wHa3I4*@d#++u>c7RT!)T>NddT&51vFeZY<sKppbq)8dbp@DUJ6%7o|?}q0|YeNrsdcTZOXeI2?Aq&QBcQ47EW|9ze+b)zZO?M*A?JbH)ff={ldwTxA41S_tN?DtAh#yVgZ5z!8m_AQ4P(3t&L2+!B>YJjtnGkIp-YTW`+RnN(>AIdoVNe;hUO&ITADIDK`OYwu!4AVZZIM=hhlQlIy$;n`?kgpfdG{Hjzy%d>%U7Bx|)53uVHJuMJePW*Vdv+JSSgljMdelDZMlR%sEGRqZS${!<c4;-*EOg->|$r#3*<N?7;U~)8yhRc~bb9T!!@tR)82ptrBY_7{N>65<}#Fj)X_n5B#T#KBfgESGbY3;gOGLZ&2K)_w$N%i2e=mp7TlMb0*Cu5fejW?uF2lsmKObC6*-Itg+q-`NO@wUGAWCy<vGQs<23Ltg5B{)U2LZX)RiGED5V=#n`rhG{~VzA;<>PRz2S*D?&NL<VHnYB0P`M9W$rzSe*0l98mJ_YMu<Z^e+o-79&qTUNhfv?g#iv({e^BE_%*5L&S$%gejP0Lg9AEEW&s*s7=`5AqzYiF28;T&2o!iTD&I<H&yh&&%x!yEee&CfO-!6xn<xgHHJ%!(3Wx9n|nA%z7@Hv*qRRq60Aazq3%Z)3Vt2@I3Zlk629q|*PT2X@}3zE*i1y$qidv<c|8#=REziOj0x2uqqoZ6V!~B=BXwkG(vVUim5lfO(UJhq64$L7v6QVbGMIJBdY|1o~7NCQ`lo$!qx%j}lG_43AlX<8Pl&X2XC1(i}{oBvFqbnh<dnf7>#I-K5M2^KzCpB|*_PZ+piI>Z+){FTS+8P8`1r9R}PSyEPjEjm;2M&3jaO3?6r>XXD|E$8adb6f~3<o<4-@_D2jktX)Z|sDly5lH@(2r->e-bhZti<41nt?L5sHX(TUQ5}`Vx#LI`q^8z%|=7vs#?hO)$H!SiGYg8N;jiT{LI^z1bkMRo>$SiN7=i@+$&_R!b8?bh$Pw9vDHJZW1cHd9C@KkbGy-l`x*4)dXi@E!YG~~SRvHrFTQ6YAn8CrVG{TQ<hQH<&2q0}RtI4zzql+dhS23c(|p9AKKWjYGQE6|mODunF;=V?$lBf=C47$5H2d$f>^f(sfP<ArAGP(r6lXuwZ-s4|p}r4~IB(&iU~Q_2wPpyNF83$kZnW2#Q*QW^phRKJ&)lE{6fjR^#`eBe6@W$!8HL0L0Ty(m2_VqMz5rh@OwuqA{x{(apmW!QVVR~V+=_OmoCJ5LZxTvm2@$T-~6F2$W@$bFK-&jgf<F__!l&T&*T%7W5)LdX_WJ!7EbdM;}Z6xO~Yfy5B;yHqLY^N|_nZdwD{?MNAfIvW(!xt%6vEP9Se&;0Oof1=bS0G02@N+4gc89pz7c>FpDA*c%k?(Cw<yzp8q<N2oHN0@Ud<J#Hu1x^T&OnZ&nqtMfyUck5|5-w1^woO?)z-F$;q=N-NRi-oetT%>aDKS?JG_2vJrH4-mXYJ{eSY%k`8yOM?{s0Eqd2gq&um35a*m+zhY-*m=Op1x#$~2`MWEZa*hOH?+5)#EW>@z&iE*?{m><b`>Q6as=)H6{=kieg8W~>9zRHoWXZOUrlABt9`uVev+nNqeF`$=VS(zxIeUbWMooK{)V80BV`2=2k6jGzH9%)Bh;95xvlNm~GE$Pa9_qI`3VaF4TGgA8d=+tA{QZJgXXI`7Inblyu#_-VO75mS|1+_SWpj>9!~aCM5AmOCyiT7-sR#GaISdYO>Lm!(|h=g2z~O+hGU=O$(3_K(fvU3SwEvI)x&2@J4T=h1eU)&w&Bp3KY~DGhM!f!j<psigiaLZoS$GczzRUrzUA2bf%a*H@U=T&*$Dr%Wqz0SyjG1Rvwx^mI(rx&(kEQVA?>K`V14ZxG4q^axm7UEiq7k3<e-$WyMtVkzlH<iOn6*)8L1Z=Wo*&fOcl>MFs|)i)@UOmY_1`vZio7gh@j@M^D6DRbgZ(D+$y3ZdA5ByO#glBdSJW=VZ<R9>bO>#8)5UFvJeGb!&iBPfmTicoVci%v(JYAfRKHxEik9yjJl)N^N6m2Q)Re<*Y}aTB~pVe1oS;1t1BQv%F`r~E^`kW%*7J{wHiiE4WDysT@4s$6o_(GEd_rTaF>{DY-o8)DKYfvd>(pXandjO?12hK`7cq0pSK_9U6Ot3?_?E>b-wby}K+si;HA#~&b~)iJ3Q(J+Z9)qBCbmd<h<>JBnGHvX}}j4~~gY>fOYwLYQPA`6}7G+u65A#gL6|Ndl9mDyt(5*a-s#K1aYGZD#z-z0Auo*s9$TRu+U9ZT#N4CRb1t)xK2_dBrXXJOMp?1xxea8k*pEJJ>@HuX(M+gWBw64;hyj0@im4@Hm;S3BQRnH7OA={dZ<4{Tu+a{hP)Y!q-0dEm(03W-S$jI)HiHTV<&B?qea@Fc06=h!b*KNkr7qm#%bEBaulOX5giJr$N22oG((pXqM(Rvoh~<9k?MM8l+qrOstjpl_Gxo<w+zd;KY-mafeC=JkavyW9(fny(V5wYb?%xx5b8W*rh&<Z~kTN~YQ@BAmT&H>^DUnZRAglub>9zLfPum-{IVM-n?OFgq*4%p%$dZP72ppk)pFUMW~914MJG91-9z0$q-0T;4DyL97TwH90cG3gzw_CCmjUCDF>t#GO>u^$cQoU1YqF4ciz&nYCbDaN&mB2qjTA9PLXDvXuHNq?PiKDxf2~Gz>^q=jJn!0A@KQ!SOF(ZwY61`Zf(U5+Rqdf;@E63;xl|OX;Lx1hm<kS60}#ir0TEH?xg${wN9|d13};ES9G_r4GC8VaXSa;UNq2=eqy>AK!ld*I)iH=%Hh|CRz5CQe6b<YXEr=ixbrzTHE`?W_e=5PJ-vcSq=uXp%O)y@w;qAp2vspKLt;<-b>zYq<xLHnyAA&ix>t98VQ)D-ynpi4yk!*h@os5M<WJ|`ww8gMr03S+0heD+>kv*r5lyRJfbQDK|IM_dbt^e1L`4_iz7>rUFI4dsdA@#S)#0TNcM<sc%r20M|yU!4f&JCXBFK+E~`Oxk@;SL@rS8sVwyNsKnF;<w;zmm3M{FL^l=WqqD!K8o_I&RA&}xoT$bNs6y#Z%T6W4y$`pEuQHjc#`A6V2*G_rO^kuPElQIkfh6Y7`=NRK6b2v*at)5YrnK%SOk$vsA9<dy?fT42v=)hPvnTJ=ep?DoUF5@<X2e<e>y(?$mWkr*ql=3cGMV8OyEuv;;>JVzTaj&BXxNT1#xK!S`ufy0OFD}Za+P0`fq0Bk_wWWUoXcu&nOZ5IYL-YBuRg{c+1B#OuIHHj{$o$2TsZo+gZ)wyJ*s9VA_Cc#KpBay@$}}Bgj^0;}ec{9|J`AQisq`pB%qO<U?xxf(#7M|oZv&i>RfS4sGyMU+HXd0gWEttj@QxRq9XM9Ot_^!shE69%O_5b|7KT0!86S)%hm>|EABm$i^BoA%I*#hq;xyD8#m<~dza6WNG8UOh4TOw7iK80<F6!8cG|t>9FQ(A6VZ>u{<BplmW6}#W7Wp42MB$@LJ#{#T9%X%F25?Re1#G3O`X1}3)iKK4V)(q5t>iF}lr>d)gzvM+rEO_1k8};3+A>~%Q^zc@LaZQMCB`ToF4N1QX;Gy_l75`C`5gZ)M^Cg*mv!wStbl^~x&U74G(@faK_d@o%gy6jh}+eWK-sHn^PbA*E3!QwRJp))TN-Ys=$hh%=8bL~EBXLoJMUzymsF=&?}LOP^^$mz0QCZ$@Q;baG4pbs?vkiVW|`0FRXkTbbZVxEvV!k1`Di%}s*_gLY3Z&Q>IGV@(U+Hy{9C!oiNr8B5|t!)Ld9R??Z3Vms!n=i4eV>vx}RQxsmTCj#^|4Kv!4gq?|sM$q70FSQ~&V2Ww|qFaPx@x`@6UlqinxO^OV>dhLbncp4jU(=iX%+KBZ_CJAgNyH#E;VrX3JR1tP87Lk&Co>s<7%j)Z^;URhc*5i(43eacS&0U`Q|9((UGm>1RWW%R>J6MkCh91OM}Py|k>j0fZFIhxSLEi9_1RZDcgK6`kz##8rvWJsaFSyX*o>T<ee#E|p}oL*8kSEHe)39KJP3Sc5BNfZ?n$aR)yR;Ff+oLc&20?6+(CDZUm(axCQKE5k@&l-0%+pvqARP7^*0y!Bs8O8ue)>rYbOp(#0JRp1*>UJug01UG}e*^RamyVaQFEtqZl9w1UQFWqCD#o{gF|I1-CM!~4j1IFRq&tamsT_mebYwKq*^D~q!D(+_HZZom6XC}kICYm}M*oIkS4fpRJrK2q1jaCJH#@vWU94s?7DlC#s8uI32A>*Y(PemxJyCUfA&#Yf5su{;Y8R0)V{TV6_xkW+o(P{9%l2kLGUn{h6TT?WQdMhJ6$hkMRlN~O1s7hcrB76&x6O+&<hpTrT|4q@AD3c5sP?V9;r=kU9<UN^h>;tzB4%R0VggUa{uO+TI;ZWqWqIX+x(qMS3nTpp$OI)@nmk{689TcDOuZ+d5=rDKl8V}OnN+e-$e@_lY|_Q%{WYIe;@t>bMrA{`5P=hC)t2%KdQnLNl;MH|P9`w+noCr3Iz;e>I&nc@%9ZTTSwvo<my#tU@0T;qNU^8^){_)i%7w_MHdITu!SQ>lj*v$IzVQS{W^0KpE+5Jn<E1_hF`FNDG}VR}3B)D|QzkWRM78q}N7IlXF=$e-O!0}P-kER`8mc4zxJC(s$b?7#?&TC3rX%I3;*SDeHC%m?oneYc$7tuy)5?&=j2bH7S`%=agH7n3X1U=vvVAXlYl}*lAkxHum9J`#&MPQ+yGdY9py_>y0}7=782Y5;K60o$ptc(g`X!Rx$?e$@{+L*bxxqE?<hRD#{w(6636s`h#@#}G?L*^tJRzoQ_(%c=59AaczQFV$N|-NqoYqYz;|(8q#xt3xKXLOA+o+t3fCi#Z0XvXj$}^SR09<EYVhg)F72t<YitsGjWt$U>9^eo#7T|#PgAEQ7*wn2k=R}UndD|})bSCQ#7P;z&fJFqkBkmDA<e*=kXRt-3NC4Cb1bzZ3ma7ck9@k90L$v0M4Jk}Rt-#RF)oZESrXQTpmdB)EtT!S@UQ-*Upg?_B{217z6ILiaf)MISp4E|k=(9LMm#>zP;0Su=7+m;+>pmuqk)Ig{7uh>N;H;_C&JX$yFsrqPB)u|5gms{@tV&M(?V+O`BYgHb<rnvLT7Ss7MrM#%$a^N$8%82}+C+`#pk?kf3Ne;quNkuh5B%{h1FK<InkDy0M^nQ)gsDNi@(pxuGzBIXIKx&p5}66lozCW^rP}H70Ta+kh!8P}AflM!9&llHd&JDkFd|QqzR(q11|E3EwOniTTauLT!}!OyKaT1Y`2P4zc4ld~gX|f8xX~y@A}9+vc^Qq=Gd-V4Z)IRKodoWY!m#A1OOLgg&dJRBWLSF+kpQ9enjd1>Z5fKrnWaD5gqA9nf~6fvs@};m2qjT9AJLhup~Prj{Jk_(LFYqr7>y_!6UC(};whGMS{m{o_6FGy%?8}E-f3LYS{n8ss(28@Zq~JCL`$r64u-kQ;s-X<az7A#Y8~hNxc<xeA@a2w2Yux^1JJu(0R>CqrLnye)36AI2nx>4<EK#`h8TAffMG`QB>0^40Y?`w0j>7ec<$vJp=TZ-$3^OLay7@I2JS&hkb<&UFPd}(ufh?_C_H)$M=C0V2Ys&o0ay}d`TWZ^UhcxmKLy9TQjRSRHBf9UcntY)sxd4iAi*LkQ@rZqg(b%<x5$U36S!oc+FbaD)?Ms3vXF`GCNL|`Oy_f^dnod=MsJwpCon8vuzR<WPJ>Px<9Coo#{MHzEd(PQpLV%I(2mJzKE9?2e?h0pnvU}NGKGzqet9Ll-{1#B{vpLvJBB{@f<pt275L47G~PWvU&&T`-uK<L1Fyi#EK^l|hLCkbl%W>07JyZ}H)(UsRBr8LWN@?!Z?BWjYcuKb$+W5?*U)uLa0ZNAY<Iekc2nC^6P~(G(nhD^P=qfHXOToz6J;%O+_o9@q1%`nrlB6P8k9?-0dBxJrWCH1dDNAYIpe(w`Dd^QeYq#~Sm!jX!jl~m>AIN&u=caea!RijV{QV&5fTYttfljOGuj(gc%ySCVRu6j#0qn&AOgqNlS}~^-O|MZqvvGwKrsNM#A)Uvi4Z+@T<M0L4o$oH7;z%0%b>PVm_fVG*x8LZf_Q|>(5nGr-VcoIC_}EG&ZaLJ&!q7PgMp8oM6WDZ{7_pC{q!U2Ux6u?2E27fm<{z0tLLKo2K?*hVSC8IjFaegt5T}xWX`$FGT*U8tj4yG^#!`tFG2qky)%)|@nn0}lB59Aj<2rSCDO1ft)7pGxyO*SoTp|96OQ*R10~?s*!j`j5$xys3{eV#E{f@t_E`W!iyojRZgwRi?2mzOq0%I6;W1b<Vq8|#k>)U~K63QD|MjoO$NHSA6PJ2gma2lqskb9aZnjxsa(_1G{!I6gFM1CU_1<ZliR-Au;NE2&JDVeUzB+72^{=8p={pRjqR@QvUOM^n+s8~fZP5}XG#@v3{-O@QWu0Z3?gU%3EYvR5sipw~?IKLxxhDvw<u6E)7v!u<8f@){)Oaiy-akQF8Ikte;+#pAwtLe;FNF>fxgjm#1|_@GCa|ZcIoT3LryvUy%@i1YL|G@L?V3Kjup$!>`~%MiL<3@`!`ig-b=l`0u4%|ie*_~xUhC780uv2p$c4XKD-9wPVz`YPam>5uNmdwg-9EWE%zxmE%P%@>Lo(cWs+XqW-8fDAenLX`umKQys&}nU>)F~b?mrCwlx!g`g{{??!nK`bvm_vpB`^QuvK}k7%FWA)>OzwBueFJDJKHU*%P^U>nYpjLDk$3wSx7*a4=wkDUGYg5tOxz*3*h5)o8maARb5uRWRtmHhWi(ZZsWqI<oOCe4oEqt*f7A{h7q-MMWkSi(G_Or2`B4qu9eUAyb0C1>vrb+T!%Qz9_%+wrO3XQfKziGxvSOx<J)gP{qfEG@Z%lWx5xYc+xxHIe#cLx5+fbP)_;^f4eL5)Tn*|`%lx_tP+|WLG~X7spk3L2;~tbwCTER#{)1Hcb0r2np7_7BH&w0`*vG}qk+hC$yE3d&%~E>K3ghkg?_T$uFx!2}tpjX*J^RBUH?aBY|N8Q;fuBMmjz>(zkJEh}jr|37g@~tuC;8uEc~Yyr_0y@@B_ltRV^4F7k2q2E<|C25|NZ69KRuQp!hdzctCM{k%huQMp8?F7Y}8nXxTol$cD#5z;~_#oXCy2(PJP_uKmX;Y-+%e-rypDW?ISGt+*=)f{pt6g&(*G@$~c?zN0?84&+z^^YB9STssoNS><YVlERM~P#L?Aw_6+yR9x~R@vHzcc{qpP2|NH%u|M-_9Is$Eo{k8MdHrGCy!+egksMhb(j@eJVR-C+CvSwc_^W%O0L*mQRqdT^r*2?eSvTNFW2iTIR=)kB433TD%@e4A)7y7KR?y#Bq^5^K`6Qgl<?Op!P%ZrY8_`Ej__q$zJs#!n*5%3H;qn!CUToPnDky-&^x@N)Mehy`cuLL?-M4AB7k(eJxf7jlVW$jt1pdTm3P>u^1J)Tl+Hc$CF%dR$Jw1Zp)(23aA`B`ARWXG?*#d*5dDNQ1%Yr#>iTf2{I1h8}7BGSMT{RZ>e0LXt_i`)nDe7?s^|A9GKLq~i@KSeyQRWAPU0YS&6eJAy0*K1Ob@XCvO@afUCeq-JvJVv$a30(*@v{{mNXb#uc*fI=j3~w}<Y@75wYoC4Z&-L2E#vXd6ZZ-|PToeJQBBIWtw(000PBey&B**}CE@hD^$TV!l2N8X8hj@&o%9tGEVl<8l1-@!d$hN2r{>^7oT@A9;5tIFWnO1qr@(^D)53(itOTg7)>|K$p*0}BYgTcPVp_%^5Hw>~wYD06BC1?lRlnfiJ`jyLC4L*K)k|pr9fX#8A^RK&tG@RUTMwCS39tk%AR09!wKI!RnzB!hLpWKYpVx0Yd{_Xw!??Ni^n08c)usk3L{C_U_?Zb(S*h0tUMAoi{d~xbFN{84)=jX(DcQ)LlV-8b8)=AwVn{)*SFh#Sir8w_n9aWh=DfN0Mqq(mmZ#d%~$TZX*f%(t}q4Xb8NINxjf;L`!%(KGL5U{@wMNqxnX^0XQw$vDOAmD!{wM9K8JdHz7n-X4F1X>NYz<bZ9F+^-9d4T<Y1Rp*HM~rbLgH=G(B%$upd7c`K6DZoq>e|Fau#p|(sA^GN>}b+<gry6n250e9nsR!r3pR~wzROPSm9y`x{|hrP{H-se)eom>fc$5n9<k6rVH1v`jMEEV;z>@}GPlK%P&R1ympKrV-aLJ2T&0Ocy;d!{m-n-i=sAReF-<!AJR(mm^qY5Gjydgm#|JaRvA;=bHB*M%hY=EjB1GFB1U`ILb3<I6A>3flajxPy;cjDhXiiinX(?4@zx5N+)4ZrT7A?6%tGg6yb9G4OHPiP)mD3>Bv^AdLo-XIWwkX5UQW=LFXvUF6`Ebu;n)kfYiKb<dac0Yy=HQdS*B_eX9quc-ThzaP`}WWGFqv{bc_H^nngC8odQ}}M=VVyC7p9)`n*Sa1A|j%099B||TWRT-6xVArelXZ2gNwvg3ZqOCUAE1W1xC54ctXxKh5nVOmV=4eu~qEhAHd-S57YisFbDJt^pDt>MnxPPe{S*`xoUVf>nM0QX6U~7(OdKj?80)WKU;zEe7>td^GnOW_kX<E?ywa9p@x1o$A7L5o7e(qAC8$WvTR1sLGHu1(93Nn#DSdj_$`Bqlmxy#a2WWstiNq;`LXNFQ{?c!X&KcbriHn{E_i<@0uWX6g;@QZLX;&qFM^~z^Y}o11ao*!4Y)Fpi8n^#jZkH0Q(z545(9oPX$d*ddtiM@rR_cu|Bib)ifsd+pmLhsWl5CR6m2pl2PUKzrK;LnSSM<LqBd1d5fCJ?_W8KP8jDxp{F5^~H*Ad*=kLKQxVM&?&|o}VtV~;sqUvmKPwd^QzmHjZ=&(Z6Uh|GkYtj-ek5K^OCyH6_&ahH_w7;<tBU1}iJVn|wou&!=J^gasM!gNG4YAH{SWOO-Y`{10eV?eoq1luz%0;BqODJ3mxz}97(f3^%Feb|?<`llkg@Ob{-oMEc=~86onq@STVSYjAFPXOO$(GR@UC|ei`b`an52tpNCQ=|^L^QUn$GV5|hW3FGE|+K%;bywWZXSA>DQ(vW@`y}|ni=3@L^>g~T}L}A0@$Pw@MAD@v^?@&YJ!9D1Lf>viOhE}JVd=4Jg-!%O&)mddv^dXh073V$&MIXNs|Hdu*mALHmyP4cgfI$^SeeND{yx0Nw7l&Ia)92J`cLT7adLzPAfPa;c1(P2#X%p)Z`l!@^z5&clc}bI6eCkFRy)o=P^=-@hPz*qEWXga!v%69H)NFVU^!*@C-3zYjnh&{MX#jkr2Q&$k;Oaz3`dJrm2qc?ldtpr|9H#R&1(6C5A$$4WAOQYvlA;=klIgvDP*|ygdCpPYJvXN$9X{8k%>uM|PSLdO;v1{3Q7@gVY@ZtR0ymuHK`rS@J0Al3|p7n@2JXljXgZbM5F=Q@`rg+Mee{wmuQA<M{`1jv%vC0}TOX2~{rqc`i@#_!6#9iAT&0Rw))+B}g1W*+$_aJ783EsQmPq_=eJWM0>@$Z;CZPhBf!JhJWI39nZ2k1;wM$ewI`6ph-UFQe_D+$aKu~7(p*fs=7HhC>kbMNOA>{T^H&I)>@UE7#%o)ls_ZNzUC{E5A4|ff;R{gO=RkEcOSJc6J(IoFR+VW%QH}4cf2gQgML(bZ0jn^Lq=FtsFH?%NzfTMhS$pVe$LWkZgA7?n5H94;57FX?DqbuhUx?qTJHt)-(+ZTTNI78`q_-UVF`bsAGC~WZqh#ewq@9dEGy}|UDO1)t^wYJ4)m@|Npdr)NFe?8FHD^J;jwHMN$r-Nmp&97Z=Gj-Abk3Mg2>+N1|TFg9>2S=Qs$TnW2wQ@2TJZH9n5M|8D@{UVOz^HefFxKLX<OXpW^|_=~(cl-+9^OIIBxu$OpZ&NJG^pZB^1PBoK2C`O4L`aEkI|=J|@pnTTHJyc!HE9y*NGOH^-vSOFm_TuZ0CC`j{B%8@)l5KQ;4A@-0&Q{nZdl{}Fy;_4GNV633gLhq9O@PkLt@8hM3)+jThH;|qc?&}4VV2$1@vJD+-@L;p9Ljv^*cAb)m$_Bmy_8T6WPvO$9NWitcV-%#CRB;V+Z~U8HMZ^A<C>MLtIm;?w-FI<MSw;BHqtKi}Y6K^uanJ0PQNTYM0K-1^VDRR_4*QWDGr5nM7Oyz;Ow$rXYF2U*V2^k`z`X$j51cXxh>Dh|zqYoo9jUBN#Z9V`{w~YY7q5S4ZWytm%MCL{Z0jfmw_%IFDxveKUGeO1jIU^J(04$>%+D(^y(TY<$9|_(kRbbZ_@!kSRoOiam&$NZ^e<$z7|mWbE-Vl=KV~~CnL~7B7Ro9Sx4<DUSE|XILAchV3`NF*aUcVy-IT3=&ZR32GS41GY$4R7vlWm=9&GUX?B`fzatU(%ffivV2Ys~*NZ$?Trb~;DQygcM&3v8bTw>NYL@L0tXtuCz(yfYidYsNSqL+)w;1+k@W0a}}&LGhdk9*l}3kUuxz;Pc#oYZVOV^48xp`W#Dy%I1mA%~psU~MUwy6aH^RA_Qo&qELrL_^n;Q3FfX(T_{OVy}Hlt+Y;UPcrnkg@BF6KvzvS{D>Z2Yng<|j-C~olw-XFj0ol!+t{}WQO}f@))h<l3e8q&=++q0m7ZP@t<V)GH%4_#rV<UE@oWKS%6qwO3P5V}I!3v}9DjTEp=+X1PXcF`bi}Y+^JP#+Bvs~7=2FdamWD7UM=a6LA(nH{({mJ>U+h=SQI-Vol2{xb;-C@hsmjkiVhv+|Ymjq{?OK#PaS#)ox9%h9$LG_xw|QRVjiX3hYnf<kCWEja1KT2JC5p}{bUrKryJb=;J#~zIPh@R*O2&0py^62ghQYE;rHs0G#s`O6CG?#@xX{__P#Oxl5V$Kc=P^&6HMPpaj*8A26`_C8B=*ZFr5hp}&WNKFx#CB&tW0K7;eSgZYfA|Gr5b|a@;bmu7F>H7mL$;DA+RS$ie*0TK8*Vc<O>vc`?IC*fl%KMqQj78G=??YkI>#z>Nb`KTPW*KV;p+83Fm4%bb?Jv7?y`rC9t%dbbxn2qK{tI-oNQJ(PQQXQz+1dHC~sw6t0<8FhWy%!_c5oC%KzJ1Y)3Ev0GEN$q@wT5SWcio#oDl98IWSGGT0ewEFetC5Miw<ltJ5X`RQ@sHE``2deD)Dt+8nAGr21(gyOl(RX`#>>Rr4H*ab@X8KRW-*wIPs5`Q{A(ELV!&v9XXNQe}<b%a8W`Zf%E8|lM0CcAE>n=*6F>KS$U@fj4D8O<@3GbLp9*ivNWs35zT%ep0-77xg^$9<QJoPn|X@ouy@+HL8xyWLPA`2n0p75zi<_I9Y68NsNEV3H3_hxlH!UQnK!igmpCwX-WiLov`Nh+eQDHt^h>kg(Qgv+w)kYVd0w*KKvLBI7jpEXJu11Xl){ne4)jNXKmP#-^XJ4aq(*M>C*h?>bLtoDjB8*QA^oRjgZoRcj~CI;1kh2tw2c@FJOo78VIpJs!&jNVo}Aed4%r}pESFIHbb0h)u|22Z?OZzu_jH|WzV+pKDPdCy50%TP)t7ybgST9ng_s^BnT9F}S=#MvESRUV3mci{5GNhEmKU}-e&aiP}7Rc=e4rjd!3UEc?%I`u%AJd3)>ecASW20H6qK|h7%*HaMYtGl>ITqOY(8&ns4E@bGgsCfUfPkl0NVRDeHHB1-wFj3zpG3y9jL2k_13o3CV@_!LGYp)$JW6X8q0<D#trXm>xCvrY+`;uVrm8!r|>q1D>$N);vTpcr6We!_N%o3@L=Xk4uUDKfL_~M6bo<Mk9D>aGC)oSKHC~EAno}H~fcz`^{{^z#5kQTSZRvmVr3RKQEQILd3u&CH?FeS!qi>otmuJf~^jTE1j;CRtXpvTAyP0-d9b&Jz%^SYR{hD{)x0))ffg=}-S72x`=G!f@2%y*GJO46oBXgVUSiI*g=L#};~O3iXRpc8C{QD7bR?xp}7AL@$Ev@ww;NVQ<=0PobMA;UWDj33xmHj)-O?gwN^(@LMn+EO~JXD)M^ypTXct^~aEXeVdSwW(uB376=qpaBDe*J#2V&B&LIQomi{0FRN%fQKv`b<9;8Sc3Q=enlCKs|(?n<$FV-4gCcl>@CHbQ^ze+_Qy#k-Z}!@F<n1M$YI>(F^#HV+LO)jEat(-?){&7Li)jZ@~z=Cb#eyrF0lw+YuCcG&N>H`Ol9c?M1n5aP@%&=cRb{alOy$<&>Cr2B9#zG^czJE@Rua8)1_y*PTO;>D)v$Pf}&Jy+L$OAzJQML3sDpdA(l*T3v382C%M3MoAa#GvvF!Zw+l-|hA7?6$B^d)=YC&F`-A*ChtnQItlc&zd?u)RNQ(Z<Yj3Xeny6>F$Ou0#&jCUqM!6Um-u-B7YR!-$f1+L2WQiQUs$-;4Ifqp`SOc$pvpV$#Yspk-Vp>g^p^qnw#qOEYX$!k&f^OMH*WBba!BKJ3zG_armV`i})*2%bCCK@KW0aw^2=s$PV-*s;#|#Roe3|4Bm*q*#%6EY!u_x6^2nA|cb(9UoLWDbUy6K+B={_}O&o$*S2`E4-EHU(?0;e-AUk8<j2QcV%=ur{8ha(oJq{a@8m}5$#e#T<}K|hajf5o9rd3vFXk6B+%5PuA;s08Y)=g;TPVeP8ntnd3@Wu6S)xI}E-C88w1+5sFpO?A`wkjcYKB<c4b0>xii+{pE89h2EqlDz0O#Z2XiP69<OL!mDW(uH-;KxyII0QL%dAT}c{g0&_-ho;LT;5v=$ezaS`YII0*p!8?c9|HH~K2qcl*vobPRHEdS0z@=1;#*4Jwk|UJ7y}3eTgr2!X|)<oPkEo&+$TiL{XL2T`^dIBXj`PyPO@5%EEF0j-$eZn_hE+*?Sl-ODb?7w3C3BJ473A-7ntp3k>$e!dR820f8<ySB=#z`{5=P!a82;G**j!&QX&azf_X03yG^DP4Jz}b{aZyUdeA@X?Jps!jS2zC#Bxj*@rhFWfncxe5V&~!5zW-;DJ4=UcyS-_C|lhO;XN*LV&EWOfB&SfDKOo6L(l)>BP=d&Obu}6hS!KKOzG{HvkqKD7yT=1_`j(6)kYdcipL+kwXZ1ht#b7==s=sD1k7ih)M=t}V`r{_QJ!ilBc+HnEPH;u2c1?Qe&H-&8E{4KqLmOPe%h;TkSB;Co=#7P-;JrI!on6u`{Zq->}65hL9$T}8osvX1V%e09HWQqEk0TSL?~Wlfv^PCIkwJdDJmJ#j5~DcIrCk*r>t&z_yk&zulv;gUz>`zUq~7R$B4IJA~lhlkieOofSY^~{&BIe4Nqd8`k(ftWZbk|IzOMV2||=@4Ld$k19YemKp3Lyv_bQ#o0&~VA5mGSgh^!jo32scJF7(RLP}kf&`dA!n<WlQqF5E#Eh=N;J-)K;dK9LrweNPK-#_;s-yV!<Bh+<Tnd8U8nm5!dm#<Z*dX?UHHq$8+4PGUVHnn%}jTiUW_8p__Ab_Q`k=OHg2DePp!RZj!ccKF3v^PvWS@%Bl%X4YLi0EJR88<vncm}CQv)7Edp$)K6g9bRKYR0&8ij)PY?y{GIfm&B<)x%5XVl6o-6W`D^V{7OG&&x3QvYtN~@1`vq?LKAY8?D6edCFc<+a@UJ5L*Tg2>4cH+W<j&-S=nVGq3q7(vO&Ul(7s?5l0E)tXigS8OEeA*W@P$0_IAXs$&Wqq(r7n)6ZE2nvcscsR-vFr$xLJUut9Okx3k*DMfgG2w|~RGoG}LJ1v@-=n2N9X><qFnS{|j!Bjx>zts%lGUQql9DCe|)#S*wK;9JJ+PGL9c=*e(^lCnUG5|K;U!5d*n5h5MF2kzY1>B}|&Nh9U*cO7*x5*Ggk}wP#+yJhtPbc&|Pj_3jCo<Y0jMuqahpUz-HfX6-N{b)eq;cpIfRj}VffuF&<HLreXLAM1IQ9i(w5y0Uji{|rY|N7`*+Z@y({`j$lStxUqotoSOV5Pgn<yyekP3PjGIuNWZjD9Xxn$zo<U$@V91ko&==Aw+Je7{UgpwDq+%ndLa#m14i)g+<#;XDUq$X#d?lX6IOl?WGE3!D23Qs=#oV^9|Hs1MQ(g!-xibRti%ou^Wf;o1pyU)=aH$4FmqqZa^QcCg_bE?ee$oD6U8yLGq%`DU&RjQ<(g33Wsv`j-s{Q^lnWG$tI>QZ`0FJlUKXd0hPA3`bzr!U7&SCTz&HV@2m_LBe0G>Iw0hry{FlIY#i(t+&9TMMJ+3zupBug@1=U*blLxP{L7`La2dbm{(rsjwcyu3|njq8XA1J_;AKjgqs=%QJ^j`fXZdbliuMeEWD;#LeKciT#Rqo4DyCmkZDU=!D)Zi3A6p#*p}d;r3FL3t+UZ<rjk)G?6)?hv3no4-3g5#g4&@ooX%?<c|_iP@OZ%Y^b@V`+|1SjQ22XbOKB$g8ea$BMG#5)_XRvQ<<XB<S@#RH_fH5UuHq@1+eY1Bo}bnY}m(Dg#Eblg3DhTexfYIhfz9qHLHAN`v5<WRU2EMQNX<D2MxUr29eg`cuF@%i=RVECcaP6V<!@KD&2#}c(*>*Y7hYHO_{pfHl==P*S-u1<#VQn0^yJ}xMX3OP_%H!OO{5<o$0=&!1j#c)lY2O=e$fZ$17bvfomw}HE72#zviVTy884$FZy@RNAJRumJ&t*?CE0IL8ZO}?urPwJI#Gr^<ernUv&tAoAxm%>$k-HmAW~P&XA-3o{nyY0c7y6-@M<DKfis<bfUbVONJNpt7t)&re{<NkYiH+B_SRl1ZxA%R%0GbyC;)_kcSJRv~_uB3`AZOfkgANY+YJ=+;nkWiB7ke<&{O%G#WcU>5}`j;Rv0?89i-P7RU^Fw4ZEEqvPGT1=aZO_kItr6eoeSd=WpAXQ#mdh78O@+yjG|bfc@--o^S=Fin3)TUi8*{o?+^@K1G70FA2&vy9*fd;wO^23>y`9FQp7VImkLU-^;YPQTw+GuiE#<g8slkX~Dd+RK`cGa&)xLO>xC)(AG<V%40c+Z01c5sM-i&+R9{)Oi<>PFIxtDSS#)tp41^1~qgH15J@4AmjX&%}QR-|35yL9`ed(ds~u9&7ig-QzkBAD?&5%x^_;?X5rZNeSbXke|-Dxr$4@#AAUUe`*x{&zW@5|ck}bUEp2V)jV9yzO=Dw^HD96xhQ;$T1KYYZ=P2wOgiwpI!6nZFUnyY|+O>td@cfEzD$9snGy4U3?Y%EVyM_w#;P#t~{Qb|bfBxmM1Uf=OHT)Gp+E}&><09*O{*Z9!w@+;tbFDE8tBpxB^%x=k<=cl;cT|exW1Up-yB{C>77(Y~vKle7!EmpQ*kcW2hyVH4FTei$zu!OkkAImL!Vc_y%j~b6cCIO#i}mTT7S#xR-gNtkn1M{{Of>h*&Hs%J_b(XhY4eZm*W`Qbnl|47cPb)i0=Qnr!hhx+A07c5@f{z(!_wI0x9M5ai6ca3<YCiv!i=$DFSX0a+hT==VQG}SD|TE;Pue!}iZyz^YfW@)2rS_ZKnF?cn`a&9=<nKdxjdQRhS>nRP{-#!Dcxj@d-oIH(mnbd>g^!ch;~hG#(IDST%!J;e*fjSpME{e<Nb86QySl`*FPzrk=@5N>auj69wIsr{RYDy10>qGMs1W~c=u%goiitE=saJFhQ8xk<)juL5cFfD9x%A<dalhTwGVIL(}8K-#JmG|jB3|Y#I(!TADY8(G&X#JqSgyV30krO&)R3-`*Xb-W<W|Gh5cHm|HWcA^V)6aQQP!V8f<@K;0hG?b}nV)3zOE9#yQ~7NAJzuA{Ur1371HXXqCr?;7gi5`xZA${x<ASDC{5?Osa(_3$%}~#~Q?-m~o#nsTRAg<%<gB<1X}PVjWChXqDB$Nf|)TFL-9*GO@S|lhafa;T|FU0!N^dBKG34?O%UL)r?DyuuYy$ZYF0YdoUZ1`k#M$fB*aE6S6O=Du)I-&AErN(vLIoV-9N{qpYp=s89v+ui%tzPZVE4QYLI(dS@_MzLLAlhy2(MhCFKQ<)TMD-J<Wixl=>7^q~kxAl)nxmKHYEW_Ms3dckS{B`qc6amvR#%+oOCi_9RMNXZ+Vb0UbA`pY^8!=^D0Xcu69HKRE^hEpQP9V`$yr=d*-w#)hi_a}j5O#PLu(Nw5)rTV(;YWXKLgx-dWWsO`QVeE8i=Z|Tal?2Apg0f(4Nl24E3I_c+6Z8ykYO#*Lpj{T0;F^!o?Xl>G3EF2I*gy(igQ);TF*Rd%Zhwg2p;Q61>qEgO+Er}uHk4+9)X>50!AL55`iKbFwL&w+>^xq8%J$hp1a0WwTp^aQJ%&1~HMtKW?imK&cEkY5DW$uovFPbTYmXlL{mrGT_^2QS7>y91o(CezJ6S*o7_t8aSWG*@V<^k(sy@?e(+yKYB?BrML{~Pb0x_aSo5HXUWgE3>=!?lxme>dd-8O}LFxjrmO_&DNIG=|}u77zxp6{zzO!U(Tll!ovQW<&`qB@O^^dVSucy_`@SEeK#)$sgy{i%h1^RCM=r@f~Y-af`GQNd!~+bHI-XB5^K2i{HF-~v8;RvYp-mwmXwKtf*a5fD_J&mEl;Ko6RDOnBd(t37uR%(FX0!7`LJ@ahoGYhTYah%#UkNNYU9JzdU$ZD~P5aQGvykIKS2e#*Q*SBhay5@SfZeR>&HM9PPvf)oFn!%&T(D1ZI-?Vs-tz(4GQoR40a)VU<{;?#$#I^x#vqJ?kF=~S2b-!U)3%<blVN~*($3(WL%DvOjT$6%KXzB<FXndlTHJp{)n<rEKBDWaW_EJlEm%(t;s?BgE|2#Z73ZGI}41NsH}M_^%Af^Z#wZt^;QYIry6DEK&L=)QK+Tl5R;!g5AVwgTh%fY*E>+%b<g+Z|$?KGfjPR)f#=VG~<CI?Aaoa%DW|yj8?ofP-VbY`qM79=~OfvsyrC$T|#sTGrz>xBS@kewCqV8CC3##SMbY5!;CXmD+qEf_|nDwhqqAGpR44=4nm%65v4sBjKP!=bj|kQe`9^a>ZFLh_XBN&~tv@v7cS{G|Z6sSdr80E_$+(_JlKd1<PxHyr)gjOkqgJw6*{aP3u)8wf6bAgx8spW~XO%ZrB=u9`4~QxVM%S(onQD^$j178?j7x@7=1uk0QZd1WNI1K^>dcBqkb!c+?YxlI_vX*v%y3er^3KG-70GAy1u1suY3D7|mnia@|I~4XF*W&Ta@-menJG8FUjl>ZWYd^NQ;bmBH?uPm-hhE|y}*%`3j6z@=F<kTzzThl0qdJdx7V0D*1=|5txMgoeE-63mWM*6SA`q9;Wx`a@|(2f$%?PQ4OFgO6l-TTy+mL!K0FrhDw>24wb;R@MUUzJ~G7Bchxc)IP%numh1Tqt%~`*_wy2fC$QlBt#@#rtyiL8$=mH8rsN}#pyn$85o4_73f$NHr$?$<#~u2b;62^eqa31nv~s7Px?08aeCHXFRwMza|3I#5f%vcC^a5<vSEHzEpLow#H(!20f!<Z>d;gR?Nw=*ZY;wUlPhH0U11MIHg$1~cc;mMSpwdwX;<!Na$0TQU^i$X+Uki?1J>cV$J>(RLLiIPjy8d!AVEHBETp+edt@6}lEwF6=0sJ<QtvDB?o^{#qh$~LZjQ{FC6D4fscI%5<l(*3KEIIiHqN!9h4wYn&&<1-7uotmwf^Uyzc~U@vd$6+pCmk+T&z8O30J0W#CSK4sct#SVusGp<WLF3=IR!eNJr;08H&o}mKuuHI%ENdxy(KM3!kV=$B%@vPa4QO^X8u%tH)ewm)wDErU8_bfZ`!l@tPZCg`#zU`l$lDF65T2wQ5N9BUL5VNf$nvNV7q&Qu)i<U<~Z?a?Q6!`zcynk-o<+wE`XB^<|23U=20|Z+yK*wLAk!b=Q>TlF*MT&wthBa%4q~7~teNoONsL&*!8(eik<uOxlzggrYGNV2t~#NG<yM<9aa12a)vL0y*p>lT8X6M&lQ{UCWqeFtF}BhY<-<$G6vh&k~szKxBSQs{=sl_6pyEN+_c_JN_90gEfn!_BGB+ACL?BxNN9AOC)5U>^*KUD%RHl*&tu9jrqaCSZeV0f~v2t0!e|oF%!VtFev89dV2*FA<!1~aPfHP^lUhl>%44oSl6Y};^Qt_u$$_mwK6~##+o_m5{X?5r<OuyE>^1Nb<R_zupWI2{QU%@usA?fPCrIna(+F_A!=j^1gb8?q79lRK+5ZljzrJc?L)VAWsTA(dJo{KAb&l+5-!cN!P_8v!n8zx9TF%mu;ZD`DsG{;YM|8f71^?_CQydZ6QJ)oPn7X*dgTZETcHP(b_nl#wx?_gd=pU|O%V{ngWI?=_JSx_4Of0Q0H=e&o5w9|A90N0K4v;{;-D<uM;@uvc+v2#QyVc_$-rNMaFu99ND^c$-0Nyc)1vc_$<fGkDNDQ24|v3+mV}(9*UNMIJA1@ZLy{5*_l0sO7e!X`JLg<)`?IjkI~<=fj4BzJhO}ewJ^B|iGGq^t`ZW-^&uUiEOXz4Uv?D%l-a&4iR5><-a4%LFiVRQU<#rk{=!P)o%akFKY?Nsd;SZi3BQqV2Aufa52TyLb4Qo<)$?J7@iAllWIZ0(c=k>IQScXWT0CqpKT#K!?np~VBAsZ(>jf~r3@_fae_ZTHKfg41qf8(Z`+rojr>JeC#aZ+=xjOf8JeSU7I&6R<H37N)(?`G?h)KQJ9asnEAJrBVm(<<^h7Avo_zL*$&QN}0(*i$^UCmFh)La4&M|Eq`{elw5QpiDwcL(d9L=78YLy*_pmrm=4mB0#j4{1fZR3L{Wyn4uW_@<U=g<`5`&q6j@b^FyYP%bZaH0pH1cxoz+(^`ji4++ilTJ^Ro#5m43Gx3#BOLY!R&bp%Ld4(X6Hlrxuah1eRaCg<}H9+k~w(9?5le_!lZ%~8St5GYvjWki-CR^61J^Vx`@QfOzItu#DZ62l3TQ6^g1oFath7LUO$^2SkksI^SAhm7H>kAdxpoFC6txGtYpTa)qiED=*mnEeY<W??at;)$LHv6qH#Dg-=<G+E5sWgTqtu%m*X#>(d(R*CHHT~W4By!KM$>JUvpGEGi}>?sAAEFqqgDlmr2>)_K^fXa|*hh*R}^tHQ8qV@i<bV8>rcSDE(E8(T=J#|KNmGPBlq}DcpE+m2-GOi{q8Obe(DqK-T#eb<q6>pQl_peS(bmMp)K8n6z$<5{c3x#Ol)TUr+lZ^5fYu+eb=@#^Ce2!}80uN}Zvy2GOQR?|gdd6&}WFwA&_c9s=dbQDad-`!0;c2Pdas5vOK@Flg>{WGCZ9~u@&q##t+zipPV5y6l;FiEw*hg8wib`mB*rDPE5)Ja$+8jGj0K1H`jxqT#7}?a<yTQ<Dtj@1RIXORXS!6-r$DE`G{gX{0!Hh5$Xvz6@Ucyr1*a<g41(h_J<3?oLsU?T_Fm{SE{368OJib7iM^stXD0c+t<6D;lKR?LRW6k%hmI6r9%39*bl%Y#S*<2I~c-h$o=@`84UK(CZ)Y_i(*eR}#Q+&Sb8*LQPUik5=UidAeU4&k{g;$Ch69w(XnAC5k9E0VV))VBkZB7>3v%f4;iu`;BZ3&_sH*;D#QJJST+h$cz#d{CKWFO@>aSQp@R%}sbDXQnev|U(qvM@z=fJ>j+!gUA$&KdNPi>wgYCW^A{`J`CZSAt##OZf>e_igl%xV6$AN_lv|aAD5kiC*K<AX_O^P0$R%*MYOtyOGMiBq-^mN=JlTO>(e-AxBNToVq`%@+TP=!HpnZ!u?!_Ok#IGhk_ABAw?fJtU-Ut*$(@IL5|OJ0T~yO3t{FG>uR#<*qA!Z&x-BPVtt|sn*XS|7PSGy0&HBO+qsy?>BVw=H3Y!&u33%&6tX^9T;vbubQR{c$nP!bJtQ5hQE|{S^>xU#B2XzXn;d~=KT$(={INRh-AG96O6rPxw8?@dgFHApthUw$g=+IzjH%CN5|apnxVM2Nh$?*^YD=Z4p1I6v^1MCPdqFC5;ZEMSt#k@>iyYK6lcaGZ9|K)F3P+p@mv-<9*D-9Ltz#~0$`V}<4R|O<vl&BRa_<clHs~SQjm=3sZM0}!$1Rgk!`VlUg$0R7ow;4jRn}=#r7AE;S_Zf?pB*2&2-dK2yEaXot@0e?9wD3T%uS<@b1cbJs$5N>eO(VJ+G9*QVCh+E`r4@7X7DqhQz>NQ_OA+$zFgmIS|fcUL;wy6|DyN={*qMOKTFxikhka1!565&{6*RG8cPPJYT<syoNB^~x!niTW4H@~1o-2eXPq~NbLP0f_ehOb1y+pb{hj9o_ikVD@Pqt12a6p;tlcIie8?zgc=+2O&H=+;6Nz`X2CeAT`Uxx6M}HoKO)X_mAVRdqn)HA}g>j5@m*wDXD9t*g?1R*)JX1ps+0-Eo+XHC|GFWKe8Ezo$(Y@nNRbM<DdDu!QFq(|oeU~N~B1@9g;IKrn1UIFc_4h6NADZo(18l4zcs^)2Ycx#F$bd0$6X>z4;_qWZ9!bN>OWns}{^>r-kVGEFV&QWXQu@Yi$>AJkbIvB5rzR$Gc~ZmbT_D}+N#bi4$nEW|Wz}IKw3r|6-x=O{cGY!3%AV`(VG<#L2U6n35R)~RYF({^%7_6d4?FZq2w=gH4pI`fM}NRErBS~JanZk@__Dv=Ri`}D$0hctuZb{gQ3-BYr;yKD!J6E{N#3`+${p&wJA;_NOJafiY7`6$n6K05#d_mJ8C=FC%WZ~E*%6%GwY#V#k@4Pt2%reG;+yaL_-|_i)h9Gs(Q;#I+yoxpE10C*J0>{YxUhB4pmO0O2X+rTV73O7cBF#YH0=ukhhX%SMH?8bOZY<QlRjoQ#(Q-iGjew96+C|`QDvs=L}8RgUBdfBWp*Pb3=nLp9&dw78Fj!#(?8}p_sMH=mzE;yA|O~)UW#^3C%0o2TUj(O5Mj_o-|iC#{f!54AX8ekPaAx+qXdn{emy%i+7Tx;h}8^3OLA#=<7n}eoO<M*B_@D5IG}5SNy^?co5U4a82dTdYr}ufXbscV$}|d=B=Ve7drTsPTT%*cnd*wkhqVAlvASnj17HDQ9Reqkzr-2H4HYJDmLip^S<bnPvKh}%R^tpW#=(la=3kpegn=^3P<#n1pDT2KWJ8XTrl7m0DLVg)Z?1S)q$_bdEob>?jToDhRg%+9TwN3Wt91S^>RNTJ&uK*|Tm@P5H8>_qK5z7J(Z2$uu*&F<FxP++g`YSNr(4ZU`gl+U%QgbK_wr49_oK9hnsO8#4#?chI_WKu695n5A7P|dNFJ-MAwK2fJ?P#0@DUCH`GYGPCSL-7htD@~8{`S%Ee#uofuAX)_QIxFYdN-2cJL`4EZKSqU#1o=07g3{TyzwXWAD#lVhR`ev_S4~JA?QL)<J7sFs$sPuB)3Kw1YPL>%zDH*A~0%7gCUZjCkY0-BuF`G6|H=*`~=C;U6b~eQ^W(W14xMd)kYa@#S*`GuqtKli=Of=&0rf=+J$DcvlzSg7#8Q@@|`s`=shU2^+^G2}Plm`|$V9^6a}%6cWV-lPg~lz(>qjpXX8$U82ez-XkjuVn>M)HCf;GMScI=e|&qev5idAX?%_!3jrxmT3Wtsp$JlD-{)wiQzk6Gs`qSa8}l14v!}Q3KKKq^S4v)aJ(g$kf#p9OmWAX7S&S6oA+38KhVA);G~>W0w(|i629F^1bM~6CHninG>fi&%G)!ebH^n!~$yj&U`N2rbtF_YF0i5r(zxqU3VqY`1hQ9l}IEZg$)A*#yc9~R)0Upqu+|njW)OQK0i^OPw0|LGk88JX`UibZ3+}dltQcEAVVK2i|3}b>4r<Q44hB2u{HTf}rz!M5njVb)iCsC*}O+OViarMGwnADz=AXO!)qAR=>!gYA#=WSNy-eK8@q7f-Bk!KS1yy4Q&nGlh9rbQkTAron5H8Hphxz;ep{5JY5IaW514pq~ItWg8v9vTmS8J1qn22j_C%Ryg}JMmuJ3#w%qR@G48zR`2G>FdSz6dcD*2K$mcV%TvEaEN`<nCE%A+v7cvxeoF3&Sis=>a?hkRxr)qq;cpIL6epHfET8Bt@NR+SX$D|f9#9MXyYgA`civU*_aam33A<-zTvY`Q;n8=&MZ5V{I=8&0a7xP)UYjIQDa^(?V|5oG9PY|9*-A}2Noc7x`MH~S`<xg_KY8wu_i>Xg3?*U2@kSb507Hfjs#xIcFu1}ca*a@mWnSv{G7cBtw;?QVoD$8ME@U6d@w@<<_YHa9IAVcCc5bvfEW!Z$#HUW#|Y~^p99~YEN+CI-HeMt#@t(gCLljsrlF&Lfs{6~meQidsaBPjGKD)djZdZzA-9gxA!ny61Ub-jfH|U^|1rl&Ocy>3Or^|4Z<dw{WIwLEnkcz5&HwcY!)uV)DDt*oK%wRHd2k{V9DTzb#Y@8@=BGF#ZaRr`sc>1>NaA*Rc`|WylZ+11eVG;+8TX-N=sw;ReKoj{V%G6)Cs!TQcg1}{7($R6bpaMyCP&!Q>h9?=-%Z~sxd;z1VCdZjB+~HMS7kYl>4eNh4854*3<C22@1iP?>|UigB0AzhwU3^OadtkWahb<X;V0XMgA#U7jWo&x@kJ+Y_uQq#(8C_piOgwl9t*E-LX0E@InR2Z6?V&0oYWkL+F1Wo?*2X@K{g7R8j>#r{;!Ro!4C-utKCh(H!OTv+!SL{?rJQP#XNZwZ@q*w(3%(hB%;U1ytW<wz2BVKG1dD{t}^Wz6g~-FRgp(K-z|KMe(TeT0I3Jvum#a)yeCt%Cwr7c(h3NSraTCO1-q$UwcDJ^pl5lhBp$@s(yT==RWV;NdAw9hLygF!jZ<wKZ2M^G#4SmdNv5EuD=N^?1^p{vChmD6H>Ko+4S2*$RY&3b<Whozr7yD7<%eXi2>-g1%o2<&Tk4wV2-lN2(Z7RAqSiTmA9onvGh?c>M6=%q225$`b^G=YChB8q>vNsH`LE(an?EPh`3W^{m$+MB_c=1{&Awn%91#!0U|r?wH}BW!&u<?yohWttlA&(@D(3d3Y3G;HW3jr^l2DP70Yf0{8gN~!*^|lXnSl$UG<14r4CEFlNRd`**t)dFyJ_pZa?x)Ioe7!|0}tr=NtcR<4X^1WPII?a`3VihSf1=vrQ_YV1r_@5_dZlkWFlB38U2ybSGjM9d0jShjpo;7=YOog8Un1C$IFP>KdInO6ekjJj3{Ue@1gqyM6)SgpRr>YXo~o(;&LUJsm(cFdLe#%E=%%Ez#vw01S*AkXe%;h97whzG-t01%P9#;_=fNM;~n|q+iySp@y-13<LkU{mrC&auit(*KmTJ56;I;GxnI9&+>v9=H<i-l{)N3c77?v~(SOTO4c#28?|**#^DmDjP=Rv*@V#!)*hE8O2M23SU|hXAX8IW2mSGNM4b%QTG$HO-hnP$0p{sOpF14OqqzJCh&tN>VpYPY>KK=PG--EiJ@6X&%zyI>vPk;WAzkd7n&-YLZ=-h{f-rKH7Se;B7v&VCE8>(2(6Xr6hO0mZWGaf7Q9UIq!JvxRI#wP#suU~%s`G5cN?J!_$Ja;R1`<?IK|Knec6Wah=>;)*Qwf!`y_D^HtKMpi@(;s6)IS$5jjNo(EG|4-=Opl8#o2rI8+>TFC*>&|(A7>^UtQPbL)D*`Wv4nx-A(K8ivquk~6~sjVUo|$&*YJ;;d-1q=IyH#sNjb~NsVByUEZMFu?{F5Hzok*~2Ip~!E;_GeV2|GXjzIP|E=zp9(eaX~4j5?w`n&RJUDnr86#97x*#<4W8j9WSV@n|Gt5vjvStFjn_{?7d_`7HGmv0}RE3!^$w7y<arKDB%Rb7j$jGFVJ5|$1<)9gLbAc@EPs+<nu1A=ai)GmiE#Tp_W!28B>GZK@CDH4z~s;ALxI`aD;y82<~Jv#q|dZldHwr9zPt<;bWuG3sBpgVnxNiW52bAJ^bOy1bgQHuIs6qso_GW@40=bN1Cwdti0*wDyO4M9yaGs?)}Ck;i7lfY4$jv~~!$uzpW2#@miL}Bar@J)xAaI$+(r&hKE4SAfj5$s#slKTf@A751^_IU#AMue1I^a=+K&P&KU?(4Gzi4CgWWOOed8n;B2MTVZ5+(gx4UdMm_?fw1la&D@rLfHa^#Vn%w-nkRE4=1ik3+YhX9L8Pu&J%K7VKbGTSZlVWgu;(GOv9k_U|Jsv96*nlKQpFLC8uG!<Bu(4H^G$qdT}T?cTT1uAzhPr$avLSiASb}e#FKjkI6ka8Ui`dm=JCQ8AB%uRAumx5J!D5c&`jFHI+|<UNytwt-ZRez%)h(NAy<-Q$I*I#YzlEWH&X04j^TY$X%TLi+j1)$c}LobsP$hCS!b(;a|tVYVZcpGeALtX-HZ*$F%(Wl0i;-XlhsltZ5dCg|6?!j<(^F)2m0V8={q!CfmVood@KUC{$GWZmjgfK8<Rk%)Z!R$AP51srtFoG^K|MoFI%=xj%W0amcJ>BHsigHljM3ODvHo3)wS%jD7Fv%Ckm2_U}l@H8qWn;wY?_2Qs-WBoTc0tir50@vyUzRDZkYR`3eXG$$CCX-O(XOfxU}7)u99Fim8zDw)8FbGkS4+Shyq!pOV*VCF@3E9NaN>IDwJvvb5(O8Y_e9Ps{JiYDVw+w)b1e;0Pj^LNUqmcu?2iG}#zqA7J?e$K;JCUq_x(7?ZfNO=vc#m%94{LV94=6}b$2oJ0qa2A0&O;s=G>3$(tIxyHJ1I^2@x+R(p2v^fF%1s5XaS03xs%L@ZeFAoDbrd{}TPpSjv|YFg#ar|X>~waBp`Y;I^BJuI?IVcyfGt44J7yK5xXI?W&-GywTRdW~sfK5tQG=p3UPglt+zjjMy0sM74pu>PnZT<)V%&=2KiVm&mj0Z_GN?E<Bt2mV&$q|=?~k-)K1?s8J25SzT5+@R2tQQ{PgH<xX}%CkbyJ9b1Lt0V;xk9llYO&xcL{h}17qg^v1i<&m-QeUrF&MJNA{mly+7gphB)#tNfzQ!r)5c$$4JwdeU`thN#U&netW+nTae(VRs9$)uUvCVI@${?o*Kz@>tNr5WJufF5@Q*rnWm8A*WV*P((b)m_4i+74SEE2@w!&aDc`YaP5Psiiw+>y7@*E~hLzx>{f$kTKecU0P0hN+VI5Xx>;{I$O}xm{o1PcBg}7~Ydi^$J)jP0F+-@H59fdf}qJcCo)0q+!<m8Ez9`qmblli~;`yoK<r%1c>>(gS}o@_F#5s5;aLqb1jtZ4kkpVd@FO7uf%M5Jv%<`@|7b#8==KGISqz?=4d(%cV+C_Hs*=ArgkE#T%xhK!bKGB#@-78wq0gG=@X*xgVLLCBa(1bA2&>{CX7L4*i#`6vRR90f5USigCkGS&~7fc3T3aBk2vAUL+c38nG?4<HoNBTY2N$WjWXT)mD?La>X}c|V4`%EDBDiiUv!H907IB^sInf<*;MJw^i(K`i9b@g<QtHyRS))Wl{v%ED3$r|!RRn5P6H6`&LCQ+<z4U5;kDuy1s*31kBai5aM#X7ucdZNM}Zp#@tMWq~kJ%Z*&AMsNWDA@k`?)FS%+JXlFP0<|M|KzlvpGmyMl^Q7{+gD{OZI{^!qc+%%tX8+881u_)02zIfj^CH{RFORzBIRalYv3vNY6NWA>^sC7b=Q%y5bE;d8%Z_0!H03;k<heR2Wl&M}kVwlCXs{xP@<1KKntOUCKjD$iTMyMh?0^%E%#;-8m`m;AEw-)SfRD>{8B{CU;3O2PVu0p~OuLX=wohwAyBd)WGh*)04?vX5Y)<O(HXsVSyqqezk-dl(SL6n;OI@q(`0-qz47S$WfdKuTn{%FPm<VBk6{qC!;Wmm}P;~_WnXEa+FnNx3-5R6xdC+idLh{;}03Za8G}gn8v4u`p>;2^|BJ&bKCT*Vw;1i&*B0*a5(WzLoETQF`N(W*R$S^&oY@jyN?6@!p5YQ|Pc}-8xVCjQ#sXT#T7wN?P9GKvIHE0U^I)K8Yuhm3>q2{)N>$X10qSq^G1c9Agke#xLPCUe2BeuZns|y;=L)aM2f?`9R4C7tK#rrI$h!|HRXt*whQ_&!J*nBGDe9G53&);mFX4Fe<ca(X#s)Xz@>XP$X;gb96Yn<AgRUnSxg`OUXJHmTU3velIuhVO4uq*-ST<<_68j~NM><C!RD2Jib{hdm`*ZU@+#hiwwxgj2kjv`WsNpQvl=78+@A+|w{_BP1gGleKz=LYI7%n~Fslv_<e2A`->>D(>IUt^wXL%-_KVCPkJkM+r&Pv|C~^G7iZf)CR8fc9c3XbXFD5wgMfcVO&*mL%|lZp`JU-@lKUR+zYvGTjayvF&>?>OK)QjRmiEARF~G5wxfINM-1b=|nUYn)+1Ga|BiMq76<68#Xp>5B-TKnSmW+qOHlcSknt9(^)(6b>MjQ-6(JXqG$7d$+wg(g&8Dv>L?Acq1k>!C6{0t=4Tx%wg<O|<epd^^)Xd;5z`~T(-Q2*MSwDlsuYU`4rPc_`WG_dHFpZMV-8b?FgT{-Hm78XOP@Z^cX+NA-2LL(filcWdeooDyRRi1wA?8=iQ0V0?23#Q<fs@<?I^npIlsCLHB8_j>!v2s&q$1!L&B~1!z|ygjLa!P%$Ln>r1I=;IQP!;?`2p!B?6xmH+)7VG0xDG78u&N?ldX!HR^w5=t7{|Ts63vFhyTfUBEc{o6VD5+-Z(cF$F|F)|9ep9b6~yS3%wG7~-Vj*BSMTW6<B-%v$RLf`JKjk3{Tdp#+pTCMuu{b<p)Z1fftY^z;>lSZd;Z-BPgFQ7NPc=U`7VjMan$1rPr(ErA2}1deK2nS@LRJu5Ub4N@}h^|6~UjeVOCbzOM14H5dGaD<fx7Rs>Sn$OGui||Ad5^v^RO(hySBMAc@q33_toR`$`c8oH`@1jY4C(?!L{SO28GVL(Q)m~!gDQc{pPy@cbjuO!IGN>c1Rpv2Ik1O)fhIl@!^M$#$$~<+ljsAQ5zq#ajfLL~usMop>+BweuAA^mE+^N<wu(BFKKkLA_4Xlj1D8UDZO(isIfOnZDi{ZtuQj%KOB1Ic>_@HZ&>!d8D$Td5fUSvvd3Nu#<5nDpIE>-XfUycUSNw~R4eD3+y2{bQ;bJLbu9pwo#`APWnW`&QBNv_>xL#_3e#ntzh#<gRS6t4?-DP`}eahn^CErInK97Iy2m2rj+bqF1o#VMVrvOQ^uTD2mS$d%SfM(>Ld1eBpOPl)FSVkm<W2OiVWo0D?%hkmx25t;=!@5Ue;Q^+B#9)r*Z*B7Qv5vQZpDX6N5T`fTErPvI_8>8>4DOnMacv`z-QrutsPx#xRxU8o47{Y`VO*IYhZJ<(@>13pPfHHK9;%4%b?h=%o3w)bP1Nyi2*1AkG<v*qCj3{MGgP)iCkr*bG0b(>5LC(2dBIj1fsU_ZL5{F*VJae4Zym}wYBCC~p4?x#TMzCSbwOevNtCymbc)P-rB;&}gx#C7l*Qtqzm`ipYgwsd(Gok0RSxCt-pEbf`0SSo<pI{35%(y;S^~8K+qd$7grDUj4Kr)DFMFKCIr38)<tr=Iw%fyQ*PD_f>gABP;?l;<erui@9SNShnnCSxaV~?-x!b`)9pNGSRRlXfX8GyF4m2FmacDx55bmb|nkz1>_cVVlF<#h1(L0nHStj3?LsTN>N*tYbEldvAE*##zs*)_BV4i71IkhVRa{mZ%)@PTHz&D0}zz2>)B?Ngs*5iZ<;7ywKIBI=*$r7x}2Ekmsd(mUAG<C+R?>0w_I{EMu(fu#zmxR1n+2!<T>qjRB&P}ns`gbHp7d04BP9BNf;O=J(cDct_F9u8C$qPb-use3411iFPhzlt%8xgc)RBa`sBj`zC`qs-43XCkB1=+h>tPUGPmvMs8^{H#(JEr%z7ll(_%)#aE<p(&-BqNpt9tWU3Xh-(N5R;0||BBozIKbD11ex|sCc`dR#LYhbj4M5Z`=e>A!$Tgf$VL^V+b&|f&6R!=>HiM$Xu(EJWte7aKm4dMKS_7`3G&7?ZwaL|_#f{roSgNUV``Tb&<ujK#O`g-sibJG!8SdnL+e!$F)iI~k|7Flr$|`sabnWXZN2g8M0_2Wto-MogZrEU}BU8B1dVL+YOo|JK?;M~Cd=y=<K}aXw<}r<`*2|OqjVva>@lJ*Wy-rgn^@a|C;RIoB2a!_Q;GL;;s&c`Dwvas}O^;E=BD((C<Pc%CLG5OsJD>?F<l*<P3J>O7r)LW5#+0?ljqii<y$hhFA@VWg?K$M@1w}G{Q9`@M%HFBsyPw3S(#<0K#chFCTRBK2u<Oj|4d!t2z<<`dO*J0{kxJEhPSA1p)%QNguXCK*F~r(!V#0@v(t4%HkzDU;-qflFMH57er>S{3T*${rqf9w^eEbeLR-Nora;hP@accK<8Z4eU72nL$I|~J&gXWt?Th?Utz)^A2pdADbXF{oj#PZO&4DVOS@f$ZkMu}!}z?LT!w%!GLufD9F+w)h;suz!G1vFgo)5G+fA=e6)J=gHSbV~qHro;r`=k1)-Jpw=0I;aEyK+Ly8RRt0-v7DQfow-hF)DL}J0PUv=eJb0104a|dO?gIui+@yK;|13_Ndqv)S_smw6o+iixeS36FL!%uQE7--PmJHw&-$MPdZ=TNRqo$)h5jM~e~IwOul8{Aozqym)7>DbAWbEps!D4JzVqNewhhXeP$)&Ng4~|;7Im!<0FCDsG2!XP^=q)uL6dXzE<`iMClfubil#taWF`$p4IfN}XX{i-e8**7LL=}XJz^5iMEW}b<0h`muA&I;M=JDK$=dSvq~htoJg;#ZMH*B{`m`U*n&7&yPOJ^QMfNM_5hZ)H$)r)~gsly{RmRK+P*j%?phD?(Wzr3%Ipo2SYoq#Z9}j5r^jtFsb0o9@&M0jiWwcv{(iRt7FtUetfBENkO~GK!`*r>oA53w1H3ZMa+MoHXHR51U8V2Pcj!V&@e~r5c?=xBQ;mp|@@kROlRW6(a!1dXQXDuY%^=?Fe`cf$!<sjz`^)No3z;SYu1?w&oY<ie>A`}_)G=92ciYN=p2yZ&ABxotQ&ZGUmHiu)sNa4KeCUn|H4zo)b3*I#Hh2%|dduP(+U5MVeQ;_yw6nb>ZA?iWUbpd4NLWsBhVSe8~?jPSC4o}0Vej5Gb$HM$C)J%{m$~nO|RZx1fedobMr_4)!rA6LUsPr38`LK8I60YrG_Do<yzNQ8q58vsZFd{<k^B==3`b~yHTs`3wC6$Xh@ZkZWq1G<b-r`Et^*U))Z0CFE_>h6GnFH@rN`_?+Y^{I%q>$ZvBV>=3aR!j+)O|}|7LfxqKuwbC12(?>me8kM_x;)W#0$QPu{5J`6%RwU3{SP5Ho%QHP`m1N<CkGf7APh^-4zgKKtEn1Qd4FXiZ(C9q#`l65D$CqTqQ)<pP<biowajHt2!lIAUb0#T703ppb8N3KH5#L!FbWYn}Eo(AZVGWjHU9=m-0ML<Iu-uD^oB7>#0KsdUDT!m%KD=-$58asTHXg;|t-ruf7@ToEa)pII^JHpxH6O<&0l<Hm#x)V&)<#>vBFGJKop^UU{Dg>3kXA;w8B^T;1lrq=9tI5upsr4?k!3pG@v_K8I)@6Nnw^lQPP5Fd1nQ*JhUV5#4lWEl$EqRN8*Gr9iQ{OyiRg0t9wDr~tbqT}oai^Nqo6=ibccR3|Y;co?7B7H)38=Klvj9&66-=iKK1)*#{P1T}2zZQ}fk$@3tkgp<8qrYeRlQP-1%<}b0H<qJSdlMCE9=Dg^VSUw*dbru9M^OA@W?w5O&M{XGdZRR+LWL&-heY{(T_?QfpREQcg4HM^}LySCYNJ^p85j#`!x~LqC%N*h6d4H*2dmwR|*K@Tr`T{z2o&^k`coDL3i#pPBd@;{DGy+%XQ%&idhg+bjK1MB&$^n`R7Kj3Wh$wwhx{AB+d<=HcmlzocW6?UC8>wC5UaaSi@x01p;E>QLFnD5Pc<fMF==*80=dF(o1^Dx#4o^zAz_J&!-PofDOiRD8j{Cs#k1T+-oQ)m^qb_$i;{)_1dvR$p<`~~3bCJ_5L!t+d27w_qD=3#Pr6xdTdVC?PSmwI1m$K?H&}+WxXw<NUc`v9%o=gMbC0QU5kU-ZzVKzsvh&P?P69WKs8y}r2M<XNc_71~fvJA~P?|0_UZyz(|;!I1XMg6Nf)R(o$@kfhjw0<x|fG~a_yC$hB@kNM!+4h8)VtzeMCj#bPRXumIY2Ek~?M3Ifgs7E=SQ_C9?H89{bY@Rjs((y%-<NQ*7p&cWR*6IYM#e!U?WItCyr&FjSZKERqZcM$*07|;{1et?e*f0JtqHM4N@_m<Z{?|+z$soIfnykGiulgryfT=n4Sg@Tlpmi<PeA3fy)8+#uS0r8ri_n8r5#!FM-KI3Shi!j{=CVb-~Hp;Z$JI<&HV7C*JpdYWWT-t`t5h~^EZUC@C+Y#Z{N^-TGq9xjsnZ7zGA2ruMs~mk4ktVQVZR#-@kFC%Tp`ORKcE?G}ZOn{_pIEfD(V`0W`0L>tnahN4q$7|L%WNc#Yc`!~H-D_NvWze&KUOVU7N4K)~rOx|Ng7QHJ~<TK*7lVBKM%^83JVbzk$V_ieVqllbLM30{Ez7PFMvi7jvd$x7KTSTy5&Av(Cm=l=u~P`}V5ZN7ir{^v)HC3p*8hXtj9|5&z66TZ!j(&DaH^%@(J6`}~8d(No{(3xcT%eRjV;t@x0hr>SBNu}og@v)JbyshdH4?Gy|wQp&xp`ZId|N7<Epa1v!C;#y;6Fb;}-LIYfwbSf1$6qXlkF}`nl%H4Mej;wBZZo1!idT;fl?oW^`5YhHuW_u}HEq5F?o`x-%9Kk9o$bS;An{AwS7wJ@GM7I`51%ed>Rx-dR=|+H&An-uKJ2>k_8o>Lhzji{_3NL*rSw!gq6CVD>AE&(j|~Y2yb|bSNv&tB8w~wjdry`p>p~FW7;`j?%ac^K#@ctk`OB_yRJDU#qh52F8R-=GYjdSP{r<~uKmB^x%lqkGr!?GIud~Y%?#EanmRRR4BE)skZ?Lco)CI?;n#0(%bN*Gr5~Dd;L+3eHG)p?JRW1(j0YS%xfwuUv>oto<cBqSc@afUCeq-JvJVv$aSvN{D=MT+}==RZ#%A`mjN^`5W`O>rY+4ufjuSR{6l67N87r$Hp>6+)NK9AZq%k^5AKxMLuC^GI`%E&n;jT((}z@eDlo4Z9mF<%lcS`kr3jZGz5nm+p$H%$IE>`$<?A{WefKb<0d<37F~q7x&t#{F4B)YpP9#*o?pTv7!_G4-_G9z$A!v<9WbG_>3gFvQS>_y{{_CpXuz7&r2te|vxb`$H7ZvpEgwz~&<@kQUJ4+?V|J;l%lnXd6+AWY>d<1P5xE<hB!Qk0x{Ru1p3~Lj*t{TAR)T2hiiBd?I;vA8Q0QWweRb#k><t-q%s4^Z=dj(~zL@OuV#Io?Hr+rlu#~Mk0?HJUAMHz4A-Lsvk8CQ7CM?g90=m{%2Cn(UXnS82ZzsVWC-A1Of}Tz)R;(<Crg~iK?KiiS_vK2xrZ(dSDemIxp^@J<n4ECIRIDRUwI)2sW}~991o>iQwO4TQPWCr>5%tR08b93ae975(Y^fLSY_wVD_D5G%?ojx4w*4nVO~n3NWSQBxMZ-QLz36FYzR&0-4)_AzJsxsM)et411RKgf0;#O<CzxP|>}-pPjJXjENRR=}e!$;Hiav^RCM=r(H)-Gcz3fn<Vy}=CNlK*1H7h?UsKUe0Z2O(kS-A4c7FH(yT*`J2WS1UbIM;kREqZozvXG3CQjctsAm>K;w|i>$9TmRt19@&u~wdb6{JVkQy9*FZ0y8w2<ZB@tx-VxvW&i*R`KsMzuKip|Ie_{}%B`Tx{xJzkU1Xdzel+AH6cEbKy)`{41zxuc48g9E<nH)N@|*zhhp&7KD*lsTt8`&RW~k>nOJ5AA?;o*fVUW0@|?{jo&<4V3eDRRpZRZKI?rDBltbgQ`w&xThKHUxtaIm?hP8cpz=FT<39X?Z$zql4abARVX8R9`TYBk{1FVBE))6%`bQx5rzXpI`*V}mCR9VyR7b(ZGeZaWg3n*GSG?(ht-yHtFIC_!q?OhCKi-}$QA$mSeQlBBT%YjJBT1C0hSrdALUNIJ=GNN@af~EAevPIV0U;u4Z0j%aY1x3o-11}BIkPg2GL})T;#vd=Y^(KmBETm#Ux?-3DFiTr^CAG~nZxS|Lf98<2}nExBjMnLX55LH%?dXB3Jhg|ViQ#Z1MzUAGMRtw{r5fm+4a}Ml;N9OV>%7-vLq^wr0?3gJh4=L<oiY`ArHBNI0>f)r)ld6R2Yq9A3q<U@X9y1^(W_gZegPmX2X`x&M<qoEvK2`l4|NkK6*=`DoXC=F+=?g<pfiJX*(*TwHLo*)0*5(D=QTs=utf)+8Ksti1s%&Yh-F6dzQ%a67hyJZnnhbx{Z1pQX66&;;`f{6H+53T`$+AZps#Fnr3MFD5j0e!hO6aR86J^3&~Qi?<lxw7LE3xzd-GiOr-R{WhKc#aX*Cij%nMT>|7kzFJdv86ltyxrI!(K*TQq^ReAPZ7I%nBs2z$ta5LRwHxEUXG7i0!(66C_#=62mJA>M1xB&VivSqYD7HfaJ(P=EQ!k~?r*~4J>CqBdT5K<@;IT9A#gH)rJ&z=X}PlygD2+R}^j9?PyAp&}bWh(s!`2o2=@OT?;gP7{D;LB?b_uRmy0EWv3g#IzYk2uWAiUA1+fgf{NWt$I_q8V&7)Puyil{sWr0Pl${M4)O#fD=w8Jmzx+cba0DQ{vz{eI)WlIoG9c!lwkL8Kn=bQ*w{VB~o!jUra`u0HcsZ0BcpDIZb<H8+4b2Nx|-0Sw$*39SpB_46t@&7?4Cwe$A3cah_CmeoEZQJ>VQC_%X2B(UkQX4qoQ(%!_P&Wa*9W2XT(@s7zfJqEHC~CYLn~y@8dzkf9Rc+yH@K&=#;BN|db<Qt5p2Z$m4C+PwgYDlPj6tC=X){212U)6x40Zgo6MD7ykUU-i~-D%X6>rFOBn+kSt*cL^FrQkAp00jMYx?f|V8*>xfRY^_zpZXQv{F|z*f(L_}AdTq;J-Uh2+mzN7EHR>kO;);Y2cByN51~u!Bm*sNMk19`V)nzqg+Wi=V<vDY8Ywq^vq`Yo=Hy4Yk6Lj@uwuTpjRQFf)BqvbCdRv|I0^i2IP-*2qEqXRfYq*PF=;JJ-ns>C%y6v^~5xz=hZWl?r3lfmK9-yTI^y;!i+#)z61b6$F4}xrTMa$$i<9X>rU#UvbvBvc5>~R}`SmV<GOQeq7cNdMR$y~c*slh`B%CNqu7zGzoPU&Mb>yzY*y|TIx91Q!;c<^z$5xiS=UN$*~O5lZA?c77CsSZ&q6>?!un4`{?*ynJH8)WABV#XQPt#e+$!Fu(miQaNbFgN^R1%!yNWzLG+YL>#ITphlWl%(i&U*!;?Mk1x~deh>Z$g^+(SIrGTC+JVm+e?Z3C}@-MQb22zb<sO7Pj#H@1(d*V-Yc>VvU5+X{?{RaS_HdJ$t2_!iYx{?IbV@n+iC*JsF3Q26{jiwrdO@7zePeBFCn*QC2H=wxTmZleCJUhPGJ^;6VbS5_R1)L5LcKpK*@u_n+H2=<8jR7K4v<jbX`EXpFh&rA^qgdOd>)Iu5T|oWe_COB_=P`&Gxk;aRpqNzD)!x#$<YKq|C*`JI@W3RCKvvUWjcSWkogw-jAr>5=`xiai&s<^B#4|k+c#Mp7C;a?04>}5I?qNVf(gt>I}DOm0?sx!ZZvc14h!nkdalh+E`}SuaVwz&URK3is&dUl%^qWsY2ebREIZ%aIH!iiVXka-~}2H>aRl1)hk0J4~s2_ntHZ!lPTrJGtGC5Rc31-W&t$HW>V8vdjV{tQ~D__CQfmvQI_*{9(9Rn)KHH;%dXjCwn@Xrh3qO&j8M_t2PGId?=ebY11Hg1A(RX7r-WTkfcZU!IH_57Mn@88rUFb*<E?;!3AyEjXKTy9)Qyjdo&q3#JrBVW<zS#o%D8qV>*&WTV6mf|Z%=L7o@D5U3xOPujjpm(_z^uS7G)A5K6+MYvJQl<?)9;oFpYhi5Mk22bgx*hS9q&R!(YbGt@QMQD2A>$xiP9^GL>lPjJOIoQ{KyMQv*^<&@sv#=KkBW4_y<D%Mm!c_7qEizRRGF2&>GaOir350S%!`j*On4TP)|Gr{_2+zu2#uqwERbxv(13h|@%@vnoILh%b!&t)VjsSsJ!CiR*?*WD}8a&g8;#vBzK+dE+Sh)><ao#>Zgm$H4YPMwF*JT$j(QrpoOLER$18m>Ui9hhh1elG{ApBTyPvv=HzrlDRQ&mo*W}!;T8N8h50BSS3ovC|w$&22QWN6uFv4Gnh<OPoX4BAyP{Sm!*<v;qp2VMHZlXS&Ae;)nQd9M~Y<+?tXx4N%P77yZzbH_duwf2N71tco{<m?nh|vDI*)pgDsTxNilw#-P2EHI0Shp4(VHyXobZXRSGEvIDrWAUFn1|b2FK5|L)gBx0V;8pzsk^R9$*axMoxi^vy5Wpvk^rXilk<+$kUeAy7`%t?Ak%1OikDl)R<Ra#ul)-O?{jFqXBR>eFyeB?p&!OrJcSPbFQBs5`YLKCwsoqF!5SFOh1X7#e-Ir+>}iS#|)*rSjP1KN08FHP`>`D2;|lVxDvodIWHhxe%!QF~O8xlkvL*05}sqbr+@3Sg~m*uol-26kw^N#B$7n4n`Jr4n=uRuG!2O+7&<Y`lug6p86WL7$%lsbF|ny7kw;I^dTg$6J8d{&;X=W0$){@MHa~Q-mI=im;lyT$g$*NDX$(Nv518yNkz0Zg_%Zl+QDvwa8-64G7L(@)<2vn=(pbHvqq^|pdr$_zdF*IQHQWn<>N<g#v?ed!&+izhr#tlVObQ6d*zS@iXHf0UfoNqj988hwff<&=|+3;G=FRSDt~JWbErXKVd2mW#<fG+-6r*$%uU-Mq@%aH4~UnP%_$ps7MYbMP|WGT!GYJ}mMTgDHV#_<$~LPyTiy#9hG&$)$wkgsTd_r{+^B#K^W<Tb*P^D~0aoShdwAL|uQt!PQH!fFiicKi_92<u(x)$E5&*6{hcmo-?4N4EE8Ct=uxA}Z=wh+*0eK=y01)1%KE1IpeMlw%6N*m|MU++`n;~Nb-7I|fxl)UY@!ifL*A6f*W|48>%t}U6(YbN%{4tRw!Ko_MiKE7WB#CH@P&sE3kz;Vxo=_Y+$0Q6)L!=1+A?3&1LY_>Zm#r0}L@r_Vf&@j5J*3|N^$5@XXS{lD!wG3HO9ci$=2M4JCNPbY{m~HwF|ps?Nlx1q*Jj{c=V!GBDGDsXr=k~0kC7Leo~<e3lmbeZFAd*n*lNKEI5@am$TepH_dkNL)%8^3`7W|kMw;XZNk)W5QH|Sp4mj6SM}<?ldC(ax!#JuAdp9B<M_9T(G3^$lSyS7o(c*n*9<PS-@r<I^7C@4wJ8sWoxz$SF(%P~rtEVt?zPw051HlB0@92ij=j1|GwnR$<jT#s(hm!6e16?}G{hTPDl7|R4G-Sf4W3J-BQo;|N^C;xE*;HVh@6CTUhVDqwPFNkxt-sW9%Os<5o`yGW05?rndJ&qVZ}XT&Rod#w7IhX2;e#lF@@$sZH-6L9$>hU(v?5@xT?^B=>Kt7%l`2;&X`k{#!Q&W{j<*%XZ4xXBby~U+qOwLU>u3L<nne=C?aaX)6IvsoMWiwU8H1xh3I39V?7B2U*J*pM|D}1FzouMOo8BnOsxLr+{1O#Keu%}C+X5T*%t<ai-R3;&TyUHR&~5D!VK7Py^)ci*LEhh2zyBb=&hf>^5No&1312@dLz3cJbA8EqO;oyE7|6TZ-oqb~RQPoP+|+qftBDlm6z#gEZ{(0;9V3kjK<Huh``{UDqEqm$hP3plW2@5v^8C2iPIUUBO&eEq6S*hW7imY1dIC{a!|te{qqxx$H(6<L^4+ApoTe%X!9lI{Ng|UFD^T}QhLS5VS_y4$NPr)+Or!!9uZ9!2$z^#`74lu+oa{-R6B>qERvlnOVIbk&oS}?o4&1l2?722fCYA+Ank8PNs0PynytjeZK_xE&e8e5fT?Fdl$m%H>%)?<grZnnjJjPV?vr_k0km{5tWx6=g^);bVEh_swYwGj~hFCvxILZ5VSD8$N_n{Hfc8QS5uXaG>PRm@^?s|#DFn|9cP`mG`P0?qj=};j|g3)t|Y2FiUAVgTi7n;&%e0rdD&!C>+Qvmh~yCAl5Kmh1Mo8&o%rbQ<pijB;Cv|GVybf}mhf3Ioof%|eFDSH0x<vM>VQJRc9TT53PZ(U?UHiqU3Hc$_jq}v7>n(8w5i7s>3jl%Ih<Q^2V{5s1fE62%NsDa!MW>2U~_(DDiyP4vceN<qCL?hvj)|kNFE@2=;jxTS>E}qIB;g9I9Xte!J{I;(NK013fY+6htca`tOeRnpQ5;a{aN@GAhP$jr1AzqLQ9LU6YOv^DoH;bGMxZ@kvA@Ilei<bdEfUlUQ5$0#8>nI!647EQl9Al6s-x2@puPNZ-c{k7h;zKPiZ%o2)CZ^Yj|4d;~kTU{Y3K;z>qgJ@66xK!rMv9dm$V9%P!nn$%+n_OSc9J8XMOvq~%MEn7)<=1&*NxOc)-6=Mq##qkHE7mJZy=lifC&Ex<77j07<CPc%OCGSr`v~Lo(za9TpdIC68JlO8s=?~Cy2K+Y_kOpjF68DTTJb1zm2jBNzon2Mn!1h+sYmo?UeBS9#Y8oXa)GPc#(Y$oMX710bNvqrTKjrm~=8L)=iJ?KvVj4;oJXf6a4lINe|)}aR6T1Y9a+9A#*tyI{6~}<8oeS%Zo11UZspXnJWndSs>q$+}5z$Cp8d<1Oo(0x<Vebg1{PVI_8QhXC+J&lQ?y)*4|k<dKVJ!qDpD<LR5@DZrS2!GDT4~qlz%zV<^kkM-j71OVVbIzJKmNzCGB&MhopU8^@1@g>WbUFW;X~Sj^pbHlryMZeG=*HnkD+jhFh^HXWnv;QOU4q1SVEM$b$J!|9k;1YL_yU1(D=$AtUPFwZ3$BXNX~uuvrv{XB%!^Vn;~uF!VosILYbR5cI%F!jt7X%BVXW&Z>Nx2|TXhhxr#l5&DAzM*Tz*wB}pS8niaZ8{Aia!IMccDci-Fu&(1nngXJpejU+88{%|Taj@Cg!pyep9Rmn=Br3^W8zdL%kUIqmJzyrg_Q6yuraA_Hu+(CKuZd<gG|Pxqo-QS9tDD$%P^^k?jXBF{1#uYWa@z*g$FR|Uw{x7TcYE6^0>34nTfDj^_)S8cu@(Ze}agDh^xa~UbX(^GUQq@90T1b{^V%KKn9cb_eD&7zRSN1ORwe!C_G?u{)%)*O0*TcyvwkvRslC<os&)9B~n=iM{kqyha}AxcJl$ym#$g@4%6NA?uoo|i0F0h)#0}#QvRsXyCZOkuF^R4sp!elkH9U{aq{>Q_hK~7+{eD?jCN45juH~EsOgTSVc4L8P2{>Ub<AgDs2Z*NoLP69MYl`_zza~G-7mdZMc=1n8r$SS9`6<pDnQtzh&dcV@DR9sV@=4R1y!qvmmTD_l&P34L`@;fxTG5_S!hc2Hy?h^9_Q9y;aXh5iA;16(aZ(29bi_;*>F^3i6*(};d_kglC)PT;hL6TozKzlPu3wYzKfbi@S24vwcXjBLk@14hK?!&(%i_JI*Z<o{U~yprt!&iA7qwr+G^|!g&-tuo%Hg$=b4)(F}?RNFqOR%y)#<sj{P`n#a9!2%QXMjC-^SS&`YDZ+@k4(KC$P~eN0f+VT8L6zlw>-h}B6V9w}VCH_ECmFVFCeLFR8-WIWl2k|g_hS2X9~vWbbmyWv=MB;3_AgP?#QJ?Y{aw1zeb;m5Nv)28o~ToMP!DfBc00#^a%$EOogb1=+biWCFP10~`zDwb$QbHwDqV_hH15~I^ddTbs$<%Vpx1j?g9iP<PS!xx=6L~|Dbeh)oLCr(D=*LjR*NosJO^>!HSd8Y_oIePOWQ_4TaFDMZq%R*9iz{j;AF#I7&)pI{bUY~*~F_O`)P9MJb@CdcJg)=sq7yVG7cf>rL9sW6&-O#PUDvKXOv54SF6zO9bs?mwF=dF)h9i#?ygA{~{YNmkaKN`X<kmS)4@{F7}h+5@-G-0F4pl4C3b`J!r(xgH#%N|2;o7-7lZaBM`1aqoMfo&ZvMKA>OQYM*rnJ%k9Bo%aQxQR&FZk4%HXgQEKCzMb@i!NXKB8ww_NH&Xb3_IB;Ze!U}*F@v3o_LA=-RC_NyI+<P#^ubAG90c_83h&$37Ubkvg+Bb*L)RMsr;Oa>0tz5ObGeEO}626_(&C-)cM(<E3RIQVOA{e@7BGe=z`$OBJmqv!t7xfY_G-joA>Mg=eLiUPLvdR$&ey{6({o2^sGx+xLCktNeIOVQJr0VPeT22{$NP*2(3g5qI6q&XAE363P+@cAGR)Syx#O&URj>E1j##1ynzS*{G`v?3XJ0EBu>k)Rr$3KwGp0dB&Flsx5XZ)hkGAu_QB%V9fD|)VfKsr55qsz$D6g9TV~kD8>4r2z`rSG6D(8|MKgsTQXKfm=tA62?%Ymxd!`Z+EX{2N)}i()g5X42Kz$O>H-&|{%`v3-G#yh6izSRuJ}U5YH3uoh-js#cVe2wOf(IfT)YOR2QxrlOSv<`6#6OAePIH6gA3M~vruMFt;G#5$#bX#~iWE5+XP|8*;nIfm<8$ezR6g6=lJM4DZAGR`e92aXR^oK+H3dcoUFLm%v@3sn`|YPczL_6>v@QGgXjgxG|MlDN=I7CK1s(T;4CVSw^Nby9zC=km+eg6Ou-1DzM`53NgqRi#g#QBbl@d0gU0b*d&#(BV5-Qm>vtJO0%KJjJYZw35zy0PSfB*CUzqxN&jwLyc{UI#6o?W#Zi7=98LmrtpG_0=aOZ4w|IH+oLWq7!IWaCI$4F;zH<TElJ9`3{KU%z^og%F+Bmh^H!ILupx3YJkVd{_YX&%fF*cSma`;RHoH^&E}<`;QM7O~K$m$4o|7RP~QP`z9nEVlAB5Suxxz_rtKr(Es25`PX0n^k2XK<=_4po`^WG$2E&Tb{e_{2V??nhGllGz}Hoee-ZO9TKN8O&(iei(2$aYv7Sc%*nUs`Ev{+v9dM@<868O5GkuUVZTs{JhzS2A8au|b!_xNU*U`i0v(%XG$<r?S1hhlLyd2k+ckCNn2G%Hf!~U?&J^66uCwpwAS4_juF!sVLfliji>A}b`(C>}+WPP!608=n@p^m@%qG(<Y^{c-5E&FY*_RtRUt~e))Wawi^wfyq;zy9r)Uk`ivINkTL+^6D07$_xL+{e4>_fFm-qK2Y=f`Q)w)^@nhw)AJszbaT_G^c3jG}an9UH8S#B=P}4$HrphgUjwGIAccra1Xvbn$~ZudxXcRBvYx$H;@l4VObj*4pCEtisFJJk4k3ktMC1}UJY9)rLe<}Zql_E(dl*7%=4&iejN|8Au<RNiiA6tQaQ(@v956rIFdPgb2sG^^CjV$+lpm=Xh;UF>9cQf!<28s{(|&Z3OF{%Gvos8!}o(Y=$$(L?5nC<-&>R)BxfFFTM_P9l>_G((kjv#R9q?uQ$Fb#d;^=vnC3dx;70!AFYoXFA$61=H{~ws4iS}%s^sUAfBtdee3V72&J@Y+2NMM~G1=}IC)OTK=Hgw|9>?3we`sSm4;;Wuz~+VI*<-AOOY&qT^&V<8k9BN6Z9c!p=nA?&g_o9NLY!b}Y|6ng5_!(x!O;*vS5a*m_)+6cg~G9;PoT{3Ka)zLpKKfl=}(g`mu6v+$b{H}ES*0#<yr*B5A_zxCgAlEAAei{w$X1TQX3$h$7(~DWZ~FQzJPK7KPQ)MOHBkD*)fhqJY;mKDZaQ2czvAS_4^WF<M+B?W5XE&k~%~TRCr*FJuebFM#JCwGG1kBjNBB_13{jR!w6UJza+wywU>CbQ-REF!LX5t$@?}3VpLf}lnGHOE58bAYoZ>bmA!jR{#T_lbC#Kx7Wyr_F2|hqo|fKdhPA&*V$X3JdPWhwOOW1ffyUsEPj0UVXB?Ls3}n7tj4Ir1><&$Zninn7$<_|$ogZWApaExhh}I2RJ)m(&rh8upC<tpI2)Q+$a!=QDU|U(34jle0^VGVuP!crpou>V@tW?F<jemU}+~VBFyNxULF{c;+{jjNj{_*1<?=qcoK6>-$&V|!Y@~>c<$w!S&Gc;(yH)c8KHT_S_i_j&fk=R^9m~$PFo^Ch-76XG_E7-FNX=0&chX5>(QEo0)jf=+6juaLnKvCY$u`SrgKhT+L!l4{KCFX#Bfc_FlS8r9bk6$-taOg$e&1EoroG|oU;^s~L0K2d~WOfI#_I$t>gG82=79aokX}e{a_rneTVwV40A2zWSH1{1dmF9pk4I>%@Cb0pT6I(AkEwrV_Z@sxFJR}Db9R@zF=y8Wze(ZX`7R<N~ZW%K|C;-ly?Sug6G+&tY&ru@yz<Dtc<ILmBv=O5TUj=`%FcJw+X6i|THEre$RDfJ@mJ3o$FJ+R(-*@a!se39jWN&Fn<utqNS}3rQR<HQN8%iD)5mTN4A(f&Agcy_MpnPS4>c1Wrd7T?j_KPz+H>^><k3RV$e1+`AE#F;Woob3AU1ZOz&R&tdyZi5>$rbjDLgO`}_L_HWT9cS)wbKPW93|V;&ah&=+FxzN$kZh3mPu}*NZJ@%UEy+lj(WS5HY7T`vYu@7`~x$XCUV?O*~Zs(sv$6*-MO5s!1Y}s)kB(Bd`E#xvuGe~%#`U2DN1`Ha}O32-3tD%`F<F^3!~C6)+y`zPoi!a9qrx^r%?|O3c_=ml`!_*)<IJB!445gxS8p(n{K`QL$RX(*57@=q-H>$8X>livOW`tO+0L7E~HSp<<o8Hv$6n(p$soARaKSO+G)u8C#ZUo2$%E=(F>QI6G^f`bjMiUA?L~oW?;JcUXD7gAc%DEDTYCxhVfN{zJ9MApBjh|z$?XQka8G-HytKm&G>`^o{u@)?I!@xUonWJr$84^W5XOkkh>u9$GA|`^H9!q9OK<-eqnNqrk$zft|{mH%Z=n%!0)2BGx{ix5IyCeFE9qTqb&e0NM3-oWzh6xJhBavDMErU*_SIws7?pNW*q}uIuZ_))yZD7;!&JNSK|RhNxbtcr)zMYpK0l6K>9XD(#(aQrq#AS3LfzKgE%SdCCHejrN&V(ZgJ6V=?&c33(2VBj;U@nwn+x)@RThHD(8IjKZiEoT%<na-ik~ctUTga^J7?3PxtB<kTdZ-p)61waG?#Fbh$s~vUCxl$4C@Vc!8#fQju(Gz!(niIS6`{T{qIv(ONZJ&x*#JvHZ(N6Y;nEg{^#f8(2bIUQWK==-;TtHOUX+Qafk^UXrH32t?UxP{&?~Wu|3*1;v`KDN8@0k2=r);tPk^Oz#>KC0Fu%j+U)4NMEze+TGK9GUhgrFpS1>fD^fYSC4Q3<?FY(NiX601hnvw_zqQ5&4EPn8$GjiaPyJT8HwGnIR@9s*zG1O?{y9ECUn43Qyz!UxD$%hO^FMKAZE=XxsAZn+6NEgUE!3(l1@KQS;d>(AYZJW+Fa0zxyr^^7V$iTT5_(MN8!K0WP;J$U!+Ium6wC?UDz4ML#EUD;r*=By4jIm7YBci=4c^wt{c~iJY4t<Ce?eQy^y5nL1u2&zo+|DXJ2PEum~sqN+GjQ!IS?wqtceiO1b_l%}BX3s9=<?%$(-9!RQG5eO0~^Z%HP%6z$4gWm^2s!c&0!dVDRkTV{i|o9!&q!vA$hp#H#)XEE`(N#)60gL(W(NP%fv3fM)5G{&qljryBeg(ChG316}#++Nr8J{D~CD;exgGG_#?%h$W)xM)U-siB-w_7cALD2+fdBeoEtBOh??i34|GLaYqm4`vfya<2nt+J{OHlMX@4o%c%gAgey@imAfW(-XcJ1o)^GQANJyyigZ&zjx%_fS1#^i(n0zZo=n;W}p^vOlB+HZkRG+n@O!);M#u1D9@JKX~yfBsmh$bYlAq8XO*O!5HgVJQi`8BXaBibE8EF6+sOGgxDqZNI+H;@>2Ih=C&e2WPQW$%ThG}}PMQ%NtCg}V=teL{y;Le?t<=KIx7o&uaU2E>6a6Qm=E2T4CBufTh?}84;{;}QNWS{a{T*YqNfwAfh~8Q$VSTj}z)mKK?779uIdK9?eSTk{Fl+WR)LPHH+*p?nxmiaiQs=&dfYKT~gE^h|pz_+lLHzJ_$1+X=@LK_z`55BprrsHgNMZ}~6kqGPfPona=YpFXE7{bASM^&1>VH2EfeiYf!|Es=Q|p+=DqyiyBDkl_9#1m#(v7H&CxNf>QTP!(;?{XIqCI+6Xig8rvFY`Rn=lT2o1g&fSq|7l9yoMUb3;4EfV%Ybf{2E$IJq&dV=~Ta=!|a)I8)in9n%6<v(quk9To)IvkzSpkAe|6yYUoT*u=}Aj@W9R2Afl~%H1hZSW(6)XOuh&+{d8D*Qg|avR^f++zLnw#&{Spv6#hI=X1|cNkbF8Gq*Z7ByARb4ihjXLcpAVhUZg{!LIhkQ6O=&Ote9fA@GlZ?S*V8PjsX%UshtZJ24p3@;u8#smLzMnl?qAz1;3F&qbwplY@<UyR1FZ9=59cdX$g(VYQePRq9ki2~Mwlp6wzb&1Nz&JcmiF1g@PW@|P-|$>mLuj4VLSvJ^$EZ9;}ljugutbn4&I{-1~a*?X$X;pXBS9(_6t<(Ad2F=NM?6RNi+Q3(qht^$xo4S@*k-D!#ma|@Z{{O&A;#;wf7N8uMNPp0)+xMs8<o0T+@$-ZF(%)E?t(}0POKsn8{9vXvqgtIW1Xy;|J8w_fsj(KXIajThin`ZvURC-x9g`A}NZcoEkLc$x9rN`8`2mHSgO)d9Y!*n7;DM73}wZTCD;l_WVvBBccVS*(wpYXaH*kh{!12#pa5lMq&k9H{z6u@{@`chM5gOQDW?Lr>o2ZYQR;Zn_ETvuDc^EtVhK}l_MNpU*4bG6pI#w_z`F+s@<5V)PletFDccdFD9Z^%wjg$0M$o2=}9br|m|2?azBT1N#xNXTPkd=IQB^ZX|_0PZ>FGV2GI;g?P2OB8lwiQfiGD|~<~!*Aw*BQb)T=grr2qpe8Zn?L-lH-D4aB9TH}c@dfsq|k1k(fuZK6*gGB?rm-Y>I(CgB*-(1%#yGuI!N%mAdX6tvU36C3Ob+WZE}TxvKLb35h?9XiV=vmVpB;gRVsuTL0Qkr6vx2;*FKey>kt5jR*)H()Fjn5oq5~q`L?R}1pN?}O_a9!JlXr$rx7G`A7r>N8}dTK``n7!GFY6Ub%U=1S66TWep`yu+?Nh)ALhqM(Tz@m#!;)lDT{L=Yk@q{DjO+Gagl(~pNVRz=h_=m;<iSa3QU8CCxtHiE-CeZ>Mb}xz`B{FsqU2#Ion+}?Su4c<|8x4uoR0<nokN_b!5dBgGDsP(#3iz3mo$%HsYLbNg8vbd$-)CR~5r3D5Su`z&{$in598t0}N(?Tp<S5->f;hNaVF6-JW4hjig`|fBQ$IayRC++Rhj0lOYZBstBFsESFoYe}?KA^84<S@5$(4x$WJETO3#TvZ1sy$nWU`y&?Ck#&R5@L6S@M!Yko6u?BY=Qg;qr2~sm6)R;9dJ|ntwh$TZ8{x-DSweAI~T#YP_VVzB+nyt5OIwvQ2r3z?k8q+XPHf1_L2D)}sQaRx_r9Uu?i{u_yhFXb$<#3-GdQtizhIZfqdGsa4c)la2I#TS(GHjJxF;2B}69*hbUra+z_?*W$xavVK_RX>=3?Do71fdw8n!0i9WFFzoA_^fG*CKS#@q_A3Zn4XYw1x7iLUD}JhXR_4BA022=c$n`uYlJ;SD;iX$S)X=wl(|d<HFsQavf4jfV`|KXoEjwfo3i}n#;Jo2F-7t=ATnvTC^B^2|tq8l&IRbS^fB2;K24b+O?w3IZr-!73VEWyH1qOx(iPl&I>(F1&Z{(f;$TVICS$E;?iw%<a<cP9^_Ah00|8LUMNkaxD7{%JkMCt$nhBF<`(-Xct`DVQI+LNK6H#!m7dTunm6P!R70nx*dnREONUhU=F%LrSm@lRZu&{oz2lx(UtFymb<a^drZd@P4OqKuq?kiK9Gv{LTwrH9W+@N>;{a*HBwe>|Brjs@-;#nXbvNhrMM=ANgDtNo9qt7KXWnDJ`&b)_h>*K=1_{~KOJAvZuk~Iru^&L!YLS_gg3Ik#+vVmmmH=kb4&@<&`bc!PoZR5$DP9Ku)NABKKR<1MooE^BOe`1oboqAT?PFlGOH9pLyK<Tl)|Dt{{n-D-rWD}aG{pK{f>H9L9q_T!crW+vs)|KE{rC_l+0#-LdvTgh0m2)mURKQXT!7;{Y6DDky>aK7b^^hpsBEB`5k6_?)o@fZmWC%Eo~6f-&?6X6)cL7G)lN61&0QUM%W88GG31iiDc?c2jvhjBtW%#jDR*Ef8119llyG&k`L_7PbCzJONisv5*1_G7&&88$Qz*(r3kxF(8k6;s84_b99e;AHd5`6sX=uH!&FzskPSrxmdM{8n#j6w(Hzp5aa*xQaZ8m#gxpYy+M`nOSaDgP2j#8Z498yfdO~;rku8FdG`~4=I8U8|6it$uMUeeaC=YR*>;8rNHacL6+82OImXa8OT^__R~{4YM#=JM)(>oawFS5!d`Kc^i>a{*BFuZ+6+qWiTpG7wgT`9x>^Gb&zpyObz8tEMES@KrQSnu8b@zUj2qo25vm{=P{aISRl8v|M4G{0_7c09vSIfWtv?OjH&-!JJfuCzCE{yYEvSF#8hZJA4}E?PgC9Z>j9l1P+Xm#gaXW@wMLu+qI-<gJP!}wD4{135<3u_<m1`SA4Vt0!lCPX@Sz=b_Rf|Mo6>bFktB<AzL;-<^x^L*M)EYuT6``FD&ZxW5lA%U|R|)6ALNId4tIp@|WB7u&vHdPWyN&?qn^I?q!Xh=eY2Yc)QCEnbH6gb_EbX`Px~~I{KTt`H&&1M^mt9Oi_?{qj30pXW8c6$Z?xmfyI?yLMj5}D+Kh`krAR24B3-vOJ1wE+hxaS(=fmP-T(aYWKkO>qSN>sACqNiC?0L!HmUPdyK!QsV<niq3bt%+3*;NGwz2IyM%h8UN$Cc!=kJWo86SPptM2av&+1$eEc@&m7|68Ili^e(<x*{FOwSs1U-qS9R%pMlY8C<K(M@u9PLZ?UExYaIV1UxqEP0U8<a_Opa-Ju?qxXtYp$|N-7vWpk;OEVJ$P@EkD!M>w;QLlKQKkTgs5ud%1r7-KmNH_1fqL2ZSAi?v^A#bv2ael%dx@vX(8u%=i0f@AiUo~%C@=UIVFr<@0=(sZgfq=N!!)Lfb;qKNE-qPQpe*%rry<<94sZOt)d1~@L1-i$YHUj&?^dhp3J-F<t-W0CAWM#|#>=sJhmPW7dUy9!;zpKpjuc6TEPdRr;1{n=6F$R_kqne<e2SrSiOuLdF^`MB7c!j^nVH-fsHshp(2|vQWVVsqkm1%RdSokgfk)lPJiFGQG~=PqrKjB`3~ev^qS#PJUrU4BAtqdwd)pQIfH3f>vc^p8IQE;01`P+t-F;bRe?N+8&=3MY-xuy?0!KRcJkMz8CcJ}TDG1SsB8Z|_28j&YcYX^H{bT%Vxsi;8CRFh3>2vY8>b<zDQ&;HQpz$iR17I%J927^fnA+xtY8nS*3ELGTwF`0EI_xiInK1^48n^b{QPlikV-8WBbsS#IeZc1N1kN81)C+p>S#Imxm~k{S98be>DFTCGwX+xO<IJ5w5$HJmAINItv3Z&=UK@SK7Lb(x%0cTYbblfB?AC@lBTvUD$`*@5VCEWuN-uH!_Qb~^5+dVjLve`k0yTVw-r-!xhdfNh-3Jj}fhMpLDzY|djn`|W@xf8+xcNI`*ZTmt1iegv|It7~(cH!;`|BAjs?^yI=7G{bm8b&EXj1L?JUq(_^%}rK$P(9S=+yLxh;o$Bfr@o1d*C<DwI1cv#i`xHa?l9_FvZ25!!(kvnkK(#0Q;ULMoErw`>50^kMSFVAIP|nq!MsjV~7VoWXYWE=g60rU>J-Vu&W<}mIvSoYD4EUN|;vvOre(~Jdqu~H|Op5t-;+EgM|F^;!!j?AFVg!8fZ>iA2~CKhJAx1f<JXZypX@)%>mgAFJsIYHANiin>=Hu=37DUn28cWFdoeYifL9ZObp+abAE%ZOId<*v;CtirKuw`k2YN@T~>p(M&R0A;0n1WbB%$QhoDpn4vTQxSlVN_vn@jQVOcFg7Mf&~IAWG9^-}0h^ph;=-%~1TvqxZ^WeCnJDZ>*wwL4(Jp5l8SdN`l6x%>I8@A*oXV)Cp@XaIv+gRAZ&^<4~g#uABchuQNIt=?|8n9I9<^Kpaz_3dM(Bc%gfD|Dbgiw$&bpt|73aO%3)(*K#LJXQy+I(W&Hy1dG&zQrI>ZH|^Vf{FbHwkM)7;unt(!(U~m`!ChKdzgM8M{On_C3?x(eqO(0p;WxUv=d0e^P@s!{itmOrQz+B?5<dv&lR}emR<^ToG}oc@Pg$-7Us63Q3Ri+&nZgC3-d@BJLeav&v_S+j8lh*#^_2;pS###T#jL&DdKg<)(XrtX7ny#=Rf`~7mbgGYYB&Tp=Quqk+I_Bu@#{yabI#pgKQGJzVFY6{<j~0`{lPE;ls}df8Q=#FYmwp_<Q&~vZe6pKN`2M-wZbPSo2kd#t}Wr4D9*nUS2r(1|ck+Hn`+@;45WpLc6wb7hYfS%_V<`YZkvCuYLA~Y1h8W_te&fi~ReqABKPZ>R}clE*?DkWtVc8w+f#f>+{TwP6)S$hMO~5Gg;Rw+NtM)-oO9&sPF*NGW)QMt~lBsfA&ofB*&T*v9n^h*ACNRk-@{i{qwKC{^`Gd|I5GqGdvM-V2^7Sf9y1LP2t_Fa1YDuT7j>t9{(cdin2Pf!aYlq7(>G{3dVXG{bTz*F_pNc&3C|^Qp7nRcgEPZ&*aI|D}Y13<InG~o^<(Xde;0#dD9zt+BAc$@Vq7siDX<x-UeuNNLr)hU4X+n_hg%tTkPSbu7$**AsK`>039T&A(*w+qTd_O<@#b?4yFU>LLGniMSYnZN>hE}TVlSPt+^fKUD06`d0od4_W$ztzy9r)Uk~&6INkTL41V?thm@@)?&DoayChE!p*L4Q!HRbP%QiH8bWA0y=1vtXF`82}beS(jW8dMv*jX(;An3<fWI=G*{bbuS@$khP_;O%cH?i&j9;4d*95JO^&xe-KRt*iknW-~D@p!R0JG1uH_x@b3hRBT4<zT-y=>Uo7&$__WdDOPa#zsP-CRVpcfp6zhDqooNZ8XjSM-XOj?xtK|z9d|*QW4+|4Ret-efBMGnDTAdU(oVEE|^seaTaJFzQ06D@6_>U$4aUtuIv1h%6Y?XbQxl?zFZ9wimbD=NHxEZnT5;5be|!o4<-^JM)(Dez(OPi*OU?c`XOkGm;jnL!Zv$4rkR|H?7<W~>VN#@{rx|_o{)WY#Sv_zX2CryX^Mb}A9J|(@nXhuk4xcG0dNhHrp8mQhuSAjPhe#wcbmTTxt|Pq)Y!{Kk2;0L*<B@nOkix-W<DG$f27dkqiJ|YYIO(3TQ9T*V2rI~JWly!hk3k>^(r$+CsM9~<eV5<i}|unV%Rk10r-06S2O;$V>q*N+`$5Yb1H2zuwBt7csvOtW16q*qNYNvE0qN;B2SM2N&KK(tZ3wf@@mrcTtB8VD+!DxY3C!b$UOb}DeCganV@HQbBlHS1?{r1jaLFjw`(zm5VTJ?uz}p70aO8sVs6In+<pn+p{@5Ecx(`W$5m_qH<Y7+6w$%$!BDDr`WQpdr9v}mR+%h7W&0d4f-&@Ot`JMu9z&hnn%oDG5tM;<95H}$TIud_nEmu&v`5c`0pZdu_^2Rd4iC7zoCiYXogyLxj5z-SEM^?xF_iWDsy^fQrW?kFhXqtJh=Qf40>$8wktoK8vW;3j^u;*dU|gSa03wi|El+ETQ@jAxIG=~nu771dUhb<zQ1r_PlgF?pTT=dFTWOufNBY<TpT}rrn<&$)RW-akUVmw!-?Hm+%xUlG9*>VPOH{C!_j44}&@+nYiv#bbm5>8}d~&;rI7zqMU{58!S8w**(WwCRpozzV_no=gQwO0oyF(N#!(8gdA)M}g&Bh?gfL$Q1@sxYIo&(#;LUG{mE3c1AcP4(yw7*u0VNMcjK>Pgb^WY*<J{)-u{cqPD!yPCOoBHP;KmPIl1pLD;$oc5aqdS*kUYz<+i;uX?d;Z`Xb2`=Y^gl5#U<=+=-e)eg_;BTno(4+-hz5gQEBNXP>!eOgWoaTXN;}2F<yWZG7>f~d9_DeuKK{{xuqJ%b;ZtG`=m+R8frVKM!gc(*F>Co*<lS5b!^a6j&qZP0)DN%=%Xux?3Jm81zSIlhiFy3A-4fgM;Rb)P8how~o7f77M30%Sc4b_&-a29xz`==LwqJ%lkKcN;vsyq{B{~dzTG8VUxBS@kepQum9bD{A#0`SX5!(rYN^QO{K|iB}t%LLOO6rSf6-E=j3OtA~5(zqV>PdpFi;bj1t~kpDDN>;_!RPNg_NUZ6l^L=eD{`9M)lXK^rf>$YV0mrMw^oM0Jg&kf;Lx;QMN(^DkBhv{P2<svGdnlzu0Riu@D<$KNUj(N&YJp0j>n}U^lvZh-Q9m5O;$PuO37<M9h=r9CR#0X(G!J|?P_P@W)d;8wtiI+8fm8{3EoT!7>^DxNv*yYF$~+Sv?0;im2hQS9|4%bG?C+O$~L~P8x2tz?9L&qwBT@Te3u5@&hm=yC~#>O4Wx~k#+#wuXisGBX@Eetg8ys2A4bF8s04y_%KHA35YeNfg8Sh#qXXbDJf~R+W8ZD@CsiNpkYj|KnI5~T0hxW21)qSs?_vDwh^S-+OP}Ea*a2nBX!WOJwx-)^Yuv}^mpub<H}r{}Zg(4L7$a8}r-MvhmYSVzzE|L5S=exUI+mwleANK1-)r}#1}79l77#t<`-0y<n6NbcdES$J%;9dE%(jXvxG+4ux_BBJHkrsGl?v4fek|E$P|Xe;<K1aIK3UjSH?zrIx%T~ZZDIq+q1}`y`i^h<Bcx5m0SaW!?Pv=?1rkTI-aVS`i$}IW{zM23W+!yT4E@%f>`pbZGG2h5H%wI4taucs(G}nTQ3Y>L&MADH=Vw|vx>Uc76gG7rrq#ASs+|7%gE%RyB5U4&2t~qW$pxXMH*oJ&C_1LP)iiz?0K!wsBq)~i&Ho(QtQ23q@{Onx9od&yIl-~!$FQazii0oUW8!&2Z6*&#U3v3Q9@AqkOBX$T>{kJ_j(|m>R8*Q8@Pflgk6M<5T{qIV(ONZh+lpVFHLJ--6EW-ig`j+Sn=*b}Ue1c&XcMW$H5qc^QajaoUc#k70@lMqAiW2z<hhjdE2z(OO<B4IebjmW7hluGrr_5YBB{L@rD(@<z*}RYzUG~=q@)>H(k#q?42>-TXLSEAYKguswI1Z}9gtgp&ZY%e#Fwd>tPNDd-{`BYLz!71`urT;!>XxKLDnD^zpeq^gbrY5+Qa)9i9$`mDRJr$NUK>Sx8HDD`v6wZF=j*M$tEL-6>oNf9f=MSNFn9oW6XIr#<GY98&qR+kwXfg)gAg%!)#b5(e2d&gaBCBTP4Ko4|j-DtWN7@$ASe+EGwaBAT-ypYsEw^Ofr+|-q3zYQsW>qR}X($Q=aZqoz#SN(?^KzSDKlH6P|k88M(HUh$=i_sYs93fPl)WF8DEC2}>gppS<3*Mi=u3^spS`T`L%TzlD-$EvFss(K6mu_Q>xp{L^3m3@)IBc*|aq?Pdo6wD^A=5~!)L>r_mpZc^t|hyeYJB;mFc@Qcuwp&kj(5AttjRhRfvB)GjNnZvzP6MkwK3YAra?>tH<P_%{NL^SSMyfO|hglXe4AUqg+c(7%wN|LGEhf4R44n4~~>q-(Qt3&NRjS{1<6h0V)#;6tPFZVU{abCU+crJZ=23Cw|=zONP=5y#<>E>bzIkHid%RZ<qT=ft6M8aotn%iktTs|aegwSzR1XTRYIoHpPSlKQePUn0ZT*@>LkH|od^fy%0+EQ7*HBkbZ&)H5+S`ZzXmGTMb)+a|8R-VO`+KTx$+u$yaq@ZD)Z`y1A+I&-*ur|pg{NU*oGm|1S&igr5n^u5a{}_9g63kb-kn+5ShjPAg&QCj4`F(Ejd{cT4u$i2t$YNzZ<WhB2eKEK&f-K$|(zA0q??L6EQ$c%pesmAh=fZ*Cn(=|n!|0~U8E-~n3-grR2a$z824*CP3+`#GMN?l~RbUNp`~5rwtIbl$YnBX3!P<;8(q<l1;<l$y9#1m#u8nAn2RK(zK>Uav;m<r8VH-UwG~)*1&-D7lO&Ev1O;GsqEN5$C2ONT>xgpwOP}>iSK$^qd;E5t^|I9HNB{e)_SOU&e_HxJg-fHhTM!CZTetY(zYhr-Zv9lXbv4t+Y4C;ua=1H<kR~URQ-;y}0D9)GDIUWV+W6<Mk<cUAoubNa&1n^NrARyu%F^i?n=W=pqsJz;lNt_#6GK(;V$x;*Tan88H6RO8xS9{|q6gXNY+LFgG^vA&VLRyojHBy%^D~Z~@6f9#i&oaR&vVyV(O|fGyH!REzeU}8cnXF^X+hq-b_OMk|)+0I0539u;`0faWI9~fa+a)oYsbmtT4tG`w9y?3yE)}$t%bQ>kS%8{lDT-)Wd_mcfV%dXERdbrsf7qX`d=HEQxQMVMHKVTkKaSAeQwt832U{pcX&ws$6s3@0L+6B?tx2>h`3+N*O;x>eSEE#!c+x7(@BUI~9m_%#6h6YTXvzaAg^A!~)2Y2-G|jw>c9VjMT|gPwv<w?l4hRFmnPL-^=e$gIi$jfuF)vLpHZ(Kk0?SWJFE6H0JyzfCX*o-1b7Qjim>T!s|2Lw+<z8#qPSlbmXqKmDSlhvI&T+|gCaCaZf?EMy6TK4y>uj}vz_zS3qH2)y(Ne{M0@$!hziLuzFf!HbW6OQH+I4_A>D?^TA44AddaM}ylfh8D2({*;ugXU^(!2#<gyb;*sK|j5Jtnf+BHz!6@eDR>KUD;q#T@gs7I9=*bBi}io+KB%)s!#R-9b1=WG1@~70w`H>z~dP^!GmJb5{vWAPLdBjXtQDv3;<D-t(W_&XLdBwP84PQwkdes9A}i!59l~E2{;W)q+TZ;rfeP@TpFNve70p&$}9amUp#P^vIB>v2wTqBg3J6T%-F<=9Fy^=Fr==29zh}Eh(jB_LrsWQDm0joPm#$rtjwh9vbwt&D-RPBxUcR%s5kur4&sPZN;Y2o2sY`bH}ps8R5X`02k+_dwR$&Z?q+ji7l?jhApk!gy4(E)Yd+6nCl#w^M<pYCc{p(w`|__deXV-21195rPNJiDPa7acf~OxAk3gBms7_=zpB(452rBp>0QaJAlU<$Cwzg7Vr~%s6!2>3HYIyRl|oEDFXAWeO9yHfbJwJ}Wha^GD6b@j?3l<}AVReY!m1OX$o#1jmFG+p-38Z?QCX29{V%Y09#R~}<h!K1d^qmas*_0o?56x@Ud`AgeFi8zWHAk6^GiEONIO_5+WBKX%WbfENOe|U9YHF3Yz1ter)tw>893MJRrNax_bTwA_|?#3<TK4MFD06jIo#53*3VsJPX(vT;3#q<U0y}jU#)Qyao&yjuC}L1dfW)5g@T=AS^ni#>xQG6o!k!igqbo5TyA?e#vaFqzBDfF^P?Hwtb7b{JWJEx5S@9(_Zv$yMT@N4>sZ!zp-<$}QZ&0~u5y~PkiY}62=;Yk6(-=?B>BQcE5jGs7H9~;us4(>{}|}nQPStc_LSwrxU-V7Vi{`n5|-kA3T#mdBW8zzU4At9#hgGX<s8Gdr?PZfJz9pXl3d4mC*GU^JTzaK#W0bd^B4zLit5GYaux>RgIMYa{>obC267xbDR+1umIB|#wFu3r$<ZZKS-atqpbu3_SLEl8M}azDvYZpTD|J95p8>giRWJd6$bvatx`LN+d#xEHzH>jJPPH_RLX_{`K>XyjDGKl~t0<of9QYtdyXN#c=gDU`<IHwxpOcApar%jmAx{Nb{k}5&2l;UhwmpWpblV*HOi+Q45_?$cbWQg{i7Q2WIBM^CCXMn0Cpo-j+T1cCMKh^g_oRGsx+gq#RSRNe64o>uUoo!j<`4>=gPtn|AI)58li=|@v)O-hI(ALple(?kt?3JGmDlSO=f*VJlMP0qDYuc$4*6biU($4VDZAB7qoBy=^%GeP4Q3|gF-j?_0>cAo!zIPNrfw*e-g72#ZV~Q2*oQ(g<TTIFAiI6(^EU6bHbJH=1(<*>-W^psXo9uRfiE|gTnCWecF0^2*hwPl=49xen*o+(@b9$7H}q2<_ZL2vu}&Iv@oSgXhabKtoLOd<^PF`d=8QP3fmY7?vHy$Be!&~3h?T!YvE)Zp<Yi#`rgK`W&5RMV=r(TNZedOeQs6M(yUQ9DKl|fDpqB2HUvi%zf0LT-7sBPImK(FB7g|iRY`8WPJjuH36;L&N-M}tk2PG!*xucPfy6Nx{l&b2jQX3-XFQ0(ap=jEH;Nm|9huoHUcg{~03WSuh%xsh$umhN1t<@$$W56o0pMJyz?w9H+1<g{+I`v5ybLW&I=M=uFl=EJF!b?^)vo%tMpbnw)JjN@%fG6p<P|b=D4tz>gwC#x!Oeubp+UHdwm&s}8UDR`?%10<3s>0cAPZhKq<UHOB+;Q;|#jKr4#45!z$cAk;k*Ub?koI^N&`A)I$*DaiA)$a&X}~78W8#o4Agu?;u%<bo`%SoZ{F$ww9Kcr~fk7sD;bB<rgKeWLtoyiBj1igU9_5#$(Z->SQM6po3aAd9Ct3buq$ObGX?V{6;(KZy4eJ7Yp6at+dRL5W&MMhCAg+{*{?$3{SEa<|zPu*t=g@Riv9aKoto3Bh(+l`Bs?vA6+%MyOoW1)h>?e(YY2t+|o{TRwM#9?Ju_Bw)2c_U$K-L)6$?rBD0XhqRgpu08<mg=j5<cEVTjWPx(iWU1shVRsDR#biO_MU44&Ff7fem~}Bbg?<kE5N~2HTyd_@81AD}0CAN-r4gSa82l;EX-Hgs4m|@@a2Op^?+o+d6}CRl28DC>TjvSGka%-28AI&>LL$sr|pUJQcsN)HaS03)tYc6cS+;ZkkiglP}~imz%bvP>roFazR_hDvo}w#6|lrdh!_CT{dHt2AI&SfY8^M8-(W7H#3`$0;K9>1(V2RWUE$k?<}ak8&w-qAl6Q%%`BM)SpV{K>4?fv9iQw?j@`et1KtMaX=wfX@BhyqPqws?n>&rn@v&q_(W{314t1-fm|MEPY(`@x2ES@{ZEpAM8?S4#?Kno+!NyEET(9TpOewIeM#A0j9Z%QZhoO2ssmydLOcS?Q4Nh;#8KjQOzEsQyZ9!KJQQ(}q8qb|md`njIn7ZxEU`XKAD)mqsrqJeZtwHSfiuIu{J1_I$>wA7u_j&ACCM&}PU|!i{&UHp@Q@%-54vBRGM+SULSv#O#u<ZM*ShDZ=N=c*$3Yzuy5}BJJF6?C<*V|Cko*VP5fS|*LsmFRF{OnFMPgadw)^xp%Zi|6PW)Z(7SCbiCtX;NDa7wD72Ew0WQI^*XbgNT$W^rxECjcKW5nL#+hY<aGH+8t)YP~^;J#O@vY6N&7Vd^Fn%XpzC2v~1xuSN@~bLjHW&q$X<-xH`Rt+%^tC~)K8IotB}VtWdX<7NYJN$OCxoC3^XpEmA!o*u?)FXXl*$UV7ihwoM>JCr4i)x8;ReG-SZE+=rpK5TS+AEJu4{fufwhQ64M_W7|6CbwCUjky4rAlHrQnZ6oWEo#}P%Cg7IeB`A7o`LfezjC%FHOblEr((i8q)VPJ9FHqN<a7mI)mGw&k8kIkmx6$usE{d*0Fdi?dhlM^+3lRoT5bhqAu5$kefnHH)2&_;mrxVOvd~;dGZ@T(fLVdr)L_+bLJ2HPbn`=bjp4Iob2){cmNq*EzQ0(9!1z6CBB4&MQ-0Z#M8v@WwvM-s5(E;0soK1V@uu9X<RFd1i&;NNfs*u=#mO0=2r~;$joo05=b0NvGt2ihFqeuIy)|A2kA2*C5mCNkoc_<}`7TA5wb99LA$;A^zSV@@xR{AWMYv^A-OLPAD50=(HMiHF(rXx^7%uI@$$ovjJ5qmexy)w3$H?zKqV9^if>nKycTDjLF{>~sUJxF*<e-EaeCZg>&?#RO`x{U$1PZ&Vu-i>@oF-)IqNVSlR_TN{FnW)#NaKy>awbC=2(TKn%msMSqrcCEn<1Wkl^jXD6+mTcOe#&CraV*R)7Hl<4cutI8?Z|qI~@I81wCHsit&#MH%?`}qRnYIg_z1}2}a8%kteFa_?AN7l<!Wdf9DM9Y4LuY<rB@$fYU+5ejWtXCS+xc+#bh-?yt4O)W7PGw-#M_K&WSee1yP*InXC-)A{>R$~d`GkFT~--pQ);<GF>pfzLPcm5!&J;ok@(Zns#myMFUwe*g9DW2Pge?_4YNoj;4cb8R~OEH7Tu@vjBie+}IlZ}bv1beC~Y#sn7&7ewplz}&{8vK)(h@r%cY;jhvXM##{NVT}UIX>(-B5r4Rzw_7F~zDiXaM#4`*!;cD4^CPJfOz8GXyvv274^wu(Exi=om?1`VCJTB7nOE78Yk*GEk;}Zx`YCg$7=`8+Wy^UNkWP@~R2X5t!-N4IQ@lP%$1u<o@w(%zCYWiAaxX~7KmM*e*Yn&jVY(dd8`cP}$XM}m*@}R^t3rQAbAEV`3}54Ye?IiT{rKB2zx@awem?m7c5&F=fBo_I@OflQp-*steT3CL)?8AbMeGtYuxB5@#V>(x5CUXqgKIq)Xr+uzXxA3*!s{!(xgFwh&Egm2wa>n&-u0<w+J67_!}zaXJ<LM3#7LZehp#!zTZOlbb$8`PC&cVS!<8AWnI!Wp+Nozp_uqefR9Nb;XL8u(VHsWZtv~+kn_wu8d0Jv;#c;2EWy2z)ihuj(Uw{46fBpWKfBR>6BI3Xv*DU_nY3Q0nzbT<SEVF9`zOH)wi<r&F!ViUemZo!thV>JS^)&j&_IqL>aZQ`=fIFqwH2`jj(OsWuq^DOv$kJZ;jE08C5&k-Q`22oZ(>;0GMZZsYXm|nRy7D$5qk+mA<;2h7I`?GZl%E`a#;7L@4M7~d66j=EeT1w>5B=VFPuBbQ(f5E7PL`)0))$pyg0=5{^II;poKCqN<Xw^I*vRuIVC*Fi@XO!-`nO+xJ?!P<bl=A^1kSJaP#TB0k9XB$lDtKPe_Z_p1J;0I`fyiGBr@Q8vDqM*Q#5p$b47#U;l9{uE<PaW*jRvfxa@xR?U_sV;vRf?G_BuQ_Xv+sN$MrD$0;9L!qzi1G)dIdqCZVLW|XzBzW3*PHH1i%H3K`k2`V@OXX?^X=TY1I5&^{eBWjOplKfkiQaQ&2v)eca99)yVxtsEd`I2zTM<Nk%{Pn#)efBMGnDTAdUl7|sE|^svaTaJFzQ1&=5d*{is?Npt*82v@(?L5tg*#U5yFG@qinIn*JqS8WPu#aA`4OvUk7=%B4Q}K={__6*A5u*4aZ~Q1?huiN0GRez^3Oj`oR7A!Z>LChKbR=UTu3N&oLGA_nTz*8R{SxC@pkhc+L+D*2QVYkeIa@F80+9RmRm`^2l@G99otWv&+jq10_l9=rOl&TH&_~**5Me5JZJFWXb4uMD7gsysPU#k;RrSs02chuq>|_-8^=NV(*#r6EG%Np6<d&{^T(!Ki*SvZ<gS0<5~Aa=sf@-WhJGvI4hHEwr#5s9W>Vz<SFo6w2sW}~9E*6!=u+n>N4IMPJg#F?PJJl>Hh!-QHa6{uAgM#twuA@97&{`FOf>whFXL6F#@O-}JrLyCIGhv3-hjkA=z57qI~B;>77QDSfU$3LAjZko#JxnAG-c&iK~4AaadxD}3)9zA>CC)&^`(V=%dX2Yr@g1|B${FEZ<5$^oQ9rJMDG%$w_7m^@W&??d(Mdu<pz6Fu)Rug=Z;Q=ninn7X&qYPogZWA;2zXcy*vlyI3&}(uUQ6!wGbiO8c(^W>p8HkEDQn;f0lV_U0SF>mH1B6{#sV5;_Jr0J`Zkj&XT3q|CUgd;i}x9fBg8zyG*B?kKR1GbK&eZ{40oH_s~d5jwO3zmUCXy|HQlqMOzw)%_aCV=N|6q!69HVFxa(%J*$wiWM6}~n*c12QEo0)jT2Q<nFbak<h^<0f_?l0ow+6?ZQ)a54(JEyFM$-9RyF(hb>o~iTdBLb42F*rhMv=Ezo{Q!7q*8e<3QG)5BOq`RMFDn;~zh5w<&vV1b;Ehf36Rk*b4fFj+shxz=+IH-z#JB1rAR1veQCadi)w4V1mL!9MsWa;M0m8cev%pu1f;y+|6z@fk_!NLMQ;vn(c%D=rmuL_0Lfv_`rEF5aZ0_%k*5L310<2n=ldyP$p?{t)|7Ao>m4kK+ZYK4k@=&@T2^`V}DBBQ<))qOG_%J*<IH{fsHiG#TVXS4;HST%7A1*4QO>6SYk|{Q-NBNZ2Nj{<OQeXWaYV@Ti6JyMlbyl&_e3ImXswZ1vF)n9IQk+E#A6z^O&LkVsZ`-K!dBQM(s84*t8~9(aJ*#z&O$UPIrct@74ZlBSxksDND>wdPRN9*kTHo>vPoGt+XN0{goAFn^_bX#x%9#Zpt>kuEGbQ^6btbAekTnY`mEU`o}Vj?<kaM77ZklnH+|pkz-F}?m>sT3dPQT7~Kq`5>eAh?E6pRi5MNFun(to4=}&MbD9-3_T6S)R~5q!<r*bNc0G2}t(WX1_87p5ybqz&B&<^-2k}uRga^@zht|w#TT8cmx-ETH79cZ};ibi^ijAFat1V+1gLn33#of@?Yr08pL?UCr(hRv?EEt6E!l<JNB18v{Vp!|xrXbg{VC3JIJTpL00~b2gX&7I9T-NV>Q>F&M1khA5R;9ATz`ua$VKY|ZaO`6acl$YNYvuyL>B(=z%hT{05L_`xOERVw^;Fqq_v^FMaDRgh(^tyQBXc*I6P@KId@P`g(K{afrANA;rZ<gg;@i;{U?C(&!J0;Bay1^=24@ukOPD9i)oA&!mF%-SH7*^=52PDVU$f#-oYYdrRpBjp$hubOYtPqmS~}XJzK5le`8(5UTb~!Q$mWAMDP$;9>xFnw!m7q)2&Ff0?_&>toYSo)Xl4l(Qy>$;3|%;Xr}^gg5kO|J$OFQPH;y$whBfu{)_%cE6VDRzsmB2qnzTs|{$nmn7te2uiUGkGXxS*0@TLYT0$A8d6ll9|Mru4-tA_tpak4WyXZdIXPpMF3%a^wSO~mEpA_@(2yjon7njtRrGQWafO~=d9Oz5M|)4KSi>NeA~Mne&p_cicbw&t>b%`$6rPxHo@)xeig&Mwxne^+;K0pII4xaBV}G_Na_LjISHucnl{<bqAFXC2(UV|?giA8d}kb#kG*Nfvuu1H1_xfYg-1;WMU#YPnP59wBfURSwQufTy(&80JbiYw_nP+2b}Qi8s5!yjb0|?<rE!)1OYqvbciFF(VLxNfh`SOePr3{Y7HLUiA|Q+=V@1JRCV43*N~(t(zTH6|lUl(4T?lTo<Wjj=wM)OseZddm%}2gUsBlb5HlFP72OyT@gt9m7Zm8xToZIMtm)Ym2#_D3Xig8a8X>6Ou2@F_qBq&_ZugPP8VnZ$x<qJmBsLT3bBN=g>%bn@OHDEWm@3RRIR}w?naNC_F$6=Pw>!uNs0W7WYxA5P>T*-j9I}M^*6KZfBY%REs8T(dsSHAv5Tu;C17`wIU{ggzTPFrMbmVv)8^+Xkw*es0vLChl=61QyxBa3E{hrK@R4d?_PF=b+XQ_pwDc5*V>oX0nK%%lR9sGUQGnS5uSxbfF`=gGOomD`na&85DG-$UgiD+}?ab3mdb(g*9u=@Vc|9|wL7Hkxw@Q(uaKURc7=TDJbp}dDPt<hxdq+|g>{;Kr1#8G8J3cpPK8L=Q3>?f*vaO?!Y9MtF0_>(_-OSZ;rv|nd&mqZYB6umv$38ox>}Sroes09dcIk+a=G)-v0C|93h7zW~p&}0TOw<Rr?3ml+<fqXASt%ih?j1yqhK2J8gGepIe4A}}AqU6M{DS|O)k2^7rW7}^J#b4KXMo8Jh%9vM=U8oC4szL}n_sGQT&)1Gcu56hZZVfmfQfSE-xp!dnlKNsF|hC`f+a#y-%%~pMU$YpwPNueIPXCfM3{PdJU_Y#@N?n7Zv}AoV~C?$vth(Di7m`?!>z{w24++$3J!UM7j(&llVP{7)%`pKGFt#0O-HnsTE{%_0*kFG2tC+`c#@%aZG@;i$h#_z;YajHxXz;yy3(^klLjCtPp?nhgmLKG1l8e?6%R}}h{I4eH%xU5Jxxz9h(zd$lN;kYCgZGz&M3-&GnKvEF~?zb!yTjCVSL}7edwBatewEwW$8LsH~Wa2=4r5LXsdLu5*inkzj6}N0~v7)dVGz2^e6jOlgf#Jd~(EgBJv)yYVUmR8NX^Mbay7@=Z4qMVq9WLFCuKrDT{a_{uu0PZyZH;N6SPzSXo=dF|fUm+T}@%)aA=+^LBd-%g@ZSOzDcOpaeru7N?hcQ09jJP6Db;+CJv(vi@0n*a|S<v4rM_)gs?iDNmVWI=%LJwyVoDFUj;19rC#n;(3;EY$}c?mp6gHvH&&9QWOEu34cC0QY?GWDVa>0vL5zlE8hc}eS;2W>q<**Qw>RZ9HG4jRuL=@wouV0#r*-Y6gdWJqI3NdcEcvo3JWT3xmd&HKm_^jbXtYEg~~*J_m@I9U>2gF@DbLEQ=kG|GulXkC!0b6-!SxRUPikU#RLYSoNQX0j!6gvFfz!O=Vh|HR%$$^d1->t3DTNUCi{L)rI%P%D5$FM_H+>@ywfq+drXac@c$dp;Bv2Z;U~(g61~k+GpySs-1v~RPudfX36}J$f_Gwo?wJs5x+pV^sG1gzXqVzZ0e)SjUo|T{7@6wdQrSSRVa*up9d8S8*Ue2UhTS&jvG731l@Xzmx}vXpIj@sjAZ4&w30+TTOfGI^7AgWUlGp`Li)3j4Y^+d62!6(6f~yTbd@cuMsD1l^rZBxc99e5|R#q#p$o1s?abbH+(Wa3ePjDR)+RcnWg;-32*m9rtb3S)<(}9vq>l$Mh2;Ce;Tf@qj&wp~uV0rU>)-E1v6*1+7QJ|icN}9F>;dN#;F|%qC`CZ(~NWP{U?fUe*%;9HwnVZb7ilW2HVH=F+i8fY_?l+lpx-qy%cpxfuiVRnH#;;paYRW7%D`%iMHEF2;K3rPfm<xRdp!sy(CRc?mdpTuBp0bLiXq#w5HkJNWMR%B6mzCiN5KjlVIB(+9lXrQ|d6te^VvlaW2gdm@e`}xm)OC)`{li&dlT@nO1UhefJt<#x7@_OMN)GaQI-Qk$?9-l;2}Uwpm~wo9s$_1((iwKv&``rSovZd}exNzI7uz|Br2_zrnT=8iw37vORFL3A&Uav63lzjwZCSMt6lrXux!n~r3m0#a8tFBLZD0dDbUCb;?2@Dv$fkRhDwAW|MaYW^$S%2GU`rzQ{~4)c+G9fc>PW=080^wKcVi@}SoE7WJ(r@G&ttXGO<Hc#tJ;zj3szw5@k^!0$Y+{<UP@#<Gq{f58mKL@;ewO8aEQ5)ORvK2v-H~^Vc6Z6?`peQq}`1WuP97PRsvXVwZ=HAh|BGOPmn4@pyjrA1MqQh<O@&JmcL5B@>_)W(A3;ANCMzqv^Cr&MwFuKuct|E+DypFcLzcJT;v3ZeD2qF<PSsBi4qg*jBGm=(TdNbZhK@Q?INZ&^%;Q5)y^U=4{jus8Z3OuFrCwtjEjYK5*m*&Ocd4nI0m|QKrOiB1tkVD%%ye~hgwC4rQDzB7f|XX`g!0<d^BE~wtzd2h^m3X?UrGyB>Qo`i<@!a9Qy)OZklBo2Uk(=#TI`SYT|>a?D~dX+1wnCV<$@&?~hZU=(rZ4X*fB$WGZVnj1}|;OHrHr-0?_TC!dycLU$#5iiC9_ZMKTz;15~wvrD)3GH$Om=`?TH&#9X&O#@ezG|H;QOcHowR&PERI1t8;Hkaz>oF||DkP}U%{bwc$$?5YxhCCG%Ec$>1%<<+R=wpaWx6P5y1l8h^KMi6dF#LO=w3gyg-qRi=LI0&*v-vy-n_H};m@>7;o}^d8Uw4dD)t6AMB5%!SXpK(!$wewLln$xv(x-8(Sm@l<Y&y%-z2go_Ur4I_SBDMlJm9inOEfuu`NB9C4o-erDsTay%PjSKpnEKBm{e2HloA~g^HlYm=k-PP(|3b#wI@SPI2V@r?jwdMenalf>Ca~uEq#;bz1DNdl-B^iw?$%9im;BF@Uq-orXqj`?vQ~a7?nh$(Mh6R9^Pf}&$tFd^b?x*7mAj#&cJkWMwiy{9=<0AS*9Wnlj`Spd*J7!Q>+h={l}7Q6<r6s8ndhGz#3e0vL)7=EziKrK~l@I*n}&*SC701mjIpos0u0#bmaL~G;LLkj3t%>>{boCYd$G+f-8UTE|yu^6ps%9D27+mt94l(v)Wv;NVVKpDWcHTlqLGLG3EK=Wv}4Zp$`Cd3HzS0M!|i^eAG=-ncyu}FS^<gF@O0`rfyf$fd&`<F*xMh#k+HUs!(>OEP0Y6_6csEU!>J$*<)}!v3q{N32u{WQdZMH<~jB0wsRMrA}kd=?p>;C^PTfqS6PYB)?OC!VuVxn7_amTo+Kqh=`KD&@NrcM2~V^osrC6ihYxEgqhfMLcq{*$>3<UD5zYHt!>ml=gx(93hVi1sG^WW9EX9Q?W!y&Ei81bqWEo*?aN)uPmMgg&F2I~s0#d2mj7`hPlxkbFq*($JY%53C(sI8E50Sst6&wio3S^7OB%6^BwqdV`Xy9Tx#s!;ul;4_0UW{^`Q9uJLF*`)GWciPgmQcT^Z94ypFRpnstPAjY&d-X<U2zFIt7IqKxSkIBSLd`}rDd1<@|rHHLoibXZi8d8)-z{M@5|4q+uv<KgiIUYROuJ=A!*TMqEIxSidtD;=u~|irA-PdQ)D@y84c^?_Xm#vzecsQ98RiZq7t(4@h%!xKk}l#VB<*zaqUZx@9_BsZZ~^^cuQp$J#ajYES>BikCtN_>==Mzri%T>@MUT%=wP&C!DmM?I`;Jv(mlDzrv)-4a!&Vl>x}jl0D=|)VL)nKZlA?w+5D&<P*hy^sr|pUIvBsOlw*z&i*BoJDP-6zWI2~jAYaH|E;sGOC~kFm7TUO2arAq&&|W;4r^nw2Hlj|!(f|{x9A5;E;s+|5`#7<ikCUX@f&~M}l(<t9zIT?X-;FAdDW+Y%KX0Vv{P|(e51^y{NTsH-r`A^9RLKxkO8Ncw|L2b<6WM4$p4Q~}m;~3Lul(yH^#;@ZWiuKp!S+=|ZgZQp-*|nTZO1Xn4#IFsGkiTyXYPQdFB19;|3=-7RN3R^%)Y^Zd`G=0XC|&9)g4=N@O9Rx-?1+hGeMaRR1X+9kG0fvd5WC%cG+$B1j8w>=BI~dGlg?=wmrV1_li-WFEg+9;ahorQg3IhPVPxUL+@mr%iR<X6Xil;w7>xY-%>^lC}%AD{wnb9d%jZQJR^rjt+$ux^9+S}FLSuwh9cT-%wu>##0*o1bxhstPBTv}ja)u=y^U^Lg-AUScO=&_8eJ$}woGtJs$~eGpkm#X=lpduR~>b?o->#g6Eu<fC{WXYChd1d&J7ZM>#f%Pl-T1&39Lpf2-2Hw`cHsQ8c%+`t-V@6pemt@IX@%0kv+H<;Lv)zyJi7Hi_h7XFB98AaQHSGbxYEEvV|4^1^YCZ&-3&!ReK@tEb;%z)jB-2LP@|&cyjUyag&BypSY&22n(DrzoVuPMpc^s&=-)=PDa+*<u+fkF&E$s<hn84+*gC9MJ@YOS@xJUk31W|4{#n{2e#CGw`PBzis|W);ds7YJc<Bu(iJ9Ea{SI{_;${DDF`Ks>Xp)>012z72d`)&n#QtYHfy=rnFXX&p7-f<@l3b6U|gzC9LqxAA<b7X0|I6RX7d`ldQubJ{J>o!?kss`&c>)E^p1h=FBTIp+K!q?sK@NUmG{It9*U9cc<ZPmAi<%k&5JN@O3X_R(m1@B<AangNkdtjoDqsJvw%CO&pDoFZXC^=-qXNb`d;+bc=<Z^ao-_C*@<!bKcCgRhJuYAdkeVB^MV5t7JCs9DD|h;aWS)wif_zf`kA?=w?w)Q931E-`W~MX!9F~gs|`N;aFS*p?~XPlTu8H(@L@vkK5Xs^t%5avk*-W(3SPR!*vci{!DGIgzf*SQ8{nqUBMm5?;jv$w<v6Az`EnRQu*6gY<^i5XS%e+L22F}yhey6SG(}_6a)it}4V}_sv9ASX)u0r$O4sm3C$7=dC4<q!S=0%8X>T5joIV9=NuF?;{Kh5hgO`}0Ii|C*{xpGc4BrqXLxzQ<@PM;R^cYPA<V%aj+VHwnfk=!Cx2p^5qX&aDh8)8gA5E)&rqDAI-pvk2J#TIF4Z+>kM~5uh;x#l`j_bX)$LO~{^#zb0@C}j(8Z|koN`N#Bcp%f`W#<`*w1`~|dso}3`Q|58sbCibpVHKVn5vmnh)B5QoZ4VZwU;^?*!I!7L|X5gN1Gs=uBgF3Ct5qeOgf;U>s(`^=aDMc26$(h1FR-=jC8g|Qa>zvMYyn&9F$>X*-|fs)@VNmqy8O~>Aa@m$GBx&&Wx$kEzEu%7%->X73mPH^Zm7+*ZNnwjFnFz^gu!}<aJijD@c04z*^=;yrc@2ShZ*|?{StZq?|^f@79MyJ5PDTlk!n2-nqvihOOGy88TGrcn)1N7x+$QrPVvv-O{O-+wB&yKi6+Q?B~C}eav*E%<gN2+5Kk`yRS|!XSSr^Y*9QTEf=w~)jm#5>*kf2ebcn`EW<_9ALn2CD$BsIpHAWk^Y0SV!~8%-ZvDk3cESXa0-|OT$IVp%ahsc|djs1!hJmJtj}@-Hftkh(+68_8$KPd1j1k=ACFBAYOq^C)k+I@du@#{iXkV<%Nw+~mx9`uqzQ6tW+b_TU2p@hnVf%I=jDG+1$KS)}KPzE|xjiz=*KY=!eXO};<&1b*ChOK3fpZj(AAbBg1RH$sTyJBgj7@0Q7Vg69E55m`BXP~*7xBaL3)8M$%y@1Q!bSdn|NY<pA6+S@%K')))
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
