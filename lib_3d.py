import pygame.draw

#https://www.petercollingridge.co.uk/tutorials/3d/pygame/projecting-3d-objects/

class Vertex:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

class Edge:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

class Wireframe:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.vertex_color = (255, 255, 255)
        self.edge_color = (64, 64, 64)
        self.vert_radius = 5
        self.show_vertices = True
        self.show_edges = True

    def addVertex(self, coordinates):
        self.vertices.append(Vertex(coordinates))

    def addVertices(self, vert_list):
        for vertex in vert_list:
            self.vertices.append(self.vertices.append(Vertex(vertex)))

    def connect_edges(self, edge_list):
        for (start, stop) in edge_list:
            self.edges.append(Edge(self.vertices[start], self.vertices[stop]))

class Render:
    def __init__(self, win, wireframes: dict):
        self.win = win
        self.wireframes = wireframes

    def render(self):
        for wireframe in self.wireframes.values():
            if wireframe.show_edges:
                for edge in wireframe.edges:
                    print((edge.start_point.x, edge.start_point.y))
                    print((edge.end_point.x, edge.end_point.y))
                    pygame.draw.aaline(self.win, wireframe.edge_color, (edge.start_point.x, edge.start_point.y), (edge.end_point.x, edge.end_point.y))

            if wireframe.show_vertices:
                for vertex in wireframe.vertices:
                    pygame.draw.circle(self.win, wireframe.vertex_color, (int(vertex.x), int(vertex.y)), wireframe.vert_radius)
