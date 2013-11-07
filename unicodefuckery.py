#!/usr/bin/env python3
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


fuckery = {
    'fullwidth': lambda line: line.translate(to_fullwidth),
    'circles': lambda line: line.translate(to_circles),
    'fraktur_bold': lambda line: line.translate(to_fraktur_bold),
}

if __name__ == '__main__':
    import sys
    if sys.argv[1:]:
        fn = fuckery.get(sys.argv[1])
        while True:
            line = sys.stdin.readline()
            line = fn(line)
            sys.stdout.write(line) 
            if not line:
                break
    else:
        print("\n".join(fuckery))
