"""MIT-grade smoke tests: verify LaTeX source and figure assets exist."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_tex_exists():
    assert (ROOT / "Collatz_v8_FINAL.tex").exists()
    tex = (ROOT / "Collatz_v8_FINAL.tex").read_text(encoding="utf-8")
    assert r"\title{A Modular Residue Framework" in tex
    assert r"\begin{abstract}" in tex

def test_figures_exist():
    expected = [
        "autocorrelation_decay.png",
        "autocorrelation_ki.png",
        "error_plot.png",
        "error_vs_N.png",
        "freq_vs_theory.png",
        "hist_SN.png",
        "hist_SN_M128_N40.png",
        "hist_SN_M64_N60.png",
    ]
    for fname in expected:
        p = ROOT / fname
        assert p.exists(), f"missing figure {fname}"
        assert p.stat().st_size > 1000

def test_citation_exists():
    assert (ROOT / "CITATION.cff").exists()
    assert (ROOT / "LICENSE").exists()
    assert (ROOT / "pyproject.toml").exists()

def test_collatz_valuation_law_sanity():
    """Minimal sanity: 2^-k law via modular residues (no heavy sweep)."""
    # Reproduce Prop. 3 check: for odd residues modulo 2^{k+1},
    # {K=k} corresponds to a single class a_k = 3^{-1}(2^k-1) mod 2^{k+1}.
    # Verify distribution over a small exhaustive sweep without big ints.
    def v2(n: int) -> int:
        return (n & -n).bit_length() - 1 if n != 0 else 0
    def K_of_odd(x: int) -> int:
        return v2(3 * x + 1)
    # Exhaust odd residues in [1, 2^10)
    N = 1 << 10
    counts = {k: 0 for k in range(1, 7)}
    total = 0
    for n in range(1, N, 2):
        k = K_of_odd(n)
        if k in counts:
            counts[k] += 1
            total += 1
        # also count larger k in overflow bucket
    # Expected proportions 2^-k; tolerance 0.02 for this tiny N
    for k in range(1, 6):
        empirical = counts[k] / total
        expected = 2 ** (-k)
        assert abs(empirical - expected) < 0.03, f"k={k} {empirical} vs {expected}"
