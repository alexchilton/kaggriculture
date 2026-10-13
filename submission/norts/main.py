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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_kBvK;td_}mYb-<kV%hAeRik!*rIR6#2cgS*<h5U|i<aizBl{r5emJF_Y?+}zwevU)gItEcHX?5>Irj|g{jbMt@w=KuJo|Mt({{BQs1U%&ak{^?)->p%a?mmk0R<<oD!ee=i5H~;0I{-6KzzkT_KFF*d*fBKjI`=9^&m!JRBH-Gv4KmP5PUthob{oBvqynJ)}>-E!@|82TIUY!5bUB3RO->yIYc=)$J{>RJyJAZ!t_48l-FFpP_`L^NffBEYVzh1vlfB5<_pML(~r%zwM;M>>RH!rRE=imN%z5ep`KNO?>?e+KLsJ|@U58wX#-+x&@>gxxstNEDX{-@(_@8?{6)BP9UhjRGJ-N&)-`pfS>{P^A9zWmDP-@i^>`Lg##J$za5Dd7Zv{PgWrn4j7I;!pAS+^)ZUe*59uPr;Pd-&9xa{=wzC+q3Z7_4?hH|NhhU$Jd{MiInTbNAP9NKYzY|n)5Hk?nFas${}qF3rq=o+cvb@r_a}4%b(tsi7flS`#O@tH$49M@yXj_OSURa@!cK{-+SLtf2|+Cb6lbHrdw;17S{gK`})=F@Zp2R^?&>~d!7#8yWPWP-s=bKzHhrC!NPC1%YFpLptSEb>utB&E_3<)(K2_5WoG+rm%I4wXRJHeXSVL|zn%W#(pC7Fg>U1pCF>m@H1-tQ34(<M56A~DDA~|;0MXYb7WDDi%7TI?>C}RjUzPe`@^QrvRld-1kv$JH_H)4V2evVOVakERf2w$~AH!PzoA4?2{k{L~`k#~!dHwOn>$ji(_V2F0e*WRdAO839io1Uj{KbsJ3;cNJGdItm_-A<T)}Uqgt6$E$8zz;Oa{W~9@Z%{h9aSYl^SnTBb@@!4uLe_A?waj1+Tg;yM}-Oc-(yy??p}F(%*PB9oZnO9z27wNw)N!EK5mCIceQiwPS`p5u1~&|RlF{z_U6eio!#O8HI)2o|I$Z@l)2nP$SHhpDV`GBn0<O#pv@jG&smJ#W%hmHqmO_f_IaUQkOeNn&eO|_5R!0w@@lRQL25ODn|N-tlDU#_{^V+&bs6bk!^tDK7Yuj%z`uU_^*_|%8Dy33R!|dsNy~j7_K7f7-iIALqy)2}k9^X+fzx|<1AJ%7-*50z^f>Wwj}9V`;Fx3JS6hXd&^s95hvBla4+JRqY81jgkp-~h3>^`2JpN9IM8Y-c(ojU`i?Ae#^iwVq;Cds$i)_+?3G_evUCDdxS>J<TBKyF2Kh$jlxH2*?uU&IH;Ky1V9+|pFGTI9hokv(Sdh3e3^&gpivU9}mY#Ob#&)z<Bg{M_!WyPm}CGZ|Uk)^J?ZjFOqEGKv&p6i#Oxk)CIa2dIQ#*d)(*$_3Xa)dhltJuW>J)+L@h|W8fC~m5mf8dXoU=n=O9o#@a827KM@F18M_V`?vzY>1Fyf@q8f<z?wwu)yTcx}QL)wppUS0(M%4SxdSbk?^^`dc6DW>tAt_tPt(7$HPv*Vs?q)OlA$8tu6-iSM)4fllD_N*p8Qg8&eu!mmm{F84JDt_b(4p6t+CPsB@`)Ho>U8K)UDH5EgGkNb|&oLcQQ0l)xaC14^i&$XY!PNFO;H6_J`uxHS*5Wvqmk<28(CHNu%=TVZc?DN!t=TZ2?EC@_#KkmfplkfTN*VkXNo(Tv6hI%-Q1EJ^g<h5TP9-DI>SiC)j^VdfCWapE?=OF4$L6@#f|ADJz`#3ls=i+%1WOyodcmHF%MCYAUkMSfuZDf%VHgekIyWc~0C92^4Tv!~_Ss#<;=H#6H-Q)e+=U+eF{&M~G*Z&A?8$|}u_nn&<KqrC(T!JTN;m+OcHDBJ2`2LjmfN}of)l#buzn?q!`#sM1DC&&VuafeuVB?<xviL0By%E&8EezVOL@YfE)$h2~Fi&Q;AvjsVv2*5gj=)!y)YfY2^0?BO#3J+**z@jknWZ&->^e-Egw*L`eD_CEAYG>p*!_cDkmv<^0_axAox}aPaJ`{Chird6j(>y)*18Q~MeKizrvLD1UtfO&0|7VP22rnnfCsQEn8IE{8S#@r`JvFg9`(zO@?BK3`uJ=5-r5;Imfo34<Okh9z{w@lkmJpNUjOX+{r3`O-efaCT8PBrGEZ7@BrUm}4d(7;fr48Qn70BEf7};hzu8=doBu!%9LUNiMu}BPjTzsv%u=P&A@|}_`}Y52mzCC>?(MD-mJM863MGV9OuL06FM51q2MQjOlE^Q3HK<M%nBcJ6;m@x>efs<=0X+cjr|FNdj5V&lf%Bw?Il4d5_7_*C7-YO)lE@2ubgi+nAe1|;GL=TJys}reTLa{}@o01vMF$`fr&o#Q039!B|EP8<_cJg|X9pQCh#d2sTbqj=S(zsdeRVcb2~;l53FyqT(j~4OaQ7g>OU+4c)h&06bHh!hiPHQgo6CDlRiZ}+*^hJKAb$Gc$AAB2xh|Kz!VL9#8BSiyq22$$2KH`xO`Fj!D26*Z;xYRtAh?x??9JZ&`tor8`udfPa`~eMls9g-jVPIO7?U6LCl=*g$-1Q=c?+8FuC6P02lBCN@v4WuJis}z=l)3FAP|fGMV$Mzn-@a)wE?L0p~E#buXADl+ZooPQi>UB<a%epZG0%D@b&{*{>Wrm?&fJ9LjU=*uU^3BWNY%U$|Amd1fnigG4%e>GZh?I8*wP5u6nKjAO-=6cN>SlAZR=u@Dhb(^kqlmqXJv8r@_LX?VWv>hZ#jb3al_ac<(m?D!6m&^0nM9TS*>#l=pIhc_b@JSOA4aR6G><{aXE^rrz^K!*UB_BjBR$pc09mINu6}e^b&?o6^_U_ehe?Q^R<l9iIX2YEoF_3w2thA~*uF9Vn&Dw&s+!1%n~MKc!!G<hVCUH~}a<l4z39>3!WCvEnElK>~7Tpu<%@b>L8OBG{SKXif2@rXhMDk<t96Sd?QjE=^hs;t<}mXA}I#`=Rr}^h#a~2j%x;2JpCD+SDlS-WvMqM`C$>;NPFjQHp=auC6aHQMUDxkE0&`Z0D(q^Sm~N3!r_YdFzHpk3Y7Fh!j;a^8F)_-=;nvV=w(EHMeubkCfNn9wlBLz>v%^%boK%S-KdUjDqmRLmIGXo7>dtx@#6Tv9U04A51COW8+y?f+xc3IA(yJ09Mo@32``|N<QYxBXp*vodvi^0`XirRs#0nheDH+u1`pcbvj|(LAhiy7D@eWR{RF&chTaNm}<@H*+a6YGx*F{(Y*|c1UKZrjD*KO>g)2r?zy!j2()|Fv9RnJyv3M0djHSw+wlzHV_zn>*kPhf?b(7FkqurlUIE%DNtT^n;Xg9_1W}MC&jl(WiDp?yl2>WRIHT#ly}UpmTnaL(P|qBCkckzMh|TCH#N^4U6Abl9)Q?~mCv+5J#_&s2f`xX==rEDA#~NNWNp_|^cfvqg#+NRW!<w}0Sq)>kL<;z)Hu|@_5=VQ1j0ddfj)K5QcbW%!M+U3Bl*A#mK~fZ*T3j<3*(sv|Aux8B@2*&JNhSm24f+%!I!E1yW?psvb7+<1c!L=DNJa0t5Gpsi_m7wb3JTNiQgO7bO|g75D7}bi$dZZ~7bEiHU3<gVtf|c@CrA#py;9gR$H)s$5>`M4iEORr@@3}WU(MqmRpuGJ4Qb6U^?eYR%VJr8vh?^Tk=N~#k2_%%@uR>zf(+F=Z)F-)HeyDB#jHYCP;yTtJkV4cr8|dsv4m;jg9K~wR0;yozKki~ey&qY{xak$rosib?_2fWFJLZIE~xg?yWC`@4n%r<Imb!HbV@jbm!z~W{)AH6io|g!5E~q+OnVvQHw7IwzkhxG?JB8?C?ap+Pe5KzuVM8&j20N)-)lDDCQ_iuM;0tWgH*>vur8M|_r8cHl*Dj7H>+sj4@_9dOUk1Kk)vGsb(ACVeiuItK#3*d33Q2SVJEe7C1l~!y%eJC8W|KySQe{!7;MYs{&@{va<sTQ%0ezd)3QBZwk%m-7su$UboCtB9K5b$k56{W5Y2$;0--;k9|F|$#cKVnCuL81Q0vW&_k#mxmd{XoB6uXq=GaXcwh4;B(WohxovA#O>r-d4gY=eYT(x&+CY+R9T43p4+ib$QDw!KZgbgzy&h7VJru*${sRb3r4wl}vuA=ID34t${dnty_t<`6e1EOLWK=a<+QdvWr+0}rw;#Yto@WYyEtnfhHXUE%syGIJ{Z*l#ovN!I9BjlGJ{7P`gKQ6}mkP8!}{9XXrL^Ghlz}rxl>Iw|I`P)1nw;@Z7!^&S!KuMdrzOUR9>JmV#V)KnowXzjqHsGJPMj?NZtD_{v$pA~=lzd8C7S*yAKXBIl>FRgZnwrYsng0e-yM7YwP#gN3?$*i=xvJQZQ(|6?06B0f?Aue&6)Q?ZJ}_Gg8qa2dHeYRP#jg~tDp{0=Qqn>0%KQuKUXT>d3zHD<OWMXM(mE~9{S6CV_*kj0^I1J%Rh&<rsmtb50=A7s9}j4F<rWoK{GzJctaPmpn3?U86Xmye4uE;1qH@F}b@d@+Ywu_)-n@^^xEb;B9*)ucoMR;FYx44IM_G~;6C~8YR3l>z>U6l4@|wale6BvHzEA_ijR;2o$^-IE7Qd8FtKI;pe^iV>o4p6BMWK>))t+fSDG0d}#Vbtr10hOaIYNpV0|j{BK6~?p{Q2_EP7?PXb%Pq<5lNt7QAK`WSV3ZR^C!L0y{1esQ&!$kmBx~ib@gR7taJhAFeGM&cuky<PfY9VS)9H4wqrd>eXxN!7uNI38yYf<Sghbhtk%!9zKC<Oe(TAXNT-I^mjR8zbFvDzuyGi^{N3)YHEnG<yyO;giyA=57O`}z&bKbJVF^`P_eY$E8#Ce>%p7PpmCU74MN(7cH-uw)_HM}Yug39DAYehd3**4VoF(*&w5T(c5@U-0RLVLyBo(!e*8jx37Vz@at&HVjL?mvIRnvcyJvUBv>0bGfi8r*e5vrZVG<R_&2~~UmIts@A?0?evz0kx#I792^EaT_)oJKdYQH5?Vcr{61bY+o3V`BFM?gga!=0t$~D1bw+Et<v?lH4^frF3@*Zz6ZJd2NUwGVT@!T&u4=x&17^XDYoa6srUS20=Y@r%|O-zUeWbIoitwjI63(Jy;ak7(Iq)qKNK8><vI2nz~%nAAn}xFLC<)!OD7G)7>bTrBz9x_J|8PHBc-mK@+!Z2^NqrVUk$teMIsZO6wiq1lW<-nE<M-g1QK*T?}uDP6Nx3)kRf+78BL|=tt9MG*tBH07*8YMH#a}Dmz%@*d<DP;`4PzU42wrR9}SwFQDYuyu5#SFun!z_&Ug$=9jQaD3p8g#@VL{15p7amGGb|Eky4*hn6z5gBlPog<k1Wv#Jq9kqoX=Lhw4I3yw`Z4&*hi<wZm<0i_nKrK~lX%s-7`Ta-?D3!*TUzV(`YMh?sSg_V<ew@h0b+un&G)`TlYx${)4uazp}C+rlKnxPztOc@wwYXLT;oP<0fq~o-70@7u9VyhbnR%z%+VNyi1;HQaZRJ?}t=`m{L0;;htTdCSymW4P~dhp_+s=N>K>M^}cUdce~aY>nKcve{UOil+CchiZc=1~eMR~t*Or4+=&vUsR(NEH&vHEXJnmtYI8$(@d|QpW0IrNTV7BdPfW-2q|qg!Yfb3CaHiKtG|8R_2T-x(_s!ruS>8YgeD7EoHzA;>^b2`Nzw3*rNdMZnsXk4N_C^_j#pyq6K$bS-b~rlTDi{?I5k-5GM>0OkMc?Mx7#VjNE2Z`We5Qs8`?617{&I22Tl9j-;iH?+ydwH1SI;l^D6hjJIRelRzM-lzhF%7-MD2wuio@R201C>g|ptD!|Ar`f4o|R!Ib48kpLMjZIaLw<$E#>eCDN!+1iKDP*33LgY#mC=?ToK+*FjDXOB-4xenFhy2M&zn0}Rxy}xS0&>kx&?bf+4&f~Tpf|igHSt?OKG9eSn(U(BPxB}DzFOLu5!>)q2>0mlOw^%XjIyG34Jio>UcOG{WLQchG{U6Hrn~RVCeg1Z`(cV?WtqU0X{=I5(q|bEN^TZAgCuU;2&1`MQY>{wp6IpL^<Fe`I{^T$eprOp^VPj!aU)_KtRZjoA>eBM_;3Pt{*Myjb)N~ZyRppP^nXWEwkbvii~%b9#A>dwh5!zu`zpCeUrq5?@@^D4wbU(>CaP4-;!Inn)2$Ts$1TeWX4e!Y<xD=IrZwEvt$o)R2ce@$8ot@s+e))gB+%S{yqn~68oU7&e51z_HC>}h^t$+Bc!TCtSRfq&#>EaqCpdZxPfVzTvQk)2aOXKrDPq3(5^F~{FVnUqQ9W&s7<Hz=SLkehzcpZJw#T&qEo0Bsr|9u9#bOh<tJs#?w*e5P1n3iz3Q~M=V#cK45H;(w+r|*2-Q3AEruw)Q#D28YiYLs&5+VguB~V{@Vas87U3n3>1jIhg*gmxSnXp@(eH3&Bp6`D69-J~sYbxpmkwQ<U1Uf_>(_zqw1jKF+_shj~KPXaVLGHg_#{W18K)Galk!~QD_H3NPtic<wo;0|ssuBS7(vGMMVX}z8cDf?@tY$alXG8r-Y|SCl55TP)1?Epg8Mt)c2?DqBr^P?Ig%^~Y4o~Rft0IaWEGY?>J%ub<hVy?!DGC6Q%9Kcz<r+p4lmS*y^te<o=Pk%-$ix5>^dyi}08dS#FBK7u%<wFrhiBIc6+fAn8BD`OKKk8lFufAS0zP2SWkjzom;0ec6dAFb+>)sU$8E>2q%b6f;4t-qiin+xy4^&m1{RM;Tgw87-quu9_h@8!La-YFqa(mf;*1p-VU(x}s+sJ4z%1_xaNaExSHNzrlrvXkHY(j<o<zmgEZ<4M%wphN?M5A3B@{uoMMU>D06YJ?52EG$?+$<Hf;DlKxK|pow-xp`M_HNiWE-gze4{dW6ee^!`EJLaRAyuPUi1^B8QA6y*%~=P^T9FZF^>9BwH*Pr%%@8iC(QQy115cqgSIJt*X=~X(r76RqoC1%L3O6kz$?Zm(5^d!6?KtYlc_(1JO{d%RgTGqXR@1I?Q=XOB>u>y3_7=ENG2}Sc#X*?4(hIp>U;nN<q5Qu8^wT*{fPfT^Z*&sVe3DR{1K`4W02@aFNPm}s%?iNXxN6%6HPDG@YI;(r#+2=7{lNM`Anwk$S>FRkyvqO0Ev4wzrjcoox2k_g5~Gay3va0uY6G_m)(;BEWsmLlTg<)gCX3;wGLr$<^AmCeB!pl=^zm-GK`{G5v=t7`%Gc3PYPf(IcT9J8}_n+D2{+{%1ogy*A)?Uf8RMJhoJ8Ta8I&|fT5$4Lv`SVm^pf>s6|R0<Li=Lf)uM~dV;)Tdu2=FO4)Ufrz4gIsde4=N+*qFM%z5Axs;T`bv>nz$slQAI<KIIcMv&!N4G%ePxz?hO6cO=NQY|=sRAdIuohLwp{wur!cYZT)NHdU8A@xA>*4D5R2m?aEumtLI-uraHnhuwb>pK}>N;OS1)&IbVfo-LhRr3iT_90V5-)sU3|D038wfp5y2*=o>BXR#)u+*}xou5Hx+#V_$dQaA>)*rqFZMr%#Gvg@9*GA)(x#{|W3#YAfDcDh?6Csif)%O&$6qZh(Ys2LERNDCHNmMNbqh4F9BS$_!I3UOAv)fei9Mtq3?av2@WcF+dWC3l4)9?atPBD{MbUIj)=fY<sjg54mO3aL`KW|D4Y)*+K&8He6McB1)Wy@1a$^<j5h}r^hgU4U%RRqj!$Hn$N$f0bMk5`qtzXH@sh$a8Q9WyC7lf9O$U`Lb%97}6(G1ENU?5u}UbsD9dyk_gtU+CP%SD_u9{f73aY#u9$DUmIRw#|Yau_Tv_&$$0C46^{VT3xF6<0|*cPG`!O0x67a&~vW+jSCR(urkuwimZWbk*4wYM=rHTP?JyJk9KN3Oa#-76}#wq0(3{POsJ@{v`z0qXRywfOA}N3~=OYGT4^+CS6LVI<9uXTrF^QA;~cYi&auAgXWZw2IUnfTfTP*y5M>%LE+f(UK&A`k=^4t^<1Cw1dH6ySJ>^t6P|Nox1C=9Xs?sArJ?*Mfy8)9A2kjy%Sa=tkN((_s;Ie$Kp%l12G5BQu<X!IlnB`5YQqdPDG0boYFtoGvMO-5rBx<qVw#Xhj}dK*qI#RE+p^BEEXP1QlM_Yt_>ckFmcRuT(~~UdIbF8JYSn`W1cq7pUKG2oMCTGPtb&~+4Fd@pO#m^)gb71G@K)t=)M}wneA41COZc<|p9ZyaFngCMoAmsOD#u5uI@~h{wcro&k)jjp(J!Qq;o<oW3Klb@Iv(~gq7WVs5tTkuKoF`Vu$wW{{#EWsmC}X03N5n8xvSKiPC(fNdq|MUJ@7u;GWBp`u7R{iAph=eLXH)&Ker~HY;$TiteYC8(>^d}V3KVzU&XTVj2eT0wOUFKTWHLWLb7e4t%hJ(Jxh!odnR!yRG1+_iZhBFJ~{-X+Ih5Wd$Xw~FehqvLgJaFkN80)FyY*_M0p|Nx<y?C(v4OA9KjXZqY{RxBQK+2ZAZC^irS&`j85!}qX6M;O{h}kO31%N3+Y6pZp@zVi+Z~X{1&OIohmHRWHNEzSGXq}bi|K_nck4r3g~%}gX1`~j$&DmWZ|4u7S#uW-dpKwd<}YH;l2oF=Xz;1F*b3~cSN|V96V1D$t`!C{Mb``_<-0GD#uX*{_Px#OUkWhqkI?(GZsOf6KCOxfVE9Rwi}m(k-1UT_=1eA>Q&`o7+TkTgk~>Oc}!v-FtaHu^B51NE+Al3HlCOT$Rd$GBSGU-mrcI%N9yq$GC93WIb9G^R0%G444F_uLnwr#+!E#T;pKpg`-nqfM)B0dEMx4e&pf3GZP-1|95-EZ5FiqVuKqzECp$r_I*q6ka2ON`Y@-lbXhyu$N_wC=2&9jgFGP05m53x@0yD6Tpea?XmuisA55BgSf~*J6X9>wV26+3D!Oy6Il&FvjF9bi%c4Z_gUv1<f7XBnqa2?x`dm;A`tzpPC0BZWbUx^U!KEs7Q1TIEab|n^{Ndz?ns3px@BJwtM=I)b=LYSZu-`7kDXxo{9FziG_ijIQ|QdGiHQKfqsdw)i4rBd`ji@%lJ_VLloK?fNT0k{*ay+-WHlXIqi8x5e4BUhjGA?FQcPz@6*`PRoGhxr+(XESr^yjWc$z?*-I^NGEc@9QqO!I(h(senv4eS+ylutcxhF1@DB6u|zRi;7&ww`ZLbjaxzsX{tz8PwX+Gb0jb-ZUa2vBHZ;7qua_Yt@GkYijud<zT_C|=5Gn`LP$D1jZO&KQ5wIL+a3uUYhJsMbMAC2NIoDOfv7ss_FUA7Ni)!ghzUO-6I9nuT4lsBMAE3D@<aYUtwEd?&(fo^m@#gS?K6@2dc4gvKD@flu-27`H1`V5*^cb8ZqjL&E7?7S3`H;X&FL?_8(90Ka|7|6D4WC-x^FC42};tAYBr1aQZ_;*3~e16lhmB+#FL~+w1Ez#Vh%GMKD>%3+kZ%6uXJJIg(#G=LCNQ6KyE?cl51=ux06<jb%MGehKpn#66)6xf-(67K|%}lE#+f!)v&}GpOiPp@|nrN1^l^KPED^h;>Q7|Z<-L1S-#9O61tN$(!Y3RRSoHOP7<%-Vjjg^d;j$y?Bbe|f3J!I=KGnPik~U1BOB5Rx9Cv#m|$g4W-Xk_zcLX-1%+Pq4yt_0)M?R0ig-ew`IJJ_QLm(7%zB(W2B||@BZxyO!D3Pyg!K>*4PnPaFBPA~Q2?~sW_TY=#l#&X%GrBtiwbdnM(Wp8i==J<H4YU7Pr{cg?9mqM|MQ;KmU=Oq;K6a4%vI=ZeJabo&I(VUOTj0U(H?Hb7RGy*6Wf}V-Gho!>5^NY9OQt>UBtQpRB}r~AvaW5?f3Z9dJ*L*dZa>0R@~P(v@c>#TrUHoCJ{5PbHdX#YAN~1MQSp1h}<tvz&C`N@VMhpq+hElzxGaW&yD<z`!WkCM|FoK7UeURHqFP}w1&K6h7!oNt;j=kK<vn$rb@1u9zX9U6S)O~5@xz}MsR^KHp~5&0KZlvKv|V?&V@}%Ip5TUm4y+*7UiTW%gf-h?!fH{FoOBJ0gddIQ(|e8ZL*{1Gunb+zIwwuC*^D(1Kt`6Ie_*AZNHV^lEtZyuDU!<X{8wLj~<{)CuDPmTlL7_@}1M@UWu(dD)ot2eG8+{MB70%Z>zgMf;0SB6w7BJxq(3IMyhz~a!}L!haybkS}{+o_f8DU>I>={=k#ZEv`Nz0299FeTA61lOPjEUujz!iMRJ35hZiL?%Jw4ImtVG#?}tKb!5BIscuD-#%FrmOf<Ec#agT!%7p4%jCJMX#D>P%|>-#nTk<sy|8COQ1P#QXhDyu<Z&30LA|BKI*XaO}!P0F-o*oG9_(qj5rL?$AM<fMT!Z4&j?%^%-rh)`|<nVHT(&a8lp-w`w4Wv6W_I3z1Y(N=g)Wu!L>v>IM!1*Biis_Ei9Euc2zU-4UlBx=t+)tQ@5l?b$o-LmyKe|fQ&H;Vq)eDGF<%3Q!P6Of>);#Agcz#FJ8;F9ZP#GTY#5&)Y<Kva+W<A%-UYKp_Sngi2!s%eUn@sTX`=eV-v|0{Da_J_FLNz<GOSR&}h(_clNHTglsh1{mAEM#FtYB#m`sy=TcRGiKt+K5WsQ)BTYM}Tmu-p4)kekf7ZZ)2XjOYF5;bvrX2U;w-GNcVJ@-VC)8q_Oai+!vIF$L`GT)GP1UuD=lS8F&}K$arC79q-Fy^a5vx$8Sd-;;br}1Qg#mDpDGv(N081b8%`mu+1rzb-icv7wglvwZx-yz#whmso75LBaG5`PE5)wXMr&#jbE4md5AGp?RfrcIzklZzoM&q?hw-#i)S|Q>*7~$?UG7$`4<_B0l^5%fsm6A_O$$`=Td5(@Y53{fzkd9&p~Wr>PzbfVL_iD2-)~Ys8uK8!!!cV6-awi1cvrARy1<Lt!(2GNyuJcbU+S&dQ-0$D`?9@6aW(9Szg=fGpaTCdMX;e=VXxq%oAoi74J3CDi=VkF$R4)&eRVY=D=-(P8)CJT_3NM1hvdVKwgBxQ9!4ukt!`cq0Ky6(>86+<%C1>s&h0}KO+Hc280RM;B7vra?B=QymJ<GHo8h#uwK+^<&(3O^=>&WqGDwinmo^@Bz{o`PE(!aFtO%3s_XrPg|$$j)o=k%X7F-VNW3&pS@0xSXM)oGDd7@}zz6r6KYIFzo*o`AwGMFgsHGl25Gv9HgiXU@PNYDx`#o!NWL06vnXwxYBV|Vw%t0FadSfomX^`(t8qLL278>iZ{}@iKIgh1=RfDXGH<YN?kWthuHG6AV?qIEZkjG7+M2AxkU}qEg%Ha$;9YEQAt*WnWE?*5C34Z;VS&ff^P>RDgMii9L=blit&;go!0x!k|dLqd+Nm!+41exd=8Bd@sB6i3~6*mRWxLuXj_HbEhi;yT0#5A9_iMjwJa+8aB2!^h%oWKGE0@{+TN|k}JQd05<sKZ!s$EVub@=(N2)siqLCb|#SA6_g=X}G|9sk-fqr5hsz<iHS;NEI3#;gEIPwZ&9?0I}~(jYvjKN?ITeKk%Cjha7u<Dd}oLJ5rET=&_>ai3DN+E*a@1&R+VEnWLuonZ9ooHU6e0ICI<2S`D-8W@M~ss}*v9frfYR)QB3)G5*$0)&1{~c)nbF#X^v%!ifquW@32_=VXf3K`fMOy~|@^ieb?viJthDABVDO<<G2jXQC)QDyd{%nughK!Y&E%Zn|O#!8MAJ)IzqA7sF#E-aO#Sni8DrEPj)&6{4K%01wsKLtgo%N9@smmzqdZ@ty|gn+rt~<jPZOrP$wttLOQpLHVEljrE<@yYhfQ9tNIaysrTTuD)uls%7eXS{uNP9wstB2}>ajOn56MNKvV0!|>Oib4JqLg&0?rcd9!lmMg?uthMbUeeO~WB9dpN?1qIS?7ui+rU~}zo9!TH@2axFY3rR^9ghXDA!~`VsV=F=N7)gbS<CH=#`60|>eBjZdjuqg$~o8x=5Ek8UFqn^*rWj&wyrV;9yN`X0e;IP%*Qxd-5CV@9ed?s)hgRRn``$!h3b~7%d-b8bv^?khr?Ph2hS*Pgbl>BRzkOD1l&YOgPp0Jv#b%hdAr#2IeuDvm;b5mjpKxsL?VNW>X8;rb>tPXmWxJx5<+L|?T-elY&xaB@xDr+{EPr~p`JkiOaa1-_`bziE7I)xq;iX50Rne5-bcnK3VX898n%o|?2BP<>I!N$g+X;&OrlsJ(}YXCER&hUvMeZ1sEG~hKz&B%#Ba+SUleZ7mJ2A`JN_e^dl}u1slGdZM%x{de0F2@G100yPE)sDpPZ%vN6GF(i)vd>Ek!9+WTy&?c^PTWE@9MWOSuAZ4@RH*!sHwbm{7(2lc*2e_y5c9Km7RJ-@bia-yW^!wB`MUuNzq>EiWtJ1gacBke9ZUhIn@D9R^;S7Yjrb=p5jMofLmVG3fx1po;&N<sPU7yY$6Mcu7S2#Ni!^iOp22O;X7LRyJ+7O+FM403}*1NeRV*`+LC2<|^|*zNC#Ow{JR}??}HV;;Pt`T&7&_CIlGZ70JoKvJ_|7F8HKE634orf49tIF7HW+_F<3hP_!m5Ma}1j{8!dSoHj!f0O?4lES7`P=fM~XLYK9s^}<%d_`fMlTJlrjHpf_`w7P~wz2y24hW`?j$O6ZkEi~^P4g-1AhW(kwm6u+!BGARRs`JQ~|32H`0Mc+kDBfm=LTd0z(mv|!6nUBL{A7VO@`iSHE8n$G*RKR849rq|?03z|16shj8M}G9y{Yz|aH{>`@Q2Q-q)+7A)R)C0Kzwc7oD{U$hVp<pO+CK-;r`3;qw1>ij}s-+SDFj4CGEx!hnQ|sCE_*VWh#0ncemKa%3ZmL^M}<TrQ0D>@QBJ9Nn+>)n3mWn=2ocg$IUAn$PwLmB8jmN0wVJ9e$FBWA)PVJivTZcIJ5v_!H)Wk1S~S6BTjBnW`L-M7-g_|+B;`xG)o0Hin%oIFV!1byt9%yy>OwQI89-bL$e?+3H%P(ujDQn_|rmjDJSsC`oKpu^l(Zpe)R;f<T=<58<=@y`&`5jm?!D>6XvFJ>!-9#XQ$?FRG>-SEl`T;og|ejB}yHQbpSfe4Tl~G<n`&9_lZ;E7~D=h!U7C{t^eXLWU_}}@I2GpLqg5Du%#O0ahbi&qIhwaxpCSLpa3GsZ{J%yUs#en6-U#|DAGOys~Kijs+YU?XJNg|W&Ag=;7m6@Zcwe^)&GB4`+%@*--+;PE>l8xI4MZs-M>M2wv#Z!^Ec&r8vsHJtFp;LLT|k-%!9-TgSTEYb-e!ncx!#ki@yIcs@jj#P4^l@<^x?|oB(jezc2(<S@}QVMylHnzXz6GBl`oxZJi%<a*FlqjQVKd@c!{XzI^)s`%nM<KmV71{xX?={igZ)9Zla?L!1-)@(il^<>#g!vhB5oh)M@mG#JB}Xmvw7kDKk)!m77HOmbgxZ_fOSAwT2oo9F7z<EW|osi7=!hru%a<q+4%IJB0{W$5#De8UA^+>ewt=9z1qu7a@&1=@EFiXT7y{M{XL|Mc?@KYe<;QU7|q{_>6+y-lVG7Mt~&bu~!>6@m4uTg>TwAEDd%8g0GBG|Z>@C`4M$`A8;SC)3GFanZvqmQAx7pWO)2!uNXbB~HY8=a7Ce*w4SmMLb|2$9up0G-QPsVX@=5cY(fdzn{%eiiO^WJHms{?3FE$)Xtf9IF4*`3P?u@G8D3`2*Qc##o(A{mFMh?2!pnIC6{|!MXwS~u-t#J24O3t1KAZOI$c=oc!^FrQfZ7f9dx=*+iN+{M!gC4PXVbBevAm*4Q{6eyX|9JCvOj^7)-lQu3y}5eiv+h2aC54o5?$>lp3>z9eDqYm@1x8tV8W<bk!&g7`RjJ9uHCE2l!T95YyQ`zW<<7t~%;>@Vy_?!K}Y+PuSn-3B#$|+xcm&n$9zL-UhTpT71`}A1FpN`$0^XT=%F7<(}$K@E+i)QDtd)#S17xE*voM-K{F#!#>?=w@_)Sw=eGMBzMSHJ-L79J+S=t_4c@broOI8bLHTie|Dlp=bu#^U<;k6L8iLseGEXZ_<lydt}sPTrZJYPM>D6)VhHGm;-u<gcH3f3Izf&0LIY61mW1$^FAPhjSr3`Hc?C^=jC<>a@*JsfPUWJ{g2E934bWQWe9;Ngp3R3%prr>T-0rz~7D5t*s}I(TB5JgqmbuM$R7K&3)XCO}6}xWU+{umZ%R|X`RTHj{x3!n6dA+DyiI16tJ#*UUC=LN-0iq6w?yAqDyhdd}<Dm$Ow;u1^q}G`eR3Zd23hW&$&zxVLXT_=WQXfT;sggA0`}Z!F`tM~EjlZ~gMiiUNyB_Nk))P9fM!2;6UC^qivLWNr39A06hi@jO@Kp^hkuF_&St2r^Lt7nf?nJ^3+8)MbAf$>h3fauB2TgCa9OAtxeYu2VDz;;iU(_>;8wP(}K0mN4GKNcZ5o_9HHt7MziBu-u#xSd6VESSYU;CIWEL;1q`qp(k(aj7yKZ6PDxxrgiTQl&owwLI7r!h$s+0g%pLM1g1-(I5EAr`+Ux}G+HDC@I0ca)GuZZECOu4h(cupVdUN>vYI+3iKoYkSxMi;DCf9a51wG?PA9QdY?ZEChfya$V{=qCqc>;e|*RxIy`DIUa!)IR>z+9v1-(8Cd>MbhOG1camG(P^}Y0CJLfGuO}wB2-dOAkq^a+cEpwfPFc8SsEd5~MP*7-jueGnZF7;8cyKM0sFWFQD2(3QrqLUX5Y1>)-fuF3$e%k^7~gF(Xl0QanvSh8NT`bbHmI&bflcDlNr~BY5WTD?OTtZ^Di9cfo;mgcrM4O5WhKyoqU1ox&HGptj&|8bJ5u@2E<;*=mMjB`k?wcFl*_Nam)pf%Jce|+W`shl<DC=aXU1S7tYm;Ztj-EJZxPuFJkOvRp+6W~B5McHGM;arBhuxSE?r$4!u{>n?QEO6JRnc?uq)Icz_NSZwt4>&fJYp7F1OD3%gUm5DhI$7#)`<(zDC<Rgub!?k0_6-XS3Wh6NWZ=#208l67GpRy0Joqk2bVs9sk@>OnEYiW=SG4xejAKYfP!$IXtZwWrPY}yItz&B}|)uxZ<E&L8_b5*CBToJ=g;)jQY)xBu|j#Yr95niV4<CtF#IE|7|DJs%n_rWPRL2(RC+VoJGPV$#tR@)mKuJNe+g^qxP-OAA%t-9zw4^ns5vc0j}pL0x6o(3g6Q(#hhr(vBhrPRLfUJt4c$8k)X~7JF7WdBzg!YGN{X{(yWJVq;h&)w7;4wvA<+8%pcb5^KB@N%2ZDMAgJHD#O1bc<?a%aW}c869rRF}qP@LNj!MU2pe>!m3SURoC%Rpz<Z3GTBRKR0A7LHoP=T?^RJ{mMXZ!^)*0EMX5DhNYBBPmqFQSYK&Vf=_fT=_IF&Z38$%vvt{m#{Rmw_0gLG$4;i7v)p!Gw?dkOC04U*tp}7$6f<3qv!ze6+cTo!k2ihKoD{^o?AE&}KK`Xd(5f%;d4jJWA#r&P!WV$zui<7~@Sz+2REuS9*myl$oiq$u`2Yi*kL`kkZ!N8>R=IEci?G2jC?E-AII^N!H;$-8|{eXMUTRuu`bU8idgWD8EjeU7f;bYiPZ+?MtvKRTooygzs}2Dw`1b)1j4P002qxv34r1Z^Iv%CRFPeoD@Mj;>*J(3B}*pV@2efZ3j?RlG+YY)C!DD$&+gu6wv`9oRf9<vlw)v<4bZ9k6*VFksGBE%ECH&nV?AfEfIDc$pt1^C!@?q47ya3ZlB=dq?YcR_1Ngt0IFDEPpb7mBLyavIaT<fg~$Q4ZMRT}Q&`-K$s#!REPB>FcKIR<`cGvqM48i)y!EZOaoM(@LW=F+%%Bu&S4C<tgB&8)un<rn?W!TTqVOJ`fqNNIEW#rk$9&Djpvr3lSC7`Tn!Ju*6dFxyQsur_hh%WYhs<z~z?d8Utnxy1{wB-e(D7fhWu<MQ{lKbIa)s^*k4NoK&)K}RrDlA(rb|sj7g}9lJrZZXm5RyKt`@=+U^4blg;r@9(lp;+r5|*kKr5?G^2V(8%<<Osx^P`Qhc28$?THF%6~e8|_IHWr+RLDALe+~`?68W6l*!Q;aT?URcJfZ~)F#aVCGNavkH#q5!_HL2Q_Ig+l3FlLmGUhC<A5LzJT>k1q*9TUX;v*ONWLZ7P=ku0kai^R&=T2~Jt6E6uy`)vbR_L;j&!Izr6f2`z(Qu+5%Wr^wp6Ht5L-$f6OHqt^<X<89NHH0BD9GYFHj2)NmweTiXams>jEQ#$r&HRpv6O!H|OaMIOFbBGXu{B06EfK=YyVpIg=XX`^w@#09%xWX$kpG-iT2JBqNlFU}YK&D=%HKv718ulyK}4lJ->Djr-WCh~rn>B_ZQDeiUD7j!4N-&oB`j%TRj?=@!fLJ(fm{=EM|3YGvsLp;P4B0GogU3>W2yoOB7^hM$oqkj93S7xFI=JJ|Xok2@}4i=wuccFyJIf#vPOdJF@9QK6ILS9UUuZyiowr$`<;6sTk(Bm#o*4S_Y%(hrJ%_yYsO7(dv~#K7Jk;3RYlQ4A|?U>Wc_d@sGwh|z0Aq6m+W<yjO(C$bKCsVTrV%S#_<<7b#*bcG;{RF;uI$vmQVrl4Tm<gU<wk?S>Rd_lZ4Fy^`dzPq%QfMvEih}ooX0-aiwNsAq6-L093ymWouKEoH}O@C8OUgsjvt`K~wu~Mj=<XWkFse_#!&t8+fe{|d@P+rAJu319^v7xaN<9m`2-DN&yguZYBd7Hr~mO9G<NnJVqvthZrNX_M}aUsL^M?@bt9%OcfehWY-&dOZIK#=8!+(*|wF$C_O8~Jukmz2900$zmL<u6AQSqB?Q(=)=gQsCr<$KZSnHGVXB_cg~*7|?jO-3^t{()~qYs8fX;)YIq@aqFP2ndRn7s%|1vz@U<Z>xh;-8UP+pSV6<2vy<*pA-t05MajevS-7^JQbmg}I-917>mrYaIE1p&0z$jGwv~A;G_%Okpl*S`HQu(<$y1yl3~EL+G$&rWk@6e5wz6cOGlx+QUGF(x8-=xltgD&NE$hl5vZ#DH{74Iis<61>zZ`tHK65A!!x&-cL=w{uHRrpmN=$SuqhjE^s)DeJHSHR!G&Na-;x21<QLT^Uf8aaJ<P=B^&pVz!@awB<RMSLfM#D{QsY$$;?K5l?ie!<aM(P$^2dwMlVi8^Fm6jPr2gqMkUGkD%%aSstuyR9%4Cv`hwW`e0ld{@%{EmWU@hN{w5MKny-Bc6Jqsktbx<wgf9{>1)GyBgtTx64()U1k`;OOScip_64g~cS{igC}|a2FM%0BK>?gOGEUG7T-ZFrk+@d@vyoXs|HHQchA9V>k}BsnjRLW*Y=)HRxuL3|psBie|2#A3r7u6&{9wfgyEyLh6xBFgO;=w0f*vxE^8O%isq|UDMnQY7G!kG`d35#@WkC!gaM_hR`RN$f&n)lvqts&jbEM_-<^UFM_k+F7amhSbYPXpK72%tir<nbv(-l7-m?I9}$2&(WF{7cUMT*Xl9GHSi(DmmWy^LhDJ458h1eeS7_Iuo~xmi4VcMx6Tp^dcwI{#x)YY1QIn`a4TMZWq12*D$7#)lV-2!YolQ3kGTEN?8YN6`c9`P0b{JL98mMm=6OB$11FGmzn&k4a1bii<%d9(#yRdU5p@~12AabYuO>ry9Zdl~(zKA3wAO)7_2TG*f$UEJ{*g*eL*g&avf?$jxk@^qF?~u7IXm+*~E*Smk)yRv&Md$)AH)x8fshPb870q_{j-8xvW<5OA9fMPdS+3ov2VxM5v9dlfQN0f?nz;W%H=c>p^wdT`lJ+LpW~X&GnncvLC!RcJpX(|iO(bZqh$kXPb-*-$2g1{S!7*UK@$PGV2cS?o@vP0yp|Mkfra|IaFC#yOZ)yZjgzQ5s<5E^EZQNboCn6gWr0l0lx+7=uaKv5O1)#^<ql7pKqx?{%M988M!rG}#**Mear385T=H^1&sjD^l-J0&LBeHu~zKZI76>dMBSuZEdV=Zbq&;UjR4zW`fQXu><EH0g-*PARSZ>-Je?nzM$a8AZk!61=Jp*6kaEnCMmRYrW24#K1viA<||0ZI>P6vyWRYIta|)??zKx}Vgg0u7S5%#1q{*7LH{H($>6N2iQE8i+@jku{jPQLFtK_Z5tot*-D|&h6=T=TTOOK05S{bD`I{Q=6)=FUr@ZWZElXFlI{`&wU<@Srw6okAh)lxsQ^pGr&VM%H&8kr#<ME?zKYZJ&nWf*t#yks4f8-r#mScEpZZnq*1jFeu^Lv*4rhKs383};*|b8XT;QPD$>m@*cp*4)xQvzibd2rwbnlVi3MJSLI=)%#wk5Qs1-%K*6~Go$KbV=s!4V~>;ofJU9bpa3W*M{Q-|x^M^Zklyh=&EgGCONE34YKCTgD2pdFY*riGM;j{u*Ed8>}S5ZY8B??IOuSn578{jN2;d%Swb*Af`{@WniS_Bwt+l$xO=IvfW?C9b&b5Lo4@qDhx-gU@MZ42CVdb}%17Iv;p1pa-Pq@)8vASeCd4xXVN#H#oaIsjd6xvcE(WQU_&H?V3{iy?$EN*nNMI8z<&*Uf$(R=bw1Tpf7Yu*j{i6h(Jb|(yg<NW%~;*4m>CkwxL)A)9GfNx!6(iBIEwjS1h#XYmmx7s(ZGMENtSAvEX`;%qGh9Bb}rB^@ZLEO7Tk~PUH;JY6ik$USYnTT|LV-jVa>_P;{LlY5XUrK}&y`E4rDyVJ061ne>;XrmBSz=WU&fDGAC;R=AZuM_i<H=NU?_<ajiJ%45vvw#LykDg%$T-{2>TLObyYYly7&S-{aTK|fgQ>UCsYwKRg}1o1~liywsRtLb&@Mn_}_-Toz&jEW~RY!eX_TrBqH#RdDHgUEn-DXQBP%e}yqfWQ~k0_hkY>6@vtVhfm!y#a!fwAgczJ=Jbo@;QN&z=pmh3bCWH9BrmT$v>4ZGenwohKo!?Oo_%*+fss1Yh04j46FD;mj`Q@1uk6Y4QiV@sgOXNXTMJPeu=C<u2<;WHszeU+|e+KOsR*YgUUj2hA;|6(*%j%fJay-F51UBGZCyuC`(qNA;&^mhd9*gpE5n6o6-){@2L?Yu^ZRAFXUsu@bTS7i$#I9L}itnzwDFT^cjIDBTaN-Y7sAv=iDyy-Nfc+ndu0a7+esT5$_zT30V3i#;7j%l%@l7dqySAA8hlNUHthTrLPHzzPnT&Vyhua3<sQGi4Q_yhIIlJqMuoPktBJ=8cxTxKU)o1Sw0F`={i}65h5k6cM_r22IwxY{N5hQp!yq5E8UCIFZb{l&L_3*zpty=tFmge)sRwp<O;QPiJGe8oYy&wvPEd2&h6^II6hn5o}|7>B!GEYYywRHaXK3+d*u2ym!xFk9)W9(BLC8Jl84=$NJdg90aA(UL@{EWp=q0rp1R@Mo)$%fp|KAUDP7+0n=q)F{yd6t+hQE*8a&NmJAZIYr<9-@KA_B`7_9%@udl!GdnmjITbi2h`=uiD$L0S3qzjx@OA@0}rthOI^f8>M07mwzhH=bLB7HklH#P_#hF0z_psGOn4Jtv~YU6Mto)Z^ATPM;5B8_MVl-q_jdY0rG;l3<Jylsmvh9N_b<UhqVOL_6nxM;W^#&fd$_X_V1^4$kn>#wNr*J<MHu9Xx5hd-jI25`o`TN$rHBo3&iN~PSYkqNLkT3kin4@-W`mZ`>miB)8|!x}I7VOflV4yzIp^M~BT`3k3?Hw%@A%><O;wmN~OiXrJIA(=W)GLRXCL^g08t@q1YLNn%6Sg%h;--nq2Y%%t5aiQ*$IzC=<X&iJLLit-=$S0Z80Ye=VhJs^Nmougqcx}yNKTbM}PR`T<S@0xFFodbcSz$CBsP`n-!gO#?Q3kUoc9BWxAWN5_7~q4?`4iqboh}LEr<JBWC=<*I46aFCf-E@^bw&m{4<S{mP?umk4(naTynht2DhnA_0D+>8$TlGl0NZ28xA3g9k27w23$SB{RclO!@P)?VV2Fu|ACiHR#c9t|vZgSxY;$M!K;0BPtcs6Sh&~|vV#dQo_o{iLAt<Es4@uhZIKFi%vs{}FX4xvIkm?nPy&3e0ZLUY55TO*^!={)x{cnF2-k)JwvlNB+N5e)6Aqduu8OHWw1|0D}p_)T(0TQbbc|=YIVNqH+wMXlDUw9%D0E=-ih5;Fwo}6aIo8hb&r<!(ESclo?Gp4-YzNQx#7_m(;tpkpdNj{1ow|=Bgen6b_QcHzwghj_Ws|?vErcpwqLKGxWeTDf%o{S)sp{TKqRta$Dd5?;^#162mC>c+bz<cPIWBd{J8p=tb6YE(LEg~!L9Xr@UWI~h4hyrvq8AdCDBhz2UAHuWbs<F;}7;-=i$%X`R&zWZ6Y2c;J=i{RSbWZ=5VJ4UGsNPIVl!V0L6R9kTj+D@bj~$Xeb(4DdA!8V@JQ&EH>hA;0b+6MJ5&|ytZKWzl_Fh9|N#`9{Mp<}LD(Uf_ipcHoK{GJsss2s^DFDr`164M3Kw-Llox&`u2<nLmpUuEXC=u7%9$L&(<^+#rk+t1}q{UUdZiV)*>MJ;0!Y(!3?}>6Zl+?_QwRc8_OH<K-RqPBWqoCqL=Fw7IYZ^+K3_u)5XQ7YYyHrJ!)Xb7SesJc)Hbq&wQNFF}evqHQZI9+{2L1C8rnvt81lBZMqKBH(O?ctE&pi1kY-ti^Jj&khRl$jvK8x$mfLkl-z8%!AYRWOJ50*Q!WG8OYPBZ8+p^GKP$ktHkZe$b-Qq{rPW|zXyn@h&a;~>@1R|s?yGtI$<rcn<P*WiSei9k2zd|~ZS=xdNe#w3<QHHC!v*45b#g&c=`CNrnai)WY+Th4&`N`(cn0GARDZdX+_cW4GVAHxeK;@(BT+Ns6~v5-+_V-p&i&%n%<!^b7ULz6?5X*&eTrkxxzp6%A_MePn@KGX%|21%L&bH}BcbggZN+7@DH7CFG8RcTDT1u+Anz7Rv9s$mamNWgbgGOBnhSqb5xP~Nad)&j4}sFVVc8<oq>QEZ1og(Eu0PUvRF7;&|bA8|jl`KtdQ4sS#5R8VU(Cf+a5D~~SE+qA<OPQeWOM5Z+>N=r}rwriEnQK9f*&k?sCG9Xzc@@!Y6p^*8=WLR~!E5n1hpm(h2I<%7vdwO0Irt76KAEE!oy86qu`tv_DLuhFA8XVZ#Rx6i!B1m(%`8p5187<z`H0~mF7uhY};gtx^(#Y*M-<fw0LD$Gv5vhX`i@Gq<!?lgqVdh?J8d&9k<UB>li_*F-r%(WbF8H9SB_-u1ff4q4VMapl0k160#RwQwH$3O{=lmFI>z<q6jjEr_Bp~s!o$N0Q23t>+(xve<8BF3TgK;NHQ_tF}RwwG3!;-L6V0x;fN<G9RI@4eBCQS18YOwT7UC|A^D5PypashP-PDy4%u6P;>fg4&26C5t8a}&2`QOgL1LfnQMJ`jF1eW?v(#h9qp!Eo=ALbir+Uuj>~tB{zh(NI`NIaC|6#-56MQ^0`6evy33jB-DaZ2~6J4Kj5qolYBgw+(!XfIJ)Rk(LQT4Wv@3#7bh;G0$g=oOXW?fRplrW%F1nxrcx$fxIea53%TSxZp#m0SR%pPUm_gU=X?bXc#J#A7vm!r?*fZ%Vr@%dkzOVMEApUu#cgu>8HU&Z#CS0oznID@7Kps8MrUg*l*M6Rjp^P6pJREZ^kOI%;7W!Rrp!ji3sbrKD#>LyJ?SgGUsggB(nv|w8G|w!!T7KT(?6K;3Z1_>#jG_F!djoVXomb(OMrh_6@4e{p5&|QT3yqVW}fv@JKCENHcqjh21hqlWjud<p~X5NErq1q%IY9d5-(oRMaq<+)khz5`r8I40f7p()8OHRq0RyRYeO9E)^9@p!n@WhcPP33EW4V!p0#h#ikitNB1IErK8Ivu{I)T{(_7XI3Gg}8K<oR?DLh=GSm|BYXa?J72rF5FOQ?DV$H6C7$##84a_?!-E4LgZ(@r_r{I0e{8~^4&O;pEFy%L9E+sq;L*Z@Cq%s$tlyFH!;LI#hl$N+p?Eomet2v%=S<+w*&sv^06!K1t!4<4%d{Q_;M^e*W%UW9_*!uN?SZCCTry{~vq8A9dV^U-7{VdQKA(Ly<=LSy$th)->xH)orb_!W3{p{ShP%i1B#w6(Co_gS<Y)E7wHDzm&LhedNFAH_j)wFupgR+>}QDYmPpy4C89ub$19Vj-JK-22@vCn1dyjV8SI;aVQYJ~s~M7t?wBZ(TfZef=2VWJE@DqI7%_uyiDg+SImDUX)LYp@z<{g6LXpV%!GH-+v30Dyqczxx3z*C<$yy^&{K965ArXeaQr!j3=WMlpdvnIt9h$r~LIj1mk!EYcM_iZ}`zXPHQIm(Y;``^@y11FyU`1fP4w9;)h^ncg_y;E=_aCo|~w!6KlXfqRl6HKpIcrlMpsAlz_y8T_9ut$yq93_nMWP3I|h-w;*;=yN5w(;jvTR(jU0C%n#Mr8!m|!)u||;Vzkum3q@{TaXndmAza6aW5y1H!YXCYbmJa)=(N=$B?{}mL_3UemVmjZqJ^8>D3Eu4@)S!EK`J7%`pR$+$sutD3&he;nr2j-(*-eccKf?DrzcXr_%sn+0J@N-&Ak+Wyst?(1zE4G6X4hR2gQOCR!GHRap7OOQT_NIjQ*_SdHR^laJ^m_aBo}DB)p7*QK9b3=Ch_u5yLQYI}?Oecs9Ib+?^Jn3++CPU`-|$)43pI)hWKhBIDx{2HM{=g^xwezA_F35?k9BRfRJJRG=rI>l<8P^*`vFhN;D=W!dp4vJ#ySO`MV5wfBw(q)C`U%helx;C2rSQGiN5Zd5nVPFPAYFGsuD$y3IbQk%sUzX_C*U!6)VuYEJ_17W<CJHzM0#%}m+E~avv6sY#U5s$X%2i?wj`1?<eJg^v%zDa97c0zq#{SY~4ELKl3_NcTR5+SUUC)(m5qKk>?Mr0)ZZ7)va8;+Pp1}o6;^EXm$Y!R~<d`X3g2~5Jb|a7LO7zi35hwWi^qD~iIzgUK??_iGMMDn`D7(vQ>+4hKRUjZh8Y#h!l`691y^c|McbQ@i^>-+G9Uv_0@W#X|uzj+P(W`1IRPi+39;W0a!$Z%VePfnPpoT^$?u4SywvL)YiBFo@&ynv;Cw2h0O0@l^m7OQqKKBW)6IjB&PgC>)O0Ebi(hN51eWdM0mjv=li1B~K0HB9c%4egHoT_p6BBoLBMr0fjUA$?+lozlP-L?{8{jZ<a39kg|htL2heoES|mfb5Wyi+7d>`wk3?~k@9$|Wg{o_@?_+p@DN%PX)lJ*6;hYzNiv2*q2(_T(aC<^4i+Rd<HW9Oa5)CO$}61NNBtHES)K@Uo40QpZg7XGy{rxUJ<sfpa^nHO>jgU)KPnV|MxvjfL)%Bxe+XDmk%azm>{Z=t0$p7$K;OhS7nNoYG-o>>9l%Ht(=tah}Y@ALMdM*P&}w`^|M>3r#qbUv}{d89C}YSv;2>EvD`TMk&A*z<l~jvu7$vEayk(E}HxxCj!+L9lTC~fDO7)j8!^AItZi(o&jN|8a_{oRZ)B8U7eU&C3=C6T>`IW6yS6}zuUDMpb7=6co5A9xIr<2rK<RGMJQ1fy)ro~=NbSvNk*I=-=t2Jzf_SDk*~K5q0vn3(7es1m2=SO7y_5Pct3YY&pUBn@YH4d4|S{PRbbs6wn41i(*<%8dR5W$6ge{#e##sBeTj!kV`nxSWpeR_!0Tf3w`U=0g#b;X#zlcxz8UD$@bn$26B+wS7XP8}i*1Y+Kse=FA&4P2!#3#Xy(+?TQE|rkCqdk%b^bK2^qVZPXY_E9dG{aQRDW8o=+k;1v@YW~s04ZHFo}I{OMsg_D~*G+wcF6Arm~`wrZM9JT>lKjT&N2W4=DceezhF``3N6PTmx&2P{#d&cF(LX+~aanFN>{jX*xq>y-D@Lij>qS%IhGi;y5Q#5&<ZnDH=tIYAvKKO1?rEK2Yoj?-cOb<gm6h`0ZdXU5z9))RbSH#<!btJ5b>K2I5SlNhT=wT^}mxRIgX~I`3Y`+@Ndx{>?p-U&KEg{*bmir5xGgoc1SbS<HjAEaNucu;2{(58wUz`itXl*dOk{3_mK}OVghz+Ss>$dz<T|a2hk(4}mH?ym`vD!o;9wFU<vfm3Eurl4!53YI*3wh)TL?)qa|qi<%W<DIm7)ce}g)z-vs)C4C7Ws5c9{PpD8DdH>R=XeW}?Vv_g}<9z>Kddm;E;@+RXy<yjxQ^$4+d2lrpU|Mb~3(-(w4ZLXX5)$Z1Io`3KUw``a`PKaLp^4OdC~CO=`1&)szXEsF+=1)zXWnq?#>rZ^31U}%2b}j?SnYBV&n-8!1aA-eN-1ScEdEB)ra74P<TLzla&HD1EVWOG8=00KVYxCa^~Z1uFD8ZC@sGXkxfW*kCAXfXbx7<lhxG&Ir~lcPe+v8*;>z!n)Nj^(9F6@0c7%whf+zWpa`U8Cd#+c_vP(vOC#C29AUVDm_xwfmgx`XWFCX82{p6+(BIoBxYP~IN(+^3x_cnSk1<YAh5pVjruC6>ogEClCGhE`rlU)XH^aRMmRIM(d*RwDRrWfvL`j4M}{_ZZ8|LNx+e){xgy05noao=`fXjIYHoU_CNj=L3o9cV&MJeW!7%m3x~AAbDqZ(q**=ig0$^cbAEHte5mHc}jQYizxGvpw!8`_Z^d4%f_fg#?-*)F|A%vag#HrTy;zWEZLU7x`W&l>6-fnFt)o#_ry=04+5)_}5V_usZheq14pGaGM<+cZ&~CHWl4z3Tbq^x&UMr6Tgumnrx15q+>5@E=0QjM3|Wif371L<Ku$Ni^%yyO$gid34E?>t>dJt%v2OL$ce;lIJ775Gd-a7`xce9F6P>~lY@KL+@Is${(8Os@>q=NlJm;+^naEvAh=6YqcW9+1~a)fs!fqSCT&oFgJzTYuDS*I=B}<oNz};K!qT<9QJbl+1CIC1FXU*X`L*anVxdaUm3yJr+BBSWR_}-4{Y=K<a7xk!-FVXoD=!Hf7_B34PYt{fx3kqo-i7y8*p%Mkd%f43-WNQy8I8kS*1YmWOEc*`dA*Zi?+-L)l|O#;+15eoz3F++RJUTH@KQW(cvGq#iz=)3c+s8?dO?BU;ckmKHx-M>cG6ipSE>%IW?QqGwNy6n{heH(Yr6#9w~}>clcUkhM)oyMEK^$Lry$V)3?1HC<|qQ_H?%ST^nmRi^@WR)0N{IJkDg5T)MlR4AQVXCU1Nn{Mj=^8FjoYaAQIw1osTY~Cu&~mSA}uJDBA6BQX$VP=^k3HlPpFVHGgdik=?rH8jK?DEsud;`)!5V44!XSx<+!aSp?0364&n>%U~T%1+3wP-|WFWdRbvCpox**HtuU=_O#oEH9*JxE~~)9PxI@6a%upcIo*%I;9oe>MuCYfx>|BcXGXcFPK==9*`f14<&jHP1I5PU)ja!VGpmC`Z--SEK04CxXAPFg<I3hH6s?sSOz0guGj+_&i2diWy<F71fa6S2nh^buC?Yg#-d>^yN>!YLRkqe2r`>OL+ifqh`a9)P8Eh-`X~h)G-2gffMRr5@8Z}2j9yGJo{fQo%yv#988(&8>M6eDoFGl#8wN>D5RTyfdBA|zSpdbWNh3}(vWL?^euFK9vY5cC8WoC($Jn;3K^DuzkQ-nrLqAf1+3Fk-%VZj5Hc?_|)A^jfVo%m7~!bD!fg6_j6qHc(Z#<I@Fpu)&uOV_3VJil!s9ULxqsbd%5ZvZc69aMJ)8n8Hp8;A$wATKd;Oz5{wlqzT6udkqAmUT22eeVZ(nF;Qp6jwQbLfedq&Ir#dIBlCSkpkoQ@*jIlb62G9GWo1Ht*x-L+E`1~y1XcgWZ|0@O=}dp?aeGCRKd7ef*Az=G)EF=#oIP|l|lgxxg!E+0EL;|VkO(AE@SQa@+2rp51hQRZ7X{Lr1%eX8@T?KXlvxJY8MQTDo3KWMy2QO)wl!G>}AtrO@wOn5d6kNZKy4JT1<~(T&(TZI>1qHg~CM>sW_-7M?JH&`W$194qu>c1?}(~(Tk_Rsn(6qO>VS>f+%SV&*Q_YsEEr}NeFK_ov?>;^eV7cY$Td0@=n&c3uRI8eumXY;KWfwCu0gO(=OC%VG6snYm8knFMZo~f*b~0iSS*gi<YC4w}sp%IY@4J85}GGFoD%fvYedR^s)iS=O}5kzFCBQ7#VR@qe^&@78uQ_3-(*oAX-Hs#OA^T>mVn6kgj=xlrgQVSH@Yy%<qHM(K(^&aQ_X%nI%1b&^pxcxp|~5^vruIc<(QNuUa}UjPIMYp1YJtxoPd*@tE2?@jW-F6Yv67%G*ZXouTZjKgCsqz|wlT-Q1a>p`OU32PPP2O1mfMp+UV?q1_0R&|8N)CUkgcs*^|!1WI9LU;#!ssrkC7p%HVZL9-qDE`o8+`Ei1z1ogG7y8t#I;cfSe{NM$WQCxUBz?Igb_7Q9ZX5(zX|2~VNpxAyYe89nX(>`zL57584-C{erD0%(3w%;b$2wkwuKzK_v^cMs)i*oeBbO?K@iI9w;l>vJM>hjGd&H?MVB}{odG2=YRFsuYP+Y8q$hFRB>i-AMJp|9zL>I&>0e$7@1qhk|RausVGh3;E)Gz<xV?tQ4=zP|o~sZsdsn;MG8dZ6OHplA!S@||0G%(F{TqSP(RMPiiJL>Uov9jJhkl45c&X71z3rz?pA4Kv}*e!YCbdjU#IfYw3*Ohq+C(F8L@TW6{=x6-`#yDB)}#G;O>!DC2u7yMa`GQASy8-Velu0oGFQiSxlSn>oS`XwN*5cU8&=Xl|5rp+Ubg(3`Lc|;mn0j0;7I^2$3zV4&$hh(j>TAnd)2GJ+@9mrcmS>e14IUM6a82fGHo#|@$FbYsWooB#jQPtnOc+ongF_H6#s#?7=KMl-6lv?Y}dikzV1`Igb0(8pvj;}Vqglx>_6pph@cd###ja+DB-ctj<ABIIP*g<TZh#nlId5XWQQR`*3?YlanU>QPHkwm6CQ9nUsYe@}p$|9%cOi}!)6Xm0`DHEMqc?R+sk1UvX4>=)H&`zChX#msC9h}f;!)8^n`zRbPJq3_pGu&94Cuf~B>4bIEgWjkidQu$_&x`4ms&N&jm`0g7${TKg(b>ktYS%G&^ix%bS|M_ZhD`pH?!`LpSyx6kmsTQZV#WKscdrak2<Lmz1rxxX#yFjF*v@1fn1K~aE!=YsiM~`Uk-k63LKS-EtXHwvVNw(hj4V3bz66wtLd>mP;FqnJiXIP@OCwLE)4NH9%s@P3Vmvm{2W&^DYe6fr&|>aQtJFVf=b^&p!MNFr7M=NGqrl=Onnkk3)oR96l+Ycm-W^hF6Iu1^iPn(qJpb7Yrg=%~gAWlaCD0Uceo<>LaDd^q<n(f>BAI7|DWhhxZv*KreXy1x0UI<PRnLi|;gGuSyGw*BhM^5?s0s@=$@86hZoA7UM`nPMXoo>WZxth$^2K7{o9swImc$GDx}wUvrWU|{EgNo)u5x!->cleGwJiS$tq>@nxA);Typ!n=<rNN>*Yw<bylc9ed;BD~GoLnC2OC|K_LinCpODL*P#NwTfdye>ZV>!ZMNXGH2L?1&R?LX95~%!76ZrvSt<r?mQ9Zizp%7x%%xZC@st7~`dSXPbYZkRYl2-S@UX+3YruwM1f>R|5SMzurvjxP$OL;a;MWu?42eM!`o9?-HP1=UuMnh)?%uW%l8Fg}-UE9g2wxFg9qz<*Z&p27;R(QSm%iLF2rV~e;B|H-)dN3p+);{F%CmARU#BF>sTFri~^NBQ{(EBSLPV^qRo;NrQQ_!6N>_2Z<!%je09@rHX&0)_1xowkme&iOi!YW2DB5B`JTXYQqR(Dm4@@38Zu1qh@D_vCzm+=uPs+Nf*GC554I$OX|Sh@BY_DBx}QwXvrN9d-z1*csnYbqrKEPUN;9Tk$?hEA7+Vt2PB9L1J*9nDaor<H_eT~q)JXT*{GK0@#Ro-l0Jg+UbTp6inQhOFA|kdaJUShqrl^a%97x-M$S0ko9qOG=4#K~Z2tzVZ%Q6@ZQq3+OLn81=X=UGX1HN6*Oha;DZ_WSAxu#L>2FSJ*mtl#n_)nMMWY#cn`!4_u;|y^Q)&0C8O`?QQf6=0Fou2)|e^i7!F9ebzeiE<%~fvh9WiV!T8RXF_xOFpF-RMK1&P5M5I@ChpM#Y-5mY16>?KC#wL$@&wSa2ik{Om<rV)h7nMy9jCCN>l0ul#Zti~mbv;geROA~WkeHzJ{hqUKQ+e4qw64-l;uVZDASr})YCtl|KU<;xX>e`7(1||&=GN2UtL_3P1@tIW(bKW+r>MrMGS2oh^GOc-s?3NOBaRDk?AIK8Zi3v*+xRPdFU&R*H=S+3G~X{&>M^{q7&fDlk|Dgi#-8ODIcs+^?ON;9<^rDqS`!z3Rp2ra=xE+Y@$WAK3oYlKGd;_9>@w+YU&U;oUv|LWX>4)N@%s!%G!2xWkGJ1a&Z0r`&A_RiCD$hs1dIbAPb09*Rbt43I04#VoKF!9wDH0!maK!0_vMllk-FMA@`593wCsX#_m+JOt62p3i@zR3_ihC!`4yu6{7?yI+lIKq-Cv-2Szr8&&9)o2u2stvO>qg%|(E5j~TJB-8-<KO~U74c_nF`C)wWx{zA|<PL|&iv-qn^$z>$EqS6*_fw$gL5tcP_BIHX1yqw`LdSTN|VXNe<9!g_)F^{#U=~9t*EOz6n8VeNlQAj%LSerzJkJdKIntljssi^rOC$JgI)W$g5er><|;d}osRt#L^ZnH>W>f|B~bO`s;A(ajFR!=C9QkJkNY7NY)Mi5eHk1pX!(-703;K>AE0-S;S58wUz`U{oHZ+d-^UrJS>VO#f6FRMbQSvUqkCk*$Z3FVThzYbafRys01d<F(RCyk@Vl6hK4X-2RPcF|jQU44;FQ7zH8BlVG=^%iJanWjB-7F8$NZh71dWGe1!e`jYNnB#{0m8j2-R_;O^$zr&4!mWO(sP#iN@=OuUC8sLa&0P&bqcE8;<``H1*)u(J_Nb4|v`@ok3XrBKFJ;J4D3L5`TXWnZ*&?pFRKqrR!x?4K+D8gMC|D%S8?IRS{z1Nos}!-%ne1hlZpMKyBMJ)s!+fg8Tddn1-M9c#5!Q7{RFH}uR-&_7-AXSPwPkZ6IE`|yHp~X@pzEhCO=6vy-P)_k+OO;KU87)oNj#+1<09B$%44{BEPF8EPA_lazLw4y;2HTa`*yZoW9en#_yn!^2r*#PcIUprfKy83t&<q?jiVutoYpaL88FEUEr_wqU0cS`?e1OYgCthHr@>;$dRba&?V$%A%{>x+l!S6<cZLiXC3WY`L6Ji^grEzCU%u`iC9Vi?ycxD+-LeFg5H~U+txAp-?!=^x{&Go`MKG#PflbZsRY7o40x3`u=nFwk`%5FE1`N4nB50K@J8L8H_i6XG3-`E9xqaFZ3XU^^qN2umGG2c<0GHbhxBe@Cr1w|lvfS6D3r-|2ZLpf)d-b+9z`tnCpW>k$zD-(%V#&NUUKgiN-30_q+wvt58P3Z5Q&lS!bW6|w#b4reY4oBYQeTb)6(jL+B6Ok^V?ApH#z-SxW*Fh?L8dB!CWBH<-J^l<vzKO4mj>$k?_i%Lty!P622M|krt7K4Fa6>y>$*U5Lizp!5Xk;gRT#xUM~b<<zsz}onuNgr9=P2ex293Kq7t5=R_bZppw=O_YULC7cF5pjzvos+fPr<@8Y8TKeNZkQ0Wf6P<#C%fBZ%dC5YdVB38oYdA+iUHJ=F<ZP-uaJUeQv+kX|hBJKmGnDeJcFnG>)hBjthGwUFeYs_nY%rQ$-oUJ~nJ$D^7%8Di^w+tk@z<i>j7fzG82Syz4A>DoII=Zg2ggNKM(g9}CVZHSMuQZ^_O5yGL7iUe5TB?Jq<9&R*hMT9UYWDrHN(2cXf9ECQBUg%&QY9b0EW1K|L_dbs=pYiLfb-_Qs{`BedtK^RseUgs<`sN*#zxnO~FOvcEm!%K<V(k1*Gj)CoIh3RlFs&`Q6U3s8z5gQXRlj951f-xlDL=UjLq5XY@6HKO1~h^oN96|uGVIl!<s0;c<O;z5n9vzH{%Y4$9lUMsMl}T39C7s?7d|ZL5PHtgc0KmBC}dks%L$RL)>-w*h`-u*LXS@>;VkqVq)RRdMuKtAHMLIxcZ28<*yoT!*y|vdyh0bEzUZ~_M{g*|$@<+3`a)ub=yu`7C6;?5Dt$z84vew+sAE@Q&ykJQlqm2boxaywcfr#J_X|I0UMRz|S2;Rm-*@U+q3@5Z2cRoE2p~qG)glQlLViKSS)pCzf?fq=?T6>;Gg6IbRv!i<O`?3FfMETY(AdrBMRED)kU9YF24Gl|dMe;u&k7IerJK#YQ@&Jd!>i5DD>P%s!QspsDuoo?(z%uo>%f=iK0b`b$yyolS-Kb2aFG=-><eC*)N>yZw`xqizY4_}DZ&Y#L`{{~7i`TIhV+FH4T*VtZmay%3G4+>HNnwvh(r~tHQ_-45*h9Y!Kt@VDn(7S7sXKRiZt>%)BbdG1f}~swY^juk%Agks^VC1ipz@RTbxL;sqc7IN(FPvKMdnPG&EJJ<0J%2RD6o1twlW#xt3HAH!<=r#X_&^GM~~lf$|+Jfo+6PSP8lwyseX2Y9?dBEUkqLxIW$ZdAw98m&B<yA(9SLy8f7(N==gl3!60$$QHIA%Oux1w0U-YV$^=E03!+~qxG??(S1k>V+5706*_A7!S^}E2a@mNOzUKos-tTOPJ!N|6R|V&I&yjf1YAUs@^OSpEhY=wW(W3t%}U5@*LFhGM<!Q@ik8OIU6hS^bsNd#jFiuf!h=XRsai24dxUkd0=;xBhH+&4z&W^6rXluYIQNt-J((%#)TBblW=&I5t7rjSh^VL&Fv1lQT&TI;Pl-axAZ5hymx#zMT%l8^3!mtw4$(p<l_Lp>Gke-rz0cVW_aF2M6T-WUVT^6;`io1N6REl>8jF_QkA;vAsQB|+pfm26BI%|W^_0{=A;Y!HT#4rwbr`ZgU#R@7mo?<{fO)pLu9Nlcc@)Oa=KV~ITE$SXiC%))j`&v<y;^HU^W_=vPV-Ul&K#lAfhOyi!FT*ms4hJ)5<kZ}gOlpD{oKlxn4S|xTkhtX?}p2=4!S!fI%OR*FDXJhO~$Q*`?=Q#>We`*f>W{{llQoQ@eaXZ@nMYwNJ2O$0o|E2pRqd1unf15{jupCu5%A)Zg3Ge#`26tAAKSB6Qy*xG#r*zliGfSBqLyEb0Pq9Rv3W7+}TX!OWgyqq&l%NV8K61qUL#dIfch!I|GF_kR}urp$ojOigsh+dt^6ZiQs2)OW6Pc9*mHoB}33YxV1!z0D(@mr6EM+Mlwd`X-BGe(~>FbPg9YCnhx^3gw4yE(SR=Z?aI~Sd+;ct{#;$*D%217ntw%rFL|HVP<Nxn;-=9B=wr&@$d9rbH)~;gi{zVb72OG)M=q56QRJl9VnvKG00nr@TA}X)NC$r7B$`Tr1zRp`#DN*szYW7iymNTJgpawHjd9FM>Z=7BEJ?56a0xq;(N>x@y!HyP!#mMKC;<d4o=X<p{07=$_i^W)J3I%yszx`jA@)!x|DbX+bWr-}ZPfEQD#=HBD2qX^bBy|7N2A*RcZOyOKgiFamEJf|$%aCGCyi_!%D^nqW_&KvH57U<%%7C%m(tLU2ZIcS+K9|PWUUbc@IIqUi68LcvQ!IDIM3FZCJ63t3GDl!kx8wr{|a=*GmyTkYry6(&_{e|Dw(YrtMR-ux7<c2f)g>M{Y87<$Xa%**uIhXPt_gvp~<0BtVBZE6eoFwZ?R1b4Lm=!GW+eeL35^UR@AKpZ440HAia2%g9gIFp%CV<HwI}CmC`R}1pm7F7po({g;|HTtyJ9P^b@&a?EX)8yS!HR+#1@bVw+RQK*+d_Da<n5!a^Q-5@R*8ZLKoA56R)-n5OIQw6gk~TlIo|A#$6gjuZymGDTtIwhQw)@7D%1ACTT1+C`>MqnALW>sM!Qy&Gv|cU5F;heA|_CA4=zAEM>cdRLk_6@31#k#8cx?6q6rb=07#TEDh)=yI1ob&ygK`3W(7xvk#Nbva>)pa(r*MOHWHT?g3f7+j*AT)5<nrRfbdlN?9M8IrJM)g*cSscrK|)rVv1fl3)^^xBqo0~WVFn_Z*nc8#SjRE2rC^0O`qan`7b^o|yJ?k|pIo4}H=bqW;8%mTmHf$BGgaw)9--hxgiyPygBm3|nRR8`>`=?OL?$yl%oA?L>I+eEuaeiEr52+<!9gt+f(-X&}vlx6S3ag0Uq$KTxdYBBVNSBLs1v`n6r65g(9^#PA{JS1gKa2vjgio7U%vaffz@Ds-s3e6KH@9<#quHiN?kdUYn6DgwWr`tvz37(*$cR!9+Wj+Y6J#2F|gd!$4(#=tp{sHHuObyG=RZhI*Mr!`KZWM#q!gCxJ{x>ba+umn5g!-p2^Vy}84LEKZ=RH%bYY#QK&$v0K-f$v$t4zz?v3ph4FtkrhdJa!Od+<6}>4}0%HN<-S?yR#qgBa5pBAz%Coe9t^8kS3cAvAqkrxDd>p@KbsC**dM=>cz7@Gzd1z4xOpmd$m`rR=*lOci*aNh$EWrw;Dtp15IF^Uh8O8kO`yIEXlYep?s8PH3`kSn6`mJhF_0(#+lh=Ow8NzfEYoJfY_XVez7COermhwbX{OsVKEES+1bOUhmPyZX%C&ba<Eb#*)L>%A%b}wJP70g13fHySpBNGw-DzJ5`%7>Itz2c5r-7!F`5h)7|Nxp;5@fCh#J1x~^U$JQN})VFE#eI08^GdV~^in#;-@qo<#N#rNwXhW=Ra1v7OSaS?tk936-EG4oqN9XOA)d@GdSp}DL~KMaK{U`w>?fHVM3h=Xw!8Ym#*tI@i0lRvpiEHP`bor&opS6Nh%E<`<HwfUwH%@#^2{uzjHpXhN3da@EgaX$;?2HQ=pO`j4xjR0(9zJf~}wI`*}P|;6HPzgYqP%u3wDqj7*(u1eKGZZQ+obO&G*cl}I#0m`dd@KU4wKKNiL`%)IIH|aNk)VV(mq3i1X>(jYipf-}u{cr^5D}&*j-)W!y7Cpmheb%)n8(Gua9}Ds(LZPij%bC@U=!VhF1W<7nkjS!C{4*q=Xn|nJWN$#ur1p^>l&n?GsA@Qo>`q?bX}k!Q1CO^BcA5o2zp8T#jleIOT+?C18UYn)2ZoCG|XM1;vQ^#a-~^JA#=k0z-aCj)2S-BV-moCr-U5d+*AhLa9D(t+aRx^y`~~Dj!rJ_V=#~My%hwzddHVzm)9l199Xw5C?J_9#W-!CC^e8K{yVb{FXcYZy7kGJ4!Of9SB2N|tOH)6gmlyh4bQ?B6onaf>GoxYvRvwJF?f?|WC4U+xd4Sbk9&*JZ6Zy=ipmtq`eDuy_w2_;ttx1}cbD0mTD7`8d;_&sG(@I&w?ys(zjP^Ys<OWICPTeU`UZ@?*Dc6>a$}%jCk1R+TC&Yk$hHt;3GOFo@asRBQZir-H-(cGW9{nPMnML_O8`P23r$H=oGM;M)!SMoxo3c!#tF~As76>*%i1&m;Ck^h;YT>-zACdUM1p$%2(A87wevz#I;%=OZ=vuKX|6IZmd4l$=!A*wvkKvpk9v(49_1@VMK7pa{S>Whlfqbs*yxN|1Vpj^G93NV+JKtQIjJf8cvrj4ztyXus1%1JDHd?#l0A0DLIZ{lo`o%>fy6VoU-#kmy5^Pc*$`QxxIL;<+UP)F<7LS7^`K@_35D^NJaW+#^`*x`*T%g1@N$;peO@}_@-D${O!6~mv%5^3m=;UX6#F``S?{wD#J8*~gx-imgh&|?Z?lp6VGaX(B0{tCAHyChia-KlQEcC#M#W=u(RYn`xS1XlEU1Q|bd-N%^J{X%BCbN@_pyS(f!7p*&8Kn5d1Exu2nqlr%^$<67FYoo>&19Sy@=L$bNx2+u2u_&olKy_$OUu4#;I)cbOHB3t(S5zfmi1mGS|vlhb?#pH~;L2ox?5o6rgD9;Ksyzw0*KgT&l`}PAM#GXuu^p@l*0@<5<D&5McflC+5<>iKNKbEW`ewbOHyQvdpO5H0=f#xDzz-#%2k--%QbaYfnHGcUq^*+0)d9egb_hz)=rU&8{S|e5tn0X@@l8u?3Gw#wpVA7+2;8tVQSPjE`+tH1Fs2!mENqrmRh`^a>S-Q`^;&#{-2cv730d-`+avC(6E#PvM4*?VzTUIEJA2n@;tXn;B?)78x@wkJcp_D}=v*pGEso@U|NjC}Ovbe$oYEt^%1=Y!p&@tNM87pu~v2*tPT@s(xESCTh{=SV+bZp@1MC$b>TJfW>|-+lx>rzR5xXJcon~-)D{_d$f#&{2TBNMOiL@bY-5592a5iTGh^T-LFDZ54DwDY$lxB-Hf72I@(P|%QApb3P21npT1I+k4c(Qn2gO`R+N84i0d>4y~(`T<$xF75F|vmld($sONX)acsF2UNx7eWwF5i(IRQG6dq5477HMj}tJh_Dd$+p;_OH1~BK(%3K}T3|s76Oez!>RK-M!DIid!v@p&niIq~*>J7truUjpd6WDN3g>(c-F7C5jL3Iw#I6)ae-6fI&`>PkF?&n%27?C=n^_2j2uV#4(h#qZg0$!RSV!#z=Yr<U*J$31PeF8I^VEIh1-P|3&6GR30#PO7u=<PL1pJx6dht+3rnJ`Xue9KZc015dfrOk&31(BR^Zev=5W~8b<XvQMCECua27X26jsvy`%-EAwnO{KM9<p*7;L`#W#AW(`*)CDp90XN1YIaFh+hoxC?ox!Fa1B#UgIvVR@bNHu6!gP?Tr|&_#D$E^4;#Bb=JbGI5#<kE{Cq^BN;d7xXwE|M7nRU+#x-;!=BKro%$_L1oF~6tenm*L=H#QSGXb6TN>4ufi7XNo)Isx9);0U5#QrY(B9%iElU3W-h=C11YnxWnp8d$BfflmFv8F9npiX@cTEHZ4HTPz~K+QPL!mhFP!S3{&|_p*)CiElc}JT@&2u<Fp91_spMT&qRrG?^1U?e*cij+-jebD1DC@Bhv_i#K`1j=S=Q?m3n7>HVMMh_kvtjWvOvU*sNrsBXmBo*!~AWV=?3!4eIH~Bd1W=^U4XV{YX2E9kvOB<QXbFe=hvS;eSS5+ynh9k`H)w?{`mSczSNW#d*!1n?nc~S@~O#mF_EO~E2KFSXi>#p6#p!2M!Ck%*bQ=-@3$jGjJJ22>mrtKTDdsUUMQ_Qodw6c^N+m^A<@rv`epJI-l{*u^S6)lrLF#FU-Ai(+V-DIC7U9<MIUHfJhLx$gNh%R^Q!F0pKwW~c4ba$XL&1C*A<)L$}L#Oj{7ji9r^P4-Pez9`rskd%Ir=@txZ4I6;cywM=bx;42`NOn#=5fOYw0cw~+bU*ITBL1_NKKbJ+}G(Zb<tu`7*w2OVSDn&BR0Fq$C@$N%#C4?lkQw=duP`FE#d2RwN8&$er>;OK}Ps%GfbTi|ij?Kk2+IFjzPIcILAdozS;f7@HUZok&x)~;#sFW^i?%~Y9=8p)9C9svxZtY5#t;={vVQ(KFUJmt6r>?Kx3Ssar>Bit?{0GY&$O2jWQFr{yHV?xLylF26;#hfRy4rPo_05T+^eh=jV%&()*wRSm9H7h04s=eZ!X5?Lg+mxWdsV9DnI{&(;@+73B#EPJIOxbXmKmGi}PoI8VugAM}Ppz6YV(ngBO*Ybm*6!mJF$0{Zhft5BzhEgnKznVbUhW{AbEgtFF`ART=saJF0(i|d$Q*D!An3=G&!WEUIyHUI3pscL4+o}n6Y~z>I;urS*r34vwM4Sb&>WS!rc_7O)TQ9&S(GEX?X&OwwqA3{zos_zey4$#i}C~1eCcLtvz}X2Ta*{Xil;1P<O`EVs)ci)uvLHoPO>HuXS^ULQ$%@b<|RLU_D}p`^0%STJ0xoNnhR#UA5F5$E>K3lQ2i-xc+@Oy25PbE+J6vZpjm{fztZRGBH>c5_T(iq)4C$&S~yIsmqkXnG&IvpNoZg<g<RkfoE>qa3-e1{#;AIPE>+baIUU)9&Un<n{q=hN<?)0pQ5m4s4XMndsg-r^wFV}>&LQ%+B2*simfEa~Qm5D9>CNn!+E~!)&wo5JD;etVLwyb8QDZL`J?fPAe7k1c-1c%&&6&DnvFtK^eONCSz60&0mc2)~G8Bx*kdJ4~?WN6AWth$?!*mKe5ehH-W$on7OsqVQ)eEB_#tDhqOUQQs3k2*mypvfW)&2ACPXa+q{goY}snFY1E5QRt%eT;w1s^V!z2pKpJgO#>S<DcX1ec}dIYMknfJyhg9p7w%+VCtl0HiNy)eT#CC17+*tQuy5_6`R&w9(h?8tQ7P8Ll?uA&NziRHNIkSG23xG`ctrNupEjF2r?xSYOOfZMVe>bzh?HS+vy%_$}uMF~D{mYNzJpJPbb76%2|-u|EbQP7w6$ePk%frazW76_?^1o~B_lhzNJGj1Vwl{|8s28Z6)VysS_AT)3farhG}0TA0LyS}lZOAIdUn)z}wpdx3F%*jHQ-m9zO9v7^@ss>b#_v~vE-^YMIN<$e~(%UU~Zy@>X3x6(X~&h*Kt+q7+>z{>(sQ4Y_K*H10<i+5bsIW2nWiPaT+m<|If!v3XgM$(4);=sEp1sA}VcdFVVLILcexErjsbx8xOM=-zb5=0LQJSMzv&(-cmHL*a`H<m<55-*BF*oDDVgrq&xQxUVhygUUlyLDi*sAvoV{ZJHa?`stwQu^v(E0=Srm`qC#`|W+BGE&G7ny47MbFr-6{Z9S<_4T)FSoyp?dZ9Q*T5(QM&>M8dtrLiPZ_MUY_ub!PUf?c>gk0Nx$f#wf8|b7YRg3Y1!HyYzb)>T6{Vu+(JeUZKQigcA2o3tLb`-2k*N$z#KK@#OFydj_-wNh{{(yc6Ow39YuJz+uuUu{j&*snwK8_i>-va6-`U7@gol_#LK(jsILp~AiT#xT}cgStJsllJk25;-bCN_fl`gNwGoEZ;_*?piFX1C0QI1!$j-*}NxE$iI_hk;Madfeueue%<0GV|T+u~E4@mNy6s^8K9%SgFMiBI&0MY3smV&Ol!nA;BV*?HKSuf=j|-hjuj}*f_{cI@aYu4)u2O8tE2jUv}&}*F6mpGM_85UAv<WR#HI*smHPaE=u_`MnhVsH3xKPny(_z+T(GF+gBb7k50~P+psAjJ>0`raBi(g-TrYy`3;|sOH6&NqAzWGH|g(VRu(xV8<fYqV$%v>VwzGlQKa*hyEAq((VOe!ufj`=OfBqXDymFHBs0)Xg954)p`I_P4YAH{NLLPFHsBlhzE7^xc{{gt{J5|hOcP4y5(2*OQn1?@u9$1XP7V~*O7i}jJdwKg+O#8?Lj2R<(q$Xve6sYsnLdaS-4@h!u^kuVPzH@Ry%fe0wn?-PjBvQbI}vWCYj$1Ppw;I>hTclPEq9U;<;-BHySM;%AiB$F_9t^~b(c}@V``&c_6*qFh%L4&7-fuUXd_n^rvoI<gJ!#n?iJ`<7B<|Pisi0p&t8DzbML*bi8@aB!mk)90&gG$EJc5w*CelVnB*&yb#Vmg%*bXO*r6-bWULe(xQ;DIjgai9%pi*ntm9p1Jl>^5>vZi`+Vdt?d)5_%99m6@qHp`A-$Pn^eZ|JhQNOND5EV!qO<O52xX+qw+a_9y03=Qhrt(~-b$~-ffX=&iTyw1<Ra4YE6x~>ZMD9TH0ucQCbVEgzs`^t+1LJjAqkQ{B>GbmtVi$20X>TROP$W9C@b~qW>l1q+nRNO()j8Swkq{ujB*7&cO3AJKl`ibd^1vHmCoa;2z@`(F+k72XS0i!oAU-;tXJG|>f=8WF58d}2>IyOg>(~QJWm)?-prVjUDs=^Ufi*%SOs42w7vNiaTlLe~R)16nCIY<@i6DP@i!{F0t!2NL`^I|V;))76cBzN{45QK=FM~qRuPRULFv)G?B1#~v!o`2&IdenV3-mE5PhP}@GD(#!V*nI~P`HqW<yj&Pb@g5~9NM*0c~=q>?2VoUIgQTv6MdYqNmt}sUzyWlSQgSYmCCdm?!8WW-B>}0bZcMVBRJHnxv1ge<fdYg)H=OxtRp5thmsAIgERv8V=teAb736|0KHsYrXF)Tg|Q65LkF^$20CSMKMKuUkg`w&%!|*~_8o-8QCO1{^nzU72rf<9jk6p>CAg$4_3V+iREMbS^K(#O>GXblp3f2VZ38nGGq2s$<)uGZ&AFo^K1R8W-F$`kZt5%B=mEe^EB+_cYa#F}*dYP)TQA(Z`C*k?S8eZ=DZ(uDnzrwL_#T+A#Iy45;Q3O~VHu!w#~}eEpP6S8!YlIWV85Z!JQ~-11T<Bu+)>tCvWs7cO7Va6uzvejp$C+92=9Bgr0x{>CejAWiQ+aQE@lsi!aV>L6|9=fZA|zA9yhHVqFb6wL5beRRW5^$T19!$@S-d8Fjd6BJ%MbCXhrHXNQEMq2H}8bzHZOJipA}b`)%lR>Y!p(vTN9CJ`$JRYL9nh&^}R>zByn^Bm+ZW6V_GA!=%{X9D7=iY&TX<tiLp>+LlITWBfS!37Ot{X3xsDv+LYC1qMTgFw(;FxJCwfn^N}J48pwu`b#gffOyKC#xeSZopZ7Jf_Y^PPgWy@zqmQF?4k(UaxU9g<@$4S*lqZg0#uK;fGY@Up1=OW#Ub<9+-Xm?zeJ4zVAV0hglr1dV1`OB+gu0RH+O$Dcx3O+yNQ5T;I0wL-MHB0ec`~TdcskC)2i4o6IgKWLLY-FJqs`}0TE3&oi=Gn9qK4mC$ONW%?L(W&XCt9vYb1sM~NvJeKXZ{E~Ob&Yst`O7D6hHQXZSf;YV}@cKTL`y{N5F&<O;Q?(wmk&^C3O5D}3*kWx%CD@r_lp~%EInKwyknDe5bMG;we=9sjhhB%Yr0nU{7a@!zXssmX^xj@9aw0-EB2yABT>{=_9XlRE)t#MP|g)+n$sh7h)g@ha1#m(3K+xNKc3u<3lW$%OisxCr0fN+5k{(~YFVs=pZJzoVFw&<*c1N%b1N>UbKP1vpb823QvVhnU0>?m&><&4^!iPmm0vh_N!C4o(H5W{u(yd0oRx@Y)I--obefc1q*SE^QWn%UkLI!_@@Q<SG--Y%;glZPE8CN(uY-&mi~dHojVx;L-A@8v8O#UEKOOhsfV#iQ&)k|*ta7%s0vtYZPHhf*YImH2=%lVa!r=t@qMt4KP&@0Xfnr#YwiJTs+e3y#}0b_A^o%rR<NAa=5f(mMXDE7pYVIy-u>uzxUyL;;THzoXa+CjMMCy|BFtoLU=9t(A%0V&)xzk#1ViM&BrdFQ{wwLno8Kb3%1KCeQSuXfnlXUB68w$9LJ|27B96aAKswr`24Ey&pG_bDdeOCSuU>Hu~3^aw8_0+7H|X|1-k5VagTfI(>0NnkUCr1OhiML+S~Sd7a>#V6<5GLSW~zHofkm^fV+YxZd`DwF3o2*9bq2<%_|{+Pcyd#s_3n3oTyDd933ow-okn$*OCguymNeH|E?{4|<hUdcq9|XgpS#aGk@Vq{%}@9<!p1LJ7HV4y4R}iqI|~G+(+=_?bceEYlER*`NJa&fCcQ_|as%U9rI~ie@}Kd8QRC+C$iU)I&IDngpRoVdSY{rcgnPL|XM9+50)elyYrN4DxMe2e$UEDF%%q*WaOmf&j>cO8ZK>=yn;*o!Ys?dp1HZnd+XnnR{^5A}A?J;6a=&%raR*r8~f}uC0LyR!W{}P))AKDXHp?eqQn@Sk|S0k2Ayg?6ODgqLqqOD#QcE1@Vd#rNw<gwxz5zp$iALd#?Mg;wal|T=Zzxh;&$Yz@-u@po*-T-!EfAtxihDMBLh>JR2BtR3Ob&{UahmQj8ItVS$dh&Lor?yTi$pMk#h$^a;)yHI^LJu;3cNl^$h;DJi*BYu<z1^Hm3-gRu?pl37L;&G@xP#5tZFjBuu#G+er~EruvnB2g;Oe--RfPr;obRTJNv#s*JrQaFTsWL{g%8JGf6m1U*AMGBKJuTge>NOcFPbB<E89*{O%a&;iI0UAH=y82k?y$_eAnum)0dcDset#F|L7R+f61=rVNZA>K5qMXSaHZCk-a~SxwS?XG<ww19O&+}$E8Im)NsdL>nxxTXhxG1qr;V(@BdL8Ikk-_6izqFuRICrsk(c~aqhR*HkF;Qe}+yHd9-V0f5s3}A^tV_Vq%$eLB21q%<7<fv$484#Df1gL&sC_q1mOZj40~^`(Hv#+eud%kR)Jfo#0})-!&fJt!IYvmPGRTP?T0OU;`L1KqSzw~h{=v_jf*l&Gc}t)mEEF5}4-bzWT_>!aqV`Ql-yDi9Mu7<YBZ*~ksKy)G`5XzmcvC+nXEDSbkyD9!KTknh-inC&&eVM=3zmO)pL3_n=x_-ox4s~1HmtHfn(h2{T|)P`F0*+fe=gAWhC;SCbH#*D8&z-*{~81|VED6|nW6N9Xz{d`1&-v%I?_dMBX5IIR^erD`pS+qLnw@!+WoM+ks_19Li>JaNDU9lsfx~+237>7A~li6FT^(JP=6dcm*Hs&)nMb|)o>16OJwNBlih=^f;?0WkVq;whknvI0W@<PuKVU^dJd3#^Yu%va)Wh+0BVGi6oSY**f8q%fe#l|?*ItzRkWxe*=eUCivkqwd8)(E=r$f_c<bdC>+$rV&FeTET%O@Mj_uGT#T%j`K(%nLcNp~C*54f2S!jC7UE85o#bsIbi?77M3b(?oy$^DbtFC!X0=du+Q5^Zx3NFv~9u>Uj48$%8$liYmBx-5if<2<ctO_YbjsR9`O%R5OJ~;0ef!(!&@Ei!gMHhWEBW!8tX;d`iheGQb+R}YU=%u$7wf$Bih4Y+@{V>YnER0<e><fnrRUvw3dh0y8x~_ZNC!_SBn@o}>%dabLv2=#q%_|VB$CZ@B7(N2K)+8pmK$>g^RP!@^vF=w*7>N)w<+W(N*AM1=U)GXV&(H9bP@J&_Z^05#zD>6F`(Dhl=vf+ePZQ8Qq8Bj#kkv$`gJtO()?+A<(S5-R*+bEB-MSO}jmji|X%}Ep2v`ibkuS%LXf95$Vd5BHf8Wxl6vt{iiQE5T6Bd^@t}Wfb$tlt^QHn$5aGf`#L;sakj2?RB4277w6v(a;vLBVKndB^3P-xOQ$i*Yy<<v^J@t7Al?X(8{+L3(8$bFOMu=f(>!vXCevrc+JP76pB_*a<53hEj&Okti5%&Dl}^D{j`g|6F8M?M7p4sRFpe32)Jx6~;$@T<!-uq-UuvTys`$nGJ{izf?z;0<49cfe@dgr~Q|cd=;&Je+uu{nGw*xRpU!l!c?<I}9!=m6C>8kIz7j<Z<E4|5u{#_6JGdc^z>;`<aIXXd$r^xwt9$A^dPTfi~wwlxh7$#+}UJ^=S-nb0p^}EKEoZ#HqAKoyz4-Gw>D!x52E_S7=X)#1+LFZMnDBQkmDe3iz<tD=T>*1{3r(R>QvKK#9^bgetsykD=T=HHweb+;j;(fBD{DUw3z5(RO6JHr8JYv(&H+seFFIrXKFTvl+FSaP!#HVOER7UU)`|ZPPl+3jIE+V|KK&EqZ3M)=qJ4;_11Vqt*ijv30_|ev?3LfEpk%5<4bQwc7;ap^FBMka`}=khxcAL1k2101Q>dk}Ie9!s<GQMfOiH7wLE{X*@;e-^xEd0XHvG=CYwLInTb}(^_z}BNZ(d+i*`c${#Ot`sxz({e#R7xy*opfPacEHz063EX!GD%X5Ar8rmQn7%xqdM$-DhZ=h-hF*l}T(|MN13DQ*rlXhE=PHmeD!Eeeep&SziJ*`8VR0c1m>}<$GdW_cP0)v}n&I^gz!zu?Go1|1SwzuiN+e-o)3Mq5=zvEt>6t*MUTZ~Uyc(`M8sq0)Jw_5>Mr%p7@blWvEYwG+X%426V<)E~I4Yk#U&&kPPU1ogWB~!X<2Hs`XnDvRY6=H!Fh+bN0m57^YTD`s>NtnpQ8T)g=A8p{4`0u#Y``o<E%Qnd|UF^YJB-+<y_j`7u*(|my_+Y;h1as;)vl9g7!soySJnN2N%ny*d@@RhG`|#T4WF!LX2OVOnUDhYIV%-*gO(BkLE5;kU;i!T}=3vUP1pD<k9BZwsyH2+I2M9NSb@eoZU)^XX$s`!tLDbQVO6R2l(4J8W!i$^<G^eAO7Z#+B?I<UqZ%S-)yDHlHaJfWI{e9$<o<2XOSYal?@2S+%WQeu+E-D4&4x66{$)z^e!8DaR$d*rs!Zp}tB#IWYzI|7vzgSaES(#E1$fu^?VHtRKg7h%Z31a~lc&e>)$J+=&qS)9?ax)bu7a0VZqTo&ZR*u_v=Q^!6;C1QL@Ty)-#`KrS*VQ6!rV<qRXHl?j@0_Bu7i)Bq;>@r~XmR;Ez9B*3)tx4}9d@o^*Vu<oG_wJvJuUlt5KD=<FC(9QpU|Xxs?Yf;Q`wB*Wvg<i^wv0l-n(_!!jqyPgv8_`V}M#+;@)h$lw7-QVN5F5FZt*!IW5H$eVSt+aj{wF;vetV@7I4`XUaQ^ju}y#kJ7Xm3r+yIBDhY3t<ZTtu<Po8RR^XSb;C3HnTTo=Z_d)|o+0FJ?7|Pk3AaBS{?J()0@lAxep$wFvIpw-GH>&Z94{tLNdmcBMj-8uvY3l)HrQ+Ttax?3c&0Fe!F&TI_wuMB-D;1KT68Gk*}~A>jqc$Tk9X@j3^YaTJ>e4xW@-br14H2Ld#MEs4n6KLUCydAYXn!M%{XjqMF71x!GkR9hsS&H?)rL^AOHIK^`}ptU(GM?pNwTbl%idKeEr${{^71>&)b?0@o$>P)jAak0}y!>O}YbV-0kK(+~Tn3x7h0wy$aE-idIV4gmP`+E}UQSS*>-lYi567kC^j=h)6zAc6$2FLH_db{nt-!`ry?TAi!sMO-(;%^b;5f+P`y5^w|`GH>Cf0Ejga_KmYdimeHM{o!pzDRh8M_zV;>153`7)+Kb)}_sGg_hR{F$%kMw@_}$;WeDmku%?n`%c0XnI&$fH6fUL!KNzKr!m%!ts+i%2m&=PymoHG}gXbM#uFxKtPU$<YAw6$wm{0lf!QJE;~Crk8%caH#$YSyn`AVc-=*VNYZauLxP*=-u*^cTmZkTJ2#$f>gesaP5%XU;ZbUjrXSUa=+;a0J4eLKXv_0AxrKxt_7q(dSyb98UsmFtH!!e4Fv45U{!2tDpFBQPsi9K~7Qex2z+yBgG#A;7>pQ@YAOs*X!|a-BX(;>gZ_-TAOJ1af+y~&eKCQ1EarS)kz==+!X2yOuankP9<()G$(t}dA<}4eVb{J5g$Gv=*LK<v2fXSAZjmtb?^or4ovAL<{iLwRErLSQtGuoG^gCLDT?_;saCjoK+z(&?X&Owwq8ZqKCLCiel32v0OKRC1iqQt+{ru-SeDEh@diY`%u+_aFyR;$&H-nIcyI0;xxjo$c$1Jw+^H$5eWmHMf8rODzYWU?fn4N*8SkgE&0@1O&(C?rsqSVut4;gdL{$?OuYyAgFG;!I^DR*EZ;J9li(*hQQX_i4F;Dc`f0l@CU1(!8Zsc!&y<UIW1??QXDN;!`%U~&TfKhc{^7k(%&PQ7ObVEcIJ(x(S&xSN#JF(I<nTvPSL~kz_{h_t!9WX#o4e|t5b{}h_*1Jg<-d*zXzK*;k#eII)(IrGQ6ECeF-KxP-TNLBjNMsM#!O;+sgD<$E`cdsA3WaTMKVV+q|4j0RI=0w0p+8N?kj28H%zm&19(vyv$yr3m^ExQ$2Io|2v|(RJ^r=Mi4#0VFdCq1}MKu^e|JD9e?22F`TgNd34;fu*pPr}IP=m*{Et03F0I(<b(`}3LDFEsa@%X?4v+pdc1-BP}>C0$|sJ6Yp_ExE;qH_BSQI+lqFL5hFfy`~eB$4}Lq_8@Z!|vp6O@|1RLRNaxQ`XjBM;j_zvvv^?oaq<oom%J@@3^dUT51X=>@^(wn<VyZyQXFo*1H7ocBvE%zPwXO(_H!|++eMrRBfw=ZAZIA&Wk4L5`E<zsI%=V^my1AqIpA>4=5axZmO&D0AcO@c4U`lxToVbusN*|4UFGIo=TS%>h3$fQ@5N$r82&*{r0|5lXEvk9WefH#~s78)cc+K{p;&**APzG9=*O*=fYJe_)nz|HR$9c2V?Qxm|>e&_xG3=xC_EatRFH>vbi8%P4NifhJnG38LAn+rvhb+Kn9u9Dc4cXDm9I(H&TsZ79;pYW$l1{{FRG2I<iORw}LsKKcF816|SUg_WE(HM}8i{vpF<^k7I`JYfZjHf4~kb7p`C{&}<L*An41`)Z+a=zTe$q7dIjJvnc<zK5Sy!`#*$-pUDgHj`7TkwZrEOKx%A7voS)kLn@5cJ>b)_{<S&N>mJujFt$YtGLp2kgb7$0<nKg4$0>dgvz=|o*8}z<u)&#s=Sh;=3wsP?m4Yk5p~ZB#5;F^e6{VMqRDfJ@h6P1VW+3D7WyijAozV~vdvOye+a)`WiF6vN6tnNSAYm9db`jn|@<IjW&_d(18y5l69#2VloD0VF$(d~%Ry3Tl9{4?21?Sc(g&1YrA_d|TkrW}Os=b@^_mK-r0Qtx$BUB#hicKqEh_Yo-Kn5qB3EiDxsrhJsQ|g%I)IuE%vAjEykz^7kiNp0i>iLq|5bN58*<)G$54Gd<U>kK)=JtGh7}`9Z6BkQ#R`p#9S|39ZuP96@7L7I(eL^cqGLgQ9`6+du6Zb=?RA{5NAu&KbeUNxTtF+9xDOGqtjtttVm#|nCS+O|E23Bad!_9QfuDkSV%i+*l3H=({cvu(0EoU&)U0i_35Zz@o*OR%ny2~iHva-=Hdj{-o#1`9KLJd5ksLkSZzc&~dgzgnYrU*hTg}otMfL+u6<6MC2h`NZ)W1}b9vkkm~5S~<o)5@_<^3@2s_%foPCZ<kfk9CN%N@xWL850DFsG@1n+I74O4aB=tCud!43Hfl9ef_#NL2E@}w|&g-v8>p=kBlwBJ|N*Tt4*M&p1mgvI*;YWz;a7jdjBT3^>h%st{p1ka3rUlU$g24_1kuL(c;>5;<aGtTFnT4ZtqSvRMh1>N7s&d4&5l<KH<wae^6x5brDsO^;CldMWT4c+uEr0oE~sJZBv@#U?)&BV)9+!k|ku7gGy@GcQw_M4<e!C+d-*kAeyF^;gTxr`&@=92~t~I4FsbADL<9A=?XFc5Qrv$i|jZF0I9te3Te(rE}ALLhVK<{NfL<_e|d|vxLsbZ?=JPAhWrP$i@`d~{tQFW9WMhL(61_Q*r4k@%Obcj-^KHzhPgP~k4brz%Pv@m%hdJmao#y9v*q>@%m$vBb^zITc5GBE$v!!@6woIiDkYCgRxz^QCQ-q_b4%9W-A&ZM;r+kdu3_iapo1GDrFUZ;6NVSSQguE$eII`Smfz>g2d^$QjJZF;Scc#w0Esle*#c!cnkz*>01A1Yyb@e(;{r%s<gK)+)+Mjy>&97j;}dK~mJam@MXC!iMH+p_mlV`~hm3oQ-{A+b5@;$FtPg|jq9TIW<#51vxp%Oe+U%w-FL!KRcvPKiH;nn*QTNyF<yuGG=X_`ej8PE;zvlsq{0p{4z?;^~-bi~OK;L&q7lr(KMHp_gDe;!P2W7s<jxbH(dYwOk%~taRw!3U@60jpzXk-x^b^Pmby*X@)6Nt=z1THlX2@ahiRU&3@+V~&61c3c3f}%7YCq3<)H@y8=SLg;scO`UOP%KWV0D@OkIH2|>P)G}IkEMX64F+!>?XYUXaR!zqQ-~7d%jxpzNT=S5`WNQKIOQJ@NJTlwN(n%(o0b5!E|Gcy@AxVD$dHDTYq;rO&4n;ebao-~!{$acW{vvso><zmH@sl^fF9UB5`@@T2)Nq6?(A>w?L;>4Iz+bnOQSZx(D-kRR7XD{(=x<t&M|<z&#hCCJ+$K^txb;$Ymf&miDQ~UxaXz6^fGmbr|W5Krr*suKeE3JVN8q;xQYR9-a5Mxh_u7umFq8Zi8?v#Hl$2p#K&6zTwxA&+?RYR#ow(eg^?ZJKGu#xg~<%XvuRq>MJ-Oz4g#WTn$3*vESm@hXZ>!iwZ!!>@5=-}6>ve<A+{<~&lDGeh!3z}3Va6)OhBv?-lWaCRyB4d!?s=L*NKGP7NH}hv{|Hgp&ujI#cqY*gDxROlRy;ZS``>u<eyZQBY5bem^@Y#Yx+XDh_M{$rh*g&U2$Sa>g(M0(a@P>4e%(u=gUT^QU%32$^`~-$6ia$`>d(B0gumGvBcvl2K7FHu90O4v+{o-k;XQD@kQy@H1Rs<_M93WP0XHmF1jcb1_l0>a)rbk#H6P3dwcpAiPC1b&DXP#vyLNbeW4U3X?QSfgmjJMA{Zj#2-4quH_8@4*_`&uqvceL2K_#;K19y~j3&(3Qn8KGjP1UVDGKR_qPi0E&8qsKm&1+{ftr|`ztxgPT7-&*iSo_I?0Y$lL_sjt)k@I_O3@bkkW)!}7zy3oA&-rPQ(gp}WHCB2$Hb&qWLw$ClJ|yfY0Y`xFEx2dbE5Idw=S4NRETmA8_efOITcVE#KP4MA2Blqgh$t;R~X=ZLo0KT#k4U3ncP%S=~UzNvmmV451q_c&S{kSSSu3`(!KSeRw6Fwg%<s5by-F~aL?z@aL<P+SElH+Mhn@7JXU68<wvJ+aC7#AJiAUX)nLNBO9Dxhb!u}LrKg@~K`^$LiybK7TSnyeShf|6tgR~{V8kt!D%NzobFR)9xjF)fm3WLuj0F<^iFAKIj&ggvJ?!Vv`{c`;@F$obGv*vO4-=GxS3*lt2^L4WnZ9T_=_D~jQW!f98PN&PN1h_o1qg#5)T!Ke5E(wJ4rk!}{wwEofu}xx)fq8V><x$9ckkJrX}O2?fHxoYfX^Xl5ddr>&(krD0a|0xs{g1WZf<@rC?I)Z^4<OHz^C4=!~izruRGK|5cs-)TVDydZFkn(shuXgS0aS7sB(pySOrHd!cL+@5(K8gY=_s<77TE#lc8rN1)a;A3Skv+v!!Yw`gzI2K3NX}zQqjGk{^qut!qMo%|ScSkVtxhY1fxs6B%<zXr_RV1DEf11CeE@U^PJ}%;$9}NXY-k-Ipy#avaP45FTpDtmTnMgh@0bIWmbdJY75g{}-1tUDfEy@bK`+Zb-88L=Xd@bB&C}!(C=MFZ+_<8>1c05c^IACi>Jv%N{l0au)Vb>@Y{C2ktQOYaSoy>((A~3+bbP{vkLLzzm6mdMduJ@O<AMifMq_qX%YSBsnhRl_1!O_gaVfS>Y5~*iJ~!@E-*uFEn*iQ*GA8P)om9daZ^KN=3oegOLe&s4S4qdf2yhSw)}wGWSJxBS<qLX}FE5dfp3Gha8TbN<Z052z(n7#b4(Ys|_SG1GvK;vaYa35&AUq1IwW`l(l3;ayHNDxtme)%|*MjIaK;4)RyB<JzJSm<2kDg&o7FI<MPUUPA+6HNl?>J#}%n`N_4o#K$ngJ7H2)By|==>i(ln2mkVWiu7?&g6k}fFCdank@%c7r3s1~WtJihhGG#iPYUGenkag54x$V|WqbfFlJF#ROG;_@HY08k<)@kbOROiTNy`k7`{vf<-&Qz*g=%Bqm4|vRDOgb*;St{|`Xpv@cE1+2=WKZ^Q01up8Pioqp1DZCk%-7_@Ypjl%Dqj0Ja4LV9YRIm}1-~fdfNuAEx_ca5A+p=L&6$>GnNKM}-lz#vi}JeVoR!Xw!g+sOba^Dn8mCashjN}1R1ST0!w>T7DX`aR(;EKMj7<yQNy?!U{x%4MtVx@fOtBHJ<h9AS_*rm*)S!g3$KO2$yvyp_Hj-rxKX!DT(jT=9!CRd=1Yr{xO$Snvede@=kmR7drV$i0xjb<HB<*edn4W_U8J?lT8eXc9^fPYp3+KRzVrp5Qlwo-nc!7E{m1xjs1YK6WG*1ht;kuvRtd|^d4Pe=G9RrMIA8_hP?csJ*b<}q|E;;tI=k=$q>y+>EeytqEF^)Oe+8uRAsr^93ap?lE6$X7o6yza&Xst!14`m$*elIs`rjec128)|X`bylI_a6c!w?JLox6E}@8B3zq1@l%WK&*sYn7#E4*ft<diX!l6<k+1=c2(h-t_`^_JTvzpp=ZLLob#s=#RIj*y75<jk@*i8LLk@|p3zE?Ro7+i6S?9qHwA5c$N*Nd&N^2O%b3d=I)Tgu#<12UbY~xQ3QYc*Xxaua;KX^}v0gE;HK89%&MEH#DvmGv0(nG@=P7XEmo-6aVK0b9Op8QG^6j|q(I(RirBlXfbdiVR0oNr2s8A+SnO~zJdruOA9=M>|=pI|Qfxl6i(j#R!b$I0JI?5(8LpX^GJQ&%-SJgkiYs3+t@LK_nZCxt^xyNkD9c7BzkQqx+)WLE3Rpo_N|JevW0sR;Oy94xRymUJFyGoH^b%1))VBWAD0)Rro*f<JXw@?&?LZkrshgnj+lVJiibNnNWje+Fj*02->X4dpN`I-BmG1FD<u(oc~-9gYla~*K|e{D+0eh~}R1X06Q6Csd<vf*rG<O?Ze+w$~<6dId(h`P9N)rV)>JJWXWLeAm^N*0`Ep*G~n=f3>;dH?wKN1SYiqERv%G3WAici<S@{Vp^O5dqluTD#g*DD@jpmxVM+_rZ4XzED<+>n%Pb2S(l}!kvy1{4s3#{^E+z^;Bu)W9NIZD-{G~ZR-I)FQV2t%4y)6|Klf(g<OU)nYEt$us&cTfL>M#E<HPr)yN?nUFmF3fAZMQWth}XKdwTc2{S2p_AvQ9S@6p_nOW7E;v$bc8i~O>=z!*6501@msQz+&mVrn|tW$Nt7@6j8|BYFORXt?5C}iZA)eYkB;xV{QCi(PS(Z?}zZmo<gBwW(zT+%&}8w<r4oYMvcbNoJd?wT7*M-I$5^pVEO1i;`?)r<NW1uHYNF@qnX?0?kp^6}{UP$!+-klYMSl{n*})adlgnKfpTBo^}<v_I+?_%)hD(N{kgquFHs<1OIbeD)Uz>Fnt_4(F5>^%<}kd*%fr^!dZj*-ebc9PUm6s6%~Vc00ga_#D`PH$BphQ{@ubwcieEAK_^d1G|T{P`jATVRim3_v6f6x&*DuG(U??dcjv<$qUU($AF{ZCHe7Xsv=iT)YKyZ@e50oGrMqz?qnKWy8^Q)V4D^>Mf{;eI3HmE>@H&tth7w4Jo5X+vn&pPIV#9&M+|k#9N~|-=i(<NiC5(H%q$I~yiR#$%dIGGft<RcsHgnc%v~faJrM4k=Of{yKfRVW8iCETUOmS}+*CU@^mfS6Hmn=Rs0Fe#z}dj!CE(w9LU`KJ@8?)onZ+0~*#t47*jOy<cQ5nS$D08hD;*!zMW=2q>>jzZTENV@u>&tXx(wD*mQm(Yc8IJ4+#dti(6IU#Urhj3bQe%oQ_D4*E@jo-)Yp8K>6w7snoEqi(TzZ~)($JYLPmXcn+J=ZXuf&Bp5MQH%#>@kESXl?uj-^-wkmUohF$y2Ow!gDl0Q1vb>9{XMtoT8ZBN`><_Xg19_RrH!iJxPAuxP;gqq?h@XB~YoCTBq7|Z#=U}k~HW@eTToT%w}M{We8w2}5yC}5rAnrGOmVyVktSmay7boz(Vd<r0mpB(^aVG41xX)p`J$u0?D+^2Yb365c)DdM|}PbiqF4Vo_H=^vj<Pe8S2crw$i^yr&4f-5p*+z+-Q0K%1^8EwuFkGbGo-uK5l^2fK|e){8^`QZ!5etW!SzrFwZ?RWF@7u&@i<0F}O{ib=*k2T*^tfy6PvtQUB4!;nkWbW38pG9-5{`~Xx`(GXd#iHvlo^~w8#+8m?px0ub!JlKoyz7q%>SXOG1#SS2fB;B&OCR75^BBgOSFN-k9R3XW;4Ray;eRwJ#KoVz_f?F+M<i@p`#W}Aj<(ThRG^S~{Bg9}!UkomntR)g!_h(_{|w=OzWXIV{r<~uKm9Pne|vxb`@>IpVur`+jIyvF@kea7NqKXE>B8YULD+550YxF03ejZgA2^4u-lsClRTm<0b51-)t4jXBF|=M9L7M?*BHTP;glpQuR<0PRWAxXj>VN+A%dbEG@1Fzu<6k}lS^GoiJ3wWVwEOw?Xu(=*<OG8z!uz({aXLnfC>TC*$mes>S5^J!T(pO+a{&i%9;dy9GdF))pBp$*BSoK&O&`52Tj^9eb~01~)=Mk`BXkUPSIHEJs_aJ`tl0D3wCZb2>9&QrIWAJutg76tliG|+1ar1t8`xS}#0-H0;}UiZfb1%>#I682`0U>H`L^=VY^b--1Ow&#h0JaTZ*<&r&+?04?P=)%EOyoJj%Dm4zG~<KG)?cg9@U!XmSoY}DC_4xx4FLf_PDIFJiJz3=-9;V87Zn;m@u&@p*yHw<VOKHZ36ituQ9th);5+ouj4x8dQ3DZ4ecWce%uR&*QhcIR+e(*gOaHC(K2^C>)2zwgYGAHQmaReo>`O(8)A79*6ui^ITTEoX2|s6#6j~K6$PWvkwu%d5~#-)$4GH(<eeaA9l?+;9Lwl;o*4Y>n=KYu95dESV|EUo+Y!Y|DnkX^n@t|6cS(qXyvu<mxp5<R<JJVfv`vOm*+1&FTKm(;Qc{SAWt9Nek3*>3plloU&9vSc=t#ut;8L5vVpq4RV=Z~Vt_a@_Z*`;I$XHz;5$?^UrV!!wRDwM&9qU8s3&I#p-Q{*CtK6Mvt8REqjPl#RolDQ{v;hK@B5@ip#w}v0A&UT2s(mIh-ni0kPE=7%u1TUPWo%$TsWrKO0r4|_(f0Pq`|!l9quyYUsS3w4rt8{ZI5sO3e{g^#?=3VRe|^puY^&Q2(OtxuGD9x;Ze=Q80h2>vf~HaVys9KDP8YH@?o=?${89ewz-D!)Y7mF~Ze8=3|3cxI#c6A?t`tb2F_*{9o(jqMvski+eK?>RavgcwV#9`<5V0E@?N3t2p&#`8aH1vL`${j?%hE<KeI=%xf6QPShR!x4lZ*JA3&*z7P(d##&2d;eHEb}_35Re##*MA&pd3S*)RWy2-bB!KJx=83ergC-I!cbvCnYIPG1euK$kd3!%EEb+@kL}R=7KGJt>wJgB?4;i<a?%!+Wd4T>YQ{zSGOsQWSVJdE3>L=aDu582ycOhog(ktlbVuhvy=iy8?hI+fw6^cVH)u`y5LXo1xyX19hlP)x~CW&%FEX*s2I^s<M>p!F@Hw8)-tF1=vH1?xrny-T%IZc&wTylV-jJ`OKZW=m5Wkgv_)AT!!A+Dp@}6ze1pw9*Z>?I>+Hgpa|StLGt^s5z9s#ed$4(sHoJKQdwG`#ruDimx@laKT!zIlODJ<efaQ7EI}eg4MaLJsXBO8>K=8nzAI?w0DHucWI0-u~qTP<t#uWCnP7Enta*tb7QYAx`QY;T0C3In@F{bt5wP>2V0x`33+SLl<G)=1iir!$vtO87ym40ko_UD#+R>2oc6kHOZbR<}&sq~>R(3-|L3x;G&hXzx97I&^XY_abN7B&j6d@jA{c#2KbeDT&i?ngU&V#ezj#`f&-3pK1T{!SM1<*T?q32%*MU{p<CySDQnmzB|Sf)8VPm9UuWF5;~7f*{UMR;5V5q^DU%!s(pv+S0kVWA22=Q8ESxkD6JjPFNg6F%k-QCanVoSM$B|)UXA)PyuP&#E^3cTWfU78MY{T;yN{{QOG`r!Z<O;n=?T1B&`<i+(#?7b|YmTFq4Ym@-{oi1d*?Q@EGZ?j<h%67VdPT>HV_8eMdZ9#&q+M@&$h%z~KsFW(ua=&bdr7hoZz#7<1Y4w1Ey!HP7{VT+7@cEh&bDq?=uECX2w8CytGOMWZ0QAA&D*UtFD$N%Cbq|6L|Z_oY#%vSd_sBR4!ISEJwnL}brbdX>H7$amt992&zba#B;-FnH(2ld?pE=EGx@IZRI#LwW8)idH|wShE2#*D#C+?edw;;&Z#rpbqj3&?j<LDGT0*qYadAh`7VavEy}$)o=%^AdG+p4=SB}wjlbmuLIxpU<r;1h4Kji4)*ab?J@XG^b4%TN=uYp_SM-x-ZnSYJjl}XOu!Ub#~i}4M;%sezCtofxX@dRT#_XH_hDVfE3YQZReZ5y3tVfTu*rvlwc>epRZ!;`=t7{Y-w(RiR1}eIyon;{_AW}~l_9M4z7uQU^D#;QHc$I|3185{fYAjbw`q$tiv122n~+hsOaNjj$V7Q=<8@AFPN7D1N18LW9wC93+9!_ANg&^ymWVbVE0%*~r@0XJpAZ<&E0ru!w*tGJ0kx|vEdIGES2}($+$qk3wHbWrzOsL_i6<*%=GFKb5)P?5g~KFoSMM+1zPUhR?=@rp4n|(`^5BtcJ9?ZgzQ`G2k(zrlTubfM*Q+XY<Q4h4kTp)DVVjnvvu#HK!_poNrC`-Z|KwJ)mQ{Ttto202w*V6^K%K$0+En}uqISdsVa2D|drXuI8yXVY%G9HUtvE->f9F{^`Lvz$xJ`B)bloxvFlD502{NS)PO)>}8j_P_CtSn>ry&wpHR%}TBtxiatq@!s-v7a;npx)%S=)Ur-c`=X&{$~<6UT&#oT<&Up|cJl-Wrm%SZh_~#L3&hE2p$lBpab)xQomeNAWoF8z$A-GwZ$fp>k9%I*=OR6>fCeJ^Qn%XC)}Eb*Mwql6*hDr{Plp=gA&>cCuM8m3Z1+d$UEnVfOeF@D@`iqIE<7BRIx4sz;<(XI31cqJ`=StWPl?i~aLh>LEPfaX;p}tP(YCvrMuG3;=;S1t1yMs}_{mrmd()2AFS<6F^Rlj)lwUai7urIgu*c5}O|Z$+gH!fGM$%MSg0iVQj`F;-)i%HK1#W`T=^^O~@n@4l&mv6v}0QAyQ7v@3{iGF=+cL)Y29~fg>FoG1a31VsP?e1=2;g(eF`z=Cu=IF;@b~WH3&BXw$hG`}xtwh@-YlOaybu7R(9QgI~9fl_sZs>T4Rd6>k~uX#@U;Ik&s1taqqJW-~w(n|&R_ECch7;gr6H;?Ql-B$wmy)!=y2#txc2@COElv3&8t6Jut7fNPHi4Ok!S8{+T!quDz9IihHb;M`d_qYQbM`;3roElHb^jDs1*JPi5n2|b@gx##_6fO#1E8YpOJV7KY+(ty!P4FWfDpZ|9Zdg@HziCsKWAnkAToTd#y;p972nlv*3<0$z97aIScfB9>oCY$8Morn7LX#|dbJU}J!G&giG9i|TjzBD0DYd~xrSGi#fjl>4FN_ftky=%g29=4~BrXRP8gtNye_P)~ws*zCyNQ9hZA9)^!XAfW^4AvgCag^mCdKfSiwwHOFI%8jSfhvYR?5~Z5=W$LlV$`6vFEV08Fo>qa>JGo8ReMmP&i}#<j8&nMd8|EdGjIzu?=Wmtog3~Jy(g4eKw8m`B4K~1t1My&AF}5l0db0XZg^N29U`st^SYXkRRkm2^T9uOa4}V*brC`Y%iNH!;PbE7vs<+}6rDW|K0M40)N!81E<A_)xsqEb9KmVQHECI?j+GYOetIyRIZt1V;|b7Dp||rZ3)k5j&w;I|&it<Sf(yaa)W=<^6<-qs97=2YNv?B@Jfc~lJSJ|K9v)fJ?0pPuRngWxbP_CQ$X4+fTatA}PtVvv=$r+@nnw704zYSJg_$^<M`y=859;A0bsoa={zfGI?CQ;<dLq$PkusPJ{6m-RQm&ro=@sV_QdE&k2OQ8ae?8B$ER7@f|AwZj=W#MzB&YqHi#&c<!~wj1gjXYO;-4G-mLs(qbinskp7Z)vX8<-kT$LUZXjGTpzo;%f&udRCjv7xCVT~ycN?fLmW4xQn{=tdgVQ=&YuMmZ;O7q-F_yuaPAQD49H823eEh;jG4Hmlr!1LYJ#(S8P$`gRHx@GL7^TTH_2$_14iBid_w6v7R-;ZB~1W^r3J%J&Gj4eXd@}X8=okPn=YV28|3H6H`)$qEo>;owk({c(TK_?iAV_a3)>Q1n6_qh#Il3*es;+uj#c`XkWV?t$_xvYJ0G(j*B50;P7jYrD%(t{}}3)1oIUvMD9M)3$}<FNn<3tWeegGm9nln<UnHf}84@Su=>KN?lR94U?WJr|`;@}blTs7Z#D7h8q0={OvAzRph^-wd@uPaZ(X{ngUJj7Iw~pmW9uJn1^0%UopyJ6Z_lttxj)sJqrhEx-|tnjjHOa0_5StK1TmNIc1@V2{o_h+A*Y)|pgk2sw0E5q}&t@y-SqAUJ(>muv50Mj%6#8AmOn!BU_1tKr#bUxbiAW&EmCK+Cg%auzjFrw_2}5IrprSWf(SxU=h_+JtK`2YxQ2#gjmr^D@g7UdkUMZVw!=GE6=2g2@=hoa6z)OJH&|iiXRXIdgW)Gx3^U#|Rx1d~B}EFzJ)O7Q~iBEcckM|6Gflq=PgOv1#qPTQZRbI6%N%;Ys!2vgifLWs?q>UngUi28}nQPzU#V?@S1N$laHiIHYYMI`Ou?_hbjZ4l=>}X9^&7x+OS8v_hhm^of2<uwyWUji!7_Jz}upQ|d@FMp>qzph#TH^_jId=lQs(kEbR&=K;BHTs{TsUgUCj%$_U<8=~F|NrA7@JBtKwDf1a8x7OhW3CV`_JWb0}@gJe};Hr>`+W8rMtZQeON8ub=FT#haqB^fz_J}+mSHm0n_|4BY9>FH=9l0J2F3gG&VYlpUbRmTWOg93bLRIPTFLFc#F>hnKR0#}|&y(yG9;DL$r3ZH2roL8r9lZ>n6SN8Fw#K~{_leA^<OoZeL~SA6k|gkDzmL5<m0tNO0)Tmwg@>{{$w8jQ$zjlxpgW00odo(+875M_`^jth5|0v23Ji}~f#YwVPiDh_0n!{yp(Ig{Aes<y6@S|@gx#df2=j85HYGvPHg9{!3hJt;y)VABx=tLw3mpdB9J@6e0*%cORn2=;dJG<Ssb}Nii^p&%#1u4?7oI+Z>-I+sIjmhtsi=by$CBhdqNj--qI9+mp5sS;;_W=m8EGUhT@s->qQuLG#`6L+(&mOvgYFFyhc_(p4{KB$7mcFvNIK&Bw~z4)6v!-ZqUYm4iO@lhgB!4Rs88vK_BEQp#CG3LyYN(USiMcQdDh&^p^Lfui!|iC@3H>23sE6<of%qs%>5X%3{i~f<e}6foj5I?FqF`&Uj|uiFrNeFie)+q#VgR2hAM>Z0q1E@I3vOo3K$>m+k3Q-je-jr9OH#%>QF+bN@&1Od8jg!j-?ho64K@ugHy^7>Y(F1@e8tNVPmRJ=u#R25>&sJn3BkSrHu&$wS3?^3T5vp=RsLBPrWETEMi^Szovrk%djPcHvWCxD`nVwx>p#c-uAOJEjv#TOI%iVdB`~2(k{iFX2^Y#!_Neii!qqn-p+AUGs=R}c|yn*R6S#$<9aS@4;0qEBZ0&a@w-$h=<|^o=Wbd9+U-agggP4()VZA|W-NM+NYDK6bbq4MB><K0$4Veyu^B!ufOz~m2qCBo1n%sj%DnJeEaUm6;YXNrDdXDN^aV}`kxYAy+oRCao?gJXB@!-By|ztRJiunI$E1S=KUJnP_^daEWGOLM3^c6arKN{Y31{u;lUQU}<r^6i2L1pB*?DiLv9JFrpxAj_Cv0k-)J%$r-pVwk9Ap=-8iuVYJ`xheHtaJz&n_NQkn9T}h*2TE#MCoUMv%atY-X$j(Nw0|OKr+(;U9`trLSZGhM7{f7yC(NaniWp5ni>^pPW`%(ir7tmI&^_qKu#cFwDFx=NvW}8A)3JX~++3wW54;jBt;$T!Rd0QQOesifx?SIy&#lJapbmOZaKIKoL`wT->v?n2y6WcW`xznU*^)ELwzyV8ou3d3u?U#h0aA=I6*e6HP%VXXhqm<o1uv<Xv{t5wZ!(5D5&hSLe}onAQX`{hrLs94QTO?19@%G^wQiEJCDdnlm#nFJDggWCxgBeb-l**IcbJ(Wgu+a{&zwNdzC`-t=@#)Vc(KBvJ`1Zb2(^BySMO>huU$TwUL&%a243Wyn*m!D1=tM&!WU*x4=PYj2+{w9efdyy_~!(A766lT30J*82m5t`}Ad3h-*LP$_fbPSE&SZVI8;fFy3Ml#-{$yk<##aa3NW6zi%qk6r3($ulYMH6tjE?ut-zEsIV^oN6oL@HY=iNFF!lNYry@R+Vm(gMTP=H*piZM`7y|X5bXTR8s=XgQxsMy^vD&*FGCe+lgv=^SrEUgsNO})zJ<?gQfd6$ozw)VH;x7CxNTT_n+sqK#c5~n1+ssh@sG&ul6LFxT{4PK`v4~Cv{qyhN-AS$;TfcqSY~}6wxq=DAjwxyq3;#9O@1-IyU~X!HhC3lWdIqEVVwN*dhy^<}_YzSs`#UmjC`_P?gzZ8xk2kBgDWuVlxrRgx@4@8lE0^wp%_<;2lfs7YyZ$Ev=+L#P>U}=VxKlLF|WETX0gzrYu8#v^MokN84FuNfOwWWsD2o4i80;4p%$hQ<)WkFX=hFz7K3+6mtG}1#A>>4|(9o+zN?F4ve#eyfyd~03`>i_wXdCoafjtRX-O9{iBn}B`f-1s7vBVU_BL<83+$;zMtuC^;R9TE#rGwUPQyBho#PCQ=o5`=$=G)jC=hlq?WGC`R4V7EW6wbg_^GtsI|D+PPx1e*k&CPSLAad_e!SPEFzq}a5t<x{h7dB$COP?guayZM3?(14M!3?E-*VQ!ptJt2yM|X#Gqvj`(7znDFZ}vsvHsEF9KbTXI$PeCPAzSL^U}w#0ur^8zsyICneF!%EX;i*7XcxcwJ<?kPX`yL7BB+U2x%s+z2I6HXQ9s4YHK_Dx{V2kt(1gyEF_)R_Eq3kpN~nCBgA8U~dU$cKS9AH4-70v4T8w(hL64%S-8`VFa|<n^#uYxQf?*EH|@_a{ed^A$ej3W-OMcI;9S~?P19mjNu^*^L^d_{*P}z|LZS*81&GwT$3#ON~taa^)-Mzh{cI&53TKeVzWFkVJE?J;VcJ(*-(ih%=lflBG2Q)_n(5NTJI%qH`2aFTTRsAoka`-1&stu({B*MQ-{>NG{jK0jH3|)#{CB{Un8;yvFzvxCvM1|qSB2@VjfWyf*_vcF1_50!U6S=%Egf-$S!jYk5swSy)02yIwX5UH#|{N^&>qy*oOQ`<FktHAeYsky2yMl!1%*dG%-yaE1(0U+}jVvI|Y_hMfy00U(qGeJ5RhL-VjJ}BrePEF$(gmOf5U*C1nb|#Hd8&%={zpnro-LX8N+&t4SFK0Yif#zjKUnkvW{DmR8TG%S;>sp~$}WTaQ?dTEI}bd~{%}o6N(j*HF9;9+z>O!Gl|TpWc<T@3NvvP)d0hts=|k@)l9EGj#~H+ql=!1KhT!4_qqm+}C03kQWzaQ*B#RqEO}>{@T(%0kjJ`$t8M!oT2&r*eXg!y#d9^3mnl%9c2FE$kZswqqj6_2y9j91pA;>n9q#IS7n-xF-Pw!$G&i47as=Gom6@hBIXlYWOq|)7h)u2uD1cs$f`mmvzh(?UmK6C6S9o-VtB`k&JG-_VAqB{DnqA}qNd2IISWG{hl~%#lS4{7laIvFn)wa{X&p!PYH=EBj$&udrQeQKM;VLEqy|DppTyCP02g)aL>g!AlowNI+A!iVxpBu#=P~I88jJi76r%9arJg#RLyxk)F#|X!hXS_JReg_j)an>zZZUk`%T{t2NXnWjJ;L`{<kGgZmq)q=PHh=4z^P*vSRqyrt`cJu50~lX(6p#hB1u2a*?f+Fm!l`zr^~wb5LQ6Jd|d!9bsD19{-BYEwB_b;EyV3=NTBT1wRunF^A*{i52{??x-AX2Q*=%7Li0v9jum}?u$^}@)=R3>toK2}ka|hHNPv2QPWZ<};+T0kPj^XFC9}-u^eUb!9y&EsL|MW2n0&OH2GvQc>a=uM4D|x7*67PiNdB!{<wRnb8;MF1JfY$*^7dcf3{@w+u?F_FY28mR!PH~`GGp}5x7p8w?Dsxo1yP1b!>NDx-m=`8Gq`y~{QX^Aicz*-q<Kp04a3PBYESI-nse_m4WCl9iXFfk&l{TO9McYnqXLmu?xBXA{dF#SS4ToX1+OfvnFtxCxjyA5fPfHvMUTDr7|e_6_cHonr3pW+bPfjF4=4gBRK|mG_8d*<;uaRw)2b!9U!Og^TH~pEJ~E_G;4G>>E_FHGGGa*j1Wqq0o2${#(*)KJA_Xv!lq8A@3gkM=Gb>ZGMoumLG6CfGnUZOEqiAPLa39|ly=RTPnr+xcPOA11MS+}*n+#(BB<rjASEk75QXUY#3w1jcPXLBlpT7ZmflJ5B*q0iNeaTCVn5a6@CKcn`z!+DRbCVS*Fh+-25z?K+xKxfoZ#puX=xjzE^x(9&FB=%!-ih#I4xGBnF{6LOuq&j>ogRo<Ljq%%wwoPZqb^pn7z?9PNz|&78G}y^vFI|q#h$1-y%5JzzX->247H2Mm@&62nR|VBF;9d~jAeVXAQ^M^=LugFXsN2Ts)_^Bs;b_Iq=E~t)zT-b(c9+57;@dXysjO2wvS7(AXNL--Ee=HTMt-?HpIvcSrId_UonBFV*d(0MxE34+_Jp#KwX9x=!KE~17w1dElr*;y^I~*ex}|NP>Ce+6iG$xx=bqBC}dE~Yc}a(^ZuI8D)DXvE~By`TZq7kvuaCu1-+;w0m^Ve0w)s~d(9=PIUOQ+L!G!FFy%`2=PV*G(M!n^lK0CQXQWuv0P9H#EagJvQyZ$K+u-;;RY%C90N;3mBeS){7MBm@jPX(*hnUR|JDO@kj09qngej96Hlo^jh@)vpkQg*6Sf=<yQ}0YT2@Tbee_W%4L1e<CfA?|<4bzcwRPjdvuNtmC$<8pvqhqvl=V@igVnz)WaIFcr&A}#gPqW<c8`-`Wy|qOpOb}^ez{*#(N9Prkyxk-)C(!i1!~q4;e++%navwQV9#Gqj2K^Gr?&S9D2!Bj0#oXW;c=B80ZGRSV(S%8BG2?C_zxJW=JDw2JHGCw2g9ma74_{#V5GBl)J5KASlktX+JmZ<n)1SC`h;39(MnD76r+^(uFy)y_ZUC+`FR_K)oeJ>7Cq;M`?Xt}YMh|cZ7z=Pf`@sf>32f?Clyf4-<-F~e3ObW@2a8<wL%<?}+!6N(9&*qx&okJfQX~Ls1Oh*S6w6hHZ;xxH-XU6Z#)cH8p;ln%=jyf8ZPO1<Xv<?#FxDH9Bd@6qQ&6D3D}D@Y(g`b+9zh88B+u%|KJ;0fpvzZFNN@x_a||y0!F3-K$H>o&gNy7PAaK@HYUc-i2bk5`Ly}$@Bf>gRSym;d{`Sz(juAflobrqNI;}tCTq85cEaW|t>J1|iJ#C`KbI>w(8ig23vDb`Qf(QQimVwo<E6tL7q@$_f9m3QgUik((H<|*I3!Gsq8;Q(>=T2wy(o*g8_<#xMBt(dqL=aI-aSymKyFFs&Wf+ksNnhv+E&~rd<65pY`YlPypTqdaw?B^R6!`x5Om=2zxP$B&ez?&nMItB*Ie8h4)H6MwNpEFfG@S(Qk;1U#s7sHvna;_~`eayp4v_$%^qL=H*=-q$&Y7h@+k}=XmV%`nNvht-G6*G6H6PKLt)awdUi`f@R6*xMa~O>%8xzH)D&i@Yb6OhmAod2?5X}bMvfgQ2(pnn!AgXu}#BSELW<*P@bPk5O%i;$%({eu$eQF)&{J8$h`62SP8wY*mIRntUUI7J5;-#^@6VtE=g$N4H&Euz09)=iq6M$hx@g(@1^Z`c~FafRh*Ld#b8=+?&Ajd`Oa&k4tq6Y3kN|1uGSTCA%1+T&p%P2g03`Z&|g9m-C{sCALX8HWfHeT++%0C6iyHbuV4K+|~EO-q0aH=sZBp|^eDpS1b<Ao*1EVsyqr4zVhpxRvcht^%}H?ok4?ItiQ&P?ZXrh6#zvqo>2<R>sJV6c0)kxqk78{>D7M#lalR4oJ}8=rQ$LeP%MX+FND34cMS%9@Vy`Z9%$nSOaCyx-slL;fMfQ#*z}_ku$MjurULfHdAcK3~aJd*1imwF9rf%Pdn>eTI;ALzJNwvlf6=yf<lc%v5geWMpu(3U9BI&ucU3@yWERBiGP%OmGH_Tx@r`k9JerQxl%LPSQrF;!uPy4QG)=RTE_`a@@8V^`YCC8>XQivKo|2q5*EeIHnY?mwD8clR4wP3i)TS2z|LH^;qXLtiqEW66v~`1hDqA%yLSv7GrJ#!x0h*V63I{d^6e`R(PXxCt-I(5yT2}svrW#*ON>E7~Rsv0;A_-^guBHq{M0FB#96`c3kO(oeoXA`518`smq|YQJ6uy&)C_GID&YD%h0O<V%`so>?lL7pw6Z*8PBBg2!nx-okXuJSo~014*m2a>tBH>mj=9bMwkut53A>*`v&~$=3#rt!HkpWcB@jV=VZ>g%rf7xM6AZPko5(+)-OT-6TLH$&+%k?){>+E(vGjL*(K7jE3KZ7iMhv+w4A4A2@{U@ECVIr*Vy^d-4X2P`V3JDf-Z{bl=fKwLyI1uCT?~mBJ7WWZ=up8ZQ(IkGh$p;)RE>et3Gn{y#MvD$H)4dsuP!bT9&GU#i_R=N^Z7UVsd{r=l)FhkuQ1=5cS?^n~CeF#Ngg#9Xp#NdA>SqNA<6wK<PUSrlQb%^Ikgn{_SI?oVI9*5}J=2JbzJ#-?Gj!O?QGVS{7=T>QvK!fp!rl@7xmv)AARj$P04TB@MRrLux!04DWZ4Rz{@#wm4^!rS0Cd&`Y61L~ck+xIxM8v<d9#X->98(J9CRMKc9PA5qpxX}hM+F09A|1pmPE0nvb%>998Kd|mdrhie-0(jURdkJtJ%rNBgk8FJz8)=Gm2g&1z*MjZ1ldXg1}T(?gy4)Y)Q;_{2m+K>!4p6aD(csEYdzMqiLJ!}Akp6Xqz(|We{i~A45KP6j;OJQp@rf_X1*(?bNWXa3_xU9!Yt#b3SqPmb|{cCOF+|G8(>M~4bZD#H(uL{aGLlzRy<wMK;U{`$71?xdS`U3bk-KIDWYE_pNFWF@7m*M_JqT9IeDS5uaj{{Q9DK-o+w_!x>ToEZ4V|0btdBVwhn``BBJ#Rv_?z){hKi477vIqN3Qz^3VCE(PYNA7C%|M>RXPk($fKm2$H_U-Zh|Mvdtx8Lzosl-T!vGpINPs6&78CQdP)H1(r0#w+)1I@REEofKv-?#^*lgU|Qp8p_K{#=Pck0<``>`j$x1@>`qb0n?f+O7<%RI`+xv%+{g{=3&bC(L$Va_azFU(fz<$PH}1`oF&XYv8Alh~p7c@#Az~M`M41T_NJB;7R_sSf12sZ~b&?cFD-k<k-{P;v-HJz4=I_KmY#n{ZEf2i11(C@akkA$FlV`{AU1jCL1-@A?_)9s2wjJ&v=Ls&>0DfjZ+^t`TM{8^!qQr{q$q2zkP%ypL?sruRs0%^SRn}R2gS;{s{Bw?-}0jqZYHfp*rAL!>+K)$Ku!wNgQ2`XU}l2>>*<f9sB?J*Dt^R{J(#G@*n?lL`R?vvA=en+UD9vbC}PO7S;NF+A;fy*NT&uOV;d*Wq!Qxe@J|JdUVJ3(^~ocTXs#G?*Lm86&)D$Ab~DCJbppu_d=gF)*UueU;Z3Dd}1`tuD#3Od3n+C4xjg?;eNO4N;L~8AOfC2XOuHPhf9J?CsHdQOxG;9+s~ma@s&U)i%1hdIui5a=<nKlvaCHT74+l87|L<sqQ_IJ&E_dzXW7+8jCPQ#06G!dIzJ1Hm+bh}w>VGtI;BYjbuBomb!+!=jR1DeTSOXIqTgU%8vyx_Ymxgvp3nDq=|3<hYv_p2=%<LswaUdGJ|O7WwC|+8?0QY=5ng$54?aDb)^E&vgvY3MJ)sMMhBiym4$a~E8e4{8jp2<ZlWmi}XYI4^{kdLS*w{nQ)Xk=Wmy03*RYcTz)HWSG#EHhxkpvll&ZR6e1(}Ae_#mQB?huc$R2h?FT#Uw1p}<$o3E394!N2)zs;fb^I%2ZFFViY-Ssvo+=0UbZe+jr+jJ+$8)f%@we=yj$I5g8=`G!H3NNs42vIOm5o04IJRljmstHH-lPqGBQ7O*+)bN+Q#kcN}{&4`j{+#}&8fNCIu&nG>d&Ns)>@ROU7T8y**&%eFD|6NEW9@CC$5tau8f&b4XzkN7y5nJfEoXFbskS|W%M(Gfn==_`*@6Lvsbj)FD$U3PzWRtGo0H$cRwG`)ltfMN^C#7ERWHk46<PB%s1DS@}BQPKOAe8<?3TdZ?PSD1Sk9k%&8UptBp$MwCI}K67!j>9?4g~zqq_(K1gr{-nX;Z=ri$JTv7I^RZG=_-nBoDCvkKn_n;D|A<WUvZ|nk3YHI?q#saRNmfSzVi$2sW}~991o<iyckcj<9sW)Zi?hN>fg+b-|`_&3D<Uy>j-Q^?zXohQIY?wEE#R4UqpV)FT%9Cv3t|lyQ2&OFYR5TjsVn63Pbc{xSz*(wnC*jjJ@VsMo4R_ws&r5<Q17Fs4aopGV}Wg?{s{%Q2^2@AzP5IQBP5t!B!Q`!GU6P=sjPgTRN+YHo<DGlUxqI?h!*C){o94$X<mBrT<??6-bGdYTtC$D$>dXmyujZLSW<yk`1-sB#*_nzqI>+|%V8*cN3NS}Nm^1I;+HC?D>5O!J;sI?=Q&GR|xn(;R#f`1(VWyu*D(cZ>ShZ{Pm;9wt-HCokkaNfW>+Nw2CS<(v$Q_rlb3Uh}_WUPMIHjl)W+aVsqylj3@9#t#O&WN?w#N@0{qqRX~<vcM=e6;H^yrqI6<)p9T~JGP2F`~x_=;9=UI3g&=*f&LL2)2N7p<IhcABUcUYW*r3&#|+&UKYELPfn8V*^=B(Ep3ip`Xntw=_x_JJ+Z~qTKh)6A=J?O`VG~;b?ZYwCMV8G7I>>$a7J9kuggB6s9=~N!k&?i-2Mz<Dmi4#IEkAahd5RqVH!Y)D#I!IM*ah$JL;#{{z7VUQQ;4zz=S7f|XC5EOk6;eZsR368GV#Vpyb-GGYznMlNMgVbCM_WcdJn8GskGfE;@@#kN3m@H6jV;LyDW+Fnxaj{<iLc~qEuCT3+qG;P}HW%DFT8d);=GXSYz=DoPTm==Z3A3;`}{$1^3oc6B>+%i<N1MQB<An?TNix_4hGL4;@yB+H2miX-!(9<uM8%{6sO!-5FM@kM=h<Vq|Keil<0>rqeWmzo%cW+o-o8wISBo4Xepvk`4F<zV8z?I5eBGMY)KSdI^PVA@`bVIQqUz1IA=o#hk)7xloXx$on^WB3+8iT(gX3GR!Xs{Uy`3J=rpPqbvFXQopIe@Zr>s(nJabjEKgT^;q{%-q1cU!sQZeBHT>(*v&&PGo|hNKpv4vQ8NR4j7TShw(Dp|MF5)=0)7l;j+RH>OHFVvexRIvERp#RhKHzkgXfiMwaEjoeeVvyrEnPnE!h!cD`_%d9u`?0)}}Sc`z{%JaDLY)WChNyJqdQGAV=#Z-RD8~_oBlI!f6GkBRp;M5Mj~7nworrLcR`i{tka_9;att;^nmu@H|G!Fg_)AL^SF)Mb3%9lH=5mIjr*A4W1!}Y>ke%lmD6<IuZi71{qsMzZX7J*)-KL-km0f<`kWr&WcTSsKij{wBb_%c8#1K>s;P*E7sb^hnJ_H=P7}gAqgGUO+)j}_Q+0CLN5rUgr6i|W{|pLfVCr2#MOJ$HA@~vT{4W)Z}UioVY0l}a;_b{YU)?rTHEuy$kr#qbv*wd&JkpmYM>#YETPJUKhNb!9$&)sDe;K8!79aKs|1N7DBCDpWCx6D4waui6W>r8k7%!0_f4_p$FSy}*6>gKt>alXr=WN=+Rt)I9yH0vT&gSq2APhT9wX>wNmV!J21UaJ3rVgZvg<+}!CI@56Qctskn(3l+1GqU@_`-OU+@NDqKQmB?(U=ZWr7Tn`UQ6JYk3Ch>yDQtchHY2k8NFLdB_N>3RTkZF9|vW$M9OY-p^Tj%nfeZ9n*A#37qDhg5BO<)li*)LhHSN{+kR9Zi}L^RzI7OH!R^V^n;dB%}v^;-?j|<kYy!(w~Lwp*EPVK(1G4{DM@Zd6$zx@{)LHCKRlMrBB|Zd^U{Z+<E`_o4}?$OPY~Ig-2jB7#^ZMvR>~YxVJtOx`asFuq=Q*)D#PqCH*9Nprq5pWQ;2eg?Q=XpIUNh$^gAz`9A|aO3;Cdz7HO#Zq^(NYg#=>mAz!(=7EV!~%sgN5I1|z9oL7Tk#Y2a&dWq`o4=W%<g=^`Q7X@iPN;#4z2!iSUHN+m0Xezwkw2~*%MO=Nt28<OnTIgM}AAax%`hC1K(HdoD^aj$i!hOAf60FgCMYf?s4IXUPbx5FI!LCy>QQ5#(z<$F+^C?{V6$!YOcZ`BmlPa!Z?u~!bt7zEY66InqI%io0tottRDXR$Ic@&ycNR8k`H13(bG79)d17O(49t_?**kM1CV<z`8)8Z9}o@rWwNX<%40_+j52e>z2;DJ*H0a4Ks_1D(+wIh|)sklj1(%)ry`r`Eu%?%?~bh%-sh;1FE;5KaWS0!{lwJV<ejqw%D4f+m9nE81nrq|?U@!0RQ3KC@B4!^Vvqbj?n;Zhk6ivER+7NgnA#)So<=ErPjC3A?5%tBcu;ubjM<w`YqGYHpul%dF2Fb-tkw41W^&$)D^LFU<`h%JPgbhZN0$b$`DpZy%GOfEsLKhPq~<e;y10qMKp+;nO2af;)NvYD^*oJ-95hDZfi7R?s6O}bUlPLI>sM)Yzq8QkK|dyG=mz!@Yu;&CtAZQ;OQ1vu_wh?AO4XY47CE%dW?tycmDCghM49;__|Q+GWofC^0x>v;%5f@tV^GHPJSI{I-5SnRb=sg>5L?Ma6Iwh*xK80f0$h9A+xYb}!y+0nB?lX9$=fDyqQV;lQ6A?lg((z;^lUZL444c!_;y3*4Nq7}O0<i@Cu$yB1DGoCHrOnEQ2O#w)4UdJeRnB#BHK6Fhq>Pg`2l8zXbYrYKXh@{Fq%3P{h&e9OZ<cKBuImB`fdU}pR^NaneIm(g%UJ{GLLmV_>JyrR+N33D&Zw+#ev0aOjCk|qw^VWSN{rG(P_BPLpym1tXYb_IP&14YvV_;k4tVGcnh0cd1V7E+4rKgUu?}@A}PszCMs#o!q+b~$RsgzL{&-mbQtAxH22p2kg9ZEw%7Xo)h<~-)9v!+&g*iq40qayS#n#6t?rF27N!x?duB3JxqmX*m&D*SILWNisyzf?moTwVuQ$%1Py!;%ErIt2FQNU_Yv-G^~sfqa4DZhyA)JrL^qL39|>jK;8r`w`lEO5MitU<+maX^cY;H{o1uhfc6b3B&S`ssxsnlMe6>Nc7Rm+WR-XCVI@gU<w7gu*T~$m%=sE3PxyZZx|X>>LhnFh(HXKD|TzjHaUU-9Rjm)sk7YqkfRCpOD2r1k5<3lyyVa^l^k5_F|G4>8kICY;y{&MU!{-x>I2taM%q9gH~MZ*kDWtT{pL-L$4vi;_`9yT9(6}nH$*b?WEkuG`0TJTkbJQC#Y`|Idu4no0f5d_e%(bWG=^>38LY*%0|i*_DB&HG$%Bzay-ZR5l?#+JqI<<hyguQ_kf*+;GL6s&LcWB!Iu}_iQDh+`))PJz$s7TsR|4NvmPJ;B_TH?nN0<QSSU9od;v}z5Au-m4CrL%rH3g$aVco%$gm77Q9WrcP#MVEYDd@M}=CejAV<5%Sy1zQoo6(!F66)heZs*8L?AoyA08uj;h1FhBW}}UBnsYLKm2<L%$;6;KuyA|@BhR6|X_NX*=F@Btm(kmb2Lw~f=G1;X^Tp~5C_r<t+u(_J>kTD=@dkZ*Wt&xPFYh@CV;M@x<icOTRf}?(Q575}jKfl`g*dwdtja_2@D5y_IEe%g8!U~+JucMxxXNwm(=;;Cvg`ZcRHq&&lV?#Exi8zE&p>CrE9j@N{CWz)e03N1h^r*PVuR|U&xH)#6&3Ga_Nh;%ElduQwT9`!9wzGhBxW6<E69yGdqE{`ME)=0X6>~DW{kORT%fg*(^Mpb;6%>HZC?@$zETx9YF!A48W}(dnyX_btIS~wiCH3*@f>e8uxlE$9bf#A%@YWZYo#WUxmwNq2StrN*0Zzq2M>_P*#F#?7t-RE*s8-0RDsIbCJK`92o@Fl4W`7nZE<x5&UJoPw2|V|5*#mj3G^6wp$XcWqHb}TZC)3X*02eLQ-E;TyO3?pwgOz=l_ug`h50VBM@icB2u(+XHSv<<b;z~vQK?yO2XunXFbb^0-rW>{<3nB1nKmZU1gREm9pIhXG-Oz(o$&+P%0|*6$NhjTX<F$MSzAhH^~_~XlNS<b$d!P19_{4pxi)nSDd7@b6*ORA@ET2+qZ#?qQR=rV9N;lh8Ss#WqmH?114|G;#IGoWadjaavwUwzw4uM?gT19#bLzNd%KkXX#9K#zJErRg2|0}0Jf=|<Onb5!p2a-)*uDQ#Pe?yFPrfyrrcTZv-X#{nYwcQ?)>-GElBq1+fJo3K8!B}8=Z=SbadM=d6Ivq;OQaG4iGHKV0sfK%cDnQ|*J*pMRmDDPUr>~)O&b#>!xzvoej$p2A;gl&ZGjD;<s=uFZgZY>dNxkY=XPO<$PlI5`55w?;N0&kX@8Jk=WyC%h_&11gwF(34@uFVdF{=0UK8~!7a8H_<vBno#3&a7!@D1iO|2PH<WIEgnk<pSS9OduD(A3D2W#N9Z&s(?U@e&nO-!pPGxYI<vDiIxI&ES1OwcXc=$f0nCO9f?+E>k~*OCxO)LLUCq69fVaEvmP7J+_nXskk__n1K;l`oSV;<7xcS@|xoB=)3Q386qOtB$gvScq^ZPB-22INhhF?75~qCIJO#g(ZfbRN!=`<?Eo*@Bjwg4m~P@_i)7Gl+@V45pzsw)X#VfAn4~&?yor1DNiqS@iFVm3F41|6_r4p_5AtVIjmhZob`SGtIU(Z8<&W!yF`@aS37`Xr>SllA2NA(i6s60L!kIeiyOI~tz$BqN|G17rkJTb(Mh1FWhnH8LAtQ+87M7$8^B&+55#7qMX=Vy=g@R{1YD<)-H&!FSd9*84wU|E`a|Hp+((N10eiX5pGuUxQh<miMtn=@+tx*9A7cQaU`u(9G_6*{=_&6soBM=_xxYtIU?1652W^XV+DTRml7&J8<(sJg;Xdr}p?#1+Go>2)Ho-WHl7V($@B*{FEV6ufK+lQ;?T;Kwfy7>=mcQrV6s`&0HhYI`PD&&}O)$>|d$-AyqCsVzw12BeMGyLCz5OLbwNW7enOKhLB0f=yKM?G79Re4RKcbmBJ*7kn1uyOc9%ZYWA-u;$P7EC6>+hfRH3g<SZ|M17e1yg2ji~|7-0&K)g(<!La@K*1=%RmR4gVK4zuHKnNb&fCxAql9zE!TC1|4X#lYsfGlR8aQZtTnzFv?R+Wuz3bhGox>_n_12!!Mi#ECa6SU9=Ly#7}#*4e|sr#M9~N@Vha!R9M*JXrH`ol)Ws9J4iOlLBrS9oWN+Ogk$uOy~Rf>fC$BlED)BUI>*)-Ekz|mnsJ9NJ!ig4_mtI551&8_@^zou|7%n6_6tda;27~1Or$1q6B0O+6L6C+!apt+w&6+4Q~%Sxl#H8}OXuekHbIE8tzpMUYJd(E0tiENoi=D*bu+W+=p!oYlrV`*f73PUduNsCT}Y{m5}N5HezU}3NffIhyG3P8yvJA8U5~<4wf5ak^v}=z$F~P#+6Z->R_6Gzu;vZ*%H?Yns$Qk{oy~O0M1xm}qfPDId*j7DwtdGaI|yJYZRGX*oxv^BbZ|Pv^_{4IIqeNoPu9H;{qkH|Fe3UFeZ~#X6P`ip(d;#2ZfFB+)Sv;*shTnFoFZibs=MsvV4&93TJ`XfxmZh1%EUKx&Da|H!1FQ;zO3g@#=B|DM!Qd0`9>@8d!Dja)V2u<I>eTN0|LGk*)~9sUibZ3_{?j*iu5BU9%U@UQ^Zk%IIEVaTZS<y%r*JRfq=OZrs|ji2Pu&$)AVyzf#%~fOe(@T$Y~KT#h2QcdSnvEXi5>DA3|7c)r=>t<4%iaCVGN#X&T)DbtYkSPcRh_{ckmcxD2`01jimXVl_FkEs!_Gw>B<T2Oj=1EWMf!pbUV`_g5!L9wzEPwac)ob^*63owH5fCbos(^ldW4kR%Ml1~-7~>eC55&(qyj?TL(b2;+6`*5RrpiVa#SmD1uzH)$OD1mI-VLg0nz!1%Bs>DgStGLC%#8SN@!O(SY+6dUuTOZJfK#<U%2)FhJl*J$bI%+fRA_a+L8Ii!LfhRoecy<20^cP^RuHo1_;3&#Ts5ITLn8&9QUFQMcGEVqm`p_~;I&?1^|knw83KdH&tr~Awu9#dP=?TRdprNWaBKWA@&yp4B0nDl{8v?9^u2Qx-su3(Pc>h5zi$4yTF#HcMviIkFj#hfbhIr9C<;s(ZUQ8Np*N0ln6r=W6>6fM)xQNKV^4_QlTp}LeF(#x2_9h$}`(}$4C!RgDf)0JcooXrFCoW11#GEHL2@L_N&ha`Hpv~(c*@z%nq`NCzI|LgOG*O#~vBW|H{e!gsuC0)9|U@EM~u&bEQjA(`=f{(%lZKLGu^771Klzy8Q86EebB;P*X6>&4TY+}FS-6n4O$mIew06L*JOCrI6r!gdcV7R>$<pLOOYx%`s22Es+=plHt=)*#CNU>uuW2c&n1^J@{6jbMoG8<}c>As*{G~+!C8=U|XieP_?<46K+p7ov$>{O;GG&zhi<V|zw>z7#&d;x5`EXf6&HXHVF6=6T_yx{VehMy=4@nMvXUCk;V**?I}W7WpiXB03m`awglgF&QqIG)nY(c<Tjl8NtA^w^2Sol5uMG2X3@wHgG#dQ+w@w@s;E+O;o3LiwDjp+Gn!4K7(&CKN3k@{*;|a%Z})DX=|bc=Z$8_Bk(;%<)Q>Pv9B~dJWp~%ddH<iLO39(2M?^^U=HTq@{#W0DHO^c2KGBfV(0B?oM-GRy~-0%~u_Q;HG^H%K9yFf2D5Dqch~_zo(;{VE`HY>o@N=<omaenNE}!bjk37eibd~()5f<0dh?0za+#1gkWvJ*=o$AY4>Du5b|(Al(sJKjDg6DB9LfamaR)`kDD&8E79o|v%IpXnnq*iCtY%%HXNaoIHRYn$^w}okM@(TX>`2%wxAl{{oe24mEt6jmM`K*^6WG?z>tA?h<ji#lWues+q+o53a07rXe*0=v0vPO82+g)3ZQW{VU`gbfiJ-7*`VtWg98$UJ4^(F<SRci-0AllYbLurlbp2+2-0ioP<vVPaV8|7TnH#+!WzNGTdbPXbem!bDPmCs<GKALm^$wQ(&>tlKZQ?;iq)UH*r0}vVW25e1Z14wvRTOs`v1r0(nDVPY;Q|asTtH(WXi-vY(;3MUf0fv*(@BpzVDBR{*Q0J{q)B-^TUq^f8Q>3&-Y)y{ce8Vx23JkywPM_ziDjjvF1yZz_55;W?);F<{X86gAi&lHn`+@;439;Lc6wb7oK17O=TIeYi7S7uf6w$XxC6d9^8I&k^lVj>-WDrmOw{HsD{5HNE^$RVO(T=&mR&F{r0I1W3Dx3VYM-7rXC~2zkK_U>W)g0e5{iye)r>J-vZ)vTUH}xHW==;5qqp*?C?MT`sLT3|M$;N{^MWfg|Gv=-!l7ar=4rc=3;$%tVJ~fpEuopB4!|yIup%3bMt>=!~F}!dfNPB`!)F<yQa-|z@3T+ngFhsvGAXH$A?D%M|{V}@31s>`E7dEbm9on8F|<=oiJl;*h}p)^0ru^VOSa^?}{Cl(v!B0ykd=>?^+Wb8v;vs1JFT|`sP^&I{LfzTrN*0xM4PcF4Xb4Pf9l#<KF$mw{(v_hk856HKJXUo3S2X0hg%%r{911?WbQ4^LRhq>y*ZK>-A5{XJq$rjk+wIr-z6RM8CoC#{h{ou2CCh7~VbEf9K4}8amIHqM`4&RynD~2L$~XsRs-$yPj*aN$tZM_;g@eH!<%39;4dz6fy1c^@rv#9E}ZMps4jiQG%ANz_a$*_x@b3h8d93M`6F#>3^}<&AfKodDJ$&lm^@17`Ot(y`4)L`NE|2q;U>7^wE2Bx5x$NOTr~mBU<ILA^4J}&%VVClfMo76AC-X1(Rwa$^z}<>#+tgC}!NJOsd7MYx$xA`M3-HnOFzY7g}X?a8d@)^9!C?xJ)eW!sIm7M7T!?zrYcwq=>z^Z2Q+AQZ?g}BW#nWlbgwz$sWwcqyFdL-rxWJ`Go9?s>-2(PIK;|tn}kd{FuYq$0%#7Jt|az{3|$R+Y`lCkdz6Vm);pnmapV4^C3UBgCUO^d%5UQPq*m%Ztm2OEqy4$5lA;ngr$W|wb>n*hF-85KuJr<c%1U_4)Zij`64q&CsOhT=bQ+lrT((c!LVt}1KI_cU(IL^kKvTaaR&<o&S_|qf$g$B!Tm`f8B>2{Ycv&VU8%k<yITGU4WYN;Vp$^>NEka^+WBJ|W+j2Kw4f}QTN2WwkAguz&ICQfn_8^nFKCyACAj8ebbBoNVS@G<2R4v`*I+6@QB2L)o!cKGcqml>?fOvgiFOqmybYz9AT@MwdoYs9o<1T1cCFA%F*}bJpt60o5J4OIH&=)yY>%PNYEABgh<k>Cw;eG+a!Tp$X)JpB(AuNNet&c6Dn2Sm0Y)PPsON!*@=g{I0!HkA0T$Da@EFSSx~k9g+H}LzP|1Kw2GNxbsz8jW(WWr$L)k{H8v0_glqEJoLAOoe9!$0?a}%aPHO}W@lIvfdkLUX;78Ct6!sI^es8ohtg{V%WBYg-K9iE-A(UmDlM>RY@UVmz#-@NN`%xUjwg}09}OH{C!_cn@o>=}ji#esLzHn@NfpVfvu&Sf8NFp!W}djtek=W|Er1ki&f9uwZT=W5R#1oP|;QLqeU4ZJ#p^V-)l4WbO#1kxJMa8H+WU|U*{5FGx<>!Y%;j-N8`&y`}Blf)R3Zl7L86_N6xsNlr^<}g%aD9T^Ief#J81Mm;KAm^i3CUq{!yg2ots*bqzyJ+DXb2`;!{&&oaFmt<kpOWhE;Q})~oysC5$}!j_gRjnTZYDZKNe{s>N;$>DRf=dQB#RNCB=c=-75n%{1H$5vb(^0G=74^I{t;N1l^|TlpPRgnpBmoHIto6H8M?2X^cMXByRe**ldZsbKHxQ92zSim&31>_rVlmvv(?~peb~enkB)Mxi(DBGI&T&67U1AmFIz9ep2u$)<g6AD8nO-ppO*Ew%`HE6y<cT$T1FMSV{wBZbHsKcK&3Wch@hV-gsp?~@=WTBsCilwz65xXz(_dg(77iGwp1BOhg@-%3!>~!J@lM^?%2<+dm3iQe5}Z6b{9QaNqfQ>yn^MmKi<<OXr?fvV_I7Pho<!^l3M$GT*B*2Nwd>4J2z~NKo9ru72I3P3TY_Xn)-&1$BkH~yZ3I@-$#*PF9N0bwV;koYZ4O;LOkk;Ldo`MXY6JYalf{H6&f)zwUDPyBvpz)W{l=Bak*}z-iFkMSZ6ncE6eH;zzn*H9CcH+>3PL<h{|Ah&L_!HeHTkH<mMIMQQ*=n8b}*6%|k)tRGvubX@Eetg8!?(A40?46bWX>DeLu%5Ydw&7X6_#qXXbDJf~g>qrpcqy{)J|*db2}H`6_Ka|1H_NGodrcVEN!=MhoP3~Ha@0@#7bmeJ}@#%#?)SU?12LlPpAF4OqL&JCiBAq{Qh%HnjN(+mtk_X>0@3ma}v$MQTxjXGh)MZYh8XiduQrzd?I?l?Vbub0=F>A8V5*$4{+dz2avJlQb6s+KoKGvZaY=YT_z5p`&)h4!j6OgEO{ipdo+?yj&0BAdE6#=FyG!7Kr9)wC=3GdZocZ?GG*5N-8DsR8S7+~aLYav_k#YDb$uQIH^?H5Srbq&>0?EXm?~Fms|RWU2QRd3UN&tkJRuem6&E&5}oPo>Vmx5c2TeX`f$6c^l{2(L(zg>SyNN%!_P&qFVp+&)*yYDOqO;gijKlO)l0RzJx1NH)6b-$5gi*Widl%XmY3oVsmwiN~ELnnG8i`a!U=xY8|qG!(8Sb{)JCersGFK*(VL;oq6+5j@4r>wM*{6Hq!vgNkH+Cs(8%}vO>{1K>bvKT^Dl8)><{B`jM&<>!b@GO{CeNSE>BvZ7>FQdAa6Wqx}>uu1Mcwms)`i@cJ@EIj{yBf;YZiqgtMUq`GU$a!Ke%mFK_eayhc1MhtNB9L~Bm_UCg_9zTnl3np#K3_{Tu3NXg~RiqYu{c$~*<AX?gZh;*3k;x{74Wsc3-L7R!GZ<L+ox_L(spH#gzh{Ze3m`H-rqux;b$f+xK_!&YoE`rRfx((ZQu`X`r4PsjeOxwFo+T2pPxc-+7!~X5fNYSj*T(!{VJtOxdqLILSAnEJ-IxhrZWt8vWWButiV$cEd$@Q!bb2<N%5`2gIjrkaY4LFvE!a)<(OMax3uDb3b&13-hEq!+GZ!n>^E&6LQdp0^1^#}5QCJ+HDyJW#E;+xR<q$Qp1OinTV$lXo6CmaFMn|G&?DnBsyRt@U6uk%VRFJ<OUkR7y+2C!EJz-j+zYYl$7ufMkW)-(kTs2VY`HF1WRud>g=n2sGoF~foH@)(M{jJagN;`!2J=;?@1-^+Wj;06*;lXWO8GAt#tcEMU8-UZn;LYO}wvRYQaUU}sIdM>y?jw&>YP@K8*Qt#dtz_V@K)6b@A|wei7VdR5q-oLl$K+^ax|F5e=m$JvQcFTk)9d9q{hd8xsUb-Tg!@7{l#3!O`JHpFxBXez<{get8Ag>1Ohei+_#XWW85y#NNc|cJ+-Ef_=_PbD7TOUXH}4>~PO2Q6LAV#I3`K?~@p3y27<5CJ^JU5qNjAzfiSP$ckCB-U#}Jo6?t>?{+J-f$yyW$|yTqhm@SLPFpYwX!Lo7oiPyoB1S+2!aTTL!bk&um(o<_!PF?qh?&U=g!n!pVr)W31l&28bpU-byA$~dVxS4Q;Um_9$Z)8@*+z=TX=!gsUvN$RLZRXG8Ty`G0)k!clq9gCIMSzk<yz9?gq0qiNB+LH`jPa#y{-v3p^4!@a4Y)~d4rlDtrCUZb==3XDW3DelO2@xRLOa6)VWQ7r^G|W&8e)%CW9&-p3JW+(6p7|kD$Ystbfq?Jiz1%kVmHJVRQSLAk+@5{tnh2<B?AzK?EFsP=gE|7FGKX}?8OoW<w?b@<Rg?4i2an3;G3e<zw!bg-tL7+S00<PU_%b5P5UXy=&-rY`P${%C%~l#7Es5cT$tV-8Y)%ovbBo7d7kT3-Jk(ky+C#>0)yKg0M9z<AD_ob)tF6iSdX|VOCCvT>DYLMcN%2HagV;;MHx&Y&M4Bw-?XnIwdDv0GPh;it5359W_pT^gC|-Lha&?F%AeknoLiUt`OqLMONfj8w<#q6BEI?(*v_mrR82Z{>CeeETSURComb)QDfR*r4_MSSUxyty;Gg51tKo=6h4jEUImW<>UL=~>6qT;{QqKdc4;QLpnCc1Gv4<AKeu;k|Q{)Iv`aB5R9wMj;Ki#2bQu5=4}Ha<tSbAbo6)LBM^=P333Bt2ucQnC@pz<U`D1HIblyFL9ljPSHn?zsLZf}jS`9QLX@s<t8MkY^;qcW#F0S+LZ_OmIu!E9|2zU_~V~JnT?$1BnKCY;BGmD1co?S;v@s7>sP{>)l}JG*;)=qMV$cw=A+C@MBKWgZ{~;kYGlb3$)~XJ1=1=aqNT}pn^)8%yA>K?bMP(d>A`L8GaFBZysNu%_FKTYm_?z^zp6BfuA4b>9OW}R!adSX=N?(W6IE_qHHb-1-$HRgLDkucP|YuCTeX@dh8Te$0<JF^^G=)XfOQuRWJOO(Jn%--NGxyjEREwVod5cQ;xy%OzR19+BPSP?b%<JDMfz1gSG_Gj+;3xov6&ynr*WxsN%hcVX}|%o4AF1Yb&-WvlP|yVA?J$I$4;aJHVw+ZQ(iu0Ot()$VFC&Y!gM<_Iy$->nlO8gQfh0m-{yQNZeX!52ZXjV7M@6@kFn2X^^cHswQZL;OoFy>fK0XUlNpbQl%q8t|mFyz>uRRUQXQ~Rr!;Qi{M5OFX4W!Lng7ipF_cjqL88w9M+(}<ZOri!63)yxqys|$b~R-iFGwub!<!>=4ZurXt6%g1kHccT#MQOVgWWT(d}GJ<n&^>z8V5xdDkq*018>3EH3hgbGi!iTIBbZ^d6E9)~Gn>nff~9S`nxem`#pAv!AFTJN{T5_HHC3b|rPiJ=$bJlR+Mw9adXwgF?0WEXLGlGl@xrLEPKG5=50g54ELIRL@-IG<n`0>%AbAxo{`%+g3USx<w9Znn}_)l8=Ed9fc!Kg-bhlh3go$&(<-QHD!sehXy<pquGohFuC`J3LEs0?8fFKo;F%Euj7_UsNw7*$HIa{q|V%~<|^wns!|mgBrOBnna_@oT?A`bxm}y4&Q^I2a*vQrcIKwh$2pc{Dpjtg(7vvR6zwr49kBE)HGOT=ZZr59(5V!%ar;+=M_;aQHm#Aq5h4JGgnv<d0)I&=?w_UXW60Zc=->-fVE&@)d5tB5Q?+nEV@@?;#oX?L=`q{|K?3}7&a=*&!Z~wX;CrOTs{$*=^Zw3rf_t~Gc=$nnorA@WA=Yja6Fy{=Gd%ol5a)p5uZhIFTZ2~gYW;*2>!Uvp!lsroC=emqV@-O%p~5&uy32C#Hk4)^QuaaWRGz6JhivMQhV6kg1sN=~?+iDP_UPVmr>ZX=jy!B76c|lL?Y>Ks43Q;CYH(O0Sc02U&HDS6{SVFd%>g#n5Ii3=oHZJzW@Nw^xC!*wRq^*RA&;bC<)!XpG5>TQWk@0qW3li#3MqZ#w&ZXQvpHuI&QlYUxIC$0^)8TZ^(67N3*`3p*0Sm_5n9X-_wNkvJiF?;AZ5?>_ArSMzym39V~EL`OSP`nL1n}Ml!qO9B?PeGNCzni+oM0=n9``<gShD5Pkh;5@2XRt>EjZ6)Yn9qwWtKQtW(Hmtzb=V;Uw?dUF8mS-km|r-zBj?el-e)1<coJ^kThnq6{wMlI1o-r|byM?%G|{lE`@PKLk(&TJg>Ief+nzf$9?)t!TM1HEseA?-fi^?i~}HZd};9XHdEDkpsJj9WYx1N;^`)Y?}6kfI~2P%AySn)+Kx)^hqDH8{@sYj~O{T_6nXqm8ddPcA_xKqAuZmqB6S?69x!2Rgbs9rHne@qUj&=ocrW8xl2otbrBFODlbJlr<2>Uimfb~7l<(EqHp&Jg#N~ZIFKo=+NTXZ+EIc=W51rA8tsUa8pLXbp(VLAym7R6N=`j;&k_^B930R!!6aqxnN8w~ER6k}?6u*)XS9atYGoP)OA>j`sXZnU!YwHUw@h`#<ilEkqgdUutO2k9unvI}$zS3O<c129H%pO9)hy>+M%j#KD64UX7vo^XUGuL^Bf>x#WhlOcmCqHrKe8dmNK??=(-fWm#Wz<xEYg*@otCqFv__0g$|}j}Ca$iD{#82v7j><=*5|aM6t03S`WhUQC7(BXxaeO2Qdnj5N0@8CiNa5uhtsX*CVf1pf@K>4-Fx|_z57wxLQOde4+ms!W}Wnw$O(W4@sBXlD<qFq*ASob@gDT<efS86fc(Lg4U;c{zr*JnxDE0I@s@^-!@$oJQhQ<3thF55C_DHR50-4bgfCMI7XYK35-vK5$g%h5FfoOTd|DuPxSc_K1nZ!+E*MsJQrFc@586SS{dM8n|7(j~_6sRUKSsRq;BKpl1epZN=WNsDi|~(=z`nSF{V~lv&pqwM%lPuSf*Eb@=}GWzYjjj|19a#<K)kDqZ$W!0CwaF`$9+=uo`j8Kl7ynr%6<5IXL<HrC<=*UgUOYz2;d`Ttj}|)h%Qm(4)2kb1+k;Vh?=Z#`=b8*+<$y~u(6Fy(`kH;9}58~P+D5PZJ`KKX5Z&%rc)*?zpD3aY8&$#FSDn&?>_hrURO$9c|DeA@`2?)9F~RT23d?0;vubjABOGugf!#8C${qe1qP2G^>g-`u{N~jKkDEE$23f3KR3lU%E?%F+4;dp%d550+5w#JwZHmASz=!^wuZj@yf}z&Wz+bi%66GliUA(bo!rtUO4N4=s*A*Efdc}*6&W!=a9;QQS=`!dzEVpcw_z{CQw(E*5~r4FT!t~JMK$>`f4~z8Q;jM7%_mW)GEF}fHF5RAWth~SlOR<ksiG^q7Q%IS<L7Nw<=$c0h@ufGE|F&v^}ONI(3udCc&0@j6Co36XEian47t`Y$NV<>EIC#-kPcPTg{)Bn;vO0ge;Jlu%?41{h|57=kvs8T+zYB@8CKO$;J(pww(0A|_7oh)O$PgtJYv{!3~-2j(wOIYy4&MDk+}}>^Uh_1lIpamkXA6w-=uNq6G4-e`+ygwcdhiHtXNvo%zx~Q$Y|py>-tiARoR#m010y4n7-k&QB#eUea<X9ll->S4*^m#lhm*+Ur}RTFzur6TrwYSk{*v2jt3SXbh?7Ex>^)XZuX2Hm$4>9uY%H9#0d|wS`Uw6(vAdP%XZFhNq3a9IF^bpKKz`$39U#C7h*~u=0yJ=O?)sz1m+3m_Z+HwjwZV48GslKD9Leha>oekJ)Z;LpDb>Ko!yL!LB`x$fF>Y6Tc)9-eu0!WvX;`K#i>@6mokMrG>uQD4<WaX(;;W4D+D>vbbvXcoc}S$NlX_$3{0iWMQ@gt3S>X7yP7DuGtK|?3BzlU*(mb1U_hbe^LcP06C8cR9mPw-Bj%?#BW^m0bE$Ay*GS@ad3iE%bd!t@(tVj085#GXWavKL6@4|hkYd*HZYNhA(|5&vK^Q`i8+8E|S|&%>)9UW&G2cz!DY*y_FktB21|-t(*jHsaj_HKVMGU=|;tT@w0PmtIkL+HhIU+jZLA8&biE(y5q;Z+YPT?ophJzAzP>nRo1o1^DZui`!#L&YY)rrh$ZypP;ZbFPC1v$@ppA~k?Q=HTshuT>GRPO#hAwf0@nHrKW1pcp$purCb39H>r!8a^?S=<z3QtoOjlf^uF6mPwRGtinB{UoBt$Go;3{=MIv*)i4oPOdWT85BMVUR9AtJKrsQjDG9Wi2$hw-LM7GXS^p<v?qI%MA8ZfjHWyYf(5&&UbWkt%AjX?sU#l6+0v{<FjX;MF?qaHOGAywq>WQ;8*KY%>BKEbmPw|drz<MZ&;|V~U?%Q)A~&VvgbjGaOI1hV`{YuBgQYLB)a8d{uL%FTlgtu~EL-ZD=m^)7Inlp^N}|>|eIIui-!o&Xv_!Mt2L?=O>2>?|4<_nkYU^{IzWJ}>LYqG))A<QCZkM=QU-vmO?ajVmR2&fx!(d(I>o@P$>HD{jnNF0teaTR_e-(54(zNqS>9JVdX-TL^$$%jcb`7|$)$GaS^vu8oQ5rhEGX`=C6r@NiHEdm4<K47%Ub*PEgw6!bh=B+6{G>}o#D>>&5~sP_s{Dk8Vk}Sgs?zc9+ky)H_j?~ICo&N%l8pYy=&Rf}#Jnz>xkmHrvhzPyU=0CQ%;ROm?4ML{CyEmZI7Sq-h4;{X0;1Uzug};q3^YZ2R&lu!%+%%_FTD^yK9?nVCSVY&IRceJJ+u{>G7cnL5t_5th2@k4C49s8{qc_c@$I*t{`h8o`0;h#w@W4X{nu~5o1g!&hKeU~<lL{{H15c;=9@}sa{t2K9E*t7zv#bZsD^Hi)t`TU`~H{55~#pA0Qg?FXl$Y(v4exPCNQpE9W#B5Zp$!-vW98@9-0t$tV7JD^w3qhIG0*aE>Z;7=Vve;+0Xauai6~b%b!8r&-Z8Ur{911?Wga5<geep{qsH40y_7hq4%~c5>_XZ#_aJN-G(aG^Mtufs#5In!Hma>e8<N1V2_R=g|W&1{OgxrfBxUUd^-#n8_(U!-G1lK@Bi_y#))l!E%pKw)!KfVRQsnf@gD~oyXlXyp&SQeI!5rhYntSpU8cvymQ7W|9d5^`sO-A>sgE-g4ps|#1Zs+7jab4!@{mcNoY|v?&kEuqfUg=G=4<#z&AoWsJe?Xu^rW0+<kS;mLzZk;mv=Y|&EL`}d4uz~L>HacGO$N)en%kt8<!=%-spHqR0oVS0R3J0v@YxGC<^^NglvPBUJb==_pv3A_0=lc!K@KaV0`8;0sP&w`OCMD&lOpxG+JLTsZ!D^`>L)*Rz}TvQ3*?jo@w@;XpqEXepOBf@c}`%MrxNsmtqYO58!=cxfzK`#1sk08P(HhHXZrrAG-Qs=RG?Ag?goI*|ulNhON|)4X)E%ETB7mj7cxWZgYPX9ZcTX&{2x|Ulf>WIWqjGDd(G<>$T~n5ZKVjPz^y%Gc(G_;U^76jg!DpnvNpWxXCoSya<o-_C#Up`0!1KnQ*duPp4M41Pytdv=QuE+>-kTVjo{sCH8p&>_&u?UGxeE4$e!+JMQbV1c?o*-ehzy9~!qrmPLl1n%qRyVqV98{_Xw!?{aRcsY2NTg~cqQ`rf${w+|<-Nek&v+Z@JS_s$b?U12koomgwOrG&zdIZVT#^I%#Z3LHR>m_IY7Q6;Bgy5o;6V>iK+`+9LGICoB_At7Cpc*uCwT8T%dhJM7xBag{FI2r;u(U=f!0~tdn3RGqAkPt_GFnF&FFg2A=gkCkn;;p^9tiUuz2uJi+2~$5vH^oW}M`SlOgbpBOj>uh{{EK_J*vO7?6m=X5k0xV$lHp&+z-sUY(KA3nf@w%vImfj8`;tLUdT44`1gvQmiiNK4#E!P%lGCe4tsA11l_uN4Zk-3@lqghG`EIQA!#<5_qRhV7VaI`_y{Y=S(=?@r3Y;K}R=GcUjd94VWFp@LBsQWtnoBH^DGS*%evEzZ>B_T4J@)TN$Tc;Mj^Ze+mj^PrEhG_q_^iULIq|TwkyL-X=T`6v&on0(m}yBWL`*X;`4~$FNia=huqv6rigUU*^V-*Z1;WU?{b1%rb}QyBE$Rghzq511S4#Uq^&Ig2T#6>+P}}oWhJP1!%JX;1sFuS%6p4lS-=ZmXV1CZSS0;5X9MHhOf=GD{ti{ctdHl{ZTIPSpya*4h8*mnZI!#qC=;?kTSUND+B?HaNu(~Ch4hUD%G0IH^u5k$r3aV#;<b48mY;_bojaw@A2DDwc3dLLW3+!}uh@qeG-}4!*0_`J+_kb-xz&mCYqqxcDw$Jrp6I(oDuc?M-pHYLNHeN=958Mpv>$<fR*A7-ebD6-aK4RR8;y>Ccsh0kn$1<omHY7b^2hX?1`tOglWj;(VqdPGzqgrvZ@CZLu3QtskY-zp_OLbF-ego%TfZ{Vp(UX0%c6SMQS_5O}0I_G>p_la_8>M?zn@9GaQN2Im{)Ra6Fi95TQKw}|l*dTZn0=PNtV!Xm1AcqIB3qE)r&awJF0Wj3N;=vLES?(4b?ac?gJekC+Y)0LrkSRY<JaFKKGN>JTlM!}WDR-*cJaDa%PHTnX-)d0m5UA_*BGGAcZQYVqy3FdnLo8{NKMVU#bF&*X6y!r#!bA))0>_bxrMlGc6$9bWYs&cP26rC@EwIX&7y%cFVmS46y)TIlpgdS@{{?$`uib3>!(P&^y|}N+n#JPtPzPqoI^rCXsl@b#-G(xMN0HTX+)%LK;{@2?{#j3j6Tv*CcvBae$w0zhbTOCYv!T$SuNn^Muv=*YBDx!9u^r6ZG%hp2H4$D4nfG6O9XgW80=F<fI)-^arr0$p&SJ<Ay~h8oHEuAnSk}R)^KjnG$1&(!3m}E01qG((<4nZ$H-C&rd+*_PC~GY)OkOKyUM~;fQp8J0W~=&dnFp00)j;aNj*jb5<x8F((xscIX4;-;MBxsIm*IP3#abCZ<wb9A{C$$?Nfb^PF;>>y0C9_unA-X35gk~o@VsyiEY3%7NG@O6lH-hQOk{7sYY-C03q|~P1GX#{ybPoI|8*McR+hR<TH@GS@Wdwx`Qx{H#-3fmw3|WS!Vyte+4oWv<P;wr}HA)(=U&@<~agiGO>I3rW1xPF7&I(5a&5PrgN%Wj?0c=Ei~mkg5<e6DP>Sm_K--+5@@g@i1I)k!<u_~CO_ek&RY-FK<t1Mjm(r3=a@_F;w`qV-++(Hbs1DE+TbJ<s$ziVicGtZT((bZL%SN04l`oz&<{YA%WO{S@-`p}yS$t#xskny7FXm3uuEO5?)dRspbWOw+kpW6ottx>YnTXOffc9Z@!>X#TTpcc0GX^g#xQw~b=?}H^m)*5Y(nzdm;fLIjx^T8j<JPKSnK`eEh6(0K_+dV2jCN+up&WP@zJSRvn-+IoJt2`638$;rfi@#)9kn~2oTUL40%mY&tU0;aj86kU>E7c{T!I!d^Kna`#ONaq_5RPfuZKMg6p<E$)eXQY6O9uT#%iziB3GkT_d)@>#GYI&O_K3&4OY>oebk$#>M+Ar-&F=BWSoThEvfXc-VX@;(W^2InUp0oo3WaZFiJ;xvGThG3t`@TH%uW>T8_ZoK+x>;f0<ai95o3PYZA<ZLia7YOpK;=v?nWBpQ<+p6m!%%_xVV)BT-Fzt{UFp~akrrnw;=ijE>uh)Hn91m=M3_#w7IjrKOk-ZO<LT;~SrF3b`nGn89RKn9<vQt8|+$X{cgYD2&3&|v3Pb&vJQoloc{pz}vD41y2R_<;6eDQF9Oa}lz^_;+CJfR-figKo^_r{BMinO2y%kuu#59<l9vG3q`MHH`(Yb|4$|G!e9?`AB8xj_E`+6`J}~&~pS;^P&w-2pcvwZV&y5D4BsBW1_9ewph~(C(~Iw@^#>N_1!3N0HSB}e#y6#Erl5*cIqe%u%X$0L?xGC8s=vmE4Bx>hvc4E9rZC)b`jGfzta-z$3=iLjH(oi1`cJ2Q~DP&;x%^)v||oahcGy%;x?ybiA$e8&v$sP7To>f+JQ36N_y0v$h)s48?@XhI*HnR$?S@Z7UZZHPVFeW3^~8L3^h#PAnT?k($7eYnM1;@_romTuZ+woLClxUZlv<;ZaDYO^Y3L?J0$|26gPZEB{9y>lolA;xb8G5@ippyW#~en+gvrcnJ`6PR9(P0`kT#@UEFDoQ85KXKh~78Y8_lB@K-_I?ik{v;@27Vi(}B=-OO6+0)l}Fb&o{sW}yU>I3_Bf3w6--JOrUoEcEmhg;;9hece*9*ik8@2j^f<GK|%P1O*TOFD-!s_5_Y<TA74Q20be@GYwKQ?)9;oFpYhi5OrO6wG9#ap>Twi1{TV&-<r?N0gLcN5fX3aT}>q#IwJ`K9--%d*qoQt@pg<d#qXj?eJ9d|>irJ`_cHA;$<<zB=qYNfolpb5y^a#l^)jd<tyShRPme3|(1v(EtMi4qx5_+qvW@<G{J**6d4O1Ulc?9a5ZXD;{~v>mh}@~xGO)55K|kxjxDBj~x+uX1hfO6kYk+r|CX3<4uTqj)*dj$6bNHZZlIx@_rN}iqnqFi|ZwfP43K3gExGq)j3SW)}(n+|vNPO=3)(JE(hI7-FS{>yHGx<sQ^k#*Rk4diGWkap?mc`Zgm&UbYkrb~BcqwJ?sd1YdjxB-p8XQDYq?K`o4s{3}m&GZasIon2iCVQHl*pCVNk;FB5CoK=Gf#-;2Vy9L5(ggB(VLTU^oM@7nh}}>IPb<F98<_4tR92V2G<v+P7$Z0)+wl}h+Qo}?WNcZ#2cgUswr6!ka$|VV^Z8-{7?AXp}4H3_ZY&26-_k_@NJ+{m+54rdw?=@jN)eUlkO6foC|!LO9T41_SU*gGUY#|>x?L6OM{=6`;izXl>uTj7(vdtT_WdJ$f+gXXA*~A(L8gU*1UQj%Ob0ldJjO?OGdC^%(Yu`KC73alz6+slO*HFuDRkyOxLN2hnP!t9fZ?I_%osBvsp;VF`qTUV*v??3!h*L`pmdKSoOqwWTQWN%%x<gQ9v??X+;7ro23Mf5v>_l#>>QuDNaj@(Sr=RRPHz0e5Uy?<5&4FTbStr^ka{&?ZQjLjGu?Yg;l;CMHzs$vz2XDb#}Z5Aavy^t&v-+ws&Exisf|h_d#4wFRaF&tf>}YOxU*ciIcD%tJwu6hS@c=1`ZD?c96C`pZ&|a74U&(xy{rgcfIDfS?yDwWDzdhffxWx10w35=%p{M)Gb4;3DP^*)8m>7Zs}oP68wv-xPhe#sko2CjtGVv^`mp4iBQ-zM}!J)3VB$on;dFYY)xbjx+&cLv>pyr6{5LiA*p*PUIe;@Jim%DjJY6g(j$}bxQ_R`4x`M^7-u4*)9BMCsZQhJ9I`E{!~CpL7cGY;fRp@3Y1QSJN}(yGnxd#I=B!Vzb%<*S309=c-y)`8KR=d*P=2PkgLy5oJ3^XB2n|5gF6X^?b;vcGP+>uS&vlZ%&=ao>&^Cjj#IUk(OstqFrj>%Q^;!e2p)@n27`4gOq{WTfSXip5a{Jm~VC6HHIZd9^%Zfv!b{X#EecMV1i`6lw)c<ABRLUxN40P@5Do3YH*#hK_Y@RK<_ior=t0Pmm(RzIyw@iu)hwmJq3Vak@ut7*C-sUlls@BVs{f#Up!0}Fo1iemEC-sI7f#C#UZU>Q4+2Eb2b*gf~gSL=8Bu$S|#v;1@+T;*nwL$G>pgW)mD&*n!uL=+5T&HIW>&BF|$c^uV^1Tb7r6KY$<n1}+>jgzJe^Ela#>(EQ;=7;3rqazK`^9a6S6ewqC9vzv=ndv@^1y%Ax=l471(8bCc}~!A_tp14$ggvp+A+l1ZDPWQjM93g$dO#{YTneU21OG@i>Il1I9$lbNTW<SdVKs2I98qPRC1~zxp8Xubs8+5IThc`(>n_Vp@Zg|MqAco^}tba)1Vy$4rfBCgv9dDxeV`D$nhIDKSqgWa=?}+6}H|5dau5$p4;<R%c>WTX$3S~@zcZfoFUf=mOa<-z;sIhQKrNM;OFg})I9<});g#J06@&QLsbP5FtMDQl%2UwY19vWTmbE-3VkZueE=zs8BKXcfQx@rU*iSWIY|RB$65%|uM~%D&bbVM6fbvsYf)*4Sx=1L)6e>!1bV1rkX7#Ab%p*S1AmF|$glQr@}1LIyVKnus31)xpsGr12)^^+Kei3ZnNTQ2u7cd2^cHok5CDzm7BS)J#`SBk&_R=P^e#j*#U~Rzt%{~VU1TN=MhzcKg=gzjN_@v<T|y)9AU$Fd&qVq=0OKaE%&wvc?nf&0SjpP*_N3zJz&x*U8$}vaNcyxN%bMW2uuiNEyhZja=Mg1)w8^AV>4dEfyj8}`2vAg)5THWoc4g8Hra9!nk!z#+ZXXY5^YmOZ2XiE}0nR9G9c8pzhSC-nTrjeScYpckcTK@y&ii%#7avS<c{K#j#oC|wtTp0bP#Om1AdXAXp?{6L2=6ml^5M+c8u3N>{Z%fU1i<y#iDxY&-SuunfBI4>9pxbB4fQZSp1^T(lLhN86Kr~zb|MrR^fZ3DV~QvX$_Q^dtt4nExz3~gzcz<szewS{>n3#CMh>$}7z^Gs@`dD0Z+mCb<z0y0xKoh!Ule+D$|34O&~*W1=0b?K{b7E8e%wF4Jsh5fQT;Uf$B%{iU#OWNQ<QUpZ>pg5X8X>AiB6f9{7Q?wsZi-Rp7LSu-X&by!|a*BhI~y8JRZK&KVd|K+~+@rS@fF>g}8dcDM~6Ab>PDTLPM=xroF|Ls_S*qs@Tr=(D5MyUo!{Zr<4rKAlO>}_(>tV_eRJbE#nLz(W(2EzAPdKXn>j|*9UBT`z@hQx$gV3^@$gJ6=P{e<0>A8Y#E+vJ#By+Z=iP7>&7p`m@H6Ce!43l%z%EpMx>_9Dim#AhDk+Ya3LP{+__4Kus=bYJvwXWlvZ_0xIlEqShV;;bwL#%<bAZ8T!ZnVfj0q>XF<?1Q5j3+pD*QkoW`M#%~qyh2G&!D5cK4p121`L*uH}>fKn?`FUA+bb6<Tk)HyR$rf_6IwL!CEg3B4d?rd5`C&bJ}Qr6{sJa)XX4ZQL`5z_fGzQs#&Z@9Y6eMtl9m?J_NmLGo3?mwB_>3j~+J|+-5)F)+>>0mO_B(BXY=_9)7&RU#=m#DP;ZcBk;bD72`BLoQSc2EI!OS+W2Oy(Pd+s?h2&#6vgjPNi%wJqG-e$D?6emvHk-Ostr|E)p7)d_0Y*xSVU7nA2fN(m=>y-ZaMTcWNf3C&+(J<At>mL?atam;zqC9!-yIO;42V&)|gBit|dDv#VU2HMPV5XrcF1NwNk4)HM=Dya}PW*R2WL5CQ5){vA!rz3Wz=5<jy7?(N1&GY_JzxF`lG_U7sY4inj>O2b=K=C4E;}&(K<@jQrb!Y^x(5ITxIS;o$Q+<qDAe93&6)X@1{t!|6q;wT`-}xBqqAxKr5XPc)I5$$e#JyP09pibG$-p6@QDE@I#_-sove5U_V$WM28w&8}MID}$Zh>VlX1lRR5tx>KVIB8@=O0-BYdIS|3`Sk<aK;DdOZMW@WXv(XN#-J_S%yRp9t{FRY*tV%T}n-W%=Gv|R<X==V=raZW1!c3)zPS73-ex3i#(YI!b`G1A|QdTf5L2zUJ-9PcP9n_>NY+)RgOkR+U*^N!DJblZ{F|B_irCF<>E|BrbYd$I@Fi7$ni&uXtaJXM1U}UAiE~1D)B{#e%bbfnPPrDO(z28UR6DJvT5D;6zxUlxP+*chgcfn3hft{Uvy?qSgL<ab>Ek8vKOq~epZP?{zk?@CGDk9eY~d(XIN;q_@fslU)Hds#{3i3Wq$wGy{!qcMoMZw0B_}~oWLnwAAw^SXo~pG;=D4LsSSNExRf8COHV-Mv%M`zwXZ{ZMW&38MWr2C@<$H!Vpz6gy1w7!&+q>6?YE!)_-20i((AK5Ub5fbfBp8m`S}~dSa^mHyti*?J}v9oR7ZhjRbMewi`R%Bm`5c%5vhf4*YDrB(&ed@W~yM%OPcEXZU1-nLqLf?^Z=UI!u7FR=c8R5yMOn;DZIw*jNyKu1$)(IJiqWcqOeB)H6Y;h7TwCp<|sq{4=sNPII!-pQ2Bk}x4N(S)%!ME;Ys{*rvxv+e~Vd4?Zg&1fMliY7c81_z7QQ;<MV%l38-Iak~V*S-v0fg#uB`Rufu}Uz<(@TrU~EXMrm=^t9p$M$qG?~&OPT;1n5jM{N>w62Jwiax5Hr{>!eb1|M=KQP2N`ZhzA}F_u98K*3i%WpMU-G>(BrD=O_R1FB3c1f!(j2{k7BVHOF5phL5$V?UbKa-+m%)rfxH$Pl{KM4V4NQ>-iiX+plq~+BI#y1MXDRgvyjl37zf3qag81+*f9YT{4$HM-QJaO6p#Fw^qQAzRkU9m_F>f^7b8uC5Q^`CiUx|!=?08JE8=NhUvOCXpapE2fPyKWJ#@OtQ!pdU3*WKC+k8G;TUr?jLVZ$wZ__azxm6qa#Xd0T%%rdnHlL6_-k{eKmGp8Z$JHd*vtFrUZ*tNS+BFp67I)XB9>U^Eh5Bq(QmM@4Ace3rkcapv~&Jd!V;r7SwrVJS2RmHu2n7$@Bu-`hJm*Dvg<XAM|P--d+_Pew0>jWBRod6>sdESGUpG?j_CH$jmo4*AWCzqw)xVt_SyITT(3rbl9F{}M;E_b0O^|Nsy>g}Hp}%|m_TK+iYPMfT*}BfCXE`6bHJgP-kZBcJ~3YsE?N;$MvYA+TADul7B@`(HtbKZv?3SGct4#Yed9j99-<Q?v&Q{dLe$rSFUFAC0bEiAMltoY-X23*g0u#u#5A<r4=}{gh4=_NXeT$<u^2b<pMQIQ|NBD}&$BrV>cHkBEsz$_;oO(}_Tj|&kZ2oGie%S=i3A5~nB=w-YmX*#@vck;Q$qwmA6lEv0|(IKq<kWIb{}g5Hf6Ml*2TONOy1W~rt|=v@6(W=@=Uz6RGwT4mZqjB-$o*j89X=|g1z!f!>S)O4N)j;yMqEWA^vAl&C!#M(-`{Gq+y|1SOfwKw!lm0Pve*`sEMketcmsb@CawkuzFw>Ksqn(pFPi01116G097H0nFuzrV;og2tcl>?WLq(KT&Je${Zs<%#R{uaQxXPA9YSFqcwqLOWi&C?@VCB<R+*Zn0SYjs<RoPc22rs71uyX=rvjPVf+1S>$Eew|R}6cW^@J`FCQVuCRZ!8ryq}%0-HeGAMCnYQzu>8be)F!&F{fQeP%|?e`<o>8oaV7-6xO>0>Ft((8hm(|HPR^d!VT8+jnb?`jXN|aYF@NRmyjNJQk~P>!3oIj5Um@sdO+il%<HqF?N$YY8P9M}mvdlSnvfbCelPRXy0nnx-|?O1{kg1E#@Dr<UPiSz_o1-h#{U-aNL*~{U%!3(=X;n=IUl_;sdM2>S^O)gYOkS@oE(ey#?*6O^S@(Wz!rp&Sg9G&X3kpM)9Wa<<R61wGT1Y0rvlos7>(aNT40o$idEyx$3E+Q5F_|K&{Nr;8C%da6S<l9<n9d`x}fqqPUAlOf^S5sdkx2f!eOd7#QFUDko*x0n=TXj1^P!I_opVyc>8mc*Ctd$(^N;n#WO<(_kzz~vsb+7f~~-K`Y%=BE~J&!`#;{EE>TKNh<$C5<6NKc&?8BdsfN~&aYAyDcjngH32}@hJ${X*7Xcw6YHaH-@oCwB!`$*?*EzE?jWU)|t>Rh)32dwNcOt+iHD8G3-zfwzg7YE(=$XUo2}0NxYzas_10&(!gl61{nav6|{0a<ZfnpO?0|W7Jq%xV`_x{g4{Mq%_!<6BhTVpy6@v<Z;j->C}x;(K|edPN_DIpKJf;b7M2B&H32~-%3WFJ2tpzz8!xb-LJdTwE(5@y4e&(1J=w=Jic;gV|VMm~B=p(;x5<}pM44dnz=fN47_qqP^mW7C@4O)D!EAm~v&BH9^-XNdMUHfv;RA$yj{^AhofGj6uT<+_b}8&Vr$9pbR$E)!BCC0#GqrEba=YMN$f`Y5K2%ffxUCsa+Q1`EkjukR?hX%>z4pua%vlT4)az-1-LKyg2W_Ks=Wp6py4*Dqo*niOfS52cq8aM!|f>Q#C6T^4tUN~j%*Ja9AJV>b^)l`;;!mC&!Dg2uYSK|6!mXSe|RBeG?*Ko)C%ywPbavcjN^nc2f&_a{EX^AJ)f6FCwV-Gfx4m(QLD-A{-PCkV_G5R70F=OF@mhh-}L2KfQGK=61QZiATWu;9yU4fou@rT~V^288}G!jCx2%8CIA2Z0}RSY?|Jl%g4IG}ME{xs^F&R{-ycEkvMdMSv4dCOqbI1$UZam{a25I(;PaMLE}{Z^EYprWvIVtW$E2$t6;8L|;rsn*gJbL;!15p*c-^WE*ssg-OBgTUkXaIvotJb_}p~WEhY{O@7UiM{%B1c796S$vxm4C-^b2+R>Et8V+9O@63yAePrp4?gw#>@Tg2(7NSrI116U>484Jsy^x_2;oJa$V9*w@9!iw05>n}W^KU~dgWA0Si7GAo2&<VW*8CXO+|$wf32t>fODMYnIA8VFa4Oe)%%yg*xZ8ezz;_86MN*ZsxdEss6z%}67TI+n|7@*Q!)_i?$T711@X<t6^m=W}U)~0*V3(H*DK+XQ(c+4P5O%3+c?LD>j+f<f(2pulYt>~nWZL~0gXKAMb!+bS=cK%DdN&t~sS|YdWwwSFgH-od^&}@y#d=$v^8(+-zEEl9?-o6qr8V5eFZ6MiQO!HrXWjPN`UqboGq;PR-31BAT@TRG0eW>=B5n~J5`w$^%LhR=x}s%roAJE#p|4b>=vZTVcJ{c9K&<g;fF)AL?z@Y|)MT#RvDDz917%oWRE&a)DW~)?n)ONY#a>xm2o8pQXFT{g-3Z<-J1?6YLnZLStak1p)KrJ4l?u7AC(Kc2OYCzv#SJp^d@<t;>()6h;9$La)I@JNC72ujumVEF*D_~CZZ%8cQLYYONlH@my03DGP$Q92c)e+HPUKm*fUD*PpcC{b=<TIMeiXFHcqyPY%DU*Cm!~?;^#V%ZH}4hM2HCl%RsZXdKrMn@r(_ax3q=+Kot&>ou5C2|WmHIY#ER1tf77d0*xw?djF*txvl2D;UEEVv5x(;%5T`H;!HH<xGkaweK!_{M8KC6B;LU>_w(&S-avw9DQMxXm+|M6r?2vx)W+o9K2G_S2oiYfL=@OHd>Sp`ek+=e`Oy4Gg6=O0zH&W)};hpD(N-DbCFfYWmj<O;f0`EsuZwaP$#W+)`#CeZ8<w#nI3D0;rJN7$wRfr#3v#@<zJavZKw8}85B4HYakpUy=U&zR+S#2z{>(@wcIcGa72}N|27E03)w^SkTSE|FCLAX|>3`K^2aqt3-2=!MX=jxRql842XLrpzfxyh9B;+f_<#wxQl5VHUpWizSitGxiW(JB3u789p9)F{jOI*+=<G-{|vpJmr<G25hJ<3e^7C`PF0?t>Bxoc9=|uz{0ktq{ru_*25JC&2t3L!8tsJEJ2BG*ba4sPR_7z=Yg#!n3vIU+Tt3MNa_`zn+I+iE=Q|C1qT@l6Cas6|mS*&bOyFZBH`v!-YVO$3|CKD*T8Z6^k+n5g$D(G+75iSNHnZO_;{MO^7h*Ub<H-*DJhLrQt7Q=vI1qK@>w*oZJ}IF_}s<bVghSoGI_+wy6QBCFmIC4s-wQ*@v!)#^nf{U3-cpK;LChM}$@8Q6?wNl7NQLB}Ycj&n=d7(9?6Alwa&u%~AFQ@LX7pX~bzF)>)OGd&C#U{?^c$ge(o)o5Xd)B(jM}IA?O<x!7Z{i@b3ZeQPZfZR2CG^<!XrA|uMv9j?pgRa52m1(wMvCCrTm`NOb$P04MZ?hz;rD_RJ670KL~x67Ic<zYt!U5z`^KdcfZW0WopQ3I#fUW!~zqZv%5s;5wrr4Xqlgv(ONv~YPHh$0J6y(~o%pz5%ylOx5l2X{ZfwWRsv|K0v<>3bm5&VvXmWW0<a1NS4e_mq*1<-r!p`lJ}Y&F<-^G8}?D6o>S!NwmUZj4Fi`1Drqv`L1-rn7NtEw}1C*qFc)gQBe2@E2=KNCR{Tr2m0n0Y|v!iFf^ysN$wO7fe<Js>(+E_5&{7#1WMjgXSu5&$8PDDCK$_FPxWayr;>w9J*H0{&!>_uN7S8K6Q9^4eNnG1wU<aWPz;T}+ta`1@GLt3<x+WU@}G!v>zeETc9cd#Br#7q2|WV1$Xp0i{+M7&ugUmb0sx!|pSp`uXsp<@6IhFD2MVy%QDQk}K?fs?I)|b>C)aFd4DE^^d41H6Ay0h`TMQG+usK@nor^w}DEbf**a<I-WM}}=DuJ&m%OVTpdT&<OBTN8mEaX^nv6NR2kXXdRlcXZrn!-#YI_+RLLbxis4jBd|V(TBy6!cqf^I4<REYJ{X-CrGP&8S0Isq*n7H{%hU*I_NOv%}!}qOdFq#=UY#1H}&fFR$(;Rz@txhFbmb*L0)3c$&X8ewDwqg*nuqu&{7w2IJbH?QWC$P3ER;5Yo}x-3P==%I1`fJd4aq6Da0%;NZY(aZ42?0UHOce`T9hoh|Q$48t?Z;N&7_tgYChRBlv2hk5d_%4<>6?f|Ru_B}jpmsgu-+^EIX7{x;?H~WyxZRyh&G6?|Jox>SkJ@!wv;FWF9C)l%&A#|}=`G7nTB>)KTQ=i^gm_8&EfC<GXh$2cWkj;>>f^HVR`&_9-#rSULkZT8+7qiH?aAqZ=sp#A|cm9~jlHgR8>cmmwK$1i>MyQ-KiO4ayYELMRonsOPrXkV<fROTIZXr)5(970}Q6iVHdO?CB#~#vefO>@I{xe=Zx8Z~|n56=PAM>fhC=-~*$^PgFf|%HE?<A*fi)%A*uJf~6gA@gp;8W3yq{qk$P0!X8aY_ND%a?|4HEgxu1RNY(F65fCfcqao*y?&J@q8EADI-mCgd`(Eqo~GhJO`ZXsiVTF+&t)vmSG%KhrJt-k0UHypO|(F(yXcN)M)WOG>=z9`FKXrYYQMr(;c_xvD|8<Z)t5=mDN+2IbU9+pn+fl#&>kX=5ul(D_f$afkq7smqSVSkAW^7<$g|-Psu}s8yYfU)G=3aU@75;&UqB_+iWT@&iCd&8$)-bXeX===GI^8xMh;jI8VbHH-MX_E4>KK(YJX_qbhCnWQ#hBh44X?KzTOH>l?pm>SXfaJz5bk*RF+WTy>5vnM#$bm9$U!q2O_hNypoY;x-8ug*q+W2vJ$1mi4oLP|YF<;&$fXjtQ-i&>~V9fsDaXpag$OLUvsmq3g6g*Z<Ny&0kZls!eYcWz`p;Kz@meB0t1p%58xSd*&pUo^ErVbuKv01L(GPi7*(Yh58usoFMP-tKWZ+U+4JZV~Dle=7g^wl_5!St+~GBye2ALE)3+|ZSUa^Nh<uh0B-8MsntXZbBcCd(>HR+v5t{O1t9dW`hD;WHqj|~S3_F*)Unm+0C|2~Y$rN>(WZ?nx{2Hq>x;A_M?HZkt6_Ik&{5oIiJPo6IQeeUUQSb$gy5jo`XrG_h!v>&C_~8=7_Ef1HzdH1Ste2ei&w)5+~l%6sS5cna8CB5&It`eEvpVNqA-wfZ_ZH0GY9TlTJ~HUCKJm7B+U}9QB;Fz0^Zxe>!6Ys0Y2gm<t_qsab)$B4Cdi598((gGah3q`dO*_D@b+9lQLbL==z#asTP%eo;7v)1VgMJIh^EuyQ@ql!u!yOX}d(o<X1Z&a;IgkYj?dwVwk`G5UAbv)TZb&({!j1Cc)@A#We4UHV`5#;tNgbGd?}gx@S<&@F@U$g<TL^IUoRZp-u9fL(`%Y5XDAjKH9BdH9AyGkiXY7_rQI*j}$%s_Hvy+l_*Wdovo#-jkhi`Asa(;1skY`OVVuv4NY~K`$U(y>qg;tA94>0S$>^mla=FSE!05n2eT*CC43<tgxySW%swhGLZXpyM{7)AZ<jETA;*_DWEW3mkMKuyS2WuGCVt!31RtHf8a6E^lDo?H;=VhZOo^H<6{Rtt9;gyrln^gS1rB6lJf`IspPNNa2Hf!t>k#;3{Kd<FAHY{k(+Kl3)OC~%Ylhk%7mhJVlkbRs_SY0}@w}VofAOIfmp3M1I1|%r#DAu+D99NBE(MJKl~F5PR0?Y&0wcxB4`d==QDI!=(rwTfH#^CZ&myhU+vNtjT<fDe)$2y;AnO*YUQ&=L;2JdRq&E;w06>I)gmJPVI*hu8#pRFppwsQcFHZ)<6|Rn<d<py=J`M9W$P>g{8n)R22S&)pg)OG`wckeBg{0_?WTPUq@NH!ejCM-+eh(>Re6#|5S-i+T2hK6v&VVkez|#Ca3`{zi73-$QcAzQ!y72A)wF!Rvg`@{@j5q+VZ8ebsk&wBZ44r%t{&6|4v*kq>Xs=Snoy?U4f-I2lNN#J`?UNdaLxKSUC0!v8T0vk9HXU<Cm9r8iib<ThR%`Dp9lZ;QcTuG@c_AvsAGd6AG?}6(n^8p=?=h5R>!XNSr6p;zMt^?pKfXQK!bS`2G#kf{g@te^059L4P*}{}cQ&Ib6K-DBqBgY=^NpAK*ft%b?BM&QETPwPc1F)k2E*x?R|H*)PhDtJF~@}a&@j&>8zXUqkg!lC6a74d)brSD#;(wI=BTd*98@(A{V?^+6lo82-DUp-1GlbbsfT0Eg_3fDExw^^#@Nu8oL6q}ZEZRYB63Noz;?OAs4&0hDVjw+pr9&5j2So};9HS#1BCc>-=77~yymM&b7SIECCl&>W0n!ReT9_pF|aYIZZ`R0dO%AGvx7{=q@$-=%N_-Sn#(Y$i0&Y}MEn+CuVm_hAB6`n>R*5m7h9s^dGffkq?w7ZS@oPjiFi>7rGJ8mf{3fbTwb;Q<uc@2F&qQkDE{PV$3O;?_4h?geZI@T3`?)(2PiyXbN-5SM@qC6yu8b>s#XCvWu22v-z8F621jp`@rNYM7k2Xj(3h@S0uIyN^zMnga){`4?$zP9B~t#V(YqsXiLTN(^r`5{(vQF`({b|n68B;>&D_Vn=!|wyv5pcFu&C*drD52hf=%SQF?GymW2hRf`<z*Kn?<)w2EYqYp4~6KSViBbWE$J#K_2fG4=O;|q=-2jLGTc`d}B?>p#@c|h?gDYwUnutEksQr%ebT)ELmtu^*0}W&K~F1U*TF@!HG<C5z)*AvmIbo$=PsJWQiuZ>EU~f>XNiqDdC!yU!Bj<?@!htFuseLNAQ}3D7D?$okI?8nTC!k1Jc~cnmUW#jr}Ncnx^r|bRT4vaN26@422*hZk_b<y62gjCNaJDFff(96TLH9>W=+5Y{gd-e9JWd*C+Tc&CpAuxZI-Ygg&w7(S1x%)?tLZ55J0u$cWWRA|5GRy*J9LE-%mUjX~ybT4X%ghms`wcvm#%;IfH{zq{dBbtK%?GlQUjAU)~g8nlKs3E{`HG1I2+lw1-A$SL$R0|Hk8=EtWKQgblOUy2k1%mXFjGAfp6MsvjE!DC$?%Mzp0NP27@JLQIKw*<<gL5bNYJHr>9I7D+70e%lXN+(W6<JWnNXGv;sp7nMZ?0KgMUO9U6BU8#h#xE!lA<IHicEHEAAu#+QN!4>dM_!+TDKV1Ku1+7m`0xm|xrH+}niu_0p?AbQoE`o-m)+2<!77U%L$Qe9Nfha08LH8Vv*)dkTOFhZbb}OxifX2S=RX?4Es*5V67r0kH;7v0el%gD%AjXasdf(ptJ0)GFv}i8aGTp%UT!$Mm;`gGNr7!0Ek!T{^HL_6c$qG%KqM7(Y`BR?*>07&Q)oGmHz$-(L5nV5`XY-Xen>Wpa11-yCvIceQrAS|t)6&^{@v$26uV!R62|4skTM*uQW*sn3<;Wnv$E>ht=D`NSE>A*i|JtmU`z=4zfHE`b@)gXo7DN)pewFkjA2$R?(f#Uqv(R*%Odd`U&8ER7;LY_^_%zW|NYy?Oeac;yktm`zlsxiX?oVBEL<$$vLu9Jgs9H0z9*r6Ie#!Dd4yJ?1yQ;!y)y<b8-*j%!Vg=QHePRfF0U-lTY}`BCf>k<e}2+uZ3Ra0bP}g!*sA>6huR2FHj>iu?%QGy)Wf}xHTz(3><&S+$T0iG{fFV7>f_B?%`G$R<BicfJK*0Gvk4X|ilUjq4=E0OWOO0!CwFcqyFF7036|!z0_#wF6+v(!EucOL=$pdA+~ycke436ahQ$&_C?6I0xtfENVsFaA>#%j1A;AL?4r*$|=P3%Ij4U2zeBz(Pcc-~Q@{b*AT2p)1N^nsc#NsgwG)0P>j5E--l5lB5`tiARQ!1bBZAp0RuC^jmCcb1VLMw5)_L>5tgD&&FKiZW)zWw&oAK%OmKiZakd$g;+z5n{{ck}b;xq^=SL56burg_GWHD98nob4lEZ&>R+oujbNJVHzh2Eu=V`AP|!(5@}qh38j%Qwf#qn%OUiL*;!T+O>=S>)(EJk^lVj<M91Yk0lVI)7p}r4hYAxWvE~o)xw7aV84B8!`%J<oBNjKSd!z|AHt&R*;UJt2qS4W<dKO(!|Iy8ME`z=gQ`YXhKIXHHjbp#U~n2hJ|pAd;U2A-gcB6))N?fY?>|0VGzEhL9WxnSQPn^G?3<8uh_!HHXT@-@+z-PdL;rvK=U;#Q(|`T`mw)?bcp~D!9@i}X*lFk*9FPgP8J5|#0$*1>{zc5cXyN<AJxkN4Lqkdq#(En4WBWb%x45Rwcfg%eWON{H&-6jgwC&R?AR_#eXzUoz4olmYUq=t0&r)N$Cr`WR6VMI~^Kx8Q-m!0R8Cav_4g147_vFKspX{-fUNH?r!`KV21Ugw3rw1d)K)*NMll8^Q0ZhTrg*yK3i=ufs)UW#Hx9qpM+Cw|YyW*TIlA(_w)$+^V|N6IIem(5v<8<H0a-WJ1VW5;~aUbuh-#dAWh#HFe2?l-#Sli(~+tQyk|Ege#(VU{8(^zZdbln#_lgI}I9UF_04=%f(;EWmd!#()&Xj;Fq?hziNl1!y0-#|XJgk^1LI7CemDvAq^JSv&BufF%^dNpjJl)?@>x=GhwM5otPGtZ;8`E@+VhR7g9C=%{mO644r#=6Ei;7I1|&E1qw%$I~~ZY!4gp&=Qxrq8~`4O6}i`wP-vDd5;3&yWkW58n^spm*x{v#+XdeQ!~IkeqpxZAG|aRSukENUKO|P;sdsO!=f|@C|GtW18z&gB$sezr4TyhtyGi+?2bhJ4946s*;~e{`tp=^HCP9I#VROA50X~#ALf;oLGA_nTvN-dmL{!|DlcPJa7Or0h<?+XOFQCF3FRX)O)DWJl3)OwE6rVqbunC6kb}632}m@u_*_~NaQ(#2S-ByT}8EN;75%&6$;0WK7lgB|4b^0ezI{Kq(4o%T$+VNA`@Z@vUL8~lxq<fKh#?&n}F9xeEe|**hasVNNs?09;*#ql7(YK`2xxT{G432Ej1BrWXCub@sQD_rugDA;Pr8O*Y8V!jo<5njSXiANa_$VP~m|w_Pj{!7!7~x%XpQkF>+Hx4+MEO4kKK>|B?t-)?VV#P6aZz1;a)nChyxEh*4z?Q6@yCto$mdt%-V!R`%{O`CpaJ%vok$TIjdzx*T)bds=#<8P@(Li9N?@=ov-yE<t*`1sa1tKDoUfoN-)kFp&9nF{*I4u{$&sYF@NRCtEw1cYcheg9e=4AzC+N^?=49neKfZpdhS;Amr9~$~|4rfo)}BI&k>2%v0;qLP^lXcbfLsvQiaaH~#f`aEo&v?>4T~$DCpS^uwn9`NxlcyvuaT`RL7~I~Ptr$-jbaCLc9A&Cs9)-<ai`*YrOzFG81`Mq+abVa|0xdb;5VSPTqytzge8q=|)&9RjdCM!C6IH7*)MJ5pGT07ZE}$F^V}|3GK135Rm{l$Znh0s2cIUA<M!K7QSp!J!v<H<!Wial+7ZiJLd|1MI@~kl7u`+VcTl3=&ydT73NDr|p(y-VZnUi&_42eb~fS(A;;-RGI_EG>m8rn8XHTPHesGw9u9wzxC##@Q@r#bQt)wqQ@O>`LXN$S}@}}xMj=;p#V5*wi5!N(|lppKSzn+1Lws+j5Cif(?*OYd=>o3!bl`QnW-lU*0h;3PyuqqSuRL1y_88Bf8Vh`rS7TBkiDfPmDB95YoWkKTD{^6Zzy?KL`-=Ggj9+e5MoT0gYuOHs{eXi<aKU9*)PuQ+^|OZKKkU3@D;Kbw|sYjb*d?fbdf!;I(tR-?(V;jCRf-q3XRu@+H2miX-#6H)lL`iaFlFUJHv|gYJas6BU6*CTPC@MB57l6b%o3IIqL0J+K}k%%6hWR^AF5mn#gfCWgB1DsfNIKcIR@k0@rtmR1axh@f`&&&7y&{F;k{9q$ur)%sp68bSwD3=KEpvE{saQSf{M-KZ&|!bhLXvoJKuBC<xDKR>IhKTL($i2RlS0;bx}CZo2jI55<lGSbz5clbQj2YJ}K6%KA(oHu12TxsXEXmQS~(&&mQEhBCagR8>`8Yo{UWpP=eVB3#lhL@!)+P9(_&(H&!Xhny=Xn1Si$dpYW~f*{htrx*r(8pc-*`ue?gd}<&<0Iw9ILCRqS-gKCNHRBTwcs}NEx1Rt&f5jk@o&sGwjSX`ELGFUYALBw%&qF!eag2AT`Gv_bns%m^yQZA)FE^570l$mh&gi2&LiCh>zQ7pVj<x{2AbA1SmO;~(@yIqvrU(hbWM8fzp*kH5n{^Cu=}0(GRwsMSibru8U5y72CGpO)oUXxnex{|P0qNTqNi!FInpWHTD0sl@58|Y-mmp)BmKsOFxWz@cr8jVAFC?RiJEpqT*d`gE!&9~-sGRf7{~X$UbCLRxdn+<+u=0pw&5vPCJ>9EcK+eSTgt9<!z=bww(&he`%hE-J9wSje;RTu^N=34%0b@A4=OE}+cHKxvM{Ct^Ju4b>#_}&8O~l{s7q;@{ZD0v;c{%xdqkp3o*CaoPOYNWycuAT9BM@b)K^=P`mYJ6M6%=c_rY!x0KI%OGi!U5vGrem}lw8U4Ia;>HAbrg;Yj;oc$(Y+f!Y~@k0Z!!pT|L4Dl&|0BCcT8~6VSp#;yYALH3t&OZ}iO8!OcfTXC!vR<``TjW4D{Eyw^3ro6rGEO?ezX<4!12Hzh6{f|xan<Te6NYacv}cZE|DOFI2LWfgCBgM6`iYI8v=<|-RwS;X@UYRS239)<q~lL<z1e~})sS6&XncVTB351CHqhxfBi>t;uOT^#&5nxlo#xo%u5@^Ildm{jkH_Ck`P2bsB9|DNtsoqe6vz#^RZD}~HL1yBC#j7nQ3E9LsLG$ZBCpn_4lGIN^a2BRbJ_f`2yyd|03QnV{~m1*%i3r_*^>+!YFZkY|<Znm>b3;)+4f%*eGp2fuDCY2|14d(GDAqA#wDPR{J(ipSKH0p0=6^i&%Bz(z|aC=?T`&h8muVk=0$(#|mE?@7G<DwZUriOA#*-QA|qcj4=jMzemj(otmCl1_&39&MKKbTE;$-NGoX&)**OgaQDcit<}gRJ_rE2auhPfz$_5a6R$L>2j(^Fm$B{oavx171$wE`l{=x(S~Xnt@uxF`2D&yJ5<RZ6>vHfouC2qdZ$`rx~wjrYdv#t_|WWo>h`^LdZa>ODTTloc-r!t!yXPY$NB};7Yi7=u8Irq`#peofL0iI04u2Z#`!_IcY|8tX9gdpc}y)^-`&nwNeW+-)0*t#&H-lO!S|Kng=`IlnfiTB5sEIj1!pIA^GYv_jiodCRrc`A$n`2g!R=@06Uo^vgZ~r=fnvp_4$2)!mQcPP-{K&a${XS<Ypb6NS*r*0!nM}4CZv+gUV|I2l2z#9m_Zgz;6X;=3|JXn|fy~B8e@`Q+%!G0tRLzoC|JltYlLcUe#|6sQ>*u1TyG@4y&VhOs!)ctANE;iQt|xdpya|OE;oAo&>(iN8v~Gh+F5;i1z4Np*cMe$EMdOZo)Y9ZGr-@XE|UKdEn4Z%?<4s1M1S#3nCi2;^fA-j>$Nyp)<ZI;7nyNcT5Xd%}&QCcUTZ;&pvcbJPJnO?8Z}UVG}QdI%2DN8f;F{DtD(uVMQ6IoKf;9a36ynU!#)z$$r(Oaw{M$7~^5Y#9|g-ozFc(B@IpV&fMzUkhEF!IZVKm2my2c8J<r)2D{oDM}frAGSLP_hQL1twimLYJkgQ5d|8Rr?!;hB%kwM~r6Rj1YuXff_Hw(!JQtPXO%68Z?Xvbrd)TV(>rp=Dht*<IRH;)5B{;qIdA5s$G@Hr9@Ej(w61aAj$X}{-CYLusGO_?Q%Tg4vwh0+JIZ`Zp(5Zh*`+pwxXYZ*lhntIUc=YKolv`H6#*7_nPN?3RL?tY2xC%fTH3TBCcc&>P%q?V&^SiSY8n-eRABA7AJek&O;hNEcY*x}pCi{jFF!M6nO#>!A0_8N*dT0#d5zfM3qMet?ZZN2kI_9Z;#;s=7ZJPNXQ|V>d6mpX4yFCqG2?=jZmL5~%9`OH0G_~Ao4bzDXr3A6^)CL3nha3Ne#s-T&hY6O%e8TH)V2`Z^4A>NvMkEcAJ=&!>Pypjq=}S$K4MsNhwF`NS9}qHQgiAGtab0Z%&*$W31|_x4CB^CF&edA;8neu&#RMfcK;U*F`{gl*-KkPbydgV96&4&~Z?dxc)nUA=Boq)iXdM;&AR&*D@jbAj%=4ez0J!Iv%d8(<hF><7FHzW$C4L($t?&V|48NHJj>HIVo;P39jkY3rZ~pMJ-uz8wi$n@_<wa;lkV3nCM)#Y{RoGzhy0^Irs4L7{k|574GE2gu=pe!Kf;cKo%FYFlE9iWhx5*U(%3esBN2IhnDMldLicKZ0RH+bV1Z6!dQyd2aT>Df)u0sGAT0v%DQj=8MbmncZ=i92@6ZAt^Hc{H@^JMR1pGJ_(eURb8Y{&}@?{h0^%V2Sa)(yT6TwTEh_-!dpb6+~JeV893MK?ML8b_@Hr!3BitOfE&t8An&#YF-_e<rG>o@;MNiQ5`wDliQmo)o(5yQI_us<+?(0qbUxrn*-~<ZO4@v=7p&nUBmE!%{3dX+9}z)sYoj3>MKCOBd^@EO5-5*obq!C27o!?%i^mUR4aEppXI!1OI67VwMJp4KSDma)lUJf3xQ3B9YgQbbE$1HIjl={Ouo+%H5dPYCB(~Plhzit0Hukvs`Yq{u!!g$nU#Pz9*xH<+gVtZgE`U%ZAd<Ait*%^oHEC8q0Br21zd23$KLR#2VafNZmPfB}mPPP-E7-_>AbzA(jkX_}kEO*SZ&|ay7CzhIKZPYPR0C>71P8l`5dEX-vaF*_7%080gwjN#%s!l>WdlE|Pm-8EPd0mcxB&=tb#=7}|jc<k6QD<N1!9>PWFC%dk~)#W>Z@O&o9#eK8F=;d372;Hn3`*f-0fFnsLP6NF-XYU;+ZlX-+UiztL(T#L{_#}BGExy3Fo(iY063dJ!>9|~wHid?28o~K5(yaHYWU4c@mAirQd+Scr+j|+EK%5_LB0rIk{pbh?z1)90^XfEUS8Z^Iontx7xY0+ZvCHzQUQ=)3$X7%H9fdkv$XxEB9=REn`Rh+jh?K)99>n=QLI4|@x6)4jC3hpcf;Ly!uh)cK4k?$cDdyqd30wgf}d!aOy;x-&5@;qZnBgbQyn_KLo;2pKcMOBt7`Oq;^ReD0tXx@;^Pz{}$VvD5uE*(<Yn@e-hVxe=Ny6GoT_l|pFeQ~vN)ICS-n9gLEHDK+skzx+{aB%X|a)F)cn594jj02<%lXTs>k-Uhpe@hCo)ZLud7bWf94Ys_VbhsA`oOzG=?qh8zB0}!g86;#^FMXxvz1Dlh#C`x>t3_r~3NE)}ZI_$NSOS<yJCuhA>LbzFa&m*0r+69sQ?HQ|{rt53b)sdgGqGIU)8*TVw~v9%E-^K0?aFCJSXZK)^<)1Rn^J&x(-7--2}a3}cEHC@<GtLwt11@x^y5RIWKT;~?8Rw11qg4LdRZ~ka{-R;s0}dD^~RlR+6e@YqOyT%M);(mSHn@wSQ?&uc$OYRLXTiPQRk-$RXg33Hg|R4EvwB%#E?s3r+f$9I(i7ju}*#Bq}+j_V6=~FQ^M8F=G)>E&sl=CCdmwKS_gMSJ{M22O`#|gEi8;EXiU~iW=M>cbo|M&<~^2krlIw^Hn&IGI8_TJ>%BnT6t7ZD+?YIw$vq;ww%P1~<<dnNADICT!3C07I!bYFb4W1-HyvZHxF*W#?f08-X7~$PDaKP3c}ZKlo&z3igIl4*#-&XRVB|ZJpZ$9Y)OX&^^S}5|o6D>Ft<TiyT~P%&{G4_i%>_WwzcT9Pi|*Ib$Us;T<`bRu&!~9a?NXxXteTRP!dKBSX%1ps_@>iZZ<ZpN`uiqz<R}0W&~k-!@;lH*0BE6-0S*VnF;Q9U1andqo=m!+?Y>WS!0bzq@9=4ux0^jdyrr^F6F4wN7EAUh#@BuuY}b;a4T_y^(89O1CotNv;QKu#Uh&Zq2q?YCrv*xf+Zh0=8X?V!!+@oeglyUTm=AO{Ul+dpzcwu%zp$v&j}eP5gKa6KOe~}*=M5%b$X{;P!?rp<Iql=AxRbR+x|cP2p5wwp;_WUwWJ&`}*cCtk<!fg_>*#Op=0k?49!<fbF-1Y*jl$vYon@PMBgbuO1r}F+38@H>uMp5%M@EQBFl0}vEqSftZkHXSO~d^DcmMOplSOTmh)&~kd`y<5p?I`?+oaA<?Z%0jj+J2cD%i5QEs$@#+Qzo;7-a|XCZ!v^p1(6TXMFTYue!ezJgaj>u<WyMU?9^*Pli*GluNaxF+FS4ec6|aS)u*Hs#ye_M>omcIYrKXx9ql;g8@ocv*bZWlkc@Z%6Xpnj@~Oqg+B1SUW9LDgP%9^Ay3SEsptZ!f$v+{M418{qUJ=57C0c_Tgr$52I^(sUj?pw&sT)x9yo66?IoTjLm$&iAg;HeC>Av4p}gQ<gc(Gp3h<Wu5zaL84AYn@)*Xv7y0~PKfwI)gorZAZI=u1oRs*yr2BDF3sIe`9yj!iVD?G^cw)S$lgDg3=8ZXD@9Xg7S>D}E^i5pqYIZ`AUvh;Dgf?vEgP52ByMlw*c@hOJRB{rk;#5^wgUdVJxWM*<_pr$rWLQ7WKk=aIaLxx+Q=#j0|1s-)D^XyuK(u{{bm!5W)Ftoksi(*3^eJu@ghnR3#?rm4-1H!<k${I7V<JfO18Z;anclTwP{rxDWK|=`qd|$Ym2^{I%^E{)WoA3^Xr65EjiXe(!86+}n-}x;-^pEkc<wi0Vnoz;Br_aUXs`uiqPF<mIgT|}O4uH8>b5I<`VrrWos%adMC2UuW)Gowr>#)C=WyTmFYTVj)M^W>GjX6Yh)^T_-_W_&76F7f7P%r4gXSuC&W5&_Ua6Apir3eg$)y`h9k27}$MWEyKe;})o$L49icy06@TR>9&D+jHs(EWwfvs)YLj65BqC|fKJfthOrD!s(@+Y=vyNQjK94aFhC3)Ju#dWUl%AM!92cOOJ_1)9K0sL0x+HD0fg#s^2O<L2*(UGD?n67(_w{zn4|MROaY?5}6As8VM;m<LM#RH6zrqe->n^YAP$)N23_Axm7Rp;OZ%BFa%h2P)R7?1A4n*Lsvw7pHa)%Rwg$z!VpI4%0}wYMT6}0qlF07$rHz?W0nwJjQPbejwvQl1jjBjUgWVkR@}rpCeyhf?+Ufz^;A>S{{HWs12RZC}CRtGlgD~@I-d_-ki7Jw+44x3=;Csi$~Gqe6-$>YoIx8edNp_8uks62>#Rs@k0KFHwR=hyo@np)D&^3Z}N<tnr{WYV<t)j!FV(qD5hDtFfn{v&iM_tE@cVM&GwJ7l%|f%Jlb@rbXg7B8i8wffh**i%rypH9)eOSI4r_#V`-1!&bA2Ihh?=0S!j|`;)q$c)Jvg1(ND6de^05X%^rbumLWK^qzq5!)b4-<dy4OU=;3_M=I-aWzUM1lipjGsp#cnP4X(PA)ORt|8A~L(9cIr<w0gVUVlMCc&BqP;*SC+Ej+72`t<Zt~EH==!f$D-A!>Q|HOaEu0@>m_P>fj|)>hdb9`WAykwK-be2qyL)*q(^Sh+jND41blK?!Q#`?qT|Y9JQHzl;|aA`+5D2g;MbX(@r1>&yNa`^`o{Cl!mugvb$nwK3Cv=TY4$XamGM&!V8uUS(w|BMiG3PKBp)lFU%ul?3`buKIdIPGEN;L8lx*YeePm|aXE&8rij-aTPrZrn9;j{o&Wf|Tr@r!t|c7Wg_=QcMaGJg$5w=<#C^#X4YEn>`o2FO`rm&1?U&zvgbzO-{C&G{y}bYW<L}|~$d<yV|7hI4elytEW6f6;8b|afGqC5QdwJpD8-%cQ+TfDsfv=RY3GLd#U3h)PH<$b&u37woy!P1_rd|6g-&0!`F7ofcei;7stA|;LxOnjBmtD$X-YR@{tj{wyIw9O18g9;L&17A#Xs4bFdjJ08qrwA7%k0B4y5eYm{Mk1_kQ{4L#LkN0UOP;OMFtQ5_Rqim`ltW;{V)Ia&+tUVfjzES{IS!}HHCMx!aXdrYX!cpdi;x+E6VD`3im8cVhjz-C>ZN$^pEZL#8l#%Hs1kvN)hLP+!<rrK9eU;uK*7Djz7P{deY^m=~?p|<xOwoY10h0!t<ImB$9C%c^jb7A!&`0cL5IT+>>omZn1}#x)u_LhGY=l0CbS7hG5oOi+*oBm+OmpIhYQh3w8Y67xiUwC{6W=Z;APGw&r$_cSVO)<aHfG*#FDl|N6IIem%_N<8<H0GWgjq98$KHxQ}-w?UFn_gx*~J1S{SFEZflV(J_^*nmbjn#Ar^@&}F_9jeUpvVrRAZfS?~^kp;nJ_mgeU#KRYF;LCw&-Nd>Bc#LZIbHtQxJs(;^TQxNFW~R;r#pA{1?9AF%-}`gD8X_}FmxKM<qyr?PKkEWh=TX}x8yg9UnpoW)1-_k2seED5x6wEU96^}9xtnr<`I2zKN=1M>G|WZT^x3z#Vam5*e?iLwxnNc?#95$y`2G?py;H}Z9V@ApxUTb0D(4Nm(PfCm`f@c$D6-DdBGvptW)?0J(|v}VKA1>^7~vN<0t=B8TvJB$>xZB%VghL12;1!Gm}YV&vIkS}sQ>Yo_xJz!dP4Tq6-Tg<ng#c;q$vU>e$3(C$BP-uJuZb$1;8~(ni@~J9%`RBJ%N>#+->^S=YBHeQDZL`J?az|XLptSF@dpRoB434{E<SBkEY=rsns1AZ@thOfHAg`@i^s^9p>>i)~n1Qok+O`l5=8cE#}KQiDA>22jJ_OU(NX2j^WJ8aR&<o&Z)G?z;;ES;PE7ojA_2Ii<%0xu2dGZh&(+8B=LiCv7(U^%BxA&bN!ggtRyg&q@9nzBJ=d?r>M&xXM&#L%`MjP7qrX5HeLxB-LAzLLeM_pzy@-Q22cekin$rPbNeNPhqm5x;ITmf9#^pe+)$1NQbY&02Scgi>0=B*mkQ0OS!J>SmF;uH2*%LAxk4;qdkl4QYjPh%Mo<Rcal`=1X{EczVfNF9(H=b$282tu;G=?+IXvL<avlhkcZ!G*Fyj0Ru$Xa#$57VqtNM)Jn{F5z9u`o^APSbE3KWA!Mxq!W$~J2C&==!)gK>Sz0f<0;wmhvVPVoX%<9r@QyZ)8=c)70<LD4TGOdi9YY)ScxZKZV@AL(NYd>*5fZK6!GR@LzGc>Se?e#@@QF{iz!dpthIEK$K?-p^4?L(eFpFAlt$RzeQ^@yYEf;w0U2gFTh_UcK3KN2dbNgC-se-go9|PaTBX><&?|40EX)hj6<0H5-E{19pM5##8R;dJb$W3&nxMue?4g-I@3))Baj1hB-;B0qygz&x4Cd`EcYt^uJwq40oVBZ0etX{P@TF6YvkaAm^hukM3NGd2#APEk5El@A-po%;{9m)BnW0fGv1ed7rt|;=`3QdKxSVAQ}vIt>CLGtdlw|m8FTmDD4yvmtUb$V=P9<d6>rq`}ju(!kX|!hfj$)pdX;W1Qup32-orJ#;oOMk#}<$3?C;9Jr{*}Q$N5iEa$akD=?f7_);%~C+6|fc1vv2ha3FGYVf%}Y+@@Q5<O<R+Ldw9dh3W)00$>}*?t-JJbvrV&T0W+mFO_=X+@7a-11}B`&CuOb#Spe5jO}jM{FkqDz*8-1pSN>whqqAE2%G{RTxe9D)1n}NF?acsV51xE;f=5x#BDrq)3Iz1fRd}*q>7ORA$I>tjKA0S3g-vo5C5qg5|Y2-&z?0^SBC|fJ4)I6-ljqJudP(H;qRx&g|T<y8=Bt!dGx_Be`NAIBV(~IUbja(7(N~cX$7NG+F5sC?&52b!=Lbm}s@kMNbq;wyT|qn@PmX+WJ*RXr!H*BzQ9^U_3g&B(?fp#4v2P(uPE5SHhKTeFR_z(?pKDDcktEZZt$?usesa(t^XW@m(5pJIgD+qrjzEG>|rC8gGVrqdk$irvU=p3jVM8ei#jVqY?<#DeL=BLPU>_3hsx~j1GXq@SJ8PjD5GopHzLYLyi${W_s+V24wb87JLHkzK8LzBchTSEPaLxU<Z^fqt%~^*_v*vt#KctU-k^d-Owj?y4`K0VT@c^oDMR1S!#B=`CfsKWnshZ=~$kI@l^x3ey`n|8k|rJSwQrZ?+bndVZze%=Xp=^F^9WtGTSPy;KK0q>f&i^*kmG$R4P;___1W0K{Y#YjCZH;_+(*Q-OMI;<=XetwTTTNhjvq<=sUjYkB~MM2Plv^x1%ip6-XS-diQ9$FCN(j`4b^Dn4QoSGxS?`vOCqt%6I{K-Y`*Fv*J;lMpu9XL>0U}Ij8V(o}X#y=u-VQQrOgim{!~RsB-%258|Y-imZ79A`}UiB^QL2-oU+Aq3D?ER@3-p00>Vhlb~46H~({Jvr>Hd$~U4)bYx#*<pjr?AH$k@C=R}WkBR3AwV6B|b>+=Jc}$PFEM4^Uv0nwyIsz7jQc-DYzzYr|J!)AJcHKzdMr+m3Z7Y6x)~qHUO~kD47lQKTZOZs@c{wY7qfMk1*JQ|vOYKzWc?p*S30Mycf%G1<lIK#+ub@8DHD&1<^ik*eUwlm$n}T0sh@|#rl%gHa0dI|o`kHsfl9Fa*NwY8mGBmaXoYDQes3rQk)OwJ=cR+6aIhz(>5nrZivNli+f1|Iq4rOM6=<{=U538m|1zCew{JI8s6FPvMX%FvbBnmYJr^Km4AgyMR+<wDp?E_dr$CwS3C!35UR=n8_b|gATAcd5Rk1^-j7|S9aY*3BOMGh%|R(I%64YOgLM7LK95CULfZ<P?UKinZsu{y1r9SasPv8;rifzVvXt`!rxFv(1+dqevrNsWWdTs{10O?kRcby5@7O&=k;Uuk9*PI&5VXXM&aBC7C!r6N6A0|F|iy5PrnB`l3ZeDZqJ8ePmE(8F?!cdcOX{T521wVZaiN6UCu*(1NZ@K1mJGq`{j;w^hcwwoOQ(Bl7fNT8;|u2V6Yx=Ec=Ap-O>l7!n*z%N2yhI%ACKghqCRbApwk>K{8WDfUEP57x{C{$JvzVj%dK+zV46VbS5@ya;35T=dGfbd}O;lY-zDoLhtA1d8HI`k~}tSd>JtPZvNG)j!ZQutsH8lzUEzuec*$9efS;JNhe8CWr<q4SyEn$MwcrJIW><j6)*F8iReaMeHL6A7QqX>O-oaruy>5kkjN5m50n=UhKGVr9E@IGyuta4FL~JR$=*(%(=~YfEMM)<g+tK4&{QX+d;kR>~)!Tb~?ZSa}v#YAfd3Y=gTvl7fbHzG<)dYx7NM!rCO0@PnsU%uI^RIPd3JZCU|x{bTG|N-$sTLdx?R9?JQ~IX~@G<@dS8^G)eJz-DrmB8!#vkW1B7^~K=A2(ox<NYBpcya$zsP6h4Z`O!U0p9=?mYsLpQ52KqZXS^ASEzDDLA4C@Z7?_bDF1V+$7EOI|Re?3Y?f3H#tTsy}uURrE1#2_XNSk?3iQAq+c|6I`yEdXR9^hO>0r4Yxgg^6Wgl+V!(2N_1Khx_IH(?z5HbLRbvz)Do9dHPi=7wmCL2W-Q0%;C+gC~lx{WHg8l+^HyVF@@>*~=Z{d#k<Y808KV`0d$;u89Fs$Ifm%#TL5oGN>bxnkUIFU19LKd`se}qBvhp=XeyPk3o;GkthCSziLuB5x_?gfq;m6#4MINpUcUeq4H{HCUI_P$t=PcCQD7U$2sE)PpBS)UG0sdP~d2pXiFZ$&>sWa3u#TB)<|8xtR!mpQm~B8Jj(>9$O_6DG{ug++^{e=^j#9%X0nbkZ<jR$+QU{=S&!r}Kdcsa;JYIf;&|=zY?s7nrjkjVI^0<$c<d~(yHwCpE^mTGWC3cHr6{6h@daf^ie(QvRn2Ki|6zZ&@;xvL;3C43)Qr0B|2RT>Pc1lD9&Di)rFkq2P?SP~4V@EmwkFZ4<Tp%JHdXb?U5!#@;z_GCzxzv}bu0@}Q1}STqA3rg6efa`O{eyT(KPci+D!^3b^&Ez(=u#KIUo!KXNpZwp7S!<Ee<sr#=JDa*wD<B3oJh^y}X!0^;mtkr{yf6&5g<4V`|)k|KErPmwT;cJ5fuPpjn=pVQmM;Imac}nV`at32p^+P4rF-th3bu0^73Eh^j%(M@tn43Sh%3{i;c=!N^pzk1hA*YS#hgq<6DSe++r->#<_+PX<HrBGj6XzA7KxNb?qa5t7FMpdtrK^q9zMi+n#P#xvNk{ZtWb7IVzkTEvlM%`M(6d6Hc4R#U!McL(7hk(ul|R5*i(t$#XG(BJ!<&s`-jfh0uhHu|7q#`eJqde47yJ4Zfi*M{NHO(|>?pk^h424gI|t*jPgRtq8thU+hG!KXS6%0`>aJnw4wS>DxF(IZ2i#>(Lej0}hNagFXbnNzkwm_u*d8c?2?x1^Mk*<Y5fN0C{Aa|S+2n!cY4cxcemHgA(Fl9auNGUH4smQplHv=y65Z>pj)%pJ?hXM_W%16-V!?&%@BywR38Cbqa98@9A^6M`=uQ(ODQVXkvz&Ku5pnhZPD-m-by>q+OT8wedLmQpv7rGW8w-WA7)fG~riTuvPe{i;%HJe<PVr*|c@f@BY1p6~@Sin&4jQ^2dC+m!4PRSGfryojH;FCC~|%w3b>mYrm#qr8$BvST7^fe6(q2&+zjBJ-zCRGu?YbQfGlMrB2c^uNH~c}Q^>lkbx5^5M8wt4<~Xu$%Iqc{O8~^ckS=ki|5N%`fdBA?;wLXy=dlEVsetA=O!Zbp)yCu@$g=o~likW#C+=SJm$*+^fKc;#WhDk<T>4yp(88=5R~DSwDA?Jr$fTgQLieba@q7f3?O<#CbR7yV{;6>2V{J77BKfW%-v|ts9PNc5*x56K2XNaJlW>7<(Ka`qH?x&yQw!v+^;-@hnY$Lv-dD-)}6<6fLrDuVY!?g+7r>OVR9}xyotELIMxOBG}iFRhWQlljI8*tqfmiTc9BX!`@Jm{9~YNM@gR(+f$Yg<IYOTie;$POIV8gDX>K;jF=q;cKOlZ7jpuolyeN*p32f`^=KKkN^%|Nop^Hw@X&l^7Q;k-&SM;0DXJHn%UKwN4`Qh!_$zCj8_03&q}<_sSPFa_*CI5hCP$Y{W$lJbf<9C!U6G$V9tG-r$#PEUuG9gMd<Nw5Rlx-OAq(bo=?Y%P?X_l*_|E-=I@QuN3Q@j$1M!pBrYOL}tfG7_aNvU+?V8i)oF|{%j5FJ%eNHCY#px$LhCCH$_4~^7ALPe5*!CFW(rt6(GeHGHO6*~&(>2`-C9V|h;i$dmnKa51oaFG9X>-en6wRb|-IMak>7MY|RV|2>Nm$cte8sr7n?opg4tlN>d^B^VO@hbs%x3@1>DV=WPwKXEx27+&RbH=CoEy_<Pc|5drrbt0JLG%8eM!^drR-KSje;Vd*H2_IG?<x`$0((!3JedV4VM)6n!2G>de51}xkb49U>^#}kkdRvgY5RD&)dA$+60-h6kr0jcz0Ckpb6GK2fo}~aveZ=+aYsBU?+*Fo0Fk?ZU$JE!N1cQ-_TEe++X-u#yV-x#jjmjAAb0raAuiZ&U4m<m^0$A23k4m$Nn!i`vq^DB3Awq#gZRYk(Yt#o6c#iHZw-dqT9H6yM;L^NP)wA?=EXt{Opepfm*s(e#w1?{7q`QUkI0<T5imiUT87Nvf<iH@FeT9S3uS9bpyME9h8{J=Z;1`>ZZd-P^zl8N^OXkzkC8xhoWf*f{Xtc9CBOY-8ny1C=gQ0GP6;3zz$%3wN{%1jRC8~e)<s?xL>NP6f{dM>(nP<%$-w;oKyIwQqFtz2`^dI%+^R1f;xoG^BAx60-mJbLNzNsIPfV|(Y7Z_Fs1lWYM)n$TqdWTcTvxoDj%VEs0wGdJyp<dkn?yiaL2_<6ti|F5vvr>ARD&XM5ZFkL)znAKqo;+Ca3n8goFZ8r2(7Vj)_CIfV3VU!<y!V?l<Au@n^PzasXd}1O}Ppg@<9e54Mf2u<qkhF-ByXdz4?2MjMARM$vLTE1)`bo@Dutk(Pj!r{OvOi|?s<G^`8od8*HP>0L3hIjdynfVfgJ`d8<)UzHM<`|_HopF`78#m0hTveuJ1PcPuls7l}Ma=(oCarW-3u%9#nrimA>crw1!7zt}<$BJxHAC!W30a;^MC%@Zt1n4aM5k_hUlcRSDNceacZIK^&Nn3E5q-u`kq}ci5HBHKFI(P$R2R85_jbxhaK8|)`8*F!;;(v-gtneLbE4^T}W5NAKfiw2(5~4D>$fvzAg+@+SZ|e-oRq38qp<pCwUFAZ4a`VG=KyPr}r}qEa@>Kl7QrkF2EMSA%Qb>eZxM@x`Pri`9TyENuLN&I!$OUZ~t2p|#5*O{i=*eSjciD_p8el@R0zzM3ZV;MR-^^@23XrOk6-*+Nk*!+Ey|bYDZd7edfml14HnU_JVExO_r6Vdwb$qfnId=cn4tN`wr=j)lzyCjfJlWDlZtgTP$H$T#MXwt2JJhX`Vs7dFvKft)82qZ)wYlB1Z@jL}w&NIO2OBfxaJ`<VGo`??8VPs9cRXEtABO7nq%zZ~FiqTIH8{N`XOKEB`%*C<v;|!?M1gbaYCLyN@hw@+W9qgugCT)etJFhnm_nPswFa@@E7pg;?7Yl}ukZOu-RH4mnXC*GfO%z)IoBDrP5CBKIV9E%92xK}W$l1|!LskKV#&VeD<zR4C}`H(OJr__xUiRbTyH~Bdv46L0)h?~rXK5!@UuJ3JXtkzS=044x-AAGnMM4TTuo+lv3A)q!6~VR8VG-iMOj`m(5+70nZ>msp8$NkL~x<N9zyi%-PGZFtMvvY_PEhwsuAFUgsGcQEaQcmAYi?%y&5f`&Y{agKO<cdeNUjOwBGKnp}>uU=WNT@i|r{mj++g@C8<N%atbhmecHI^d3qSHy^!0MAot|59ll$k>`<04R`+JO^+_Dsx}3lX`>@gReTXXF_A{y#8Tw*2+ULhQnA~PXHs%6gf?PMIXZmVjwWwvED$5=-^O2VVcm~c>{L0yy)FfwrpNa|ZkS=+?a6GO6k<%4;Ra=Q8KE9oEUJ3$sqC%!L0zj_o>A`ztXSZ`UYq=Geg{V|E_33l*Ot*SXTtZD8%R+M<&0sJC0%iqfQ-f8%2_>*F(ajI#HHOcU&E*t&TH5Rw`2J!Y0^|3niG(`2PWfd|5)lUj*gD=iN)Sj0rfTyd#+!1ll7lo3FJ}E91xnIe7AI$fBFrp2HFkqJo@Z_x%`D&3z+5U;^wxM8Joa(lMMU|Ear!@>=erbL)<!40h46Jt`&JWr<6<Tj72%debu%+ep@hQD)!bfxO0QvvVz{&qC;RpB?nwQ?<uaQAA0xl}h`KB43Rd++-Z8~1#H_-kctLpJl7kXz@TFrgL#KRE>~BE15Gd@b!frRsahi~+i<Z8JTBQ@-!00``B8@ki%b5&iAi!$OG8f=QkN!RvZiaaFRdOWpRsfZ)F{w0ln(|DMPg@_eG;pK+Zon>e>~QpV74&$iE5<)6+&Go>iZ-X=6k;l?B^WK6M4qSu<68=SQ@%T;{+%<Zr^WkqmQOT015O7K`*{#ln~;?)a(f&Ty1&*AQ~#<%-dc3!0im7=@(}_L=0KmUP3P}NDdXf$J-*sTc_*vVkLMQZ20q`&S2~_@hJPcFxZPsK?)uG#`Tf_okC~2?zH_b6cm6E)&b8_Av%Gjs$G;Y6|21@LywOY4&|Sto853MAToA3F19KaX%5p63#V;NohQCTn7$HM5hBXQ-r_GTiNBrS>-fo#}_$pOx7zsZK4L>SG&5xu`FrnKk@h%sRK1|vDw)9eTV}=;fnJnlTWL{-Ut^qntM=tX&>!-}2VicNRlr867KsrH^Q(=Vp4ig4=O!4|49m7CV#Osc;nqa0e%Do^R|M<J^T+egAgz0j)Z&)L^B4fqNWh(;ut_uAf&H3R$GJK8q{rS-U_Tz8A{PrV!`1#=P+r?pf|Mkb;!{?DLg+9Rn_7PV1SaV5z7O_jrz@B{o7rz9)K?snc4X*WIpp`N<p<P?J3$L&E=5~n3HH%-6*FO8Ade^6#Y5V=x597an^)L(B5+iZ?9lqu;Zx!A$*4>pGoe;AR4OeEgW|GXaXs4bX-GBe_QDLdWp2=aChh=otxBmFEZ-SvX=4pwY6~n#ul?{uGD*o-CfBp4O|MmM{{_UUPiHHMxT(kINr=e>S{icNSu*|L%_`2%xFJd+y3qKU@S(?rn8rDxR*3;-8+wX~m#5HZc1MZY!*8sRBMt6Otk)B=wAxnGVGa4EmNBHaL;q&`tP50z!7yUlrq2UFL>&n}Nj0P%eloLOP>)extQ+{&z8Ka&sGz4+*N}!Wv^%1fjJ@k9yJz4MHN8bZVI9Z;0SYK3*3D&;*&2PEXaysR9katC*V<XR>fU%c6z%PIQ>)(F)^{|(Z(|sSy5IDcuLunl1KHgQ2N%9sE{&Dpa3|Iq->BC($k;s7W#b$$KPSMb1&J_)Yhx=lux%hyfV`Bl{;j;VLw`VTdi+k|p(X@VJ-6K3kC8?Lp9;bY030u$5&?He)i~cn2m{Hcg`re=G)es_4)(q_ECaB;DoT*Dkokwl+O9T+>kElJaN%C)5O643A%x>cxaBxlb=5ER-=1amUABjZ7@z?kI^x3z#Vam5*e?e>mxnNdx#95$y`2NzdMhp!5t2!6oTkjhrPY3Pr6z*8H@AeqdD$*KM^&sdhJ#pWf<VUQYJ*K&iHMo)g_{;nIe@HRG$4$A5x<f=70$|!>$v^)%aX#9@zMUf3{a~UXb0MMBaboS!WG>zVS@Fjl#@o$*Xk$7L9KeiB_l4xyW2}SQSZ*ct9^~hbb!<OvKEKE43Z(Oemo|@X-C${KT8CpK@|?kgqaj$4qU0j*qsE&Gg(KKl09f!plS-nWY#ayaPZLaOv#^LYS8PF+&L5j{Ey6WslDqzaONfrgrZO6j82YV*I~b(%oZ8Sam`RlbT)|>yBG|}|aV+8?qf4Em9Nn%F@VJgmIrXIk*!aCJ*x0lqf}{>n+Y%laW9*1zGSTq2zKmCy8e_{_^gxhj<8V$Cdjk^hpz9?b?NlIhTQF=S0>-}0ffy%S6ZaBf(v+271vTBv$Jvn@FHB!gr8D#9)t46fExRtqoc5l+lW2yuze!@xaT<C?5xq;0-fqPxz#pGn>^UbslpE|x!S*V}ojW=eYF@NRr*&wFcYchegL_a*_3|8)<B&}EzGfK^)<T4AYdqziuIIqEvM>lZ{8{Fyb!njjRpL8M`)gULimx00`aHPBIZKva|64*;hO2Ua{_*1<?=qcoK6>-$&V{qv@UI|(-9sZKIhO2=S<ZP){}b~f6m4lFHkaVfoO`&Z2Zw;gz+l%3_N+q6l6?){ZUV48M!C6IHBMAbWg1wFkoV?|3-<93bmp3nw1rQJIiMe)zXVcbTGj01*Nt=9Y^CnzG8jHi7<x{t{ic3^UDzI?j00JFKH!T%QbkLPkAM8M-KOld5&Xq0|G7SFVk_tyI%X=(0V6U)eXoqg7dSZ4%T5bz>G5lHfC&l@aZpExfln)X+~JlVyDkZ+b2q!u1SVz72%!KtYqk>tpwoO|);~vy-~;EyK#VhwFVl00CVUnAY{Ez+K$)b)wVD=ddRiIG06FI@JEYuB!H@F$j{PZhPi2PeEiI{>W_Mi+1vb(!7hiaTJy^JUDg%-MHK5gPV2Lq(P6cX7vhC}+kr$kjla=RsZeb&+8ol&KKntn+T2hvv6ws7Oa<CHRw0P^<&0~iCi^(}W01d9H8nxHFW7C>cMJo>}0OLgWJKY&pzE}IJjTo7lq%1Kz=@s=YV~Z(VuFp|#x6+10_g7Y!ZDvtm7}L~_yD8iFx(XkJ%CkF%fMkLQu<>RZ=pV~8zN1j4Su~JHW^x#YMvgs^xd$EUDik~WVRSQ$N<>X3vF|^LCt`Gz!akhVJ;3}1&uLcF*ms+GT~!P_lxvh6+4a~>w_dW7*kb@I@;-!8ldw*W9K=VN5FSJ;9$GV}Z7tpM>9+J)S%Az?hL;wvDmHeyt+tG54BpwB6?a2lujwYa5s8ceOEctpv0xCs3!{!Ah!7n(ieas%n}S@+f{}k;^2`814P59{r(t~caaq6jO_>@16F^hNSe42S1OEc1hs{`t!?BM!-0kP6t(gk|rzgJ=FHgg3Kybw%Ey<W#)Kg`b-LKD1!~G35OkXKGkIda<PIQ)=@Ueg{M(=p^mmcYYn%*>~iEl?+fQ6781#23i$<=sd8=O@HEMcB3SEJ>_R<h6T)VOpcKag%fea(tTaZ*beSB1CaA?sS9uRUMOY3XQ>`W}`>=I>0aZGB$IBAXB5q>!OZtry}!39A~HA(Y<0y^lToaZb0IpqV9DOo2=UGj!qno#va{M*x|@A`b{F-Z<9$7}nI&Tl)nwO*~7;ryd7fXwoJ<_>Z|PT|B=rDh32&pk<>}!kZeX2w-6+QK0R<8L9DTts4GY#mUa-oaLhlJf%XBEnnUSG!d7VizqbA@oI5RYKFMf%lry{H61TYGog<<PwV27s@qJ{8VyBY-q*l$*_zA#HOs8gJ<S_qRs&x~IlEZP{$1U{1$?jH;FiC@(7dix3i)3)zM4|*k_$Gyo^^2Zj`5+7eXu$D*2#tLCRyxt4e%y(08&#1htHS}s^w0JdxXGcR5>_r0iM=AV3;f6ti_+FWRKgJB;M=>^I~<=zNbh@Pk%Zc%i;<y$BaM(CQ;yTFqvR9_ZNu~d(}@Ma2NK3@o?mHEO;mDv~G4(RlxGHLVpIHb6upCIsU?IFsZH+?S&-84Kj1H&OP0yIw?4-bwwcYS9+GY;hvJ;8S%9oR?4krDLl%W!9{UNGUXZy-q#B9-fx^FI$fXvBulB>RTjhVDZ~=e7S1iR!Q0JtmT7@MQ?&+%xEnok+Jj9hJi$ZrB_;ARl2zMMKrK3SF=hp4)Zfgq|M90Nw<ykF?Nwoc$1bjZm4Mwz=8V8~`FfWe7fsWxPMe>nL>>uj31Hl1Qp(#I^JeoDx-4d_!$+!p+2h_zZxi&b(9%;Jj^Vh~XW~GJQgJ!aMFD0Lye8S_#DtozGZ`w)WI7{Ira(~Y6E1P`v@=gL>FI)Lc~rpe<n_#y25G7(-6}<r!UeC*U;rY?)EOupJyFx$?;S~1uxEYe7OWwY?D*WE`5gLIGH@_M$+nI@s)5u!2(X)ybu(AXof_C;JclHoiQuIuAN%Z(vY$EU`neG++odByns0-v1LOgE8A_P`hKe}UGf^MhvSV(Olb=QhWTk{0x_1yc8WzqY3?j7*^KG`_g&Z71^9%lCRttURn^N4w_P{M|oB<{?AhOW0pJTOoIml&?ZhooKakT=#;w2T3xy4*M0Vc|se_w<-Yr;Il#=yd(2$l#*eMhxW7fpiZ){4b@;JgP_5Mk=+@%-o}z|VyPzZJmUk0Fk3&4v-rB(^Zm4YwW#7?@G1C^+O1UeF~IPKMpSR`>G|$ZP?0G#$}iY8~^y3oN#(AoO4#;z@?ywGpE7An&R;h9A)*;X02-=t|EDO&WlpJiR_~6UL!$6I6#oRy;7_APz&>+%VNK^fW!aAQGV~PHv3rn2fU;I-@89&Q$ht#~g>%4R?%khw*)T_MvOyv33Gym!<1m-RvW7ny100p{>%rN@!eE{>n*64`jqK=<zl7(Vy&BO)4h>^2rg~iO74*s=f2MXZ)(6(A}AopBr93i*bo1y@;?er!3-$_+zlEy>S%X9W4{>U}bF)$H4YNYL_Q5QkO5Q&D-rUEI%{PGNmiBf)WftS)5+(L75x=I|-;ZY5SPB%lc>SVJpCZ#}b+!R*QU7r95Sh>Gay?*{&|ryd=|4bjasQi04_tv8gzoT;2o%%L3FaOHl+sC;a*3NU`ier(`m1%6izJt$Yt?_6<6itt&0LO*JItafJ3BSVgcr*g{306!!<nQsfw@iO%&;*bSRRD=etE<zfw&0}<rA(`gmv7Ah0@-CqjbfLVxw!beyuPJs$=&1fSDo@@#Qe8bSMc^U0a6cZSPa<XZ0Iwm0yz{nt9o|nn)TB-4v=A{WnCrE2bne6*Hm0n_5p`fb1+tWpu@J`2M?=dy*!T)bWgUh|vg`X&|O7u2Q&9H8laN|SLK50)lCRoz13f_qUx@SVL>7vXuqH0<=qFssu1^9K9e$}k-U}UO)OJxJOhBafXcf2jYT{kza7<Sv7$HD_4S4M<N>WaSZ<-AUAft0~!C3HQVF}b*vS*QraNMaW}Es~`Hu(3iNA@~`O39dH$@VOk2q4w<un!@z*aAd8;Sy`>XBG;4m$A#@RMVm%?Ji&EHXg4zg6=E?7V#|Hn&-vWdO$SOct!s>3AarvWZ4E19KL5!rgXPWlS-W_wRm7ARMuB=(Drwplgx8tX#LTKm<aco^Bl((cwCmIJGKZh#Wo|ORDvAy(hix#PC)!v!y5D5Z>Bit5;en{sDKcE)8NY5xsVTG6tek=3)TE^X_;6`?V=nX=facSAn_LyP?B$dhdCDr5qHUrL*;M*h72RQOT~>x8Ks+7b;=GAZPu}G<=UF;xi9Ndg9vJ7t{H=ZJQ`b2%_YY@<O;V|96X?9{^`v~&VT7(1D>=yL>2y~1u}^zWCK$<ZVao9Zs*<@COJ~?wLqiSUbgtT?`GMx-UTo(imJR?gW;RM8&`uWAQ9*(eIp2YOEl?0!wPn>pP^7Vq=5|-iEL^-vYNXc~wt)@s(B-gVvP+UyAe-)0s!Wb;7a=byAiLy#fh~#H|7WC*X^#o%t0NK1Vz5i|+>Mc>V$pBj^jwN!K9AK#H)**|uWCzDELefH$1jy0BcEydc`1?c%-}kHYoNBsh6_&W!Xf5HF1-r7&(d#ygkg7MzN_tKk#;viyrM8ESqWgd)f(fdA}+TBK0&GsftK6e4Zz32kuN+=TmCBj%5M?gLsN6hAPInb(bjOA7*UF@zn&(wX)_@w-yH<?bCDAu^0{Bzkv|MgCrV7LGqUYiL@Pdzy6usLw2PS9)Mo%HS38TiJh+iiYOwGr!*otpGA<U{NoYLAFi}+N;~41L0kz<g7nB&tFqhg{9BLIEmU4fhUqGpo=;wha@zHo`+5+x8BB}-kw_Ap-lI+L%E^fwwbL<ODxoMVV99%`c7hC*UsEH4vvg;dmWpi^lj-4!BygyEXqT^bGrs3r1lBulSFjmkXEJbbdbH^iXoqSr(3Eh?KDH7I!wAm_-gFj@!&o15C%ecMPq|>}%Kc{ZCG!0x;(kQDIGfCi$S-tsO;6NBV+FYuibDn(qLryf6_Me$3B&W~&81ht5u;>F4FvpvNppPLg-8M%)6I6>w{xpb<!0_*d(pri~c~5(g1pSwK&F1qUY;LiVV#?GWdy-xWf88-sRbN82io7+Sp*1??Cl{&2P&%ZtOP|KEVxe<av*|2T_l`R#eIcpxUmZ5I^MK2SEz#us<qP9nI5_!fslWw*F0<6{f$p)iVNy*&Q%ZD1%v05Kp4S)EPu~r~)t(GF;apheyN?*6_zk%?r$3)vwDe7y_gc>-Q(go7-WG{bDZ)Bx!pm}VnTh}&xI+exU{n%~Mkk4Od3cw>KjRt<(NAdJUnp9}Is?<i8C_b(d-$FhWSNRQOsb#X?SY?@PO&~f_8&{KRdgNjYRs;#18Z>2$(C4ewmbtf2T3i<ViT_LUOn<6Tmp3RqbjI0(2?g`(X>@DGL~2luv<0kuKA?Q39kITyI5vvQ#?Kdpcr0JuhwOG%xZJVBGqzZrHDdTQ<mu0#+2uem%V~thduz<CG2~~8U^<u^HDcVWrDX@z36H~#Qfz$nYvv~2O3=b$Ka527w^vbsY2PAvgApQ*eAGsevww2Wskw_#P0b4C%8?jNm)(*nCH}|+s<8him+7hxOb_l&3DdcU1cRgTYFi^ixE!QW4zKYc#@P1rMvh9!N*l4Bs|fUq}J#696qd}jEcz};jR30rvFKpM>Owq4YM+d6M8RD8pewj)0ieduoM@nlyMtrC&sudl4XRo!G#MGSgz!9xBzoj2}q@KGd3+FQ>tyzl4c1^u&o?jOUwNxJVgFlS8yQUE08TBlWayl*oM6#qJfL)7#D2rQGRP0c`?d$Mga}1#Ox5!lI1@}T0;Gvw(0yYzPRSmur9#oIX^2Zcf}>>tdgB@<9a&iU!Bu_m6l!Z%WJx*4#7+nxDAfUTF;z4y)QqbZhyA{5i)InQ>9<fhonW5i9*qQDr#kYp;Ps7lr|}-Op)b)W;Cpm-yb{z{2JBHayY4uiAu=E$Gd1){m6^{f{iB?#I-L$zQgAmxZUgt;w_b3^uX~nvUIY8JX(%zuwwv<nJV@h!<VV8po7tl1)m+o=-AgwNcZF-pBBiJ$T{8HtuxwJ00>$HgaN5_xqTL!W%HwcKv8ksr}qEa>R|lBQjR%BEV`|>rI2B>kmX!9fqWr<x!kl9qqx=OS!m;8#nJE8LVNLGo*sWA*oZm>O9M=(a(oduiXW(K?&HL6K2DNq3l<C@Q{qld_}*EjemAN-rkHm5{=AWv^XG>>KY)(*BbA!Uo?2UZQzb)GDdqRy|DQjeOk|@0d0La>V-j40zVfe+)Ei9qm(6Ib1lv~;xy^0Xe&h9VwjIYPI|#!m&G7X+ow);+zDVdZ{2O&QQe}^uGy4Vu@*VZ2oSC?aRCjF6!Pi-%e#gF4%migNP(5JaJl0av<tcL3+hw=i6AY)knx7t;%@oef+4lI3-YZ6hzRbMZhi~QiNxhx1I=Lqa4ZV|fE_YKnOq2_W(E<kqd`lTIpq#Pn`>Vja@A*oJ^NbuCwccK$&odO_z0Bcy8;WSVF^}N|5i?93)-iRnJIy?`G;;ae^)|X~6(aRS+>u<zXmp`?*)qW?sg@y#f{Jxlp7YnuTy@mldd^^0OwdH?qd-jqnzY{;IX6i3t+!hDQ(})BC9oQ`AV_bz=|2HJX*~J$w)ScPfvSWq=KPH0M)u%dfJ5u;?wSP*Ek0*kzD#Tf!QtC%)GbNt$rf4w6ztPrKF`y`RPBYlv&8==SL^W93MBzA;mOG-#7!D*ed3z7A}nyi{EnJF7*%QhLtj8fI~iGLm)m^F#$13mkn6^Db6*Xb7PahCW!YoaJo0P+Kfrl-9oSO$-J1P<DyFAHhU58q@hAesNmrOu$?-d*;oCXqr680js#i*j0wk=S9=xKBXd26o*{tPeXBLoBdETeb#WUUNf^n%naV!gchcsWo3<#JNn9XbG>Pby>^8<H{xU=M$IUA#v&^rdczgSGbXgg{mp&qjXSKbrrcqm4$<E^8PfCPuCHZQ`sDKRfONaOHgjt^40Bn@S8az-e^%mVJ9KIeFzxp6dedQSs$>3h*z<K^qv$9;zoWhchz|9n>O8VWXg>@DCf&kGJrSnNeapwypU$HmM#D!ws`>1XDe-V*6LaB!fT=zDxl1pDw{t~U7W!%3QbygS;Ia3RfB!iNdD`>?qyv<lYvMY=MDDR}7?V=I?*2aow~{!ZDIZ-ARZk2IiohR1$!mgAU?<jY|I!4gvqm<M<kWf67|8#F0;9Ul4S&=ieL%Mmi`G;~Uj#l9AlRfAI0DqX`Dow!C*mkdS^XHh5YrM-D9a{3ggC3(VW@*9`14_;!1=9tdL`qKo)F?>Um3>g-Z!UN7O(PK0fkS{G7Ys2eS1tKvn+^#OHj~)!t7;+3}d^D~8nL^J<csDy7^}MywHw1TEA04u2i`UR(Ij;BG9;4s-)E7X0z&A)DXw>ASDgn|k;DJn!mz`%M(js;>>|JfA=9`~XrGi}$d`eRbVyb3RAtK?Hb83Sv)n4joVB1IQ5^23}9&Lhfx}paEoM`O;GwFbau5*ovo=2)&8{nO34zQZgG1A!<N&T?w72(28a!`hmWlOyjTBH3OjQV#_rt_MLALEvBIWwkCw=ny8V8EPiSENI*&iB`PUh7}!GFCo?&;tp@kk?s7uOR6G18bQZ@scW7V%4I>yvJFtka8M@zFQv-?L6fTPs&HBc;_C67`AF(XUI^g<2iKAT;MyIl~(UucT1;UZns;+{#?KLu%G|>_A%3uGP|!8X7`^(?7lj^oY|6svqkZYv|Pl_R{J<Lt(#Y7_D$2$vkVtaf1H2mt1JV<emaRG%)d)a5Ay>Vx%C&D*a;Iv3W%CX95+`5#BFY-?hS0`7zUamK32H)24)&FXczSTAAgr6F-CBcmyiosFmYOGMaGI-#a4u7pnb72C*1}O-M&Bb`u_IgZ@>KZBYgPTgzejfF#7%1AAb*@|Ez===Jv=eU%we__Oa%Yl{4aLnXFrD1kO=Be)#e05Nz<hbG?m~GB%-ITeu6aulVM&j>I*KU&If~FHF03G2^*K2p9SP{r7+Wf3JO2c>')))
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
