#!/usr/bin/env python3

#                 S u b j e c t  E n t r i e s  2  I n d e x . p y
#
#  A convenience script to help with processing the submissions for an ADASS
#  ADASS conference. This takes a file containing subject index entries in the
#  form in which they are entered in the .tex file by editors, eg:
#
#  \ssindex{topic!sub-topic!sub-topic}
#
#  and turns them into a text file that contains the entries in the easier to
#  read form
#
#  topic
#     sub-topic
#        sub-topic
#
#  which is also the form used as input by the ADASS script Index.py.
#
#  The script is able to pick up a few possible problems with the index
#  entries, such as entries with a missing '\' in front of 'ssindex' or a
#  missing terminating '}' and will log these to the terminal.
#
#  The input file entries can be any of the following forms:
#
#  \ssindex{topic!sub-topic!sub-topic}
#  %\ssindex{topic!sub-topic!sub-topic} or just
#  topic!sub-topic!sub-topic
#
#  or any of these preceded by a filename and a colon, eg:
#
#  directory/sub-directory/filename.tex:%\ssindex{topic!sub-topic!sub-topic}
#
#  The idea is that it is possible to generate the input file for this
#  program quite simply using grep -h *.tex or some similar command, in order
#  to collect all the subject index entries that have been inserted into a set
#  of .tex files by the editors. This program can be used as a first step
#  towards concatenating such a set of entries, or checking by eye for
#  'almost-duplicate' entries, such as cases where an almost identical term has
#  been used or where a term has been misspelled.
#
#  Note that the example above used "grep -h" to suppress the listing of the
#  file name by grep. If "grep -H" was used, and the lines all begin with a
#  file name followed by a colon, this script will attempt to spot that, in
#  which case the file name can be included in any diagnostics. The script
#  assumes that the files will all be .tex files, and looks for the string
#  ".tex:".
#
#  Usage:
#     SubjectEntries2Index InputFile OutputFile
#
#  Author(s): Keith Shortridge (keith@knaveandvarlet.com.au)
#
#  History:
#     15th Jan 2017. Original version.
#     18th Aug 2017. Converted to run under Python3, using 2to3. Added
#                    the importing of items from __future__ to allow this to
#                    run under either Python2 or Python3. Code now rejects
#                    lines that seem to come from files where the \ssindex
#                    entry wasn't at the start of the line (this happens with
#                    .tex files produced using latexdiff, or if someone puts
#                    an ssindex entry into the middle of a line. KS.
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
if (NumberArgs < 3) :
   print("")
   print("Usage: SubjectEntries2Index InputFile OutputFile")
   print("where InputFile has entries in the topic!sub-topic!sub-topic form")
   print("and OutputFile will be created with them in an ordered hierarchy.")
   print("")
else :

   #  Get the file names from the command line
   
   InputFileName = sys.argv[1]
   OutputFileName = sys.argv[2]

   #  The idea is to read the lines from the input file into the IndexEntries
   #  list, which has them stripped to the basic "topic!sub-topic!sub-topic"
   #  form. We can them sort them and output them, reformatted as needed.
   #  Along the way, we strip off filenames, leading "\\ssindex{" and
   #  trailing '}' strings, and try to flag any possible problems.
   
   IndexEntries = []
   InputFile = open(InputFileName,"r")
   for Line in InputFile :
   
      #  See if there's a leading filename
      
      Filename = ""
      Line = Line.rstrip(" \r\n")
      Index = Line.find(".tex:")
      if (Index > 0) :
         Filename = Line[:Index+4]
         Line = Line[Index+5:]
      
      #  Look for \\ssindex and it's related braces. As far as possible
      #  patch up any problems we find. We expect all the \ssindex entries
      #  to be on their own single lines - it isn't wrong if they're not,
      #  but it can complicate things and we flag this.
      
      Line = Line.strip()
      if (Line.startswith("%")) : Line = Line[1:]
      if (Line.startswith("ssindex")) :
         print("")
         print("Entry is missing the leading '\\'")
         print(Line)
         if (Filename != "") : print("File:",Filename)
         Line = '\\' + Line
      if (Line.startswith("\\ssindex")) :
         Index = Line.find('{')
         if (Index < 0) :
            print("")
            print("Entry has no '{' following \\ssindex")
            print(Line)
            if (Filename != "") : print("File:",Filename)
         else :
            Line = Line[Index + 1:]
            if (Line.endswith('}')) :
               Line = Line[:-1]
            else :
               Index = Line.find('}')
               if (Index < 0) :
                  print("")
                  print("Entry has no terminating '}'")
                  print(Line)
                  if (Filename != "") : print("File:",Filename)
               else :
                  print("")
                  print("Entry has characters following '}'")
                  print(Line)
                  Line = Line[:Index]
                  if (Filename != "") : print("File:",Filename)
   
         #  Finally, add the entry to the list we've built up.
      
         Line = Line.strip()
         if (Line != "") : IndexEntries.append(Line)
      
      else :
      
         #  This catches lines that don't seem to start with ssindex or
         #  something understandably close. Someone may just have put an
         #  ssindex entry in the middle of a line, but that needs to be
         #  pointed out - it could cause problems.
         
         print("")
         print("Entry doesn't start with ssindex")
         print(Line)
         if (Filename != "") : print("File:",Filename)
      
      
      #  Writing the output file is handled by WriteSubjectIndex()
      
      OutputFile = open(OutputFileName,"w")
      AdassIndex.WriteSubjectIndex(IndexEntries,OutputFile)
      OutputFile.close()

   InputFile.close()

