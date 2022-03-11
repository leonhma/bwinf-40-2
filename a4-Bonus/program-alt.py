import itertools
from operator import xor
import os
from functools import reduce
from math import factorial
from typing import Tuple

from alive_progress import alive_bar

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{1}.txt'

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n

for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = tuple(map(lambda x: bool(int(x)), line[:m+1]))


def xor_fast(x: Tuple[Tuple[int]]) -> int:
    for i in range(len(x[0])):
        if reduce(xor, [x[j][i] for j in range(len(x))]):
            return False
    return True


with alive_bar(int(factorial(n) / (factorial(n - (k+1)) * factorial(k+1)))) as bar:
    for comb in itertools.combinations(cardstack, k+1):
        bar()
        if xor_fast(comb):
            for x in comb:
                print(''.join(map(lambda x: str(1 if x else 0), x)))
            break
