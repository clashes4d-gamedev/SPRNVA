from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import pygame
import pygame.gfxdraw
import SPRNVA as sprnva
from numba import jit
from SPRNVA import Vector2D

@jit(nopython=True, fastmath=True)
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

    output_pos = (x, y)
    return output_pos


@jit(nopython=True, fastmath=True)
def _calc_verlet_vertex_position(pos, vel, acc, size_y, radius, vel_magnitude, coll_friction):
    curr_vel_x = vel[0]
    curr_vel_y = vel[0]
    if pos[1] + radius >= size_y and (curr_vel_x ** 2) + (curr_vel_y ** 2) > 0.00001:
        curr_vel_x /= vel_magnitude
        curr_vel_y /= vel_magnitude

        curr_vel_x *= vel_magnitude * coll_friction
        curr_vel_y *= vel_magnitude * coll_friction

    pos = (pos[0] + curr_vel_x + acc[0], pos[1] + curr_vel_y + acc[1])

    return pos


@jit(nopython=True, fastmath=True)
def _calc_verlet_joint(vert1_pos, vert2_pos, length, mass, vert_pin, stiffness):
    dx = vert2_pos[0] - vert1_pos[0]
    dy = vert2_pos[1] - vert1_pos[1]

    distance = (dx ** 2 + dy ** 2) ** (1 / 2)
    difference = ((length - distance) / distance) / stiffness

    offset_x = dx * difference * 0.5
    offset_y = dy * difference * 0.5

    m1 = mass[0] + mass[1]
    m2 = mass[0] / m1

    m1 = mass[1] / m1

    if vert_pin[0] == 0:
        vert1_endpos_x = vert1_pos[0] - offset_x * m1
        vert1_endpos_y = vert1_pos[1] - offset_y * m1
    else:
        vert1_endpos_x = vert1_pos[0]
        vert1_endpos_y = vert1_pos[1]

    if vert_pin[1] == 0:
        vert2_endpos_x = vert2_pos[0] + offset_x * m2
        vert2_endpos_y = vert2_pos[1] + offset_y * m2

    else:
        vert2_endpos_x = vert2_pos[0]
        vert2_endpos_y = vert2_pos[1]

    return (vert1_endpos_x, vert1_endpos_y), (vert2_endpos_x, vert2_endpos_y)


# Precompiles gpu functions with dummy values
_calc_verlet_joint((1, 1), (2, 2), 1, (1, 1), (0, 0), 1)
_calc_verlet_vertex_constraints((1, 1), (1, 1), 1)
_calc_verlet_vertex_position((1, 1), (1, 1), (1, 1), 1, 1, 1, 1)


class VerletVertex:
    def __init__(self, size: Vector2D, pos: Vector2D, acc: Vector2D, dt: float, mass=1.0, radius=1, coll_friction=0.75,
                 pinned=False) -> None:
        """Generates a VerletVertex at given Coordinates with a constant acceleration."""
        self.size = size
        self.pos = pos
        self.acc = acc
        self.dt = dt
        self.radius = radius
        self.pinned = pinned
        self.coll_friction = coll_friction
        self.old_pos = self.pos
        self.mass = mass
        self.vel = self.acc

    def update(self) -> None:
        """Updates the Position and Velocity of the Vertex."""
        if self.pinned is False:
            self.vel = self.pos - self.old_pos
            calc_pos = _calc_verlet_vertex_position((self.pos.x, self.pos.y), (self.vel.x, self.vel.y),
                                                    (self.acc.x, self.acc.y), self.size.y, self.radius,
                                                    self.vel.magnitude, self.coll_friction)
            self.pos = Vector2D(calc_pos[0], calc_pos[1])

            self.old_pos = self.pos

    def constrain(self) -> None:  # In a game with a play-area larger than the screen, this may not be needed
        """Constrains the Vertex inside the given area."""
        self.pos.x, self.pos.y = _calc_verlet_vertex_constraints((self.pos.x, self.pos.y),
                                                                 (self.size.x, self.size.y), self.radius)

    def draw(self, win: pygame.Surface, color: tuple, show_forces=False, antialiasing=False) -> None:
        """Draws the Vertex at the given Coordinates."""
        if antialiasing:
            pygame.gfxdraw.aacircle(win, int(self.pos.x), int(self.pos.y), self.radius, color)
        else:
            pygame.draw.circle(win, color, (self.pos.x, self.pos.y), self.radius)
        if show_forces:
            pygame.draw.line(win, (255, 0, 0), (self.pos.x, self.pos.y), (self.pos.x + self.vel.x * self.vel.magnitude,
                                                                          self.pos.y + self.vel.y * self.vel.magnitude))


