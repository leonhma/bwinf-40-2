import itertools
import os
from functools import reduce
from math import factorial
from operator import xor

from alive_progress import alive_bar

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{2}.txt'

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n

for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)

# O(n^k)
with alive_bar(int(factorial(n) / (factorial(n - (k)) * factorial(k)))) as bar:
    for comb in itertools.combinations(cardstack, k):
        bar()
        res = reduce(xor, comb)
        if res in cardstack:
            for x in list(comb)+[res]:
                print(bin(x)[2:].zfill(m))
            break
