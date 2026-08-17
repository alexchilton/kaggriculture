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

from .branch import Branch

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
    "Ojc0LCJNSUxLIjo2fX0sIjEzIjp7ImFuaW1hbHNfYm91Z2h0Ijp7IlNIRUVQIjoyfSwiYnVpbGRzIjoxLCJidXlzIj"
    "p7IldIRUFUIjo5fSwiY2FyZXMiOjE2LCJmZWVkcyI6MTYsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJt"
    "b25leV9kYXduIjoxMjAxMS4wLCJwbGFjZXMiOlsiU0hFRVAiLCJTSEVFUCJdLCJwbGFudHMiOlsiV0hFQVQiLCJXSE"
    "VBVCIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo0fSwic2VsbHMiOnsiRkVS"
    "VElMSVpFUiI6MTQsIk1JTEsiOjYsIldIRUFUIjo4LCJXT09MIjo4fX0sIjE0Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fS"
    "wiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoyMH0sImNhcmVzIjoxNywiZmVlZHMiOjE3LCJoYW5kcyI6OCwiaGly"
    "ZXMiOjgsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjEzODI3LjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIj"
    "p7fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTksIk1JTEsiOjksIldPT0wiOjZ9fSwiMTUiOnsiYW5pbWFsc19ib3Vn"
    "aHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjEwfSwiY2FyZXMiOjE3LCJmZWVkcyI6MTcsImhhbmRzIj"
    "oxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjoxNTY4NS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjozfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6Mj"
    "UyLCJNSUxLIjo2LCJXSEVBVCI6NjUsIldPT0wiOjEyfX0sIjE2Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRz"
    "IjowLCJidXlzIjp7IldIRUFUIjoxMn0sImNhcmVzIjoxOCwiZmVlZHMiOjE4LCJoYW5kcyI6OSwiaGlyZXMiOjksIm"
    "xhbmQiOjAsIm1vbmV5X2Rhd24iOjI0MDcyLjAsInBsYWNlcyI6WyJTSEVFUCJdLCJwbGFudHMiOlsiV0hFQVQiLCJX"
    "SEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjozMy"
    "wiTUVMT04iOjEyLCJNSUxLIjoxOCwiU1RSQVdCRVJSWSI6NywiV0hFQVQiOjIwLCJXT09MIjoxNH19LCIxNyI6eyJh"
    "bmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTB9LCJjYXJlcyI6MTgsImZlZWRzIj"
    "oxOCwiaGFuZHMiOjEyLCJoaXJlcyI6MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjI2OTMzLjAsInBsYWNlcyI6W10s"
    "InBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIj"
    "o1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTc3LCJNRUxPTiI6MTgsIk1JTEsiOjYsIldIRUFUIjoxNywiV09PTCI6"
    "MTZ9fSwiMTgiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjUyfSwiY2FyZX"
    "MiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjozNjI4Mi4w"
    "LCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRU"
    "FUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIs"
    "IldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2"
    "VlZHMiOnsiV0hFQVQiOjIyfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MzEzLCJNRUxPTiI6MTgsIk1JTEsiOjEyLCJT"
    "VFJBV0JFUlJZIjoxNSwiV0hFQVQiOjM3LCJXT09MIjo0fX0sIjE5Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbG"
    "RzIjowLCJidXlzIjp7IldIRUFUIjoxMTZ9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6"
    "MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjQxNDU2LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRU"
    "FUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjZ9LCJzZWxscyI6eyJG"
    "RVJUSUxJWkVSIjoxMTIsIk1JTEsiOjYsIlNUUkFXQkVSUlkiOjYsIldIRUFUIjoxMjYsIldPT0wiOjM3fX0sIjIiOn"
    "siYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjEsImJ1eXMiOnsiV0hFQVQiOjR9LCJjYXJlcyI6NCwiZmVlZHMi"
    "OjQsImhhbmRzIjo0LCJoaXJlcyI6NCwibGFuZCI6MCwibW9uZXlfZGF3biI6MTY0LjAsInBsYWNlcyI6W10sInBsYW"
    "50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnt9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjR9fSwiMjAiOnsiYW5pbWFs"
    "c19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjUxfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsIm"
    "hhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjo0NDM1OC4wLCJwbGFjZXMiOltdLCJwbGFu"
    "dHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6ey"
    "JGRVJUSUxJWkVSIjoyNSwiTUlMSyI6MTIsIlNUUkFXQkVSUlkiOjE3LCJXSEVBVCI6NTUsIldPT0wiOjR9fSwiMjEi"
    "OnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjU1fSwiY2FyZXMiOjE4LCJmZW"
    "VkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjo0NzUwMC4wLCJwbGFjZXMi"
    "OltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiQ0FSUk9UIiwiQ0FSUk9UIiwiQ0FSUk9UIl0sIn"
    "NlZWRzIjp7IkNBUlJPVCI6MywiV0hFQVQiOjN9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyMTksIk1JTEsiOjYsIlNU"
    "UkFXQkVSUlkiOjIxLCJXSEVBVCI6MTUyLCJXT09MIjoxMn19LCIyMiI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aW"
    "xkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Mjd9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6"
    "MTIsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjUyOTM4LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRU"
    "FUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMi"
    "OnsiV0hFQVQiOjl9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyODMsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoyNiwiV0"
    "hFQVQiOjIwMiwiV09PTCI6MTZ9fSwiMjMiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsi"
    "V0hFQVQiOjEzNH0sImNhcmVzIjoxOCwiZmVlZHMiOjE4LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW"
    "9uZXlfZGF3biI6NTgyNDIuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldI"
    "RUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjh9LCJzZWxscyI6ey"
    "JGRVJUSUxJWkVSIjoyNTAsIk1JTEsiOjYsIlNUUkFXQkVSUlkiOjEzLCJXSEVBVCI6MjEyLCJXT09MIjozMH19LCIy"
    "NCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTExfSwiY2FyZXMiOjE4LC"
    "JmZWVkcyI6MTgsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXduIjo2MTExNy4wLCJwbGFj"
    "ZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJDQVJST1QiLCJDQVJST1QiLC"
    "JDQVJST1QiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJDQVJST1QiOjMsIldIRUFU"
    "Ijo4fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTU2LCJNSUxLIjoxMiwiU1RSQVdCRVJSWSI6MzEsIldIRUFUIjoxNT"
    "J9fSwiMjUiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjk1fSwiY2FyZXMi"
    "OjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXduIjo2NTk3NS4wLC"
    "JwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFU"
    "IiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLC"
    "JzZWVkcyI6eyJXSEVBVCI6MTR9LCJzZWxscyI6eyJDQVJST1QiOjcsIkZFUlRJTElaRVIiOjI5LCJNSUxLIjo2LCJT"
    "VFJBV0JFUlJZIjoxMCwiV0hFQVQiOjEwNiwiV09PTCI6MzJ9fSwiMjYiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidW"
    "lsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjUyfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMSwiaGlyZXMi"
    "OjExLCJsYW5kIjowLCJtb25leV9kYXduIjo2OTYyNS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSE"
    "VBVCIsIldIRUFUIiwiV0hFQVQiLCJDQVJST1QiLCJXSEVBVCJdLCJzZWVkcyI6eyJDQVJST1QiOjEsIldIRUFUIjo1"
    "fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MjUsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoxOCwiV0hFQVQiOjcxLCJXT0"
    "9MIjo4fX0sIjI3Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoxMH0sImNh"
    "cmVzIjoxMywiZmVlZHMiOjE2LCJoYW5kcyI6MTEsImhpcmVzIjoxMSwibGFuZCI6MCwibW9uZXlfZGF3biI6NzI1ND"
    "QuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJX"
    "SEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjoxMH0sInNlbGxzIj"
    "p7IkZFUlRJTElaRVIiOjExLCJNSUxLIjo2LCJTVFJBV0JFUlJZIjoyNiwiV0hFQVQiOjEzNSwiV09PTCI6OH19LCIy"
    "OCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Nn0sImNhcmVzIjo3LCJmZW"
    "VkcyI6OCwiaGFuZHMiOjEwLCJoaXJlcyI6MTAsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjc4MzgzLjAsInBsYWNlcyI6"
    "W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiQ0FSUk9UIjo3LCJGRVJUSUxJWkVSIjoxMywiTUlMSy"
    "I6MTIsIlNUUkFXQkVSUlkiOjEwLCJXSEVBVCI6MjYsIldPT0wiOjIwfX0sIjI5Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7"
    "fSwiYnVpbGRzIjowLCJidXlzIjp7fSwiY2FyZXMiOjAsImZlZWRzIjowLCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbm"
    "QiOjAsIm1vbmV5X2Rhd24iOjg1MDc4LjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMi"
    "OnsiRkVSVElMSVpFUiI6NiwiTUlMSyI6MTgsIlNUUkFXQkVSUlkiOjIsIldIRUFUIjo5MCwiV09PTCI6Mjh9fSwiMy"
    "I6eyJhbmltYWxzX2JvdWdodCI6eyJDT1ciOjF9LCJidWlsZHMiOjAsImJ1eXMiOnt9LCJjYXJlcyI6NCwiZmVlZHMi"
    "OjQsImhhbmRzIjo1LCJoaXJlcyI6NSwibGFuZCI6MCwibW9uZXlfZGF3biI6NDIxLjAsInBsYWNlcyI6WyJDT1ciXS"
    "wicGxhbnRzIjpbXSwic2VlZHMiOnsiQ0FSUk9UIjoxfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NH0sInNoZWRfZHVz"
    "ayI6e319LCI0Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjoxLCJidXlzIjp7IldIRUFUIjo2fSwiY2FyZX"
    "MiOjUsImZlZWRzIjo1LCJoYW5kcyI6NSwiaGlyZXMiOjUsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjEzMS4wLCJwbGFj"
    "ZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo3fSwic2VsbH"
    "MiOnsiRkVSVElMSVpFUiI6NH0sInNoZWRfZHVzayI6eyJXSEVBVCI6MX19LCI1Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7"
    "IkNPVyI6MX0sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Mn0sImNhcmVzIjo2LCJmZWVkcyI6NiwiaGFuZHMiOj"
    "QsImhpcmVzIjo0LCJsYW5kIjowLCJtb25leV9kYXduIjoyMzAuMCwicGxhY2VzIjpbIkNPVyJdLCJwbGFudHMiOlsi"
    "U1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSJdLCJzZWVkcyI6eyJNRUxPTi"
    "I6MywiU1RSQVdCRVJSWSI6NH0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjUsIldIRUFUIjoxOH0sInNoZWRfZHVzayI6"
    "eyJXSEVBVCI6N319LCI2Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjoyLCJidXlzIjp7IldIRUFUIjo2fS"
    "wiY2FyZXMiOjYsImZlZWRzIjo2LCJoYW5kcyI6NCwiaGlyZXMiOjQsImxhbmQiOjEsIm1vbmV5X2Rhd24iOjE5Ni4w"
    "LCJwbGFjZXMiOltdLCJwbGFudHMiOlsiTUVMT04iLCJNRUxPTiJdLCJzZWVkcyI6eyJDQVJST1QiOjcsIk1FTE9OIj"
    "o1LCJTVFJBV0JFUlJZIjozfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NSwiV09PTCI6MTJ9LCJzaGVkX2R1c2siOnsi"
    "V0hFQVQiOjd9fSwiNyI6eyJhbmltYWxzX2JvdWdodCI6eyJDT1ciOjIsIlNIRUVQIjoxfSwiYnVpbGRzIjoyLCJidX"
    "lzIjp7IldIRUFUIjozfSwiY2FyZXMiOjksImZlZWRzIjo5LCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbmQiOjAsIm1v"
    "bmV5X2Rhd24iOjE0My4wLCJwbGFjZXMiOlsiU0hFRVAiLCJDT1ciLCJDT1ciXSwicGxhbnRzIjpbIk1FTE9OIiwiTU"
    "VMT04iLCJNRUxPTiIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiTUVMT04iLCJTVFJBV0JFUlJZIiwiTUVMT04i"
    "LCJNRUxPTiJdLCJzZWVkcyI6eyJXSEVBVCI6NH0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjZ9LCJzaGVkX2R1c2siOn"
    "t9fSwiOCI6eyJhbmltYWxzX2JvdWdodCI6eyJTSEVFUCI6MX0sImJ1aWxkcyI6MiwiYnV5cyI6eyJXSEVBVCI6MTd9"
    "LCJjYXJlcyI6MTAsImZlZWRzIjoxMCwiaGFuZHMiOjExLCJoaXJlcyI6MTEsImxhbmQiOjAsIm1vbmV5X2Rhd24iOj"
    "E5MC4wLCJwbGFjZXMiOlsiU0hFRVAiXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIlNUUkFXQkVS"
    "UlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIj"
    "p7IlNUUkFXQkVSUlkiOjQsIldIRUFUIjo1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NiwiTUlMSyI6MTJ9LCJzaGVk"
    "X2R1c2siOnsiV0hFQVQiOjh9fSwiOSI6eyJhbmltYWxzX2JvdWdodCI6eyJTSEVFUCI6Mn0sImJ1aWxkcyI6MCwiYn"
    "V5cyI6eyJXSEVBVCI6MTR9LCJjYXJlcyI6MTIsImZlZWRzIjoxMiwiaGFuZHMiOjEyLCJoaXJlcyI6MTIsImxhbmQi"
    "OjAsIm1vbmV5X2Rhd24iOjk0My4wLCJwbGFjZXMiOlsiU0hFRVAiLCJTSEVFUCJdLCJwbGFudHMiOltdLCJzZWVkcy"
    "I6e30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjksIldIRUFUIjo1LCJXT09MIjo4fX19"
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


