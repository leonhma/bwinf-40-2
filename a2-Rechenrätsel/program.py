import random
import re
from typing import List, Tuple
from alive_progress import alive_it


def generate(operators: int) -> str:
    """
    Generate a random arithmetic expression with the given number of operators that follows these rules:
     1) the result is positive
     2) the result is an integer
     3) no divisions that result in non-int values
     4) there is only one solution
    """

    def next_op(previous: int) -> Tuple[str, int]:
        op = random.choice(['+', '-', '*', '/'])
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if op == '/':
            for number in numbers:
                if previous % number != 0:
                    numbers.remove(number)
        return op, random.choice(numbers)

    expression: List[Tuple[str, int]] = []
    expression.append(('+', random.randint(1, 10)))
    for _ in range(operators):
        op, number = next_op(expression[-1][1])
        expression.append((op, number))
    challenge = ''.join(f'{op}{number}' for op, number in expression)
    result = int(eval(challenge))
    challenge = re.sub(r"[*+-/]", '◦', (challenge[2:] + f' = {result}'))
    # check if expression satisfies rules
    if result < 0:
        return generate(operators)
    
    challenge = challenge if len(solve(challenge)) == 1 else generate(operators)  # stupid bruteforce check
    return challenge


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
        try:
            exp_result = eval(expression)
        except ZeroDivisionError:
            continue
        if exp_result % 1 != 0:
            continue
        if(exp_result == result):
            solutions.append(f_expression)
    if not solutions:
        raise ValueError('No solution!')
    return solutions


print('A2 - Rechenrätsel\n--------------------------------------------------------------------------------')
while(True):
    choice = input(
        'Geben sie "gen" ein, um ein neues Rätsel zu generieren oder "solve", um ein Rätsel zu lösen: ')
    if choice == 'gen':
        operators = int(input('Geben sie die Anzahl der Operatoren ein: '))
        print(generate(operators))
    elif choice == 'solve':
        challenge = input('Geben sie das Rätsel ein: ')
        try:
            solved = solve(challenge, False)
            print('Mögliche Lösung(en):')
            print('\n'.join(solved))
        except ValueError:
            print('Das Rätsel kann nicht gelöst werden!')
    print('--------------------------------------------------------------------------------')
