#!/usr/bin/env python3
import sys
import unicodedata
import functools
import random
import collections

to_fullwidth = dict()
to_fullwidth.update((i, i + 0xfee0) for i in range(0x21, 0x7f))
to_fullwidth.update({0x20: 0x3000, 0x2D: 0x2212})  # space and minus

to_circles = dict()
to_circles.update(zip(range(ord('a'), ord('z')+1),range(0x249c, 0x24b5+1)))
to_circles.update(zip(range(ord('A'), ord('Z')+1),range(0x24b6, 0x24cf+1)))
to_circles.update(zip(range(ord('1'), ord('9')+1),range(0x2460, 0x2468+1)))
to_circles.update({ord('0'): 0x24ea})

to_fraktur_bold = dict()
to_fraktur_bold.update(zip(range(ord('a'), ord('z')+1),range(0x1d586, 0x1d59f+1)))
to_fraktur_bold.update(zip(range(ord('A'), ord('Z')+1),range(0x1d56c, 0x1d585+1)))

to_monospace = dict()
to_monospace.update(zip(range(ord('a'), ord('z')+1),range(0x1d68a, 0x1d6a4+1)))
to_monospace.update(zip(range(ord('A'), ord('Z')+1),range(0x1d670, 0x1d689+1)))
# todo:
# http://en.wikipedia.org/wiki/Mathematical_Alphanumeric_Symbols

combining = []
combining.extend(range(0x300, 0x36f+1)) # Combining Diacritical Marks
combining.extend(range(0x1dc0, 0x1de6+1)) # Combining Diacritical Marks Supplement
combining.extend(range(0x1dfc, 0x1dff+1)) 
#combining.extend(range(0x20d0, 0x20f0+1)) # Combining Diacritical Marks for Symbols
combining = [chr(x) for x in combining]

def make_combining(combine_chars):
    def _combine(line):
        out = []
        for char in line:
            out.append(char)
            if unicodedata.category(char).startswith(('L', 'N')):
                out.extend(combine_chars())
        return "".join(out)
    return _combine

fuckery = collections.OrderedDict([

    ('fullwidth', lambda line: line.translate(to_fullwidth)),
    ('circles', lambda line: line.translate(to_circles)),
    ('fraktur_bold', lambda line: line.translate(to_fraktur_bold)),
    ('monospace', lambda line: line.translate(to_monospace)),
    ('umlaut', make_combining(lambda:["\u0308"])),
    ('combine1', make_combining(lambda: random.sample(combining,1))),
    ('combine2', make_combining(lambda: random.sample(combining,2))),
    ('combiner', make_combining(lambda: random.sample(combining,random.randint(0,4)))),
    ('upper', lambda line: line.upper()),
    ('lower', lambda line: line.lower()),
])

if __name__ == '__main__':
    if sys.argv[1:]:
        fns = [fuckery[name] for name in sys.argv[1:]]
        while True:
            line = sys.stdin.readline()
            for fn in fns:
                line = fn(line)
            sys.stdout.write(line) 
            if not line:
                break
    else:
        print("\n".join(fuckery))
