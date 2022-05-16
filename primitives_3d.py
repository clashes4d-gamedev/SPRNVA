from lib_3d import *
class Cube:
    def __init__(self, vert_radius=5, nodecolor=(255, 255, 255), edgecolor=(64, 64, 64), show_vets=False, show_edges=True):
        self.data = Wireframe()
        self.data.vertex_color = nodecolor
        self.data.edgecolor = edgecolor
        self.data.show_vertices = show_vets
        self.data.show_edges = show_edges
        self.data.vert_radius = vert_radius
        self.data.addVertices([(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)])
        self.data.connect_edges([(n, n + 4) for n in range(0, 4)])
        self.data.connect_edges([(n, n + 1) for n in range(0, 8, 2)])
        self.data.connect_edges([(n, n + 2) for n in (0, 1, 4, 5)])

