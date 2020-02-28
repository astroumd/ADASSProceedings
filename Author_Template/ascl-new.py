#!/usr/bin/env python
from  __future__ import print_function
from   operator  import truth, contains, eq, is_not, attrgetter, itemgetter, methodcaller, __add__, is_
from  functools  import partial, reduce
import sys, os, re, sys, collections, string

compose       = lambda *fns   : (lambda x: reduce(lambda acc, f: f(acc), reversed(fns), x))
identity      = lambda x      : x
const         = lambda c      : lambda *args, **kwargs: c
choice        = lambda p, t, f: (lambda x: t(x) if p(x) else f(x))  # branch
drain         = partial(collections.deque, maxlen=0)
Filter        = lambda pred: partial(filter, pred)
Map           = lambda fn: partial(map, fn)
Pam           = lambda *fns   : (lambda *x, **k: map(lambda f: f(*x, **k), fns))
Sorted        = lambda kf     : partial(sorted, key=kf)
GetN          = itemgetter
GetA          = attrgetter
Call          = methodcaller
Star          = lambda f      : lambda args, **kwargs: f(*args, **kwargs)
Reduce        = lambda r, i=None: partial(functools.reduce, r) if i is None else lambda l: reduce(r, l, i)
mk_obj        = lambda **kwargs: type('', (), kwargs)()

def DBG(x):
    print(x)
    return x

# Read the asclKeywords.txt, looking for lines matching "ascl:[0-9]{4}.[0-9]{3} CODE"
# get <ref> and <code> fields out of that and build a dict [<code>] => <ref>
get_codes = compose( dict, Map(Pam(Call('group', 'code'), Call('group', 'ref'))), Filter(truth),
                     Map(re.compile(r'^\s*(?P<ref>ascl:\d{4}\.\d{3})\s+(?P<code>\S+)\s*$').match),
                     open )

# take in: dict [CODE] => REF, yield dict [REF] => CODE
mk_sedoc = compose(dict, lambda vk: zip(*vk), Pam(Call('values'), Call('keys')))

# codes = map [CODE] => REF
# sedoc = map [REF]  => CODE
codes = get_codes('asclKeywords.txt')
sedoc = mk_sedoc(codes)

# strip leading/trailing punctuation from a word
punct   = re.escape(r".,/:;{}@()[]\\'\"!")
wclean  = compose(partial(re.sub, r"^["+punct+']*', ''), partial(re.sub, r'['+punct+r']*$', ''))

# read the tex file. a line is either an %\ooindex{CODE, REF} line or not
# if it is, parse out the CODE, if it isn't, check if any of the WORDs in the line
# might refer to an ASCL entry
isASCL     = re.compile(r'^%\\ooindex{\s*((?P<code>[^, \t\v\f\r]+)\s*,)?\s*(?P<ref>ascl:\d{4}\.\d{3})\s*}\s*$').match
get_groups = lambda grps: Pam(*map(partial(Call, 'group'), grps))
groups     = get_groups(['code', 'ref'])
words      = compose(Map(compose(wclean, str.strip)), str.split)

def reductor(state, line):
    mo = isASCL(line)
    if mo:
        # sometimes ppl put in "\%ooindex{ ascl:XXYY.xyz }"
        code, ref = groups(mo)
        if not code:
            code = sedoc.get( ref, None )
        # code still None?
        if code is None:
            raise RuntimeError("Unknown ASCL ref {0}".format(ref))
        # append code to "infile" set
        state.infile.add( code )
    else:
        # normal line of text
        state.candidates.update( filter(codes.__contains__, words(line)) )
    return state

fmt_code  = compose("%\\ooindex{{ {0[0]}, {0[1]} }}".format, Pam(identity, codes.__getitem__))
prt_codes = compose(drain, Map(compose(print, fmt_code)))

def handle_state(state):
    not_in_file = state.candidates - state.infile
    if not_in_file:
        print("{0} possible ooindex entries not in file yet".format(len(not_in_file)))
        prt_codes(not_in_file)
    if state.infile:
        print("{0} entries already found".format(len(state.infile)))
        prt_codes(state.infile)
    return state


main = compose(handle_state, Reduce(reductor, mk_obj(infile=set(), candidates=set())), open, DBG)
map(main, sys.argv[1:])
