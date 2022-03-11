from random import choice, randint
import re
from typing import List
from wip import is_valid_challenge


def generate_challenge(length: int) -> str:
    """
    Generate a random challenge.
    """
    challenge = '+'+''.join([str(randint(1, 10))+choice(['+', '-', '*', '/']) for _ in range(length)])[:-1]
    while is_valid_challenge(challenge):
        challenge = '+'+''.join([str(randint(1, 10))+choice(['+', '-', '*', '/']) for _ in range(length)])[:-1]
    return f'{challenge}={eval(challenge)}'



