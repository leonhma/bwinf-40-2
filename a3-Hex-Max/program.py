from os.path import join, dirname
from typing import List, Union, Tuple, Generator

from segment import Segment


costmap: List[List[Tuple[int, int]]] = []


# create lookup O(1)
for x, from_ in enumerate('0123456789ABCDEF'):
    costmap.append([0]*16)
    for y, to in enumerate('FEDCBA9876543210'):
        costmap[x][y] = Segment(from_).get_takes_gives(Segment(to))

def get_max_swappable(segments: List[Segment], m: int) -> str:
    result: List[str] = []  # list of char

    def dfs(max_takes, max_gives, index = 0):
        if index == len(segments):
            if max_takes == max_gives:
                return ''.join(result)  # return result if at the end of string and number of swaps match
            return  # return None if number of swaps dont match (one match is guaranteed)
        for hex_, (takes, gives) in zip('FEDCBA9876543210', costmap[int(segments[index].char, base=16)]):
            if takes > max_takes or gives > max_gives:  # skip possibility if either is exceeded
                continue
            result.append(hex_)
            res = dfs(max_takes-takes, max_gives-gives, index+1)
            if res:  # propagate match upwards
                return res
            del result[-1]

    return dfs(m, m)


def _animate(from_: str, to: str) -> Generator[List[Segment], None, None]:
    from_ = [Segment(char) for char in from_]
    to = [Segment(char) for char in to]
    while from_ != to:
        for i in range(7*len(to)):
            seg, i = i//7, i%7
            if from_[seg].panels[i] and not to[seg].panels[i]:
                from_[seg].panels[i] = 0
                from_[seg].__dict__.pop('char', None)
                break
        else:
            raise ValueError('Not the same number of sticks!')
        for i in range(7*len(to)):
            seg, i = i//7, i%7
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
    try:
        choice = int(input("Bitte die Nummer des Beispiels eingeben [0-5]: "))
        with open(join(dirname(__file__), f'beispieldaten/hexmax{choice}.txt')) as f:
            display = [Segment(char) for char in f.readline().strip()]
            m = int(f.readline().strip())

        print(get_max_swappable(display, m))
    except Exception as e:
        print(e)
