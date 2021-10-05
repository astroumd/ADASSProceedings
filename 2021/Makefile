#
#  for 2020.   Cloned of the ../2018/Makefile
#

.PHONY: papers tar write_paperstab


#   author templates for 2021
write_paperstab:
	./tab_producer.py
papers:
	mkdir -p papers
	./paper_writer.py papers.tab template.tex PID.tex
	./paper_writer.py papers.tab makedefs     makedefs
	./paper_writer.py papers.tab template.bib PID.bib

tar:
	tar zcf personalized-templates.tar.gz papers/*.tar

clean:
	rm -rf papers

