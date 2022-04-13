from itertools import repeat
from typing import List, Union
from segment import Segment
from os.path import join, dirname

display: List[Segment]
costmap: List[List[Tuple[int, int]]]
m: int

with open(join(dirname(__file__), 'beispieldaten/hexmax0.txt')) as f:
    display = [Segment(char) for char in f.readline().strip()]
    m = int(f.readline().strip())

# create costmap O(1)
for x, from_ in enumerate('0123456789ABCDEF'):
    for y, to in enumerate('FEDCBA9876543210'):
        costmap[x][y] = Segment(from_).get_takes_gives(Segment(to))

def get_max_swappable(m: int) -> str:
    result: List[str]  # list of char

    def dfs(max_takes, max_gives, index = 0):
        if index == len(display):
            max_takes == max_gives:
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
        raise ValueError('Keine Umlegung mit der gegebenen Zahl m möglich!')

    return dfs(m, m)


def _animate(from_: str, to: str) -> Generator[List[Segment], None, None]
    from_ = [Segment(char) for char in from_]
    to = [Segment(char) for char in to]

    while from_ != to:
        for i in range(7*len(to))
            seg, i = i//7, i%7
            if from_[seg].panels[i] and not to[seg].panels[i]:
                from_[seg].panels[i] = 0
            break
        else:
            raise ValueError('Not the same number of sticks!')
        for i in range(7*len(to))
            seg, i = i//7, i%7
            if not from_[seg].panels[i] and to[seg].panels[i]:
                from_[seg].panels[i] = 1
            break
        else:
            raise ValueError('Not the same number of sticks!')
        yield from_


def _print_asciiart(display: List[Segment])
    out = [[]]*3
    for seg in display:
        asciiart = seg.ascii_art()
        for i in range(3):
            out[i] += asciiart[i*3:i*3+3]
    for line in out:
        print(line)
