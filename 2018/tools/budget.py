#! /usr/bin/env python
#
#   ADASS 2018 budget analysis   - 8-sep-2017  - Peter Teuben
#
#   Usage:  budget.py [np=] [nb=] ... [f_banquet=] ...
#
#   Any of the variables defined before the functions can be changed this way.

from __future__ import print_function

version = "6-jul-2018"

htax = 0.22  # hotel tax
ctax = 0.03  # credit card tax

np  = 350   # number of registration
ns  =  25   # number of students in this registration
nb  =  60   # number of poster boards (each can hold 2 per side)
nt  = 100   # number of people for tutorial [not used anymore, see f_tutorial]
nz  =   4   # number of power strips

f_reception  = 0.85     # fraction of people going to reception
f_banquet    = 0.60     # fraction of people going to banquet
f_tutorial   = 0.05     # fraction of people paying for tutorial
f_attend3    = 0.90     # 90% expected attendance for the first 3 days
f_attend1    = 0.75     # 75% expected attendance for the last half day
f_early1     = 0.80     # 80% will register early (regular)
f_early2     = 0.50     # 50% will register early (students)


if False:
    # test with fewer variations
    print("WARNING: running an unrealistic and limited variations model for testing")
    f_early1     = 1.00     # everybody pays early
    f_early2     = 1.00     #
    ns           = 0        # no students
    f_attend3    = 1.00     # 90% expected attendance for the first 3 days
    f_attend1    = 1.00     # 75% expected attendance for the last half day
    f_tutorial   = 0.00     # no tutorial

# fees per person
fpp1 = 35          # CVS fee per person
fpp2 = 550         # registration fee per person (early)
fpp3 = fpp2 + 100  # registration fee per person (late)
fpp4 = 200         # student fee (early)
fpp5 = fpp4 +  50  # student fee (late)
fpp6 = 50          # tutorial fee
fpp7 = 75          # banquet fee

# fixed fees (various of those are still hardcoded below)
fee1 = 3500        # CVS base fee

sub2 = 0           # placeholder to share between functions

cb1 = 50000        # sponsors contribution


# --- function: Income from registration 
#     (needs to be called first)

def income(np):
    global sub2

    er2 = (np-ns) *    f_early1  * fpp2
    er3 = (np-ns) * (1-f_early1) * fpp3
    er4 =     ns  *    f_early2  * fpp4
    er5 =     ns  * (1-f_early2) * fpp5

    tr1 = nt * fpp6
    #tr1 = np * f_tutorial * fpp6
    br1 = np * f_banquet * fpp7
    fr1 = 500
    bd1 = 3000
    bd2 = 2500

    sub2   = er2 + er3 + er4 + er5 + tr1 + br1 + fr1
    
    total2 = sub2 + bd1 + bd2
    return total2


# --- function: Expenses
#     (needs to be called second)

def costs(np):
    global sub2

    # conference services
    cvs1 = fee1 + fpp1 * np
    cvs2 = sub2 * ctax
    cvs3 = 2008.0              # hotel, lodging, per-diem
    cs1 = cvs1 + cvs2 + cvs3
    print("PJT-check",cs1)

    # meeting facilities
    #       projector A+B
    #       projector BoF
    #       4 power strips at $40+/day for 5 days * 1.22
    mf11  = 3019.50
    mf12  = 2244.80
    mf13  = nz * 5 * 40 * (1+htax)
    mf13  = 0.0                            # we now do our own power strips
    mf21  = 1788.82              # ivoa plenary
    mf22  = 3204.15              # ivoa breakout
    mf1   = 3019.50 + 2244.80 + 976.00 + (nb*75 + 150 + 30)
    mf1 = mf11 + mf12 + mf13 + (nb*75 + 150 + 30) + mf21 + mf22
    # ok
    
    # catering
    c1 = np * f_reception * (47+6) * (1+htax) + (150+150)*(1+htax)
    c2 = np * f_attend3   * 125    * 3     # 3 full days
    c3 = np * f_attend1   * 105    * 1     # 1 half day (105 could become 65)
    #c3 = np * f_attend1   *  65    * 1    # 1 half day (105 could become 65)
    c4 = np * f_banquet   * (61+12) * (1+htax) + (150+150)*(1+htax)
    cc1 = c1 + c2 + c3 + c4
    # ok
    
    # printing & signage
    ps1 = np * 5  + 600

    # invited speakers
    is1 = 12 * fpp2 + 5000     # also includes financial aid (5000)

    # additional expenses (the swags, the goodies)
    ae1 = np * 12

    total1 = cs1 + mf1 + cc1 + ps1 + is1 + ae1
    return total1

def profit(np, log=False):
    total2 = income(np)
    total1 = costs(np)
    delta = total2+cb1-total1
    if log:
        print("N=",np)
        print("Total costs  ",total1)
        print("Total income ",total2)
        print("Profit       ",delta)
    return delta

# --- print version
print("ADASS XXVIII budget sim version ",version)

# --- optional change of variables via the command line

import sys
for arg in sys.argv[1:]:
    print("Parsing",arg)
    exec(arg)


# -- print a few important variables"
print("   np = ", np)
print("   fpp2 = ",fpp2)
print("   cb1 = ",cb1)



# --- try a few budgets

print("N   Profit")
print("----------")
for n in [100, 200, 300, 400]:
    print(n,profit(n))


# -- show the benchmark/regression value (should be 27656.6)
# -- and the profit slope

print("=== Details === ")
p = profit(np,True)
d = profit(np)-profit(np-1)
print("Delta        ",d, "(dProfit/dN)")
print("SponsorMin   ",cb1-p)