class VerletJoint:
    def __init__(self, p1: VerletVertex, p2: VerletVertex, length=None, stiffness=1) -> None:
        """Generates a joint between two VerletVertices."""
        self.vert1 = p1
        self.vert2 = p2
        self.vert_1_pin = 1 if self.vert1.pinned else 0
        self.vert_2_pin = 1 if self.vert2.pinned else 0

        self.length = length if length else ((self.vert2.pos.x - self.vert1.pos.x) ** 2 + (self.vert2.pos.y - self.vert1.pos.y)**2)**(1/2)
        self.stiffness = stiffness

    def update(self) -> None:
        """Updates the Joint."""

        vert1, vert2 = _calc_verlet_joint((self.vert1.pos.x, self.vert1.pos.y), (self.vert2.pos.x, self.vert2.pos.y),
                                          self.length, (self.vert1.mass, self.vert2.mass),
                                          (self.vert_1_pin, self.vert_2_pin), self.stiffness)
        self.vert1.pos = Vector2D(vert1[0], vert1[1])
        self.vert2.pos = Vector2D(vert2[0], vert2[1])

    def draw(self, win: pygame.Surface, color: tuple, antialiasing=False) -> None:
        """Draws the Joint to given Surface"""
        if antialiasing:
            pygame.draw.aaline(win, color, (self.vert1.pos.x, self.vert1.pos.y), (self.vert2.pos.x, self.vert2.pos.y))
        else:
            pygame.draw.line(win, color, (self.vert1.pos.x, self.vert1.pos.y), (self.vert2.pos.x, self.vert2.pos.y))


