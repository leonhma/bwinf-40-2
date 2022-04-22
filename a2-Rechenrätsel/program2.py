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
        if s_comb[0].startswith('-'): continue  # first summand cant be negative
        offset = 0
        for summand in s_comb:
            a_cnt = Counter(int(summand[i]) for i in range(1, len(summand), 2))
            b_cnt = Counter(skyline[offset:][:len(summand)//2])
            if a_cnt != b_cnt:  # may discriminate some divisions
                break
            offset += len(summand)//2
        else:
            if not prev:
                prev = ''.join(s_comb)
            else:
                print(f'{prev=}, {"".join(s_comb)}')
                return False
    return True

if __name__ == '__main__':
    while True:
        challenge = input('challenge > ')
        print(is_unique_cl(challenge))


