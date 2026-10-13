"""The leader's OTHER branch: when the opponent commits to melon, he stops buying it.

## What this is, in one sentence

`data/seed_scripts/kawashigi/schedule.json` is his MELON season (92498144, $149,998, MELON 20 /
STRAWBERRY 11 at d9). This module carries his STRAWBERRY season (92466371, $147,059, MELON 12 /
STRAWBERRY 19 at d9) and installs it when the trigger fires. Both are three-quadrant games of his.

## The trigger, measured rather than guessed

Across 67 of his games his melon count at d9 is BIMODAL -- 12 or 20, never between -- and
`melon + strawberry` is 31 in every single one. The switch is the OPPONENT'S melon tile count at
day 3:

    opponent melon >= 9   ->  he holds 12 melon / 19 strawberry     15 games
    opponent melon <  9   ->  he holds 20 melon / 11 strawberry     52 games

Zero misclassifications in 67 games. Day 3 is readable: the earliest melon harvest is day 10, so a
melon tile at d3 is a PLANTED tile and is on the board for anyone to count.

`docs/allocation_bounds_pass2_2026-08-16.md` derives the same structure without being told it:
best response to a melon-flooding opponent is 7-12 tiles, to a low-melon opponent 14-27, and the
best-response fixed point is ~12-14. Melon is demand-capped at 188 units a season and he alone
sells 120.

## Why this REPLACES a token rewrite rather than extending one

The previous implementation rewrote `MELON` to `STRAWBERRY` inside the melon schedule's own rows.
Measured over 24 games against the frozen opponent: **0.0 per cent win rate against 66.7 with the
swap off**, -$17,297 a game. The cause is in the reference. MELON is `ongoing: False` -- water it to
day 10-12, harvest once, the tile is spent. STRAWBERRY is `ongoing: True` and must be watered every
day to the end of the season or it weeds. A row recorded for melon hands a strawberry tile melon's
maintenance, so the tiles die. Rewriting the token cannot fix that; only playing the season he
actually recorded for that board can.

## What differs, d3 to d8 -- the whole decision

    d3   seeds    {CARROT: 1}                          ->  {}
    d5   seeds    {STRAWBERRY: 4, MELON: 3}            ->  {STRAWBERRY: 4}
    d6   plants   {MELON: 2}                           ->  {STRAWBERRY: 2}
         seeds    {STRAWBERRY: 3, MELON: 5, CARROT: 7} ->  {STRAWBERRY: 3, CARROT: 8}
    d7   plants   {MELON: 6, STRAWBERRY: 3}            ->  {STRAWBERRY: 2}
         seeds    {WHEAT: 4}                           ->  {STRAWBERRY: 1, WHEAT: 4}
         animals  {COW: 2, SHEEP: 1}                   ->  {COW: 2, SHEEP: 2}
    d8   plants   {WHEAT: 5, STRAWBERRY: 4}            ->  {WHEAT: 3, STRAWBERRY: 11}
         seeds    {WHEAT: 5, STRAWBERRY: 4}            ->  {STRAWBERRY: 11, WHEAT: 3}
         animals  {SHEEP: 1}                           ->  {}

He buys 8 melon seed after d0 -- 3 on d5, 5 on d6 -- and plants them on d6 and d7, which is how 12
becomes 20. The strawberry branch buys none. Everything from d9 on differs only as downstream
drift: different money, therefore different sells. It is not a second decision.

`SPLIT_DAY` is 3, the day the decision is read. It was 5 -- the first row either season spends
melon money on -- which left A3's `d3 seeds {CARROT: 1}` in place against B3's `{}`.

## Embedded, not read from disk

Same reason as `q4_branch.Q4_ROWS_B64`: a submission is one file. The blob holds only the fields the
agent is driven by; `breakdown.TAPE_ONLY` and `shed_dusk` are stripped, so the branch depends on no
replay it will not have.

Rows are cleared and refilled IN PLACE. `make_agent` shallow-copies the outer dict but shares every
row object with its caller, so rebinding a row would be a no-op that looks exactly like a working
branch -- the failure this project calls a byte-identical null.
"""
import base64
import json

from .branch import Branch, count_tiles, opponent_seat

#: The day the decision is READ. The opponent's melon tiles are visible from d0; d3 is the first day
#: at which his commitment is settled, and it is two days before the first row that spends on melon.
DECIDE_BY_DAY = 3

#: Opponent MELON tiles at `DECIDE_BY_DAY` at or above which the strawberry season is installed.
#: Separates his own two populations with zero errors across 67 games.
OPPONENT_MELON = 9

