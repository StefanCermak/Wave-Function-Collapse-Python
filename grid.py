from parts import ClassParts
import pygame


class ClassGridField:
    def __init__(self, x: int, y: int, parts: ClassParts):
        self.possibleParts = None
        self.Part = None
        self.Parts = parts
        self.x = x
        self.y = y

    def neighborhood(self, n, e, s, w):
        if self.Part is None:
            self.possibleParts = set(self.Parts.PartList)
            if (n is not None) and (n.part is not None):
                self.possibleParts = self.possibleParts - n.part.bannsS
            if (e is not None) and (e.part is not None):
                self.possibleParts = self.possibleParts - e.part.bannsW
            if (s is not None) and (s.part is not None):
                self.possibleParts = self.possibleParts - s.part.bannsN
            if (w is not None) and (w.part is not None):
                self.possibleParts = self.possibleParts - w.part.bannsE
        else:
            self.possibleParts = set(range(len(self.Parts.PartList) + 1))


class ClassGrid:
    def __init__(self, window_width: int, rows: int, cols: int, parts: ClassParts):
        self.window_width = window_width
        self.window_height = window_width * rows // cols
        self.Parts = parts
        self.cols = cols
        self.rows = rows
        self.Field = [[None] * cols for _ in range(rows)]
        for row in range(rows):
            for col in range(cols):
                self.Field[row][col] = ClassGridField(col * window_width // cols, row * self.window_height // rows, parts)
        pygame.init()
        logo = pygame.image.load("Designes/Basic/Road_T.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Wave Function Collapse")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        for i in range(len(self.Parts.PartList)):
            self.Field[i][i].Part = self.Parts.PartList[i]

    def get_field(self, row: int, col: int) -> ClassGridField:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.Field[row][col]
        else:
            return None

    def start_collapse(self):
        self.draw()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i in range(0, self.rows + 1):
            pygame.draw.line(self.screen, (150, 150, 150),
                             (0,                 self.window_height*i//self.rows),
                             (self.window_width, self.window_height*i//self.rows)
                             )
        for i in range(0,self.cols + 1):
            pygame.draw.line(self.screen, (150, 150, 150),
                             (self.window_width*i//self.cols,0),
                             (self.window_width*i//self.cols,self.window_height)
                             )
        for Row in range(self.rows):
            for Col in range(self.cols):
                field = self.get_field(Row, Col)
                if field.Part is not None:
                    self.screen.blit(field.Part.image, (field.x, field.y))
        pygame.display.flip()
