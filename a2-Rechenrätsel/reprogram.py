import math
import random
import re
from typing import List, Tuple
from alive_progress import alive_it
import itertools


def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

def generate(length: int = 5) -> str:
    print('----')
    def swap_factors(i: int, challenge: str) -> str:    # TODO raise error if left and right are the same and ignore the swapability
        # made for non-whitespace-containing challenge string
        assert challenge[i] == '*'
        left = ''
        p = i-1
        while challenge[p] not in ['+', '-']:
            left = challenge[p]+left
            p -= 1
            if p < 0:
                break
        right = challenge[i+1]
        return challenge[:p+1]+right+'*'+left+challenge[i+2:]
    # generate expression
    expression: List[Tuple[str, int]] = []
    expression.append(('', random.randint(1, 10)))
    for _ in range(length):
        # generate operator
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ops = ['+', '-', '*', '/']
        op = random.choice(ops)
        if op == '/':
            numbers.remove(0)
            for number in numbers:
                if expression[-1][1] % number != 0:
                    numbers.remove(number)
        expression.append((op, random.choice(numbers)))
    # check for similar mutations using the commutative law
    challenge = ''.join(f'{op}{number}' for op, number in expression)
    summands = tuple(challenge.split('+'))
    multiplications = challenge.count('*')
    print(f'{summands=}')
    skyline = tuple(int(num) for num in re.split(r'[*+-/]', challenge))
    print(f'{skyline=}')
    print(
        f'iterating through {((math.factorial(len(summands)) if len(summands) > 1 else 0)*(2**multiplications))-1} possibilities')
    # iterate through combinations of summands
    for summand_combo in itertools.combinations(summands, len(summands)):
        print(f'{summand_combo=}')
        swapped_summands = '+'.join(summand_combo)
        if not multiplications:
            print('no multiplications')
            if swapped_summands!=challenge:
                comp_skyline = tuple(int(num)
                                     for num in re.split(r'[*+-/]', swapped_summands))
                print(f'{comp_skyline=}')
                if skyline == comp_skyline:
                    return generate(length)
        else:
            print('multiplications')
            for multiplication_combo in itertools.combinations_with_replacement(
                [True, False],
                multiplications):
                print(f'{summand_combo==summands}, {multiplication_combo=}')
                if challenge == swapped_summands and multiplication_combo == tuple([False]*multiplications):
                    print('contd')
                    continue
                # swap factors
                swapped = swapped_summands
                for i, v in enumerate(multiplication_combo):
                    if v:
                        swapped = swap_factors(list(findall('*', swapped))[i], swapped)
                # and compare against skyline from original
                comp_skyline = tuple(int(num) for num in re.split(r'[*+-/]', swapped))
                print(f'{comp_skyline=}')
                if skyline == comp_skyline:
                    return generate(length)
    return challenge+'='+str(int(eval(challenge)))


def solve(challenge: str, quiet: bool = True) -> str:
    """
    Solve the challenge given as string.

    Raises
    ------
    ValueError
        If the challenge is not solvable or more than one solution exists.
    """

    def numberToBase(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]

    sides = [x.strip() for x in challenge.split('=')]
    nums = [int(x.strip()) for x in sides[0].split('◦')]
    result = int(sides[1])

    solutions = []
    iterator = range(
        4**(len(nums)-1)) if quiet else alive_it(range(4**(len(nums)-1)))
    for i in iterator:
        operators = ''.join([str(x) for x in numberToBase(i, 4)]).zfill(len(nums)-1).replace('0', '+').replace(
            '1', '-').replace('2', '*').replace('3', '/')  # TODO check for float calculation steps
        expression = []
        for i in range(len(nums)+len(operators)):
            if i % 2 == 0:
                expression.append(str(nums[i//2]))
            else:
                expression.append(operators[i//2])
        expression = ''.join(expression)
        f_expression = ' '.join(expression) + ' = ' + str(result)
        print('solver: '+f_expression)
        exp_result = eval(expression)
        if exp_result % 1 != 0:
            continue
        if(exp_result == result):
            solutions.append(f_expression)
    if not solutions:
        raise ValueError('No solution!')
    return solutions

""" 
for i in alive_it(range(100)):
    test = generate(5)
    test = test+'='+str(int(eval(test)))
    challenge = re.sub(r'[*+-/]', '◦', test)
    solution = solve(test).replace(' ', '')
    assert solution == test, f'error in {i}: {solution} != {test}' """

print(generate(8))
