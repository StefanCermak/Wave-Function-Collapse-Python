import globals
from parts import ClassParts


class ClassWaveCollapseFunction:
    def __init__(self, design, part_size):
        self.Parts = ClassParts(design, part_size)
        print(self.Parts)


if __name__ == '__main__':
    WCF = ClassWaveCollapseFunction("Basic", 100)
