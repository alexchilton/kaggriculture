"""Days solved offline, as visit orders. Generated -- do not hand-edit.

Each day is `{unit_index: [[tile, [op, ...]], ...]}`, the exact assignment and order
`scripts/solve_day.py` found against `cover.py`'s own cost model. `cover._apply_precomputed`
seats them; a stop whose job today's board does not have is skipped and the rest still apply.

Solved on seed 11 against tape victor, whose schedule the agent plays. The board has no
random terrain, so geometry is identical in every game and these matched 100% on seed 14 too.

Coverage against the shipped greedy, jobs seated:

    d12  45/50 -> 50/50      d23  64/74 -> 74/74      d26  49/60 -> 60/60
    d16  61/61 -> 61/61      d24  49/58 -> 58/58      d27  50/61 -> 61/61
    d18  69/69 -> 69/69      d25  54/59 -> 59/59

Regenerate with `scripts/solve_day.py` IN DAY ORDER: each solved day changes the next day's
board, so a fixture must be dumped with every earlier route already installed.
"""

SOLVED_DAYS = {
    12: {
        0: [((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        1: [((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((3, 5), ('WATER',)), ((2, 5), ('WATER',)), ((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        2: [],
        3: [],
        4: [((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((3, 0), ('FERTILIZE', 'WATER')), ((2, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((2, 1), ('FERTILIZE', 'WATER'))],
        5: [((8, 1), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((8, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((9, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        6: [((4, 6), ('WATER',)), ((4, 7), ('WATER',)), ((4, 8), ('WATER',)), ((4, 9), ('WATER',)), ((3, 9), ('WATER',)), ((3, 8), ('WATER',)), ((3, 7), ('WATER',)), ((2, 7), ('WATER',)), ((2, 8), ('WATER',)), ((2, 9), ('WATER',)), ((1, 9), ('WATER',))],
        7: [((5, 3), ('WATER',)), ((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((9, 1), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        8: [((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((1, 3), ('WATER',)), ((1, 2), ('FERTILIZE', 'WATER')), ((1, 1), ('WATER',)), ((1, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        9: [((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((0, 2), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((0, 1), ('WATER',))],
        10: [((3, 6), ('WATER',)), ((2, 6), ('WATER',)), ((1, 6), ('WATER',)), ((1, 7), ('WATER',)), ((1, 8), ('WATER',)), ((0, 8), ('WATER',)), ((0, 7), ('WATER',)), ((0, 6), ('WATER',)), ((0, 5), ('WATER',)), ((1, 5), ('WATER',))],
    },
    16: {
        0: [((4, 6), ('WATER',)), ((3, 6), ('WATER',)), ((3, 7), ('WATER',)), ((2, 7), ('WATER',)), ((2, 8), ('WATER',)), ((2, 9), ('WATER',)), ((1, 9), ('WATER',))],
        1: [((4, 7), ('WATER',)), ((4, 8), ('WATER',)), ((3, 8), ('WATER',)), ((3, 9), ('WATER',)), ((4, 9), ('WATER',))],
        2: [((1, 5), ('WATER',)), ((0, 5), ('WATER',)), ((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((0, 2), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((0, 1), ('WATER',)), ((0, 0), ('WATER',))],
        3: [((5, 3), ('HARVEST',)), ((7, 2), ('FERTILIZE', 'WATER')), ((8, 2), ('FERTILIZE', 'WATER')), ((8, 1), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((7, 1), ('FERTILIZE', 'WATER'))],
        4: [((3, 1), ('WATER',)), ((2, 1), ('FERTILIZE', 'WATER')), ((2, 2), ('WATER',)), ((1, 2), ('FERTILIZE', 'WATER')), ((1, 1), ('WATER',)), ((1, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        5: [((6, 1), ('FERTILIZE', 'WATER')), ((6, 0), ('FERTILIZE', 'WATER')), ((7, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((8, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        6: [((9, 4), ('FERTILIZE', 'WATER')), ((9, 1), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((9, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        7: [((3, 5), ('WATER',)), ((2, 5), ('WATER',)), ((2, 6), ('WATER',)), ((1, 6), ('WATER',)), ((0, 6), ('WATER',)), ((0, 7), ('WATER',)), ((0, 8), ('WATER',)), ((1, 8), ('WATER',)), ((1, 7), ('WATER',))],
        8: [((5, 1), ('FERTILIZE', 'WATER')), ((5, 0), ('FERTILIZE', 'WATER')), ((4, 0), ('WATER',)), ((3, 0), ('FERTILIZE', 'WATER')), ((2, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        9: [((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((8, 3), ('FERTILIZE', 'WATER')), ((9, 3), ('FERTILIZE', 'WATER')), ((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        10: [((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((1, 3), ('WATER',)), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        11: [],
        12: [((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        13: [((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
    },
    18: {
        0: [((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((1, 4), ('WATER',)), ((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        1: [],
        2: [((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        3: [((4, 6), ('WATER',)), ((3, 6), ('WATER',)), ((3, 7), ('WATER',)), ((3, 8), ('WATER',))],
        4: [((2, 3), ('WATER',)), ((2, 2), ('FERTILIZE', 'WATER')), ((1, 2), ('WATER',)), ((1, 1), ('HARVEST',)), ((1, 0), ('WATER',)), ((0, 0), ('FERTILIZE', 'WATER')), ((0, 1), ('HARVEST',)), ((0, 2), ('WATER',))],
        5: [((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((5, 3), ('HARVEST',)), ((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((8, 3), ('WATER',)), ((9, 3), ('WATER',)), ((9, 4), ('WATER',))],
        6: [((3, 5), ('WATER',)), ((2, 5), ('WATER',)), ((2, 6), ('WATER',)), ((1, 6), ('WATER',)), ((1, 7), ('WATER',)), ((0, 7), ('WATER',)), ((0, 6), ('WATER',)), ((0, 5), ('WATER',)), ((1, 5), ('WATER',))],
        7: [],
        8: [((4, 2), ('WATER',)), ((3, 2), ('WATER',)), ((3, 1), ('FERTILIZE', 'WATER')), ((2, 1), ('WATER',)), ((2, 0), ('WATER',)), ((3, 0), ('WATER',)), ((4, 0), ('FERTILIZE', 'WATER')), ((4, 1), ('WATER',))],
        9: [((5, 1), ('WATER',)), ((5, 0), ('WATER',)), ((6, 0), ('WATER',)), ((6, 1), ('WATER',)), ((7, 1), ('WATER',)), ((8, 1), ('WATER',)), ((9, 1), ('WATER',)), ((9, 0), ('WATER',)), ((8, 0), ('WATER',)), ((7, 0), ('WATER',))],
        10: [((4, 7), ('WATER',)), ((4, 8), ('WATER',)), ((4, 9), ('WATER',)), ((3, 9), ('WATER',)), ((2, 9), ('WATER',)), ((1, 9), ('WATER',)), ((0, 9), ('WATER',)), ((0, 8), ('WATER',)), ((1, 8), ('WATER',)), ((2, 8), ('WATER',)), ((2, 7), ('WATER',))],
        11: [((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 2), ('WATER',)), ((8, 2), ('WATER',)), ((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
    },
    23: {
        0: [((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        1: [((3, 5), ('FERTILIZE', 'WATER')), ((2, 5), ('FERTILIZE', 'WATER')), ((2, 7), ('FERTILIZE', 'WATER')), ((2, 8), ('FERTILIZE', 'WATER')), ((1, 8), ('FERTILIZE', 'WATER')), ((1, 9), ('FERTILIZE', 'WATER', 'HARVEST'))],
        2: [((3, 1), ('FERTILIZE', 'WATER')), ((3, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((2, 0), ('FERTILIZE', 'WATER')), ((1, 0), ('FERTILIZE', 'WATER')), ((0, 0), ('FERTILIZE', 'WATER'))],
        3: [((8, 4), ('HARVEST',)), ((8, 3), ('HARVEST', 'DIG')), ((8, 2), ('HARVEST', 'DIG')), ((7, 2), ('HARVEST', 'DIG')), ((7, 1), ('HARVEST', 'DIG'))],
        4: [((4, 6), ('FERTILIZE', 'WATER')), ((3, 6), ('FERTILIZE', 'WATER')), ((3, 7), ('FERTILIZE', 'WATER')), ((3, 8), ('FERTILIZE', 'WATER'))],
        5: [((5, 2), ('HARVEST',)), ((3, 2), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((2, 2), ('FERTILIZE', 'WATER')), ((1, 2), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((0, 2), ('FERTILIZE', 'WATER'))],
        6: [((2, 3), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((2, 1), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((1, 1), ('WATER',)), ((0, 1), ('WATER', 'HARVEST'))],
        7: [((9, 4), ('HARVEST', 'DIG')), ((9, 3), ('HARVEST', 'DIG')), ((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((9, 1), ('FERTILIZE', 'WATER')), ((9, 0), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        8: [((4, 2), ('FERTILIZE', 'WATER')), ((4, 1), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((4, 0), ('FERTILIZE', 'WATER')), ((5, 0), ('HARVEST', 'DIG')), ((6, 0), ('HARVEST', 'DIG'))],
        9: [((4, 5), ('HARVEST',)), ((4, 7), ('FERTILIZE', 'WATER')), ((4, 8), ('FERTILIZE', 'WATER')), ((4, 9), ('FERTILIZE', 'WATER', 'HARVEST')), ((3, 9), ('FERTILIZE', 'WATER', 'HARVEST')), ((2, 9), ('FERTILIZE', 'WATER', 'HARVEST'))],
        10: [((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        11: [((5, 1), ('HARVEST', 'DIG')), ((6, 1), ('HARVEST', 'DIG')), ((7, 0), ('FERTILIZE', 'WATER')), ((8, 0), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((8, 1), ('FERTILIZE', 'WATER'))],
        12: [((1, 4), ('FERTILIZE', 'WATER')), ((1, 3), ('FERTILIZE', 'WATER')), ((1, 5), ('FERTILIZE', 'WATER')), ((0, 5), ('FERTILIZE', 'WATER')), ((0, 6), ('FERTILIZE', 'WATER')), ((1, 6), ('FERTILIZE', 'WATER'))],
        13: [((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((7, 3), ('HARVEST',)), ((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((6, 2), ('HARVEST',))],
        14: [((2, 6), ('FERTILIZE', 'WATER')), ((1, 7), ('FERTILIZE', 'WATER')), ((0, 7), ('FERTILIZE', 'WATER')), ((0, 8), ('FERTILIZE', 'WATER', 'HARVEST')), ((0, 9), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
    },
    24: {
        0: [((3, 1), ('WATER',)), ((2, 0), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((4, 0), ('WATER',)), ((7, 0), ('WATER', 'HARVEST', 'PLANT', 'WATER'))],
        1: [((5, 3), ('FERTILIZE', 'WATER')), ((5, 2), ('FERTILIZE', 'WATER')), ((6, 2), ('FERTILIZE', 'WATER')), ((7, 1), ('BUILD',)), ((8, 1), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER'))],
        2: [((4, 7), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((4, 8), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((4, 9), ('HARVEST',)), ((3, 9), ('HARVEST',)), ((2, 9), ('HARVEST',)), ((1, 9), ('HARVEST',))],
        3: [((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        4: [((1, 4), ('FERTILIZE', 'WATER')), ((1, 5), ('FERTILIZE', 'WATER')), ((1, 6), ('FERTILIZE', 'WATER')), ((0, 6), ('HARVEST',)), ((0, 7), ('HARVEST',)), ((0, 8), ('HARVEST',)), ((1, 8), ('HARVEST',)), ((1, 7), ('HARVEST',))],
        5: [((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((9, 1), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((8, 0), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        6: [((4, 6), ('WATER',)), ((3, 6), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((3, 7), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((3, 8), ('HARVEST',)), ((2, 8), ('HARVEST',))],
        7: [((3, 5), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((2, 5), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((2, 6), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((2, 7), ('WATER',))],
        8: [((4, 2), ('WATER',)), ((2, 2), ('WATER',)), ((1, 1), ('HARVEST', 'DIG')), ((1, 0), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((0, 0), ('WATER',)), ((0, 1), ('HARVEST', 'DIG'))],
        9: [((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 3), ('FERTILIZE', 'WATER')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((8, 4), ('FERTILIZE', 'WATER'))],
        10: [((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((0, 2), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER'))],
        11: [((4, 5), ('FERTILIZE', 'WATER')), ((0, 5), ('FERTILIZE', 'WATER')), ((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((1, 3), ('FERTILIZE', 'WATER'))],
    },
    25: {
        0: [((2, 7), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((1, 7), ('FERTILIZE', 'WATER', 'HARVEST')), ((1, 8), ('WATER',)), ((0, 8), ('FERTILIZE', 'WATER')), ((0, 7), ('FERTILIZE', 'WATER'))],
        1: [((5, 1), ('FERTILIZE', 'WATER')), ((4, 1), ('FERTILIZE', 'WATER')), ((3, 1), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((3, 0), ('FERTILIZE', 'WATER'))],
        2: [((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        3: [((4, 5), ('HARVEST',)), ((4, 6), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((1, 6), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((0, 6), ('FERTILIZE', 'WATER'))],
        4: [((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((4, 2), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER'))],
        5: [((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((7, 3), ('HARVEST',)), ((7, 2), ('FERTILIZE', 'WATER')), ((8, 0), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        6: [((4, 9), ('FERTILIZE', 'WATER')), ((3, 9), ('FERTILIZE', 'WATER')), ((3, 8), ('WATER',)), ((2, 8), ('WATER',)), ((2, 9), ('FERTILIZE', 'WATER')), ((1, 9), ('WATER',)), ((0, 9), ('FERTILIZE', 'WATER'))],
        7: [((8, 4), ('HARVEST',)), ((8, 3), ('FERTILIZE', 'WATER')), ((8, 2), ('FERTILIZE', 'WATER')), ((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((9, 3), ('FERTILIZE', 'WATER')), ((9, 4), ('FERTILIZE', 'WATER'))],
        8: [((3, 2), ('FERTILIZE', 'WATER')), ((2, 1), ('FERTILIZE', 'WATER')), ((0, 1), ('FERTILIZE', 'WATER', 'DIG')), ((0, 0), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER'))],
        9: [((5, 3), ('WATER',)), ((5, 2), ('HARVEST',)), ((6, 2), ('HARVEST',)), ((6, 1), ('FERTILIZE', 'WATER')), ((6, 0), ('FERTILIZE', 'WATER')), ((5, 0), ('FERTILIZE', 'WATER')), ((4, 0), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER'))],
        10: [((2, 3), ('FERTILIZE', 'WATER')), ((1, 3), ('WATER', 'HARVEST', 'PLANT', 'WATER')), ((1, 2), ('FERTILIZE', 'WATER')), ((2, 2), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER'))],
        11: [((1, 5), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((0, 5), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER'))],
        12: [((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((1, 4), ('WATER', 'HARVEST', 'HARVEST', 'PLANT', 'WATER')), ((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
    },
    26: {
        0: [((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        1: [((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((5, 3), ('WATER', 'HARVEST', 'HARVEST')), ((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((6, 2), ('WATER',)), ((6, 1), ('FERTILIZE', 'WATER')), ((5, 1), ('WATER',)), ((4, 1), ('WATER',))],
        2: [((2, 5), ('FERTILIZE', 'WATER')), ((2, 3), ('FERTILIZE', 'WATER')), ((2, 1), ('FERTILIZE', 'WATER')), ((1, 1), ('FERTILIZE', 'WATER')), ((1, 2), ('FERTILIZE', 'WATER')), ((0, 2), ('FERTILIZE', 'WATER'))],
        3: [((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((7, 3), ('WATER',)), ((7, 2), ('WATER',)), ((8, 0), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        4: [((4, 7), ('FERTILIZE', 'WATER')), ((3, 7), ('FERTILIZE', 'WATER')), ((3, 8), ('HARVEST', 'DIG')), ((2, 8), ('HARVEST', 'DIG')), ((1, 8), ('HARVEST', 'DIG')), ((1, 7), ('HARVEST', 'DIG'))],
        5: [((4, 5), ('WATER',)), ((4, 8), ('FERTILIZE', 'WATER')), ((4, 9), ('HARVEST', 'DIG')), ((3, 9), ('HARVEST', 'DIG')), ((2, 9), ('HARVEST', 'DIG')), ((1, 9), ('HARVEST', 'DIG'))],
        6: [((3, 5), ('FERTILIZE', 'WATER')), ((3, 6), ('FERTILIZE', 'WATER')), ((2, 6), ('FERTILIZE', 'WATER')), ((0, 6), ('HARVEST', 'DIG')), ((0, 7), ('HARVEST', 'DIG')), ((0, 8), ('HARVEST', 'DIG')), ((0, 9), ('WATER',))],
        7: [((8, 4), ('WATER',)), ((8, 3), ('FERTILIZE', 'WATER')), ((8, 2), ('FERTILIZE', 'WATER')), ((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((9, 3), ('WATER',)), ((9, 4), ('FERTILIZE', 'WATER'))],
        8: [((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((3, 2), ('FERTILIZE', 'WATER')), ((3, 0), ('WATER',)), ((2, 0), ('FERTILIZE', 'WATER')), ((1, 0), ('FERTILIZE', 'WATER'))],
        9: [((5, 2), ('WATER',)), ((5, 0), ('FERTILIZE', 'WATER')), ((6, 0), ('FERTILIZE', 'WATER')), ((7, 0), ('FERTILIZE', 'WATER')), ((8, 1), ('FERTILIZE', 'WATER')), ((9, 1), ('FERTILIZE', 'WATER'))],
        10: [],
    },
    27: {
        0: [((4, 1), ('WATER', 'HARVEST', 'HARVEST')), ((3, 1), ('FERTILIZE', 'WATER')), ((3, 0), ('WATER', 'HARVEST', 'HARVEST')), ((4, 0), ('FERTILIZE', 'WATER')), ((5, 0), ('WATER', 'HARVEST')), ((5, 1), ('WATER', 'HARVEST', 'HARVEST'))],
        1: [((4, 6), ('FERTILIZE', 'WATER')), ((3, 6), ('FERTILIZE', 'WATER')), ((2, 7), ('FERTILIZE', 'WATER')), ((3, 7), ('FERTILIZE', 'WATER')), ((4, 7), ('FERTILIZE', 'WATER')), ((4, 8), ('FERTILIZE', 'WATER'))],
        2: [((4, 5), ('HARVEST',)), ((3, 5), ('FERTILIZE', 'WATER')), ((2, 5), ('WATER',)), ((2, 6), ('FERTILIZE', 'WATER')), ((1, 6), ('FERTILIZE', 'WATER')), ((0, 9), ('WATER', 'HARVEST', 'HARVEST'))],
        3: [((5, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((6, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((7, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((8, 4), ('HARVEST',)), ((9, 4), ('WATER', 'HARVEST', 'HARVEST'))],
        4: [((4, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((3, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((2, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((2, 3), ('WATER', 'HARVEST', 'HARVEST')), ((3, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST'))],
        5: [((4, 2), ('FERTILIZE', 'WATER')), ((3, 2), ('WATER', 'HARVEST', 'HARVEST')), ((2, 2), ('FERTILIZE', 'WATER')), ((2, 1), ('WATER', 'HARVEST', 'HARVEST')), ((2, 0), ('WATER',)), ((1, 0), ('FERTILIZE', 'WATER'))],
        6: [((1, 4), ('FERTILIZE', 'WATER')), ((1, 3), ('FERTILIZE', 'WATER')), ((1, 2), ('WATER', 'HARVEST', 'HARVEST')), ((0, 2), ('FERTILIZE', 'WATER')), ((0, 1), ('FERTILIZE', 'WATER')), ((0, 0), ('FERTILIZE', 'WATER'))],
        7: [((5, 2), ('HARVEST',)), ((6, 2), ('HARVEST',)), ((7, 2), ('WATER', 'HARVEST', 'HARVEST')), ((8, 2), ('WATER', 'HARVEST')), ((8, 1), ('FERTILIZE', 'WATER')), ((9, 1), ('FERTILIZE', 'WATER'))],
        8: [((4, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((7, 3), ('HARVEST',)), ((8, 3), ('WATER', 'HARVEST')), ((9, 2), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((9, 3), ('WATER', 'HARVEST', 'HARVEST'))],
        9: [((6, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((6, 1), ('WATER', 'HARVEST', 'HARVEST')), ((6, 0), ('WATER', 'HARVEST')), ((7, 0), ('FERTILIZE', 'WATER')), ((8, 0), ('FEED', 'CARE', 'COLLECT_FERTILIZER'))],
        10: [((1, 5), ('FERTILIZE', 'WATER')), ((0, 5), ('FERTILIZE', 'WATER')), ((0, 4), ('FEED', 'CARE', 'COLLECT_FERTILIZER', 'HARVEST')), ((0, 3), ('FEED', 'CARE', 'COLLECT_FERTILIZER')), ((1, 1), ('WATER',))],
    },
}
