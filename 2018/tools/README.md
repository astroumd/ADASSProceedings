
# ADASS 2018

Head over to https://www.certain.com , login (if cookies keep an old stale login, logout and login again)
with adass18registration@umd.edu and you should know the password.

Download the 3 Excel files, but the one labeled SECOND needs ot be done second, since it has the same name.
You will then have 3 files: (watch the spaces)

    1. ADASS 2018  Submitted Abstracts.xls
    2. ADASS 2018  Submitted Abstracts(1).xls
    3. ADASS 2018  Total Registrant Re.xls

in debug mode it will report the sheet sizes:

   106 x 29 in ADASS 2018  Submitted Abstracts.xls
   9 x 29 in ADASS 2018  Submitted Abstracts(1).xls
   118 x 35 in ADASS 2018  Total Registrant Re.xls

The two abstract ones have the same structure (29 columns). The full list is the summary. The code will
key on the  "LastName, FirstName" string.


## Bad Design of Contributions

Contribution should have been:
       1a. Oral
       1b. Poster
       1c. Focus Demo [$200]
       2.  BoF
       3.  Demo Booth [$200]

Where 1 selects one of a/b/c [radio button]
Where 1,2,3 can be zero, one, two or three selected 
 
  Tutorial (independant, not via a form)

## Emails

Example to send mass mail:

       ./mailer.py email2.txt test1 email2.tab EMAIL

in this case the email2.tab just has one column. If you have more columns, you can do

       ./mailer.py email3.txt test123 email3.tab EMAIL,NAME,TITLE

Real example:

      ./mailer.py email2.txt "ADASS deadlines today" adass-1.txt EMAIL


## Names

We designate 

       Bn   = BoF (Birds of a Feather) (8?)      B1...
       Dn   = demo booth (11)                    D1...
       Fn   = focus demo (5)                     F1...
       Is.c = invited talk (13)                  Is.c (by session number s=1..13)
       Os.c = oral contribtution (36?)           Os.c (s=session c=contribution)
       Ps.c = poster (???)                       Ps.c (s=session c=contribution)
       Tn   = tutorial (4)                       T1...4

## Layout of contributions

## Adding abstracts after the fact

Fact of life.... a pain. I kept a reg->reg_dropbox or reg->reg_final.
If the official version in reg_dropbox was updated with an abstract, copy the row in
registration (x3 in python) and the abstract (x1 in python) to their respective sheets
in reg_final, which is the frozen version.

In the end we used reg_dropbox for the list of people, and reg_final for the abstracts, just
to have more control. That one you can also use for editing.

## Using this software

1) make a symlink of 'reg' to the directory where the XLS files are (i use dropbox). Also "make reg" in Makefile

2) make a symlink (or git clone) from 'www' to where you keep the website. Also "make www" in Makefile

3) now look at the makefile how the various targets produce various tables

### Example

This workflow worked on chara and algol:


	git clone https://github.com/astroumd/adass
	cd adass/tools
	git clone https://github.com/astroumd/adass2018.git www
	ln -s ~teuben/public_html/adass/reg_final reg
	mkdir papers

	astroload -v miniconda3 python
	make
	make index

and no UTF-8 errors.



