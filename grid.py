from .vector import Vector2D


class Grid:
    def __init__(self, size: Vector2D, size_rc: Vector2D) -> None:
        """Generates and Stores a 2D Grid."""
        self.size = size
        self.size_rc = size_rc
        self.cell_size = Vector2D(self.size.x / self.size_rc.x, self.size.y / self.size_rc.y)
        self.grid = []

    def generate(self) -> None:
        """Generates a Grid based on size, rows & columns."""
        for y in range(int(self.size_rc.y)):
            row = []
            for x in range(int(self.size_rc.x)):
                row.append(None)
            self.grid.append(row)

    def get_grid(self) -> list:
        """Returns the Grid."""
        return self.grid

    def set_pos(self, pos: Vector2D, item) -> None:
        """Sets item of given Position."""
        self.grid[int(pos.y)][pos.x] = item

    def get_pos(self, pos: Vector2D):
        """Gets item of given Position."""
        return self.grid[int(pos.y)][pos.x]

    def fill_row(self, row: int, item):
        """Fills a row with given item."""
        self.grid[row] = [item for _ in range(int(self.size_rc.x))]

    def get_row(self, row: int):
        """Returns items of given row index."""
        return self.grid[row]

    def fill_coll(self, col: int, item):
        """Fills a column with given item."""
        for row in self.grid:
            row[col] = item

    def get_coll(self, col: int):
        """Returns items of given coll index."""
        coll_contents = []
        for row in self.grid:
            coll_contents.append(row[col])
        return coll_contents

    def set_area(self, start_pos: Vector2D, items: list):
        """Replaces area in Grid with another 2D list."""
        for i, r in enumerate(items):
            self.grid[int(start_pos.y + i)][start_pos.x:start_pos.x + len(r)] = r

    def get_area(self, start_pos: Vector2D, end_pos: Vector2D):
        """Replaces area in Grid with another 2D list."""
        # for i, r in enumerate(items):
        return self.grid[start_pos.y:end_pos.y][start_pos.x:end_pos.x]  # dunno
