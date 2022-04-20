from collections import Counter
from typing import Generator
from secrets import choice
from typing import Callable, List, Union

import regex as re


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
                print('a div can be cancelled by one or more muls')
                return True
        for mul in muls:
            if is_sum_of_list_items(mul, divs, lambda i, j: i/j):
                print('a mul can be cancelled by one or more divs')
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
                print(f'found x+n*x case: {part}')
                return True
        elif i > (len(part)-1)/2:
            left = Counter(re.findall(r'\d', part[:len(part)-i]))
            right = Counter(re.findall(r'\d', part[i+1:]))
            left.subtract(right)
            if not left-Counter():
                print(f'found x*n+x case: {part}')
                return True


def is_valid_challenge(challenge: str) -> Union[bool, str]:
    print('---------------------------------------')
    print(f'checking challenge: {challenge}')
    print('---------------------------------------')

    # ---- invalid if division/multiplication by 1 ----
    if re.search(r'[/*]1', challenge):
        print('division/multiplication by 1')
        return False

    # ---- check that there's not one number followed by the same number again
    if re.search(r'(\d)[*-+/]\1', challenge):
        print('one number followed by the same number')
        return False

    # ---- check for 3*4+3 case ----
    if xnx_case(challenge):
        return False

    # split into summands
    summands = re.findall(r'[+-].*?(?=[+-]|$)', challenge)

    # ---- check for cancelling muls/divs in summand ----
    if cancelling_muls_divs_in_summand(summands):
        return False

    # ---- calculate each summand's result while checking for non-int temporary results ----
    pluses: list[int] = []
    minuses: list[int] = []

    for summand in summands:
        sum_ = 0
        sum_ = int(summand[:2])
        print
        if len(summand) > 2:
            for i in range(len(summand))[2::2]:
                print(f'{summand[i]}{summand[i+1]}')
                if summand[i] == '/':
                    sum_ /= int(summand[i+1])
                elif summand[i] == '*':
                    sum_ *= int(summand[i+1])
                print(f'{sum_=}')
                if sum_ % 1:
                    print('non-int temporary result')
                    return False

        if sum_ < 0:
            minuses.append(-int(sum_))
        elif sum_ > 0:
            pluses.append(int(sum_))

    # ---- check for cancelling summands/minuends ----
    for plus in pluses:
        if is_sum_of_list_items(plus, minuses):
            print('a summand can be cancelled by one or more minuends')
            return False
    for minus in minuses:
        if is_sum_of_list_items(minus, pluses):
            print('a minuend can be cancelled by one or more summands')
            return False

    print(f'{pluses=}, {minuses=}')
    res = sum(pluses) - sum(minuses)
    print(res)
    if res < 0:
        print('result under 0')
        return False

    return res

def generate_challenge(length: int = 5) -> Generator[str, None, None]:
    nums = (1,2,3,4,5,6,7,8,9)
    while True:
        challenge = '+' + choice('123456789')
        previous = challenge[-1]
        for _ in range(length-1):
            op = choice('*-+') if previous in '1357' else choice('*-+/')  # cant divide with primes
            challenge += op
            if op == '*':
                challenge += str(choice([num for num in nums if num != 1 and num != int(previous)]))
            elif op == '/':
                try:
                    challenge += str(choice([num for num in (2,3,4,5,6,7,8,9) if int(previous) % num == 0 and num != int(previous)]))
                except IndexError:
                    print('index error')
                    print(f'{previous=}, {op=}, {[num for num in (2,3,4,5,6,7,8,9) if int(previous) % num == 0 and num != int(previous)]=}')
            elif op in '+-':
                challenge += str(choice([num for num in nums if num != int(previous)]))
            previous = challenge[-1]
        yield challenge

def get_challenge(length: int = 5):
    for challenge in generate_challenge(length):
        if is_valid_challenge(challenge):
            return challenge

while True:
    i = int(input("Bitte die Länge des Rätsels eingeben: "))
    print(get_challenge(i))
