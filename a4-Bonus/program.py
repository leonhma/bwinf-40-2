from functools import reduce
from math import factorial
from alive_progress import alive_it
import itertools
import os


path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{5}.txt'

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n

for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)

goal = 2 ^ m-1
for comb in alive_it(itertools.combinations(cardstack, k),
                     total=int(factorial(n) / (factorial(n - k) * factorial(k)))):
    if sum(comb) % goal == 0:
        print(f'{comb=}')
        break
