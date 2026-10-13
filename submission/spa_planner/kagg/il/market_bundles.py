"""The market as ONE categorical, not six independent heads.

**The measurement this exists for.** 78.7% of the teacher's player-turns carry no market action at
all (5,752 turns, `/home/alex/labels_pilot`, 2026-08-20). Every one of the six market heads
therefore has a base rate of overwhelmingly "no", and six independent "probably no" decisions
multiply into "certainly no". `CLAUDE.md` records the consequence already: greedy argmax over the
per-head marginals emits **zero** market orders while the marginals themselves discriminate 12:1 on
`buy_product`. The information is in the marginals; the product of them destroys it.

The failure is invisible offline. Per-head accuracy reads well because the loss measures marginals,
and the game consumes the joint -- which is how this project once shipped a checkpoint banking
exactly its $3,000 start.

**Sized on our own teacher, not on tetsuya.** 117 distinct bundles; the top 100 cover 99.70% and
the top 200 cover 100%. A 128-class head is therefore the whole distribution for ~16k parameters on
the global token, against a 726k-parameter net.

**Quantities are deliberately not part of the identity.** 52 of 116 non-empty bundles carry more
than one quantity vector and `SELL FERTILIZER/MILK/STRAWBERRY/WHEAT/WOOL` carries 48. They get their
own head conditioned on the drawn bundle, because a wrong quantity is graceful (sell 4 instead of 5)
and a wrong bundle is catastrophic (never sell at all).

**A bundle is a multiset, not a set.** `HIRE x10` is rank 2 in the teacher's vocabulary and is one
decision -- the sells in earlier order slots settle first and fund all ten hires in the same turn.
Collapsing it to a single HIRE is the d10 failure, where units 8 and 9 were never hired and 20
planned ops died with them.
"""

import collections

# **`jax_policy` is imported LOCALLY, at the two sites that need it, and that is load-bearing.**
# Only two integers are read from it -- `MAX_QTY` and `N_BUNDLES` -- but the import pulls flax, and
# this module is on the play path of a net-bearing submission (`kagg/agents/numpy_neural.py`). The
# competition runtime has never had jax or flax, so a module-level import here makes the bundle
# decoder unshippable for the sake of two numbers. `load_vocab` already did it this way.
from kagg.sim import farm as F
from kagg.sim import market as M
from kagg.sim.game import (
    MAX_ORDERS,
    ORDER_BUY_ANIMAL,
    ORDER_BUY_LAND,
    ORDER_BUY_PRODUCT,
    ORDER_BUY_SEED,
    ORDER_HIRE,
    ORDER_NONE,
    ORDER_SELL,
)

# `jax_sim.Actions` does not carry order lists. It carries per-product quantity vectors, a hire
# COUNT and a buy_land flag; `Game._order_book` compacts those into the ten order slots. A bundle is
# only useful if it round-trips through that representation exactly.
SELL, BUY_PRODUCT, BUY_SEED, BUY_ANIMAL, HIRE, BUY_LAND = (
    "SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL", "HIRE", "BUY_LAND")

