#
#  for 2020.   Cloned of the ../2018/Makefile
#

.PHONY: papers


#   author templates for 2020
papers:
	mkdir -p papers
	./paper_writer.py papers.tab template.tex PID.tex
	./paper_writer.py papers.tab makedefs     makedefs
	./paper_writer.py papers.tab template.bib PID.bib

