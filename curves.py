import math
from .vector import Vector, VectorOperations

class QuadraticBezier:
    def __init__(self, p0: Vector, p1: Vector, p2: Vector, t:float):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.t = t
        self.curr_x = (1 - self.t)**2 * self.p0.x + 2 * self.t * (1 - self.t) * self.p1.x + self.t**2 * self.p2.x
        self.curr_y = (1 - self.t)**2 * self.p0.y + 2 * self.t * (1 - self.t) * self.p1.y + self.t**2 * self.p2.y
        self.curve = Vector(self.curr_x, self.curr_y)

    def get_points(self, step_size_mod):
        curve_points = []
        for i in range(int(self.t)):
            curve = QuadraticBezier(self.p0, self.p1, self.p2, i * step_size_mod).curve
            curve_points.append(curve)
        return curve_points

    def get_points_as_tuple(self, step_size_mod):
        curve_points = []
        for i in range(int(self.t)):
            curve = QuadraticBezier(self.p0, self.p1, self.p2, i * step_size_mod).curve
            curve_points.append(VectorOperations().vec_to_tuple(curve))
        return curve_points

class CubicBezier:
    def __init__(self, p0: Vector, p1: Vector, p2: Vector, p3: Vector, t: float):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.t = t
        self.curr_x = (1 - self.t)**3 * self.p0.x + 3 * self.t * (1 - self.t)**2 * self.p1.x + 3 * self.t**2 * (1 - self.t) * self.p2.x + self.t**3 * self.p3.x
        self.curr_y = (1 - self.t)**3 * self.p0.y + 3 * self.t * (1 - self.t)**2 * self.p1.y + 3 * self.t**2 * (1 - self.t) * self.p2.y + self.t**3 * self.p3.y
        self.curve = Vector(self.curr_x, self.curr_y)
        #print(self.curve)

    def get_points(self, step_size_mod):
        curve_points = []
        for i in range(int(self.t)):
            curve = CubicBezier(self.p0, self.p1, self.p2, self.p3, i * step_size_mod).curve
            curve_points.append(curve)
        return curve_points

    def get_points_as_tuple(self, step_size_mod):
        curve_points = []
        for i in range(int(self.t)):
            curve = CubicBezier(self.p0, self.p1, self.p2, self.p3, i * step_size_mod).curve
            curve_points.append(VectorOperations().vec_to_tuple(curve))
        #print(curve_points)
        return curve_points

class CurveOperations:
    def __init__(self) -> None:
        pass

    def p_on_circle(self, vec: Vector, radius: int, angle: float) -> Vector:
        angle = math.radians(angle)
        x = radius * math.cos(angle) + vec.x
        y = radius * math.sin(angle) + vec.y
        return Vector(x, y)

    def gen_points_on_circle(self, center: Vector, radius: int, num_points: int, spacing=0) -> list:
        point_list = []
        num_deg = 0
        for point in range(num_points):
            if num_deg != num_points:
                poc = self.p_on_circle(center, radius, num_deg + spacing)
                point_list.append(poc)
                num_deg += 1
            
        return point_list