#: The first day whose row is replaced.
#:
#: This was 5, on the argument that d3 and d4 carry no melon in either season. That is true of
#: melon and false of the row: A3's d3 is `seeds {CARROT: 1}` and B3's is `{}`, so installing from
#: 5 left a carrot seed the strawberry season does not buy. It showed as `BUY_SEED 1/0` at d3 and
#: as a bank that diverged from his three days before any field action did -- `money 9/28` at d3,
#: still 9/19 at d7. Dropping it is worth nothing on its own (measured +$20 in the melon arm over
#: a full season, every op row identical), but the row has to be his or the comparison is not one.
SPLIT_DAY = 3

#: Where the rows came from, for anyone re-deriving the blob.
SOURCE_REPLAY = "data/seed_scripts/kawashigi/92466371.json"
SOURCE_SCHEDULE = "data/seed_scripts/kawashigi_b3/schedule.json"

B3_ROWS_B64 = (
    "eyIxMCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6NDB9LCJjYXJlcyI6MTIsImZl"
    "ZWRzIjoxMiwiaGFuZHMiOjExLCJoaXJlcyI6MTEsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjIwNDMuMCwicGxhY2VzIjpbXSwi"
    "cGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo0fSwic2VsbHMiOnsi"
    "RkVSVElMSVpFUiI6MTQ1LCJNRUxPTiI6NjYsIldIRUFUIjozMH19LCIxMSI6eyJhbmltYWxzX2JvdWdodCI6eyJDT1ciOjJ9"
    "LCJidWlsZHMiOjIsImJ1eXMiOnsiV0hFQVQiOjE2fSwiY2FyZXMiOjE0LCJmZWVkcyI6MTQsImhhbmRzIjoxMiwiaGlyZXMi"
    "OjEyLCJsYW5kIjoxLCJtb25leV9kYXduIjoxMjY0My4wLCJwbGFjZXMiOlsiQ09XIiwiQ09XIl0sInBsYW50cyI6WyJTVFJB"
    "V0JFUlJZIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwiV0hFQVQiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwi"
    "V0hFQVQiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIs"
    "IldIRUFUIiwiV0hFQVQiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIldIRUFUIiwi"
    "U1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JF"
    "UlJZIl0sInNlZWRzIjp7IlNUUkFXQkVSUlkiOjIzLCJXSEVBVCI6OH0sInNlbGxzIjp7Ik1FTE9OIjo2LCJNSUxLIjo2fX0s"
    "IjEyIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo5fSwiY2FyZXMiOjE0LCJmZWVk"
    "cyI6MTQsImhhbmRzIjoxMCwiaGlyZXMiOjEwLCJsYW5kIjowLCJtb25leV9kYXduIjoxNDE3MC4wLCJwbGFjZXMiOltdLCJw"
    "bGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIlNUUkFXQkVSUlkiXSwic2VlZHMiOnsiV0hF"
    "QVQiOjN9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyOCwiTUlMSyI6Nn19LCIxMyI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1"
    "aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6OH0sImNhcmVzIjoxNCwiZmVlZHMiOjE0LCJoYW5kcyI6MTEsImhpcmVzIjoxMSwi"
    "bGFuZCI6MCwibW9uZXlfZGF3biI6MTcwMzIuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIlNUUkFXQkVSUlkiLCJTVFJBV0JF"
    "UlJZIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6M30sInNlbGxzIjp7"
    "IkZFUlRJTElaRVIiOjEzLCJNSUxLIjo2LCJXSEVBVCI6NSwiV09PTCI6OH19LCIxNCI6eyJhbmltYWxzX2JvdWdodCI6e30s"
    "ImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6OH0sImNhcmVzIjoxNCwiZmVlZHMiOjE0LCJoYW5kcyI6OCwiaGlyZXMiOjgs"
    "ImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE5NjI5LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIl0sInNl"
    "ZWRzIjp7IldIRUFUIjoyfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTIsIk1JTEsiOjksIldIRUFUIjoxLCJXT09MIjo2fX0s"
    "IjE1Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo4fSwiY2FyZXMiOjE0LCJmZWVk"
    "cyI6MTQsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjoyMjA3Ny4wLCJwbGFjZXMiOltdLCJw"
    "bGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJG"
    "RVJUSUxJWkVSIjoyNDksIk1JTEsiOjE4LCJXSEVBVCI6MzEsIldPT0wiOjZ9fSwiMTYiOnsiYW5pbWFsc19ib3VnaHQiOnt9"
    "LCJidWlsZHMiOjAsImJ1eXMiOnt9LCJjYXJlcyI6MTQsImZlZWRzIjoxNCwiaGFuZHMiOjksImhpcmVzIjo5LCJsYW5kIjow"
    "LCJtb25leV9kYXduIjoyOTg5My4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hF"
    "QVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6OH0sInNlbGxzIjp7IkZFUlRJ"
    "TElaRVIiOjI4LCJNSUxLIjo2LCJTVFJBV0JFUlJZIjo4LCJXSEVBVCI6OX19LCIxNyI6eyJhbmltYWxzX2JvdWdodCI6e30s"
    "ImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6NDJ9LCJjYXJlcyI6MTQsImZlZWRzIjoxNCwiaGFuZHMiOjEyLCJoaXJlcyI6"
    "MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjMyMDY0LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MzE2LCJN"
    "SUxLIjo2LCJTVFJBV0JFUlJZIjo0LCJXSEVBVCI6NDMsIldPT0wiOjN9fSwiMTgiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJi"
    "dWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjE4fSwiY2FyZXMiOjE0LCJmZWVkcyI6MTQsImhhbmRzIjoxMiwiaGlyZXMiOjEy"
    "LCJsYW5kIjowLCJtb25leV9kYXduIjo0MDY3NC4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldI"
    "RUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyNjQsIk1JTEsiOjI0LCJT"
    "VFJBV0JFUlJZIjoxMiwiV0hFQVQiOjExfX0sIjE5Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7"
    "IldIRUFUIjo2MX0sImNhcmVzIjoxNCwiZmVlZHMiOjE0LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlf"
    "ZGF3biI6NDc2NTIuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hF"
    "QVQiXSwic2VlZHMiOnsiV0hFQVQiOjV9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjozNTYsIk1JTEsiOjYsIlNUUkFXQkVSUlki"
    "OjIyLCJXSEVBVCI6NTIsIldPT0wiOjIwfX0sIjIwIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7"
    "IldIRUFUIjo4fSwiY2FyZXMiOjE0LCJmZWVkcyI6MTQsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9k"
    "YXduIjo1NjQ2NC4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVB"
    "VCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjd9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoxNTAsIk1JTEsi"
    "OjMwLCJTVFJBV0JFUlJZIjoxMiwiV0hFQVQiOjE1fX0sIjIxIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJi"
    "dXlzIjp7IldIRUFUIjozNH0sImNhcmVzIjoxNCwiZmVlZHMiOjE0LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwi"
    "bW9uZXlfZGF3biI6NjQ2MDUuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJDQVJST1QiXSwic2Vl"
    "ZHMiOnsiQ0FSUk9UIjoxLCJXSEVBVCI6Mn0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjI5MiwiTUlMSyI6NiwiU1RSQVdCRVJS"
    "WSI6NDksIldIRUFUIjo1OCwiV09PTCI6OX19LCIyMiI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6"
    "eyJXSEVBVCI6OH0sImNhcmVzIjoxNCwiZmVlZHMiOjE0LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlf"
    "ZGF3biI6Nzg1NDguMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hF"
    "QVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIkNBUlJPVCJdLCJzZWVkcyI6eyJDQVJST1QiOjEsIldIRUFU"
    "Ijo5fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTYxLCJNSUxLIjoyNCwiU1RSQVdCRVJSWSI6MjAsIldIRUFUIjo3fX0sIjIz"
    "Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjozNH0sImNhcmVzIjoxNCwiZmVlZHMi"
    "OjE0LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlfZGF3biI6ODY0NTcuMCwicGxhY2VzIjpbXSwicGxh"
    "bnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6"
    "Nn0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjI4MSwiTUlMSyI6NiwiU1RSQVdCRVJSWSI6NDAsIldIRUFUIjo0NCwiV09PTCI6"
    "MTJ9fSwiMjQiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjh9LCJjYXJlcyI6MTQs"
    "ImZlZWRzIjoxNCwiaGFuZHMiOjExLCJoaXJlcyI6MTEsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjk5MjA0LjAsInBsYWNlcyI6"
    "W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIkNBUlJPVCIsIldIRUFUIl0sInNlZWRzIjp7"
    "IkNBUlJPVCI6MSwiV0hFQVQiOjV9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjozNSwiTUlMSyI6MjQsIlNUUkFXQkVSUlkiOjI3"
    "LCJXSEVBVCI6NjMsIldPT0wiOjR9fSwiMjUiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hF"
    "QVQiOjYzfSwiY2FyZXMiOjE0LCJmZWVkcyI6MTQsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXdu"
    "IjoxMDY1NjIuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQi"
    "LCJXSEVBVCIsIldIRUFUIiwiQ0FSUk9UIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiQ0FS"
    "Uk9UIjoxLCJXSEVBVCI6MTF9LCJzZWxscyI6eyJDQVJST1QiOjIsIkZFUlRJTElaRVIiOjI1OCwiTUlMSyI6NiwiU1RSQVdC"
    "RVJSWSI6MzIsIldIRUFUIjoxMzksIldPT0wiOjh9fSwiMjYiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1"
    "eXMiOnsiV0hFQVQiOjIwfSwiY2FyZXMiOjE0LCJmZWVkcyI6MTQsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJt"
    "b25leV9kYXduIjoxMTg4MTQuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFU"
    "IiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIkNBUlJPVCIsIldIRUFUIiwiV0hFQVQiXSwic2Vl"
    "ZHMiOnsiQ0FSUk9UIjoxLCJXSEVBVCI6MTF9LCJzZWxscyI6eyJDQVJST1QiOjIsIkZFUlRJTElaRVIiOjcsIk1JTEsiOjI0"
    "LCJTVFJBV0JFUlJZIjo1LCJXSEVBVCI6NTF9fSwiMjciOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMi"
    "OnsiV0hFQVQiOjMwfSwiY2FyZXMiOjEyLCJmZWVkcyI6MTQsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25l"
    "eV9kYXduIjoxMjAxOTIuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6"
    "eyJXSEVBVCI6MTJ9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyMSwiTUlMSyI6NiwiU1RSQVdCRVJSWSI6MjQsIldIRUFUIjox"
    "MTgsIldPT0wiOjh9fSwiMjgiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjd9LCJj"
    "YXJlcyI6OSwiZmVlZHMiOjEwLCJoYW5kcyI6MTAsImhpcmVzIjoxMCwibGFuZCI6MCwibW9uZXlfZGF3biI6MTM0NzI5LjAs"
    "InBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiQ0FSUk9UIjozLCJGRVJUSUxJWkVSIjoxMiwi"
    "TUlMSyI6MjQsIlNUUkFXQkVSUlkiOjgsIldIRUFUIjoyMiwiV09PTCI6OH19LCIyOSI6eyJhbmltYWxzX2JvdWdodCI6e30s"
    "ImJ1aWxkcyI6MCwiYnV5cyI6e30sImNhcmVzIjowLCJmZWVkcyI6MCwiaGFuZHMiOjgsImhpcmVzIjo4LCJsYW5kIjowLCJt"
    "b25leV9kYXduIjoxMzk1MDguMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbXSwic2VlZHMiOnt9LCJzZWxscyI6eyJDQVJST1Qi"
    "OjUsIkZFUlRJTElaRVIiOjksIk1JTEsiOjMwLCJTVFJBV0JFUlJZIjoyLCJXSEVBVCI6MTAyLCJXT09MIjo4fX0sIjMiOnsi"
    "YW5pbWFsc19ib3VnaHQiOnsiQ09XIjoxfSwiYnVpbGRzIjowLCJidXlzIjp7fSwiY2FyZXMiOjQsImZlZWRzIjo0LCJoYW5k"
    "cyI6NSwiaGlyZXMiOjUsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjM4LjAsInBsYWNlcyI6WyJDT1ciXSwicGxhbnRzIjpbXSwi"
    "c2VlZHMiOnt9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjo0fX0sIjQiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjEs"
    "ImJ1eXMiOnsiV0hFQVQiOjZ9LCJjYXJlcyI6NSwiZmVlZHMiOjUsImhhbmRzIjo1LCJoaXJlcyI6NSwibGFuZCI6MCwibW9u"
    "ZXlfZGF3biI6MTQyLjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsi"
    "V0hFQVQiOjd9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjo0fX0sIjUiOnsiYW5pbWFsc19ib3VnaHQiOnsiQ09XIjoxfSwiYnVp"
    "bGRzIjowLCJidXlzIjp7IldIRUFUIjoyfSwiY2FyZXMiOjYsImZlZWRzIjo2LCJoYW5kcyI6NCwiaGlyZXMiOjQsImxhbmQi"
    "OjAsIm1vbmV5X2Rhd24iOjI1My4wLCJwbGFjZXMiOlsiQ09XIl0sInBsYW50cyI6WyJTVFJBV0JFUlJZIiwiU1RSQVdCRVJS"
    "WSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIl0sInNlZWRzIjp7IlNUUkFXQkVSUlkiOjR9LCJzZWxscyI6eyJGRVJUSUxJ"
    "WkVSIjo1LCJXSEVBVCI6MTh9fSwiNiI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MiwiYnV5cyI6eyJXSEVBVCI6"
    "Nn0sImNhcmVzIjo2LCJmZWVkcyI6NiwiaGFuZHMiOjQsImhpcmVzIjo0LCJsYW5kIjoxLCJtb25leV9kYXduIjo0NDYuMCwi"
    "cGxhY2VzIjpbXSwicGxhbnRzIjpbIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIl0sInNlZWRzIjp7IkNBUlJPVCI6OCwiU1RS"
    "QVdCRVJSWSI6M30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjUsIldPT0wiOjEyfX0sIjciOnsiYW5pbWFsc19ib3VnaHQiOnsi"
    "Q09XIjoyLCJTSEVFUCI6Mn0sImJ1aWxkcyI6MiwiYnV5cyI6eyJXSEVBVCI6M30sImNhcmVzIjo5LCJmZWVkcyI6OSwiaGFu"
    "ZHMiOjgsImhpcmVzIjo4LCJsYW5kIjowLCJtb25leV9kYXduIjoxNTQuMCwicGxhY2VzIjpbIlNIRUVQIiwiQ09XIiwiQ09X"
    "Il0sInBsYW50cyI6WyJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSJdLCJzZWVkcyI6eyJTVFJBV0JFUlJZIjoxLCJXSEVBVCI6"
    "NH0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjZ9fSwiOCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MiwiYnV5cyI6"
    "eyJXSEVBVCI6MTd9LCJjYXJlcyI6MTAsImZlZWRzIjoxMCwiaGFuZHMiOjExLCJoaXJlcyI6MTEsImxhbmQiOjAsIm1vbmV5"
    "X2Rhd24iOjEzNi4wLCJwbGFjZXMiOlsiU0hFRVAiXSwicGxhbnRzIjpbIldIRUFUIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwi"
    "V0hFQVQiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIs"
    "IlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIl0sInNlZWRz"
    "Ijp7IlNUUkFXQkVSUlkiOjExLCJXSEVBVCI6M30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjYsIk1JTEsiOjEyfX0sIjkiOnsi"
    "YW5pbWFsc19ib3VnaHQiOnsiQ09XIjoyfSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoxMn0sImNhcmVzIjoxMSwiZmVl"
    "ZHMiOjExLCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlfZGF3biI6MTE5NC4wLCJwbGFjZXMiOlsiQ09X"
    "IiwiQ09XIl0sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjoyfSwic2VsbHMiOnsiRkVSVElM"
    "SVpFUiI6OSwiV0hFQVQiOjgsIldPT0wiOjh9fX0="
)


