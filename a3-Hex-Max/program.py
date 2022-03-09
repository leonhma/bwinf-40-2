import os
from typing import List, Tuple, Union


class Segment:
    def __init__(self, data: Union[str, Tuple[Union[int, bool]]]):
        if isinstance(data, tuple):
            self.panels = [1 if data[x] else 0 for x in range(7)]
        else:
            self.panels = [0] * 7  # 7 panels, ``, ^|, v|, _, |v, --, |^
            data = data.upper()
            assert data in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                            'A', 'B', 'C', 'D', 'E', 'F'], "Invalid character for hex display"
            self.char = data
            if data not in '14BD':
                self.panels[0] = 1
            if data not in '56BCEF':
                self.panels[1] = 1
            if data not in '2CEF':
                self.panels[2] = 1
            if data not in '147AF':
                self.panels[3] = 1
            if data not in '134579':
                self.panels[4] = 1
            if data not in '017C':
                self.panels[5] = 1
            if data not in '1237D':
                self.panels[6] = 1

    def __repr__(self):
        return str(self.panels)

    def panels_needed(self, to: 'Segment') -> int:
        """The number of segments needed to convert this segment to the other segment."""
        return sum(to.panels[i] - self.panels[i] for i in range(7))

    def ascii_art(self) -> List[str]:
        """Return an ascii art representation of this segment."""

        # 0 1 2
        # 3 4 5
        # 6 7 8

        chars = [' '] * 9

        chars[1] = '═' if self.panels[0] else chars[1]
        chars[4] = '═' if self.panels[5] else chars[4]
        chars[7] = '═' if self.panels[3] else chars[7]

        chars[0] = '╔' if self.panels[0] or self.panels[6] else chars[0]
        chars[0] = '═' if self.panels[0] and not self.panels[6] else chars[0]
        chars[0] = '╔' if chars[0].strip() and self.panels[1] else chars[0]

        chars[2] = '╗' if self.panels[0] or self.panels[1] else chars[2]
        chars[2] = '═' if self.panels[0] and not self.panels[1] else chars[2]
        chars[2] = '╗' if chars[2].strip() and self.panels[6] else chars[2]

        chars[6] = '╚' if self.panels[3] or self.panels[4] else chars[6]
        chars[6] = '═' if self.panels[3] and not self.panels[4] else chars[6]
        chars[6] = '╚' if chars[6].strip() and self.panels[2] else chars[6]

        chars[8] = '╝' if self.panels[2] or self.panels[3] else chars[8]
        chars[8] = '═' if self.panels[3] and not self.panels[2] else chars[8]
        chars[8] = '╝' if chars[8].strip() and self.panels[4] else chars[8]

        chars[3] = '║' if self.panels[4] or self.panels[6] else chars[3]
        chars[3] = '╔' if self.panels[4] and (not self.panels[6]) else chars[3]
        chars[3] = '╚' if (not self.panels[4]) and self.panels[6] else chars[3]
        chars[3] = '═' if (self.panels[5] and not (self.panels[4] or self.panels[6])
                           and not (self.panels[0] and self.panels[3])) else chars[3]
        chars[3] = '╠' if self.panels[4] and self.panels[5] and self.panels[6] else chars[3]

        chars[5] = '║' if self.panels[1] or self.panels[2] else chars[5]
        chars[5] = '╝' if self.panels[1] and (not self.panels[2]) else chars[5]
        chars[5] = '╗' if (not self.panels[1]) and self.panels[2] else chars[5]
        chars[5] = '═' if (self.panels[5] and not (self.panels[1] or self.panels[2])
                           and not (self.panels[0] and self.panels[3])) else chars[5]
        chars[5] = '╣' if self.panels[1] and self.panels[5] and self.panels[2] else chars[5]

        return chars

    def get_donors_acceptors(self) -> List[Tuple['Segment', int, int]]:
        """
        Return a list of all possible changes to the current segment.

        Sorted by highest segment number first.

        Returns
        -------
        List[Tuple[Segment, int, int]]
            A list of tuples of the form (donor, number of operations, number of panels taken up (can be negative for freed panels))

        """
        return [
            (seg,
             sum(1 if self.panels[i] ^ seg.panels[i] else 0 for i in range(7)),
             sum(seg.panels[i] - self.panels[i] for i in range(7))
             )
            for seg in (Segment(x) for x in 'FEDCBA9876543210')
        ]


def print_segments():
    out = [[], [], []]
    for segment in segments:
        aart = segment.ascii_art()
        for i in range(3):
            out[i].append(''.join(aart[3 * i:3 * i + 3]))
    for i in range(3):
        print(''.join(out[i]))


path = os.path.dirname(os.path.realpath(__file__))+f'/beispieldaten/hexmax{0}.txt'

with open(path) as f:
    lines = f.read().splitlines()

segments = [Segment(x) for x in lines[0]]
max_shifts = int(lines[1])

print(f'{max_shifts=}')
print_segments()

for i, seg in enumerate(segments):
    next_1, ops, ext = ((s, o, e) for s, o, e in seg.get_donors_acceptors() if o < max_shifts).__next__()
    for j in range(len(segments)-1, i, -1):
        
        