class Q4Branch(Branch):
    """His four-quadrant season, taken when the town promises wool early.

    `install` does more than swap rows: the shipped routes were solved for the 75-tile board and
    `cover._apply_precomputed` keys a stop on `(tile, ops)`, so on a 100-tile board they DROP rather
    than adapt. The four-quadrant solve goes in with the rows or the branch plays unsolved days.
    """

    decide_by_day = DECIDE_BY_DAY
    split_day = SPLIT_DAY
    decided_key = "q4_decided"
    armed_key = "q4_armed"

    def trigger(self, observation):
        return the_town_promised_wool_early(observation)

    def rows(self):
        return _q4_rows()

    #: The four-quadrant solve for each crop mix. A route is keyed on `(tile, ops)`, so the
    #: strawberry season cannot use the melon season's routes any more than a 100-tile board can
    #: use a 75-tile board's -- the stops simply fail to match and drop, which is the failure this
    #: class's own docstring describes. Handing the melon set to a strawberry board left the whole
    #: of d9-d29 effectively unsolved on that branch.
    SOLVE_FOR_MELON = "kagg.search.solved_days_q4"
    SOLVE_FOR_STRAWBERRY = "kagg.search.solved_days_straw_q4"

    def install(self, schedule, state=None):
        moved = super().install(schedule, state)
        cover = importlib.import_module("kagg.search.cover")
        from . import melon_branch as MB
        straw = bool((state or {}).get(MB.BRANCH.armed_key))
        name = self.SOLVE_FOR_STRAWBERRY if straw else self.SOLVE_FOR_MELON
        try:
            q4 = importlib.import_module(name)
        except ImportError:
            # The strawberry four-quadrant solve may not exist yet. Falling back to the melon set
            # is what shipped before this branch existed, so it is no worse -- but say nothing
            # clever about it: an unsolved day is a day the greedy plays.
            q4 = importlib.import_module(self.SOLVE_FOR_MELON)
        cover.UNSOLVE_DAYS = ()
        cover.PRECOMPUTED_ROUTES = {d: {u: [(tuple(tile), tuple(ops)) for tile, ops in seq]
                                        for u, seq in units.items()}
                                    for d, units in q4.SOLVED_DAYS.items()}
        return moved


BRANCH = Q4Branch()

install_the_fourth_quadrant = BRANCH.install


def arm(schedule, state, observation, day):
    """`BRANCH.arm`, gated by `BRANCH_ON_THE_YARN_STORE`."""
    if not BRANCH_ON_THE_YARN_STORE:
        return False
    return BRANCH.arm(schedule, state, observation, day)
