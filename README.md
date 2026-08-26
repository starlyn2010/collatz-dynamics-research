# A Modular Residue Framework for Orbitwise 2-Adic Valuations in Collatz Sequences

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Paper: LaTeX](https://img.shields.io/badge/paper-LaTeX-blue)](Collatz_v8_FINAL.tex)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![CI](https://github.com/starlyn2010/collatz-dynamics-research/actions/workflows/ci.yml/badge.svg)](https://github.com/starlyn2010/collatz-dynamics-research/actions/workflows/ci.yml)

Exact prefix laws for 2-adic valuations along deterministic Collatz orbits, a density-one discrepancy bound, and large-scale validation. **We do not claim to prove the Collatz conjecture.**

---

## Abstract

We study the distribution of 2-adic valuations *Kⱼ = v₂(3·Tₒddʲ(n)+1)* along deterministic Collatz orbits.

**Rigorous results.**
* **Proposition 3.** For each *k≥1*, the event *{Kⱼ=k}* is equivalent to a unique congruence *xⱼ ≡ aₖ (mod 2ᵏ⁺¹)* with *aₖ ≡ 3⁻¹(2ᵏ−1) (mod 2ᵏ⁺¹)* (explicit: *a₁≡3 mod 4*, *a₂≡1 mod 8*, *a₃≡13 mod 16*).
* **Theorem 6 (prefix cylinder law).** Any finite valuation sequence *(k₀,…,kᵣ₋₁)* corresponds to a unique odd residue class modulo *2^{Sᵣ+1}* where *Sᵣ=Σkᵢ*, proved by induction.
* **Corollary 8/9.** Under uniform odd residues, the prefix sum *S_N* is exactly negative-binomial *NB(N,½)* with *P(S_N=s)=C(s−1,N−1)·2^{−s}*, identical for all admissible *c∈{1,5,7,11}*.
* **Theorem 7 (density-one, Hoeffding + Chernoff).** For any *η<½* and *C>0*, the fraction of odd *n<2^M* whose first *⌊ηM⌋* odd steps violate *|p̂ₖ−2⁻ᵏ|≤C·log N/√N* tends to 0 as *M→∞*.
* **Theorem 8 (reduction).** An orbital discrepancy bound *Dₘ(n,N)≤C·log N/√N* for all *m≤21* implies the geometric valuation bound for all *k≤20*.

**The open gap.** Extending the density-one result from the prefix regime *N≤η·log₂ n* to the full orbit is the genuine frontier (Conjecture 14).

**Computational validation.** A *3×4* matrix over bit-lengths *M∈{64,128,256}* and prefix lengths *N∈{20,40,60,80}* (10 000 independent random odd integers per cell) plus an exhaustive sweep over *4,999,944* orbits with *n≤10⁷* shows: mean absolute error uniformly below *0.002*, autocorrelations below *0.009* at all lags 1–10, and decreasing KS statistic with *N* (no degradation). Early termination appears only for *M=64* at *N≥60* (0.12% at N=60, 1.94% at N=80), precisely at the theoretical *S_N≈M* threshold.

---

## Repository Structure

```
collatz-dynamics-research/
├── Collatz_v8_FINAL.tex          # paper source (article, 12pt)
├── *.png                         # 8 generated figures
│   ├── freq_vs_theory.png        # empirical vs 2^-k
│   ├── hist_SN*.png              # S_N histograms (NB)
│   ├── hist_SN_M*.png            # per-cell overlays
│   ├── autocorrelation_ki.png / autocorrelation_decay.png
│   └── error_plot.png / error_vs_N.png
├── src/
│   └── validate_prefix_law.py    # light reproduction (Prop.3 + 2^-k check)
├── tests/
│   └── test_import.py            # smoke: tex/figures/citation + law sanity
├── Makefile                      # paper / clean / test
├── pyproject.toml / requirements.txt
├── CITATION.cff
└── LICENSE (MIT)
```

---

## Installation

No heavy dependencies are required to compile the paper — just a TeX distribution (`pdflatex`, `bibtex`). For the lightweight validation script:

```bash
git clone https://github.com/starlyn2010/collatz-dynamics-research.git
cd collatz-dynamics-research
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"   # numpy, matplotlib, scipy, pytest, ruff
```

---

## Usage

### Build the paper

```bash
make paper
# or manually:
pdflatex Collatz_v8_FINAL.tex
bibtex Collatz_v8_FINAL || true
pdflatex Collatz_v8_FINAL.tex
pdflatex Collatz_v8_FINAL.tex
```

Output: `Collatz_v8_FINAL.pdf`.

### Light validation (seconds)

```bash
python src/validate_prefix_law.py --quick
```

Output (example):

```
M=64 N=20 trials=500 total_steps=10000
  k=1: empirical 0.4998 theory 0.5000 err 0.0002
  k=2: empirical 0.2510 theory 0.2500 err 0.0010
  ...
```

Full 4-cell demo:

```bash
python src/validate_prefix_law.py
```

### Reproduce the full 3×4 matrix (research-scale)

The paper's full validation (12 cells × 10k samples + 5M exhaustive sweep) is compute-heavy and was run on a local workstation with 64-bit odd integers. To reproduce:

```bash
# adapt validate_prefix_law.py to loop over M in {64,128,256} and N in {20,40,60,80}
# each cell: 10k random odd seeds, no external datasets
# exhaustive: iterate odd n in [1, 10^7] and compute K-sequences
```

See `Collatz_v8_FINAL.tex` Sections 6–7 for thresholds, seeding, and overflow handling. Figures in the repository are the frozen outputs of that run.

---

## Results

### Analytical

| Result | Statement | Status |
|--------|-----------|--------|
| Prop. 3 | Residue characterization `{K=k} ⇔ x≡aₖ mod 2^{k+1}` | **Proved** |
| Thm. 6 | Prefix cylinder law (unique residue for any sequence) | **Proved** |
| Cor. 8–9 | Exact NB law for `S_N`, uniform over admissible `c` | **Proved** |
| Thm. 7 | Density-one bound `|p̂ₖ−2⁻ᵏ| ≤ C log N/√N` for `N≤ηM` | **Proved** |
| Thm. 8 | Reduction to orbital discrepancy `D_m` | **Proved** |
| Conj. 14 | Extension to the full orbit | **Open** (stated as gap) |

### Computational (frozen figures)

* **Mean absolute error** in valuation frequencies < **0.002** across all 12 cells.
* **Autocorrelation** at lags 1–10 < **0.009** (no structure).
* **KS statistic** decreases with *N* for fixed *M* — model does not degrade.
* **Overflow** only at the predicted threshold *S_N≈M* (M=64, N≥60).
* **Exhaustive** *n≤10⁷*: no violation of the stated bound; empirical *C₉₅=0.300*.

Figures: `error_vs_N.png`, `freq_vs_theory.png`, `hist_SN.png`, `autocorrelation_*.png`, etc.

> Honesty note: validation is statistical and computational; it supports but does not replace the open conjecture. All limitations are stated in the paper (Section “The open gap”).

---

## Citation

```bibtex
@article{rosario2026modular,
  title  = {A Modular Residue Framework for Orbitwise 2-Adic Valuations
            in Collatz Sequences: Exact Prefix Laws, a Density-One Bound,
            and Large-Scale Validation},
  author = {Rosario, Starlyn},
  year   = {2026},
  url    = {https://github.com/starlyn2010/collatz-dynamics-research},
  note   = {Independent Researcher, Santo Domingo, Dominican Republic}
}
```

Also see `CITATION.cff`.

---

## License

MIT — see [LICENSE](LICENSE).

---

## Acknowledgments

Terras (1976), Everett (1977), Krasikov–Lagarias (2003), Tao (2022), Lagarias (2010), Anashin–Khrennikov (2009), Inselmann (2024) for prior results surveyed in the introduction. 2-adic dynamical perspective builds on standard references acknowledged in the paper.
