#!/usr/bin/env bash
# Back the fix out, run the test, put it back. The test must go RED in between.
# The restore runs on EXIT, so an interrupt or a pytest crash cannot leave the file patched.
exec 2>&1
cd /home/alex/kaggriculture

F=scripts/tape_edit_sweep.py
cp "$F" "$F.revertcheck.bak"
trap 'mv -f "$F.revertcheck.bak" "$F"; echo "--- restored $F"' EXIT

echo "--- backing out the _apply_wrappers call:"
python3 - <<'PY'
import pathlib
p = pathlib.Path("scripts/tape_edit_sweep.py")
s = p.read_text()
old = "        a = _apply_wrappers(a, edits)\n"
assert old in s, "the line to back out is not there -- check the fix is applied"
p.write_text(s.replace(old, "", 1))
print("removed:", old.strip())
PY

echo "--- test with the fix REMOVED (must FAIL):"
.venv/bin/python -m pytest tests/test_a_wrapper_arm_is_not_a_silent_copy_of_the_control.py -q 2>&1 | tail -15
