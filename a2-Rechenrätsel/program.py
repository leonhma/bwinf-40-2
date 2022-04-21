from collections import Counter
from typing import Generator
from secrets import choice
from typing import Callable, List, Union

import regex as re

from bruteforce_testing import is_unique


def is_sum_of_list_items(i: int, lst: List[int], add_action: Callable = lambda i, j: i-j) -> bool:
    """
    Check if the given number is the sum of multiple items in the given list.
    """
    if i in lst:
        return True
    for j in lst:
        new_lst = lst.copy()
        new_lst.remove(j)
        if is_sum_of_list_items(add_action(i, j), new_lst, add_action):
            return True
    return False


def cancelling_muls_divs_in_summand(summands):
    for summand in summands:
        divs = [int(x) for x in re.findall(r'(?<=\/)\d', summand)]
        muls = [int(x) for x in re.findall(r'(?<=\*)\d', summand)]

        for div in divs:
            if is_sum_of_list_items(div, muls, lambda i, j: i/j):
                return True
        for mul in muls:
            if is_sum_of_list_items(mul, divs, lambda i, j: i/j):
                return True


def xnx_case(challenge):
    parts = re.findall(
        r'(?<=[+-])(?:(?:\d\*?)+\+(?:\*?\d){2,}|(?:\d\*?){2,}\+(?:\*?\d)+)(?=[+-]|$)',
        challenge, overlapped=True)

    for part in parts:
        i = part.find('+')
        if i < (len(part)-1)/2:
            left = Counter(re.findall(r'\d', part[:i]))
            right = Counter(re.findall(r'\d', part[-i:]))
            left.subtract(right)
            if not left-Counter():
                return True
        elif i > (len(part)-1)/2:
            left = Counter(re.findall(r'\d', part[:len(part)-i]))
            right = Counter(re.findall(r'\d', part[i+1:]))
            left.subtract(right)
            if not left-Counter():
                return True


def check_challenge_fast(challenge: str) -> Union[None, str]:
    # ---- invalid if division/multiplication by 1 ----
    if re.search(r'[/*]1', challenge):
        return

    # ---- check that there's not one number followed by the same number again
    if re.search(r'(\d)[*-+/]\1', challenge):
        return

    # ---- check for 3*4+3 case ----
    if xnx_case(challenge):
        return

    # split into summands
    summands = re.findall(r'[+-].*?(?=[+-]|$)', challenge)

    # ---- check for cancelling muls/divs in summand ----
    if cancelling_muls_divs_in_summand(summands):
        return

    # ---- calculate each summand's result ----
    pluses: List[int] = []
    minuses: List[int] = []

    for summand in summands:
        sum_ = 0
        sum_ = int(summand[:2])
        if len(summand) > 2:
            for i in range(len(summand))[2::2]:
                if summand[i] == '/':
                    sum_ /= int(summand[i+1])
                elif summand[i] == '*':
                    sum_ *= int(summand[i+1])

        if sum_ < 0:
            minuses.append(-int(sum_))
        elif sum_ > 0:
            pluses.append(int(sum_))

    # ---- check for cancelling summands/minuends ----
    for plus in pluses:
        if is_sum_of_list_items(plus, minuses):
            return
    for minus in minuses:
        if is_sum_of_list_items(minus, pluses):
            return

    res = sum(pluses) - sum(minuses)
    if res < 0:
        return

    return res

def generate_challenge(length: int = 5) -> Generator[str, None, None]:
    nums = (1,2,3,4,5,6,7,8,9)
    while True:
        challenge = '+' + choice('123456789')
        previous = challenge[-1]
        for _ in range(length-1):
            op = choice('*-+') if previous in '12357' else choice('*-+/')  # cant divide with primes
            challenge += op
            if op == '*':
                challenge += str(choice([num for num in nums if num != 1 and num != int(previous)]))
            elif op == '/':
                challenge += str(choice([num for num in (2,3,4,5,6,7,8,9) if int(previous) % num == 0 and num != int(previous)]))
            elif op in '+-':
                challenge += str(choice([num for num in nums if num != int(previous)]))
            previous = challenge[-1]
        yield challenge

def get_challenge(length: int = 5) -> str:
    for challenge in generate_challenge(length):
        if res := check_challenge_fast(challenge):
            challenge = f'{challenge}={res}'
            if is_unique(challenge):
                return challenge

if __name__ == '__main__':
    # repl
    while True:
        try:
            i = int(input("Bitte die Länge des Rätsels eingeben: "))
            challenge = get_challenge(i)
            print(challenge)
            print(re.sub(r'[*/+-]', '◦', challenge[1:]))
        except Exception as e:
            print(e)
