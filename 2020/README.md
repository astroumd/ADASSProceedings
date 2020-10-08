
# ADASS 2010

These are the tools and files we used between website and book production.
Most notably how to get the personalized templates to work.

## Ingestion

The LOC prepared a list of "paper_id","name","affil","title","abstract"
Make sure papers.tab and this table are consistent, no missing papers.

## Names

We designate PID's in the following way 

       Bc   = BoF (Birds of a Feather)           Bc
       Dc   = demo booth                         Dc
       Fd   = focus demo                         Fc
       Hc   = hackathon/ivoa/prize               Hc
       Is-c = invited talk                       Is-c (by session number s=1..13)
       Os-c = oral contribtution                 Os-c (s=session c=contribution)
       Ps-c = poster                             Ps-c (s=session c=contribution)
       Tc   = tutorial                           Tc

where 's' (if present) is the session(theme), and 'c' the contribution.
Some years count them from 1 upward per category, in 2020 they number
them roughly upwards accross the board. Some 'c' values might be missing
if a paper was retracted or so.

## Workflow

1. Make a symlink to papers.tab, e.g.

        ln -s ../../ADASSProceedings2020/papers/papers.tab

2. Make sure the CSV file is here

        ls -l data-1602142408446.csv

3. Run the script, maybe check a paper

        make papers
        cd ADASS2020_author_template
        tar xf ../papers/T1.tar
        make pdf

4. Make the tarfile:

        make tar
        # this wrote personalized-templates.tar.gz




