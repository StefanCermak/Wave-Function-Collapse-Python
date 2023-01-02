from parts import ClassParts
import pygame
import random


class ClassGridField:
    def __init__(self, x: int, y: int, parts: ClassParts):
        self.possibleParts = set()
        self.Part = None
        self.Parts = parts
        self.x = x
        self.y = y

    def neighborhood(self, n, e, s, w):
        if self.Part is None:
            self.possibleParts = set(self.Parts.PartList)
            if (n is not None) and (n.Part is not None):
                self.possibleParts = self.possibleParts - n.Part.bannsS
            if (e is not None) and (e.Part is not None):
                self.possibleParts = self.possibleParts - e.Part.bannsW
            if (s is not None) and (s.Part is not None):
                self.possibleParts = self.possibleParts - s.Part.bannsN
            if (w is not None) and (w.Part is not None):
                self.possibleParts = self.possibleParts - w.Part.bannsE
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
                self.Field[row][col] = ClassGridField(col * window_width // cols,
                                                      row * self.window_height // rows,
                                                      parts)
        pygame.init()
        logo = pygame.image.load("Designes/Basic/Road_T.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Wave Function Collapse")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        # for i in range(len(self.Parts.PartList)):
        #    self.Field[i][i].Part = self.Parts.PartList[i]

    def get_field(self, row: int, col: int) -> ClassGridField:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.Field[row][col]
        else:
            return None

    def update_possible_parts(self) -> bool:
        for Row in range(self.rows):
            for Col in range(self.cols):
                self.Field[Row][Col].neighborhood(
                    self.get_field(Row-1, Col),
                    self.get_field(Row, Col + 1),
                    self.get_field(Row + 1, Col),
                    self.get_field(Row, Col - 1))
        max_neighbors = 999999999
        for Row in range(self.rows):
            for Col in range(self.cols):
                if len(self.Field[Row][Col].possibleParts) < max_neighbors:
                    max_neighbors = len(self.Field[Row][Col].possibleParts)

        return (max_neighbors > 0) and max_neighbors < len(self.Parts.PartList) + 1

    def collapse_next(self):
        min_occurrence = 999999999
        cells = []
        for Row in range(self.rows):
            for Col in range(self.cols):
                if len(self.Field[Row][Col].possibleParts) == min_occurrence:
                    cells.append(self.Field[Row][Col])
                if len(self.Field[Row][Col].possibleParts) < min_occurrence:
                    min_occurrence = len(self.Field[Row][Col].possibleParts)
                    cells = [self.Field[Row][Col]]
        if len(cells) > 0:
            next_cell_collapse = random.choice(cells)
            next_cell_collapse.Part = random.choice(list(next_cell_collapse.possibleParts))

    def is_solved(self):
        for Row in range(self.rows):
            for Col in range(self.cols):
                if self.Field[Row][Col].Part is None:
                    return False
        return True

    def clean_zeros(self):
        for Row in range(self.rows):
            for Col in range(self.cols):
                if len(self.Field[Row][Col].possibleParts) == 0:
                    for dRow in [-1, 0, 1]:
                        for dCol in [-1, 0, 1]:
                            if self.get_field(Row + dRow, Col + dCol) is not None:
                                self.Field[Row + dRow][Col + dCol].Part = None
        self.update_possible_parts()

    def start_collapse(self):

        self.update_possible_parts()
        self.draw()
        running = True
        solving = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if solving:
                self.collapse_next()
                solving = not self.is_solved()
                self.draw()
                if not self.update_possible_parts():
                    self.clean_zeros()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i in range(0, self.rows + 1):
            pygame.draw.line(self.screen, (150, 150, 150),
                             (0,                 self.window_height*i//self.rows),
                             (self.window_width, self.window_height*i//self.rows)
                             )
        for i in range(0, self.cols + 1):
            pygame.draw.line(self.screen, (150, 150, 150),
                             (self.window_width*i//self.cols, 0),
                             (self.window_width*i//self.cols, self.window_height)
                             )
        for Row in range(self.rows):
            for Col in range(self.cols):
                field = self.get_field(Row, Col)
                if field.Part is not None:
                    print(f"{Row} {Col} {field.Part}")
                    self.screen.blit(field.Part.image, (field.x, field.y))
        pygame.display.flip()