class VerletCloth:
    def __init__(self, sim_size=Vector2D(50, 50), sim_pos=Vector2D(50, 50), cloth_size=Vector2D(1, 1),
                 cloth_spacing=Vector2D(1, 1),
                 mass=1, tearing_threshold=0, fixed=True, fill=False, acceleration=Vector2D(0, 0.98), sim_step=0.5,
                 cloth_dict=None, stiffness=1):

        """Generates a square piece of Cloth using Verlet-Integration if cloth_dict is not specified.\n
            Note: Tearing currently doesnt work with the fill argument."""

        cloth_dict = {} if cloth_dict is None else cloth_dict

        self.sim_size = sim_size
        self.sim_pos = sim_pos
        self.cloth_size = cloth_size
        self.cloth_spacing = cloth_spacing
        self.fixed = fixed
        self.cloth_dict = cloth_dict
        self.stiffness = stiffness

        self.mass = mass


        self.tearing_threshold = tearing_threshold
        self.tearing = False if self.tearing_threshold == 0 or self.tearing_threshold <= 0 else True

        self.fill = fill
        self.acceleration = acceleration
        self.sim_step = sim_step
        self.gravity = True if not self.acceleration <= Vector2D(0, 0) else False

        self.vertices = []
        self.joints = []

        if self.cloth_dict != {}:
            [self.vertices.append(row) for row in self.cloth_dict['VERTICES']]

            for row in self.cloth_dict['JOINTS']:
                joint_row = [VerletJoint(row[0], row[1])]
                self.joints.append(joint_row)

        else:
            self.gen_vertices()
            self.gen_joints()

    def set_acceleration(self, new_acc: Vector2D):
        """Sets a constant Acceleration for the Cloth-Simulation."""
        self.acceleration = new_acc
        for row in self.vertices:
            for vertex in row:
                vertex.acc = self.acceleration

    def set_simpos(self, new_pos: Vector2D):
        """Sets the Position of the entire Cloth-Simulation."""
        for index, row in enumerate(self.vertices):
            if index == 0:
                for Vindex, vertex in enumerate(row):
                    vertex.pos = Vector2D(new_pos.x + self.cloth_spacing.x * Vindex, new_pos.y)

    def gen_vertices(self):
        """Generates Cloth-Vertices."""
        self.vertices = []
        for row in range(int(self.cloth_size.y)):
            row_verts = []
            for char in range(int(self.cloth_size.x)):
                if row == 0 and self.fixed:
                    row_verts.append(VerletVertex(self.sim_size,
                                                  Vector2D(self.sim_pos.x + (char * self.cloth_spacing.x),
                                                           self.sim_pos.y + (row * self.cloth_spacing.y)),
                                                  self.acceleration, self.sim_step, pinned=True))
                else:
                    row_verts.append(VerletVertex(self.sim_size,
                                                  Vector2D(self.sim_pos.x + (char * self.cloth_spacing.x),
                                                           self.sim_pos.y + (row * self.cloth_spacing.y)),
                                                  self.acceleration, self.sim_step, mass=self.mass))
            self.vertices.append(row_verts)

    def gen_joints(self) -> None:
        """Generates Connections between Cloth-Vertices."""
        self.joints = []
        for Rindex, row in enumerate(self.vertices):
            row_joints = []
            for Cindex, char in enumerate(row):
                if Rindex <= len(self.vertices) and Rindex != 0:
                    row_joints.append(VerletJoint(char, self.vertices[Rindex - 1][Cindex], stiffness=self.stiffness))

                #if self.triangulated:
                #    try:  # I dont even bother
                #        row_joints.append(VerletJoint(char, self.vertices[Rindex + 1][Cindex + 1]))
                #    except IndexError:
                #        pass

                    #try:  # I dont even bother
                    #    if Rindex <= len(self.vertices) and Rindex != 0:
                    #        if Cindex >= 0 and Cindex <= len(row)-1:
                    #            row_joints.append(VerletJoint(char, self.vertices[Rindex - 1][Cindex - 1]))
                    #except IndexError:
                    #    pass

                try:
                    row_joints.append(VerletJoint(char, row[Cindex + 1]))
                except IndexError:
                    pass

            self.joints.append(row_joints)

    #@jit
    def update(self, iterations_in_frame=1) -> None:
        """Updates the Cloth-Simulation n times a Frame.\n
         n = iterations_in_frame
            if this is not set, the Cloth-Simulation will be updated once per Frame."""
        for _ in range(iterations_in_frame):
            for Jrow, Vrow in zip(self.joints, self.vertices):
                if self.gravity:
                    for vertex in Vrow:
                        vertex.update()

                for index, joint in enumerate(Jrow):
                    joint.update()
                    if self.tearing:
                        dst = joint.vert1.pos.dist(joint.vert2.pos)
                        if dst > self.tearing_threshold:
                            Jrow.pop(index)

    def draw(self, win: pygame.Surface, color: tuple, antialiasing=False) -> None:
        """Draws the Cloth-Simulation on given Surface."""
        win_size = Vector2D(win.get_width(), win.get_height())
        if self.fill:
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

            if antialiasing:
                pygame.draw.polygon(win, color, outer_half_points1)
                pygame.draw.polygon(win, color, outer_half_points2)

                for index, point in enumerate(outer_half_points1):
                    try:
                        pygame.draw.aaline(win, color, (point[0] - 1, point[1] - 1), (outer_half_points1[index + 1][0] - 1, outer_half_points1[index + 1][1] - 1))
                    except IndexError:
                        pass

                for index, point in enumerate(outer_half_points2):
                    try:
                        pygame.draw.aaline(win, color, (point[0] - 1, point[1] - 1), (outer_half_points2[index + 1][0] - 1, outer_half_points2[index + 1][1] - 1))
                    except IndexError:
                        pass
            else:
                pygame.draw.polygon(win, color, outer_half_points1)
                pygame.draw.polygon(win, color, outer_half_points2)

        else:

            for row in self.vertices:
                for vertex in row:
                    if vertex.pos <= win_size:
                        vertex.draw(win, color, antialiasing=antialiasing)

            for row in self.joints:
                for joint in row:
                    if joint.vert2.pos - joint.vert1.pos <= win_size:
                        joint.draw(win, color, antialiasing=antialiasing)


class VerletRope:
    def __init__(self, sim_size=Vector2D(50, 50), sim_pos=Vector2D(50, 50), segments=5, seg_length=20, mass=1,
                 tearing_threshold=0, pinned=True, acceleration=Vector2D(0, 0.98), sim_step=0.5,) -> None:
        """Generates a 1D Cloth-Simulation witch represents a Rope."""
        # Cant i just use super().__init__() ?
        self.sim_size = sim_size
        self.sim_pos = sim_pos
        self.segments = segments
        self.seg_length = seg_length
        self.mass = mass
        self.tearing_threshold = tearing_threshold
        self.pinned = pinned
        self.acceleration = acceleration
        self.sim_step = sim_step

        self.rope_sim = VerletCloth(self.sim_size, self.sim_pos, Vector2D(1, self.segments), Vector2D(0, self.seg_length),
                              self.mass, self.tearing_threshold, self.pinned, False, self.acceleration, self.sim_step,
                              triangulated=False)

    def get_rope(self) -> VerletCloth:
        """Returns Rope Object."""
        return self.rope_sim

