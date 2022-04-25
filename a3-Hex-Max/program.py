from os.path import dirname, join
from typing import Generator, List, Tuple

from segment import Segment

costmap: List[List[Tuple[int, int]]] = []


# create lookup O(1)
for x, from_ in enumerate('0123456789ABCDEF'):
    costmap.append([0]*16)
    for y, to in enumerate('FEDCBA9876543210'):
        costmap[x][y] = Segment(from_).get_takes_gives(Segment(to))


def get_max_swappable(segments: List[Segment], m: int) -> str:
    if len(segments) > 500:
        print('warning: this might take a while...')
    iterator = [0]*len(segments)
    result: List[str] = []  # list of char

    def step(index: int):
        for i in range(index, -1, -1):
            carry = False
            if iterator[i] == 15:
                carry = True
            iterator[i] = (iterator[i]+1) % 16
            if not carry:
                break

    while True:
        current_takes, current_gives = 0, 0
        result = []
        for i in range(len(segments)):
            takes, gives = costmap[int(segments[i].char, base=16)][iterator[i]]
            if (takes + current_takes > m) or (gives + current_gives > m):
                step(i)
                break
            current_takes += takes
            current_gives += gives
            result.append(hex(15-iterator[i])[2].upper())
            if i == len(segments)-1:
                if current_takes == current_gives:
                    return ''.join(result)
                else:
                    step(i)


def _animate(from_: str, to: str) -> Generator[List[Segment], None, None]:
    from_ = [Segment(char) for char in from_]
    to = [Segment(char) for char in to]
    while from_ != to:
        for i in range(7*len(to)):
            seg, i = i//7, i % 7
            if from_[seg].panels[i] and not to[seg].panels[i]:
                from_[seg].panels[i] = 0
                from_[seg].__dict__.pop('char', None)
                break
        else:
            raise ValueError('Not the same number of sticks!')
        for i in range(7*len(to)):
            seg, i = i//7, i % 7
            if not from_[seg].panels[i] and to[seg].panels[i]:
                from_[seg].panels[i] = 1
                from_[seg].__dict__.pop('char', None)
                break
        else:
            raise ValueError('Not the same number of sticks!')
        yield from_
    return


def _print_asciiart(display: List[Segment]):
    out = [[], [], []]
    for seg in display:
        asciiart = seg.ascii_art()
        for i in range(3):
            out[i] += asciiart[i*3:i*3+3]
    for line in out:
        print(''.join(line))


while True:
    choice = int(input("Bitte die Nummer des Beispiels eingeben [0-5]: "))
    with open(join(dirname(__file__), f'beispieldaten/hexmax{choice}.txt')) as f:
        display = [Segment(char) for char in f.readline().strip()]
        m = int(f.readline().strip())

    print(get_max_swappable(display, m))
