import json, pathlib
from kagg.search.schedule_agent import make_agent
_P = pathlib.Path('/Users/alexchilton/DataspellProjects/kaggriculture/data/seed_scripts/kawashigi/schedule.json')
_S = {int(k): v for k, v in json.loads(_P.read_text()).items()}
_DROP = ('plant_tiles', 'build_tiles', 'land_turns', 'orders')
_T = {d: {k: v for k, v in r.items() if k not in _DROP} for d, r in _S.items()}
_A = {}
def agent(obs, config=None):
    me = obs['player']
    if me not in _A:
        _A[me] = make_agent(_T, me, router=True)
    return _A[me](obs)
