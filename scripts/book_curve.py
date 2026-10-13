"""What N units actually fetch, per crop, straight off `market_price`. No game needed.

`market_price(item, inventory)` is a pure function and a SELL walks it one unit at a time, so the
revenue for releasing N units into a book at inventory I is just a sum -- computable offline, in
microseconds, with no episode to run. That makes the per-crop question answerable directly:

    where does the curve bend, i.e. how many units can a crop absorb before the price collapses?

The measured contrast this explains: on episode 107642213 one agent put 249 STRAWBERRY into the book
and realised $21/unit while the other put in 84 and realised $61 -- same crop, same board, 3x the
price. MELON and WOOL are the same shape; WHEAT and CARROT are not.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kaggle_environments.envs.kaggriculture.kaggriculture as K

PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]


def revenue(prod, n, inv):
    """Total for selling n units one at a time from inventory `inv`."""
    tot, i = 0.0, inv
    for _ in range(n):
        tot += K.market_price(prod, i)
        i += 1
    return tot


def main():
    inv0 = K.MARKET_I0
    sizes = [1, 5, 10, 20, 40, 80, 160, 320]
    print(f"book opens at inventory {inv0}\n")
    print(f"{'product':12}{'price@open':>11}" +
          "".join(f"{'$/u @' + str(s):>10}" for s in sizes) + f"{'half-price at':>15}")
    for p in PRODUCTS:
        row = f"{p:12}{K.market_price(p, inv0):>11.0f}"
        for s in sizes:
            row += f"{revenue(p, s, inv0)/s:>10.0f}"
        # how many units before the marginal price is half the opening quote
        open_px, i, n = K.market_price(p, inv0), inv0, 0
        while K.market_price(p, i) > open_px / 2 and n < 5000:
            i += 1
            n += 1
        row += f"{(n if n < 5000 else -1):>15,}"
        print(row)
    print("\n'half-price at' = units that can be sold before the marginal quote halves.")
    print("A small number means a thin book: volume is what destroys the price, not the hour.")


if __name__ == "__main__":
    main()
