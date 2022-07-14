class LVL:
    def __init__(self, path: str):
        self.path = path

    def decode(self, get_size=False):
        with open(self.path) as lvl_file:
            lvl_file_lines = lvl_file.readlines()

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

    def encode(self):
        # .lvl Encoder/file generator
        ex_path = tb_ex_path.get_value()
        file = open(self.path, 'w')
        tile_lines = []
        for row in self.tiles.items():
            tile_line = []
            for tile in row[1].items():
                tile_line.append(tile[1])
            tile_lines.append(tile_line)

        file.write('TILE_TYPES_BEGIN\n')

        file.write(f'{self.tile_types}\n')

        file.write('TILE_TYPES_END\n')

        file.write('\n')

        file.write('TILE_SIZE_BEGIN\n')
        file.write(f'{self.grid_params["size"]}\n')
        file.write('TILE_SIZE_END\n')

        file.write('\n')

        file.write('LAYOUT_BEGIN\n')

        for row in tile_lines:
            for col in row:
                file.write(str(col))
            file.write('\n')

        file.write('LAYOUT_END\n')

        file.close()
        pygame.quit()
        exit()

