#!/usr/bin/env python

#                    T e x  S c a n n e r . p y
#
#  Defines a TexScanner class that can be used to extract LaTeX directives
#  from a .tex file. Call SetFile() to supply a reference to an already
#  open .tex file, then use successive calls to GetNextTexCommand() to get 
#  all the tex directives and their parameters from the file. This probably
#  isn't of very general utility when it comes to parsing .tex files, but
#  it is useful for the ADASS editing purposes for which it was written,
#  where all that was wanted was to find graphics or citation commands and
#  see what files or references they were using.
#
#  Parsing LaTeX files is tricky, and this code isn't perfect by any means.
#  There are lots of constructs that will fool it, usually into missing
#  commands that it ought to spot.
#
#  History:
#     14th Jan 2016. Original version, KS.
#     28th Jan 2016. GetNextWord() now allows for nesting. GetNextTexCommand()
#                    now allows for any number of required and/or optional
#                    arguments. The list it returns can be of any length, not
#                    always one of three items, so calling code will need to
#                    be modified. KS.
#      1st Feb 2016. Interface to GetNextTexCommand() reworked to use a
#                    callback for each new command found. This should make it
#                    easier to introduce a recursive scan that catches commands
#                    included within the arguments to other commands, although
#                    at the moment this is not implemented. KS.
#     11th Feb 2016. GetTexCommand() now does do a recursive scan through the
#                    arguments of the commands it finds. KS.
#     16th Feb 2016. Now catches multiple LaTeX directives in one argument, eg
#                    \citetext{\citealp{l1980}, implemented in \citealp{w12}}
#     30th Mar 2016. Now checks to see if '%' characters are comment characters
#                    or just literal '%' that have been escaped. KS.
#      7th Apr 2016. Fixed obscure parsing bug triggered by the sequence 
#                    "$\mu$m" which caused the scanning of the string containing
#                    it to be terminated prematurely. It's because the code
#                    had assumed that all \directives would be terminated by
#                    a line break, space, or a '{' or '[', which is not of
#                    course the case. Strange it took this long to show up. KS.
#     12th Apr 2016. GetNextChar() now intercepts "\n" characters and treats
#                    them as spaces - this is essentially what LaTeX does. KS.
#      2nd May 2016. Fixed a parsing problem where a slightly unusual sequence
#                    (involving a \newcommand definition on a single line} sent
#                    the parser into infinite recursion. KS.
#                    

import os
import sys
import string

