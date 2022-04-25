from typing import Dict, Hashable


class TabuList:
    tabu: Dict[Hashable, int]
    offset: int
    default_tenure: int
    cleanup_freq: int

    def __init__(self, default_tenure: int, cleanup_freq: int = 20):
        self.tabu = {}
        self.offset = 0
        self.default_tenure = default_tenure
        self.cleanup_freq = cleanup_freq

    def _cleanup(self):
        to_delete = [k for k, v in self.tabu.items() if v+self.offset <= 0]
        for k in to_delete:
            del self.tabu[k]

    def add(self, item: Hashable, tenure: int = None):
        self.tabu[item] = (tenure or self.default_tenure)-self.offset

    def get(self, item: Hashable) -> int:
        if item in self.tabu:
            val = self.tabu[item]+self.offset
            return max(val, 0)
        return 0

    def tick(self):
        self.offset -= 1
        if self.offset % self.cleanup_freq == 0:
            self._cleanup()
