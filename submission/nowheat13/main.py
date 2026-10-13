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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_kBvLyCj_}mYb-<f(lL)LPLCD{adxP{dPF}RYhuz;|FaChG>_P^_#?#!ypaC39>$m-$Tm7b>Ou)8WgJR;o9&CUPqoB!>f|J%QO^S}JlzkTz6{`0^7*MIrfFF$_s%ctLd`{s|AZ~n_a|KI<|fBW(eUw-_r|NO82*T4MtFF*g&H-Gv4KmYBQUthob{oBvqynJ)}>-E!@|Lrb+y!_KQzg>U)@$hed{EwIY2mk!~>*v2FKY952!GHbX*XuXx4_`m#)6YNr^y%wZzJ0xY^U|7s{_U^V>n~sbLoveNUVlH1@XKoa@a=#6{g?HlzJAcUJdf$@e>(p5etyL_-GA|YD2K1yeH{C)zx@8gkKg_6%ddR?{p-|~FMD6q!<QAG5>D{PPv2hA{G9!3Mr#>g{w=bM;*0R8Zr9&Fzy0v-r*Z+j(F|ZTLphrDbJZQW52M^uWk4MmP`BCZZ`bR0U;h24>yNKL18Xg}jt}_Dg8uyZ{%Ov?6o&HT88qb#woL|y01R%M$?enU>#yZcZ=0Zuw*lid1N#qO$9)*j<EtLy*fw4|lezI|>-TQ>hhg50(ckyS?;Mx^$)j!Kb0uxE{iXNa5r#Y4(aySQ9==sHg~xyME~WK*x5YDyw0^+u`?gmJZ0dHQ??>RAgy?(C=2%m*ds2SC`?c#bcZp?Y#$lJc`0Zz`JJ@Ho?(e^y{^HWz`j~}p<F6&_9iK|(eb@<tg$3{G2QDbt&~*UO*CrP9@!86Pf~WV?f|g&E`e5>L#Sc~P=W&rer#^NT!AlIbF@BE9fx>^X2QG9T9>ZGyoA4?2ZNLBR`k#~!dHwOn>$ji(_8+dle*WRdAO6?!io1Uj{KZU+0YWF|GdHiJ_-A<T*0+22t1owN!$zT{rCdLiJN$S`OaEPQemwWpTU|a==c~b#mAhs;jW(Wh?@?ib{`Z)bth-kpAM-K81n2kEc<(pOyKOyrw2#~2%w6rAyAyU!zUz~3WfiZ>sl9pfOJ{fZ{~t>JwSVc|_ujkQLzFLkZz+To+n9ZNS<KHKF3(wv-evZE;iHexH1>I+U62JX!p_sni=drweDZ3p4nb-)ftz@4w34}!aQ@_Ko^=`NV8h8HgdGfb`@p|``t?86;TdF=?^aL~d`ZiFANGkbR^EplJfsA(p^tphyn)kucmsTA%HMDBQuH|2Q(}>>OLI)?@T;xDOz0g9@WXIf*#`o&e>DnWpU48(afXfvIUau}L?YpubZICe^hH?iNct)DaQNOx@FE)wKap9;epm8dd)D_Ln8-db-Vb%#0IrP8%WK!%4*0PahexLFk&O1jMCTC}jo!L~7Vt-ApX?m*JDWyp?X$Pfis5OMiE!~LV7bJ{Ph_d<u3O{a7t0A=i0AqxXl|0pBwR*rpz$N9eKtf5s~n+D|0<r_1|Cu8c|_+OOB6TN%s=qQOE3w(=?-q7AB_9gRd^803wwO7OBo73U*4N-aX})Id|Sn{54<+vi)!3BkMNUr>xMr8aXRbUCH<`rcC)IytNZDdP>c{Fvuo@pZ|c0OB8~Q3n8f#4>p&;)c_ogK@<9LyQsGynAD8=@16PE5RZn(kttaB8O==tz^o-MtnVO0r!N+|^X-=*7ngCz`u@W$mm*?8gVJA_Rm70>`LfA9tSP0-}ok(U9;1Yb1fb%HHSN3`8!1E}4Vip9Zv>$h3^~v{q_v`B~S<eK707E^T#evXsdGgw?50A|`4=moE!ue~Xe6sV&;Byf5rr?}crvJdzvV9z!k8|-n2{JsDy1W0eU83_&s>gVeo;I?`2pc)=@!jtsyAoCKel9GI>8y`Qb8~Xe{_gSq?enjnZhyJ{`s;rNwv8f#==;u144@N10xrQ5vvB8b_L?tmM|^)ue84z=@oK5nhu_Z~{QVwhd=zy?>Q_nmR<Q9;0a<*O?%oLM+!h9HS0a|4h3a?QYM3Xp+Yp?r;Mh6yIY;2DN@@qCi`BT&nZzRW6xj3ba+#$yee60+nuOHpVtn^UQXpNY4%q#JU6AMndIIQH$eqLexp2LqJcn$5J(|i%dtj~G09M5Qw`lqgpZ4|jM=%g@(`^v-`UiLbyMig~C6p0A8I&Ii-AjPK+$i5gWx|iYrthtt@nh+osYHIz{R5m_LJc|I{O9%0uHSzzQRYoH1EhsWEH3k;6-UyN+u305UKXfv27!4i5b+Py%x^ZA;pRUO1P8M6iBV!zQe(!qEVERpbjZE<)V}>c*=42WuY0>|gk=NQmO=@sC{i!Wm1%rq2MQjOlE^Q3HK?c+nBcyG{qyTjpFY1zKo5ZXY5F59V~wkC;5_MJj_yyi{l%3j1{p7yB=Q0uU2Ci?2<1+zOr_B)uk4lW)&RL~JQ`g^(E*6W=~bdRK*vkkKdPO|{R|A#*+Iq&BFB8^*5+bIR^~}VU!6@<0+ow%0y^`obcrhm+&zf!Qgf19b<5r2+;Ed=qBOtB=JFm>mFUqy_TyYQh@XD=@jrf9uFGXF;6uG$hLhKFX!k#`fxVkv(`K{_is4R<UeEps2yP{!G_-fWzC4`2zJ6t+T>hv5<&E2IBTD8R#^eY6iA6bAvTi9z-h$@4tLw_$fqd**yy~GZ4{%QGxj)i32*jd)5$8Vb=7msxZ2)S0=x|NV>s;9Xc80a6lwyV&x!zfD8y`w3y#0WdKQdXCyLsA&(0~5ys~502*_u48vWV{<fv8JW481?}Oa%wlMjT41tDY+Wh(SQ&-NxZB2pW$EyhLFcec93YsP0(oX|V8TduQL}VMfu90xL`p-usP!3hvyxd@Z-jR+0xF<-J^B9?6Ol7C@m96%R#zzgEAfsrP)*u-wAf2)L*_s6?VC&bNZ$-;{LJru6moJ(BbX)iB;?$7g`MniLlKLY-Er2#$bk2TCcktvRJ_!C*-6PwAH(IqppoP5|PXB$_02dS5q3tT;+XkbvA7=x~)!9XM2+2zDklT2p+f$+jLyWHf&%7Uh_XOOw`uIE44?*#!Ube&~EKy^<HhLHYfd0X%M(HZ_X7w}!s@kyu_I`1dDsl;R(<tLw{4#Du-%<EV!}+j;8ZJg-gR0%+gJ47=gc<Bx43B1M&qeE$gKx2ey^*h@c3&FviVBjxqCM~RmQFeEd~a_4+bmM#V-qab|okOnN;<~Fsu?wW;7Y%C1i2U806*m#ze;EC`$jv1gQfEBe!LLAPgl8^cF2%TwZX8|q}Pia>fD*^lPL!qf`*C!;!I-M}?pj<K;i=_TGD}Dp?yJ+!BOtoh9>>=6H8GL4}=w1dzf*bN*M#AGC^>uk*_uN_%1lm38SXlN9-eOE0z5nO;?RbXpu`iQb>@ZQL_H03o$ObPNuK;b7B+E{(@E@6df+$Fn=K__GM6)a;$*Z(uoY8dOUS1#&E(IA?sAmp6$i#|B#AfspV)A6w35NP4>PIk(6FQ19WB4U1!9u%bbeKrmV-2sGBs<fdJ7FL#<4c#xVNF{0tcI~%A_e?Y8~xi|iKD$h#sgM#M?qkuJIw>VBZF05O5%{(ASsGYEv}i2?3B@f5EwhmcUP>qB$EO127Pv!ekfrjwodEQt&$vX5Cb2n=sg!g<wp1Z5wk!+VcK0Pj+V74mX8Ld7ZD9vY_!9~i2Qih-taYRYIDj7l0$8;6t>JU^1_pZ6_7z9TdTQznK}4Z^Y}-Vc}8zTTJuYNAH?OdSQelxJ^o4Lb-U!_PFO|!C@_y8L-o#EnMRe3m{DLctI!pc+*1h;G?hl_&LLhbVVd|L!CE|(f<Uw{W6HOm>lBl}47rM_aDnanR=xKNm<yE)s{QmXH(99zkse>pags5e63*ZyDea3tp_H~FaU2T721hE>UdH%MK~vN3UtfQ_N~$7?$Xoamkk`{|SpBB11%~(cnhm&#6ln611xwH%)iDvQ%Vo^HFX9O$F<j5hDq8ph6BhE4@@PTiC|7<R<w(5W#ZLoJVu^SHU7}jpN$p$-S-5mBg($m5289xq#cCb~+j6;oUW1n$Ev}BTkW0|CY|oc1OBUG0G5RW9Jx4YNuj|<3lbtd|Ghn(v=nv?J05yHFT7T<F>DTKIi4M{G!GSZ&XQ(|9JQ8Jd?4}Ic1V!Lz)RfE4R36IpsWaI@dP_8}+PgCoPD(B<u=KBOHsM^A%nc&Kh8Yp(_IoeW{r0ugf(l~?OYd4&QT4rqz?aLt6hr6M>NCj!Q85gld5?0btf9^9YCu}?D?kzWVa+sFc%bgH<88p*BL(-jxPDaG8~4Hy@=FhXCAi}s7vp`%g$YuAFMw>K8PH(hZKz9i1%}=HZJv+Ykfp|9<u53pq)lDlSMCXQ2_ROn`9`N&*@`e5@XuSLkiW>)QIg_hfTeFrKBX;-YFUdPIP3m&^*d`#O=a-Re*>vqKZ$mz4Sh~`YvqSrRcy#9F|S5|95@yB?J4Mr6{R5`n5_kkXR|<?ueP<~SBh4ZEXqSE=^%Gy{)KffNDAkLNr?9)ZQ~SaofhZ*h6OKttkl=}te&tc&L_{*W%DTk+s2}g2Q<8LiwZ1$QPpi$y4DBG%y!9%^4mKHz`RjWIbxE!`Vg|UceE96-p6L#jQDsD$7p`eF%tDPdHJ=YEXj%q5^7+ok+BAKI$TS6O<@{7SD#Z~r~%?egd+gu0r@72U&^OdZvfOkDn_8q-UHR5P|3P#&orMDgxrbZ6{h=v5GAl2A;pY=0=#dZz4=1^e0gUliF=Q_K@ISTB+#&^B0n&!AThf6liuiFQzn=xD{rVuV@b)n`Z60<x`1;S60<|RCeFwwrgio#&R%`nv7V$p*ub0%>-psk4H-r(R`4QL>*rcu#5q~N_2f&WQ^V`afX3iCS%q8JI1FF@Zui!jwzeEzatpad4WML;Sh`i`TbJ3egsQCjBhJH(8F39}4z!y}=F+Glsj2cC!ZAI2H{|(O<M<~Kupr%qabRN368c42)R{_&F~xr>WgQ%nidskOe_~z>czNnp#&R(t5;w@I>A%UI8z;MTul&fw8(P^2)y`s?ySS2sDn0-m1!I5qKk58lXyPE8p>=bX@pF4lqZ`?%Lbn&ZnxrqfvPhvZvHJn{0#bc*BEWtWz@gU`P2&kk?wXfUy1RrokvrPFHbf8^cZ&nA)z_ZfewN=em0lH!Re}M7pq{zYsM0Cl^cc__?d1YSR@JW_EQ)N59z!%yME4=~2A~d2T`uYmK(p_cIQ{-$Wj(LyZWPSYs-#eR#D$z1D3+9<iCeY=3rLtSNi6j~BKZuZ^$u_X>`3fP0M%AOT?ExGhPOngfn~_*qAEa(iRymzqv<mmDtdH)BpcD9jM*TS9V~L}5~V%y`8uPnKB_IMufl*AP;zWu-akAT--3C39pp^&OIRfo%Ds5w?9+sSr~r~mc+iy=qW7FbOBvch4TzUQuXL$d)d-?U2G=PecpcIO$0i;J@*3CjBBGaoQVZ5n)|yP_pT@8)N~gR9QJ6~Kdd)r~hvogk%E`Q2rmc-_@5B&m!WE<3c`DY|N|o^wb_z?)P>w{V42-k20Gm=yLY@%PaauY7>9Rbr)eQuzG<2jeDWX~M(?l~WUPJoy7&USM)mWFURBbNHLYyi+cyUox-UoU0m|iBYWT5r9q)atDD=d2^r-O>S=|ofWD20@(jiuL83gTf|Jk&R&3W?;JHC4z<u!Yy;PRCd&WA(98VV>KO)O>>OfUtQ&`$yu0<bML7pU_Avb4C>12bxOL`!&?Ht54FFGGGRAW@GUD<K;T+Q2=+hTc_LxsVVsTyiz^Ug1fCO-h;NurcIT0kXCSr69x&UE_{EZP7yaoZnG)<jNeVvt8eImvyd2rr-Uj;($dCvhk<dL_$8J~jND<y+p+3NAP`hazTRVuv9e{`L*G&=3SM*dcE=JGU}P43wU!F2BmyuEOl`!*rmDx=6dG#v>4p1YJfX@IGS5IEawQ5Biit*`==qZrRZ(b%PqxoP{^X=z%W|4rXNN)oxn?J56GIP&@D>2j8(yHA_$?rxXsiTHc2V%B`ICEJE$z&RZFnn$dvtgv>QFC6Sy8)&lmrGZU#D_1EF}^eVNzw&-FIe_=vR~dFh#PmOyJ5iR;eTDvkV9&H;bJ?5;tyy(cCR5mO3L(^xErsFB-X>0037%EW+#g>fW%p5wQ-|kT?1ea5aB?H~~BVM~U#d&xF_ASY~hfzauHz6e9!10F`}WHP=`}0Ef|im0YB+rg$uQH;SBE>Xu0pRVrq2rY+OyR*L%LmSqLAYl@O`CZAB#8t&@WzH5ww(9t9f-)!t{rCBHvXzoAWP4YPn-hc|e(PN34u2Cg=U3@XTL31iBkPZRkVh5rV96g37Ce%S$DXb^B^BkuXF<*R%wWFJtY1@*hp0-DfI#b{)bT+@=8Zb25<63~0vFGYj^!S)!u?gH&Y|HK20Ekio^a)7?DZV%{V^VO4n)TUjV+hi2?qnKMecTFSKU!+V6XszFkpij`s4u**<uJUiya-$ZVxMMgA6orP*sab!3c3Q%cRzd&PMM@N74?Ehp{G&;9U_nEFz7@AVz-C;<>I;@6sfWx_unt$f1CuMT(Z4LH;_wvHqK$z;0;($8eCOX2>^O&M^uI|SwvtvU6FiNvm5fWq5dSc=8)+J;8u<T^CzMVT)OWBfm`|0;ve0@3(8H0Cv@>u5ycLcl!VKkLKZE<`9Go*1%OCpN~Fqi4WkLl04peZTq>CJ7UVQ!Vt@&H5=bh5rzX*tiik#LcoxvZvulNlpG?dQrePu<{q8oHUI}9XA28@LqF0y8{ZJ!{jMz<X$<%`5w&Pb)7?MJ8n0i4)#7;%sZX#3zi^rp_WdTHQYbvUHG_pJ)*o}bE5nv{9#tMuuN>l~aO!hutmiGiW?-q(HU^iFFnJY3Im2NOkqGD^7?<8PmF>tPSqYkbTilEyfqI(;Fo&Vhj(enOxhd*?|nz%~bD-GG(3j3R*tju__jZ_N0Q5if66FQxIw_{H#voU=y`U%nuY;%WfjhvwQ;2855M}4T;jsRQc)1`|OX8ZjClfK45+Z4a+cA{Wuv=oL>&}hJ*I#X!i6=M`=*PX$Ny2!1`)E`2g16|B2$7I7Z*-ftYIi3;{f8<gIo!c@b6BlZ{#^e(Rb=O68K7fMq1X{|CVnD}!#Qz|AfDGxd^&dz6h*bMANc5u@!w)~zwnGs#Y(wXXrk84XYE1Ieo<>28VQ_+cCewA~m+SgSthh6P#J!r|V5Eu8-3c7Q^7CokXhrl_zNnMS?nwcb;E}9JsOy=*5N_jIhcLMEe)e)caogc^kO&qTM$xPYR(k(^rZCqh1u&W%w9t|bd)Yt~N5D5_rcjsbiio<u@0^lD(DwqkCs{?n(9y}EI`Bfw9KBT3BBhS;b;&M4iq$hcLEf>wvL$h)?7GL(5le&Ay6$_Wlg2WmZJyO!N=o6np3=u;khCzJSJ1;dh@8HoTOjl&d{lBJba8K_!?lN0ffGttiz?*M)%Sa0r~)l&w%L>nr8UU)aCLhs4Uo!~P%%dxP;)UG+U3Ez@lh*voiCw+Pz1ZMd~g@T<`UU1kSHjL7d|kCE3)zpgq|ne<i)%6V$jU$(`eV+wx%Q96hj^4NXC)%@8SFx`yWGM(Do;f!~-B{Q&gC-Sy&;!ha)QXSOIXs3RQsPuNIc*T_s5tN9mNB;M9=11)5h5HT9X`NSB}x9dFFU9#Rj6kYh3UVSY-zLbNys_^=FC27#cWXgVhACLo<uS11EZ9TbjyRKlGGT%t&zQs2ReK0HzC;%P~_u?qGGm0;7uE0*5no?o)zAZNBDc9u4yk&f2ZujJ)a&xEk3p0%?JLQ6>GArg9JNp!Vn2IUMekS!4}+@7z!$59j3pf0@SBF-8Qex24hq$Go5Pp*6`lty4V43-vrpU0dMzPrXSLY>Ttt0bMflj>w8*?C|&ySv}*Itel9#4<bEi`yc)>TC-&PyvFi7TQ#vX7)M-oxnhg1dD=DX{;BgSL+e~5`yc|0UuSsIj%ScIPx_aY|DI;E+tbPSG!=Y7Pz{Q<QRj+Dk+vhb4o~q@(PqK-@61|aJ`kFaO`+5jUda&?(v*@u1|S_MegS-?DpXa&pEN%POpEo*U8z^Q2vuZVmzgf8i$u<q!HCee{4xr)LcZMk3bNE=R^otc4#L`1Z;A(VFsEM1Y9IFE+{8i6}a2dDibs@O-Q82h&D!1y-n3^S!Y<5W1yYMiK2RZ$bf81-~x;3Nfz{+F56<Y>cIm7!>oKSid|Qta|sw$!A_Effdq{vfS6*!grOgJt8zJNwNNNNY4MjOd|HA}gW5Tmy-So$dVWQf<D*m^?wNyH@Q3(F(TVlw7gERY@cae^iy2ZK4|^C<2oH#eN}nkp2vri;&6sKbDtDwx=|WzG7Fp!nRccNrplpIYB*^3*c%N;VdN?uHK-wdae|I+_$BNjWTN6*VIkg+sO^woN9~d(*$u^m<V%c~`jX}U#Ev1JoH0DPk*|yMDL$Iu#CB}|DleiQr%#a|(8AT2s9RgDAJX*HB*;Esl6SX@b@yyak{Gbw;aPC^7yby8SqAmjI#wve~;0o<g3B%Npm(j4cqg+Kr?a+BfC-%irfbg~^RH<?$<X@tNbRtqWX3zIUy<G)<i&WK46_#i+nYiyO+!GEu;zz?wZ%Ate^t{NyaU5Dlu`EckaLy`=>H|UVt@Jg%20gKGUj(yry|kJbn>gq@B3xAto+pUpmb*@V>?uBcK<o*X<0t|Dc8<j*<<_%NK8%GKiy+U5v+zW~+9n~}jZ4DF+^A}NK}J^fs`4-lt?NEQvzMtnCb18g*_4%ej0aN}5HKnmPs{>jkw~ABpmD0pCSUm@^>_}MoL;7!E(j^A1Q$GpOemot6hcyNiE{byazMs?#Gx>wcxqynG4|DGp3;Oi>>g*1n=UyB5Q#%q|DcbPouE~nM$`#742lG{Q3x$GBVKAHJy0D4(nrh}BD>;BL=rH88CXWplq%LsHAv<MU)xJT)`RD>gk&89ynV^wXH-E-R7iyvf*)tQG7^=qHgXXQe-bFTj_t_3ko$<%Fk~74HT~bOM2L5v;ldsQ7b7dX5{u6yf*JzUl4dRud7C<O_sK;eOi+pMYo-LW?My%zcA_Cg$H4_DDq*Rp(!GqmKclu%DSDvA-%4)#_-N*!gN%p(+zHlRBX;G<Ia9xl22jY6tIzt7^M*30h6$B?>tm6_{0!8ynK^Y{tgaE@&A-L@#NNvHbr;-VOrZW$Kqj0%!So_nqStMgUejg@V1Ld<MXux9v(AaeEun=pRV1q?_88GQ5*QV?0UmG>?s|#QZRM8Md2u8~$=hUKa*TEJw*+`0BpsecCj{*%jbF-bkA#giuU*JFce)iM9}tc}RGnyhF6zXj8R$dAgrATJs%s~$GU6B_X;e}9A%CCNAWn;C=}}qC7&piEnaF%S-ewvfUR`Hc>q<nLdj;ogM|N2^>9ot0>>fgfqL=#S^q1ZZtbNkCf%s08O=1e&Hx{e}C22=Bo5g!68=(@0whoO+YR+}yNzx?RK!;K>hnWr^UPYAcKP0hNy0Gv<6iV5k<a0D2w;*uIHMWu4Nvp*=L0u5TMKTWw_3H@1n0$gDp@sUE@-ew;SYnM&%9~^P%w*sK{#-1lrq>$r;{ek)O^C=WU*;JJ-N_p1U%axahIBh8iPvy3kK(Sq|9TL1aZSm;SH%JI{Y*~9&y?1Y4QYj2bSQjGuresK7S7~fnFykSLa%xURX%0vwCEy5JfY8gN}=hfSJE(MJx(5j)FG`A#G#a6F{us0dI*Syu;ZbZiqGOG09tJ`ybq>g;tmq!>^-(cg}6T>^=qm{Qa6AahYErx;mZ~FXp8m#c~5Igy%<jL;5bd@D)hEKm1SRNg(uLZ;1kMd4>w~A<Gss?ZOzK=K}D%_$*oTga=_#+V%-2Lxh0{H8!D{!dwgoWi1HLYQlTU(?rR*{7cnQUmw{1}h#A*8;prN+lzikOH5ocY?w2Rv8$wNZ+;J$<uT_;_dndT(M*hZqnFW-iy2BES@)=8;=3{PJL*6k%3FO*V<RLmBcH~b}C09(3pLdgq+yX%fGu=8PxWE{j<^D^6U#k(ItV%iO!X~AhZ|cIz!iZsua#EG$WpG({;PwO<!TjBTMs~|7v9!rH+0pYEZ9y<!z2Tjca<-2FZw-YUKzo9=-%4=F;?zf1T^^^jQjGRT574C(vN^-8dgO2U&S`Y7#8w`a`b4b0h0$lC?Vy^s)!iS#8GbB^<+G67K%jLaRXlY$sA>K~5hii1m?zeICx&J91@(<{`ZGG(B<XAeN3m_K%(IlGO<2R%bVA%Bxk0+ai;@{-dlBr*FWboXL!q@`3>^`?B>rk;Xp~ezpY-&&$3ck;QwUlUh28!YnlbYA{hI&C==jr&E2B>+4IM+3)u6CuyDYZ<#b-*ifEuMHW!f@qLyB!_F?}r}6Olx6(!iNEiF)hik8d<YC^v!3Oy?kHRzSw@h?(!Q(>4_xl9i%pD?Fz%(i;U@4KK3-(ywOKba9>*P@D0u_$@&awdbDd%+04t1X{&z*?OG6yx7YdMSpBQc&kEXF5s96NKjRAD(g1j4OAC!$#pW~PU<cRfK4MHs>l6t!{%}|#bI2{f$2NdG)2kyNS69@T-oyfl{pyuL)`A9Y0d;J5%lBfuOiQy{Gj4OZqrp3valkxn_7HTpSKYzPG=EqM5XSjv3QarKsZ(J;~siHl&I>rG0)v4_FApFof!`>fZchddpb;ShFS^ISolZo3rfRdcV>6$m3M5{UkLdOybEAtyfCtk_vJBqfwRNow<8a6R+UTwif<ehDGkwRC!(XdI5ivC=9J31-n03O_37JM;?X%^khbvDY^U}SMrk}JCS{egz?hQ8FHC?u#F(mfJpVNvA&T=~(bYY7i0O;PGaLAI@vFCXNu|2{i;Ts9V1(sB$jJwLTK>~>DK$^{=?Rj+Xn%(1AT}}erS*fbpidBlZ2TkCsuS^H8iD5uq`fHuL;D#k8ad%swsDChWG^r}AcsG_saK2@wB;cR015FduWj`i)f#*~6%F5Wvd94D3A3Gw_nK&x3n11QgFYQ+>IV&T;I=`hjW_bHk5@{9TIL}jFGArcpwrYym6o2+W*)6+n>Oci!XbIpIU1{<k$^S>!h~z^HXl?uW|J@8ISV=)U8O8oFKV^&$=S+!x11JHv9b$Io@Y}Mzo-MJsZMg3SaTiK^?t&_TBy)!xPT`!c)2PhUYe&YcoM8LLFxXKaEV3WgZs@NJ$*z^5095x2e^9FQV$>q6=?#(reQHBQXtv=o;5kLsxait*o}yhvZD&-AdP*!F&F1F$oD3V=3*)fjrG`n45!wd$5O+pK~}{ZO4Mt}C~B6Py)`U%u+}}u<0ep|!>I?bvx$7=a0Z<YpzOX@)z>zcuLh0;zy8du#z#RY#bFyG3QFj6PpDex08KuD7vlmwk>r{rtkN@rO!SP5C(srVJ7lDan*wLtu1afrxGc3rNR$X-norwAT>uif$;CVbLswT$U;zRFZOK-p%D`ADDft7`VXV00Q*CW|DB`DTNthE8-3RLrFP5b=T;RP_-FC*(jS&KJU<gU13XP6%$hz&?Vk$m>*mtHzB%>xJEf9wv_)UgGj=jH>bTy$JDM%{xSW)vt0<i#>jPw#`FMY_&QB(X(-?xeyf7242x$S4IhFNwqGS;-!3OT?)!#j9tL=EN`e`}}e{&z?`U#`7kAxKo=M1>nOvAl+JGDYhk7Rt5W<*_iuuxOJ+PkhUdL)o<QXV$tiQIsB)R5CA3!)!NUmxOpXU9p7V8pTLzA=}7{;jt2L9&lw%3C?vEze(2$QBHP%hwAJhul&*@_UOM$O{A%KPXqMLg`x>^<tepN?C-(V^Ze4F{7?VR`cCUzc|af!1J5wt*MI_7Uo}?MGW9*J4d6x(6PcfcrH}?DycH9qsMNDz`0LL(BkAr!jH}8!)twW|6=E*d+V+t?cPR!D$+J>+!@?2vUz{-01pD>Pc964oRoURQ_0Fx1#{$@pwZz#}msI4V?1;{+<#tA6`TZkxX??Xl0un>z9P9*hH|U$LbaZ5F(tr$GR~ZA3n#RfizvU6;V;rsS3<Ca+y>hW?mF=I+wfmn!bxYOd*#nk3p8=7>VJ(=0XOuU>24Y$(q1!V8ZX%??&eYCX)`;A^UF`WBKP|q?|5W$Jal%R>k-<gvNQ<UA@`_l?MWa3mp|kb&M}t*1ol@U;UnNj}Mu56d&maJ%0AWUa-{PzlX?A^5xka%6fx8;-BjXc=Jy~cCTSg`J#jrPZ1vQ((pt>z4QLK<@!lho8$xLEd7L+H{#D;aCKBIHuw`Gnm3b$v=1(fX_|B=nTjBdwN-<?0B?G8ykyD|HiXw@92savm4PSb#+WcQ&(wXLU?qLeDKQ-#I6j5KGLFlw`<T!FX;qfdQdat;PesN()f)CcbS|K;}|e*Erl-@dMIkJfYA^8UitjjWTFmlbdVRSqD?OIu1qJUjLd124^s1tJP`4)DTGioc<lbO1<D#ed6k57dHP`eG%#B%*!d@D9bqW~$XDspJ4Fo3`5~ABqQn5-pabgkr({J>X<>m3bgv(#Dh9HyzG*q~8;9RcuNwQ?7Rt0u1nq<YZu3iZg5%d{QBaV_nd{TjnvB_oPJou*Y^NT9cQe=JP}TD{CW8o1qDSbfi-j%R%Y$U<?JJ%UaWVVJl($-;^dT`KfT5V=PiyT|=T?a{UOye+f!tf#b~<n)eQefjnx%{!HV_OD|aw=;B+|dF0D~pKWjeX*eJhZ?i)oHFzayA9Z$$yv%lfvcMX7Lp!^b@7ky9SAr7;W+^`QyJqD9E#TaY-8|jiRC`Z2)&6k!LuXaeC-QCT%i<9rzBX=73R-PLdBB{e9^d|O|7G}5byfMtiIV9n&4t*KcH@UbOgE_#@tW{56}^+YTWn+Hu3W_V!|IUI?T{&WL}iU6G4ujVOY9VLD^&O6=9LZPh;BTQ#MlP`5&3vOXAy&t&Y0#!fR{BKS^%+NNBu?u7MalzC$}gwKvYAFGT1!roij9=rGgv9TpIV6>J2U4S;?GUxX@3Wrm)GOS&)|meuwN=a+eJJX`#846L@8P;G-IPI3*XqdIDJT9BhXT%sjGvE@BAGlXUwDb5ptXQ(C68Q*$>e(4_7bC`I*7lFF45rH;lr0G;NBLk|S<`t;2E#Hn!%Zl@k$0S3U<fAJSG*~2e*o@wqOq2^rJQVsIB%wA_vytvEUIPC{e01@Q3?=7A$EJ>b<qiJRoX`g}B46`fM%U%4lu-@e|{ySK3rW+qOsMhf6|F5ilK-jkLMEEq9DWN-@6r}L(-yl5ONtogJoASI30HK9d*<>N1x84@!L1Ki#Td$cqUjKi*wLa!W-~Sj@?MLdSdyOIUfi5sk0J!2`7=o&-{GV_m)$NDh1Iw<F{ej`O&JQ{{#rkzdeY9|R|M(wYKK=js=l}k{|CfLHGMRt-ruq6EP2X2ToD=)<466C%=cXUB?X`x8N(WXn7{i!obwfLko9)%Ys<%N*a$j<9&isoZKjZD2=jzVmsHyv@p)7HS!7}~j5ZA~!w3f|f=<{`a!v$X4kCZm%nQNV{g0Tt(+IJ0#A3y#4-5qlO^z#oteR{i5|9ZXt@{Sw5O{NJJoAsJ?HAw;$f%U6f%;|j}q1*WyZN0@b%%}M%L|V@ING4t<)5%J4(Zem4O|u%G-3Zab_j>OoPQ-fWkbW`P&%eh-JYXQld%yfNWQ7=EvE#URfxd6QpUqH;h2Dlc!h_H3l`W9e&Y5;Nj%;!YNJj}W6tb)c!inm|;FxEX=j@CKgSL7lmwQ`9uM$nL+<&kJVJoBq*%c-_U0CdRiB39FX^b`<bh=L4YdO$Hy$SYD0jUvwj0oHfZl?vi?PFUfZx5&#OuJ96U)*ng7i@k9i?<J($vdi)8ncBRc>j!;DxOiSL+xvH)hG=ZxKr*P4^iX?_*PvI)7d?~|DaN?I_h`uy&u!TtiNqf*x%_1!>QZb`Dv}1&NF!42DC(4eAlEOC`L5<K}?ri_oxcxp6XBV9^k1_WodcE3n)S^95C?Rtt#HbKHX}!P-&{SFYf9jcgR;gxqs(9u>AJ*_PBqhzOG4g<=~uucA`b+pH&=S3!SGyrn=~T3_z~<en!5oFhx$LF_x-FGpEdA2<V66r0QaJ+hR^SL5=o815m)0gz%Ry3`?e251F}n1x<d8d+UYr9I0?l<)Y7m!Vv-u&|2qw(FxL?&4*2(r3WS4?zwpuLK20m57vt!YP6k}xy^S}Md63k$<~M!yKdgx$&K#IL&<kl6RwZ9wU?`Ty{KG?kC}u$bK2)94gqBWq7I1es?VdmMrA<bp$Lk%9`D_x)|nGjA_OuD>>Vu6oL`=2#i{dBA4QR=k~HM|_b!+E?`0E>zqolu6r0Pt9_tg<6FRR(xU~FT(5k4iA>+~ss{W{lZziSiRShkXE?s(AA~K*uTODogM8XZ)9>!%Lq>3>L+03s8O>eav;=L(-xrAdXwqufC)H91427g^XKd>t@hD&r2YuaQs=>f)xR3_fWFsox=`eF}X`<N^&Tl=v3)^$A5%?vv~g9+=o!CO^ZGw`yum*{$@F-a8J(Eo@+B{dJ<UZU3_7QZLDo;HCf>$5m_l#oVlFRje3XI5me9%tuDRS#p??M2UPd)NVsiu4{GQjs|{lRj8dR>=k|1b{YjUFtfbK`)Krg-8~-LHTYu9)T7)2C%Ch7Xb|!SpHCSw8{;4l3U$StrJ8h3Zgx)CnmTE*0Ii!55<ah#Fhe1S-57Xi+uP+WlB<x6op=GbCH#Ja4nRmlo@U)jNaR((Ho5r&1h5JZ!&_&pF33;-)%E!Wsw@1j;%3BsEYnJsIEeRP2$o?iP?1!y{soo!cCnj5Ey};Irajjwi)DQCD4JQ<Uq*H`&bo@cG*TdQu)s=Lt1{8ECY&>?svhI%dftd+r?cxhIF}RghH(2ofG6|#$Y3?WPm)Z&I&kh5!nhn&!8EhKNwpgYX{LXo^PKc(&d#dU0oZ({q5K7Y@50~AW!wME7TysvU}dPdH)iCM;v%Ax6b&>%A$5E2f!7^ipbNxM%y}szOn(2D37XVv)nTihBkV{7id5d?uk3Pu|kE9Hne6P|J+ebc`}J+Ng^`24r4xROsU>EJgpaHgbH7~UFzs1Oq+nX;-FhWs+-c+A$J!&*aIt!`pu9ePmtwnyGCw`3D!)jv<dnDZ70*JYM9()ecVIQbthY#MZzV?b)pv4S5lKn4u-{}_N~t!f*~&+La#oWa10LtuIDHMDVov>-_tO~oM_Fl#cthH%U4FLN<(>(pw0$6t2taGdI%;msLQI-tcPu+a(Z2~znUwtzhpAZAJ**iZ77Y(R8IXMsNcE7<+g9-?h=w_o{$?I^iZ3ky}eG3O2=WKEuF*)Uq{v_x?QN`YAX06IP?V{VIApEfw9U|y$Dff`~@)9u~tG54KCIqqnUp%qKpg9fl^n1sYCfO8XQZ>h@wLM&eeFAff%Df^WiaxF2-NMgpd1>0uZ)e<U}ACAQMvyLo>U4w7G|!+xrZLi#!ALja-D#W;fwzA@!-u<gv*-O6DETOIuXQV+Ix&<4sA~;sqgBdWAZanW?eKHo~-va(&d0($?G?rU#xZ_)GK$;3WawNQ9$F*5N+gJn7D7ew&%FQmDrogwX{kzfPQ8ox*2pXuY)UORy?c7gKzM?{gX|n-KZap_O9*07>z&b}FuK!ylO@RO=U<6hS-U%fluK#oyUuMdX`p2T)d$+740F3XDw2lWQ6j(E%cylXdvB7<8lKOL7vAU$+yH8>JD-!a91Hph){I5q2EO1twW1qs&JPx>S;GpWx!8mhPMN*yz*%s#su8s`Wr41tyg_RrsNW$N{u%w@`>vSlo-rA~^Oede%I4`63MZPh~GenbVTI^{uyY*|wlUitXUcpcHFYMQSjE93t1S5KtiPsv)?d@E)Fldl^wI!Xq5Ve9gt6%4-8xkJhxBypCTK8cl0b<-S;lWN^iY%y5sum>d4A@<Md}Cd=W_@n5rLrEQ`8z^YSnh3*NDN9|9~*}Sx+W_-G)OHD%;T3uj05@)}aipkWj7Qz%@GWJk~R%sd1G~ZvPA9SBUE2~cO#;o?t@z(Xaa9uoyE}TQ{i3(~J!mZ5qcZuiP%b;yS)r(i`u!@M3$<Y{b8q~UW@=o#8Cd~mQ?!0J^#wgpv&Q!%y%g<MmS};wO@+|@5fFKS$HSPAKQjwKuRxK+?z9rgFgNmV$b|ml664{qMA?y&acrM{|B<*aDbf`R~BsfmMLT20%^Gd0<RH%axTS^`ijq{@QU^^ik+7|L6w22olPzw)9SSqH9AQL0&0waUT86U%-#Y2=g=jjbN<L*^61J4BjInrI{gPwjllN#jv%Hlu(Ta<-q3HeUmh*1S3Bb10>Wf~1DFI};*n?n7RaO@J2_Eg!8``D?7<5%1zA>%lH6klqNNXb#pFcBQfP<smL7R&QJmPU-`#1unnW$6Z?Q{>wKn}7lg7v+eYbP3*upOGh!#)gv@@-GoP*!m-nJ1$_0qPCWH&gJHT<?X_H3<G~rp_AiRb~24`9Zp}TNFF*AsAM7}0)p`kfi=?74~l>I0|UbtKiJO1z}_F=By<Z=3@dJ68SpxMFTK!+(Q8Da2#=8ESrkPlvJQEvDZn<%OCM<CXP9Ahg&>SnmXScoJfe1{pkUqPuF!yy>osV6LA*3D=DGmByR?;nWwttq*`#j*om!Piiydj*t(l0tbba1F!x!XDe^X6f=OWOq5PYezQmCEeTB&=fgPk7FUX#3kblfLUUd2hSSwjP{p|KL<dy){{Wj<wuzHkD0o53iSI?Dn{T{-@<VY$0V&E>3dA;b4aL?1UEWOjvq3qUB&%3Q`kkmZNmN7p_v1n!<2`F2g0l)D%LUWD4^FGmwu2OCM#Gs3k};N*tK;Cu`<el&RZHOEjG(0I1p4VBQ+{Y7D@Q-vJV)94X#>!7Zg<>pJOZX#2_ppt~^h?YDW03J|SLBpi8lkQR>yprif$;1#@xVE2CMT;;xo2H8EB9DeRgtF2CLc6-Qm3b{Rv&hn*Zh^lw-nP@pQ=A|SYDP3PCtkae@*BFgvSgn#hfxk)?>S!^g|&mMtC`O&>&hXrsC+s6NDGFlu(;vB9DKMwb0`nP7-8r{64MSf=ew**Omr=yV&J^0g0PA;?Ha2zHCcq>E^BvDt&ik?;5*FZ6i5xvJDxxA>#J*2(?n-R!%c0eNxYctGi(%!WRasr>K0rFtn1`r5nbq&mKj9{$X`@l@{(T5k}{^Sazlj-=;=(gs?5@pvf6e0j)G<JDSt{3Uj)eAR1?jk${v`yMHyut|M-G4`_DLBWRscHtcsc7=;q3b&2Kz~#U$a1anIXu7Zs!cX<^obkaLzY4K21Xp_e&)Fd+|UurS9`PEr<QI1aX{)F;Gd8w6=J=w^@%Tc=TqX0D$fKPCwk9)^H{A$55|>XA$^I2OyadaPZz9%0|h;0H-v)7%Vd4G>W@x<b>&*~?18b+uuJ&?lJ4sJC#GSWQvS1O7z#Zfu_~g0tW*@n-p0eFL4JYM?=^!ovP_Jj(|dW>}CP5r90=q*^w2S4h}sW{b91!aIbPi*_f5Mm1O(cR>JGXxE^gtD%(*n8|h%z?NrtT}vLi6PBD&lc+%rgiJ!A)S^kpY0ZUW4YE|7O*afO*`D?qB}{L2nBus07*)?2sBah(jZP8+s_0Rg<nplud?lmHtUHUluyZA$i9eSha;N=GaVyDgSmf-!h$JK+1(xUsN~GP$JKe<CK>tzLK&f_uV2mM=`VYwOkhv{rcD58Q82#zh$cw^7=mIY{Xo{(+nY{-U&35;Wot$uHJv`JMgHwoEuHC2yVi1e5vOY0Uy$>#$xc@^po{7`+)J8y(_9ob7r*$`)MAWt?o;+rs>nb5lBxtXQCn866z%+md!qa}iF<`*)?rVJqpinyTtj*7%u~UMkLE>32BR__3Y6MS&>_aT$QdTT&++E)%A{!B;?59h*BWLn(#9i72pvT*zgg6PK{7|Jt$f6O#+Nn+1IMe8*1bF)9=0e=5t2O!En(nP5vU^y*it2q8Za<w_FDJ}nEowQ?07e83u~QaOAp9>ZE}f*;n=B`9tj*}|Nl^@NPR3KgAdyO;HNE65TgNq3MtqbG!lW6AOsjhVN)Kri$L9iScxbWKW8$H@pVXxS4U)Lbj5`w6^Rm-7U(WSMr;I%sh)0-_HJG_ktNj`G6^xjzuJBsU?df*sQC5gPI`ocnq1U-no2sxc%Gai3+ACo&W=k2*eIATi6_JOJf?;O4kCLo2z(X|3<VZHBJ?NG0wL<1Sjl=KQx-P+}E&&>+J1H71aT0)}QMC?!iXafy+a-~xApJMul>R(t#MEsn(#<W{8Idd1zYv#-MbtaB);|7;1zv<g2hM)RDLq1{6-B$&@kM#Z;I)>jNp?T%10z*kun1!ci4Lz*hwI!&Qa-G_N=dzgMGloKtJ=3FYM#=d9hgL>g_MVn0H29@tB$=8+EgL$L6;g>>OL|3t~I-Ryn4si5*YdL#XNrYI(|WvnxP~*90x=tuDI<GSmmjrNtbSe&uL~1hAq5yFdsoWA9ydI2c+ln5)|-QmbeGF%S0hJIJ-Qlt^4P)zeE&L2W3+2no|3{ep=PoeSeV~C+2Zp-sMf_pLoZhFLX)RUT_JBKt`C-t+S0~`wK1(JSY*ip;!dd>1Lg|*irH#<NnfDEVSrrkjg-+d$x`&Y~qfw;ChhECd&0Aoum8ph29BD@k=63<P6hl2Et-qVZNSSJ<B$YDdP%Ibe$q;{3oYDOMjUwx|zITCLaZv^p~Zks)Z5fZJmoL3Cc@WxRpLfT%>d78A`6?cr<~^W6bEb#?dq?1CO=e;3tYgJMjo>h^+Qmz|k>5KUnMPb!1(&G=k;?@kd9CAB5|x>2>TzM`Q@y{w0-+iYGE`6A=_#EcWKb1^b_a$bfn&s@oLHy}*=!z!%j5=@=gAo2jy53z&_)0fLgW*mIFR)oxqzIf0bGhQ1{Vv7@mZZKguWKb0>tM4EMmi%dgIiN;ggQi4!xT$0iZtN22f2WyxGE?nmgYMVN#kU*SgzfSmmiL5`aSLoX|<(#_Q(J+cksfVP4%0h95FbYM}1c~2(M_4B=+Q&LG5v)fjOID&G$3j|%IMnK&GCiT2(hk(`sSzTv8`ruo<YU0_@!dv?MS-?NWtE)2?33K|8G$GxO>|;v5igGC+%EIo#O7z2=?It@To9NM?;NTLSo$T#s4n=FrUP?(MkUQ3Z1b00{P`ZGuL+61yHp-xt077Z2b^Gu4?<yvbpjQlpILp8BzeUePRF%BTMb!RJ_=dsI$4MjA|<VN5~0=x=q|7P-X6-J`WsFw-HXyM_wX0aC$;XsudCUsvTC%|kWzZ&3bk~JnyTZR*Ex)`MQEYU?drccK3m<Mq`pZcfO%PL0!;vMIvXl`<oY(3q-5eAfoqK-|I%}khuxh>Mp7sNQi<zCF=CyeX`7Coy5ZWM7Da@iu@4a`UEc4TFsPdTJc@DKVjSukJk4P{e{f8vl%N|vpv<HgtpDAwufOnnD7*(-nwszXr6Tjk<^KSr3!GL<5~EV4@1rgBF`TFXM)s<Pam-L6eLGY)HV7YvR_-pKszCY;DnZ+7<8ULM6Bj{SC(;EXjc5my+lDrJmgE}YzAQ$(ZHq33Aw!SkKgBgmdGXJ<Xt*E7bF%&S3hxi{-3M9guc+|XY2xgzl@tPpKcc7xaK^n`8LvVl4ydL|rQE8K39vX?Tt(jxOMc9jsm6YZRb;ut8ZY@_S&V`Xs}d6Phup;Z3a6kq3zdh>1eD>nI)SB%A?YU}nL1B0kQs$UHgFxS_sd&CGv-uSuTMtbhnWFvG4^nAq3)A9K3;NZ9CRB(`CDDcCz;a$Lmd-_f@4*eGo~1LZOvmpPCAQD&eQ@~@FYtxgsI0_VKf}5_axWCbZ}2m2D2x2kxA(wOP8S-;DgWk6W%$UE(znOm8Lu>6U+(>u1Q^jEIAQ%Mg}?$AyukSmtZ>%>s`gXe-yDQ3mH}bfufGcHX#oH+hfSL@T{|sGj4keuw#c+YfOglg~s7vh>40Hl7W)NY0p!#rZBN=b7%HI-4r~mijP%@J|O&J#=}MTs(GU!D5UZaN!sr?zI7_IT$>JN*(#@y>J^B+8T5&5u1BE|p%mT2rkFVWZ+{iupJ7_F6ovRl!$t}r2-b}m#`a?d9PvM)nnP{@5~~q;L{0`_QCc~*N9%cCcp?)3i*YZ80U4Q|oMy$F;j9>^ns!xKhuP;dro7<3rWY6(u}v|p1CEkOK8hf>exy%+K%DbZONDHNMaMa-4B029Q9`6b6eLi6h51CDj3AYvsIiS!32^6mkBYj)4zR2!8BdhJd+3*A{1NsV%1NOU>sb;lA}jA5JJ>>GLX*je0(3PQMk|6N(_hCQ!n5S6vCe%MazG5ph6HiXnP%W=;HAyy<D&v}PXCu-CYSK2-b_oBgv8+!sVs?(l+cEc9g;qElY00eV;HbJ7|5RL?*q(ruhSY50xtAzr7B1EUPEL_=N(u^S$I+^>G7V5$nEe!Gce|<{!RiZ0L`ugRW@`$VY+>t!Yr!@>WK-T&A><~5!c!tTFg`C1dnBrwcUfH#Z|m+h4!!ND>z)jE;ZcmiE=lT)Xa{xcSeRwQ_+D{><lNPpyEU3(NbJ%8cLZAKpaPBp^x6XR7I22%#uBRaOT4{MOnI0zOCwhke|S9kLGO#{qqo}xc>eG)-+tAhnmw(c;UOxJozYWX%c2U%HHo)!HJkYi|fyTTPy0m9n`LB$}y}DmOHX!CvMVCGw3m)izUX$)==nfWE2Zh)xp_jm%`ASOUBFNAl1=V2y_!O&B2DIQ4bQ=;DnWlKsV-mVeL@pYmh_6B$h)pg@pOm)!7b(9EW@+GpEgqXP6LM&Vc$#g$1zyml6(cS5-83Xa+eS!wV+j-bKLLsm2MhkWpr16B?V(z|5Az$0fo;lS7qhI|Rw5og6Zr?bho>?G9l+)CJ@QNty$5$EBKdt!;<e7Gh`?Il!V-X-vEYF$1E$5JRD=VGn9Zz;{$Ks(33|3E`no-mpj30<X%blmd|(mCMdiY==UHBRa=U=w`+kakY>iaX+;As{bGkZ$s`>P-`<L-Y?KAk1o&Kw8I%r!3_IErZp={OHcZ?Yn9GXq3~hP5w{*PAXz2yY*(bAkom}DSar55!-Ke>cdX|+w37^bdR`Nz>!mRtq5sCZ`pdTZ^FK60XlV5s9N5}cE0=mANOQRPIuE@WE#B2M?jm#-*)8AUl?cw#$n7`ZnRgFC*T`29se=-Wx-iniwT;(d=3Z<XSml7^JVnTh(z-6EPym81_@JpJCFLf85%zjvMndlauPn{Q2pCj1Jm>Z2{1|HMo}1r|s-MgxAn~%D>@N!jTThkJrSUWwOyVkoaVJVs&)TY1C+eERlCV@@da9#JJ;WqB(_iu?O!D_?u=Gq_(G9#Pq-{=e0d)yZNoGT?cp3_U8(Iq!94@MJ6Srqk%Ls--+=d%I5Pmd$sSRYsn5fplaPN{rwuW(EX<yc>keI8{P*_JfR2#C!o{D=@z<|bnk$lUHazBu50w&T8GIc7QP8)c)4Sb4#JR9wimI*-(q*AHGN@CVA&u5IBc7G3mlk$UQ^H?gmhkz-8yeei7vFLKR;6tbZ330bh=XxYy5V`tj7%G$>WgtYSw@@C-W+6j+4hK0z_rr6rkD;sSr@=&THQauk()IiA*T+#AxG&S#Z`0{jt!J(jizc0K#wxMQ;WP$S_*vSC2<x{#yE@>zX^(X>=WO^Svjxhu!sdp<FjXL2w?h)(B})G5t~b&!^&gjEuHiG$S|2s`4XV!l<cN_`^`o9)sUu+UNG(!GGkc4L-7-m&Z9?Pa2@PII83pg8E){lpj{DeD)G(UdPM{nTf*cGCcA9I_^xGI!=}-byMGFot6%|UL`0Yc7F)GRl+((?k#vv=krWssE_aaxNqst_*HX>;Lf{YV5A43iqr>z3)^Oe&w)DrP)0_|cI;5&XVkE5z$&8~tNCSwr|%sVOFY<3iHVv9$o;C;;eT2KehLmb~Q<u_(7B|Hv8;cd>OG8dkda7jhr%q&rqmbg#t04ThxIi7J@(qInHTAnu)@=lDw6|87{QaC|JQqx__T3aL7`t^cXXVi$NBEnaq7YMpzQe*A?EYKMtlWWuG22TU5y9(I2IdXe;3Rx-r?A*9eF6pAiB<SLvdf=pNNMs>3WowZ_?n*{43w6@fw0hWsvY6RXV;i2J;Ul*m5tol0C^nZs)9U!K&t>YoST@i)s0o8=g#ZskyD4TPi5j<VVV3Y=q6|GMTm!fF;9`7*K-NAfkCw%2uo`InkUvwO*ew+|h3*0XfPl}x`vEK0C|HiYk!M{TIdp4iC-Ahwjz8o^F@ZptBqj368yygg5)3{p(iJ<3I0_qQnMiY&(2)WA%=DN8ue>${pL@j~s_L4V-Z<dkkj0lLGwAlgBA}dsdy*kFrQg7&qGU55+;Djr{GTnYe(UfIKSzyC=P7sJ5LN={b0xUb9(D>=de*Hcyv}2#IaVFRYoXTRE}4#%ded!NkQFACy<7otFDH&SEtk4$DX8YwP#Rvxki3(YCSg^6Is+VT&z^wk)eCJ8ODMZ6Q-oN}F$0s_DhhijmM-Pt)>X;hWLP$Lq6^U~YARx<(*R)E&U#7TRB!iX$lO8DhSz^G1Sxh@8D^O#S{8a$Soy_EqhWD5sremPjpBuqkLV=#ACprk;bBJCrJr343}4r-a)rohdyD&h-pT8Ax1C6snNf&N>i)#Zp4Cb^gHx@BGhTT78lgky(3?Acv5ut)jM(oZJ4D4i9JqNp#cG{UtCyuPL0LlQaT~r4iel?n2tv^jvZ5){WrgQoy>a!rHk$re6Zx?a+TdkjU<N{JSOps@(H5$77x}PXmgv{l&%29agqf1{*CGTa3OEA-Rica9SjauGm&Ar$jBv)vRbmZ}@iOauD}uPpddf@}E6jSv{?cX)_nSHlJZ}(GIGRjd&y{Tvcq5+eOJw_QF8cOxRi~?-!39g=;nYFMW~S5Rm?>O>$;VW7BaiD!^wCEVC;0mGnL!6SL7q?VNLMRGLk|upyUS|p>r?1eARs^*DZ!4FDzf9fj!}4bnPLw0cPM%tAS~<f#>6YIeX@<wt7<A#@ig5YrsO5VL(iRkW0p*yhDIpvgrd;4j+#P=Pny}!k?%|=b^y0ZwEd=)ohR8o_X)2PSi-(fQ}hB#t_UmA3^wb1r0qqQ1oBIW@qfespode+XQPmus&V%srcv-lWE>G)ylKLe7qAlDwi03eub<WluLSCc&;TfYO4_cL-771+QzS_2PW~S6kG3evB`J-be#~Xtva>47E3h&>r7&%52i5Ng#aqPo<RW9`{X%tBcZSRy<%(h^K1f*u_L%uKYb~4bvW<CC$4vESNx~Pnt>r&~b33aw&I!j~*8rqrcKQ#Eh3=FjXB2@dIk9BFmC9J?LDh&DA*hRn(Seej(qUoj8oehr@33HTp3KD`<Z?>ap=(w9&2?c5O*oWacJT@sIqEuDJeM9VrtSqsDZmxLeELeWXDUf7=SSx*n*1Oq0@W5ByiS3D4Z2Z`RXRgD2&4y|0b!;ZK2M5OQG4ZGotRlAdV!B!0<UHi;B-H~+qD{?3I(fp5X}g<K{0`)s`zn5C{Y!?GC3>f8UQy*Mw}ksq)wH;RFM*queS`L(M;{oyv?PRbI|A*0++maKX*vaJ8@s|)Mfh*b*t!AVBH<IL9E=<1#%L4RnhYlIWrV~${YKAiHAyKXEqyUa`A=0>tge_XCZ2Z08OLDMS)np8R*pT^c|@a8T&~V|Do`UZHyK`IOSU*h#@z_Ht6WRD#CJ6amM*4LENTw{xq)in=G+s^l*`R_aEL=e_F2S(|RAYF5@_;1bON(iG6QNfSWxljf1qc+t8<`vZ9lwG2;SU{|v-js0$DeDE{$&wH*KX2p>&c18a;>#{GhJ&#W%o<8o6ki>+^IIzwc=N%g{tl+-B7>maJ)I44pP0Vtp;8byg}Eu<|<zCsv2Q0xcq6!6;Qu(mY#?O-omjU+YHlwY03x0`Z1P~iLq;!LDTCMfq^A1diouUGgw?_S5;plkg8%{`J|#6KMVkhVLe9NFWX_9tpt%!9Qo<2K*0;0*c?-~Iafi{o$DAMU>lKPufz)1N8Y*tdUso9m=-8Z+7tfhs(_dCIoJ#Gq#{%>{gwcAMgoXs@kmdFaB3O1f#)ewvz#niXRyAhzyzySx9uYfQ@}eF-0^Hw(K@s8AYt|I(;vCz8}+lK2qgeE(j0%MZBX-k-m{Vb_^c$94*Na5WTQT5c-~(NJOyylCzc66i@e-m#xwfBN+K)%^0IiPU^3YPkOR`ZKw|0(aHif$Q>T-f-&1$y&GxVpo0#ocCK;?Q#*%EjP3TZx8xPDP>J8{zlTKIhgh2GyLyzZw47GwNHr~nU)@5xiT#E$8ZWSCWYJakG<}>7H0P)x1ObSNbE0%^#kUo|Jj#+3j7q}%I}lZZ`OSrjr{|5govktC;5+Z^Q2aLu2;>nOGbVtrRV-2IldV8{6+PI--3=WAK!lc<facI=jTaky)A6h4@tTAHhM4x%vn_tZ~D2et~^77GFVeHT;jr$T?TLT1jxfwtuCS0voH##7w%~KkDq@2?k<-9>E|DQ`t)YHueT6!-*#bWRMFR*v%~_9yA^#MXhKdrm`Ui%|K;}|e*ErlU(WpJ-%Wt@7@WB_?4NBmQXF+_Y`uE3J?<#`(YQ+v*UWZ>1ezh#DBQfVubUI4{qFx{7peFc`CcfL`|SXk2pq}A?%uTkEj2gz*HJC7I`;6P)YQaqn;ji@iw{pW72RnHX>_}~0Av;uzmXxDY>scFV=rqiM7sY(n3)TIt|J-a<AThK$oWG}2;21ue6DP*<D{$1R1`JHiNtL<v?uU0J)rgb7L~Rx=GwWFgL~K9pX1;DdcFSgSd8hC^UCz}f0iyFxJy%`GL?k}Gr2aZO_4n&ZBT%NW|R4@x&`>=uC7B#)X3Mu(zU%&o2jn@j`z$j<Y=V%wdg})p-Rt{d!g6bG@Nu+?}y<1Ovd7HO40`1c+&_gF9{nMts`(x4ZIMyv(-l4h4)t2l-}Wcz1N)H7d*5Xjl*2lyz)d#GwD5fy^~?@4>V?#KYsMt)<NpM>3Ppow_>93Qao;WQ>q?|Dy#N*(Vh-^L4n}mZi_fK6^qDr(pfuKst&AXTeF(AR5tMaom`-6y9C|0l67X2qtVPp_BBo{Q(EPxAkhE}9o|{yC<5p=v@!qmfbAajg^Q8^;Co?@o=o@DW}eg_6iDP<V})QwAz4Q-R|J?K65>Ifk1nGpYF_GBg>l3v+U;*rA<rx69$K!GEJhhMe{Bkp-MZ!)j3VwWkAYwNZH3wlo^MyWMsl!O1kHjH*Y6z5U>!{btl@><?7=*GSz#=oiILtm?rUWBwA+R?K*#+qtH8rg^Xq|fY5<-&-H*WFUpUf6fr%};T5?HeM!Ba>jG*G#q4PiGkxNzs#m3{+Jo{!dtAj&thgBCoI@0fF4VKB{%H}2%t(6)~=p8#Vb<E6&{pYd0T-3aP<4jSS5dDuRA~b8>UZMv|Rh)xWw$>k~-EVc<Z7;I=JLOUtY%BC>#T3ll06Gyxc0>3YHAg`nG_%(Ii5{E0%rQ+HUq>`VunsRTM);YvRp4$_7;2;<poe^*AOuo{@1u2OUD}JT%g#k<{H~p4W{H(N@b#PXFo51ughouFEiUp2=ST=)!2^|f46(N%{T|_+_)-?aL|(&!?!zXcZitD-vd+e!!pLDu*QNkGzilEN94>dMV;A6W054}9RCfj%usDSqhzH~#FEMgV=(kOjDreuXub^L+bu<@!?+1CA3GSg3S2=(}+l-0M2+u1xZJRKW0^|4cAA3x5SETMT`K&mtt+2D&SWDHqyeNuf;hPpsYZSZf%`7BT!MIt183g|{M-pen+ctWYLIDlABLZgtg_+%ACEKPhW9|9!Bq&J_oV>DaD|-Q?_z!d&xc-)CYviwL7YvUoN20byrRVO|xC7JdWz%F$glhB<{Ki9Vs4aS0Opjt*tnJo1z)^37!bKCQIH)H_J+rj>9Al0SU!ZLT?eH7Xi>JV;){W3jZnTAhC}|7N<HM?`h|5+<2yZ!^u!nN=DzH{;B$_JnPS&^!Wl`{chSf*l#8E>hV+t<QF4Ssa3cIvxj9oD=ecN_|90ps7@Li{imZOumh1@4ONN#u;94rJdfz?d1oSfP8vH{5FC~365S%iHU8F5vkN_deL7|o~)_FL2-T16qm=E4N)ASZp0u6cr#F|Dgt##zM7?}OFRIic!s{|&>LB|U!7I@IvFd894$%zG+$?=OF^S~@R`@0+xqyOc<|Y3<(enA$w?JvXQm@B&uK+eY4<q3o+a#Z`pB(t5ew+?k=Fp2(yJCKzW*yC>+OLA_R?-3XJ=TZcO)ba-g0lSmB&N?~PS0Y*8g`MRi~5p$<OvmN>_f^p9Iae|}-^|h?K05%}uZTE}(;02OVTzERbmDZy65o`oz<7~hGK8vED*nTQ}z`=LZK5ys`(7(CeVmrAgdHuMy-zL}yU9ikRcuO_(7X&nma`eJ<2z#oDkc^>~0eb}M^35jB0qeLWOnE#p<2=bQtOPjQ3)d`$S=W<`fkVQfujz#93hW+!%~lDcV-r?#6>A-Z?pt&;3<-eleW>5QzW#!#QTXhe8j8nypyIutXbZCPom+X#vrAE;)Gf<JVwBcI84-0IsDP4^VsbEM?&Ha)D~SUQGvUpCy?nuY0ZL1N)<OYHMKwjy1T#ciXR0!{(!BS(DmdT7qK>M;V@P!u{8^1My%OXbfbpTOLXSC8g!H&r@&qFKB_OX5_5eHQc;RiP%_EJ4A`D@9L>gHErN@{$+>Two?xXI9WUaAUo-uC*(I@yF$Xi5N;k*nv9OFP3`)%Z%>1y~e3Q$0uXTWDs)!(~#(K@9uk@JYETD>wq4a`E6TI<bv`L0n03^>{XbjtURuQtDgY|Q2qj<Za6urHF0Txet7Qv<#qhD9#eL2R6e9vq~3iodH->t(g=yE>v^8A4T&M5a1XKS5+`NeywzBB$m|QT(YB<)gDH6P;Rl2J#t?ESPr>IU!QePMvOP0MpJLoX}{)W>vBKC>$<51(0Af+*q3@XPq?Zgmu(|-l!pZQXLS_i|LiBaTTVRMwvOv8*YHn*~Y|b*D-nYQ&oprA##d_O#YPa#X9a;S4KCNRw8I(#rwQ>uMAKK=X=ow6TqFuIGu9X&SV{!ffY(E+;a|zzEmuczCXx96?*2ZSFzY(QWOr1EIQo21eA(G%&lDDm#vqI9uJjEBTuE%yGe!2Ks;n(JT}n>Y)7YSK`XM*V(v|=)IVwGp~B|DxY>&qo%v#;z~UyFMY6@!YQ|KQ&>gMb9a3u(S@r9Q){yNy|Je+tc}ePn4-qRR&=hfgQEM-7fZ?{}^m3^pnP-G4qh_*i1L-b(u$CbK8#EqO&xxbqkh<=>ON1(hp$%-P3JW*M^PPHbyUQp?W`L4the1Sd6(gAP#bV%_>_|bD#0&enqRP9b7QlWj8*YuRa(7wk#4^~mEdL3u5GbIx_u)3Ylj#uU6%Loz^xS*AYr2|y{3N$CpEg(r8(oz4mZmMAkjtJ>8SWZ^1z}@u5d2a_PM13e1~gVy%!slQsQgb8`2l0C(uCDfJ-YLu5MtNNYH_5h2t)*WVnnWM7PUZ<R`<bPl!5}L`lz;oQzZ&l^LQMy1;oNjc{WW&rHYORvS2ow?zwkO+J@dnLuUreP7$pcb#j|s+sUc6pr#9?4z;?^I9cXac)j?`+*eno6GxmSJQF2)FeD<@KIHKy87K?HZG19X&3>)(i8P<k`zswz^d7mMH#iJa(47G6KW|vWPC!^5*cBDcVb21&ZIg9=<QB5RDn>6NY2Q*?bPWPlcU6n>WzGDqOfStVT~!K~@ewJimWd@YIZXCCTfk9Rx%L_MNDl>52(l+f=%%{`r(Gv&DkTIgeBEpv6_VVBPM3sYcef-Q#g=y+%}}AIm4s$pQ~(TT#F6|yLht{cFl^U_K@{ws>yrG2tlI97kxW`xw?c>X2=u?YE^5dDw3O*fN{MwrQD8*A@(x-RfQ}Fg=r3a!^|&rw@gGe`&&c(1rq*9%m?jm((Y9<?*gAKVkUBb<Mg`}^Za{PoT%wu1jQUalaa}C!ZS)J~Koe64zgRAbFG0C|);jVoLYc|3?S=(nyhIIWLUZ~si*B1mF9Y@vT~jwE?$HBmV~}hET^vFus{q3C1kkYu+J{+~3e_Qo5m2cer?8>x6JRC9Qo$vbx%xDHbZ4byL=%8M8L<^VHO9!J>mZku<wgxC)0$`0(?6X5;ZkY1&?BQ5JFuhB5ph{xU0jq++T*Zh2#F}$#XGG<3~e5Wrvabd>opfk7lqG}=_Ya-F#7Y^MnblE=qruaS3`aY^vd1P8;mZZ6X45}^m)>YJpoQBAFNUJdr6HRwPw<y+B|~_STRg;zMpk$qD8enTnRQl)Uk>l$O=_z>JT`bv2Ivo&KUSgXtmYK+IDnhL2j0EaQ*)KRV4a}SjE_=5w8&-3y4+Mu<bYr{yb1(O4Vi_A)s}_t?o1e>YGuM^F#F^_m8y;c65No?o_i(uz$7+`fyMTKEYMP)=~BqqXa5CmVL#fWv!0~MmB`c#lwRLMi<etLdU|*MSyXS8L_b4JFuTk!slUmC25@}+1~~JLeMu(mfsSy_^V6FWhA<y(iU!kx870_mNjxB<Vys+oZ&BeVbe`vtK_U6N@I92kF}@iQjvEocH^oV3l#NHNIL6Sn?!|=);7wTeh6x*sQDo$uo=tL#yH!4ZNK~Bd;cz03|!=Hvq)g-<RT4p2=~(=l@0Y)PbiR5mar&l4a}-W5K?H5F5yYj5YwRG$pl{loPqlf-~Iaf3zf=mdVP^!N>!m@TlY~ft3sz)I0iu{4ELf5<&vqt4q5?LIx;?d1_nJRjibhrd0I$mMz9Wc(OY(1eUVL3Ez!3l^^u?T7HC?Trag2PRVUeQdE5<TD(-84XJ;Om<A(f|sLzg8?m`^NVz_j|t$wMf^+PrCOcBi`rz+RYT@6B`Fqtss7+3$<Gd*+msE^IGPs3&kkftavWynz|kt}LkbKD}?BCfeq!!~!r8D-JhM+!eESR~9Fu2}j0LB5Eq6tT~l>}8m4#(^*+3JU(ie5%J=tlJ&kxBycT)^$l#kcu8wqO)4vN-r0+Wpg4pjdHFw%m(hD>!&SEVx5`Y+N;Uhuj}$%qhNbUJfzm+BG_TdW4L)NdobWmFK^+#md+U98Tl~#cD7z)>1E;g1g-c8F<{ho=f1*#Q%dBmlNj=iqalx+)-iAyFv$xoh_TFFTgK4s?p^1DBv!qr!D7jJSz2lBp$8t#JraJDgmP$ih71=ab?41NkwZ9ypbLgyzV06-t_X0v8Mb8IvILb7H!>ovN{$xp#H5Y>a!Hj%Fse?0P0j9AL2yz6DNqvV3qel%OCzHO47p_@Xq7EHYa{XZY4^4Z_qa{DecBNUjx&OyqQ-eLUVk|Nm)i}u{wsf^_gCez+}EWGP9!gFu$tg|^|m&^zi7>$;-MVAO<ILw$-FgQ7pG6%1q4mo@+A=&&dU5#RVx*AOV9tsU*dIX^r9hBUycM7Bk^$}bfOhwJ!=KVNF!cm7~$(drYeCZgHlc1qk-_Vmu6Cz2I~6nV4o$eS)a59PEU%a>#4^t{o*X^x<GS6`TheC$o^7Q7{x$Gin+bN%z1&DguwqExZNJNrct?~5}u(}>S^7e)*-fP<rDaJ$lzkX=T=C7fpygyBdmXYP%a(;Fl5-}aho<Hh~;_^(TVg4rW6h#vImPj)d^fsXn})X(Ne>ZUM%lB-jmoV>$dHg6R;yA<$>C@kmRAN?Yixy;zGP$66;~dqnbMzV(Wd|)Y)C+#(Lm^&ZP`lSAE;*+B*{Giub>RhlpB(3q|#9h>x;THYgGi!l99h1X$oD1Pi|&ZZv8|gfJ*%5Jj@kjkCcVg*J#@=wKacA_^j7oJ7#~K94V-@$0K~!9TzL^y%}f<c}78l8*oS<{g#4`R)NPlL7RXr4RgK?EFqMb$$yul%x_ctu46|#G;M8|03&EzhyN9q@X(~Ke-D-KEmDa&IwQkG=d;U<p%^Z?A4y-8}x<b3c&xE&>1=YYS&a9ylw7AH3ZlkarGV-J}l@Edd|>xJ@&OIWLr+l36ZYWS@p??zuI>~k54M$Ec6_tOD+jUf^p9^wNC+egXj?0=a53!>mZlBLKmXG=(X`jZz#yg`rQlqLSlvJcHzY(mU|;AeME5%jIsHsV^?9%k&V@qDDWbkzSmoK!P5r!3qNRHD8sT>IXY$Ecj{T8?~kkppes8FAV#6pA_*=+enG@pp<U#HUIk?Bhv(`uQjKR;9|j{$qI{x&VEvfT*v;rgarx+wIsonlU|5rSD&Squ3J>X}o6WsbzEo?&tIf|VG-JrY;mjK<g%sV=xt0&>z?bJfK8(i6S{d<Kx);`PkrgoP3tpMja~~16YD~Sq3dI>I!U>;5O_kRdY|R#i^o0-&iFtf(tNhdn>;+IY!O?JtL=~zv;Xwfs8SV(dskc!oMNPC9#Zc{vH1ayr{&aH$rTaUzy;K{Kf*Mt-;#hEs%ZlV%oJg{%?|4;81#`<k4C6mEG*znOBm_%Te2S&5MLiF>mQ)ZoG4e0PLa*yGpVBpf@*OOJZG=!*3A!G<t&>@5CS$=Yt%VD?KHd0vyi_Qc#HltRk`7b4{+OFeO_Kx*n>7!}7PcSDB-c5#d3Jqb)PAi1BMK*@^|7nbeMkvo1eL87I%@a9_c_G}lJDY7>tvOxqiYFHf!?DNu`~2Ka(V&;Ttt!bafC`OCJWnU2ljo<O2};2c0$xgCRd1xmd4awl#O|H8_DF1l+TUAgGe{2S}`Phgmtk3y>u*wab*0!Ik;1%A@*Z9_mnL?nJMYiq(aDMO;b~=XaQV^sHhV#!W9x+sJY%xi9*UCWyJB9h{!Emp;M;|pXjCz(LyJcBMFH!d)ijL&)E+5AM^?n!n=%NjBV`ti%Xglsk$i|i<aGwg^&-Z`14z!Gwzro>82R<l+-{W!?nv?iRTw}7_vWKsQj##HRSYwdA7N(llAR+6vofy{Y;Bm#Za(`UV_<<_*WIZT5Cn~<r(l!^HK259HG*IChM5Ncl=MNE<G?3KgT+Qlj^no+{%@ho)bn}?&g~BhRd=Jx;rI0WgRmwDMC9<#;t?<xz`8ki$OSoQ?eeD_qc%Z4#8pZVT}YxLO3V^-I+9>u{z4I47ZT|vFRPIa}Q{4a1l7h@{C3weIfS~rF6J79F|s-+J1y2BVcB8A^>w%7=Xgu*-Yh2-2<|uI<YZe!9Pl(=6QKJg~wt$1BEt_CKMH+3%st1c4OgtWH(`n;Ae76*#H3^jF6!vL(o3BwM2>lfljrhAw=ayGDhZUN2+(zk}2v>Q;~w24)VN&&C8n6fG+p#%GKg~@F=4GTwUQR)DQTYe?@>Vd7su$ccaDPrqKoHW6I#jkFpv!Yhinf<eP34-3gsXE|mLG<fPbQMT{{31$fU|q3;7o2Y%xuno5BMTP|$Gff?4n4Z}vfb9ldmkGYtQam-5Us|6Y?Nw45=2|JU~R+=@u_6o4WJJCZZ0R$|bOBUVy2HIlxap#>oJO{n1MmMh^_E0GQpmH;GQ2OX?)blwi$wzu9i$Sh)jQU|mquT#>hGq#r$j_mb-Z)UnhC+QOjcgstz%0>bd@j;86nZespOosC($I|ugA9e*h|E4@tq}w8KBG&CAMoL_R0~iz&(@hH2<~qQ?E9gSNv*8^3UtOZkiM&Hz~(T}M|@~1nXMVC@w_v)+(svY6EURyMSI`KT6U}0zLED&)gAVs$)QuML_*pWCwYZ$u}usOJU_KE`|Y+tbEa)p)U5?=3=rHPy?B*_2ExLj5azHq25AtL(l2HN|GN4Yt0TaLS%<c*RNUnB6S-pS{!e$iyjJ$y8rrC0n^VX@$heIu%re}<LLPY%V>PmEtunk1$>HIcrt9vsvih7`^@4sOa+{@&6b9TfMPcK%3-dYe*9J2mklr2IMW#=qmq4WJS7&d%8);>CRb*_3LR5w&w0A)tqUF<iSDH8#eEzPHZz96%wOiqJ)S#(azqWJea+g1KkWvx(2{C=St=`aeIbn&Q2R&d#RyXKf2iWTvT%w&^xa5qb=?yiL97o9+lCWgeBzgU*ZSzOfhhyr2N*QVN+Lm?$7Pmf|U8CuCjioMBg?YI0vn~p8)~Jc}juv_DFOFrKz>=_a3KYrA0>9UR>NkdRDXjk9f=(y9pb7ewei)flRpA=x2{t3iSg;Bq=f>>YM7v0S5~&~v(H{_mxbJJ;C2Ss)W$(jrj79Lr-`w|VG4zI4hx#Y9OrDhz-mYo&0grV&BxO!;8@`H)yeNFKuXnic6UP+_%@Zc?@L=+;;WjXkkf;(9DWdDA+eRJ<o}i+4KaN&qJ_xTpY;!e)A|^M|%~6*A0q3Pm4a?6}PQ2tsYW}%y6oc5pa~u}_H!Z;1-e)+3`lm4S*`<^XIBpu}JyWb}4>h^ZxH+fZa3XoDOv~M|dsWsjv`<WW4o^UP@H$uNiGoWt#CrVhtg||U7}FUdo;VYo3D7JWmP>yjG<{pA5!Gj*f<1pH<aU$k0dH6EFrJpZ_oFYC&2`JA?7KEh6?mUXDe%0f4({ikxM5cF&Q1p!mGnY5h&X<JTNlAjXtHlu>T=IKvW$e%%-#a$C8-O)O=!G4q2~r+@uF)?DJ_V#)P}LCD77(JuAszT@6pC?B9C`;c$f9YlEc`_qMb;!D&LiYw}w!=yB>iv@1-9*RhuyC39$!uaC}a|eTHSz-RYm9QOLq3@FH@$u3jTN6e1^K0zrc~0#Gn|gc5L?%gP+1r=Nkv_v<2t{#ft@Gj$np5q>Qk9f$WZ^IJh3IFGb^E0o`%xvWe-423ITOSJ2NGyqPBgK-ubC?Mji(YkVzKe<XQF>A4%iRmI&SyYiOL_J}(`KA!f7D_4p8HjM7=y3^pvJyaXKMUms+fA-bpAtNc0BmHwf=e8=C#BF((N9WH2|$`qFg+(KUj4q(gQvhV6e=p5?_MR?86^9}3JmsqECQ~zGq&MGOU<-6sknTRpoBM<K#ZJeb6h@($yBPbI8qW25vC}Pq%hjL@)g2|MM&A0$HlyGU@AM&KWGS!Xob*V6WxR^xWurUDRc%XP032<c^V5mOjTj9E!#iq8l<5!!-VsmS)E~YU7#UQ@H5#Xp61>NdP)1muagN&!~#zPYSu#2sp(HN%w3}59&CJarCCfNbHe?=Xzmr$sVcZ*62O3`gdE=7R0iE}ScH_@Ag`jmrXn$pPA=|aFpu)R6$HC_$CqQ5*CoLmShp@HAekq{IBlRPHIOF$JF^Zi<v!24^~snHxx*+|h1c?|174zpbkqn9&%zcIg&B6~_GN~$T<UHyc#~>m0fbz+0EIh`dyCO+B2B`I$`s1_Va^fv?8io}DrmiTm)V?JwYoig1GQE(M5cJRMD7E>bSZDDvcB~uL%mG;28_PfEy#UxW1wLt1#DPavdvS-wh&_p?k8yQ>pz)NGGGlig_9Ly?dse{K?cD~074%NO-WOnDqcp_+gc{MXMmi>3D3W%Mp#qJ+B5**dhs*iM>yraDzhv^f_nc5t^QKA^FmWPt4cj@q3{xEt}-r`#@Gtzgo*953gMHFdW{zz<ts%+FQ{Do6s>EM!dQpc=!{teM6v!d9R1STfSS%ZsVVz-SG&!>)vKYX6o(`!7I5T}J$A-I1BMQsg)O9k#51^G_u=-s=9TW*5Lu$QJ*rdM=s;lOWytjPpk`7Dh4Gd=a?up^rN=_o#=QFQa+c$LUOMCQF2Qb0@-t|&yG)#z7E93-`#P{$@3RoZx2!9K-iSnmNEs1tvyuB@4g-54LbLN9!yYP%KmuY>Y~P_q#ba~Pca3?tnI04@sD`0*lz(IMYjVUQu0rJZv4X*Y*A#-yr*X)6V>HnS3IHR`AH%8^SOFO8#dt@(h}L*>{WkNiRttxnOrXTb1#`m2sciFf0rx<ymvS(HSLYfs*UDOlEqDeu|LlmJ!!7s}plIvh#>9KHeX>Pds>*>*DJ*Pgz$H5IQ}Sx#Si$ZPVEz>+=F-23q{!GT!~URj0tcM3%&6Qn?FJXP6EyM0W(m9BOwoI5Pe2uSTBpm|)6|B30(~vOQ4dnht|YO1skY5&hcx1`1&>L_Dbn#6SLO$-Md#^^k8M~q@8|WxtAazOtWB@<3KfV`+trfC1BENGn|QY0-a6_h%D#?I;f9Uvpr(^JhM@PGPW6_X8EAYK88a=9)+HG$guj5FMf*|kwi^{FVz-Tc(gk9!0-0586jFMt`grG{#E8Dwwe%mVep^B&YSHIdNX8MNfFK{pgfi%W#eOZ@i%=-O$wC1<hlC8@XO1L$w2X!P8}JTASuTKdWuA;27h&vL)y{L>uR>D~wUu3LCY;;djG{_9+D%2vGJsJEKnyUSzEYKsNt#iZjLltElz&8s>of+v$-LO*fEV5nBt*B9u}b?(hq3f{H(+B)xu1Qt13URS0XmU;Kn;@?X==W!*JXKox4Q)PuenJg{Fb6YM_6&FMn^}$80k^nz0anKTP=^F9$oaL<<1Wm(C|f#<%=OHN~bW<;;K?5iVyBOC(bL>=@{97K~9iQdBn7u*1I1l5h?5k-vl(oF_g5U7mxM9=tiQ(NO}R}LYONFVY}!Vm38SklzJxrMdmqF9x!%F^iF0@jqCNd&nbr4?oCqqB<-d@hKRBe0Hk7(il!?gKU=@F50m^FM)f#RwE4ELj+*iYc1s++qy?rSLLbgQ37n(W`BQ<#H+rbkY!+ZDQKVK!oe+dDMt(iG3wfx)c&jDFB5vYgd7bk%@=>o)lxPLeMR#2;YPRnqoSMoqaheN{tNQ)(8Y4>=^f({?@qYhb?uT*WQhQ^j!$S8#Wy#|dvife<e7l5E?W&Lyy?+U>!WQjGYx{+_?t&~`jbc4)KCwE9Z#U9rF2D=}DYLL;VPmJqjMH3|>%4m%(Sxq=`!|<u4T);N;Saq|l%%6Coa&+ed6~=EE?fVTsi2hc{;jGoimp4U<Xu*x&D31-y)^CE7{lh?lJWinm%{>w=`iv^C^J}D*6S1tA(!`IM72qgJQ?G%K*Wux;cjPWa4wU>{B4`*2J*{&A7l!7Wi{kofVO99{~0imIHTKA9?$3J*PlLpel@?me+8HMkXOI{`1&)x)RY%{<)bX_M%-WWsmXLPk)-S^q&X94QN>;q|14}qxyH}f4RV?9w<AT2w|ATCB9?Djxj4~YD6Ko41;@MdkG%~c(a(1JW%3l>sz1c@w~zCst^Q|U@(GgK_Mb~7n<BeKA81@WvoCgoiXWKss_e<1a7m?hWln2nc`H@d6`SG8Em+5n`!L2G`SSVQ*N<-c;33q?>`q6mO+VKaQWI)NEdSIDjjAb{%j|$l@o^%zkonu!Tc(f(17E9i*$iRP!r^PND~);w9b?*>;T~l$njs9w|ML3}KYsVOFW>z6cc)_qJb3ocwrj57=!hJuX6V&h;BnOLH{w1xlJ2xQXKtl?GlXh?+grSDzt-T^u4(Zv;7mo$RGE$%$&l<G0Suz7U%$ZO!^2-wTZ@i7<+ugxC00dQ9FsyL+%6*knZ%4r#4j;0rEhj)LdYYM$tN1coF}plWsFY%G9;pY59I;OucObkb~#QpD<#vaz2co_<XwT=l%T+=Cw`1N|GKF1B&4LoilBE)*>IUZ{rtmEpMG4g$Gde;t(rAr?Ot3>HqwOF?&B0O1DvOaP>-X(U@1L7du^s(?jW3VrxG_Ynv=cgJYR|ec+E7(9B@7$=*N`LqQ2}pHGR(uId}sP2c~or^A6xTszpcGpuqmMM6%7$9F@DKR7cg+rQqgSlq0(Bv+w=3UUSI5rZ)9{r-7G?@&nX->1JxPo?BE~lo!N`rz~aU3zJ5wg>#^=Re%9bvL+E{ydWl1M0siEB|m-kPyAx?x1rEGBx?7X3ue3@O|r`_P)5H{{V8sE)GTcVYO(9ue-LA!S%j*;(&y?T;Zm;l<RvrHx+3OUI83aUMMk(ZG}BB;Xka&mT;LI$9dV-z^GjUDsCtAhRn;Il9od7<c+|iB^?Lo~@q{c<8KBh-sm!CPm38j51}47FA@aB)R37Y>+N_IGr`O@>&Fq=lSkUUve>^fP8S3vteGTMMV=osy>Xi3<yJp<n_Ht3pnYv`L>@t0QST7g81MQ`jy+^n*6pY7^k7vy7rOi`in9eH0bP78W3NQR+?c~l(tUQm^3!@;$35nWE$aeq>1ne}tlUX6v{qycm0zpjul^vp~(A!lj!2?Ijx6qIUA1;=?<N`T7swR_J%n+3Xm!;)7LTpKZN%y@S-)w@~@GLg~q%UaI4O@66V025Y8fJp_4hJ^0(bw%7>T0POt~TT$ibarAquZ}nw5!-Ox;PF=qEqcI#C3gGU(8Q!x5W!}U!v|=wABdsE$0X^z;+#Kr{?553_jHr42njvKL#UC5cKSQWGKm|KbAEWm*O0rreQOP2zRoK5HMo@2UnvSEZ_LNtWWz~xS?&Pd`Xj9n8buyEreko$}(!z*cWYkfpLA<S6mR4v-umbqt^+l#`Zk4a{kNn@qAz9eiq2fT03mLi1u)|(majM^vS8)v~8lm%K}nS4$qI*Pc8I|cU;yvEqdvR)fIf04g)H}{-te3(uVosz`H307r>Wys@ft#0qml<8?3c;Ndv1#Fu&~*L=Or)CcJOY)$T?$u|U%|mPAMrFN#Chg~3#Wq&?JA5wpF#JOwekbzrloXbb}VP!w$MYZV_-`s!dSmvgC@OiK^@?R}#%QpgXQs2I9)v8>+xPW}G%^|xzS`Mf=Pp*TibaZXXt8+6946Nq|m%;r@0-QQzg;4X-ST-$!gsAZ=c=%gf7i}8cOjv0P+q_X4vF21cim<WtghIqIL4f?Nk6s%0wj%~m`{#t-A;$hm~3g&?RfPM%}%t{ol_2XKvTy6-@=FkW}jv2b&0_r9D19o7YQzEQDvpwKLJ`wI*kMDPP$Zfi*!Jo|rZ|lP*HiG*4b*7`784rrteV`X+x6Fh%5uTdgc#%;p>)iu~flteN+~$<8yB>Bj^WE&RQMo&oHwX*z{hbI{sl^W>>8A~8>%d;lKwlUk!6KFI81O-YOTuA?b~PZ_ILJ&o*5yGC^>*?a=@w{TcI-RXJq-~upDVImyQ2<PQb7i($Fcw}O8GNJLt3Xb2XttfuOiUe<8g`GR~`$GPR?xGuqh%v+{0IJZmme&{&7S34WExoOnt1PFKv4_>F;A!7C9svl*hbc(+Xf>no>1Ur1O@$Gj=o4o9pDS!b^-yE$n3~s!T;BGtf?h0;&|Do-e5lvCeKtR}Nt|;2Ze9Pp;E>JGXWGxUd>b6H4b20>1B3u-h4~m}|pM4iwZ%^8TAVk-GNUv?G~9{L|plWgF#uvh=)}K8O+B7SwgI9T($J28}np6vh&^Nwg1)aJa-f5pJeyc3s(^)#pNn-b%hLcajn1%wVXyxBzz`y31(xCv$Cemr?FxYNKEF4A|X>Ew(EdWsGTPBUcuu10>IbX1j~-73f?RHr$$u<*sSZUV!6s@4c>xI!^e)uNWx;Zy*FLMSq^xB(HOr<SUbPaRlki$Yvbap)1s6tP~!&jx9)yknE_;Ad3#H<6USx-latAbnRE#^Cnk&))j;tT1|<fZ~La-Lt1-%#m37~zphOX6-XRSTPZNO&zfx8CR&OBBu);d@?55MfI~%q&bxM8bFCp&Q`9>Y-B^P}?m+Sa5d8dfLq(OU`cq8<<8@f0eEUS{^z#p57jYG7ZzaS~Bs#M2_w|<R6MG?<box5gIobP>5Fo%L!6h3?$*ugAF6_(lz#CyFF4Ba+rW2Igd>vL-BXRH`K02OfVFi7HN1aj+-S-{p3Ni!h*aJ&tS^GDjqL4}|bp?5WH9{jyrs!T5;9GlJ_0!o_e^du10=*K6Ab)v_G``lYWxtpE#(Lr6iV8V)sfYdyqtYEOgF?`+Do^V$$!+8!N+7Jl#ed{Eb3@q+^f4(<Uc`kmNtG>Q02GH%xR8eBSt1Q}^<Fg`+O<=8R}vHKjh+QLjn4QJeVnmLSL9n?nbTre7ScAA%CsBqy-s@FSV4$%YhT|ZIMl1TsNv(}recxQI=ybJBPKzIk`0xEGy?czFQ0;QVI2zqy<A<U9&<W{u?)dO2eOz3I%RM_3e8-QvQPxfi_g~f9fZVDSd$d=f?VAQE=}5vvm8SuxTGxg?2)%rhp6oHb5LOE^nQGv&k^)(12Y#huiez;r9W8BxuYXKM!AgLe1-UK>MPsm0l-cx{wLIHA@D2MAp!GSFWkHNVU=4~ZSR#S!YuTfw(oxU9+<Dhv-0lX`BKqg8K88>Aps<xnP(EhEAr`JzoF4Q8rOXUG*znHQPy0ti(iOJ@qhHNe*0IU2b6XQ?|ZhS?iBbY(gw?k;x-~KW)FzMJpdIIteVViO!xvGH?16^TbfKkiQdLlE`yF*MS0QiqAT+-Rm8wOfozLtMd~w1g(8^-;ecnpZqLAq#qE*%ZRm6Apkh_BYuIW&5|`a-k9TCyK2epvIbcg914CdF)>X>Gq}bmads>fdH&#!qzci}amPTb`{5bjvncjM4&&sy5>)bj821AB0(!%q&Mh1DCQuf#k!o30dOE0s4c*>o|G5Up_bFun@d1VbxRwIPJxH+=yq6ph^F56h;`g3yFZTOV}RFAiSD+p?yzy89-A@kVWX-~GlM2!Jp)iJ|_Yzo$3hDtBnTnF1XcYic^Wbe+qiGWw&t`W)IxY*@=;lQVQ!cl$Gs@O0SSa9w_AA>4A3otMN5luLqHfc#6>L^twu%M^S2u4}Xkk==&oI9&Wi76R<Gu3r2r5ROg$<SvOLMo0@9-GJEM|1^t`c{a&sI5@Y2?UYu@v)oGHg%g25s^KRQcN-{N<4j`$iz6AH%V!j^P-?d5m|WVn6#mWIFsT5&Xo6Z+aO)416fD8K*YMVedwA9Y-a52S}T@lXoo?qaZ}%gGQ=6Fm%~4Wgd5w%&DZ_g_qgs0YF}Dq?}PoSE<!qhaDfs2gCZ4Tc2M~}Uj-Pp=&XbT`$E4;QWjxN*sc2*_dw`k40IjrC~q9)jM|%t)^0Jf^*XR6flYD{!*%(*9H30PXZTFthp=UU^@T}Ss#bEE+1?jAPa#cHl&50eE~^}qhaDv*H8ninSf9~({TAlBH?O_#<t!G(A6YL<MPw<(qwGVHC+&O~F0VtZV*#p%QY2}W_<%B#V(0<rN=}rkNIJgnmzrd!Ij8tMGo@$?j@vbM1g#3pF=|;LcCw1nI{vFG)`aakJ9@CNe=vqb0gmUtqu2^2{#-S^u)PbMS{qEQm5JSA<{g2NZd%bs-zbAGsB88^CzHT)LUleS&-9{bGR13MzfC2_ciH0xd)rfRVx+>S)m(|aA2*P5oms6WV$kt6`q!FrBPN;J58MU+Gs3xH$`$82eQ`sYC&yL<0yi#0>Isi|o#32cv{?5-VCS+nz3!s)G$bmx-u8aA0|i9a2tSSGi^0g+y3!QJ2V_(WEndrctm7!R6!vb(s%xLHbeO+4=G;~fdX-dq!VL&$JXV=-ox`G}$wNjSv!aYb3At|$q|APb&@Lb}U%FBFnL++6(-2_UpZ!<P+sOO)(PX?`vB55iW;{H3rWGvOL)d)OLpW!e1ffS^<f&n%P(h1CTJ;~<`#Hmua&1iv@@-}Zw)U<m28|-u-=Tqm0LX<(`%1d#b{Wi_+PTDgHbO6%>YlindvMeuC@D(dL7XnkGFd{UJHWB7t$_(vN}g#@O|Hi&sp^h?Uh*hd)}?@tGsF1ovPbQrm5Nm=!~@0!@ro0r#eG4xrK~ie3kSA)uKTXyDBEjX^k~+IbXa%5r4lNjimaO7FJnTjPD;i^+}fl(8yIp_Ak9_%BO*dlj1in+fsVP(B$OJv!^xCJDRx@)3C<cdmK@cv;2OY{9%Y0nDY;Z@-h<uqRR^Jiu?_H&Sw<Gk__asGIi4MiaHg9yT)ML@hA34cQ7X@W73@+^!JQ#h6W^Q022XBMID~v;UR%u>m;zFjWu?AF3X?FeQFeYvbqA?)j#9H8kTzU$bs)3>8b9y4`dH|_50|Byhl>4rz0V-6aG?Me%xMn=*VkfgOeE2woXHzDE-Ybl82GhW>RPI{m9ZMn^JY02k~58|bKN$%zOw(gD6vi9FHHh^9q3q*!Q)E5w4hr!cd>WT<RD#!&h6?kQDkh~0CczB3t4QaDMUD|OTf^~ncN))NIAh6cuKkqy^sihpGVuMeK$^)J+deR8`<?Y0sHf>v9_($N#K<O5nasA+>}!}Mo6YI$cY_VJ-4Izu4B?!V4}|c!Oxt69U7~7OQ0Yu6dU&s504#PC#;>K_Dx9N9EvSQfe8E~iDhx9#v9uC90|L4Q$HqWF~l8_Q;B*%PeEJWiirBo)O{%nmVbDkbEnJba0w;1z94Egtg=3u?fiCKLie~Xvw0(bF3|RdLbf+^#e`2ARd5gg8U!?8__Lasq4a}j@wAo&j^xNX(nW3~Z-Y@*;bm|7%8oTdD2$uh{jj`|B9p;F`+jFg4G+qxiq4n@Rs^OZHIc_J#5U+qe;hiO;b{uhVB_M|a1LBcWa!6}-Gi=zJX8&kNGdmne$qJsG;<rS`{rkQ4v>5E^-HdDgLQ=fYJ`#$g2+4AFzWY#4;NMM00{3@w5TB2X{RBJ0u=3es>9IeHXdhq>*W{g@${k1>o^=-p5Zx;?a(E~8=@jWwQ#O?81&rM-yGRlXnM+B+o4y*Wm)x$uf)I#x5BNx4|0&Ju6a!YxzG<$9Qo4<F3<KJ6};yR#4ZWQ-hT-sYH8krJ)*;`3Moa709I>F5Qd39IPVvM-L-=790<Qf7kxA%Y-#9eR5av=LhBmZ(tSwirMDKf{Z=A{^PG(RFv{XAj9n7!3x^9;A$n(e>pZ%;u6x`kqx7JgOp+$cuPbh`bcWo`D-f*5m6XF6J_5VeBqq5)nrsJD^D}+1?pIA1i4Zg8wP?N959WMd){<7w&+wE`oUsOP!4grvO}6&?Ud*!SSsHdv6VN=O7cl>j)kLL(W$7E%V<?f)eZdOZL(y^Fx)c13$|Qhk7hqBdSPZz4FUO2%E>5sv;uv3l-_oZP$7(x?+y7z{7MC}!E#1J$Dbh1hibLgaoj0UI|CLpY9(v^rg_yb&$gUEyAC;_`<SbZFXwo^z#UtP4)JnMVm=`$hv<Cg!k$lO>eUs*}_Y&p90qr2OPI^I33rH0BSD3~M>KZdlVV(}msi@xbGd)3tuG>vVJ_P;_Zx{1?ktc|^)G0OatIIU7EG*fwZ~NTH?jg;KCkubz4PRz=z-Zfqr?<m*v1tW7oOqG_(*AY0l|fmQg`?m*3@$2_l7?B2&p?gjapBAVSEBFs2T9*~9dSVWnTG^uA+Zy=xGDJ|{BSveHs?i@Y5hdToy_6&X$)|4B<CqCOh^sHskBC&%H>Wo@D>EO!K~9)Xitj76~!8DxwqC*nb)}r_^{Y3D|sLW6ZAD!!@lJ}iPAHKD!hA-q1-$*ijURYbO}Cx`QBe&cXwgYc4WIY)?W*=)UXYye15{F9`3%g8MT>k^Vrj2R*S=4ct(nC(>lru{XVK=cC@oCdS<fLPH}DG>A9Gr)&m8xb;7-VlR#~N8Xz$eJ0?-J+XUmGiw2F5dLGM=xmRdGWmH=L3{}OFE2sFv>N<x-_D?Vu>3A(^JVoc<%0E2;H!oA>vY{_I&%WT(T5z-@6)hLra8EVLA1`zI>Js(+gUk-O%z%M_e~K<QAaFY@%UNd2bABQk+8`VlFHMq0()z(~plSv&H>P9Ld6vfs(p3bLc3Y25ZJP_hZ^|s891{jTtwWns1}~=UY{)};jMn7>gPUc}3yImoDhC^zq*OAtx9PsyO9C4TDRcP0<6fQ=wj<hGj89s4xMOpv>s%qXTLD+6PBhJQ+ch(5>ii?hV`ntwptOMvwbg~s$;n_{W_;fzQ@U#g-euO9^@+3<Vu2QjURr6Dh?{6yy}lnwn8?H#`*Xn`ZQz#p@3__b+`P@pHpwwv?7>_l+Sg_Gdv>GQEVe56V80RsbLuy<69neM=fDO$>yBW|50JX@Xnx@P@Y?2NBm(OP9b&3o)+e@N-4=dLA&zY;#v8lgsDei3V9K!s`}H^+YptuhPPY382seOr^)!QD-DoDsBpBO4)X|Je=cNMBo>2<Ii<}8Gr=yq`7Nm~tC?}zBN^EnxD%$#RxkOI=edLp#K0l^dVJ5-vsnpVBh_(1GDh1>Yo1X~Dr8d{WG?hBYmQRPmHP~h(iWaiIeOINwSW`_|nNktRr>5Uw8F+Sr^f1r~V*wX<s;zU!+Xz9T*w{^SGZiQo83dW4;7$Bij@x+WI;}R~b?Mabs$NaT^q0uj)go@D5)}AnQLt|BoT9TAYjl$0%&<vlarrvFAwl8QohG>*cCKO9*oRLvvjL?&E&F>AONqHJBcFYr(4>2+&-p1+*^J<2t8%FH);NIPyLH&YlcFGm#N;AlfLdMR-fX;-T)S;yOe)te`RFV;EyWalnqwewv03NhAMe-i*MDAT$~%jW8Bv>$(zF>1P5`(fxK4zv(0M<w>*|122c{Wy!!!Arh-wpW&eH3iA>?lC!Vkm=w?7>I&{-P-*1t`DS;la(2kQ4SZ}W{DFD6b&0=Zj8AnlH_n2T*T*lYK!cy+yarZ9uSd;=!;@~9%+YLAgxbSUB3!qDA~?%@=Vck4O~G)3$^;S&jFY6G?dL*VUusRaxUJ?=1F&Z;wO1XrZZIBaZ10KGWDgDmWa$9wSZ`g)Wf|N8m$r%#_>%`fktjAcHQqFsM{{n`Bf;jU)S+nNvYZ<@!|Iu!{65P1|$x&vw4?dCk(;;`qp*y|I$3el~KR!Z1}a&6%*oL})-t#z_%W`AIhnDc{(NIp<@diu>l{_^qt*H3Qx;MEo&z-M?(O+RP!6Br5FzjI9V*%X2|r2ly>IiB=C|MvBk(Vd{3+?%0QmD%6E_9f5{vxuYGi{1|R$jWYp&_Djm??3$b-QT`^^XK2q3t<O#KV|mMwtKFCti^Uo&Csitz~iLbZ^U)b5_{2{GZ&a>3RN30*6q$;w_lUAwQE}Z3pi6znJDWgOZ0?yj{uHp)~{b6L-p|2)YkNJ5z!ghZ5reB7ssTKF|o_Ysj~v9SQ;f~&NgFT10O|Ru_h951j3s_76YCDWJnUZp0U)?=UTfQPXcW)u^;DroAIO&u({l;pZIZ6)xpX^PEql<tRu7|#UBFTPe1?g)2AQT>+x>gQ=2C0=xGXCn`rlOim0#7(?c`^qrYI)NgxZ{6zU61y*%emC2nFgCwtL(z7!38n`w{{A3h-H$4I5IaM^VrYA=0t@CF_ZOz9@(9l&)|iw=WQ>a{;Kr`)kAiupyUR=9aU(IU9*v+w=3UPakHttG{NEq=KG<0G#GzM0zG$vh8OmdqOQ21LHhQbxWo;TRUq0cVAHZ|)qqz<fz~laNT<sVS;`rRlSO;un*@4a*6ET;zfo@29fOVzV^Q&w0kF?q)fwP5azLRTCDkf<p=~Nx9$iEl}}qit<8>Vo)(sBYM6uPxRV<mWXX#Xk#>P<ZpkyUVqsI?Hs%*Qb{(;U@3BdQFUMP_b(^TM_T-JLqrxmm`JG4hBRM0vC=e|i+9vSZ!Z`9p|$88FhEZY@&s0PA8Vu5yGa<{UGnk1j=UtreSX)`B}6n6FRdTls=-oQ6yw=QWDnTE(GZe@FSw%mQSBuPg>7y>U|!(=O!9_0w%9hIKTXJx#loV@ey{}|dfyhwSwzV5Iw<J|=TvI6VP8n}sYLS*z<F_b&Sp<VH5fqu)&5iLieMvK$1wyC8C`0ho~PDOgU7WklBcHtuqXG^ZHw|L0O}C&_`n0R?<}hYw-<lu%V>$Hw!OgiR;i|<a{CKWmF@{IaVtZC%x%FWk^5t$usV~&?&NMwhX|8GR(jG?*4AG~8!B6~b`cSr=@;ppTId(=xU6$pY6>RoH5~h!B=&5(re+k@y9DrdsT2*qyi-ZjT>2;6V6C52ZL5cEN4rGMizew3edQgfv+XMMc-R@Dc|(>DC>)Y*s;lw<VeS2PWS3{Sr{gxTIjs;4jNe0^N|zSu?mNCyx12+zGQO_;_P$Y*b2mjDF#d1H9mBNL`<?pz>+5gV5Kh@1y}niF!c{2vPo)nv=;R{@WAWaYVVhU?_m~&B3&KdOA2Lm{xgcLn@d)9Dfx(U$su{kg0%eRq2AR_-*HO+YHI1t`QjK92BltyS?SOs!m5Vt#vPb5(f;pf+pdSJiuB2@C`f;sCejdWJIW&TgV}|Z)O}<2bzz!@Iu3#(BY!CP#=*!U5;{89q-`!#tHzD}5DF3!TY+~E{KZJ*$$qVt0@yv_0!{-b@YHUTbF+#CJDvZ`W;M21HwK>!49@k4SwnYmvlC-ph30NBB??gbyDSi;Moo&e11NI`Y!I^*ONs`+Odkkcif-AwH#dNq5GYf(hrI(CUfLw8g1w~F~Amj06$G&r&(GU-NaT6%pB|DCZbQ-A?v+ubeVHh}e5#B-aLIvf}LgTa>7Xi{9Pf2*33&!=ynQa?ZG@P;?_&rz!=hiBP7-ifd1>zHt6d|Uny_@v+kqb)z`N$|ER37SzO)FrCvSm>~1}B{f-JM~n`DlMr>X_x!LLCjUygQPSWD+Kc!}UJu`I6cY>)M9dV_E(Wwd3_*8+B9W_I!I7+B}{U7fW<j^<4^DA43tZC`>69jW!g0LMur!k-mocDRrL{_d}>uXrs0vF+e?ika$6>w9L3ERd_&-4BDxeuvivZu{g>GR%o}w&2-JKyYy<y;m}(N{TkYMSQo-AXE4-VT!6?B-DNb_lexCK%P6<9ve7Sl2JCLc7TaAy4LqW#&Ej;wHy9X%?iEC)2tq7{y&+tHUDN*KT!8C{x`@qVqbJ(44ZML6o>YX>%CS!J)d;%yGNPa+rcPszb%?V{Xaxuv69kE<qG{3Eb-W7=#Jf}{XI*Ux`EZqe{kk?mYeiwVea!E%tk}Jej4i=FAmK8rO`xcry(bGgkLAU{a!Xly|0cKfbP&6)9V+5*B&VHUv+4%*+je)+;@WlMwP5I4%?N&O?@l*V)a5)!*N%A(-6-Ea;mbIGP-M_`5mk}(RD%RXqIkvI+NkxM9&kNvQ<~#oCr~qD@?GGPC1jO@N@~}4HPw?3BBA5kL8)gTnx>cGk}B)_T!tzMQd?UM1fu{cKb5xW3Nio?h$exH>^KPksl65oY0gM4nkmhO?-g)K5{VUmd5g5TU0$y5F7=>>{0Fs*!8*+T3`5Z!F9RFUuPSfYpzA%$BDgW%#q*<vxj5U8NqLpaE?9`m)b;Lh-Z?6><@OTH2A-LA0NHnTY*Z}CJ~_4&&?g`&C67y1F|yw#QNh4-OV;1rP1L~Q{lDC<VdvJMgBv5IcVitBh8Mt6bv`<MAAbOr-{;E*uP!x=xj({KhTtUti8R020%bayD@8y63VEKq5?pQL0!Urtt+c7uC9mb{##wgb6KqD74)q8{stYki8hyu?6x4o)jC+dT;Rmr2Xet$~4}<NZB7)fEaKLxDcd(n<?4~X+cWhmFRGn-$jQQMA_t)*^T1VaId}s!YQ4s{c=K+iS3${hTo7T(TNP8ea-*-nBh5UL&7;dvE@s_*?WxmLcFiqiloj-xiR`Ub4yKHU}up?J!WDy&6{OfVOIc$p)h|GTkE;SDc4xJ)ZB4%&e_#eFlfc-0iqBI^SJ?)$~y!}{L=mtf1C3IX+EKaEaf>%^Hp!OzENDFR{rGTXk25%niuxi3_29_pMh!W$=>GJ7Fr{0VD7v{w{<sT48MLEby2|%x#mH@Uck$M8}_$m6xkcN_LxanWbg)mQab|Lb^=0-JUjr#GPSlY8UykPl&9@st-gxFXJxZ1z&>~HSvL^kj`M7H}&qc*_M_-~9<M?WFcGQ@1oF@U_!ty7RawBsYKO^*v}kOwV^W12y@=cT{&GIfZj>uGGJ-_1EcvcC*rOpFe=iUDulI=c~ww8P<*>o0PNIyvk%q)cJN$6EkgVGefOmwYP4->oWzksaPX){a7j$qdD_X<E}oEl$x60-|b~&5Z6Wn+OJH{cf$b#Pu-m%LG0Za6#80wklH36c>Vs53pbgd<P6nK&%tqq|LfkHFhP#wq57fiG<x2p(CZVS)_NNA0ybsZiV23E+IveKosR#6&PFOpH!A3c<7^;JXREI`a-#gu^j29f)oW^abig7>)iIy(3xZn@F=|J%SNeE1;skb1qN})UQ5pVtf{yGkI!1M#N#Rk^*({Fk!1<9@_!+b#x{QOMd{Ww@jB@CoEjZX%$|2Hx+oL|1^$+Dg~S}hq^9zFd-@oO(q^~K*Rznbjw5P)p%f))cra{)bdBU97$V{b(%*eI$`(P{oc7A2<y4FY{XVchM9%_@Cd}AUv5nJ=?Y@vH3h9TUx)Srvs`{Xp!;TVxnwXov)sjY9go=iV^3BKWdpV6nK`_?UO3?^P(H8rVQ%QRm3EkZxkBx;>UId+FF*-8G#H3hcTiM5w_l9k0&3WH1HF-&MqVdVME|^19h;k4c%;!is6;K+)!qpBRF*62)N7tlR7~p+FD|3*=v@rsi+*DENRO9rsAgtIAoy=FxX_Wa`D-#dWz4f71A};8K7X52=Sw=r_&*#r@&xa{jrs%Xr3)zM|R%T@7N2hUcbM}NhyG}6GV8Xmh0!fs0YI7H*r=Dm*Ft(SA9Vp;iM&$NbwiS%5tt%m5#4VO8)^xmcuFe>_Is%B5c#KGl1rq;>bbmjNa(lcz?B~(@<jb4zCzu~I<{UQ<6O@EkLQ7H!7Du_6zGyk=Br!u$7&{Ib(FxB-o+8u*2!kKgsoZxE89u8HXW;z)E9Z5Ar#^nw88KAs4Ts!!@7bPdxrg?EHy`zY&mm|L0Bj@A(=m+!T4T|w|EMBvZhkK)AbDZ(-Tmyqr{1l^05;^WJJdZ8__}~wUkSKvch=mgohH0jB80Q3a)p~%1xGEyPNGB-1g64lhu6{;3~;QIp=Tupoy(gFVHI$*rD`GidC9{*Sq}of#SGMvAB&~^f4Tdz<w%ZW*&o6~Et$1E@`x~rW+X=@QHG~$=l}oWa;B>qT^Sx89@z~^cAf}g0CcXAv3R)miBRC<pxtN)Bz*#DS6bCXh8z;a6!3N6^xbYCveyn&6Li9ST$hpwky*~mz9jg@XooYzzEgpTKK0PDM-8}~g*_BI%+cwAJ52nV#|Qelwa45-`Y51(2#y3WLn5J`itj5t-?xWi8ld**ff*P{jthAu2zKJV)?t2DIE5Cr6OuFhN5RMoP2JQ~n{_eN(l3@?t09C^QLy!3WI`S)3#79i_HA8O(dWL*eUaS=(o9GiZlkK6_kz_ShhwMGPc{<*--bl-*LlTi1If$)?y!ffE38q3KF$2Va%c@@Eg6xV&2xJ0W|Vw$(e7*xmA(nJ<@i(2R_4@r&ML$6iz4E<yfUAY3mHrj)HKv_MJk;V9quvErK5nwSx;&2t#I$+S9#3kLRp^cp~VcvnAf<;v8{J}z75*K6SLFmbse`%nGUBKIb;-M9d$}>yEW6OiVfgSEExyQ9CLh{GGw-OnmRkxIr3R=D0Z7a2=AIRl`0oHXs^!$9`hKJjthF0O1w5&q#4`_XjTc?ll>dO11Hy$nzrYFrp+t!HTm!wtD~lh*M1J1%3r1$va4~yFA6!J+dZG|9!FP*?6z)mrsY}YQ%aCGYQof_yly#XrL&`O-X9lT9!avsDU|b}oaY3ULtowSgZz35>~-3-hW|8U)53R>a_EG=4Z<L6(&i;oY=kR$ZSpOC7Mvh8DB<k!caH(@vii1-WLd+H9bKpNM=e9}R;La@*aSw?fs|yQIjtciIq0rw1O-hl58OXVdmBHd=b%G|XXvnomntOvj9dJ|IdGzwT9zkeSl$I*pq@-68uS@KmsKy#(*kO^?x#2FB}ZHXSoU1U0Atw)oO)7wxE)m;_1%t3j{WR;{i*9Z<-5FJD@SpRV@|eqN8M3sKTvU8x&Um2K_3wXc}O2xYf<S#Sx183%gvf;WM{R(;%1V*61V34hd{|KP#5<tbKO+NlIV58yp;(ME8!MqZ+!!{4M>xs2s|1&b|;ZtRd}XrL+%UD%za4cnXo74{Ha9oK&`QE{FPs1{sV>(2=;|%v{Gc%b(#A_uK3GMK^q@3fR(JX&Q-%Q=CX!PAaj8+taS<9*$15hlfNdKwgC({ah`XqS4?b8=*N<C%DaGy<IBE49#P|Y3S9VQP0(7{3t|z|B2kijJMMe5$@D_$lyMqe<e_-LbqN6~l!;X4*J#MzlZ2oLE~qxT$JTA&Z&arANEuEY9=W=XvWd(PPT~R&M)vSk_0R7baRey*R)Aw$*UCWdF<Wv+nW8pi#!?h@aGZWsd7;&RHiAz;KSsdr0R0&+oeuu4Qe;>ipx!i?H*ALhppY;&j>6V06h)yBDM0>VmQ?R#m_W@O{|IAaAo;j8EJcBtHN8%L=00f5bd@`-t=n{W5cJPn2i*Q&n-a2L#6mSe)Uee=2qd9wI2#%HLJHZoJbfXB#%3O(E-qa4;o0`iwB5Uqvv`4$1*ci44SDjpFModCKfe7DC!3*Yl*~rVxqRInI0kpW3r#~r0QSAst~M1){l?Q}A&t^~upPWFl-1&Ti_ge`k@tykr=tXa3|qdxxFU2tRa*Jj`CjZw1wmQcdce<%sCABV8u;e__(@|Smtjn1ttUUM57-Exmz9D`&yHg?atKFPI@{BqJhpQgCbiR#s}N|yObVVoOny%m{BllaR<)+M$Rm$NV(<<+pgGusWAhuTzg(YXAkq=*R9!Geruo}{W0ql64;d~B898QkgZR663~rN2K0R0Tag3Z>D<caDmvlOpbWh~QLNNyCv_ZifzYm_f=El;I12YbNq_HvqFnCn;qJBof%FJxc;D;#tA9cKZJi0#ANhdcXH$zh;&Uh#_Iz4k{jhQ5g#ry{Ck2(f^jV4j_)z8IfHkto;3wSr5{RKigdwPz;Ii*E?25iQjdBF&M{_t~l6XP+5yORLwP#>7x4lox!2R7hMkF?`dxkPsDw}aY8c$&n(?qMy|E@pFBoqx;yICGaSLF+Qj&tj8a@D*6{Li5rw;AnVBetem#$dwZ{^+-Vc!V=}oE*zpenMT*Hz$^;brbSK>e<%^oM;HLR%a{WzEz>HG{C@E)ivwVe3i8?!L)|h*_+#$5_(@6P6?r`~OT#FyQ=Zv!D~eknr>-dKDL*!I7s*NwggfW?NI2<FujP$KVDqe3&v6kq)s79l9dfh{>&7u^fh-MhHn4aJ_&1&qp0@P+Io4HXF@{VwL5wIi7R&nG%e?jRW&p=Z$47P1shbPCNA9c^Ftcv#z)O!VgSC`pl=+k$BI^M6$G|l-tUkt96Mz-n1(em)a?PeoS#>w{HD6_VCLp)w5@T+3BM_~%!wRpEQD5EW!Qv;HZ{Dxx_irCF<(e%^rj_=qI%$`!${eC$*FH0owDpDLkIr@7x5a`H9~OJt6E~N6f;74ZdO(7(;b&n844)pMrg#dxGTsnp!K6RNa(*zFSs=2RndJi~YI@$08^I`Tq&*c1Sm(Ir8Mdle>hc#B`PML<{-HFV0!ZR#2f$gFLfmW`%))T8OF|g;DPCWKV;E?P`0nBp3TA49rb~JH$LG=$Q0*C>%ycU~`eu#bicA^zgRKaFa3yF)oAbkCE_j#s{qc_c@$I*t{`h8o_yV%u9&g!i@4tTg-TeH;cCp9!NakI?X<qbW%{LY6Y1P~87xst4FGMMsyEWox(HyHk|9t)am&ZV{=sJw29gDGXrDGWAwb*Cy=a?|>`eTARSvyLB8-ODq08-x42l&H0hOy>VEA0n|KLb8^%k*pb9}Nm|@n`RS6=U!b3ES5GjvbeyZFCwHC}bXg9IdvnK^d#&-ge_~w2;U@L-?QXe#uY2|MJ^UKg{so-rxWJ@Kc_c;jucSEbK@85u0sN-ke~%aJWtocAIoSQ3$3&G+Fuw&Y`RKsmyZKg-G0-6OYlVl0R?^t(Qj7X26*UH;)+Mnzpc&D+cNq{q?E(pMU-G>(BrD=YanBm(M`f{t)^OP}wBye!e|gu+|zm!JvuozU_9Lju9gYhEE*w`CRl>RX;ix?P2R&zyX}cX>Z}o&7aoi29DH7(dT2+M{mnkI#rIH43&WO5{tkH9Yft!G6kY4`w<5#_PjT(`WjQZZDDSXi_|o$DtGIoHscb(oUPXeww4w#L*T%;gdGDQyUHxFD?koDySIJ5tvoav>g_YZKskRQv)jQN9XH*x{32L;S~>uWUG=+T8T*K@8oB^Y(>tz5wdT1cS@br_`uWdot}nhlE~_jLuay@%HgS7Kis}|7Oe{+14(b>AQ9w?cK>o;U%x;dgjb+a3xDL4<6Aem3`v`&`_k!Uys*Hk_rCj--B<g*%%-zm9_89M=`^lZu>QSR-7A3=mSe}HnJ5Fg11rw$jGJQC4(7Z-P!6<ZO(I%|~>hZ-fQXCt3C&*bxFr*8|GWwk-20!~|i$xa4jP=r(ox|sLM6r^}P{H<QlSk@Z5~3jQa-d0W+{oRyHNh`!lc7}hk9w`v{xq_b6yjl7CBXIL5Gpq)+eUpet+xg`67f2?)aI|))otonOWv<5!nea)-KaM*R@X;_dvmENM7TYbV2?}3`cV3UFh)~%x!uVscPHAa8y*v*{Pu6>(sMg)fIy{4oCb_>i&$#NB0!aDpNWh&uC$vIRaBE}l4wd98yHY(P3~Vn{ET0;y?ydNJTdF2HyC89!tsphx;7Y&%?iaI93aVi3(d!0pYsLV>b6647jdS{kW0Q>naWqd<WQKPX;eP1DhZ3zg=~#G6$~?fls`MLS>34`#38?1*F5IGP&j6B+FGnD1yX3t<#Ds8LNfj=mh5344ycA)N8YyBupuWz?8Zj>lhkqO2R%QWXbJbe(u?)7w9!jni7DqFGnj^<v(3olB0lHBv8^;z&`U~l9M(<^8;o?qA)JqKW2-tS$B-uVWOsx&5p-RT6ZyHH8iJLMk|Xp<Ns3d9bx9;LHKMSxa2{oR5t)j)U<+SsId67}fZ99xo++a?Kb?s>Ctc9hZ3-iqW?I_Htm+z^V5$YeTi{`*$UFC>rli^|rNGff?8R+hY++lNMm&x#_)~lVQ-f#+<}`%vDMp9#@-+)8Mzqs7KGki^pV6+h%&9)Ql~-0SqAfm`r%J#xUqAVnM40o^T5xpbqEr}dQP#(>OH^`bVu=vnVDk<(07u6<yYS_lL5|oA^%j$FN&n^^Y#yY|ZXUs2-X(%*y{?OH8rLM3VR6h7%3Kg&c^>x8gXBrk@dfXh#q|;pJTT~o^OJB2#t=MC!cL25x1+Q%g*~kkLyDK&;}(@v$xx*f%R@&AUD#=iX?=Jtn&z%R%xs)?wZb?}lj^^sHyAOi0Fz~<9~+nbx#gZ!@C6eEmjoys36^OpeJBjHrZLWfAsN%5!Bn5covRL8?0bTRjlwIROD{T}ViPrAyfu&e(axTj@j8aFJ$w8@4J(YllZAZwD(+9hTVoj*Rnyn5?L5e3Wwe~&!&qJ=Eatk4IP1J1i1U+GDH1U0X_k?2I_JB#bnfk#J0WtEjKRU9W>%^b7ROMGgu<Ok>wv-4eD6FpY(XwmKpHnO<Q&4*8r^b+EsCDFPEBeQvd^I~PK@#93{X5ttA#uF(aNpeNSO!Bq++<d&CW4F<m(?iM!Ksb?G3nvJKbn{zpQZI5l@#f-F&2c!QTgPxPq9Of@!yNE|bimC@~bqT=qO|pu<zmbA2AyGIvNzieVw?W*3~vB5>u2W8+`ZD9G-I;0xUsS7&6Bd|A(bmx<DSY1FAK8CBiL4UfsyC^!HS+4GfNW$!rhoj4?i#_)=q)KoSM-nsFlEYYC(@EBzd(^JJzp8JrZ)ekY&Y=F!)4C6t&d}g!w+-@_dgFFNDiCk66g7@KQ1LYec?r?JKc%5Q3+`%dcBcQ>9N++K!i2m&Bz;``Zf@4CVd;)-jeY{J141N>+0&B6-5~Y`Yb@q?9%}q5Avh+L?Fh$lehp_BXhgF-ekjxS;^wuJmBuW2$Sl98&s|j-zU+mZd*V-p+@}Xd@c%EGq)Hw#a5a{angYGpIMPwUqq6oUZixPQd2y4CX#2WZ~j1qv&)Baw<7ql>7biv4N+G34jzk|glWE3tFfLIDLQJ&j)ozt09s8QXK=1i?eNZ_URiKBB8$akkDqRq#O<sjK<E`<Fj1jh49B}>$;z;0(i?J5h4e{RZ^jvownit}J?24A|b?B8tS$x4}dHNJ*~L+Vc9Fv;81`^&d)E|A!J&Dg(#k(azYc;woS9%qX$az<FB=AI1KQhW9FstO%>MZPX%jnin@re*1D+fl%<v`0fJSoP6Axz(&?Ro@6}JyG#3z=R7>XK<}H6+eTh9q~X|@hSEm6Xn8&hJ>~<^=M%$&Jpt8c@|DSZRb30lU)a0w~PWz87W+XOsRuY?A*78<RsY%7xBPphy+$mIz~Ck5NcX01Q&<*fAFbh);UDhc3+Ekl`}FlRvN>^F`*)7YBO!<tV4*mhGZ?)T2(o5@;30wDXkRAM(7ysBJ;&jJdXT^NwxOOdar$`9F>a>qy~6}8=ZE~{%q=535shS>X5V~-;eKU_*B4ovd5mCY!*x<o_5#XY!PpmJ^lo|#ng#t9TC6?j`5A^5$V;L6-TIOp?U)AQ_RO=|2&p@2oHGNkNGaEL`~Z)lPm%QKwwS*NXGT51!cBrE9#K}<{RV$kW-^$;WB#MXEc9Kq{_C$=0`wsE%FjzN-SiNpBicyn{kP_=?q~F=vtzFfZlZzGRcHP%(V!Gav5NVloRuNu0U=K+P(_4v_(+hNXJG@^=N<?oV-|pbkS|}d(@wK?Sxp&l|V8Xj8h-lbgssJe)KWos4Wu{!CbNha{~6@*R5lv$!VYZnucw~TgH3Zfd666?QSaT9jcMp3=qX;U&k=Zz`SEPrLUnlbQ?6u<#>EGIG(hzgJuu>fq`KxUwrVynAsoT+M_`O)(88B_`CjSw$6TzDB2=8cNWelL*C^+BcxkP(q<&%V1_XdL%w@L&nHptdA}K89>%@~3K|;NZMwTOV02Q0z)jre{~d##Ium$e7mpN3`x`x{X+uyr`A(H4%}l^JO8&rw#{cJE{+g)CCOL8Ep+0>YfukP}P)R(^4INB}=|h1pO^DMP5L?GpZWu!&v4O1;o-=3fn(&&3?Wv>b$E_ma>@kYH@3etxWE24sAt%{Kp2y+Y1DFVdwMT6nWjTl*1`LJmWge%_*cV-(ilGntYh&SgoRf?gHK^^2j2ICNqA9Vu!!K#o9+ar_zi<O%Rj6bhYmeIu+yc!z3|m#_hPy@Y31t?LR<xr?*dOXDix|R(>^Vq4oMN6E9u`K2NGtukuI6JE!HD*J@DCnbOx0*zgb=|pH{>h${Ok4XR&5SNXODvq53>VxoTsr1&mn)V<Q57?aGG>YT2`uKrA4=&9t>yB(--4-0`ybp?flBZb@s+{U@NLKzpK6ALNGP;aaU@^*8~BF(wcsf>l`DGXjUkXi5sSeN0u~u9|K!ev~>@i1j`w+RXoO)WL?qIGj<R<XMwP$5&oV-te#6@CJyJ(*)h+9dN@g)hw!|=5lKJ0dh@8BNOV=C3?>8r&}F-ntLJ%o#rcF3RpinE2Q<uI&+{xx<B0vgp{eS5oD3JqX+P&8j~^Cs0Iwh6)rgz;=Z3%KNUa7P@V%AiyuQ^LfXxn9rN;ys)us0@s!PxF+7pYT#uG(YV~T?kmuce|@20YUaN>8^8~wp6L}9DaJa-a)ff_7`#E?%741jQpii}}{#clxbe0R0+9_FO-1fZ;L89V9x@EHt3rk-S?RB|dUE#>j|<5wX;RKrqFU`Qcji%_+EsMS~J&@z%5dsb*d{o+P7ye=&JKuX25oPtQu2}a@=S5>yU6KvdlZo`x$m`I5Drl3z=%R|MOP+4X!YhN5q5DdhF<zsZ?k+Qw?U`on@bUgbP9LTUyJObKyEI`5n*P-KJQUEUHgC~)V8%sAlD5T$yMpZCJO5=UcMX8f~D0KpAk|E{AR-tS<4u_qu^ApE6Lv7HL2M}_9wRA9}(LN05oG}7Vy3Xe^R~f;M7J_-J%AFGGu60oha73dfNCXqy0vOOLw?ripPjV{Qqw@~p)|<0+CRG|j4jop+A4g5RvjGMOPG8;S+Pjz$$WUd*QOjts)aU(bcsAM>AtX>4zbX~b@@$}-MNQP{1ME6PPYVQ=6F(mA?0Tp+;Tp_=pUY_RB+%x(%yNa7^2dnV0|%@OQxCjgGKMiHc|h<Im>i9w;c{lqoZa$Fyr$PNLI(vOo9i-6`sA+#u_Y19J*MkF*CHqBAWcMUTD$I+Or!x05O7y`Qa!jVdO>p8q(kP{$=Ibq;|(d)!M)x)6G9(y_a!C{X<LX+yshs&*}<=aOz{4h0!W>12~H8Mkf<enq8}6N7z|;fDPK~L7_9h|I?{|$mT4#`64!ElX6?;+J}&Cxsfo^cK&~5?Pr<qux!fJIC(FTxsP{rr;H&h`BEehAe8$PGb$CHSvSB?>)ACgOM`%5`DrBN|enubb+8O3iIEU7Y@S&=x&g+&vBG1Rw@P<Bq^Rtadu!(y|u1A9lv!X=UEqfbXNMQlfjlic+RXY5O91%gx+n6p@0>k9<BzuJisq}y8ft|OhuT@@0FT>{qZ34Qjaj(UFBC{$v!jdLYTS&Jg34Gb_V=qsoSH6k>VBTcmp)5~wkY{mn7&Im5PGV6ffj(7+iB#`?@>;&cqlA+J!(&$9_}k}`*)U*$GzU{CNz@~VCPZAt-?j{4Hz_m1yqu*?Nl>)S+upH)x+-e#i!ZIN6UXmDhXFUoZq0^3V>3im^B$ERgU4O!*?9QkF&qjp1r6nerw`$}{SiYBYgbY#>R`mNBzceMX`+WHoo$2X_>rG@J5O^)8p%tSM5vA^@$#YZya0`~xuMgbdxON`4U7E48WqPyqi8&mj=28qWBdXIGRvFj`8ZG_bkO7A2CN<GQ~IHOjb<>h-S^WjJe3?)Z<B4FHTQDpV($JT4LR?7tiSC-RES+?hL#?4KgKLW6k|GhDD_AuPKzfDB{b`oK~@{g=YY9lnT|s73UsBR3SoP|c^VYXh%ki$#)td%9xY^};DQFnc%hj(l+dXX8t_vdstl!LsYQ>3wE4y0lrn@m=r~XOg6vt?n5q-Hl!kx=)$b*yBywMAV*)`fANY<!*?Y=)P}a;-FG>%KSeN#%so?uEYzd)_e_!`X8TOv;6^5y|{VYw(&J)BEmz7-}G7h)2OL3<ea-ZbzGXdpd4Cc1Ca~#!-vY>RH5V8eT&lu>qp3B+;g|+WUATdPzE>#Npd}PMCo7RAKJ5mOr&ISc_Zl{SEi=HFWGe11tpD1++K;`?f63AC<hR+Ki9={Gk2<ifXJG-bdFT57Zc)n@)5$0UVxOO&uffGU`(_Z8DDD<?a7cg##gbP%!ZBrHxu$k*I>0rT6mFWyV>y05<O3W1l4QqI5>ETntS$p~<78zFgMuvoeKY&4Y-rH&H>wgL;b{^LWo0=yzlVYN`GEFH5*~P1dVQY$ygha6o`wY*si^mis`vM4JR7fu|^-PozB=9Gj8S6kam8tepo3dK?hoV*KD_MYHrj+f)eo|SSG%k3ASMBsCr&X3TM!A_Kf_tziBWM5&GcU_IhfPLC(iT7(@&j9~DBm0-+~X|QAVXTzHng~68z;Ap&bu-Xo%hlbep)V2#8f30_be@@<8aL#T%BU3<&F!B7NH>+u_tAoUM6JmWhs~WIr7d#QxMA8xk(wh{bMtEm)&%PY{D``0t4*Td9)p-HGxdOCo?lgN&_5w;5HLYDyct<5NVp`%nZ!Sm(xAj0VY@9^%dqdS8Gi4DbvbaK!ZaP!N<5aJslIZE&(8kR04}z(8?Ui8$_}?JpvY2*Ej0&BauTH@|0_^SW3DPIWRYNcFXwM+b0XHbN2?Xx=Ju~^$p4-lbnV1{s5uth1G%ryxJ>N%AB|pG=7$wLMS#MiCZhB<f$>QSyEpdm6s{Sx+=|Mm-<@rOv-!B2uh>7BGg>VqSFzl+KM>*&4Ut>$Bj7>_1u|NrQ77-9}3+~+yw7Y*!qMSI7KkklmPSKDgRI}q?G-&&j!<WqMF`3FY6kiDwkY!v_sHf>Anpz|6pm@hM4q8;41R{=Q%A9BfBQ1p(7$<C^YA*JxM0+YLP~ei&W1^otCCyD(X=3@dt=#bxbNnG)y8&^<FTqrL!D|x`T|4jel$~qfE;r8zVnUtxqVn$U>(%jh9<i2;7Y2zdspNW%k&HL`KgDF|dx<Ohhu_H_4lZr^lV`mX8y7#}fMmLpfthD=851{SNH;S=e+C`ytjAoK&(Y%a9+fO?}hRc9vO^1h!=v<HEPYLlLCI)z0@+W<}sjdJeDe16vq{oIhRx8wK1$9yl_$LSm8w<18U>4L$`x$${!UJV`3&IrdA{&jmvN=p=H<iar?Xk~k7rPlaU$!b6+yXS!RxRmW`0_#T!Q(J<*@sdL#B=-VZ_ClMawUVjRyr7Ls3d3_<vF84yA=Bos1EpE0`F0TW&S%<_G`JBkTlBqU}2xl+c4J%K7CUDm=Wm6NOFJ(Q^<$g-Tk;IM*%+881vxqiATl5PtXj#L)R|;0j0MVQ(M+EqbK$qhgmp6<_5Gw*vO^yt)Lb>}!33I_oNwl&uaVM2^J%bot7a1>P!!|}xW-VA3T(}`OLP?YjNBdHPETz5*X{CIm3h2l#4Fi(Zx%o^afLTsSaQq9{Tf&*0zD+}oM95{VAP=4Nf`9b#QaWiE0d4l?l@&Iw;`JZP&1|EbKZ-&~o|u6di{+_Ksl#r2Sn>s9c*w$hU-!TN<J-^w`pX{%J#;MBB+I^1s*6B<4ImF<aiZEoYkQyAEKf|>N$^}a%fVnaRH6toewVGt^Z4-nr{Jm9d&%34w6D=t6LolJ5yL=1BLUO&8-(!GAvG@zF_bOiXvBbV{{hU`i0nZuJ9@&28?vXUbfc1(M^uF%h$p#AFE^ubKs}^#abyXy%Ur`FRqk{zOO%xk$sW-SPn1;sNY4(oA%D{NtfD)}Wi_ZSGT#d@{xB6yOcTcn=m07A_Ji?GfhARuKF;A+bV>Bi6Yq#O1X3J{%kq1Sf;=lz%T9SonL;lyDp5Hz{|LP1+9|J@zAW}?Qiegm(4ffg9AjK$4ri&Q)idfc6Nf-3vakKtBbK8UFjOud9T@8-^YH356t9EFW!z@);1=JfcjfH6tY{LHQr<<Y$nv?oMbzv}9YXCk?sfD4x9#Zzm&!Z$br?J3#YNdv+ZL55lsSjLw)9T`?Sf8niQXS)Xg)u-ijq-pKymT{M>J9gnZGzPHA?d6EsYuiTU9#2K4=x@Gvo19nWkgR(fi7=FPzxLhrx6wl^%tN`NS64-IUse7zvr{ZGbbfs!+*nra!>f#v|*5EF--b-tnTd1IH@ZwPBCS(CMV8DY9zL!qCSd<Ad?!kkZcNBXP85z5_v8$5FjnoQ9gC*qL+bw`0{&#v(JRfsoNBadacVMIAel#+f_i#T1%0jCf3L+%eO6OnQOFBL4%0D13COrw-@PqpWYt0M5ywfUR^@-(wxMI!2jW44?P1l^h0=vZhLp@O>7!v@PxBk*<MLTgD4;>X-#qh!upZ#2CfHWqLU@Evl4A(vNdCpX1-<=!y2}vaUUZ6;Lo=7r;xMhN!haXyhSnxp`a*al0B4D0_8n-c$K}MYiXIDi^qJOT+CHT~oZ!ywQzgMIRt+=beo8lIk?;eULDuUJ@@7pkAO8{xOj_W?s(IT@qEvEb}?Nisy=lPR$fiR`5M0A1$Xrb<(OjE!`DEy+Erq`tlNze=Aoxkr?JiqLKtpsQ8P#{ns}`)k$xxfqiXS_tQ%-H5q`+82$5Y_VXb7y$@MIlp)e^>L0$hEO+J%ZXOYTe;1cxl<gO3o)UY*aPo%Q6MMbp+`CM}rxdMX2k^%8hUPiPv;*R(K%|v>s9|S+or~Vpkq}V9D@$u8LWXIsPx%QTAVgo$WA8l%^P>8_jDA>Y!cQxmgTeL#iogk#@nD=iM-#fZg+=wWYKiXGXAiH|c<P>y3@H>ii>i-HT~4=*7?M7L(@V<cYBcmTf%St(0Zb$%iK2o6xz6&;%G9ipQ%k>00Qr5UWE$Qm+8Gnv$9F~VS>vu|8+MVCs(nOJASdG{!x#X``YQgFDKfg02ZZlJ-A=_5fMM3>Z-8Fl((y9(r3PbP@)9E^s!p^?#rQTb##QCqWJL;$(P37EbSE(`m1EGGj*KQcn^6ZnIPLAr2FA8`BK(*Gr|xph=-)8x3aN6Z2cp)Hz!;|OW{20Pi`6W~!l+adwd!QX;8Q~^x(sizC#p^_#Ie*b!m%7f?IJQ}%<W3%ULRh}6X6qM+1@Nj#+?0m!WRWvs%ovO;()ZOsy8C3;KFOQ^oeTpws|pzTsJPSYe$~#<5DaL)xLE%+#lxF16HC9F>*sz#7yj0OyH^5zk-iZ=d?YyEU!FJm*E9^VWj^6nV@7#ljln>V@J22srLj_B8fajQc=4ulS(!U85HxHO}f~;zvi<_yc>bbsBFj<B5>lY+EQLYFDglZGF*_r$ppq;bBStBhX~$KCoTv~xsv@ki^xm#QnG~P{c^?`DHb)rdXfT5xe)o(hHB|HIDSvn5%MU&H=f|gY%Q_H<wH4Rywt}bX7j_2rrHoAf!HKr%A|&ksCFLWXc`hE22Bc<DL&EEI}=VqLv`dI*C=5Snegb}y_`bBbfg?r{87NGhO1AqGfeU5813A7S{bsKQ9}h>YXWX_unFDMEI0f{w(mu6ZBYpmM4A||@>T88c?BhJHwnxMG`%lzK!NlhL!Y$VM-G(-)OMpmzeKV-xjj3=9}`P4H@F6#{MLBepG90WVbWU6xLe4teQ5lSC&Y9OA4%Zgft<p_7nnXo3G?NS)4J(oyx}9ycqa4oCvF~M8<mq0&_MJlU<VRRd8U#Zfa}alY+-k&0{rkv5uQc6Y;%Iq0~`Xz0vynOu)$#ho4OU{oXBxGZ~LW!&Sc%eB3Jzou!tac#65zC9Q4cc47R8g34j`bz)v8>a+TrR<C>{=h}N93A%$tE6&U)tdM$O^^n(-H@|YBi^+x2#Yih$36sYft9|N0o!V0BF5JEl4vpTX5eHJI^^3@U&96`?<gA0Ff-N(c+@-yS$B6|l2oHdo&`9a?SX0`T^q*um>unts~RmrKpJ#@5VgwH;w{Nlb&>km2C$P6+IdC#PJ!$?F=o2c;|w9K7GA;wbdHDi|Gfj_=wU^VPYv*aG>Xli(eFg1u*zJbn-roiL^XV}U{A~WH+)7iYVR69LBU;;V`5h5lLL=;op11`*NkC=HGM&wD-7rKJWzyr^?mTQfEOOo>EF#hrFkE1#TzCS*bomm?0AbW-%ZZt}f2+BfEUPdGJOwVW1TNxNlCxLsUFf2Lh(qnC=b276&8P=XdBtR&==7(5zTZW=@X6es1p{0tYU};B^s&}#sLP=E3M|5UuC^4EBe=iMH(D~3DMkC6`L~*H#c#7qmmWDity+JlavjMlPcN&+pmWDluDjo!}n{}-j(Gn}2gJJHn_<_x|+z&*bTE{s*uK#j=h<xqFL0@^!0Q9a`K*5rDX>9MrG%P|Pf`W7N_-T}fA;#SVV3<)n2|g!%z|jRvK&$;Vo_qO5=$Qw|agn;5T+OklfqRe=q@XO;izZ#ct8m0J3XdMck&4RTL7%IC0G5PVKL4_fm%Fg?Pr>o7lw(Un4HO#-9z#ByY77erNU(^?6tDVtVaYMeE%IUM1TGn<HW&V(br<`MEM#K43CxN!)A^j~9*X>|(HkcD2@DGu?A~pp)1cGF_#LE?vHu8F3&F_7r(LcPv}1CbkFROMU(l(trlY*ROkrcDUtS6CH~7Jje@OAvj-k)J;Lw0$1%5LijdzdFSF+Wf_kDNmz$@@F%T!gLA!OYUWvIoh1z;8LP1+nYm0LR*862&`+w0`>+Dv+UGOg;!HFO;loB<;j+nw&C-PHEfgr}~Pw9%<J6yZz5StL=_L|Ka*w{1p!=r-ntX{d*+2IZ1yfEzH5DTV809(Cnp&Umjv{uwMnU+zgg);SHU@MMQXx^5-`to<yroYJesn47?GghT=uYw0}SjP`~V-ss#(*xgVBvBI1xh`{mnBvSxJw{)?<=s6iZPz(Smahf?vB1DfJSGr-RL(^_PMx03MGN^47X3*|4c6K9<ARgf|^lE^Z_X8t4%8)Clv*}C5Gif}+VBljX(JKoUKh%~(KmEx1S76Ge0dJiVW<&kM>bdB?0sp#r*dB5)<0QJ>s+8(EnR70)%y%pitFbL)eSxm^OVIyB?@Z)#JlUSLBq@Nj<Ev|Si8Sm=tLI~4?lB}S=c!r3gyTKSKneIYc7Aks1pB!@LzIG`i()#ZeHOsbq6esnn_Y<r`(xl+s5D7icnsEz7?%}wq&dv0j~qSkfBoz6u|B8j#HF5=rK(_Y>g|Y<n{Aeu+@H<4Khu5Wi{1l7y?5GX;yNlZxOZ8{&gMv-uMXQ${i`TY`VNDsC^X-^mrlNa`<N-GEn1?4=Hmv>U)15Ztg}qhonVWWh1#V$)ihwBU4+Ry_XNST`~@lUf}C|pgRT9L8jl6T`yHf}5oy0I&Y5IsyEiTLQs@wo8`2VPP_jF10(*LzlPytn3bH`aOo7oylyy?tuIaN2D>4DWKk$4&G$3X=tW7&#mwoQxnufgeM=<i^wLVQLFwtO!T==`S(jY=1hTFIi$GnT4WQ8Hu?URec{0F|c{GziqB*TrTdTAQojnlO6CnR(a8vvoFde`c-o~`}j{=@K3$rj>L*jkM#T-!-DO9BE}^720}>#<U++`O!)E+kq1TAMhxv)!_~43k-#nfuDCg0jt!g#>i@&~iW66`yp$deD!)06tE)DUO3$)n&y?HktcnxPOu8HZFWhp0DuZfRuBJ4Fk+=7*RV{L<+_jU14^faI)U!TKQbhn^3L0ZfDNVb%?X<!G6<JitKv{I5p>yyITD}zWw&oAK%OmKi+|Td%XX@z5n{{cl=Z;G16gd{YUB3u&!gq)u0}=%&(gO7548y^KD@Z+Liq`?m_8fa@LsVKS-57S7OlPiT^u$Q{`HLeO%leN$a?_E5j<)ET!kHFy4;;?sd-zv)z~6I>6S~vp*bi1Dmh@uP^@^_$egfc*IovINjIL*k52*h<GY^lK(B1C$-vJKb@LgGV(Jy_B6Nnh!aI`J`(BAzrTF{(_;xD{8u-;I@!muY<&&?8Ni&$MvZlddx{=v$BV}^9wG#EM#5s_)W=Q!{x3iM{>yJa{n+YnA7RPo-s<q{Prv_su67+&#@U=d!hHIBhWGoZ#q4gV4mj4ZE9~;II5tBPM_1$7Gu$hC$XG+i{(t`U%dbEG@1LLi$G;rW5okl~ubrp1x%SZ<=5wS)wSJ#=%zomv;^gI$HTz<jAMg7g5?`Jk-Ld_&R(}7MUDM_}z?MWs2Sz<epbHO=Uy%8|&}WTxht1TNKSvLr7>%=Q@A7wEUUa;}=e=pT-|f0m%>oLDfM?Jd<;>6Fk|5KG)CvgGH4E<cb0|xECD6$t(gcu>#QZq=yY`+eYtKpr{Wvj(a$LCR@sw(_dCJ#WcC`_s9poy2PQ<p(&jRBmJAU;o&eOe4X%azQ3yx~t+I?IjfSvOekp`CNH<;H3K>p)e<UWw+^F3br56sCLI^r|>DdKUha`A@`2s$?HJE<?bUXyx+S6<wMPmiYc8}lCFF{)ip=t7{O&62c3bGW|7mSI?9c%#W=+obPV`|NvvuGbbe_RuqRvuWVvq6k105p^E5O-B!LqA_$NK?b06DT_=&reP~Si0G3$#A7T~#^e|mqj6Ly@Ktj{wnc65Z$6vqYLKmtnC$P%w8~qShxodAkS)<)0<IQg?}}u##%<3Z4E8M!&Gc8kVUQ(K8=9jmK|9!{WY}QUuUyt@@bS}=EP<~DY>xY!f87<N;pBcZq9hvkNVo~08i?TYNl&Nq&9OB6<YuH6<Lv+QZ}0Da7gCAGw4+*t<pDw9|8vQ2A5L7v7CJ5`vUWY>i&M8zI>aVAKPSe!v*9KkbC?>kPU;TXq$@apDVl99#d#m=sLJ$7sn<Ih&3zqt!x{HLrlIx-%!fV*rT>sZ+Nq%vwDIC&o)wOUfc<?ag6i!~LzJ+vrN*EG0sk|pE$S)ZX&idml<>kL&}y&+-g`ccA!0kp1ML4J`0yz>VvH*ptOBAY33Z>&^VDFRK+#54*Cr-{jqDglRg3CkN0YWAEL|`)IE$y!l+$ZnuxVWLU3O}(oPB5gUzma6Z+#i9emG47<Ub4bh=u+Mn{X6moL=w}PjbSRxh;-_vO&AQ%z>En=IKl0DorfvwQAA5yq}#!&mjzqY0}x}5qWB%-@NN`%xTv<KA0Jf{Y_G<nKI-)jF1o%A=>sJ@ZqzX8{+B=;Rb__a~01CcN@DybD}ayOQ|aRt)Gyd=0(l1Xvrm7-KAKYt3xucnZ6&YoCdL`t?>-^bU6pMMHz;c$~fdeGmb3EhkG8=yyulpG%bsaGh4<q2cHDK{?H`va9`2gqW<;Uw|~Be$&~ZS3%O6y1aL~ytLjKOC&S{sF!h|*{O_0-5fOFcu##%rN=wJ2xL%v_gTXEtTqL$q7-f>^vTdF$Fv?BE6LPL8^shv<98AoPtzr-V01hvBnD(cFIiO#lf5gT#D&pYybCcJ|Rl~bkN5R7}L-)mx-lAV%7nVc)*$Ry3^IZj+Ut0dX|KrVeho$%rHT1JN{&RiU#1=sNaLja(Wix^fav#2hUT!-f4&<cAZy8jiB=GHl!@#Fy{cUs0k6mY;B8UG?%cvGHEzAXW!TUQAfT)@;#Omi1qAbCA5hUfA#|QEwn8R~wz?FeayfG4Qgep6m0&5tO81REhOUQxV1M5pFZTE@zcihuaY#RUtmDB7lOQO7{Xp=EHFd?-lRn^|YI#B}@wW)H7fFOyr&&MU!SiAz~pPbpbVQZu~e-B>4y|vVY2IJvkW!hpCRcCv9V((V{eazBBhZUmsns;nkla^?Ci~<NhQOt68hL!50{f&(nnOdmgDbk+lG)>^|>6hy^>TO7Eh;??uYI2xl1HOUp`$P>6&8BQoE+VB~Lg8A-z2+K@zVFh2F<DkIr|?ZK6eK9}{!N}pmm)LQETfqW^9w?M$+T@xwv68BioSr<Z)z}nIJKiRkpclDqOoN?);*Lrv=5AMxkQ@?H`6_K^U%voX}dm<M`Tje%m5!F(g~sMI@(bYz$S%&AA^~r<&pPN6C8{mC}$r_WWIypA?n@Wd8Jxy^1y4~y9013T!uhPcEs39nhcnSMOKHkX$|teONJht-!%$ZfwOB*f*mTz(RxYudC>j6=x~B?TEXcEPuo01SoE-_Cf}ftuY;Vw!(W@n>DiZfdF=x{kC8HrPl+87jk-;db0V<hIQ3%=tNeC@XNVzNqa*I*zvhOHgaEEV#+K3Vh0jzrO?8ZSr-`9CMJK1TVpAO|F%&v&_>_QMBd5nYm-pO?wYKr$<>}{nO5kNkLWgzJ(7dxfveT5%3j!(OC&`x?r0y7C?Z^~y^&WN2l1EXO45RehJd$CUEbq0PYe%n|`c=2q_B=1L^@(sD&p(KB1ev88Xb31vsB+=Yb9s`-mvDVbJYsIJO0n1~LE;F?HVPNn0i&8j<)_cYH<ZRB+AG$5Q>^(hthuK({1bocc$Up6C?1XWvz(F#P4Y39DocPtremhZ2zpsk)y=s<(J;Y6k}HVpx==^3)~e*h=)ei2{25X9HD8f@V8`|syg`^~B2$mM`>1`HAcLfSfnEGso`L$h<7LSm^rOmSTUS{gGQz4tl{EZIg3iD(yjHIFbCw=+gPV58G#z0Ar@5zKxA#{yR41U&dM}{=CPRbUqG+tu&t~KeOZW@@pk-8ZllJMiEyF%!SxMjRq9(v~4e%y(pm$wLlABRQ0_nGZVdB&ek7ct+YPa;f^r7f@>pbfN;nVjMMD}Jk03oUI_}zt-GRIUHOAVerP;xivU{;&TFni1m+ghIKvse8TqMTv-91l=V$AUNg&dVmpSzYo%KIo-I8mc~NtCDshftY*9SFWywQ<Nt&&sRLoMD#l6)nHih&|$1zqI&zo3J6i*S~}%LL7I<Jj^qh~V7h+|v4<p@3a>Y<<cV|<SD&x}V+D;CdY9~nA3TD7A1_U`MwuDCf%L3!UoW5pYxG``ZRk*g2b*;r5~x?O>y%7XHt-d&-|*0U3YUIG0<Ps9qaf9!iffpA<KOfu8uqtDx!8-&Syln-zKeUxD#CXjh2|7eBRCO_duFeU0{+ne81}ITgEtR$*pK9x$$iYUc*UV-nwB6^vyzhld&KJj?hP1t;FLi?RJ26>wY7ciNM&^@Zc>%>cUhjkc>P0j!-y4KZkQ=zTSqCl4O{$G37t>vif4agd_{AEz5^0weqM>`HF;S)_B*YD1lhO4FD=8U%I;~nREC41e<7pAX!f#kVS%XmG22<m9HJw$P*#b!1rB++Qcd0r!nGb{C^8m|0~t8&rfmIlE?sGmdG;t`3!x^Rt$;N0V1w6ZKgTMQOOWdiv<Ndf=&M~o`ffNkU0Qsc;y9yh=IcD?60^P`QUR7lvxRMwZdJ6?<8-zWy<AKNx482jqf|9;28oV%+{<=bIPg~ij{6wmq-N6@dx~QV{j6Q<m4JZ>Ipl-~YfHh@U5^T&LX*RK9)ge{8oHj08d$Q9ep~_;d+k$drFCk1lA*sX1Z+G8x@x-NNA&Po%Opg0^sLaN9P1@uL@>wL#=cF6dZxUzu2{NPXtqj2x5kjJ^z?#gg|0ZcF{)!Sm1yXUXA3w}-pg%M08*RRG0Gk0_}jA&T@#IZ5;(i0BZlRgFM~QFsWOi;mui-?G=woZVu^kZv7CdRo}<wGV!vvRvLt|)#NzM}2aQ-yRetUfYZ&`mgPdb**P`T!gP7>NbstGTKA*n5&GRB}97W<<%S2l<8HD{9*cLe}QFKP3^I-|tEt68|sblPWB5TW2GOoMoRea?(43=#wWz@wpJ~-Seq3;C3h0b1w(ooQaz+I6!k9q2>sZ}0!RCLy;2>pvDv0p|h-4NMuMjWNc6+fC~Wipcr|62-KTSC|`)esDq*8x_t;M&WuB!RXLfjv1=Ec0>qVcb_BU!b_#pDle4g!+CE9fmZcF|6T!g!Z0Nx3N6fLRo(r<IuxRI9J=D6Kqn#usozHfu-f71H1zgee|;S{!Oom9y2ePLV+%<@w&{VaLu%W5t`Z?h6a^7$=wVh5Ci3k-I}sZjvzpXz-(OVEO$QSXhQvx31jP{)vq@%Idn`V2iJN`>pY%DC5?|bP-WLw>Epioz_pi=Hju}SzT4Ad=g?KZc~j#t(|;oVu4}GG-I3J|k<2_9#yUSfJ8TRjA1r<`6HLio8J|i3pfi<UcTozBVViaaYjN#B0hT*Tc*kV&U}RA*Q<Q(@0_BY8UhxsHPxvw9sjsO_BlLlgFCnhZMHWjGSqO>sgil2>M*!)Sz;~5pk=3BRH>>LrCV)8>PAs`N$*WUHjCJ8jQW14c!KhJKcQ7R(T$Wvj3|kkm^$%wX`mMM5tWnAsNU^l;ua5L)^d_u?`uLICIr0*_Hmo^7)J#TUwO5qcXycsboQz-PoNQq-F{lnK9ACl6b7*hcq<)k6G#kWa^tR#w!IZK&wI9!XvHAiE&>ZYGc;el9LrGw~L7!gPW>wqEdrrbwhEg)Q@E35^qMT+_1&0aauvBXy&h7xK@=!dy1D7XGBEiE3OQUg*3$;G3a$EW|jZC!c`aU?-sRzpBS=2@D%eLn;&{^*a`Y9~Go`Nu6-NilPDhaUIpt|UDAwzdX#rv0i>XT^;lY?ZfVY;w~iTXZ?Sx4v!a%0Y3P>CCn|BJX;d+mT3W3C$)XszTl70Dntk@Ioemjr{aR0WP&7eb;&22g_L>X^wYbJ#*+mPlnh$6F2Tng(sh7e8e41j6H5sYzt6Rx|%WQDcww>}>tP1LQIGKey$Dw74a<>aYV<pmMf}f+ReGMa6!DDKTzaT%Cb)ou3tLr1-Q1$BSM9Jw{$=g0`lpTbyQ_*TtkYYy#mFARP8CWSg_C0M~b=i8xnbzKiTpk~Td;(-C1!yd-%Ya_xImYL?pponSMJ0_(7MHwEDMP*-%Ojfpftss&pIc&9cE8P;iM{J^%dk+jHhKOjq*R{BKNmeN^0bD7iRg#;RMCE%S$J2`u<O&vo@xI|Y44Hy`_Mib^}M!s~E`t1q_c#KpAJY?ahW3Jl362uSjE6QM8T?of4-y0Hb=r8zSZz<NCI&PV=KTb07))C;2>H0xJ4&yeDX;cN%o@|C^F%Ld=@Bh>j(hts)Zw;rZlQW2SiAC^QyB4N();XwTDoZyY5_HLi3LXBr;~`(19I5Ao)=0w=sf0kH-zai`za)X3E<MY2+Ma7wv5(pp6s2m@#ze{R1$2yGh@xN!v1D>vU_)p*$pxm{oM)Y$jZ^cvU05PAMCo=uhCC-Y_xnoPALQ3Loc0)E?Y24LGeOluQuJqDdvl%FL_NzzM)-Mo4iE}4%EiF&?nh%&Ylam06YaVtOXToX9V3m(Ijqvb8hGuS)u}gFOQu2-(`w2LeLP_-cF&wnTi87lbjvon<|eNRj*6T1RdedKBm@$*))<K>LCy~xqYR}*pdTC>tB~kDW>84w%Or=mEKh1yz6&ggJ*iegC{W9)qiiS^BHW47P4_%b_o*p+t|^a6Kml4|iJ>PIIGt(vI;b=}fI+uIkBZ<u9I-ehHFj{s98((gGads7`gxT5D-Lza(+gdE%=&VI_+wy2B~WKQe?E5(YgY|tec%5o^JMVGC1UF?5heN64&c~ns+-1#Odeh$Nx%OPDE`voMy_Y;n9Qb<<VCM3W-3o~5-4gJ3VmUaF06Y7N(<ixuvgdvu^DL*tTpjDG+iD6*J)(;qumNtqeGelr9Yeg5V$Y*ks^P<Uas?}5+$z`Afky8-%|Rvb&=V}7(gi4Ql2ACtJQFN%KOabJ|SZ6?@<)kN4C{L+ajHIlGTD_q0m72ChC8<4?BElA7s!>sm8udFwUZ6pdA>zz-%vzEFT`wv*JMeBgax8u~(_(?>RVyYl64U-XWWl5=l@K%yYrsZ8D{3P?;y~-zrkkgZ^1>e+f}-R0u#OmSehzPn6;h1bbbFz{TT_Xr@k2DUm|Ki~E2_+3IEp?{Se60|)u~`zL)(f$7d0dj1z5VR3n5YJf90yhdzcN^ifMb>Jep=wDgG|3%HOHqt0kJpSOVeMOOPm8+*g2ioi;U_R@lP7{?IJ97n$@>Ek9DMhSd+4JK)=(PIq3ugh#fGc_zt%NY~(_U?ZJV6Zcbb31cZcHr|7PdIrCvO{NFN@+1l8tiE@U=B3Fxn~M7(HZf@zDw(Lh&LCge9oXv2{jEQOS^I+@VX)neWm)Wp&fTC(wd?-KX~d+El##Led~OM!W?RsfpZ#1kU6H+~kY!kBfzEcoOr}|Fkb9<EG`(`T2xR5Ta~r*zu7XphJZK!Vq1j4VqWo%xpUPh{`%8Od`|YbdCDnStWWGQtG0FW_pR=EOA&8#j40|Q5h5O@s)MgqcByieYX?+^K<|4?ZKEfLS3hoIesjxc|*N&`C5glSLuCcGo3Qg;8o&iQ+xN`cyW(y-!aM#0$55Lc|Ct;aLY6uoDOk)Cn{i0d&AU|b?-yJJeL-Xi2g;Nal`Y3XOMa{d(D^|+5j6hXn=F7W{f+hNLhgDE_*o`sCBhgJ-lQt){>Jl@eN%wwuV0NybOac>-m%MZrZZZ?o(F2(MtTDr|cEAZGwUhv1Q<ZfNw>%4G^T)eSa1{^O~<B{fLQ28O!h#ag-p=s%7eyVN42hO@4A9V6KFzI;OxuN@U73{hU>x`M3;|if|5cTEt87r8cG>nZz-gQiSJ+5EffC<4Nnd)1sM)o?u*>Mt4A+Nf_M|Oa(;$Tg@OYL#{Q!vB!;AO^$2}<W2Fdjf>TRhrbL<ujT_N17P$0)k%_viTY3NGOVgyz->zBY}2=iZ6P>)n+!1|3B$0#4dA-^bVASbbhlM|BBLF`c%8d-xN3=FgO*CAwD{3Y8izgsI9at2cwss)K5R&OHdnBWV_!f<yNX!Th}s&(#yshgJ><GEZATh4i6s6tTKYM&^i24@iGpGdsi21;bGK6O)>!nNOD4WeF68mT@xTIvPM`0_Q|Z`CD0u<PEn`h6X9Wech~^t)yc+ONYI64JK68i1)RuI+B8y|G@Z`hK*;^oQ<DCyCeV`MqNHqDuj1ibCm}9rP`y9=2(-QzOYD-cgr6gZ5r^<Yee1EdIfw5cE%tGx^rAq24s2n6k%QSS<FObwj)>2xiE~SU`GNy2crt!)2A*6C}`f}`aCD{XK^T0f3FZsVrlbAAm7@W!>iQX+O9msyXwJ>VFaGB=+`h4N_C2qusTj-phFPmdYm+mi^3hOcKD&{jInjwkcqi{jnC^@^lJaZVO-=;-I$9*Wtw~u#4+zc+8*splEiJLxhxd07-PUy{&NO0h342d5YZZAc-07lzdeleIq6PY7=2p%o^u#g;5>=?}0speuq{wM(j)j6ZghMHTtFK8Fdcn`xyC%}Xv*dOCKl0chhy=MbEl_?5M4x<ct(_H%cWflZq0NXB0asj8!hJ9Q`*pE9excsHzC(1&67^P!Zv&u)d5AgF?wXyXX1<Z?n(9r8(5NREbr*w0)_&KCx;`<amb|P`7(mi;Lck5%V1_7|%l&Q;YQ|gy??aPo*K4)qu5DrO$OBR+1MGJ?#WNEbAneJ-}Y|j{8{lvC?&dVfoywc?pxQ2pWgLeG#YhG%it4|N~qJQUn^e#MUDPa`Ao-T$RRO&n6u84rU)7+O;52j!9RfizBX&-~KeoNe6shjiY3_1Gm>F8z{KnDN%&HD}c{_SI?6XgY6GQ6N)MGLw#J)=^99FzJl3Go0SSQ~J*8uMt{J((PYJX{c^t;;)OAo8LJB$}6H>(bieri<%Jbh^bXuPmyj(b)M(m)xffN9ZKZ=xM96KxW9J{bXwz9q+y^sK$4{_j`DyI0>ZXi};Z|I}HvnWMCfR9vIA|8(qcrF4nJtY5F_b$|7Lw7xy2Af2xZDXk1O0Wdujy3$S`N==#IpfJEUA6Tu+)%8v|p`u)b5$!^aiXYB%l^x8VqUe<h^2?;0{0t%V1MzHY~tL8M_rWitsSQNo{Za)d8&bxqgx}xMy;Zvew_2(`&sG(yRXo?g88RxfbR`P=W|M9u>kXJt2+mcjj2DKHLGI0@G5t^yjwR2)N3&*bS`{SYi<J)gP{qfEG@Z-VXw@cmg{nu~5o1gb>X=^iYG#S@#8XJ48`4S~CES{Gc*w&>vM`7O}gj$RZE_ojKN(r0Lt}Wb!=U04FSw`%d*)Paz?|mWKHB^uXx8GdkKmYvt{V$It&=C@<;jakN#<FD?7g^u)hlE4FeQLv)YmHf0ZA_Y}#|ZH+-#(<eqf#Uv>!ga`{rK3ofH>Wj)rgr5hI?(q9%~po{LjCB`Ss`j{qvLm_?LMh?7;4~%>LSG=bEy)Sf3tiQH{XoO}C$j8OWs0M03yF{NLDc|AMieHviauO}@vjY4aU$ry_zTfa_%}{Ab?r;Ss<Q-|_J~ER9`$o1QhDI6`zr9yU!U%orQ?QoD@2Emmk4mPX0DV#lTQq-`UwSfl5=)<nmKz!Kg7bdaRJdDelB{;oZj%aaLim<^x{b$srV(oM#=cR%qh-J{Q;-VSn&XxHRstOr=YCF=j__g{Yd>DR+N-cR>BrSaW*{gd(;*?nB2E=%X>A)*7(Z!r8ZK%$Ln)J7SGcTe`;Idigx&hw>c=sT`ePHOQ1K|e<70fWn~=h|#i`|t)n9hlZl%sYU`sCGR?OuKyjp*ajkW5X9HYQ0dDpd~BttbO*qKi8{a2Bh>+*spc^Uo3VruibVYwM{Rj!S*)>u0U~b=Tb(#Fljw$oC6Mh^xoVpa)J4haEa82R(Wg)zNG21Z*jxqZ^QnC!VYr5q*{owK>PT5tU(Nl8TToZYO(8DzNkPx?m~Yi*1`0JR#_dKlmYbof@c;k6N|erIZZVY?h(Q-a0DtTVlOV+{`H4c&A8+U+vMrwW^!h-2ea|0|M|D~_rHHWA^W1La%iB_oO>uM{Wudp=CJlL%Gzp=3RNKg3QpPfMDZ0QWy0pAcLtN?E4j;j$dBz{$fL$yE_&3{E&9HjJ2hlWABu1U(#;ZKX<<`sb_b@R7pw+Q(o!-Wr+mD_JPlL6$PChnl)S+?CxU3HzpQgGY#Q@`b^+#BGn&I=I3;r2!2*GE8ro!FyR1)ee-cQ>)L+>eO@&%ls;|qgmVZJ+=xw-I*2o1C#!i=Z{+NbYNnk83C=2G6gf!`+V9<{<LC^4}7VG#6+GSx0uK5_<9*cgMpnb-H4W!^Tm<mu7Q!{qw_J;@_N)<r6J`{YSUBw1(Lun>R4ISJbjHI%skBER>D>PHg&f^8BY@aPe(1!la6=Dh7W2m!Qllvgzo?+l^M+}ghQo4H@i=IBT_UN(S-(0$ij|x(N(Fg(Rc_5;^lLdr;5&K_&#k3<lhO)e_>NCAI-7qy&GN6({bY+7o5F=`|DGd8iwo$8wzL+d!iH%UuZBw`hlkLjfglSNX^Ld!$`j_Y9`M!$9L_du%xeq%km7!N5s?+F5AA&`PXD4iQWlGXf4bP9)pIYcQ@46gw+Iw2z?PJUm6)fhxjba{qMqzz%;N7$hF5tswwIPpl*@qhpB;?f|0YTOI+|fA!^q`5yg!k>a+H(iNJi9{_EJIlXuMXk7_VrAIC<8Wuw8k^s)8!o4mKG!ghd=WAs4T4Gr_B3vr5NTUF@~hur<YMhq<knUIPt$Z4AmHl^4D+Q{`vj@{KGED`RJ8Nol7z=PJO7VBX0dJTKLACPIa089rGg0+-}~dq&j@Kz)Vl4vPg+?40g%jt23ONiB3_{LvV~zPVsP+BH9VbVgxA3d>dQEKK{{wusCGh=BI)=pkJVW1Quo`2-orFCa>eChIg}$f{$Z{?rSH#MZdr<ENA3oD=?l9c+D5W9rJjz-66K=Lk<3HHTYZ~HnGK{qnzp@SH^?RTSdGDI5^hJ*2}Qx@mmHts|AFHti!;kWj$_l%a2{}R~ed?QN`|9+#tvtv7HD|sm&K6=w}LH>)^aRllmfRp4Nmf0UjhU5)L|a?n#0zRYuYwSDfX7D7#Y+J?Ec0_Ot7rh8Z#+D{`9MMNd}Jo^S@QV0rD2_p}L`DGceD))v5_X}yZ1);=GX@H$h{?DWje4O=77!##Wj_tvsP8j7~2zTx9>BbMpzy<7G7Q6$)lKq-DLsAJQb#6*J-k9wj|vOU@vyO~7XudQE&MvP1?<f#)$l_HQCqj^kRuG^@$A+;ga*$v^!vU&tCgKi>6-IQ&5UU40wGT5E-Npe)*#ZnBpdBt}WxHO9f(#A~lP!KtlCsKMEAkeMg|LX6D(6Bc}g4uD(di^3q^rVPIe<;o905}ZKsaL{i@R3Y!E2<B6$dkg&bdTNKfXqJ9%38qP*D(HhM3ggw+Gn@`b|A84wEB}VTk{YW5JB0HgovceG(NF&gD7K2LmRoWINj$o1B1}L0v*f3hTGGzJP%Q$PFQi#?~5N=ld}8iN#BM$PS4uw<+WydZeUF|!UDk_rN#qKHq5W8<&Dvdc$Mur;80{l9hz#Py($gUjb*rEa)pe$E9`;DrY?^0?lf62OTb$-?aKX3POI%3>;^4FTRl-~z&afFcw3TO2xPI^(I!w7B*<rtg)|pwk8A@=viKg%oTv&}>U~AtooW<owCsW3&5>EN<WZa_Rm}v1JiK?>=ND4m#<_O1(7uNHnRz$!B3qxR*8lwTH%CB9)>#7KlZ0oJi?xR@;mXvF81LpW)h$O^%+MK{94dj>T-~A)>F9hWLs6OBQbVy?hb-VQm$`?3;S-hV_>oZdNdtLj-u#ne^_WZTk~^@?G=OpvP&}k6UUP%2P_zzEKUHAYh1{~WRt>3sq^iU^>B2`7X*TFpDt~z!jDcNVuKCtzKShfx()ZY<R-gmCzD!XLtiguhjjz|JmS-TT?wYb(68cf)`LDWMj;yE=1DrgEvu=(3`J9x;&*J8SNt-f*P&9@DjB$SzsYPFZTo2~>Ad;S2AcuWqvPogXX#7IAYZ=oF2G)J&Fd{+f`1acGSt9cSh|G^^bpS}+Ug29%31u{A$3H`0ux63ezQ%d!19CwhmkpI?iG=Kvy~hnk#rirR8|3S?F+W%sOAX#$Q1$gyASqBcW&)TS2E{yCZ?AwN1lqzLE*=k^o(-pRotI4x>$+50eB4C~c2j+{RtD(8STjdmBC(6%)KbXI#Y*+O&Uva7)}wEMzn@?f76+)x>Bp!`&aY=VM2#$gK-Gm<v_aDZNO`@{k?0w_edyM%tWg?8?*Tj&<gdq9!lijOcpGF-n3m|TLjuJGc07|=#Vr(94U~GmB3riA1j-P40`xuSi8B68ul!(tEA)WU4&i;z_LNP5Zz77LDFQ-xa2r>~UJwPV;mYp@;B+u}^SFiWBaTtr$4o~~9F(Q|$Rm{+FB;x;Y9mG~8Tcy@t`e;XNrH@pdtD7_T6F#~IU1QRWobA10gsr}l91E%dU;NNXOCEFNKyjfzEBS3qR2{q=bY<pe-^fRhvQR*Q6&S@kai5dNB=@bhU_6yzXk&LS<Om%2_21vcErccJIJk*D#vCJ?!_uYk>N?a+)e`q-4Nz{nKDF@jWSIl{K3;>WTwM0#AT5C;K{AFVNEJ8dA;r~F)0{4C#lTmyq@+D%Mb|^!0u<3Yq8Z<lZ#U%WaFf#k#Sp0p0Bv`9;1XNaDxc-Z`^cqTR8AnJp!vTPHN7T5j{Aj&(H0&xiT;?A=8-f-E4i5I;v4sPC#R?=OI{RT18&RV&!$#7Zal|${1w;dy1#_BtzFz2vxZEe-*LAZ{`sjlu3wb=vkr391xtj*T-(cH1=&m1c>&Me_}mZVFW4-GZcegen^bR90CPT6rrbQe#jJZnKMct;5&IQw+()!ew1UBJIn;PXCJyI0;(GOw)PZDh_lO}jsU65Asupta^~`_5L;u_<b3|Yqq2DndU}rS?~DDaIZ7A+0tG9+jL0&?s+;n2J{vJq3hhj@m4-)4VmM(k%0w%hQ-tu`;xX7o-Z%;mwU&wYkTG2KF|a+6^W)hH*X8qSYcjr`C1OemvwuO#EG%YHJkir2_R{c8g@7lKCX0Eytb<J+c2w}wSo!?JDv{m2E6Ns%*ItTT9ij<Hrpc+0J*6O%CB$=51;%iB9ef%KP#H4qkPJMAzIK;MwBA3KPUw{7ZU_-zCA^fqr_N}uGQRSR)Y>M{g+#DJ#?_=HBe?}pg)6G4_%F4n;%zec{?)08ZXD0UN6{B7xw*W5p%4w6+7wJ}l2P7b%^RgF-GZKt&r$7M-~lalmJ#7ON<BYG&zP;0Y{W6}UPi+}uQvK_Pd^SLJS~+wuK$T3s6jM`y{e9?Z3sH#8Hw<nn<07@EOjvx+!FW-`zQ-oQ3(wXJ5=02qCp;8n_~wGV3$$WF(w}dBb)kqHyApN)%mq3C+Fuai!2EIn3MFNf3hhgm=WdzEji!LOIS)AJK+YXppqtY+=y&Dwd4>V#!gX&Uxe73#}{bxh$_n(<&FS-eCu-H=LdOutofeRQUFO>SxfwwGIXgZn~OpLFFV^H9fSAXOT&waTHBKzJH^#;iqCg_qm3fk3qO9<3%_Nwi_mMg@JcabqM*GPllsk+W3W8adV-v`&B<bW_LpT!k)Q9NEkU&7W==~dD)Y2v+pG$zc<*7D?4$f9ZXw^=iY>}4MfE(GwhN0+7N+P9aOqQ9xDElpIfFiOkrg7_L{YXqpA^gbO3>?IDL>)mzKuQ-w^rIiDGv`AF3edx(Q8~9WGjWL37R4JI&hYHH&WS`1SOqR>4=c4Ne(tJ<fw_4Q};(z{v_ifxDmulxS#8gN$l?DP%xq>r04^OHRvxn+hKn&$nkkDAmbu(A<SH2T}@UU8&ik*S+N~jtWPvS^B*<WqBek7fQ?IZI~Nl<y;!cVh5%UJHOn!8Le?jXi~Ql7uEM+)`Mo8*hoplwDh_(4z7Dxo1S$n)lOxdVCu+!!KURmm8wrVBNnLS|Hd)YQkOyan)z;deP;EYoG4<I@ViI8x_cpKuQKipAZK)L1GnY9{p0~$(FGyuB+{yd4l}>?fk%O9Mk~EIwW1ve%;fPb=(hgqXI)?4Db<AZ=S)%Kq0T0D!He(1(?!BSH20bLZu{nvSjTX)8xMdP*IQz)4upkksGq<a`$~ujzR0Re}%K&%gv*TkI!5UU>*QTknRi1;~BV?1ExoPxqjwP8&m8&VVuj?U2dyGj3EImt2UmLaC41NZ5Dury^{#D`8m+PBNYou?42*4rXUlgCfUy_RZXDRy_^7b4$_yQG}zbJcNW69uDE!@wTQ%zVgxBFmv40l100DqkGtn;RD&Kwu`9;xxFz>4v_zw?~n-t8+Mevn`1V6kI}wcEsm4;keQ4}TlPIbir}BJu9lpcTDZKVilC=+A?&sih1GM2PlSlOAxWFpiP#vK+h(rCEoReULhpXKKhHn>wUndmv3g1`F*w!wsZ8x_8{E>WhaX4_gTZMw3yy@6segWJ!`59F_={;HFfw{=Q}ZL$iHzfQ>Z-&j$@>jfSZi888NJ0zGzB{C!NwBWYN9sry*WKix+elE}kYEPReaO5eCGIh@06&e??X)Wjq%Pik1b3#3~;Nqp@BxxKx$tU64D7W2dXJHtEAuDUKr*>k-;Od<sEKuX*gVzTB^t*doV88HCmVTWD`0W3JuK}y2*=npuiH0t*tF8cQqU-s9#>Xc{txWpdyH4$blD#0!56!KXsSd&{g$@_L!xkH_IXAtvuNi2|Gje=nT^K}}%SZ|ytgUh&Nxy{fiJA$*jb{DlIGT!?S0Th8&eDi%D|7~rc`h-R+T5e2@o4~_+1(TF}#{{Pv7q;#hR4#nv!0urO%+`R?j#Mz4rhOsc5R9I(Xaj?F310|((#Pz^c(3kbM$V4Cg6B^qs?3y~D2%eGOL(8C%x=Vl0fJ4{<85#$qYk)e`o}!yK6y><(o$qy1O$u9OVQ5h<aVrLD~sj@A`H6d+kFC|zwsarWJ;^{X@ie;l%UbruV<%5JL04Uv6^9MNiGd<94(%bQ;*!U!~`%02Xsv^N!fd5lei)aV?QT*ZTRmQtzo)anMT2qM4oeMk4c1ZOG?2lQ(ZCnuomDbR`)Dx04xBkL*PX6mpB8tp~B?NQlwHf%Q=@(Hscw}YMkN4I9PGl{A<&QFi=JriZ5a1bA|4YY{)Uv6m<7AMdyF<%@q%ebR}-5<t!hq5o43GN^-i1t81cvmCpY~U8}D3Ijty#t00TM2FGN{=ZzjN`d5GyRvG;f<{EIK@Du0ZbgQ{Z9}lWv*+xM3UcPDXew4OQQ;x#J0hyawC%q+d0^mXXBaHM4$z#<u#HW0`2fceAKEfd&e{f~P<V)c1@c9OAgFHdJrD5YR@H2(fUf48iEyp&>4nD<$C0j4y%hbXJz-Xt0i;g04?EN`ROyMG*7RViLXAmF3I%us6hLxSvb#>E&cF<;jUHJC@+G3aeLJHE45pO)W+iD^~CV}!f+cfzi{Np6BFK%FeOf%1OPkZq)zI?7=Mw@$j61>|Q9o5_b9l8$?@9N@P&|b<(-fh!ypH#gkVdI!2p(wO+AO7B1o_!aJLZaAUa^))m_=p+n^IR&TOH{eTdt_xn>?kp!ChOb2s6RjVAKxBqY$MZj8lU6GLO=?XmX>c@D1wyP_c@yBlnKkP>OGs<#{9<1?CI^h559xfm6BIpkL8(sVEGS+Wg)pi79)jtNbBB*VS7Fy%{cIh?R-Fi!6QihoV{kO4Q=_4I{3gb4O7|AP4SI#GS*#oelXJVYOS<(0Oxz{uRc+h*w>7$q3=E~4&qzcG(M@aT_%-cfCqFZx3q~8^<9GMA~9OvfPimBMhp;~*L{B$xAvN^)Y8Xo*vs$~!<eANsbw0MVN7aKO@7QD@PxutV+w!sNffF~(@#ZBT)l7^Cbj1zNL5Ly=nAiea2?+Gd7D+acUU%}Xhe!j<e5Z0Z@4scCPXBjX_3c7$VA#%O$;tWt~Jatzl}aij+G6hL)CO4Yt(?ahsMKShNV}t0n|0(a?n@gPP`ZQf@)cYRW%g2Z}gmP`g*ZF1;=rd!M-Gq7<L>39Acj|=6Rm(_IOWZu0#C1bJ?JzIxQ-s6-@ItX&m}Q&}8L4;Dza3D}5*{mX<X0ANwLQ+W5)3zSLe-Hs%CCf?PMIZ}@D~RHJ2|Gt15-zb*AcfRxN6HEhdQ)R-4cyXZTY%!iw#$K!?LfdvSiu3)UL7DbbrJ>$n^tO?PppmY{-!h@{V!=sqABZ1elo%37L9px;JrQ(YZKWA@3D^kOSn9_$i(f>yiAIuPed4l;phw7fAiEerZAVvd9a-5vpF~WM!=fL+TiyL8QH{)WEG4~dr3CPcuY3Qh5Af=70rL<^qs#WEsOyLeq<CEz_$gSga$l2)%K@Kz>V2&u~f6Q?b(}fQMQz>)No28`!*^le4CQ9y1^M8H9@ET+`io7itP-yvl9-PPoN8fNq@zU^!`6<qbn@-|fDqPkzlDJ)7o=hCwB%_0LU#3My#(gLmx{r57Ukxs#n036{$yLYnU2$I!h7jaNU4Vs_$r1Lnx_f%echh%DF2Vy07<#t>i8MU+RauT>Iw5lrLocQ{gTOq%yQs<|yH{zBh>mzr?W1R6oShG8T;{P;_{p~6poAS%BaJdae9?*9J$ETF^sq;DB6HfC$HJ?d5F<%J&a>WUh28QLCpE{RHr79tyT4CJkc~p7hU5!@|7#;?@IykvYIjrc4GUiuH^rEgyBf=6F;5=FTQA`ZwB|)WiRke$uWg5a?>A?5O!dB#t4w<ag-?Q4RpimmcMBh*-}-bSK<Ys^Y(exH@5vPH$sQ$<v;qR7DG!2R!EUNo?KY<}=viJWi3f4EG;0w|Rm@jR9xv6>P$M#F<5b%Q+df)4aZ8eAk}2rviV8GzLH`PviF=;NO({8H10L~G)lv99xs>2w>5D9N`61aW!oTh$vjii{mbxZ7!u4cM^zWdOsC7=?#~sG^%$O=I(d_qu0aIFf-M;;UiTaq@`dp`P{;Rmq=FiD=enO4gCGOVOeU40fvo9DGN5sQ0SXcS_&HHuw{_SI?6QyonGSux~#oWF$?fg=DELL|~5-L(MU<ia=1FmZ|donpaGjKtahEDH{f!qQGDbh*}TbI^&H*K9)F8VE@GeI+A-~l~9=~5A~;WeGaY3{ZvKcS%*%agsTbiDhvphExs-iOMGOazN0qdzkGD)$XBughkx(fqpX{Ern_Lx2_Yco{MKCl%a@;zR<D5e04GJ#?RdXg0;`Gj<FEO%b0}T&@H&wK>O2FT{_}Wl5e17{qFhK&4O*ZAGSx1Ibo|=InK0IVC{}-|&5Zyd!^n`|YPczL_6>e4Y30QVD+l_1o{}=YOoB;z=Ai_v<%}J94b~rc#>RzpyvQBBJ##`fnMkp_^m%=bzuc|K+g+DsT<}zSk`pn`lVv;9#u@jH_42Odq4$GR&c@VcNfkCd3`<5OXO#bd@g7rPh;+6v6fR8H`8v^Zk0<r|<vrXHfU^{h9me_g{Yd>H8n~>$h+Jd=IsN&V6X;z3qyG)ybqWdpt+Cp^Ei9VJ?%Z6nlIy<FO*&v2i`vqhm;6Z1O+<`sLT3|MxH74g<!<bGLH0-}&?VfBdU)VjEzKy#PhEwx1@|{%K77$AQLf`eSS;$HAD65q$2NCV6L<>2a}TQ`K;X+wmzXyRLrf<IIGE)q);@n&Ma^mN1Y!WYQ;R_UPfWg189atHy@;8vappFCI5frv?!{DQ6iu^~BhaCEL~I9nM1Yw=_!L;5;tTMd!5)?9rRw5y<|=Wr?phI$jdh0V54Se^)-O%lbNsLO%~7+n}XaL$TX^Yzbt2wTgByYs3>6pZQAwfA?(u^6leuMb;^e*4Im_l(fpes%w#zQFC5Y!qTB<n!P6)B=MMEmD53dK+vs`+U3xtSVP1Ec;8rVMq&~%MFMh0^)#AINB;STu722gkIsLgUMX9)?OC#6D>Y<;>ogY&=uRJF(o3=1++RfplQ%YWl%oC@1!h`~4F74$`6lOjZF(sLHZ(F+Lr~Mqj52cgNkdWNByg0bqX;!_GL0@T!lS%BQP?^@eA8hjob2Aysg*53Lmnq>1p5}Z<o<!!$5&N}eVzcj5g}z4y~2Tm^Ahro`}!<FVuPwT8Qsf=#x0R$k)fw1H&L~i*YTf!dw>7CoSSN@P_{r}F^j0ackaaP!-;FsLORqohjG`v^MqVi*i2<7)|zc8q3~l4(=g~fnAV2^2hbzt&x~nQ$!VDG_+!i1O)%xYUK|R}os(%uNY^ADGG4V-;*qJLAF=VsV{#9UhCog<CWPBS#?XlZRT(@a#8Dp%-YWx4P304zSIw|^Yp*UVFpUwy5&c!d)DO~4u@b`(*-Z_h14x-8au+B6;$AK`vSS=Y9f!iB$rztx_}4M88oWXD3{a3@8j@DdF)jbTWRQ~{ni>`XYnp{(q3b)bqiwk4^y*RThG=D_$#$??=K(n-3Kdnp8!P>=PotVBvoChoaUf}Ls($V?P3fTmCkUfe?oVE095O4J$TtCrji`?15=&&tLiUUwW8Zta@~lyh{W}tJO--YtI120KflO`-NdzB0t1xR$JnU>F)!**96}-YT%?So(T9OJ8)67dg#?nC&OcNQbN+z)4obJuM_BCIDF!F9cn0b-iig`<mdV$05>>Tlx(tc1q2fRO*qRBYa_I#D$--Vs>{GBqY<**M$Vj=#wXi6QJpY!mQNu3J^H1Mw=QeFdVadT)Mzw?Zi`QI@w!UO9DoJF8cQ`HN4x?c#E4h(k5K=U%JZi%J?!qs$)a#Mk8TmplF>RBLppMV`(9R*M0mWsUrZ5OUW@fQ68JDnY3=qLR5d`7E4`v~GaU<(lNj#<ShZnC-UbA8yv7LV9#s^QsZ)S#%1m(kz@H^ch6ZY{;NgH_O6Ch)3{7`LMMk9JC`r9bDf3@VNdNl)0p^X;+z`y*|c57W!&PE5<FR@^K+!cUdL6BQs^nlHps-4vqVz_}No_{>rCWZ$gaT>_rgz}PuJ>=}3HWj)A7>7Lc*k^N^>?@zeDA&xvul7)EGX;~8GG14?<pXD!WQh4it-`=mt79{v-RX>KyE7zQoj`jkJr$%z!I@tFh8PfK)#8`%DrYYq3_4kO6w0rMX{rwkNgC2ohysp)9%6Dv9lm2Msq65e^2B`C$VI}xze`8bTPi-4gQ?qVyScjDvyMdu`6EE`grsqX&A#R(UUcU`l^$u(kx0?riM<GtLXdunYbfyFaIe8+b2mOcqWd5)IehAR|Dbg<e`n1@#Cz}jwM4}MqkkAhrD;mG?XEjxk68%sb5osHcIR?giof{#ekF=Bt@TR?=H21?H3Qygdd8mC>3%I$FA)}?5jLn*dMTSG$;F7%ob~ltm5HjWx0Uj0x`;-x25FtWbK8ipnM?p*o)^8rCjP*k%V12DMoEtO^2##%VLa98!0|>?RNE6L5vXp`;SFfX!5bPp#-jCs~vM?2(qG4b_O%BRliH4?tU{OI*kI{fc5DU3<d`V=^jfMm`HL+Qavar;`sr&C6<|%<l1?WWkRNtdhm!p|3>>C|y0@*-9Vg{<G89jSq8!(MUXu%dmSs+Z*awAu&5nKR3$b5PewTQky4_4BSK<&sK&|VMu3?y&XJgL0yAWY-UPQbz?p7eQ^*+27NfeZyLf?e$CyvX+S%cHJ&j=+~p>>j@9grSQI{c1AAc}|b%oa&b2vSU~aO*xMsd9F@M8B~-#B+{}38mtJSJW$85=ANF(Pk5yB)<ZQAJK#hkGbP12=2E+Oi*4&S;Nx;#2Gxo-I0=QS7@)Z#(=H^J?bF)Ou12K8jF>z00}$mho0Gb{4T!=nFQ-awWG|w{6}bWIQrD_GemoZ_gRS*;AV7cT=A7pmCPG+X#VL7wxQ*f#R9yi;CTor{OrB$1x5g-a9yA=Aki0e~00@C2jrFi&Y@rj@dVhI~$h<_5N!#ZE_yj1dNRU>1bSl;?OK3T#(t(%+GE9#t8>r1RJ1z_Y1T+gnUenVvSo&aGDo-HTMLKam2PQaQ4VuEf4xljUYc)||sJX4+x~)&L==F*kL0~5rWT$MR6Ay9Mh%NB?>Vk&z5H?1$px96+!+4i*@jlBbBF5DS8m^1sR5S=4HlK<(pYnCi^EX?k8TC@z9c5mwDj|D}y5zi8xa7Y28mBgA6^LVap{GaUj_}^o0$fVl>-3r$EK2}7*E<l2#^i@5I|5cS%3<hqf2Y##^}b1HF{hzvZit7Xqlgq@5}YxCIUqZJh;2}#y$!PWOd$%_xq-S1vjoWu<yI4r!6&LzI(G~5*O;f;(62f)*m+gmV|{Yx6S@iL{80>p;Da<ipuJcM+QQykglsVW9T+>HB?<hX8*};T_wQq-6((+^Ot*taZ2Mk}x=%z+W5KH($VNR)1np@)QW?5qIuT8Ural$)96{B*XoC~NhK-HeLw_PlW?;vdXlt@9*7U;3bk>f19XMWnHwqkp=-Iqq@-1acVFrnvI!Xg<Xtp0w$t9SE`B}$`?ZNFKxhGafeN2^I#PrDTv;_Nc5ugmCD#fCKLmA?f{)LQq&7A`6n8VZ|434R|%_&*p(x=b!9iFQNcfYuHpbWE;9`z^k?rX^gEq97eqBdVLyCS0nIVy%zJIXFY&aW;*4HG!Xx~YluGZJIwkZ|k$Fw6HVBXdd+^JTLesXV(I&b{;edl}YFiNGht4WCg-j59Q)1%@`RJ55S_jrw01x)A6#R}F3^Owkur7ch?gX7gkhcba2VOaal4HKnXt2iFPwRZzD(hB&GCbw>T-81#2Hv(~zRU|>SsBN4k<C;=soi3;dK9dtbpK`0apJ$*$XmYR59w-hXPR0`?AIoOj7V>KZ`!NdPcOW=S#fuovMCLxnS&kD^<gOrSWee5PoW8Wr3T^C+$Lxg@P9ATw_g);27<}-7^B0N!q#G83nQ;CMoNWy?e==mQu=OuN#9ivR~yJ%A1iFBcQ|HHt&Ogl_+wU-!riW+Mt)PQfVqXcxl4C+X0m3hq5<BB}AA)e3bd|~dbGEbdsqyHZNZ!UQrAeP-E>a{L}c8>G^$6zBOcdE4vtgJ@R&pI$}11qC0O7Ov9Qwhx);9aK4VtDbZl%y86NYTa|KIod{Iw?yja?OsW7n#zV!pxOI#Fh}QOBKArm!pAn5^gRMpL@P_0?muz+_a@uM|r|beiA;tS>fYjl52O_P;0$qarOPBaqU<n#p?oIO4)mA+~$U3OJKbQ2ayzMWt^cy9YV)taY`quY)@LER;>sna;0^W(fc9<0cGgS6XN-S7|Ni;fyZ?8=A<0`p`Wd0gk}NGyD<pI6mkfw#~`%9^@XWZ#ObJY3aTn%R|`;kDK-P~#^}3hN>&6Up4RS|6!#bZ6aIE6F01K1hA?48Q%wVW8>rM}IvMF6pbQ<OxS9N<y96cY0^jD+fc~w$wJwuP`A_LOBTCuQ;OFIjB!)?4fEW!%kaKRA$hj4AYKixm#GzL-&m5;UuinS9$ZDnD1JL!75o{Q9?UtO+>ZK?p-mdT@$vCoWuDB7?b!y@v=8|0p;q(#yOz8P+7E*G|XN~Y!KtkfeCzyghGp-L-Jux5I=#L(ADH&=MkPKp4k-*DlDS=}|YsQuFGVx-H(~@HJAVV&d`;9iAY5vRjRsPEsX1W0V*yC%v@X|2j=izW+m2XE;2B7V1Wt&x<9q$1MU3p4t<kqU~UD&E(IUW3c5ZBWStMMmmss$Jmwk>_)B&^43c7cgub`7n8!$XQ4q;1b<|FUice4trwGxf+_ula3O`_v~{gbQ~d1_0B5i25gb=}Rkh%TQ~A^bYp)xTb<zdf1l){~{}HV5veX?jx}yf+0u!=v-(b6n4!Kp@N%29@gq6hgua|6WN1q3b#M4hXYlGXl_|Z>K=+0fo>tsuVM^iE{L1-$Rs?j<NdC~DDyMMnaJog`m{-^(|9<CY>VnJKdaP5%i#&&B>z!bbvdR|XiBN3C@PCN>(gr;;u=DN6)E$#i0RkQk7Xg0pDFHOUW@FGkR}pB0}!>#c`sfaat$X`Sdiayoun`H#A^ez&7deTtSlT8D<+C*r66p*)_`j$&CDo9ZE`hfapN`?mTIcpzBU+G`OIZbljroZ;t;7_hC6xRwi3c(b<8RCe;G8DvI-spUHiJq(P>k*0J$TZXUp!r8#dVL$P{k0USG#8lj6eRI|rx&A4L~z5Ymaac}%0K_3~tYBZ~=eypth8uhY~?y`e*3I6;`(L8MeRcxP&zs$B4(Eo2W#(_@seh_1gjIYd}(P`erE4rqc3dHDUS!h<>2>6ya1F=Z`s<NKg|?*eFPh<prrdk*<}L6OW~l+doRvUjTZ?kBOSbhF5Qaa-WkRt{1L>^d`ggE^c$@SnAAQ_V*~q*8UB6Lj2t^}P@B>l~+c46$~bnD8N^v|cH4B-gu|H?^uk(FD=rX=)x07xFREC{vCeAHM^RRVO=@oN7pJoZ5Yz28(A-#W(Zx&O$-xp!ufJmNi*Da8%qhXa|AAnNTVru{?Ax!}}F-{Kn0XQKFd~u;odGt#^Umt1qkP_Waed>cwMP0S#CD^e{bV$hCrH&ow+S-4Z~QDKP=~c{?X{kHC+$4k`fv5cBO&Re=OdEaxU=XRcEk^+O*QK>MjepUQS0K+0oAQ=Spv;vd!5c)@i}(g4h{7J~FE#UYz>E<+&2%iZ2uR2pK|6XW;vv;HT69_kommHT&Hp})w$Um`s6t38~2=QP&tbT<epNK*-@s?r*Q?>zXAZG&<q6iSh+Ah##IMO`ZdK;yYZOnAC+{TeKE(BvGw3(-vR$wW`9qA5@pnMs3D!v|C0**cXH-*H)&&<H$8kC?<Wk^T<AxQQ#Xt0;o|kqSLlvbMZEsdzdt&uiR9kp>l#KJCY{Cb%xF6Kex+k^RbfM9Cg)GHFygVQT|#l`%5{6xAgJs8G6HnRJ6`4ta3o+Ni$U#{=3tJ=e^^90_fJGfG=W8SR##w8aG%jO^jvU;g=BQ!tqGex3it2UA>L4Z(A<_Gdn8jW`&ThCw-q<5G0!U*j&q`%IR6ICHi}d{KUXl?x{UaD8^-Sqn*by&KV=zEny_ImmfKJ&cbhaGcy^!Me)?n;xc}2t@`xji2tABFcg?!kbPj30g|7^JxFC&EeQDQaJCr37xi)!|W2qf;WwPA$il=-kEfH7os=r6r}wZg&v)9h<XroT>zQ65aMlrnBSit_m6K6ho@mwKaKwJV`2UmY9`1O<(%M~Dk#0#zVl$BQ|2YV(jspvRQipleAv5p3D@>8dnT|UUsD5*hwt=H7!e`&`Hx{1{U$>puAXp;lFCIL`0#+xP-~ZIZ*isSdY!Z?w(~u7e8|Ap%z^hQCBrfZw$?v>QpoPT5wb_iI0Hy@>b|8fi^u^QpeD)n0UO_bOXyRs`~GZw;ssyDSenteiiaUvhNoIj8{ozps9p8C@yjqK3lx)|?g|JqpdYUhsVTDxMVpslQjr*3h=)CQt`Z{bPtazM&e}PpRh<$p5S=j=Exu4)Pz4BiAMGaBV7zGHO+e&X5VTBG#!~s`OL-orap+^Sl_{8k_0%B*J-O$=OI{kb?;s4I)QZ%L@rCf*SKkbE&J2|)99d9p(CnDta>lPan^w^YF>{fWbvYl89dB#{ue?u$biRyl@sivdu5NQ*(m*=qh){;*ho7_iPbPOdpF^~d3B(TdNf~82n2a=uYcoswh;F*G7AN5)Ds8{pQlQvert!%L0Rp=nRDj)*E+sFM`NrV3b8qHzs*@NaJd96m3pcl4^Z$b%k2Poab8hp0Ymjhtf*LmVHgW#N<av-%!pUAQQx(IOsOw2W^Oso9@&%x!$pvm4b6#{wET0dKItzlBc}c_w_shM?Be#r!Hgg<AGA`eMKHjZEd`yN)DnyN$hKX~~Ax54xB&E>lh@Gi<T~rRnWsY$3yuZ}1J&-uf>$zGQeF2?1&jJQeya?I2MIC85zL;kn8i6bHsit(!!!6KMAEOpX<p50u3q*lGM3g=$UB%sZJ_ft!ON<PJv1lF6jnpo2FV=I%cwS{Pa7btr7(B5tJa(uo^!>Eh^VY|P0{nSVhbN_5VA+e=ZtPJ6rlnt4$9>@WM;5?Z&PES|QI|WM@d5ghy|^?PbBu42xyWgjA<=_JgTN4*6_iVtQWGFEJ-(1tEOXu1OIh_8=rvz;G-}wwycg6WPo{zJk}Qx2NTBPVFq@-S#GB6Di2;DRjgL;1qmhwzdxv2#S%&7D_dE0b+s90~IMb48QU9tA^<^z`{LvyBtse{#AdDZ#u1Ts&d=a8wwmo5{m|suRiGaCRRnMJlS~osLd(k;AA!_9zmPWWj`^DuKo!JwX>K{|x_a&U{1#7pTRpOApk#SH-dnr^O?<vC>7Md;o=!MCbH7uzy|Acj!-@kQlYeKA%lG+czTX`xcaEjMQ;1~v)BEGXYuMB2tL*EN7<;UmJ6HxhVZ%b0`>yTcNDdS^NX-Ag)kwd*0mhG6X?>G7LyMKK9?WaG!nIFFN`fQJv?6>z{zx{50{)R9Xp5X)U?Hig;%epqzQD9lsR}9tSHR1>6Q3+2(YN6Zp`!}w1d1|GZD%kUqrn-LH|DF91P~s0gfabMueeBlxXcx!s-~De2uW>tLxF2Z2UbPv|FMN(DtkHiB2sph(w{o&M%8>s<%O3&`tUD}JejoU)?rVPazRgy662IIj!3*%;VwO@nu>}qwSt<Jki)NfJL<iUS{GVU~>KB@%&7YsQfB&el1aIN%u%I;XAIp|$!ne6mTHN)jUSmVDLKLBM&p8zVI+F~4`Sy`PJmTo>aM;H>snpy*J~mR5w^cpjfd|9A_AQMy^mG5`U%&kN^Z)+&$$$LI#13{~_iJZ=?KFGM@fVBXV=Zbs<>%G6pNN~O+l=Uw;?-kAr2@u!KF7!QYaFX~O`Gq4I~6sdGUZZ2XZ!FdNc<A_mDypJ%;nF~!>5aqy4T*V6)>c4b8i}^54*0seTQKQqC&e#{rcx{DLvJWD1oA3x~>h{V?)9LuLL?-QtKJ(219?>-jn6Yx)4M-#vBdf@+4KQvG(0>{<5naRqY_xsMlO(Mmh!l+Fa>RzyI>vPrn}a@_xG4DGhhl>+G_G`!SY?CDwV12ytEX8!RjXb-}Tz<}fzxoPU+D#Ar^|(0R@k&6195m5T#>K+v&ape?@add=dI9qQs9e0nsk-<bCZk5TP<){T<P`9rfKx_xw`GAR;>(%h<TzVxhp_PsyXt5Kh%WZl@&#V;2?y5_m6&!e`@a=jKNP?@YEii|s#GIEYdqekN#a44qt=5CQs%$J0VRz#FhV^fKirq8~`4U@kO`x7j!$OSXrPp3%VxR0-g=)}mZaetN&^|j!OF{E|?msEjKOg*i)$B>pFtwAX<4K4Qr3^8;eKEe*#$<1{v#*O^v-`?N<{t(6UY)*qZu=z*}qy=<1_a(o5IB`BC+D4Qj+4W!|!GRhkx$VT-qsd&nE0e+05CPDK)~55o0rWU2pGcnF#~Oi68Ev9<G4BME_jQyhJwWICG$g1z6E7{5Czpbysp-kLk;r2P4~~Xlul&-m>PJmO6bjq!pa4yX|Cv;C^km~ShW<2ZSZEd&fxv<-@Y4CyIOYp#qADnBVm&@Q!dWw{9#{pC&WrnJ&-2uPNkBP3RY+ncf{pALM^y`JBKSAiRtz53si}HDl>mFO!s^tNgh5h=P?!fEn0;p%O^h}CtuLchrlx6t0!%46Nm+wI6s&*2OFYS`K<2h!h}QivYPReZ!=7b5p-Y5GQ&xHvRCF)zXD4hoW1<C7I@9Mbcxs{Fyz6qzY1a|d%nZl=CW$?#dF&a5^)5kryXBt-A0B3nG>W}&gEf7lH0w~~4$X<07cJ5yq{p39=QMY40<t?q>xQfz&^RRX`mAWXRl#7!Gu+eV9N3m7qy~rI%RIF%EoAw3e5ZMTE-RJsb?v8@Q7z7WC@i?~zePL}7n}OmZ{Pm;9;Q>yN3TrkTsTt}{|c(wYiJ}V$Kt&)^_<uI@0b^`1z{vsYDTn~v)1<XI*Kj%$6%KX_6*ypfOafK<2R2M80Ds7)j0F9&w3xk2!0RrRQ6}a7BtO7Zst9?dxM59sQix8xDUVJ8<FZ>!||YSm?{o&KL0)>e+0v(%Y=S`{t?LismU_l{@moX3DwXv)lqQq%+SHT;Pcn)6>qv=D=?n^OBJ{aX=U~PkGH2wlu{F7Ut8oj*C#ymND^hLp*3WjkX+=Qx%GBJ93x4OU!&<oK!}JM+xkm<S~lP?xBS?3&a6zMjAc}-xE4VI+iLxt2=GbG7h?H$3IUAZya)h#=J0xg5cUOI0us-_NH{p58Fyl4vw{u30z+A#*hJO9Ks+3&Oy>8!|8oz2cK!7*W%%aSm`+2yEQyLE>ASWrPb^g*`Myy~$V09mPQt0dY1(=M6-Fc3$Ik~Syz&ih{mHqWTiB?C*|6oaGtAy?%V}n~q?)>skKR(Kijuo|%us(rIl&ZQ+K$R-?Zxldv?h1c%1Q+YdQ^{yc81{@qWz7{8kt(io+a|UM7-gQn=Ns<Zlm6Y)P`7xI4rr#gw#k$*UNROo3e$PrWu+(ifQAra3AjpRg<Z~LbBBBI|^=^MWa3FFHrj=6Dd7#SxGWb+z+9>W7@VSI~T|Gi&%^%MVjkF>171mweXyJRi1s9#T}v&YKI~Z+)Ve_%|lV8j6-iF^lPY~v955?&Y<=gE`a`sY#A+(#o8ZlbQ+7SFlb|D_AuD}iO=vngcQm|j)X<`Al2yQv*$tg6QaWj0y6~!BbdZ_h=AT<nM%Jwen2h|Jl=-eAf`Gj`0`rAJvXo^fZ?(Mp?{3<BM!5&VnD({;Kv+R+2#YKXa*Y%^&oL>We(XDz<Xi~5vW=b;DnP2kNI4|ou(M(lsLFfABlWX&UNXV@F{_5M(G3Vl-y%-iBufX7n9K@z$hdUz*<#kPSYOQ2Hj<0Qn340R*{NM2g9o!1FRhx1|(6FU$f*<oF|o?pAvU+4>-pOehjR3G-bVpgO~X`^CDXxS$d=UL7XEzDpQw*C{)6L$z=^gZ(wCFWT-?qH$Wg5v<0k(5@oA|R65`M+tA9Ob}vApO3OaNY9@*`KZZ5;bo73LTOH35%B}#;SG_fy$~7Nzsa-7Yw%;G{U4llDROM`L04fTFJ3y;Nc3sFnTWi&@n@1FKjI2L=G!YfOUfc4Qx4|md<>f+3jk-y+xFR8hUFuq%LCw13Ww{*mqsr4-by*FWc0a~odCpwjn!EiuDX*K}&BbEs1YLcZt>MKW)%{gH$q7`k-d5+lz_+n4R9gAFMbBnw4R`SieVk=f^N#jex4pJL!dJ=6?ILM+K>~8u1GIF2UR{=mTLg!M;BNo&L6D8EXqnt*JTHCdD^)2v)|j51J#HfqYkV4DiPW+C?xHa@nQM0}HF)Si8P*pSqu^r7DSeD)eUf~!S5_B-gJItp4?a#ef_KZ#%O=NA3A`|?oqGs1)gfx7LN4qHbJW=q`y5VjgUmc%%s9ikb<PVoSg#&6(OXUl=7vA4fDrMu%vq6J%~E)jtHW24k`%q}s~jTKNTd{AZ(5uac@{3<s<{E^1pNtmdnu701#L233TTb8E_&zXsg85KfD-u4dquWEcJ67_|2ia4i(uC&nS|Uzk;OnK=PQzHTTMV26;d6s;xxtI^r{v1w@4`CCFJ(3M9qB{_mowH?>q{`Da=A}A{zJ1UKs@t;tF#HD0wh=^I(T<JdT;%$4qCGt_vvl^G6yxq@TQ*NkoXj_3cHc41#33#N?&A*}irpu7E4kw~1iIm`u-&l(~3#=eePhiY_<I3$d-EtjLDI`w`V!f~j3G&QvOK-lI-Al2&5EGhWV){mxw#;>Xr3Y~L17o#8gEGK{K7n1*3wz)1QRGO}t`8_VqaHPTzo+0IHr5gnz4(lo>^Rml65>hNX|u2m^Rk>Ot)yg(yD{Z+`hdS!^@VX@^<Q_ogzGNrtDrumMs%4`k9EPzJYOltaSFMw@yN<XE=#3>Fn%5uKWqb@Ox8tTz!*)?0tHfh+nkX;3e5h}X-pacWwJw_>P;3QfrgmMA?l(6dwFu%tTCpF8?=tu(1RDcO;ycIAoA-A0HY;F0My75ubQvk%T=OI|491L_x8P~349sPI(EOwOh?Ws-MlMMZEA&}#-(N&fTKcYv)qD(@>N6!jP)`8H~y*_pmrm=4mB22oM?iI`R3U5_u_{$i&m7ZP@#n2TeH%4_#rV<UE5my0c%6qwOYCviUI!3v}+<$xap=+XXIRa<bo?;2mcNx?XVU>B5$w{*$pdob0k<s&Wi{%{j^c*MU7yDInlsy4F7gl2$ahiyAR^{g&@rAL!HFPE+OT+diaosS9Y$6iQnOt}-_89CUZyZJ6TFXS+_!w;c7}%c3i1KuY>+*TkRJnbDWpYXhbE852Ff3nFa+{}n1WLn-76M*HGB@V!vL-@#*ik`O<Bs$Xt3=5drAtH9!0EM@B3ILB29v4kDU@U>L~04)vQ#oHTwVvF$O2R^OOXVqI;`sCNU`j}-4AdrX+HUXw?A9@9tgGbAi@e6FJs8S{Rr(nWn^P{u!XWdDaLQJd-|yihaeBdA$@BSt*{uQN+HDnClEotE1fWAZYJ~X-~F2C*78CW6h6X=s!Oj4*Nn=6zWD_kG}$){%_((~I|W1_1j@;}HC>y8K!6H?lDE`Z?kdQ!Tl%F5#<JE^eHzZG<ls_|>66Fvsieyhb*I+EC-z8R)N4!aB~lF(L!<BZ^shNQ%ML)fR34lBC*s_?=K8-KrO^;c%#%(+j{q(*7Xp<(CYaJ|GJcl;0B6Fd?xGYLD>m%}*5cZM0xWfuSdLlH!N{V{p(xMEHJcejyW&S)AN6C%Q(wat!^ARdjuw08qK_qtK7<5z!pkBV8i2G);H%2A$O5_Eo7MFQ6Tlh^IhI^3<<$cu7P0Uosff0wFw=-mJJ^j7uF9@MhCzwg`iC<G{np!j)+jX#G(=kWS4Ubi>JV0{eEi7Gcm(HlSWE2eFu1-bEQ^A1uN=}qu>=3ht9yx+5zDcmRzLhT-DoeK=5LK(<!^0a4mBt&EF7A_xOQl}+oXPzxoI1Obo6%j0r8TuIb|cyBD2y2ia8xPIPhBBQbkF?#zE^}*=AK|%X=Zi@QgAzxyTu7E4C<=8x_!Do;<AbTGX^Vz^c4`4^P|W)#e#DYH>A2@zBc6J|uHn`t*fN0>E|WaE4cp{ZlP?W!v)!_N-$FT`X2UAWuXI0K)s!r#BX+56J{zLh%Wrh|&sVGi0own}zQ_S87o)zS}wE+5zUpEHW;fS;=TBIycUpKPIvyI8~)Oanv}FBoU1fD(6fhatyB86N+Q!n1q38h%^Bpr2Lp$$dd{5vbAEA$R(^^kf6x1hx8ku9^twFj91TXI3W#YsledJeCjaD1g3GaKRSXSCidGq$!Xi-+6<iQ{H)d>MS&&wRP-Y0G4evwvo%GWQb6hQrQur*TP-*N2M3o6x#le3{znkDx}Hir-$i!HNRu2P$%xP>s&O070q1(^sBkJb4?3e|7)RA%??&X~2us%|rrm-xYic_+TD%X<<JC|;o>BDL0!Y$y$L)D6w_532T3c3S^%Q2#mlr8$Aeeyh9o?|`oLtDtmS}09Q3J!}P}2Qlpi4)&pA+R%@(|&MhD;cB%vBs%O8B939)<iin+lBcz4_0^&>bn-39Ey-^_MzsnPfE1)9}U(;HK$HFG6$lZ64F8N?SeIqRwI=d=Mp2p3U<5#&4QBnS6MURs_toYhfB!ouf;pQsrtT?NfdzcpPKW@wTG4O@c+CPD?jJRMx0v{p=r9vq*xtojJH;LTe<nh*U-(V{jBG!C#V)U6)4aI&IJOzcf$t*OaSj(;G!u^#v%9U!tPO53!hXTVTVUImxA`+ni^e3y$*ux~*Lz3`S|8K88Fe$ou>1_aEffIllN9V(qp$;p<0bNK#yDt}i*SiAt9X19^Abd-y|=3coIZn>uf5HIc%cqFvYYjT~~UW28|52tBNRA3TFibPC?pkd{7mY;`(7o*x(6iB4a%Y2%7+BKO4lBJIdgPaw)_*c}yg6gOJpCMyk2zMHg{(^MrPIH<KgNn{dY1?oP^P;v!EE1~TT3Gic<iB!Pi)o=ngxhzkrLcR-}lRc?(Lc>tYssoHD3?$r}GnDbnf%}%0J=ccG#IgWMv&3r@)nJ-{_cri4sN_X}kGMm*i$Gl*Sv@6#c{mKmlt%rG$C!$KR_gu=Ql0XoOcy7*z9v+vMP;97O`Sf$5bH+{CwbrQDwB!uJ~U$5E)g>M)eeZ<X_@QVT`!Rs=I=iQYWF?0Df-Mb9V&!LFnUfg&3mE^gb0iHLR0#TPY<;28Pqd;3cy}r7sOT$2moDZlRW3pwCDsxv5}dNb}Lwo4iyvR?={Uma9{2tMbE#zT<1?EN|SMCYw2p^t&2>^#?V~B2I}FGblX5fQ(fjh(Pi$sQ8?a*+=D`vUuW55<v3XjHIVzk><M)VU&sexH&Yz5j|z;CXe8Xx8WY&tB@AT9@#PKK#Z%cM{1M$1jkdpu-}W`ZM`y2wO^b=-uJXOO@6IMuqNYnlX$+_bsstA$#0ye^1DP0)X*tH{W|5NtcYMP-1pXL*@iO2C@D<ZE!u$+%9c9Csq4vjxV+_*dJK~@HH3eKe@8<bme5l3cjY$~J#Pk~RpD8Q~az=nl0i%Cq)Cw1s!rF+yNU`z*naEdE7+1M;8#KnvPIBb4NbB@=xq&X%`Y2EJx{*4_x`nEj6l4mx2F*I@4TKW_5aAzToNR~=qpo3b`Qtt4bo=njlL2vst79l%0)K~3!@Ldh1o4)JZMMLH5%O_ii>ZC>w^4Q>DY_%ss0b~5TiFAnof5v^LkbxmtpHyZFS5^pa}2jLpo=Q7G`|l6lTK#Ey6LeUXiC2>eEWZGg5Q22=|LPL4!~<$O{731WG*K|CtrkrT+ZukdC>*htCVpkb0vWw3*<YJ+ZuNJqz2-UV1PhLSIC1_5Lkmv$6Qh6tb~bT5~r@!+B-`}??U2TR4Gkfh>G#YEn6H-rYOp0R1wB|3}xB+C}LJ=N!qN@pP&1WZx6Px(Ly`T#_?leAsh<8%l9V~7IXKV&1lMmn^(1{O>M+{<E1{fO~)uZ_<ku%==GeP(KD05a60A{LD%9_7ur<JG2uQm%yY@cNE{&~EL6!vKMx`GJocKgE3}<C>Z<_<Rn0>`Og%G2+CyD;*+0R+t*cq;;h1xwq?}-jZ|IsaHuNRul^c9pn@)p>Tv95qUG6X{%<p-MW>F6)s0tBd1`Y`LR%F}&A%5NWXTdYC`6|-fm^f9*GCakYWrS{DAtihaY)q<~O@5dj(2~OJAd@la=&9DSM}eT`GE6F>JIF2(zs1)pnR?(y;Q@^L7a+vNmgsn%Jnk%MW+H4>J!eoNUQ|NqpCF<j;_5J$SFL}!47pYe$3QoVKRMblkilgAeGyZi@A5Ch(yRFa3J=(vzarg{5^V)9?=q~aRlrSI=Va4&iBy)s(c5JFAxZOv-FyJ_rK^^J!*n;jdm^tKB6^*Bb@*+Gls{_p?g(6>t27RMDtfZ?BXG-foIJk7y%<e1_pvWJqa9SNql5%3YPw@-7&fS26S;0o9rM{3sz&QRXV%?j(Jhk!@B)-)_e(EU(f28t#x{A7$GgRY3J^9aVh%?TJOnP^SQBz+LDeeaWe0gJWh!P1QB%k=F6jnK7MfE1&4-_}$GP=axE5D%A`@LiG;_gh2bfiIHXIdMqDgLg_#UIWB<)p7xTfV-=X3P?lXVD;@1o`ryk;RvZFhF(kb_&Mp`*%xG&i!Q&Z2i?KZ=~DX?!x>2bm?Dwi-J_Aqa_EC%wGxdFG}`Oz%AmOl9vx?~InZV?PdC@zn(1GR^<>3BF4+^wKCUw`e+{PwaVg9}|>y7~$^2uVNxHVs(;;M+#T(jk2oC%QJjqkolVy8Bg}1B*{MB70o%gY+~Z?Za7vQ33v6(ASfV6PrA4Ut)Wdq`0;GawCOt~m&5^b3O&t$z*T_x@#%!r91Qc9BE<mnK#91FiY1!S95H$DSl7q0#OO4V9-GHbxgpyvf%0fjVm8Xo@I@yM(cDFV-$RemiIdUzbspnck{X<6y&VR7-YJ4tj^6ypl=6@93ra-DvXGP=@NsPj41Y*c_1w>q*Qa1gjAXQ{(}yoUJVI@5;f#&uML$&N9Wf7QhkwpxH*{;T%HqdREFyRkMfzBVYINf4dF$g=2dM$wAO)eKnknG<kA`pyBzd%iJR|1~qE@*dP1vY1=vh>%-2=g@G^r5Gvd0kI=605s8_q5!!JKMRU|UB^5e&h+lu0IDrpqc2Nd+AnZX!~)TV?JPS`OsR2_;m}qRW@Q$l{0}lFcF<!%p^z+gP^LHPLvhCtjj|_jwP+?w6&6aXB-j42P>!Mu7!Gf@a{Xta^6qHDAS5DnI99dKdv16GHxPlWlk%K2pUdb$&MJimMl6m=%lryLIm<x*+(nNc_f^FnbsV+iP+C=KcDA|MoG{iIO5O8B*l0;zVAWo^>e;7Yn#7385Gvs<W%_NvL1W9}Gzzp_OPslx|D!jDgEW;fS>G!`7vZ*PEWpE6ekiAbF>WH}K$}pY&N<fl)l2#Az9}D!=xjHo}vQq;$Odw%7ypaPMQyK3E*PLl7-8%zknIVfd%|c(Yb>%MAN?WAx4r_&3FDf`y8rXr}N(iUS`RU5NY1o!iN7&s0K!rMa!ZI@Df85S&O0s80g=rm!%#IffLUrelg>v4j!IM+JVa<{+imo3ijaY+YtZ@IZuvni}zWib5zOi-#GX_$Tq*X>O4GV~3j7)ZVocT$Bc}cnkwgks>GK479BzT-uO+d@kLT%4d6965hJ2t;m##FWHLFN}R5}roiZ+%e?Q8cIA(6zy0*bH}k`fwq@TQ?dosuzkd7O{5*QDpyPg!p<KUdp0Q)imnbP``v}+@)_PCpDC{$j5YvKz@LyoQQo<&*YYTVb`4!((LM6Lq_6y=rd0&Wj?c)FXx8Gdk|KHrVEXR@@$Nmr&UC*vsjzkzqvmuX692!>F^d<WDI~-Isx-vZ6J+g5mtp<bB0P-0b4-fa>fBkU#*RLLCAw=i3CA}OF4)a!_f@M?-9~OZ9^RG6{-O-v!I6=`)Jx8Pe{^P?%Q!qHtF_Y01RsG}7z6nW(SPLh1Rt)#b{V*&t^#8Yi{`J>C{nzh*`L}<DCn65)an0h7orbQ#0hxfCVVPYk@O9PWU&Q>27QR2+vow7=G^FHUtf$dGw%?O~i)-3^2iz$|MhDXNOdsS-+djPlBEmn3#*Xpqu(W;ob@cH0EH$Qk^0bRS0qxK*FUNJ|9s35Cfi+6rus^JGPd;4v$sSwj71J;@jJ@zmpp#{BdN6Vf^n2qySzoLiz!VH!sN?UxD4Lf;{i<(%%YK`yJ+y<oE6&Lx8TuGfEx-KzuYddH*TY^uPWOE*_o?_021<z*_wla!y_2_ysG+EzVBmLvwH@xWE&W;ZuL_nJ%_$l>jkQKj*L|@wiF`oNv9TEW;IjJ(&X`d@+=DNVru7@^9^o-6$y93c4dg>hSk{JyL(~+ZqPXD5qmo(s>U)2#SHl)cDeSPLn{@3(bb4Ji^E_&sU&n)Nhzvr6BH_-ZRL(JJtZSSDj%3c>+)eq!d`Y<Gwqltd8j?Y4`s`cWFy-5@zaagU0*(#x47ou2@ckeTdZ&&*`>N{J_ZH;`$(cvlR)jlN<-j?Hw2HI_6_*OaluvpF-@qm^rn!zaxRL+(%lrF(NFC+JO}UG@LqsK`D*3tOpMRV<A7#<1Gexrd!9+n#Otw45iM2<Qxp-H#$MJUaAKIAC0|zh@uz4YQ_89Bnk~~>Sy@wjjV;$R1o6qktx`OUc;icu65GPm~n{sfBM4mHva5MzaRaBb>e$;qVp>XWz6DTwM&!m#*CmY8>`qQM#rCC@cG9k7gOXrVGxfX%(L%oHv33z?P#~)XKZS-4-)CNfBvD(ljSvWS7FQ6R2&&g%mQWL>Oc8p^Y4;fu*iZ3n$ULU7-{k{a)_`NRJ*l>n`qz(}S6&@I4&x^#4(eSsvj8~Z&BR56#K#*tSFv8XQFNttv?Ij-VR3LL(Fl;1Z^1jW17**B~WkOWS%CCajnyANUW$zx7|5fSCoMq;vg?`Jf%Q2_Dr=>TVVeM~{*mInQo>4^a5~R0VpfUL4liTaT8OP-Y1DS6ZqY8H$yF*i<=0%HivbBSG=f_w&Xu#PWqIE-74`>{c>E71?3c^|lLT-(x+|%_O*j5&%1BXA$Jhd(@lmtzDr)hsJD^>Az<6oZ#w>bClZsSUQ%qa#yKWyrsfBg8zyG*B?kKR1GbK&%p{43aI@=>GH3=LZFjakllP5%?~B6P`VBsP~2=3ED)ryGud#lT?K3ihl*npo)AAppx`l$(oH<DxONBZb8XP?Yy`Yzy}B4|L|5a43gQi8-JjpuYst)mzo<<JXND9D0#=a~TXDCk#E8xOr1Qz%FbLncab`Js<GJAd#h|#m7H>+HP6q{cwZ7nB_m$hfQn+&3(sAr8!_s!-&R!No+vo#MaAB3vKD~TW>B356Qtqhk;KkdfefbAG_YK1v9RLTgHqK3V^d_J0So%%@=0<bCd`^a9#|=IP>^2ZNzB8SHYhwj6?#InR=37O`ACb6(Cof<$@H`OPQqc_Z|CF>YmCB*;`stInD0677A>n)hoX6hLVRx#FS@1NTsL&A;x4mC|_Bi`me`DUgrjs{o>5d4QrI|qfh<_Um<&O%Xb%8r<$Tj7uoZwvsYyA?*98|a)mvk(0Glgz2+U8)+8oc?Q{VTN6B`zGptyz_E#G*GBwG%Ws+Mck~YRxSGZiCquy?%4T;XKtS8$%|G*5Ui5z!Rw()hHY6y&HcP=L@aDA6Z^^oQj-%;SwEE-4~Gi5qMiqf9Q+=B&0w}Ss`z8^;K!l?9%b;|nwlc-xpN4xjKY19LRg7BPXC5(Nyb&ynjutP)=Zf1Jyrdu!nQ0ypx^>-gIsTt6xMu_dBtj`2u6Azo23n`Rt`E*<QtSrD`D8oxjRaND+b{ew&396nX!X^De^ulH5M3QU}-7%JT$hmTY8JKRqm!nQA2qGPPieb>FVSLq~uitCOrv@Sf@JcZnq#Q=zO@|3sGd|&f=VK0c`w0N_R}3QQDbU5!*f0kW<St13F)kGKJe0E?$9Q*|Uzi-DX=iG=Ys&flaw9nw@Vn^kj6TXEL{ItW3yi_-XbZp#k{4iY88m$vk8FcvijW{o_T>r^s?))+S;qjEj)Vhcb+Xs2coe76)p!6=67M|A=^C8pXIeTMkiLzPG;`snX|=77f(N|*AWjN<2{NW>sc{sHTU>NodINX%LNcnjW2#$?ZIS^xJY`FQ$~oWs&!NpX7pV`qw<6O9D~~wV{212M)4loy<V-wIC<_z^Txf$PUG9&$EL}wCF%kt7UZ5$WR3w`kFowf>4uW1~*Nt>^v{nt*v!XF)EdTP+MEvc3VJlzW29^+)my@qI`ZsEEP4a`d)DGH!m!v5$0#UXa)Ug+0nQ56{L9wQ5%F<8hqt5fc_`)GJ)4Rq*$(1~xqh)Ih($_4rcK0-&jJXXY45P6e;6(1<)gxR$`TA{c(o48L0WCZvzC+bib0CrYM$c>=+<atoMq)Q?j=^;@cDu>SdtC#(2_3N1l*i#S?t~(BQ{uuQh*`5pZX@ut_QAt=S2!iHq|?t+R`F&x$QP@pHW##FuCg(fMLf@-mYl2RQTT5#nP4>c7wHju<>erJ7j}m6km+=Oct7j3Zg%9?#lfGWIa&yv>&CSr4;OxeN%fv+FC-~?keQqH@993(+1FVOEW(MuQphY+@Z`VFsI+CWQm#KsGg9shDj20JGp9LjFggN%UzM-KTaw8wMZ0oWnHImZ@Dw1w9$yRXmf7I#W;@HY@P8c=s6VjdSxh``Qh74hU><)GQefJa0(Q|MjWMfCqyA=Ap@=_4!j~)wx7Rhjj|E%(N(Q@=%o%~}^7Sq`E}D^IYAC0ay@c;QN+VFrh%JQZ$OoKz;=o;)5G%v?gV}_a-0Q%Z_My_lq(jhh=e-g=$f{4fVyf`;^n@=40X}L)RFSVaFVw}{?;UwJ;N|q~B3MJFoA5cI8K^}Zli5nQ8>WodW>PB`xVE1$%Cn_*n(=yOsxqhV+91y2StThagbbv*l;UU3*?(@<%64+iHgdiVu7rz+&Sa2J`Wq_JN%01T6L1ax)^oO#lV(K6YNhN7x)ID#FO^DJE4485ZMLyu9EU-}ME{AXd9d?M$*^H7;%2DNIDwfRlCM5<f5%vDk_BQAqPJE`SYIs#u#-t5dv5V^PMm;JpWhcK%$ofSwbnB)H`e7tZr0I>)Vc2<ptJ_hU{2>fsJu3C5I=m~v5b=d{8oTwK885DsdvUAlGwsL#n*Z+U|>eVx!~r;N;Y-jRsGh0`rpq(AcH>WusVvz)H>#|3RrBF2<|Df$CC`bbR(+cN#Lt|6n;dHxOE<lXpf#1n$rVuY<hj-CX7ShCMW=VmIF4C2M*oT+|Z6Ope{YVAfllwPHv3rn2fU;I^&xH&Q$ht$FzXe>~xHBhXsN5>_gYYqhJKiZal>nHt{m3Bet5S!R8dLa(7A;R+Mqd86}Sb_c7@4H7d!U>{m@Hw*u0FF&;)tEN1c5`P?&9($GZj%&pE1Nt;EV!vsu;5HRPT;rY~Ku&cds6i6H`6Kzmr2>fGUdm$Uj6CJ6`mz7xUP7KDhJkK&wDzb~RrcIG&FSk3)b5SYY<X~goE^Cjphpp<q9_3?xSS=<+l{%GBg41iCXS+y9vzbf`&tVcPfoo@p{H01~a(NRZBMVToEJYD(n~<TCBgL`@o%*-5|L0+U_MYl;xViX-N1qNuxn=ch%-FH!gzBwHRKmiBs{o`?Lm&cscba0t+(PC!zdK8zaVvB2QTPSRlWDyct{E-JW+jbevTqmxGcTjvG+^Q*P);+ghsGct;VcX$+IgAm27?-@W1iY)+-hdsrkVdSm0p%jAt$N6+tcusknqN2=`l6#0sn7AQ_H>9FrCOyN)RhgZ7|S(xba_TY_Rxqm|#iFC%o<k_SkB`fK5?pMA9JHqg{#v1u$NfzSI=iU}R%oyO78D0U<L+xKwi(*VR_=d`@m=P*U4mQk+iiT&*>)G0S{fOi*$I1a2p?UmkPVohr4&8?sYWVZkBxCM&yN9mcy#LIIJ3)=|L^67m=s-vcYkJpaiJfP0R)%=*D)_+?Z15``UE;<v%l3LhZL@S8c{NQ~g-dGj^hXe*NU<_|yX&EI6UNTg6#UW8@@DYV;Xbic`5g$)+3dz+hpy289A3G&P$vm`8v4iY>sh@;Y^>|6l3g3hOTn_MBF?1hwhL`u7pVg#bC*i_O=l?q`-P}Z|D#c?pewNEAFIs|~B6=Vh`HA%HiXWsUDzOCv#K|h3L6Q!*_Pxe0cX#~mK2N^ERhP=@5KDVN_3>If--QerM)fHTT-<IMu_oV~dhxsv5bfc4?anves%Ho{JS|E?K%0>!PTqGd$XQEo_x%P&XxUEs90@L8(NukTWOG-VUdJ7H^ux=)4s(WQb&UTkg`yjoV`N)hhEXAUe=99u!9a*u(U=fY6bg`bw0>`|GjX399lE&QV-YvK3RmCt03MsHK@Q(&BW@(Vv0E1Z|SBQc2H*1bA5_#=Nw`W*WBPm$L-~JJ)+>Lpyw(~{$WJtrjDne&D%jH(<pP_n&{J#6-dop@hZhJT47RMF7Y$)vv@_YI~Z^%8Xu^fkJkmQoR@JhH%tij!e)SW|Dg4B!%HD=9=&xr0EV#&~jzYQ&St$TqgS0jsKSZ5QdX6tR6&dEt$sRG)X#xx9+O_|P*fvz2uR8II!=?@I!BDn{ap;jVbIozj)UX*@_p&fWY9(_qMp6|%1jud;c3|l2vj8pC0!~qA<7t@dvKIbtGu6odmeX}eI!^ciNK`6$jrfwWNnMZiDh(ZX)wFn(_{GfW1TkP^8ZJ~UsP#mN5p@62M$YomMd1_?KE8sQI6)2So@(aeJZOwlAxNvu+T!+*WATO&5+TagapqWdL<}z-tLGzoZ`RCM^7A*!}!jI%NC93vqRzE%$II#VVcCF}h&Xdnw#d*upt`nuR?!uFX^FmKkfg-)H;Lbt-4&6M4xOCeb`5scS2l>+=Kmx<R7fMqpZo^R`&oh=Zay*8)xy3#T-cfs8RAsr64;>>_r6=@^<_)<F)zGOawn(b)(jk?-xikkY7CQH-n|=~?@3<${7gsAs-E-8A=}dN61J*7ZDdvz52PZ!*7ucDOSqenJI6&GkN!P6#$%`2Kx1=CT-OYJ@QPS?+V9V=ChkL=mnfI9QKGudJBIItJK|*%*(pPHUYrR)Y><7@bT4W}r;Bq_GcDcEXC4iZ<LwSgxJ`$ZRCpUO`ikHDZ^%^<R&rjQ5CtAij6U)UtUA~=o`xw~l5>vC*uAF9sbtTGKKlXpIDFt{p4Y7WgV3ho52Yl=_-pjqas$!8(KRyIX_Ow*RUYw>=fbfQ?mlZQT7vT7g+5i(>Z``@2oj~v?DjTR~gijiJH5}E9rQykkXX!B{^a#cib$+T)wbM;$b5{r6vf5lk47ntB%6HJMqlZu&>(nPs${iRAM*FBXC0yNXzAZlSoF!OmlFZPib#OQ2bMYkG6pAv@!orAx#$>%@hQwG&$DbT)-eWmu8d|Swb9<zXQ?*dC-V4-C@hZi{jmd+U+#|AUo6R0rE?t!Iks06+Tp)?1qZH>hhZIwA(=q0XYoe^)e!mH4hQE-NVmwumm$bF(IpD!IxD`rlT-w9{M!qBY*}s=Sedpag|BDZ`xxBjH`b?eP6;+VK&uPceTmTgPE2D0{=zcAY41^V7KG9kKjEdLYE+vZ2swqh+d=(9o<{-v}Z#u2@W+{@Xzi(1Ujsh?NEmv44zXNRqfEFql;BZhJ6P3kIFeg>v$)pR~?)y{+%)SKq4xfg3yV(=OTPpiBfdgY?v1E^8eC@Zvb}cE|pxEgKEqq&h0;3%ZzTZ>g6(22ufYOV6TA*~eodKY#5z?$U3|Klz$d=8I`9N3mb>Z9pYt!QK3yV7a7_sOw*p@=d#6pU4-eB^D{N;8%Y^(E=(>|VxJ6TJlds(CBIW9aT-tMwPrZm8WT>%78zIGP0j{fFuK4ggM(G)BiQxqiLC>;LYS+;pMa@?j?U~%P_kct5L3IV-!WQ3>$L-wTFlGiHkcG)r7G|caR_dkC;S=2^}=rlgZ$7ER=ibvbGP3rvAZk(9uSP5pYf-Rfd0{O<PZEX9FQFah-Qo6zG`8#8C#z&v@s{1>^vpQD<%Rc)C1~P5*WH=Q`xl~&k)3Zk1mwl<271}SXnnl2Qbd%hjQ{?P-%Wiu)7@%}DOCDr2`Cj{@oac$}=)Gc8=mXE|Mfg@W_<1uQ^2EHCiY|~E_`a1*lqtX=YEHyxfdc}*rHmM0pkDU<Rp83^d__p^f#bH`UgBvo^fA2z;(8m3VnJgb$_xHQm_cN!0B^Y;;Y>5nFpa5V-LWX6i%S+6C`-NEX$Uv2!y7+uH9&h}5E@B`8ru@cyVdHt!h>9IYcH2O$dY5L@p5e5p`-Yi-rYTwxRK?YBSn%SOCPr@_{D3}gwOC}Bm*TIpJM1-Vlz5V%;Tc(g-oYJW+rzAYHHIYv}C0nnQbIDWVrQ-9@$D=;8FK6&#pBn&3Nc@>1lTfL)(kKC^pp5*U}(&hzXbF-gbpPAPjt}tT7Wij{T;hLBqjucVCv--;ZJ%G=#v<_l3Kez>&^9&odgj3GZN73PLoZ2%_kfK_bKUo!<gP{}}&TZX{!&2^Bnh`dmD&dN1zk)D`+RXuQho0GNw42gOk=rndQ^n#KWH!gj?-?LyqP4*QE)W{d%%#;tvK6g5BCm_t-&9fuclAFz2mf%C@$^@1LJmfJcvW*p57$J20Jiojr4?d%2nICE!E1UgRt2eKM@Y@X(e*GAv51tjIaa?rX8-CsyOyS1Ut$kQ>3vc=*Mn7Kxv(o0;wJ@GM!gvhwsP#hw>Kn<UvcQ_aFArDh=_d!Hgpb4ymimXjq<MkS8d~nn{ZvKwg^*#VDK`#^Fe>9L#G`BIz{(1(BDs{Gld7$)9C8|I(np8VJ56|*Ky$0|Qvcz>7IyF5aq8uf3pkkfM9{7!Otw%X^accLl9CX3}OmVU2FpZ?Erpa#_z`kdRQIccaJ}R}!WBi8T2Qn@ssRZ2C7~;VXSu$t)Ir8Nt7zU#T?COW0<pFqt+R*uo5~kHZQ|KiLPh^Mh&3XHMYjC&4AR+&}coa>}N9zr_2Ab2>N6rkQVc#H$;7?r;FXV4{b3iu3%NR38O%aFsCePTZ`Bu<7W}-w8j7PJ9Vw#l;6T`RVoZn#UQkLM{Z2u@rY3j(#qfM7em(`%H5x902xI(VUTw~znAt;rC!y?=^mi8F#Y>SY6SXPUWg(ev#j+kXjy%hQr{UnR}_mqm->=9UJ8G<uQ%J76v?G9M5r}*B79?s`%?tXsjd%n`8m^|we8o;2|;Ho=GeHTNWu|%TVVfMU4tGC-N=JKxJeB7XaefyZ{Na;Y=3LWUrVgp?ps4loMoVqTy^nWHQkJSOI4qh^)F0ZnxZ!t(zo1^88U}FD)?TKiN_{HPH@K@RC{!4Z59;P42QJcv}iC%KHpV#kLC>1X-?F5qW{HPFFKWZC6X?S}jyDOIFa|Q0VrI*4SXADFqykPl|g}E(h6v3zIbBYr3!aP#O&iO^^bKV6c<J2LdF}jk|=PouFmtz=cig?|zwE{DZ8NCbG`H#QLMdPF4TEd}Ss2TKDWUM%OY(;2F+?QO@Ae+Rl@B8zi|Lw=$e);W3`0(?=-?t0b%lofC{vJM$Y$<&DkH+omH-n8m)_hf=aYT<Y1A9KYmlqDcK?qBy4K8^e_(~a@(5@}qh1XYnbIBj#n#C{3YoC2#+O@CpJ+*b=BLDvDhv8qpdYFZXiwBQ>*`*xjt-@!=`aE-^6T<DG;pU9iOxE>^cIvsH_wPSGDm;L+%swomD~|TZpM4Vq$+0Fy?5r5>wZn8+Wbp8B|NQH(fBLWA|MGAD3{ONH*yEbTA3F_QQ+PKk+`}@vR^aQZ$G?cVqO4A=aL>{t#?Y{gg0Y@P|JZ&{OeL;q^Br)f6mbs7oiVoUGkNm#3gD3M`13ogCtZG;o;ANw-t<PEHqBrwJg-SZA{m#Fw*eX*lGZ4B7vQkYJ=rGZ7JGQ9YawxHNCx2zKnKZc2xhId==a8RxxSc}gXsXeP{-eWQC}v9(o~=LmY6SRYi<X5S9DlKUe_^%{lEPEuYddH*TXzMPWOE*gP;AvA!Tcc`*>H<F3HnF=*`tnu;LxSvJDL%9aG7wxl;v8jOG*#UFJ*C*mt-uc2<iI2>LM=SrA-yKiT$7Jbdv6z8sj=O{_bB$EbEcM@;F~^PwfQRYOB>X6j5(JYH<h&a8d)y+7BhAu^+MIoPjFIzS@&vo0`o9<^<<v5}CdiPh~<;M=*B$`>Ym8;x_o5ro;ByD1l#F9{c{R0Oy~!(3!dpM8rPrhFUr7qmQ(3uYBVoCVs4?=O+kJ9Yfov65<u>pK6Wa^A2TU4~e!FIR(vBI_(IQq3=9X5lh1-Dk+@gNa0l5q^Oqun<YXHDyG<ehAtkCV=LRu+5&1X(nePdoTr$`X7IJfB%oKCuCn;aReKwS#S?anj&E0#~ki`yqK}v<5Kuk09=ElsqvKSq4tT>6IfZv-KKAS?k7VYHTH7RqfTLQc2~(C6Brw|nGc7`A1U<sXd2#;THS&1)(fox7-K6Lk5fL`VIFT|y~+&IiIi&~IVXnJV!o`C7&eW00KT62)r`OG7|yI5cd$U<oJyMvY*+LN9!~<vnC2_HsHsrvN@YQd$kSs$5<e&xD;hbWyqa`9*N>^pN&;g^+W819GEcvLin{!9Cg>U7++rPnLAxw$<CTEX?OKc>1nm<JY#_I209AmZn47UXw_iedXzM)(9vcMUaTOcD4drMcMRag`FqA5uKE@DqsnCp?RVE8i**-^%U=016E5s7E$51D?Cig*P1ZChIM+~5xR=Rr}W<Pxx?a?z~K)7@ZJ}O9=!viia=Yddpr-%pvBhJ47iy23F3}yYks?Yen>4vf4VF8s4qF^biKrwh^B#QB&Y@=2WeKC$V7}uv9fC%Jg%hQ_T6fZzE&gWsY>tC6Vm-{La6#X*7<T32YmXyEPR$8a=kv_J-=P_E@CdxExRShqX*I!!bx9qwcbJ}~l$Kzwn5)~}w{T#(K^o%0<;=sFUCFH;#pWLn@PSPzm*i(t`)tfzcbSeNnXyUQpeP^!r)Iq4t?hpmbFqgV<2&a2rvoVM=U>8VhJmsFQ=fJkIP#ie?%Il-jor#|^?XQ($n3KdB&_4hAJh+II4@cfZ|J!xPa0kl6rvCZIkAJ*B0spWIaz1+V=+32>7pFed;v;VJo<I1;oKE#T{ZGsb*n)SJ_nAvAK3qAYr@@i{qQPL-3ck9+I;qoAS(*rp(oXSk`4uWP#$tq=hk0DEkAHL^tO;Lq_>`Cf`T_b&U}4sRa2>yH%vydHc{i8A@NvS>b5WQ#^#km}a$ZZe0>k-$FZDurVje$jx5PGmxWQkn2A}K0Cbj}1(PO5oT^Sdxw~kl^aB!lR?U!NC<G0@ItQHVfi4FswR`j^TEkAa>UsYvX2N$~&af2Xp#CAfUQkySK(9bAg>)^b+lKLWAh0%ns0uLgLM1l^TdXix4Vk7C0E6#F3id3jf@cH|W{V8=%Wri%rikxP5^^=vfDV)J8SYDg+t(74#kE^f=I5e$Sk<{AP<07wf(|Gja%+3wFE6~Fud<FM5k}C#+v!=e0<8i47{o4zBclX~%la)?^Qu10*$EG!jiB`*8^hBX#yV{w!nMBO2tzT7yM%t-Kf;W=_#-jsFQmgMp48wLSZAf%>C0yCoM*wCpP2{+nvW>6nMnhBvyK@LDEjSz--=#sfv%KOv3S62+18HNX@n)zu+7p?38X(ZE;QyNMhtaS%DuG~~vcCT$MD*yW;C?vG=m0nj&uLb|*mqm}N!15C<QU;*rpIn-KxQ9h!6)GEdl>&ZA}X1|(r35;c0k!OTK%b*t?9Pf8uu~!WzRs|4Siy#+ucSQ#>kb$=^&GrrDms_?-lr17B<|Tj^$|>Up0X1_u9Rw!3o8X1w>EzzTh_yCM->Vp7$glbGX|kv#sI^E(}kvE}q7QO(wEPr9yRrA4|3wRI>xecy}6)PZqY-&1`a4u6;jUo7ezyXg4K_zT=zz2x(JsfC8CwJK6$JfyB|QcaNs~;*o8TKM_KM*$G`SL%($=yHky<j2EEi4HK0$D;~vZbOks-RKeSma|$2l`I(lEF4b=%g-soZX|=77DyP5xAWjOa$eK4GLXmJ;azSY64cvPbijJvnHH}{efbf(u35w->^FN0+E5(<ud?TtvNA@LFPH?RGF|4VF;@}JTn0TI0o5{mbSKj=S$Ml%X(nU`n`&9s~BVbV|6_ut2yx=g>qn0IM*NyaTv{nt>w&Is(&1&+|M9lhrAt+zori>q#m$TwG+C*w`O@^Gf)J}DtmvAYNfc3BtNbf-_c`oJr3hFamQ<knlA9bGp#n*JPDfl&pNNR6JDcbQI@Ya~9uX$%IDQQNQGz&8zLt{(88Qs5&TB5H@tq1vg2jteDvuObq@nxzeYXjBrH~MPpP-Yg0K0k-|uxe^lkTr<KuWNuep##{N_V9j2qEJ(CN}M_b(rOmT?Khm(K7bW;jM-3mvdKtd#hcw=N1}rSQb@V@7;~PDu`J@j2G!VH<d6brb%*}cFdNoMbbGY`ApjQkRtYit!yV!jtJAvKv0woc%Sz}O2+eiuS}~Celgy;LH?&`p)Huk@)x)3Gl&AYtCpBT+^bw-_m1bt)gs0wiMy@R-q6!aKD$=7hAfR%p3x14O!qP~@C$BfH(Z&1$JuJs~*9r#TZ=obw%V~#uw2XI^J@UH?|Mb^Cg9~UO-m+I@yV(H%E&gAJ1ZpbmIu(<to76cKB0xVQNw_Tq{37&as7J!{gZ!IW)g}HE32yI6=5X)Sgr6FQLS+@<JC70y6m4NR5siBmuZ)8WVcNJ12oDAy9&FjFl4L6Pq0;@ML(g*0x{}1n>QK8+qr@mIg%1XyF=|En%Y6-foR@C{o=e}JffZvKI-lvS`5gLIy1AG_j%*a=vJWZ?SN%gik?`4^=62c@mk&uAA#@xS0Tn-U&h>L6R<=ur(>dP;mom-6BQlU9{S6hhwp5mHO_YG<bGDO{7DPv8rF;Uq^~n*2m1l9Kwqm}`Hn@u;DQH;doA#Q&Hs6#ctW7crKX`h@%%sSS^L~!irWGL9KgOP=1oPD{q&%<Tp`34=^V3dMexF-B-;~}1Y$j(ZvRGLUxl~<MUkomcAd9z#^z59@dr*1kRL~xtAKk<Bxp3gOW_)1tFuJL7#+#AY!aODSL1f{Nff)(nf_oZk(bN}L6<7n@em@VvYO_@Gnk9o$ur?!&w3!E$xa}#F$CC`bYa<%t0nSwv5I>?v_%n}2*hbF^&A5U1Grc}>6UL!$6BNEY%h{UP0f%5|Ziu!R)b_(7kmhhVc%lf~KXXh*Ne#~!mVh&rz1%Urx7vG-QSLB--=2NwniwE;?Ci!<Y@rJ;gE}Iqd6MkX6$YQnw<L}#iu2`kjz>ZI81(oWdE!s@t0t8b0eln@2#B~x%wnnYxt!b?DzA2C66c1N%p#0oveZO-oHMTQgz7Qa)!sM?1&)@9w&XDk{V}k;kk;gBjnw7KN}_fz1<TmXvrKS`te~txQ|#Ew4GVKa-zC9qChHjUc3DH9J#1B#^+*o$!)kE{zB@u8j@LfVc1et8Dw)Ko!<|)v$IcSFO9d_E@+MeB7NBNXiXvJTUr=_WSoWY()tsjEANFS}-vgrnE+Q;R&8X}Ck0Z4A)PjTM!4`^9n#aNbMJXiM&^aMzYZ9$We#2B{Q&q3r)hJaap0rByyT24#$FdLwg^#c-n({zOVInx$bZT!HO*1c}-K1b*7f=Q^EyKo?1HwRXrq~4KIWLpl;!vYu%u5rD4b4os!1B}5%Zn*gkJWd3TFw&M+?eb=rp7(^|BYyHxz}2@6SZUsn&qh()^>25b6j$r2`c=U;8sA_MDN7FI$JFuuq`W%s2b#av{Z4R05+`BubR{vj7&BA*m7U4b{$|&dN<4T$B@Uq9xDd_WH1yjLaq7etMbu}G;hHdA$be{DsrGikBO|d$oF$%JcA9}PZhytF~@wZMI2ey+~UoWC&>kGHRX$ScMuK|naQq0g)@lQ`lmAm{k_lm+*JY-NJ6x3qYo-(Y#*$k_xvZfbL6vjZ5R&Sl)^><YE~j>Fvh~$%4$JowIGsUxc=f6e5%u+Y_!SD^R9-U<y~zRJu>8JtQ@Yu$Z%*M*XVweIb|D!IrO%z0p*E#OG+u3{blKT6qzMBXW*lx>HE2WhXy@u^ESC6N!fcSGtQJ^DMgb+Td}G1rYb7K+_9{DMmTUfz{Pp#o*uHx8*PbWVvFmsVM{AFA^74kwY5(i<~m2_yy2{;$*@!HEt|K!o^-CdfzY91DRmQB3K)OqU2%*E2s0?k<<zmzuPU|1!zqk?dRH<lNcI5c311+im>a}D1-u%%P01cnr4W<Pi};EA(t+B=+%+j~*-2(P$}5Q>J0`Lgh)}J9u<8UTGJons<v9~YcfoaJR92)&{|oG$hZKh~`7Y@$AC7yq>SPiCyD9&fS2K1=p8*OFSxm#&{L&5*(hgRNcK(>pavN+OQk~UTN05phTLIhWsoHc|2F`VQRsD{_y$XCNel_$M`Ajp+ONr)W4!881^>Y{5Q^DynIEvgzmsgSXS8LovoOffstL<r$9yda1p<pLjmVdd`y5Xp1C$|GWVWx}%m)qWrvB&YDFO5t4{Ah+ZD<4A~&(icaL}#Ay{l?Nv(IV^iI+pca=o7iL6wU6LtDL4RB=A5if_)uXg$cMeNxpE=%J7A@1sXyy><uN!KL)yXl=L~VJ!SbY?yRJ&ScY1?gr&Hj0$Y^Ah}mIammdv&F(*(;ImfW=sVtpVkCtJpB-e4?i8p5e56xF*F-+v=JjTJ5qI$8poP|O7AeK6Uzp~c3fgHz9${pT^rNFmwEkbi@a&*a5)^4~Y=tGs#75Ta2QJ~J3Ea!yoN*xf%XFx7r6->Y%vS3b^uHa?dUTX%4@7zzQQ!P!S5aqi!5I=csiUK^$D$3^q2R_Krt~q_qdGguKII~^a=VYQ?oPOeC$Wwt<zpqUHL4KTrZI2-?-8M%)6I39i#2%J9UDLf#;!4pTj@o;kNuxZ$Ne*wBHn)sO(M)RBJt?1@?g@`w)q+@=gf-2^SBz`BIfR1epyx`#M>AL2BzQc}Z1&%rj$PCDq;4yBYx+W4<@GwnxiO9QWP_1t%57w`L%tW>moyz-%5F8&C@AuI{X`Z+gPBQrj8clK!0<rYa7l5msT)eA_nb+bTZFq0_MwmrIn6UP$ZlWyyv=*9O^_)|0VZIJcSn^Dnqcj7;LFV=*8!xr9Wqx0c9Mv?IT^a=W`JcG{5!4j4gJ)|{e_QZtdj;^{Mx1U;fL=DXO`LJJZD{qIU^2hpp~<J?Ehl3U+~5$V&yMUEcsCtc^R0#>73STGh@Uox{aH+TbPrA6gbTH?y`o(&;IxjsHJ=5m)vK_-=wDdg>d<)<;HC3g%*=68?Ma+PqHq11yl`RH?T|CL5Ycc?r7wrZaRDfrK)<X)P{)p%O@apD4KR4xcHC3A-5&oo%2(L0wJX=GaF?G>;UFhYqd$x7_dt0ryp^F`=z={L9^7dPJI%_+&QJlIfZX3<-Av)@RC){Y>iYQs6*&HkMT+`;7R%|RI}oP1D{eAZF`~wQ;Hv@_IZ`aWpdhi7xkQ}@)3%Ms&IDOQw8k?Igj@OcU-(gF>7ZMu}bj_vSFJ|WGb>eq&?mRbP|MQa%zuBNGKpx8nDUjm^fq$Nb3PItZ7c@eiN=8e`YHv2k;e0V30{(co>%ZVB6>l>pm_OV??I8NBJdbv~eh76fM`Y0;)sjNtXW@X$e?)8lLmN_@0_a!@2;Ur~0gy-W4O8vr2Xjh$|(de|1j#RVi_~FRzLEIW!$rY%Dk?Ydx9s^aB2js`TA1_se)6XYalW`$;2Unt0)gC*w<vk+61ltjH$yK`D3_kTr&N^1Dq(fX>1nVWf62IeM3XgpYU87Wt8vv<0V0s^(Zuik&ZB)1=I%gEvriU;`i0NT$i|<7g+g!FJ~<{-@Z(3g4l&(hEjA7Tj+XIAhN)Au5xLeA*jRXykPDw$7kjmF{U33PzIFRW9TwH$Pkl^aj^`YX7e-PsJ}RwT)xM0yelUg+!Qzo90yW<O})B<)$quRAZ})T+o)WilbjEanb&Zo;=2Om(5tE0VXsnAoTU+2BCTN&CKSb0I51z!6Y&n*{YS?I}57sM%Bg?h_#bxGfSoc*1!B*I-+t^$0vJ}WA|_EfVY8p8e0GU`~UODlPzuJ=1wDXd@R{f^r|7hL)|JV=9ca+o6%T_!LOQKo7+A6#_QT_JC0FyurX5(*XwyYQwl7rk#IMB$J4d<VW?hDDl?r5)5I-SgVS4b2C3t+FBS7aThLWQ6ga1@#&hQs-;&ilrfxek7!r83N<GwuDYW@pYY_XrVtwe#&dYrG`ktTEeI7fO$;vPRm{<0gbDdG!ly4H1Lt@>)kpbUQ)(+?wEc^Z{mh5}JQW7bGf@ZzFMCN9Q3wxQz^)?i>=f*rMAn0&m>apGkKfBY+lT{;^HC=C`+hQP+S;TM2)nrB&YnLq(oRVs&f$*nTl;t%8-RjhxSzH_P3Bboo1Q!bIAw<94O&zYcT5nKdj~hLv8UY?in7RqYGG3?&0@mBwtI-1L9J)O8Gtwo|_XMg+>+S9u3fwq&&bEBL*q(ypxY+<)k~)+vrvNk9r;U4_r-$*{3%P9xa!)SX;ky;e4rK{rb#I1SpTwc9%L$yY4;vldhp6IhKciZap)Y2meSWNi$!%6-V=e$D$aQ0SrmqH8i(2-nvg|Q4A9*Q&XW%@=ubiz(O>*}4shIE%>5}IQ$KwhRIbDHQwUs#H<J&psr66D@Dr8C{0OY!!9=um}b~|UYmRo^Yh)QKspFS7QbgS3ICDg>REHu~A3<fhGU{+u@HCXkVPy!1R-TY8qWB4rDTuz~<rOl3k?=RLNFn*7kNT`$RlwbBF5pghpt>dku1c8KLsx~iTyeao8IY{I1V%85*pd`IzadJi|!py=`V>g)NdFIB^%<?@A%%x&QZ;hA1V;}cjM3k=>r~mVLzDv<%ZFI6*2w%6fZ#AJeE@om;5pG#jH#5T&N+|4H&F%H4^csdJhD-Z!vR@zXj?^DqF0&c%G4i{QsJo)BU{zn_9aFqQ%qmQZ7la2cIVhn9UpfXebjlaS{sxo_fx@mT>~_-}rwN(5Xz6>XRXX7fjNaob(s-k}oXJoI0<6X?a{*rT=<jpkW{78BB}Wo(1yI=<lS)&kDbE!7wDmDd12@|52JBMD4o81iL64WZV*I1RjZ;~#Xmc7)A*Qlgg3+=`<cTUUzNOGN<-1er-#LSNTD)Ip`9!lb;B*kNp9ev;30c`9x5qJ|`)lnm^{+bQtwmQJ5bBvAA0hBy4)n>|bpC#nGEVN)<Ew3ycd{z|cy6I?;PZ`qrQ<1Q_%{NH+bve?uHSr^-+z7knCVFAJJ$+*=g(sAT$>I*%Zt}^{A+>sUqiRX8@)sg-DTX9F~P;c1=0FBFt_ojEXU$r{NnLp_^Y&p5i&GmSfjvl+8kMO#2>Eb?Uu=guTs^9k?@ny@S{T1{7C8q6S}<;?{eYj!<5}`OD{z?W{44;$%39i=2f=j8lcm3<TCHFe##swMxpsd*>c_mq!T1L6-JovFkyhl6t54`F$^?CyzV%w31%9j+zZn2kH72A^*r}Wm@bF=hBbmKGFH4?wj!YKs?gujoF5(}!`FD<pAY?SKmPX1Z$H9^pAY`NT^zReUw`~Pd>+|S=o1`ZA7OQmHJ8+95xc|;?AZr!@k`(vga8@Z;93s`S}9`_+O>td@cN2xZijeWv-kyh?XxeccYUgvw%>pKF#hXT53`UhF%qZW;cE`_R^csU-CeoS2{HT7aAihoCdoXDcIw&D{r4Xq6_z^enH+X`SVmWU>yJPCCK!rio|f2IG2Clk*|5l{;@|%H*I)niU%&t5-~Jh%h&ZsvHH$xX8oDOYZ%QZ+%j{Z#ud5#aB4+ck@I&FArRkiZVf_SSJ&pdc{hnAzT+`+|;7%!a4S-u>bk}DZ>FE^^va}aIqoLt(gujj+KEGeqbWfgk(eD!;8eYJ-uDngiXrQu2Iq`G2&OKQ;<tK-qG3p6JLl6hA1Ugw(A0g|}L%%oPllA_6^gW=2ljW(0^+n~FVC}o#{FX~Cr&DeRc~>MlHuC%l7<<VB{POp|{_U4v4}1AI-S@E!f%B_9l*S?M<6ZTbBySPnA6GxYfHk0)KHOCki46E&Y&J;d6b)VGT+v{7xG#2^iw_7oHWuI=F1w$7d*+h8xCdVzP3t$-J;GyDl6uMPamt65u=NZLO%gS==ugv*8D;IO@BO)64IvU`&A^Usf(nknnYwh;dDJ$)L;$h=h}z?tB>$GBRL(KM>^9B;2iIh8?xuWVz9gLTkw`=we|@h{pM8rPrhFUr7sNJ@3uaYEoCVs4?=Kx|#K5q>s&nzZ^}a#!bkGh@;f_`NZjT|YBCSDH4}#9p6Zfr2e#Gk8W18z&gB$sezr4TyhZGZh+?2bhJ4B=*0H!^b{PT|!=c6s`+bNRW4<-sS7ZOSxC)OTK=Hfk&6@ScOyxshVHm38y0nEsBUr3%k#yYr-<yKPfL4N*N$M)0a^Lvc0KssM|Y4hmT4VK2HbvQ;M&lx;88iExmN-hFFYP_jXID(A@fCc|EsU-Tz#&MATG{KZM3yWBD#TI1g{IMz5B3xr8x$7Uegy?u|Dx>j;q2EflgF!masSO>2nN&Hz6)a{Zf{pAL$08mwy3{$!(d`-mkL%c!Q(sDejo<5njZHfuNa_%^E#ZMN#*RoP6Agds%XpQkF}A!#4+MEO4(CL%Hz4s2x?bYZP6aZz1;a)nVC>r*h;gztaW4@jO<DO>P}9A9oE@q0!u0i2Ix}xxeQBZJvg>lpY47PfiDp>)n<Vxer=e#Q(Yplc?N*Ee{PD@fo^#?uxxt<kY_C$>xua8|=0%HiT8EZ+=f_w&xCgaVFV8_a4#{-yYnB0FEkww+##8R;dJb$W3xj~epJkp}mli5eCBD<Nzm}D%_`310&x2c>vt;S@za>;<xGMMOA3y%_F4HOJqc@N4TsXT8{|X}5Jv361W69o_<(${_KQS*t(UwMHa|!;;xrcjta0plo40f$x&nl!W+1KFhCIHK0l$(oH<3!a|rh&x>d2imhU?2ZLXRZlJTlkci1Ns5_OCUw2Rn0zr-8iSsR_bmpgW=<Zq35*PZ|Vowh3z5AIFPmH1HKp}RkXDD_{UG%ZOUF7!C%bspX<XWwt~K)W2Vv^Fd{S5_sUp&frAsh?6lC99=}Ehn4s_w2X%B9__U(O9d7xt>ym&vce5K!U{c165DI{^W;-DOI?Wem{d1HEK5$+P#5nW#GCh}Q!dJo1CX7S^lu24#t7);Or<K7BkaNzmL(1(G{3yTg*q>7ORA$KD(vr$)cGtB~U?UB4@r5_ogN3W7G9VdH16th%mKf9LRG^k5+rFL~dBG_;S$VGK7B+&a(Mx{>w2->5C1nXp0Zo}C2P;udi?^=bJZ9*>n4H4{(BP`7QG3lhHmyljwDOPwFiv#8)16`Ed$qsXh>@vD$`Z4aUQypNwwS`@`W*FkD{V-0e`ST)W)=m8F-`5bo3f3stMEanJiBuUNG6B?8*iq8{;^EsI|^l*MFWXsCWm2Y<k%CLd(fe-Lb0<SMmNK#MAUQ=`~H)7B1T6k?89l@1I%ymoMuIheYcs{RmHGFxkky6U60*#>m@shJqEBM??Wgx3G39zL41@6;X$<Gp*3^b*3vDXZcCq)1;`9#cxmyfVq>S<YRj0$;GMl$aX0k!nr@OCk;oXZG()Zz3kKo4FzP6R2+@I~7}k2aDaf@f82R@l&kPXMz=ckA8pc;2m-Tz!l&JwQ0W?*NRjKSS@GoF`*o>7p9Q&BV-F}YRnz;aQdh#3b@-(~#1Xm2wl8mWEJymwu{rc=Q+}~is^p&#n$lOilL}$4P9}DPW^o~b=>5(p|=}lvr_;$1fSP02cu%;23T#ZMz!C6JX66VQrHCjGwCHw47jY~)J1L+3T*Q|IHC$*GuRd`DtvaS{S+Vi!XmX7wQ?_p_V{?4@8*5`#RviTrR3K`1OdLbT^u&QwxLg@|M``E)D=X9$HnpuLy6v#v{Ll@59X}-CA1dtgl@_?}7jbqJ^VNE@~wO=sP#IuBa>T$q@CT-G#|Cr0t#q%4ZVn8qkS~f~0ys3eT02X!<1={YLks6QIs^Py?oa~IwSw5P;Qz{hM^5tzn6LERDh(g00uNK#&W{69@%&*{A)A6!26Z)w0v@SlWy3I7L(NF~DeGNR9t-0)9v&<UZ)4VZeHSlGWvx~Lt-_;#l!1wwMZutug&Fe~~kpE@lt10C!xnR@lSqC@o7$5rB2b-gBom}W{lEq%v0B=GEAT?!h_>AeGTJDs%M+jU-m4ovZ;A!mxhPe{XTKsuR_PC8n;>~U_FIG40dy16w^rzFYEUw^k%m_qa5(WMSlL<z1e~}omSN#M6cVSN$4@XYNf_Jh`>t;t)1uQQs^k?8X*F|cX<1fqxlj=IrUPw~hATu}X+|zxklY+BaR|FD&rDvHN?kV}55nsz;rQB+k!lSGiTojiiQ?8-leXStx{l-b6(*+tpvXshQWikAoLM$O|;oLGCyxnYPnHKmnRcmmFyU`=3J=mne6Ff9uQX)SiS+y+%)S^QdV^(lR{mm@<AAgE+i{cE{UKJL2?BeQI3D})v&InwWuXo9D(KOxawE1~T<dMLZ0LEP=rM#UnZ#GY%%VNele5Bf!J?_2qHbLJCEj`8I7>-+gCJuxs6_*oT6ks;NYm$9VOsMHPlcCZ~rZWO%3IwG-;SwiLJM%P?o-UY{M+NLoUe8Qvkfxf_tx_Z@T=3cq1|X75oq^KP6E)ra-jP%Vd)9Yu!5T8jj?WF6&!KN60|zsdZ0qQw8c5xP0J|w!H*>YzsevuVb4c=;2wsZvvCj@E`<ZjDpBu5VT{<G9`8K#ZKpvo%p@ivgsE9*76ZOF@JLWby`Dt`OR!YdBdk2xDVc|T&AX3XP-)0+L$iXo*zu-S+wa{n2DaB1}58Tqm8DKI4A`2b+IaZsOgIxCL=9elRS1SN4UQz*>Tg;^sV4|G)_eGeqCd@-@3@ki~V2O~_cT@{?(IjYYtysJV&U;V=5vHCV&yQ{b{9HKjTLIkt7~<&GY#8xOVhi)!aO-h^ff<#Gf<qqR1zj@XWZ3O%bw3Y*%oadL(-G~Z)-eyfz+$TkLJ#&Ko@D4<8zCwW@~(<w_z^u4uJdSwuJo+XqyY%Z)9VvAVI2B4L3KD}#RC%#;xLrW4O1OMPt(&2A`!ac<i@y;$vCT_Gm0|cOl2>3%yC%VaK|Wj7~i*NAG#(UYbS7aS-Q^E%|7C$c^YgQ+A7_vgvLeXubhPRKt>#c9$#Z0{mFjSq;eu4pB%BBh`h(F+B=_n#;+O*-JMDKx#9J*7?)VmiwGNY$|9bKKL)$n8%NRI(K68vR@N4A3~Vo?c6kybb@{T|yxktd@-y=+Q@SE6D8Uev#p&f9l)2%*lYnZIwvTzctbf)XwgL=zETQ>fwa7PB%2Vc;POp8Q?dmekOEUdLhkUMtc%CI3n~LMf<xL>4EI`e&6h#1Z!k<r$6w4lTN+#2$tcU&C%J+a~-=Krpy3&%{R6|l8M`-VXRRqg}EmZVLaesg;MUH`*=v@DV-LOft!h(uhF4k~45JA2>omOFPp)!%*{iV<in1v`Pe1x^)6sQ2#j5d<s$)-@iHw^unm(lJ-F@ZrSCz}?hV-f-Zj12PSd7134l^Ty}UYcNZg0!ZT$-bXc=_QsG3aaY6Jzaze?{rM|9#i8U{QpKYxZG=9_=)nWL~rxd4C{6YH$EiollFvTf+hW`;GGztdnN>%F3L<Js-}e_+NC&9fL~YXSIr6!MyC3=R5p-nSTn|Y$J+wjb#v2-VYkhBEIbf$Wkjf?uITGt&g<kBNEvKaLf6w7lZ#uKg^ECoBzD2mB3T*$8!OZif}io2;A+DUpUVLmYTtgKDNHX9N7h=LmDLI?ay@x}T-aVyv}vTr6I_Rcb~7VTAr_M$w%n)voX=g|bf6^Dy2jWALN|xe*03_>^Pk)@Sl)b}wTs7EMND~N6sTvVlBR7zc%4~I%&eM3eiyeglCSATyFNWHbNE?a<|gy2qUf-4*aqWyqK%cK`%UJYZVc`b9*9bvBEuD)@#~h9nlekx${8q5O<F2|50{oV=0cwVXg-~{$yH&?UQU^jr>tTr+9ukNO{ITT(H-X2Wo0-5#M1#T&YSr3<Xv8Ko~5If*rVI;fpI>}-`b}>b)6$~|8Q2=B$cW*fzI1rPs&#vM(BF6l7oDnPG@Bw`?Tj|f{_dtrW{|ODw$icbcUTZG}Q1-=c+xLA81bQ#dc0&=>Py@W}_4W?PNh66(l&3^BvgN0tK;ETUIRuMH<^^Zg<7Z!o{1UMtY558`uC3T@EWIyCi7^vgux>%H-H~5%Qt}vP<q4*pi6-e@5z<_Lz{qIufxg2D>!R-55zK7X9W;&!s5l^H^<kla|}`s<tG>f)!YM{8H&L@|mWeml7Gz46ft125O6JxZtEN9Aa+d(yOrhEdBOJ7<M=2yV`CRX?G*UD+-g6l>nAotuc-&;&MCS6Qs%zXu0j(0DK%A`NGq*<*(AO{1)LoG&Q#jk^s0DZ4I}H5vAz*>uFM(HWPC4-9b=47dZhUpZm2P`NPn3qQt~HBioKewBqxq+a6g+yNIbxeFmU%wX=xJgBuB@1`D4uOy_hZ<6@zmgvMhG6GgQ?j)ATnPzx@3L5YD3bE%!hp;pmhDfcJ(1(Z68eja!dAB~r$E#S^0qH17pyJgra$$p&g;$|E;$G*Unn`T+Y!By0IvBjT-n)o0pyS`ypHaCak*vZnx`{NWSI<7@%8cvQbnabJ?V+H-eQq(3tcRbS8$*1L<&|S%%B4Hg!o2}wF_(K-_?9#2hjN5BXI?WsQbLwVG)4)|Fjk0PnlLX$F)tk=+4ur9z&87M|=gFr(<U~_x|CxzGa{9cFAx{Mbi#{L$bG$hS`WWKUZFA%^LA7|~PlMP94F6szt)+OB_p}E|(0{4dY(5Xd<`yd{rcCXzC+U^&*Bv8O^(9oR$XoLnTBB2ba*;|5r9&#a^l2O`7CLt|o6a(I@3@1~7m_Of)nP+B54ddD5>3uuzA(;(gOi_@3S0o_GE4m)=pIWOCe;))r9?->JXJmCd3{m+^xYs_?a7c6&V^;Z`-mZm-;jHA`t#XEOW&k<uk~Cq<u$<XZIKw2BCMk(yev1DsR-bKJ7nMpMkUc`bdqS7hj$tLGp@l9{e<TIg`#DwGcaA8(WP~~hwq6&mZ`|Yr26^Y9{4%w6zc<I|FI-nMb`nZ#_Z}kum;zhY>D+|%QG-@kkqm)HsK2I)gv#$B|s-Xs)9-b9eKVLO<NTsV~OPeyH&&Pnor7{;L6{-i)EHJ#p6Q&is2RYYF(DctTvY{QY|-DiYRn7Wr==mOnLrz*(>;U=mUUV!oFv$QE(qJA9d4ICU}e0i>@|A%wIl~soT|bpuxp|3=TPW@$Q_TDwLfmOP=J2eS+KP7iqOw_88nw?4BQRg4?8;l-2Z)c}{)0?c9Z@2ulTzdzY%(eCK@DRaPRjwU>pw7~zyX#w-1TCrQarx{FT`d|XvR!V_&tYJGms;lmorsF>Ul-pW5``k#b(MDsq^Fe{Tdq4xr%VZ3NDjcM`&OL3t}8Ml#kVvM^YSw>hJT(~fS<w`Dx3ovJufK)0sW79G+rP>xPX_mkQ+se_kwA^pPL*%b@1qTAY0@)%m$!6q(ZP+U!8n~E_alz&u<+rAh7o%Kf6wts*%nlJPS^i_BCDiX}o6i5@i)$VY>jHe9^RuFIS6qV5D%lA)uBU_k)j91~Y1!qzyrzrl5X@A8+u)e2^~~AR`|>mD_IDc)A=3spRr&>eNLn<RC=|`7qE^-yI#nM>X_JD=6j=^vM#DP!{lO!^uTkwRhm-1<sDx~Myo-j_kG$wF*mzPwT>BE_JAA%@+s&RJ-cs2`4;)V;OD8+XqvhBJI|iVbsbaq|e3{w`IvDL(@Yzv}j(xp^bWbkwX@N|MoYTGCI-`9BfS^S{7?4_*+h?&^Hb3eI6cyKfYX7gT4#qDm<(Ol{qT6a)3K=#FS<Yn>$QSaL%S}5mid$Wtg*Gl$9Q|G`v=<NN>G3y$ji^(wG{A%^#}|R4_<_piK2GfB<0PrJV8H+~CGOOO@114pccaQ<ifNbc&l_nue}35W1L$Z!QmLuzskN0iRWd}CQhxva|M}y|L^c|br!_e~Cc!o6EC2dPy}@*U*^I_YuzeMg+uUaDH(noS+i{GtgD{-Z3}4UFnLA+Vi-bPIzfpH1Rra_!vu`jU-%)SMnTe}Nb;s5me4RDwckD~WOi*S6)dL33V=XmZo+4+xU3S|&!Enl}`RSqAOyS&|ZIAEhy<$}8%gn2N_*R~u)Y}=WlY5fT&^uY@ayNy;M7fX{EpR}<x0DeB${EYPzY4tjp0AWR&&Z)s>+L1_JVPPg%N(w^p@_B{^B7(bF~ihh9aA^E)67##BbU!zZ=>5*AyQAo9m#c!Mi+{gEfbuQY8iqks91O9Ie*>ERY%>e=L}}W1Wlwq3e+^9N&B6VbAv?RdaHFmCHA;c0;^FAg7l`F{uAJn#*<%fYp)g%s7mN!&d*40WDo8IIJDmGu35m);&Zm;%fxmN9KOv)-IBDPY@r1}!9ES<^E^FF)n3RuOZ<OwwGL0MP!jMGo}7F_+@#^wC$4EL!U8AE@2Kg6QI+OD^aW(JlaY0Hxy_es%msJ@xo%81_tl_jQOiD6mOW<8BhLo#1DuD~fh~34t=ZqFVtP7cIG(Q;k0L;vbcIQk9KSOfzMXSk3POpZdZn}|K*H+j!7JK`rm^gp&021DW&tUc=Y9HIJkzZ%7?<i3$Fk6ONb?oUfPh(n*}R6Xp43D)KXBKGJ4>FKvoUH3y<_0}i^T+twxcEz>M=WT<vp>EhhpS9-a6_CNN}iX^CFC!67!OSG!8H3_#mZA(ohyBXM`fmEZ`36bB^bk8%Hyz_cSn<z8AeUUcQcf+;<33c4D0V&u8_np<tuO-U9COyx_ou#a=`NO8x0|T+FPa;v2J=erB%eEs?GR2M4-|zQ^Z8un!OBYJ<-{oTS;uyQ57B7t(Ace3+2C51YF}t6+^^q$^XHf|qVFwsJ{#@R;xB@04Bn2DmBoNCS#zc<dKvIgaT_z8nS+EHTx9d4Ok87GVdmL6f4_;gN3+P0`r293it#L#Omu>}x?;H7G@`(lvb1iEA`<$zb$w7Ing2+MCBBr%!=ek|&%dzi|os;3Z~gj_GWyKTTj9!#709kYOPyJmBmSJw{Uj`O>1XHoR_CAQI!k?drn%=)oY3A;)mWN7L$`DfEnlceBG$&s!UPLvXkC(IJbrcnwXK<9e^{G5W1feF5YLe1jx{Momtt5+Dr&9?0}~*?C4HEn-*0-qm($zWGU2D%b_Vr!=)7rfMb?A`)&nr#9G9?WK+ewtciNk=Fa>(IyC|D{Ao1iPjD<lMZO;I@g%!d8Ep<0p6MB0ILZdBb{xL)DO#E5iaZ`2W1#pw$w|ZHQLX?sDB4#I<KktF>V=`Gh^y>3$vdG2F&SpMLGoQe1EOywf>bZW93r_J&;fgd7V}C3X&c$u$H+IFR6khRxMi0dz|G8DW_5ByY=DF&Qsp-q<oZ$ckXeBVXO9ah76TDo<rBn1-_G6Y4y%^w{+^|cDqIF&-I%R`}wbLA2S^(v-?_McK=z#?yJ+wnJp<eTNKYo%SG&LwU1NNx_M=0-!v^f%W%>3$N87O$}%wQr;|9s{JX^TFh7uyTYs^MoiIV9fT)?oadTBb+~#KL-oSQ_VW27EV})yPV5TvHc0u3&@poAgV+1#O3Aum;6Q`9{WURPVY(;1W+7~Nx(rwVt?fWyY?{7c;_RDWS!iS$t*uGr|qu+o1@%Qlg&q|nKZja3J^_#(FA8RgIIU}By$-1>h;2g!{habNV!3N(u*V|YrV-wo7g}d<jif=CKNL;h{Mf|Y*!nA7_GoD+7aFPGtfB*OY2QuEL$p')))
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
