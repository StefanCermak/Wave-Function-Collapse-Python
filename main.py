from globals import *
from parts import ClassParts
from grid import ClassGrid


class ClassWaveCollapseFunction:
    def __init__(self, design, window_width, parts_per_col, parts_per_row):
        self.Parts = ClassParts(design, window_width // parts_per_row)
        print(self.Parts)
        self.Grid = ClassGrid(window_width, parts_per_col, parts_per_row, self.Parts)

    def start(self):
        self.Grid.start_collapse()


if __name__ == '__main__':
    WCF = ClassWaveCollapseFunction(
        DEFAULT_PART_SET,
        DEFAULT_WINDOW_WIDTH,
        DEFAULT_PIECES_PER_COL,
        DEFAULT_PIECES_PER_ROW
    )
    WCF.start()
