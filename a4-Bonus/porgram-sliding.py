import itertools
import os
from functools import reduce
from math import factorial
from operator import xor
from typing import Iterable, Tuple, TypeVar, Generator

from alive_progress import alive_bar

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{6}.txt'

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n

for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)

cardstack.sort()

T = TypeVar('T')
def sliding_window(iterable: Iterable[T], size: int) -> Generator[Tuple[T, ...], None, None]:
    for i in range(len(iterable) - size + 1):
        yield tuple(iterable[i:i+size])

# O(n)
for window in sliding_window(cardstack, k+1):
    res = reduce(xor, window)
    if res == 0:
        for x in list(window)+[res]:
            print(bin(x)[2:].zfill(m))
        break
