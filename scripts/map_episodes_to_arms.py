"""Which of our two arms played which episode.

A replay's `info` carries only `TeamNames`, and both of ours read "alex chilton" -- so on a
self-match the file cannot say which submission sat in which seat. The episode LISTING can: it is
keyed by submission id. Two calls, spaced, written to a json the analysis scripts read.

Arm names are attached by submission id order -- the lower id was submitted first. That is an
inference, not something the API states, and it is recorded here so a later reader can check it
against `kaggle competitions submissions`.
"""
import json, pathlib, sys, time
import urllib3.util.request as _ur
_ur.ACCEPT_ENCODING = "identity"
import kaggle

ARMS = {"55786408": "carrot_only", "55786494": "d28"}
OUT = pathlib.Path("data/seed_scripts/ours_2026-08-26/_episode_arm.json")

def main():
    api = kaggle.api
    m = {}
    for i, (sub, arm) in enumerate(ARMS.items()):
        eps = api.competition_list_episodes(int(sub))
        ids = [int(getattr(e, "id", None) or e["id"]) for e in (eps or [])]
        print(f"  {sub} ({arm}): {len(ids)} episodes", flush=True)
        for e in ids:
            m.setdefault(str(e), []).append(arm)
        if i == 0:
            time.sleep(20)
    OUT.write_text(json.dumps(m, indent=1))
    both = [k for k, v in m.items() if len(v) > 1]
    print(f"wrote {OUT}  ({len(m)} episodes, {len(both)} played by BOTH arms)", flush=True)

if __name__ == "__main__":
    main()
