import copy
from .grid import Grid, CellType


class GridEditor:
    def __init__(self, grid: Grid):
        self._grid = grid
        self._grid_copy = copy.deepcopy(self._grid)
        self._selected_cell = -1

    def select_cell(self, row: int, col: int):
        if not self._grid.out_of_bounds(row, col):
            self._grid.clear([CellType.VISITED, CellType.PATH])

            selected_cell = self._grid.get_cell(row, col)

            if selected_cell == CellType.EMPTY:
                self._selected_cell = CellType.WALL
                self.move_selected_cell(row, col)
            elif selected_cell == CellType.WALL:
                self._selected_cell = CellType.EMPTY
                self.move_selected_cell(row, col)
            else:
                self._selected_cell = selected_cell
                self._grid_copy = copy.deepcopy(self._grid)

    def unselect_cell(self):
        self._selected_cell = -1

    def has_selected_cell(self) -> bool:
        return self._selected_cell != -1

    def move_selected_cell(self, row: int, col: int):
        if self._selected_cell == -1:
            raise NotImplementedError("There is no selected cell")

        if not self._grid.out_of_bounds(row, col):
            if not CellType.is_dragable_cell(self._grid.get_cell(row, col)):
                if CellType.is_dragable_cell(self._selected_cell):
                    sel_cell_loc = self._grid.get_cells(self._selected_cell)
                    sel_cell_row, sel_cell_col = sel_cell_loc[0]

                    # Delete _selected_cell from his current location
                    if self._grid_copy.get_cell(sel_cell_row, sel_cell_col) == CellType.WALL:
                        self._grid.set_cell(sel_cell_row, sel_cell_col, CellType.WALL)
                    else:
                        self._grid.set_cell(sel_cell_row, sel_cell_col, CellType.EMPTY)

                # Draw _selected_cell to the given location
                self._grid.set_cell(row, col, self._selected_cell)