class MelonBranch(Branch):
    """His strawberry season, taken when the opponent has committed to melon."""

    decide_by_day = DECIDE_BY_DAY
    split_day = SPLIT_DAY
    decided_key = "melon_decided"
    armed_key = "melon_armed"

    def trigger(self, observation):
        """The opponent holds `OPPONENT_MELON` or more MELON tiles.

        Counts TILES rather than harvests: the earliest melon yield is day 10 and the decision is
        taken on day 3, so what is visible then is what has been planted.
        """
        return count_tiles(observation, opponent_seat(observation),
                           crop="MELON") >= OPPONENT_MELON

    #: The three-quadrant solve for the strawberry season. `cover` loads `solved_days` at import,
    #: which was solved on the MELON board; a route is keyed on `(tile, ops)` and this branch puts
    #: different crops on different tiles from d5, so those stops drop rather than adapt and the
    #: strawberry season plays d12-d29 effectively unsolved. Same failure `q4_branch` documents for
    #: 75 tiles against 100, one board over.
    SOLVE_FOR_STRAWBERRY = "kagg.search.solved_days_straw"

    def rows(self):
        return {int(d): r for d, r in json.loads(base64.b64decode(B3_ROWS_B64)).items()}

    def install(self, schedule, state=None):
        moved = super().install(schedule, state)
        import importlib
        cover = importlib.import_module("kagg.search.cover")
        try:
            straw = importlib.import_module(self.SOLVE_FOR_STRAWBERRY)
        except ImportError:
            # Not solved yet. Leaving `cover`'s melon routes in place is what shipped before, and
            # the mismatched stops drop silently -- which is the whole reason this solve is owed.
            return moved
        cover.PRECOMPUTED_ROUTES = {d: {u: [(tuple(tile), tuple(ops)) for tile, ops in seq]
                                        for u, seq in units.items()}
                                    for d, units in straw.SOLVED_DAYS.items()
                                    if d not in cover.UNSOLVE_DAYS}
        return moved


BRANCH = MelonBranch()

the_opponent_committed_to_melon = BRANCH.trigger
install_the_strawberry_branch = BRANCH.install
arm = BRANCH.arm