#: **The order an agent writes orders in, which is the order the environment gives them slots in.**
#: `kagg/sim/game.py:70-77` defines it and `jax_sim._order_book` mirrors it, both because the
#: reference pairs the two players' i-th ORDERS rather than matching them by product.
#:
#: This is NOT the order a bundle stores. A bundle is a sorted multiset and that sort is
#: alphabetical, so SELL sorts last -- see `orders_from_heads`, which is where the two are
#: reconciled, and the test named there for what it cost.
# **Chosen by OUTCOME on the real environment, not by reading the teacher's list.**
#
# The same ten orders in a different sequence buy a different farm, because the shed capacity binds
# and slot i takes its money before slot i+1 is quoted. Measured 2026-08-22 on turn 0:
#
#     the tape's own sequence   bank 3000 -> 13    hands 5   shed {WHEAT 5, COW 2, SHEEP 2}
#     SELL SEED PROD ANIM HIRE  bank 3000 -> 484   hands 5   shed {WHEAT 6, COW 2, SHEEP 1}
#
# Both sheds hold nine items. Buying the wheat PRODUCT before the animals fills the last slot with
# wheat and costs a whole sheep, stranding $471. A sweep of every distinct ordering found eight that
# reproduce the tape exactly and two that lose two of the five hires outright.
#
# This one is in the winning set AND matches the teacher's own turn-0 sequence. SELL stays first for
# the reason below: a sell in the same turn funds the purchases after it.
# `tests/test_the_opening_orders_leave_the_shed_the_tape_has.py`.
SLOT_ORDER = (SELL, HIRE, BUY_ANIMAL, BUY_SEED, BUY_PRODUCT, BUY_LAND)

# Index 0 is always the empty bundle. It is the majority class, so it must be a real symbol the head
# can choose, never an absence expressed by falling off the vocabulary.
EMPTY = ()


def bundle_of(orders):
    """The market list for one turn -> its bundle: a sorted multiset of `(op, item)`.

    Sorted so that order within the turn does not create a second symbol for the same decision, and
    a tuple rather than a set so repeated ops survive.
    """
    pairs = []
    for o in (orders or ()):
        if not isinstance(o, (list, tuple)) or not o:
            continue
        op = str(o[0])
        item = str(o[1]) if len(o) > 1 and o[1] is not None else ""
        pairs.extend([(op, item)] * _multiplicity(op, o))
    return tuple(sorted(pairs))


def _multiplicity(op, order):
    """How many pairs one order contributes. One, except for animals.

    **Animals carry their count in the bundle, like HIRE, because nothing else can carry it.**
    `SELL`, `BUY_PRODUCT` and `BUY_SEED` each have a `qty_*` head that predicts the amount given
    the bundle. `BUY_ANIMAL` has none, so a single pair meant the count defaulted to 1 and
    `BUY_ANIMAL COW 2` was unplayable at any width -- 20 of the four teachers' 1451 trading turns,
    one of them turn 0, costing $900 of a $2,984 opening.
    `docs/the_second_cow_cannot_be_bought_2026-08-22.md`.

    `HIRE` needs nothing here: the teacher emits it as five separate orders, so its multiplicity
    already survives.
    """
    if op != BUY_ANIMAL or len(order) < 3:
        return 1
    try:
        return max(1, int(order[2]))
    except (TypeError, ValueError):
        return 1


def quantities_of(orders):
    """The quantity vector for one turn, aligned to `bundle_of`'s ordering.

    The conditioned head predicts this given the bundle. Missing quantities read as -1 so an order
    that names none is distinguishable from one that names zero.
    """
    rows = []
    for o in (orders or ()):
        if not isinstance(o, (list, tuple)) or not o:
            continue
        op = str(o[0])
        item = str(o[1]) if len(o) > 1 and o[1] is not None else ""
        qty = -1
        if len(o) > 2:
            try:
                qty = int(o[2])
            except (TypeError, ValueError):
                qty = -1
        # Aligned to `bundle_of`, which now repeats an animal pair per unit. Each repeat carries a
        # quantity of one, so `to_sim_fields`'s `+= qty` sums back to the count the teacher asked
        # for. Emitting the full quantity on every repeat would square it.
        n = _multiplicity(op, o)
        rows.extend([(op, item, 1 if n > 1 else qty)] * n)
    rows.sort(key=lambda r: (r[0], r[1]))
    return tuple(q for _, _, q in rows)


