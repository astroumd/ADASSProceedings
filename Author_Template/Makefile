# Example makefile to help you compile your ADASS proceedings
#
# proceeding contribution and version ## (1 before Sep 28, 2 before Oct 17)
p = P2.17        
v = 1

#FIGS = gmc1.eps  s3-ell-0.eps
FIGS = 
SCP = chara:/tmp

POSTERFIGS = 

PPP = 

all:	$(p).pdf tar


$(p).pdf:  $(p).dvi $(FIGS)
	dvipdf $(p)

$(p).dvi:  $(p).tex $(p).bib
	latex $(p)
	bibtex $(p)
	latex $(p)
	latex $(p)
	latex $(p)

$(b).pdf:  $(b).dvi 
	dvipdf $(b)

$(b).dvi:  $(b).tex $(b).bib
	latex $(b)
	bibtex $(b)
	latex $(b)
	latex $(b)
	latex $(b)

pdf:
	pdflatex $(p)
	bibtex $(p)
	pdflatex $(p)
	pdflatex $(p)

test:
	pdflatex $(p)

clean:
	rm -f $(p).dvi $(p).bbl


tar:
	tar zcf $(p)_v$(v).tar.gz $(p).tex $(p).bib $(FIGS)
	@echo ftp://ftp.astro.umd.edu/incoming/adass
	# scp $(p)_v$(v).tar.gz  $(SCP)

