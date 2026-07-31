"""Local arena: fixed-seed measurement of agent strength.

Built before any agent, deliberately. The Orbit Wars post-mortem's harshest
finding was that half the diagnoses were guesses for want of measurement.
"""

from kagg.arena.arena import ArenaReport, MatchResult, run_arena, run_match

__all__ = ["ArenaReport", "MatchResult", "run_arena", "run_match"]

from kagg.arena.pool import COMPETITIVE, OPPONENTS, PoolResult, evaluate  # noqa: E402
