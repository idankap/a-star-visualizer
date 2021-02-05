import enum
import pygame
import numpy as np


class CellType(enum.Enum):
    EMPTY = (255, 255, 255)         # White
    START = (140, 255, 140)         # Green
    TARGET = (255, 60, 60)          # Red
    WALL = (100, 100, 100)          # Grey
    VISITED = (100, 200, 255)       # Blue
    PATH = (255, 140, 255)          # Pink

    @classmethod
    def is_dragable_cell(cls, cell):
        return cell in (cls.START, cls.TARGET)


    @classmethod
    def is_a_star_cell(cls, cell):
        return cell in (cls.VISITED, cls.PATH)


class Grid:
    def __init__(self, rows: int, cols: int, cell_size: int, cell_margin: int):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.cell_margin = cell_margin

        self._cells = np.full((rows, cols), CellType.EMPTY)
        self._cells[rows // 2][cols // 4 - 1] = CellType.START
        self._cells[rows // 2][cols - cols // 4] = CellType.TARGET

        self._to_animate_pos = []
        self._to_animate_size = []

    def draw(self, surface: pygame.Surface):
        for row in range(self.rows):
            for col in range(self.cols):
                # Determin the size of the cell (0 - 1)
                try:
                    index = self._to_animate_pos.index((row, col))
                    self._to_animate_size[index] += 0.2
                    size = self._to_animate_size[index]
                    if size >= 1:
                        self._to_animate_pos.pop(index)
                        self._to_animate_size.pop(index)
                        raise ValueError
                except ValueError:
                    size = 1

                width = self.cell_size * size
                height = self.cell_size * size
                left = (self.cell_margin + self.cell_size) * col + self.cell_margin + self.cell_size // 2 - width // 2
                top = (self.cell_margin + self.cell_size) * row + self.cell_margin + self.cell_size // 2 - height // 2

                pygame.draw.rect(surface, self._cells[row][col].value, pygame.Rect(left, top, width, height))

    def clear(self, cells: list[CellType]):
        for row in range(self.rows):
            for col in range(self.cols):
                if self._cells[row][col] in cells:
                    self._cells[row][col] = CellType.EMPTY

    def get_cell(self, row: int, col: int) -> int:
        return self._cells[row][col]

    def get_cells(self, cell: CellType) -> list[tuple[int, int]]:
        rows, cols = np.where(self._cells == cell)
        locations = []

        for row, col in zip(rows, cols):
            locations.append((row, col))

        return locations

    def set_cell(self, row: int, col: int, value: CellType):
        self._cells[row][col] = value

        if not CellType.is_dragable_cell(value):
            self._to_animate_pos.append((row, col))
            self._to_animate_size.append(0)

    def out_of_bounds(self, row: int, col: int) -> bool:
        return col < 0 or row < 0 or col >= self.cols or row >= self.rows
