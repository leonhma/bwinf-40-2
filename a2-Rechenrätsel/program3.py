from typing import List
from re import findall
from collections import deque


def is_unique_bfs(challenge: str) -> bool:
    results = set()
    s, *n = findall(r'\d', challenge)
    q = deque(((f'+{s}', n),))

    while q:
        results.clear()
        for _ in range(len(q)):
            stub, nums = q.popleft()
            if (ev := eval(stub)) in results:
                print('in solutions')
                # body matches the result, now check for non-int results
                summands = findall(r'[+-].*?(?=[+-]|$)', stub)
                for summand in summands:
                    s, *dm = [summand[i]+summand[i+1] for i in range(0, len(summand)-1, 2)]
                    while dm:
                        s = eval(f'{s}{dm.pop(0)}')
                        if not s%1:
                            print('returning false')
                            return False
            else:
                results.add(ev)
            if nums:
                for op in '+-*/':
                    q.append((stub+op+nums[0], nums[1:]))

    return True


if __name__ == '__main__':
    while True:
        challenge = input('challenge > ')
        print(is_unique_dfs(challenge))
