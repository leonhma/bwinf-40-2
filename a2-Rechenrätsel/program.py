import random
import re
import timeit
from itertools import combinations
from typing import List

from alive_progress import alive_it

from get_permutations_cl import get_permutations_cl

NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
OPERATORS = ['+', '-', '*', '/']


def gen(length: int) -> str:
    """
    Generate a random challenge.

    Parameters
    ----------
    length : int
        Length of the challenge.

    Returns
    -------
    str
        The generated challenge.
    """
    # generate a random challenge
    # start with a plus sign and a number
    challenge = f'+{random.randint(1, 9)}'
    for _ in range(length):
        # generate operator
        op = random.choice(OPERATORS)
        # generate number
        if op == '/':
            last = ''
            for i in range(len(challenge)-1, -1, -1):
                if challenge[i] in ['+', '-']:
                    break
                last = challenge[i]+last
            last = eval(last)
            nums = [
                number
                for number in NUMBERS
                if (last >= number > 1) and (last % number == 0)
            ]
        elif op == '*':
            nums = NUMBERS.copy()
            nums.remove(1)
        else:
            nums = NUMBERS
        # append to challenge
        challenge += op + str(random.choice(nums))
    # check if the result is positive
    if not is_valid_challenge(challenge):
        print(f'{challenge=} is invalid')
        return gen(length)
    return challenge+'='+str(int(eval(challenge)))


def get_skyline(challenge: str) -> List[int]:
    """
    Get the skyline of the challenge. (skyline means the single digits of the challenge in order of appearance)
    
    Parameters
    ----------
    challenge : str
        The challenge to get the skyline of.
    
    Returns
    -------
    List[int]
        The skyline of the challenge.

    """
    ints = re.findall(r'\d+', challenge)
    return [int(i) for i in ints]


def is_valid_challenge(challenge: str) -> bool:
    """
    Check if the challenge is valid.

    Parameters
    ----------
    challenge : str
        The challenge to check.

    Returns
    -------
    bool
        `True` if the challenge is valid, `False` otherwise.

    """
    # normalize input
    challenge = challenge.replace(' ', '')
    if challenge[0] != '+':
        challenge = '+' + challenge
    # check if result is positive
    if eval(challenge) < 0:
        print(f'result is negative: {challenge=}')
        return False
    else:
        print('result is not negative')
    print('---')
    # check if summands cancel each other out
    summands = re.findall(r'[+-][^+-]+?(?=[+-]|$)', challenge)
    # remove last summand because it has already been checked and first, because it's sign cant be changed (always positive)
    for summand in summands[1:-1]:
        # check if -summand can be made by combining other arbitrary summands
        to_check = summands.copy()
        to_check.remove(summand)  # dont check against current summand
        for i in range(1, len(to_check)+1):
            for summand_permutation in combinations(to_check, i):
                if eval(summand) == -(eval(''.join(summand_permutation))):
                    print(
                        f'{summand=} can be cancelled out by {summand_permutation=}')
                    return False
    print(f'{challenge} has no summands that cancel out')
    print('---')
    # check if there are divisors and factors that cancel each other out
    summands = re.findall(r'(?<=[+-])[^+-]+?(?=[+-]|$)', challenge)
    for summand in summands:
        mul_divs = re.findall(r'[*/]\d', summand)
        for mul_div in mul_divs[:-1]:
            to_check = mul_divs.copy()
            to_check.remove(mul_div)
            for i in range(1, len(to_check)+1):
                for mul_div_permutation in combinations(to_check, i):
                    if eval(f'1{mul_div}') == eval(f'1/(1{"".join(mul_div_permutation)})'):
                        print(
                            f'{mul_div} can be cancelled out by {mul_div_permutation}')
                        return False
    print(f'{challenge} has no factors/divisors that cancel out')
    print('---')
    # check for the edgecase of '3+4*3'
    for cl_permutation in alive_it(get_permutations_cl(challenge)):  # TODO predict length
        if get_skyline(challenge) == get_skyline(cl_permutation) and cl_permutation != challenge:
            print('case x*n+x detected')
            return False
    print('---')

    return True

challenge = "4*3*2*6*3*9+7*8/2*9*4-4*6-4*4*5"
print(timeit.timeit(lambda: print(f'{is_valid_challenge(challenge)=}'), number=1, globals=globals()))
