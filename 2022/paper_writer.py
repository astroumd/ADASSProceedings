#! /usr/bin/env python3
#
#  personalized templates for 2022 based off a papers.tab file

import sys
import adass2022 as adass
 
if __name__ == "__main__":
    debug = True
    a = adass.adass('.', debug)

    (o1,o2,o3) = a.tab2list(sys.argv[1],True)
    print(len(o1),len(o2),len(o3))
            
    if len(sys.argv) == 3:
        a.report_3c(o1,o2,o3,sys.argv[2])
    elif len(sys.argv) == 4:
        a.report_3c(o1,o2,o3,sys.argv[2],sys.argv[3])
    else:
        print("Usage:")
