#! /usr/bin/env python


from __future__ import print_function

import xlrd
import sys
import adass2018 as adass

if __name__ == "__main__":
    a = adass.adass('reg')
    col = int(sys.argv[1])
    verbose = False
    if len(sys.argv) > 2:
        verbose = True
    if col < 0:
        a.report_0()
    else:
        a.print_col(col,verbose)
