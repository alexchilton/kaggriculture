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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_NkvK;td_}mYb-<kV1hb-|BBH08vR6#2c2Y0o1Az-1!;!1B9`tLi_omrI`Zf<TKS$%k}R!?m9ba%yvM})h%x%t0-^MCx)fBWZe{<r`1uiyM%|MV~a^`HOc%a`B$^69tVzWL+joB#4p|Ih#V-@bg~%a{N4pZ?|l{^$Sx<?H|S&0l{1kAM5+*VpfU|Mv4YFW=n$dj0g}zfJeYi}O$2<?BEFcKz|k!}tF9A20jQ{Q33Q&wuql^!V%K(}u7A^4A}Jy?&#9@%7Jq`uT^SK7IXwZ(ncUytL-qzy0-k{pIUF6r=v__4nhbzbxJl-~RjGe_8+3*FUtb=3|QcuZ};xpL6j^_aA&8%Hbn-e~x|DUw;4L$M633<wrjM{&nighrKWA;lql*5>D{PPv2hA{5(S%t+jmlUSuuB2jNlOuD^YL`{LVA<pOx48Ng_Uay0ATRd?h*jB-!qbLO3f->%p1zI^|u>yNKL18Xg}jt}_Dg8uyZ{@0xE6o&HT88qb#woL|y01R%M$?enU>#yZkZ=0Zuw*lid1N(Ph$9)*j<D(wq*fw4|lezI|>-TQ>hhg50(ckyS&m5Qk$)j!Kb0uxE{h{~W5r#Y4(aySQ9zInxg~z{nm(u#V+v1r;TK~ZA^R`zBZ0dHQ??>RAgy?h4=2%m*ds2SB`?2dXcZp?Y#$lJc_~~b?JJ@Ho?(aXH{@~I(`<R7q<Buil9iK|(eb@<tg$3{G2QDbt&~*S$_*nb5l?4S)@2LeXKPvTy$)78}sB%A#i|je|v9kzXVz7<zb5sr#e#;)X(0O<aYyCIjuh_T!{=4fxDSzbk#~-iXe*W9PyZ-w5haZ3V-^(lR{+HknW?~EwIyrxH^E!%e!*jR3-Mb%sY5d5vw3O?oa)%#JY3aW!&X4E5daKK4>U=bqvT}KEr_si9?ma3@(El8>l6CjW<IjA|Fv0mfHQxJ8^KM&D9_{0HICED!=kA1^lh69(TUo{Ha%yj${L<MS{$E4MzxFSE1Ol4NJw*A!_m)Cfv5ncMm&N?-;ab<gT;S2W%swxC^bwlI{$6MoWPyvY^Yro}XeS(>yqc>+kXlXPCY~FuWUeHfKe?J`T}C?CaPkOY2gBX|;9o!e`XB1>46@31E2s&+q~*R3`$QNk@52rrQi9pgM?PuZ!0A1_0lqWk?>BfUdYtPiu}IgYIi_{^)mC99^bQ92VYsa94+6A*H40&$$O71LhK>k19)Bl9BH@~JX(%G}MOf}g`YQEs_})nHA{z`pky*%oR`OnZ*5@FY$UZRM7j@eJu8hpfYuDTk_^}p;N2czPjP}Ar=Mff--nxP+@JD8!>>Tks8_m3pp`m?N3{R^}go{rB%OyU(B1>I&-5LkKSWfUlJl8KlbCXOa;WBaqjUPenZ$s3u$`R`HkK(y);1PA6M|9q?L~&Ei`~!cy1e4&K?%)Rc!MJ~1g$KdBu*ctZDMR7km-l8{T#$$)pH}hg1Fuc^pc*&MBmAV@y5UbioX+}oNq_5u-K;9_>VA496eEPl>>B&Yn>z2RNTWR$Ch>jNI?xIHy%NVr`5*uUsqm}PkIQ|{fh)qjswX?N))Vp4CN&NUdd6wSOijg*;N!ldG^bX3O#m=}SP7WO%X97Lu#+guN=->|A?z7+EClegP9!r4a0xz0z<HG9EBkxu!1E}4Vip9Zw14iz>XXm;?$_5}vYrVD0fu@wivywO^5nH2A0C@?9$36Rh4a@&`DEuWgTI5QHwEXsGW`dxmhI2M`8XHPlOV%Wsk{3x+a)^hq<V}e>1iX2jIfc@9^d^QvMW&q@8`nen9ll`G&d*b?C&1$-#-8P>GqfFufP6BVB07%h(7P!!~i-GB;XP}F$;I@X0Q43cEtCm#0QM?7q6CDefa&{!Qbz3#z#?Sq<)l?Zv`9w6p+Pd>F$l7&TV1Pb|qrzS*U);t%i9ryA8p~3XYvKpK}Dhs-(77&X~uQ&LkG0r@)?fm&+`z>0{Sn(j=r#7vsA>k^<>Eb-?a_*aeARpeKNCh1@yZp9|L;%5%u}*Q2SNv<KF@4PZs=zeUr3__VLDKZ1dPn{I=s*I&Q`*cD7+FQJV1$)NmD=w1T+<wp4~DiePEHhpjHj2}zyOeOMz?tj3^CDf4P%|EZdcK!Z)i861p86Yi0VsV)#tvHgF+|CAb_p(5ZGYHIEfrx*oW`47|3^)IQAUKefPmGeQlFIQd%PdtY9da)|wQv6|yR5YQb#Hf#ux#MkQYax6Me1d_GL3KSK*3{D68QzM1{Jje6Wmv@e}4Vx)8|(S=mBs)O@D-Cta0@XoF_fZ(fx_Gzqm5RAmas-L|)*dYmJo!q1<VesWf`!mA$gv8X(t=N29AKIslP4y-G9(=y*x{N3~PApMhaIJIHuJ<e2Z=+Fb0&$~<Z4tFwtppmK3eKxdwnE^+06y9W_oYEE*iZn;~W8*Va9l;$_tT;5}<5<NP|ew+&j@zW1K{`)V>b-C<CeW=&VaPnFX?fwfkuy@mI+KhHVG2F?~>)Ag6!L3A;hW75)mxuG$*RO1p%O5qMym7m2M9G}PnEaqWu_)(C)-46eThM%WbzQkTkdIx9S3UIQ0nUj%_ec5$fmrl6;@qd*yb#K-4M43A9j>W)oeTTl&af7hQp`{z*E<Vt<3lNhw;#~*M<&a1H&6Qz`p=(z^#V30Ta$-X7V+I95Ot}Fq4$TLso=och(jrL)pG>^F$hS!+c^9MLF4g&mnbZwFFP6^)g6mH4Ho`v@9eug%qaR%V1?<yd%qD-!JS)|ujO{xO7h^Nyq62iBUw?x0w^@1;-Sdz*XkEF^`0*pmRlGb0T*=#l}Pl&`BpIeo05*&l)k>cN0R=a8piwV_~*(AvAiexo=B@y1V=!&1ErMN)|}F|U@#>3R{CW}j(d}Y6M(oTi6#l1-q+0$D~{3;Bp`PNI$Y&b2M!e{f}Kf?))ZfAvaJUa8O>jcML8zp(xkN@4&gm}Ho-sM51kLDSMp*wD8C;wfXD69rbco1*3d^k63goY|Ndl-Qv5@9b$xk>n6Q_89QE*LJ5ODl=d~$Z0PP!@VK+Q_{IX3%q^OdS?;nBuHud=!d+A51xt$|^q`dz2DDm<DhGd3W?wrrb(#7Cp6ofAx(tt(V+@@C7U9+%>jfH{xU`oLr8_%*5JP}^UF$44ju%Z@8h{O3*@-bf?p))P*EWkzLDeWp_C14+ZC^VJr`h=udrxV5<luIUKk<{O2#czOq7cE|isn)EXJtTWNgU^f=-OHdza6|sfNO=6CzAg{!o?A<TK)Yuh3(KCtTa2lr_kVuhj%NrT`!c!34ijZ+&lc2(Z19rt3eZMLvh4H<|H$kUL_wN77pR0Jnq?tLUZox5jHdhc@&bWyDafcoJ#*+mCRRiuHlwc)lP9ZAFw`eeKZ04D&{2#T!!J<@7TPVN!$i^^Yk1Wp*_rm-2?J>vU%E^VYtpi3HH_sFDd3;l=-=*29PI@%9<ZW23IZeDX&&eu8LaYB5{J|VNl|oaam{38r;G-Kz}R8FyJE#9nGBFO=(Ef8LkTOfby}ZpmE?GX82Cs<@3{~vH@f#fF$)wFrro9DXjz+L`Djpj5z&yvMmtQ5$d7mJ4PUdSHm95*In?$_VapsNFFZ+D0U0E+wVKP9nS*~dkAGB|XY@9tHNVvNL0m42WdX|4<69!H+a(`&!YblNfq4WOs(0SXG^%XGi~@^Ug|49Fo=SM2sWeJ=4)J0M)5He}*5auY1fqQzQ@;INr<nX@$W=^*3vA!F>b+mUT&P@7?WcFS$x0oF^!Rd)lZ@$<a0V|)X<z&arL+}^<4_<rI8vGRGRAKTnwoz9`uf{dQWa4|-omedyq;de>Nj;QFucFlY`{&VK$DLwSb_$rj)`DhE@SR}5l<+I;d*XX(ZU~?u#lIOM++iHx$^5MN8<e~ej0!hOT-iC64k;^YUfJG!lipDMA<bmD3q`)R`W2}mdpL~8ocCaadni1T!N-$d%kR0vcN8m(O2o}IkGu;UB@1O*(pOb1Evdveu4fGpr$WY>u)_Nd(!q>?-0Eo95}OlhT0RsBT+WTZpyGtPy~)fO}Xq$<)K`kI+Goww?yNry*o4Eq~y{9OaIzt6V6r1+#n)sm=SSqzxOiTZ(mC-s4#Z0^saRkRo_bpe7W39F?4RNK9d{}6~h3U_b8Xj8rsaR2Ba0g0u+HC)=XoC2kJgM-Ui$~QgDBZ>qnKnaW5Ppzx3c&f;;|kG2Vw<m>}i%0>~zs0SyM;hPqT&VA##y=J~h{S!x_s{(=HZ+SK)Z<(^QN0AdxJZ*;1atq8LL|GYH{`HNf~B`Hn@So)^qQ`)kqmbLhTv+hq<zq8iVR0hxd8%XW?Nwh<4=ySSTD_`WQVna@ec{Kv$z^SlrPeE6#C=L0*Y%OR!n+4i@wXGGuQnadMQ65T32e~Wr9oD@dDV!H3A>Nm?jZ>s`TAceE7QFDWQeWq@dcvwWpFC5S&8Gxx8;d?3(D2GFDzNxPRkvB`S|2bo+a)K;Z|@uc^F~GGh)L?|L&(<N(N?^9ADeMA;^RFWqxm_<NYvNl<=2j~Br7IJsDY_Q#v0V=a4qFEg=zR)eNKI$28bIGjsTPg<eMyhDW6uo0Z{*_7=bo>4^)dnCF`m^(|l48awm#cnC=Hcl)!R?6f*`2@V<Ta<_r1r<(-`*?mg-THNYd1K*OSn{J^k+#OUTvdZT+ynP8@@yrC+MB_-?X%WPQb0?uJb%ntFII3u5!*4eW-d-ZL{dXoBJ19L8{=a)A$WEinn!HZa}pKE;)=VblXlP{4@4X-Z)8iVI#6>eeUFnsyD-CJwg+H!cwE#ww8fRZg@=~kU@U1q})s<Q5nI1e{w#5I^X&~7T3OQVXUrpj*!$Mo#okmp~G<DWplf^-+gfr&Xw=m%+0XDTJe6#uD|b#O>3Y8|criFqyH<*8d4%f*OD+#su_|0H{Eob1xQ@*@*(Xk{Z*JBw-V;z|;#_yBYijQ!bv()qp6#6dVi>*g%u=k}aNH?mQMZZCK>NndnjkwRl)_XF+)r26JWfc+?dL$58G#uJj<H7})fcL{GIceHtJh#)fV76)9buRXc_EWc+ey($!|1Oo;^J#(i~rBlA?F`zlx%LR<As$V@=6xkR(hG?RQ?nCSiKpmR8T+|<cX5TMy`u)MmdS27rD43;HNul<L3pq7VEGa<~w`>U(kT7AASn7R5@)=6&9pD7mk=U64s;z>$2&!ESZ;4I=%aGMYRe%-~)&1y4(`PhP^ymOdHljrtvq365Smf9xN_*n-bw*u%R9jSEg#j<1<k-Bte|Rvy1@rhi$eHGsuu3SDd-2BErwId50VI|1perpz?>UE-GPHvl5HE#Z=~A<*5k!#;u2VwrI;0DZO*{_dHLm4FL@xoQ7ObVLHJQvmjbU4qPI(KWFqOXbntetN%ln0ulX<sHTN~Tni6Pd6D@M8VRIIO+D&r^Y6qcHy9EnUB7-wq%Hl>_|JRzjxv~&W}WqD$&8wgfu=tyBwM6=+hiDp#1hV<z%YUBc{u`XMw+FX`}I8}P^;-ad&5Ay0Uy-Z%oK<jZynQC}eSoTa#2NieIiKgaJ3Mp3`ORuFA#KW?9sBcIW63I1ds*smp3$MwYj<Hh4>SLwCJhvmM`2^hoVe^FckHiVde+584p^;YRj3~MfG?k|JYp82ipQJ5izzpKd#^CwK%XQeJ0Pb$LPPq+IQ}E|`rFx<TcUxJ!2W^v0n=0)ft>6$R3=&LT`2I$nB5sV_W>fkZzniF6-_QeRAu$F|3001yrH$_n1LHLDODvTbxx<XNW7U&DAgGjly~h}1Wy`jQzNJ(YyyoidjwLF<$SnG5EfrQt1YjDN+K7!!RgbqRG}P+T3-`l#LX|0Go`FK-N)#v*6OBO8^Cu~)qR<YXY@dhx$w|MK<utj@4ut}8%}&rJh8_;#EdZc5yg)VaTR=Y1SP7c!qTo;SC-=Tu+L;mC@Ky--=<rO`p<ax#qIL}_2@GDoPUU1+N+dMGq{^nd@60CAk0$$JiezP(z?EsNQb*Ef84yZt7CVC^Zrli?xm!{!bw-}(wb%7tG;%uu0Iq&mgxB-cy<u@9VjZj@Z}cJHYX10e0(SnF65(~939q}c%--~WM^d&aMh1)lD*ME0uCayy4x{@jxkz74@mTV16gjojEt4jyRLtT`Tc*>k6!pg~%L-=K6eZ<MKB1;H+|{jp*BA$(qe&XR+1T4kvrr_^+<&~A<Z~Ll0Tq0s#}YMNqe}F;_+og2=2Tc99RkM14n!w7dJIoYsDrXnSWj^0IZi2JzW5SrM>j9iwk1(LZI2jrrocz&Y<|BrU}(0-wE!(+&(){s@iE0>6S%9`mfN=h5Tyj@6Osy2d~ssNq~H)W>$BU&5TxDQ$uy?=xD~{HwA6|x%)=5Q1ym(aUwC25VR&765x4}zKF!!ZwECH_Tb+FrbOoO8e)t}oGD&MH>IIQPPo)GpL>|*&(1`@ZZV&g%#dSX@Qe{EzzhB1xI0-<xWP6crAeZ)RoWrca8?c@<xT>lW0QAz1s0?AUh`@HbBKfRlH{@qS{Yq@jA=3}QtsDjBPed8Gbl(XAxALpSH{HSu%1wtSbn#UY#SWH~gv*{n7A?d1KcW-`fJkLZq{?y)qY26YD=2zgDwy*Y<TPYrfC+jMNGgD*CefFQh(>037SO}9YlVuROw0_XVIm*>?lzcS31a~tFz7O(SC`BEP$P<r*iCN9)Pm!-<5yA`l0tBpdO=0RPDR~rB2)v5$D^%f0Yq<WDyn-lvOFQ!jeyY+U?y?K3XCvHR0Y*c_C8>i_XIfa7K$riH&@D;D>56EZZJ=xVr!P~Bw%JSaISWv4z3c4pxYv%dmDhA|J?`C^8ROsKXk#GxJukB4cXfY`<<h#%y_bmR0_UP89WLTI-PvCV^1oxF?}!k7o-{3<__5!IYINmG3GIj`cSnU0k+Ivmo842?e_;v`WgpqQ~a*miGrokQW!=-qXC2JOre2Sj8ULncLpo!BDW?}e+YRFbTO+OlMT;gH@Vv9cuGk8kxLnLZp)BNT&VFHlTRGfT^H5)01C<zXel>}0Ui4h|AXiOGNi-Se;oNEQtihe(T`pXKm1hN4n@$g4V@>NUaH}#G09JR8U-<i!3px2OxKZLuInSQ;?4jP_iBEFktRBKCvXJI&!=^x713Y$qE0TmCk0r7N3tfNu4e{AxQ%Na!r;pL+RORGZHLoAB3NV?MYAGU>HYVa!d#yez-V&NLQ6L6Wdl(h0pFCFLS3#aBI^FWb4m_D-wWWLWEBBJM<<8szzZ>R^iolalsd-OCA$PER?qYVdB^t3mc*5^>mE->EDciYy6=@v8q18fc~)~NDTV8LN*|L!(!z9JK@aaBa{7*LfzY4uQOT9i#l4XZ*B(*@PAFk5s*poh-|vN?3bd%%W>Yeh)*#oz)$OS?Kq^~8#T<1&&BbhJmj~;{N3GO#zJv-w5$wY9!CefSOJuu1qM#&R_`n#h$jUbmdY*KX7w^)GK{KmQqg`{`nvQf+40Vtr8AsN?hx1?TKZeAh?N=U&2SC!Ms4!!*utI<jM^x;w0^oubssP7dEiBQyN|G#&(kV5;sUdX>G_M?L>NCNSE<qtW-k6C!q#g_*$71lqe3g2IXmJkkVHvCp0zpO5bWGMwKsu?ePzIJdC>;5yggXtmM3F$HzJn8ec%szB(~@#y73>iz!KQ~-EWOJ;zhuKf&TL8SENw<39j&cj$;+vp31Lw^YiAdPmXOFpB=pLX=xWgn${AoFTOwY#Jzsl|qb96DU3kkyoHZW&I<0X?Ne0KBT=`ZgjlgmkEG_sxk2xiLca33$I++z$Nji5Y)yYb-^T2X;cfZ?p5@OPcWp=g~w?%Z-*%oS`0t8zvw5dGJ>~#t{fq@nY76qZwST9bm)+7EU1lOYjKB|CoTyYF=<ZCk6miZ=KN~SulcEMaNaCITcF$RlOQY?e!l#mAH6)0Q2cL}=SdMiQU*zsN(L6(u-<2m(QpYjBY+|O6o?ZXqEb7HrhUjJyXle49v{40UPcuF5N4lm0{BdU-7*pjNKxrjg?fglFYi4d^t&`y*H*yL)%3^XYSxJYVTP)@QcaJQvZCTL=skVuaaZH%INo2uKg&af=UKs%EYMfLcQ0oj(o1s2njEa*91w#91Ig9ikLS@~WRyRJm%5-_ZSog@td2^viRF~x)lLqG6V<#N<&p-_C%;txysv;?09wR13gmnfU`{E8~aN2xm8GY7Tc5Al(r6YJ40q>ka?`3(vdGo(5m_AsIl9uN_gK2tytswA+RG1LB4?nsr=g}e$avdFos)SOO0*#vt?kjXvpKHD<&aAK~3v_~NS?ruVk6|q0JCZ23_YB#K#8l}@dFlJzqZ8BfQvhj=>gMhVKN)KCT%#T8{ZK17(U|Bs&j2(L>aVb=oAwh~WiX1*V1f<$|v}}8`sU|QdYIj27nWc~TK_xKZ+_gk`A>z74T?EpNRsI~o722Z`hN&YjqhW1Fxr&O~q4SJR?2DrS;cZQ*Qsqj>zeEe^M5J!ap6`o#y9)dksj8hSEYV~#ao<<CCmeLdkA|7vkk$(5d69$TIJAypS&(GmoK+Up2ZG*P>1%uqdSc<e2xjMcX*Dr6anN@}xT+jHPY}s1cb)v$Q+)V<*b^$pQ3C$$9E(fJt!JZr7z;BNL7o$5;fa8?O+vOCmxPhIQPuc@jI8Qa<zX0F*L{R$FH?C;VjnQGDJ%0B52h|4U{p4qm<7lpkv=0q<5ZVTzVb)v@f<Qay-Yb>5K>eLE_e)?P(ni}grwXO<?`X>fQ<WyLt#eo)Wj@f?5oc_r3r1=J<c3AU2+g05{It-K_4eOL905As1tA)6bWpj5L#$Pywpm1pgIVokC-n+cEy#5BwzwFu#BK7Rjik4kjxLhwwHpe2hV2-$vOsj`;x)WsDhNJkP0sZKhAb#Br0ER<RTXSBv5c2+mU-A_YtjO$TR?I`oCX^5br+2g*^l=Mpkwu7N1E3H3X<7&0He#Hg)FilZ!%_pc3ELObKY)nSe0tL_>;>g9}nr!ctMCdl`FwMs1~1^gxThmE896(ab>y84&@v6Rf>P?8=jKrhXa?ppYY1pY<W<4P{Ub6Ds-E$0CRM8K`G7bLzZUT_eDo@5TAV-pcoN7u;Y>p#D@qCY(OO^deZI*KL<x(`E`_f6hfkuH)OY&WXk?p@lS6B&#R(7|}Tr7!|hx9&i!vdWq3(<(AfYaU?~_+hkvIjCJ$31b87N9iB!f1nnq|U&?KdgpD<?UC23ix)mfJ5RO1pooIV5>cpfO=tIPWpO6WvYbUKT;us=nR8jdMf1lPMPK#&hQCZ9wH^=sw$b3ECW*Q$}U1wP9N<^A_1?Ox>c3C&+w9A$39zuqqm-^=Pm);GmebTvs_)e5fVhY_i7OVs%X-74i#d|3mp%R9+4vk4_&UNBR(j?kIhf*<znGPRbMU?G7B(Ybzu<$|@O4*>~b2K2gAaKbwwvpROtHnA&T@b@XG7ky$>j=S^`~^Wm3-vAKV{+B7#2TNJH^=gs$-o8tx>!z4uQlSw0j6)75RqBF%rg?YlQq)6cx6=$>2^*Mui;`I#a(;<^&srxnv#F7iUa2RnVgEBDXk+L(h9feQ23Z&Wl&}<oXNj35kv)rUiA*De9F{m(M5`QLZA7RLeo*Nq+!f@oID1pLs}z<Ln*;xQX7Qz5D*Pv$3rg_pT$uCwAyBPA56u>9VE)xdu)peaeqeY*Hnw7ZU8k76$DShmn-bi7VH1>p4OInF`VGRahl9k=xu!}%f8MEPoPV|CzR11ZpIeIdzTa2nw8yyic;y4Tb~@{fXQ9Nx&c&jOF|(xR9Nlz_|$q4<tcikLP=KK*EqB<VoqEy1EVGpGp=*O(=}=-`N&0TGIWUCFHgWXgqrZU<4~kut17?tPH@kS{EhoE3n)i*hb0!}GnO{Z$K14rykmwE$hED=Lv%pw$gieKu9zM_?<Nzu1%eW0x^+fyfiX7A{f7X*RwF=Jm2%F7O-ec6)P<FW5yKYcq$<nH;Ii((?Fle~`MUv)?3PnvX_IZTqvtc)f?&RS!#gMCY##&O8VWgp_5^J|mEe-asgJI@JWgq)810W9pi3uYbB0^>$lvmv)97A_tvo9AiCBFLqt8U!K{aoyyFY?6{8$vrXCb+PK<h@Tc<ORc)BJ}bOyXKGPptP&49n^Z>Ko_uXLPhl(%A-%V%u7oXDLgYu!gVcgt$d=gLH=%B{RzQBG{K-wvq3LLTkYoIwE*U{ME|PD5-)z>FIHggAx~}5VR%=yZtLPW8~}mHUE*(@uwMAMxRg`I)*B%L1E2yS#1BsXG*ky8l@&>+A?fIifw5zeJvsrkwkLRz?n9Qdh6zoZ!|<GH-XGd=OAZRK*sNgneVdGHWeI_m7-`XJf||!8wFYoFS7#DuV&SBah?`XoAHnMEkP2s=bq}!&8JEPTE%YJdYr$!*vlJ5e{4Q@t3qWi;Ft+WP*rg%>o(vGR2Oi`bu!{k>MjX@O(P(x$Nh1`=5jT~VO-6D={walMalR`milvC+4BF&9E|-UZg<i&X9AW8`tkHvk!MZ5P;nu*=_(6ZSdrRIExxMH+Xxk>vxqjLQuowYJjoFtoT~S654|5sRQ21K=k5}FtybO6j0YIN?mW^x9i}%!tpsT-{3G`TrQxwVvpe<5JGSc&gnS0x1u!yR7+J^r@)*6q+2Qfqk%u^|N+totH;#&whG?`C(a~I-nhk7oN@ZQ|+5E-&^ldHi=o~OeTX<@=Q~L;`G@cWavdURtOiAMxCO{ryOjSFc|C){v#rd!3>Yh8q^u^+t4g9+J)myuyQeFN<#$rG)!g3(w<bypezx7;7%@e+Qf+R57pW!)(O-y}h{U9vp69gd}{|L3}M0}V=;JE^6Z;HUse#VMMPPmnATp|hC3ycoP;ZJYs6=MZ$d58i)LOjcBTYW~g247D_!}pvlGJtu)Y^UPACR*hJh&9HbPsf@1LBkxlZP01sjlApQm6D*Ac?ighP&f+cG&NGCr6;tRM{C-q&AFU#NM3c0#_DGzpv{0V;TpWn2UU*Q<coLCg3d-)DGSz%TCIF?wzA$Wr$tn(>_U_0*_6aD>cDBLlN=`2Tt{`ipRlkNDzq9d;K>YLt_q2l<|zxF1nW#tx<4gcViEY@e)C69AJNmp<E7RCt{%120|-Jznt-rrSj>qONOnJGO^&Q83^_A)BVwfNsDe32V_$E~#W@Y~y-B0Fn94$9J@${`)SB~HYFIVMs(3?*dJP#x%~G?shUE^{x(9jO1WI%`^#FD@k*^%ipwj`A-N&l>+UD}rz>(m`pPAM8C<vuEY-2=034QJfRSO-U$tUn)T%aeCT$6-VdPb0mo{{kc+9G0yj8t(`;EdZ<X>AXerM3u(5<yJ!X`84EKq5D}n1^8K>dFZ$Kp>zk*{W0-7%L?ue}FoS6?c59tt}5l{8TLob7G?VVEy66vXq7kyqBum&RDuJLO>1-A&FF>(Gd<=w_RII#Rm}k&eVux)TE>Z;_w5%$#BTA_m`5cCbT03NrfIOYMw|S7T}VRUgGSf51Bb?il6EGR#D?`T7omT{jAk6%Wg)-nzmXY2N-C02TzTt!5rgn?Nr_W4vFW>wO1?zi7K3^aAPKx*KkgzXdT2txz@Wp7N!^$ZIbATZ~1X3n^ykJT6ZRj(xZ|}=A~(v?I!G!5bvfdmJnQ{7)dQ;8+kE2R^rVAuB<7+xz6G@=~^Mm$qw*Pojv50UwXtI{kzmenu_-{K;K*_njlx6QY*!NA6z}pFAd6n^>3{2wBD5m1oANO4C8$bC~);vV^u9v-_zOvZuBsb`AJv`X<))zF+qw-JsXC<{+u(C?k>c*s=QO(Ik8+J=3=dFAL(<KVi1u$D`ht<9AUrXgqbGTuWz=4oV}~c2B)oeZgo5sz=o_P&ZfGgA|GW(bY?BLGaAe9e^Qs$SKA{XF;vdMPB3?azUfLwN5&=%$gp*lG4QBqtPJo|9$`Ml(dy11;P2Qg7pqp;{@Gl+|0z_rR9&7uV5##N5IG#yf;o6bc_VBfrnM5fJtN>ILK^H$?VM$e$j#fup3m{q;=BA;b#ELetRxZ{TvU&=XsRQxh_zfa>XQ&UTW^0fSY^{G^^Nyc0_A4}s0;NB0$>UdX2ka`&RUUX*C&-*6blfztMNWEK2g|{h1RfTRAOHYdsA0XvndR!+hP*M3YjKc>SdYCB$j1Cc|uKWSO@AeIwyWx=J=v;d$wFa+1~M+Z0==rJEr>X{26U`Nb=c@*~dhy<~U8=dVO-51{@{34=t)~J+&02RFR!3EaqjTIlF{Wn=R!E#61{&>I;)|FknIz_fMieaNqwgzyI*#cYpi#b$xrZp3|217rt&}owU5HfD@>406|{bQX1mfv3D4FX<jT4QJ`~x7j{zo4aKAbK!Pg%Ez3Pn3wG&?mGF{?_KCwg6cd}NR-2@f1FUS?Zkv249so+TSdtQo1^4%Wlg(A;fqY3DPi~)dINy<ePsCNRDY;C!-c1NFz$=oIfn_PquwC#;g(Qx3LH}-<$6Vf%679nt+o5PpUW%H}5BaaGjW}(FCIHfrPFXAmrO$&g6of8oP3wiNgz<k<nzZDn!flSRNNIHqiF(QPBMko~D3Jw@H(O}lI~)e`s15rwjVmv`WJREhPgUoUFaLeE!2zV<fKa^64u#a<m85;t*(vfe+xf`?Yvc{>>{h;OpROMXP8gV__}K57l?Swdb2E1HbbC|nJ>gXQ#o-s7RY{-7x2Z3SM}YX+xH&0kwGHI~bDDa5`^Ei-;h(Cj%0Et&OkZg(#Fn%hKOADZNtKA#gqNx4o!s4G8!LC^BF-OHhm>xIOu-{6Yb1%G7hqaqr<hxzx*s>MY#>K;<B253J_v}&$NM>p7=(1jG%o_Ytl`iChy^?9HxjVOjE*?DMVSGj8e){e=4tPoq0uZA+$iSKxIa{HXz|WU=Jdjae&RHRO%Bb1yd>~DWWSQTWZ+i|&83{cE9(Ov)zHH!x%kx+z>?=+J8WR)k?nI4Ltvhy+fSIA%B`Q$GM$~8yHSBAb+<q%s&|r9u9PTsG}Zy=G&dZ2AduImXWl1Hjbm^-^#}_v0Ji>%zmUlue!=rha}NnM=fak1kjG{AI*a1PUFODVKY#*=AisTY@qA%P@>Cp6GowiR46J6DU8!E~;@iS{m&^EXV8NMgeB7W~!>j-Qvi1RC+rAUw(_E&6?r>6&!n=Qh@N6exhUag}^ELp47FK1Gg@oRETbKul5e9F)X6ktT|MAxPm=}HjWmL5vshjRKhRh#yfpG%B72jb9s<QHb!i`k7AAS!kyGHg4hTA${=;RdZ*BSNE!r}ene|-7t|L;Hj_y7D~{`t#f{`H&Y>t{55Uk!0i?87st=9jOVe#o}h8X_tkSkYh%W1`g!?L2O_R|~7&1~JKf$-O!A4~G1Vw@;p{JCCEL?x%*b#2p69^p`_iBjeCoHkYB#*YOP(cyT{c+L&jqb-D`1DimnnH7I`k^z(Oj$o<pLKm7FR?MD6U_4>;@ZuB;pCRl9NYu42y2~-5uk8Uxi_kDzJ=WDd}7Sk|)%|{{9a?VFG@j97KR*H)rZn12d)%fg2h!(!rdoOV!);ovvi@|>WJucz_13BLN<zGWqh!GY$j(ZpA`}X_U45e7;ZMY*m_{?6}0!i(hX@}#;CZ~XOlpsSP%ZebJs9p??c~*JO&WJE*t5<Tlw^j5i(FDu=3u_RzLOPILVWQK8#g3Qgq$8EaXwyNb>$JU=18vlsVE+`58sW!?z}?_>TCm$bwsrFMfQrGi`{eq?{pNSU=6A4o`>>h3qe`hUTiAj3ZNyaZjA9*XU!$u=X~4jpa`$+MB0s>l>VlZg?(zK#m2%Zlzk~1nm=0$BZF|E0PEQz4-QLbmYt?j~!SgntCDP)%CjCG$qS+5(y5zb?RVepV{{`;>o*Gq_mRG!hBILpW1E1Zh;yvuITkRGqP4)J{U7h3(`KTxN@4N?=-@e`+_s`VVHEFIKobzobT6Dgx;s9IdJPk6{Mekz(a>e&E@^ytNax#svR6UwGWfns~KNKfb7qi<IbJ7WFv=<tH0=6WCzkFd>GR=C(%*`uk@?+dvFO=s<g>xzweHIjs5NLqbI_HZ{koIgoYyvGkDB*U`&9e}aC|rH8UKCNI?X=8ozN0D%Kcr5!My%L%^X5)&bYC7yzN?yWeY~x`T+Qo6<w|_aB<z{fK1Xo~C<_pEKy+7q9_2ME0~!xSP`vec?<Td*oS+gRkWpaoV0q^J@;oa}otOG3icFQHA>TiDxzv9yn`r#O%`>9dT;BCqpRk_Lc{ReN<?n)4MU@R1mrhXiM?HKqDTS|UXo+;`(#sN&0Ug@vXmckLZqW8HE(0M|j8VvDemrP;tK|^yP3g-e98<9!ll-EdS==!A>+<=5U6C<dqKjD5CbLNoFixa0@ivB89Rt%Bd-&SNWMSFbht;>P<B4u&*!dYuSkDdKs@j@?m$kh_*E@|#qR58+BMOz&JbZhJUWZuxp6Gho1fs0Z;@nX}8o9l+GP|Bxk->VLohwy6jAgeMJ+JLy2P`Vmdvr)e=Fm*~U`bge8?X=n+Q@aO>xc%uG=>)<S>OicyXANUTI3kOu6kSqG-P1;L($PHH{3~XbwjmI5Sb{5_Pm~$;38PZI!8VfE7}oT3OHrqnxQW8;TM%DNjXv!dbQ0(R^q|6P@+<1xS=q5Z<|JMG(t3^O?kh`2qJ&(RAGF#&7hS<YG^vP#vq|8`rDwo3I#TaOD82}*Fp5Mo-7GBb*eyM1bXJ!3zXVske8J}2a1vdAvf=1RXEyZ8|_HtKf4TR`B}0IC`P*91ye4+`d)4qckvj~<(d%+v5t36ke?ZYjj)md@~}E9;Jig-EATvnW`zD=Y>BKLM9X--eU3<%SGsg{Z3y?bU$?Vu>hgd*)x)k(g8<9!dE4gwO8_2m;JMs7<1Z_V+Nm4>R~RcIPx~5e>k#_N20WrXs-Deq&rBHF=n-F_0ZF(g?&!t}6+YU~nsxkhM=|BeB$_3O$mBYV`K&Redgt)8UX&3keC>9rqn9vk0^*8;ZUw1sN?(WEUG!iNtT5^~Ly|l}mapv^xhW=CGp*7l<o~ywOslG4a+CFO4@K9VY;hI|mn7GTT2x<2O(r=Q7LVGuK7R;?ym$z``e?#2JOsF&qX?vEN-KO%!xVF(HOCgabyF>08LcV}<wb%z8|<v+aFOUCn8=_mt4gyTwvo!|b<zH6uEhS5$uNIdv(LAoG%8a$^@X5*=MtCOzLmR6NSb*<ZgkK?ZHo5xIyovGhk>?q5-WTiS)b^3p^~eq;E&+Y7kq?uq(cS9DpU0$M4j;$z*xsx2|+ZtSc{Bi{=JAYE;t8DT>+*J<;Q4nEF~j~3iUfz<6Q<~j0Vkz$0WKKe+3gh?n4Sd*nW`{fnb14Of3w}?DEm(9(Hc;GZ-%N4A3WX5ki~YgrkMjr!terCi5tncQ`L?Q6-NVSYV7dC1r~jgk0$r>QH8;#wObc(=N*OQA0{wb8na)c(UL((Jz3P1au=2jwV@$`*ic9JD>S&X2MFL9%~Rr7ohw)adveIpRJ+w(zY+bs#IM}@e#hyX{c;M<WGlIjsXB9#mCyIxV{a4WSUT|UvN?c?T9ZAn<Ny!XO9(;Z?+vkSxIU;L{Td+G9^#0X;4H5h;UBU;m=~wjgBwLNj!esPDE~$MkovG=w*T;?YBhOaU>U*WSxvMA2H}sNxFT4i<4TqZ`Na@Qv;}Cfjz0#1C11zROVFShZZ6S(6-$|Ax>d&FD8rN*t6(a^VsE!FzC0+UWhWMC3)*xZ{xCUL4_3C!I?oR)~<@wU<Nrvu3;gdK-yJ9a7E!gJOlSKqF97SIF9+6i$Rsw2Cg2hX*GErzbG`C)}+dPu@1@LiVvCL9)U48{8{CN==@EV!=dB9X3I+3Li>SLr{oIV6CRJ+pPsXMX-m!cbWN9<hAy<az<MOkek&D|sa-9EDZpgxp$e_iGNfs~ze+#oK7m$No#c&K?V01P>viF}cn)1ShuRYr)GCBqneFcq&$X99+k~nYuh?M~5h;_SG2%3+b?xMx;;BuV14`U^(H@Oawuhamil>&JuOzi#nkwa60>%MB9C&Kl?MbB~E7Po6R*-y4w4nwSLm}-*-k~M3FMC4RAz<-b!s$rb*&OLmc}hueoPdSQxFhD3Qf;YF2O+kUJSH0FMeD(KLO8T7<V9!`FJ7P)9+I$BOcg;UM%D#J29q;BhCz#mC~wZw8*s+mt7ZnC3jlJYyUqta{c<KX$oG}SfdIBB3)2$voxBmF3P?sM5y8qd8dhGqVq-Uj`YGYqB_!>svK#lYQxV6nxJyFDar`L0)EtqLqn=?RIF_OI6w)o0=X)%T7|n?(hSbW^4ML~Lw*fW*1sE>M5jp7+ybV7iPausACokk*B6hI#M;>=vz!pVqE$y7k%>&EZh4mN){-Q!B$B*n}8s9pczD|)mbSO~CL`Vb#;~N5Nq@^De|L_L}hB1Dyor!_HKfp=o7NQtd+`uy6b@*O-p%J6kh(r+{A<MHUicVx5@={ZPZI+il(8kX&!{`b@7^y5Hfs%Pd?My+zy2)Lk0VCII(D;IQX<*EC0ep99D*?-Fbr7>j-vm0fDw7sF(z;tS5qatQynTi*$eaGAn!L_Mpj{#OQe&l1JIS?D_fiKtJ)XTLdH?9RPoTVtlU%cg24X{FCC2w8A-c<a$_Rbo1oAe6Q7m<q1(LdQ{Aa^*cafUQS>r;6?~jN+Zam2B3jG#<P@I*yjDaA_54n%7ePRgQJvZ|0nl34KF$BB_waZ_QCbAATlBQ>bYo)-+4UfV37;5}z@a}7lp)jEFY`YsOp{4ta!ceCQIjE=6BjVOUT{FwgmsH(Erhq{u3D*%Vc{Bh#ps<35NoObBr9yZm(~FXcA+m67Kc$KmVRSZ471u=`4RHu%r3Hj`b!{v2T4-jGr9s^Se`~yLr<12RK^WAGXlPEnb|d9CbZuqHK4%W29J=0fzBUSL2U%A$pIg?ILu66;a`=%J3{_!q!+$yWaDC=b9)>Z((1|3b9cs>ZS(TXRT1Lgdc~u2r6>HixR%vRo2*q92?xI>B$^XE2n8_)S8lHDNf8f_w*Qln6&Wwhe+ESBvG23U@C=|&eM~&1ixDHs?$;BeN&?_x7iVl#!sJi4Oy_O|qOkw4Q3K`JTnQB#;r6*;z>-Zf7%i^#6DM5S@Aa_$uG><BKVCoiSlzIH)3(oBS#^EBH%%o;j%mha_S5|C(<0&jA30I7J-iEuVAO%PZvmS(;vy^FQv4sh}%;AFxc|e1OIhJygvKYg0uuY{tAvW6}NUK3NgJjq`jZ!po{rmA_l2GAc2pAYrmnWni$pnLAu}rJS+J);8_Pq>#kkmEJ&7jr*5k;dbG;N%{tR!4l8)gW7f{BcJ3rC676!kpdPlWHr_W2?>3+@tcmXFmp(D|tb8pJ9r>|e*Te1Ktw1^E#H$P-PfWpj6hgpFplXp1GhLuk2ZcVcK%gQam71aO6R4eGfXTG@b^Y&QXHd4|`u<e@uZ$r&|?8q`3@Bos<5nsl7jTsYPsOV!zQ!yuFGX|GYj^k#=Cj%$Ze^{j#VhB49TBr%|h9;HbxA4|YjGP=yVv$zX8R}z}|a|t4M+TRqnlI(^>&hCpyLIP4?iGH9&+Ks%^O^glnAB7E+Y9|QB7!s-ffcy@b+k$3iOW}gipI(i;C|rat@N$Eun3|f|dr;AAckkHA31`;BL)|erg_z~qjd~yku^21s6BE_@;G&89KXl`nI89G&1SDy1f^BwMccV!}ZF}O$WA?eO64FG1_KJ8Sa#ROQ19%`j?H3#a1|07`)^`93r4!HE{2UrPC1@HXp7k>FWB8^<@I=Ty#4;{r#nQ&z^?f3;5kbm+x}-aDCJ#s4rCk7eygf>YlQ7B;RZ4^`8X>Hm+LVnmjb2KCr*Cd9#GSfYli#iB-Z~<?hvloN-dExF)0y>h!aUZZmIDo7MBorRWg!K^|H9(ZNqW7>a`ML7jP9Nk#Q^7IJQWNQsT5k%OWv||TvKJlN9iC;nvuw~x)-4IkVbKQE}({o7Hd5w9;*9ET`JHZiObBmBVj!+JAL!zTz_=R*rS1Xgc(_bnH#m*pK)Koh}r52ujSmHZg(DKh3KP0?>HBFojbLu3j3gZZAzxS5(Z<ol=0l>!I)JMdH5(8W|sRX$vOi(M59cOWOLesUg=&dWZu&_{En^b5{&8+pmDmBqR|p30Z1BE>)@vd0%5&f5{U}Ze<M!m&vQmh-KHYl+=87Exl;WLaj95Dy;E!L<DXdIMJROO>}Q<PBZOK}v}+w-ly?kXYpI%K_r*RiQq={EFs6{`@H%z4&V3~1!^*3a)H_(@P`R?IeQToTDGl0zNn~0`dH4wMnV7fg*bAXe74jZ*sez^L6VvZnv%ANucYG~@kq=+Y<KJG#FNjhzlthQ)fT+Y3w;ckjJXJL5(rxfL&5XgYh1U+|BS_~1?*;UL^juzo0v^i}_W*a9DC7obmnXG#|6KN$h(hY1OsZW|YQNV{s~WrSFLL9=JkHCzyy^TC?-=xjE(zNUE&&n92vfRswy|t~!Nq|GCBiloi(oq4tTPuoN?v5#U;2uL7JUs;8Ax@{){%ux+%Xnh50cqLxqhT`bicmPJ3%RaNyLeqVOq^VSj;QT*R!i<*`_gNTmg!%QzVUl<uqvNFLOmVlQ+!dqac(1veZ<yFyg$eb1@}BdC3a5(&vbabnZMu$(0<BCQx~d8Qs=6nnq>dvGyDML{Vrb9$^iU)jkV2Iwt4`YhAsLtgDtr(3~Lt=xFhSaD6qsj@{^p458b<q>@qbM22l5f`W_1-n_VA|8)=<P%lMwn_{^am=X~9qFNvw!y|n&RaR^Pv#~coP?8pVF0!ZEZA(5UkP_I?w?rX!G?t^yR4DnU@@0ldv(9jlX^1J&cxqcp5NeG}Qkr2EU+D5+4YR<7>%2j2QzsP?i1X~%3EwY~^~d!JecPs-Q<pm$Mv*D?kaSR4D9#W@p=g>Q@f+|6>%>L-SZ5}J^$2CjN;KqHNb3-XTK!X|Cv;QVf%-i)LL_$MTK9!~3>ZGX+i0;U(3YsIlJl2+lAAsw5M`u^PE0N0#qpfmWj>qO{46sa0TY7@0yE;BLp1?Qzr+~T1)tJ%U~bQ-r1^tw{<4cd-=p+3A<=i2%0p~5M2X>m6D;vTD9o@<phEOBt1pryuUNzBxb|nOAuG#AAuC-c3o$~Zr1efB)Y<^u<&~e?Lm5<m!)c{^QTpW`e#7}ot^56THG5T7jkX$6N{?KjmM&3Kb)54$hf%f&E!4SP{TIh)tJ{;*H;Du=FN;l}2_Q~qLuHR#-{z8(Oxz=Itx@D(dQS4NyA#Ps3MD`)ah)hetTQxi)6r8mT-(#4h%hwvAtI&A`+XAzRnwnGF>YIoLtTTXIc(<-j_H&Vbi)UfnG}Qdzx(y|7k&?g_h3s?^L@WmWd6APAAod$(`rd#RLb;yw1qx~6BWS7Uez#;8A_yYhw8=#;lt3%-33$?NWVcPXj^R@Zp3rqB53PGx<I56?SOLI&_>UaTqE3<#fZ0U(Zw)i=#l)ZxMnFY{uvhy_rrKjw*Ow?{XxF_AZz^<75+L+oZYpOLg4U66x9IExOXe#Rfxm^)l{jJTQxEP7DtP#==)*GkJ&QS*blLaEO%JrB|j{SQP5#kLSp`qn>b(L6!d1H^01kJGTc@tuv9T5{Ujt)=Sc=Kqmal3uA}vSc}r-<oC@pp$>{qqGk`6|9xg7_eNxBAOD>IrZbK-4s|)!gb2?zCW5Q5ytm<;c6a%lVdF;nYXVJ--S|AIaWC?~a^*Aexh6DAU<XV^x?kUP(_QWnSDIH|#G86-R@Hv0NJEzknVf?hxlm}&kS%JYdsY{S0C!)^CK<6Q(N)_r7Y{y}}tC;tXB35M~!wMi!)DhVx<N;uN4EYwGb@p+_ZEpc~?67K$$q>HKI2;TyQSn1EP_j7fc}mt4CYEjP%pRzlf`?V{u?o=#gkQ{fxaeLrZ!`pjRQ@4J`yI!(PGy#B)4?oT<rGrA0<kxPKC#X9C=?=;qI=jB6Q}>}kHY&iOly{+5dUb{NFfBlx-rApe$0R){$Hr(kXwMnYD6B9lR;RNR!;5FdfpeF$OOP*+>2pAMy4mHS@C8#E5@m&T@}`0_W6t{FSxJi1qMcJQ%viCqhykgBFL>D>60H2=e*QXAsb=Qan343_K9hf5UCIa2~=NUK9MIQNM$H$Y@<~I+<D%kqAsxmEGtUJ6D9B-`sEmZguRAxQs~5bmPCul%6rESwh)=nWHO=vT}_73ir~of*YSt&EV*i|b03Br5JR#dLELku8F(6aY4iE`r~sYQ|7DoTB|NG((-I{iari_kOQItswBciiq)*+X9)8Fe1}qN-vZwm{0CU~zw1$L$3w>Lu%8|X-5LwcB2bNJ5o|H;@yr&{^JABX#jCrcRlRyeUv+F>W4INOJZeOP`%PN9;V!~%LFcM0{wYG;A^OQNkV_9Tv_aJF;6|Y;N{j2&44wtY?4flJZ+zll)vt#X@k>S!*bYK-b!^tS9_>g(D6xW)DQYHfs$I)5nqxUXV(IhpqWRD-5`LIn<mTr`9tGX}bCve-Nd7DB1JcKE(zdwOB4VUPl=5!NY`0g`LJ_=i!gc*;r_j^@vBBsyc`ZM6xin?zHwX2$P4C{mCjx5=Uo3zsmdQ9kIi7~P@6uKK3#e!6IaJJc{F!bh<@$xuGb@UYi-Na0Du%T(xgTysBVPzuFjX7UfI~4jF<d89m<xou_VZL>BwnHJuA)m?2Y4hS4Cd8IApuSRJK`g+fgoE2v70n%*LC(kUf{D0y5wLcuaY8I)l-byX#^y6Hv*qw{iSW?mP-WT<L9%Hlhm2>t^?FgeLzqA60&;^S&4Ib&Qcb$nwnJ?TF*J)DV9}~HCf<UW0a0Iwp-|PZ2Q?(%J1QAfyp^nk@K7jk*duF!S7lU6fyj-@W#=fiL!rVEont3-Gh>XnTF8&MAKHA?e-MYaA$KaMwHXud7wDBom*;KT;S8r>hJ7N_niZv`Cw<$sO6RCh_^{`QTMrqKtP**)E7DNNd}K1LI@^`uL0r%~)^i=&NrpW=uL;xj(wL9Xe`8(!Wn2CEADSUFw0aE=Y;CKROFa>!Ioy1mhu(}9?`j%%5xR@)mhbRN1ZQdF_M7j_yN94_<g19(L5W3O80q2K#_KS1FE$OVazJvPBIHGBU6)fR06`ag(A1KWa+AOad%Z9tq4$7SmgZsv45}NR^ZIjs47GL7&F@ClPi7L3c-c<&mj#2Zr%LJ4c$y3*ah1Wi6Q!wVZB?rib<JT(SSm0*)lsD$ViKL{FL@It`Fk~3dZw=E23{1>HYd4&x&)^rvmsYJ4TZoBt%V5=7uC6m+q0-;1VbTi!wnw@KbpSO2C`yIRO?{4cS#{z!?>@sFY8rE%++WptfL&N4OwGP#l0zDKx02hzGX(aAILTV6X^z-I+aeR4ZPb1K1D#DjrK^(grEjesZ?SmG3%J;Ge%CkzX!lc`G;lmSSq=PfGL5zDrOI{=yJH=L#P1>akozAdL&>Fx%y}rDwH2(AVjCPP#()>Awzo(2RTId!*j5Yp{wbq!9;I0+<u+X_51JF$59!$FVom>)9F>MXRZ{BCY^7_DzVJrGzL}pS=xyR>$g6;I^er$k99KVZ1^Oz1<JI-=7z&CRUllqLlWR6O8)DvH_|ZmAD3aS;WN=%A2s$3s?Po7h>=nCqn=@@BVh1IEmBA`dy9qLGD(wdLgVEL4PHnY1@ELT6?S=!``A>}Fq+&>pd1o{91IM0nrqVZ+Za{pPy$s&3l1(76-uD^?L&t#D#{7mN1VdOAuGkE8C*yAB3GrO%OtTjB53}Cj1xE?Lk=0Itpe=xmD4iR67g#S?P3++JAN;ZqpD)fu7VgQV-XF^J1O04b`)=7i$|y6ea!q?PzTOK9N#eIH)bv+JPt$QZO)`J7oL=GNk!nyEK!t}xKHf>D7>pVo^e^yU=Gh(o;MWoPK?17tY~~vI6+5J(_PD2TO-)|^@3Pu)QG1d!dIdf2)biZW9|Jc&>10<Yt!cjPXnyG3fQ<ga(i|PSt<SO+_+FK>7vFY=;EGw;G}FwWFa+WYmq|kN=7dWb<)+edf0=qnAuTd8=j!yBexzAmyaDNHkUxt>iB1$%hY+XY@l^e69&}^0Un5UQ_MyZHE!L)Ea8udGW4i$4cy*?i}4i#S^K0sS{ARtYM}K)eocL1w^ZB|x(fgR0zUul3#?qDU^(_io^^5L(5<1Jz|#sl{*W8R1OjD}l*lJ<bU-jlF!-=YSL`U_C~TZ%BF$YwM+WRO(_;?2^4bu5?iG8es%vI?<A8%h7GIvspxXzFfN}=zNru#vegm6|lFfi{!{uf0KU-S;*5Mic9W^$cr`&x*SP7udmEcZ$*eO`)S+}0>I**m+Sal4qg<6NZWI9&rO}A}9R+v=was|Y_oH*XJT<Wf+pqg7lX?Pt&@=jWsgjM<J3~;zTdjh6cFSI=@q3p6u5n?sR3`}yXDD0tFx|D}oS0#UwVcFb?E<~%Ssfe9U1At{a>m_|tz1^1~a|b~iUcY4sQtYTQ%rZ^1EcB|d@{5;7!{TyM^E<E_#S14N(Mj$<CZ|xs!;G#=Kf4$hzOG&63X#?J7WezSlh^BRJCQImqY$0c{fU!3tCe&Hr&<kXyzuxnLWj<wH+TGE9ZM4!vEN5_h>CeQaPxGE)jFY8FH2#9vV_j#Hhdiv#n!P9grXy4MN_293eUfK<LY&7H2twA@?#;i!OOzH420CM3N}=tEmY|)@?pO$(XX$ccNfJ7GbQVfMF>n3a0UdbL>INOkb7b;i4D6L;f$55#2OsqW!C#v1aX=5l$kD8nDvbPrOg=bH+2|z-XN%OG?}`dE88OQMm*bx$oAb_^zGrQPFFpH3zo#gse_QsOsB~)Q@8|^kE!fN9@mxVqmLp^@bT$0gAR0pJfGf?u2zbM9vo11m(|wSr_ifFK!7w-f*mVWWXF3QqwwxB#T@GIQ1m)LSk~c<iC19z%Qi-@s;N-L({y{7l9vn*J$LqvSu%kd8lkuoibC5uY6>MjX=Xo1zB8TJ0o*Fl_M29Ao@D#nC%jHz3Hv@x(F-WKBCJR=*sS-FwijIz$S)zr|A+xV52uvRMj<&><L*UFqu`CmI3l`u(}XE6U?sY3CBph&Kdlp93Dggv0Z{yuv|TN`S5|nZNRZf_{5{?uZBdj<QW`z|n9H_hXH}M0U}btrVcOUZs^1Zcw}|b@MaIheh3cyA44FB~6~#<^kg^8sG4pHIS~lTj8}p=&nd;AygfDPg%Wr{mJF7L$3CCa80HkAf`VWnT?vx~F6oD!^v1GrM%2?<@)rc4&sEdZtfs&lkVPWhVy(c#BuwZeX%*7w%a!S{sYgPNrbzuulIFw&@@d_C^>N;6GmmV#q?gd6Ez!kuJ`bx8BDoHHoN9Qh@{2(U+)fOGRPJw_8x>1Z(Izu`Lqz9e>VWt{BPl{Dhd*xl7m{}!yfsb7RuVxhBbU(k_wHlxb1*>=v%?P+bF@dG3_;E!jQ5C&1IV<NH05?fSoF3n#PL;n@krI)ww+x}tOzqIT&83xd(C8Qfm%MmCcSz4WabNJ%W&00xtLRl=-5s_;tlZNDauRw~(eo5JGZcQx8~c5Uhe~5-HXCJf@rA(aV)M6WA!>yHO{2y|fmps7=+yA^9jOx;`$-o6q40}sj21vR<y#?$AveP|=;*yF!g5h@#`%^YZqquy8dv&Fme@0TxX8Twhd0%qmMi+S-XB_*aU4{FJaw4FzPBa7&7PIULE74F=u=Z!(Mi*oaRIJ>24XJM1&9X}-@IQf$8R6uqls%^jS<SYU(oKE)rEUpZt7*R^({?jh^#lMURaTm8bx^>L{%K;L`ot61vEvYC{eA2v_;8R2*U@8{otJfUYi`&mIl8a?4_%bq=uUEtJC;)Q*H+eoZmp4i8RRs<-Y4fC7tT^3SZ~l>zEsKjo&}HNAipKi^DI{cBhmhdz{n$L@kSXu$E=q<{K8ALI2^qUtfQ5{0;lX{fFV7O83(AXNorV?R#%?ofJ-EM*AU9g@-p!*;bes^z5a%fUnYSQ(O}5wN)(-T^LbGH?7)FQ*%+XVk`y3*8OgG_b+&jX}P2?;RE$%VfP6YN+a(d8WrtCl3Gj>A7Y&EpG$A~0ax7n^S3wbI&<pSP9YDjh5}5>ZDk=EO00nw&0RtQJt@aK_VepcpFY2uA3ijZnh!+{*B@VhCihq1u9`b=UH;4)PTe?J3pYXR%I|>lehaHzF5<c6hL+&%L0>7Qtck_nNZK?9vz~m0|4r`AAcLj$DRCpy(jzQahNb=(PT|F*a6A67*FD$5?7rmIv$PJ0{o$~Fz<l*T`|?kLpF&*ueUkdkx{sr=zrc<V@l^06|50w9)N0T5s#$i)$j_wo+#e*z7vrA4sGjg!(DCKZw_pEq(+83B^CY$27Pje!q}+QOJ(vRKtg47N{aja9o}ob*tf?6;apB1>gEx8t<YB5-m(c537zNV{cQpOSPd|Tm7t8<j^AA6LdNbYETZp)CyD&7W=xfedVgbk9ioOmsAtxTpB=qI~^7{`ze)qR8Xa4i=CO~=&&RiSz*ESm|j=D9rUcK2Kca;6pxJwS#%yxwYnjzFE+`O`{n-it|?%%SDRD4Ii7YgNmJ3uA^N3yZIcP&6m%?<u_R12(*J^WE>YGSy}j*h#<hbNng?lgrox?NoWGK-1d$Pi67$2Zckmo*n6-G3s?%!NPKk&N+iLFPr|{Gld<?fL}%u57L2q^rzS6g9|+#BDgVC-5^pp!M?>m9{SC+PRa1d)M5b<KO;zz5eo8jOmi|%JlSqmM$Q;OH-pVm4yZ~xi+dzkv%4DP=JGGlliW?1^DEyu0u)G$k)QswY^cBsjmZ$_slQkXr%eI=#Rugm7Xj2La()HIO(k355fDHjK$%Uqz$_9rV&<N5;ibeN8p|scp+|QtBt%1@2#*Yy~Fo<uQ|OhcxW>khq<hI<%yPN(tGlHC&S(!Xv`{q{OGf-gVcM|^PZ`0#YEwyc--)&R6Q0|R_*bkJstFd0>Q)G7IAJW7Lo0wvv#gj9azn_W;JW6Y~b@dxj@%;3A%43>&zxcqnVBDYn)i7w8~FGq5&8>ytB+v1ki72WB%y@+db+F7bO9}=fWO6neM60JgGq_kjT5n3c-v*vW{S`2rxk;#Dh8?T}DsTywtA><A_nT+ux)@o>$U6v|J}yj52Ee+7u$Yb<H&xMci8+1Hbm$3bh$L->!6x<Y2Q1ngu1U-#M1SI+_Yt!wbLJgL(9_!dO5PBfV|h*U0Q?w+(B6j{99!frp>w#{=cm06cTLAA!NYaHNd_6I*n(<dV*ea!;KYLB+E}=YPs0m#hYgjmN8b_RVHi2Z!Dct1f(Wq~FgPER)BT%}pp;D>azVJ9cL3n3)m#&trSJsCfa$nW8iy`j03gG;7{oq6bP<oP$-i)*q+cZ*|*kFS7bO<x&}JEA(l_6wKWKIuS*7L--msM?oGmv)28I9-F+(F-;p^M>IsR4lgf8_?fj;;BHkIYNR5dhkT$Q1X6|Xqjh9m+KaBs&P8ebuAOCOiIqI?^_%lBfZkJtMogkDF7gTINC;uU1C@CUv9}@p9^sw%QWnBQUc-X!!zQ9`h>6Cs&c>j^$YD#@rT{#@Z6X~UE_bP87vOgQFJ~Q8cLo};IE5RC2jn0xF>*}kw@s8PXP>XHpkJ1CG#7pE2YHzZ?x7S{Ie<djjET+&&nq}>n=p|A<M;BLJ*K%UQg@krR-D#W*ja6?rD|PX6h*S|O^c>Airw~R780sp+$_Nif`6JLiL>Hu8@)=QfQH-=fir-@%x<xgZBv)A_I!B~l%xkvUfH&ly#P}D2f7Vhe@nDA@>jJBhDVhnQCp+ZbN6c8fob-#X|g6lHF^ks<DoXx7CkMdM=>tec55BrsJBAlqKQ--)RUv0Sz3LLF-M0l(6)kh_>JhrQ{YtVM(8Ft+Co8;w1wyKVO3PbWve8Fx13JcLpgdCSSvOXO%-`3YutshD0n}^>LYOCsG*ZF1(#_TYPB$hUD`Fqu9%m;Z972@gRMmPuG2-!(aGCF?vorOH@plE76O>SY9?7u&TM+w0OWI&G+N&*!aj_QxT;Ylyhsa-X4D1yEou<0q7Y(pVS;s#lRik-JVDBs*3~QHEMn&O!RqLoP<6QfgyGDR9{<of)bP1^q%HK!dn$PEFMqFEIxmdxo3x(0lt{U0?cVX2+C1?+H>eZv0#?e~M&6yF?5khJRfNFOdb!=)nW3Sc$fO4*7-vemC+ML;y;h;!2$RrThdU;8cxbAVNDTx^VP#+eMmeeZx~QQMbEiSG9r`YUanAX1f}{lXwXC}UHXz|`_lx}C1(H!*csjt9)}r<iYy@WGY(M`#i=v>|{#E#ZgU_aY-q0_g@44M#JGm%%{c~-<O|TKVV3~pNmTKrX2xu1N=!NMJ_EZxg8AB@r_6XGFn@yYp)^SUi@_1s#d6HpR32?R-u2~GTt|u1*hlE34(+SlT*ggE1trAAZCamNt);bE^x9DgX5&+%%P``bB{RLB_@Yy#t6p!^l#d|@~7G&i+xAK^0m!d?eTb7H&D6NSyBI-I&0VO5H<Y3I)$CFQ25(gS)!khhi`GWTXl$HRkg#wt0YKo!>W{9@VRAp|ZdGB{saK4E}9aV$Jkm@e@vl?Z3CCE1b<3nAA9&@A!>2a~-2}JZuKwcs20d~&u!rM%nM;Z%77{c<1G_nFpk1=()9lLzpN8K06T4S|5W8Ms+Pw+dCw}`UBc^Psz#(^;Q+sHf9)$m~ypny8hfX||;zjyJXbxLC*=Mh!4dS!kZn1v{{)|>V6U84*baI^*Jl<ys1ZGH*an9V61XPNF`UnCp3(8j!{27EsZi(IgS*f<eAI7sspzgMHy%WB(qbwt53gsLKmOm(7ug2>jA8sd~iPR*I3_){m!M`u$eI<@i)<TD;wFz+66LZqObI^EI$rky)Dq0xrTs$%z1I9z%PAi-w1u{KZ6I%(1g>!=64QA6~kIv}1G(<@cuDoinrGINwS+yJAqjfvH+WAf;yst&b6<P;5={3_jxb=<SAjBYNiM9{>F_j&JL8K4l(_o53XfIE$GI_0pP$vQ9tE0kKe=NuA!saPU?e~^VL^vqeWVzI-dC>$7Bbhv#9C>4d6Te-k5TQ3zo9x9hco=T^8lM0!Ec*w+fY@!d?j!xHtR%D^Y+?!UZf6~rFh0TL;vllHo^TkGi#Z5GeWQ(iSjHxK0J6gRvq}C>~>c<nUA=`QWvl&eDlGFzuB34SEDdPN~)?VNM!)?jw<x)j5&j?dS&1ByO(p~ysEkgn}XgsQ(6Gy`#b=`ND2vrP28`w}47H*Q~JN4Xlmr;()04325gNWWLMlj`z#lR=ok%BCV7xr~Um3K`ofc;oD+!|fw?y}U0Ww2{m{uNpwP(W|*!)<sc(;><$94@cvx%YV2bT#+*Np5F8ZLkhDx+v`}O<O)8mp!2}+%*CV!p7Vn_@#=RE_V(LXsoQ55oIM%`JX281IAjV39F-ebmv1M#IBju;z(5yhzRt=h+Nk!YJnuJ?t{H31qDp?QEdgMN))c<@i=A+h=rH(Y?_Kn6&(*`!E83&bMKn84ZV$q&J38HB3d)*<TksulT&R$O&3TVYIUD+vdpdUdhwUJudYldjyOwrCQ9^RNJOlC$m35kP!@>W_++%2{aWV}X+EL%S2~>NJ#sy7a2TebI|0~#-mr$9fUrEUD=M19o&|E-ChPpjEo6mNj9x_2zNNP48U(EFsutzTn)zLsUYb|BsuV8cBT`f?6H8=rnCx}7fTOT-?KA9=9tx%qWKWLJO?L}UyH3_rN(fl^y4gA^B)JWpE(yi%Zb>+bE$=#-p+Zk93C+5w02t1QBl&%V-v2#e*scqMDA+yMCHW0mwcQ~jnY6HOg%0Tv=zn!x)Q|&cDbtsf66=DZz=(Y19keO{9U&IbU&b)%ab3FNA5BNk$n|oj)?Z|pCKbfdwrp3}I(L+iIy#v~1?R<XKy(jWqM5yn`ceRKT`cWw^b6)d6H^GkST2b#LAm{{b>v-yGLvQ74GYA0i5kv?=Ja6}-8PF}2J9iarfy8!qX*c=AlU}GID}4C0fglVpkoiT53?{8szVGTpi(<dVMEs^z)Fgxf=euO^=bO(&PvOOCIEdhVk>@XjFCszK`trFjT%s<HP5K0e>nfcrP6SrM@BJrU`L@N;<CQFxG0;n$6?J75>d8`cUp@W+B^_X13taiYc7^93ZEm>P2@CS^yjmUglzNBR~oOchWrxfmAj!g7+pjsz?UcK^Q0Gh0-RDlSflFqk{Uf~&7?)Oc?K1*VwmK7KkL{;i)wwi5^Q{^V--D+6{^(KA#gZj-LS}<G4PSlYO9sC?dZya+$`nb`u+E-Nc0o2im_26UL!yj5UZ|X+i?>7d7#9Us?9t?K<k8C-Dw2WH=`!!hw4M_o3#sebb!Y0RI^O5f3^zxa8L|B!BxZ7QT7$11S&d~eZ{0@t&ayrHiXZ`!-EJ$7tyjp$HL7;fN_r*v9R4cu%AuB=V5szX`Lt8-v$0c&^Jz&-x9O<t4qmcB)X!~7H)yJ-ck{kHF6^4O9Z@};V*h&(@kNk<g6Y_V|X!-wWsM)k#{V1<Ek196!lR^I_p@QM1_ymHp-fQ2x_UQ`5`B;8OzkhINN@0zx&~P|1MSxT;y)ENMP#ZA`Ns1_tPPj4fR$}D3DT?uqbK`%&JBZQfQAZ;YrgF)1ctV1RnyNf%_NV{rdU~mCA2=eUV>ERiR;9_fapaLZ?|c20<qb_o4~qlBvHAS^-u%GCq6;20bT@qsEeXT1aU|unu<7TXtQ2kxfx8(YGV@k)QPzXj+-3J#-dTC)sX!+zn(Z?rVQ%XC9d2hWwSN&yH5^LLA9rxOBp;eyOPSLpAbD5zQs1D%Z_j4ML+ZnK0%USO3{FJ#+S`kIl4C!)6MQrYJ9E$WbVfENWYG+#=Z`uDMjhHh04rWzpJ43O^`VB+MJGSo!{kd=XbEVxKeF%P`%H17SuK6#R$zRFAh<w>!FV0j46X>yoG-6+Ns(XSKSOUM_0O=0tEB<y>u;4ctN3Pg|PAIy1YqSCh40*X6rL!S<4PNUg_3u)~zcaPwI9V8EST-okw?oiV^O@?rMvY`w<P%fj&qTJaHLz^LuceT4z1l*n5rG2|OZLmoM;W8gAik{4PKW0||QjG^1zyUqtmta?v_#gg^1w9?u`4?LQCB>X4|<<Ra787@ld&YOcGhj0i%7Yx6A-9JiP5#V?;Y{|N12`V9OWJFq(94*|5NgMs;k}8W}RGk8wn%%2{;G_gnpd`>2f}Hl3Mn(-7a?3=}DqD8eM&j?&?rj(Dahr1cv?CN8X9Pt>jq_x@{&D~=w;OK#E`Ox=SLL$Y*QE<iBrk2Sn&5l&wl=`OXw9GEp&UL<T7_cCyft1Ir%&Al1WnuWB@r3U%KTGRD;0E0&;P|=;&o~Cq9IaWjsz7W@o^$_q7`F3YX!zgBVJ}0;p;)BDuE`0Qcc~Xf$+1JW>S|1>iX|spCzqXpR@)}Pl~4NsmCw<;w<aBKyyO*{sR!m{!&#K#Xv`jxxK&4d4ZaQ!2ce&-5$55QMsZLo}pIiY2BdKA+~De6Zmw<;9@`LR!D$>b=4Xptbct_E*=3eWZ30#n>Hhe<$4g&iS!Ak6b>P>2a7$`30zQUfrDPrQp1p5Eblwslh`Tiw(Xe{up=Yof!ei@<e{qVy6vUnLcCrQ>tV;EnmZX{>wVkQ*<Iwudf<W1r3_hDecS2UI}+!L_rHUOh+2aSMfGinkFruWC=wCEp^=INSl}fD3%?$2G-^eJFeqdYMY7P1v%wsNHi%y6U>#~A3L;~iM9}v>k1v1Y*H`O;e}4Vx)8|*oA1(SM9l!hL9hE=%?g1~80rZ!p5By^6{7y4<ehWF2q!KW#Ex8lKqK&=(AnR4XWi<q(pgSo)xeG%+!rkxA2~Y+!f*?ob2Lv+g)t==W^o8UK!2g)g89DxH*Hj(6ZSF=j1lSyL^&S^KEa(t=&d_!}_O&QvTTaUfk*?NR^~s38+IK>aPb%Ro^c<v1E(u10anCiiPXTv>=n&ZFkV4q&AeX#C7oxuCwed%9D9FkB-3$6cVuk2-;l(AEdm}1+L~#y`vH7TDS7FbQjn$MW@FJbQ*IReN(+2koKWJVk!?IU7I%VH?>RF-hkE{ovD?11vMxoUr2`)l@LBv_1UF3pZ1!V1q=jt<3jb~OL1|v<Pe4>D0{g}|$&FDpO`RI^30PY50Sd)4x;9buO59y_w&An5;RBOYl&Ce?|W5~hb%o{3&6y4IfmJjQ|m*+k{jK;}Y8Sz=V7uIl*6)@}zUYXQ$9}%}|OufGf#ThBW37<qwmDd++%@&6Ag%Ayid3<iG{L~5T1yD7?(Qt@F6{<DiK>-pO?g+uDw^1rZO|%!qQ0<B|@;cN0baMoy`#ZJ0R2z|k8da*|Sa6EVisW0INV2K#cvVUTbIU&r<3BVsRjT781WQzWilwbZJrB8-R1h~Y@-M|guj?|O(lvqd9V~%ugiu%sx*oi(lUZseW5Fz~g$uYo-S~ODR4A9ksWu^!4pX}Rn43yXlLQN!H4n%ZwjawR*EzI#c70;heyso_3MZrWv8&O2NC{&Em8}&zYWKnSImHK(@8V4BWR<F;YY9$)-lG$-GxR!gdIAJoM3M4wgi0+Y3)^M~_I=Gt$ZXekLexhlSBQ$1#?)Pujd^t&$>fZb&yB)^NH?ikF(iA0b+H1ybS#E(Wc<K6xKpMf_G38rlr24(De2UtLda%KQ&X#G0bGcvs1q>46%t&ix!zBSLdqaz#POGi$Squ<Q>P1`=%x<QLMN3Y35hd%+E%^K*$(#~^a>NgyNqFsZS4AsOPUj@x+xlqmfeqqkPoQ%^IM=Z?wBI!rWo~<)IcG_waZ+I=NEMtvOiy_{H&KX<n(}fwz;m8_3e2S#?R*cOp98@P_T(!g4vGvM-{zVYen<r8SqZ?QSi<jq0)gS>zKiJ{J&6LdSE1ej&%kn)oc5?l`AnlCych-%{AW*mt`GvcS>~1I%Zx{gm#*YTL<@ZuMgB0gKz|=WIZPDaRK8Ug2Up&8VQhua8LreGig3!b(CQlZXx?)(>q+}9?;z2B5;i58I3;rLhdI@>2PT{EUhNB{Rl}$z|7`E0OqVP0EM};naY>C2V_ZgVq?I9f0RVc^YU^EkHvNd3T+@wC@Ml1cwH6k#=`f=Zo(45&*YY}0RlW2Awx@spnY&_i4*|>ooY)%h{}y*jLg%HRPUxGQ`DcPA_X-a<ar63mo=jSUGCeJtHt-=QAGW@y24ecAMiE*iU42oKCPkdMvKKwqYKc-l);f7Wi@Wr!uA%)H{B|_6FQGvDEFhtNwLL>7-Ikm@Se3o-v^Km{KiQ%l>!U4T-b;MGpv6bhK+dV@O}v&b1@s^n3dF53p7}gUcuoKb|#~(G;4V66<~*VqK8ld2v|IqEV}s(w8ie@&O3K_4tiCMZeBy|p-}!o<!0!h^wHa>=W|q&kMvL$gIwnr^}~)vwf}d9W(i-&&!LsxI8e!kLVYKVY#qwLEYW6sF48p=dN9nNl<Jq#(2WO!429Z=%synT5d-i(qf3b&@Zqvl3s5-E)|n;<?oSEq`=OCZt*rkFbjCA~zN>4%<}lDld}u0}tr@HFyfe4lMkj(3F{J%Pd*8@fcB|OFk@rv49rmHgp;N3xLfRB3d4+GWO$-e@KeaOZ?Y2R4rfpW#tp#li5ZoZWc$I?&!or~t=CC&gX%LmtFJ=V)y80KZBfy1OhqkR$+~o8Vxnk`8t-D=bD|>DYZB((%DP$mI+{P4U8E#=Ak35O78rim18QzEF@Ni7ib$41>ea@|VK|c_=%~D4S18$k3uyNak`JDG_gP9LV?+)!E)2Go(Aky`#v$x)jw6eP@GPXk@D#H@myPyxz@@c&*O`Hlof7i%25n=Y)t?)W(&{VBo+c|W(%bz+(sfhf9n7-UrZ|J(5utd;<9<U;-8}zON>~#z-(M~R0a>mm1hMGx^qvQ-pSh8x8y#Ca-`J?K?G4(*Dj5K;}OS=J!Tc6FY(R91UQWvViJY4x%7lk-$)I@qmi#+!i$FfaeN!U6CiezSi-|Im28$-DiR)23nr;}aK1pP`sj7+MkaE<f?n~`KJScQ;tWA<&LT_it=R1k#d4+uis_ciYlHV?|O_u)9kBKYHP?t8Tudc&(j{S#Uy&q@hz*R=Y8$2uO8GAFnVUqwY;6h7J4J6!mQ;|hi536pntFnQN-8yHAPREdcc(e=}9BaZ}6P|>>|N2@X)gx4Onxf((dlN;&gC`<o<^HQdU<>x9VUUDNf|6DhUL2ThU4h#RA7T|5~GaN$wQ<(YeQpyG#H;wb2Db}@zn%rmHoKtT&k-Sx=<?h(MDr*?pCni0IC!jreovZXj!KE5vJ$`rAS)D<Q=?oE1oQci^Xci62rQZ;mzOB=U>a$S6p1%`vyUFx`w<~xUPs`r>(HG0+y5&;#T^ptfyw9W*c-~V7_j6C&FspfIrvr^jdLbM{96!IUi(n@-**7e8xn~|(MnY+3Z-MiY)P>(BG+v(2bAzyW(KV)&7Q|X=!`M`m+L$a?P-3t5Xk#~#$2&T_%X(wUVQgj5PNZ6u?@Ga2L#W+dkHDGt(vO|0O&Ilr*aJH_KBwS5!?Nk_^v}>JWMLC{5jkB~uMr*!k&`fipg|k~C>T9L2{_GVWscF)&%omQbrC~<Eck+%x{SC8zZQ;;!~2-|t)LE^M_RrW%J0xzR;C|@!WFP3+I2u004K!3I13FF5b@P$UAf7hTqTy6wb;(Ybdjqpsz?{2p0L_{Q;22@r4;`RM7U4%xCA{}381*2g>r-KCfBA<37$p(HZotqC63yYQfR2?Cncx^AWbNko)Z<XeqZUqQ{Wj26&22RuM+GGl6_(Y275jh0oU3Y+i;?#W?Gz7T)s$9!kbGVM$WW3E+55YD%DsVDG7)OQxr#17;Rno3gM4MNZFXj#k_D}Dm&3XXb6sIh0tIV-GnZ<#ITwvbOtC*$x7#W8Vfv3Rbj9#+du0Xq@gpzg!7(RondrcpdnE3Gub1a=H3W;N&CgGlL<@20#5^K)<V;%=}$DwU83S1Y<zO1Sxg~w!u`N#?iJIiD!5}3z<{TO9Nyei2HkL2gp}JLucE!CA~B9mF79J6kMg}01iO02mt&XLCBYn6w=O6knJ2|KZJ;PMkS6{+vkouiKF_-K$(Rng!zfpU*Yd0bUZR9_)CdjF!WI;T8FuORWrng`>TWT3lWJrEgj~4*g*%UXi_vW&O~Q)G6w3O?oFnepkBwSY(0cDKvpKbDb$j>*YOQF9O!01s+y{Q?Qr=W$ed|qzdYSYM7=5o>ko)AuK*LT7*s!!@o2QU%A;uEiPtf4kZ<$guU=25glNDp_>fA;_2Ej`JLLUoFNmHCEUPjg1S|+(?fSkq&&%dZfSX0Z|Gyvdw@iXB^IOV=7vn)h{djANm{!+E`LQ^`cN<D9(@DgdRGA@?J*b3-`iS4rr;ggSgjTau}D@8>ws9gONt!tCQScll?j9COkvHmg~{nFZin$9_?Df@U=yUoAVtD&eAha@Q$aO9FbcE&;jh7O*EEu?|OGq_*(;r6=bmG0RPS)#Z-s#DtNKw#r#$n^D~W>N`-@s>Pt(G>Ni$3oY}y!!BRmg9Y1I^*&#!EQ|QGibBBOq`e&OVJejI<Q&qvk=6$tSf}xh(v@)84+)@k^5l|1A8Juv-2Or9x94J0%B2YpP@#@V{_4Wjd{449uzF7hM{zne`E7&a>OF8Lge?cg292;6oSpCamaaNG|>nO03*#G!>Sfo0T}DWct^d6)_8OMHuJ7l3x}Odpv1@pbHc`{Z1Z#h_du<eaxj5c=NdBC%36mlcm_BB?1-JiE%+3mXzSp{#Cx>;WsA5}l>?npSlG~jOLXF=<kiNpg54p&{3}k(rN0wNk+E5Z{Xyvj4mf3*QMqZ_4K8peXyT2{5_Z3tqW9LGfGX~^PM5Q%sSW)E`dWaa9;BLGNn-g@ZJW~$X~bg-9+Qkyq~kHJ%nw+L&eItm+puWf&+CO(1&2&on_lS^DiEi(t0j*I3Rhw`@oc}nb<|IkeI1{|4IA4*O($^-LGL%6>Mb`j(D*DeW?CMtOEOjne*r&>_M_l!H!4uXZX5li3&dOnGOO4qr1Vzx@y<bs5q+_1=|5EcwuDU7qR+9Aj3Yt;K|YWPWzYeO{aUscp-_C2g#vgE2^qf697*<Q84LM0;2nyxTmb3HJQ+DI!q~N{o#(n=g{B^AE4$cCIJdhQMU`~4n~IiY0HYLu7+^kqr79njG@~#Xo4c$i|A-LRX$*Rkd9lj@FT5d0h;AoimG+koW9jj3z{ZktKl^G2cJgxqbRzeF8YV5$)O=U3%kuVacM0rYbCX2)Ek%Qlu;NgSj*fsa(xbY2pG_6FS{_3^y68#EogXfs;for}7ei8%PGO?ORi#Q4AKZ0LoL8vRF|q-JoFJd_h-o#gcRx@fQrHi^322C8C}~G89_xeAjYN%+^a99*Fjo@7cF{8`>(X;5^-TVY%yXzbVC<CWoy?pX*XwVeQw+1+o22wf+D(595oIF)NW~%*O;<*Kwti_JCiyjt>T#lI^KD-pHRTQLmN<Gz3rs_VKAdj}oTJwHRe{AfdZ^QE7GNq-q*h0r5QH#Bem%Ggd8om7t0l!EZsK8io%1&GQLj*xXa&$kcU>-Ow(ldHn#wY9nhTGs`u+17BTE<bI3K@xzyB}y!#HuNy)n~aq5Gh+<Z%jFeYb1AUBak#Rmh3nzl2v|i}s|o{lZ&!L6)vYu^u*`Se?YT8)-8aV1|K|S=h3$vD0J5X|Bq3-o1|KL09<wlgqY-L^a^>i(V&6($N=A^-%x3%;jvCt^dhXP|A4!R#g~9*PT@IE-TSyYA*R+ns#iAVRLWEc>jXSVS&SR82KQS8LTYpb&7?M%lj~*+N4OHjB!~Y;zrbPw=*<2m&sxNw#{?{`Q^S3GKIXd8uBhc+cUNQ446oq(QPS@=kxRHPoF-&njhZ3g3El!t6zV7{TW|s%8R}7Q5JV2?l1Y&WV)D0QuY<noC&n3VlRqs3!71{@iTUVT;}`jND<@h-R8Q8<(pP6PP7+F>rQ9E@$UR%Z$n7*vz>mKJcYOF5Apo%&-v0;|FbXo1W9fCze^>XBD+O@(71SJU+e}IUohuY*^@uvl1lB$oYv0rR;sQmHp7)$u#O$~VT?QS<?nZ2|8&y_5203OcRFfq`nj%<nov7p`KM-RR87%bW(Qn~j}y6t%-_D=GKDl4_*$LIW(bQG4j+qMY1BLD7}M4a_b7wW3}HC_m*0Q*@w>l$`Q*>PI~_aV!Lz@%U2_FTN90g7L$BTfkE3os5%<B7bf?WZb1U7OAyoU@-r{xpwFb9#O^fe<GZi&cWjbmkL$Z4WFo?2#`~r&)55G-qEjsd);})=&SQTY)ObU%~yNm#25;H0hzr?_lzS)flA&*EVpJ)_wp2#|sF+Ksvkcj#{lm{?Bj{dH-%W<k%DVbL774I}7?+V<e1O-k#@nh8a*F}{lAtfbN1ifR*hRgiv=O2Fh^y7Lx-mQCT)vOU~_u^`@ktVcuAE$^J;5<EqdK~=*OX&gHYcut72jQGMmAHw~oa{yC`BD_XYo<Zwfb#)CKc;*Z^<~$o>3d$t!5eruFr}NAcL3K>Ejq#m1@^Bcl5K|OsN6NBI;y5F1vk&49MNr`eebvRnnV6IwW;?z4ZK{GAE4$-H&dJS+@ji|ydYLQWho<Hm^4x?oCAfe0t|4HHHkRm1u>Z-%1bjZ`RTK7@r%jdhC=U<sNHKWnDKrz$u7G<8T~@_tGMA&v$Pqg#jb1rL5zWB5vu-5pR0?6OS#&Um&{D-ikNHRFtJ`18R62<Ofw~+f!!2xfk$w5#EmY@4{;fz>JhqBRfFVoWDh#yQUCVW>-Cq%6S72QfL1r8GLNQK*16XjnD{z}$m5Dod9Yh*vo1=VUWcbQvuA2!L90Li@yM)XsJ{>OHIPS*y<GIDQ{MCKnsIa6%SAP3>XOB>%k=eOy<GSXw3k};9^uMRFdjobo-wzVHcypdI;#xRDeOcjyzrN`lRGo9@;p{AjDi>^Bx)}q-vKNTu+#8PW`$JuzjuEU2x985><~?b-mY2+9ynUQg@!EnaIx$q7s%mJHJQv}hNvXCEG^FwVoL%{y6^4yW)swgXSo3&eL<^k*upCTqg!ItFcY+QIIy9OzHZl0S4+)swIL5tEP|vO-G05IUB#x+#c@ayooaU>uIt14Vt#77EncYm5_Qj_twz94IY)>Aw(C$kH7Dm`@Tsm~P&A7DG8l1!pl9zRLrFIMv8<`M6zA|X4VytkxRYgsfD!v&xEj@9`NrpEecI>34Q(^!OPbWeBqr2qAq@LamQkz5zG&MEjO)X`;)1B0&EJR}y-rXyw&$Uh^Ix8i=ld%6vp`<f+F|QOw1>Nu=4o`MPfp#YZ4(7v7LbZ^cz(QoYN21e<Fd|a(MwOPuHeIT7*G-RFKsiDHp~|X-c2dE06x4^)fN#7U>C*RV6Cl78dyDo`E8dVdQjjo;eC6qb~mbt1)9FGBtnvSQ5?c945lI^?V+BEnC<1|DTvvv1Di!fV-V<vqF{SptN0_OuMW0yIhTsbwDho_-Zv^Eg?yojilI9f%j(_l)bC$kf4hd2&)cIHiesb|=M)9KL1)}LfvES!Y)*CG{XOOd?t)0jwe5$DT6VgDPD)a>7(W>7nBiAPDm&iK;@irDiNGjjh=+^NpntWaU}d^?Yy<Z3*8+qQ57YisFbDJt^pC*AtVH2j|6J>p%MIb#92&vLF+=xTK)po2zz(c)N`w_?wg-I3C&HcU@%`=&xlK1U__NvIZGG6pMo?eB&UBPB<3TaI5A?$9mYEPI!c+4bFEXlSy?fv=@M&3(+nn-s*TYU`zMDNZDtE{724O+IzY_r~wfI6L{j?!%9oWkm=nEqxSfsKY13pM_NjU7#t_B1f2boF7x;)6C-cDX4-2&~)j(z94ry)Y-b49jmchtd3D##%9SQfxVDSyUjNb9ubfDTRbRRmglJT7tj%46Zt$(d~%Hbta|d-w{@tre-;KW-?$;q!5csgG6krETvf{e8^JB8Oyy@|ag_S^-Q<Q>rG4bl!4z#%?BhbDjKEc!`mzg}qEgm8pni2HI&*K$RlY^Ch(**4Yi|$|1}Kd;{P2$#pt!=eCX?7gmF5Lg`#W!1rAWc00orb8Xnkfr45|-oMEcscWxIJCZ5HKMgKjwo%R}OV69>gBa0mL0uQyaWM{M(0J2JVJu;rMEk%9hfBN@;byvK*Od)geJ*6^t>oKsCmB)B42HUk3vdUbyNqUkGS^mj8Rb5vHu`1HfZdJQV!MJ-#+ZgSa%FKkK=M3jw!7$FfzD-N!>y@U?wa=O1vozU-s_sE<Ag8#ijgAl213A6^yhg^@;Zk}zA{-CN082pY{r2dx<XCHO5uU)*n-pu$&Shlvgp7%-i5~FT}rf0*M6lvZ*sL~T|vm9)s!guwr~19q_x*qY`h%x>)HfSfyB|Yl>&qNtjV@*qNNBx;^bf|&t+N%I8+4aylclb*BVkaMZH7OjWtN*4kRxC!Ou@OR8*;|U)3})UWYZxw@;K#KmQ<h5m%A+RzeI#q9Y4`UT?WRu@{m_r>|3;lf54a0Rl`CT(Y5*+{$0+!oDmIyb*TdB25TvIzhS3*I{)v5(f|BqvLrNR?sJS)G77Qecz$3ATzLzJ+M@kwSNOD3aO-0SCAK2BQ(Nfitcp*zO}biKb>v$M|EH#&?}J$@|U+r<7?eo_ItT+tQRh>sE}iqdg#wED&6riC<Ohe^0W?<+(s^<1i~s@{7arQH<Z0VACvOrMO-M8RM|2HKye6#3u#!MCDKq=?^VO0T|1R`B{9L?=vk1{=!`$n#~GV+MZWcwIW2}|A#GEsOuOOU>!jC>6@*B)_Vqo2L%o`d8a_^LDi%qt)9c1MViI&H*-$x1BY;2l@+mkM*0BK4%hhG-F{e`)%Md(tAd6|BQwH~=(98uX3q`=Z_-t+8K}Z~hHAz7)$kmPD(xlxu%P~}fOUhEu9(hZ3h{`@c2L+Z+@5kr)96{eUFmo~U+D%<v`h(S+J38WHl*`!7SBUSXzOs!T0PM8le?q+$0>6SC5-`8@!o8axR=IW6_FkDH%tEhe`|gMDf%!^2EAI}TFBKh@0ZMlq5<v2qc_tyeBA*WS8yd}{aotBiQ>DrsWz8kK_=Ttx|E7oa+usU3ptM7H-?Jrkr@%LnHdsy+w-IqMdq5QK0jQ{8)nsmC!WZzkY2^^z(qsxs^fs<?8FbVt%8P~<U73feA_ndWWLrclQlCL86v;FQ2R!q2dj?i4Zjan=L!VOz6|0h6!&dW=xa?MYyd#75iK_I?0b3#&7y_HHu2LQ*#eV15(|TmPv3g?trBT(kG%6e8$I-u#>8)q>tZX~G&aG2mFk}cLEj*8FWRSNhWsl7u+#8_3^fC*Gr`%~AqhHuL7ppIrSJv=kHA47<n<L9Eim)x`vW-=)KPQLXhF>W_^>_=of}rO4>n~g!GLOxj_GJ4@)EEF(9WzYGreF<bsPwYUb+CPN_eX<A_U^o!2zUkV8j;+Mi(TFq4*XS5II3@26&q#(3(j5WV^F1M0R|=@q6w$dCM~H$9i{377WA|k!6?fa^7=%Ub7%D^F(spKrn=6hG^1)Q8T!mZNX1dgWAixth_1j+-wLr8wG|3FfgsX7K6Vq@rfw4=BC-ckib-ZgiKj0VnHVSYCMgYbUKF$_A`8zPlQz^4XHq=Cnetw48>CBhAnPa>h*+1l4_y<1&5WI0YsC@`?J%e{ZtA;GhBzbja`;wAxUpT_eBHl&kL$jm_N7(!KG?77BBTQd7Z~9`C{iJ22bG`mRe)iO&Pq72FZ8P<Wf9hd-MWu)4}>npK-a;J^2SllsJ)qJ?G__juLD~W*dzxrT$j(w0m`I%hR^hU2wMhNUzl{IY9*(c?R}y16w)+Bc`D}ZvdS@e*im9qQ^WI(^%<SlZ(*)`^V<7f&SFvgk@dn<M3z!K%047{($0tB@;byi7NB}4MUqyD4=6J!h8}>f<V3lOq~rU3sY!O4bBfP1Q;N3WxLspM(5k>3qm~6?C#xu}<G;FMP1vrpqX!H72V+PS;CTK!imhPc&sEb4+q=N2wZYU{nb<96-Vqq-rWI}UjWYOxx@JFgG6_5<ROe&zOfQNiQ@qyo+f;IVmpyK<w><?XMk;(-&6U{uaRWKmnbm3{1|4ss@79zXG0D_^;4b)|5zY-$t~l4}iyP8BIkqAYxN#X$Pk7Ah1m^^!#kv;)JD0WTbr+?lAyL8gw)d+YC?L8<_-QO(3`W-0m8LL0AfsAn@mkJf9Y?vPuy;#VUHgQk!~DH5=eBy#tEAEsZa_fevC4$&92O-_9y0Qn6=f7k$bEAlW%g5qb^)RJ(v8B;4Dx50h5*a{>_2keM&8GdCgbgj4R%p9<Kf9Otzgj}!seqM!a36<2t5iTPYpAL3R)!6s^4Vq=L}QIwKXxwx0xN-+PkJ0G>Tk*hXx7)AQvj_E9s)!WiWSY=MwMP2)$&gd*Wv9!BLB#q$q(0ak?<eWC@k-0LQwv1}0c3d8R=%xgMvasyq65$)jLdmjXV{4CAxQ9<_^BDpsiw4;UB3D^8Ra_XXLOveJYu9N6x;?z@VkY_D<Aqgf-;Vch|jN~nM;vTA<6j0v?mDH#)SYm@S9V8~H{G*|VHhzLnBMsS7&I_5f)P-^TBCsP`w*lE!xIBV2ca#X{DYXDbzlo6(+<WjA94|dO29fS_XHo!|}8Cf*r*B%k)cy=(tnQqc>>CUzoqEv}QsXYHtuuDA!cZO6=d~X^XJh@5X5b}|EZ8c|L3P@F!mHHMbOv1cI+4&*W9i+}VO3ive+HlF$fzSqM{JiVxW1;sxT$XAcD)#I3K7+Kvg#uVGr#%#0UyHRdkwlAfCU4ldu!PNF;MZoUYpL2+#%eszo8@Fk&NQaZb=&0n%Kqb`#5RS$GzsW+pkqY_k1PGsf^Om5#ok4egLD}>x2wlQk+E?D(A|13WU-;95aF;c0Yfuqa(5UY<pg8kDd{rwLL&Tq9&Mxc-8fnH$f68vWY^yW?9ac(+O|?BfmaShbTK<~Q%>a=A(_e`Cw6G{+>YkEj!9>Mi8}iSKXVFpXsqTffr7A5Y}`LQJa%-Quy%^tHz9p<D7F{{BJh_amc^kOZ)oRpB<$i%{g|A^5O+jQCF=b=1#NjNBI-L+_oXaY{^5Pjoi3xpC6wIyf~eWB%KB)w^V@X^-Q&8<=8gQiK-(J%+1|_*6FzNJ!9DzK5YT|(&uV6d(hs7=(^?idk|XO#7rBkR4Mtgom%ZsLJJt-LFm7u1!}3OoOa=?>`<)>*JSe9sI%67G5txe9L>|8o+n_`Jap+uzrzuo}jf+>qIdCnJp&w6n54sBSP&GgzsoWg;N#_L6%x$>to1f`9K<>@gFS*JM))fM%5lT`BBJW_ssNV-ZTvWXSAiP)6qJm_norWw5P_*Z%4nw2cc%0#_mtU;M(}y;%<8W|!hUYl8Lzfh9h>8H!!nxjI&~saVb7W_s=_z+@hh7zzWz{df5(6vT3b*z?$U&~U<~0fALO(=t<X0=WJllIz@SZaeyCfic{~?g5rFjeXhz_$Vq!c*<Sgkcd7$*AQyk7)%*9yXOAp90x^wEs4rJ<)$(U2bst!rpY_aUK|-dfc5Q;8JLb29eBD2uZ&c1f@=94=Ia=$+}U^XTfj?s1=t(t~a?Nt!IbuDHe08FDwTK(HQHQVwJI2<%#unB)R!vK>&(&-BH*Uo~MQLd=xcqV--snDc#EOIkfY!&5?W#u~f@OGNoL+1l@WG0UQ7Y1lnYK=X)R!2Cm26O|5@rEge|p+rXa1uJ9^MaOmPPVhG>lK`e&fJq@>G2lkN95bT1IKhUAV|@L6OP^94tL-Fi|HUROE^l00x`C5Zq-UZOhsxnPZ%Bv!l~s%$dgTm-n7S0mt`f2zm8_ZMELc!z(mBY*Bj4rJO1SZu7dY*-2L0NRe96dtljgAZ66M1I?I5#GdO=PLNEG--n8pg~8Z%5`o({~ZsNVB4Jwb)8+f7G41pW?h7xR3PCy2MyDK+q`%QUboEZMSe``pOxA<c^?3xD7ZUuJi}XxoIRx5Ia_X$3r-c#-|m{&l#OL0OcAqu@IXE-IChhFOo#K#k;a;miLk(RcfWr0=|rIH3K^Ljtsr*oj=+lzb8XaXEoD=S7rh{Y1u{%;EKE3~+NK=P4{qNDaiPv__rE<xVs376iA!tkYL$Pm079#Tsq7x7Jdb*SQM#u-Gdrc_0Q8^fgw)zU4rP(ldlAynBzK+&ndkkJa3C2|j=M++SaJcVW?XWV<%j9}Bb8unnnve!`|6?!L1bwV819*wbNFi^E=cMv86II?4+DKB{AOw6iUGX0p~!ac$!1xtOEY0|l{l!o7ZzKy82;ATbg<CQ-H91mmHL291z<9?OuqS7<?HR9gTHRmGAkr})C^I)_E}PcRqhcr9r>Mdy3vubzOLmnn1E(3hNNU+`%yINFhlmWyq;ryAvtmpOfPiTeIQW`|s6z(ByaqRR~k+z!ifmf7;0uZV^=2nWVXlcbTfe()QpnnBEs>DY9h<#B>^6~Uz4)}vF~=0fnBGD|4Ogh5a1&?c3^izz!B@{k^*b-BRcW|{LsV)n4g!Nw*jm5l9ey6^Uqz=lG~9R7FQ%ag)(M0<<zNed5mY%X=3E97=7;Of+grkQTLW@b&De?)ogjHVovHn5?#y6`zU8LZ2U@4IA5cg?`N%o?*kk+woC&;rp*E3Fc76HTkv_ag}tnK)yAF8HGj+!FsCw|bwOw|UtnIi`y}n2SXFy6k?=ZZw<4Rs|pISAt+p{bqK8z+Cto*nnr<5sdi(Qdb_$4}2e9+nkI<VEv#&Ots7U#8#}^!mlaBv2De8V>cXC(8wH2IhJ5Q9*1MCb#>RtcK-n32C%N4X7H;U%_NxwV>^gCno;SzQ~=sDN<ny$GlAxG6!XG@)Uh4qB=k**ZEjaZTOTf$$f>`NeA3hB#}q5fB=|j*TAB>87T-msfZSp86Ct_O<~o?BQU}@c=}@=^+l)lfLe{tMs`M9Yswpc|Dgyb`^gApA&rXmY20CFZ-~vyzb?$f@AxIP(yGd@Q0_7ruAX5~)iQmd`8}D4F)dsvSof=-%tI3%D68XAX#LZNK0{<)u*6p2BboOG6PEwp1HVG{*U&l8jD7?DUB)7xPHS8Mu@QG$NptPrDzYk(5G52NUv+om{bWim;Uu7zr5xi_w4wc>-2he-B4qJFq6oinNTx1MTt4rLQjhB*Zw=IlG<@zNboh7HGn4(W}3?wc#>s);Ee*J#^_BvDES#->Z+I*Cz%~)^(z!kxDB5Z}u`+;3o2dp|U&8Qom$<IVon|O1UUiS<kcVicRAWpdb;_!>k+7Ph*ZSu=9hLb%|zn6KNZ{&C}aY_=%-7*4cca+6kY_q{$yJy9#>%}vL84TtdFu9jU73o%cjMSn-3C|XW?rwAsr+B<u*I}S3V($r`NH9|yupJlzZ=XvoU~uShhv{-womnHeB5lTDV=Dsa#R(o{VLv?HgLl{0qx|^p=hvS;eSS4Ryniy5`A~{>{qgl@^Ye$hnmuo8KE%Ii9#`vBBn&|0Q8eieq;a>K^Kgs9p5J1xPxLB8w<=mGVH3)=g}ZQm#b>qF$*!6Gf<0o+7a}70K-uZ(HwXF4pYOl^<)#l_Z2<y&hS${eb4EXbk)ZuM$3&k^A$UXjpVyM(N&oY2UvC-R3EIiM8Cq4D{q1940{t+HII6wq?QoB*>}Cl4<G=j=!;jzn?aL>B{@uI~c3}5YW`AwF=L*PLY?sswy?O~ePP+X>Tn8<&7tJ|yfr+M2wE<(@?)-K8HA!2$rp0%_nTpCpSwC5#C%k(Ea8$E?`~n%Ohu@~Qrk9I|&d6@l7^lBDCWVZNT}Dow6-dR>C^>Vs8T%UeDDsLmk$@u*-W0MJ@B|=3lF0RprH=ltwaf7&&;}Fxan83HPYMB>%f0%E9~V^}tQ_PN6@SY*LOW9YAprjL^AA6L`f<G;@76uFX`+svrl7Tnb|0sR`szGAL^Ck@4OX25vcOHDzQEMWbM92)CPs6z7oF!z(a^V<1{v|;1A=~xR2mDHT?eA}(pLv>;NifOZerd6Tt~I&Fes&7`$Kce9h;(<UzBQvn+Fsvg4;g(-f!zwl<m`6Qta2_mkTgH@=D;Fsm-0t^MGZ^tPyWO<jX8&<O>syVc{HbR*3iJ&XEhumxMP7iNu|nqS{xQKKmBGnEY*6P6*^87tDA+m2DQArFnkNGfs6k%UNyO=O(I}uy_?5Qg}(q{hn`uihom-7g`j9ijf-8^No3;*Z#9aZ0kZBqj4jD`|I`k%Pwf=;7yTAvRMX8kpqmX`;xzZIB`DG;-?!TvgpA?LVY%*`Pzw<rpa8qqb7QLx#$nAMel$CdTNj-u(JDD8@1j|!tm~rkN0)tB`NOnyN)g)qM3MU{peN=mfE5i&qgA9zz&XvkQ{u$71fVwFHtCLbNd1F0{=6~8|v6%+l2l!Aww1mi!%Gc7I^4=TO?-@A<yfeq#K-5snLdgA<<tYns)%si_3F1dn&5I0Q#@?pJG=88`(OJA$Z8>Qv38gwT2ozu5FP#Jq3V0xu0%ZlurRrhls}q9+-V+SuMD|_)A|#OGLHp1-7?JH5HZHUx=!7Pk4!2846@>3nq!&A0vg;nH+W}cWXLCm=v<olb*7+{yN%F*_ySBh~P}WNbl4_zj()GozqfNFk!FZ*xw|vXWKP3qp;p3fVWGfXz<~kN}A@<Kj8*z{iJGJJ#0JLC30RgNtfs=??9bxSE0wl&JfKTvV1_{kaSaBl?MoG@3$knJi|R5w}H)Rg=k>>9`aPWv`}~7@twNm94eLZb?vA3jhdXhDe8dnza4iB(^Btu>i4g&zg<H(Wqb7cR-Fr1q2OPYKGdL-j~tA}dt-)eUfthgUf?bWBe8zSG|A?Id^N=*gc}A1J7%b6_?`-sF#;K6PN!T)Ijht(uHHyBhFOf@7nQXG_VHIP=IF>CnV$;gfPR7g5vXt_WwX~m*LvjVAv~KyBltLG=)TtEOY{ruz;fXVwgS!efDeMc3{5TG|MC6q7Q46!!JkF>xAkEY+ur{nJp4>vh<A)<UaTEHX8=-TE1HcFiXBp6wC(|)mi4dAnO^s}UV^bLT9A>Xr6o+j(jb2)0y<9dg_!MZL%trc7l94V{5wyQ++NsYAgdHy2@Wl$!<Cp>5UeP@WTXP*iZd)Iaxw!Mk1sp+o$HK-c-V`ZK-n(YaZIGsNTry4&jks?z_E+)4w4rtD2Emrr`@;+koI^=!sA>pu20Tv+pwbHl=Z;x!74bnRw=|N;}$6ppNOOgF;(r|q`!|`SOUmLMj4^<P*-eP0Yj86ivlt@=}hSE3`@;N`<qh7ET<OgXo%(Ak&GmhFi9M)_fgN6)P`8sHq0K&@_(ouuLs+xn=-fO+r!Z2@tn9=qO+>+QqcMsig-m~O0j6Pq39D@Ns@{5HOx<``<%ERLZw0*wGD{@>gj{T3tFXR#!ach19D{0PQ8T1vdD_XQ8utbyB%((Yj)kGS6dE;-b(1#(8j~M5N<hxq3+@WM26@tqq&~Uwbfllxs{cTe%Ui%cO$mg?h<O?5k+klr~AFZz#w$5ATmV|Vkztm;R5WM_8;d0Tu0PJY#tju(VlJK4TSKdBAix^b&{_}(8ZS#1vN2s8hflmoK-?AK**RNNJJG)i`K5=U1%WQr8+t5YD>t6tL*F7wFz1)3cKxNevf6v?tNrz3HAXAmsxEBMfL1GS<rbbF9w!d%F_Ecxvi&z*mdnt5r-o=?fjZmH>lsXyNedrt`n~XL)U6X@N;{2x}l;j=Q+A|%yZ~Q`SuB4#`%LHgRYCHimay^Bq$QaE8f;dt>^TB>uH<P90xmrnh}%l0+%cys~l8PyS}Tbo_r7q9p4U0Jp<7+y$qLBS>NX}R7sH9+G-#e1xWd+v`tr#0f0a>30!2yNdQRgwNOZNMsm?iX*PVXfJ>4{toX}Yq{Z#>a(#EH2Q}nBs9g-!VfJSjitczB*noaidBX->?^zbXjrlH~A2rOy*?vsQt6X-$LR_Y<caQVVQJF2bmtZ#V%(Mf@zO!SaVoCPNv88}M0Z}P=T(XLh{WggT2A*58{_bv~1`hB4a=V6|TZ0a6jFjGubxasu087>R==6R30a$*YFCV<R)G+4$2xA$7mjEQv{ALT3>1eJL0RbrFdGbndwT%lPb&<EyrdpT0maiLU*^N)I8Cg2iBNVAF#1v`t9bZyV`yDdwDSn3^#7dy4RIok_wu_1gVwb}K-{s!HZfdiey1d-6b>UHUvfVJ|b4T4@x0h=jb)WO088Ajg5d5A8Eb=ed76ETsFMA{HfdGBq9bFXi>lI<R&8Ea#@*b4=B0It~h3j?x1U6gE57_Rqxk<o|T%nOgY}E0u$Mxp0ElwaZ{}H&<JR~@Did2c1y=mibdI<pgTLeXEJWhJrId6FTv98b!itbA2xS&{^QUL_7sBl2-O`wn#+#X8-OB)Q{JlbK^gyRe>O{Nef#+TFO(~(ZS7xgd9i*d?7Adrf3kd+dEUN<cPY+WMt1m5ve^pPPACD(A%znTkSp6KjC<cH0TYRnq-<2|voXK#4H@&P@teIy96u@G>zf8E*d+}nw4;B|;>_m@U(fT8i<7^#l_g-pv3vpL5A@;<jtLH5v&kF+*DF04Twv?Pvc2H~EU{?g0TA)c<Mv6+51=lsb2GK4WPI^Ze>ym{;FMj+A-hgYt@$R+CJu-lL_g%KZb0dR#m*l}O-sT6;=suV_cc>7p83Kb?Z6wjt<O&7H|MLP(Hs%bVey0dH|7@YOHwbl~X!@MsO_^W^mx(=~bk$R@M5JY@{1ykTVU|<4bo$w}Y*0rj!D;c)!I=@aN?6wFUDW%OKy$k&q!7g?y1Rrz>DVhYLDA%gM*dqU=vK+xfAI0RcqFB=x%0-OjNH-OvDCmk4LsDPowvUF+Bx`_2;XPkAN|h=o)=@4nh&%RLa^7c6#SM6T)`}$_S23vf33QDtOPH1a3yCzg@ry4?x2B2LLAU4B=xAd0ymQe-p)e@$x0EX+<{&0Dm7m+w$4HbmyKTOng`9O9QR@q(C`rSEVI!n#Bp1OD5l4{z?z>U82+HQPR~{{=Vl?RYf%PGJ7GN}C#+Hh0oMvqIg-lUMKNQuKm~U3q2fZA2lnB(s-2APUG}0neG)$ClK4#y`X(S4Qv94B%Mo@~j*oT}-+QUfb?hbiuES&Np=p>8LkvS$N#Uk6vK9;;UY)fm-`+lj(OPUjnPrh}*9HK&$gV<m`N6M*y(jXSDcKC>yF(5p;CcVM{?;Bc~gDj?v5y<4Gib|&%r=JC3#eV2yzH&~Z%*R@pc#!U`5493;K`*rEyVYeG{lGn+Kf^sArd*k#(;6*g8}eA0k(D2v#=*_m6Y}gj!Bm3@^DYS_QP!!=U6h`Bq6NX&UM_Z^fNvR*+hf^QFtWC;gn$vZSgKgl@y@wAW8~@xAXefrA~6<7{3p`={W!|)@%FHvNAHs_Z^EBoe$1G2+&oNB5?%={NhMeu<!1V#<)o9u3`t?^IAla8JRf<AP!}K!eo&`!-$7*ftU8>5^ZSpS*9D&X_*G}bP_Z{0a^JmYd#2?c+5_Hv)B`?;phW<%jXY1sGzMsmMXP>OMcmx{UQj^t!sNUA*?~{JTZsW|$X|D;dm!+20k^&qaNF*zxl=n$c&|hVXHn$}H?aziT7;cMi6jV2h1m|Tr7alXSSLfzN(wrcHx<Gv;ATtJLiF>Jhkddh1bmAbs3kuZOZ)$E_hrkG9LKUhgoj!(YkA}mVG_+qj!dEqPuI@>|Hb7@S2emaJUl$I8<Oli5ySxKTq9%gaPJeLz{f$m(GW=b1k$dws)-CaB#0^C>%i%|-9Tio9jGSgg!#BGB@-gEoR@t`@Qu+9XNY~L0uz1ep=FO6a5)QmD0Y~m(*t*y_%)9Y^mS{GxrOvmK>rXN31EgqLOm7VS9rc}55+V<?a>1>Fp?Y>@=6fw#Cxs7{H$;aEo>(wXZVkTkr$e}si`*WVyLBGEWK7k2&JN6>%qu`JX97)XFcrOx~!tleVO|ryAh<BkTl#zRXy(ot3wXQPNko0CIr3>iQ=#Giq!^^nE~8k4_Q}OqX>PP`GMuo8p>KSA~~Dq^xVxT`R1bC*&Hf;6Kc!xr=G3MsqvguhUXVW#Bq6LJ|`D4m?WrasN;%MIwd;XW1ve%0gJPq(%xI)-o>x-n9GH-Jl8{u8HzElag$?P@A!Nhw1p>Tr`78^ZkaM2PBn7KD9AeMl-zb}rco6ez@1n!4w^aU_%vn6Z0j_2cB*sav))kbHh&P_HD@YSE_Bddp9ehVF(w@s^emNlZL~-;xE0W>60#@zH-HCDt|v8Z&jC%FSLSQ-;WbuAO%<>G95|J~Of_Uz<APrlazM9xKHWWzt`OO6-R4Zov&^TIAaB%!sYQ9+a?VO;N8!9bF1kFDWQ|iO=R-Nq2`Y!ay5R@;^%U6av}q0hX~w37?<D2W34a@eLDr<rOQzTeSMu8ATl_3IL26LK+2ijX1KwrzZ5zq5h95h+PU(+YhTyGE9fGh4jHUxA$v$&hLr8MaUDF5(np_^Zf0Fh#eoW6nhYZiqVGS=;NctJK_=R)eL@~82Ps*^o3%o!*nMyS1GlDLwUYe%`)NtKTZ`MnWxCXH7xsCzGvJW`*r1o$-sygbs9hV&Y+4K5S*LBKwdB0YU;uy!AZ0(M^qtt$&;<$7H*b0L_A`0@5KD5@N(ucB+1izP?HPgt>YJ<hiBz+}r&HE35l3SoI?px-%sf;Dj>w<YJ6ChT?EzI8f25cLUCPfi=G;-`tBD<>aOxK3o7oM5>kkB(>PtN&MiQ<7;W8L^GzsURt3?UHg3(sh!$g1ly_laEbmz#n%K4btZS!bQAhGooU4V^&d0%KU~61uYwIt3<wO*Cx-7;xe|?^v&x*qYFfCFhiP0TsuWeStip#`6@o@XMN@wXhe&BBn*6B>8sS_h^&ph0-bGG`h$`@qp_R0#qmysm!m@ki91fK@VI|ZFG;V+rZzbOzDv_oH{&mbsc3BnIW9S1s;s-;j8MO-!<Y0Q24C?$F{DOf!t%Z<c=~$ZODwJDC*!i{i^aptN&~SpMZXhfZYN5GhR9!{9UEUusT4!X)tft4go+RVQd_Qty?IHLLpLs{KG7%-pMe5nmPUv#>PPMacfwL0yArRo&3yw(3t5ecUW7u>FyxtpScdW{l7LPWWR`oYJ#X?tBDXuLfLROGV+BKvTb?#LJEz|JVaewxaz~R?VV}6cOhr-0woJhvrrrI<a1yC{JejB`y);^L(wRijhJ)!x;t<T?tT}VhKK;{d#zn<DwO(-r^`YbrTbtzcwZ>1#q}1Skpm;|6X8xr3H}(ie1CC8=z6NO^0D*1*p&)`vbObrpBGW<9OX3d&HwR}#zHQ`n9N#Fepnx{5kN011(%*3$7<vdj;?gJr$2dY=Q2!cryo}#(1e*3JbRe@o-Fv~oXo6hO>vP&9*xA{9dtl*um{KHH&lPQKFdI)Bi5<9V2n)jxBtd0!>S%KTof{L%<2a5ckvk9CX;-6uIS?!Ik#3u77{M$bS~+h$c=?!49;nTf;oO4Ja^5Fr6UJs9QsIOWddOEsOm-ijDnS!*_go(QT9LTc=>pAeW;U8Zb)v1rb?XgP-=8~=FA#1NfL|s4cZ@d4E!2RqUfuii_vT{|M3>^Za(`9gmm`w9EWpCi~0=Mj6L&$5&Hb$=j<lNV-9yG0o0*BFuNUKE_@Dbz?&Xv$Ek9O?AmV!wU6*LiGkh2TBu#j=CC^dmiuw$E?t7wWtyMGCcWS*u;hj2rDMR+@RI!aGF6c)Cu-`EfcS+a%9&j_M0YZcu3dpy6tGQ;oFe{EBAkyf0Ctx#2Uc39RUY~M;#n34z#J9iwIhbQWsdO2+;j1hlEf?WdS;e}QC_D!v*lJ4w?Ix^QPfj@Z00VKl^zIp&hwFQ(w|<-8;!u`S+AbsB5tZ38+tqBXdBjzW7Gm!8sKbT@e=TFJRv-7>GyN2tIT2ynQVd>QEV)h^}CmO>*LJ;j+Ks&>Y`IO7j}=_SuJ2@-PnPb9$f}&Da$DHDLX{g0q&21YiL+~jISmDE4m9PtEuIhO_#FjZt82k%JfV?Zp|ge+~`IiT5E?DULm8ty3K>dPc+}WU(fH~K4!`_Tb4{K?N@cuE?bp3M8mFqW+rLt3&|gy>$-1?1tUHz_O>T(F7pIwbPx1^1YyI^!VnlfJwi?K6nJI4A<lwHe~jh)U@)^lWHU3%2Ts)VydyV)QQAm*DipBJam_PqRk76NFD&w{VLJUoX+8yz#Lo_ZvoM9Y*)*7i;bfPDFz!>lz68fG&=m3A#U~WZ)CNtL^7N0-r6-`;Gd!8;R(kZ!8o?ErGVTXk5dh&z(2O?chsRv-F7Nx}9r@$iZ$JI<&HV5MWWPP$vfti+{r0>0`HSshkMWVryMEKW=*OCGD%R7gx7jc34~JifQZjdI#LuERR)7Ba`u#7Dfnw2h7*9JEW8+H4FwkqU&*0B7Vczw}1a-1@lma&ZM?e6iyrmEDhj|QR&8t@04-S6@eDId(*YH0Y6yoB~-uo)X;3E>Yt^FN4E=SwwG%8TYJpMRZZDE5lR?WTb#^Gook$;BpKi~b5pML-4x1WBP;lI7V|NY^oJTb##bw*j(kN6`t+oZfX!F1tpognNs>42gTOoeE&^bedvSMO7q<*EyjxH%^tqg5q;;22sjjiAkdGZAhcF~T)%VJlY*)G_+&Q}sXp`sLT3|M$-U{qZlKfvo)@^c|qGN!tB<d$eG!HFAPM6XAW^?KmAHMidO6IOOxW=&P!JbS~P%*13QKIFHlb!kL>tt<Mb{sga`3$EJ_omaTNE96K2*0qZ3efe|`}x~pUgL{;`94p!`WZ(8*=rgYoF+#DCFX;xM4)=6!~C4xCyuMKQ1En<eifpG~t20(U|Sz=d!9DH_f`+Qq@Xg1W_XM%xp{z7KAgEu;Ex@Y-Cu=ccc02aIIcgHgJ5nnZQ0h*?FT#stab4#-5ZIt!%pW9qte0yA0Ssq?1FLZ3;_KXzOElikLl+Yd2FY=>+oHl{{k=K~r9BUiPoY!$3ay=#*l!o>Z1V8Qt!)sI-1uILr@<B<|`)HZFoptOn-a+@1JE_&9M$arth7GYi32S$p(i{pVOfzKqaN?kOjf#R%=*Xf?S_#zSi({lXHu6r8vyNa$7mj80J5LOL_RSWHERGrLr7=5)&+Uj}C6%Fq?ad~S)Vm}^LEhy+liawGyK!rRU)m-^sq7#1TCM$QWGN}c!?H?%>&GEfZcw(3`es^h4Rj>pb#ST8U$Lv()UlSlUsr^0hqt;>Z)B{lj|lhXQd5X<dn&;mmyY$J^aWvzrtWgPlU43cv{g4eCPw+~-_E7ycG>`eN|87X7~>YP)R0AhD%Cy{8E;%^Hz%s7Cf6j<lrlCjpwyb&zkv7|zi4~=<b8Nz)=_UT$W(>n8Pj!bFdUl|ia$6&lJ^#xkH0?W3%1p5hv+WiOqn5<e77={uYk#+FhSF(d|p)&7N-l@8h0ufX8tIDc3`u*Q#FV~ez&f9%zvS9%;L1QSXT<9(3s2PW>1A={8=p7!#*5P4Y`iIZLwiPPKelzjrJ$0<IoR!emKz*?tP^f>t$)9m%b8H&Oc@_4MS&}k;z4T&V^%JX{ex=l;$|Bof<Y6>4ZZ#ALGVWbx@8WP3p<+2yY_jx*jL;b3Zi%D;*_A=#!EZrx@#!NMve6VP)Yw%J?EO6?4HBzSeTy>=FUBck(?`Ms0pN6Ln6ypsU*yMl#K`w3S)aH8{ak3xv18!%mTR?nzBawOLAmqm9^$+rZeuwlIx&99{6I_yVQ|(GJXM2;EbR4&~)*7F3LAr*V9$+n7J2U2B<BeRM0YtXxD}d@fIwfM>pb@-c}p=cTpa=*mT@FxsN5k71Xn<j}+tA-=)p9c%!Oj&*k7%Q=G_u^H+uCf}0&%{|yWNSoa}g1x*;1k-w57u__jNiM_Um?f0CAi(lG?41Y6lcM7b-ZP8qB_McU&=2P);S`J^c$|ct7SV1;X=4g|S|^4SFS*ApDyfp8N-36yjuN`C(-_nG@LDv@U4fX{IPGeMahfL8e?@OFVpahr%St~sF8g!KJ*(ggCJHVIP&yJU(^UFU7-&snoCQNNrbC0NK8rh79k$r_1PdF5S3Z|sbUei-YQA`D9`~c2Ju%~T3}but_=Or)7=I@V`SMlVpM<x@GBB#9uU*@Dkju(wIl+gqyh>Qibr*5gc|j28C#zB<VA9hpBjI$;cWvq1+c9@S<R}?~gGbG*R3|Ksp%@8;JCoJ{gRA-8d1}~#T&RFFZeqwegsnBY<qTUCJ#n3y)F@=1Lt&g4<INeMc#>8NckZK=Tf31m512{CaCw`ZV}i)nKX{CES4Y|#a0_?3(e!><;l3lDE@Qg+Ncn=l58!YGF*60zZs%MknL|-xD2%!6dD=jSr<&*bJg#N#kd_p~LekAHIFm)-$`i-NzoJo)-4DSRx-YKI$Rzo)p8qZrrTfyTQ&}>qx{(_mldDm103x#IE4|9zapXI3NDhtR6*;M?Y#6+A<4IYfLG$4;${ePrilIFBAw{bnVyxK!nQIuvgLe7MX7Rb*W>5!t2Iv#Hs+0xq!_fxHH$>dw<k;~##cH^NRS-r%g9nvPK3fp|+1G*Zdawk?ghKfQ00;Ycm-ZO^Ci(@|Vx=WYFZ=53A8(tRY93_ic_v_rtYZ#g*`p4tHeVr`C0yvOMJ`E_{`;`5<CRwv<|@9}u?4QRPuS!`!CLV=yDF%240IvT)$a%0YbuJ!Hr_-LbbA*i^2!j_df$mP@c9@e0Gp@%y@W4lVZi8uk=wMz8pVDGi%rNVTqXdq6l9`2xA8isGpA6ax+Be*T91&xOYIX!=OmEtPD@0aj}^;7veR4$`%egr=aov9s9S;E&Vbrg78d{9lq(%S815A3!P*SIbYI!O*~F8TGV^MD4GD+Tox)*~x2yM;Z{J)XvG<y>e+MHkd3o^2wH-aq7GLCyut?248Lp-F>g!b%I`WEqUC0`z(XdU+(%H77fMIEmhElNVqknR%S<9-v5!QO5;#+_T7og7IT5T$R22nfWfw1CJ>^&yRg$)e}ZDs1w!d9Fk<iGPQoP65OdE6$u4!Uj`1(-5YxCEI}2dCJ%Zw<*wvJ)=ifzuEPteSL;a*`p`v{nc%4)6cqQ_ZY%h^+0t7Vj!&WN553hKXZBMb6Y_+R#~t5N{31TCBCIa^mD|;FVKaDUyxQG2BJwi=%iP`3;k5?V0sn`%pP57ad3q@Cr9N?VkPF)Uy&4*E-Z8X-U2x-_!7^fb(RJJv-Sfm`XhDuD#hJ-Y|Ro33!XC6VW;%fDs(y8`UGyt1~N(P|-s51lFgRkH!9ZEcFl`@VFoIT~>*jwpk`w1O|Y>oC1)H>s1TNY|~cMBLmDg$O#~)M#sWs^tjJx{+vjaZHdi~faF@_CBT$e$Ra;A)G#*V5^>WR!Wz)EMEwB0>n3E935S?#5enrpzz``X=J#BI+!(Zd6>4dVpumxijhO1u05Lduu>$F$+vxYGKl9oNv6w4?WHK11KD6mvjs5)SW5iKgCMJTpWDDj5?7^>F$4ZmaKJ_&X+lsf0_p|~3!<^gQRMtCGBeNMGip{=`VU~e;$8bttLviRfXp+nE_-b%GX=4Y?9{2+T!&tuf;E6G_Kftv|g9fY*_6_lO{n2cl{TxxWMR4vcoKc3n%Y8;jx0a;MNXEeoV;+Wl_k^BLqTKU-Gr&BIeGL>eG_c!rcWJ=rqy~YTxX=GP20e8q@Wd`2DUkLzdQQ`Zpm6e?DovW1fN_-kfeVfQ&%gXNQIkz_;?6^T`ZNMZKOUfxc$ynJm=4p20$-XCr!^q9j;q`-hDKroTO~Ya&fYcQH4ocUN7Ij6MZ(!*6no!k1J%eV0wh9CvX4BE!?Oo45e93I+BnK`5IqbS3fs#(PMxtYx<C~}ANJSA!t*#M88K>5+ZP!zA{azdVs(dK(yBcuQRjc*2F9vT$voB`w;8wvns*qss?H5}i{2B;EFi6DN0G2U)KwNSgb&$skbpSFJU2Wnj1G}j`gvW=$0~vm?fKvzJh+&u(YgpBf@N;VSMd4Q>)EZ^9E#2!2Ol102kJOaV;7!7{#?l|6pr9D>6)~xRL4q-Za+O3&YY(&#_<H`r_kH^m4)l<jpx8tRA+uyd%=ZZYU<;z)QYbO0uH4${Up~pMjp|uP#zOEOb?GNY4$z_wyJ3B9y$q@Gi0lHj4jE!qNiu<Aau?GVNE0aJ%?C5m%>aO&ZDzqo(J`Ck~$CJd4D64es=ZdQ9Y69sz@132L7STb}3iS^Yn`I2`Q?`r2`IVn7^LqS(e5T`+q}I)$=$RE|SxJ&P5(SEaCuOKf<dKH}TI6f6I|t4Laa^E6;g-t1|$b9j;1`2{fup?_X4xp69hE7DtUIim=8M2PH1k#xdSaW&hyB@31%egI9>cR;79FB>Vz3SP+RJpBfkd;T9Dc!v>4p0O0xVYU4f3N#zMZS=};r()r;t7=%nc$waB-R9aff<L}3>LV~D<rJlf$LdF)MYWYyBug;-mBsKP|(1iNMjcRyZSoVRGifK6ok)RWd#4)a_Y;`Btxcl6ODM>Jq5b;expS+fbiZP+G%v{#KIGP|BhzHBZ=*A;ud+EWHlm+Q{_AfY)VWW5iwDDMggaxic$HAlkT*?PeA{#fBZg@~gzaNdNV2+f=`<{zZC;3q71k@x$%8RW+*>oHZJ74D~j&FwApeGL?<o;^uU`C^T7|=Om1fF!A&t<MMf*mac^H!BRCDdK(q88wYMoo|iCb$JKpjB>(N+h1-RIo?q9mK6SXX{L=G=v;FtcX93ns{de3=o{Yy34h9F(Z(n%8a9y(O{|1`_=Glv@b$PpfY|{Dxl@rKsk$=sM817b%>r82rMUlJlxs!P;J6Bm;*nT(c(#<&3T#S3NPi45w`~pSQ(}sc)?^0V@~pb;3Y6Q8b!n9%$zy9<(YU*uVaJ`3O+X1WtjBIUkhSOB9?nh*MF`>PSQb|h}g7t-7T3&0~{dWuJELKa9Q+%<g!VJ%&(KNOM}K6QmBJ_y>}*rKIHC8OdQg-5S@5i-+QuyUk91s{WArSI^7bSB3dC)OZr4VCfG3;!bVfRq#iL?@hNqr8KW%IP*5bU<@(IpoAZ2J)W=g3o%4WPH!h!obuV(cJ7!OogAGydg`~h&>77M_x0LyelUwWXf`nwldY-1`srZl3dT>?9MD6^HKGwA}%%gA)try`#RZ*SSEqg?skE`Jgef;KU8;@WU_l{hT1{Y>UiLhJtHoB0)0;U^*Pob)G_!l`Mf|$24U8)3z$>&M-3J+50|I!0HZ&P2ZypCRm&k5QDbX((Ii~B@oRdR$SO`^7tZb=gOvfsyEo=UHL6#>A!$-+Zfp5!3U;^Z)BO3<CeqD}&RstgmU-u>jYe2GU1Ck2MbtibWN&nL5CzyN6urcjcoM-WYjxQf4R8NzN-W`ub;OPi9QXq&gaV+D0p)ZQ0gT3siO--QkXZjRlW4S~jHh^pp2Dm?~|yVSGs@Wo>|6k-Y*$_q~)!gc#2h8)(eq*T<wh+|3e9?{c84^cYX2G8*$Kk;^+=8QCwmoAA=9Z}-tL*sb?8fkMwr$P4yiNhNf`G++sj*CXocqAQh{oBX*1qx)AH_`KPphW1P$H5I)JJhH2L;D)dU}C%Pr(Jj|Ijr6$+dOOT<<Q04{Y4sb-uGC4+l8nQyUq+PJ?4IlS%xUabn;N@kxrZzPZ&yQ)-QvsHki)=bHy?ph2j<HN<$UG_JH#=D4Y>t3I&W0_w7Ae$VR~h4UX|bGj%ATQzbOur#w^{O2<-*9tmmli@_;n2zAhLp7;gXv#>E$Cv+(d0ST(#OH4`RzS717f?7WC9fh*@l=GmhnWtWq9u~1K?O#*D_hr};LL2|S?v*m^J>4q|Q*ZlOnwFg>h$Sv7yF6qZZfTd|PBY{_$>C=L%EcJWZExo|su^WL={zB13#y(m&~ZJNwFe4o-;qFKi1=Nq6!iJXjB_`w0qu6A3__g^3hLZW6EhY)N2F(dc)CAP>Jos;_hTiHuh<Nq7eG9I9fT0n1p;?=QDt6uEtc_o)9@qAxs-A3Z2AHxgh-~n#_dt)X-_X;+!6^Fs9xKqEFNGp*JIMbf}bkW8GP0oL$Z{ZD+U_Y@Y2%5r-ZZi^hqo-tn!Tv2?KusgY3Mw)7aPl6j1Cut`jyjPiiK`L~mu9QVz0<R}I6~6dwtRVjK1uo@W=2DM<DO5X7jEUSjH*C?iPVPc}2wfoLjI?WHzlweSx`tI}7p0K-fv+l&3AvN&m6@CdKk=}%6pENP5#GfM>bU{OZU02pRomU9l9jEtl$fHdR>wpvlXIYzk0S*}5bw5V-pam6-HZXKO>Wga^3r6v5dT%d@lN-pkMT1>~`nmf2U#Z1c`7Zxo-Loi}b$~?VH$l}XVF7tEbor$I(l(Tb_GIIOJX7Vn(=?K|`Wrzd@*sJqsJ4|Z=nSM`ZW{#8wIQGD8CYn@Ie-<IqG|ibAn3pf7d$I#euD<Il%xkXJnCMfcmAQZhha`fJac_D$CTd**KoY407Pp|4Ig&SsWOaH3EUvC^)a6Gahce_T*I==fbR%+LZtU!q@wK;47Fy@-4PJGXVCd=_lu0Hz3+w#>Le~qc1qFDuSE!UZaVKc}EH{NvY(NsXR!YfJV_vhQzBno`Q;Ky}n#V5nwd9$U_nHxuMt4Q1xt2wzBTlsyarm1DB_xj<b0q4yGpkCs$-zGqx|_HO-lMSf2{UktV5%tr=D}0`p<YNS`)i*KrtL&Ey?I{NH9}P`x$0<#puy688)W{$(y$FN>65@!<onNaS|CPtO-w^aM8r^N&R2VqOx)EXjUX4Po|8H)O~X{wq2%Ka5Yg(GRElVrM3m~iU|vgSISzFP866w{*kDGPmPs~7ewJFFP;8NfPIDSBx2zDj8OwivGN{Vzu?>lgo)KbT9kH2+WWsNfHw{mZJKHTEC-9CX_6vq`#+Fu6AmaNS*z>cn=^*w)tSvaHWK)(QKU$mmrlajFvm^;@%QD7=Z-<8>NQbMP@2Sj+z?bwKUf&0{FbX+;yaF}~xQ9G&WNwATBnQS>Lf#sD3V@OW)q8l7RL*nkm#Uu&g#OV<<dPMAFw`Y+B(R<e%M65vHs8;5w|c9N*_QD=EH9#A(!)~cvMJEFOLR{nJjT8L6jDo9=6v(|LY7_bg+k3&3DjELY^Pja2W+zri7WCsk$WXmZ59#EUbq`pp8ibWu4BrkCPH7zdZNqyl!haT9T%9L6=7x(ZG^Vy7h=$|hJCLTtds$wIaQ7b@E3tD$1^T(7?U7Y1frT88DfQU_l*+ff|HVHWo6<{D(iX%F}yA^UdV=RjG)X~ur9c8LvDnUC>xIUr3P6_eHGG5`A8MekzE=FB&&1tnMeS$oRZ-97qGX4Gdq2oh8l^G%UD4kI_U-f=;ft!(l7$r?9D4HY+S|bKbD)>Mmc{Jg^)Zk12Y!OQ=L+W-S)8L3&!w}h55ejfB(m~pa1ojKMZ>4SguKyeWg?vf%+Oi9>n5AwTIUBKCxMzn6Q)Jxp0<)!EC5R5oY`@TaoAS;rma)Q?2)sw;O3+qpc?D@XjKJfr3T?rs+2b;i*GvUK(O3TgK6d0ptDyn6DApgIIR-gcCPpPf_VcB{7ev3PBK0a+h9iM&W>ZNaf<l5@eUThDWO0>0Xv7D;<(Oq8pwlsrr$g9c)AXr14orcaY0!P+erc7hwEhDw>!kjup@WQts^s<DCLasv>=y!>{O)=$$9t5pM{jI1-oT_ZS6vR;HGn@{%%zUSd?Da%TP!c+Is_UNe1J?A4?UgMgtyk>5GSxX2vNQcJ66)MX|Pfly>$`>jVTM=fBeTs}H5)=lQ&)oUnT2an6R&EUZ;zEAJU*>_pdBq*i4i&l~4b9sxX*_k?o+HKtH=mBoq(+4h<ckb&jcF2p1vZ=N$Dp4qN4u5Uwp8(ngo#Ya|KhDs6ery#bquzkx<OPmsqz*EFab#+g<k4FiH3YV*bb@`*D$Hlb<Et`F$C#t{m1AExv5OCb=}sy=3K8>(EwZ~QwF@y4GS}MxXJl2OlG#jufUk{5)(KfgdNI7?MP~<&Rj_Nr9+jcfNl{Z|)trT)k3+@><H;eVoykYyXw7^Fg0zmKdbKzWHAk^C=hAP-s-uiWW>Nzoqfg@KMu3Ytb|Q^4cgl+?G;J91nB2Hyrt_He0*yuf2MSU6=u%G|&Y?$H-<ScMlS2Vp>8ifRI%;){GPf8$?`11F3?yYul^)^yEOKdE+RGzd1E;o(7vR(}3#<?;2v><QiigYea%fsqDUqZf=WIU5zsu1R?bBsldk8C_V7@MZmpTnmYk$zlL)volxEA7eH6&2>>e{@g^7)Ev&j(d5aNU-M+bO!Hc%gZt8^?-1K-kVZ8S5q0Y1aE7VMx6sUL-)hKqvfTB5};ToTs}as*+jeb9xoe6%U=7DWa_4drUrBPJ`;CRdrgrD~5W3R%`U-B_#h=u5uzV%#B1P37$~#7kT@yZ-%Oq-dF?s+O+Pcmtbl#0GToR=iBV(LH2tevVtf>q~X**d~aFq%o*G~BL4m^F2yL@FVZ|E_J-l)4Yeosdd<0anTAg(TE!0Fjpq%`bB<{T#8H7rEB8>t&i*<Vy{jW3pn_MH)=Y#9(_EkO6F@+SzM{w8dkp49^?Mopu+oH|RyqfR?FSTr6Ds4uID3vJba4xd>S@&y-LKCcUaj%eJs%lTC~y{4AD6nEZW%EoeFCSKl+D#>=xGA$2ay7pNJ<h#1qE`Q<(ZYKStF;GewhIB`%K9+yiv3>Cb*C9ir%xvUClP^A}3Y*h@wDF#!ZGX0Fw1p{3}yrbSV!A--WuJiYEZWtk2&7y}+g8W$a50#=hhwMod(lXp@TZZD5S6%DKsk6d0q!tO)5&Vq7Z6pf?>EO>{P+4tj9f+m{WDZSO?*F$YfF<(SdGVb~Q?<xUSots#LiOxw*4uTdAPS&W5IsU&LE$&A6LhFEkN-eONwonDAzsb7R+IfmLrWXzb`mCU_9yqG7#C&se9S&)o5`}2e^3ba(!T2;jXX;oEkL{h<p*J|k#)#z>WVhp)%Twd3XJln^mSP-gx>u$I|%&iBkL>pq{hOCI0*sqwtQ?Y*qAEVA`du~}?d7v)C3-rQB{{b>V$(AP1mtMw>Za-7+38+L8d5WZ>c3mcwY!osm<~5siv3Y;ZXO(z20+&(QkS#>u#96hayn<d-k^p76Ac2z!jJ@U()tn9yyrE895SVf$`*RkNm*}Nr3Ca8Aj5AU!YJl}51(tFl@~I8g(rs}3o~k3{QGjne!I9ZoVvEa%a>jV6k3-DnhaF9|Aw~kRNy3y#4I5GIJjBs7BuEUJ6f9GGqN#T#oP>tz$Um-8!XPr?(Z72+g@)-!IjZ=hfL9GypJZp4;?XhMx%0F#WHF<L3b@t;+~!~tx~Exg_>FAei{9Fz5+;Z=F<|AZ+N1LdO5Sb~m=kDvU*doQ=|6@(X}OOaDi5gbMuUEdWOs6Vc7#7BmSS#j4Ltd+@wPvUxM;$pwU}|YkYD@I_#ID(=^8$gz`+AKg@-RNeTWj~%N?h6)5&<lN1pLa=IKw|Jj6CCCnKPN=u^NBB$)C{B{u-qnU~nY?oI{x;gcdfi+0)O1fvHy1dIhZp#5Nj!vr>UE6O>M<8t2iO9h?Dx`Rco`XOKuLGFlq1P?jrm**L5Q7IAtH3EU3K#Jum!?(vZQ|}P1Ib%Z#(@-lg^mFxE>bB_zC$!};DH!XG$dT97hAAje-xWUwHtB>FN{=9fdXi^#WFPu0PSEA6B_ue4o;d~={@}WgiDTqv#=%AQ4iGqNDz)>2z5~o^?IB68j1gfSs4T0JQ-6EtXvYYjeNOqseVx`Ha;}jXWES$CN%e-2h@Li4<2h)VJB>n&rPyo6EWrbRe9ORU*p+6<J<`$C@D5>W5U+d#of}Po$py}^m5oGZ!gHsyd1<M3dVIhHbP^&&Od^OVrnm=OnB5*R^D>OclcX<n1($&bo^dVL8vT|e<<DXK<J%ucbqaicd?q`yG~7Y<3_sjxlp+z7g`B*MM(UZK&!o39Fq%#R_efz_a@3{A+DzwUW_>cOJ%>nuP<qV|vFx@CMd!@YpKU@*6-&X=jwDs@WEq5#sG5)H%+^q1G%x;M8mgf4p*f63l#PkvQWfzO%Q-C#c@TSpY=~w9Zdva%E@>?ddk|GT2x2$uS~H?0Ryqg6+-30tn`yZph(5KBbADX^<@^x&+Kq$0@|*$aU9W(GCGpbO-ic{gghB)b=jQR#C=Wx7y9vNBqj(a0PWphO3z&db`)fS+@{Q0l50K*`bve13V^IV5ASFmaS*#aLx`J2Xh-DNWJ%%F{mBE8PSN{Mk3A23uWg9PdVdbBK<6SAomWCQAHWoaFd^pt@77~zP5tS)k_3^@zW0qUw!_o;{GEi+U{6p(5_8VEq#C8*y6=$aNInzB9`B|ekO!5;L7BJYo+eoKDr;YJDNF!ta5vmq~k&REgTp?)3<TM{&(}cgEQ)Nv@d3~9}#!SDw65em{gCYNr;;9`&pL@Zf0mlmbW<VP69-psdt3B`g?%IJ@;ANJnsy;)=x*^I?i&+c6D&Cv4Ic6%ib}}+JT7|dQ$>+71^!Q|2)sbuHIwm*+MlQBH-AB8r?WqY*T_<UyQ*kK5mxi-QqN<6q7CCO)jQY@R%nj2}4_OV$CD8ykU>s8l*ULQW%E_GZUWNQKScJaZlX|Rk8dl-S4vBQ#OafT@S!Ow<SBo(>f#C>=1TfapdA=F#4J*9Sxs$NFp$KAyIaLsW<LgPL0E}+wVu8_fGJ2pG08-*KbCN`e9y_jd!%l~$-F%EVk<?{S+bGPS-Dm9VMjSyr!e!{y05R_eMs}1TS5RlumyBo9c!a^g$4;VG7A$_KEr)*kk@c^@luHBNIwQ=6`iIqX(R~B{b@Q-2<Y2~0bh}k4)pIiETxOZ?SRz(qTgdtXUF(;i|B2q2$me*nJ!?r)0BOfp*X$B$*p*h#$Hd%YNLtQQvxEu9dzOI`@N4Y+=<W#ibA5&=1wj|ZbV~ayfT2YXP!l)15)t;tz_(ColD6;|tQj#bE9yvdm{lJ+dfxx~*W+V-PSuG^JuORB!Q#~05hXX<EHSx1n{$7r`^Xo)2Z(y_w9UkIRAO-NvW}h2kvv}=wxjx2QK0l422)XJzIiX5eE;?_Q%+m7L<!Bu4W7TK!*5w<nWj6z7A*_4OLeMgz(BhQlXvb3f@%2+Qsf0W>yidr`yn+R3x@YQNGl`Kep{R~$<lUjTIi+FAtE=VCETE7ciIH@^fV`1qUaQ4fuflLqmL--q_kbrXBSpv0)l_w`G9CZ%yd|rcD^qA+`}~udFhW}<i~4$no?k*!3??ZcWb3VghC9raU+g-7d^=eL$2E=7l-)|d~x|jXKhG^8&CDpG`t(9Y2Qys=pHrzLQnOs)oDFj`^Ei-;h&N%#HFyc8dJEolWdj*1hVAie_YmMrB=ClSy5d`vi`L;ac*b3Wpx=Qvo<sLl~)C2n;{Dc=<=cEey}S(>4Np3AAJFQoNiMb2eqopikECM_sekqBGGMJ_>??f;l}|f=M)<TnA<R-cCLsNj4`^x>^$LQz0I}qxt=$nT6f*foS*9uXW4`Orl}O!_Y!bw&LelV`hR@;?WaG!nIC?<1N-)P|9^Y`_1o|GsZ?U5!`S+d(x+iv$Be5%J!+X>HvuZ_-+|`a!WOhE`)}NX(#hnkG0%UHDu1rTpvM#cclM^rwF3LNxH*#6acx(IRjOG^&skx-9sk|yo)c!fFS&Jqt*>W)IOGO4U;STS{x$GZNW}4osrYfaucNWQz^)MSRPZGKTP#m%wYPpcHM?ZwXL9UmZt)Q(ir#!A(w~2S`TnQJ5=8i~Zg_RFk7L>T8vZkYIg^bV>k#)8J=BgDk7qnY2<VK2#m1?RoBaJ>e)|2F-+ubB)!#nClFz->;n$yj|M^_)I;xDbIe&!t^!E(!_fd=4-B2BHtYKH!<zsPdh9r)z#<OR*SN4#xhK~LJ{OgxrfBxS;KlzV;Iie%bhS*;_Pi=GUqdCmyNQ-LyKJA$O#B0UL%Oz{}#WFwM_dg`QJUzN&`)RHG{w=$v&3Aw;iHZ)4dXPXD9v;6S^LwGs8tV?5sV{$y9zHP|XV>24@4UR|c!$q>({R7rb)}jG6c7Q=pfk#upTi|VrW2_Z5T<Ju-0kO3miS7blSQNnARUSMarAfXJz3VCl?wWCVhrWDaM9x_)n@aQue0oGBSt&ORREocZJnP5#!Ghm>RX(rd!5oGg1QzQ)w;F&xJCdw=Pe=)EYWW;uML3w$F<0PAkXJ}y!0QKlQne2XY^CV<67n74<8V8Y}$8HUv|AF^$4%LxCfseP3t%2J;GyDyPnX6Ktr1)X@}-;eT^-{u*UF4lgYM8-?R4F_x@b3Eo|(eXX<9tz{^DufGQ&DJZhVc9^yn}=tzPLK<82xnSxBiR(ufACwGX)SgMT4F)l{qs8Ham=7emE+Th=OHr3T2TOBdk-<N5Xw=56wb@L!wqQ3-OEymsz$!d+;o<A7uTO69{uYAKGOQbe5M_Gb)uuaLZ!Kz=mtkvM-rzcqgUklhA_c{N%D@eo1{boc-H13gb6F@Z(!RM2nPUo9rY52*_NG-<M|L5P{-~TS85|3#|wFt`tg24ahlHWd@xQH!uTux-|ddL^2ZliRFO>}-vjCW_lO*-Z<HDsOC9kNMRZ~#*@+gghAKGso{>622gcQTs$I`W1y?tx50?Gcy{eGp3jA%(P4LnmnC#m77=91Q{c`%nbc+nt6eVPQ*+K?ef<XHr|#Q^M0Y^t37Ag+-v%U<<tWd>TW<c9I9!|3~oQQ*gu>S29=yL`@RvKAq>O!8n1UjjXOsOavR*F^;Mh)y0k`ZAVzTU}|s{Po*iR*ScWSxaPa;)LuFJ&icPF1H<3?GFts`ng+;!7U~fT{S!9fD9Sj!;3b~qge`Mh90_HEc7K@zG3m|Im&R3^Sk!CPqI-EiJBgk{7#P!}v(F>))Iz^`*X5Ygu6KMeGaUPyq*gO!$bA?gAt*w$?LpwfXEis()fvJK1|8=ro)hjic8BIfWs;UsRrXsyAwA8Dnq$$DOSHO6u{KwSWL`6UKU6slVoh7)8Sd$F4s44u3@w#$$bn`YS(Fd=Jf?ZiE1hUs78z%@jA;%&34HybN#5bUqPs=?>$h+Jd=HZ;=aUz5pQH)kl%!YHk#bIk#d~4uIj{NOF)tz_>c(Lu)wq?Gj!AL7Hsc3_T{5^xY^5;DB++HtJXv6rn~EpoTvO;@iE25Rm>pZi9{vFwUhpvOPX%*8zd-+pjcHWG!SUxNuaT>Uce9Ryhhv8Biyys3zrZdmhx)S>7|-Xs3N*j8{Coe$o9zxu@gHjFXLJ1L`ml*DfcD{-=_1Q!1Rdl)d<(tYc0wG;Nsr$$s7OiR+XIJzPs{q-=9VA3&OAj9|C^RkEn-@j3+#gTcOn2$HD8F;&nZM%g7YFs$}^7-<VP@v=hT2J1DSYZB;E*Bb~XjpFeEYH2a}eN1HA{<msHyB6Y=l3r=!?5017In*<F@Ic}>wKV{%|ZYEi1Hy@hq61}JJ%<rD!y5^JB2ORTYY1<pS?vvb4NNOAriyn=gcsR<3n!^O(9#VD%I_V&cyt@`_zrH2kHMC~>2*t8}s(efAt5PqVV<?akC)kpgq8!<AqP{mWEJ=1BLz~9p^*KO3>klGOI?1t6kFv$jd1K;<F8XTHU*`i!TO1*@_wUB$wH5`54r2%8ItYS{#n_MVJP~`oaJdrL%X0BOAGa2R=g#MCg+n#J0z0nnY0jb~AVEAxqM`<Dj0!Bn*%X+MPC~s&V7~yh>HW6;7d+g?+mzmObeISp>q^OwzK1QSyLfdt;qauJ!3IRU`Ge^rK@1-U<7(Y<XK9<OQ2g5_uyTS8Hwc6x?*S>cL;8M5@ftKuuv6VC#Fb|8Y4r|jI<b9V6JvhH>6tV(m*PaABRFI?flJ4`M`+L#h1mU!T(-EGwd5Ey+VNFfGK_OoUIe&-0HjmS@FY)r)2Y4PMWf-3lJ0co&n<D2#V99an#~fDq?FP>fL$*do+{u5<4IK#qT!V})qu&dkscf3+81GIKLvxBwPG`lYI#gmPblUJK0lP*{k998ZxfN?|<HO6-&-0YP%aDW)>!zW3XM1F)DWMkxQo>J?FEdEpF~Hi9DdOrq>Y62wqAnRm>9=_#!!TLiYdP1BUN!ZrZmsQkUS#VN;X0mw5a$RoOEu6CP?k{T!k_2zB#$rQ`jmLY++dYru~mY^5tMBdF0ungHHXSipNVfMjYqUstox=|^J7?ZPiy!m{?_p<n^RCc8trE}B@de9V=h&e0E0}&Opg)tvZSh;bAzH`f`uek5ZQI1j$o}-$%)Z{6G-_pqU>wFBKg3M?JszPFwsP&9(VUq`!YcWN&N!5__aI(^>xR~k~`=}mB+TOvOHvjRfQ^P_?HBofn#{BT<_;BJ>~{C?T%?W!URrpPr+{QuWG1HK%w<sK>tmK2De4gSgW7S$QzdM7y3cVsOBc^({EdbeaNzszS~7jfa@CIP3S=Hx|Ae0qlyI5Z~wx?sUIH8W|7ox>3Qix(ec)K)(66;?<a`t&29ifQseQv3oB)gsW6rrJbj?#ZqmW5HkD!am>agWJkw{d`YA*?!}d8Ipq!2cZ~C2=O^&m=<b{0DON%sAebQDX?Lq=E_mHn#T??luPiCI4c$|sob<V57u;QV^SiMB`_J<V^qQbRw%8P<DAEg}069mC@{~BTsNi-E+Z(7L{=_0N^VFShr8ZGoL*$+Q>1pPi<nrMwOGkOE*S>e83Knd39y&~Jtp#~2&>pCP*uVB|HnW${wD`3Cjq4^Xp{fY!!%R5Fvs!0{sF!#p4=~XoBZ;5iT7oD@L0@i&O_mowH?>q|4DWpblA{zJ1UKs`aqX97NV-E&z9_+9m$uX1rm}&8fL(eoVL8N9SCjs_|*8|)eFz~=BgMg@LiTZ16``VGp>QvmMD(UaCJbm%{hvtS6E4th;Q^dB8Qg9o#_^T2+pV}4A{>J!<<_3KSB+UH064Pt)vUu!wS_KKRZ--x6hEbK>({QN_2SxuvMvKwxW#hsEQS)QAvywSPM`od{5^)P0@^Yn`ycvXRJ<3pIEEoqeaN14T`sZA_(jfEfQN$KPO*&fvY2?8Mug`vtRVJ4p*B@vRW^&M1yMXlFaBjM^_&CLJM%m2QdCnzfeM6)IEQ@9f+a}$rXs5^NY$JNPm<(=l=RHQLYTyhK9r3uA?Y3~>uL2zRF~mvDrZe^w#}@ioyVffK0~2z{2@lqmf~mV66+ne1hxI%JAwe{BJsCByWF7su1T6O2r_@U8)b=Dpe_IIHcnoyabi<G6;kA}Yi0tTDp-DN`OTdU=j<Jn>n-KL(d1+m-bg$5Cm4<GOAzkU|1<?v!adKl+$7Cwe&>7DbaHhPM+ok}dHm_rpJIwL7XCJyI8ucV_c1cGJ%QasHbwpBS9%U}oEN5v5V{*h2{TyOB2R%JUq4~vr)f{C>056Hf;UNwhv7V~@+#}X7_O}K($Jnk#$rA@L(Ru4Wl74(XeS4edMcz1y#I=@*wq`O2`!TRBa#o_~j6&zb60ln)rP5Q!*!M)%mZxM~ch#%-%54}d+f>S^i)VarxK%>m34{xsy$+?JpbLS!B6A+|)LB!jJnX3GtWgpA7foWnj8eKGvf+$4N|7smG|S3lCKdj-6tcF2uwSYn7%r~^tYpEpmtjc)Z5;x8a->-1<L<+_uRy*)akoEP`W^`N{UACFX+~pM!~F>DJ*94Ad9a1D{xrs+hnsM&wnHb_q=aF4NL2z$%Si`#2PFFFW$pc&UK2fLUND6MU0CCFnM>iCX$2!RwKoh6Ds_^(8AKok$`!jcWt$v9fDVD#xYSwhe8|y+`Xv*_)<>&fZ(effm`V<=^_bRqJdH{kA90|{uCLO^ef5EBFC%Rrj~jirr^n8rtA6vQ#$%@cMEqUXT#vdVs~aMjc`}T3etdS=7)U-?{9-1UlD#rMl>k6zD!=Zc6dJ=e?F`o9+JOQrca-ps$>hPvqF$yb|H=i*8PUDsBVM2IW5`oqQ<+BS10i2RT%C(7mMF3i66*<{ie!!e(kp@QD$63PL3?jj*CR{-b1a-#a&eMZr;r%y!jq&T>Y9R4qp<E^N<z3SyABz)E@JB+&J^@pZ}VBBlrfNEY29BP>CNa(SPAv<Be!$pC3bCCbAYIsjKXTKD6`SVIn6m4zsfn;!enAl9auQNf|2LY-n2>mCi7`Fh|B10#RGyVWpipjp7~<+1r(q;*lqB{yY+^Wz<7f`y|T@!wwL#ugs}{zWOCsz;HpJA&8P|v6UJew)<T@!0aoRqcz6dcPn<-8hYglS;~p1keO%?X^l2KIXxa6BaH>-el*zNGi`<uO&u5^s-WBvySbjYPVZOSHd&E@|V6j1U(dR;j?uv@{FZ<Ld(-tNN$y&p7VGk4aeG;>d&=usyoV}nDHzNNRakKW?0W-#2H!jdx$!RK*L2x4H<F+pe24ATP9JMZlM2!rf1kKeklU3%hg~Tk8%6N{q8rU@r+Kw-N$mR)z$F)+E$Xu;v{)3{%9_!iJ`hy3^W9)x!%L{37OKjC)2dY5jY!d}Zcm#`z{RUHF+_tzn1LrzFE80l$X$g)Oy##uUywC(~O;NWv%{H%#No&{y!YM#F>|Mw<XIlZT?@AMKuEKm5*`p+FdW5DU!kTzV@;c<&_o&n?w*xxCW*7z5Vef7V!11B3=u8_EX@XP>whr)4Z5lGH)6V#TZDk{Ak>h?qmNc#OiL5Q9vwG$-r^yQmG~`OaJCAm9_FS7fhLmuLt_m73FnEn7%+ZW|=_vKv6%OzisSJ3?!coUuwSgswAL3V(!MM5*j#<7pB-+ql@WI|vtT}buGG%|9Wa6zOz#Y@|gM=K$Z64F83Z^~T49{X7eC*!;sVAf#oG0HJPE#jm5bqL;;I(!wOzW(3P{~x5Za^gHk_{C){By@czBoBj&k3!Oh9y!7fkeMi<N$w30y|xLmg}@V*Q#P4wJ#`2)uxS!lHm*J7{3rj!4P7}<hH<u&~lOsOt(4DIz1bw=5xESL}ZB4?R*S*PH^t`m9#&|uX8x<F~r(!bHZnWs)wZL&%E~LI<JX(mWzz=^YR=Z6k?Q%f#Kbc#-`Q`De@=UbxoGY;j21E8kKWcrGqu_+Bd6HZ?Kk3g(jxelo|SX!dUE{Ii0q!dnV|XZFJ2|UK1P@H|?wD)N4ryBx<cO5>bMjA2>!CN{c{0I5buv(R<9Gkjj@y4sltY)U13LSQ2|ut%OjZmQ_dDP%K2a6Q`T*d7SQ3Q}$d_9+Q9qw89cYPbzRa)ADstX?OsGZigNf!FxDjaY}0J;D|Y<H0ozO1`zb~DEC(!>XfG!y7-v&<plA^z=}$s&U*fQ?i|*x8qWH@|5fJ6;EhYf)?Fe>@~a)dvC~vHjSrbTyhM_I{~=KPrNxb0&(<-SO(n^TUQ^6ep6Db{)G`$M!XRB(_Y9O4z71fnum@r@(jr)E;&W)aJOZxM$nHnG6|6>wGzUt5HvJ)RU+yDC{(!w)=T9X{UMWCC6C=K*^lj@RvyU-=P_U&uN19fv;q;XEnazDd#N6MbD6o%gtAn;hI_)H@1<698f$~k%|8O66_|QJcpqWyQeVbsMMae)rFnEF4UKUwCJfLUAf%Zp^r9fh@Qp?|Sa0=H1Z=1bCHYX*LpeC5-g1y^hO3|P)Pujm#q@oA?v)=v^qS~ksfJ`jMbP=B@#UBXvx(<Ph#~;y5ot{!6g@PCN0gtlP%@E$>A}0n8^7Z#m`kDgMoj3ISFFwNJ^2XEvXKr|n*us?FemU#FMRd`>vWEYQnqO_CQKWeM!CU)^BHt=kPlFD$*-5~B)=8ZvDmQlK3K-?7rZQ5BSi`dC$9vFe_2C!J0+s<+^e$QnVdAH~+6H-o7~<*lbokwvS}H7TakNj~Hp*TW#T_IY<)GnfYffOaQ^GNN$ll_k6+ndIMHUE4P@QAzjFzI3A<ei$m!31<rF+WiriV|U1^K#9?f<o@c>9H<L2!(C3no$%xd{oJ$qBg07vUcl3)}D{=BfW_UrNSJ%cb-437a59+19Y*BQ-#W3IT*6x=tH3uezDpbo3FGbxN2-roZVL^}Vx7^e&{-MG4LH62DpEuq29Ak=>#)Cf?&K>#j#(s#^PQC;I2-{^Q$&F>QppPAhZ#SXlFhdgb!93RSPt`_5)MWun2W#L=eq?!EEi9^1ZSlpO@Hls58u{?6c*X*xI^;`&Zhz?}AmsVD2+hkki3Ef^8~i$3Fq=Lyds^=S5*F*mdUHfqoS=TyxYcTSPA0M%XgaxhTqYOQ*B$y}@@CuQOrx@K$*ec*W+24B|mC*$3;Wux7vtbC)D_&rbAD{9*W1s!6`zySf@ifkJoNU!_;EPUoQUq$*66OS^M;VI%ML7Y{~)Gfo96y}=z<Uqh&2~%}UfrFIDlxg}ot3dN{8739s9OSf!m*PupOg%D*V>G1*&krFiwra+c)^VprGZQ_*xHOIKfI5>fx+j<li2k>lL0pDhYl35s8?l-k*%ru~;#(URs{;>z8J1qn2T%sU=KHIYBo7nypW0<uRl9)Ol+M|vZxh=>aQZeGVn`B(VS^jMb@l0lp6BUqtM)`jJB0B%ck6J~62%5Bl}c&xqnk7ieFAW@Y9a8#bYOhgko0V>U>V20fQ)t(v8EBVHHwXS(j|Mybz|C&G-?t_{A;xIb7tw8@Ou*l#T-&W4@2f|rQWTv=sTB8e4AXz<Avja1qhu!-;Jlzv6oQt0+w6Gno!OP3TP3{H^_K3;Gfjw?9+Yb4v(oV>2^gH$5P?Rho7^zK;FhXA58i{Ct8tc@`D*8Fjp|gZguxLn&YM?0AkdZq(n+dzG6<5`5gKFWN`yyx2Tzg+M`O9)KgG7NQ#ze=%`;HsfVnkv`}4259wu0;SNpXlj%c9<>2(?*y&2L2hQe!dCp$)f0-sRW%w{Sl|vG}TUt7h{dj9()O_JG&HwfJ!s|=ih!MBYIX_=E$C57HUoaKcW7t*9XGSzb62V8|g0@j|c6oW`FiO8oi;Rx@P?B#S?~1q?TsE;^@op10edKZh8UUTpn<bIpz|$BKKQP>0igE#rwzd3XFoPyCNAwUpTJ&KdIi%Pzn6XpM#e)1%0t%{gMwtyYw{&07E}HQkhK){u2}Q6!#&INpHqUy`26ie_6q+1H8S<vN^!3Xu2)+QeU6$kmPMZz;xQehJcV2M$OT$l;h4?T^$F63Tk8B^{=do&I>oW?N7yY22*TEptIvh{w=4kPANXf+aDSGTg;!dS|@EGsb$65^nV7)0*m)oY)FYVfwA)$QE)KDNCk_MM7EE9?r4tdGaXt^`p*A&>EF}(VTZTp;;N#=N^%O`LR1-%CC_~qBU)I?XG9_U5?&iUwFc+yhBD1bd(3_GaQcfef{0e7dlFRLC*zvinBL2%PP24(%0xW7_2=g}E*^xxCb%`kur{`H&p8}j|z$4n>63%X=@LBEO?bZL4<r2si5^<NU=0Yb1g;A}PK(X@LqIS6^UAWB=8cg8^EMG;6eFU!`YwZ}~t*OlmWi&<V-R86C?^OG*QPaBTVNu1HsR%L<AkVpH;)-*caeOpkC?|$$1@JewKNXr-TBYAcj9AL=6Jj6XPm`OLfitSyjUj@_jceIs7z}PSDKMem=7X{F`nlQ@<j=&dS^=#1fhrt1f!W|}pLGqO!8SeD^jWv_qo=MKy1qA7}b*R0p`8X32P%Z=%GGUEi<1JRrX}V1@gcPwTg7Msb5=@<U0qJx_$)CcfM8)dQU2IT8$1u<oDFQOiZ`rKm1^xfybLk<ke73hGsniT=D>7x`BDNwlQ?G01#B3IhUElY|L;uIO-+ubzoB83#gTHT=y65|^-+nhg@7vPWX5MHruHQ5^_E_^JN?=$#FEg;MOLLCGzCj4J7#m#jJn)qgHlbZxxC_s(_@=Uq*fq0Xkk{V(LbPkBAP;W8xyXP1`Str>9!sDjBviv+5u}Y}%P=mozUL1KhkpCihB4O~v#{EjG*gce;$OafNOec0NIup{6~FuOv2Ou!x-F{_GaC%|+K4^YFn0K#fBo|7&;R@9C;#y;^Fr8x-EW!wwbRZuWplAUJ=UTcfzO+6KM^yKNu7!2p1JwIvElv&V?AyDvHhBSk6qK|JK#=51Wf?f%UJl&yyL?ofFr)+<9ApZyZkmiYdUd+=!`sUnogK8HteN#8F^c*&@e2Gl6S?9OX*45MqaT-&v&hfjtzk&yaDJSNqzII10DTcdoGtJ6WlNxKo{!x+$W`*jB)RN;#;~$pF_PJ<Qmbg$<0^~uz*X{|I_ck{PxqYhk3l8?sZDzyY>1f<ukJTxJF%;&eKCg2cq9#_+x-X8`r3fG7RsY?7ws7WDT9?OVQAGT&tYa;sb(yjMM`LmtD`b*`)U24SYH<t(%y40FP1adWx8K`T9e17>>q<FHqEap(sI1R^VCt?0bK%SHlcQ>7%e;>-4`^>}FoO?L2CmUP^=QZwy?4;@-}sjC^6zdeS%t9Qx?Jxm)A{^CjUDsS&O6*bsb4(`Vn}hRNTC{RxE~<bp}H5M_b(@%31P7!)(^Qzq47*R_06fqdMB{!FZc=?ks0Iyfl<==lZDEL<iQcVTjxY9ibtgkRtYR8quVT(<q|52>1Q$q}~6)5*=`%w!K{<5B<fZ}0Da|9nFBMOEd{K&LtPP*(bJCVtFe?PHX+)gBe9K>ih+vh9iDD@e+O%}ehLCd*fHm-&z%+rf}WjlEp-sHa=>eK&V%$d*17;RvLgCBo9errPWdOhYeN4WOi@WIRs!c!zl!rhJhZq!TH5gL6&<(Ncd|=U~`0<^k;j%&%rNhsSVA<hX+c0_QZe$-s75pWyx^kc_FnvNf6twXRfOmt8IYgoe=DaIvhB3nYx4F75m=4YQKKSXxjP%q<CN(nrCdA7_G|;Y}^p@fWnq!V+BbF}gh#{V+lMi~}1;!D}!TpeUwh?9S~E5j>PCfOdT-_(Z#k4c>;*OpqEnxIGw2WltXw0lQXcrkI__3sBiUTZo_y{hKSq61K-sXSF8xLBu`7z}t=(AUUOU_cRtgeQ52`W52(-bQK>JqyVE40@U+BM0qC*2mvGZzW|GAM|ccnd0o|KdTqL4YN%vDC4=b722~(N)M!%}_MvQ}Rt<eIS;`U{p`hEQa1SQimAMJipc?1%Fv;~V&&Tt96^n^}8ewuDc2p`uuR>I((UCp`iw@6D*yzfXq@x<1AFn^P&~M&#Ip(zYw8GoRm?bJ$%zGQfJob#j`r^R5X&YR?htFz59_O+THyB9Bt33jOs`I&{a{}l=6ORe++jF(&4uW}hhbUNvvIbrq!g=lMnFdh?YyxSGXSk=!Ij}7)NC*yp<n>WmSjSJ9_vcD6%t>MlNw-fgql!rRP*iZ@e{&eBF%;#m-@g6x{Q>xgU6Aw9E0a2xWL}*5P*q3V`dzf}jX9m_GXFc~MVPtWyiZAW_;7)lo=#<v66F}|lEGJJI5!iWqNIo57^R%z;VMP66OzRUP?GsJwu*iHqXA)Y$hyr>1#>{ZK>r9V%t{ch<IhcA$4?FKW*r3|#|+)qPI`-efn8Y6$jMe<JRk6yFN8bh@n*Y2Y}1Dt{Ml;oxjt-Si$_N})kUt12c5TycnffFte35qVb9~Y402Wr2n|_>flteN+~$@ayWX!dG%cfw-LbeqkU3&I5uj3=FGSGK6vEcQd3h%FMbtd4310#{NMIx!bm-iZ1Y4?%q(iPa%LP$(ryhFFKX>eB*F6n0WIk5pG`owQtfW2R3|_(V+8^&}6Ess8(lM<qfJ4)I6-ljqJ}%*Prli^FnVlQ9Mxcj#_zLc=WrZ{pZB2c{$KysU)7^Ww>hGgSuor<+{8~`QrZtI)1|c5xM4@DRv@>=yiMU@|zY2{QnOewGCz2{fATvhun7CZGQEx+PL#(qK!j)z92w(=?M2@;C+w{ERIz(l#JLi++sJ@G(7;^K9?<jC-77e70ndYG&aw<=x^fW-ATfzU;-w&Z-Z;Ax7<COLKMTqE05sUs%n$ZDp7@kwFgwfz5nch}ZAMB7Pg`4RfySV|GeWaDOfV;0@{PTz?X9l&;Z~^Q<WXovvCu6qeAuJ$*vLOi(NtbDSV&?`?#*l_Ka%FM4&uIn*p?d{7mW2(sr(<~@qDGyt;-cRdKeQ%g_tTTU4R@TLwb#pQ&Gg*Bnrwsxf;~!&2cB%0UscN+qZ#ok+jGF7$cQ>L)k1q!8m1e|aK+>b8FyFM1CdQ#9OK<-vS5~gw`$sz`<a|p+c($^T8OrKqSSzOIPUSbB)JgCVzr}9peRU?&l(G9F47*^29{*;J(xLB6|&U(io843DAs7%1HYRivu4SoI8UmY2?%+3@3hY^q`ZxD?P#HW4fQkgZstX{K2fdz`R8wrfRwDW1i~i?&n6dZ4`0HSsT(og&10%tj<T4cGc-9=0<pQeMJ3YF`AmkQGP$LOVzmxgz+o<P5C6g^D%0^Jq3n|e^3J^ZC&%hBm)a$FV4G<G<s_hZNL9S%23etK9iV=yz^)6qWoxY(QvFC(iFMM2k0#P=(5qDb@-`R)yS!ZUt<ipp7FVS2u}iH$2Y7v%q8wO*4Z#~<uTd?}KvLZ`Ww|8uqssGNb-5f_Q6mO8c@AgY8vFA(DUYAU%>|P-Wd@;W3<VhD{wh+7zW%r#%<(}aJ-0v(`^aRI!iLfKg>Kg}rWp*Z`_5rRg4FTtwcoQu<^>R$AJggpkh;CXx1bWrXwHs*hQMIWBB_0i^U??8f<7)AD$f!L*(ZCC8;pwebwD=A*K1>burQVyyuG06>#IOgpl-|rFgFZ}d9vPK0YwP3g*{w69y&c6PUSi;n;h14skHdGix%vr`e>~T(1o#Pj=Dr*7sIKgkeQ2>>Uo{>R4J@S-vWO>!6+;aP?gh<QJ0)w&vJ+wSptEo3$bW}rU{VpdZQ!JGj{vXtzB88G>YB>cq+(WkFSJF^K9@o$eu7Q(O-uIiVN&`CbNoLD6SeP^?XIPY^w>BA@l_3d(IPO{F`3+!Twh00i_+n`=0G7n*!fN6h~78gz(@tu8h4P3Rc6F-wnX&VDRQ~3)@E=qqvWmj+{6sOZSmSDm7j-yzA6Pj8-!6S0G#^S`m^284LHi8q&1r{9|%7GF{5jZuA2lF{vdXr|I?boc_)pvDA>H1j2ox9LhzJmHf^**W3OqZ1WDsrwpS?2BsnH7<`ZZg^Uc@L!^EU1n#q%mGlxi8Vl`+kDGUpTPIbH%^=*1RfZzNlX$tE1`N6(%=t29h$I_jnnd`6r^m=lhhvD#AoszOTW!OdR9^CW-Cbf*FnCT<na_DW?ID&S5-5P(&n(wstF0y%r%1@gNlzo=wwOF$apyfo2~FSz5$fN#>E^a@;IDcFR%M*joGT-Ga7>?{+i7!UU|>R~G2y$}`XqH!qpF;M#$L}uu*kHEypF}n>#Q#(MqiXM$^iBhPwh#DuBQ;HaPR*rVu#<%BQ_|L5Yy1JLX$ZlICHO$-GpiE+k^-Z?Ir)jda}X@R2pU|2EY7}7>_vw3Z5uJPtW|2DdaL|lt93D@?LHm{7U^O$0&E032x6mbWH?QHTG@oDV7jtmq8r?Qkg?K<P7D^<y#@P#;VEr{DVhj^BDB>9NXU)`&Dz4FaQJ!R(u(eWr$Tb<>!1hVyG0_nPw{ukCw!6!eo?*RyL;y;km_Qu#3EL6dr0V6YU{mxawnIdm`t@vlXt(=hfC^d_7CVloDqDf|OZU%%pgtr$Owc;hPEpPa;hg^LAMWn>_5O;HR<j`G-{^yL(rZEflZ46uCM?6Oc@kQz3gwK_*Lx=cEdZ;qp58G!~#TWZEGacnp2*E|X}ze=MEQDa+juBEU*`DSJ<y(OhMG<r%59O`r>jV26yWNlQj@3!(~FR8jF?YEi}8Wbpl~Qxn}do`;X3FIaMOdH+Ho8aTBnnA#+xyv3R~N>{oCJsY2++PT03TIwt#!gG{*ev+OsTPfLyW8l4vhJjvf^xd9*97cFrDtBD}6G2deXbyW-9aY;9bjULj;X5}&^ekBFVkWpH@D=t^7O<ic8Xk72xPe52JhnE+4ivyHqpV|0J`6@S_4RHrbQ-JkYf(<l&s!E*5cn}C=|TTwQ%Eo)%mrF<zMYq_lsI<64NyTPP3E`}*>-BlAwG<qq71(Xu{Vz|(B=_UmNm*90s8pX<-pGm^7L5qJ*%YvlC-jx_%UVZQc*S+g#uo7wm~`u@4J_V7ZbI%Cp~tGtK$@(@A^g?MYI=w{Hhmz%V-y&*KXmJV#Y*4dod>Un<>X&d8YLQIc=Mh#rEtk%akHN-$7e~XvfW*mQGaWY0b7-6;$!w!!X%L`AytHzO@xwlv#@Ec`$7k7M(0i(H-E@r?zk%0)TS{edHo5M7D{dY<oT_mi3jO*TGVL!pnUdeI#zJw1-k29xz;(vv{J{xHQOC3RM#{L-2LrEcI@rvM&irI;qkTAy<<eY+%Sy6ECOkkE;Ah#zk-=h?j6b*CCVG-Or(5L{Ui52M%k{Uvjp?{$P;f^ISm2MdU)5xx~7ftU5NP4)e2OJG5AzXoBWHYOY0X0I>iYm*{pbCUSbQTwe_Vu)J%QV*rJ$PZk&X!#Q1rc`fpLOL`AU2WwOu^h|vna;*qd3d|-)pxIB<kR5-l4tqBe61$SR;vQ|XpvfQ)&JL@swLziUd=_Ksvzf#s!XWN#U<sm1pNHB~DXM2KbDBJFkM&-V%3QdU_iZbk0^K49HO(Yx9LdK(myW^_r^2Njyux)1+h^;T%bK!8*FysyiqUMw5SZM1Lxl}`NOog$5>Fc~n%8m5B-C*Bkz-*&B2s5=S96th8da$Z43d@s?#yS$$1Z|3tlX|mQ)jC@2f0VcCOdP}=;ItqGL<S<Q)pk;LyGnolMYyVmYTjcYPT8u4Cqt}*|`0y!lN(OH=EW--v|+aL&Co(K7qd^75C3l_A%t`Idt#^DlmUh_PoZD!KqrfpE0MJuwria!SopJf*=9@IOkdCP2rq5F7Q24<5htb<9UDQIl;Z#S3LY6zs|v8#}I3`i3uMv${8O1Hi&b;@Yh7*-K{|@dbNJSiuKW-2Vql785D>R?Xf03;80;4Bi&^=cpFNy4k`N}bt=!)kV7_gNW=C(nt}`#+INN<NPBeexKq^^4@Vxh5(<naqjuk=NruRhBsDlJ5iG$?sb>9s%l?OE`{n=}YY3hX8qOLGQ!_GP4BP~I?5g<tn2<-(u<}y(v6z3lk1`~Yhp|}r9EFs=aa(dYhuNI73FoPaNnD=PuzD9rw|bKJ+68iZduv&Bm<TQAhx>Picb;8!U68WpdV82e2;hN~xG}_J&81pb>!31X0LsG-y%GXgaHNBjgzeEEa7<~`??GJj?<c<OuXoic&-8JLJ?d*B%vw}}Th=M$vsSPsw{Vj8?XGf%I`7UP=I@eNAio*~!vf~(G<vb#I8g?damjL<p;LAQXLs!`YDr|g_a6c%0<HMw`#%2L+CcRQjaIbWm>M^MhxZC5Dff;EPB$)W-7~0M_{f3X!w#6O0i_+OU^Y$rLck#yJ!R1b2I~^O5c;H#*^TjD-N%fa9eV}OpGs7jDLYXZWl@*#K2e$7hzSD(o2tj#;8I2%aMARSdCq<En%t$O$hrs!7L}KxozuzfSjAQr%?m^rbkVo_1VVq~K^(}GR_)UUAMGeXqp@GlPK|cNNeyB(!_bmk8s0csJSC?dxo3$9U=9xGnqZQ$_sk}7MHa?>PWIaH-!odnbhR>#f+dMO=hPmP2;r8Lf?KA#V)9`vz)`I3S=Inp09c2>iR3SF2697%$(yA}rD~RQE~9M5GnCah!;5jS;;#AErV(MFj4~8o!pi3g-5=SIW27nQ?rDn7|Kgh~9v10J+)m3`K3XHjCS{f6bQ4$CME@$C|BJd-UF&mNQ3_W<7JUtl$&$|-JzVs!04c08`XkIW;6&jk&co?ebCW(ERKc>1fbP9~)873kZK0+dg@*$&H?vN9OXLK=gZM`n=@pX4s%wZ(`FIa{_da}tLqPuE%7)38z~ABX4crEKf_O{A#$n)R3aP!YY1UefZIm5+iU&)!Uc#5Dg$sbuP6-zsMdaA~bC{UIMLsQ%JKWA7K7w`7S{Do}JE`mHrU&hy&HlRZ?f<pKF8hTPq#q;RcyPDXM1o8L<#V=a@<sT^Nnl^x!2XzKp68zS;$?jKT)~Vs_w*!qw>3JdxdA$KA0Xb<#kZinl#{&MrsF=TdQZZ}F-byEXyrcqy|X;~E)<1CvBBiZR|N18GuG$1R797ka)<ZG%7WNYVnj{Ww|!B6e(pcMJ=oYrrs*_3$B%`86euk%-?mT$DYNf$G}9>)mS5F-HnolUjhETe+jk#)2d^t7ue=`1Gx@;s9}dexa)T^J3h|KEy${3od_tOW;1k>VfC7U@koq}$%~%`S@*j2Zfnyq`vY(sc8|7rIyX^d6q~+CGY3%^c_u5~5qAanm8Cyf&eO?^Ix3Xz`Qf0eLD#ZW~=uU2F6D8`q1l2`iw7>xY--?VFAULo4{w!|oHD9TvkK3@9;VFhOL5Wk#G%mxK)S{aFm_OhNg{j6A{^pY?RGFrqiki53;WA8W&q<J~l2p+ZUJKzmyz%okt8(wKY(&wB6qm>|iF)2}Y3NLdNIcUbkBN|pw6mHRT!vh0m}7n$eU=<68%T$$=|a}10dWtFhrbL<uVw?NYsBTCugINvFYX1^vJ9(gC~)8CIotI0VtWdX<0gZBNggrmI0iVxK55MJJl*Z_p2%E>_<85DK}mI5R7fkB=5NwC^ogL!%6-5K)4NvsP*yB0Y34unMP#(`lXZQmy{c@?34jE-ZcN|s*{G>T%RXn8ok@OM>W2U+nMrEcmanKWFPL`GcP^O^H%X7j3&#Ts5ISAKSY0iOCO3P=kIPsSqE|ubEaHR*S*?dhF=<BvuVp*ux1>ADSsY8n7axAk-h@`9h6^#J4|Agbk0w5tAp-LR^Lq}}Jx3GW^bA0Z29)GDIk{tm^`6gx?@tyt!p?5S#UNwuEkF~HpDokSQNKV+8(B+f(c)CA%1fET9h$}`(}$2-$LWx>(-ndoXga_gQO^IE<0PgF9|opU=At)CO9iqY*IiAN+?nS8`h?*%$ZQmOTQH!|^7%YCkqM5z;f~^^;SuvwoDnyj#JN<stZO83ySzM^IJ!wj2kE{{i;Rr>P%?BM?~1+}Tu3qNc(;?Qj_JGNz90-C$c?%H3oVl)>}hrP^qB9a@047G2N*E)ZUYi&c<igP9LID*<|2k(OmPN*d4P9Ol}C23(i{;T@u1pA&%`)8AJVwYW2f+wZNotcJE%q)WrFyk6SsTrQex;~kLpC`v^S51S2rO>l7gIPz0V4}<ta{Tjzev%e=2u>pO7FMg-i{}7Xts+M$q7ggoM@Zrr;YEzASEvF)4R7mdRqCJc_qo!Wn4Ii+&Q(<6~ai4*%Y7&g_`#eJ59$_6!Q21h1;dqn+;-K1RRw=|q6kgKpS@=ri7vDcX}gN+M|m1V&RH1i^ycRIl1?PG!)uyi^ho;%sTwBABX}ub4bus->YuWYWf|whgv@v~=Q@B+DdI(9;zaXy}6e6)+R`JdvAHa>52Y;-#vi@O^SA!NJlOS?cmbvR8zE-AQH%MwTsgO>~6o$(-olK_yY^oW74cjPIE-Ra&Ci?*jv-wDh`t`v(*CF}3x%PT%}jaiPthlj;0~8n;W_t*`qWnf7L1Fe;9Shhea;^7Whd>-7EG$4n<m-M(a~+rNsreQDbHrSw>=?zALSq-4Ml2)hPc*J}1;a(ZUqf+!80-WdbA1qxE6l^V7#t?_Q!I<H*xTS8}oX2ie)dVbQSB4Wd9I*HTVZB>3kLot>odsXRp_iaIi{`<WTl@pl=7D+~bWb{?;8)9CU&0M4Tb=mnJE3k$DE9UVsV)joexD&;R1RNs@+QNJ2J^|5eiq~iC7zUamKC8G~31(_@j+b7DAD_#TJQFa8)f|CJp&r_bOc@7~tq9H8>%wwMf)c*r`~G-G{`mIWPk($fKm7PQ@7tvk{Qm2=-_6heSVP5=ICAdSZyI;xSo2M#G`W9aZ;nMo>tFQWGE_r1$Lh~NzkUD9V+mB?8~}W;TQoM&kl4Y&S`!#oua22MMz>{{Ls`SLe-BNFJJuoQQhMkrU7Sm;Cl@J#>+>@hkL>6B^|(*p|K-o1?&te6_tWpc{PxrLKl0aa-~Ra?Y5|@5(9nC^6$z`8Nn`eSj&4I0>v_UlCRHi+_+Z9kMZRO>day^wkiyvHfByB$uRs6qU%nj%jE(1R<!-<8=lB2kSL4Jsz!rM}ifU~?O{)FVnD~zajotLe*iepxF&!iL+%-+|&MwpAV#}tg;SRUsQ&e_c{nW>q2?whMJpwhwu|_OmAbH57PtNSo!)FC?5x`fC4f8epqvl>bZk|pJB6?EJGIHvPu^~&gtIIo_h30Q*l)S-tT%wE4YZ=(1H@_p0{f)~KUvG50B&q{O8i4+;d|H?Fbrgku9zwQ3ORt7vxBJ)<$ogs(?O@i3Con$qmjM3m+5F|($LETyQyQ(WmsBZfm3>v$A}gcjyr_hwL(epOPc%s4F~2IOgZO};TO+m0p-ZubhzIb#vD}QrBw~sL<c#WRG@Fk6^ABD9u=5_B|3bY|wrtz8WW!c!$OhMGE*8+8KE|Y%Vz;@!iVh}kZ0IOO{Vxj4v>X}!)0Fc~&h^^#QV48lWT=LqrkNRK<nWV*qQ*(!C{0HZYTRTRU0#God3&O;b$s}y!%R5Yy{A(vTY`o>PTC0eEpEyE1F?^<suKG=0d^xo$}W0^0|)0N<Q@0*S%Sm{Rc|u7mk*6wBFiE}Pfc#3YB8_lKmYdr{&zVy)l{Kufx==IQGM^+iQ9)0*QAAXsBI48u6ySRxvsF8%1*2`+fqW|#~h|%(0MSe4+RdON6eoY)2NcuFx~OTma&^)%6+{!6r4LJ(~yv^Njzk{YOTa0Q$s&u<B`YY9vlsUoM=o4w}FhI69uX=cu0t&J{Y`L2AG=4Cql29Ve!^pT~=TkBZMRRtAwc^q?=+Th9k0@8bSw<GDqYtPX5KcTx?{=IEp$Bg-4SyKFRQ}V_-FSgXkHcAi*>wt(;?8{(Z?HCp|PZECSXv3&ld$cVb7|aLMV_qt*@4%1V>%V7JZ#a!M2`s(d$A`eC0&HBn|??6BiN(%w}4+-aK9Lj_I{MyuSPyv8_WRx*)q0umch9nB?{$drZb89&Cp_jKi1qaOQrB;=Z!Mn`cJ*2@E#+!m4uK73YT)|`0Q*+{Ct-E%8=g=d-*49v776(XjYmwb$+gCv+HGFX*NV8uDzn|bYPz5-$7-F`6hBD)pymKOB_hu_&b;wz>7pn48?e=bFnaj5P2D#O1EJLUO1WmL;yABx06{BO~eIxs)y;VY9m7Y=CPUqPh22G-){&^&(U87=d_V_t*@)(tp|K%J(l7xZ+$5G)-S?2>`zWmw%3O$UUl=@{jv0@t_%1_jl#K=M8TJGMFsp2jT|djr}oT!rE-`UQ46JH*gW`0x3QR)O{r#CyONAmAOdic#ETbKB?ou!$`mvDZ|?v(KnOQ5!F#!3S=J^>y7^ifad}pt(%oRUa{KMe!f)lvGQ9&SM!=92=6Ju!HB@WBvC>+A<%em(iV=mQk&^S$Kq>DupL1K(;hrh^4wIM8AP^FF^5`qv*-LS-ZOgJgtGTbAZ@0?$FD6kd4wktIZ?(&#2y?aDPJ_d6*;%@u<_XB+6r?Y0N&$U)H4X)&al0Uy&_H@YAY(43}4~IVBzK1r|?@<hpgR??E!8?QMy%4AV?g$nop%5g%#y-mUukFR}(b0=sx!tL2pM*t917(aJ>!kZTN3=R3nn@X`Lprp%w(Hl(Iz-QutgD>HTjL*pi1<mpY%i`+uoHaoq38?x#h*d}f_5BQEkoMzELnwRNJ2?}!ZL`o0(5BbUbU;X_Mp!HLvUHbKDv29N_8P<qIA<iM8A2e1pe&f$-sv;%&p)?}WHXw5hjQ2V>LPj5HDHGsLdp~LJheH&ex;67q`>Ymlb0b4WOEnprH4lpnhql2bdjsrlD2E_q%q0RmEDZK3Bfua+gt&YZfl!Wum=LVrJWd(whfKiwT5C8rXc`b4+u(#!d4LBHis_Linqy=s1yinGM<*fJMe4jC!(C-zDnLcUz<`<@l)VxSO##88f}|d!0f`_Ma_RVz$ebGu32<s+vm9k%sfAPb-#5%t0+9;PiT0_!N2e}FGhNs>I@koVfrP{iR8KQ{_QW<|8jH|^EsC;0n5gAOu2dtq0DzGB^d@Q%eSaRTq#c3UkvpKh9`YGT-mH02dEG&n#+#jhg-bl?^DMJ}=Dz|N3R(oa*wcBD?dg|CUGp4)FPYdqeA5X-7Z>`~WQg;e9@9D1EyrcYuojwf9zpV4os=@DD0@hxWeGG`5kz^Qj$zF`J(HjCNawAGY9MyNiAH8higV1RcJUV5)^EVa<+=>26>V@53RN*cb48|ING{u_wV_>&NQW6QcjyNo%4Ieub$J^Qg<W1wmE6c)M2jnO1K6dmRd@V&E>H$r>+L{*{?5%g&oxYhu)vB_^7wEY#Vx410)R}`9AlU~$GUEfQTjY+I5r`9ZA<_V0!JF_VaM1)C#?1U@)nVKi6E1<&jauYP*{;5t@!9vtXY=Oa!#cKF$rXt9#b|@n`w4j7z7At7KXg0r)RMA!MIeOK(LE+;(iWHaK0Keg?$}BVba%XqQFpdTfuc(pJdVN6*YpuPA<q!*+eHE;;s=};Pur74d)?jjAlWxp-zVJF5}{TmQzHGs}VF@7sIJ&5Ik%?6>&c0>zwCrwoWtZrM5fDyj)d6_84`^d985Cef2d?ZO$qX$M8Z=kHj6}y{84Zl(yIDH8oh40CcW*AQFwq4^MUktY(zM(CPk8rQhp)lh9&LL(|+44@E~2Da0f=V*+zPcKi_AphkNeWbc_m6s~gvbr)s{k{QaaCLn`PRH=0C7UZunPqm?6b!f2js=CMe<jyB_6VUmi7zV)yX?#F?u@tn0y}1b4VEj8Uc0fxK_(3=3^3(6%$4o0s+(?;j2ankHy%=?$h?>TNS38i6dYTB@(|n{dbjNfenhH&QD(E?as(H}{Cxi_f8@Gr4M3l_Hjxo{JWLvE1g_G&59r-$Ny!vhwH~`VJdB5aa%9g?m5<7L22H4PSKcbRLFb(swjuqR3+e30std9DaD!Yj3k>6<v_TwTz8Aer#MFWR2#3}s?8S$Ds1==x(sY4hXQ*oP9vc#oNpXWO~R}1cbaqU1EW+gr9PvqU#k_}q!6rDtEzGQYqMhkLO45xOKU51=rU4|MaaFBIV6X|Cp#>^q%*85?W?^j0VlpyBIW;arKb~l`R=lS<Ctep~pPl_8pqmmeBXi5tVZCrPnl=vF;zcO?o&~2_7+)S9FFRCtJ9R1Da$u90R$EcVBq91EYS+x$X6Zos3Zg&iEQt|7I`o%Hm?`~$TbpgS^gt|u}cC%0dN*ogv(1kkadLDvMC>DD9ib5<k@xE>;SnQ}2(t~rbCmF_SLV|*a|Cg4)0eb>RHLXlSCWD?8nwbVE8Tb0wO_;{MO^CWKyxN8c{ZKf<N&^dJ*l*2e=72?bq6mpM^RA{64V{sM0gur0KWxrR>UcXwnc{cRq`njBLiPTKfqR*DnB;0NG4vEQ)=sDa-(E)v=z1B{k=82nn5V}Td1ymCpVj%o+*@UyI@w15J^tTZ@;pE+yGhh*T?p+Q=l_qvMnvvZYZ+Ksji8@(VB7{)MqQNPgTtm0nl-??Oq0d%;#Vn2Eo_mZjX8YKHOX~SmQv)J9ZfGXr8k9{D}{(HAzYU#c!e)V1L-8(TqHjCeCq_77sI(}ORbLbgqi##e0sCO$Hyes?y{lQdduSK`%B~6u}F&71-z89_tdz}4ab(idJPUDDbmU~Lx(zqj?3bdPE^^Rv_!315lZAr>m;N1MF;}Q(3vO1^8+!IL5Ty8>FCW#Ir>9CTg?c~0-Sea5RNJ25LS;tXoKquQ>Td2QR@^`Rm83qp!QO12I7s;ch!`v2uM7w-7zWdFa9U|?ND4+(|ZhI!iuJv2KY8msmpXS(mg;KI!19b`AK&PO3nqo&7}eTTYGC=CYkb|(sf3ZvZcY#%l$|Ulga=w8jK+4+%A!GE9BG??=y)*uV|h*PHSGhk7be7O1%f5>m?)DFy`7VIiJ-_QA)gB;YpHlWY=7ABc|)r#6!#_yAHzXBm9}r^Vuw<<e1MI;jw^(#Dz~V1$|~*AFO&}KC;mtJ?2s})F>bs#Iz!Tm(5ZF$B5R9E8}J2#T2I{#ppqXTq^e)Z9dcdm+`Como3b60s67W*LLBhVaCtH;le84j-m`e+u6!Ct2#U00}#6Ml-9_tRolC;RmE~T`1>HPrx#Y^Pu5fmFeYqU`ou|CkJan~6T|EpS_6lN6gx=Up3nYe-3s_Xv)pFtk-J{=+pPAfPqGLX?m!FxrU4Q4PxR84R_d0a)&%Jt?CEh$1-JCDFA4rdR@}f+g;d-}Vn+l+j{4EL&_pQgnj=C5H-$W`)lCkyDz+xF2i+8Ie_9U*stVEEvXIn06fXkZLY`m67{*)>H|dc{cwEQ(U58QTXN)tE(P{K)lT@eia1PlP)nR^Csf(7w6TnISqqORBOr_A2QcY1*7IW68*E+;Cgaj*6=5G<xub&^wLMT5|+`+sS*&QKGB!mVaYM1j~ygK9>PN=XTzvnthU+9U~256f>QDRtGI3`w16w^vU*m|u2*HD_7QH<K;YSQAyZ7eL+RJna^FtGBO%bX_9>1D+sQo9Uy^1f{)gvIKZQ|kXRXewnDJO;Y<b(N#jrfdOnM>fxv-Fr7|u+@<%+-SYNj$0<hg~N9aPz64UF4!QX6L0gFMpf(O$^J$b6X19!LxNtXsgrs`hrn=xFt>w9sci7h)H+qU;6Yo+9+IZVC}R;_e{FJzu-c$@GteE-1Qqh|`&WerbFR}fg>_@fTI9y}LHXVV(9#h381nWU^7VounZGEZU1MeMRPo(UVpHj6k^SPfz^knsq!QS5X7mPgIC<bdYu%=rkAg_0>O3dtxclmRALQ3LPVE?C?KUytLq=)6QshXkcQtQnRfD1lqQ%qHJRC0MW28~096dgM2OO(Tb}Bj5klZ-6`#KF4&zy>H=INb<g3v+pO`|PqvU=dCxM|Q10*5o9R6=5T=v;>PE9Cf%n;)Y@GdW<(lL}k!0=-vXR?qGEt7X-T$Fu?(uK4L;dd`q*1<Rgmcwo9EfGAU90`T*8PU;?kA8Q>{0stW9+o7rg37A;UP0G$(r!?w^J}!XvQ-wa2?LL5%$Bd>tBf!N!s;}{a>zt$km}4yj=~s$FHs@T1K#G^Uy|t(`#H=UA@9Ag#PXayEF~}<S@47;Nk%7NNc;r`mIQh<LtljBu5LA$+5>Qp8H3Z*z@E_X-<xD7)B3D6fPkM{GRtSK`bBmbpbmRIpSm>b1IeHhOnc|a)o>oOupe{0#2BU@#royvzDkZ+-vM!+!c#s}3iDx4H9e{BYS7ujH1otBqdaPt^d3#dvbYPy>xQ!wWDkOc{k7Z48U05g92Hqn3mGg*_J=$c_sC2^C2Hq-TW&|jzO9)V*bh|R?2Gbn!;K;R6eYcMXw0U~2nS(hJ+5l&iwvIB|EkkLG3oaPh!@Ixy^Sh>CFz5X`|BDZ%xV##I=VI;8eAXIqFenX!auCO*=+M8$U4-|UEctNeY>oJ${QfEzP6FWi?8LJclJ0spqCb79l#X(c^M-mDA5Y*oxygccmkBmKOgj;Z40;+r-7!U!1!aUcomLXGlw9Z0{$HEJv0tQc-gOf?Z6k--C5#1c8u>!<rnkK_>GCc_Z`>(J`!5PTI^_`cAn3XPGIJrs+x{@WKR@mt-yRN6!>E25{o}{N{4dl@kSWSJ!8cV<db54!!9=IbOMazA-c+dc8&CPLckdFe?P2yzU_-v91|ARJ>7OtnLhkb)!z}tuhC*CD;S?p6i#qV(0imJRF4NxPO4ao`X;p0Jd+7L(fv=eZ?^8;KWe{wwfBdA7-FqWskCt%;km%HXOJ5d|12jNQlIsIDzWtWar(E~_+4{r_zKXFlqj41vL$(Z0wVpP>jW<xc>UHCnVN4b%CO_R35N1F>UL#UdW)+GyFT<oFF}M&9d+uB%MA)C8%^sb#b4sf^C0rmnV=P*Hp}L?75b{3SO|HRs(ZHL4$g?15nW&7V^3Rv@JWk`#$7U;2FaztULkN0u&w-b`G;H5N7(l5NsTbo5;kmEA8S0!FDpNSJpxU6>F~Q}GUw1aGq7!1~A}Q-~J{~*X*alvCp9txE8Q<b1xi?(h=DwtXbj%T<49gEcXZN2>?sPtfXde@Z9qN-Z%5*RpX%g3Fmh=(bbZ0G2!b?=zez&DSvAIm+lMw<0b~~s5yCq#pUMBO6!ENW>%;!`mF-CY8pV}5~ZolUL2R|Nb&hF>j=Kt0p;pzl6Z0v2~{ENx+Af<$py<Vm&hAmOolZ56kv7Y4%KuePg+&JdE=#p4I9~^ZS1TpiHh!O6WdzD9S83S$RIEZ9iz5#u_TZj0V43$)f8Z!+O=b%H3JZnfwq0<pNQ}ep09E{5x;pTaNsb6~_ahlh2wKVzyI(41}44`-svT=(#(sFz;&pI>$SLjns>70jKps7AaEs)9qnhF+(0)L1oeNwuLyYGAqcF~s@83<$1I-DD+UE*G>=Z^8b%4Fb>&?qo?Vq<vhP+92vX|d<6j|~O*^P&z<O1HqW7qi{iqX<k(zp#$`!1IqRfVG^B9tNW>cR1q%^d)<7X)@**-z0O9(=0=x2ag7UAvP;0moB9yKxTS;A*)#Cy0MqC>M_u3zUpYyu!VUqs70Pk1K}lEAQ6y2*FRx4N3V!Cox2kQ0CgK5ohnBoBklGM!(g%u%{T9N=KHsgnR0QaCDWq*RUPWfTIBenMKoGJ7$QIzKagFMRF(K5M89l%!b~y0o~9E4bFZqNJK3~ue2Vs>b6i5y%0n!TaE11Z%P%^!CoI)Jrn>J-IN1x<Za=HUA%7#|ppy1ds6O6PhBGWQTl~=rlP_ynQe*xJ>oUK8>)zIcSR*C1AAq;=R8HU&uaCen3^YZ2XK`K`%+!Xy7hKAZ&!s1z^4Z>&q}taZy&_Y_$D-1XEcqjcdNC~9F<swp^5=K|`1adRe|$4PeChSs9xvH%@4tTg-TeFwVJtku2j1H^G@q7rZK|WdvZ}8bs>N%>56q(yo`}>!x9j(BT<P-EN;6fk=Os;b{kH!*`yrsjA9?`IYvKCXt@F_?j@`fe-xOZscE)f&(1N{cGoD}g98p-K{~8c*dW&x5WOI}u|A&@81RPj*Sg8Cy@LS#2{OWz1t?(p%xl@7{;J?KzrFLQq96+*C_6ruxIA4ekuJQRl!35MVG)bF3KX3p3QDX_-!q;IzY2ZJWEz^W=bECAl>s7tRhGc~(Lg$`yDgtyS8UFI^BZGLv(c9s$k9AV1xqp0Yq$Y2xdc*?{hI{Q>8f)n1{?EUD`Ss`j{qvLm_?L+t?7;5V&i>kI_L}1_7Q@F{)OO0xt8YIMH&eG6(I>^L$A(G;jP-nukL}kuR_&TL-vM_jYC>horG(D*;ZczICGIP;!!DW2pQDFQ7bSJCy<00_NZ;n(G)y0MU3vQs!xBV=c9Z(`&*4&fsvS`RMZ<Jm8??uUgacj)bh4z@Gu91;{;s_z%ae5>h;WQK8ph>Gs#;_1yWjj}S2?QML9S7+xy+1o3jDRX(w~0+<+q=HJ?!QEbgxqy?yT3@WeN9VED=kr^A-`}y687pSO)5XV^hsxY}z^hDq)GyoUEbqoGY3o9oH%s2l#-XW5YmOeA)Gy#Une^#Xb1+Xj;E9?-3rO+V!j(C7JVwW=C}U=tgByBoL*!Roi^&S^MmJf38=fK1s>Cv7?J$E`W5+b5);5ZJXtKEli*?Sw$2XcP?e*9Fs<k#yQ|nOz+LzBA=Kq2^X!1D5J)v5-m-ieTy3=e;f8ESXz+_X1t$Hk-l*sUk}lVky+#ZEFtP^!53pl?Eo&R0;8CET5pdbEkRm?Qeqlf?gtoR=t6vi9ki31>sX8%`Om+-zyJLqis#v!26bTbkrqe`=y2{!e*19Zd`Ps7C`GdC!9;=sHB55biM2<Qxp-G5gQ+0`pbxE0=Ya$0aZ)~!JiCuI0-G}0MC)SS2`2CBC{ucX&i83ZP<bX^S}IR21xr)YlW!xD#|$1E4Z&XdrD4^NnuaJ8w%tJinh^gpspja(#%T=wY0|LJEGz<n1zX^y^QUpl7t};mP}anHe0YSjW>`J23Lu>q_s^c^sR5IKa)7Fk#7qPm*)fi)7S=@YZ?dfzJg!qy^?oV=_F{$AsVNDAqz<7l4?HmY&N7-9YxrAVMypIs(*OmSQgV{A27@SA|ALozl2d`qZNU(&`(xB>*(-)U%X&hW2$QC)^eU+6Uf$16*lxx|3!-$U&tLG=Lce*}<(Sj1BdD1fj{Qv%drtG%GYacng7kLFKMg)S%o=GFd*KFa`bKHip~fAW6E!bdq)SMTJE_iT?%)JucZk*vSv{a}Napof(RQnX!Hj3Pr^`98Elo%b4!@UqYF%2$^6&Ug^Zr~`D&y<gPcNfdocmB%aN~cAcqA@1^{?N){qsFcr<{*onbf&(rY!yyRJGU8NKTH$dt>T3ule6GFJKG8NUYS1XftQ6?df$CTk?;=E*b0@wo?J^Sd7MR9xX7+O~tBl=3}4rK8O+g9_Xp;&x|c-nu*-Zdvf;%4P8+A9j9?0e!({))xCz}LE$h}9O8WbeMtTYhE10V{Q~_Xko!}UWxV~l$!im;p=qk4;NqE~gL}c}uh}c!bir0&JpGp{a2L|b>ir*YPnRgACd9tB$Z@Vuc<7NN%2Y#Z$T%Un$UAfE?Swc+k{-WC(~E!*5jD2;m-w`7z+rCrvFn^!nMN7Qs8(?;f&{kJ`a2QelbSEY^6wM^7{PfF0QAh^^#md83$_F#o`I2Ya6&Wg#LQ*|8-4|bvOuwks)2!cI8vF+?|c8}9{%k5>tV|9&8;z=hIm;L6-Ux{ZC##Nsy_04qm+<`TtS?KQ-jmA^#m%6MzW8e4^VjJ8{GPnb3M1PQ3<nQ%V%epz1x=4%y3CHbt50WrBD?mck`H`{)TdbDZsQHmC@RZ-?3>;?xvNM3J~<D9ue&f!!tzt8=EyUwU9ka<avpB!x=YQ;&R<ay$z`iu?}%qa+e9Ik&>>L>ryvm3pGtMG<_7)#%19?-V>@OQ-g(Msn>TD+%$_ud(dB?_DLpEdf>8>WT3boLVL%wZBKSCj_Vh(7)^>a*N4)}2)JwEIrXYM`!0(+L?zS?MIN}B?y;MPqDmQu-b(1#P(fo|;h>#C?K4~e{SnzRS|E$HKi=px7Fl7?#?0(tu=^9A;duxtl!+V(i|#?H(aUGggYG9phZ6*53J69piSrNvy~8q<euMmgTp)P74Yxr|by)D_wT63cU{e6YWdlP07~w}8W@W{IgoD73IjpkH2TIWlHX7<d;@rv{vMYf1#1<k@wIaX?Clem?xq>@QG0Z7(aGgF9`J$Zb(l_B#0@IAr2i7UM$K(>JIHE5mqfLNONFso>s?eOKJ+ckD%fh5!_pPiV6`c--S33q+J2DJNq9(s)$)h+=Dmy<V?&KbDjuZSCSnX)adJP9J^LOS&wm!1-M)!j_M|f1GE(=kpgaMPw8iwA$%3jD&iEwU!Krm<vSPv!2Rtc$ezWKMIl|k)ZfJBv+eT3Ca6l;DAYwqdj{RFo<o+XrB0i3UTYdDo_KIT%pSln&DKj6CrjUuVa+1vnB6bg5MR*USqkbkz;s$n;eDC8JffB0x3Dtf)P<u7l8Rj|v;g_Ig~lW1{8LI}ImwLF8Gb;rwcIp{}~r?u*`8ZzyEjKT7pxw<uX`*TuWH@%yS#ncJ9`Z8O?i$SXUt9p_XsA9dX&Ut}vV_&GW@^_1#&C(j~;urcj%c$lZ?XzxsZGD8Vl9}5@((Zx;<gN#3=>WaDED^T|4hg~C{^f%p8(q;dxy^W9`p{RZQgo~_Jv)2cMj+PsG{6$6WB1)fV`?(j?pSK@(19|nFDgdC#gtR}7|r@5`C_lEE(8a|zB3+toNff~mYtVPj-e8GVOBf$5NfJJ)Jlb1*c0ZcvnBR9oZ<$VdA^u&hIQ+l7jUp%J!+!2oD$3pe^>z_;%k|+BDb2Q@F-V@uOuZYdfit!M5vKSDZJjaI4ANfT)<Ux1JDWj6ZG~{B0mb+WV{s68f9Jd&dXCB=XwDp@SFFFY=i9F)2jb<NT3$Mu2V7zxrHK&flkg>B-gf@fHEqiI%36XiofYqE9`HPP{vEh?OBPM`!4P&s|eqD6o^xph2TUq?wP$Z3LwN4<_u8sVDRR_4%>JfGr5nM&L~|MQ10iCG<HZoc{7uU5QFR6i%uB?$#jXyOLen-?MPe!SEg?h!HO}No*OB1@$k-bLnRemZkQKhTSr-u4T1L~s<#AFyJDQFRN}lxopL0t#Dr(OoE`g}yDG$wty$Q<EuK2VZCYg*Rgo|a!^nV<^e<#&)vPv_+4XCrx16(`m4qTXN(-fFh+C?V_bb)m%^+N>QidYKzc_e-MuhsSkaP9Q5Xr-0%b}*8t=wcvdGSp19b=W*8i-i{jk1~4^wnMf+vt>jN{fk89BP#1e4R&KVj4BnqtCKywwP_wuyG-~3KSz$boW6C2F`noQrN&rv{ne^0{kgq*ArlVk0DNKmYva&1e&P;6V!MsU|>RSIpNvb@-KDcqoSt(h+oe`utYf+=#nz7UCBE7@d{Y%DCgT#o3<wz`r$$#$77?bEERr4kBUW^gouxx6`HIAp{sj+>?TZO-zG$ubT8d2mg^PXs?zY6F?1_Ey&#IAD^6~V>X=L=8agAc0?w58a@*8^)Dm=za)-J9_UuE~MB{P<&aOSh5}@xgs3XEE^C**(W=TLp=#nF&=jRs7Iq2y*PRcL#tL7+s0(dU0#x&wI5$mkV&pqM`V}EPtOhT51?M>pkVG`LyB%Cw3@LcRM*hStrioUg$iMH`E*!nTBJ&_UR=?>TB^Qx(G`vS}4loIAfgZyDwzNX|hPxlCvh7~OYyozLQ%-dy6gz~VXg099L=^s{!k}*n`hNywlYcEBvrqK*0Q`J)_$x?{a62fJvWLmhq4n&a!s9u&L2~c%d)ya`!*@L?u;9Amr^8apsw)8y^YUe?O6*6ANkb(OV+Iz~##`0hbWqneN-)8spQyC6H9*RTy)+AbCF-Da_iUCd_f_zsxVa(i2=G(vfHPNl*g(xU|gcVhnUK6evl>>eA3pQx7Zy1_W>Lhmxh(HLGlXYvlHVJ_M6#^x1sk7WwkYl&>OB0M`t*81loKwlcr5@8KkLOcKmm}&<t%*<Uk-n(cmfB0C8YqTF-|gvNb9j~=fO4rkHu+D)xpmF;e>+N}A(EIUorE3%Tx2c;Dt}BcrPpNqE&%|}giqZ?DKu7W+6k=1wF3oM>L{@sv!H{KMV&)Yo|9`fGlq7>kGwwW$B?JKhAoDPW!M}o_Rd8gOB8(w3G9TIMKUx1X_dfNm1U6ya=kaJ>k%e^H5PI#xme1p2S_Yp;Ym^vZB1dO5uJ9h8zEekU55;V60!9UXA1hQxB0A5Y8GgSwC=Btv}V*HtW^2<k(==d&g-z2*x6xleNk8z1>;^hq=8}w{+Czx5-TH?V?(We_-ne+UOdg;8o$cl+QJ-aP*_+vG=p*N&~~>;{U&qMHVEnH?d}8OC1rEUMxI4xr3n;sI&g5{wYa5<l7Nka*1xjNs?L`8LWbcPWpHwlGuBpYQ7Shopu;?QSmm{-X?K8CdHWuow#%!{Gj7!4YK-Ecm79G?=C<_d3z-Cf>(1c}uO9oSTJXxY=M(H%#}K+$tb9P8h!OyV_o+{BEKDDg3BZKn6GRcE7071DSV1=n-+ivsqGEivbI7#=%!^rMTsX6m(NuJ9oI8I^WJz$UN_FC>aUe+|8Y5KBnMC9mT(u_@$IdYc1Je*`0zgRlF}IK>6X<1Y#VC<WSiK-Ykz)_(H$XkYbN?Byp4)Ij8q89G!H@aWVU!6><79ty1VK#fw|A1$w#Bs>IM?}EtwD+cOYo`aMbcyBg{Eg~ia4c!(&bCTw;HxuZ~_hvE*EmmS-|~|AZ&F#m3Y33?39rvIYN>Vp;1)hHl72{_0&<}RBj%0M$0gcs>9xm$j1?uu1`$61!>mQc51YEADYLjp?o}}=(Poqr0I^^^H^@R(zmp>tjg*s%$zSTQqVv!0pmNmVe>h;kd-ab(m<mIhRdO(`^P|+j&eUI%BSQZ!VL|XFzT4AIIxuPL+3mS`E52880UNQpN*kAQnV9R2XpH$b=)$^Xq>0vjT^vC)0JL?=IGlzrcsr)da^~G#X|TXN}xQO<@Jr<G<7oh@E)xQm}}R<G_E>FmrSL~)k@l@{7~>X#-!tIMRA)1i$a~2ZiJ|;QOo+-Kd5Gr1aUiaaL0t!NN5qMj6lZVC{TjGBq6&ljnH-4p6h>Up60J9SJkFBin8hpP$0iVMUfw3G3B<vhCOqVOHa2s&pH<z=K*wEyF?g_(n5U<c}|e`_toz|$ggvJ@iD~OZF9ockIImwxYk@>a$XaaE*A#!?zZ>vha?q#T>v+A-qdO$g*ipLuIU>&<XFc@qXH0mSp7bD2Ak*<ysIHCed^fibbvfRF18b$zG&0N72QPciS<R=k)xhKl-001D(EO~w8TwT8k~GLX)mX#N<wf@YkiW)B*Y5TeUzc(3XE1l+Zz(#$1D@6fW@of1a5L!o>YZ=7dR(-Qs;z*p_Ww#7*QBVxHo4g<Cz2ZEiHSl4U>sw0g`5k*C?vNGy(5z;B`>RivS;ShjJHzx;V0WN(S?A7>+58`WcTg75%K#{S~A-<w=<?PIP@us8ox}KF^vueS#s@j~q_&zTH(O6XAVm#I#)^Wb&&W5V_Mb*R{J|A~DS0e+bm>dumhknQ1yy2$Nv+oMM{yL>mYZ7V(9q^ckNXXx%fYXZRF=y}~YttsD>ly3i(h&Y@}135a4NGav0%uo@jICdl7wntR~B+((L@e|x#kpGuS_<IdL7)y7*FnUIa4xq=PU!zJmqfrh5K%zdKE+;yXHybrktg)G0$vdPMEvKDF}_k-CJ>Jq+?55jJyIA$Le7$MO}xT7^Du(wMX$dKd98?uY1vPbwMx+@xOe-pp$Yl4r?UJaWT6UklWdvV{LO{PRmmx|IDP!CiIE=q_Oqyh&rF&@)$jL*#?Cj;*IhII)1G5+FZzz^UnrfG!v8R|O9hBZU&j|;~bq{(;0Kl^J6xOm>p^S}5|i_066Fr10$HR3;0SQO-p0G9$r|H`NpE-Hn!5rL6n<p(m6uc$Dta_Kf`jGLY0$Y+t(>Fsg@U9R;}p6YcYb&z!nRWB*X6mSiib<!IMCjcPAKf*ZK5FJKc!{YMCd(i3j;g=@^;tE&CP`(8I4xfg38{`S%Ee+djfdeDt<H8nG``T}#>_Sp>N3u~7TKKlI2Sz(3e7}bjGCo=XzARp3p9AL@Zf8IjRbXj;9|k6!%!+l>V>{54eqH$X|Jnq<{X)`%I7S?R*S4BSfk?<)PKHjt2>-a8*V*!-3$#}$<4)#E0znqYcO<tp?Dk0w#38`|fs(F}2dyBm2Aht#qRLqb6U8J>U8}WsmX6+q#Ji|cn!FGd<BwamIGRjRl+CCjjQ1GIvh`8KtkROSS))Hc_aEOLY+<8?cAAaj$HGE56o8lSPbe(r?mL^&lnFPlYEhfoi224#eQcYKQFieCQkKx`IXk0gCWGO0%qxPf#iuT`shDHJeQ22Hl8uo#LP%Jsl8JsELh5<!HDgz3J9E@m0}iU1hklrPW{R|jy6&=nf`MCCv(&>e=R!$2!4}`pHDhe(OU^4d__j8k1`)ZWRA9T@VN{sk^AydZ9#BvfBE}3H5b&+YxB)`^y6?||XI}GFq`5J1s*+`RiZROw-M&If_!!ujR5zRaFg>6ph1o$SW75%6t!0k_LCs~DR77`>T_S#quU9hlz>mTM81*keh>I=J@jQ9lS<=iz*sOZaphUc=gwj7jL_x&WVJ@#)|8f~}tr(7hZWMoVv|}KH$@=>uras^0UxuYu^8*wfusMH4x+5jp3SQo2SXHZlo3hTyrtcD|EQ6!B$@oK(<_o*|0O(6sEdht=ZhH4bUO7bcI```E+Y%{%)acz2xI|ZJ9QsuBWa&rXmgzWoe2IH8nr7}}Uvx%0s8~k{30Ty0$I>utP{Ag0-IzM&voTbS)_u;byUn6oCIjFFD9`SfUaX?;Q!<Th@*t0Qiw6}TY*NG=jv#mlT)wd;<j{huRm95<@><GN%od`ikY!xb4VEl4rTUu>KWC3~>#uMvuHZx_x`=4zg4qr*tK@7rDzZeA-1P80Ms-QrtCVm}%dgJo==Ue<5E$P@%_DftLX_I>?9L$vw@gDvl>upPWKEq#@5X)<IZe~}WV#PBOE_&cc7{R_61PrzdEN8OO_P}3dl;C?-ih8BEp^9!9Jb=C3BF~T|LYTcmuBdtQCx1(bV8rl^XNV%DC;o7-G^VrL}bM3BoU7kuHGAERhO4%_{JdfH!U)r>_bVCeY`80b8y+j#NXX;tU40z>X|`MK#-nvaSd8Sn}qP=*_dh5cS<ga1LPEXngM~U0Q2M138^_4<}XEx0p@`caTyg$G^06U^5C(qk7bF`X(T;1kDYQuwp#+_(V)a^l%3&=P8_1SivYie9;Fi}qw(uJ#<L_fIL~@J4EDTJ1g{*u`H?B*ALAF4h>&F=DLdff+7KB2kfiFlpChkN!IT)uXji8XUwn9k+T6k!8_kP;sL(rN9?lN`oXc+L)?k&zkD*vZ@Fa@#u?*Gd#M$%K$E^-h1G+&9LPa%G!1Ess;TA~pXbE{n&KpFnazC1|QDxAxs8qWLf>mi!A(&;4A-K)$EH5{lT}*;G)uh0-j+P=Af_W*EOuS5&RUncIIyT%yq-?j!+$ppi$eR;NsGvocFMW~45kDlGML33?>=U=KY^iIa@m5c~ME~yd9*W&BO9|t0W=I(hSE-Bw3x)*Ez*$-K?AB|(imOz9&c*aF0x%|o{NE<q@H%{?icRYLY|s@~FUBw{7Wa4S-cfWx@MV$sjW1#LFbuZW;`+_|_5c3uW2O@&MP4$b$X~^Yyfi)QQWh>2a9I*UF+x;lSKpIRznni9k~~5y(Sj)5mfjfymyN;^Y2k;hOB=5@J(pLO=Pg0<P7`n7!9PFgv$g`GcshyGGHg|T?L%#ZCmTuWc=v6w2kPP8$C`bxICh61T4b30;{L<%PxbL;t>%^)_VLE(ogMIRirEAU6-CiZ;fE9lJ~Fxx_mexflii-Fgak`-TY+_`y^0_>krq&&1oTZ|VQzB_DLzfd6vJW(Bb1K{{9MgJO0hR(;dR)$%#h%L2nRJa;`0=RP(~IHGd}T8;=9w_Ao<4*HLa<=YbCfS4Px;a2AU#8PR1E%TS>UIA^rGVx+#^<_O>Lvbyr)FDHC6^6`_?lU3*P|(LtAa-yiMDAK!la>5p&bhaYXrzCGI2-`;=y_PhCc^jty5{UAfRe$zZ-$C@uuQqJ}fus5vrp3YI&XC5J@1q0!~z<i~IO=#B^?!xmczNv&tcFpV;#G&%O5bfH<|MhRbxyb*&xo=sHB{`1$AuPI{U9}vEFp_3N9+@~atgh)x^zU~#sA_a&c({9H<49T!2B!h!Gcq0??!W)~;r6dzJ<LLg&TC70IUpS7twIIMs1`mf0Q=`(ZJ4{GHIs0HqMdq<M*scChl{3QaG+x*qbsWV$De%@k`A#JPVB50?v?vtSY+t`Z~y%3uYdZl-~aM&{|rw=9N6QU#UDEjU4sKM0XM@kyH?=qs>i>G`4=sGf4FC9`gCYW$-!7pqkn9_C;t}LwD}IWQ;LiZr0tnL$eFf%dIdy;e-e!y<Jn<p`||7P;qzH)O!wqz7kvWSp<!N*>&iR!4K4#~l)PboSm&O6xbl-dw$dx6VQ3h8;gvuq%i{E4<QVAp#(T29SUG?x7`jl$-+fUuFNgY7-~5*SHdlLS2YFYVlSMN0F{E04`TJl0_RFt_y?mVR`&jN%@gWS95-slIUG;k>ZxK;LQ9r@J?*MB%+-F<*v*uqFEHRo>G;|tkjhwFgVrLThfS_YzG4jD>_Y<5kqkgytUmi{CH`YDEV^or<)Z`n;hnBFc4Go8=DMCeY!I4KLv-Z{Z{#>tyEtFE&VMjOV+KcG)x@zWm)Hc742iXuAga}2#olB{lW71gHI0qcboV~f5@`?G9aLsMSGCwpVgVyxfx42=-w_$%l`YQz-8{`>sf%f71K^*i>9e?&!)vfO>$`6t=kFu=@cdW{Ra|~$}X$>ka6@)3D^bEd%O=L`S9cyqS|M8di_y3SO%8#3J7j=h-N=8-kbICvdIB`D8qE%;#WcP!Kf|{6YcZ?Hjk0x{Ru4<3t?dCtUF`WkvU?yPmLh|e}*1;utvXXiaHJZmdwx2ei-(z$I-Jils%P}ENurxO1;24QKXYk-?2%xK|HVyo!@uouI*wH6YX84~;CDBhdj)U~4Nta8rut;P=Y(bXJADeP50^^5z3uP1V`iPG|t^nKUw-Tuhkj`VZp-ZxGY$#tqIe?#&%eJK^f{pAL$08mwy3`b3Tn4;8PVf4C39#{dU9hp?3;{_UA_givFvgx2i5;WiZ+#iBGBrkSis*qL&&FYdtM^|L;mX=eJld&1=C)wiNW|oQn*%YbtRc#TsFamo1+_I%kI~BBJtqIF(wRBS%u5UXmR*-)PJ2&FZ#2W&-z2f;I1N3ch~6bgZ?`~W@W&^&*Ml>T%MAuH-!4WK?lyLZrb5k&7U^Vb2lLL4v2@UYvpYoVhO8dYI3&}(uLBf>wGf2d8c(^W>p8HkEKCOuf0lV_U0Ns!n)puB{#sV5;_Jr0J`Zkj?&ICYmHL=d41j*v)Ib0D@sD?zPB|aFd35K(=_mPDu+8M7MyDAXwBQ@Fob#IgC+0=ylG8|RE+Ndh4oFWo907}g!LAkTS%oyQ(6K`Rmd7YJ7pulaV`xVTixHqG@8{SS?BgHk%r)Uq4xbWpKtDi#38bsHs@cb{8#6fcBJbuh7(PxIdM<JErhb53*d8*w16g}M;EO>bOG}H7fBdxFvdsJ827fWjf36Rk*b18aj+shxz?g;+jRBL`fXs=lmz@^c(&M+@TofLXgNY6UpH}p^!!18{y<ZDvTnD#|86gw^XU%p(0Cbu!%=+gj5q#jh7>IG^@nzbG(S)ypKUo-w1Sm80B*B_Ca|S9vt~kpDDW;b)N#pN3_NUZ6l^L?Pw4`#H-E}P#*hs5aeBlix4~vK?&w!9hQ3FDZ$#PJ>vOx7;kBhv{4JiA?nVlQfDBnk){1LuF_TrZBF0f8DMUgJD=T&E~$ll%k_tE4Edq$!08c}=AJ2tIJOtjkR0v?W%?P_OOv0m-3HezIIl6A`@w@@T)jIFM4xjsj|-AWr0on2W^wt4=68B7y7?xt+x>pImC7|-rpPFCRhE|KaX%`3j6z@=F<kTzz@bcPhAJ(0Nw3yN+9|JQs!jNXM&=@;vi_5CMNw~UT<?}yW<2M7h>In7EK`)=zXsrq1th$P(1^w>?eUjCujQ2^`jK44Napihku+ecZS3B)EIHZvDeDBbeuw)9z9fWuIRmzJuk%4_X3Wc?FVJxPR1`i1C)%g%`;*&w=OEbowW<peV@-Fz=comLP;I`|aBpijg2szG1B*N#sOL<r!OVl+rOjKG@?6R>7{!U5069PaiL0O+q6MAB2Bi>I++4j{-~koaR<DC&7AXFHDZ?liwJIY!gY)N<F9^Zn&UaxCC?(c2k)lt+l3^3N9-gWJ&-fEOe$z}hls`Z6Bb2FVm5L742z6(m%rgJH9d0WKX02g>SXuUYXZPNS>w0HP$`d6v^PIM2_tbTlA+8zX7v!cWs`TOS1vc>O_~6!sEiOw&^1C>Xc6=(h9*?(BtRRB^{tw;J0d19W)GmIRe^zWJX+n{O^sA98O+rVUmeajf|<tf{Aa^$W<Ec%D!eC=R&L22Hx$A9Go{h|pss3MjllQ$(pqHZ@=jhxZ%=y~?f|>F8*!8m?zWW6oIq<)exC+x@~;zPt@AAucZ`UvKnp)Z&`t2XUz#v;i+kQ(y$5Y&EE3FT^s_GQWaiP1lsApU_90=YR2qLu{sZjfs*gc|J$W))=I(S!V6-X+9Zq8%P*NV>!Ty+`p?wxPbEY+uWp=aD4(=cu0JQs;TBcBKeJ;**duS$mop3ZrB`y>tyV9la=?n26z)XV5upO!)M$HMe3%+g+matW|7=R;A!oHhw-j(N@7W;pQo(i&2Eq{R!?m%XvJJ*V=Rk!o<S`+SIwjF-(WJqXznl4BlgP6LHI804C5iw>HP41)@j}B$ghioKSy)45IWb5YegO|{05WiJ<(oBQuH7*H|yWieX6ssvl>{06Mv<US*YO2f1Ocj%Vecof0kyX+!<6bN>^r1bKGEb1pdA%Ux~LQlUs^*<*qU<erMq+Kz=>G7TPVd!Q0JtmTBStIwVkkV8^qVc-*A&WUj$H{v@Qpv@HefqC*;ER+&cq&8$KZe~N@JSrTrqYkD6Gw)&L}b|;xL0@vm1U2<GBBgNEEPAPi{-+PospqLR`2+@%bIQPVXyD%YEhVKWn2`{<VfivwxrH4s}pykecC3=umpLWGm;pyoKUkn0#)QYGgUvplli@D!B@@~M(>DxuHhD<l%b3!vvi#R5;m2Njo8L`czRxWUDKVy_<OYJn{^~_XdPT#dboW-+BQcegNNOdX2&z!UW+^m)D<eF{dd>dQ|7Z07uAfNO%RHT#Q4GbsX8vd>4Y$qqph>q1t*%fpnn4?}Qm9kc9VdmRxW5qZQgNBLz6H)VE=bMsY!&b!2P@i!EGdm<-edhj-vDzdH#2`d(t(367S_)t%lSKC1;^mw;0i`~_FHo2@`x$DjXI^fs%ZJ>oqZ6rf-$6iW4W7ZA&U;XKZQvk&__|{mCjt1a0L^?1adcDfj721|g?Wmv^<2QfjD&N+&5f08>cXq~tpWAFpNBvOeb8Zb6pyKO%wrX>*eVg+Q)Z7R8G7kPRL7IRSNSOXh#qn4JQ~p+Ju5V)2jbZD`ov8bhrUfv0QM{gY$6XFx~aLL9b-UUdU`=bLsy*K7}qfwXEk)jHwB!j?B$MW0jt^R808KN0`1v{u8Bv%2%Oz`iY;v7Wl%?KHBW=hDO%<3lqjqy<CHT>9tG}W(Bo@Vl0Vt6npAEDqy=L<jF?!=;;ZwyXQ-s1iQbu8og0!ii#~@5m=Ymi&OgKRsmEYfd*djOI9ev!pvVyT$H4YNHk2niQkO3)vD%#&jA?nEWujDM7iCSGBF|oKcbMm*QoPB*#=KqD9%&C-)qOq6$NaEbOo}RXDxn0Y*FMj7k&tFHnHZkKBvt~~&Jy`cmCoeyCP+pWpk`T$BGxt`LnlXyWe+;_Z)yL}!~X0&)#Y$=@ePkY9foqt>eraDW6cTGTa&1Sg$-8$NTY^81orMU#e}(q%yE8qmO|rJ=HjF93zjF-dM#WtT9D038p&keFal;?M!RXi#7Cf<W?B!8K|I1)7)-SDGT99VHB!eswa>WK%(_i8|6?k>ESo}3Qhm3l;VU8GjmgquYTN_<--xD`d#zzQk)f0zR-W2mp#N~=ztGrV@#iqXl9*3;-3{!q)qnw;qSA<@L9$1?6bA}myefUEDYC)H#=dqTkMRRSW{hyD<}j|St>F2b+{~b)wz;G@o!q%vYhGiP`Lvjz<OT@bPGrA4=CC_eYKb>wr>Me$L+njfcE37|ca?+!A_uLbf*&O0F*3dfR+M@ElN$i{9CMlVgUj&Crt&2UJF>)YgQXQdK$hV*bHI@p!OipLYr4@^B=5~1e%716$!w8Gp{~3L%?MIxx6kN)ler2TEME6EHvx5pc}o)HnMGzvSQH&3cwP`krAgVj0CEMLPxCgpLO|IIDf5Vwb|=LML|d_`q?IZa!i=D-XJv}xV1R3%O2~Bx07EOt3`}a0YMaiy?e%<H)q8?|2+Jl)TYaAFeeBZ+lDQ8uT$l}cq2YaQMQs@@&d|ES*MX}mxB$N`#cA$K2euFMW2ERtCqd(=Rp6AxIgzzM9%+@06sEXHK<LjzwbXO%4JmP3qf7;+!NZe6mwlI%dO-CS93WubOwv^M%7~opE}Qm2dNuQr8Dm(AMJLTCg{?ZWVvE5d8e{2VJ(UHHc@rCP&bK6uxzW8_ZquuZVH6ZnU}4}N4PMOBAh7`kvp}v81M6?r99<;x+L3P0u%<>*u!_I^BT~5=^IC1^i}cBmhIv(l&T^K^t=2z7^$hua_sREU^swCaZp1B)D}32d+8N~c^nu=xdsbsP4$&aVC41qOaGO|zyA7#3hpq&v84+sCniroD-8saPp$mT-TJBo+0#&X?7RRv8CQ{AT+cuq(le|&|v^9-s7$}=EogV{TJ1VK1@SD;f7{*0%4=h8iM8I;mPYt~&{SZSt@PIt}l43mHky9Nh_GB5hO0F2E+PR4X4x%rnAt!v!V;o%dpcngQSrmqkoqB>$j89G7ICe6R@MaN(5R7XPI_UU8^(MF2<we>;`Bb4eM(INVO+}H*w8Zn&$d*^YYoIGoDi!1xj7Qs={q%9+?n=21sU<*ORu#0tAF@C*mmbY!++Ks`H&64=sV^;B48DXP$!khf?c1z=d@gWc`y1_A(dV2epSz0lmZe=MN@v}LCk^L?o~8mtdSAhvg#aA7c?@yswmI@Wq+$>9r$K-OhJP=Vrc&I7qePx(ENSF;40CgfeH6T-_PD6ZawQ)+Myg6r=o!r$av7?jQ&Vh_RNtjTDtmKj4q7a9?o&7YB<kLAPpmJlR*t&os2$Up?6L-|T{cq8As-G-ep)WDGaa)Oh=6f`v|*C2TQ`yyG4^jsL6*9k^ZKHs-Mhh-*OLzSf`K#dG2eZx4MjxA-8zGW?CPbj)V$Yvub9{mplh|rOiID!cC77ka~VqjGiitN5J7z;I$KU|@bVNdgMaEZa-yG~w!coajCCfKi+j3!JMs20u-PT1X02U0%?RsCl(T;9|6)@L@NODn{Vu^M`Oyye*lE0%dv{gEBA<SI2$bw;sfxWgO{W0i4O1^GW_m8b@g21RCc56Zb4@#e;89dIP|XORH1ujXsu@eelMm0*V@T)`j3?^+RH168o6_d44!mWxxri8YN$iyGpj$@|p*Ys5Pn?uHFcggTQEf`Ny4ieNeBwDvu+}7*p-t=HZpi22Nwz5zWuk?J5e1FOddUolv67BIIo7<#a?UigUf1UKNE@eWp=7-msGH(diisPO2Qj%vWY;#EJ+NH5DB~kDz#+Im5=%!Z&TS4Urr@Sy%oW!}S-t&!6V42OAuGjrsv<9GYu9tYgKcmtl-Rhmi2;m!NAk0OFM;~byLtW>A8K=Xb-(qQI=w5ZAcvpRj-$B%DEe1M-F(sgS{fM$E5dxDv;G+sue)7J6rEL5l2Z688Yay_j0@j%TI<bHBvXIiq>dZ~U;<jMuugsl+6VwGR5HNfpg1Nfi=ALjs=|{=7qs2?sScQZ3Gy924fA%hCy2LH_GtnK#>isH9>w_DZ-ebxQnW#_(+yhqw)O-@I~IJur^G8hS^@#37x}b6>2Ny(Kvg58S#cP!bdr!Qn;-LmuIB5)xBu6s#p4$ib^0-4(PgkLg_Mbf6y?0Z<O})B?RwZ&=O?FqJQa7cmPq%qM$dCxcu2h6Wrs{@fC;+-2%voJENC75&E0&+5Y?k8STv?6NW4)v{Jpbm^KRt0O|8J<$}b@m0rC|Bdh5stQ3;0ZNwp=fRov~eW3*|Q-~aA^{&=#ejS|sme2$OFvNRNrwr`u%`KjGFG1IXU%w7dsHn#=xjaS>)_8p__Al{^OgV*zS#^#KVKIv8WcY<eit_YTW_6-bV+UUt}Dw1-kwlt<^jk+)UQZXyEUsyGZfb-}kxjU!G+3%L!_Hr;l>1vid$Y}Dt_D4C-6W`H$#i-B+p4W@;t!(h~W<KPJc`p@RAT{uPE1M`&fJ4-rh|vNE1bj;wF~C5*?E9<0mGAkAklX{uZN0t3(`4vldI`k!HWbBz#ypf4{EIMy$W#H|azDbEW}aahQ^mStQAQV+EHY4*db!gOZd`{qe%@+;_QW7Gk`6VtC6ITk)pdmjx!%@ZE_aY6$5!Lz*t|nW@iD!-dn$1w%Q;7iBtw=yZddS&*QN=d;m1e@N;W>l(7D8Bbe@>UMc)gVPKnG+?hMq_rb%eYN;@*!NN&h*>k~b)mAb&A?qi-^Yfzf;(C5<A?h=N!7kyD|sH3l?LGBO}F3Y{`3VlEr_*7YACUzYAO+|x-gX8YLEVI8K#WZLLfuHXScQb(_oqL{VG;|Z*!LSsBXhac2(JO;QhV47Q1&IDJ{<Yjl#zGS+c=q(UcwF^f+|{Wo^li|1mDvF>7i$iRqgYIB^FuX_1G0qeijmrdxNRNw7qiS514NBm`|c=eey}lzsLnbLFXldA^LPU1j|b`nJ@_oQb#BZ!ni-C#;kXom!LZud3-)p5&Y%c%oc<4FHS*Xz%@?nYzGDkW%75jcbrrh5ka~7&L!FVQV-#hJ#UU_rjX<TBxPE)$V-N|EakZg1M0kN3K11(tF62WVrsD2{h^{~rSP2zbo3zI3HPZOtsCC@@9kJ_u09=AzCcyt_Afae(W0d{%3>H=DYzOl|>7Pnefo3$Rc6=V5<%N0;;2~s*>ojy~dPGDyO6WkvI+Z=}8|PY&a_ZvL?qNCTgaMf1V$We3Nmosi-!y=I&k~~~$GCk|YL&<M4Z#m&Tu4$0xUDh7gCDYF&h~TU%S$i}Mh)224?)WV@C3D?^BE;ftAD1@OA?;Q4&R&e_WRc0Zi_)e{(12znw*c;8*&Xar>&2i8AQXrK@!2Ax*%T2-|*&uY=)OHW{jF54)sl*u~YM{pm)qfi69t{W&_1ED;Fk)Z_7Eq!PccL!MWM~QI^uwk(o!EE|o5;L0cnm?JjVIT$8!Rz{^8WDg}o{xNR)$G2Gb}A^Whb79k5wGD;jV%a(d6^e6gB7WMBb6}8zTu+B0BXO@)V37y&<uwYN|y$?N{&)MAl{MPq;rAsk+)+IE6L9M}6car)phB{-3M7P82d5KnUw_D8RUBCIbLI3*pG1HOKfvy!g(4WNyx;9W<aAP=iU2N(9OjI7L16CcpWJ+CLWmVr|kf=6C%NxPO{sY?+(HQZI$A{ssveW&S>fSv}Kais~laCU;<ZM5$-?30CUSQe@B;ol{A+mndHiFXd_DXhFEY0T%+;2-Sg*na`h)#IH@*xXzThb_kPt)fVCFF&9q>P>Oi`3`53rNPPLqubAC8y6_Y%ngzFwhk7x?^hvW*Rek7qIgmf0v8KN5i#*L%UEj=&i_Daq`%T(3H3@xuQWfiCy3K=R^P7kH7u$+mG<!=Yzj*7p|B0Uw`~Pd>+|S`1Bu*+t+Uf8+)wzszT$49%Tmhd~`1_9DIWimQEX7@;vaBGB%-ITeu6aulVMYKg2bQUy#>6`@*zqU*&sh>%v9;{nrn}zkc;F3lSF&9{sXQIm}yy&yMwZ=0+!k+e5?68LgSD>lN+Pb3yOle|%JU0BM<hSVmVI?T<hECJ2&aO^VoAG2Cm1>9EM);otuG*I)niU%&t5-~Jh%h&ZsvHH$xX8oH+NZdSO5Wp=H=*Hw>y5pzXZomk<XrAdsTVHpKuJ&pdc{hpXgT+`+|;7%#x9FRL>Y};q@<mnZ_A>Z-mcUVul{4_mlextnUjXZ6d!B%))lZHexE+cOPG&&@$QSvUpVV!%jP0B6y@KV=8;?R%`!W)1NlGPB*T5HkojpuTGF)s(x0d%2`zx$%TOb(@~KJhIvU(VLt4)U((u!_8{V+i|y`TJl0_RFt_d3>Di`&b4)`-MZw))M#euB2U(r-#s+tDj)SJAh>y8a_Ivl2vo33YHknDH^)Wm!h%na9`}K79SAwV=S^Dxa@wi?U{J^;thN`Fs++dcL0x3?S77!(yix1OK7WxhThE7nV@*Q*qohN`|5jtu2(~3M(J{}Uz>D*MD%A}VCp<-+hk)SAyE^n+oQm@b19WCO!_t&=YS&!vp08BE-+sbE?B7uaEFGu$eKR;7B@`!Hta8Gc_0_eDuy@<v=853BBgig__Jdr)e_fr{z>J$VK=%Au~=WO1_?#hSz4r;U&zeDWn#L|kkbbfi4Y_F0!LsWl7ef>h<^PLv_(t+%^P8xJss0b&P4WL3Lf=8{__6*A74+%zPjQFHd3?T9+oskz{HO^-1~SjW4Xtr@TmZ}21!%nDc3{o6Q?JzvXZ+^-}>B7hCFKQ<)TNO!s6_%l0POeHf%E=4wXMr=<(4syd$-`1LLh1S_3e~Rx%!^e6qtl-o|>B8Ke^_*FbVk46Vg{Stl`U8uI{rJ@cy>f7>yfSvl@tfxtPHHW}Ei=o37i1d=h$S9VcTq1Khkf)<gd$ABb$P%c(9azc4E>3XgoQ<;?n#*(!25m;oNe*F}6`QuE`GrYOQI{t!oS=h!a0i)Zs7()o!Cmh&7ZqWd$07Wr3V|Q-9gz(VTdk#D{2*BeiHh>$-(Ljpm;PzlBRXlx+A?Q+}88xd+7ND|yju^oh`ZrgIC2WtOPHs)^gUATVz&nl@Ksl{+_c+Xc`Y_s~XTpGR=@xuckTQn{Twcxtq4G`<5dub>e*qRVj_?@D`h8WO@q5z^W5dG&Dj7t<QdEIr@W@CM<3rg-tseSf9B(kLPdNY)$j_FiHN`1jfNGr2!)VvPG9NGZRU#<*WrWFN*pn?Of3dB!PU9neY=O^Xw6aZ<Y1XP5ULLQ%w9s$abvfp=_jHfP$CxE5Sj_u5ifQN>MfAmichgG9fj>UET}7OvTW+wY65p#gd+z8|0D92GW5N5*T<xiYP@CN$3YK9mb>k3D_r7Lh5M{tFkk)w0JzdX%ZDpZ2aQKziN2NOxKV{lqE5$G;i8Y{o{`Glq5h)*zyodg`>yF_Ll!s0I^N%0@cz*)^VHf0l^ybl>OEE7_eW=Ap+~z%h@Qpd0>UsK~m=~}G?<(&zms)(daz;;sB>_Z(!LAj2b%k|Or=_wq5g4VN;^FcuRBDXH2ssb)xL_au=s;K#zUc5NF$eSm^q0WGtOemZe%+Y0{4DZrE`#CYgrVo6FmLJy*oEc1mTU!v^8sJ#h492Ye%fw{ZTfJ7zgP`E*N07P1w^99Ojo-yE?RFLu?pbeL@(Pf!=A@)z1dkUAgmG{20pFmafe%e?0Ubd%D4_Lb|>NnLFS0<gg~V>UznhuQNq^2d3h!EMYIZ|310;sL>P$#9Xj<S!Pdn_(jixz<$@HcP?_NK_Z|CF>YmCBS&kJs&F<<aD``_WgIBP;Hs@O_Ltq|PVH0p@TCXChwXerTUgxIq=*5|x8+KQqhe!Ad?rkJj3<PIQeIv)?QW5&M7xwP%zmFy>odTugwV;koYZ4Q!mbvJOLdkZuGjTJCm|0uDstAp=Q<DU5CIyT~2biQ*--{TA?N-{5=<G_kvaOE*%wU?xaW`cfU)PO>s0?=J5LQ}nI5xgZgKlSe#dj3AG>Zn(#!TbQP;ay+GWRq<pj*NJHQx`TVQ*9d!8&Dq|4E4G(NV$uaGKEpa2TG`tc0=ew)m5(4|d2g!p%&N-PC~0KFWemz}@#S{&hrDGJ~bhZ~^RqvSqaTQ!!i9ZM8M-WAw|Ofw&v`#7?)njWmprD~r=XCNE3PPB-5x@UbjxxIG=q(=fhj0N3xedsBlGiXjV#p7MRcZy-!qn*KcRNj~Oqw@qeS#T8r_o?cx%jSZVjWRXgR>I6TQY%{242afUXG#;NUY^$5u<gQ%%e!4cX0p!qbN)&y^H~kUPrs4nvGUs-*1)u_nqgn4BP4~qk+aP};ga)${x?+ZY>rQs38d(`HK+hW{Dr;6eiqq%{aDb?Sw<qTmKF;$qEgfB|-$n|XIuO%pTOU<UfBiw66jqTnZ$N}1;j-j{(9#>Y_bL<}Q{8GBzYGB3DP<BA%lYPi4sBM7FJJjaREdu4ORSvWSo338QxC<#7w|FhJfSv|hoi2%`6rL*F_)!_o<8=g09r@DqEIR-O$~U#VWdYbOTw-j>Dy?n8oF)8FVC9Q<fDn0_5DInzPwEtKQ1q4#c#BU)Z&^9IdQ3->O3#uQXm2AVIh#-gI4lf%J~)4XS${=U4uUAJpYTY>0(pxYYdUp-i%VT<2m51F;QRh&R9~?j4WvuW<Z9<mVh(5e;2hxUzb`B^7jtNtv_ee0xaUoR87_fs^M?+)z+cRED(Ku4)0;r)Tkh95Q|^e0B=GEurux9{ftDRrr?w~bqJ)@ERx%AIIVpEE9e-rq4H#tk;IBOyTOh`2MMH*a`7?dJR4(K#Dfj0vAM`01<>ja{i$I#tdr>WY5_t3EbOfkV)lnS#3@#%b+co^0w$J~&@&L4>)5qoA{Qo^Np){%za*(~keRE8KdmWG_o+^5!n)}rME5Jr%)$vzz3q%#TS`O~9<WrTM{7Vp<y05^7_Wq-k%&)TZ(5^^`2%`bj`6M)48Gq&Nwk*J4)<so?<#xbcNhNYuYU#?&_cXrugG?@0{~k5zYYo1RM>SYCQ~=5b1FoDenygTTMGC^=*v)#gy#qOH?yis{3#OL-jmGX-l+*cH4KHyD#CXjB@`&y!f+xQ_bgr+2N%M$aTyRE3_d*AvQ;I?RPIBi`$vbK<(_pViIdf#cArLxQCJEe3_@eniu9NJ8u~ad-v&IFzC8mg#x!(3(_8a7^sRJrF@+r2D9U9YR2HuKhkPR8vpLP}v@0$jk~Bi-I4S}ve&(F(=SHk-mky_Mz6~yAnukYZAV>NeDr#-1EZ>?a0nO)ZCnqh4j?7B=1a#|@BMd9g;!17Be4A}>7e`Xiu+BH_HGgfsDNR_LWD<Vx^op5Dks0Ux9IH($K(2p`JxdAZt6fNWUc*B<-#F)|ovQpkw|KrOy$9G#&QfHtvL14&x~jeyTo^$XZw=|$Ii2^Q^3bWEJv=|Uhv{?Sz;Dg?z~*6eQ{{{|Be8{fO74Tm!XE=O62t}fG}fZ2FRm)E2Dtrx9)i_ospK_F2BlzaMjB}|4=QonQz(xo8G6@7G{ys*t0*9TM33-i9*wY#o)wyL1Mz2iec~pJL*FJSe0i3$HL(K@!P49iZ850rheaUG;coCm5w?Hkn2eGdo-r%|XDWNSV|;J5_Z*|#VFJHB`_MHpK<e1pji=Z`7hVQ+L{jr4*`+HCK9_Gv990zO%jq1Cg7h)y@ip?qpX^snDklQ?C?XILagUhAQs;9yxieH=?aU<34K0~P7{g?#iS{^WT;U1TW3a2eaTE$1Efa0YV;K5lV0$60$<rFC%a@fz?OqC&v6*L?;1pRwS%aq7v6mYb=7zpYg4;~iG3M>EhCqARsw(S|9Oj4B;tqUwghCvzeV*--7|m2NiBpF=s|1goC3cqzTFT{3u!t-`&9W3lv@E`$>`1ZfL8q!YP3b@E&sM$%Mgd$zSdyAi*Zm(yXz!^72g`#k6r(hcg#n6ENU))ELeADCT9y2Usmi9RUb(ALs!Tj-mF9PUDYTAdAqol~VOccgft12TaI)#t-Y}YGUPik~!Ne}03~XA4jVT9&f#6KB3CeR`CcDL<M#GqwCKwx<nR0>Ur=^z{Q>Y%R@AkBuCA7IQ*?UZld+`4o(cp5gwQMJ9$r3cnQ!}jX;5g^F<T?{n_%Xq)fUb$&iGg*tT0mf1RvJ+?$oXig;y?jxSfyVzsWljxYWA_^zFh4(z?}4Mmg$cnk9|E>4F1VrC|-nG^U+u3qZ?`7f-gey7ywk{K#3j`S#6Q;=frph8@8V+g3V%%`C5xOvaGqqn<Y<@3*KtV7whgI93(Q6U55&15V7@7XA1gzpYyq^1SXJ#Xx&C1RLs~uSV8akPj2VPXYJZB9J(omjRMrHM9^T2g}0T}g3M|`B*Ad~#Vz<$r$O0hlbPpT4L{4f+A4Zv$kSLkT!E3{&_1rw{U&qDHVAX*ZCeA%6Z4joQZoC?()B1ZOK{G>M@iH7a{&(xdfMh~az&D|_fTe>DaBHXCW*FUQ|V1rRED`@S^11`;B<hC^U^&%WS2ME634_A*JHz$R&GM@#bat~pE%5Qj?8((Sx=K;r`lUKZ+kuITy+DXL&Z|+CbAST{?5DN7!eR=P?XE5W1(MFYK@0e82j|DWLA*u0n8J=Kt?e)h<^%rHFTSjJ)%k>CZ8Aa6ZfS9wTroHQrxnW%yg7j5<_-OWGxV(S_NU%2~cGI)QQS-CW`KY>&U3ANRj>**gFp?4rB6N(p^3r_iEM2Bmj0({xh#;?2<kM6dtmehOzmj9VDb3tQ771F`wl&*gT{<tFMkA6+N~Bw$D?w>9P!*>-4Jn9ff-p_)z?6=rQt{W|)@}&B+{Y={M`=F0!YB(`9fJxsfifBI~c#xQRIL#(Y=X(<D7^gwjI6PO>cja;tU2QO!<n2YkXz83iu4y&GeX<3nE>m-hM53~yFGhB%(3>2HY6JmdR~rJ15d*6npH>$}h=a%m}=-7{A?O<73bfmj6lI<g8AaBY%&;i8q{3vCNDgkabkN|JvJbnPhVb7FhS@?qRrNm;QBwR#ClaX$sND1{NT!@w>-8vJ5Tpp<fsVcSz#I;|cp!&XVI<Gd4Z&Hx^ougqeY$j^C<gDXY#VskkQgYZEtbp(H9t#bo8j-8Y{ybnu(Z{u2o=G5fqlBulSa7oaIDy1v(bH}4VoiAC=3Eh=CAd=63T)rxpfInoxoGx9#%ecMP3=-eDpHQb-nnoeYcW)qm^4b&yc$ig`&jk*AkfU95`keFRvzu{dyR^^AM7ucs#K(}Q0<C^unf`<PI0xGvLtMITj(jGlKuC!_EOol3d!fXYqCFh7_dJtEd4iK1-ZE`&8Ihuy)UJC{J~`bJ9=oaqu`&s3nvJg**LHIV1<ygxm4c6EuCz(;c%Iqpzd0SdrteAJR_@mHg|^D;b&7Li8tusjBhi%G$YzIpFSsvhI=qzKYNk<8<n#K8EQSU%lkym)6jg!YfwbY0;$BlXluGY8lQ_2scOUFSAsKR-XK0Y!zVvyU_gb4EQ<efuz!vY0DjhVz+ULNRn@g?(NN+o2t_bWT5p{DibkEHI%QE<PTH_n~sgL^$AIn%L4Z8TXOY6fA-xJO(v&(tTx)5_l9M(W9XZ_g!#b&?YjZ?(RU!qv@qbl+;Fn!ZGt<`46h*@+SH*dEvCj}{RnD5<X4U3=s@gY!4_sTE1&yc@KP4^4o@>9!=+0qLwCRsLIn+cv|UG@s78oq8|m#~8p6ZzcH$Vc6D_y|f>^;W435%ZT%K<ZF5?LctxAA>_~OT0VhrwRo^N?B$$$`058%&*pJlb|tRmDo=|;sW<eb(Ml<sb!t|B#gOpN|AF4-&D$ZuRh@=tD4ywsX|bP(0Lx?m0rM;^joNA#RmsIr7GI?L<y!8KT7TMDv`_NwDT_NIaB2$6c1J5?6#*0+6{6Z?*;C-c!^@x&Lm=$;u&PaHk-&)WO+z?ybI_g2+8Es9+QwzK&mugliM+I$QF>+17uj!oY4IyTs!{ER!|P$E0Dk-lf3XSEcd~-(G}KxTq?$hOmmO&OVViLP{t@)u4e^Qht88M|1r`Mu<|rK=YR1%HIIgM0X|RlSuedSMmA@a>>LnRN=E<coc60y;&NYJ6ZLawI;z-Ma7@;EGUw?9{25j0yIt;=@jlMpeHHeTM!+=j!WB=(ml`8s?d({QP3nVE@Gc;04C~}~n~ngTg+Ibb?O<~BE&&N2@1ia8BQI$SPLov4v78h;U%aMCnN0_8pzOc~KBSRMlikPBPHcni&QttPv4<7DLv5uOjCL%z-zad#o?SvzCKvg%H>S|Y>FRBrLAfg3(<&5<B(1Al$WLy5xDMzIuKU#fUt6AvUs!4z$A|@Na9awAFbg-$spiQS@|Vj^TT-aTRu{RTEn^i&zgFU+{TDrXjO{L)u}T9>XjVYz>&p#7^Xi+K%|`)Jb+Up<WHPc<E4g<TRNsxNjVTaoC(~w@OarWc`MGpN<*1HN_9n;f-`W9h1M@Vr{{8p==Z_~_+Q`kFM&|ffvZLr#Lw<+4RZ`3?-Cs7Nu@Zw{HM=&qd-jdjwb^zYqwHW~rW~%<^K_;ZSXLw9ZupL;YwyEQy`EHNIu)jgTdW4Bx8w{`$7NqC=7YANtA;3WPF;=X&MCent9eY_c4jan@M@KMs0~wS^S9O@_It(p(3hQ;`SA5UKdJjXb}W;XVFEC(>@nv$qqZsEBr1o*x`87DzNM@k&@Wi_{Z%a4_k5)!QUnFfdV7h?%@7y%GLP$RC~D7*c~(Hs;lk8oy%BzPr<o_KMlNf*-bS~@KqRw>-;%4zj4swLTP8Rq)ldWBPq8S=YX-X2sXMc{Hslk4kCzB86xc(Ee!ZJITyM4Bpu`?GdQ3F}JdiMT6N+WLP!j~Kx3yQJ1=KlodFW@POQP=yRF&4--8B@raqygN`FgQE1;=r-0k|Y}C|gbeX0T5i_dHJz<FyxZ+Y;oST(-k^E0i6|62|J@47WasLtB><IAI?)I=&B4#oK;HwIV}b%trhCSO=5atjNY(08EhU#`H{I4XhTm>{DggV`e_`QUK4ud5T{-Ta%jP?C(=C;T_T?&lirz6(DlD0<UT-am2^BbIwaaz)n=iltuu^bv-?Juk7r0&SovQ0<#d6%BDVjE}rRDuZc^jiDOx4uA><YW<bEKz-(%;>NlYT7ACs+p}fZMS+cpDLQhMZ9RuHAtV3Y@9yO6rC)X*z>`5ZxU;takTSo~33BgotUc`7)?p1P-#^J@RAEZD@dduSEj8KG`g{Q`DFvs)EjiZ_6dm5Na#fsh<FN4QE?z@O6UolSq=kt7*qRZOoWVaB$ZfW0YLT_Bm#G)eHvZ!umhAEU#*twe9>rd%53{ec1_Tgl|KHeRvKe$|GGvH(7cOOxAMP0$FzQ{YKc!ii%m=rGv4_tCkLJhuj3})z*FN*yQC>H{ST~*lara4X%GIi0?_fV^J!W$U9$5*8BMsqonp$r6AjalXbyy(&2=fcep&%R2IB;E?3vNa}^rcP6yDe`ISW0nSPwBHTbrH&nr{;q-^FLlNEM}-@wvR={VG@L?AWwivOWs}GgRbYHep>N7}r_{f52KBUfzs~ZBW@o_ZAYwlcf@%}8vPEu>V?y`W+F|Nnb;w(bt~?;rGeJH=;K3Z|leOvm{U~Le+^NS`+bHj3Rr>MVLfydU8~IAdQ_k>j1QNGftk_+@`7po#`t~u?k<xdr75dJf#ooC#9e$P<uj%;L0`0$sZjCp3i5j}gxF=(Ri-ilK^>biu<55|T#l85&<HPV*X$d1_XvVNcf#tM0vgC+AT+iDrlMP>`stqIIC!yg-g{b+F)CneZdnMlG!qJB*yWf^xif+shBRZ1>J%h}vY{@l1r|HOL-evuiIaG{7^NX_OybDMtNOCHSFyCRq0FNnNAEaX#Xo`5<aaI$|G)B1>q~jld*PZKm?w2rK4)+af1XpCNc)4svK;KoNzoR)nJV=JG@xDJF`rm&1?U&zvgbzO-{C&GPZ12DR_<Q&~vZc@`IKV!_>K<z@sm~&Ii5b|l58&dLz&8j1GPJ?99t^Zn#wN6D3wPo572n(r@wjI33-a1$UsUh<R5NYA|N3G4*RLLCAzNZ3PQSy~9OkXUTgJM(a-$Ps_Mzd*jMhw&c^2)|v!na(KRzlfb=WgG?DDXTuKLy=fA&o<6vsR*v9n^h*S@l0kx|9J{qwKC{^`Gd|I5GqGdvM-V2^7Sf9y1LO`_kFP#%`qwE|yPJ^n?^=40W9!aYmVIYYzx3C4OF{bTz*v5>f?&3C|^QtTQ4x5VhK&ot80D<EWPFMLKr!{Z2l9X))0zpUw=Jnf?2Cp<K~fN@=Un~>2!WsP#;=Wv~SvT({z4nJem6NZK$4qgd#vaCKr)}x1hZ@ee#{rl*9KnW+yQxEHl$}z#(cfa{9ms(Dz+z#@tNOWxE`4ceqk_Y(Z?|=Q<FTWo4@^QNFV;KVHS9>UpL)^!^>M=>)BEmneeu4pOKrwx|t0oc|@V(e<kjyC>y3Dzv!SHZj>@*i25Oi!Tz&l)aKl}E~C3|rXzC4=NZ>)QS$EYOrlG)>w4=rKq85)`-YHHD+rX4fN+E?HEbG;fuB+8nB9o+;K9Dy@+>8SIlZGMRWV*L@d$2Cd*Ela7KV}jXjoC6N7$==*e`NVulIOQXeh&cZGUY|bu7B@`!Hta8mZ6FuSs*X4dv=853I@XARVSiQU;(P0TgXHO;9iGA+tM=U<Ls~^zgQ^|`ouw!4Ta)~V)w9Pm*RcjS@*jVBfBz3DCiu81cTsnUNJ9Wjdo20qA1BU7TiCZ#B)cC>6l5+WlsZnVJ(|qLdmt<Rn8SFx`44SO=Ya#5k?FpWJbR3Fa2w05q~3%4{IQPhr_Ja07+ryMzVOoK(XAUSjZN!tj6|L@cyKfXD^iqP1b)<bQ=xDK8w&sn{%2B2^plO_ApL2ADQy-OvF3^`$kO>^Q?5n0#!Pb8KX3`r@z_*G;}Ju@m2d}xbe>ZiItDYTa)2vX%uECu*)fhqJY;mKbCjdoH3A;ju_>p%lmHvQ*99A!c0`cWA!=K~17nOGkxV8U{??cADpO-@d5azh@@yQ=iDGX+;vICo#G{=GWNr(FjYPoMw>c2wWNYGHB21dH@~fbxd-*s!Qsaf`>#1~R-n{zKLce9#<(Sjn({~chu=Y1e>^V+D&nTjI3DVoG7zOy_lZ!p)#D{W&Jt^2;rMPoPr$Wt(7U{GOE%DBev2<_`YN=kHgK`{_>E72Y1HxK}kZp~p+|%_O*j5$>0f#@!Jhd(@RG><Hr)hsJD^>Az<6oZ#w>W3X((8XqsLF6v?$1Ad{Nr7wQ_e?k9^JWcb{qZ`M6i2kq$J0Zy)nx<ujzkcUWB48jl|{>{F!qP_w?WpuoxKZTEU)GNLjM4!P`v$md7YJ7pumJs;Nu^ixKkPym7%k{(;V16Oy*@DKQ811N4_bicG7Tef+v{PMfXN-CPF4#|cBvX|><f53mc{LzHnKYtILKF-WRtY4P!opSIhSy*7fsnB_m$hfQn+eM84gr8!_kW~lF#vG@W9Cwkdwp)EarjSetD;UNy{=rHhUMUOk&@?+N}0d?+XH=4ktj2R&m0B6m1LI8A{FU<PqC=q<%ycmda=J92EF42Uqf}c$oi3BK<w76E&VogsggBc*_oMnfU+bQ@_e&4Y_rS7TBkiDfPmDB95YoWkK8s_2)Z?FdoS5IX?GN1;ux(zHbrq8KBElIY0JvZ`#Q*yHMT+c0R1XZJ#{s?Fxbze)$5|jd(GD!|rqMR0QUAuYA(0?&GhX<g+RaK+*ns;nkld5RtAq8NZ=zga=!^-z+f3*=KQ<Ib>W+%O(zGZANh0FCh>g`tAkm&x(3bV~D3JhbK+Hp5!8(&x9gHU;P=Ma!g5CJycOauL6nZ|b%$~21x63I*s!_dgFCo=b-LtTYpXFrT?hEa*A=_L03C-Fp#j#Ai%)4B(k-{3jTiW>WFGq0<PVTW>!k|VnwyXn?Tb`pCGU`5`CP-+s^sgZ;DC=<eiXvITo=CrM)TRz>EJ}V258Ord|;#I}QPPf&TF^$1Hd$Zzh=<7AzBsU_FF<@ziTrU<3!gpcRQ3Mg914l8e^>kB^YgsVz?@OK;AgF;0o$54<uRbp8_r57p17HGZsu-(M*<s*c!1S;gD{(mXF^9YT9JMub0pRrHH{#`Kcnt`y7^Ec`Q;T}4?6Ujy*=e}H!G`H8W#^H(o6L#MauYrl(8cH-kN(mlT~O1T#x(KmXbZ3qlA~ZvBQ&`hk8Fdpihw1|ljUl(eAr6%*_|4fj^qc@4XCeK@hDDeDdVc}mONx#EA+MJYdI|)?NQ&u(#ZUsX|=7-3t43IL7Wsal&SSXJSbsR<1&QO8@Ttehd<8gRueR{1dAz<iC~5<oWIk2bNdJ&Gg#ySVZ|HAnjgcOdU|WWV5W&@3Hj9HfD299qzC^om!*s6H%7&PU<|ZuluCG00~G-*>?8`b-8UmO9<5cwf2%mz8J)9yG=Zm7D6-|t+khtG@^TS{hB;m>u1U=hmwK6B!LO#{Woah#QRiu0d{T9rX<DP92+aE$crIIW*}rC)HM*yHW6Wyc%P40TYuUf6JGg-F^&8ys7Z{q?l}aK1%f?qz%3X57rq{C$Zr(9I^sx^%N8dWR(A^}9y{-Y?gbqMz%HZ%B(?PY|DRGYwxQr?X=Pkg~+6N4CC7iYR^OWpy8<WJF-C$m<Zrb-0De37?r(;=M!R43{h`=NY{0$}(jOP9#F=DU!2?XxKo-iJcoQ?(WWS!Q{j;ab+URLPOz;mvP)H26km<=Y?b)vnHq_{z5Zq~V{`&1_dXSJ>fB>qazGB?~)@;f8GmcvT9)hvZaSu?mOE=i_bL&5u6LEig~lSHQrG=O9&mAlGf_&tSKLfXQ)Wj1)b+0HU8@Mo&l;1GACM^1aNNrfkPXuhOGenzrtTMDQ}hc3pf;Eej4S@u8v6y+Ah8LYi3Eb!RH)vpq;JIS08xGrDslH;Ojy47j(^OVRVfh_@yyG%-XJ7eB#o<f(!jCJ@(wJ&?zd+BY0z7<+}io-D+xB5&R2vI67C%P!WY=YM$`<$3i({(08rI}1;1j-Z$N`1m5PM&t=X(l~gFfES?*qywdnbIIlHKkjnNK&}qwHXXRB$+w`rK2Zmy8FE&sS5V2@7#hlWRe}98#JFo-%17!W+>U#(ML6qx(5MvQ?hR6YPnMbTa4$B<TDYx6y;-|9a8o)=UhKGVr9E@L`d^(aCLw@KrcfH)89}Lhk7RJgIjjYZF2I{=zy%0kVE$lB1gl*d4xfvmSMilHoTC7V`zTCf6Qv3&wNvgo7f(>rHwPdWClbQI`(s{HZKRc?9t6HRXVO#09d@F0y4LlODDiYIrHy}FlSAehu9cccoe}BA*t`E7V4r&(A-+Fcn_TSpb8>PJw2Wu-30i#aNxHBxcf20(XH7q;+e!2=DFe4;{XFQDisBXJi-gQWWvd?+t=!T9s-#yfR3gk+Dolt9(aMpRuzOE>_a@s(7QH5R37AA702)+dL&%u(Fk4XS)oY-5R|9aCvL(x^lgIbaL9@WCLF|JD4QFmI)<L6rx!#bbj8VyaUGL!RzqhLWx$!rUhbIVu)5)nQSLClZ_hq-O+404;Ow$=ovWLD#7*-w*fg|Nx>pH}i^^X)3F(21I0ikw#y<L!{i;djL_j_{VmlFek6E>MKKG1YH59r#lk#)J>t``8v7{FfHs+K?JQ05kcC|N-qPwGIq8+TPE#es1UP$foBu47;Wwm*`J%;6H=2@n6MOILPAt;N}%RMM_!+$3M)h2Bp^LAPPtUYW681Ps^^TTS9Z>p51%rTu_`#js#Wtx{{`iTztTnX_!OE@+a$CJyOKww#bnq?`90O*82pByQcJ?NB7rcGH7`?Hnr0nNTa2eWmhCAX=Dq&$w$-UF)$mIqs?=#%3909lG012xgP{t3HblW2tn6}Mch;c_5?e0Msn!rVe-BES1fp&Kv@QBe2@YsD#00j?QsB*BwSp@44~`ZX`3-HBoXgHTR3El$TI1OgZt<jeCi*<C9&9@D%u!RQ2OO(~OoKc~`5EGraL)pvWk2ov7vnCv~K#y$A|jc9PW*Shc%<yDE^=BXLh?GkQ$NZKdu3C9FW`c=U@F+lfB2sT}mnMPDi3rDm|ai9RduF|iX6&{RC^>3+cAlI;FjP;JU1-R?xrWM0(oAX$BAmqx3P)S|U*S(zA$t{pF*sO%Er!yuOw=xSAffz~bf~Q5YGypbMs3QbF<1xY2h95qc12WXU{XkQgULKCDwKyxQ6<FkY^8UE6y{2f>NRKDD4hijMMxa70CP8euPy0EaySnK>Nv3s;u?vK54x_DMWz6S4xn;1t`95nGkF|=J^1>)k&q^gt+k)^qvznM$HHrK#Ze=82(~Wk0dS2%6v%Jhr=2u10Vdbz5#`8oQD@XU6%sJf{+#@^?l{!U+D?H=ZEh#l+mYS6_P@I~yQ~)0?EpN<)J_FEvI&YJ!!j`?9G9yn}#Zt6Qv>}^H|Ei)p%&p7Ha0G~_16-Up@#)FCyyiShM=h~Ox8DQfe3-wrPkrh-N9O+FtguNcRc!*Dx4oW}uR4s-^<pIl`8=J@%0BjK&&dQM87@pYzCcwnw_@oGJ8NjD;hWA?do(}LoZO4;oW#-r0LIKlDFoWdf;uWla3beBu&)IQVym{SS_q0Xw$a?~ikXFrH%X238pAfQ0Uo*>R!nwD(h6kLy-JnIvF#${MFnJ++%K>t5&Qp))G_TbA$@fuVp$A!X`Z_=l2k1E&6}P}QOxJD+UO=Nx9L@FNs0w4u=e<+(qrT^O+POsGM*V+$8QbP7TIvYNnJR^+{mR@VfR`3?T;|*Zp?SJ-7M1XMu=AwCM7EYEVo)?996{ScEBe{l_Ah_+q(hyI5_f!r)kSyrC<3i!h2|HZW$y2a4*^#ZWAL)(e>BUq&96P<m9`9pnfiL0z^LdYdi9Xq3J}4iFHP{9gAqi=TWykvXFKWQ=9q>K;>#@5tj!y5=spgK4qBB=}N}MLOThK#~3DxYJD67T|1x_T=Iev0~zL0JBvfDqQg?|PxK2YbrStN@FYGOFHKv(okv8~z~FYvuvL=%IN!z1IB<@Afhjl5vW$bPsP|%vKMOVSK~#2q!>(*@4#%;RrHl8+DNuA=i_kQj99=S%wHw9?`h%sYO@8ipq^*-r%Q>ODl08MjI*>M7#c}Y5Ecn@_TYDL|*P3*iH|*!s&6cKtt4bPW)nX<IyfLdcp9>raV@I1y^>faXPk+dXrqcd16NTjTc^^Zb3JMl|Kmz7?a}e|~#HHKj$Y+9T@yMSBu@M;ly--?9@hI<U50aq&Qm@&39)!&;R#Hrv+G9`BE8(v@Myl#ds8*4;<}<WLr~Kq1l^9BgRCejpI94ol?rJujW$NB>2c<70RsO5PhISrs*{~&=oWFcwoC^mhKP?rw0MKQY`aRG+mNrbPDQHTGj)-}xdd~CuqWbB(LActJAt#&*%Y63{LlnOu_vZBHvx}C#N%LOoxn#;~fZy99F)Bq^M@@KHZZ1<1zyo*4z!8i}qS5Fi(Jl|~GWcg)gCY6}&HD>Q%UEY%x;Udt>v#{}6N4;Mk%vk3^SeFpbJ8i+2gv?oNw$iv173~U)pcMEt~uEf>&=#DVCEpHWm#;(72c~yUW7}4PJUDcl?FQUd@Gu^Dn`Z<%K>()hTS!vlsUnbzjqhQENzO%hX54AE9%v{ERR`jE?J~nZmbkh=xWLm{o0uF{PD6^@axbA0K0^J&sd}2K4d=Xrm0Nu7ONLsZHSn^d?-`5tLZ?4i~krLa_-{YIX_h>J5!cC$r1Ymx6d!qYP0MyxSiNNKi~wnNi`{}=^yi)`gGg53r`W23Lf_^Rkiuf`K+s~L}+U-3wbfZDSM1p`UOvtlA&}LpCI_Ss)U3m+LF}z{GP*yHIz{?xg)%lf6nwj3G;~NeXe0vCUHXV1xmws(PA3Y<Oi1GLX|RZBkjZ(cSW*{ur|1GVFJsQTn-mt&ME<^RBpzmWn@aVEn3nnfeE&iqiboo--L(AU+W4E1bhXuMP!oA$Oqf7S41>$F&*QA%{|I*O(QQxxy~q{ft8pYB3iQi$4E=4-_tgo|HT*AJQ~&o_&n!lMdhxz1f5l~6K-5j2mPya+ON{G%YAuG7u6w{sRFmbF<I-Gv#0mvXVmTQHXuT#4REUT3;K|>XfjbKnomWotS@w`K915R1(hkX9MFu0b@KazM}S|W+F1@K)iF^C+4y)D4XYn{(O<Cfq=LBiCCGR9d;_<eJwd#svWp%#o<^2Vc92KQu?=<%KrvIreq;DDwH0(Q+OgoXqZl3gdI{;CT;$UNnG!jtd%JZ;`w9R-i-0g7wJx{MVzX?1)DI{suKU#fUt1lFUs%d9$B0F@)wUEeY!<Sd%O;R7<S&<-c48E_x;zVQT&y_yy;^859?a9@Zv-1rr(kJ-3000S0!Q%!mCb#e*v-dDQf<M40c1+tsR`dZ%hc~imB$p*F5jOw(sKU%u;&NR(SD>-Q`u8%D{rb~h$^N0{`>#)$CHU{G$2oFa(qmJYtUEz^^tmm>He}Ajg?^gDk8VJ&Dw9gKF+q|7-a`xIHeiBo~JW+z|t29eTILd?nbKYadT$hU_id3-jp*FSCQ(DtvUEQYt--9mx`I7%m%6l44lVWYPvi{&U(A-wtIr%lvnf9L$jH}xjEY&-_d);sL+?0SNrg-JU^+oGgc?}B%z^qvd-mh3WteuAu(FufPil)BL<W+mVJK}c=tVDDRG{WL!;K)OZ0h$LcEtbTyH}WZ8zpIydYwRslz&^Zg!`cr<O)8pS#{hx2-~?o`^e=>llqL6favQI3?9G1W{12?#grix|yqvx?9f~%!&z`NPQHjX+V?qJ0s@?iN5t#>wZe?aiauQqZS0|O*j1~z$c9-zuwkfEg(>p(8Zjek=)20+zW7Mz1>~2fT6|bY|EF4?I1XOn~l09X+7CO3xI-s8qDW;dYG!ckaw2&|Kw^No?4+K;3Ygc`GmMh!>vzT(^iB9PMF_O(+8s}&41_%$Y>`c>+EuyFWHz2@CI_-m~QT?LDQm^eX1;b%$i4@4d4ej53d7T>b_gEzfZ;VbjWZ#UoRd-fH>(2lPWoWXEb~}=e!hz5=He&X;FZL)zgDlv=L2X*)f~7-0aK(QYz2;^tpJZTU{_N)hCW+q3@99E0_TRvjVeu4P8B{iEe)2t`T>ZJTqrw)Dn8f!1ou62^eihO(fJ~cHqi;VjT~~$aTDR)De*2P}Sx|7&j&6B?oC7Ud-`9N|&UeEKbe{MVMK@9n|L>&oeiUW=`*EU@m<xdTYFV9s9WN5TfkFIQ^f`>Rm&@MvuJ(+~s+}feDMfhzOMW)9bjHSx3b;W-<NDT+>@3T?Y;hbQ67#&xv3k9?aDSpM5w<vyXR2n-VUh*-H2@A$K1(cZF8L8ox+arZ5FB-C}IzlJ4L!-_74CyYdZiQ|OTf6wmP3FV1ot(~*2R3?NuyssZx=&!Q~C4q}5QMX$pn-yE8vv1vI%W}Svk>9N??g0gB*idv;>_@WcnXzG%|=;18tguS#kk3~+O0<|PhI8A=z686DM%+MUu*;s#?z&M6)h>{`0LQ;6Z*(G|6rULS%MPqGv-Ksz&#)aF}h4s;cK^jAj;f#-_)jw0{842%ZhohdiHu{F(ZtJ5%7H#nwnk>ilUfW~zTc7#@$Pf4iNd%3WoKz)18U{R&>G87jj6_<*u7<s<?bLkpld4p(3xZE+YC%lZOe#bq+;UEBu%+5d9Sv;zXk8+$_syeC5KdRr;GYw%9bhIM(9m_RG12o#m1_gMGtB{36FNpZ+ajqSmc1fe*hvn`FtTi^mqKf_pMz2V4$5?1Q}JWmGA?Jv)ae#xKMxF;)9s3M2-f-jTF-0!D_zFQrx1D|p&0TytLPOZJz!uhb0c0-1xu`2w3zoe%N0^iqtJKj!=at0yx~dtC>8JA;}FAE?duE~Ds?=Eu9*vbC$rM(o$GGt)XVL5i`bv*Hy`%%U*A4vI#Oo$wZiQFvxwbSr<XHZQgF5?o{^S|*x70yr>1rD%FMoLT6&h@qUn$GFMX9|VAxM5afJDIiRoc}AS1W_ViP-If=B^TGl}Eos(`r7&D6bt?Ht2EQ^dy#*WSQPV+QSlzW?LzvLwa`Zt@ax0ShKhE3L>_ajV#h&<wOMR_3JJprPCMXI|gme*Ep1-+qJ-Kbx?9yAVdd|N7(a;q#xBFvHv)ndR#@gUvqHT(WXTJS~%TYmLA;ipLK>ejS1hzIU#-u~Nn+v}+4@;q?{YT-K4eX7P*oVflq=*Dhu}w+P`P|G)qK@Ba_GGP9}')))
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
