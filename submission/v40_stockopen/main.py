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
# EXP239 native schedules: Yusuke Hayashi (yhay81), Shop Router 0913.
# https://www.kaggle.com/code/yhay81/shop-router-0913
# Ahmed Berat Ozer: V39 prefix/terminal, shared-action encoding and controllers.
_R108_DATA=json.loads(zlib.decompress(base64.b85decode('c-ri}-EL&p(j53My5<F0e<Xd^M=BpR+!6(;<$}j(9DMM2FoS_Tz-QkXes^~_Syg-QjEsoPwX0hP<10~YlC}2Q>nAfZGU9*y@Gt-AzyCk~-+%pYKm42j_&<L5zy9T4|I2^=*Uw-6@Y}mT{`le3-4Flwzx>z#^UJ?|{_?;4%fJ4=|M|av{`x=u@V7tz!#{re{pF`WfBg8v-4CaqkMBPJ_hI|#F8QbJ{g;3G<M`pj?0cX7=iT%(e|`D=<Inkr&VQYJ+WyPG{QUm+;}7l^U;fOyU*G@o?#l=K_;UK;ZWF%!$Ir*(Z(sglG3q~F{+y5c^W?q%@!$RV+uNV|@`v7L^ZJO>ujW5Jedfg{U4HO&D6@~8{5kenfBW<OhoAoO`A0tf`Q_1_4||=|*@rFuihRHi?|wWQ&lleR;#cwKoQ{8d{QAX@@5Cd${iHi<mp{Cm_qZ4SI39oc{O`XUKfL@3mdJ9x_y|5f^RFK-e=YgW;_av*JuHWGo>;Jyz^9#uc6#^m`1|s!uhT@P{oj5W$?OxZzkL16=gGF#s`ZGk>tXh}mp7Wv_4Q}wGgN-*akW_!8-M6^{yJ}X_J_>*zy4d?PqWWGpTps~-~Pbl^Ug;knE3PQG95u!P~PW;`HrtUPV@5f)iiGl)6Cv?obJU>uQBi7J+pa#{ps=tFGGdfO#DWFESYb;(b!cO9}r9|xIk_=q2z_W4M2TtVM4Ee+nG>sB@IpJ@}o+BnEbiL7p+)mKFL{xspA}Q{ejo0Z<ysk;kOz$_H|fq|7QG^c>i90_wApYKl1Y7!|}(D|M<7Z-#@<p@c#c;9&wky1b?s+@Par#`J3m+VDW9Z@7|J@$&Y^C?`fK}Tq(zQ%Qt+zN|%AElc8l%U^ct_Nt2HTkL;W^=iL~Si}V~d9x(r$Fq6G=<@#rCGfc35hsJw3X<paX%A>uW4kKrEvhN1gIr*%2`6_GNE<^8T<(n?P;r4auUygS>1>l6UP$D$)dZO@yekJjyVtFY$=d;*KU1RL?<Q<7{6ZZGy;vy5g$kK+V7Xb=#eD-X<-Jhk|1X0!4XszW+vfshk9F4H(VCBOjbQBEt{0D!2_xr!^rT=7>FRP%Ft60;08TLTdXTOIDn&RYsGNc?_-XKPt-2r**k-u+nQ|vHKe+i~lPCbX@`O(%`CiDyjaGRV~_6GrI{I)2J_e3Tjj#GvZWP5z01ilcOY|ELuj73;Y!TPEOoTt%<xRFEktN@l*KdX4It@SwwRf!i&_C@bCfFq-F^Ts)k1HR71?2_qSlImTAWL819=&oCoc|TR&Q+!5z&z8Z>c<oIKJ@~PfMNIQ5VD+x+S7fSt$88Ak7t;xDh;`!<^la9WDTIuCf$B@p``Zv?YXw4E|D)K!0VASq77>jHmMCxPJimy?m)Hxu(-Yjl-x!yVYeWz%3cLQ@l<pz_zWr{_lMCv0<kK40K8V_k59)+*8MUJv*6oMFI%jpUg2-Bs6ODsz9A>qmtIO`SPz(u?#W~Jv9lhvkQFU4uCdp&g9_R%A-V(<s#UKC#X~b3K%jGiXAQa(I)ye^Fj6||3LnlB%*ElUOxs?l&d|cirEkSjU2>=F=RRSL5Zr$}Wdy}XrNtcpy$j3dHtPntF8mRpd;1Yb0f%7=EO7{2Mf!9&^!c!2KGXA-N*(aa#)9)|8RU;FS0_^*676(Gd%F5l3m)pjUz??r0Ue6-<+o<yE^%FmdIC6u@Dhq;fvjPZCm-C;4kCdD}E1`x%)w|0t$0-_*Q!|c`b-R&CM)1gR(04hC;!Ly<{#s_N382@9=F2JB{*(LrkB`5<JN@nW`|tk&tZkGWsLvaFFaS`98eD-{6%o(L(|h539P#Bg$uZ;l+3QtTuc1GW@u%;&5~jFM<bIS@as@Ab6`UpKwN4j7FLGh%b`!MBR;Yi*y)Dea0yo4b8?3bCdB!Mjt-7}8Ml1D~S;3FfL4qO$cD<+U-z17z4&nOVVdX^9jTa-lT$2V-xwOSDe>g>o?qDo{&V|}eobHS?9=dBXyyM=C5dwJh_;2btui@*<%jf?bj5z!ZNWc989>AoV2nPhq{GJRdPkb)Tnx7AkpHxHV^|y<e$93wHM^Pcq<qss4gAQ}Nn?0RTcTn>Ifdk=#uvg-QFd%k}3~(^Yn5KiSRFIBu*1fo{AVGpk<=iK;Pv^nCE@1!8ti+Nt_@>{A^H}H_4r2hvlSA}iZNq8z#GRkA#DRj_VaaAU0+raTDL)u&JX)!c4Vt>I1P-3=Ky~<`ce*(5%w*us;&ZT^kjIcVxy4`g@tjSYSkkB(jjlo92Z=G=^@7%(yrr$nx)kdyc~gv$L$=~1maL_0v~`xIoIa6f2@pPi^4}#mArOP4v)?xEn@pQS<-4Pm$8YuS@TSXC!~*?bvvQ8ut5s!5+1+EJHZl#=#3^tA&~pm*EK=Wm>R{3#HjU{Ni=A}&-@my~)sf6w36YMN@#F+K@>|x<=QMbS!_{j$ZHPeBZ?FW8#;x&9N!YrZfyLl5Pl#Eb)!wD<P++EG)t@+`#7YF0#TD<J{I-d6CfJB<POcTPMdEVJvQnxY8jkgj!2Kb1A=n#6@1>7_gOpfsQ_thb=ShZ=^d3bYO0|>JC0>pHojIaA>h-)vonUEybph($l*CwgXudpe7s-3E1A?U&Xhhd7=+^@u+A$;=LE5vavhUtzBVsGM4hV)nRsb%ft~p1$f-MzZ5qw(kJ&WC^fpt{BWb-{FJ;3lV@GX857ZPJ2uID9C;pWM;O3YVKPNb}rQ3#D!t*;GcQ{X_P(v34R5-ouZb53UYE4#eFKVJ4oj><MU6CB;0ju}j7oUzg<E>REq=xfRG?LPhG{fB?|R<P0}m7K=@`ez<CX;JEc66TADXswVF>wvMu2hign7@8&<*I!0zgI0}%lIc_=t>EQYF}ps}a<6s(adZ{O?ZX-442zSc&{~+lYKmYtEC@iAI^MS5A`|mTR#{vMl5!k;giHjA(_pG%)~!?DQc0>#h4(3S@hQMDA#_FQSP86!Pkm2mx4(hSo(vhtQ_|2d>UJFxAXKSYTEc{#X^OjHTENb^j(CndPOXUo`u$bl&7?g62)tTr$;XZa{8lml@AA*DZ(ubV0EpvFQsW&}>dn@LjvFa|k?l9*ABTmKKu;P`kJ2r+n@>$XC@zkrcOn~;KLRPk41=`7XIt!2^cCV>40nm&x^&m$d4lSUrfsHuBkXMjJ)AlDGs#w}w6nPJjInGOZ*^Iv^h7a7Lt4941%!_=(~ifA<_ZZ#1=w7xQZ1#J+e)X}Knuu|j%F$tk-uVm=8Oj9n>eh!#8Hb4c-tH+(OjYRM4zW>VgZ!{0A#0gCh?A|Rwm1GMn8Bm*b+==$wjrQ%Z(LZ0YzTa+dauCm6*b_zR5r#IJw%?c}Z*y9|THHOyw24f{M)f3l&T+2CO{8@N!hQMOlz(0Fk3%B2q($vAw)<!K~o(p56HsvTl8qc<e}de8kDoO(K3;TC*pitW}A+76`MjpUJI_6A?kp)XfWiW>u4+MYMUwXHctr^s;y^w>XQ1WZd9&8D+&#zHTjxlxFiWPh2a|#&>H!T%C1FzF-@O-}b_&@9!@!e;j2oZCiMXqIN4yX!i~Icqs1&{0+a&6M?hG2mKhY&K&^3qEZ6a>%0#rF5#9})_=h757`1qI!ODisH(n@{VYDvfi8s_AL*Y=svt)~HeE(=Mn2oofS`m|v-yGnaE??#aa6b!B?1}3%jnHz?SP2snEx>O1-!9#{9N8=W<=M&oHTcZ0n-UWzd-*8Pz^U}?q{pI9k-?hhyDJO?}a)YG}xm2$-Q%)CwuJKA2t<g1xjkss43~0^}R3Wr?-^%)*a!Iv0j4~`A{|oJ@T8*Pa~go#$<9T>beGzoO`eBkUzdGC2(X6AE``l^Jm=bdlQJ^8W)S9^L3gNl>rA&X1LtsH(9)*Z<f7PLE*?-^$-#f7pQK0Z*Dx&t$fm*e$Jan4;G_%b0rFbv;2AhUWU9_aMaogASmhySo-lg)aN#xKfdbob6!t9R(gg#nxIXNdOg0*+zQNhkZZ(ZUeZ?@#byKUmdz12Q@C5rL3YvU;l3KxnYj33h4<jN&{F-b@Nb|N`mQW&VOiEXU(}izC2$l@coD88*w40xAQf7X5Q4|541M5>%L2W@N0Qx8Q5B&iXi%jI-(jNaRWYv)Csl@pu?9Uo_`t=hHNv)eD}`)_$_XPSW*BWTBCLSxy(Uk{g%Z%(f;P5PX(sCA6lcMX<<h%-a^+PoGoG_iBX*hv@fE|zJ6rn)V$^&$L>v|DCj1OYzK&7ZZG|F#kufVQAMm7n9a&SZv6A|20w7OA89Nk8Fb}O#!F8;60O00|3Qt{_g`A5N%<W!IMg-{_x${2OnCc_!226(}8L%XrJA}oPPZGJ8XLg^$vZ=~DVNo}}Iap(xI_2el>WhnU+Lga&NFl4=)xik%xISQ!8q5P=U5x;-q#{<`KF64^VV=mF9pB??iuB7`-Pkpmd|jH%o$BtCREX|e>bJ|Eq^S@-u2W~nj^$;KmS~wl%74w@K}mkjY@my21eIRSpTRhn$5a#8dZ0cFmD4~Q*$l`k7@KnRB={?^j2`O=(_RrjG&2YNAng<^RgIVuI90^0czJ;>8{<Pv=%A_=m1&4<1;rQ!RVM!@*-etvUoLG0m3+YKNuW|iOac_QDbPlL&`lo}Tl^=VpbFPBNH=KPR^+~%*73Wr7nKZNi6wY*)62!g4g+in;zrm+-+8WeLeD5#=rW4FoomrLyNnCa%*(pw*ThgtDwVi~ll(kcFWgiE1_?I{l2cWxQsM!Keen<hBWpQSgGsR$T}FW{c4Do*-ax_AlLAxv<7<rF_Rmy_Chd7ytxpUz;TetcRC1!F0tl|%_!)7Gxqo|YPuNS2m4nQDq#=tg+dcdpkr(9~()*ysBt6vGxL0E%beIbLoDrpXht+aOt??1-&H28-&=9OoOJVd_I&9kCSRFK|0FjM<S1ypNHaRNOK;M9o57(kbN(dG$2U#7t8Mm?~1;o@7$E@Te5mi9I!vu3-tM1wMVF_sj>?nPp`!d`Vd}hmQTxuG{$}!)&kQw5NYq&rqlT16N33r0k9B2i<Bz*>LH`M3YH7O=qqOXiP-H}Q1)^$m&WvEL0d>7DqLFTz!9-~*-rpnIt8tiUoPioqnIhR<_R0-r{b=orNcM<}FZ&L2Dix-RIWhKR9-<K)-njSSJ?1I&tkkdd5N@I#1&9q#+!ejAGYp{>e##q-UFHZ285osk`^!2X*K&5A;wCtVsdRpG`h2T98fWac>h~d`u8`Uf2Dh9`H+C{n%WfA!EuwNJ^mXB$|d8NT)g8Rnmv4V?{JwMeeAp#-i{FzoXw(`DID)cADiHZf|O0q*Vc2DR+iXagKY&30oTd_FFgI2IaLk=PH02#D0rbv{V0T3H$;Zdg6rq9w<+0Saze5)46S6JxtAy2Vw>s7G!5rAPpY+ge&uIP0v?jX~>*!<XRD`WS)!w)J@)fW%6?(R_Bd2d6ll8~~%l2yyNL<vo}Yh@Jla%4C{D&GLbYyctDE#g$HYkR74hUFr^Loc)C?FG}&a%5-N9?E7q(<KPVV2O#30mzWy`f{-q#RAj!%hn$H(Ng9`VM@{Z<C1@T%Z6dIagH6a#aE%(v9ngeBbT+M^`VU8?E3aI>&5ic#73V!0wV9z^|`k7U!tMgU6Q+rgm<Tkt;fIr{VneN&O}{80L&<aNnCH~0rJdt7iuQY!K%8a4w$RY&3l=Ho}X8vw1i)%#-S@v#Oa(&Y1nDvR<21M3n_zYO3USP6vQwp=EhO>g5q-FEF1`dY;)qMcA+eqsO+^bS0~TZn(_s&+{4R_1twSPJ`v(E+^-;=$XXmTy_j{vQAFIxWvS)?Ud36W5Jxc2cNE3NkMJ4aM>l+kOL;yQz(I1Xhr!Q)*Mdq-Q{8+Gfc!+@LtcbU7A<KxLk3{+B{8ID@}!kH_VZJa<I(0DUV-kgNeR*>PiQ;4X7Y*{l@_?AZ&P#1A;nJjNj&a-eUzWx{~hcfOWdasm(b135`U?r)@vrTC1~c;<GP89qeqy8u3jFWKLp_Zv3JoWuW(*f8F+xvli+K&z;=4@s`|bxzz~Ryhk{duf+sT^^pAe`E7LK+F5rWcHAf9LYoZ3QZq7x~1}Mb7`#MU<MO&lHxu2=zoN1LuxuxuiV_7epf@`kfpa7-&(dr@g@DtGp*5I;n*;Gy#u*-mj0TxI<peO*YnSx~wQR=HU126>zCISqG9rBf`V!p6K@H>HR>qNyav7H@JgD!RxK9WX)5{$xH${Q&%Rl+)%*a+<CRqv1{8*L9ZR)7O@FDMNHlF)@8FhW)D5xp*P=dyLSLWFvf{p~m=wTjM;(m^w3<+Vt>cI~4EEHjcqzt$=qc5R1Rag<QdI(D&K)XOK~^G-Yhr5q9!5#9Nl^)yUZ5Br_D*2kelAp--iKq@XN#-Re2F}FDOqBs^)SfYQydIFH5O$&N&Pjx6YRI+>?E$V|#-cZ|@dvxBxr#yV}ithP<iKD6Tc*y;B1@&|}2=fAFP58W_iQ?COY}W;1P^|!+wJsmyj2yDVnb<L(%iF$S8aZHrc~ph3k)nIY0UpO{{EXF_7z%71Wwvos_{CIHV}L?zY6vt7-O!Mb=)ZzcS-bop@HKWeU1eXn864TTjSP@z6{kb;V%myvml_TF`y>bN431SZ;2Fn$F7+i|NsWs&m^ymny<~0~tvr_SKXAo$s?2@?tp^3g%+hJY%*rR)esqlnewh2R=1c2B&#|zYf?}iBARY@4Q!#)+zhd%mkE6V8&0&rC!7OvLJHW}Ps;tQvrYY8hX%YqLc_*o`mJ~i1*>OkFZ>G`444k_QU5SBZJQcIiMYIk(b4d+g-HJm=-Z$BmJ-q{FDo?R0x=hGXy2hZ>2m#-eSr!s25thbx+hc+y<FrRMRvjv|Oi>fz3f;7|yi{zc2;mVtDup_zD1D5Om4UK<_Z>`tgWv?we<=lpx$JL>!x;sr<$Vqj0z=aegG{WHOGF!HgWB}{UE&N!^DAP(CKX<lQXarDOs+@#M@fP?|H>7m55rsbixh|&-xb1$n+Rm-^8!O=25xpO_!f0$$>TLv9;J&|-teqknU%|=|9Ocb!rm8+F9>lH0}0`)?x>gy4ORRlE!uiWg02s_kG}R4m{-xSaH~Qz&1XzWH-}cisVcl&m;zBnAt}-lTdaXn%`HFKVYN>l*A*?yIPIhG!l_rru%4rA*=FWgBBg`e6{3XJq$ty(I76rk5&fwwm?qIq#<ixvI)EGGk;eI0O)d-Fl5$FuHhTu(H{>kEKIAg+KGclc@z#}jz$0U;pOvvLk#Typx6A^K-D$MW2w2x`*=TAAuscFH2mv+th%^*4(L;i^xu~gbF$G{~nfZ2?kW?yy7rG4svw*;vf%KgiV&usTACkx1gwm|x7A&0XASoy7Q;h`TSero2IudcXk1V52MNX<FN1F3&pvQv^o7{)@Q*L6M<`2B)!cIKDdoCU+J=ZE1rZTv8Lo$|<((t;&?g7a`<Obgrjgg)U22%oJ47|=j@~Vsc$r4%t^S{#)AiQBIhHZx2ho$cXg#=rfd2IFx=onK2L`r<<g*mFHrB0$aw|1L9^)?<6!&Y&yS@&aE&2ZNcYk?N`63nA)+5gcR2y2a&>KN%WHN`U+PekT+;2NuydYejlU=!&ND@4i!F$RrWPP-QC(aS=PR`f(#+&q;;vFkD(g5@PF_n_OuoRMzIwk4kJA08r61U8WtNO6~K_w2l@xJQ!UB9X74nt(^c^@nV%rc!VLP$t+zfi#^V>vI^zF=3o-pQDh85IWxJYp8J#rkgmVmz$bQ3bTk}w9&afL9KY?S$BYI3!!5}6Nni?NM2g5LJ5QQc~Wdc1Nl3{7?L&n4XHWg01}YS<~eY5rg9O6r$V!d<Yz@X24v(1(RYKl&NM-pMWU(M(S~C~0_J4*4>!;5sl^^lCl9<cgt;kFDb0=hP1RU3AREe?QJzxdKuRE`TH<$VzLT6YO~H3feG@|&6*7d4rfsVBLyNx+mnOv~hBaHs9tG^oqm(y=F>a!YCCV?HG0M_+-bk3W)q-O*laS6O6Sryf)=96MSw8b1=kqJvM3Xw%DzUs^-$*SoN?1RQ@v5vUc{QDf=`pMRmjDMrg(f-LiOZDOOr<uqV8ft(546lXdnOaK?pdmUl7#?kqU+e3u-0@&+^3fek^e7r*gsWzTeAg3^w|A0E8D6D9l>h-&nPTXs=;XL^RI5+z-G}2l>&?Os<#tHcEJ@iK&LRTHo{5J88er3!VO>o=8<Ux>3~WXXCfrM^8<?A)!SfG`5mI~*6nJ_`w!LmMs}b#`-Uh4F9R7BEruWGlCC5{PgO+kyo20tZmDxJ@Ld__(4xn6^8>TprGP@Og}{6fN8lLDtT!XNi)_AK{|oo+;PMX!U7;o7@i^qA8qX_w%g~dum&e33L9}+~IvRqzTpE?K0U>R%;(Ro<k!k=;MU<o2G4Ca=wEA0@<>)r0!wF{w215$<?x)cl1qE3Bx(eA=sQMTfKrJ74*ZO+7680;Jfb+25y3tt?-YVp4j;O;K=->>TUBJ`_I$rWR_yaIla`ceH^t9IUuk$RZCrE``w4#Rt+q)P84r2T04!`K&sguW7@ZS`jM=*}d&wLORkixKYAkEnZ1sP^Wf8+~^<Zzu!Nm8nF2e-;Oe=2$p89OvC@}9^qLr#dKD-obw-=xBC4dd=2sgUKW$~B_t<Dk8NbEYhR`mfKWuT)nT#5Hmuo<?F<O*kHJuVhq|r)sW1hT?ahTIxKj><M_|s@e$CKt8d2L9}MgfQ4uf`wEyKU6CvX5`3%VK*-ceN+PsXS&>DIdTYi@)q}+%SZpQx-=t*3E<C^l@(C?(o<Aks1l!}*?FkX>Ck3>DUJ*1rBV1VW7i>$9ZDCBQIFi|2Vv5h8f2dtcJ(4xUAxfRXBv1q7)pCuW&g;NkBICu5dMlnn#3e4$hT*i$WjJ^FH9{D(od)%+*#H)_nOH|&Gvr+L{7|F~R%)f^IGkZSR!F?!B4-MoOfPRW^rN&hd}$kA;x<FZat9Dk8G2}?f*%~l6O(!%b$vl_gQVT87F_^cHx-H=Q_DyPgR0mWV?c(a`%e{$xu<4hX{mRjA&6ke+eI2!X*G2@joUttLU22dhTU$bd~9i5(}<MPo#kAgljrP=8El4#p)n|MlGB69r#Dk}Db<B~ZFA2-&y7W}JFq1M*KZ)LF}8rY$I`qrE5ht}*3U!NktX!kG=w{X9HppE=TG}@?#ZGAM_rxHU6O3`)&3PFc;Zi{Fb5ry91Q~#%CWF4ED{xv0`-kcERox02Bnc-ZFJ|96w|pwhl&9VImDItAfzG$LM1>5rNo-1R>jGkCtDCtnj(|_ocS6UsCP2u3_Rb01a+#ZZ#c5vHo4!Jaq+xuuP<(igF?2r%FjPl;6Sa;RzCjGFo;v{!q1Pb#ZP7SPIW6N`gTlbgjE~PEdx$9`?TMG87J4W$?Hr+o(2Kbg{+BH1KYZCoJd|GU5>n-yh~C>#%MR|l}quKyM8`I%B(SyGi@{NRlTWLPL@l(<u;luJ+0-$IrG164?){~JW3P9prTHvjAZyFR3Z9NJ#ylRkPMZbgho<W=*!K|#$^U<9ye46ofaS&bHH(;liHY~CF6WXod1irnEB4>8FyhW1z^Dlzn#gkF%;5sNt>kE+5JUuvxJW*(nU=*RxIQW^l^SSw<cZ?7K@M^*(UJTm9LVp6PUZJQF`lBE*zh7-qZuMIK!0qDl8ko)5Skxo0+g4<V+ysl#>L6sBGH4OqTSn(l(9XhSXgG(U<|YwAvq;N_;j@UtXhT55ptV2^5dtz93&~PtV-z>h;y%x6?&cxTiH8;+C*#z6kg)^Qm6`-?B6kzi{PMf>^pIRHyKoOi~jC;^d1On8T76)*W?nTYUOe5EIaJ^5NPCXF3u<+R`_gmRul8%FKP1Yo|s$KwIZ9qq7MNn<u!1EL>X_xN?zNqs4Ygq#1JhOrQVi?=R>8Jnzo8ACQy)Zl9)>EzFkn8%akm(y=+k?#Y#_5Cm48Bs$(w)DmXCHj-Wgyud6flS!@_1LvqQq4BN<;5$^kN>V-6UkTPjWwDl2D<19(s2}EO%{OvKMSro88-dEUxJBu;!>bDTiZFYM?gQBOOi3uTPV8)W6$v2lqy%Dt1+e@U!4ESw`(_22$_iiU7fLN)^6!iZ$fiifEom&9Jf{;DFc87v?k{*vcn`?ooK1lkE&v2_f9Gy1n-0gt@Z*Bq1xEkl0BZK=wJkxP0r;~J8^wY^RAxOqBF%!2(S<>GO(qurO|p*aM5hH)Q~=UyAbW*mw|Bb<UF7q#l-IgS31YJzw3;i>&@zbT&glLGES-u*=6Ts{Y6WS@R82O>TL4vnSOr*>F8f$-YK}P+u_vL8PddNdRwf)d#gIN}84@qSfaiXto=SEA^Imb21}+7J9wmv)#2bh(Wz;_bm#VnK>I;R=brB>CDfV>zbMZfr3lKE_Et|WqwJ-}rUYVo;>_S!?p3)_6-UUwcA<L++?MnQ)xa82Yl{WRAR9K^JGBnX<I~_b-<EbiHq-M>~9FzTH9PcoqEBpFb=d4N0d<^H~)?M))z>B;ztH)2IFWM2rozlCgqexJ4BWWXu&!@s{`Al1&WNM>ElYzKG(&41{5Fzp7ZqBf=&)>fedUVbr1cAnAds&&mlR{8RFwGKC*)b{)xqylFj}7?T<t-NuPQjQZCkJUc9UX&rIAb<GWJ1Q2B{R3`hP6$BYo+yAuK{NC3H*v6AX!kCGFzU-kaS=SpOT~k80YfJsSg;4T+%cwuaT1!Z(J)GwJ`?(DB&u3+>(*J-SkW8sAF{M^M&jl&<`G*>l7hu#$v{eXoPCj)~!bVfCS$Gp&fC$Hu^%IM=20Yb+^?HaPqK*O(;-4mevC^&Shm}+pOIOt_spBP*q#pC8kz#i<l%ehmPe=GM32%5rHNM<w2-SMp|S{CGS{}&Q@?VYSfpBZRIH}d$Q85JPTUL&_iJcst1$>S|!OfBBV{Hte~Yv@fZLZyNg@}COlW-68%Re{qOXIFze=%b$k%%;{>NbL6SR}ys^zs(bd0G*Pqu6(&T-iUJr7{Io)6E_rXEaX%<@*)+j2r+$EN@n#1L?V%F_!@_lYV5)YF|nd^HXL8`XOWV+4~Tab-S((R}DZqSg*#bx%cn_s4FLVL}h=~H!ht)CND%051f;me)g#sqYYtcy9aUaR*hZ$a^Dn-U=rGKk+v63vj@uc}%f6GU48r{W*O=oITnua$g3Q2;ZchcjR3ith63pY(<FUF!oRf?8s(GfuQH_jarkUGo_0^>2zrEKggHDL-dz2BPYJ*WH7FJ`|5!tdAAlpt*McDtx<AH)7mirTxjTwX5}?*myy8M0$964nUntjA)6lEi?(IJ(4@kv{s-O(5}P!SG_BZb88AE2QK1A%$7<WOpNv8&Qv_$v_z5fYANTA8zF(VI|9H-tpx!`0h*0@X=$i34(7s%9#o-m-gARh9N!~jAxR4s+Ro?uojp9!#-L0`==CRe*ippcXr7Ele-J%^4xvyyb|^i%yX84@ke;8XQ*$|t@9*yi8m7H|Fs<QIuNZ$BcX)sEZ?b1x=DUZACC_(p<RK;FG>bnJOp)2?{tAa|?kTa2)Iw9-<Y8<omI_YsQDFx(<M_oXte=+HUNI-XFcFIYCV0fe4n2X#{(t-P{fD3a@#D+eHRZWGONqsJ5t4cGO0xz|;A$n1P$$-RH(K3^Uf3XL%Q68)-mYZ|IGV{{Cng;LveV+<`b1vd2u*LHLO6v8uw1s!tb3MBG)b=sm|1((Ua79tJY1kjw2hN8m5nfY29iCsRtJhXV|ID|q!}ZaOBTtZT%|kkWMm!SzNm@&usWyo{2f$)qKk47xLv@m7`O4#Cnfw#>uV|AV=H9CC-DMP=I%``&kXEYDYND0U;Q~4S;25vd)Q>jENK(qvL)?D;cJeOI%%g4$%RRyNqzVrfM)Z`4ZmSFpE{wh^aORqsi<nb_*C~f3f;mtT3-Mem>~*ZpAMzQ;0mPf=YyN3-xk1~>*A~YT8ck^CfHEmDV6wOCZw^-ZcFQJ(}lUqbX?;XvtLZ+puGR)@X^zf`SARFsLFYrhjK+WL$iMT;_}1rPYrHD0w7)2R7)@Tjf!))IWTmx+8vLD7}60{xkSZVikULgq)w;NsMRrre5jU_C4ap@vI=jC#SCt2ampG1Y8*FSAz~~7K{}qF#?{<k(iO}625^tcp$V`AN8u-ujo8c#UC*KwepC2SRib(My0*}0VG6z|7Qm!G)L&@&&05Rpj;jWhY+yk!VTXo1ssg{dP-Ut~(=y|B)qM{iDaDsoz&F-`W7xpL&AF=u{bJ1#ry*G;(nZxr&?K=0ySD|~IEHnzZFE_Xz~_!prGgwJ)yI1<l!M;};PcmT=7I3roOgM7aJsPe;nnPQj5abCqWOT$1#KUWxxk`DwUL<46Pb@Mzr6eS5`K8P_Me|-5$^HB%daF=5cTIbBunHVrTmyyE|CNpo8M)&IiC3&GrXL*e}XAyD);|;e(&###OZjf%UgI^ojDJP;0I*NjjF>x+mwT3Ac|}PoU=Z`3xw(acQZXNNxuFv>X&EN8Tb<^P|bkA`4^0r>CFFkICFY$AUDlo=fS+Zw4C($cgN;DTlMH+NvX5+oCg0jmJ0A62lkDQ<{yRb0OPFNmFP2@Y**}#uC6y~F%28xW@YKpWP!Tsw~Nf3#pl)#fI|7ayNUp+blKmY#i-2dz?uihfgv-dCTzW4+@2&oL&S|fTT7Wrr_n^)gn9*y@?PfW{z3A|Og$`SCV9_t?s;`&`kuc0%ZGQr{&Xp#y!-Y2FYmryGcTvf&*0jMV=sDs*<b!%f>MyXA@d#qPovL}SB~lDzy0ygoM;&D_V{b4F21SpQ1cK1%J4DjUb)=}jOHAmzrCc~Qf&III5CUwG;Z=RG(Z4GJ(0_f&Pf0%s`8Xi;E`+<9_O{lq?%Odb)ko}JfT>JDEhngIU6$P&H0qWVd0wBqZX|ybOGoa5Er~JXZ0UHACJFzUPPAc1=Y}~{=DYl5;;c0OOSRil$sW-;2_maT*cAEibWb~iM{%k`tan+s>vrLe}orfSWIG4#p2_t29V1#f8B2dzaCp}wVGAqxdUNMfQM2ky5g9(_Gv^dM<eO*I>~Z{cnpWG!%d_JX8Qr1^{ILcYlU0LFciB*DHDjP-Xw8_(If7eNP-QNdxw;CAc8%D<M&)Namhu(7W0+1<c`l^x8uIX^vMzY>x*NmNOp$OdTm~K37l&}<crrie{UljGbWjFsibQu-yhv&rTozxK}qfV;b)<7dPwpcvzG!_%S-D(F2WP4E__{?3C2UG<%8BMNx9#~@*#QzjThusP4GLcgU&b5Gqg0Z9l^b=?xtO}K4JOhQIBEocBt9k5ogNct;EZ)8!Iak8qbvRv53=Iv2~Lox(A66NIVzR6IGRI=VT;il4nsg3+s4Wvf7wOr%Uq;Cq9*9gzs%zFp{OQy)}1|mR_@fb+v(xWPy9L(zJt(p{wcmP8hqrfRHA@T(i6r#HNaAV5$rGCRv;^nmxHH(!4{)9jddEsiK1a7?sJs*}B#sIu)-eVS~sn_LxSkj6mL>xwsSo>mUmSMYmDom=v9%EKE%|dUN5s<O~I6#4#&@%x+QAiZI#BjOhk|L3PF)*Hlb+PSz_`<$alvfa8n(B{4tL<Gj&5q}CWXjcU{8r*2rEG?eJK_FT#QyB>L>0qt&(;rc_|jWi=aY|=W*w-c>{SuwHflPYyyS5vJBOInwJhs!Z_Aa=$kKRQ+~fvVZ%P>68-Dub}S-fjOR6YJ;}JZ1L!4Urfo1V!hAr;sJ(b+WFg3UnwO!#WU=*)e#c#QVKt8djSapSaqA+zrjPVkv-;RC1%9oKG}iJw8eA_HmO0Z?Ulop2#j!pggx8h$k$Ln6+1yWszlw>x$Esu*S$2z5s*2CumDIU4;H<m~;T7aKwTlBaN!8t)~Fb*SWut7LoXx%RY^_#WtWSe`Vv`ZADqUz8}0b*eba*N}yNX&T^LF(tmWIZmhV@SSax(&E}}m$Z#6RhpD^rrhk0jm^C=cy|L`ChF*<a@-J6NZ4hzE7fc9=^AJ~{1=of%khVfh^<j|8?0&`QyQkyIp{x59i1%Ib`mV|pkF*QuA+w7srEc0j0mIn^5$A%%JYnT3C0fRM1vcTfTV`j3rc`j8Ayz}^lt|bWFSMn&?2~{>-nz68VDd4!;r#O%6XWvtAWaH<DpjLGzkt4X{R9LxS`B({e{Qq$Tx-J+xbz_U4T2^rM9p{*LO^*K;eu0gFn_`1YG<9F#={;~cvgqyC3(`^&r4>5aT>ym4o<^>YbWh3LJuAr578!(-7AY(E_*m~BbLn3gzs@;O^Mo*M57AiFN+hGy(!8$P1^~PlrV9$YDQaeQLxeS*v#HV?G{`{FeGGq(2E>}>M1!(J(^*|w=ws8B=N?V4Z3~u1%+8d_T@&qlUvUN5{Q^*yN0+FV4P3W8qDq}e@z6m*-pljo!L`2S^1^nIFOU7wIn9=`EdI^wMyu-Knm6T>JD&lbbCVU+YB@j^Pt$lEY?7TR2$K&tVIcDSG+$-2c#$sh*v?NCo32v|KyMYplME{LGQ^5bj(eqbWNxb;9Nw7+EuB#^ZWUrIJ>fWOVk<`zo&Q+<f^CsVnbb}h0<m6SlmgAd2+Dr;jh1{X8y>|$w9`onhC+)QM*{JS8lj^Y&CUO))jzbYa2u^QE8o|Bdf|LBDi(Mh?$A#Co|;rP*>b#)a96<Q`#jyzrM;DIcx9XiuGVzks{~%eXcTYFvydUJgC8vU#0V3Q8^9=QXy|(eZ6o_>df=O9n8)v)=^;Rsdf)Q37Ap{fIL#b_?PzyT91RwLZ~C*083y@YWwCIF6D%qMCr8RuelYrwWQIU)BtUX+XCsUVOK(|eXZvK1CT$qjM(ioEO_9pZ7^bXH>q7sTn>zqOoXrylxi8NxsaC}CwTD|rG;Th#*aH(ihW%zb+1SV)IL7_LE77gL8o1%BTJD=p~pMtIk*G0(Pvu}8qLPzw__-ol%5jvr;fVGVaDs9+FGEyw58L>H6WNPI8}p485gTinNdtZI})m`F11l|*Ikt?)Aw9xtt4$D)D)1S5ji)y*ONpWAcPxu+Fia5AKa99<Uw#^&h53MtPw#nc4J{Tu{^PiiYm<$b`>%Rni|}v!KN)tbHGa&v-kkQ?sd)RIoxJfvN5%lCcMQ9S3w3i^v(5kn{?04Nbw6a=nUm?TS_zD_Cq&IEQaf*J|fzI7A)<_K&2YLO`|Ey!3eNKsz>$qkBM{?n8j9@UYkj8nNhQ1&}(&c-2%iWsL8}w;AYI-Z@=#7vPU?6PW&(oVGNmi&PXady4>0N7wW2#5@+O5*eT39f#Mg244oxYS;RV8?oQ`iGE=YkhAlqAwHPRcqQsdgq`5sH5IJ~eMl6<Jy#@@HL7=!9DL+KCag0XJCftG00vONY28H>IY#09+42nk22L_Im(kp5ea)gF{2TLWg`4|9?rMmWX-c!~D4HVuc$h-0KMh9TQ1fh>uHhq^m*PQ>B2BgVUO$G#VtwN^_O`6I09ZgKIoc-}w4UIC>%~k?B6b$bL0U05Gpq>`FoxLLNfz|Q7L=?MFAjK$8+$(;3O}3J1aHROy5lh6=H9N3EmDN#MbVU!zUys67o!6Vu9$b<7LNwmN{Ls33m1HuCUenCWw+U+|vT8*Zz<-#A<@NILmseS&AdR7sl0nU3<048!*rJS-0u-zxZ9k2zL&8v^y-!yyanuVpR|y?p!bHqufc7%w*k4U(MBQdSI|pRoYjYgHhjEqJ>gXLDz^$o&wdLM@hgy2jS>Y@RPObNxupUc2IyFCEK?e!CIC=KFuYI#SF<Guu^jrdOC^nYOmOphP)=DGR_<*1QV8#&rxfp$w#x%X>#kdqvM_&IaP~TTWnVjF#=P1M^ti)29TNZtSTOEh*#0kZXuC&x{mo$*gu|?7+Rx9xfqEjLUPU-I_hj39_-LQK&%Q}V&Zi_c?be9IyG;kOuB{n$49LS+7@gNsWo`K{K7C1GX&!67^JwIEWg-p0n<%pb7e9<<WJ_upQ_E$II;}P`u*+GxRvg&AB8LpW%hz9a@;BL(IhvDkKxVC5Vw+}m0Okv;TAJO#pWNZK)c(w8<8c#=ZS~n!g!KtC8&{?s(PU7ed7fui`sSw6v`ts?jSpl8p{k<g2Agc5o6DB3PGVS<!N}fR3oY)536m`CBhYn}VX|)?cwxCQ6cJeLezguZRh=@bU!C0Q|4k_%~91B^`9wP%q7)B$N8ckVEjvp)pbY;+Y-v&+|Dw=xN8ntMnArulWwDtOja;3Ri7R`%yj-NM3Q5mysu>bdz$&p%Oq3RsvD(yW);`qnMN=zhAOzO^EnO));Q%D<Cu`#B;Ab``66`xznrjo>~X^?ib6JUBt#u$m9bfx>gV=71cC3tk?m&8p2n444onKo^K<2q0HF)}&{HDUT^6}bvhCY-`dsq$vKBzrXrmS#IR-ld@fDKutBeMD;gex~KxULjerBnzmZbA?&aI=3QgUVgX`%LdOg-6L>oEQe0YJ+X&4QtMA-EMB`5?f9q=5u}45A)74Fo~Lxv6XcO3@3f|N*Tf=?=2syy)AX_`XTI|S$l=q98$)bQ1n4N|nu_quqO@~=f1mNi=l?WQskx7LY20X>6d#pErysBpFcR(l>L_a6Y+A$?C!o~1u%NhFQ52Yphq&0)4JU=Qm5|P1q(i0jRkN-;w`u1aJiAYi!RLU@vmx%XM!(fJnF6T%J3&vL%fh?g`+b}JCkz0iD3EV2n`459<WZkO5|uEi97`yl_7>ME>Ake0dLl$5-u~ym{QFD%_Q#iB-hF)03*s*5F3-RF^%X3C^0hWM|K=r+rAu>6t%x!SFGWZ7;x0dE`iJEYI?Df>92?)*_seCo!JiYjN`4U7M2F3Km^X-qnZg6v%&y6Z&!>xFDZ$&WpaLZE8Je_I$oG~V*Tl%FDx-58v%$ciuP@h6r`giK>6SDUa7`@BNq$4qw2n*xDysOcM{|%xpo5MMA`vgZ6G~R-iHMF6d5v$gu^Q`Et*8z~%_U<pCh<vm=!q`J`65C|sny^#st`l(4ZHKoZ<DKZc~~kk%tO%`j{zUm#Yjd)XQ<#DWBo#ijI@ig5dN_y1XgL9=UR3W#1_7a{_2NkHzSYJqqK?z)9TyCslJgN!izezIb0pSbpOk{ZuB-`6@R8|%%9I_c_gic@fvOdQR%Ial7Uya3|NILyWKqPuv}<rO{FK+QO*uaw1*8$9gydewg~`d?8<iqXgy4a2DWv~5Gg+4-4OAUXD8Lurxiq39Zxg5(lRG^cIRyj?1y)1DqN>&-Tn#(m6UuABdwM$%ECZbvqModojNE~#+d-$w^Vhiy_>L6k*QLJ5wYeRKdtFKMg(s>)n#xr8S)lZcV=YLFb-O+rad;=jGa_q#4t5bv)QLZV=4?Rr(-b&M>jn+o7+kqe}d@WkZ!2AwUGh~r@a)({D~4yw?hTc+5E;Cx}+<~KU@@vkWmB`p*xgV$H!_9?4S;gLc_QyPFT_@aKz%B?NI;miDF%-!MoiAxn748HRUQex@8xE$dp?wcaX$h>VtIem9&;dwFnFCdElm3On1Q1A^i50#;@Q*D$C@1kq>I$po3T~X$XBK)dou}ka0@OD}~?wKCO?4XUoKPlQ9yK?;k2>50MpjTSW67r8TJ4xeplYNOg25DvMpWdy;|1scpj53$C2e5V?4ax5F9|NWc?rYThn=k!?Zc`MP;G1@75`v~nk&^MHTUk-}P2;OdPjbaR4BL|%mq)S&{v<bPoWX4^WFSlm1uhf~y+s%B6nAAGPoK89EsoKL-4D#luLh<V>z(iv~Jm1mbisS1~a3<b!7&>n<l7ZHh0@xr8+A(kY##3f)&!N=!_$GSqjst&<bDzMgrCEF{xEbU||nN@(W@_?~a%aa>Hc^|N3Ki@K@4C3<Ok<0(^snyZ0GJbAqLlu<ydntjW<OGU=I@|z~{9}tZ8Sqj(LWR6tEP^Y!D&KJVsBeH~IXAV3aJVj_;g(z%lK7}j$P8*^&f=_m2J)=3UBH}4|EYTvX*ncya^=u$Q=5;uI-OK2`Ke**QODGsrgk<#iem&aYI*yBdUh^ePHPU4f^bi;8IEZ%JA?#l!5GY=$?OCx->haNYs-?k2MXxbJ1o9FYCzMWH#b0p&Q=Bsp7&gzavM3*cQ3i6B9EdehJhM|&_>y*tF7cIY4JzcJ?CLq5%y8Tnf^ONhKw)l3ojGDd@>+ULw35Tn{`|8Me8(J5`I)jU_>cnAeLer+_Y}GIFAu<j6s-ln>bjyUGclkNPcY_i&AzYH6|<ce-OMkWrw04P)CF%+SgIJEd#>wu>Qu4k6d-mB;vJCo=7O92ss0Qjkm*4@yXSO4rki$K@r*t#v0F63V7sjR;EBm(O|28Oq?y04^WCV1_a7X4M}LbS#6pWK39NF(Y6t(Bo+nnY&rdm*ir9@QK%6?Oc_IzDcmQub-DRi;x7su3CF<H;TqV0Vr|-07Jj-}DqnQAX~W~_;w8=Eo|nelqPMiBX`#?AUgYX>E5M%AfGp&|gSyZ#a4Q4St(uXPhjdsaxM8Qtwd3;le6Lx4i=MfeY(n8{8}uUu3*C^h@GCu>-)=L|zET=xMr)P{tP5(bbaKa5s*25l$bRAt>;U@RK6daD&Pgy>53=;7%QWh2+3GcqTD<bC*KJrOjJ1O1FVV;ZtK9BWrw)YO{z;{nNqXD3qyg&*m0MLdxIKq_bPKe#^a&3U*=?zrkGHRDJeEA=Mn6-zC2;^Y_6Pp3xd{|A%LDh{M{x?Ah!SndA>Ai;$V0?B))Os|B$@zQzhMYk%LhQr`h50nnf&rl4X(82xa64+BLJlQ<x*--1Jv`SPn;K>bYj%ihxGI(f}L*3jPMn3zWQ}Wj8(A?>Tk+*C`FF&K0$;*yTXh|fuLJMHkzSI7Ef@@go8@|(CtuwLY8aHkcGG#R&ugzK?@m+Qgw4Ny<I`IMhP`f@eiEXQmmWX9^X#ci6tQ5lH!b<P9Kd#%so6nAZ6-y;8oReIi$GT8H9S->>46tnGLK~RXT9Jo&P#ozVY25^Q<LbhUGhBIS8(BXmO}Sog8cq>CGMUsg8yNbLA?~p$n`7$bTzPC|i^RQ&>)#2+WhmCue)-TR`C`>RJ(o5(JN<*hKRfb9N1WB7xmme&GdIYJcYlvL6u?W|9X~#PE&wr9q>|8q=*M|0F76CexDLBXJ3OYprA?P!_o|Cr-6xmOJ-pGx|4k?_6|ZLXef>DVBoPCM6&me@vlOhhc1LT69l3KXcV7%G5|f9ZxeU9$u7)6BT2!rbV7Sy1>(Or8qAG7N!@|@*30}6ZqOGxLEY2q9rMU5f=INJW7BvYQmo05{j2)0GiK%*W7jf5<xfxzAZ=tE|eB2o=MXI-VKUXdk;a^4JBWfUP{(j*69~$YV?V;(^uY}yYD?0YT$1#!DU`23oIsXmd!1RoY{Mp6=b@CY+!{PLzH8|iSN3os!S#D_#^LL7L3iKv%f6J`>j{K5lU3|le?HFl}?>dT6p_2$tKQLOUw&h40sxzI!{wK%r@6FLx;fRI7K!d+az>PU(CX;FVr?JT`%cnsMGg}DqSEE*=yT_LB-hv7xuyoGH@s-@BZXahBRTa`c$}aFe`w;hzC84C#bNv<La>w5udf|A##VC;yG>$S19JD{JJt3hcUlSh9in|R9M8!X@#MVsW6ApqWzs<BE^NRwfP?CLuKDNSY5n}^{m&=!>#B@lPCj$H%wuiBSxO)dhkptJ!6g$ZA$I<RM5*((h#h!HTBi0b5G=jGYG5CS#n$qI&lf<$=9Y)N%LDz<B7W*s<=_5Q(TVybnHdz;fCfm^(uen%@ryCuPH9Un#7BW)uOEI^eIuLUXg4vMPXmE+T=7a&e(aOY@DZq_{lQhlRDcm|B17LNCfB4s4sf@rl{L`LBE(~xG=A+KZhjH#0}#46~K5s69ul18^~P553cW+mVZG-aQq=f4U7m5zAR3YLAwa(0CAabX$aMOV-!2GUEM%Hl`ck>PVBwe&R4!^ZWvLU4*9Tnb(}vc;ux(~kfGlAi<7zwpy@M;XXBGSfJs7}B}#wC<Y)w)b?3Q37)~E)hW;&U5GSwe{^W?>NJmY?VtrJXW!xAoQm@bNT4j^bO9UJVqU@UL=B*r}7_)?qSaHQvf*Xf4yHB=C*Y+YWd&x6`<B-f7&AEeu)?Zx>s6d4lIz^_DVma)&X%pRHWwH~g+VGU$HwdhB*B#bCr%V|dPqzugU8do=XF2G(osT}x>1gmVP3h@nJiFc#Sl+f>pEdr9Qe33oVMv<EMInx<CeWdpYT%o8GdVBhpbc>}?6`~SsUT1^wUq#PRk<>{1%9%gYmNzWNki1a!dT=}Z7M>QG*)1+KNz0@v8*Dh#uTY2#KoT4Ry@6?i4{{&Q*)QMh!8ZSzA9V+Cm+A^(_KMd@@Se99=@};)%r3E`g9r6MnY4Q2+QZvq{$0@OnA*i+Ryd*yY9(KKbz5~Rik!JHmX?WF(IW=H>ORjgL${#6PO?WDrPXqS-PFk$-c#@Ri+m_bm#>xz65EAa{%jMlbsTj<5PalXZ$l=xE@3~?6itO8C@q-)w<N#mp*{!|AcQ^St?;ii&sir;T8FNmTf%WZ6j&eJpS>q#PTX`-KOk6!k>dw92F6C)I1sKxK`Bn0IcioqP~o|I_9VyFXv&c+rgKiTM#T<VlX?EdM|(BkbaYR#IY;tEA*A2Bs<XYy8O<*fsIYa-4jk)OaUj{a0^;`-ZPS9Mg*mgGQW0rswq9oskv^k@Gm@htdr;d>mhUzy9O0V*C5vKQ)p7%iP$2md(^plhEYdl{Xd@8N_PTEBm$v^848j+iPgdNN#w}alR5%dBQTsk>LxC}vwQ&~&)=$8`77kZ>*y854PRRRSr^D;flca`Kyl63;ucLNzUOcrO{J2H3T({xKH+YRE%v6(`XWhusQC7nSXRCvs11!wgDl$P@*_&@B@n#(X$tj>GlTk;%nEIDgCPbNP)d>Ym6(zM^b4Yk5N2ciJiEkhY(S#90}gMS9;S*!glXO+YP0Sm<%nSEme=ZQ;20AWc1Feq%arZ;0xE}&0e+{S@+h7YuS%Wx>`l9p;U&Kg`E|Fx8Z=5-iJGQ?)(t#w<h#F*iR;(zR`fy{CTG3q4usWv4qL~>GGLRve2$z`??C`cB1E1hO^-K)hR|X^Y7aKz>dbolbVuYAnz>xgdkTF9wr$tk%_Hmdj^S`_g!6-ny_D3<4~}&CU9E|@Mwe#{Nhuyl)Snxyq~v+Fm3Ac&onA-vw?E&1_~{=%zP!1_#&-+#qCD0TUGgiwGS(W`Ft6cM?b1_Evh6};B%7-Wlb9AG0Vh04!U)abwvNB#0fYF{*KuWyn2Uci==DWd`t?;lC2<VR9b38td1^oKZ06ns{9_uFaoJIn6`_`--iDMz=Y~)XCkCY|uC;DhL_D&RCJFx6H9Korh%X7wE^2e2i^X%tkmVYxO6dw4*4(57-Iq4dSPm*oZ|zF0ntjLcUjp%*;M%Ef8q!#}q=<BVAp~ARHCzNgOtMbx#LYaF1gF{qRBA7kn^&ieTY`EiUnv+B`+F5ha7saU@43RgC75@Z3C1LOTvBn(X$&}A&npdYSw1kRjH4x5@_lg-VjS`o?!FCC``C~Ho43_`Qsz<jeNBG}QUE7p6c??T{c7^SWPuMq5ggU46QJo!cllxXr+gB9?MYatl(dFx+s9qPo$1BPJmuEtabvY7gDNj<tl5oL-S(=xfewwI`xaqzAstr}E)=1L7^tEO$vOjdLgq|s_=!~bRLErL6-X<9B5wk5QyLBRSD=2iaF}3lvoh)LGkC1zA?-%u<<|~=)1ye>J_j$1qlp6#-8ygE4%YZ8WNXhL*bs}{wAn(0a7yPRX~AM4CaXG<h2Z%Onz%m2b3}AaW|_mQk85>^FwZ9X*o*T4Ps!znoYN#WK~Ry%TRa}iRq3}H`1#j|3k8n1iGnq$^Bj8PWg?ZQ93u$Z{F&3Rhg4qKBayf@M&upwMf%i->QlddXV;qt1*=@1Gfqm}V$njKQ-|n0JUqmS*y{&Ujep<`vf|t2#}W0-NMcq~CC-;3%zn9<<?<fzMJmAX3!4pGu9q)xjBu%#<%>->`_1y*+0!Hh4MZ}SefQ(bFYi9SEWf)Te@x%~@x#ln%Wr-?hZjTeo9{qd30R|)VzeX%Y|~QXIoWm->UfzTtDYbx>BGHtkxB>NoW~ZcXO|V2QsT<IOiC%cEOf?xKDj-Y1iCwiK|LW0^Q&CFk#^Dv!qoQLb<jB`X0!qq`!tZ%9ScIx&traFQK3A(>KJVETZUFab^rOcpn9lmrl-m=RMHjw=rB~n0%Wc$Yw-J@OH4@qRlympElC7=Njbmqnt$DJ+de#L#2fe>M^h5k;JN6L7Kf8hMvTSjqUsqf@WRLdx^He(LYulfI4ne&RL}SByzF(bxFj@G@-;`AMsqRgWSxiL`FOk3Wpc=wyV+IH$ryyl14N1I5_U$Z<CR;+qA;0XskQ|zI}IG|!e@A7@v{IVV!NJVhbVIRe2cWAQ`#GlAI>197)OOO(_x`|nxa94GqQ)QyJuhOWkwIS$*LFp?7nUT=jW!esKy2ktE}TEJvB&5ixF+|(sUYxZ<~ABW8kvVIFSH4ss1HuiBa2zB+90FUBU8Lvc$Fh@-ok&MN>JTBxzu=JR^=Idg!WM9S0rkg|OohfNzWS1T)5EW4dmGu^pUw$Jmi}P%!V~lDYwfT;}V5yB~;3JUDoL8A-p9o?q-lxJo(v2BD1CZhxfE+T{AyIy9*pYAz?BxhxytqgULxQ}W^>Em_QU{ElzR1U7?%g=drrn`I=KN2*h|;g?fI!Cwy~S}cbby&$&dXZ!`ISVlZnn!YQmN4-9v*;Q#I?A3tSlAq_{TzrWwo``j(33h!`v?o3R?-sEf$yAJ#-v4^|k;Bns;X?Xp%T;1Yu3`AZr%DaS*zvpc7@+cnW-<^xSSN+wI?gxCEs&&LDc!Jfy+Wk|MK~o919~FPA+N1`>mbVY(D|@&tGr0Ty$Wi2+0J1+6e(f7)!{co8fhpc)!nqv2MIKYoE1~k%SEWM#2e8Rg>m675(G9Cv12Cfn-0=)ifEg|`7V#(3iIq;V)G6;E5Gpi3ra<{t-5U#%4EEPMiW{%<L26rE9-V>Ty?8U&(^Q(k~@IEdDhU;ErvZ8ie3!T0f}(V`u49jM^Xai;N*H0;!W&Vc{JnOUs0M#ssyV#?9q`fj95zf?PVlT`7s0z4Wmp~(dNn2P9&via$%~s!{s3Hg)e(l!BATQoK}xF&(fWVCE{aDPS$3qt;(dJ9{1o%R#jTo+*YylJ0vv7%=UC&lZl91vLMpI={CAV$(u`-f=$fGR}KbE^rwz4uL1p_7$?aD%g%feChBFpk3iMkV2Dx73{*<PB;}=K__r5uFaDAF&0f!hnQB;uJQHO$ft;r7rfOP@G6y_FK^QUN@TSfrs3*<Gx%|In8Wg{1UPvVMq1v0a_?A;JrgP2e3s0tay)6O4MC0Pxf~T+csZS;Lm%_ZZ6Bz9#bzV$(5MI?W9l^w9HV3JmWEGLonk@s=q=!TRYzfrn*$II$>jg6N5gOaX7zj%BpLuD)wR`FX!Xg|;U!h1IZ)~85j}$+VF;|1V;>(@0pr51xhBYUba%~@w1Kk*v;%h(?3h>t9TcKK;Jbn;`Ul{w2lhX@ML%3W@OcNmWgrZjz$0|g6O~;Mcb18#5G<Ier<elKFz~q4BUlH0H4!!(J55{amUzxjNcx+Ni3M4eo4VUIYIn@Ug(KuQj=fZ6_IB|$cO0ceLRzg*3vs^{!7&U^8nt=x6`9<R$s*6yI|I3F1o!+iJxoL(>e?jw6i<ALRbt#>D05C@R{6@{1#a(cq;OF8(BFg@m*->Q&B7sQOhjGejz|aNOG$t6y7ArEzN5=vlu50-k9*gIREv00Nt;iyXha6DZV)HnNV&e8yH=F@hP6FXbZwrLH-OBr95oa>VkABvu&3tLrHxZsx8KJqg3zS%$i|tpY8svE)RpWMvc{^5^AP0rRRIMgwk1cx?mYSW8PR9V8lU9oZp_@f8HSa0gP?3xk$0X7NhqrBk8^E32)lIHgTm-_tvB5>EP475Voq#P)W<p-SQ@C3eQ;U%ES_`u|Zw@?4zf*#_H-bwv#<Z5n_%$FMELtFO7OM6kwb;F6%c%+RGD<kH8aKGbr@ZKH^kaXvDA*fF^{~wcO@v{3rZx-%Ld^;=&SB3{Uo@;2u2e{7Q|}@(si0&omARgh%Q}iLbeY7-rs5}+pvH@al&FIaf1f~9w`lC&yoQE_=rHOuR`teR{czY#Lo2fd=fx*bYty{0C_tHcA0=zPX)*|06IU@DytJC&ml+icHb^jVgBk~9GR0|dRKNOMyI%+#-Y2CBYGLH=rcL5+3H1{lA4GKDC#Bi14|~>7yia@`m>jz>ve1tc^n#0Ii(HEI_FfQZmCz@@&h$TnO+?;$S2d0(3T^QX?8>+MlT+{qj?&$R)XK?eP-6m~QMt9;6!?%FrI}cFqC`Oyu5qBK6yjqd0;6K0wSI2mWPzfuMINW-yh{w>War39oR7F4lKg_pKs#sC<dbRp=)=ZgDfmKhtcI&)i8t{Onnp6SbL!o%?|*ssbw~evJpMK*;bf{xrH-_3<Q(nylbKOm=`0M}hEDK9ae`S4Yd94v#-DEho2@BFS~XQP7S!<9IV+4^UON&6Z1BU));(|bz>x9hgRorDn#)7(1twOQ1`H@kg1XL3(jMa|zk2SXzAVC1W_;3If{b;qDil-^qc)x<tAsH*a>uA{4;rT{a~@Ra-oH>H^VsQ$9C+!`UUELCG6`U9c&@W!9CF_8FevVv4L6_RI<s7z?@Y>v<R3%`OW%HlmO`eXk)jZt!;v9{G#~{f(l|>^r4vs<q_Fl_IdpWZAXsc`Y#ju#ff;mr|Gk|;Ib+fKrC^GjdAydi;=u6Yl*G}YSFj%$A63#Nst+fpsZ9TyN}d`C+cr&HU!7wP$)ty$GC|_$FVH^%bGGH-g0tM$KeySXH?+q@<?{M51u?WbjJPd`^jv0#J?z1$t6G#FaJc{N&-WjG`p4&O@$pZhS0kQlIbp`7v^Nhg9!AB{M>K!B0#9jCnM#&s@r2_&F#Y(hvPgVPU?2|acK!t#m#7O4>`Ula%&RU>5+4$Dz~tQm#<S`A+_T$>8IVrMAzwUdAaNr3UZ`y&x8h>*>akAryd#_<u+|X&V$vuX#IUky;_Zy)+xfOePUU{WU9y8KXe7azAnFK*%4Li|_6g`L;rz+((Ul-Ek{tu@C@L+g%|Vs|i#oOQMVF~t&hoA%aK+BYXCXfwL5UnVr2bPORvH!CXU2Ib#*d<y)**BK@i7cMYUu#Hlj-=9(yf#ukxjJm;|gdu)w1ma5<YH1SBKFKP&1ODmU{%ZarQF<CWh9SDHcsDLvm&s%S^^Fs_)06NkW9Ak22b_bA-|W!aafm+rlyr6(j|{2a2@8NG(^n^_DI5n6TU!9OuK5*gvyID|BI`{no2&qNCYpSQp$gmX%#K0`UwHg=9n@PA~0%pcV;<9+>>baU`ILAQVEAO^I2%7r~PL)|8$M`nE&}m4>CRsZuU`((#Ic;<R+psEk**P!yo9{bSdZI%2mIltLv0`3r0~y>C?VzW=t8*EyFnv&m%~2+Qru)|Ilg9*DmhJD4)P)zm*>Y2gHggxSibLIq4mq;J5q)#^yRU{>kZ<St)Qv(oLiI8zmk2Z3UO1#L&ceV5U(e28QXZj4S4ss$V)Kg_=+fl5IjjW{q8F_n2U%z(pRyz?awfg~wh|5&5ykA|TiU~~9jM8yA?J&UO^;;F1dQ3z@JHr@HWil-|#){aXBbcCEy--glV;K*Bzs)f;mxfG8?Kf)9kjC}gH!>c3&?{(T0nk{pqbXiqV4>n`Q&t}SK#Vg9zD9vWr92}#D@_ufzTY2S<bAPn*6c^nxg~bqUJ~mUc<mqgNqQD5_3gik*eW^4+++)uu8s9x#V(V@3yWv@Ewq#GKXuuTr;@Z-*^*#+(S$m4rz22G-(9?a(qOaMxM|>$oJ32AdQ3Z}0^mUNu04;c+0!MGQhLt$opPV_)Ln=xO_s>;sah_l-)H6(uwS|IO#&}sQm-AUH`M`O1?DyTz9Zd>XS%RTJk*nemI*ONpMd?sRT8rN>NE5QI;V2gu#iWQ*VTT>TO7W^fZ8?<Hd#;>80tPFNrK3tfzlsm!&On5i9DTk)xxWrU^2MC_<e{7bJvVM8vTi?x1C%=%%a_Yv>oy#y6$;r`Q4&<56xGt8w)|j=nxe|BYMVkqFRu-XiY$+wy2IsPH-_1_EL%b9n|GDppkZFoOwq%epU(NE)JZgYx*Pmg4H7s6QSy<R(}A4{gg6{fQW_cr+#>XdwMNiU4xoJ6MRP!bh-i&cJDXqSGCuGApGcpT-(Jot50v_#xyZ|)F7a)p$^a}x%qSy1knnb~Qs|CJJNqgroZ*Rxpl|2<WNdBv1gD&`rlbmkWBGS@LN~o+K`TwvGe`lHPNVGXkE3<TCWRO=m;@_#?Zp(OP-R3bNa;o^&K(_X1l<B4yBG_O&3rziJcHuFM=4&UxhsMqLeU^p{d*}1<w+;g%9vvAy3B@1b~!QQ#xL4xq0<MCPxwrm?Jatp^{VZrFZAlD7HSCn7jHfLc2pe8mq1U9+G7J26c-9KPNJ+v+VWj(&n=A<y3LoCEZq8Uvp0~zH#uOKc=JX_%3tvSbQpv5`Yam~(e1y`XeBZ=x&W7c5hnH89oXNE%u50fcbgi>he#(smL`z;$&W9mkshDsuxc7^oPJ%eqcO1`-)#%Y)tq<1ms#z)NhVJ#%LS)nE(3!jP<H|ywIp6?CThgz(UK|i(*v5KN)|tp84ZDFmNauTK<qm@en+^n+0#PZW3p8(aewPlSn1`O4Y?|t0cP1T{MrtdBv=<Dn9!_Ytk@BBOg0>UhX7w3O5kIF2+AZ39aKSU8?gxko1C~T`AD5N2LosD=LnqQ#?C`;>Zo&m2@?=Wx6YJ&i@dOv{t<n(kxyg~ccYK&DvZMtzb1@%W*F@h&Cx!4&B-ee`<FszryR(1%V3iY6aL_VoyS<2OI00Iq7;5ybR>B7vZ-)8oHmtFd0M>mA5*faLr2@_!;}q?dDf-OhSGLtB{?AdJTHtb`L+etDp3g&?!X1N0N?7ie;3kxKxGy5A5ogps4B-17c`1fA{Zvm3BEf#c}fLRCRM=JOh8YPx3z3PX`zjIX3jDaU)9Izmn>@2GqriJ9smqtTO#Rfj<nzjnN?K7wKIZZdDPEIKvNUs`CdkfY_i;eT8v02J@gLggwh<#rW4onc#e72*AZSWE=abq&GvjkjrP+X)?%k5Zs@5YUte7>hM4kBY6D9Zx={UM+S^T9YeBY*mK!?@Pjg6FYD?2s&|cvb9_7cgzvs^dtQ>+@KBQ7sm`akKI~IUixqa(vqWB7|fCRgyd`p8{{|(hzdA|SG5o`S}qNv1~z>!3~jqoWulc?^g7qfQdP&q<6ric1h78w1udY$W(+xx1VYbpwUGg;2>C$hQ7H2yjwo7~mJtf7ocX&PmPZ>OY5=Hz<_X%^?^d+KPWG4aqcAJ@yI<s83McvEdm)^1~K4BuWdldeWrC)KZtfm(1uL^DpMOAhUcXto%ZJ)+2MbVS-L%hDHR|4+A{&~m$?B07B+UJr+31d(#MPg-m%ks9|kaw(zIN!MU0Eh@P!49un_DSVSversKx)4!y`SN!jIEa-+&ML-rW+6X7q?xU^}ML5_ph65x}I51{r&+7b^e^$#)f(?!7kn8qwW^;!s9Kza-jU9a!8mep2$L;u*H52w2*EU+o4Zw^PX4U3C4oH9E5#3Ob2+tT+;KoK9!C?UUa6@$*KPLE1^b6o-02+zL79=z9FmAd?ADT5`AfI?e;AbW9A^SyQrx@d6Iv=g0M{m_bQS5|Ot7y2w#0@%HW}A}FU@Y(Ex*iFvo1550A3V}0|2DjSa~oJvPW{pALYK~-d9~h7d(j3ZF!lAviS4BVmPq;6CuzX|I)IAA(lXvZ?RtIA$-<#yto_As5gdooUA(+}*^YvUTO>58mmT+`;FkF1Ro1k?i~s4N6A_cR+ZwBub`OJZy>6}_UtWGIvH^;xc#IY9TQW(rAOzLYw(IzN><3E6X+*tuYshOLOhL}ZVN_X6@qNNvI;Ib1I%tRbN8WJOXHjPTvq`x|bWyRV7-~f!j;B6*ja5A8$dCP&HO8i|wZ;}A6<73^^A}0vcBt$k>KtRTq@g1dddE(GR_{%M$B3IpuEEFyrFHI>I*2p$xP52^i*w~V(o$oi@9rF1_){KmuHo0fQ_}U2t$)uf!!&gp6(z~LV#&QzwNU7tXEv)EnDCIj)3`J(H^tlWM^wF?8Q0TNE!rVg-Mu3CDoR!ArlhJ4nov`JD{(c&o#0t!*``6J&|Y^{y-T&r;s}`nFD=o*YWdj8>G}zpBW8UytH|~-4HMBmWBZ<^?JTaaXlqHq;zo`lINqtrdq{eg`_~#c{sGK@qA8yh76GEw7Ep{%Bl8S#_e8!$NMtL3X-a{JEFHk^X|~s=z)80&(_-)x20J$DA^+LKci;nIt^(tHaPX!=V*x%XGq(95><MI$Vl{q4Qb&oP3MXQYT5Jofg}g#d;Dl}4yT$VpVcJ*tX_qgo*2WrvCMtw5|FEr1N9*eN%0K`S^d+IKwCX&=Qd3fFoC{rFPi9ix)y8)g5RUEecTG*CO}`64Wm<%+&2k$02)!21Fs1Zj4Uxep{l9=gWu)N>iG9=VRie>8iKR}`KYES+l7d4n>ozfb;!7)z375rPeHjL>SDRU{p^;9lSCgsys)XkjaJ$)GXEo+loM<&#236z79ybkTQs7NzDc0+Rh7c1{C#Tk}<kiKNw_TGvb&Wo!j{i~KfMwW3)fW+3+WA=M)#Rpj00kHopVI(K<Ug#Oa&Es}rpfrUP7g|&=Zy!A;0p92qQX!bz6ex##t)Q+2FVMWgLU<auLN`BaD~HI7d%zw>ZG#ZMu80vOx3j;Ex1&Iql=}I2%`5o8B2iHby)c+Z6dB<DwK)Bd6R$|@1^amUlcP*{MK7-hqOlfzOAI|$Ks6nfz}F{>4K`Q43m5-)OaTNUB(5CBF|Q-r4YvAtWMSkNDN0-ii>pD_1MN_!J*5;!(}4Do9>I5TFU;@I!h61r;xowsKojzWSnhZosM$*)eh+>Rr6>BDI6Jfqt0ycUDqsNx$*-$(v_B_8H?ZlF1f~C*VX5>YJ=$Xu)2fFO+3~-YLn)>#kPO!bnoLx^2mBJPaFehN=3nz+)wsE&4`%?acV+E6MI{r<iH9YV6Q>IcKLXAZ!#Vx$}N%u5H3#<(s!U0fu@IB|Lrg9YoQ=7!El3`y+>Sh^Sa_bS(!|PBCY}*wy`9V)U_zki&TgG3T^V{ntaIi0+jGj?R`_KS$wHVNSPn@tqhGUHn>>R(jOY-?H8g*99Wg+CJRvZr>bgyrT{Wdv-FlHdZAVpZ@46t@<=K`7?&nS3sUvx^3Guk6={T~n)ZC}+-}8Iny5QTdIf;<bd5YWKP{QlB(yWmD>VQk<V&_)3OOZ-c|oIjSc+<|aC6)qgPylARsAPZc5wqK@_7sVvIF@tH62s#Pps%?X6}U)p4I=T)ZOyr*17oZ=D9co4EBW%VZlL#WJ*IIZbQ@agMKhi#ST9HRz#t~$Ew2d^33Zap6<RAI8;v&XhQB?e5Y{VLjWYoRcIRNPMj(gdFxs<;1>e~sWE%BP4$5`P5avEbJrBRtw#{1N&FE=R0|dY2qjR^hVC9r^OmUp&MfR@Yb&oYvE6_kfTWmGyc|Uv0w0j<A}m<2><>7z@ABYA9YTYG#@AH6v<b8as)4b{_d?6;q<~G8yI_Y^CDT-EnQ1^$k}ADOn^|XJX;0>Hx)#*>hHYP{L(XB|HrKOK6P+RBZcYG}4A`c9igvP&$b@ktOGZO2wttr@6U9`GXadkCIN#;m&&Me5foX&hML@%<1HN~aQ`b^lxGS;fSmDNL>PuUkNk)>84RBtYc-54YGNNc|tk9aC-W_Azfw8g~tz38=k5N@ep|=M;$~v}Z7M@Y3iB}vlFc`9Jfgx|gn){o>AS80M+iiKiM41bQo7}Yb{VCJOo6#0>yEXse(FoJWp$QBxgInS%8h2n4{spj~$gdZQ+Cp_Vmg-V`K0XUMC|exuj;55)8&k;2=%jMaD=vHyuBWLmBX^OwYb`GN<cn#p;>ujrw7W?hu2d;l`-M}2u0^>m-?>6(L>UolyMSbH1c-82Oqr|>hX_Qc7p%x>nf6u0aB?&4l<#_8aF(~;&RWC_l<=`G&{ciJUJ}FJD*jqq$8E8?R3U^<<gc?^EW@F1(bdlw7UcY82OwR+Nvc-0D@|}5cllCAdFF+(0_IH!uyw4IJMs8*3%%N@!8~n*7Gji?{oA+eL+9<n5&;dCsk$;h6}E>u-NICIj)w?D;)3e(=(rc-seJ@0R*n5l+hwbvO1C9JLUt*o&l76x8+x{5$I5f@9;c`@g{k;gQh?vntp5s8?EflF6O6ST+bBYp36XhE^y||W5@0Ofc0sfVBSKqD6O4N_GA6ao_YB2Q{IPj_%Xq-!^pt=N%<R+Z=x;Q_Q8mnJVBf_=e58X=yYEWH8KyFKJ!FkZj}TTCpijRRAv%pF)-X+msJTIA^fK2$uuQ>OsMDR6ywy5xRfV>nN<aiOL|mr&6FSCxg*4QgOQoX*2MwNcaxc=A<Ya?wnG+Q7pp$_ant)^TSOzIdVJ@5-e0Hc+UZKUSkTIn?%IvKqv9PB1IwSmWt!1XhMGnw4&*@W+5M^|m*o0qW(DXI+m^R7Dv02NN(j|!bu=!N;Ha7bQflNTNt*QseFB8G(GaqP$5A$Mp7c|G)!e{rSc%nE2#o|GG1CviL@FWoKbC367ISG!t&{AW;Yx}-0bQu-t$f5u{(xNnw1pc`tBv%!KC^9eDqNwW0y(JCze-)sj(?Eits}#y$C$b_<YzogC<#SHN<vlokPg(8cIcw;JQi5P2m$?VM653#xVVbI~ukmE!3C+oF_4J_N6T>fn6kt_G#)PG5BTh#<d>-nlJ}FD;e{?a}4zoP$#?K<vMAnj4n}amD*BCEKnDvu&B#(Vw235*u#n}YPEYz#06k~~B&j}|PjfYeZdpntz?J4VxR=6A58k@pO=LXVLiWxi!hYt%}!{O71IUi8VOb!cm8sJa$Vx?#$$`GFvm{?UETvXoq8sO=5ZlJKHh&{!v46zUtRxU{b@MZXE^urpy3;EcrZm~+&zVkqLAq8B1=c%vy#o!}0d}I+<&kk!U==FYprmNUWIqczk=CBK$1V52wm3d3oaL@4z%=`xl@22zoZUx>d*$1(O2mx2}8EdpLon=47dgE3aPz2oQfSPD-Q-UJtk*-#7q@euZKnEGIdBvM46m|1EShE5VA5ZaEJYeY;tx~GO>mzO-uKPWxWz=EDaDsp@W>hRJR!f<jCP4Fexsb>EODU1krUEed!lQ`#HI#%JGt0$E#KshOhxnrF?MWI!Rv0UIYl}>})wTtg47Ain<qcb%aO!Adbuwki3ZyW6IvRVwu#?!Nk*F@^!M-fee52MN#HsMQla!rfM`mUEzT>E2&ma>|yrbfW-99W*47J5^S7hvgvBm;!+%nobeweO@Foq{QP;^d)8y0GTy0lXhi+K7}=<5g1w{i9vRdz7F8~jJwd}>G)Kqo)UCW${vOxbUVMQm=4MKBv!m{A`pU_|~G+N}T)kcgU=bEINFq|}fx4~cLit@#r78$JVtk+K$9`8=$wT`_j20}PX=G;xn^w;mYl>$8^%U3u<q8|~2xTW~35^H9Y5Io%MgLtIsX_<$+kuzGdZ)pwOb$}wvsu-IU}(Q3Lc$Oo`;eF-*{QdwwEX6uG_@-5Gl8mdAzBQMIziXC7h`mQan!a<foU21$SC>6<?a#YMsOF6i5nk7e^7?8#qwEzw0IqR?#r%Z-!A@V|A-9{R!VO6P9v!wb$uM;YM6t_4cow^+8g07_1#grYO>gvtmowd#z06}}}SLn0p!<z^M`q+2I^-h&PE%tfbe;I%KuIupOcHA7z<B}P@^Cqs^J2Fk?3)Dwa@2?QjJiAcS3C%|1*1LQV1pzJYow|!k4OvA)cXwm#3UG#fxb(izQT;r(et7z{Ce)$3`fsGi$k_(GsXiwj+zRA)90GWXBz30ZlExjS)K&D-ddf1)1ZtdsN!%ZWFN3dmSOHfm3J9eR<*GwtWzZtj;y8)J`OoPTO{;32RhoQZ7Ay8!e91Oq`o>bHp|DIxJAUn5SJ_Wl^1ulGz2)N5HO*FFT7f<t>l(HU+|RW+n4$+b_EKxs6_zxnAZJh>ujQ9c$MN<t+6-Z>-K5xvpY!a1;;IIQKWgAuLLC?GQo8g#dkaHgppf0r9yHd=gbK!fw;|}`6m1WrsjyC4=xh1LO&QTiXFLGP%U?AEAy&U;l0=HO3UONAb+ui#<#AY`k@k?m<o8gxaX>#Voq(?orc+y2Ac0rls=}~z)1F_+aP$&32456pD7KvAdgecs%A3zg^!h2eeQS@ZEqk*d<*E#(7`_y5GyYuZdVn^jUYkc7W0>vJE$vsDfe(iW)I2<l5ltqz8p2^bD(@+eVD*w>o0;@)m~AK+sNkZ##r;ZihZ@LPr&{z1<|40v7l2EVXHCQvx_LoJ9nU7k{VU)}`-bFf1G=Vl5|jsrOd-+f^DP^Q4s0H=5^biBWyjtWxGtoTYE61wYmJl!&to}gqcPL1gd{}W(-(AP)kfB5)u5MKft2DK8!j5{MF6_OgYj-aA{c)yUY<<KmeQaZg^qew9*y#eThU$V(DH~T+FJld!SRFY<yzw5a2|R{hD1HZWgB@z-WG(nh(96bQLrO{v?wrM{McfqzSbg>UjE_LPhuug07D4&_O&FhKgp;s1>r8+k`RKM7vEf{VSw}CC?Q^R#ZksUtcA}%;_&VC8m759(@pi@*l`{MQ+<hD8Bj5?`tuE=D%4JxPnn3!VpQ4bP4JE9tg-=<-0S3eG;llLoV;G@$FjEC@YY0kP09!5>)YKPN(~Vp*N&)|TdU@<xv%+meyLKUq5LRbV@?36MZ0<-EA19?h#np6Pp`WMaA6VATEC8{o8^|oSOJDi#t2e}W*VG!387f_wv5Y1#O2L^n#<}o{NG7%39;<K0uzYdIxfS^>_*jd{FW$Ia_2y$G4u5HqofTF3V2-v!hT8S#)?6mYe^Db?B?DiXDnBz;!#nxdHBXirpoGL?N!a_a!mL_G`Mt(?`2hyC#XoM)9Z<^Xv+7R;B9%nY72Z)7rjyfuKzSk=rr-6m^6)~epv%Mb+d<Qk|n~oN%`c)ACp4u`>do3xc3hmr=)u=*kJc*>^3KQ<;kyUC%t&OfZznAaLNhY%B^(9^i*L5$lIP8oR<64oxBvjaMAHwlCL^ZoR@$D#pXGq7@POsu2y^IJ=x%`GUY(<QzN?C59W4n^;9thOi+O(6TU(%0u(5P(!CHapSy27<G)i*Y~=1EB`W9;l0|dmXC&B1_nJJ=v`Pu1$8zd(%^1r!<&4a0S#!vmv`Mu0Xlo6an^ZJiv1Hd(r)=*~x`uL~4Q$_R^?-$TBjH55BFx%^7^aglE$bIKhulpbj<aW)dzLN?(>_h~E1Y-plD<+tt;P8Q*XrB1LM5DSMur#mK{VW7oi*NINfpal0L;VUu3Cd^pw^=u!<gtNU2aX8hg6}XYdV^nzLu~N&p4sgIxoAJ&PyQDm$zzF(7(62RpEHDZ&3>G`nX5jKo`pQLytmPvP>t86n0Am=`MrUGOJH($akcq-Zv1wNy1D8QB)}Qd6s^EL5J!2WPJMpl|-w|$gSm<{1C{Y8MB0#?0Eu7qZYPq8WBT1rnVqy3pxZizj`NvIl)|azCe0{(C5eJn&9UTsjp-DO1N&o(Jxei$;g03kzu3{0<=rwhnCkETKWa*T>EJXEyZ-90k(Nnc5{taaWbJI%3ENpe6|sssb%CP(<xE3>WrR_=f4>fu@--Fn2b_ex<)57SjV_jF7zo-uI|<$W~9m2I`d`$Fs088qAmJJGo)e(i=MoWDUi{#0_o+E4Egp)bthOCGUMoo7qmj`pz8YK7_HoJzN*AyvY@uc)ttlCa@U~eqpYrz7i7$`%gv`gZORsfq*=7MdjTQZ>r$@Ex4mVck2lw7^IL39!@H8p`8F$_@7F;FSX+@-^<zG~CSY(rnf=jH&P~^DTvnM#b50?C^`%PaXr*|o)m-kGA-gJUYseyVWfN0%O=x1&6juEavo>S~Ia6VQ;%MFeSU-RBBT7-q9LI&!tDx5~7p`V+rRBp#Ln=l<Dl7IE=*#KMdS=w9O+6;_f`k~0h(=!N%PFx?(-R1zIlslC&CHjdD_A{Rui$oGgrSpM=e3|<T-s|a7rI-b7z2Atj5*&CRq;ip)zv&g318!U^A@YZ>~RXi+X@Db7L>XZBXk<2aC9QS-J0#HG%boGZ;@Ipk4lHQnWa#l696^Ms)W6}xy={MPnSu-R#C=y$uj-|IhSWC)B-7(O?>)DtUSRvqpYCPqH&%N``4@GfLlqz58)yMk+Js1wsfi4q$_tz=Kb<-?|yy%%e$}J;pgM=H$)XVrtQ6Udr@5*+rx0dBkR!%$`W`(ZUbTE@?^wt%X~(f>qxSjF?;dEhAh&r3t!XN&v(USAtoEZa;cf0G5)em<>-p`Tr}QWch=RSWh=(Ec<uDnpN_=vhkYxi5sOt}1bKQYJ*8lx07xlVj6|qIGo%9(*P}dRS+0HgdzZtVWFmStks>-fE#va!5-0^hM_-(sm3#!Rg;wiU+Sv%q4Q9x3Ip!8|i*0nNiG5uGO+gQkXcm}F{KQ;D6Qyy1t7j4AQcHM-R#*aL^Uv)}qgxGS@V91la&76Hut|9g2oAZfGGdNYpj4Ng;8;s=zDbrWuo6KQY|eO$H>|Tvr|m9rl31>zZMDY>BNg+K`(>~Dn}7QK<u^H2hi=?=^4=EG{DYV0erxfno$E%;WvA^xd^%(+!-U`kOX6h*F|Lii9Zu`Skt~t7>Y}`3FhL+*;pSaUG^D5k0{0tZ9$g02Ps(Ku>9C)1pvgu~Gf2zUm-aR$szviR87|Lt=GfC1GZcc|623by-;2$!^eYLjb%J*nN@5Lu#1w@kBddDbsbG#)5_LJ&7T=@R%DJmF*yGMTCAk7+_xcj~1c_la2%10u!Iw1Oq5SR=5n`2bg2?-#1AGqZNG!*##=w|%9Ril~1-*Bu#wQMas5Z`1#VVQgVzD18#eK$N$Zn*)*9%akJ>^uW<m^{=Dc;~kyKhAUQZd2M=>wAK_PE*ki4O}{ZliXTRh!{mM&<tH_~GT(Wz7vd0Us;#!+^iZg2wBRprNt%Uck;~qh*($jE>@5hSykp(9+|ekLQG|7%ju0!}_-6TmSawX2Mtj>=-!J(6CR8!O!RD<Y?mAd+z%1hW_~?cV0lyWX#|<(Jz2Q+-nlW@3MU;UY_c2f4=|l(?32(A|L-;#?2B#$v85FeW@4iVQ_8Ih{iL8X8qtrh;q)F`0^4n|HIU7jsgNi)gnch6w%O|{FnxTrKMF~;F2uJGDrHT<g@2>mg`=o4v6u`<0IHYu?y-<Y21{$4lOZZtqh*Lblfc1*=qT8p)yKZ*5W^*g15vQeI~x^qe@!#Q@7-$`m9{JFk>!Qvv>ziOk88hNiJ4PXoXi!UpLi{FK_v@Sua|%o}?-w`)@>Qq!c>SFLN6IZMv15LZHF&4u0Thc7#P(jCzKUx=0xwG%y?HC)UbH4aau6ZV)Z)n5G`3t<HwR_$sN!O$X18!?JWmOJ*H*Sjd)$Q>-Cn`K0DgI}GSQqGDBzF;L*i9CeUF!KZbqoffhfLrqETBj^Kv-OI#F*AhG0FNSo`N<2Dli^L#<NoF1cfPqC|l|RiFoQa9}ksTBL<GsQ0`pTGcdF<BTI0z09K|K}KBlrN_Fknj)DlXtHrKKlyJG${@5_}axWvWhi%&C>kE+Xf(2m)IisKv4~oeTBbSa)hkeJ<uZ9rr@2*tjA^3bn-n;(u<oiuESuKUN_|jW=(Bw!WOi)3F|o=|}uX`7>4ZD!`<S#<$=+w?EaUCV)R)@NHn%FC}(8+}Bu9Of%Mv24)1Khx;_(&a${me)swA_^Dg@eyH4}q$(CurgpQUInYq&puJLzEV$;7m+wYMDzk7pjt`V}6qc91yj5B};!VZ0avCHy*1;O?)Fsvp*Kh>H9f;g0gBWKGTd5HgVjzAY)$(bW0~AM<c-qa2q#TI;^mq%jV^JE*1h(e@scH`OE^a!!E5?;e%Z{bokV|_ci{s?@)VijRu-CdQY#$>mRzswE4n60-NUUNfYuZLtdU>i2m^Zq?x9WGCcHXUf!?Mo56Kms!WrEUcWxFFvwUda_zq%2VL{nE4F2hV%E3eW?jG0zR;%OacuKUXJaE!^JvdH}weMXcb!V+wnhMaXP;mA;C@lfuF%3AaoCQ$ovnTQgBLrSw@^}+SB-$3N>bm|1nN%#u+McH-=sj?K7*Z@*yC%Dy32@V24<<OJg85s69-+L^qEhwI_vW5!LJ<Y(bYDi3ovduz^x~?Fjkr+6#Unw{y#>s=Iu65TH6DAwXk{)Xc>VOaekU3Q?s}mnS^y9-Ez>|(pzH<ZJv8;I@lp-KEP<J;BuPJKEC6fa8oi^M?VbzA}A9<;GZ|BA6l*%sYM){o7LMm|<l9hRlD-g43U1k(s*O~{=7nfEDS2JmoY(P@<t&ha=qz6h|_D2d5;%(W6P-%WQgx+sDgJl&vnl^Cyp`YP1hGFCZ@%FvgDRku_S^@+f(@<oQF3k|UeQIKGy%z!Q!UB^NU|WfD1i)}47v@D#EnQ6l;M0#7ABZhh;9~Bib%2h$DSYYFp?nTMY1}YL=_DL=S)OiCYOQ3*Hlrem#5TCMf*T2jG?B5hv(?u(f7J{NGjmH%aonYNdn%72by`6{)zW|iyY5)2kWrU;cUuv<C$ke|QcP(zW1W>sodt47u{-61KHMAy0<h{>Rf)1wfuX`W4C!|CV4TPu9F~$v<s2+r=wu#hm9xsY?#g2MYt5hG$)YH_%m^7Q2FTSm_5HS$W+)nFTsh>DC|gNoHJumC=dM<&COSB|^KfIbcV+(`%Xp!nsn|OJ`ig1+f4sGz+CPaR$+-N;UtO;wdBQtWW%Qp*aG)Y<LE8`hN^RPl`EP2pJY=-0ht%nokT|z1lOwpPilfH5MmvP0WmnnGK1k}MFcc$WiQ5<lvy-+(bQK)spdmu`o@PmDjmJR{S0#Dv8AC1JVyoYnLB=IUNkRSug}1zlYOk&Hb5yj}&8A~Wf^gZ5YgmvJ>kEo*&3L4q=}RHK1s?_&(IPiDX~QecZF~9K221iFTFZHpSCs{<VY3>JYn(>2fXF-Rxw<L^>FfihK+C3(j(r<hfc{MtlU>R;2&%dAZR(B7OPkrs81X&E2n)roBspcw!3()E5fm4^1pj*O@YLfnC-e~jM5lI;==kp~h_>^%H#XKHKo&=*_W;XH$c3zHT9$!Qp=SYXZXy;ggt1N8lqEUcUm)N(23Q&jMttKh2@_3{-g8!6IVWPbKQqu$`3A(4jpoH%;76&P5mcDFQ`ZqrTkFR{R>8NTB~IVlW?xWpd%C%WZQS!1p<=>r13iTcU^o??denu}IU;=si+(Zejji<s701a#96og`mr>)vHbBT^<+c&5Ka>V<N=AST58rKF6HMl;0<IR8`;v5`<h#xyxq|mD^DSS)frLf{@sz%tbzoe6^y8=7Jc*(T8=1-|liKJoFi_mct);?4jV>%19RBqF?*%c{cB@Wj)j=&kHMCmx==U?{PL2w(qF`*#+KP`M#;#86&7`$_nh#%sd1z{O!*o{_fd5sfM`TLaRGqKS@r721af??HYnSej2#P%zc3_J(#~#-apTD1D<6e}@Ovgr3_;|v$uMV8~Q8?~OY1CV9*k|6<%%mI>gfn+yYct?L)yMLeA~uMLHyyUz_Z_yN2M#hA6a0mB+DdSE18hT(V!jDkuF*!%ITr}QKDxehm8j0;Aba3$!D`Vlz&q2hWPsw^Yc8IHFHK@J=esoc>x|ZG)AMR1Uh%WP`0>6EVqqTRa^wZrmZ^MN#~_PvUs!|$Wg`7_cSL)qxAM?tARd}tnUGFZ0)aQzAv!_WwgQnqlU6851eh*%@&M{wFoB7@tLRcdXf$@3F)ngNZS4(}5o*j`G`pkWaaYug&-mO51AqPw7&wgiQR}SJsJzi`2dSf}F9*e2?zpZoMrRAgMRryUz-hodM^P}?^kZs;ocImM9>-MkXYw>Id7SIv0P=~V0nZ@*eKMWQpf)}WMUwF44MtAu>KsKy@K~YI*-jZq0ft=bd~`Y_y9{C-azpL+@RrBhzY|^3#39Zu)$AMAFD6*7p~YsrcA6Ll+ueIdhREs^6MZktUY?HdQ%mcWz2JhnYZU~|@iEd%D_{*$CK%Ro?QU7dx5?lQ3T@vR-)Wci`03~g0xb~xCK7H2%9TbuT0l<%W2uxVn`9qu9tp!>eP2M$1x*BYej7$_8`({`DDrmPNzz8KSr}kGK0J>rd<S-q!C0R)yhV1%bn5b*YR<Z-dRD?5AN-OjKMrQ*6R@d1_NLIZ1m+rCksR0%E2;tV`pLz~W~Sl>s3jfiOi{@1#8QZf3R~BuR)X^x<z38;sW(>Y^<kAWPg$j_ft_vE$m$^H4%34m{n@L?h09kxUn6Qgi!O2v`ZghX{QivcqsOcPJJ6w=C94C8B~b@wF5KalJsiFHw|n~W(_pMl+LO5ENCDq}=!e_1wB(VpPIXNlV?m7PJ#Y_Bzj<XWj`?n|h?FucSdW8b5Buq?u&m~SJkDKLXl^m!RB+sYvGP`7uP~8Nmpc}~M-vyqVLd<2jGiY$*tKCe?`69hGRSh<!)R)I`#uK}K2o0tt~x@?KZZ-_>$E-v+~r~DfzSx-YSlj5l(?+L)cs7F>^<;!^&~JXH*APG#4f8=CpPr}@OuILD!9s;mlseaF@#ghPqY+lJ~~E#W9gr`4J{ht<cn!m;G4T3bu~n;@MSW(OCUd};2N09@H}}dL1o#ha;Nh3lh<TLb*4PSZGQ?|FVk#m{kjXix##Srh#O@4a+<kLr`|-sZ1+LNfg(GUC6AO7&<m`S#9B1CcGgBorry_eu<BK2bB#>29E;Pb)a^!gx-e}UaBNf<cJj=7aH#AUk69smRiVMD(?<p#fK^?I{w)=urKID9vG$I(;&~AW?anf(Z~QAFfmpJw`ln&CF-i8wZCeochI?Mp%F$Re3<JjbnnhFO82ttK?(tKLj1o^cp%O{1P<H-NEWOe`L;1tB6|kv9<UUo+q|HyeI9yeLWDR=IqxEJY3Z2D#)2~I;N3Y^_J>ywd2qt8<Z(S#X;TaDKUV?kaq|iB^=7xe((E-~cpcrzSr4R;6N8{x+s54pV&s8DBkyusmFuBy3<*YdlX;9I6s$3)}13t)46i=C}d{SzS>FQARv>-6SaC$J!ge+KbO#uT`MFVCLE*Yy*{7!DBO~pF^<$MQKa`N2keZigihZh(Y05GL8DQLq1Cog+z!HoIdE~xRZ7#hlDYEhzm-!Do>#RcGa54vv!0<&zT8dXRzlgLY%Sv~Edzp8@4kBEi+Wzx$I8<ctCgap)XtcjJiLm-PjVIH(OCB#xb?OsTzfn+Ll4^63&m6vK#uIol3h=ztHO`r|Q93@ZZ+ty@(3T=W}OPtFSk1+fn_yvHU#cfi{7^F@iHcLSTgCa{I7?SB82iw}}qPc=izf<mly>h4}i!jgpb5U&$QJbwW9v(ww`b$JdUOUa|xuod94yKAo0k74er=<ZNg96u3)Z%g}R0a$@0jGiv3A&x?RTM#oPS2V~2Q<@m6QwpjXFN{?VXC32QrGayDtx%ZFU0odS|>%(a_vsL)&)yAmKhk<@!b}|hIjm+$lGgzQeh>K$bZo)=7;~R3T0B&n1$EA(-vlhHk=8^ej#{7Ml7sE#dvCsKSuiOhZu{zts7^JGolxCoK0M;t<pg2?Jc@cUaDaY)f$R~pg0Igc)-Z+bE~hqJwhzt#sXA1dv&ha#;nWD0#86JM-x;KCa|jzoLgizZ!$g|Qr#|8{WOUXEV!dEZuIIw0R6pSb}oO4B~-46(xcN%D%O*h?*PE6rNpOT0Jb(@9!=Yjbic3FHM&?2&qe}DOK6pnC|<>q;-!e%4|}V!0c&lEI=Led!adr$oM<My=!yZgI0~$m6(dpBic4IOTAj@(w|c@E0yR2dh>}feB_#_=8ISsO!76&@{91MH8gF`%&$RjEcVjU_n5-}wf0P)#`@=rO_8AFReg9GtD|D#_VV+IGWb3d3Z*iM;zcC@5w=;Y*RAq`+ZAQ8|<#inja1o7FbCQa2BzT?q3j-&9^4N@!SaBkHuGI>X(a3n%Ya#X2%8U%=PPw7Px<b`)GXqs&ZfQ2lu~g<@q~+vIaR}S5W~Eb7!i?SG%ml&VOvAdK$ui6uz>%|b+|mbOXH=YQwQ6eAJIfQ2^PCAv(a^1=)~ZOo5+~Po+et<AuC(8@>bg+|OFKH7au0shJ)>=<(k+Zfu;daqs8|SsG#Rc(^8{gt2WR-!-iB#~G^FsKJHQPq=bPHWk^feZPwXsmxMFw8y&>}$ONCb4qLjPRZFM=4qp4%W$-eH&<++;~CT+j5VNzW8yza&Osqzxo8d;h7NaCvELAXN_%d0aUF8^3?C*-;ooUg%dUyI(B`^8yqPH8ypcT)LWYn$$XLF<fvheIq+f6ZJJ5juGL)_tD<VKza~lE<kfDt-T{VCkB7u(7^3W>iurb!>E648ja>jiwdzYG;wx#&MqMP1Prc($lORkbv0u(a%Dl;?NlpE8&R)-2|SzV@ZSX&D^>WSyE~<BWW^&vqrrP@Y@Be4n*69qdrq3EL}zsCn*{Com2r@WO)O35uRMm(c}$`lM?rN*Hs#0DPb2T7l*>#0(uVUqkeq^ojn|C;B8e=hi<m>EEnRFuzvX)B_C=7Je`h91~$mNN=bt9WUS)?!G$GFMq)cTxddu=A+~7r6rp7RvoV8}vW^q%?8zKsu;)*OWlva$CcP5Z$SJ;8LhAYX0Rlht6@9v46G{;n+qEg)VdP0Ky+#-N+PMrS$~~CrY1wfd1^bC$+3tniRj(k5I#~u&SS$rYT!$TFrAj9+`hS>~*3*B;*wK{yC6@Wo5&O=&^4zzVNbH%NY9Log6EjxMjR$6D&xov7X6U6BpLNg6lZyihX*~%%H>?%G+Ya$xf%nJi0FAb%6SQ1Oo0{B)F+#d47@bpkgJ-(oX1~kJYn3`W3mx2dDrI?=iU)N_2As1nRoo`cY^|10U5Q%5&B!wvv(p~G+;p?L(*8zuCEq8B$=+~*iR#arMl%N09dX%n4vTwPpN6etz1;CM15~71x*rD`2v}Y^!kfjePE)l<d?Ds|5}o9gnyY=mhVyG0ksM+aOmO$nl~E`Yc%(~uoe;4DRlcQiRZp_eRcN@Ey4}2&7@Q|bfFX9ElP@0h`Nm*?%hJ%<D+@m$sO394g>uU4u%MrsiK=rB5?CJ<pIX=M%T|1oDk4_#(4IsU1FNm5{#}O2%lGA<2f~(#z!E8*T66)n;S(&r!R9UP&t?T~;JIShC;99tWv{GU?0n$gu}m5eR%o~AoNMt~mhdmsjI-##pyom_z_xT7HYp*@_+u_mc<<C%pnDx_0(6>c$gi1}NY6&r2|@>uP$+{NEAB6~piRHOGiRI!>`l#Ze$+SmO|pvKgBG{IEhEH_h*mP1l2FOy+xZozI8%*m!fRo3ttS=~hJ>t{5Z0OtGd`E$TDigr><wiiWkBMfwsK-YcZ8qV>Fzv64x*pa*H`w%{UaMqLZn$Y5RC-f(~!LMI>zhjoNM5QuaO+_06Q~V9bh53!X^oQjkqLA^qY~SLG8CGPzgGQCs7jLwkm+B5Sl3%<m<W!IYp3tB!XjXwV9&bf&_Zr_k~K0ICJ1qfBRM_(Xn02Dq)t_8Egc~*var>_moVT=ethmL+VyCs;%`LHC^H~IQ)P+`zLwa=K=iwa(1}|-+#E3I(Kf~y03U4#r(}{HE%x&wPIt<<D>*rswmZ3>EC9h<|t?RK&6GDJ5oNY0Kc>m)4wT5$D@`^rtH0yWZ8HaG@NVF4%=R6l~ZwI&SMJ*SCC*T<0L}q7#@LL%h-}lYC0jGydAb(sj>5uaizNRhtyXsoo(J$c=XEzU@|g<s3+M7LkZZ0ktec~!D+Twso(-Wp}df}=jsYHwL(7=UE6>wWU9>c%&Sf&)<RoUnKZ4n$ub2jewv+MZcGW*bnZ5>uZj(z(bohP2`)T}MpYs*$)F}jHkS@@mRK*bIVu86rAl?<?Q;n1cO^T6oO!O!lamy?UHRUYWzzs|Ob_Y81?2a6K4e9O$K?Bt|5uK%%H08eP&VN?;X$89BATb*H!TaXZzf@JPJo}2?{9C;LG*iwOhtM#mjnVr-6Y!Qi?a@AT6tnNCM|HlAG61JV1jh1FJ^t5R?C`a-6Av5<vmg#E!C&zB1<kAjTPJK118M`HGM_jT}%0}ghXk8#!ro>*+%qwIXmd4ewSR>KOPJu#c20eMqFGcaDFf>iiQOkhelqED5AnI&q}D-_fn#n+VxORc4HN#1QwE>Tyk)pM_cwpSB)EHFF7T2acK~S<#QWoxTxlt)5FHR=xtS^x2Nx^$>QTi9pS4nUj2o}){C#GX^H~*nbI!gsn3I5OQ^1IrWMP)w#VEQ;?Ub<YOhtmB$_XWt!bS8x(gmtv4iXPkAMIB8$<3KxSz9~-+q7j>CYcOs^%l`@;qknJZO@j6yula$$7Bws#p(@PK~9``K3AAXwfBi6yp9u@e2~gU)t4SBVLWH#haL!6%2g+mOJJK4?OxQ<OF^Y2!lhGc6jltLEqim{`3oaC;IA)G~?*Y>ru-btqtDfh%Pv5?9RxD_<a^|F@MoJ2v-LQBS-(&BYq<+E-FabGed-`-~SfA?;FCXUHs^>=^I_u%-1nh0EsWeduDzeZwe&jzC&cr)Y)|CDGzQtJHMn=d0Z4vGb;#iM4GzL+mu1oDyPT0kF`Dau9dwzWcVt;g$;;9k(?leK>Xz5fL&DE50s*@#olOu)JTzsZKt1r-Cxx9dh&De{piNAM|Ya*@d!-eJYtI>rAf~2XoB>RR(|XdMknDk1ew@&sqjSn_#lP;+XgZ5g(N}DB1t#2Gw{{3W#7M@u~-2^Ti(1o{Y}_DYRb%fo$uXPXmZ!D1m%=jMzBq1E1j#gBNp~7m)%MDha%ESMOm7{sJ^$1(=1nOjVARpiNpHvYoy-mgOHXcY44-%+G!Rp3|aO2<g#+=+1!r7rlC4&B~*YjUci+*YMrn6J2doR?wFtT*K_sDaq`LGgHFmKhXf(>-;-ma98UBli1s<KczvB;{^#AV?|*ss<=6lI^76-V@>BRmcqj<F)HVtT*JDS;>mc=Ef6t%dzF<Z3_K|nOBQ5$aq0B9RG0mIlZ-2i3@Y6qjd<ov-aXc4qrPts2{QZxA{yz6sSlsbymbZpi(%WCY&LSnWT)q{@IDOJm%?CsqPB+C}7`*W+m+(Q+{Wq?B-je87Q#W*ACN6!{<hE&U$!cMmth|g+F9+3+FQ<7l_xgnQ6)sinXsVe8Eq4-KH{sBNhnWn!K&-4I>etu6Tx=t<8lUCzUjF#`c>HaWaGMthQNk7@=U`|o)rxlMd_%9H*vHzFB3zjMP>Fg4juY26_;OiLU&P*MK!WtTb_`16VzsXM2AL7f)r}qOZzJ`x-lt4k&k>%#gAm_g7Lx8{XFDq^<MFWM1Po}TbF#}s%-bIdXFUQQ;x&3-l3Hr}0T+)nW1OUohPUh|dnC@a@9v5Qyd5e*aancN`OR$JI(!7yo=uBHL_9kqNC+sO0wb3*FsZ`k(Bxe7EzZ%`)p915#q4I91%OKE?Dx0&jj9~GfOb4=irRbU-#&hL`E@~YjD0L6sCuCfQ2-E;*)jveaF}j=A<+jJJXX@H7!~qn(w-$y9&vkjdpVDMD0DRxz%gZj%>`>wl)#^C?3vFe>*R;rKK<FRaK;)TjV=C4=K|aGNVFBeGxuF##;V1+j<;1ZNiINJ^221Y&vL%aY8Jb;YvO2@SBYV5q#o@7^#Jq)uekgGZ4jy$V3|%yM3aO9iNem-K)b?~sgLu=o9pPF%2X=Epy#A2+Oc1rMlfP^zraoaw%=%4VkK!&V#^USit&12Z-Dd5+F+H^re2r_@OU>`p%IJ#krF_#q25IX@NLUc7LJphoR{;z<J||4vqc!GR2q$41y0X77n1sI`}&JeZ<Us?_a(m=shzeFuBn_REZ4>(^B65qc4dnfvHtR<`*BNUC-f|VpQ!F>H6twAgOU^h1Zjox!2p}Ul~O8c2+L)bFhv2ii68J+cGsda@7skQZmX`+<qMJgEN)R^uNe;bm}3xbU!3ENnENGf&Gtfo`KBB)HW5ah5D5CY6(O&=KuWUK`66BB6_f-URuDQLpl;EeU4NN21eF$vD23N*RSAI?^0S7~-t?fKBeDkzeWh`rFCbucvC-;!0F>d?0*W!2IDMjzS(Q7Z5u(G$jVZKGdbF*e2ooiVxnX$*sk~3;l&TP3LU5tcf$kl@amDSXjTup$&}fQP+g5!X8|QX96z6h&HMi%P3j)-2pPs8%{=<liIbeKK5$TdE`{LeZLK(YSUla}5QTsg7$y}D)+zph}r<ipeqX~*z6SgT0v=`mCw>(Es@qlG|LM|0~3?B>vol9xLk^rf|5so1P#U?0_kY~!&N@&tf#QHqAo?(*oFH~&1Qu~ffzViN4t9!(>G(G6c3ZY{r^ZsB*)tRwPGGM}?0imaKqID3x&T|nDYsJ%mKNvhgz*{Cnv?O8!=%WI$nC_YC#Lc@@`bH|eWW)|E6*G@HwhCRMO%`r&>>=-<+X~QCqwAaDn2Wa3W4*Vs5O!uFW>9^?{2TjNitI9i8K<UkQyncUVy7*INZ6=g3n=Mw`y&yDV>y=D`GP^{!Vtb5f-zX_=5j^Ddl%&reiF6(T#F7EuEmrf%9$aBRrz@Ll_XjNYRTC_Y)!o$cOl;9K^-mzpoN_3r45zq@W%n|URI-zEbTfC%AzQ;Ecki~0yUT<G=m#pe`>14CS_N<qf8S&6bix`GT0S$2Uj<_xk|u5%uSd7n8FSKL2{XbLb;(5J(CK^sqQUG;e-(@o5<%6J%c_x3|9T}ThvV!uZB&L=?@x<Bb*8%{ajeexX84Y*!27R;+2spV41wpNLFd}$iKCi`ZP+YPd=+5&C9<^s-n;!e_uJ|8TbD?ko`<{j8v)BiD3cD&oAOby#l|Q_yG0Yz}^~Ld6y?KOv+x`k)WU^USfn8iO#K6z+Xv}2JsipYmrb7z^8lcsJ7sLa@eqj4<?j1shaQ{C)2CCK)QZwCnyeDM2M_1-6vOcslgS5feUMKj;7G}(_D3Y2MgyAh{smAA4tG@SR)Ei^5CdRbGj7-(Y%UDGZf^Dba^lC)aG#_0lh2`LvExBI3D3SCFhTUg;{N6i7Yv{=U@@|tqzY9LHa>KA=$(fM?Sec5gFG}$I3!Ko^5`iOB2+$S)YB1s{>DB{-o92S*l(_Z(6(9n-{fu&Ed2ef)>`%LqEyhc9u0QFiyQp{N2R>8c48>#KP6OyDB{Vl=kKsJh@g{OeaDW$PDlv{$fTdt!_S1w&u=LU<EM=XH$+aa72t{LiXsDr$+ie=L`RWwn!!z=|y+<>JF#^MC&MHJ9oMy0Q@9%CTz{d^&LZ_WbwCYjT8QCpw0&F1CX?OKG4+LR>fB^-d4>7SzN&AQ>4TypXzZ9Ha@_v@#|s&H<HEKXA{S(r^g~>=NK{lA*b)-4X6h3X>~twPQc^EaKFRUHy%s<K+zA_R?JMZIUH}5o>!w{yGyZD8grUJa%6ZQ_+3EC!L$W($4e|~yV<MI=jy3AntJEYB`bMq^hoNH<S*2>P30W$9eB~BmHJ(D{&_OFUNR3lTJ~e|;N9p*Pm%(d_#(i<wTfAdtVtVuWc<8{yMeMr?FCEtFLfNUEzn~uXy!GEB^yayY;QK(QGjauC5h6yHYTf<GI|p7sqoHX<+M8(9`-AwCi4Pqx#YanDh<}J?2-$w*nc;DnkPejZoKmwAymg)n+WnpjR-m;i_l?Xvo*1ISv@w2KiWwq?=YS(cfT=5iPu${zB#qGqR-2<#^|$(J_U6Gt7o)3DvGSO?WYn7h;HDx0M9=q<1`Q7h^SWw0wj`K#EVqDuK25(uPhsNwgZdqI_H<3A;KqwPy_9s>a?_H)VYFvwP?)4jfSUMUxTUICocM;Nig@-j5ff;caS$RBp33)k;g!F0f&=v1_vaOQA-|<E@Ep(N)e>ZzPS|Oqoxp$=@^_vN|bC$9m@+n>lio`?wV#Puc~Q%-T>$S;&no+8A41l;<!9BgEmo8($G%YP;CvxqfE4COiWb4mbEq=x<Y*5RdiNvGq+^LrDY~1MZt;!ih0ns5R4F(RVX78b-hV>YfmQIk;#SU&w3~sGD2e*NskwvwKD94OXyI9G-4$ll_M66JvB0Tye$b>Riq0+S$Nrqju1Vu%stIxq__#N&rEPFrFlEClWVa1H+G{e$#{^ON4~IR4Bp22G!mDpELF3w2<KV_R~~)VVR~>a)k2^&=rguPh*TRwM)<S6XCYXYtX{e4pGzf7s&`a4n&NTIj@5SRngHEL1Ek}*ki`>T`p1lA=59ZpW@JVlRMUnR7AJw_Zdy;d_^}JETuyOQ`$baQ9j15sEFxu^TZBDH@*``B%Ee7f^;AbhDW~I~b3X#u;ce&L9ds8bMAkZ*q_n>>N4&5Y?wShtVmD*>&(!+?OGtu<y@#tes}dKO%V8iW5qvo;f0Z4{E<Px>IK31jdZ=rz=bx+r^2y6^_P>f$5cuJsDghsyykqdK6;22ri0TT5QYGVN+i~Io$K^aAh~mkc2N@>Ua4eJXcdHA>LXR=Dr=^0~{8vq`m&Nx<wZI`ROH0|bsBHp3OkE4Vvc2ZQGBab4#!1RAk!D$pEZ_T*NuAj7T=XzSdoO=M0uK`QIJ0|o!N2TFo&ii&1I68(+1x^veUG^;q0!ylIizw`<IFiwk0c_;wQu*#!lkpRRW2pdjGI>#0AJm-FE#?bHe!*d`DCH?ISD>|BOkmG{jj>53OLegB5#CEBlRIul}WN;n4HvTFuz{}^WFK5Sm;DqaUPh9e#9Y^K}#KF8Njymwu;zgNUf(kNFq-t4JZ~V9wW`;;l9>xASw?^43YNe+2G}!v_B@7X5^i)Bzgfy8OioCs90s+QDQpHq1mw!w<I6D*ldB0$oqY0E~>=_T;=e5r%fUyCwH!c$e4aY{X)S#B}=6qB8&tdt0xlGAipINEb8PSkVlx15yrc){MLtxCUYujSLBTMU?A^X(oXTO3mXZdjm)p4wA*T(4GA44^co0F<Q&u5)ui4wj%Mv)6(B3S38*|QrPl<B+gNNASe7ZA!*HR8o=fMUXM|xlJvl1H*dQ=x4SCoEk!q3>Kq^QEPk`{6CaMB-ylGmM*S|HL#X(UNI0xd42=pYZD4U_ufa8pn&23C==eK5^-Rf4oCPQ}~c0`HSzCCU#;lOEKC%>n`L%q-$K~Ns3thCIkxcm|)`O4g(N`e3bh4tNtwkR~rO_XX&h$)4$;;-5bT<^FMwi8L{f`DS~tb^a3MR@YlPQ}3Vy=g7AyU|GpV1S3of^rg0r|g9lOLnzNfuO?CRvMbKipTMH?H!RcD8@z#4p6;%Rhc?3w_}bbbc$tnq~vC&C{=w=sQ8IzR@94y3)@wvn;9H<W?&x7<<joG>5ZeVxWM@T4vI5f4m$`%*(u2=c~0dEoLUpe+2<5*qE66g%TxU;UBQrao>EUAuh_9PEOGyeQha0~U9)!I4iU5%av@w1+cWdW%9V;Eq2q^_U(XhKX$9=-YJ1GCx9ymPM1Reex@OF7J?{n&Cy4$NhZW#MK9k7v((UR!)y4R@G%wseyQdL35U<aHw<MSyyukP%jy-7oV(I-vlAcQ~INxC+W(hy~RA#kgz32{9l!u^}4vV>j{LUff7RDI3EyQT|G(PzNe93;2igny}{@wixI+m4xhSo8!DEd^E&?$%3NTUaMVHLAo5SW7VgJkcQ&(AwUYqdPJLWRt%<MCB$>W|&?YU>nSPh&NK5K!d6K$QZ675S$!&D515l1hbd&B%muy@X0f+!IK52p(St$0?jy0Wx=Xk0Hv|dmNrL5djAcZvu{|2DLG+Tn-0|B<G<$apY!=s&OO4aaT==&E%BUm(3~dxn6g@hzrbWHK(BQ#y_o|Zk|3d;dN6TIde6=Qw>V;@$Zx5`^)zg`J&ndVKvRtn)qvDNKPf$>Q2sxJzu&_PE?#6DWhd9fyxNCl>(Pz;#(4R&CuC!UhEy^fkOSw%2uK6QmO=)j?};Fl$r0Tq?*;g@b=H;-Noeo0K&mMxI1%9X&C&DvoWNGWapV<f7cZYVR0Fy)e=P3*lv%dy0=~97*g6yhn5JcGw6dhgOz%fN$@+pt{!iX57&Q*dNtpbE^I~m{KC>~dIMeik-v@AGwDA{rPdPup%RmS_8!w$s7rc!NDDG~NXx%it6;>#<+0FC9C0cj>VMRp7+!nI<0`&I6e`YHO%n(j94eLj`{}vZ#^%Vp)(woa(g0OEd)7OYxtanDe2VoaE{4gI^CEU;khA?%@av9fMadzBMv0Otwk@onxDkBiG29~@vxzh_8(lHtYE@RkU{R&<?wY%nTd9}hKTm+S0W>`g<UF;;7^l0^Hah{}h0<OD7e7d4oL^mhGdnv?Y1=o!<4m^YsS#J)SG>dFIYePZ8(x-7xfo#VM!-doqf%o?NoU0B+Y)JfG~78nvYd!bw3&O=p+b^w4yKkCb4Dk`L~!I;V!rWj3i_Zv(~Vuk;fX<SNw7kUEA^h~1TBx8;$FiB#g@l5xbd!HJ(;J3*<`;<GhW{#hd~aWpE>;t6(7*)quqnjP=zbNi*cr##mSTSUURF(Hzmxm1!Q&cXCaH#$Z+nNr2H8eC`-fbRmvV~JOM?}^_{(jx<dVZ4_bs-8}VG<Yw^eK9Y1+=i8*v<x)O5H2_qzl5wa~)<n?s%+uVpueEYZ1G?=psO(5b#d`zaW>_i*)kn6=1sC*LYCBe4S<ScB)byq44rgLGZ+pb7OZ_5;<z)Lmz%WC;QV+@~2>uDxL1ZJFocO$O=ja-DPj9Nll%<>k*+H9M*EZEwo+*<rZvav#f4`RYEr<ZLpK))gwp0$2wquTVB0yk-o41#**Ek#M<8W4^xn=HY0EKF^y(~XG#b3>peL}Ingu&%}|11-C}Qk-b>sqp@2Qc3h$sqkT`JL$2i%Ew!j3Tm#ha_!WVoJKvBkD$a0+1=SDMW)H>rY4qmqTQk?<-4jp>($&VyVC^D8*M}!9&}cJO`@?!#G+)K{9BD$!DESWMzJ4ocgqbMk=`{C2T~+!dEg|nHjDzq^SB(AY|(ES%*C*X3u=dSg30Kw=z+$UUDB1|cwkgnMS3oCzCzZpY1TW<8#;Em;C2OF!Fbw~XnI-FrG&MRBxwv78~ycnrpt3g#qaxS4GPm>tJAN@$Cqq|$(}cjn?hAI6<pd|iFE$@V(+zxVJzDS%{}eUu(araB}LL(6I^dI=i%V!F*_rtsgA?!i+5bSm+S^?>Ss}JD|s?x?`*{=+fL|+S@HB}G)kQ%L3zDT^2~D1i`wca!sj`;MobKn#SgrI;s&C)ok=K`gds*ktGLbShPtO6IK!Ii&1QruT4D`{=-lT^BCrv}@+c*S;T_{)Bb7j-^|w^4ugQl=BV=0NgBK9A$*U8Xbiw2)tl52Xc^z1Vv`v)0cXfGBw9^GbO2Q}-pIklrnK(M$B5U^_mo(a%V8+w7l``ktV;w;<7{g1Jw@uMkBcUOKgei_U?e^8TEzv+&S&8lnE)V5YowjM1+v2g{UQ19dItcx_v?Iu8=NxJ!atm2i)T*NHinFnIp9<$xK~s?^^?-duO<0N%Rkr5tjWu@xxT??*Cj(kK$RQ2vnU(?!B`fDM39FQsM`*Ey!s)Ied|@hcTl?L8DR{S7a!<Z(VnZ1!?`|L|-`;Tfy*%Na_rh#>V%inZYLBd7v5tOTEHF7HqnUgojN`XMJUxyXMIPdgsU^ONb&g0;NX#$qMYPpCD%#~TVtO|C+%dE6QMcKJN8|w2i?_D#^L@7$37k2iA{md}#5Ml5uZ_cfWRyarvA_^(ycUYN85neq3s9)jq?=?dk`Gj6JeK*cM@=}4+$QM~kAYKcBo)tX9Xt89!1%GAdfH@^>JpDyiimTI@h=IQyhiW21nIW$6e$DG2lh{6(nSxogR=(}pUAJ9SA&0z0ox^!Uq*(HH_-!}1bMB3x9=9^bINmEDn%4NyD=tA_g#K<l6qTVnop*Ac;;?EC{Hx|mF75?$4|Rj8z!hGkzP8aSfuHyml)YW%xo*J0|+r{2bK&Th^Iqo@A>>W4iS|(9Ge{a+*c_Yyf9fwNAUJX=aS_Jy-2+GEk!p1Xi8JpDIE-BJ*HZMXv_2|T%x(-+Pi^=ivXiz!%)hxtEUA>kMzj&GfWFL6VnAzB}{S+r=0U?W~aj-4Dl3NG8}j7gIT-MTZ0(x(GWW+fLLB*`nHr7<m%eah>+(nUK1-=@WyN<wMwfhy7h>HChQ<}6amf<6{9Gi4JpvxPT9|6t?N^;+&pvr&FLO?qo!>L%i8;ht{>P$`oS93&`wW7#q`AxHN~%6-JB+fGYe}&i}tXlak=+hHGjEHQ@aGG5i|h`sz)tDF+V-i>3bvUBX|xYB2bQ|iI!|CJ-YF5H#QI$cme;<e5|uISuyyr1Qjno1S-eS<htN!9pYOa^b|{6C-=o*uY&?FIP0(QusWj`qyW~iFg%NTmXUbTpx}S8_cpzeEIGE|e|hUzgwgzSSzRS`7f@BV(bWYl9xi(I)&mS?R`chFhpq@kxY0<OMJO|r*MaU^O36cVcbbv3L-L%+9tt-N1#I9vc(CI*a?XgQN!R<;GR<<6U9M`NTL`JF7tA`bBgDCZdDiMKa%>q#De5Z2?M)Y9u_XJrU^a|7@W~_aR!pg}-702lbzOqBYs)Ck;Pc&GnTw3+JT=&QP*uYTyn@cT+oZIOvDojdrGq=~ZDWl7h+_|im4kg*dY)0QMVH6nAU#*-R-%Sup9hN?+{4kvMi<WPYEd?Y>$L)28?T1fquJUYTb|c$7vmW1%d!=a%Xr&BUu93*hgF1YYLJFEZ=q1}yW}IIGkbI)n2MS+{$~B&q8E&ip!u)Af7@tmdYAu=u@j$SK&x|5R{~EisVxKTeO(Ht?oQE8Kc=v<rI~uw96bH+heaqNtO{}SMNz6!giw(|40KB>N}aWyp6V#MO{_C3Ope|t6Is-UojgRE6ujAq>U8nswz)D=CiwJAJUWrqwkK^e$1Fe?3PdM&#@o^ZY3YWlkOo)}qnoobdQ_j+jA3j0l1f|E#$v;$-Eo}2!0JMEGxM=6->zt3yxWMsTSHT%V=RtleX*EXk6AiZ{<W_&m0xJY+C9nvZOBiECdWKtTVFH~6Gswg>nLQh4!#A+6Z*?afdhP>URm31ROaY4!9kZPwWIOP?47RD{kCmsOQq-ug>a+W(~%ugJ!q8ME>KdSK<7@Bqrji8jjI*Aqf-8c;J@)-ziDvIWy^nD;P!{uM1|h!cZD0ACXwo6I48IJ{?sKptmw3qdlu;6?XoGa?iWyH=0snGVG2lxqo=bM>|x;2<n;8~UOt!20~n@Obg7&it+8{90Izv7yS1Eq(yw^9H`HdYo}!0%sMZMHk%+aTH)eRWt33KPQZ&MXO!U?Bwk>6udYAycL`FkynqW9(T`1qO@Sc*=%qBZ&Z)bYWS8ZLh7G+!HI~Vp*N2fH_3$<2WZUOcr`cW-VR6lh(v~wy17Np;-*{DggwU4#u+%Wv%pe7-C)5s)ux5yARD7LBv2(xX=Y~TtJIMvjI%x5rET`gTypY5PVIv#}&=juN5W<V<L|5JqOg5NZ7j63>_4#GXRpU>_Ro=9MHo0b&-%d0Uz1G@-PmbQ2by(9GUP|dr{vZxVXQj~edB0DiKJ5@{5-eH}pU6-|1AH*6PF<7@1ys|}A30e~vx7%`R5zyIa)u#@t@3_NsZ}n6%K55d}?h`>3!soz<!jS_eXaN0F?AN*-m7|{}7xNa=(rf7r83Rw%M<H55=%wVdl5sc`cMq*G(*lj)bb+MYZX}zPsQf@1b9y?r@l`mgt{$JOf^gl$yvUUHQr#j^4z<AOwslBWpIf=ET$j5htQbzTKUJP$!=C2&oe8N}E<$-s<?&R^pc4&t_mnM6Y+-xxCHQbH!5wV22n`}L2)Aot?&lYbRTY#5ux1xl_6axDdF!ENt>%C8`Z)4<x97_fh~p9hN0I2>Q6w<u)#N&ABqCOBKgyeVizr^(pF(J(b$PrMyawvDQfvMIbkYpXgTiLzG^_=o#6qW`Xta9bRAn9b^h7;F6k>zbU03P}dfZ>rS3rm<3N2cVSn+bL(uJc=_U$Mw1H>{l-<sC|=Zw{q)x`3mJi^`?TN^8{;X;kokFVLI=zZvLqqd}{RZlF;GM!r}S{ft_>yobR^Ip|^wbkb=#aWXcQO!)O$Q{F+?wsw?V3KmDc<G`ynrFF;!c1*8QKoXO9NW&$gQ-$wzTwfWV2_=|gTME4ll6EDDdFMHDb#>%z;The4D0jCW($Jj>EW4x_OBXfm#dkwK2cYoD5qH4Z)mck2x{dQ%Hj31Bvk1<Z9URjf1~M(HaN`HfG*;Kp7p-{?YDni3gfnjV=WWj7&W>R-(qX3_gS!A-`&CVXfhtB$hMm2Y|0a#C7gV6lY$PTa++%#P>DuYLt|Z;=Gmh&#t9=jfUBHq0t=_Qbmy;HI0l=5BF1OTtptJ5@(|m2C@U$XvhS5+iHk!_?zYYPB0E*bRdHn$Ty5nOt8E`)+OI2~XS^+As}uuk7jrkaCygHeP3hB$#nP>MP&`J>sofIp7Tc~iqIdg80@<w7&q1}Of(U_CnCOZ^Ge#7R$ZHoU)9|Xye&t#_P}LI@Uqw{d$HwBQ-P+&KALL4!2Tt+x_>J|x=@BvSpRI)b@dV#S2fNB4VaKt4VeFzw&?{E^v*t=W!YA?<L079i=HEsfx+VpEll+?E(9|gotvt7xk_M*swYsL82@D-m<#Wqac{w6pL~%>-Lp#N&A}o#CBK6kLS5fiq6QlTHqTSEXrFgHOUOnfg2KyMW+{}7r95%|*iRMbn=@`3*yOHlO1-79^!x*Lx=#yNDw+MU>h4%&)w+0QZ8q+{m^e!Ed*N{<55WTHi?I5*MV6%hTXVVJ`JLD$mFS`P04X4#QfA`(1K@%vlC!a6YE?8A2y!#}RO87n2**N-bvP#LsYS*hN1*<!^XNukML8Z?(2*A2DH4XSV%u23t$f$%XwWE^ixHVCbnsu69p)G(y5oQ>(jZghne0Xx{WnGBS+v&M%oyfKG#p><7+89eiYihu2JegJ2NUbf}zIS6STRM|oBJ0!_YqK&@O2;eeQ%`@}7q2m9Z%gxdWWq|}qu#OAOV^@QiaW%Pd-We$y3s2H^G!T(xyoA+5XjUI(e8qoT*AGw^0X8&etcq^VUu2!)}#~d@YRHZovE8B3U>aUdgV(SUg^SFW2~vS*5I9nuPXokLdxU1&Un(b$$NV~UP>jo?0N3fP1aSCrw3G$UsFZ+8>$7T2UuucPL1_DsjjZSj+E)Ip;!8X@|WLR<T4~_`F*t&zm<UEo?AXDmKf6E+w!2ZnI@FVe19MzzPqx0GEaGr3-JxVz9ihQApMs5^)_BxOYNH~rZsjD{Yt87^o?Z4eg$!{@2gDpee|bl<c2lHsfuLN>#7}nPfa6TzvxxveomeAN3SLe@yfjYef<32fX}|#vKyi{`VJ)WPB-%M9r)H;+4dgE5WfL&`Ez;8zXOAJD_?h&!8@g=Q+VG{b%%$Wn!%IrPc7Wd@%eqIg3~vm3by(2e?<!6Z^;w<YRtHyQ^mJr#oa&bFF=a>{M_oh@a0Cx2fiO!ZjBK1*CEl3v&{O>TGMR#nJl^wu~YwaCf&X=!Ve(Pee5Xly_j@6c&2N-8?VQd+p<5h(#`gr8E`FCt{QvU3$ovaD=!KYUK+j$&+H4Z$|}?cW}^FM3|3W>=*AiNu^Ye8T7!zia79476?Cs57Ngr=8;Q~;Ifq?EaJvWlG-<8rG?)6cnkAcMMLnzsfO}=i&V~it@~4`UXq1ZvL8cN4jbV5Dec!*=_0gJ1wYSCX*YL{LJ&Q$WVtWb3<wpdKe=5K7v#QG`fp6T0I4NQiudjbHi>XjqB*{)v`oI*Ya*%jYvg=l<wOv<g1L=}^i*9FF@Ibmdhj*<tFCnp$OOtOx^}qGx%p7L_iPYTA%8$I{pT)*q_d^CR_lt6HKW7%=Rj9Y~lc~3Z(#DoZuSK-=V4IG&mX$QrB=Fbi0G0HlHbOYtXJiWSTVBt(*h7E%$6x>cC*0bfe|z7Z=)=^7N?9YIaPYto$X;LPb7S5twH6kfY8Rn3c39j*6ql{dGPS>ldP}Rt=JH;w-Wun7_+==Y$l?mMzcR%z+yG@xOWdAEZiYsu5a!_WV5hpw?Nn^IfBwhY+kdLcxMoK}jK02r8-L8KIh;t1YDZ~>zAV3RcSh~)M!eL&{p+uP`^*3E-~8`?6*G3_EnQbp`LWB=*>OC0cc1+RUB#~z_oMuEy_Gvu4lmY8m-n?;0*&l-=d4}M{<D847I>h6Tf6IxKfW)ihlW}j*imDv|0{<0zB1P+U!j?O^o&J5;~hOlAW<$lB?i?-4<3<s3*^%GF1C6SbEveo=Xsh3`5`HHEKs~hT6xTAOP9jv-Qo$4-KDBeBw=9NSyL~=>3-fk$WIcD${#;rfB%=to_{#~siyH85uYSkM%*-e8zM)!Zd#AK2|w-D%;i@d95&-;J%njzi<<;FQE05$!Jth7l1M1NO|$Pq%lT}l-g?;S%)yJpgO&?9Q=?|BSHmP-va4*p70)BrQJA7UY;)?^yffY)TdwRUPdBMyPCv*6Rp-E}Q?`$7-+c5{HMp3d&B{XkUF2<!Zov%Hba2Yhr`2PtCpvGI-oR)g8_L+BPCBdHvD=OAK@LhOG0s!((0gj=bel+x^6bt$w0FzO=CqD<QLbvQWZu{wfAONxe77>as=sw>qS@F1<!dr_!ZWD%tq>mXjR{q6Ypu%#;bjw0sJCFKtZEHAA;vBjD+t+r?6H2}DslU%QGX!X-I!8HK1CawwL6B4HE)X~HIO*d?`>?~#s0i~EJGlpe>Z548k%#f&6y%eY+H9d6~@5HMgLYem2qV&D}PMMFg}@cE=W#E^8WGqhOh<hlJff#&Dhp>;>tNXNs`S8={r-C55{`c4<|&965w;zO3wnfr#mf`g|`O;2RwS`daLkzX!8FN{`;7qqeXON^flWpI=gyKPhqvtaabyk;<dJfo10@Yi+jvACjS<AX4B(DWny|X#cLe#<qv~TeC~&#jkaRV7%FTYQiHe5*f;L>W>S>)q_SrF))xU$mea8EKBJB6(J@wI7dCNXUExSq7t9SdHppR@JiU(MDCfYsPCir1wH@qS9hW(u&utvdHN?20zmv!bfFb#WxLjy`sXzQ$ni-!>0!X#-y=dImnsy`O5kKmsSZ!DaHKZn><8(un+!u9Sm+&ij^0UV!Vw^g#+Zt9BmiO`cr@sQ_i@UnbTDhqHMWemT6Zg{}Khz;{!=?0;-iUsF=+OfJY+>Nx2@)iOr4MwkIiWtea^)B~KA<C7Wv#8YGkCKT7GsKAxK1^;&O}{PF=01hkdKx{gcyOT`k2>|hWicm-@pC+PyhW}@oi&c{{8K5zx|{5?gtsWg5|7h$?UN%)8kv+IIWnANcrIv)$+`?qaU+jt(K=T4>grpwK(ya3+S69FUC`@e)6uCPL1k}nP7zoLz|9bYm^b)8Afc+6hiT|{KDuxyJ>#1`Gs5B8{Q3iyl5B;_5g%Y;zGCXCbbBKsG&N|)7KqgNrPAuQ87iuP-Dl`*H=)bNO*$$u7>;uR2jNE4&rnPL0v0Vd%?q}t>Nl8?4*0T`zN>bTkOu6-XeXu$y+Pa77%O^@IIqNUkQE|;X%W!Z)|9&sr|z&b(B4H4W*c<oLfT?OkFS)-i%V|TNSo+7JCydU?9X>-8NwyRgwG)RY5GE)$B&DG`}}B*}R)P<62)+cftOvifKJ;5PpVibAc&)x{tm^>6N=4HOx(G@wfCaS=DRu`S<?1v661+>&qhguL{>UmtI;beU-XinYXEZ%VFM>r*#{|7r%NQs|YhW%sTHqq^yfS0O&3;J0FP`c^nD%7&Gv>k*~DLsVPZ{A(Nq=j!h2k=Q`sO=L&UPL^?cU25N3#Fz&c~<DJk<Sz56I`~AJ{9_S-FsNk3Ktkj^YrUMZkn$f}jTVYfPP5oAD8HJ2?d8rNC?7lD-Rh)6B78l(%sLBj+v9+~Zd5QpAk8Vv3?yovz+kfplh?|(Ci{<c`u%p8oR(gsO-uE`rzWcH<O`E!>)?En$XDHSgPi-g>mh)_D6S`&MPBv!QT}>;sXN~sOhljR2*Yj?`(%K2n8nS30Idie;!4&$b95kAdcW-^hi`-pPmyU>7>0Y$cL_HvQC#R6ccYrRyV#W0zDa_t(Q1V;I`Fl{c$Ap&4YL(epZOa&jyFVj6&mkXP_Jyg(Yb(EYX)=Q+#4Er1b7hEKm8g10Q;UYhdnsO49F=OAPczEcB8+XBuG}~lKff|`6PxmD>0(!yGOR75(ocqG=A&n)sGhe`x{ggFHq><D@`Eji%HTT)C;IE`MB33gO!d2m?b^LupHiGvdQyUAjK8@7Qf*a&v+-+t&Le!V52}Y+DDbIsPSBduym|>AskHJ_b!@^KO0)|qF}JbZyX`fi4`9QPfwkHkj4T!KGEP`~D%j_vZ6(7)_(y@BTE8`l?4cVfO++8+T>~vDT|3suw)4_k=4hM9m)j3W;qB9+gQ@L^r~-XV++{UYmYlJku5G73pJJ2fLEfwox?L^do#%jMHN^|3JYKv3NB-Tj)$9XeE)M2ldXAuU98!-h(I6nPJ~lJZ+};>}jXvfQd%_`rAerP+o<L8uT_Os+ti8aCN!RBEMym&<Yd+Fs6>@->&)2KLm}-YW+Z>}QTW_OmZl*l+E0q~NHZEg>KRMFE9{X+{PZ~HBT`3GZXROw>n@^6FRTVzD+ch3jS6oY-9(^2hQCUfPo1q%%uY4(skk*6Y$eaU}mnW9Ql9$;9rwPV79WKE{ud)QolZe%IZ8RZ<fXZj;ZnPr|){?TINZSMZokEUCu_Jii(D-ZD?EBkM!|qFUqp^~nP0mstmg0KGO^a#|<KGC%D7(M5oXP`EAEvtJ>upyB^3tc^7O+s0R_WEojH}Xt5z~ZdLiF89hhA4@#bD=<deesc;SYiw`8DC<KEfIO++42r`|8`NRoKaln@@YbkS2<Hpt9UUP(7=RrQKPWG2Rm{MYwK3^UL9A8D|_Q&eMb5tP-O1R`#MrQg7vNJ^XorURDD-xO*?9*7#YI`D&ovXdF#;T3OUx;-V*$Y1{HU&QejpTxEbpIU6a_!Wiy(Mq>+g<11E2WIPxe4T3J7Q4{li0Bvz5wM=ZM6Lo1LNpDXtV=BYplcdeBq!r?teQ%5Vw3xmc=go|PmB4^Q%jAr6z_Lbt;sa+^S6p)!(x+r>;5k)zVV|A2^KxZgU%nql2sd)XY*8qV<xwruMb@d#o=9weAh*w=+)J?$W;N&ZhjE(9RH^^O8CQZfHelD>bI+Kel2mP&T=>lGkoh~yPe~e;Z#DF5b*@&co6bET8_j77g|oGwTN)S?in=joocbO!lSIWt4r4&HGq5q9UH)hZ33O5MG*s4tfK@s_w0i;*Y|7fvdr+eKvX#%o1}@8T@DhCiF){2)L+!qZVC$AEeA17#c`7?_j!>@6UYHLPj@j02>o$tc*7mUgYhkSXp_=XoNGhJ3Zv|eQ$6#v#e}P{gV$ukrC}l_6SlOKsYJqw&%=JY!YWU`JC*OR~1zFa>5O|x=MAx*PNq1*|<vt>rsFBf^(<IUL{uby8Gx3EwQCAEwdSF5-FkD~;jo#J@lbcMF{r2_0V&HE%X%H>7RF%BEhu9tD0yga(qO@UoOWN6@H#F;FZJJ<q-cfQWc*Gc15x%AH72gDHLR0QOP|x;JNFw-n6xain5|s(FT2U^BNVx0BTmI%r)S{lVm62kNh0Zajg>o-AvTt|L+n_)T1V{d^u-iC%geQJ@b9!Xn+ge($4aUJkSd_ruDfgNS)tu|<XUJNb5_=PvQK|{%vTKICZz{WeUfR41tBcs1!8N;Cg69w43wzP7Q@z=iT&lmbj=<t2Doss6fq~EJ5z@#sgKhhf?^Mr6?{5*&N<-yqmjc}C){#pvAD$R;m_MBFto>yHOFG92;#Px=nS)mgLyt->TD#bb=x&+9TFp&@nXyCgGeTi(pL#`7-4mK)eoY-F{Tuz%%jsLnCe%5Q-6-@PX`Xd?!Gbz!<+n-^3<ulM+CpQRa4E;<867?wgNn`unzVy+<T=bky&}qPtHIRaohM4cl#Y3KpF!e$^14CxAISHw@UqYT^pC&({ZDxMfB)^bf4<#Bm>`_>UT3f^C2O|7QOA8g)i*3e=l<?)hx9v}6RkG1OK#9Y+*-@-^qa0)A@Ve~{J7CdVi69Ov}|4P@ZbLR*T4PcfByWNt*Bx%9aPIJ%De1)H5UVau1)RCRZ~Q6LFay;(}@dFSq<@Rz^u0Fb!xl)YA4(0<etZgmI1V{REEF+TIU)#mk(NNocN+gGnhkLge{B?#ps>98)eqd&8b<!7qlo|Z)?*~b8~uA={D59+%^-^!f{snTI;o}bhS0nf+_yg0ZL-+OF``a(R<YblqsZPWn~Uh_t^dEN4YQw%vA((({-CFkfe$7+<a8uh(lxFeR)$AO^)K$%~z#;!2Bg;I&Jn+TW^O3BMbzE6!os9;`Ytq82bZO%y3gVTQTk;92k*ZQO*wK829ZH)RmgrTg@$132&vxS|OFgpOS}sKD+sJZn3m@W@8E1Pu<rRUp}njB6r7z_welLCumZ>H+5Uqw_vX-R_*L#FIk0ZIx^nxjR`3XsG+6o45M4Nb|Rhvp+#iD%Fu7O@jS2}cXlgJ$@fah*{?)~_hP6usX~l>e^-grz@VIPcaOVQs&<Fboo9<twB8g0y6EcF#`fJ4->O4|W}cPAr}DJBci2mAT0WO@9{P0LC9rC5G)s`6cv~Trv0ig2vhoGm9Ws|EyH<XovC?bLaPm_Xg(|I5ALv(lEeq<qH)ZMEG>srPebLx!5>`<u0*eor<%iHPuhga#N~=ktnRdiSgj+!4k5y|5xr86Flqd1LyjCd<jtf+Gpgk8`MC)t4K-C=Dm$YxQUfHQPf6Y;Q^=9dt4VC(p<MmU%bsTsPtGCs%Wc3M7oh%tWGbLd@4RiG92^1d<0>>ULtrgokbs#KYwminWg0y!3Tw7<dqTlvb??ZVva4a7;(<o}arjWP#1frt}Xdpf{qSdfWibwwu*ZJM~^`_L}=J;ABFf}Q=sN_>a2X9;Y)FI^7QL~%%_KB~k-j%IT%30qOiB&3^DzF*o?WO7VhJWvFDX-oLRltlo)rNAKZmXy$hdzr`BRnPPiSjv}E4hhmJ5DfR&am`SXEbzd*~6n{EV!n7Wh@D{p7!0RnO%l^4828Si2Plq?HV_kH`3Eq9<*5w8m8Q=dY{b>)X<`0?IHCYzy15aKht%``@hVYAI&EkT7~NMHu`(Fmj`RwaW{JduW#1!sC}r_=s2-dWA+_nLFzMmCa?&$pQp_?i!bIqT8H<2R=?Wgdt`{+2%pb)Mm<xm*Eg;tpgT;=XuqGD$mwnfKmW__T-$H9;R!RmEsqiIVX-<)m6XTi<mk-YBckPcxN0JQHd$cpue@MsAG#VM(cncQ+fk+T<C+5%b)=Gs)vRFOpAzeVH<5ayjbgZ=rn!1|S*{MkXKxt&=FGc$AJ3Se_bMH2?3qEF^Eu*s<$jMB4TCg7eGODTA9qukLrn$LkzzX?t1yl?bs-o8CQ3uW{lI;I`l&{x?({>K%Q{B!(Lp(A{@ila`{I6deoh?#_lK+6vcafSuEnLIjWE{7_V3@v^r)U<jeNLq5Z+ui4f&TD@tdLdct>%7b4MRMskfW#Y|+N}>k(6a>3P_i(s~FJjC^$WO}C%ybH}+s{dQh%%WzbAvi78>4Ok0_$wbG^O0uAvUWbl%^m{{uu-orVwxfrp`oqzp(wQ99o@~2Gi}cwz4|m9kz8kWI&hUUblkMdfPZx!Dl*Jm^c&?a$MyogkoA*w2b@B)@r4$eMQ~ULjvP(MYeCD1jVQNdh4XSMIj;+~i^EXsbFgxLP?_OU?Q8BwhnMHZaZVvq(3Ej`GLdNj|bzIBWCaj&hhZx8`TDZcwva9Mia41SglE049klks}+QVS?Z}zq%n8b2rmeIn@5jZB75h3s-En?BNqg=ent)WWgO!e7aI31Fx=EL{7axD-}F13)ws}?`Fx#Sj85JoYay$SY3l4=EEj~~~xw+o+UgS5f3W{Ck*e^*37s=K4n+ec+@YWd#7o3e+r#UWoYsa)JD(&Zzcsik*^mR5ioNU7QsW+LGA(_MCo(`}XJEtjOoiFy0pqeo_wpVJ}<)%#523Wq96th%$Ow0c;{wUw4#m!ig%?y-7Js+3$ec4?*lR$z%WmD)L4JLyo6GSMO$h)VmaaX}~2?eN~#7HR7nG8Im%15HhZ1l1G8gz4|-gUmK0x6fdx9PAg<vE44GStHrn_D-$Q(#B8AcpfNkTB2sv7dV*X9TmTv{gai|NnVe2R>y;TtWnoSus5qB!B_jq+}1-EPL$#gYjIyiaFpKKbybGd6%{c$ni?o<!tF{{p-gv#D*WS>@clus{v(W~F<%TtDI=r$V@9WZ`+9Db-|k}JO364<`g?1fb9=^?^;#R;Nv-M>?=AYLYq*5Qv2#mtMit!cO$m(l)(E?LEwhYIB-Frg188=)f6Y@wjq<dvdhL7BDLRX&yumaIS+TA_uL0z@FU)eyfqhp_RcqQ4ZAgLDr5x#j?5qcRJ0#u~WgVm%WFKRjxRNpkrWz|MA?ok;`Nk}(xl7!KN(-*Z`;qO4AWnIhRYsI*ZaAo{Mvcv7mZXi!gi=;HG#b@Mm$IY%;%NZr*Y?a}KVy2=NbRlas5NY30u8szCT0Mq@2OTqiNYe~%$I_;8ldC-LA;_Bet82n_d_N4n01(PTtS(RjlF2Iw_T$Ik9%w7_qd;q57icj@o@Y5mzJ+h-N?ps{NPQ}ntkUK9)I;3=xZgg8W-)O4flHMoXuBR;tcj{H;KP$NK{8V8hO)f@jeLUsqdXf1Eq>3+GhcqJD9p<Y{x5+tIb@s)T^v5c96<eP6(O~i{GGT<|biMDZiy?`n|2PSc^2y$zCJ3bdeHg1|xzG^wPhm*rP?Tq-SjY>DtCV+t^FoQ@b}x7fTl&!<yWj#m8e*AVb;A0eN5-KXN)<j8pQv-BwzoR(y&CVw*mtEtuv&<H1R(W+*JEj8OCFu~4oG3U<<h_0SzPYde_)8AfTaQJ~e+IW^`geMhJdq&E!AnQzqXk<c5#LN#s!9J3~)?*CX5MXyCa)lxQS5CN$6GBl-UHX*&+|5V(A*-~f<3$!gHWtu<Mz~Nv8F)5N-VZP7JD7&+k7Fdin)hPm9j<vQE-6tJ>Zy-N%rr!<7E;N4Nisd$tx%r(a-gZ!)TFK}Ff<(?5ayosBjNj$S*5hlnCaZc@KgkRqS%Te=4WN{Jsekv%JVIpZu}Zx#d=(Z|qSz`N6q$vH_4u?7Q+yJOyC9RmQH#>LNzR+ub%S=3^%{`3L46Q8Hak+cb?|7a&%a*gsY(dCspg<$;5y`g_t(NoSoaU}z(J~P;Z_`!Q@CreQ-iB>*{PZ;Lsmb7Ij!0<#1oN)>792`-@HW@(Bha4>>~Pi%_E$aVJa`8eb}@BF)V(_viq_zO9{<OKGJ#NlDcU4%DdasrsD>&PVV~QpzWaD1IXBSVKKb5b_rNCfbN0bQ~atXdfrHE*A8g!C^F^4JCELv_Ip~*43+*M?eMnLa*ONuZv|?N_v$afQ3|IpujA)-giz8AqxYcpqo!_-Sf{eRqKp%33#6fNnmX)p27g+M_m3Z)JGXGT_#?L$IsZG7k2c2lga8(m$BFX`Rp<F#GN(S2z?u1(+=Xp)vfJ<B@`O!;MA3=cD8-Wk)C4<<OZDpz{MxyN?CAyLrkt~m1*v^y=BLJMr=iY>1vZ4c@0V&4Cr~94x@qhx4#O25XiH9;X4C4;Mdo-+um$FB_m1l9raQn}AJ-ipXf9F{7+a9F)<4uby``++X0h*~SJm7M0%kI1baC6ip@JB8QYG4d%i=3&8wNAE5}V>p-vEIHPgor~O|;teWKC%)ZEmTk%R4@47(FP`U0W;Or!C2AbEd%QZLh`R8}6&29z=|;ZR<6A5V+l`=eDR==ZQc`_WpIA+HW>CN$Kq+69DW5U#u-s6&rDAY#u+`m>p9-f3e3FWxmOVxBHawJNqcohn0E|#~0As8;vdI-#vL_LPHc$ak&NK)Ejl-6-`6D_<LGIfl1R5KV}ZUw+u&Ev*St&aA+jHUCq=zK6$Oj5An&B_uJiJXZPh8Z}|PKeWWmU-?=G=Hk<3+JGva){nB6$)s(Wq%DAabK?GVxlug&UEZkbDHi}=g<(eHwYOAqwyA3m43dO;L9k^Dd#UN!3JchY6{NC+;@q)+p=I=d(rByw}J8Xgq-uUr{6PkLwXHlxOp@KHVv>|c<y*RBk&y!Kn3N1zxctD@{Q5=O@a1?9gOrr|28&a%~#@T_WF^eeuXiL?`njNd33tQV}Jilr6#9S{@`h~--ShXCui%91^`c8Ebm<9@_GWzw-cr@S}Rxa!`n^kv8^Zh#gv0g;>-nR4PK?cXxZE(FSEoUq@!{w@m=CXYz_zZ>fdfpPYLi{wZEcswtcst*=X@wxg@-wQu){u?WL*u>vAOWz}&e9fwZZr~$wicrX;g4)ug}@kps74i2U6giheW;vSt&*(yGv$#Uh*NsttrwchW27l$Wfel3&0-wNJUGvwL$$jTL+D)35#5{*Y2=~y2FW_OpzRpb(iUloYCS}#{oYWUZ<qr&9iVnv4f7H!PB7RYXSGLI5Y3xTe%?Q;bMXV0|J8R-(E3dvfHK_@coku^#-7qOhw%-Ud~;I&{ZW<KW_k6%Sk>dO%N_UE@a23vE@tSAo#YD6rk=>F33IS3=0^VR4su#5?J#R(0BU*wlTn(8>=7}yxuc28h?MqcQzEXF3Yxm8px@sdqMi48uZBY!ZVlo$vO`V1909t8U2Zic2@D`Z)mfyrkYlm!*KR$|?CUg%c20R|r3rl%Iqmbk#5)ZS@ZJoz*?bljwU)yM(>q1gkr3AQ_x@k|%2N47WtgM)S!~=VG$Cb6eHmZ4qwSI7y>&FR#_8Up<6!+|DZ8WT8Q4HeUrEhqL2?^c`Y&QEvz1tzbJ3{I!jhr^NzC5jc4!(zEgIXJ>QNHYXJF{&X|qBW>TO<cPlsg!_z(TpZ<@op?Dvlg+|~}8vejGst_G~n1|51TPqgc<b8~5?l5ygs=W^S7B_ou+_19P*cv04@HTu-_5WyC#hjCQJUV-!=u%;fsT{RC`Ini6g#>%=gn;4(=P(~J@xBT7vkRBNqO@=UJyS<QUH;I!|2U6*%l@gM^m9Bd*%#$4P0zu_hr;ud$1;w=5x8e`g-pBNuufCX{I!*CWsnHS!`w?wRWYpPgAv6_G3$jqFuvd4NQp<pW1E3gDzODjBJ-tf~r*ulbb<1G|wcW&O614&HccY!D5$GBlrNN5ol-Z5#6J6HjR37Gss5stIo}hu+TS4sfP1?+CxUV5s^X3LnK1{Cjj01nmIWs;ZI<z&$+55(^nS0+>d!hkbx#P}Cb5;a}YDtx;trx-VqOR<%l7GO1xl4}{Pn6xFW#?lQoeVd5RD2>LGU?ZL+UY&kn4@~usE?WZciYLV%p3d28qJK{Y5ate9&*N-MnUO`OEw9ocdZT{IE{pThG>*CD{z3@J!7Z+<p+Y8T5HiLS~&6KLQTTshMSBG+*-#x_2!l9%B9xA1NW456~w%)Ev`J6O<V9xXwuym8ef~`W6cAwYlnwnZ+EoSN@>e{rLAyf1KFCGb*pzNn_LwS9A6*Bk+8R5WtaJ{_OA@Dl+WJOB+!y<<gW4K4p(kMRgK7&<sf#QFm4xF`u!WgV(v{Vj=^s%OGOXWTEofc$sK2PV9z5u3{fx*R>ztDdTHMGjLlEQ$E?Pp_XuqC?xKa&xAGi#Z0c$S+o?jTMPvu&GbJ0I+Tj(iq$)H0twpCcN))SotBHuDNu8?!KvAe@&7<6#AxT_4Cbo=1#zmycDF6-nxoeS&w*T~GBz^i&JybKDZ4VChR|KLm2RZZvwuyk>Zkl_4d+e~O@eUerl9C#hXF&C$PDK{GH>B{tPV#AyF+T)ySsXqpp?tWtGBU*5*)`?TU%fSt1v<xw+B=Q{S;~<;27X!;>(1dNzFE!52@}OKl|xPXR`rDGJkdjld>PQaL%LTNv2qq|_4}>N7MHyF;u;77O^C$p+lnrDFY?=`4O_tC%@W2imB0eb2G)DBL8u^(V7Dwq->*I87(Y3CKUXRm#?q*c4@NR7%OOVQ0<F(0-l<{ajUJwNYyYZ?2dr!a3r!y0bb?Nmw-wI-OqHI`wx9~&_wf@p<+kkbk3aq6uYdm&KK|$5-c`8p4l^k}_3yv^_RqJ_7P_8fw~y5Hij^_y`xCa$=@f@N6?*RvgMHp)tfBtj{`J?t{pEl7_x<<3K1{XyPJ?b7H8EHz+^ApF=T+@<n!TaNFoVwa1ZNG0+Aq{+zC`+}Db&kyYEnE3)4&A>*&f(2xuFfN?1TB|f4sf@rxByC?M%D4@zfhGqlrZ(rW(xa*L{2VruS=ndvi^Z-R@m?pDRWX8h=Q?1AHTNfBV~S|B%S2c2pHtshtsbqzA<Z%wM85q=v%n$FHMWAMRK+_ZaHLC?iUlm0dSb*9=xjxqeqo$-kS-{E5_P`soO+&#*n-pMU#!0Hu6rw#9Ub)!#iyR63?OqFbxst|R$wU*w`Nm7iH{I+4Sm_#RR3eUESr`mgrvd%BO8en+|4(3EToRtM@vb!yFvKfSrNu;fV$x36m~Xq(rFub)Y(uLWQ5|5V67o6XiQom<QB+uEATR@IVc>q9Z-Tt~Kwg?L*j4N#UUp13Tw)RF1xV$&X~em32Cw#Mz(H|SAL{_GycB7C&e9CyFw^PSnGVCLF13XcsqL7Z&UEML_g<T0}uqOp!1b&(6kU7_i9f}5^aEVe{(clYb#K4xQE<(GOKb?vdQPqELhY@3sxCE#HKvBoY8ls2NWD#a9nZUb|+rQ0qZtKi*D#7H%(8>oy3#{BEvuZH(r@Bx*ha&S&HEGcS<qc#{UPyp2CRs#Is0jH+5_qO=Cwh`&tYExQ;dcB`D24Alcd<A)G0A}$<!&=Ggdijn#p?lNUsS3z#q^C_Y^%3z*lZW`3B(z_m0~7qIX%)Zdv;N+~R%|J>nZ)?b444nIE?CRKVur5gU?Cs!Eb*GI=+x8q?A~UXeJfyuNr$F+1P#0h!Z0<A_F7(XaHZT*N14Bz*0VgoS>!pkc1juXZ6*Wv@vRr$*iP+EN{7gU%nsEJvhZ*O69=(mS?wkiNBdGG7TFnRv~lX%3MzN#Cw8MXzgW!KrBJiODm%4d>qU7w(p9W1>w4So!%PKc)Uw1?t~XVaw=xREQ=l%U9S%PWj+L{MI$cnjyK%nMdz>8F{c1ciaC&Y0Ksyz+^qfcg{K`D1DiWv<Ks-;y)JjdlM0qioBG%8`v7=m3#?U6Tk)kJPxmeBEHlbWl5$6%+%7%t(1A{ToOS`7`PEBB~E2@z<%v+H$4c%fZ*&#hdvaIqu#)fnr*-{?;V61^xvr)qvZl}YsP#48%YRGN-+HCAGsV)F(sa7rxQe3P}BScO$#+zaYyQp3*GUa4zwL{wdh$f|Kx71ag#l+&RS8_cg6)LB7FUippG$!>aC%;Xg#^C02zvaqH*?af<cX54AYfLpx*=E?w(nNeW=FQp%QVk|Hjf_D*p+pHYzL0#aOl2&J952u`+;7=S?e$6YPC)94k{$)N*_8ef`Y4D|TKG=w?<?EVs<0_Er)Iz3<0QQib+P-1*wPMMXCG<Wl(uks`NtIB;v7yI&q?L7-|=AFflpJL@`dI?nhqppYv{)vHK1kMdv#N+N)5{1BVLYmgP%o`mk4!Fi3aFud3$qOM|WSNp?n@2ZHpfwl+?RE!S4+&wvIz9xvqh>xB()3AhNi@io!!1o)sTxFqlN%jcLW$n=NBcydP0#j|}zNHju7a=$7I)tYcftP;2*E4Yz`-q+usd_0aKo1|9Fi0GC-@u2G08?$0{mKLRb-?cuguyoqr|K3bQbw~maqI9?hoExg9_Ve%_2_G!bGQ`ZibMYZF3WYKE1N}Z0ehAdjNQQcd%DJ)HBsO;zV8oP7l<W(n*&y9NU@wxx-?4DN&^>qaH`I7dgqf*7a#Mw3WtClLKlF)dq8G6ocaL!ooA<i4tTzj&iN7YL4rKUJ%V|?;vvi7kwSk(itMx#x=nQKM1Dv2H(2|ZU-F9v<?>P|)?Fubl6PEEo?O`OG6WW#H1**E@t#^?ckHmWzonq)@9(N2}19hWm1dnVP*(KfpV{$9tw-rvHqnTk(S_l=u{+b2d1Vc%cY)}kNNi8uRn9D?dy#@n3PmYdT&wrbh8S&BAD=$o<nvFYaDjKOB5j&9W~AM8hJZ%uQKXTjQ;->lNxxbjevVQLV>)r76)mZtpKf;!5B#=EEg{>UtKEd*Co`;1bCZGt$UW$JtOHW=7EZCxEL>M&Mq+Vg3+K!XC0^&-uKn<sSlEHoyl+GsgNcWJzL==EBKu(<_fGBal-$5B%ZSGcFQ=w-mAU33(co)D|?p|$hQfKT<_-(rRJHLdA&)o8cq18`6b3$~63*8`fBi^OV5r1o~y3Qg@Z_!gFG6*MeD&<2>?KNSQ4<zRYR0%es_X0y;maS)#>s7Ca3(oAp{CY|(-{P%1C-SmmI&NX#xN3E?XZcJ<5wrjq|=Bhn(nUtNQ<6;FS?#$NJ**cYehZ4)Zo02^@`IqVgm(FDOR~jOO--uEP4o0BfAKTlW?!n=KIAv*5)H4wX7Y!;$*GhcolZLo3_40e`KwgEO(CzKBp$`KF{|IL~+%;5VWNl#2f|}GbKY4>A+Ng&11|suzU(w!JriS5OBwLZTz`i<~9izh?R!@xXY1HgKM)&jtkj*HrD2G*}$F8E!@n{R4vP@c}Ejzd@DxFKYr9JYJ7&mn1sqNgofvDU#4^51O6-jp8TaoE;cPr=%E6|)8sYp64yatVxes)xH0j(9ZV;g+FSo@q?=~Rj%oa*+C%y52CMK;YrShef=h*@WSyCvORS|Cp2=-JSPW#GUXR2z8DS~I0_)^SF*Evxmm{+3L(#mO$-)2IwgDc`bS@B5UzQ_(UCmzC*QgNTZL5N>$idJ)gAhr8KVgp#8ZCN{i?GPP4rSl*2lZXR$W3*0%Q)fx!vRo;6A(F<m`cjoTOn3|Y)G?}Q_9eR`W*8Sd$h1EbF2Xi+yek(b@*(6~Rv{;>ik?u*gPG0M=*xt?3H8NN0)Tniqx=p=RZY#GgT>;Fh=ggs@o%HtM0zEYz&zD;Dss+v_&Wl)PS81VkuwygMcxOtZRq5l^PmMi(uD{co3aqL{la69>*m64CjD)kqP}D5hc!SN}_$|WqW3F6#XgHb%Q32wOf!kMzVPd74AkSO$?gy)VurKX!5RU+gV;#!sQw6~(r~*~)d&)SAnvxnc9C~^Zg^xH8K=~cIP?JH~s>nayLN@jDA}cjadr7{B)p9M6JdBm9NpKV0rhA{U7*V~-?&R2~UE{uHO^so&g<qvo;jPbCI-<6b@MCm*L~q9oL|P0`@|P!&LMaRh<?W~s7wOfH@TUe=*chEVh<b#Uy<SaWLroUO_uOSS_Z4Mrywx1R4WkiXIRa^|M1Ao69)_$`x304X>W;F|@#5D9DgX|yVM=wnsjI=@&<@B1bJze>X4Vu-M`H@H+C)_C67}Wk>YFvP=+E?RV!?PNkn;pDXA2#BRT!(Sz8K$m0!(RD_<}3sa$E5pR;vf_k)l&eM`F1mU9i~L?)E9rXDS#2ilE*YLU=Yz{ZOa_sN}}_7+mwQPP3L7=yj>%n{_UuI2czF4PT0bMJoL;l9}rC%nd{>_FT9!-EA?r6+69~V*32Zo^<1YNt@F|F=8bg`>FmmaJJf9@a9!ZP4vl=S}uFF;)<ze>yPq7-N6(-FtCUk7mFQ5`;J6jE@+SOhi77SrlA@Su%6YZm7LnVvN_)v>q`yvx|`D3g_><~lgi?%f~{`WoGOnIVOdb~QrEY*GZcnsO!UYT#YD|wqN()Y-uxxQ>mlCL0VsF;OVgw;<`=cqQ!c*91|Ie9^n2zPO{Jnm%EUw0!<-!!q8i%v*Rau4X7_ut`&k~l0QNHNOsnUzeC6l@K3yug&ckZ$%|r^>7ZVA6WT>=W2PkXK_LDX8;VN;`LdxFiszm`!wHU!lBr#Wftu{~+>20sD?ie5K=r0JLI9f^}AqrnhdBZ76MR*_s4dXt*tn~24l~wC~eUDMa^n#pDTf1Tzr_{Jxvat$w@7-Vjs+Mw;3+{4NLnY3vcSu~EO%$N3TwN!Iv9v&(^%_46g;u87N^0uMmC(M?Y3z5(H|V;zGuj((&z=MvYCIP`iiGwQz^PvPP`*F*_e_|KkX{>BshVD=>S-D$tbIS;%%gE$UH(@uLIy=P{C3b3IyN+m2u3D7gAY{8pg-Zwf-*ghO*`$YxpI2>M4>B9n056vYU)T0k#{!cu-cfm7Ef(3u$-0D$3m+@7be?YD9uyO*ZMs>b<`kRV~`%O0YLDww%W9p=Jbp&lwaN=sun+EzXkH@pge*RO_$1`dS8Iu6+I=6-gJXUnj}y5DbOHdEJycuuDHb%6|}WWf4EKv7krKzV_c@rqYB>6F`?3eXEgwrg*$u6S?P1@gE^}&s8Ob!H1z!_S2m?G<?*5PZ{~Tt1CM*cSHZ(k4SO%C6C&TaLQ^(_cng%bmgGIBCg6vD6tGA2XzGwYs2P(3-#PXxFp9u~d$Pi(7^mZVfNU_Tjiu$8=11S#)s-tF#D)}>txg)|c&`D4!7_1FExLcsw6d7XgMxp^=^_PhFFqS<Psh&-HRGuD%2X|=p5BVlXfyr$bkXfAQjoxC23&X;CE8PWzGC($1e9Ys@d+J}{!Ct4C_4?i#KhD0m|IlR@TRjnwAxbiaUJVf0t96vq0_DrPc@UClyyIlH596+W%?6nVmaR7IKr@II*LdqP|>9F@qS!7?VIaLdm7K?P^Z=M&iP5}(wyvbT6OClsl%^CkWe#)Dhy#e9<6g#v88o#+QTOe$bHpZ?Poi+tF=;HEuYWJH%tN<{h4x{DfH$>T(rIXNI@QP`?I#odnmSTU-LQ#*h)w5poK*T@pj+Ou>UKQm1IA$hopX5_U2nc4cCJO(i`6W@zxP)JiSok_fre3{~kHPy}w16R@FD$)biVUmivnDpIhEuO{_@|OHMsxcRG1q<GN}8xN=oVnq(60cehTLkb^m#($sdZ5i9N@?DKoQHM*7J#9b*>#fmmvjYrjt#bj%?YfaA;&kprXUoiDD0iB}f^jM;)Exr;_u-kmX4E4@PU-eNm0U{*_ehUz_+v9(Jq8EjPnqUT#W=AbKnnwWZ$vocuh&h_uBig^}pz$ag8Opw$DtOYME+1htw#gUm;=;cFBanGL&pcfkzwUYL{>_`s8h;!;+A8_lHx^plU)#|AYY{YP(aPx$bV(ZD)y?MdlfAf>VvQ_cj(4NpZB-ulD(Z?21h&00vE|VB^}+xBx8MHxrudckz{36=&R*kMoR{h1p#SubzyAGCqCD{1yWUx7&GWatwHCRskF9Jv=%4u_HJD-lE+crc5(<?2`saVVz5Qo&C?#-oEXFAR{`R-u{!tZ8y#Cac*wu2z5NM&4KmP4sfBoBE{^!rXeR%h{a8VidKHgtR|L~cgG%^$257H;vXZl+px|;3!c-uqqvGc$GwXc@iGuvTUz(0Ua(PuO>oA<XW_pl|T@E#dRs_i({WcxE&QKbuZ(7bz8FL4b)<+xP_tvi>oEtSs$jh;B?>f<O_f#N+%2Ya`*E#DGQ{Vc<w>rE<q@H=`=Z|hw>>{oltTj%lwr&&A0KIA@iHm$d+le8D^dlhUj<+*BXz^zlP`vu)IrdB?((xz6bv2@8%`Wv`~nBwIlVMwTE?Us&H8yt2IZISV-7?@JEs61`?8hdqy%12Yh7%KX1E<0JtHDJ83khV>~=3#LMK{;kGr2C~vel35gM*n0-|70XO&5A{J_Eh^+TSSG(!LCLn*ObdeFn0e=%#nlYLbR~@HgRng`-<fzVa4WZysl-)u>+56=$p?*-h2^}?>^rI<Ti0*1_^Z|JjPWIs}>TkXyoqrsvsI&Iu6RH<i~FY>JZldD<5k29a~4&Tnf7<_u{q5Tdn0IZ7Vr2Y#N`Gt&704i6j32gzrAWY+$4^I7AI)f91wLKu)!Axj&(p5+M6Osv&?jby4LLd!>y4XNzB*Qo2RTm|2(hDA#joD0dNQ6TBa<;L|Ff#gWotyRI3Z$0*<|gF`0PZIyS^H)Cmq((*<5Yg8-g7kx)2b*QCh(N__*bgImmgf8x9Z^Y9Y+E*)&tz?as1ed}dQCEKn1{B{YngR4oN8=`_<V5%Hvxyd4Vc#{#5j5#`V_2XTP&LQvvGltzl%u0&3sTn)7oizhOJuyBQ#EUgG#}9)075@K-K&+5N`8<YwD6j4{!FN_3m$B577xOOmbdH&32j}Emo6do)Q?<K^a3fL8`3=kyPD@u$59;BsMkR$eCH7h+7_>_N}(Ma6$xmmwF{(KZ9|&!uGjoI1ysbWjy01*y?WHm{t5O`;!K5&%wn&P$wV6FH5<0eR&#9`z6I~ag&q|f7K_Epv8sznJ=FMsc~=qQ>w0qgGVJTo^*uJ)uB?F2s6(yXR=%LR3s#8q-kiyY2aadfBL{;)Zz-m)4x~!9#g>et9Aq5fto&D}_j1`Vtj<yesnTj1;UnjJPz1|FD|%=}U%h2qi&nFj4-ZW|;`5`Uol4K_$HZ!!U$)HEs|13TfwXXUl&^wQs_azukb#txE?bcUusYFAMd4OOL+3PB`frE#JE&LK#%&NeJl91%-BV873s}v`roOd7EbLY?Jr`MmsXLX!5+?N$FjGdR&relye@h`MqP=QbUWq&%DyZc5A-_k6Ijl35g(kNvF;?y}F8rrNaZ{7o)MSjPX~$s?7xlc5dfYFI5WwS>g37vKTm(@Y(FqCOJzYhx{a{lS*=sx9C~m$^wvf)xOg|!A6W@83uF3@+NpZ?D{q(5Jrd=T|-JJ^wxRR|6GJVR?MA?+ujR%B);<s!QbD8X~N?k-LhL#PyO48O=f^JHz-dc5`Vin(}1kDyUeNfF;+4@Fv!wrkHofMTBU051bz0edmxZf0yX#{?YS<n60W=V5YJ-uG0LPK@ZqUs&dJ-E+Wv=WE{`Sn$I%T?xxA5hh01|++}(q7ckB6MyKbxltA-53`ykHqhubxlXu-YI5NX4r^VL-&AEpth^DPUY;Q5wH-c3$x8R1oc*LQe5M^gR`Zg933j+Hq^>1R6&;BT)Dy?NS|Vg0hZgp7Bv*~J?71-T|u{H+{tY*v){i@U{sQ0h3n1A&M259>@>lw|J^SVwN$DC=~|DL()VCX!^a<!dOC#doK9<=iZtD5D`*Qa?@Dy`<cMQUMZxp8FYVA?ZV2T}e(vKI?<-y8ZmmATH|J4jS*88Ktx72Ss}wmZ5+qaka@QPQd-e#0Qd@g_k&K3cXtNE+ATM;+iFf2zJdr(ERaS`JW8~UP!vV|!5)ExWr)*MdDs@u$($E2bq9MK+e4*t*v#nFbF=eRxNPnswB=UrFku6qF5lJzVxO)FBcfnF)bg7*x?as7Mp6u)RM1<w@J_BnJc~_n4WWxhipVxh^+K$Qkk|ay(`LjlLR*+Gpp(>;4o|E(%Sb1Kp0}oaK$ndUh9O$+6so<6>b6c}uU%#W(+CSbR@)l~(Pl@arb4;f2oj<KvW+OciQ<dw^K)!ohR2}a70G?u1TI-Ury+@cx_7IS5I#uA)fDUOZGAa&cjy3F<-dy2u@bixbt!oQIs9x2C&A1IRCdq6Fps_NTP!{Ay*}3PKR_57#H4v*W(GUamxZ&;nxB0*M_m(^}aPX{W6y|v&Sfeew$8HoI8gqwBiM%NnsP)W*7|2x6tVx<xj5{{Bn=0W_Q~EUov`P|;7P;H~0yhC^FCv9Yp&FIe&D{0vpEbAA<8mhbN_IT}RYNbZUmhBt*SOl4g145sqSdjXi!$t^z+yjWgJQTrF=169Or62%kXKBrCh!<@%P@}(e;Y$vcZGKg3yih{;l7)>5;U@+!fCcdeoG%F#7P-aaCf|;l@DGox}p^}lfcue=I_xrr?w!qpsr;=i;9;-$!eUAA1{n~Pi29h4b|z^Wp%wRO)9%wT$igF4k`{wPD|M@J{n<+V|w<nu~chDCQt>teV$UFbM>1I-=mJf7C|?07Dt)0(>o~p=krgNa)ZVox}LXN?Z(X|a|?TM)B|)d=)J8&!1`IR(i&xD)T2$gJ}xFQ^hE7)g#vW+v@+BV98uakrO<678QLg9bnd`kR&~%VFng@bMg-dHn>^F)_j3#O+tLrL!y=BDu6@?-+vK-@^0MGB|EsSOvpS?f+$N!F(f{=!1QWnf%bD`Pcia?9OSbB4YH{zhJ}f*GX&H@Ms)uZ;tSA_)TXl$9qob;fK1A8P0<#Y-SlZ-+s21zJitH<G9>pt)mo`Z$mFbs6D0GxAnTDgYMRR=X?QNK`Y^TwChOCj_z>&Er8MqnL)o<RZ^t)#T(>&d&u<iv+FXl+U+q4n!BTYItMbxsT^4<{pf9(O_a?tt)_^7z;5Y^A}dpEs~m$vPeT9|v@oH%r+8O>^mIeyerd4D&n5WUn3Muo{y5m7UpuJrvBp)71t8r8mvuL|`H-11~~QTs?seqn`ro5>~X3=vC}neyYLt&bm6&8e`6!})yKr^mdiL!wZ@ITWg;7`biBBz^BQ2Ee1C;q<KON|Z9O?R}@^&g>bBxgZ*C2RPGD+xVEiwJuj$$>Xh&)_$7P@KNpE;slHw0Si#$#@@=eYWueGsPu#?>vO&`PI&u`^{Jd&HeZzE47+a)?G;d}r_4_Ozj{!t*Exr(m4X%D7A4`p=%9T>R6J{aIDmS}qhxv4p0i)sb*`4UN(|LTS7MB-y%kdG>5;N#>zvZB!_xN_)+*?va4LJY-BevOikd&ht6kMh((U?DP7og6-ruO=JW#Emy6fVK`v$$Mqd2%m_lsquPPw4+ixMD-FL%FB(p^E+R?>0%tSY-kB@fc3RF!US8=$Xlg%alOy!oOEbd%A%hx@SHhQU~tuLhjn6N}cGZk@nPKC151uQ_gSY?x|aymyKSmKpXcn74LleB~A;%kE&{*U%g4>3#3K5p65Z^SArMPOG&eLa-a+a@0FNv@4>Zt+uk95~InKSv?!n&gr$j^p7ApHbhBP>au!T*BEMVt}9osOLK3ywc0p=dGK@VkY-)`Jw*HC3aV10M^F}wUdT4xg7Vg*b^6o?rfT%Vtq!1U*l8*y)M3<SNXL;qa@Kxiup_nyavapT`TK5ThXTs%8<A|l#=1O^#8l3U-vQRSJwZ72s(mfLv9bE0_W7G~^KQ!3=45nvKk6vb;D6IqTnLeag@B`zdyF)JCad259zk4UD(~v+>cE+bXAHcfvE`W!J_g0}JM9I^ysL&Xjcu?%tCpeFix=k~GGneo+Y`BQL$A}L7IO1)<&NtVUhTK;A!!yrsit3{vT%8a^e13vChwEU7V27{?L?*IhHa3}NjW98bd&0tXwwX`dVYv-EH-gK+Nr0J_?2fMt>EX*J+F^;Bq(>JR)R~=BStOLwpfbO=%qT`vUn^>CaXRi<}C{M?)DxO%(;g6o^{S1-F`|FdJ7?wma36+)CuhUSl5xwt*LcFnf>+ViPL$ejvZ1t>z5U-;F;JRg$m*nQK9wfn(|_}eMC?~qSM*Z(^qE^NWF*lu0gX<Io9_g_3o{=P!Gm`uE6-6Y+YJUw&7%~PP0h)MA`4VWbtc6q`pvsPEDS(rW1Qo$FEf2_m^TSJ~+(!ILxLff5IP(x5aHE`iaaIdMR=4nH^Oz*k=!qs_Dv;r$?>BQb#TR$B$&1?pNzF(J-_S5N}L0$8NP{=uf$oW9si2qO)p0pRzhk1!hy##a3dj`_k$62Y5t&Bnw?={BF@o%3iQ|IVv~(h#K{+^#Rk`au18)s2>V(*p|}<Te&LG32iAF+H#&s!%%gyz~u?l%9k%g4yUx5U%%7SAYv*PdZ*F?GB5`+Jpdxktm0)39_xp)H;uJC22L@m`*0nlNBU#Q&1+2{k5GF26yCs3p5l-H`_7zu|67^=7`_YNoqgbGB)NMrcDTqO(kru-)$YGI2nI+^elE*blek~LS$H1F_={0}nQ`zZFkJ<rL}U`rcr!nc<0>FZa&mc#8gY!D$;?zFr@pB6k7q8b2Eq@5qQ=<%#b^84-F_S!1I-n`BB9M|k-b=r*)PQP@<^5BHMw5;C-A=;&r1wf{pn;ck5P7fA<s(#D^P^%<u#Z`!u=Je=Wp*9Wjgq!M)zN4B)=KKA1!)@-C^oGjl%c#_`T{Rd~k^d2H{_BQv1m*QZG2J-9*Urx})09Y(4$jQEl^N@_oj%AKDo&JF6X;j{QDk+QvitLPOa-9;`N%Z8q$gXCKQS*lkYj&+%%b<X*eWYs{1H)?@oP`3nwXM;S_T+k|gDCr_3}`ZEWBhgX^L>}WhXJ%8f!Ri^fOX0U3Q^3NQE>+R5cooTpexFB=3zBUeLNQA3G#m>RT&W#m}!NmYyXzHrR5|xnnz2`nAtF+XvO8+CpxC{*A{>G~)=y%k^*!;n4k|!7Q8HHsF%<iU*=9{TOEOy<^#-}O+|39Zh_!Bw4TU6hY0d)j7+RviB4p2XT?xtUm`nuMU`O>u4hS5rz>yI^;UX#K)&b0SQb{#l|>3;h~%0}V!^>U25LD_;1i1&*S^<YMn9>uDE1Q6O1k!Gd3*jg6;QP5|cpjLBi^Q!=I;YgZ8W_V#<L5s@L;}rbHe0Np?6p1xf|GRbQIoZVgWhgFp(x3kE*T4S>cm3zz-fz5J4IPd9h%zAIFVwfvwKrk+L~%v$&wH*Z$OMtcOUv`+hON=Yz0)ut9mRgyG12%N7FSDP4LLJAwU>Aw0L>DDGP4}${!y0d7(@?@U*JZ<;?O@^yS%Xj$0EVf+Ak`d_Dd}<D+deg(X3iS{mrySV2D8BJampVMngf%2w)f%zU|vn*Yh&G{1~xu96I}LiuLDomaGj3>r*pkKkoY;QYcMtxTHBa%i%qinnZhLh?4C=ajRNZ5+fGfp78t&vA@*7Q~5@IVEFK-%xbqQpDn&uY4RcQnx~;U-qb>N8=zIsIpuFP0v@k|PPw;r-I#B+a<#HnS~X5-g_oXR4|mH{au6k3$>ES!z8cexC5llk)V3nb&AZOXS6*Y@KWx~urlokczf*fsL%}p$HV89^@8qlW9_pIS9R&MHG-oXo{O%Xugvp>f9e?{WmPhywYPH^Tz|pG7Wv6@9W1O~`+muTRmol8cQ-8t@KoKWO(D;dJ4bA6QryppjxHL_jTIEykv9#Vft937);0*H%Ff4?_-DHsygytrPvOnegZO9u!qXez&l1jLbP7dAjK|YULvNl6ntle>bC8mi6zmX#x8#SiBF|dN4NxT_L!K1XBwR6_`0yG>^NKiQotqN<$w{77Yp4PBu<bh3I*8~A~ia1^x<jm6s=Q-xKq|R3&cDwP7FU&^{c%v6#L}+rKoh%7~j=1uvD(CVW_Y*=VqR(2k&Dz~r%d0mrRyZ9_3YbyHE$q_xtF-{e8nn)h-zi(HFWDW%8$4Y2W9{wsdl>Zi5uJ|D>T5J(TM*-T75<EBg(<=ca{g9)8ES?#Tkm7Ay2|_7uwTA^^xnQb=ZzBjE)xNla=T0bTXLP+)Rf+NLod%C^1y6*rkC#n4s@V5Fo~RBp4y`HF-?#CYji^o0iR=<^=EP{#7w(BWWt}=FddBrK}*GkofROenUtjjsdv@JCJ*YhY%b?-K<&^%u%pc4E@x%hxO;l$7ig)ESGQjEU|Qz-m!o7Oy+@6|;~59Y+DY<7rx(iNX>gvQ<1Cq?XUv}}`ToE>0j)2l0dE!EXpJ5QUx)L<K)QD^FF*qFq6*lpe6*1o<IiR@3HDhkb;A6;rLzC`gN4uULgX^mn}P!fqIW3pI%lllps&za+wb}JZ=qN1QAh-A@)OmpE0QIK7|h8x)C*}{dyB2VNc1E4kRn<{DMVBqAGvG@Ny^HyW~z1#_Q8z!GhyHl{NMlA|NH;^AHL83?|+^7Q|D7U(J7yX(|DRr^JzJ)r^Me(r$l@#Ii-Q$&M8f&G@sIPO6!TvC*sf0iSmht6OAXDPBfor;f(B*&!?PDnSW(I<>8daQ=U$FKIP?<*VAx54e2z{X~;MK9Zth|8m7}QpN8c$tf%pO8q;Z{)0j^q-`RK?CyuSBaXF1EZ<f=PP7|G`e42*S#5X>jruj52r)fRS=hK`{Go9vqnupUoo@Rco`7|%5dF4a(X-TJrPD?&5!)X~$%XC`!v6s`bp4RheO{bMkYd)>RX&q1NbXw=r%5Md)h2P7WU(A``%$Z-!ncvNsU(T7|&Y54&ncvTuuao!3*WnG~72+M@CE_jOHR3(;i%k3`6X8Ykb^J0Dzs<z2Gx7UO{6Z7I(ZsJb@jFfYQd5RS_&R>CiC=8uH=Fp?CVsbxUvA>JoA~u6ey3@G>G(Q+vx#4A;&+?)<tBc+iC=Hx_nY_yCw{|egpK(+e#wd7a^lyV_&q0n(TU%5;#ZycT_=9oX~JUQ>-c>qe&LDVc;Z){_?;(y>51QZ;@6(|y{8$ghOgsSpZMJ;e));te&W}k`28m~Kw=9dHbGjjy!bk{LSi!{wnJh=B(_9iQzW)UVq+w>Mq05Bu@HGBvOS3HL2M6Vdl1`$*dE08AhrjwJt$$t@^x$vVtWwVgV-L#_8_(gu{{V28!KCuHeZLujn$3ijrENMjup=KAhrjwJt$)j@O5ktVtWwVgV-L#_8_(gu|0_GL2M5iuvz#zwg<62i0wga4`O=|+k@C1#P%Sz2aVWOd>z|^*dE08AhrjwJ&5f=Y!7045Zi+$Y(Kt^?Lll0VtWwVgV-L#_8_(gu|0_GK{NI#U&r<!wg<62i0wga4`O=|+k@C1#P*;C8=9|Udl1`$*dE08AhrjwJ&5f=Y!704(2AXpt<QU(?UC6YneCC;9+~Zt*&dngk=Y)Z?U56F1YgJY$ZU_y_Q-6H%=XA^kIeSSY>&+L$OLD?*Ree^+at3*GTS4wJu=%P!{xx|!0CwB;p^ac;CSG9;CkSD*dCefk=Y)Z?U4t#C%%sDk=Y)Z?UC6YneCC;9+~Zt*&dngkw^G3zK-pY*&dngk=Y)Z?UC6YneCC;9+~ZtCpbL5j_r}z9+~Zt*&dngk=Y)Z?UC6YneCBhct*aC?UC6YneCC;9+~Zt*&dngk=Y)Z?U5I_P`-}sk=Y)Z?UC6YneCC;9+~Zt*&dngkyrRyI9v9%Y>$EMF|a)bw#UHs7}y>I+hbsR3~Y}f!7KB1Y>$EMF|a)bw#UHs7}y>I+hbsR3~Y~q;J*1fg6rn%*d7DhV_<s>Y>$EMF|a)bw#Sg+;rTkY$H4X&*d7DhV_<s>2nL7-2nP}a_&NjvL;{2Y!~z5Zw#UHs7}y>I+hbsR3?l*tU&r<s*d7DhV_<s>Y>$EMF|a)bw#UHs7$!s(zK-oNussI0$H4X&*d7DhV_<s>Y>$EMG0X@-d>z|kV0#Q~kAdwmussI0$H4X&*d7DhV^|QY_&T=7!1fr}9s}EBV0#Q~kAdwmussI0$FL%(A*yj$V|$EjkCE*$vOPw&$H?{=*&ZX?V`O`b3E_{gV|$EjkCE*$vOPw&$H?{=*&ZX?V`O`bggD99u{}n%$H?{=*&ZX?V`O`bY>$!cF|s|zjDX75u{}n%$H?{=*&ZX?V`O`bY>$!cF|s|z0g;!lV|$EjkCE*$vOPvbXM|_OX9Q?OXbI7L9fCBXG{Q97V`O`bY>$!cF|s{Iw#PUjmh*LNkCE*$vOPw&$H?{=*&ZX?V`O`bY>#n9(C6#e9wXahWP6NkkCE*$vOPw&$H?{=*&gG9?0~OhdyH(4k?k?EJw~?2$o3f79wXahWP6M&(g@@coJg=eCbq}K_L$fn6We2AdrWMPiS045J*I?&gRf(IOl*&d?J==ECbq}K_L$fn6We2AdrXAPgs)?JOl*&d?J==ECbq}K_L$fn6We2AdrTQA3}46gnAjc@+hbyTOl*&d?J==ECbq}K_Lv6bI(!}5V`6(uY>$cUF|j=+w#UTwnAjc@+hZD$6!CRzkBRLuu{|c_O-P)OIU#jI?u6t?vM0U{`4bW-w#UTwnAjc@+hbyTOl*&d?J><rv-mo;$HexS*d7zxV`6(uY>$cUF|j=+w#T#}ALHxT9uwPRVtY(%kBRLuu{|cX$HexS*dEi0#0{Anr*3SIne8#NJ!ZDY%=Vbs9y8lxW_!$Rk2xX5<LlTSGuvZkd(24T|5y5j651K7t2d*aQ<2in{IDxt)cW+Kc19x0zkZfvwoGbg`FcxgXZhZi)XqqFD@pB)MEE1Aoe6(qzDsIn!rxmZsh#n=*hq86JIa#O&bgk{&iFeMuI1m0zm@Sj_(kJyu{me9;XL4F^S$G5u_<S^<&3|@)|}a#Guv}!gU<L{Bdo&L@!y*HZ_WI-X8v0<{uWzy#@}Mw&TQOyg8BG5-f%P9cZPvsVVD>;hLK@qm|5)1*TK?k>X~glv$1Ek_RQv<+1@i7e1^prEC{}iZ9cQnXSVtbv-5_VVRzneGaG(p%g-xT4weqD9k%_#wqMxx3)_BS+b?YUg>ApE?H9KFlCZ}3I=217wqMxx3)_BS+b>vYZ2N`R)xx%42#b-gV>>Tw--YeCu>BUc-@-Oq*k%jcYe51%;%ls2zLxE^uw53m$-*{S*d`0xWMP{uY?Fm;vJ6<_d>z|lVVf*$lZ9=vuuT@W$-*{S*d`0xWErs+__}f0?jMPCAgNuDY&Ryg3!Z~*y|Aqpw)MicUf9;lgw4o*pKZOctrxcS!nR)6)(hKuVOuY3>xFH-%s7Ygb!_Ve+Zy{C8yh<tTN`^Dn;Yj<Ik56|{2U8E$HLFC@N+Eu91B0kg6CjcFZ>+K3O4{hz>a{QW98>q`8ig8j+LKd<>y%WIaYp-m2JHyI1IjyZN0LsSGM)awqDuRE8BX78-WjDTdxGq!q>5_SGM)awqDuRE8BWyTd!>Em2JJUt=EiGHDAYeUfIqo+j(U>uWaX)?Yy#`SGM!Yc3uY@zxg`0^U8K!+0N?#_r=$-omaN=%64Aa&g-}(wJQ?BCnvS*i2vum&1+&E;WznjvyE4_@ya${*~aSxkbtja8?S8Rm2JGTjaRnu$~Iov#w*)+WgD+E94}wTHeT7rE8BQo()Rn=&MVt_Wjn8I=auceF7VR$8D9%W4o?nr0`LUz2>=vu=J4j?&c&a@p^HZsmo7eCoVs{*aqHsO#j(S)pOb_Dd;-q>4DWu1dq2a!pAjn02$pAr%QJwBGo1XHBx>Lj@abnb^E15m8Ls{ee|<&<x&@atobqxM!f!{y>Lk5<k^BdL9q#@NzkWslIRh3s0~a|XhMa+noB@rTfsLF8iF5b_;E^-%kuw02GZ2z9Ad)jMk~2V(Gf<K<V3PAFp%I@zP&p&2oDo*eh%0BHC1=1TXW%7g048T3Cg(|_DLw(v<P6m04A|rh+~f@4<P7BG4Cv$x?Bopa<UC6N#wUQEoB^PmfuNiLp`3xCoB^VofufuNqnv@GoEM4N_ynMoGq991z?3u4lr!LzGw_r%0F^Tkl`|lf^D1Fp;yi*mj3z08<OGrwNLC<ef#d~}7;KrrmKxv_k{n2OAnAeR2ZDMD>?ODt){i6!k|ju*AbEnIUjlzgsvrQEAYhU$2nHq~m?R96F-XcFIfEn(0)+_{CV7LPVFHH<9wxbiBo6|K2_`0>n4n?;iwQ0!z?dLo0*whaCV7M;5|T+sDj~UqAY=lO2}UL$nV@6>lL<~HK$#$A0+k6?CSaMMWdfH8UM7H<AZ7xY31%jsnV@C@n+a|vz?mRt0-XtVCg7Q%X9AxIekK5#AZP-i35F&hnxJR`qX~`%AT0q&OMudlo+sdGm;5{dSW7_G5}>sNY%Kv?OF-8W;I#yNEs-SHus<NS1dJ^KWJ^HV5@5CjoGp<6pOPd};*^~Z4En&J4-ERipnog|o$!M9AaueT&*HCS8vtu=z@Zb2bOE9h$?n0AKA`ACf>pO;(Fw)|7@c783mTnB{tEUYjGsu{oQ+5)EDu1^32OwHbizW3fYJ%8sRflzSb8n6biz9QN?bZ&6C~_{Ju;oJEpDOdM1n)(u?38l$C(A4P9(52UMBn)iGkqBNGv4yG%o+<Aa%m-e=KEBa2~fgdm>4hW!)l-N}Pd{hgTUT(f}^LfvXez%qYtn0P+oBo#1&AT#p7>C-|cThXl|%!7C+_b&og!$8-U%6Fk%fxlV9Z3BD@9StWR@J$jwsz7qV`1;0*kWVZlzf>%o<y9QYG2Zo(UKx_HYASiYsfv-0hJJAP@ooM^daz(NeTwsC^OeFtAR3h1Ah)X2kwp=j@qMhIp6MSMK0lE>W1?@(p#s%<?2@W#BL#Di4fmps>f@lsmiCSHPpG-Mj{wCaI5`T%RT@r_hx?Muy4nTK;*GzDmlcWtKc?13+eWKkdZ|I+VHK~Aif_DYto#0}h33(^@>s!n_p@{e_&^u+xlmPFq@<rYfYZNA1fbW#$JxPiMn6iR>^A8u!r1OzU|7w}^uLgW4q(09?z7z7OghVPKlS)~<2HsQ_w}Dd!(y4@eDj}gtl2M_&pCqM1fj=RqN|IEe#-C8+zhL1B)&51CB2eBBG&~{G^78A1RP2&qC*))aNm)WxM)GInl}vIa{s404n>_n~#Sd8gfW;43{D8#|Sp2nM@gpY>=H$bXlOH+xAFCN93BHJ)*CYTVx?U3y#sr8l0b@)6852;(1eh@aXG{PZlOT=ge@%cI6R^gV<(I;V18z)NHZz<!5XY2dHzUhCnpBQ#{K&?SZ2ZW^k8J$N#*b{g%*Mwf8$Yt~=V#*y<?f?5{7AdCv^!xs@5sBqHt$a8Gx?E;cS2LkqnUR?SImz}y;J`B+&jy!f2G`ekZ1kna_>Q2Szqowh|!;yd!vOb4Z+-7`n&?U_aMLJKKCBvm)_^z!}&{d??LYV$i1JCdrwF1edOMMG$j1zG^ZTt_<@2SDENVbA1L^Nf*&aOk%{jz@%hNak4*dzmWdBCeu)<&GnnPfWkT|ikbPKFmkFuKe(W+KSHWQ2k$WGx_mO)ax%ZKKAG!CDdmp*Cl6x;l?tSFmf4JNml{8pkkP;wlF-Vb5@@^8c7`n2aq(O>()eIcp%<>uhT6yuX+90GTM-qM{;YSjFB;iLAek9>X5`HA%Y7)L4N%*fvIhf@?$P2SD55j~3&f*hLo=D*LN+9@3!tgc7$Aqd-xC*!Q9iI@oLTUdJ!a`vz#GZo=MS>7Tf)Yg%nlETkB=CGC5Pc;ueI-zRC2)NukbNbveI?L+CGdSE5Pl^vekD+TC2)QvkbWhwekIU;CGdVF5Pu~wf2BcM{@`ap{*}P~l|cWM!2gv%0G7Z2mOufPzyX#(0+t3zzNO`F5#mLB0)7@$U<q7c31naiY+wm=U<rI+34~w?j9>|rU<sUH38Y|2f+Msm5~5=og*R%Jf8r#A)i6pc$}C?kAH$spnF%p7A!sIvnozY!qwFy(5X8+SjA4kJ386C~b|xVWljsS3iv)p-B&=bOxJb~rNJ1M1m5T)4ums|;B+OyscGkitumr#zmOvhsggp#;7YTwF3G`tJ{9y?MVhIdlNhri1dy$}fk%U8R6xK?itrXr$A+8kW%8j}bpOE96oaf{~ha~_Jj06>o1R}8nCb0x6u_Rn#kitmN!bl(!OTs1wIgA84u{6rt#S(xdMuH|r8s+U`2?(VabTN`}ia{A838@&gF%nqClF*7l9wP~_7z8pB6fzQs#gZ_KK_nwVB_ly5BS9x)kz2+xfLca^Tt*UlF$iWP@QW?Nyosd%-HZg`44e}Zh{kYGNRZG-!ZrpGjRX~q1R0G49gPGbjRYl)1SyR)iKoRHfSN{voJNA4MuMP5f}%!(q(*|KMuMnDf~rP>tVR;LF$ilUC~G9)8-un+g1AP4x<&%wSQ5rD2y7%MY$Ql*Bv6heaE>LAjwP^;C7~UI&_<GQ3aO2Rc$yGU6C!FtNKJ^T2|+a>swRZhgt(dzSQ8>^LTF8soa%+dR9H-f##DGrg~)VcGQ}t4jS875)&L|p(j>1GYhaRhiZy^pn-FRfVr@dOO^CJ$;Wi=OCIsAsh?@{{6Jl;c&`pTCNy08vITB<!lEhsIb0i78kmg8;yh+G^5qlGYZ$k7<2)_yOHz5EgMBs!FoFoQArXxY8BSEMmAqXc#;e;@p5Qh^2ags<p<Cr$dzwjv>)+YI4xt>fCq$-kVONg+9s7Q!>gy=?yKm@>-B<Kqumn4`A0G9;BB>{3tg1HFbBFGA0l>}TR0a!^uRuZ6<1Z*V%TuDGz65y2td?m?<4-l3Fh$R7INdQ?AP?iLkB>`ti09q1|mISCJ0c%MBTN2Qg1h^#uZ%F`L(k#zDT@Efnjy200z(N4_l4f}a!fPwUw!&;H)V9KHE9ABtyDdH;{I*yKz+n=Am;@vy0g6e$Vv>L{7zaw22TB+SN|*>r7zs+42}&3WN|*{t7z;|63rZLaN|+2v7!6984N4deN{cK6JTGR15{85l8WWRrCSpz~Noyh|g%WxblQ3rioJotEo$z9T(IkL02`EhhOp_K#y5I(Y)FePP30O@6Sd)O(B)~NZcufLelYrPHKsE`OO#*0>fZA+l8Q?Z)k)zinKgDOU7#2ByUC%PWauUFt1T-fB&Pl*?5&)e9L?;2#Nx*c{B6p8v0azyi*GT|&5|Ev=$VqIKukf)^Xom4ItPKD>3Fu7%9FxT10+2~SWD+2m1WYCYlu3&`0+t1EnY73w2#vVBPOJ?8G)WxqBF}-fvCNmV44|3>tR^kOfGiZq!htL#$ijjwgyQlhg$!BPkT*JHd<?4u;7wZOiLgq5-=sxY#qZBDi;#@VTf@o$u9E=lq(x3_cx%9S5&)hAgeL*wNx*m#K%NAY=Qzs*&ob%I@H{FCFIG`Vz-SXd+60s~0j5pBX%m3j1f(_rs!hOZ6TsR8v^K4>Ht|vc*d`#h36O09W}5)oCZM(nux$cvn*iJ<Ah!w7Z31?i0Ny5`w+ZlV0)CqS;HEXt1@p`*X92lCy!=%f_V1Zz0Q9C+`uDNRf%hf=zG;<1!u4>nif5DKg4~~+8RY&D82|+*V8IDsZ~_{f00*aayc|w|;3h!02^ebvh?{`ord8f4B7<a1KynkH+@ln6lp>B&#8HYkN)bmX;wVLY&-6VV>HCqszgqeZr;EUx5Sf!;afr=HNGqhafDoM!qZ5L3LX=Lc6emPC3GR25{8}m$*V+OicUq-ZA^J)1#)#f&m2~?UmpxMSBSk+_^dm(-QuHH5KT`D9NYM|4(qFG#Xcc4^UImdTt%B@|?5E_fBK#@JpCbJ!+MklYiu$L>e{TApA^-{nP>}!?4NwsQ6%|mC0Tmrk5dsw@P)LCyDiNX*Au3(ccS3X`L?=RYB19)bbRtA2I?I~EszP)kL?=RYB19)bbRtA2LUbZTCqiT*L>xlIAw(2HL?J{JLPQ}%6hcHHL=-|qAw(2HL?J{JI?Js=)d&%V5K#ybg%D8)5rq&@2oZ%4Q3w%*B%*xc@t;iag2#{YR>twEc>Jze$j0MGc`tI>lJ~N~?m8Y%=L#NA=k0qRcswCc5&|Wi<)_d`MWCef_ES7GG*S^L34xLjC<%d*5GV<Ok`O2ffszm?34xLjC<%d*5GV<Ok`O2ffszm?34xL%P>%8oq~WJ*7NYak1SG!z|HNqlVU!R?31O5FMhRh*5Jm}Mln_P<VU)1J2|Jvy#R+?yWRol1LWG@9Y3l}(i!pYMosdKncT>g1uM%Bc5yll|T#?3=Ic*u#mPu{wfFypEL`WB(zz%>%ptQ9FeKZVF+M0tt8iojtg3{I|Bwwvt!w|u1P`We>QQH24Uy4lv|3Ppd1P?-RA(XbRA^eR&hRWqD+8Tx^ZT&;I7<(pd-@`B1zK36cJ%fl$h{%M9Oo+$?4P*ieK!5=VH~;|%ARqw*D1bI8WGo~g0t7{5f+R9+n#i*Zx64oGn}#8RN-{wvnV^$QB9x4XOOQ(@(Mv|qC8#D-l26PsBab_nKN^Mz`pJ~!V^}_rP$tn(M(`ylDU(PkUmJ!9s>%deWrD6UCHXB_aFA9eXe$%Ml?m#~l;pQy!9ie|ps-9Lu`KH3cMU@X$z_~PNOYG)cv+N}MWcKc4dt`^6q7^JjU@9#SaYIQKFdfE7M=()Z;H&Td=J-Q^$AOW=#~R`At4J8@$zfS5D9Sr{5O3JFUeQ97x`;4z9jQY^4Da732RQYn}tO{Xas~uK=hkMz?q~$X_V{mG3in&TZTx~=Sb3jxizdqQK1tVI?<sMAv#fd7O7{Eq7$)aQF|7-XA!McT82nOphX2*WS~U{T7;lQp-v>~L<?HPphXQ@<e)_lS_Gj*5n3dnMST@5LnO-3+k3`36oF`x-j%zSArcwZMXV+LEMh1uOOcNj{b&)876oaMkQNPT5s?-ZX_1i@9cdAg7I=iDl|_t#btr18%QjYq&tfr(ys7wU(N$f<GV8dt43TI}3xXobs@Ikw0-8dAQwVqp0Z<_zDg;P{fT<8b6#}Y4LJACQheTi%=ng?;l|*G#JTatJ2`a0UH@*oOdBZP&Gla@2L1C4kuu4!@B~e$swhR$;Rtfs5lx18Fix66>goK|&s~RW`Wl<3qK8uae0v{74agh=iEph3ITI4!>7OPHxI>0srw2pw*5zsmUT1P<Z2xuJvts_C}fZ>opc0h3`%R|d~M1CJ!Aiz5k@DAV(34*uCi^b9dj7M4Gu)N(-rv1)a%Md|m@i@?gTZWFFp<i$SLPlcmiVhovt+f811O|}ibxD$?=#a*G(P2w8q=g#!%xTLnr0p2l0OC7Zd{2@}NN1|_%p!6jNTC<?B$<PB97@|KyzNQyg+-bn;j7?>;7Wd4&(Ie6CGS#sfi6?Y7Aug%^BpOWgmUqp@LP+k6)OSyLn>CHGlDbRBD^A^FoG}~A^hNtMy!NiL|+77#9p|61TX|%WPOOZh_wi{aQQf4Aj?BEMKDDyMJPoig_lPhMHodCg@;EBMF<TP7$iP678no%5&aPS5cUxD5cCl95b_Z55bzN15bhA|5bO})5a1Bs5Z(~o;QZmQ;iBPLvv?!E4*m!Z2_6Y92|kJKfiQ*uhWLf>h3JLgh1iAAg~)}Ng=mFfg)oIEg&>9SgusNjgs_Bwgm{EV1f^dH{X*v#62DORg}^WLeIbqpZ8RK+aUO;+8g$Vhi-xl>j>0$zLlO;&Xb?n$9vTk8I0NGd3@tQBq2c@sAvEZqK?V&fXpo|S;s6No!BG#2c`(0&njK{5U=9ZZI9R(u+KmDO$hMzdV8CEL=JGL?kJ&7YW??c5gISo%!dMojvM`i|nJkQCVIm6yS%bs|z77Eb5dt9sF#<t??SVNgjA3C43qx3#!NLd@Ca^Goh50LtUt#(R!&jKS!srzyuP}IpxhsraVd@G)SD3lN$Q358FmQ!=D~wxV+6u!~n6<*F6(+4PXoWc|j9H-)iXkh^SYgBp6IK|oLJbt-RhX{Aa24vGD1TzI3WHUsePXN%Q&p%TV5TZsLcrt{2B*9N0w55KOJQ0H_y=aCfPP?73fKqcq=0;2N(w_#n2`eNfe9%LNMSw-<58H7!f+I3qc9qU$tVm)VJ-?|QJ9LtP!wjOFcO7{s8K>UUx(n0=#B8r_P{6<CZRA0g*hmUL179CLr|E3!Uz;5pfCW1`6rA&Vfu-%p=9_8o(XUUVS5qw*C?4OehGfWM#0<@#-0ef4pUDUdcw>TMxJEiNn9BABZ=TPb|hg-680oz$%_%q;Lb4YBy&!Z@x!T2l5ZmElRC2G`?GwDuTJtW{AOf<Y$h3Pl01J)@!@5&+%o(uHa1~rQ<h{}ZX3=PyBk2oB<VUo0Op#eEfqleBcI@Vkz@cd4sH-LO&DpyL=*4{%ri}rm9OU`JC0|^M@!BhCOf7q$89;BuCh~PBo$v^E6NC@og-705xLJKnX;f?_gONDGRia3WT{a|YK$ZnIV=Eepwqyh(Qt!8#wl%;36u>^0+C5o0;sM4(I)}Mq#z-H?n$69fnc$E@j)aCGzeyk%=9eZN4|>RfQ*3#L2Bgt$Xf-i*(Jt9`pArhb`$vo3B~3!lVhRetYybS&568)khrJ`GP0Q>Lq>W-$ZsS^Mv`+)l7*{ikmtrezvRinOY}gZOvsuDX%iuD(sE@Ij-w&hvt>e>rKQV++$)+d(;!K+pD+_Lxl6`ONa?(knUM1ll0HJ#M@aj!7z)4oBX6cb)&c&=N9Ih!wjzdW?o3DwYsoVWaz9An7rAt~%by8JBq58uWYC0k@-~Gg<d%fw@{&XovP>G}8IWhn_CT_ElSn_>sYA$INmAEJDov8pD!FvRe%anDypqrjkmSzrq>@16sgMPKWYi=?1hS=&6qB$K$gYyyShkkz4`j%}%$kr&(;)UiGL6(~ko_bn^_E@}a%<X>YuVelX|bAYFJwo9m<`zx@@yJpgNfy^!;otel5HBqcGzXew+RV14Prj*H00cbq?-mY;3^(OTnK!~ZTAjsIe3|SlO*QwUcz^vHt>*qaF>9S)Hvl=!873Z(e?`w2XSn_q~RpFJ@%dS2;n4un~5h9JK^n0^8b;Hlbiwu`L6s2e@$)%{tS0RayuV6IpMxYP6py9NxlWoDWO%8>sfvv|H1Ep6UT9Z<VLXz<<Kz6cf|SPci`+W%NL{M=!APG+&tm#2?q(nNrG^cAlyD}_YViZJpfiC4itnF1&!k6#m$SK7e_CTu;C#11QH+EbQFg#9v?0rCk(<7gK)+m95M)}3>xM2!R>Dkf`z?32^K648-&vaZI1$cWP28QC0L-SpOVy1<-~#d=_KzEixlS$!oh>&<N?A3!qJ0p_8=TS2&WIi@q<9PKp<Qo5H1i17YJkvv^~%&(M!S?&>grL96*lzJ)FPiBY!{g_djy}{v+Y+Ne%`#Df=Xcghv2vJmOa&+Tf)jAU9^J4$c|^XAOa~MzVE*cEDS6&DX(SL%?_lAP<4Rh9)^=;C+L?Msjwvq}&4BB<(5Sv#BQSB#~v3Y+b$>C2gn4$lFQ!S_Che<VUz0`MHt06Cfo*<I4r^Cc%~_adGk^{Mqey;n!!m0`Em^kKgx!dlS$m0^D>#zG;%>fHeIE`zA2zNCJ;Qh6J7v%`O={A*>PN+Lps3x=9X?5O>Mp39*h4>~2wTLgc&T@PrUZh=GJ4cunFF4JC<}Gwviejy(1zi6=zKS{6@}tV(&jZC!4eJRyo+QhAzWnIdogK*b4sJ|yiqh^*Iaev;>(<$_W2d79)cU=1VI5`rxu+Fk&1n&fpX8$?dhwlm2~k^ETh40!YhPELr%gm5ewJ^FYqP&t7Bh!C4^Q+fg!&?ToQ1Z)B+&>k-*MDSa{oF>^OfVbu5*H6rx5Zy1JIU&qTE{|A$fz1g)pAhvWkw@q!#C`&)5P?*PKq^EC{)Ff+dHlTP<@iAAhtLTb1kLiDEr%yG8xb0fZeer+OA*Zi7r>oLo6#)L06Z#~iAdUvX1Q3>2W(2rei4Sh2$Nrg(J#X67h(8|F!@Co@giw6!hjcH!i&&mMABx2AumFkk)*=XD~ee!!mt-%+KVvmMVR*@415tLz6c{<G|MMoc}#r~#=Z!1UxdLg!sHi8s}W|u2*Y1APamK=+KmY9Mg(#q0yz<ZoQP&gp5?~G6^kzxXDr@WJ}drM9P;Lo@iFnqSk7oSBD5P3+KousjlfVuvn&gEW-t`dEDHl$8w^D>%gVs!215~np@_gxL|`Z)Fcc9OiU<rvB<)6EC?b#(5y*)MV_<|%BSNPUNv9FWiAXw)FiHi-EB%7fafG3;3knaXdI903QxMZ)gmE$WNO6&v8zT&kT|juk1Q}t3j4(q+7$Q6J_;4OS9C`ea#~*q8_i9VQkSt+JmX<Ad{kqPSFyekq;w!x=b^?!4U#ml<in+&=cLCj(?J6U8CrlgnG^%W<`yyVD+Im%-eEqgvMNihXh84o7^uA-|9&Nu%)CFwEX!Tv5jyY=&Z8x&?edkIoM_&YKmmA1iioOK<R|r$zfZJ)wA9y>VUs%cym;%3TVj+x#(;{hu*c!WWk>7&-xX7=;j>Kp<N&oO7zX!V#<Kcw)a9ZS7jncS<Phf9u1LCqf@m4X<O&I8wL>*JzT62q@r{A`>NR}>W`y#30B}o^s9lgkx9v70HWQ>b{WtR&r(<ME}L^>_vUzGG5bLzBgUPmV9@!G`sT+?%muG1op=$f8mjGdPGE<MLcJ7K2%(*Ck#=h7~{NP;UC6R#z1OR`+CnDo_2s(a1Om(7tax7qn3+hx6E=a`4DX6J&p@3M1gyxwK!i=@wZI%&q1?0k_#T3oGU)8cF;rI!0%#l5auc0O)jT#|Fl-xCJ#Nm{cpf=}!DlAKF_Hb(IY9iD^^PeO+$t>Tpt?^c0T5b@CAN$Bt-ba>J#`SW)1a!t<RQsGSrZJ&g;PeR)#q3x5<_DN{_B(#0fD%Zixt0aI@&X7<5TVp<rFrP-4-zN<46Xw&7Bt4v@k4KXJD<<i*ZjAX)?<FT;VT8+)QO^gv$q7@UBvYdBr>opK0;f!c?s9bcU~N2_WsYW<qgm!?mN}Ybj%JyoS>|Y#`9tUL(~-abYWX{XT+U433EU_IZWQ{UMUfnyHf9t9WEU3m50IU}RY$^R{zWsPw6UZc89Z&2ElvuLOykJmj~xEU;g1~t$l;G1{>b5v9R63z;pZcVKQQ<v41Uw7d=3V0waCyWXLR82NA7;)?nmx^<nBlAe&p^)?tbL%*W7(Ma`z*5Kl*2m{Qbz^kNo|}-+$Ho{pf%{I^d5E_+K)EUyls_kD%ZxW2%rd{819F1i>MK;82f<E5`WYA>km!Kd$mkzK{(JzlgDYcttox_(Y8C!z0dOXub}nW?N%eAHEQy`tXDp)W@9uq1O7n)mjMxR<9`6N~;`mrNeAnxY!Gm`~a^)?i~pXbVvz8qy!~Wf)pu1i<BTnN>C#u$dMBCNC|?Z1VvI><=l&y4na~9MbdzZD~W8WA>&F=lA~4n*2J!2Sh1{_R%|QAU7xGxN~?r(Su60doszD!ZmaBUin?Yf-QiDUsNLZ;=CiCuS&p(EWkJe{6n=jY{6q0BL-8&{@h(H@E<@=qL&+#Z=`KU*E<?#EpJnnI=Se8tWhmX{O^5YSnb#~&xT(3`%Dm<ean}!-*L*MYD#`m->AViIt>sT4(BtoYvCeD8lZei1-fr_w=QZQ5GqeITv;y;XS4co`R~dJeaaS34m2p=Yca?Eh8F!U&R~dJeaaS34m2p=Yca?EhdAqASo!5+;%(%(C-6Y7Iwwr{)!dX@v=GM2H#N;|O_A)f~GBoxwH1;yIn=&-^GBoxwH1;wy_A)f~vWU^%>%3-2?qx_hWk~L2NbY4w?qx{sWk~Mjv#fgvG2ou_Sr)zAGiKW%xtF1~m!YheA*z=ls+S?<lp(5@MVt0s=QTrPFGFK5Lt`&PV=qHvFGFK5BTLFilQQz8j6^9TQ_4t{G9Dr05wbi&5)F-wq5z)|tVX~Z(9;~5d@z$whb+>s*$e-bx=7Lm|CPc>MHBopsb+E#ELU`Pgkk2MZ6=HE<_+CU77fl1zL}ha+K>btCYN$1!=^b2o67cS`5v4YpkY`xC)q9nD`x?m@d<1j*f%HnE!aFTafXdEjGR$%$*^*UnKSI1VdxA?XHnjq=o6LCFnosPbJ{5KOfs4*Ohg_VjY}%&ve97qWvsu91(>k{GnQb+8q8RP8LKd38D^}*4Va%U$UIgg$vc*3oCKwxY~>`Z+ABJb<$DLuV=ZSa=8V-W06ms;#+uGp)H%ufLCn0>P{JD5xM>pBN1>vG-H@>zGWJ8phPblRU}t1(jf}k^1U1+o89PKMYOqZ*_K7GAqrRi!^r&Ttq!M;g##YMMOBtI<kb3MWkzTnX_1IrI2_XLo)hCkmhG3mURY|_sQPpHRe^S+C+P-toDVec5Z<GEkTNSbOlJ;k8+<o4kv6C~la>icHB)=<(b(4VhnWQfRp`?b|U-)XSn7vd#NbUkjIov?nN?;e%KEo|!_yrU%5{c@PT#uWO6(&n;TVwcbvdUzcNfAh@K(f%J4kR~<#Xu4rrCx;14u_H9F|xP})a<et6;-<|FCTTgOmfGAtYmxwn;nIRjOty+z31(=VNF!<GKvkE<eo=a{KCtGPhfYUj+X%gWK{ApI$kn-Mn;267N>z)UPdu5lWZESKDdnxzmefMGCW6y>&WmOS)2!IdKum$!+m7<j|>Nr;XyK7NQMu|a3UFMYZ+c7!;NJ4k<F%9zVId)?j*yXWH^)zkCFiwWVn<JpOWEJvUnA7D*_q_Y9O$I;06L52y!6Mfe5jQ5}OcRiC>Y5pEwq&`AN}F1ldH9P0D`aS;V!7ZxQDr-bLJt_!p`EiGvXjvlRfv#fXpDYJm8JNVG{6P|AQ(2b4k}>@KB1sRfFg5kDi2M#_QWX~fltuMuY>B|)hPin|eiBMwJAjtIAja+^rE2_KfY9Pv3)85B+|A;l7>Beg-{#S*V0DsEC86dgAaaudHJjz>I?xE}F6!jC1+M+DtO(M=@Xq)aH@M@X`SB}-_s#Q%u0n@GEf0}>A;Tv>VR#E~E1V=%lpBGGx1Gp?K}#TB8bp5cqKI3pAeGYaa*u^@abIP{?YILCsFAT8;k^qI(3Tep9%&1ZuQWG^Gi|Fpxw;{&o;8fjn~X{$j5kggg80O^LgJswC0Oofgz51WE@{csTJ&dHL*SK4#(u-(<F_UGh{n;W-D(pDm0;Zq1#KvMG{1d9k)(iS7JS6X1C)kWG`q+MleMUfViER>A+1op19m`HocAgwF%1oX8Ms<hpvoP0VcDnpGr(hVbBFoPID5_{Pfh_;e5OIHgzS+Zn?=wQjniZl8-G8#HEIyy31I`Sa)K(rmiAc(d|HgBa>g|ITC(<5&m!LOO*Tlh5y!RP?V=m5#+_sD4Y$mssa==#WmoJ-^^f)I?3kBp9wjE;|tj*pCvk3w#Bkk%diD&ek_MkD;DMNTvLO?O>9gUGMq^6g(_uvli%1HI|u$s!K=aWcrF5?Uz-WRVZOsRv}y5^d05&1g!=XiCXwO37#{&*&x30Jbxb?F?u;1KZ93w=>Y~40t;O-_8KIGZ5~K{*;Ucl?;eG1LKw#GN!GaCj;#k^8@nE!m5t4SqAc*rRN-#vyA?gj0TpB4wj6L?u?G^JPJ`M*5N3JM%+I-xidPs^C&?R^qMd<y12#8=;Y350ueK#n>(Ws<RaFZ(bX-sL}&Mf&oZOKyCk&C((`>Gw9IJ!-d-KlPj6IPGn&COn!)oZ=UnMVlXoE}T{&`GPXgn%z;V-}9xR8CMJ~oKkQ2!DB!CX_j1KWElBx27&~X2u<(fr6^`kLAi;}9m8*CKOQ~hYn&*&h}=pfG`ttzq&&{q|EKx7pg8%;GC-Q;<ccPe))FBSV^lolUcA#Yah7>cW#{IPt0xC*@HQSKg%G9MDJS(I3BG+wjFvd(htdfNUr1X|@!ON$R*D}Q*UPm$M*R`gqy*NnFGi^^+8d%7gXXmH8WqAoc*`qc5WjJ}<WUiFM#^^9Ki3<Z;m%xi{vNrnPRhEmA({~*KN{sT%}-V4wI$$)V(zPiY~W~hT?sDfmCD}Q_sI0a5jAQjF+DlCd1PyxwM0Rh2$Mq^Kw&Ylm7`7A9y$Z+$<FrS4#SlH+*GOt-^>W{QOn%2{i)*tlphs^8IdEeA||I2De<w*pIzEnFZ<G22B?WimPwMRQD%j10{^I0Cx){e?}`X8hnbu{N6!?nk7?J-<?r1;eo|4@ScW2N|6a*k)E_!-H|KE=;SW)20ZKbV5lF-Cig(H>*8N2Y#c>PM!2Wa?j#sUKReM~}?|JvP%9@>u>_JvK=)x0WWGJW0MM(cretW|Glgy!0%dS!=YJB<cJvjW$O*f28wAI)9||M>>C`^G7=WNIHM0!XA^ff7D6ZuLRw<8CvO-XrG})PetB(Dv;w#4@KH?dr9Z<6%sP(n^0zG^EBQL(M~d{S{tIxaD;bLw9;ZBtrZ6(f8_8-4u9nEM-G4F@J9~+syY0j40|-s{Gpp?j{f+Anf}P%kNo|}-;ezL$ls6r{hQ_QhbrtJQ&}oclAj9%yWFAh8Joa@;qxTlz?GQdpXA$H`kt|2E=YWy1OUd?5oCAz%-}Qjk(R<|Y_3ZVpJkWbB=K2>+*$>uvP{LDB{?EV<TG}wp2>ee@)>)%hRJ7a@*mL&pC@st^5FB<R5OWd^%D3Dx3l5z%h~USmjqsHv}_!f8LsLMeZNcJm-g&EPr{`h<Ejyoxk(5YZ&LS3C>^)lUFhZDKP7jcga)sHtY#AGw0-hEf#ze{DAS7cJx{{hf|s<?J!d5x^<Dlxtsnd}@Z1@$J5Rz6vVL+_!jb1mm?l0bE8)^Je0qjc&+zIQZas@%|0J!%i@M9<@z%gh0~V4DkDuZ4uSq<7e}?nV@ctR@Us&UWkmfUs=O19Yb^IJ<73#|MGll0Xru#wG8F{&q!{=F&^>&u}eG1RNXjN1AJmWVYs6e_%PDYR~k~S|$7zxo4WQ;BuJpV&JC0}9Pg8yZdtCx+7W(En)C<i4N0_z0I9l}He`3@l>f_}#(iO&%1z)4_`Q`bihpJ(BjN!JuUL(2nc{FcSbOfvsTwwUnGK;c7JhGyZQ;a|_|9H~1p_bdAh^goccBWo9SAP@q<SP%sf>X}*iX%INi!aS296LQN%pP?CYo33XFh*(lme8F6j(S!E=A|}OGELWx(<iACpo}o)3`R+}cE;KWerX$b2Wa&t9g=7XYCV3X)U`x$nol%ai@>AIWxV=&4y4MeqNvN9SS*(P^@jP8fCTB60>@l2?A#jpK|7rUzqW>f>S<cI-OG58N=w{~aKluE7s~?r;ZTsQ#B5rljkIJ)bMX~JWP4Q>Noo)wip_0PyTjU4$EsOjBzZ5JtVoYq#8M|}F_MByZ!mG?;bL`N0yG~fCgq8|h9(G^gJr;NmXr$yt`bv}hV8VZph{01pD<v=DDdeZ{5YS7>i+Bil14yRiMW{Sixeg!0tA=(;#tc@*3|3w?H7Q(-_YD=5yvX5bmG9wC!Usc6B|}doFWa>Jk*hc4>W2#K!9{a$(HvO&fwdo4`>SE?fkb_g@BW}f{T6KR&eNgt_KW1{5Ucy@JbjVW;n6&OkwYE!*CKiLU7ntoe96-xwU?o_cOdEqqW(fz`l0lCWa&qieq`xKmVRXEM@P)j5p#6J933%7{{C(9cRKW4|Ck*yy;G?K{dY;-*C+7H(551fn}#n~<<8;sASS<0-<w-uj{N<|-;ezL$ls6r{Z5-{!CDh-rcHdRPn&5O21A=^0jOVSGeO;|)Mi>_>7ujdqRq6(rn=K+T96OiX)`Ty%d@O<`p{-tWcQ)va*>?jqRq6(16;J3mQgO9Ked^bQ9iPMYBMd<`Cgl8!65`4FUv$n5`QG|uav|eYOF^Re<blo5`QG|M-qP|@dpThfbdZeJ};6m-zD(;J?y&e6foT+@cd8g&q*#>)dW5-vfGtr_XXmz*Jk$x6Jv|q#U%d}?X~eHf#-kXlp>8;a-b14W;x8r@e93Ki?|5!5u(bxOqXVN(Q!-XErI8ME}sc}UL-p&6L@wjG7N-E;8>O|ZI`d|O#;vV9E=2h&2q_jB=GSB{?J`L68Iy5KN9#Ofj<)XBZ2>A6L{p5gq-rW0e+vqBipvx-;pivQ+FiCm*#gumP!~&CZwt)sp>551iKPb2sDcu!HZiq7X$|aM<gjJ1`P;<286tnBrnAzFk!NQkeAXTGIH2X7!;sIhC=yW0>2jc8h!t?$UMEwg~Iw<&brE1LVznj#jnIG#@s8RpPrV@pM7+~(<};jc<o3~39a;m1XU(h7rf@JlOFH-b7FN_FDU#r@p_q9rCA&<o>S6V8FZD5789$4#Fb>Ib%n(+)XHDUf3Qu@@-g`-zwPY{d|>muaJ}2LaJIM>myt}dt}=-_%XM(WNYg+5vu+cs{2%-YQOHJsS!F_f`vL9@vk|xiNj$`?p<@jRYyL5Q10u&t;`!nFw;5IZ8mx&`u7jCZ$qwa^Bq1S7$}YKzM2x&;@cf@6gKx;-4_VbCgKx{=alx}Pc&h`R|I++**}KRzv0KWTPSa}XH04$P(IV6oN!;&rnnL2Lm&9F?7~KDg`-p0*Uf5)+;;Ki=ex&S2%6?$(2j+hC%p5&4FO#qz>Z(V=en9RA<bFWzNB(}~@4s~Zo`IjXK<@m3<(j)^z^fVXYF;I47bk)Pzx<GHXlDd;736&uR6s5*k@qaP>@1lBHt4#2cG{5l|G&NS>22c%qWE|5*@xkdwY%(1H5Awg92v5ENPt480=*?j+Ed~0UjE+Ns#YRbELyZ^!9xT&;&5j<{PXz8nQ_I5jnfa~5%cb_whm$IB5Yya9oE*x+7fc-59*yTI~}2QM7_H%Wkglt{Y1Sx3z|n^6OR-1?yN|z)#yOIJL{51RXU^IqaM-g<26{MM?F!v`Hgx{|JR>V@9F=BSL%J3coS4%?uUBsh$s0<z2E3hB&4ziFxW`cyG{%g+*OJ7G_qF;>xwFR0a5RaH#qt9Exu9jy(Vqy><`p?uMf=zv_-Gzu!wQ*CjzlvsrU2;PgQ*80{NbPMIG+>#K9->J$*x#c`Odc<a_#4zoMAV9ste_%hzK0mRhx8`G(~imTy?TVflvT8yDZW_{POIF8;rR-&<PM{~dmZ-GJOU3nIy89Q+Q|!5u?l8571B{0`Mo!tXF3;CJE}6S|nohcF<-CngLr^asob#0R{`Fg*-NhjcO~qzB=9iQda)LkJH-_Y%1mwga+*u)PHAh3Oz%FVT9TIK*&7{bwqe3=FeDU|x6)Xbo5m5@*0^3^H^ohpCgTp)+7J$cq7&K|%~%gaYU+0M7#WECA5b2aT$^gWV3PcLEqK0MY^|EdbL3I4uCw0!S?Y)zSwN=~YODF=`;DcOnNyAR7-i2yqG`0S5UmNPj{03zA=u`-0RLB)uT#1t~AcctOGo@?DVWf<zbOxgf&@2`<QQL3)c(OCsOt&Z%rNBN3R1kW74IA{!IQm>9-{FeU&6p(h9-L7)i2LJ$Ok7!ZVhAl3uX9f<2dL<eFy5W#`C4Gpz7)ZS2gL+uT<H`Lxx`@f3XTQb##+8b(bsJ#NUOaIkS1=>fQ*3Lour4*`!ZX;qFLE4DVMpOr)IN)%Hza1`dIK#;oj$>Zj-f(!s-wh`>eB5ws!><izHXOC^Uc-3}w>2Uy;IxLj8s2K727M}*UIec+4#jaX!=(&oGTg}Ubi+Lj$25G#@DIa13{Ntg!|)BmdyJFm$tO%lQ!Jx#>bQ)BUO&(j(p^W+ETfz(chku-%P5D+-E^qTGRjeM7v*inG8(~oQD;?3Ov@4))2ndy%nbrA5O76+8v-1<aX!Y;*mSa$-j_oy&a^nv;slFxe$MrEjvq&T@I={FhLvSyTG>{{jeiZcpQcYu74p97E6lMg{-t(K9f3iQooP~9lm?|eX--;`#-uH$rkr{if2ESCA!$dNkyfM;X~R??=n?5ls+Vn!sW+-Ssz0hjsz)lTFaCNK)OqQ>Y$J_*q_L4Sc9O;o5+kLNv6nP9lg4h+I`wxXnAuIsgw_cy6j~`*DyTkCeW3b4^?~XG)d#8%R3BV#$O1w2f$GC+^^}`_Kq1x+V*#*kocvV}(7opJOdhxAJXXVvhP58WLeKNkHy-c$KmExoGTR!ntufo$jaE(+X0|nETVu90W?N&nHD+65wl!v3W45)Go}pi9bE(NXWh_)i3>LI@vPh*5tR$@fAZX=i<!I$-<!I$-<!I$-<!I$-<!I$-<!I$-<!I%TRyb@K9$PkQDx(5+z>|_(V40L8R;8)O5oU8zl4zC2{@u8zV%$@)UXvjb+*2{)(-`+tj6J+@4aGRl7SIsV2<o3~>Wy8!v8}g3(<v1U`jraQ@41JA&Ti`T(wT5GM$8x+H3K8TMI0l9jIqHtcK8Mk6#x+e32I$J$Qbu>j4i(r6UU;`V5bT|Ne)bMaFPR*9HitxCFd2KS8%-oaLK_-9z@iLsS#C^#y~^z)kwajT5U+aA^C>nYxwu^&(rVT3v|{&d1p>%ax8K04qnPo@6M&mzngidH;8x#LDLs55%11C-OzkP^9{{6G~dvCL-YSEnt!>z`u6kZFW(ZN|LySY>ihNk&F<sX_1l*O`oDhu^_QQnzDu@wxz3i{{qW)TZvXVSeV!HfeDQbd-NR=0w0~Id-f!j-H+hNs+s*!Vw^={zpYFDgGl^AR;&Jo5zg@rE%*ytKviF}pt<P&7@}-|1w%g~s`^~w)m>2lC-hJ3VJ#Tk&W#YW_Q4?mHezjD*uKi~+Wg`Sz5UaPuOe|}Tuq04rlbJ}_FiV<MS?8p&as~?Ff<)d%p<5QK9xG>(3ziy|C3D6KenBR0uhp_tt;x;=^HvM<COK(=ieYswQ5abl#1^b}L9%*$ok?bg*d>{~)y8G1TC1H27OXaxI=n~LUS2F)7+-x!U||9rN;1{fIg-harm<MMX5Kq0Uu%mak%ATGGv1LNIXiT=P`YZ&%tXqz=t5blY>lofOI3`MdHJkGIxkBUZPMM8h4NPE=8Da0u9(oy1oE~yY2{O?>gnuMuzI|l3RW2DOr&N7Iu$AppJ7q1V6FLNb5tmc7~(?df}Iu~urP*(ved#DT6k8@Jd5S?V`wZ(l*iD*V~S(w$Cuv$UEG@c')))
_ROUTES={int(k):[_R108_DATA['actions'][i] for i in ids] for k,ids in _R108_DATA['routes'].items()}
_R108_SHOP_ROUTES={tuple(r['shops']):r['route'] for r in _R108_DATA['shops']}
del _R108_DATA
_SETTINGS={'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': False, 'front_run': False}

# EXP241: fixed two-policy choice, learned with five whole-team held-out folds.
# The full-fit tree and all five fold trees use only first-two-shop YARN_STORE count.
# V39 handles yarn-specialized worlds; EXP240 handles the other shop combinations.
_R110_OLD_SHOPS={('BAKERY', 'BAKERY'): 0, ('BAKERY', 'BRUNCH_SPOT'): 0, ('BAKERY', 'FARMERS_MARKET'): 0, ('BAKERY', 'ICE_CREAM_SHOP'): 0, ('BAKERY', 'PET_CAFE'): 0, ('BAKERY', 'PIZZA_SHOP'): 0, ('BAKERY', 'SMOOTHIE_SHOP'): 0, ('BAKERY', 'YARN_STORE'): 3, ('BRUNCH_SPOT', 'BAKERY'): 0, ('BRUNCH_SPOT', 'BRUNCH_SPOT'): 0, ('BRUNCH_SPOT', 'FARMERS_MARKET'): 0, ('BRUNCH_SPOT', 'ICE_CREAM_SHOP'): 0, ('BRUNCH_SPOT', 'PET_CAFE'): 0, ('BRUNCH_SPOT', 'PIZZA_SHOP'): 0, ('BRUNCH_SPOT', 'SMOOTHIE_SHOP'): 0, ('BRUNCH_SPOT', 'YARN_STORE'): 4, ('FARMERS_MARKET', 'BAKERY'): 0, ('FARMERS_MARKET', 'BRUNCH_SPOT'): 0, ('FARMERS_MARKET', 'FARMERS_MARKET'): 0, ('FARMERS_MARKET', 'ICE_CREAM_SHOP'): 0, ('FARMERS_MARKET', 'PET_CAFE'): 0, ('FARMERS_MARKET', 'PIZZA_SHOP'): 0, ('FARMERS_MARKET', 'SMOOTHIE_SHOP'): 0, ('FARMERS_MARKET', 'YARN_STORE'): 5, ('ICE_CREAM_SHOP', 'BAKERY'): 0, ('ICE_CREAM_SHOP', 'BRUNCH_SPOT'): 0, ('ICE_CREAM_SHOP', 'FARMERS_MARKET'): 0, ('ICE_CREAM_SHOP', 'ICE_CREAM_SHOP'): 0, ('ICE_CREAM_SHOP', 'PET_CAFE'): 0, ('ICE_CREAM_SHOP', 'PIZZA_SHOP'): 0, ('ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'): 0, ('ICE_CREAM_SHOP', 'YARN_STORE'): 6, ('PET_CAFE', 'BAKERY'): 0, ('PET_CAFE', 'BRUNCH_SPOT'): 0, ('PET_CAFE', 'FARMERS_MARKET'): 0, ('PET_CAFE', 'ICE_CREAM_SHOP'): 0, ('PET_CAFE', 'PET_CAFE'): 0, ('PET_CAFE', 'PIZZA_SHOP'): 0, ('PET_CAFE', 'SMOOTHIE_SHOP'): 0, ('PET_CAFE', 'YARN_STORE'): 5, ('PIZZA_SHOP', 'BAKERY'): 0, ('PIZZA_SHOP', 'BRUNCH_SPOT'): 0, ('PIZZA_SHOP', 'FARMERS_MARKET'): 0, ('PIZZA_SHOP', 'ICE_CREAM_SHOP'): 0, ('PIZZA_SHOP', 'PET_CAFE'): 0, ('PIZZA_SHOP', 'PIZZA_SHOP'): 0, ('PIZZA_SHOP', 'SMOOTHIE_SHOP'): 0, ('PIZZA_SHOP', 'YARN_STORE'): 7, ('SMOOTHIE_SHOP', 'BAKERY'): 0, ('SMOOTHIE_SHOP', 'BRUNCH_SPOT'): 0, ('SMOOTHIE_SHOP', 'FARMERS_MARKET'): 0, ('SMOOTHIE_SHOP', 'ICE_CREAM_SHOP'): 0, ('SMOOTHIE_SHOP', 'PET_CAFE'): 0, ('SMOOTHIE_SHOP', 'PIZZA_SHOP'): 0, ('SMOOTHIE_SHOP', 'SMOOTHIE_SHOP'): 0, ('SMOOTHIE_SHOP', 'YARN_STORE'): 8, ('YARN_STORE', 'BAKERY'): 9, ('YARN_STORE', 'BRUNCH_SPOT'): 9, ('YARN_STORE', 'FARMERS_MARKET'): 1, ('YARN_STORE', 'ICE_CREAM_SHOP'): 9, ('YARN_STORE', 'PET_CAFE'): 10, ('YARN_STORE', 'PIZZA_SHOP'): 6, ('YARN_STORE', 'SMOOTHIE_SHOP'): 11, ('YARN_STORE', 'YARN_STORE'): 12}

def _router(observation,step,state):
    if step>=144 and not state.get('day6'):
        shops=tuple((_get(_get(observation,'town',{}),'unlocked_shops',[]) or [])[:2])
        use_new=shops.count('YARN_STORE')<=0
        state['expert']='EXP240' if use_new else 'V39'
        state['route']=_R108_SHOP_ROUTES.get(shops,100) if use_new else _R110_OLD_SHOPS.get(shops,0)
        state['day6']=True
    if step>=648 and not state.get('day27'):
        state['route']=2
        state['day27']=True
    return state.get('route',0)


# --- OUR TAPES into the V39-family slots 0-12; the EXP240 plans (100+) are the author's ---
_OURS=json.loads(zlib.decompress(base64.b85decode('c-ri}TaP4H(j53-_*@U2m&&Tzw;nRZAw;qWvbhPZ&=`Dxv{+!FefW0Y1pW8z?#fF<xVf3RpUCbRQBPCTtjaub;#}O#&CUM%ckjOY-~RJ||L*_%w}1a{|MlNL{rKH)@BjGYyN?gw{a^p~|NNK#_tQUo`tiU0+rR(c|Mma-^z(oI?r(qor+@tR`|A&Xe*fXShwn~*KfeF;znk61hvYx)-hKX0e;j}QdG>D~|Hs4hJAZxs{lnk$FP;B6`L@T;|K;yL{eJw;{o(V+y#Mv5U*3QIg705X-#u)@KmYOf<MFr8|6wueKVJWwkNVT({q+5R{PVZ-M}7XF^K9N8ar)Ezx2Mm%_@?VGz71vem6MNS-}SdYfBN}{e|-9t4}X4sbmz<7CUy2@i%*dc`1AYkkLdZbg>;Ck<<q~Z)w1{^JgU?2j}Kpd`2PKJ0<zIOg3&xKM|1vM_l;bKv3#fYKFfB)AIIYlpZ@)q<Ik_Zg4Mcwb$q~|CiK@2*H26SWwB6JeuB;N2`(=gYyvR2%afeme>ncW{OQX}aK^g<;|&A*51+?98_(^lZsWMTcxzAA#^cT3+rpm>^ST)G_kR1G`Sh<m+O6JK)=Q4R^!9d);XcRFKKn~^_O0epxc#^6P&$9_W%9x#oj+jmeV1DaywuBqJ{>`_6V&&HmlKy#d?(BAPrvp&&AY-hv&9jod-2<A%sY6`Y~J5~yZpt==<Gfdztvw$=3DPd7JbAA1QQGH)jLiod7<Y4sIM(d=<Tze2?ba0(1b3(s`SC+;}$=(!q536XF<IV7QsynUZcK_mIH<V6gQj<9&W=r|2N}P;@y7z+w*^NKIHZ1pO4>v_{V=Z{{G>opMUy4mPg$6li)8_atx3<C7*eTIu`#7_ucvKp8V>=CeKWlE9Llp`G#*-=`wzIf}bpW&1RQBY4X+Jk)5;VvKwPQm!6}>1LofoX0ms#+&<<$!vy<xXuQ{x=51}QJlfmoFmhHW`)**Jlka+;ud>GNGW2d%zUkr{{$E3>-}VoC1p<b{U7~#QzNHYBUSsj<WjQ~)xUyhT-OKFz<fV_$H1>INU62W0q@Bali=Z7jK6^IL0YPatL6|r;T5GwIbbfF)M?*$BSo!b>VF$y#eBj^T|Ng)C@C-7`*HzF-zO3oK4tpStwco=89&(ad86yuaZxHm(?tna)%HKD*DfYP5v&16PkY--i;YV9znb0#B;D>Tr*#`o&|GX%S_e3Tjj#CCAWP5xiM4}Ly?8;Dtj73=O$oi>tapcj6xRC>fU#KipzpHqzt@S+!CW;qK_CxPAfFq-F^Ts)k1HR40?2_qSlImTA>|9~d=&oB(1wK~ZQ+!5z&z8~Jc<oKAV)(I^g>dsKV70{CPh_fl$88Ak7t;xDh;`!<^la9WDTIuCf$B@p`)r6BwgRD@|5d!U4I-jl77>jHmMCxPJimy?mtYdS(-Yjl-x$}gYeWz%3cG!7N*R)$Z@-(%<bpyZ`L@Qj527~Xi#lOkM))a*b&uZwaT<;7it*N+!>m?xb=|!diXkDgILCSMrWai;%4qAtBzer*1D(L<Epd!e3<5xqMqE|CT&{BtLJ=NStsKzCNF*zpbOID~jnj&mTZ$pc$MucUnp*dm0AK)FCE!6G)?GidH;JmObSXI@MBIbP3IY7Afnp{BF2NTWIFD0&WuNB`ypF;bo`S%X@#6+&pM1{`zrX%gjZ8oa@Ysj5I1oBkC+~i}+%{ton0`Hr;BTwy$;l^!&q36i1?Rk3{sTwL<>TP<BnQt*kl|42?)t}ZipGP~jPYb$ZDf)WHZmOXUC*I76D@eZmKJL|>+PZWa!U68<nsRG!|(4;e>?vE`+ov!8)XLS`^Fv&pcA41SKx_7xO4LKUMwF+e7#C?z_@<!dZpD{+|L92={v5(DDD%vUuD%>!HZu7WXV~&(?!q=TNt$6L@cuv>Ys7vg*jN=hTvp_W0yS77=f=<)b`pL>$uWLVG%|O?0QeR%+{RV-a0IrNb2-reAi3TAYGR>*!6=`kmvzM0_aqz?ZfH5NTZ=ThirO0hR(^jVPn_;W+eVM_4v1#_Vx8=Fc5IkT_Ec7AK(E@8m4fRu*~?$pz>7c+5-IPMEOCr3E%#j-na3IZ&RN<ii(4-ACS}%I^_89pU;1G{P9PNG9RiLpe#gkahoUY1d@^5&IWUhvOteBNX)ke5r5Xr{AJBmxcN5(A%U!NVwBmHv<c&Td3m-vm1eb<oZ2`2r#P*&{dKzTHpaApW6Pn0G@8_x?aDO2i30_f$&$!#L^Y_X6)eGN2m6QDU*3OswSXP~_tWx+Y-82kH}E;>W>)7Xdi{$d(@ZiRFiGSAUb=CyvLuuTtu~d$@4SjfcG?4!hVf{0jiv*TiPNLR3xMW_biP%0F85O`%;XI+UJ%*lld!gyJF+%Un)>=|q9suIlI(z8xK?(BBL|#4i15<c$y@i8r_H(YCDTG_{UwLP`%vmcR~tFcbKxL<`RV8X_-VS{y_<^q(5RQ;<XsN!^anPux23n)R<sKi!+lEhdZt%^IF*Rf&@}w|baDRv`k9UL?qdg(4`FxAC|Pi*$q)V&i)yZ9-b#>s1kEQ$*O7+<_1txFtIJp(;G8&ezm;zgh(-TG*FNLRlTdy)0gW-VoYQbSFV_EM4|`cD#SA@ieKO%OKeS4C(*eDFtW;U9%QIet`SllXJ;CN=b8=gii~R1Eh^ACU8U3MaN^IDeaX786eyso?27<(U8Am=LXgnG4qS7*Yv!n4*-7y_$u=MA0&%VjS9LzWh%rM<}Zzlq3xJ&!;z1l9DNuGQx&*cT?QS2yT2^1R9;-aX(uX9|q=|{e3SZQOd0xo(Rl}PmHdMg<I$tg!&l)gUSN0$Deo5ttt_zG~>DPfT>^l6oj;0UO8ppr6sHAC7K42A^%RKD3!;Jzus2|!$vWRrwWpX=tB9Y^I15|BHE4%hOk1DlEy!A44>o#snVwsl4#qxDO(DJN81Hf1e{S$fZ|P4FMDn=S{_o4gnf%1_4(;PE)MrBPg?HT2cD!t(iof4eddR{lfY>iOm+V!~PR@!+RFm;JQUb>3LQ1<-zw8BWuq+aJe5M2RY?Vt)nl$I|C*?8`XHt?kV5Bj@&yTZy*^FeFn}xoa^eD;I;Eu^@c$lm<-NC2ZRIx@!?OiMcQcA3`hG?ZvaI1TTd5IA(yJ0A@5I2|ArG6(8&E5kAv0J_R^PGNoN-tOV@C7lo&?-7iR*eL6Dlpj<K=i=^>3YkmXtJ2iPrOtmw6ag$8x3^_B_3@=5K;05_#X2OS${k}Z#_R?Mw1lp~&Eh2jczhX=sz5eI7*Rh81aW0d)c*8`QI$H~FM)sH$;~k)ll4RNLHU1-8pCAkJ<hej6B+)FBBzc#1j4PVy-OC#U<W!JRNj-BIK^A7jA~vI+5R<2>PVm?-qTYj9T+mU}jNu2>f`#5z&|xBFk8^spDY7%;zB2~0Wqj#naoCfV9n~<lTckjI8ngfSR&=%}WISL;w@Lz)?le#I<_uPQDoH>ZlO&a$MqIO)**T*DDKHM0uc6rDkSr$17wB_W@k5cF*gmb#UzKEggB*BHMc;EFRKDomKH}M+pfK$&7e}kEDOQgLtrv=hY#Qw_F`_)*jVF9(PGe2EKyv7MrLbw%$O|tLHXwsSwbl#yD$kG~&4-Vz<*Dw5vgVh2KbX@Mu`EDYy8V;M>rTnXJ7X5{rNAPB3e~&5$~>y9Vn%_<Y@sWtxaSfcXeo`-oh4puVVZa&!CpL<f<Uw{HRU_6b(+OrhFobXoLKw$s-DILEQG2h)p>cBFImfh$j>jIb&;`L60YDSCGCrE&`R4V97};%v85{ZG9hjfrlvo>zW#BvR7D(-H~ABg*YkT=b5qv^hWE9e2Ao6=G<mCn6=;y|m<ZODGUnbUaX?87_j9w37Jk9VMqbh$ZHOGz+OJiOB>P=_H2@_R#S_>Sx`mU{&XJIXm*J(6Wp`vyC}G*`=3%fcm;2{Ec*W7;?x+a42-C7DUv}BDzz&W>uF|#V$mV0_I(GZyqzy3)m`)J-1NtFAP2cR+zj#vaiS4)V5Ir3n*t7fzy(@xeqU;%WPZhQa%D~a6DVLq8JS^v@w`3o!yTs$Fy#+J!q3qUzNdLM#jeJ(8a)XGlvLce4es68M-@h)kpk(e4>0RepbYm|g@#S(ai=p$?nls4(QBfw)+@suTYuHxasvxc89iRyOh|5$fJkanti8kQdBMtW_-9PHQoAkgj>Pt6%B{<`62jg|fizP_;y#TUNPe7A_FGGE4cVNVqe|gT^X~;_Bu=5u*P*PLZx0zd^F9GB#vEG<;D@PIL0RCljB>9V69i=Ev23Y!`<<oj)s+V=~183b2cfT`hYAS;l{u?Om=0&twZ|FMi*3J*Lu2{(_3Acto4w4T0?GSXun$l1V%;tjTvsIuiSKB({SB_SdEy_bF>7aHM{)M?06ovC-5#nu1x4J~y)8d?-u;7N*N`1SW)g!y&a`H^CnokMXF&DjEpz_FFbYSs=s`s+Wy*}W{qDzjdZ%+b%a7U?j#3FU|CS)7W=qTPi&CU2S;^Uodqvv(Dk*TlA+piO4N!CnIPy=%p88fK!;abXTl4bZ>e@?$q1LTbeM*zwL_DQC1%GJ6z0P3%r5vbX_P%V;5)~$Eu#iStRE;O$&-4BE)f$5MGGX@H9-@bVAN&fuu%q|l5ZheCu;GrbYu&5&6Fsva_o&3dUbgC&Mo|LsWw8~gkv98}{!&(<`4Z~t~n8(D3d}3K=FXHU&(~fzP=3oO0E@I?YUubAyXt9C^vs=GreW7czx%K3O(y8J7Wk6$aOjh9}jl=NapSrhpY;8Hbls0mk8bC#hSo*5Qt;=FsLRHrD5!d0yins<_4%AJha%i+jYOef-u}w$MhC2W1aQFrUEJ$}@92m`6Lcd6xI!h%nrua{#ti>j2^g71)6Z2ZY&C{Ei$i+}3ZctV8f0JD|Np<Pk`BBL?ytWaloy9bFaVH5?d;mHMVg1Gb<nw#s5(nuF?VF2?pVK-<H};~EVK2Bfi7&b{Npdl<^8tGSxv@DBV4n-%&|{01@r)vO=ccsIF5^z*fi~|AF+|4G=73}S*t6|t`8m^!s!*;X1`LvV7EYs1r@HAepgG3F1&plaR}Ut|UW^$-w9rI%m-Pmq4o_W9`2*1E`#W8Jzp=8`Gu>6mEbU5?+9N6Cw1Hwt1)6wdOR$8536p54_XCp8aIAMg5D-Tap9D~C9n{58?P7R~+6}Bi*2}5@Ek^bI_**k)G&DRqK#`4TQEE0w)4`&~E^+LM$NP+S{j7G;eI*lKK*@=9`F!(Wd<)j`eUP)vFJYZfsP>YLb6+M5s0K(X;X!BG$lhxKEoEqn9+0er-VCW(*9f9WisO_Jyk_NsxrxV&yvDV>i0CDt)PlLRwI+-8r-QUb**SNCN>k}w@2yW2u)G~uHJSIww2is#l^7D2aATB{NF~Nvr8a)TPGO}P%8{tFfpNALU{l&f$N?dp#L@{!m(_`_X(HIt(6Q1aMYG_$iB?oHL;CU<J#qonShrWHYc9)DoR%KEIjJu1gWP&dFOzpN(0*LfrYiRetDf2ApvBoVU}~;PNVVQrdMuS79#+Lez9B6nl55tqkQea^kHt5wu~NqBW39rxwqvRJ2zNkep0NE`*dg_w0O)5JX;t=!qx(QhX}(`W&#t~mTdIH=B$(CU`TgZO;#L4>ciN}C6{RWo`@B=VV8Oj@Ht)f;$sU_3?I5jSi4%$f(@x&M$|>T+$ZfHtUx~Ykdi4oia1jz?@RZTzNGxsga2PDkkiTfDL=_G*-cD3c0*Rp0^7WQu9GaGGH+@U1DfnEgk8iBd0Y;u;-_}xLokRepfu#+-*j)AaSVBWqpIN#u^9fg`kVOU#k*m<4uy{}fijMCj)kWcLK6`!6>L-J7EvspAogE4V)XYxMOOz1~;Vl55S013A_$?rxc&r3ZcF~BZ`IUQ}EpN}5HoOht9v_}j4)tc1rR*9?5*WOFoyy6ul89V{MU~C;y|XomezoX_X_A#~0$0UYrAN|d6%a~pHl0BVC$7S1t}97Posld0>~%dAjlApt09W5uMCSRLp0L=6*avIK9X(69HXrX!z^?yMA-&#L((Bz}S-shRMN)QXMh1)lD*MEGuCayyPNVlNxyW2iao+MC6gj=pEt4i{DrRw}Ez{|Cn)<b6*@D^iq>6H(p3t#|JEpzw9^*g;n#Axe=H5}7g(89B{Nrwt>lnNN75t#bqD<GQ61^|JC{NIu3Jat|z`Qtt=!`&*;fV!xP}T~Y3GS>Dlp^L!F0nQb^D4G2h3@IN#b_`EzQSko=hlF7+0N$zSjLX^r}+6X#bOJ%t7*%fuK|#y2=oa_1v#-eS;nN{5SjJG*TxW}$+MHkc<Se^AoruKR=i*?TZkM`l|X&+z_!!yUV9NZ1Wcc1ygt1C8R=FRF9lzL=ZBwu1iQ@Ano?d6CG^xPphM)boCXaPASUl{I$d1%gCbQC<o<dU|M^1z$|ZXjWdpf#WRq-W58i<Nq~fS*6#(d=t*8vLSVUkuUy=OTt!~)YhWnFg&0*6Iz^SYf^A%ABF5Ndk;CB9W@sDZa1?8s09r}{1BAO1Cl!VK!LY6JV=f7ns4ggWAlvthR9!4YD02>rNE)~pq3w9Z@Fu(#m2^1B;Ra5Y#BBGHMo&}8X;#{HTr;sy)#|W8^e|85<ZwX_87*M#3_}%5UAF86rm~L_}m0oacJANdMAteNdsTVXdb}H(2GNBsSJg#0XOCa{Kr=soA$m)dPZ3sq(z)W<-3XD({szf(aJP+8)TLI2HNpS@n=2|s#M`oiL2J<2+Ud{HI1eTcw&RsWZag<O5JvI?tZ2%_m_g-Yn)8Bpk=nK~9F7d22WV%+^-^^uY4udvQCHTf=@HkB9a`8Qmy{OE_^u6dOSWghm9jZNYhUP=Em=8MZL)~@+*b1L+9h|V*pAVS$8VlQ$+;zLquylwNhJ&HefI)Sp(7-#!DA4W)gN?q(i^<eSqt1a2W|w1f!86%O?)n@*6(s)1p$wecDkPH>YCLN4NrJljqB?h=psYYkIZ+H~?nnGjq6f&3j@bV(=Z{#uACDIO=ppdKhip3>LBp*Ko@jZg!&76DpK&)DVhoQ-lFwwi=KOMBABi=03P?Qb`4uBAICmFtgvigQeWQ)+Z+W9WrR<&(U<oeCPC?zT3`)3-YaPPmD*HLB`DokWa*_xp8D`O}3D&y*bEYuYCj~H?owU%Fjd<8V6vx0fZKlw!=8A~i-zP!IEa`gy+>@#zpbT_ss17_3D_gIWwOFNNd|a|akYe>rPmnvdH!X>qvg;X7$7~I9`?{~4P9DpQ+C00pl#;@ApVG%<ki0aVchJK#i0r<3SYY@Q-a5Goy0|CeaGfDlV22Xcq6<0f`hG7ARiI7Hv6@n$w2E2}SGT9q0HtaP6?60fwG^|VE)Ow`S61piU%~~U2zC+q;3<a9C9+c>(NGd!#K0J?sLD4GdY*NXFYcv>fM&LLW1RD7O-I}mr4F)^ab*5Ioc|L4qa+4h{^VA803>aS3NtnfYXrDEq7t_i02iWA1=#*>V~Ou7Nvb%GQ)+=zL;4nIU0G`CGr^HvfkHGtF$?dIMlggNi@}fZQ|T6>%{d^3Ww0_x1RX`wL$PlH(n)=VGBDMmapYbFcbagSB7shS2PgXQLTQSp73Ibn>=7!#=BHPzyvrlMqTwKCwiMnhHKVb%*2S;nVaPK<Hq|pbJCRyKA`g+!Ted{EMKdU8fPrj<eBrdd_8vz~m_eO9<rHU)C%=g`4r$5Y*i$Os3Z)TP4TF^h-=5>SBz$+&FhWmeB~_BHok=}eNwyzY&F&g^r$K@yokV8m_FZZb-P+qm50pT#-A0?{Zf3WWZ~_As2@wUM(pV3PSL+=AGLq{<0zSHcv+g(sIP$TWY}<U3T}h@|ce`M&7C5?)<QRj+niNZ6P6=sHS%Y%qdoMv3+;3$l94FDs#*k%X=Xgy$H>W(oCin3UyJ>pDYfkL6^ZOs;aWdK(%6~FQj6?dUI=x(G8md3~zAaVCT*RP{KoEo1L<m?mvlAr(HnrZc08JVKE|wY>l#^^F?y<EhBuz{c66rCb7vrejmio40Fl@^)P-k+YsIE5|kZlnmuvwmDNzZWG7VA|P7YIzV>RuERSE8{34C`PgMMEJ$;|U;^m@qQ+19w%eM(s8V>7Ay(tPs-@d>Zu5!RlS1Z8D21T7i$#bvR`XddVN+BdHym(Jw5=aJhd)!(xS0$I~806v6`{qS7M`1X3k|os1RxSKE=Qqzid8EV9VHYidpxplpIY6v*Tmcwe<lo$Z*TkoFMr@99gZu_C7XHsq7rn%WI>Q=@d+8^#Ql<hEF^V%2y?jX}U#m(s%~8uO!&Y@1xG5-jVp#MriH5|>7Y84{!zQRK+cAt2Sxv*qZ`<}QKfLhp_wo<;gdo>YP*TsxL1FT|WT<swivR{1u9E7YSBrl|+sM#F4Jxr&PG&^e+L`;aI=WUof5RHYK~4{9Qlj5N*J>%OR`qrq>ny4tD25-lc^@cj(;$U!T9G_3SWS}UOEsQ@PlXcNUUQDotqRhHEYLGMfJt3C!ZvG803bC*VGogAA4=o2Dbs|L>tM7HH_QXg9-h8M&hsT@ZM_@^-zmsMM@X8AA|W-Nj_CoaMhg0)RjwiB0xvAI!ge8EOm{jPGEhW6Y?X!WvG$0X|mRyJ*Ao)E$G5&}kL<Aqs(EE4H6k~BW`s>w%wN!_kPCZ|_vrxPhfOK>4$$VdqdqY;vFOPs@pw*xZnBTj`G#nThB)Y#X)a+MaeVW&8=HeE^(Ad-ik<Ac2}b^@z9kEkO!42}eLPzYUUMm%&SJy0J6(nqW}BB$a?L=v!o8AL|VQ>j_6WRT1^zV|K-Sr1;%GKzH!@XjTJ*XV+@sE`gX1Ygc^W-KaSH*+x?e+nqLkL}oA$a_U=c&r!zZT4TUMToo4aA6OFi&2$b(c&|Oq=o>s#LPvJw`nkUeK?iEh)(=mGeyw0D+!@=q9IMk;(#=juv}E>+Qz;gQCn$>9(eh;Q`??jnl<R4A|e3a1hd!Bp*-1V?zhnd3I%fgst?(3sDc`pP{q4miyYRUz}=gbU6<wR9sxf5o31DBqkP})9X1#<s6P$JgwrROUIZ)jrgrHan<;?(B?lEbj!$dt6OUU$8);f3s}(&)e2xT0#bbg8LWHYcqB^b8*19Z@q$v5e=u3{VZhn`5D1?;5%jkrm9p&*$`Pw6CW9PP$ob$x3pm>3B1fsR0<G$#LNi)!ghzYMy3F_HNyNo!7NCs6@zRBMn>(P8HUZqEEF$Zmqoima7e0+IQy?K3|Vb7I_n0twRHX*y5U(#^MRdf#_L-AXEYx+xX3v9d6zJd6TswOdo?h{K^L`&LS&E_S$DK|zZ47Co`B(>x?$s}nCHqcTkX7;3yckd#q`VU#`m7Q$7FojYsQ1TcJC~XLQsTteYcG7OMj_3<wxJcz9p>Z7{7?V#hB(#ukDIZg+hGq8nl%hFS&nzY`;Lpu=YI>}ZI1Vs<%Y=x^^i{4A8BTVjfAP$^8q(Y6BJmnd=3Lx$pWhyYUEFE;&$>8Zy`Rac<dxDM*^qX)sZEh%g3Y8Xu5c#*%0v(y6#A@p(26NbyTunN;st#cQyQkDSxdvA8gcR*q=&RBh{I{YVp1D~^&p6b(D5)U#aD3@0IhB-ybq>gk`5Bp>@&7SL)@Q{`aRVm%MG9tP(koS-dxh7P3!-2PwPm%cpTutahlB0@U|YRvY(#{Kfta8pHN1-d>NNCK0BP)t2wiKP*W<M@)(nY8ZbGFm>WQoTOx(rP-AuO@#%RH)hT+UL&;X$_c*i<W=-601EWhqGp=jG(;c;xdgfx849zn4cPro<Mo+kQ98&tVuJY?XN$&X~|H6HFHc*bX!xGE#8B3eiV@{qS@1a5o<l0u`BAOv~<WEa2S4@weyUD1qz)-?0TW5#^jImj+zXbTT9sw$<lyfd@QOfz`POL4AC@soKS5{WRW$wV+0WgBayMjh`swuH-i#FNn`c$t#Jg;wfmz132Wx%bWPyiTr(B-!ZTryqy*tOf^94kfje*6U8+98)<c<XNYQ{6d@zAMwpqp45C`db)%M!gQIdE0h>1bg^4DUr`YY6C*+#_D+5)u5*5kB%@&x{7&WeV^p8tiPadoU<R%(I!Rbm^hlYwKmVvmNsFAujPVxL~=#BBg>K*W&6cgUwPX`-4BKKf-!W&h?4lNRiRN*1%2Y_am|AY2d0s<78<+rBeb%}&-d5!$BK?Wt++D!gk$I^RaQk~&E>GT{4d^9<_hR2H93!M!#1SZmNwIO5gA1isYwG@Y!ZFz=KC8B5z38_nb{@CSrm}T9Wm=JJKIfzLvp4l#tzS?Wu|v9Xf?de3P`_(S@Xqtwt(7<e<imBDfFIasxzmYDj~Fr)3$Y8zkC-DZ<PJ9=fST^DszFr%s_%#&8f_7ARDMJ;8Jrk;z8=92!NM{AgXJBTxl-XX%6FR4ou&vV~SFVks|eHKC{dJx2(a$AGF=cW;2qoDCj5CUqz8M`N747QqxtIvalw#liPgNuiF?Mr_UzZh+5rCW62~(fN-ks<1V8gN>t5l%xh;!JXTw$GvfgY*qvv(!)f~Fu`5BUg@0^cP?{d6Pj;nVW!v`r3zE;kT>#bMg_*T}FSpSfoE@IO&3TB=u9AtM`0A|4F+`(IMDyj6^lacY=XBQXvo-%N#`N1R@n{Sfq!ymu+UZ`xsEn87q^xrmET-b(Hy(go#F(l!-~Sy)h{gVIxVqOiF}<;PWdq+XdH2?&sMM>!*jNlmMpzAm?0oP}m;babrDlbnR*(cn@8@wH#70wJws{gJe1afklW(D|`ye??WAI#ov^PaysGqT;kt1K_R<}q(_5z~=a`-cQ^u}0$Ee}xuD2Qiew$&r5HTZa17{1qJkpavjtDR2tTCmCm5Ua+Zhx1H-qhSu*WzglttD@`qky4<RWeCWF(Krg|G##nZWh8W29@}7>_FSt8OY&;6HO_HH0ooLViFCoodQfxBp<X-*7JN3kOIe6f)OnRZC9kp{meVFG)^_2^^IVj~-?;;)rB1S$n7NJ{dap3C5h{!tF5t=(H&;XAWwXkJ7s0xalumaEmskWbcy9if=_6)(c)ZnG;Ofd!4<HDQG67-Ju$&VqkW79rE;%x*Fy*YQ8xtdCTNONmHTLs~`I77g``o12oTjqST#x-n`DmMQELC<5vMydJQSTw6$Sk#bYDDf}H$150CQzay=?92Uqhe+G1Unx<nS8CQuN@9w4;&G{zGhY9UJ%M+vmF!#MaJAus9R_TO|HO;Nr4_Exn>Eg>={8uT_cA9w8g{@8L8srz!|5bV{H$orQ3u=i6FszIu_~#NR$>A>ktf`UAuq<2n5uUt)<GqSScm>1LQEaIO9vUwmcQdOSL4;(M0#h7!SWhmeS)pcrLYVXCmDgAs{n`kVUHS=m@i_+r$>ri2+RCnT|+CrzC9<hi~{zg+q>`zmjw{p&dC$DvVf>c_M*WKuAWs#Mw<RnK^EWpXvLysPQMSz*&3!%xaibH`QV-uUex9C^WpqRby%}Yy55d)b_ta;`w&(6-z->hZ7ZUtmN_@&dC(5MJ`mc-sQP4#jvPJVkW+o=b`Me>U%bZGb&40EtM=v^Dx_suuDO_o6cB4aE)RlUC35NF+5k|<^e}$N-*XuezJ}gqMV!n5AEt9@BH#JcJ<#a6KN{mvjO_%M$-g2@|<2N_V?iES-&-?{?osh@3imA0}^?dc*=a=0}4`oRjsNO`g^u9fjeZF$n#2A3NbL@R!oqh(r3f)+n;kr%I-pptID0~#>8@soQql8-pc1G#Xylfo3a}bj)?z~q?sYv@0;zQVDIR%!KwAmsmEghY{)Kgw&aqEVw4HdnOSaEG?w2!(wEkE?Gca|D(7Gqn7hI^-EnkeY*Imn?RCb$t>&>Zz;9)Qd5xp>_8{Qz#3L80Rz?48uHC;1)veT*7dKdGe+nW;!deI$FDP$F12NA^=(I+{O@uVqo|**99+8{d#g5nbY4ctEr`{dM2`hy{1{c*M7EL|!irLFWvpx%<i~aWV1?#+YN`2$LN}&CW0CiH&Kmb#KFk{|tx@twtt_PJ{oE2bjSM_^jd?M+|LVMUMDzOiNz3D5c#S#Y9Z3%^9hfE`<`sL**JjBb(3#t=(V#7XAU(q?qZJG5!k$Seg18sZre`L?T%x(`Q-<@w^yF-f4Y0iEqST*Z1^)~a#*=)d8itk~IdRvF4VkuP=9~Cz9GSXa}LS?h%9D&$_F{i#TIfnoyw77p3^?}F!fBW;NpMUtr_pj%>$Mc+yygzxnk$Lj!vIb7z$^nSFbfh%sr(^dph|;oLKvAG;fENx@@)wFp2Y>{%_-|G2f!nZ4Z>&O;M6^#5-l198ELm-mP7W}$<#oHMr{V%oqRo<&P;7+1Go0+XwLDNP8S}}@H_i69((h4Rl~|IiwCkOW1Owb6H5ph|;*@s5g9=F;>w@v!%k!aD_oPI7>9H+EYwA+e{P|G)%521`8JYn|E1fbe2jxEpV<;FdYnyGBwi3qw$uViEKMG%Sj73VjYe?2hjvr(A528gD1m0|-xpz2B<dF^gnv1J0y%a^D7vJhWN4@=b?F9#rh8aTf<>^pL4Q@&5qt13wR@tsUELe@)&@R5pH|^8&SArb|p3=PRCuZe>7BKe2X`ODmRQH*1YW!jLhsmszcjT8xe|gCW5TA{ki-J~{q1<53(2pN~xc)Nys9sn8{6Wd%JLW=cN_U65Lrf>D6Y*GxG9A5>Ygim}<=t`;pYPU(RJKE=;1QKIvc%9AU|Qi#v9Q7oKTcWOK#l0e3rUQ9Ac)BG^SO!`NIGMg7XfZoIWz&W;6VLE5*C}$p^ICT8DOd*stPtQd)F2ktx~}k#X_3&m--7$zgcTJJ#e8PU8ab|p=U#062u*LT**T+@TUvSrJBGi^MO}A^ze~V{AvZTWF2gW4J=%;`&z~zmM3xhk+rGX{5h8CY}Z^D6)>qg38kogQlv_yL}{RL9)M4C!>I=Xd2@Q^^}*@lcubvoj0t!IZ2gCPB8wh=;(DgFhk}~(Vl8!$$Cu~KSrkw1%kw6&A3zC&sBd2_p5L(|c`1*kl~JU924+)MSK8CP_-A9jm(%z!FyTx$UK><<c=cap?ge2x-V^d_UY3NeaFQtDUBAJ&wu>;s`Y&a@7XVU=sItjY!fd`H%!9-T#a-_$bv*z7d~-doi@yCa>e^T8rc;ff@PR2XP5`*Yzc2*VnfY&UBK6)!?tvBODE`23+vEqIoD$=@pgy_?ct8G+PoKW|^ufNy(j2I}yv$w1@GhVyc=tPfpVG@L|F*hr_UDgz|Lae`y#F$-uct}3{`H^#`1|qro7bjwWtx5dsN_HdytFUB?X-Em4JCo-=y$ylyFUHOhd&iri|AP`K1Dv@<)mLeU$&4A;G{TsJ;S#z5*6Z1r7n&JX!t}k6^7)pVJzRNz0b1UaPDO|pMYVtE?*rV@P)Sg_G!t#P=WE`C)i|{A=m_9aEuL<wS&a*0$I}t<^wS-Q0tEYKiQMD@p$t`=%M7jhp?@%UJIk$`jU$DCC6XN4B5hP0g(FaFU{GvnoGf!&MY{NpenI4?WuonPJAZsg!e$kY2Fp4nJtc7-}e05tGM;W_dL)wm)hjyOzIUU-k>;>`PRF#MimDWo4O+0WkSgdRgJM(K_;J2&|swB>}nHQkbrb@At$R@S<<A?Y7#=$niX0>w4|h@X~~EB${_?g>1uZ*D1)D4_;MV8)uuX|py@`;Om)p7x7TrkpDcXMW|u$dfQBsDs4<^Q&r#z6^X~~W**jNgd-Mv!%;k!D<6Tr$R~{`B=<+|MsD3##;-T*Bju^1>DeH_yvW5PVL#f{OpDWA-pS+bs${2*z5u9c@zagVs*3@F(Cog@3rm@d!NP~k+%vVNW)7vs;v}d!!96CA5%9YVt%e7#mSDek!kdY3y!(wE;Gkq~LGRw$U$WFej=?09l@&nlKfhk((%@||k!R3vbR`ymfRgx*(<64hxPCPH`@T0A<Oz0VG32hWU5TN~9eQsW0F~=zb5wbnL5+YFuO?E4&tG2oTdSMB1=%B3zj?Y7(vQYi5;<>ig_i+1(0V*tc4TeowP3*(cQ0jyJ9RY8OMQg*#UAuvfHK3HyTEb^;Nmtg^3z$qY)xG1^>@>e$T!Nm>S~7)@kuOkv33{ImQNvaswDZ5pQjuJIHjaqK153~6po)&>wp^BdV^McIeqAGiU{P3f&<@-c`T6#{0ZqY4k!$eU2T_~xMV&A%Bm9)Zy2o#TIE}`3#dzz^VOA@;VlEz9A-QDWvJOtd<dKJA66%K70G*hoeg|{%+A~*=4qzWt8Xw#-ppB78+p>dp<`U71PAP^YAGv7h8pi|x1IQ`?5Av|?`k^W*aw%DYxKUPC^-OW$)b1NbNM8Zxaf+|(^W1^gQTW1B5STK4+`#OU@5wm-#T4MN4`*>8bgWL^{rXKyK*f&0^y`6sL8PASc|L#s97MfI<x@+s4N<Iy&*K}ob|Ax{(%mVsD_tc>%@|KjHGOVDFdFeiJ=MZsnQnrW7FU#CWY0C)`;*Ii-iU5w2EG_$=fQ*`SjQ}o>Ap{%-izhqh!=gP>j?OJrPW3AruB|1F^c;{?pIm$R$(mA23c~J?sO6K!j`77C40-+3iZ#psD#m}ZbNXg!Ldu8XN<ttDr#3$;htE(=9*pu&>(>M4uDhL{C3!)pE(&akg!*BL*(KZ5mdfXuOaxz$|D%{-Hi+aoF6#b1)&WYfk$4Ww@p;|9SJoa$`rL_*Y~x__tTm2!*_PaZ=B$08N&pQJUit=^KXzfmn!q&({dpupIq-;&8)3hsTP=?v8?iHUcuntboJ*Wm!5c+ks**qU2t+tuUF8Wy=a+bB!PPCRNjxf@Dst45>ucW*KQ;Ntt1&ZuAn+qD+jSE#=)9&zEPb#gS?z49whPgN9$MNCm&3jjFky?G1xlt6{lF?3bhBa%cqArF+9DE#ZqPHB(`$lFuk9YscXIJolDI`ua3IXsRStdXVnc_OX?wJz|xMD2$7g(La|*!fpB%=cQjIXXm;va{if@`&E7x;-=x_UJDy24NUIg|wMu4Te!bU-OViHoC&-Jl$imHS-(r~5>jq|@8v*piZM{bCF!>T`8_&{&c&i9zn_aPO4y)GCJlN;Ftr)awuQVc38~AFi-g*4AvP>VuXtIoPnL5@XM_Lmx$VEtXk4%}L9?%q3H<8EuFP4r}(#+8SvG3^kY07W-40I{}*{V*0F?zj~5}Nh!2bCn=q_jV~O{#<?)!qT{4I0gK?WY8JU^_k(R7Z)?^V{U_F!vDby+kItlI6cnKFWy-tq?kABPj{~RRU-5aRg3rW9OkaWymQ>m|%fUucpp($GotW{;kaEc2cD~ePvgWH4&0)>6-@Iqjri0t5Kkzu?Dd}Jod_g$UQgj<$WLmNHVbVlz!$S$On}ug<pqu1tv3osgAr&r_E*%nb8w7@{MbQq*GaSEN(b9L~!@B5lU-m^6e>~<pELYu8&8pR7)edKB2Jh^6Ov)FUtO1Nb>=eRnY&4(v(J3IgVHX)~VwvESA~k>n4w#&ObBFVQVI!C&}AdnsqlNptH=JWh81{=Z@X=MG>cwnbLvv0ALW?VzT0I#ofdr6oP8Fc1BPvkNP<Yuz-hMI}6pa-at>x36PnTBf^Wwv3!|uBi>;?Thv-y1^vYZ$u>6Ox^cHIkTTT`!VtD5%G!KldV<Q#`Hg8AgvQiR{X$XKkaO*>(q~G`jh%(pX(ck#*JJMRIP~@G^ZdEUdyy9}$F7MQ2@9D@lAb%3%DU}4ALq-*wqy<<!LH?ujB=Gtxr+GKDFx2BB8}D-ZS9e18Jmi5T|tfyWc@Wi<b6)+awxaalhSC9yV^BY=v<Nul@HP?CEYA_dX+C;?qElvXcTrrW-I;!pbQ6Sm#<4WNbrdy6>Str#U3aUw#bCuu5F{)DliSxuKl94f}L&gK`_QdgZO~HEFN0)x0d^Plmg+cnEOa-fN$gmj|z`i#SXzHMKD8O5*{x#tB2$xXrcvX6?{1>cMNED0Sp1GHQLuOr0WHq)Mo>eIazbrA5B;9;@mXTJhjZh_2)QtfJa&*Cp}8w?7^)h7Rt9$qAab_IL?%$1!~2%!7M#@Rrcs=bfwpZL^l$d2yZG~!tUe8PLpJd_1YuvbQM_d#C$FNKtp`Ahz6W(tYP%B+YUC$NIT^mNUKTodpFB8UFv0Tgx8DedJC7dsbUIqX4Uvw=WXh~&D!zP269@>mU$eD7j4uzViux<tqRd!*amM_YzH-5J}~fmk%0zg7*iImLvn#jRsaJ-i$9=(m>^b9N4a=G{HY3KN8g2p%IbM=oRFlmtYfjq*!cd%m?Z>8cXG;;cq+&d&0nbZj9~?CZ3LLPH&05fN9&D)zeIlkZief;csQP(flY@DmNSXNGqA>(+tbUqAGFUl_9&y40dKRUQ28L{qjmJ?t$MKD6pe)pu?8VHQQ{A!Zk98KTq^I7I*zFFUsT@=+lQD=EGc*WhQrh@kD~#eGJx7Bgh64ay=a3H?Ed!a@e$%(oo$Z1B<~aFU;rIJ#W-$K6>D=Sa-JLx9b-K<hKoq4l&$F2@?|>;B5sjnre1d3kAm;xm%Ldc2`6NvhfYLH;%;lKTH4VK{^@OVegFFUTalqrJjG+I@UErDISWEifpOO=+K1si4wUoLi2Bj3>#u<@1&JYt<z}(>9}_m&F@3Pxp-8(IL;WLf0_-zev!3RpT;oZ+xoYPl1CMN5$tYwM4?6Mz$wk)TP-|B%L@K;J*414hk=voNi$H3?2ZIC8MLeNJ6H}gI?@fZoh?_^QK_HFG>f9~G7H8;j`_Kv&=P!2TzQ#u1-8q5>FJB*RpILi((e*%OZDreZYN@uW`V;9?Cijjo*J9O^!g*#h-D91E?VZM@$@kIS`6H^{PI7);szp1b=lVw0ktkKEo02MRXhKc>t;E$7cLMc0B$-wra9D9wy-)Sz;s{fTbycD>UGFL@r??$Feup89v6hq~)0Gh|P1+DewHUc#udO8oiyJwLK-*9#|4ZoQH?B2s{8Qa?R25VUFakuYEua{kM&=pf?umShkjPd5)08R{Svu5^at#53$9AWz#o#Fnc5Ku`R(*$Wzz4!y1;+W{;LVuf^PGZz2zvsV$5_qykknB#o<$QeM=f>*)<RyPCUC;;W7l9NR<#wo5zHod+T{ytS}LZtL-70GzHHZZO0>0=WgvhE`jXIAT6MI!fT9j}F)y#LCo`$;`V}|}2*-B#Urn8=ZNCdaWm<%+&2k$02)(x3qw;6s7{n<3zkoqyq~Re8^@dfW#ROoZ9Zj2k2(a31!q(o9KPzp9qy3lE2;Fnzbk?D~1-_^gx&_>B_SadBP{k%)jp^}R^PuyW8_gwBfS^2ctk($*Att0wPOaPftBWmfh3|Ph*((SXHtpOironn*8jA=m?R+fsYI0LMfC7vP0&0LI@*h@CId@+#(=<CZ%C28E8iX7sqy0LqGHE(G9@~PO+6&wYLupuQP|+eko*Nn@ue%PG|0|Xx%*e&noMQ?GRMf4Laf6Ew_GK_Z;BHV;@t|Wuax7JvK1{<_s2g@u612YG@_^0mo#)6AV`<R38Y};$P25iR5F-9?nkwi-@K6#xUk9^tZy%SOzltiwN4Ft)JP%?Dg!MYAulZn0V*9Z@)yzl}Z95g{g!zoYg!UX+!Ue@_8SblN7Bz*|yX6Zr=UKM3)CXC<&_OQ%8Ry7K%8|BhvgT(RLyzX6M3x}h6&~UkTNm!W7NIy1*-V5J-|<wY9JaFOyRk(&GWa}RMe=Dz0kkt)eA_iEv96BBp0rnH`SRlLze&<Om_4Ju5Ll)}byJ>=<ia4+&zK!gPaPQwoNF9ebMc86bC~4TV#Ln{H~<tsnKK#Z*i;1fcLi=4EHwifCagRxAJ1;G$HVk>-th7i$x;U+6lI}s?VmqcUke4D6oxF-yo2JRn-|C*la<NTRN^YoaT|jfNP(7CERdwRPc=y1T$9+_UVsunti5l_nT#)0skHOMzLhnS#ReB^nu4KG-hUyA%z>rZcUge4(OS_~GAWyJzOc7E(F?VZ1;c`^lt@xkATCXeV5HKl<(<P8DibCqfG4kMuDxO_Y5<)qy@I%V0$rX}sMdaJc4jd0Hgy*yEMm4@3OOZ-d4Xa=Sc+<|aOdq_D+uq!tD4)UH2DTp<P&iCWe4(Q>S(B}<yiIF%-jnpJS${V&Bo=)t#k4H-E(mW7(5nA+k#9DS;2<V;g+W72mN5493y=Eorpq(NuH-1^%m%FwjT>6R^~3?z9l&L3cr$F?-1{ZGAo+?ycdT^MXSDc`TO9%Ame6_wyi$UwrPbueeRk9zV!&gfQ>%_31Y!Q0FeVPfQjYKfY-^_S|vKXw(^=1+YRUeNJc5E&nUPMaDZgRVWEv>U(1Cxn#VF^^84j!L|7_q0_~@4Kq~URP<jGk0#L;{$O)+=mTE0C?NUmvruSwu$t*1G$vjTif?D6OT@iJ5I*jq=dR8j92K~n(MT2dcv=%H-@dqnEOjZ_|LT;1G2-QU)gW~DQQZpiELAy7}t<=uHDA9q5+Yu>C!(#@%W|c$NQd+nzv07f?%4rItTP#|}ijbX~p1wiV;h1vEXezAGnVwK1<6(lavKg)1cpbxHRX3s62R*qu9*P!zQSWc4Si4~GW7h&d&Wf;)cZWSl=xFze^Mr{q6^hoBGiArAn#1#yrjUC#`VWsrm_828V0hWvQU%h$1M{9JfcwNZpismXa?!Cgm*Vm9S;#@zV(oXt(0rblf>uT+mGf?Kp^K0^O=%>#i^N@Pbtg=Im?kT(K3h$6o`l^>PK7n(I3?#=l-n|LEcD8hA+ff7O@>E+D2K(A$?9;3KXiJ*iky~Z-_$oJ7tlV5jtu5Ey!Gav?aVAgC48_8$N?O&3Cgf3kiXW}u`jJIRfype-S+Gj%Yf(_mjBQ!Kr@a7Ig#0sNY}Kp^G@U<!<0tb>k}N@nTyW~s5fD}*3nY#A?5Qc^m1qO&s+F~j4Gx3_Khadfx9sCK!as^#LNkZZJAD=I~7ahF#_ovql!{G@WqH~AA$n*)%K?C($i3B+Y-+qyOi?f377T^pY7SP@>0CWDK1TMD*ltSj_}+TzF-uO|14b+jHVs?CPG_DU2-7p8JXh{yCMHhiy<OZ@ie2j#~WiN0esI;5XB#xN3e_sJkC!E+Q4jT2b$fzu!UbAUSwZ6lqgE#V;_Xv{ZJ~`=tp?8&ee!%WfA-IXA!g0=wc1~ZwR9sY(_7Y9YoI*zJ)XcXc1hk>sFa)_pyXbKx@xs?mr=D%vVT5hrCov3KWq7ZLTDLO;?hW47QbUPymDu24>9zj?rTowJ3$XaBlF~p;mc?7q3Fdl-Ve=xsvWfKe;0eICBYt;-}!fjS4W5bNZA+Mi~JoHr>}aHGOqRrt)%f3<Gn`e~D^F#;<VcHX8_mPC&D-s)x`o6T|5<A85%B6J>ZCG-oG;@9wD_r2;8Z7M0P(5-NouA~ah@@9;h>C&h6WT6!#aZNHo3fp2;8zAxe$)fUMz0ejS9J<t@tBa&FvhbWRW*fNO;vV&y2d;_wDXu#N}=H^H-fjMB4-<tvmR7D{%)qLkTXU_g2`J`?7@4k=~H8^ovS-9i9*_|_g+QKTJZRHt4@}T`4#>5uA)aZ1~@3ox6-RF_;Uf4oa9Og$t7DH!UitS0Egu-(y_<_~=BzwXt6lQZqX@RA6Xc`(xNX+ugD|&8o4gv2mE<j)aVq*KK&x8@ks3~X)L91n|u!1v|p&y|7M|{3K{qL+t^XX%uLdXS0Be*Tkt~r+JSe_g5i*!rMDP6RmWb(!F$xC{SVjps)PPt1VtUxK31HyTDWNh`bV%QJAzy8MWa2eBVSEQrR;KxFeHI&&<M=;D`)3_@pj!FNL>MJ@pOo&4Q{kfvkniNPZP~42zMIUHMKjRFd_z!}#DJ|WAum(LST)ooVBox?x2gm{OBDuU@;T*;7-C9hAU0Y>n<s}Fb?yDv$86nS6TtT`$c7#qeU~6n|{*!KztgGu*bOy>^6;}y}Z%8Fs$bR^}EbOYaWI7)|Do_eEwq%!b_4!?XiA6{W+99!^Q4!d%MjHva?3Y;U=Sl;LxiTG4vo_I!BvK84YCTdqXbcW?kno-JH<;kos);lRIbfzh+`$=HREl^s3$J*6#O=d%><6W}I=nAVck#8kie>UP+J=#llp5<S<ni`tN)xt;EkHHDNPzY$f(g-U))Pd^*Gy1)hz-5oo`kj*qGl!;2l!BG>_ooEX`?z%RE<Sclm-=RLXbmKyuHQ_W$za@%A2GpmAMbL9fIC6wFX80?f5m>JYYy!n7;2gYS<FXv_KzdGT$u`kV3w#^}Hhg6pS^J58{?NIpE|N`4mAO&v>BdoD4TCguh%;HDOH5$5)W80MEB|_8Ao}F|A1aN7{aDC~-iCRm_cwzY0&qJ{RPl2a90#+%Tg)RKSS*6WWa~5s-)yt#hQ}aV2gHl>m6)><@rBY6FtTHdBIhfXnA$O(3gNIk*Z($Dj_3RZ<e-CdhMl+gX%e*n%0{C^T~NELw+{6%O$MQ=epYqj6WRSn7hutdYQCgZV~FQ=&i~$`B^8$WN4JVG}5_b#pR^U(U+*)NxdD>{h&}h(NJ^F4$LD?uR9DC9x^8f_?j>&7-XpX>cx-LPfQ>WtuzonI!S>#3>DFa8p~y@PM?A`DP7~Q7~Ag2oyy9^B&gQODawDexzb$@ytRD@OtkRwUR-`L-^=dK|>Bqt##f2@Z4L!LO2m^L0B&@2zvTpeojGPR2S7861OF8uNWYcnEh}^^AI&$gzNVictt#3QI!tbi@`STT6VssQK5}4npaZBAL;38!!^HGH&>~R((+AZ*BE@}#{z0&pG3VM?91%(UY=KFmuP8@J2m=nQUzDW$oUob!g8L5a4edLTb^Ca=tag7F~}4R@SZ#rvu@L4Qr6hSvsKuu_`0PP45=bxQj!&@`l?n2E#fi`2hDGKAz|9{up?WA%ih9<XCMx>W?w$pMogt#imMcs>1dn2z3VFbDa$lGW_xA1_<}2D|2{3WpN@4UYF5MGO(@!c3#@7?YSdcNs1lnamYlLsIvw@fSBsbWfmmxdsj1@Uycij|#wg)K4bV%lp5ZQ~OW$*;sXL;uq=)wJF`Xt<7xyhu;#QQ@??fV}#m?v}a>q>>p-g8yPA|oYs?2u@plYWki4<)><LtxRYP)XBx**6)Ul2sJq8ti05ioG16Z7SP<+DB6wsoxjSXF(dd-?LFhJ%{0U-()fL$Re=*R%Gj)E#|BCc|HNn^;9QnZb!!w1Wv}WsJozojK3=%fE6r4tIbw+iz9`MP{ekE<;NW5n0-7#t1+Y91sCV9>w~UhunIxvtx$z)tK!;7+K*`;l-1LCOb7ywoZZR5g9}x1g|Eybz%8px@zGC{R%vrw0==Rd)jw5XMxZ)t+Tc~nq_h-c&Y}Ci&s({@Fi9}6<QL|c6;we*QD1?*vP@~JeI>r8qKYThJd9?s@HA;v!;~qc4Z!$uYGH&Z8SP)Xt#yfK2(iII}p_g?0kU(_0?cz9$+EHnT&yfJ|`GIlN$aWjiObjTYg}{dR!oF%L0>(_(dxyGDXf+$TdY3%O!+)L*D5X9EZ%DLqxxv)BnPnF2)vferai-V)?<VXZB#^ydjgleOL0wnPk-Tgix)W&uA#X4vn4`OMcY`9(?)+<!Nk&afew>{rL5iKc;8`)06fP@AJbPfBf-$!8t?DwNm#5xpXeYj2^e{^=omRix0r`rFd<E)>_I#b!6Uc6HsEM%Nl+P{+b?sbeaL@531<xhsH=Sc#Kxy%G}x6r|3J*O9?@(c!f-4Y9V4N4~jtP@;<RXSf#|^)nWBTo0Im@5mjsvYV`b5CsDc`3eW<BR1-JXZfT0rff~LuT+BzxSvXF$akq<550`Oq>PQh@28OLe9<t?Zm}?Gtazk!s1X-r;8C>95cgT5V=yQqbU9?HqnWrt2i6)y}Ls2Z(fb|*2s%b(uHdfx-X!*u>hs=|Yd>NMSjO8G>C!f_w!QuRrE>p{#3a4cJY6_Top`vbfc?_GxXzs#@1(-#>BRB!YQi44<KW>9|=jS89Ui}KyP&Wz;qbxV}>G;uJFdoa<ANT>lT)QwyS|?s*kDR#3D6#xwGGN;75$uSa?r@O|jf$cXvS{|SR@epc5}wOjS}hG0+i%C5IJR+|rwB0I`~%lzqC7;lO9o#p1XLh$Opy{x1a_M?`WPQ(s<xvRC~zh}I@Fb0VH!;cajIcjE#%MK%ktUi;{&h@h|DKHU=<PvM`;$ceMxCX8n$r~2Wx^aTqsVI<P*8LKEVNNcbVx1lBg)G#<Ag=AmFVs<ysLt52wP(+i&%{G6iP9G$9jSFITeFz;ct?Le2ysI*q`k6$EG{Tq*?r=Sc3p7=^>nDQAlEEFm>{VAEy<y%{puJvrp@tTn$_7Y6UJshOtwe(kZrM;2K##GQnKPqzMzdE|)RUJo1L4EnpAH>4Z@wr{q2z(Tu|46#jtVcn<<yh)k+^{|Au`Izj<68K-+vvgsY*17`Lxa{U7>9BlSi}MAp)$>0E>JQtD3=!<p1F?!nR&K&FUzW)nn1{t(wFbLNtw%d_;Wm_c{cT`@6DcFtR?t=yU>MQ`SdkzKqsR;@w&()Mc}?sBA|#iI!ePeHk}GN;7i(@-{HPj5I8d@Wd8pF<z=SyoX(e?Peyr(V(y_579O4(jtCEeaUeEwJ8KO`UP~Z(l)l#XO;y2L^sy3z~%}<l_`zyLDE(ibl7Zl>55<fu=>bW_QJ0T`Pj6TKMA}R_CRGD97NimXTnnkh}s3V-qt9Jsl6HMjj3#8{Bad~`hAaePV`Z}hsgsbly{fZ`-j127+2~_$Zl7+zqb8-x0GG^VyP#-r?E{k7W-W$TXyX8UHehZvL0XGO}-KuJfukk8QCW1$aVywlDZD40=nc@kJQz!;35RKBQe)-IpAGdh?u9($54iKIKPS!Ezf(UggLboQR`Rz98o?qgA>2re!mp;-AKw6^JC$Igu$Y!}ds^L-dr0y~+kYH_n;ssU2T=M2p{2wvAmf?RZM*}6fE#AO2y;BQegfF%8gozzs4tB;I<V6s<>1h-}Q<KrFp{0KUz!l2`nPDo2*l?55Zw{Fj$h&csl{1|2ba&}lUx>rBD>iu<Z^vY+n)0|#8yD-_^=jsEJLNr4TlT0gh0#(SPf`E{A?EU*Y9ev$hAcuH4A1SD16dL@3d*R7%dTM!!TGYLn5@wB8umvq^;iI|QaQ*)<s-fL$vUlhLdm5n<!V!`ppMiq`BA!gnDP=Bp8*xDvb>qH4XcOIr><Hhko4ZQAK(mmlIYi$fU6MWgD!p=C}<($AhcRJbX{@>8n%d94#70FVARyImsr7<yKo-zG?vjr1&uutGK`3y=~R^Z$84gJrv=<Nqiro$mOP%^#>O0Stn{TkSE{jSqk)ilaR*M2l{d<`5lOFd@3U<l!xZ*XSc70k57GCzQ9%d=dg_aMK%khdO;y>%Tb_4M4xEVyD2yiB4BF%`0PPN5;Oh1xcyLFwX%djh^6WRnV>gci*Z6wvIi_T47@wtOlKhh)o3c&*RCldCMH<Z^!$zJb|KW?0%$BRfY_kt4sBidfO5{Z4zYnU$lFZZB*<iM{FzsUkEgc;{144#G@dbSnbtKJW(7Ta3V@*N;0wlRA^B)<pLEWvqy52+$fL@I87=mQfY`~tV$$tsWCh7_JPqlJlXuK9$?5-FA&7>VRDQTS+s!%6Ks*iR42)Uph0~u~L3Q;pLPe*e!@HgM}y&q_nNzYf-8SvHX<O;?tNQSuA+D(04Y`j3Ektn6-*h3aZLN3PIh`L{e63?Kvf9}=NPJ6um8&^BkF`HiJa!|BEUN7MM)e1k7bQsd>z%+he#y)IaZjwUmc2ny2rl>S+J5CWbc5j820zkFk0jPVwY5XD%=7-;3e>0V8=nHjLKwWzgyhjG$NRbL!VDXt82Q57kw@nPAK}?iM9IFV*!X&0s{qhp&C@(Kl^27B+eHUdqe0dnk{?u<S2SfB?dIyxn7XLVV#s^i&U*@$3MemrdncdxS5#~%(@WnY4Oo<IH;JXZ!*kIYW#hU?YCEKy7xI{#uG4W)nE;%B(2UAd#H=|+Rve9P*(sQB{I>g0b?Y%JS|J$EG{rtl}zJER6I?PzPz{UW5dxmO&twB-<!E9^u8`p1n?v%O`JqA;j1t{6szT|*IuMv#&^uP59=^WyxcU2)iipy0=_t8SM+FF)Gv+86hGA?AoEnp)My@K+i&AM1#=bMa`{Wky4t>r=4r_<u&mv5Tw?+EsYGod1Dtb-^cwE(wBZAAdesUYR$gnMPm#mJ5k<$@94%d?@MDabO4Szc*@wOM`U^P#BS(~8GWAce6x$Alb-_2*y|I=Jo;b%BwefQJ#c9dADhUvstga?X=Cjvr(Ap(3dRZ-ZrKNVUc^*t&1)Z-nB7q9yve&gS3hK8Jnu-fh8AL&?k2p(GpJlGK`>?V_xvU4K~9!!m)QzdY=hWq$ceu)~DA1less74<IrFRjo`m+Bt5Kj9x{f0)clc}LEnsla@Ac{vnIYB%e#E5I43Gx3M(FT;--+?E8Kx~;N~uFFMP{_suBnjH`3o{iEqERMPIZaIn1Rc|GmHA9;wc@r}up`gQu>vdr;t?;H;SmA~rr_9i_CjP-oNQ`&D(f`HyT+L(^M13kVBEZcmhbADFMCraP@VORs-sQqW6a#GoUhu9hG+Lj6FN%dU=`Zycntrp^a>`{~l|K7(*5>+zAb1^j*l{Hf$-tjpZ)rK_UOGZk`|Q22wIF$dE?BY-w!@{L7nkh5mNB>%BYp_r^b_w34bKcAXWQty%C0|H^9bxfvbxWgfF(T2`Rjas8_qnKmp$YiynQcS8;{r~Ab;|h<D8%QVP)?{TArgi;&xex);eLpe|5Ql0OTyo`SAM7`wy?-m#63O%kxYJ^7!-XuOyEUh3}Aylrm>p3$-nA3tBt%xlgiYW1g4OH#X654XD}oU6eidcb0$D*w1SsQ~zpjh4s_L%R*k*%R*6v(o(w=Ui?}-Dtr<DbL@jfAc*1B<MKXNClrZM|0)w7V-NzGO;rdcMb^t##y?=&hD0Iw@%~xPnbtg)OuOP_k>4rVx941xJ&*5}JzAeWef#Ny*&{j)h`UssX$Ri@PDd|VUK@T}-GBb`$Grdbr(fQGnbz0Sq-pQ^&wu>=c>K-l$GQ^BK7UkFnFKVnFTc&`QkP$R8%l!6(eHZWaeexg4}U6dR@yuoK1Dv@<;q+>U$&4A;G{TsVuQCY5(QyY>&W_Q<7gf$z%3ib@}1iIEZYs|riJqf7*^}@)$sve_{nddmi)_Np{)D_DJKYQ0x&o#J(u)-#POnXUr7KVcDGx5vNj%X{s<eCy!Ytn?XTCuXbo=y>m|ou%7mZ7aG&F7pZ%pd`&M%)a7skatOyl_Nt@PjEteA}18Fro#%bOarkO2{TqWoH+v}P{S@YiXcp}8<6(`<cG?V$(yRya%CtfW9MY+p_k{4>aj1?vnbQ0+|yV``ZuANm3jAaRERJ)|mSwaQB^>tKGCn>3WqRvP4DMTV<(ZD?*BB=Bm{2asA-2fyu1u%#54bDt;?E<PG*`Z?=z7nB5@}$0D^tJ$6#C)zGJ5>0disg*;G4~l}u1nM#?@39j4vlu%7u_2pEzqqz;-NO|^!6Y8ly$};$w7a~p;T}C&-f(=0mI?Gf*KivusRxpEax{Wqh;|d_I(|5I{JBXU62V*3!KgA^`r~Bv)LgEfiQ7wwAOO<tq7~LIT|w3!FEWCtW~D3T1I9Wkj?z$%bM;ryr1p&z@#hmW&}oKW6K-$sO+s^s-#D_$F-h~DX6t5>zLxD{xYFwu%)O`_&|X6Yni!ufyErB3`EHG_)3UGAvD>oAfwtM{rAEW;>J*SGhJZ#g~~$pyQ(6{D}4{`!zwXf3+63HX{}Jx_OQf~`k;S-<%W#5GciZnBGvAfWBn#&w3gX3bu=n#>xJ5ImLlK$xHTKg?-!S#XS0?}A!OtWR9}MLXA|x8Vj#5hzsiz}Tzoc;h{glUypg!}{30F)3I>ESRTS6;WVw0-!J@F}Eg!fm^7HL?1A2gyBG=%x527~Xi#lOkM))a*b&uZwaT<;7it*N+!>m?xg_K;KcB15lW?nn%;3P~3c^D?4&UX#aiE+|9n3LCyxq5T}`<~MH;En-pj6}G^T(=RIXk2tkF(moO)k)VlCIA>fRtb2JhjrHv6-ALt$x^;Onw@WepEXd-B)}#3A_M1fim&YR+=16o_`*{Vm@<Cc!0eOn$%y^M6yUKBXK^5OtWMtj`b|qO#g4%A>w(5Vq@J97GWZ-sy-C$lOR)`+riRbs_rrD|!=ch0u*6so3(Oc#P1$_zH82|SMfudiV3|yUl@?coUS!)Z+WV8sd#3zv;CTh@#m<8X0WdxJj3*Z1&dJkzv3wly^(x5$<NCqtl~xyBnbte5#3=3)xnE_~TZMx_8)V5@y3<9_3tJep-9#+273!aHr0cX$-G<;~gJYLG&lrKPRn!*kjCa*{bG`gBp8&fSNKY3og|C^@i(zMWhpG!r?k^y(57gviAW+m=cAfi-aLZcJabw2t06aP{4z%SXzH}cO63ugI--8r%S2iWu!gJ4*ePAkdZ2|stqWqxRgt1DYkt!<v8W{&gC7isW*qwpmGlb#=r~;AH+onZ3abx7Nv%y@0D$vpl^6+i*0=dBe3GS4$o6Odtjn!H-E0$1K<?BDiiJ|?f&b1JSM*U6bDOl|-Uv?SOv?LA`Tms1aQ3NAIUbxu8k;-Z-Vu{`Uo_1f(o{4TiQ=*HVYGxkr(6#lPilLD3(I&O{Jy7v9O}lXnQP5@1RywXgPHZ}_t3xU{YB>j(SZB$bVoV&eLno1BEnD+kew5gsm&%`~>ZNclnEn@??Y4DaWZL8^UmYzt)?b}>%F?cGwH5Q6v2jlh_P~xLkQL)Joh%B)owKyg=Hp7;ws`|z<M&qr%vpAqhd;euUzW>7c)UO{uq&-Jb%dIx8t<*E^QtdTqVZZL)@s;g>DGgHOx07#pdTgqiUt*jpJ2Ua=k#96r#sUpZZIIT(+DJ+Nc426Ph_kRPs%;`4L)=^2{C=jb_fm4`I+y6^+n4A#%bbMcCFk3`P*>=<)OE>zpJG&o6)wB_}-HFvZz(P8SHwG*HBgXq>D|NuHp*#(t2%PczNA|r1LPX*|?Or;>Ju#IL=zi_eXbGN%4aCjb8b<nbr`Jcz#yF5Vg*Yh6xg@<fgyB2A(JB^1`uWwO5jwTp7zpN-^C@73qO!GZ}#0z9_32=k;+YmxM(>&_yZmrby8DT<6&7Y(4?9_07AEMV6=U5({#jC^R2b(ieUmW`rh(f2rfVB~nTc9Q32fe_8G#wUt!?hpv8qeglKRDL81aZ;Fk?mZ{veiUY)Tei7Wh?WWu_wlqQ4M;AV2$w|y6OxLFK#oD{vrtpDXE3gb7P&QVYXBh~k&ayB@woT^y;%c7RML>&Wv}u;u3Ycq}ETcTfUeW8;<_IQaw3%Z=I@?FHV&cUu(-@cnLZg8NY4tdni!F0#S}3)Z*vCkH02Fe-rJmJTnAfW}XI8?E3e*1K)LnCI_i~(pn2Z5w-8vMFkV1UC8YvpL>MfFY%+lJj<u+ibD6A@5@KVH^b<jfcwT%yezv(nd(GO&DYN^?ZN8S>hBXOYYoBdhK`>_`+-W7;0V1IxS8(z`6S%CH;-NT+42?U^g8K@+p01C9W7u_23PAgm}sqqJy7BeM+u>{J?VVj!3V8pD93X*MFIjB^9L6K8bP{DCi;9*INfKE_atE93Np*-Z?9ckI6$K_d5AL`6xEbD`aG1R*!(R5}E-duvLSx!~sZBc=C-M>*L0RJ>*osR14XtvM`#gW>CNdL?V#?KnLlQnSO(E-LxfyXRus006tc$FU1IP9)KCxm2aVxxuPpgP}Utj_2Y4*R~{oJos)bV1j90d^HuFRlLpc?e4$z}Xt?>E(S)C#u~SkZ+YVwG&&15=u$Z%=tL=og(>9Ilt6foV`v<LYDLj|5?UU8wbnJ)yx@*ZAr_34liAXR3#AHDpgsE64GTDsxA~f`qMc7AiWW8kiK78UP;^T4%u>pv`l_rEuNgSxdMf{Hk^S(-qUs|(!SlFbR%n#@w3LDkRS${U!8*E7??JF@b)1Ygu*W24pxx5n~O%3>}PQ3GL0L*T7^OKJO_h!xp}LNj<DKd6EAonMX^R<28=`1-X`TGj@O*+0uNyFF_Yx-`x(vU`guu*Uien<bg_mw{R8xGv447+yjiX07vscz!K`>X1hl~UgAf=>)u4?BA#9(`2ydRkq5K7ttDT7&7!P|`;aMH>o8**ph)AZ5aT>ym4o-te%@}`<_F<t1kKM3nlgLgVX|pYQhB@%{HpuT^mkLdMkCP@;)XF8AdYEQqcH&x0N8$?}TQ5=DZCsFy6zNPn=`jbR<*}K)iv|#v2_18@g|`4`OaPJ;%%TiHZtBr0bk8#NI=*bs8AUvjVSBB8xk*#?^7DWMBIemiQ*hJ`W|*ULSYN@*m{rQzPR5fRt5A~a)N?+r;TfRGv`$^^045bWMRu&abpPj;mg+3NLp9M|8KZ%td!%wJ{XTFWt2<E28bFom1bY*XD%A;8FC!I{l;9DfcgFZrR)k1e%#n`k`2e_+_LG$)Dhj22Ai)|k3qZMK22myPnnKeDVwfnBswj#q{>~?pP<xj}IB}r6roe{P+%%t?kMfC_jk4|GufJlm^U%)8vCs7zwe4N3)+=R$+^gXniD#*mBv+u?K`Bc}2Yi)HMBwy76(2MRNUFKl248V@Q<q}`nq|4Q(;r+03K+YQJA8m~MJ+eE?9426Te8$caYLTdsKJsyt$2lj5tGBQkj}8yY;L}1Lj;36n4MRQeQ2l8tVO?%m-#|~R5+2|Cultm(g_VKN4#sRenC`*r;G!zX0U3{jk*k6-bnc&5JE|sc7R{EG>n2JIcKFX3KCp1z<arLI}K}AcxxMsnB7fkS1(@9umLtgc&&~j7m4fmNm$4f?F!Pr?od1)KmJoQbRa6hco;$xBKgG-2<j$)eV6K7k@G7Wt%1Xj)0s_~2Rc2&4JRO&_J4C3X&OdZSAF-2drbIaO9)D4YYW1CML~|VkFd^?9BOjbb6if`f&r*ft>Z^xFDgG1>h!k2Ns^0+9R}F4rI_-U6k+1Bp`|OMl$*8~jGkQv-;D!8%(mOo2=b|s_6oJ5etyn017_4gA_h!*6FgDox;HITPhcZ!*@`ocwEbQ^Vf|*ZR$p%*OtgbuDjvVa*lp8OC5KMs+?!KPAW^`aj{_iD-<9aj>M91`5yuEf1R81Ww3@{)WCLAW)LxCMup^W#A+2Ez$t%RwquC9s5f)bN{s8${!NT?F8>gLv4HtD*fgEOxBLVQv%atuDc^vhI>keGmRG>K}y06k~YU&`Net0h%t&NgP(Wqh|ea{8GT%r)*iqR2;xJn_9;0CnaeHsujccW^B!lP=NE(9Fp$0R^geP9iQoZ1-ryNT7oJl4k>4zhXo?qeZ4G%|Qq-72^skwjXwJ*Sq<3W(D@nY0P|K~HT(ZiS=;jNeq~T!(r2TE#0n(-ul=IcL1{j-+ZCx;?G!hi;ZM8z@=FfVa&Z?$}B%gs;+2#zszJxDu;_W?D1s`aP&B0@7qXlio5rG6Bv^v%%5l5SxIkIHr`$?$%hFy#KnR%brQp#l69LFZ`64H-hMB#;*Qb2V;6Cv4OKw*wQIvQ`(YjELLt?Y5OH}oMy!PZ&RfO$qX!7q@4T5s=WGRMW^qD88;{02i)K9n7L6;NXqmcq-=N5E3eqmYAc!G2EqnlJc|L?`Hbuq|1p#ZRhU$NC=hcv$rN?g3|*PGS(m6^^DzLsgc_~Uc~3duG%Pqzkaxf3-Q>Wr9ReMZ1ez-qCwB1wnI=;;84$>|3UUSoOM%(=OLCzQwQ^sEHbHBw1av4EW`F`9%6u$Vt6s9~h-Kzf_f7T(Qs9pwlHh2n9B7`+MLDSkM@oTU!K!pe!z8e{LVX)-Q&5w};COHQ3lzps6qg38Mg|Z)W<TL7Fu$5YhMQuCqu@17ynLJOW*)1SXaW0&Sy)a7u2h!&MVbrWKM3=QH0^D&K(L86sRSrg2Vj2XtwZ8c(ymTdt>r<_*i0EX!0P$T29GL8<j`M{-Y2fNhUoyk$cHH0;LG6ZY+EL*SyDg#_~V(s`jt!RLETcYo#`!o6zNw60z8#O3Fcr+CA0$^^dL`~C&-Vrf9y_G7P1t5g26kB0w1#tK`FxxZXmVqW5hwGF&^Ww(wL?<zZjRIQTcr0f^MczrJS7T)8{BeDXivFnp+l+f_q*VZQ5#&X2tp(__;jcgjJ8{*y>7-i<zjn6TL_=aN6&Cau^u3)eTjgvOHwC0=IYrM|WvJZ8?W>Qfhzoy!hf0mynT*H_veNjfG!L=ktf3e$3BSXCa&IP*#l2dK%F-n?49>2kftILeQ&K&BP+=C<!y~jhxF@ZS#P84}3hh%CA5C@cZj;)azuk_b2vYDQovw>N7_B)mZMrrl^xg(Rdp8r8WbQ9Gn_j3Y`_p3nz|)OvM4Q+P_7S=Hnnkk%?7#tvYdAMLe3+dfQT$Q$dU8<Owh*3&k1A;LK|lAwl0_xZ}bEZpTeW6HpO2x-z9EBH}P|FqWtL5(>LE$3nKNVIdhP!Y~@Ck8he8aI~Q4ueo{GhDkORCG%U+T6F3YP6?Mce*2(Y-@BGG^J<<fw&H}85!(jkjhIcQwrH>$9b0qB<r2)8s9;e!IJ?A&zK|rU>SIiFK>*k6O1IW0(Gr*lTqi-=P(wfC$rDVjbl;ycPIuQCi$_O(jht7aWo2r$UI69@QlPlb(|e4APC`wX{&h42m{KEWFjJ<yDJj5S&4RYs4vzO}=s*gM*-;;HS-+i$>8`*y*?sDG&{|4u)Ly5;xM-bckxVbYTv!+7E!z2(;hpaDy}#Ft`x6<9*H=XwK`I0VMZaexlm!a(oE`=Qe<VpgB`Q8N5lN#bR%mNB9gVvg@kADBUKlxiTyd+24U3>3<v?nq-tT6x;N|o>|0}<4r^n#S%R%ovPN$E?4^uhNt-zaTmzWb}%)ZTf{>5Zvvs>Kr1iiY{8x*N4dbUszMHl2MKlwvGxrK%l(qWABc$Lot5$f=od+z`2K92?;12!QCc(z)7SvMc`Z!js)s$~Mayp%0TiYtIqanyrm79lVDmt;aq#wPy^LY55Vqe$06fY25gDLA)GA<{!dwA?`_x16n{w9Y!2AnR_WzVEat&2tX)+kU|JLJAf8y|jg3B^^Vgkiz)PJ{5!wc)8=BN_;#&DWseOKR@o_pD}xJTy^K^AXWL1CeU>j5F~Xm6+l+RGccE$hKz4nVZx3TEy{##l{N~_??4<_?`pckjBW@z;w0V072;3DKr4-XtT7J9_7$c=Nx7n}hDB^2>U`BgeZ}4jDoM&<C!fDM%7dfs*sf`MN$I6elcYjL7LAX)`NA`aZn55=Ssx-);E*W4lIU2sK_nHORn1{}mso9pHdaLg=NgVzfmBIB6X8k++3FR8Xobh|>oI)$Si@>e;lV3#>Yynp+fWT#UhrtcIl`!-`N|Z%Ls7@}V|(w#872ZjcI}C{fn1;9(`Wqt8ex?WufM$i@M<9q3!BsVzkbPqm%sUjZM-~%vg*srULYPA)_8h0VU3!Z2<?Qsl4jK_z5XJ33)iZ01?4UGuT4Oue+CFg8`Z!4p5O)KAdg+3*sjOf0yP?Tcam++gBdGt4(m(TPe>|vyANO!nqeYoyL+rHAr_BJW?FSBa0;sdIhBJqY`^I=TY|1#lAfYs0nL7+5J$_29o;=d6ZF+J=E1n&yEw*WM2!zmXu<YH=|$)nU2$VI)~#AmoffOU=?FNPGSpBA`DDpH;|g@C<YZ6Ko5a=<@s(gIz>g)13OQPe<wvcZg;|-St~sirN)^;u*D8cBh$2#{0>G86E4px8oL$nd!0zwe2=MG?&Cm2Gt+JRXpL81&pLYcnSI$zT@@MMoty#dVeVH%{J98rC&u3`(5ZJU~hL%Z~Czry}snIs?0!GcuE;mmLI~Pt~Q@NOFrm?e<Vm&$c3v_+?KwHFr<c0uZI_cQJzK%H~MJ&7<A`p+uK8wDtPz3I%&r{DzC>5NFU=Wucsv8_xQpRuiP)V!y@IM0-6hw_&Jcv<$OywWDhusiB3gS?UDIU~5f<ixxV-v)Zn7D<XR`nhuf=8Z>5jYwRn>9<_NSB6<yjE6`I-|`hfrTCuX1Gxm%b2%nclw12<IPDqtR<qGHJh3-B_SQrQQy!=tgFS48WHa!DR##v8nj(02*6?T6)I|UhCYD;JN7V)L9XLtRa$CLa8`kITz!_5`7NSSg@h#=WrZhu^ZZ_8ld_fWx3y~U#LnPbbV`t1UkjOZ@0CQ2i&{dvk9{2+5CEu_a?s=Auxtx12DF)5lvz0Hp;}W0MP|`Ktd=xH<dPzYCDYGVPkE*A+u!esBQ$OeAym#1W|nPgD|r<BZtrp6v{+J3j$C79@oJqUGSE1+O;mi*J64ak&xbE$u7D@p);v-B=2Q-^Wn1XHTCimv#B(0-uR0piYbryZrS9$yr$mHTs3jjNcuM{W?RKdk_cia0T1`=!^?_$$6SaA+89vJi8I+rgp_Fc1add#XL(GL_5~(>`k1e|_N=3jNOejDTgmob}<-~?5Dw*?^|5y^?o)Lhw1s|Uy8|zx(s4@tbeZ=C4mNAZ`(zKJJWL5#d$^*kvEm3X+<u1sQdZ#JQ)YCJU|KVdxB2H!Yyp5826!G^`f^x|T6a#p;0VMaxhI0)VDITFh9X=M}Rr{NbMrF#cE0mK{14f5xBYFzRbs=r}HirOpl#9t3?1%_1$Fx;L_q|q3`{o%*_q5Uy#OiR%QQD^ZJu^~1DfzZj!&$QquRB6=Y=RUE3MAw5f&wM?+%SxmA7D#R3e#{ngn1HTn8x*^2TR<nU?hvk@{j}eV%7UBz9(w;+F@EZfQHVVJss&i28tTFMZ4)~pWIlp<9+WcO+N3PCML8Y_Ue`^we?z57VFAe3{pZvYCO~b&d?*{2m4}+@;nJWs*EJfnu{Wx<Zv%!3E;Pe)l^YEdjv_+h*2S?wR(Qa5RlPtkuw~#RstfwU6OnrA?}ifcG1n!Qtxf$<|T=SA<LHZw?;L0x^fb{wv#j5OPCtZR!!D9C3g3fBgnR5u3AzlNCoJrb_-hxk7n>_@5;)4%QAtqA;~Az6Y0L`mH*Ud5Sw<n+>yGI3bL|Gt}GR>K$dj)0@1Dg;Ca|k#oQ4|=z+_Jwd`1nJShO<`~4z+Do-Wf&Sv|uW*@2i&Csg^0R!=gcMdBG-7si`$?NfD1*-e&$cW<%f>a0URFnZOYTT^Ed$MHJz&d$)4Q)}fW53dEhToQJ?!@|>u3P#zY~)G1Bw-SMkhc}nS)fn<<+*f*?dt#VDk@|2iwYgs*Oyl^D!vuB4(9-qp~%AYN%lzIwJ;jb1Q{fe8-N$dbjC;sJZW1Y`UQpOSoUS1auT|0$NQxsvi6nRrZ_BN_DQwDm+bUElXQouJ1n@KppFQQqM`tlM>7W6(6V$MR%FI&l(S=rjEIATW<(_zc)*vb;f^d7bU+p*G+RtIL&wjqK=4r3oV3V7P^Z$Jj%xUXzrxz}>SB3?D40ncJH7Vm#$2wFfsH2Crp<Zdr<i3{L}#0--;6F^64819()3Vxsl}<Dg160z5-sy%*_}n@AGEhMG(!!<qQ&5o?spFNAImpXJDj+?H{WYi=ZL`HhQG_Uwzh#f#WYpKAQ!*7!};whLp)cAs%d>#5pI3RV;E+{KFW<oW|h*!8(2>EQ(Myvyn{=^3zmcAA!^Q?I$Cym$s@gwJd<_Ri%45h!O@gB{eeYpYnFk1v1A9W4lbOC&<U5fW3Zy!sZ#A^vjrHVKF=Zgwkrv_aIjqyU`h=z8CJ0$mZ=%w?>G;XzNO6y3dOT@@NornMa-=yRLs=QPZbdT3y0;|9s5xG6I0F-xKYWD>QUD~ppUP%+yH&f`Rv>7;N_tjovylEoo7UhXp(lHHcQo{IKs&UJ~+O<@>^m*=&~6JWgO?Rd0Az?DjrtJoJ>(irP~<ZCkQ=?#TKt@-EhTaXp_~=Rgre|x)?(>NT`dHozO}o(%IeG@d0O=z(`iFZdJwon52pdgs9|gO(anjbB_A6JWJ9L!-emu8q5+JaJTVZijH`K1mHb*K~;#wrBVQ{G<`mv2n>F`9tav<V`&krXjL?myp8`hTE6eyA@dw4UvuSqWjP2gm2Y*xh{AbBG^%yPbj0}5f=R8h)kOXG72Z~hY+y=}yZ-2v+%jM53T;uBg|HtZpxt!*&gq0wW@9(t2M~ZByYExB^eQ_-v|tg(874kQRqo$r_fZRo@phw@9<V5ineA@uI(RW~q|K<`d0F+?oH(VQQ<h9)!b9)w&eX{?b0E@6u@g(Wc$;=t86T#QsY4xyl0o~l6rZT`80O;WluIEUPklEYUzCOu)jKm`8J;@2u+vMWWG_Pzrrmj$7Omv9uV~oG1!4$7NX`ofd>3&7B+9~tGG;EuB}c$(F3v8C`EBmFg;l_X(&|=b>fwNmgM!oEL(pYH8*WN3B@_1OG;-_g;a#VGLjAy1wt)Zp+-m)$P(wezF1IfyS&A`vV>cC{sc1~rDM8b<W+N%&d>UxhtXVtz4PCJ-OIDn%Gj(KHkoQ|Jn<Jzsg$U9oxO(}P&Zkg<IDbsCiL=!bb4V8ko`$y0(-4sld7F98Qbgf=GC58$jz>Yw=Jb;dp)wV(?irI_n>y8>Xo&|FlD)Pcx~*EmCGGl8p<xWX`;)^t(ztc?sj&7-Rw#q95qcO;9&d5S)uSZR^lBGC<PJBbP&*C2n+*Vz9`gF|9LlgxWx^&q8IGGJX$!+AGK$zgzi3#Aag97ik|4(wURg8|cydst<yv)`S00c8!VqogqWM$dc_QG4*+p@*$@AL{7FeZ+&GDseNl=Yy^H`dPg8j9oSr%2$iM(<KcJ;YUjwfCxE+MLF+JQJ}lIy7gq1(V$V)XT2a(O0?`QXI8;pT=%uAO)Drj3+8*pv-q(jrCwAzE^-7_5kFlNrJIPD3UD$;f4w6|r^fV{&bxNyI1Zk(@?(#3Z<UM?FWSZ;Fap6>Mi%iVG84RjqQKOp<80AXRQW2SfPG4Te3*CLx?1`YAaWV|}}|JnID1nPp#d#ei*y!uA6)K5Pd98Cb6MBfW`xFN^|Dw!t`v#?ocWMbfO<&i4q7ufUwUK8>aO<?@*k?P#^240YOHvhsK99a}tSpDcFFGU9Yn`Zr2<&Uro%l+&Tlu)t+S;^g)4pB#ZSDIJMOtWWCZj4Qpx^7V;ewOvC`e<YU2%dn}k`O1MwNp%!2X@)NLySlSBQY7C3W?`od3BbJMRWNxNa9EQ0UR$?HhVv8%&O)IGz*)jE!m_|zv!m{?GWUrTVt5ws8?~2AAD<Z*JBmaF@3NL;6Nrzf5e;|RY2bCck`&0%AYz)XK+E{DK2jj@$Zp*(;e`r4FF}iX`ygo{7u7Q+l|YAT8ZvF$E#$oVf);qrn`oObfq2doR07CS<qGIl<;i-knbyfAErqUATtq(AwxT^uZ*+#$gYg+4$SR6yOoqzPSof)xB5NxYQ(dbQ-ts|Ei2AB<RhxX+$j?3n=g6v>Oquu2-d5|&tisb}NZb9qI5V><-<6UeFT62<t`cF_#$cJu4BDTBFRl8rbIwr3ubk;AmAWWxejLoB{r0~6La>#ebB>knOmwnoagJ3v0WQP?d4Y2bX|v5v07|++$vkgGs{|wLP>Hb<eR)*)T{hIcIE)R?DHmUewxT)*Do1KY&J)@jiR}j8bTH|YJpS>a#GsnoF^=IGcyNT&28lK*-sh-jGO}*1=<Q)bx1B>>>vL7g(v7aMq!dY7w|~yJ>k8wuK#=6047SfU`BQ@@cgT>Z=kOw)mPpdpN1lqn!c860ZY?A<DgOJiD!B&Wz%Zvca^4SCXl4V!uK~;hu1KI5qprevxLj^maEZ^6(;{FHl0U9tq;YbuWzLppVkJQJ$#@JwIcth0Ox!WPgou+Poq7Y26&%D8gtvz)7eX^Rr_+GQ9SChVi-FHNt%T^8vDJh$qlfS_4Pi&>SQhvTdk{&M=f1eO;nYmF?#Vz<;B7(F$Gz4v+Dh1Xm+$5tPfF4}HpFR?mnWjCMRF;z5So+Z>b>ovyw}m@>NAU<dUqULy^<|T%TS!nT;au@@{!T&fd3RvJO;GPEaqZs&GW~KWP`;Jg%M$j_0jxFHo*Ww3lB)$`>x~8boIrqIBPOAs!C{}nG1NaOp{Ft&CoKF&zCu9`JlLsVpt7gq<A7;$4(<E3s9b^h`c<7hj@9J;%V0t_8kB`ZHXt!*wt??$4T^JdWT@o`9HE}TxPY0iWAuG?x+YVY9H&iUWbBrd%>>hLBdX3^d4qvRTD6wKNXjFD75aLj$H?+IEAL?96jndjhUb?AUP*mzl^3*;G=K?!F5P~`}3!tfB47uujf0)v!$0MdeB#z&y#O9bF2qocC{X{C(rw!(lwh_f2<rpl_>jy9h}ycT33i7uw0>V&v2tpvzMe04G|7i(xppF=4xwMGV8LZp}KAx4txSg0`V*02$)opga&^}7dp#>a&@P*%`e|H+usrD5obb0np}rWMk3+0$d%O73pVA990(Sx#Sgt=Trj?Sc|Pb#7HlBJ)~~cf+e}9D`B41o`90t#kmB~7{6dbz`g1VaAYAu|K*88uz&&kwB(3x)e9bWyFUxvac1w;QWB8#SsRM6=MrVjC$E4S~Z|iSlM8@&D&gS3hKF0v%bEO4GMN}_Ohf->AOHv*W+eKMLyZ*4I@ooY{e|gw1%lz_{V225Z7_!@dj`3agUs|7=F4g_wRTHu2*&imeQr?ksAnJMfoG;Oq-Ss-V!I^<W6Mwk=GW;leTN2O-KmKi%b+m;p0!)XyLrkmz$gz;`S)pCSVnjZEupHA?;LOlQRKYzxIw?+`pEc~zPhJ*WEhsRstRqLt3rLRqu@x><5d#HCpUQlQRKuYUu?Wtk7?4xC>)Ir9{xw7~sH&;#VXhR3tPU*^(xkuCUugQxTFWVyM)rJ1H&39r`XJq?LEK@-l{_Q^e|o*8<(zxz2u<y|A2Y+RRsc)Z!FISM+2WGj*D?mz6vz(&obK&?p}m|T<ZK&VSK0LkYaUYrpGQOf^Q?-vBnG_=z~{T+T!bmvK;8lIU%srC$D}+rd-7Nu-#{hERUK8ieMGE3R2(u`n^XsjoFzOTUVnN2;Whm7^pJjeo@s6ze}4Uyq!gm!eO9J<Nnb%Zv8JU`)WF~?<XMq%DUUX$dpV11%s0t@*O+kDW9B>b7I@Krl@}ps-0{+o7x%JYbOoElTUcDAyjbUe5dRu403;rZcu*va*?dP3C{N}8Dw91go4)-q^@LMv6@6fen-hF)@dE=`owxA~j-=lEFl_m<IePFs{2U8D;5`lLEHNNl#&(}Re)s8<*)v8m^$p0oyv<$2_%5I*c=<bhz0&I}|F*}Lp!xe>fBNP9mq~m*O?v#U|NO__kH_D<_N^-u?ej+^M<U>@efe!hpSb+u+fWh+kABx1@$1vCeE3t5xzb+K@G0^EFK7Mo`Lcy{07u2aQ-i#Hk*FY};s_oM$gVbz6{MF9WBE?)eU|NpbC1LM2n?%r`Re$9FZAWNPfPw~u~1fif=#NW88-nK998y9+C<`bQGKu^$Pl~Vtvy*Ak2imWK1$wu2;2(mwJ_SP-dEO3j=z+tV};=Yp!L~bnzL^;mjdTd^h}0O6`6E(9oO;)Vk(<fZ)BY2U16Hp;s6Yt`ERf5B5BRL=%&lQm@utZoOpu*P3Bwg${LlNm=6WS<t`ISUTD{;FrQG+Xr$llY7@$udRFl$mo=kNsgpu0O38#eUPlEn6KXt|vqBekL8aD^s1>0<#MSgjU<N<O@MSsx>#fxJlxL>8w1KJ<e(0EmuS92%JSoS%s8kEts4<^Q&r#z6^Y5X?T%C`(&oFZtquzK=N_Tc>w97u~-WX{SV&xIDw(Z94GW2d%zUd^J=r1{x>TUnI5M3~GTuHo)L0Ec?#jBU){DyLES!;`ZpS<)f#XcHm`xBfNLz~m<DI0WWv%@R`VdB_mt>sG6`N7#74H@ZRJ1j@mThkXgBeM+HX@2r$O}8{(Hy*%#4@}uYZ$@AqH@3V{Q_J28rb_aKdtB>ry}TD?9aG%YUncYnwgfi{9|+KXtx7j9u$beNfe6_iUkQ;YgeJQcR99PF0==+=SXR(h1jm@JP+6#cSJ&5M@Ox<ER*5QGaKbrC|B0Fyh^3{}2mRH%;L22~_9Hj7?>5-^+SdkJ%iOa%l9sjgLY-Ahk#Bz7nw{wPi%Zb6Sxcr6GV%qgFG26KA!^tPgm(T{S?ZFD&&Cnacwm`#9@m~<#N$BnfN-XYdff5r8W9AG!fv0NQikN`+wTT64JSpe!D}BxZN?XM!nlm^Qx5AMzX9Sj8rv1)tviQVt>_8~zdHR#$qmg+gVw=Gm~8SeOp?c}J<y41?RPLIuYGg%=m54wS<W9T2edH~;hJ>a&Rrsk(J94{<Rcd^UE`PlU;tSq;6WbNT|ZPsMJ^>v824y4#sPlTKrxd5m*9&GoX07?vd?n|UPs{zPeEYH_;CZXPrfH3{TEY!$3C3JfzYu!dH3r#ErAs~0@JSt`UsJFa`MUGa}f0=l~*mrHbl7^J`Zo89fb^sN_W6PV?8V|V>~rg_PI5|Xv7!wRttk=x(ZfWTv3LR{n%*lPcHA7cYuNC6~r1l4<;1D^yD+1ScE$#Pw&O@am3fFBnOP^2d`IJrA@BMJFdhi?i0CRWz}1S!9W{i$yvJ7MbHad7_{9)EVC8rpK(zbqf_06;ADeimpsoHfv;86_SzYP3ff(T;#^C>%y6K1S99@vO`TqhFSAEfZD?|X0YQGCKOZB3qB^td^k>9d*7V1n8RG-+=)h>u)|xm=&FCX-CI)<v67b5#gbD(m)rzv5=i2N0>FD@D^#f!5LL(<sqAD`riF!$S=djCyFFr%4Qh;&~2pb3$q)69yBFD&P2cwJ`I%sMJnfP|yYwLy&B!E;-dvbdpwl2E~^&-uxE7Yd>`cH8l3r*)?4Ad%x9*@<o^JV`rO<3YU!R>%tBt@7atu^8or&8RCTVi*>rwy31!P6b64nOox7w4Us3Osa;K&R>`B!aYgE&i&H=WN=LV+e^Z&)?o+;ySgt=b`nMcJ7fR)>-nV7#W9b#Yrq#OW0@|Fikjp4$l%EeEI0VOVc!?v)_g;7w_HCqT|<kcS7H|#C0a1@k-2tMq-#c%sp|FwQZrV<?O4)g?B2|%S=ND=29$h(q(`D+CtSvGHE@_S7gK_l<MqcPUChsRwWM9>MwjF3i+laV%<%@Vq}?T!z{^q=vI>5p};i9Dm~Gu_RM^ls4tfdHI4!{C(-)rd=lJJtdwGBr=`Z_p;SBL-Y_~hedwD?lu|NOK2IG>0q*NUwXxI<UJd@8Iifr2A+xH=8^sGK_qL=e<M~G<nR~JGfeP9(=f*-QaMKPT(FmA}Ax*t|n~fQs$`T+L{#fm|khfA-C{xU4(=$lr?v56#uVUK?b}g9iAq@ovh9O%qdJ`A2Vj#@uWlxr+Qt1_xvnXq2^lNKz7Wa2|WrDRX&^<`akeR<X@lNm&_3Q|SkA!v>b>WB`ik{5{a`RlW_<%9u@JmGbb7X8wapNtK7kbbrn3R|$tR&k;yO7_Q?0y$5wmGq}IO&=Ko7dQoj~YmJut`jQ4YX!29<4FilA=-5><9%3G$1g0$u@;$OJitR_2u^nYjGHub+u^OiV>Z-6<sXLV+T~8P%%oys2!oLAwf0V*mu+xrcRa$LS`^2U_Ht+mSrLff#+#1*_lnRhl)iEy#2L+lKP}gunGb3Rk~~$GM}xTZJEtMP}8VAM9E}ltrGeOzyDe%<|3M?aT9UJGD<V3Dd&k8WV!J0?qg>fdEXV&X$TKg%TkfxdiVkC5A609SDE(zb<7O1<dD79=<*vA`^6?<wE&-dLAix0-DLs+w*7Dgk7e!UxC;m^jMOk%?w3am;lu_e*$V%_<$%hq+1sy5p)CjoYHDoSn-kKv{10}lPI3+^s?5GvHZumYWgBc+2=+8oN5y*WULX(<UH{t+J_t)()3JnJ1#Debr6DD-yiDuXoKaG9jtP$Ei8fGsc19Ciak8K>de9HkQFj#&5ZQg~ljO((?Mj_Q$JJO9n-HmKQpN(0FCX!25K@?o6|X6_`T4ZO4Z08ntHJf0DK5E(><;M6X^fl-Kw;N5giSMp;3yTWf>5^W#0hw^2)rxLFuWYqZBdrH8h|3uH^h`5Bv-e8l2<O673IIoz=mP-9a4$q1XOu^#L2Pya9Hi9<z_=GBn8kxA`GyM<}wh7M587{=Vev1cFgF}v_HuwsjG^^b@4#w+hr^ymyXxSm6e?Ny0sj2n%&(T?qX?bp{u;!-?_Pa5t<Nt$q#G;@!MWlY5w^7`o~c=&+Q6NQLI<eg!Zu^&JV>CfdlE+c_MK3_|3VDz32{rbjhYAl^Lm_qql>*idp@Y-ygExNSbu}-M;uJ#|1)N5y|Qly&3~Xm_a~-eu@EKTP4jJBFFDRIf0>Xjuu35RJhU`fec}NbvETYAnX^DQzn0aH`bn?%a5rM`Sp{N{<$z<Izi|U=!Za7mDNmeaW>p1H2g>ZNGJZo(?NqR%Aedj=XtWno_*u=Py<jc!a>tf)0#e$7Ff<tZz(@^*my~F@D{Ylhq9Uek)C#W8u_d<n%S;G&!b2@IQQN<PQQO$Y7EI3K8lc?=g+v=AI;2^%ZMz7&ev&92fs}ZlEg^PX6k*NEMC!?%-*U{t;!h*kX#iODAyJk*m$HN{G^*Hoi~vlEH<ZfvxR5*lC%*Q95oID2#R_FmVUeq^`+f3ky8h6ryesdh8!JGiKf<|Z!@<-e*wrfVlgji-HlSd0e8#hh+9=WtY$bISrpc*QT?BbA69q|j%jg$8-Qz}@5|aDmcz00L#<_00!QJ57vWmcF}fQ<ide%JLhx9XfgDx4GOm>iF`dyQNp`5{xKIVxQ{LdfxawW;v_=ns(Jjv#H4F{5T}t=R9cMXPq||;-$&Z8*aJ$sx@wiZ0T3ay47J|)0vz*E-Bj8o^S&UNhO^q}jvQdF|nga0^!^b;2S`MwQn@v+Bk@qJj@_;cuksl*2WxB|i%b1ULQnHRLC>K<v9!3;hL6U~j^_;e?4=sJw*~51o3JPt*s^P29=dsF>=a!j$im}`C6;l{Q-(I8$#fIXeMH`PNpX{tzp4ol=%C;(>g+=rD=7>i+%Ds{kva+8FMR88J@;3}AVHI{rL3^3@fbo*8x%=1EU=ZsmqSWm}jQK_8DZJTHKfb0&E3wt>UUMMOMakR&@IgtjERV`H<p@sFtO=jhsbglxN_3R@Wbx<B24If}^zyN178P>{s%xD;!+j+w*kYjm6_ukvcM%O}Rv0^S^cZN6i=Ms#y9iP{gouS8<e*=yG}`fE5z|<wTEi8CG_YS|WQchjw3)Xu4Uwdvh{B+_<o_nSMv}72wVR-l33#mtR0oQQtK#kiDi{_^Dsi#J|K#&h;d%y%2JP00l$X;wJ|gy_l94O%S#NH7xtQ2tfUQ>C@R}%Rr!qF6TZ+}Uj9PE!TC~nC;{r63vaX{z(H2oF(RT6V=gE4prW!CvwONFmN`95H4#4M&hX@#1%l4az+}Q8cQ@!u@ES1+AsB?NcYjxF&`q*t#Qk7-WR+rV<!$9vHse}_oNhOM7dNHxS!YBxU_1U6l+e?lWg3NrRAviC)Jp3Jz*Ww$d225vz$nd7)UX6s%At<byGal}hDgq0>SZU7p1;&M7W!fwh@^+j8If8Y~Fxi;p;P>UaxN41~(hPL^jbykhZNsuN%#qK^$IYOXH6|c-o;YJA4=I|iAv?1WN})al74TH4ID-7Lv$VWyfpZEwv*k4|;*A33nCx9S3~|NjLuHjFazdG4)dpI)FIhQ2Hxu<eb~TC#mFWATPH|*n$8{|d>-DP2KHmkjQji&0m&fSUv#Dmby#~A6*%R?LXU^pll(q`5^q6gue)k}7O(%sOyK=EOUIrYGRkfqm$w-fy5^%u^PRPTdg`;VW*>X-UUg5F$rZv*X*kY{HlUFAA%!r(lE&BRTxpd-M%id|Jr?nklV&8LD7_4B9_?Yd|#PhB-$+(J{s4z^8NKFL(KI{>O8RiqqJaY>B)@rJPE0H}s6(}K!AeStf)-rbTvP4@#w3o9|aV67<=gN)0jBcX{4>735Nfrt&B6-9L)@Mi{WD+1FRz?ts`Z54qBRxCHDBQHKx=Hz2eVOMvu_xwQw>#gp1u9sB2-9~3^?_zA3%f&N<^jgA%&hCF6S?diW>A5izIdQ@cZcH3dmCz%Y?MWntWL%?Nocm+)jlr7BBbUGAj}2|lG_O=T5wxN&Tz8icj$GtyuD!hgpTYC+n3tRWxCV=87wiiF@P5`P+u;#qB>yue%abXzgkMWC`KvTeO%fP|C2Q++YHsG{MVkKKRas`HUb@l@E;k++3oFTj+W`ENgRSK_(Mi`yN`FL-PZre$lFA+yRS2I&;Q~0<Bw~)(KVdH;)TX_aadz)l%>E8-8j#ksxW2C#SzZSrRL_n%ehAhS7~xoUZ|j<t4730oJ>~OY1%IOCB-<2@L9<+qjhpQ3gE>aThNZFrauMbD!yB?h12zWj?xww4(WN?5p6noeAZ+xc*!1KY%D0bnJ9|zjsboJokZ5sn2E!z6N)0nMy^3M5AG^95``EdZZaA$fv@m+-p4d_kV|<!7u4;u)4AYhziYvyrcZIc20(5iupuwHcAPOS7BF~84CR?TX=RT6+!W+@o_`+c@T>s8Ak`wUn>@1ZRJ+$^0=B%at><uJr{^Rd_r4y=4?q0~_Kzjq(}+vxW@bshluhfk5ZaP6^XYL7+Qre6SzO+$E<S$<K>B0vqRU$0gsL*=0HY^y+_Zppdhn{kzAU~Fc#VgGQ&ECvGaU4fe)lKS9>A{LgOe3L{TF0ld-o<@E_pV<9d`b7@sCnV7Sf_&&Rqr{YK&5Lzp<1TKL0Jza3Fxv<!H4Hd*F%a{c14SxIijr3fT3(!T<|YA5aYdcTB+?hsg3(qckR(z~p|xutTy^)y5a52Y&OfZIY;HCANnn>dC!MEv9|>;=Xn(GJ)0$#_A~GFo6-+#H-%neTed&3o{%!NU8)Lp({RMgsRXZI$Yw;W$SE(@bn~G+HpW?Rhu1ggJ!^Ln%4J@8nDcW7r|ShVzY01(TbylBG$2Y<*HLYiJkWabJOidUpPcJ`(~XC)78WNW-jk>C~?QYz$@^H%Z70Xz-7QKj=d;`#YC0pCs<Da^0Qg(?(L}#r8Y{I%%eqp(3u-*_975n_;l+?h1K?az{I;$xH;s`x`K1sc`nv;&wH3Ca_t9pT?htM3D807vM?@~Av>9g>++=%?hB-m(-n9`RahD+u4k8Ee6f-{FgH4E4uK}t$qQd!J&mCWv5z6pDRd9RqhT4lSu$1*fvT||^B8dS;I=XhqJ^3chl?pD#_eb{-#;dqc4u&`U;z&^_Is(%@JcdUta;Rt5bvdI%b4V;gz|yAtW!w#Yh*pZC+3e%i)B_J(RQM1H0Q$%mo-*eH+PPB)ua&{tpxE{fXImf|M^9c%{v^<?P`u`%-?01fjt1)MO8jc1}jY!Cd`B=sL4C2gSDja!N`s~ig7dXHD<`%UFb^XE2E;AeJr9a*qKXe=<3!LO1iztuIy<UFq3$SNYQ0Nj?y&-okj@wrp(ffSZ}bDyW6%AEaj#xu(7sKVP1;L2iM)EZR4eqLPg<@piU{EL8azngscpa{kzXaG6*0LEtOK}m+SeaXq!=HTHfan3NXa_FqFg!wk8y|+4e14;tWSWE8?LhrCXH*9sn#%I!FAElIL>ylN%NvhPQ0{C~z^pDOM3T5y;Z#WrWP!+iXnmUFXcg##^jB#0asB-dRO5tB6T6^AZb$y(}7B5Mm}q5yDU1Q89fPs^d%Aul0}w9UpQVeNibeuc9B}UbSYL%$Qnj4s(LDQFui#MWKocQKSR0SmvZ+T7IU(%9}i>D_W9qW=G+LQwNM;p+?z`&HS!JJ_qS3MB=PTL8f(Y22T~j`BPa5O+uZFOHEOAfHlY?jZ?0gbQQWK<&-8Z^bEak=v0b*$i>}#oEf*<tt;VxN5)n^D^^{@;`C}?p)ZNC9aw_O0A05qqbUx+E(l=?1O(nA#!$>b4++lZ;-$KO6u_X48BY}Ne#4}vhUkHjGOEa{`yenA2plR%+=<~y@S*x$vBH@Sl5Vml)JPDHRSDFI!>+4sMGvYbCYtkQpgn_jggPWk?$eVOkJxFFz^f|kWb<3#;?W_gjr+Eo8T!c}(G96m!f0P|1HUP_BE1m|;sZntc-g?vYQbuidm>*_YA%W)m?6z!=`caTzgCtVdvgNJ#Z>!{Vjg-`jx=eh@h8r$-I7nOhes5vRZMFZ@K}a2+~mXBmBsY~b0S-tf3%pv+L)!1Mfyxlp$kU%ka-%ot!g#frlK9#MEc7LfiFRSL7$b=UBz1JvdE$pB$19ZPt8#5x{Od@x&6vL==K|D?3uE+h-b`)he(urM;Pg{MV_5^6@Nz(RwNo2RJ-qJSo4sL)l~E?fWrhzDA1fUl)P$^INLl&A?P5~w$qnTqYzBDaL5(6HT@Fi;>6gWb0vXV8OU?j0GAfRxrQbX6Mc{fv|NJ{)9TZm*med&b%t>x>&zR{UC5ChAaKp|+Grl-@++PT%^{Lz6<HOKSRbU>4f;6~>SPv%rn*KOTMg-#lhtqTp4C$qJeW)#cqa#QJEWqQTlXKi2|DTk>8g8Da0bhPn5+wgQ6};tAl*!}?|oB-#1JrrEMKF&nu_w!8g9cyNil+9=~Xg70mJerRY+lYn}}D5LJDVnvdo=#{bdcX;0(=Fo^xfxT^hP|GV5l7&kVx({0g_vq~f(o7%xaPQZkH^&QD|XD680A&E#Qb%!>FWtU=J3NqTnTf+9BIs0}OF2&mt%EK|;&4+O1Fmg<ybA;8MzIu0bPkDQV3=_NxH`U|zx=SqKSwt$Fcx}RfZTh$;ISbh2#6Ge(D7>#-U)y<pGELNb>N|8qLcDBeaxPnyY6yeogH3>9hYgXvR0ereVT8y9%P=(<Eat0#sBU!q7D{Cs0LzLLMok@8Qp*r8l4)kW<P;lTCAfuSYpyOP5m1O773BSS>0reYH>Z}WVSH?NCSZ>|?z-(D50MKi}FP{Yt3RWmnP~h#|Z@*p-3%A$c5)KAap{ls?1y*?)@;Z&@6}@HXN!iO|Vwxb@vvVyBK|wB!O1X8A)>d&o`lj~<0Hz|W(d>Hn5?5OItxIck8_VH@GoOJWA$j-PXpVvctbS32Y%5fF4CJ4d&$??(y<7>8D`|D}u;04TS^eFr;p_HThc3{;891?kDF}4D-gWQ?V6f!qA&2Q{t>s^*SWxSZ3aw~Gs|B`qF$NsMVRVOIMeEeb<Hy+BA`2MfxctlqK>?`>I|tI7YETeNX3R&vkVp>Kxs)VFIyYLYob#umMUb&W<09|L@iOFuh_9+z=Bi#2euoz~0ZCOSS5==8?HdPe&zqBE`O|-SE`6mQ+FdR}%sk$jVpmNF9_LpwDy&nrK_El%n@BB%okb%4w9+ntcd)9KF#X~a%OENeJ!ixOiGyT8kYHOSCqgDUQj(0VYJ)6-)O+(?s&*+B!(u0y|0XA6vZQl+9mZWLNgdd>vu^8$=rSoF3-mgmp%|gOl25RWHg<(ErD8^A6Nw{uTe@m`oN0zFl=^r{@CDeY<+?qczk%C8#(*7FRXl}FEn5Nk&BZbI`Mp30u$|`dtaAXCsF{jJUIi?T$Lp0+t31cm47aaBA{7@nQ`KY|cB`QorCs4G&hV18DTq>T=HV$o4}DZ{g2P~9A`GNXF9>Upft%HqtC$6F)!0_3cue0S9VDt&XUqT{d48<$$UX5HOZU7J2|=Vn-Z;`yN-LksY25Ys5`x2VG~91HWnxR0nnt6P)-31xk|bwm&tS(x42wY_lbk9{>bxmbC6%>MJ8kX)=vkzgEdv)`hu`XA>xz5C%LlW_Yn8dME(TpMnxI?L_3bETj5?#tGNi|^Zik{IKwa_7eUeV|HT?xIcot7qKoCxb9zVO^IE%vp!|CuCi;Zg<kqc!8ijhBUG}@E|%(-EPy5<dm!j-5Uq__j3A;9gV9GRx##L1l}TcS=n5tCM%`5G7~T{8U(Jl}%PbgF4+I4avVPv4kv@w{!1E$&c*qO!QkFTYiwGp$ZMKK{`#W>fFNPmQg`KYuX&1f7_fHeH--iH*Tt5k~S*vrqf>m!WViVZ6;mq+AfZT!@p1<xG8)w;vsuh;%vf((pdX3K==QR(hPqZQYcIR7_*CX4+NSt9o0pdMsCM%N;RU23kvda}s~ut$}v#n1#%RBB%^m_-#`m=TRweBBhuNl^uCT;#cUU%@4sf0uz(X#j5&__gkFcS_8%97`Xf|-bLoy)-s_lMhk*54>l4)njvZTGCPT1N+^e7Le$h+D~@XxfN}O}zdIL#5KDvx$S%RBZWNM)MZjEBDTqa7J?d&6F9t7!_uT-c%rHZ~O3D^cY4NWxUxS4%YN2m96ZJUdBmklQnzkI<OFn<ACChgF8l|8T2+s`kMQZ0%mC|yR_v{gTQ4PjIY`aEI5PH0j1ov7`Y%U4iO)XV@pO$#I*FhK1q9Io#%giTx`Tv$Rlla3DKw@|8^GMdC@SaRq69w|*2l?UkiZIKNSU1(lZ3*gES<3jSlYZBRkSS0AJxt$b8l7-8;T$T`TQFr|E&7F{)33c94J4hX*@<S5T=<V6b=@F($0`^$#k>;XSGCDie(!P_mN5ON@BRJt134JZzaUu++^|jU69^Jm@7j45k(th!gwL+dhG65eSJQF1qW(1VRh6_$;HBB!QEyHovn{m;{xD4j(ips{%oa)Noie~~em8K*4MY#9WSAu7tUnbjOBdB{KHP&Rg+pQtOpTi#JRNU>l*POT@GXuLdMERG58joFmLuhtl41<$?xnSS=WtTt6N1D_C?r@E;Gfj-MNKFh45D>@B2L9Tbgyaeu0kLx^M<y0PAqJ5AlSxKg?HIf=Z!}#M$xt)Eh{h^5>@2BHQNr)Xse0(kUzp$mK^rZ9=&K?L);<@0$Q2F@`!W|KKB+T<TV*#0M^NC+zEmU-md^K*CmBka^LH8!KA{=pv$W?&T~^?jv!F7xfM{CDjJ}d*S@V)=_PG9S>Wf0qyRG$YZAt_PnUBn=QW=tRQx9ag-^o2-xei=Ld6(AY5A4<AZZ1f>;PsflSl3qsiW?^Mx-^Wxqv%O+&G40=mV-04ZnjT#2K>b>H6n^D+tQ-ST_0^Uh=DVwFYldq)<+A00N1lZggF;Tm_rQ#NUgnjZNr9`mMicOdy$UUGNlq^i9C7;HpE#iRpio3!#qu%Em?37%WBDJ(L#Nc2>82<X8%7br+2lC2A0xicO`0)B?}*@=QA)B$*7vm8lNrsSSXzU)Si-HYUpd6c|ZCMMfhZ@7AUpr6`P2T(d-2_KbHVZ(HUTTt++|JWzqLR!$D2a5_5n?Qo*HKnP{p%$XUmR4IU(w9Z;9`%*tfk^FEwYNm~(#T^)nrzEZb2DCixOTZD&H1eu+jY-n>MTz8Wge1&ZP%bB=or0Q{CmlhIW@X#xSa>_s9W;dU>v5=7Qhw&Nsh;#S^7kW91&E)BPqi_-FQe1|CY;;q4iM5Wy|>RyZdq~CHdb#VE=)TG%3zDTz!W#u0b}1|4XMoA4P-1^SOw4WkU*vaEmD$-?`sA6p`Ln~idLTev8Sl-z8E>E+*oyVvVf?hn?@9_=>!!7(J1bKuuf;~s#t?3AY3^A$OQSvyp&JYfk5PllkC17_3*AWKgCu5o!jsj)DzUuK@KaYuZ#UXI7LkARIsew4EHkCf2s&3A>u$Z$k`=XFwhFyEoWfYC2*|UF6A5AfUFxPk1{#;viekNm2q3&a1N|3yEKGN2v5&F;G<#_!d;9Yr=w3F;T0%~gVe2h7#EhCxsB=O8d(`LUA+~s)6zX$b>q?@5mJc%k|d%b`CnC-J|>X1FiyoHhA|4(QC%xpf1+q;LZ4>V&lS1lw~zF-@?CcWq>IXR6AIj1;ot4JBf9=D*6ZIE(@jrSj|o9%H2e}6RoH`oK@*Q$teX`LpP3l{N|dou=V9DnrTr;X53lZiV&erh5^2-rnf#E2ap^bmfd?Qu!uHf8boZFnr{gdtMJx2QbFltX?~davl0q?ptNjs!r5>ZiY$T)kWdX$7WPKc4=cQ978n;CPy>A4}lPV7a@d6wc^M31inOqsbgZehk3aHC7g7?TMKGKhc_Q>@JahI6OSB8s44yt$)s=5w0Mr+}}JcWmNd6~B5Tu;<@@7@jcD|<agTIR)a#hDW*-o?hh#XquVTxPL{ij~ecand1$;xsou6x@uB#=NvyYeNyL8x)UQo%>U<6myD?3j2W>*DX$=NmZgp9d=60`6x_|B7g=h%AQ42;4%K+{`~3ZAO7+E>-moHjGCpyV!Xx3Jb5Kr0}pWJ3gBY6@$qEiF?c$5--2i?i}@A*xCU(DU?hK`n0^45NsIs1C%N+0TY57Uq9M{Rk`$lK%4o?ElQd9(nJur|O+Donz!B{tq&#3F%$?z3&#mQwV#b&^UcPCzzaz9G&IDQHtF*VBj6?$5A~pSHRy38SzJpp%9MgjF-OF=P|C93LrM0z`*s*1^&F4e$D|7Fr_Gbq0tkl`^BeDJ*jPqdlt!=hhdP<1;r=y`(Q-2h`<{0CXHnx!LmK;CE@D<A*1m0|-xx+V1*i-BCmEK5Q5h`k5FTT}%j#IhSW9<b85QP~M@#X1IN}Z|!CdUQaMOg*A{;*&*a%;QzD&Gho=dT1i3_PWI*@t3(s_ixQ#A!Wlx>Wa>Y;62t_J_%=kRAEuv0q*e@-gSw)N@rB>oSxZoEiGr;}6$gh96~bO9DFKXT7bmmOSy9wR5;T#B{P62#<v*(-8u>hQ)!G^c<4s-CE5-wH{Qi*Wd}I<oQ{{clhLG!PSBS1Is#Mi@adOSO$W)Y-`eDluZ#N%lrp$v&x|fhy@4gCz7z(%ne<{q6`32P*GK?d3n3G&}cOZz9<&bq`%Z(X!^}s%jtm&<7ndO6L4SDX0jmeu;WS|l7T;6XcW~t5t;S7YJG=~l;T$_fF<i-J8WR#lHJ!b2C+PenUSnb)#lGJPiMR4x~PC1o@P#MVYhPH&`bl3^8kE08%{kC$eYtJuMbWa$752Bn>{GkD-N?m=R$Nhu(_c9!xE5NteFnN_%b~>KfM0({=;kd<>}G;@;oysI{y6nD@hbY9s3M*<tbG?U#1mMq!9*YQ&v&h)4lj-W4@Qu_%ATwOvGM$Tzk0mUuEtE0XyCY@(Ny-ey*^QDAirR!ML7_aKid8WxW>wQi!NN$x^>;z9XE2<o*6qb3LzrzWp)k(^smWQ^B9`fhhn^fVRcIFtVrfHon1$)O#Pf(^s6M_yfadlOIf}9Y{-wk=`<B`}FDiPao{-8_fZ^%gfwFtnLDCf_J~u_bI*1@^7naOn?5E_rL!1%lj{r_<EX1(qI4ikG~&}zj<v}S4P?Ak4g?iz(4!)+l&Tr`Ng-PBv2gvt~UbLr(gN-ry^w$d8x&x$OpWf^vmbV77{8i9K4R?+ZTySa3&%bM+4HP&0__zWy4s$Q+uCfyW!lMa6SRUYF)lMKHv)t`R&t^f1!qS!%wiuE<>;hz~C6`Cu{GB<3(k?jV5TIntlxU$)2o@$D2Pw110Z0gl&cOS{Uut*EgguIsOu=<-*|t!1UQ)nzL^;mx8TqS?~ox)nH}qQ~%za;7r~L?`e$FyemvITO7HB?D@A>aTSd3d7uj}`(nbFUUA|LDl?gHy(?>!a4@l{Tfki=l)TWcPhdWwpkYYA+0`brAj|0FLQYn*vP4OtrG(l&R()rv2uVrZvZLKelt2h{($(TfPzFE8@Z~iCdrfsP&6C_TGu1VV++W5CezNd2n_d2-15&eOqsDwLJx7fP%)ckhWba&|?anI<GnXIgjdxK!U3s)j+ROixqTuDwh=;nZI|9AVr>rv;$qM>Q4yAhAf5tQm%IYhLjxh+UBLdBGe!~>9tdYgOucP`+Kd&Lz4Kgub>3~gdOTgcr%??B8<Y*~ZMr$qCg1uaEHb+B7I@k_dk@d**#mUGlBl8|R`Ld=PFvrRdV7~{ZP@y+tjFAVIH)>AVTftOGc5shtJ+6oHqO8M@w#G7{XRsxlQTRZB_G>k{d4a_orwl~M_V`MOL?JZUt)Q0LV*B^P65^UcTMCQ-rBYd_epm5aTkCtc3B>^AmAnSSG_0v0E(`;kpnpgDn_|)02x8Z6lw*x1Wwe&?mRnMkwe<oflT3B*xHUV<?-!S#XS0?}A!OtWR9}MLXG7Gm6$tJ8ud-Aj7oUwIqVd48Wr!fr(cBZu^0hDOXveQ>L=Y?ri_X%4yCOf|em9``Hz{%rUi%<wGrp)3#$|+`a#;8H4G^c%*sd6F-8sx^MOV!K!|B^8IK8ZclQ6mCVVHzk5jH?4rjg&loV+&7)uRL0@07*|cMND_B;p%=R61~pxJ9QFLz0hNgmjH#0)PQzm4F9%Sa<zUH59p&EP>l76RUcrxDaah4I`wlfb%%TSN3`C!0RY{;VB4A89#1d_R05Tod049@Ysj5I1oBkC+~j!rX`eOM_~H(K>r_7PxdUBKYtFQ-lQ_ArPzijP{Zf(4O%;p;ZW)Blo*t*5~OB~r=~hSw-gwS_@ZuVVX#ae!AgrO3NNzf8twhb<vkPlH}JfI=wj!=gz{I%W{~N)PoCb3<>QDKeWvRO@_VJ#Mf0Zhjw>;W`$X<nS@l+76wn4)a+dCN5&Zw;eaUhp$&u{8yfY4k+zL4Muv2<kgv}Zuo06xJ`TxIoRX{EgVQQ*s=8h_Icp`{KWqNq{Vv8=lu%&5<$=-6dLj5x?DqeKD+psv<z}O|vGX~&mHMKoDV^A~uP{B9X$}ckxDBjgv1Ybj^H{;7}4HXSdZZIIM4|L>XBv4dYb{+bRc*~mpxHE~vIM7~sgi^NB#2Y2q5NBSC`ktheyRswER-JjybLaYgJ34+<d|<3YXyk-SMWrfgLz%-a3cmOZp-TbUJs@l#P>>>A--#R}njMTXX6S&_3^MWE+-vJmA4m#PIqb>hKI~j{6XGJRx+^(&Z~3b@j|I|s7z4FDp~qvDb-v{v(}X1s6x<HT{ZWJ|(jp^%aVn{;uq8GFJ|$qT22XdOI{eT(r6OKwD)7`b@LY<ckO<PowfL((p0g<-#}EYFp1-}t#Pw!#uR`lB?cF0uth3}zF)$9<ii=pXmav(I@=EB>OXsh1_4?I+m!|neXTJ?yF5bJNO~)Vg?u1Tp3F}OX#*>f-jl?i@iu=sX(sl)2%hex?3-46AmzjnR%%xc1q}%@fwS~HkWYT(8t;kSG=+xQCoUYs9Sd}<OtAF7eO2{`QE7slgD@K-iHq4T&r*0?N9STfytkx5qYR`k0sr7Q5P~#|Ia}q7Qt|!4G#Y!P|c3Ns&9%2`Qy<spn{n9tpB&A@ee4aYi0NkI2YGbJzyc+yFb3}L4Q)W4p6U7Tv?p;Y$#`A$lGWR0$fhyQC2gX7x@VOm8q7g7RLYjK_HXAc8l`TLp{IT9|A#bJbPNta6bI<6MyEIy;zKZ=O*tKB3hcpyeF$~#*(VMuC6$4>LFMG1AkxH+ioJCnHqYxT@SmHE9-lMk27=%RoU&C;dRr1O%FYq7ldn7N(HsKPyv<r=>*)*0$0sJCBRJ+zoK6$2~Ieh&piM&hO9H(4;w${Rl9l+S!LpHcurP(yoc>H5xmdCpz6hx=OXjNE_y|Tw6F^h7y6prrUxOb!ld0K@lxyx4K-1t3UD`W;RGX=L|eIX{3tf#ougXI<Q5fBk*OM|J3DYwphOU<Y{{@sVt#iszrL?)%`jFr^1@R9GyDEBw8NyLy*JogtLExBQ%ChBvZTXlD)Dei`4>pI6c;yLoLv}Os=CslzrlM(??<!aWFk2D1QRx$4H{-25ILI(f<f_M|m_(b)Fvvr|^Mv7Zx`_1@|!|F(Yh(;u%G_Q8|wTT18ZL#!DESMgW5lAs<7^D@x+d`G1pAhO|m>NFRwA+1D?g?5m8m^i0McCU4A~>XWe@#`YXtTKMjDhSJSasW+^mIK(<5`=Z0%FIQW5+W^LxhBe0;JQbJWGlG@?2_cMoG*V6BLyP#+qL-ICDk=l1&`bMt}1kkzge%E3}j7!&A*dK;-}csp%R(e2|uVWLds{#ESuvVA4u%J*&FhSlbmK<3*?4^+72vxu@(7=*(&CkrtZsT`LPV&AK4MOWKWuztFq%0>H{M3@=A@Ta+c32Fh_XMnw7tF|e0cE|?W%_6wMw1&nTem3W{?d3+4GkixTM#9@VkRb|PwfRlwZCbuh2WCJxoH*fWs{Y+LWqMR8YIIWV=`{IFKtlL;fE*+0tl(j+my0u(hnv7$fwN~mHQ#pt88lw%cDfxkIAb#5md&l3teEG*&cGC8Rrzonm(uDTd5R8X{e!vy;$2<`@d;E$YL)5tgAcd$Dy7fNq0~$-1>B?va{Qi*4M?xI!Gf-7?A^Th98*h6L5!z(Z0yz_y={ABh^4X5?1BJSpoC{WcbMy&{qrwc7SjZ4|Ojo106N02;<ip}0;Ei?Q=khW2#=d`Y!s!YFrW1tz0sRo56K(?BZ*F^s1R8$yk96XRyBsvwqWsCdbDk%A?Af1p6<h^MYSE}E+?mncxAW6m%17&t@L*W)L5qAS8+{&;O}D4v&uTy~WxF9c<=#1ufBCXixsefjL@ixs%ecpnW**9gEH*>ut1<^91FW6QXSw@wvQz~*mc3Ph*2wvIsO}J#BWJe{Y%@YhzGyn1^Cr?`#Aww#0D<7-ejIoAA#WBOwXOp767>Wu*?1r7Ya6y7U-j)dA7>ovGD9LJpu<sf%J-R@fN%$yMQq(A<k2W58>(#C9C5RRr)ieA8%BrwY7_%;^TUMq;MnF;iLUV9K<D$9vU-K(vFrR$BQ44@Q8?j6aF%cu_ly7VelF~XDn*QhgerKf%h2`ap;AEC+L44dRFp(0{28=p!f%*{dQrY>1{yWCo0q2^xOKG(*goe=NX}D^4JjeOD36E$03Mf`JRUb%KeHukY$?)Aw#n(kg3ZZwb^9R7haP4;WTOV`GU4GXhL1O%cH=w7l<DIP*+ig@LDp>zB7c!FpDVw%NufEieO$nTKaJ1<K$3=%bEt-39$NZho5m3UC2|FMr=HP5utf^uw%(Z+`TDl=oU9u2d{m|Z(;@K$ECc8EU-9IVfbH#>-AAkJssc_}wvBHNMqpE?d}%)wTHqXB<!>0$u<BDc7>XYE0W9!>x%=m;0EqPzYtrpQj5!wODZI()9$!<05o__SYZ~~v1(|!$Jt;8|O;73*;xE!J2%pudXJg0Aaunxeq2<&<5%4;pE@!gjVh%x-mGfu#SWyJF7^s6n<tWhpGy|#$#*Q341{zSJ&p!c61c4k3-J#((=np9uu+%JKD&JJ?wqnr*_G^p`F=~T~R#c`TLJ|}#7&Mpszhu`)(ssFX2P&C>M?9cPL`>cja}g+&AMoYFVvGODN1?*?3=$2>&58h*%N!>Qdr`^Al{kGjH@#d;>@dJ)A8vR}w42vbCiIM={Vk){+qo94v&*;u&7`dBX-%x6q!x+mBgxN`d9kJ%Fi5pogq(^_m9h?i-iwC_7+K4B8cd44=rWvRfo}C7>kafdJ*6+DEk0xHwk@X0GAXfT8W{{Q?F=eB6_sd-{DEsXen%W*Zp&WV6ZVp0jUY20X-J++PKUoE@?LyHRv&biq%}Gl_cRbf2cYn;nlow@kJxF>_XVyC!Opa96rNg;2gZd#{e^6hhjRa05#Ffa0-a_f>8*u^6xu7u16iB68Jse@0Yc%4vy?E_Z|!Ga?GJ!1!Q|L#dN%1Z87bID`WW}MwQ0SXt+#RgXcQsGEbk6ph)Zzds4QdzYbwzGd`Z9z+GeQlv71gzeMDaibtEHG)vXJROfk9VYo0a)GRNfd7`?VN6=$~BU;&-e7`3OA4Ia(~5;WESI5M5GA$^h{FzhBB9=m0+IdCS)82e63+0XRwDOD_3rwQ2yv<hfUtfQHXi&uCqzG+?JV=ysB=;SR4J~JYjWQ)H36DUjRSt%`hhdEE1I=;HQC+t7ix*W04+E+5pmk)1J#?=ju<CHkM6HOBM_mCpYFzOkm|FgxWf-8|dB-J4y!XLNvnKm)@^0HLA@)w4Iiap{=rbC2tFX%Rkbs<)x>DZc+ql0KS#0)}a0WxG|K#-^!1Bz&bo1-kLO{1iTK%d3Gy!M0R8!HfaDo<g{PB0<}C}6<qyIyRraCL0oAlJOeYHaew*xl|RfC@15%>&Kd9SRrkZKx^fC<`K4Ka4Al&~&@jC_yhrh90E14N91eG6;2ixD-3ro;aN0naHoq`)ql8!E~e?*%`J2vYEPcApkNqVj5zgJjjara<LUP|I+u%)*kxPQkF%Fl!Dgd!h3w%g<-33UMFIUuL7iFXRRuQ+}D<tc`}Z($J@`m6Vp=@J9YZi4tbx>N7L5-Q6XnN)VrkD|8V~8w`-jFV-U6kxtC%8l5kyGV!h^sY@Eg(TB3Hj4BVP&9EA0}7Ne!fLZz@>r63NuWRkxQ#aek6b&Q-0I4JFQ%TW;9rkLGEMG9I)3#VDB5YTgJ0%F)fnL;@yQ9){7NKPJ;HI)k9iHG+Ui#48IpBq-5D~K90Mq;MzGAF`BK#W{MY8|sxJRb_70rO!;fm!?tAEteFBZ9b;*K+|}9mj|Veo|Y)N|0iwX>^;f0g!Ttl8+ZOlSNBNV#t>(z9d$>Sv)C?GukO9NZTl5hBuHq5KvM)lP9#DF!x9yV27JNsdzaw7$Wg>_ti^&{rxwvT`ZxUMqEPoE=%2|$XSo@XA8uvr^hw)7AK9c>YU!pUOxnY?y+~##b|L{RJn8jgC!4BU4zItps8$CfI_Eis*ti7j|G>a0x#~v*=N7|lPTtJH{iip3!nb2GO+vb{x+8^8^8qnmgp!&7i2`zR(sB*m&^5t=j4NSB@8LM99g~$r|OZEIQ4_l&1x}(y~>NAc{MO=Tnm+B1MC)HVSoj24`>L03##CHLlpR`As*95V9LH=*dej;&-o-(67~i@@z=IPRLBzBtr78Yu|4paPzp)~7{(x%<O9QohiYJ5%rXmP^s1LS13b@~abW5Nyg}45bQ1`SQ1yNU=_T%Dw#+8Px);f2$I-3TfOd2Znz1hLOX8JkpEO{Z>0Hvam=)&+Ep|t)%3Y9r5o8~%0TU?@P2bH(3(G~p{>@sj<5a>|fq_>_EH3WFLH3qwaB=KKc`GK9L_fiL0+6vS!|>}<ol1mBmhhw1d(ycaVsVkYI()iyQo_D^K49WKD*PF8XI#<L>O2>t(Q~>IEoS@STDMGt8VBe^b@3Lrx*|J*iEDD+7sw>f$mt3^o+@~ZwDxx%z-dgwUrZw;6wo-Ty!Nl4hsKHqk%+JcSXd;4qXBYw-eOozV~zlhp4(1FH?&jJ!DcbV!?^hjQvESWpF4wNEev>cvA;`QfhWmiF;=J}0p82Iwh_qZQt1xdT%As`-!<!1abgnaFeS5|i8lY7k&weQmGL93dpa*;)$*AJMIasvu-IYL^a%Y+$iZ=~N@lvUO{<;&yrQadCL@rhSQ17&6hz;he85^c`21t18m&(=jWp(x++EK~j4Okjm^2hY;&tYdx~#fAfs(wgz4;vF0p{FJt4DO1kP~yppwmDAUx--_5qkxez;@f+f#uPZuo~L{6@;Z|QgC@}O7bpM|0_atq?D9aDX1cR41|?SvETQ1%M&EakIqMFnU>4$rX@6^BeXI|_>|=LhNd2_53y#eS>O6LsP^8AGaPNFh}D@?SXD}OpbBB4HsXJjaF*LYc~sKF@V4xZ0_393r<hoPh?@u`<5743Ic}Sb1m7Hvm^a^Kwi9E+PqT0zdlwI4`M0zFW7hwY9_1!dhVoU|DxgsdfqLR9MEI$6Yf)+mh*4R=79@0fNCM9f(UQKl6qr{*X!xjxGtH7r5jO`t!67QVf0$OWib7Eh9s(85@^dBD_2gk;(R+-eHVSW+T3rkaGfF--Gqw^LA%va~NwX$;nYP1O9jlNKT*}I4vL?!4*tGl(sul9=;`pj2IE8LWIi(4Qo|X9<N|j<Caus*KAdQK6b2S|B$k^&<J*<0Ro!;Rj3OuAS+EbJ3#NZMv8D=$Nm-Nxp5nxw|@CgE%@3EfIQTN&;^{~k27Hc(071UtQ#e~?cJWv%3&7;7$A#m0p(I-}@Y95`!feu1(GPY_&2XD(Dn8U+vt6fD8s-_*9qiCQFL%*`3&eLV+&zmspaPp~garcih2Ki40Zf>T+<ThmgsWleqWMIG?VCv7i2U1fnD{dT!SV@UW6yqpEn!{34g0g+BoH){JLJYyQ_mJ)#dR2~YXo<TM=hkN6Q={M!nQ0Z6nteQ$W(@Om7+qOhA~3PBCH6;q8jQv)g)7o$YU)}rc!x~3z%5j3-8OaUz$VgPRtP~!2^UbMS_COZlgmPgR_sGqW}Zl)*oGO<z%uKVo6@DBWvH66Lx|_AhlfZ6c}L*qk~7Z^z=}O%2Qkb*UXJ`|hcVZz@RBUQ0AbE*+Eq)#)m}LZK?fm`oxX$`l3=-GL&mqO>6b7sCWiG~>ju=CHl8I0xU^8QYG?v6-UmrJ%QYy=O?}i8+s;6!&ahczWV#`hg}g2UWU6@r8y%nAV!%s*_#x3&5nKUb^g&>K(9ND14w_mT?XqV`znrZ8`NOk%>SYI$$rER3FmFOCdbx9d>0&8Tc8AdN#N~ujS~QSKMX6}_lbY-#-AuFZLla7|*WCmN_B9yMRDy>#VjI>+3K$IgrxFMXfR<;eLJFhVM7&D$I5_x|W$v8Omyuh+8JcM|=R$`2G<54^*3AT;*?IH%6`q|*Gipj0FCZ^cGK^x+FJoXPt7BbF++iZjI`Q>jB~}~+*qLN)7cK;1qlVhW1-mfnbChK!+B12eEyhx_k*p8cew<@3!l>g6nosW@BER1)|0g-LrI7CDSlL!Jdj1v%KZBD<!32Yb=U?5Ni)LZ?l;DZ9eYdkkcEJ^-I+qn*?KqQ^W~9#JGB{tqPQ6@!|CWbg5wHL%F`S8m^o|awHCLyyrusKTUad=6%E^W5Xd`>ln|(vCf%k-r_7<xh=US{&xM~i7&p}P#%P-E11xf4X0VYGGP-vc2X8A5#P%t=ICjake*6znqR=AA@7iKUJ302jMSWtPNk<Vs{#WW?2Cl$SM=o#6|X<}|57~8oDhQJh;Mx~582-{VhjJ}V3p%_z<)Mygny(E_QeCwhbU9LHtaAq+uBr5NI8%<15Xw`49kZpyUkO2tPGD>&7rMD~LI7y|OrvTQi&sy(R`(EQZ9i%{~xWF+5OjMv_)~>@oP!day9&(soW-b3Zx`MiPR3JtZZ5P<y#r5EzhL7&>yEvUXdBA#pH7OFJwTf%H{LBYI0qGF?c|DUcW^hNoVn~|SxqT!8I(JvA9O###4Un-F<7)27=CX1LQB$oyLCcHQg>JD@To8?%sxu>a7ANhao8w^l)4x5JzA1h2RL@d{xC@Crw7_s&U&*M1PSvb{48<pVT3R|&_5{30RiA^24PRIqP?6rbmPU~1M;6Hl_*An0Gbxcm{X|N9Yy!)V#;a5vODu%MULyBPMlQ!tGkJG~%>8ldaFpjv>*M&fBu-#k&${#v!8BnNg@ndaxkhMYM$oY26KvOvePK+g+>yyIAzhYT?QZJ9rdf@lM7ym7YXGuZ?&8y#9Jpa*%-9iH#dF$}w-vR(wUFi^ziS9emMzZP=aw*B5(2>lH1bYisiEpItkgcpD{#$}D=uxOy~&jBrWH6!`@vV0;T>%=d@NIYc>2&QNU910%&iLY38alL@N5vEn>Cu9x~eeL*j12vOqn7bBx+q}FaaIdeyzaFJ%JfZ1YMq2AR2--4SCl{lPE2NE~jzd2Tuq<$JsE)?R1wd^=cZCQq;4Y>sx}Iojrquh!`4!-X=L!nC^Kqt(WRqh;5tu{CVyuJjTyxF1EC|hpv1wo4N&b7<=~`i(6Cj?Wkak8l0>$;?F<a)kKMYx?-1yBx@G5U(9%U5zoqM4La618`dEdA7PnCv?~FOSHpBKaE!+OX-W8ksg-jR40T%@T7r{68>E{9f*OF=r0AEXuEfQiCtFQUS_XUk_TAThPR@cwfk?X46ft&1>sob@shJhe+jhg^?lLHdimUndR|P<l3mSGk;E7WbgSLxz;b*dJk?Wy$Vp&RxxY$A%gIo@V$57Ku>Gs<YwRS~3W+I{^NG)4Ph!ocCYiMNbT{TLi`jD<i-UdD-SsX)_n{7s~SmCCv+*K!TgqU=hj+6E-*j3yb%bnXY@g>V7Ybi{Q%&&VhP=d~w?>N70D)2h0&MgHG*}-R|as?u6eiY7#LrnM;>)<;!ZJqf<E~~fy#e2hixg8-E=dta|1z{*srZL0XzLv^;3gl4JN3E!DS`~=*B>dxbItXS&=ymLqdeQ?Ol63o-pDCG(&k4(K_bEgZuaHUtQvcU(1p~lEIL!tKV1~)`#ZPts6^s9bc@8)Y2}TOe6gw_?H(yA*rhMWiZ5h84DS8BAE2DPOA{#O(^lYHMyhY6ug~yqT8aRI00`RQuF{P_jhX=%2@k|6~f)N9aks|73J+s^Yw{1bhADE```v_k~QVvyx$+Rj_6it4pm1rEFc*^ar1g*8sg;|btlHA%CXR-}IMACO+mT?V*Q07L&wL>DFm#t%$p~^%BnrEk$qUvshSVG;nvn#{)7^LZKx{|+r>fgVhbL6%=uYVw0@7y9xEnAox>!L<FdXbW?p=~d&7K8wbN?*U8&l2@LSud7^2!K}{U+`B<auek;R+6Lce8yrJxG7O{DoGp}#}O=;%4+r=fLx#$7q#Bd9o_oPhUVhaZD^0^2S6E9&`Q8pMd0}~_N2PKQE8-9d;%|P`>VMqj|o4`lR902IF3IGyRpkNAmLI1>m?-#jeSxgdFCvU7N}#F5l9M>pCV5u_h#-Vvg<%Vc9B`5*$xl`zyNQ&=$TDM(PV^}^A&`RGUwV6VG(@VZCs;kg0G-t<Mtx~fhs7oJ27Ixl@nA}b?tdL<@C2BhL7C_U0%>U0xw{$vO>p`L2v{JmWqPo?X~Y}Jz0szO!mSx{3z5VNy#VN0M2rbeV^vDg#PX#2=SrQayPfPD8Y{@obN^JXw(NuJCkGwFt3na$bB3-`cjc)D9Zt^KXEz9rT*C+KArJm!7XH?%hk^H>_Chj3gO#V6de>f8&_1fm9-a0`y0i20!v|8B~qSP{9Rm0diq9|h*{EP+Y&qlAAPe{Rj@&!YO?e{%7subVoE9*<77&Np;wYbK8w{&9?^9IJ=-lrihd=CJH@6_0jPX}y<ekTe66b@9L`Fw)*=3!WeZv5^<S<;vVn8x!pNuDfReOGqcpE9NsR+Tmavom?FF7n8l$cHhg}z8xP^;TPPm*MOKdoSU1ki$TCA;-VarUEZPGSh6aL|MjzBY>I!CoQ_6*@s;<$qWZO`~p(TJxGd3ThgCF4T0h$tFr5eX>8LlunVl%@kkN0*?}nN=bg_q5^3D{oMEG>*?on!E&L<EXoMCWgqCjT9q56h-WXjp=?J?S?ar(-sW;;<XNI%Yk{5vc941huyBJFii`nSS&6FQ-@ZUo%d~PEF=hS6Np&OFr{MU)%uuVuSiTPcAb@S54A$ebdB;HkUd3x_r*{`Wyp%U$0DSXk`)mnrV~_<sG`+}E-pz0A3Rgx8s}%GojzuPd$A4#A}E{W`0X%=)06yMSpD~5uM`B>Cx?~8=wbgJoFXkk)y%R%QJ_Ycz`J0Kx$G6+{{y7LFr$+hvzKb83YAR5C=y#9=!~tGW>QsnnS|0Ht_s{32Es1-2oK)pSwGsavk3!aa@VVZfr;<Z<oZ=U+QeytT%jDBIt?+;kH1N>!;q0r75t7#oUJxeanxXa`#FkKCD%k0ku1Qw%r&<nNBjPfz6QCg8jmz1Ij*<>T@}{Hj*Xmar(wPRT`}eJB*&OuZUzD`Rfr0E5a3kek&DHMqA4zuJ)Z>3Dv`(H1}p7Pixv_jw!_8?3J=oN$n!+0%PEuO9|$?HJ+%m*J-{=U1s?B}Q`T7hr`{dM@f?K?0oO_+el$I7hsjQ&IbNByynBxLUFW4!ycai@0fZ`2P?My4QFQ`n67zoRxJKL|xr1UN&I-^CYU4dJu#I%SphPVnc6I`2d|!quHX5kjNNBY>C>1%?udkn@l)~#$OyPc_e){xjfVJw8akT0NYsV&Nhfh&0V)IM(jN2^sRB<u+DJCYQdz<Fwr-DJO2F<MWIZ~^UNML!C!=E63wm%hHDV_MJkcP@oXK@OtlZIK8F)icc@duLeP&8<P=Pc|1kMaNOpTGb0*Z=*?m+Kwl`PxdEyLgL{dGgw%Mm@l#u*1dhz{)*sw~SWlq4zC_#<G}SA%Sa!EgX#GFBD?}09<JE-}-P<&P=5@Qz056tc*nG&FoH=d<6+j0nBW9-9Fb-Zc#X*L_dniHNxCgJ?y2mJW$LS^TyjZt@gJPlL=>nY_wHKWEUfm0Jlg@iG?*Tr3dPuTo0Yh*Oya_Ay9b7yO|WJE}ej-(2A{544=e{Uzyo4HH9(?&q_2)Y7-TngW(Pg7pmu7mYx#GJXertKMG%S42DT5CM3Hh$4}ONEIbbgyxBx^Lu8n+r%ut6-bh_8DC!JvzSVt>0!j6Q796N3tSS+2Plr-!a7$9tXts;84)&DQ$Zfykt9;uNx32^{3_PWI*@xYBtF=#l;<O*PT&jmm#WVh}`iIG^ly~IYWW2tnN}aDSRduG@P#)#Xz#5M~-2WJUl)WuU(TO}hJdG^1*egiq^x-9@i$&!-7oto@tK%LP@1ZNrDtX?2n374^A(j@8sLYS0d%P*872XsJE8OtolA-!*5I5d1VkiRv9$uf%)rx@xDVFgM;AWLW6D1ZLs9#9JVk0+n6N@4MOdUVfspjqN+Crn<DEOjSNR$3if1&9&Yb~cIE<dBCLShr>#W30gafcmO@{kPt(~W3QjULFXu@wm&K2lo0noum6Q`@oJ(QlXRp_Va-<w*=>WN)fAe~zUz+coz^1w6(so~G+EGC73E<lqJx*8%u&Hk^8(B5w}EygxWy9LJ;^w|dYc&1u5y(76x{12z|w)GG^en>EwOzQ5-zkKg|J<&R(f{1X0n<%{&PjBo!q|Mkn?NTMM6*w<3m`j;UuDdo$w1B#Tmz--DcN_)CDzc%K3JB|Ma6V3$8wg0bIm;O(gdjY_X_kp~Ex2>Oh*+{hN?%!Zs&&6`W{FgHC1%MPH%0aT!FPraJ&Osu2Lblpl>UjSD_2zor|9t<)h%2vTIG18P;RDkGI4QJke#1b>&dmRW6RGz;a^s~qNAU+%pG|%s7_9@Cz&(%jwn5vsPd|S9U|)=AU68xI%zdoY-HMyw-S72%N-wkg+v<AJ-#_M;zy1ElFK?6h<+9L_z5n_j|9w9Hk4L+@Bg(#iRB|8!{Mp-II~v;WLrF?;^t;{xT;KlW&wnaV7SV#*e2RR)+eyEDzHA|(mjB6P1wXz>bb>QEw>TP*Ha#CJ6<aop?K`#iS+*Ol+=S~17*^}{)$sw}V94*Emi&fDUQc*}=j<{Bn*a=sp?)%YM;tF|>lrHJsHYzTezGTP<MHN?z(C1+4`Ewjy%t8h^R)-*OOAh(xqyY?f`aLbzcg3hYAyv^W3phNfx5xUSf>8HIl!5`6V7Rj)4VTCGg}<FnCtbgr&z?r_dLLYOMPE*#Pr08H=xX9zV)uGLBherrkea8GNI&!cHQFg2?c~9{br|4XhAE{$%UM(X0k*{fl?Ae)|xd?L4>3vIoT1^BuXHpbkf!0NU98ej^WE|0Q8z-Fs+l^G&9vbi`?+V34XHhHJe@jq!n8nf1}2HE<Hz$2h6`G%w+Fep>*d7!_4J}dgCQN@)JhO<hA@yDT+=Gjd+M{-BHbTK4s2WBr51Xawyf?{(DWcAcH<hbc~g-I?Bu}=cm-$Bv@4UGW))c6gU06hK4rC#C)X#HoYyieS0=L2%(FkXIvSrwOk8+Z^hXh4H@ZRJ7`75k?D(*ky%DII(G79O*cS}l^?)<4@{v#Z^jrS4=!&+PB~b?R7rO5fO|c*+wQup!;iMcGNEU%C7e<CKv3=1YI5rai#bjih>-2^gDMh*&}2VBEwzRA?}a7A%7Rh~i~yz5S*U(j@m!nrJ=_^$0P;#+gJIv*RPh$Je9fYNM}FIId@l(Y+eA4=G$~hW32wP1MOj-fU^2;6_l{eWQT}mp33@hb$rM6HzCiUQ=zTV<8nyzVz5i8~D&*#~aYQs8Shh?FWOXz*s$#Z=T^;TCb&UvuMPbpuIbc`h=iBcFkbjdV*Wk4eqBi4;I$>M}_$h~V$DdGf8jbCW@zw{2S*_@bd2l$qor2rSoH_}UJ032RP=CNi(TQo~cWO=^4Rd;Q0QpX7eDHw*ZHz>GQ;rG)mxx<*S}`Q~$VEtJ921}zKvoHOkf*uphpM5-rDO@*MwwW}nc_mI-8YOXeT6!Y(|l#0=MKDHg)ck>DO1Le8<>6aJsIY|m;xO8<t$zZ9qW^Kzy7%;lwwC<`t?BnAJR|u{F1+a4uamKGO4B5hA2?O=kZ-rJ0-)R*4-s>4V@CCW{9VzIzG1)7>)R%Zfaq$Odr8Yiz^B*l5>sr{^IgpY5p7ayn^Ur=fQ;XSI6p)>9{YR-izhqh&MdbIfDFNYjs23wBB(gMsc6W{VJ>9DvSc!MV1_;yIcglu%&5B$=-6dLj5x?DqeKD+psv<z}O|vGX~&mHMMzA^Rd<e%m)$78FUF;|5+s@vkbnesUX1$Wq(s!|M9+!Un&2lsuvX_lK7<{-tfOQ9v$Yj{nWVXOVZspo^=iD%wRsCxS$O!o>Q84ni1WZz~2s*U;kfD3#K}S&lOE@B7GFSW*n&-@t|~|jC34FgG6J3YvY6=Z{LlJ+yP|fIKJ@6S^~$C9%=`@v0B0O%ecO}RcWKax<w(5l!Ex1_z)==t#sC~l^R*;kCzN+?f8HqUTrg}C^2GQ`V^ojCvM2>32vt-d}bQ0@~48~`I7~&0L>QV+_EvISut47QYp~b7`p=H^<wDfO(LCfi+h@M3N((}ObO;#ExK@wuu>`#1rK}iI50VjRT8ZXS(MFnI|3?$(TSR>I&|Kxd&3r;{e+(ENSejvbXi2{U)|V26(M(=*TT?Oomc6w0m1viRR(5D(S2nuxp!l%^)vv+Xn=4lrg2s5?5m+ebj>V`W7Ojy)0#l-&qwgCfY+Sc*$tvKz&AwO&e$+0fG+Ib^W$5Dv8JL|4+#~kFHge7?4NbW+7$}(XilxtHkRp8B%>eg&!K-)MeXF@3=DgpA4X4p8J+=>;^-f*K;<l+<b4;g5i`VWvryw~dKuI*rDvnyn^p_OIC)fAi>8sH2-#pTurIg*7A4o90x5d-I<l<u4!!x~?uNEEx4UCOTnmuTVZ&0~;&$~7uPNG*ms!#%S}?9Uh7HG~F<cDBcOGfuwwma%KSmxLBwnPnC!hlb(Wcrwz}$K2Jmk_RgIIV=y(y2+xW?3Uxu+D3(&A4{qFq{T$s_8I9){W(yUt))3zOzigfCqxd8{R)Pl+NF^8v@v$NEG0b+Ofy-jQ0mPODvkUnWjMlw7f|6AMf%r3trr0AfVY9axX~eQA18RKC_qWdX2an1@q)Anvr;O^6r;dE+jVe*DIqPcI4i{^KdQ4=oMZ{kF=!l15r98FEC@Y)n|g^;U2r!BBQ)es(r}ee+k%ii2iuIR)$ssv!pHiIVNd=9ko<RyoLa*ENj5NQ1wJ$BY*dh}*KdEN$=1S*bbCS^3dl4D+=akaO;c&Bp481sdv^@qMB10-KlNs|v{xI36XK%sEP^6Xj+S>jc1@pkURgCeELP8E0Ka);NKy677g8k7sXWDW1W->W)yzg3n#weJu-5$!<L%#sT7?l>jH4t#MHe_ABeZO_WQD8}p<<L_fw9n`iqRG+ojNGTPZzf(i>6;7(#>Ba)vsEJ}>9h$Vi2xfRA2<9r*1e5hSes)<MjX%#aTHcsATLQf3dadmXDo?NA7ud`;!2T(8o_EK2CNMT6Qonitd08e4T$cXb$7gK=dvA~-vBowWBlR`7Q!Ih2>o5K3wb<t&*Hd5#0H}t#N8v7Wv7n)2Y?-nD%NEfp+b9G21m^0$avQ<<!DT1tdilz{J4Xa(q#$^XkPP1lO&2K?)$(jeRs8X5Auntq!|Jihyce214a4m+Vi|d*hs5|T0vTLUYm8c~eSk_AZwii-2@~$NOtIJ1lST%B(OFr`QrYi(EBmt9%mUtKes2>Byc>LO-?A8+8%6^^JnEoK#a_I+t#)Cy9a#RZ4eChc!S;Oxo=sqM8*v%RM9YZ-!JPxbt>B|n*2+UFOpJ+A`-+>Xg91Y=JdbhZ>S|f<v-mta!FEyQKDimoqkT$<<Kigvk^rzw+4l1EJGnjh^e)4Wjcv8dV0|S2-+qhurF&O1OBzMM{a1R(73*cl%7AG#eApTT^v7_%oLq$K)ae}Jy>e0d4-#Ec%?4hIo)-YZS3>)<M_;Z3RES~oKO^b&wc$R~vG#@kgm*^ib3XWH9T)oTO`Q0K>IpDu6t^g0m_)`cct#~-wDuH$Ih&Cr{&Jq5!?0jS`#=?Q5H}Gk2pL)<p8W5rK+?kXrY%t~XE+?QUIfSH+ABAeep5rx47iek3YK+p&o-qEqLJSunshI(|*fl_ni}4>~8N|_<0LU9r`SF~>jXoT$LdHmrz#ik3MW3c*_(6oYMPM2ie*8}eJl3#JWcv@t@lo|jEr7?1So?q0Ap69vgz_}Ve~X2l#|~KkW|Zf^L45C<>n~rvq;S^kUSj{fE%RoEq0gCy#+FX@Z3_SXMJe{|Cs&lxIQ-~BBW6^_qy|@2+R7(@IPgr0|92WYJ;9w0_98MzKxPTl@2Iq5(`A4lLy#069s+CC=y<QwN~3g`5?j6y)SxJvSH0}Db$bq-GYCp53`Qft+m*6uXg2K!xl>A8%j?7!1XLN2mv+;@2I1TS{*aUAw!Qq%uEw4`h&+XWLLIb1HD+8BPCFPmjaGq~ch(CdxwAu_DQX)t4K9i|v2P=*>-?dp6Ib60B<H;2i&phnBOkMsAzD%DG6F?Q+MJ$%UjeHpE^lhsNz$Cc^*rPw0Q5$~SW-6t)o-&be6s~nT+bf%g9&hSOp-03IcyZAt#~9~@7(Y-WCC?ya}xlM0EDEmFIOV-7YI0xsjxn3v#G@-yKal5_m)*x&WTu+00k^{$HU@NMHM^LIh5*GkQ4#@7kZ0#xEyhmYH&5mN#>3;*T6AWRbGAqDhC$;8B$_EKo*w_J}-(-?}&H<A-YD~pTeR?GX6{#9G=mME8J?VC&T3fig&Cs^?jk~pZ9S|3cdf@C6C75uZ>TP$@b!Dw{NgA$IP;mSr)_r-4<NaiPI*Q%IluB@#c7hQtANB*?az4(-)YTuQpL<)&jy29R6)bDo#s_tNu%=hf*0VW2}H^kCmfHhChnZ_p3EjKYNDv5~A5UJ@M$MWlI08Ek*hzF_RTyrLRMNzLe8;cAV0z+|ycE@&Nz!_umSA$+j|RXVrnQTMw;P&}kfHDBYw*WZEC;aX<MOVmj%h!z>tUu<qaz%(KOwDVV*gKu1nxU&JP+5w|uLS|RN$UP(-@zN27Jlzg;vO|&_VxV8WK^Art^qJwQJ8mKn^rnT4@I77iYq?R-hts5qop)9z_z38n#T=aQ@>_ns8Ta|fs2FaV0gDvk$L6!;1(M~q+E#*kMq6ruQGu*!e%iP6Fy@15PE8OqeZoR2cX0#l(T(lhpESh%c3+(J0k#&2@UZaY&)Kbp$sC+Aq>j6sNCu>(G%RbjQyb^U&&o1}3lFqnVe_o@pAf4clkZ+PFGBT&C6KO&$mnI?i`q<u%C;+Ru6+Dw=pzfDF;@A6J^uj!Pj^y&jErC_6MR+VMLelXdy46p_^sBe>&}Oh|e+;rhrz&a3HrFAP1|r)E1c-$?FSFt>xu5a?>Rd2EKjKjFe}U}`ppQm$5h@hz=%dcJVy&}U_sYqI&@;6})pvdU34K?X)FRq~BmBS9DMG50;OjPU32VrOz3^U1f!1P|eL$xX<U%Og1)F=!4wbiY0l@H_dT1@4#^rz0N~kZ3hS!=%T{<PXTJz=p$@+XRNQtnLP7yw;`*e%`^D$YROhzQG3|e@`ArH&*Nkf!28IZIy>GgXrwh3x&uTNRnt1Sl#H{_ix)S~zZvqjR6ClMweoz4zM7og=jW{qUd!jlAG1rN!zSt^t2EkFwQESPZ*%gNDHKQ2OQ?^`ktVvElg+9ef6-d;2sh0mY94lUCPHNBH}mjK6>{uIUU!$68j9n!h|+A_3fOS86XN}a~M2}S%dL<yDj;)f0EyX%eN%(GG|>F>SvVKDq^^9=kpE$>Qb#(K+U240aC)H%d+!0Ad=3Mp&x{NbrLtPUIteQ1G&hR9q)_HV}*gM2Penh-wyUc{kHYODwvWIau)=V87QIMl%ba?dWNSd+nv58^oSX!WZVvKxyF{7SzJEbt;(Pr%N9?4&_NL)v9=`!NeO`FZORObQczLnQD8%LRlPybvumMXM=?msH+2Vw(evRLVn7DY{&2&K;I^*b+@{NY6a#Y06eV67SL~wtxa^ZcLZhl8OOCig<o_G;VDq^RaG4)-Ln(B0`?^4n|=qFD7!iM$~#1a-+J1*lh4>^;kO%Fx@8xipR*}l4?qEL0`X#UXYsq{B<xJBf<;ZH?Ghv9^f8Opn`{Ozto)+jRi5D*}^@z{N;oAQK9r(RTU4Y%1Zc>7wH!)n2>eBOCaB>1=_yRv;)UYt`M7*>8&<*!gjO?&pu)nUJPjB(SFpZ{ZqjbffXqfwV-X80Pp3~XgTBK3EU)ltZKuGx<*ntpry8v;iK=f0T9P*2lDQ<rCfs(@=wc*{QB8Wmz_B%6l(ZH%f8UJ7LvrI?FOq}QOu$xc;(HS?~mBMudNwXIW#u7pvP<4+aNH_o*Yozj^b*zH~@<umMMzgKhG5H(|}y5lrVye(@Cx&>09=P1@1|?mIc@AQknJTYsr=+D^DoYf+}=eJlzfIy+q#!GIkDn*o%2NBtaELkC7t4`m>!mXLSm{+65YC31YccxbjmXYS1_05=zcuZ&h>nb}VIOr*l?=Hmlx=k=(^N2idB&m_u|q_j0|Y*5fYS!rI8}XiD^Jf_kl2Qn??JkFw}MPOaX)$@Z5e3xn6S@=D)H>OIrHWo|SE^FbcS&&KAX;(|PqAT+QF_yPpSxY|0QHYEv)9kC76x3&~&$d07YcY>Y0q8JWTN2PjEo0g*{mSg*Ab*MKt0{9nZLoft)<VS4C9|OVwtJyp)^8EKQ$6?6)(n5v^i8>7??$u=t-{OL$CFlZbNZ#kKEr@2k5rnY`iIiO1S5u0i!Goh(E=?f3`&6|WmS1Dxh4Ml($N<fLw%$yvoMoZ?@@Em;)6k`7H^IA-Oud*U24e*|6^t|LHD*J#!xcxQ^H3{rKp)F(p<n?BSucu)hIgrj6>vsR9#Vs0@k+|nbg4OMWm}rj?NBj@12|@<acG46$#QP+F*4}UQW4TpVQh+~l<8whNy5n{d7au^j-Zq#Aai~jnH=AjyttHsd1Ccx2%l3Beq^2Ci{oaOEA96ks!fieZC0q81adR&Dki3=7IIRc1{VJdvY4!NoGKVTN*AN)HaL47*A1tV^vQ;7xb!96yVM1wPkq=^ltzrIiAXKTZhS>C!3N^m09oMwct<v=$KMD<e2~!ozf6gvLoz`Xv9t(c6AWHLo#Qod4qgfq5VdsJ{SmC%mq2*(;6s&=D6_-6?I}5B=Sq^Ze2tbxo_~b=P8?cs#+$<HNvXz`Jg;{!SW&f7{!k<s0GF_uL}Rk-%F?4Fv%d~d6)((EPj^JFVDpeL*EnFb5Rwk>FWWGghb4HXT?v@%W_K`OSpiHSN3+D%aB{A5Px#uW8LUk^pgr+6^2!nyT-P0Qn?&BcGy9B_)aQMi6LlP6a0NB{y4p$wT1zw)4&cfFaO9d|VL(N&ki%Liq_nW&r&(lh=~SwP51xRR%nPmt!`A@wlA%7mywcgxi@4PL`+|m-p7jlVH)hQs!aDx8dG!e7szZJuw0`PcE+H4%VrZa_qhI|wPH+^-hlZq3LIJ}(bW9|r*ECj3{J}X1-WvHL!HOVT<;@C4vF0dY8z0s@DBi0u{}+od8xat{0>i*4CPjtRli$raHrgtU=XB8}791r=hQxM63EcY98h<Rmus>o{(YD8iHO^Q-rsHh3CT0qLrYZxXsO++yrzyq^BE@s~1{3gV7PCMo$J00#6j(Z5MX5df&VeR9RjwbD^pb%$T?Gi&;!AiH``PUUfW04BRxTH3ogcINTEP$7$Q4$N@Q~4d126$^tukwpZ!x{;A>5Jg;P)i?2aH>TXgme<m8NPr+p`5G0j=YEf6pZ)7%NS_foL#&_*y(E3n?g7u;>_(u*CuEohDpLNdtHj?aM4u08Rx^mGlP`SWSThpN|$U0wQ%16H-T_^oh!hcB!Y#WX9E-ZXsD25+){5Oe!j#OJgurRJ3@(nYKlpq=H0J@+Ze*P-bp)<9MX+;Q4k%aP|ZZ4*5*Gf;dPt455#E!hgED?UJ&Gftq?M7vz6_EreBSR4T^{A+Szx8e-mD&*2Qwe8LzNG9}+<{D1!b<=21y<<EeQDHuaiAp_y|1p4mUJmuJt1T8(1@%F&+pG*V;lTZs4rGd<z;F8BZ;=1)Y#oL$H#$hBACj)s;n#ohBH<Cpu@Eltoo)nu#zQZbssr$mJj;Ct7!xeN^;&33DCY8aSD9WNZit{{BsTH>Cl~$nK6c-BiqBR4DbVcFE+e2wsaY*elZWcg&Qu+MXMox|$-YNH?Kk5E1osTY(C0XQ-!-CIqkV~1PMOh7v$uU>$ES=S?4!Eq~Xvy8OxCY$Fwbd+mKJ4bBnr?uR?-+&@bZ#x;V|GZ}ItznB5&6lWEolv0P^t;mR4?`W4jD%zRU&5K)h$A;!TVs|45IyTHqSa%A?0+!+S}mKLI+A5*BaP7vuuS;!^KFpDKwNiiyW@lgSttQLFKx^E*8XH>4zjUe=d}C)G^`|Yo5xem?>Zu^yK?no#CS@J96D~ga;St$iW`%BF@sPw96GLQc;*RR2nPv0Djd<xxj!H#^j>(klO`kR`{B#6+hgH97;)kpz85j8MKI+cp1ha$>c~Aj|%p=uz9#hFUL}|K(I&eVVzv=lw88$r=l7&_Eu%rWYNCoY+){ncLk7L9{_7I{b_6d(sEz?q*t=mMCKws-~>#4o-0mHadBh#c2@u6kcZM4>99w4)e<P>iCD`$>9yiVzxgSN6J|uZm?x}s6L>B;B`cS=Rb_yHc&<qLNnC@_K`<q-4nXS`BoRW}tfM!2!CR~(I^XOVja;Zs`#8-MPcA1*aa7|1ignv{6;~I^oP$a2sc^Rdsy%(ww@1)f>#4>Yt*SuN&32pRLNF56FMp%tOYOp9M^>oPNAp{i9tD)QT6!RJNi9QY5>?Ew>~{an$u->h$Yj$@!HiS@AkXSQ7oyWewGGu`Jhb#Bk7;ez$EUPDhkyTCoCJ0@5i*X+GQ!0YdSVQmPc)?|N!T@jCB1gP$ZdqlBabEvtZvF7C|E(@*`$4jN-d{)%Y*a`{X~~{L->KU4h5oV(Cv8A<qlS&jcelSC!UD^d#Z9QvGzt6sYg#VY--sO1#8ZYL}_@~VYq`;N}9%QhB7SgyO3lTC7UtSm#>7&TD6Sy=aoBl0EPTg;$DaycXqsBJ!N0^k`lWcQ_u$+h~t721J%SBqq8+cHBVL^OG+Gb^Ri351?1yFxHERgG9l!(1=@{9XqC=sBm+RSM_ff3!g*o37!{PR=gIC?^|p7^6kHk$w%m8BRm?Z)q(-S(BJRP-3yWg=M1`iMGNrK|4bvDRLjt}}VxevL#)siFjvs{6=n20v{c5M?Jp(twM2jNJ2g=q~|DGuN6v;V=<C@Q;8%0>onRMgWRsmhA5K|ZJ<is@4yIr`v0q%#%Mn}Yh-cXu_P3lofu6ci9OeE1$z4P@zZ?9=YXT9fMM9}W&cqx)&8UiQOXp}DJR&}85uuG&Hp-x@hQ^q%$9+E3n@F;47@FKA#GsPwwlCKU=-O$b%DfDvDIdBgq5xY2=ojS`&-*&9Tci(=x>cirB*mrSY7m4`F`>^;<bjQZy^ZZEUvIVQJ<BHi9Q^2f)7q~GXUnm?<79~J+j(vm(1KNnG(JPn6Q<e9gFH4oCt0P(ccbUmMOVT!jhciy<Ak3Ggy($^XmC5!9y(<G-_$ih}Pnu2P6DC|zyead+Rz=SFm?2@>7V)^jAhqq$zmQzVMwS8kO3_r?5+&WG91!Ef%$CJFC_ynm9*s=&sDxt5v^U5<yLkF}uSQ`E1Y;nRU;KcjAe<Dt!9`?kP<cgDZ}YN<g;Sn@>p;-^dycrmBBri4@eV|CN~sR8At%01!*OtR2Jp(6UaF9AV8c?PBgv|;b7D>crDm^Wu8XW@q_5;YfCag4`fqlu1OOaCn2`u0iM8$5tL`2)myBi21YOBwG}`DY(q$sgW-ZUeF!)`;5#iP88-hpDhwRv8Vh=RxJG4&|!TI#c035r`uJuG|l`opSvJAFrwp_r<a)oaf+V$1Sk&l63+(cHzs5wt9c+3*D!lTz7*Y;x9@YpfSQqPyt+A{rL1=Z@d?F+a8apb^-ef?DcjId41N@or?2FpBTZ4MZecn&csB%}$nQR~asRq{&Jbg?wWVvxLqVbNA%nQL%ZEP*f##GqV<J8PR4uKSts_}+?Kd>g>uzx;Xa-+<pge-xNvv0G6|!tg&y>L8vtV*5!bWS+?#5>P`4qfrxoyv|C^J%G_Yh?xNuE4-9jQdGmpzjTRMkT#K|+?Kj$18fnxRe)x7go;z?4ET0sTn_|Q{ZRR#i{Ggj&9K`fCQLEqwfzz+O&_Z1E;6YY`Z5t5);Mm;yT{7L{q^^J2X0TseJgHXQr}o~wz*Qv+3yH~$;gVq<7fe{q>`5{7K78+^-^yYd_#F5qb*hd_%`R2xBubV2FPVoy4l%$Bxx3<HVQ6c942d%Wpem%RvF6CbO#pP$I)Z<_L(tPZQ-+rKxCQhlRgM|F1J{{82lhaiHP$J?~Y^%gN`)m&{tKSZ7uoYu}pK41bL*_kSraNXAGr0goyjBZX@fKX9za&#wvmzIk!+9-WTbNHaSR=aFkFbT;7O<+uoNh+Bv34c{4)pVDN`hC&r1b`T$0ukpX`xgt8~9X*lYhx4rzD?(vUS`}7qQOj}yBRsgh>yG0V8`o~1LXb+lM-nWWB{+K;v7_-O#V>XF12BDVTg~eh4E46k!R4jQBRV%1zfmYm6CJ2n6strvvh4$01TZE~*VZ+QB5Mb)^tvTw*6)c5E(=5KUo@p#ZZ)A4=8%g{Wp&TYv!kSX_sXILkz2dlaa=ac$mOeqh!>@t(X`6suOjIGH%Zs~mu(jYhx>jO;1_4zG0Oc+@Yc#F}o?|j>rNC<E$x2fcphOw6(K(*h>J)iQmb6`5dRkuAW84T>;@E(YUMrnVw4*@$ySbbeHIL_=85X-HjJL<AsKHvYR_wJgCRv9^?AwE=SYaB)$6w!Unfk6lrU11=1zeWBmZ{;vDdgRAdnz>UsgR>RQaBZhLKg^XXO=Iv$Gl&&NGld|sVKfZM;Kosz#sn%{0g-XDNQ9{x5zQ}8L_Jpjm)LK%lWt8u3ww0WA0ot9HMF9vvkP0$p0QRPv_^l)E)cG<hPl^#ih}WHcGS*IlVy)BHqp#WT41mPPZA3Di-!d_DymfHOS|$h5o*}A$jk)nW6&?4&yNdWTwgEU5I(Vg<DIjBlu4>Vlc3Lg>1G<NvDaelg<#1FKhl;s^WqLBP3Xitp;v&xYcM4naLfN1RNiZCr{lyNYh4ozA~^pY}h*8*>3k))eH*?5$?5?VH3i}3+NMB67;-GB!uzVQ<2kr4vN2m+U&WZ1#EmfOT*)*xO$R~P41k_LCQ<e;yg!VR&qkZwxid9={dcPeaO0eNm9JsbBPp93&WIyn^wpwe5nY@2lxdZkh=Gs0gDZTxqEjGnu<FsVu}nTE6Ye#3flDWkrO9CP>|awhSeZO0;b}(vD1jEj75EY{Tv?R^>tZQxu39~K7IPy7B=B19Qo$*5{O|&@##}|#LX|+Gj6lmlLBrmSIGXut0K%orr>IFDwwrueBJI7rtT<~&+R=R63Ez8+~T3Y#JgDHKt@^VI|W1^Y};w^NEQwa2PEgAh>+X2)w;)o?+Ro7|N7_efBp4;|MKPL4^5nC86HBj+zb-Et;bOaz>4A=JFw)9fT0R7%5ngu@7d?TIsg{|`A+{^75Zl}-qp=ih=vG!C!vVZ9<th6VikksfYi)uxE+~pi=q*TRY611gh0g0`#A$P-}8vZ@}L0FWdrf;o7VWtQ0k%MH;gzdihGWrcU@*k<3a^2jyeEP>3s`@c&~B6`0n+^5P%SX7Bt4DZ@3SjGoKH|ub$L4egdgW%poJ>NUT2x1F^w%kH82Fpmg8q`7t%=QTUpxv9D=!_+lJC#_&TwQU~4!63kEqjY+R{-`3v<triN_?|q%Eztw$?hQizA1xG#lZcm3&YH&+Z%Wk%dga$z2VNF}Wq!9h~uy4!!_LX3Vfu}St`&+5~>4W!Q+Mio4)k9+c0)ANi!(>*<J91r!3b=>Y*Hf{fb|1>4oEhLT@rU~#!;iAJ<%*dSt7@OOkGGi&fOjKhtmTAugjQ}M<for%)a&@~7X4_pLG^w+?Jre_-d%V}dlzv-S&N)e%m6It=wd=vS>dhlrdUwo1}~S)P_l-L<LxJgS>T<5&FS7}>D!TmKvRHwc~qn<(E}+9WzNFPy9jt#13}w>H_K}a%~n=H<h~Fpq<=I=4nikz>2k{DP;)W!*qU9|>G6%IqZT_V<pCY|r}sNv&bgP&(82(BpJWxW38j`fl_5(f`F6=3YWaria^Z&n&G{p3493j5|LVS|?mradr4M}XWNo9j7$!{kbpSp%4ks?m@DhR)h-KybQy%$K-d4~tc4*@>KTWp2quo8qQLwv8hNMbXs$Atme}4Jnmp{LRKVBZNuP@86^pEpjzx)lSk4{7UnvCS>T0QZmtyJ51w4i*`pZm?Pjmh86=}(w_-`3VM*JcSw4LUuuu=VfuRv5u9ULW$t-u9VdB`!52;k~oGy6}H(A8aB)T%A2{Z+LY=ks$RyW#VHDLTYYH8G%KQ_V$(WAFyphq7eLe|0?H9Yo1H~R&lb(-_-1^QhqLmw>+f`uWuiJ`u54}86&p(QLDSX&3!E6-Kw16<?nU)Lhq>j+m7YB>GzNM<!`_L@ypwceYq?sfA?Si<G;`6|MA#dcVOE0k4ie50LJ$A*A5%>eJDvyj(*oW4(!{X{P|CX?MkVq;Zx)T-tNrp^JNR^1dfW6Ck*)bBGFJry%IbckU>2kE2UdDjO{zM_gS_Zu9S!C5g1nM_SNwL-_XqOpO*Y)vrr~KL5e8?n*a=ss>da)kvLw|E-Z;4M5ep7Cu`&J=8vFB$$O9P&Hj2VjMmUsvtDxiBh(Ux!v!VP7k_E4zSUd`98zKMn5fi!c&Uiw)#FbQ@jLQPI8`!E^S&_6Y;okGIoH3QG4II0qff5OzL)^7Cr<p%2z>MT*1K|=e@ZB$e8_~77pnNP89h0lP{2FVZ+6;*ez@7MYyyocpA?uWB}2z}9Tl`qN}^$iIH^8`2#jp#-veSqO8vplF?`hy0D@B$=Fq>vnd#SpCp>R1;ov6=Ux~&ZdC~#%7_w1gK9`=O#slWxQ*mXnKIUVFnX4N0#!Fo)hex}mRrkh7J9LvrToJ%BZkM5VGx?^I@Sy+5p;T}C@2%#7Hv1$kGgiXt=nS%)-)N1NrMKAk$xGi-=c949Kf#xC-4LElZ_5tAp3M$a2!x4aqqUZ+55=j@=4i-B2it)yGOA5q^Nh?gfSdWrmo?qeS=o31`#mtB3%wbEx7XP6MjV%e6-<@X3=g>1^K8m-ZQ44fkg2~+=oxJ3ZxlWdRQnBE+f{?b9H$IK$oBX_6^TM<vY#Nr+JgP}!V+SfP<8f{D$t~}Fz6yG^^qri59M)<U|*U2%2}Etbe$y}|J3Ps3>T_Or64Ius?E1!jFWP;mU%FB6fSG)g*soBBH#SDHHqmT7nh)CvzAODWaJA}UxMCe6J_;cAhh?t$`YI0d^V1V#skZoh+KPq5sw1}1cI3=%5wv>Ts?wdQCPHY57-s?`S!a39O9(OHF)iVsLlAIP8gQ~e#&9p@h4QAMq|5Ty!F9hRx7$fI<N-0IJ=>l_0F6+2~$xXE|XC2x<=87fzmrQCy$RgJvxBIr!+qJz<@SJB3z=bOT{G`8J$)PNj`Ed(;3GEC<c&K0v_aP?)sskDsm}VI=N?)`Udb>1I<iQxCCEh)OnodEBicm;Pone;VDR&GJf2^?33@wkp0CJ;Mgx`@j~cWpS=6^&n?9iI|9?M2igjeesc23;Byf4CRJN4#WqC98a|Iti0zaNhgx^QP-9*#Fhe{wMfbT=!Dz%6<yQ-XWkLy7T3nHOk-T5D_ZOG<$~eHN=M}UYI}auV#PsAdoLDS(E}q_t<>QF&S4mzlt{=Q!Yjs1*wBB(gMsc6W{VJ>9D*Oi8MV1_;yIcglu!WVjn-$A!h5Bb4p`8}G+psv<z}O|vGX~&mHMKoDV-Py~P~|t*Au#hFDBjgvOJ75$H{;9P5)}<iZZM$F59H`$Bv2G<c8&jxc*~mpxHDsX03IFq4%X!L4UOluHt<O*!Yfx3?EsqRJUc-F#;Sz(>cqDL=T{@?P)ap2;E9?yIdj-W!54LWLYD%xdqCJgpddxKz7sh{G&>k&%+LX;8D!$Sx!2aCK9Cfoa@dp0eb~9^Cd5Trbyuh*^Zi$G9t))NFb3+JLXXEP>wL>UrU^?ND7YPvsiX)~m`wP)+=CuTD%GvPCN?ELWn`|NhHgnyw~HNsW^VA*H40rSq>zx(2D<p$ARfFaL&uN`-5$uL{Ri@7)0tgyB7;kpb4H1Emb@v3&LMkq5nR?XILZsA8K@8H+13kR3kQQ~s?phRL${6h?r0bCN4-0tU|a$}lPdBgC_*DsOdaSxa}%~*f#~w^;vz~sm3C$(ssocN7D;IwfPZbF_9L0Jo+T_YZxUjGc6O%=c{q3_4%O;k_(m1-P012=Hy?|kW}Y64G_u!Pc83D<9;+8cr`j|7WjelGGT%4~*qlUbu<J?i$hlI?ot>u|mxq$<jC;eNa{9G!stHTcQTaS|Oar*@3l+;!H+VJpcjk!hsHe=zDrb%t%HF$@%#7y{k)-lPDg>3SWzLR;-r#dPfJ7r;&WCGj+TQMB4ydvT2*yk614WFnpS4oYsELv~bg`h{RRklbnJ3t*VA3D`g%MpHQX502W4|cL4KpVOI*nfLWEn1b@o6=8;w!>`3v=;9A7!>g&6Y7HiMGRr(I>0am0exnKi>CBUZHKGCwQe7+FP?}ER6#ANPw7jEt!1stVVM*`&A-&mv%i)xfpG&qZ1o~vDb&pb+^K^X`b=;$E1?Yn<W%er-EozR*tQ+$0IT0bGHzV?%}w1q_KHggDZK~R-)YaJzy(j#xOJWw_<f6rjo41xRr<H_3sf(5$IBbsfr1=&U#C|sX83qN7lus0LMh8tm=%FRJ8Ds@2M*HH?YaekRd&HEgvnoVFM@Xo}L?kccv-shGi!^hdkmr@}RY50nq1Ifj5)#0<^D0f5}Hy0)DF)26+F^#Dt-P2LQpmiEVtM^26D>Xk~Z|c4=-#&9Ak@k^nD_C`f6V?e1$67K)o<>77_GLnI@R+R`vcD}1*FGDSZj5XLZ5e5hr&`>5O#G-fn<Go_EPw-q#TNag;Ts#L*ean~6G*)i<uwl(R=e2&JmHeCh8jxooMXG)B|ijoSDU90jer2))ysj(R)F=I?nR2~>>f5qU;84XA_aZDRs(|<&Qm58p;KBA9SH46ci0|2C^YdrBmy6ll<`Th|v21J4>ExGlq>T+XES6IlVeRkItrMTptvOAzNr?Ep?Xw7$>E!Z^cf(S2dHxm9r=h6!RE6*^z9Mx@6R%99|$I%!O$sxqRUS7FiR+I@aAc7VUy7g7!K_cbx5hur{iommE#BhZ|Rb|PwfRcr*CbuU}R0K6VH*fWMeN773r4$+;Hm#D;`{IG7tJ_#eE**nw^w!_UyF0U+kXA2E+OfIq3RR7%1jKo5(FV|z{J^#kzw3q9<8NQS{NpV9X#2ub6s22fI(uxW$3t~LV3GM_o(P;ge!Y*O>D&R3GE@rNdY|_J!6i(4Wt0Pcdq^52VUhOfsH(M){VhJufii^}AK_3Y4UjW|m~P`YBb)80Kv0;g$+uv&H%F|XI4aCOiDeAo&2)8*J0Una#yu?l0p3^#el8y~bEU^8Cw#6jU^+qQAJ7j0qTwdE{bs#)NMPYd|41hWxywO=Ey|zVJLh?-$DaLpS3y;vlopMeLY*1+eLFwBrF^vR2oHqy9<<1ZvXSQz*K~Ut`K&7hlhaJs?T6&tduKrY<;zwCN5=9I#dMuN<7Pjac`4Vq*bJSoQ;6N(<P1o&Avv3=Idigj1yz>4Re|2f*?A}-iVKvJ-v>4xAt+xoxzBkM>A_;OZXN(ZaF#y~!26Il3ywNlf%=Jh0+xQf5B0ST;*YQT_MDGXk9D0PEfbLAsCVW2%uPVNgIpuF@)9a()S3-dw``8Mm%`IDN8Am+!+kZ1kGT0^!h3LBb*X|^_-~*S`b$~d!m{9XeyC9xW#K5C@FHAG7>xU&N)aO<p-LX>F_5EbU#@FCG=Gw6(z7WXWC@K>I5cS4gx@fU^`g4h40LL2KQB)`aO-N3uzk*-kQ}HSD^fy)QGO8t1UxP^c|2~UfMzS&*h;0Ds*}@~1>2R&?)E{I54p^E$VQ3S!2C*A3?J|6XgTQ)c@r=yfKB)rkbWJ5uoonX+(pK0u>5K#h3d$5aseCuG(rymNg7Jmp*DhfXz8nN8fO3$%@qWmT1pG~7O9updS_nb>$}o(@@mZUQQ-zmhr}1K44k`z#gk70xVL9^AHA}x$~j?GH@-O-p-r9grTtWBiF3G>zhOuVt54-%sCwKPu)qxF?w_j(Al6f?QnwE=W@wnF@G8ccwx$R}*5YB;B=U7rGPkIEQqmxruGA;UU!<E5KC4rXddKT>6!&DI=hQ+Ga66$jXR_vE4nc*N^Jn;2kp#9FsKG+zDA4vb18NG!jvPG(8sMVOKLK3?p&bnGp#eGQ4=FdW)GT5m;8YB^;@}1LYm5vrj)RI=RHh+<6ckJtG?)CpWY<X2cDZv2Dw%*sM4-AvOzabL6DYMG@aMx~i~q?-rNZ?L5)I1LijbGf9HR?+QOU@a7=br8y<AM}Fu-0QZg@?UoY&GO^o*kYEu+`lxfZRn%eVl|q^xUsO`N2pHi>I9$<LE{v8Ea@NVOL@?k)PdU@a3T5uo_u(LvT=%as~TiM`}l!058CK4iIpHmAzjslND(A=_S=mJ_T}{+5bN1FV$D#B-?fPX1O?_yPBDeD86Pxs7{mo7jtxb%x9YrJ;x}=^yqUA<cOP8+==5hPwplKS^(O_8`+>3LOZ;+^q8SQOP9G{fNEje52sX5$s)?twc`PDZnQfuLgA{vcVt9opVK<qtXp@`i*qC7F1H0uplC24d!N8%cu(ozb6h|iBuvofdHKe=E9cYD}!|eJZA44@4h5AEljiJH7+}iLg|<e-cb&5#py$33dx*+Dp)^)w)RU}XwZK{eUII*VnQbRzNmvBnLuw{tHgS}s`t-#0qrGZUd-h&dL3`7_iV4h?soPBsLh#k5eH4#Kn`K2L`t7u2#mi;E6DC`5W(yL{bS#tDf^ioHKig4Ye^y3fmWrBseCl^cc-#Zc+<KT$na#03(9*Jd}c(F$rgS6Cs0|_vr=024(XnDe}=U32d2hV^e8xQ?bF2bL%Wu76@z0p<(BS5*987OWD&y*^D_st?_B#LnEAn#$R3^wm=MK~TNX{b9ea6MDna@S153qbawXFtio38r8_PqiRO2KI1?P)AVg>6nBoHzQkP$0`kVO3%P+TLd9_4jy8ZJGg{w(I^wUZoQVS)NXo?_pYuwWDtP{4o{d|jV$C9q=)2)XY?K4g<=#x8pYJ5&I$Zyspw?ofz&Z$p*W+|zKJnW>6or=ppE*Lp1Ib;;<2^e915vr!kJZW5Pb7u*w`Gu#;Yt$Lp=Z+Dnpmm_<{_Et8tn=YI{hEGhX3{((VnO`opqMl&-e%abXe_Be!Xw_0sgj}eQZ|N{>Le5J`UI*F0oRYIvRZH$`ON&SmP2gMWJ)Cck<&fDlrpG8Y1@$W=^2(hL)vf;{FO%a@9|$_D_}=S(IREzBHD>)WIA4Mv%n*o4=r3U*uYnDYQ{(m1^NF|Q_j19yH3K?G0D28fODl%TBD$JJ916;$i5=><@>uE^P8l#&+Dn(CAofx*caBOKv}jjx(QKMW0gdh;kf98ns7|)8a3>Gcnpg&J>%*&#g(=Uj{SGS%7St9QF*1{wnG>86Q(NdFxeWIzRul!^EHj5kF<tx$A1!`%V~4nu*K+~PCdc>>em*>_lxq6$=4$|CE24hnK{<C7`&PnULk42;wXxdJ;@K;+?&q%{2c%S<x+gTpG=g-D6zk+6Zl~iCeOXoS^{sC%c~!DQZizR7FT8RC;jg!tr4iH!UFd#il>({H*5fML+BWOyalOgK=_Fi7r?=PF4*{@)>|J!hFC3Ruu2jGPYuuCGfoNrG08~+B4~Nv`c(k}wKX@@CM*l8we=>atYybc_S>e;a6%TeF&KBm{Y6B2t-^(54?1D8(Ix3%&X8da|WM{hZQK%}r@mQV=XXKHcICX>4b!jn{y^4z<pf#XzT$`0c5bVZcVSoh;5ojuaTc_a4Llgn4+yak&7jt7U?2zI3$9WQI3Ihh8h-}+6DgaBpFwY3X*w6S(m<y%S45PR=(r&8BbusHLkYTJ|>c?R8S&I+My?{}OGKX$0ff1^Xk|5W_z0KCygpl?k`Sv)7wc6T_@<KDn<=sxacI~qVEHjdGzXvMM2W=i;8|R9{g_g!6k>)O|zKFmN;-S`>mrtHiJ<&hWtmTYuv0P{D->g+iP9=aF7<i>x;{tRXlybSl9>-qP^kQUl`U%z(fb|r2%5sHWpYv2=f3o5MTK*@UDI$&<sS$=xw~k|o0LTYSELnw3MQ#`@ip`zpV(I~$dPR%rew5fP`Jl!HI+9(e$gM`n&Ttu@z7~|<$axFQuPVrqw2pWlK$J{FicF(h6o5oFp5iCU!m(OKq+bN6ho)W}4JX{^Er{k6&?AR2^8`oeZYKjK+9~P)&6pHq+>VB3z%j|=JA-2l5_p)gzf0|tC+UYV&a0!1-b?qkG0Epr4H4XBo!++Jlk1g}V(#fML$i*I_DP+gDFCx$#s{@-?!2B>(|l|&AmXtAt1d=y(Qm>$f5PG1zGel-jBB<z*%Ls5RCVEGu+mhM!r+X8OumykSW5~YjO@6h6?CRA$DF3S3tfq1XXqG{ek0h-&RkNbTDNOa5+qJ`Wlw?uoUAPW<s5N%;E)~F_M6Be1bkCw=|=2kSd!#zKMa;~Q|4}LR8+vAqK(1@#VOmp)Q+eq^^rPMTF{^x`Y}RQPS5_`=T<UEK_GfXrDbC-RGik|3_a)VeGW?jhUg$JC9!s}SqgjJ^}T4~3`e6bVh$%YX_ayxC|H>Ak@z1auIBbn9##7=ye$)@fc^NXwTifjK$adA7?5kZ$(8W!^hgV2Rm1pX!%X~HU<U`oXOq*#eDKmSP7AOIi$}X5M3SjHDkh5qNYs|PmmZQ}2tX{QuZ0EXRZt{8s!vUm8B=18m$~1w!`;^s_=PtO)3Q`i>57nai=9v^3g)LitOLrUyrTIUhlvzc0QLG97MzqMa^~zM5<G}?AyREk3^Z+xvwBq_zQ2?e-DK^Pfw^g!9TXqr8K(eUE$j>3l5$ED;y)|rH}p2eK8$OpAq|pJ0_O@(;E}P_&$?IlI61xR>kzbEXR{hq9Z~ajDIygNqe-<eL$#PoCfvJoSr;Cc24JzyExKx6EU2aWRz*v&N`SSDY7c9w28I)XV+YAtu@Y2{{X!4*q<DN)tyYZO$;h=4!yH>1h(5%wxLrjHt0ttHgKnT#g<gcGWD$OQ^5U_)%rtmwhMj#rZ!exD5?i@zOSz$+3~b(zA}7ocBIH5l3_rDIBb_1)JOwO9@NR_ECfq|o7BJz5CPyj;a)t<rr9lPd4_nE5Bou|}8PhOC`hn<GIYO-^wo;s1TYP|8HIL|btH{{w3$i@NhQ)SO4?Wj17~>l?kY>I`S|^O8Eu}otXKE^aFnEbf0>QOb>kv0Z{=nYSUsi~aNv#=h##&4<#uv<Dl2&*{=ysmsqu7QSp22camYdS$<7METvLg%n9WOJa-T6k11_I)xA^<x8E54Z|{8%h^m?l+p56_0t5!r!FedI!knv^dJ=<BRjU$v!NZK|`-wGi6n=}V{~8<tx;WS_g5t_$<TVxZKuphB%X<$0BW+YMFQh9(f>kC3FcT!XTX)<<En?F=OS9AivEHXM?l$g4>}E}Un|(TdB3eY_MnD-!(`!5$FrAB64=R6G+oWrmQZ$cSIh<vFTX6?p#essQyAgvscM6HJ(QB$Wr<xxeJ5^N5(z)j?f9cJ@N0U{flU{-h>5NmtYC{ZLS2p(3f5vjJ_f7~@o%h<1`2o>U5`3>&}_m<oWOXQ|f;!`?*0%k!>Iz^E+6=O~R;mD%9yg0nSK&d#+V_i0GiNzF-kAD*t&%ICc*+iNvx!c7VL1r|sutx@d!WenwIwdkuA0hnPk=s`&j!7gqH_%_M=E?j)Y09a*%>=ricTCLC6mdS0;t%LSjOI=s8gkT?bijOHJ(lhn}z0Qb_f^V|x1pSP%n=L7#Z13lH*|yh#w<leYVR59+guzv;whfAOJqs?W^k-BiPWeOd#w}c}1#Q)3(ONqaB}Jr)=!XF1#Ki?1+dLSN08=<R(jD*$;zS@F!8$uQRVgCUc_S4GN~|l{_41AFy%a+$gLl7-Mjoq@=bF0YB6!i@pz15Iz?Kd)1z*Z>4lVd#H?=XzL4}(7tcuciDT#s)P9oX#W7tC6TZM~d7~qYnw#oYP-Bgf151Hh~<BeWZ^kD6!U@>tK1o>QzL}0#4qf!<wgj_7nO;bv$R%@zAn>2L?yquf%zP-YZBYM)M{KFT)EGUL71>A3=$rFmx`h6v`-B9l};HQcafK~=%*n;CE)pnj{SP=k&CRp$Wy%Y92o=4E3MoEODFqql{YY(TcgLM-oQ2a|yEpiTDX6=wVK!qB=R8U$IeL2|n#uf2kpn$IbyW*faoHAF2mdB82L*sfjzbHV2LAvSHf`dWW^bn_fX^}*+bCXH5dT!-cxg2=$ptWb?vhOJ~vpNn@*EM^<i_B)KIf>8M<E}EPtmssEAwjJ<X_M$2m&~93?YZ>L?91zV20p~gO6;=*ROb3hMwOGQE*fMgJ}KCeQ2L-<0`F<n4Puhj7nX>41i1GnJO&KMd*uen!DNw>0J0@VL?$v*5(%!V!NlPAL!m@f`yC6svX`U`6YlapslokuXTyR@S{AnVvCGO41fW7CgWeA`S|ey;@(G6K6|&>xV@l<#On#3eaa_84dN6fXv*0XjKRyFM-!gK6&fmcGAj8CtjxL_Urh2g`F|OrM5Ba@7u*F6T+tfozI`B*;C2vxaQ}ht1ug?VlA*HmbjgXi0<d%N@T1dy@9$-?dOxSQ*m87(BeAOY|hBrlV$`mV}HuMUgswe?-s)EV}!5#?sAH+Xr-SKMW;}9$Sy9)Y(DVn5%M2+<f+t2`uFciNhKxB#G+dUK=L%}kLysM;jnO4a!bu??49(@fQ6G&#i)B3hl&1qyy(dTmZZy9)YNDUHGVu%fzu;ln*LitTqGbzJ{=+U`DrDw2Hs_Io3NwzAzhgy9y8`M@S?ixB)){DkP*Hoc9QYoXpI;(8!2t`1CsJo6*ly$XO4@s`h7x~*mzf?F%)#qhNJHtZLt_it7*CQ`L^|;;@xnWinH}X##1gVl9KKEZyk$@p@ISHpinoA&#0=QNR_^FAH`O@=h{%qkxX{T*cr!q6mp;jvsM8WSzfVnPARK<T&yP`d`x=+;`67%3&zj;k#?x%#Jz_^KSe^r2fl`!3#!i(AAH!3ua)u4KfeqLYRX9ok0Uw0p)@6<Ho@YHg~oi-UdM!g{_3$YF12mRq6lNG@$q=_Iza)y{p?qLk&O47B>8|#N8?PZLDTH{s#JzZaRZci2WO3YGCm)C-onfbn$b85LqUZzcDDS539kTW&v<|mZi)qzMF&f5Gstl%f9kUkL=O@_+OQX>;CaJuu;wOl!;(*3kQ%P<s<m13OW8cXJOJly^l?;`VUYr))CgJ)vQgIyXT)LP1-X8`QiQrSnrOlrEt6$3-7qO*udKNM&}P&-1qW}g)79{8LDqQOjvX;p7Tj>hR>0?-X7R{@3CFhjn&&klf_@t@c(Jd9$VY0q48K!p%FPTA?|tr{=!RAJBKw<dMJK$K<_o20~3RnRXtK*%1!*LYzN&$j34qC<ffl7PDFi8Zv)i-h@7@!oVq<$fV<U1COZ3vf#7ceDL}+ZI#&VOuU^H}T6zuB571nT#w7^T`kL!%fT%U3V;_VwAay%lqoLsp<u@fwaFiv`hsB=)wB#@95~PA0!l)n>(b}j=OjT6pm`Y*LgM?6+DYiq_H~XmEBx+72^0xWh2`pRh181G|Bc6zkToDzx+wgk?S8w6bZLiRNDvEAco$x^Nb=PUZX=_Txl19ux78UV@*dLqt>e};l$u2+nxO*Fjjd|u2U{zY^(^Y98=9$?*%_0TyX<Y32M|Pr2s};2CLGo$u}R)RAeWS3WhSS&!dhLND55n3jXcrSahYJ#4~7U;Z3=rm6>&ng<lbNt9tSf6wcYCf-O{tE7d;1q5!{Arx!JjZ2-CE{G{y0cXmclldfLZt9}rAYnP|$!n6vO{Fq5QX)rnunAeLkAjz&kt`PMk5^3btQ9Bp%mBq{SVIm6yLU|Z6mRIJpDcL+jr=SPSr-*B8LGO)Nuh%PfQoRMAvUk9j62Ip!Le%keOW%&h3(nD?VW3+oA5pAWJYw(C6k71N=Pd6U_S$OfQl~&CY1aV9MyEY(yWUpMt_FgTaPVXgT|=xw`Q9s9Qr}v8$Hb0l^Em^kVi7(0#1F}8oR_)V2@|CzGV+tltaL_8F#%*-F@q|a)tLUe$4S#2Yu!=*2wdp;9%WT6V-NN2A^Nt8W#v$lSZ*vH{)5!!aT^R3K37Rz0t@8&2%-U{%q~H-X#;;MJyyJgZxy=+tC{7N*cvPTU0n0_tGjDF&Ro7`zknS#;3>h=*~Y3*2>016*%oZbsB}90kM~E^3V-|Yc7dcJGbI4j8>g^4e1d-Nbp(*}a`hC9uw$yhpVcP$Td9}ppd?VjUy2WEk%*EP2A*(l6xGub-C|g-P(Qkdyz(3S^X(b(f1^H^+^JjOTVAEwYY+AI4|#p0P&rg$k(M~rK{%$10_bUarOqyTF(lZ<DS2IFoim*<le4)mq1V=EC)kb`1;!LhP~XyYcI}oj03=bDN?TgW(4k>Cx{?kI80YrpF_R<u2td=9W}G>oqlV&Y`(H)c1S(Ul0E;dj%dJ2?H?6HYB0o(~2nFFUb3v!TMwu@-U@Zykb10*fjomeKT4X9qieMltjHx4YVrE%uLMo_2ahOzji|li$vLhdhXq%INE-fqO$Ig%eYGYVCq?mUz=_zPnAg(P_gx=v)cHMH2Z-`A#Wyw@Q#<o)D@T%8LzhC5VH5>CX@z%6_&!i0V)S5k((Q1*>Juw7Q6%0j0X8~VH&XTwl&?z&tzXbDOJMwx&q2eK)gK@8vGxK24^9mF`SRsv<;LNH?J2K;(SHE1K{yTSSGazJ$4o1#2hZV~HJvduT2;}Es;$!`%irgGbhylUA36+}5kM!-xK#c(Aw6c`o)gV&gYTcK^O5IzB@+3Wd>6UMNGbip%2a!{KkQR>*Xf32}w8l{A+_`g1h1^K?nA`UQYLUWC;Hn$fIEs~u_?slZ4K;<Sz8^8^w3WarMqUj2GDml^<P(hom<4fRtvD}KgUJeh|4848#5IpW64G2ir2vaR|HE>qVFU=*qRV>yyJBkT35zmW{fq!ps&N(eAi#RXBNqz=hCdTtCsQzzC6aO6V5R*jbYJhDtzzQ^St4ns==rQ&W~AgqWr*#mMYQda9Jqb<I5L7#f9pT>?l=xADl|j5yeV<CE0OIO+{vA(c;eYwn*ieEymX3q<UVwOjY<l4Qr1P3t^nM~yx(*uDGufihaVKQa#ldShX~#yLt{yIE6PswW!z2%jK&b@05K7ud4(RdgCNorrq_t2dwpH<-|i>sr%#^-gatf$pVoD%H>AIhI~*13U$ST1X0fM=G1*V?B_sXkG&esLJnD_k`X>xw#8y=CJ?s)Wg8o!&)!X8uLWVvA62>W1eH-Vf!`8GpdWI>?grY%?hphDoNcRE8`2Y3K-~amS|NiC6^^RdO=i6Jcbc>OB@|w6tJ-`(Zfr|mb6K@TA{dDZU1<_a*^D8)dt*}LjZ@7vMPz?Y_wfS#-Z!^w%r#Dj}8j{+=r)G<@WI;@bI$&nY>-M>xa*M(d<?2$jG`ohFZp)%X_R?B0D2$A$<n5bQTRv8M=<p5O?+V59V&oR!ViAj^(E60d>VryebTVIGPKfLiBR<{_rF;Zj2rp>mHzfa;PvV8Nv2&(Yk#GE_BpdTnvi=+ly<iwxKJT)OmCzV27WuCHD16N^Y$>HBk%X5VKgRGw`%=f^Y@$g`D$C))$4y;ab=kJ4m%sT|_c`pN_rn$(C^D>y6K_w4vg}kMG&wHVF3OtP^@jzkksE`?SNXQgZ(j*^7<fwavJd_L6#6>$#A%Cexl|9Cbaeb-^$(L-DeuU)$#{Luun(`VFIAPg+fW`A&LGPWf4KiK{HT^2&-3Sy^X<0}4r^7Pv(mx(k4Zq|>6>3cKc^2bSzRo)=eZD~I`TdDI6Tby%LqX#zR9Yy8t=@|Vic7MvxNJ&EBwXFs;dnOR($KosqzLCLoEo1bFOl2RqYf;vW%wy*RmX%DB0jB|3b1I8wsMDViZweN~WsLH*c5M78>nt!578iq4baX3r)XSYdJk}WhqkRdf`ICn+s6~Ep|}K<2mq8Hv(Wa&jzp%Y@Gu5NNGK6LZxL+VTcVZT(XB+x*?V)aaEJOuG;*O#zy=BEU){b0)C>Bqj%tYCkQmsK;t?9A0CJE7F0COVV(B}r;FprpYwe(jx-^v&4nO1u(_Z#X<5zNteHmY{ypJ&{Pxc;fBf?2m+;5SQ}y*_C4F)J>zBXbB+KcGU+ZM+Uxpl{lx)+ED$>aVvnjhW?djh9+L-U{H2xb*ICHg-i~Hggwf|G*UI4n|eIT#kZQtl#a}uq;`!^WZGbtVLiJSFO=Dh%rLPTj-milG$9cw{I*z!MWuGh`e_kWDE0+gigQaverU|KyVRl3b@7^vBK8$aPh>b;NLDlpDb{DBpBlON3J6~bI%q_+*)zJ2=VZy)T7Laj@5x0kt()w^496TJJqzEA08mVeu^B|i1b-+uq&m$ym$a#`^G@4x=Xf1l6)<I%Y82(|AYl^low&-V7$40m<=!}p;ir8xRs?|`sxfAZ%)708Q-Y;8V8KH%-7-#%ZqkPu$r<dKpeUnJVds6&EB1Jb7FW2IuthOvF8_CCvY!<FlBJpsdN-M%_L;2W&@{nL`)Q2qPiCrFV*U=x7BG00Fx7m4FVJwZosE7Os6_hfB6-uw|*DS7W9Y%8qS!e|R(k@O|UKSGUQI9yOkeesv(>RZjFz=0G!iyzcVRwiBb@67?z<ehMiWSr)GVVc?E$kl_de?4Q~!FwKH)n#8y5ZDtZ-hf7v`PRF#1~CT{o7!!B$b^y?s)(~0FFBu3KtR%OcG`q8vQHxya<ZDqk|za<3bj<JT1HV(6Y{|f8cNg#ePt0+I_YYABvl4K$MEGk0Q5~k(Sw36&P;XBB6ojsf}bpW&1RQB>41DK*{Cs}OV3f`0rT$(Gub;=D1CauFmpMh-gr0N)5)V{>R$e*6eKo>M?A#dwgiV8pE74G5*73xIh5*c|GlQ^yForr5;0>XEJGwZT)iykH~d}8np^Dq<fV_QY3%dlx*!vrc0Zfb>nR>|XS0J4x;T2ymC;(u)kok|XLB@Uq=W6C6&b;%FLp*|8F@q5$(J?V06A8E0Q)^K#S6U|V~jkwyb-hIU<Fep8N&na^|*HEo3;)=+8WD*p23z7N8tlOwO^~#ts5-nIAtJ0w#N^uNEAYo{RH*Z7TUiTmJk;ZN+~b`luBoz`d!6yZPxd2uZ#i6D|rou`CC&+TsT@bi~b$;Z(57iZXo+M%Z?FE%GFweTW(2P*47J{OfuEI<JP33e_ULGp3Pb^g^-aiP<;t{pAD;qtw3n+f0d;&8Pvy7L^K{)wtNv}bu@Pbvn=q6y4>;W8W9AG!lKW5z^=&8x8Dt54kt~n!D}BxZN?XM!nh3ZQx5BnKcV6@8rv1)tq%^fTG17=0MQD{yNcn<oH_}UPaZClP$R}h(TQp9cWO=^4Rd;Q0QpX7eDHw*ZHz>G^N$JxmndU&S}`Q~$VE+O921}zKvoHOkf*uphf1l)rDO@_M%h`#nc~8#-8YOXeT6!Y(|qOL<KDpQRrtbFkTPZbxPjRx-;-hfiz&ddU(Vu%(6K&w_v@cqLMe6xre6>A6QTyT@RPykAm~jhyIP8Eh@v%o9^Xf{Q!*TC-CYtN)hR)0hIneK?Q@HQ(TFeVuoec(^bxGIxT5ePIoD|KFD~zuhk#MfD=0R09!$uFb({v7F8t!@y;weuc*8TDBk=FFRyX8L>m65O6!(eTud@2B!g!!vWXVyw%SF%&Tbizz>@8<2)IZ~*;zg&s4U3Zvj9v0PV*tKZQ`@6627R*+6?}880W%|l;$6)}^)+;QGrr6wQPI%k1_MI<K$kv70!4{t*YVGYx2)-pJCpd81MQVZC}k^6yit-*MhL!A1U^Y=cx7**tv~ae=g#&0c69uz_`q11(8vjuib_?~hBAj;6nya+LYD%xdqCJgpddxKz7sh{G&>k&%+LX;8D!$Sx!2aCK9Cfoa@dp0eb~9^Cd5Trbysrm-tt#*9t))NFa~O&LXXEP>wL>UrU^?ND7YPvo1_R+q~%8Z;#7}YVM}ZVd`iGv4W8~mb@-uoN=3ZVRN$#=2)YzUArYjFYw=foJZDovjv)xTJ%4+PiR;bg-iOv(+Pg=RSZB$bVqhGy6&JB&EnzcF=9SQ&m(E}3>h-JtE=}i*&VC!ZT)cNjn~p!~-3guI64sd%jVB=w8i`@*JolNKuk8xFmaE?u7v8CKFEb4tm`kz1Nw@v|YYTN7$)xqHUy(tR(5bVNIbFBIu_|$*R{z3xqmXY(R;;_}SBxz4Y?vikPu)(kI~17aSgj{I)t;v>Q|skAp~g|b<|O)mT~C5Xij_j_?6lOlJj5;pd&6LE`lWBGNlL*``8;*30l2vf)y7gccs2NU=7{d7r_8S^CyE!U+`E#hjOPQ9WbQ@g168nPj*f*^;Bz~GL?dAChBWo=Z8m0vDqDbH_+!1_Lf%TPp-eHG=bmvYw|KNreHA-Tuxr754{0c{Vi@ukqc?FOD+a=hUiM`9DwSSAIg7GZM!&ZfXYugi?n<!N1=xesB$@es6H^4gqMjYW@R88YqHY>-L(#Lj0B&9@7N2m9IQ$V&{u~+GR@-<-<b|Ge6--LZ5>%3HuU*J*Omx3nEw(YSu{r5F1Dn^_kRKXIcCgt?ehsu{FCMKi*^;7B%j^gR2{a%uxn$3UWlLjd+4bf32%|U*%(_~%Y{dvBZbcW%GS2~>C)A8mF=|I>Ye-NH6Z_8E$JEJELC6dy1*}JT#<EOgBk;V;B|Ed}aj00t!0E4rDya|J1gj7LU!_}?A@kYV*_LS>ENU9PhbWostW^RZ;rCzb#N0#^HEbegETc4onrmK&^Oaj3-hb^(Bj;T)ords0wJa40u7@AM{=lwnag}KkV8_fLOAgsvjaI)gvEOVG)(h~#7Zh8l(p@GHV0#c(>amPoj#)rxVWh6na=#pP2`3VmBo+RN%K??C*}ESKp)CjoYG`cA%?asS{tx!7PjU?^s>r_BHZumYV;gMS2=+8oN5y(=E)WQa?*HvkJ_t)(!?A>31*9&k){qid-llakXO#4uV}henqF4?po}SKVf-6oIG)5!(VL0l(;sGMr$394oEYPmhNwiXpJ+TFlnkHo|@Ob-(7Xy&OWUP2kv5n8CEpEU<5U2*%bEdfDp0YcjGp8|fDijL4wjpeqSqY9p!73HXcAq#Yo@@f|$}<cvM|E42<*o)w5$GFY$`6vO$FJm-3uZ+bE3;z5u=x(@#Bu<tJU#{-Us>;`<z_=WB!!}btT4bfnu|an5{()RowrrZ-Z6tmQ+|>UQdb>^`{IGVx7%1qE*+1^m9?Dty0sj2n(S^~?qX?bfmL4TcRqi36Pf^f$q#G;@!MWlY5w-*%RkPNJhv}AMX_H=6WU`#oF9rO0teC`^F-k6@yWRiz32{ruw>Jg$_mub(c8hSV%C4<_lN8^5|VD8?Te3c+#u8)k*rVA>oMR8GYCk~Pch(YtE5>&<n?>dPGHqHM+>4jD%|Ofg$!YRbv5NXq1rD7r!4*f-dG2IE+11L^7|(z{JAh-Izi|k&<}yADvL~Tb2dCAF#Mx`q!a()<)Fb9<xlRN^E}yO&;IOis6kOJmV=g~ragToEwG)R-cmkx(0EC7@E)|thq96W5uSE?8u_d%nAyGp&!d%iaPGY`PXF>{t1%>F_$Weloj>DdKbn~-ml4?vov+gz4*r-PB#Dun&D8rkS-gUp%-*U{t;!Jz5L^`&DAyJk*m#5xe$iw~=S`#si;XFL-odkc3)+Yajv9x73W|CHmVUes^|ei!$f1LeQ;!)JLyQjSL{n?f_nDi(F95klZ004@-6-W7>TcN_ajS}_X@<iQMPa=f#sA#=FyTEoro{zp0PcnUQq~T!9FCnIYLrn~I0`4c2-gzE=zgeD#0X!gg2%cH<fz)0>sq-G)3ur;!44H27pmZT$q5b&tKJn)Yj6k*wmc_l7#eK*6z-uJXE|D=M8ButM*<0WTx#-o+$b&077Vh5U^CGyr!&g{colsXqm}$nBaMe_RN!5vKzzmU@ve@RQ;T);+!RUV{NzL)FvchHW5lIQ7a4OI^Q)Z{tRoxB1y!l15k*&!q@i>@hi&UaOJ8;N@Lh+30&Q3kz6v~#DMy~$X7(Y*F6S$zFbKZANfC;K;<E)Ck0+mG)@;x0K7M6amCwSWd3<xkBOT>l$q8B6Plcv92VD6ZhP1E>JEWk!OgUh@Woz#Kxf%>&J;f?@`w(M(k$DPlGU~_I6rmDZZ1<W2fo@9X4uDTeie-CL&Xgm#NV6t<R;P}c9V^jM<dcP;GYP;R5a{)5&nznD5LDMXe}<2hq+pAI`d3tr0?i^C(5x_a<mfTb02h7!3FsmS?GPds0+56LutK!s%_63;PPK+B25Dfw#>f!kI4GI7G7S-=pn$@lx#a&PyGD|>%biV7$pkzq0@Z<H;;NXPKn25MOC>J0_@8`SDqPPX(V%Rt2zj~8@e#2Xm5f}8&w6vy%f-YF18lY8hSx+nJC(5kY$?{?GJ3t8YtcHpj0@0A%DRr?L|a6yMBBxapC|KTO*LSUYO@GAmHaAY9RSZ44-qi3mhCqaxv}4?r+VMzES1+A=yQ5HYjxF&`q*t#Qk7*=s>?Kb7~tNKPB=l7RH8Vh7Zdv{41xeqpDlQ{z2sOU$jnC?g7cE);qQpN7tc_F*Gp9nlnHMTUEcITrlAr#h=sXH<msbwN8rg9ThIAM!G$8&sxIjal(7+vG{aP5wnIIX+v18DN0k}qWE;6~SJ{RoXBZ-%b&s1dE8`^~aGp3~B@8Kgt|2$G5J@4Lf{J&lNF0HE*;`Uxw!S&7I<w_9uHlX1<e2N-Aq;WFY4E`m4mm+gux118+n1aipqYvK9=jREbV~H?P)9g2t>d~BiS>F_W1sH=+9=3;tjlBc+Sybx+g^j+?d)lIn=|La2})aqH+oE#q)#3Mrs<^5V>d1~$IF1>v1)eIh>Y~8Db+1lzX@45w905&Vz!);i&uCqzG+?PV_-2x^yG~RJ~JYvWQ)H3Q?8siYuP)DdfM9Y74|)Ig~0~qh>h7kO*22VB^g&S(-elO5ow9QzlRiIm|=cS&7LTNeP?m1;7Vi<PxVQNAV^kLS+z3u^0Gu*La@tOr?`^o#B=2VUq-i4EC#W{jFT)BOhodC6|B#YK*%IOMyw1U66Iw;DUDEelux+nUiDD&vuK&uHnFGWT6a6&xAiF)KZMD<g7!c&mWAYyn0bIPY%}Y6>O?Mk2N+a9r*9r;?(R@<d2d5a$wpaJ$=YOGl7wd4UFqXOEJ9k|poH0|g5+)j3KiT|ku!`e`5k(nEpIQFHlZUs!?vY1bD1tOKn6=pYz)*3Sy7+JuO@dxQ7tfi;cPLYKP}~9v}h^lKQ0W2|C1RIZdT@}c-Wr6KRbL?u>?8_;eTYDZ;!X1Ib5d4C~*w3>LK!iosYV$|05%B6UpwO4$Qs&hx2d0%`~HH7=^_PjmzRNUTjpQz<h3;=PpH<lH=0S&C8YM*3{+PqJ)byIU+Aq&(IYk;uub*D(rB!i*`vdP9kttvdn0oT#f=*u}22lIhFLM1-XjtmSk|ccF$4S0+&O2mUcv%P9C2%l?&dohxZtZK^`88BD`Y-zk*C6V>D*kFmpmtgxJU>sMfJu#YLhJGQ>?r<0J4DKFs^<MhbB$ujhiAeRhZoe)c=7OlsN`=W77uCZaav1=Ef(rUe29FNsxo7EfB4V?Q?q`JHE<M+lyk!Y|0INZCyu*><YkW0`<0uY2oxIk7`IiO0P!hw|(1zk&T@Dfcwu61tgLjxSZydJIBaab`U|u0OjtdNPO0kLruB9|C~>*t_VWRyd%lTw{RIlQ?c#g?4)Is>Z%-zL4@74+WQ+1TSVd=pX&=Po_J7-MI%RD}4I5%E0c!IlNr)Yydm#{L{@ZrIaj$MZ=uCTzse@O4<F!QeOD{k3_>M0hBIBi#6;OPXzU=fnekMs2nL^_x}n5EI@rgHvrr*1#cXp%2$ojm}UY~`vt=e$%=n?`x?~_?hhbOUDHH`GqF7#5l8nv*BA%pi~ZWvWWTh|jMh;EVpd8ZsaL&2(h_^P4%DIZo-H#RI!Lobg+jM{zz9{RM{r)^US<nzLcn^F9CsX|TK#87?VuULnlARevj!|Poe;WKwBqET73;`dxyzI<V&{Y4Nru0LKFYqHh~@xi42R_!V*h5X`f(~@%D})YWfd1C;{b!pg}6BOqDB_eTB4s|Jwa^$t&94n60wq{_h^})bS{VJU!-UkKHWM}VY@vaFflU~_71t#u0Wx7o{O>YIjf1*vi-=eTa-b419bGdFpOIjk)72}OqmI!kz*8iL{(53X<_d?fYz9X!k9)}C}48x=!GAzp2o@vk;oA66q>|vG^p{<Tgb{OU^Nb79s`aZ+)l<pv{Tc;Y%#^exE&4l{V_?kJA-2#3wU<1ze|0FC&_Fv_NXHv-pkOoA;{-anGalDoldgfB<odtV!G&XEVCAgwiBJf&W8ytV^&%hbzbtSNh3D61o2pal@g===XXV(KjG+YUvo@j{w~{8>j~g4s`6<vSZS&-VJJjFP2R~AtR;mHMt0oMA~zFXV}{J#g|1Y-GAxQoWD&ezXD+FstJ_#8>GmeOvL|N1OyX$)iY^m!l+GA*8X@4DGD|mN!@*MSZret%44ZObV=tisy%e1euDeZn<E0itMd6N=m(uzLm70$cvNA;W?>@J1LGu4-sgzcFxt?!YRx{d4+xr}r0t~S}TsdMLTeI@@yz5)G#2Jo$R>VV1O1CP-J5aDN@f`6#N}$W_pFE23VR&2KM*)oSQ)?A*6M-y!-7m<@y-j9<?>a|18><?|r(sBlW%SM(kXZvvnwghiAnaw);DR7CaTOu_)EyNQn4vnpgnzAvB=GnU+~})Hfq4~#gpX=1(`3dJYjdjF9FD?Ue`yt}C=o^It;K#ORnzh_9oEO>L0!?3j3YS;FPu7H3@bHCJ~s2a68Rj2qY#a=CI*={xLJ9s5YAu9QfRW&$-vaKst#%m@<`(lt0p>yZb><%31yyD@1<nTuB2IZ)`@ygb|WR=%@uXPBV*fvb+7Jma(dT0Zm(tT5<@<)9G2C5UCu^RFM!=4!Z!$Lz{fH~1wWHi0$^><t+8s-DJY%#20lwrQvf@SiuP)%1O^3xV+ZL!v5FIXs6KI4c-KJ`PR3J>7~<HsKx7?up_R_sn%-y*pn(PscIo6(m7lUq8hDq59b-NxE}j#k)Ik1|0hSw5rG&x0!~p)(+KO~SFmMmBXu!J$GPK!4nG!I)hbFlwMqq|Cho!>=1^-$}cI4)SDi>4jLyCFmRXNh6CE`z<Tbq(korgyht5pPR_U~ANGEDMebY*e3z?8_=<{#~4FdDN|vPhq)DRjZ`9x_b>ms71}+f=jzn@E3IA%-QzU%<11jj#fxE(;`D5fEXdd1{7Y*JXGD%j{R~L6@?YfoICzBAzcF9wJfh9l@VViaa~-D)x>ftO$H=P8FmQerLn7hitf}(r=+=Ov(oZ^mA4`uX-o0Hq}`OJqQ)<^d;1g1<S1+62x6i*Mzw{F;M9GD{I{$&vgS_W~kaVG=UiZgT$fb8kBXcJ_?F$XCPo__&G9u-jE(cUfu!1*F4{irc%0Gbxg`ts1%p6NF*LB!Y?2KKZv*+ICUoJ$*c`c9gcQ|H6&_I{{Q^p`9Jl`gK6i9Q$CmrB9+J7xxXxx4NfCEptOvGg+oku1}ar1LL?wDP4o0aQ?SI4I)!jxgLX~jduX$_;kTrq!>~syp`rkad6s&mFc3~;u0%V9!$Vn)FI2%3Vk|gAGx_IS196`QbDbQ#SqflI;(UIEFKE*DniALxw2c%Oqv-U@7>>&7idS=fm_xH}zmed{VugT1lRWOi1xRebQoAl;mr#9vv&>C<MiR7lS?Xev^#S{ub1Y04?VN%4>D@yV{kx5VB&)X6)%~n1+o}e<z~b*`2o))|U@-U`YzIwuIEl?d6)Le6X+&?QmF(UtXnihA#M<m8so_Xn+81Nn0gEpWEhAtBRGfGKw1J@iNYSoNf=xAch=^MOH1Ja5kCpsg`A+p-iXjQXdrC%oj1{AEE!Qa=HwQZCfHClu7-z=9zIC$$li5-zNY5(1d@phpEK?4lU9kIcR2Oc;!Id5iL_<}W<E^OjdB_tr9!~T!p~qq`i;3BQU~%V?83L(X8kKVOAPiV>>Y4IJwem|vf1^o`_tI9{AkN5}b!Cn&FCD%J=2I{vMDKnZO;J#k)o;F#?S>kZ0X)?5X?Lxyw=3Z|N$Z<O{nky-`u7$FK<)%**>|c89GAfK2Rc^qI?@BRvE)P|XY6Ix>aQa-sPjh!l{C?*fo)w}7>*DOaJAnR?$p7v>ifJTUCS4fs3H2WxZKMx0T4ZqcCvFqQNREbTxL*8zO+aR*SV!6=sI_9s~r57qUVsYXXCQ(srj->3Q=t(<&)3T%_)3>7<Uy(MJuPO*$A@7N&Efgs9XN@Z_lM^7^gNTMu?%udsOVI1v2FNN=Aixs=f+jC_X9GQtX+sC*U2ddL>Ne_`(v1ionmckb<N|vLHx+vXcFu36@aS%BZr)YX9s%90XH!Td`mldr2HHff|crKDhG;91DC}E|g%q*1F6QK~gCc9O&Us122M%C7)p1a_kFZN~MrY4vHg}Te?_!kZV?2;1pj!)B>Q@a@U^D-@t7kBfgF%E1trp60WEOuB9~(`Mp4JvK?M|Mm&IhYo@`GcLJH;O9ALcxmRl0=XEy2J*<#N#TCy)I+-NiwDLx2oA?4Yyn}5<fMs$J&j5PWNL5X63Lej)CsneqB%OVMe1lNltS4QqY8-;FJ9^G1$<1f@2PUbJJ_u@gXQ%@m(HifL!Pq^K97~_w?3g%tI4q3FD^D6=Y2kJ``h8ecJKWK2Lc%!M<ZL+nc3RxtMls~MX;@7`+wz^=a{KJe9OQGv_#QNB$x+7?-<uT$DKLg;#km`zXAEN&#uK;|A@bPr>K=ad$!ua<?Ye8+T3Ig|eq56`?kI<h8pNzpz2gseg;7eVu7>C#sSEHm{Z{yRu?ruK=Vb)~212II7IMq3M_$0*ap5L%>8z@I<e#eQl)<IiS9IOEkBAB%Jl)0w5H$(pLb_KVECY~M4~CP+lr0gDi#x@(#-B8Iu7{tPllMH*-DR31_>Bo{SU*5@pF^nnt4mnDG%+JCf4iPda9<%5M8>Ul`>O)Fj23)leoBLEBN=zB_SB2?s}o@JDd9Wy;Q9$W=>et5D6WC(l|K(;d5+hqdT~^(q3ENTyasSaJmxQgYe;8AsMuunTWZMuB+vInHtPtiBE6Axb8x7@AxX&@S3&a_xY*BAKdB_G^q3BtHmE`t-g+g>U9{ZTFO#T9wx6s~y`pl`N8K(&QNM_5M{J5mO=8~ch`}GfQ!CI<DpOB9Q)C(IR5_fDM7_Z5rpGmUlwJ&Hq6ZnS#PKd1GOj@;#JB&&d(&JR*3y4p8?Odi#+Vtqs72_xie}HA<$YnimMT{Yrc;v{_Lg&}I<?ruABxx^@F$t=<Kp83=#*exm@}{`{|yvr>OwTH26~B;#(*4bm?2-_X9ob^_)nO3$414cKzYyfXf8QaMMxZ{Y<YXh=Wq2?c{KbQr8*dh42@Enlzpno{^d3W*(3ORFbo;nc1A^+F^<<t@-INpOb+zYA=YtW38o{(6j-LJW&lXnda}3wZ`%-yKUm4~b*wKV370CLW$LjgS0F#g4<`xsAx*FgNg5*oUR)+yzo|wkvqR-mq!v&bS|+msWMF;Mb#xZiOQ;mWoEwwZ&aZf;v$NM5xZkin8%-5nFGysx<e-lTa%5J5+sdw5D9N@gRiz2H{JrJIe*50PfBBOfFV{bia2alPsCE@BVszj2-hD=qB(L$cFRlWOz^IpBS<g_8`aG={VZtQBD|zUpM7$O^Lvt~7<Aq*kYf8?=1r`l1xPe#&HMx>n0OM?fMJY?fV-NRaS{ac52ID%{=TXP+BZc<QDDjKagx=u1p@w(ghIOYrh|-cqXvbS`&pCut42EiQrNSs!6yR6tn4-R}4K&)EpWHUW*D;mqbzSNQLC|)21}>baU}>*}K6zMCIS-hZfp*Cj+7<XIqD({ri`)-t*TJpr+^jPaSs=KGp?P^tKAVy{bnT>hF3iKVph8D{&+COasY-(n)jJkV>D==dQ7+FhY6rvtq|tc6*co&RbW`OcY8ctwX#;G84*cyo%iD;(#~MG^soP27IzZUbX-_Mbx7D+&0W2h@J=s*(5UWt8w`!R+<V?C_V)L~5oB_VEh@O0gOAlAX%7C@Af}?P`<f$doB>0u-XenTTY%6A0HJa5NCrx!Me@7uGaJxH~sxb8pG%!Wbdz$dJiq+;&d{}NQ9{z*WW(_}TkrYD}G-h^OTtc*-l*uKiC@n6z;z=PQkCzTpoaL6-C@cP5T=!cSb+$7<PhGlZ3xORq;0eK#jbV{TYPJPeG78)?P<;+Uc|YDRki2cCrC_7OBj}I{OL`pv<gZ*k1tZ3pYX4`&$+A79DAz$zrG%9gAJj-i;NbwC4%O1_^4wxbu4e$cgS^rk`*S};{I@I6CF$Q5@@CKp$H8}bf#eyKh3#UZ($2I5whqD>J)dFb3^!1`drpgb5}D0VU>Bz@c9F%<bPCNXUkQ}AK{~+}y{JN_umi7_V!X#=`W`E9$8J*t>=Sjp1XhXb(Hj$?m4p~NucYJyo&el)qz1@O7e`l_Cb~I}L}SVv$ewTK6)7R8Otu0>x-c<5(N2hLT6T35oSNvA?G9t<&$op1$t(F$o(~S8OWp<?Te&&YOEqz?dWnt^QlA46Ys_lF9~s4>S6$k!;)R%&e2da_aSKO0r;a!M=hC`khVl%|ptev>|7$#CNoWk(Oo;o@bPuSrPrFV=$m_*Ev_xL0-@|U8fa8_qnIVHnOpP<q-BOiGDz(JT^e*%2fp|!>Zm`o@OECab)fy!MzyeVMXeuePnl%_h>`m}0z%!()$Jr4oCgWKsH^w<L!yVT4(TXgrsL0EaW(mnSI(scd4Lnm!MyhyLW#2l{EjuC|S}ptc;Bay%qAAn+D*Qdl9IgMPTU7be1a9FLA=$*B%_W%n{&k?P0`quTe(~xysf0T123><sq#3_;e@}`aFWn-T@BYP23n3(}kACCIa<ocZcjjYges0t{riX8ZW4Xin1G19Bc2t|8sa+LIFYz}?Rvv02Q|)D9hHR_9Rh-`#hG>omY02js1wjj@$J+ZqC|Z*h{Qi-?<BjW4gyhY+pICujaQ=s7gv1yluJ4=m`gg^=)>D~f1`ioys8pFN>_LE;i$^Y&jSPP#GVdu^(-K!ZZm`n+6e7TPGheasf^?L0-}KD;3`sV>iUD+?*q&NM<Q`dsyQPl<OenLu{!{Oc;|Q%nn}>_v5}U-5?g7J&xib|{JQrWP15h#NrBmc6H#Y>V-c8l8WD6$hV*t8k-fta`vOCXUP+81b0rl=Ec#jO(CVkc@%a@<qnO${O$u>kyKuiSaa-nbUAh9$z>^0&NUtgDvq5FyY>C>kH-3E^)sTHy;x4YG1`abS(RIGo=o^hMSo+=i3KgA)BG}P1F{N(-FvBaDK9nw!2BD#4GyF}KZKNVYLy!fb4>3{(;;}oh^k#p2xzvCQn!~}do(ICf_*18U)vjJoL|N7_efBp4;|MKN}$1oB6?X6h4#mGF_edbF8SA+f(E(QekOt1ss>DYY>qOmOISJ?hqVG9Q%`3uEZ41hh`{I|Z#9#;>bH&Y=Ripy2WrJ8-zlCL!(Jb{@luiNK($}I{<lmtyt=j<9{`ZtRb*-LB1pfEC~lDBVKZTVR3p~E-4<SSI!i;-J^i$yGwLf2IJ>s<x~^XO#0zMK$GDn@*~c}jU5xDZ}&KHx_WFXP!EZS0(>RpdJkDv8Vdl&n7o!$TO>s?WPDV<mKu%h}L*sy_-}a||p?DPAPuCC863eAW2|u{fJ(Qj^MZc<^yk7gt^WE}9r@zSVsW`{@0!1qX@@tK!7l)1fRol~hfR3$}|=rbhW;!D{5DweeNHE%Vz~f*l5)(!A^=nm9uQj6HGMqFXN2L#DkQe^~v)WLC;M^6k-IUo-5(>+4HZ?e8{}M};%UTf`ske+)m$-j<{eMIIlXMwZ6=6}NNx@T$|rBEFsrQKlnpbPuHi^6Dkz)BAbcu?icT3%PjGPkGAbl-vq$iiH(!_+bevR@yRNnBbQGePM50cvG0jG9&`rta50g>VgCH3rSdPFo*7IQBZ)X9;=$yyyIP4XtY5EUla>z(m(1iH2r3+<@Cfwwluo+Gr-Jie|Hdf*l{Hf$-qC|h@+7?_tFttvH?C)TGE<OESXc=vAj!fm+YaIF^J_!Opj!{sy2V5HxYjT%j>?VfDP<LnR*|%9{EG0(g`%K1Mm@UIQ2kv-yE5Fe{dFI?m!lD3?bN&iuu&$LJ%6*Tu^qm$<{R~t}s3Op0hlD`{$QGe);oD_~Yf#`}(p{0y+Qn%il<%AX?kkQrG&IAulQA%d{zqBm=>0%En52x;MWz=6gGh{{|Dzd_UykzIb)%|CG5GnCy5T$SZi;`ni{lMECCg4aW6cEGNu=Df3<cNFk!^Eld5f`Htlrr16>0HJZNC{Qv9C^}7H0{*RG1fsz|uib;hJObg(o(6;#vtCTu3{}WE6-uuYy65|}jA6R`h`Jo@ZBJj#KX#4i*FW)}cm&aNc<Zdr>A8U2D;wE_adwrkM%Pjx4V@sFom%sh~$1iU)_T{or3Aq3IAOC$m|BuJSx`WKVe^hcH0!Z51Uo+^`?GN9Fl9b};cfDh}zWvFc|5P|FqBgeq6#0O+lYaYr*+N1s|C7f(etePW1fwPg9u2UodOlVvwrm*NcWUpmY&Tr#3fB`btk&(T;{(1Slixor`3?037=D5j3<Nd-7#u_WWQ>nEUZmCQsDWjQrS6`rjmMimf(#|^J%nwA^;#HhK|7Pa<oHLZmkWmr3Z^gq(p-J3xfD1SqUUymy1~krtp2?@=9#<`PIHXYye~{MTO7HV^7XH$ShL3WJV1=gzL<chCr-S9ZYJ}scV!JF4kk8r9{G?7B`?(U_AN{(;1KCIJ8eQ4U#F1^Ia$qQ)sh0sgu2UA?X;*a3He}#?j(Y(zBmXeopj|nk}89rWB7_20KHbW1Hzf9?pfr{SWfVhg|FG{@+Ymhi1`~e=5y&eYCK^6Jz*w$=L%&&PZ(ydNYooIRVN)D?UoVU8zb#HOdjzN0Xx0@2R~)bSR^XwKXNG5+x~k^(--D{o}@#@N?0A4N0##&I=^MvEcSi!(nr-a_IYw$kO@w^pUvs@L<_pJ*+B?h9R29ZXszYyBXFv-IT|w3!FJG!j3d+6D<iXvyt3@%%bIS094kM7{T`TTh2D%YMjl+=h@5h;f~k@c;Q{x0Tx<AETZbQQjb%d5U`tD*@PVEmTJoOA1Y{(e-uC!G6^TM<vY#NJ+CuyH!V+RpLMa7CfKur!RKKfuuFd)$?$$8?c_pvGu)%ApiwlF#X3@VR0#0kuL=q?~(%3{fMl>l`YYA?-rA}E}FJLmsRQHZslTrS0aS3`hYsnNsM!rDxCFp%NtQxigp}qfAmQZ965JwTwcwm_`h-=R;;&C8dV2Y<3_gDP7Mg+m4uxL3Suq*QO?RNvnze$s8@Y)AaoAE`RFfIf9l*78?PpCMJ#&*Sc>x09rR&>RjK(q+*uHpwXr%u8YkcZ18)PJ&3bYimkotl$J!<-%+K)zENAADdy8zT`eH`it05^;-8D~2Q=xi0C9V*(Td$SMI3@-%n-P&E{}lq}8Ls2r;}Q(POh`-V}auTbZ4ny>8h+=17t@P(%!Wy<(*1G7)QC&T;~Q-EW?oW%>FV}0`O*FU#}QtSv!zaD4_MEc3eCxg#H(3?~_wG`VBQEK=+oFqG1G8}5%U2+50@gOxrJT(RLxy!(4#22Mh3xj3)2v%BLQFxJ@YhfX`vH>vac?HqM&Vvc%FFpATCl<?{i>LQu`8eVY&vcGPzt>vbkT<P&T!~TKCvv~a>bDB-fOe53N9isXK`(4!rR`?LGFzek85b2VI^AtpoNQq1lIIx%@U@!Sg3kD%!fvjMU*;KL_W}oG@ilUKGwjUhP_fYD{sL0_Kv_Np0!5K!*R#(Ex2zQ%Hzu(`2huB#NXizPcw;1=j0k+C>3fpm?#iG<n|G$hoM|d_rvQIDQGSgy;orV|`Nw(jS6HCXNEVg6N>%M<xf|XG*#gKHpJMx!xEDkca2p)$M2{Qq3O15^Tm@LoAQj&=?~q3&ASpfN04I}O^lY(<-oE?sj&eZW@>g+cmJ?jR7~;sN+X+1fH_v1&pe@swrY3Qy;37cQk0Kx;+QLN|N2;l<z$G>XK4oC8o{0(ss6!6DY^vgw<^oS$Q_rP33JD=?V2jU#il=GH$T1W_w|QIXyaIVKJt738J$Xxe7jY@pS@NbB8i(xAMKoE<*gV%CCG_W|^Vg|*Eu0Ic`9){D?c5ic5?$r1qfN*9tMg7-%IsEKG0z(tHzg@C59gBwI{#)EpSi2r&Nv!~_)evRnd#`jgo=e!y7lkhT&Uwnrl{xOihP!YR-K*E>DnERVxvrd5DqD%aPpPN@^m+)is5CR`?9p@$vkc>1b8xoF{QEkOjYkz5bZK)-m(h53q@pe6@9#}N5LceN^y3sSif^sh;10dbBDeeya%8Bia3=jr5LGv<~oi6+_r^EX6cK)mJ&E~MEBlP=0uhA$GsjTn>Nn}V!Ql%%m=Dq%S;&yt-$AY0EtGx3<_yN-s>|lFH_k91j8Te{T9+z>h3hL+{C(W=yw*VuVTmvb|;u_CZW(RXt8n{G7Y0wb|F;;a*ZUXA^`1NiN$;|<s1sY1xx291rhydLnTl0a|J-6%`cPCQAXIU5?6L{f&X~lH+l88iJ;(BU}#s(X16p7U?Blw-?fDD$@2-#-{Dmyd6#yhPPrg$t#uQ-g0bO;oN>3}vuQr^_{V0AdtbxVsi0bwnq!yj@kq?b+%1lyt2yo+X;hvT=1PXMl^8dE57-KsCroFiVp$=kmf$WA^q<H3W3}%Q{19kKgDHs#IM0I1-KjeC-AB>IrvS%6rlRVMm6WpZ(e5cI_cyA^!H@www-z6*v|*1XYH^;sba$pH?uKPAJBK%#5#40s6nF(G*dG<FX07drbil6<WBcy^85t||lxcGv)6Lr>(!tq#*1;ZyAhP{q{KsLTBfu#m>Q9;?yZhRNbm9(IddC&~3&{wiE;J0Ttofi(o`oAlKOwY5mHd79p^dhV9GwPaJ}D*(dRalv#>a+jGmk20EN(_)fI9|L-8LFM<<3!wSet<YLd2Ld$F~)OtfEQ+B+RO`Ny+-oNR3Dc81o91zQyug&*Hl?NRT?>$Tb?6&rFvRxfI$Z^x>p(9g+<VGRHOM_aII3m<|2gN4yvS1}28&mYa$pJnfwVFuTHojyRX>^Rv4%cd>C<=%jZ|CfIc9x&-f9HS+O7`_PN$D$g*y?9?e=7DpPWiqY5(DHFsvT^><jR+J4d;A9rSv-MTtp%oQ;X2c&9!Z1d>Pbi91Rz3>=R>&}N`_)9yPa|jZcAMF1WR)CBXYmouD!05Z9_W&~4PxpU9_0OGtw_FZE&mli{W}f=J}cFWpF<KH!F!S)*#6;{z3^T12vz&SQxs)XX&!oPD7nLP71&k&m?r{9k6*uIC^vTiq^y*Jr{3p%K>P@EP#GP7Umuc_NGP3sZm25#XMd{<-EC7KLR(B46lVen-3D+*e%euFps-Yv48ba&j&MM6RG1nP3lPF5>FVHiLO5}ZKUn+&ys-}aTt23z)%Q<MxK?4nbb`=7pdSJRyiMZp%?9t_AKk>1b~!k(75Ni-=Q+>m*fT!wDkuh&yP{E3U@;?{Z|A4CWRKQe;DMeHtC`+xqS_j9M7O7r&$>bkIZbWdH%QL64U5`LF(GQmXXhTx1eA+QY=+L)X^s&FST~u-azo@~@d~;sd#eIPkyGSQ!67bCO+#;PJVFw_XeyoaCenkYo*%B^e$P92#6Ql(`;%<eAw`9P`iXil_B`)HeQg8m;|hrK0j!A(xsiahMr|aK!a(b3K&la2a0#C?%D#rGTQ*1B*5GNHIc+4~S+7R%1UEm-k)V(Uw^U3k{5R0S{6!G%n{K$y4>iW2tPh2QUqo?<$ju%E4kM)_Mi)XMEt{QzikDR9kr0K75(q^lgO*MB4O2UxBf#}E15_IO%*)ddT+&*|YoCKvBx@<he)L+?6vCTIC^^UGhD|eDipCZbC2~u$U%R-M!<ABz_%IsG4@Jv(_(m1iWyZu;3?J|66g<t@F{S_?C$lCRa}0T2&=ztR8FQ-gi=Y&eBiqacfYH+ksvqQZD7y!AZTryD7v40eKd7ZE<T`bI7LqGc(zf-^yolI0j^}*SR7DKq4j2!jkg#(DuXyrFoc8w2?xR|ERRtz2$i_DZ<D02dzO<hTt#T83EH@14Z1ou!3_On;1{TP{-2HQT{9--DqIUZbW1fR~YH#wdoi&BlfM$L_nKbE|ioNbt<}PwiO1DF^jQZsDi!}VfXLahj*s-G=#Y0)BI<-&)3{U98nPj(^Lr`(#{24x0z<@0V>VZ%>3bZ2CfW(2ZBS(*ce=Teg1a>gAhlb;zKNN&MR5dx&T1!l)o66W$Jhs4gje#LXcYq7UoE`~XQ0QUMit_)G-6Bah=1wK3Bmy1}fl3K6eNIeGpu~H?dJl^&{wE)-3fD8pGbr^c0%0z5tSIb7B?DJt)vZ@MoFuuJ*kOR(I^5`*XfLmYN9Y+v+g?UzxN|F7XP0sR@%Y(_hJsw16Um+1$DVBv$<LX2A*dQK$iP|Pj3_mATT+1ji-!vsS<6uxOp3i2Gn{0Rl{J06fntTH)}=JVXN=wUyHv?1<;6_nk^w@VL5!zL5-s&Ua2?0*h-1wC)@yshUUIBIWTq(%Eptf;@pnYtx^KwkgQk=8JZIychFR#~8TzRt%BntpRB8z@C9wgW?+aWmf(>im36$X>7;^?S8L}ZA%1v;^j-#pybW)Afmv&us#7Ggtf_soPkDD<oV=Exco;XVXKY3rb+{kq#{X)DL0wjmL)LIN#5te6TB?qn)`~Gk7jfMb-?#jxa>gLS)^Ofll37kHCeyXyvG9^2SDD(lMCYTFb0nhFbZOF!8*XToArE&Cbb=TWwz2{2Qtf}6Wz)%;Q-UPe!l@q=MD>cxneWXqXeJ|Aa*rh0@Iii)Ga^7Q`-)xf`$zHfB^z&^&3kRJya=drE@;23BwpZnJe|y5v=FGYDf}yk@r?=B)O25Yt7;%%jk6p-E9XK0g{8aHH>vyDwPXt)7`V-RsAK_|D>SLITi&yv>zG;p8G4dGe2j!ItJ~JYhWQ#uk37}H6yAFp<(LQiG@oDkLS8ShIAcs_$pn%E3%kNmrtg9Lv!)?FmLDWp(@59bwm}kHEzP8kY2<D1#A+m?3swPB6q{$1HwT`2_Je64di7};Wi8<QSy-My0-A)xIVvvoKP6U<|eM}41XGt-%E}V*B8GodT(txatwE8GBYSRkoUAWKc@;uj(>njZUfs&`NWi41=2|zd?I<FCBSGKyAcaT+HmwU${5xe{y;!wa|Up>&iyF=0Gy$v<t&PGuttCw*l6Pk}_g%tF1WGq5z;sEp<;3U-7;S^T9J?*)J-VOW?z0Q`m7fc(<Ejz<@J~ne3rTHFd5Ac>@s^G!O0CKT~l7j8~Wor-pYUn0s(p_y5kZ-YYy-Qzz`Q?03Z*&OfI1*cX9zC&3X4&DZz?17@)4Ec|`S!jXI=jU77{zv-K0YE>-~O!J{EvdH_TdM6menRvP`RceIjrp!q^6(yW^SCUK8zIddQG`yH*!(w^9qiZ%*$K!ew+#saYiN+4t5%_ZJXXEJGbncUfWh=uP!b_Kw{QZv)U?bLD95wXl)2yY%k!dXQAwosI0ZGM<)-zOxprh<Y9iv(XLAn=JGcgTo-5~vVO%*#AKg95-~J-J*s7BmN-5H7e2FIM-f^53ZKRO>fZBpDKF;&STt_yOYn17B{_fqTf?c*G`8)R1V}Ul(Bl=cBS(AEV}?w->RV(W&dswYcbT7hg7l4c-0({CgepovG<k&EiL(p`UP4IH_m?^KXyK&gq}~U<8p_YV{sMNCCFnB<T<G>@IlUB9n>7&Hf-}qMaXr4pVMJEow?uy4&tcZZmrn&)fb8W=Su31k6{8HWS5UCCN5DEgiB(}=7F!6M#)HROje_Uh30Se8IX4Ti3-#cr{f_l;E`+v$OzhjDqvV|d7Au}K4!}O8xI{)NWfvSvis1yjry>q&5Z#Ve+pveUh#s#2V~y*kawdRX-wOs9FnIvl5AKw}F^8z~rA+~KYEVZ_$%DbDLDgQQ_unA0+JrA05&Rxt+xSqiM{Hk4)S8QJfL}=)K?Jt2W^%%jcpItVS4-8fP9~%Rn|swuCF8!IQ|MX64ZIA&VGu}$CQgD8s(OxSeW^Q|Ej+_7cM86pWD7hFSgq=_BZe>xXnC0uuW9>C0?SXOI}c+UT5;k~1ibdTT*c0BBI^h70OfbZ*-w;5bXRcK`f$6P*xxMmL7pO778rPf$hdSFhaeo&L+aQ=F)b#_L_fiLf@L+}DeAyvSw33NPdcSTePQG*EuTJW4QlG{{UZ=BRAC#@JMs#gxC~-rUp{YlqByu83{KG+RDwXKuFJ=`;En8<MqJ3-i{dFzRwKtM@SIBM8Z9LFx`D>A8$DyUj)tVhaH5b+b?x}SAkfBuiQ4i|B1YZr@Mr)t#}YC;Y_lkE6y^>xB%(DQLp-pT<g%b5qmloyNzx~SW3>)=ma*S!ZHspj=wfZAj`sL0sapprpCfz_TxF9YwO?MFK}9vgbeb`{T8g$O-J`D`=D@54)4I5O#%w04IA}7c#{$Gw4B*f&pS<DYhC&^e&qRjLH-W_>^|}L;j#OYx1}j6ICQPdcWayn-!dg=JU}VP~MaP*u8#8#GE_9^>*6~`*4j0it?93%Kh;=Ixk>GE$D`%<)%yXV%Q*@b-qjZl!w-ExqDZ6x|mMSdC@3G$m%eZNCY%ND5tWHrZ;ey??pFFBU2o-P&XA=0S#W$#CeT|rv;j(`hy1)j(2Pz@D1%<gXa0|N`m8$jq4xxcm1Ay?;EGdV@pbm5Impa4M7>k&+NwHTYn#XKLI1!}&N6C=6{K-2`uZG8H96uDAsGA04=|$NWnuVKP5WZa<DRL|zi^FCviDewmYL;DXOq!!d{1NuDXmCL|oft(ZKTSu)lxV2ZFKNuyLlRVfNQ?C4r@*|5UWbpWM$=@*)OmBr7M#bzOMxv46>3QhS`?_hmY>qF0w#~%Lenx%@(A86HOYt#x?S?G?9^sXSt6l>3>Kn>He@T)iZ{cjf_VP4zi1jq8<_o-Ji$0AYsgcf8&ghT(@W35dL~`d;Kx+V>{Tb`GyRQLT{qLPdA_OQ%or_r>}-Fq^3^p`Zf}3`Fc0HCD8`LoSu8_=-Tsf^24<Iy@E`)Z@fDbeWUVk30MR-Zb=4iN08D)iGufv(Sy97WC}xD5#kSrl5vSp?D$MO5AE#?|tsYLbK7qP-oYF>c(q=NGJ$(lDMH|4`oidwJ=jd&+z^g0lu=2a;>S;jI=<X!770=L5290i$a3$&Sz1$ZfGx(v1i?mcQ*bop(;I#zQG~elkl+M3NYf=FO4G|DaqzS44`ngO{cI*K#ru2tY_R#xs<V>Sxq8bU?LIBjwc#G<_3U<xX9!q96Hx98LXmJt2^vPEI-&)pSz0srwC$vsH#k+_KB2zkWe`VF&p$Z<@MEc8uV3y#*MQ>Nt#B4EKj8t|q6?XhY+TJ`#M6nG!?t$efEH|ayBG(XYD4mQaI*cEKhe+gqw{X{G-#t436B9`Sx0ELFWqV4b4ESmo1Cbp#lnV}EX96q)Oz942Pn{SSo9b1_NeC(L_9a9!wb<Gv$vk9oD$GNQ5lG8dE>`3rl#ycfZ$?Eyz}Ti4#pEF*2__e%guLbyDz?9wMxxQ!ghUUvs6O=A5RlX6DRMQln)EZp9Vn8^RjC?%DhU?vR40@<DVky*V=T60at=yx|KTVBb?Jk7=@ah`VWx{*%)>P;RH`U}<|vjNG3gly!fYf=K=#=t<GCf|>D6GBSgqGo(1#X#2gO9i5r(x`$q5A%H#M{-ifxpzM3sc|Kv~Al+W-rgC3<JULD&gH_xg&*HbR?Z+QWpOnT_*#7nY(;nQND5UC?c$3>l@TpSBUHtU7s`$iu{#)&HZcZFvDnWJ2(yNz!)WS|&D=X$(Tx0IJ^zEfdk1^#m<yM&(ViZeYQ4AJY@opUznQ^sXYV08^S?lS0>(N(I@HwlR?~j2itrDvQ)<Fk1T@ipTORqV6_EH^hl9V^w-`h*2bkR-}CMw*axW$7ui?Sv7ssmF-%n1bSm0i$)L=97*Kv2FgS|P@4df(aRfXTd5wR92eyM4^i(~WFpHqv-g?|ISF2LGU{gxobCl<nRdtBxM9vACOQlce2vzrvS@SDOv7x82@q=^jgf~?RaxKw&7#lap&S&4@7GAf4Mn()gu#_aRX*McO=Bz8dVJ9vi5{G@6se{ZqDQ<J<PgN@XjICMg!I>nbI}x2$}pcq-DB8#@8!g_q%6?yK=)(X^$uSI^H10$knesQ&2vy>Hm}Z*?S@L4g?}`%i+2sR*DK+1C&_Ux;%Qy|tm1F62INj~mi+{(;7kUlZZL7I*Rdb~-kKAMoUy09R=>yTpdBeAR@0955k3_G1JE@O1GoHDT2Gxp7AfS}?EeroTMR4n`v3$Ir1b0@R!g=)paso{nS7y<d~b4LNltg8Js;iy92FRC-?|BAioy(;A#$<#6O251U6L6C1B*7MLrr{`C)A?b<ViaY_Z(h6AK#u-H?6o}fomy4?3To?x?z!=U(!}Zpw#(+48?DLwWNV|*(DHTQMDJQuY6*;M4}`FT0y8~qb6`QCqk!$LIL8f5+;lNbNq0|OzH<?@jH&P4Z$?Od7ISFmAy4&$Z$ml+l1HcLlG@60ro%-e;RlZS}pkm+d||RjH%UFGCNu{av5GMGrl%M8F=TgA8G-DYs><m^S9wPkP+WR{1s2(P;ys*f=dn0hyGq5oZ3mdde^l8>)=f5qc0@Rcy+XKORe%AVUzpy<<B5(stcTne==#k-GGf~SNM84yZ~+nd~qWY5BO&|qyi6MeiX<)kgC66%Ry_nt{9yn6b}_}KO{Urrl`>l64kLga>2j?=lRcso9@ZzSc2`7*a#vO@(z-2Sz5APaYu$sE=~z~HN1XjRc1p<n?|OTcP(f6k{);G(8m6W8X|+TCplr5I{Ppwms((`&$stH^h{m)x_84E;<6E>lg8FY_c)$+W{udYhT(^y3rJIkGi~CD*atJ8o|wBV(y7Pq?&zXqO<h6IhbH%K7Cm{809`m4mICai;~WsjdW;T_ao@P;61iX&fEoGIiQ93a!OlHD)P-+IEbc@MA!QyA7Xj)hW!Utw+(<Ix<j$Whz9;RONzYIhpDx$ThN34E_Q3B)u%}L$ILIM17*@BWdK2P#eOs}}lm|t1byr+|D<Ds?{Sfk<Uw<FC(5biJC)n0@=+d&>fQr5m(~n`=4M(~y7+FM3I+aQtFKn<M-zTNAHwg4DG**Js{l#VVAO3XIF50!qYt0W$vdNh7W-ZghSKO`5orvn5sJWr(=V{Xi4~ZFOTpq3%sq5|@wD8o0)OQx-{uQ(ZDU$i%S589wqsr(+I<irtV#lD7EC!vy{lU0LbYhah7)`+OysHzOHE~=v_vL@_-Z0;`*D<rWv|o%i2xDSwIE6HC(&lW&8-9tP62-O1WNMRBz(PGPGFm@C#q@H-37wK-19DXblHO*}OTiaZ%X=FOxkHk$x7*<Ups_>1M&bQHKrFP(ny>D100dtAE4HT!>wxa$Oin%1K#1P9&C_`)mJJ-g6Djiq!Yl)%8TCyv0s3yBzVt`tRl`Hh8`K`J0l~!9?xNBJY|_-kl>wMS&<@rZG+e68ndQu`|KGZ3Qhylcwj2hr+6TD(Gx;IQYgxv@TBJ^HpU=D|!qVXL#6QpT-E1tKbOq4S^c}8c07Ds?y}@&KNYwLkbnG%BoPfG{qB_r}UExVB_G0@l(zMo$xo)29>(~9y7j(c}w(a>BBxQgbxT(bplV_m{{4L5mA~uZqh$4|&GWniesSLq}Wyy~Vx;j#uy@XcNqkz||MWQmvI@^FdYN)8}Bj9q_0P3NVS(8q(Hcqf)^kI}f0J(rM1#G$RCx!s4eZNNxCh7-J(iM~*@FmiB9F_VXw$Hgk{#exP%h}Z`R6u}B1bTs&z5b_2k$u2u+2JSM>T+KY1f^;cQCaTSZ~OUsQCbdt?j{UrAf)5@PCC!iqd5jy6{t*8poW^;I+`!ubEB1|N#>Bpz*vDCQ0=B<;Ijj)VMv>Npcd768*kBT!AIfB?mLs~1>lh^k~(o^V7dwrT8&|EPICPXh^cRvLC1^N4DBz9-T}v~16J;g22Mb!ajiWWJ?OGN4q2I4vQnF!a1M3?d{jVB?fR|-rQw)MY567&@yX>AVuPIq+tEMmX<}Uyq7%^>BrTSboxyBd2GRU<5-Y@5WlO*XDDEL|4NzCx*@TC<U&(xLHvty}1krnMDR_x{@APC`MeC9VXMx5m+ctnb42lbcQNt2jq}6frdvy_#dA{VdpEfKe6N6>@7d(bF{H3DRc!$tTP?KS3p2+^Aelef7gSfKmk9E~bJ#-IwMZTQrQBqlj(~uwsY@irML;bH$qrzd2FoS#NE)RM1A)A|#xf0Ul(DvXM@#~tV{PKSovuWb~HL>M`y@H{Sg6>Rf@gpT@W~rV$Fd7az^oH2Xo!2eH2plH|<T$-Lj_hz2OvvUKkxq&=a;+T-NU5!N?mJSyrUu9g)H=)-LNSCD7%?UiHb8b*tJ`7^;EN|feXW@!SKBp;QKN8yUK)yzN88wfa+#hc6OD>V={v}u9r6akv5bX_d$tHYiJub9T>~Rl<k&}G6%djU6Kg6He@%EcQV5u+?TB4}@(QWhdSK4Btcq&et{ZdxVy9t5-vo+Qi>t)cA~w6_R!okmSprgzw>!63nnK3^v?06q&`u`oEV84-5;j4$s9|5HhSevc>?!h1TcZ$_rmLPx7IQ`VXGFA`PEa6hMnMtTGh|byRLH_J9WIXl%0&0K884r#Lxac)H_*d4c;fA2e*UfgJGb63m^i3uf*fB?gBAOGaIQ@Hv37+jW-=+2b=jd%G*xkFDf@O7`TjE?X@^Os%<Vl;pw&HPJixd3q6obnkTq<Be?0Gmn-KR7ZaM_XD|4O<uafcPId;}z#8_^{woSy=$kCYn>U%}K<ru(Kw_SUqf(i9snzXc}{d1=o6bin&EOqKTbDA+(084Yq-;K;ZQ2=v8qGl%0iT3f^NBT1LuGIh%DUJBuj6f_Lz8w=o#$6R8-C1J}+-e?c1N>G;#*d1_!5##Zo_geBp{nZT%#`tWBD+QXeszOI`%`p`G`xng@rpi&bkFh}cTRgy-iQnb+fz5uwnrQ1eyH0y0JQfn|7mu|aY{>2o#66%#M@{_Z!vq!Xi6BMb@yHC!@+s!lp4n!i9lN%!RVwQf`F|6pT@l3CdMLH?(#-$7-t3KMLqBy8Qn;lqtJ#qpS1S`6sdfHwOZkzYB8lK>~L+g8p6xxDroU?D`{~(Q9ph9w4u@1>ypxnD0zkWuW_#*arKYv8P{3tQ{rp$Lu_qGiMY+pp91q?+Nu5x-Z*^fFo=69wET{z<3`%~RIG)N>Z8J*VaA=SQy4YvUBGV3q_C&6Fgb_<8jL7_7D0i>`2Y2<U;pv*|NiaE`Ht~?l`H*E-eP2)yz;Dp2e_&Oa522o`PLQ3gH}+Y_brIVx|m;)p)+6$2P6Fp#bg9PY+C)dxit>&52iO$5Dg)=>Z(dRD{n?-l%%5r%xt`F@AH&f07tZ4lJbg;Fn586J&%?LiWzI(c=@Kq{#N=w<xG%uxuh}gWF!*c7RmH<Se;Y)>26e5;+PhU?_Qptvf?M@+e^!7sf}aH^P10x;#cOXO})qr;92RM^+#g<9E`YNn4jGry7ZI~|1D*Y{89LtV_Z+#WJ9uBa{P4V$KZKD;LRqQn`^^_9l4V4xwvwLr>YXY`d0Tj@;=|a7aTwo7D&Xmr$Z?<xFxC6INL>C1$&p($bIJOt9+C3JbxwFVc;pv%l-nb-+l1@YwK~hOZA~sSgk)S{;-)9vLnAe<jc#Ge9R>_^_;3?U54@wXO_nM`or~?;YZEd@0U-7pY?r}jg)-PN-9qu4l$jqhQ!w(%5)S@u3_;J3fffRwGZhnitUIgctpjLEKO=|0(|na;IyE?z_JM=ju(s=%RsP?m*;be7)VZI%zpqks~nnuSa6_zA_<Gl+|WfV$^bA$7geR2m$$QpMypZqMX`{k{iXRr({I*VPIp|=N2^bK2AX8r*%ibcc3jCrGVrG>b)`&4mie%&R(kkIEq=8FSh5ec!v<C^*@rA+5X+O;0m<4_Hh+$jIombYMFsrlj8-^YrCLfYnt{f706v`!rydC8?P-|T2d9hUkw53#WIWay>v%3iLjs!%+GlKcz0Co}m)mpmk1xOd^v9R-%L`Mh=iBi1x7UAs`6tN}L>c>xboCiko-We@DAF?XjOh)rbC&-`Q@ozJe}g$@!t-)D%bL}mK-0h5n-B!-dLPIucwPFr!bascub*jL$RU8R|7+N9%2kg>mCa<CUpL(q&B?6m|392~#Mdq0mmv{!Q$xMZHpaXOwzm2g297#!;0GK+qjyllIx<J~2L{PDKbQe)LDC>KrAB+}cC4>o_wx0de2JtbD0g|g$BNfo08X$Nj{1hB7h3;qxe@$dAM?{cfBo&JZ<F}tbko3m{pa8R{`&ggUhCDBRrc3MHK!urpndyoMuoWi;@eOfIF5eT8;R@dul(^ZMa&}dQ>#yr4|qB5*U#52BvfK}@*0WXzerSrJ7Kyy8jw2OKPIRx8^-#b+WV~A4d?!Z^O0Cq>-yF40bi)dZ=cru3zZGu`~=8-;?2;vZUQhk#{B78JnDFXnCZQvS_SI*H3cAhG8>OKe}oE3-g}ANg7q4V_TWn-(wAI+sWWdY!v&z}v%fSK-)b%eTP-tiH$fF)W%84MZ%=Y2?}Ya?)@eQl)65n}FKK)J?OmMx>U-YM3D-LC^sMO}C*Ghlllj)WGNXlqiEX_OK4e143sudot$BJop`d9<zuDa;lr`x1Cc#mfv$IS|&{k4H)~JIr5h5WU%ov_T*w0r3S@mjfaZV9Z4StT{OKboJTO!zb-)E+}Zqb|OIKfXBzIL<ApENNT@;7SD=h}1Bc)<R9XzgI~F&{I`UV>;g-c<#4=g~4nF8@<P!OKk}-qdkzsrC*&WuLJ~X3&4+P}1A}FOV~E%iBqKj6qn2_Hwy;S<Y|NPGg-c_I>iwM`#-RJh?8&1h@6j;q-bc1=HD_u!K&Im~t{&Yq<vIc;Rer4H@ZRCyYhbCo>l)BeRU$gzV(Ynr^@ziyy##4@{*(Z^jxUZ(QD}LFK^;rXuOV2VCp1eUF!A9e%V8mI*zBE%A)t0|DBv73G!%7IU035Fy*+J0TK5XmZ>^F?GcFpM@pFN`tl)IOMLNvXFjPc&_dBJ=}s~1MQW(2E&?cC<QKz4TqrrM6sJ<(b}EhIBu3>%_cEgOSsD;Im&FkfXO6NJv(mAuJVtIOVG1fOC|^z`2y9Kp!eAjH5>&(NB^rVWysZM<A`W`U^#L&kmzV{t7Ta>hFaS7>jn`7i^8fecHyqb&$r(VXaH`CTpO=_5VaX!GzsH6!cQF5J^ld1X=`j3##<j8W{sjNX4|1vk0Z;LeQ**cdAu1Wp>Bo)(242fPcSF16?6CK0QNk!@xccMv^5g(eLRvbTq1BWDaDZFqZcCG<Cp+o09hsALGJclKU5J#E+tFkwo1jSP983XI(@?k=?ickr})Y~&mDM<!Us=5V9NS&8)lz;PuBzxrT~v~IEw?J+v?=gufHFOrPvXeem&3wh`PYSPX?cZs5h-tY82ZL6>9iAzCG&%GTc<UJ2jT2y9B8n<7udn&us;^MtoH}H5e?@NU+l4MCC;aA)>v1b9paB{tY}Y5MG=-m{9+kxC1gR_nW8pV);7a+7r2hD8E-)U3G9;?>LE3+$VCs%Br^tvw$(k(zA4L7r`uS89G_gCemhw`ez(zj|{5Yj*Y#;v1^`Z8-Z_B)b`pLi=x?wioUsaew}$hcvo{Fd`+ERjjyvdRBdQ-g8^}Upe0`;flz7Lb?GzWEo=Jg&Lj@wK!4>ul(N+(zV#>@0?kWd-zO>Ot}IEkU1y*3Tzh@L9vwfceqgLcXyk;-yg&v#Rg0zX9Clgo;WLyf1t|A`uz^rPLb|>aIaW417-h}SK~pox#1H#kTkrTl14#9>C%5<E;If-gFVdpA(v$aY|EbPn&~#qLKy6Rx@tAg<ultW_!cqqcZU^K5DZ&(@I((L{&?9MewiVgLZi#O@G8a!nx1>4^(MzV%UTto0H+A*Al}{ldrA>74w?RF4+YTK=C3JltNBa-t$@CZy6!+#W9o;iZth44#F?J5wn>WE_mcf|@@=E>B%kR%~^%5KmrX$8=ziqm0ymv>dkl*Xw3Gw2H{7g{fou~+dOtH0(`^+8G4nd>K*))qQ@g(KUPE-dbS1gj!JOKaNLghy?X*2&;<gz4urtIua19>=jC3e#4FMO8?`KG2?i@_U4Ps75f&Q35aExSX3d5=|#qEqb|^D+fdu9j~c1#C{Luh;n`c+a_7&Yhj78kdLIg<x+Ot(-m<PGw6eJF1_jiC+LWZJ}aW>IP4Pe`k*9j=Jl7sQS+F0QNpaGBchzM3c&gtq@e?mf11}wZZ#w0EtGxEDC8ZKHF@}%~aL|!SJ^ggM+-4T0WWTHup34Q*Pa8(fkrmPOxjid~Xs}VCWd~45K%3kQD=^MlXA^{F0(q5NA==$_PT^4@;ajb@NfLWXwvU1+mTilST5%E-&yOuY07&Xovg>j`c!!YBr70D1eCsh-#OL%1@qCXwPRqizXl1y2n#5N1N4jYDutG`;a&8T6(t4G~WN1VA;G}LRobxj8?#MEuOtU67wy0p>T8$*S#Zs$y*dIvYbug-1<FWD|D_fdn#~Me4!?jtjM?)h~)_Q7FH3cQ-i6hDYwphqv}*ni1)d5^(nwH(P^tXV<ngtKJq<X<@p9SJ2PYy&rQd-LT=c-iJG7H{@s&ls=MK~mfe#c@f>;NS`z~FyR5*QX*&ZDa<$izuYC#ltzshJ^*<9^h6y781o0-j@s0`*ck4n2jg}h*EDP!XxLGa<bfysvDcxv$_;W}M#bvSfP7It7$q1ynGz`*$@3v^B=qE(O*xW0=sc3ijsN55jW;B1ZZ6IN9tEl1-?Eajpr1Z18>x_XM7<+YHob-e~x5l$}!wQHUYmQydlp1}7q6)CTR^?er1(@ej+h&x+j5R?~d0@r-!r;sq4M;X|Oj}LQzej@A$ga>zqR&?~fq>)y0IBJcQT!lX`N*<-`-o?QB*C<nTs$jXZmjGIsPdxH?i!<nOYW|_1157?YotMOe(G((rdb0b9MT>n{6X!~3jmX6*t{IoZ4qlSZGhuwjEDpgYG5y~Trexj0T{G`1{~ddm3X8`d3@B#v71HUS+d1)g_2bz<Qni~VPBJ56(>4^nxNa4`pkMJgNkSqjZd6b$>??QK!etGEF_nX*KO35LHWA1Y+r^g$UJLJaE)D?5ceyL4#=kD2eyIuZ7=*DfBEv|_g7g-I|fe?%D2*l_Hm#f4;B7^P3HG`B5?Njh#zCrxdR|TR7>4@oA(W(OStuwwH@&LL$*SaPSSZxswysYzboA2eKR7`N7<A>UJ1=~9l;s->_iEIQeDlS3x>Wqf(7BIa0f~SGK4?V**WeBQPMH<;pPwe!}qb*D|+Y*mfk<P>FFv1rW1tzfPM%N4mSzz7yG@3h8q6pAL+y-_jb@=i}EM;&Uv2fv1h+OB)kfg)S^*Sx-;v4U(Zjtl)JYB?+A~E^%k_qhqBq{mDzN88u_dX4wF+(*9C~?+<WVS{M(nc5RQ!DE05_sf5y%JXlABd>tZ!@zD|3JGGO1y43`@;H;Y%a%d)pB_#1tP9zr7O0_6?x8#W$kQa<ShKj%%f2a8d>d8Y`1v;6%4ybgJ_;HbM5Kv2{Zu=L|?s4rt8e|^=L=X^i)Slt=6W`YJe>R<Ubb31U}L9S7Yc}+WM)tfE2TQ^7CPvLGiSKL*Phx=+&PvYu_9o~cEtV>nA%6|j3(4S&~3(JPr`5|j#l)zCr;YGOCbTJ-FgmAwJJ7R4~2-9PA2Xc7j42@nt=!`E(`a>c=LMhUqj8p!F39pBmUn9n9T@|uOeS0#3n^}vA9s4c|*(udCN+RAE?LH#3f%l6~9-%AApuLrEY(>*f{mH4`f(^{&dFRy2cUjGP5LYSL+cb%<7(U*`+JDk@^dYTO(4X)#Ae}o#bPuGA+(pLhvV2685_)9OIbe|AZD}F^i5yDlp@xEaXz9yux6T3ptSh2CwVoC-FH%=`dN~;(rte<QTU;v^fWRFv9g>B>vUKhuR!=@j^Io6XbB@a)m3_kMZ+vsGwl{UkNBb!#oO4o^zhOw3Yu@m|xc9hvU{M~--M_DPfLKoz$sQkK%=oZR^UY51?Q4qk(OO;FnUuaRT=rIWcS=G;H#N=M=ugsh2%puh_2a}7b1OT_;@GK$B1m~clg{j|t2qP}XzrikW2F?>VxUG0$x)zfZZ>Ew7&~(7F)$z?ef|LqBuM{YoDfagLBB{l2%~}$6AP!Jxrx&k*snD*#9R+5b&*U%B{C>7F(^R!zsatVrZjWyI7l)9uU&!a7co&#+`&Kv06>?0S#0$``P@~wo<X8PJGv?@=CqF?hP|j{<Vp;~hnrq5CUzKL&k#4fCW_BX0Tg;h(HfXh51w3$*4brTfM!xQwZ<lnQ&PdiwWH+c$$qh>8Zbz;S%ln5RYh3`;QZA?1dMFtUkxV3UUVHhGHBBJko5*?p`JdNQY7DF?6$k6$}(v?j8tyg(7jSS_KcQ#Do!yH3j`N&{f;`u-tRrzCH5j@r6Dsz8Azwg-VlF}^c8%@Ej(AH<v>9JN}8~<2ic9wFyT4un^r!3R5l6ZL25C&-zXS5g2ijImdLw$0!9UEzCoplZtxFr>0EW#QH2LO{YJi=MU|9GEV>oC3iB|oW&I6^<R=bYNoOKzf`Gya=E7F%3;8=zRPg8=@4j|7MW)&E+OAKHV(FR>UTF?>#py$3mtJ(js$c~PTHB8#)1Xm@`X0Mr#q>_}eUURInT~HRX=1%zRs83>fEE)v)8=@LUdfxvLECF^x}80JYIEjX%E3@wkn`MWx24~N2pqymEyylztd5tRWRiU+r|xHZ)I`_@t4Seyf)Uil#6X5=yLg4K;hWZAAS0BqhEZO;;4>qVOt$Frp8$ZRXC+$pPG>$X|M=?ho^im&BIg#1u49{cerVaUu3~WPwhgEUQ8t0U4_l34hWVLgo;~mVVD)CfmB=2R>YNZ^kxLd$%N<8~St{N76Jtx&YI2h45MkaEx{WG4#Go1{SqKa=`iK>*&yqmMBtS;2j6+goY5=%KT7Q%&w&~3Dt_Wzgcb-eh^%VyFLF6fpW1S1uRRRDE2;6IY##PF$l^<l&SDPk>?P%<>cgRBlgMIZt`|b`!srNS2F4-uHDp@IwOPkPaJFBRmmm^~lQWggg<^Tnu789qi=<TV|877VV4!zEnw--zc%q=^^wp=!InJIff21`t|4B&+f)R&7b6d7#aFI#))SEICxVw9pI$YlokJ`bC{$vJSu7GJ`_V`r_xMy_j1>q;5N+56k?%o^KM6I+A&@P~}>j(>hQGdKSuBX1MQ?n6%AJ^zQ-Uw%2qqu+<bOUQv8y|4-ECFA3zG=JmtcKP&Txj6cJy<*+6y}4)rdc{dgEQabLx}rv$=gHKGoxW~mvo!IXGB~KTPA*459HwesT%|H7AXm=84dIV%Wn2|9l&2Gw%JwDh<nfuQW$=<cyx3S!a_>6uFu*U6TV!32oyN>Qp(tW(^io#K;4X2a2x1845RW3b`V~GEymup$OL;jLz;AL}bAzA#?gf*Y7QFo$0J(|4hCG($A#rdet!c<ZtiCpe``kQxGV6Y}3Nk+0r^AcUr0CV~6+!YvfH--G+sU_NR;Kd3zWdFoM;s@eEA>Y3RaJie^%t<kEJ>h2=tB29!v&;3+pH1M7Oq)Nk84jZPA6eJx_jw-`4E5?$lk@2*uptiF)jfEEOGvfuy}eBtJ=S;&kzKTM~k=82G3^1=-&nIPo@!pUEBvJD}4HI;KAX;TY<Th+6H>DZ|9D3cF__^P^hjB|I+K$nTC9nhRSX{mM6m*dCyK9+#tFxt#)J&aS=Ub1KJxGXXW$)yJ#2;FyIG)5(2n&0%IN`_m}n!Ffj%uH4KJbG93RnZz4_Mz~FZo+m4NjoI?EinrC3$z}V9Gm2@RU&<yKeAEez>aO-5^EwFu9z0{B4-?M@qn0rBy5HN=>B!LmC`jKdyse7BPvmHX(lWeBPL9A88c4QTXK`yUt;<am^Jz$xUock?Mxqr|qu(o%uI9w<+UYlgDy6QI(_=9+;rJ&`V=T%R{O>{$Y*Gh4_&e-29B}kq)dF>89=)Lhk35w&=bR1@KTxYLi4~4v#AQb%s>j^5B30}zUo;pA0Q`GUvKn1ido^%F@`qBt?SU%l4rXew)A24xi75){ym#_e#C(p$M19-a?1=;=RaS8>Yf(AOOUBbu(yJTm(j9Xs<xi@kS16QnsP}1UycD2ZtUiko$$%J?!P)(a>@dLHs7=}?>E(!%iw_7|KCb{=(a?Mj=l{{?oP;k`k4l<CU6{HE>jOjnt?P%x(JU03LWN@r-0uM9xd#$tbPNHF~&(#q`pQVB8nB;SWErPpjQuFp}bu*Z$=A=$HXjiGx2C94L2*9kF^?+J8caO7WLXU&4hk7hPG{yiO{o>61CmhZlGmkjtU$f5D?f^q16@!z(%1}WHlQsfvd?$6VmJ~i1*>OjabtWapEU2doU1^qetQoWAMszScb4e|1-D*apLfq`ind|~MSy}$e`@-RYLw3~IWTJ}@@J-pJ8@0+|>5z|2Fj&e>yLD>;BO!^3@(NcGrycH5nIci=BREtGXi(w&8X+qSX#ehWkqiO|RD-A%PUh;wE&gVRIIr(>2n85IgBVI;WnvQwyFbhgXzC1CcP`=)CxvL0S|0!`Oj=3(kCJb5`IC1vzYK5Pp%QRHekfK^HxbCvmj#E;&fM&w@ICZMX=H(6eA>)Iv8?S`m9wj|N&EJQd%|884K4^l6r%{`r|GDe6b@A-CY|DXNTPE9ax8uQD=@F3b>gGy*EE?iW#ya>2hM@vwZj&L3dO8Qvt(EhrMh2!ro#%MJg5r|);L=vc;VE~W3#5D>>OwAT_T@@loz7LHl#w+3OR$Pf^hy6i?&IqlX1E!st&LQd88>`*N6f`x1^lXrrV#P_X9~yu@AXay^k~F&cJ=uCh*AE>Sx8OYgpV~?Ku<eFxjj|$Buw_-A<8&%4l|6n2}jc9h(-sS3#CK6t2|aPa~6kYS20tb=3{C08I4_iVlp$vQ=<c_i$i75jcpDb``^*)=anNG21raJJs@+O15G$PuGWA>CUy<fjW)YHF!uQu`)f?o`(Z1EA+B#*>0awe&TKN!K*dweDquV>UpDSm}5mZ^pio?+a$~hvxq0Ht+CE4ekhD14I>PS1;i(Kfx-~5!L-!}qUjQ~Q`KP4&?~XTsh|qtD4(yrM+H!0Qie!I5WOl#uQh6Hs&i}W6j00NEi&FJdNxaiEEhU?Wr~MCr{ag6dl}3F44h<`laXo)>*toLAMG;@ML`(jL?(*hTFZ*YL-jwfxAd0<F*AXmL3`P#sf@K2b}`8)yds@>o)o0mh8@Mha#NO@(rw-A_&l*Oi)Va@he%|Pw{Ya8cmO*96aP#Se%vf~m?kBHh_8m<5!r!5ndAV*CJ;wJ$nNm`)SPm$sa}NyhLA9CUqVK9xZT<%`#fY4Fw7c@@l=cU!XRg2szCxdtwChqX2PZvla!Fwwp^7GeVbFY*aioBfQDfv>r~vNUC|>>Ku4VC&efyK<%Sq5l(f1?(pcq)z&3%RiEohUnL;Y_jx;q(d|a64u^w`8|KZ31wI75D>l5!wVK$RgZS>&&BR8l={VY>i)#YP%FI4J3wL0r}YO<S@w$1P#0&y3rxq5mv7%^4@I+Z%273qO}mEt$ULbBwu0>0?0lz)YxaU%&PYCfF9%3uKA!+3k(AB{F&aJF``+r8A}u?_ns>H82xV5aVT-i7^YQ?%P91rSsrDbPl#^`~tlFsr1Wq60A7W>f`olRmh50~P2H>~4|+p15X<&A%FB8a7Pp_ixL*cIMzg3$IZLmaG_9l-<WWhPBnRUIcne5pRV+8sIr;*X<S%QM>okwr)@B=-HDk=!iK|W5VcDOzQ(-tDeQ3RGKs@!KS@K&f&=J%|LJU7M<3fL=9SGhy~v@4JLYV0f#n^QzTduj<)oKw}Sd1khWmn8Qdxt5jnjGXh@psB70uGvAvgK=w$FRmr=1}aCon?OBVjKW&x$Iz+zrH929&7*EzJfgwy=QYzzv(^Sxl9zhoo=Z=44};`?r$LfmhK3uPEAja1j<8{G4`4fD5{;@0DhUQ_g7HS?=!vLbrsdw~+c3r~_k>GneUjm2?ls!L@!QlfS;lp^r*Y+C!SqCD%i0JGRBaD+q`0KOXLU$M!L!2LFwQ=x!vURNR;5LIIfqbdv)w0t0A8$9kL`OfnZD^y@)1&i>Y&q{||F~LPR3xf$j=<3zPo(bT4%^^jO-P2ynKj))ROPGX|wWDJP+q)RtuEkRj1Y9)-)yZR3WDh{?)@!B_Rc8!h^Lqh=7^HZf0ue@6r$;&Ei;X0ZlZ#8z)qC5&<SyW#!e|%QjWAPjX7~<K+%+j(HznU)jZFNuKJGx%N{#L+IV5^(p0s^*PfX@d|LwW-MeIxNdS*Yw_e$)u8)nS;m26d0N*y=IQ2fqeOIB&9_@A_n0@+#>Pmw!;Bd6MouZpg`Av#DRri-NnZ>>2ZI^mf}I5<^^S;e{^%@azkdMswjQFdjRT$Z;<El$w~oAVP1Uf4d#Zd;D%01BWCdOy%;jnIk7Cm1?d$hwn{sg<-c8+;tu<LK_0@zfba!CSTc_zduRW4Z#JzYW)e3==2Xx_AnQipBzCTuP)q^!Eax5*wv$Q#7Ti%rh;OzIbUui?*bJ*VCppLXY6dE&cLmkdD<oz~on%*x_!tNwjf%X(C>pH<feZ9xI+U%y3QxN{qVNm^KF?DF_lEWIK0d^b`sK$p0asX)qm>c95t7-;p2&tP;lA_hgGK#e9>w<0Rb>7m=5j^gYv3`VlnJF<_2!R*7J`yc*Weld8EThE9WD%08Fx<C3Iz=h()^lp2MDLM=Ivn7;l{9Zkx)p%&`i@Y3_;QKXg?@aK0V*<$t{z4gv4Vq3+zbJUfr7tNQ>#H1&3DqHP%775woclY2?y0flg>qC>h^ELeqo_J1LlG5j8X*}ad(>e;dL6;*BNPS!si(DuR437NipdTty&F3yHDiknOF?XV_ka80UqyPhULRgw=xu4wmv-J|C88_*aTCR<|<XI1Y&XEWf=n8(<iRrBP%5jI#Tv}b9>J5o`@D1X;$ez0{p`fpBqRVduY%neG_pnjNka&u*9tZK#{Jh@URa8#tl>3j-_hs5~>?$!}xxK2{rwR}2*gGo?yw5~srjUAo5WKOfb;pgTD3l&)mnpB2KQ!qnYZ@5WVAldbck^tF6q9QnY1+5i>;I5gpT-64xc8|`j<bxsZ@0+ZOK6W4StU<4jB|g~aTLG168<9<%O|3sjo>UhE{!ZT=)>+0(0Gkgd45`6WfTa<9kEVu*8Flg7%u;d_m%m!wczcG(LQ3#gALn|{#e@i&gjxF5hSBnBAM=R;z?+sEjPN+AIcLUq#L0tb8Nu0cY003uwcHzW{90j#W*EMz?tDaQ$XRh%#g3Va{z2*{431)gR3C3R`O0L=F}4;glciyg>EnT{;fVGkA`2Pl<fimn*kL`J*HHluXjD@9>Eu6VU*3Wuj)-X0WTy$UDp%ai<?i=QblZ_^(gKJGUa*GkgF1jmXp2yf9nEI{b7w>vAgzpOCF>^rB3J-h4$nJ`QbVK#BwIquy%60uI42nfmY2@^lS*7C<)ME^^Mrk373g3Q5EUHwuq@N1V^V|D10?wf1Y?ZdQ)=YKjK!UHH~E#0G;AxjS#Wg<SOHLg<sd`*4OX-pD%xqgW>!Ol7hi44b?t@Ac6I+oo5l5>5^sn>`JEyrZRgq6CXHg&$L`sO>YTan#qn5N@kw`a5Q9EZG%9S9jSDXab29=m)wTv0o6B~q@1+?gJtO=;x`YSJe;X+L}Cm~0bCwD6Hkqn;mx)1$D}k-@PX3EpjL!;<*GkR`TSUAyv1In!~^GWQsEPV#3B?DEDG>X>iD8ItpmE#K0hfh?}IBG845fvkt5W&^gUQmhdyZ*eozpNW0vRxVIB{;IW&9e5VS1_WQW8ay(`mULY=agTkUUvlo&=R<)C>tC97vJUeKd%e_*Dqfx;RwI)~WV<0cs+eC%F{Q%W<QzX*Y-opi5*nQ8>S%>c^R#f~ZL;635&4iy6Gm&c6v45?OU%nS!slikdK4CZ@IgQauGSP7Cr-Rz%pycK}xNSkGlUf5fv7Bh#>S{M*F;gsJmfj8@vqnRBPgdM8r|0hcUNTHAIaA~ccY%6B`v^B?h+-a^WI$cGEz)kL4px<Q!(RUMq#08JI-9tR|2WgGta(hlpKe?eAR}&CbALR`RFeT?9%4_4THBQGbOBb<ARQ<iWc-JupdnKPYtUnXgXQu;rp71$1H}b)KJeo{v&KFI!*?+tVoE#+cxE<M-4Y;f+ezkH<Wasvce4gR<$bdLK#wuf1M?pKF^@73xG6b>XjZ{ImzINE@(TCG+hUBW&qkF@H%Gj?%#fSet0JWwIf6W;)`pdSn*Lt|3L)H%g<fr5kEqSB|VHz%w%ctEDwR;z7W8A5e15KSI9@$Qq3A9C2wpBz03+4g{Y^(iV!<ofkGw~4mcI=`tU<^?cN8tR|)7ZQR0U9ri(-vv0fG0rk*K1J9q|XARbZP$CvpO^r%MzWkJ*R5l146GBbV8S0#V6VcXG~wIiMGy=E8<Bp-R77M6i1s`aFiS=+;c|aDJgS1K|eY*2t)>=(wdgSUlMRf(+QB$bC^E(s6)rr{C!_A>m2`cw1k-XIU^6K-N0=E2k8q@bb`JB;&L<9-Wgv{Wxcj-4RY$R4;zuhxf%N$VDTVsrk^h|NxN$-c{voRq{ghBq+p-ii|3nc^|z;b)Pa)%QdDa=3n1~%aoD%aUw}@fA;l#+30lZ6Ka*4_#ZyJ@Ve-nnQPSxKG8_!}<B*|=`S6o-R*lo7F4e6^<*NMRRL5aMonhp7bQ(n2--FW$IZ;nZ=KK7l>pMN(QM%*+wGh(Mha9ebTPS@aGJt`=oLfRA9>&s2Q!_;N5?$W)Ji4pFc#|7HPvI%wor$~BK?c{HEXK9KD3X?YsWE;$_w3xJGj4=m%*6Yh_R%t5;HulMSyW+?`Y%leU2u$Dojq!LYb$#t&RmR#vyW_K<PeP_pPQD7rKY^l1tu%_?IV4&5!W6Di9~aCm4L7R`n%;p!#XouTQ2MMAHrPL(*<S1`CV&HgrWs|5b)0Gk&A`@%CGG}YSOB#NjGxcVA1~M*V?;VtJru&vq-uldfsZMSPq<^7C@Sa?Wvn6-0QyJ#@X9RAGDh||7mu|aUxVulHqct#Ir7H17s8}cc$uzr};nkegzu5bjrTuPII6ic7+tOd#fnF2v7`Asm%LL>!Q}dTxt0mHLsi%kXJIndt^*A>0d?rW_{DirvfD&1EtAYf}tu{rN-{CqjYc8%jfbCFE6)*uIq{V>C>kT8U|k9p_YEKT*MZO>928@{`%!VvS(apu}_Kh*bi|YBgOAFH-8G;>5VGpC$KZ_I<u+z9uAHC!F(##0&n$Ep+*4XN7gA+6g=ms!{)O+JBUft6wsijd1h4xQq6!d{(t@J*MI!{zkmC3zGIkd`TACjZZR@XcFFiO;K0~&%kRufDMkREj@`E)8tY<yMWN4tE!tj#(RIL^06ekPf1A6P@pgQAGX>EQQ4()7KF#83WHL;ehQQ3m>-IiRxdm`Udxj|!oLxgL5oigKJ&#rl3L|SOdHJTrmak|JpKe{uOL|RDMs5Kv7O_ZzDyg(i-zW)3C-dd`sfHCO;^P%l+Gc@)@Id>1AmM-eBwk2cD`#pI`A%+1#IZjm^XFjv2g9=R{y>?BjMA!#eDS03HOGjpwB?E<yyW;XhF{8;Iu>UWO)#l0hX)_G>*C6V<Eo7Q>Ra9Cu#eskTW|nmSb!7Xo(^T%t!QX-T(Di#6}9t+1*?%;f7Vy|ZJA%bvTY`9Tf4|^t8xt;BVgMTw<WsUrTWmROV=M3f7r}Qyd%Fo`pZkleRz3!PWAIHLwQFyi$X;G;rh$)qh{_p6=*9gkkw>dRHg46V2cDao&@@t4D|Hjkk!d*VtoxlR7XbW8iya(v;MrL0ZhE3Kesy2Q!t8Zm|2Q~-1q(DWz}hcf`M-nL04XYVyp$hqPBIfF>0q+lrf(IT+4E30<ytT{)uEeHWNe_#VDh|6m3<NZ(c6X78<Q?!578iq4t;N3r)XSYdPI<i7VHK_6E7f7orYY?4Xp#bKp-`LS&i9HCPC?`~rNW77r6J@(_I42P=xk8WPjRiY5MQviy~SSESZae*i1)y3T-QsO*n@;M=KaN7C5iJOH0Dhf^7ZBlk?t>x0w9@yMU^Z8Eq_dNvoLD}v1h?d+BS-)hYaviZMqp!a|M<I8V9{qd#z^6f$U@_ZYf{`UHhFaN}Oms2V~Lubo>ENMxUf72o>Qt<<`DGN2@>0bS_G2iQH{5P0z=A9uI_sPS#|5N5(aJ=h%Ag|zcDd`GBiE7~W8=UL8M-%wO?e$XjdjTM;sH(Fp8|>!0!b3=R^FL~?m-W=QKSn|YO6~VnJ*s?Q3#b#|ZuKt=d3D~#4>*x#@1r*utaDU<V0drygBiU-=1YzA)<N6XPrv{4^^<);tR-xBd7H<I=v@F$@bZuPLZ!D^|80*WC9a?T`Ri{#eVfHEryDu9>p%bg_t)3|_FB8HthK*BsyPt>$L-s1GcMNU7vF}`z;pDw-bi9!f8~#VDdHCq7F&Iae89_5zka@MAt4UIlh?rf{zam+jH)JhG$3!fe@swZHjMQ<wf9-K8_xX?=OeJJ*7d971HMq5-#)GR7pl#_`3dg3+YoF5FgQjd>RL$Zc!5>ey(0w%NCGwDCwnp*k2imWYD(UFiQ9tp8jSYft7X!cTz?4_hv9Gmy87%d&BeExOM#OsW`0DdysRw6^6%|Q)a0G;zR5bx$6%V-;^@_q&%eEkn`wQ|8#?W}FD9()9VgzPOOyH5yE3DlgNbduKt5zb$qSwOllBt|nv(RJ-EBfy1JEEDa?+ZeWl(~)73x=!+F4Pd6Y{}~E=tr|eYFvSolNyU8koV)F?<ORK!;QG^rByjGgDo(=$)yY;HL{;yV>PWnz(rR8@1+h?Kx^ZVE;X3CTHggZK>X2n7zc&Y`iC?{kM6v>lW+T7(-j8O(Wja(cRwu8$V^Au}G%Sf8<co+x{<5)0g7E-$~evL0Ec?)vK4~{DzZEti#2=PhR>6O=F)Y*9Dp2w){DqUQY#KI-3@2NQa5rMr$ospMsOl=GKsr4tBy|WKB170W>np$m7aRzO3m6)Uo&h?DxP_F!W}uG4jUcjk;YPtY9jVHhjRf9@o2lRo3B0+hCc{GuRU62tE*?{aUeZSzs~8DFYF*J-!nn5rihk9TZtd9RRbig!q%tHUlF-Nh%BJcZKKLUf;v5IyP`#$!jpY?uPQ@!gO;8`cI_9DHcsMhB}bO?!05oCox(}h|43n%WS=X$s|)fJ8sPu^^c27(6d=fCI}h%0@atG_t_9N90fv0|EnzJ$)Z$_BBJeqW#5vVJ->*@ffj<P(r(;e_3H)^1dGC|3w+_O$j`Um4d^Crid-A7eGs)7Uo;8hI>JvJ);<0J#A$167sgv39A=H8E9NJnRh18ksmwk&36oUb(a>%J;juKL?KO>J5U(|J_vipNJhkz`2L`k?65;xF)2>{imN6;CkmREmI^E-#0AK)FCE!8s_FX?zUPUe?OGLLy(W<5?F19*-!wBgMa2}`l%0AB>c#gscPeEYH`f(d(pL|b8`VUip$2pwEfzWMr^6A&#kHk~#2u!~o=rKg<$;~H&&q36iR*E%>ZHUS>d>-B<yA?9rRJuDw?ycdG(J`Ke3jEx*U~9xzwONC~GR*`lElyNlWYaa;`!|>O!bHHp^8yve$%6?gF+KT=CsyIko2U0;`8wiNqv<}P|6Xa;wVzzH<o!7z1n?(vzsjn&3NwN+$kMZPZx_KVY+=y$5V7o5sDH*)$%{#K8-kMqj$QLS+X#H4qPEx0STxT*R0Pho3+&7Z!n>La?Q81vYJ8n_qH05v8w`l|1FiZR352rEt_z?MZ&}k{cP4R82jVO5p_DB(@vSHM$q2z0D#1@uE?!xlXgkn8=ehR!emy#VR{g+Ot<cB`m5fTNYC}7RT^4-!45dl|$~_=#AXJc$uJ1&SmCX)DSu=Fd)C@B5!@k$nJ3i0=Qa$a-?R_}7>?YKUw5YE1<h|Q}s`D5$otH6CTNQddrd{Xj{$rZ3)PaKA0Xa;HFog+*ze!c-k+h=Sifm%H#J3%pi>IMmQk{nAB~w|iHaEDNx`y7$rI3))Cc60BpdP$!hmN5dx;~Jj{Ri@7dJG7Pd-Il#?inT4S@WhCJBRGeo8U6b;7qG}CH?2+_vg8K2@VF+USqP~Hr+PfyQ5Xe@AdA4m~ljYCMfbwRD?mM*xJ*5<_>L#pwZ=Q%Egs<l5%DzssocN7D;IyfPZbF@*|nFnLjLYaT3aPc6O(MJRH0dyK40pzGa1cQxd|S=3_O~?9*eGb=^%%%kEHM-ec9G=u~^gzf8ZED~B3K0h^O*5_Ucb-gB;&b7$wN#^oV)A=n#6E2oczQ<YN6j_T)W;vc{rV5nG@y1~=n-<c!2qwYFWtG;tQfV~fq%#3Fi(WLTWD+JZFWwwt&ZSZ~^K%x;a3q+cW&o&!#OO-W2F#K)B;2>|M{!ym7&Hc<>mHR+iG{4026YN?r-<w1g7&?Xw$mmTRWW_+K(aWAJ^QGt&#95TJGJ??f!xE=W-F(!G8MBgTL2NVsWRbkG%M1L+>mKPb+97{}W4+M*noVOg3g93CqS~c`@{?yf+Vk1ZBFTrg?(x*i(PlNBS`w_)K4i4JmY!`hjrTt$ST--0P*$A^qZP1Ri)ZhT#C*|RC>-6xb?->u^A?4R{A-gqw|)=U3Y{g)o(fzQU#Q6>D>AMHVmSi7g;fOV)L^P=%B}O>s5+Gs;(cyieF|_)blR%USP7<uk9<#8dA@<o&I}pFa|iRSkQ=scqE70)8Te$H>TbBLW%r~<JVze6)`S54E-Ub6+RgxkT<x{wYhMC>tC$FQ{m;aPVZsOiLA=RsyrTld-MY|0BPBAj{bu~f&2mYgGmU6S=|<bbpF?6OE{nByV&IHOMj+LtVUQMlw?#8WKOq{%=3enlMZ3dC<({B4qxqX{0||RuMHPo&_vch4rJvPZXAI=P*sJT}q$l*bHJ-H_RzU1nbL@Ji)aWY|Re=4qD$i0Xz&w}QHlrkFtO<(B11shi24~J_K(dKr+UlVGJrb-&c7;|FeZHy*1SAIlNKKcF;s<HMN0#N=M?4!O38uB=;#ui(V`W!Bl^2zE*BB*Sa(CSwFqzX@BMpl4Q*R44%^DElkoF+q4{DcQ0GK?(=H;kvi&&Fs0~|+VL?nn%1ABSpf>}}azn~Q~;OOS7#3Mz@<70y_DLhNISgugAs)Sqvo-FKZa;xG*M^F=V`%<4-&ty;$ZKCms(<&LgE*|L4x{ih9(($^Dx-uwVx0db8umzcCtqHENYZKyrh0y`ol>ERp5Wnq(-{UV|zWn|wD{05zDMI;Hn$SKD6y%}8AF#>%K2HSB9v|^zj5>D!1c+*>TW|BeL39bXzOuFhet*bTNYY6<Z%I|fh3<Eile}$4MEWS3638o|nXV%^BcGipK~Soz*>l0rH%G7_92M?BsX&JCXF5B_Jt0auW<K2f0p3^-{9Jx)-LkKr-1Kyn0n-UWe?UJ32#1>l_ly1BLqiRJ^pA96l6yO7utoWkd*?h)_Sm!E9}->#N@~%lDcza%zpv+Kwv->OJHn%3y#+1up=|bfWj0-&Mn3C;!{n6HbpfI|_ujf7|Mq1qgd=14%40gupK-H4nwcrrx>yaJuhX8Q4A^%v!{r9e&Egg9vh1x2{zl)ShmeT6KzRfFhK)y>lux?B&v_H=!D19|-YJ6MEPp=$uR~rfIO=W%5ES(UEd6*J>dTnOUtjg*Ip0q`R(FQ2nV><A`d7Zq+zy;~kZaUpUeium^=1q1*3A+3Q@GpB6?fI+;l3Kxleqd}hxgz(>rxf3^4~x$^ru+h!m{CYe#qJwC2&+ucoD8OU5v*~ND*s7LI@tKGLWO{7~@*KTF@Cyl4OTOY=jb`LD8oC3zJz76~6Z1r`7`W?WqTDT`d%L>^mrA7gWy{i8x`jvxrav-Y+$IJg($`_ExpA)k-^MC#NzCwkwz3ozp7cB{S<GTV-NzQy{)#_;?pb%ag8=4=JO9+Jv70Y1lCmdmvNfE;43?<)fXHtRoA`0XzI|OM?JN(onh%^%2ZNOJ8-nbqxT}T#?|Zt+bGEk(#-qcjiUDzB4^<U#)pQ0&c)`NQME+z_~+MJ^3Vsdwpil`74K1(g`cO@y)?n+SDl@?Wdq9&Iwokh9M=ac{2y&)#J*5MQ1Q~|Gv5aVm(!qdVGj6Q^P)mH@m#IuPM?aYjt2}GWohF+1u3JDR~gxurzOxKS@U+d{(!%juXGjt;{EjKc^OoAlwPPIkRuB<`7hTxqpU_l}TWWftoBNM}fAm*`T9f?8vRhz<^xz`3JCzAhm<>Jv1Q){UYrSjEY4}2%HMyCN5rJzt+eQ^EjxCMKTSQq@akxpt$7!Cc8$OvdgubAjt&0Rs^a|!~{QacLHth2OacfvDN?N^HSk@28jmk)~b}3(>`Vw_M(!JD=`BfZhE<x*kOSEK-}<}s5vjiP3Rd#>sv;xcXBOSXP0pSnn~Hz_L{g!Np%v}YLcHP`^B1Sz#!FT5ppX-#q@FX`~resJypO^M`qPvmh4s7Q6YnltPfd$pz!I5fhqa%J;rWZX{xl7_P*$4IB!*{?RiH3JXNA#kwUX=K%@Y!>iVU1(7oGxwr%WH$%;p24l@u=mz^R0rs?bV195&(k&=$<Y}~sM7bc{Jee=wxk4i6r7D%m5_xl24NwAu278iL7Pe7<(oi?ae(GC6~uBEGXIx6Qtr{74RvoMnqhec~bS8^T(x~!Q2G5W+AE4fQVIuP(R!CctVd@+4T5N3|fY3>VkQ>dCPukB*gD7dZ(;+6MMSDZdnc4<5(Gz(UtpvC@39}T*4sPC~WSWMhR-xoP8l8N@_`X$!uRcrvh3utwrb7+po=+(ff_OrbPr`y>Rqc&&G<sb~D1UadlwpRKbhrkY;6o>3;$Le_5NfX((ZR&oeM@>{>Wko9FMKHqNnDWOkZ5OZbHGI<=9b^nM)*Z^L8GL3$PRSO1{u2PO^sGe7-f6?9^&np=-g61qSoPfE$8~HI&kwC*)>RCS-L~8GAnGXa_hDZ#%rHN*%(JJxAFM_!xDwgJQ&AJ5B67*1Y5n6UFH0p-e`55hT3${v9iqZ}Lbp+chZt1jBnyEXMjx?)^;r@KnFPp)m61xSCJg}BNS}{#z&34|-sS(SUe0rExxT`n8HhZ^aV%=Vno0nG0fBps&$zPKweo{J`D%ycu=k8z_70mUptP?ZXy4tTIQHI#+9exhQ6(#-aUBzyZD&3T=;g>*gw)9aggHP#sGr0stb%*ebA}@$zeBIH<?RL2?{dq|u>F<ITxLoqkiimDC<AyQ1NCzw@=#*1ec@~|qF;^jFbZ0Vo*|bz<hwj<b|&XY5?hT4OOGAC3M{!UHmxcpmmFv%dtVNncVm05Vy93aAdxrj{@mUCkD^4b3Hm_HnG$}_|KatQU(O-x_aXigLSaWqY$AV23VA8*;Wz_cK0Tj!OOLNtuv@l77fnE~erbuvP@P0q<cM=anOd>a3$ARJCLUA<Z<UtP<tT{bR85_$bOy!j%0ajxLb9!mt73-oc%stTzT}-eP&4%mUe$+J9Sc+LT}K{<2?p|utW&bnoY^N@MWl{i+G-i@CGHeKBQ0}`M=@Rf3ZFjy>c$RrDKF;&_)l(Yi0~8Sy^vJXlDA(2Abk<=kr!{1MN693kb_u#Nel?OdD3K#{qz;2fV7i`SEnWK)Y0N6$ecW~?QDG3y#ltpY4M8J$Doy^9{0Y?%Fn<40``xk2sDUG=w@axfK+3fbtc+MHp}U8y~xGUBV0yzFP$$R0`LOayO<JNIOi&cAz<_*j++q{PY+&I`<L|@g23@m@K)>K*$fB$qu>3>bRDpZ``~1SPyY=WIDB|-FjrFBKri;a+fhO;dL#)X*45!(df7VDeUH*m*^S4NU^pZ1sfPm!B;`t$F7adCz*j_**?<SfrCB-Oz^)<&0}Kd5pr!z>p}>}h2m&TW2^iTi{RXBy44$JTIH^p(@L%xzkZr$4#a6NHBvE@X_Ah=VT?rBH!W!BKIW<+_I+<V!>?c<5Q1S0qt9s1HXC*%HHUw!xpc=Z81V*R|NTQXd?q#;}b_jA$vfmzuwN_c%QC=8^y}Y=ISF?TifMrIE63(mop_m8UkF9gXaYK>t+BS2QRlkYJAC&vUdv9>(_zWU_!{eJ&Cs{X0S2SmTv(znl;siJO^1!1ckd8~@ad^uy2w2A+>V7f(DEbN36SNmbS+UDP!&B4`${+`{MV@qiiMrMZkXSz5I<g@tpdT<XZWUG*y{)hy&rY6;$qDdgEQ+uDq2v@OLbVKZY`g4{3$n@1dBP>R)a!k9IC265gRF#1(xQ*A8%QR*kw<oGzzDcSHpSuxO2;vTqc&s|_J?l9cr^TS@7KJVr;;~3Y%^GJ#PAL>sG{Yh3HOZ2Mb_<Ts0chZx&35ttgHeLGxmF}$?{GbW2_6-(NCYHgzK2(bA&vCyKGYK_A7Z3Cgaj~FtO@>?&>(&OLY&G0hmFv4pHmo?lHDZ7jn=OQI7?P)ffn*U%I*fgu}UGW*5iIZPr=Z9UzCK+Ho>i$v_==)FrzwN*$~vg%3t{+)<dF3C%G#>ghsPie?>Q#%#zD{msr?Qa4+-v=NCGH@k8s$^cGQmjCjuad_a69X0l(=pqDsQ+DY_t#DYf<zvqbmU7cx-dfE__@ScK!bQhv|9e!#NJN?m4%Gr0RA;|N$jS}czx!Myg8%~6PpXBMxtMW_zZr$C^?eSZ07G>ULrJV=Y(io8hq+%(o#ATcMGWMmZmrVt1Av7|I;sCrvT-hd@{a76;jNof0>;P>#VYD10$F-3K_F*yvwgz1+#_X@1%~lyGfTyCxn~v6uHq)0+#`WQ_OfVjLFl6xMJPW_N5zD4sAe(gBiBO`O#_gD>8oRbc@<p~A63hy$&4vF=WsPR|Aki#TNEmkx*~15R2zouZIenmQ1RzMUFgTgxg^00r}iJ46(?n1IWzkb`5Yv~5UsW$QJU7q89Wt)^QTzSO+uZF@l8>6fHlY?jg!2FbQroN<&-w9{|vn!2yTjf$c5~EoEbL-?yE(CN5)n^D^^{@;`VCKbz%>b&1$so2#DA1BN@sZuq#7&BmwREiaJo$gF7j@g`ofl&bc6~ZjA-lsc&C&V5F6;>chIB1Jj4Vxr2nP801ta=^gK@dCWW2?w9JfV(w1Yaa)<qwYY)Wj@YetNc6EXan+u71MMpGvV3aZ*ViWxPwLxTgBNGmap?E^)$?X++av$UAmeQk<%Br`;y8$`;fI1W(k#LtP(bv7mmj1&;Sq|mfC+yXwo=tl&JZH8gsGqc;wW3MeMbc@V={(FLJ++wN2@jJ0j_gv3lLEM<}DK5DmFF?fh^P6+^@u%v&H=bb1U1dU~5r?HEm1Xj`o>`vL1{$BJ(|PU1hc3p~N59MEc8uSeT&5phL{*3uE1ZU1%|il4x_CBkw47T}Mo?ER*FPbi1oN7EWxo;<+2*ArdL$EzEW)2*A#}#3Yl16<yy!ldw`v!&k$@h-|o_^l<<_6JR2sQFkbOYB;&rRIftTLdcT0FCn8S+-~iXL>@8~7iM?G*ri2JVbCbdgntCyS%bsCp@dB-rWPUnY`H2WW;Q2Su?-Fc{0tLJ)@!&)kD>>TfHpYKiL39H%jhsxC}~iURIkeHfaLz7b8k@KnaC;ggEVzW#%OLy-5f;V{=*RgYAFa4(I?(b!mJ~yJm|swNA5z8x=^M%sLRLhUZ~V`YPHkv)MPiQYMZ$~1R5n&B=z)a@K~%Caw=a$>&OF3D#c2M<zLA{1uV~3sn-fa<3{F7lx{fllx6)w#ky(21!ridklkxQ9^3G4l9dm^0cOa~=T}&#HZ`_gLVZExk>YBU_<q_((XtBeDGC6yYDOfG;fvu*B$(DDvpaEh6`Kn+Mk;Jj)$gU2+3L(|gH}bO`Y2f+uwuH8%L{99XMF+m?jfcJL7V=w7QA51wB3>-GW33W*6nG7^I(YzbhH_%0AX|yI)sx&B{plMvzU!aJw_$cw6n)~26k@-TB*07v-T5eP@zPQBS!gvyPC)N5hMpH`n-W=g1Qxu3}D{3+iDCE<-6eZJVY&Tk+m-0*xpMqR4jP)$|%G!*t^%rCFsC&Lk@A}TKy)SoHBwh<vNEJ({Gxem~A@&NWK^R^Owj&U|Lg47>DoI$HR?KxQvCtvPe}&zQH=5HyPK~V~k!$^Z=dZQ8gbCE$Y1<h@fFdqf)*qq`g<1kEWPY1^^}EBE!yqFLCx2VSxzR=Z@p|X9f%;ZTRrjFz*Pv6*Sm=?jUG3g#x#Eorvs9R9!91r!XYYB7O|Gd)!Huo#!1^NWjPk7J)%8EQc#GK}0yKg2^!GYShFZ3E+6m*+ov{(_YIz=a*2ImV{HaqpJqnyBNf-PzwkGuF8Mv<gqHO2eW}i)QmAS%`XQKXOPl&3NIL)lpYb3FD;T5PONPtiM)5&OHTe%=nrM=*}Cj!D#{GCAu6|KdG@Bly{ol|-%7_lVOn`lzQ?o2;^lYL^75oDo_k&~pO0@(sxM++_|`MzA>LGC=iM+}&M#@Jrcr8wL5AY@?^@zUs|B`K><4ddRSjZd(kGUVc&%y|gkue%ydgJ8sHKag1P`q_G&=d0NWM4KX<5a(AI<wo?Q|@r$x(JsnB0`NNi9~*2b;qa$xhft#cunI=+p@i4thV(_>Itm$tT!0E5~3=t+15Yh~tP4M|aPRcg`RR-a+k0Y=Ea56BX$EZMYs};5bpZ#Zx%c6&BFrQmFKyzZVEKc+$4tbzi^=JX193i<A^`^tpYs0ZlFY9<P%d_~p+a9jhyzNuDx+!QD`jXq)(QK)mQ~s@23DQankRp_&Sm@N%j^AcIg31ho%xmAm423WWgp|B#R`nD$6JNK{wvs0{<I2xHuPQbCqV{Ula`0EoPkq`{chsSov2?iv>3+=+z~RbCC(<w?=oLqU!a3PNe)@(o?G@$LxQ*ill$ZBVEsXAzULABvGl^)%G#+<QxUHaHRH_Z+km+1l|QgZ0iVVp~<XCcI+nMH8Si?dFNT$yWE9MdtMgl{>zx2aeKxbrn+|n!KGa@^26QoHQ4u&&v{c#*3yk6_PeAM;_4jxJnhda~9|u`O`sXQ>0qYT~buEV5m~=#AP9+ClFKtjw>Yv4dp>j?mXGLgwg?<^foQmz=pyq6Dz^<EeKqvOz^~!R<}DKj2RctJ2qD1wnQjQtE>F-TLFJdOX59jRQ@BTTdd7Myd6IYx3&YNVxMw@F8aPqzly-bXa`G5Mqg2Hg^Db!qv$L{eV?I9CLs{M(44UfY{zWjAO3XIKicKX%i0f3>dE;0S=m&eFvl@7fg3s1EmJc^(+|~VH69W#(YQ7pw<~q&Z<cfS9TK@62yLq(JLU;<wk)<{4Vd^{mrxn0`n>cAe@c!~BM%K)r~89-kFdyOx-m9`V>c*uO+~-T<zTq{FWy(?+t!k@FGk0QF%LE{Lz-M^vpQowzeJ#mB79`ZzKO}7g{NHfbv~N%LHIL5^5xjTW$#RxhAhF1dd-kLS8;Lbi-7*Z+nj)?YMCKl6z2el$M{#6mBva!H|YNEG+a(S*Fgvcw~gcWlJDQ@Q}Sr|HA+P-5U?58kCaME#q)X_f$kA}4Hd?|92=G16b$e}61;Rhv9^5pY0?VD#Tc0O5>qYNRcQinf|irL{(tKdPW@pGU$MLPc}pIo(56m<6@~WX2l?T7S)1idtoQ8XHc-urJ|4Pt`*e@<ls+3;r!NAeQ+>yCbn@jdlrmm>SMcn#swX%*X?Gx4kUk7%(bnAyjnI_0z!q60WV-Bv!&5Y_Q5sf9g~AP7W!E)m^!0oH=gS}Dcsc)qByVu1LA9$O)G&S5_A`pScS*;5cC}OlrJ235iESITS6Z&NrU?Zv+3D<a460+wnH;TcxT`V`WqCd9fP7zB8$u9N^=vYG))EX>p9{ASAI^3DA(0AZ2`&$wi5W&q`Q~Ex<0_6QGePZRP@%%RZ`H76;u1HOJ@_r%d3*%t5K_Sw0@fld6D$hwPwJSW?x_P>)IL8Ei*23&WP;60xam7lpALOuEo_<~V#j>Q@A_E4dB7gsIW#-v5cDkw^oK+cy;;&>!k0R@S}wK00rF!Qt&{`n-INTrF0fZ3&ZvP<TIVLdMWP5Fl~)dw5_0F$%doV72i-=@f%7rI?sauzgfplIo859k!~F7e@w%_CC?jMzsG00L24t^9kM^=Y4jI=#GM}5hagKiiXj~fl9oT*0?1WmB96nuPGTa0-ey@YO-$&1Cr!BM>k2Uv*mRe_!w7yRE3iDCwGm1p^YC5kKN3O~~;64@C+DC2*`VK;%wxsj7`+^75AX(^R>`RvS$&HM7uf8b6DC0x`#Mt@4U1@9?G}f||3tK7G->ZvL&;REQYs`en*-i&fVU1q-xXqEsz>SJZaMS-to~+TR&arRV#mf4~31yfA9G_=^HnP-BPohec6-@dmKrJ`{AOaT~SB2tK4F@mvqmL)u48+xIFGswM6|rAu0o4CN45>#&4CH-Hy6QjdURz#|f9TPd0QOQMf|f+kgD|-64@^J=+XH60ci|^SIyyOc%}IiE?Sz@=Q^WyV5o=(LSfFEV-P>!)+MD|2*FyoNh8hq8*SenP<sl+K;e?UCB83s~1PCrl@)i0lKsJ^pdp%)6Q<ZiRGDp4n1#xPqZ8rVLZ?bFy6w^OxqAfEdLU;;(i=@v1wrIl#j&LKLch1^7B~@G}U`GcBfuBI2SrbP1OS~Z0vE@_p36sMfb+OR03S2Mi<ok29f|zwTtBkANz|HRl2?<d&f-3mpdNZ}ntvkUtRg$V;uW`GjNXyhl2;l;Nfq3XKQ;Qe5p?{nuZ-*j=)K|1q(CagF@qo$3sEO61j-M0|qFSz597*^vk<g<Fb{G;>f^F|obe!#=qA8vha?g%e<^>`*c;HiivQ8wTg5KaboZmYub!pC$YH6dYO}yA*Ftkwj6geNACQA1A;B-Pp$^+qpv}-W`Nta)G#G^Ert@(6A#?roBhQ93<Ks#X8EkO|vO=*RgwMHLSo?hE#H`(#?6o~S@h`84pBrwgnQoOXunM1Lm7$bReC(3QA+D7=rtf}8Q6fJuMuDb1dKNTpc|I#GT1<08DW}!Iq)$P5YE?TD<cL{h|ObO(X?=gydZu$b23hF`^m#pBokMylITzeEGlFS820y6sR@0JG(>o0IksI1q22y<Ca9Fxh!cl{+1h!*TYK;o)LE*85hzb25sUFeNb!*1PR(f$;SovR0_*my<OM|uHzPGYB64x6ABK)r|Ushc3&Yc1e*(AyarwBa`YX?DkPVp33);S!z1vn}dnW0Wa(rs|33k{=KEwKnd&bV_mLPHUjqbA=SLd#i|}2uuvHoy_}9<3@EbSN{4&Stw@(<h4xj9vK--x;4?}PhU3h2@uA7@y1$#p+Zrmn(i>1bSKfv=h}1ja!bm(o~WNbecI5@?={tFbtKC(Yq6OA8h1G=mjB3}ah=6JB}Q96#Al0?zuVmWDezo3ikNM8;ypDdfaSQ`PPFk<tToW;qrwJwMs2K9sOWXhQHRY}dma!|aVemI$IzURFL;dqU;p~`A3y)^-@csh7|%{#s-4zbjLcJ5G0p-mn``;bs=QNmfADndz6H@(7xODhdj@RbV5EPcm^J|zVXOZ(_v+%k=JaL?q9M|<)W~3(wbRICmvrWUnT^-&eV%d);E1-&QZ}~{<}UEC=h5;&F=NdeFW<D--xb;sXM(KTC9RkzBar~NNG7_@3Zl{{e4|7f$FyL4_wxLd6-Q}11V+6B?Ra17-h4h3zt%FDT1CEXnG!W5U7YcAFs_5)#(00|(o@oIadMb3`J?bP$9Sx?1&U<1<oGd$Uuu;)@MaTD0H`iu2OqcV;>sn^s@(kQTixe4#SJ@qFF1fGERcwAPlr<KRz$NoF4!*WD%knMg4M`<F6*m&>z6ryCD>u$Db35iZR^?jiQ9VI?NWW{)RyZHi$82;CEk(WCgbI$BRagiJg16pm!Z7FnMG2e{&4+e_)+$@Tr~4mRIN}xR+Dj2S-x{ntlRk<NrImlK2INxPo1o0)7KzGbtH4HG4*jh>(5*Iy2LyBbE~;JMV_b{mnDM7EzM6}3Y}IX7}7RzHsIAJMo|!yX<G*xLv)HT8Ivc#wJe7w@EIKCpGdZ2(>`<sjM4{8`B7Eo=C$!`q0v$nd{HbOYJX|I(Da+NmeU<qfFg+2a|6@k3sDCxc2LUWIq;_|c`h>NUM^$HB)~^%!LJ>VmVJOBt6}GI$v$N1hFG4&luQ=3viT!bjQRsuUe`qh3@~Ny>jU3AMHG<+8s`D{TsWM!AcVN*a9$srMVJSW!aSCU>X9Zy*<6Tj2R0Y9Yg?jut2Hx$Ctq$))IYxb_R}9<$}iuZsxQwATe;VNeEBC%vYaCL87Eu*W643HWSf>xk;WaEO<95&PxtDdjrm?r<G;a#Gvf$tbMJxL|0#1X*xU6!kXP`!Zgj<*M4j*Y4aW6MpaVW}d%cwXUI0iTs_-gH{kr+CSP+t@{EwRJW%2awkC6g_61=_Dd@3K<qUQvqTm1`TFgtJK2b@T=_tCrS)j6s^FmSi|!HixZr=>=J>!9uHr{CXy{bXOvYKhTZ-sZ8wcNcUMy!@lSQ0Z;ff7|0oH0!5-{`%Wb-)8a4=|+U@`p>`r{q^;~y{4@zAMLM?YEDGJUi<djj6`wy#kZj}SRDPXH~QDtU-{!-iqb{I!B(FlAMkS2ub;15NKfFXc=9@v-@i!Ikvk#5I+{l?n#TmPWy4s%Q+uCvyW!l~a6SUdYF)oNKHv+9`R&u1f1#rDo1fsmyA8o60E1(kp{_Zkju#aL9hon{2&fT1*^}9Ly!j&}Qu5wQ+!n0YV6+Ec<C4DQ`b(%142KJ#)MtNbF22=V3bwjwV55U-$;$C6|K6S+P2LIbh^*6m45pbaj$W$x{M)-&dDi#5p@**fV#2rHapDakG?{O`D>FhlnAp}A<3lEtyin5%HkeS*ZlvGrZWGE{dj`pnlh*7ka1u16Bx;k=r-@3KkPl|uP@=f%>xdBSWUA!Rzzlwl;fr$s?pq=+ecxxMx@gf`E;+$Z7ru70%bzr{r}8&y&F9*4)Of)Dd&*4C&K24$y~8kj@uJyySLM^4N4svGo{f=~9d;h^re5v#_TTs^`;0}>g8n0ilHT@zfttPr<NZ#OWemca2tcx&-%wPJ6}H&-$x9!hY3%dlx*!wWmOqEn>**UzXLCXkIyo}Y$!M+R8dxiav$-{7q=TK%6<LSPT-uDxGIEo$lP_z!0d*{X0Q)^KeG9!AYmB^cd85{r2P>G0L<=8qt;h8oUzK(E(Kc8n^bEFSH-ZlYXusB?TNYT%amql1Y>)4RNCctDaR;r{5#4_lmJsg|+Ed_IJ_MD8^t-}yZLja)CL9|$ujDltmUBbhap7Y*1pOxx;S`G|>OmbyW4GC{PLmj|CB)^CkY%=Bz+{rCo*lPlKl;bTCFt3#B@={<e1Ymq(EDtN8jb>?qyJTwrex6?M-kEXz|wOhPSMfc$t>1cH}0?cb%O|kMPbz%y>M6L=iBcFv<^2#u8r3|h}w)VnuKv3;U^C39)AGhv^BO1<E;-4vqsSs^9j*<$%n)#W*?k{i6w7_NvMJ30CZvs`xDH`>%-hVI)DvNZG7;70d0*$xH8?e1(!%;OiD2%`RFA~_c$g17(iADc#yk&*ALZFkxR*v$E_l>s%eVLs7~K7Liz%n$0@$D&vOT!qwv8~5SX%l+=kgF-_w!)!xZ3g4rg&7bX%Q#`t|oCr4%~?)2|1*2a$Sm^U2_I5cQ@NS&d>FqF)W4hj+<tg$y^9?oN>{Yj|XIjHjWtJ~t%T8u3-t)nKqpAi+wD6NwkubdC1@&E>st3^4G#K(cZ2U_v)cPd?*`Rk-u!>AhIKj(F8*x{sW{S6W?lZ(8p-iBa4qa=*%|w+fqqG04)hbZ-~IENo%W_7Jh`R;Yi*RmqD<bsK_{1CCwuJlhC-qoTIg&R7J_K2-6|H3IBx2g19WOXzFr^lE&aDWYmalN+qH#}*R#p+>Xo?`OnY*7Vn%Nj%Yk_{w`IWlK$b>q$1GotKipPf`e8nVD##&pzk5_WFK3I(}CDz*w5l$O)B<N~&r@JBM8seE1BdN&(6}AZ#F1kdUtLM2?ls4n|osbkNicGV#N{*Va2e&;U|B?aA$ZIJoR4)QhyJuJq)++kdL_7&M)iF;K%4dOW6G=j;Asny}P?g4+RkM~W~-8f?@rZUwm&x5Vy%ZyPWdgQq)C9e(JYQWdW@6}X$)f8MI2kO<P|wfL*Pp0jO3j-d$3EZ_ab#06)2r$g&49o-{Ith44#F)|L>iZ`)jmav)L@=EE?OXtsX_423xE=}u<$$r~(xp?o679GFWyAwji5!ac3#yc?&28m(oGxwQWtsR2Cmb1GS7v4##mz{<V%%xc1q|5&PwS}sUWYT6vugH!`2-VrioW|{NtV(>R)nE8_6!J|;#Cn>3)yT5XhFOwzH?1VQLxE|IReGXR?K$`|xn3?5Y8(Y@PO1Ue`6PHxv093qot7GxhuDQ+Zy24MKJ-mRNhukspQnj80C#tx+F0raPlJDFj_8iM>kO;<M)3gUK18ZAo)JWoxrdz(RKk||HwLA^`*8q?M!>ubY3e=OY|QplmH@%<x7B`wyp?)GnPN8gGn-WI@o2I767x>5Yr%YP(okSv7%~^5H*t^^17Suld$Np`qE`@SQP#?s*VgJRK76>n60CKB?m=pa%v`>SD}s-xcSkUMB($@rokrbI^lT2u%}dGRCyWu7Un0t%TgJ8)H$D(~p*xL&Nr_p)O0vzggZ##1_q%AZ&55nWN!J?Kyv8;eqJd-wyS?<+z-adB(OQ!&DH?T~9ibqB1_Wj=*?q8VX$&o^zWg3xEe;!IT`gL+VnioyqKjp@=YYx+Dn_Xobt1I2Nl*<p_PuH&QzuIWAv2g1upZ?Z%QBIb!1HY`Ihjqbhl)iEy!|ymNqy2LScQQ2D($iina|PAwp`;NsA<$5s${aWRtbHC-+!YMa}`Zw+(g{5jM5D1u6ZKXS1vq!{Btsmyzh$XG?WL*vQ#9vUVZ@k1KYOMRi<5l9W#S2Ib?6Odi~bKezi$hEx;#VP;Q}0cbPzdZ9<&jv8=rucLAY=(b`7K{qm?GoZ7%7TjB4x98lbvefX{v+CVT+Q)AoSoRYrve{f`Vl5<dzGW%-T%oxalZLoDA*wawmD%NZF0)c?&`rqE+gR;am9ZTp{z}96|8d3tw>$Gmq86`F6n&7CEsKP<v>FJE7xZ-p{V|Ak6Oh-K?9w4&&*eA)61v-^Fsa~qJCU!%lrb!tKJidLzvq4B<GFH5%IOgZm5;y2V5Ud8*b0%DJcikN@nbR6M1wi4{HiS(xgWxC?EI}y8b>ap*Sq0w7Gi+Xt>b8jGt~Njs=o@Ov50b0*f09=&m=)!$%)o}t<~yVk%L%CR_}F0i%4$C&Hyc_Z2|x#lFu*dJ%RnF!jhYPImsQQ$F{4M*{v@BIt||`K#RH9R*RhaXI$k4JS90d-)^gMtc6W2Qi>0YSS9#vwdH>->XhQ5IKd=qNZ+l^-`OB9tzrV`nxnuAYVZD+jw2uREekh&@97w;<6M?hGZ_Z`xMRx$COSUbkEJzI#y&c?D%<8ZF{*d)X(xf}@_QgjzE)eR9NLQzr)fh0s3<47LQw{jWDrwdbIerhy2@HL6v>?J!;Yx1>GKBTj*_7`IVZWH1a`OjxV?FS5`LQ)3zkYJlKUW4!CkXuk{Se5ivYH7l&V~;S4gb+U(ux1@?V!OH<xlRN^E}yO&wlUpPy<k{!a=vArZs&gEwG-S*;0O-u<@Gc;4Ns84`nm`D?RP<H1b&&G_zwu&!b2@IQQN<PXG30tuZ8H_$oqno<HMee>5{wE+euUI$x(f9sGTIkR(QPHdF8GX7P&FWcF5tYE{ojfaI#OK)JTShK)xW!cV%H(s>i@!D4et?+@@SUz0ZKf}_S^06|etz|xPmp}vfpCVJ}N`>Dr_iy=n`RHCUh=-bTg&|d&@jatlWT6e3IZ^7NVIpS6oce@!5R~Ci!YE=K{>W3ZPgJW78a075H^ru)m#Bw-xe#lxzC2&+ucoD8O9izuhND*uJLI@tKGLWO{7~@*K5Yrh=l4OTO$Av1mp85s{##Nt+rww`tjBa_}s9|WZ9b3AG?l|k&B2oK2B|j2M!26{pkH?kL(%ynWwh(M5n&nhx838ZRXE932?`ov=kgW>5w<!=`F?_s>qvdJTb#p%yN#y;>jXYqDPvpmlOPMY*<}&7^os_I23(A42)ZG?ESCFKkbiJo->qARlb@uRGhk~GOST%eFeIC0Ud2X56rx?3EUp0k6^zBuO5H=LQTD0+c^2yGc^_e~AuN+eOEG(MGH%C3vQSQ~8kjZ`uisGDb<!=~L!U}dspuJ3cz<9~l-2MA%Fo^Y3QR?v_#{44t6yEHp-@c|uE3wt>o;eWcqGay?c&DUT)<@-@as(%7)`ZXM)-iKpCAyXQWbx<B24If}^z!G-EUM-ZRM)zHhL4q`V2gqJS0qP)?jqWtSz+wRt;fKCT=e+|u!|tILx@-iLJs=Hq|uHSi<rhb)f!F=(!hSLks;=B&}QCb8Y)Ra5rsi<$^T7ujWlJKYd1lX33#mtR0oQQtK#kiDi~HvDs{2d|K#&h;d%y%2JP0Wl$X;!J|gy_l94O%Ss!kCxtQ2tfUQ>C@R}%Rw=y=MTZ+}Uj9TyHTC~nC;{r63vZ<pu(H2oF(RT6V=gEGtrW!CvwONGRN`6II2jKJ7Lj;U$Wc$rTZtVB!soqa}mg4mW>YSd=TCRGLkKHyURaqu&b=j>w4D{ZSN;qMZBvBmGi>dV$MnM3q&k;S_UUIAuWac9S!Fk!`;qQpP7C$gGU^*K_hPNH}ZX|>WL1EvV@#&*dMPR{KE6x4Bz_<{sOq+#5-i{NHBUslAlZ{yq{voc5tJXLw%|NH$NQS4<HY_{C9Qm$%JPcY{V*+C5i8EI6kgDk#vNJ286zWq@0Z&TB5#*PnrR8M{oKx7DEwAk&-Y8J6$=;R2P*<EjRCZ}1CzJ_RZJ>qw$jSk_nW*ovt5Hm-MBf)V#gT~}=UODz>s6I~z6)rjpfj?L$LQ6wsb;pl2B+KE6Y(}@&gBzCTZLD8%r;5Cdl0y$lR}SOxmX=98yt^SwIl0fq(@BzT(E)@@^Bd8Xj)@7&dJ3qd=1~UM*0|AjCFeQ$^@SokyElopa0ZLC+@ZEotAo9+wmp#J$HqT70fL@X2&-1{Lq?YUBygP7^X&~CIWvS_6Wla^E0QaA6zpinEAn#$R3^wln_ObOBPLQ8Ao|pqAelX%UP*7$#m+u^3GpIw^4<M7*yjV3xSJBAF+b<SrQ1D1jvY$5k#uK3;@?i&yF$*H|?w5rTnbE%yXUC6LZb&&W~e(3f3UP^j$%HU>M87?vR>!fHABy>pXQLm%YOb3h3#p2ikXcD89V6p?1keSyajDWL%SkX4_Nk;~*9xHE#f64p5NZPC(Iu$1-w;lO?}Hue0Ut1=A;V%g(TUsm)wwN)3>~5>p!kcp(GziT>)_-LO?IuzlfdF`{3M@-PZoivAy$2gLtm4-Pkj`6(fGrtr@WUj>#xOCkJ6WXYX{3~sWDi|2AV0^b)%=YrXuw8T}&f=uKcygxHH|06H8<6$6(LQ^{L`9Hk=^2?qUb_08{dJA$f9o9`-wJa9R-#AxZK0Tj!OKq>$r&~5W_r@k%+R2fIp(=>3gb`<cGA&}K(>pX-s=*Z@!IEW0i|cX}z`(ust-ZEJ02IYb%(`UXr)v^j^)N7oGBd&>f_Cyi&9pIiogZF)EO2>uUKBAQLkR<MMb-z|Daz~<zapAPFI=?@02A+tpiQ=JG8$BYukgv?uWsy6m-2Ehs72_c-N8?p_rg|9bK`yufP_W>N+`l~Vsgh|(;^dt*T%r2n`cjE-A{2rn&{c^kw#H6Qb)3ppm*{Rw=;I8(Rf}O85Zh$-JE)ua?;CEZv<aw<>z020b9(H1R8`cbiXs~K+3VrS`%$4o8|Pl#_!^E>Z~(As@}eQ2tX!e?_$b^;Y6(%yMO_fIDbX}K0S#QVL%pj2yDlr#apq1XES2-?*jKH({{jS1b~wjKK(cF;PBzi!CXph11H(})73vpjao>zUcm~Vo9g^auUlu@?@{h5yYX0_3}@s$J8^J>=(@BTls&{nbeRpfa$Jg)a}w-IV=%ygR0Qe{;MNIjc!&UC+HAn&8JMsz7<S2U{Nvo0!*&>kfaB`=Gb%=lZ6Ar+fv<Co8E3w(u-ygiBlOJE9mOOjyaM}&)jRwcj=pCA4Mz?VF@b96+7cL{Dk+KPn!1(QI@=+FJ;`o*9J5-5Zbw&P7}N4{CtkbuQ3IA4NwLo*<%h8it~g34?p@nvt`g}t;q`-fgz~%4!`as|(f!9=bH(kdVt=z#9C?c9Y+&FC6yp+f98PjvP_JVT^|_eN6a5713Hp-v+w<HueJ&SW((B2P0kr&|bQ*{{(g*-pKHWNeVR^qFFfmvamJ_}GuRxL~&&8Ahc%v0X%KZ><iszuJ1UiykX2=DAWM{bKiM#|VZsfcLMpg+eqy-6IH_%0Pqk-(!ToLewY_h};lz3x6L~XVxJPzGx@o4zk-me)lPlX!tu+0d;5v@DOfQgoYCcH8x>sYs=p%C!cB<YjEvFZmr%-HX>X2?5ffw2x(N9TN&+^u7k&k;Zf?y^bY+Ap}xu%eo2I(?vBxkY=P?x7$6b79u~Y2DmCSeEHG4*DJHu>dg^13C07Ecc&qICso!-Ixi@Iw!jWG>=r{O$IANsVL062qf>F)WKR(_+Vtm9fil4LL76Ao-TAHMb=SY%w`+WyX?#*b)9uf5|OxYvnywU3(U!$VpnvTkfU^uLAMbCzA3wOqn0WxdGWEg1xvYUpKh%}Bur0HBjMuUw6{GfJ|r@H1czz?4XTG<BV^^;?B9JZl0g80>ig7!#9VZ^#ovsA)cQV$P=KK*h@m7_>ouXU`@`H<rp|CR-6BSBQeRf-^Z~%a<c8G$C`mJyKY2&(%kb81CIPYIhhi0V6M-zf>MbA#a<dV_x5gtSkOhYEX)~F`a-(Op%dU1N9oHiQ342*IxF9S~j3ShurlVpaI8<zy^oZ*r3Hm=IO8UxIU|vQ4!$(!6X)<F9$~hbhPGsRV!WM-JWvoaGZdmxFieG-F!wQ}}s0)45I0qzn;nb#Mvznyr8E2+kBA<gq7NWy8<TKMsID@BxaQ+m_wMnRx5wj_(4zLD!q;YcAkk~@Eq@2>Gt)HRy12Ijp54i%pk2B-;zI}Bj@W|NeXT_>(SlnLiIlt^M*{nv}jevOFc8{cc$84K0BeR-1Hhpwz;tyKlpuq+pTIZs!y6Y8ysjp#X`v9J82dQD*h=KV;;2=V(RSbiIkJ&!do$As{rCBj`r)!<94CPweK+Qqy(mQC$0(N9)N~%2%2YOT3fXk=y5OM$HZSujZHSB!!`}FF0GjrQ=0WO1`w@HB$CJl)6Akv5*irPqL2!l}p;Rs%jkXnSthK>3_bXcMms2bZD8Y7kp6_h(1rSG+0sNiQzvk>V8qF3bzvqsHGb#85K0cyOwMXy^0%VuSer9P)ulW09vIrKcpVAyZKBEuAn6i-+Wwp8k9pJ^!M!3ZWYF9f$(RwEwD{DHltzbpum3EB)=!kk7hqlW|IpPfF29ZivLI#2UaY{QPxV0j|TP3gAVb@ZLsfyJ{g#6u+d##<=yvf-Z{fQbtx2|sR@JIs?3p~F|h*of@Fp&oL8S`$Pg;9qy}eQGhe*i^4VwnAu?w=W^%Hr#IQl71dC*%s!3#b~KZy@aej<$05U+YJG5n<fx5kdTD7T!Ru?oAa>Pb_R-lhV3P5F5ILp(ZfkV9-L>&)q2atA)ZURdmr?%NJdyCfWRJrB6V*t<(aA}vxGENMSRegXRRJiaR1>r0d*CG>FE=1I$`dSR1fsv{v$V)N6jiz;nU?~cP~^bG_~^ScWSbm1h&oR9|HLms)~AgHRvu@&o~t$qUGj+E0rQI!z!^Ps{%6Us}yL3fp8<*B?>y6pvsbd-k^AU;2%+MuRdEl@$6m<^4JD>lVp8}889PuKJUU+wW-MM67UNikd#oPy!q2MhL=^ZPq6@)TQeSl*}J|dxM)~IP`63Ocj7WDJ-KQ;_$kz3qqlw+w@i0u4j#1p8Wm#6(t@SgeY|5>b3N-wpw}6(Qt)kdowSs-@pem!NZI=tUw0hnz}u5E=m<Mfd&1~nObZEN3!lZQRGKs@H>W*C&e6oK+(1nA7RJ^tMGdT!2!ROZPF-BUv(4ig34Vnm99<YLvl9sl2j(5at#T33%8M|Hq}eVq?ByHVdntx~2Cs)1r9Fn5_aeIFB6!w(q4X74j7*1{f-mJdhZe_hn%bBRLjlUZ7ozl+yhLDp^H2`A!}seT;$|vbK*OMOq<SaIi))1-ecoh~TaPz-P0@pOmYUUsMl{X$3MGOV9*s(QwvdKnac-LOQW@5i$ej$e2)taJR>M06XfA{@l>vY+f_YAC@(^&pjV4bhPMcSn$aX{3*utm^BLJ-y$k+ytJIS>3G{cGj7+Jw0Jm{1C2;%v>fs^C}B;iaArU{{IUK86TfC@Ip7CDGddu@@NvqG(265`g5P8@81V@SM~T*3W+l_6B8lc?iXsON@~Yanl;R*j)=es_SNgOuD;48myi^k}Jkv60+ya=A%LdvE8L+!q{A813S^5oU7D4B8<gypdV!{stv}ryqBgY1Kz}RUr}$I8WM3x+gF5r~md``m**_cs&yz;%6oH*$toO{7SY8ETv8wWGH?!v8A+xAb}lr3B0*gfru$vpIC0<waL9b;bWn7yn#7LHKvQD1lz4SB04RaNJ}^sjj8eQhq8-O3m%Kla+IALCIjYeQi}uh!Db3Y8W^_!vD>;Mx`YC7gWeA`S|gNW@(H$A%P|;Jt8!&F0Xa&@(cLrSvNITicW?Xg8DIm)BnLWw8?FZ#CQjsb@e~e4js@ztR84*8?*&3YHmcgDj!ILMXYwk2-ICd*7`4*=Y@~f}Y9sV0pWM<fdekgItGj|}v@%6RFM}C{meJ<&6^(fH-W1%4d$o9KF~dt0aN*F)4jM>gA|Hg+AP9$$S>4s$Qvl_m)(#E{uY(Dyw1Y$?`;IjcRr9*{!a4>#MI=j%->la-$vebX<RvJL(zHr{L?iB?m&2TxBFHkYhBfr0@Q&^}LwTKs)szh{-_Rxf?@qssjWRX92Ss6WXfZMWp%k0cjzbOHy+x*H0;HHSD@f7rkg}EYJr?bqSunRsgIL{!t{2VU&XlVsVlG>~e-^3U;~EsW-x(Rv4nRuv*42xBXn+E~$iF@GbJ8=FJ}*NI7&n`iY{(_M9C<(;<dR(E&RM{H<WCh`Wwfsy6Agdv8Ka^HPouM8Y3;<YAvG`%l>tVs#{ud?%8`D`$(>?b;89wDJJIJ-_j*Gun8~`}HzNpWW*lmaS2!}LTUNaU@#Jpj``G*mg@bjETz)Iyq*3VB6jr>)Il-t+&v8gp@6g8(z&=u1gj5jflpCheH*5NbDACW2ZA*-@qh1P?ukgH1^-h1EoJyr31q`9$)4{BRHY@kkh3YEps^%sBhbAj#?GCyXf=e6Sd5N@_`;nq}&00-oS|QADy(H%E8kgwfMlO<+H)~X{vA&ZeH*8VuXT&!}a5<ke)K^0?eqkm=PihoETx*mLFFSdS>^bOHr)M!5_$=-+d4P=l;dn)EG73U2(3k(kJJDPS)<S<<y)Q-^jWIJe(nLCkm3RPqmbZoR62VD|JCg}Cd&_wO8Qt7sA4;PkoFtiXV?^+sebf+8m=iOZi^C@U9ay2&lp@|u21Ihp4Eb_K2SDb=zrwsyIMm9T>^t?HQ_mj}!q07gehflAB@cpMnp8dmQJ(=`NlB|z(y(`h=pMn>v|;?!vF|KOU~w!KN!S3fHsZ+^3Is&O0n-(ho2a<G_4gY}m_)^U`EJ(#Z(YKwKd>};eIq|_$-NXF)(PpNw1NB}KU}`3M@{fy`5J2xJh^>t^D-E1sNEY$$cEObz5qpB>A_6}#PWlLl8$?q`0Ti=R{%Sz%@fcrvA!Br4-OqP%3&lkePG}faAMhBMW6|3BOt8~4~0^w0>jtO|DP{^kYnWh3zD|N9VXT8fw+bBPMv2F8S#?g`s^y!2$nc|1ru97>Xx-!JxyN^UV_Qa39llTinblBWmd4}@%3nRQ{Oc!ZbR^as#8to&$_R{s+92WwuifG=FtyGFpqM1?o2FCT5|oz;Q8Wwp?5Sdjp1#&YL-*ROsnktuCJ712d}|trJ^hZ$wjy*SSH|~)Okj2bO#KveST72>$ZGmsL@?I3BCs{?9k`v!mkTLeYqaegZqFzP;_Ya)FEgY5kL}&J$l!ygUcoBCWt;v?IeMOA4a+57=1S-J0N+$cZ+!F2Eum4cRq*eq)ZJyWv~1&rSi{TL=51?Jef9N4~(@z<v<r%J_5F=G2`-j^^XF~c)dJlyp7m<%!nrrR42R30UM4^yG-{E8NEUh&zntkj=2IL--0h0+STrlS~?v*RiSF!1W$g8$&5q9`<f1$&I-<q<tnO{B$MEswWFm30<x``S=ZLY=W(a0u84OPeFC?;bE$4wNk{kb=(`Ew<N{mVZY&=CgUn`0HOl7ToU?w))Ez{HN%?sKoayEQ+wwM_CvDg)ZN!FO_4n!uUi;CrJ@$FSA~ex{c0_>Z0nd?<fuR!H5RMJJ)F|D~;Nm&m>BsHJzHD!1LIpNGyP`a|@96Uk)JN{o>3LR}$<#Gq2NYj0DL|eeHoTEAu#Jxur!G%-^ij2&A-N_3=<e_kGxqC#X!mc2t97;X6;Vz18-3cFD%V1IN{iCco_b)MIZ5e!NU^jXAT-9oIysorNdk@SM43%z(U?~}BUtek2wz*p&&;=|4X{Wr5$*s2jFEmQ<D^AmFknFITOrb);;C3qZpesEV@s^ssetgC1*gxYEV<Ck{m|`dBH%M5NKko<YwmRCAy2f~1V@CC=00cp%|!o^i7WwwK$un2Eat^5sq`uHgvpMN`eDofHGBKaTb&iZ)%vxCNcy;%2suHc0dW_Y((oEfpBr`}e-FE1lO+|q0Dd0U$~5#v=91WrCm0wtZtcVa`)rXtMZWuL<e*Y;)mY5}qDU^1_yf=h3UnYT@PSHo&e~P622Vh^HOVWpJkfIs)F{|oaQMgs0me}e@6+^?U-jR)F`7YSLd{6zuyXnq+24ax#3buIS3RSx4SD%b1Hm=X^9x+7k5JATWSx&w_Rqepe!i6$$hu+jD3fz9t8W#iDSH16=lIOt!PQ;7Df~arfRDt8iTlbyGSHlN#C5hP4w9RsF{(9p-P|S@Ze(T5!TX&o&=Mv-NcpEi3iV%_M6@LTyBc)V1k%>RN=&#Idt)Ds#>nFtMMF32{G~L!knSZb`0XQo&k)z;1t~jo*QS8`{rbCQCBu0CuDh1?`VV2c>4|VM{rj%VBLbs>JqXxJ^~l8{dga%IDakG@zo=ohZm?*7@@wtgZ&hr(BH1I25Iu`DLr~oZ9)KPX+fz58yT{w-*4Nu90<?`a|7mu|asEtDjNnqB#Ck63C}YeXcc$uzXAok$ZiR#M(kW+;8^(baN&@Cdg%W{y0rHJ`zv+@s9n6*Cy;0H0SpkN|rhbo%n<Q<hXbYzA9r*;(ZC{|V7CES*Q>p4YTpHb#^YXbo#LLSq{pWh3e){xjLzBGMv8J_(EHkhrf#TDr+BdNLNA`^CEcPjJ5c?qpVx&;q=H^d<zr1ezJba=+)XFoezK288F+ZP*wMJQeRM>9LD0OuTP5Tpi)L{?Vo{z%RQVM9$GXuBM6nKpPU;p~`A3y)^-@csh7$yn6z7?ZejLef)qBZaUR}2F#hIg`F?M~27$L?DYjdd}<VqRy!77j-G7mDczfSI)VZ*vne-r7xXrXU)s%T*Ph&B|!x6--)9z|6+$_C8O!1#m>$PbqKM2y+*B*z;(4pqR1djhAm)?C%Qgh%-SJ`I3&rlaWY(TSTmgplB-X&NoVwaZC%wcQ4ORStXUy@G<HgXvgz&X7GF{eywFPwTgTnHKjG!ABp*MFwTQvGkJgL(o@3cKfV6`hue=6JPKcPjPXf3a!7Vdjvr(ArB<l}Z#K~cfa(%<@Nv5?u3T8GYR9j>)qM{8=>4z-2M~n?67lWnP)gluTQ<i9+eKXkJAYWP8o3o`eU)znkn>l99R{A#yzFaFe^>tB_QY*H?slm@bdtyQhs7T@vl8#fZ;$@+(h(hAUY=9kwaZZ6;mo2UP=C1oGW;leTP~P5hXQ~U%ExLl2xf(6@6wAr(&au=fu24bpE_Ahj;}$8>d4PrW9mY7dfw7UbkqLrU^%gCJVl<U)RiSp$GzH5UJ9L7BN);qC7Wph$BQxCLIIIywjesiu8heO;98bL6Zi~{@=qk&v1uQ=0!HZrrr4({bMxAGw$NxP3%)2854FEEUugQxTFdE<3n94<uQxC~x)47bL5m%f@^}vX=}N#VYhwfp!EVookJN%+J0LCl07I7N<K>cl$kGk5Jc&__ENo@-N2(b02e7=Ziwf9hYTDHSwmO^2nrqU~+W>qn9L`%1LfmsWuMh4%<z>A*mIviZxn*|fT!_{PHW#${SfY8WH8X)HUv5v-Kfe6-(;r{TFW;W3FV73c|LZ@#{1YcxP7(Z!lZmV(O15eF6v?`Q*_0)i@pP~L*_iM3H2xb*IJ0Ari~Hn(+W#qYFWB4lK9E=Nx^8sEoJ5`P`VGeQY=H@A;`Vwe`@H~=LR4u|mil$`U9ljf!}uRH*URGR+aIGQe<cZfD<xDuutm=aO1JtK2D3VE;|H8bv-i<k+|@a%KQM5&`5}$#j!^*n_0#VUUq9JbM_OWZm$!MW@ZAO71TX)nFI0M)_22dw<E4Ln%uoOP^|znCP2!i+jkeeIpMU@R>+64eO<Pw!+Fu{loQQzE_U*SBiQ@8$Z$oLYIQm_0^sleK^2fgvrHhDDtv*FQ;N_@aKVP?yp1@J@<n=SZf03voqY?=o%_A7iV*=T-VXWV&z0bPcaPDk4AAx1Hu3sG=@P)+u_G!((PyzSNPjKJehF}wb!7<KI*BnyEi$quNHNB&ir*!vZHXd*O2#J)u_Y$`S>opkd!Iw^?FS-5_sszK~0x0#_Uz&?=HJ1WsQp`MRP%T;cPUYX*)1%2d;T@56nvcOWv&GRX=bnFik9i00c|#9f_r-*7z2n3iL})VKdRJzIaxk&2J;aAhD0!i(O}6Vo?k5zq8|gQ@+k^(9j!rV<q%}JWoCFOi)B+^+JfadNkv8T;`IG2~5bR{C<k7$kevaXba{%s}>VGN*XgD*~MT_3P$O(SB@U@#={-hg(YRN{e`CNOB8V}fiPnpTtxk8(zcNk_bUNjr;s(iZhXqhmW|0$td=B5#E>eZge`#PVp&sZca=s$8O>23cPS{dlF?<85qAgqamG|Tx7=bl($i+$fjGn{_jK<pc2V!loSn_f@fU^<%<iqOeXVopYDEmxm{lg{SWkdY2{LRVxRHgjn+GRw&H$WFej=?2uX_yO$q!1OKjW~?#t#^sG#TOO=nDiSSxz_lLN3VK!6;YZtGnb0%XlHCYC(6hQ~-V>RCu0?0IJ-!nn5rihk9kf<QbpKgcLOeHUPk|AjB$b8qyTWsAukYa&78^LP<TV(cXG8sQ;lels{U^fV6pPk26320y9qTlS(ON=W9tl}y>jg|End;ebYxbjmTwH>l%~~=+$jBF{z68C`hN$5v5IXu_Wob&TJ{w0w+XKsyoq|M1dq*wH3ocaQu3tBZAXpSueZdQNMSi~hZb0jBQ{>us?SrVz_@YS|*Aaf=u<r2(AWmCjyD;AR;4o_xT`~6%r*S9niP;AyVPeUfVG?R&H~^iP!u|wv^7=4$j}BnNQyU+AU_e_V5#J^xX~8AZ7?V;ANj`cB(>;y}00xj%0v_aU-}OVaROC{!<Z-LWtZJI#GOE)zjF7$n=W&X!+#=l@c#gscPeEYH`f(d(pL|b8`VUip$2pwEfzWMr^6A&#kCamE2u!~o=pIDs$)17pU!Q}hH?7EO6x$H}YWO_9z3T)r+*G<dHTI^v1gRb4X{fEw4GFeJd{uQd7%US=u+rj0;zc%HqrHD~c`xh%3_LH8Y@9rp&<&fI6fza~o2U0;`8wiNqv<|!{$6Qy)xBxG<0M9LpUC|xtKKSX2F4&u&(ghJ1hcSZXsF5Fa<@YLGp<TrOsd-uoE&iMn&;U@;2RaSy>`YTaQ2~!Z>|wwXFCwy)m%bfQ>Rzs>r4?<8=Bl;K$ah<(AP*H)M$47{fv0an*O>oi9b0IUwIFuY^jNF&Blhb^HLJ{NeaO$GZSs}+2=ghUf-`r$Iq%C7)uixIiZqKNmXrV=djCy51*k_DL}aggbjoW64LdZ$g#57!6<8n4w{-lCVtrW+Iq(a8bGS2J-NLP2bbN1dXW~@m7ctJ`%iTqgQoK`25Oi>kH@s@eBFOc6P7wqa62IHND-zmb?`T-3O$lmp<9tn?3VbpBXjXIbW5t!5WQq7>(%B4cT+#mTe%bxQrbipe;d?;x9!j|Btq8*a<u<Io=lGcL2+;1($PJm#5!x<6l3R*y?GN{W*MC6Pp_o^y!`$=S1-ZAV0vjx_S>f0#(Q_P3i-X>olq{0$j<~t-ieAZ$P`=SxzF5t?GQA&ob9%_5>Haj>_l~7a>XJk%>(eSEmVFalQwgHMgB}exz5h+G?0gbS7Jo1{=)aCkZ(#t*wcKhhMIkP%(AY#X=&LV3e0<~S`?jX&(fFa_j2V><0xQrQXRq0C&7Ep)pG9aJk_{7#4ZGT!)WF7v2dzVO4(8UJWb33xZMjC%ThOZ8vHwRM0eC(=U~-$jt8*!A(EN#oFST2K5T`cnzqc)F{lmRj{`_F0%mSVbMe_`V?L;|CJ2VVtr#5St<)^aRJXaG`KEHyM~mi{xOswI3+8*1r~*UBklPr&iG!>dC^dT7ljXD&y@EK4vQ|bA8h=>gw5gkqx-4T>5-o^r=ASH*S9W=U|9IUaJw`j^PjIXk`dYJTj79+*BtTTVR8W5MJVtvy`&lIU(AGVkdO6yxrc+CTwc3YVb=T6fZKm=5#{|pf<r2!OQ(?3MmTU3s{gIgCxeJA(d${f$>1f`faFJPU66e<M0b8N7gxOPptKthanPf%AwLmOKz_+l9K%E*)RZY2d-Wye?azeb%t*cJ~j)_iN)fp?nwD6Jd=_=1Ru-Ta*qj+vtz7=xA)=ktly?6eeOjF$rx3%n^^oZxkBiEV`px<Q$-b~vWfRL-bmVE6?z;6{30k8j=*f2~O0U(Gs*^PHpfVf*1I%uRsMz-IK|F~H$33R3r4JpUiVMq+cWwG{73~Ug|2&B3+4AO${wrHm4Cq%>8+$+ARXm|Li+!K^$G=H;gAYpH-sNxXp{+z0$^s~C_jDZ{&dv#r$^n^aQ#<O<A3WyzRj$O}`8hwSL3b4Oc<ylGvnCDX4W|YK?H9=8%V8#5x;LI5fNH%dyTkX=nM}pPJuFy)N&sQ~pfaCxGsp*nY{2)#E$g+I<h-ZT&!L*iKJS$yptn3P?@}ko28l!|u?ykE7CUaVAq(O0h>TSWMSpy;*(jFxILG98D0F!6fyd2eS5o<DSfa7S4hy)R8U@xy+Fe}Rb7qo%~9Nm1Cc%(>qd~EO~g=fhY%N0sim5^(|lZAavZdIJ<2x@|EU+OdKnG7nTO*B4nS|y{`#RJ`0*RhaXI$pO?R|e(l*0OyWwjlGYHNiD@Z9?3yFghTck{{Rx;<vr<d;I0gm)~DyCG8kIMJV4&6WYgtf;?3C12&o8=ZV1C<0F2IQRfbT08uS<>uugQh%VvQSJrmG?+@7uNjgdAEvc%w(EYA*lDEx>NFQZW0(m7g({%)A<g*hc2ugJ|doCFI<_H#qqrx31703|&OlRk~Cqzld%!ivlz#Hp<pUaP}TlV#no1U&RU^+qQ59o&g;c%1SezD){Jewc=Bb}J!-VPdUQU2uKInR?l_U!kEgja!*S~O}(cV_+X>-m{2<wxs|@Mu_XL5qASn|)rHO_!&U&${3+IpuU+fN0LWw=T%PeOU|P$QZuzn9lQO-0Y8LX3DiLRzv6Ow5KQo_MOadxj}QYctyJ`d#i%K(Rb(}B%&@*-T=R0<B=xilWy>H-b8z_7{!}+iXb@4-w(j+kXH+ix?2GRMLhvaKi-D=GA8oZSABWT_fwD6ondPxXpp1+m2We*1Lqy&8nu|$w3Al7*@C-ubHx1=?sjv<UG;dluSWGGu723zJvh#~RK=_OH&6@xDHgb}Y<Qg?vNlEu9F-GZglkO~;}Jv%Td*V6mV_`pR(F`%_fWN<GnypH4vE+ZB}9XwP5BolvmPpZjrgfDN~|U6+j9`y!&*A**!NV(zNnr*60yW+uMr^$ykB$jz+4Fg?X7cT>z8&~Pfo2CY*#MEJ11Jci)hwkw+hGJCPjS3@bNCz{*$hn4@sng?1Y~IsoF7GdmvooE;440<>Q}}z9UP_0bl%XOUnRA+fV`z6%))uOJ8-n^$`FVUD4vH(X<eCkt({=%gG2ReXn}n&{{Kp1m%F~kemaSlXK6odh$t9_xjA9Gg=O*$P?Cj<C}vuxv5h=+D}25oKvv;4MU1r^Y#wLw8ymqi{N1H{(Y4K#Coc@_4p8DHivyuZ}xp}UsI%O*6PX5g!6TovNx`~Q-UG7g=yY2f07<U_^fV?9w!c%Te(mcqfRXpLBSIWbY>@A%^|29bN>t<E1bX<1GQa9jsk6Jvq4$G*pXY0fdSp<^AF$~L9z#9fM|*i`bF9=7?qEhG&q&WO?<t;eyx!qW_D0vi)0!qZ9!3oLAlBQO?Hhmg_vu9L6Ql0%?VVkh)ICreg)d@4|?j$VypkjXR5;W3=$36zg0;vr+w@%>_sIbS7Hx7-1KrWvBLm6gt*}~(RW_TozOFiR=kYr@8nvv&MxBuG?TKa5jOFcl6obs`6NG2_KP*ufI+IwBIH(>ieRY*DHl-w>Zt;TI<l_@vt+NrjvN{EXnn{61f@_<9!v?6?=g1UTvMf;v>Rr(4l>Z5XY|igC5n+UAh?I?choWV=I+^^u$LUG44DbaKqp-`g7`b4FV{07;TzRQ4;0j&q~kh!kllz26H>#zS>@A5C6ho4q}HPQje?OQSi3e$iM)j;pii()8&sL-2LBLO&Q&`dm2;reZ=}mvP)UiyqBWr_Fb~68*35tyed5rS+$AC%2>6;{E^KK&yMwfe0>O6D$Gb1oO@V2)yta!`qfol0gIAVAU2*zQ*`@KEkSbU`f|m9peKhFGp}xniS21xDeP86XNG95w>z7!sSJnRcE}*r9&Y?LTqgU~!+RyeHoNi}NjM|(zmvJzZ66B<I+FI#%90EIVQVOzb8>{1GCrxDEwyFD>9yL)xm6fEB7r_W=W6B@HBwf71*YHhiERgZZSa&F|UGSL^NhVwL`A-0@(z6mRd#4SbR)2h{c+VwZV~ul*AJ?%>JU_H*SywSQcH3^#gQ%Lo--mt0FvI-J>Fo#C)CgvNa3!*br=liAMdXr2(`v_2UY1Iv{=~>qwV0e_Iz)x{gl?k>4>735NfrV(j6Pxo>$4;fG6|3oE2EH9O&S2Mkv<>gfNk0^z03buy`1Mta(#tCGZ1--<5<*!HI)DW1H$wgpK)ceYn=yq^3@K>Vec8c>>ch<Kww`z(7wAvG3vbywM#b2qDodc<2oiZ+s-N~=;g>*gjB@=ggHP#sGr0sta*FVbA}@$zeBIH<?RL2?{dq|u>F<ITxLohkiimDC<AyQ1NG%%3l#<1_siBE`qe1yq8O!U2y%%*zNy1zBXSNLvBj5A@Yq?au#xN9(jrns6}TyY-Y$pEs<Ayru`#HRhsX<de`0R_M_%5>V>}RIrflBxe|Y`nmve;reOSGOE!go5n?PR@k6ubQI8KC@PtPablHcnE>z4h_MFP+(S6W&zR2I?IG~&chCQj@$dMlTuiRF|*N~M)^ISOJhRWs$PltCf7au99^h-@e0Dv+Tpov2c_uW%<1)J!ac7xCd$$HJ6**MNsXfPvZ~YlG}0X7&kA5r?B!vRa0Fi5W%ECCd!rQA}6A!smv+y0JrD%FDR`c9Yw>9sGQFFW}U4;O*A{$W{be<i*=$(UQ(IWEfUo62pCNo-~<bKU)PEA8pg&#b{FWYM@|{d=Vf{9@%#CJ!?$?Ti$eZ#p`3xr&5o5Uqj{RUw;An#}WV<#3ghyGZ;XMug%&HZJC<o^tjgJ;^+~kqPthhmk$AGfb3mNc`Te_6~hoPdJ@OY2zsXnuPXJ+ats07cqn))WbkZ;gZ|O){$!dA*tL9cvcjkTh724&yz!R{r)^*p`&R8JAr}phq#$?S)YV^ll{(XGkFrkLjmMH;I3w?=hXV@G$q3RVeykh#is&FCh*2|ImWa4kGE7?E1F)kJ2Mi)mWB?ac;L}6&0F!5cu^*FfU{b{3IZ6uTUkNvV!k<BSHu#;&w#TDlxDYJAc?Q-|j7^YVNozxd=CB@kQe(OlCFJX=$voBdI+-XA>{3?mJz8iRnE$Ml2ws>VX9ze&m$1MHRpm;w?9?NIEzTXH>yzx_$MLjPK6msShVeG9s^ZmbA6Q_Skv_`v{(Kl4@{03^0`9dL=PK5I6Z$`hM<~Aw-K2dD72W3CwQSt3D)u)^rIV+KBnJkbph7O~$6-3hIAR@ps0+sQrRXPEPq3^&+%}Fbmsrv-$}kGF*q?Mlin`he@>o9II%*+{pdT<Xb`@3^z3s3d*G`^`$qn#kEego{VdE58Ld6es0K0UP3lz#uY)L+O3AEzK=?V<A681?8SH5mwrR>Hw*{wk%AS2nFj2|c@#~_i~uu<qDx>@7V@YB6t6LFqOy#KJxZo!epJIL^e)}JP1H6|Wex1*sl@YtmKlfkh%3_Q%(@3kh(J1LH_E?GxSeU{3tW0lVlR0-~~NqyWe{mDj7E`$dYqVDIe@T0v}_fR2#nJ?=gwQlYna?4aA2R#$@Sb!Ld0Z96_p8HQYoI7TAa?I*xoq^o}Hc6@^Cxext{uCy71j71G>R>G?d@!=(j>7Ovc8<AKPZzq<H|rQSX2Xu?e|F}Qy4|{^k4VC}*_AWV25_>n{Fir?!vlxxsIfyu7a`!AvP(B=!NU?UA3JEUl$-YY*2+afC>3=TE<sNF<D>dSqU}derxwtls{1uUR&LS$-RB}11Q4k1QY|FRrHxy(%}{_|-{%ktFk}ibl*Ee6CKPsmn7h~18Lrk|#9&UU*eb0*09cqTmHHngedqEg?-+d<-nyG5pqTtntfForkfm462IPEh_FMP{e5By9z%V{-rnQhB0a}!m%IDJQJrY1<FN+2jgl~#bg!0pLR7^;RDj1VKb3G){WdJFgzIqmzSJ7tiQ8j3q%$TBdPB#Rn!|;k=i$aA`ScG#CmN}_vn4jse@+J@JLU%UK0SR6>H3QkKNGbcyne~^*=OB@VXt@oU)wJ%-;He;-KgE)766$0Waf+$~tU(@WiqJKpvCu6kr?k-uVCelokW=hKE^F`O%(#niU#$u}GPe3zvFaKYw^w_vBYT)^R-@lXK)i0_Nuoz!HgK4cSxp_AcD?^s-nA?@ZY04U(m@0tB9Hbi4;x{xBJ6SCG~qAtzwcNSDFBs~nN@&1F|nuR${Y#Z=tosnR;J>-4#94F_-bUbrv$BYQCHnu3&2$0-DpTDD;vla>y{AA9s&muQodps6yjilVWus^PpV<CD)@@YJXz0fWIo4g2Wnhm*WgeQ)T*hm<~$r|c%heN#-#c-^5W4wO+I+FhMkXo$6!2f);3P^PX-rnm5L`!8W8D0q!Hg0wUO=;2BQMP5xgED^$hn3_w+#IUP{eaF}5?LOe`fUD4Ezw-(%-ez|WZOA<`T~ugVd3Ep-vcxwRz>sJ-(V&2JSfo0UP9`iy2p{%cn$(Q`V3VZQ;35Q<{Q1)CIASeLjI3Q5OG&XmscGeU~YBf+g#t0_071;Jj_f2<Hv6LcChq7_&wA*?L5FJ_@kD=MSSevba6*v=U<!g6qyo7-*v%V<DlHyF=s5kDf)T3$n~ml6i-Agy?I%I>{9yQ-)#UJa8avNN07%mwtDAR`4HcUA_d`d`jA)l~>_2;KDbCDb?))2$tn)}f|5!~D1yy)`I6G#ZzgRFME&V=!8<P+?PwxlKsmTdqn8+VvS;Y=Z;ILBpk!H7TxA(8z%*AYRUM@MsL?Qc8>!N;+gD*DO*?V0S?f;x{<>OqP`yR+`EwKAg<+VGn`WeL4a`Jr7~xd*baZ%-fO*nhx#{8E|oCZ7?C^t#D1UcHC16d`NYwRP_Bxy@VuXP7#DdL2ZS~y^dFdU}N>9Qz0f=;BI(nDY`VQOG|nzpr2l)@+=IQ6Tvc3LgJKI1~Ui^58gHGT&|f0c&>7}Ps71Zy5CeaWq$H}-h~%zQUly1H4w}rDIZ6f`r|rInZ*#Oq6RPvXUqo~?ieK~K@BIF;K*fMZ1Pqc*|0%hzxi8cw>|R^TD2|JZ^`<A72R!YYgkV{Yh<8z60vo#OuG)rIexBm|7J^y2<`jnT(+lmRPCuCWIP`!Sz)w2R_hPN&OeKasf24(;_c_F?1C)FzD{9l?Sz!TMHQhC&W{1B2>8NzTqMD^p!(G-_%5iA0x25SJBm{sBO=k)Z4k>_In~ifwyHP#hL8p?fEhJD27Kqbz9q2cw!&SBS-(%HPEx_wY@9=jY}m~>%+8?#OuiKW^taAL!D#0IPO*Qim57_Sa3u|c*HINd$x4@RfX~Y+&)s;A(ff#=puLPKW*(w@K9?#H4Dr%aDUTS^c`VLNQ)j9M0abKQnxX_=id@mIeToeNX8lq?02PG*_-dFBh9*r``Uc!TPctSIvx$2A$17;bU;_WB_*hc>MbSPizxCxJI&LI4&$A6HY+w`xi{{WEjPD$dMF$z-Yz(F!p{rOOCn$jDB_|s>tDEvc9%I{#5etMUSCqHwAHsGs2D4*a4nl;7WTAOF@n9cGh<m*_qWX+MYkrx4xP%nZonwq%d`x_sQCRt6Bk5(w)<@FcbBDpo?JyR-v5Z|DH$qRynZZ0np4Tk&PV%8mZB_iPK<<Z=DwS@kSR`6=PTIRVCpz=dzl}?0YQAExXFWt*xWqo2Fl63e$yza{s=Ehy6u<G<Qf2z2T>@`zRTW~I*CR_-yq3D#2#<k~al?C%!b}!R3I1AgL}a=(CEekwz|11n{cOHa)i}svqU>dthsj;JO=>Wu9&Fd<l3s>w$?UfIh>oHH{z2~t8m$ppG5HOKj23bU<<FEVVwnv?j%sr0?&<N>8H~X@z5VzM@O#UI1v-B#t_K+=cBFan6gCBs1u!{RSUu$T0-+QerEF7kC8@+SDVDs3Nh0h+f%`{0;?%OwF+I6~FJBAES6uN-tCcAuZibSSwu!G}#B1`V%uczpiYEy@oKry%j>X!cBIH4s34-DWInG(_yb63AVsT)okQbR~O8Stf8lN#A>V3DAsqbkVS@QawSP8-%@=lVDW?Eps0dVizNC<rcoE1nWzEdi<B+_Y2OG)JNecW^J?7&*tcM^kZP_!i{4^!Q5YNkn%H`F<uJ7RinJtaKvTxdA5CGI`m>XTW}wyJPRFvZr3rajjrraP)DYfXA)dDd~6k?%H!CA3wKlBacrT@Oi?-s`r1n~bv!Pc-I%rSXg<P3tHmdB}REXe_{}fLv>f+(<KQj{H-FEg8*W`-(U}H-k~Jg(tq5u&y>@%#eZ=2+jbN*5mZll+k>td^N?ka-%dACqXDaDAyEjnJx={GlEcNMyba03abTmE320vM(#GAw_Tl3_!#%d{aXc&8O2#;qB!XxZuP!7Mu+N+`Je#UHA+BG4P1|~lNiv(9M!a-z>3|9+|4ndRWFX}NqDxVdhdTsS7gGF`hyVK$xzagDf*7}i#zhRND?L83%q83Nb+jd;-K3fY7|u0B%b?e#SIlRVbhjYsPZ?NP|WVNT!k+;Xpz)kYN%p{Em($mgGt@cMfI5xUzJ#|7HY<ZZ8*PoE96dUBtTqk)HAc=+DO_9-R1NEM-Sc$-%RcwV|+MXlB<k_kW2LafAQ8d7lO6WZ|nJDbk`U&V*^~IMOd}^v$5P3#-)T}DZWfiz}Z{Q9i(b<Q+z6QhVYPN;*NpH55`eKI$=)D6s<%mIx9qSE(VQ=H<<wu-7rJGDA522-1sZZOJyOMT<E6Hv~tFrGa`hc(?)!I$>(qNR2dq6jZ)DJgo*|#CZ(#X;)S`7L^cFplZLTa+fKD8SH{s<NrDE5un`wGUgz!f;c?9iCVj=kVK!4Irr}(qV$I*p^8YPsY4HQgwwHJGc}>EmfVNCB7bOzpgZ$<4MI9>%9BT_4-A=ZC^^Nw~ZVfin9xao10ZO;hqnpZo)sGEIG|pY*YlmAr@CygCU&6f_RT2&wB!XVXK6xT)K+`LFebs?xo{0jqIujHep$Zb;e*bT;Ux<3?`xhh$hFeXlZ2|!b>zz7d5vlK-zIt}0X#@qFy@HNEAGOVzub!l72QR_y&UrDQsiDhhTMy+jmsk?1O-2G&){58xRjra#p0!Ye)mMXj%Y$<rok)m*S(WnxrekuFQslX*Ks$&PWiF^O4Ju@K_bnRSO#ESD#grAyt+(eKLMlo^kXi}X1d9UvNF7tuCbvN>+vbz<QXgD0P*Ev+jx+s3Y_cKGsD&RFgzD;?v4cCn9M&0<Jv9^>KLqSULW<lKYjCM%*#yzS#10Y2`(aF7j<IJ`QfHN&bOQ<V$SvsA5nuT_uqK6M@G1MCi7Bmp{vyh7n;>AMQFp;68{qu9B=Q*`Lw0rAgc+eQe;;Rg)3CSJl#nDan(Y4u6gWEVGG`lVd<n@;Pqxr|gjE39J!p|DEV(--mOh)~4BU%J@Z|TQ^oT>Pk=qFq?V4n5SZ<4_^R%?wPqr1a%vzh&95<Tkh(<?QCUBQKSExhOS-pqoyD5Ud0cn_SBOdF6JZ4S|Dg|u!4E4FDzaXkV%AFH{MUxAxcnU0<nHsIrEJ?&BTk(5w1uxy@*&cgYu?S6Uo*fZjJYXE_IKg{&h%}AXj53;JYv!E86yC3g=Vc=^lM=95+7ZE-<E$-Y9(h4m&$CEAregjZK=Fd*0P+N};f;iWZG7A>d>`H3$IvE^<VyadyTilB*w_6)?uSFsk|b?OE6WkM9dmVG$#~0Ai~_!=#3d~;se`a=SB%XaC%?JC+T(j7^`^^^5v@iCsv0FenNFeEvR2}~EyzT${w;vPw0Q3U9>(iCrf;qCcI?_P;0sYROyHn6e|lpgv}z6`z?D>MzzD!KCrg$)_oV<SVw#QSBn{2Oa#$k1Ygg>CKv>p{d+1WD_(VH_jp@wQQ7dXvKbAX;Wj5b3%O?+)qm45-UM|@RaGv7gOs7DC6aAw@gFt2=JdNoo_>zI&T-FkBn6!GU|7YxQZ-$WTzm!%G^N?rM0ks+O=D9`=L*%ib?Si=1OriXG?`GE&2-&09hmA<*v_9>A1<K;#-OPJH<deo()_gk@xTH?DnI>bN;)_9=$$jK|9d+QOAQjaw&jLt77AmQRnm~!6cP3g6z!+8$9aSvFvqx?eb7clJtfr!MM;P+QF+&siF^<k&eNL0QRFfYS2CFuvI#DS*BAt#?_V2;r<aAGRJDPG2W&M*b0Ob!Ky6l!@!zO!c+g3~8;SInaFx{3Yi3hKws@_`g@g>go2`ZbTwD{cPepRflxZNKlbM<*+TwaZWXm#&8#(?Lpr|Trzt>`QFJO7}6q!gG>5^#zLN&HEYJO>D4Q&W_f+S-z46`M20$Js`jvt*`?VxCFU#9WSFh%A#8eEXHYPmAlUgA}*9Q&xegfBoIE?_tdsuA`at`iEi~>uIkt&w;G@rUalB_8{P&#UmGMA%?GQ0B>mJ+e&+K++d~sDWq{9Hn?Kr1yv<!HR;*X8FFPlXaNM0*q)jM;9lRwcr`VVo1_ogMqK~YyW=<`s!)yLO0UH3uhi(rxLWQ^#S>41Y`d&6XmDOSWnprYKG4~^014T>6%=9w90urA=KZE|qxdinhW<)LEoTMPi<sa&GPaqt{-T|+zS{E%aL|0^%~*b+idvz(?y#eDSJmYuHsoEVgs#Vl`uzO7LZra!IMiBEmI2#rG5!7Ap&erWLpH``7JI6=wtW}VHd6OabMuq;wWHZi@SI@~J8E$YOL5b#y!KQqHR9q>p$Y&aNyaHuJUr*9!@j*aF^Fl?1kfPode({zq>uq){Gb2$&oBS}^Ixy;cMMZ@U*3wPTa3(;T{0dU^cVD1xEMa@mrttb4@SrCTM&(9F~8!{*MKb?jN~sAQzigKZ1Lav#&5h4pWaM`XecgMB^+v&O-ugFq<IL;Y<b=8>M6GXj%fQZWrDM7h-t%2AhL67#h@@Urjqx+G~4nK?V*ovc%oO@PDdlR02hl`B!wcWbe&(R5yxRJ81h}tMG<1!Yk`6Af-3+&dK%+HA#JRjsa53L;wiDm{FJPZgV7%hx6j>>WvrxWW4!+U#cjGO427>b#%ZN(S0v#j$B*&&p;oD5aW>Helge^<@ar~RTy+V!sQAD5tL`}LqxaJm8~_<+;KbYLP?nvFizdef+eKMXyFOU38o7^Ze3iE@oA*Bnb{H6?dD&02DYEkaCL>Nubkn7J$W*A~huJ?&W~IC%--dp<oHDWL%ektMcYl-*gfmD*#1D@z!(U}@OM*j@;ltC&QagX=?VLUxbsDW^)N3KibVPw3p>#~2_t1E63(2Hfhcp*O@kEpIl&#@<KYEFAwZ_2kvyQqduOTtwf#5;s64w^+rYMkQN(8uB<)aDI1qbRQNmy($hpuZ;Qh=$fs*2aV;$2&4v_J)46bot6FZCCiezVqcdg6jrn#}qFTzj=qIfy&#xRQrt;GZsJ#mJm{>4+_(0Ed)9S{r~R+h9AEA?N*)J=8J=u{??Wk1SW!=8x1S;s>z29*YWin@X3pOo2PdJ34{J`vdq4H=KGP+&5=tJ_gPr%mHK}#}Jbpv0r6tE=2zVn+w{6Z8p`eLKrX8gY(PluRncx4PTxfy_fSen*H_q%j<thq997!?@-tLhaoR1<;%1visbjeY|6q)d%71tHs*UdjX%JIGm{IsxJM6{{(qT!!O4#IfxLp3rJo0EB&v6hzhGR?ML1#mm$Kap04YQijAf}`Hs2A>L3)|jZ4R0rW3K1*&)Yvnq5?{&cPjZ5eqjoL6QFJJ6NZ#JEB`y3NWJ%w8wbWYiXRw0n|v^%SIAU}(cdy?`})`a0IM2Gy8')))
for _k,_v in _OURS.items():
    _ROUTES[int(_k)]=[dict(a) for a in _v]
del _OURS
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
    if state.get('requested_day')==day:return action
    planned=_v219_native_day(native,day)
    # EXP240: committed crops must wait for the native worker indices.
    # New schedules finish native hiring at hour4 or6. The existing two/three
    # crop-worker groups can still water/harvest their ten cells by midnight.
    # Initial investment stays within hour3; ordinary schedules are unchanged.
    latest_hire=max((i for i,a in enumerate(planned) if any(o and o[0]=='HIRE' for o in a.get('market',[]))),default=-1)
    deadline=6 if state.get('committed') and 3<latest_hire<=6 else 3
    if offset>deadline:return action
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
    # EXP242: preserve native indices while servicing already committed sheep.
    if state.get('requested_day')==day:return action
    committed=state.get('committed')
    if not committed and (hour>1 or day!=12 or not _v233_eligible(obs,native)):return action
    planned=_v219_native_day(native,day)
    deadline=2 if committed else 1
    if committed:
        last_native_hire=max((h for h,a in enumerate(planned) if any(o and o[0]=='HIRE' for o in a.get('market',[]))),default=0)
        if 2<last_native_hire<=6:deadline=6
    if hour>deadline:return action
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
        bonus=_r88_feed_bonus_cost(tile,day)
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

# EXP219: charge care credits only when this feeding decision can affect them.
_R88_PHASE = True
_R88_HORIZON = True
_R88_ANIMAL_DAYS = {'GOOSE': (4, 1), 'COW': (8, 2), 'SHEEP': (6, 3)}


def _r88_feed_bonus_cost(tile, day):
    first, interval = _R88_ANIMAL_DAYS[tile['animal']]
    first += int(tile['placed_day'])
    tomorrow = day + 1
    produces = tomorrow >= first and (tomorrow - first) % interval == 0
    pending = max(0, int(tile.get('pending_care_bonus', 0)))
    if _R88_PHASE and not produces:
        pending = 0  # It remains banked on non-production dawns.
    care = 1  # Conservative: charge one possible CARE even if not yet observed.
    if _R88_HORIZON:
        # Today's care is added AFTER tomorrow's production; its first possible
        # payout is a later production dawn, which must occur before game end.
        next_use = first
        if next_use <= tomorrow:
            next_use += ((tomorrow - next_use) // interval + 1) * interval
        if next_use > 29:
            care = 0
    return pending + care


agent = globals().pop('agent')

# EXP226: retain physical grain for two complete days before trimming a buy.
_R95_PARENT = agent
_R95_REPORT = {}
_R95_RESERVES = {}

def _r95_reserve(obs):
    step=int(obs['step']);player=int(obs['player'])
    native=_IMPL.chassis.players[player];route=native['route']
    key=(route,step)
    if key not in _R95_RESERVES:
        demand=6  # Physical buffer beyond every scheduled pickup and sale.
        for t in range(step+1,min(719,step+49)):
            a=_IMPL.chassis.routes[2 if t>=648 else route][t]
            for c in [a.get('farmer') or ['PASS'],*(a.get('hands') or [])]:
                if c[:2]==['PICKUP','WHEAT']:
                    demand+=max(0,int(c[2]) if len(c)>2 else 1)
            for o in a.get('market',[]):
                if len(o)>2 and o[:2]==['SELL','WHEAT']:
                    demand+=max(0,int(o[2]))
        _R95_RESERVES[key]=demand
    demand=_R95_RESERVES[key]
    # Reserve full feed for a possible southeast sheep commitment. Do not
    # rely on its future discretionary buy, eligibility, or existing cargo.
    if obs['town']['unlocked_shops'].count('YARN_STORE')>=2:
        demand+=6*len({t//24 for t in range(step+1,step+49) if t//24>=12})
    return demand

def _r95_replenish(obs,action):
    step=int(obs['step'])
    if not 10<=step//24<=11:return action
    orders=action.get('market') or []
    if not any(len(o)>2 and o[:2]==['BUY_PRODUCT','WHEAT'] and int(o[2])>0 for o in orders):return action
    # Preserve all same-turn grain trading/arbitrage sequences unchanged.
    if any(o[:2]==['SELL','WHEAT'] for o in orders):return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,step//24,24,100)
    held=max(0,int(private['shed'].get('WHEAT',0)))
    reserve=_r95_reserve(obs);result=None;removed=0
    for i,o in enumerate(orders):
        if len(o)<3 or o[:2]!=['BUY_PRODUCT','WHEAT']:continue
        quantity=max(0,int(o[2]));retained=min(quantity,max(0,reserve-held))
        held+=retained
        if retained<quantity:
            if result is None:result=copy.deepcopy(action)
            result['market'][i][2]=retained  # Zero keeps every later order slot.
            removed+=quantity-retained
    if result is None:return action
    _R95_REPORT['replenishment_trim_turns']+=1
    _R95_REPORT['replenishment_trim_units']+=removed
    return result

def agent(observation,configuration=None):
    result=_R95_PARENT(observation,configuration)
    try:
        if int(observation['step'])==0:
            _R95_REPORT.update(replenishment_trim_turns=0,replenishment_trim_units=0,replenishment_errors=0)
        if configuration is not None and any(configuration.get(k,v)!=v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):return result
        result=_r95_replenish(observation,result)
    except Exception:
        _R95_REPORT['replenishment_errors']=_R95_REPORT.get('replenishment_errors',0)+1
    _R95_REPORT.update(getattr(_R95_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R95_REPORT
agent=globals().pop('agent')

# EXP231: protect inputs using funded current orders without unassigned cash padding from observed physical resources.
_R97_PARENT=agent
_R97_REPORT={}
_R97_LAST={}

def _r97_market_stock(shed,orders):
    stock=dict(shed);buys={};sales={}
    for index,order in enumerate(orders):
        if len(order)<3:continue
        op,item,n=order[:3];n=max(0,int(n))
        if op=='SELL':
            q=min(n,max(0,stock.get(item,0)));stock[item]=stock.get(item,0)-q;sales[index]=q
        elif op in ('BUY_PRODUCT','BUY_ANIMAL'):
            q=min(n,max(0,100-sum(stock.values())));stock[item]=stock.get(item,0)+q;buys[index]=q
    return stock,buys,sales

def _r97_delivery(stock,private,night):
    stock=dict(stock);lost={}
    if night:
        for inv in private['inventories']:
            for item,q in inv.items():
                q=max(0,int(q));take=min(q,max(0,100-sum(stock.values())))
                stock[item]=stock.get(item,0)+take
                if q>take:lost[item]=lost.get(item,0)+q-take
    return stock,lost

def _r97_budget(obs,orders):
    farm=obs['farms'][obs['player']];cost=0;hires=int(farm['hires_today'])
    # At most ten 100-unit purchases per opponent turn. The additional 1000
    # own units give an intentionally conservative upper bound on buy quotes.
    prices={p:_r37_market_price(p,obs['market']['inventory'][p]-2000) for p in ('WHEAT','FERTILIZER')}
    for order in orders:
        if not order:continue
        op=order[0]
        if op=='HIRE':cost+=_v219_fib(hires);hires+=1
        elif op=='BUY_LAND':cost+=4000
        elif len(order)>2:
            item=order[1];q=max(0,int(order[2]))
            if op=='BUY_PRODUCT':cost+=q*prices[item]
            elif op=='BUY_ANIMAL':cost+=q*{'GOOSE':300,'COW':400,'SHEEP':500}[item]
            elif op=='BUY_SEED':cost+=q*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[item]
    return cost<=farm['money']  # No current sale proceeds are assumed.

def _r97_supply(obs,action):
    step=int(obs['step']);player=int(obs['player']);day=step//24
    if not 144<=step<695:return action
    native=_IMPL.chassis.players[player]
    future=_IMPL.chassis.routes[2 if step+1>=648 else native['route']][step+1]
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    following=_IMPL.chassis.routes[2 if step+2>=648 else native['route']][step+2]
    next_orders=future.get('market') or []
    prefund=0
    if len(next_orders)==10 and not any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in next_orders):
        later=[following.get('farmer') or ['PASS'],*(following.get('hands') or [])]
        demand=lambda cs:sum(max(0,int(c[2]) if len(c)>2 else 1) for c in cs if c[:2]==['PICKUP','WHEAT'])
        if demand(later):prefund=demand(commands)+demand(later)
    if not prefund and not any(c[:2]==['PICKUP','WHEAT'] for c in commands):return action
    orders=action.get('market') or []
    if len(orders)>10 or not _r97_budget(obs,orders):
        _R97_REPORT['supply_budget_declines']+=1;return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][player],obs['private'])
    for actor,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])];night=step%24==23
    access=((4,4),(5,4),(4,5),(5,5))
    if night:positions=[(4,4)]
    else:
        for order in orders:
            if order and order[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    need=sum(max(0,int(c[2]) if len(c)>2 else 1) for pos,c in zip(positions,commands) if pos in access and c[:2]==['PICKUP','WHEAT'])
    need=max(need,prefund)
    if not need:return action
    original_stock,original_buys,_=_r97_market_stock(private['shed'],orders)
    original_final,original_loss=_r97_delivery(original_stock,private,night)
    if original_final.get('WHEAT',0)>=need:return action
    result=copy.deepcopy(action);proposed=result['market'];blocked=False
    def project(candidate):
        stock,buys,sales=_r97_market_stock(private['shed'],candidate)
        final,loss=_r97_delivery(stock,private,night)
        safe=all(buys.get(i,0)>=q for i,q in original_buys.items()) and all(q<=original_loss.get(item,0) for item,q in loss.items())
        return final,sales,safe
    # Hold an existing grain sale first. Preserve all order indices and every
    # originally funded buy; no extra overnight overflow may be introduced.
    for index in range(len(proposed)-1,-1,-1):
        if proposed[index][:2]!=['SELL','WHEAT']:continue
        final,sales,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
        if not shortage:break
        sold=sales.get(index,0)
        if not sold:continue
        old=proposed[index][2];proposed[index][2]=max(0,sold-shortage)
        after,_,safe=project(proposed)
        if not safe or after.get('WHEAT',0)<=final.get('WHEAT',0):proposed[index][2]=old
    final,_,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
    if shortage:
        last_sale=max((i for i,o in enumerate(proposed) if o[:2]==['SELL','WHEAT']),default=-1)
        index=next((i for i in range(len(proposed)-1,last_sale,-1) if proposed[i][:2]==['BUY_PRODUCT','WHEAT']),None)
        if index is not None:proposed[index][2]=max(0,int(proposed[index][2]))+shortage
        elif len(proposed)<10:proposed.append(['BUY_PRODUCT','WHEAT',shortage])
        else:_R97_REPORT['supply_slot_declines']+=1;return action
    final,_,safe=project(proposed)
    if not safe or final.get('WHEAT',0)<need:
        _R97_REPORT['supply_capacity_declines']+=1;return action
    if not _r97_budget(obs,proposed):
        _R97_REPORT['supply_budget_declines']+=1;return action
    if prefund:
        _R97_REPORT['supply_prefund_changes']+=1
        _R97_REPORT['supply_prefund_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    if step<288:
        _R97_REPORT['supply_early_changes']+=1
        _R97_REPORT['supply_early_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    _R97_REPORT['supply_guard_changes']+=1
    _R97_REPORT['supply_grain_protected']+=final.get('WHEAT',0)-original_final.get('WHEAT',0)
    _R97_REPORT['supply_buy_units']+=sum(max(0,int(o[2])) for o in proposed if o[:2]==['BUY_PRODUCT','WHEAT'])-sum(max(0,int(o[2])) for o in orders if o[:2]==['BUY_PRODUCT','WHEAT'])
    return result

def agent(observation,configuration=None):
    result=_R97_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step'])
        if player not in _R97_LAST or step<=_R97_LAST[player]:
            _R97_REPORT.update(supply_guard_changes=0,supply_grain_protected=0,supply_buy_units=0,supply_early_changes=0,supply_early_units=0,supply_prefund_changes=0,supply_prefund_units=0,supply_slot_declines=0,supply_capacity_declines=0,supply_budget_declines=0,supply_errors=0)
        _R97_LAST[player]=step
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)]):result=_r97_supply(observation,result)
    except Exception:_R97_REPORT['supply_errors']=_R97_REPORT.get('supply_errors',0)+1
    _R97_REPORT.update(getattr(_R97_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R97_REPORT
agent=globals().pop('agent')
