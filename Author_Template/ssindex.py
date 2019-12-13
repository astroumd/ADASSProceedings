#!/usr/bin/env python
from  __future__ import (print_function,division,absolute_import)
from   operator  import truth, contains, eq, is_not, attrgetter, itemgetter, methodcaller, __add__, is_
import sys, os, re, sys, shlex, argparse, subprocess, collections, functools, string
import AdassIndex, AdassConfig

compose       = lambda *fns   : (lambda x: reduce(lambda acc, f: f(acc), reversed(fns), x))
identity      = lambda x      : x
const         = lambda c      : lambda *args, **kwargs: c
choice        = lambda p, t, f: (lambda x: t(x) if p(x) else f(x))  # branch
drain         = functools.partial(collections.deque, maxlen=0)
Filter        = lambda pred: functools.partial(filter, pred)
Map           = lambda fn: functools.partial(map, fn)
Pam           = lambda *fns   : (lambda *x, **k: map(lambda f: f(*x, **k), fns))
Sorted        = lambda kf     : functools.partial(sorted, key=kf)
GetN          = itemgetter
GetA          = attrgetter
Call          = methodcaller
Star          = lambda f      : lambda args, **kwargs: f(*args, **kwargs)
Reduce        = lambda r: functools.partial(functools.reduce, r)
RUN           = subprocess.Popen
SHLEX         = lambda arg: shlex.split(arg) if isinstance(arg, type("")) else arg
STDOUT        = lambda cmd: RUN(SHLEX(cmd), stdout=subprocess.PIPE).communicate(None)[0]
LINES         = lambda cmd: STDOUT(cmd).split('\n')

def DBG(x):
    print(x)
    return x

# transform an ssentry ("topic!sub-topic!sub-topic") into a tuple:
#   (original_entry, individual-lowercased-words)
# The search/match can be done on the individual lower cased words, the printed
# result (for the %ssindex{...}) will use the original entry
xform_entry = compose(tuple, Reduce(__add__), Map(str.split), Call('split', '!'), str.lower)
# we don't care about master/new index, so read both and collate both lists into one set
Details = list()
Entries = compose(set, Map(lambda e: (e, xform_entry(e))), Reduce(__add__), Map(AdassIndex.ReadIndexList))(
                  [AdassConfig.MainSubjectIndexFile(Details), AdassConfig.NewSubjectIndexFile()] )
if not Entries:
    drain(map(print, Details))
    sys.exit(-1)
print("Read ",len(Entries)," entries")

# Run the equivalent of "../pmake words"
# detex <file> | grep -o -E '\w+' | tr '[A-Z]' '[a-z]' | sort | uniq -c | sort -n
get_words = compose(Reduce(set.union), Map(compose(set, functools.partial(re.findall, r'\w+'), str.lower)),
                    LINES, "detex {0}".format)

# Also read words that are never to be indexed and the single characters/digits 
never        = functools.reduce(set.union, [get_words('notKeywords.txt'),
                                            set(string.ascii_letters),
                                            set(string.digits)])
# get_keywords extracts all words but removes those that we'll never consider as keywords
get_keywords = compose(Call('difference', never), get_words)
# get_ssindex filters the list of ssentries for those containing the keyword
get_ssindex  = lambda kw: filter(compose(Call('__contains__', kw), GetN(1)), Entries)
#def get_ssindex(kw):
#    m = filter(compose(Call('__contains__', kw), GetN(1)), Entries)
#    if kw == "calibration":
#        print("keyword ",kw," yields ",len(m)," matches")
#        print(map(compose("  {0}\n".format, GetN(0)), m))
#    return m

# the main program extracts all key words from the .tex file, looks up ssentries for those
# uniquefies them and then print the appropriate ssindex
main         = compose(Map(compose(print, "%\\ssindex{{{0}}}".format, GetN(0))), sorted, Reduce(set.union),
                      Map(compose(set, get_ssindex)), get_keywords, DBG)
#main         = compose(print, "total # matching entries = {0}".format, Reduce(__add__),
#                       DBG, Map(compose(len, set, get_ssindex)), get_keywords)
drain(map(main, sys.argv[1:]))
