# Example makefile to help you compile your ADASS proceedings
# but you really should read the ManuscriptInstructions.pdf or
# at least the README file. For some smart cookies the Makefile
# could be sufficient too.
#
# Version 14-dec-2018   Peter Teuben
#
# See also:  http://www.adass.org/instructions/ADASS2018.tar
#            http://adass2018.umd.edu/ADASS2018.tar
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

# override P,V,A,E,FIGS with a "makedefs" file, this is where authors should edit, not Makefile
-include makedefs

#  variables for proceeding editors (don't modify, for export, not for authors)
YEAR   = 2018
TMPDIR = ADASS$(YEAR)_author_template
FILES  = AdassChecks.py AdassConfig.py AdassIndex.py ADASS_template.tex \
	 Aindex.py FixUnprintable.py \
	 asp2014.bst asp2014.sty copyrightform.pdf example.bib example.eps \
	 Index.py manual2010.pdf ManuscriptInstructions.pdf PaperCheck.py \
	 README subjectKeywords.txt TexScanner.py \
	 ascl.py asclKeywords.txt \
	 adass2018.bib Makefile makedefs

#  probably don't change these either (or notify the editors you have a special paper case)
TAR_FILE  = $(P)_v$(V).tar.gz
ZIP_FILE  = $(P)_v$(V).zip
FILES4AR  = $(P).tex $(P).bib $(FIGS) makedefs $(P).pdf # $(P)-copyrightform.pdf

# ensure current directory is in the PATH
export PATH := .:$(PATH)

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

# these targets are for most common unix systems, but YMMV. Modify if you need
# let the editors know you have a better way for the next ADASS team
# ASP prefers the latex;latex;dvipdfm route

DVIPDF = dvipdf

pdf:	$(P).pdf

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

dvi:
	latex $(P)

aindex:
	Aindex.py $(P)

DETEX = detex
words:
	$(DETEX) $(P).tex | grep -o -E '\w+' | tr '[A-Z]' '[a-z]' | sort | uniq -c | sort -n

tar:
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

TERMS = 
index:
	@echo Using TERMS=$(TERMS)
	(cd ../Author_Template; Index.py ../../ADASSProceedings2018/papers/$(P)/$(P).tex $(TERMS))

ascl:
	(cd ../Author_Template; ascl.py ../../ADASSProceedings2018/papers/$(P)/$(P).tex)

pdf2:   pdf asp1
	xdg-open $(P).pdf
	xdg-open ../../authors/$(P).pdf

rsync: $(P).bib
	rsync -av $(P)_inc.tex $(P).bib $(FIGS) ../../authors
