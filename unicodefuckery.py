#!/usr/bin/env python3
import sys
import unicodedata
import functools
import random
import collections

# http://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms
to_fullwidth = dict()
to_fullwidth.update((i, i + 0xfee0) for i in range(0x21, 0x7f))
to_fullwidth.update({0x20: 0x3000, 0x2D: 0x2212})  # space and minus

# http://en.wikipedia.org/wiki/Enclosed_Alphanumerics

to_circles = dict()
to_circles.update(zip(range(ord('a'), ord('z')+1),range(0x249c, 0x24b5+1)))
to_circles.update(zip(range(ord('A'), ord('Z')+1),range(0x24b6, 0x24cf+1)))
to_circles.update(zip(range(ord('1'), ord('9')+1),range(0x2460, 0x2468+1)))
to_circles.update({ord('0'): 0x24ea})

# http://en.wikipedia.org/wiki/Mathematical_Alphanumeric_Symbols

to_bold = dict() #
to_bold.update(zip(range(ord('a'), ord('z')+1),range(0x1d41a, 0x1d433+1)))
to_bold.update(zip(range(ord('A'), ord('Z')+1),range(0x1d400, 0x1d419+1)))

to_italic = dict() #
to_italic.update(zip(range(ord('a'), ord('z')+1),range(0x1d44e, 0x1d467+1)))
to_italic.update(zip(range(ord('A'), ord('Z')+1),range(0x1d434, 0x1d44d+1)))
to_italic[ord('h')] = 0x210e

to_bold_italic = dict() # 
to_bold_italic.update(zip(range(ord('a'), ord('z')+1),range(0x1d482, 0x1d49b+1)))
to_bold_italic.update(zip(range(ord('A'), ord('Z')+1),range(0x1d468, 0x1d481+1)))

to_script = dict() #
to_script.update(zip(range(ord('a'), ord('z')+1),range(0x1d4b6, 0x1d4cf+1)))
to_script.update(zip(range(ord('A'), ord('Z')+1),range(0x1d49c, 0x1d4b5+1)))
to_script[ord('B')] = 0x212c
to_script[ord('E')] = 0x2130
to_script[ord('F')] = 0x2131
to_script[ord('H')] = 0x210b
to_script[ord('I')] = 0x2110
to_script[ord('L')] = 0x2112
to_script[ord('M')] = 0x2133
to_script[ord('R')] = 0x211b
to_script[ord('e')] = 0x212f
to_script[ord('g')] = 0x210a
to_script[ord('o')] = 0x2134

to_script_bold = dict() # 
to_script_bold.update(zip(range(ord('a'), ord('z')+1),range(0x1d4ea, 0x1d503+1)))
to_script_bold.update(zip(range(ord('A'), ord('Z')+1),range(0x1d4d0, 0x1d4e9+1)))

# todo + missing
to_fraktur = dict()
to_fraktur.update(zip(range(ord('a'), ord('z')+1),range(0x1d51e, 0x1d537+1)))
to_fraktur.update(zip(range(ord('A'), ord('Z')+1),range(0x1d504, 0x1d51d+1)))
to_fraktur[ord('C')] = 0x212d
to_fraktur[ord('H')] = 0x210c
to_fraktur[ord('I')] = 0x2111
to_fraktur[ord('R')] = 0x211c
to_fraktur[ord('Z')] = 0x2128

# todo + missing
to_doublestruck = dict()
to_doublestruck.update(zip(range(ord('a'), ord('z')+1),range(0x1d552, 0x1d56b+1)))
to_doublestruck.update(zip(range(ord('A'), ord('Z')+1),range(0x1d538, 0x1d551+1)))
to_doublestruck[ord('C')] = 0x2102
to_doublestruck[ord('H')] = 0x210d
to_doublestruck[ord('N')] = 0x2115
to_doublestruck[ord('P')] = 0x2119
to_doublestruck[ord('Q')] = 0x211a
to_doublestruck[ord('R')] = 0x211d
to_doublestruck[ord('Z')] = 0x2124

to_fraktur_bold = dict()
to_fraktur_bold.update(zip(range(ord('a'), ord('z')+1),range(0x1d586, 0x1d59f+1)))
to_fraktur_bold.update(zip(range(ord('A'), ord('Z')+1),range(0x1d56c, 0x1d585+1)))

to_sans = dict()
to_sans.update(zip(range(ord('a'), ord('z')+1),range(0x1d5ba, 0x1d5d3+1)))
to_sans.update(zip(range(ord('A'), ord('Z')+1),range(0x1d5a0, 0x1d5b9+1)))

to_sans_bold = dict()
to_sans_bold.update(zip(range(ord('a'), ord('z')+1),range(0x1d5ee, 0x1d607+1)))
to_sans_bold.update(zip(range(ord('A'), ord('Z')+1),range(0x1d5d4, 0x1d5ed+1)))

to_sans_italic = dict()
to_sans_italic.update(zip(range(ord('a'), ord('z')+1),range(0x1d622, 0x1d63b+1)))
to_sans_italic.update(zip(range(ord('A'), ord('Z')+1),range(0x1d608, 0x1d621+1)))

to_sans_bold_italic = dict()
to_sans_bold_italic.update(zip(range(ord('a'), ord('z')+1),range(0x1d656, 0x1d66f+1)))
to_sans_bold_italic.update(zip(range(ord('A'), ord('Z')+1),range(0x1d63c, 0x1d655+1)))

to_monospace = dict()
to_monospace.update(zip(range(ord('a'), ord('z')+1),range(0x1d68a, 0x1d6a4+1)))
to_monospace.update(zip(range(ord('A'), ord('Z')+1),range(0x1d670, 0x1d689+1)))

# http://en.wikipedia.org/wiki/Combining_character
combining = []
combining.extend(range(0x300, 0x36f+1)) # Combining Diacritical Marks
combining.extend(range(0x1dc0, 0x1de6+1)) # Combining Diacritical Marks Supplement
combining.extend(range(0x1dfc, 0x1dff+1)) 
combining.extend(range(0x20d0, 0x20f0+1)) # Combining Diacritical Marks for Symbols
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
    ('bold', lambda line: line.translate(to_bold)),
    ('italic', lambda line: line.translate(to_italic)),
    ('bold_italic', lambda line: line.translate(to_bold_italic)),
    ('script', lambda line: line.translate(to_script)),
    ('script_bold', lambda line: line.translate(to_script_bold)),
    ('fraktur', lambda line: line.translate(to_fraktur)),
    ('doublestruck', lambda line: line.translate(to_doublestruck)),
    ('fraktur_bold', lambda line: line.translate(to_fraktur_bold)),
    ('sans', lambda line: line.translate(to_sans)),
    ('sans_bold', lambda line: line.translate(to_sans_bold)),
    ('sans_italic', lambda line: line.translate(to_sans_italic)),
    ('sans_bold_italic', lambda line: line.translate(to_sans_bold_italic)),
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
        print("usage: {} <filter> <filter> <filter>".format(sys.argv[0]))
        print("filters:", ", ".join(fuckery))
