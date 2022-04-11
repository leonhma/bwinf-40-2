from typing import Any, Callable, List


class ilist(list):
    def __init__(self, r=None, dft=None):
        if r is None:
            r = []
        list.__init__(self, r)
        self.dft = dft

    def _ensure_length(self, n):
        maxindex = n
        if isinstance(maxindex, slice):
            maxindex = maxindex.indices(len(self))[1]
        while len(self) <= maxindex:
            self.append(self.dft)

    def __getitem__(self, n):
        self._ensure_length(n)
        return super(ilist, self).__getitem__(n)

    def __setitem__(self, n, val):
        self._ensure_length(n)
        return super(ilist, self).__setitem__(n, val)


def remove_by_exp(exp: Callable[[Any], bool], lst: List):
    for i in lst:
        try:
            if exp(i):
                lst.remove(i)
                break
        except Exception:
            pass
