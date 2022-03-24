from functools import reduce
from operator import xor
import os
from itertools import combinations, islice
from multiprocessing import Pool, freeze_support
from typing import Tuple
from numba import vectorize, jit

@vectorize(['b1(uint64[:])'], target='cuda')
def check(c):
    xor_ = 0
    for i in c:
        xor_ ^= i
    return not xor_

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{2}.txt'

splits = 500000

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n


for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)




iterable = combinations(range(len(cardstack))[:-2], k+1)

def chunks(iterable, size):
    """Generate adjacent chunks of data"""
    it = iter(iterable)
    return iter(lambda: tuple(islice(it, size)), ())

chnks = chunks(iterable, splits)

for c in iterable:
    if check(c):
        print(c)
        break

