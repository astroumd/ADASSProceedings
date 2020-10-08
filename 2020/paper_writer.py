#! /usr/bin/env python
#
#  personalized templates for 2020 based off a papers.tab file

import sys
import adass2020 as adass
 
if __name__ == "__main__":
    debug = True
    a = adass.adass('.', debug)
    
    if len(sys.argv) == 3:
        (o1,o2,o3) = a.tab2list(sys.argv[1],True)
        #print(o1)
        #print(o2)
        #print(o3)
        print(len(o1),len(o2),len(o3))
        a.report_3c(o1,o2,o3,sys.argv[2])
        a.report_3b(o1,o2,o3)
    elif len(sys.argv) == 4:
        (o1,o2,o3) = a.tab2list(sys.argv[1],True)
        print(o1)
        print(o2)
        print(o3)
        print(len(o1),len(o2),len(o3))
        a.report_3c(o1,o2,o3,sys.argv[2],comment=True)
        a.report_3b(o1,o2,o3)        
    else:
        print("Usage:")
