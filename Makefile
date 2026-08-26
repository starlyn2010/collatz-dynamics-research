.PHONY: paper clean test lint

paper:
	pdflatex Collatz_v8_FINAL.tex
	bibtex Collatz_v8_FINAL || true
	pdflatex Collatz_v8_FINAL.tex
	pdflatex Collatz_v8_FINAL.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
	rm -rf __pycache__ .pytest_cache .ruff_cache

test:
	pytest -q

lint:
	ruff check . || true

figures:
	@echo "Figures are pre-generated (7 PNGs). To regenerate, run validation scripts (see README)."
	@ls -lh *.png
