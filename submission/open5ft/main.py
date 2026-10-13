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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_NkvK;td_}mYb-<kV1hb-|BBH08vR6#2c2Y0o1Az-1!;!1B9`tLi_omrI`Zf<TKS$%k}R!?m9ba%yvM})h%x%t0-^MCx)fBWZe{<r`1uiyM%|MV~a^`HOc%a`B$^69tVzWL+joB#4p|Ih#V-@bg~%a{N4pZ?|l{^$Sx<?H|S&0l{1kAM5+*VpfU|Mv4YFW=n$dj0g}zfJeYi}O$2<?BEFcKz|k!}tF9A20jQ{Q33Q&wuql^!V%K(}u7A^4A}Jy?&#9@%7Jq`uT^SK7IXwZ(ncUytL-qzy0-k{pIUF6r=v__4nhbzbxJl-~RjGe_8+3*FUtb=3|QcuZ};xpL6j^_aA&8%Hbn-e~x|DUw;4L$M633<wrjM{&nighrKWA;lql*5>D{PPv2gJ`I-GMeieVt?fTp2w=cf^6ijLTNp;okf4E$Cdlr7XUcdYD?>}9CeEk`iNV#5o1YhR-^XL0tbG}pTPBf&Z9MZP1z?8tJZ9}_#`h5Mh{OWC)$g=;tuOm5p!sC}8e|cMM$yTK)zT3m$bMHIqul3_+jw_VjbZc$W!rC8tU%#3iKKvnZ{U85k&(q;^w|m&kd;J5u&)cp@u<+aMvLAslDD892dfV-`%Uphbw9H*%nc05Z<t~2u8S4)AnXUW#Pp3b)bQL~k;oJCQ$$G~JjXi~Sf?#3617a7nV(G}%tsj;80Q*;zMFP*vsYNP3DmMlH&lO)(`8P*P^t{H{cL7ft*f4y=UeLFdC#IYg{8q)2{g}i0Z^B=(5AgkW*MCy}$m@?kUcdePw|{s2_45xu{_ww-cijCi!5_?cyugun{^sTy6yJusyGAX$AAM}Ejg!h9zJ4lq`0<vOo~ja}d2XP$x_qY2M}sLVxA%5*ZFJ$jOu_{H&oL`mcL_cI%*PB9oZnO9y<bc3w)N!EK5mCI7rS%rPS`p5tWUm`RXjzf_U6gYqTS*DHI%$-@X|++l)2nP%qe_tDWDSDn0<O#q|F{K&-aMlW%haDqmPgv_V+@&APZc?ou`)<K_ub$<kegqg4AjPH}TwPC37Y5{K?fk>oU^8hLcBlFBtCj2mku%*Z)ulXpmLDTR}~vCN1}U*e8Gic^`K8P(_SuedLqo4V>P?8{j)r{(gg(qQ{vBC-}22%`wTqueJ&^p?5F<5W{6<e-Oant5FF1L>9n~Gjv4A@%THz7YWy-OXC)yFT%1U(pR}ufa{F}FS5x8CgA_<XC?2oXMGOBl<WiJeNnd!;L6Cnymrm)fFEmdcx37x$!IT3bRL1x=&dUf*MDU8$<7hKv(e1k7#iBAuJE+Vw5<3PungYgE3(ve*R65zi{%6_#B==;G&jj)5-uY*(D)J5{x(Dns~n+D|0s5GK#!>NJficCC5oGB<{$XuC71-?bO$%k561oDDm)10g+2bROJE8AzPvZv;(|;h`Lv2>A9!uT2i3T79$6*r)(w9G;&j%xOZr<M>}FMYSNGE^p%@`VX4lwH-qd+lMH=n7Fp2N8)`3po@0B=4$_D`;NQGaOeq8Qr4qOrLRXy3EwVsHVHmPw?&@)amW@;*i1RwVur8%|QYXX1)#7e+KUY=_|hn+-OR%%L$3t`WoV<CW`bt0KbfJ^W}0?wl(U)kSN2cAda6SE*NrTud!R-b&%cfY>=lJ!hL2r$&cSsVyGmnX0N`0&`A^T6WmDV)DH$|pO28T=hYy(#$8mFYilwQPS5&d0fUo&*`5O5NRm*)Gv}C)Hy-NlzPDWQ2{J_W17ikX?x?cs~~w$9&euq`5gcXMgv2|MvOUPq)8ZfBp480^3HBLG*d&CI--nAOV-)iCMUFH+#*Ow<EqkB|c!Bzj(FO>cj8n4*q_RGd_wsBlV-Cd@I=ar+_RzrFU-xb#4oTwkr`!&qDP(ZZ*u4*=-0;R&eZ``J5y0RVB5x;<`MpbSAL~Jq7l>yIf{zO&_}slO`c`x)|U6krYVRsRMTZ!!Ahl0zCnAE9B1M{#>};P@Y4!zaGaw!UJpF2CyRb-=gV1eA?I7AHhJtO}9bR>o4E|>?)?PmrzFhWKe!6bT3H#a-)0~6|Fvgo4&Vp#*d|UrV{x<_dnp|5^Bit=AYMJyMF(@M430)43HKgvAE2WRvbx7ZfAqJds(3376j(4K*S&SmDq1Km*M6=5CjLZ@`+KI+Ly!lmSvV|zYe(<pW3(omR(j_bh@{@Mp!m*Z7GxxRx<4tj=bpcjU6a>OiCiZ;MJf)RbYa{Zihd={`Beds|54_xSys!!aCNt`UcLE9_Hx&MB86nnPQOPREWL6N7ouF3qrZmDpP6n$}4+iyEQ<r8;?d;QFH(zae9?#4$$$E_K#|(az6vZbas&Og2*x7xwX02k=2CK&{t;@l|bd<oPf?eD_!Es0e24~ywsfJR^4*9k~iFBnkdb0vbns+R4ICNko`Cp4&tXDe*E`emg{oaOUzKOm*M2K9NPUCY+&!E*R&b&f?~LnqaL$=0)ktK=-%wzuP+bhudiR(D3?EKKzZYK+lZ1mhcWp<e_~P2m8@F|lDDAw?&`X7cOW0T7O#5f%LAMfd+v|)4Fa*~Z^XGzyLlm$UmJj0A39u9^Ewyyznx(%Dy5jAMy_`j+{TAe3U5E4<&R93<!+w#A@rX=`|1U3PPQfwt1RNXM<D7_6+`b2JyXGfwGoF>>Z<1o0Adi3c(-x*3xdYu0WVQlMqhR`KB}-4dm1eK+1}ZAeV9@7qreK&gZF+Tpn^NME?>*-vX$h)M|m$7m`AdrgauG&M8!jq->=m#YU({-G%U9;HUci{4k}UZiSw;s_%|gTwMl(_eUBvVJT;8>+3^|Rt|o;=K2WDsDuN>*+ksNbY->(wTQC?Bd@KF3Bgef-!U;g?kwlY(PVejHh!sca2ojJx>1}MEI&i2s5$sHAw5Iq{6A?X-$Y}mjEXpw%mnN+RaR~3(vkCt3e&~EKy^<HhLHYfd0X%M(HZ_X7w}w9Ykyu_I`1dDsl;R(<tLw{4q;0+A<EV!}+j;8ZJg-gR0%+fe-n!w@<CkqBB1M&qeE$gKx2ey^*h@c3&FviVBjxqCM~RmQFeEd~a_4+bmM#V-qab|okOnN;<~Fsu?wW;7Y%C1i2U806*m#ze;EC`$jv1gQfEBe!LLAPgl8^cF2%TwZX8|sfKs}d^m4JQtq0scC>l2b<olY2cP%fE_MN)s86~6)cU9@;5rdqRl_K@u93_defbT5M<!43H@BjNFn`no)@du}ZW0_~o4EG&BlZ!xBh-v9Z1JD#C@?5pP%J4~dhJzG#CvcXHnD?l41$+FWc{3EkZ5Cv)ST%Zz?XqJT}d6jmIGn($(%L@d;r68jU1<j!cnOG5t*o?kHOrESd!BC$>{Rn1pLPs%X48KGrSZKG54iiaxtl?FYWM|rQCk&)zeCaYdtVzqB)i9Pzq=0{Fqkp?AakLl6c)*J8C<u&nr+J`vWU$IhNgPreBt_Aw#Wj<WoiZ8_0%M2y?ur$cWHLbBpid#9bJTrk=2hoEhgM0BH;93cRP>$;p>m^p{}Z!7L1EfmDvp-5DVC20r56zmSyD0MVnlwtYj60PHMKeA1j(VcSqfX`7<u7I!V1VBk*(ESzRVo_t9ksR$~>dDA+7nPz7OJZSu6`smLA^{dEGAgxD!?pKMKqv$WXoWR;E#9BW4s>%qnyRCHGXq15Kq-x^svZOPD4;NU#=9r63UP%b4=*=Q_pYFGH?kDqLXuzE$u20_H;Hf@(j#%S~2lOr*z`bDU&Mr-U<jNlN?TPbj6WNF0X(vB8nbw3jh{Q_y1b``6dsu9B*VBJvh~1?2T|?U`_k(E`K!d(8&iL<%(d$buzkkm{HS*5xwh-WTzNk{GV%W)&^`fe8zFNqMv&a+E8-j&da4&*G;6D6vF5fi6)k?4)+Cge+XTmqL_XBZEQ-%VISTgKfFoKd-?{juux(S;!@5TDIrQmL&`9;uw9EuAU>CgV%NJ@t2)4L^EKzK<F3f9|3CmVzvI(l(HvHsP*o~`@w-T%V(%P5j+xQbL^%J+XO}6Xw;O;&Qu=C^{F%2L3&FxuG+gZ6HZDlEwJ>jZ8qUtmCOwy!iE_U=k|Lq)BX0f)Pf3Q2TSi-S5fu7gus`}y%a;|*6K6K0Z}mwpn3CdsjQ*R>}o(-@hd<P_+ia7R(PQ9v*T^R-6I9}x43>(*&Fx55%Nn9ekHi$9~a|&$b|_~elLJ*q8ZR&;BBZ&bp?jq{B53(+mNNkVdXC<prlP*-&gJlbqOF=vH3=)TG@&)8}QFtqmaMI)lrh-WPqh_N<O76i)vYmFF5P|boD#yV@+l7%)f!uuAf9Z)P_E%6}Iw4t|~U<l$ci|Kn|P=`}P!c#fs9956sqr#<N+V%~#u6@he5EN*3jzlys20GT&j{3zEWlVG`nfN!vI@TBpUizhS`(A1n2BKC36Jiu1`cb=iDMz_zjI;{gq?+@b=DUsQFQm9F&xGqYWCqWt#G0Wfb=RF0UWu0Dip?Hz5!oA<F9HzPjY!!eqlbBsiNO<sQOC`+<pf`l5FYGkZIoetMhUQ?Kc&(-JD7ixgG5#b0xc|g9&;+OJi)f)iykBSj!v-d!?C{(hp+B3~31tE8$c!lYHAVdi)M@TVapaAdNXK%icKVRP2N#fq4Zcqa}A_+7ss>lxvD@crP{-ig$*OUon%E}w6(pXZmuD;BMl`h~MhQ#a;uZc7AiD{iZi?dhXcC06<4>mC8!g_vrLqmoUixs?x)%v;C7jaJ3Z$0@E>D2K0GN3VdPFCR-HV(s=zuUdFrmZc9m)t^bQ3EL1B9?B|`POANETJmv{)qE%V@6zqnFH;nlDRahNNTG5hHy;J-VJ&F)j0kM1T08*VH}v4vxI(-7ImglVodR$N?8Yoq@vc*`k$EB0$!fFm9bomh{O%DYWh#I=f=q{-77yb@rG75LbbD)<}R)zp^6VcN5R;i{U@E@3r!q^Gqi5bGJbB)X>=nSRp|DDSCjNbR~9KWCU!sIUO=jEP6XJG0yy;AqG>!K$zAhON_Us=CUQrc*M<lp<8E=lwffqV+t2cQrqZiIu}Uyt5Y#hw8dW;wn;rw2qrF_f$g29)gGG^z(PM}vis(MX-T>60smn$E0ciI95~trEtgPoX-Hn1-T9p)PkGPOi1I3aOG;zz8U;zmeCW)oqM<k!2wB7+ufE|gQ38304sEeT5#qgHsG_VX=T~q~VF;U%*el&eXLq(4ckYpoTlrbBmvV%pAU81xnK3`|l)kn2O^;H<~0!og}%ln51<6AI~uY;UvehI6DLb(@joPC-w5EVdD2@kr`LiC<<XemQGr~&a(=#?%ts~SNR$>2IA1g}H7;Mm0DKwjfoUPSZ~P-?+i%371j{L>h=Md_5cAPQ6ITd&z?<gmP7SUH(@%e1wz?VT86O}Ju|J5R;>TB$OA!cJkS8Oo8!l!0-!7GP7#NyrmII!;R`AYGOxwz`2}m4=QKCPg$0ewt`T#cN2P9-~Gspc?D4m8#8US%_1m2QMzF%KIR%9@ER@l?=2Vmz1f7XN6_Y<aAJRH=Sr|9;J|SwXyVCN<lm<i--D#R3VXEv!)7p3AXT>-02uAWvo6{D$H{`lA2G@9S}B8X#Yr@ko;Ew^b;CsWzLAA`#@7^dcTIccJ)cxQU=T*&TI^xf4p3WJqqCNcI%YeAT<Slo>!_TT5z|O#e2{;*|e$B4$=w^al#<M)P?VF)G6Y|$Za;IpYgkidi4!Ga266{@RU&HNLt$X?l3S;6Tie#iIF?Zcso`-2?T;l$=7>~F;=#0d+1wAMZs&X-tJhU0*uU}uhvpwl|%rhfvJty*i`j+n?ggaKD}^1j3-o?LgpDLM6N`ELNU<@6g_{EqACjQ@X7Xh$e*0_YgtZ{>+Db{AlK{!ZDQ!*5Z(d+dczA;6Tb!I6OEOi$u0{1G=FmMtEHV8u?=s9aE}hpL>=nIC@X5$kdnaQ<?B>VhNVP8BTTAny8F&-68&hhAEroFmI+*$#wv9reU<^C<YuumNaDtgFq*q1#ZqVFiC%kM??ofG69C}qhedcjU)>uPHzL--8uCUT0<Pwd4<}&fe<=}O_nGjz8_VoX|92#1n_^_Z7@)FGtmYbP2;eZfuab-O)fA5<??#bROWiVQqDsXq&a`DZ-AYk^+_J1-c1=-I&g2tnTEku4+INj{5IUNq;hT-UtuzZo0?qx$yGcH$!5dJ)H+n2l(>1C@uZu5+H)u|U1=1m4T<kz}f}_Xq#DqF1D~0t0cb?;vBIb)Pv37LxGHqKD)zkKfQD+K#gwE#oTLXq>dt3|9GWJ}3iXI<REH;6=ify@l8vs#CfIcCqAjKCaW=skWQL{d~Z45!$&7DkRs*hVi>_<zjc)~m^AyPn90`-L#wj74nl^20aK<v|u?L(`d3A@$VM?qKM`R<4B!6}oprlMXDDfCoIphM&_9R{69K<xH#zg%4RgCbQH<o^3*{Ew3WluNc3=>~FX&&D~-8oUAPNrS7ZDgi(*?TE?{CW{Dcrz?`rYIZ|@Hq@`g)*LeZ0Nlz^VE#muflK$DAaE<cT71(jyrA54ctRIn6;bS9NlCcuDP++yoc|+AQ2>ZkrbMbN*D#u(46uTt$EAWfZ$VB&CI*<GCxN5_cxn=TsfcJ~hGzjiJiAt?_{qe~U>YX!(eG}9>6I`R@BxD^BYJhY+z&OP$cWwKmP{=;ZaaP@g&`>fhp87-MC?@5?IuDsuy{P$S{6X`wx*)GM<dG<g53xh9RX$%XRN>oqeN9u&1CNbW_eG5^KPNI0(NtyoVg;iQRxQrBr3LM`A!0676a#MH|pRjp$NJyBD%K$*!kam5H0V2cKAaVtck0{z0#1qt+3xY%F2u<+eoG08<oMMFrm}QcRTi^G8@zPqJKe}fo<-Pt&tNn9~@&I<ERf++Yw;P{B`N#gxP+7z@)En&^E>Ix}7Lk8ZCuk6f_zzsLm7`c*Ph6+I45JqAqf4GWCa$=Rg;;$}!pSOm>s2eU7Ju#2>koLFcv%$;5>kuQB<=LEUvxoe!X(Jb{*SqZrV!AMrnk9w0+HZ2iZPKO)tB3=;k5#qh&Vwe3&@4cpLpqUog?o*I+<w5L%JV;GzupUHF``Q^Gk5-aWuAaSqeHyCN6b9Vwqu>5>lH(C+>l`rb#vU^g1C3qxj66$(pFofH<)*%e8ysy2SPuzAm9VCK9hEX&tf|cHXpDE1sNdb%|2Q9Q@!(KKJ#S!pLnJLuex+0?P?>ndD5cItO?nzb=Fm!Zss1CdkGe<8KwMeOBd|k3jkYe>rPmp(PuWU(NDZB3Rbi~piwXXYK>7=pDXq#s>my%MruBY@d86+)C=N0tu4kD-T=oSe52_KbQ30>S9>2U2KRp5jY)}jhIboKpS7^*;vnr${ELun0iJzU+MN&}>_B~;8&2h?25hIV<dZhX{AUFS=vAQZtaEFav(u(?FG3nU6k;)M^4;fkz$1EJ?hH+k_cy%;pJ`ZU@#x2@?&H^oo~Ig)W?{d+k7#r|VR4BCF>k$3<kZHfvrHVZ2R_;5tU9xDJYSfL7V{MEt|y{jb2;wYU`6Py}Sw?OmCp{70)9O)7iqT`L3*hA{U5OORAKg?IDSBMtp03VjY${-L_6ivru-2|kQ>I!9Gse{6ik4m`HfJ+n!RO&l8(T68WT|6x*H&($Op%QF*c*WAY-1AE|9OTTF#Lm)YG}6)9`jxz#>X{H0)w6bXL1+nyJVZjTEQzib&7hnC2C^mMh1>JB_c&_88q|fiT*O)9!LQRAhm>S+?8%jHh0+Kthr!Z<@AH^b!gtpgMyQinah0TVcT%0KBs&i*XLt9zT_+(XomggPdvRMtSDkI41}Z?X)k2%f)68C{pc5Eqkzi2}DvkBx^lClgUqWy_I^d%UIL8&o07t$igKe2_(xqgo<7yYo)dE)+k{n~OSS7_WXif=fP+ozu<$IT)3$C{k6pkJ5r4eKq**%_9&-E!!u*m&<h21_p;W;OE+v)X>_BuIR8p^*CNQ|fSQRDEkj5MP9=#MR_ikgcE^brVR@SF$%%MR^CiGWS6Hq1bif`E&p#s%dhs{(ghT4jPJrU{Ak7}3Tks<)}SE$a-+atyRHIZ;%P4;hec30z<?J;{Qe(`8$%Ry}w?V3?KfMX~EjbS?qID%eTVFp!|p1Q1h9m@xDMZ&fZwtriN!CoTT4gilNGX;3={vv-NINzbpSa(tAk!##6Q3;qxvDLSzp{X*&(9-iNzU@=3g<6#dY3gH0}QRy=U1ffa-yBRa>U*(QeDP72`&?1YRyGqUJ1e8s%hXk421MjmfQx7NR8c2Ht^6%~@<X92=b8F(sHm7#Ox~Wk*?E_;5CfO$QRV*9Ns4)mwtEKd?g~t3SB-<9+Y6zCqv&7i3XA+k}g&7j0IHSnnqeDQdokz>IH=Ak#bE0-9B%WFNh#yn}6V6>rloukdThv7$-B{(%5nQ1?Dq)y9@-iCMc9g5As2w`b=)}G_3J~7bgeq08g#1gikWNJE#_ajNsJE-YZ;`6nslpOXCKLC4g?qw5NBn4*=?!VEfSwmQIF3W>D3%3D7S35^QGFojy_LSk*PtgB?u%e{u9sF5V-p8`M}(`&!Se)>+;Z2+k3GeQ4~RXXavUY#-_EhPq}+No%7?KqV-e&zaTcBkSlc9IyKzYvnHyD&FUZKMUR553p>^FyX!bId$0YUvGn=w9kMUsY0s=;5<B3^-EE4H65;RVA+2kvKq#n;9lhezT(*+?#mEeNMkO?I;ghEKlEm1BXUJl5(k2n-&6i-deGRD68%u|}shTY@LanmIS0U~ke>L2uRvJ<qb(}+3&he46RHVUDIX2eUaqz9^lK>CRJLS$E5iAVw_Fayg7no`AjsRqgX;A?v+$a?U6mXNGtfVVFh{ER9{i3+LkLh$2kS4N`p)kZF2;ZFhu*RdVB7jhrb8iq^*pr-%(l?d_fGhEn1;9_KDS7Py*L{LM3TGGrVB5zY??moFFgb6C~ea)1Bww(zG!%j4$=s36_MI|g1Rl1k4_h-~rDn$>p_*=<sA0N#ebdV7dfIGq3Ys9WRIcMsp(EtiLa`jmsa^6q|)i9xwZ+$Fsn4f`qHZ!Nri`6v(y!l?7PwcIHUw6R`#sun51!ThM6HG6HC3@X<={0Sp0QToxROC9oJ?ork+!9(yQ$@0RVviA>BY{zI8{h#K;jWh$-BxaCofk(^l)O#$CC6Ade@lQDLek-BbVAUM()gv^_DI-R^V)@+bEjKD@&VxpMAeD5=b}zbnt?t<O!x_zpt^R_DkF{|l13GkAM*EU4dS$TmL8SGjB#^ppNY)Z<87w#;nj79wXQ^@xmR$`c4U`zlTN!_$?hR!D0-=HPJij$z}hFB8;I{j*(9dWePh8&P?C03vst{CvJom_XzS3Jq~=^Fo+M484Rk0KbC~Jy;Z;Q0{zDRbr3(u$M4^-oN<K#eati{NTw@!#owQo46VwGUTqN_5P`{24jLBaRB(zZ9Qa&bE4NI)?NqKWDpP39?z^{wt)bv^-ejH%>rU?<5<;y%Hp*vY4{fk#t)sSxIB=H(9=26_W_g@dfF0Lv0_o_HxzMsjd_?gl=vLUT-iw=d4304MW*20<mD-%IfQ0P_fpvtFAofciBh$r-!PboAV^-3DXtjEb?kUFF_f;f~CEGD%<SPucw5OzHDQt??F1wgB9hWEi#Ox!`DoV~}ks1WyOq<&4cNa_Yq<4{5HBz(ET9&NGyKksR6sTacu9vr91T!r4&r?TwptndW76nsJ%?cru@VZ3)av8`FzJ*X&^F1hu|K@OPQMXVb@CATCLazlmHevePB7g3&~M=F$L#eI!K`y%GV^)fJO5;5aCCp=xFmXeQLq$Wd$$o=vJd_$-Sk2?-U`n9U^Ywra2+{oX!FSCGhRCicnQ9fg7(|pWLYsfohD1lttiabOI#E$%Gs^p64@$+snky{`rVWwMW1Q!@%v)q3O@M|>!lvOF`T-c<P^G#h?Sr{>FQBJC|ybLbu4&0sqBbdJ%(8z8%C6+eXCOdjQqb&&Lt2exJQqJ}<;H{yM187gs_EQNiS)BUls>|b)R*KR7=mENPLN;f(Rge5F-#Lx$mDtLoQlE&`w=nulv>jCQwz~TxIKz)cv3wSi8wj*+q>8652Q|%qD8eMJ74yV;@5HdIzM#HwPJc#6n<SlW;3&4Om3fx3v<YkYnofvYBsWNRcu_K=Y%hX+`DGjVekimSjG-ffm&9MK42_a1=#!ov_c$nVVG2QOqOjY)LNi9bzF+en86AI`ab@%grJ-Y}vKkcDY?sCMUwo!S3#d_QQl>4#Hl)~=7Sq=vG7(86Ck>owlc=|D{`f{igmM$e%ybTNW(8#Yj+pr_J8e_JAz3Mkw!(8NBfU|e)$lSaApL4qO&8~B0ks+bh~E+<QG4#G&fI*eM4(mdmaWJ6%Zt6dQS`^=gSRSF<^qnHfCN<)r?PGX-avH$ms}?!?xgOL0N6AFqI%pPH*79fQyj+C9GJdSO;ePNk7TJo$CWMrugt;NFXDD5O>-t-iJ%`(e-(Mw<O>xSa+|KQkcAbg-PGc%`n-)$aXO1=BPw-Ijm4830m7+zANSDvp+r@`jd|`avDa$V?aX+90qo8r-P2)uGt^3u#=<{xUr-tzyED5}ue@Ws{y@lQ;9USC<AsrRyf2T@3!EJuza4pqv#MkgP<-R4NNI>hI}sht#i`lAHm6k9^`6aNtWV$85|7RSgS3UGW;?ZyFiPV&F)6E@1;&&#eqjRSA;wg-<N2@Y2vMB>imvXtLrh;Rp4q^!i(kF9ODfgnUt}x>1S2d5LQX!|)AC!-rPMs(t0zbTqx~74gV@B>m(~x$f<8eIvhj~lt4_p+X#}1tkoKks4DDyEXyk-j*~TT3kiEd@fE@nxrd}~t(3XcN03^h-ytdV6RBQ0{R5X0g$sz-oC(L##-fN;&E`V5L4El7OsUI}Vf!hY1Hr~j)K3*vaYMF<Cya<J(fKF2*Ra$yNn|ZXRZQ7j635VoW=V+{cMgrOl2otWs+k8;vm`%QT=Pc-Kbd|DTy{Og7Cub|`-Evw)#mX);d7e#4{Gtw=raH-CV$F3_*ZT<zYoS7`;R2q_;N_~2cxj%p;7PE~1f}~^!X*}g5AHXA^z;!uJv?4&9pLIwOFe)fRHO+An})@lNP%ScbJpa@s=|;nV>cp3%8n|SgEaQ_#$24!Am5ubnv1C{G}dGP7*4G@kEMoHgRF`-l&IH`QPeCoduv$kV6A(Q$4#I_hf@z=XA}9#;S4$*K-qn)s;_M>Ukw}ye*BqPjgNv*io-TW6qL~Co=~;W0h)XQFUAFWBFQyLSfytKndliAPoOO#cF0H-HwDhPU6t1Ma9L`LkSGzvG@rJKx&S0{lZ$x>hOVxhzybsU+LEnGm4UHRQt}6=!&q_0r`p=`P{dEwk}xMGx)0VLUMx##xWId<y6udm8zThdzz~v16&fAkkagR&#Z-I%vF}WcNJdRcS|AQT@S6;W9D9E$>1skdQjk>Wv7+XQ1Y!X$8R;d?Uiy%kqo(+ozHb#Z{-z~3bKB2a4YTZKWUOhc6>@-qhIjDPh#Jf>{?<;_{qK-?zFd37LXfD!i3&GnVtEbcWQx{7ER<`#%VS}RVbLaup7@p@hq7tq&#ZN4q9{EosbpT7hS_eyE(!5&x?%~zHHwkcLbj0?!(%1hJmAWj5}fNSev_^hqMYmi57pU2Uiqa*?9snVO{A%KPXqMLg`x>^<tepN?DxUd^Ze4F{8#_R`cCUzc|af!1J5wt*MI_7Uo}?MGW9*J4d6x(6PcfcrH}?DycH9qsMNDz`0LL(BkAr!jH}8!)twW|6=E*d+V+t?cPR!D$+J>+!@?2vJ5HEsg8lktJIL9)s%&uDdgoThV*zZ)TH<V~ODghFc0^~^ayz53{Qf6(X??Xl0un>z9P9*hH|U$LbaZ5F(tr$GR~ZA3n#RfiKjjhTV;rsS3<Ca+y>hW?mF=I+wfmn!bxYOd*#nk3p8=7>VJ(=0XOuU>24Y$(q1!V8ZX%??&eYCX)`;A^UF`WBKP|q?e^vL!al%R>k-<gvNQ<UA@`_l?MWa3mp|kb&M}t*1ol@U;UnNj}Mu56d&maJ%0AWUa-{PzlX?A^5xka%6fx8;-BjXc=Jy~cCTSg`J#jrPZ1vQ((pt>z4QLK<@!lho8$xLEd7L+H{#D;aCKBIHuw`Gnm3b$v=1(fX_zscraMz>?C@6Mmmc84UN-I#q$v}%si)UDSir)j`Zvis1Y+SXG`QA!orslsAjMw+ur7`53_u0Y&_(WkyJIR^tKRB`_#>I3)v|ML3}KYsVOZ(rB9N9#Fld4J*SM%GEo%L+JwDhCkcr7fi)o*jFKftTjR0uco|2Y6v8#otg&Ishc7;@`5|1GQk6zE}w_iD;iVyhAaunQFC3DmlQ)rtP-LhvEUCM2jUUp;&N#4>;LeWgf_vwDIKjNr&?t>Gwoj6`PXFl<VDu00X=tIT=`%;tbmbpHxWVSQqr~mU+zOJt@&X?6Dn+*5swA`TUUo%G!w2W@rK+9qE+Ca!~p_7(+qmvevX-*h(1xH>F8Sek$DN7>krv*N~`}TtC9_UxE@@;CQoz=DovVAdlLxKhwDK(o0qZy7*Le9{KX$XB!+q8V(4>+w4$C4PHswN1dG_FSDJWEU-r2(9Uk<yY}h&k>G@ZS&EPSu333N3ph7pH&3@W)!q|MwO<^5(OH%BiF}*-vUmiDuZ^3Nf>zs59x$h=$G2bHe;EF$x~lx+M9K7(=0a>qyYa&zrkhlWcujbjir&fHEw-_8S1#iGVRcC9cE}VwqOwMk7<vJwC3cFr6{`Dj^U4NtL^qyDV(f!}h<v=Cvxq@RXH4@Vz{?sAEr3|Cqkba+i_GYVlUtM-AgUoo8El^R&KVlbQo)U4E{*#`^@bMjtYl6vT<9lGQ`qFtEXYd&zeDybxl0Cqwa{G33B0mC@KFstoRW)QJpn9v4z|MvW**r-7cm6pNxJ=nxvAXxDJ|34sks{!Xi|3zl%jekN##n3Qb%JQfKGG6p$7taeR}47;?y_>w^NU>00Us_zxWH8?BN$Y&ouXtP;)M9sRnsmX0Nj-UfgAFoc04KfC%#2_ZH6=mLyNb(KIuPw9mk5hS`<s<u1N0tarJL{{|ME>Bh$msx`d&|1WDF5Vq|*5kAdjO6U$J1u4AyCkW4W5@vY*raW&0KxkoAHd#pMt+$1FkQia`)@!DY*Z&`Ht&e%p_g_X;`;ofoUSr7oK^GV&09^4MhM+1d|0mo?b^GD>z_M#(zhJnn^My`Mv3{LVA1xf-KmNy;zyAOJ(|`ZZ|K*>*Oy*y|X}*3&)A!X7=fpldgKB>Hy6J~(d#xd&(t#BX#xN#Y-O$eCW_z`;>TM8{+?U*&Gyh=7&v^Ufxw`W>YU+M!C`;U7uuOkB#5FPwtz~l=`g|SVaDf;1Bc+Xb=31w#V5~xc_FaSG$4@_hcZb|R{rtmEpWbfNzh1AuyyHf1lWBs*X1!)zO_D%GVEyP8b9&!L=ytwFTW>K9^VfV7A}!~9BonWb>13t2=;0R2rdf^8ZiHyzd%gD(Ct|&GNWU2D=ilQZ9x#yOy<h${WQ7=EvE#URfxd6QpUqH;h2Dlc!h_H3l`W9e&Y5;Nj%;!YNJj}W6tb)c!inm|;FxEX=j@CKgSL7lmwQ`9uM$nL+`q5}VJoBq*%c-_U0CdRiB39FX^b`<bh=L4YdO$Hy$SYD0jUvwj0oHfZl?vi?PFUfZx5&#OuJ96U)*ng7i@k9i?<J($vdi)8ncBRc;7}$70)Qvq4qVpYLo^H+$ndDhbZy`e5)>q>FgfgzfdVx9rZi--jC^E*59@#?C<o1;neNz{Iph0=NUY216m?2zH8DC6eF7bAf`*MdsKyTPxW8$9^k1_WodcE3n)S^95C?Ntt#Hb{<_s}q0&@uAKcYR?vRgqa{tbIVEOIq?Q#E1eO;60%E39`cA`b++bRyQh0fC;Q(g2v1|U~_KO<jPm?9_B7)#ZonNwyl1oT63Qgt!AZ80aEphkP40VrTgLio!Uh9%Rihs@l(f+j!4z4bzQj#N0Oa?xi&;Rt~SXsvU;=mcrc=EEk?(t{Fi_uM=SA&J7(2kS)<HQG+g+~zx~qVPlNWNXBVT{my;<VN@9q2#-&3D?Kl+RN3vUR18c$4tVWIqh>4hk&vGQ3phK)#p)OqcWiJPz1$WkN0j;>&yu%5ds+n_70Y3&M(ii;?#MmkD|y_NgDF~bC*l~=dy{$AKW}6ip}L+kM#-b37uCXTw4AvXjN3%ka6h*Re#jOH<MEMs)m+GmoB|55gE{-t&TQ#BH;#Y592ZrQpFgBZ05&<rng!S@!piaT*5IG+cC*6>Y2q2gTF4HAJ`Qc!zH?iHElAR^Z?^TDid#GnAI^beX)nHeM}aXt$kR1>pGt3W`>=g!G!hP;H|2y8F*RSOLV={m?Vm9=s%)RNzKEzm*{nf#qWu(r%fQr`Yg^JC8UwtODnVMnH3qV$Jx13)x%hJd(rdS9(KT@BE3h4RAdg#qz{&qRk8sK0icasm%5H<&`V=@A(91dP`+D^N1#QH0qm;BML<IamOm67t#ZSi<W@IS>jaUBf@sg{i3u)(b*yvbL$RVAv88}h7OolUA|HNHnUa(vMWI*QTx2C4Tni;CWriCHqxZIH^hP5@Guo8*n~Wgx=S~&IciRkFS)_)hV`~f&s-nLQs;f|7lelzJVs;%wFYC#Ya8suW1V*4|j=eysZ3cN+33Q++IS_L5K30XJUAEDVRQ|Kekd~h%%Yb5}`&}^Q@~iLVc5xSvAziK+p%CkM=LGqgG1v$z86Xd<vjWarM79FYGiXNW55|_r+Cj98=iBFqba|yqSJ#GcfBSVi+omoL$WuM+3N;9@?4Gx6-oFIk5eJ^jtuy|zvZ$TP0dR$}BJ#Aa(Y6kuuWZ00%A@MpEceWWp^YB#1safqd*Y66tWe>j4Xs(nKX(*Uo=l=yl88*M!<f$+Q>u3kPwPb)p~Ba0mpXb0(<UIUIOtZ8>ZbH{$lXN`_P`3GelsM=6J+_?u92H!f;H1BZ9@Kk+sU-58YVYcANNpn-N_bbk#I?Jov20imDFUCgJJQgee3gwV91My(5sIo9K%C^>p6-*il(%}_cTl~Ct7oCv0FFQ@|Dr5(okL`sI$S&Y7Q5P9)gJs>awad>tP$IoL(30ujWeZFPRMUhc)|r8%m=xl~Z2`>US=2x$RrIyM&~fC*(#4J=CUXZ?BW1(s3AQODD0y*OB#!ZWk)KnhO314t>E#SVuZkV5~A#FGAEAe*uhjtd$T%gNwDuXy)IGDC2^2pwty$>QH`+2FFq|qNq^6b2Z*&AjW9We0WTvi}6=5;p0A}0EF!qIS~j3$i&pb(9A9$ZSG;`_CAB*BF_MQA{QaF*-bcFNPQ|Zd2BL|l6i;o(iT<nn1KbxcvDigctOaOUZD<UW@>D*jWF$^Tpu;0v^DpJ>47H;eiQuycu7Dv65(i)b+}JAPrCD&-)1JP6zZ`CVRQk?uM=lir|{VtS}$$;60Azq#S|am`<#Z#CPe;pXyq6HKvI0Hor>$*@JFTz)%pb|MbM7;@~}xl@q6}I5&34@0hE=bwnG%P0wYuM<eCOWbbtuwWF7u22HoiRlAOfj$L&PqMrnkyu#R3PDAImQgdIn6fl1cMDDx46E|sL)C%8DNrTb<*HaazcDi+w2YCX_Mfk|af6@F+TasX}HEfnGu7WZPZ2#!6Ao;8nMz6gVUtL%j+b6S$OzV$XP+ZI$vu^pTllw$3wNDXF?L*yD30t%#EH3U}_-orC+FC&UYc!cAauelghd2Qh8(VAA1*YS%&qiId5+!yPR46gW)8SW7nbHkriUWm@$WH}r<{%f|Zv@NtBSanLS&^_VtsQu|Vo0qoKj8E5escGm!s|&10;_SClF`3%cLYM+f#vZEBDlJ2r=KHJkgYFY(Wz|XEnAM&+-nw2Fu8Zf;g>$GqQ9-RjxRu%dF7aG@8MIBPdhv=KRuPdhIT|BQgId>4-YK5iq&c9(ofqxV7-f6dnW}hd`T0sx3#O@3z9nEB5X6C}rrn-YDzY-os$~Vqw?rFiP%#wJj^rI$BKxu@gdGAF&n29Wq@B%?4wa{r1jh+j$c#H;UMba<3Uv@-OUYxRabC0@Y$t?6+d^K1Hu2&GYT+RXOT|<XWMX7pU}P{k<6{`Kc!=`mJiP&D+`VdM;JE-GN4o2L(9<txQiFV7SsVypi?T2+A>YXxF{*%Mgc1>~Orv4tr7JdeQ>dR3j$K01o+`U>A3GIs{EE9IWE{tj;!DjDDLLvHCW2!bYEL2EVtKyD(umQVm|{q+EZrb<ihLVj6HtKRq8yQvF2URIGx7w|*l_Yf{v~1uTYuzn#|3Or)Yj6@x!gRkyj@t2Vc;(+baMR2PNwm#!|Cf3$wP+%l}v<0Krp@`utr+?LGcfNU|<;I2iut#*!u&Vgl-{<VZ{wB173&kr5748dW}dF;SsVti=ya6)*&x71=wbJ=>u*23^R<b5QLG+G7>16N7T*~6s()v6&f&dy#|dhh?fS&To=H1m$nkH%vJ|6oAgbfQ>!v*u_LX!H4~ASuFu<N_=3FYZ>q`bTm;$`f-f~z3bm75D|Ih*u+!t&Ym)bmj{5}4t2oIuYiJ-gG*)7KPZFZL%%_ad7fv8=GZ@8EXIUVrE60B}EO!^FxtujFWcdDw=;OwN%&yRH0SLuenadamviy+y=-MZSz}<5r->&JBau-9ui%`4#<!B=7U?XXIMz~fAoZRpjoR6W#j|T6)<`@bC8qc=7p%PlUzbFiKs*r<v8a*Oz9n>|m+<ZyZO=JofRFZHV(UM04zyk^^Xqa?%(p@TqS2DdQnHVAq*Y;DYXc0zd(^PR?<k1j^P*z$%Xjj*^GOvYZ7Fin9E%3L-+jcs6iW7uE&4`BP#A`QFenZz*mh5xpFv_9pJ?Cqquy&AjHS@V;T{%P+l`n@MX~9qx7B~EtgAdnd4&`AOBMhBLV%nkRe3w;;iLPZ-44hY05LU6KU1OD|CW}zqW$iAi^^yD!e21Bw0;%D7$MXk%eRYj$n&`}ExT!5Qi5IhdhK)jzEOOLH-Gb|Yb)8%+q6@v!GNb4K`HQMcUeaq>QpOZkZm5s}J)Nmmm05aHR=bYhQLrrj%AXR%7XflN)kO2CvInMaQAU}^Kfd71{%;&EvdK(pR>e$kbaQ3J<~N?gVv=yhxaV!SiwaVJv@q*I$T>@yh8A0x(90Y?n2-lFSeRoeCn<|D90%J}>JwtK4T7{9bTdeXt<xw)GuOW#KPCwk9)^H{A$55|>XA$^I2OyadaPZz9%0|h;0H-v)7%Vd4G>W@x<b>&*~?18b+uuJ&?lJ4sJC#GSWQvS1O7z#Zfu_~g0tW*@n-p0eFL4JYM?=^!ovP_Jj(|dW>}CP5r90=q*^w2S4h}sW{b91!aIbPi*_f5Mm1O(cR>JGXxE^gtD%(*n8|h%z?NrtT}vLi6PBD&lc+%rgiJ!A)S^kpY0ZUW4YE|7O*afO*`D?qB}{L2nBus07*)?2sBah(jZP8+s_0Rg<nplud?lmHtUHUluyZA$i9eSha;N=GaVyDgSmf-!h$JK+1(xUsN~GP$JKe<CK>tzLK&f_uV2mM=`VYwOkhv{rcD58Q82#zh$cw^7=mIY{Xo{(+nY{-U&35;Wot$uHJv`JMgHwoEuHC2yVi1e5vOY0Uy$>#$xc@^po{7`+)J8y(_9ob7r*$`)MAWt?o;+rs>nb5lBxtXQCn866z%+md!qa}iF<`*)?qhuipinyTtj*7%u~UMkLE>32BR__3Y6MS&>_aT$QdTT&++E)%A{!B;?59h*BWLn(#9i72pvT*zgg6PK{7|Jt$f6O#+Nn+1IMe8*1bF)9=0e=5t2O!En(nP5vU^y*it2q8Za<w_FDJ}nEowQ?07e83u~QaOAp9>ZE}f*;n=B`9tj*}|Nl^@NPR3KgAdyO;HNE65TgNq3MtqbG!lW6AOsjhVN)Kri$L9iScxbWKW8$H@pVXxS4U)Lbj5`w6^Rm-7U(WSMr;I%sh)0-_HJG_ktNj`G6^xjzuJBsU?df*sQC5gPI`ocnq1U-no2sx6%Gai3+ACo&W=k2*eIATi6_JOJf?;O4kCLo2z(X|3<VZHBJ?NG0wL<1Sjl=KQx-P+}E&&>+J1H71aT0)}QMC?!iXafy+a-~xApJMul>R(t#MEsn(#<W{8Idd1zYv#-MbtaB);|7;1zv<g2hM)RDLq1{6-B$&@kM#Z;I)>jNp@fC10z*kun1!ci4Lz*hwI!&Qa-G_N=dzgMGloKtJ=3FYM#=d9hgL>g_MVn0H29@tB$=8+EgL$L6;g>>OL|3t~I-Ryn4si5*YdL#XSD)b^L-THA6{sI1Y$PTyfhWu*y?KlP=u`pVQ133|n~ZU_OF$KJZ>Z4@l4DB`DyrEO8HTmx)4daCUi8Tlddpe~Boh4$7q3HKq1@{j{pF`~D&~PR!%Hyvv);Kk<%1U+9vsz2FiMfs8PvTW1@~_7_|ncu*p2L$L^^)6F__v7_Wg#{H$QSZLALAeDhs_iP<m*u))U!Sx`SO_b|LI!E{G3%wJR;+I66$Qh>941~qJ!hAiudX{Y(Q^pmb=sHEx_*YJYmi{tVbTfIwOg;)S=`Tx7RSP4|+d3Ch5|o#$a4UU|xJc*DGn8D(@n`~-$C%M=jiYH)1|Dm_!A}&0cH$A%5LxZBfTLrAez4Zn>&UulX#~v);*X9NKM2=X)9cucj>r(Y{Yxqt6;EW?CL$=fSnSP<3-(_JkpcBmRJSRXdx0qdfiJ2B(lI>JH&bQB7BCxo0|X^$vF9Rts@=Baa{?)W4Sh=#Vn<^++DwI#e=1*Qh&1aA7nz2b5{;*}r39hYxFn?+R`G={57saXT)55~)HZceA%Qs0ex30B5?Oy-uh6$`$~kqpqhS=8QV&T7m4)IAVHAp{2@<~nkFZW$w2yUWB3O@5maIfWj)k-iaj4ZlWqLw4r5&i>QzJxTH?DPG$j5-;<GYO(ivn$l$|^a3*(bT_GXhaYn&`yTB3>NNxn1V7iOtV4(-AN+xF9ei-Z@kgu=GoeQC;vUO$X-oj7pk6*yb<0`13tVUlS62cd0zYRzs8+4miOQAB4gT>jWx9KePHGN%D#{oQ`XMwi>dsd=#?Mb+Qm6L`qukBtoqX&|O~nxjmFY^*5YWx)-Hi?%_9_ztp<lUstnNWz}e_A*J-l6>8}cHC4wsuX7k>i_k)y+tq(@e73qhNqv(@0Q0ig1eyTibT(A>$n|Y5Ny)@L0@oTv{-x(654$^&jHFNkq!QPOV#GQ_(>5JFb;GqiEs6+3V;>??y1d^vVNf;wc@*Qe#W>V8c$&j@{@|ESDM2@UK$%G~SpU0UUw`5EP<RivG&SG%OGW07%l`pL7dWk!Bu1r7-$z^MV>nR(jO<kn<CvjD`gW*pY!E&St=wHeRe|&yRD!nE#^FXhCoY1vPNWM&8qp3Yw+(IdEXg&(eOZin+ZJ66Lxvv7zlv*?^5UOy(QrSE=Vbfu72Y4@yAQI~Us2(&)5O_bD=7pHe?(CY;Ea2>GG2v998gV_O1V`d6JT+)xQf0Xmi(A4Q;q!)tH^SPHD2<=vKR#&RwX3n54nl+6;45K7Ag;$2`IyDbplHjL()$|GIgG0ATtVyY~VUt@0YiPX3VLuUZ0G<4>JSUV(j7KLft2Ie7xk+IOsNn^0&H>Pco+ihB_t;1;?r`XG}5h+M36HoOBkQoT&w};7OKX2vd)<!e}^9?@6wO>ENEC3}#R4B9qcVmM%jvzz3i6C%khyT@uDmD@}P&CYTi%T$8#4S#l!kj0|)hLaJ1uF2Qyj*1L*%|0rTr7BZ{=0!1B>Z9*OZw#Sff;aO)NXWaG{V8;%t)|d?83ys6U5EB(YBm*Uj)1IefO<`i$=FaSax+!>A6(6e*eL(odjE9TvRr5weP)Ow;lC<A(eCt$Zxi%flvQ<tY)hiHtGw2iBT#rH_LMgh3O)+u$-~K4PKf|<UDGKqAhK&?L5Ud+BjP1t^IO6|>Y7V&tNUTQW5jh!zMQP>K9<Aqn;fYKDEXKVU24rM<a+(!yhO=UvYT8v{9cG`;nDT=AnqFXF#5TpW4me6C`6z<i`jI~Q0ddYtEfum679HoTGGw2aMhTG$QIJ6O73LFpGJ;fwqQ*8_CBU8MJu2!FJHWD{WIRy<@1b9g@kiKeC?|zZtY=BIh^)MK>|hI#2~8#=3eeSL7_A77On)7J2+xwM#ya<5$N@1V8xq7lXPSYhftNO)kB<t_IsIRTnOwr7dNVCi5)y|`q_QMBQbHR(c1ZfvP3qx?jA6j?U?6*{zYj3iy-sUL2)NL<m8u-sdkv8#op)dvW#LJwq{n+IBDcc_&A^za`a21v05rP}RN2r0h3WQn3bU*ts3#_THUlG}L|kioXfaQj6Finh)^-n)7FY4Q723b5ui$VAyVP*MC(7MWQZqZ&-WeG#O+^P*u``^Ef{G8BM@w<7X((kf0C60hg+6-kQWZ^7GfVdP!I=-+6lLi~`L?S2LVg0bJ({-}^v^?>;`;j&SkrKc9%@cE;f3!$^W>wjrAe6aD0{zG1t((qEUrHTZmp>Mc2K*jDaWurSnkM@ow!Lm&7jAGE|wT0TSK9{kx?v2RR?FAT?#{QE*US6gH%UfA<#|CGzS}+Mm<PegA-OJ0^OMNg|$PWuR#tOlUNSb6cXlJS7$pEavbuR%$znao?$|4IRok|6&Az-TuL~&T~*QCp&8_S3@@07dlvy~ry3{3LPnX5O=xUB12bC=AD0LZO%7G2?GPlJc5=vgwp*_kwL66Qqb?vfNYWgbJ1*6vYi&E!wh%+J$N?6uN@L<Jh#3&|g%}D|4SP^S0=}b?QN>%yN(c{y@`gRK7I;-gr4)$Vs9biAVmlNn9ML&;LN_zUh^vMCi2I?<SN#WZcpGx3f?As~@qU3`d31T+rX9|33TD_RGObxrT6)sAU8{7C3WX1Qj=1%Z0m&+nXS*T|h0I4L!>Y4g86Lz1y<<Jsp`B#d)AO1zT`!IK2>mzK)nB&NpZ}p5LPM+9;K0_lTDjB{L7KzO*Lmp8Xz{M5aTlSx$Zq)#uS9T`MsC0P&b)gFx<<Z=NF9_|)P<2Au5G*yGxuWCz$ynM=P5#7l-6}Qg#r+C!3Rw(DJeGzjIh@WGZK0acx7oWM!=xD;W@8A=f_Z6_uTw$RQ+To0g0FGWPe#O*m|mzE{&(jU=mjuj5|@9de&C8I#JggmV~7O(^DN)>LDi4nf{VDVUoXBgQaKcif-UVA#HP#3#dzQN-`UA#nVs-+|XK>;BZl$o47rTT1GGw;x^pyf$*d0OKl)4#zeIahI^M3vNeqRO8c^2g~VKqhQd0^q1uo&_Eg-P0tPhpgXCLgl>32f6EKl(kf~GYblSkXZQxS`<k@JCv`h$UAeBlbRuZ$0c|K$0wEKGioRoi9Hjkx}dkB~k$g5)Z5Q{E{3qFJzkPvt4bgoAN29c|ehM_|FQ3gVEdJE;TY!))K=WviibU!=?`xv^Kei}^lR>SSrDP6z+etjI3f%`Iz{WhIm)q3Viv1royW~>s+98P0Ug`cIJh_HU^v#SHXoAy{IbIyiOGFzZbD{O8!3{wTdbvq;hUZUi`?s_8)Q~z-p<{CZ|t@Tl3-=ON;PmUNFRX^$(mO26kkJKWCG_$u@*e#PZ*(Nkzp3vZhlu__b>QZ5s=eUneMGd3L?F7mpA;`hNV5hkzO}~v%l@29PRkYyXQc<A<ir+qT7^9+`z<tCiY#g#uY?{G!bT4vMI=V~}Ya@c@FUUB7^D*R*aoQ@tK3_R4LoE@%CeSWc0lwq+@;It0*6b>XVKNrcz`T>v&1OgOCboEV3f{-euLX7BJjC%0Q+{LSQo`df6yD}cDs$mU371p^&dd@;X^H#P4uHbDn&TOlB@O2AtmSz_A@9T(T)~RQCxsJqBsJZ&thF_QtzR#Qbw-VNDk6L(dV!!jCN<XH&jOthGPyQ=Ztyg~x~qVVn<KYpr;wG>&(4ht<&rLHOoA@%sRvHVhC~)pQ??c<<gR4&vQQ^oO{<4JD2tgLHMZdi8a{IC5pnt0fnswBG_8(*_PI=*7t01(2Q^_(tq|aWXg9@dBvIqmEzA=Bm?%S!3fI8xJ-8TOA&|9C%A;lR8mtCdKjhccCw5E4O`*F003hJ=@4mpwH42tvZ{%4QM-JT@+6g?Zu;UN8QA{9ECP|5W@<s;)qXdHwi*&_~B96kwStiolC3IxKJ~KV$z$>o}!RKDFhpM_}rZ)~aIArnV$qc%Eum~t;;GSeiP3bqVsVLbD2sd0_2LH3A)o&f1;onhX(|O9>H-wb{`dkU_w1=I7m7aC$39s{5X^vIL@LH&KxJ#yErQUSg7G#A<WiMAi+{=mMP0OY3S_-PUHI#<eF(mJ#rAb(opUwb>+p{NNdi6rv!xG9a%M>A2bIiabw~E3Zils|=xOG+XHyM`Ao#;Zeikgbp=`;XXwzFQ+H`UvH88UYewBhwzh9Jd`D#I+(M9V_23M;>OX*4V@CpEtVt5Ljg@)4cn{$p|qB|OaNy7aS)f#K`gRjv?OZEtbE&pUa&?zR&NGcyX&N!_0~*|S<nXK<?3aK;OdUn6wr9C~xdFV?X%ff4(CWQVAjhXXfHr&z5MYW1=dCMZkjJZ{6+K~ZcS3qdG4LRK_Ix~%a0t2eG**GAJHYa%}uLL0m+49q}C4Xa>7CE7xj?jj%d%M$(i`gwOzj4)HO{#b;-L;+_&ph|R68w<H7_LA7JixJLPxk{|TF<xf9Z$%K7Sx=eiVue}H*k9U=;eJzxf#(f^3P+Qv>$$Qm0&m2#eTZz|%|+iHuIhBvGq_+$Je)cR+01mB95aPWF!`9uZsc)Yi9Y%$;shU`J~QY*C&=^Z9qDSNXz0NKWp`O^eSHeO3Iqg5BPH0eQbl&W*D(t3E>p~*{tiX21B7KA-k5j=w!ds+^s1T)RXk0%hbei<@X&K--<Ty6sG$*xJE17Ft)r$;;*)0fbL2bIi5<YL5^cX}W#>t@&waw{1eUPx(-ggck}JZBG=t50A8C8hC4u}BV*HO70Q7K5`D_%DQ#I~h#54-th>Rnmi#JV}@&Z<(+g2j1|Mk;4;gvxB5E=l*Pf6R=vU_EPcZvjw-O1nM{m~Xhxg@30(~r4qTXt4uc?DLcrxd1*?V$P{p?Hhfo?K+CykDrU>dugvqg+wU#0M#Bz#cQdX02rtUbZn$>X@niEJ^qRx3&BhIJdJ}<D78(bqzo|W~cwqSm;hkaz+uTk`qhzTd9nN9#oBp5rVpC7#%3dDIFHZuF-p9^9~CZ=gD0BK`y6s9lBPv-&_~A(1b(zWf!lIk)y7Y#dGP=V(MOClmc7<%%`t3d!~}aa(;B~qR9_(B2aD7!Rr(V*q|H5Sfw+hgFt%V84zZw;q#<e6}4C1)rpx^q8IqsCGcuS0Z#YxyIrdRs!*_s2hogx8x#{*s)`?1gc4QJE0eQwt^sh9WW?$5P3lznOBE>*`FhI`8qL%W&D&gBIR}l7A#lly_j8Bzyc72YPhGbEP`8R+1=ihR8^p>zT_7i+R~0=^kuyW#r@XP>mw2c&c4o6tCKq1_ye>9>dlsTr2+%ZYToj1qn}JRZPv4O`k+Gj-@gEAm*v4o9gj2p1f*5i$Y=e&8t0F8H6=$4p3F0=b^Q&>C-(-nBqlb&kyMK67{b{+PPwV}mbs5J&CCF2UN$h)D0^ICbX&j`j-G)9jl@*;djTsl<`ez{KLS2A(K=IA{)pGpy5k8u@2G$s%jQa)co>^VE$K|G87F*xabcV=!lj?;PDXCGE*FjXpaZaQp0#HCxG>Q_{T1Z=ze1$N4px6)IDd4rqVQp#f+reJC8cAxXDZe_6Z#U(3puqVJ#F<EwOi=E-K2*}FUa#<V-o1{wLD%^GlY1n;h`%`eB5ij{IkLw&?N8LQm<MZF#%;b~!5Q=)zWep{7subQU)+Bf{;6~?O@F3nW8c2_HrGkvG-k9P0#$f;^OS9ci9yd^nhW?U?KZ_F(Oz5C^3a75m2}gp{WLWfH7mwaKy2Obc6a}R*O-<|`Vu}+Zx(i+P@y#P{-IIPP9&+tB=I4}`Tn`|mLG7%y+40@!>%)@j_nlk;A$wqwA@w}qM^hZc+uP?B+!#`ykkGV{`BedtNGzW6RG)7)NuXr^=EQ_1@5Z31J~uxyy4W1leKUY#IF1fIPbTx+T|jiTW)9x-X8RoQp%cG{Eehdb1>`4XZYXb-V8EWYM&A}GA%vAa%EWRkKq(vObWN-AA8+%EzIsqZaquukk}s%>j%tN|FbXu6!<B`mER|+->myM8v6_E2oX;OPx2q-=1HygT(6pCmyG;OO3(d4a(prF`HSiazXcs%{(SrOFE@P<IX_QQ>uq71en`r_x6y+sV9u(Fc+<~yb>$fvl);*s;Sv{~>@s+xCqN#iYIO;{o`q2`y>Lg<fBf|GcXzS;Pe1?g)2BDneZ7T<`?d>1ql&)foFx`;+^y*AKofG}!AwG5{x84(@Z)!X`*P+#|84@L$KcGhVSjD2k>aRZW9!wM?QuuhKaIQOaLsI2NT3-)jl#_<`?@(%+VB1?yGX@%<a?n|?zaPEB5))dyL;CHwA9?-Uq`jT>e#~{rKTo^+wADLTYPx3spw8qNTb`;1t7DS_>BzFWOIBY9eY`GA=3RP!pvOwa~;VT9~Wd^M9v>-LfEcP;P1-TI!?OEOhr+HoJib;Lwf>0(*s&RZ&7LMVy>M#Ik<Pt{W<>auh;7@kHwfSIj>Al|7Ym}g1a;|DpOf#Fq3Pe+7#Ji(gp=MXf~Pes#}0h?&>;}M2&ncEM40hwVC=l;CRpcLXJk7UyJ@oEL7>aaxe5+n}(Cl>irPBpUGGpPD$FJ8*dt6<t1SQqjd!Cseu>bcDCBcyYSu$o6<XculJhM`+|oyqj8wanpd7^X(qiVuXi%+{ei};^2d)p+d4?SH$Cr}>Q+n?UW&&JZ%Wl;QDxO0FWS>VFDMW^+-(u(reYD<PC9GnO4WhYY-?7tmdXY`zmp4eZI__?R<h1)ax|LR$iBvjWlF336eJpep~E}N97O>AhBoG(9<be`zHm_z0DLa&(Ua+(+RT$0gaV1YYpf8=C?x9$=86ClL_$2M^U-DWM9oY6sxXciMZ5h?D&%=3-9yWDlEo;a=C4g5vRl_&gHgo2<uUMUzpYT4!Sn4(*GLXFi=bIh;`*Iq8LXqJfHl1En?0CEFDr}%G%?cK#(j;<o_5=?2I#ooWfge%X?{FVP7S~_r~45Y{0m3gC@`@_S4%GG%qaKNi4jyhJ9Pf1JaWlupxAi4nrGi^W_57r?Xc>?M@RbotidvQT-n@&qP0?k3B6-yrjD5zvHv`_my4PgaGWVh6Qci!B0{s~?In7kRK+=1Wo!L$+Wl6y-S#4@zf&%i!L~x5R!qU%4WJWIWH*GbQF9dJK{IRJpXjm4%N*0R@pVK)1ncnfVuYVrTLtb`g`q|&0(!^?3PK=N_&!=k)}_7Zy6jw(#_!r$W|mmV17E*64+H2uMQFq%+TtRgaE^o!7Ccay#}IoP((e)8i7#a#Oyo5z=ss*B>V}wTEbD9xDvTVqbZrX2^V=rU!Qpb3I(7km2k>&%L3L-K0gF?(fp|a;@)9G*gnrvZsdD!D`U?7GSx0lx_kNI<ncyBuag_row9T04jPSgI)3yl{DKLI7zu9A&yCQX$$!EoBZH1lH##*Y@<wa2>3*WS8TBF!)Z)PE(3dYS6%pmxuIg&Ul-nP-J6bfj_9T7MKD9r2@E7>-68Eem%CqYSi;N+EUTiFXB#ebmN!1cF8TO)r}yI^=!ITE!sDm{0v#vPbuFPkQ7B2=S?;5Qy>Lv7L1VtN$gVr{q90gier6fT-b#X&te>Y1h0=NNNz_yTP!Xoug3UOWX(wQhuNa-%I2L`hqC9v@akMO?N@LU_yRggum_SAn%+Bhgfmce2J^D2sykGps%WCyp9A8B=hXcA-`aQ`n_lW9*7~>D#sw<S^Jugzq|Cv>cthE#yAQL2|>(;9wzu39M$4<>bt!mkmHZM@ggg%_8i>$cU>NRl<w3z-UHYu-~Ev(JBfdHWwyX2RZ43bj=f_jA>oHGR`7qejluk&IwhA`%f6oEa~wNtwRl;n@8G0&%CFC_x|$ts-^S7_`XT&xl4(Zo7V0fkEzWQ-*baH0WV;sylv#&8Opx;Ra`{~EUlN@&7Bz<>WNHxV1jX`w0nXc8q{kQ+Kn&?y>+-_LWhT@I*HUkpcGaH7GRW<ny-r*8ZmboG~1!?A{ghKA16pkP+!Zs3t$5h-gdvp4_+V{#f7H>Txl(8AHhaoHqQ3*@3SZhitS&84><U2+UE`Z0{WiYEw+=3lGi`i_S*y-p$nE72ydx|euIE!QI1}i4q;C<5t1>qGGLEDUB21GIba>Pgei|FW}GJ(hLr$kd*PbJFzb49F>pvY^fjGOU4h-hkJ&0=bZo*(u41jD(0z-Jh9Lpay$|)<*VkV#H42}7Q$z7s4^+Gt6m3CPzH=*&d3GsEl)7cPNQ}~&C?le-0~JtGQcMoU%zZrhbR}`1VJ5uUua_@)FF<Jt&{`;fsi>wXnqY=#>r7SVR+{&IR|V&rSkzH9cnqoTf<LQKrdNV|128_+Rp>ECijW=`OP)YPzXaqJ!X9Af951}hw0WelP=p~Yk4Pgcp!671hug8s*L~D|k*qaV%QNQ9Ao>Kq19^)mE1Z`hhhrQFW512OGhGcIMga<_^9=Ybs``5uFIuNGCUPE8RjXI#r-50BQfs|gFW)uFfB{EafKK_|@zv&+kd4`#!f}@A4)#T|kqd3iduqV<!?4H&JBW=F(Sw6DPw{&-YQ3zseOE^mEJLU&lE_pi>L-Y7EvX?+S>)85DT+UJqI`5VWuj9n&p<xokp=VaAtyu%+Nskm4Pe^2gA*EU*sLmcABDrErvMUch8t`1<gAk>ov@C2&>J;GPpSjrc`?0GHLk)G(<n1XdBY7bI@_37?K&opeyZwFD@0Dwkjbyoy;#RR>&ocn(n<tPtazXI?v()w;e0Q;U;?<)7^hPX+nKBbGq6Ibg?r8+(U*!P()R~hs6x-2^(q!SOp3yRkwu5wmw-}Hh`E&u{Ic~@(c__VY2>MNdN-+%8Hk5WjK?PWfbHmXEoem+TFkv^mHH>`JXF{`7&m*-qBCD?6j<Cuvq-kMTFsb>61t<+yF+SiBCCEp(HgRy=RcdlG%rbg@F8NQ1ezkw4{GfN4lvx7oL(+fB=d|gWz<aeZ6MvH57sgyV1ve^>N#;V98%YPcZpENFtmXURbk;KdA?K6ZFd>v$P7>t?J$VwtzraIzE})=k{v0?l6YZXS5$e|)B@O#Wy7t}RqifJomd9DmgQfe6#@nH_CDN(cQPHKyu#t~nx1=)cTHDwkDugr=F<l2V55uD-qN(?6LQ%TD#KkPupn&A4T4{)$mw$Dz<|ceiWyN>0+s)1B0pfPRhqCmsz-M|6hiEpSuKuK6@iFAPmIWQ&7u}a(&|3gi&9X)R3Ft=aH>S%Y95bcwt!f8DbJ><s8rGMKo-nq(>?dDN!!rdXz0v<*(stmqfTzKYdbmB7Swcs)S*`Q87Ir!3a=M`nfvO>bmEA!glD2e4~9g<+J`*;Bm-rExQ$OntJ$x0K9S}VdVi(EiQXgE^9F}u3c3@3{pSs9*a-;B1G}Q4IqX>=w{5b{kK965SjFf?B<)*ji>^Vy>aJ>0zO0$wmFcB<rK?KeGCm?j)iSX}CWpyhXA3wAE7v~59_gWA3PJYd2;FqI;I!*xO{Ii@g|C~fqe7C~(CLy;?CzF?quBDUqZumnw35)Qiwc0@j5w0tN9g_E6Nc@&Fo=TPb6t|(kX73qGLlIP>sIKH9)bQ>*F_CEfR-|SNhz@|C<=_oSKdLZ0?-j+0sUnRqaN3#EB?`R^o(3DXKMXLhG|kk9Bs>Xg{^Z(38|x#X;g4t>;^>lz$Kd5%cw5}5ZA@h-bTM*4m2@^@QdY=_!5-c-&#lBMJO{_w%xEmjF+h4OlVFYX3=f4=w-kjqHF5L#65a|Z48oapo>H3WEDVIo&Y-bK>IKYQ=vM<Faj#I;}kY@eFChcSSq;0GFP9bkM69rjA#PTCnL7vr^Xn0bRFc9vfQWvWm@x$disa+KU^ve7kXqAV+VE=IwCIXtBZ@WNqZdD3?UI^yLhLyh@s5`@igGmd%fmj>7wvCGTlT@14e&7+epYZ4}GQa`fA88fnK>AdV|qLbOL;Nl0Hv*u_wSO<%2b<elMxfqt;AXRGVi|0V{?{&iAv9O|+=ihbzIxhdNf#16iR;O&tP<Gu91@%ozh839YtTS=)}TEXd7L4zAySzluaZ5vv#*HR3e_WC5}28nzuL!Jh|8OsU$;BLuWgxYeCTKz%c6a(<{j<i1(EU`GdN>`pby1p8;JpbrPd;1gUmY#n7^F-oAKW7$_sTGsk_U}Qu1Ts%C8U~~~JD|9T}Tm%^Rm=O!xy#xE%Bzzv0SCZCwlKoxaF9dz#Wce*Ii@&;*Tt=cRDsABwc<U_{VOb+5LcT=6%NhQn7dG7#wo1<Gp)`gU^H_VDE){vlVmGd;u|QEDg`~5NwMkU?Xl<jc>4%_}ikcsC0-Lc+ZH%++*Y>*~zW489#lS`GHj4zNPA<|whj2d~QrS>%^@IW`WeJO-*1)W41R;g?=n|eZ4KWQ0o=or|z!|uI@!hYlzfh_Crq>twrBoFfwsjx%vMO|%g<}wO!f-E|P%fGJ>!1~2r6c3RXJF8C(l}}?nWu%6W(4bC7rkZI)fd?m)e?O>QXlzQZ-J(jY1%_)QFW5-mdD*drsBT#cXsB1Ic~^biTdnl<u1gLEQU)b-0GK#T0c}H&lJ&Ia;kFO+|?j73X=(Aj&b#$J<~I1kNVh5`!sB(0BMTyQidFb63L>rHODQIE#jI>HEeS?oKY67eWdV%f<?l-;fj^-f5;bcl_K^zlf4Yn%{UNdL_xuSm{0Y1i*>uB8y8?I!n!Vr3R2O-N_1AMTj}MZwroxWr%}$;hS|U!bp5oYNvt!oTYEKG`*mHuYZPoRiHFpBTm(Bzc?>s?We*12>E$il*U}jSJR=`w-_F)+EWIoopP&^VAqI@v?%Y=xa7u~1brM6qaWv$S(>ew&115Q)1u>SnYs(nA-M#C4ki@F@G*~QIFH0+}J@mk%xkti}l28uq&XD1vr0%>qC~^pg5Ol%t%h&y*#1#RKH^Y{!Tb7^_;zmZKRmsu9otU)IUoNS#2u9T@u&LR-DhN(WAO%VSeIdwce`#dYfFZX`1g)}VXKf_@KJDIi;U2dsw@*7l!Er`VRMa?6#_KN!;Bvd+*6;F1dVf_e%Y9wC;6(D$2CE6aS8r<r{EOE7DIUt<)1*}>mdsn@b#eOCT|m&ZEngCm;jGL*Rkcz<xAgp9{3TwOMlTv7_2o!VF%lmqLMK`=*0WY%j5Ok9h7rCVWU3NqGAPy5JsJo<dub+hX`rtE4)$5nn)OL*;Pj+ux}JLc(l5@kt_w6Ll<z+Pf$T3;g;5N2q?p_L%bXXeNeKM!f!pnIYZ{d+D&ZMwrJmLeY8_&$Rz87GhYT+Eb8dwM7+6=WF~a)S2j$`s07Hgd9=B;Tf>^Ex5uHe%U`pW-B73mdQ=PyCg%&vI6)iOk>BaKC<2{L;vToa+IRQH|QXZ&X3rQZT+OFGPDlWw9C9xiMJgT{qA-3MPO`Y9EZmb6$=v>N>b=9|>uDv61u6X}Dc!;PqxKLEzhWIEeWrHFSAsia1NPq=iLa^}b;YOoYL<oaI22msn-8dV}QD}qcg$~xCCZZrR#z_Qy@ALTbH-3G!F8JrypFVwlmHg47Ptx(bZ{AV)lkXnzG8sUBS^B^)#?J3FQ|GskLrE$D)7p|dK`h$X`wy~S^;=d$Knl8(@{_wT<Rjeu?wkN+KqClpRDM7p!(Q!KzCm9|t^oXx37wJSuXat<!Q19;R6~Hx5m)bV;lqLsq2~;3*JEFcLbm0!oDk`1omHQV_^W*<^!TI_&O*;Yy5y2zBpCNxQ~MNfH;4{_eGVyvy$*88D|8|1i(VUl^oD|*tlzz$FC<ooZWmr$V!1b>(nl2Mz!;m4I(8NI9NAb+i2^Uu>3h9(7d&lnzwm?Rg)%IAm7`PkeW#uk`u@mz0J^e+0AdtcEt23O<QGJo71~8E=v6@0et51vBh`3j^<gm5B+4fW2-c4Yjopl16qk<<sRQ6{0ERWGrvl#ftniRty4l=2<x90TyxRP{LNkUO9L~I<Qb^G)ooo594t#m;<HKm2td$X;rF&rw7g+(rzTlNfJ@*lDtH#v(t5BSgBAoC^)KqzW!PabHNM8uikeJ8kw#rYPz+M1V6C4ePNK~O(6CM;Gk>QRIoO&CjQq)9yQ4H0tNF%Q^?N2vHP`bZU+e@_(DX3AUDvkxGxU5LN#fc=F`i@tnR4}*v!!Z6sLsO+XPC~Fm#iv->TGaE9Ye@xh6C?jpEcCiA^C?{uDBr;n*hUD2m7wdv+d7%0W-=Dc(ptEH>(h;&$4iBBNt|jEBIz)t>yNpq)HF%3uvznfY+?JcOmdw=n`hT2M(x)MFrsiWS|7U_-G`JgMo`&Wp`&&me4kT%Ao(uNv`$v3I=YtN6zDxV5j#V#Bc~@oz(o`(A4jOvVzRJpc3|Jvtc1*VZ6`#1WO9Y5XlYE{McJ5Fw~<WFNcr3-Jcx9Ysue@BM_3mt&`ZZ+7)QnroP#@M8e%_&b5GgQlbMoEO)7+J)-*M>iWb0yh>AJ^BU~ZDg_`UAlqjSOQbrtqiHO|76*_gg@QH5f5G{04Ig*e#v!`v<`<(4?|3R-XA-u~N#@NQLzqq71k*b@bv1r--SP1!mia);vI^&Khl5UDoPe~0FGF-dNm3V$phavm(h04!*Swl__m}i^oI$7VIM`8SI-p{nCRSX52=p~r#h<{YktF=}%U!DQ)G#>@;%n>RbXtItOe8>L_)ujhU;^$ara8kXtpIf;S({sXT%iUb_-EdjfL3gJ_r>tY<B}Hhb$+&fJKll1TeK80}a7xx=@*Wp3-XS<FKCF=dNeBlepgWW1Gge0#mf;q%KQ_I?b?yPp4K4!5Sf0`7qc7xsqLdDohQrcoQrnM^WCYA?P6S}i3IkA>JDaI|se3?{R3|nDEci!B)I2XQr|?*8XQ0pq(uATSbb;4Z(QYh!kL)Ha5&TSUDH|ZbgAp>cWC+>^x0Xl|Ake9{G=!+!NXE!K?MU@*S~5lbX)01s(?On>uz6WC8qnpwUAbC(4<1F-pQ|feh57+s^REc-CGXQ3>Ta}H+%&oXeM}h~`B7HmW-V-Qk$lswqC27U$c1u0ikuW%tcWoNpaAb#EA)K;>A-KCL{llSV9SM#I55Ndw_(_bcMk8D@G%#&F^*YDeYHS?CFvC$E@5Xf+DfyA*Iog3cqe)YC4hj%bIGEc-#}aJKJL78hv%SI)#&Cm#2yOeA5?CJ4oV-rje0&uCHY7XWiiNgj!{4CXjJ=uXK0r2h5Q^^>5T)GY$()s(#Y1K49pU3#^)kkL!k%5{7I>PDGl9tFvw7-jmYdn)*3MY?=!lT_yHd-OSJ%n^K6}Ig5ds?z`h?EnbgYquRv!!1L?cE25b%keZ+^RlG&QE8qYg(%WZTbI1xkIU$pm)tYx=~?HhUjRNY}8njAXCN+hIBagtZ~7Td(o!1Gfpv)^tTG-ujoMcrD^#sI+$(u-F)Xdo;c3Ska=V~_?>Dg9zb@UN?Xu{r`=n008|O2ti1KanfO?%%rG<+ZZs*3d>3+nhoMLdI=OVV2<*7V^lG7^{(OYn9=BNDdFjG+lS6mDT6msu%PFk=rbFq%h!?DGD36U6{{#zc!fpfb{OrE;4-@y#yj%zdC#C-AF6Dt0H4N6rwULp}h<G5G|k9yVAs|;PZEld=n97uiXl-qXtdY`n8=ym%IF_gOrNMPl)NuZS{t(%Lz*aJ?H@|vbsU<I>27X;1ccR!X;-cO>d}~<Ty&skc1_xCdunhZJR%;J{(gIRLV%B*S549u(<Wv>>5qCYb<r4D$K)`pLJ1)vqnv%ceKcJe{n3^1eS!YQ=mv@7WlmmRKGElOJVi*7IZq<1x?Ve^ux%cstVUgPp}zD#)4G{IX7nCCfY^vlSl<Yi2i^e#C>1$E@AVaEPEf0V=RI{{^q_{i=j8XI@CX*W%8_)@ODkB4|uHOAt`f$+wfIX<VE3=eZ9klpE#~iXr3^6hX<2)4Yz@TghZ8?ND*B>-8S+_@B|gT`*E}?^Fes+VVkQV6fwDxZjQ3_4>&JnYFK`*a^fX7QuEJsqZq^%p5w6azi9#9_CCWQ)IWup&n~5Gz;V+!@0ns<d#K5M#?3kPh7-wKWm@iz-K(;Op?zY~b9e&UgV(uAPZV6LA=cw}XPwm<#F)+y@x+<vOn_$5uw42Lq3PQ?ji^2g73}#tA-9`M4|uzRhw-%Ry&rwCY_3}_W#6@7s=)h9N`dD+b#OoT#0|5WcXm3^sH7LdLB#R%+qwvLLX&;NQkQ$?k!2*5X7(01FG*eaZ9?Pa2|YImix*vEN@+o?r8bOBMX8O+as?&!dXF}C6M4L&!@I0EmK?@b7VSi;Rr#(IyfuW{-Sr5Zc`yCgsoI25Pl!FRgX41w?lUZ#?oR&<jY1YSfftd}b@dwIp%6I<69^i_5rBfxBb0#CTvp~7J^c(UzF!wH^v8lPn5oN%i|}jV=s3KOncoWPz<H$QTcP|8&1Gf!VJKVyTcTYDqycb39E`KjKmie7jn<W${K-{fiCK&7OiUNK%A$&NA?gXM%{PT;wopp(&p?FxM2}0*la&C9`&lSA*lu!d`jp^l1Yjfc6<p$|Jt>8TihfdpN&wP?g6TO?@#^=L9y|q}p-@rbeD^BB&LG(*R$#E_V-awzov{rkT56`nNyX)h1SPz=1Y+b&o8$6POr}ze#gUSLh%iNQB!$t|m9G%~ScH^~d0fm32d1(U{ey<!h*k&<HqlM!f=djmnL=lP(v+-po~N<E!&DUp+p_($u0a|)GfX(|nbjFa*995^1wWHL;%V-UpqI2?{5qMiL@e+$pk^&Jotpkc!`vk*?!m?<SDM8XGAG;*jOJc3ovMO6CIJk1O32~OO=Zvxheb%a4e~15Ybp}s=;Y!)2J<N2TS2g^cYHZ^d0i6BfpzPG0+M-BjMD~+QUht?zccIbQttDtTc3>SkUNZWRd_AWI^ZQrNJov(@GNXWQJ7(uZeM07%cbrXgEy&07C^|A3sAW8xVISHCekFVs7#@(f6O`Jp8eRURRyj0?lPNGt5&y%Z=lwShR77}mdJhJmoDW^Ro1uOWT=-(-+<Bgx&^sUZVWW+q<{@eOSX9m*%o3f!Tkgce*KmyB?H!QQ#e^M)~?QN6l4&*1R(UW(3CXAsp4f+y{%=Edj`m9obddMYJ@eltW5&|t`|QOeuPu*t1`<%B&hd~(CRN$J1;b)v#Qkd778zs<|^Z2X^gFaPMFv}s}Mf<sMmPmQNB`C^n%LOPtm$IDU5Z9jn0@wKosjQ!_hCT4XEjylbW)RceUI6TfG{JN^wY%VgW}k*<)ucG+^l9S=d4vNIZl4bsui8YhLM|4Ur{^+oL+AjSd7hUWQCx4{9crP#AB?BNt6kUwSNbZOp3=FK0R4=cO|)?-K0BBtL^TyUWChX|WVdv9AN0^*#$he9O8*=#5B3h?EiWHXFGg<}k1)A~ZYyG3=qD2qYjD#r7F$R6I5peb<<Wo9RKpf@&B_NBK84za~d4;wnUbA1fFfcugVLd>V(GH%1eUpa3w^{4uO*ffazUUW|9ti)f8E*KafLYPE3K$plJ_TrekWoXR#&7jO^MdMO7Jcy+EJbFHj(*n($p^UsdhIoyIz0gAQ`ZcMyK+h4YbOI110DTRd%4Y))neo9_#94puz0?fbS#9aD2krWx5W!N8-PT+u3mKl|srrqEIcY-F~*eqf9n<;v4?Fp#jPV00zdz#wNPoS>_IO;*F*_9-gFV(g=?T|)1w%{?zI7K=h<I4Piwdg#Z@v#ky=KZ{0cvW!7l(p%VUZDbUYP(wUc%X14b`#I`+gnHdMA_HzDcrEJ9n^FZ#}M>>)2ZHaGXss!B4eiI(YhpKh42^fvuHmG-gct`MeMfGPr5+NRUos9jY3LqRUhvhlo-($yO#b#)o)A4L@oLp3&}Vl6cFSCnNS8Du-LC<dl3r7H(4lv=a7)$`^=GKkCw5Je*@m3D9Z(quFR8><06b*tJ-<4`&DS_p|-M%&4hEin^9CrN4u$LSq3ml0f+(S(^snUF-bEDld-wWit>*Lah=AXH<=f^9Pq*$f`sUHGFEAS=`fZa?*?ovDfhFlc3>wzCqO5152#_%B2CSA^|~x??{=5K{xvsAgx^v$=m;wg)#&I57$ZHZyZ6~tajWGq)T4`@wA}gO0vf)kv3xNkMd=hKT3l7CMDf90=fru1Ivpb$Fvtn=DUX;|(|Y#<B_f6W;G2MkIEIpT^y0BT7~M$J7)dXHTnKX|A#4{tqp~hNhf>evzsNj?$^*tuiQdV~sd2sj_Bq8c+r3FjpQPRN#}H9A0)SL3Qqgo}<Y()b_F<A=!>Ar7iZ<W&)lpO4z;217m$bk%MCil$mcTh`onIALe4~dt&1M0n5=Clt)CoZdW8~L^yO4((jJH}+EaD~}me)CNBOmn&MTu4bU3AywqGtO(!l|h&6Q{ZGxT@bjuQ9T8L67tCoA>+wazBg{m)aXM9TvI|DoY-xkkxm)=G!HVYFCAv=>1E06}D(kTH7zYbr)pmY82~X^NH0-e7li0a{*=;NSTE#3mZE<W}N1#T<6{Eh#qu>-#@u*Ye-ZB4!`Jiq9h%C;ZzUx&&yoScG>!$Oa-Nk_it5&QFPr&CGWBlZKmdu@1<$S#uzsDmW=l=xEvNZOox#VLYcwJvR<cH2)VouBdSe`<jEM91tM-l4R<?3gL9c2=5O0fH;`ZM`yf-uE2|;z0<=9-`_F)h#2MX|@_0T!zy9>;^Q-yc{VTZ4hrIgr$Jd|nrKY^tD<5TXH{$-1Pfezai6muTA<daUiz@b___nYa<r+U@H^^na-;NY9-rjAli&(yC<>Ewpp|tLF798)+KlV0+L_gc<m&sFjtNswr-~OC0ZS_C<l24G-w*R|SvMI7#^aqWLXZFQzQ1JzGUX?xh6E3OLuFPreEN`Xix?(e2xdrRkaUaIGBVYc0_w`RVeee)!Wp<~d)~2893aJUTBbI+^hDOyC&1H7LrT93JTgd$F>n&4AgMqKrxon28XyNd&*p)`TgN`w6&2W!07|jrd<A3@6habQD+m}!N{JYb!10Fp4YuhzfaCAftRWtPJE$}$%_7ia*97%WDoHMu5y%|EazwIqvw_j^;YuB{+4meX$GgYReMlvM3M*xE;>&Gv!`0()C)YhUSPdRP@dx=$17RRK}2)D}!KqfJx67fq6OzE55m=N-aWb%ndG3SY_LmA@}fDDPK-$Qu-^W*66TDu&lnw64i)n4&VGxDy$ZAwt!)Du5Ooqt_ac@k1mVnxt9rfj&(pML(~r%ykw*W=x~r&i4xv34)6CL3u&Yxi-Am;uhyL#W5mZ?KdepuILzFLw~mxl@Uo7|qFEbe=Co0la1!WDYnV5cFfpXHj2votnPqg&e$rhXYf(iFpTb9o3>EY*1kTS|ZtIXpYKVQ>vqC>QZp?EXonx_SyG-Tdz6fUsIcUzth0WMfm}0zH~FSS<fx1Ey@dG#Z#6t@`Xtw)xtSY*ebvPCs~t-GhPsrDWbeI^OB!F`xd{L{B0=o4vE^m=7JgTN0aQb3zX3>RKJQF9yLpwfm-ak_8-I;XcnRBuk^XPNVt@%J$cE@w62J`77i2ZWswms4b3!D5*pY|As2WAXGh%V!u$}IF{&P+OI0;UPDl2jGamJCf4yFRc|0LYR0e2uLn`xVYGs{!t$~TJbBH{y2$cuBr8euL)aiA2dNX^bHWsw{^B<4QN{0ITP+tRi)Y!{Kk2>W&->w-qx4m3cbEYm?EW1o!AJ)r-??8L0W$zKL3<cvc<l`B0duj7j8K$$!FrC6qgu)AdSv$Ei6D!YS^};BKaYCZ@67n6u0s%V>?_^d;b^m+!CxIZQ{>l!~ROs!hmEeJ+<y&aTf)5wVUUGpP9#xacEM|yGg3HqK93i$Oz@+=$j&C+WZFrU&0MZw<>V_@65-_?YRt+;jdxrxX+UV<c4Ry8D3|AZS5XB-$s?qJ&E810T8eJTRB+;pM7vj1;tS{!Lw%g)`x-U`pEZS-W{FHNq7+|{&wNrC)9tNN43I;`^*e`<-CkT4>J~EVK(;v&4ic4`0Pt&j&M1(t8MhF<O|Anhj4VG_wUe>35F5J*IQ@*50ElgrUtro(t4`ms(YV3=)y}-CW>?<ya%Gvyl*wO0*RbzV|S~>sa`FOssaz6{?Wvv~yUPODiTWOv~XZqySZQ3?b;AH`+D2M0A>!%j_#XBzRoEE+G#Oew@Ooss#VgJ%LBWc5Yap2vQf(zioJ5_BFp#XMK+zr;+x}<^CBbeWI38DuD9uwZT=W2JOnpmLe8%rW2i5JBo?80CwLed`UsfgKLUY>%O-8!&YR5S*GekcmI_qB>YQu^v(E0=Srm`qC#`{{k7GE&GFny47MbFr-6{Z9S<_4T)FSoyp?dZ9Q*T5(QM&>M8dtrLiPZ_MUY_ub!PUf?c>gk0Nx$f#wf8|b7YRg3Y1!HyYzb)>T6{Vcw%JeUZKQigcA2o3sII|^2&YsWTVAAc=C81XRePX%*8zd-*8Ow39YuJzBgUb);5p3R{Vd>k`$zXjAw^b733I;TWffo6NahkPR3xgOu|?vUGbQ-eR74c^v=O>6}9_3KPWIWry<v-?0V%x;+paUwi5zwsiYTGqP<4g;T-^|;L`Uw1w1WahisW216+EN>7N<oi1juu_XJMAA<i($;~!oPoYDLV`sq+cDsS1eb)v4()0{uyK%?bgavR9O~`lHPS86zU<g{u6r6HWIk79yLLw%tfYbrQjcW;T$J)>jE1yMYYynpG+#xawa4QUx34@F9-W-owqa95dbo$L;M`h~y8YvZ@*6%MmzerkMPJ(XZqnb!tSoX!HYksI#ikX&#5AR9qDbd0cW3NoqBqycUxk+#nOfM(R8*OYNM@j&1_e|pLOown8)BW^kggoUY`{10eV<&X^LB3Q_;F!1m?o6YB?NrmrC_%+Trt;%og65rmE`@KJdwKg+O#8?Lj2R<(q$Xve6sYsnLdaS-4@h!u^kuVPzH@Ry%fe0wn?-PjBvQbI}vWCYj$1Ppw;I>hTclPEq9U;<;-BHySM;%AiB$F_9t^~b(c}@V``&c_6*qFh%L4&7-fuUXd_n^rvoI<gJ!#n?iJ`<7B<|Pisi0p&t8DzbML*bi8@aB!mk)90&gG$EJc5w*CelVnB*&yb#Vmg%*bXO*r6-bWULe(xQ;DIjgai9%pi*ntm9p1Jl>^5>vZi`+Vdt?d)5_%99m6@qHp`A-$Pn^eZ|JhQNOND5EV!qO<O52xX+qw+a_9y03=Qhrt(~-b$~-ffX=&iTyw1<Ra4YE6x~>ZMD9TH0ucQCbVEgzs`^z;1LJjAqkQ{B>GbmtVi$20X>TROP$W9C@aOfG>l1q+nRNO()j8Swkq{ujB*7&cO3AJKl`ibd^1vHmCoa;2z@`(F+k72XS0i!oAU-;tXJG|>f=8WF58d}2>IyOg>(~QJWm)?-prVjUDs=^Ufi*%SOs42w7vNiaTlLe~R)16nCIY<@i6DP@i!{F0t!2NL`^I|V;))76cBzN{45QK=FM~qRk19{=Fv)G?B1#~v!o|PjIdenV3-mE5PhP}@GD(#!V*nI~P`HqW<yj&Pb@g5~9NM*0c~=q>?2VoUIgQTv6MdYqNmt}sUzyWlSQgSYmCCdm?!8WW-B>}0bZcMVBRJHnxv1ge<fdYg)H=OxtRp5thmsAIgERv8V=teAb736|0KHsYrXF)Tg|Q65LkF^$20CSMKMKuUkg`w&%!|*~_8o-8QCO1{^nzU72rf<9jk6p>CAg$4_3V+iREMbS^K(#O>GXblp3f2VZ38nGGq2s$<)uGZ&AFo^K1R8W-F$`kZt5%B=mEe^EB+_cYa#F}*dYP)TQA(Z`C*k?S8eZ=DZ(uDnzrwL_#T+A#Iy45;Q3O~VHu!w#~}eEpP6S8!YlIWV85Z!JQ~-11T<Bu+)>tCvWs7cO7U-cSik+P&;v?4g!esLQg;e`6KR9xL~$Dt7qbUM;U0jB3RX?#HYR)lkDFEw(Jf7;phR!uDwjb=t)jeWc+r)4m?~o6o<O!mv?BExq(YHQgK)qzU$<vq#p3qJ{WkPDbx^S?*)?o6ABoFuwZ}U$XrHJ`-yE<dl7S(x3F|85VN&dOjy<hMwi~M_)?XS`ZA+uFF@7BV3z^<}X3xsDv+LYC1qMTgFw(;FxJCwfn^N}J48pwu`b#gffOyKC#xeSZopZ7Jf_Y^PPgWy@Ke#!v?4k(UaxU9g<@$4S*lqZg0#uK;fGY@Up1=OW#Ub<9+-Xm?zeJ4zVAV0hglr1dV1`OB+gu0RH+O$Dcx3O+yNQ5T;I0wL-MHB0ec`}g^@OAPrd6?FCa~b#g+2yVdKO?{0wS7lI&IRDI@D3BPGCV#n-Pq%oFT7IWI1<Mj}lWd`ev%@TuL*l){>#mEQC}Xr93u|!;k0+?DVY=dr@1Vpc4op-Q#07p>66mAtEAsAf=dOR+M=9LXnAaGH;U7Fy}=<iz2e{%rR+04RI#L1Dq-E<+ee(R0pz-a)F3-Y5UMM5!lSw*|k<I(a;WqTH~g^3uTBiQZI*Zg@ha1#m(3K+xNKc3u<3lW$%OisxCr0fN+5k{(~YFVs=pZIbQ`Bw&<*c1N%b1N>UbKP1vpb823QvVhnU0>?m&><&4^!iPmm0vh_N!C4o(H5W{u(yd0oRx@Y)I--obefc1q*SE^QWn%UkLI!_@@Q<SG--Y%;glZPE8CN(uY-&mi~dHojVx;L-A@8v8O#UEKOOhsfV#iQ&)k|*ta7%s0vtYZPHhf*YImH2=%lVa!r=t@qMt4KP&@0Xfnr#YwiJTs+e3y#}0b_A^o%rR<NAa=5f(mMXDE7pYVIy-u>uzxUyL;;THzoXa+CjMMCy|BFtoLU=9t(A%0V&)xzk#1ViM&BrdFQ{wwLno8Kb3%1KCeQSuXfnlXUB68w$9LJ|27B96aAKswr`24Ey&pG_bDdeOCSuU>Hu`Q&xe=30?Fa6H{~6)jFy)GKoxZps&68s*0)ZQsA@zjEyiRaVFj}m8A+U2<n_hQOdKwZHTyJ~7+JOS1YlNT1^2K0eZCz;!;{!6Pg%+>nJl1iPTMB!(WYx7#SUSw#8*^@}2fa!vJ>dofG#;x=xXxiw(&Ql{k6BShp@iHw2U2D~MQ9fgnlIfb{LCPKmT3sE?9cuq=WXPD{Ae=XuGnA~MKd0rJktsm?ICPF>LHvnO@h#)F!IzeQ>dUtBCYyO_I}PVrCeJRgM6FWfvvr3ib12u^>=8XAOLcq(!P=|x?Kiyr*<y!o{i8;rn)C?<{lii2ug|)co3%xvrLvy=?-wLYinSFm6B%~RFms*N~*e}pO-uemUSuM<IFHVyX;ZBXr*G63h{t(LA>HbX>nhWZ7C~F=)!^Rp6kA=ILh`K7d@IaA|2KpaH)g}s3NQ8_sf`2tCNy35w|ue&jyAZ6-aYc|A>f?6k`NuSfFFBGYO@}?r<`tQHq@weS)(_jU`7lEVu@6rAHZIN=h!(n)hJ$eAPkdU~B`tWR{UdGk)z6agJvPBb@0b4VUh0iy=ytNR-O+9|gPAQ*dWU)x`IvvB8s@6b>ODnb%fx2Bv^iWm&0jk-{X*Ym}WIQr$u7oTJpN2c!*`Tpb8)fX2_eu09re@55!O=AmN0UhgwVD_kgm1#{X%!S%IR8xu*iC};A9jSEZI90q=Emb#XzZDp*+^SoJ3hU83R>Rh)?uCMGrE=p`u_)C+3UI#i>WbnAsFD>X6&Ry(XG&x9@p>w->OcWU#HvrwO_d*sMY6=k!>k=?Db0&9(0a8vd2A+~GLoX!4-{;XbYTu2MWsfY%z(#icO~C&AYpiW6brN{xKtva_GdJZ_juDcn402+JR?qEdzU!ED7MQ5BfABM>V28$P-V!JX3&qC$!^2}o*9mK<sC^UCH-}=2Q6K_;Nn%+Xs_}+)K1aeX-qerDSqyPU<W!>G&r{Hrw<4mxGj(6eg5@9H=iKQsI$T1@tuKh04Xdn=W;?%Km(V?~%WU4ruM4!jp^)v(TruI(Mitz{-v$8<82+qgW+?q2T0E^~fg?Gxj&zaR$lG9)Re0H(zOrM@5DMd_c0Vj{q{w8j(7xXpQp1CCs-iQdffa$NNKNGN3$YD4)E|e=Wq6uGHQ2a#HJk(25*hmOWcQ$}AP-doB$CR_p`Ub40L|Qn>%RG!o&)6GeEpKE++bZHfEuABg&^_{HjMgx;KN1LI{?Ca6)h@AcG_vkq5wsEp6W0(x{b#f-g^1PdOUq-^EwU(muGm6V>@(7@rI}fP%WJ69R@wO^*2X$7Mh-N*LLVtaamUV;wv$*!mV&??}HrVs%u`8KrZw{6i0rwg3GhLM+NUW1F=g2viBbXiCUVsV2|i9t3pbVBY@Rf6NF)+56=5VV0Wz`JO{#W(M2E42wNI@8Wj!sq0qX9wsap7dg-l2Z9kPr;XEf}Ka8?C3uBiA`@-QuRfyi1-a3!2uInE6$tXSOCX=Me^6QFQES({D^9ls(aV6z2hL6CmHHk?skS5y!)%;9ftov0HMk2&ac`aJ+^@BOzm$jtT^D{gp6lbi#Td+iwZ<DS4z8AABdX|RW(*!h+=mpF_WHnLgU|ITx^%zQIbYHMS_E2<Ox9$XgqcRC#+69;t0u}>q<jXN5nu`-`m^jAQ-?#KB#j)B>;`U!`!s7DAwWS+4IYoLVN^z(huJeX;=wDgI=%H86P>88Zf$S<F`%%f7NzQ@=g(jVYTs-n!POXF+k9mR9PHWJw9m$uB+&5_sdoNKw9MBFj>!cUtw17l`e}rkQpsq2)6z1u`oQmo_KhqOb=(^o><U`=^@OClJ7kPqsOPx{!zq(8V%fgZ^`?k-G>>kp*c(U*Z-tc912aL8&czQd07n@eV!-*H!FYRB4TN#u^SvU&5!{DM)DQTGX_zcuY9v8m+zY=}7Ur74S>xcu|&paeR3yGb`#ZAc<;UAY1XmegfnbuEa+{qkXpT+<;M{=IR!i3a7oJwodsa)<f18+fa8_YU=h4!RKTv4pimV0Y0m3f`3fDenkvXTd4FhO5qHSAjslqfwzsKUGV7|P94qxe|OO_$*Fm(Tt6b$1sQZAZ3iWBsu(OAXtQ%I7C+>f!D?n^BtyH;+9XX0<r%g=eJLHm#$q(C?!<W=A{QqGu*+?G)E0o}P<2YCTX8TPNJ>Hwn}Rr~wiqv11ZdyG<}2x@gb{spqi_nR|s6R7SN0z))2zxpImxtgdrdWd8(nk&f4r##3~@SN`e=xOtf}mkoW%dG-aL)`FuQsc5;_hI^_}{&<<wSC^>oA7pmOWd;lcd@H)#fWYmrEN7W5&-sdIXoGNIyfjG~N$Ur{fvOqA+?b9{=UE;nNLLX|+HE~LwQVj0zbUhXa!eTXv<_`j8N8UXvmp=ZF<O@k3~rV=FC=CUs~l`>l2Xao-lqF*F9~cYq|D)e$Gto$Y)7=W7@xH8aL49S*SSJ&w*szCooJfrwrghA)cHr0$IfWVL1_aUYO4#Mlas-^%=o@brgYZ~yvwXH>l0}!!~!i4y|mIQ5jWAadVN2VFp-Hf_UD2>+Q2RG-*Kz=xp|wHZIWZU*n_!9w6DwV=j=waS!`AC!G0wO=G1RyCkV`i&w&ki)*Zo^A0Tz*(fq*o;kC`lNCegoI>c1FtWRvkx-I;gLLA#xj5l_}Q3Z|6!IWbO_TzCl)>>D0oox3H5N-hL>S+eQy3tIMNiep9sG}K`&PxTLJ);za7daDXPDe2>EJz*OQBFeNl-TBWRkZcta*3S!`^YCfeSS=_!c2nSQ>mrN5Nq*WR0_x)Ha`)POKq-$X)1M)EuRjBYp~5o6fI<Z`>slVv8I}`GNmGrPffqWGVtsK>0zJ~#sV(zR9okcw-JIwv9X)vW-3rFG6*t7!JGK49Jle#by{t}>(Z&=RlS;w=`WG5t3}*QB`EOEqF~+LIYnnL*61X~nPHRA;_`KTLxRGqJ56#s>|DdHu@9eUW&=ulTK4-OmJ)McMn3yKp-J~tpYv6wvKhh4R^?FXt#JUock8f)Cq+RBiOEIA0JXZrz1esvxpv#am{hJ`^3hpxT8b(9G{->VVzbW0H}BW)*Ke;g<();xjHt~=Y1)hhCjeX#TqnX-=)51;b#=h11JjJU;hFqQM74=GXX$m%5OOzm;RoV`+b<5k=&TI^>)$57EMqv?1ND2ExA{hn7Zax>f!r-4kakB|%*8ev?6rGVyt-aIQ<%YEz5$bac~p^ZwZ}*;I+XBiVd(Bg_i&2GyLBA~nj-d|@QDO7wE^3KA@KIO)B*;F9(R~7XVsZCf-BNy95%KhfL@&7K^FGI<2`tHeLc#L?|y#$>C@*|^TYcmW0?=7XxATKe>OjVxU1Row&p|po91z~PDR21L>@(x?m!xMyEzZHIPCc?_WDGxLUgO5l@d0gTwAyc=U04IYn|+x*)P~5=6oR{k`I)fo_=$Xzx?_B>tAmA;MEo&z-M?(O+RP!6Br5FzjI9V*%X2|r2ly>IiB=C|MvBk(Vd{3+?%0QmD%4u_9f5{vxuYGi{1|R$jWYp&_Djm??3$b-QT`^^5@^p3t<O#KV|mUwtKFCti^Uo&Csitz~iLbPsDZ55_{2{GZ&a>3RN30*6q$;w_lUAwQE{@2b`&>OqBJLC3?cUM*v4P>&GvUp?dgjYHNDAi0F*$HjQ!mi(^vAnAm0H)LDU4ERB*gXPdFFfsZ1uSQ8020^v;|ivdpnG9-yy&sgf{?^?SYPXcW)u^;DroAIO&u({l;pZIZ6)xpX^PEql<tRu7|#UBFTPe1?g)2AQT>+x>gQ=2C0=xGXCn`rlOim0#7(?c`^qu*fFNgxZ{6zU61y*%emC2nFgCwtL(z7!38n`w{{A3h-H$4I5IaM^VrYA=0t@CF_ZOz9@(9l&)|iw=WQ>a{;Kr`)kAiupyUR=9aU(IU9*v+w=3UPakHttG{NEq=KG<0G#GzM0zG$vh8OmdqOQ21LHhQbxWo;TRUq0cVAHZ|)qqz<fz~laNT<sVS;`rRlS8@r%jdhUJ7nE^@()_fy$sv00ku=RD(7ce9+;rhRUrstJo%!6Aj0q}=cM7O40)MR}n`F{l`+5k23SCwlEaOT@M=v@set^0&WUufObqb`IVYsU(|auoOAKsJbut`-c<fBQ1WqAtH+&OeEB2Lz=IhSZSKf#XD-Ex0j3l&|35k7@(&Hc>*iDkF`<j-6Ra}F8O$0M_!WRKELbe5+a(3m)4JN)nKVDit%hDvIp$oXb8!{7hF;OsP+<t!Zx=bFfZ^wlf0phEw)YQPZKg^v9Kt!A8dh#-nT_^77_Bi4obSgIh7i1*cTH0Rib$Z;JmmzXS1iG8VsQSYX2#AMX-^r;~0X6j4riL&r@rt!Q<K%$<tE+*pvI|wnh0A0Ck9XeBgoEcb3(H+l#;SWwb<8+g@OMt5j1_x&4KxO8119xRs$m=C)vx$o(-=Se?mXcXGF;Lxf2oD?RBcYwNG04VA4~yNC$R^o#UPE%b|bT-G@)H3bv)8jk%<5_`5?Q!@(dT>^N!REh>4-l?Q%F8vd3u+~qiw$;P7qg^8BMU!-izVZ&#*>)9rJnRh7ydld66b?x@)m3?bu=ajCvdc5v({UTvoK}bi#_u6drArHS_Z{D<Th5_U8DH0adf%wYxtpR682{UG$1pARey4u_`uf{7gj2RhuW!}4a1{#vRp~<wI{C=KSiCo8*yh#!J>~`Of-n;6hfI@fF349?JVLl(V6bC`YKHHrKp7*DLFRPIb(FJ8P2=i~RAZRM2!2snJ76Dw<zkMG?2-AYU=HXP=pTU!S5h{6{d28HejdWJIW&TgV}|Z)O}<3Gzz!@Iu3#(BY!CP#=*!U5;{6}r?{2Y+n-Kh2lz&?vHnHvfAHu`W<b`<0c;?00;d2HcHMXMJ7@^o96-MhG@M&59+MMZikLx8E+oA;-Nm^RM1S}2mcOszU6kmwh&Nk%h0ecbH;LN}CB+2cCJqEH$!Ij|9Vme%jnFYa$(o04vK(08$f+8m~kn#AkW8b;XXo!csxCxZ)k{!oHI*n9{+4o$KFbo{K2=5?yp@MQ~p>f)civVelrzAYi1>^eU%(e|H8ctac{2r`=b8D4Cj52PK0`ZARiV#!P-c9=Z$b}_<d}NdnDi3wVrWG(m*|I1ggOkpL?#{5(e6+tQb<A>Vp^k=F-W|zEG6|E!;d&qSd`WGHb#24!u`K_G+VOg@jk+mwd%iskZ642wizPa%`Yr{nkD-WH6s8o5MjMJgp_L?=NMFPJl)BG}`yo^+v{BoT7@(d$NW7p`T4vmoDm)-Z2JO^KSS*XISR7>oE416;X1ZqAU3#_UaOkasehqCrtPA0mGZ^YFE<j|6?lPL|$y{6AWt3Z4+31%&19mrJi|sC<1|Ct=W^uaT8w?CW_X;9Y1R<8f-ViRpu4(^qF2Hp}UBu?G(G%_22HrpjPb$J`<ya^AY6M+;8BtIZQ>U@VI>cEev;u^T34%ma(X?poI^Kl_;$5nfv#z#;e7MTKeqEcOwW6@wKIZpWR_xwK#+G0okZ_sRCQww*-jfBL$MRxexuq<<f0NsKI*47@4i#}YlGDzwS#^W@ZM(Z@aqT+sS}=62W&}UCcc&XF>T;f=YsWl?Zj^7I@MWAoC^G1}h^okXszHJxQM}@9ZPa>B54fJTDa~=P6Q~(6`7UtD60*ucCAI6jn(E01k<jt&pwu%EP1DP8NtN||E<=?BsjaOBf>D5!pGw<w1sMPcM3cZpcANx&)LsjPG-o6i&6H-t_X@ZqiNuP(yhU2vE-%-2mwHe`{)5`ZU>#<EhN0+=mw^rFN0m2h(Dj~W5!{&X;`vd-T%7I4q`b;y7c9hO>U#G$?;Mrca(fA81J6u5fb2UvHY%26pB!5X=o1i?lE)>h7};-=s9@l^CF}3*CTigD{x7#{*ts?6;KoSl-B`zj;RUc%osUl6#~*;@_xbX{t4j@I?vF5*A$SQuBF%5MK$(u_N)Zr%LY^nD1XtU*08$ruD{ZQE$!qz#ahBcq1e=kiLp?%~>OxGBM&I!z1-0KH<DTMo_(7}$no0%h!(h9ph#+=39PnN49qgtyyQ#~|9a|S3RVUjGV?KA({dIe})=~F4ADRJUR0P5AdB7t7f^8A-ruDKn(jExV_ubJ&A-`S`hTCjPye02JnJ=;<OjEdC=TBg>)%<|%E}NSK?8p@wS;R&i|9V_+4%^}cBJ&@COU*-qL#IfUh}oMq{-&1zu)jr6l*Z$vr=9bLw;$^Y-Js~MgpLb}#VHj)@QMlt)ZPRNX~FHW6tJ|x;LW2QR!un0z|v$2QDS^KT|OP@)O%6?!n_!#`~w21C<j?70qAwp62R6aQcvI=KSduI(ok{@H~p)*5ax-_E<}FV+^EK^Q9s@jOMCW)7c3vp1KUS}5E}~tSNqqU{m#9e$Oc}A$aa5e)CL$D|BaFA=wHaR3^AK?3?T1w>l9=U?f6J*)8oP#<Uvc~m}U^}dFd~`OdaCsdK#PQcXQ5<>@PzY6QcvJV!)fX&Ta%E?QnSI`ioqmP7b>bDN`8n@fHAAn1dbnC7(+1cdJTaWQVtpwWCmBGDGofn$~nti&M0NfT)^gGow4pCW66Pzguf9aXrlYGJ(GexS;D0TNSBiiVH!+2Usu#z5@m(Al3<Q(q>(&8oQEV+phELM8a;1(2-KwEYiEsj}h!*w?gnimyn`KAc}IW3XCoCPb$k1JoHga9xIA9eW6^$SdMg4L5hN|I58ykb#D7;=uEN(cog3AWusK7f?^%z0)x0?uO;Vw)>Pbp$7iir;&By&dY?eo$g+f4`M;1zV;jHtqI7GTcpY?mPK}NxX3skpT@(s~0)I=nLShbLQd9Z4J$;NsX|vnr>siQI#}T!@P>PZ?JQy}Yx<+yl3=wez>F>T9Ws9I}PJ89iaw<lHejivLqGtg{6J~6w*v4tbc3;R8h4e#FU5WW-RejLQVMmETP0Y>TYDpt4LPf(w`Q~Hxy_`m(AQ<avrDz1DXp4QwsiZxOgzoN;$Hu}bFM>|87#*2oVp1%!t?XmTd&9Q0=DhEhn!Kbr(fH(B7tA3lL^+5J=5wT+3MdU?;cADEm>C1YqifPD4Di08l{v^_+8BXMZmOtss&V>R5LWDmPUb7;G|GIem5B%G-uh505f}7Ai@sZ3meCK~^Z7H}^I^)BDLSpuLbf4~l^I$2(P<pqoIN4Wt`kf(m@w~>KoVu0+T2CysV7<xjP2!O2MYL>5xG5<Z3QE1>q-b1af_vjH68Dqt20KfjsRjM9wQQCfy93z-QSO++#YWa`+4*}`SK?G3FgO)ImgYz1SR2>(2`Vw#ZhjiFIrAINz9NG#*RZqbi(tIrwDZc!r%vWD)${khR>?Q892ZH$a!7hsgGZEMhq2u!y)(Gd$wm<?x8*4%||`pa|l`l0Ncp(bWCG_)>yRaH&w*V&F=*TBri<9yPqBS)Vq}!z=r&Fhq?y>Ul(xeD*?Cd&YC;5(}ed*gm4yBu5c5p;HX8|Nt8%}z*Ly+@LJk}0giPt^sJ<yb9qxCtO9PfR4qh5FL~G}>p{S`n1NdIW3jY#O(?KAXeSyHNl!5C`m$>xV-5+;6!3B2^4)GAvJ4fhCg_Cyf82f9awNyG><{6gmdsinc|@2*Gm;~dD8tjW^Z$QwInz~*t_%+kkL-pdJ5K~L06N#mSUlW)T$hpwky*~mz9jg@XooYzzEgpTKK0PDM-8}~g*_BI%+cwAJ52nV#|Qelwa45-`Y51(2#y3WLn5J`itj5t-?xWi8ld**ff*P{jthAu2zKJV)?t2DIE5Cr6OuFhN5RMoP2JQ~n{_eN(l3@?t09C^QLy!3WI`S)3#79i_HA8O(dWL*eUaS=(o9GiZlkK6_kz_ShhwMGPc{<*--bl-*LlTi1If$)?y!ffE38q3KF$2Va%c@@Eg6xV&2xJ0W|Vw$(e7*xmA(nJ<@i(2R_4@r&ML$6iz4E<yfUAY3mHrj)HKv_MJk;V9quvErK5nwSx;&2t#I$+S9#3kLRp^cp~VcvnAf<;v8{J}z75*K6SLFmbse`%nGUBKIb;-M9d$}>yEW6OiVfgSEExyQ9CLh{GGw-OnmRkxIr3R=D0Z7a2=AIRl`0oHXs^!$9`hKJjthF0O1w5&q#4`_XjTc?ll>dO11Hy$nzrYFrp+t!HTm!wtD~lh*M1J1%3r1$va4~yFA6!J+dZG|9!FP*?6z)mrsY}YQ%aCGYQof_yly#XrL&`O-X9lT9!avsDU|b}oaY3ULtowSgZz35>~-3-hW|8U)53R>a_EG=4Z<L6(&i;oY=kR$ZSpOC7Mvh8DB<k!caH(@vii1-WLd+H9bKpNM=e9}R;La@*aSw?fs|yQIjtciIq0rw1O-hl58OXVdmBHd=b%G|XXvnomntOvj9dJ|IdGzwT9zkeSl$I*pq@-68uS@KmsKy#(*kO^?x#2FB}ZHXSoU1U0Atw)oO)7wxE)m;_1%t3j{WR;{i*9Z<-5FJD@SpRV@|eqN8M3sKTvU8x&Um2K_3wXc}O2xYf<S#Sx183%gvf;WM{R(;%1V*61V34hd{|KP#5<tbKO+NlIV58yp;(ME8!MqZ+!!{4M>xs2s|1&b|;ZtRd}XrL+%UD%za4cnXo74{Ha9oK&`QE{FPs1{sV>(2=;|%v{Gc%b(#A_uK3GMK^q@3fR(JX&Q-%Q=CX!PAaj8+taS<9*$15hlfNdKwgC({ah`XqS4?b8=*N<C%DaGy<IBE49#P|Y3S9VQP0(7{3t|z|B2kijJMMe5$@D_$lyMqe<e_-LbqN6~l!;X4*J#MzlZ2oLE~qxT$JTA&Z&arANEuEY9=W=XvWd(PPT~R&M)vSk_0R7baRey*R)Aw$*UCWdF<Wv+nW8pi#!?h@aGZWsd7;&RHiAz;KSsdr0R0&+oeuu4Qe;>ipx!i?H*ALhppY;&j>6V06h)yBDM0>VmQ?R#m_W@O{|IAaAo;j8EJcBtHN8%L=00f5bd@`-t=n{W5cJPn2i*Q&n-a2L#6mSe)Uee=2qd9wI2#%HLJHZoJbfXB#%3O(E-qa4;o0`iwB5Uqvv`4$1*ci44SDjpFModCKfe7DC!3*Yl*~rVxqRInI0kpW3r#~r0QSAst~M1){l?Q}A&t^~upPWFl-1&Ti_ge`k@tykr=tXa3|qdxxFU2tRa*Jj`CjZw1wmQcdce<%sCABV8u;e__(@|Smtjn1ttUUM57-Exmz9D`&yHg?atKFPI@{BqJhpQgCbiR#s}N|yObVVoOny%m{BllaR<)+M$Rm$NV(<<+pgGusWAhuTzg(YXAkq=*R9!Geruo}{W0ql64;d~B898QkgZR663~rN2K0R0Tag3Z>D<caDmvlOpbWh~QLNNyCv_ZifzYm_f=El;I12YbNq_HvqFnCn;qJBof%FJxc;D;#tA9cKZJi0#ANhdcXH$zh;&Uh#_Iz4k{jhQ5g#ry{Ck2(f^jV4j_)z8IfHkto;3wSr5{RKigdwPz;Ii*E?25iQjdBF&M{_t~l6XP+5yORLwP#>7x4lox!2R7hMkF?`dxkPsDw}aY8c$&n(?qMy|E@pFBoqx;yICGaSLF+Qj&tj8a@D*6{Li5rw;AnVBetem#$dwZ{^+-Vc!V=}oE*zpenMT*Hz$^;brbSK>e<%^oM;HLR%a{WzEz>HG{C@E)ivwVe3i8?!L)|h*_+#$5_(@6P6?r`~OT#FyQ=Zv!D~eknr>-dKDL*!I7s*NwggfW?NI2<FujP$KVDqe3&v6kq)s79l9dfh{>&7u^fh-MhHn4aJ_&1&qp0@P+Io4HXF@{VwL5wIi7R&nG%e?jRW&p=Z$47P1shbPCNA9c^Ftcv#z)O!VgSC`pl=+k$BI^M6$G|l-tUkt96Mz-n1(em)a?PeoS#>w{HD6_VCLp)w5@T+3BM_~%!wRpEQD5EW!Qv;HZ{Dxx_irCF<(e%^rj_=qI%$`!${eC$*FH0owDpDLkIr@7x5a`H9~OJt6E~N6f;74ZdO(7(;b&n844)pMrg#dxGTsnp!K6RNa(*zFSs=2RndJi~YI@$08^I`Tq&*c1Sm(Ir8Mdle>hc#B`PML<{-HFV0!ZR#2f$gFLfmW`%))T8OF|g;DPCWKV;E?P`0nBp3TA49rb~JH$LG=$Q0*C>%ycU~`eu#bicA^zgRKaFa3yF)oAbkCE_j#s{qc_c@$I*t{`h8o_yV%u9&g!i@4tTg-TeH;cCp9!NakI?X<qbW%{LY6Y1P~87xst4FGMMsyEWox(HyHk|9t)am&ZV{=sJw29gDGXrDGWAwb*Cy=a?|>`eTARSvyLB8-ODq08-x42l&H0hOy>VEA0n|KLb8^%k*pb9}Nm|@n`RS6=U!b3ES5GjvbeyZFCwHC}bXg9IdvnK^d#&-ge_~w2;U@L-?QXe#uY2|MJ^UKg{so-rxWJ@Kc_c;jucSEbK@85u0sN-ke~%aJWtocAIoSQ3$3&G+Fuw&Y`RKsmyZKg-G0-6OYlVl0R?^t(Qj7X26*UH;)+Mnzpc&D+cNq{q?E(pMU-G>(BrD=YanBm(M`f{t)^OP}wBye!e|gu+|zm!JvuozU_9Lju9gYhEE*w`CRl>RX;ix?P2R&zyX}cX>Z}o&7aoi29DH7(dT2+M{mnkI#rIH43&WO5{tkH9Yft!G6kY4`w<5#_PjT(`WjQZZDDSXi_|o$DtGIoHscb(oUPXeww4w#L*T%;gdGDQyUHxFD?koDySIJ5tvoav>g_YZKskRQv)jQN9XH*x{32L;S~>uWUG=+T8T*K@8oB^Y(>tz5wdT1cS@br_`uWdot}nhlE~_jLuay@%HgS7Kis}|7Oe{+14(b>AQ9w?cK>o;U%x;dgjb+a3xDL4<6Aem3`v`&`_k!Uys*Hk_rCj--B<g*%%-zm9_89M=`^lZu>QSR-7A3=mSe}HnJ5Fg11rw$jGJQC4(7Z-P!6<ZO(I%|~>hZ-fQXCt3C&*bxFr*8|GWwk-20!~|i$xa4jP=r(ox|sLM6r^}P{H<QlSk@Z5~3jQa-d0W+{oRyHNh`!lc7}hk9w`v{xq_b6yjl7CBXIL5Gpq)+eUpet+xg`67f2?)aI|))otonOWv<5!nea)-KaM*R@X;_dvmENM7TYbV2?}3`cV3UFh)~%x!uVscPHAa8y*v*{Pu6>(sMg)fIy{4oCb_>i&$#NB0!aDpNWh&uC$vIRaBE}l4wd98yHY(P3~Vn{ET0;y?ydNJTdF2HyC89!tsphx;7Y&%?iaI93aVi3(d!0pYsLV>b6647jdS{kW0Q>naWqd<WQKPX;eP1DhZ3zg=~#G6$~?fls`MLS>34`#38?1*F5IGP&j6B+FGnD1yX3t<#Ds8LNfj=mh5344ycA)N8YyBupuWz?8Zj>lhkqO2R%QWXbJbe(u?)7w9!jni7DqFGnj^<v(3olB0lHBv8^;z&`U~l9M(<^8;o?qA)JqKW2-tS$B-uVWOsx&5p-RT6ZyHH8iJLMk|Xp<Ns3d9bx9;LHKMSxa2{oR5t)j)U<+SsId67}fZ99xo++a?Kb?s>Ctc9hZ3-iqW?I_Htm+z^V5$YeTi{`*$UFC>rli^|rNGff?8R+hY++lNMm&x#_)~lVQ-f#+<}`%vDMp9#@-+)8Mzqs7KGki^pV6+h%&9)Ql~-0SqAfm`r%J#xUqAVnM40o^T5xpbqEr}dQP#(>OH^`bVu=vnVDk<(07u6<yYS_lL5|oA^%j$FN&n^^Y#yY|ZXUs2-X(%*y{?OH8rLM3VR6h7%3Kg&c^>x8gXBrk@dfXh#q|;pJTT~o^OJB2#t=MC!cL25x1+Q%g*~kkLyDK&;}(@v$xx*f%R@&AUD#=iX?=Jtn&z%R%xs)?wZb?}lj^^sHyAOi0Fz~<9~+nbx#gZ!@C6eEmjoys36^OpeJBjHrZLWfAsN%5!Bn5covRL8?0bTRjlwIROD{T}ViPrAyfu&e(axTj@j8aFJ$w8@4J(YllZAZwD(+9hTVoj*Rnyn5?L5e3Wwe~&!&qJ=Eatk4IP1J1i1U+GDH1U0X_k?2I_JB#bnfk#J0WtEjKRU9W>%^b7ROMGgu<Ok>wv-4eD6FpY(XwmKpHnO<Q&4*8r^b+EsCDFPEBeQvd^I~PK@#93{X5ttA#uF(aNpeNSO!Bq++<d&CW4F<m(?iM!Ksb?G3nvJKbn{zpQZI5l@#f-F&2c!QTgPxPq9Of@!yNE|bimC@~bqT=qO|pu<zmbA2AyGIvNzieVw?W*3~vB5>u2W8+`ZD9G-I;0xUsS7&6Bd|A(bmx<DSY1FAK8CBiL4UfsyC^!HS+4GfNW$!rhoj4?i#_)=q)KoSM-nsFlEYYC(@EBzd(^JJzp8JrZ)ekY&Y=F!)4C6t&d}g!w+-@_dgFFNDiCk66g7@KQ1LYec?r?JKc%5Q3+`%dcBcQ>9N++K!i2m&Bz;``Zf@4CVd;)-jeY{J141N>+0&B6-5~Y`Yb@q?9%}q5Avh+L?Fh$lehp_BXhgF-ekjxS;^wuJmBuW2$Sl98&s|j-zU+mZd*V-p+@}Xd@c%EGq)Hw#a5a{angYGpIMPwUqq6oUZixPQd2y4CX#2WZ~j1qv&)Baw<7ql>7biv4N+G34jzk|glWE3tFfLIDLQJ&j)ozt09s8QXK=1i?eNZ_URiKBB8$akkDqRq#O<sjK<E`<Fj1jh49B}>$;z;0(i?J5h4e{RZ^jvownit}J?24A|b?B8tS$x4}dHNJ*~L+Vc9Fv;81`^&d)E|A!J&Dg(#k(azYc;woS9%qX$az<FB=AI1KQhW9FstO%>MZPX%jnin@re*1D+fl%<v`0fJSoP6Axz(&?Ro@6}JyG#3z=R7>XK<}H6+eTh9q~X|@hSEm6Xn8&hJ>~<^=M%$&Jpt8c@|DSZRb30lU)a0w~PWz87W+XOsRuY?A*78<RsY%7xBPphy+$mIz~Ck5NcX01Q&<*fAFbh);UDhc3+Ekl`}FlRvN>^F`*)7YBO!<tV4*mhGZ?)T2(o5@;30wDXkRAM(7ysBJ;&jJdXT^NwxOOdar$`9F>a>qy~6}8=ZE~{%q=535shS>X5V~-;eKU_*B4ovd5mCY!*x<o_5#XY!PpmJ^lo|#ng#t9TC6?j`5A^5$V;L6-TIOp?U)AQ_RO=|2&p@2oHGNkNGaEL`~Z)lPm%QKwwS*NXGT51!cBrE9#K}<{RV$kW-^$;WB#MXEc9Kq{_C$=0`wsE%FjzN-SiNpBicyn{kP_=?q~F=vtzFfZlZzGRcHP%(V!Gav5NVloRuNu0U=K+P(_4v_(+hNXJG@^=N<?oV-|pbkS|}d(@wK?Sxp&l|V8Xj8h-lbgssJe)KWos4Wu{!CbNha{~6@*R5lv$!VYZnucw~TgH3Zfd666?QSaT9jcMp3=qX;U&k=Zz`SEPrLUnlbQ?6u<#>EGIG(hzgJuu>fq`KxUwrVynAsoT+M_`O)(88B_`CjSw$6TzDB2=8cNWelL*C^+BcxkP(q<&%V1_XdL%w@L&nHptdA}K89>%@~3K|;NZMwTOV02Q0z)jre{~d##Ium$e7mpN3`x`x{X+uyr`A(H4%}l^JO8&rw#{cJE{+g)CCOL8Ep+0>YfukP}P)R(^4INB}=|h1pO^DMP5L?GpZWu!&v4O1;o-=3fn(&&3?Wv>b$E_ma>@kYH@3etxWE24sAt%{Kp2y+Y1DFVdwMT6nWjTl*1`LJmWge%_*cV-(ilGntYh&SgoRf?gHK^^2j2ICNqA9Vu!!K#o9+ar_zi<O%Rj6bhYmeIu+yc!z3|m#_hPy@Y31t?LR<xr?*dOXDix|R(>^Vq4oMN6E9u`K2NGtukuI6JE!HD*J@DCnbOx0*zgb=|pH{>h${Ok4XR&5SNXODvq53>VxoTsr1&mn)V<Q57?aGG>YT2`uKrA4=&9t>yB(--4-0`ybp?flBZb@s+{U@NLKzpK6ALNGP;aaU@^*8~BF(wcsf>l`DGXjUkXi5sSeN0u~u9|K!ev~>@i1j`w+RXoO)WL?qIGj<R<XMwP$5&oV-te#6@CJyJ(*)h+9dN@g)hw!|=5lKJ0dh@8BNOV=C3?>8r&}F-ntLJ%o#rcF3RpinE2Q<uI&+{xx<B0vgp{eS5oD3JqX+P&8j~^Cs0Iwh6)rgz;=Z3%KNUa7P@V%AiyuQ^LfXxn9rN;ys)us0@s!PxF+7pYT#uG(YV~T?kmuce|@20YUaN>8^8~wp6L}9DaJa-a)ff_7`#E?%741jQpii}}{#clxbe0R0+9_FO-1fZ;L89V9x@EHt3rk-S?RB|dUE#>j|<5wX;RKrqFU`Qcji%_+EsMS~J&@z%5dsb*d{o+P7ye=&JKuX25oPtQu2}a@=S5>yU6KvdlZo`x$m`I5Drl3z=%R|MOP+4X!YhN5q5DdhF<zsZ?k+Qw?U`on@bUgbP9LTUyJObKyEI`5n*P-KJQUEUHgC~)V8%sAlD5T$yMpZCJO5=UcMX8f~D0KpAk|E{AR-tS<4u_qu^ApE6Lv7HL2M}_9wRA9}(LN05oG}7Vy3Xe^R~f;M7J_-J%AFGGu60oha73dfNCXqy0vOOLw?ripPjV{Qqw@~p)|<0+CRG|j4jop+A4g5RvjGMOPG8;S+Pjz$$WUd*QOjts)aU(bcsAM>AtX>4zbX~b@@$}-MNQP{1ME6PPYVQ=6F(mA?0Tp+;Tp_=pUY_RB+%x(%yNa7^2dnV0|%@OQxCjgGKMiHc|h<Im>i9w;c{lqoZa$Fyr$PNLI(vOo9i-6`sA+#u_Y19J*MkF*CHqBAWcMUTD$I+Or!x05O7y`Qa!jVdO>p8q(kP{$=Ibq;|(d)!M)x)6G9(y_a!C{X<LX+yshs&*}<=aOz{4h0!W>12~H8Mkf<enq8}6N7z|;fDPK~L7_9h|I?{|$mT4#`64!ElX6?;+J}&Cxsfo^cK&~5?Pr<qux!fJIC(FTxsP{rr;H&h`BEehAe8$PGb$CHSvSB?>)ACgOM`%5`DrBN|enubb+8O3iIEU7Y@S&=x&g+&vBG1Rw@P<Bq^Rtadu!(y|u1A9lv!X=UEqfbXNMQlfjlic+RXY5O91%gx+n6p@0>k9<BzuJisq}y8ft|OhuT@@0FT>{qZ34Qjaj(UFBC{$v!jdLYTS&Jg34Gb_V=qsoSH6k>VBTcmp)5~wkY{mn7&Im5PGV6ffj(7+iB#`?@>;&cqlA+J!(&$9_}k}`*)U*$GzU{CNz@~VCPZAt-?j{4Hz_m1yqu*?Nl>)S+upH)x+-e#i!ZIN6UXmDhXFUoZq0^3V>3im^B$ERgU4O!*?9QkF&qjp1r6nerw`$}{SiYBYgbY#>R`mNBzceMX`+WHoo$2X_>rG@J5O^)8p%tSM5vA^@$#YZya0`~xuMgbdxON`4U7E48WqPyqi8&mj=28qWBdXIGRvFj`8ZG_bkO7A2CN<GQ~IHOjb<>h-S^WjJe3?)Z<B4FHTQDpV($JT4LR?7tiSC-RES+?hL#?4KgKLW6k|GhDD_AuPKzfDB{b`oK~@{g=YY9lnT|s73UsBR3SoP|c^VYXh%ki$#)td%9xY^};DQFnc%hj(l+dXX8t_vdstl!LsYQ>3wE4y0lrn@m=r~XOg6vt?n5q-Hl!kx=)$b*yBywMAV*)`fANY<!*?Y=)P}a;-FG>%KSeN#%so?uEYzd)_e_!`X8TOv;6^5y|{VYw(&J)BEmz7-}G7h)2OL3<ea-ZbzGXdpd4Cc1Ca~#!-vY>RH5V8eT&lu>qp3B+;g|+WUATdPzE>#Npd}PMCo7RAKJ5mOr&ISc_Zl{SEi=HFWGe11tpD1++K;`?f63AC<hR+Ki9={Gk2<ifXJG-bdFT57Zc)n@)5$0UVxOO&uffGU`(_Z8DDD<?a7cg##gbP%!ZBrHxu$k*I>0rT6mFWyV>y05<O3W1l4QqI5>ETntS$p~<78zFgMuvoeKY&4Y-rH&H>wgL;b{^LWo0=yzlVYN`GEFH5*~P1dVQY$ygha6o`wY*si^mis`vM4JR7fu|^-PozB=9Gj8S6kam8tepo3dK?hoV*KD_MYHrj+f)eo|SSG%k3ASMBsCr&X3TM!A_Kf_tziBWM5&GcU_IhfPLC(iT7(@&j9~DBm0-+~X|QAVXTzHng~68z;Ap&bu-Xo%hlbep)V2#8f30_be@@<8aL#T%BU3<&F!B7NH>+u_tAoUM6JmWhs~WIr7d#QxMA8xk(wh{bMtEm)&%PY{D``0t4*Td9)p-HGxdOCo?lgN&_5w;5HLYDyct<5NVp`%nZ!Sm(xAj0VY@9^%dqdS8Gi4DbvbaK!ZaP!N<5aJslIZE&(8kR04}z(8?Ui8$_}?JpvY2*Ej0&BauTH@|0_^SW3DPIWRYNcFXwM+b0XHbN2?Xx=Ju~^$p4-lbnV1{s5uth1G%ryxJ>N%AB|pG=7$wLMS#MiCZhB<f$>QSyEpdm6s{Sx+=|Mm-<@rOv-!B2uh>7BGg>VqSFzl+KM>*&4Ut>$Bj7>_1u|NrQ77-9}3+~+yw7Y*!qMSI7KkklmPSKDgRI}q?G-&&j!<WqMF`3FY6kiDwkY!v_sHf>Anpz|6pm@hM4q8;41R{=Q%A9BfBQ1p(7$<C^YA*JxM0+YLP~ei&W1^otCCyD(X=3@dt=#bxbNnG)y8&^<FTqrL!D|x`T|4jel$~qfE;r8zVnUtxqVn$U>(%jh9<i2;7Y2zdspNW%k&HL`KgDF|dx<Ohhu_H_4lZr^lV`mX8y7#}fMmLpfthD=851{SNH;S=e+C`ytjAoK&(Y%a9+fO?}hRc9vO^1h!=v<HEPYLlLCI)z0@+W<}sjdJeDe16vq{oIhRx8wK1$9yl_$LSm8w<18U>4L$`x$${!UJV`3&IrdA{&jmvN=p=H<iar?Xk~k7rPlaU$!b6+yXS!RxRmW`0_#T!Q(J<*@sdL#B=-VZ_ClMawUVjRyr7Ls3d3_<vF84yA=Bos1EpE0`F0TW&S%<_G`JBkTlBqU}2xl+c4J%K7CUDm=Wm6NOFJ(Q^<$g-Tk;IM*%+881vxqiATl5PtXj#L)R|;0j0MVQ(M+EqbK$qhgmp6<_5Gw*vO^yt)Lb>}!33I_oNwl&uaVM2^J%bot7a1>P!!|}xW-VA3T(}`OLP?YjNBdHPETz5*X{CIm3h2l#4Fi(Zx%o^afLTsSaQq9{Tf&*0zD+}oM95{VAP=4Nf`9b#QaWiE0d4l?l@&Iw;`JZP&1|EbKZ-&~o|u6di{+_Ksl#r2Sn>s9c*w$hU-!TN<J-^w`pX{%J#;MBB+I^1s*6B<4ImF<aiZEoYkQyAEKf|>N$^}a%fVnaRH6toewVGt^Z4-nr{Jm9d&%34w6D=t6LolJ5yL=1BLUO&8-(!GAvG@zF_bOiXvBbV{{hU`i0nZuJ9@&28?vXUbfc1(M^uF%h$p#AFE^ubKs}^#abyXy%Ur`FRqk{zOO%xk$sW-SPn1;sNY4(oA%D{NtfD)}Wi_ZSGT#d@{xB6yOcTcn=m07A_Ji?GfhARuKF;A+bV>Bi6Yq#O1X3J{%kq1Sf;=lz%T9SonL;lyDp5Hz{|LP1+9|J@zAW}?Qiegm(4ffg9AjK$4ri&Q)idfc6Nf-3vakKtBbK8UFjOud9T@8-^YH356t9EFW!z@);1=JfcjfH6tY{LHQr<<Y$nv?oMbzv}9YXCk?sfD4x9#Zzm&!Z$br?J3#YNdv+ZL55lsSjLw)9T`?Sf8niQXS)Xg)u-ijq-pKymT{M>J9gnZGzPHA?d6EsYuiTU9#2K4=x@Gvo19nWkgR(fi7=FPzxLhrx6wl^%tN`NS64-IUse7zvr{ZGbbfs!+*nra!>f#v|*5EF--b-tnTd1IH@ZwPBCS(CMV8DY9zL!qCSd<Ad?!kkZcNBXP85z5_v8$5FjnoQ9gC*qL+bw`0{&#v(JRfsoNBadacVMIAel#+f_i#T1%0jCf3L+%eO6OnQOFBL4%0D13COrw-@PqpWYt0M5ywfUR^@-(wxMI!2jW44?P1l^h0=vZhLp@O>7!v@PxBk*<MLTgD4;>X-#qh!upZ#2CfHWqLU@Evl4A(vNdCpX1-<=!y2}vaUUZ6;Lo=7r;xMhN!haXyhSnxp`a*al0B4D0_8n-c$K}MYiXIDi^qJOT+CHT~oZ!ywQzgMIRt+=beo8lIk?;eULDuUJ@@7pkAO8{xOj_W?s(IT@qEvEb}?Nisy=lPR$fiR`5M0A1$Xrb<(OjE!`DEy+Erq`tlNze=Aoxkr?JiqLKtpsQ8P#{ns}`)k$xxfqiXS_tQ%-H5q`+82$5Y_VXb7y$@MIlp)e^>L0$hEO+J%ZXOYTe;1cxl<gO3o)UY*aPo%Q6MMbp+`CM}rxdMX2k^%8hUPiPv;*R(K%|v>s9|S+or~Vpkq}V9D@$u8LWXIsPx%QTAVgo$WA8l%^P>8_jDA>Y!cQxmgTeL#iogk#@nD=iM-#fZg+=wWYKiXGXAiH|c<P>y3@H>ii>i-HT~4=*7?M7L(@V<cYBcmTf%St(0Zb$%iK2o6xz6&;%G9ipQ%k>00Qr5UWE$Qm+8Gnv$9F~VS>vu|8+MVCs(nOJASdG{!x#X``YQgFDKfg02ZZlJ-A=_5fMM3>Z-8Fl((y9(r3PbP@)9E^s!p^?#rQTb##QCqWJL;$(P37EbSE(`m1EGGj*KQcn^6ZnIPLAr2FA8`BK(*Gr|xph=-)8x3aN6Z2cp)Hz!;|OW{20Pi`6W~!l+adwd!QX;8Q~^x(sizC#p^_#Ie*b!m%7f?IJQ}%<W3%ULRh}6X6qM+1@Nj#+?0m!WRWvs%ovO;()ZOsy8C3;KFOQ^oeTpws|pzTsJPSYe$~#<5DaL)xLE%+#lxF16HC9F>*sz#7yj0OyH^5zk-iZ=d?YyEU!FJm*E9^VWj^6nV@7#ljln>V@J22srLj_B8fajQc=4ulS(!U85HxHO}f~;zvi<_yc>bbsBFj<B5>lY+EQLYFDglZGF*_r$ppq;bBStBhX~$KCoTv~xsv@ki^xm#QnG~P{c^?`DHb)rdXfT5xe)o(hHB|HIDSvn5%MU&H=f|gY%Q_H<wH4Rywt}bX7j_2rrHoAf!HKr%A|&ksCFLWXc`hE22Bc<DL&EEI}=VqLv`dI*C=5Snegb}y_`bBbfg?r{87NGhO1AqGfeU5813A7S{bsKQ9}h>YXWX_unFDMEI0f{w(mu6ZBYpmM4A||@>T88c?BhJHwnxMG`%lzK!NlhL!Y$VM-G(-)OMpmzeKV-xjj3=9}`P4H@F6#{MLBepG90WVbWU6xLe4teQ5lSC&Y9OA4%Zgft<p_7nnXo3G?NS)4J(oyx}9ycqa4oCvF~M8<mq0&_MJlU<VRRd8U#Zfa}alY+-k&0{rkv5uQc6Y;%Iq0~`Xz0vynOu)$#ho4OU{oXBxGZ~LW!&Sc%eB3Jzou!tac#65zC9Q4cc47R8g34j`bz)v8>a+TrR<C>{=h}N93A%$tE6&U)tdM$O^^n(-H@|YBi^+x2#Yih$36sYft9|N0o!V0BF5JEl4vpTX5eHJI^^3@U&96`?<gA0Ff-N(c+@-yS$B6|l2oHdo&`9a?SX0`T^q*um>unts~RmrKpJ#@5VgwH;w{Nlb&>km2C$P6+IdC#PJ!$?F=o2c;|w9K7GA;wbdHDi|Gfj_=wU^VPYv*aG>Xli(eFg1u*zJbn-roiL^XV}U{A~WH+)7iYVR69LBU;;V`5h5lLL=;op11`*NkC=HGM&wD-7rKJWzyr^?mTQfEOOo>EF#hrFkE1#TzCS*bomm?0AbW-%ZZt}f2+BfEUPdGJOwVW1TNxNlCxLsUFf2Lh(qnC=b276&8P=XdBtR&==7(5zTZW=@X6es1p{0tYU};B^s&}#sLP=E3M|5UuC^4EBe=iMH(D~3DMkC6`L~*H#c#7qmmWDity+JlavjMlPcN&+pmWDluDjo!}n{}-j(Gn}2gJJHn_<_x|+z&*bTE{s*uK#j=h<xqFL0@^!0Q9a`K*5rDX>9MrG%P|Pf`W7N_-T}fA;#SVV3<)n2|g!%z|jRvK&$;Vo_qO5=$Qw|agn;5T+OklfqRe=q@XO;izZ#ct8m0J3XdMck&4RTL7%IC0G5PVKL4_fm%Fg?Pr>o7lw(Un4HO#-9z#ByY77erNU(^?6tDVtVaYMeE%IUM1TGn<HW&V(br<`MEM#K43CxN!)A^j~9*X>|(HkcD2@DGu?A~pp)1cGF_#LE?vHu8F3&F_7r(LcPv}1CbkFROMU(l(trlY*ROkrcDUtS6CH~7Jje@OAvj-k)J;Lw0$1%5LijdzdFSF+Wf_kDNmz$@@F%T!gLA!OYUWvIoh1z;8LP1+nYm0LR*862&`+w0`>+Dv+UGOg;!HFO;loB<;j+nw&C-PHEfgr}~Pw9%<J6yZz5StL=_L|Ka*w{1p!=r-ntX{d*+2IZ1yfEzH5DTV809(Cnp&Umjv{uwMnU+zgg);SHU@MMQXx^5-`to<yroYJesn47?GghT=uYw0}SjP`~V-ss#(*xgVBvBI1xh`{mnBvSxJw{)?<=s6iZPz(Smahf?vB1DfJSGr-RL(^_PMx03MGN^47X3*|4c6K9<ARgf|^lE^Z_X8t4%8)Clv*}C5Gif}+VBljX(JKoUKh%~(KmEx1S76Ge0dJiVW<&kM>bdB?0sp#r*dB5)<0QJ>s+8(EnR70)%y%pitFbL)eSxm^OVIyB?@Z)#JlUSLBq@Nj<Ev|Si8Sm=tLI~4?lB}S=c!r3gyTKSKneIYc7Aks1pB!@LzIG`i()#ZeHOsbq6esnn_Y<r`(xl+s5D7icnsEz7?%}wq&dv0j~qSkfBoz6u|B8j#HF5=rK(_Y>g|Y<n{Aeu+@H<4Khu5Wi{1l7y?5GX;yNlZxOZ8{&gMv-uMXQ${i`TY`VNDsC^X-^mrlNa`<N-GEn1?4=Hmv>U)15Ztg}qhonVWWh1#V$)ihwBU4+Ry_XNST`~@lUf}C|pgRT9L8jl6T`yHf}5oy0I&Y5IsyEiTLQs@wo8`2VPP_jF10(*LzlPytn3bH`aOo7oylyy?tuIaN2D>4DWKk$4&G$3X=tW7&#mwoQxnufgeM=<i^wLVQLFwtO!T==`S(jY=1hTFIi$GnT4WQ8Hu?URec{0F|c{GziqB*TrTdTAQojnlO6CnR(a8vvoFde`c-o~`}j{=@K3$rj>L*jkM#T-!-DO9BE}^720}>#<U++`O!)E+kq1TAMhxv)!_~43k-#nfuDCg0jt!g#>i@&~iW66`yp$deD!)06tE)DUO3$)n&y?HktcnxPOu8HZFWhp0DuZfRuBJ4Fk+=7*RV{L<+_jU14^faI)U!TKQbhn^3L0ZfDNVb%?X<!G6<JitKv{I5p>yyITD}zWw&oAK%OmKi+|Td%XX@z5n{{cl=Z;G16gd{YUB3u&!gq)u0}=%&(gO7548y^KD@Z+Liq`?m_8fa@LsVKS-57S7OlPiT^u$Q{`HLeO%leN$a?_E5j<)ET!kHFy4;;?sd-zv)z~6I>6S~vp*bi1Dmh@uP^@^_$egfc*IovINjIL*k52*h<GY^lK(B1C$-vJKb@LgGV(Jy_B6Nnh!aI`J`(BAzrTF{(_;xD{8u-;I@!muY<&&?8Ni&$MvZlddx{=v$BV}^9wG#EM#5s_)W=Q!{x3iM{>yJa{n+YnA7RPo-s<q{Prv_su67+&#@U=d!hHIBhWGoZ#q4gV4mj4ZE9~;II5tBPM_1$7Gu$hC$XG+i{(t`U%dbEG@1LLi$G;rW5okl~ubrp1x%SZ<=5wS)wSJ#=%zomv;^gI$HTz<jAMg7g5?`Jk-Ld_&R(}7MUDM_}z?MWs2Sz<epbHO=Uy%8|&}WTxht1TNKSvLr7>%=Q@A7wEUUa;}=e=pT-|f0m%>oLDfM?Jd<;>6Fk|5KG)CvgGH4E<cb0|xECD6$t(gcu>#QZq=yY`+eYtKpr{Wvj(a$LCR@sw(_dCJ#WcC`_s9poy2PQ<p(&jRBmJAU;o&eOe4X%azQ3yx~t+I?IjfSvOekp`CNH<;H3K>p)e<UWw+^F3br56sCLI^r|>DdKUha`A@`2s$?HJE<?bUXyx+S6<wMPmiYc8}lCFF{)ip=t7{O&62c3bGW|7mSI?9c%#W=+obPV`|NvvuGbbe_RuqRvuWVvq6k105p^E5O-B!LqA_$NK?b06DT_=&reP~Si0G3$#A7T~#^e|mqj6Ly@Ktj{wnc65Z$6vqYLKmtnC$P%w8~qShxodAkS)<)0<IQg?}}u##%<3Z4E8M!&Gc8kVUQ(K8=9jmK|9!{WY}QUuUyt@@bS}=EP<~DY>xY!f87<N;pBcZq9hvkNVo~08i?TYNl&Nq&9OB6<YuH6<Lv+QZ}0Da7gCAGw4+*t<pDw9|8vQ2A5L7v7CJ5`vUWY>i&M8zI>aVAKPSe!v*9KkbC?>kPU;TXq$@apDVl99#d#m=sLJ$7sn<Ih&3zqt!x{HLrlIx-%!fV*rT>sZ+Nq%vwDIC&o)wOUfc<?ag6i!~LzJ+vrN*EG0sk|pE$S)ZX&idml<>kL&}y&+-g`ccA!0kp1ML4J`0yz>VvH*ptOBAY33Z>&^VDFRK+#54*Cr-{jqDglRg3CkN0YWAEL|`)IE$y!l+$ZnuxVWLU3O}(oPB5gUzma6Z+#i9emG47<Ub4bh=u+Mn{X6moL=w}PjbSRxh;-_vO&AQ%z>En=IKl0DorfvwQAA5yq}#!&mjzqY0}x}5qWB%-@NN`%xTv<KA0Jf{Y_G<nKI-)jF1o%A=>sJ@ZqzX8{+B=;Rb__a~01CcN@DybD}ayOQ|aRt)Gyd=0(l1Xvrm7-KAKYt3xucnZ6&YoCdL`t?>-^bU6pMMHz;c$~fdeGmb3EhkG8=yyulpG%bsaGh4<q2cHDK{?H`va9`2gqW<;Uw|~Be$&~ZS3%O6y1aL~ytLjKOC&S{sF!h|*{O_0-5fOFcu##%rN=wJ2xL%v_gTXEtTqL$q7-f>^vTdF$Fv?BE6LPL8^shv<98AoPtzr-V01hvBnD(cFIiO#lf5gT#D&pYybCcJ|Rl~bkN5R7}L-)mx-lAV%7nVc)*$Ry3^IZj+Ut0dX|KrVeho$%rHT1JN{&RiU#1=sNaLja(Wix^fav#2hUT!-f4&<cAZy8jiB=GHl!@#Fy{cUs0k6mY;B8UG?%cvGHEzAXW!TUQAfT)@;#Omi1qAbCA5hUfA#|QEwn8R~wz?FeayfG4Qgep6m0&5tO81REhOUQxV1M5pFZTE@zcihuaY#RUtmDB7lOQO7{Xp=EHFd?-lRn^|YI#B}@wW)H7fFOyr&&MU!SiAz~pPbpbVQZu~e-B>4y|vVY2IJvkW!hpCRcCv9V((V{eazBBhZUmsns;nkla^?Ci~<NhQOt68hL!50{f&(nnOdmgDbk+lG)>^|>6hy^>TO7Eh;??uYI2xl1HOUp`$P>6&8BQoE+VB~Lg8A-z2+K@zVFh2F<DkIr|?ZK6eK9}{!N}pmm)LQETfqW^9w?M$+T@xwv68BioSr<Z)z}nIJKiRkpclDqOoN?);*Lrv=5AMxkQ@?H`6_K^U%voX}dm<M`Tje%m5!F(g~sMI@(bYz$S%&AA^~r<&pPN6C8{mC}$r_WWIypA?n@Wd8Jxy^1y4~y9013T!uhPcEs39nhcnSMOKHkX$|teONJht-!%$ZfwOB*f*mTz(RxYudC>j6=x~B?TEXcEPuo01SoE-_Cf}ftuY;Vw!(W@n>DiZfdF=x{kC8HrPl+87jk-;db0V<hIQ3%=tNeC@XNVzNqa*I*zvhOHgaEEV#+K3Vh0jzrO?8ZSr-`9CMJK1TVpAO|F%&v&_>_QMBd5nYm-pO?wYKr$<>}{nO5kNkLWgzJ(7dxfveT5%3j!(OC&`x?r0y7C?Z^~y^&WN2l1EXO45RehJd$CUEbq0PYe%n|`c=2q_B=1L^@(sD&p(KB1ev88Xb31vsB+=Yb9s`-mvDVbJYsIJO0n1~LE;F?HVPNn0i&8j<)_cYH<ZRB+AG$5Q>^(hthuK({1bocc$Up6C?1XWvz(F#P4Y39DocPtremhZ2zpsk)y=s<(J;Y6k}HVpx==^3)~e*h=)ei2{25X9HD8f@V8`|syg`^~B2$mM`>1`HAcLfSfnEGso`L$h<7LSm^rOmSTUS{gGQz4tl{EZIg3iD(yjHIFbCw=+gPV58G#z0Ar@5zKxA#{yR41U&dM}{=CPRbUqG+tu&t~KeOZW@@pk-8ZllJMiEyF%!SxMjRq9(v~4e%y(pm$wLlABRQ0_nGZVdB&ek7ct+YPa;f^r7f@>pbfN;nVjMMD}Jk03oUI_}zt-GRIUHOAVerP;xivU{;&TFni1m+ghIKvse8TqMTv-91l=V$AUNg&dVmpSzYo%KIo-I8mc~NtCDshftY*9SFWywQ<Nt&&sRLoMD#l6)nHih&|$1zqI&zo3J6i*S~}%LL7I<Jj^qh~V7h+|v4<p@3a>Y<<cV|<SD&x}V+D;CdY9~nA3TD7A1_U`MwuDCf%L3!UoW5pYxG``ZRk*g2b*;r5~x?O>y%7XHt-d&-|*0U3YUIG0<Ps9qaf9!iffpA<KOfu8uqtDx!8-&Syln-zKeUxD#CXjh2|7eBRCO_duFeU0{+ne81}ITgEtR$*pK9x$$iYUc*UV-nwB6^vyzhld&KJj?hP1t;FLi?RJ26>wY7ciNM&^@Zc>%>cUhjkc>P0j!-y4KZkQ=zTSqCl4O{$G37t>vif4agd_{AEz5^0weqM>`HF;S)_B*YD1lhO4FD=8U%I;~nREC41e<7pAX!f#kVS%XmG22<m9HJw$P*#b!1rB++Qcd0r!nGb{C^8m|0~t8&rfmIlE?sGmdG;t`3!x^Rt$;N0V1w6ZKgTMQOOWdiv<Ndf=&M~o`ffNkU0Qsc;y9yh=IcD?60^P`QUR7lvxRMwZdJ6?<8-zWy<AKNx482jqf|9;28oV%+{<=bIPg~ij{6wmq-N6@dx~QV{j6Q<m4JZ>Ipl-~YfHh@U5^T&LX*RK9)ge{8oHj08d$Q9ep~_;d+k$drFCk1lA*sX1Z+G8x@x-NNA&Po%Opg0^sLaN9P1@uL@>wL#=cF6dZxUzu2{NPXtqj2x5kjJ^z?#gg|0ZcF{)!Sm1yXUXA3w}-pg%M08*RRG0Gk0_}jA&T@#IZ5;(i0BZlRgFM~QFsWOi;mui-?G=woZVu^kZv7CdRo}<wGV!vvRvLt|)#NzM}2aQ-yRetUfYZ&`mgPdb**P`T!gP7>NbstGTKA*n5&GRB}97W<<%S2l<8HD{9*cLe}QFKP3^I-|tEt68|sblPWB5TW2GOoMoRea?(43=#wWz@wpJ~-Seq3;C3h0b1w(ooQaz+I6!k9q2>sZ}0!RCLy;2>pvDv0p|h-4NMuMjWNc6+fC~Wipcr|62-KTSC|`)esDq*8x_t;M&WuB!RXLfjv1=Ec0>qVcb_BU!b_#pDle4g!+CE9fmZcF|6T!g!Z0Nx3N6fLRo(r<IuxRI9J=D6Kqn#usozHfu-f71H1zgee|;S{!Oom9y2ePLV+%<@w&{VaLu%W5t`Z?h6a^7$=wVh5Ci3k-I}sZjvzpXz-(OVEO$QSXhQvx31jP{)vq@%Idn`V2iJN`>pY%DC5?|bP-WLw>Epioz_pi=Hju}SzT4Ad=g?KZc~j#t(|;oVu4}GG-I3J|k<2_9#yUSfJ8TRjA1r<`6HLio8J|i3pfi<UcTozBVViaaYjN#B0hT*Tc*kV&U}RA*Q<Q(@0_BY8UhxsHPxvw9sjsO_BlLlgFCnhZMHWjGSqO>sgil2>M*!)Sz;~5pk=3BRH>>LrCV)8>PAs`N$*WUHjCJ8jQW14c!KhJKcQ7R(T$Wvj3|kkm^$%wX`mMM5tWnAsNU^l;ua5L)^d_u?`uLICIr0*_Hmo^7)J#TUwO5qcXycsboQz-PoNQq-F{lnK9ACl6b7*hcq<)k6G#kWa^tR#w!IZK&wI9!XvHAiE&>ZYGc;el9LrGw~L7!gPW>wqEdrrbwhEg)Q@E35^qMT+_1&0aauvBXy&h7xK@=!dy1D7XGBEiE3OQUg*3$;G3a$EW|jZC!c`aU?-sRzpBS=2@D%eLn;&{^*a`Y9~Go`Nu6-NilPDhaUIpt|UDAwzdX#rv0i>XT^;lY?ZfVY;w~iTXZ?Sx4v!a%0Y3P>CCn|BJX;d+mT3W3C$)XszTl70Dntk@Ioemjr{aR0WP&7eb;&22g_L>X^wYbJ#*+mPlnh$6F2Tng(sh7e8e41j6H5sYzt6Rx|%WQDcww>}>tP1LQIGKey$Dw74a<>aYV<pmMf}f+ReGMa6!DDKTzaT%Cb)ou3tLr1-Q1$BSM9Jw{$=g0`lpTbyQ_*TtkYYy#mFARP8CWSg_C0M~b=i8xnbzKiTpk~Td;(-C1!yd-%Ya_xImYL?pponSMJ0_(7MHwEDMP*-%Ojfpftss&pIc&9cE8P;iM{J^%dk+jHhKOjq*R{BKNmeN^0bD7iRg#;RMCE%S$J2`u<O&vo@xI|Y44Hy`_Mib^}M!s~E`t1q_c#KpAJY?ahW3Jl362uSjE6QM8T?of4-y0Hb=r8zSZz<NCI&PV=KTb07))C;2>H0xJ4&yeDX;cN%o@|C^F%Ld=@Bh>j(hts)Zw;rZlQW2SiAC^QyB4N();XwTDoZyY5_HLi3LXBr;~`(19I5Ao)=0w=sf0kH-zai`za)X3E<MY2+Ma7wv5(pp6s2m@#ze{R1$2yGh@xN!v1D>vU_)p*$pxm{oM)Y$jZ^cvU05PAMCo=uhCC-Y_xnoPALQ3Loc0)E?Y24LGeOluQuJqDdvl%FL_NzzM)-Mo4iE}4%EiF&?nh%&Ylam06YaVtOXToX9V3m(Ijqvb8hGuS)u}gFOQu2-(`w2LeLP_-cF&wnTi87lbjvon<|eNRj*6T1RdedKBm@$*))<K>LCy~xqYR}*pdTC>tB~kDW>84w%Or=mEKh1yz6&ggJ*iegC{W9)qiiS^BHW47P4_%b_o*p+t|^a6Kml4|iJ>PIIGt(vI;b=}fI+uIkBZ<u9I-ehHFj{s98((gGads7`gxT5D-Lza(+gdE%=&VI_+wy2B~WKQe?E5(YgY|tec%5o^JMVGC1UF?5heN64&c~ns+-1#Odeh$Nx%OPDE`voMy_Y;n9Qb<<VCM3W-3o~5-4gJ3VmUaF06Y7N(<ixuvgdvu^DL*tTpjDG+iD6*J)(;qumNtqeGelr9Yeg5V$Y*ks^P<Uas?}5+$z`Afky8-%|Rvb&=V}7(gi4Ql2ACtJQFN%KOabJ|SZ6?@<)kN4C{L+ajHIlGTD_q0m72ChC8<4?BElA7s!>sm8udFwUZ6pdA>zz-%vzEFT`wv*JMeBgax8u~(_(?>RVyYl64U-XWWl5=l@K%yYrsZ8D{3P?;y~-zrkkgZ^1>e+f}-R0u#OmSehzPn6;h1bbbFz{TT_Xr@k2DUm|Ki~E2_+3IEp?{Se60|)u~`zL)(f$7d0dj1z5VR3n5YJf90yhdzcN^ifMb>Jep=wDgG|3%HOHqt0kJpSOVeMOOPm8+*g2ioi;U_R@lP7{?IJ97n$@>Ek9DMhSd+4JK)=(PIq3ugh#fGc_zt%NY~(_U?ZJV6Zcbb31cZcHr|7PdIrCvO{NFN@+1l8tiE@U=B3Fxn~M7(HZf@zDw(Lh&LCge9oXv2{jEQOS^I+@VX)neWm)Wp&fTC(wd?-KX~d+El##Led~OM!W?RsfpZ#1kU6H+~kY!kBfzEcoOr}|Fkb9<EG`(`T2xR5Ta~r*zu7XphJZK!Vq1j4VqWo%xpUPh{`%8Od`|YbdCDnStWWGQtG0FW_pR=EOA&8#j40|Q5h5O@s)MgqcByieYX?+^K<|4?ZKEfLS3hoIesjxc|*N&`C5glSLuCcGo3Qg;8o&iQ+xN`cyW(y-!aM#0$55Lc|Ct;aLY6uoDOk)Cn{i0d&AU|b?-yJJeL-Xi2g;Nal`Y3XOMa{d(D^|+5j6hXn=F7W{f+hNLhgDE_*o`sCBhgJ-lQt){>Jl@eN%wwuV0NybOac>-m%MZrZZZ?o(F2(MtTDr|cEAZGwUhv1Q<ZfNw>%4G^T)eSa1{^O~<B{fLQ28O!h#ag-p=s%7eyVN42hO@4A9V6KFzI;OxuN@U73{hU>x`M3;|if|5cTEt87r8cG>nZz-gQiSJ+5EffC<4Nnd)1sM)o?u*>Mt4A+Nf_M|Oa(;$Tg@OYL#{Q!vB!;AO^$2}<W2Fdjf>TRhrbL<ujT_N17P$0)k%_viTY3NGOVgyz->zBY}2=iZ6P>)n+!1|3B$0#4dA-^bVASbbhlM|BBLF`c%8d-xN3=FgO*CAwD{3Y8izgsI9at2cwss)K5R&OHdnBWV_!f<yNX!Th}s&(#yshgJ><GEZATh4i6s6tTKYM&^i24@iGpGdsi21;bGK6O)>!nNOD4WeF68mT@xTIvPM`0_Q|Z`CD0u<PEn`h6X9Wech~^t)yc+ONYI64JK68i1)RuI+B8y|G@Z`hK*;^oQ<DCyCeV`MqNHqDuj1ibCm}9rP`y9=2(-QzOYD-cgr6gZ5r^<Yee1EdIfw5cE%tGx^rAq24s2n6k%QSS<FObwj)>2xiE~SU`GNy2crt!)2A*6C}`f}`aCD{XK^T0f3FZsVrlbAAm7@W!>iQX+O9msyXwJ>VFaGB=+`h4N_C2qusTj-phFPmdYm+mi^3hOcKD&{jInjwkcqi{jnC^@^lJaZVO-=;-I$9*Wtw~u#4+zc+8*splEiJLxhxd07-PUy{&NO0h342d5YZZAc-07lzdeleIq6PY7=2p%o^u#g;5>=?}0speuq{wM(j)j6ZghMHTtFK8Fdcn`xyC%}Xv*dOCKl0chhy=MbEl_?5M4x<ct(_H%cWflZq0NXB0asj8!hJ9Q`*pE9excsHzC(1&67^P!Zv&u)d5AgF?wXyXX1<Z?n(9r8(5NREbr*w0)_&KCx;`<amb|P`7(mi;Lck5%V1_7|%l&Q;YQ|gy??aPo*K4)qu5DrO$OBR+1MGJ?#WNEbAneJ-}Y|j{8{lvC?&dVfoywc?pxQ2pWgLeG#YhG%it4|N~qJQUn^e#MUDPa`Ao-T$RRO&n6u84rU)7+O;52j!9RfizBX&-~KeoNe6shjiY3_1Gm>F8z{KnDN%&HD}c{_SI?6XgY6GQ6N)MGLw#J)=^99FzJl3Go0SSQ~J*8uMt{J((PYJX{c^t;;)OAo8LJB$}6H>(bieri<%Jbh^bXuPmyj(b)M(m)xffN9ZKZ=xM96KxW9J{bXwz9q+y^sK$4{_j`DyI0>ZXi};Z|I}HvnWMCfR9vIA|8(qcrF4nJtY5F_b$|7Lw7xy2Af2xZDXk1O0Wdujy3$S`N==#IpfJEUA6Tu+)%8v|p`u)b5$!^aiXYB%l^x8VqUe<h^2?;0{0t%V1MzHY~tL8M_rWitsSQNo{Za)d8&bxqgx}xMy;Zvew_2(`&sG(yRXo?g88RxfbR`P=W|M9u>kXJt2+mcjj2DKHLGI0@G5t^yjwR2)N3&*bS`{SYi<J)gP{qfEG@Z-VXw@cmg{nu~5o1gb>X=^iYG#S@#8XJ48`4S~CES{Gc*w&>vM`7O}gj$RZE_ojKN(r0Lt}Wb!=U04FSw`%d*)Paz?|mWKHB^uXx8GdkKmYvt{V$It&=C@<;jakN#<FD?7g^u)hlE4FeQLv)YmHf0ZA_Y}#|ZH+-#(<eqf#Uv>!ga`{rK3ofH>Wj)rgr5hI?(q9%~po{LjCB`Ss`j{qvLm_?LMh?7;4~%>LSG=bEy)Sf3tiQH{XoO}C$j8OWs0M03yF{NLDc|AMieHviauO}@vjY4aU$ry_zTfa_%}{Ab?r;Ss<Q-|_J~ER9`$o1QhDI6`zr9yU!U%orQ?QoD@2Emmk4mPX0DV#lTQq-`UwSfl5=)<nmKz!Kg7bdaRJdDelB{;oZj%aaLim<^x{b$srV(oM#=cR%qh-J{Q;-VSn&XxHRstOr=YCF=j__g{Yd>DR+N-cR>BrSaW*{gd(;*?nB2E=%X>A)*7(Z!r8ZK%$Ln)J7SGcTe`;Idigx&hw>c=sT`ePHOQ1K|e<70fWn~=h|#i`|t)n9hlZl%sYU`sCGR?OuKyjp*ajkW5X9HYQ0dDpd~BttbO*qKi8{a2Bh>+*spc^Uo3VruibVYwM{Rj!S*)>u0U~b=Tb(#Fljw$oC6Mh^xoVpa)J4haEa82R(Wg)zNG21Z*jxqZ^QnC!VYr5q*{owK>PT5tU(Nl8TToZYO(8DzNkPx?m~Yi*1`0JR#_dKlmYbof@c;k6N|erIZZVY?h(Q-a0DtTVlOV+{`H4c&A8+U+vMrwW^!h-2ea|0|M|D~_rHHWA^W1La%iB_oO>uM{Wudp=CJlL%Gzp=3RNKg3QpPfMDZ0QWy0pAcLtN?E4j;j$dBz{$fL$yE_&3{E&9HjJ2hlWABu1U(#;ZKX<<`sb_b@R7pw+Q(o!-Wr+mD_JPlL6$PChnl)S+?CxU3HzpQgGY#Q@`b^+#BGn&I=I3;r2!2*GE8ro!FyR1)ee-cQ>)L+>eO@&%ls;|qgmVZJ+=xw-I*2o1C#!i=Z{+NbYNnk83C=2G6gf!`+V9<{<LC^4}7VG#6+GSx0uK5_<9*cgMpnb-H4W!^Tm<mu7Q!{qw_J;@_N)<r6J`{YSUBw1(Lun>R4ISJbjHI%skBER>D>PHg&f^8BY@aPe(1!la6=Dh7W2m!Qllvgzo?+l^M+}ghQo4H@i=IBT_UN(S-(0$ij|x(N(Fg(Rc_5;^lLdr;5&K_&#k3<lhO)e_>NCAI-7qy&GN6({bY+7o5F=`|DGd8iwo$8wzL+d!iH%UuZBw`hlkLjfglSNX^Ld!$`j_Y9`M!$9L_du%xeq%km7!N5s?+F5AA&`PXD4iQWlGXf4bP9)pIYcQ@46gw+Iw2z?PJUm6)fhxjba{qMqzz%;N7$hF5tswwIPpl*@qhpB;?f|0YTOI+|fA!^q`5yg!k>a+H(iNJi9{_EJIlXuMXk7_VrAIC<8Wuw8k^s)8!o4mKG!ghd=WAs4T4Gr_B3vr5NTUF@~hur<YMhq<knUIPt$Z4AmHl^4D+Q{`vj@{KGED`RJ8Nol7z=PJO7VBX0dJTKLACPIa089rGg0+-}~dq&j@Kz)Vl4vPg+?40g%jt23ONiB3_{LvV~zPVsP+BH9VbVgxA3d>dQEKK{{wusCGh=BI)=pkJVW1Quo`2-orFCa>eChIg}$f{$Z{?rSH#MZdr<ENA3oD=?l9c+D5W9rJjz-66K=Lk<3HHTYZ~HnGK{qnzp@SH^?RTSdGDI5^hJ*2}Qx@mmHts|AFHti!;kWj$_l%a2{}R~ed?QN`|9+#tvtv7HD|sm&K6=w}LH>)^aRllmfRp4Nmf0UjhU5)L|a?n#0zRYuYwSDfX7D7#Y+J?Ec0_Ot7rh8Z#+D{`9MMNd}Jo^S@QV0rD2_p}L`DGceD))v5_X}yZ1);=GX@H$h{?DWje4O=77!##Wj_tvsP8j7~2zTx9>BbMpzy<7G7Q6$)lKq-DLsAJQb#6*J-k9wj|vOU@vyO~7XudQE&MvP1?<f#)$l_HQCqj^kRuG^@$A+;ga*$v^!vU&tCgKi>6-IQ&5UU40wGT5E-Npe)*#ZnBpdBt}WxHO9f(#A~lP!KtlCsKMEAkeMg|LX6D(6Bc}g4uD(di^3q^rVPIe<;o905}ZKsaL{i@R3Y!E2<B6$dkg&bdTNKfXqJ9%38qP*D(HhM3ggw+Gn@`b|A84wEB}VTk{YW5JB0HgovceG(NF&gD7K2LmRoWINj$o1B1}L0v*f3hTGGzJP%Q$PFQi#?~5N=ld}8iN#BM$PS4uw<+WydZeUF|!UDk_rN#qKHq5W8<&Dvdc$Mur;80{l9hz#Py($gUjb*rEa)pe$E9`;DrY?^0?lf62OTb$-?aKX3POI%3>;^4FTRl-~z&afFcw3TO2xPI^(I!w7B*<rtg)|pwk8A@=viKg%oTv&}>U~AtooW<owCsW3&5>EN<WZa_Rm}v1JiK?>=ND4m#<_O1(7uNHnRz$!B3qxR*8lwTH%CB9)>#7KlZ0oJi?xR@;mXvF81LpW)h$O^%+MK{94dj>T-~A)>F9hWLs6OBQbVy?hb-VQm$`?3;S-hV_>oZdNdtLj-u#ne^_WZTk~^@?G=OpvP&}k6UUP%2P_zzEKUHAYh1{~WRt>3sq^iU^>B2`7X*TFpDt~z!jDcNVuKCtzKShfx()ZY<R-gmCzD!XLtiguhjjz|JmS-TT?wYb(68cf)`LDWMj;yE=1DrgEvu=(3`J9x;&*J8SNt-f*P&9@DjB$SzsYPFZTo2~>Ad;S2AcuWqvPogXX#7IAYZ=oF2G)J&Fd{+f`1acGSt9cSh|G^^bpS}+Ug29%31u{A$3H`0ux63ezQ%d!19CwhmkpI?iG=Kvy~hnk#rirR8|3S?F+W%sOAX#$Q1$gyASqBcW&)TS2E{yCZ?AwN1lqzLE*=k^o(-pRotI4x>$+50eB4C~c2j+{RtD(8STjdmBC(6%)KbXI#Y*+O&Uva7)}wEMzn@?f76+)x>Bp!`&aY=VM2#$gK-Gm<v_aDZNO`@{k?0w_edyM%tWg?8?*Tj&<gdq9!lijOcpGF-n3m|TLjuJGc07|=#Vr(94U~GmB3riA1j-P40`xuSi8B68ul!(tEA)WU4&i;z_LNP5Zz77LDFQ-xa2r>~UJwPV;mYp@;B+u}^SFiWBaTtr$4o~~9F(Q|$Rm{+FB;x;Y9mG~8Tcy@t`e;XNrH@pdtD7_T6F#~IU1QRWobA10gsr}l91E%dU;NNXOCEFNKyjfzEBS3qR2{q=bY<pe-^fRhvQR*Q6&S@kai5dNB=@bhU_6yzXk&LS<Om%2_21vcErccJIJk*D#vCJ?!_uYk>N?a+)e`q-4Nz{nKDF@jWSIl{K3;>WTwM0#AT5C;K{AFVNEJ8dA;r~F)0{4C#lTmyq@+D%Mb|^!0u<3Yq8Z<lZ#U%WaFf#k#Sp0p0Bv`9;1XNaDxc-Z`^cqTR8AnJp!vTPHN7T5j{Aj&(H0&xiT;?A=8-f-E4i5I;v4sPC#R?=OI{RT18&RV&!$#7Zal|${1w;dy1#_BtzFz2vxZEe-*LAZ{`sjlu3wb=vkr391xtj*T-(cH1=&m1c>&Me_}mZVFW4-GZcegen^bR90CPT6rrbQe#jJZnKMct;5&IQw+()!ew1UBJIn;PXCJyI0;(GOw)PZDh_lO}jsU65Asupta^~`_5L;u_<b3|Yqq2DndU}rS?~DDaIZ7A+0tG9+jL0&?s+;n2J{vJq3hhj@m4-)4VmM(k%0w%hQ-tu`;xX7o-Z%;mwU&wYkTG2KF|a+6^W)hH*X8qSYcjr`C1OemvwuO#EG%YHJkir2_R{c8g@7lKCX0Eytb<J+c2w}wSo!?JDv{m2E6Ns%*ItTT9ij<Hrpc+0J*6O%CB$=51;%iB9ef%KP#H4qkPJMAzIK;MwBA3KPUw{7ZU_-zCA^fqr_N}uGQRSR)Y>M{g+#DJ#?_=HBe?}pg)6G4_%F4n;%zec{?)08ZXD0UN6{B7xw*W5p%4w6+7wJ}l2P7b%^RgF-GZKt&r$7M-~lalmJ#7ON<BYG&zP;0Y{W6}UPi+}uQvK_Pd^SLJS~+wuK$T3s6jM`y{e9?Z3sH#8Hw<nn<07@EOjvx+!FW-`zQ-oQ3(wXJ5=02qCp;8n_~wGV3$$WF(w}dBb)kqHyApN)%mq3C+Fuai!2EIn3MFNf3hhgm=WdzEji!LOIS)AJK+YXppqtY+=y&Dwd4>V#!gX&Uxe73#}{bxh$_n(<&FS-eCu-H=LdOutofeRQUFO>SxfwwGIXgZn~OpLFFV^H9fSAXOT&waTHBKzJH^#;iqCg_qm3fk3qO9<3%_Nwi_mMg@JcabqM*GPllsk+W3W8adV-v`&B<bW_LpT!k)Q9NEkU&7W==~dD)Y2v+pG$zc<*7D?4$f9ZXw^=iY>}4MfE(GwhN0+7N+P9aOqQ9xDElpIfFiOkrg7_L{YXqpA^gbO3>?IDL>)mzKuQ-w^rIiDGv`AF3edx(Q8~9WGjWL37R4JI&hYHH&WS`1SOqR>4=c4Ne(tJ<fw_4Q};(z{v_ifxDmulxS#8gN$l?DP%xq>r04^OHRvxn+hKn&$nkkDAmbu(A<SH2T}@UU8&ik*S+N~jtWPvS^B*<WqBek7fQ?IZI~Nl<y;!cVh5%UJHOn!8Le?jXi~Ql7uEM+)`Mo8*hoplwDh_(4z7Dxo1S$n)lOxdVCu+!!KURmm8wrVBNnLS|Hd)YQkOyan)z;deP;EYoG4<I@ViI8x_cpKuQKipAZK)L1GnY9{p0~$(FGyuB+{yd4l}>?fk%O9Mk~EIwW1ve%;fPb=(hgqXI)?4Db<AZ=S)%Kq0T0D!He(1(?!BSH20bLZu{nvSjTX)8xMdP*IQz)4upkksGq<a`$~ujzR0Re}%K&%gv*TkI!5UU>*QTknRi1;~BV?1ExoPxqjwP8&m8&VVuj?U2dyGj3EImt2UmLaC41NZ5Dury^{#D`8m+PBNYou?42*4rXUlgCfUy_RZXDRy_^7b4$_yQG}zbJcNW69uDE!@wTQ%zVgxBFmv40l100DqkGtn;RD&Kwu`9;xxFz>4v_zw?~n-t8+Mevn`1V6kI}wcEsm4;keQ4}TlPIbir}BJu9lpcTDZKVilC=+A?&sih1GM2PlSlOAxWFpiP#vK+h(rCEoReULhpXKKhHn>wUndmv3g1`F*w!wsZ8x_8{E>WhaX4_gTZMw3yy@6segWJ!`59F_={;HFfw{=Q}ZL$iHzfQ>Z-&j$@>jfSZi888NJ0zGzB{C!NwBWYN9sry*WKix+elE}kYEPReaO5eCGIh@06&e??X)Wjq%Pik1b3#3~;Nqp@BxxKx$tU64D7W2dXJHtEAuDUKr*>k-;Od<sEKuX*gVzTB^t*doV88HCmVTWD`0W3JuK}y2*=npuiH0t*tF8cQqU-s9#>Xc{txWpdyH4$blD#0!56!KXsSd&{g$@_L!xkH_IXAtvuNi2|Gje=nT^K}}%SZ|ytgUh&Nxy{fiJA$*jb{DlIGT!?S0Th8&eDi%D|7~rc`h-R+T5e2@o4~_+1(TF}#{{Pv7q;#hR4#nv!0urO%+`R?j#Mz4rhOsc5R9I(Xaj?F310|((#Pz^c(3kbM$V4Cg6B^qs?3y~D2%eGOL(8C%x=Vl0fJ4{<85#$qYk)e`o}!yK6y><(o$qy1O$u9OVQ5h<aVrLD~sj@A`H6d+kFC|zwsarWJ;^{X@ie;l%UbruV<%5JL04Uv6^9MNiGd<94(%bQ;*!U!~`%02Xsv^N!fd5lei)aV?QT*ZTRmQtzo)anMT2qM4oeMk4c1ZOG?2lQ(ZCnuomDbR`)Dx04xBkL*PX6mpB8tp~B?NQlwHf%Q=@(Hscw}YMkN4I9PGl{A<&QFi=JriZ5a1bA|4YY{)Uv6m<7AMdyF<%@q%ebR}-5<t!hq5o43GN^-i1t81cvmCpY~U8}D3Ijty#t00TM2FGN{=ZzjN`d5GyRvG;f<{EIK@Du0ZbgQ{Z9}lWv*+xM3UcPDXew4OQQ;x#J0hyawC%q+d0^mXXBaHM4$z#<u#HW0`2fceAKEfd&e{f~P<V)c1@c9OAgFHdJrD5YR@H2(fUf48iEyp&>4nD<$C0j4y%hbXJz-Xt0i;g04?EN`ROyMG*7RViLXAmF3I%us6hLxSvb#>E&cF<;jUHJC@+G3aeLJHE45pO)W+iD^~CV}!f+cfzi{Np6BFK%FeOf%1OPkZq)zI?7=Mw@$j61>|Q9o5_b9l8$?@9N@P&|b<(-fh!ypH#gkVdI!2p(wO+AO7B1o_!aJLZaAUa^))m_=p+n^IR&TOH{eTdt_xn>?kp!ChOb2s6RjVAKxBqY$MZj8lU6GLO=?XmX>c@D1wyP_c@yBlnKkP>OGs<#{9<1?CI^h559xfm6BIpkL8(sVEGS+Wg)pi79)jtNbBB*VS7Fy%{cIh?R-Fi!6QihoV{kO4Q=_4I{3gb4O7|AP4SI#GS*#oelXJVYOS<(0Oxz{uRc+h*w>7$q3=E~4&qzcG(M@aT_%-cfCqFZx3q~8^<9GMA~9OvfPimBMhp;~*L{B$xAvN^)Y8Xo*vs$~!<eANsbw0MVN7aKO@7QD@PxutV+w!sNffF~(@#ZBT)l7^Cbj1zNL5Ly=nAiea2?+Gd7D+acUU%}Xhe!j<e5Z0Z@4scCPXBjX_3c7$VA#%O$;tWt~Jatzl}aij+G6hL)CO4Yt(?ahsMKShNV}t0n|0(a?n@gPP`ZQf@)cYRW%g2Z}gmP`g*ZF1;=rd!M-Gq7<L>39Acj|=6Rm(_IOWZu0#C1bJ?JzIxQ-s6-@ItX&m}Q&}8L4;Dza3D}5*{mX<X0ANwLQ+W5)3zSLe-Hs%CCf?PMIZ}@D~RHJ2|Gt15-zb*AcfRxN6HEhdQ)R-4cyXZTY%!iw#$K!?LfdvSiu3)UL7DbbrJ>$n^tO?PppmY{-!h@{V!=sqABZ1elo%37L9px;JrQ(YZKWA@3D^kOSn9_$i(f>yiAIuPed4l;phw7fAiEerZAVvd9a-5vpF~WM!=fL+TiyL8QH{)WEG4~dr3CPcuY3Qh5Af=70rL<^qs#WEsOyLeq<CEz_$gSga$l2)%K@Kz>V2&u~f6Q?b(}fQMQz>)No28`!*^le4CQ9y1^M8H9@ET+`io7itP-yvl9-PPoN8fNq@zU^!`6<qbn@-|fDqPkzlDJ)7o=hCwB%_0LU#3My#(gLmx{r57Ukxs#n036{$yLYnU2$I!h7jaNU4Vs_$r1Lnx_f%echh%DF2Vy07<#t>i8MU+RauT>Iw5lrLocQ{gTOq%yQs<|yH{zBh>mzr?W1R6oShG8T;{P;_{p~6poAS%BaJdae9?*9J$ETF^sq;DB6HfC$HJ?d5F<%J&a>WUh28QLCpE{RHr79tyT4CJkc~p7hU5!@|7#;?@IykvYIjrc4GUiuH^rEgyBf=6F;5=FTQA`ZwB|)WiRke$uWg5a?>A?5O!dB#t4w<ag-?Q4RpimmcMBh*-}-bSK<Ys^Y(exH@5vPH$sQ$<v;qR7DG!2R!EUNo?KY<}=viJWi3f4EG;0w|Rm@jR9xv6>P$M#F<5b%Q+df)4aZ8eAk}2rviV8GzLH`PviF=;NO({8H10L~G)lv99xs>2w>5D9N`61aW!oTh$vjii{mbxZ7!u4cM^zWdOsC7=?#~sG^%$O=I(d_qu0aIFf-M;;UiTaq@`dp`P{;Rmq=FiD=enO4gCGOVOeU40fvo9DGN5sQ0SXcS_&HHuw{_SI?6QyonGSux~#oWF$?fg=DELL|~5-L(MU<ia=1FmZ|donpaGjKtahEDH{f!qQGDbh*}TbI^&H*K9)F8VE@GeI+A-~l~9=~5A~;WeGaY3{ZvKcS%*%agsTbiDhvphExs-iOMGOazN0qdzkGD)$XBughkx(fqpX{Ern_Lx2_Yco{MKCl%a@;zR<D5e04GJ#?RdXg0;`Gj<FEO%b0}T&@H&wK>O2FT{_}Wl5e17{qFhK&4O*ZAGSx1Ibo|=InK0IVC{}-|&5Zyd!^n`|YPczL_6>e4Y30QVD+l_1o{}=YOoB;z=Ai_v<%}J94b~rc#>RzpyvQBBJ##`fnMkp_^m%=bzuc|K+g+DsT<}zSk`pn`lVv;9#u@jH_42Odq4$GR&c@VcNfkCd3`<5OXO#bd@g7rPh;+6v6fR8H`8v^Zk0<r|<vrXHfU^{h9me_g{Yd>H8n~>$h+Jd=IsN&V6X;z3qyG)ybqWdpt+Cp^Ei9VJ?%Z6nlIy<FO*&v2i`vqhm;6Z1O+<`sLT3|MxH74g<!<bGLH0-}&?VfBdU)VjEzKy#PhEwx1@|{%K77$AQLf`eSS;$HAD65q$2NCV6L<>2a}TQ`K;X+wmzXyRLrf<IIGE)q);@n&Ma^mN1Y!WYQ;R_UPfWg189atHy@;8vappFCI5frv?!{DQ6iu^~BhaCEL~I9nM1Yw=_!L;5;tTMd!5)?9rRw5y<|=Wr?phI$jdh0V54Se^)-O%lbNsLO%~7+n}XaL$TX^Yzbt2wTgByYs3>6pZQAwfA?(u^6leuMb;^e*4Im_l(fpes%w#zQFC5Y!qTB<n!P6)B=MMEmD53dK+vs`+U3xtSVP1Ec;8rVMq&~%MFMh0^)#AINB;STu722gkIsLgUMX9)?OC#6D>Y<;>ogY&=uRJF(o3=1++RfplQ%YWl%oC@1!h`~4F74$`6lOjZF(sLHZ(F+Lr~Mqj52cgNkdWNByg0bqX;!_GL0@T!lS%BQP?^@eA8hjob2Aysg*53Lmnq>1p5}Z<o<!!$5&N}eVzcj5g}z4y~2Tm^Ahro`}!<FVuPwT8Qsf=#x0R$k)fw1H&L~i*YTf!dw>7CoSSN@P_{r}F^j0ackaaP!-;FsLORqohjG`v^MqVi*i2<7)|zc8q3~l4(=g~fnAV2^2hbzt&x~nQ$!VDG_+!i1O)%xYUK|R}os(%uNY^ADGG4V-;*qJLAF=VsV{#9UhCog<CWPBS#?XlZRT(@a#8Dp%-YWx4P304zSIw|^Yp*UVFpUwy5&c!d)DO~4u@b`(*-Z_h14x-8au+B6;$AK`vSS=Y9f!iB$rztx_}4M88oWXD3{a3@8j@DdF)jbTWRQ~{ni>`XYnp{(q3b)bqiwk4^y*RThG=D_$#$??=K(n-3Kdnp8!P>=PotVBvoChoaUf}Ls($V?P3fTmCkUfe?oVE095O4J$TtCrji`?15=&&tLiUUwW8Zta@~lyh{W}tJO--YtI120KflO`-NdzB0t1xR$JnU>F)!**96}-YT%?So(T9OJ8)67dg#?nC&OcNQbN+z)4obJuM_BCIDF!F9cn0b-iig`<mdV$05>>Tlx(tc1q2fRO*qRBYa_I#D$--Vs>{GBqY<**M$Vj=#wXi6QJpY!mQNu3J^H1Mw=QeFdVadT)Mzw?Zi`QI@w!UO9DoJF8cQ`HN4x?c#E4h(k5K=U%JZi%J?!qs$)a#Mk8TmplF>RBLppMV`(9R*M0mWsUrZ5OUW@fQ68JDnY3=qLR5d`7E4`v~GaU<(lNj#<ShZnC-UbA8yv7LV9#s^QsZ)S#%1m(kz@H^ch6ZY{;NgH_O6Ch)3{7`LMMk9JC`r9bDf3@VNdNl)0p^X;+z`y*|c57W!&PE5<FR@^K+!cUdL6BQs^nlHps-4vqVz_}No_{>rCWZ$gaT>_rgz}PuJ>=}3HWj)A7>7Lc*k^N^>?@zeDA&xvul7)EGX;~8GG14?<pXD!WQh4it-`=mt79{v-RX>KyE7zQoj`jkJr$%z!I@tFh8PfK)#8`%DrYYq3_4kO6w0rMX{rwkNgC2ohysp)9%6Dv9lm2Msq65e^2B`C$VI}xze`8bTPi-4gQ?qVyScjDvyMdu`6EE`grsqX&A#R(UUcU`l^$u(kx0?riM<GtLXdunYbfyFaIe8+b2mOcqWd5)IehAR|Dbg<e`n1@#Cz}jwM4}MqkkAhrD;mG?XEjxk68%sb5osHcIR?giof{#ekF=Bt@TR?=H21?H3Qygdd8mC>3%I$FA)}?5jLn*dMTSG$;F7%ob~ltm5HjWx0Uj0x`;-x25FtWbK8ipnM?p*o)^8rCjP*k%V12DMoEtO^2##%VLa98!0|>?RNE6L5vXp`;SFfX!5bPp#-jCs~vM?2(qG4b_O%BRliH4?tU{OI*kI{fc5DU3<d`V=^jfMm`HL+Qavar;`sr&C6<|%<l1?WWkRNtdhm!p|3>>C|y0@*-9Vg{<G89jSq8!(MUXu%dmSs+Z*awAu&5nKR3$b5PewTQky4_4BSK<&sK&|VMu3?y&XJgL0yAWY-UPQbz?p7eQ^*+27NfeZyLf?e$CyvX+S%cHJ&j=+~p>>j@9grSQI{c1AAc}|b%oa&b2vSU~aO*xMsd9F@M8B~-#B+{}38mtJSJW$85=ANF(Pk5yB)<ZQAJK#hkGbP12=2E+Oi*4&S;Nx;#2Gxo-I0=QS7@)Z#(=H^J?bF)Ou12K8jF>z00}$mho0Gb{4T!=nFQ-awWG|w{6}bWIQrD_GemoZ_gRS*;AV7cT=A7pmCPG+X#VL7wxQ*f#R9yi;CTor{OrB$1x5g-a9yA=Aki0e~00@C2jrFi&Y@rj@dVhI~$h<_5N!#ZE_yj1dNRU>1bSl;?OK3T#(t(%+GE9#t8>r1RJ1z_Y1T+gnUenVvSo&aGDo-HTMLKam2PQaQ4VuEf4xljUYc)||sJX4+x~)&L==F*kL0~5rWT$MR6Ay9Mh%NB?>Vk&z5H?1$px96+!+4i*@jlBbBF5DS8m^1sR5S=4HlK<(pYnCi^EX?k8TC@z9c5mwDj|D}y5zi8xa7Y28mBgA6^LVap{GaUj_}^o0$fVl>-3r$EK2}7*E<l2#^i@5I|5cS%3<hqf2Y##^}b1HF{hzvZit7Xqlgq@5}YxCIUqZJh;2}#y$!PWOd$%_xq-S1vjoWu<yI4r!6&LzI(G~5*O;f;(62f)*m+gmV|{Yx6S@iL{80>p;Da<ipuJcM+QQykglsVW9T+>HB?<hX8*};T_wQq-6((+^Ot*taZ2Mk}x=%z+W5KH($VNR)1np@)QW?5qIuT8Ural$)96{B*XoC~NhK-HeLw_PlW?;vdXlt@9*7U;3bk>f19XMWnHwqkp=-Iqq@-1acVFrnvI!Xg<Xtp0w$t9SE`B}$`?ZNFKxhGafeN2^I#PrDTv;_Nc5ugmCD#fCKLmA?f{)LQq&7A`6n8VZ|434R|%_&*p(x=b!9iFQNcfYuHpbWE;9`z^k?rX^gEq97eqBdVLyCS0nIVy%zJIXFY&aW;*4HG!Xx~YluGZJIwkZ|k$Fw6HVBXdd+^JTLesXV(I&b{;edl}YFiNGht4WCg-j59Q)1%@`RJ55S_jrw01x)A6#R}F3^Owkur7ch?gX7gkhcba2VOaal4HKnXt2iFPwRZzD(hB&GCbw>T-81#2Hv(~zRU|>SsBN4k<C;=soi3;dK9dtbpK`0apJ$*$XmYR59w-hXPR0`?AIoOj7V>KZ`!NdPcOW=S#fuovMCLxnS&kD^<gOrSWee5PoW8Wr3T^C+$Lxg@P9ATw_g);27<}-7^B0N!q#G83nQ;CMoNWy?e==mQu=OuN#9ivR~yJ%A1iFBcQ|HHt&Ogl_+wU-!riW+Mt)PQfVqXcxl4C+X0m3hq5<BB}AA)e3bd|~dbGEbdsqyHZNZ!UQrAeP-E>a{L}c8>G^$6zBOcdE4vtgJ@R&pI$}11qC0O7Ov9Qwhx);9aK4VtDbZl%y86NYTa|KIod{Iw?yja?OsW7n#zV!pxOI#Fh}QOBKArm!pAn5^gRMpL@P_0?muz+_a@uM|r|beiA;tS>fYjl52O_P;0$qarOPBaqU<n#p?oIO4)mA+~$U3OJKbQ2ayzMWt^cy9YV)taY`quY)@LER;>sna;0^W(fc9<0cGgS6XN-S7|Ni;fyZ?8=A<0`p`Wd0gk}NGyD<pI6mkfw#~`%9^@XWZ#ObJY3aTn%R|`;kDK-P~#^}3hN>&6Up4RS|6!#bZ6aIE6F01K1hA?48Q%wVW8>rM}IvMF6pbQ<OxS9N<y96cY0^jD+fc~w$wJwuP`A_LOBTCuQ;OFIjB!)?4fEW!%kaKRA$hj4AYKixm#GzL-&m5;UuinS9$ZDnD1JL!75o{Q9?UtO+>ZK?p-mdT@$vCoWuDB7?b!y@v=8|0p;q(#yOz8P+7E*G|XN~Y!KtkfeCzyghGp-L-Jux5I=#L(ADH&=MkPKp4k-*DlDS=}|YsQuFGVx-H(~@HJAVV&d`;9iAY5vRjRsPEsX1W0V*yC%v@X|2j=izW+m2XE;2B7V1Wt&x<9q$1MU3p4t<kqU~UD&E(IUW3c5ZBWStMMmmss$Jmwk>_)B&^43c7cgub`7n8!$XQ4q;1b<|FUice4trwGxf+_ula3O`_v~{gbQ~d1_0B5i25gb=}Rkh%TQ~A^bYp)xTb<zdf1l){~{}HV5veX?jx}yf+0u!=v-(b6n4!Kp@N%29@gq6hgua|6WN1q3b#M4hXYlGXl_|Z>K=+0fo>tsuVM^iE{L1-$Rs?j<NdC~DDyMMnaJog`m{-^(|9<CY>VnJKdaP5%i#&&B>z!bbvdR|XiBN3C@PCN>(gr;;u=DN6)E$#i0RkQk7Xg0pDFHOUW@FGkR}pB0}!>#c`sfaat$X`Sdiayoun`H#A^ez&7deTtSlT8D<+C*r66p*)_`j$&CDo9ZE`hfapN`?mTIcpzBU+G`OIZbljroZ;t;7_hC6xRwi3c(b<8RCe;G8DvI-spUHiJq(P>k*0J$TZXUp!r8#dVL$P{k0USG#8lj6eRI|rx&A4L~z5Ymaac}%0K_3~tYBZ~=eypth8uhY~?y`e*3I6;`(L8MeRcxP&zs$B4(Eo2W#(_@seh_1gjIYd}(P`erE4rqc3dHDUS!h<>2>6ya1F=Z`s<NKg|?*eFPh<prrdk*<}L6OW~l+doRvUjTZ?kBOSbhF5Qaa-WkRt{1L>^d`ggE^c$@SnAAQ_V*~q*8UB6Lj2t^}P@B>l~+c46$~bnD8N^v|cH4B-gu|H?^uk(FD=rX=)x07xFREC{vCeAHM^RRVO=@oN7pJoZ5Yz28(A-#W(Zx&O$-xp!ufJmNi*Da8%qhXa|AAnNTVru{?Ax!}}F-{Kn0XQKFd~u;odGt#^Umt1qkP_Waed>cwMP0S#CD^e{bV$hCrH&ow+S-4Z~QDKP=~c{?X{kHC+$4k`fv5cBO&Re=OdEaxU=XRcEk^+O*QK>MjepUQS0K+0oAQ=Spv;vd!5c)@i}(g4h{7J~FE#UYz>E<+&2%iZ2uR2pK|6XW;vv;HT69_kommHT&Hp})w$Um`s6t38~2=QP&tbT<epNK*-@s?r*Q?>zXAZG&<q6iSh+Ah##IMO`ZdK;yYZOnAC+{TeKE(BvGw3(-vR$wW`9qA5@pnMs3D!v|C0**cXH-*H)&&<H$8kC?<Wk^T<AxQQ#Xt0;o|kqSLlvbMZEsdzdt&uiR9kp>l#KJCY{Cb%xF6Kex+k^RbfM9Cg)GHFygVQT|#l`%5{6xAgJs8G6HnRJ6`4ta3o+Ni$U#{=3tJ=e^^90_fJGfG=W8SR##w8aG%jO^jvU;g=BQ!tqGex3it2UA>L4Z(A<_Gdn8jW`&ThCw-q<5G0!U*j&q`%IR6ICHi}d{KUXl?x{UaD8^-Sqn*by&KV=zEny_ImmfKJ&cbhaGcy^!Me)?n;xc}2t@`xji2tABFcg?!kbPj30g|7^JxFC&EeQDQaJCr37xi)!|W2qf;WwPA$il=-kEfH7os=r6r}wZg&v)9h<XroT>zQ65aMlrnBSit_m6K6ho@mwKaKwJV`2UmY9`1O<(%M~Dk#0#zVl$BQ|2YV(jspvRQipleAv5p3D@>8dnT|UUsD5*hwt=H7!e`&`Hx{1{U$>puAXp;lFCIL`0#+xP-~ZIZ*isSdY!Z?w(~u7e8|Ap%z^hQCBrfZw$?v>QpoPT5wb_iI0Hy@>b|8fi^u^QpeD)n0UO_bOXyRs`~GZw;ssyDSenteiiaUvhNoIj8{ozps9p8C@yjqK3lx)|?g|JqpdYUhsVTDxMVpslQjr*3h=)CQt`Z{bPtazM&e}PpRh<$p5S=j=Exu4)Pz4BiAMGaBV7zGHO+e&X5VTBG#!~s`OL-orap+^Sl_{8k_0%B*J-O$=OI{kb?;s4I)QZ%L@rCf*SKkbE&J2|)99d9p(CnDta>lPan^w^YF>{fWbvYl89dB#{ue?u$biRyl@sivdu5NQ*(m*=qh){;*ho7_iPbPOdpF^~d3B(TdNf~82n2a=uYcoswh;F*G7AN5)Ds8{pQlQvert!%L0Rp=nRDj)*E+sFM`NrV3b8qHzs*@NaJd96m3pcl4^Z$b%k2Poab8hp0Ymjhtf*LmVHgW#N<av-%!pUAQQx(IOsOw2W^Oso9@&%x!$pvm4b6#{wET0dKItzlBc}c_w_shM?Be#r!Hgg<AGA`eMKHjZEd`yN)DnyN$hKX~~Ax54xB&E>lh@Gi<T~rRnWsY$3yuZ}1J&-uf>$zGQeF2?1&jJQeya?I2MIC85zL;kn8i6bHsit(!!!6KMAEOpX<p50u3q*lGM3g=$UB%sZJ_ft!ON<PJv1lF6jnpo2FV=I%cwS{Pa7btr7(B5tJa(uo^!>Eh^VY|P0{nSVhbN_5VA+e=ZtPJ6rlnt4$9>@WM;5?Z&PES|QI|WM@d5ghy|^?PbBu42xyWgjA<=_JgTN4*6_iVtQWGFEJ-(1tEOXu1OIh_8=rvz;G-}wwycg6WPo{zJk}Qx2NTBPVFq@-S#GB6Di2;DRjgL;1qmhwzdxv2#S%&7D_dE0b+s90~IMb48QU9tA^<^z`{LvyBtse{#AdDZ#u1Ts&d=a8wwmo5{m|suRiGaCRRnMJlS~osLd(k;AA!_9zmPWWj`^DuKo!JwX>K{|x_a&U{1#7pTRpOApk#SH-dnr^O?<vC>7Md;o=!MCbH7uzy|Acj!-@kQlYeKA%lG+czTX`xcaEjMQ;1~v)BEGXYuMB2tL*EN7<;UmJ6HxhVZ%b0`>yTcNDdS^NX-Ag)kwd*0mhG6X?>G7LyMKK9?WaG!nIFFN`fQJv?6>z{zx{50{)R9Xp5X)U?Hig;%epqzQD9lsR}9tSHR1>6Q3+2(YN6Zp`!}w1d1|GZD%kUqrn-LH|DF91P~s0gfabMueeBlxXcx!s-~De2uW>tLxF2Z2UbPv|FMN(DtkHiB2sph(w{o&M%8>s<%O3&`tUD}JejoU)?rVPazRgy662IIj!3*%;VwO@nu>}qwSt<Jki)NfJL<iUS{GVU~>KB@%&7YsQfB&el1aIN%u%I;XAIp|$!ne6mTHN)jUSmVDLKLBM&p8zVI+F~4`Sy`PJmTo>aM;H>snpy*J~mR5w^cpjfd|9A_AQMy^mG5`U%&kN^Z)+&$$$LI#13{~_iJZ=?KFGM@fVBXV=Zbs<>%G6pNN~O+l=Uw;?-kAr2@u!KF7!QYaFX~O`Gq4I~6sdGUZZ2XZ!FdNc<A_mDypJ%;nF~!>5aqy4T*V6)>c4b8i}^54*0seTQKQqC&e#{rcx{DLvJWD1oA3x~>h{V?)9LuLL?-QtKJ(219?>-jn6Yx)4M-#vBdf@+4KQvG(0>{<5naRqY_xsMlO(Mmh!l+Fa>RzyI>vPrn}a@_xG4DGhhl>+G_G`!SY?CDwV12ytEX8!RjXb-}Tz<}fzxoPU+D#Ar^|(0R@k&6195m5T#>K+v&ape?@add=dI9qQs9e0nsk-<bCZk5TP<){T<P`9rfKx_xw`GAR;>(%h<TzVxhp_PsyXt5Kh%WZl@&#V;2?y5_m6&!e`@a=jKNP?@YEii|s#GIEYdqekN#a44qt=5CQs%$J0VRz#FhV^fKirq8~`4U@kO`x7j!$OSXrPp3%VxR0-g=)}mZaetN&^|j!OF{E|?msEjKOg*i)$B>pFtwAX<4K4Qr3^8;eKEe*#$<1{v#*O^v-`?N<{t(6UY)*qZu=z*}qy=<1_a(o5IB`BC+D4Qj+4W!|!GRhkx$VT-qsd&nE0e+05CPDK)~55o0rWU2pGcnF#~Oi68Ev9<G4BME_jQyhJwWICG$g1z6E7{5Czpbysp-kLk;r2P4~~Xlul&-m>PJmO6bjq!pa4yX|Cv;C^km~ShW<2ZSZEd&fxv<-@Y4CyIOYp#qADnBVm&@Q!dWw{9#{pC&WrnJ&-2uPNkBP3RY+ncf{pALM^y`JBKSAiRtz53si}HDl>mFO!s^tNgh5h=P?!fEn0;p%O^h}CtuLchrlx6t0!%46Nm+wI6s&*2OFYS`K<2h!h}QivYPReZ!=7b5p-Y5GQ&xHvRCF)zXD4hoW1<C7I@9Mbcxs{Fyz6qzY1a|d%nZl=CW$?#dF&a5^)5kryXBt-A0B3nG>W}&gEf7lH0w~~4$X<07cJ5yq{p39=QMY40<t?q>xQfz&^RRX`mAWXRl#7!Gu+eV9N3m7qy~rI%RIF%EoAw3e5ZMTE-RJsb?v8@Q7z7WC@i?~zePL}7n}OmZ{Pm;9;Q>yN3TrkTsTt}{|c(wYiJ}V$Kt&)^_<uI@0b^`1z{vsYDTn~v)1<XI*Kj%$6%KX_6*ypfOafK<2R2M80Ds7)j0F9&w3xk2!0RrRQ6}a7BtO7Zst9?dxM59sQix8xDUVJ8<FZ>!||YSm?{o&KL0)>e+0v(%Y=S`{t?LismU_l{@moX3DwXv)lqQq%+SHT;Pcn)6>qv=D=?n^OBJ{aX=U~PkGH2wlu{F7Ut8oj*C#ymND^hLp*3WjkX+=Qx%GBJ93x4OU!&<oK!}JM+xkm<S~lP?xBS?3&a6zMjAc}-xE4VI+iLxt2=GbG7h?H$3IUAZya)h#=J0xg5cUOI0us-_NH{p58Fyl4vw{u30z+A#*hJO9Ks+3&Oy>8!|8oz2cK!7*W%%aSm`+2yEQyLE>ASWrPb^g*`Myy~$V09mPQt0dY1(=M6-Fc3$Ik~Syz&ih{mHqWTiB?C*|6oaGtAy?%V}n~q?)>skKR(Kijuo|%us(rIl&ZQ+K$R-?Zxldv?h1c%1Q+YdQ^{yc81{@qWz7{8kt(io+a|UM7-gQn=Ns<Zlm6Y)P`7xI4rr#gw#k$*UNROo3e$PrWu+(ifQAra3AjpRg<Z~LbBBBI|^=^MWa3FFHrj=6Dd7#SxGWb+z+9>W7@VSI~T|Gi&%^%MVjkF>171mweXyJRi1s9#T}v&YKI~Z+)Ve_%|lV8j6-iF^lPY~v955?&Y<=gE`a`sY#A+(#o8ZlbQ+7SFlb|D_AuD}iO=vngcQm|j)X<`Al2yQv*$tg6QaWj0y6~!BbdZ_h=AT<nM%Jwen2h|Jl=-eAf`Gj`0`rAJvXo^fZ?(Mp?{3<BM!5&VnD({;Kv+R+2#YKXa*Y%^&oL>We(XDz<Xi~5vW=b;DnP2kNI4|ou(M(lsLFfABlWX&UNXV@F{_5M(G3Vl-y%-iBufX7n9K@z$hdUz*<#kPSYOQ2Hj<0Qn340R*{NM2g9o!1FRhx1|(6FU$f*<oF|o?pAvU+4>-pOehjR3G-bVpgO~X`^CDXxS$d=UL7XEzDpQw*C{)6L$z=^gZ(wCFWT-?qH$Wg5v<0k(5@oA|R65`M+tA9Ob}vApO3OaNY9@*`KZZ5;bo73LTOH35%B}#;SG_fy$~7Nzsa-7Yw%;G{U4llDROM`L04fTFJ3y;Nc3sFnTWi&@n@1FKjI2L=G!YfOUfc4Qx4|md<>f+3jk-y+xFR8hUFuq%LCw13Ww{*mqsr4-by*FWc0a~odCpwjn!EiuDX*K}&BbEs1YLcZt>MKW)%{gH$q7`k-d5+lz_+n4R9gAFMbBnw4R`SieVk=f^N#jex4pJL!dJ=6?ILM+K>~8u1GIF2UR{=mTLg!M;BNo&L6D8EXqnt*JTHCdD^)2v)|j51J#HfqYkV4DiPW+C?xHa@nQM0}HF)Si8P*pSqu^r7DSeD)eUf~!S5_B-gJItp4?a#ef_KZ#%O=NA3A`|?oqGs1)gfx7LN4qHbJW=q`y5VjgUmc%%s9ikb<PVoSg#&6(OXUl=7vA4fDrMu%vq6J%~E)jtHW24k`%q}s~jTKNTd{AZ(5uac@{3<s<{E^1pNtmdnu701#L233TTb8E_&zXsg85KfD-u4dquWEcJ67_|2ia4i(uC&nS|Uzk;OnK=PQzHTTMV26;d6s;xxtI^r{v1w@4`CCFJ(3M9qB{_mowH?>q{`Da=A}A{zJ1UKs@t;tF#HD0wh=^I(T<JdT;%$4qCGt_vvl^G6yxq@TQ*NkoXj_3cHc41#33#N?&A*}irpu7E4kw~1iIm`u-&l(~3#=eePhiY_<I3$d-EtjLDI`w`V!f~j3G&QvOK-lI-Al2&5EGhWV){mxw#;>Xr3Y~L17o#8gEGK{K7n1*3wz)1QRGO}t`8_VqaHPTzo+0IHr5gnz4(lo>^Rml65>hNX|u2m^Rk>Ot)yg(yD{Z+`hdS!^@VX@^<Q_ogzGNrtDrumMs%4`k9EPzJYOltaSFMw@yN<XE=#3>Fn%5uKWqb@Ox8tTz!*)?0tHfh+nkX;3e5h}X-pacWwJw_>P;3QfrgmMA?l(6dwFu%tTCpF8?=tu(1RDcO;ycIAoA-A0HY;F0My75ubQvk%T=OI|491L_x8P~349sPI(EOwOh?Ws-MlMMZEA&}#-(N&fTKcYv)qD(@>N6!jP)`8H~y*_pmrm=4mB22oM?iI`R3U5_u_{$i&m7ZP@#n2TeH%4_#rV<UE5my0c%6qwOYCviUI!3v}+<$xap=+XXIRa<bo?;2mcNx?XVU>B5$w{*$pdob0k<s&Wi{%{j^c*MU7yDInlsy4F7gl2$ahiyAR^{g&@rAL!HFPE+OT+diaosS9Y$6iQnOt}-_89CUZyZJ6TFXS+_!w;c7}%c3i1KuY>+*TkRJnbDWpYXhbE852Ff3nFa+{}n1WLn-76M*HGB@V!vL-@#*ik`O<Bs$Xt3=5drAtH9!0EM@B3ILB29v4kDU@U>L~04)vQ#oHTwVvF$O2R^OOXVqI;`sCNU`j}-4AdrX+HUXw?A9@9tgGbAi@e6FJs8S{Rr(nWn^P{u!XWdDaLQJd-|yihaeBdA$@BSt*{uQN+HDnClEotE1fWAZYJ~X-~F2C*78CW6h6X=s!Oj4*Nn=6zWD_kG}$){%_((~I|W1_1j@;}HC>y8K!6H?lDE`Z?kdQ!Tl%F5#<JE^eHzZG<ls_|>66Fvsieyhb*I+EC-z8R)N4!aB~lF(L!<BZ^shNQ%ML)fR34lBC*s_?=K8-KrO^;c%#%(+j{q(*7Xp<(CYaJ|GJcl;0B6Fd?xGYLD>m%}*5cZM0xWfuSdLlH!N{V{p(xMEHJcejyW&S)AN6C%Q(wat!^ARdjuw08qK_qtK7<5z!pkBV8i2G);H%2A$O5_Eo7MFQ6Tlh^IhI^3<<$cu7P0Uosff0wFw=-mJJ^j7uF9@MhCzwg`iC<G{np!j)+jX#G(=kWS4Ubi>JV0{eEi7Gcm(HlSWE2eFu1-bEQ^A1uN=}qu>=3ht9yx+5zDcmRzLhT-DoeK=5LK(<!^0a4mBt&EF7A_xOQl}+oXPzxoI1Obo6%j0r8TuIb|cyBD2y2ia8xPIPhBBQbkF?#zE^}*=AK|%X=Zi@QgAzxyTu7E4C<=8x_!Do;<AbTGX^Vz^c4`4^P|W)#e#DYH>A2@zBc6J|uHn`t*fN0>E|WaE4cp{ZlP?W!v)!_N-$FT`X2UAWuXI0K)s!r#BX+56J{zLh%Wrh|&sVGi0own}zQ_S87o)zS}wE+5zUpEHW;fS;=TBIycUpKPIvyI8~)Oanv}FBoU1fD(6fhatyB86N+Q!n1q38h%^Bpr2Lp$$dd{5vbAEA$R(^^kf6x1hx8ku9^twFj91TXI3W#YsledJeCjaD1g3GaKRSXSCidGq$!Xi-+6<iQ{H)d>MS&&wRP-Y0G4evwvo%GWQb6hQrQur*TP-*N2M3o6x#le3{znkDx}Hir-$i!HNRu2P$%xP>s&O070q1(^sBkJb4?3e|7)RA%??&X~2us%|rrm-xYic_+TD%X<<JC|;o>BDL0!Y$y$L)D6w_532T3c3S^%Q2#mlr8$Aeeyh9o?|`oLtDtmS}09Q3J!}P}2Qlpi4)&pA+R%@(|&MhD;cB%vBs%O8B939)<iin+lBcz4_0^&>bn-39Ey-^_MzsnPfE1)9}U(;HK$HFG6$lZ64F8N?SeIqRwI=d=Mp2p3U<5#&4QBnS6MURs_toYhfB!ouf;pQsrtT?NfdzcpPKW@wTG4O@c+CPD?jJRMx0v{p=r9vq*xtojJH;LTe<nh*U-(V{jBG!C#V)U6)4aI&IJOzcf$t*OaSj(;G!u^#v%9U!tPO53!hXTVTVUImxA`+ni^e3y$*ux~*Lz3`S|8K88Fe$ou>1_aEffIllN9V(qp$;p<0bNK#yDt}i*SiAt9X19^Abd-y|=3coIZn>uf5HIc%cqFvYYjT~~UW28|52tBNRA3TFibPC?pkd{7mY;`(7o*x(6iB4a%Y2%7+BKO4lBJIdgPaw)_*c}yg6gOJpCMyk2zMHg{(^MrPIH<KgNn{dY1?oP^P;v!EE1~TT3Gic<iB!Pi)o=ngxhzkrLcR-}lRc?(Lc>tYssoHD3?$r}GnDbnf%}%0J=ccG#IgWMv&3r@)nJ-{_cri4sN_X}kGMm*i$Gl*Sv@6#c{mKmlt%rG$C!$KR_gu=Ql0XoOcy7*z9v+vMP;97O`Sf$5bH+{CwbrQDwB!uJ~U$5E)g>M)eeZ<X_@QVT`!Rs=I=iQYWF?0Df-Mb9V&!LFnUfg&3mE^gb0iHLR0#TPY<;28Pqd;3cy}r7sOT$2moDZlRW3pwCDsxv5}dNb}Lwo4iyvR?={Uma9{2tMbE#zT<1?EN|SMCYw2p^t&2>^#?V~B2I}FGblX5fQ(fjh(Pi$sQ8?a*+=D`vUuW55<v3XjHIVzk><M)VU&sexH&Yz5j|z;CXe8Xx8WY&tB@AT9@#PKK#Z%cM{1M$1jkdpu-}W`ZM`y2wO^b=-uJXOO@6IMuqNYnlX$+_bsstA$#0ye^1DP0)X*tH{W|5NtcYMP-1pXL*@iO2C@D<ZE!u$+%9c9Csq4vjxV+_*dJK~@HH3eKe@8<bme5l3cjY$~J#Pk~RpD8Q~az=nl0i%Cq)Cw1s!rF+yNU`z*naEdE7+1M;8#KnvPIBb4NbB@=xq&X%`Y2EJx{*4_x`nEj6l4mx2F*I@4TKW_5aAzToNR~=qpo3b`Qtt4bo=njlL2vst79l%0)K~3!@Ldh1o4)JZMMLH5%O_ii>ZC>w^4Q>DY_%ss0b~5TiFAnof5v^LkbxmtpHyZFS5^pa}2jLpo=Q7G`|l6lTK#Ey6LeUXiC2>eEWZGg5Q22=|LPL4!~<$O{731WG*K|CtrkrT+ZukdC>*htCVpkb0vWw3*<YJ+ZuNJqz2-UV1PhLSIC1_5Lkmv$6Qh6tb~bT5~r@!+B-`}??U2TR4Gkfh>G#YEn6H-rYOp0R1wB|3}xB+C}LJ=N!qN@pP&1WZx6Px(Ly`T#_?leAsh<8%l9V~7IXKV&1lMmn^(1{O>M+{<E1{fO~)uZ_<ku%==GeP(KD05a60A{LD%9_7ur<JG2uQm%yY@cNE{&~EL6!vKMx`GJocKgE3}<C>Z<_<Rn0>`Og%G2+CyD;*+0R+t*cq;;h1xwq?}-jZ|IsaHuNRul^c9pn@)p>Tv95qUG6X{%<p-MW>F6)s0tBd1`Y`LR%F}&A%5NWXTdYC`6|-fm^f9*GCakYWrS{DAtihaY)q<~O@5dj(2~OJAd@la=&9DSM}eT`GE6F>JIF2(zs1)pnR?(y;Q@^L7a+vNmgsn%Jnk%MW+H4>J!eoNUQ|NqpCF<j;_5J$SFL}!47pYe$3QoVKRMblkilgAeGyZi@A5Ch(yRFa3J=(vzarg{5^V)9?=q~aRlrSI=Va4&iBy)s(c5JFAxZOv-FyJ_rK^^J!*n;jdm^tKB6^*Bb@*+Gls{_p?g(6>t27RMDtfZ?BXG-foIJk7y%<e1_pvWJqa9SNql5%3YPw@-7&fS26S;0o9rM{3sz&QRXV%?j(Jhk!@B)-)_e(EU(f28t#x{A7$GgRY3J^9aVh%?TJOnP^SQBz+LDeeaWe0gJWh!P1QB%k=F6jnK7MfE1&4-_}$GP=axE5D%A`@LiG;_gh2bfiIHXIdMqDgLg_#UIWB<)p7xTfV-=X3P?lXVD;@1o`ryk;RvZFhF(kb_&Mp`*%xG&i!Q&Z2i?KZ=~DX?!x>2bm?Dwi-J_Aqa_EC%wGxdFG}`Oz%AmOl9vx?~InZV?PdC@zn(1GR^<>3BF4+^wKCUw`e+{PwaVg9}|>y7~$^2uVNxHVs(;;M+#T(jk2oC%QJjqkolVy8Bg}1B*{MB70o%gY+~Z?Za7vQ33v6(ASfV6PrA4Ut)Wdq`0;GawCOt~m&5^b3O&t$z*T_x@#%!r91Qc9BE<mnK#91FiY1!S95H$DSl7q0#OO4V9-GHbxgpyvf%0fjVm8Xo@I@yM(cDFV-$RemiIdUzbspnck{X<6y&VR7-YJ4tj^6ypl=6@93ra-DvXGP=@NsPj41Y*c_1w>q*Qa1gjAXQ{(}yoUJVI@5;f#&uML$&N9Wf7QhkwpxH*{;T%HqdREFyRkMfzBVYINf4dF$g=2dM$wAO)eKnknG<kA`pyBzd%iJR|1~qE@*dP1vY1=vh>%-2=g@G^r5Gvd0kI=605s8_q5!!JKMRU|UB^5e&h+lu0IDrpqc2Nd+AnZX!~)TV?JPS`OsR2_;m}qRW@Q$l{0}lFcF<!%p^z+gP^LHPLvhCtjj|_jwP+?w6&6aXB-j42P>!Mu7!Gf@a{Xta^6qHDAS5DnI99dKdv16GHxPlWlk%K2pUdb$&MJimMl6m=%lryLIm<x*+(nNc_f^FnbsV+iP+C=KcDA|MoG{iIO5O8B*l0;zVAWo^>e;7Yn#7385Gvs<W%_NvL1W9}Gzzp_OPslx|D!jDgEW;fS>G!`7vZ*PEWpE6ekiAbF>WH}K$}pY&N<fl)l2#Az9}D!=xjHo}vQq;$Odw%7ypaPMQyK3E*PLl7-8%zknIVfd%|c(Yb>%MAN?WAx4r_&3FDf`y8rXr}N(iUS`RU5NY1o!iN7&s0K!rMa!ZI@Df85S&O0s80g=rm!%#IffLUrelg>v4j!IM+JVa<{+imo3ijaY+YtZ@IZuvni}zWib5zOi-#GX_$Tq*X>O4GV~3j7)ZVocT$Bc}cnkwgks>GK479BzT-uO+d@kLT%4d6965hJ2t;m##FWHLFN}R5}roiZ+%e?Q8cIA(6zy0*bH}k`fwq@TQ?dosuzkd7O{5*QDpyPg!p<KUdp0Q)imnbP``v}+@)_PCpDC{$j5YvKz@LyoQQo<&*YYTVb`4!((LM6Lq_6y=rd0&Wj?c)FXx8GdkKmYtVeE-v9354jhwxp*6!m(@_Dp*Ff@F4-%|9^AevK&it9Q#99bUnLjITB$c&4xTOacEdw)0gPq?{HAn=*sYL_sGVPv>FUf1ITA&JUrY#|7yeB9j%#!6BO;#b2R$zKR#SE1%m?}GZ|e`)j$61n~-#fwQyo*#c;3O55pou|9|`EUw{46fBpWKfBR>6BI3Xv*DU_nY3LdpkO{aMmf5ueUspZ;Ma;iw;rqiqOVg)ALrM<DdK&#>`#t%$xTei_z@1WLbRccd^g+(F?b9nDBK(tR>=@4uOWT)UM-QLRQe(O&PrK+7&<+jra$Hy5v2So0Sfk_(`@=f-<inMp?6H+zF%3h**bA=&I$0K{2P4Nozc=2K^~K5oOu^8FI{xm9qIo&gulnY<?6<kvLp#X3;+!m!p^qWe^2^`<`nO+xJ?!P<bl=BvpNbD*pp<BFAMdK)J9&$U8jAV}27U)v+u=Uj(w{Z|s$hxHoT8!ASZm~T-4{EP$Oi-+8;g+-F1w%Lj2ZRAJ^1oyTEDUG5gwzGOr<8@Kt8mDWo>9UL`@MYiVKcBDw(yfzW3*PHEf}j!VWvSN!MOPr`J_8&!e{abv($1$RI>067F0|<s6g7y2d%+NapO#-IPzvmxOC>E0+18AsMu$&%VVCQ@#!R3({XH;MgF~kPEaA-w)!Tck1}Fuc~f+Z&7}boOzUOMYv;C4xD31t4M25aj76o`J`v?4QwJ~n(J7D8~KmFyubg4)KPxil)I=qL{u`WlAlZd`NxU#Q5LN_QzW||Ocd0_WV>UWSbH>?i+5Ff9B()Op^fQ0Z~!v_n-`L2kFgFe$&;1Td#KSo*0KGx`TQQEE9m|dURsU`ae}3>DF??$<T--}M?(NzMYU<*M~ycX3dfE<filDYOe%?fvT+=wKTWz^nuSFo6JiUpbpF_sYY`Yf)LST<fY(QS{BZ@?M!%IvZGdzhs|{U}g=0hc0?GmWoLsgoH4$uN$2b=8kkO^4_~J6)^>KRF?@NG<-|K>n4QB{Q>JTwd;ej#syh!XA4S(y)c$KL!a#KVP1bH?NBV4`zk_cDUUgFVC1v0k<!$u+|@7o-RQDqHLCPbyI{3@ueiF%Ay_U<wHUzN_xS!P~Z=(p^;9CO-xT6&`y*8V1mJ;!P28AbFiL3+Cd8iPMRxxF5oaa?XNkok5os&KclJ2Vw)UbILjTRWI{evGAq2Atg?S~q0%fW{%2?tLAgAgqNT<kon~JzdX%ZDnCPaQL&#Q|r<~NzlZ1n)cVSQWak}{`Glqi*q0EHm=mioMHg<!>0cE$B%!!%XG^5=*^=$7fwIPzk+QhA2mA7(4Yn1nB|<;^gl5#LYJIIVsi;$&UHX~y5R^|3=DRyV9zR~iG_|G0<b(rxw%+1E*e8SQdo=tMR`BRwqPIsKxeKAhjRFom;?F&`b!{Py;aRVe%+YCp%-~Km%;FH!q9Vxn>Y0X?85et*&WE*^8sHB5?NYWeEj35?UrTU4>$OWS^jf<*u+-Q+;_}Wnghl(jA#s)#0F$eY`yHX(3T#*_2#1RkQ_{O82GfJ#~p6@vFrU>FylJ7Wy}bn061&569S;qd|}o<M~UDA=fyybGmkIRMvNwW75vG<NF+d+sV526w3#zd0dmDzE=V!Glt~(Y-?2ZX?y1a>y`?3U)9kKmp}<C3z2XaRD0x^!OnC-`REio9Voa8U@|6Xu|9V{Hb#6e}FV5`Tutxbl`s9!B6|xt%e0PC$sws+ekv*?Edqwu{?!S*FSJ*QOjn|0UYu>SGO=6<eP8aZSlx$Z!!;1B4f3*=KQ<JP)Cb@+oX=7}4h0FCh>g`tAkm&5nda}*)56obi$Z<Di8(-I{hQN4s=W?<F*LR6j4{2WU9R)7UqJgwAQ>HVdDD8>NJy=k5EBL?W`(gAhj7q;)r>yTkiMnNUw0l3CMm<0%2+wI&!q|6P2T9cjJ47VmW~Rq(y7lr8#f}14fA;~CngM-kgxEgH`b;1;@vxb>kV5H}Pq(Gd$^smQGQ6}@RaIVVry=W~pz28?T+%N@FI;v`B*_NR9b<WioGT}of$8RZIqI~6Akx977zTYB##asc`n`61Y9K-YuN0#}%3%cFbeMoO;}Z^eKIU+@p8!CA#UPTN0$n_f4RZiN?t;W0<3dr-Lpj@VjCZH`g~>6RcBYoQrkw9DH<Dukzl+|^=%YMB^pt<Tz!=<)wg9{!c>&gzLDQG<$Tmo(2noVuU#=jbIvos~bqsLnNH|bdCwt9`M{ycmjRz1V@y@fHuEBYJrlq3+>Dw4dGZ%iER@?e0c);rq;-s*bAY+=A8b`sn#YMNJH*jY!B%_Kurn=SGCK;f^Q??|iob%299NK(yk@}E(D>7}c@`z*2k6}$c-K$?f&cySCvOsabg*Ir?<^Gt<(nW+GBT+!%1)3sCMY5>@V>rC$Am~+g-AG4AYt?W)D;jgg@-H7v#NX~0w({j|U<q+~Ir(~{f1?)HBtM8t?Vt^KNtyy95M`@D9eW{`nU?t#6l=PsEd7K&>OB98FC1bsy=zRAT*>n}TDHa@ea$j!cTe-lnA<?YFdEANPUQYwJ;DW)uixe-y@cx%(85FFJ5)_I2NKC|^vu@5%|}LOBzD8*7+fb~x0|fI*EPVK&;d(Lc^p3DPAF10B`zF-m^F*!HUdv;A3ThAg;NqsI{iFl6>oNfe6f0Jb3rTSDjQ>2#PbYl$+>DCh5rVV2}W~&ksh&EUJk-{VP_Z*nNH`2_p?sxW=DQq9Q-+&qlM79Zd@z!aN#$YRPTxQLXx5fnYmg2p6*kfeVx_7BAoauh0H<)PyXwSN?Rr?<@&QUBjwJZf>F9MbDHA@qa*P5RryN1C7Ik(v@3U&Y4JM?PXY4l@wL!ynGN1<wzEtN|JNab`U5+j#l+(#l_zrz=J6*X1*UB&U>6<I7_-VW>ThNhiuh9`e94k<dtKA}Sg_TvWUxEQoDsM#U+<FRq8TZshH^^TOZeWSGy=tp*g}Yoe89OU4%~$au`+x=m`!-ey$+mdA1XaeIs`3u-Ye0AtopPorV39_PxxXG;G<SV75SR;LS4-L-jR0$UQXXGf;D8i37-?1fm*~dnXPoYVakYYCbe>bYx^0aJX>m~8LwxiDs%d-4dN`GRg!W-$Uv$~DSqah{pV(_Y$w-jBj?-TO1OCFOa}R+zo8<X6mMWS0oU+vJ!d;PX-0IcR?4oR8^Ij)QmK@+QVTQRW*aNUaTqjA^q+{D2Rq-C3>&s0Zif1d6PVc{`RX(GcZ}60Ss(@>dTXVG_0>`UJDDW1=N2#L#0e<%`F(-Htl7^{Yd!OFV_iPvW*wbKo%;>~N^9^8=5*eJ%4-7$@x#|0%Qy+ZZv|-PV~C@hdS@&mi7m`ie68mK24*Cj3vO<#WK$Pj)o%@`|NT4!GU$U2tD|^Ktz#amfW=mc;GQyjJju{YH=;V81is2g;Yaj{Tj$Y;_UKumIXw`^rq?HK!Z`G8f&#E-Ibaic;LuIY4eb~M>eAB-A{x5l<i@y;$vCT_GrlR{Ol2>3Obb}ePRA&BSP*E>K6Fhy3P#}U##3xz6EA~0Vyk%?Y);WCcc(;QMH#1@QSvBoAA=rWqmul|e$}LMD<CZx<6*?aVisSW&pksW4NdgU-0Iwrv|02yOu&=~0dxKto=-gnyV@H^fyB`=(FR3^z&{4I7qX!|(UH1*S&7x|#9&Oz^DGmkBD*MS+7x;Aa=XJk7nR~o4mRfPvi3-O*sAX9Q9kB})nZaqsZ$9hIKB3Hwu^)`o5{rR944_6xOSGvU#fH_mp4H&vH&&9QWUYa2^l&$QY?GWseeoRe;)Q{@2M__n~QIF^yx5^TUNiuj2&xEsNR}HB`j>X3P2h)1R}6^rzs}PEo6@KyR#G;w=x$Wg<r5dnbvFJn$d!6R?<i&`-TxP^D^2^113HK<uucJXbj>J&ca}#otMdOFsP9_=Ba(gt!CD3n)x47>1Ejza+2!1Jq=$832#i69#i8U@c%|MwcKkB(}@hF1hMke1_S+v8~=sI28%z336{is!s~8ekF5p_*c6pUBn^^1+NC&90OM8ZOHGjtMmF}f3wewm5He$gOErgaU2O%==j3JvCAG~Z#p&eE)mrl!v&^T(1SK~>;C3SW<uQldsZvY4Av;AC793)4va<WtVZ5s(6c9OR9Tof_A&-&qJ+Pw8^Pk)RxaXM5tRGy4UpAF5QP`0sej6;U@By+6znKG$#0YMlH(%3@wjz0N{_wNj{7q(yL<)7~MQBElLc4uN_nXXB*kJLxx48+ZE6iJxAkQo^OTwb)Ai?v3I4Vub&IOPw=zN;D$rS?1UPzfoq_jIJMj+aXO(m^VsSsuaWj!lX90vnj`&2@%LjV|BL1ti5lT_Pu=54R%+p69Z^g~!SQQGSBWbb32Mv%;Xkm15?$O{ecb1Q1gU~z`l4ZaRsUBLzTZ7EK3UplaTm>(lWH#!L#N38;<EY69n1@cI%Y@{&7MFK*9CaR^LYi~%2+ZtsmFby7_6uRuYq|^hdx8MK)>t>Rsx>rWzY<JnT57MidkIWduQY<=YJ}GR~kri7E7SR|>7wf4kaLk+7h;zOrY0Qo8-Ex~=RSct`kOB(>|7h@HmIjFpFqj2$g&0_Wv*zd`k=KrNdxkYNl7dzI?H`fK-I&*EJ71(vhBVBpB6OCsTyC}g8LDT<@4HXFC!>euws#|Laa`fchSJU;zo!rMhTO9n%W;SXNiNw7uY}vg8r*G2-8pn6NX>{)W7fR*jOflGmJD6^+t6~?x)-Q&HL^H{bvBV|w%)esoSfv9Dxj@tOv6Cgl<E8!=-N?9<%Hjq{=hIUl6znoY9#`e!+mP#Md^na+JOh;(U%nC`Hr0GNU<l&uvK!!IMvQg9B>eQF%3E4a~|X1st3K;H_M_heC*T{gkpSZ>c+8?d4xBMD1=~Ki_k&G52`o0#V#+>7Rsjz#W6}B3TP^dT&5+Sr$)BC0$u}Mfl{d;zhFGt*6gQ`3wKw_bx17%^0KO+4gQb?nz{67F5~tZG{1S8e@=aA(PHo={77C?qH5n}_2YAa1KZzd*NQ&pJo(&JoVP6PI#D|7E<9;CFZ47ODAM~1?koi0(9L6rOSjFD?;#a?kUtFqBryDYp){4^HXJ4LJYz{C$77hATkNCY9ks_rRhBFH&@oa~dP2`=-jK^s4V{`|i=_H49a7nwOLNd-p>v<Q=_gV5j(cK#akX;PJxA@B&SaN0VC}MzVh;ImaPre~ft~4?r9cFX1EdX;bltj<yoj-XOA4~o-JI7KCGFk~w!EHnxEBnZd5`(-V{IrRLhjZXBxF}FeWm8T)_cXoegIvoMP^b8F1KTCmz&F20+>lVl!plFBhlG%a)Xzrcp3atuaOh|{IvabqGhZzv0U8K<=ct3kAclDF*R%L%4tSeSE8KtWB(VMQh;~U5bJjdM#+zMz{gJGz1+L2Di-<l<3pfiPfJzo#c4VP2yd8rSuxXd0gmse4KUI5#+_^02?UR#vVm$w_@tp%!%@vx8lHT3mL5Ywk6=7e=cfu)JKdBvcXi+`tIb8kkV|5xd<We+dI-g_PJQB}+<~EBw2x|2!qv^@+u{??S%S4D$qa2;2X{k07f-THp(qnAEQ}~<Ox8<gNQ{+q{K>KAJ(hE(q4l~pw@2DIRSPBSy+GX*uTo6hm^_HdJtDid+3bPk(nT2`nE?*L1(H}gN^x#;NHGOB9b>MzCd%sV_nUBL_zPJn##0q}Nn5*~10HOHTcO0prA-WA<U5j|{d)=2cizqOzxYs_%d7jX&(!H%Q3W~toOT?|1whfiGV11w?$^@DKv)sx6P@+XsCeD&QljXrnv#^lSJ5zO4q{yRrqfz)mLi$@`zCedC;$`Ca)ovBJJ3b|XrYn;4hO|CQCaK+b5a$aOuC@$zE5?)>`RdE@M)O0n>|6irLs>GI50*QOZF(n*M1vp*OH<Qik)uI!nd_2Fxs);`#mLI@zD|pD80z11xkn8833vpA<c@zfTfd!Y}x#n4|FwO7ry<!HZ2~%u&C3I5sNN^Z7HNoETkys4JKd6UvAgKwmLsK?c=GqleI*;mo<8x<HAGY?JhfHN&`&T6+i&xYiB|0=x^@kLx!jxO~IluMM2_?!r||oWt(>+$8Bl_7FT`=sR)p-5YSskMu<u<WKXIsd9C7ZmmQ-`!~Fht|MSO_MQxObPUCZYOqQjgc(i@nq|Q(6#)+AZm0<QN*s{4TkZ-)&#<uSmWe4#lr5n7SzcV&xeDq1Ly1x@Vt8+!L?6YrRAk#)qhEtK0OSPpjJ!{l`*_Vo0q5Z<DSp=L%H_6>OMb3V=?6#MK0ZLc1<UvN0@3lY5d7k)=-YZ6hKJdI=gl}bopEvU%Pt1F%=mM#M?_1eKnF1W5=0uDZI3VC#%7_65>Sf<w1+IM0SA^sqIBx6hC7vcjAJa=9uD78m7BuFeyx?Di8APTE@Rs`#&NTB3)0isO9g8x$xMY!mvee6+hH&FLyz%o^1GFawp^<c`u`PkTTdl4uJjnI7_Hwy{EIGCsFURH`I*O0!-Q81(8(GddQY0C&^l`g_U%WO=_zXWrGElPdDTdA^Hly>zJTCfP$aG3%W^!ksrZ!DNOIF&E*+z0hhFhQLk*(AP9(5n{>{^4;jE6p#o_3cow7uwyVnZE$Ee&#qm~dI{ZCB_6!oa7>8Z)uu*l#KtG#ngv_hp&={V1kELkRqQU$~nI9O>NiJfoqT@D7HhAVedIAc|fYBr<H@`7J>7kMXbNMlu$fP{FgO&&A`a_u{TjU7>G-#;eQ@fVo(6P#nc#YMURbX&jIxY*&obF2rr?u)mmP#uy-K+}d|XQS*b1IYf2Vad<KJ0h`AYIDb4)FX+K%xvg_!#?j1hJPpUC2n>eR&R(#OGj|3>pyTv^Aghtb=4rloZS);mKvMoI2d%5n{e{%CTN~<(JRPGbTPzNNnQH_py~Op~6CZ;}h>WWZ#Ua8A)bJU4hjSqx@-P*5A4GHon!rk^$l9beUayhH2S=^r=I@AI?*rfx^fCedM*|5(a~q@VuV=8RQfE7u2TK1`q6##lNwwqi@GLLXYXA=+OI)X+Q_~|N%27fGD%Pp&f!{dSdX!Tar*;p^K_?8r6c>9A(@45%n*62#?0c3NB{|0Jqf)Cp#%~CIAmc)kO2BQ6As+mYC3Ci)BVS&EVK8dIu6_tw9)KsP4V}*@VOsq&g<g{IM0WVzoVVY%26tNw67tWBN73YbwBC?wpgC=Q<jf!%_6?E<{?rBWLjHy~2V^t6j4@->6mh6;@{FCDZw0+$CQ1ascr+U*rdhc#F??Ij`3<%%WeLvB_K&iZrjE=!+H|ROSq<76fopexE99EYH3nWDf>J3sEW&MLX^-K~wg}mWWwi)dXp&Llh*`GOOQAo}PqL_gPpPQQ9)We1Avm+73{U9P?tle*itl~s;e5{K?&r6@=PO-`$+Iq@0SsyluDX-dcQMo%OC-7-X3tBsdb{0XF7Nuy#|`?|w~v{Qln!*Q(1HFeHqf<!>Vg}?sq11(|7W7|SRJtH;3ZS)@+zzP7K22!Ia=NbCiWlLo`}YXUpzhxf0do?zf||`Vfuj_wV8aB=p|?SdHs%sQt<-QP9O=-j|!3XqqY&0hPPL;yJBfRSKxkIdMV6t#z1t!3ziRAnA?&@5qz3HrzjyW%p+y&oL{6q=UqTDP8}i|qboUm?qY*+Ifj9zh}RukD=^cT(Yt`1|M<IHG(H-xB^=s?nn7<x#)^~2R)nU+eaRIKvPtavzCR!O-+uh<m*0Mb4?iFLeY<eIy#M;+@8R>vmcpn1XxzSjGuYT;%~ur~NAxH&u;-(DdEww2gs^nl;F9NouavO~?b^a!czwk;m;52FS^R>$_SqMvUHdBEQ(G4<^6$TX82<IEhgpcYc<|_#UCLqJDtvaV&oehVA>1AsZq8`UWL>Xlr=AOX|Ni5n!UIUl?87p;;%I;T**8Iu9BWd<&Whn)J4}Z~1`q%C&%gfqr~mr>FaP$>@I=IcJ+4{&vD45sg?F>UJuI_p1-`C&{EL_?%Id@l_bg3f3=PXD80%^DkL~xwRN|U8-vM_@5$Ay18DrZ%lP6EF01o+%Kfl9z(&eY=S@Rp^O>g9B(+sx4^O`gyl5rV%8=%o4X^oP10S@cjlWkINv4@ws77~YsWDwo}bdaouVAfiTes4UN>x+3gm=2%|b^P5I^<{D>P4$UyiTQH2=5~;GMTb@7bsa<4|I6S1`nO+xJ<Q|dbl=A^_}MQUQnr@3k9Q^Qk~}?x-dz0zE8YPt+tBdQF_o;EJ5{j6Xim}4Wxf=ReTVyEXSMi%pdVwA1;J(alWot$!xwMh%YkX##JU4`jB59D#FTD5A6i0NH8k{Qrp^S#<HhFe%-UDq`*Xb-A~Q;tgZ<j110<q9>jG2fQQIaP8wrV;Slu24zMV^{d|}eJ(KrVjL72U{n{t8ql5oLFMSwdr%thAp*|)f1%C}*ELCXWVU{*22S)hIR{t_v@Q^%hjE2);auJcbS=MB5jWr)T4ay3XOvd+>X)%-$c7A_OheTJMqm`H>e;TJdp3y~CDQ%3abhoCKD0%+a{+wAF>W^yL72UGB<|M8di_y72MLiW`aN3fBa1^2L|DFP;b%;Db0iy6y3E`?78z%@vk8c(?%YM(egft8iqZTi;delp}yV=osy>J%1dca{7xfw5tm`EaQGkwTA;rr{l_)g2gbz0ewfF}9NNIOUTa=J7VxtIQysNVx`*b7E*M=F2*XVbhog;Om)R&G_4n;mpc$2MYwwskF(!c154y@g$IpX}+?HnhLe9R2H;|JUs>^@q==)qLCBIt4Y^${g}$EBrukwosYmG^YrVdsLLN`f}Y{cE!OcDw9CRaUI`f8uEiKa&_3b726BrAPz5N8xf#22`z3^jw%&8#u|WVHSFr)yP>u#tL<hGAL#g8FV+=u;3eBilWwHR3?Q_Hk#?ZgHLM&l>40UpAavwxSPzK&{!~n`^rMt&r_S1*a9z7EVgiE*Jqk@z<JmB(j9tf3piii*};`|G+m~n*1P}c9O`i$S3ZWtRL7Es9`3YMY@6oW@bq8J~_Hfr_I7vp$?aec}Gh(La}Jgq5C@d8xid>%%-{+0Q7xvvsI(Jv!R9>bn&N%@OyrF9w~>0=9g9;20QqD-?^)$sCo{iTI|%dX2Yr@g0pJU+%OQNd!~&rwW6&nTiV4!oOILJs`#$?YoQB;9g@J(c)gz1ed|rvlJ}CLRmkcjjtO9faEK4pFcSbEzALaJu(38-pkVc7e3UQ|{?{4s0t6#eu`Gygn-3nfNKw{#q%9IZ3Pm?enkCgNsP{aO6Gozg>3>cc46M>Yso7_{aMb@DIBn=c6}|?p%s_aq2@YKH@g-`GarF=~U0t|HQn2EqGUXpSjfH!<9378Y~GQ8Vq)=;HxXFlR7PxrHQ~O?Gz7}U!hWCEJnzAn8yYC_(uoAn(#%3Pl-98AE3Vk7G^C7*YWGdtmS8scXJsGA14ew7lnCKKfo?5=e1-jFq{wgQZIxj=JC^ZOKj7J8~nv;@VP#0Vk;mLJ!ZPvm2uH}>xfkV2Pb;jei`;We(TN7Y5`%D=rHhUMUOk&@?+QgRaM4yaIrfPHwZFEY$pUNwfVvX{frW}4$jLfsV|~c7)|&p@F2oSB<RqoCkeJLHj)mx;w%@WNQKG-pTF<epHlZ!X2^1^$Z2+0KUqne!Wq1R<+VBAS{VZKxC)zqL(_T{Nv(Z7F7i4zjYlue?A)-s0zEv!S8#75xndwVYw8<09+!&HzrC<`cmI7fS?LrgC9ef_Y+93;Xtm5mPZUbFtDT9PNyN<B`c*|}q@9{1crz(rJUYN6wfbJfFl@KdhD2vq!j)}(1Yic!M2@>D+xWU}G(=^vJBP5+g2S=#T^e*d%PYR4z@=F<kTzx-Z-#oKJ(0Pm0Rr6${;&Cd7!7-)5(w5Q>-$eaM30UN?uXNi4uHe(oMt7AeYeG*RDG~RjuCEVdhDhKWcE=Od;;#ihw-l?qLLXbeTEBQ2b3+N)t`#lnr^GDaUY{!_6)?`&?k1f-EE{{j9giq4l;RJYIeH$UV)EgVZ-g|Se}OQRRg$wuicv(oKOr|K=hRF3w{G(!qW8Tc~9~&hr4Yu+bXW$!tnI!;%RKyWFm`HDpV)<v1FS;H9K&Occ=0AWMNy~%qDl`+V|77i47o!c2lD0JHF|UkTw+uD3Cd~qb&dxNF2?2_h`B=9@z%@6CpI1ozN9C^jmkbJJra_cmaCeFi}~v;!&JNSAYXV6}&w;r|@x}pK0mnQvEhk*wlfTR@?fha{B8J;-s*Ota$?>6bY9l7lfAHz`a+Y=$PtO)A(fo2u~@Kpjgf~|8r=wQhfQ!H=;^(WM5+C1jm{m!<u?14!(eoiRTHmnLHeI<;_2NOpm!NUG(&^Uj@)Q0v3f*QE6(x3l1YaYFQF?-ALa?Yt_(gD}H&_tR^2##H{ZZg7W2U%J^}4IV*mnO{5mrWXOq2?NsM^36}y1SPu(<^d7X5=TgqEpgz+zW$7C9QRn$zd`%adf?s2Zr1oZ%q8-lxZ;grins>&Ml4fK{voHfPG`0ks(fzxqCHlJ5dXT?&KyLjxn-*XZU#4oZHc$<Jqp!9OWoCis^K*C)tENT;S%X;ox(0X?I)I&N5ASCr3N;0%#Hm9dt!9zje#2?)16V=Fm<^RDn~Wq@yx9$QBsxeSg_MhrG3VJB%OW0ZP>sz+4k>_Ecj!+IvtgY?w^s`g0$^cpl@PN(+#yb}I<1=>3l=c3tc0F{&|Jr^6%)BI$xNzyL;EF3jf2cwJ^X1+dAd(^QWMrqA0fJ5X=WBqc<OCu<l0gqs_=lNB0X9I0xGAv;Kz6+ER95b@_N%6UCbZQ!*Yywtzhu|7D}SEoOZZJ%XnAWBfq=wPk;S0xPTVoEqg__n;ihq;{SC>pr*pEQ!$ykNu5(60`xPIgxgZUFG632dL%qQ$iJCYUE)uX;P#$m4);z?_^DwiR8|qb^C+P}(H4di(YR;v$~d?Xrj5&h@L=%a!IrHmNv3iiD&0Ri^ep$RD@mNJ4z>F<N{qr%_+StkqgJH9+}F^@dHFWrx%BNBSTUxd^O@e7&!KOnn~N#r$VO2v`=GLL)j#AD37^erZl_&w`H-X$LdQ`NQ1LV8Tt7ErWxI4Zo%3yQDbqYWA_F<n-%wF&OJ(`iL<wj<XFEA*L3CtR$|s;(pB!OWc@|e{E9Tp5gS$AAf`)azX|MTf^G#{O+9Z?kgQr)_Op44n@8?);S^;wXW9(T<FkkIL%JUi?%K64QKkZcI_qoOMP3b+rW^$Gyi<R||OVw5N#o)pSvUqDq&(7(*2bG6T1?}Pa(LGF`3kQB{#s@YJqnj#cycvlt%u{k7L>B%Sn2{hZxTmoeO?`1yfi=MG_wx{}HcKV1Su!XEYctYFn|V-)+nz#sJju|zHli^e;9Nxk@gsVKKl5mWZS<_rj2nnQ)9VvAVI2B4LE+1@oUMr+a0r&>hG>gHZ9gmmX%2UTCyKEBGsk3<)bNa92{=>P%N^r;tG(wK<qi}0?b(N}i2+i_&Tc%#7P{~<s3Ve^C&?~dVeq+pOX8@aIA2cZcod|ML65JIC;nu=YEn57z()~*fQWm<ES5T-%gLRg@@i)$ac*eIEW#KjOHH)LIpYdXs2+n|?Tw>Q;Aoj>OCH0}9|PM9X-%HiNL{|HBx?6ku#C+-%LJ#$3d$NZ#g4t)urN3DT@u`8vW_utmo)_1!&X&UkK`~vtQL3RyCW3hc<u9Sm&9nMl1ZF8+*u`f>@2anRM1i`Z-PZ+0cw_|D57QY1!YHyWe+-4&1p*iVSl#rJunL3BEpi?jJodsI6`|*EjU;nY@ryXc`OW2ltO|HofC4lCef<oH%wJFRrShUjZ$UeNvkx!`%9s9EDKRk_z26QDG#I+CW4bqr}l=?H1jgrO$sJ<0cBv*GHgsaAPfX&icL_S^D@~j4mBFayfnes(9DzzEI%#1yqH4uSbevr<t(Aijmh3)YTSeW--rg6d#z<VQA?JfS)Q6<Z3o9W$0gU9pu&#{ZUuBr^iB+{v(*9u+p^M#szJ_2OBDwSV8bf?s!6TE$W*hBE%)VW*8%3Fce6}?40-J9v10H~21D^8)S8dJDj(fQ^A>y&lE(m`A_q$Jn8<32d_O0~GuW{GR1s_zbIjLT#F1sqE#547l3egsQ@&Vt2jL)*nd~}LID?3-e>zjp-}{`;T_rGqBt+{r`k-RQ_Q48z&wp||M?P!UhT+gnDQpy=W+j3KV=TO_tQKTe3nB@I>o0D>r#cPFMw`q$?`rs2-qlvoBSW6X%Hax(42Sk{jqW#@Q?@~vLvPy}P@b5#q?D4`UzV;%ky(Os20lufzMl(tXwcI(Z<8yMl)Z;C<4h@*QZz}l6`M+Ls-iN?9m~pRgafAoT%4Eg=^?wk(Uv$SwzwV}wzP5+f-fFZTl>Ueu5)D08_s%~3_I1{vU%I<N$08?2puYxQa6#Mfbn<U6~~BxFoU98P8|#Vs#0q_oWj_rcO|oeWDj7T@C7o8xk3C>z^kF#l<W~z3NiV-h@ZGG9jIN*U6bOLon)q?ypkBQV<KyT2-PYGt4@F-^QTT!o-<K&7hFe1WkrhgzrfykNO2gG?~?BF;kZ|;P9_1coARG|HDj0b8KCfx#Wak~FYO>9?O>&7=a2a;x54Hi)meRY1gYq;6|jAts!f+=;9RFy)$b_WtH6iiS3{4H&oslllxR-oa7({gKX;Km6`U@EqsWbPc@<fIwZ=`vc{k>}+MXuqaU+x#3U-oZ`IlR*8;)vray#G?X38jVx$WH;dmJD7(zvwGk7jtY@-f8mEKPqybmke~Z!FCeEwXN}V_DyYK9NgH(d?eN%4y0%0uRI@*w>L&n1E}O<O>(A3}0wlpdkdq-cXYKW1wqCNuLwjQ<e|o&PvLPWvJClSc>~8uth11m>mXo`O)APa{{H5a}3*_%F=1|Xc@LjavkTLcyk8u(0pYU!$f}0V;o#5su!EfSr~*5VyPqeD{Gw_$Z_nX+~Iv#3Va*aA~dHaN0&@x?S@N&K2#}Pk)Jyr1?qgsa!%;3)B%xv2ITTp!36vv3+8m`3SP$TwPuj`&i#Zs)zUNyQNDWv@sro4D8R$4qI@oJ;Da3Pn$zc;C!gJnGux$oPA1yL=_fvhJQZm5`^xkm<i|PK_88*QZFA%^K?Ooe>|v?XHQfs(t`zOzsJ-WzG|Cg4<nWehbIXVn&7^kSlk&;wp77XJEr^v#Skr8L#kjVcLnwF-dae|FG;^g*g2(gBX8+CU*fo7m>b7#XrZ2QrUawP}8`Ee{HW-Pf+(tG#<a@z=Nz>t_>{c_4f+C;SPh>GPn3<HvD5a<h3=gCYmlXG!x}j8h&zZ!zMY#K59}3Bk(>z0i?DnP4+q~D>1evlFU;?&ycU0-13D!ObzT8}L9YA{9A#+7wCyA(=lc9TV23VHCztbAu&`*8bU-($YI%&|wuU%Rne)yhnW|>{ibJm5JGvcrYS~=^-{x3HB1#g@pR{j#jk{?x(mx1Y<&S|YSGe*p!+qikVg*homfx~?7E^Ao)?2iwDTDn($$$f_WO=`Md2$!E)Zp@ZmXfesM;o3~_B<r$QK-KVd1G|JBl$glpjz&J}ro%^2s;ak2ZHSn^d;(I3qG<<$i~krLa$DlvIX_h>5K_uAvr%@y4q$$@R+|Kk0jtD*`VkknU#hDVG)pb()F)xgol}aOQ~0J*&U^I<FIm;h)<_kCI)u*i7_amKo}}MGH7h<i@F`W%wkJw3rT9^5pI3=oCa0ZuQO}twAE9`t3TL-HRnTsb^LQ_C$Hhw&vvwvCs}#>58@Aa*rXtHj+T&e7CqYOir}mhHgaT5f0h`>8i9@!4v>qVCn&yP=H{sgxXSRZJ0AGOw2ASlAhhe!7wvDc^?&DH1Mr4|MlwXoY8;3GR(Q-X2pgMG(WciPgmVlL~;W__{@2Pn-tPAjYs?U1qT`{sbt7PYZxKc9uSLd`}l@gcx@|vihL(@^k#)4zA){{9;FW}FpO5g2rzl`^B_U@~&pELrdi5ISTGQQLp32SG^ifmFJl!A8wSz}lyzuR;K=q&sZMrsF>qjw2N_;?p>kso<UTX34BYL4Zk*!ki$P0DOKcmrhzHt->hWSZ<gj&@=jY<HgGe~LY<@EvL^y<oIs!Tm;oGxqEfqB6P2r@b+SMow36>kP_O>7G`hU?gc><wAaP^TTyOZ*bkG_W#=QRQ$qH+c-unV1wIINQ7CqX-+jyzL39MZrYMUHMY9Q1#KCtIQq2`7wy03$zyDH*^E^hU_!G3LSJ8Q5Smxt%xpdikgAgvOd^w!ty;;wv!MEJRBcRwSUZ_Evt$}z{maj#BPvIAe6lw=cK_B6cpI3fq4n>-|37~`+0sUC?ldyT$C4dIuNv|@)UA?YZt4EA8I6?~{Hoctx!tpGyspi*;}~TJ8#Co_y`HBtrNFWp33tPHJY9PqhU)dCGSjIrP26HNIK3rjkUB2=QZXO21zj~nfph9=Ja<m<Em_TD>b5h3A%Rz`)I)8ULYu#}2C?5O)`!0Ayv&EM@A*mH=doj%tPB%?d1a3|*BP}<`6f|0B-RZa8SpJ-?SOv4vhS~A$-d_+C6OX1Xx7_HWNwDIu$OsUZ$nXgZp^a+f({p^9_x+pvpdZ^Sv7K5)AcsGEe0Z)Mf{drO=fhlcG)t)DXE4U2!D!2Sza^HtxnyU#kC=y0DQbeaG}5+LiFq1)Zu!o^#&#OxY1*(5#WJ@shdzN<As_aV7;xq8ZDsCq02)*BV7`GPoS!_-tMlUz>S0FY|Gb+?I}2pn+?DvsYBUv3NV9x+PLR=dKj<0klU6Z_vEr2zFVQ}P?j)O_hz{DNgUd`oWKeDu+i~-h$`OpGpZFC`eHWP=f^sj+-5~K<^o`XTsNj?`f6acsAZoj%N{fHk(UB^2F_Fb%GsLKBxir0iV5$KE_uFiJgxwd(-nACTZtn+zMXSk3IcYbLZ&nVK(6cQ!Fy$Aw{tdYxfPg&s8lxf>2vW+w|Y%nLQNdYLUSF>U@!v$W(8(bgH^u?C9p8j%@5@@hR>4C<rI2a+Uywk{$d>h<M*hEggUuS`DITM5eEa<I^H@;5J(87YV#t-n{uy`gES5=X8j-qO43^vCuf8r%q%=Lc7r*dXKozLEZ@_>Tq;)d)_55__Ho}uMEQzw`ahrNyA)m4Mkl+4@O4Z3Rug*TVkQ<9;g&^pGc!z~gu>3%++Kf5uVIK{xU>%^`}OheNd3X(GMfP(BftBIx-04mR`o^RF~uvytiq&tL3rSjgA!`+rDHHdr+iWDZ$P;aDD0}jZa2+wnvkiBmcEBtr4!!3=smt7jW?RhnG9thz-r7g7vM#Y{yrCOhIsZ>awPFq0F|vVsWf$(@=TFWTOYGDaHIWhz%F&{aP)T-^mwT&#y=|DIF<E^HmBhfVk)a87%iJbo~Q!jTMB(szB{G<oinJX#rt)ZPc%CNP6rYDc@R{akd-ZRdmIzGzt#>@|EfdYT6E<Bp`Hoy5dsh9K%cBl=kG@;<K#{~zS>54C#%wr=N9S)KHtb!I-YWde<P5%-D1V=`pt*={nxjTnU0jcbFI*K{w(&+wdwG)ym(E=zZPi!HFRsd(M#0OUB*2b6I?7@5UrmBa~qG!axCt}FCHI;ze-COAwx5UH3}@J&5<QX{NZ}uZkcTODphS52|o!9KPp7ckEBj8q1!9*E*FkIOxgXm^ip(Vh8WSAEa(|zUS&(J0Xj`bF7qzyr_7;Z6q;X@E$3Z8Izf_CVTAb(69#xp@%kVg!$4ES>yERUV5Tw3y&xU`_`B|0&vU<o>2kPlSR=S1W5vs5D+2ni3jH0;`Qbq_e2w@0`OyFN<8QzG_9J}w`QY!{#bJB@^~c}C=aDUiKEVO@5mxtDb4h&`u}jRro_zopzXZNP2#}!-uJvG`l`=M=U0b*dudn##c8JF{i(in}KKr72*Qc6k`~BAs<G+6OFbmldBXRm2zUDA*72Yz|-IW`i5VH>rS7x+klFYMcr=A_%fB*4OVX4EO$zhj=WpvfI{`j+Rf}uF(X^EW`!@c&E4U3E_{_UTC{q;}(_4{A`?VsU^hy#0Ev-o4Dp=%QTriAja%&ryqy6W*SVm2QOKNRj+n$8&-)=x0j)94@D?}>%PHEq5F?v!HJ0JtSacYUUjo?ZbVOMBrn8X6u)`0ME5^ZR8@_vC38{XXHL;RTHA%G-pD1}bZm6F-OR+>?b<escI3qn<D{1aa_6pp#|w5wadV^n2qyS?}LR-vdfGS)O`WUsR3>*1r4AZ@JWRI^}kdcSWLOBhR0Jv6no+FMt2*-+uY^u$Pb1eILsZIKSFMX&mA{-c^rD@)i;ParF}nSObdb!(BCz$bj#~W`kr-(a>ei6%B@m`(mfL_<*2eV*%dbvisS$XD-=`d+_Daw0>jVBRobWsh7+ir+jD$ThGwYBvDg~{xt2FQP#ft-k<B$5F%054D9G8sNe{ksY^$lM{V;<1Q6?ws6DPp@^4v6<s1{tZsQzqa835+ZptU-OTsB1iA2Ql*Z2DL*|)f1%C}*EL2LuLU{-a+S)hIR{?f5V3=I3LIv3wt?;9jf2kr0_?pU?&_88JC(i&9tAm}VTao?KcN35Pbrn!zaxRL+(%lrF(NHM|3O}UG@Lqr+^VA^BJKmRy!KH9>*og&%&V4@&%A)(Z9V(rmnF5UxK@y8s-+s%JyV>%BUz>G}yh2+^|tb^NFZYA{|<mZodY(H&2zsKkbr1OQBHji%IU}<bxhhrr2oWX;mAy|>3<Rb8+#+wR-BiL8~SnxlSN}``^90%!76HIBdu!uERY(bXJADeP5!Zl`+yZ(Voh>pjmG8&H<`mKaJ7^L%@+R!nWNtFX!!D412*vO7?EaD-fOP!+}-L4VvxQ<OZ^`!*Z_`NRJ*t8>pqz+Nr5*`?1?1*GC(eSsvj8~Z&W6N9gK#*tSa849^0}}6`>m?rTR3LL(Fl;0O#=gyg7$;j3_Yz^!l$BovHQmd{*^wGAOkYo>GxO%vmlpahyDrC^_MX0zXoj`FNn+1&8hS<%y-SeZZpA3TAD>+8IVV1p8|+EJ_A14lJ319=UbIN3b!drqevGAqdr(XD@*I@okWBZ!W*HFHLWFE<JmsFQ=fJkIFbFvOS>~yAX`upD;yX?IYgws^uN(jRJh;U<OO{^$TS8Tat8#z-@#7!wGM#chdh_Vcg|pl6uONcmLn9?Qmh6pL&UsD$6Z0YzZD}Mnm*CHwd$^|uhk(VvVAl%vtU}6?eGT4j0<b(rxw%+1PE<{08d!{w_vVcY_VEvN=9-YSg-?k&pdX;W1X5&L)$HTfjdR*;rS9f37(PxIdQPkTrhb53*dC&c16g}M;EO?0MN5m1fBdxFrtGy5{KYK)xjt-SE9e_KW-84ABQisMuZ+bPI5^SEP77`6@oRK|2?`H!P)CP>Pb+%d;g%n}E(xe}H@ndUCS}YBp#V5*wi5!N(|lppKSzn+1Lws+j5Cif({qU?d=>m`!bl`QnWV+Fnigw%S{cj$Ip-`pq})!ykMjGD{V8=%Wrpl6EvcMlcU=nwHqtN`UwDH(Sh#vB1CjwXpw(?)i7|an1!_sM?d!Rb7o3ulmFIeHVI!y-z4S*w3#t2BQkI|;(3DAXuoC68c<b8DV}|~V$vHd#4X&yhwb#63)0$L8D-S6E<3#s6-5FNCSNp4t7@3-+EHOLj74<D+iz!^L&rxr;(uPF$S5}y9W>H`m)6|Z;DcktE3Lk{Zvpa`?WP%8=@n#z6AImhpqfn+<G>}MUau|k2jy;jN2Oa7v6g&H2bTf=fL`^5L?>~trVsw<kKAhG)!2AZ!X;#$Ocbj=#RSY|nYm^+>_1I0fUb2(eV*o4iK7>+}uuhE}#7CJB9z-i1S~I6@E#30zw)9z9fXq;amlm%oHg>wLwv1^E-r1WKcSB#V=_a`miHreDGvs=)U=Y3wqmCko5FI#*VXdc|f?Ugjk$+$E%m6_RT<BD%VSM#*S-<y9nHm5SKvTt7mC6nS{{p6m%~*-Uv5z_2?dPbinF|1?C%+LdPs3|KaK#`k$(UNyQ)QRkug^}y{S7uuUnx6}%-v*8be5a&v4Ac{?|Af=9_fOb-ZZ9(Z%12zg^(NtYZ{@+)p%qZoK*xYVV*2kqvgX^vd`|+xO5~xkZwSI&5B2HQcD?Eg}3A(>sq0&JzvXd>1dDo9+pPt?@X(0eO|~Sn-AiokfBVi7vez)s~VRfl-|I-k3IZxPPdw%nI%|EflLH5bm9D+=9}9`0GYue4+tyXIM)0a*3{Em`vo&iJWI%@9tT`#(k4ClkGU*eJijq21_WcEWusKWn;NJHU|}awpzXdHsqtv78va|w$<FAU<)aBar9zP{U)}~Z5to;XC^XFRYH>|!hPc$r{0e?G9WP5Wp^rLG>*ABD+f36M4Mkwy*T8exn#=w*%dF8o%^PD@17AityI9NqUERS2e6Qc&mcPKzyslIV`Cm4^no{nP3pTx;b#U{J@u81>usQnH$%XDFS?qNU@FsKsQd0(p&zKIX<xYuvgurD~IXG_tp4L8Km@DC|#h<5SkK33e-s}eRVs+ELr$|Xpe>xq@;tDRuj6eh?QQ&VdnP4>c7l{#j)lVRB7xsklaO89>cqi+$Zgx~v!1A&}e+Hg&U8I&d{=#f9sjd_4g(SrdGIO)eJ>91|DLAWjMIiB4dX~B2o|4}g@wFUQ%B^N8Jj$BEMR7?o<r)g!*9!99Z=57LU7!IZOR3yd7Q^o;#1hgL&MmXS+s$^CX@NgewFZZ{8$EK`gH0+t!9(*UCGs<pRohZPEjn~DW(8-|-^{ZA@uw)aD9&K*Rbhe0F0Ou+fZa*vjKFpIdY2p*P1CJTo1dpd9tms-VBBR=%G(+9X7d!fEM~03N2-0<<K9be6ZEan(o-Cc;keaj;y{Q}aXHaN0cI1tCfVo2gqp5187j?WIwMe~Kv3!vE^+d-Gfy+=>4Ir_RKV`!^~{t8X{ssRDn*jQ1+UFu03ylM87Lh+QPbV;9Z6NNXMN`utRa)^_}rlR9Qsx=a4<v3wvIlkfz&++u$z)~Ggr%<8rWhyha{hg;H4-Z`|OaipE>9Hxe+Vdr6WR`Z-c7?<N<maN|^qJia69WQ6Jp0V{Vg^pGF5{rGy;1cMv%m7S1CKBDD<jZMNZs92`UQ3;ttP3w`FBQryJ$z%6Z@0VXpbve2=gW3_oX$YqaieyP%NwF1E6B^8jl#auc8Cd!$AUxYbp!aT&rz`~;lmIz6GN3~EFO@ijuip6{2ya!bfVe0Ae{OBgY&xHfO6~Nt(A&zd%h7r#swlL2Pw;l%=m{F-HIOGvt&?OU2hTXna_wx|QYyosM9noHD9rM5oEVim3^k5(2Nrv9F5u)-S@2WV4AJHS>I*&%^O3w;S8i1fYy*_ah#-VQ$REI-WJTT!P4nx`8Fx4^iG(Ei_5}_+jZj9@gjI$a#qbLK;RQ7Vm9Ea5ncZ_m}@qK&tp=;u?b^>RYrR!YX>?3ZPr@^M7t<t?pXk1kO%1KBMWW+J(@iq3*pX^snDklQ+$r0O$$a~DHz4N(e{HmeQ-I<i18(u$)afv0ph_ErIEaHjyW3a2eaTMJhEfeivWo;41!1h9FmnSh&moKZ$+wCzdKQqrVr7N<65)46EoL=rhnH&B)38*${`<S=O`e*H7E5Lxq5}F@Yi+oe1JY|mQ^xEgyt}fHOB-2lH$mdFk=UKwBsW_fo-UI^60@N%^Q3OCI{Q2ZavFt&oWHN2adf1<>d=F^$4LX>uD=oQAH6-P6g!Ud-MX)^BLPehx_Xo&Q<QS-l&h<~&4Vy$OEU38UVhxuA5#+nmX%*%cDiitLUkcrTS%`wdM_4OPfeLWVXd?-pYzhT@!_cpJ8SPFK6BvYYvT1QTCLs{O$RJ;ym&xv0sqvWRr3pqSNNY-&?E5*DUSe6HpsK#x(?yu@PRC^LF*WYN|8GQt%e~fxpD3?N^fph;ux^)d<3rLuX-_yNSkkWw-iZOaXF{;)qRcd+YFap=U5Wz*_;r<j)vWMfWU7BlWdpf}HDj!Iye+_8H#e;qcH5lC!UG{!MubZ0ioWjUyiRU`l)+{tbUmFhxww^Cs0hSJVi!CulBEH#u|gdo_!*B0t~UJexg3z8_U#9n!u0ZRWUa+nS*^e#*OT|hh3z#(n?`y(!F5PzH!}hiVlfF~%YE9<`P|h_2TC%nYm8kWbaNPO4J%_l|H&<b<<0k5yLhZs#FQ6CfqGUdY1$Tq*O}GC%&JM`cX2Bt`I>ID>(lcxho9wTZZf|riViD>Z7`lE+E_Wd-(=3|#^4^|fvD6eGF;&qzivsXDYMk9oPpxhq@@D*aA|pCF7z3I=F@qbTotzL<&+tD$|{zkZK4g?RQgvH-C=HBR)!-$JRRWTyopaw-sLstSvqQoJ-YoK80W+Mt$pfK*Eurx4`+o<QmJYa=)CRqq<qz3gsvAWImqYfbXNAUPkT-#7|C#9%JBuNlDQR2XV_UoLk-__uG*vdf#&31Z097F4gfG_HcBDTP8QTrL4p%G-+_HCP!L<SWz|AZq_K_Wc2~?ST)atYq}Ld>ferA`<*;J1OOjR~o9<PrOpa|AAulQ*yX1a>Es5CwXQYm4j|u6kBN5ADuuJpYjgh2c(Qn@LT#8~okJUyuX}L|WYD-cqSb??2FO?o6pK1DeDUtEa;5vS5pti_{3r_07A?8Ldy$ZX}(r<r+VRvJ`tL<iyb~i%2qA)3031GR^8sn%UF1G_dL8=UamfPM9z{kOnFFZ|K{wn>-ZxP-@Q*+B834nXi)^M8`QHrj=o+h<vGa)D69R&4rkrN>DxnJ9nKMYMLN=&RXvh7$zD?X39?U9AFi<sKfX8<Z!JBzqHxRFq5u<$9vbWT??E*9EJXgtO+QB>>W80gvowcwH$lo-e`m)cnzY84%pa(|*<K&g}H=Yc2j(RgXv0`5E_ss;wPTZXNY?8o^oZpMLg><dh}X_jRiTt&SXTl`t5i4UT(>l=1ub8|S3oh)6vKTd(7<64BK;pFI&sjS^FR?r_TMQ!qP$0Kc>d|J*4-IeSq64rsV*(#2MKV-qrF5TM8xV_e-)4X9nr*5`14O~^yD61ATN#KoHz4=_=Ko~pPT&kaQo_zX4PBfMFpP48mr_cKs@>Ec;=mQck$D4zok0CDIHb*`aREtOcG>DDB@b87vT8c+`PkWFA{g-;p=JOzIZn2VL%G4fvl3oda-7!*CUqZEtyfvSpH9F-d7pcThI;65opT@Cbp>tQW=`2(CjyouQA*u3T9X7P{fXjw0(d7K)3*%fkIQeO*zy*LVv()c_?y<CCQcXcqN_0fbQ`K{x*B8}K-wndmo(wtRTv+D2j~Jr(4Y@a`Kc8K+^i7)gTF)g@UIYBz7Ku?Q!a8cg%W`v>iU1zCLk5muR1%FwCy91>c$dLH;~EUnPiWp>C|brk1JlJBU0TO`_?{SKnTkA2s-NHOfuEC3u|7cdA4{@TbRF<&%&x8jYjDlUmRN7LJOeWaNiEA_6Rz-HJ@O)40(A1DDyTHjk>^{{v{f-OmRJt3TQ%&i`J~JVuKc~bSY~NcJU#@V7+z7Y)@6CjYIDgV)pBE{h(cFWmgv{Ul;@9^y@FqdJ^<Jy?0d!<1@|HIQ8!Ixg11<`=xRg6{N+QLx?N2N8eIIx;E;0{@6P$DLfM(J<VlX$C%Aonkye{!kHPK4?)d>HxJ{}_Sxx_#=hUa$&RuwluvGB4cd4q)cg|;BWhFveds)bf5l-1-ywWdtl9UXkyZ8jb$5kaHJkge<*5~&eKCGdPipd?}t^9MQ|4EofH1Bf_voeVjdM{8K#)}rym?l546c?(LaT{qT#<(kzWrVfCg$ol{uH<sK0CQFeNTqT!HZ3Dls%_DdW(iENtsGrT%l#%iME+V=a3J6-kS!vUY(_rVhP@)9fs5%F7i{iPerp<eG0JsD0S&Cg>=4nC<v&JRLj9h$>HIIgxaQHYF2LtGKPxJC#U<#hlAUnldOGM|ozs4mmR;`4Yr3co!Aupn4UWlL&zwEIFF&Jhf42b<GHrlUrC-p8q(zg7LeYFGYGr+)Q}uC_HYun~k>!A9G^~@~A3Os58r9BnIH`__O322?yJ%Sb$cz4hjVBevwJ$-w!{-~g-RueCEtOsL!0|M)bh3jyT8?e7V*rYoD)t-0m#M9wgVBx!pB=^M*w;%)_v9j<7RZ#yIo;c>Gul@G2wDV$0jYJleHNQ#^P_%1QE}a;_W#=IVEn>TjyXmwx~;aQkYTfs<y<y_d?A0i+_V#;xYgxZXyanV(eKqld+}hN9)Ba)h&lyJ15BuLd=WT`AE<2Z<HT-0PLgU177QR$;!aKY-dU!8H>y0Qn0ER8ypfjk=Z8H%fR6Sfm72<)T3dNjB|}sx<@ewJpFf^VWTOFjT9e~r5?q76@~@B78%+0?&1kFy+gA~}&283x<Mna29mgm;2*WAO@bx^MxdWEINa!>C8+A8QWsjRP`vwE@9rdQ1nYfBncWlkU*IA=}$G%j|1Z6f*Jz(HG)>6~uDRS1^Ww+fE45z%BpB|dc6wb}r_V|w8D@KLB%)Hu%Z{_((y`8Z-xhDw?y_0n=cT+e_lnaT`0tW<qOBpesoU!cttH8VO`AUiNj2s%Z-d>{5GZf;z%;9<)ifFqrkKqLoGfW-UF?F*$%{;X<a{1i#Ho9#UBK1VvkzB`UbfI|JGQlaSmLZ6Oigj0>^ViK>b=2K@&R|wd&_wE^KurUhwBH#yH%RoYw_5j8Vvidouo|@>NN>97KLI{zJo)vu_G$rvs)R1){EXyA_TXNCL+kDCngt9kK4)9LOl$|i;oEG~ElKOi7Fqxl?9*UA&(p(H?S;Iv#Q!H(>+sYHB>^wt$;l_gO&V@};+nQ1EO5g7j+#CgRcZc1UqD7X8ChqS+kDB!T!1%_>&A3*Uk#cTwd_-6*<;o`@@xP<z<GEb*i!f1n*Dt$rl&)O<N12=C<4SuSC~}E@jIj8+d1c@Ae1PoS4xWlB&?nuyrPY08q1E^tmS5B7LZbT-lxySGu`Tfaj8CWEDL>yG+)6C2$&U^&1>lDNlkR~19y$Mv*ejM8>5!cI|jbLSWLiZJ8B}K9<u{i-V^J1C`PX1t)q^B1c$0NFT%JfF)ukt<M3jR4^p}$4P|k1MkvC}0`8zb=XjpEaWr#!PXlx5d(m6t<?GnTeTNWbC&uajd{*xo3O0J|E#NNC3l2<J>_tSN)Sq6*#mqV?zA=mGXXcvT66rc{aG;y$dwfm=`|x0{Hu&trNt%7UJKB_RA<b68hY7j+u(>O=3fA~Vx-x|+c<B~nE0=T!kNIx?PT7@jfSW>(G@y8f$9{2^<Cu=*%V7Y)5>pMB2Y41`5q1z8G%0!=9{J|b6pc;G5i;vEbV`rKz7~{KgHqHgUBefhxJFZ#3`P%UQ77!By?HEh`V^=odBSP(8<(&TUSfvkn9j!f(*(vbd_$BB85WYl1I{kdV>A_zFD)8t!|PTBA~7!9t}d*P9t_eLatvpDG_C%bLeEHeH#;2lytUCc1b15>9kOVP*U)4+uJ_s=qu=_}7eIc%H%KCA)a0Zp0n#wwflQB=oo6J{B6c<GU2Ui4o1avrf?W`NN>dABs%BClBH@;EYJ)A+Ug~II+ehmXX}xbAZGv#Rq6Yt*Xzc(q>41i=bB&3fN2**K;GJm>u$s^@(%BYC{jls6;lfUGP==9ZOT83Yqx~F=`gc&K^O}ku<CbwbGp0_rF#CC6z?^PZq(iXI_t$z}>tE?IRz8K$0|~{D*I7lcAn5@EYndDIk}6nY)uP3`$62nBavFucTOSVXJmn2f%15bq=N^X`wrXEz$WW={Idsij;5(U>R_|PQOQ&9Lw_C*iT)+9Spa1&yG1HMUyRQ{y_n$@VzB;{}*^+{@Me&TZT*S^+`#3eNn^$J`P1Dk|3>Qs*oPX)7ECa)SI*B99ze`LH^8*>V^%tAi2@^yLh?+?pH&+G3ZEmLS4Q%Ha2AU#1R=D;CW*ReS7xeuff0rdOMsSmtkPBEaaaw6b#)@0TR)l7teX%kp-3ATazCZK&{`TW<zx?(ieE8Xf?c0Sg`u*1*e-EGktb`fn_Q)(>zZq=yvF4JMGvaBPtXpdY&QUym`0?uyZ1BBvy^WPJHlbZxxC^hZ_~x>X#5Idw#1G3aOuKe5<GDo$7y1AF_kaI?8e3JR')))
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
