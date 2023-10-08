#!/usr/bin/env python3
from  __future__ import (print_function,division,absolute_import)
from   operator  import truth, contains, eq, is_not, attrgetter, itemgetter, methodcaller, __add__, is_, __truediv__
import sys, os, re, sys, shlex, argparse, subprocess, collections, functools, string, itertools
import AdassIndex, AdassConfig

compose       = lambda *fns   : (lambda x: reduce(lambda acc, f: f(acc), reversed(fns), x))
identity      = lambda x      : x
const         = lambda c      : lambda *args, **kwargs: c
choice        = lambda p, t, f: (lambda x: t(x) if p(x) else f(x))  # branch
drain         = functools.partial(collections.deque, maxlen=0)
Filter        = lambda pred: functools.partial(filter, pred)
Map           = lambda fn: functools.partial(map, fn)
Pam           = lambda *fns   : (lambda *x, **k: tuple(map(lambda f: f(*x, **k), fns)))
Sorted        = lambda kf,**kw: functools.partial(sorted, key=kf, **kw)
GroupBy       = lambda kf     : (lambda l: itertools.groupby(l, kf))
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

def DBG2(pfx=None):
    pfx = '' if pfx is None else pfx
    def do_it(x):
        print(pfx, x)
        return x
    return do_it


# new approach:
#  ssentry = "topic!sub-topic!subsub-topic"
# add scoring:
#             +1   ! +10     | +100  (! +1000 etc)
# if a word matches in that part of the ssentry, i.e. more specific matches
# are valued (much) higher than arbitrary matches.
# 
# How to handle multiple matches in the same ssindex? Say: one word matches
# in susub-topic of a particular ssindex, and another word in the text matches
# in the sub-topic of the same ssindex. Just sum up those values for the whole ssindex?

# transform an ssentry ("topic!sub-topic!sub-topic") into a tuple:
# ie the words in decreasing relative relevance 
values      = [10000, 1000, 100, 10, 1]
# depending on the length of wordlists:
#  (1) topic
#  (2) topic!sub-topic
#  (3) topic!sub-topic!subsub-topic
# give the whole ssindex a larger value such that more specific designators
# weigh more than a single topic entry.
# Give the words in the categories lower values if there are more words
# in each "part" (e.g. "archives!data centres!ESAC Science Data Centre" 
#   has 1, 2, and 4 words in the different parts) because each word in each part counts
# as an extra match for that part (in the end all scores for the ssindex are summed)
def revalue(wordlists):
    rv = list()
    n  = len(wordlists)
    for (wl, val) in zip(wordlists, values):
       rv.append( (n*val) / len(wl) )
    return tuple(rv)

Entry = collections.namedtuple('Entry', ['ssindex', 'wordlists', 'values', 'significant', 'all'])

rx_noparens = re.compile(r'^[^(].*[^)]$').match

# this function takes an entry of the form
# transform an ssentry ("topic!sub-topic!sub-topic") into a namedtuple with
# appropriately named fields
def xform_entry(entry):
    parts     = entry.lower().split('!')
    wordlists = tuple(map(compose(set, str.split), parts))
    # the last part is the most significant (most specific)
    # create a set with the non-parenthesized words such that
    # the code can test if all the words in that part are found in the
    # tex file
    signif    = set(filter(rx_noparens, wordlists[-1]))
    all_      = set(reduce(__add__, Map(Filter(rx_noparens))(wordlists)))
    return Entry(entry, wordlists, revalue(wordlists), signif, all_)


# we don't care about master/new index, so read both and collate both lists into one set
Details = list()
Entries = compose(Map(xform_entry), Reduce(__add__), Map(AdassIndex.ReadIndexList))(
                  [AdassConfig.MainSubjectIndexFile(Details), AdassConfig.NewSubjectIndexFile()] )
if not Entries:
    drain(map(print, Details))
    sys.exit(-1)
print("Read ",len(Entries)," entries")

EntriesMap = collections.defaultdict(list)

for entry in Entries:
    for kw in reduce(set.union, entry.wordlists):
        EntriesMap[ kw ].append( entry )

ssindexMap = dict()
for entry in Entries:
    ssindexMap[ entry.ssindex ] = entry

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

# filter (True, value) entries and sum up all the value(s)
get_score    = compose(sum, Map(GetN(1)), Filter(GetN(0)))

# get_ssindex now returns [(original-entry, score), ....]
def get_ssindex(kw):
    result = list()
    findkw = Map(Call('__contains__', kw))
    for (ssindex, wordlists, vals, parts) in Entries:
        score = get_score(zip(findkw(wordlists), vals))
        if score > 0:
            result.append( (ssindex, score) )
    return result


# helper functions for collapsing a list of [(ssindex, score), (ssindex, score), ....]
# into a list where all scores for the same ssindex are summed
sum_values = compose(sum, Map(GetN(1)))
post_proc  = compose(Map(lambda e: (e[0], sum_values(e[1]))), GroupBy(GetN(0)), Sorted(GetN(0)))

def score_ssindex(keywords):
    keywords = set(keywords)
    rv       = list()
    for kw in keywords:
        findkw = Map(Call('__contains__', kw))
        # look up all ssindex entries that match
        for entry in EntriesMap[kw]:
            score = get_score(zip(map(Call('__contains__',kw), entry.wordlists), entry.values))
            # extra bonus if all keywords of the entry exist in the text
            if entry.all <= keywords:
                score += 10000
            rv.append( (entry.ssindex, score) )
    # now collect the results by ssindex, summing up the scores
    rv = post_proc( rv )
    # now we filter the list: only keep entries whose singificant
    # is a subset of the keywords in the file
    def filter_f(candidate):
        # candidate = (ssindex, score)
        return ssindexMap[candidate[0]].significant <= keywords
    return filter(filter_f, rv)

#Map(compose(print, "ssindex {0[0]} score {0[1]}".format)), 
#main         = compose(Map(compose(print, "%\\ssindex{{{0[0]}}}".format)),
#main         = compose(Map(compose(print, "%\\ssindex{{{0[0]}}}\t\t% score={0[1]}".format)),
#                       Sorted(GetN(1), reverse=True), post_proc,
#                       Reduce(__add__), Map(get_ssindex), get_keywords, DBG)
main         = compose(Map(compose(print, "%\\ssindex{{{0[0]}}}\t\t% score={0[1]}".format)),
                       Sorted(GetN(1), reverse=True), score_ssindex, get_keywords, DBG)

drain(map(main, sys.argv[1:]))