class VerletBox:
    def __init__(self, sim_size=Vector2D(1280, 720), sim_pos=Vector2D(50, 50), size=Vector2D(50, 50), mass=1, pinned=False,
                 acceleration=Vector2D(0, 0.98), friction=0.75, sim_step=0.5, fill=False, triangulated=True):
        """Generates a Box with physics."""
        self.sim_size = sim_size
        self.size = size
        self.sim_pos = sim_pos
        self.mass = mass
        self.pinned = pinned
        self.acceleration = acceleration
        self.friction = friction
        self.sim_step = sim_step
        self.fill = fill
        self.triangulated = triangulated

        self.vertices = []
        self.joints = []

        for y in range(2):
            row = []
            for x in range(2):
                row.append(VerletVertex(self.sim_size, Vector2D(self.sim_pos.x * (x + 1), self.sim_pos.y * (y + 1)),
                                        self.acceleration, self.sim_step, self.mass, 1, self.friction, self.pinned))
            self.vertices.append(row)

        self.joints = []
        for Rindex, row in enumerate(self.vertices):
            row_joints = []
            for Cindex, char in enumerate(row):
                if Rindex <= len(self.vertices) and Rindex != 0:
                    row_joints.append(VerletJoint(char, self.vertices[Rindex - 1][Cindex]))

                if self.triangulated:
                    try:  # I dont even bother
                        row_joints.append(VerletJoint(char, self.vertices[Rindex + 1][Cindex + 1]))
                    except IndexError:
                        pass

                    try:  # I dont even bother
                        row_joints.append(VerletJoint(char, self.vertices[Rindex - 1][Cindex - 1]))
                    except IndexError:
                        pass

                try:
                    row_joints.append(VerletJoint(char, row[Cindex + 1]))
                except IndexError:
                    pass

            self.joints.append(row_joints)

    def update(self, iterations_in_frame=1) -> None:
        """Updates the Box."""
        for _ in range(iterations_in_frame):
            for row in self.joints:
                for index, joint in enumerate(row):
                    joint.update()

            for row in self.vertices:
                for index, vertex in enumerate(row):
                    vertex.constrain()
                    vertex.update()

    def draw(self, win, color, antialiasing=False) -> None:
        """Draws the Box."""
        win_size = Vector2D(win.get_width(), win.get_height())
        if self.fill:
            outer_half_points1 = [(self.vertices[0][0].pos.x, self.vertices[0][0].pos.y),
                                  (self.vertices[0][1].pos.x, self.vertices[0][1].pos.y),
                                  (self.vertices[1][1].pos.x, self.vertices[1][1].pos.y)]

            outer_half_points2 = [(self.vertices[0][0].pos.x, self.vertices[0][0].pos.y),
                                  (self.vertices[1][0].pos.x, self.vertices[1][0].pos.y),
                                  (self.vertices[1][1].pos.x, self.vertices[1][1].pos.y)]

            if antialiasing:
                pygame.draw.polygon(win, color, outer_half_points1)
                pygame.draw.polygon(win, color, outer_half_points2)

                for index, point in enumerate(outer_half_points1):
                    try:
                        pygame.draw.aaline(win, color, (point[0] - 1, point[1] - 1), (outer_half_points1[index + 1][0] - 1, outer_half_points1[index + 1][1] - 1))
                    except IndexError:
                        pass

                for index, point in enumerate(outer_half_points2):
                    try:
                        pygame.draw.aaline(win, color, (point[0] - 1, point[1] - 1), (outer_half_points2[index + 1][0] - 1, outer_half_points2[index + 1][1] - 1))
                    except IndexError:
                        pass
            else:
                pygame.draw.polygon(win, color, outer_half_points1)
                pygame.draw.polygon(win, color, outer_half_points2)

        else:

            for row in self.vertices:
                for vertex in row:
                    if vertex.pos <= win_size:
                        vertex.draw(win, color, antialiasing=antialiasing)

            for row in self.joints:
                for joint in row:
                    if joint.vert2.pos - joint.vert1.pos <= win_size:
                        joint.draw(win, color, antialiasing=antialiasing)

    def set_acceleration(self, new_acc: Vector2D) -> None:
        """Sets a constant acceleration."""
        self.acceleration = new_acc
        for row in self.vertices:
            for vertex in row:
                vertex.acc = self.acceleration

    def set_simpos(self, new_pos: Vector2D) -> None:
        """Sets the position of the simulation position."""
        self.vertices[0][0].pos = Vector2D(new_pos.x, new_pos.y)
