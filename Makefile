PACKAGE_ROOT := $(shell git rev-parse --show-toplevel)/reports/template

export OPENTYPEFONTS := ${PACKAGE_ROOT}:
export TEXINPUTS := ${PACKAGE_ROOT}:

.DEFAULT_GOAL : help

help :
	@echo Use make FILENAME.pdf to make the pdf version of FILENAME.tex

%.pdf : %.tex
	latexmk --xelatex $<

clean : clean-temp clean-pdf

clean-temp : $(wildcard *.aux *.fdb_latexmk *.fls *.listing *.log *.xdv)
	if [ ! -z "$^" ]; then rm $^; fi

clean-pdf : $(wildcard *.tex)
	if [ ! -z "$^" ]; then for file in $^; do if [[ -f "$${file%.*}.pdf" ]]; then rm $${file%.*}.pdf; fi; done; fi

