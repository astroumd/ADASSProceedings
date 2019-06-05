#! /usr/bin/env python


from __future__ import print_function

import xlrd
import sys
import adass2018 as adass

if __name__ == "__main__":
    a = adass.adass('reg')
    a.zopen(sys.argv[1])