class Vocabulary:
    """Bundle <-> index, with the empty bundle pinned at 0 and an explicit fallback.

    `index` never raises. At play time the student can only emit vocabulary entries, but the LOSS
    sees teacher labels from games the vocabulary was not built on, and an exception there would
    stop a training run on the rarest symbol in the data.
    """

    def __init__(self, bundles):
        self._list = list(bundles)
        self._index = {b: i for i, b in enumerate(self._list)}

    @classmethod
    def from_bundles(cls, bundles, max_size=None):
        """Most frequent first, so truncation drops the tail and `coverage` says what it cost."""
        counts = collections.Counter(bundles)
        counts.setdefault(EMPTY, 0)
        ordered = [EMPTY] + [b for b, _ in counts.most_common() if b != EMPTY]
        if max_size is not None:
            ordered = ordered[:max_size]
        return cls(ordered)

    @property
    def size(self):
        return len(self._list)

    def index(self, bundle):
        """Unseen bundles fall back to EMPTY -- a labellable decision, not a crash."""
        return self._index.get(tuple(bundle), 0)

    def bundle(self, i):
        return self._list[int(i)]

    def coverage(self, bundles):
        """Fraction of `bundles` this vocabulary can express exactly. The sizing number."""
        bundles = list(bundles)
        if not bundles:
            return 1.0
        hit = sum(1 for b in bundles if tuple(b) in self._index)
        return hit / len(bundles)

    def to_sim_fields(self, i, quantities=None):
        """Index -> the fields `jax_sim.Actions` carries. See the module-level `to_sim_fields`."""
        return to_sim_fields(self.bundle(i), quantities)

    def to_orders(self, i, quantities=None):
        """Index -> a market list the environment accepts.

        `quantities` comes from the conditioned head and is aligned to the bundle's sorted order.
        """
        bundle = self.bundle(i)
        out = []
        for n, (op, item) in enumerate(bundle):
            order = [op] + ([item] if item else [])
            if quantities is not None and n < len(quantities) and quantities[n] >= 0:
                order.append(int(quantities[n]))
            out.append(order)
        return out


# ------------------------------------------------------------------- the sim's representation

def to_sim_fields(bundle, quantities=None):
    """A bundle (+ optional quantity vector) -> the fields `jax_sim.Actions` carries.

    **`hire` is a COUNT.** `jax_sim.py:258` documents it as "COUNT of hands to hire this turn, not a
    flag" and `:315` warns that "casting to bool here would collapse 'hire twice' to 'hire once'" --
    which is precisely what `jax_act.to_sim_actions` does today, because the policy's hire head is
    `Dense(2)`. The teacher's rank-2 bundle is `HIRE x10` in a single turn, 113 times in 5,752 turns,
    and a binary head cannot express it. That is the d10 failure: units 8 and 9 never hired, and 20
    planned ops dying with them. Counting the HIRE entries in the multiset fixes it by construction.

    `quantities` is aligned to the bundle's own sorted order. A missing or negative quantity means
    ONE unit, not zero -- a zero-quantity order is a no-op, and a teacher that names no quantity is
    naming a single unit.
    """
    sell = [0] * M.N_PRODUCTS
    buy_product = [0] * M.N_PRODUCTS
    buy_seed = [0] * F.N_CROPS
    buy_animal = [0] * M.N_ANIMALS
    hire = 0
    buy_land = False

    for n, (op, item) in enumerate(bundle):
        qty = 1
        if quantities is not None and n < len(quantities) and quantities[n] >= 0:
            qty = int(quantities[n])
        if op == HIRE:
            hire += 1
        elif op == BUY_LAND:
            buy_land = True
        elif op == SELL and item in M.PRODUCTS:
            sell[M.PRODUCTS.index(item)] += qty
        elif op == BUY_PRODUCT and item in M.PRODUCTS:
            buy_product[M.PRODUCTS.index(item)] += qty
        elif op == BUY_SEED and item in F.CROPS:
            buy_seed[F.CROPS.index(item)] += qty
        elif op == BUY_ANIMAL and item in M.ANIMALS:
            buy_animal[M.ANIMALS.index(item)] += qty

    return {"sell": sell, "buy_product": buy_product, "buy_seed": buy_seed,
            "buy_animal": buy_animal, "hire": hire, "buy_land": buy_land}


