#! /usr/bin/env python3
#
#   ADASS 2018 sample processing of the 3 XLS spreadsheets
#   1) you need python3 (or expect UTF-8 issues)
#   2) you need xlrd (should come with python3)

from __future__ import print_function

import xlrd
import sys
import io
import datetime
import numpy as np
from string import Template
from pylatexenc.latexencode import utf8tolatex

# names of the 3 sheets we got from C&VS (notice the 31 character limit of the basename)
_p1 = 'ADASS 2018  Submitted Abstracts.xls'  
_p2 = 'ADASS 2018  2nd Submitted Abstr.xls'
_p3 = 'ADASS 2018  Total Registrant Re.xls'
_p4 = 'IVOA Registration (Responses).xlsx'

_header2 = """\\documentclass{report}\n
              \\usepackage{a4wide}\n
              \\usepackage{graphicx}\n
              \\begin{document}\n
              \\chapter*{ADASS XXVIII Abstract Book}              
              \\includegraphics[width=\\textwidth]{www/images/ADASS2018_Banner.png}
              Brought to you by a Makefile, calling python code that operated on a Excel spreadsheet.
              \\newline\\newline
              \\bigskip\\bigskip
              \\begin{center}
              \\includegraphics[width=0.3\\textwidth]{www/images/logo250.png}
              \\end{center}
              \\bigskip
           """

_footer2 = '\\end{document}\n'



class adass(object):
    def __init__(self, dirname, debug=False):
        """ Given a directory it will read in a set of spreadsheets that define the participants
            This is for ADASS 2018
        """
        import urllib.request, json 
        """
            with urllib.request.urlopen("http://adasstest.strw.leidenuniv.nl/wp-content/plugins/wms-lists/wms-lists/send_json.php") as url:
        """
        with urllib.request.urlopen("http://www.adass2019.nl/wp-content/plugins/wms-lists/wms-lists/send_json.php") as url:
            self.json_oral = json.loads(url.read().decode())

        with urllib.request.urlopen("http://www.adass2019.nl/wp-content/plugins/wms-lists/wms-lists/send_json_booths.php") as url:
            self.json_booth = json.loads(url.read().decode())

        with urllib.request.urlopen("http://www.adass2019.nl/wp-content/plugins/wms-lists/wms-lists/send_json_posters.php") as url:
            self.json_poster = json.loads(url.read().decode())

        self._htmlheader = None
        self._htmlfooter = None

    def create_template(self, oral, fp1, template='template.tex', comment = False, dirname='papers'):

        def read_template(filename):
            # with open(filename, 'r', encoding='utf-8') as template_file:
            with open(filename, 'r') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content)

        T_paper = read_template(template)

        kwargs = {}
        kwargs['FNAME']    = utf8tolatex(oral['firstname'])
        kwargs['FNAMEI']   = utf8tolatex(oral['firstname'][:1])
        kwargs['LNAME']    = utf8tolatex(oral['lastname'])
        if 'Affiliation' in oral:
           kwargs['INAME']    = utf8tolatex(oral['Affiliation'])
        if 'affiliation' in oral:
           kwargs['INAME']    = utf8tolatex(oral['affiliation'])
        kwargs['EMAIL']    = oral['email']
        if 'Title' in oral:
           kwargs['TITLE']    = utf8tolatex(oral['Title'])
        if 'title' in oral:
           kwargs['TITLE']    = utf8tolatex(oral['title'])
        if 'Abstract' in oral:
           kwargs['ABSTRACT'] = utf8tolatex(oral['Abstract'])
        if 'abstract' in oral:
           kwargs['ABSTRACT'] = utf8tolatex(oral['abstract'])
        kwargs['F1']       = '$^1$'
        kwargs['F2']       = '$^2$'
        kwargs['F3']       = '$^3$'
        kwargs['LENA']     = str(len(kwargs['ABSTRACT']))
        kwargs['LENW']     = ""
        kwargs['PCODE']    = oral['pcode'].replace('.','-')
        pcode     = oral['pcode'].replace('.','-')
        if comment:
            kwargs['COMMENT']    = "%"
            kwargs['NOCOMMENT']  = ""
        else:
            kwargs['COMMENT']    = ""
            kwargs['NOCOMMENT']  = "%"
        t1 = T_paper.substitute(**kwargs)
        fn = dirname + '/' + pcode  + '.tex'          #   no, it should be P1-12.tex, not P1.12.tex
        print("Writing %s" % fn)
        fp = open(fn,'w')
        fp.write(t1)
        fp.close()
        msg = '\\tocinsertentry[r]{%s}{%s.~%s}{authors/%s_inc}\n' % (kwargs['TITLE'],oral['firstname'],oral['lastname'],oral['pcode'])
        fp1.write(msg)

    def test_read(self, dirname='papers'):
        fn1 = dirname + '/' + 'toc.txt'
        fp1 = open(fn1,'w')
        fp1.write("%% created by adass2018.py::report_3c()\n")
        for record in self.json_oral:
               for session in record['Sessions']:
                  for oral in session['Orals']:
                     if oral['type'] != '':
                        self.create_template(oral, fp1)

        for record in self.json_booth:
                self.create_template(record, fp1)

        for record in self.json_poster:
            for poster in record['Posters']:
                self.create_template(poster, fp1)

if __name__ == "__main__":
    
    a = adass('reg')
    
    a.test_read()
