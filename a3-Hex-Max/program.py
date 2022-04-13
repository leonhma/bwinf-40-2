from itertools import repeat
from typing import List, Union
from segment import Segment
from os.path import join, dirname
from utils import ilist

display: List[Segment]
costmap: List[List[Tuple[int, int]]]
takes: int
puts: int

with open(join(dirname(__file__), 'beispieldaten/hexmax0.txt')) as f:
    display = [Segment(char) for char in f.readline().strip()]
    takes, puts = repeat(int(f.readline().strip()), 2)

# create costmap O(1)
for x, from_ in enumerate('0123456789ABCDEF'):
    for y, to in enumerate('FEDCBA9876543210'):
        costmap[x][y] = Segment(from_).get_takes_gives(Segment(to))

def get_max_swappable(m: int) -> str:
    result: List[str]  # list of char

    def dfs(max_takes: int, max_gives: int, index: int = 0) -> Union[None, str]:
        if index == len(display):
            max_takes == max_gives:
                return ''.join(result)  # return result if at the end of string and number of swaps match
            return  # return None if number of swaps dont match (only applies within inner dfs)
        for hex, (takes, gives) in zip('FEDCBA9876543210', costmap[int(display[index].char, base=16)]):
            if takes > max_takes or gives > max_gives:  # skip possibility if swaps exceeded
                continue
            result.append(hex)
            dfs(max_takes-takes, max_gives-gives, index+1)
            del result[-1]
        raise ValueError('something went horribly wrong')

    return dfs(m, m)