def from_sim_fields(fields):
    """The inverse: sim fields -> bundle.

    Labelling reads sim fields and playing writes them, so the two must agree or the loss trains on
    a different decision than the one the teacher made.
    """
    pairs = []
    for i, n in enumerate(fields.get("sell") or ()):
        pairs += [(SELL, M.PRODUCTS[i])] * (1 if n > 0 else 0)
    for i, n in enumerate(fields.get("buy_product") or ()):
        pairs += [(BUY_PRODUCT, M.PRODUCTS[i])] * (1 if n > 0 else 0)
    for i, n in enumerate(fields.get("buy_seed") or ()):
        pairs += [(BUY_SEED, F.CROPS[i])] * (1 if n > 0 else 0)
    # One pair PER ANIMAL, matching `bundle_of`. A flag here against a count there would break the
    # documented inverse and silently re-index every bundle that buys more than one.
    for i, n in enumerate(fields.get("buy_animal") or ()):
        pairs += [(BUY_ANIMAL, M.ANIMALS[i])] * max(0, int(n))
    pairs += [(HIRE, "")] * int(fields.get("hire") or 0)
    if fields.get("buy_land"):
        pairs.append((BUY_LAND, ""))
    return tuple(sorted(pairs))


def tables(vocab, pad_to=None):
    """Static `[N_BUNDLES, ...]` lookups so a sampled bundle index decodes inside a jit.

    **`pad_to` must match the head width.** The vocabulary is 197 and the head is 256, and a table
    of 197 rows cannot broadcast against a 256-wide mask. Worse than a crash: JAX clamps
    out-of-range gather indices under jit, so an unpadded table indexed at 200 would silently return
    row 196 -- a real, confidently-emitted, wrong order. Padding rows are all-zero, i.e. the empty
    bundle, and `sell_table` marks them illegal so they are never drawn in the first place.

    `to_sim_fields` is Python and cannot run on a traced array, so the same information is laid out
    once as arrays. `hire` is a COUNT column for the reason the module docstring gives, and
    `sell`/`buy_*` are counts too rather than flags -- a bundle naming the same product twice is a
    bundle that wants twice as much.

    Returns plain lists so the caller chooses the array library; `jax_act` wraps them in `jnp`.
    """
    n = int(pad_to or vocab.size)
    if n < vocab.size:
        raise ValueError("pad_to=%d is narrower than the vocabulary (%d): the head could not "
                         "express bundles the labels use" % (n, vocab.size))
    out = {
        "sell": [[0] * M.N_PRODUCTS for _ in range(n)],
        "buy_product": [[0] * M.N_PRODUCTS for _ in range(n)],
        "buy_seed": [[0] * F.N_CROPS for _ in range(n)],
        "buy_animal": [[0] * M.N_ANIMALS for _ in range(n)],
        "hire": [0] * n,
        "buy_land": [False] * n,
    }
    for i in range(vocab.size):
        fields = to_sim_fields(vocab.bundle(i), None)
        out["sell"][i] = list(fields["sell"])
        out["buy_product"][i] = list(fields["buy_product"])
        out["buy_seed"][i] = list(fields["buy_seed"])
        out["buy_animal"][i] = list(fields["buy_animal"])
        out["hire"][i] = fields["hire"]
        out["buy_land"][i] = fields["buy_land"]
    out.update(slot_tables(vocab, n))
    return out


#: `slot_src` values. Which quantity head, if any, supplies a slot's magnitude.
SRC_FIXED, SRC_SELL, SRC_BUY_PRODUCT, SRC_BUY_SEED = 0, 1, 2, 3


