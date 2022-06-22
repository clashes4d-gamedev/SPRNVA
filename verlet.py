import math
import pygame
import SPRNVA as sprnva
from numba import jit
from SPRNVA import Vector2D

# class VerletBall:
#     def __init__(self, pos: Vector2D, acc: Vector2D, dt: float, sim_size: Vector2D, ground_friction=0.5, radius=5, grav_constant=Vector2D(0, -9.81)):
#         self.pos = pos
#         self.acc = acc
#         self.old_pos = self.pos
#         self.dt = dt
#         self.ground_friction = ground_friction
#         self.grav_constant = grav_constant
#         self.sim_size = sim_size
#         self.accuracy = 0.001
#         self.radius = radius
#
#     def update(self):
#         self.old_pos = self.pos
#         self.vel = self.pos - self.old_pos
#         self.pos = self.pos + self.vel + self.acc * self.dt**2
#
#         if self.pos.y + self.radius >= self.sim_size.y:
#             self.pos.y = self.sim_size.y - self.radius
#             #self.vel.y = -(self.vel.y * self.ground_friction)
#             self.acc.y = -(self.acc.y * self.ground_friction)
#
#         if self.pos.y - self.radius <= 0:
#             self.pos.y = self.radius
#             #self.vel.y = -self.vel.y
#             self.acc.y = -(self.acc.y * self.ground_friction)
#
#         if self.pos.x + self.radius >= self.sim_size.x:
#             self.pos.x = self.sim_size.x - self.radius
#             #self.vel.x = -(self.acc.x * self.ground_friction)
#
#         if self.pos.x - self.radius <= 0:
#             self.pos.x = self.radius
#             self.acc.x = -(self.acc.x * self.ground_friction)
#
#         print('Velocity', self.vel.x, self.vel.y)
#         print('Acceleration', self.acc.x, self.acc.y)
#
#     def enable_collisions(self, vertex_list: list):
#         for index, vert1 in enumerate(vertex_list[:]):
#             for vert2 in vertex_list[:index:]:
#
#                 coll_axis = vert1.pos - vert2.pos
#                 dist = coll_axis.magnitude
#                 if dist <= vert1.radius*2:
#                     n = coll_axis / dist
#                     delta = vert1.radius*2 - dist
#                     vert1.pos += 0.5 * delta * n
#                     vert2.pos -= 0.5 * delta * n
#
#     def draw(self, win: pygame.Surface, color: tuple):
#         pygame.draw.circle(win, color, (self.pos.x, self.pos.y), self.radius)

@jit(nopython=True, parallel=True)
def _calc_verlet_vertex_constraints(pos, size, radius):
    x, y = pos
    if y + radius >= size[1]:
        y = size[1] - radius

    if y - radius <= 0:
        y = radius

    if x + radius >= size[0]:
        x = size[0] - radius

    if x - radius <= 0:
        x = radius

    output = (x, y)
    return output

@jit(nopython=True)
def _calc_verlet_vertex_position(pos, vel, acc, size_y, radius, vel_magnitude, coll_friction):
    curr_vel_x = vel[0]
    curr_vel_y = vel[0]
    if pos[1] + radius >= size_y:
        curr_vel_x /= vel_magnitude
        curr_vel_y /= vel_magnitude

        curr_vel_x *= vel_magnitude * coll_friction
        curr_vel_y *= vel_magnitude * coll_friction

    pos = (pos[0] + curr_vel_x + acc[0], pos[1] + curr_vel_y + acc[1])

    return pos

