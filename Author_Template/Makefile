# Example makefile to help you compile your ADASS proceedings
# but you really should read the ManuscriptInstructions.pdf or
# at least the README file.
# Authors should not need to modify the Makefile, please use the makedefs file, included here
#
# Version 7-oct-2023   Peter Teuben & Tyler Linder/Bob Seaman
#
# See also:   https://www.adass2022.ca/.... / ADASS2022.tar    @todo    for 2023
#
# P = paper_id    your proceedings paper ID code (the one with the XNN syntax, e.g., O12)
# V = version     your version # (1,2,..) since you can only upload unique files
# A = 1stauthor   your last name, e.g. Teuben
# E = email       your contact email for submission issues
# FIGS = *eps     your EPS figures

                    # put your paper_id here (with dash, not dot), e.g. P10-2
                    # or find your template on http://www.astro.umd.edu/~teuben/adass/papers/
P = $(shell ./detect_tex.py | grep -v '^%' | sed 's/.tex//g')
                    # keep incrementing this after each upload of your $(P)
V = 1
                    # First author (for Papercheck.py)
A = Teuben
                    # contact person email
E = teuben@gmail.com
		    # your EPS figures (can be blank, and must be base-named with $(P)_*.eps
FIGS = $(shell ls *.eps)

# override P,V,A,E,FIGS with a "makedefs" file, this is where authors should edit, not this Makefile!!!
-include makedefs

# Which command do you use to view the PDF? This is just for convenience.  (mac uses "open", linux "xdg-open")
# PDFOPEN = xdg-open
PDFOPEN = open

#  variables for proceeding editors (don't modify, for export, not for authors)
YEAR   = 2023
ATDIR  = ADASS$(YEAR)_author_template
FILES  = AdassChecks.py AdassConfig.py AdassIndex.py ADASS_template.tex ADASS_template.pdf \
	 Aindex.py FixUnprintable.py \
	 copyrightform.pdf example.bib example.eps \
	 Index.py manual2010.pdf ManuscriptInstructions.pdf PaperCheck.py \
	 README subjectKeywords.txt TexScanner.py \
	 ascl.py asclKeywords.txt detect_tex.py \
	 adass$(YEAR).bib Makefile makedefs \
	 $(FILESASP)

#  @todo new PID_URL ?
#  probably don't change these either (or notify the editors you have a special paper case)
PID_URL   = "https://www.canfar.net/storage/vault/list/adass2022/upload/$(P)"
TAR_FILE  = $(P).tar.gz
ZIP_FILE  = $(P).zip
POS_FILE  = $(P).pdf
FILESPDF  = $(P).pdf copyrightForm_$(P)_$(A).pdf
FILESTEX  = $(P).tex $(P).bib $(FIGS) makedefs
FILESASP  = asp2014.bst asp2014.sty
FILES4AR  = $(FILESTEX) $(FILESPDF)

# ensure current directory is in the PATH
export PATH := .:$(PATH)

help:
	@echo AUTHOR targets:
	@echo ---------------
	@echo all:   pdf check tar
	@echo pdf:
	@echo check:
	@echo clean:
	@echo overleaf:
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


# not for authors, for creator of the ADASS instruction tar/zip file

aADASS_template.pdf:
	$(MAKE) P=ADASS_template

export: ADASS_template.pdf
	rm -rf $(ATDIR)
	mkdir  $(ATDIR)
	cp -a $(FILES) $(ATDIR)
	echo Created on `date` by `whoami`  > $(ATDIR)/VERSION
	-git remote -v                     >> $(ATDIR)/VERSION
	-git branch                        >> $(ATDIR)/VERSION
	-git rev-list --count HEAD         >> $(ATDIR)/VERSION
	rm -f ADASS$(YEAR).tar ADASS$(YEAR).zip
	tar cf ADASS$(YEAR).tar $(ATDIR)
	zip -urq ADASS$(YEAR).zip $(ATDIR)

