#! /usr/bin/env python


from __future__ import print_function

import xlrd
import sys
import adass2018 as adass
 
if __name__ == "__main__":
    debug = True
    a = adass.adass('reg', debug)
    
    if len(sys.argv) == 3:
        add_themes = int(sys.argv[2])
        (o1,o2,o3) = a.tab2list(sys.argv[1],True)
        print(o1)
        print(o2)
        print(o3)
        print(len(o1),len(o2),len(o3))
        a.report_3a(o1,o2,o3,themes=add_themes,posters=True)
        a.report_3b(o1,o2,o3)        
    else:
        a.report_1(True)
