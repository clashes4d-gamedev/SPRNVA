class Grid:
    #TODO make this use Dicts instead of lists
    def __init__(self, size_rc: tuple) -> None:
        """Generates and Stores a 2D Grid."""
        self.size_rc = size_rc
        self.grid = {}

    def generate(self) -> None:
        """Generates a Grid based on size, rows & columns."""
        for y in range(int(self.size_rc[1])):
            row = {}
            for x in range(int(self.size_rc[0])):
                row[x] = None
            self.grid[y] = row

    def get_grid(self) -> dict:
        """Returns the Grid."""
        return self.grid

    def set_pos(self, pos: tuple, item) -> None:
        """Sets item of given Position."""
        self.grid[pos[0]][pos[1]] = item

    def get_pos(self, pos: tuple):
        """Gets item of given Position."""
        return self.grid[pos[0]][pos[1]]

    def set_row(self, row_index: int, item):
        """Fills a row with given item."""
        row = {}
        for i in range(self.size_rc[0]):
            row[i] = item

        self.grid[row_index] = row

    def get_row(self, row: int):
        """Returns items of given row index."""
        return self.grid[row]

    def set_col(self, col: int, item):
        """Fills a column with given item."""
        for k, v in enumerate(self.grid.items()):
            v[1][col] = item

    def get_col(self, col: int):
        """Returns items of given coll index."""
        coll_contents = []
        for row in self.grid:
            coll_contents.append(row[col])
        return coll_contents

    def set_area(self, start_pos: tuple, items: list):
        """Replaces area in Grid with another 2D list."""
        for ri, row in enumerate(items):
            for ci, col in enumerate(row):
                self.grid[start_pos[0] + ci][start_pos[1] + ri] = col

    def get_area(self, start_pos: tuple, end_pos: tuple):
        """Replaces area in Grid with another 2D list. WIP"""
        #WIP
        items = {}
        for i, v in enumerate(self.grid.items()):
            if i == start_pos[0]:
                for j, val in enumerate(v.items()):
                    if j == start_pos[1]:
                        items[i][j] = val
        return items
