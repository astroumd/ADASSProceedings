#!/usr/bin/env python
from astropy.table import Table
import pandas as pd
import codecs
import re
from pathlib import Path
from html.entities import codepoint2name


class Program(object):

  def __init__(self,infile,format):
    self._file = infile
    self._t = Table.read(infile,format=format)
    self._df = self._t.to_pandas()
    self.a = None
    self.abstracts = dict()
    # PDF presentations are currently only stored on the final rootdir
    self.presentdir= "/home/www/adass2018/abstracts/"
    codecs.register_error('html_replace', self.html_replace)
    

  def _getadass(self):
    from adass2018 import adass
    self.a = adass("reg")

  def maketitle(self):
    if self.a == None:
       self._getadass()
    titles = []
    a1 = []
    for b,q,h,t,ab in zip(self._t["last"],self._t["first"],self._t['code'],self._t['title'],self._t['abstract']):
       c = b + ", " + q
       #print("Key = %s"%c)
       if h[0] == "H" or h[0] == "T" or h[0] == "B":
           # save the title of the session, tutorial, or BOF
           #print("Saving %s"%t)
           titles.append(t)
           a1.append("None")
       else:
           #kkk special case for Varshney
           if h[0] == "x" :
               titles.append(t)
           else:
               z = self.a.titles.get(c,"TBD")
               titles.append(z)
           # special case for Varshney and O'Tool bof
           if c in self.a.abstracts:
               self.abstracts[c]  = self.a.abstracts[c]
               a1.append(self.abstracts[c])
           elif ab != None:
               print("For title %s, Saving abstract %s"%(t,ab))
               a1.append(ab)
           else:
               a1.append("TBD")
         

    self._t['title'] = titles
    self._t['abstract'] = a1
    self._df = self._t.to_pandas()

  def write(self,file,format,include_abstracts):
    if include_abstracts:
        self._t.write(file,overwrite=True,format=format)
    else:
        t = self._t.copy()
        t.remove_column('abstract')
        t.write(file,overwrite=True,format=format)

  def sessionsheet(self):
      fp = codecs.open('sessionsheets.tex','w','utf-8')
      fp.write("\\documentclass[12pt]{article}\n\\textwidth 6.5truein \n\\textheight 9.5truein\n\\oddsidemargin 0.0pt \n\\evensidemargin 0.0pt \n\\topmargin -0.5in \n\\Huge\n\\pagestyle{empty}\n\\begin{document}")
      days = self._df.day.unique()
      #bofAB = 'SALON AB\\newline '
      #bofG  = 'SALON G\\newline '
      bofAB = '{\it SALON AB}\\newline '
      bofG  = '{\it SALON G}\\newline '
      for d in days:
        daydf = self._df[(self._df.day == d)]
        title=True
        for row_index,row in daydf.iterrows():
           h = row['code'][0]
           if h == "H":
              fp.write("\\newpage\n")
              fp.write("\\section*{%s -- SESSION %s}\n"%(d.upper(),row['session']))
              fp.write("\\subsection*{%s}\n"% (row['title'].upper()))
              fp.write("\\ \\newline")
              fp.write("\\subsection*{\\underline{Invited and Contributed}}\n")
           if h == "I" or h == "O" or h == "x" or h == "L":
              if row['institution'] == "nan" or row['institution']=="N/A":
                  fp.write("%s -- %s $\\>$ %s %s\n\\newline\\newline\n"%(row['start'],row['end'],row['first'],row['last']))
              else:
                  fp.write("%s -- %s $\\>$ %s %s (%s) \n\\newline{\\bf %s}\\newline\\newline\n"%(row['start'],row['end'],row['first'],row['last'],row['institution'],row['title']))
           if h == "F":
              fp.write("\\subsection*{\\underline{Focus Demo}}\n")
              fp.write("%s -- %s $\\>$ %s %s (%s) \n\\newline{\\bf %s}\\newline\\newline\n"%(row['start'],row['end'],row['first'],row['last'],row['institution'],row['title']))
           if h == "B":
              if title:
                  fp.write("\\subsection*{\\underline{Birds of Feather}}\n")
                  title=False
              s  = row['code'][1]
              if s == '1' or s == '3' or s == '5' or s == '7':
                 bofAB += ("%s -- %s $\\>$ %s %s (%s) \n\\newline{\\bf %s}\\newline\\newline\n"%(row['start'],row['end'],row['first'],row['last'],row['institution'],row['title']))
              else: 
                 bofG += ("%s -- %s $\\>$ %s %s (%s) \n\\newline{\\bf %s}\\newline\\newline\n"%(row['start'],row['end'],row['first'],row['last'],row['institution'],row['title']))

        if bofAB != '{\it SALON AB}\\newline ':
           fp.write(bofAB)
           bofAB = '{\it SALON AB}\\newline '
        if bofG != '{\it SALON G}\\newline ':
           fp.write(bofG)
           bofG  = '{\it SALON G}\\newline '
     
     
        #fp.write("\\newpage\n")
      fp.write("\\end{document}")
      

  def getpdf(self,talkid):
    # remove special char x used for other reasons and replace . with -
    pdf = re.sub('^x','',talkid.replace('.','-')) + '.pdf'
    fullfname = self.presentdir + pdf
    fname = "abstracts/"+pdf
    if Path(fullfname).exists():
        return '</p><br><p><a href="'+fname+'">Presentation file</a>'
    else:
        #print("%s doesn't exist"%fullfname)
        print(pdf)
        return ""

  def tohtml(self,days):
    fp = codecs.open('program.html','w','utf-8')
    colors = {"C": "lightblue", "L": "yellow", "F":"#ddd", "I":"orange", "Q":"lightgreen", "B":"yellow", "H":"#e9f9f9", "T":"#ddd"}

    head = '<!DOCTYPE html> <html lang="en">\n <head>\n <!-- Required meta tags --> \n <meta name="viewport" content="width=device-width, initial-scale=1, shrink-t o-fit=no">\n <title>ADASS XXVIII Program</title>\n <!-- Bootstrap CSS -->\n <link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css" >\n <!-- Icon -->\n <link rel="stylesheet" type="text/css" href="assets/fonts/line-icons.css">\n <!-- Slicknav -->\n <link rel="stylesheet" type="text/css" href="assets/css/slicknav.css">\n <!-- Nivo Lightbox -->\n <link rel="stylesheet" type="text/css" href="assets/css/nivo-lightbox.css" >\n <!-- Animate -->\n <link rel="stylesheet" type="text/css" href="assets/css/animate.css">\n <!-- Main Style -->\n <link rel="stylesheet" type="text/css" href="assets/css/main.css">\n <!-- Responsive Style -->\n <link rel="stylesheet" type="text/css" href="assets/css/responsive.css">\n   <!-- Custom styles for this template -->\n <link href="css/modern-business.css" rel="stylesheet">\n <link href="https://fonts.googleapis.com/css?family=Carrois+Gothic+SC" rel="stylesheet"> </head> <body>'

    begin = '<!--#include virtual="includes/nav.inc"-->\n<!--#include virtual="schedule-menu.html" -->'
    end_sched = '<!--#include virtual="schedule-end.html" -->'
    end_html = '<div id="preloader"> <div class="sk-circle"> <div class="sk-circle1 sk-child"></div> <div class="sk-circle2 sk-child"></div> <div class="sk-circle3 sk-child"></div> <div class="sk-circle4 sk-child"></div> <div class="sk-circle5 sk-child"></div> <div class="sk-circle6 sk-child"></div> <div class="sk-circle7 sk-child"></div> <div class="sk-circle8 sk-child"></div> <div class="sk-circle9 sk-child"></div> <div class="sk-circle10 sk-child"></div> <div class="sk-circle11 sk-child"></div> <div class="sk-circle12 sk-child"></div> </div> </div>\n\n <!-- jQuery first, then Popper.js, then Bootstrap JS -->\n <script src="assets/js/jquery-min.js"></script>\n <script src="assets/js/popper.min.js"></script>\n <script src="assets/js/bootstrap.min.js"></script>\n <script src="assets/js/jquery.countdown.min.js"></script>\n <script src="assets/js/jquery.nav.js"></script>\n <script src="assets/js/jquery.easing.min.js"></script>\n <script src="assets/js/wow.js"></script>\n <script src="assets/js/jquery.slicknav.js"></script>\n <script src="assets/js/nivo-lightbox.js"></script>\n <script src="assets/js/main.js"></script>\n </body> </html>'

    tabstart='<div class="schedule-tab-content col-md-9 col-lg-9 col-xs-12 clearfix"> <div class="tab-content" id="myTabContent">'

    fp.write(("%s\n%s\n%s\n" %(head,begin,tabstart)))

    for theday in days:
      xdf = self._df[(self._df['day']==theday)]
      if theday == "Sunday":
         active="active"
      else:
         active=""
      tabopen = '<div class="tab-pane fade show %s" id="%s" role="tabpanel" aria-labelledby="%s-tab">\n\n'%(active,theday,theday)
      accordion_start='<div id="accordion">'
      accordion_end   ='</div><!-- accordion -->\n</div><!-- end %s -->' %(theday)

      #print(tabopen)
      #print(accordion_start)
      fp.write(tabopen)
      fp.write(accordion_start)
      for row_index,row in xdf.iterrows():
            key = row['last'] + ", " + row['first']
            talkid        = row['code']
            #speaker_first = self.encode_for_html(row['first']).decode('utf-8').replace("&amp;","&")
            #speaker_last  = self.encode_for_html(row['last']).decode('utf-8').replace("&amp;","&")
            speaker_first = row['first']
            speaker_last  = row['last']
            title         = row['title']
            time_start    = row['start']
            time_end      = row['end']
            #abstract      = self.a.abstracts.get(key,"TBD")
            if key in self.abstracts:
                abstract      = self.abstracts[key].value
            elif row['abstract'] != None:
                abstract      = row['abstract']
            else:
                abstract = "TBD"
            # make sure it gets into the votable
            row['abstract'] = abstract
           
            #if key in self.a.x1:
            #    abstract      = self.a.x1[key][24].value

            if talkid[0] == "H":  # session heading
                #print("doing session heading %s"% title)
                card = '<div class="card"> \n<div id="headingSession%s"> <div class="card-header p-2 m-0 session-heading" style="background-color:%s;"> <h6 align="center"><i>Session %s</i></h5><h5 align="center">%s</h5><h6 align="center">Chair: %s %s</h6> \n</div></div></div>\n\n' %(row['session'],colors[talkid[0]],row['session'],title,speaker_first,speaker_last)
                fp.write(card)
            elif talkid[0] == "C" or talkid[0] == "L" or talkid[0] == "Q":
                card = '<div class="card"> \n<div id="heading%s"> <div class="card-header p-0 m-0" style="background-color:%s;">\n <table class="table table-borderless p-0 m-0"><tr><td><h6 align="left">%s&ndash;%s</h6></td><td> <h6 align="left">%s %s</h6></td></tr> </table> \n</div></div></div>\n\n' %(talkid,colors[talkid[0]],time_start,time_end,speaker_first,speaker_last)

                fp.write(card)
            else:
                c = colors.get(talkid[0],"#ffffff")
                card1 = '<div class="card"> \n<div id="heading%s"> <div class="collapsed card-header p-0 m-0" style="background-color:%s;" data-toggle="collapse" data-target="#collapse%s" aria-expanded="false" aria-controls="collapse%s">\n <table class="table table-borderless p-0 m-0"><tr><td><h6 class="text-left">%s&ndash;%s</h6></td><td> <h6 class="text-left">%s %s &nbsp; <i>%s</i></h6></td></tr> </table> \n</div> </div>\n\n <div id="collapse%s" class="collapse" aria-labelledby="heading%s" data-parent="#accordion"> <div class="card-body"><p>' %(talkid,c,talkid,talkid,time_start,time_end,speaker_first,speaker_last,title,talkid,talkid)
