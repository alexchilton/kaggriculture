"""Take the leader's FOUR-quadrant plan when the town promises wool early, and his three otherwise.

## The branch, and why it can be a single mutation

Three top players (カワシギ, Emon xu, Yura) buy a fourth parcel and run a sheep-heavy herd when the
yarn store unlocks by d3-d6, and stay at three quadrants otherwise. `YARN_STORE` unlocks by d6 on
**15 of 100 seeds** (measured 2026-08-15, `scripts/find_the_yarn_seeds.py`, playing real agents --
the shop draw comes off the same RNG that weed spawning consumes, so a PASS-only scan reads a
stream the real game never sees).

Our shipped tape and his four-quadrant tape (`91907974`) are **the same plan through d8** and first
disagree on d9, where ours buys COW x2 and his buys SHEEP x2:

    d0-d8   both: COW 6, SHEEP 3, land on d6      identical, byte for byte
    d9      ours COW x2          his SHEEP x2     <- the split
    d11     ours COW x2          his SHEEP x2
    d12     ours -               his SHEEP x2 + LAND
    d13     ours -               his SHEEP x2
    season  ours COW 10/SHEEP 4  his COW 6/SHEEP 12, quadrants d7/d12/d13

So the trigger is readable at d6 and the first divergent action is at d9. There is nothing to
unwind, and the standing "do not regress d0-d8" rule holds by construction rather than by
measurement.

**The swap is a mutation of the row objects, not a new schedule.** `make_agent` rebuilds the outer
dict with int keys but shares the ROW objects with its caller, and reads them live every turn. So
replacing rows 9-29 in a dict we hold does nothing, and clearing and refilling each row in place
does everything.

## Routes

The shipped `solved_days.py` was solved for the 75-tile three-quadrant board.
`_apply_precomputed` keys a stop on `(tile, ops)`, so on a four-quadrant board those stops DROP
rather than adapt. `solved_days_q4.py` was solved on 2026-08-15 against this plan, armed seed 3,
covering d9-d29 for the 100-tile board, and is installed only on the branch.

## What this measured, stated plainly because it is not a win

On the 15 armed seeds, against a frozen build, with each arm on its own solved routes:

    q4 - q3   mean -$4,626   median -$3,799   sd $9,575   6/15 seeds up
    wins      q3 12/15       q4 12/15

and with both arms on live routes from d9:

    q4 - q3   mean   +$465   median +$4,553   sd $11,220  8/15 seeds up
    wins      q3 10/15       q4 12/15

Both are inside noise of zero and of each other. Run on an UNSELECTED seed set it is clearly worse
(-$2,749, 4/14 wins), which is the expected signature of a branch that should fire rarely. It is
shipped to be tried on the ladder, on Alex's call, not because it measured as a gain. The q4 routes
are solved on one seed; solving them across several armed seeds is the first thing to try if it
underperforms.
"""
import importlib

#: Switched off ships the three-quadrant plan unchanged, and is byte-identical to not importing this.
BRANCH_ON_THE_YARN_STORE = False

#: The shop whose early arrival the leaders read. Pinned against the env's own shop table below.
TRIGGER_SHOP = "YARN_STORE"

#: Read the trigger no earlier than this. The leaders' own games unlock it d3-d6.
DECIDE_BY_DAY = 6

#: The first day the two tapes disagree. Rows before it are identical, so nothing is swapped there.
SPLIT_DAY = 9

Q4_SCHEDULE = "data/seed_scripts/kawashigi_q4c/schedule.json"

