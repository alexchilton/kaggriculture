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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_NkvK;td_}mYb-<kV1hb-|BBH08vR6#2c2Y0o1Az-1!;!1B9`tLi_omrI`Zf<TKS$%k}R!?m9ba%yvM})h%x%t0-^MCx)fBWZe{<r`1uiyM%|MV~a^`HOc%a`B$^69tVzWL+joB#4p|Ih#V-@bg~%a{N4pZ?|l{^$Sx<?H|S&0l{1kAM5+*VpfU|Mv4YFW=n$dj0g}zfJeYi}O$2<?BEFcKz|k!}tF9A20jQ{Q33Q&wuql^shhsdj00>-%-B!I*d<0|M1hNub=qs>+PGD)_nW7zh1AueEo-F9KXH(ejLY_<@n*-fB*Y0>!14iht~CZ40`|7@u&B*C_d@_gYQE*eB|!WvCsO;??3$b-QT|a$mid`PF?x1_YF9FSn*fF3I6!$+bf!%XBwm3|1aN*_P_WbJgVFEx6f~1eEX?f0B<w{7|l?QX8pVBj@*Y)?x}ooiUHkE({I=7cVE8$)Ah&KpMkZOTgM0dWkG-beE)0CcM3y!@(h}C2HPfsLjVT1&E)p!^Yz#AtG7*1#@m4Lnt}bhuj4+9=kZaGacmneoypvIwDo&8{KGKs#^~?+<7bY`|K!oO@wt*V+5XV`?g+!3?PzD+G!LIDn!@AXyh~~Q+->p9BCUU5_j%i^1U7ZM(Dx&7PD1p#W^=45**z&g-~HHinY+X?Gvlz!UHtSj)*b9KTle>$PJeLeZ+*<dxADi4^^Q*^^FHhZ!NP)f^#d1_Z0I_G=wlNL`uN+*f`X^_)Pj~DmHNZv&lO)(xu2SwA3KZSB?j9VKS$+2;kWF83!R6@u-1PQ{)&Cu@4vhLlk!JifBf<K?dQM!yX&u?fB5l-|Gm88?tcmXU?#=@p_B7BH?O1kHavIh+r9hIm&T7ZOG~+aDtGwtl$QRx;{15-tGBv*rp`x$DJyr)b{cIw=iZ~j1pUu3D_M81JpRnb3=^E+Q{%ngH1D?c<k3EEhckDzbM8*qIr*$lzLizHE~ob9$uFJV;r}(1{A>TxyYIbsxrZoU_})?oE4DHF^s<<rJzSo%7`@Bv^TJ0Tp=s>zg?2#}xClE>FE4_2!tu$gxjF=?)dX(hxzS4IO2YY*t9jOCq=OA7j}Ue+-0ctk_0zBap$^X=t9-YDn&3-X?)$J$gt78I?BF3Km<@g8ljaSa-oqQ<J5&CCgO{Smxt<b>bX}TbT8Ce46=p*3V1OTn%gX*BK>Jst5cY{IfE{P(h>+v)cS0l*u1WWVjAJ5qBz={7IDBs;c##c;pU5m^KP!2!J?nE2Ok^Jz?~A%^09Qul<+W>W2mDxz!y{AoNJe{MqVougMsHn_{Qo1fPj-&@olT>)_SxHK#qhMsM7a1Auw3HfE3(ve*R65zi{%6_#B==;G&jj)5-uY*(D)J5{x(Dns~n+D|0tf@1|Cu8c|_+OOB6TN%s=qQOE3w(=?-q7AB_9QRd^803w!)smogOoeR*%T#RZ8-@@W;%KJeOv52|tFJi<@ftsDLX#ObVWm-M$j*v+c)uI{H-LNP*!%&xJYys7i9iZt4DVG`eGtplCF-z#y9ln(+xkP5#l{kYuM9JnIft9r6SYdsM!ZBpZ)pl6(B%+yp22|n&SN^@$p*8~6qh?Rheygb)_4m*jmtkjeg7s8%F$3g%<>qIh>0GHr{1e`}nzOuik4m^*-CuTulO8e(dtUmdi?|yy#CF_}h5MZc>vp5iXE>B+j@!_#K=YhrBQ#gNZluvg4GWa`)dQ))DE7O1AYT5oAoR4$yJP9&9mAbqCvR$I{PO8UvlAboQ$Os!b?eX33A-fV)@O~~Vj_ItANpo{@&i?N4{_XRxpKgD-{`%{G1h$PLgXr_lO$?wDK>{wp6SHvVZuXilZ%2H8N_@aLfAMOm)ra5D9sK<sXM7ZOM(RgN`Bt#;PXSqcmhRpN>f9CvZC4_eo`vdn+-jI7v)d4ytl-!=^EpT0t4eAI1&Y<U(wW2}^c2|h?sA!>HGS+lOqzt$>0*5MM^YeNrw-Wt54#}I3-kogt&ls1`*Y!XLwOF_{(3Z(llH(`w*jn({kLfP51;n+^+zxeaMNuN_4*5V0K0-I>?M>DKN*xC3f)V9zuYL_MP<T|-=^=ao$+JoovB2A(ESfMxr7>Wy!q$#*RJ1xFHz=AHUp%ENGvY%q!mZflH1u}?p_wCaRz~TD-iJy)y!`;m*M6=5CjLZ@`+JmRZ?Tdw=A<%sdUJ__|(4rx9qag^4GoHHNvuiYfGVoR1~R~<;pa^u>%E<NlD}vyc$&03QTZc!T$O6r%#_>C7=hu{WSd%ma)dwH*lWxFh}<%+Wz9o6oZTxOcHs4kFGUV7KC!ARi@JDl~?x4c58rKHy(|yqUZob;`A!f9H8SR?H|=n<$eZ+>Fglm1(9REb8B<4BP;Wyp|8#+DuK$yIRTw{R=UKM1MVI~c&Rzbt-9rIac;QDG*O!0WOI3ssY>+dAp3DH9K=sQ{P^#`EZ60-m+7HiFT=@CsP^2yU;}$My{64*7Zk&t9KD|X6A;`=L}_U6etmg3e|`PRM!Eb^1Iin>+eVbkIgH5<`V)(Cu4LU(kh}%WcURYyy94>ywRqJ-UmoC`*mHlRZxDz@e<RL)+RY20{MrE2`q1H;n%B9o|LqKGQ7Od?HFCYP;5I&#Qh56TEq`RPEO+y?52643*;g-MbFwvgSY;94Jpxgesu+5I=$Q%*tc^I7Qdd1!01$(K#Ji2dUl24N4|s{fGWxQk@loBe*wbL)&-Tu~%fpPK9|cyJ9=!J(0TtZ2b@^Ium#riZKFWK!z&w%_B`knKBPt$>{C=%|QB&{vqG7p(u@P`lcTkB$Pn>TB!@nu%s7>kX>w6^W52|6j&yLRkcQq+2@_{<7QV|>h*$$LaW?OSg+k(N6;9KdJ9Xakz5>5c(nk1Sebb4PmN31wXN05Nr8R&48PaQZ^oCtO%HCj`AsmZn;NMtmBDHi3Jj7yW&f;fct?AZkWct3PLm|n??;h_9}%m5y@OPd<S-CIK+{YWgY5B&R+IZE*l+12&sC1S!}@^RF|pY1$#ah}(vZ~?S$WQN`F=<&-o5s{)wM!tUp^4rwsW9+3LrRH{y_>uDZ+oQzG0~nGSX1Q}dCrcNDlTi@9ct`^lZF8GiU3bmGCN>rZ?t>`>du%+*O7KK@9mfpN6TpgEBq0vxQ_07Cd4$fiw6g#giKn!yjFo_W_@U5Lw(Ap;Vx3MHcTg^wj73s^n-#wS`dzemC8k=ldiId)=?p$IR&+0eBEb#$FC*dckNUbiuzPMT2?Fh&bu27<25&K@j^6+IeLJ2ZeC*5Q7CTIosXbdzBeKCu#w$P@CCReWEBqs~PY?xZ@?4-2l4zENBzcu~j5C_<+sg|C!lfXi3iZsP2bowAiP((3LQI~lI>At%MEwY6aY9EiW(>bXC0J;;j1Ch?d#vGAlVoSwb0-X>Wqj!}Ijl*`p4BjxOQe8*YNLO<D{-_J$auht?kEV1bf<ZscVw{2OGzA38ze>1sl_#uk)1Lc5CUU|`R<Apmt-<P-k{Ge(+?%A#MWtjx>b_n4PxLU6}{&|sNCq@|HLd%P?&a?ilb$1ishq0=|x0C78~s_F(N<SwKsgtn%bOlg5*%!D}^m{jJ)t9VFhH6$ku8uUuF*e)ja-DWuDR7kk<TC-v@EIES3c*OOJ1fyl$6#+zG3Q9|h(SWT@VGE7Pd55i<%bW)-@El6xxQfu_<Z-8saIB}@|^Bv^~5QV@vtWlZ_@bDd)Hmmya%6)v!S->Ub10dt{pLA9UW<t8h2AkyQ@IZiUBQ^Fa%B&B`vCzR4wB#uLY*x*QI+RGTfDQIf?{p;&*S4mYw5qS&00`hu#4J&+kQ4Q1IYc}8}QlQC47A!%7RL4ZHE|)R)zKAE3#Be<~t7zd5OjyWE%A*C5qg?rQlq2ze7C#L@i6!C*bct$VC$)1WWZ}}i6r$`J85Bxb7OQy}Y|G{Tc@182w75FTLM}nmvOQn6ELmU|$LOnc^&Ht8ysl%9zwDGDngP=VLcc)&2vE}(tM#{@lzzSbkmwM-9~?Nde1_T+!6Q*N$8O57O;7}mMoqcwOy!|mpE{Erq_;%ls=Yfi;iTl!0!#neW)sd;$=o0!Y?u*oZol_3-EUt@EvPVdu=K8V6;<C$2z<HROEGkAtv-_+5Ea7!n)fJ|${O0tt_GwPzXBA2AJ$A`g$L?BJKhG|JyLLgi|a>~y>TxbA;0wCSAskKaWUS9T$mu`_X5Z!ngI<4-iEqVS76x9-{$$a4Owa&R{nwlO4`)*edV4|mjGfFn{RZgm8}S~0sp);3i*p%9VIDF23Y#0<Wt(RsFt<(g0t>VSHH8?)Kmt~{2NH^`bo4yZRm5lTPt7Ws$xS<iFq{w<iM%0Z%;v2tSAlnz-%pOJevjDe6_6=zf!cSWKkYUNe8(r^BvZ`ASs*|CL!LJw2f1wby}SJ8y39qu~J{>vwFg+IG;RIm(8aHY#WO{9?<a0Eh@11MOC+1=~^E!GutI6%5U!+0P{vg<%mh@>O;uZ-qBXPc^{i`Gvebt9HaR;$4J!I<mK0nvLq`eNT`9SM#dV{>2NLOHHB&TTzyV`p$3Q>5sm<q2jrV9ekq?;y#Y}Fs2G7Zdk<8LLM7{}J=1(r5OODqSD5YxLX^OAgcLId3h=&t_T~%u^W~kLB<?-x1~tGVl0d_viu}N^g2d?NPkN(!O_^Y(th}KrjU^@P>dS0c=>pDSNX!oLnm8k$nAX{|ID7SN$9j_bU;}e5tml_EG-MdDSiy@}t)FXs5$9z6){`%hP7SXw0~&+pWEE~<<1l>ryWLxB+S+n>$t~m-HGq;WV(C_$Z(U}?5~{N9k2nuEX2dm^InZt@nM<RJq^8Pm2*>p7-H_*BjpLs{z=Cua#({}BOXvq_QD-V8#uWdllyz`ODrz0A|A~1m;N_`X8Oz0pNZcT+rvD^+Zk+7Wz49XyZ)jyBR6C1l?&3-ks`vnO6pa1Zf71EA(8NJFL+j=&<LCCAMmMrig>El+HA!D|WsyQ-V)p~?1*H1sM1cJ$fJ3h>n#L27+%+$ybax4FB6qZTZHOQ;?iL4JtFJw|{Vcy{D!nQcs{{iEK|OP)QKeJ9=`o-=+RFuutg2r<SQOb9J%(tai0(t|4L}{5x?I#BfM(w>ar*ti%6eYY-6)u)RY{@thzmJ2P%J4y6Sr&$7LYJul340}MDiI*>mA?(*pb+o0IIEmx(KRW3~z}}1Iv)rMOA<n6V?6bN7H9CRP^WoNj9QI8M8quJ6Pn{B}#kZ^L0jDeN<aiUxfiLpyb%RynlEwz6JC6I>?#km#|7GlzZ{U*{2BuQ2`{C@SrO#MDIC=mNK-18W1mqUg=V^su4ty46ai`@H(Umj!irc<TbA4MMN(Fr53EEtTma;KaF8qlumgIqA-=d^_qP~4$J$6m6Lh5Oj{e<-iaaBgeyk5^Hi*_l`7*W>=c%op&W@!85n140XC(agghan<Fs@F(q(yKs~ZSbY3N8{Qbe=hr-^1%yoU7YF>2%js<AFxsoGqYg*a7u@ZzGXybto~F}+M)$w2FINttSRR#^5-P6rit(}||$Q3@$n8%wXH6vV@_c&Kkk6%xrcYpRf!U<<FwosO|m#_D6G!aTPlsrdxm0b%om_K(B~$$tevKcSIU=8P!14>Xmg_iLzYSD&OUWxx#L%*NpP$IErtqX6!1w@$eYQd98fd8K-y1$SFnya#QQO`9t1Ag$mKCkzryUHJY+og!|G+-6hy8NZvTSKrVBXCW~LPYG3yq@|7T4g=#f@k=a~7`elYw`0|lKp?1;e7(mQV`a;>hrXp$6ujo@?T#fXz{o86YAqF3Nd#aTnA(VqO;wM#DKymT(+l^*ctVvaWS)US<VqAM6cdd=(eo!Ms-n;ipKPCp{K-kbmgO|L&JKkFa?MWACWamk;Vl55H@rYK@moMX(O3zZ?4saL^C$PdTH2Wr+wfKh_vr9U)S+ICvZ8hkDG3Z-zE0(2SV|-`!lcTkyYI{<(T^tkVTxpBnZT84tWrnPXBiMmZWcR(ByQXYqq$pBEOkbn=(X4NUNmw$0RXOkScKQ})xBYHBVrw_A#d~{;A;N(Z~}JzmlEN1p9!zKvCQ7|e@9ZbDMkj20V?~%YOb+{01l)3D!E8sP4QUrZWKAS)Gd=Hs#MJ4Ok1YYtrYdgEz1gK*Ayk?Og^EeHQd#$eb*QVp`%F}zS-E@O0!TT(A<B#o8)sEya5$_qsJ08U873$y7*#vgXUCNARPk6#STO#IC>0EOsIphQdm!L=Q&O(V!rqiYezRP)3zm1J#CK|b*8{a=xlz!HDGAA$F%@0W6#y6=<zYdViUNl*p}P30T87G=o69(Qhae@#-!j7HS4q6#t@|4+{rYi`nVOuezeqzC(OeVA_Y_>P+xdq%VBt3c@ek-#6Hc~KD7Fouv?vd6m$ii?|%3moH9vkD(VH1LQkaxIz%4RVbF;L#BLAw%f)p+C{krX?!RBg|2PRixnz5hZXlQTY@EZa!5griG`Om&5&-nlj;IV_vWUQTx+3|kW;f(#L;Xr@%^}kdz^xnw=1)W!xOCqM0=M$3#W&r;3(8H0Cv@>u5ycLcl!VKkLKZE<`9Go*1%OCpN~Fqi4WkLl04peZTq>CJ7UVQ!Vt@&H5=bh5rzX*tiik#LcoxvZvulNlpG?dQrePu<{q8oHUI}9XA28@LqF0y8{ZJ!{jMz<X$<%`5w&Pb)7?MJ8n0i4)#7;%sZX#3zi^rp_WdTHQYbvUHG_pJ)*o}bE5nv{9#tMuuN>l~aO!hutmiGiW?-q(HU^iFFnJY3Im2NOkqGD^7?<8PmF>tPSqYkbTilEyfqI(;Fo&Vhj(enOhhd*?|nz%~bD-GG(3j3X-tju__jZ_N0Q5if66FQxIw_{H#voU=y`WK`b*yaw|8aYAp!7=7Bj`~ow9Raq?UzaXUnC<rmO!^uJZBzWN+lhju(NY*jL8AeK>P(@5SBz1hU3Ug6>LRx$Q-26~4s<cA9Fq;tWH-6m=Xgp;{E<r;bZ*O#OkAk(8k0{P)Lj?V`2Y&a6KE+niUA$_5&whe0Wze+)_)xNBU0_hAkmLr3_tu-+YUw0unnCjnqI2msWHh<dm05XhQSH)nM~J_U#{yTvEt4E68CC;gOMgWcPDTJ%g?8EqZQF#`JzrPyC(%$f=99@p{{2JL%5A=9m3$s``XL-#BGPuK_XaW7)7%pSn2)unZjJ36u@Y5&_YW#>}3N{90A{ynL=HzD<bOtzH>?rLEj7Do@5mPLq{iv>c9&zbM#VCi<COX*Co3IDOS()1bN5y%9g~Hvg;mCM=T9e>$>liP8!RMws}@_DJg~PdP*OYLDIr>UO^A<AaeSSZh_FB@KMQ?(8axx4%Z%11x_eoEvk@1SKsf2p$fF9*=AERl-3~E!`1DnG(aj_Ld6_)K+VN$XqN};#z(Exb-siOLJ{o3^1)pUn@eQ7K%$@|UiiQmuE@$a5PF_;lNayOi$OE1PorIP+nSDaQw(*GBN<25zlZZ*>_3LYpzT*4i3dQ^rl>Guv#>&d4@Xq&u>#<N6{-NoUo9-ryGoKQj?yVL!Kop23pB4BYU(q=kuE_YI^LLxJ)|BCA;)6y!+e!`g=ldO@L?IO3<5z#(R57KO+Y%Su22S+Iw&0ZsDwKWxI~darM`m`eR!hO#nX~<V-@TXD#50QS1i5DJ-=kbLC$PR>@00YBOR@+U&+g<o(W-5J!@wdgqD!VLnQRdlIUvD49Xc`AX_3{xIJHckE156L0x#uMVvJr{5q|1NJ$3Ao?Q7>D2>2!7%VOLK94yie0PmuggTiOS4lc|C)LSHvh%=lc6YzqbrNFIiDh=S7q>-p)!7zmpaKM2EwrgT&FpmwI)Q-}2^IyR(pWD}uht{}B?Q-_13s#Nb6jx@aO7(;*p~SwT}q}pu6Ds(EpT-q$uS0tRZ=X2=9G{I<rOGfzIO?_;Cd@T;n?wB8bOwk-Qzj+T%Ym;i`>sw*zLm;o^xWionHTFuamQ-q5La>#CS>{H4ZP!NF%C`{@9YLsJVzhAAukS&xsJQ?9fh>2-xIm!wfVj2)IaUTu@H3DsZ=@RVHX+nvh735p9g3dYh`-vd*w9$3Q!i6Gip-kOA42zy%i5lPu^tUADz))q@8FhFSSu6uYiO=Mpfif}JD{0|^>U05Qdc2}3{dR^@WkYN1ek(&7(G__PF{2DNiAdzUDi^!$n{$499;+%pHY;1BVUq7&=UFQks);rR^;7Bi$e9`-Pz5FQW_l|EBI5UM1wn=#Y=RqjZY(uKSVEwaeDtJIuMK-mO)NRY`r@IKoz^>AXYfwV^;|L$%=juo*#w<ex!b80uNn;NClJ}_orl5H|y#j^2?8iRnfT1pRFXv~j7vTdQQhG1DeON<?RCUGfLm?1%mGm0EOIs~NJd9-YMv#BO9Cu(;>;+dt7_(3Hw;oP-Ec_HGuMO_5ajaB{}!4=x05{9WGFQZ{?N4biM+M)A|PV9@L0O4&-s8Z!h$iGAj=|rS%%%1Oydb<kz7OAS8DlE}tGI8HmxF;NR#E*uV-jLP`=y{QY<2baAVp))6;ha?#)dzy!Tj^_j4SHhXz6fULdTBK=HgV8*M7XLPJWmkGEq9&#*i(G?fY=i%$58_Q?Hr3s%B^Rkd>9Ke7D1j9XW@x}wM{~{8<&KUxlz^lf{d){RpntATGxGqW-n8DOky7}vnea{7!Rf{AYfEBo|py5B9T5LLE}`HO}_F+>hT;hIlW9dT@X@K2`+dHnNUJQD1@Zk66NyY<$#R)h(lpU@zlgDW9+NXJf#V3*gei1H(hcNAQFeJ{y`rnJ3*^Dji?iF7!(O?qYzqXM!eKYdZ0Q8q>q>{M0UlMh$LVFGq8-HDOIeOYLLtizP6WwtOw6$3CTJJc>9vU&!~cwsE`UT1V7GpWh5$JZR8>r{v=Rv9ovz6A@>ojVaPN9YWlxli4gBT!-YKrE=E>%B^IAa1T_SxCCywS@-}tm?vsl`n4l8h*Gvg$+nInc>_kI~j)MzQRKikGrF$8Be@1PkQuIKJzm?qf@zKmd2N@9oxD%|sM(oOybEbY84WN)CSD*DE=M8004HGK)*2f};`5CBZGjr;^SY0E)oA1T>#NNvHbr;-VOrZW$Kqj0%!So_nqStMgUejg@V1Ld<MXux9v(AaeEun=pRV1q?_88GQ5*QV?0UmG>?s|#QZRM8Md2u8~$=hUKa*TEJw*+`0BpsecCj{*%jbF-bkA#giuU*JFce)iM9}tc}RGnyhF6zXj8R$dAgrATJs%s~$GU6B_X;e}9A%CCNAWn;C=}}qC7&piEnaF%S-ewvfUR`Hc>q<nLdj;ogM|N2^>9ot0>>fgfqL=#S^q1ZZtbNkCf%s08O=1e&Hx{e}C22=Bo5g!68=(@0whoO+YR+}yNzx?RK!;K>hnWr^UPYAcKP0hNy0Gv<6iV5k<a0D2w;*uIHMWu4Nvp*=L0u5TMKTWw_3H@1nEVAnLJRdR<zsTyu*4dllsCunnaRKf{JL09O|LcL#{s5qnh=p$zRWWcx|221zj$R;4e54H60hN69>raI|Mej3;+m3wuZjca`<a}IpDC>)8`285=ur5WU}aEdEu6`}G7&@tg<kazs(i}SY0*WBctW4~ltR-{ucTqjdYn84sY6;Lh(jsCVp1D~^$-vZVaG!+6`#dX0JPd>cppr~#2qBc*?Vk@3UPl%>ep0@q;3E;4iyAX!j~)T(H86f^Pbk0dNG{f!Eu_*Rp@PfD$Bmk3QwR*!6%f_9&W}K#(S3&+nSZ#gNjn=l3Sk~<bcUt#JT}ga!W!XH&j^d_xRL$5#=d*q(Vtn+}Aj?FJewyF9V|{5i_oH!qYWsDf!4nYBF?)+%HeSH-wt-xZ_ZyU#lv=_D*omjr@)KG7Bh2b%!Mu<ujHx&BxrdhP-2j63Df!$U}5M?8vXCO0Jk5Kkp_Jxdnm}X1aAoaDg#4%l(G{zg8naS(S3mg-uF1-_(Vbg%QIR<)kXh%iyx^!0ibzg891vjqH|FVri3YvZLoS+Ja!ddc!*><!m1V-Wm!yfc6A!Kb7E;#i@_3x;##4r5Npx9-vDnWOIgF^~m4yozv)EiLE>;^@&)03!~3O+d(yNtGhpfGyGT-%V#0Efk5j<s(9*hP}BT}B2401F;A@bP7KTH3+fx^^k;OmNz&N{j$+$dnP(|Wo3Mtj>4dmNa)We-7bP>w_9EDqU$&9&heB(?7&;<&N&MBy&?u>bKI!RkkAo5yrVz9y3cLL)G-KrJ`!)ZO(ebAlS4N*u8ajq5t3hGSc3Euy#b-*ifEuMHW!f@qLyB!_F?}r}6Olx6(!iNEiF)hik8d<YC^v!3Oy?kHRzSw@h?(!Q(>4_xl9i%pD?Fz%(i;U@4KK3-(ywOKba9>*P@D0O_$@&awdbDd%+04t1X{&z*?OG6yx7YdMSpBQc&kEXF5s96NKjRAD(g1j4OAC!$#pW~PU<cRfK4MHs>l6t!{%}|#bI2{f$2NdG)2kyNS69@T-oyf${dXSB5rrmG-m>q2>S8#SCMB;zEE)?x9KViSy++UO)b8v&)WzUr?ZGQqEh$NSUkxQAe^fAaSy#8N>ugRnCI>id#zU8&Wr~b!0tTKJsqYuL#+g9Ec_$)1*PG!JF`3W$~(5}4}^RM-UTo+UKm-&`|=pQz}eyP+mVMjt4byT#W#+Ml!j=u6VcIJoSF@6b4q1h@7est`t)rr@#q{dNLzSnwp05Eqcolqld{TLU`$El7bZX+VoX&#p8uMT5XJeg=<1$3#Pr4DnGO89_|;pxq*7h}MaE)4Fv4;m<m7`rEx+|#O3f3#dV(Y{+MnS$h)qm=Y5gE9=o17X8~+Hk>O_2)M&P*uX>W?a(0;~>MozeuZCoM=*$a#g$l*_K>J?)JZFz_SKteprYg>IrwFX~LMZ@=;EHZ$3!fdDFy(U`a0*E!npijq{`a#1SxNXpB<Bh!Q<CT)2mU#%si%>WU=rlD_rKKmdnMZ5drp>vWa7bQtj>hU|B%sZJFyR`!%?DME+2o6N&VtTHS1AkDi(0LGa<;PGEvH3Ptn5OQ=h>9RFY3T)s*@Zh)?7z*y`QkK7AmwFF5t-wUaks>m*y!8o&@VmP`W=QTw)RU;C}N*Pao0K!{epa0j?gk)B^}YMVf%HX;{pO6i9YIXHAZ*DhxR@b|Ye>?5Kh{NMm1b%*8nk^1Vr;xtPjAV?Fkd;nbS*SZY``$f|fliFyqgMa@#Pw}#~o*189I+yqK=IQ0N_Hj%F!&Y;r)l-<Xw`r795)xeS9$Df(i_$UaaIBa7?K?!~C2~`UnpvfojVqBmnl3bI7ReDB{iJp=11ll5Ehm2HlQ{ar-RcUPxm!-A{i4s9f^J$x?3qT?_xtNDw=<3P|EI=TjE!nD685k=iC4YcAj1_l$s;w;#Mf_AP33Fni`(XXy#j=!!3%r-A+s;_JF+xBN3?YeBq0tczS+`wVOvMKf`_9yeWYnaj1>*1nzsYdOvG<pft|qi21xbY-D{7udAQs?~kzV5Lr4N}oYKouf`&LooZ(4#gxBaZuFw1U6#+tTTAqN;}cn437sKFfLZ|zjw{|<@g%e7Z51c@q~sBmK@me+7jrf40+Lb=wvJQk)H7HyK~iEsIFD4SOP%vyIQiqfN!O6H|$nC&L)k`V8vE0z#kqZmmoWE*)gJXYe(1Fozo!MV=jH|bg-%E=D!P@O&Gm0x<q9{s!2M4F2CG(g{6D4HNwo>D8teji*t&o2$ifAw#y@3h{P2L$pk@C@U94JdH+Rby2xQ{U6t0B-a!k@-nj3Ta@%TQNb3N<ABfzy6#vlI||VxT?HU-8r#bA?9MOZ6E1#mtqi+JS$~4EF59K<Aj+e*spK4gPgsq$_A&ccW!k&7QlwACC;Y0q#_?>M|5T_w=){c?|)L4)>qpjATd<V!A>xDgTCoXM@Pmc4al%{l`-(BX{-$JQyyVH#?k7|AmH!VD;KL)+5XvFyZ<Rvw^Uu8Jz%Nx84x)f)`B^BMtLJ_Af~kvx;-P{CPEtQOzoUyjmXX0#h%ac)8f1QS9Nb3C#)nA8C+D4v}md$uZXo=H0qNOI$LjlG+1TRDfNx_RRZN_1gH!33<6*Z5N5>pEzVkzX4fZ`TNDcrxU2C#GCon*lZDo>WmIBc40}^oP_rovs@q}`#R{1wT<T?+%p{g&L3u(=Y*+{CGdd@JTjuzpaC^2~K-u2$n{4i7bUUW{?)({TcS!QtjoHUUtL8XO-Fkg;ng$#tyALg@Z9TOVrBsofDlFz@q&d5UQJXF03dB7aed-I7b1+~+757h~K5*avFTelr<9C1i_H})Gw4T$J_ZPlyWSz9Utbh}!asWYI+EN<g*|B#RcxhfN5K*9WfERXB{0+sV13-c*{w>QrPz!eHi<R(_i1vxYI}{U}saBh$k^`)4+HRYCC>{Vxv{;f7iUs%gfRoKt=7D@k8&7VZbU5FUeow?zu_?Jsx!z3(Fu*I4lYwO^&ahqZNrfbibwU4bna5n-lM?O29^0X4O<szc&ky;ptc^Hrh9&^gkxp4G2c^%0F%*O@YfbBgt%UJ^Q<}8or^0QHu}Eok4T*Zm^&<@bB`A>vjyGFq-a8xy@~92_GmR@Ry<|n8i%(VOkuU#!w!s0U;eb%Q%?^ds;FY9()Y&QWGTZsd0&C<A?d(>*YoD$k2~HT8rTEzInw1B%fO9i;^K^St?LFaC`^DiGomEMn$hWC4i${R?+PFC>XtfRH0dtyqeEY@yhvA>9tI9u4luTb~F2t6!8$TRkx=EFY*Myg;=$+i%VjC-W<s!}>R)>^shfKjEDr+Q(p%-9UVyBo}p}HS8uWTSkbmNI6#y$v$$jAFRix`A-#xySiysY8S0*D1W>NgUw$c&CSxkZ@)q8eh9!RBf2oT1Sy72GK1(zriVZ)ow(O6K&!g?{2Rg-s64g1jW~J7m9-yJX;33(cjRz$@zmAJx#qDY^L76Tp(^U^{GJ=8^4l5kp{}q}xxJo64=9(lVW$n!8bfCUv(!DXMppRIZdLbu`ui=rlJRdLWS3r)S<LPK{%5JM{<)FaWmxi@%V`9)7{|OmhzjHRr;XYLLfe_BxB=#a-scX+MAhh#<dxZ}EI#N%B-2O*5lN`wXmRm|dw}?&90RdY8-iZ(zZhZhYLJTEnaV|FZT0VcWhF;nQ5Egzj)skixrvg79o7VTR{#%JVh=gceq1lZAxddRv$Wi4g{Gy=Llo{r~aS`j{7e|7BFQAE}$}HHOR|bb)aKz!l$N2&%I3f5MGaw;z5FEW1Yb3x?Y|U+Cl%>(?3e(Zb>V<9~el>;LaR{rCU;U;g>aWd8M==IduPeP0c6PVB=osOFcin|{c)*BT-!9azy|3}d3z4edN`wpR<Q-UczreaXE!^ACpnjJHpot2>XQrtYVPvcw$*%k-B+TqEPqS~i!V&)4w{7kF_$Qrehju64Q!#wrwO-!&+H{Pgp8cgX$I&p-V1>Fq}S>-GA}J8twgnI>3l)@#<)Bneam){ky6r}uq?Zs%*X^%m1Gf6YfB(sIs6GVwZ@PF9MG9&WL0n$`I1Mu--^*LyE<BGx;H^ozlM{yi?@0RuVS`{iFlR)`T6JC1u7===8j*$kyv=xw+oJowCB*#b%JoN0&S$R?+Nbd(@NA<K#&oTy$5j(Jvj&d!K1XscIpxwlpHD$xYX{R?Xlwn93PU16frg~g7S=%gc+#%R+)r|Y!6mIH0nn_&MGkQ(8~h``<8c3QC8KDKr8_JE4PwEN`x#r@`Y!RB|cc>A!KyrW8~F<aPy_ie;f@r+^}YG0$PMrpvnopSehh$270x9WnJ&hGL33zc%!QNM%l{g@7B{cU@~{!ULAPTk(lPixh5p271rpe54cyC(fWF{0TIV!GtIM^z~IRR0C<0iGIFmX=q%fFk6=0Rx}is^UHDuUqXFDoyqF!Cjr?4*94j_wT$1mfybK9{11G*EMOb9GvrQCt7sAt>OS%=sXQF)kW`P0CL6mGxBwXDRMH6u~a>pIb{|@KtB{GRTs0{7IV@GYP1&`fC9E8gui@YSTfCe$jr?vX!2v+TQ8L7NQHAM7kw5Kju2>o);i~lPLTF&K5POlJt*OJ&&{(Ck|<n#uwE2VqwTcJZN8%_3O}SywnnVjb@S#<ZggKBO1`U_aDBY3y<E-fMdeC-%p~lY(>_OW2q+5>bwG4ieIDgCDgzo1MNqu;c<&~)&YYkUA&^mE?_hc6{PH|2PMw$fD2hy#q#@rwce&JmE}Lll!Ob(G*j(QASf8+-(0Mh&rRDE}Rz;N!8JA8_^+!E?Gbx3yYG{dc>C(#*kpUgr>S%K(5^m7;FfIcjRg6){W_~<qdaLCS?@j5;B^*<+9h3Z`o>|;5`0MidfnAX?T%wCu(<ZY?4=_%oGVwNsSseq@7kl{H$7EsI+K1J*uH%VrX4v@|Ojyqi-m2P~ftR(tMAtiwNutPx{v!&N)I5B9iC%|T{GRA~+61Dk&*I!sLK?Zfv@*M%S&_kdoSiFGJ&a|y7d@}-VFxTK(tC7BMdr{<`d~>}B^$610NTiPsq2Uay)=dwB3a-D<-6s01X|=6z^-~+1T<t|`9smsDmUCoZgoSoP7s+Wi1xgmnBXE<$2vzo6f4>hTM9U3;hLc?^5GYiDM>j}6neGIMONa$wNRo`X1Jj+dT*OXZ!|(QqfL3g$p|8U?o?rXx6PoHMQUg|w#Fc#D*D@?x(Wq0iAyIXX4gUVvYspnH+8B&U<7*R*b9`}W{{VaKnIGF10gr>V^uiXWgG2C<v+U&Y57^Q3@Apr-vv`HzxrNo7kBX((&d^F3bBrNPLQ7&gN?9~0rIdqE8x6EWGnDIgJy*OU~Gx39Yo7`zI~2Jmsh%Ub!`auw_mrjZR+xXJk`UlP=f%=?s?nh{YwBIap1Y!I^!=Zi`uCi09P0*B2W7oZR-&F$_6~5JgT0}a?eZ{+UOBqpaDs^C+_IR3Kc%u(3*Apb4M}d$t0R3iOA$SjQOlFrF!S^v|f}EDtzsBsiT)LZ35zogKh<>Zc1N=++Flw53DfiH$##<L6)!W8o4PZSTn8CCglIOolL8$VRDo8aSuh;oosOy36~_-iCR=&Nlhj>7#5G(w?2OehP-$Pz4~avF+2pgo}&n)Xi6)5Ps0>*qBX}ByLD47Um2|`4dq3GIveb)=5UedA(+UZE~`qj9=4In>2=ZmYOciolF2ZCShLT!p)@K}IrW90e&-UG+rE{%OGuh|LT+@>Lv4!o_BuH#9fyIobP_9k9a*2~cA=81so;;`&=-7!b)-WD#wt_wB1E0>7r<D@S_wfkxLAvfX8yg1GA=j=N?ie_4&}#aa4aPwiVF2RSL0m<VvGjOhsPwk7=Hy5KJG&bK-hkf6M<lWOiV2d&Fu2g<{ox#?=u)K@(j=?auGtC-Grls)Tc6&$0qYAnRhrZZBZqU8CYP9Hzj3@7ld5t73xrCrp6}Q2-7ag^-)7gTXS!i9(c0gH_<PEmjrYp5soHVhx>H%q&uJaZDztsp&n}xMi-#`I&pS&3ZJc^_0qO4!KzeUOz{!E&uOS^LgY_}R*nGxB*n+tskpuke`K0atzU3b1nr0~51S+uzh{pXk#DvgKv_v@J48_{Fft`iu4zz22Z(S^*5S`$(2b5S$w@qZ+)hMpltw5E>*!^IBJH<C*l{Emm}H%dG9NMMQc1dff{T+{x^LEFqf-N@Vu3xW)&q?cm{jIe;fEF?2hg_NLLp9JaW5u|;MlY1S@YQCi!kW7%3g>vrzLsoTW{mCZ9#<;+rgPZDb}uv)L;fVM6O{Wpg`JHLvTgmJv;;VGNM?7M>vl8nu|e|*9NX0t!XuR9lt0vn%1PseX$P7;EE5K;U0l8H~d-Uh3NcEmcyarzh=uy+d}(+Rj1?%-4h;<+Mk}Yd1*_{_;gK|nuad4y1;rQ&VDNulc`-Tgekye?4b&+(lVrJzQ0O8=stl~R-NRHS?!tQt?PB+x_Ay<IEUI371Sz(Tbb?e63?}lLED6?7q8f16%i?uqcP$%sCDh+o#LrYngdGQdC?w?QMQMjsfwqTpRXjfV45oBTLQ)bK^%B$+U-fDA}iCZT2_#JOSGW|6+<EINZz3(vM+l=*dbu?T*B!{+SwfGP<cv8aGZdJ%(x@wl~Qe~PzNEllsqOH=SAzmc0xF`E#yUL6E9w%79NtYR7@2?CPvl;Mh25JK88VyhbV8((;INc-K%B>o(lkSq`S@sJ^gYfHOTjs#eo2}C=1gP@}0a9qY6kyC=tQRG#XZ3x?*EDh59Ms*d-+Gsj?gQu~QMpueeJ>#&P^8zSJC%lB1qsA~=?z_7u`BmgjpcjTp^|DTdU_(hWkV$hQGD0R<Q?$`Lu~61)vRBTpcW4JR+;Um|v}^+z6eT)-AZZ7uDb%gqDJ+lBQQ2L7T#C&!QMWE$T(oW4$xJai~f$wWv51mhb5Yow(g6#wuC28J<yu$_s4y+6Q7=oX?FR@}fc;C1+3dZ7`c*N8+B9wE!KD2h&G9r99BfNhqSKG4R`FvI8yK^UnlBY~26MD0vL!Me#^p#dY;YtZ<DcxhnFbpd>LX)6KCY;_Q`N#6uIwJMVqJJPyaGZA^|`n-LHFUXtzrkcFYMW9_F_)=q~P&>)BQuk5^J3XGgCVBtpxKE(Gij!Qkh6Z9oV<pD-Bq6%Xe98!Y;RNzFgHbGXmIac!a{On*a(9uM%UR<>hVPGvK5jh7><axBfKZ&3xr~7z%MZDau6<$%+&wq)?V2trcQFLK2(`;!jwZ4WHj<`iglnb1$qkRe`50>aXz=c9j-fE1@oc*rDxszOi^5Q+3OT5!(Iev4L0vP;&6iZ&M5cg2B?;FNEqOEmJfN_GhDm29-K9c!CDV(Ni6OFZZ9k=o7GZQYO%>Ng9u08_Wu*m#c6Dtl^IB+Tk)=W10)K0~ZKso`I6)ZHjA&?1ymlkyH*{@f$v$Teqa3>4bG|kTYX@0ZGoM@5l|y7v`EvM?77SHkal?N(_;7vZP#%Uc!qAB%rX6a|cUhH~=vqd_z<E^#VHIoIHCAbAvIxap*6yNOAIbl~cbLg3kQ$zMJb&QVSJ$YfiO!6Mo7z&7crn{&*eDdqB1etXEw~O?*U7~qy3i{vGl~w7zo@$8CB2p<WlUk^h6)+b)0t{jnWZOXwd?pD1<T^E{3$_v5g>O{O*D@xdtmAoWt4gR;|tF0|Hk1Wo6MwURm=oOH&<3{e&Z=DCJ9%Jd)|h-s2~MM3$q@CoU@c^Xt9L}z0Bc*33)(+g*ldTlCl`Xaj;FLJ|Q;SAV{l0H-lu@I*n2^bN&1AW0FweVF(x)QkN&B9?1lQW3f!D$J&MK5%#?devs5P&CQ_J01-u_D>QAKy{sf$R~u#seS(RMdJ9L1)fDwS;7^3_#`gIlI1BC)Z<deMH_-X11{%aFEbL#$vwVPIh6VW%0mu_gs%3L`g@lb}wrGnbyhCWYXm?_0RD-2)7X)yHb`9#e8d}+anQS)!Y<Y&)wdA2YVaXXai5k>E$Rrd>Et+(k)?7H&AWPNRbi*K%?P;%3!t`c`DUNH0QT42W`i3#l=p-?qiXNp&E+0$4S2DWHy0f?oJ695#_;U#&ciP_+x039JMb7SvNJ0WqV2OU9MB0tK(@l&G^dE%{lximk#uyT*|A71sncIS9XG`IN(Vt$8yeM3RF7R@LrkI+V*?UmYY<KV2$q8rH!$aLMIE9$y+KqZ32C*0`>k|{z`{1I9`#*H!nK(^PZ3HA~Z-Q-hT6d#KL~VQG$z%4pt`gEjg7%7dB63s*OapizJna`80|p%LKGt^t3Z)az+WZ_EJ0)luB%bv$@?-d>M({+)KEyIEWyR9Q-SvGUvJpYbe!8SPawZQ)+@)Ordb~YKh?6kN4^>KpEE*xKo!XR*GmTzKfTwS6F2tR>T9e<c>E1dbyNBhgsNPrM_S2d5a>6{;qLu><U_{^$J7pmS!vDhJ(n)%~$#U|>+Kld=6vY7NWIPoN5~&ng(@Wm6bzD<r#7F5MOq!9%w7M6d^pHkzd@i7dhZbu+CLXH$NnI+?Ac@P&xFcabFFSqn<y?Ps%GjfUc!U{QgP9w(+MjV>!HC)F3a{ndo^E#@WrgUYL+>~jdYwD9sS5j`d~Hgmy%Gjvwv_SQ=fRj&5qbD17-p9HD9JhlJVc{Rj%0J%gI?)gD`ei&IQ)*S>k^FW5}<LqlcLcQCjm$rRqNoV2m)cfT@r~3(tjgP>CbaUOx>m;-Q0qm5xG+R3vsDfM7>jM?c<+V;6*5O;Ou9d(j$agQM79vUzB$YUTdkEWcS5BFjCb8i!i2;=<qsqxXyhf<-^LWl+-&|<WRY?s(ovs<|z%@fk|XqNO|}O@R^vm>evgRO%?JUbg6-*?i17RTC=;yt9N`Yfsqei%;Vo)$1jLdGn7P!<AA8d6}KG%t2|XS>C$cRIn9j0u!YwS<|9bw1Mda&fb?8mf&w1P688XinJDB2XO}0nb^l!Umxw~@piHV=Q)<80PpcZc?=N!W#5~T+yS(ZA6Ym)Gg)Rx(3oZc>$Ou!qb+)l=f5F9p2PMKb6pLUw-K;YgJ4#+;++X^Ng%*7cQW;2f&(@KJP24dSTo01jM7e&Xb9BGH&^tjXeo4fMoMBqcKv>Kx%-6H4XW6DPWn2M@u2Uq9f8{i2=`V9dH<LHa<f9;y{<73mwJ_qmt#dIYL3zmvx6<c`i*)WhL&=pKk0wxgj2Ye5IGRRf;IZ}_{6tY`Cmvx9k<~s6I65Zi2Wwruj;yPeM$nuf{^)4&gK&K{y^h`Jhzz0Izoe2;@kEAgB7%a8#ooNQVE=Ux8Bi}pb(><j7nl+d_@Y`M9m6AiGgVe>0kg3;Kv0qvdoHr4+HFfdCy)}@(6>Y(b~Kiw%~UA)r}AZnNVCpxk!gr2(RgZGN)T#|OH!I)6<_G`U=6dth3mXQZBr)|5{UEc*9qS*k@d&*3VqwAoKu%O8b*;R^^kN>St!mBMxkh$An_aU2<yZ}`&eftg7pYx$x1ZjSV-#-hg$tprYCe$+JX8#H9{nI<68HHd<+;qzT0TADA1OutdjGWeUh6#BM@bziB3!{;>Gct+hsnR*!(Or9RU-A3j#CZokKMNOTWYz)dio@bYO1JsHFLWZT_;0Ki{MDH6hV=m&!wIHAIQwfD<h7K`6|yPM|{cGpjF>B(GS*>A3c1t061PM<FX+Ckrt`q@?vuBGlRd-Q|^^+d~;tf5T~|dr|u39)835ORf9;bv1icR*kkAQc90pp_VRDQ+1s4I)_oV2rbmPUHuowXRF(j)HjI)FfWTupa~#OXG3L=T;JxBluX<saII0~UwTgRu)7n<ND3uDDsi1CMyxY5ZPU?HH(cA(qKGgw_8}sr%lmy3236CaM=@?&j6+?6r#Wor502@S5_H1{l$jKR^}qY|^%s5*h4)}fQ}cblRAm0R{2zdHfzxV9VpPiXeYAx>h7%RQ$X?Yjju}d%Z-?r}2I0fd%H0K26-d89C1_i19B#yO;v#74M7ltv5$%9-+t5bOl3XL)m&J&;ZPCRrWayFntGH$<Fa8-94fn%%PPYGE;r&6r`ygxm6&3zEO`P4el0x9{M-<fn&bW6g<5h^n0o7Eglv_120TxG#tLXb-$&cAG)z}ZQiY#|n<0U^Vi&4;FRYGF^kefJP;S}^{q4KbqfHK@xC$Lm8B>f~LQ|CzrGNX{l2Ck#^etAo1#+(Z4^~vb_Ff)KH#vU#%)O}LN$4f4agKk48f2#}mBy&1osAIxVaIETb#uNjut$FOnNoUc?nOYzVo@5DzF!eYqjD`dCp5$7X4(=(+VD`i=GASKo=`s`peDFDc!aJwaC1L!u(v$~ff?0vVHK|LGB`2cJ$Ux^Iq)HX)5^Tp|y{nk_k0MrOA;StFP}C9GCgcHNdkpy&o^|$d#%*r_cI>cfjmZ$c&^R0nF;VeDGElNO?RiSp6egB!?#v#jn}UZ`@v#cg2ZUeDc(~|ZHE%Qog;f3_N&6kgw@zi2Ytz9jTjdl|y#lc}gFdm%^(Yh~l%jjs6ceZa?T^CyGfZoiq7eUR*hnD+!MZWS*nZ4_BmQ5g=8#)}#A-wyk&{7KlvYmd(R$t&p2!5iV%&>iKt`q~r&;l4I4j1frd<`*VfOiqDKEIM=>-NxY*S3@fTLuRk0QveAL)}H5a+zqQXv~*(Q(cyL-vVjln|*91qoDNVLp*3BS>W^YHXub0^E7tqoOXc11u{_#uFv*9{S}Ne}uh;a#HBTdX_|s$jW=i4z>`P&}1^A09{Rn(Td>6^w;r+@GQA%taBfR91ugYAwk@8rWtq|cxm(b_^1G#)Bk0d$t66hH`5X&A#wObDodgxCA8sVhon#4q#l0A7zQj42C}F6`v7y@>$HZ1fD3(FsmhVP*AQ9Kc?XtJ7M_$!dc3D1ayxv`42*fIzmq@;K(p&Wl?@$Gm~LOEFv}`}dSb$7GcXcL#I?4E7W0%j!DCruZTBE)aTTvyq5Z4+3J#aBOAYsXqTCH7HM3*wosr?vRCHh!JHyE+sQ8e1v=rBxhEgU25XaG3=%e>8Rna6hvt*ASocXX#QI>9$Z>zd5<R@_3qj{S_|2%{#uD?HlH4T^Oq2_cGUij`aPd*A;nuHmTviEyca3ZG9;`%e-){44s2eqr3at!N(<&G@biJP?340=rHVu>-bH59rV8O4HBb#S)Xr7-m7lJW95NOklT0^P(+bFiUl)Puw|IALWX(2Y4?SUVK@8sv~MiRDmDAz{9Cb+$tx$047|%xUxD879P*GoZdwVL>dwrG$gqRTa%0nnBLT@PdiBcM-65s&PUrWR%(1gvRDGFtg?Gaf$HI<WObW4neYMCx?t@yY+feyF-{i>H>0uB+Y@j<5Eq!*0w`!3o$f{9AMF^G$!7Hm;q5=h@nu`um?3H;5#ZARlJp~gz!)(Z`dPifmdZzN`c6Y%4O#$wnL%95uIZvbTea&xLU}MxF6bl)qfC&w;^{bsI?gr?-%HmN0;Yq+TjeRV1|7n)0!2fr6+ycwMyrxQ24Oth+7XCkgO7Uwky(5$b4intUBA3;Xz!`JJxd@+DV2zJ+BGV_0pJ+(0^lH{bgJI`5&4gG_-mR4s30!l}kMlq&eJtorm6x7Vl~rcM-aa?3VBFN(5(V<o28I%)5u6Yvikl)Io_wT^Q-%+Q#cJb1yaxta3ndo+9K$X<e67C;&khe9+XAl5&&42z$LSBcb<zSC-~t1PrPhp7Z*1ehjsB&&}^f)lX&;ka*cn_Ll{Nt*1)q(s-H-CUKR)xD%zRXKhuh6LrmDNmwc{J=IaA9%2%m=`VQ`Ci#0cSbC<e=muUC(l#f#fVu>yB(ot`JPn1w4XuR<4j0wAiQBWNWduVZZo>^92tS&>)CRI*OjPS&xOYh*Tf?}ov@h#bNX*q}D6FF#sts9VPsP0{U_fI(NWNu8xgW?j0Tby4nL3qDrwzQ@20leVo{jcM%Y>i?QmIs8B{A!m=QBo5yT1p(N%@Cm^H?gmhkz-8yeei7vFLKR;6tbZ330bh=XxYy5V`tj7%G$>WgtYSw@@C-W+6j+4hK0z_rr6rkD;sSr@=&THQauk()IiA*T+#AxG&S#Z`0{jt!J(jizc0K#wxMQ;WP$S_*vSC2<x{#yE@>zX^(X>=WO^Svjxhu!sdp<FjXL2w?h)(B})G5t~b&!^&gjEuHiG$S|2s`4XV!l<cN_`^`o9)sUu+UNG(!GGkc4L-7-m&Z9?Pa2@PII83pg8E){lpj{DeD)G(UdPM{nTf*cGCcA9I_^xGI!=}-byMGFot6%|UL`0Yc7F)GRl+((?k#vv=krWssE_aaxNqst_*HX>;Lf{YV5A43iqr>z3)^Oe&w)DrP)0_|cI;5&XVkE5z$&8~tNCSwr|%sVOFY<3iHVv9$o;C;;eT2KehLmb~Q<u_(7B|Hv8;cd>OG8dkda7jhr%q&rqmbg#t04ThxIi7J@(qInHTAnu)@=lDw6|87{QaC|JQqx__T3aL7`t^cXXVi$NBEnaq7YMpzQe*A?EYKMtlWWuG22TU5y9(I2IdXe;3Rx-r?A*9eF6pAiB<SLvdf=pNNMs>3WowZ_?n*{43w6@fw0hWsvY6RXV;i2J;Ul*m5tol0C^nZs)9UzVpUc#Fv237qP!k5#3IQI7c2mqo5;bn!!YtvBi8A!4a1GqvgNyMM0$KZ{JX#j7!D^uOLw-$tVz*S>6uJul00KV$?hCA3qhLAqMxJ$X<j}35oxsxyJN}Rx#RLLnl9b3NZ*)K~N-+4aNLTDA;wWsKWg^X8LPrMdGt*-Zyz<%*eC`!{sH$sbdgFkDLl$42%%Ix`i-2+l?n#E!lzs!7ijvKMaKq(g@IPBx{np_b{v9<oou}M=Ls$u*&z0a#d)O&h=~=g)@H&r`=2&$MuZ3ENyJR|6>P@$8K~|Vl_HqTpy_`7Sv|Q@0rJ$NyLuq&&L-I~qnuJyP=?rkVJ$nMCS1+_ZETQbOOc7!=#|%tzt0?TDSh|#lTURB2lVRE1i7rH|sHupZP6L2tJL@HVQ@!1nA#(>o8(zO<2vY2*GR!hfv@G<hu=0zSM#JKAQu8~o8pR7IAJIwfKPIP8!o!TNOFz397{0Du<qDD2_7?a1ypz}KZaa}MGouil)cuK*J*$;;2B%sLXT0$EHA08Zp*MH@VjW8p7_r|+c8H33IB@fHiq$%yRxe9og0h6p<2HO96vfuD5QL&5WJOb?%L>oGdgJPKZ8ZI{Ch}t;w86{5zzl@cunIO*qAgVEF7jc&EYYv8pLZ9<2s0(?k3|Sf6mSLvszevHv5<RWFNqDi7~zbStHc@{<7L+SRs?aG^^}<|R+#mS{iV$q?l*N9c-|nWa5R~^o-5lT@J2k_hsgHbT=ebXs!mrugA10#!>NOi%}l4sF;ln%laHzFMjqFd=%bG!PVn*RGlLFvf;^wzk*-#Xh8`SHc9+%G*Qd~{KtO;rQi2^TRb<C|9i#B>GQ}L~?@;tQKv>q{jfq!a`^z>)ud1m~#nW_qn39(a4?TDGjaf2*8XBRv6N*CHI%*0fK51q@N4_(i*a6%s(e|5GcAjMW+$X$FU<vy^P0<S|xgxAcGuW*6k+v6I638zh#{Y-`Ko6&s&qg6RRpahOOrzk9$T%Xpc+-R_FJL9QZ6(6`Uq7uAUJ29>p#f0*l(bzfyH{3tr$~_4o%}uCA8k>TOHvv={g}(PWoK2ES72p&N@3dA4yxY~inoaE$wkJ>`-SSN?hKhZ$`!>-e2}sR>@o9e)><~<WgGLPj+yGul7ugCTgz{Ob33aw&I!j~*8rqrcKQ#Eh3=FjXB2@dIk9BFmC9J?LDh&DA*hRn(Seej(qUoj8oehr@33HTp3KD`<Z?>ap=(w9&2?c5O*oWacJT@sIqEuDJeM9VrtSqsDZmxLeELeWXDUf7=SSx*n*1Oq0@W5ByiS3D4Z2Z`RXRgD2&4y|0b!;ZK2M5OQG4ZGotRlAdV!B!0<UHi;B-H~+qD{?3I(fp5X}g<K{0`)s`zn5C{Y!?GC3>f8UQy*Mw}ksq)wH;RFM*queS`L(M;{oyv?PRbI|A*0++maKX*vaJ8@s|)Mfh*b*t!AVBH<IL9E=<1#%L4RnhYlIWrV~${YKAiHAyKXEqyUa`A=0>tge_XCZ2Z08OLDMS)np8R*pT^c|@a8T&~V|Do`UZHyK`IOSU*h#@z_Ht6WRD#CJ6amM+UAa2t-zZzHiO_ta*dbr5E`-eBxpO!27wB8?DmvJ0af;@GY#J;yBz|EeO#zETJZRk@|S<y+;m~jEFe+FVM)CGtK6yLmGEyr&k;iHLbV2u&VxL?rjnbn1RTyE-RvGpxYXNasfsa{x-k{U&M9Yj?e=R`^(00lHfqbO0Wg|tP<R|vxgiv8f70$!UO)|Ljp9qgs6k)(#2@~hMMc2jN#3Y_0SoQX8a1m(W#LnWQ+^$K6--RqbebdBFXxkvJg_>03Y(srkmBYT|F{zNT{d9apc+~yk=oI(HLyI)^_ar_PY#r=ojpGx=A^k<4T_U(IbbDb1UV@CTSP=$v#PuW(O81(F=xqz?IZc|(m?X^`c4_z2hNjI(9Pg8SIvtld-#Mb?8clR%NjcK{0FX03AW?}aU6-p!T9~u?yM3P!e5+7om@1IL=`2knl`}4Oq>^gJm*iIo2u7(0k%WY*L8cM8z7tLKl0zE0mJNEPIPoF-&njbzik(v)h4c8xEe<t@=;I5iGa9#e)8&2IgSqnEo?8@(e^L`7fT`uCe<%X8v?Ll8DrL2j?-$>dt2eY1hhW}0O%^-uN_9<~A)6yd>SB9nj7*65Eq;Na_vDZD<!tB1}*0Zz@iT&ZQe!zV7Kl}1efuBNL`F)c5&AN}HvA@8M5b;#-B>z!vp44j3^{QER$;i*7^xPjL#~0(Czo?$@ThQ_4&$nOya?=Nq^YbLN-WIm$hoszl8$Fl;=B%oSH~m~!SDv9k8LX)pE^*<>E`v9E0_0(;R+rH0Sr`S=3wJdA$4@_hcNfe5^z#oteR?z9*IS6VZ@Vxws_1LZSz-al-HN^rG$AJ*%p~;X|ML3}KYsVOFK7Pq?<PQc49;8|_SZHWDUP}|wqCv29(R=e)3{3x*UWZ>1ezh#DBQfVubUI4{qEngi&T6^z84DRemg)W0!Om3yLT->OU(`bbyN$ijy?QQYHDJ*&5n+{#fK-GitaRpG`d|~05Xe--^dV6Hpe&8v6nR$BHe!?%*=&9*O83zaY5!q<oux~gzfqS{;q7T<D{$1R1`JHiNtL<v?uU0J)rgT7L~Rx=GwWFgL~K9pX1;DdcFSgSd8hC^UCz}f0iyFxJy%`GL?k}Gr2aZO_4n&ZBT%NW|R4@x&`>;uC7B#)X3Mu(zU%&o2jn@j`z$j<Y=V%wdjw;LY1B?_d>6=X*lVu-Vee1nT*BZl%x&1@um@0UJ^DiT1ViX8h9aYXRD383-7J4DZRt@dapUXFL-D(8i%>8dF6?gX3~4|dMCr)A85=ffBfjPt%KBi)AOFGZpB35rFh)%rc^x^RaWisqCFk-f&#(A-4=0fDi)FLq_cLeR2^8&wq`YJschi$JGnsDb_u#~CF{&4N28gI>}#A@rnJgWL81W|I=r*YQ3TL$Xk-5A0oy(53l}8;z~{mqJ(=#Q%{-|=D3Hjz#tOlVLb8rvt_UzeB*cR{A6-UI)V$QM3gd`TwA<gLLY`OBJ+xdWS&TAj{@N5GyLHVq7)9J$9s|Gj+X}TAJm0Q#jpSgn2$}^YuHQM9!8)1>Si=jy*@JoXvcgzE6C=HC+}FtLX}1k)fR6iJR)L3~=Eno&)Brqlx*vhTzi_0D0ux(wwd9h{jB-z%7(vCeL+5|WBbTfOijBvsdG^g_RtJaP4y!JFbfn+U8Z48?mCa2kS}Qe}&^vZ!>X?}k`_E&0xu|&o$C;uuA^MLfA~b8>UZMv|Rh)xWw$>k~-EVc<Z7;I=JLOUtY%BC>#T3ll06Gyxc0>3YHAg`nG_%(Ii5{E0%rQ+HUq>`VunsRTM);YvRp4$_7;2;<poe^*AOuo{@1u2OUD}JT%g#k<{H~p4W{H(N@b#PXFo51ughouFEiUp2=ST=)!2^|f46(N%{T|_+_)-?aL|(&!?!zXcZitD-vd+e!!pLDu*QNkGzilEN94>dMV;A6e054}9RCfj%usDSqhzH~#FEMgV=(kOjDrcXsub^L+bu<@!?+1CA3GSg3S2=(}+l-0M2+u1xZJRKW0^|4cn?0tvD^hovd{&&+R@hl>tfgvQUKB;L@J)-RHHzK#W)>2vVB9Rh41#}}BZ;%(Z5zExp@4?m5rH#+!pv^5l5JC$vG#m<5|pF|PF~rzmAwE`{0F)XTz^ZnHS$-r3x-FPBT-wU(sTD}+<|HKvT3p=LN$5_e&eAw)D}H0rbjU@)^=+h;HbAk;i8FD9MqGeo>^Lbjxk4vFVMDvcKD6x#Z%x^>qh7%H`+o$l(dEC@nKa|#AT}_gtwed*h4vb6<8}a5=|9(Cu`h=vM6{z!|Ee&;;5mMF$I@t7izUIg<aY;#;%x`zHK`}4uh>k_^#7M%hAc(Lhh3sBsaVa4i*BKz-lI0PR?w4*#P8olr&o3EW$pFjJT>%CA>%rjAqmY`z>k^t)dWOb76vYkdr=0*E~VWnAX)R<1Aw4_rdDuoKSVR|AgVpk{<uiI@IvFd894$%zG+$?=OF^S~@R`@0+xqyOc<|Y3<(enA$w?JvXQm@B&uK+eY4<q3o+)#Z`pB(t5ew+?k=Fp2(yJCKzW*yC>+OLA_R?-3XJ=TZcO)ba-g0lSmB&N?~PS0Y*8g`MRi~5p$<OvmN>_f^p9Iae|}-^|h?K05%}uZTE}(;02OVTzERbmDZy65o`oz<7_|wK8vED*#1@cfP>GbecsS7pzpceVmrAgdHr*3zfG_ax?q`s@Rn-mHwb7J<>-a!5cX6PAsIs}1NI2i<(o~M1J-d%nDTgH#(9!qSP5{p7p_?hv#uu>1BZk|U(*TI71%xen5_~<$0n@gD%Ls*-M8py7!m;8`%u4qef<Sfqwv``H58BaK*f7O(H3OoJGb(fXP2Txsauwd#3-$aG9v0aPyr<+#pGbj+{cqoR}u#rX2P5OdijF)0+f~jt%U-ZifW3Y31*14&QxV?rFrjnRdBwEMIBXx$B^nS__G>idL_s=0OLblg&uRH2<dUL<OxLdOF&*B>;ZPp@xt3on@1W8MHs^Jh%~YSN{=yhxE;HE-ACOQ$y#HzJY(JrqEGNUkhh4k!g(2TIL3i6_S?ui)79`{6rg}Q&w$UOs=s&fqIF7RBIglRwR&ZK8kmJBwbq;U@?E107;v-&=#=jrUu}K~*_h2K9A}yCU|%E~xzNVErv`jK42xW_gV;C`Jvd176u(!a*2`+!cXdR;GK8ukiA;5(euBu>k{aTaMNZ9`qWDuM%138YCOWn94CFH&SupP&azdn_ojTpp0H&QgIHA#o&8lMeQ8-+B3LwE|xUn`*&N^w*3G1i_y-`E-q&gs;7t<?M<0?!sjWTnTH{1ZDvyF+>u4D4(r>YLMLgW+;nfxl<i*?+yu8eLjtwhkoiuZZ%UKyYe&iA4VCV)GQaXRI&oyj^d11pqTxaS-aeW_R?eSeUJD)h`*uVS&oq$nI1S#-F42`CkXm|MBPFIz7aJsv8TMxIKicasX4fq2Nocx<8%*p5!uf>vaq#oU`#sejVWLxs(QakCdKI`hRwfyGTUi)4$d)r_eqp*vc=JEYbovg*eZts&ca{<9fO^ODpDA0k#tpef?~pw?dC0K;v`>E%*IGS3K8M$Kg32GU*nU@b!eHfTJmo)bsIA$8q%mk3o1LmSvo6&7xi=R5V>c9&6(%m5|P4ugo^Dn>Bni^aev*^z=Qi5K>DMU{6=Er9)4HryIr<?gc7iDj^BS^gDTAy7bX@560)C(|LyD;zGb>AClK*K{@a_(^VOK5eiLHo7S7ElpcKA(uU&GTb!+3&O_SAo!(<oGy0`3}~#Zm=R?qQ2C!G@&m?Nr3tH}dUWSQA;hkk)#6B15r_!%#E4wiENX!yt?q-pC<O&f^-*mFr%DvA=J7aY3y6i6@@$%lN);UsWWj7U-E;4nv<<zDhRzI_og!K@>f|=Nwv$tBK}{D(9cp!-ak9*<@Otr=xv#EFCyqEvcqU5pU`Rx)eaPcaGEf$X+xTR(n*Cbm6KOu7_g6Zc=sj{hZ*Ul<pgRHBf8MZ$oq(`Buq!H>!=43l+a~M$$Sq`rRg7Ll(!Qm(=o$p9?y45$%bNLJnO>S#x~dc|<0Dd3EfY&*a+vIOwt%Csa_uwhksb=B5M)n|&`oy>PP<OlR7wa~_`2CTDkQlLoh}K*?rupqiY@OtnxR5ZD+$fIr~nwwh$H!Zgx>!>Vc4z<gDBWN*CqK4S+(6EBbl_YZiNo%5$Jz)UDS{RXerZ|loIQLqQHoJ<sGyt039I~&|k(d>TzAV;vY>%&&c(1rq*9%m?jm((Y9<?*gAKVkUBb<Mg`}^Za{PoT%wu1jQUalaa}C!ZS)J~Koe64zgRAbFG0Eet##yGgff$5+YJlEc!?U$gy!^N7Tq?BUIy$Tx~6VS+@lBB#vs`Sx;TVRRsn?N37}&Sv=6f|6{<rFBcM_{PGLjWC%{UIrGiT=bM<NZ=*~*Zh$aAiGGZ%!YK)Ob*Fi2R%Z(aPrZvx~r++yA!==)2p+`nBc3?-LBjU2Yy0|Etw8vr15E4<gi+5U!7}`7#PXj)^*K018E()I`(@o?wVD#s+jf8CT&{rC-uZH{*=#{&nHyB++C%~5{>GPx)djgzNK3Jpb_mUbtYR#lYwRr{=uwt0xd_U{hM2l*DxDsr9sACm9kQJ)b)FE&<W8JXGoH6i`&}yrdwe9H2g4`_S;QIadt4Q<{v5K)#BVHpw77(khVcT&M{CS|nl&Z}<LO|<;Tis~{)HkCh=ZES;?whp>c65No?o_i(uz$7+`fyMTKEYMP)=~BqqXa5CmVL#fWv!0~MmB`c#lwRLMi<etLdU|*MSyXS8L_b4JFuTk!slUmC25@}+1~~JLeMu(mfsSy_^V6FWhA<y(iU!kx870_mNjxB<Vys+oZ&BeVbe`vtK_U6N@I92kF}@iQjvEocH^oV3l#NHNIL6Sn?!|=);7wTeh6x*sQDo$uo=tL#yH!4ZNK~Bd;cz03|!=Hvq)g-<RT4p2=~(=l@0Y)PbiR5mar&l4a}-W5K?H5F5yYj5YwRG$pjw)oPqln-~Iaf3zf=mdVP^!N>!m@TlY~ft3sz)I0iu{4ELf5<&vqt4q5?LIx;?d1_nJRjibhrd0I$mMz9Wc(OY(1eUVL3Ez!3l^^u?T7HC?Trag2PRVUeQdE5<TD(-84XJ;Om<A(f|sLzg8?m`^NVz_j|t$wMf^+PrCOcBi`rz+RYT@6B`Fqtss7+3$<Gd*+msE^IGPs3&kkftavWynz|kt}LkbKD}?BCfeq!!~!r8D-JhM+!eESR~9Fu2}j0hkOxNDPo^9*~>89j00gt6cqf2`Baa$ShqX6aRH_xtm~4fAQe5VL}#_Sm0m7t%jQII8s%JVm<`-P*H2rT#5yy(wO5n1U)SZkM#1)ycu1|sMX<w^$8hsl_F%xBUf#leEuAsIGxA~f?QFfq(#yi}30m<HV!){F&V7Xer<BNBCo$w3M?)Sttz+OaV3HSF5M!CUwv3_M-Mh{QNvwKLgT<2dvb56LLk~QfdnEiQ3FXl43>hv;>du>kB8PAYK^F|aeBD1vToK@SGi=GaWeF-FZe&DSl^iYHiAfv%<&r9kU{sv~o0{FLg5abCQlKQz7lNGjmqtbn7;?)*&?;MY)<)v*)9!5-?s1!P`?Mnz9A^YYMUC@hy#8_kF1H(Q{Vso`_gCez+}EWGP9!gFu$tg|^|m&^zi7>$;-MTqO<ILw$-FgQ7pG6%1q4mo@+A=&&dU5#RVx*AOV9tsU*dIX^r9hBUycM7Bk^$}bfOhwJ!=KVNF!cm7~$(drYeCZgHlc1qk-_Vmu6Cz2I~6nV4o$eS)a59PEU%a>#4^t{o*X^x<GS6`TheC$o^7Q7{x$Gin+bN%z1&DguwqExZNJNrct?~5}u(}>S^7e)*-fP<rDaH$lzi>=T=C7fpygyBdmXYP%a(;Fl5-}aho<Hh~;_^(TVg4rW6h#vImPj)d^fsXn})X(Ne>ZUM%lB-jmoV>$dHg6R;yA<$>C@kmRAN?Yixy;zGP$66;~dqnbMzV(Wd|)Y)C+#(Lm^&ZP`lSAE;*+B*{Giub>RhlpB(3q|#9h>x;THYgGi!l99h1X$oD1Pi|&ZZv8|gfJ*%5Jj@kjkCcVg*J#@=wKacA_^j7oJ7#~K94Vd<JVW~f`5Mf>C@*|$saBHBptu|<{gzk`R)NPlL7RXr4RgK?EFqMb$$yul%x_ctu46|#G;M8{~+sCzhyN9q@X(~Ke-D-KEmDa&IwQkG=d;U<p%^Z?A4y-8}x<b3c&xE&>1=YYS&a9ylw7AH3ZlkarGV-J}l@Edd|>xJ@&OIWLr+l36ZYWS@p??zuI>~k54M$Ec6_tOD+jUf^p9^wNC+egXj?0=a53!>mZlBLKmXG=(X`jZz#yg`rQlqLSlvJcHzY(mU|;AeME5%jIsHsV^?9%k&V@qDDWbkzSmoK!P5r!3qNRHD8sT>IXY$Ecj{T8?~kkppes8FAV#6pA_*=+enG@pp<U#HUIk?Bhv(`uQjKR;9|j{$qI{x&VEvfT*v;rgarx+wIsonlU|5rSD&Squ3J>X}o6WsbzEo?&tIf|VG-JrY;mjK<g%sV=xt0&>z?bJfK8(i6S{d<Kx);`PkrgoP3tpMja~~16YD~Sq3dI>I!U>;5O_kRdY|R#i^o0-&iFtf(tNhdn>;+IY!O?JtL=~zv;Xwfs8SV(dskc!oMNPC9#Zc{vH1ayr{&aH$rTaUzy;K{Kf*Mt-;#hEs%ZlV%oJg{%?|4;81#`<k4C6mEG*znOBm_%Te2S&5MLiF>mQ)ZoG4e0PLa*yGpVBpf@*OOJZG=!*3A!G<t&>@5CS$=Yt%VD?KHd0vyi_Qc#HltRk`7b4{+OFeO_Kx*n>7!}7PcSDB-c5#d3Jqb)PAi1BMK*@^|7nbeMkvo1eL87I%@a9_c_G}lJDY7>tvOxqiYFHf!?DNu`~2Ka(V&;Ttt!bafC`OCJWnU2ljo<O2};2c0$xgCRd1xmd4awl#O|H8_DF1l+TUAgGe{2S}`Phgmtk3y>u*wab*0!Ik;1%A@*Z9_mnL?nJMYiq(aDMO;b~=XaQV^sHhV#!W9x+sJY%xi9*UCWyJB9h{!Emp;M;|pXjCz(LyJcBMFH!d)ijL&)E+5AM^?n!n=%NjBV`ti%Xglsk$i|i<aGwg^&-Z`14z!Gwzro>82R<l+-{W!?nv?iRTw}7_vWKsQj##HRSYwdA7N(llAR+6vofy{Y;Bm#Za(`UV_<<_(v7JT5Cn~<r(l!^HK259HG*IChM5Ncl^IlU3y?7evWkpC)I2Fxs@w1JtvH|+|4!L4VPsdbazU0$~tCVQiOJzj9UlybFUB77lUvFr(``Q?{NX+9fHH+!x{;Ygm6#-x-)4$V|A2a8Ezr_W79ia=N{19;39C0<r$4W`a<p}O6hQEI4rFuwfzW5M!?MGL;&WjFaU+Qvzf}5x(8%Qbz)<{f`61m&GYhd3XjEh1`2H;O(-ft7kFJ2?Z(3Q$Zo<C!O!HDvH=1-7$HMThM;|LYl##A0-b70Lx{?aWQ@$yj#TfaB~#R&rXmG39prflo0m1C0bTCfm8-?~;88^Vxw^tts2}h(|B3)#@;<Gh?naBnO`{9Y$CSa5A7wRe*24A{$v539x)VB&TqyUW$VsuqiWp-63h<t_Lf;3F4*bSRG?fAiwp`eV12e3D8-|T|=kR_BA9FDq<CvAyR|_;)l3u~#5_Tq|tu$+R?G<2$ccO<-0ti?<mn^#Z4YbAX<IX#Gcn*41jc#5;?4eNpLFH!Xp!Ct(sONK3l8^LI7K2>p81=)BMz#NUhGq$0$j_mb-Z)UnhC+QOjcgstz%0>bd@j;86nZespOosC($I|ugA9e*h|E4@tq}w8KBG&CAMoL_R0~iz&(@hH2<}e_?E9gSNv*8^3UtOZkiM&Hz~(T}M|@~1nXMVC@w_v)+(svY6EURyMSI`KT6U}0zLED&)gAVs$)QuML_*pWCwYZ$u}usOJU_KE`|Y+tbEa)p)U5?=3=rHPy?B*_2ExLj5azHq25AtL(l2HN|GN4Yt0TaLS%<c*RNUnB6S-pS{;j)RUMqWU4Q*7h%_(FcWZcFSW*Kf_A&)$Xu^QR7RvF%h<nVAz({*=RS$)o}dO<%Bxy@2X3IlGLqOft>h54NKYlE2&Nbe5qBGaeQOCZwqtFyP>jkL16Dl)c1Au7WX+Pk0+(ei1%D@~jVK7ZH9HxXg>+O6<9YS2`zU)wo!xyzqANU4bYgqXhER&VIKoUlaDgC4LVs~hyL1MGDSF40adTyn<J^oE*Aj-%uZNm#OKlDz)Zw)vy#!!h+hrHnLsZA-fWi(8+~uF-V6#!?rm!aQ90Sr>&kYt%$~M~gi77ss+qU`g0I1&U;5f#2&u^&3OE6jpz4L8p^l&;<QTKa5POs&I|;1e=j$ELeq*b7S^xqFp3EiBu4T=nn`&-1jx_5;hOYviIRQ#v=IRZ|-}w7<$92L;Vw4CeKO<Z`ZW?fX6x>k}@Z_4PQk?UKBpr*E?MJiQ@`|<_VK`crba_a2ps%NK}c56w&q5Z6l8aPf*djA4jV)AB5K)wz(QY5tAF~<|s@5fb&wOhUMofCth+RHUC^Uia~7QISvc|n-<`0?=u`i{Zp9v>{7}G95;>go+;L~hnn1H+?-QyIFY<nrseL~y(()M+9xJGhbN#tc%7^CM8TyRVm*F$)>)lFjOh#!Pn?O)1ZWlw%cb8Cn!c^mi0ZRY!JfYpa=Xd&fVV4n7*EUI`_UK6=DOul_FWsM3cSyx6nNfK2lsPN+%T(oXQu;=N_rt2L>xcAt&3nMG}$*Sb-8CASw=!>W^aM>lGKIYCNy52&~t;Zc+oYclorHVYQxx6l-igqS5RWF_h@4`k;gkayvurH$zg0|(N3gVmG4TyTSKVbU5~(-_tKA@s!bU6gxCW+I6kM~KEtx<?)1;lC}d$1co8{WSFaHs3XzjAfuKPg0Vo(fLJ2s{Wo3@h)6c--`*jgRe=PWdnYxU)2)`DNj>G$y`K_Q1oJU%|70U0>TvnzZhQbxFCE9gB8UQE6!8i*I6cF*%XkEF<pIjxDn6=o>#B`CXEUHKsqMoqYd{c;K3#AnQ3`Dq3^tc2)SqY%HpM`RR?IzczPYIqz05&pT!6lB`lTv7?=qDwp1RzZ)n4S|AuYO<Y!BgNF3KbR3cdruc43d3f1qORQ76I4V8QXB8rDj^3R9wDDP{Nx_AV$u#IW8Z?WGdBI94QHi2vZbCQW$Mr`3m8WMM&A0$HlyGU@AM&KWGS!Xob*V6WxR^xWurUDRc%XP032<c^V5mOjTj9E!#iq8l<5!!-VsmS)E~YU7#UQ@H5#Xp61>NdP)1muagN&!~#zPYSu#2sp(HN%w3}59&CJarCCfNbHe?=Xzmr$sVcZ*62O3`gdE=7R0iE}ScH_@Ag`jmrXn$pPA=|aFpu)R6$HC_$CqQ5*CoLmShp@HAekq{IBlRPHIOF$JF^Zi<v!24^~snHxx*+|h1c?|174zpbkqn9&%zcIg&B6~_GN~$T<UHyc#~>m0fbz+0EIh`dyCO+B2B`I$`s1_$DAYX*^iA{RnU6xF0(ncYIS?~25PNnh)nTriQET%=~CWQWqs>ShI*Ow4H$i|Taf$Y#z4bP3fQo;WSgguZ6U@I+)vQp*Ke6pGGGlig_9Ly?dse{K?cD~074%NO-WOnDqcp_+gc{MXMmi>3D3W%Mp#qJ+B5**dhs*iM>yraDzhv^f_nc5t^QKA^FmWPt4cj@q3{xEt}-r`#@Gtzgo*953gMHFdW{zz<ts%+FQ{Do6s>EM!dQpc=!{teM6v!d9R1STfSS%ZsVVz-SG&!>)vKYX6o(`!7I5T}J$A-I1BMQsg)O9k#51^G_u=-s=9TW*5Lu$QJ*rdM=s;lOWytjPpk`7Dh4Gd=a?up^rN=_o#=QFQa+c$LUOMCQF2Qb0@-t|&yG)#z7E93-`#P{$@3RoZx2!9K-iSnmNEs1tvyuB@4g-54LbLN9!yYP%KmuY>Y@eY<#ba~Pca3?tnI04@sD`0*lz(IMYjVUQu0rJZv4X*Y*A#-yr*X)6V>HnS3IHR`AH%8^SOFO8#dt@(h}L*>{WkNiRttxnOrXTb1#`m2sciFf0rx<ymvS(HSLYfs*UDOlEqDeu|LlmJ!!7s}plIvh#>9KH{bh@|RFwmrQdro~fJ=1Zr{vYfv4Y(p!2Byt%%#5*Ns+NxhW$b51P(Z5nNhiE+6^vnCuri0%@TIMnWFdBo`5Ruv`&|^r>PD71o~QlqaLK1T}fj3Qf-^l4r#<=3m%h<Q>5cDuFMZui_X&-AKS2K-p}iWR|SVmS({$z6)F&?wyPzN2MSkWH}P!0y>--2lzkna!VMeSK}{!d3_<TVo$4(&Gtl@fGG<yHtxGai2!8=Ti}s`7Z8s`V#BLk?qzlAc1v0DHD5UgO_3_R@i4lFVYw15!{kDWm)S}O^kc=Zj0YN^H31!d$i~U-*7okvmlZ66!4hb2)&m2kiXc-InH{czLvRnY^$~+l4F2dNgs-5S$UxlU~YAd_gOgOi@8AX+Jw3~{SWdNfTfEZvteWfZNlQg3+8JoMTDF28M*J%uTlX<br0WZ8ENQiDHW0m%o4rA%@ZotNpazFcO2X^vv0(2txfEp$(($sucugmiGZg&anUvra0_$@_)j<DiTjgF3hG18;Dd!J1ew^|-UJ-X;g%bg!Cpy7)e%NIjZluluy#Z{$B6d&AmPMlY$(=oCEgPb6r@`!0Qt#?0AB2w57z6ofEV<>4yFCOcI(Tzlnk@Nz{g)mnV!gkR!D(lj7DD_PKi_CMVJYejU=$*`*8rSP@pHmF8-J7KJN!m?+3=w4`07%6m6-`%0eztyTA13)VjOuZsX!C7f9W~_*?3OrsNefIvgg%^a37n(W`Bj0%H+rbkY!+ZDQKVK!oe+dDMt(iG3wfx)c&jDFB5vYgd7bk%@=>o)lxPLeMR#2;YPRnqoSMoqaheN{tNQ)(8Y4>=^f({CdB6WJ_ro}Gsl74NVWIn=vgC0JS$(%_zFoqoc2&rU-oJ!bVT<;pwf(|dcR`k}MzJ0?pIDv5w;O3Q7hr~glv&uau(8u)#%Zp~b>6*>=s{Qb{gcbKhD0^s@QYq2O4896PW4d#yv*fnm#zQFR8Y!z|5jBPMc18F@-8dUW@;|^UYd4njA3(c$$0;Q%VB}TbQt*{lo_ln>vf8SkjwipqS~ZLo{Vu>AmT>UaJMrwIG4#`{<h6@1Nr5?4>E<kvKsO(K-)95{|uN&oY8G5kLUCA>rbCPznUN3zk<tr$g5v}eEk_;YRZef@=+FdBknKx)MUDtNK*C{(wqsjsA4aQZws4IuJJQ=gIwnO?MM;h?cL_Oh~=ABE>5%;O6yK%!SU|=V{b!9^s}9QnLLHJ>JRb!?a%qrR{ygv`2<OA`@c&in<BeKf6%yiW?$?E6<;vtRoRn2;gU-2%AD5D@>Z&@D>lQGTd<BD_hF1X^5yS$U;lK|2M?iEW_LPjZTh*ckeX0CV)>_LXjDznTxJJcijNbyh0Nc+-ZF(W82DP9%Vr3R77ibaU1`)i=or)14EHF5(F|cY{+Hi>`0=~Hefi|izdIc};K8%Mwq0`tM@QsPHAAo70*|9^KN0uAk#wicIdd!Bn;}&D+uq`J`?UtQc1?@#fHM^}Q)N18Btx=$1TcuQe*6N94-dahZ7n+Tl;ak#msk~LaZC!0aJ!5EWD+wf5x>O1l)l-G2_cV2CZA{&bDqdLlrcU5$dHKoJ(LG9KaT#cwaam;St*%T?G^7dBku~_rUV5}J@I4I`PW62Cm|&zRs_9c%7)AQ>E|DQ`t;*^J>IQ*YSpX}Yxm-6vXLgVb|0sR8Q?rUgnAtP221Gy+G{iQatGm@JC(SJ(VXl>=lN0;z-y*K=7947K|iK^7WHM<sp)%O$iW+UI54G~n0ElzQ7t;c1_k!7C6aB1=BV5?r8=snE(JHwq8!m}pMCGQ^_oNeHMObtI}N;ClpmnxOE*)S_1vP`qP!qhJY^{(UzjvfEt~^|tpW^ik~N7q;{`F9BFalMFZt=SZ}E%C--bf(kf_~jE|~FtG|4WzKpFi)^{cqyQM0resKu^p|3Qp_W)Z6XN}sEXgiE>Flb6g)>x!6b;V`jY78&8v&`dKWp@H2La)C#1cEpV?%nxxHqv{d5R8@oIbYu@Y<5B<i*X#9{#}l$dWq?*Uq%x1DR@S-K8kqPxhsfiKP<gOhYO^j%onD8hH?wDIV?nDw|MAGIWT?Ln^)--3jlEp-s8ina?V53O+sj2YXX=v0vdi@KVZB`V4z!nA_8#HNP%s`tKAthRmo`t8VLGb}(<$skD7^5OwUawDvGP1tFN}g1CnRbwA>RQk5U|tmPG*Hv_rG_45(r}Iuj~*_h2E}O2_86FzJ-P?_;9i8B^SuyQ8k&&Vuq+BxGXKt5n@XMOuFyw_+}H-hG)3}AbmlrZrH*r0i#=D)i4vZcQ~-2jlOQzP*+RMaJ3;1Q7nR_8r^=qqFu$N(Zz8{5}j&yA+GDg`eJ@+yDeU*`x14}qOC^2PdP`30k-Q<J2fZgVeqN0U{ExQ{W2JFf}m&bBST3x{jsd6xD@B`G!2_UM7Wb>gn$wIU$`38VEM-9WqsP`!VPUR<x85>!XzftY9S2!P?k}v#=dCV3ykZ-zT$$YoXy{e9lcIaHMZxWmGfVokLUX;_p?A=*4km~MYM;zmF8)5rcX}Yrfm}iUKWswa(I5cerlm#yyLRYY0*nhtghh0bQn+(_AhNSk~Yj22i{F7xBx!9Q`Hs`3Sbw--C(V)OBz@`g86NiAbL>XG2wlCu68%7i3OUzu_Qv0cu^d}E)1q3B<-P|ikR)?<td2Stpl4yMPm@?hoWG6U#s{drLPXQaygfZ$+YyapWZhrBZYjSiHe~+7t8A1@6_*KUw^xXmCxIw7m8z~73UNMy+LQ(I)SM7#%xY?-~B!21@3}K$hGZ<j9PZOflf+NwHQAb?3m$KM=Cqs&*Iz4gNeW>Wr&B1(4c>{qhMvac5DOo@z(-`5f9V;R4@nh3-ph`#H>W&TK`<@mCFs`*&G_d$1y|qTR^=;zrYTxb4r92XtoD@$S1;`>+${W4!KP?HTbjH;B9@_#70nGzs_`&Gvh%qyASlj?3S4jC&E+n8!s}dWxadgFz{(vkK3H`b=SjAX1<#}HY#_=@&;i+zP}RzE4BDSB>l7@Z5`Ol8R!cmBv_=f9Rof{a7j4q(5?mq8wZ(5$GSYoq25kjBi#b+%Z`2Lx~CyR=5s~1Yj@PaN-D@8^;j0bMJa#AXh`d{=70`O^Hl^|dps_2`^sbC(aD)@8#YCxhkN)6&aD-x+dpn7zv1(7iK&lO^rda@CjEWP$|8qkgYuYHY+3<KOjD{Rigey`cgAiedUKupRd|V!sfE2vMU|<DWCq%4P(YO;)bk~^A=cRq>B=F@27CkG_sMlSZ|Am-9~V}GX+r5-LcsT33U)ig6?1La$$^4eN#4K76RB&jO*@h)#6Jx#UA9rqCri(p>4O;2Z9!cZ+i@`tWzcxjOJOWwn?(D-2!~6&6X9mMX4jPsT752L=&j`2awi#4&J2dSiwkfEqPvV{e=^rrcNyhArZ)Oz&w$;H*kZeaQO1~tHgaWgIzaL~XtulPUV+YKVZ*JdSnitk>;*VJ_ulK8sN;k${ECqx@CHJ_QuOC}P4YU2Nxm{!7e|oJjBLh%9lAnI#!BIV>)3+S2+5Ah46^9JI^KoG<6TO$PS<{=J#TWgXI(+aq1BWq`nGTSJ*2hQS8Ti-_3PRMQGvwKw3Pyb`>e^fZK9<JK;q<JD$iwF2RKv&=)7ykHP;$aHATHc(Tz1o<PIb+0Kv~sH&j%qs$bPKFkXi>%C}FHPCx%3b`e*R_Etg+MWQ1Me_n67KCu^)NvE$<os+#E2>}935?r#Ol-$Z+>B7D&54;g};v!85Y&t=?&DUXdH4+C8;-lkv7FN(Fc+@HN(0$*bt{^k8jy<qcmbHHaDhjEjQdf`{SR*vTWQy)}0lu}jRX?3=^+$DJBG4<52=bS=NaJhWTK0RnZ>$$CuBeb>mwM>WFe=^gGAIQ7sPeQ9liWrwq6ES!T>ML(GdGmIKp&Ix<V9R4lT_I<20(ELg$rp|o+Z*ySMOEBp<O$bcO@~w-soA7)98#p(Z?B^bVa`Pl{qbjWg%@-sZ6`!-s_~-jTMAQxAyftf<wKUiyA&oZYmZ@t<&qqI${!ZDA`asNF#th_VOt>7uK-=(96|j>M^HN7|RembRdgqpi>6-qtMI+DGNowy!dQw-$6(mg*8b*FUZx6;L@bsILk3qf=kL$&mMV8b%@G7KL-VtPVdL(`5ZytHZXHB^V&^aUiyR8oI5(=W0cF-%~y!;roOU`9sumL;(tQD76QM59TG6V^}@ZIA6B__)%ISQBFsXsY5VSn?}7PBJS*=Go-Y+0mH|q491=kCnRzB5yds|t_8S__qjB9wKvSj49c9fWyZD8u6#u4&_1oVHJ)pEhc;B-nb*I2Lkv3RP6t@v^F?&E1?g6N%VAW)9W5O5kxM}4O-O^+VO7u3aav5~gD$0w77hRc$sUimM31nMDD^j09Dip~y2nRg#b$bR@EN+k7Z$qC`2NkQ5UBg!Mk+|$ud%Poq_KB+W%>i2?85jbau&z=bCdGc|*wcDsyRmv={iRXWwlpdm<Hymzkm;>w_N;6>yUwjsU@&9|BP~3SYh;kODP@n%Alw_Ezw|N-h^O3X9HU>@ITx!hm{->DWHmzggPSAEE{d=%=dz7eu0JP--G*N&K=pVFxPqYO`RgxS95Rp1o%Uq=OVk(uRvj};$fjToW~lVC&2_MSbN5GsNA~W#n+SLX?i!KYjf-907Y_VYPdKV?S``~+0t?Pv=wnc&X8{H#AfgGU(<UvcLmj2+1QztP8Nn#a8S?r>mUCzIC^03YZ>GA=r8J{zEgAaELP*6?%4735{D`i=PTvZ#7qt}%I)Nb4JwA35+NN$3A|kQ}Qi@4tMTw^`6qy(&^Cl?`b6ym*C?X5b9FsQG5NA?6z?t%1ZX2Xabs*~~7l>Gwwhvtsfz6DaU2DY>4ec<fHE!y=P=+`o^>X-DNVu_G+<e`?eUIzDp!TIz_CDCJ>LR2A2p1UPKPXZmW(Sp@^HqRhi_S_ourKthBxMoSgx$K2aSwzp#z5D>j`GG)&ZxbaXzdmwTdxCK64)dMF<h6=%K^%ydxp>SeF$3ySYMcQrD`RoneBa{^AyrFMR_Xb?Xt=-dDu~6Qd7h8jrAFw*Kc92d-K}+Ue01s{E_v-R793iJjy;KdD6~@;qp4fIu@XMC`FQ1i4Q0<DTW?^uH;0yilpQFeyK@znsbWJGgFGT;J965N6@Ok9HW*6VkfI8t>eGCVolhtv!e$K`v+r46ySLNJBqDf;?Gsn3){QEskOn>TAA1_X5JAP>82HJ^o=t3g1TlubTSD%CsgNS@=Py^CR4oD_1jc(e3w0Lu(v%0Cq^oKTFsT%`*8y~*O}F7A_g6Aqwm&~8!^e$e&8<npApUtQ?5AI>5CiEJUO-^5V&y}Qcrly>jdWnqs6)x0y~$r>2(*Sry)_n^|tq`9Vj5WM)+wgUkpap)|I9(J|Lr7Xz^OkV;x7irLcEPR$cpqrNjKaG3T~=(5s}<6K+62<FU$w>l_v(O&&7xm=$FdO2~b4AZ7MbgmwX;`O=NT&kXWsnT7z%{_H<;-bUWXk0#^oiVb#AG~?mPGp%6J9>V6M9>O`(BnUkUBTo%8g$i0E(yHHN@8=9t%C$8y$hVmt*xI|M7&MApe}@JN0w5PE?JMb`+hs6!YUdK~*$BO4s(a#Q?!i%uprj~)2XVSE%VY_a?f}QSwgx6xDS4(rHMt(Aq^djmdC8+-S(gGn&J5$T%O16hRw`Dh5Dyp^#4Ape7WW0&ma@`>E*#kIx$e7)qinBn(W6--(qY{JmrAIBDza*Rzl;gBIw=_wach(EY+%Syfize3kBA6KF-CBP1v=(BlTd2x4kuF@rPyiFCpc@=SaMXuf@=U*dXy2Sq~ubqc@K8aR~>{7#x}r9W*J#D<JTS$=XiE7!kKQ;aOuvr7@|~(M5#RgQLsxr1$Ty2O?+<}8$7v5;SlnXd2KakU<yc8mX-PzDNMq=M%nox)g7eHIZDlXK-zH0)q&6kX#BkE>SLkzK3tY+9xC?h^*)2N!i54@FsD5fTwjZ|F_A=zawc!sxUhuHVc^$hscWg)R>o>P&zt3BNX|5-&UM@5`pW*}qQo|ZzcdNxb)aKK29GQK(t>W`+{NBSlY?{_I=8FGM3J#^1JK=iFJ!TyrV!z<E&)R`XL5HKAms#O;3?@c^g<&1eI9M2_T4yH_Q;|PY-HEp1nkeh#@e=0CxKTEM07Dbb5l;`7$KR;ASZTc_1uo;yN*d`fr&c%2S0NPc4(~TErEitP;A^kJUn)Eov?O_+BYG6b11eL1tRd5B$maY8gFRlb0qBIP5qdh#SnKyP9^I7JOyoeD<bMUQ}?ATSpMOC&Ydo!!zGm5`huw0u*&*qw)5L{3Ektm%;t^!x<K0-3fbPw6%#&fRKY#`Z4l6a;m>MjhSCqB#nW0AIFcjlNEf+{ybVTKg_phQD?8Q<p)hW0_rvl=icAIz?fab}H9RP%Dmr5tSP__t)I=V?5Zj<b{c-4AhNmf1gN=(<!#Qv*k)a<?b`QD=@=!HEBB|UQ`bp;m(9CVP?wg<KIY92s*Dtxs4b~L`s1Zt12qN!b!>Hc}K3r7210cLt(V~K6r=5l@3Q)A?sSZP<+jyMet(RY{$J2*4uj6oVd4}gWwnLW`Z-|Nj)xx>nVbF71e{*DKq3J1iZHHbJmu1y2z7hi~+zPk$KFC3?y5=<r<U&70apYGkxIEi?RPdfN5W6HGd;cMjsHJ%e_J|I%Dx?%S0$8mzK^P|b;JjZ1cGn8Rb0GW{UG&k6u%)4=QPGee3ax8sOZOq6m)=^`_EU)z&T}&M!zhchFm_3>FB~pZh3K8>t@G&Wy6$nGjM9T{GD(^&zpl8&(iw6$uRyRKS5gjR_z3J;lbGZJX|f$q&Cm43x?eS6Btp!T*P``aKbZ4<SxZ_yKf_Z(amE_F1xrNvHrd+mdojzRXKC0yO+fRAUcmfARuh#DmZfi4kD)|H_XR6t4@Jjy>rU`DDw6=FU4Tg;U@_oEz8o{6xj4awiDP{IeM_HG9INdlZvVw5EG}<cTe^XhQ>1626o<;;I&Vma{*_gX9(v^rg_yb&$gUEyAC;_`<SbZFXwo^z#UtP4)JnMVm=`$hv<Cg!k$lO>eUs*}_Y&p90qr2OPI^I33rH0BN0`P6>KZdlVV(}msi@xbGd)3tuG>vVJ_P;_Zx{1?ktc|^)G0OatIIU7EG*fwZ~NTH?jg;KCkubz4PRz=z-Zfqr?<m*v1tW7oOqG_(*AY0l|fmQg`?m*3@$2_l7?B2&p?gjapBAVE75oRg{1GijyRzG%tHdSkl2Y_+?0F~{&6{hHs?i@Y5hdToy_6&X$)|4B<CqCOh^sHskBC&%H>Wo@D>EO!K~9)Xitj76~!8DxwqC*nb)}r_^{Y3D|sLW6ZAD!!@lJ}iPAHKD!hA-q1-$*ijURYbO}Cx`P^S$cXwgYc4WIY)*lPA)UXYye15{F9`3%g8MT>k^Vrj2R*S=4ct(nC(>lru{XVK=cC@oCdS<fLPH}DG>A9Gr)&m8xb;7-VlR#~N8Xz$eJ0?-J+XUmGiw2F5dLGM=xmRdGWmH=L3{}OFE2sFv>N<x-_D?Vu>3A(^JVobw<*%NAo0lnb+0d7qXJ7DXEjZedik6FQxThNBkC!=pb&2}^L1u?sX23wex1!4p2;2_Ka+cZhoUe$6HV6mCOOvFLw0`g#sG32{jp^8Qp5<|ZbQQs*-PWU1+vY;>n=(r%$Am#o>(C~Z!HX$78}g7IqjkB!;AWZgLSpu?%E87aDV2=vZMyIFlE8*S${hZ8+{=@~c0_xN@kt90cWf?ooh#&aE8yzXiKdxuyJluhoqt4m?2M)yls2%Twz}{+IT@_WjPJW-N_Wk`yUZH1K9ROUEYJecODnAsaT86e*Y_g{6PY+;e=hi=4crp{9k+U)o40w{COM{yJ(!C``?~CY&TcfD#a0C$>{o(dPW@(fg1}t(9N2(o-4TrW0a8~U%@2GZUfZ0EL}2}(Lrk^H`ovbO+rqCY#IbF~cw;vlRnW*BOgWZdKOTo;t#x(R$#(w$;Rdj-o@Vf?8_gt{1Y<jhI+{`Gyi@?%GfF{tku!njbQJT#g4D4c<s|e?iEVCIMOz;(m&mEVk9^Y8=f@N)%p~|dm0Fq%u@>J&rGVUF^AjPt)aE*vrcwvl^65~x2HT88(L&a@@2d0{YpN+LQz`=a)bu+n1J6#79tJvLEZ_o9wRP@z8zD#(8@owvrUK<6gCJ8Byouk+aU1Vkr_~0$E}a@))vL*v{u24RTExv%f&%|63fAqNQ*`!XjZRXW88!(mE?>ttBq+SP(<HaU&Nb{B`|ycoHlVbpWxo$%DKYnD<g@P+nsiU~IbUTen-RQhRSuQj8VAsOw+>r)QWS)cm|SEGP^(Man~j%}Yqu?oN#*(_ADtzqrI?~ma||RdHtSq`^M3t){q{Oj-dS|ah}wLVrp;Jz0>Bl)bs}tq&ijE~R|l**FwLkNp2^QdRGWBnmR|P^A$MaJejrY`{o?S8&e{;L{%!KhGKP~qP`{UXn{VWJF>y)~$lWpmX?K*xTx_$!Ub|<-tLw!xg&7Ry8!)+-M-}N-dyLegLkZ6ohVE{352tv%Ti0QrDPr#lpGYuM8?YT10&ky7Enslyafj)0R-IWRxFT)FVPh)-=*0;hWMMx%-h+47*Q5OS?&sH^K7D>QKfHf3mibVMcKz}7XY=!iyP7?3Yd*xkX&zVWR3r>Q<WV%~4y19noAYps!=B$_uTS(UM7JthDPa@JwS~KIe#K|C*2%7!{enGW&KDvg`9Rs}={E=Y%b)MR{^h0*UTpyae1_N5^m9f(fsvs7JI6$yO(A$g`k&X5<4OPXZ(na2-3i*sy%}0nnf>i!UjqFwi#V#i=<RTitn6k8{o}v<{=<*o{q4&qfBxOP5O!eqQ)Yi{yXOkXT5Olp483{@JWjg(L|g|gu@}ubbAgGbP_+SL-R}H#`!z{hyQal=z?q85L|H#sq9?q21aMTde*6L%s)ygEwx*Yhh|b7v(-^0}I3|URiCsocofSyM(kMA|wi){x_$cy<HIaZL5Z)BB81MujLz2k#jHQnLuC>eYB+v#E`*F^<8BYoUo6EiWi60kL9jqMW6cvBVIzl^A{2>7T^z#otefn{|9`DvYwP~V`o~EF+iFO~Si2CY0Jw!7w`VCf{1hT+Qp}xS>%X98j;wDCOvKO7_OVQA`nFbm0;RAwxj8qy6mt6;<_R?1eZ{Xp;lx||)0bED5=rAayUi(9H${m}cm|v7?g_{QyErQ!V``&NsRg~@1T2k!S;+G3BKJrT7o2kv6%=3U{$*d7?K;+9TW#kJJj$z>(a8`)-=FX7|%$I~W35mp=nxfiQnm+p$znJ`OSWXD!A{WefKb373o27Yv&NEJRH_KUV+UF*!ny`2k98!2m%Ke^ifr@`qlowhQgNl(F(esUYqSyYjL~QFq8>4X}fBWn8`pYh8=ip6|O0ro7OOXSNs{4|^e>ibI(&DEZBC_bgL_&Qwr1{#3m8QvDyrU+1d%5TjtwryE0eWhXC$O^nSR1w8O~UZ*l8^Uw<RvNY^Sh2NA)=XhY5nL{4VK!X7|%u`d%zBkhL9Y5!4=hyYA;bJY;*eo^8)`f$s6j}V%voNG$BJ43yU)Q!4`PveOn}F5h2g(prjj|Q>oF0eIe0bC7O2t&Wp=)HhU_n!2tTN_Mc)`1RL2pjv;u+=u-RiJhg@zJg#k#JUs<~J-MH5Ta-@$P=|=e2OgMxXIU+{z4%LCMoUDs?FF{CN;MUg+h2&PbWeDRTNw&uZVM)f+#e%_)tMZ2CwFT)M3@w^(vzODw*ETWP}!Qbi-_P%zew-YLce&&Wu4PfQ!rt#;n?3Kv1i*gHKVZJC4jd}rD*Wsol2VK(m&w_YyG5ZTRm($+9h&cG)b4}EAK#^ZC9bk!_E-R8?t;r;gEDwU6lt2Ywx!syF9}^9k+qaX@zKD{2uaDy0lPt-|?Ng<s2%N@pbK|_l=sIyD92`@xL8+4AWBYck1`AufJVGIAweE`c|C_SE1lvl|Iy<laCyX#d~9hZC>5qV_x7c2qUq6$TZ33f_yc_BZM0U20Lb`X84{8lraJsWKO4CM>(t1G_KxAHHKM?;1`v(1NQM(F6QXS9+{sC=74^I{t>8fC1tbMKi7KX=OH|sLnHV&X6U}w<V*Am?7(v23bq2x_J9w9z6?z*-v9Ca?iRba3BjL5`M3396WiYZAw2v{UWj*$XI`uwK4$<@V=J1C5sDpBVYKc6pO*En&6!^JxL$&>En1L~q@^WHz|tUpCjvT7@r9V}Y(u^tuor<1&ip%1lH6X{V<4*(TnP>>ro)w(SrDu!y=0^U<cc#aC~`6b8ILbJ_MPjDhIrVEn?Ttv*>Oyy(@3S5ea{66!@#kN@D7p}Dkz5*8mHa32$1%8O2Xq@Fs@I|Y}>G+;gt2j@4+fKw^k{{DB~6>5TA&o2r*Ud-K4*dTv!6gM@AW;@=#Z7S^-0pEsFv&IO$C2?hH%KNBf&n$1JB7>S&1N-I0tWlQ2mfuJ=*Tm(+$>*EY-^%kqDy9j^!5sGBmk=i9^3=JA}kSfaD4?^4kE7>amBVM?)Rw4vw|T1k?L^fk;+sr#I`A3~)<8?_CI0qW_4#0y%bWyVdZ!UJ+-&`!OC#j?nX#Zfk}Lc1MqrfYWHrB_=Hhu%u)*U-kpx)5$TgQ4!?0z`)BE~B}g%(c~BM!A)hjeglPV0R<7*zOW);1NY_7N`5Y!N4GNuOKo-5Mn9p4dDXpn)V;(0$fMbMQk1$J<*<R;0=WEq#~SFj&+i+M$pBV5d}3dbsBrDL!4DYD?rGYAV@?NO^ep9<6USV-laM@>uO8LhpX)C*R=^+D+;^qV}6fi#qND%Yzg)O371)I0!8)gJz3CsEH4I@TguY=H@U5+gV=TLP!WeCIqm$KRX3>Lw!4cK*RB(<1w+?rM(}fcce<gXF6TMAcFc3=M)~#$U&i@^B7?4rsEVwo8YCzZ#Vg*{My==cfa__S(i{gnftnGM?*f-BA*&ozQoFvZsh)fg2_4@KN<9P7G`$R$R9WBWGE_;B+S+O$7zIfAskBX3kO6=|GznZ}$4LN4?X^%yb4GH}OldZJuYgOENUZqFTcpM9@^XE5sRuRWKd4;{)?xN%7>e$A8Q6e+RC&V&UGG^I!HxMYo*y;L#o2yL%Bx&<!9rZ7u6K{~&QX~yx0hfx@XWLW$iA~<qhd++$+4w?J^@iFd0euJk^MG_3I?8Avi|OFq6QA{|8l#Aom+zrZj6-Pjde^IUI0tg`RMe0`~g^gpD!Q0y3{b{{s?0kf|md!()?x%l<8=$6afJ!<azQ+aJ7vKAa#+q(xzIMyq2#UXW5NUuo+o8)FTwBF2odR^c`PPQ2QM+?kRqUAH+(asZ_8&47Q7k2x6DR0pI1`!ES1^o4UN*v3225b+X+s=5t5gU$>WQ9d)1cp&2knMG*X+2Q2b0*cJhAS}%Je?STM&-yK~P^6M30xXq@-Tk;;1`64^QG==MR{scB#%@5e_vbjmXj$EOUMQqgZugCS~uq{p?GXD{{)I20Obc$4on7wJ^Z+Zy;`&$G>X*^DP+Bt7{`?0Rj4T|nc=(wO*oKgV<uc&Z9?M<MN7Tg|70ZSVU-aOi2)r8{=EKQ~mCB~Q2<<pT)y%+T_%!_f#KOm5ba*&l0fL=E(0c>3&^#tDWQ}mG`4JFrb)4!SvVV>yhLga_djcUvq_2WIUv}bR4!SVq;uze&5v9S<vwSV2&@7&voY~Xc>Z1<N&ZGfTi-x#Tm{)J4-5VJYQ0P;S!PC@q2j*ql9Jua+49<(HmX$Ik*m;Tbr)FGa(r?HuSH|PAw{xXCyF*@KX2E2Le>_#Bc4u@B+zsM!(<gnY2GKCQzZvk+HIoNSu@~ISmx2hCIc6j?(I|>yhGZfFJX-yZkI7K@Mh^lEeGrF^EA{d<YyS3I5*TcLo6Zoru3%U-mRgrq8xDZ5qfCW?FJ78b}Vx90NZPvA_u`3z2?K;0sB<!{b9Vw;FBE1X!7{M-fD+C{O2`QQcqA1s@z}O=Hq_P~rLm$QDv7%Vh7s^G9<w!Rbq$uc$6GKv8=eCcA&LnGqN8vqRHcFK$DArLfFo-+$T5{fJO~nm(eAbF39#=7__X%{3EK8V`{|kvUw(*NEO1Gwo*Fm@E)aYnp_Ple^MWHY#@VAsJB<3I{HI<*+)5l1ZHoI-Uo`sxs98v2Fr6@_mgJC12Ya|!J5D`a^{_eX`wg}4Rv{xQ2r(!hd_kr~xdKO?bVaAq<ZJcIo_k~PRNIw+Sm6&f<)d#&Cc9aOz#N7O?mNe2LR5VPKZ$4(<%V{JEg0Zevibhb1w%CW9O4`Fn=<W`AY%HAeBIqQG(UCbOCdDG#%08C7H*8C5&ij6;$xE6OjZeOH!5pGOl!Mq{K1a%_fYKlqu6Fo{nK2+dx+cBC0Ph=GnS(5*jS<M?rix0Z8mFHHVa0yvWWI7vqs+%znRt-ytq-*laX~M%=)2Wr8U4ULpFhJrAEsQHqSG2JWE=8WnUR$royNh<*%R{YI>A(f3G*%qBvIC>&0Un9dZGov*j_Gnpnz`~k=tY0Rxq-*u7rRQw^*uJ)A7!^I%DMO2q0GCF(NS*Nc<<#{rxz~?eX@opGWVLFK@!1V1CS)bKE>kP!e7VElDL<9OY*EqUEHM#0*Jc>^NjZCp;f{icl9I41Q3ja^FE@_^djdf%E&1oYw`O`uJ66#89y}9CF{iXM3jQ9@+!meAELzhoD6Ou#G%V$210LjYX?|Q$^g|{9aH%^1|f1``Lj{y<3R^Y{*}CsCyvrbpf}&5^&q@thrM=O?a<F2xn2{3OBI|j#`ABM2RE_OoiDFuca**;8-U^&q@k9mp2u{D&S^I)k5_1l81e=9t3=g8K@;c7E4>#gaVs`cA_DX^#9}T%a$WKj%9xc54B|0^2j5?B$|;NnM4_$uATq?i_4j=YIJ3Icz9$tB-wc)hyl>KM#kdd{shvlw5o{=IV6ZF;OoHYyWK!!uN|l+=!E&WE+rEpvz(WGN$`!)4rhpcrvejw>Y-(i8gMxadnk68qtgR-nD{l15A=0wkGX~PQ9%C?90_2CL_$3k-&c6PZx6*ZK<&{3Gcb}I7xGFF?8JMm!~Cpp3N36WBxm@Kf{_=Rx~Zu)>td*-Uo5>=LkOj!VC%uiggjIhNM}9l+q$fx&wZKuBD)c!nUFNxMpZrU1*=02$4;f6Y$gQ04T<8f^NQ65l9>VAVGmhXSfdDin)!j{&>G5GG9o#f=k(moDEa21-Ps%}eG_WS@u!}x%&GC5RfgvmMZ|G=Wj-etGMFT&X{h6hR5~R(++(0iM*)kop3>f1;oils@|eqovOL#Aiy4YBuW^%OTkrUM8?=QdW~bHbI&PUV9ZofJ$SBA<>Xh7eYo<{Z8^E1dG7g$K=J+&a$ZYF0b#|(A<g?yT>^6T8-Zf_`RW5YUUY`d%<}oH67xXNZcx|*uGq@GdtP-*(`!|3GPOc|4ZO;Ksn^)#*^5HdBM@<#4{Tw)zzf3h`SL1?T6mmefdp_Mgj;;{dZQbTf%d^a<lpt@^gsDY&-Ez)KXGh_@KQ6jFl4OljDCa{t&j~7rzPjND`Sldo>$GVN|7pgih3_Qg&<TGVghAG%%}b`(2v_pj<XikKI6-Pq!r9~R9s}NG^=%u;vW6c!x=!hjT87}QP91`<35=!#Dak%_T0=;3&|T9A3YuIVxPOxNHhxUcL5B>_&|wWPRY>|7xA=u~;6yRCEKka?ybHWQJ()^0=re*Yt6rL?1=MiePjA*sj<^P}?75Bs#<CAM^`!Q2JE}VByB(Jt``PpQQ`dFMcX_{7j^Y@{oNVomx}(&7pyIf60oV$IJ|YV8kUq55qSA-5js(A#n>EwO&T50j%_My#Zq54-fs$LGF78|Ax~YsM(d&YFD-$4A!Y$0+`UY$pkS0YDcr<eCP9nRi@J!c++!vmi`;gExVNcHaQ;Fh%T4UY#E5FG62Mi$)><iCmrO2x5GWUsG@t2!|Ha=tkD_LiqtA=IFWeuG`<^p3_>k_)N4>|=Ve@!%P0~m1PJnvYqnAn=ok0s}ncL5d0mwkaeqQ>(SxbVxGptZ0U#3H6eq9plt-1lgc>4nlM<21U+L-By?5&~2x6RFIv(U83-2|*8BP;GRNt=qugs7&dRGMqX*a&;YL6PY2L#04IV?BT2GpWij&2vGQ~0LQkjm4V!2w&ad7MQzB8r6}s)IQ^>fLaYC51fPI@jDXz%`ZHcS9sFIT$gny<y=gFS*bV_eAz^GBg{@mCib5e$fc(QOsou#jftoq~5yr+q@^NceiUKohdY$~tebAWcDtB00x9RR6=%2X`xc$F2C1k&dg=&JRVXKJ{NJ80gHZt;s6tZo3`a%kg%{)Y1T)67Pv+bQ}yLTaH@d70aPP0%O^5k=0{`|aueETC#Hbc=UnT?op`MNuB4DNmxnudq~?0c<UZ7P)dji<{(8m0SSJ9u9xtHt#epOFJ2?-SupM+yEIwtRnaMd*5}wDPg@z1Wosg0i;tfS(sp>m21Y@Xi16lg2_W!<fukPkvY*un|BnD+QOH9mi_q5RR^Nwx>UNZ09meYNsDpA<%@G6g+#F{GKfM<($l{YE5yGM;?vD;2m^8bFc@;<~LM-xjxH4q$Ad;x?qe<^SA%TEW@fEGF%iga?I)m@pthU+$NKJdamf>7&*6AMivq->2xmXp2&@bVhqk{gMvAJA3S%>jin<8W*quRV`Tzh@TlrV{fvT@nc0}Z4^j3%>UjBhbbY9kPHsqUhNeoK@la}Xdgja;Gf5JQ`3>41bqxF(O`_<lpNr9KGXL=w@NPc)3xss`^c;tCN{jjo*o-~%f)V=s;pglo#$yh5Cjr!<J}|o-U@m+PY`~iyX~(H@iR{{M2epszG>L)T!&<0a%;vB<|Cal4<}O`=)@7QX#U{PrE3o8+=A~o6(eRS|_%c<ID<^8|k%0JxCCZsyI7D|cjjmmRSro8Mi<~0<P$Ha<FaUO!F$Y#!rd1yK{o+{`2f!Q^<h3J)x@C^=$J}%Alaj<M@_J^LhEZOpJhSCi6t_T5T~X9ier)D0l9e6^ch2*XaMGV%%Nvcr=2@?v<05XV9UFQ(<Y*h#jbqdTSsLJMVDS?0Z#*G9ZRz)OtgFmo44G_#7*T92mi4=rdF$iN0FIT8kLsdRHy3t~+*vJPX5H9<mmXaPYbnbp^C>$-)&cI1foo`3eT=Ur04ur+D66UEnoXCo>Tc?5zRL7WKyJ+?#@y&eAX;mO6<#5uzPinW#ZNTfykF1n-#%u_HCvWUEA3Zx(k@$-IYh&*eP$+U>kG*ro$I=9iv=S-EcUi1ZZ7i#X><?tfCOQ~&%zKGK0QKB@f3JvydlnlNq>yx{9rJ%Kx8vB%Lh)>^t>ZCf>GK?dny#L&T-8%Y*n$;<u5GqtzkO-Luoz*ki^dpfU_`#xY;zAh2dnEgfQ+?yuJj-Fwhk7-Nh#q%+v-=m-6(F&!s1z+A}<v=~jC5%^JZKnKJGNTM+=^O3;ip=ZD8!@GkHB;~n|q+iySp@y-131!TWH-m>4`fBp8m`T2|OVvq5W%)5Tmyy(Z8Zz|T)s<+uM><@=uh*C0lYsAl@IaYuE`TG4YkAY&*br?@O7GvW|$1u=qvCrVoF=5{I#{_k<c9a4)07pOoq`ajM@P~N}W6i5p+7AwY27K_A>DTZ-8WiH<&))kg#^56owypggJ1$4t=rk%&$UOcyT5Vy2GFHvK?Z)9~A(4NE@IT-ElAnJ6<+q=HnBl*@zyJN=r#vykV|7MZ*pK)lHru4UIl*+{aGfCRHtB$(5KM(=vh)v}Ls#!pndPbrk+?Z09-~zyf8ZEeFO8thfHM(p9x=i-ZDA`{4Ae3D>r?eV|N7<Epa1vI0sZkWpMk9XA@m)fvPs(ge0#KDtu=CjK@;J9+wC|VBSsVqpE%_6x#+8^esnI{!`8Wg12~V<-olxiKdsLV9I26_&&Q^Z-j=O&svJ8RDgo;y7J(5uhPta{3Pe@*BMw&Vd2d?vHKugi!rUAescBYK?$$|d#wCI|TdxglEiGb(z=3fII|e{@m04m}fE;{wZ~J^(d1yA&+h>A-a{fYQw}Ur2Zn|grMX>g?bO08+>UYO7_7Pt-bOD;CcU+HZ&2vk#=xvns^Pk&XUwnI9R#_fiD=&0x;`WRb)h$ezSd`Em)GzX*fSfjg{E^p~-5hHh%beG79dbP;8kC0i5d=T(1;cAp83ij#x$;3t)ca_eyPb9HG2TJ<lRK%^qejmxN`?)wJPB)eoYEW$CQLJA`f%c)d5wyKQRv8`O<D=m<BMaYI5zT5kh6|pNEeP}^gB-se)i24i!6>A>!mR}htKVZVkMQKg6+*FkJP&)L_yx=K$G0Kk-Kqgf?wJuL#gZ^^;)g{X=EuW#KW>mfa}L0RBlkVjrwL<Zw+)L;&pJT&0n#r+tjg^ykA#@Z-=+KQEz0du8#=!=2BCLaC<7j9+!^wq4Wh|jHd2#yOUM!PPA1wJSIl@?cdI&=XTlvfl84$4H)AVvDA=7fGX8K6B%z@X*VaTs3zAW(UdYaFrd_$+`oYM8NX<I`{aFiV%AY_FvwJe;~CR+Z7>|06^cJNK$7<snvcIe=L@#gZHMSC;!K$#mwdM}m9K!wp)f(ysC-^k5*DWm*&25$7-s$`e|BKAx>GfXLw>iedCY&IaLnSgwOCgQq|lhl<7Q8VWc*ny*~2~@Pz||`ylt^zLr#d;jg9svspHTOdVV<367GGa7wctdqnExCQ_eqTFbzXzn~}*ye9nbqTWP4Emz3r>teqM*80myVI3MH2R&`L0Ax-MZ?g(!p=(-*!@^e2m1S=gSN9dE16sH*Ll1OA~L}6v&Jj(bYG8J>d7QWVU-s}<qwRiG8Q$}rmIumtHx}dAu6h<=5w6v93)ipT5R11W+z{5_FckW3|Nwrx@fuoJsi`&51!nQDtcpP2ur}zS<2GI`8X$aj@j1J}HYZg?DXs2;}s@s@9qg`v6Q+;$RudG}|TYN50m4Iiye)2JiFz2PU;ONRlsW952tdC)rsN~SZ5+T09<{fMRj*fM9;mbLL9I+YdEhgWR{>?quJV=|}Jc7NvO9az;T^HRnu1PM#;+Q3rxgfyuJnWqZ$&;ev3*Iw}>m?v~V9*ceC*c%~A$XjGofgq<M`>dUds-)k6fe2QEh?#!p-L&1hmI1uu+tdR`tVvb&0T?***NWLg>jlD)qh2AFk)5#Cd*1cHZJ>f%RQ^$3nmIK2~au`EYno_P#9=UW1Iy;GNwa=sXmK4R~@$4_XG<Yg;ze8UUWRgCThNTYaaKbojoz*bqr&B_V|SwRv3RL3;FU@+@FNE#xgLfrmtPwd63J>XgR@$vAjxH%yk!W)_Fk?=O?RDBw*6hEF<A`&UbC;+}kmCLgXkJgM&xStW+l~j-eO{g*%hh0fVdg-g#=+f?TM8G;U(ZIfSh>y5$U86g_dBn$##{pF?4s7~{<upm>s23wQ3Lm0P=!G7p$Z#c+9>onwN?*FSiSbXP~(8*mGEy3zE0S>e7To-Sj$`AGSKzYpMW1u-)P({ATnCYeJ~VknHc?0MQiho_q7`aG^>?vR!g!$Q){E;y4#;K~!n#=oLbklhc#7rHO5&d4PBvY!7g6Q%pos8d-os=ARI9+Rt4Z~!8*=PSL+-f`qRaYzo0;T1Wlscaa$bK^-_qCxZFG0GgKr;4FG_aQ~AA7ZT80GVqT#)EeG%x3Yq-DXe+c?RecxvG=}@59js$~Q#Z;pEuyI>l<ZgH;elK!XRBPCi=@{n^)n?|QHV$Am)p1ONy7c$fAV{3iMZ)?%e4N-z8B>>qENn`$0p>3Jq#imYP}VcDY&t2SRDnI&B4twk<LlK%U!uH%(g6Xq(u*s%q!wNKdOL%~|{Ji98Wa}0DL(ADn;-D@g}$Tr?Y5p;VOCGyG;)_UKGHSqZuB><bJ{k?=QXkozUf|1*_#Tvza2a8R}C|o80u@q#YJh$;Wr!%Keqq-x_nOcvKz)S5DN9QDv?@miZn~xRCL9)|a2>VY6jOUd~mZ)2S-Ohm8RTdWi+>|RFKN#*5=fT<xzI0#NzuCl-l``{cd<_YQ)Sbd%lDDh(mv7%(AhGwFv4006FL`<J$h93k&K6(fjIc<}JsGa0_Uh|Z6*}^Yd|k*Ir_r!Y%hK7lqkv&)kA_mP>Z5;ht69scz7f`XqT*YC2^XNw;96}eeg;uH;(@T@Q|vt^%7qOL32kNS(ZW`oBjmsHES!AW&UxG>yAHZ;83mX!Qn&<}QU|Blxo-{0NwO0z;(^l;39OoQjB=78)U;LzE)MVi;8V@4bBL_%z83E)XJlxsG=_;|LPgHhX4=qMhY)WK$y%(ns&eAwZQzwtS}Br^&@tRa=8L0v9Qh5CYVDczUi(lvDi<9{4e$y#I_;kQ+0?TV6xTY`A!$jzAK%mPsetojk3BotESO3>?XJDqBHl22{0VrAsT0vUB7hMb;~Ui@(yKEoj!@A;^#s<Zn2*K&c`Wr19`Lvy^IcYnnzmUcSp)`vz?=e*jO$ek%52kC)FT7TH^>Pfr$)!ZW%RhuX#Si?m2HX5kAUP_<R!qASjZwjHPkRR;}UVx8NwRSwM6{@z3V1qk_m^HYY__NGQbciC+7EDf!r9heHChHi=e=fj*Xb=(Eu?xd9ecNqTA^As6X@C39*<ffn+imr#`glT#fzw=wrlDTP7xgxnv9G1nj}DTgOV1(?0bz4cm&hjQ6ww|HGWy-Bi{)R3oz)Ad1btj$xL8dB<={Uqf-|HfWN|@%U<RJZWPG%^vsz1H)Lp_~3~#vp>MKM}r2e5B3f5cm2_9o&6k9v_)|4ESyn>yvuz?NVk@x%}B<<3}YUKeD{Q&PomuOelx&4jC~ChG&Hc=ba!dM=%faLo4C*aI|e;<Ch){A9x0IaH+oLfhM;irohnV5nSgPW{DBLN|IfetHBpmIa^lWIefl&4M?W5*l6aaMI+zaAhXP-k5T`XDwvMaZFos5A16w6LXU^U=;WZE2Q%BQ}TSdazV-$PeX#>^BC;}uxPO^_YkHfPEFcAi8kJ>oOau7WX7z*3VJWidlFS<Y#Lm&3n#=`SBCmAtnP}>(7F(Md5Q(|?8U(%{QC{gEs;ReR4P{};j9=92|1)6slwyMqzcZ=Q=$}AwQXh)H-Kh#wgF@z7<bC7^I#XL7WEQ}73R{D8e&BrQ&5$*ZlA3V62s?oX#A%bOY$XD?B*X!A>+8m0`9tR&DW(VpxPh%IJL;hUJEfkL6H0heOtW?KJi*7$X7|xuhFUIi%=%>)z`IUw1?2YHZR#azxS9`&QU~1~)uGEUJ2?7qKHT@*lIYu7QtWX{kH%t$YENS*W2DYkb>mE7@mNR6lc#JK{x}v9N>>zZ`0%1)f{5^+QJ(t2v9L}S&W1a`~aFRL?;dy@}l74pe=21P7=&DE=Oa}g;%XTSO&-3((^9d=c$fW}gXqdmA=UJA<5&M5bQ`Pf087`93e$GW6KP=(^UO&RC5jXMA4S&m#S`9kjdn?a*eXBD7n;ou7j|nuYOYdJ)m!9XfCl*JICyKDf6bB_P)5bC0O=bV!#P6^-`h!=9!d9hu?j-yIHCPadA)gu;0O1xD8N&vP-2mYE?rP&b%t_@5Kv~@~cGCIbGZ=(SJ;_9=<WyQ(%H!|HuR?;ThNYgskV3{5p=$Y1tFO+XWh6EBtk8t|#f@rsU0C*kl!|FN1(Bc=jKndns%&*9*tq-LhABxfkr44sL7%*qhl(+wvdmo8zBrm77>EbU$LPi*Wqawtl#~VOc=j(ikYS^E1hny3fP@9EL&w3S09?ukPa+#PmTq`ZNWUMAs$h<k#`~U&QYZOP>IBpzL&}S-LfLd24m)4xCysB1+Mp*7AmsjP>0m~qeHhR=V+5XbozG>iGJ+i~1oKvvJ0;Xz>!KFmh(=A22qw4%FrZa#iAp4%<W#Un=N-hYH)rcisx*WgI;@C4j+%I90}K$HzPih`cQGT7p~{S-meF9T&->NzY_u;zNT4!)RVtw6*+4mqnyAwU*ma1W76>dSemvaS^-yiXHJAfGm(k)$pv`%i<q9w5j}f;A4p<qc9(ciI3}a66fZ!!CIT}U7<;<KpyXBd9O|N5w4hlXt*JYUW$zKa%OCpwgOxJ&|MNZN|nuyr6cHJ$RNCO-o;I8nbdT?3vg5<JEhs>{&u}g!-8&ar)d%brigg)f%OH3Tnwh*0oTi<)KgI@=k;QccNkUHHGoFZBwQA_$nKPK2Q7{W$VzN8*8Sn(-!q#2_u(@;<(uI2j7+MDxyT-3)?6P@#bTsJPCf^{!)xjSZ0mV*sZ?}enmSLvNag140UjFVgI@PdS7!+M^k<*E3O(0XuH$VBb@j6T-2Gt8rK4y_mALse0o*DZTQo{y{H4SoFPXB&@T6Zei>j|LZJMTxLm_BOhZ!UConflr~TboduJB7&H=F<q(zhRNqi_6iSD>HpFLJ8x58tGte0hR+Gw1aw>DUW@xgW>s>8B~7BXkZws5__E)}UY<&?d=&w}yvf2tS)Sw|&*J1TXiCtX#G+0DeX0x-sowqMwS0+32`2@H$E?8dx6dcDVZZ=s4yI6&s7DY@h`5TsZ5hIDQf7pCIZK<8plF-7y<-J+Rn*=WUs_!!j^Bk218$Dpnhk-*W{9fhJt{p0kGs^f@$kiCI22+E8p;b#AHsF}BZeH-uB24d!H8o?@*dICL=RCq+Xm0^BR}zWp5}}+l9w)tP#sa?<wN6n0UBv@L#ILa28qKP7Ws!YDvpar(Rd^sasAuJ_yr1NmN(J!aiB!#pvS=tSUc3G^h5g^&0u1?@26dODmkp)Cfht~?&Z+M-2Fuwa^Ck?f7^wq5WCI{Ej{Lbj9G>##&q&f>XA;I7Ec&TXx1--tTvd>0dvJN9fjf*=t@Hs!uEjkG$@=AVG0F|5BKdoTF6Gh1r3hzLNj$Jp;IL^;HNxP8A``eiyjGS^NYbLWe9c9ah~`E*|V@QRVQ>Q4FL(N-%CtM<i66z1cF*V@EwJ+_muOXteK}?lpYqbF701a!S`j@5<(mQzV4MW>^<Ep3{!9WS(=ueCx|63E4w^o9Byfs;!ZQ<KFQ%{0?Nf0%x!PyII0<CLFqgpWDBaEG0<^6m$e59Yu}MTVu<)%sucA3$c%G0tpV+Jqzpox4GQYqP7^a0Jx8Qxet5b+QR)(a%J*X>kgwPbpBF$pejS7m)CB@}c2Q+scrBLkeADnF%(;|t?QHr2Cxl3*y~gcP=xI+cVB8W37pPv_rYs&{GuLC%!GfPE(;0l$8$+^`m@5Vv*6`BO!>5F^_Vh_CGOY5A3<(2&0E6tjx6|0y{}fQ{JgyTqHBV|L#YAsqno<t3i&qW9))XHJiDDb}8J=esk10s@1rWrjkX~ZynJ6Pj;7>L))`4g$Q|+ZTWwr1RMXS<RvH-(ODcg(vq_Q|^T<{35+UZYDt1M}Zax+T=_h3;*&;S@_UY2tXn~aR4Er2xS2ew*KzBxv?$62mHhP0?{XmQ0hPHr8YcV!+r@1-UDv|ONwsY)*HSz1iT;hH<RI>k)O9TyfYLPIcOPs%*KOvvKPQZDmz<eiD8Ae6InlQMGq$7b>_yXgqogk^{X2H30fXgf@60-1hKW@e6*1~~S>Z6=yjQhyd9(lpJP8JL$Zr+cykOs>A`E6i)I)|lv1rj@yX28Seqk8y8$Iwope0zeX}1QxfTl{u0(h-7to1T3zuZ`9>SB8M{MDc4}JlyoC<U~cT}mhrW>PZnC|?hRgbm0;-V8<a^VIScFk0YcXcs|5vkwO6Q=IdLaw{46(xP;5XFw^mBYQ)6DUq`o*RFH?$jRhq{x^|j=gl=qqulty<&sJWI!rz1|a6><2R2PGtr8*?P;xihOux5>dj6uO(Z3Ercy^$9a@ieRcK0p`I|{-It-Df?@m4W{ixHNAOW)-^&^F1hMxhoHgIeH&!{!P2k|G3k@QRpk56b6Oxqc1=t}M?}O>XwFxAl1$vyB8?yysh*QMEltBz)S=|#4-nDnm{f{rm_(H7y<lETXE_da2N@k3|JYzgnU+a5Mt+uBpHOU(g-&xCFSo1^xEafTe=?}b?6D1rjGhr<U>&iUh-AWVk~a-ck2~8fA1CmRCH4!3a>kZcQXt~{9oX};u<0Q7L#!=0sbo`@AwOE1`lh4pEVCpDY|Apng>Q$4B1ng;o$sm4ioloj9A4iCwlE4gf4l-V3b=<naAa<U#3TpCSwh|#d<uY)1J!$Yl2p!f?3b#a3xxjBN#v3heK6D|aU`&w3d;<Hhc@5Obhmn|j@g#+JuEMxVba4==dvl#w@Y+SB0R>u{uEM6SLS^4`a+gn?uA0lR|(Ww+-#>@UI%Qm4v8!BIgxuMQ*9Oz&R)11R-XP$;I3oJrY1sP%6g*9{gj3yi5(Z1ofTnb5p9IF=oezpvW9)H6s(j1qB&KL2=EtyF2^%2Zy1vxRs^D&92sJTa`%lA=7N)wXk}&MPAcnq1~I%YGG54rZH%DITCgs-a6@i{k|-OF_N4|{N_`d5O8H0?(2-pl1|+L<^O;Bhvz(IP_!qFZgflyRn}!;Rkjq#>9y;j-|LEnVbkZ;a+U(6MD{NfF>pzy8*+w~k6orsHF#|Ie%Tt|Fhu!wD<O{~|kcIia?tlNsx1ay@mp=@8=vb~vmVKpE7lHa3Kpw>6M74+3_CB#$o|v$c;JI*?gTZX5L=k5EE?bf3@!|VV!BegGlD8XaU!$!i>hR7YhJk`c0;cIV2;r$iYF-**C|kzShymmN1DLN7*@IYi^n?>PWKU7)MkO(is0u+4PjZ)DZbspNdPwEs$P#3ixrRro-05DHC@US3J)#?)D5?69o*isM{-p6)MR$<PYEWHdz87HpVJe!KCXN-*0aEVm2jiUrOR6G$oWrl^lIWc$-VtvIq&O0n<@Xo`c~+*Do$``0g<fJ*qH<>b5qQnDQ(iNDS?txM41<87L6P4%#<<8F&QeROXVhgT4uMc)U;C{`EJrP1s9ZieFxE}x;niy>UI&lMxXs|fExu3h%Gq~W(IhCPyo*+m<#Tz9sM(o1gxYP~>*xV)+tUXwm3QvzFm}j`i?XS<Eh<qca}IxP>7M}F1)by)y+6*-e12>dC8OSe;^YO6XrvA@e{p1Ll;qJ{8Z`vAs&s;V&??Ml#^b9pO~;s{_myK`II)WlgXvBxJqi)?i7m3bDYXkR5;E7@0B2-Xp_185e}J!zN7e~hMtU*4<3(o&j#aR0!yc8P(@9ZNWYwI7p^rnx2jj^hrJcz~;%Lo$2ZFSYqk6SC4K+uxGw0H8$Eu@@MP^b1A)`;?=th8xI(8zBGk401DKu>u@tEAWW2W<%^a71V{s#(C_~=qk9nPUgS>KoeoRdQVTj{F4$2w|tj54<vKJR5KISeFaO_d(u`z&&4TiVMbT?41Kj2Gb4F$=5^D+pJKF^Y%F^m1rgR4I|9ALnd7$G^+b6YbMwU3&;CpkTf(fR{QAQEPwD$V1w4^SBn`b~PkW_UhWar}FuVY|jT(E^ytJhTAE+rg))wqZ`MHK0w&cI~nUG)oIrIAYn+oBwi#yy+9}YV<K_Pyqu@IB&w2G=5u-#&lL}ynkk~J;CoCyT26!Nq*ZlVx+{iyfmUnu<s~HlR<3d)G0crbB?+ET@fUgfuWyE`lipYZ``Wbbr<Y)AG60z|`sds1=Rx*+AF_fdL!{x<KYVXl?#vn7JR<)7E-u9=+b_~QCH98l<PEha_Ik~^cbSGyDO$x2;Em@E&2x@v2gFf<NGtbH!_NLX7rm<^A)ta+mex#!4AWen@)JNnh`yr7-g^w@MfH0b{jk!6pH?~tgY5?tffFj@!8m)4CUkKNi|T3B65X%Q9$u~S)IA>=QYdg1RUenSoNgI0Bz*#>mz2%bXy|DI>j#knm`F+zMFj<No#mO8saYeZmVTK4^7~B5G`vx?GbXr??~2~D#$C-e>>?*s`-q}IPR31!F#wYFRs1VcWOOMH2;YUeor)&_!>rHW0KLGa<7Mni4aUCYB}PnCooJJa@oiv?tID~_iWC^5!>kDDPGVdt$DlVI8BKIHqYip-+S`{6jBW2k_%R1g-Q}3kzhT%FQsqt$M6Dr#F-+Ud4zE!ct67YNQK=+q)ya&(r-oQ`8Qx+~RGnUkW2s++V>yP}MP$sF+m+0{KD?MG!Y9VEy;+cqIs5a3FAB6&)ml}>0cllLZ$whTh1Y876V>Q#^I{CSZd_j1jy&7PrC1QEed}(xKg_KMtVA1P<c6$>nb@zGz*Dh*1s|i%X?t#2UU{G{!wdAnNdEycLCKaT&zD}tj&46w?+K_x5_yWGqIO*-m24C;DCRYrbg_AV&1aQ(Hv*SY*^n(n;KW(ArM!Y(RFVK?xFCU(35>nw64jgz5xk*JTo9OYCHr$0k(cPDWC_Xp<%}~@ENX!DBn6goA@ZpW)zWQn{GO^K<WYccJi(FKT4IaKhjPYvsgFa<=7$|kwIN0Vu}Q*|NevrO?L5TMG$cq2niMQke4?p$CY*$Z>c~H?QNkcH;nBZ)IfaJlNI9zbqkvZpSD$2OnBvhf+PU+zGGsBMh6=dW1l;Ce6S}8aZupIC-;3Vbq7o*EG%;Z1tJ<UU3QFE?5||TcdSBvz0_i`7K54m+94Zf}?M8!siDY+jdv=6BCYEAua1A{9t?{-$i@0dQq_voFw~$}^(D)rsi0K+WlEA?OIfaKWFnx#;=F1(Yb<@ds!$+R+Oy=oN+&siKDkmeLf#_4f4kVcJOeHq}*O`~t!tPE5_~DZxJd1YO<^-b$I0TFZIH3JtgTn+ibt}p_k>hgS_Dcnw$-09@uKFQh5kc;Vdjt<T=$GdiY*8r^05t-EpFoP`D#N$OHB;{ptvO>u3e!+4F!XcvTI#mx2Pd@UF)0}9jmVML)P^Z2P~R0l1~%!06-tjFgnE)^bz~p<EKbnnt0g2jf}S}B7yjV7kBMXCXU4%r_6`s@Ybv$#gT4dIYV9FOuZ$649jGj;l2d<s=xE0XpM6gG#eJRDA9Ajd8Dtjno=NqFk%*o)QR6vinLCX_jHTFX#w@`De|*cpYS@)#$vx81)bI{rY7nn{1DzX9fyo8Vu$7HOX2Nr)vw3N$c6xlk1auN2L`))xD5kgvT$tS+G4nEv$djZmbOo1z2cB^)*BbqnB<0Ux{NvjnM|BE(e|#o8vozd6_6$GVXp|xml!ctUj7I92p3kJWGBBD>0{2K^SaQ^*$J$KiWM+LbtUZTFfKYnP53%gF3`OV6(w}WYOBGAO(vBom?_?Q-lBk-G=*-qoVl*%QUK*;P^PxG6MwE?-;!+jy6w5g+4S5iIgKUUq18!OGG%jf^4SNt(JP2Yp>sm9SC005I!`x-@1Dk2NABaA+j&puo|K<D;`Pz+xzVe&_=v}XXf+g|N*xre0ScF0Z1?T4R(<l!^jJpZIFr#=9d`|j+qYIdTR{Lu__wtR<GY^pCB6T^rnqyG|_aG%mL0PO9O}c_t;fQ4v9zBL56_vq*K3D$$ED5uG{$(34cVXq9g5zB&$Cic~C^i;6hI}~H7#0$cU=fumUiI<9l4F)z<ipYlTryB?F8o95F7_K)$i#LNm=$NH^EuN!6!}@BH%#&q7#1+tz1v8qL8p!JJ4hpA{}HMdf{~3+yIdh?$K*60U(<xYpi^Z{M|pjj!p2O$yb|7T@Pi@$km9KwL!W!Wp#jGV{ANHJ?;fA8WUD>z`|jF-SKwuqsj5Ch$hslQP>Wd$z$)IGv^i!fw{|izI9i3b*U9I#ne_N%TGf$j=sG4i14b^kJKaaSsqLu=PhBTzqf>Dx!k31#NTRBVvKBdR+l>0qZOjeRP!CxR$|cbNH((r73fId#>dMKS@m_`eGgySa+>?5&a~f9R$qtEh-An>l`&ni=rB{nFH-X^@i3Bj#(s{la?F}ou(YcebyP*hTg*jCaf#d5*rT~m?>0*J=b256M7ywe@G;@+fh#otxbi+=ErrmsuIFZz4P}?ZXpxtNe>_!|xJi=w@)c`T?2S#?3Ay-gm)0d2A(s+cyz{gIaR~9UOs4a(n`jPdoz?4e^-Z~@9hWdxqbJ2YR{&n-PJ>+1<Np!naDb;f_=Uir)?^q&MV_V4j0$uBup#O>9naJmOvOQ}_QUGbkSJ&(kY1oxk&&R~vV@O)gQ?rB#$9tB667Xy6{OIlo_H%uPC<Q?m#dJ#hEP$a!4^R^~yAl!h$H2ExX_B_^7_1pFE-UItbC^{hIeOmz`q$%QeNNShOFb=1Rl(xa+Yu!<+bl7;Kbv!Zru)bjy$6VT@3hUtbyQ+-@3M}a&5=A`9k!$TS5ct!9R^cTXuf$boqYfHF;h-kv_uKb#|@spsKakrXPKru!4@qGwM%uXX~00c2$Og234&?)3sU3-IqQ-JTl*n39t(!|J4h=d(tcZ<Gs)6+Z(8W3&><o>q$S*-WOv#G_VhF-TcYR`WPzfY0;7*8>!h?@(`Oe}WCDVJ;Q4@PK+JSln|8h~``p7d4SDI0VC2VZeVS5WqQMNg@ONvaL4-mKw{atmc^5s&3PY~jCl`nL4}5X?MQ3eDh8s`y(lopqr)l3$Na!9m076gouGMKhTl>ZRhvA=+EySg;wHi~nwv%j@1O&3=<$qk(W2IKPd0A0iNV5L5HgRreyJdA5CbKp(_mx)#Wt$-j3Fz{n<$ka$KIww>pdWn!e4K7m90#?k%Zit5GWW}H|02<CT=<kcU*X3ADd!X$2AJD0qIRx`6pS&t!t6ZZWWCL`^0}Tjp;~v{&YYj?5NFwg{idlD+4mA~YR)5fwfcX2`|YPczL_6>yaW68c>jNU|MlDN_^DK4q{G<ykJ6`MUB`^8K|N}jUpE0N?B9Xr+rk#KEBkNUgVM?5tTE4jkSc$!#GuC$|9AGL%C!RfxVSlz)^TlDhE=LrO3ztgydD4D>z)&4yDzzQfUU1*e>mg@HedZ;U;Z`lQ%J<|h^hE-y04?Lzrd~#@l^06|643iYPGk1IyJjw<Y#j1X>RcmCyL&DB+{RMfBF8W#}Y*NuWopCvX5ig`WpT-fH{+m8tV}E6g||A7msH=L<s1NgvG|GkDL7cUw-=im*0N+vDM!`!jjLu)#2Ble*gJg?K-NAvpIi+`SkY;@ApxQ+1*ebaI9fh*yUq!Y=$I`uEw)xxL5X&v4)QQ|NQHhUw{7JKR@}8e>tKf(1zGwJ5OzM?V~x&=SYic{XXrO{lsg<$;%~c_Qf(k-uFKwzC1m;WBX~X{QfPwrp<SNEs2T_jCznj7aktJAoF{n&l>9vo2f5<jvhWS8fVwu<?p<_=y-?Ed(&{g+jXUy1r!hg&!98PnV-WYL8cR_6%eLt7ToRUP?q>gpp!+U2_PMb`Em4j?LAr6o|OvvabgVRxNy<qDb;54l&`bwY9mHF$W;KHh;5yp1;$Hu{OVhrr+b~!B!apY9M!tD`?y8`JLfGT4J^@bFs}`O{KvJ(eIU>0d%W}?n3FYh#AozV#N%4!;twAXbZpvpQeSqxCiMufytoIS9!={v<~_n=RJ)$gg+N1_C25D|aD9y}!?4EiMw7|5N#C>f+4ufjuPtosp=au5)4<C`5r8Tp>O5+jjvnGfW9UeN3_#~n7MX%f!&ZC{(I<C^$5^V2$uTZQ<ET*JtLB7ki`wAdd^Xk9AX^<V+25CGmA5Pp@pbbcTcW=NTrI}l70GIi+nzrd>{}d~>92glAWNh+G)Gy2cCby!u)(TdxvbUT<EJNC0$&T*9QQf@x+_S-$^B+TNi^<}a1%f^5W(k@o=)eRV`=!w%}6cA+5hL?-rxT&q!N#5N3{sc1A@T+=aSz(oVbWBbX-nk?Rv-;r*5Nkh)r~UPK<YF!%aHoFg0YI)E%-(S8xDRG}~H=^FG#5mFbgGuXi$<`#SQ5Gwy**L+ufm4}B0y{~?96Q$r_c<Hg53D;y00`}<G?)!UthC}CksjX?(j{%2BK)KkLKIP|nB;e|z@)nE&}_k0>d#CDPg*#AfH;ZtzL7*{e_1w>5}>OP(4slhmbqK&MsO-uwE*)fi)7S+X$CT&Mpx?pN>7Eh%qr`Nh*)41ll?9^U4`_B5mFayKi`Z8MmaGD0le-`Qy3;h!|;V8;Dz2GID<b*AATO0{xgLZ$J12O5%)0f6onpo6p)uMZOKRbz@Ll_v-q_fW>^3+1VdDrEb)2?@XFf$zco1|7VWypOPAt5M2wCzFQ!)G-&#MK$X4F(<ODxMSWHg<>RL}ikeQdRa_KOsHMi<)E6l1sF@OR+Xrhh$zeeLqw=4Ps4O;~DPhat>^ZG7K%1amayY99fhP_dKR~&num1S{4~+wv1^GJ_&sNp-JB1zM{KD{p+`H|9lUVDd&?Ha-XCL;FP3S)sb>ehQ)hf>N&6Z-!U&DBI?FrCDpi<mX1kry*A?qgIzMXNNlAr$|TWc+dNrdl$(kt<XlteUx{itn3x?~#UB0v9A5A+?N0@BK)*o$h>dAf#KH0BCa;mJhIg}$f`?;<?u#G2MZdr<EQk8D6&TOwy9zYFwETPj$D8dAOYt9S=x1~M=lZaTEr9mnnCT+RW&|DNK70$k+;&17$VrdiGN?#N;M)U-fltf&+vb)ZyUsjC4*#2$Q7vLxm<#NJ_je)yQ8izP)z2wJS%UK-NXj#h59CKMhv(FQD+8H$V<g@PRdzN7)-WV7;0KeIkORF3)|XV;?i2CvxTmAoHUJ7Lr`cVWM0rioCS!77LTXW}s=bAEq6R2xQ{@x^K@w}9k4vnvcm>WsIkR)a)<|*w9=w8kYpDqh#>2(Rw8bc@&i3}i-mUukn5BmfD@5%z@7S~^Ez$BA1rUCsnC0#aE7eE)8yhh)wNS-Vq&?GVn!w-FFV}6<+mPB2>+FWr<S@wwd;{P2i5eW5P1&McL`uDc!nKfl%{3f--=zU#vaDiG;hS72NKoYcn>>*&MP{y9Ml%`a7li(jY1^J`8NJaJeF3T8)L{5<YDZ}z1p-DyW6OH1dnj*c9~j|si8c{#rhDw>p_iG`c6}g^$fT&50X{~g6GGc{w4)+`O$q@&1~W&?Bk!dqI2b=r&OVmNd<Vlr)Vsm+O10YLf!Drw2jEh;41t#Hh_RJ4888ovtPX3_8svSK3_Uo%YZS5qXV;ztJ5-RP^^)%Mp!<8#;RNBdg3}S6wt0xK=wVGwzCj^h2RVO-zc!E4voG=T+6Q<ZBV`z$5<4Oqb(<pRL}1Br>c<>b`RxYJ5JR>`N8HJO%?%w10bGNOEu-HHpQ&t`>KN}%6GL-~PEKdVraDw&D0JHJDFM4iPLFji@3|FgZR5ks)6esiz{`+?4(q0&d1rfMrzxQq1X99Jk}oqz-7&!0ktyQpJ?fezkD@LaM(MYCB*QRS-fKD6j$SqOt8T6Bd0u4e6X80Ze-P&gGD|hk5Kxv-<-(um@+6Nh;rf(##N1$&VzE_%#1WKj6fUv@Mm2}ZPoIfzD2+$7SFHP{So338b5CpdC;ry)ESpnMJR0q1IVBI8<YO*XmH>lH$4rkA^s=O?n{$JrVS<GuR}k5Cp^jj!Rmq9bffGpiGotKkz9RX+j_ogagD}xVrXF|qQTsAM21)$_yZE&{1NC*s%aS|jN0rC6uChF2gjIzqY511}oq=O`tz7TtEIsB1H|>sTI>H1_b5Fr;@2_g8PC%jcUO@j%h6cAq(O9dW&Bz;;@E7_)%c$li?bB~thJDDglD^wTO@Qkf;7#a2@4A#EH=~LK(r^F5#Hk-1%Vv?(Zs~dHL(%cpdDaKQr|&0-?9FZfLQ>=Ly9+C2j;Sz~8a#cV<ZjZztTvTl_Lv*CwLH^julgxOIm7lj9-y3#1#kMDmrahdy5xm?&`XOnRDIG`CGA22G53(KTwM#NC{JdduXvn^=ylGk!LZ_?!&tpU_4bDq5Te4hbjpi@G#{lL$rA*@bpIM+4@oo?UT<2-6X_zZK4AmK3K}i+F4+%1cm(}EUYcl)GBbJu=~>~vUO)-f=)EG_(4htoHtRYhP_JOuDVeBj;45Ii;i35yF8zuGT+2H~L8?g=*D&|Szv)#p>~D#3u@{}QtOC}37x$D^gzr2G%_*cta3UJ_%w8D<{G$Od>|+lGZyxNhAIUM3`<Q9*ibKydEkUGaB_{#)h}Q$$8!+&|DT9EhXo>o3Yx~-f%IZ|yq$=s}vOIn9`iJI*5i7dfFjK^~j#6+Nw)m?OI-lAV&;G{vislA=2PDk=yb{xE^0IjBcUlDrvTui9T82@T-P3TX3<pL3LPm?x>}BJ^0#Wm0wzHBsL`P<!tP*hx9P)Cdn!Fi=Ydy+PWGom5GH}{W+4|>Py3!!?>`}xPLQOhb0cqsH2CvV4j#Va?AlDyg5oU7GSG$1p-EeNYwD>s1aYot9*Llt*W_?4X0xXMW3)?2$s%WRj>1-o<xtI)YapyfoscPU15*_ilm+iK2;I9H4_c6pt&89Q<6vr0&S-aLN0Rt0q$O#YDmV&9f9u+`^CWrMr1R+5*bUhh0uw)(mxCAWr+Nab?>(urnLw{Qc*mw+d)pWy;=;5`NNr>#|S)oZe)=R*MV2-hkeVY*VOnGTtv2?G{Y?X#?jUip>=>^dWU2$?_RL5j0(a;&s7I3D#m)oWQq&BZ(lsnAvw`U)^CK~l5aCS*Y49hiN26aSIWgcZN)huUe2xD@@68#)vIR`yGN1^$}e$^ahNdPa2#o-|i8nK?L{M;kfF!r|wImg(pMadHfG0}PJK9YWXK7D(e=SAK)io~^+iMD1k2>UUxEpk?(=!`<=!xFGtCZ*C-$JqBo)|RJaTzA#0_{wb<EZbDdsEcQOaJW@M-wA{ZoxKjFp`Z(ayCQQQ^VC^Wt32$e=&Vr@`WH=Nzl>74A+q6&I7*Q#el*L<WF{5<w-mCrgs@+#As8;N1FU4hwU=Q@0&N`vdvc^$=Hu?exUWFIKykM}TlyXd_5C0^3~5GVSi}7Y?LDP#V|lQJvi>y2p@*AruC_xb*rbGEc}P_POUp?Icn2i<=w<Ewn_d$=W?nFb0$o_+b(u@ynrQ_iG_^Mj4Jvh#yBS0v2Few?HD#L|L4Xc{*|^kM?tIA6g!&~D#@0uxUvFM==$J|luJxGKc|46u8Xs|>%C4`{$9?sIYcC^hAdee;x2MO>p{suLrp9BY|3v&<*IbXfBdZ%CnRzmdb$)zy*ceDYSo~rpn3BCRK9vAKXDYw$q7)j#Hth`7;@W`%EO(Ufj>+V~$f91RDF4a@${EqU;v-(4@MFkRUsIVz=mQ~NLR_7TES4y;5EAPNpNeFT0MaXg?<&h8t3i8jR@Wm;0COyySaNZaSErB|>%x<yBI=rgQKPW#U`j%`EV~XFwk~4pAI=o?TW|AOqm(g_Vrku99qG;JO;`!_@gui$<Rx}(SaX1=nT*0}uPC$8#yQP78NbRo*}`OEP#st}zJihG(B8C3{U-BiHi*mUZN&qEDP?nNKc4ww^#v55IoNIR#Jlx|lE8R_KE1Nds<xN+oP@CqrDSs9FW{<0InAgF4im;<sn$ZA-2qnRp?G))E>E09f`<*3M&lkAYJFVgw)ANlnP}PdeQ>H%50uHXsEgc}ZO><*v)&c-Q&@gI1!2Cri+jXX5@4}Gb<yWShVF`r_b>a@C({-t2gzE)bYTw@^?eevj?fk4#+<#N5;r3M7jd)p+5t1hTsJPzTFGfDl0k4H=i|072?k%O3LLdAghY)Dpajj;F_Ts1u!Y1dk;-_Ew;I?r4cd+`e#qttgvYf~lgM1HX8wbs#vbe0+4_SA$Ybn(Zp#a4aZ7B~VF#)}<!loLNq7W{iv0#tV%)a4Is@lAKP%cu@o5Q;7rg{}jJ(hUZB0?PIL$V%i%DzP1i~pmIP6`>HfLJ_uJ1|{ajwFA7ulmEZF+>JBf^?^N%A`6+V`l`EVlzX!Dbi*)?x2%3c&H9uINk~6KR4}3$_mMPHh@8tkcf;fo)|YX_4c8K$bME^ogu3rL%hGGN;K42{hzNz&nq2a`s%CI);>RiLMG7Ffe$HCd|={eCa6l+Z7J*7^w_+$ih*_T(yBEh#%rtl)<>V5RO^CHzeB7U+}@+Qmi?3+%jc<oMhsyBfuTg^@D^Q#%&(cs0yY%*$mHO9(?TH|EVXWADk!O8ctIuXAtiai{Q0(EllgIb5O}tmTo{K=#mW;I{b6TL%ujUQqKvkk%lEw34uhvQRD!BNdh}vdY0?7J=dyYAGI$iO4X)~iIU+9=or5cMZpka$>g@chR|}73rx2;&pJIDr{;6Juta2t((QZ<c}{Td_m#9i$ggua?J>mKZF9nBf~tq4=+C_N<~py5dX|ff@bmH<AQWPhi-F<YkH)6f3@P#_+I3Bq$l<FxMjDlKSfztC@Y*-4Q*W@AOob+<)sz|fc*0oho;jViuzM!xmTh#+O<ofm6*ujx=G1FR2qbE)F%nUNoF6zw8A^*lKR7g2A<=uxppeR!Ne*#Yp46;-7g!Q|Qmuqgpq5of*-$J*xD%(F?s=T<Q&aX_Qy!Cm0<^*sLr*GjI@9uXP-%DogKmc&6~TKrVsT1p?BIwwrZnnjJO&W-^C<UM9O{&(7rOYE_2mTd$H0n8pw4>!eC{09t{TqzzW-I`$>5Dk#MWIRO7g26z_HU*H;oUOJiJ7be*Ym*{H4W>T+h}qnN20hi(XUARG#Q0P}DLM`obVxSoaK+7QPK&udoMVGtwehYvOZgx;z4|)5z{eyA`ZPhcpLDe>VLga9{2tMgD-jT<1?EN?s{IL=z*vrSxs<BD0S%fKafdJV%;VtKsyN_nFOoLd4wPqbRVCY^#H|MLO*ys|CqIp@H&E)c<fFcKFaf$e@{0jeVP7oJGk%J1}^G*<Kb|K0Kgj#ew!mj-^0iuTsn3b8rgR1aF(YLpCQRlAtD-=YqZ4WJ=MXGEdsSRivT^{j=Ww5~A9u5P(c9$8-^&D8(NL_PP#%i^m_)Or4%mB87q%_W_Tx)y)vz<02;p4)XQ)Px_hy)15c;{4YMj;_}AS0B3G^jo8AJ-hMgjz(sV?zp{q^i<)0;q*0`J{J~rMiXz`CS5JcuwAo3(eAY>wCMq{}<_Z|)sirbgide(4=f``{Y4zb3&H|PJSM)Ag31Q-=z1jwOf*9iI^mO>$m|7|<Y;m+t-Zsi!7R4PT8|9$kYimwmv{S+{ddS}5qZL4e;zbq+OHiF->x`D7k|E8wLzkX2-=%xX>ZXTJpauE5PwoG;sd)Q^q(N|ucnc;{6S)ZqoXH8e$rs@t7Yp0)B<89AX<tglP0OY8^9h?EMA_D`<0CadhYA6NA-YZ*G_Sgu*>v;~m32y(M5e##8uh)iO7t$I)I|x+^b)^W;;<x&RgvAIGA7>RE9<UDVX9jDZYTQZ=l<i{gE4J{x=t%|{8(7?hI-}lwF*_Q()-S4I%T54tHjZ!_U^s$;vU<+W0V~Pu#`6Pdj8JfmT5XT9pd^<RKT3}hN&m(-iLm9E-e@l{fj>1hUW>-AoXbWnlU%D0XAyT0OwTA7<W#QvH;ax_Hr;#>uRlfc*$I>B`0O#8@gs}4SnEw83te0^C#oov}L2+r>uOVmH0hR*(++>1O**p%fJBv-->J-AV{zK{w#dvHD5*g5fhIxmf<PlC_$W6%hWBym=xxk{NzBuTnSTkOo4-x$dqaNIjcbPaTz8R;T+_&h?n9^ZA?8fiDNXS2+t28EVgRKlh$#kMKcpU!MHSy?tnUzFuEt03W)x<nn7HKTx)`3j~lU?9N8Ago8ns=7pnsge;Jlu%?D5hz~=j_lOzul^`F{hSXH}#+mz1Prf(D5LU8&v8DdBhhGBynz;*TMgr4W=Zmaf0MmvP@I(O@E)e^-9EtN`X@uQnG4t)Y}vT7ml!gOGK*pT#Wu3#C*zJQE&6|trfwKa;3dD10&$aQ1djx=f#N&IWH^mAtEneclP1;rdvK@UUbZl&I>vFJOOOnjSM$m50MfdvSiKHrU}(y^CN@&cAy#+p#h3JPcu%{Rz+HQ=Ar<m}UZ<_?dkE$Mbe7ROTI$%mh_w?N*;J0DE?Kqp#}X!3&@BQRGm$8L4^Ihy09Cjes9mZU^VNxouEmH8a`{$z0jW4EZ8h1#P^mDE#EIY^3@Y3Qh5AgPC}rL<68N)PE}OyLeq<CEz_Naf)4<=E*;vIoxQfqBke@_(5oF=hBLIF&;Zy<1v3ko|aTVbpx#GR^<>`NHc<+=vmk&^bR}Hph}K-Cr;j)??UJ%x6Y4LlVJ9;exhNa&~!n<}gaXO^b|<`%sc^AMc8|8C*88U-51eH+|%C0U7|E(3>TZ;K0)u5<f89UW#%7jJCD>VlaayGDq|fJX-W&AvvVjF_^Ja&BcQJQ3498b4HmBHMewM&@P(s9)^uhfC)vgKgMw+fi};2&jxlXQxuvUMj7&^x%BnREC{{;wq2Iw0#2I^`?!j*A9r4G`Afr3l!f>(O2@8dm5*#6;ODVwW9u^tm>2z^q1VA6(mEVZ>E>whb4ba=_bGbpMB+}Rd+-?V*2h{60${x<Q<vMO)GzJYmm#5i&eTvK9Fhi?EG!d>77lsI(rCFe-PaV@o-w@oiEaCwmr3S$rOPL94F$ah?fB)_ywpTjpC0H%|IYd7U3k(`!YF_}T?{*@)OWyL5dn9nxi708Ouy!<4nc6!J_cp|mbkxCH|NnAa`fNR(akV`4F2_-_Z#y4+s8~N$_u(=ctO947IbNPMx_8bCiPzu;sHXiHsEYE=Fzl!GC2r&xFAYfmv_cM<V6ukG%w56rM1UR7uS{Obc<PDSyWA<vGbEIxlbF8&`F%p(^h4H%#cU>$<{PF-hEq8jqiT%_wY(_5=hGz@gsS58XREAz&yk~Fqla<x{B>xtX~Dw^mnwCMZnlE?mrCwR2K!%xSBA_2#&xPVD)U!^@qU$iNYNwf<f|?9~tiS`;9e|-JVI#+64sZwRNbytob+-5>PG#6f$9rVB;-T&1t$#F@zMcD1!0aeiBTbcLC{iMaiGSr$oi-&s}U#L&q@C6e$8S&TrYQ<OTiz<8$dDuY9(*C8^X5YAZ5j;v%*pG*ho@=frFlj$PmP$3y?ex8HvH<D2>6$AiCbm%8Wsuit(*KkwVp)@I&lGOph=HuhNaB}!meJTEh_txI!`!oEQWwHO;*@;vaB5;mb-Teu6)ulT02jMz1^Uy#?{`$Dv9s2~q+zq!bN{`vL$Umi=KBP3MAUlF8@Wy>%wvcBgJ35S0B)P^zF8ndw4m^4$55#nFIeMogjrAR*3Nfp2Q@v(0Kak?$55i=VM_u7a()-ZPXpMU-G>(BrD=O_R1FY`j!f!%MJ{k7B1HDz<LK0Vf=8iCK7Za)z-kV&11=AOCvzp>%|1!FyJ{;~a<e2-nz<~!g{MFdR%*UMP=&%EQqBY-2m<KuT&8oT^9J!?8~gy@VsY?@A(F*fX_b{TnFtk5tljgoi8j!WrD+eTioM$dPxiH;3{CA<OXAW41mtOFhWU3)H<CllN-8$cK8_}nL@n~ZVqe&SoYN1sEz9poC(uF1_<53qns)c@1(zx?*ouZMZOpYC-^<Gc0xC*?D;`?yA3md?{dL<geZVEAKzL>t$rjWP`Hp6tJK=41_>=S$JhcU-HS)ZznzevH%u2A5sWwb`Wh;SGE`Fs+-IcL0x3?RtuscKP~4a~O`shA&XmdZ8#mOIF}n`|Nvvu2;hhNa>@nU+eV0SnOtAyX`z`n_fzT?QaZRf#TlIrHp)G(t6T32ORq7y}4WD0`n!|5~&fb^4Ji3Nz-TF;)coJhW!bJ9pr*ZwGd^2_VM*tgBTPu?o%e!V%N2NQGtBih5k&egXs&cvN|{^1L*k$&n#Rf7I$HCnrb54BZObz2vkzUUR<{Q>kp}#amf+3$<xWr<jiCbX5&%+^Kb9(fB$?!_C;0Y&_Jg-_fS^)aVCDuVeMm-wbdRKszCk~oU-kS;wwnXgw0Fu3?|E0a+mp#AKSr@M~%H)^r)v>^nEvXYRHy86yXS@n<c{1!lv5n4opKYSPh`0rDQx#`FMwU8m4@a8Ke^_d4qFK1kqA|S?6HbH0A;A0?e;wG>6A<O60hM1p?<Zw8_ABS)btkB#?}$zp^!&3bn3OUzc4i|AdCn+i<b0kqab@oi6SCF%7elz*t&P7R)UPY0^i*pdV*~p5aX`*6|m#%fb>|^D(+T7X2_m`-}q{NWp6`6`&}lX6(-G4-q_+Du8x<DELIXiVfa|(oB#VI=DR;No7wT5dphaXr`E*#|u!|K3j;O4gH%d#1gj0P-nF!_d&!x!@%2)7$7;NboVqCJ$-2H(PO{AxpWmD6{G;85dzfnKty>b3kU%t_P+p&X-9YrWqDoIXL@bAVQQ#kKqZ6d$_7;+M$~9i81|uTqgD-lF<HtI8=;`vrf?4?+m*Qq)1VsX^DxQvFVDyGeHDv|ei~tNA9hqKL$5+qr_qr<1d9&OPT1(ml%%5?o*%D2wa{<gbvfp=_q4*>$CxE5Sj>AH#XR<m!usOCyJ;I-z=zLjLmua{4>uS{$g4d9f~xbmqjLi2K@*P&@7r^==MI8-c84ffhO!1;9m09->zM{o25bUpjc2&0%Q>(uEl3Csf8_O1Sy;zUnfK>PG0aI~3`w_7FQbY``A}4F;(v1(sxcJhuiw7?^Zfz%hh32K(JPZWmt<a?`cPFz-1=R#@Qpd0>N5X3=0%vf-Mmjpb@*_BnVwE%krL$??2^G(XE-+#ouZ_N;25Qx;^8Vqv=frW2vCywHnxg={G$P3amc#OPX%*8zd-*8EX+y}uH(;5UdK-j?`9nZAIA*c*G_tiet}(B&dAADU_2l2nlFSq=J95`Lu}KB8vNO6@VP#0Vv9#dIn_n3j0c^!ig*ifaIBZDmtoK2w+wPt3kVHahk;MadfeugAG_YKGBhotiruleL6A9OI}xB#n=eGr&lJMe!FhQm^+nV?tqETOJV;<99CYa1lLT9;jHE-ZILif5cBdYC&OdkTXV*OqGh{wi<TSgBo~)!j;S65E^4cHoX%jS47}7DVEr3JQdKF2neLgPXb*7}*>6x7ywnm_bd-w|Ot!0HY6m3m?!^h)BEYsb4x9absNU#@yQv6y_$EG!ji3TAa^+cg$d$colGl{rgTfYj87@1ngQzw!tMIbXq^O(3?w^46HYD28E8^V=k^$1`F-9(PMDckhC;yOfSusi3I<fy)jr5JMaiti|JX%-EnjhW`5AaW{Cr1UgEpj*NJ)!z@HVQ-2Av*VQY`bCK7NfC?wP@2&Ja2TFbuY}RyBbnY-R3Ge+Cxx5o9=o{#nSG>{wSc>?Vf^!mC}#$>&u{_kKxE5k^(SMt<{>N~g0dkA5lNS6d}8MYQO1ylHgaWgy3c6_2BCWeI+leEx2I!y9->B_u;QZM7eBNnW%tvQz72Prp0(G@Yt8iBz?y7?1%f?FjR&4=m|s=P8>1QVD%*3wp~#3jG}S_TRT`!n%W%cy3K@4-*aMMGT^!@xX|iCJfVXPemHU~TR@*n&4O)n{dZN^TbvW+vwj{X_$YQmlO`s@9kk1+mX)e+p*#?$m@jaM1Q5CY(`-;3f)hO0z*#p0uBeQ17qc~5hnh6Mbc<;2&FQmMUbM0uMeGT<9^KRxvwmwm<|M}-{j)0V`vjoB?3C|`MYY$(-m8lys-pymGTaL1rp))i&R06TNx<w_@(fLe<qB6OqhGMl2S-@c~a}WQ*Co0qNBcbe*2J+6l`6tKfF_+pUcVL@o0Ocg0ct};e<_1}zXdR$_s=%%bxn*mu8dCj8Rf%=dg^woEY|yJz{_-{$1G~Ij^R3Z-iWXO-@3Bj*KnHkznW7w6gAKtOU$0Ru&p=Y$HD$RZ^rOo2Uv;@0Sy3YfIC&0d-5UGzIVq2y#mxniHf08(Xbc4y<NhjAi@yH29?bDUBt5r44*SStlfs74_=RrQGNu^}tozPkM1s`u?X};tMCJt$nIF^Y0Fb)9!ndFj%4p7xe}=$d%_6CNjq}n6<bpmf8!FEd3E3xmj~k4N^>sit$k%IQey}i>8oa%r>g%gOQlM_k1TZ%Yig~i$UI9f2w1qufJRUkd8&2gqFPj|Jb*Z%YxQiC-rut~D4A6zKW{$c<Vi&`yrI4A6mFjt&^HeFUN8bW}Kfx$04p5cTk5QMLU(a%g8d(B?std7bgQf|P@_M5q(KB}Y(5+orqcn=%19&RPUyrYZOY>~-HpreZEzw_x1d0pncqX%oTPUs?DD`|rwrr~jlp*v4=zGo+W&E37`N95H=mDi2!uy`>DVqY{L=;C;1cdP5Hm;1lAPQE)mER4(>0t2YaSPi=9HY38nU0(|C`<Q|M=CX5G`#E7MvPW6@K+#QC0Y@Z1Q`qWx*F27==@`HG%{Vv(r)wv9x<sUA*bo}@|^z89<kJrqy)l!p&ZIZk(K<;IoI3%ENt@*$EOUVN(QDO?HGKI{)LPT*+Zm$4FvA9nw9htIvNY@h>x3hkXt8Jj?Ez4i&cgq!;^TqodyiLA<X$QWr!pjWtv3zgQv&HOowBL%OLl`lUr@Wnp9r$dfi=OQZRT<Qkl<rJ?$ZuArdHn-Onu7Vymqt7pF+b#z{{j<F=SQUvcL>MhQ*e1`+DtxasD$aNw_c1Xg97)SN3LdT>mipWA73Wnf@JrZM5W+4>}PRHLe#fW}_WL$JuSioA}+%ImBzCPrVBG0Fh;6i@9*hOVa&s&McBDq@G<%p*1^lMvI;vqF<OAUJcckKKf6?AwG05bY)Z#Co#A2vizoC<ed$kQk3S1PY!gLQl{9kSXLcXOuv|ck*6t8~jTBD90#wm<evrK6Fh4R5kW(?J1TJXO}@80aBSmI^+!H%;j4lw#KT-`TT=NW%C&H^c>sY7yDInlrR7U3RZj>k!6TgH|6JiHe#q0+L>l64Ud+@aKdDiiB>kJ2;sTKW3Y?7aTFeEEfeh_W4P*LV0$9x$Fmi#%jebBWPCkK#FP?d|ALfRSj?n&qNhRZrQw?j0Z$@L7V~yl2b(<XsNkou^7)5VBD;H6lr0pmy%f1RL=%uqlT#skN<k(|i07mVjN$S+_%s%vGGy8z8F&nR?JkpOy?-p7&?(E^5F)@zcqw~NozYxneB~LbwN0Q4iC~9}t4T{natopgS5#5)Uusds+hp+lt5Xx*IG%@(qAyr-b9w(lAsRTfDVW+MqrAnMH%eE!1w9*|quRN^16t}VBf@i(dVZ3gF<U9wh-2WrjD~?;ZS>uqejG-4S}J#3{}Vw_gJ=$WRUK8^5Ol~h65%^HL-Z_I>S89iCGZvYQ5LYG5*i+MsJMYdgFLo2#|{+0E~BhtOg;=oHud#xFmxKL^J`H~&d*yGSrGU!C+R`|WK&2mBg_R_a=x9Hu#`A<!VOSCB~9kI5!rTX$ss<BouUlC2(dShFVN-@RhBi%9Rd3I*5$y@5AyU_^F6Dj0Ftz_miRGc=u%NO7li^|cD6w}2JgF<h8GjHwkJJyimT%kpYQrc8%4Aie*CHze#>YVq1SHVm14$3L3=SK^_wZjV0otX1UYS+lg0MzFUyo7Ki@%Hf@sIhoR&^h=4s8gSrt_A-or52NBK?MLcX;XTa;Of>Ul727Z#l?Owk?S(x<j?9Rh%J27TlrD@3-5qHKFUDVFt>px41te!|Or8+{~ht+a<y9v(1Un6r4I*SIvuRti-UG(+%p;4JlSq_QswN;;|15g}KT9Bg37Q4=qx?vJYcNybHRBZ!x9Ki46X*xk>eU_?<!(FYD|&|h-4!~S59<MUiV#zo{pn7PEdnyflDrVjJ7Vmq{0pJ;;SKWeT;Z2++V8<*&IE+%q%v0Psb0kFJlmSX^gtWOpf`NKI~g?TOVdrNu`Ne63G9P~_m9dfM*R0_-{N1)kH)Q}y2tPXoO5)!+Ty5b&fvY^Qz56%v&t+hd++I$vc>a&@|B*Gx>ZD0waN}q??QYoruE_0eZZ;$m}kjh-RllN^aodVq=2Q|$kX&lMNK$nif5vRhX9lXMI4BKbxn9G{7MAt(D9*WUy#t@j?dqaf{dPsI-a}rM*Et=PH%Ouor_K{;@K_XITZdY@absANv3Jj8#0q)Fa$Hy*$HLTpOO;cy9JO{Z)$R;~;)9B+IOEQ%zS5s(T*F%c-7?TcIdX}2LHfpyS{0!(+3fZ{*tHPr%*EgHiNZ$w%fJ4H+C_aI|Bo+71QuZ<A?KyPt1u8IqQTDvXlEJB3xSuhnny_MS_rdfS?t&lz{y67Z=S|_9IWF)$QsY&D72|n-=Q+W>+gCjNAivJRV#g3`w}}ZKGRheq{x*nn!0^{Z;@z!5D|)ql!ix3Lp9f)6OBoc15bd!hJ>XDb93$OjId~gNvkocyAayFw)R03qbx6bZK$?OK7TR})8%TR}@3>Rd7Y|1swh{`ACZl%WrAda!k|Z@aED<chO{r%6earrbX8Yy<8*2!j4;s!I4O25RU<}*@dhDwB`<ReN(y;PU_pz9Nx{op>k%zHZ_#B0lzHwV}IEUGsvkB*^iAh|Z)UbLNNVj^D_}T?>dwXkHb(jb(=7;-thIgJ_bzP9M=X!gXL<r!4l(;d(WX+{oSL>iMVgSm+4!sfrSa76+l!WckA8<@*)bBxD^zSFW?5}s#DbMtAi9PCTBFtJ;f?L)p<g-?=Cbw{s_wBB7hdS@hAm;CqSRlU|1;Ya7>oj_?-Z)VPmvPB*o1s&71ZQ{cE^0|+y!RghC<3kc=KDVW+uA_&35`~?+?X0Sfrs}BCMoxh2~IaIY~3@cT=>X=-NO!;tpTMSsbDru`$E7W7(Hdt1_tXAz7YDPkJ*j!UfsuxoE>`w&!0+EnJGI_7-dnH@IFzQ-G~VT1e>bI+u%}09dOa~k9p30@|xVGrO3Jn2o{x>qMg&p?O4TD7R?Jp7<AFM`vgLN<3SwAlveH21|RJxL8Gx>&rXeY#7PZeHN()7TpHduT0AAE9=T_U31AKm=$c@XviHm;aYYu!eopq<@ZU39!*sPWje;eKJm=INlL+CKl!9BPx?=KSEx=K%?pf9VSO8duz=`B9aRzcjg~^+xNTq6)b1tK7#xs=FIKzu^u;Q-y*QOC+po}sUU&6}g3f&*skYl7N=<aEX&i~?@D;^f<O59G%Sw31L#wKNz<a85P*F^s+o&SrvR$c3JT2TsDK^A=tj>(eG8$Dd~uK+2mGWsLTHQ+?yC(gs^R&$d+9#p}yjezdGeAC|jC~cvp9EFDiGB>kMdQ0R4z=QZl80i&~$Es_HPx*KcdiOqjghN37;L3){m%!iQ^9|evd4hOL!^UCYX9}skuxZv>j%}13e2NE4wqC-Qsf7!G(M|~$9Yy5W`*WC>!bLtUkUQMYAU=Y1&{`J^D?6#{>ZS+npw0fe@a_M##V-4W6r>*`-gt1g)kK0!0_AhIY4Sz*$4Ovc+`#^rW}fGs_TpuH`CP$_Huv--c(*k=s<{C=bRQtz)y21<y_A!@+ot0_sd`Vs#xY4kQE25p{Jpb0`z{oPM6to-%2x#N5i{23xl}}#sB(w*$jXA)QDQ_**0+68e}3*izCGC3MyBaBKF5!RfD|Y#E#J0K1Szxcb2QT_6P91qdp5O=`Hh#^)7y6+d<U;9C9k|5%QN}F@*fV%LUMyFMhfwe*1ZqI_IyH`ao`i%`G5k0N09nCd(BuI+VUTD@PT6*rm~-#;v3~;th?;|V5H^MT50V7&iC41eWEO}uNhlI-+f*j#J93(d{Sk*Oe)0y59m&AX%i*ty9CumVzj^k0pE&@7$7*W`~EC$?KNMirH|XNm*FXfF+qt_%QP;-nAD=0{Fp!B35BV~6#nLuC{&rIpNg8edf_rmYR^fKs*+UE6<!PBI=u1oHmh>)uxv!ph!mH|Gl_cMaB1jFh)6usB9DoXiL|qt7+i*2YnWqx8-11>D;r3Ms_8=3r~z>gjfcMsORr`FsB6UKps&cCcrWe+)v^q$YAA5u=sDZ;^<sMpj^ieSeMufM>^KHE#6D@v^E}<{@t(+BhxmEtvO!68T2x3YnC5TNIP{62$;y4e3)8z+`cPIZEotUI_C;j0@so9ZslBRf%n5)5xo%9~@Y$%TM$0~DmYqp{Tk3}ZDVa%X*p{!TF)x^Q(RVJH4>w7V#|y^;3lKV8!B|}_iY7OE#*fQb6QWl^=`7-e2U)F$M=@zf0<UE|=eMLg%2^ys#TOrb&fbJpq=pMIr4MtW|Bog<m>~l51oL|i)jdZO-SiAVj0TkCI61jvg!P`!f$vWiH^R<t#>F6G?kzwQke@Bn&{4lYN*h^AY0=_TtIA86!X28%C)0<JTgT~;v(puV9B4Yg98u2ynByd-3m*oiQs$yJOG^c^AJ<(?l-!x-|N4aCHOOofd0Q}`(DL~_IFSjCzTuAIrQs3tQ=Abuoy56RxU6d=al5=cnK-&hMhEG>OpA<+`%p4;AMc938eB**>v*@5tB&cr;=UjZA;^uo01GXXBkXB)_w<<Wrtg$oga;Tf^lk$ZX?X0bvK+^BLgpfdUQBTYfq8&;QI$t_uhJY59r2*rN6*AKJ0H@x%wwnUlWoI62|K7p8fAj`q7%1!?owjtVUOxW=Cn7Dg;zHrMv{V@XT8q~yX7fPYK}u~tbZzZf1i*b8-+{_$rl3u*GACbhlGUH?xx@y7QQTQiZLm7HI~U@o;-@TUcwn@&5M2#(c@!Y+YbNUZ_ezP>U}3ynf43{p9HU}$fKR_7CuJ5_31=_)Pru=g6K2elPTJhJxU^J1q4P@9t6RH-BhpIZBAv-v%FLi58`ZT)*_gyn6H>TUaF;`Mr6{)skRNaeYAAqmL$t0Q_#~D6=>*!{uMA2_dJoCQgXruJmRIQqwsxlDZ#<g7g_4^L$X(df89xD2}YJJbxm}H>&cwx-$5l&>zuxiJB;s{F;!Zk+3y1brnL0BeftL!^)a>exlZ5wS8<`upOfkQgc`R?+^w(s9GUiJUoa|;h=*aYuJZMp_v`fi+s8~NO5MI>sN27axqWHc`K9z&tnRcVRHS6U5D2>lT-R#$WO90D;DRU(o!%J(xdjSRq?H=BF0Juy+B&aX^jkt_f@Z|P1A2bar6OX(YdVS3+-+5ULPIf@Cwo=tc=v5Vh5q}!50w*{2o_03e`NGk?i*rWm(5(G`E}X(A1kni04wJ4GGg{mD!3EHi3A)Y3fjVZ=sp3_Y>L-s>=*``B0j6QTnT1sbB>o@h##NJk~|YIh}9f{N}(RwicA>?lC22M+3Uh`N`ex;;rsr0NB;Qs+fRRdGe7+JI`7-168!$_x8Kdr|5!uClQ?qj*KZnk<XH1fr8K#JVQ-E_MC)Jl-!fD~H^=JFKfitd%VP;t;2Z#auUj-W(U91|!CDg-SFetlK1R1?m_u2^w0{pxh&$FH=2Cj-DqWmQttS^Lg6s1$7?14d`}Md_-~Z*$pzi1UGxyW)zx?*o_doL2Z{Pm;9%=!d`_RyP+Z73`lSyOtc#dvE73+DzTqad1_V{4NV@1AW<9e`1$B@F<<bVG4%dbEG?_a(h28@m8Zsl&j^XK>f_*dh^Hoz8p0g7sEKTWFr)0p^=1C8DE$JkJggE1W=_}n#3^3E>P<6_IEs^Jc|<5N_2UH#O@nF$B01w8^a#j!>#VIX<Pq)*Q5(Zgp2aS^~*jScfP{G;YxJZ_#&4I+9{&N6c9iLoI|wyVoKoQ39ZX_UOdd0e84&TARiqc^`Jko}Fz5?^n0yd<gvMjC+ru6$aT^>q}5ejY-$K})ZOVz>L)63F^$742Zwh$k>U^Oper?%Dk1+sEgMtWz4Tua{IQX_b9d*CH#U=Detcr9;m&drve-;xWG}r-S%_pj#ug%b`oLhKL97zOmel#3W*h1mukBX*8RT{PPc8{jl>Mo&Q3;QnqZ{vt+|oYRCrHX)YGfoj%5-mtwcMzlshfZ*1r&Mg1=d%(NUC{?nB6P0sb&^il|HXk@5{pr)A_W#sUahN8wv;3!Q;5o+9I8eLw5M|pdquyuU+ro&7)*}bPzD_eqwJWkpO_APG7{R6R&uc{LJJOOqiLdq_Bg#!oYCFC9V^;v?%232n|x|a`)TO!LMLr+a^qG~a(<3IoQ{{DA4H`P?3Y=OdJ7Eyig+=<(V6W64Lbf|3(<F0$>3AwJYnaWPAHQQ1`;l~`NVbFOntq%nbphwJ~8Plke(=grf$Ck01V9I^HI24>aC)1FSu1P#(ylSn)BU3{^V&jp=<Q^Oift+Ye2)BWZp%VqFGI&UcqdpkCR|c4x$|pjvnql$QUR_pT8Y6@w`m2PgAEcXNC59uin;Jp~kTOT)E>8Z%y<BW$$2f{Q4uwaPF+R!guVY{}c!TH}pdi6CB(0odTK;{>ASXREH7o+wGz-N-*LPw^+i=P0)uYx8(aK7b?O?ag19D0fDyn=pR{CL|Mm14pU+l2sK+@h+{oHAq(nAGK5Js!qpS;F6WL7efZvqk<Q60@CmdKQa>={4CzV~$HS)(5NcO>MRnnp))6xPcFncNnV2tIsPVb+{@*x5*`zuj{yc!g)06Aa9>Bo!j2nU{QwrGq4xCNfx+Okl-1-J5ysYrX<u<lTNS^CG(y^OhF%0*Bw(IpQm&{h)ddcz-TMlX0l+`6|P|3p?fcJ7rYMVIPXbLi}&hlsYg!=iw`pIu{OT;9o(cyav|d=FmKT=NT>Yzhhp62i6TZi$I;Gsu%QhzYr`P80?aP=4Dvj5={q$tLYf!rUKWv1O^4wvq17b0Xw!j3ZBL-6?+5PE?kA;E&2s^Iy=PBPx$Zoj8=j65yX4I79ijqvx-sNWOLi+`ml*D9<kR{!?Vw*K~WnoqrnGmhV^ybT8e82tDw0|;8h<nZbk7Q?UYnYf6ikWR2&<Up0I=G+hhIrN7^zUrkBy3n3hqkxLJ6FpDKkXDnPb0Ux=l;DMY`4b1y*gnWN~*zFE7w1U#*Qv2%dfGw#sKdXSCMJ*&+l`_HJ}pKyOe9C?@|3-PGavLwo5q-o4P%U{-{@YVspy<d?nNbu9Dehimat~n(g?FAN3jpVv@u<t=Kr0s2qu?*8pQ^@h_?-3tq_uj4g`!BKvJp#LUU907k@7S~^{n5%r2aszFQ0F_tO7PMC#-_}l+BT%7X5Hej4l6Tu14H8`UgYUb&x_nb+%`MCejBpt9oQyrHxKxZLY!vNK$@57ObH5d@<d7x`VaZZ{9pb35TNx_q+R;;X|ZijHW}84L?O;0p&v9>G=AgHYN{e7`k^!;(l#J-42<_WH$p}qX(<!nO?y9S?uSDZp1L*jQ2VSFaC0L=MoTprn>7!M42QPCC3^$xZYYN!WXvT3JS+_MDI>rjLWH<{6oF8Vf|wAj-#ktk>xWFh`dVu^H)t9V9NXZ8Qh9&}5Q^!MCYobpDFsumUPmV(*hT8RAH!W`VJbjH!@z)=9F)Bh4NU>TqJpFzqXCH^7INwMlE|DJ4GC~+VzV4&VX1{v_un_nQv#6+(24e`zDK7nM>Ad6H#*n^vVnxe3{+1udiKONU>b|if-Q=&K$xiIMy^yNxB!5V`Sd1g5q*CitfU=*+L1e;y&m!zNZzb@QhD7$n8ur(fQ3su>GLeJf9Age846kiyV%otk?rZ1M_uzAfiIcZJ$%y%Ll+nN)nthCoF3CT)h)+m$FLTfavnkQT%D9Ms3?0#q-6;-SP?{dppIe9Jw213@JQ#ahiV{pz==j?N{VyLrFQWa+tzQu$K|>VsugW;5(-r@KyyW=T}Uq5r?sJ7jYx+XF?Z+(Aj)MnCv|xn5QSY{PL<rqUPOy4as$|<u2pyZcrH)|TkGvWfd0<SInOmrgs{MhQ}Xz58^tZCx&nYq)*NG)Jjc3jjZykMXgD?@d2LJp5CTUU>tV;(LMN>C{_+-)d5IvCw$B6b2~b#(Ag%c5RIFK+&~i?t12G9?m>yF$P@8FXTo?ohXcmUNrl)7H^uf4Po<OjRbmD#vOmMy$G=+T~Kw;9?YNEhUb6df6Tc2dn>lHPEz)mj6PT52!9^$SMTj2H81r6sRY>Z|>v7t_e@h;=yeU?*1jH?keTo=QsXb?PXJ{563<?Ed1Z?;Y|>ZP_j%Dh}vLiQMS$$71C$$j-TPHoOA5XbOBPmjbM;k~B?xRkcn=`}T2mH>3FcOVjt$q!F<1gvJ1!_evePNm=LeUs2)PD9h&5D!I15h=tZIAa2HKz95P+n`2!8)Wa9LKLoZ19cZ>36dGgttKFYPgJRN?iS>)F;BIjUv+4(^QyYX`sB_hbQ93|qZkIk2Wfmjd$AO>g}u25*<k!TFm^yo68J$k=JM0;-^WZVOx#GBZU>Lp_PrQ&pNN{qf>%3`je430+S7cbGIYmuBAN<KeJbcVf~tAZ1}B6K8ymNW{zR0_z>YD|)?{0(>4lT&tR49}aJ>3%6gU9Uvw6SdTgsNg3=%talm^()Y(JusOE3-dvyK(pgWE%LPpppmm@2!7>5<=Q3HIY6Kp93=ibVs5GQ=tU3mNg6I|bS?hp9st98+<dQ?kURPoL*IJXZ_uesS$U8D=Ft>QCg|*OCod?i8IwZN6l7MMev9R1BwflwF3LUtNY8CUB5-QxoZDB*x4k;nw?MmhV?a=9D1j%VsxHd3HCPd*}K0GOV2vflrDXKBJNtXJ|?b3~gL@nw0n&^}jN7A<%8E8r)2nqA#j0U>yC;=E*MZG{>lz0-_&lN?ElIt`qpHpl){zaZ>T?jQYhf=<jZ3t#tvxz=XO-B6hP-0!kbc70`t`=z1Q4P$(99`iep<HSxY~DOl{N6w-rpuqPSDYC?j7hyRzBzyW&#M>VZXLMDTr6`Gj_DH-?r*iD$mzD<a_F1*@?2>nnv!b$@RW!P`cXXb!Kc%lf2H}kHh5)GY^gaMDx^FM6POX_$#Mw#Mw(WJf;=|c7Xhk<*Uc9`U9FER8KHP%k30pDIn3Fvwm)RERI^O&c{6?tewJfGG1!rWVBo;uk^|2_WST=G0XEW1h6Yh4KK9OwU!!A3;xRBIVnS&g8dbzs~ERz_Wv;Df`a5}Gx@yG)bC@Zwh~NiA%VqK!Fx&^5_*QkGKWnjK9qGNm_#nJa~eEg@W&DtLu2M+503+*~9+_k8OFnis>lX-ln+@`RcEBz$_a!pFxX*Y2{R)_Tk0>ibLM+ObHA*9E+kviH=u%?-zvz<Lc1A}P|!I75dzgpSMNlulIHp0q@*S`kX*O6w$}_eBT-%Fvl7#Pb6&ltGCDkLl>mNjdsMKU>WR%>tZvV-Suh<PcVmL1=^P3sa|v(^2abR8_>T7NGW0YzE?u(RbC9tO!Uvt=%yx?l1l){OwR&R?~Y7VZw^0ng;kbP^rswGSWRj89GLBGx<q(2};fdzRjfp{abr$T_&0GpVD<kl(MD4&&&Nt43o+LF&c~@=iDxlb1UT367MsKL$7F_IZkU{y^m#))k?hwpz9?g*f8eWEjgdnOHoR^UExWRab(wAaU-Vd)Wk!~CA$v7=_CA^(DT_Wq~w^-8sV{kgv5nUFa>>PTpz4@Vm`9bA3f$$GSny_8N{?AftSrv0>_Bfj4R`1;>8rFCB^7LhFmK58*M(*{Fm{o{Fg1vbOHLY$Jch@rD4X;!{Ndz-;SaTK-<~MHmf>2-UAT2@|4!dtySB*uvNu!I{5n_uBR7P<4@L93os^ZTl&OFSdZ200u#gR8d?K~hZH+V+n&$<W!(z+K(pLt>XEx%^V_WUsZX*97w$j|0Hy&E^-uKDmsaYQq1FWH9qj3GO$E2~urCSzMONIvQiW99M`A|=Lyr2<xzI!??3yD&1viB}tkq2pwJNqIvIpH1Zhu-22dWCu+_I3=Jrpkj-9nyU#Tdq15I5<ONqAhx`(1}o=4XsEk<n@NX_Hi^@o)~=7S&;XR;i1Y!xO+s{-d<&a!jSrlu}JmR2FmAr`I~fHG~8!Qs!?F)32W&%R(qWQ{2J47TFykO(cW{AZnNMUc5Tw8cwLNAiw82NnhxR*9K^tK~Z8@SvV$EOcc{fLD+h&0oPEPnNf_|<Z9C5#%(Mt)l|8CZ7{I%nai9e&*^2wAyT^xck;e%C4|N5m{aQiGH5Dg6+8yI_H~t`)23_zaz{4Lmfd?dY_QdlDcoqizK&Za#f8In4p0R?iZ0k7q!VxRm_}9W<;ng=78BrjCqsf>r>T>ALx;d{f-tv(NU3b_&eS?px!^%t$R3iW$0%bFU4LzIh_KqAb~Df&&;%9o@cUPV2Xn5|Glg|y%39>c_d)sI1<=wE`55x{9P;&oBALG^p<QET?^N;KPhwN)W|95kw!o{c9HbK1b!PMib2xe6KWp8lnva4=rRqE<=(zjpdmrT2IZo{uV(m6D;X_7gy;9^zu6H$WYE^@x38KZ*)I1z6<YS~!rW`#!eg_<@PIf9e)sWmcwfi~^7SEiDZ|3Qpg@VvQ^G%~IYqEOasJLm+4g!ZWp;SU*dFWh*_bcT1jhi2%L^C;H%aaOQ?*hG7UsliU`Kx8si^sGA8m{>1VS3JxYX!@mYj|L~C4eYXVgm5<c24RZfgfufR004X=G&pF0tuK{&P~eBT&FbZhdwTV_EUvEmF+%&l*f#wJR`uxKdP_sg6o{50hnVg1nF0bLpJAJhCqs!yS=rjG{meY#_#E8{Z9ft)G^2^_wTwwf02Q|M0n&^dpP;dX{_DpZV*(ErV>z9r8NZKdGH_G2IWjBlp<F_ZcloPx>g8)#&e69@O0z)HCX7N$vJu#qM728iJn$PQ=l#~lLn)P52nJibt)yk<FYQH5qOXuF^Oj){T+aD6IW(eQ3UrR6?&{>ZFzfA@pNFG*SL)$4Jssk+K**Ta9vm@)&|}p`<3&El0DjF(x`O8)&|}xV`c;>s!Iq^p>(@4=?2pr^5Dp|QGK_M2ef&5u9<^5650S~l(vpC+ATwAiwiCo*~7cP{PVk}U@+(XI{%9grntNsg6CrG&wSPzaWE(igK`kZrRdPV#$AN>nJoEm=4_4lqWu0U7fu4;`s~EB7Lx9IH=;j%sg#a#kn@Im7#~mIIJwD!b(aY?Jxn_hiVS)hKix4!lm%skH=R}zw3J-u(f(hX!?9naaNczjI&C9|*(HnxZyNbR@}{@FGwJd!L~q<FNc%4eJv!wO^&sfF05WqS#M}Nbzdt|jAKxAhPs6Bw8vWzP!u&7POpqzcIl(toP<pd{=fOm$%u9ZyMc!1X^czq4uy^kguI*v=OkhL4rUo7l-|3$)B0}!-AHyvAO@=~TJ>e83m5Vy?;Q^tc)-KcD;!4%^I%!pG=X>b*kb$q61MgExhGh_Jt$+NakllMDWRI3{29W5~eM?^!kpnb9O_J*aHopCq(5GDY{n`4&3%-i6G^2494@0&LPqm&lz>POhyXtl0mtjm6C?-GM6%b}XKVBnJQ)U&4HZQ}ZA~CoS4}0!hB}CYtpv@kgwR1|VIwf2nI%6zae4)Ca3J~%>+D)#(c+tR{fXK5TXql*trSi|0@;pxC(8p#gQ!oSTsY3{Qa?gR6yfkdzK^Q=(6{#2F3*ou1z8UJA87fmavY^_a*)hT8j9+&)t)dfR<{~NUay}kA-q;3Sd7lXBd>P;3CAl|T-R8cefpp9fp$y9pKWF!!Ozw0(hiD%Yh#l&aGRkx?8EF#NW|s63-E?OyPQpu6+J3jCK(V<@<C75r1a>>90J|k!N?s=Ojlpf_-puDzCox8N7@yh}Zf?Kk{|7%FYtHWH+~)t*AmQo+HEir{;{1!r^B|>!lf7Q1Duyjl*OP?iFR`BG3qVVg3*0#7yy%ixJ|7%)76dW#l86!RmwS~*ZW#k@<~WFCT)qK)yjzF(m<*Lvh#E5u6X&2qj67>dN}<ycJ5%$zs2q&T9O349f2m)4AaR=4bG0=30y=e`1q`5g5wdZMI?{4{G0!?Q0$1o$P3fG6TcD{vMlF!a0h$UHhys6zD1B18io5T840h3%7#Rp-(K?(Psa@h;tmlsLyvk(YkkBYFcw%FC>`+<g`)RS~t&a@_`17I;PfEAIvKO=6*rNzcOTVy=`@r*$EP%C~jUEQ0E_XQN1N0?(acMH<7~dpwk<%<gq6d!#fgv_4D3>m!CO~F-d?Bk?=DM+$vg$F=Yrg7e)UbtlFQ`SHOatL1Ss)RRK-WKEHb<|BH=Vl^0|0d!ADt>kBO~qh4#Qxw49z$1cjo)IkC}3DrX|y&{#707%Ub04qeV1YKNuoF7(b9*lT?-XB1FGzd%{dHzn-QO0dudao;%sJZhVUNqH|nA)XGCFjc|qbi_0%MvnMRoKc>3xOE}pJ)^0zm#36qp<DioEQm8)OQ-(7vG+X@93zIKvSW;vD3F|Vyf9u}XgjgdbwI6`D@>EXX6t9oKF$^?Cd}nc98O+p%z874|kI$tipz_(?mZaL(A-y6~#>b-4jx6~jhk7wA+c90=Z}R7N|M>RXPk($fKYZ!+*&Z+1Z|}c;``!Hf4Ph)i!w25mH#DD?b#1Dnz_O~Z7^=l<#1G7)5}t_ELbvPpZ(Ql})Jii|u;(RBb^W&gJNqG^#2<P9&1>QM*sb%?E{@&5``;8^<95byKhT1`YBQc+_#9DKqyHKZaC(bw<z#b|A^(S#KLi|DcUY+WKJZ)J*Zk^zo2~F9ez{YE7vR6eETwj03mibQQuYfL%{X6(4zBU}KfwglFEmM;KR<8({!wEI-on>mL22MWmMznSZ*!xxxa(ED#)f2tC_?9+b1DLKCK>+n?IVMD#L?T~u#a_8skwiAY@{Y{t9rx(4~Bc~TN-QV=l;*Xe);w1|NZlm|M-`Q9qhpF*UtXhY4)1qFBZecTGV#R&#P}g5jRt}8PO-jtH*{)1&sB4j*sovI9BbNHs1kvDr!Py%B6(P_Tf>G_$BTuv%@Z#%b%l%PZuS1uf1C<U`XHQ-ZV@fc3pY<4#N^eg?5wr_0Qo_da4~!0!71gT^qE=hJ*uN33Rfg)-%=(hW@U-C(Dy{A&78{IU2_0Nvc|7?YrOnWmh?>+Ci>Suer>ObPD{nxzeA0|K+!zem(5v{dBKW8t$yu*<}g$V=NI%tn(HT;=1TJSXc(?f@4$7VQktt|0-dL(VVQI^PDT1B^}o)7YF!&pku>8TYTB|n#ChK)Wtpc^k`bYG4Bx`quTYX8zq_Zhh|4~`{+hxQX~+ixmDYI=~?^idw;H1qdrN=y0N2+UoL=j&2v?sM{S$sdM!+#GFe3w8Fwya<Q$VmjmA0PP)zU5-6EfuF9{c|h$y4RrV=eppM8rPCVw0DCs<mM3ue5ZPLaNGA72mAiIG|3{wyKtYrz*|NbLYFsRE;zdRlLfAuT~#gHmD|TJ8rJV(3DAgdMb#o9kGN8~M+_y}$qcA&TeOoCbAZ^N|)v3+Qm}OMd%s;(SQ7jVML3>%l~V12s%?+ljSDleu_TCWEOV0-z7AP3M6F=y6g$kvzMPH3FM5+C=MO-U%k}>nKxtfX?@6NKknuURo+oE(J?d)01x_k;e=k91X!<`K4jikD7)k6t>+#0h$p1GpXk2$;N36{b|y$&@3zhfdyOOrSqq8%oo%|RZ!N%dVF|<vu0R5unHiZ7x&Me=cxgcfO3GUki<*`8`&|AsutEn@NcrM7(A|1Q}uo-0rp~r)u|~7gQO0jFb_O1`_3|&7;E@jUq-7;P167cm{M|*vIc`FSpR~Tc#>0r%x%FCt@~rtY}qS@J<EDRmk5)ltn@0V=w9B>PS|e7L<^#Hrq5sS)Iz^`*X5Ygt|O?K8IJu;5_?Yb*fR?2U4ry>%Rdc1Jj@zt6no(YYx+iM)}h87niDlITBJ)zk2|T(Y3|?zWOs<x4Ou;)aY*L%S<!Z@g29YuxTniGuq{nU4GzDTd1_r+$nx*_PV@d;Rx0D`+D|W|TAce(Sa9Qii+Ch1HubOHzWwt(OsAZWUYXRnaHcH&6;!p?&`3^>#d~AwIj{NOF)v^X!bq&tjA%1wt?lV`6kGC-!7dr>8Mada?O2S)Zyqf$%1y<papq&6^*)FZ{2u73?9YrXXqt)K%zJY81`S<M`5mWmAAZ3%BGtWy<3ZstRUG1c{(VUP2!>6U3H<{7Bar)3lV!a9xyfr2s-bDBqu}D1p@VzD=dal--gLoMU_AYoDsUIl%If_eZ%>yfr6$C_w#ad=Pk88&B+67nYsfeuxyU<n>+OU%Mv@-CM$?Oc5D_)D^_TdxY`|e|`LXMqS(!!|%cxdyErJBL)%rUT;FFp!#PaVH0vN%05diee;q?R|><hL8B%XnhaBxC1?!?Sy1si?^hO$7hiK>BtcsNp-%<p^u=N|s-`s-oJ@Xf6;orZW>5*0_%cWqssSgJnqeWR3+hg?CNgj0jlwDklkj7GALpAS%Y<s01klXE?{uu%!KVasP{n7!MU)68&5HFYB&y`@kUC3o|fq5g()f+@hX9hK4Ai{G(nP41?Zl?o8_s2&mR48t=-`x~1zGPRIBOXPWpc*7YtTjFxvM!gNG4Y3Y!SaO#MsgaVdm+MkDWeYV;Gc<h^)5c}tKHd|mCR2ljWU1G86x=k6Mtjg-p!P{7QhMOBl4PK`A3}S_v~5pzE{^LLu^3H?G}njH%Luq@;W_oHJo_$-J47Ya4n-cgneMThhoVXuhu%u)*HA%YUE!deLG3eK0R0i!GFl*uwLjkIG!|K5(8kQ{VX*rXpW%53DU^vE35)JQs?p15&x7tKM28auW(o*KFp2XJ0lmXAm41W#fLtJWybZTOOm$fB<+X-;ZeUXY!({_P{}|y%9A;(3fP{m<k2$Qe%?C=+3^p3-LE_xX9I`8b_rw+=P_-h!2`3XC^SOdMO)<<Vad4eJ68WN>>(V#jQv%bB(g)TlxyR%ZsW_r9CZkP&QAi?ywW`pZraiI^y34|(VE3)8A{CtuhF3cVSUWNdNTMdcX33*CPbxb<CGO-NaE=rF7+CFS%6bh4FY|ZiMYcY&^hWoCI7fI?rY;LnsDuHN%NmB>z{+08P>FDEfIu*43s?^&%2o-fbiVnwp_M`HUVucEmVJcPOcZN=3~TP`==}t@I-VtzT>+f0dTTh9Yd+>uyI9<9zdzu+1dSr8%GuliR1^w#fL4p_x{!ai)~aDQk0|6AS%3IwA}V^lw&gExgH^E0%Y~F0b(3guMM4O>)U`Z=nsvv^ayjTnm8Z4pvKlh&evHBLoVmI+cl&cvUN^m)i^bFly81F(!;3+x`>T4A6R2Xnt<HIYZ)0DmwDNb0p3Tx4?&25vILoN!9qqGjdu@G$uacSDMbhqq1mvy<Xz2jGx-1d52o4Fs-Tvi+ARArLGP%uoUi#2is#0{UF+Dqb+(sbQ_%y&0sblxuMPq6**X~$q@X&!WtS>4?!NrtQ`WVgnB>7^mtS$rx!@e^fe4K6s@0OjHO^%@wcwtsM_Yi8TL)1!zT-X!lsIw*ZIh^7KnR&jLafWs4oELDgUOj4}x118p4S!exA>wP9vm&>erSK?Mhp!|hDSF*kIYg+DNGZJDv^Xd7EL^}<a|6%``V;i_QX)SJ+GM;G&>Cf3^v=su9p`!hCGeZ~ifn`I+|#Q6bx5EV!LCy>3Au$Li-AtgS0vZAnt(DYq&i~7X^Ow;RV(aokx<4<$n9B)n)@#9DXR$Ic@&6Kn1$d(H13(bG72EX73K_3@?h}h!4BJa95cC(na(I(7f|l!k2H2jKY25gh!BJ8+lx*a1j%%X$xC&!eeFnG0avDP6TylxnVuUdbMf%bb3-K+U2d2cVp~U9kqv?OBdWIqQ@diEsZ`>;N1bvct;B?9yqq2Tox3W;kF8nQzAc_Q!);n+7*&xl4a3NQk@PQQWYw%Tmf7`dq_>>2ot1<lI!X(rX^2~@koPOq;msgit5Sv{!@oFqfkuS-tB`Z`$`HxJV#}eXo~_(uN_p{2^BrTA*&2vh0FAPl)b!O}0Nd!4eoBjpQyglP<$Rq-U1AzF)T7U`Yqpqe(y(zMy9yK|RCM=22?ox4j8fRZNwii7<pTUEVb>F2evcteYL=bRkp!Bl029=BD_~$kZaLxE+VU@T<D;Ud0El1DL$E|S80eBRu3gDG`tb@_>?r5kQ=7IY8T#QuAje~)t1K0MM30I^nS_Xso)wy`1EH&Xee5PoW8Wr3m~=1QE0*gO-m22@moaoJJ-r}`p({>qjOv(7B^o*-t^&@K_j23RfYcInjB<y$|Mu)d*F@uT1kSEK#S)<JGN>cMD)T6llV(XkL+Fwtqvz)q%Q@)jIZnzi_N(S7djfbatj09rG!g5p%FjLG3uAw4=uASEhV4z_x?vL8L?oOux$s=<G1x`kIEuctmWj6UG1&Ssusx9x<>?OB<@2hka{B_y<dhQTMuYreSiYv@Hc$5ml!g^81iXr5Zp_<dO@#8Wqk^u+9qAudiIOo&mxic;(`zq9uBOopCR5c@D9KWY)DpsFsbpHXybeT>1*l$@A_-7+Sk=jqV%dYcAK+TjeDeQpf41~J5NhW^gcUMg#*l&g5!!po$j0(u3uS#$jNfMW^ivrQK^}@j`qm^`VKGLPLW%)SAcA~XI$_M*Oy=9a`!&(6<%K9He1sKMmtGUD8I=Ql^9wd;vTqogQ|csl3Wz`ml#_L9x;6=c02KlyZ>h7~Rgh!1^h*<rWv!?BG@Mh(!KEJ4Cy(b-NtYw)POXVg?2*2x*OuB#q#7uOM&Iq}Uvqet9e{GFJU01H#JP3N^?y4`qal)*C!K^I0bFD*1S)?_Fs0XI{4N0i&V*0hMJY5^Y}yH|#kB(kSn4RT9J8Q<kwu+DQJ#})HZz8H#gDu`>c^0$zJ@J^iDlRvE%weuA4?Q{2np<jmqju(0BM!LSCwUv1#-PNtLqUafHf9!EV)?9s|QFdV&O?r5p7LjrV*WXup1#<m0gDngA%dz4`&Mct+)BCQEC=wh_vpnj<jafA*@vS_>r6O2+r%Ume|>0aD7o&76s#8Ii!JN2mY5=_Yx~3mSaP$e)wy;(Ox{w-x|Nl-`c_)YEW2MI5dNC?a+3&N&O~s(>4g{=<V(U;w5Es%0`|=W~B)fb2@Nv;I+7=ijshhgVw*Y&8p6p_d<r@8D(&Cku%m-Y*8vVDxkwWd06GOsA+eAReAd!p0>-Y%`<M);%bcIp_Q9`NanWm=?j?zfa}iT46h#hr&{pJw&xS<S;r8%Sgd?No`@0vg!idWZ!An7k_o_s;uAy>r4`6#$XG!)3*UXN)S_a1w{ys~1I&wAWL!A2lF?LjZk#)ROk_!Ls!Da@sBs`kA{rx9&Y48y7+kd{6vxgn2?Ns*X#zk<`7yVUCllypYsDy$OIW=iL6Kt*={G<<!gK!_ub$g*LK@6cfx(aY)M1nfOygvKbOb?6?6-H4)3(L6893MZS*<~e0!#3z=ta_F<b|eZYl=9ffYRkl!?zl?T5tjm4lWmR%~`<xk05MyJ(YOAi|mw<COJZq5us63<2IfH&h^w$;Z$xObVkcCj;h1njmXClmab1sy9H_1)OKpLcpsX_tD$^6qv*8-kfiC3+w)j%wbHk=wyetPDa@QNFH+DzFahH`x?%G<xsa7D(b7Pp28PR_r2EG}myU8jC(5VfA;Jv}nK0^@t2nTf@I&W33i)j|6&UAx^Pi2OJ5sb0RtIzIFLm59$!MIX;f))>P1BWLgy!hmJf=~VwtBKfoy9`<AWEP-o8|S5-!yeH`S2dC2$*Zv!ZfZrN0&^c%GFBRr~FXxIL4&oZAEdL1dBqQmTrWotWnGQ**~aekpyu&b8yFm)<|d(sf<9z;3!anza$~ME{)K2+MerwX`be<DOc5|H;S_A3s4}xL`9JwVlm~mz=l0@l1opwInO#59OnUaTf0OUjM74V40%qF_xIKBKgh3heDN{F+HG^f*N@7Oq`1~xUvgd(l`a<s^6s|x@P{N7eq8`Jb>7r!B853cyRPXQIpkQ!NTUJ}dRYBFcm|v36uhe;Eq&_P>U4lSKQ6WtoxW((#ueQ}?uqq9+L5E4K$O+6J1XcXZnVTrRvMgqH)$`YsY*g{P-}gX$RxxH)P0np<O+;dLfab>;KwWzser|+;RJ4SS)Npdd>1$;ds63whM|^K2N+QpNVqp=DC3y}_bn}Zt__okWdV|AiPtEq!88HyZQylK$%_CVaffmjfx0-ddP)ZKa2Sp$jrtjnF%|u+)cqBtI^{{3E>3iPO{i3h%0ADUI(>p6){h)c^1j_wCKKU(XvDN#B4qNb9T2(GGS{`cULrBf-+u_y?t5xe^qFZoR0xw`^qgXv_e2{A5f<@<rt}$~9%$V&sAu>TfW5*lh^-tD0J_j7dCs9}(FurRBQqcER<If!DkjL^YnprDzT8KOo_~9}&Ywz@CgaZ5($&UW7nzWap}B$$)Wap|wt<GGy3Bo|%iMLNaJ&z>2Zb!Z&a%nMak3U_AoqjW6Y3JakPpIcrZ{FF6&NAWNVualCa||l7|4+0%Nw$br?N-*Bf2XZZGRKL?Q4RM&Rz|h78A)`<$H18olT}hO_z$&7*G#X2`);A7o-9QGBF<0a*WT-A}0gx_=a@|{4xIGWxx;ME2e3L`5Edu%7!&V?T-t`7^KN}#6SCM3b=UQ&GWzbP>ahOlQ5i#={4d%Q&<$_i~yGcM*qsF6)q};wGn}lV&w-ik*}yQu5#%%XpEbk<j7}{*6HnX16{85QJ(5`BXy8<3so;E$P{o5nsw3}2qyp_!au?|*$^E@UBlw?$9vG}_TiT&1L6u-$56fm{tlmpc^l*j;w=r^Y=HwK<m18?Q~TO)qwGRbbVssL5nA}RvIj;xC49e!6f!<q0lq9=WS;})7;a}k7gb<sejf%Voy>}L(_=f(lzv_K_W#-hzx_hegE&SUfY-K~NP$SmTuz2gz6k%goY&d%q6@TFDdSG&N&-O^$af^SHSG3D4a6bA0D+ROkO!?Gum+osxuVKh2@}O6PF<_Dcb1Ocg~Yq4QkuLF72}Uvwm6zhQIyT7B8>MK%ChxQ#H`Yiv{|D+KldNs9&BNwg?5^a<Hy26I23@F?@uT!=I%S2(Ub`{uWC`7+KBnaOMPscj!|~-{Zf|D>p454XC{N;bj&M)uEnP=w5gb5!hL9%=aP+)I6_ERsFI0(9zyDQ>@{OoXghP%R|5{JnumUvdS;5Whq~^ve}aKqSF_Z^G3P=_Il&g+&^2Rh=u6HkH~6+TodyxPq*P$L++kFh-}4mBq8?CC6(YtA91!rW$hZMQ{JQVYf@fayRiwEwajKGKc#1L02;IIyO86Mqm{d2L{4hPBC572RCS%gkQ>|r>0zu7Xm{de}kX<5vi?3HQ^}vt90~qx$K!}Si(eXTa+*#7hMA)o)&Y(oRsD#o#K}12s)nP8LTK{qxa;+GSfo>Fka<pS0gUR~)BBnmy<zI%SSMviD9<VuoMY<y;+6rFYWmr|KfSa<;$)@iTsVsw|x5@ZJlI9D$`2grkS1kdD>27-WL|!>W^g8$I@Y@n8f7IyR5x7KGX&m}g^knHr;Fjq)d3=d`F`8!XV_$SeJE&Mk2?<!#bjQ*#Y*4`_a^09Z=Cd(Wjn;k6th>#kTP6eG1t`z%mtL%*?^803ZSo+GcZ&xVAZ${^9F8D(2wc9gCgjk9s#V0x4)R*cRLmBlrjTV^(hZg@G^P5R4?ky*bL+2gEw121Cc21d=7QM{FstNjI4ZJ4lic+1Jw|m&+N+dsP0O#&=jit*>kt^<Ma?64%|evg?(EJX2e(W^N0k9-Ze&fJMeoLb6gf@P_++{dGD|pZHFkzV5E8dedU@UR%uSP+-g_9B%HE0I87+0kejK*qs|mhkn*Zw)e3xeErBPgN(R4ze*z@Q<CMfGL!rg~o#YAMp>Ld}56t3PIWmT7#XZXe-^EWLrp6o+Ol6|}@nsad3#Khm-aI88K?&_IAP(YBLba4$@Lz{%~<Jp*L(|1ZPi38*mdYS=&s{r%k(+R0L80IfUiUH<<5^)(7OEjZ7V)Edzu8(Dj(P<<-HjkZhL$+H2<<X$TY?Phhi%uM(xr+e5haRO9C!_J}JjSymH8{_DI}G-`Qv|OZz4?(T<sai0l!%aJAt^iH<Ju4y{*a{Vxt}AiPr;NJ$!J%n4_|zEgxcJ~85_-ueyGqpVjj*8|D4Ni=+<DB#gCy_MDQev^sx-p=)~Fc*2k?5QUkg{3PMFSQ^4~d4dE6@@@NTpM$Q{Vt#Ut_uu)~uv#3<N2ZB{;QX!aSk0H3t?JO@hoLx+UIn|`VwvLt}7=n2zlT5r!msKE=3OY92M5JuD%G@cm9LSp!N~oYkmoI&h#SuRwn?*Q=o$M30v23YpqVZNwyhQ)*^B#)bFG~sIa%M;w4p*s+0t<!&&A?e%_3YMbzKW|<e$K`8Faj_pg#6zo+weMkq>4@I{A|z_S1-meD;D>6>)ugxLGWdf_>C`N_Am^#*W&uk`}P0+?PI1BB}HB`q{v^ziM%vD>rxgj7I0Y-LNP*AXII~oP`{i%7?M0fE75`|-Im@N1DB1$5ozIvtxFrPH$9hEmgg-&@=g<P;K4sX>9e*1qj)-r(=u#Te(ghTgeMzG>3H{Tu?Onm-p87KusC*yAX;RY{o?+^@K5#eX07Iy8TRqU=$#$#Z;IIj3l&AtOyP$V2R<^o5ciWix0BtTse}Yeb6bIRsJ)6HIFS}mp9J(xVPS4_3@JWM#}vb22_uw`3jAEnK}xYVW#M($y3CN^fd~gRHRAIWg-}Ko4>LaTPvX1N+#vbK4mGW*y=x`7C=Fuq7zUamMNY;UXj@6Rv?2ZYT)HWh&-S(?ymePwktq{jvK66~I9+>9fzd&idEX!H${*i;`{|Ew=7%3`%f3C@)!*KK{r0>0dGuUC$NeBfxqj0;W5=2=QBuzK5wJI`^`6dA*k>LgrUe7xzrcK@giUDI7Vg6HE550ON_Nfc7sR3Rz7Xx&#sBqhzq!bN{`qnE{-^(cbKkNYOL83hLs)b@yJ|TSVI<9lJTh@;SY6YX=-=;fP}S(l@NoCY#*wrd3{C^cXJkA)+=p2R(Rpo2F9(Ffyj7@R8P&pv1z`XDs||B^v}O`cP_$Fe(dfVb_;Aq_3=VY6WOPMU|M;_SLee4D!ik*~!@Y7p42ul?|LvcD{q;}(_4{A`?VsU^hy#0Ev-o4Dp=)qJCg5gRX4eXQUG?}EG5?~4?+^DZO`i@8DLEMHY4nfn_vGK=nl|47cS@1bfwVo-2RYNWPp^Q8@K2(#V>~-7ZC`#JJ$yb(jp?2|?V?XWJ2cG8ab0=GzQJW+jgmL)59{2M4_AJ&$5wj9Gz<-6FT4`yWLcaZj2r{~-gr;e7b^!a1w$9=_`5HP=H*bo>YLxP-{xu$?I7=pbFxT=K894wFMt2*-+uY^u$Pb1eILtxDn5jPQliCuysLii<Sim<DC#E|_#I$vhx=?xf7bk~f+a?CiiS>Ot&!7pU+hdG9}skGEJi-K?0$kXX4DV&;LD?F{l>aSc#KLim7075`Op%UwV~k<HASc>E;#b2WY)g=-k<B$u!T|zJM8EtU3(FoURTXLkJ{$f@gN%_gAk!exN|9$b4(iR8s~r`nX@-{Q$8_Y60W(eSmuX@WYC&E`xZA$`8Mn?NPne(V}m?HF3>)FKZt|gspHSSs=D>PMfpK;=25m4;f_@~aE>9ZBCSEirGhZ!lb*phu!)Rmu44^u<UjuM{{A0QNBMD6?xOAxQOT%EelGdvA1BU7S+wd*k?ejjQBV_;?T&F`?a^c|-c{{!yxshVHm38y0n7w!UPzuj#yYqpPgYXzp+@sq$M)0a^Lvc0p!-vJX*nju36{pD92_H&=L{Yk4FPl&)uw?THQrPx96S01$_)QAsU-Tz#&MATH0g3_78Z$2h%Ly{`D0VAMPU3;Z=q}gULW!C#}!~3{Z=Bi0n&M_HgriAjt%7tC<pL!a@n@jM6i(^<5<K)Mwgo6i_3u5$LU?aF99}wuM0LdoFO2oL&QLZ2gca*BC%sM{H-tJRi?(sO%Xj1<k>ikaP|I6B3xN}iAOsX$lMkT8;O{_Z*w3<l{G|}5S6m>tDv?f>M>f`yT{~zRXQ_gnR#iU-?Hm+%xUjw>5XPs`<o>89H*gY6w$i`>FpM14F34!_Ihx}ak;@j=G(=n!rjL1&{U{-(ITB}?O@*dF_sP*aCV1i-H_D-8i!=M_jQ1Ruoi-lTjMGBbUg>Qm4)fR;m<NptxF3fK@;C;+F#2`Reas}*XO}4&V9VwxKbZ;iUH6MoBHP;KmPG9(<$epH;?XIIQ=C53bvVi)aW!rgBE;amUCXy|HQlqU2+<U%_W36*8%D2h9h7xFxa(%J*$u=7CLqa!15U7=3>>jXbkO0VKD*}<^3Gnf_?l0ow+6)%HdOD4(JEyFM)LRRyF(hbz=sHUgX_e2E)e*L(e5{-qa7U3)@3xcOYxe2YfL|WNB&f@sFRjTb6l0+~6-}`Oo!X6I(%Z-!W5Z4j9ugqA_3+8<07%^|I4KTYCJ~n~TCjaxl?h;M0m8cev%puJ>!fjO*Z*F(ZTm;H=qB2!KxWg<1a`C4vu}7XvZQJibgDF`DpI@Fxo+kpN|;o+Mb)X3jtb$Q5U~AjR}jCTaYA$NrSMr!qtKmX=gbv%9W^0vl=diZ8sO<Y5sp<rxrCDQZB7F<B1ER~D%L>v56SxdCOrIJ0xZ8s+=wlRv^&$X?v?-38XErYO=y_Ppxs71_JH|2~>rVb3TuUL$I+dB>(TiHTM_UBJUpvR&;AE7q(1)kcg=O|ov8<Q9sgjj`1gF4yO%w_9mLqO&XO$u`eFFoS6#$K8}|d|js+0^`}8%gG8{-z8E#q<O`66u2~t2GYh%na+@+v?nt6U_sHX;QyNMhtaz*D*a-evcCT$>Xy;b?)`8Y^#GwDJf~R+W8ZBZBvl{m5RrtNnI608*2_N>I|^X^-3Lr+2K1>BV*4oTGlAH|!)E3}3Z+{<-IhKp3vd|9@X}IMRe7zQhOB>rswatXNxu-iaM?MLBpXC`jO872uAE>7rkn5OsM899NC%%{81!ivUp46K_uBEPfd~P-Qj7*EhY@(wVFK2SPdMQDn8V$E0s#FLgGhP`bn!Gc%mD<s3le{f3q?H-<!r|>-ks(bCdX*nnOg3ea=yRZNR9>kE_yqokMao7Q~vn^V{kj#0`P+51z1}KO<%?%+aQ@DBnXpzxq^i1bTDkzF~FrG;XqlP>@_PM#c6ak9zc}DJI`{u2Iu*imW~FbZ(}6QT=;2PZR?}p0k1!ZlfqttjA>eG90lVR7u}ZLz@5F2j4JM!>Q-Z$WPlD&*^;1g&Nu&aX!FfQ>O=0W$h5)ABaSschBftcuYLhJ6VDUM0>uFr+Mr37`(rLk7ZG}lL;-~tXo@Hm$)*O3;qab=pjX*-BOM*BRm1hHXv`VQzkD<if4g7U%9po+CB)_B<m-+8japoj{2(s1gErtLX$p)$l&uDJ?1flnTIN?!tm&Gv^b`81^ZYNqaEQ(Ht}#(^CC}$**&2iNHOs8sJ<TU$ZUYI!Xe<Xfk^6V`2p3Skew&;060T1`3lE9!P&L&YNF=|}Gg}8Y9~qsI*bSRwaGi|ZZnE-T*8p!q2P`$^arlfop-A17xNrz!)-00S2t2KQ@G#yLPDw23^z)Qeyx9%%#p<ce1+AE?Y>Z_Q&oihc=c;)W{u@jt7|s1fdc<CNISAi{onbs=I-MWh&pNG}9r<-}@aJfb7DDH`ajnS1h2LOOy(iiWNs1n1=4SnSx=(fXbyfq5aN@5NG7A+v`L8o7ZJDf;>(A1Rlskh8M(N7TX^tC=j=<kn<ty=)WO7T<uH03o#qTUU1<0?**Fw8xHh8<)&N40hUxx(h5A1jr6OWrzp3F6v$Df20n6{;WU35re%qr8UznN7i;!lzAB}>BXbxrSM!B)SL!R{n;M&P=9y-SXZW~7)J$|+?p;d_tL2oy773n4o40q34La2F=T%JBVQHsK}rI&h|asPr)D5VYKRuS5^B>eH^6Dm*<s;fq0lk6IB`<ZI3gbussQN8Sy1Ieohb){yBYd`@TvY7xg|w$kl}DI>O-)XD{}?PrYgY^j}Qyq=k=%;~!}h_iTBNy-T!1F0^h_?dI|pPRL^om{hxoNt3G;o_k)8RV1xhKh7jyn*2aT*JThobBYK8PTy?DZ7Gh1as6&rBc>PEzEqIZLAo_VbCzqe<Erg?0i!)Y}ksp8R|1mU}lHptIyouF;<&off$77t(6kiS4#oxWRl39TfCeTC!o~l_XP^GW<Nu%^~}qSb@`B+b#x+i?mGx5t-&*x(|HdnuMHf;4_|jI<0JsT6`+}qA&ze9ow0}{wlGiewVn$Yn2~TUxVf>CO<j0Zzcrx#_wx|Qpbt8%j^Z)3j(MyC7F#8Pd&=zbBttLVi0XI}_$nWTAJHRjokt_uqi2QY^gtY&UZ1!L<IuMW3c#M_fKB9qLpL=yv||jYOHVI|Xy}TQ8{;}A<E)0x_@;m}mA%|CEnqb}9i!Y~L7+YR&^7TW7=g1JPqBqfybS7yt>$U4IYq17of3r=Wt?(G$)mu140?QxO7bWBRg=oCfV5zYhY=HtS$uUq_Y9RZG|@YAt8+urX3^&`0aGFb%=u?{KJ^&vYHu6`5=YBK8x$D={}|X_$cFMnN9yurC04r=gE1}7vrLqV?4qn`Q{>sp?GE!?REjq_*qFD=+9T~@tGcg8`IsM8i%C(XP9>D!^xEgyE)vpgCKJPRn8Zrp+F2rhsnVHT-UP|W0@N%^QN-FNWa#8bvFt&o{w?kQdDx%5r@9<&F23Q>r^8TgS^XL_cC0y}dTSDuu(07O0BO_^h``>RrkF6dkU7rp&QfUH%3ORDe!=o&TCas`Mhmi8Nh6u;8%Ds)%V;+ZnD_{k(@g83F^ESv3xkPvUM9Q2phoJLr}i1QnpwAL=6_73mt|APNviMmG<+o_yfImNOpSZM{~OWNa<4T^Co+^0#L80}4D=sv{1+M<EdCrOSQ7IIue*Ugwi+;CQ&bv}G)VSnm*PMHj8~;EHAOZU+1S@E<S~9g$czy#)f~okwG}*{lbaco)HatCr;|HZYt3uSGM^R`l-vM;+llO##~gO2N-gn*>=ad4aEQIh%I;T(@vf3kK;)oxRPcj@JVwU%z=|@@e{uuho?|YvesCFn*;KwnVMmtuZLqY$2gow~W)3(KBe;3qd`&mnisZfd!_Rv2H<>LGDb$r0p&3C6?e-bnZ!%Y5gT?FK<|d%7FmFkMJhR9w35%kG1kVfNs5B`%7eKC{^J(5DR|qJ3A!Qzs((a@ffoLl>m9$c&LYNVh^{h;B91L*nQwg~a0bpnanSn`7Qf<?jx4oWkt9nn+4`JCvX{*nZy^nnwK{EG2h6}SHFEqT*t*9-7#Ti;R_&RWP1sCAAr8v!f>A?13evA~|=p<+ywF;cFI480e$Rn+?k-`)g2?+g}sFr%Jy&)xTYm}+LG<bMY=(6vUQV*!!f&&Dsn@O7LUKx?I-DT50NUvr-GGh!&vFN1vq_9;-R%|g?L}M&ntf#WTF>hic&iR(4F*mw*%WZm9F^qyj3M>r#qrr<=8YDKrU>3*~VqpEvnxl(EUOUq58P?QD3RdyAe?%&GV_vK6e33pG(lD=z&{@uMxz+k-sGcFe?>_mSj2@QT-i^4$afL4%N;`x6o<7hUa?ffk#~~UdxnwWA5^fV~aJM0K=g^fPH6uceS@YsEqC1CJGIZf@L(5(3UZBd=$l@5**+i<@dfTRRa*|i7fVQSF4FhFUrt@Q<YeyxO6Mj?r1H-sT?tx{fl?Yf4_o<;5r5|Ew2Of||Us8<cJ94Tc#hxs~R>>9PR693uz(MrIG~|TOd5nXr9`s`0EQ`YMu~SbFit(wb8^=!O5#B7K5Q1?nLI)i`sNUojySzwSD4!}6$0&U$ps6TwnU;8-8rkv+cnx#~N~MDQg7Iiuv!6aL++8WxA+-d^%c_Dl_(K+G=F+3NjN5C_{N`!?IrXJQi@}%hBY91Us(qW)kIw}TY=5I&EBc)C<a1YX-m<joMCq)%@TB3q(9=|)Nbf7Svk-toH;*AM-8M(Qhg9rA{xk@X!0_*d(o~AuaFodNj3td6k6~_Zv5$gx)E*aAS+3+m$4FJ_2|c5ELoP!#bZUw%lIpv3NM&y>%|VNW&VA~ppG4g|?uqrq)yh%#9JOOQlU>$;waZ3|Ipo8^$xq7#cBW&N0ue9{kTy)xb?Zj*BF6qLDacZHb6#JRw0k$$@_N$YUNCUxJ?6WQwV{Xzxm#zDkX^m>m74cj?-djK0d%bvnMo<Q+>W(fZZ2a9U?%NQ9wMlZL}$y%4PKt&W$;hEMo#qe)ArYima)#na&b?WZztY91~$9I)U35Drx{^giE`GD{a<WK0p3kRtluRVB|q8$A3Kfra__FHSme`>4}p?BEmg4>r|A?RykY8P#Z1oyIKHDcz(m&@cdltC5Il;?2C5n1lZIXmM>S(<c=F*{dJG9Yg7HM1pDI-CbW_^g)q%IHHWv{?E{UD;9dzsHAr!|t^@)>m2Zn;tKB`R#S2vq)i%&df3D%k<Gqh<P+zt6$JjphNqD-`~FruI_SudF(F;>#?C&!xiSk9S-*6Z5b9%<uLEtIVH0(DcoN-=R`@*pPni0s;Cvj>(-7iD~81~>#4NMh+I#ktKP#T49hjJe{PD66;MZ^D`3FJz?{PgUe4ZS8svc(4s_g%TT=HZg#a??`_3?<G**c{k7h;zMmNukN=#Q>S-D73A=9+Ho`&07d`GsGBdkUrQqcVMUlvbk;wk;&r!6iK4S=N>U16MZ=^yh;iYYPHVkcie&2Vo79n`08Bv371qh`KpO#|g-QlE92CbyWw8^?NmY0<>4LWVKGgxUFG0S;r(xc1_5|^k%05ltz!+I9*`pX=`)#mYONurqcDg|e-`1YMXvc!@_mp_WM@t}}^dg@YC>?HR0H|t&G%F4RmQE6~W%FY`(A9ih`1b$Ww0Qi&qE0_XEV>M~rI0eQkfNM7n0z6Bxm^$2>ip!ikEh~J))MJn*64YT3lE96yX=rD4KQI>00ES*odvC<zqy+a8KQbL1&hWM1&KEbhrf50ZQhL>x2Y9aT=^xWB0#=EKyMuxAu7R;J*l?jwTio4c8oR+^ZVcZ&mT_~wNWBEjnDBhS(b+4(e`bVIzP1=CuTZUg4wHJ%jUK~zVT`s+rDFz9mJcIZt!~k&e)vs(I>s?{!Z|$&K1G3&%S|yOdCBJPDN5K)t1KetWo!6Un*vW_6w_K5pW*eBzNZ&Is4tR+g=U^C|%8x2N_Mi*ZwHydEz^IuNW2j!1H<$zLgDr-pq$QG4G|K3#10VZ)Fo@3UG*;6ERxgfPil)BL*0#mwkT~xbi(;5t4i0xUILBc$y4-OfP}B-iD%B(3pqvf`1Wa5Sc2#Tkc0V)66qWW2#tpEXwHOl0^o}QZIKJ!j0?j#?M;~(4H8CM$)0iwgmESwYskGAlKX4%jFKT<k)Jw9GiFOC_bilcTXj5WI5+Zkz~ly$L$J!@!B-uGyE9IK*`3Z7&@2OjLsADxafN!(<zae$(@0k+B69*S!qXR8_5kBZhfLhwo(^()P2meYYj>>9{OB*+FioX_M$I}4R!RjG{_xd!ezO)U7-&M1D`5u%*2jkzo}@@aB$q+mu2?%qnHK_A@K8k;cg~yq;t>njD~K)I~bON5RE8;D0*d($gq9qw*b*U#=n*u$yjJY1<#&77musni@Q2?g}x0MuQEFT=3>o3aTJTGZGNbxaX^-^T`^L-5Vx(v{$iFHV}Ph}Yu_D3%?~!_5Y<`7;l<nsY#vYG{P94&pa-Ajw$6<iM>E6mG#r;AFc?-ld%-@=+!+*sj?@2vtVSN2r}^Tw(RXYCN%^lFw5~$;7gEn|ZKyNybc~{Gu{Z=~t`Vs864!4}d<-HXGOjihhX^lF!)NFn&V_u)!&KaT5YZKA0xO{+Ym?S^y+#@z9JP*{zaw_N4}eS1%LMoz4I~uJZH%(Np24C@o$X*ADE(83D$tB3)sD}@v%FBR0X&2(ah--vO^=8uM+qIMSf{cFe&by0QBGZ)+C3}>oiG4XT<keaBk8JX@|y;*?^$A$<QTV)O0Du3zajX6j0;IB0k<`Vc<@7(%-Md9e0d3m!KeYd`XOj}0G^;WbUvemY4y((dP%|)+2MP0-hSU2+-)&P$UiS0MU(T<dPA;(=Ct*ZGlOW@H%KD*Qy0Vw`5WFGkj?Ni#*9%@#G$^)Gj?je74(joC=mqX(QKfYX63@f@NGHgH`uzAB{(<RKgv>?Ix_QU)1}g7HE3%DuH6N$kZUs67<hRIN~Pei2)B);J%&5mB4i(y)gok}Nk)kyX4z6Nh5kf8$)f%}rJ^=_1lC!G;LMUTJfTy&0~YKlzW1Sr^EsQlpWphPuXHIU&$@&LFsL=S>P}MM#ZYG~k?3}qJulJf?RJZ~yz4g~H|SsAK4v;nI?%O32l}(vK-UJU3vLXju8S@GpNYz2b-=2FmrSY4tE}o<3=-AmXn7-;*nePqA{rxp@%S+ORd%}nQr)|U=?8MuX7W*@mz?eA^*a_y#S2V3fh0UXDn!<g+D1?s-d@S>ilzBnf%|Rgr7*`C1JMaDSUzN7Zc7?P@M-#-qJ+FKkCd@<ev$f|cLB*bb%<z;uH^K&iw(x*7zUamUUzJ*z)WLC?*exI<L`3O_-MG6aA+552E7#-D^4C;5t<VBC08`aCb8@L{(R_v`|-D5e)|zV{Cx2D?ZWl){_BswhtDHh3ZMR?ar^qsU}KLpUsY%v(WA`3o{#S3g@bPp!qRDjOP&Y5QpP5<YYTVb^%dV-@`t!)@eA_WXJ43h?W=rGZC$v?zyJDS_}8x<W+CF@!J}VxDTjHh@Y%6G&)n#QaC>ODIiod`b-kjUdM@bw`;U(b4<IeG56kF^qy6z`-vmK&tVt0&D~5aRFdY^dJp9`~|N85n{_FR@{M$dn6A=gYxMuOkPD9re-pva4u*|L%_`2%xFJi7Js}n2Svowh@G%TZFtf$dGw%-#|iEG+?2iz$|oC9)ajBWc&o;<w*IOIG2{0{3$m!GC*&2N-9y^*I)GuR5xYtoQN#%1JffJTR;HA>zEIIMF|wn@3g9$xBNNE{lHL3jhuL9!ZxS!*r&z42VGFXrW7I)E<J@poU;m&u_t)hE6s=F8cd+d<wH9afRobqrzuFMt2*-+uY^FprPZeILu<XTNYr*;?X0-j%dV^7IgTbM+Ifcn7d-L&HbMRI+OBRKXIXIYmR4`BF6Y9qx;r)#3w!evCyH1ee`UwmlOMU%Y`Y2c~rs>ki;Cs@=~KQ@ZthXbElA(9oNiIujI+7n`#)YhQiu&-H4E%qU$B_G^<4kcj@Q3rw9yZJTUtBqVBLb$b-}b}pszg-PE=;~a1VVfN;3$_3_2!UZc80q)Q+7g^J1-{OWT--i7KEf3^^S;Y`%f%f71OQiHp9e;MLq*~&-&OfP~H|$22Ar|Y))gYnBI!lXG^9z|-xJ*p<8FKnyA`xPQU*HHVL{e}~8PTsFg0_eWpm`%~v!`R4$(hI=Ou?i6$6wyx|KsZk*;iK_!A5Ep+{2Ql2$=XWhkG9{W-Rx(6h0LI*C1(XJmq?*ed6>4R#tMi>06)s$&g2ly<GIDQ&^ncRr1FK#)fU?!=ds=3OzoWhIgb^cVN8rLTdoV*h<FZluve;$J<!1GJ|v?<r+xNiJ`TaFY6?RO=BK_uV;QW<8M2LGb_g(ED$)S(k27j6@7xolRz@2`N}S8D%84CS<oW#^caxD56Z=gMouWNCSA|<V=A+fz*v%YJ_3u()32YRE`OW}dWJW*SjS(`E(_auC17;B7GnrO`-B4<$SoQ`6`&~QX6(-Gmk=J>de4E!1_5|n#RhOgIT}b29o!xarHZGIF$7&IG^1vf$pTci&k-XSL;vOqv4rh0)XA;MeGnNz8F<GL11P7J?jDEPPaj5m^h_8KF5QBU3R33qfXmByAXMHdB0|83^Dn?+#t|MvS--F9Gk$NnVQhF<KqZ4HSc)o83?3PYVtgpusMSMXjN=W)^(hA+0{PkUw5B-43s8;oc^K{bSLWm8zDfi|zl<<>412OA<uA6C)@gjCk1g<dj8?XZGR<05!^`9KmlpahyDrC^_MYzX_!zT91&et<M==dOqlmsZ@NQZOIq=6Px2uSgbjuC)RN{N}X3rg+3P2B<cr19|nX5f@5NfkKM8Pu5rEVO;>E73D45AF!1=1Q%xu@$nu&pc<2M)jT`lxhg;-^geYo!?GB(Vmx&%ZtoE+XZ_k@wL5cHJ@Df%34afBx~~AMa1VKkR~>kKR1Gb1CM<sSmaIh}*p9556&{Q$0`r6Y~PL;9cc?=2D9fSI+2Zuq1$JFxa(%udc98>a<jrCIX|hQ#@RLg-VUF7$N6j9vAH69~}s5!WSJrCFX#Bfc_F#n6)5W$FCc+mY+r5&1EoroG|oU6y{C+0K2f9*OINka6aHmy%3(5$4}cWu}vRt@E5DW=lZaTt$;}MnCWU)#zpI`BUS+%oaklyW!Urhtv5TX1%y?i!@#E%J??PJk6rIqRT<a8#qLDhAjllCoe-$h<_i<_GfLPxI4`fHzKB*~G~uhjg9sy$phKsgB-pyxNIK+-vs{oO6)F>a{=Q>>O5IbLA<MBMr`cWoWF>71XYdM^*XDd{WeCjUDr^D{P3u)8wf6P6$m`rR9=$lTbHnZm^zaB@!M%;-ih<y)sc+<XTq;8U_QKxX{rAyirBk4kycX24X-#6H)iM`7Q7GB2b|!8n5i@J+R~4a=c50H~&7^?w=m3+{>U$Bxu-!@<5}jQMSGM&LfEi2^Iqs%x<LkQ75S7919KuQq4#&oKY0&K~ulSAvmuAsG+L&p)8S0JpMCP6b2y`p>zvla4H0+H^AXulY?>`9<Jvu75A5Jqm01m@*nw2p2-4=gR^}!A~M!1>jv6~u@*+*IM3Ap<n#=nk;N@lS187_bwP_~R#e=25cx~;axeT;tDGZ1$}pV;Ykw~>Z1a%FKk$mC_I+3Dtc1wNLA4Y#Lbc^bx74dD8{c5iBMLNR0k(Nn%J_zi>!OVgj{J;}!$?zYKntGI#-!_%var?Fv^i7Zm7P@Uk%l5Gan?7%VJoyOyng>7{+o7|Oa-%r;jHh>)3O^KrK_@+NX+Eg5%K<3<zwg6NhaWw1Qqv^hQWE<p9gwSAiLRZYtZ{5l6R3j_n1?YLhL}ks2M{ycm0S*vV@b=`K!pC`jrlq4x_1j2cQwL&NZR?}T>90SClfo*p<_(BYBwUtU5L$Wz_g;mfW2#$C<Cg&-Jf%#6VmaUZ&!Npq@#QPuh$_*MeTkJ59BY0IYwDpm_yRsAo+s31@^I9ZH~-`@J?64>(bLC%6+r6<SQJV{rKtfgIE?hDWl7j|BYhjKRYSL}_~lu%ntU`7v%X&l%9pn(<HzOYtoV&Kky>1nAtx@iQ=R7}TnZ#$JuC#$d(cXrOF6%S`b^i9rEAbfo#%h?HC=29evKiL+M7{|c032XH74q7-Wf|unvo^V!VJjJ*b;C?_wS;X=<8DJLH^zWx%KC4T7X4-nX1X!KsEf0zS=sJnFXTH&*43+ni>^k4Px=@8sJUn0CuK5yq}RM)D)Z&rw)O%nniN^4X3paU<DmxHdLN$GLl&FW;fW8=pca<QZ7EmoM&S!i+Hd>H8vMHqySpop+7auhIJC%UM)ZffQ7wPLd^bfhd9ORv~G4RSir=x5_$$ga~-=@Oyt5OGpX(k?Uy7q4l;A~@TWE9=|0s-O;|U5gy?>ynOQjDskfbxYfFi!!UL9y^k@wTsGRD8ALEs<G!pU2>rHEPF@Hc0%Q4=yg2DG&D2di`+Tk88<6UKs{O-a({q@h_0$PZ->=oH=b^t(&|JNabnhLv4#boLxbxwr{(9cK`Zc72b2z?pqk?{N=|7KQoi9bbx+k28Z+&eYlr-q?WSw;BHql5xQTNqA6<DSJU<KRM=HZB9ggTaRfTehksnaX{rbpPnkv)r?;ByqAj)b7(LF$zoJgF$GFT9N*8Uqc_~<=cSg(zj<|#h8Z9XL@TshrX3=E~bzp8%4S7gUZ5H|Bz24d^V@Kop#0LLy|@a9Y;k##m}5`{oII^?b6|N&bPs(O!M%F4CF|ELq)AEmE~I#C7}77?c}5d(UDmxpMY+Ca)e>!SzM{Dm~XQU?&3%a8rJ!yz2>jYH>C+{lT5-7o?bCCDKg`{pJTOY1<3V}v1cj4e6<TH&ue%n=Nsqzv{RMe=N8X5rS|}v$ytglR@Or<Raey)g9{_b;;kV)JE!v=R317Nw1?+M_b`1f9QdsnAJ{yMZmOK|W+b*SPsx1{S@>gMMuNEDp2k`<^~F^M)&RHP&qJ`<ES0=w$)FUh%}66{=0PQHdkW?8Bt!4oh{kw;a}@=|kLVHp%%c&u(X&D`ZXo_luTR{Bap>Cwg)h%?wkCGKAy}FlqAdos{jdn6Iou7ND8ly79FtK}!!w2@;7nyNcZ~0?_MT&uJ51oWXCJyI21p${yYUoT=)%jOj!0^rB)fEl!RPWViKB|*d^w%tQII|cJ-$Ys_>=vrN##TUA4LQLBJL5hSn7N(CwGR*tDTv|xuGSq2xFKmHPIgDj4M2$dJJ~8H;zJqqh+Ekc??5;3~Vo?HF;Vib@{TAsNGA!GB)!p6PzL|C~MFZJN9zJ!rahzNpPFVI>x+R)(~h9TUBK}lEeJ4THJx}j!=l>wa>F%5~G<)CUNR;XO-Zwv&8OFK})&32^NtBs9Bbxh?d0{lpQISJ?K<5rz!o1{n^U*z$k!=2uo5k>bn2q2<<(!;9z;Mg<_QEu`obU3JErJPRQAsM5~hDFjd)9)hl;3N|lKxt<wDNFNM~zEJQ)!BP@%iJdjeD2u?Pg+8ajG%*$vuDVW#=lz~mlurcL;Fc6$6HbHsL%Vf7W)Myy<(gb5eGgB_G{IvA)VhYt`_1&J9vxGJ`CVP*maS#4~BN|-pwU+HfEm?wQd1{8W9USKzmt1Fp3O^>e70@-&J29}%RtpGh%St1v200%sRU9aQ4XgC4Cbb45Q_ViM+?T6e2bh!I%`*Kl<gu^Eiorh_48@C3Yd-p_d~_qtTku6l9s_`i94OIaBC9R({hS!jV8ixPMX*`SF<)yDN0v3Wc(de5a=}|o`C{E2go8w8vg=Uc3?jDv=}bX??{hwPmB0j&5UtzjgNhm32P^13|H<tf`K(<VhC?@{uu*`Tl?WP)vGBICT98>Sh$I-UzqkdT>NF@DZ8Gz`tKnyPS6fAo40#$Whbu5L9NNb<y5D3@*#=<_y=`kid1Bs@Qc7ljS-KuYW(m$2_$X=melFmlK~LMfO|D2%_8!WNGo@Hc(InAUY%0B}ipnr|EGwT84xA2fabCKohwSo3TjH45;(Bb@(#lN;zIaS+?GuN&&XGB9IO}OL>{NTp=54PhovUsjbf{QL-9(lG#@~5Y93uk442p6&bu9F&O0Ds53S*z%mCOo~J%D+_7sx2)2Jue;uZC_@vPV=Y#N_iLe&W7#pms5LO^RD~l9`V3N@B>4iL3=8RI4DYIsuBzpE^-_&P35&a2*+y6)DpH0(<8n#bHdoOS;R4<6f;gnFPRY%75n7j9t=afWku-(=ax_w1b4SgO#G4KjyRC2AhXeXZ6()q@u@G!1j5nHeHs1bDdsQzoT%k0w0QB4LwFa(+u-cqB)tvE&XQw+(q_OaJmeRA~(|IRb>6u8aEN=-I(ucdzz%jjZj)B*h!Y<Uv9N-II7vn?SN01DWkyUws&LfaeU}Y<I+Aqn&HjL#}LP}H2n?HnP+^zu{2Y($hy6bWqlX=L@q5wvwP+$rzr~wJP?auUq@D90<KMxFI==Te4%ZDh7b&ULrL<Ffvz1TeNJpoSw4(AD=90Mp;j+pDekAh7Nsy^b{N>@M}uF?36xUKF>HG(OQ+SNW!Ngob)0wN%^AQ$^Oac)6Ztuhad4%mUTiLBVGururH<gQtaWZ6$FY-ghxcJA@NHa+(43kaT{4xm8!id@P^EN5e(rb_sPiSuIib5!2SoB2kjqyE6Yz&DnA4>zcp10XnnB___Y>+=OVcPs`R)zGPhOj%01vZ@^0~l)4|23?PM>q0e0DR=Y?t;qnP?ZMpZFN^RG`)GE7O0FALn4(V~9()&5_Rp6$mM@how%}bT5>+QnZJo_MT_bC{J*b!&|1!EhADiliGDp$|t9L!edvpAXX+}O|$V8<JxWxq2M{_xl-`a%#}6?9?vtI{Wqs$*YrK9+sfUVzR*^Ay-sm%Ort&7U?iGy8`<oT?*;cIO^27VTg@~IihN!_k;TwpW>Oxbl%gsyJdieAQrv6mhEnN0XA<WY;qHTdC?rEp^9&8L+m}9X^ImHcWXe*23E1M@QKf?>So<9Ka&yUb0O@Uq%oTy1B%*FkhVHo;U|9zLPHTKaKlO2c;bR%=q(K+Ic4>Y1;d{cFWp+8wSr=l?h{GCa<*Xn3zu4>-ym5+H`AZZ_epE$X2BvR1r?uM57%_`(<L2!a=A<A64)eXctYPu9KRyI%>0bFI_Zjjxsp)<pTz+b~F<W|}#U#syYcs)<tjk^jRm0Z}>=JfRVj`bA8u_T34j)0Os@^KKA!7dW2}m7^rX2__{$p^+ZHag1{8XVpNGZ$AM%e*7fce#0Z4xvFtP=a_M_k~3sjgDcEVZmtpM)`YPAPIu;hRc1@6{)~WK}a;BUK3M5IWCeywVGJl70)-toY!-r&LATo+!bT;zy}{UL|swoOa$tJ!h(XgyNwpoZa?RLAycD<GsKg7cWuF+L=VGQapof*k%)%iYyOlk9Pr`1R<H6+G7$D3P_a(Y;rp$4%q_IdVmaTniIO;glos2*$T=5d<7C1WRe#ihUGrkHoC&Pk4wcEk!kKxen}c_9Lg9)%k`{)>d<+T<v&JR0#=@e=ln0er{>YHF2LuhKI^4-#mMHYlAQzMO3CP7ozs3*N?h*CYodM*O-B_Q3y#TJPv$(mfIp)ueYeZ~GTz78yRX82(g>I)Uby1P_)=peteqVzvPpeV3f=`|jbWYqZqpH<v+ze4sU1v?-X$R6<6X2xe&i)>!D*7JIhK=R=Zn`gDYNO|4U`?&z=t%FX|nq`+KFwj-Fb@tDfY0!cc`uOg3*oz_ZtPy*t1KB%H$%S_Qn(%IbFT2GbmT3ds>Bpk)(B%3;D^-57z;`!F8Y7|7*)r@e50B;~24k4Q@*z5oY10In_M*LjH2OX-f*#*y<t|v}LT~=+{bIwEv<fkFnilGgfJU3C#)!eSNt>XkL9Yv-v1Ms!mogiA+YeY9;s1g6g|bwJ`-^?PS`_l4*eTFF%)#s2tVt$=>AH{aZWWZD5{;*1!M$|NQY}OB=bl)5shjOLi2!YRK<Uw@Qk+rTfcfG*)8pt7g~ccF(@?x;ER6W0W0i%#_3RdY;ad0?TS7+zsFHbnSf@s@IdsOsB#$af{X9^p>1K>bUGn#eC2fbkz_A&Z(>M+&RU!WHpbe+s+Jz1YWID54B+mZT{98#D1?>ANsQMG9SLa=O=Za$Bt#PGE4yGl|ANMXVf<3n?&W1ST}HFz_*mO1NsHazQ2kk`<}0qM2euGS#K|qxf$ZZUgmMV4Mpv_G0zGJI$W4~tT)2X?lkjc)yQQ{*W2i}7>HyR@mq2=nbF1CWy=Joq#9}<{3#Y?dCfq#I(26j*M@uo@bMDCg#vpB(XV$?hwH7@8<g1NMvtjRfCmz$ZbGq)7ixll^|tnEw17H?E)V^TbV>9*fvVDaySs)0Hx8b&EnhFTr{FklHUO8T4rR+Jzzp_j<DTc~VZ8Q2Zd-!flgoDaZiTW#S;AP|o8i_cacJvu0w?UlM#uLds(9Pas8(d?i`i(OAM0Rpn-$rZ3xEl7-I$)~tAW*`mVK%$d(6y7UJBqDI8X5_XKPZEoc(<&CcHzs<oUw!xB^5@SKw7`C64&`cFuVz2-t}VnbHUVxvr-N@0Fe1&e^QxR$vyQQrXm}&&4y{>NRl*HE}Ep&2=<`!3+qP6_`y8R{bWFz`{f~Ka|%PK1(*2Q|M`Fvt!`<i**Q$-=iiH>f}1*mpw^D91LLVc<U%ZAR(Bl&5Ias%DqYs(m1@B^@9{BNpD%4oDqsJv+&f|4d!^Bxp6eJd`|;&saVll<7M#J$9)$O<txVN|9qbBQgm4xo$MCE*DdW^P3Vn_nOIbWTNc&L%rJ!#3OiSGd;KZBh9QdK(mtH**T=gf^#_;BYzBOc{O%*_uBa<m)faik6t57o3X|dm;eksIN~pn?j=>C_@<p+~0p&uVu&WBY-89E(LZ&WS`W|YPPIv>O_xOr5-e@joGL(S;t1-)5fEPXb`&_sg;@MZpk;Gd8RJO*X($s0nGetgaeazCpjrO|%yVSA6(ce|j<E5?`|EO@|RMsonoQ6|~sjQY@v}_W2q6&;}DfCVG?v(m>&Y+$a@7GyA(d-O39YpNsK~QZ%R<_9PaZKp`T02brs}6Z<(Uk{;dM3z62t1ereX=&4zaOQHlRNeJY8&O9tV%zgTc{iOd?R1!c*+_6jX>gdixs=;Hy`HrU*A4vI#T-1wL;(dv)DV=ro+$j;x!%rTA=;c(5>-CFHu8x8TVvNaItVfw0;iEZ9FQ=vA7q%czhWCDlK7z49ytUD6pJ1N0uD%hwFK}WwPO`RJCCw{3JB|s1P+jk~+bJZm-0<TsZnLW%t|COVN!PVnk=Mpl6VIl`Xjj=rkR<%)6|gGKY#$Xns+)oOc1~1W8VX5#~Eg7~nC*>w|O*15FXHJI-o?nZ_vhf^_`j@49n6&;1gn%i+FZjo^xm6)%^q2<W>i^mjDphX={<HQx8<L;u^4zy0#tkMQB=gTHSVhwc5>AAb*@N46CD1P9nhSlwgICG}avE-?dp_5ob{68HuoK!!HB)`Njo%GiW<ZQ(AwzT%tPAs*K(enDRQ?2GDMpK7M<_g_DZ|N7O#EM!ZJ#OZhVn!~(Rc*|IKS8jAd%sw<+nbDd_GS8x&dUkaG{l`azr4D;0hg}|)(N*92<IlbchT@o~C3aQ}_u5xBEHbM2w}1Zi*FXK&?|=EXe}*R_4(xHw;*Xt%u1WNp63W9eyH?=qs>i>G*?cVgP`GDlI%jBDKfzc}qkn9_Cl(UdwD}IWQ;J;!;FcKO^_fO`dIf|m?S;>1Xm}jqucL?0@0T^*lc!zu`-F#v7cj0XZxb>asH{;={2Z=xPZm!3$>C>=dcx2U#K9|pPL|b2$a?h9?~V6ly?-Bl4=CYedFo+(Q8^}9`|dZt<x<P(l-ohx6^V|GJbwblUh)9H{Qa+g`{mceUOrCueJn%Z{Av%SafthPS3M@lTSWNB)lV>B4Jf7$chy891HKoV4U#!ULzg*MG#DQ4i=F1;1A>l?1$c+c?q}bgxnwWy!IwwV`i*su@EDb(UNU=}@}VVcJwrp2L`^OF)3jqoS^MgHf38<Uh(uX4u%nxxf+KLIE**6qwaqUPK&(Ha_P8d=zhx<vb4)P1jdQ@kHQAfHDW8}x38#D{5)sE=-|N$7-{OWT--i7Ku?^&cS=A9|f%f71OUD{9Fzm1DTzqf6Z;(74w8K-lW7WRfV@Rt=Yf#mLptJPEeQS~*v3mBH<~r8kM*ib3@9+O1#RMNW<u2+D5orj3X^$oU{Nu#=Xbbyxie&eLiGs|9gi^<ewMUb=cn@U7A9EOQH~*oH={#@%Gcw&5l4p;x4sK()mDGEXpFh^I{j~Y~9-}Le&KF+VJi2v*rLk!pj*-Z71`m#gU`2|Oi@=W>Zz>dyU}FJb!T(GuiGH$i9Hc)@Fs04HBGz271z9?OY|6C=*O*D}`Ufr{Iv$(KXgp%*w-WAPkj`^zL&snyRSs|ki<yaFBRj^ih=+_Wb&hg$yGFp{IyU9hml9y(_qt$X(~by|Iz(+tcwmgNBa+EP!{7QcUS(>GEpO2SL7t7nIZ^BlNW6otmw2>Ofy`~eu#pHD`!)w+oNP_pON2>NR(=)KbT1!gM{2w<eLa=V%$rwVTIjdzx*T)bd-_hI8P@(Li9N?@=ov-yE<t*`6{7%ud~&hpocK^~uqOrEs}y(c=v1hA(ITDJp(Wn=F_sSQK`qtGb5M>$GTr-{Wk6U95wflElzY0K1KY~NAmH$4nWxsJg$h)O?=<bNWu+><Zv5->;1=gBS$h3%2~`=c%KiDrkAJ+&bjtbY&7(UP&ThlMf(UjGjg;hAvNvWq=QaIL%!^R8rIFZNf<JTa;hr8G0u}><T`SnL3MotWHF&!T!15U7=3>=2Q8krmU@=18n>Q}l$3M`SYeLc%J|*UWet`ZGNReq(vyWdl&S|rix|_>j_&8zcIj#1a`T=%fdx$a)WbOHYF9t~!EiFF&@zZvjve!oN7qk55`ml+upl|4ysWb<S$PD$pG8SLp;6yJwEwrV_uh9V}C_KbL9UTTft>|%wTYl`iB%sdS>_!uqlrbZO0^qFKP6&Wb^MzUe93_GeoEHNz&OE+M&n24hRq(S3Bar}Qk`~u$TCC}5WiSKeoU`nZaytb-%I`b&r_?=_8M3#uq;i_wbuARwNW)xw;SKg+;p(XjNCwn^R=0sA#`HNAs3pm^ujfWya7s>Ap6j`Vji74u(jNgWr0#1;S%OkPQzps5N|e*$t!p=r8Tv0K=kNeDxT<Q@Uh|GkYf=@hJfr}O6W#B0XIS}O?XNasWNMPK#O$P3)VGW+rf|7FN4?!j8xq}LSz)%BMS)>VQ#<aaY~$-Hd=M(n?i>P=2_nG8n`xkbEYtXoLYZdKKq8sRVHg@Y_C)3$bf~LP?Cgip%`hqvHJ!x1|0JG>(NPNfa9Z~O^BX*;Sy5x(ZRT}VG3-#TQF3J0V>jJ;$xdRA0j$XT5K2wLIyG_-A7w&#5UqG<&78KibjzpP(r0A>GD8_&TD+>**y*;~GNv(jXKz;A4Sl_)o8(3$G6pQokn6>QLHI6=I*K4dbl@n4wVrMYaxDu+{(Z?a0|Yg2p;MiP@zuv={oXfaY5+_CO%-ERDmx7P3z!}@V<is9KIU+@pQE;BE&!aK{6@Sy4X**g6@#=SV`@=Pm0fnfK06KfH`p+JrR+R1cau5MS#H9|0=gKz<I!Jwqzh_#)0if{9c=*?LUI(WX@n+M<B@G}RuQm-d9qxMmJeIWKD$%n(vkc?x&ieyD;~v3EoEF4-jau`YlXh{d@ZM?qdn?-SQ?qXGp)Auc_E8zK8TY-hBCEYhzBLCYFvg;dIR@9_VC9!-D-knmS8ajG7-$sh4XisZ*Cs}WCn{oAgp-fSo338Q%`U07tA#AEFqtI9B`pYoAls6=CXA0{Klvl5R8GAjZz73YM>&3g`Gr!w)<wJ#-p`r_-_>_JEL=!k0$Vx3PrYjc^l9~TwX4s&@jiV#WkrJ;!-d3EBMuPye!RxKI%NJi%+U<GfitW6oGkP1J7k^F8kLkvqtwcZ;V+Dd>Q5JVlDf3bq5#ly?%pR{sKeux>70Rf7$qIO1Voe*z|hV!Oc6yhd%bf=IC1|7rL8dvDY=go6rGBO&J_MV>+moJ0<QB0+&(c;JgKRTKj-uu7tA|f1Z*(Zex;ovm4Bd)lK`JA|*Zj>2xfME4Ump0uh)*fxp3Ig3;VxBu4C2KY_qq*b~OXk<+o@ovhQk*-=#i%gYM=8F<chky_^X3$wwbx=yqgk`y<{%*{IYbf4;^;H=gafy7_wS>}d&N`7a=*K$}Xx0<E!C~F26#U;s<YbbbME697lagykCfd-H)rE*tU48NxkOGsNdx6B4_H``gJ1^!Ic8XV$o^vG!sHmUFg56zd9$j?YtZA$^Q=+MQO6`WCjGt2(RpQ7BNID@rUg#{kFxcXHBb|;xL0@vm1U2<GBO}9F2ex4F}B(NobahFLcZ)eP#%~R;In6VBYsrF@$doR6B(6>TMPjNVg<5r)E10hPq<wO?+m`(7SWS<igYP!y3s5F!5j6j(JL8(u;#L3gnJk6x13#R2!0lSmeGgBI*sit(R6iEsfyf%XYh$K^Ipmg*^O?SU{Bvrwl^_^R=hD@^KbA#q{=v&Fa!3-taI{K&vQuiRhZc5h8TrGEMV2kk_l6)qDm!f>^vqQ>$=A7&2Myza?jtFVK4XzH52k2!eVfq^?;!w{-eQ?W;xlK-f8Xb_85_0I?LF8yyIFB%h)H2Ms*@hQ#a16~a_>WmF^qFr;aTD7Ex3qBvn9P94LdSlN)#l|Omp!`qrAo)u3IL0jR6ynybLj+_C};kC5$3E3^AH;Y3y&gLA|&-4)k0k~37T6g7Vm-c9#lbusi(*DqniLf7Y_VZ0CzuzIJz|(Mm&?)!aO(JdK_S2Mx~<QkVkkymrOVrcKcf0&qE-y1<=uSM0=@q%mXj5*s6ligMEl68G6@7h{}V!tKt}bM302)JQ|@ZJu5V60D|)L`ov8bhrUfv9S&LXz=VT13}th}RL9WM^z?#AgswQbF|K1W&T8n4q6|1w*~=Ys99B2nG0Gjr_wCt-u8GIm37lP)u5)#>kGN@`2AhVqO7|+EaZ&jzCm}tM5yzm%*VspYvR^f+oCwG#M{Fk|?=h?P&gY)-tA;{%XHtG{c>OHKC6@Fe!p5Akh$rHY!LIhkQFM2-OtgcQwM85Q+Y6~(p2SF9zN|KHx5u#j%sk7KuE+{XFa%|BdbtN>ZusvcpxUJEW8N<7pS6dr00SONXnt5N@=cZUlsTr;YoBMkx=izuOh3^fpDQ7rX9>rq;&^g-69_B|P_ryW5dfX==aVDFvIm`#$+Ri!VSl#rJ)qe)=wP<4wB$C`kd(&}+IwIX!SY}W6@60NA0SJSW1uEF*FRx5Y!a=opyHN`HCzrvknc{XRhV0-OyqZeDRcv7Aqol~VXZg?D!?_PjU;%oDHQMxL%-%_v^!BuU=Yg5rp4))gg^izgM4{jCcA5;#$%e7CK#O{ttn-)@8?u{iDiX?s`_qE7h%FX9h1Gs)VK%#zYz^C_gWWzqP!~6+dMVHx?RGJ4@vu^J>i&ONxv$1CkE)A3Bjg|GSi5vY2k==DGn6i*H!vev%-Usss1gM4dfcujIrMFwg7kC+_YlYZF3$A4}@G95h|%G`ns3%I=KZ>2Ah@8^>oJM;#Ov%A`l~qUGTI>mIlDa3U!3wXFMjj+VI2YazKXKw;yN<)62t=wH9Y(wE~M=Pu?FFw$~JG8tL%_*CC<Z%m`G7#UzL=_h~=pb5}PVD9N<0F?NB_&0(}Ptc>~mC$|iiH{WON;;~i{Q(hPa>RG9zX<HCpXI2w4t0s}(#jT9wYr4^{PtVI7ewLTH$^5D)I;<SF!FZl%W98_6lR2jwgL{MrqEe^GaD`|5x+SHi%u=&*28vUYmI~m*rR9ye&}RUePv>oNRoJqZQ)c8Tt5}M*i8f?Y>0ecJhq-lG8IAz)bbyQVCO$oRm)D$U>8K_4==OVHoDcK2_Nh-@=g8bYoE0`nrK(M!^S0NM@>Pcsx?Zg0AfKnxS=q-v?KzoXB*TR%#}}wd=2k47VP_2uHGI>#YLDgznv;96os(EP0Kk~pD1|^fSx`p>2~OmE2lll<L2T8QRSQ9p#x|PUT`{w8@g}K}USrq>Ho!xd!-~l+Nm_wyx>u<(IksJdyr_WelKTa=Bx3)ckvgV5CZw;9L@bNJF3oc{Mv{s}zj@PhDT?_#RvX=<<u<*lElIIp1=b$FRC<hjrs?OUM8-3N>-epK+9De+IH?PVm>aqDD(pT>zx@%0-HrLKwwp!T-3alD!lYy+faO+ejH8OU+z$8zsWJpwZhJQX9|uRi@HB1ttMn_sMR*TQ%`Jl@0PaOw!);<jDZ2i8n$)Jvgq(bL5Y*2_PJqbger-qoFf^SgF|p3bwqp^k_&n;iM;6j9Vro;L0jON<EaLLuMnb8<!lw+=IbF%PSZF7q@fgEIQLT?-plb)zf=gadVj#m@YG-k%RdiU&{fT}7rB0%s2cE=7<E3c}xbujp8W`Me8MaEYALqNc83)d>FEHh%S(b5d74=?h@n@kXK8VV$Z`hU1&EYt9vUKtOI0cH1YZ01;lcP(fvUbB*L4U9mwaL#NkF<62X*nl!SF)!_SO?N(t2hq+kOe=xbZal;_F9up^M?JLy4lh+a8*g8tXj+@fj4IL=5v7qVeDvgseaCR^63vb(Nx-hW}=XsKJR15Q$fL^4@kfqZw`V!hPZUw9QjO8Egt#PAT|QSzZXhtDIVoL?LiXsU+OiR&x5eJ#Y&1PQ+w=5dL{gI$4FIu3Dqj{)_jK6=#-yaq!L5vkjgH78pn!-&Rxx>vrOGP?x6IAq{@GF*wD@cE*rK)lk=A^jC0}O<fo+q7XZ4<Qojef$I^yLH3dy6(Gf9ERnK`|UsOMRHwagIGUSAFVVUnfVu<25<ldbAe0I^&H)-B$J(o;*4e)zgBu1qO>!=AY%gtpf0(jsK890JbNi-UrB--WST?YS*YcNDVp?QCyXc_AaOc!T#X&vw3dt#7fD)KO?etx$Heoi{Y`T*H~EXh{Ub-=4JySfgn!8IpaV!he&49pxPwJeKGxWaq&$cu0Z(8-Ugpwd7`o^M6dR>jCzVmZKW)v&wflQJi`^7rmynWatf_z-|%ctyQhm*p|5%_WOe%Z-&H3SCWEqF)<Ro<Cmp3Vt2>0AQD}?-^?p+=t9Z-87X6-eUEls|^wJmk(v?b~PPnaPc35L(W~iJLjhgWoOEgCpluD;P&}NT5Xm+2DcNt=LekNHmN3MHT`3rQ=e`-ci}0*Qo-ZirK&dHIiGcvl?ZL^Wg#y{IAxFVO26PqQZkh8;u8cPSCx?PL|c+tpWk!%u!b@!CU=Cl^3R$6Ct)7Zyw5ev$|O$cy+COgFIr4vn*6|0T&PmUZKRzT<E}`S5!MD5E=*v#lFQ)&%vmKMmCDW7w2Vxtwna;tB{0FZa&#>%_nYt#`D<Olfq<_-wunr!8Tnuv_KJuGE~aB#u(?P1t!d=NDAySUG_Vr0LqtoK{}^cr^?TZ;^S}7wnn%OB0H5dltf<@-m!PvscEXM8>7ajgPWx3_cDXOF>7qIWGgaU=I3{a7bN2MU{EWK&-3CO+v;j_)enB6S7ELA!Mf0hsmGy;A)yGlVq@XfImIIp6uugt|@Cfj0R6EPzq&g-lAsZj>qG9zTFZv5Mo>UOmz6ALWpKsuHvnPnRRCdt=$J5Bt$qw>pIkv%$0Vrmw*l!G9rnZ6(MmrXKb`+yyUoRoulZ$*>AX6gebZ@uLXkP&!Xb}(wq}Jv3S!|ZgkNN>c#dV+B|7)v*@e4~i<`}W)w%V3LhRs5jbJ+y)h5Y4m(@u=yR+nd?jf)jWzgG+G#e;cz{Ec8E>J%&uFrmuvMc^oYpt8A-6TA61NvbVaFn~;nJ2l~ZXPNrlsPdR%+U5K6Mq19FANKqJI@*s^YASnbZRJgs3{j<&-+%vq{&+HxjRxdtO^%OAa1Hv(zdllLFx_7^qp=cfUq$3Lw^{p**T>m*9HZ<Y45u{1*YkAd4p{mkq0jJd)ZIvxJ#NnI8w|*I)SGf<;wn<zu{8%@XN~$D`%*Czl-WS_fPwQ^OHG%j$XRcf-F8nfobqaZdT2INI5%h8<2!n<7!~?5^J*WymFFk*cE;-Do+LE%PS&~HP2n(6E+j?^91!p=WyFAT#<K6P0`I=(D<#e|a%j|gdx<{JP>A<3hwE)9qV2{!h8IN4Fm+hR)XnZR^VHJF<#X5D=(bge)Dv+>avh`5h2mw)1gE50h9C+m)?IndUpI5rQFrS(gIO^_6RD2^H4SLeerM#|AknwpYTZwXJ#Li1YSe-tz3Ha^1o))!<k#EUs|5tA61tf4Gm;zGgL?rEt+%^t7BIB<oNf6su^j}5Z?jRiB&{b~XaP{LPlNe9PY+YI7xK;$|DRl~!&57i1iXYNC!Y{EX}I-?YubvizzOp^YWiSQrTGti0U7ONWSw1Z^CcT|0p38a8`I5wHE3GYvQL#|k6H7`vjO}7=izl=OWk*C_V=lno(>s~=j+9z2oNV-VNxZ>?~I0T=bV><P@<?_DJ=?+uzGs%iZ-HYEIVeimYbbfKuYC#pFS7QbgK)-rTWCNEc6}Hd<8QgU{+u@uc50aHPOuv+%@9Pl4s^@j9NnP82J8TF#)6PsELGn%nn?6Ppspi7`cwOjyeJo9ID#92;-*2yyPH_!;3jSNa>O^l*P#zp$IbzxP$tf<9X)B(ah;R4a}wQMQ@FluVWwg9YU0y7^na9S-op0*yyphfV(^|I51(c7ZHI{e|jAkGwZ1M#w@0vnQMAWr0c-Jfo`Jj@i`If!-Kin;Ij`WY4-8%Xj8(4G+PNDCgkqJ=C05xSmPJz$`q#HrCW@xT+$sp=DYbjWmmodZVElpfZ`b*`^8y~V>*&AhXDjjOf_I0;8~PK*g<U2r08{c<eNiNG&U_q$gI=QDLoeZT2NLEN>QtH4PSKP8ckg?7(JXtov@eo=CR1>Q=pdQ38%?#T*5whi5Z$>IveXx6Bx(v4N)>=SV#&FIJ-oT(NsXbv}mjiuUi#}#JF&~y0AWaFi2y_F`V(ywEAZXJtN`W>~Pfc)<)kD+--ey$f7M?LzCsW-fMe|e(O_T0QmvmAc>$+las0hNW*{!GCf{)o{>n4*wwIiwVj%8eo~bRc0uqdO)ZG2nn{I-gj>$34YpK!siT2yAFWHI^}czu3Bu`$8vJvjwFAtg0~)%{H70r<sd8<AccwYOYC^|IXImuo!?IU|3p>d{8Ag^Z^-^e!_H!`m-$9wqYbt(>TgK(gm^$6U?B{_2bGluT4#7I#U+a0Tf2GS<`4mDABosqlXBEAIqz4SFWp2bvs$hv#ix%@9XSqVkX%zZyeK@r9ls7ynAEn}*dmLies(qayL#2-A&^2>`?_^e5y>s0yoqD<5ZV~%){pQ1d{_ESvOh?M>zE+sse-^R(>hyAEOA5{w#WT`!5j$J$<J7cnUYXf9O-s)*Tr~Z0{-v+73=I3}B#touE-^jK4`k%lUu<G0Ob{s`Y9?{qTon+vxtY2*u$^NVXo~n);o2LRY0RKq(D#4*U6#Zc!A)L5E?~jLX{8kzD{d8A5t@Pa#mby?8#HwL{><z9+mFBf^4pK_;b#-JZx_Po_g{bfJ$(MN5@wj&BeQ({X0X}EnoCyBh^J+;ZmkhGNAdXK$FD=M!S~MfHde~mgm!J=F1)_to69;9*DQV!KP<m6?b^kR=N2Jc<p1~I|NZ{~ql~Bc')))
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
