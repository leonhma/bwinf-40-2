import itertools
import os
from functools import reduce
from math import factorial
from operator import xor

from alive_progress import alive_bar

path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/stapel{1}.txt'

with open(path, 'r') as f:
    lines = f.read().split('\n')

n, k, m = map(int, lines[0].split())
cardstack = [0] * n

for i, line in enumerate(lines[1:][:n]):
    cardstack[i] = int(line[:m+1], 2)

# O(n*nlogn*k)
with alive_bar(len(cardstack)) as bar:
    for xor_tmp in cardstack:
        print(f'starting with {bin(xor_tmp)[2:].zfill(m)}')
        tmp_cardstack = cardstack.copy()
        tmp_cardstack.remove(xor_tmp)
        out = [xor_tmp]
        bar()
        for _ in range(k):
            print('sorted')
            next_ = min(tmp_cardstack, key=lambda x: x ^ xor_tmp)
            tmp_cardstack.remove(next_)
            print(f'new temp      {bin(xor_tmp)[2:].zfill(m)}')
            xor_tmp ^= next_
            out.append(next_)
        if xor_tmp == 0:
            for x in out:
                print(cardstack.index(x), bin(x)[2:].zfill(m))
            break
