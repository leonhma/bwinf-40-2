from collections import Counter
from itertools import permutations

from regex import findall


def is_unique_cl(challenge: str) -> bool:
    """
    Check if the challenge is unique by commutative law.

    `challenge` has to start with `+`

    """
    skyline = [int(challenge[i]) for i in range(1, len(challenge), 2)]
    summands = findall(r'[+-].*?(?=[+-]|$)', challenge)
    prev = None
    for s_comb in permutations(summands, len(summands)):
        print(f'{s_comb=}')
        if s_comb[0].startswith('-'): continue  # first summand cant be negative
        offset = 0
        for summand in s_comb:
            if not (Counter(int(summand[i]) for i in range(1, len(summand), 2))
                == Counter(skyline[offset:][:len(summand)//2])):  # may discriminate some divisions
                break
            offset += len(summand)//2
        else:
            print('else')
            if not prev:
                prev = ''.join(s_comb)
            else:
                print(f'{prev=}, {"".join(s_comb)}')
                return False
    return True

while True:
    challenge = input('challenge > ')
    print(is_unique_cl(challenge))


