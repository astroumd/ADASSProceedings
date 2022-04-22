D = Downloads

TGT = adass-0     adass-1     adass-2     adass-3     adass-4      
TXT = adass-0.txt adass-1.txt adass-2.txt adass-3.txt adass-4.txt  

.PHONY: papers

all: students countries dinner tutorial abstract focus comm demo financial companion proceedings date diet count \
	$(TGT)


students:
	@echo Student/General
	@./counter.py 1 |sort | uniq -c

countries:
	@echo Countries
	@./counter.py 12 |sort | uniq -c | sort -nr

dinner:
	@echo Dinner max 150
	@./counter.py 23 |sort | uniq -c | sort -nr

tutorial:
	@echo Tutorial max 220
	@./counter.py 22 |sort | uniq -c | sort -nr

abstract:
	@echo Abstract - max 237
	@./counter.py 28 |sort | uniq -c | sort -nr

abstract2:
	@echo Abstract2
	@./counter.py 29 demo financial companion

focus:
	@echo Focus DemoTalk - max 7
	@./counter.py 25 |sort | uniq -c

comm:
	@echo Commercial DemoTable
	@./counter.py 26 |sort | uniq -c | sort -nr

demo:
	@echo Astro DemoTable
	@./counter.py 27 |sort | uniq -c | sort -nr

financial:
	@echo Financial
	@./counter.py 18 |sort | uniq -c | sort -nr

companion:
	@echo Companion
	@./counter.py 19 |sort | uniq -c | sort -nr

proceedings:
	@echo Proceedings
	@./counter.py 20 |sort | uniq -c | sort -nr

date:
	@echo RegDate
	@./counter.py 0 | ./date.awk  | grep -v / | sort | uniq -c | sort -n -k 2


yapp1=registration.ps/vps
yapp2=registration.gif/gif

date1:
	@echo RegDate
	@./counter.py 0  |  ./date.awk   | grep -v / | awk '{print $1}' | sort -n > registration.dat
	tabhist registration.dat 1 120 360 bins='360-120' gauss=f residual=f cumul=t maxcount=400 xlab="days in 2018" ylab="ADASS registrations" headline="`date`" yapp=$(yapp1)


diet:
	@echo Diet
	@./counter.py 16 |sort | uniq -c | sort -nr


adass-0:
	./counter.py -1 > adass-0.txt

adass-1:
	./emails2018.py > adass-1.txt

adass-2:
	./adass2018.py > adass-2.txt

adass-3:
	./abstracts.py > adass-3.txt

adass-4:
	./demos.py > adass-4.txt

count:
	@echo Counted `cat adass-0.txt | wc -l` participants

#       our dropbox keeps a pretty recent update to the 3 registration sheets
#       or grab the 3 files from our LOC google drive folder "registration" and
#       symlink with 'reg' since that's a hardcoded name here 
reg:
	rm reg; ln -sf ~/Dropbox/adass2018

# commit
gitci:
	git ci $(TXT)

# undo (shit happens)
gitco:
	git co $(TXT)

# get new/old names
diff:
	git diff adass-0.txt

www:
	git clone https://github.com/astroumd/adass2018.git www

# index2 should be last, so the prev/next in the html files are thematical
# Not we don't have the B and the T in here, only I,O,P and F.
index:	 index1  index2 index3 index4


# alphabetical
index1: papers
	cat orals.tab posters.tab  | grep -v ^\# | grep -v TBD |grep -v TDA | sort > all.tab
	LANG=en_US.UTF-8 ./abstracts.py all.tab 0 | grep -i HREF   > junk1.html
	cat header1.txt junk1.html footer1.txt |sed 's/Abstracts/Abstracts Sorted Alphabetically by First Author/'> www/abstracts/index1.html
	/bin/rm -rf junk1.html
	pdflatex abstracts.tex
	cp abstracts.pdf abstracts.tex www/abstracts

#   author templates 
papers:
	./paper_writer.py all.tab template.tex

#   templates for "toc" inclusion in the final volume, placeholder test
papers_test:
	./paper_writer.py all.tab template.tex comment


# thematical
index2:
	@echo '# ' > all.tab
	for s in 1 2 3 4 5 6 7 8 9 10 11 12 13; do\
		(grep '; I'$$s'\.' orals.tab   >> all.tab;\
		 grep '; O'$$s'\.' orals.tab   >> all.tab;\
		 grep '; P'$$s'\.' posters.tab >> all.tab); done
	grep '; F' orals.tab                   >> all.tab
	LANG=en_US.UTF-8 ./abstracts.py all.tab 1 | grep -i HREF >  junk2.html
	cat header1.txt junk2.html footer1.txt | sed 's/Abstracts/Abstracts Sorted By Theme/'> www/abstracts/index2.html
	/bin/rm -rf junk2.html

# for orals latex for the session chairs
index3:
	cat orals.tab | grep -v ^\# | grep -v TBD |grep -v TDA > all.tab
	LANG=en_US.UTF-8 ./abstracts.py all.tab 0 | grep -i HREF   > junk1.html
	/bin/rm -rf junk1.html
	cp abstracts.tex abstracts_orals.tex
	pdflatex abstracts_orals.tex

# thematical for posters only
index4:
	cat posters.tab | grep -v ^\# | grep -v TBD |grep -v TDA > all.tab
	LANG=en_US.UTF-8 ./abstracts.py all.tab 0 | grep -i HREF   > junk1.html
	/bin/rm -rf junk1.html
	cp abstracts.tex abstracts_posters.tex
	pdflatex abstracts_posters.tex

# for peter only
sync:
	rsync -av --delete reg_final chara.astro.umd.edu:public_html/adass
	rsync -av --delete papers chara.astro.umd.edu:public_html/adass

# if this list doesn't agree with the app.certain list of registrants... something is duplicated or missing, i.e. a db error.
list0:
	tr '[A-Z]' '[a-z]' < adass-0.txt | sort | awk '{print NR,$$0}' | less

# tells me what's missing.

PDIR = ~/Dropbox/adass2018/Proceedings
missing:
	@ls $(PDIR)

# program and session sheets
program:
	./makeprogram.py 
	cat sessionsheets.tex | sed 's/Nu/Nu{\\~n}/' > foo
	mv foo sessionsheets.tex
	pdflatex sessionsheets.tex


# make an attendee list for the frontmatter, this will need a lot of utf-8 to latex editing
att:
	./attendee.py > ./participants.att


regupd:
	(cd ~/$(D); mv ADASS\ 2018\ \ * ~/Dropbox/adass2018/)
	cp ~/Dropbox/adass2018/ADASS\ 2018\ \ Total\ Registrant\ Re.xls reg_final/

compare:
	grep -v ^# ../../ADASSProceedings2018/papers/papers.tab | sort > papers1s.tab
	cat orals.tab posters.tab bof.tab tutorial.tab | grep -v ^\# | grep -v TBD |grep -v TDA | sort > papers2s.tab
