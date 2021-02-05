import sys
import pygame
from data.grid import Grid
from data.grid_editor import GridEditor
from data.a_star import AStar


class App:
    def __init__(self, grid_cols: int, grid_rows: int, cell_size: int, cell_margin: int):
        if grid_cols < 5 or grid_rows < 5:
            raise ValueError("grid cols and rows can't be less than 5")

        # Dimentions initialization ----------------------------------------- #
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size
        self.cell_margin = cell_margin
        self.width = grid_cols * (self.cell_size + self.cell_margin) + self.cell_margin
        self.height = grid_rows * (self.cell_size + self.cell_margin) + self.cell_margin

        if self.width < 120:
            raise ValueError("grid dimension are too small")

        # Pygame initialization --------------------------------------------- #
        pygame.init()
        pygame.display.set_caption("A* algorithm visualization")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()

        # Data initialization ----------------------------------------------- #
        self._grid = Grid(self.grid_rows, self.grid_cols, self.cell_size, self.cell_margin)
        self._grid_editor = GridEditor(self._grid)
        self._corners = True
        self._a_star = AStar(self._grid, corners=self._corners)

    def run(self):
        self._grid.draw(self.screen)

        mouse_pressed = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Dragging and drawing on the grid -------------------------- #
                if not self._a_star.is_running():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            mouse_pressed = True
                            row, col = self._screen_to_grid_pos(event.pos)
                            self._grid_editor.select_cell(row, col)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == pygame.BUTTON_LEFT:
                            mouse_pressed = False
                            self._grid_editor.unselect_cell()
                    if event.type == pygame.MOUSEMOTION:
                        if mouse_pressed:
                            row, col = self._screen_to_grid_pos(event.pos)
                            self._grid_editor.move_selected_cell(row, col)

                # Starting and pausing the algorithm ----------------------- #
                if not self._grid_editor.has_selected_cell():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self._a_star.start()
                        if event.key == pygame.K_ESCAPE:
                            self._a_star.pause()
                            self._a_star.resume()
                        if event.key == pygame.K_t:
                            self.toggle_corners()

            # Drawing ------------------------------------------------------- #
            if self._a_star.is_running():
                self._a_star.step()
            self._grid.draw(self.screen)

            # Updaing ------------------------------------------------------- #
            pygame.display.update()
            self.clock.tick(60)

    def toggle_corners(self):
        self._corners = not self._corners
        self._a_star.reset()
        self._a_star = AStar(self._grid, corners=self._corners)

    def _screen_to_grid_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        pos_x, pos_y = pos

        row = (pos_y - self.cell_margin // 2) // (self.cell_size + self.cell_margin)
        col = (pos_x - self.cell_margin // 2) // (self.cell_size + self.cell_margin)

        # Out of bounds check because of the cell margin
        if row >= self.grid_rows:
            row -= 1
        elif row <= -1:
            row += 1
        if col >= self.grid_cols:
            col -= 1
        elif col <= -1:
            col += 1

        return row, col
