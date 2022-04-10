from itertools import repeat
from typing import List
from segment import Segment
from os.path import join, dirname

display: List[Segment]
takes: int
puts: int

with open(join(dirname(__file__), 'beispieldaten/hexmax0.txt')) as f:
    display = [Segment(char) for char in f.readline().strip()]
    takes, puts = repeat(int(f.readline().strip()), 2)


