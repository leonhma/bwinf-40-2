from typing import List
from re import findall


def is_unique_dfs(challenge: str) -> bool:
    solutions = set()

    def dfs(stub: str, nums: List[str]):
        if (ev := eval(stub)) in solutions:
            # body matches the result, now check for non-int results
            summands = findall(r'[+-].*?(?=[+-]|$)', combination)
            for summand in summands:
                s, *dm = [summand[i]+summand[i+1] for i in range(0, len(summand)-1, 2)]
                while dm:
                    s = float(eval(f'{s}{dm.pop(0)}'))
                    if not s%1:
                        return True
        else:
            solutions.add(ev)
        if len(nums):
            for op in '+-*/':
                if dfs(stub+op+nums[0], nums[1:]):
                    return True  # propagate truthy value upwards

    s, *n = findall(r'\d', challenge)

    return not dfs(f'+{s}', n)

if __name__ == '__main__':
    while True:
        challenge = input('challenge > ')
        print(is_unique_dfs(challenge))
