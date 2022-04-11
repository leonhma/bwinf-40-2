from typing import Any, Callable, List


def remove_by_exp(exp: Callable[[Any], bool], lst: List):
    for i in lst:
        try:
            if exp(i):
                lst.remove(i)
                break
        except Exception:
            pass
