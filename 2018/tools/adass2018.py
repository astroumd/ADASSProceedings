#! /usr/bin/env python
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
        # filenames
        self.p1 = dirname + '/' + _p1
        self.p2 = dirname + '/' + _p2
        self.p3 = dirname + '/' + _p3
        self.p4 = dirname + '/' + _p4        
        # sheets
        (self.x1,self.r1) = self.xopen(self.p1, debug)
        (self.x2,self.r2) = self.xopen(self.p2, debug)
        (self.x3,self.r3) = self.xopen(self.p3, debug)
        (self.x4,self.r4) = self.yopen(self.p4, debug)
        # prepare some lists
        self.lnames1=[]
        self.keys1  =[]
        self.titles = dict()
        self.abstracts = dict()
        for key in self.x1.keys():                       # loop over all "Lname, Fname"
            ln = key[:key.find(',')]
            self.lnames1.append(ln)     # make a list of all "Lname"
            #print("keya = %s"%key)
            self.titles[key] = self.x1[key][23].value # makeprogram needs hash of last name and title
            self.abstracts[key] = self.x1[key][24] # makeprogram needs hash of last name and abstract
            self.keys1.append(key)                       # and list of "Lname, Fname"
        
        self._htmlheader = None
        self._htmlfooter = None


    def getheader(self):
        if self._htmlheader == None:
           with open("header1.txt","r") as h:
                self._htmlheader = h.read()
        return self._htmlheader 

    def getfooter(self):
        if self._htmlfooter == None:
           with open("footer1.txt","r") as h:
                self._htmlfooter = h.read()
        return self._htmlfooter

    def latex(self, text):
        """ attempt to turn text into latex
        """
        text = text.replace('_','\_')
        text = text.replace('&','\&')
        text = text.replace('#','\#')
        text = text.replace('^','\^')
        text = text.replace('%','\%')            
        return text

    def xopen(self, path, debug=False, status = True):
        """
        path     file
        debug    print more
        status   if true, only accept 'New' in "Reg Status"
        """

        book = xlrd.open_workbook(path)
        ns = book.nsheets
        s0 = book.sheet_by_index(0)
        if ns != 1:
            print("Warning: %s has %d sheets" % (s0,ns))
        nr = s0.nrows
        nc = s0.ncols
        if debug:
            print("%d x %d in %s" % (nr,nc,path))
        # find which columns store the first and last name, we key on that
        row_values = s0.row_values(2)
        col_ln = row_values.index('Last Name')
        col_fn = row_values.index('First Name')
        # C&VS had a few revisions....
        if row_values[0] == 'Reg Status':     # (added 
            if row_values[2] == 'Modified':   # (added oct 1)
                self.off = 2
            else:
                self.off = 1
        else:
            self.off = 0
        status = status and (row_values[0] == 'Reg Status')
        s={}
        for row in range(3,nr):     # first 3 rows are administrative
            if status:
                if s0.cell(row,0).value != 'New':
                    continue
            name = s0.cell(row,col_ln).value + ", " + s0.cell(row,col_fn).value
            if name in s and debug:
                print("Warning: duplicate entry for %s" % name)
            s[name] = s0.row(row)

        if debug:
            print("Accepted %d entries" % len(s))
        return (s,row_values)

    def yopen(self, path, debug=False):
        """
        Return IVOA names
        
        path     file
        debug    print more
        
        """

        book = xlrd.open_workbook(path)
        ns = book.nsheets
        s0 = book.sheet_by_index(0)
        if ns != 1:
            print("Warning: %s has %d sheets" % (s0,ns))
        nr = s0.nrows
        nc = s0.ncols
        if debug:
            print("%d x %d in %s" % (nr,nc,path))
        # find which columns store the first and last name, we key on that
        row_values = s0.row_values(0)
        col_name = 1
        s={}
        for row in range(2,nr):     # first 3 rows are administrative
            name = s0.cell(row,col_name).value 
            if name in s and debug:
                print("Warning: duplicate entry for %s" % name)
            s[name] = s0.row(row)

        if debug:
            print("IVOA Accepted %d entries" % len(s))
        return (s,row_values)

    def zopen(self, path, debug=False):
        """
        Return Doodle poll stats
        
        path     file
        debug    print more
        
        """
        def fun(mat, order=False):
            """ return the lower diagonal of a square matrix
            """
            n = len(mat[0])
            m = (n*(n-1))//2
            c = np.zeros(m,dtype=int)
            k = 0
            msg = []
            for i in range(n):
                for j in range(i):
                    c[k] = mat[i,j]
                    k = k + 1
                    if order:
                        msg.append(" %d-%d" % (i+1,j+1))
            if order:
                return msg
            return c
        if debug:
            print("Doodle %s" % path)
        book = xlrd.open_workbook(path)
        ns = book.nsheets
        s0 = book.sheet_by_index(0)
        if ns != 1:
            print("Warning: %s has %d sheets" % (s0,ns))
        nr = s0.nrows
        nc = s0.ncols
        if debug:
            print("%d x %d in %s" % (nr,nc,path))
        # find which columns store the first and last name, we key on that
        row_values = s0.row_values(0)
        col_name = 1
        s={}
        for row in range(4,nr):            # first 4 rows are administrative
            name = s0.cell(row,0).value
            if name != 'Count':            # last row is 'Count', discard it too
                s[name] = s0.row(row)

        nr1 = nr-5
        nc1 = nc-1
        nz1 = ((nc1-1)*nc1)//2
        print("There are %d choices, %d people and %d cross choice counts" % (nc1,nr1,nz1))
        ok = np.zeros(nr1*nc1, dtype=int).reshape(nr1,nc1)
        mat0 = np.zeros(nc1*nc1, dtype=int)
        c = range(len(s))
        csum = np.zeros(nz1, dtype=int)
        csum = 0
        for (i,name) in zip(range(len(s)), s.keys()):
            for j in range(1,nc):
                if s[name][j].value == "OK":
                    ok[i,j-1] = 1
                else:
                    ok[i,j-1] = 0
            mat = np.outer(ok[i],ok[i])
            if type(csum) == type(int):
                csum = fun(mat)
            else:
                csum = csum + fun(mat)
            #print(i,ok[i],fun(mat),csum)
            #print(i,ok[i],csum)
        csumid = fun(mat,True)

        print('total choice counts: ',ok.sum(axis=0))
        print('total people counts: ',ok.sum(axis=1))
        print('total cross choice counts:')
        for i in range(nz1):
            print(i+1,csumid[i],csum[i])
            
        

        if debug:
            print("Accepted %d entries" % len(s))
        return (s,row_values)

    def expand_name(self,k):
        """ for a given (nick)name "k" find the full name we use in the hash
        """
        if k == '#':                                    # comment
            return None
        if k in self.x1.keys():                         # full match
            return k
        if self.lnames1.count(k) == 1:                  # match via last name
            return self.keys1[self.lnames1.index(k)]
        # one last try, min. match if 'k' is in lnames[]
        # for names in lnames:
        print("# %s" % k)
        return None
        
    def tab2list(self, filename, use_code=False):
        """ filename with "NAMES; Code"   - return the [names]
            if <NAMES> is <FNAME LNAME>, it adds them as <LNAME,FNAME>
        """
        o1 = io.open(filename, encoding="utf-8").readlines()
        o2 = []  # names
        o3 = []  # codes, should be required by now (I,O,B,F,T,P)
        o4 = []  # times, if appropriate (for I,O,B,F,T)
        nz = 0
        for i in range(len(o1)):
            s  = o1[i].strip() 
            w  = s.split(';')  # Split returns a list.
            nw = len(w)
            if nw == 0:    continue     # skip blank lines
            if w[0][0] =='#': continue  # skip comment lines
            if nw == 1:
                nz = nz + 1
                name = w[0].strip()
                code = 'Z%d' % nz
                time = 'N/A'
            elif nw == 2:
                name = w[0].strip()
                code = w[1].strip()
                time = 'TBD'
            elif nw == 3:
                name = w[0].strip()
                code = w[1].strip()
                time = w[2].strip()
            else:
                continue;

            ic = name.find(',')
            if ic < 0:
                names = name.split()
                if len(names) == 2:
                    name = names[1] + ', ' + names[0]
            o2.append(name)
            o3.append(code)
            o4.append(time)
        if use_code:
            return (o2,o3,o4)
        return o2
    
    # switch to makeprogram.py instead
    #def tab2list2(self, filename):
    #    o1 = io.open(filename, encoding="utf-8").readlines()
    #    for i in range(len(o1)):
    #        s  = o1[i].strip() 
    #        w  = s.split(';')  # Split returns a list.
    #        nw = len(w)
    #        if nw == 0:    continue     # skip blank lines
    #        if w[0][0] =='#': 
    #           ws = w[0].split()
    #           if w[1][0] == 'S': # starting a new session
    #              session_num = w[1][1:]
    #              newsession = True
    #           continue # for now skip other comments
    #
    #        # trim the tabs
    #        for w in range(len(w)):
    #            w[i] = w[i].strip()
            

    def print_col(self, col, verbose):
        """ print a given columns. expert mode
        """
        keys = list(self.x3.keys())
        keys.sort()
        for key in keys:
            r = self.x3[key]
            if verbose:
                print(r[col+self.off].value, key)
            else:
                print(r[col+self.off].value)

    def report_0(self):
        """ print just the 'Lastname, Firstname' key
        """
        keys = list(self.x3.keys())
        keys.sort()
        for key in keys:
            print(key)

    def report_0a(self):
        """ print the 'Lastname,  Firstname        Institution'
        """
        keys = list(self.x3.keys())
        keys.sort()
        index = self.r3.index('Univ/Affiliation')
        for key in keys:
            print(key,self.x3[key][index].value)

    def report_1(self, abstract=False, cat = False):
        keys = list(self.x1.keys())
        keys.sort()
        for key in keys:
            present   = self.x1[key][22].value
            title1    = self.x1[key][23].value
            abstract1 = self.x1[key][24].value
            theme1    = self.x1[key][20].value
            theme1a   = self.x1[key][21].value
            r = self.x3[key]
            focus_demo = r[25+self.off].value
            demo_booth = r[26+self.off].value
            email      = r[14+self.off].value
            theme = theme1[:theme1.find(')')]
                
            if abstract: print(" ")
            
            if present == 'Talk/Focus Demo':
                if focus_demo == '1' and demo_booth == '1':
                    ptype = "F+B"
                elif focus_demo == '1':
                    ptype = "F"                    
                elif demo_booth == '1':
                    ptype = "B"                    
                else:
                    ptype = "O"                    
            elif present == 'Poster':
                ptype = "P"
            else:
                ptype = "X"
                
            if cat:
                print("%s    ; %s%s." % (key,ptype,theme))
            else:
                if True:
                    print(ptype,key,email,title1)
                else:
                    print(ptype,key,email)
                    print("  TITLE:",title1)

            if abstract:
                print("    ABS:",abstract1)
                print("    T:",theme1)
                print("   TO:",theme1a)
            if key in self.x2:
                present2  = self.x2[key][22].value
                title2    = self.x2[key][23].value
                abstract2 = self.x2[key][23].value
                print("  ABS2",key,title2)
                if abstract: print("    ABS:",abstract2)

    def report_1a(self, tabname = None):
        keys = list(self.x1.keys())
        keys.sort()
        for key in keys:
            present   = self.x1[key][22].value
            title1    = self.x1[key][23].value
            abstract1 = self.x1[key][24].value
            theme1    = self.x1[key][20].value
            theme1a   = self.x1[key][21].value
            r = self.x3[key]
            focus_demo = r[25+self.off].value
            demo_booth = r[26+self.off].value
            email      = r[14+self.off].value
            theme = theme1[:theme1.find(')')]
                
            if abstract: print(" ")
            
            if present == 'Talk/Focus Demo':
                if focus_demo == '1' and demo_booth == '1':
                    ptype = "F+B"
                elif focus_demo == '1':
                    ptype = "F"                    
                elif demo_booth == '1':
                    ptype = "B"                    
                else:
                    ptype = "O"                    
            elif present == 'Poster':
                ptype = "P"
            else:
                ptype = "X"
                
            if cat:
                print("%s    ; %s%s." % (key,ptype,theme))
            else:
                print(ptype,key,email,title1)

            if abstract:
                print("    ABS:",abstract1)
                print("    T:",theme1)
                print("   TO:",theme1a)
            if key in self.x2:
                present2  = self.x2[key][22].value
                title2    = self.x2[key][23].value
                abstract2 = self.x2[key][23].value
                print("  ABS2",key,title2)
                if abstract: print("    ABS:",abstract2)

    def report_2(self,x1,x2,x3):
        keys = list(self.x1.keys())
        keys.sort()
        for key in keys:
            present = x1[key][22+self.off].value
            r = x3[key]
            focus_demo = r[25+self.off].value
            demo_booth = r[26+self.off].value
            print(present,key,'f=%s' % focus_demo,'d=%s' % demo_booth)

    def report_3(self,o1, count=False):
        """ report a selection of presenters based on list of names
        """
        n=0
        for k in o1:
            key = self.expand_name(k)
            if key != None:
                n         = n + 1
                present   = self.x1[key][22].value
                title1    = self.x1[key][23].value
                abstract1 = self.x1[key][24].value
                if count:
                    print(n,key,present,title1)
                else:
                    print(key,'-',title1)

    def report_3a(self,o1,o2,o3, count=False, dirname='www/abstracts', index=True, themes=0, posters=False):
        """ report a selection of presenters based on list of names
            o1 = names
            o2 = codes
            o3 = times
        """
        # first loop once to know the siblings
        if posters:
           pfile = open("posters.list","w")
        n=0
        co1 = []
        co2 = []
        co3 = []
        for (k,c,t) in zip(o1,o2,o3):
            key = self.expand_name(k)
            if key != None:
                n = n + 1
                co1.append(k)
                co2.append(c)
                co3.append(t)
        print("Processed %d out of %d" % (n,len(o1)))

        # now loop for real to create the html
        old_theme1 = "N/A"
        old_focus = 0
        for i in range(n):
            k = co1[i]
            c = co2[i]
            t = co3[i]
            key = self.expand_name(k)
            if key != None:
                theme     = self.x1[key][20].value
                present   = self.x1[key][22].value
                title1    = self.x1[key][23].value
                abstract1 = self.x1[key][24].value
                theme1    = theme[theme.find(')')+1:]
                if themes > 0:
                    if c[0] == 'F':
                        if old_focus == 0:
                            print("<!-- HREF4theme --> <br><a name='#FocusDemos'><h3 class='session-heading'>Focus Demos</h3><br>\n")
                            old_focus = 1
                    elif theme1 != old_theme1:
                        print("<!-- HREF4theme --> <br><a name='#%s'><h3 class='session-heading'>%s</h3><br>\n" % (theme1.strip(), theme1))
                        old_theme1 = theme1
                
                if count:
                    print(n,key,present,title1)
                else:
                    fn = dirname + '/' + c + '.html'
                    fp = open(fn,'w')
                    fp.write(self.getheader())
                    if i > 0:
                        msg = 'Prev: <a href="/abstracts/%s.html">%s</a> ' % (co2[i-1],co2[i-1])
                        fp.write(msg)
                    if i < n-1:
                        msg = 'Next: <a href="/abstracts/%s.html">%s</a> ' % (co2[i+1],co2[i+1])
                        fp.write(msg)
                    fp.write("<br><br>\n")
                    
                    pcode     = c.replace('.','-')                    
                    msg = '<b>%s: %s</b>\n' % (c, key)   ; fp.write(msg)
                    msg = '<br>\n'                       ; fp.write(msg)
                    if True:
                        a1 = self.x1[key][9].value
                        b1 = self.x1[key][10].value;
                        if len(b1) > 0: b1 = '(' + b1 + ')'
                        a2 = self.x1[key][11].value
                        b2 = self.x1[key][12].value;
                        if len(b2) > 0: b2 = '(' + b2 + ')'
                        a3 = self.x1[key][13].value
                        b3 = self.x1[key][14].value;
                        if len(b3) > 0: b3 = '(' + b3 + ')'
                        a4 = self.x1[key][15].value
                        b4 = self.x1[key][16].value;
                        if len(b4) > 0: b4 = '(' + b4 + ')'
                        a5 = self.x1[key][17].value
                        b5 = self.x1[key][18].value;
                        if len(b5) > 0: b5 = '(' + b5 + ')'
                        a6 = self.x1[key][19].value
                        msg = '%s %s <br> %s %s <br>  %s %s<br>  %s %s<br>  %s %s<br>  %s' % (a1,b1,a2,b2,a3,b3,a4,b4,a5,b5,a6);  fp.write(msg)
                        msg = '<br><br>\n'                            ; fp.write(msg)                                                                
                    if c[0] != 'P':
                        msg = '<b>Time: %s</b>\n' % t                 ; fp.write(msg)
                    msg = '<br>\n'                                    ; fp.write(msg)
                    msg = '<b>Theme:</b> %s\n' % theme1               ; fp.write(msg)
                    msg = '<br>\n'                                    ; fp.write(msg)                    
                    msg = '<b>Title:</b> <i>%s</i>\n' % title1        ; fp.write(msg)
                    msg = '<br><p>\n'                                ; fp.write(msg)                                        
                    msg = '%s</p>\n' % abstract1                          ; fp.write(msg)
                    if c[0] == 'P' and posters:
                       txt = "%s\t%s\t\t%s\n" % (c,key,title1)
                       pfile.write(txt)
                    msg = 'Link to PDF (may not be available yet): <A HREF=%s.pdf>%s.pdf</A>\n' % (pcode,pcode)
                    fp.write(msg)
                    fp.write(self.getfooter())
                    fp.close()
                    if index:
                        msg = '<a href="/abstracts/%s.html">%s </a> <b>%s</b> :  %s<br>' % (c,key,pcode,title1)
                        print(msg)
        if posters: pfile.close()
        if index:
            print("<!-- HREF4theme  Generated %s --><br>\n" % datetime.datetime.now().isoformat())

            
    def report_3b(self,o1,o2,o3, count=False, dirname='.'):
        """ report a selection of presenters based on list of names - latex version of report_3a
            o1 = names
            o2 = codes
            o3 = times
        """
        def latex(text):
            """ attempt to turn text into latex
            """
            text = text.replace('_','\_')
            text = text.replace('&','\&')
            text = text.replace('#','\#')
            text = text.replace('^','\^')
            text = text.replace('%','\%')            
            return text
        
        fn = dirname + '/' + 'abstracts.tex'
        fp = open(fn,'w')
        fp.write(_header2)
        fp.write('Generated %s\\newpage\n\n' % datetime.datetime.now().isoformat())
        
        n=0
        for (k,c,t) in zip(o1,o2,o3):
            key = self.expand_name(k)
            if key != None:
                n         = n + 1
                email     = self.x1[key][6].value
                theme     = self.x1[key][20].value
                present   = self.x1[key][22].value
                title1    = self.x1[key][23].value
                abstract1 = self.x1[key][24].value
                theme1    = theme[theme.find(')')+1:]
                if count:
                    print(n,key,present,title1)
                else:
                    msg = '\\subsection*{%s: %s}\n' % (c, title1)              ; fp.write(msg)
                    msg = '{\\bf Theme:} %s\\newline\n' % theme1               ; fp.write(msg)
                    msg = '{\\bf Author(s):}\\newline\n'                       ; fp.write(msg)
                    if True:
                        a1 = self.x1[key][9].value
                        b1 = self.x1[key][10].value;
                        if len(b1) > 0: b1 = '(' + b1 + ')'
                        a2 = self.x1[key][11].value
                        b2 = self.x1[key][12].value;
                        if len(b2) > 0: b2 = '(' + b2 + ')'
                        a3 = self.x1[key][13].value
                        b3 = self.x1[key][14].value;
                        if len(b3) > 0: b3 = '(' + b3 + ')'
                        a4 = self.x1[key][15].value
                        b4 = self.x1[key][16].value;
                        if len(b4) > 0: b4 = '(' + b4 + ')'
                        a5 = self.x1[key][17].value
                        b5 = self.x1[key][18].value;
                        if len(b5) > 0: b5 = '(' + b5 + ')'
                        a6 = self.x1[key][19].value
                        msg = '%s %s \\newline %s %s \\newline  %s %s\\newline  %s %s\\newline %s %s\\newline  %s' % (a1,b1,a2,b2,a3,b3,a4,b4,a5,b5,a6);
                        fp.write(latex(msg))
                        msg = '\\newline\\newline\n'                       ;
                        fp.write(latex(msg))                                                                
                    if c[0] != 'P':
                        msg = '{\\bf Time:} %s\\newline\n' % t        ; fp.write(latex(msg))
                        msg = '\\newline\n'                           ; fp.write(latex(msg))
                    # msg = '{\\it %s}\\newline\n' % title1             ; fp.write(latex(msg))
                    msg = '{\\bf Contact:} {\\it %s}\\newline\n' % email              ; fp.write(latex(msg))                    
                    msg = '\\newline\\newline\n'                      ; fp.write(latex(msg))
                    msg = '{\\bf Abstract:}\\newline\n'               ; fp.write(latex(msg))
                    msg = '%s\\newline\n' % abstract1                 ; fp.write(latex(msg))
                    msg = '{\\bf Notes:}\\newline\n'                  ; fp.write(latex(msg))
                    msg = '{\\newpage\n'                              ; fp.write(latex(msg))                    
        fp.write(_footer2)
        fp.close()
                    
    def report_3c(self,o1,o2,o3, template='template.tex', comment = False, dirname='papers'):
        """ write a template conferences proceedings contribution
            o1 = names
            o2 = codes
            o3 = times
        """
        def latex(text):
            """ attempt to turn text into latex
            """
            text = text.replace('_','\_')
            text = text.replace('&','\&')
            text = text.replace('#','\#')
            text = text.replace('^','\^')
            text = text.replace('%','\%')            
            return text
        def read_template(filename):
            # with open(filename, 'r', encoding='utf-8') as template_file:
            with open(filename, 'r') as template_file:
                template_file_content = template_file.read()
            return Template(template_file_content)

        T_paper = read_template(template)


        fn1 = dirname + '/' + 'toc.txt'
        fp1 = open(fn1,'w')
        fp1.write("%% created by adass2018.py::report_3c()\n")
        n=0
        for (k,c,t) in zip(o1,o2,o3):
            key = self.expand_name(k)
            if key != None:
                n         = n + 1
                fname     = self.x1[key][3].value
                lname     = self.x1[key][4].value
                iname     = self.x1[key][5].value
                email     = self.x1[key][6].value
                pcode     = c.replace('.','-')
                title1    = latex(self.x1[key][23].value)
                abstract1 = latex(self.x1[key][24].value)
                kwargs = {}
                kwargs['FNAME']    = fname
                kwargs['FNAMEI']   = fname[0]
                kwargs['LNAME']    = lname
                kwargs['INAME']    = iname
                kwargs['EMAIL']    = email
                kwargs['TITLE']    = title1
                kwargs['ABSTRACT'] = abstract1
                kwargs['F1']       = '$^1$'
                kwargs['F2']       = '$^2$'
                kwargs['F3']       = '$^3$'
                kwargs['LENA']     = str(len(abstract1))
                kwargs['LENW']     = ""
                kwargs['PCODE']    = pcode
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
                msg = '\\tocinsertentry[r]{%s}{%s.~%s}{authors/%s_inc}\n' % (title1,fname[0],lname,pcode)
                fp1.write(msg)
        fp1.close()
                    
    def report_4(self, full = False, name=None):
        """ report emails only"""

        keys = list(self.x3.keys())
        keys.sort()
        if name != None:  full = True
        for key in keys:
            r = self.x3[key]
            email = r[14+self.off].value
            if full:
                msg = '"%s" <%s>' % (key,email)
                if name == None:
                    print(msg)
                else:
                    if msg.upper().find(name.upper()) > 0:
                        print(msg)
            else:
                print(email)

    def report_5(self, latex=True):
        """ report IVOA names"""

        keys = list(self.x4.keys())
        # keys.sort()
        for key in keys:
            r = self.x4[key]
            name = r[1].value
            inst = r[3].value
            if latex:
                print("\\confpin{%s}{%s}" % (name,inst))
            else:
                print(name)

    def report_6(self,o1, col=0):
        """ report a column
        """
        n=0
        for k in o1:
            if k in self.x3.keys():
                txtcol= self.x3[k][col].value
                msg = '%-33s %s' % (k,txtcol)
                print(msg)
            else:
                print('#', k)
                
    def report_7(self, latex=True):
        """ report for latex attendee file
        """

        keys = list(self.x3.keys())
        keys.sort()
        for key in keys:
            r = self.x3[key]
            fname = r[3+self.off].value
            lname = r[4+self.off].value
            insti = self.latex(r[6+self.off].value)
            count = r[12+self.off].value
            
            msg = '\\attendee{\\textsc{%s %s}}{}{%s}{%s}' % (fname,lname,insti,count)
            print(msg)

    def report_demo(self):
        """ report who wants demo table
        """
        for key in self.x3.keys():
            r = self.x3[key]
            focus_demo  = r[25+self.off].value
            comm_booth  = r[26+self.off].value
            astro_booth = r[27+self.off].value            
            if focus_demo != "":
                print(key,' FOCUS')
            if comm_booth != "":
                print(key,' COMMERCIAL')
            if astro_booth != "":
                print(key,' ASTRO')

 
if __name__ == "__main__":
    
    a = adass('reg')
    
    if len(sys.argv) == 3:                  # specific colum from registration
        o1 = a.tab2list(sys.argv[1])
        col = int(sys.argv[2])
        a.report_6(o1,col)
    elif len(sys.argv) == 2:                # titles 
        o1 = a.tab2list(sys.argv[1])
        a.report_3(o1,False)
    else:                                   # all , one or two liner
        a.report_1(False)                 
