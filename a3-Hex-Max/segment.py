from typing import List, Tuple, Union


class Segment:
    """Class representing a segment of a 7-segment display."""

    def __init__(self, char: Union[str, Tuple[Union[int, bool]]]):
        """
        Initialise the segment with data.

        Parameters
        ----------
        data : str
            The data to initialise the segment with. Either a hex character [0-9A-F] or a tuple of 7 booleans.

        """
        self.panels = [0] * 7  # 7 panels, ``, ^|, v|, _, |v, --, |^
        self.char = char.upper()
        assert self.char in '0123456789ABCDEF', "Invalid character for hex display"
        if self.char not in '14BD':
            self.panels[0] = 1
        if self.char not in '56BCEF':
            self.panels[1] = 1
        if self.char not in '2CEF':
            self.panels[2] = 1
        if self.char not in '147AF':
            self.panels[3] = 1
        if self.char not in '134579':
            self.panels[4] = 1
        if self.char not in '017C':
            self.panels[5] = 1
        if self.char not in '1237D':
            self.panels[6] = 1

    def __repr__(self):
        return f'<Segment ({self.char if hasattr(self, "char") else self.panels })>'

    def __eq__(self, other):
        return self.panels == other.panels

    def ascii_art(self) -> List[str]:
        """
        Get an ascii art representation of this segment.

        Returns
        -------
        List[str]
            A 3x3 matrix of characters traversing every row from the top left to the bottom right.

            | 0 | 1 | 2 |\n
            | 3 | 4 | 5 |\n
            | 6 | 7 | 8 |\n

        """
        chars = [' '] * 9

        chars[1] = '═' if self.panels[0] else chars[1]
        chars[4] = '═' if self.panels[5] else chars[4]
        chars[7] = '═' if self.panels[3] else chars[7]

        chars[0] = '╔' if self.panels[0] or self.panels[6] else chars[0]
        chars[0] = '╔' if self.panels[0] and not self.panels[6] else chars[0]
        chars[0] = '╔' if chars[0].strip() and self.panels[1] else chars[0]

        chars[2] = '╗' if self.panels[0] or self.panels[1] else chars[2]
        chars[2] = '╗' if self.panels[0] and not self.panels[1] else chars[2]
        chars[2] = '╗' if chars[2].strip() and self.panels[6] else chars[2]

        chars[6] = '╚' if self.panels[3] or self.panels[4] else chars[6]
        chars[6] = '╚' if self.panels[3] and not self.panels[4] else chars[6]
        chars[6] = '╚' if chars[6].strip() and self.panels[2] else chars[6]

        chars[8] = '╝' if self.panels[2] or self.panels[3] else chars[8]
        chars[8] = '╝' if self.panels[3] and not self.panels[2] else chars[8]
        chars[8] = '╝' if chars[8].strip() and self.panels[4] else chars[8]

        chars[3] = '║' if self.panels[4] or self.panels[6] else chars[3]
        chars[3] = '╔' if self.panels[4] and (not self.panels[6]) else chars[3]
        chars[3] = '╚' if (not self.panels[4]) and self.panels[6] else chars[3]
        chars[3] = '╠' if self.panels[4] and self.panels[5] and self.panels[6] else chars[3]

        chars[5] = '║' if self.panels[1] or self.panels[2] else chars[5]
        chars[5] = '╝' if self.panels[1] and (not self.panels[2]) else chars[5]
        chars[5] = '╗' if (not self.panels[1]) and self.panels[2] else chars[5]
        chars[5] = '╣' if self.panels[1] and self.panels[5] and self.panels[2] else chars[5]

        return chars

    def get_takes_gives(self, seg) -> Tuple[int, int]:
            takes = sum(1 if self.panels[x] < seg.panels[x] else 0 for x in range(7))
            gives = sum(1 if self.panels[x] > seg.panels[x] else 0 for x in range(7))
            return takes, gives
