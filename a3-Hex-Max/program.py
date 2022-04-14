import numpy as np
from itertools import repeat
from typing import List, Union, Tuple, Generator
from segment import Segment
from os.path import join, dirname

display: List[Segment]
costmap: List[List[Tuple[int, int]]] = []
m: int

choice = int(input("Welches Beispiel soll geöffnet werden?"))
with open(join(dirname(__file__), f'beispieldaten/hexmax{choice}.txt')) as f:
    display = [Segment(char) for char in f.readline().strip()]
    m = int(f.readline().strip())

# create costmap O(1)
for x, from_ in enumerate('0123456789ABCDEF'):
    costmap.append([0]*16)
    for y, to in enumerate('FEDCBA9876543210'):
        costmap[x][y] = Segment(from_).get_takes_gives(Segment(to))

def get_max_swappable(m: int) -> str:
    result: List[str] = []  # list of char

    def dfs(max_takes, max_gives, index = 0):
        if index == len(display):
            if max_takes == max_gives:
                return ''.join(result)  # return result if at the end of string and number of swaps match
            return  # return None if number of swaps dont match (only applies within inner dfs)
        for hex, (takes, gives) in zip('FEDCBA9876543210', costmap[int(display[index].char, base=16)]):
            if takes > max_takes or gives > max_gives:  # skip possibility if either is exceeded
                continue
            result.append(hex)
            res = dfs(max_takes-takes, max_gives-gives, index+1)
            if res:  # propagate result upwards
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


start = ''.join(seg.char for seg in display)
res = get_max_swappable(m)

if choice < 3:
	print()
	_print_asciiart(display)

	for step in _animate(start, res):
		print()
		_print_asciiart(step)

print(res)