#: **The rows, embedded.** A submission has no `data/` directory, so reading the JSON at
#: runtime would raise on Kaggle -- or, worse, be caught and leave the branch silently dead
#: on the 15% of games it exists for. Thinned of the tape-only keys (`plant_tiles`,
#: `build_tiles`, `land_turns`, `orders`) exactly as `build_planner_submission.TAPE_ONLY`
#: thins the shipped plan, so the branch depends on no replay it will not have.
Q4_ROWS_B64 = (
    "eyIwIjp7ImFuaW1hbHNfYm91Z2h0Ijp7IkNPVyI6MiwiU0hFRVAiOjJ9LCJidWlsZHMiOjQsImJ1eXMiOnsiV0hFQVQiOjZ9"
    "LCJjYXJlcyI6MiwiZmVlZHMiOjIsImhhbmRzIjo1LCJoaXJlcyI6NSwibGFuZCI6MCwibW9uZXlfZGF3biI6MTMuMCwicGxh"
    "Y2VzIjpbIlNIRUVQIiwiQ09XIiwiU0hFRVAiLCJDT1ciXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldI"
    "RUFUIiwiTUVMT04iLCJXSEVBVCIsIk1FTE9OIiwiTUVMT04iLCJXSEVBVCIsIk1FTE9OIiwiTUVMT04iLCJNRUxPTiIsIk1F"
    "TE9OIiwiTUVMT04iLCJNRUxPTiIsIldIRUFUIiwiTUVMT04iLCJNRUxPTiIsIk1FTE9OIl0sInNlZWRzIjp7Ik1FTE9OIjox"
    "MiwiV0hFQVQiOjd9LCJzZWxscyI6e30sInNoZWRfZHVzayI6eyJXSEVBVCI6M319LCIxIjp7ImFuaW1hbHNfYm91Z2h0Ijp7"
    "fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo1fSwiY2FyZXMiOjQsImZlZWRzIjo0LCJoYW5kcyI6MCwiaGlyZXMiOjAs"
    "ImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE2LjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsi"
    "RkVSVElMSVpFUiI6M30sInNoZWRfZHVzayI6eyJXSEVBVCI6NH19LCIxMCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxk"
    "cyI6MCwiYnV5cyI6eyJXSEVBVCI6MzR9LCJjYXJlcyI6MTIsImZlZWRzIjoxMiwiaGFuZHMiOjExLCJoaXJlcyI6MTEsImxh"
    "bmQiOjAsIm1vbmV5X2Rhd24iOjIyMjQuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJd"
    "LCJzZWVkcyI6eyJXSEVBVCI6M30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjE0MCwiTUVMT04iOjYwLCJXSEVBVCI6MjN9fSwi"
    "MTEiOnsiYW5pbWFsc19ib3VnaHQiOnsiU0hFRVAiOjJ9LCJidWlsZHMiOjIsImJ1eXMiOnsiV0hFQVQiOjE3fSwiY2FyZXMi"
    "OjE0LCJmZWVkcyI6MTQsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjoxLCJtb25leV9kYXduIjoxMzc4My4wLCJwbGFj"
    "ZXMiOlsiU0hFRVAiLCJTSEVFUCJdLCJwbGFudHMiOlsiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIldIRUFU"
    "IiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJT"
    "VFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwiV0hFQVQiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFX"
    "QkVSUlkiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJS"
    "WSIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSJdLCJzZWVkcyI6"
    "eyJTVFJBV0JFUlJZIjoyMywiV0hFQVQiOjl9LCJzZWxscyI6eyJNRUxPTiI6MTIsIk1JTEsiOjZ9fSwiMTIiOnsiYW5pbWFs"
    "c19ib3VnaHQiOnsiU0hFRVAiOjJ9LCJidWlsZHMiOjMsImJ1eXMiOnsiV0hFQVQiOjh9LCJjYXJlcyI6MTUsImZlZWRzIjox"
    "NSwiaGFuZHMiOjEwLCJoaXJlcyI6MTAsImxhbmQiOjEsIm1vbmV5X2Rhd24iOjg5MDUuMCwicGxhY2VzIjpbIlNIRUVQIl0s"
    "InBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIlNUUkFXQkVS"
    "UlkiLCJTVFJBV0JFUlJZIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjl9LCJz"
    "ZWxscyI6eyJGRVJUSUxJWkVSIjo3NCwiTUlMSyI6Nn19LCIxMyI6eyJhbmltYWxzX2JvdWdodCI6eyJTSEVFUCI6Mn0sImJ1"
    "aWxkcyI6MSwiYnV5cyI6eyJXSEVBVCI6OX0sImNhcmVzIjoxNiwiZmVlZHMiOjE2LCJoYW5kcyI6MTEsImhpcmVzIjoxMSwi"
    "bGFuZCI6MCwibW9uZXlfZGF3biI6MTIwMTEuMCwicGxhY2VzIjpbIlNIRUVQIiwiU0hFRVAiXSwicGxhbnRzIjpbIldIRUFU"
    "IiwiV0hFQVQiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6NH0sInNlbGxzIjp7IkZF"
    "UlRJTElaRVIiOjE0LCJNSUxLIjo2LCJXSEVBVCI6OCwiV09PTCI6OH19LCIxNCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1"
    "aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MjB9LCJjYXJlcyI6MTcsImZlZWRzIjoxNywiaGFuZHMiOjgsImhpcmVzIjo4LCJs"
    "YW5kIjowLCJtb25leV9kYXduIjoxMzgyNy4wLCJwbGFjZXMiOltdLCJwbGFudHMiOltdLCJzZWVkcyI6e30sInNlbGxzIjp7"
    "IkZFUlRJTElaRVIiOjE5LCJNSUxLIjo5LCJXT09MIjo2fX0sIjE1Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjow"
    "LCJidXlzIjp7IldIRUFUIjoxMH0sImNhcmVzIjoxNywiZmVlZHMiOjE3LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6"
    "MCwibW9uZXlfZGF3biI6MTU2ODUuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJz"
    "ZWVkcyI6eyJXSEVBVCI6M30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjI1MiwiTUlMSyI6NiwiV0hFQVQiOjY1LCJXT09MIjox"
    "Mn19LCIxNiI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTJ9LCJjYXJlcyI6MTgs"
    "ImZlZWRzIjoxOCwiaGFuZHMiOjksImhpcmVzIjo5LCJsYW5kIjowLCJtb25leV9kYXduIjoyNDA3Mi4wLCJwbGFjZXMiOlsi"
    "U0hFRVAiXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo0fSwi"
    "c2VsbHMiOnsiRkVSVElMSVpFUiI6MzMsIk1FTE9OIjoxMiwiTUlMSyI6MTgsIlNUUkFXQkVSUlkiOjcsIldIRUFUIjoyMCwi"
    "V09PTCI6MTR9fSwiMTciOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjEwfSwiY2Fy"
    "ZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjoyNjkzMy4wLCJw"
    "bGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJX"
    "SEVBVCI6NX0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjE3NywiTUVMT04iOjE4LCJNSUxLIjo2LCJXSEVBVCI6MTcsIldPT0wi"
    "OjE2fX0sIjE4Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo1Mn0sImNhcmVzIjox"
    "OCwiZmVlZHMiOjE4LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlfZGF3biI6MzYyODIuMCwicGxhY2Vz"
    "IjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjoyMn0sInNl"
    "bGxzIjp7IkZFUlRJTElaRVIiOjMxMywiTUVMT04iOjE4LCJNSUxLIjoxMiwiU1RSQVdCRVJSWSI6MTUsIldIRUFUIjozNywi"
    "V09PTCI6NH19LCIxOSI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTE2fSwiY2Fy"
    "ZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjo0MTQ1Ni4wLCJw"
    "bGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNl"
    "ZWRzIjp7IldIRUFUIjo2fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTEyLCJNSUxLIjo2LCJTVFJBV0JFUlJZIjo2LCJXSEVB"
    "VCI6MTI2LCJXT09MIjozN319LCIyIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjoxLCJidXlzIjp7IldIRUFUIjo0"
    "fSwiY2FyZXMiOjQsImZlZWRzIjo0LCJoYW5kcyI6NCwiaGlyZXMiOjQsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE2NC4wLCJw"
    "bGFjZXMiOltdLCJwbGFudHMiOltdLCJzZWVkcyI6e30sInNlbGxzIjp7fSwic2hlZF9kdXNrIjp7IldIRUFUIjo0fX0sIjIw"
    "Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo1MX0sImNhcmVzIjoxOCwiZmVlZHMi"
    "OjE4LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlfZGF3biI6NDQzNTguMCwicGxhY2VzIjpbXSwicGxh"
    "bnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo0fSwic2VsbHMiOnsiRkVS"
    "VElMSVpFUiI6MjUsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoxNywiV0hFQVQiOjU1LCJXT09MIjo0fX0sIjIxIjp7ImFuaW1h"
    "bHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo1NX0sImNhcmVzIjoxOCwiZmVlZHMiOjE4LCJoYW5k"
    "cyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlfZGF3biI6NDc1MDAuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldI"
    "RUFUIiwiV0hFQVQiLCJXSEVBVCIsIkNBUlJPVCIsIkNBUlJPVCIsIkNBUlJPVCJdLCJzZWVkcyI6eyJDQVJST1QiOjMsIldI"
    "RUFUIjozfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MjE5LCJNSUxLIjo2LCJTVFJBV0JFUlJZIjoyMSwiV0hFQVQiOjE1Miwi"
    "V09PTCI6MTJ9fSwiMjIiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjI3fSwiY2Fy"
    "ZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjo1MjkzOC4wLCJw"
    "bGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hF"
    "QVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo5fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MjgzLCJNSUxL"
    "IjoxMiwiU1RSQVdCRVJSWSI6MjYsIldIRUFUIjoyMDIsIldPT0wiOjE2fX0sIjIzIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwi"
    "YnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoxMzR9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6"
    "MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjU4MjQyLjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo4fSwic2Vs"
    "bHMiOnsiRkVSVElMSVpFUiI6MjUwLCJNSUxLIjo2LCJTVFJBV0JFUlJZIjoxMywiV0hFQVQiOjIxMiwiV09PTCI6MzB9fSwi"
    "MjQiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjExMX0sImNhcmVzIjoxOCwiZmVl"
    "ZHMiOjE4LCJoYW5kcyI6MTEsImhpcmVzIjoxMSwibGFuZCI6MCwibW9uZXlfZGF3biI6NjExMTcuMCwicGxhY2VzIjpbXSwi"
    "cGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiQ0FSUk9UIiwiQ0FSUk9UIiwiQ0FSUk9UIiwiV0hF"
    "QVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiQ0FSUk9UIjozLCJXSEVBVCI6OH0sInNlbGxzIjp7IkZF"
    "UlRJTElaRVIiOjE1NiwiTUlMSyI6MTIsIlNUUkFXQkVSUlkiOjMxLCJXSEVBVCI6MTUyfX0sIjI1Ijp7ImFuaW1hbHNfYm91"
    "Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo5NX0sImNhcmVzIjoxOCwiZmVlZHMiOjE4LCJoYW5kcyI6MTEs"
    "ImhpcmVzIjoxMSwibGFuZCI6MCwibW9uZXlfZGF3biI6NjU5NzUuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjE0fSwic2VsbHMiOnsiQ0FSUk9UIjo3"
    "LCJGRVJUSUxJWkVSIjoyOSwiTUlMSyI6NiwiU1RSQVdCRVJSWSI6MTAsIldIRUFUIjoxMDYsIldPT0wiOjMyfX0sIjI2Ijp7"
    "ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo1Mn0sImNhcmVzIjoxOCwiZmVlZHMiOjE4"
    "LCJoYW5kcyI6MTEsImhpcmVzIjoxMSwibGFuZCI6MCwibW9uZXlfZGF3biI6Njk2MjUuMCwicGxhY2VzIjpbXSwicGxhbnRz"
    "IjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiQ0FSUk9UIiwiV0hFQVQiXSwic2VlZHMiOnsiQ0FSUk9UIjox"
    "LCJXSEVBVCI6NX0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjI1LCJNSUxLIjoxMiwiU1RSQVdCRVJSWSI6MTgsIldIRUFUIjo3"
    "MSwiV09PTCI6OH19LCIyNyI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTB9LCJj"
    "YXJlcyI6MTMsImZlZWRzIjoxNiwiaGFuZHMiOjExLCJoaXJlcyI6MTEsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjcyNTQ0LjAs"
    "InBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJX"
    "SEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6MTB9LCJzZWxscyI6eyJGRVJUSUxJWkVS"
    "IjoxMSwiTUlMSyI6NiwiU1RSQVdCRVJSWSI6MjYsIldIRUFUIjoxMzUsIldPT0wiOjh9fSwiMjgiOnsiYW5pbWFsc19ib3Vn"
    "aHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjZ9LCJjYXJlcyI6NywiZmVlZHMiOjgsImhhbmRzIjoxMCwiaGly"
    "ZXMiOjEwLCJsYW5kIjowLCJtb25leV9kYXduIjo3ODM4My4wLCJwbGFjZXMiOltdLCJwbGFudHMiOltdLCJzZWVkcyI6e30s"
    "InNlbGxzIjp7IkNBUlJPVCI6NywiRkVSVElMSVpFUiI6MTMsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoxMCwiV0hFQVQiOjI2"
    "LCJXT09MIjoyMH19LCIyOSI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6e30sImNhcmVzIjowLCJm"
    "ZWVkcyI6MCwiaGFuZHMiOjgsImhpcmVzIjo4LCJsYW5kIjowLCJtb25leV9kYXduIjo4NTA3OC4wLCJwbGFjZXMiOltdLCJw"
    "bGFudHMiOltdLCJzZWVkcyI6e30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjYsIk1JTEsiOjE4LCJTVFJBV0JFUlJZIjoyLCJX"
    "SEVBVCI6OTAsIldPT0wiOjI4fX0sIjMiOnsiYW5pbWFsc19ib3VnaHQiOnsiQ09XIjoxfSwiYnVpbGRzIjowLCJidXlzIjp7"
    "fSwiY2FyZXMiOjQsImZlZWRzIjo0LCJoYW5kcyI6NSwiaGlyZXMiOjUsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjQyMS4wLCJw"
    "bGFjZXMiOlsiQ09XIl0sInBsYW50cyI6W10sInNlZWRzIjp7IkNBUlJPVCI6MX0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjR9"
    "LCJzaGVkX2R1c2siOnt9fSwiNCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MSwiYnV5cyI6eyJXSEVBVCI6Nn0s"
    "ImNhcmVzIjo1LCJmZWVkcyI6NSwiaGFuZHMiOjUsImhpcmVzIjo1LCJsYW5kIjowLCJtb25leV9kYXduIjoxMzEuMCwicGxh"
    "Y2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6N30sInNlbGxzIjp7"
    "IkZFUlRJTElaRVIiOjR9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjF9fSwiNSI6eyJhbmltYWxzX2JvdWdodCI6eyJDT1ciOjF9"
    "LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjJ9LCJjYXJlcyI6NiwiZmVlZHMiOjYsImhhbmRzIjo0LCJoaXJlcyI6NCwi"
    "bGFuZCI6MCwibW9uZXlfZGF3biI6MjMwLjAsInBsYWNlcyI6WyJDT1ciXSwicGxhbnRzIjpbIlNUUkFXQkVSUlkiLCJTVFJB"
    "V0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiXSwic2VlZHMiOnsiTUVMT04iOjMsIlNUUkFXQkVSUlkiOjR9LCJz"
    "ZWxscyI6eyJGRVJUSUxJWkVSIjo1LCJXSEVBVCI6MTh9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjd9fSwiNiI6eyJhbmltYWxz"
    "X2JvdWdodCI6e30sImJ1aWxkcyI6MiwiYnV5cyI6eyJXSEVBVCI6Nn0sImNhcmVzIjo2LCJmZWVkcyI6NiwiaGFuZHMiOjQs"
    "ImhpcmVzIjo0LCJsYW5kIjoxLCJtb25leV9kYXduIjoxOTYuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIk1FTE9OIiwiTUVM"
    "T04iXSwic2VlZHMiOnsiQ0FSUk9UIjo3LCJNRUxPTiI6NSwiU1RSQVdCRVJSWSI6M30sInNlbGxzIjp7IkZFUlRJTElaRVIi"
    "OjUsIldPT0wiOjEyfSwic2hlZF9kdXNrIjp7IldIRUFUIjo3fX0sIjciOnsiYW5pbWFsc19ib3VnaHQiOnsiQ09XIjoyLCJT"
    "SEVFUCI6MX0sImJ1aWxkcyI6MiwiYnV5cyI6eyJXSEVBVCI6M30sImNhcmVzIjo5LCJmZWVkcyI6OSwiaGFuZHMiOjgsImhp"
    "cmVzIjo4LCJsYW5kIjowLCJtb25leV9kYXduIjoxNDMuMCwicGxhY2VzIjpbIlNIRUVQIiwiQ09XIiwiQ09XIl0sInBsYW50"
    "cyI6WyJNRUxPTiIsIk1FTE9OIiwiTUVMT04iLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIk1FTE9OIiwiU1RSQVdCRVJS"
    "WSIsIk1FTE9OIiwiTUVMT04iXSwic2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjo2fSwic2hlZF9k"
    "dXNrIjp7fX0sIjgiOnsiYW5pbWFsc19ib3VnaHQiOnsiU0hFRVAiOjF9LCJidWlsZHMiOjIsImJ1eXMiOnsiV0hFQVQiOjE3"
    "fSwiY2FyZXMiOjEwLCJmZWVkcyI6MTAsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXduIjoxOTAu"
    "MCwicGxhY2VzIjpbIlNIRUVQIl0sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJTVFJBV0JFUlJZIiwiU1RS"
    "QVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJTVFJBV0JFUlJZ"
    "Ijo0LCJXSEVBVCI6NX0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjYsIk1JTEsiOjEyfSwic2hlZF9kdXNrIjp7IldIRUFUIjo4"
    "fX0sIjkiOnsiYW5pbWFsc19ib3VnaHQiOnsiU0hFRVAiOjJ9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjE0fSwiY2Fy"
    "ZXMiOjEyLCJmZWVkcyI6MTIsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjo5NDMuMCwicGxh"
    "Y2VzIjpbIlNIRUVQIiwiU0hFRVAiXSwicGxhbnRzIjpbXSwic2VlZHMiOnt9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjo5LCJX"
    "SEVBVCI6NSwiV09PTCI6OH19fQ=="
)