@jit(nopython=True)
def _calc_verlet_joint(vert1_pos, vert2_pos, length, vert_pin):
    dx = vert2_pos[0] - vert1_pos[0]
    dy = vert2_pos[1] - vert1_pos[1]

    distance = (dx ** 2 + dy ** 2)**(1/2)
    difference = (length - distance) / distance

    offset_x = dx * difference * 0.5
    offset_y = dy * difference * 0.5

    if vert_pin[0] == 0:
        vert1_endpos_x = vert1_pos[0] - offset_x
        vert1_endpos_y = vert1_pos[1] - offset_y
    else:
        vert1_endpos_x = vert1_pos[0]
        vert1_endpos_y = vert1_pos[1]

    if vert_pin[1] == 0:
        vert2_endpos_x = vert2_pos[0] + offset_x
        vert2_endpos_y = vert2_pos[1] + offset_y

    else:
        vert2_endpos_x = vert2_pos[0]
        vert2_endpos_y = vert2_pos[1]

    return (vert1_endpos_x, vert1_endpos_y), (vert2_endpos_x, vert2_endpos_y)

class VerletVertex:
    def __init__(self, size: Vector2D, pos: Vector2D, acc: Vector2D, dt: float, radius=1, coll_friction=0.75, pinned=False):
        self.size = size
        self.pos = pos
        self.acc = acc
        self.dt = dt
        self.radius = radius
        self.pinned = pinned
        self.coll_friction = coll_friction
        self.old_pos = self.pos
        self.vel = self.acc

    def update(self):
        if self.pinned is False:
            self.vel = self.pos - self.old_pos

            calc_pos = _calc_verlet_vertex_position((self.pos.x, self.pos.y), (self.vel.x, self.vel.y), (self.acc.x, self.acc.y), self.size.y, self.radius, self.vel.magnitude, self.coll_friction)
            self.pos = Vector2D(calc_pos[0], calc_pos[1])

            self.old_pos = self.pos

    def constrain(self):
        fast_out = _calc_verlet_vertex_constraints((self.pos.x, self.pos.y), (self.size.x, self.size.y), self.radius)
        x, y = fast_out
        self.pos.x, self.pos.y = x, y

    def draw(self, win: pygame.Surface, color: tuple, show_forces=False):
        pygame.draw.circle(win, color, (self.pos.x, self.pos.y), self.radius)
        if show_forces:
            pygame.draw.line(win, (255, 0, 0), (self.pos.x, self.pos.y), (self.pos.x + self.vel.x * self.vel.magnitude, self.pos.y + self.vel.y * self.vel.magnitude))

class VerletJoint:
    def __init__(self, p1: VerletVertex, p2: VerletVertex, length=None):
        self.vert1 = p1
        self.vert2 = p2
        if length:
            self.length = length
        else:
            self.length = math.sqrt((self.vert2.pos.x - self.vert1.pos.x)**2 + (self.vert2.pos.y - self.vert1.pos.y)**2)

    def update(self):
        if self.vert1.pinned:
            vert_1_pin = 1
        else:
            vert_1_pin = 0

        if self.vert2.pinned:
            vert_2_pin = 1
        else:
            vert_2_pin = 0
        vert1, vert2 = _calc_verlet_joint((self.vert1.pos.x, self.vert1.pos.y), (self.vert2.pos.x, self.vert2.pos.y), self.length, (vert_1_pin, vert_2_pin))
        self.vert1.pos = Vector2D(vert1[0], vert1[1])
        self.vert2.pos = Vector2D(vert2[0], vert2[1])
        # dx = self.vert2.pos.x - self.vert1.pos.x
        # dy = self.vert2.pos.y - self.vert1.pos.y
        #
        # distance = math.sqrt(dx**2 + dy**2)
        # difference = (self.length - distance) / distance
        #
        # offset_x = dx * difference * 0.5
        # offset_y = dy * difference * 0.5
        #
        # if self.vert1.pinned is False:
        #     self.vert1.pos.x -= offset_x
        #     self.vert1.pos.y -= offset_y
        #
        # if self.vert2.pinned is False:
        #     self.vert2.pos.x += offset_x
        #     self.vert2.pos.y += offset_y

    def draw(self, win, color):
        pygame.draw.line(win, color, (self.vert1.pos.x, self.vert1.pos.y), (self.vert2.pos.x, self.vert2.pos.y))

