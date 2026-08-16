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
    "c19ib3VnaHQiOnt9LCJidWlsZHMiOjEsImJ1eXMiOnsiV0hFQVQiOjh9LCJjYXJlcyI6MTUsImZlZWRzIjoxNSwiaGFuZHMi"
    "OjEwLCJoaXJlcyI6MTAsImxhbmQiOjEsIm1vbmV5X2Rhd24iOjg5MDUuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFU"
    "IiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlki"
    "LCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJXSEVBVCI6OX0sInNlbGxzIjp7IkZFUlRJTEla"
    "RVIiOjc0LCJNSUxLIjo2fX0sIjEzIjp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjo5"
    "fSwiY2FyZXMiOjE2LCJmZWVkcyI6MTYsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXduIjoxMjAx"
    "MS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiU1RSQVdCRVJSWSIsIldIRUFUIl0s"
    "InNlZWRzIjp7IldIRUFUIjo0fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTQsIk1JTEsiOjYsIldIRUFUIjo4LCJXT09MIjo4"
    "fX0sIjE0Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoyMH0sImNhcmVzIjoxNywi"
    "ZmVlZHMiOjE3LCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjEzODI3LjAsInBsYWNlcyI6W10s"
    "InBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTksIk1JTEsiOjksIldPT0wiOjZ9fSwiMTUi"
    "OnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjEwfSwiY2FyZXMiOjE3LCJmZWVkcyI6"
    "MTcsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjoxNTY4NS4wLCJwbGFjZXMiOltdLCJwbGFu"
    "dHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjozfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6"
    "MjUyLCJNSUxLIjo2LCJXSEVBVCI6NjUsIldPT0wiOjEyfX0sIjE2Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjow"
    "LCJidXlzIjp7IldIRUFUIjoxMn0sImNhcmVzIjoxOCwiZmVlZHMiOjE4LCJoYW5kcyI6OSwiaGlyZXMiOjksImxhbmQiOjAs"
    "Im1vbmV5X2Rhd24iOjI0MDcyLjAsInBsYWNlcyI6WyJTSEVFUCJdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFU"
    "IiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjozMywiTUVMT04iOjEyLCJNSUxL"
    "IjoxOCwiU1RSQVdCRVJSWSI6NywiV0hFQVQiOjIwLCJXT09MIjoxNH19LCIxNyI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1"
    "aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTB9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6MTIs"
    "ImxhbmQiOjAsIm1vbmV5X2Rhd24iOjI2OTMzLjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hF"
    "QVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7IldIRUFUIjo1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTc3LCJNRUxP"
    "TiI6MTgsIk1JTEsiOjYsIldIRUFUIjoxNywiV09PTCI6MTZ9fSwiMTgiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMi"
    "OjAsImJ1eXMiOnsiV0hFQVQiOjUyfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5k"
    "IjowLCJtb25leV9kYXduIjozNjI4Mi4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjIyfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MzEzLCJNRUxPTiI6MTgsIk1JTEsi"
    "OjEyLCJTVFJBV0JFUlJZIjoxNSwiV0hFQVQiOjM3LCJXT09MIjo0fX0sIjE5Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVp"
    "bGRzIjowLCJidXlzIjp7IldIRUFUIjoxMTZ9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6MTIs"
    "ImxhbmQiOjAsIm1vbmV5X2Rhd24iOjQxNDU2LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hF"
    "QVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjZ9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjox"
    "MTIsIk1JTEsiOjYsIlNUUkFXQkVSUlkiOjYsIldIRUFUIjoxMjYsIldPT0wiOjM3fX0sIjIiOnsiYW5pbWFsc19ib3VnaHQi"
    "Ont9LCJidWlsZHMiOjEsImJ1eXMiOnsiV0hFQVQiOjR9LCJjYXJlcyI6NCwiZmVlZHMiOjQsImhhbmRzIjo0LCJoaXJlcyI6"
    "NCwibGFuZCI6MCwibW9uZXlfZGF3biI6MTY0LjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMi"
    "Ont9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjR9fSwiMjAiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMi"
    "OnsiV0hFQVQiOjUxfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25l"
    "eV9kYXduIjo0NDM1OC4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwi"
    "c2VlZHMiOnsiV0hFQVQiOjR9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyNSwiTUlMSyI6MTIsIlNUUkFXQkVSUlkiOjE3LCJX"
    "SEVBVCI6NTUsIldPT0wiOjR9fSwiMjEiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQi"
    "OjU1fSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMiwiaGlyZXMiOjEyLCJsYW5kIjowLCJtb25leV9kYXduIjo0"
    "NzUwMC4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiQ0FSUk9UIiwiQ0FSUk9UIiwi"
    "Q0FSUk9UIl0sInNlZWRzIjp7IkNBUlJPVCI6MywiV0hFQVQiOjN9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyMTksIk1JTEsi"
    "OjYsIlNUUkFXQkVSUlkiOjIxLCJXSEVBVCI6MTUyLCJXT09MIjoxMn19LCIyMiI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1"
    "aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Mjd9LCJjYXJlcyI6MTgsImZlZWRzIjoxOCwiaGFuZHMiOjEyLCJoaXJlcyI6MTIs"
    "ImxhbmQiOjAsIm1vbmV5X2Rhd24iOjUyOTM4LjAsInBsYWNlcyI6W10sInBsYW50cyI6WyJXSEVBVCIsIldIRUFUIiwiV0hF"
    "QVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjl9"
    "LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyODMsIk1JTEsiOjEyLCJTVFJBV0JFUlJZIjoyNiwiV0hFQVQiOjIwMiwiV09PTCI6"
    "MTZ9fSwiMjMiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjEzNH0sImNhcmVzIjox"
    "OCwiZmVlZHMiOjE4LCJoYW5kcyI6MTIsImhpcmVzIjoxMiwibGFuZCI6MCwibW9uZXlfZGF3biI6NTgyNDIuMCwicGxhY2Vz"
    "IjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiXSwic2VlZHMiOnsiV0hFQVQiOjh9LCJzZWxscyI6eyJGRVJUSUxJWkVSIjoyNTAsIk1JTEsiOjYsIlNUUkFXQkVS"
    "UlkiOjEzLCJXSEVBVCI6MjEyLCJXT09MIjozMH19LCIyNCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5"
    "cyI6eyJXSEVBVCI6MTExfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJt"
    "b25leV9kYXduIjo2MTExNy4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQi"
    "LCJDQVJST1QiLCJDQVJST1QiLCJDQVJST1QiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6eyJD"
    "QVJST1QiOjMsIldIRUFUIjo4fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MTU2LCJNSUxLIjoxMiwiU1RSQVdCRVJSWSI6MzEs"
    "IldIRUFUIjoxNTJ9fSwiMjUiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsiV0hFQVQiOjk1fSwi"
    "Y2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9kYXduIjo2NTk3NS4w"
    "LCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCJdLCJzZWVkcyI6"
    "eyJXSEVBVCI6MTR9LCJzZWxscyI6eyJDQVJST1QiOjcsIkZFUlRJTElaRVIiOjI5LCJNSUxLIjo2LCJTVFJBV0JFUlJZIjox"
    "MCwiV0hFQVQiOjEwNiwiV09PTCI6MzJ9fSwiMjYiOnsiYW5pbWFsc19ib3VnaHQiOnt9LCJidWlsZHMiOjAsImJ1eXMiOnsi"
    "V0hFQVQiOjUyfSwiY2FyZXMiOjE4LCJmZWVkcyI6MTgsImhhbmRzIjoxMSwiaGlyZXMiOjExLCJsYW5kIjowLCJtb25leV9k"
    "YXduIjo2OTYyNS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJDQVJS"
    "T1QiLCJXSEVBVCJdLCJzZWVkcyI6eyJDQVJST1QiOjEsIldIRUFUIjo1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6MjUsIk1J"
    "TEsiOjEyLCJTVFJBV0JFUlJZIjoxOCwiV0hFQVQiOjcxLCJXT09MIjo4fX0sIjI3Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwi"
    "YnVpbGRzIjowLCJidXlzIjp7IldIRUFUIjoxMH0sImNhcmVzIjoxMywiZmVlZHMiOjE2LCJoYW5kcyI6MTEsImhpcmVzIjox"
    "MSwibGFuZCI6MCwibW9uZXlfZGF3biI6NzI1NDQuMCwicGxhY2VzIjpbXSwicGxhbnRzIjpbIldIRUFUIiwiV0hFQVQiLCJX"
    "SEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIiwiV0hFQVQiLCJXSEVBVCIsIldIRUFUIl0sInNlZWRzIjp7"
    "IldIRUFUIjoxMH0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjExLCJNSUxLIjo2LCJTVFJBV0JFUlJZIjoyNiwiV0hFQVQiOjEz"
    "NSwiV09PTCI6OH19LCIyOCI6eyJhbmltYWxzX2JvdWdodCI6e30sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Nn0sImNh"
    "cmVzIjo3LCJmZWVkcyI6OCwiaGFuZHMiOjEwLCJoaXJlcyI6MTAsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjc4MzgzLjAsInBs"
    "YWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiQ0FSUk9UIjo3LCJGRVJUSUxJWkVSIjoxMywiTUlM"
    "SyI6MTIsIlNUUkFXQkVSUlkiOjEwLCJXSEVBVCI6MjYsIldPT0wiOjIwfX0sIjI5Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwi"
    "YnVpbGRzIjowLCJidXlzIjp7fSwiY2FyZXMiOjAsImZlZWRzIjowLCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbmQiOjAsIm1v"
    "bmV5X2Rhd24iOjg1MDc4LjAsInBsYWNlcyI6W10sInBsYW50cyI6W10sInNlZWRzIjp7fSwic2VsbHMiOnsiRkVSVElMSVpF"
    "UiI6NiwiTUlMSyI6MTgsIlNUUkFXQkVSUlkiOjIsIldIRUFUIjo5MCwiV09PTCI6Mjh9fSwiMyI6eyJhbmltYWxzX2JvdWdo"
    "dCI6eyJDT1ciOjF9LCJidWlsZHMiOjAsImJ1eXMiOnt9LCJjYXJlcyI6NCwiZmVlZHMiOjQsImhhbmRzIjo1LCJoaXJlcyI6"
    "NSwibGFuZCI6MCwibW9uZXlfZGF3biI6NDIxLjAsInBsYWNlcyI6WyJDT1ciXSwicGxhbnRzIjpbXSwic2VlZHMiOnsiQ0FS"
    "Uk9UIjoxfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NH0sInNoZWRfZHVzayI6e319LCI0Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7"
    "fSwiYnVpbGRzIjoxLCJidXlzIjp7IldIRUFUIjo2fSwiY2FyZXMiOjUsImZlZWRzIjo1LCJoYW5kcyI6NSwiaGlyZXMiOjUs"
    "ImxhbmQiOjAsIm1vbmV5X2Rhd24iOjEzMS4wLCJwbGFjZXMiOltdLCJwbGFudHMiOlsiV0hFQVQiLCJXSEVBVCIsIldIRUFU"
    "Il0sInNlZWRzIjp7IldIRUFUIjo3fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NH0sInNoZWRfZHVzayI6eyJXSEVBVCI6MX19"
    "LCI1Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7IkNPVyI6MX0sImJ1aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6Mn0sImNhcmVzIjo2"
    "LCJmZWVkcyI6NiwiaGFuZHMiOjQsImhpcmVzIjo0LCJsYW5kIjowLCJtb25leV9kYXduIjoyMzAuMCwicGxhY2VzIjpbIkNP"
    "VyJdLCJwbGFudHMiOlsiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSJdLCJzZWVk"
    "cyI6eyJNRUxPTiI6MywiU1RSQVdCRVJSWSI6NH0sInNlbGxzIjp7IkZFUlRJTElaRVIiOjUsIldIRUFUIjoxOH0sInNoZWRf"
    "ZHVzayI6eyJXSEVBVCI6N319LCI2Ijp7ImFuaW1hbHNfYm91Z2h0Ijp7fSwiYnVpbGRzIjoyLCJidXlzIjp7IldIRUFUIjo2"
    "fSwiY2FyZXMiOjYsImZlZWRzIjo2LCJoYW5kcyI6NCwiaGlyZXMiOjQsImxhbmQiOjEsIm1vbmV5X2Rhd24iOjE5Ni4wLCJw"
    "bGFjZXMiOltdLCJwbGFudHMiOlsiTUVMT04iLCJNRUxPTiJdLCJzZWVkcyI6eyJDQVJST1QiOjcsIk1FTE9OIjo1LCJTVFJB"
    "V0JFUlJZIjozfSwic2VsbHMiOnsiRkVSVElMSVpFUiI6NSwiV09PTCI6MTJ9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjd9fSwi"
    "NyI6eyJhbmltYWxzX2JvdWdodCI6eyJDT1ciOjIsIlNIRUVQIjoxfSwiYnVpbGRzIjoyLCJidXlzIjp7IldIRUFUIjozfSwi"
    "Y2FyZXMiOjksImZlZWRzIjo5LCJoYW5kcyI6OCwiaGlyZXMiOjgsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE0My4wLCJwbGFj"
    "ZXMiOlsiU0hFRVAiLCJDT1ciLCJDT1ciXSwicGxhbnRzIjpbIk1FTE9OIiwiTUVMT04iLCJNRUxPTiIsIlNUUkFXQkVSUlki"
    "LCJTVFJBV0JFUlJZIiwiTUVMT04iLCJTVFJBV0JFUlJZIiwiTUVMT04iLCJNRUxPTiJdLCJzZWVkcyI6eyJXSEVBVCI6NH0s"
    "InNlbGxzIjp7IkZFUlRJTElaRVIiOjZ9LCJzaGVkX2R1c2siOnt9fSwiOCI6eyJhbmltYWxzX2JvdWdodCI6eyJTSEVFUCI6"
    "MX0sImJ1aWxkcyI6MiwiYnV5cyI6eyJXSEVBVCI6MTd9LCJjYXJlcyI6MTAsImZlZWRzIjoxMCwiaGFuZHMiOjExLCJoaXJl"
    "cyI6MTEsImxhbmQiOjAsIm1vbmV5X2Rhd24iOjE5MC4wLCJwbGFjZXMiOlsiU0hFRVAiXSwicGxhbnRzIjpbIldIRUFUIiwi"
    "V0hFQVQiLCJXSEVBVCIsIlNUUkFXQkVSUlkiLCJTVFJBV0JFUlJZIiwiU1RSQVdCRVJSWSIsIlNUUkFXQkVSUlkiLCJXSEVB"
    "VCIsIldIRUFUIl0sInNlZWRzIjp7IlNUUkFXQkVSUlkiOjQsIldIRUFUIjo1fSwic2VsbHMiOnsiRkVSVElMSVpFUiI6Niwi"
    "TUlMSyI6MTJ9LCJzaGVkX2R1c2siOnsiV0hFQVQiOjh9fSwiOSI6eyJhbmltYWxzX2JvdWdodCI6eyJTSEVFUCI6Mn0sImJ1"
    "aWxkcyI6MCwiYnV5cyI6eyJXSEVBVCI6MTR9LCJjYXJlcyI6MTIsImZlZWRzIjoxMiwiaGFuZHMiOjEyLCJoaXJlcyI6MTIs"
    "ImxhbmQiOjAsIm1vbmV5X2Rhd24iOjk0My4wLCJwbGFjZXMiOlsiU0hFRVAiLCJTSEVFUCJdLCJwbGFudHMiOltdLCJzZWVk"
    "cyI6e30sInNlbGxzIjp7IkZFUlRJTElaRVIiOjksIldIRUFUIjo1LCJXT09MIjo4fX19"
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
