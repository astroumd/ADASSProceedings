
#  ADASS 2021

Some notes to get a head start for ADASS 2021

## Personalized Templates

If we get a CSV of all accepted contributions, the following fields are useful:  (see the report_3c function)
(the name of the field doesn't matter, I've just made them descriptive here)

      PaperID    (P3-14)
      FirstName
      LastName
      Affiliation
      email
      PaperTitle
      PaperAbstract
      ORCID   (optional)
      ... (TBD)


The code can also deal with XLS files (as we did in 2018), but CSV is a lot easier to deal with.
As for code, just copy the previous year adassNNNN.py and adapt it. paper_writer.py might need
a small patch as well if your API changes.

When this all works, all one should need is:

      make papers

which creates personalized-templates.tar.gz from the just filled papers/ tree. The individual
PID.tar files can be made available to authors, in addition to the big ADASS2021.tar
