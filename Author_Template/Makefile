# Example makefile to help you compile your ADASS proceedings
# but you really should read the ManuscriptInstructions.pdf or
# at least the README file. For some smart cookies the Makefile
# could be sufficient too.
#
# Version 27-sep-2019   Peter Teuben
#
# See also:  http://www.adass.org/instructions/ADASS2019.tar
#            https://www.adass2019.nl/proc/ADASS2019.tar
#
# P = paper_id    your proceedings paper ID code (the one with the dash, not dot)
# V = version     your version # (1,2,..) since you can only upload unique files
# A = 1stauthor   your last name, e.g. Teuben
# E = email       your contact email for submission issues
# FIGS = *eps     your EPS figures

                    # put your paper_id here (with dash, not dot), e.g. P10-2
                    # or find your template on http://www.astro.umd.edu/~teuben/adass/papers/
P = ADASS_template
                    # keep incrementing this after each upload of your $(P)
V = 1
                    # First author (for Papercheck.py)
A = Teuben
                    # contact person email
E = teuben@gmail.com
		    # your EPS figures (can be blank, and must be base-named with $(P)_*.eps
FIGS = example.eps

# override P,V,A,E,FIGS with a "makedefs" file, this is where authors should edit, not this Makefile
-include makedefs

#  variables for proceeding editors (don't modify, for export, not for authors)
YEAR   = 2019
TMPDIR = ADASS$(YEAR)_author_template
FILES  = AdassChecks.py AdassConfig.py AdassIndex.py ADASS_template.tex \
	 Aindex.py FixUnprintable.py \
	 asp2014.bst asp2014.sty copyrightform.pdf example.bib example.eps \
	 Index.py manual2010.pdf ManuscriptInstructions.pdf PaperCheck.py \
	 README subjectKeywords.txt TexScanner.py \
	 ascl.py asclKeywords.txt \
	 adass2019.bib Makefile makedefs

#  probably don't change these either (or notify the editors you have a special paper case)
TAR_FILE  = $(P)_v$(V).tar.gz
ZIP_FILE  = $(P)_v$(V).zip
FILES4AR  = $(P).tex $(P).bib $(FIGS) makedefs $(P).pdf copyrightform_$(P)_$(A).pdf

# ensure current directory is in the PATH
export PATH := .:$(PATH)

help:
	@echo AUTHOR targets:
	@echo ---------------
	@echo all:   pdf check tar
	@echo pdf:
	@echo check:
	@echo clean:
	@echo tar:
	@echo zip:
	@echo 
	@echo EDITOR targets:
	@echo ---------------
	@echo fix:
	@echo inc:
	@echo spell:
	@echo aindex:
	@echo words:
	@echo asp1:
	@echo index:   needs TERMS=
	@echo ascl:
	@echo ascl1:
	@echo ascl2:   needs CODE=
	@echo pdf2:
	@echo rsync:


all:	pdf check tar


# not for authors, for creator of the ADASS instruction tar file
export:
	rm -rf $(TMPDIR)
	mkdir $(TMPDIR)
	cp -a $(FILES) $(TMPDIR)
	echo Created on `date` by `whoami`  > $(TMPDIR)/VERSION
	-git remote -v                     >> $(TMPDIR)/VERSION
	-git branch                        >> $(TMPDIR)/VERSION
	tar cf ADASS$(YEAR).tar $(TMPDIR)

# copyright is now part of the tar/zip file
copyrightform_$(P)_$(A).pdf: copyrightform.pdf
	cp copyrightform.pdf copyrightform_$(P)_$(A).pdf
	@echo Now go edit your copyrightform_$(P)_$(A).pdf form

# these targets are for most common unix systems, but YMMV. Modify if you need
# let the editors know you have a better way for the next ADASS team
# ASP prefers the latex;latex;dvipdfm route

DVIPDF = dvipdf

pdf:	$(P).pdf
	@echo xdg-open $(P).pdf 

$(P).pdf:  $(P).dvi $(FIGS)
	$(DVIPDF) $(P)

$(P).bib:                                  # bootstrap if you don't have one
	touch $(P).bib

$(P).dvi:  $(P).tex $(P).bib
	latex $(P)
	if [ -s $(P).bib ]; then bibtex $(P); fi
	latex $(P)
	latex $(P)

# an alternative method (ASP does not recommend it)
pdflatex:
	pdflatex $(P)
	if [ -s $(P).bib ]; then bibtex $(P); fi
	pdflatex $(P)
	pdflatex $(P)

clean:
	rm -f $(P).dvi $(P).bbl $(P).pdf $(P).aux $(P).log $(P).out $(P)_inc.tex

check:
	PaperCheck.py $(P) $(A)

ENCODING =
fix:
	FixUnprintable.py  $(P).tex $(ENCODING)

inc:
	tex2inc.py $(P).tex > $(P)_inc.tex
	@tail -1 $(P)_inc.tex
	@cat $(P).toc

spell:
	aspell --mode=tex check $(P).tex
	@echo Share your ~/.aspell.en.pws  ~/.aspell.en.prepl

aspell:
	(cd ../..; $(MAKE) aspell)

dvi:
	latex $(P)

aindex:
	Aindex.py $(P)

DETEX = detex
words:
	$(DETEX) $(P).tex | grep -o -E '\w+' | tr '[A-Z]' '[a-z]' | sort | uniq -c | sort -n

tar:    $(FILES4AR)
	tar zcf $(TAR_FILE) $(FILES4AR)
	@echo Submit to ftp://ftp.astro.umd.edu/incoming/adass
	@echo e.g.   ncftpput ftp.astro.umd.edu  incoming/adass $(TAR_FILE)

zip:
	rm -f $(ZIP_FILE)
	zip $(ZIP_FILE) $(FILES4AR)
	@echo Submit to ftp://ftp.astro.umd.edu/incoming/adass
	@echo e.g.   ncftpput ftp.astro.umd.edu  incoming/adass $(ZIP_FILE)

# for editors
asp1:
	(cd ../..; $(MAKE) asp1 PID=$(P); grep box asp1.log)
	@echo xdg-open ../../authors/$(P).pdf

TERMS = foobar
index:
	@echo Using TERMS=$(TERMS)
	(cd ../Author_Template; Index.py $(TERMS))

index2:
	(cd ../adass_subject_recommender ; detex ../$(P)/$(P).tex |  PYTHONPATH=`pwd` bin/find_subjects.py -m 10 -j)

ascl:
	(cd ../Author_Template; ascl.py ../../ADASSProceedings2019/papers/$(P)/$(P).tex)

ascl1:
	(cd ../Author_Template; ascl.py ../../ADASSProceedings2019/papers/$(P)/$(P).tex | grep ooindex | sort | uniq -c)
	-detex $(P).tex > $(P).txt
	-(cd ../Author_Template; ascl.py ../../ADASSProceedings2019/papers/$(P)/$(P).txt | grep ooindex | sort | uniq -c)
	-grep ooindex $(P).tex

CODE = foobar
ascl2:
        xdg-open https://ascl.net/$(CODE)

pdf2:   pdf asp1
	xdg-open $(P).pdf
	xdg-open ../../authors/$(P).pdf

rsync: $(P).bib
	rsync -av $(P)_inc.tex $(P).bib $(FIGS) ../../authors
	rm -f ../../authors/$(P)_inc.{bbl,blg}

