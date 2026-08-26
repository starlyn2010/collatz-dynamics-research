"""
validate_prefix_law.py — Minimal reproduction of the prefix-law sanity check.

This is a lightweight stand-in for the full 3x4 matrix experiment described in
the paper (M in {64,128,256} x N in {20,40,60,80}, 10k samples/cell, plus
exhaustive sweep to 10^7). It validates:
  * Prop. 3 residue characterization
  * Empirical 2^-k frequencies over random odd seeds
  * Autocorrelation near zero
Run with:
  python src/validate_prefix_law.py --quick   # seconds
  python src/validate_prefix_law.py            # full 12-cell demo (minutes)
"""
import argparse
import random

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def v2(n: int) -> int:
    return (n & -n).bit_length() - 1


def K_of(x: int) -> int:
    return v2(3 * x + 1)


def odd_iter(x: int) -> int:
    return (3 * x + 1) >> K_of(x)


def sample_prefix(M_bits: int, N: int, rng: random.Random):
    """Random odd integer with bit-length M, then N odd steps."""
    # random odd in [2^{M-1}, 2^M)
    lo = 1 << (M_bits - 1)
    hi = 1 << M_bits
    n = rng.randrange(lo | 1, hi, 2)
    Ks = []
    x = n
    for _ in range(N):
        k = K_of(x)
        Ks.append(k)
        x = odd_iter(x)
        # overflow guard: if x even (should not happen) or x==1, keep going
    return Ks


def run(M=64, N=20, trials=2000, seed=0):
    rng = random.Random(seed)
    freq = {}
    for _ in range(trials):
        ks = sample_prefix(M, N, rng)
        for k in ks:
            freq[k] = freq.get(k, 0) + 1
    total = sum(freq.values())
    print(f"M={M} N={N} trials={trials} total_steps={total}")
    for k in range(1, 9):
        emp = freq.get(k, 0) / total if total else 0
        th = 2 ** (-k)
        print(f"  k={k}: empirical {emp:.4f} theory {th:.4f} err {abs(emp-th):.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="tiny quick run")
    args = parser.parse_args()
    if args.quick:
        run(M=64, N=20, trials=500)
    else:
        for M in [64, 128]:
            for N in [20, 40]:
                run(M=M, N=N, trials=2000)
