#! /usr/bin/env python


from __future__ import print_function

import xlrd
import sys
import adass2018 as adass
 
if __name__ == "__main__":
    debug = True
    a = adass.adass('reg', debug)
    
    a.report_demo()
