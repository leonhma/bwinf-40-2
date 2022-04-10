import os
from functools import reduce
from itertools import combinations
from math import factorial
from operator import xor
from typing import Iterable, Tuple

from alive_progress import alive_bar

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{4}.txt'


with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n


for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)

cardstack.sort()

def check(iterable_: Iterable[Tuple[int]]):
    # time complexity: O(n^(k-1)), space complexity: O(n)
    with alive_bar(int(factorial(n) / (factorial(n - (k-1)) * factorial(k-1)))) as bar:
        for ii in iterable_:  # ii: list of indices
            bar()
            goal = reduce(xor, [cardstack[i] for i in ii])
            l, r = ii[-1]+1, len(cardstack)-1
            while l < r:
                if cardstack[l] ^ cardstack[r] > goal:
                    l += 1
                elif cardstack[l] ^ cardstack[r] < goal:
                    r -= 1
                else:
                    for x in [cardstack[i] for i in list(ii)+[l, r]]:
                        print(bin(x)[2:].zfill(m))
                    break
            

ii = combinations(range(len(cardstack))[:-2], k-1)
check(ii)
