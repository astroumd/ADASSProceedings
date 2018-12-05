#! /usr/bin/env python
#
# take a self-contained ADASS paper and output the embedable version
#
# TODO?
# Should it produce toc entries for inclusion, e.g.
#   \tocinsertentry[r]{ TITLE }{A.~Aloisi (Invited Speaker)}{authors/I1-2_inc} 

import sys


def read1(filename):
    """ read tex file into lines for processing
    """
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines

test = """
% test section
\documentclass[11pt,twoside]{article}
\usepackage{asp2014}

\aspSuppressVolSlug
\resetcounters

\bibliographystyle{asp2014}

\begin{document}

The document...

%\aindex{Author1}
%\aindex{Coauthor2}

bibliography{O5-3}

\end{document}

"""

triggers = []
triggers.append((True,"\\documentclass"))
triggers.append((True,"\\usepackage"))
triggers.append((True,"\\begin{document}"))
triggers.append((True,"\\end{document}"))
triggers.append((False,"%\\aindex"))
#triggers.append((True,"\\bibliography"))




if len(sys.argv) == 1:
    print("Usage: %s name.tex" % sys.argv[0])
    sys.exit(0)

paper = sys.argv[1]
lines = read1(paper)



for l in lines:
    triggered = False
    for t in triggers:
        if l.find(t[1]) == 0:
            if t[0]:
                print("%%TEX2INC %s" % l.strip())
            else:
                print("%s" % l[1:].strip())
            triggered = True
            continue
    if not triggered:
        print(l.strip())
