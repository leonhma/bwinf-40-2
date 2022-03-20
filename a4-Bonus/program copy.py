from collections import defaultdict
import itertools
import os
from functools import reduce
from math import factorial
from operator import xor


from alive_progress import alive_bar

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{6}.txt'

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n

for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)

crosssums = defaultdict(list)
cardstack.sort()
for item in cardstack:
    crosssum = sum(map(int, bin(item)[2:]))
    crosssums[crosssum].append(item)

crossum_solutions = []
print('Finding possible crosssum combinations...')
print(crosssums.keys())
print(list(itertools.combinations_with_replacement(crosssums.keys(), k)))
# O(n^k)
with alive_bar(int(factorial(len(crosssums)+k-1) / factorial(k) / factorial(len(crosssums)-1))) as bar:
    for comb in itertools.combinations_with_replacement(sorted(crosssums.keys()), k):
        bar()
        print(comb)

print(crossum_solutions)
