import random
import re


numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ops = ['+', '-', '*', '/']


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
        op = random.choice(ops)
        # generate number
        if op == '/':
            print('dividing')
            last = ''
            for i in range(len(challenge)-1, -1, -1):
                if challenge[i] in ['+', '-']:
                    break
                last = challenge[i]+last
            print(f'{last=}, {challenge=}')
            last = eval(last)
            nums = [
                number
                for number in numbers
                if (last >= number > 0) and (last % number == 0)
            ]
            print(f'{nums=}')
        else:
            nums = numbers
        # append to challenge
        challenge += op + str(random.choice(nums))
    # check if the result is positive
    if not is_valid_challenge(challenge):
        print(f'{challenge=} is invalid')
        return gen(length)
    return challenge+'='+str(int(eval(challenge)))

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
        True if the challenge is valid, False otherwise.
    """
    # check against regex if the challenge is valid (covers cases like ''8/4*2*2)
    if eval(challenge) < 0:
        print(f'result is negative: {challenge=}')
        return False
    # check if summands cancel each other out
    summands = re.findall(r'[+-][^+-]+?(?=[+-]|$)', challenge)
    for summand in summands[:-1]:  # remove last summand since it has already been checked
        summand = '-'+summand[1:] if summand[0] == '+' else '+'+summand[1:]
        if summand in summands:
            print(f'found cancelling single summands. {challenge=}')  # TODO work for combined summands that cancel each other +5-2-3 ~ -5+2+3 
            return False
    # check if the challenge contains the pattern x*n+x or x+n*x
    if re.search(
            r'(?P<opt1>\d)\*\d\+(?P=opt1)|(?P<opt2>\d)\+\d\*(?P=opt2)', challenge):
        print('found sus multiplication pattern. {challenge=}')
        return False
    return True


print()
print(gen(10))
