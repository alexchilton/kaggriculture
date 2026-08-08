"""Probe: is the d8 sh:wheat divergence a harvest gap, a stranded-in-hand gap, or a sell gap?

Prints, per day, sh:wheat (shed) alongside HARVEST/SELL/BUY_PRODUCT/DROP/PICKUP op counts for
both sides, ours vs the seb tape. Companion to the CLAUDE.md-required
`python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 12 --diff --no-moves`.
"""
import sys
import json
import pathlib

sys.path.insert(0, ".")
from kagg.search import schedule_agent
import scripts.breakdown as bd

replay, schedule, team = bd.TAPES["seb"]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in bd.TAPE_ONLY} for d, r in sched.items()}
opp = lambda: bd.tape_policy(replay, team, 1)

his, his_ops, his_cov = bd.run(lambda: bd.tape_policy(replay, team, 0), opp, 11, 0.0)
a = schedule_agent.make_agent(thin, 0, router=True)
ours, our_ops, our_cov = bd.run(lambda: (lambda o, t: a(o)), opp, 11, 0.0)

print(f"{'day':>4} {'sh:wheat ours':>14} {'sh:wheat tape':>14} {'harvest ours':>13} {'harvest tape':>13} "
      f"{'sell ours':>10} {'sell tape':>10} {'buyprod ours':>12} {'buyprod tape':>12} "
      f"{'drop ours':>10} {'drop tape':>10} {'pickup ours':>12} {'pickup tape':>12}")
for d in range(12):
    print(f"{d:>4} {ours[d]['shed_WHEAT']:>14} {his[d]['shed_WHEAT']:>14} "
          f"{our_ops[d]['HARVEST']:>13} {his_ops[d]['HARVEST']:>13} "
          f"{our_ops[d]['SELL']:>10} {his_ops[d]['SELL']:>10} "
          f"{our_ops[d]['BUY_PRODUCT']:>12} {his_ops[d]['BUY_PRODUCT']:>12} "
          f"{our_ops[d]['DROP']:>10} {his_ops[d]['DROP']:>10} "
          f"{our_ops[d]['PICKUP']:>12} {his_ops[d]['PICKUP']:>12}")