#                card = '<div class="card"> \n<div id="heading%s"> <div class="collapsed card-header p-0 m-0" style="background-color:%s;" data-toggle="collapse" data-target="#collapse%s" aria-expanded="false" aria-controls="collapse%s">\n <table class="table table-borderless p-0 m-0"><tr><td><h6 class="text-left">%s&ndash;%s</h6></td><td> <h6 class="text-left">%s %s &nbsp; <i>%s</i></h6></td></tr> </table> \n</div> </div>\n\n <div id="collapse%s" class="collapse" aria-labelledby="heading%s" data-parent="#accordion"> <div class="card-body"> <p>%s</p> </div> </div></div>\n\n' %(talkid,c,talkid,talkid,time_start,time_end,speaker_first,speaker_last,title,talkid,talkid,abstract)
                card2="</p></div></div></div>\n\n"

                fp.write(card1)
                if talkid[0] == "T":
                    fp.write('See <a href="tutorial.html">Tutorials Page</a>')
                elif talkid[0] == "B":
                    fp.write('See <a href="bof.html">BoF Page</a>')
                else:
                    fp.write(abstract)
                    fp.write(self.getpdf(talkid))
                fp.write(card2)
      fp.write(accordion_end)

    fp.write(end_sched)
    fp.write(end_html)
    fp.close()

  ###########################################################
  # utf-8 to html encoding
  # @See https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s24.html
  def html_replace(self,exc):
      if isinstance(exc, (UnicodeEncodeError, UnicodeTranslateError)):
          print(exc)
          s = [ u'&amp;%s;' % codepoint2name[ord(c)]
                for c in exc.object[exc.start:exc.end] ]
          return ''.join(s), exc.end
      else:
          raise TypeError("can't handle %s" % exc.__name__) 

  def encode_for_html(self,unicode_data, encoding='ascii'):
      return unicode_data.encode(encoding, 'html_replace')
  ###########################################################


if __name__ == "__main__":
    _days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    
    p = Program('orals2.ipac','ipac')
    p.maketitle()
    p.write('program.vot',format='votable',include_abstracts=True)
    p.write('program.ipac',format='ipac',include_abstracts=False)
    #p.write('program.ipac','ipac') Exception
    p.tohtml(_days)
    if False:
        print("making session sheets in sessionsheets.tex")
        p.sessionsheet()
