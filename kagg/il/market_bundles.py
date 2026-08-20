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

from kagg.sim import farm as F
from kagg.sim import market as M

# `jax_sim.Actions` does not carry order lists. It carries per-product quantity vectors, a hire
# COUNT and a buy_land flag; `Game._order_book` compacts those into the ten order slots. A bundle is
# only useful if it round-trips through that representation exactly.
SELL, BUY_PRODUCT, BUY_SEED, BUY_ANIMAL, HIRE, BUY_LAND = (
    "SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL", "HIRE", "BUY_LAND")

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
        pairs.append((op, item))
    return tuple(sorted(pairs))


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
        rows.append((op, item, qty))
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
    for i, n in enumerate(fields.get("buy_animal") or ()):
        pairs += [(BUY_ANIMAL, M.ANIMALS[i])] * (1 if n > 0 else 0)
    pairs += [(HIRE, "")] * int(fields.get("hire") or 0)
    if fields.get("buy_land"):
        pairs.append((BUY_LAND, ""))
    return tuple(sorted(pairs))


def tables(vocab):
    """Static `[N_BUNDLES, ...]` lookups so a sampled bundle index decodes inside a jit.

    `to_sim_fields` is Python and cannot run on a traced array, so the same information is laid out
    once as arrays. `hire` is a COUNT column for the reason the module docstring gives, and
    `sell`/`buy_*` are counts too rather than flags -- a bundle naming the same product twice is a
    bundle that wants twice as much.

    Returns plain lists so the caller chooses the array library; `jax_act` wraps them in `jnp`.
    """
    n = vocab.size
    out = {
        "sell": [[0] * M.N_PRODUCTS for _ in range(n)],
        "buy_product": [[0] * M.N_PRODUCTS for _ in range(n)],
        "buy_seed": [[0] * F.N_CROPS for _ in range(n)],
        "buy_animal": [[0] * M.N_ANIMALS for _ in range(n)],
        "hire": [0] * n,
        "buy_land": [False] * n,
    }
    for i in range(n):
        fields = to_sim_fields(vocab.bundle(i), None)
        out["sell"][i] = list(fields["sell"])
        out["buy_product"][i] = list(fields["buy_product"])
        out["buy_seed"][i] = list(fields["buy_seed"])
        out["buy_animal"][i] = list(fields["buy_animal"])
        out["hire"][i] = fields["hire"]
        out["buy_land"][i] = fields["buy_land"]
    return out


def sell_table(vocab):
    """`[N_BUNDLES, N_PRODUCTS]` bool: does this bundle sell this product?

    The legality mask `jax_act.masks_for` needs exactly this and nothing else -- you cannot sell
    what the shed does not hold, and that is the one market constraint the agent cannot discover by
    trying.
    """
    return [[n > 0 for n in row] for row in tables(vocab)["sell"]]


def orders_from_heads(vocab, index, sell_bucket, buy_product_bucket, buy_seed_bucket,
                      sell_ladder, buy_ladder, products, crops, animals):
    """Sampled heads -> the environment's `market` list.

    The bundle names WHICH orders; the per-product quantity heads name HOW MANY. They are indexed
    differently -- the bundle is a sorted multiset, the quantity heads are one entry per product --
    so this is where the two are joined, once, rather than at each call site.

    A selected entry floors at one unit. Bucket 0 means "do nothing", which contradicts a bundle
    that named the product, and the bundle is the decision carrying the coordination. Same rule as
    `to_sim_fields` and `jax_act.to_sim_actions`; all three must agree or a policy plays differently
    depending on which decoder ran.
    """
    out = []
    for op, item in vocab.bundle(index):
        if op == HIRE:
            out.append([HIRE])
        elif op == BUY_LAND:
            out.append([BUY_LAND])
        elif op == SELL and item in products:
            n = max(1, int(sell_ladder[int(sell_bucket[products.index(item)])]))
            out.append([SELL, item, n])
        elif op == BUY_PRODUCT and item in products:
            n = max(1, int(buy_ladder[int(buy_product_bucket[products.index(item)])]))
            out.append([BUY_PRODUCT, item, n])
        elif op == BUY_SEED and item in crops:
            n = max(1, int(buy_ladder[int(buy_seed_bucket[crops.index(item)])]))
            out.append([BUY_SEED, item, n])
        elif op == BUY_ANIMAL and item in animals:
            out.append([BUY_ANIMAL, item, 1])
    return out
