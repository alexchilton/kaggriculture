"""A repo-wide guard: a script that sums order quantities must say so on the page.

This project has printed offers as fills four times, and each time the fix was local to one script
while the pattern stayed legal everywhere else. Docstrings did not stop it -- `scripts/why_we_lost.py`
carried a warning and printed `crops planted (offers)` anyway, a heading that makes both claims at
once. `scripts/episode_index.py` carried a longer warning and named the field `sell`.

So the rule is mechanical. **A file that accumulates `order[2]` off an action stream has to contain
the word `offered` or `ordered` in its output.** The agent re-posts a standing order on every turn
until it fills, so those totals count an intention up to 24 times, and the only honest thing to do
with one is label it.

Two escapes, both explicit:

- `EXEMPT` lists files where the accumulation is not a report at all -- a builder converting a plan
  into an action array, a trainer packing a tensor. Adding to it is a deliberate act, and each entry
  says why.
- Reconstructing the real number is always better than labelling the wrong one. `kagg/analysis/
  fills.py` does that for a simulated game and `kagg/analysis/replay_fills.py` for a downloaded one.
"""

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

#: Summing the QUANTITY field of a market order. `order[2]` is units-per-order, and adding it up
#: across turns is the mistake; reading it once to build an action is not.
ACCUMULATES = re.compile(
    r"\+=\s*(int\()?\w+\[2\]|\+=\s*(int\()?\w+\[2\]\)|\[\w+\[1\]\]\s*\+=|"
    r"\+=\s*int\(\w+\[2\]\)\s*if\s*len")

#: Anything here means the file has told its reader what the number is.
DECLARES = re.compile(r"offered|ordered|_ord\b|OFFER|ORDERS?\b|order total|orders emitted")

EXEMPT = {
    # Builders and encoders: `order[2]` becomes a cell in an action array, never a printed total.
    "seed_from_replay.py": "packs a recorded season into the fast sim's action tensors",
    "build_script_submission.py": "writes the action script the submission replays",
    "build_planner_submission.py": "same, for the planner build",
    "extract_leader_schedule.py": "turns a recording into a per-day plan the agent executes",
    "extract_winner_plan.py": "same",
    "mine_build_orders.py": "same",
    "optimise_script.py": "mutates an action array in place",
    "train_jax_rl.py": "packs a training batch",
    "bc_dagger.py": "packs a training batch",
    "es_market.py": "mutates a candidate's order schedule",
    "measure_sell_timing_impact.py": "perturbs a sell array and replays it",
}


#: Docstrings and comments are where a file EXPLAINS the mistake, and a file that explains it is
#: the opposite of an offender. Stripping them first is what stops the guard firing on its own
#: warning label -- `what_we_should_have_sold.py` documents the exact line it used to contain.
DOCSTRING = re.compile(r'("""|\'\'\')(?:.|\n)*?\1')


def code_of(path):
    source = DOCSTRING.sub("", path.read_text())
    return "\n".join(line for line in source.splitlines()
                      if not line.lstrip().startswith("#"))


def scripts():
    for path in sorted((REPO / "scripts").glob("*.py")):
        if path.name in EXEMPT:
            continue
        yield path


def test_every_script_that_sums_order_quantities_labels_them():
    offenders = []
    for path in scripts():
        source = code_of(path)
        if not ACCUMULATES.search(source):
            continue
        if DECLARES.search(path.read_text()):
            continue
        offenders.append(path.name)
    assert not offenders, (
        "these sum market-order quantities off an action stream and print the total under a name "
        "that does not say it is an offer:\n  " + "\n  ".join(offenders)
        + "\n\nEither recover the real number (kagg/analysis/replay_fills.py for a recording, "
          "kagg/analysis/fills.py for a simulated game), or put `offered` in the heading. If it is "
          "not a report at all, add it to EXEMPT with the reason.")


def test_no_heading_claims_to_be_a_fill_and_an_offer_at_once():
    """`crops planted (offers)` is two contradictory claims in one label, and it is what shipped.

    A heading may say a number is a count of the board, or that it is an offer. Not both.
    """
    board_words = re.compile(r"\bplanted\b|\bfilled\b|\bfills\b|\bsold\b|\bbought\b|\bherd\b")
    offer_words = re.compile(r"\boffers?\b|\boffered\b")
    #: A heading that CONTRASTS the two is the correct thing to write, not the defect. "measured on
    #: fills, not offers" is a claim about which one was used; "crops planted (offers)" is a claim
    #: that they are the same.
    contrasts = re.compile(r"not offers?|never offers?|rather than an? offers?|not an offer|"
                           r"vs\.? offers?|against offers?|offered, filled")
    offenders = []
    for path in scripts():
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if "print(" not in line:
                continue
            if contrasts.search(line):
                continue
            if board_words.search(line) and offer_words.search(line):
                offenders.append(f"{path.name}:{number}  {line.strip()[:90]}")
    assert not offenders, (
        "a heading cannot be both:\n  " + "\n  ".join(offenders))


def test_the_exempt_list_only_names_files_that_exist():
    """An exemption for a deleted file is a hole left open for the next file of that name."""
    missing = [name for name in EXEMPT if not (REPO / "scripts" / name).exists()]
    assert not missing, f"EXEMPT names files that are gone: {missing}"


def test_the_guard_can_actually_fail(tmp_path):
    """The lint's own gate. A rule that cannot fire is not a rule -- and this repo has been caught
    by exactly that three times, most recently a parity harness that could not emit FEED."""
    assert ACCUMULATES.search("            sold[m[1]] += int(m[2])")
    assert ACCUMULATES.search("                c[o[1]] += int(o[2])")
    assert not ACCUMULATES.search("            total += 1")
    assert DECLARES.search('print(f"  sells offered: {c}")')
    assert not DECLARES.search('print(f"  crops planted: {c}")')
