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
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U5_kBvLyCj_}mYb-<f(lL)LPLCD{adxP{dPF}RYhuz;|FaChG>_P^_#?#!ypaC39>$m-$Tm7b>Ou)8WgJR;o9&CUPqoB!>f|J%QO^S}JlzkTz6{`0^7*MIrfFF$_s%ctLd`{s|AZ~n_a|KI<|fBW(eUw-_r|NO82*T4MtFF*g&H-Gv4KmYBQUthob{oBvqynJ)}>-E!@|7|XRy!_KQzg>U)@$qlNAAkIhm;LAd{QB$Xzxp5i*B^epe)IKXlpns1;?vJR{PgMT7k>MC`{t!J|NPruuh(C`{)b{5zrFr`9LJX_|M2a9{QZ~pqrQI7x(1Iy?|(Y}_I?({H{E~neJF>o+<hGTuD|^L!;jzn?aQxx{{8FJl`nf=|HGFRpAt^+$4}p0(fqvaAMN&k`L}5Qi!Z{Xx?O+!{Px4QpUMUBMl*oX7;9WVSKX2OFv>ku2GoH8b(_8ZcD;W0<==n0{`mScu-0<x_<+AG=+B?;pXU5aVJJ_YK~v6P+hlMEz~Hu-+&+E2{#yR@wh7938!%oou>bIN+=uZzzUncKZR4dgnH!I`e(#2V80Os={e6G@&T;vlJlZxsSJEciUwYpiVYss$?W~*T;af#hc>Fi-Qd+-vTRgK!>j&(<Z+n%%rfwJdegw`*h`!fsjx{B_C*}9MU%M`Imsn<I9Co>j-+sorgMDV}{{GwPFD`wmk6HLO{#vr$@u_6qhn*l;Sn#fX;DVA3T?Y_-ZDK(mpRFt?czRDQX!%vC4<;X1{7~h7YHoh)EP|I9Y-9W!l>>$UWDi{EJUoWA{x{)M?Aw0-+x0&wAM*O+kJoQM|Ls3qfBpQ!k3amc<rR1TB>0P&7z2b(&S!33NAb__+^ui-?pI&#-iCSY&Es<YRPONODJ}hX#rg5vS8sLsOr5U=Q&#Sp?KIkW&b>#43Hsk-R<iD1d3?;r3=^E+Q{%ngH1D?c<k3EEhckDzbM8*qIr*+nzLizHE~ob9$uFJV;s1Xq`PcrXci(&Oat~3y@V%uFR%~PT>18oLd$>GjF?yHT_l1u>Letpig?2#}xClE>FE4_2!tu$gxjF=?)dX(hxzS4IO2YY*t9jOCq=OA7j}Ue+-0cJZ`svsIREKAfRlZw6P4Fcx_kGwW!dQ79cJPoA%!WSlN%ICy@8J#bohg66!AsHOTu+Hbx-QKzt;4Uj3NxX1Fu)JPWn~`-(EimZgnc3lV8<CcBIJ1doe+tHYtlU-<Cw@DNk63?4&NIIUSxyeCo&7!?@Hcl&-xw&6WIsG`=M?dz?G4CdF`6p0YBE_@W|9XlF?q6=sd!r(OY-4wC<10KG`|qcQ%dI+GlT{6~ogi6XD`hz;cO?pU6_zUAM-;FP0O$5YP2X(A*@GNw|#MK;uVH`)r6BRyjhQ{#87;4LqXG^N7wnmMCtjnSbDqmtYcn(;eJEKN$C~tMDM07xwsEmogN7zPvZv;(|mZ`L>E@A9!uT7uC3N9^ohL)(w9G;&j%xOZr<M>}FMYSNGE^p%@`VX4lwH-qd+lMH=n7Fp2N8)`3po^GX~e<%0kaq{6RCKQ8w*2d)VBs-Eo7T2I7Fo76Zc=ozOOGc^@Mf{*)-(wtiDH37f?VkKZAFVD4~!%m_sD>Ws>g|KJPu@Jz|I+4sIz$N%10q0SYuk7>Gf#*^9#4HF*X+Q47>XYyJ?$_5}vYrVD0fu@wivywO^5nH&A0C@?9$36Rh4a@&`DEvl!RH|AO~E;@O#gwaW&1cdALrtE5@dKPb$9<`yF}-mRFCl_J#A!>5jJw#<GbHOb|tFd{ajca(^(&r=H}#_{oUjJ+vi_D-Trd@_1FIlY#T)e(f6I37(ge21YCkAX5r4=>@{EBj`;qR_<(W#;?+{C55J!~`1?K1_$ca()UT5AtzhGy0<!ol-Mtaixh)LZu0$+73)Szq)i6(Hw;?!L!Lf7ZbB@4QmDCOj6svKiGl@m$DX{0=<uXfa`q*`tGzqEG#rW=zq(Hh(9kBZcyCBgE^aRkYkUNL_bK!bJc@EkBdNh@j_P|=V0j!AqZ_)H0KJDx4k6<9+rrRLu^$+j>b_G+|ODH3LGAKV3x|aZdxlz80%7h<(P2XEP<HyoFQ;Gbb`v*9=gc@?Z`OoX0UBCZcqRg9Y21pB$SX|~wD~_Zkx3j_Ay)01U3<C33AmSgYncr+K!_9vn2o7ZB6Qjhcq{fVIS!StH>5zNzseSu@vdc=#U-x#`2+IbpErk+NQKVj$E7SPK4ir2lC6Qn7YEV%tFu{EV`{&o6K7D?bfF1z%)AUDJ#u``Oz<JWc9NnL2`->}63^HCYN#q4Sy4F}(5XzlanM$KqUfC<#tpRe~cr?0-q5}|#)2l>tfR2~6e^fh_`xzLfvxAHmM2`8+t<A-btjv>!zB-$z1S%Kj1a#(E=@M5CxO))crRF5J>Xy63x#1?$L}`AL&E-9&D$%2Z?8muq5I_C!<A40B(R10W^iZ#t;p8V&d+tB5fxVkv(`K{_is4R<UeEps2yP{!G_-fWzC4`2zJ6t+T>hv5<&E2IBTD8R#^eY6iA6bAvTi9z-h$@4tLw_$fqd**yy~GZ4{%QGxj)i32*jd)5$8Vb=7msxZ2)S0=x|NV>s;9Xc80a6lwyV&x!zfD8y`w3y#0WdKQdXCyLsA&(0~5ys~502*_u48vWV{<fv8JW481?}Oa%wlMjT41tDY+Wh(SQ&-NxZB2pW$EyhLFcec93YsP0(oX|V8TduQL}VMfu90xL`p-usP!3hvyxd@Z-jR+0xF<-J^B9?6Ol7C@m96%R#zzgEAfsrP)*u-wAf2)L*_s6?VC&bNZ$-;{LJru6moJ(BbX)iB;?$7g`MniLlKLY-Er2#$bk2TCcktvRJ_!C*-6PwAH(IqppoP5|PXB$_02dS5q3tT;+XkbvA7=x~)!9XM2+2zDklT2p+f$+jLyWHf&%7Uh_XOOw`uIE44?*#!Ube&~EKy^<HhLHYfd0X%M(HZ_X7w}!s@kyu_I`1dDsl;R(<tLw{4#Du-%<EV!}+j;8ZJg-gR0%+gJ47=gc<Bx43B1M&qeE$gKx2ey^*h@c3&FviVBjxqCM~RmQFeEd~a_4+bmM#V-qab|okOnN;<~Fsu?wW;7Y%C1i2U806*m#ze;EC`$jv1gQfEBe!LLAPgl8^cF2%TwZX8|q}Pia>fD*^lPL!qf`*C!;!I-M}?pj<K;i=_TGD}Dp?yJ+!BOtoh9>>=6H8GL4}=w1dzf*bN*M#AGC^>uk*_uN_%1lm38SXlN9-eOE0z5nO;?RbXpu`iQb>@ZQL_H03o$ObPNuK;b7B+E{(@E@6df+$Fn=K__GM6)a;$*Z(uoY8dOUS1#&E(IA?sAmp6$i#|B#AfspV)A6w35NP4>PIk(6FQ19WB4U1!9u%bbeKrmV-2sGBs<fdJ7FL#<4c#xVNF{0tcI~%A_e?Y8~xi|iKD$h#sgM#M?qkuJIw>VBZF05O5%{(ASsGYEv}i2?3B@f5EwhmcUP>qB$EO127Pv!ekfrjwodEQt&$vX5Cb2n=sg!g<wp1Z5wk!+VcK0Pj+V74mX8Ld7ZD9vY_!9~i2Qih-taYRYIDj7l0$8;6t>JU^1_pZ6_7z9TdTQznK}4Z^Y}-Vc}8zTTJuYNAH?OdSQelxJ^o4Lb-U!_PFO|!C@_y8L-o#EnMRe3m{DLctI!pc+*1h;G?hl_&LLhbVVd|L!CE|(f<Uw{W6HOm>lBl}47rM_aDnanR=xKNm<yE)s{QmXH(99zkse>pags5e63*ZyDea3tp_H~FaU2T721hE>UdH%MK~vN3UtfQ_N~$7?$Xoamkk`{|SmDcyYMB0BvjI1e0!==$U<n$eIwpd3xs18@MLeM-hU>XmMGJpm!a`nB9xaF*<;t(49Etb4_-O!2ED=wjOH>Oxshuk!3zzPt5M|fMpisiHSk1#=TQ2v{Yw(hz#nn+3atWH2?fJ50$pX7LMqj0?=g8*Zbsc+rvQvg=222+S{Q><Dpr$WY>u)_N{d)Z&(II+2IB;h947DeMN1|+w-IQUQpa>j|nsV8h%0sz6btXGVZ;8fLdv|8SNy()Jmj1QPCY-C1xj{tOFeBpJe(z<v-@cYwP+{y~>0Rq8s=k*H_;R_IV(8pjeI_{|Duw|x?@=z5HME&s4M;0~1t<bPteM6N57d2jybZW}q~QJ**N-ZD<6byIe(Axl1b6)7V!RKzFhR=i1&~cN0~!px4Rxumz_6RY&GT^^veY=N`~?M+w5jX+$~~bj0mLdc-{@2;TM=dh{&{N@@)x-}N>ZE*u=GvIr?h2JEo<=uXWgH!erK(zsSKX^Zy>enC(#bIq0i}Vt^AOyiVZm>=G6$01E<2iJq2B{qBP_Kv$de{Y!+zq)wWjrO3|v4MR_PC9ptXezp(BFN#VRO3Gu$9ZJZ*l)8gFUu;7J{mHIlL)e~05`Q(|pY(6Dm+gSARfQDCYQGvxTs=Cce*ZP2&*)BOzetYKtm^UgaM@&*zA40bFj<({>``C<|5g+g27|qW)MxwqZFTZw_C0Q{+LJdqcGS;9@hifUXDNMuX>T~J~H9*{ma0H+{Am3#1OZl|w4S@Pb#R#<7d!SkrDp^<UndXy%kULSl!gN0nq6C&Bq?j>KfcNdQH($t~FYoLmaqm$#r~w|41R54q<OhZoBt|!X(i`1t$^<iI<qcJ7EGb!6UuMHf7jO<kVs?nv#2NX-w9cNz*{g3m)|1o+8<=xpJ-@u6A;XBp3SPu&{aovdI4A43o_vXPYIuDa&=@=?t8fb&hvCcL?cQ3`)|SIdZXvg*0hDYJOSkHL>oOabP?dFm#Cf<eBd)>Bfp$~LTpCp*HC28?IHqUshCKgj9RCCY7Nol{4ou8hLcd6hI#Vezrua{#tb;>RQR`^^Pt0opFHhadST06H;s#kY{WsZj<7Aial^>aSLn|Ah+F49<7gv%{#Rs6HVC>KSC!OC5O&o+Xv~JEaes0fcbR!#8==OqFlk`Pb7AZ6)c0b@=K&o#}1lW%PIP}`0X*?mxUGq{(cbD)caz~rjh6p0#ZgIf1`r4D*&+>bw(yKzTN-$s$)H8P)RXXLH9s`=Ay<EV^s`}M~MUjosV~8e-=sv{W0MwzW%SHVGX!iXQr{5o}tmie|je=QPl@w}^xR6r=#gY;<am$uq0SOZ(iKX60B%h(Q-T_X49f_R@pxP>^i=f)Y@RsN_unbvUR0U`;QQePzG<`-xMUM`UWFuOXF&m_^gGG*AqO>PIUuV?SN3})uRT%IBN{-FT`-cbPTQHBWgPdu839E!cxfgGoeVQ;36+lu654zGq^qzBQDMLG`0r67kl`b`_8bK7v;5sD)uS2@v*u>*NUgKI`MD!9+YQb8{T9e8A(-^iz>6Eu13RCG@ui0nhu)JSbIhl9Mw6(GAofu+GxMGw$PsRFLsWN`TPGPAT%8|&FfpNALU{lIT$P+?3PD>{sU6v=dx`AMohK>{_MKlY3nrKGFYe=6Sqed>E8tbx^s?B9th*PBpFD|Oe`yj6#)63+Q4747Xl&OYig=Np=bWm|OooH$vrI2#9vGiI>K|Cyrhx&$8A(33OrV4opw(y$V=@=_ztUgvM%yT=EnorOj5H?R}|45vW{7(S%6B=n{&WNJ>KvQXYzlOSY^-0=N2FxJNYz&@%yj+Jp3gGT`>y+CdH3fg4SE?skaJQAkd(bx7w5ie#(h3f7!XUxah3{|FDdNV+Z8oK!@w<t7^$k6677}Cdlu+eJTH5&TFfdLNzr<3Bkvq(IJ61gj1cFM**L#dHR<>+==vzuf!E3JG?pUG%jLf31)>2`WL;$9Nsg2m!RP}h9LPM=Sy>LH_Csdh2<{2nNu0(-CG0_MVJ%5s-DhloJ$@Y23pPck-Sx%Gd>`*8m*X#ssV(8%z-U0x6!wXaszXjwIjg_FuE(-oMe{%1urJWhE4R3{Tj}Fg79qPp>D{9w}lEC2Q>r_sLr9?s_OsZ_U`_60<{c5rwrbt$n30#@RDs?1%mI0yUX0bC!;>L|In!6>%QfK6eUVB~dMI*Np0O0C}MR+}5-5VA+BG$ng@<ty5uI7&qCt&CQC=p)wnee(B%j`}6cO+$-Vr0M=pt4V_<{E1V;4r$cl8f}!6ptnEMv+rX-7;ySO2sVBv}HQoN>P8@vaDcsO;J+L<P&OI!(H9lca3onI+~>6n~lA#Gz&!n&Hcx_Nj|5+8&JVFdMr`XHL66fi!X*ZXikL%(jj16>_BvaqsQ>XggPiIh4ln?p5v4v=8G?}c69SHZCeu6)Aoo_X9|3U&gS=91BPaMTno@L_FR369v@RIHi5f}ZMl6L08vVSJ|U?f#TO@LObQNBvp&0R3_;q>olIk@k6S_PM@y}E!aOV?Qb1J#^@SI<9ER7G7lBJa?9+_xL#v+&yVco8L091U?uYNeDU-COqFxXw^i)cqL*y|X2AxPi?DlZKTwM2qB2^aT{`+P8kCOnDOSTv326Ac7#yQLyyaDS;gR8140YES9h{_NqiwJC|E0WJ@c0+zP)StxG95Vd?+{#g4{zR04OZS~1a4UaW{G(fVLAmMhgf6}+qS(Qbl5p8m$f9L9|3{Rf01&B6iBwsxVKhM*U<E~wO9gY@f}Dm-3@|}Y0!an%)Fk>+5z)vD&jNaQcCAqHlZlzZG)&~9-`xh&D`70)0|s42^y+fCA8JIA5xdDPnObn%cKk{TLsAG1Q!l89*r}-7O@wM-@p!bgEP&{3O+|H&MwTZ8yAd!t0?Z`NSb-5niK?KQ$=(Od@}2<a-9m8%?B+^2b46yO(hcTGRBX-iodnD*2F}%P)WKCk5p-KbbZ-N&^S}EbTHgQe@P{r~6IY3Qr6GG;VSjU!l^IXAkxIcgDuYL1LZ_4OcI-)IHm2`IKS7#-ZSIh*krOl@9Ah5is1H@!5n#)Fx^!{EY`;HX($_d>o8oufP82MSmclR!8Vwj!X9^9xVvGXqx-(c&7r8Z=`a{Tbpo>}Mm~40^yUEo)$5TS$k6g;2b6bXF;zEtrn0(@(?z*VX2T)L+Kuft%4CvU8_#Z?MkRctm{^Q6Wk!n8%iGK8A_~ED8b|`{|ZRkAF^imB^jY)pm(<q2B3{H^GWV(+0a$O&Z6?X=ZxL5NVj5N`?JAoruem<=mt%&~07j<&kJt@EvJd!mDbv-i}!fjmZ5C&J?&tA?aZabU~62T(FD4G?)O7FkV6z2M*07jF87Fx1lFB^#B2>7PV6zXza5mEQ|ol|lM`d$F{B&!G*IyyO22VRJoqnC<Wq|`CKF4-kWv3jN_$UC-Iwj{2UUH5o8Vrh_C*L|;a(pYA+&9j<INhw^{Q~H<;k`|`(3VL`4k<)i{3xxiJk4mnDF7AzVxb~1La6$=dQH313`hG7ARiH)9Hk*>6v<A5zu5M4I0aDo#D(0vIYA$9&yF6GoK5C_|^CeUeieML(5AI^vTq4^A5(Opk!Ux81MOMCn(DS65ym*&h44PSe8tt0f)^wzsVyJ^0$vCq9J)Hky|6@oD+WzE`cmO1AiV8C}3o8Wpa74u(D*!H7p$c&P)xr|Jt0c+dD4kLhoElQMK=aC>raluK=@Jy8<BgfvL+Zg0ax4Zv%ulITh!*DnAC|$&AP`g(O~+*21f-Md3T0ragTj%IO1RU2OB4xI>N_~mhbKy1JS{0VR>2;j5^Q>S#nQXn^Gh}y<jj`D&eCQy($U)bmAstlnGhD$vvzhtXbFitL_)7DiLMsSpqv2)vL)h$+w-;eIBLQg)P=WP#98CPuhSZblw@%1$(3(~(g-Yv!P0{7^O#e@ch?w3sFPW7m85fbQk|?MI}a>pclWzpCm|-CSY~H?aa%-Joo%58DnPK+LYvCd%wDIU6BuZbU{Me%jrHR6YCYm#LU27g;G+sS#}&r_N4_S5ZJBS<rDUq(Y8TAa0#_H39AmIpCB-smP6=sHUV*aZdzYXKuD22tjveo%5o8(JJ)Tp~^(jxV$o+hU-99|wIVX18>GhBHIyqY!%6}3_jHmQb<M6VKG@|<Gk1eT+nu`eZ5eQ=NoCpES4(&vVfK9G8%s`WZfQzKY1?42G0(V<lWr8NA35oO=(Z(pMx2d`<>kP|s474*jQB;o)8IWxWTwpOh$%3BKWm~LPJ$OK1n3eBEvFl27E&;<T*h$hbkf6~75K~N;F!Td&RW3)Z77E2DE&j5EPfPG=P&)^+cZsq|&#$O*e3YugJ#$bC{tzE2I<X%8Lh2YEp5LHgF+-~3VGkn;;Q<j*=`#fcp-KX~88hu)<&IP-UC67@B8!~6O3mp6lufXQ1ex3e@3Spa4=3gtNP7hG@9rk#SP}bkYvRc^r*^}-sZl!Z17ijz*(UQ<EE~_LF$h?zrS!0c#{4KG+ZNht2$t2e#MrTC5|=`S84{#8qsZZ-LqMvXN6WT1n`#1cqIM@Fo>}^cA5;Pp&Rt8C7b31()I}iOSmn<VT%kQGVVFAdG8)!)l&h$y9XikG#J)HR5Z=~=Dpjt8{7bZuPDJX)?D@W^x2wQ!k*eCM!V*m;6Zd_Ed%{6S{Aifz4QZ`_o)<YdjzjAxmIX-`&RJzqeIV$)mA=N;peGjYi(q!HmsS&F69;`qgsaNI^8}IHa@Wa^J;jF)h&`cl93|l2&at?p+<G?3hp{kY5#%{>7M=)L+azSWaY-1N8&!=j$jGW*RUU?+b=^m3_A-^nB=!L_o3b*G@nGr#0!C%yiCKUw66rG%G){Hd<ST!q9?v0@)61081tCS1;DX1H2_-ayLP*LjQ7#`|4#>EVI22|SPfg4+#=iQ@Q<~6*-Q&!0(<KK1B5~;IAM|mu6SS(+h&lm>L6N{V3ZaE&#7nKD2daZW`iS{LWLI2?NCGA>1Iq}SQpI|y2Fd*3YkMikdhmRfkgQ{Xw=Ws|j4DWp3aRiy@Z)S(Mxyf7MlNFEPXYzku^qV=av#wehD-yXrvLku2=VSST-Zb4Vq|4kV)2<oP(y%P(#$0yZ&PRPKDj7_2`ce@&6I$)oe2oTPBf(GIJh81B`g(Hx|gx{XVg|IMGv(2Tgh!7AI%(ekP#7pJHgs(#I8I!XX>}n017#B^;sWs-cSbBFrkufeJpaApMiQdGpEjr)inaV`L{Tq*jxF&?t&YP3Dlno$b{1;m|g@+^t$cRYuZc!?9aKV$aQ>s);ZC*CA5&Hie&Y~9wRzO0;A$KzymJAT`w`Zt=!T&FOH-rd7JD@j<Ih3mH;n=q{GwbgrFUz@k_bwk+8AmwF^1tPPc;O1HuuAsuOL`MV**51AT~?@DnmYb?u~8MjS&VjVdZX<nPlO#A)#?Jt~VC<L1~t6Pd5a+f3ubtLqGFU5Q9@ui%{R$S&(9op!mB-9yMw^itoP{?faFwNE-X5Z{TiNlc;p#)6fgB<-kXvv@CMBUHlB)}b*;&ACoINt#3(=uj%=Fw^0~tBA7wha~n&7ZzTKLMa=Re2xa>76dN2#x`<0X|-4<s0(7aNai7-ejOnglTQ#Nv{2ttJ|<TUORVupd2=kEnG9UOpNr+x^jaf+9ANsU2@#p)%RD2YJ6R+Bi&s|FkZ$KB@ft4XQQWonUk}1At||HVsyJZ2pUJ8CnbJD4A+2zW4uy{iRt9C(!kPRl6G2o^=vD8a%BM`77G0!>C-j+5DKs7RN*czj$H`-mI;1s%IFu4BCbdCW4*}5-c0BY_@mU-NK&x$r_rX+5+(Dw8y~nnw5cg-KeoeJV>IP8bP(kn{e7V9NZL$78?`dtR7sCl29H+@#h2GYuvh3@u@C3RPd_o!R;bv@MymvXVty$SUs3?^#x%J6G4w&3UtQ$Zjw<HvDLxt6Tk58=^QJ$hlDwJf!eT_r=BId;PGB9cqG2=QXJYA!fl8;=ZCPRnF{qh8SL#PRlI}SzqwW{)K?*#YU$ltgxvw(6`cUWRkK4WRqe9TR2$U9~zfn3{)JVXb?j{Iq=<cjI>^KLScTOcT5rdwwO7Z_u++<yu1Yc&FtRVn9O*rb&6O<h=77%^;7PO7rJ3@+;q+@1g<n7<p)$Zk0$mNwZYJ9<8&EePhTH@tIF&h|0jt)Y+uXiw1gTL~^%ocidh%j1+*iqZb)0lIWTHfOk1kNhp)IgRd>*vg|)pNQ4BF#1fi9aQtSy89zI!;eL=d=`=$2()gbil;6IHO+r0!X&O0^Tc}Z#IUTspuTZVe?~`}B%N*GD7LMYd6u%Y32XS8PKaA1H%NDQQ8J@!FM@sfWgGc^D6|%gp(BEq#9yrpjgl(plb#;;I4E&p3PEe4u-m^vGe*9?U-KUs9e<i}W%LQ9p<}4B8Wh%Sm&NwK_)LiwP@~kOOk0L+NU<#~rmsb0B9cf>8aUG?QE%P+@r{NE<tC7s=^W(D3dr~!G4ow^+NOd-vQiXnh38a8dZR$A;bm4p`qiwOF3!^eYBT;7za>bb_S{pQx%pIyK&#j-TaWXX7khc5=#R|@Z&j$w1spR0392eiW!(n6f$9P-xlTshN!=v@uxSKD^|(K7*j%orIE<?~Fny<*rYIR7$x?rgD_j1*G6!RSh})es&6$8Df_^;xRpeQdA5>h(ZMw=r7FMKoQ;V<a^EN`o=`5m+sMI|*7Ef{n2&d|O+(Yk&5>@>+=DEAXUaM8NGvfgUuse@*PlxHvP%A+i3;)P{L1}pG&g@RT@{aBL3n8C@cL9uy7e?0czC1=RaCUh7cH|+>s**`S@r|P*r6C&aM07M4r)C4&oKjiWdp3WuK7CtDJURyq(iWbY?bJTPD2?aDq^xol7*o>tg$a;{7*o}b=f9>SL~;Hry1M5MF@3RkW&^)2e)ZNasZ^JLk+B#MjIbOCIr(5u%YS+<rRE7gJwXx}?a%NW#3rV`w0;m4^a+BHjemq%bs|1YBk){-v^PayXg^~`BPZO-HZGBb>;*;#<nX6A^@_2Awmd`uAR(URwXHs*T7$2rqTzc^78$@iVYXB8UK6cy0mK?((5K@}{h(nE+&1X6@kZYD@k&Wh%RB_+MJOBvbebBe($W*!%%e4J)8<@GI3%w+M`QIf63}Kqm~ai==7TE7Z1TlBXF+G9tCR)nMXgpoIa^upmeV3CR(7Gu^K44u7j@t?)kzK$Yp$cZ-cMLq3l&-o7w}{TFIR=cOY@WkPl9zODBYhDF0lxFaKHJZr;q6A;qg-I09TJ%>H!3yB27TpG%V&s3M9MVvnEGY6^5J{yAd%`c2vO}q_M9z=Hi?N`QD__Tuf!5u^#)6;nbS*SZY``$f|fliFyqgMa@#Pw}#~o*189I+yqK=IQ0N_Hj%F!&Y;r)l-<{=`r795)xeS9*Pofy_$UaaIBa7?K?!~C2~`UnpvfojVqBmnl3bI7ReDB{iJp=11ll5Ehm2HlQ{ar-RcUPxm!-A{i4s9f^J$x?3qT?_xtNDw=<3P|EI=TjE!nD685k=iC4YcAj1_l$s;w;#Mf_AP33Fni`(XXy#j=!!3%r-A+s;_JF+xBN3?YeBq0tczS+`wVOvMKf`_9yeWYnaj1>*1nzsYdOvG<pft|qi21xbY-D{7udAQs?~kzV5Lr4N}oYKouf`&LooZ(4#gxBaZuFw1U6#+tTTAqN;}cn437sKFfLZ|zjw{|<@g%e7Z51c@q~sBmK@me+7jrf40+Lb=wvJQk)H7HyK~iEsIFD4SOP%vyIQiqfN!O6H|$nC&L)k`V8vE0z#kqZmmoWE*)gJXYe(1Fozo!MV=jH|bg-%E=D!P@O&Gm0x<q9{qQzi8K}OX@I`DP&7fVJf&8O{XMvPo?jZ2|LNaZ-)X%o4+!L8;2FmI8c^WstH!EYroN}O0o>?eBJ-256w<(iw_<`6m3lS|fBiXUB;8$zaaDPzx^rT=Ld?Zl+dk6gF2x`sc~;79SUAG|ixXy=V86cE4s!OcDjS@(-nrHBSO6QcmN=X0l8Stk9nqP!+|Fn$zkj4It*^F6Kw_wzgPmaR27S|&j*g5?8jxY@Dr4YL(^whcw>-jpjHA_^LBQX!S1wkqvi-BUcK=hTZmGIFd%#lXGazy}tOaxMjPgd<Kul{TbbCg?O@uVqnc6wa8j+i~i#?y?r^R>qpX%N?PFP7KGPtN7Y0*?iUJ+}#Xw)Ymbhh69Xt2trQ|cS<s|3o=2v8U583e!-Ak2vGTb#8b&8|->w<s1Ma987fWPGBqCkw4%%c#V@81|;Fpk`ATRJX+>iWM?VxYWxsnMo|mg7So#*su=NXLL^dw#@NG;r48~fU>>gKeD-((e0S(yYpwX-66?mH)bCbt(xOBb?f!XX&P{p>^`)pw)NCflu|`@s<4=sk>>0YMs2o~D-ic!^r<gQ&cT2QRop*``oMkvzx@8gkKg_6+t>B&(Rxl>-e35-k#*AYvI0(^$^is<X-jE{XUE=Q;H7!7KtzGg0bbZi@i!Ec4gd+N_-|S6fm*OjU#x_eM6^#F-l3S-Otso1l^kGY({|hBL-7DmqQ#PwP%OB=2b^rKG7scS+IVvNro;J;^m`(%icQI7%JptSfB{~SoD3{Wafa=JPbwsFtPA>g%RJ`to|I@G_Sg<ZYw}Xme16D(Wo^W1Gc*B^j&#amIVgP|jG-WOS!-G^Y$c5Uo6@8uKNW6sj73VTYe>{ft{-9eFF}bcaJ<<<^WNbwkVkFUpJ`lq=_M-yU3{xLk9_&>vkeX)4F`ncZFVT62CpRTqs~r|m)Xuw7FZ*1XlJ+bUHf$XN^ru!EXBuu*Q`9C1)Q6)o2T2GYVQfB+8+*o=&VZmM7~XZSv&&7*T&6BL91;j517-`<J%wZzYIUBt}6dHQ8Im{xe!~@Zv1eF=_XYoUK3uXqIYt4i*2mjm5VrkSRGQj9Wn)vsH~ABhF*YaiJf9@h3bCXyt08D(TyjP82ca~A|LPPEMgGS8PmK7@Un(O3m_KksNYDyA~QPT<Q8QHh-!#Y2Aik7bB0E<RB)r1OXL1hy`jZBE1A;^7y60Q6gD|D3-Xe{?~wgU?vjB&Ei{*M0<WwOd{jdZr{v;SPXJ4vgYB?^nMbzIMGS#?l5Rg?ZYsBaO3QS1YVJk_n$+C_rKsLXQn^y1)X`W6pwrxN=z&09pPqT2I5m#J?bIVIzyR3#FaAO%d-w&<GtE6D)SL@jszDx?+3PHd7k8N(r~Lp5AcFk%y~Xo|CCO89G|h}6?K7~NVRof@xr=`m*1KHBe+LWBbmQX&)f!&?|CO~52;26Z2%qLMC3J_Af)w8U8-!;&2{Sx@Q=Yd0AhfV5n=B;s*4x57NQ^Le>orry>;I3p*2lc)`yZpK{Yc$(uQ6mk&;`Z`09X7ALr|5K{}XPcy8ZBbVA(aYKQP?Z`9UYASijDwj}{K^AOGXar~g0y{NMlg|MD+iCi8FKG+)1?>HBJkb7EhfK{dbp-1I}Xz19#>>A;ExV;B>yZfNImv%Oka^)`q}?n~~?nSU|lXS{v$T-|vbHFZBVlqK#kSf;-m;u;x;*0Q+_eZG!wxWJ41k<!LIbFI@=Fjk>J`>sLp<ENj$yF>1ue*WR7Pj5HsU$56+-f^S1$uz-YvtF~VCP|<ouzq!mIlb>AbUR<8t+$wl`7|GeNXt1N$;9hqI$0?$dbq{1X;$O28zEZwUhlociCFI((k}-4`S-Yp2MpwR@0Xv3tPmqCb{zLE(D&{4vl&XU(A#iFc<`CMvIUabInxfukxfnk=_o;lLY5UlI8nVA9P_O5oShM2&{nVHa&N2XRiX)&`w!M2Y=v|nyTU}L3yU2u(Md-tjnSrqPS<IBEeG1DH^KfXAT`2|5rMnG?X+OGeQfLG?Ew{oY4^$Xi~G&*g3a$>@%CXec}JB}W45pZ@1GG<#WRX^sC|vD8l?dPcgo%4A&UF}->M5@I=jdBA5_X!NBs`I_hUMk^|$Q_`#U{hICXnFKdn{Mc?QqhfR;#$@0#=j#fWA<i0P8+9#x^-Q~e3v13WdVEG@5i0Y%7#0|vgkRmFSQr(5k7DoyqF#a*4`4*9Al_wT$1mfybK9{11G*EMOb9GvsdPPFL!vx)<3q4PAzR2RLE0mv2K&&bymrpU=O#!~fY=9F0s0sT;%R9(z&Tg*u(sL@_%01DWW5dQLoVaYV>Au~6xpvjMMZ@o~SBNfi6T=ZE`I6|NSTI-xIIzigA`LGGJ^q_>>JvYxnNTP7{!Fo|djkeP=xA~5$DEyE**&4B8*Ug(dxzT-jDEY2x!u9dC_Hs3^7nLjVF_W-oPWv3iA)qWk)B(|5^?8)ns0?U46hZOU<Gq{II&*?bgg{1ty@TbM^UL$BICWm?qbM>}l7@W$-sMvNy=<cK7dOv{Vsm-dV|~JULg&>8mzKW^S`}3`WL!Ey)gSfn&7>5*s-Y#)rAseML<V$dtE0`GNVq}U!?+BDR53;&oB8#i>8+MSyf>vUmvBtQc1-e%dS-FM;IGT)2X;lqaEUHrO`FUnJ-|4T%Ea3kW_1iqU+m#)ACrY;YadqMx{fEhnPKN=FkwA6c&ln_242?o5?${!CW#^&`X5oKq~_t<OY}O#;`c<?(<TsQeHQ1A64J=+rIp$B%!&-w<Lq3i>R~Lqz36#u4?AE{k=~<2Dl&&=(g#b*D%pUA0MJIROI=4a=%q2d5Xk~JDBmr|BhVtp0Cv^mBA_7y%O8r4R=MF$a;qDvb%Mx5LA2-f!~_??I@USzp;*z5*iyhL3)c*Fkq^J9Oi9X-qR^{tF0v92u7whnGQ$mp(R<r8dZQ7d8Ewk@O-2y;bEgX9yKM%oEK)<$u{8z>RngxD)m134NnAQ9F}n_;m-S>xxT#YG0wd5f$6lb+HiNvZ1UgWZ90<92AFIOAF575FD*xGKNXyTXWk4~~{Vtet`PKJwySR(TkS^DZP>6NBbAtTL7;J=<43LM_SpnxQB3psy88jpG2V+ZQ?I2pl^X+p)y1de*t7}8Jzx}$MZBv&A<f$HZg&G7{cF)^3?_UD&hy%~%)){|US=3JD0Jy?f5qa9zXj_NSS2o}g<x%x)mV0Kx&_<8=0u4yQJ#j}jR;cjNhSsd(pF4^vPbSeUNkk^sVa#WZDb+iNr}d(YP~mI0OC7z0X%i4v9CRy4byNB}<nE#edtil8zZsI`39@``*T_vV!J286HX;AN?POY24U?O!k9#P(?qrLzNVp`qPSm3MN@_C6!LWGLzV-P-FyzHU=+#FPj^QD|^&CYYMN?Ygdm5&g6RkP6*sYst`O0WjX(%re)Y)KXHHV8t55YtRby-!K^{|apPOpphS92xymrREF!<v1*4W&_;%Bdd&^*fii-1e>9T|&~#6LO=29%@sxx7W#0={O9urIT3U>&W^<w+oeAO$C1hhrZw=tRo#NFjkqW7a{75zW~NM)=CJX!Npo+H1qF8lySj1Q0fXWbtpeZgJUTfQB<hkxf<^>5MwlGK0GGT#rP|j@Npkf0K)c*oCpL1WMXPzXl9p>Hutb|d!NB@k!OIuk&6)8>?Ry7q&}6IJT{p}$-KjPX^Sd(%)kO;yeTPLyddOCuTY0FGc`8ZMwoU{u8$g0+M0XA^uUt^e~JD8yd<C-iEuQ@I^3t5C*AqXZ!;5C3iVinFuDNc*NL;MQ}}ERt(Ufa309@*Vv3LOeNIDV6C!^)v~mmpASpi9PQ~?Y_#@MVYW;$fB4|f^dDtYO_&a;7h<vl{0Ln^I+aZctfsrYBa!rFGIzWVTvJQV1gKl(uNlxPN>vke?qclQUSVu1t6luRD!j2=kz$EKrl=+B3mrBy@6I`6s(tWcY8=V?J6$|W1wH|1sz@###3O}?EIe@n977B3+i+eFy1jn95&zi?BUxY#bsqBR)b6S$OzV$XP+ZI$vu^pTllw$3wNDXF?L*yD30t%#EH3U}_-orC+FC&UYc!cAauelghd2Qh8(VAA1*YS%&qiId5+!yPR46gW)8SW7nbHkriUWm@$WH}r<{%f|Zv@NtBSanLS&^_VtsQu|Vo0qoKj8E5escGm!s|&10;_SClF`3%cLYM+f#vZEBDlJ2r=KHJkgYFY(Wz|XEnAM&+-nw2Fu8Zf;g>$GqQ9-RjxRu%dF7aG@8MIBPdhv=KRuPdhIT|BQgId>4-YK5iq&c9(ofqxV7-f6dnW}hd`T0sx3#O@3z9nEB5X6C}rrn-YDzY-os$~Vqw?rFiP%#wJj^rI$BKxu@gdGAF&n29Wq@B%?4wa{r1jh+j$c#H;UMba<3Uv@-OUYxRabC0@Y$t?6+d^K1Hu2&GYT+RXOT|<XWMX7pU}P{k<6{`Kc!=`mJiP&D+`VdM;JE-GN4o2L(9<txQiFV7SsVypi?T2+A>YXxF{*%Mgc1>~Orv4tr7JdeQ>dR3j$K01o+`U>A3GIs{EE9IWE{tj;!DjDDLLvHCW2!bYEL2EVtKyD(umQVm|{q+EZrb<ihLVj6HtKRq8yQvF2URIGx7w|*l_Yf{v~1uTYuzn#|3Or)Yj6@x!gRkyj@t2Vc;(+baMR4PNwm#!|Cf3$wP+%l}v<0Krp@`utr+?LGcfNU|<;I2iut#*!u&Vgl-{<VZ{wB173&kr5748dW}dF;SsVti=ya6)*&x71=wbJ=>u*23^R<b5QLG+G7>16N7T*~6s()v6&f&dy#|dhh?fS&To=H1m$nkH%vJ|6oAgbfQ>!v*u_LX!H4~ASuFu<N_=3FYZ>q`bTm;$`f-f~z3bm75D|Ih*u+!t&Ym)bmj{5}4t2oIuYiJ-gG*)7KPZFZL%%_ad7fv8=GZ@8EXIUVrE60B}EO!^FxtujFWcdDw=;OwN%&yRH0SLuenadamviy+y=-MZSz}<5r->&JBau-9ui%`4#<!B=7U?XXIMz~fAoZRpjoR6W#j|T6)<`@bC8qc=7p%PlUzbFiKs*r<v8a*Oz9n>|m+<ZyZO=JofRFZHV(UM04zyk^^Xqa?%(p@TqS2DdQnHVAq*Y;DYXc0zd(^PR?<k1j^P*z$%Xjj*^GOvYZ7Fin9E%3L-+jcs6iW7uE&4`BP#A`QFenZz*mh5xpFv_9pJ?Cqquy&AjHS@V;T{%P+l`n@MX~9qx7B~EtgAdnd4&`AOBMhBLV%nkRe3w;;iLPZ-44hY05LU6KU1OD|CW}zqW$iAi^^yD!e21Bw0;%D7$MXk%eRYj$n&`}ExT!5Qi5IhdhK)jzEOOLH-Gb|Yb)8%+q6@v!GNb4K`HQMcUeaq>QpOZkZm5s}J)Nmmm05aHR=bYhQLrpN<xdIXivYQsYNB~m*#lFzD5K2dA75~0{~3piY%-IYRWTDB-CS9*`HiQrm?T^=?s*&TqJk74EzEila?Vnwp~V&^^fHGJCgcGP7Uo#WNy=gj$H6w0`h?hQgCMO2-3*dp>oiKy%=Po*$0VV`!w@hqq%KcLJ(39q$6}dQkF^WeBkX$_{2-}onwvqb0V0Y<S7_Qeds#`it~SgN`UDdh^%jm2t10Svz@G@;jqUSAa2DJp-Yg%hZ=my24K#>VSlGXgXZZlb3=8rj0+1(~RLkb>3JDv{Y|$1=c!$t((eA|1s0K^pE(qWX?Hbf`HMFt;Gudte*zydoYso`*!jdy;5;drSkVz<%S~Tf6t+{ZlL6)ks>4rfj+tXg7gz3!=QykY0qv}}$^$la9(Me)J6+KFmTt1e7uVi$Yb!TxGcCI8e@#hjm?zF!tZY9|bi=5pTk%R=Kz!LpHiL@Jer<)iX=syY@DAi67j4>oq{{i_OGPecI&X&Rjqd&bGc~Q6sUEt*gO))h!v-hB)+3w!4lM~LYhljdja0)TYwHx(73}P`>)+Z*a_rXOI_kZZdGjW=p+6YL}-UQq1wC+Zeh}!nVlgI3HT_vQ61nm{^MC7Orm<I4bc-k*G1`IgfeXZ{R6iO$awfQ+Tc1qARNIdIh<j3$$jo^upeTZdT%8I3pyX*TzWFvx<{d7rp<V+rpxJ$bL^mu!e5GP@jAF7lHSu{deJGChrXBxef08iiCT!=e$wI;t?)4g>>b`Q%}QN6Fi?WZ&A<%D^xMJ)#!z=*&hcFIBug#U%brIYk}ljY=%wHe(#DT)Ek$#^OlBvL7~rkA{B>$s-Mh>y}im^34iX>~6^=^>5c_*_5@4=vVuOgvQgle$!(K@yjlaYw>>UUvHC%ensOl(9zx@dz`r1~WHmwLjy&f)TUT6<*7^J>Bj+$_mj(hu(26^g4HHQx*0_`P!6BdnF9UY$@Zp&x0|mBJ%K2Fw89XQId5Ac!)-s9LeUi2ffn0R>-`karhlu*CiO$B|zhJCq<(rP6CiLs@B0z5d^||yCf17r2j^o(x2yyn7U0xy14~ABXXts7vfT}h<c~i+Q&b!z>84mz}e3@rAG+0qG;DTz9{b)yw*}R$?k`JV5F)G7GX>w(cyLKaGm=|%7>L#DXDj`$f0s&Rr}UN%~Kk*1Cz+Kkn->m;4?9A)v*^sn=0fz=u!hq-6y8swPtsZSMT^*0wW*3n8(jv$1jLdGn7P!<AA8d6}KG%t2|XS>C$cRIn9j0u!YwS<|9bw1Mda&fb?8mf&w1P688XinJDB2XO}0nb^l!Umxw~@piHV=Q)<80PpcZc?=N!W#5~T+yS(ZA6Ym)Gg)Rx(3oZc>$Ou!qb+)l=f5F9p2PMKb6pLUw-K;YgJ4#+;++X^Ng%*7cQW;2f&(@KJP24dSTo01jM7e&Xb9BGH&^tjXeo4fMoMBqcKv>Kx%-6H4XW6DPWn2M@u2Uq9|Kv1i=`V9dH<LHa<f9;y{<73mwJ_qmt#dIYL3zmvx6<c`i*)WhL&=pKk0wxgj2Ye5IGRRf;IZ}_{6tY`Cmvx9k<~s6I65Zi2Wwruj;yPeM$nuf{^)4&gK&K{y^h`Jhzz0Izoe2;@kEAgB7%a8#ooNQVE=Ov8Bi}pb(><j7nl+d_@Y`M9m6AiGgVe>0kg3;Kv0qvdoHr4+HFfdCy)}@(6>Y(b~Kiw%~UA)r}AZnNVCpxk!gr2(RgZGN)T#|OH!I)6<_G`U=6dth3mXQZBr)|5{UEc*9qS*k@d&*3VqwAoKu%O8b*;R^^kN>St!mBMxkh$An_aU2<yZ}`&eftg7pYx$x1ZjSV-#-hg$tprYCe$+JX8#H9{nI<68HHd<+;qzT0TADA1OutdjGWeUh6#BM@bziB3!{;>Gct+hx9+*!(Or9RU-A3j#CZokKMNOTWYz)dio@bYO1JsHFLWZT_;0Ki{MDH6hV=m&!wIHAIQwfD<h7K`6|yPM|{cGpjF>B(GS*>A3c1t061PM<FX+Ckrt`q@?vuBGlRd-Q|_v+d~;tf5T~|dr|u39{$4lq}KiSbv1icR*kkAQc90pp_VRDQ+1s4I)_oV2rbmPUHuowXRF(j)HjI)FfWTupa~#OXG3L=T;JxBluX<saII0~UwTgRu)7n<ND3uDDsi1CMyxY5ZPU?HH(cA(qKGgw_8}sr%lmy3236CaM=@?&j6+?6r#Wor502@S5_H1{l$jKR^}qY|^%s5*h4)}fQ}cblRAm0R{2zdHfzxV9VpPiXeYAx>h7%RQ$X?Yjju}d%Z-?r}2I0fd%H0K26-d89C1_i19B#yO;v#74M7ltv5$%9-+t5bOl3XL)m&J&;ZPCRrWayFnr?_S*Fa8-94fn%%PPYGE;r&6r`ygxm6&3zEO`P4el0x9{M-<fn&bW6g<5h^n0o7Eglv_120TxG#tLXb-$&cAG)z~kwiY#|n<0U^Vi&4;FRYGF^kefJP;S}^{q4KbqfHK@xC$Lm8B>f~LQ|CzrGNX{l2Ck#^etAo1#+(Z4^~vb_Ff)KH#vU#%)O}LN$4f4agKk48f2#}mBy&1osAIxVaIETb#uNjut$FOnNoUc?nOYzVo@5DzF!eYqjD`dCp5$7X4(=(+VD`i=GASKo=`s`peDFDc!aJwaC1L!u(v$~ff?0vVHK|LGB`2cJ$Ux^Iq)HX)5^Tp|y{nk_k0MrOA;StFP}C9GCgcHNdkpy&o^|$d#%*r_cI>cfjmZ$c&^R0nF;VeDGElNO?RiSp6egB!?#v#jn}UZ`@v#cg2ZUeDc(~|ZHE%Qog;f3_N&6kgw@zi2Ytz9jTjdl|y#lc}gFdm%^(Yh~l%jjs6ceZa?XSZ7GfZoiq7eUR*hnD+!MZWS*nZ4_BmO5;bI2_~Vl^U<$jKlqN-L-KXg%)>Ph<jMG491MAS2V0)2w(ioE76#)2<5ZF#CMQlo#CB^a2ATwkf7{z)>>EM-k-KkMzk8h;v?QsgRAZ=s0JUA^XHMN{Cd5f&{9sFrUbi5u`E{HMY?z0q#8SQBjxJ0hSdd<B1Y@5B+kCKf+!^IVp5vJxiiRWaYhM2V00tXfhd5fUYLPXhm>j`s?^Zc$Qo>*0~Qu4u~PykRa|k(+oTfytMgzd{ltW>Hjj!<Psj$n`w!XkT`rIl_k-U658;wL(->iQV&053<H)21KCskeSo>{by`D0z=gi8ROQItYltlAyaUT93r|WVJ>F9hxg9=e2F5(q-$@_^pxJex%7zXoOt-I7m}M0~Ju%_485jvA;#%87i+ReN;IS;SwtJAYxQf@U(Ee3@1&2%6rH1=GQSOG4n%S}T&d6|SDmt)=o#A8@RD8%hT8e8;Ln)I1h~wxi^wE2ls%Vm$S+d6u&V1OWC`&iWw^iK_@)Nl2(Y(!|e;&dV*WaJOnubgCP;<HoFMRizCm)3^O~Q;v+55dJI1$rlas3%^Yen6+gW6S1IfnJYaz~cz#7)|120bQpvBVhJ8VcQwjAB8mIyl?xQW$!3$#{7jq&oTvfo@`^IoQxN>OtZfoUk$x=*FBctQ`t{4RXks#B!*nkTBo6I@_U;<B-o}=Cpb73=?9@8BkxTupk!TQo_OQs*2_g%^>Gvc)>*6y9ii2)i@y*GRkahLSyq8nAvjpxI}npa;P$GhalOslS9U{-Fm&K-670}x`5muNpoQCxKxv_we3*bLJZ9!2UxT!jfuA)W<b;zVklHK>_H6)_>M|O6>lXgAv_ey8}`Ur;8huwQXq1pa@jeG?NF$2MCaHE-OLyxt`_nm?uRyC^&iCHZOEMpYHh~E`vrRC(dBuYb~wW+m|>sDv}Q$V=}F&qt<pIv6h7=Z;?_e3B&$T8?TR!MG9Q@?tIl?1cn}x#j`duJc9LOF&uhYTy)@<{^xs%lf7w=l{)c7=4Xs{-16$i_<x)=sX%07E=b<;F#k-ouU4-r;yX8B)62Vy-x&7ul^X?(&8u=<Bbx>ka7e;!xw(&a5+>1>Es~nJ=rwDmbTG!<i3P8{WA2hY3q}(Jh!d@@TNa#J_m8H2D0fXv>=e+)$A46^3bMw1V^^=(dBwn_Y{bj*m>#0(@G@d4dNnB+x?nG(oSzFcWL|t=O5|#=~PjytOhnPfX`b*w~N&a39mY%6Ax`7vkw9QE_pf15F$!y3KPeUPaLu+Az!$oy&;`S_R8NpD9+i=4N!jGmewSlY{6V*Bx?p;#I)-diX?aO)<5_2^g3hO9`YD3o8Q*mz!7|_@+l5d$&?gz3>z(l%1rcR~PX#?-Jflm>TXQMsRG9jpeR4SENNz6Lt`HYd%?(YF`Qhu;(9!n+n5HKZ>SH<ih7F`Y(d<ZolA@0`cT#p0{B3B;`Lxu9A420<P7RqDUEM#cU;UI_Tes~V{F?2QkG??hEhTE@Gx_<xt`Zy{B_hlOUZ92WG^~{xG(WLXuSS6M@oW`IEKTA6iVg1%;R|kAI?XgbgoDH93wm_Ly*xYa!rV51Xc1QxeM9F{M^+p<|{^K&tHGC#o>!ZfLLDjjR95FJge$+E8bp#9^sYMEDW^b{uTPA6;O=!G4p}`9&qu`y?rNS=HaUYwC8b*`b36w)Zkb{B2PIFC~ejB4I9ZI08Xu-jyqCyE2zkTR1MnyS+`-oH6IAo>RG=uBtUgWBDbeSa9Mg+}YkZ}U%W5^-nv{it8zH(ZIS|WZ;pk1s2e8=zQaa2{T*;Nq3WGteAc_*ct&5q(tZ1Lz6ypNe*3+ljmh~pck{Km|sgvVhhyv><Z=E9Q_E~yBdnI($S68EVc0EKro$1^TV8qDEY%kzdp-ia}|f)$NV3Mc4DYPxG#Yik5szg`gQj2iJ&MEFYd0zr37YOKAV1v(>Sa&7wD;Awz$R{<M0M{dtfAuFYyof{X*C0*2*1YO)y51f<@i7ce1Y%NmAUCHQWp-#G*Ru6kn7Bf3)Y{L^YeB{<6;_|Tr#pV)dS{*<3xlElG%LZBpHDOS#5a5AmH^pouQRCJv%o09Kl%Yq3YvA@CT#T;}$l536(Xx0ARs*dc@@MK3yQSi$&|Lrk5b*hTKVan=1<SEF@~n#^hi(n+1fEvd@rT?fCJ-o-q(nY>qXU9bg29JHx?)EWM`7bE6KU=eIx=9NnI3cCmDh&gbFbJ#Rb4aF8wVU5viS032Hieb1e7yyPco#Y^c&bzlxzls8!j({|FfmlZylcD=cuviJmu~i!b$*rt^{}5!%o3U&${)5*Lkco$Ess^Ez~;PCDXA|Z@O&@vcjaYmn$Id<;3x(<x+Po1=ZXdO2g|Il6TV5B&^C$XMn@)*%L6mdZF!M31ydMiV&+gW?+(AMPU!c(xp7yx+?jb49n(DbRk+rO-1Z<8UQTYSug3E>g~P^nL7yD@cK`NAjOU<!z|N8%R;XTE5CSYG%PMBHNOL^QM_>S5uN1zV{!^5Jk032^s|eB;p^H}t`J#mZ*jlRJ9)kCwi5|6GYZj3-Jdwwvsy`KaH`dC#tV;MBXsB-dUMAw*0D5!5&L~)hp3o`12<2nSgjLk^|BNuC`;%(Zo}6>QEVLxK`1&xRy0MrtnmD+H?CgSM$;c_B0m;F8@wzG%s@yDt6)PV+Cr7?A|Lk468-x6d3RBaFjKPrT7<wv0cSv<N_0^h3%MuulGw0|5zbh-O02;#US_>-MG%)+Pnqdrg;~$oU)qe}ep82m=M91iN0X`Rxw0(+Z^W~GiEQ7^Mc*E->U7mJxL`><oH_{E%ygO@Glfeq`IyRX<Z)ezKKdx)1Ye&%Gw47k$n)tP>1w5D=)nPHcUf(HeG0t_1O!MUCD^f2MRvT`F$(W4Q_P|M4n?m6gk>Gxn0N)YPqs07RZWE|o~GNwl)Pkk=()3R%#sPz&<MqyP!!tMQBx@KNi+L7@}23#4&YXaw%@d}^Ca8nKH+r&OW5~mie5m;6=6l1!DhXWw7uw(Kz<1^{*M>{^l(b~Y!s4HHSS)-Gz#8`j3c6pH%*xG0#>5iRwAtb_0u}xl|cOv8UV#lN!!)3du4@piUf(>$=~Ds(H2FyB&E^QkGX7Hc2;G11y-h~6sC>sp!yx5c#GJcTx6`gU#PC?&XAd-Tv5!#2Ptd79y7mYtz{ElwlPoYn5q6ON%#V{wfrY=ZfCW|IpO&08h~`nPXD2?(4CUxj3Q7aCzkBDQW*<9s2UL?1a;9cI#7~RIxLJ`qxZz-9TqIklezeVTu$jabggQ?xh`y>35W8_E?yxcM_nh2=hCCa)V;tc1-Js3PhV;FOeKls{OH_8lON<npxUB?*C`ONK{txAN@qw1f%L#LAk0+5=Si_DYOlPj6EmwsFYvKT;MI%*obKm$yH*2Kp<opcq8R}<C?>E}6+f;BC90xVCTHbb1K=jfh|}Yn)T#29DpDfy^_C$tnyDR{x4E=(4jLUp;F1^b=ML$4C+-WLx@`ZUZWX->th>WDh?RS~Ku$uhDtewGXNJO0d1JpX@la{(%x0rZF1`?WU2OjLEJUpkplQ^&C=kmx1DzV4z9V%aV?W8_KNNnkjnM)Kr+g~}G2~|01|7XuMOZE>&N%-hh}*QzpT?DblO^_y9xgKP{==K<Ps<g3TJM9_WgG{UAWt18vF~jOaI<Hnagerl8~W5#R&>%dW?X>lpMjVQbphf5#XsJ!mg7Gk;iHLbV2u&VxL?rjnbn1RTyE-RvGpxYXNasfsa{x-k{U&M9Yj?e=R`^(00lHfqbO0Wg|tP<R|vxgiv8f70$!UO)|Ljp9qgs6k)(#2@~hMMc2jN#3Y_0SoQX8a1m(W#LnWQ+^$K6--RqbebdBG?xkvJg_=m$E(srkmBYT|F{zNT{d9apc+~yk=oI(HLyI)^_ar_PY!~K`xN2Pmd`ZGlv`}S{dbDb1UV@CTSP=$v#PuW(O81(F=xqz?IZc|(m?X^`c4_z2hNjI(9Pg8SIvtld-#Mb?8clRH7jcK{0FX03AW?}aU6-p!TUm6wdM3P!e5+7om@83&r`2knl`}4Oq>^gJm*iIo2u7(0k%WY*L8cM8z7tLKl0zE0mJNEPIPoF-&nqNLNk(v)h4c8xEe<t@=;I5iGa9#e)8&2IgSqnEo?8@(e^L`7fT`uCe<%X8v?Ll8DrL2j?-$>dt2eY1hhW}me%^-uN_9<~A)6yd>SB9nj7*65Eq;Na_vDZD<!tB1}*0Zz@iT&lUe!%?nKl}1efuBNL`F)c5&AN}Hv46mh5b;#-B>z!vp44j3^{QER$;j`d^xPjL#~0(Czo?$@ThQ_4<J+&F-1I@@{5(mmw}ox`Au0FXMh~WdIjbt-O+VMwm1k&B25V}DOI&!e%ixWk0C||I)g|<L7DmDJ!W~Wj@zc-W-No`h{rtmEpWaOO^%f%T+b#@^D*BppmRP`Xx1z5DO~{D{GYNh9zx@8gkKg_6%bEZDy9tmUgEQBL{j<$Rilc6gtygch#~o!q8h6Rzn%S<9Kr@6Ig_~FQb#tP$-~FHLA{GB4-wTCuza1bGfg{=2-Mbc`rRE0zI;sU$#~wbEnwl7Hv!ml~@!`p)qB~6?jc!*LfXrgzH!?(%&GC(N>}Ab`NcW!zGjrk3btGeaT#$JYIe(}LVY@zo&y}rpoOG3$ilPQNk+=<q_5^;W2ef|QqSDsITswDiaPOM?bNt(1uh(B5i!ohtUYVZ$&(Z}1cWG)=rn1mrCf7!_DYD0;4GM73Y%<?fw*cSV)paO|8u?mSy0$lJGxc@A@t*mG9E~);7JW!8ROz{LFZ5cQhLg_f{SdsL$ygjtN!p+rZyI6cC1C@jbp-CIffwR-w%W+M@ZJiW(mQ;w_nOoDf`>MvahS`RSDt8TCcP)GcQWk#fyS)z$B#bSI!L`YJ@1+7R!kILipLFaO4VagWz`-p+S5TVC=fi{Z4u|DViDO+I&0@j)q&M)YgV(C$_Bo_lM8fhm!SJrvd(OBG@9ASzQ&1VN~`=7BpQIB!#m3yMF9PVHs+rmu-&7+a8VKfd@t<Llj)w?%##{~0*Sn9tPsp7B<l#~iU1QtLOiJR(Pi{R%}f2NFpd~SyZucn<as6CL(6rN#VDiZuT3GcTi0BJQN+FFG4N}@tx%i6^X*F4NDelOpjlAj`kiALtfQ%bHN5bfJ(x!?D~ts+G1A+{eT~eXcH6K9=(yiy6?ph*emzi54Zt&}`w<xY3rE^0FtJ5fOD^fmDEHKf5mY=obpEG2a>;6-*m%5}XWwjQb#UnIu<F7`NBaG&!7_PV+1!MpwNir#y<=ylj+q&;|2(#ri<%d3oGD5ZqW=*^gl5g#OY}ggigU2a*81bL`>k%f?L}69r(7z7ZG}Fqn1Z<*KqsQeZU|qa<|xR6X4bkt(PNXBIi_jj>xhO3*5T#F2tTv73f!#<Lyc4f^pFn}gg~nBeYB3OOMB6E*|{i<-?g*MEU}UYzJ7Ba2GDzo(1=O2#YH~h90?&Tc%U+mA@(+;-y^&eU&=z5$ZJ^8eb_|Q4KdMJ*4Y?T7&&a|+7y82w@svj!{sh@>;n7^;N`4?>drs|7N>9n@qirUB}R@3{kDlx<?Q?Q74*xpj^?88{U9$h!9A4XDhE(#n=#QD;duq8Z4)L^VEkVGV~=U>iqu^upB1OI6?Rq|YpGh77e$dQeAA+7jbgXGnT3QZ7&l8WgW#X$NaCz`+eWWaD4-#CMBogdFtb~%WZTqbtUX_z1SRQ#lUKHFWiNmf|AB4;*WVItjr>*Zg5go+NYvJ-^xVA~cVL>mY?`czP>mjf-*~7EwM9>h=~0Y}wcT0=IO?rXxM(632leErXO>o<W6aUv3$(4E9eyKv@f0}Kx)Hj`jkZt_C2iq(d{`9~aoH*f;Vq{V_E3&q1=fm<L{mlH$r^W|EDGMwu=)s`IBMu*Ou=Q^g<364VV8D|u`A}KZ`)3g!(b~BzUy?+a&+>xkozPD$qg@qgM|Plu$oDhlQWxMHURk?C5_fMi?9zPBd%&x2`|zDqZxI<ev2AJt0;unT$o@T<fISMHBXQ-rginoIE$G1eXu$@CsZBozhOADq{k0hhZ;UNkF<rJc~1rJ{pIgfOXr30eUsL6ml7#At=&5wQ=2Eg=LU5GUcgFu+sL~!lzsK5xQY;1S}(VoJ2N!Y6PfhD1mjF;_XIsOsMjjA8(|W9>u|?}4i8Or5~+beDXa`Ez$hm*Ul%nrV(v6(wnN`VFwQwYPLPzKzLs?tzy>6|?S7FTyg)LF3r`2Q(puC$f{nmzobC7DXHgUs+fRiLIQVYb=MDV<`Zu>*Y$q2buOHX;+XNe-3ziuOZ>fg<f`DdGj$W7!VNW#?k}<S0V2?muzS+b%U>&!FDUT;+oF^HEl>ldZ;hM!T>w0oAa7Z}xHJwmhf!)Ke*(zalY{E*eVy&aleT$BUApy|65B1yE*IzI-3ZH#bL-AM-RJ<1yZ9!JPb1RQ|b}34fx@EaYjMADYBciSY6;M)AOb*7(eLVSeC2^o(CcN3NmoIoPKxqlkS}1_2sHP~IV1{VxOjYJqn)iNJ1?QVs)KN8f45{vdKdVuuSAu*4Fh0~(=rKo%kRBIHo<Kyu1mqRM9$@DjFTBmPd8DyWgdr@CNFytt^cYiz+p){neboJstTk54Gv>`8`UJlNd5b73oR=YoV;l%$zm2>zT@4>b0Sc(|4EQXn`g<2ITBkH7avo7tt5@cyfmw)BYrR=7-!;mB0Y_VaPWj&P)#jIwjoF;SahB;0_C>Oh3vJAMYQXoyu*d~Fh>a7`gM&0r@pm<9y{xu<S4R{qL#Qf}$W$llCx~n<sUc2T<kXxgia&Ltd~`NtqEjo+KtAJ<1@rD9CqxR`snabDVA{EZ6B=#UtSWXNg~O$%01|A58*B6Atdl04u#S4r8#P2vssrMAF}+eXuEG@4C^JWS!woPx+n8AGIwp^Ps_IZHL{8C=$)D1_SjRo<%IN0ON(4=;c%S#~l>rLjd@s6S0=Ux{r&A8wnXCgdutKSYd(I)zmx?9Q_Xk<1LeHG_Di%9Tio$`BMTgs$fKpM2xs?n2vh`BY<DqhC<f(LeH>r>rh=)v!$0quK?dWtZXhjxU%)M!q`X}u?RM<QiH+#{dGhb{JSlmRjNVd3I&6tW3x}(**LuzdztA0Jv8nT_|KbyfcFG+pyA!4Njnj+3GYV8FMFx-}$UM^K6^NcWM)J*nmAl;=8)-ohugT|xkIdL=`QrCTViBQEbw1Ev(Vc{luzEjU_cNyi#3{Vp7Fo@`_VgysZSPXoV9Vy6?cwt{xRC(9b0@$x*!>!R(?k-E6SO&Y6<v*bn0tNK;KHP?PG99A4!r}6oo_mjXO;>Y|pX7Gt(+2Bcql?ns(zN9ha@i9q!(Ah=AZ*MHf?ul0>2l}5fX2#-8BtaOmH%lXKVYm?ny@;mM|VCHLhPDZEsj(bfrvm)jL3D(q83Qf>OR<uQc%EDAJtZHszl*x9*<+TfLM4b&!(xURMGK37R+YTJ@>9j+tAx+=*)oGDWWx_PHwYnJ2}-B)O3N=p;q@9C(GOluNQxr`|8Sc;)t_^XQD(8hD5~Lhdlly17(4@jZa3a*{^jzk>(S6f2G5T-XquZ28Uq^x)Xr?=M8Jv2?)yryP~2w>{%eUZL-df+(K4Z#pp#O?OSS#u0g=+u4+-fteM}H>7{w4t4iTAJ|accGO<J^hsj=N3pffZ*FM7@>7if>LH6Vb-E_C$wCiL|rG$WmubZu-LXz9i>5@?F?v{k3*z&HU87lO&lF+P+3V`8^IFjE-=>6XlhV8mAh=Sd7U6S9BRofjhl1U5eR_Kr(f&N$5MGZNCmNI=wDX}gn3XI5C-a)GZ&=Fz*{bdZJ9@nKS{-f#W8M$80)cT7I)1-np+LrAKTj!1vQb#A#sNlTV4T$c6OEj~WQC|umu8XC;jefx#XkrTC7t1B_B`CMgT1VbRC^K2M-LOE6m#E=PXigty(QUKnWxyVyYwE_tJ$is`43cf2i$myS6+l>?06O+S`!EYrp*qAc0xGrR6gG5y0<5H1D!9ZlSD&Vj?yR(oXadkDBevqF#u#~Y9psX-+^7L%TJwy0`iJvBTq+G0dSn!12X+)XA};Hzi;J>JdmPpbArWP}c&D|9q0IyFG~m;Fz2;)+qVPE~-9%0UMt?rrNXRx1eWmgGYRE5vUb!23gV9BF0(^OrK2LhFC%`G?gEgvtFR9U^)=XMdn`ck~D~3tV_p^>ow5ZmHE5XKxI#$sGS)ocz9Ri0l)(wly83SJlt+rZO+m5a*$jwp?uHS#ZibOvVs~8(K;xz(f0kP^DwjC$Ip9e}zsoKmV1hh`L)tyE_eKTrueyBd={;_t!jt<b+oobc|_Rm&99}bGaC%9_ZI?BFclt4wtvagu5to8B0$cFH_cz6)O=ptHH=vcV92r%w3BNn!M2llf`_&hAHB(3u#`@6tj2>Qm!@>^mSe|0Ijj6_#d+QKdH)>|sVvPMpXe2IXUGyFv_Y`Q6Im7LW>X$&vsvGz1wD)NrSZd_GkfucSNNoO5vlc?~~+D2K^4?!&zH9zD8He;FE7-!qB?RP(X@889Wfs5R2770w9T%>^x;eI-#vZ3DU2?bKh5*9_RfmziELJIBCB|K>wVj2`Yncz!+GjRXmyI)^_p;GxxuP^dTsVX#V>ptpbRp>Me#~|p0;a)VMTr&07K`X#YN5+TGz@X=(anx8cPYWr{2-d+addse>FS04BCHi)xKJv5P0!=H^w1>{3>LlAOkGp|P#eMDX?92mm+>pN#_1V$NU5F!D43|#0)h`vbeyB#CDWbXLROPz4t3hZKCKJXS<LW<qrf1F`^|6`uY1m8w(iG*T3^@uVl0|K6j$0&K#5I>{*ye6HqbyqcNZ|(si-dW@6)WFA$QN;yBKA3xy$sXMI1pw;LBW5RPxW|<b-SY*7ho#Fx-N+dQqjXobXKcd>E)ufY)%BHQO?zd*}xri{j{Y?tTVG)do@}6bzQz|6l^bvhtzsp1UpQ53^$Ku4+h-n<t^OT(isChBOhkp&em%zy(}D`pcNk>28`P7+*cTIN{PI65<|XmG~|)fItDHSCV8O+F_yV&%NV-dz3Y6C#H#l+SS(pDODnBC^uVLJN5YSiP!8?Rkl~`F?z}lDatMbIbiwe;*Zrf!6#<Sn!<MXDmY@>iMn<Gn$<e}{n6%MfE~&BzM%5{>soA|M2u?~M1xf;aA;@WeX=K!ZA-7Bft+HijZ6y9a?cR3b9=9pCPdh@vaYj&7)HqMZ>n{i3a=YQyf8~$#{;FJ-`?_?&iR7gXRug=$-qr^A7p?hIJe0$?NvlvSnYYI4;`FJzfS_qxz9b^US($&TYNdj1>G{9-OS~?PUNl7N%aNdBBtA}rPPAgIXRW{(X~fG6BYZu`R3*@4P^zhWG!TCF(oE{oKwbYG?6agb>yy^N=}FOaJ@xpdUz}xK7idl>-+urC*<Y#(qZsH&F}L@ZIWJI?5cuB%x7*{^G%8nA!ZXxLJ*^wmI>c73d;;GN8C>l5+zJUWu&!ETg!Qiv%Eco9h77wrZqsH2v0M)#I*~rXl)@oI_F%E6I)MucEpX5)T51^5i{*XCdlEZk-L^e*0(NAiJW#t9k~~zkUAMhdT!`08Vm<75RC6aoY`t%rI=hS9SPwkVxs)O6s&6}8dq?72@&0%45K(Jzp{TwM@ljUF21O!5I5bj`01Lc?VBy!pjYh4A5C(+|qDU6HaW<Hv&<4>99jrr5L_uVXlL-3W=ket;etoqr_~+N3K7D?b{L!LM((zy4yrc3r-#y@EGJyWF^nqWDo!@Du&Tk=yl2ihwwIz3gShTVCUu3=Nx2%SM6m%!$CwF1UN4WdlIRVOmMiAtv{D44)z1p*UgT9bl0r(#iIwQwl?V75Cx6R$Ch5(x*uHNIqhXox%&l%dT$G#SYY|CjmA=1@4t3Da=SNl%r@ku3|g`R_S$tA%^Fz&gg_9@_Q5FG;h98w5-9psW%=t9&Ny*B>n4Fx$_zk5MnNURXuF1)zJa&JVXk0{Q8F*YA{>?-Uzvay;H1zx1n_j>Ctc-r88;RnqNWmxtqN2l!jPCYC1{gL$mbY%wt#3-~{B*8_<FNioRw2NHOtAMQi@LYXHs`1R~!(gOIlur~8tRE8^yBWPGE*~9I2f*C`3~N$P1-$E7;UT?rv$=Q5muhWzwfT94W(+wvoOwf~kfK{U*YaT<`10JxhtW7$D<eKj_re-3vI2&E!7Gz`?jzz>jj8unp*SN&IN_71sq*@Qt=Ynmz7V1zF^|t}m7h9+y#T5vI2sO-s6w?SJSadS!yO?w^)^bSsEPKX7^+>7MqX#ypKgwzbbqI|mue$YP@_s!91BiyS&@8;6G=Ap9j{8MU~c(`Vf=@Nrb>03gkXt^PqDPMsOKTqk_zG`M*gK(=yhG@Q@SQlzJn#OjSvbeLDz$~buvrMWGtAawQvE~ryD<ymkQ;QIMpUZ(qT&1A9GWwX_8=Jv*rQW!uDgC<T{5o&#q65+OHL0MB!w#K6W*_4=G`cpt7|>N9{iNKBxFV@?D&1ovc!IbS=Rt(0g<uc7|R@PEUY<izre)j!>z^WMSLvz`n0p37PHMPKf%*<O)&I(wMr7vN5l2Bbl6$^0`rX5a}jWD~4o`ur5}hmyX3Sj*K5T2Y1Re#C{Ctp0cGUGbNpxR0!FuX=-W}Er1IV6?FnexI%&pHP`zoQAio2j5z)h5xIpcbn0~B6W!DyTIi&5Bq4ETPur^ZIosj>gI-}mc$YDZv5j4SaY=I`RX0Ur(X#uo5b^;Pe|`&e#vM~6-4vsqk{T#vxOSN<@%*9=L-ywjm7n#phMXQS&o<X}vc5f!!uZ*|pJ`F67z#GgOEB9J|Ei)_YprO$JOkcoJ__EMBUC!jWF0g3j{gbOr3Xgh=U8WOQoXjHTe%X`bHZrL-CXnCa9P$tcc(<BtYhXSMQEqVxOH$p_xeD6F$hO+O4eiY9v3j)Avi2PtdRgo2nQvgJCo)!R!13@;TEz#Hoe1j?g7mWE&|6`p3&%|FXVorln$4M!_sO}+mDcB1k7ws1Yphz15lVdo2h)Mdq9>{CpHEw_(w_9JTEV&@K|hTpwI@=grXvJf!9^hZY+F{>?SM`{7h~s8z8`g5i+!72-*j?mPipG(5bdGgs9v|#>hPFNcC=7GDZDqDpF9>L7tbed08_W(B-~exmtV=9!1ojt1DcE`T<|_uL$rZ@6#IUZnRk3G`awNOc@;cQC8z-Eo^U*eABI>JE8N)g>pZNoD^HEh%pAB0Pk5V^nC#7z;B#HQz@`u%Y}_NFvI${Vc3Xw4)2%nF&DEjj#){4wLpU<=@lF<VP`VhO0$O7UIBJ^Cwd4afPlqw$)cOzKwIoS?!0q{=b%^B=;k%V9t!0jRBnb2N*}$AdOk-b`A83CG01g}Q9tZxRQvzV&@ABx`8l-G8wV=cP^j;uk*z}+m?heb&qcb1LJx-dlT!Us8oKddkfBf;k=ci=HDUnXXLKp?13p}qY5@x8**en%!Tl|PeLplZsg?C#fzEga(sy+Y*c=A>h!0IAvo&Kio_FS!+vr4aB8IfTXzv?Y%Wf6hH}d|ey2Cy+IdqDZNJyLFB(Lx-wuzyE=ciU?zuh)y&a};ny0xH<0fHN(7q4>AKv*~w!W{O-APu5Y`o)akUswNPbp*ID>(I89ikqB%B3F#v|LJa**UFw-LmO3Wa|#&<8MiToS%zC!$Rkf;tVXu2RfhK=IXoQGblsg+R-bdLUeGT@ZnM;p!hl<*C~VwzVLs>m+F<4b(z`>u$n<IS5{PvD>g=s|BdzSNij3`0h{~{p_Acl{w0v6cN)xAo&)+rjO+=Wzb}PJ&8Z=ew*LDtF?((M&QYs=pA*L_4)f>7lCoB>4pa-nT>IS{*0DB#SOSF><mz=RQy`g53<0v^p5|*r*B(FcUZT_hGa7;Z=DI<+u+tO~p;?`%gYc$=ivDAgCFb`LL)<q%C8a0vL(IU_N#j$J?SQ55Qfg+h%;P*OE{l-u(h1K6%(CK6sG(o@84<nPRDqJHy!Db{G3sxcI+?aivXcx&(A{7K7`U8Rx_kGQ~gw2Dp?0q<nu?YV7oBLiZhTib%Q2&IM$+J?z+cm8|;IWQ}q|6C!!&gy}7llvu^$r();<!SgdBWr!9!%af+y({`5>;X%MRfgi+sGrq6IAr>$I+_H2jR7cZLWq;#N<Z0Im*&M;JlQnVfneriI?0+%|F+TVh~$+j>E$LrUiK0`wWLr{}g6EyOgp4$4%qBXNq<0p(ghkH|NwFP9$%YX}LRgugV&R_K8W);R$FDUgs)3QE;h-SdZVGbyjB(V>&~`6KA3`0h&d_a_KLGrf=&sqWUaUu;=fD+-@>G;Oz<?#?!L*e)Pq%xo)|Xeb<Jm0`D^^1)lfR!TsD5H_U3@+37%|l3oZ05y#JO>mt|*P4*2-UGAAjmXT1J*<0YeBz57p35}O0^xPmUUUZEqr3JB;+Aua1r8XwZ6_nWPJ=)k!<nfLU@3P)lau{1#v=gaT<-1bw)(~oU*CTM|z4T+JY7<61A@;xyj?XE$&#-K|JN+{>3R&0$UPMmU)oX-@LgXY&AZQRr018HrPy$YKS(#(>^fR#deqF@S9}B)<rY<8c!mov+<M2Laek-U0=aH6gh4MQzmzC*<p>PFkiFO^32EYk%FwQ~)1w?!`T32rJCs&CjW-YceF<s;;iz?EEs3)v8-xQ+RLMg>R0}<{MJuX2{RstyQXQA9+yUDfbQ-Y@vfQ`&oaEYV#q!bz|`bh~Y0Z0=HrsqV(tKV08@DzB4LPdr1-KzvUgJhprfx(`SMZmRo#x|U2shJih6_+m(l<?*fh><gGj>|_enMySlM@j-B!W6}k6h>QDzC!r02q_!$xR@6XOl2qf2Mxgytq>Y)qMOhKml#$vh0Xw_DOu?}Ph)|HsVWS%W&3AcgEVwzm~h@Rt22zQ3p4}@ekOaw)7%?DFKNH{buwXzSm0?u&01(WHT{W(xl2^sgN;wFG>a)@PPiW!&AnneRRwoU0vPa=ki(ms%Agw#i;!{~<W;oSR3ygH$;EvP=25=4f?!wg_;T#>x+Itb>(&JYB=e*grwtUP2GYcTXV&4R+~--hJ{i*?cNpcW@LHaAz)O^njvAriS=fT2FvBk0zRXaTOWiF7Z&HmcfRHN}pm67LZ!x+}q)Av&nL=4V%sJwo{n)5g1+Dk)GMiJYR=0<5pw^0p$Q19E$bI0KF6B*C*0<hdsFz9KfYJB51-Vad3^eSdfDKDaws{KK7Gf;H{R9nu{U=jO2CU(xaI#{oU7gz~$RKzLK<HzkDQSvR#mlIATgxQ(43N_};rSQU2y1Ftn+5<}FMcNc2&ddvWtN3VQ12h1)nBT1UT8{ZRjKDK6ka0DRmR2A7+V3IFtL4BA$;;tukpg8e5I)91(mCxqIGRj80!!loiU4mDAr$wqhDGZP}4alHDw>~YPb2fdNmZ4;*cc80*+j=$Ie)2z|g_7u!S^`cn0_DKHOf{ywW`zB1;svM|DaY9SCf^44J+j)J!U&Fy4|!E}Ejg^jPTHm{%WO&T_oZOJ`i(CD@Hgeg<uJmx&Y8Vkw$pUk5hpeHMcFmUV^D8<B_*DI?--HgZ4AVPH>0Xm<W%*h57TNI)!#?K{+{cx*2Et}zcc(}RKq)i9Kf@^5T@O^#T^RfzmPRxmj5nnJMoG!8j$j3ydE0br#0V_4M!D*$7?81JYT(Hd{A-)7#`YT>Yx36vPQU{2ULm2I9b;2x;;QVu5Y>RdzST3PF`1<&B-pB=GtxCNgA6m1>cn0Sx2Pqv6lRXNZpg@p|bxI`y@N?vUoE7%<Z%)jEqT>3YW6d9Xk*dLTm;DA$>8I_x+-QWUuf+pVBEMfPXDSB`138>;u>vTDLn%dA$psxiu>Ord6l_Zug)wVh9kVZVV;4#TKMLHhi%KU(}=scbAu?>sn{k&dyRdC3Zwds{!p#pJgyIS&ipl~I26VLYBTSxsw+1K$Y+_147)N~TZ5cGc2soruk1C7rjW2WWNx+G(T@E7p2Xg><xcB2AC?6%QQx<JfTAhU{%LP~E{AMYHL7||EImi|N4Z%fETE&3b_$v7eu5aa`yPzD{a*so=K5emgOStx+#kdWc~%#mb|ma&k31Ky!1%LS0G%#)GhB8*+D+Ig<~RcPv=wz7-Ogmb%_QB+AsyQyed1~5tihymu)SE}+cNizzQvAN5N@{b5{oyMRynHRep@WLB{gy?oMR%w6fFqR(g25c-T_p`5dU?)E(Kqqn!sA19~P0e@px-4(+c9+2ZH8)9w-%>Q_2rCZN=;#O-BR#6S_t{i&tK~7&ql=!j-1*@G8osEpd@&?N=@cefTve(>@xfi^#Ce4}9U~hs$O-Z(kC;}|diMh*B8C0nn}CKmhLU#l;;}v$-AL3JNiTq02y-PNY!^MFvMxP`QqSbS$UKM21IA8?-pS0ValQWbImIyBy-7-+q}}w#5K%S)fK)6}(R5|xXX}^tVUl0Ns2(SZHsAKuQB&T)Zi%Cpw7@h(=)?IZfpgS4e=4x}Mh|tG%>qm%iqz_;6M_)N$gc-?ArCbeZ?&XY#7#UbuXEl;KI#>U60HEb=&s8}&GvnSQ&U+cPIKXLRlk2;V`S-q9_Qmf-tYg*{V+~kYH!SRSm-{eEP0$lR^RQKZ<jEtT@`Yo_b=g9*rGjYZNKo=U67@#QLKl}Csrr%?MB+n1(;zVWfrz9Z0z)yahj`gop-Mzde9Yq|K_r-AyExD{Gr#0l63TiQ$5r_FLOEDW$S-36_hgGzf~1R(RC-4yvs_onVL(!m!=&XW7ynVGTwjSa#-Ln9Y#I~Wd<wDdYxh+<nlg@s5U8*Cu3X|h`13o-0chv&Si3#zil(!Kz_OJgG?c>tcJV`(DqF2KLaKbXLMW2<N5sj`qQV+ujZHcui!Et^6J+gUw_7zn(|_=e3ZrAi2F-EHJL6Zl9YXgG-m=Ws@RL-pM}jR*Z3K`K`!(CcBF{$_HJ`s#PUrm7bn^arFEyX;COfbv9}>4`q@suOrFA9^@n)=_Hn+n)&J~EK0#93{&T5hQ)IX31C5Jk_Qh^c@dI;Sl|A_rE~(V6%xUc`Z>8$GVl!O11?$*xAI7*NUp~M4`q51vJcL@A-RY>c>F2saYC`RZ<)50NQ8h(#nH_K`K2GEoGJpGe%M{XJ;A?d*n;|S(ID9R3rBUyoV@z8!+@lOeGlb#zUw;4L$M633<(ohM?sV*c2haZ5cFh$W9g#!T483{_JdV2kM%)KS(w#Qv%&l~9hEVNqdyCiY*Bac~H7))HoT;dpD$`LT8Is*2fI*b?>lavjc=&5-YtfOX9JheI#HuKZV^U~@+hqhGlbBJ7_$3CW^v!Ne2zf*@`9!0b^F-F6jPVIThD6lwp*(>3b@aK`F2|{6rDR&QSG?1Vyen{<5)?S~#E((uUl&!Lgp`z65%i8J8!q#wpMUu2(~s-*c(?AURkKE{-HWTqMw-yteVig@fb;Ya>T&cJETso%ug%oU9fWi4RN^K^bFvqm=SxulubBp!1I`Bo{h0Du)R$eSrtf(n2XElvz?5!c-T_=kwde>N6xhF(NVXZ8qjJ}j>ZqE!6x=+EazwX%_PyWMYYzF>)TZ9=H1Kj!et?=U-ArxPbBk(=@`70Ll%<S(VbVyoa1Io<3NXM))+FML7sO<WC@;;t<fqU6iC;|qHWYe?MD1R4!HoB#Np{%<%IFuWKgA7?nx)M^Ep}b|4`K{7i%|7f`dnQkT*}p+ykurtSHxTkhl%yF$OxB)W|}Dp4eX|n3p|3eBW`qIeu>K%Rgci6sv0DxBYV&pkNUU2Ua!AAo{%Lf1GKs!m3cI^vd+EMz{J-%L>^a!%7fifn{`p@^g2AfnLSe*3tIj8k4I)DL;ZcIuYo*j?B$|Io${V<*NmInUM{LRQ<p53U8b)O>*d0CpuN<x_Xt;pg7Fyg@r=2>w0Wuw(^+MhPGKiP;f24fo!ps;mFKZ~VHCtTAyIn?`3_)#fSrbSGApFIf8PB`Ac(2IvO_c#db?^Rc;IOH78<hP!^N_fTp))>)nqb@8KRQlva~!$h%E^)>Att)n@vy~p5+FB^aZWDVGFMWjBbfl!%WcL;lPGA`np|1T`e`k)rLGou?UiCbo=#+b`_gO7snw<bgJEjxULWDi}|VTws@iLOVmA!wi*Gy<s2af*seqE)SR4$!Kb={LD4Ao$6&+>f}XvP3?<q0$Fip4Qk=unG;9VD;ZBwj0!Hlr;A&KZ<r|-u^=Y3AH?+-^FKJQ>lbBGeg)r<xSw^iI`=V_xFs={#iVLE0Hh&{_^g2P+*q(=0&VPA6p6{#N&jNW_Ylp2D(H`zrny1m3J~?%pwoMdxSwJev;ra3UsfB*=j>|fyMK3+Ex`GeWVL(OLzqHLr+Av=ncsHfs0{HSyRa-<TfL#=KgSECUX<+pT=C@sf=s|(Ug!k>a+TExo7HIm$k_buSMR5qbFqn#vw1;{sVz!r;ryypx4r~?`jX|Ivih}KZt>QyUUma}aaxN8<Y3X6Vy>C=T3i&}36+?F}mesr8so%f8{&o#3pSMRZ6vs#_&M69dgU+~h0#Wac*_`UW`+Lj_+y#-4YugVQwd`~Qos^_%F@7-EF~hHpRCc`I#kZ9Q6M<365DyojLI2f`f|cpou?^VAUkeaMJWTsr!5q*Z&<}x$S&726eq8I7%MIb#92&vLF+=xTK)pnNzz(c)N`w_?wg-I3C&HcU@%`=&xlK1U__NvIZGG6pMo?eB&UBPB<3TaI5A?$9mYEPI!c+4bFEXlSy?fv=@M&3(+nn-s*TYU`zMDNZDtE{724O+IzY_r~wfI3K{j?!%9oWkm=nEqxSfsKY13pM_NjU7#t_B1f2boF7x;)6C-cDX4-2&~)j(z94ry)Y-b49jmchtd3D##%9SQfxVDSyUjNb9ubfDTRbRRmglJT7tj%46Zt$(d~%Hbta|d-w{@tre-;KW-?$;q!5csgG6krETvf{e8^JB8Oyy@|ag_S^-Q<Q>rG4bl!4z#%?BhbDjKEc!`mzg}qEgm8pni2HI&*K$RlY^Ch(**4Yi|$|1}Kd;{P2$#pt!=eCX?7gmF5Lg`#W!1rAWc00orb8Xnkfr45|-hY!PQrBLab|h1Xe;Qo6Y@?h{mYz4$2Qi}Cg1RoY<6<1jpz)@c!dSvKiS~gJ4wrZ*!p(Het}7d~`drA+TgkWOPBNmL84Pt77vK&=cNxw8WUj65GRl2SZS>2Y0lOQq#dZawj4=&u<jUf7faH15Y<JPU0-ejkhFepy+%@gl3vhhyz1KBS#|dBf6(dF94TOND=+E<-<aG{{d}XpOjv$>G*^C1_bcLFXmBItpu?49Sk{y*9WYK|jybF!TyOe01uKh}T-sEb}x`L2Ht0__RZQt~JNNcaJ*mybW*R=_v0*Rw(D+LDkS(9zsL`xBX#L2-_p3AfjaHt5-dDo6>t~I1;ih75l8*7lr9Y|gPf}fvmsHjp^f2wI<ybf!WZ=Wcge*Qu1BCaCst%MkgL`N3>zTR?uVlO0<PG6@wCwo5<0tA>OxMV{qxs|`tg?(8bcq8n@MVb)Ubb@l5ufytUBn}?LN5}Ilte{Wus8i~p`@Tb6L1thbdtj+7YySpR6jDj0t{^Y4Mree|6y56rd~0v3emdLgkLtigpjRRh<S%cL#@D*F?DultST9^$Q6a}J_0XSTRJ!A3Pzd@}<!K!zxs6;z34~R+_>VkiZYX<!J|^YKi?~oGsj_7ZfZ`Ae7t*jiOQfN$-m8W~yLKw?N@9Y&(X$|@(HVcDk25yuihS!Ub6O0`LfWQMnRdgy*GaD%D+rNp?dy94hk7*^HGG`hR4kHOr`L^j#3blYvY~R2MgV{8<x_AjtYZP7m#fRvV@{_qmLYiPKo-+Lrwr~#p_vO(7K(s*@!8tGgOE51Ym$OqkgFTPrAfPSmSd;{mz1TRJ@S_75S4v?4hk%t-jC1oIfA}zVCG`xwVS%U^arascXY(ZD3`IDuMpo&ePtUx0N828|Acxi1bziOBw&8)g?l$Yta9tB?Y%NZn1x=`_T3NP1M`)5R^A;vUn)8*1C;JKB!J{I^Grf`MLr$uH#C|@<GPQ4rb?AN%9=}d@e5HY{*NBkZ~rRvfYJ`(eb1KEodVxP+F&_R+(yL3>;X}@2cV*YRg<}m317hDrj<i<OOq)m(c8GnWzbQpC@&gbbY&i<iWs;jkZlpINPPyWP$bhJ9PrH7?HO3HxIJ>e4Sh}>RIEyN4O`7e;<8)q@s14IC#upn2W*LCU<ho&x=MMN6#JWFPwSEG#_Eanmqu0F(x_~VA4fkS(_7E%S=n}Wom;2CV8{?gT6iAU$RKZ1${w3RxHmw5>17rWPr1`LM!&FgE>>SKudLz8YJ~6?H%FFT6k%J=WgDwpe@+g&4Zl)=>hTtE1wqa8*I&3eWFDJ4?aB6+s4)PnI%b%VO~D$>Q0Zlx>tOrl?vDnK?A>`c5%3D!H6pni7rVSK9QagEII3@26&q#(3(j5WV^F1M0R|=@q6w$dCM~H$9i{377WA|k!6?fa^7=%Ub7%D^F(spKrn=6hG^1)Q8T!mZNX1dgWAixth_1j+-wLr8wG|3FfgsX7K6Vq@rfw4=BC-ckib-ZgiKj0VnHVSYCMgYbUKF$_A`8zPlQz^4XHq=Cnetw48>CBhAnPa>h*+1l4_y<1&5WI0YsC@`?J%e{ZtA;GhBzbja`>l^aAUi;`MQ7m9@l+A?MtideXw8EMMwt_E-=D>P^3c44l2Lrs{q3mot1E4U+7m!$|9@@yLBJq9td5Gfv$rc<&C49QF}Ad+AT)5UI(@$ut^SLxGtZU1C&Yk44>)y5Vj1kzA))Z)k;n?+xtT2DWqwN@>I;*WtC&{u%pDJriSMm>oYp9-@;t?=C${|oW-K}BkP5!h%BXelzm9@q@54L<#mX4EI{>8iX^QPA5dme3_So{$%%3mNyqp7Qj_d7=M<l3rW9?#al6KjpjCl6MlB1(PF7J`$A5Ljny_7GM-LYE55|xv!14Td6kEZ>pR1-9ws(P3YlEq^GO=6CydyBuO)J{y8)fhXb<KY0WD<BzsLsdanO+o4rg*LEx2fd#E_>WyZ+i+(j8yovnk%vQ;|6lBGpp4^3_9LM|5{US#3WPufxF;;MmRT2x#C=>FK$Tl<k*Tp;KpT0J>fC06Py!_7VBOJ>|EBS*IksJhC~I|+upBspn&Ka;is{DF&J4}SDM23fQ)LP#cMf_bsXiE!rm=eb?p<D4)gcMoZIR_uaZhnxB&r;$0`%9b6Au#dC16PR+LdFA@|LJl-W-a+69E>OE(HXGsvH18Uif)v;WF@8+ji;nvAzAHrPecjE5)Bw1P!@2%C?32<J?bAoM7VJT=S|Drk{NtNtT<KWCUyuC0kdzRm2w*4{P6pi$)dJ2X%b0J%_UUr86;E`zyKJC}IRM(8C|-4i!+4~|*{B}EB5h|`5xCQGPv2RPQXH88<S$ukYA$@MrTRo&6gOCANwx)ktnW*DDc_NZO7Qn5;fc)++IUU8zdxG%`Il$9oQ;lOs!b>CGSWqXZ_9?cq&4(krMR6+$*kyZ2iWlX5mNy(UqTbq<;14E7qq`9hpL_|o6F@iHJ&@tDUgi>R7IGNHY#ZHSp!C9lmlA{_HTm!h$ql_>mC6{W=d$4=H>L7G5wgFx;%gCY`zxIeY$FqYG&UBN8OLw-#5T!~aO6B>lf?et<xHF_`;(OEB;K@x2hmeoVYpXc}Q$VV+tkkziVG`yw%FYj|?jUu}QEJu$(uPZ}4um#9<L6yh9}B(r;j&coP_bXH_Zg%WE)>9mIqjj~`dX}wi6mN-GkL?tg(Ykb1HU#)T}#!rGFIbx-Yh3Wa;7nLuG=QpSN0zlCAKO2rAa`q105?ecwFh17IX{eF7_^(9Hh(8xm`Ubij0jLfbQ0NA&U()g$Rdr2^g9=le@zJDJK{MPf3@d7ZTy`^Jp8j@5afpM;2vZBfI`4V1NEK*0z;83A}P3qKny?n{q102+33iIk7{l=XNyTbxb-7Ow`#w_?c6%Lt`~>2^55dV&ned;jyFZgtb%Dz6t4@L$Spu5P^Rru`CYNctbm%BViYB>c`|PhPWegDpBv}DQL@E5mDcnx-VtH@(=HG?sOR)E}`Vs7evj5Rn|wdo!_oY=pNT)HgDw51=`+F$o6KgnDA+%3hv=wgMbDMe^xUylztE`p4PI!ksMh^y2x$hZ7|9zyzEV1*|BB_g>h56AC@;#WHMN2-|q~m;Xyf7(HYagiojH)Ci3`&*ajWyk3;7&JWZh*Y+Sq=&Vg%*4E=brd(c&ohpGV*N#*9yPdX=nW^TiE-~3F^0djA?e#upCu&xk5jZl(85P1h1M*TkU;iBpt0O7rg78N8r?KEUjfTBH5br>4m#^Vfcz5HT5o<6jB9fyO<Gd#z!9lE4=LsSH)7S8n!gPz;^n<G05O;5RNJM^l!EUSL;l^9szR=BnIK@M`&HLpn^7y2QJBY#@K<=Nh&g7=((*d+nk`!9h+EzMi7M|7A~A*IL>z-p}t!Z6VX=lvqEyH*gM1L3#mqK{^TEe$=5iiZ49Xk9~Fx(^Ax^wy%b-%6x#o|Ca3Mp>MNu}gw|;c%fUMDI**okv&Kb&vaGlpb`GNz!Ebb;T`~&XBu#1%masl5!ZsM_|{Q#3UC;lkI?Nex@(h{i+Eg5n`si7OnUC!JO~QTGHzI8J-e~GuGfOSR%@|$<}_~i&+*uOT+GI0-8tk0_GpGny7TJEPcaz3?(wUFIXXaC_1iNcY?oBnFKKH0!#`4ivc(C<(Lu8#R)b{9OLWnTl$pZSZyb9`(JFr;_}9|r5iXoMS3Pmai|=w^M-Wjzp{$aL$92n5L1@|*;PXJqmng~oCOOCO*#j;c;vgBS_wBE^8%-x)}UWIk}ny#Z_*t0UZQ+BpdDn^NiWE00f_?t3e#9YU1NqR%+rB671euwrYES-b-U@vhrr+A?P8uU@&xggI;94Fb(sd1g(X||ZJ!(2J*0W@WZ@6I;mhm}7;T&I^mh0zHm!h%6ECt~+P@CBGAN6(a1?xp!9}G~(lG1s8K{vwE`0g_O7z|SAn7}=BMxXk^N;{7Bz7VfHzhxWA1)`*=Ddh9t)IxalR3OTjR9_s<UECi38{fNmDZ?Jx!h?6-h$vZn05LJ?MaciqFAFX_tsh}^Ey`n9~OIMB@e`4g1*LT*tZ-gQF?|@g?H~Ul$)nU@v)klF2Uz7-}~$9?k+6aj%?S)`fFj98nz*o&rjIY!`*i_qc#(69(y{>YH`>L&q%RtT1Q!--$!-Kj&`<1&rH_ZDXvXCJr{G-dY~Y-PPo@^5~vMO10+Ub$0VwDn_xV2(V!7h&tn-f_X;hjjA{#jp{iJN<rH67UFWdK{t4zH9j_&gr|A4!`KKq~=4HxUHuNRu*%y3T3yyZAqUB;6?x{xk<7G}?U825!kl7)Z888s=PtoND1a60AIm>K$&QC-`8-xSnrAg9AT0i&=RLvmf#&m2t&+<4yx{6@ZZtKyhZF3>`O_?Q>W5S@Pb!d~y;Kh`k4S7h9(Yjn<aI?&LAu)Sc<zQozluE|-Hr;o7Nnk@EWe)#$+{=@~c0_xN@kt90cWf?ooh#&aE8yzXiKdxuyJluhoqt4m?2M)yls2%Twz}{+IT@_WjPJW-N_Wk`yUZH1K9ROUEYJecODnAsaT86e*Y_g{6PY+;e=hi=4crp{9k+U)o40w{COM{yJ(!C``?~CY&u%oE#a0C$>{o(dPW@(fg1}t(9N2(o-4TrW0a8~U%@2GZUfZ0EL}2}(Lrk^H`ovbO+rqCY#IbF~cw;vlRnW*BOgWZdzaEEUt#x(R$#(w$;Rdj-o@Vf?8_gt{1Y<jhI+{`Gyi@?%GfF{tku!njbQJT#g4D4c<s|e?iEVCIMOz;(m&mEVk9^Y8=f@N)%p~|dm0Fq%u@>J&rGVUF^AjPt)aE*vrcwvl^65~x2HT88(L&a@@2d0{YpN+LQz`=a)bu+n1J6#79tJvLEZ_o9wRP@z8zD#(8@owvrUK<6gCJ8Byouk+aU1Vkr_~0$E}a@))vL*v{u24RTExv%f&%|63fAqNQ*`!XjZRXW88!(mE?>ttBq+SP(<HaU&Nb{B`|ycoHlVbpWq%K1DKYnD<g@P+nsiU~IX`78n-RQhRSuQj8VAsOw+>r)QWS)cm|SEGP^(Man~j%}Yqu?oN#*(_ADtzqrI?~ma||RdHtSsc<Nf;m`p@f3d1uivBWm+enl@v>2>@3F*NLzdI`0Q|T^+FMz%-+7cqTs+QElSQS$f?wgxrl?_<=a#_J_kCI%`9~`nSn1%NS1fK>c3kZN8D?#l$H|Aa~0Mq}@>#bFs|^d+nYTudWx*6lO4(Z@}bU9#y1U?J-h|4kbKW7`nUBJ)Gk4Ze53grii^Kd?LY2ZNPS52)unSwSd8)#~r52S#@TO;EJ>vhmEZWpcf~2kcIv5cn{uPUyt(RUq8S8^y%}f`Q`nSvCM~3wCj(rKbzk_+|}%PTk|3QP4l=~ry^khB9Ed;cOZ?s-JFM89QOPcdwrr;A-Yx3N(q}#t}Wb!^D929wN7@;><{b_bAAvJ$p^|#Pro_HUp~J7`pHcnyxIZ;_zbV9>F11o0wY2DcaDiZn?mr0^gpj9$CLi&-@e{5x)ZdMdo#4EGW*-tz6APV7I9R2(c9r3S=r4H`p19y{f8gF``edq{`|XnA?(2Jr_BD@cFz@%wb(AH8G7{+c${?mjkpe4VlSF=<^mH<p=txhy50Hf_G^;1c1??a0cR>I6J`BmiJtK85x`N+`t=KBs2={B+L~T2B03|xO=Fz?;+PaNCUzM)bygr1OQYn>*=Fo(;G@VZ)<go1KzLKgV!#uC3`ru_GnP8~Tx*x(NuUiT_T!vyGoBOzHkW(#6F)AhI#@Z#DJuS!b%b`L_(K5v>E|DQ`t;*^J>IQ*YSTm=JxxJt6YV}u5%tx1dWdFV^cSo;31oqrLVba$m*?E6#7&ImWG_0;m!hF>GYvB0!v_TY7^yTCF1rpy?WL~{-oV3wDc!`p1GtWA(P2<Zz4nLZlsh&>F~2C)3O5fZS_HR!_PyWMt0>#2wWQdu#V;3NeB_nDH&dHCndbq^l363(fXJ6w%E%Wc9K*sn;H(hu&7C6`m@f%$5)z3!HAS_rG=26@{9^LAVL2g?i(D|{{ZzJDY?kKvInOxN-7IIdX`h>@YQo}Ga7f`LDffH61uFhcQC?_K3@S!yM9(+oiC+8960xldZH&f^{OzyT>o2>Yor5<;D#>OUEJY45s_skv{^i8^NQ<9th{&P`6AAU%kmhSAR+=Vr@s674?d76Bv=+Ss2I#3lp1{iPV{O!WHwnYLOFrJ$k(Z>n&+j_AgotM1rS+p*HCSqkVmup(>;XGC8bWgL1y@u*s=Y*^u+8lU%nSUVN#0P$7TYHDrwJLdSXh+V54ONV@7p3diwJpM2PNI$oJx&0><fuLm1y1pI4>^G+3cyP1_S87+JA~&5o~1ZIELUMqf716^VAw@@VK@`^7Iq{_T+xLZBaf2Kpi3;A9!H)on^J)_Tn#n87&djwinpmD%Dg}Zhs-F(mmlNZe=Ktxh<F^a(|2zR%de9o!qVI5MfftN>6&q+WPBgLuG5$E+T?6{UW_n3;p69mvv4{O~Hh{hGTz|#GY-})QrM<mjK=_m7>9ycPeR`OaFu$to4(sZS}D2XqU)&(Ij1>ue<|wwq1oD4?9CNZ^-fig+tO!byXf9ti9ik?D7ovble6urxl`s@q5Tq>C!^oeaCm|mUF07#@Dsq-ZyG;?xv^%#{ccOW0;nDzf-?|ef{kk!YSLM*SG3ixC#aTsq~=+oqXhAEZ!S4Z1d{=9`gcsK^TekL#9bK7v!rc9wFQ?FxW9eHN*E*po|g7Aagq9I?7q4rg8N~sxi!B1iz@P9k7qTaxq6o_Q?EJFbDJp^h2P+m6Xk1Kd$x2&qH`Nheq&m%+P(U$(QI4*n#E36>J5X?ExPIeHofsy#L4dyIbtyCIo*L<=@taO>BGrhw$(-c_H30o_Vo$_?!Vqjjd=lMksbjh0(ePd|KAOHfMU><9Z3kwrD{{l9rY*0ZW7Yoe1bS#Sdb(vkm!rz+MD4IP>p3NpgE(kAbXGa3wgjm=0HBW<ju`^pcSZkSorxpvcJ#WIVp?*mtfo8scFuZUSYyWXCa)P9v3K_B|IQ3<Jk5!aGP_sGuBLXq<NAB0$>XDG85r!MHv-vu(qQhEvu9zXz+}+*+j&ql{amKzt&SBE(d+ca#1;a$yM|9~otY%0peTX$1^Xwk!(B;G{F5yE7~`AMI~S9kZNTsG}j4cSkakOu{5_xZX!SUs4-lUE45wEX)6)cDx>Jqi)LFo^KCBo5yqFVu{YGzDq&tV<_Skg(=0N(T1W=XeCJ|($_FQrS5a$eh8HcZPYd-2B@bG5-(_#mKist3J=JUK|A#l7Rw?l7Dw5@3hj2dnXcJ&mtJi-9C|CEUqc%Y>q5BY42HUk3lJHiyNu>~GS^mj8Rb@1Hu`1HfZdJQV!KPIfkzazS)A_o1_Oi8y@JRTL5QWWH-rnYYubOD3veA#7qNM4^hA5Mfj1DslZtR!Io3(O8bKFdMikV<)M@Oo4sliqtpFiof*=u9G%Z@Yj(4Gfc$ezrtg9^{AFi^mU)LsRttjlakNG{86}$J5u_f3CBwS{-2^7_{_hdomvAh^qZYfLe-{iKQ4r14}Lq!~p<h1i^R^6a}+wLw}T)R%Z77Sgh8Ntu(-RXvkx}4|e+A+_e8|B+4d>Q8tiVV6gqAIeUYLK8v6t8$&8?~O(1FolSN^>0S1ZqZ1z6)HkgsgH<N$vWsrh4*0By@Z`DD@0P)ATZ2Qe}Og%TOgjYHO>3U=$$br_wfEK?VQ<(Ijw@9VY=Gwbw!+%^Ar>Go{(^y#g*tBC+BxZ;=+a%ggoMr5@Cf|Dbj;Sclo4VJN!eWncsPRpkvEbiHR;1UKfpcz)C{7iar1DX((b1q*SRy52p`J4a=<++Kp&z%$bhAp6dajfy4NC&!io`UFI!<Z;O=M)unzDj0Zf$@;syi5fV(|Cie}?A#i3aATzOZmeU%@B&z>&PS*3;}5{{`+WJ})uo0p_eU7Z5WEB+k>)pBpiD<|r3eT>A<vUnf~##@0I7?-l{VG7<h6X=ILmH)g3ZX%p&p?~bs?rmqwn~Vg4*wpaZm9({2*2WO{IeMVX$3PL=d|i4)`wj4t7(U-PGmfj;#xis*~-8F`ql?{<^(f>!|yj56yrvDuUqmJYbQ3!L|r^(|Xw(X%7VG`|jwXkYBF|!)-Pt-jesA%oo`arYT&n^Cz&`YJR|Wm(5KAcH|0;EMlXMe?6`@hi!2Jk@=6nrRE{Qp;M$v#OzHQ|D%@xuzy8Rl*Z$vr=9bLw;$^Y-Js~MgpLb}#VHj)@QMlt)ZPRNX~FHW6tJ|x;LW2QR!un0z|v$2QDS^KT|OP@)O%6?!n_!#`~w21C<j?70qAwp62R6aQcvI=KSduI(ok{@H~p)*5ax-_E<}FV+^EK^Q9s@jOMCW)7c3vp1KUS}5E}~tSNqqU{ms3d$Oc}A$aa5e)CL$D|BaFA=qF@ahM3Jc29Wo;bqcbFc6_9@>2YBV@}MPgOfv}gy!4k|rVjCRJ&n!uyE*4a_Lm`yiO~U9G2qQxXEy?ob~wCp{Y5TOCx_jJlqrn(cng3l%)yTPl24`hyH%wyvcucQ+EJ)5nW1<#O>4TS#VOiBKvYe$nbDnP6T#rD->tQlxE|(xnZTz4F6cVMRz>QW;zAJd0TxVw?|^{`h;_o7v{~1x#;#=8w(I;lk+9n$bflCvi}Wt^V+6a{tq^?BC8TH)h@xDp0%ME(lge@g4}BDq$BJT2UnmzbmLuI%kfNX~P7FzXo!dSdI+Lsc9)<UO*(g=2pjbz_z##6}Ysq<^H5E7D@mVXDcwEJx-Y3vCvMga%{x2lb*v2ouDBYSSUI*QtQ=_Aa+4Igt7lp#0z~54?keGv*)Kq?NPah*u+U&OZdKPllaYU^zl%gaJ4~C79u8~{>Lqr@w`n&H&*&-;L(_VSBoQlz)-v`!*=vjc#gc(~ZwsD%V-4`-NA^lKPS7N?dRUh<n*ij--6La&oTGB|1P|+|^zWJDaFQ<_x2*$cvDH=g3+F~DaDrpZRp}RZev9WN<i=dM%Mn~qDm=ud_EBjdT-mopLIq&<WCNF7DG(P#(1#^fBQ4V5*`5Y;y0!o8exZ2?(X2yW<=$iBj1H5l&We&2KHbx+mn<^@uYMg!+gcbXtlljUyjWQo=W#U1)w?5QL#09<3qJOO}%jgI0`TQB~`7q_m6rI*+A={A0%8ac1=rj&)&YqBG*9oQ?Oqh2`Ac?Y0ZSJD<)DtZT#`bct0|k7`h}<5_wt|thbtMFhxW!V%nvQqQ)fppKM*y)Bj}eKnK;l1<?(fG@ZjZNz{XBY~e0dZ81oLCYoa5$Uf|Bq`Xh|x;;wU%M7cD29BxXnoW5*#QI^p@qQ-rzzVeo@GmHQ4N!)Mju44mJ8<-9KN)W@$nBZi8-;gI|8J=-%a_s|~j=A$0)IRq^NfNkV?I;Jr|Yb;vzA63N7&F=*TBri<9yPqBS)Vq}!z=r&Fhq?y>Ul(xeD*?Cd&YC;5(}ed*gm4yBu5c5p;HX8|Nt8%}z*Ly+@LJk}0giPt^sJ<yb9qxCtO9PfR4qh5FL~G}>p{S`n1NdIW3jY#O(?KAXeavr<?hRtBRP&`e+Un?WY+S?Bf=z_ksO&s8J@14|No0SoUUqgWq5daWH%()c_N4b(78s&;^7W~q)#C2N~@a4kVAr)0=^EMzS|8%_S%7Jf=-x^>ryfyGRt|{mjvG!?Qn+JcPcQ^ryg4Nr~#L=u!mxYIXXRXhlyYF_&{H`_Ly5p9|iOe!I1!FNF>x#@qLBo`}R;w1JoWpFasmWaUrh+!A`u_I?T@sr_jQ7LUM-xC>VL6shgT=vo3~O`o+>~HH1(q3br1MOvpoJfppfxzOBnD`rMbfFR~j!nh8n6ZB*6sUa&gkaO_n2$!0>}+mI;!I<Hu5AekA!9rloQg*A%Mr<osE4y~cAB_oovc}~yWjFN9I+MUgz(l?>D9DnNB%A6X{S!H;BQA8Y<SLSnaA%jVRnua>ANTpMv!#xJNbQG{S>nZKM74BX9Dv!BbD9dv_w3wk7^BOlfw)KwBw?SKYVs=`+uH%*|)8SMjhm3-(qfW_fw`Lkuu>stPCF7u(V~$T#hRn83Q)j0-M?UKf#cuNl;azj4QsqJi?e%%UV;*DDaY4^giPuJpG=p0K%_<>#vVQ}3;N*Hz)Ak(Dw0UK|CLdm7b<|Yx+RuSg`O8#8b~P^eMIi@tyXVv0<LC;J-PUc+v^>jvN(u5tO_*Ag*DdF)baoWZ`{Sa^BT3dcg>pWW^PHe^=&KukkY7)My-u6f@SkRETKG;<4xR9~K^SCB+Pq|njc_HeO}@p?f)k_$C7eC}?lIt9R^PUfENl3&qwAFZsAUM=>eL|!o4{x~kdo{(r!|Bm2i-M|prFa+f%_+EZ{x@G9CXO=3?0_+QiY_Saf@F#2Tl}I%krcQ%e%k})RU=1gFYkZvg)OIT0jlg{q$zN<cMnk%bx2PU@ZH9Q%`CSx1*|~zT0uhv7bG!KXqNFe3$oY<tUDE%*od7s5?sS2P%$B7l5rW=p&*a59vc|Eh>E|>qzi>xmh!f?5s9e+)UC};?}(X5Gc6?>f*j-uA9nO61^^%w=w}@CEUX7t#81#0clbcfkz|9?j*9S3eR+H$bI3Nxep0F6ZYhsKb0sRs5RD&zw(RBf4~p|!M^Z}R*I~;E_0vA6@R%YXyZc$u#$DwxoTL(T-MMDWG*m<wJxDM`=C=`^4CPuHh=*q&hw7-iixcW{aA8Nc^6P|eAySsBWgTPfeXK^30ez#K`dfgBubKR$9<1BnO-QJGESq5JQNSOE+IgLGLg#s8V%Wdk`VO31=U9P*t!k;jmnfBDZ{D5BUjf^Hjx>^NnGH;$R56`{`p-ajsS(<3UF-eS{cYaW=rlUQ`CmcSc;+!j?=FyFSPp4M(_#f#|YRRpg-fK)4|_WiVUj*)SCwLhV2jl6cWb9QP{eLq9_z11;{_llIood6R4TvA7N|^Bp<hir6@47rq{{O+y{-Bu5yR9b(`)Eg8rH7fZP9TQ$qHOSg0n58n&7Ufh3d-XCotDNFm#nr!S<?*vv!J#f7UrJlo!xwtE+H7B5h;;4}-hAx}Q{<@@LT<J%u`vKfj-$!x@&%h%n3V{rGo&@@B@VBc%)YEz-qZ#-QV(kR^r+rj%nSuL)&_>3GFd7lV(I!f@zu;u%UD?-;(rInAJ@5QcE5R|p82mHK<TIVRIfp7kgpEMS78OCJRdh)~ifQ<lpSt+>m>^N2<hj4VIvpxOEV>_2&Qak;)3V|lfq~O`Z<o9I3FXv=tRcnfiJo0EH2JfH)nu9$!Hou|z%k^0XA|0_#)dgc@n!o)wW*JuXkl~_`kz-ajh`)=+;5M1$({n{1$H=+0GP00xNvCs3_e5?i6k~8s8x+j(`{222ZY&)+Fyqii8Y>e3gGW^_>Sq+J%*@6Neu%RFQOC>2qw7PRbaF#-Gc;A=jE7RA(=%t*m`RdY%x}>CsAJ&QXc9$V{alP@llhOgfOqrRUm&Ejr{_4FQ(Dw#z-H{37mU#74?kx&F&=ZcI|-l;^?}*#0CVAUU<2OtNIOoIOJvu6JE(nxr%4R#9@awbVm61>`M2DUGk56{v@X;9EH>!{Ux6hrG%p<kj)s@y$Cs&!Tscuwj|9XoEK$zv!XdhoX>{!h%%Xs8TI3Y*hZ5m@gaNR-j5)B<GOhB+?-$RqH~{9TAg>)U)Gc#_Kjxl`pOhqCk=HY`G>q~(<(VzFqPPWe>WZSC@?$f1k*xGUxO1M5gp>aCTHa^`HqUzX92ap@?by)UAxGP=ZXBZ)$kG631B;h{f8z<^X-mJKV_jtyW5{F^#E4>Jv8>;{%v&FC25_u&d{h^my1B4><j!gVGwa3<y!7ZYSW8((nNQgvvJP;63|vFQ>SKI00a(#pKv_*K*KE3!Rd-Wg^Hrv20&;6EG3G`$0?}GKtndmM_0?@2EPkT-=KXs9`R!w-T(f1#w9<Z6C+)ITnL{+}+Gl2xw!V=3(YdbswpcLY!(wlH;^s0>kVf}F4@eL;{45NC;nO436i<Oy#v9@+nDob3&JPAN3q&?EvwYx0P0u@WBN(NPw5LJ=>m1iS!&VhbUH-x%-x{XVKa}QE07?Ap05}U%h?`A=Sr|@sNeJUU#p_FO3<FIO-(7q{!Axz?bSY2&_*{Adsy)M#nQo;=->eZ_ktySTuoVFit_00!bAEWt1@H2{Ki-i)zWw&oAK%OmUqJTT<1PE`{nu~5o1eefF7_B7$-L_~&5M4l`KDq$t$LgN!v1jhg(xL+w?_Odnq&3-&(}Zy@)#%<U5D|sV=*?abPNN%7W)kT924eUe@sv(Yey+?18@WcK+0SC0DqXrFxI?krTyUWXTS$<nSKrbqd_4q{_MT4VhlbaVcXi@vEy>IjZUKih0NoRqtzBRC}Y*!+io0=783bAg#Y>Om;ChmFTeft!wmoJ{r&F`Kjn!T9;-9T!hXabvDqf&%?YLphwB7kw@C*Sg<vW~lcj&)9J+d+$}Cr1h{Vk~@ffWt`2)w$dT9i02Aqj-^N10yX$xDqVxW%EU!SV~`PVPM{`|k+2lU6kd<L@ihtPL`$|h;|^X<`swbsZ922F(bZMWlej2KZceBzML=c2Ew`q8;)4_oH~4&Xdadkbf7{<J<faHK|xJ|CMtdRw;AsdDUOs06H+SOiAs80xN)DG*iJk2qMd=e=pw*O=063v+W^q^4O_xmzc-8J7s=Y`r$HwX}#C0tdz=>=*#qRc47@0dnx!z3uaD<)PV7Z=VSU%J~bK-45R9xapqd7s1-o(g9fPs^1;U*hhTT&;@9k-f=yuHP0={qPJ1j&wp-neevyaS!H>6t-R2&iQ6+$RJSl;Vo^eOP`}8J0&>~}@<(1{c5|$4EOTDRb;$LYXiys3M-cqD7YwgaWfZI|<;n*oQSYN=?snF($9M<bPwu2vj~YF*C>b`y@+7R?aY}P2m@v(d>BEVG<~1q`Mxi5%HfbeLk1vjq;@HSLLC!jYAze6@(eFGl_}MpGEV4Lete3{@96q-rij`D`3br?!JW}tH5CwUc15I+{M()O~34Upt45hMv)N8f&r;(+k5D&{L0j?j1P`N?bHtL&cy*1F0h}XfTHh;ygZd1ov@_t<rz8&7`M!k`-x;`S@n@de0!tJR9dt5r!htd~>F`Bx|?M_y?JJD9%@R%6ow|_gAp4({y1S&=1G+>Nd#8N{R0jgB{Ok})qrQMvUqMBTjL{rMxz<^R~a{mJ2XZ)h=?UVQ6iCIUz!5~u=j%Q5QwZU*~Rw(}907>3kXg>b>oG;i`w;iIph%;q|T=Lz@RK5Zxhr$F+qw;xGNm!gNWNX~1V3_%%{Mmuc>Q2=l4*A`><}v?;!ZC}})?!^LkV0cFkDEOelJRG;WDomrKsDq#^0vi>4LKoVH#XXzq>e*B==tG9OSt!yUaXg;jb8dnOgaCU!88n=ZAK;+@i`ZcZKa`tUQ(Lluy$(LV5Acc;e3o6Th&21hBT=syCb}bpzC^^$j|-M5Ug~R9HCE2Qk-I}OCph}5rvh7^C;ts$W+V)TliYbd9zCd)ZWSWOc}NL=}go)>4L6qQy9rK)6!OERoCDIQ!NnQ0uMVy-nl0=CDmpr1&%giFKz>43){jp;&F7rpW+Lc8bmuVry+DtF*=l&uUSwrqMgR^scvKbjCQSMPW92Pys~l;ZSlE0RRW&*`pL&6!km}Zf}<-JrNU^7vOb1gqLM=sON96an|H7QI6BtZg)ip}a>Qn+x0rlO`ZxDr^B`?@^9c6xE)h)YbzOARxF)#_i({5h=7Ipr^RRawBu|QtFL=)^u9tw|fk8i<pM+B|hTw4$c3MQc9i@#a>}j1CQoQ6Ix2U8_hAO349y&_s!cJpM>%(i&G<OAJX5+N06~<|rRR0yd!H8J}m@F&(*tqP^E%&T~FPJE}BtYp%uuN0wLt&sbjd2zX$(Rlerur=ITy@xD-xDls6khpUdeQL|o2dEXt$Ey!cJ{=K*D;Lk+2a>#SYiB~Eab~qaeort8q2__n!a{z=RqzjqvZr2#_}p*G1pzhS?2{ooS&>pk$_20vy6n(Ip4LVb8pAo36Y~@3=SSOvr?U~IEG>*6z)t~2Mn&}d*`WP3v!_X(zuBs=Mc8m=$12VQS`)hYEq++eGY|jVvILufZ|D7E!??}R&MP^$~<5u6~pCic8&=mU;p4S(p?>CZ@?|w=|<E0Wrh2Wc)E<~<|E|`{yu=i6~xRGOuL<PnPd({iJ>s&vgc_79iD2Q>+`slxkFk~3=2s&yWmU~fh$iO8~=(%L3Td`U+BKLIwO<h%X<F1OqA|RqfTYXsOm;;cucNF!2yWKp0D&Od&iOQ#34B}hF9dIrm|u1&W$H!i3ZJw$0&1{o+^g&+=mpceu%MV17xmY7!TUzGn>WdcAG&R<Qbq(<f>8@ybnhkDBloqhm&K+>lCZu4pu=J0Sz8hI{9ot^k-iOzU#pf91{xV6963S<6YWg@SErtSc{dGD81~fvwys8ZmM~ZrRSM|DYA|^gk_I9tlE5qWR`HDw-&i1N&4@@x{g;~O_;0rV#gM^);?jA4+U$*^X#gi&N0x1Kv(}f=w4G%M7HrJilE!OD3Mo&u-5xdtbxzRC;`|!?e8UgK??&$7mVDdE!HUZJ6LQ&M&U96h@~JC<++X5Ih{F$8r2<X&eVE@1YT;NI65bRe0N$R+I*~74w9YbLfC&oU_7r>vP9hq>~;p!uClQB=cZig_`z_eI1kol@TL38{>>(ytdyBo<7-Gbr0x_Ble}HMzkK`V0*SrXjQu+pdCALzN3QMYakls(XM{y+?#Xa1wO3!Ss?d>F<m*D#IE{vFT9(eX9R&<ado+}SRUiG6Tg_Tl^^LIB6BXYAOt=7b2G?p+@iU0p5f6kFpJMMZQ7&v~NN6ilj~2G#93lUmXW``2cFyBA*>%u$%P7E<k-{a&lsY)Y&V6f0PLiE)5f7Y(NMO~ZW0aE&p{BJ$aB+D52cK$YokL`8_qBLeIU_@3r7=t#6Do41Hq(aAI)r#@NY-MlRh1JbZv(HK(n^tRgpT1ZGG83U<H&EARBO+y_u7ZbQMu?qYJgX`(P{VW&!(Q0pt#nd4oOS${rH}SPX(MOd+gcCX2DeAX?N|-7V(DJ<4?d_Or40<5dn<g7~iNKkzSoyafFH%swc2M#e6LG&ts{F@PNntnD4Sm)U?eq$s#ZS1m+ZgWL&RWP-dI9q8=GwzClg^IW;;KE~CeNM)T)Hs%%Saegq`fA};}^#6lMNsiB6k8JCEg&Jfmst|jUR=v_A<lT0|oT#HaBmjQ-IIWhmt708W2+gG8Mwg?Iw>DY*=9t{wKlNT$HF1n3=kNPvOoe+z;5=bV4aq2^x&ehn@k3L2mwPj)=m`k=`PQV`gx^=8HIqg$l)3B|0%Xm*4@ITDC-A!e^Lp3s+0ixLK>lkJkn0E}P^feTRZi6Pd9FMOC$CEa8(CmRfFffeeiw~X{Gy4Nvdo*ak`e5G>f7c()*4fVyMOy^t&cYdG$h+KUgmi03+Kglz%rNF*$ahcZ`6S9c?>7U?!`RnAK|=$(O?Q_Dj81A0xQYAxzhlr-X97>`;*kPrf1~F#Z3qe{->K51nF$z2$sf4T`2YONUlTRiBq#1X)Td7)aP;E=Dv77Lp@Zo#eJJpy32|BjV(Yld4P$5|Hn3H~bLQ+_6JGPMJ#{qwxK$*aJw~zjoi<R7j3PiH<RtsZ^Ef<v025)b_Na}cEC<oUfT6Ix%;VG<`=Sd}G4x@7Z7e*GbCMCG2DN>W5hH>@G$mGd_$95{gA#TA7j9sz3YE-b?QxrdTcCM|VXNxgaJT3^q09o(igpwU`$Ju25kvTpJqHPhQ_OS2!@}qgX{Ddn)qJcX7}1^&{=tKbsT!?|5F%LShI|E|f4!dFs?DM3>~ZknVRoR7^E7thIpoik+(O|9PLr-l%Sv^uwCMKJgW=41`eGbUfPM<SonKkF&fa(qY(;hEceNK>2&Se!?n<rrnjqj%TGLN*onzz?%?jl)al`cR$dYF7V_>U_w(g;mU^zp!ipSWJtSfqY#tuT~ED+W-!rya<)pIG##Nj+TJLY*%4=1Vf5T5rpBI##WZywbXiLQ#2!DQecx@?zn^*m3nIG>QBid;J2fQI?&d7foy9I^j5G*vy1li?yc?dM$N@xvkx;PoTC8gUc<-0-&?snwtZzPIw6*S9(Yu-W0N^q4@Sy7c}<b?JFtdt!0ac%levOmR@+GHo2=-Bk7uPW%pgqd$0sC~Q@l=T5>eP=f`L81kus0T6Cckuhwr*bM-l@2)o9!<<x}0F>1&V<(*-K7&EX)RRn<N=~Jvr9A$A{3;}fYFO$C3@K!65vrCCwfgEDT1HZ1&k9YbU)-pM*M(&tNU4~XQxFL{!AKnAs>)V(f{nY+ZJ3e-6A2OD6!gh!d8il@D$C4e?Te!cf`NFje2i{9Qnr^KOi5Xgj%WXZ0~t1oM?f2o1xQ%nI&>UN3c#g&@FcQvW9fzmh4lN;s0!vtX}s^bD0Pw#rA|OiGNioNDwIvf;jr^{e&YCMs117Z07CAsmJVh#+J^z1Ge+P^*ZExLDkIp@LNIStxl=;jwJvG_j%d^biC}_T00Ua(mZ(JHNlpcOblySSdULkUq)J1`p~H&!<EV*uHoySE>8rb3dlxeT8LG@UY8efd`n+Ea&qn(qgaj(%SET}4o(+_<sEIm#fL({^X@S6U;>W|CT@TeJT!T6Aa~Un31lpXJS+4L>{upt4;DD83>VX$b#xUk24+vfYlcP~IT+Ymyvs<2t*Yr9@=%C<Zb6ti>pZv8Twj^S?$8`PYTI3`hq=|@4YuDY9i8R0g0`3Y=st1=vFGwz%bjbWV8M`!Sydi};xYv7ULg+*8zQn{KZ41$fxAnazJNR{w3En?b0IAb0!6~8@61AjH^kae@gCT4*<xA=jgB71rN18FpG7SYq;##iHti3tU$3=ZSHPJZ_$aUlLDOmR+m%C&3WI5On^<GE{e3jl=BzQ}i&p5fY4lhVZHmv7qTAqsk2(1TKg-q1W&*)=aJHtE*=g@i)K2#OedEK%{<oUQ7-q6Qyezx%lHgWIB^=NQmR+I?4WpASkDJ)>R5%?6UN{4@uBO-`-8`GsqV3>TKWUufbmHsb1u=6(cwaV-0W%!(+O+dFb?zOm2WL70dSkfeF3+a|5fiL@g?B%KS%2yEp%$qDcl;ued@+?jcgQf)CNi6Cl(5K2Uk?P$~UdxwwlyFjDc+3hMfBSqg8wL!J=3ojXiFyRlgovy7+m<2hCS^vLm$S4f35vFP+dEcJS4Hi8@uk&u;`m+YFyQ9ct=SN0Y=)?6-lNiE@VHAo8xLPRhC?ByprO3*^dVfgKVryX?Mg~T9gH}ZB<~SDP4p0@vu*GkKk^fA=V{JJBYEkP2-OiKUOqIQ7od?gH*^|wZ;&{=VUd4WqvE(|6pcsH5!b(cj9;KYW_c4m9|uZ=4tgBifVD$?N<Xx((F`WG`+nMmr;@|!ZL-a?=3Wk6%-vt4A?JOM^|xJ!3bE_V(9&b>$Czb^VoWCwr5@?TY4L=igl7FR$ZCW6957cb(@`j1fvz-EA#4vgPlLi45vEYU_;BCeqlIh~T+rYcFEmq!5;|2v1AfXwm7#Pjwdj$MHoq90Qif0m9p{N(kUa|<Q*}a@(h!iK`n|-IMD8nXOdzP`1K&|7drvtJ%9?rVMd@J?>(c%;6?|WYEg`h=@9SPE!`{=q!Z7u=pQUNpd4gEtva-uV#^IKBDeg2w?vosTCZJr5!QA$Cj-#4U7L?8tLbjml83P^Hb6I<!u=X7ZB!-CJrAk4ckIXoC(;CojN6H}7*`T1#?KClC(Q`z4=7*>I6QwQzsC++G0{M!~@Oc5m<JUn5L0uqlXBSoGh1X&k&o>P}!kkMP*UqLda6*V=+H2e%g`W2G0>&+oaDnQzZOY;SHgi2D9W3~%GM&L^y)h(9iMe8+VGS=WJ$y<yYfqoVBEu@*$dEAb2QbLadpnJN{Z9eK&f_{^Q}d)|QcUz#rYYqhyLi<wY)$czkSMlcpW%6S@tA^SUjRXj3h5=Lo{2Jo1pZ_*V;zX5GSyycQ&tQAP_!z2B?~ajl(N0pPb!O(#s!b?s-6Diw91mkC^xf2a1Rz`1Py>;=4CnOu*t|s+5$*JeqgH=<(p%Kdz|GOWJrtJh89<B<K))Sc~|D4^IlrQPs;_0n5yLBo~6Zf9Im;8t5eLh+;L&iA~Xae_N2_y%Y-bxEafskN8Xue3PL$MHz^~xe{3f2vYU>OO<0CVV1T_kkG8|KCXng(WM<|_X@Fx7+-9OlCG}?!B2CkrnSpuva=Irwz~t(?zQVlbYK@6LWm=gFXmCg(_!#%5r(>elB>*ImN?>sdTA3qxgGg4VN5JCh`bJ%TByuQ2o^lNqOG!5(2j<4kZW&*D`(&YY?%v>4R|$r$zCoE}lC!YhA0TwSuv$=nS9^s@nG<({#?Nw72*m~@aciZNJT>MuOX`cG@-n4ZSEYIEQeR7+NqMgsL1}bXgqmwvbUNZxTM>u9c~C;~xG_hfo;$OubekOfL!rBgo8UbPTc0okrwFE+5?~%Y<sa&Wl(N6}*<jjERMVU1WnCjw<&vw8b_g0Q-M2yJA1n>q5R*O$Tt&YBJf{U>WY@$rbVNi9h30&<C&|QJEz$^bk?J|A)6z6dMIA~${s0lJj!C76hDk)J-V5fnbe7{#caYJs@sAB=lxdk{W8`P4^$EomS?DyU@p8)wft#`X_a}p@%pTj2$mkg%2G$XqiAW~=CVA8F^tiL#@^J$1SYp3mC}(VGB?ThB-+?_p3!4sNKg8OClS(#a8S<mGsc$;k&N54qz_u)7T=;f)D1vmj+WDT!tO$Hb&*AlbU<;#=^T#V-qkwzJ14rgoNKA5IoF(L~!KVNyIZ(ZaCrRZz$9}2$xj^V2okT8K(Fa3a5=R2-sj$pIcxdzeOn0ld>X>aA-^21E8YVp~buOC%eY-^WB*J6d>rWxIbY;#ruP<cT<z6V%e3d}0#m#og<#oU|>yWr2pA)%PGSy}g;p~OGVdd%11nxSfY-%F(rK~5q+)rsZlGt&9*;x^07STp%i+&*nEo<2KO2JAQAevL<hyZ^P=yE*c@`f=9VnraT$&n#eD0kl|VJ<i+iB?u7?xeD=XAr~dBIAW@*v1ITtOe_W3peCOD2cM+XkTiOrPNm;t(1>c0Ug<;VL-AvH=l_FFv}?kj(-7rOE|OBw`r)62)T?E<e`&Z@Q+?zN+%5?pv~UAvckqyy#8aknQfHwM^OmL6EiSlu{_l&b=YkWOTJ(X4_TN$*ZuGR`1bR^{_=-G4;{-j$+EAM>LO5I1IU9|oT&ED+TJHN%M%lJ5<C~qaxj<;l_<iD-(@TEJU)E?DR`>&Uh;M$?Q68vL>=B)#4u3MNWe7x1|d9kNX<(_3}wqW8Zltpe*p6}B6|?aj-GJhhU_US-KZqy5mg}w;z{n(%grbpP!FkG99e?wGS~1(l{?+b5@n@BvPX2o6D3tY(zAnY$e%PmtLP4LSq-X-%=ZF}KTJgv)5Ng?IzY<3{b0OPU`bV^k8}7HT@t<X#5>{*ffPsLviu&SAkWIwvQu7CrqD}_N>t9wKLW40cFJp}FN?jJlwlAsG$`^r#~2rx!&z!+^^CgA#32xh>}$XEh~=mS43*1A2gbU|JiK}h#p~d48MhfcxW)JBT{-(ME1CqQly}i8vV1OY5j8tghfuqXdmTN%ZF~B_rSi^w9mWoMaZxtawnZfhWzONRE&UTfyP%U?qW8xcn$M4|qGZ$?P@KHL5slPA<}Z#+jgmZiOQVLsR+Ub$4_bx!%y@iNrs)`S^uBWJ3nzB*VKCiErAHxRKCwl1H>GwVMndL#8{mwrDpWF?=@0O=@yI$M%SbPVcf9EAz_AK;ZP=qSbUG<&imaNmF!XWA_+UIaq_i{nNF1%1??8~&aa6Asr=jL3cII6A?O1h`vB*qnAY}AO9Nh?TQO8cCapq2WF@>fLBOa3*cg%DilU|^)$p1hg3LjnSslz$+DC-+DfOB#vU@KkK_gF`*j#1_o!{@zhC5M5etf|r?e4j-wZA*K3q-)^Rmhl3dI%a_tVg=zUF-GxlnO+V}iz+3O^y8e(=lFLydZK;0tZNTp1r*HJ1@Ka*A!_Xp8hJ=tZXVY{+^&WM%3fWY_f$S#k?r}Q$_1|5(r`OP*Ay=_Z*=2W(FX|Ic_(ANq&m%dA0!N^m&A(%s2Avje@rBfnV0i)mqb-E%Y06+;<@6XQ!_=B6?~7$N6TqYowTY>OLxUkFVJd@zPyCw-^x`^B!;<>s3gG?D*hsG|MksKb<!JaU|*Zo{qzz{O$Hz{M*n=9{XEEi??YA)Wr#GK`iJi=%bhucn@7ao-^HaEW&1^%r^MbcoV=m-#9psC_b$`$DMhQ;0le|Np?S_R?SMEc5NYKeYS`Id=c0FYBm`9O%F>#NkYSqZQ+@&n2+>#c*n5w`yr_OJqaRk9@Y71?V6gpwB5*=wJQ!!s(S$B;VNpG;TB7^)*~6<fp1S8FLkb1XqUz&Pm(wjHhNMs6^pdi<8Vx;7VErIc024_`qNt!iuCqL|GBs=D)Y2~#Kz^SonT9utcE$wv@m<k-*0`(LhF#>OY9CP)$jP|LFa|)fzKVZkii|Gh0pYt)w^Q*1V3_s!8=x1sbi9mxslnKnyu^r!suOKeF}@9qaaB1tS&;%`beI((-ARl~<rws)BcqAVX4F9sPJ8>ZfwAqK2tVe)sk<CA`Zo-_LaN;9fv7bkFotQn+2J+nVl|7gFe;TqtvZ=8_|y=KF2h^wiK^2JaV+(Va4g4AyNHY#bGwqc*M}GLMEJy5wl@osF=v0C@I`@^s#>e6I3TU6>WxS$xbRvneWDt@ZC;Ea*Nw~T+L34bxD*RQwQt=G_lLRlfR$)NjNFhFF%$b06L>22ui#_UIc?7^%PSAmWq5&J80kMiCMem`<oVLe*wO80>OBFKNFq;>RMf7^q>_z72F1K)lP)&zulcMJ??&J<DjTwe2%I>pwv<=Ui%Jrp3>PGDGJ&zzT%wxOA%Zv5i3<W#u4I4CBJvWwlq?~6znpPKibV~uo}|E1E<`@Hp<22Pj^9&tgggrHjVCxVTT5(l`B2UnFZFSV+5E7hsW!w&AT~*uGO1xBs-1^8nuY|4L6d@Iicd84&V-ZDP#yWlHA)ynCOrCgFQ?Ej9Vtf@e-!Yl;p&s@3{yNhMmu+&R)#EQ)KCG}nt<CJY(n=m%MHJg?R(K%TU5dXktPPLd{ujNUO~y*O#*WQP47z_P$2!s&?hbTkwfJHwcTjYFOlp{ZqJVJ$HY?14X%MFzct?WXAu`on6wr%?iTWE9~!^o2{B#6M-n)AAgA!~1*Q*C!hE^ov~D^XZ}`YFp2<A@iJOPmM&)D#G!T6X*ntF7o~h&p;5zdXTiD&H06%<EglEw%+niwZ0Ed9F00*=mY;c&srfx+!CvsfQ+kUB_Gg)`A$W=cCEF#DqagX332mSIqgDomW0-#19@DoU}TxIz7xMu1dqBUo1NMRak1%`gEUQ69J{osVQJSGKWy%9O`n%Xc01?s!v$G|3?utMn(giufNtd8tMpT!Bfe6@rGN6<6J;KCnV_c3vd{LDDG$ld`0XHBJce$aP-S*<-J>6I}etOJ#0RdVWY4;}3o;j_;vzqqf{`a{k&GK0)Q-ZQD*FcQ(zCTctfEpw+)h_MuV&6p*4;E!(^SPi?<EV)NIni}3AObz0dZ=iFdDKNRf8Md;K$V_<dbT%(7)lQEOn1D_~gosH55yceufD5zRBW7NP5qXmIg|6T-@W3;!<yxcPlB9ee#y`IOaa5<k_s3_lGfTrAWY6%!jYcUFL0QPj%V?yY>G@20D+8nHByf)uh9yT`daTWKPG;68!`gF*1PG<q{1D4-%TRRAEdALgv{bPaEbT~A^-h*SD2b~1h|X*cB}Vh&@1>y%Iv<+DXhhkVC@xhIPqCcS(vSzSH^_!)HsF@^PUDi+(y#|n#e*Prv#vEGT4JShFw9*RKd_mW`+?|F>p17f^<T~pk+0o2=qt||fZp{AC|D9NjqRP7hD9huP;hP@KaKJ*#JHOP3^R%+!RMq8IJ$rdXtlq_b1&ZrJ@WuLE>f41t2q`ma1T;~6qLn!(WEPQ6^>X&;n8C_Qc)Q^=yUZCz>+Y_=U=w*au-(qDLCGha%^d+fnsC9W5|b7jbR}H2^LYA;#D6nEIDSmMLsN@z$F9K=E6U;?qa`@g-mQWfmv~8I-fJ$Ly?~~dc!0?fnfoI-Mfu+8g$wizk@U~_8*~YAsE^Cw96HOc1%w5@ik5O3p!QSbd=YZDQwL2%PZmi20s|`4=JA7G4#0?92#(}z;6bm@$T{YO19ebzVEIbcm-Z&nX2kDgsdB)47HfG0IcG@Nt<J)a%(3egQHb=d!2k<n@NvPrd1uehOT3RGhpOmyVHHNo7$e5@YHpZHaZoDB7A8$izKR=C~J}9w#}#y-NxK74fT-Kpj;9Sa0A9MrEtB>qpqCH8ShodKZ8Z+%RQ;bI;UY3p6rlF*Ucn=wV!2{Q+l-+a}yYjkVpVyEuH6^(cZAa8=X4|yBmriR+v)-5jeh{WD3COmM#_;Jtw0FiUA-cPBSM-gy^y3N;m9uXxh!kh!aU&2DOdC4BCCh&ThmJ#3NjWUJVfQeqdxr8FB@6Hhsx>CXGiJ41DY)dS$`lhuU)Jryp7W3QV~);H@*lY^Z-&Jr~_K;9oZn+d~d!oJ6-<l~O$?bIxU!`Hm%GHMWJUFVMAq3HqPtor!#oC)=}@Bn6Ome09w(k%nDq^?XdsJ%*&^JT*(0aJ*+3C;`95&X4YnU_aMqh*A)AQB0?_&jJ`)^Z+$+vnvr{e++yJl_qHmkHMM|<FcZTG>2LBk)!ARuYWy0*5_26xYX0KR23{vy&X|<v&|Bd`?ERsXS$Dk(R+ZX_fFePTt_7a_b%($*&NC9)nPlTe-#Bv-(fHnh31?0(#fCSK4!{ki<T&%`MAOJ7j^h8>nziBC)lE8p?0ZGH4PYO7h&?wJwY%ne?f}8AZK0DU~505#$&<o{t42`h_v4p=S;G+-J2GADRhX)4QUBCDA}DhfjvFV$(ATO1zDhIroiYU$~q}+*Yw$i6`6qGA9y|>8W1xb)~21W%RcvTO+#M#BN+MdTA!vAm}oFVF8tkEX%L|h!)@G%W8Otivciz-_Q}Oz{sUiJe$iPQlHtZvy)+H)#%bF36B4?I4S>*7y=!$^&(?l%|6%y2WD9XAY^}x=uI(h7B>{mfdHElg^;oG@ZeCVY7m}=htxcTU*=|`~hRLkW%zfomLD^==LIS#cXt^Kkich*=J?KYY03WB@6vsiW>ayY`o6P+(+`mY48y7w$&sX?yK*~AAh5_a_jHsO}A_ZfNt}r`KI9YFVt$eQMO{msgw=?JGI>cG_V83Z9MfSY}oSO5<U9J8f-+ue)k8kFOAMe1vJ>LJ{-hch}JANva80j#!{-gA1Sl2P*YEX|_=GRSt3j24U`L?hH?aKZe_n>q#Icv=GAEe5kD>3Nt#Q&YWsdBBrJ}z#Kq;*`|m0^`?meO-p7;nda_qykV+3rhj9boJ0*&hzMfz4O{*Oz|{{1g&#JYp(-obKyr>@Tn@L_8Hd$^RD1lUnVqpH9s#8TpwUdzxE(#EGIeABpt+?=OG;>9GV6{;L~ao$TXSw!Vh{3}DV=qsBVKJw*?-<Hh3{4-o=7BVn;|>f<K=`7b~H{>yJa{n+YnA7RPo-s<q{Prv_su67+&#@U=d!hHIBhWF1=i`m^!9dN8+SJ>raacqVpj;_YDXSi4Pkg<l2{r~*ymtTMW-|wIN$G;rW5okl~ubrp1x%SZ<=5wS)wSJ#=%zomv;^gI$HTz<jAMg7g5?`Jk-Ld_&R(}7MUDM_}z?MWs2Sz<epbHO=Uy%8|&}WTxht1TNKSvLr7>%=Q@A7wEUUa;}=e=pT-|f0m%>oLDfM?Jd<;>6Fk|5KG)CvgGH4E<cb0|xECD6$t(gcu>#QZq=yY`+eYtKpr{Wvj(a$LCR@sw(_dCJ#WcC`_s9poy2PQ<p(&jRBmJAU;o&eOe4X%azQ3yx~t+I?IjfSvOekp`CNH<;H3K>p)e<UWw+^F3br56sCLI^r|>DdKUha`A@`2s$?HJE<?bUXyx+S6<wMPmiYc8}lCFF{)ip=t7{O&62c3bGW|7mSI?9c%#W=+obPV`|NvvuGbbe_RuqRvuWVvq6k105p^E5O-B!LqA_$NK?b06DT_=&reP~Si0G3$#A7T~#^e|mqj6Ly@Ktj{wnc65Z$6vqYLKmtnC$P%w8~qShxodAkS)<)0<IQg?}}u##%<3Z4E8M!&Gc8kVUQ(K8=9jmK|9!{WY}QUuUyt@@bS}=EP<~DY>xY!f87<N;pBcZq9hvkNVo~08i?TYNl&Nq&9OB6<YuH6<Lv+QZ}0Da7gCAGw4+*t<pDw9|8vQ2A5L7v7CJ5`vUWY>i&M8zI>aVAKPSe!v*9KkbC?>kPU;TXq$@apDVl99#d#m=sLJ$7sn<Ih&3zqt!x{HLrlIx-%!fV*rT>sZ+Nq%vwDIC&o)wOUfc<?ag6i!~LzJ+vrN*EG0sk|pE$S)ZX&idml<>kL&}y&+-g`ccA!0kp1ML4J`0yz>VvH*ptOBAY33Z>&^VDFRK+#54*Cr-{jqDglRg3CkN0YWAEL|`)IE$y!l+$ZnuxVWLU3O}(oPB5gUzma6Z+#i9emG47<Ub4bh=u+Mn{X6moL=w}PjbSRxh;-_vO&AQ%z>En=IKl0DorfvwQAA5yq}#!&mjzqY0}x}5qWB%-@NN`%xTv<KA0Jf{Y_G<nKI-)jF1o%A=>sJ@ZqzX8{+B=;Rb__a~01CcN@DybD}ayOQ|aRt)Gyd=0(l1Xvrm7-KAKYt3xucnZ6&YoCdL`t?>-^bU6pMMHz;c$~fdeGmb3EhkG8=yyulpG%bsaGh4<q2cHDK{?H`va9`2gqW<;Uw|~Be$&~ZS3%O6y1aL~ytLjKOC&S{sF!h|*{O_0-5fOFcu##%rN=wJ2xL%v_gTXEtTqL$q7-f>^vTdF$Fv?BE6LPL8^shv<98AoPtzr-V01hvBnD(cFIiO#lf5gT#D&pYybCcJ|Rl~bkN5R7}L-)mx-lAV%7nVc)*$Ry3^IZj+Ut0dX|KrVeho$%rHT1JN{&RiU#1=sNaLja(Wix^fav#2hUT!-f4&<cAZy8jiB=GHl!@#Fy{cUs0k6mY;B8UG?%cvGHEzAXW!TUQAfT)@;#Omi1qAbCA5hUfA#|QEwn8R~wz?FeayfG4Qgep6m0&5tO81REhOUQxV1M5pFZTE@zcihuaY#RUtmDB7lOQO7{Xp=EHFd?-lRn^|YI#B}@wW)H7fFOyr&&MU!SiAz~pPbpbVQZu~e-B>4y|vVY2IJvkW!hpCRcCv9V((V{eazBBhZUmsns;nkla^?Ci~<NhQOt68hL!50{f&(nnOdmgDbk+lG)>^|>6hy^>TO7Eh;??uYI2xl1HOUp`$P>6&8BQoE+VB~Lg8A-z2+K@zVFh2F<DkIr|?ZK6eK9}{!N}pmm)LQETfqW^9w?M$+T@xwv68BioSr<Z)z}nIJKiRkpclDqOoN?);*Lrv=5AMxkQ@?H`6_K^U%voX}dm<M`Tje%m5!F(g~sMI@(bYz$S%&AA^~r<&pPN6C8{mC}$r_WWIypA?n@Wd8Jxy^1y4~y9013T!uhPcEs39nhcnSMOKHkX$|teONJht-!%$ZfwOB*f*mTz(RxYudC>j6=x~B?TEXcEPuo01SoE-_Cf}ftuY;Vw!(W@n>DiZfdF=x{kC8HrPl+87jk-;db0V<hIQ3%=tNeC@XNVzNqa*I*zvhOHgaEEV#+K3Vh0jzrO?8ZSr-`9CMJK1TVpAO|F%&v&_>_QMBd5nYm-pO?wYKr$<>}{nO5kNkLWgzJ(7dxfveT5%3j!(OC&`x?r0y7C?Z^~y^&WN2l1EXO45RehJd$CUEbq0PYe%n|`c=2q_B=1L^@(sD&p(KB1ev88Xb31vsB+=Yb9s`-mvDVbJYsIJO0n1~LE;F?HVPNn0i&8j<)_cYH<ZRB+AG$5Q>^(hthuK({1bocc$Up6C?1XWvz(F#P4Y39DocPtremhZ2zpsk)y=s<(J;Y6k}HVpx==^3)~e*h=)ei2{25X9HD8f@V8`|syg`^~B2$mM`>1`HAcLfSfnEGso`L$h<7LSm^rOmSTUS{gGQz4tl{EZIg3iD(yjHIFbCw=+gPV58G#z0Ar@5zKxA#{yR41U&dM}{=CPRbUqG+tu&t~KeOZW@@pk-8ZllJMiEyF%!SxMjRq9(v~4e%y(pm$wLlABRQ0_nGZVdB&ek7ct+YPa;f^r7f@>pbfN;nVjMMD}Jk03oUI_}zt-GRIUHOAVerP;xivU{;&TFni1m+ghIKvse8TqMTv-91l=V$AUNg&dVmpSzYo%KIo-I8mc~NtCDshftY*9SFWywQ<Nt&&sRLoMD#l6)nHih&|$1zqI&zo3J6i*S~}%LL7I<Jj^qh~V7h+|v4<p@3a>Y<<cV|<SD&x}V+D;CdY9~nA3TD7A1_U`MwuDCf%L3!UoW5pYxG``ZRk*g2b*;r5~x?O>y%7XHt-d&-|*0U3YUIG0<Ps9qaf9!iffpA<KOfu8uqtDx!8-&Syln-zKeUxD#CXjh2|7eBRCO_duFeU0{+ne81}ITgEtR$*pK9x$$iYUc*UV-nwB6^vyzhld&KJj?hP1t;FLi?RJ26>wY7ciNM&^@Zc>%>cUhjkc>P0j!-y4KZkQ=zTSqCl4O{$G37t>vif4agd_{AEz5^0weqM>`HF;S)_B*YD1lhO4FD=8U%I;~nREC41e<7pAX!f#kVS%XmG22<m9HJw$P*#b!1rB++Qcd0r!nGb{C^8m|0~t8&rfmIlE?sGmdG;t`3!x^Rt$;N0V1w6ZKgTMQOOWdiv<Ndf=&M~o`ffNkU0Qsc;y9yh=IcD?60^P`QUR7lvxRMwZdJ6?<8-zWy<AKNx482jqf|9;28oV%+{<=bIPg~ij{6wmq-N6@dx~QV{j6Q<m4JZ>Ipl-~YfHh@U5^T&LX*RK9)ge{8oHj08d$Q9ep~_;d+k$drFCk1lA*sX1Z+G8x@x-NNA&Po%Opg0^sLaN9P1@uL@>wL#=cF6dZxUzu2{NPXtqj2x5kjJ^z?#gg|0ZcF{)!Sm1yXUXA3w}-pg%M08*RRG0Gk0_}jA&T@#IZ5;(i0BZlRgFM~QFsWOi;mui-?G=woZVu^kZv7CdRo}<wGV!vvRvLt|)#NzM}2aQ-yRetUfYZ&`mgPdb**P`T!gP7>NbstGTKA*n5&GRB}97W<<%S2l<8HD{9*cLe}QFKP3^I-|tEt68|sblPWB5TW2GOoMoRea?(43=#wWz@wpJ~-Seq3;C3h0b1w(ooQaz+I6!k9q2>sZ}0!RCLy;2>pvDv0p|h-4NMuMjWNc6+fC~Wipcr|62-KTSC|`)esDq*8x_t;M&WuB!RXLfjv1=Ec0>qVcb_BU!b_#pDle4g!+CE9fmZcF|6T!g!Z0Nx3N6fLRo(r<IuxRI9J=D6Kqn#usozHfu-f71H1zgee|;S{!Oom9y2ePLV+%<@w&{VaLu%W5t`Z?h6a^7$=wVh5Ci3k-I}sZjvzpXz-(OVEO$QSXhQvx31jP{)vq@%Idn`V2iJN`>pY%DC5?|bP-WLw>Epioz_pi=Hju}SzT4Ad=g?KZc~j#t(|;oVu4}GG-I3J|k<2_9#yUSfJ8TRjA1r<`6HLio8J|i3pfi<UcTozBVViaaYjN#B0hT*Tc*kV&U}RA*Q<Q(@0_BY8UhxsHPxvw9sjsO_BlLlgFCnhZMHWjGSqO>sgil2>M*!)Sz;~5pk=3BRH>>LrCV)8>PAs`N$*WUHjCJ8jQW14c!KhJKcQ7R(T$Wvj3|kkm^$%wX`mMM5tWnAsNU^l;ua5L)^d_u?`uLICIr0*_Hmo^7)J#TUwO5qcXycsboQz-PoNQq-F{lnK9ACl6b7*hcq<)k6G#kWa^tR#w!IZK&wI9!XvHAiE&>ZYGc;el9LrGw~L7!gPW>wqEdrrbwhEg)Q@E35^qMT+_1&0aauvBXy&h7xK@=!dy1D7XGBEiE3OQUg*3$;G3a$EW|jZC!c`aU?-sRzpBS=2@D%eLn;&{^*a`Y9~Go`Nu6-NilPDhaUIpt|UDAwzdX#rv0i>XT^;lY?ZfVY;w~iTXZ?Sx4v!a%0Y3P>CCn|BJX;d+mT3W3C$)XszTl70Dntk@Ioemjr{aR0WP&7eb;&22g_L>X^wYbJ#*+mPlnh$6F2Tng(sh7e8e41j6H5sYzt6Rx|%WQDcww>}>tP1LQIGKey$Dw74a<>aYV<pmMf}f+ReGMa6!DDKTzaT%Cb)ou3tLr1-Q1$BSM9Jw{$=g0`lpTbyQ_*TtkYYy#mFARP8CWSg_C0M~b=i8xnbzKiTpk~Td;(-C1!yd-%Ya_xImYL?pponSMJ0_(7MHwEDMP*-%Ojfpftss&pIc&9cE8P;iM{J^%dk+jHhKOjq*R{BKNmeN^0bD7iRg#;RMCE%S$J2`u<O&vo@xI|Y44Hy`_Mib^}M!s~E`t1q_c#KpAJY?ahW3Jl362uSjE6QM8T?of4-y0Hb=r8zSZz<NCI&PV=KTb07))C;2>H0xJ4&yeDX;cN%o@|C^F%Ld=@Bh>j(hts)Zw;rZlQW2SiAC^QyB4N();XwTDoZyY5_HLi3LXBr;~`(19I5Ao)=0w=sf0kH-zai`za)X3E<MY2+Ma7wv5(pp6s2m@#ze{R1$2yGh@xN!v1D>vU_)p*$pxm{oM)Y$jZ^cvU05PAMCo=uhCC-Y_xnoPALQ3Loc0)E?Y24LGeOluQuJqDdvl%FL_NzzM)-Mo4iE}4%EiF&?nh%&Ylam06YaVtOXToX9V3m(Ijqvb8hGuS)u}gFOQu2-(`w2LeLP_-cF&wnTi87lbjvon<|eNRj*6T1RdedKBm@$*))<K>LCy~xqYR}*pdTC>tB~kDW>84w%Or=mEKh1yz6&ggJ*iegC{W9)qiiS^BHW47P4_%b_o*p+t|^a6Kml4|iJ>PIIGt(vI;b=}fI+uIkBZ<u9I-ehHFj{s98((gGads7`gxT5D-Lza(+gdE%=&VI_+wy2B~WKQe?E5(YgY|tec%5o^JMVGC1UF?5heN64&c~ns+-1#Odeh$Nx%OPDE`voMy_Y;n9Qb<<VCM3W-3o~5-4gJ3VmUaF06Y7N(<ixuvgdvu^DL*tTpjDG+iD6*J)(;qumNtqeGelr9Yeg5V$Y*ks^P<Uas?}5+$z`Afky8-%|Rvb&=V}7(gi4Ql2ACtJQFN%KOabJ|SZ6?@<)kN4C{L+ajHIlGTD_q0m72ChC8<4?BElA7s!>sm8udFwUZ6pdA>zz-%vzEFT`wv*JMeBgax8u~(_(?>RVyYl64U-XWWl5=l@K%yYrsZ8D{3P?;y~-zrkkgZ^1>e+f}-R0u#OmSehzPn6;h1bbbFz{TT_Xr@k2DUm|Ki~E2_+3IEp?{Se60|)u~`zL)(f$7d0dj1z5VR3n5YJf90yhdzcN^ifMb>Jep=wDgG|3%HOHqt0kJpSOVeMOOPm8+*g2ioi;U_R@lP7{?IJ97n$@>Ek9DMhSd+4JK)=(PIq3ugh#fGc_zt%NY~(_U?ZJV6Zcbb31cZcHr|7PdIrCvO{NFN@+1l8tiE@U=B3Fxn~M7(HZf@zDw(Lh&LCge9oXv2{jEQOS^I+@VX)neWm)Wp&fTC(wd?-KX~d+El##Led~OM!W?RsfpZ#1kU6H+~kY!kBfzEcoOr}|Fkb9<EG`(`T2xR5Ta~r*zu7XphJZK!Vq1j4VqWo%xpUPh{`%8Od`|YbdCDnStWWGQtG0FW_pR=EOA&8#j40|Q5h5O@s)MgqcByieYX?+{<;77_FzmKp{~=)96uJ;yrEvXe62#&tMtCJnNFE#@G5b%sl9t|ytv1<?-*qV0W77Byq>=^xMi9SPKUU@6BRJ0y<zIfy7!@9o=XcxME|1CxZ!!iGe|v}y=Ke}ZGep$G{8AkGsc}$q%1&nm%SVe)Vf-$9$qpRYspEO_=c_-TSFgsUWUP!_58_rH*MKy_bDsiXeEBnQ}&A5HbFs$*fMZHz_%jX1_;vYzCR0}dCgame#FG1jAeL=I7$#_)iQO<FeZh$CO<h4FjvA<9aG>SB{F52e$Fb;d|ZY}MK}jJE#js4QX5l`OyU?#DZ=wZ2#c+n@uYR!Y0=C?PcSY`qdTC^B#iC}rUIh>t!5CHA=jGV*yBd5CP%gf@}~IK#>MKu!(WD_SMvds0kHZ0>Lkg-ME$3B8CKOU;5Mamw&~l%wh)}YO@<hfgkjj=25?<{I-%!zy4$Kfk<kueyw2S^T(v~8K})4lTKwoHjYFRRoUB?1yf7UYA2uXCn=4qxu`eK_T}7;EL~V^?W1e)$9&+87wj+(2L=yiRE&ZHXdM5ndL_sl!RM5kaxm&4sYb^TCB@^E!7xH-FcwhlSr_XoesdVfml)QlDma!(3vw{LzMDq<YUJdvsH97lqpSi<hYD>CZk;So8c=F-r>@ASD@y-X6KG2C)B%1tS#t6(6%&}YDeU9e1=?Q=swIwN$Qj)KjQ)NC!zCT&qz}PKnW})_|QYG~iR1T7&Wg0r_7f9+MYbh;Mm(oLe8B@4J)A(fi5K=ifeK~fzlI(%Ad0?Kim;7I*NlY0&3{K^cMDLcC4rD*xS{OB7xJ>hZeZKJe5;tPREp*P$m(8)HOZOK{h4mPA74w-9&5%U!QMjOOl$>2&o;i%tZ_^^9<35z++sC^iZU&c4>{q<o#7!T$T!02ZC-i1XBslOihQtpHx0j+^0HbX!zZlG*iOdl_1dkSdSV#^jb_{0hRCBQ)f0TfN>YPz#L(MJS7qp9JyoX_<6JSCS?2mCANubTM-m`(7$`pkrhf#*SX)b;JG7Ew)fNhs0xq#DV!#=Je?8luKT>jGV6J;SjjMA~IS>+?!2l#oc+SvMx0_H_OXy|n?h_nvJQ@S}?{2Wp;@qLOOJCV3k=^i}ByY;bFg8*1>%GBkyDfLUc_GL&YpEETS2#2J>B@4@hqJ=|VvNT%mO!qYfwr32leq!4`=Vg*PUg`1)Tth*xK|6l=H7_;M)u#t~(Z6#(dKaFwlrRclPZz@uD)k+3S46<wY3|Fa2h*?lszVUmw2whqza{Rk)XjNxh8+F(baXQeAcKGX=KY5J`R!w-6XgY6GQ6N)MGLw#J)=^99FzJl3Go0SSQ~J*8uMt{J((PYJX{c^t;;)OAo8LJB$}6H>(bieri<%Jbh^bXuPmyj(b)M(m)xffN9ZKZ=xM96KxW9J{bXwz9q+y^sK$4{_j`DyI0>ZXi};Z|I}HvnWMCfR9vIA|8(qcrF4nJtY5F_b$|7Lw7xy2Af2xZDXk1O0Wdujy3$S`N==#IpfJEUA6Tu+)%8v|p`u)b5$!^aiXYB%l^x8VqUe<h^2?;0{0t%V1MzHY~tL8M_rWitsSQNo{Za)d8&bxqgx}xMy;Zvew_2(`&sG(yRXo?g88RxfbR`P=W|M9u>kXJt2+mcjj2DKHLGI0@G5t^yjwR2)N3&*bS`{SYi<J)gP{qfEG@Z-VXw@cmg{nu~5o1gb>X=^iYG#S@#8XJ48`4S~CES{Gc*w&>vM`7O}gj$RZE_ojKN(r0Lt}Wb!=U04FSw`%d*)Paz?|mWKHB^uXx8Gdk?|**%^DmDj&=C@<;jakN#<FD?7g^u)hlE4FeQLv)YmHf0ZA_Y}#|ZH+-#(<eqf#Uv>!ga`{rK3ofH>Wj)rgr5hI?(q9%~po{LjCB`Ss`j{r<^+{L8!$c3}5gW`FIpb4}S?tWS@%s7B!PrrS@%3}jMgqPb^o{%>r!f5BK!n}2M-Cf{S%wD}IWQxQQE!1Xc~{xk3R@Ce|D@A&u~mc}l>P0yN693eU*51XbFW{eGcsa;0i7ArIiOQYmnvEx#D(zcOTtkLsbYocRAU<q#kI!IFAJnKM5f7hPN<;es$%m&bfIzIPF=_X^`yPx=$?$PH^ZwI+Xv}<xR)&nfy67~P|`!B!!^y^_B@27j6()ez@{z>_a>^`nhm!<Rc5Yd6?HyHjHAkoG(YNHIpyC?haoH<!T=lN1J^c~kKC$;#1pdTakfWc+gb8R-MeRu<(4ovGN<{iLeRJ)!crd_`N&>V)NvEd68wO%Mn(2^B+);{~*pX=2y15)}Z?AJQ|FBZF**KRwH+NPJ%VEY>bSD?7Jb15TVn6#cW&H;x$dT;I)xxjo$xI}71t2{OYU()p1x42>Qw_$%mVF$TjQY}PTpnZHj)*uGOjQf;Hwb*qnUsNC;ccDKM>tOmqtE>)A$^d$P!7~e&iN#%*oTi!x_Xyz^I0BUvu@{$Z|N29!W?XWFZSr(-GdVNagV}i0|NPtg``<sGkbO~AIW*8|&OMZsew>LPb6EQrWo@-bg({GL1*dF#qWB7uGGX)5JA=vcmE2`M<i~a}<WXZU7d`6f7Jc8%of@*G4@Ecv>1K(rw6Li*y93kE3swUtX(<_xQ$F5do`xx3WCrO(O5Wg{6G61pU)DJoHjQ~ey8!d68O`A_oDw<iV1d9n4Q(>8UDhYKKM5pb>aT2#rb4YN)z@WL%RiwZ^fp{9Yvck6W2Z|ye@w%yBruj1lm&B3LYnkZFzCmbpl5hfi*@`3?Xs{0*L;j_k3~OB&_3h922$`EOa&;4sTsR-`$Gf|r3#>39|}Ivu403?p)?buh7N8IMpD_+M?}D`6`Cn#=kWqmw$BzKXhZ+z3bBOkG1OVD$$b!U&oJ<|BL+xLDcwDdMNc1Ed-T}vZ!TTMM+GUsXoLXuJP=Xd$pS*ai2X0XV%iZNLs?!|^_gCqZkQS>8Boa}y0SqPh!Hi~6o!2$+o)ATUrd&=#6~FSwkh0$$#!LK!ZfJH`8-T={mb+5d|$<4qMt^X+=m^N%FwG2)oFC355c0tvlBMDG9~G#hUdrYPc8JDcU_J-?LDpV_AzFO3KsL;Mlp{)qp-d>@NU`$7x3Y;+K|V&?86NP67p(~fS~Gp?&zEVdeFpU!u$4I?YV<sp4}k|mZ7YHSBG$3`+BB9lmVMSTH_h+>2eNiOA8W$!ykElR2J6pQ|A4-QVesF7(>$S)61wLQa%(FocP}yhH4B&`RliD|9pP{{$Us7eDuns&Lx=_r#@8G5x0I9Eqr56r@GAlj(HJgZa42!QXM{AV5X;2S)@cc2D@bN)fvvsM5id}Avi`Ur+BzZ5$%LzF#?oizKyM7AOC1TSRAr$^Haeb&@a$G0t>SegzNZolh^T6!@F5W!N)N}_qCJWqF-PamNRm)6&TM4yygqxj(NP<?hxDbp$31p8how~o7m#fQBHM{E8{`uts>q6931Oq>t)#U_$`B+)dE68)?wh&vL3g&<;Sk~s|-!csA6|4ZV+US*iHnf)aDBj^fQI9b#PvuNqrGDPiw-L01pxv2?rfI_awoVDkJHTE6#F3l-;R^p7Z;T{p`A@VTR1dikxP5(UX<5C!E16SYG?%J#B(!3PU=kwFPi!TCXChwa>>Tyv~#~J3X^=!`2A&a1UR>y|t{6hN7*hZ}@oJh-JEa?^gYN6bbesP>Np*>e#d<G0`Bzqn;>~Y>#%vZYB};YwK5`5hGIzdFn(`r3hrkXdV-n>o)3bNNtF9c0;(btR4Z(pqt21H)WfiS6qjv40h*yk{s1{u@pmYUhy3TF3qBWv@z2>6huztiIkoO2y`p>zxw+jH0({0V0N6cUcU$tJt<<*A4)Si01m@*>Xk4Wd?eG`it2+M@}zJx-D5X5AhVCOvKDanHH?2A5#`LF_8BgK9f)iht^Q=p);xp-L{K&)AtLEAjZf^{Aj%lh&_=E-PWL&@z#w$5K*zGM;r4Va&qLIx6INXG`{IYzr0jlr(zoG`)3f$^d99hA8(5Q#ut2a!sqw&*4fCsNd1EvqUS)d@I20LCho)L+uS&yoV;QcPTp{D`3VR^3sf%O0J53hM67W_{yK+C1(`x$$yFm-lR!@`~unxyP-j*a60$Hqfv<Vai3G!KEA<aeFBiq1|EWQUbC#pi0dS8)ury9i?Eqma1b7a;mc@*bKRWku05AU7!`Gu6XajqRLw6CFlX5P)b$kr#S^*{go%@L52b(TQ*B;ncQV(sBexH5Gk#=Ch;b<0r}GjxU~he{weSGTA{Iy#@pP*f(j)KIL}AqzOnW$xi$_(Wwoek7EA(m>vsH~-{VJ?2uo<PK~z4WOI^6c4G2*W4g06s-f)PZij8A-8O;RYR&DsVcEfy719NnhkoD%3t0FV_=t;YrZwwPtoFv^gVW|73cu3FH@8QYp@}B<Lfo5<rzq-yQVCcgnm?c{;MvRBP(je04LAktXpG$J}2ezv$(ln(x%KH6pf((W87awYSGsp*Mm7eh@|Hh$YCFuY*N@T8o$u(TE;Ykfpy<Gj7X3=zP<K)mdLySBJ*Qf9RO0dSNIlGLK)53@y`$#tXU+ruW?@bfLzeWWkcmzA|d-^?{R}svAzz-2Kjnz%nugEQiHb_RDFFFND9=AnE>X7K`~F(+bf_5fwr)Ri^oH!XTzyn=Vg<_x-OL#A9vA$-Bcf~l>xdi*340tNbF)bwG=XQu~I#+bDk=N_2^sR?<W|A#Q~~v`Z4N~^Xpj-Q6ozrP<0^|ZO}9UQeJO#BznefAG)<GYm`ROdjL-b`RnnOaA}?m-UitdrX~98kU(*P9nWM|aSO#&1Erp?$d+w2fii@i0DaGSqKtpjD?ixZ3O%5-LwMh_J!Mnin~36QihvLv+{Tr$7ev8oxbnLJI2{b$JZ@q8h+`D@G1HL~2W9C#@<^q|i-vcd+KACg2L1|!t3)e8k|1N@UROh!7M*`gjz*?SS=x<$z#}HLB;+)`UY^t6*&~)3l9WKWFO);MD6*2@Ip=!YpM`DS;rNtcRLQ_Jq#c9r(Z7(9A$y3_uYtgQR<n{`LPukv9r1DV4sz?H%CQ-Qd$Gz;WOx!Ux6^<@H-tG~rVNo}qfC<sfAI7endxv0aT(-3cyg<4Sd+?2Uaz}LObQ0iNh<R>uctl4GDHFeu=|<iT5Pq|<l+<w**NKGWZV{$=PT~K$0(r*+#o{z8#mqD77qMXkHD&olbUm7L=TSX^K(0Gt_%!J$TTK=H(Q^ij%rku6VTY}c?cGnR*~1SSb3fG#l+}~GDaD|p5m!J$<Xx_LKW`)Uq$Tjn|Z_rWfEc<dRAyM2LxyC^|6~UjeVOC0iwO+pIA>;7=cQ|48`D=9}?p+hd{v-Md<07A2Nkp=8O^u_)gx-ZG&H_ALSV34l}{+*@v!)fU3s6tv$sO;_Nc0BS0#1NQa!EoVk1}#MW3fIiG*<sB9jCo}Od-`(nRpjuHldK*5SHBeD#!>Zbgh&qfTDLOauJrQy+%7*3dsGSSNB6d^pfcno%tH;%$Xt!1J;WDHk*3~W#2{CKv)b@{y7nvAb!iI`Ht>|c;F3yYZ)PxLg1y)=ANA>c`*$zt9v>tK_I9TogERzCl*N@REMin4{`wU;7ShiC$lX>uxLPbtV`3Gtj%fiYZO2cO0QREA7DBm<A3uia%5t@n?m6FOzN8$twF2`^>usWY0ZjITT+wYCX#Arb75aW!elNNzz?;fg9M{!1;Yc$*Bqe|2i28^`nTQS=2%ZZ7X%C`1FNHU(3gWR$m9^G4}Px1eX^b5uJQctA^?Wkh(6QqND)GiEC#8*vQ0m(eiLtBt<f(~rXlPfO*F>wh8$Y7os~ud1VJ8-fmbMk0LYW{92zOI^$aw*<bzKFR`CR6@hU4iz_$XpqO&=GcJ(*kzP;jLC<=$fmyD4Ter*b$%_%$@zK9A`1dP<|IAnpKJ;VW`wywOU}3R5|$FjPPhRosHDjpHzM0kEjh%8u~U@c7a{iM@desEqRO&Hxg$Uy-?|+5`9Yo@Yrbc-6hM+z))GIa3|%V9=Aux*%g#1P$KZYU((q!U*7l^wPH}ad;`3eKXrqYs!jE6|!fzSvBJ|oVyi&}VC}=Onq<%By7%b1Uo*<`fbF$c;{biX_<mWqROAzh2nbXpV$~>*vHmiav-g_7(`zXJOTgbPzVv90MQ9Tc)?ZTpyg(<oNT>8`&u0sHD&Y+K6WQE8!QIu`ZC&jY967)J)%1?N?Z=;XIt(Epr%EJSO3v(7v^ct52*-D{mf@TQ54xFXlja2p}K}jc7IwIt1l7kHlIcnnN)csMFKgqZVZUpfX?&msW61)336pSbeDf+-+4f;#YcGw>ba(tc($he4H2s4*hSCdu8#?)bcR&0kB>l01T{722Ts0|<%VB-?q&c#GdFP7`8Apn+l&2kK&koC#pB7Zoit1z!ces4+dA?aX^ii4i1uS2dCfl7hd<OnqTi5jxwkJVxCMnYm&QdiugO%^m6<iXitwY4@VRGZIYOno+!m_!)Fy$viuRO$0jTPj8M%w<lK=k2lH3sRX2ck;e%rBk3=<e;XRB#k5a80gYbIO0^ew1Zc;j$!+39dlVzmgstDz(X;b%@_icdvB<)K@Z7pY);~7qeb&NZkdD{&OUN1EJ#G^%<XEfvQDEaRe?d$GQger?D*J4u!fb}wQ1^XmFFP$2-#$3ZW?`@V@ak`<!TD;>v~Ah9%Ir0OV3i%*GBC&gP#GNN+BD!e^q$&<@#pR8tEG$0&qz97sV&=m!#tUS;{_!ygi2wzCZ=$FUp?RSTZ<O3->eTR1;Rr?LL?u!(9+0z#r#4>%1wPGsgwKM{2w(uwp##?>r~Ccl(NmALQ3LSnL>L?KUytLq<8n!`}vR4jBHLNW8l>XhpBqPgt=&`tu-cYAJ&P5u!cTqz4=-jANv`EC+8xY1ScSAEZv@nHqA)rVeS?9!OJ=!9x4aa06+N?j3ik`r_fp!&X9p(PY%_yEMrVS(2m%hb4j~xGB}Fzi-+9&}`ovU}Fuz^FhN|qhV@B28@B5K#yG&e;*U_NE%jN>OL0pPxn!VB=Rs83!kHq(l>5P4(BkNb2i~TH8F|HlNwg<0_j#y5?{MOZf|cbs}2*P#r$yp&hXB&tF8-D_FQidlL!GkkP<hBn5?-}>uMcTMhrlC*r8WK01J+Ekdm-H`U8$Bjru)^i~jw@m;LpwI^~%@F0n^_O@vvCN^r|Mg?!cu*5npW^1j_w?oj958N~cu5)0&4qhMITe4R!w)*C0v;4&^*ZZmYsj^OOB-9;^ljQ9RS07ak`-+bT4e_I=<KB3WymK#&!Ch+iH!6fD0F~RA^g{^xAl?xv^uzT16vo)Z!BNfc1X<rC91f!=c+Q494!WTlH^f9|J-mCkVk+Wm3;Q3RDDl=s#3ZpFQ65b~&vl}sCfM8SgcpF^Gr~@vV{xQ$FPhOL|v=mtv0l}j3QnYhAxgD$6%A$FJ2!k&AcAr4#Z#;+tnbN9#+Tf!dC1^DE>)EN%jyS17tY#Qml1sxIM~kQA)FbySF#*iM0bLVJQudzNB(BK9*w4vc8~%GnYnZN9rctmYk>{M+V-g|Ul2UNXR98$stOYoV)ji7^01E)?5IB+iCC)%@s4#i66sc6ra?WLx&3J~g8fSPh4p!VX|JpPn43trZ;!9ZhT%r3T8*+>^1>HSO(fMC|bH&3VU5VRiIm<_D#Mq>)lALbh>YC_ZrSpGL*Q#rMPAf{`D#)U*!7*9#d83Dm{uLmFRYre=xdxml{KR=U-D+;q$Ac<Zwh_?1mv7p;AEhnSl%w!)K;~xFNpFdq0C*7p2qV2h@>q2Z@hKngLGRv&k8lXcA6(fm`4ad$e7=F(AWsl)Y1lXn{7fOW7dFjW%dw5JgHQ2b$<|BwGPQ64Fxn~MqN9i$dw&iSQ@F^d1#*Ym8N^4h4qEGiVPz+EUETDc9kkhB7ry<!w%BFAkb?AM#2XLpwwg$gNuYerHch?=|2PTkiyPP<)6DbS(_XxcFP|%z(dM3>1n;&+M>RJ<hwcN!ySn%mw3l*{ciVK_CsprB*f=IhC<?9Ihrf50XWxaQkSI2oT=|LsK4QlDJeP{-5>@W-9$8rsJ4%eG$@;c0>ig&Z<J*IcZDg8G<8%C22uOj_((-K!MUXQ4K1Va1GGX~uy=PO~nBRDrJ-vPR!FTYwQu4~{u{@IxEdSxKEF?F`Vx$lcY2EuUY|kg883#VGoewB5cm%1Rv)7EZp)LPW2Ol`5VJiE%DZWuo#=6VS4@O#Et(Dde;C!$B)hEgl`<k&e^xfyhL3}Hl#wS&_%cN2a@PO{*mNrqMzDrPDBt{Dy5b&+YhyjB0y6?~8)?V|KTKc#Rdl{Z$7!#B@wM^qOj7cr3$&dL1o=})-OyO@ni9(fW`l+ais~0ZAr1qQysVYeoUE#G5uEQHYZ?h`*4$DRqjYx5cJd>#B4VQ+_gowm5E%KNMnMgaUiNR&awT3z7x6x<Gv9f`5sG2ThjT#X5(0KUEu=Hv+fVxIp4*H7RiTC1OP%X=_s)hphjh?ejUoW<&;5cqF*q7uH!;WKsL+q2rJkQhJ9`A|Fb%>vLE*q3or$vRdf@%IHjYFRZnylOhyfD3Mr4MDr(voKWV_!r@8$Vgsm)fh!#+(31kn6_u4WEsgYP9TgX4#qKx21jvkdm3ChHd$Z8uNl_7k%fF`EZl;c)V~tumGXc6^zx@qG)onXZ*N~H6eNxl+Gefc#ze4codU%B=B0cbAC&@qnyRDRDAK_=j=^rMQXSZQ~EF``u}L+gBc<)PcXmdP~CGh(M`_)#ArZCj+2u+Mp*Cp9QgiZaU<;PW?T$1=H3D{0r}Z74IT9hq_mN>lol;cwW_?7DcqrHd@_9qxpkZlIXhh;$bqH<%n{}Mk2y|ay6|CODrGKuv$Rwo`*GdXM9H0L{;y9MUW3d=k+%f{3N4?{gA<wH=o{`RUK$=TKgAhw(@C65h0D4|61U6ClZm67WOR`3%e2VIxDO>m_wlaitHFg7vyOK=x$2m{EA9)z5Q5yO3$V~KIl`V+cTbP`Zu(BiMR<S#L+>^qk%q^<D$8+9CuA;S=*1Lg5SRye7gc#=_bSa1(Gd@-ee_I>v-2U1%RF`pKiM`Ml(2(pq){e_FFJ9%=Po6N9`>kCWKMhYSa@|4Vk9ZZdDi=^uv?zuq~<u(#`>pn_xA}2vQfy?kbEKVe{BQ}en?1I?QRObVd2Z-rWliQS7Vth=E<XY>m{6l*1YH^5j{TUwe9fl{pQS$sor;Tm1)nQ@JaBhiagr+ZsB9}Tc1t@NImF=Er>qjJ(;3C*`p+qRzP4h<v|cE*iH4S-R4vVJ<Cfa@gUBYW-WrLiusDk<E2^}YD6Y&oNC)(+eb?$Zb`CCG6g+dQGtdo=wAUdanBREDJ3Utz$0F&Itt$>ml7N-eUYUuKO}oa_}86emSAMrQrARBxSq_3{vA{jwa)4LxWo9K8B?Vtn*Ba7U`k7`+qZu(Q6E!VpX>C^e-#(n{5hG<PpEOb#NGP3&yi_w_64Kjh<F$V>ndNrdB0A7e*2i|M5)`C40ZcgF}E*GJHM13i`AW$go>057y@C}fa_Y#o=i^93|tVUq0>8KAh$q4inLP0)}=MxO<U)ci+)S!Owf!NctFojx>Q7Lcugm9n!ByaPiQE{@?@_n9q+y^sL+4E_n~qk6Tu?M=#PxP%6&u3>#~_^G`}u8|6>K#5MaeTUPjFRNd<SJIFW#3L_u4458WpqnoaTgj2**3Q^aQ#mn*?cZO-x13-RM~S(0Z02C<qWP$|?yTahW_K(ZB~IeT4LPDxP0H+<h8@5mqDe*5W<Z{~*|U*~<hRD$1s{r0>0`5$YjcoIj>{rXMgjvQ;gsgx%7FYL{+h-m$b{#%A>=;l~`|MT0Qe|ao{3Y-Ig?{$mDCK?huI9O`}<LcEh)5qwx409-JnD+0X3310d#9T@bU8Re2srBR{MR0w72IG<ae7_#|>Cb=p9@PDOf98Jr{g>Z<`ty(c_1m|9zK2>s=RP#_-gZU8>SWTGJ)Wc6P{n$lFqcVHiakD<@mP`X*tj0-(J`bjHu;}_{qpP2|NED3hXG^bxm&s0?|lFMAOC8c*ap~QFF;YP?Wak#e;O12aiFoA{ump|aWJN11fRR6N#5CIdR%PTR5je;c6^G;uB)H=I5Xj3wV+3!ra0D!B@84Fne@q-J$m@8AT9#<s<C0dhJV!Di^t8=sX;_f%2`HEJux<9$#!*lhqKW9Esc^lIFCzo(RnQcd-Uda1hT(zS>o%Bj+aDrz(@no-<416vc8U@(9c82HfZV9Q0#UeTLM{Mt)d;w8u0|iXZ{kv-#weZeEaxZk#$O=_4Se}C9Sfr>RM!F)SMTUuyp8|X77mxNj&CP<#Z4q5Oiy#b~$t@))4Uk-Zz$;k(fkGk${|0J&k75k>CH&)ek%G(fKdbD`m^JJxexhrG{*9o#tWz-RWaYdMS3B`>W_+^2UaaQq=#Vz)Z`L;Xh3|-{f4cO)rJOhDL^J2x^*{QAQ3wX((!(1dh^l6rsjVrqSg^c$Bv%3R}mAZ#v9`lihndwX!8>$m67qVBg}F+&>We_^K+g&l6xbBBbo1S2%ERUP9h+U!NsNY*6(kqkH+#xFxbIGW68sCaM<mI{x!-@9%$?b5l(f$`&XrW)ao*&Yie@IB`u{NQc_yFz&i{o{;Mbo2l%?TC*)B6n@NM8U~#Q)A~^00D8pynK6wjIStbte{31M38viFi$lS=b21GH>6*kt#;ev!JTf)(BQ_p+Ozy$a5Xgzfgm4?k7&=j)DuaiFIO>DJdu4#BseB^zsu>n<?bT%krZGY|qQ6R*`a!xWR$@3JyQv{`04Z}s?&9QM+{?vAc8sH_<4|}s8RL@-|2hU%gExqt0SXdKL(<AQrsdz4406&#Q^O))O|wuebbTjwv<;V>UOj5v5Us2<*$#H=JRqk;p`yxnW2GPVX;c$s_Qei64kYbO)z6)#DLqu+1Yxww{mE;LLuMrt`6eK-5!KOLVu?&y$e!_I?0ZjFo;B*Re@8;DscCc+M`67@kjZT!iQvO$6=uzehn<b2`rAFXf>(H^Il;h8OHv_Xnt92`SUO08X(EGF$pluM)4iG3zUC_sM&9iQGcU4RF>h&6FL3ysog=<d+7GJdfcNK8G#Q85p06_eyRcK9zf(rF9QL6|EX4m7O{oL(a~{4jsdM3g2L2U9%4=XPZVt`kcb?HQ|2yVIcwpUtvk25_s(L|B_Y1+&fx#{rXkLcZEzxv9xSEbpZYpq%OJGn?Jqsl76R=~equ^=WQn5Fn?ZQ<k-lAV%r?W#0{e=IX&uA5BA3?kaYykq^F{>EGO*XfEt`D2o;t_jIH9Y%_8WgqhG8%l~W>{a>t);kjunL;X1YY$K<5m>^(N0OV^yfU5LB+8l=?Ob{zCG4|f21w*VR{+eiD?<tikpQ;_^DEOq5@<~^MzQdn?m#(IQIe+pE-)2?3=Z_OTg0_7&`}uJ>w3&tOwaB-Lu*}vj2?g{R#Is#F2+dvJj6tElZ+2Mw-U#v;1XE3U3|o+xr#Sf&@RU>c?<-<(gB{(OzKj)JU#d2m2l*L)zY!7|SrtG=&_${vPp>cJJM)zyBg@&?B&m*R@(s`HoF%(jTo{bO5==0Cm1ItOOtJZ*0o^scl1QYSt|d>##CoH!w7A;zgd`^t{L|#BH<F>$f4R-hpl6cJqMmD8y+N4WxOQ&Xk}aCr_mGp#PAc%>UKj4*^;~McSobpBCHpWRqcyNEG5668b@7MdLUAtfnebq8~~lB5eaQ$G~{6b0cK*k(M$6-n93V=6*Ot;i+3Q54F!~0XH`?WVBS1v03x5$Z%*IT(UR7?uK#*LdIMoz{A2|pE3drB1DMGM-d3+D2NHc`px5%v3|$|tgp3(bAzS<!LbcaD3u3z0HK&3X`(qsmQpa~>UDGyf?cG}`!U>A7N!DJGz<)=$wApG(a;nSEGkIqF&dBvVj-7~FNw^#(U1VACN|4a7M5B#b^m?CJS7mR0G()`>U(tRax~M0eWQa-AR9<X%s}-tqi0WS1E#SEE!d(c3xtVUZsbZef(rl$nNM$`7SZ?T!AjZ@s2#Zj+Up^of#l7aCzaP7glW9l30SzqlRnQf`)B?ukfESOu!}vN7ulYEdDJz}5%`jc-NQGXFm!RDUrmNM&*?FpQ{8f0b_{EwDd!O+&(%pOgNm|;L|T?WgB3xP2kIEs+|x7p36FH%dZ-3s2b^eRrldH>Txu6@v2FbZd|a-}pjy!eC!tUk12k7;+J)q@eOepZ)rfSM5p#!r0HR!Gb5fVL0a4iH<y6Uy>_xP=A~%3t>RNTjkLLnqu(jR}1nBSFobz16L<kG4I3<q{w^7`Jsw)7<WX&;#$#bmh))=MFgN9=hlGnxr03mRsu^x7eEp)<K?=No=nU@GMY5P0?p8$mw3DSy>PQ{vK2`%STIuMgUhUqb71GSlE$Av+FfM#LHYkGPHOCO9&<p~74NGI;+zy#;3K~vb*0Td>EttJW#HMbR9xAjRDy<Slx2<+s7?37J(;vw!Du?1dVUC?kI!p3M86dUSf81FJJ-e);Q#JCzk!*wy7iUz^M=2H>pQ@+l5{$}emqh4yeqs+@yC1j6Lmz>uMm)uuh<J9J?0&xs4^z=yF5#D=RfJ<q6onBLeWeGs%dIuuWnEdc$N5E=EISifd?^OD|-Zu#?<}@_T4e?NP6p=zqf-@#C2V}<&u?=dpw?X!vDMaBqH&AzBmLQp-+-d?c_(YXT=Wap%8uL^e`c;PpJFlvHtWWNILN@`OKZ;=xe2~Tmv=>W3TiBb6kPXJa17ioYB!M4vV=h1a{(a1}!o-b~>2~mlZQqMg_lc-!EO@m8*{G+9pgqk;DnoZnC!(p))Te@;BdD4eZE!-^u(5G_=ubq+4D1*aZB4etnqD}W&f1Z$1IMfHMu7tmJ)8GSzNKs_%pkE-M`?f!&GsWIxdhWNKkHbrJ-9t2_r&U`kEybYm>&6^mS8_F0+eA?rC2m@C_|jmzmO5Hxl^DWbC^1W!7&xLIVDS6`t*6e!*jLZ?ibe%lwnrVqy9wReJ$Cb<xbH_)aFZOS7fvxN5ybzN7-e_`PF5pVFCwPH#L!dMq<ny5^lX8X8C?)WKIcUzHD|Qm1lRuxp$s_FT>g?5%{FI;WH|UafYU}z|h8Zr%8#gQU5DL7Xsbps=>{KDf*)70>;tbY@Y1mPIHWkDIof>rj%9d;5vc73hH*p5GNJC&Zu7;gZ}Pj)>;=33{0qdBw{xUC7{GHQ2|}3gRbWx2!&#yr>`i)QWNj%mV(8ON+CTs2YZrXtR^HVc=&&52^_E|a8%REBxEw^S)rL}kdkq)kKKf6?AwH>>%yyTh|mv(Bdj#AP=@{1d}a<<geQuScr)*6D$&pxNf_`5J^#bzyrhn|W0Wa=7ftFrkuFs4e;BxzX@^O!_7X!+QDg0d8u0CPlz^_6K^<wWGLLzBT#<)1#PeC5FU-AF=Bbly^xxzE%_YwR#Il=2z1D@$&T;<#7;Hr3PPLYSmDLFPSqH{#U}e-r2|hS%Dxp~eyvsCM3@?6_lGMT$DcYFB2VIj~CuJ!`uG!J_B2#)(n7LAj*b>5Zse)Jdax{=m!p%kEbI-R<pm{Nzo3_;IC{LKlPr|1+D|~!Ra_ue~YOS{{uD-uCt{sb{cwN9tDSJ<i+uU$$39Q%PAd(`jj5BnoL+H3HPU%FI?MX}2suiI`uCz`vdS8SfpbVXPLOeeZLm8Af@R*L?oRp(K^t08B&@8}tHwNLDLJnc|7=$*szA$x)I32Z4K~+WUY5{65#bzMh7=2ew$%=r))7l-A;{M`)!ru<XWi`FW5GJf>s%e041C_c=CnMbhl%Zo3H<O=qm!RZa;M-gp(7&~})@70@|0!K(L@8Su{Jh+c#4xE05Tn5ea?b4%Ik!SiE%82+IP{9<nd7wP)%#c$S*_H20J>f>f(>J?-IDWJy%eRy+ZCQ98Ao=_6*pqKPE9<-T(avRoIb*z2|b_9LQ0PLtPvgyNJw1x1XIvw#`VFfC*~s?{n2ACB}0t@l0i%>5_s7xC2)*r&A2jNCSFW&T2hQ2WXPp*ztQG1&3_rc%759yOc$UZdwgvdUK(cnJRB~p^6e<f0JNR0Y_qDf<2?YOD^F>S+*-B03tLqzr-Q!_;(B^vHU4BxwE$znwxv&;g!Nd>E-*37uAwz>cu28>wC(xqU)HUF4>ZedrXIQLHNVYjpZX+=aN!Qb0ALyrQU63QeQBj`8EQ?C-oc(8*Hmyz5BrkfUu4A%ELBLweI#~7FyyEooeNEb!mc?YRB%(s!&=?sP^)5VB74wH;r6HXaG<IX%`FQ_-9zyr&@JToRg7WG1#y!enS{r6yx(;gWq!su6B(UGpEgN#8V~1?ZBZTOXO+5WIXnTJ<UdNQF2_^~O)1qBMP)H(eR{1!Tti5(B4z#-G5z}au`Go0GsPXuYmwa%(nLaN0HSs|@5QS_uHl3V3-Wuelk|n2cx`~T85AXkm4#zs#Y8c!6ojqU8gLDznHj~XO|B*_ZrsMgQcacH*9HSCpSjFw@|<2)93r*La3}BERzg^;jya|NFN3C1R>5PSYhPD6I&I1pAa`W*Y}vhc!v<R&nZk|M>+85>Qd~HE=KxjUqv(PSLOSs_k7-o3UY_i4WHAAbcQPdCb(%V<H*^RLCkS&ph?L3(?@X;zl?xuUh3p||dW<p_(e>9RhX|_;YBvMj0ZmXL55Ip^crfQWJyTdWrmRJ7d>@qWT>vc&k&hv7&mmtgD3bY$652IZ_D&Vw{UkP(ZWh@uZVSBH%0ViDU1vsbFo%-|{<GF?s`)60RI1K%f{wedzV|_Xo#WJwA=Yja6Fy{=)+<Gh<a$^0rdBm5njl&{P0hpMLOw<sWy;ax<9EQZ>SU*qQw_<DQ@gLzVDZeU_-3BoSttk{G~YDZvL>qsj*6QG?I3VC6G|l{mWR$|c)vo9-?;fPN;H!Lwmhk@^)AqR^=0+kp1)dFy?9J3py7(29;W9ExmK|3xrPU(TLOqOB_;qrZ|9`$5%{szK_vhHV!j=!Dv*GQ<=mv~%ymkme(2)@Xg^ixQ`znVNO{a?$}<97{G<9BFSyQ08h|<0LXdu?IAn9qWeB8rx!YTdN<++gV*H+d*8e2XLmh*xa{sO?^cNZUON2*$wTF}MoW|On?gl{xX(|C#Ra!&vod^H1ZBWjHLMd_;<o2YusB47)Xgs%w2~Rh!UxS4Xnw+C|A(|;ZndoU%GzID+Gifkt_+TnLTc=XuJ1*-I8i5Dt5tDc((%%6XH*sZl6-97AQlZC6)|R&?6;B7|d5zmB(x5`pr~O#g1lNUiVr}3pvR^rmDA}V;CXGrbY;EAJGG<1AqPm0t6-u`&lWs80ArFpR8`XFFctD${=bAZ~BcTm&MrrFPqunx;wz%Mekv+Wo%Rj$s3I=oDuk*k7V2aDDA$Ts<{>*2s5eI|PFenFcT#63;YurV6pUILBXU^7$FUs$)a^WNZuFp<9Ya!{bcO&}KmrCg<2RU!3hw<?Qj+2`#Sa+FV)5EkAp~#@8@zWhsL|ITqc++VmK}*SX9_|0NIUM^%3g=xnq0=^Um|enH@TQS3ByW1#JCiQ&LiEO+g0%ml(4$ihQ4fNy3m`KWLcHw{^ZWjB|M>QBcp66a)94>R7UqAUW`ayn&I!J$g3_DqI}av0WnS_tE%K&9rQdkUhrN53aBUB>X964YH8t>f_)h<X5fO5q{}^V`Z!#3(>ItVPsa({74-W_pwRV~I7FVjS*Ga2lJKsachYWnp9C)8nGAx5&YyIOVh3wuNA$zopGk`>=?pyk@h#a5+YLZ+Zu<`A;gg)iE@6XmJUhq|nr5TN@co?!}c&hcZ0dBm3+EuR`zYJrtKr#90u7EHD`tcf(nlh_Uw0RjO6^X%xc-V92Dj~xD1a0={tesO@)hXcu(HUdW;tSOURe+H9(Qa}L#)}5t1Vo+%LCZvCER}!0l;?38hdwr2nSvQuPaQ(glY0)l<fUQz4#EIRtw_BXUkJ~A_03S{%ut!akp<NT&5j8!XZ*UeX%(FiGZ#r&m-F%1@y0gr%KJn}=gasOFUh^(>NfW!4Wwg^2xVA)_&K}(WOAqTIYj%IK<rSTlu@RG$w-s9HnXIU=%zbsaS~pl()PP81&YmO8lQ|1Ah6p(1=ua=Qt~pHZwzib_hvq)I*BpD!}!#;aC7@L|3CQgSaWti=QjVh1_@Uus9|Go6X#z{o(Cx<ob2^7RWWRdx}GF7e~I-hUjSN~T;Rqr=S7#q^7-JXvml6>mqd(kzuc=la?2QKGsi(B<MIvY<J~&M$7HCaLe!XPm^cR=V&qvvQVN}p*qNHwMde^z<_I^>`%C@W1BuhTo~xzN7tpEmEMNe|i;#_5)RC6si+R?e5x7F1YD(uk+yYJYF=~NS4$xGvKos~xMCp^#Ros2&W3Y?9#K=Gxi`L=XNbM5$Vm)_^=T#;HhlECf!4n(9V~5H@-%pD@Z+&biz@Ha&cv89rmc5wm#vVmrTKa``+y|b2WC5(@Z1gY~b-BYCAD}PUi%XL+$M`0hi=1W|5<Pe{2n?}VLAi7(H32fy;|p2EGS`j0lvR&`Uh`E)qlPWadqFMoWEu!B$pVRh1iJnSvpIT2yy@JX7yzi-_~=wQ8X0M~cNhkfWoW*6zcYV+`<N*gXIe5X>R;8NzN|%#KUzei^@AY-gz*E}HAz*8FGBRowkOOK^Xq9k5is|v>ba9m>&B;OFFMC1M6Eo;(g;^*zqtIOGkd~P{bQ>8zJ!y#VD0v^N*wYxG7c(fFNNykJ!Lq<LbJsmy)gN*h9x!TpRg|T`?v0GO^7v8Qu_gTD^KMFPVxE(9K%3U#CI0wmBCDH=zGDX{P<jY0xF;FZAq$q9nvc@Wqd3u?Z}cpa;O)>vK`a)=S}|n?jPTN`{|Ew=7%r6KHK9Z`|bVLZ@-(Lzafl;XZXN-`-bMzvaU^a6j)aE6+^Xnjrf6iRKgRHTIhED{*5bLo?2<93iiCDsjlDle`h}gl=wprpm{A^AG>uv+QqT^cmJEhYuwHl?gv`1S8c}g3!ftjYxG|O0#0wyt(<I*GUWfz@`r!}>kbQ*-v@rH`<h?9Z?hGi#4mSB@B;j|n5EQCY=HwvR?2?Cq8aB4(ZMx7|0kG$`h_NG^ZoPoKR;?L!CUw`EGP~9$FgOb@NI6C7I(d>*VvG(5Jl+Rb52Eo&LqQMzI|j6k2rce9QLtJDmC|ykB!viZB>tW;K6XOeM@5v{oMcg*Dt^R{J-Bn`Hz2@*uf6$e(mh9oo25&{$eqFtVM07{Ji@16LB+jn-P6dyn1Y?RKQrz=lIxujbqiWY4aU$r=liQrd&$sY#$y4iC^NrGCS;&x%@eL_;gWH_u9L)0*3T$?oGq=Vb_(n?=UPuRA@J;U;i8~rKj2vB~Ua>*R?@=Y)ClZl|Uy;YCU7!VCe7Kd$K%P7lH`Kn4@7_o}{WZ*1r4AUv`zFsvYDS^_t7fNT<MGn=Ae4_g{Yd>DR+v-cR>BrQyzcon4l2KgJTV#5!*gA+C#lgN0?FE;u&T9LA=d^RE(?7|qEVI?uVHS<-Q>a&dqU2s$<lw8fWQuUR~@LtWg1PmiYc8}lCFF{)k9x>1rje`t0@w~uaACPe~Knp?Ham!7rHzW3*PHR_X;tQ$MJ_~imf*F0DCdDOO9uGhi@Dw9=2k#XlzM$R#5)M%Uo4#o7|+%58n`I2zaiik35Y%0;x^x3z#Ve+?Oe}bhIxnRco=@jW3_wn@*ofw%l?#~jUz7~8jhSUz=k}5EYsi*b!7}64?H7F&fq2+#nA%-r*N7z9-xw($TxRL+-+xz?9AEJ1k&1p~vHXmt$w15uhzT~$LC(egN+lW#myB<s=I8ehRx1CsfG?|NcWipr=A^`f(+H@W`fF3916UnptSR=40qfN9f=AB^jzK$}b2k3mCh6I&o;-#hX<WjISH9h$@5_!zv!O;-xm0ucG{itb(LSfq-6rc(5Ka*;Xo@|`P(4Qs^3(dkJ5LmDUUOImo$9zFeR0U;CtjC8(IBSO01FHbid2#>jd7c_D2`C4s3Q5dFu#p|(sA^$N1pg-6ioxSLHC6AY5@0V@Se=@ZFi7eU3iH4Nv+pdUiLr*i^<}im)HDrHfGH&>DQhr@g7q(Wi6=P~$lMkT(YilI&6d4l*t4uBbcrx&%1W<-itgq8?1b%ROtc_MXZrjFPc8JDcU_J-?K*;*nc>*qB(di-k3FNX-X%zHxBS!K!^5nRMzI%eu%>U6W*utWp*d0WqD8ud^thAioaPQrKz4^{-H_D-8i!<FpA~JlDj3XohI_i41KZMs)Zp-YnWxsJg)IM$?=<hvWu-E{uKn~fs>Qhvg#|bMw}?mLVpIS6?b|=!!*t5|=#@#G3unsWUqMxS4UOdFSiCo;p7Waj9rFUVAdJLH&4@O0*4mz4N3kXU80?b4o?$x`(2m7u{N~XDquf-i8fQNCS?_}w!S8{d%KpsQf~J|s&AcafZ_v;MmEUn1_u&_OBU0UKI35%ZQ^g_9=ii6qk6_qznb0rLKLWWwHCe{npPRfkp&FW|ItnhH89KNZeEyof;!PK91;*2VsRDN)t*qYv@%D6yQffl%Yl|G``h<rbNuo?Ow1$iml8d}Ex86>OV<hSEYc#zG2oX_ZTYrg9%LW|gmLI#$nU!gjv5aaJ*CI$@Tdltn0Y0huLM;DIA%GE_7Xd)e99~Zl!oFZjK;jt~2?r-M<4(+MR<Pk$U?>X|o2VKXh=(JU$^3KgzwhDCuD>3p4By-u(`ks8B~fuCeb?6IiKXfz-#1DLdB_#SNjNn)O<PZ(!e}J>`1t^ZSH8imKRMTP3mcU%8@7CQhS|GqIn4~0R8u$d(OU{tQF1qr8R~B+Czt|E+ff;<z4#rQ*5qzlS*ZX)kLnT8&M-Vfw7;=gBU206vqYYkh&P;Zvn4LqZPeS4+7Rmyhb4EJkQyoJdbuujQ?^jkG(*!zF>PEH?&Ce7YBDugNS1niN5M_AXtW3Y1!|vUBBci|D@g{5`ysS<OxyNk=i<125sT5JNOOHCy^Mgn7M@eD%CqmXxI<Jz?NH=_o9Q0Ac_^xsap<jtehn2g))fxg8Pq<*1<)UnEu#gpSo`CRPGgZ325rpD9tOKV@fn_nkV2Wrk+A3<q#C_^_B`l*LUcGmV5Wdz1d})q5zsp<Q|ULz56A_A$J=ll#8ig`UtVjt=LR+fFkChu^p6pK#9>xe3`jT#{FuWk+kBuD&0wRU9wg4K%pto1cu#C00#z#loNzMXF`p~A(-gy;5(n4mBatu4xh{PZJ|!^CD1Bg^l6y=pk%}YwVlvtU7=<JPSgQ)nY1$*(pt~$g3U=ShDpJwuV0g7-fVCsTfFx@2YnD8U^Q5x#Q{qnU0p~cukAc;WrmWX+@G^gAUS#VdOK)^Ph;xKTW$LmJg-RGOxvXL64Xo^i43!Ay1_%U$wt)3eqHL9rO6Qw@8(JCE?gdCxY1v0u%|x;0$FSy}j^0mjtK(Th*%iR~s<(zyx#nXowTs2w_WJ|AOVB8is+`RYKt-W&2WYj(t_%5RYpoh~^N2!@k@bg<CZeL(Yg_*EHdqC_yj)1BQ8$SeS0se6OI^z|s9ATsESH0RRC!vfE~_Ea?#CD`&zY-RbGJVy<#p4$xmZk{psO#lHM|(4y1%L?Ie{wH+v=Pb_%`;1N-O_q(X&}v!(IGBA7>fWyrX^AZLh75@KrK%yGYtykbvCv04*J$SC=K?7QrDQxZA&c5M-k(S|+y{&r2WrN>z%EHKu20kJ|{u8lMJOB6aM(yJ$>J=Gq-g4IVmBhV@0oD7ct%N*|+HpCn)GmDPpdVAyxYgOAgV;N7zGvdJ-20x!&J=N>{$b%<K2kPCal9CfzDK8I7>AT!SwGtRJXo$~??)~iQN^p;bCx#15hAVhpEb5`V5vlJfX>hP7MBt@_LDu)O)5-Ek(n-=Fpo`nmzYHk2JL4ShYUP|OgL7R-10$QW2i{5#8s^eTQpag#NUXg8(oqJmKzYYo1BG`3GCLy;_WHHdm`HJM)RufQ0g;YnZI8E_4y=sO1EfUIj3AsHhQFGtLJ!KW)JC6c!3bPQLh{ip$S4IJZxWb$PN*)Z}JlJ6yk7FkHG1D2P>jKLC{E@~E=_hYy5)oo>eS6U<gCLnMF?p$OwyzzDE8xoXZ6a7PCew2xWiB4xd2XnrqRS2QLTu|OE3zT*enj<_U}{&4GnGo5_o!2jq?MTPjF+=xzjIfG_^~w$+qcD2XShwP45KO%rePQvFp~a-jI5f~#xlEpjr5jtwzHB@L`P|%G!1b}74m+iI=mT#YgNinWcU{cFVKike-(1BUKt{JSZq1e)U%bFOers(X})8uGFt;N3!qUplbXKT3t$_a(obnIaf(BYvYfB;s7p+vhI;f_cFh*EO&T^XWLJS=go^GyD8ayak5LL6IEmH@p<IAJCG2_v%<nP8NzJk|I+8#$6<~rIZv_lY$So&4TU-96ZhTbq6aew-c?gy$2LoMF#<eS1M?YQxiyh^Bdur46Btt)32;_Kdbd{yTkLXdcD3cKJ(X&F6bs%(guaDh?Y3$pC2$Sxmd&P3S!dq1u{xXJcrKcA}F?7YrjZqzwsYF9(#8tqV@?LJ68jxCoj#2I~_urm<=$dF;j=<Tqr&t2?T?TbTSY;k%a?&gbXb4?$Wc2*pVmSvrJ;zD;#eUTsWlsRlh1HlwoF-zORr$F`d|~Ww4V_8I(y+ZrTsKT2n}~#SCKsNIJqEkT8%NQ%)-usHJ_cJq2DT?MqCDN<x_n+WRc>EknVeF>+-Q(L49nM)+~(;Xfzq&|g@9L)%#C@wtcg$_c2v;SxFh|;Dp4{<>CzB2aC+^f$kjBO!DOm>3ME+zky=8yER{?Pm)C(PvH;b~QX~PY4y!sjQY?FL_XAu@nos`U?a!9J2SV*Uh_FJ&%NR0nKSFy?8QEAKY@w`Ait*d*o_;FBA;?2<NZ*=7D=fySQb;kt2}F?ZN+*n&o5_6pcfTgOwY(4og^#eJ>e6e%HKTH%Z+^iBP4*2#b4s1$P5}`JfpW5LP1hzN5THV!<SliUy9#pbmVRl1v8?q}pN4ZPIk?ng`sDF^D(P}W-KjP4i9OO6_1aQ<iBto{(CE88{c8@-vI9^qmB%Lki8!~ex&CiQX*5I<^Q4o|BY=y{g+S$x38wU#jNc^yz?tx=yC{XmicLF#wYYYm081SumSYxlFtVs~D9Uqk&1S~XuK1DHNBtP`)Yq`ZFtH4qqs892=wpeZ4<Uh_@UlpT1|Y2x_^PrjvOuo)W_3Nn1hB?JjwKgMdG!E^MJzl?Dx$3^%rv6Y4t67itFr5mVNfEr{^3kPzx6hsHA>9_4UyLU)sfbWI)s%fA3t(49>IAX))G5A46ZK<%c5Z1D~B{t?7;u>>Rw`H#Byw?)enD7H`<G*`CH>x`CD6<Lk$WG3x{Sft{vL$HmToaZrTPR9lhOsK)j@EPT9z_$gDJhVonDR4!jn(R8bPJanSl#wprEL@?OX=JfjRwE^@}&iY-dzMg?@3Cl9N<7B%e-uqtog!_#(owRy&kT3n4$JhXDN56Rq?K7ApR0C3$ooZ;1D|5OWJ+4g*bJ?j`k7mJk-$P-Zlfbc%`>5YZyLoxxFP<(<YqO=0p3>hovX5qWfm0DDc?{*Hkc7S;?i;N3rRx+B3&W&^DkBKY^PF1N+95oIkNkn6W$~lvW9D}R&gyPsaCShP2B254YDL>{G@?-+NY^@k2atW&!Bq(z1A^irZM|kc(<JEH;PDq1UDlqslpE`^(foYuVkB%USiT(CYa@w}IHUsB6KdUuJQD6x^6}?D$jJ(kFY)uiT6i~W+Y4}#dRtrwR!NKK1t~m?1{}F_(uBQ^ucafbk(j-SnG9omJYTU+iz`33}DxAvAgU)Cf#!+?HyAk;~!qWALX}2KFn%Yi{7Vkszcr}!dXB54*0FpG_aeE%itycP$)|ORSJ%yR`<wXh_2qs{BM>lLfCl|7^C0ZJ2)WC2#lyv_X=+aT{=S2CGJVdymArnR&a}@`c5`O5MM<Kt>rUK)9Z~n6}bVrJI!s=jd{iTjuCK-+MG`w*GxM{l5i_jc>o5wV&(pFElsIyoIA4Cb1XS2M%@tdYjCLi9T6#;YYTA0RF=jf8DRJmG7`;;FF9><t;ysap1lVDM()6$I)l{IQvKl=yOERrB@XAbU|&>9IXB9#%y7#syk@RuZH*QF7<PTO<+FU`~ZHRY<>^hQxueE|yOm#8T6LoBA;7TB<7PIBq#Hs@LAg5x}ZZflnagHc+jk0H+q^8UX1{RjDVjxRojSi5ab`1(;9k`&jP>r2jSqSEEUK;GT<9{!M|!mkV9rp}vMO{6fVXxBA;BZnO87->`hLJzCo2hU&=oq~5Yq@_<CTb&M&=f}l%qSF^`+PI>d$UU*XNIP=W6Ns`Jc1Hyr#f_G@$x4Hh?<Vc#G*w9m4r;AW5}AZpfx3?}lw5()N@#mS0{oa|A{DTBHJrdrF3XduknaNLWKZgx&@j}p>Hs4O0}1!$3}rlX;J&40&$VGPu`EE+Eb$seHJB#gy$!q$DtQs$BkoY{B2X7cR!_-b9uC7XrBOfQF{YxQmAb!zRHr;C)5VFduL+fEQQ7BNQ>RZb#QKrLN#3`+%48zE4~>|%ON2~*wF4q|TIRZT*GnXZ`TGxn+I>%Lias+<hYDd5jGj|W^PXq}A;KcQ(3C#o(*v!02K5Y|0<c%u1+kR_0zenqB+ofCEjj^FY-Hx6-3nHtL&XI7drfl>+?V@E(erOF*ZEV4(q!D(TDsbJ>mn1fF*H}OfqJ+k-8RtBRF}C=beX$u6pr^H_n?sF*I71MIZoC>4di|>dqQ2p7xF>a%@oJ%qXHu&8VPr_#sv0u2?H5&e0f85@l^H*e?)ghqwR0vw|!0U(b=nE(_$jIt9&o+yR*rZsOeHs8UyNqD#1kw@q$#~KqkgxT8{C#S>$BE9pA7Hfj`DyybSmOe8n`4Fh4_GN7=AusQq!_7=twVj`(MPO#v6ryLtW>A8K)VV-kilF}+6oX9|mgoDtws!02BYwZcWEur?wvQmp(yCh`>(##Jue290sElN|Xh(mK6eZlKGxKFU+QZln&fZlUTW1(^b_L9<SJ1K|V!MEFM-CmW)}sB2hU{&){M-9G&CWI$Zu>KMwGz~AB1FmHoALA<45n=No)gnV4sVrpOeZIoR|itb1@Dnbk2R`$SXr-bkKkV3{sE5Mh<i|ljY9K-Dl=%NZN&F{m&q?1{(ZhCA7n$oWe-~L~l;J05$dJxBm1Mu2b6Dbf0naj!0$rs@tm-9MXUUY%>DrMZsTuC6v0{M>Qwuaq4sew2o7$8v674o1J1lC~FF;`SMD`BFT#Hnkw_RiALyO4MnRZ5c=qGJ4U%N9qIDT=ZgRfO>#Ls_;yikMYek~VAf{d52E?ZFl{T4<-)IDRZFghK&%`Tm5$V(z}P8BLjR^QsoLsg0O#ywu0G=@?}P-!Ekey`Hl(dS)^hPRG0==vsX0LYs;?CftXHc`n%)i6exBg({io=OLt?$6hmbg|;(CeKp{qs(I*#sb{80d#LL!`zIK<bu~*p9CI#|loM?64P7(FhQ8#ya)WPc(`gWqOG*W{%N<6A`8`k3Eb0LTRUu-`zySf@ii{f|#IO7QEO_QMUqzZ56Q?R!hNl>_jL_{Xq=b)wjY)O0$q&;5T2h!DWHKflJ=I$FC=k?KhDk+q2iYa!xA=M`QxE(oJb+RE0))8O5*^Qz$DJk3OoYv<=L|~3i%KZ{6GRk5Tpi}}s`W3IA=irG80bdvCr3L5GMKEtFJkKRUH)ZQdNn^l;Q^cTSEM^qqOIWNU4~V)3b-ljoNW3ok;*bSdYg<tBx$~|n-74#bk!1YnC_-`Pvn(DM6YwN4!<pt@<)x{9f3=9mByh@MNgJ~1a6s*lgF317o%zBKK4atw1bLul#qZ$O?NB}!v+;>BG-+nV?G;0)o9)4%(~kwx@9r|UV!rKe(A+3`aUJo*d`D1c(-^^0m3Fl%;5-vhrs0<YeEh!s9Ht5>>#hDOvP*=Y6@A#CEZ}jLQ|^0`S5f0IJf=^*WwCJWTK0RW-gfR0JBQYhNB`&G|5d5-(yslq`gWB*R=fVe2#v9vJQdqUDP~+*DOS-?auBTa&XHubW|CT=0?`kS@dq~N0HMsjZdcgAhU$iR%2%<1R-(jq?gw{&)hVL>Ai=6sqCHTozYTv?8jj%zM9}$run}<!FOqfUK+*a7ELGgi9L_*V}h~{Biw!XRZK)itWFZ~Na5<eQC4+%d4_KcGJn$|<H<ghB-zKiqB#ebO-%gV4ace@;jW$;1O)`?Nf+0kHMB_xKc0=5Hhrh$k~lz4p{E%TxC$^oKAn)7gJJ$sq!?fxC=r)Yu|zYPBPI_X>-t!h7@bDaWAoT4H)OjdP#z6R%tqN6zUagun!5<_d+1R*aWWde&SN}FQiJoXx5Hr1J4Nuy(VHKcQvNZ1L5T=i7Lu|9KCTUc;SWiwp8GlS`V>rwk&JeA`tZevN2tv$oUzfo=!XiuBj(}k@XxvIhHed3S^OA^MFdZxNFU2kjZU0BZ++bAAT^*Hq##sOGX*^V(GYHdB#)MmXXLy=)GGI*2^&=gJ&Q`UdmvbqCKZBN_85ZO+|KfH!`a0om{Uy(Z0l$#f+3ifGReftbXf%=si0%SO+?CetIVB3%YnQ(p@a%rbotU3Ssd|0vRQ;<*vUR|8_SluCK_+`#7p$=KJTH}{j!uWE@y_6;c%78D6n8i&<vcFRnKm{=Bv0$<>y>X4<i6$LdgGZvJJ1pN2=JQ&d&y2arI&hvtn_7x9%N97X)7xiQo7VW)H()do8ZtykGx6zkSSfqNK=6h7|d$IFXm8XI;v|#R4u%LMTRv>g?)!66%-p2SbuaXeC+@rQ6awW8kt;I3g|luytwU^`__Y%JRG=NZx7U4LtbgCw<mdU=&X$aaxA0%CCK>jqqe6DIM>=E%rb?-1}Iw4;IJn5JZa%vtQhQ82+g~-mKN!GQ&RJ7`?Lt{!KBPV4<QYnkoE{;=o5n7vg?$=XSE&GnJ5FX>Kd94z*Vi1Sir0>XU%JDJ;xwjv>XT>6l_zEMbK5QGuVUIY=q?rYyV;TbCIUJP_farbc|8q7cf+;$g-o{z-gynj0kl*rBF1wRf!q7o|Zg9>YLWq{zuQ18pk_mo}sypG!BT^4Z>&gtzW$D>7x`OSU4k5~pjgDKI+dGVlANUHRkNZ$JI<&HV7AZP~X+yZYPvuit(*KaZX(=(rzbDA#YAXY5$>B}&TKJ_7cJwcgV?3j53>#I#@_{1=$7l&}fy+QMCUe#JMHP|2>D{en1D-WQ@>yZFEU?Kc<s`=1|&|KHrVEXR@@$Nmr&UC*vsjzkzqvmuX692!>F^d<WDI~-Isx-vZ6J+g5mtp<bB0P-0b4-fZ${pw*BLUdkR(#rwiFmDwqSVpz*VFB1b|7yeB9j%#!6BO;#b2R$zKR#SE1%m?}GZ|e`)j$61n~-#fwQyo*#c;3O55pou|9|`EUw{46fBpWKfBR>6BI3Xv*DU_nY3LdpkO{aMmf5ueUspZ;Ma;iw;rqiqOVg)ALrM<DdK&#>`#t%$xTei_z@1WLbRccd^g+(F?b9nDBK(tR>=@4uOWT)UM-QLRQe(O&PrK+7&<+jra$Hy5v2So0Sfk_(`@=f-<inMp?6H+zF%3h**bA=&I$0K{2P4Nozc=2K^~K5oOu^8FI{xm9qIo&gulnY<?6<kvLp#X3;+!m!p^qWe^2^`<`nO+xJ?!P<bl=BvpNbD*pp<BFAMdK)J9&$U8jAV}27U)v+u=Uj(w{Z|s$hxHoT8!ASZm~T-4{EP$Oi-+8;g+-F1w%Lj2ZRAJ^1oyTEDUG5gwzGOr<8@Kt8mDWo>9UL`@MYiVKcBDw(yfzW3*PHEf}j!VWvSN!MOPr`J_8&!e{abv($1$RI>067F0|<s6g7y2d%+NapO#-IPzvmxOC>E0+18AsMu$&%VVCQ@#!R3({XH;MgF~kPEaA-w)!Tck1}Fuc~f+Z&7}boOzUOMYv;C4xD31t4M25aj76o`J`v?4QwJ~n(J7D8~KmFyubg4)KPxil)I=qL{u`WlAlZd`NxU#Q5LN_QzW||Ocd0_WV>UWSbH>?i+5Ff9B()Op^fQ0Z~!v_n-`L2kFgFe$&;1Td#KSo*0KGx`TQQEE9m|dURsU`ae}3>DF??$<T--}M?(NzMYU<*M~ycX3dfE<filDYOe%?fvT+=wKTWz^nuSFo6JiUpbpF_sYY`Yf)LST<fY(QS{BZ@?M!%IvZGdzhs|{U}g=0hc0?GmWoLsgoH4$uN$2b=8kkO^4_~J6)^>KRF?@NG<-|K>n4QB{Q>JTwd;ej#syh!XA4S(y)c$KL!a#KVP1bH?NBV4`zk_cDUUgFVC1v0k<!$u+|@7o-RQDqHLCPbyI{3@ueiF%Ay_U<wHUzN_xS!P~Z=(p^;9CO-xT6&`y*8V1mJ;!P28AbFiL3+Cd8iPMRxxF5oaa?XNkok5os&KclJ2Vw)UbILjTRWI{evGAq2Atg?S~q0%fW{%2?tLAgAgqNT<kon~JzdX%ZDnCPaQL&#Q|r<~NzlZ1n)cVSQWak}{`Glqi*q0EHm=mioMHg<!>0cE$B%!!%XG^5=*^=$7fwIPzk+QhA2mA7(4Yn1nB|<;^gl5#LYJIIVsi;$&UHX~y5R^|3=DRyV9zR~iG_|G0<b(rxw%+1E*e8SQdo=tMR`BRwqPIsKxeKAhjRFom;?F&`b!{Py;aRVe%+YCp%-~Km%;FH!q9Vxn>Y0X?85et*&WE*^8sHB5?NYWeEj35?UrTU4>$OWS^jf<*u+-Q+;_}Wnghl(jA#s)#0F$eY`yHX(3T#*_2#1RkQ_{O82GfJ#~p6@vFrU>FylJ7Wy}bn061&569S;qd|}o<M~UDA=fyybGmkIRMvNwW75vG<NF+d+sV526w3#zd0dmDzE=V!Glt~(Y-?2ZX?y1a>y`?3U)9kKmp}<C3z2XaRD0x^!OnC-`REio9Voa8U@|6Xu|9V{Hb#6e}FV5`Tutxbl`s9!B6|xt%e0PC$sws+ekv*?Edqwu{?!S*FSJ*QOjn|0UYu>SGO=6<eP8aZSlx$Z!!;1B4f3*=KQ<JP)Cb@+oX=7}4h0FCh>g`tAkm&5nda}*)56obi$Z<Di8(-I{hQN4s=W?<F*LR6j4{2WU9R)7UqJgwAQ>HVdDD8>NJy=k5EBL?W`(gAhj7q;)r>yTkiMnNUw0l3CMm<0%2+wI&!q|6P2T9cjJ47VmW~Rq(y7lr8#f}14fA;~CngM-kgxEgH`b;1;@vxb>kV5H}Pq(Gd$^smQGQ6}@RaIVVry=W~pz28?T+%N@FI;v`B*_NR9b<WioGT}of$8RZIqI~6Akx977zTYB##asc`n`61Y9K-YuN0#}%3%cFbeMoO;}Z^eKIU+@p8!CA#UPTN0$n_f4RZiN?t;W0<3dr-Lpj@VjCZH`g~>6RcBYoQrkw9DH<Dukzl+|^=%YMB^pt<Tz!=<)wg9{!c>&gzLDQG<$Tmo(2noVuU#=jbIvos~bqsLnNH|bdCwt9`M{ycmjRz1V@y@fHuEBYJrlq3+>Dw4dGZ%iER@?e0c);rq;-s*bAY+=A8b`sn#YMNJH*jY!B%_Kurn=SGCK;f^Q??|iob%299NK(yk@}E(D>7}c@`z*2k6}$c-K$?f&cySCvOsabg*Ir?<^Gt<(nW+GBT+!%1)3sCMY5>@V>rC$Am~+g-AG4AYt?W)D;jgg@-H7v#NX~0w({j|U<q+~Ir(~{f1?)HBtM8t?Vt^KNtyy95M`@D9eW{`nU?t#6l=PsEd7K&>OB98FC1bsy=zRAT*>n}TDHa@ea$j!cTe-lnA<?YFdEANPUQYwJ;DW)uixe-y@cx%(85FFJ5)_I2NKC|^vu@5%|}LOBzD8*7+fb~x0|fI*EPVK&;d(Lc^p3DPAF10B`zF-m^F*!HUdv;A3ThAg;NqsI{iFl6>oNfe6f0Jb3rTSDjQ>2#PbYl$+>DCh5rVV2}W~&ksh&EUJk-{VP_Z*nNH`2_p?sxW=DQq9Q-+&qlM79Zd@z!aN#$YRPTxQLXx5fnYmg2p6*kfeVx_7BAoauh0H<)PyXwSN?Rr?<@&QUBjwJZf>F9MbDHA@qa*P5RryN1C7Ik(v@3U&Y4JM?PXY4l@wL!ynGN1<wzEtN|JNab`U5+j#l+(#l_zrz=J6*X1*UB&U>6<I7_-VW>ThNhiuh9`e94k<dtKA}Sg_TvWUxEQoDsM#U+<FRq8TZshH^^TOZeWSGy=tp*g}Yoe89OU4%~$au`+x=m`!-ey$+mdA1XaeIs`3u-Ye0AtopPorV39_PxxXG;G<SV75SR;LS4-L-jR0$UQXXGf;D8i37-?1fm*~dnXPoYVakYYCbe>bYx^0aJX>m~8LwxiDs%d-4dN`GRg!W-$Uv$~DSqah{pV(_Y$w-jBj?-TO1OCFOa}R+zo8<X6mMWS0oU+vJ!d;PX-0IcR?4oR8^Ij)QmK@+QVTQRW*aNUaTqjA^q+{D2Rq-C3>&s0Zif1d6PVc{`RX(GcZ}60Ss(@>dTXVG_0>`UJDDW1=N2#L#0e<%`F(-Htl7^{Yd!OFV_iPvW*wbKo%;>~N^9^8=5*eJ%4-7$@x#|0%Qy+ZZv|-PV~C@hdS@&mi7m`ie68mK24*Cj3vO<#WK$Pj)o%@`|NT4!GU$U2tD|^Ktz#amfW=mc;GQyjJju{YH=;V81is2g;Yaj{Tj$Y;_UKumIXw`^rq?HK!Z`G8f&#E-Ibaic;LuIY4eb~M>eAB-A{x5l<i@y;$vCT_GrlR{Ol2>3Obb}ePRA&BSP*E>K6Fhy3P#}U##3xz6EA~0Vyk%?Y);WCcc(;QMH#1@QSvBoAA=rWqmul|e$}LMD<CZx<6*?aVisSW&pksW4NdgU-0Iwrv|02yOu&=~0dxKto=-gnyV@H^fyB`=(FR3^z&{4I7qX!|(UH1*S&7x|#9&Oz^DGmkBD*MS+7x;Aa=XJk7nR~o4mRfPvi3-O*sAX9Q9kB})nZaqsZ$9hIKB3Hwu^)`o5{rR944_6xOSGvU#fH_mp4H&vH&&9QWUYa2^l&$QY?GWseeoRe;)Q{@2M__n~QIF^yx5^TUNiuj2&xEsNR}HB`j>X3P2h)1R}6^rzs}PEo6@KyR#G;w=x$Wg<r5dnbvFJn$d!6R?<i&`-TxP^D^2^113HK<uucJXbj>J&ca}#otMdOFsP9_=Ba(gt!CD3n)x47>1Ejza+2!1Jq=$832#i69#i8U@c%|MwcKkB(}@hF1hMke1_S+v8~=sI28%z336{is!s~8ekF5p_*c6pUBn^^1+NC&90OM8ZOHGjtMmF}f3wewm5He$gOErgaU2O%==j3JvCAG~Z#p&eE)mrl!v&^T(1SK~>;C3SW<uQldsZvY4Av;AC793)4va<WtVZ5s(6c9OR9Tof_A&-&qJ+Pw8^Pk)RxaXM5tRGy4UpAF5QP`0sej6;U@By+6znKG$#0YMlH(%3@wjz0N{_wNj{7q(yL<)7~MQBElLc4uN_nXXB*kJLxx48+ZE6iJxAkQo^OTwb)Ai?v3I4Vub&IOPw=zN;D$rS?1UPzfoq_jIJMj+aXO(m^VsSsuaWj!lX90vnj`&2@%LjV|BL1ti5lT_Pu=54R%+p69Z^g~!SQQGSBWbb32Mv%;Xkm15?$O{ecb1Q1gU~z`l4ZaRsUBLzTZ7EK3UplaTm>(lWH#!L#N38;<EY69n1@cI%Y@{&7MFK*9CaR^LYi~%2+ZtsmFby7_6uRuYq|^hdx8MK)>t>Rsx>rWzY<JnT57MidkIWduQY<=YJ}GR~kri7E7SR|>7wf4kaLk+7h;zOrY0Qo8-Ex~=RSct`kOB(>|7h@HmIjFpFqj2$g&0_Wv*zd`k=KrNdxkYNl7dzI?H`fK-I&*EJ71(vhBVBpB6OCsTyC}g8LDT<@4HXFC!>euws#|Laa`fchSJU;zo!rMhTO9n%W;SXNiNw7uY}vg8r*G2-8pn6NX>{)W7fR*jOflGmJD6^+t6~?x)-Q&HL^H{bvBV|w%)esoSfv9Dxj@tOv6Cgl<E8!=-N?9<%Hjq{=hIUl6znoY9#`e!+mP#Md^na+JOh;(U%nC`Hr0GNU<l&uvK!!IMvQg9B>eQF%3E4a~|X1st3K;H_M_heC*T{gkpSZ>c+8?d4xBMD1=~Ki_k&G52`o0#V#+>7Rsjz#W6}B3TP^dT&5+Sr$)BC0$u}Mfl{d;zhFGt*6gQ`3wKw_bx17%^0KO+4gQb?nz{67F5~tZG{1S8e@=aA(PHo={77C?qH5n}_2YAa1KZzd*NQ&pJo(&JoVP6PI#D|7E<9;CFZ47ODAM~1?koi0(9L6rOSjFD?;#a?kUtFqBryDYp){4^HXJ4LJYz{C$77hATkNCY9ks_rRhBFH&@oa~dP2`=-jK^s4V{`|i=_H49a7nwOLNd-p>v<Q=_gV5j(cK#akX;PJxA@B&SaN0VC}MzVh;ImaPre~ft~4?r9cFX1EdX;bltj<yoj-XOA4~o-JI7KCGFk~w!EHnxEBnZd5`(-V{IrRLhjZXBxF}FeWm8T)_cXoegIvoMP^b8F1KTCmz&F20+>lVl!plFBhlG%a)Xzrcp3atuaOh|{IvabqGhZzv0U8K<=ct3kAclDF*R%L%4tSeSE8KtWB(VMQh;~U5bJjdM#+zMz{gJGz1+L2Di-<l<3pfiPfJzo#c4VP2yd8rSuxXd0gmse4KUI5#+_^02?UR#vVm$w_@tp%!%@vx8lHT3mL5Ywk6=7e=cfu)JKdBvcXi+`tIb8kkV|5xd<We+dI-g_PJQB}+<~EBw2x|2!qv^@+u{??S%S4D$qa2;2X{k07f-THp(qnAEQ}~<Ox8<gNQ{+q{K>KAJ(hE(q4l~pw@2DIRSPBSy+GX*uTo6hm^_HdJtDid+3bPk(nT2`nE?*L1(H}gN^x#;NHGOB9b>MzCd%sV_nUBL_zPJn##0q}Nn5*~10HOHTcO0prA-WA<U5j|{d)=2cizqOzxYs_%d7jX&(!H%Q3W~toOT?|1whfiGV11w?$^@DKv)sx6P@+XsCeD&QljXrnv#^lSJ5zO4q{yRrqfz)mLi$@`zCedC;$`Ca)ovBJJ3b|XrYn;4hO|CQCaK+b5a$aOuC@$zE5?)>`RdE@M)O0n>|6irLs>GI50*QOZF(n*M1vp*OH<Qik)uI!nd_2Fxs);`#mLI@zD|pD80z11xkn8833vpA<c@zfTfd!Y}x#n4|FwO7ry<!HZ2~%u&C3I5sNN^Z7HNoETkys4JKd6UvAgKwmLsK?c=GqleI*;mo<8x<HAGY?JhfHN&`&T6+i&xYiB|0=x^@kLx!jxO~IluMM2_?!r||oWt(>+$8Bl_7FT`=sR)p-5YSskMu<u<WKXIsd9C7ZmmQ-`!~Fht|MSO_MQxObPUCZYOqQjgc(i@nq|Q(6#)+AZm0<QN*s{4TkZ-)&#<uSmWe4#lr5n7SzcV&xeDq1Ly1x@Vt8+!L?6YrRAk#)qhEtK0OSPpjJ!{l`*_Vo0q5Z<DSp=L%H_6>OMb3V=?6#MK0ZLc1<UvN0@3lY5d7k)=-YZ6hKJdI=gl}bopEvU%Pt1F%=mM#M?_1eKnF1W5=0uDZI3VC#%7_65>Sf<w1+IM0SA^sqIBx6hC7vcjAJa=9uD78m7BuFeyx?Di8APTE@Rs`#&NTB3)0isO9g8x$xMY!mvee6+hH&FLyz%o^1GFawp^<c`u`PkTTdl4uJjnI7_Hwy{EIGCsFURH`I*O0!-Q81(8(GddQY0C&^l`g_U%WO=_zXWrGElPdDTdA^Hly>zJTCfP$aG3%W^!ksrZ!DNOIF&E*+z0hhFhQLk*(AP9(5n{>{^4;jE6p#o_3cow7uwyVnZE$Ee&#qm~dI{ZCB_6!oa7>8Z)uu*l#KtG#ngv_hp&={V1kELkRqQU$~nI9O>NiJfoqT@D7HhAVedIAc|fYBr<H@`7J>7kMXbNMlu$fP{FgO&&A`a_u{TjU7>G-#;eQ@fVo(6P#nc#YMURbX&jIxY*&obF2rr?u)mmP#uy-K+}d|XQS*b1IYf2Vad<KJ0h`AYIDb4)FX+K%xvg_!#?j1hJPpUC2n>eR&R(#OGj|3>pyTv^Aghtb=4rloZS);mKvMoI2d%5n{e{%CTN~<(JRPGbTPzNNnQH_py~Op~6CZ;}h>WWZ#Ua8A)bJU4hjSqx@-P*5A4GHon!rk^$l9beUayhH2S=^r=I@AI?*rfx^fCedM*|5(a~q@VuV=8RQfE7u2TK1`q6##lNwwqi@GLLXYXA=+OI)X+Q_~|N%27fGD%Pp&f!{dSdX!Tar*;p^K_?8r6c>9A(@45%n*62#?0c3NB{|0Jqf)Cp#%~CIAmc)kO2BQ6As+mYC3Ci)BVS&EVK8dIu6_tw9)KsP4V}*@VOsq&g<g{IM0WVzoVVY%26tNw67tWBN73YbwBC?wpgC=Q<jf!%_6?E<{?rBWLjHy~2V^t6j4@->6mh6;@{FCDZw0+$CQ1ascr+U*rdhc#F??Ij`3<%%WeLvB_K&iZrjE=!+H|ROSq<76fopexE99EYH3nWDf>J3sEW&MLX^-K~wg}mWWwi)dXp&Llh*`GOOQAo}PqL_gPpPQQ9)We1Avm+73{U9P?tle*itl~s;e5{K?&r6@=PO-`$+Iq@0SsyluDX-dcQMo%OC-7-X3tBsdb{0XF7Nuy#|`?|w~v{Qln!*Q(1HFeHqf<!>Vg}?sq11(|7W7|SRJtH;3ZS)@+zzP7K22!Ia=NbCiWlLo`}YXUpzhxf0do?zf||`Vfuj_wV8aB=p|?SdHs%sQt<-QP9O=-j|!3XqqY&0hPPL;yJBfRSKxkIdMV6t#z1t!3ziRAnA?&@5qz3HrzjyW%p+y&oL{6q=UqTDP8}i|qboUm?qY*+Ifj9zh}RukD=^cT(Yt`1|M<IHG(H-xB^=s?nn7<x#)^~2R)nU+eaRIKvPtavzCR!O-+uh<m*0Mb4?iFLeY<eIy#M;+@8R>vmcpn1XxzSjGuYT;%~ur~NAxH&u;-(DdEww2gs^nl;F9NouavO~?b^a!czwk;m;52FS^R>$_SqMvUHdBEQ(G4<^6$TX82<IEhgpcYc<|_#UCLqJDtvaV&oehVA>1AsZq8`UWL>Xlr=AOX|Ni5n!UIUl?87p;;%I;T**8Iu9BWd<&Whn)J4}Z~1`q%C&%gfqr~mr>FaP$>@I=IcJ+4{&vD45sg?F>UJuI_p1-`C&{EL_?%Id@l_bg3f3=PXD80%^DkL~xwRN|U8-vM_@5$Ay18DrZ%lP6EF01o+%Kfl9z(&eY=S@Rp^O>g9B(+sx4^O`gyl5rV%8=%o4X^oP10S@cjlWkINv4@ws77~YsWDwo}bdaouVAfiTes4UN>x+3gm=2%|b^P5I^<{D>P4$UyiTQH2=5~;GMTb@7bsa<4|I6S1`nO+xJ<Q|dbl=A^_}MQUQnr@3k9Q^Qk~}?x-dz0zE8YPt+tBdQF_o;EJ5{j6Xim}4Wxf=ReTVyEXSMi%pdVwA1;J(alWot$!xwMh%YkX##JU4`jB59D#FTD5A6i0NH8k{Qrp^S#<HhFe%-UDq`*Xb-A~Q;tgZ<j110<q9>jG2fQQIaP8wrV;Slu24zMV^{d|}eJ(KrVjL72U{n{t8ql5oLFMSwdr%thAp*|)f1%C}*ELCXWVU{*22S)hIR{t_v@Q^%hjE2);auJcbS=MB5jWr)T4ay3XOvd+>X)%-$c7A_OheTJMqm`H>e;TJdp3y~CDQ%3abhoCKD0%+a{+wAF>W^yL72UGB<|M8di_y72MLiW`aN3fBa1^2L|DFP;b%;Db0iy6y3E`?78z%@vk8c(?%YM(egft8iqZTi;delp}yV=osy>J%1dca{7xfw5tm`EaQGkwTA;rr{l_)g2gbz0ewfF}9NNIOUTa=J7VxtIQysNVx`*b7E*M=F2*XVbhog;Om)R&G_4n;mpc$2MYwwskF(!c154y@g$IpX}+?HnhLe9R2H;|JUs>^@q==)qLCBIt4Y^${g}$EBrukwosYmG^YrVdsLLN`f}Y{cE!OcDw9CRaUI`f8uEiKa&_3b726BrAPz5N8xf#22`z3^jw%&8#u|WVHSFr)yP>u#tL<hGAL#g8FV+=u;3eBilWwHR3?Q_Hk#?ZgHLM&l>40UpAavwxSPzK&{!~n`^rMt&r_S1*a9z7EVgiE*Jqk@z<JmB(j9tf3piii*};`|G+m~n*1P}c9O`i$S3ZWtRL7Es9`3YMY@6oW@bq8J~_Hfr_I7vp$?aec}Gh(La}Jgq5C@d8xid>%%-{+0Q7xvvsI(Jv!R9>bn&N%@OyrF9w~>0=9g9;20QqD-?^)$sCo{iTI|%dX2Yr@g0pJU+%OQNd!~&rwW6&nTiV4!oOILJs`#$?YoQB;9g@J(c)gz1ed|rvlJ}CLRmkcjjtO9faEK4pFcSbEzALaJu(38-pkVc7e3UQ|{?{4s0t6#eu`Gygn-3nfNKw{#q%9IZ3Pm?enkCgNsP{aO6Gozg>3>cc46M>Yso7_{aMb@DIBn=c6}|?p%s_aq2@YKH@g-`GarF=~U0t|HQn2EqGUXpSjfH!<9378Y~GQ8Vq)=;HxXFlR7PxrHQ~O?Gz7}U!hWCEJnzAn8yYC_(uoAn(#%3Pl-98AE3Vk7G^C7*YWGdtmS8scXJsGA14ew7lnCKKfo?5=e1-jFq{wgQZIxj=JC^ZOKj7J8~nv;@VP#0Vk;mLJ!ZPvm2uH}>xfkV2Pb;jei`;We(TN7Y5`%D=rHhUMUOk&@?+QgRaM4yaIrfPHwZFEY$pUNwfVvX{frW}4$jLfsV|~c7)|&p@F2oSB<RqoCkeJLHj)mx;w%@WNQKG-pTF<epHlZ!X2^1^$Z2+0KUqne!Wq1R<+VBAS{VZKxC)zqL(_T{Nv(Z7F7i4zjYlue?A)-s0zEv!S8#75xndwVYw8<09+!&HzrC<`cmI7fS?LrgC9ef_Y+93;Xtm5mPZUbFtDT9PNyN<B`c*|}q@9{1crz(rJUYN6wfbJfFl@KdhD2vq!j)}(1Yic!M2@>D+xWU}G(=^vJBP5+g2S=#T^e*d%PYR4z@=F<kTzx-Z-#oKJ(0Pm0Rr6${;&Cd7!7-)5(w5Q>-$eaM30UN?uXNi4uHe(oMt7AeYeG*RDG~RjuCEVdhDhKWcE=Od;;#ihw-l?qLLXbeTEBQ2b3+N)t`#lnr^GDaUY{!_6)?`&?k1f-EE{{j9giq4l;RJYIeH$UV)EgVZ-g|Se}OQRRg$wuicv(oKOr|K=hRF3w{G(!qW8Tc~9~&hr4Yu+bXW$!tnI!;%RKyWFm`HDpV)<v1FS;H9K&Occ=0AWMNy~%qDl`+V|77i47o!c2lD0JHF|UkTw+uD3Cd~qb&dxNF2?2_h`B=9@z%@6CpI1ozN9C^jmkbJJra_cmaCeFi}~v;!&JNSAYXV6}&w;r|@x}pK0mnQvEhk*wlfTR@?fha{B8J;-s*Ota$?>6bY9l7lfAHz`a+Y=$PtO)A(fo2u~@Kpjgf~|8r=wQhfQ!H=;^(WM5+C1jm{m!<u?14!(eoiRTHmnLHeI<;_2NOpm!NUG(&^Uj@)Q0v3f*QE6(x3l1YaYFQF?-ALa?Yt_(gD}H&_tR^2##H{ZZg7W2U%J^}4IV*mnO{5mrWXOq2?NsM^36}y1SPu(<^d7X5=TgqEpgz+zW$7C9QRn$zd`%adf?s2Zr1oZ%q8-lxZ;grins>&Ml4fK{voHfPG`0ks(fzxqCHlJ5dXT?&KyLjxn-*XZU#4oZHc$<Jqp!9OWoCis^K*C)tENT;S%X;ox(0X?I)I&N5ASCr3N;0%#Hm9dt!9zje#2?)16V=Fm<^RDn~Wq@yx9$QBsxeSg_MhrG3VJB%OW0ZP>sz+4k>_Ecj!+IvtgY?w^s`g0$^cpl@PN(+#yb}I<1=>3l=c3tc0F{&|Jr^6%)BI$xNzyL;EF3jf2cwJ^X1+dAd(^QWMrqA0fJ5X=WBqc<OCu<l0gqs_=lNB0X9I0xGAv;Kz6+ER95b@_N%6UCbZQ!*Yywtzhu|7D}SEoOZZJ%XnAWBfq=wPk;S0xPTVoEqg__n;ihq;{SC>pr*pEQ!$ykNu5(60`xPIgxgZUFG632dL%qQ$iJCYUE)uX;P#$m4);z?_^DwiR8|qb^C+P}(H4di(YR;v$~d?Xrj5&h@L=%a!IrHmNv3iiD&0Ri^ep$RD@mNJ4z>F<N{qr%_+StkqgJH9+}F^@dHFWrx%BNBSTUxd^O@e7&!KOnn~N#r$VO2v`=GLL)j#AD37^erZl_&w`H-X$LdQ`NQ1LV8Tt7ErWxI4Zo%3yQDbqYWA_F<n-%wF&OJ(`iL<wj<XFEA*L3CtR$|s;(pB!OWc@|e{E9Tp5gS$AAf`)azX|MTf^G#{O+9Z?kgQr)_Op44n@8?);S^;wXW9(T<FkkIL%JUi?%K64QKkZcI_qoOMP3b+rW^$Gyi<R||OVw5N#o)pSvUqDq&(7(*2bG6T1?}Pa(LGF`3kQB{#s@YJqnj#cycvlt%u{k7L>B%Sn2{hZxTmoeO?`1yfi=MG_wx{}HcKV1Su!XEYctYFn|V-)+nz#sJju|zHli^e;9Nxk@gsVKKl5mWZS<_rj2nnQ)9VvAVI2B4LE+1@oUMr+a0r&>hG>gHZ9gmmX%2UTCyKEBGsk3<)bNa92{=>P%N^r;tG(wK<qi}0?b(N}i2+i_&Tc%#7P{~<s3Ve^C&?~dVeq+pOX8@aIA2cZcod|ML65JIC;nu=YEn57z()~*fQWm<ES5T-%gLRg@@i)$ac*eIEW#KjOHH)LIpYdXs2+n|?Tw>Q;Aoj>OCH0}9|PM9X-%HiNL{|HBx?6ku#C+-%LJ#$3d$NZ#g4t)urN3DT@u`8vW_utmo)_1!&X&UkK`~vtQL3RyCW3hc<u9Sm&9nMl1ZF8+*u`f>@2anRM1i`Z-PZ+0cw_|D57QY1!YHyWe+-4&1p*iVSl#rJunL3BEpi?jJodsI6`|*EjU;nY@ryXc`OW2ltO|HofC4lCef<oH%wJFRrShUjZ$UeNvkx!`%9s9EDKRk_z26QDG#I+CW4bqr}l=?H1jgrO$sJ<0cBv*GHgsaAPfX&icL_S^D@~j4mBFayfnes(9DzzEI%#1yqH4uSbevr<t(Aijmh3)YTSeW--rg6d#z<VQA?JfS)Q6<Z3o9W$0gU9pu&#{ZUuBr^iB+{v(*9u+p^M#szJ_2OBDwSV8bf?s!6TE$W*hBE%)VW*8%3Fce6}?40-J9v10H~21D^8)S8dJDj(fQ^A>y&lE(m`A_q$Jn8<32d_O0~GuW{GR1s_zbIjLT#F1sqE#547l3egsQ@&Vt2jL)*nd~}LID?3-e>zjp-}{`;T_rGqBt+{r`k-RQ_Q48z&wp||M?P!UhT+gnDQpy=W+j3KV=TO_tQKTe3nB@I>o0D>r#cPFMw`q$?`rs2-qlvoBSW6X%Hax(42Sk{jqW#@Q?@~vLvPy}P@b5#q?D4`UzV;%ky(Os20lufzMl(tXwcI(Z<8yMl)Z;C<4h@*QZz}l6`M+Ls-iN?9m~pRgafAoT%4Eg=^?wk(Uv$SwzwV}wzP5+f-fFZTl>Ueu5)D08_s%~3_I1{vU%I<N$08?2puYxQa6#Mfbn<U6~~BxFoU98P8|#Vs#0q_oWj_rcO|oeWDj7T@C7o8xk3C>z^kF#l<W~z3NiV-h@ZGG9jIN*U6bOLon)q?ypkBQV<KyT2-PYGt4@F-^QTT!o-<K&7hFe1WkrhgzrfykNO2gG?~?BF;kZ|;P9_1coARG|HDj0b8KCfx#Wak~FYO>9?O>&7=a2a;x54Hi)meRY1gYq;6|jAts!f+=;9RFy)$b_WtH6iiS3{4H&oslllxR-oa7({gKX;Km6`U@EqsWbPc@<fIwZ=`vc{k>}+MXuqaU+x#3U-oZ`IlR*8;)vray#G?X38jVx$WH;dmJD7(zvwGk7jtY@-f8mEKPqybmke~Z!FCeEwXN}V_DyYK9NgH(d?eN%4y0%0uRI@*w>L&n1E}O<O>(A3}0wlpdkdq-cXYKW1wqCNuLwjQ<e|o&PvLPWvJClSc>~8uth11m>mXo`O)APa{{H5a}3*_%F=1|Xc@LjavkTLcyk8u(0pYU!$f}0V;o#5su!EfSr~*5VyPqeD{Gw_$Z_nX+~Iv#3Va*aA~dHaN0&@x?S@N&K2#}Pk)Jyr1?qgsa!%;3)B%xv2ITTp!36vv3+8m`3SP$TwPuj`&i#Zs)zUNyQNDWv@sro4D8R$4qI@oJ;Da3Pn$zc;C!gJnGux$oPA1yL=_fvhJQZm5`^xkm<i|PK_88*QZFA%^K?Ooe>|v?XHQfs(t`zOzsJ-WzG|Cg4<nWehbIXVn&7^kSlk&;wp77XJEr^v#Skr8L#kjVcLnwF-dae|FG;^g*g2(gBX8+CU*fo7m>b7#XrZ2QrUawP}8`Ee{HW-Pf+(tG#<a@z=Nz>t_>{c_4f+C;SPh>GPn3<HvD5a<h3=gCYmlXG!x}j8h&zZ!zMY#K59}3Bk(>z0i?DnP4+q~D>1evlFU;?&ycU0-13D!ObzT8}L9YA{9A#+7wCyA(=lc9TV23VHCztbAu&`*8bU-($YI%&|wuU%Rne)yhnW|>{ibJm5JGvcrYS~=^-{x3HB1#g@pR{j#jk{?x(mx1Y<&S|YSGe*p!+qikVg*homfx~?7E^Ao)?2iwDTDn($$$f_WO=`Md2$!E)Zp@ZmXfesM;o3~_B<r$QK-KVd1G|JBl$glpjz&J}ro%^2s;ak2ZHSn^d;(I3qG<<$i~krLa$DlvIX_h>5K_uAvr%@y4q$$@R+|Kk0jtD*`VkknU#hDVG)pb()F)xgol}aOQ~0J*&U^I<FIm;h)<_kCI)u*i7_amKo}}MGH7h<i@F`W%wkJw3rT9^5pI3=oCa0ZuQO}twAE9`t3TL-HRnTsb^LQ_C$Hhw&vvwvCs}#>58@Aa*rXtHj+T&e7CqYOir}mhHgaT5f0h`>8i9@!4v>qVCn&yP=H{sgxXSRZJ0AGOw2ASlAhhe!7wvDc^?&DH1Mr4|MlwXoY8;3GR(Q-X2pgMG(WciPgmVlL~;W__{@2Pn-tPAjYs?U1qT`{sbt7PYZxKc9uSLd`}l@gcx@|vihL(@^k#)4zA){{9;FW}FpO5g2rzl`^B_U@~&pELrdi5ISTGQQLp32SG^ifmFJl!A8wSz}lyzuR;K=q&sZMrsF>qjw2N_;?p>kso<UTX34BYL4Zk*!ki$P0DOKcmrhzHt->hWSZ<gj&@=jY<HgGe~LY<@EvL^y<oIs!Tm;oGxqEfqB6P2r@b+SMow36>kP_O>7G`hU?gc><wAaP^TTyOZ*bkG_W#=QRQ$qH+c-unV1wIINQ7CqX-+jyzL39MZrYMUHMY9Q1#KCtIQq2`7wy03$zyDH*^E^hU_!G3LSJ8Q5Smxt%xpdikgAgvOd^w!ty;;wv!MEJRBcRwSUZ_Evt$}z{maj#BPvIAe6lw=cK_B6cpI3fq4n>-|37~`+0sUC?ldyT$C4dIuNv|@)UA?YZt4EA8I6?~{Hoctx!tpGyspi*;}~TJ8#Co_y`HBtrNFWp33tPHJY9PqhU)dCGSjIrP26HNIK3rjkUB2=QZXO21zj~nfph9=Ja<m<Em_TD>b5h3A%Rz`)I)8ULYu#}2C?5O)`!0Ayv&EM@A*mH=doj%tPB%?d1a3|*BP}<`6f|0B-RZa8SpJ-?SOv4vhS~A$-d_+C6OX1Xx7_HWNwDIu$OsUZ$nXgZp^a+f({p^9_x+pvpdZ^Sv7K5)AcsGEe0Z)Mf{drO=fhlcG)t)DXE4U2!D!2Sza^HtxnyU#kC=y0DQbeaG}5+LiFq1)Zu!o^#&#OxY1*(5#WJ@shdzN<As_aV7;xq8ZDsCq02)*BV7`GPoS!_-tMlUz>S0FY|Gb+?I}2pn+?DvsYBUv3NV9x+PLR=dKj<0klU6Z_vEr2zFVQ}P?j)O_hz{DNgUd`oWKeDu+i~-h$`OpGpZFC`eHWP=f^sj+-5~K<^o`XTsNj?`f6acsAZoj%N{fHk(UB^2F_Fb%GsLKBxir0iV5$KE_uFiJgxwd(-nACTZtn+zMXSk3IcYbLZ&nVK(6cQ!Fy$Aw{tdYxfPg&s8lxf>2vW+w|Y%nLQNdYLUSF>U@!v$W(8(bgH^u?C9p8j%@5@@hR>4C<rI2a+Uywk{$d>h<M*hEggUuS`DITM5eEa<I^H@;5J(87YV#t-n{uy`gES5=X8j-qO43^vCuf8r%q%=Lc7r*dXKozLEZ@_>Tq;)d)_55__Ho}uMEQzw`ahrNyA)m4Mkl+4@O4Z3Rug*TVkQ<9;g&^pGc!z~gu>3%++Kf5uVIK{xU>%^`}OheNd3X(GMfP(BftBIx-04mR`o^RF~uvytiq&tL3rSjgA!`+rDHHdr+iWDZ$P;aDD0}jZa2+wnvkiBmcEBtr4!!3=smt7jW?RhnG9thz-r7g7vM#Y{yrCOhIsZ>awPFq0F|vVsWf$(@=TFWTOYGDaHIWhz%F&{aP)T-^mwT&#y=|DIF<E^HmBhfVk)a87%iJbo~Q!jTMB(szB{G<oinJX#rt)ZPc%CNP6rYDc@R{akd-ZRdmIzGzt#>@|EfdYT6E<Bp`Hoy5dsh9K%cBl=kG@;<K#{~zS>54C#%wr=N9S)KHtb!I-YWde<P5%-D1V=`pt*={nxjTnU0jcbFI*K{w(&+wdwG)ym(E=zZPi!HFRsd(M#0OUB*2b6I?7@5UrmBa~qG!axCt}FCHI;ze-COAwx5UH3}@J&5<QX{NZ}uZkcTODphS52|o!9KPp7ckEBj8q1!9*E*FkIOxgXm^ip(Vh8WSAEa(|zUS&(J0Xj`bF7qzyr_7;Z6q;X@E$3Z8Izf_CVTAb(69#xp@%kVg!$4ES>yERUV5Tw3y&xU`_`B|0&vU<o>2kPlSR=S1W5vs5D+2ni3jH0;`Qbq_e2w@0`OyFN<8QzG_9J}w`QY!{#bJB@^~c}C=aDUiKEVO@5mxtDb4h&`u}jRro_zopzXZNP2#}!-uJvG`l`=M=U0b*dudn##c8JF{i(in}KKr72*Qc6k`~BAs<G+6OFbmldBXRm2zUDA*72Yz|-IW`i5VH>rS7x+klFYMcr=A_%fB*4OVX4EO$zhj=WpvfI{`j+Rf}uF(X^EW`!@c&E4U3E_{_UTC{q;}(_4{A`?VsU^hy#0Ev-o4Dp=%QTriAja%&ryqy6W*SVm2QOKNRj+n$8&-)=x0j)94@D?}>%PHEq5F?v!HJ0JtSacYUUjo?ZbVOMBrn8X6u)`0ME5^ZR8@_vC38{XXHL;RTHA%G-pD1}bZm6F-OR+>?b<escI3qn<D{1aa_6pp#|w5wadV^n2qyS?}LR-vdfGS)O`WUsR3>*1r4AZ@JWRI^}kdcSWLOBhR0Jv6no+FMt2*-+uY^u$Pb1eILsZIKSFMX&mA{-c^rD@)i;ParF}nSObdb!(BCz$bj#~W`kr-(a>ei6%B@m`(mfL_<*2eV*%dbvisS$XD-=`d+_Daw0>jVBRobWsh7+ir+jD$ThGwYBvDg~{xt2FQP#ft-k<B$5F%054D9G8sNe{ksY^$lM{V;<1Q6?ws6DPp@^4v6<s1{tZsQzqa835+ZptU-OTsB1iA2Ql*Z2DL*|)f1%C}*EL2LuLU{-a+S)hIR{?f5V3=I3LIv3wt?;9jf2kr0_?pU?&_88JC(i&9tAm}VTao?KcN35Pbrn!zaxRL+(%lrF(NHM|3O}UG@Lqr+^VA^BJKmRy!KH9>*og&%&V4@&%A)(Z9V(rmnF5UxK@y8s-+s%JyV>%BUz>G}yh2+^|tb^NFZYA{|<mZodY(H&2zsKkbr1OQBHji%IU}<bxhhrr2oWX;mAy|>3<Rb8+#+wR-BiL8~SnxlSN}``^90%!76HIBdu!uERY(bXJADeP5!Zl`+yZ(Voh>pjmG8&H<`mKaJ7^L%@+R!nWNtFX!!D412*vO7?EaD-fOP!+}-L4VvxQ<OZ^`!*Z_`NRJ*t8>pqz+Nr5*`?1?1*GC(eSsvj8~Z&W6N9gK#*tSa849^0}}6`>m?rTR3LL(Fl;0O#=gyg7$;j3_Yz^!l$BovHQmd{*^wGAOkYo>GxO%vmlpahyDrC^_MX0zXoj`FNn+1&8hS<%y-SeZZpA3TAD>+8IVV1p8|+EJ_A14lJ319=UbIN3b!drqevGAqdr(XD@*I@okWBZ!W*HFHLWFE<JmsFQ=fJkIFbFvOS>~yAX`upD;yX?IYgws^uN(jRJh;U<OO{^$TS8Tat8#z-@#7!wGM#chdh_Vcg|pl6uONcmLn9?Qmh6pL&UsD$6Z0YzZD}Mnm*CHwd$^|uhk(VvVAl%vtU}6?eGT4j0<b(rxw%+1PE<{08d!{w_vVcY_VEvN=9-YSg-?k&pdX;W1X5&L)$HTfjdR*;rS9f37(PxIdQPkTrhb53*dC&c16g}M;EO?0MN5m1fBdxFrtGy5{KYK)xjt-SE9e_KW-84ABQisMuZ+bPI5^SEP77`6@oRK|2?`H!P)CP>Pb+%d;g%n}E(xe}H@ndUCS}YBp#V5*wi5!N(|lppKSzn+1Lws+j5Cif({qU?d=>m`!bl`QnWV+Fnigw%S{cj$Ip-`pq})!ykMjGD{V8=%Wrpl6EvcMlcU=nwHqtN`UwDH(Sh#vB1CjwXpw(?)i7|an1!_sM?d!Rb7o3ulmFIeHVI!y-z4S*w3#t2BQkI|;(3DAXuoC68c<b8DV}|~V$vHd#4X&yhwb#63)0$L8D-S6E<3#s6-5FNCSNp4t7@3-+EHOLj74<D+iz!^L&rxr;(uPF$S5}y9W>H`m)6|Z;DcktE3Lk{Zvpa`?WP%8=@n#z6AImhpqfn+<G>}MUau|k2jy;jN2Oa7v6g&H2bTf=fL`^5L?>~trVsw<kKAhG)!2AZ!X;#$Ocbj=#RSY|nYm^+>_1I0fUb2(eV*o4iK7>+}uuhE}#7CJB9z-i1S~I6@E#30zw)9z9fXq;amlm%oHg>wLwv1^E-r1WKcSB#V=_a`miHreDGvs=)U=Y3wqmCko5FI#*VXdc|f?Ugjk$+$E%m6_RT<BD%VSM#*S-<y9nHm5SKvTt7mC6nS{{p6m%~*-Uv5z_2?dPbinF|1?C%+LdPs3|KaK#`k$(UNyQ)QRkug^}y{S7uuUnx6}%-v*8be5a&v4Ac{?|Af=9_fOb-ZZ9(Z%12zg^(NtYZ{@+)p%qZoK*xYVV*2kqvgX^vd`|+xO5~xkZwSI&5B2HQcD?Eg}3A(>sq0&JzvXd>1dDo9+pPt?@X(0eO|~Sn-AiokfBVi7vez)s~VRfl-|I-k3IZxPPdw%nI%|EflLH5bm9D+=9}9`0GYue4+tyXIM)0a*3{Em`vo&iJWI%@9tT`#(k4ClkGU*eJijq21_WcEWusKWn;NJHU|}awpzXdHsqtv78va|w$<FAU<)aBar9zP{U)}~Z5to;XC^XFRYH>|!hPc$r{0e?G9WP5Wp^rLG>*ABD+f36M4Mkwy*T8exn#=w*%dF8o%^PD@17AityI9NqUERS2e6Qc&mcPKzyslIV`Cm4^no{nP3pTx;b#U{J@u81>usQnH$%XDFS?qNU@FsKsQd0(p&zKIX<xYuvgurD~IXG_tp4L8Km@DC|#h<5SkK33e-s}eRVs+ELr$|Xpe>xq@;tDRuj6eh?QQ&VdnP4>c7l{#j)lVRB7xsklaO89>cqi+$Zgx~v!1A&}e+Hg&U8I&d{=#f9sjd_4g(SrdGIO)eJ>91|DLAWjMIiB4dX~B2o|4}g@wFUQ%B^N8Jj$BEMR7?o<r)g!*9!99Z=57LU7!IZOR3yd7Q^o;#1hgL&MmXS+s$^CX@NgewFZZ{8$EK`gH0+t!9(*UCGs<pRohZPEjn~DW(8-|-^{ZA@uw)aD9&K*Rbhe0F0Ou+fZa*vjKFpIdY2p*P1CJTo1dpd9tms-VBBR=%G(+9X7d!fEM~03N2-0<<K9be6ZEan(o-Cc;keaj;y{Q}aXHaN0cI1tCfVo2gqp5187j?WIwMe~Kv3!vE^+d-Gfy+=>4Ir_RKV`!^~{t8X{ssRDn*jQ1+UFu03ylM87Lh+QPbV;9Z6NNXMN`utRa)^_}rlR9Qsx=a4<v3wvIlkfz&++u$z)~Ggr%<8rWhyha{hg;H4-Z`|OaipE>9Hxe+Vdr6WR`Z-c7?<N<maN|^qJia69WQ6Jp0V{Vg^pGF5{rGy;1cMv%m7S1CKBDD<jZMNZs92`UQ3;ttP3w`FBQryJ$z%6Z@0VXpbve2=gW3_oX$YqaieyP%NwF1E6B^8jl#auc8Cd!$AUxYbp!aT&rz`~;lmIz6GN3~EFO@ijuip6{2ya!bfVe0Ae{OBgY&xHfO6~Nt(A&zd%h7r#swlL2Pw;l%=m{F-HIOGvt&?OU2hTXna_wx|QYyosM9noHD9rM5oEVim3^k5(2Nrv9F5u)-S@2WV4AJHS>I*&%^O3w;S8i1fYy*_ah#-VQ$REI-WJTT!P4nx`8Fx4^iG(Ei_5}_+jZj9@gjI$a#qbLK;RQ7Vm9Ea5ncZ_m}@qK&tp=;u?b^>RYrR!YX>?3ZPr@^M7t<t?pXk1kO%1KBMWW+J(@iq3*pX^snDklQ+$r0O$$a~DHz4N(e{HmeQ-I<i18(u$)afv0ph_ErIEaHjyW3a2eaTMJhEfeivWo;41!1h9FmnSh&moKZ$+wCzdKQqrVr7N<65)46EoL=rhnH&B)38*${`<S=O`e*H7E5Lxq5}F@Yi+oe1JY|mQ^xEgyt}fHOB-2lH$mdFk=UKwBsW_fo-UI^60@N%^Q3OCI{Q2ZavFt&oWHN2adf1<>d=F^$4LX>uD=oQAH6-P6g!Ud-MX)^BLPehx_Xo&Q<QS-l&h<~&4Vy$OEU38UVhxuA5#+nmX%*%cDiitLUkcrTS%`wdM_4OPfeLWVXd?-pYzhT@!_cpJ8SPFK6BvYYvT1QTCLs{O$RJ;ym&xv0sqvWRr3pqSNNY-&?E5*DUSe6HpsK#x(?yu@PRC^LF*WYN|8GQt%e~fxpD3?N^fph;ux^)d<3rLuX-_yNSkkWw-iZOaXF{;)qRcd+YFap=U5Wz*_;r<j)vWMfWU7BlWdpf}HDj!Iye+_8H#e;qcH5lC!UG{!MubZ0ioWjUyiRU`l)+{tbUmFhxww^Cs0hSJVi!CulBEH#u|gdo_!*B0t~UJexg3z8_U#9n!u0ZRWUa+nS*^e#*OT|hh3z#(n?`y(!F5PzH!}hiVlfF~%YE9<`P|h_2TC%nYm8kWbaNPO4J%_l|H&<b<<0k5yLhZs#FQ6CfqGUdY1$Tq*O}GC%&JM`cX2Bt`I>ID>(lcxho9wTZZf|riViD>Z7`lE+E_Wd-(=3|#^4^|fvD6eGF;&qzivsXDYMk9oPpxhq@@D*aA|pCF7z3I=F@qbTotzL<&+tD$|{zkZK4g?RQgvH-C=HBR)!-$JRRWTyopaw-sLstSvqQoJ-YoK80W+Mt$pfK*Eurx4`+o<QmJYa=)CRqq<qz3gsvAWImqYfbXNAUPkT-#7|C#9%JBuNlDQR2XV_UoLk-__uG*vdf#&31Z097F4gfG_HcBDTP8QTrL4p%G-+_HCP!L<SWz|AZq_K_Wc2~?ST)atYq}Ld>ferA`<*;J1OOjR~o9<PrOpa|AAulQ*yX1a>Es5CwXQYm4j|u6kBN5ADuuJpYjgh2c(Qn@LT#8~okJUyuX}L|WYD-cqSb??2FO?o6pK1DeDUtEa;5vS5pti_{3r_07A?8Ldy$ZX}(r<r+VRvJ`tL<iyb~i%2qA)3031GR^8sn%UF1G_dL8=UamfPM9z{kOnFFZ|K{wn>-ZxP-@Q*+B834nXi)^M8`QHrj=o+h<vGa)D69R&4rkrN>DxnJ9nKMYMLN=&RXvh7$zD?X39?U9AFi<sKfX8<Z!JBzqHxRFq5u<$9vbWT??E*9EJXgtO+QB>>W80gvowcwH$lo-e`m)cnzY84%pa(|*<K&g}H=Yc2j(RgXv0`5E_ss;wPTZXNY?8o^oZpMLg><dh}X_jRiTt&SXTl`t5i4UT(>l=1ub8|S3oh)6vKTd(7<64BK;pFI&sjS^FR?r_TMQ!qP$0Kc>d|J*4-IeSq64rsV*(#2MKV-qrF5TM8xV_e-)4X9nr*5`14O~^yD61ATN#KoHz4=_=Ko~pPT&kaQo_zX4PBfMFpP48mr_cKs@>Ec;=mQck$D4zok0CDIHb*`aREtOcG>DDB@b87vT8c+`PkWFA{g-;p=JOzIZn2VL%G4fvl3oda-7!*CUqZEtyfvSpH9F-d7pcThI;65opT@Cbp>tQW=`2(CjyouQA*u3T9X7P{fXjw0(d7K)3*%fkIQeO*zy*LVv()c_?y<CCQcXcqN_0fbQ`K{x*B8}K-wndmo(wtRTv+D2j~Jr(4Y@a`Kc8K+^i7)gTF)g@UIYBz7Ku?Q!a8cg%W`v>iU1zCLk5muR1%FwCy91>c$dLH;~EUnPiWp>C|brk1JlJBU0TO`_?{SKnTkA2s-NHOfuEC3u|7cdA4{@TbRF<&%&x8jYjDlUmRN7LJOeWaNiEA_6Rz-HJ@O)40(A1DDyTHjk>^{{v{f-OmRJt3TQ%&i`J~JVuKc~bSY~NcJU#@V7+z7Y)@6CjYIDgV)pBE{h(cFWmgv{Ul;@9^y@FqdJ^<Jy?0d!<1@|HIQ8!Ixg11<`=xRg6{N+QLx?N2N8eIIx;E;0{@6P$DLfM(J<VlX$C%Aonkye{!kHPK4?)d>HxJ{}_Sxx_#=hUa$&RuwluvGB4cd4q)cg|;BWhFveds)bf5l-1-ywWdtl9UXkyZ8jb$5kaHJkge<*5~&eKCGdPipd?}t^9MQ|4EofH1Bf_voeVjdM{8K#)}rym?l546c?(LaT{qT#<(kzWrVfCg$ol{uH<sK0CQFeNTqT!HZ3Dls%_DdW(iENtsGrT%l#%iME+V=a3J6-kS!vUY(_rVhP@)9fs5%F7i{iPerp<eG0JsD0S&Cg>=4nC<v&JRLj9h$>HIIgxaQHYF2LtGKPxJC#U<#hlAUnldOGM|ozs4mmR;`4Yr3co!Aupn4UWlL&zwEIFF&Jhf42b<GHrlUrC-p8q(zg7LeYFGYGr+)Q}uC_HYun~k>!A9G^~@~A3Os58r9BnIH`__O322?yJ%Sb$cz4hjVBevwJ$-w!{-~g-RueCEtOsL!0|M)bh3jyT8?e7V*rYoD)t-0m#M9wgVBx!pB=^M*w;%)_v9j<7RZ#yIo;c>Gul@G2wDV$0jYJleHNQ#^P_%1QE}a;_W#=IVEn>TjyXmwx~;aQkYTfs<y<y_d?A0i+_V#;xYgxZXyanV(eKqld+}hN9)Ba)h&lyJ15BuLd=WT`AE<2Z<HT-0PLgU177QR$;!aKY-dU!8H>y0Qn0ER8ypfjk=Z8H%fR6Sfm72<)T3dNjB|}sx<@ewJpFf^VWTOFjT9e~r5?q76@~@B78%+0?&1kFy+gA~}&283x<Mna29mgm;2*WAO@bx^MxdWEINa!>C8+A8QWsjRP`vwE@9rdQ1nYfBncWlkU*IA=}$G%j|1Z6f*Jz(HG)>6~uDRS1^Ww+fE45z%BpB|dc6wb}r_V|w8D@KLB%)Hu%Z{_((y`8Z-xhDw?y_0n=cT+e_lnaT`0tW<qOBpesoU!cttH8VO`AUiNj2s%Z-d>{5GZf;z%;9<)ifFqrkKqLoGfW-UF?F*$%{;X<a{1i#Ho9#UBK1VvkzB`UbfI|JGQlaSmLZ6Oigj0>^ViK>b=2K@&R|wd&_wE^KurUhwBH#yH%RoYw_5j8Vvidouo|@>NN>97KLI{zJo)vu_G$rvs)R1){EXyA_TXNCL+kDCngt9kK4)9LOl$|i;oEG~ElKOi7Fqxl?9*UA&(p(H?S;Iv#Q!H(>+sYHB>^wt$;l_gO&V@};+nQ1EO5g7j+#CgRcZc1UqD7X8ChqS+kDB!T!1%_>&A3*Uk#cTwd_-6*<;o`@@xP<z<GEb*i!f1n*Dt$rl&)O<N12=C<4SuSC~}E@jIj8+d1c@Ae1PoS4xWlB&?nuyrPY08q1E^tmS5B7LZbT-lxySGu`Tfaj8CWEDL>yG+)6C2$&U^&1>lDNlkR~19y$Mv*ejM8>5!cI|jbLSWLiZJ8B}K9<u{i-V^J1C`PX1t)q^B1c$0NFT%JfF)ukt<M3jR4^p}$4P|k1MkvC}0`8zb=XjpEaWr#!PXlx5d(m6t<?GnTeTNWbC&uajd{*xo3O0J|E#NNC3l2<J>_tSN)Sq6*#mqV?zA=mGXXcvT66rc{aG;y$dwfm=`|x0{Hu&trNt%7UJKB_RA<b68hY7j+u(>O=3fA~Vx-x|+c<B~nE0=T!kNIx?PT7@jfSW>(G@y8f$9{2^<Cu=*%V7Y)5>pMB2Y41`5q1z8G%0!=9{J|b6pc;G5i;vEbV`rKz7~{KgHqHgUBefhxJFZ#3`P%UQ77!By?HEh`V^=odBSP(8<(&TUSfvkn9j!f(*(vbd_$BB85WYl1I{kdV>A_zFD)8t!|PTBA~7!9t}d*P9t_eLatvpDG_C%bLeEHeH#;2lytUCc1b15>9kOVP*U)4+uJ_s=qu=_}7eIc%H%KCA)a0Zp0n#wwflQB=oo6J{B6c<GU2Ui4o1avrf?W`NN>dABs%BClBH@;EYJ)A+Ug~II+ehmXX}xbAZGv#Rq6Yt*Xzc(q>41i=bB&3fN2**K;GJm>u$s^@(%BYC{jls6;lfUGP==9ZOT83Yqx~F=`gc&K^O}ku<CbwbGp0_rF#CC6z?^PZq(iXI_t$z}>tE?IRz8K$0|~{D*I7lcAn5@EYndDIk}6nY)uP3`$62nBavFucTOSVXJmn2f%15bq=N^X`wrXEz$WW={Idsij;5(U>R_|PQOQ&9Lw_C*iT)+9Spa1&yG1HMUyRQ{y_n$@VzB;{}*^+{@Me&TZT*S^+`#3eNn^$J`P1Dk|3>Qs*oPX)7ECa)SI*B99ze`LH^8*>V^%tAi2@^yLh?+?pH&+G3ZEmLS4Q%Ha2AU#1R=D;CW*ReS7xeuff0rdOMsSmtkPBEaaaw6b#)@0TR)l7teX%kp-3ATazCZK&{`TW<zx?(ieE8Xf?c0Sg`u*1*e-EGktb`fn_Q)(>zZq=yvF4JMGvaBPtXpdY&QUym`0?uyZ1BBvy^WPJHlbZxxC^hZ_~x>X#5Idw#1G3aOuKe5<GDo$7y1AF_kaI?q*9=_')))
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