class Cloth:
    def __init__(self, sim_size: Vector2D, sim_pos: Vector2D, cloth_size: Vector2D, cloth_spacing: Vector2D,
                 fixed=True, fill=False, gravity=Vector2D(0, 0.98), sim_step=0.5):
        self.sim_size = sim_size
        self.sim_pos = sim_pos
        self.cloth_size = cloth_size
        self.cloth_spacing = cloth_spacing
        self.fixed = fixed
        self.fill = fill
        self.gravity = gravity
        self.sim_step = sim_step

        self.vertices = []
        self.joints = []

        self.gen_vertices()
        self.gen_joints()

    def gen_vertices(self):
        for row in range(int(self.cloth_size.y)):
            row_verts = []
            for char in range(int(self.cloth_size.x)):
                if row == 0 and self.fixed:
                    row_verts.append(VerletVertex(self.sim_size, Vector2D(char * self.cloth_spacing.x, row * self.cloth_spacing.y), self.gravity, self.sim_step, pinned=True))
                else:
                    row_verts.append(VerletVertex(self.sim_size, Vector2D(char * self.cloth_spacing.x, row * self.cloth_spacing.y), self.gravity, self.sim_step))
            self.vertices.append(row_verts)

    def gen_joints(self):
        for Rindex, row in enumerate(self.vertices):
            row_joints = []
            for Cindex, char in enumerate(row):
                if Rindex <= len(self.vertices) and Rindex != 0:
                    row_joints.append(VerletJoint(char, self.vertices[Rindex - 1][Cindex]))

                try:  # I dont even bother
                    row_joints.append(VerletJoint(char, self.vertices[Rindex + 1][Cindex + 1]))
                except IndexError:
                    pass

                try:
                    row_joints.append(VerletJoint(char, row[Cindex+1]))
                except IndexError:
                    pass

            self.joints.append(row_joints)

    def update(self, iterations_in_frame=100):
        for _ in range(iterations_in_frame):
            [[vertex.constrain() for vertex in row] for row in self.vertices]
            [[joint.update() for joint in row] for row in self.joints]

        [[vertex.update() for vertex in row] for row in self.vertices]

    def draw(self, win, color):
        if self.fill is False:
            for row in self.vertices:
                for vertex in row:
                    vertex.draw(win, color)

            for row in self.joints:
                for joint in row:
                    joint.draw(win, color)

        else:
            outer_half_points1 = []
            outer_half_points2 = []
            for Rindex, row in enumerate(self.vertices):
                for Cindex, vertex in enumerate(row):
                    if Rindex == 0:
                        outer_half_points2.append((vertex.pos.x, vertex.pos.y))

                    if Cindex+1 == len(row):
                        outer_half_points2.append((vertex.pos.x, vertex.pos.y))

                    if Cindex == 0:
                        outer_half_points1.append((vertex.pos.x, vertex.pos.y))

                    if Rindex+1 == len(self.vertices):
                        outer_half_points1.append((vertex.pos.x, vertex.pos.y))

            pygame.draw.polygon(win, color, outer_half_points1)
            pygame.draw.polygon(win, color, outer_half_points2)

class Main:
    def __init__(self):
        self.ctx = sprnva.Window((1280, 720), caption='Verlet Integration')
        self.win = self.ctx.create()
        self.cloth = Cloth(Vector2D(1280, 720),  # sim size
                           Vector2D(0, 0),  # sim pos
                           Vector2D(25, 25),  # cloth width & height
                           Vector2D(25, 25),  # cloth x & y spacing
                           sim_step=0.05, fill=False)  # simulation time step

    def update(self):
        while True:
            self.win.fill((0, 0, 0))
            events = self.ctx.get_events()
            keys = self.ctx.get_keys()
            fps = self.ctx.get_fps(integer=True)

            self.cloth.update(16)

            self.cloth.draw(self.win, (255, 255, 255))

            sprnva.TextRenderer(self.win, 25, 25, f'FPS: {fps}', 'Arial', 10, (255, 0, 0))
            self.ctx.update(events)


if __name__ == "__main__":
    Main().update()