def the_town_promised_wool_early(observation):
    """True when the yarn store is already unlocked.

    `observation["town"]["unlocked_shops"]` is the shop list -- NOT `observation["shops"]`, which
    does not exist and which silently produced all-zero drain tables over 5,376 games.
    """
    town = (observation or {}).get("town") or {}
    return TRIGGER_SHOP in (town.get("unlocked_shops") or [])


def _q4_rows():
    """The four-quadrant rows, from the embedded copy. Never touches the filesystem.

    Base64 rather than a raw literal because `build_planner_submission` embeds every module inside
    a raw triple-quoted literal and refuses any source containing that same delimiter.
    """
    import base64
    import json

    return {int(k): v for k, v in json.loads(base64.b64decode(Q4_ROWS_B64)).items()}


def install_the_fourth_quadrant(schedule):
    """Rewrite rows `SPLIT_DAY`..29 of `schedule` IN PLACE, and install the 100-tile routes.

    In place because `make_agent` shares row objects with its caller and reads them live each turn.
    Rebinding a row would be a no-op that looks exactly like a working branch -- the failure mode
    this project calls a byte-identical null.
    """
    rows = _q4_rows()
    for day, row in rows.items():
        if day < SPLIT_DAY:
            continue
        target = schedule.get(day) if hasattr(schedule, "get") else None
        if target is None:
            continue
        target.clear()
        target.update(row)

    cover = importlib.import_module("kagg.search.cover")
    q4 = importlib.import_module("kagg.search.solved_days_q4")
    cover.UNSOLVE_DAYS = ()
    cover.PRECOMPUTED_ROUTES = {d: {u: [(tuple(t), tuple(ops)) for t, ops in seq]
                                    for u, seq in units.items()}
                                for d, units in q4.SOLVED_DAYS.items()}
    return True


def arm(schedule, state, observation, day):
    """Decide once, on or after `DECIDE_BY_DAY`, and before `SPLIT_DAY` can act.

    `state` is any dict that persists across turns; the decision is recorded there so the schedule is
    never mutated twice and never re-read after the split.
    """
    if not BRANCH_ON_THE_YARN_STORE or state.get("q4_decided"):
        return state.get("q4_armed", False)
    if day < DECIDE_BY_DAY:
        return False
    state["q4_decided"] = True
    state["q4_armed"] = bool(the_town_promised_wool_early(observation))
    if state["q4_armed"]:
        install_the_fourth_quadrant(schedule)
    return state["q4_armed"]