def slot_tables(vocab, pad_to=None):
    """Static `[N_BUNDLES, MAX_ORDERS]` order LISTS, in the sequence the environment receives them.

    **The sequence is a decision, and it was previously made twice.** `tables` above returns
    per-product quantity VECTORS, and `_order_book` lays those out in its own fixed sequence: sells,
    seeds, products, animals, HIRE, BUY_LAND. `orders_from_heads` -- the path to the REAL environment
    -- sorts by `SLOT_ORDER` instead. The two disagreed, and no test comparing bundle CONTENTS could
    see it, because a bundle is a sorted multiset either way.

    The environment settles slots in sequence: slot i takes its money and its shed space before slot
    i+1 is quoted. So the same bundle bought a different farm depending on which decoder ran, and the
    simulator's was the wrong one -- measured on the teacher's turn 0, bank $484 against the tape's
    $13, one sheep short. `tests/test_the_opening_orders_leave_the_shed_the_tape_has.py`.

    **Built by calling `orders_from_heads`, not by re-deriving it.** That is the point: there is one
    implementation of the sequence, and this is a static rendering of it. A future change to
    `SLOT_ORDER` moves both paths together or neither.

    Quantities cannot be baked in -- they come from heads sampled per turn -- so each slot records
    WHERE its magnitude comes from: `slot_src` names the head and `slot_item` the entry to gather.
    `SRC_FIXED` slots (HIRE, BUY_LAND, BUY_ANIMAL) carry their count in `slot_qty` directly, because
    no head supplies it: HIRE and BUY_LAND are atomic, and the animal count lives in the bundle.
    """
    n = int(pad_to or vocab.size)
    from kagg.rl import jax_policy as P            # local: see the note at the top of the file
    width = P.MAX_QTY - 1
    ones_p = [width] * M.N_PRODUCTS
    ones_c = [width] * F.N_CROPS
    op_code = {SELL: ORDER_SELL, BUY_SEED: ORDER_BUY_SEED, BUY_PRODUCT: ORDER_BUY_PRODUCT,
               BUY_ANIMAL: ORDER_BUY_ANIMAL, HIRE: ORDER_HIRE, BUY_LAND: ORDER_BUY_LAND}
    item_space = {SELL: M.PRODUCTS, BUY_PRODUCT: M.PRODUCTS, BUY_SEED: F.CROPS,
                  BUY_ANIMAL: M.ANIMALS}
    src_of = {SELL: SRC_SELL, BUY_PRODUCT: SRC_BUY_PRODUCT, BUY_SEED: SRC_BUY_SEED}

    slot_op = [[ORDER_NONE] * MAX_ORDERS for _ in range(n)]
    slot_item = [[0] * MAX_ORDERS for _ in range(n)]
    slot_src = [[SRC_FIXED] * MAX_ORDERS for _ in range(n)]
    slot_qty = [[0] * MAX_ORDERS for _ in range(n)]

    for i in range(vocab.size):
        # The quantities are placeholders; only op, item and the ANIMAL coalescing are read back.
        orders = orders_from_heads(vocab, i, ones_p, ones_p, ones_c,
                                   list(M.PRODUCTS), list(F.CROPS), list(M.ANIMALS))
        for k, o in enumerate(orders[:MAX_ORDERS]):
            op = o[0]
            slot_op[i][k] = op_code[op]
            slot_item[i][k] = item_space[op].index(o[1]) if op in item_space else 0
            slot_src[i][k] = src_of.get(op, SRC_FIXED)
            # Only meaningful for SRC_FIXED. An animal order carries the coalesced count; HIRE and
            # BUY_LAND are atomic and take one slot each, so their quantity is 1.
            slot_qty[i][k] = int(o[2]) if len(o) > 2 else 1

    return {"slot_op": slot_op, "slot_item": slot_item,
            "slot_src": slot_src, "slot_qty": slot_qty}