# copyright is now part of the tar/zip file, checksum (sum) is 13785
copyrightForm_$(P)_$(A).pdf: copyrightform.pdf
	cp copyrightform.pdf copyrightForm_$(P)_$(A).pdf
	@echo Now go edit your copyrightForm_$(P)_$(A).pdf form

# these targets are for most common unix systems, but YMMV. Modify if you need
# let the editors know you have a better way for the next ADASS team
# ASP prefers the latex;latex;dvipdfm route

DVIPDF = dvipdf

pdf:	$(P).pdf
	@echo $(PDFOPEN) $(P).pdf 

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
	rm -f $(P).dvi $(P).bbl $(P).blg $(P).pdf $(P).aux $(P).log $(P).out $(P).toc $(P)_inc.tex

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
	aspell --mode=tex --lang=en check $(P).tex
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

#  could add a checksum on personal copyrightform - if it's 13785,it's bad.
tar:    $(FILES4AR) _checksum
	tar zcf $(TAR_FILE) $(FILES4AR)
	@echo "Login and upload $(TAR_FILE) at $(PID_URL)"

zip:    $(FILES4AR) _checksum
	rm -f $(ZIP_FILE)
	zip $(ZIP_FILE) $(FILES4AR)
	@echo "Login and upload $(ZIP_FILE) at $(PID_URL)"

poster: $(POS_FILE)
	@echo "Login and upload $(POS_FILE) at $(PID_URL)"

overleaf:    $(FILESTEX)
	rm -f $(ZIP_FILE)
	zip $(ZIP_FILE) $(FILESTEX) $(FILESASP)
	@echo You can now upload $(ZIP_FILE) as a new project into overleaf
	@echo After import, git clone this here, and move all the git tree files here.
	@echo "The git clone command is under overleaf's Menu"


_checksum: copyrightForm_$(P)_$(A).pdf
	@echo Checksum test
	@sum copyrightForm_$(P)_$(A).pdf

# for editors
asp1:
	(cd ../..; $(MAKE) asp1 PID=$(P); grep box asp1.log)
	@echo $(PDFOPEN) ../../authors/$(P).pdf

TERMS = foobar
index:
	@echo Using TERMS=$(TERMS)
	(cd ../Author_Template; Index.py $(TERMS))

ssindex:
	@echo Generating ssindex list
	(cd ../Author_Template; ssindex-org.py ../../ADASSProceedings2020/papers/$(P)/$(P).tex)

ssindex2:
	@echo Generating scored ssindex list 
	(cd ../Author_Template; ssindex-scored.py ../../ADASSProceedings2020/papers/$(P)/$(P).tex)

index2:
	(cd ../adass_subject_recommender ; detex ../$(P)/$(P).tex |  PYTHONPATH=`pwd` bin/find_subjects.py -m 10 -j)

ascl:
	(cd ../Author_Template; ascl.py ../../ADASSProceedings2020/papers/$(P)/$(P).tex)
# 	(cd ../Author_Template; ascl-new.py ../../ADASSProceedings2020/papers/$(P)/$(P).tex)

ascl1:
	(cd ../Author_Template; ascl.py ../../ADASSProceedings2020/papers/$(P)/$(P).tex | grep ooindex | sort | uniq -c)
	-detex $(P).tex > $(P).txt
	-(cd ../Author_Template; ascl.py ../../ADASSProceedings2020/papers/$(P)/$(P).txt | grep ooindex | sort | uniq -c)
	-grep ooindex $(P).tex

CODE = foobar
.PHONY: ascl2
ascl2:
	$(PDFOPEN) https://ascl.net/$(CODE)

pdf2:   pdf asp1
	$(PDFOPEN) $(P).pdf
	$(PDFOPEN) ../../authors/$(P).pdf

rsync: $(P).bib
	rsync -av $(P)_inc.tex $(P).bib $(FIGS) ../../authors
	rm -f ../../authors/$(P)_inc.{bbl,blg}

