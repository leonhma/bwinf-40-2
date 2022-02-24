import itertools
import re
from typing import Generator, List


def count_indices_up_to(maxindices: List[int]) -> Generator[List[int], None, None]:
    """
    Generate all indices up to the given maximum indices.

    Parameters
    ----------
    maxindices : List[int]
        The maximum indices.

    Returns
    -------
    Generator[List[int], None, None]
        The indices.

    """
    indices = [0] * len(maxindices)
    while True:
        yield indices.copy()
        def count_up():
            for e, i in enumerate(indices):
                if i == maxindices[e]:
                    indices[e] = 0
                else:
                    indices[e] += 1
                    break
        if(indices == maxindices):
            break
        count_up()


def get_permutations_cl(term: str) -> List[str]:  # TODO optimize
    """
    Generate all permutations of a term using the commutative law.

    Parameters
    ----------
    term : str
        The term to generate permutations for.

    Returns
    -------
    List[str]
        The permutations of the term.

    """
    combinations = []
    # normalize input
    term = term.replace(' ', '')
    if term[0] != '+':
        term = '+' + term
    # get all summands
    summands = re.findall(
        r'[+-].+?(?=[+-]|$)', term)

    first, *summands = summands
    # create a big table of all permutations
    combinations = []
    for i, summand in enumerate(summands):
        combinations.append([])
        sign = summand[0]
        factors = summand[1:].split('*')
        for multiplacion_combinations in itertools.permutations(factors, len(factors)):
            multiplacion_combinations = '*'.join(multiplacion_combinations)
            combinations[i].append(f'{sign}{multiplacion_combinations}')
    # for each summand permutation, yield all the factor permutations
    for summand_combinations in itertools.permutations(combinations, len(combinations)):
        maxindices = [len(summand_combinations[i]) - 1 for i in range(len(summand_combinations))]
        for indices in count_indices_up_to(maxindices):
            yield first+''.join([column[indices[i]] for i, column in enumerate(summand_combinations)])

print(list(get_permutations_cl("4*3+4")))