def valid_table(vocab, pad_to=None):
    """`[N_BUNDLES]` bool: is this index a real vocabulary entry, or padding?

    This is the ONLY market legality `jax_act.masks_for` enforces. It used to refuse any bundle
    selling a product the shed lacked; that rule was removed on measurement -- the reference simply
    declines an unbacked sell (`reference/kaggriculture.py:653`), 48.75% of the teacher's own SELL
    orders have a pre-turn shed of zero for that product, and the BC loss is permissive, so the
    strict mask vetoed bundles the student had been trained to emit and handed their probability to
    a different trade.

    Padding must still be refused. JAX clamps an out-of-range gather under jit instead of raising,
    so a selectable padding index decodes as the highest real bundle: a wrong order, emitted
    confidently, with nothing to read anywhere.
    """
    n = int(pad_to or vocab.size)
    if n < vocab.size:
        raise ValueError("pad_to=%d is narrower than the vocabulary (%d)" % (n, vocab.size))
    return [i < vocab.size for i in range(n)]


def sell_table(vocab, pad_to=None):
    """`[N_BUNDLES, N_PRODUCTS]` bool: does this bundle sell this product?

    The legality mask `jax_act.masks_for` needs exactly this and nothing else -- you cannot sell
    what the shed does not hold, and that is the one market constraint the agent cannot discover by
    trying.

    **Padding rows are marked as selling a sentinel the shed can never hold**, so `masks_for` rules
    them illegal. An all-zero padding row would read as the empty bundle and be perfectly legal,
    which would let the sampler draw a dead index that gathers back to a real bundle under jit.
    """
    n = int(pad_to or vocab.size)
    rows = [[x > 0 for x in row] for row in tables(vocab, pad_to=n)["sell"]]
    for i in range(vocab.size, n):
        # Every product at once: no shed ever holds all nine, so this is unconditionally illegal.
        rows[i] = [True] * M.N_PRODUCTS
    return rows


def clamp_qty(n):
    """A raw quantity -> the class index the quantity heads use. The index IS the quantity.

    Clamped, never wrapped. The teacher's largest BUY_PRODUCT is 134 against a 64-wide head, and
    `134 % 64 == 6` would be a different order emitted with full confidence. Clamping understates a
    rare huge purchase; wrapping silently replaces it.

    This is done here, in ordinary Python at the label end, because JAX clamps out-of-range gather
    indices under jit without raising -- so an unclamped label would train the head toward a class
    that exists and decode to something else entirely, with nothing to read anywhere.
    """
    from kagg.rl import jax_policy as P            # local: see the note at the top of the file
    return int(max(0, min(int(n), P.MAX_QTY - 1)))


