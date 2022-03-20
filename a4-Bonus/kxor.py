import itertools
import os
from functools import reduce
from math import factorial
from operator import xor
from typing import List

from alive_progress import alive_bar

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{1}.txt'

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n

for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)


def kxor(arr: List[int], k: int) -> List[int]:
    current = [0]

    def recurse(arr: List[int], i: int) -> List[int]:
        
        if k > 2:
            # recurse
        else:
            l, r = current[-1], k+1