class TexScanner(object):

   def __init__(self):
      self.FileIdSet = False
      self.Escaped = False
      self.LastChar = ""
      self.LastWord = ""
      
   def SetFile(self,FileId) :
   
      #  Needs to be called before any of the Get... routines. This passes
      #  the Id of an open .tex file to the scanner.
      
      self.FileId = FileId
      self.FileIdSet = True
      
   def GetNextChar(self) :
   
      #  Returns the next character from a .tex file. If a comment character
      #  ('%') is encountered, this skips to the end of the current line and
      #  returns the newline character at the end. If the end of the file is
      #  reached, or if the file is not open, this returns an empty string. 
      #  Allow for the case where the comment character was escaped, in which
      #  case treat it as a literal '%'. LaTeX treats an end of line like a 
      #  space, and we intercept "\n" characters and turn them into spaces to
      #  get the same effect.
      
      Char = ""
      if (self.FileIdSet) :
         Char = self.FileId.read(1)
         if (Char == "%") :
            if (not self.Escaped) :
               while (True) :
                  Char = self.FileId.read(1)
                  if (Char == "\n" or Char == "") : break
         self.Escaped = (Char == "\\")
         if (Char == "\n") : Char = " "
      return Char 
          
   def GetNextLine(self) :
   
      #  Returns the next line from a .tex file, with comments stripped out.
      #  This means anything in a line from the first '%' character up to but
      #  not including the final newline character is removed from the line.
      #  It does mean than a line that starts with a '%' is returned as a
      #  blank line - just a newline; it is not ignored completely. If the
      #  end of the file is reached, or the file is not open, this returns
      #  an empty string.
      
      Result = ""
      while (True) :
         Char = self.GetNextChar()
         Result = Result + Char
         if (Char == "\n" or Char == "") : break
      return Result
      
   def GetNextWord(self):
   
      #  Returns the next 'word' from a .tex file. Comments are ignored, and
      #  a 'word' is defined slightly unusually here in order to help with
      #  processing LaTeX directives. Anything enclosed in {} or in []
      #  braces or brackets, including the enclosing {} or [] is considered
      #  a word. Blanks and { and [ characters delimit words, as do the 
      #  ends of lines, which are assumed to be one or more of \n and \r
      #  characters. Ends of lines are removed when encountered within
      #  {} or [] characters.
      
      Word = ""
      
      #  Find the first non-blank character (treating newline characters
      #  and carriage returns as blanks).
      
      while (True) :
         if (self.LastChar != "") :
            Char = self.LastChar
         else :
            Char = self.GetNextChar()
         self.LastChar = ""
         if (Char != " " and Char != "\n" and Char != "\r") : break
      if (Char != "") :
         Word = Word + Char
         
         #  If the word started with a { or [, then we ignore blanks and
         #  keep going until we hit the corresponding closing character
         #  (or the end of the file). Allow for nesting.
         
         if (Char == "{" or Char == "[") :
            Start = Char
            if (Start == "{") : End = "}"
            if (Start == "[") : End = "]"
            Nesting = 1
            while (True) :
               Char = self.GetNextChar()
               if (Char == "") : break
               if (Char != '\n' and Char != '\r') : Word = Word + Char
               if (Char == Start) : Nesting = Nesting + 1
               if (Char == End) : 
                  Nesting = Nesting - 1
                  if (Nesting <= 0) : break
            
         else :

            #  Otherwise, just keep going until we hit a blank or one of
            #  the delimiting braces. Either of these will terminate the word,
            #  but if it was a brace, we need to remember it for the next
            #  time we're called. 

            while (True) :
               Char = self.GetNextChar()
               if (Char == "") : break
               if (Char == " " or Char == '\r' or Char == '\n') : break
               if (Char == "{" or Char == "[") :
                  self.LastChar = Char
                  break
               Word = Word + Char
      return Word
                           
   def GetNextTexCommand(self,Callback,ClientData,ClientExtra) :
   
      #  Searches for the next Tex/LaTeX command read from the open .tex file.
      #  and calls the specified callback routine with the details of the
      #  command. The callback routine is called with a first argument that
      #  gives the command details, followed by the arguments supplied 
      #  as ClientData and ClientExtra. The command details are supplied 
      #  as a list of strings. The first is the LaTeX directive, beginning
      #  with '\'. Subsequent strings are the arguments that followed
      #  the directive, either {required} (in curly braces) or [optional]
      #  (in square brackets). The arguments are returned with the beginning
      #  and ending braces included. If the end of the file is reached, this
      #  routine returns True; otherwise it returns False.
      #
      #  Because the arguments for the LaTeX command may themselves contain
      #  further LaTeX commands, this routine also searches recursively
      #  through each argument, and will call the callback routine for each
      #  command found. To get every LaTeX command in the .tex file, this
      #  routine should continue to be called until it returns True.
      
      Finished = True
      Command = []
      Directive = ""
      while (True) :
         if (self.LastWord == "") :
            Word = self.GetNextWord()
         else :
            Word = self.LastWord
            self.LastWord = ""
         if (Word == "") : break
         # (This doesn't handle the case where there are multiple directives
         # in the one word, eg "\it{text}\emph{text}". It will only find
         # the first.)
         BSlashIndex = Word.find('\\')
         if (BSlashIndex >= 0) :
            Directive = Word[BSlashIndex:]
            break
      if (Directive != "") :
         Command.append(Directive)
         Word = self.GetNextWord()
         while (Word != "") :
            if (Word[0] == '[' or Word[0] == '{') :
               Command.append(Word)
               
               #  Search each argument recursively for any LaTeX commands
               #  it may contain.
               
               Word = Word[1:len(Word) - 1]
               self.GetNextTexCommandFromString(Word,\
                                            Callback,ClientData,ClientExtra)
               Word = self.GetNextWord()
            else :
               self.LastWord = Word
               break
         Callback(Command,ClientData,ClientExtra)
         Finished = False
      return Finished
     
   def GetNextWordFromString(self, String, Posn):
   
      #  Returns the next 'word' from a string, given the string and a start
      #  position in the string. It is assumed that the string contains no
      #  comments. A 'word' is defined slightly unusually here in order to 
      #  help with processing LaTeX directives. Anything enclosed in {} or
      #  in [] braces or brackets, including the enclosing {} or [] is 
      #  considered a word. Blanks and { and [ characters delimit words.
      #  This routine returns a pair comprising the word and the value
      #  for Posn to be used for the next call. When the end of the string
      #  is reached, the pair returned is ("",0). The Posn value starts from
      #  0, in the usual Python way.
      #
      #  This code is similar in structure to GetNextWord(), but it's easier
      #  to move around in a string than it is in a file. Note the assumption
      #  that this will be used mainly on words that have been obtained via
      #  GetNextWord() and so will already have things like comments stripped
      #  out. The intent is that this will be used recursively to split up
      #  words that themselves contain LaTeX commands, eg
      #  \center{\it{text}\cite{ref}}
      #  where GetNextWord will find "\center" and then "{\it{text}\cite{ref}}"
      #  and we need to use this routine to split up that nested second word.
      
      Word = ""
      Char = ""
      
      #  Find the first non-blank character.
      
      Index = Posn
      while (Index < len(String)) :
         Char = String[Index]
         Index = Index + 1
         if (Char != " ") : 
            Word = Word + Char
            break
      
      #  See if we found anything. If not, quit now.
      
      if (Word != "") :
         
         #  If the word started with a { or [, then we ignore blanks and
         #  keep going until we hit the corresponding closing character
         #  (or the end of the string). Allow for nesting.
         
         if (Char == "{" or Char == "[") :
            Start = Char
            if (Start == "{") : End = "}"
            if (Start == "[") : End = "]"
            Nesting = 1
            while (Index < len(String)) :
               Char = String[Index]
               Index = Index + 1
               if (Char == "") : break
               Word = Word + Char
               if (Char == Start) : Nesting = Nesting + 1
               if (Char == End) : 
                  Nesting = Nesting - 1
                  if (Nesting <= 0) : break
            
         else :

            #  Otherwise, just keep going until we hit a blank or one of
            #  the delimiting braces. Either of these will terminate the word,

            while (Index < len(String)) :
               Char = String[Index]
               if (Char == " ") : break
               if (Char == "{" or Char == "[") : break
               Index = Index + 1
               Word = Word + Char

      if (Word == "") : Index = 0
                
      return (Word,Index)

   def GetNextTexCommandFromString(self,\
                             String,Callback,ClientData,ClientExtra) :
      
      #  This is similar to GetNextTexCommand(), except that it works not on
      #  a file but on a string, and it works recursively, calling itself
      #  to search the arguments of any command to see if they themselves
      #  contain more commands. Each time a command is found, the specified
      #  callback routine is called with the command details and the client
      #  arguments, just as for GetNextTexCommand().
      
      Posn = 0
      More = True
      while (More) :
         Directive = ""
         Command = []

         #  Apart from the recursion, this code follows the general lines of
         #  GetNextTexCommand().

         while (True) :
            WordPair = self.GetNextWordFromString(String,Posn)
            Word = WordPair[0]
            Posn = WordPair[1]
            if (Word == "") : break
            if (Word[0] == '[' or Word[0] == '{') :
               self.GetNextTexCommandFromString(Word[1:len(Word) - 1],\
                                               Callback,ClientData,ClientExtra)
            BSlashIndex = Word.find('\\')
            if (BSlashIndex >= 0) :
               Directive = Word[BSlashIndex:]
               break
         More = False
         if (Directive != "") :
            Command.append(Directive)
            WordPair = self.GetNextWordFromString(String,Posn)
            Word = WordPair[0]
            Posn = WordPair[1]
            if (Word != "") :
               if (Word[0] == '[' or Word[0] == '{') :
                  self.GetNextTexCommandFromString(Word[1:len(Word) - 1],\
                                               Callback,ClientData,ClientExtra)
            while (Word != "") :
               if (Word[0] == '[' or Word[0] == '{') :
                  Command.append(Word)
                  WordPair = self.GetNextWordFromString(String,Posn)
                  Word = WordPair[0]
                  Posn = WordPair[1]
                  if (Word != "") :
                     if (Word[0] == '[' or Word[0] == '{') :
                        self.GetNextTexCommandFromString(Word[1:len(Word) - 1],\
                                               Callback,ClientData,ClientExtra)
                     More = False
                     if (String[Posn:].strip(" \\r\\n") != "") : More = True
               else :
                  More = True
                  break
            Callback(Command,ClientData,ClientExtra)
            
