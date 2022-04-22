from collections import Counter
from itertools import combinations

from regex import findall


def is_unique_cl(challenge: str) -> bool:
    """
    Check if the challenge is unique by commutative law.

    `challenge` has to start with `+`

    """
    skyline = [int(challenge[i]) for i in range(1, len(challenge), 2)]
    summands = findall(r'[+-].*?(?=[+-]|$)', challenge)

    for s_comb in combinations(summands, len(summands)):
        if s_comb[0].startswith('-'): continue  # first summand cant be negative
        offset = 0
        for summand in s_comb:
            if (Counter(int(summand[i]) for i in range(1, len(summand), 2))
                == Counter(skyline[offset:][:len(summand)//2])):  # may discriminate some divisions
                return False
            offset += len(summand)//2
    return True

while True:
    challenge = input('challenge > ')
    print(is_unique_cl(challenge))


