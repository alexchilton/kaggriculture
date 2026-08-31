"""`jax_policy.Policy`'s forward pass, in numpy, so a trained net can ship in a submission.

    from kagg.rl import numpy_policy as NP
    heads, value = NP.apply(NP.pack(params), tiles, units, glob)

WHY THIS EXISTS
---------------
A submission is one self-contained `main.py`, and the competition runtime has never had `jax` or
`flax` -- every artifact this project has shipped imports only the standard library, `numpy` and
`kaggle_environments`. Nothing about a trained forward pass needs jax: it is Dense layers, layer
norms, softmax attention and a gelu. So the net can ship, but only through a second implementation.

**A second implementation of the network has to agree with the first one forever.** That is the same
trap the two observation encoders fell into -- they disagreed on 23 dead unit slots for weeks and it
was invisible until someone diffed them. `tests/test_the_numpy_net_matches_the_flax_net.py` is what
makes this safe: it runs both on real boards and requires the argmax of every head to be identical
and the logits to match to a tight tolerance. If that test is not run, this file is a liability.

WHAT IT MIRRORS, exactly (`jax_policy.py:150-290`)
--------------------------------------------------
    Dense(d_model) on tiles / units / glob, separately        Dense_0 / Dense_1 / Dense_2
    + learned tile_pos [1, 100, d] and unit_pos [1, 24, d]
    concat [glob(1 token), tiles(100), units(24)]  -> 125 tokens
    n_layers x Block:
        h = LayerNorm(x);  x = x + MHA(h, h)                  pre-norm, residual
        h = LayerNorm(x);  x = x + Dense(4d) -> gelu -> Dense(d)
    final LayerNorm
    gtok = x[:, 0]           utok = x[:, 1 + n_tiles:]
    heads off utok: op, crop, item, qty  (the last three reshaped to an op axis)
    heads off gtok: bundle, qty_sell, qty_buy_product, qty_buy_seed
    value = sigmoid(Dense(1)(gtok))                            rescaled by `value_margin`

Flax's `MultiHeadDotProductAttention` keeps `query`/`key`/`value` kernels as `[d, n_heads, head_dim]`
and `out` as `[n_heads, head_dim, d]`, with per-head biases. The scale is `1/sqrt(head_dim)`, applied
to the query before the dot product -- not to the logits after -- which is the same number either
way but is written here as flax writes it so a reader can check them side by side.

**gelu must be the exact variant.** `nn.gelu` defaults to the tanh approximation, and the erf form
differs by up to 1e-3 per unit -- small per layer, and this is three layers deep with residuals.
"""

import numpy as np

#: `nn.LayerNorm`'s default. Flax normalises with `1 / sqrt(var + eps)` and no mean-centering of the
#: scale, so this constant has to match or every activation is slightly off from the first layer on.
LN_EPS = 1e-6


def pack(params):
    """A flax params pytree (possibly jax arrays) -> nested dicts of float32 numpy arrays."""
    if hasattr(params, "items"):
        return {k: pack(v) for k, v in params.items()}
    return np.asarray(params, dtype=np.float32)


def _p(params):
    """Unwrap the outer `{"params": ...}` collection if it is there."""
    return params["params"] if "params" in params else params


def dense(x, p):
    return x @ p["kernel"] + p["bias"]


def layer_norm(x, p):
    mu = x.mean(axis=-1, keepdims=True)
    var = ((x - mu) ** 2).mean(axis=-1, keepdims=True)
    return (x - mu) / np.sqrt(var + LN_EPS) * p["scale"] + p["bias"]


def gelu(x):
    """`nn.gelu`'s default: the tanh approximation, NOT the erf form."""
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x ** 3)))


def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


def attention(x, p):
    """Self-attention, laid out the way flax lays it out.

    `x` is `[N, T, d]`. q/k/v kernels are `[d, H, hd]` and biases `[H, hd]`; `out` is `[H, hd, d]`.
    No mask: every token attends to every other, which is what `Block.__call__` does -- it passes
    `h` as both query and key/value and supplies no `mask` argument.
    """
    q = np.einsum("ntd,dhk->nthk", x, p["query"]["kernel"]) + p["query"]["bias"]
    k = np.einsum("ntd,dhk->nthk", x, p["key"]["kernel"]) + p["key"]["bias"]
    v = np.einsum("ntd,dhk->nthk", x, p["value"]["kernel"]) + p["value"]["bias"]
    q = q / np.sqrt(q.shape[-1])                       # flax scales the QUERY, not the logits
    logits = np.einsum("nqhk,nvhk->nhqv", q, k)
    w = softmax(logits, axis=-1)
    o = np.einsum("nhqv,nvhk->nqhk", w, v)
    return np.einsum("nqhk,hkd->nqd", o, p["out"]["kernel"]) + p["out"]["bias"]


def block(x, p):
    h = layer_norm(x, p["LayerNorm_0"])
    x = x + attention(h, p["MultiHeadDotProductAttention_0"])
    h = layer_norm(x, p["LayerNorm_1"])
    return x + dense(gelu(dense(h, p["Dense_0"])), p["Dense_1"])


def apply(params, tiles, units, glob, n_layers=3, value_margin=0.0):
    """`(heads, value)`, matching `jax_policy.Policy.__call__`.

    `tiles [N, 100, F]`, `units [N, 24, F]`, `glob [N, F]`. Head shapes and names are identical to
    the flax version, including the op axis on `crop`/`item`/`qty`.
    """
    p = _p(params)
    tiles = np.asarray(tiles, dtype=np.float32)
    units = np.asarray(units, dtype=np.float32)
    glob = np.asarray(glob, dtype=np.float32)
    n_tiles, n_units = tiles.shape[1], units.shape[1]

    t = dense(tiles, p["Dense_0"]) + p["tile_pos"]
    u = dense(units, p["Dense_1"]) + p["unit_pos"]
    g = dense(glob, p["Dense_2"])[:, None, :]

    x = np.concatenate([g, t, u], axis=1)
    for i in range(n_layers):
        x = block(x, p[f"Block_{i}"])
    x = layer_norm(x, p["LayerNorm_0"])

    gtok = x[:, 0]
    utok = x[:, 1 + n_tiles:]
    n = utok.shape[0]

    op = dense(utok, p["Dense_3"])
    n_ops = op.shape[-1]
    heads = {
        "op": op,
        "crop": dense(utok, p["Dense_4"]).reshape(n, n_units, n_ops, -1),
        "item": dense(utok, p["Dense_5"]).reshape(n, n_units, n_ops, -1),
        "qty": dense(utok, p["Dense_6"]).reshape(n, n_units, n_ops, -1),
        "bundle": dense(gtok, p["Dense_7"]),
        "qty_sell": dense(gtok, p["Dense_8"]).reshape(n, -1, _QTY),
        "qty_buy_product": dense(gtok, p["Dense_9"]).reshape(n, -1, _QTY),
        "qty_buy_seed": dense(gtok, p["Dense_10"]).reshape(n, -1, _QTY),
    }
    v = 1.0 / (1.0 + np.exp(-dense(gtok, p["Dense_11"])[..., 0]))
    if value_margin:
        v = v * (1.0 + 2.0 * value_margin) - value_margin
    return heads, v


#: Quantity classes per product. Read from `jax_policy` so the two cannot drift; the reshape above
#: needs it because the head is emitted flat as `N_PRODUCTS * MAX_QTY`.
def _max_qty():
    from kagg.rl.jax_policy import MAX_QTY
    return int(MAX_QTY)


_QTY = _max_qty()
