

class LVL:
    def __init__(self):
        pass

    def decode(self, file_path, get_size=False):
        lvl_file = open(file_path)
        lvl_file_lines = lvl_file.readlines()
        lvl_file.close()
        get_tile_types = False
        get_layout = False
        get_tile_size = False

        tile_types = {}
        tile_size = 0
        layout = []

        for index, line in enumerate(lvl_file_lines):
            line = line.removesuffix('\n')
            if line == 'TILE_TYPES_BEGIN':
                get_tile_types = True
                continue

            if line == 'TILE_TYPES_END':
                get_tile_types = False
                continue

            if line == 'TILE_SIZE_BEGIN':
                get_tile_size = True
                continue

            if line == 'TILE_SIZE_END':
                get_tile_size = False
                continue

            if line == 'LAYOUT_BEGIN':
                get_layout = True
                continue

            if line == 'LAYOUT_END':
                get_layout = False
                continue

            if get_tile_types:
                tile_types = ast.literal_eval(line)

            if get_tile_size:
                tile_size = int(line)

            if get_layout:
                line_chars = []
                for char in line:
                    line_chars.append(char)
                layout.append(line_chars)

        grid_size_x = len(layout[0])
        grid_size_y = len(layout)
        grid_size = (grid_size_x, grid_size_y)

        return tile_types, layout, grid_size, tile_size

