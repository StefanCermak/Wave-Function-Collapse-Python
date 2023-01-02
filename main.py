from globals import *
from parts import ClassParts
from grid import ClassGrid
from configdialog import ClassConfigDialog

class ClassWaveCollapseFunction:
    def __init__(self, design, window_width, parts_per_col, parts_per_row):
        self.Parts = ClassParts(design, window_width // parts_per_row)
        print(self.Parts)
        self.Grid = ClassGrid(window_width, parts_per_col, parts_per_row, self.Parts)

    def start(self):
        self.Grid.start_collapse()


if __name__ == '__main__':
    Dialog=ClassConfigDialog()
    Dialog.run()
    WCF = ClassWaveCollapseFunction(
        Dialog.design,
        Dialog.window_width,
        Dialog.pieces_per_col,
        Dialog.pieces_per_row
    )
    WCF.start()
