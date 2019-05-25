#!/usr/bin/env python

#                 M e r g e  S u b j e c t  I n d e x e s . p y
#
#  A convenience script to help with processing the submissions for an ADASS
#  ADASS conference. This takes as input two files containing subject index
#  entries in the hierarchical form:
#
#  topic
#     sub-topic
#        sub-topic
#
#  (which is also the form used as input by the ADASS script Index.py) and
#  merges them into a single output file.
#
#  This is something that is worth doing at the end of the editing of a new
#  ADASS volume. Usually the editing process starts with such a file containing
#  the subject index entries used for recent volumes, and ends with a second
#  file that contains the entries used for the current volume (possibly
#  produced using the SubjectEntries2Index script). These can then be merged to
#  form the starting point for the next volume. This helps to keep the subject
#  index entries consistent both between papers in the one volume and from
#  volume to volume.
#
#  Usage:
#     MergeSubjectIndexes FirstInputFile SecondInputFile OutputFile
#
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  History:
#     15th Jan 2017. Original version.
#     10th Sep 2017. Converted to run under Python3, using 2to3. Added
#                    the importing of items from __future__ to allow this to
#                    run under either Python2 or Python3. KS.
#     22nd Sep 2017. Minor correction to comments about merging lists. KS.
#
#  Python versions:
#     This code should run under either python 2 or python 3, so long as
#     the python 2 version supports the "from __future__ import" used here.
#     It has been tested under 2.7 and 3.6.
# 

from __future__ import (print_function,division,absolute_import)

import os
import sys
import string

import AdassIndex

# ------------------------------------------------------------------------------

#                            M a i n  P r o g r a m

#  First, just check we have the necessary arguments.

NumberArgs = len(sys.argv)
if (NumberArgs < 4) :
   print("")
   print("Usage: MergeSubjectIndexes FirstInputFile SecondInputFile OutputFile")
   print("where both InputFiles have entries in an ordered hierarchy, and")
   print("OutputFile will be the result of merging them.")
   print("")
else :

   #  Get the file names from the command line. Check that the input files
   #  exist.
   
   OK = True
   FirstInputFile = sys.argv[1]
   if (not os.path.exists(FirstInputFile)) :
      print("Cannot find first input file",FirstInputFile)
      OK = False
   SecondInputFile = sys.argv[2]
   if (not os.path.exists(SecondInputFile)) :
      print("Cannot find second input file",SecondInputFile)
      OK = False

   if (OK) :

      OutputFileName = sys.argv[3]

      #  Read the two input index files, getting their contents in the form
      #  "topic!sub-topic!sub-topic" form.

      InputList = AdassIndex.ReadIndexList(FirstInputFile)
      SecondInputList = AdassIndex.ReadIndexList(SecondInputFile)

      #  Combine the two lists, and let WriteSubjectIndex() handle the rest -
      #  it will remove duplicate entries and output the rest in the required
      #  hierarchical form.

      InputList.extend(SecondInputList)
      OutputFile = open(OutputFileName,"w")
      AdassIndex.WriteSubjectIndex(InputList,OutputFile)
      OutputFile.close()

