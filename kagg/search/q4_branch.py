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
BRANCH_ON_THE_YARN_STORE = True

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
    "eyIwIjp7ImFuaW1hbHNfYm91Z2h0Ijp7IkNPVyI6MiwiU0hFRVAiOjJ9LCJidWlsZHMiOjQsImJ1eXMiOnsiV0hFQV"
    "QiOjZ9LCJjYXJlcyI6MiwiZmVlZHMiOjIsImhhbmRzIjo1LCJoaXJlcyI6NSwibGFuZCI6MCwibW9uZXlfZGF3biI6"
    "MTMuMCwicGxhY2VzIjpbIlNIRUVQIiwiQ09XIiwiU0hFRVAiLCJDT1ciXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQV"
    "QiLCJXSEVBVCIsIldIRUFUIiwiTUVMT04iLCJXSEVBVCIsIk1FTE9OIiwiTUVMT04iLCJXSEVBVCIsIk1FTE9OIiwi"
    "TUVMT04iLCJNRUxPTiIsIk1FTE9OIiwiTUVMT04iLCJNRUxPTiIsIldIRUFUIiwiTUVMT04iLCJNRUxPTiIsIk1FTE"
    "9OIl0sInNlZWRzIjp7Ik1FTE9OIjoxMiwiV0hFQVQiOjd9LCJzZWxscyI6e30sInNoZWRfZHVzayI6eyJXSEVBVCI6"
    "M319LCIxIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo1fSwiY2FyZXMiOj"
    "QsImZlZWRzIjo0LCJoYW5kcyI6MCwiaGlyZXMiOjAsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE2LjAsInBsYWNlcyI6"
    "W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6M30sInNoZWRfZHVzayI6eyJXSE"
    "VBVCI6NH19LCIxMCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MzR9LCJj"
    "YXJlcyI6MTIsImZlZWRzIjoxMiwiaGFuZHMiOjExLCJoaXJlcyI6MTEsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjIyMj"
    "QuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6"
    "M30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjE0MCwiTUVMT04iOjYwLCJXSEVBVCI6MjN9fSwiMTEiOnsiYW5pbWFsc1"
    "9ib3VnaHQiOnsiU0hFRVAiOjJ9LCJidWlsZHMiOjIsImJ1eXMiOnsiV0hFQVQiOjE3fSwiY2FyZXMiOjE0LCJmZWVk"
    "cyI6MTQsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjoxLCJtb25leV9kYXduIjoxMzc4My4wLCJwbGFjZXMiOl"
    "siU0hFRVAiLCJTSEVFUCJdLCJwbGFudHMiOlsiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIldIRUFU"
    "IiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUl"
    "kiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwiV0hFQVQiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJS"
    "WSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUl"
    "JZIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RS"
    "QVdCRVJSWSJdLCJzZWVkcyI6eyJTVFJBV0JFUlJZIjoyMywiV0hFQVQiOjl9LCJzZWxscyI6eyJNRUxPTiI6MTIsIk"
    "1JTEsiOjZ9fSwiMTIiOnsiYW5pbWFsc19ib3VnaHQiOnsiU0hFRVAiOjJ9LCJidWlsZHMiOjMsImJ1eXMiOnsiV0hF"
    "QVQiOjh9LCJjYXJlcyI6MTUsImZlZWRzIjoxNSwiaGFuZHMiOjEwLCJoaXJlcyI6MTAsImxhbmQiOjEsIm1vbmV5X2"
    "Rhd24iOjg5MDUuMCwicGxhY2VzIjpbIlNIRUVQIiwiU0hFRVAiXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJX"
    "SEVBVCIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVC"
    "IsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6OX0sInNlbGxzIjp7IkZFUlRJTElaRVIi"
    "Ojc0LCJNSUxLIjo2fX0sIjEzIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIj"
    "o5fSwiY2FyZXMiOjE2LCJmZWVkcyI6MTYsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXdu"
    "IjoxMjAxMS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiU1RSQVdCRVJSWS"
    "IsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo0fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTQsIk1JTEsiOjYsIldI"
    "RUFUIjo4LCJXT09MIjo4fX0sIjE0Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRU"
    "FUIjoyMH0sImNhcmVzIjoxNywiZmVlZHMiOjE3LCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbmQiOjAsIm1vbmV5X2Rh"
    "d24iOjEzODI3LjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiRkVSVElMSVpFUi"
    "I6MTksIk1JTEsiOjksIldPT0wiOjZ9fSwiMTUiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMi"
    "OnsiV0hFQVQiOjEwfSwiY2FyZXMiOjE3LCJmZWVkcyI6MTcsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLC"
    "Jtb25leV9kYXduIjoxNTY4NS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0s"
    "InNlZWRzIjp7IldIRUFUIjozfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MjUyLCJNSUxLIjo2LCJXSEVBVCI6NjUsIl"
    "dPT0wiOjEyfX0sIjE2Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoxMn0s"
    "ImNhcmVzIjoxOCwiZmVlZHMiOjE4LCJoYW5kcyI6OSwiaGlyZXMiOjksImxhbmQiOjAsIm1vbmV5X2Rhd24iOjI0MD"
    "cyLjAsInBsYWNlcyI6WyJTSEVFUCJdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwi"
    "c2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjozMywiTUVMT04iOjEyLCJNSUxLIjoxOCwiU1"
    "RSQVdCRVJSWSI6NywiV0hFQVQiOjIwLCJXT09MIjoxNH19LCIxNyI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxk"
    "cyI6MCwiYnV5cyI6eyJXSEVBVCI6MTB9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6MT"
    "IsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjI2OTMzLjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFU"
    "IiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo1fSwic2VsbHMiOnsiRkVSVElMSVpFUi"
    "I6MTc3LCJNRUxPTiI6MTgsIk1JTEsiOjYsIldIRUFUIjoxNywiV09PTCI6MTZ9fSwiMTgiOnsiYW5pbWFsc19ib3Vn"
    "aHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjUyfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIj"
    "oxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjozNjI4Mi4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRU"
    "FUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIs"
    "IldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjIyfSwic2VsbH"
    "MiOnsiRkVSVElMSVpFUiI6MzEzLCJNRUxPTiI6MTgsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoxNSwiV0hFQVQiOjM3"
    "LCJXT09MIjo0fX0sIjE5Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoxMT"
    "Z9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24i"
    "OjQxNDU2LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRU"
    "FUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjZ9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoxMTIsIk1JTEsiOjYs"
    "IlNUUkFXQkVSUlkiOjYsIldIRUFUIjoxMjYsIldPT0wiOjM3fX0sIjIiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidW"
    "lsZHMiOjEsImJ1eXMiOnsiV0hFQVQiOjR9LCJjYXJlcyI6NCwiZmVlZHMiOjQsImhhbmRzIjo0LCJoaXJlcyI6NCwi"
    "bGFuZCI6MCwibW9uZXlfZGF3biI6MTY0LjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbH"
    "MiOnt9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjR9fSwiMjAiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAs"
    "ImJ1eXMiOnsiV0hFQVQiOjUxfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW"
    "5kIjowLCJtb25leV9kYXduIjo0NDM1OC4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldI"
    "RUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyNSwiTUlMSyI6MT"
    "IsIlNUUkFXQkVSUlkiOjE3LCJXSEVBVCI6NTUsIldPT0wiOjR9fSwiMjEiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJi"
    "dWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjU1fSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZX"
    "MiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjo0NzUwMC4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJX"
    "SEVBVCIsIldIRUFUIiwiQ0FSUk9UIiwiQ0FSUk9UIiwiQ0FSUk9UIl0sInNlZWRzIjp7IkNBUlJPVCI6MywiV0hFQV"
    "QiOjN9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyMTksIk1JTEsiOjYsIlNUUkFXQkVSUlkiOjIxLCJXSEVBVCI6MTUy"
    "LCJXT09MIjoxMn19LCIyMiI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Mj"
    "d9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24i"
    "OjUyOTM4LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRU"
    "FUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjl9LCJzZWxscyI6eyJG"
    "RVJUSUxJWkVSIjoyODMsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoyNiwiV0hFQVQiOjIwMiwiV09PTCI6MTZ9fSwiMj"
    "MiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjEzNH0sImNhcmVzIjoxOCwi"
    "ZmVlZHMiOjE4LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlfZGF3biI6NTgyNDIuMCwicGxhY2"
    "VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldI"
    "RUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjh9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyNTAsIk1JTEsiOj"
    "YsIlNUUkFXQkVSUlkiOjEzLCJXSEVBVCI6MjEyLCJXT09MIjozMH19LCIyNCI6eyJhbmltYWxzX2JvdWdodCI6e30s"
    "ImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTExfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMSwiaG"
    "lyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXduIjo2MTExNy4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQi"
    "LCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJDQVJST1QiLCJDQVJST1QiLCJDQVJST1QiLCJXSEVBVCIsIldIRUFUIi"
    "wiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJDQVJST1QiOjMsIldIRUFUIjo4fSwic2VsbHMiOnsiRkVSVElMSVpF"
    "UiI6MTU2LCJNSUxLIjoxMiwiU1RSQVdCRVJSWSI6MzEsIldIRUFUIjoxNTJ9fSwiMjUiOnsiYW5pbWFsc19ib3VnaH"
    "QiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjk1fSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjox"
    "MSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXduIjo2NTk3NS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0"
    "hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFU"
    "IiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6MTR9LCJzZW"
    "xscyI6eyJDQVJST1QiOjcsIkZFUlRJTElaRVIiOjI5LCJNSUxLIjo2LCJTVFJBV0JFUlJZIjoxMCwiV0hFQVQiOjEw"
    "NiwiV09PTCI6MzJ9fSwiMjYiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOj"
    "UyfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXdu"
    "Ijo2OTYyNS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJDQV"
    "JST1QiLCJXSEVBVCJdLCJzZWVkcyI6eyJDQVJST1QiOjEsIldIRUFUIjo1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6"
    "MjUsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoxOCwiV0hFQVQiOjcxLCJXT09MIjo4fX0sIjI3Ijp7ImFuaW1hbHNfYm"
    "91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoxMH0sImNhcmVzIjoxMywiZmVlZHMiOjE2LCJoYW5k"
    "cyI6MTEsImhpcmVzIjoxMSwibGFuZCI6MCwibW9uZXlfZGF3biI6NzI1NDQuMCwicGxhY2VzIjpbXSwicGxhbnRzIj"
    "pbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJX"
    "SEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjoxMH0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjExLCJNSUxLIj"
    "o2LCJTVFJBV0JFUlJZIjoyNiwiV0hFQVQiOjEzNSwiV09PTCI6OH19LCIyOCI6eyJhbmltYWxzX2JvdWdodCI6e30s"
    "ImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Nn0sImNhcmVzIjo3LCJmZWVkcyI6OCwiaGFuZHMiOjEwLCJoaXJlcy"
    "I6MTAsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjc4MzgzLjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7"
    "fSwic2VsbHMiOnsiQ0FSUk9UIjo3LCJGRVJUSUxJWkVSIjoxMywiTUlMSyI6MTIsIlNUUkFXQkVSUlkiOjEwLCJXSE"
    "VBVCI6MjYsIldPT0wiOjIwfX0sIjI5Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7fSwi"
    "Y2FyZXMiOjAsImZlZWRzIjowLCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjg1MDc4Lj"
    "AsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NiwiTUlMSyI6"
    "MTgsIlNUUkFXQkVSUlkiOjIsIldIRUFUIjo5MCwiV09PTCI6Mjh9fSwiMyI6eyJhbmltYWxzX2JvdWdodCI6eyJDT1"
    "ciOjF9LCJidWlsZHMiOjAsImJ1eXMiOnt9LCJjYXJlcyI6NCwiZmVlZHMiOjQsImhhbmRzIjo1LCJoaXJlcyI6NSwi"
    "bGFuZCI6MCwibW9uZXlfZGF3biI6NDIxLjAsInBsYWNlcyI6WyJDT1ciXSwicGxhbnRzIjpbXSwic2VlZHMiOnsiQ0"
    "FSUk9UIjoxfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NH0sInNoZWRfZHVzayI6e319LCI0Ijp7ImFuaW1hbHNfYm91"
    "Z2h0Ijp7fSwiYnVpbGRzIjoxLCJidXlzIjp7IldIRUFUIjo2fSwiY2FyZXMiOjUsImZlZWRzIjo1LCJoYW5kcyI6NS"
    "wiaGlyZXMiOjUsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjEzMS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQi"
    "LCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo3fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NH0sInNoZW"
    "RfZHVzayI6eyJXSEVBVCI6MX19LCI1Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7IkNPVyI6MX0sImJ1aWxkcyI6MCwiYnV5"
    "cyI6eyJXSEVBVCI6Mn0sImNhcmVzIjo2LCJmZWVkcyI6NiwiaGFuZHMiOjQsImhpcmVzIjo0LCJsYW5kIjowLCJtb2"
    "5leV9kYXduIjoyMzAuMCwicGxhY2VzIjpbIkNPVyJdLCJwbGFudHMiOlsiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlki"
    "LCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSJdLCJzZWVkcyI6eyJNRUxPTiI6MywiU1RSQVdCRVJSWSI6NH0sInNlbG"
    "xzIjp7IkZFUlRJTElaRVIiOjUsIldIRUFUIjoxOH0sInNoZWRfZHVzayI6eyJXSEVBVCI6N319LCI2Ijp7ImFuaW1h"
    "bHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjoyLCJidXlzIjp7IldIRUFUIjo2fSwiY2FyZXMiOjYsImZlZWRzIjo2LCJoYW"
    "5kcyI6NCwiaGlyZXMiOjQsImxhbmQiOjEsIm1vbmV5X2Rhd24iOjE5Ni4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsi"
    "TUVMT04iLCJNRUxPTiJdLCJzZWVkcyI6eyJDQVJST1QiOjcsIk1FTE9OIjo1LCJTVFJBV0JFUlJZIjozfSwic2VsbH"
    "MiOnsiRkVSVElMSVpFUiI6NSwiV09PTCI6MTJ9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjd9fSwiNyI6eyJhbmltYWxz"
    "X2JvdWdodCI6eyJDT1ciOjIsIlNIRUVQIjoxfSwiYnVpbGRzIjoyLCJidXlzIjp7IldIRUFUIjozfSwiY2FyZXMiOj"
    "ksImZlZWRzIjo5LCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE0My4wLCJwbGFjZXMi"
    "OlsiU0hFRVAiLCJDT1ciLCJDT1ciXSwicGxhbnRzIjpbIk1FTE9OIiwiTUVMT04iLCJNRUxPTiIsIlNUUkFXQkVSUl"
    "kiLCJTVFJBV0JFUlJZIiwiTUVMT04iLCJTVFJBV0JFUlJZIiwiTUVMT04iLCJNRUxPTiJdLCJzZWVkcyI6eyJXSEVB"
    "VCI6NH0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjZ9LCJzaGVkX2R1c2siOnt9fSwiOCI6eyJhbmltYWxzX2JvdWdodC"
    "I6eyJTSEVFUCI6MX0sImJ1aWxkcyI6MiwiYnV5cyI6eyJXSEVBVCI6MTd9LCJjYXJlcyI6MTAsImZlZWRzIjoxMCwi"
    "aGFuZHMiOjExLCJoaXJlcyI6MTEsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE5MC4wLCJwbGFjZXMiOlsiU0hFRVAiXS"
    "wicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdC"
    "RVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IlNUUkFXQkVSUlkiOjQsIldIRUFUIj"
    "o1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NiwiTUlMSyI6MTJ9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjh9fSwiOSI6"
    "eyJhbmltYWxzX2JvdWdodCI6eyJTSEVFUCI6Mn0sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTR9LCJjYXJlcy"
    "I6MTIsImZlZWRzIjoxMiwiaGFuZHMiOjEyLCJoaXJlcyI6MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjk0My4wLCJw"
    "bGFjZXMiOlsiU0hFRVAiLCJTSEVFUCJdLCJwbGFudHMiOltdLCJzZWVkcyI6e30sInNlbGxzIjp7IkZFUlRJTElaRV"
    "IiOjksIldIRUFUIjo1LCJXT09MIjo4fX19"
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
