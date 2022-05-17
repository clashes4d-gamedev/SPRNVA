# import math
# from .vector import Vector
# import pygame.draw
#
# #https://www.petercollingridge.co.uk/tutorials/3d/pygame/projecting-3d-objects/
#
# class Vertex:
#     def __init__(self, coordinates):
#         self.x = coordinates[0]
#         self.y = coordinates[1]
#         self.z = coordinates[2]
#
# class Edge:
#     def __init__(self, start_point, end_point):
#         self.start_point = start_point
#         self.end_point = end_point
#
# class Wireframe:
#     def __init__(self):
#         self.vertices = []
#         self.edges = []
#         self.faces = []
#         self.vertex_color = (255, 255, 255)
#         self.edge_color = (64, 64, 64)
#         self.face_color = (50, 50, 50)
#         self.vert_radius = 5
#         self.show_vertices = True
#         self.show_edges = True
#         self.show_faces = True
#
#     def addVertex(self, coordinates: tuple):
#         self.vertices.append(Vertex(coordinates))
#
#     def addVertices(self, vert_list: list):
#         for vertex in vert_list:
#             # TEMPORARY
#             x,y,z = vertex
#             vertex = x * 50, y * 50, z * 50
#             self.vertices.append(Vertex(vertex))
#
#     def connect_edges(self, edge_list: list):
#         for (start, stop) in edge_list:
#             self.edges.append(Edge(self.vertices[start], self.vertices[stop]))
#
#     def connect_faces(self, face_list: list):
#         for vert_list in face_list:
#             num_verts = len(vert_list)
#             if all((vertex < len(self.vertices) for vertex in vert_list)):
#                 self.faces.append([self.vertices[vertex] for vertex in vert_list])
#                 #self.faces.append((node_list, np.array(face_colour, np.uint8)))
#                 self.connect_edges([(vert_list[n-1], vert_list[n]) for n in range(num_verts)])
#
#     def find_center(self):
#         num_verts = len(self.vertices)
#         center_x = sum([vertex.x for vertex in self.vertices]) / num_verts
#         center_y = sum([vertex.y for vertex in self.vertices]) / num_verts
#         center_z = sum([vertex.z for vertex in self.vertices]) / num_verts
#         return center_x, center_y, center_z
#
#     def translate(self, axis: str, ammount: float):
#         if axis in ['x', 'y', 'z']:
#             for vertex in self.vertices:
#                 setattr(vertex, axis, getattr(vertex, axis) + ammount)
#
#     def scale_wrld(self, center: Vector, ammount: float):
#         for vertex in self.vertices:
#             vertex.x = center.x + ammount * (vertex.x - center.x)
#             vertex.y = center.y + ammount * (vertex.y - center.y)
#             vertex.z *= ammount
#
#     def rotate_z(self, angle: float):
#         cx, cy, cz = self.find_center()
#         for vertex in self.vertices:
#             x = vertex.x - cx
#             y = vertex.y - cy
#             d = math.hypot(x, y)
#             theta = math.atan2(y, x) + angle
#             vertex.x = cx + d * math.cos(theta)
#             vertex.y = cy + d * math.sin (theta)
#
#     def rotate_x(self, angle: float):
#         cx, cy, cz = self.find_center()
#         for vertex in self.vertices:
#             y = vertex.y - cy
#             z = vertex.z - cz
#             d = math.hypot(y, z)
#             theta = math.atan2(y, z) + angle
#             vertex.z = cz + d * math.cos(theta)
#             vertex.y = cy + d * math.sin (theta)
#
#     def rotate_y(self, angle: float):
#         cx, cy, cz = self.find_center()
#         for vertex in self.vertices:
#             x = vertex.x - cx
#             z = vertex.z - cz
#             d = math.hypot(x, z)
#             theta = math.atan2(x, z) + angle
#             vertex.z = cz + d * math.cos(theta)
#             vertex.x = cx + d * math.sin (theta)
#
# class Render:
#     def __init__(self, win, wireframes: dict):
#         self.win = win
#         self.wireframes = wireframes
#
#     def render(self):
#         for wireframe in self.wireframes.values():
#             if wireframe.show_edges:
#                 for edge in wireframe.edges:
#                     pygame.draw.aaline(self.win, wireframe.edge_color, (edge.start_point.x, edge.start_point.y), (edge.end_point.x, edge.end_point.y))
#
#             if wireframe.show_vertices:
#                 for vertex in wireframe.vertices:
#                     pygame.draw.circle(self.win, wireframe.vertex_color, (int(vertex.x), int(vertex.y)), wireframe.vert_radius)
#
#             if wireframe.show_faces:
#                 for face in wireframe.faces:
#                     pygame.draw.polygon(self.win, wireframe.face_color, [vertex for vertex in face])