def orders_from_heads(vocab, index, qty_sell, qty_buy_product, qty_buy_seed,
                      products, crops, animals):
    """Sampled heads -> the environment's `market` list.

    The bundle names WHICH orders; the per-product quantity heads name HOW MANY. They are indexed
    differently -- the bundle is a sorted multiset, the quantity heads are one entry per product --
    so this is where the two are joined, once, rather than at each call site.

    **The quantity head's class index is the quantity itself.** It used to be a rung on
    `SELL_BUCKETS`/`BUY_BUCKETS`, which cost a measured 27.2% on SELL and 35.3% on BUY_PRODUCT
    against a teacher whose numbers are known exactly. See the comment on `jax_policy.MAX_QTY`.

    A selected entry floors at one unit. Class 0 means "do nothing", which contradicts a bundle that
    named the product, and the bundle is the decision carrying the coordination. Same rule as
    `to_sim_fields` and `jax_act.to_sim_actions`; all three must agree or a policy plays differently
    depending on which decoder ran.

    **The emitted ORDER matters, and it is not the stored order.** A bundle is a sorted multiset and
    that sort is alphabetical, which puts SELL last -- so walking the bundle verbatim emitted every
    purchase and hire BEFORE the sell that funds it. The environment settles slots in sequence: slot
    i takes its money before slot i+1 is quoted, so those purchases are refused on a thin bank. Both
    simulators lay slots out in `SLOT_ORDER` below (`game.py:70-77`, `jax_sim._order_book`), which is
    the order the teacher writes and the reason the module docstring gives for hires being funded by
    the same turn's sells. This is where the two are reconciled.

    It could only ever fail in the real environment -- every sim-side path already used the correct
    order -- which is exactly where DAgger rolls out.
    `tests/test_the_orders_go_out_in_the_order_the_bank_needs.py` pins it.
    """
    out = []
    for op, item in vocab.bundle(index):
        if op == HIRE:
            out.append([HIRE])
        elif op == BUY_LAND:
            out.append([BUY_LAND])
        elif op == SELL and item in products:
            out.append([SELL, item, max(1, int(qty_sell[products.index(item)]))])
        elif op == BUY_PRODUCT and item in products:
            out.append([BUY_PRODUCT, item, max(1, int(qty_buy_product[products.index(item)]))])
        elif op == BUY_SEED and item in crops:
            out.append([BUY_SEED, item, max(1, int(qty_buy_seed[crops.index(item)]))])
        elif op == BUY_ANIMAL and item in animals:
            # **Repeats COALESCE into one order carrying the count.** The bundle repeats the pair
            # per animal, because no `qty_buy_animal` head exists to carry it -- but a turn holds
            # only TEN orders and the teacher's opening uses exactly ten. Emitting `COW 1` twice
            # instead of `COW 2` spends a second slot, pushes the turn to twelve, and the tail --
            # two HIREs -- is truncated away. That trades the second cow for two hands.
            # Caught by the round-trip audit; pinned by
            # `tests/test_the_second_cow_survives_the_bundle.py`.
            same = next((o for o in out if o[0] == BUY_ANIMAL and o[1] == item), None)
            if same is None:
                out.append([BUY_ANIMAL, item, 1])
            else:
                same[2] += 1
    # Stable, so orders of the same kind keep the vocabulary's own ordering and two decodes of one
    # bundle are always byte-identical.
    out.sort(key=lambda o: SLOT_ORDER.index(o[0]))
    return out


DEFAULT_VOCAB = "data/il/bundle_vocab.json"


def load_vocab(path=DEFAULT_VOCAB, max_size=None):
    """Load the vocabulary artifact. It must be the SAME file everywhere.

    Labelling, fitting and playing all index bundles through this. If any of them uses a different
    file every index means something else, and nothing offline shows it because every index is still
    a valid index -- the policy simply plays a different order than the one it learned.

    `max_size` defaults to the head width, so a vocabulary that outgrew the head raises here rather
    than silently truncating into a bundle the policy can never emit.
    """
    import json
    import pathlib

    from kagg.rl import jax_policy as _P

    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(
            "no bundle vocabulary at %s -- build it with scripts/build_bundle_vocab.py. It is an "
            "artifact, not a constant, and guessing one silently re-indexes every market decision."
            % p)
    raw = json.loads(p.read_text())
    # **Index 0 means DO NOTHING.** `Vocabulary.index` returns 0 for any basket it does not hold,
    # so a file with a real basket at entry 0 breaks in both directions at once: every unexpressible
    # teacher turn is labelled as that basket, and every genuinely silent turn is too -- then the
    # student plays it. `from_bundles` pins EMPTY; a file loaded here bypasses that, so check it.
    if raw and raw[0]:
        raise ValueError(
            "vocabulary at %s has %r at index 0. Index 0 means 'place no orders' everywhere it is "
            "read, so this file teaches that basket on every silent turn and plays it back. Put "
            "the empty bundle first." % (p, raw[0]))
    n = int(max_size or _P.N_BUNDLES)
    if len(raw) > n:
        raise ValueError("vocabulary at %s has %d bundles against a %d-wide head: %d bundles could "
                         "never be emitted" % (p, len(raw), n, len(raw) - n))
    return Vocabulary([tuple(tuple(pair) for pair in b) for b in raw])
