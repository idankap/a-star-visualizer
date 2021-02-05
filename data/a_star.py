import math
from .grid import Grid, CellType


class AStar:
    def __init__(self, grid: Grid, corners = True):
        self._grid = grid
        self._is_running = False
        self._paused = True
        self._start_cell: tuple
        self._target_cell: tuple
        self._current: tuple
        self._corners = corners
        self._neighbor_cells: list
        self._visible_cells: list
        self._g_scores: dict
        self._f_scores: dict
        self._found_path = False
        self._path: dict

    def is_running(self) -> bool:
        return self._is_running

    def start(self):
        self.reset()
        self._is_running = True
        self._paused = False
        self._start_cell = self._grid.get_cells(CellType.START)[0]
        self._target_cell = self._grid.get_cells(CellType.TARGET)[0]
        self._current = ()
        self._neighbor_cells = []
        self._visible_cells = [self._start_cell]
        self._g_scores = {self._start_cell: 0}
        self._f_scores = {self._start_cell: 0}
        self._found_path = False
        self._path = {}

    def finish(self):
        self.pause()
        self._is_running = False

    def pause(self):
        if self._is_running:
            self._paused = True

    def resume(self):
        if self._is_running:
            self._paused = False

    def reset(self):
        self._grid.clear([CellType.VISITED, CellType.PATH])

    def step(self):
        if not self._is_running and not self._paused:
            raise NotImplementedError("step was called before start.")

        if self._found_path:
            self._construct_path()
        else:
            self._search_path()

    def _construct_path(self):
        if self._current in self._path:
            self._current = self._path[self._current]
            row, col = self._current
            if self._current != self._start_cell:
                self._grid.set_cell(row, col, CellType.PATH)
        else:
            self.finish()

    def _search_path(self):
        self._current = self._find_best_visible_cell()

        if self._current == self._target_cell:
            self._found_path = True
            return

        self._visible_cells.remove(self._current)

        self._update_neighbor_cells()

        for neighbor in self._neighbor_cells:
            # Calculate the g-score of the neighbor reletive to current
            g_score = self._g_scores[self._current] + math.dist(self._current, neighbor)

            if neighbor not in self._g_scores or g_score < self._g_scores[neighbor]:
                # Update the path and the neigbor
                self._path[neighbor] = self._current
                self._g_scores[neighbor] = g_score
                self._f_scores[neighbor] = g_score + math.dist(neighbor, self._target_cell)

                if neighbor not in self._visible_cells:
                    self._visible_cells.append(neighbor)

        # Drawing the visible cells
        for cell in self._visible_cells:
            row, col = cell
            if self._grid.get_cell(row, col) == CellType.EMPTY:
                self._grid.set_cell(row, col, CellType.VISITED)

        # There is no path
        if not self._visible_cells:
            self.finish()

    def _find_best_visible_cell(self) -> tuple[int, int]:
        f_scores = [self._f_scores[cell] for cell in self._visible_cells]
        return self._visible_cells[f_scores.index(min(f_scores))]

    def _update_neighbor_cells(self):
        row, col = self._current

        self._neighbor_cells = []

        # Checking for corner neighbors ------------------------------------- #
        if self._corners:
            if self._valid_neighbor(row + 1, col - 1):          # Bottom Left
                self._neighbor_cells.append((row + 1, col - 1))
            if self._valid_neighbor(row + 1, col + 1):          # Bottom Right
                self._neighbor_cells.append((row + 1, col + 1))
            if self._valid_neighbor(row - 1, col - 1):          # Top Left
                self._neighbor_cells.append((row - 1, col - 1))
            if self._valid_neighbor(row - 1, col + 1):          # Top Right
                self._neighbor_cells.append((row - 1, col + 1))

        # Checking for horizontal and vertical neigbors --------------------- #
        if self._valid_neighbor(row, col - 1):                  # Left
            self._neighbor_cells.append((row, col - 1))
        if self._valid_neighbor(row, col + 1):                  # Right
            self._neighbor_cells.append((row, col + 1))
        if self._valid_neighbor(row + 1, col):                  # Bottom
            self._neighbor_cells.append((row + 1, col))
        if self._valid_neighbor(row - 1, col):                  # Top
            self._neighbor_cells.append((row - 1, col))


    def _valid_neighbor(self, row: int, col: int) -> bool:
        return not self._grid.out_of_bounds(row, col) and self._grid.get_cell(row, col) != CellType.WALL
