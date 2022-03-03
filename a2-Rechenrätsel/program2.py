from random import choice, randint
import re
from typing import List


def is_sum_of_list_items(i: int, lst: List[int]) -> bool:
    """
    Check if the given number is the sum of multiple items in the given list.
    """
    if i in lst:
        return True
    for j in lst:
        if is_sum_of_list_items(i-j, lst):
            return True
    return False
    

def is_valid_challenge(challenge):
    if eval(challenge) < 0 or re.match(r'[*/]1', challenge):
        print('result under 0 or division/multiplication by 1')
        return False

    # ---- check for cancelling summands ----
    pluses, minuses = [], []
    summands = re.findall(r'[+-].*?(?=[+-]|$)', challenge)

    for s in summands:
        res = eval(s[1:])
        print(f'{s=} {res=}')
        if s[0] == '+':
            pluses.add(res)
        else:  # s[0] == '-'
            minuses.add(res)

    # if adding minuses can make up a value in plus, adding pluses can make up a value in minus
    for plus in pluses:
        # some recursive shit

    

length=20

challenge = '+'+''.join([str(randint(1, 10))+choice(['+', '-', '*', '/']) for _ in range(length)])[:-1]

while i := is_valid_challenge(challenge):
    challenge = '+'+''.join([str(randint(1, 10))+choice(['+', '-', '*', '/']) for _ in range(length)])[:-1]

print(is_valid_challenge('+1-1'))

