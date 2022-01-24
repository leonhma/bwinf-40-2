import random


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
    last = random.randint(0, 9)
    challenge = f'+{last}'  # start with a plus sign and a number
    for _ in range(length):
        # generate operator
        op = random.choice(ops)
        # generate number
        if op == '/':
            nums = [
                number
                for number in numbers
                if (last >= number > 0) and (last % number == 0)
            ]
        else:
            nums = numbers
        last = random.choice(nums)
        # append to challenge
        challenge += op + str(last)
    # check if the result is positive
    if eval(challenge) < 0:
        return gen(length)
    # check if summands cancel each other out
    
    return challenge+'='+str(int(eval(challenge)))

print(gen(10))
