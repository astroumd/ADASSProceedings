#! /usr/bin/env python


from __future__ import print_function

import sys
import xlrd
import adass2018 as adass

def open_file(path):
    book = xlrd.open_workbook(path)
    ns = book.nsheets
    s0 = book.sheet_by_index(0)
    n = s0.nrows
    for row in range(3,n):
        fname = s0.cell(row,3).value
        lname = s0.cell(row,4).value
        email = s0.cell(row,14).value
        #print   '"',fname,lname,'" <',email,'>'
        print(email)
        

 
if __name__ == "__main__":
    a = adass.adass('reg')
    a.report_7()
