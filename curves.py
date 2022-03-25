import math
import numpy as np
import scipy.interpolate as si
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

class BasisSpline:
    def __init__(self, cv, n=100, degree=3, periodic=False):
        """ Calculate n samples on a bspline

            cv :      Array ov control vertices
            n  :      Number of samples to return
            degree:   Curve degree
            periodic: True - Curve is closed
                      False - Curve is open

            All attributions for this code go to Fnord on Stackoverflow.
        """

        # If periodic, extend the point array by count+degree+1
        cv = np.asarray(cv)
        count = len(cv)

        if periodic:
            factor, fraction = divmod(count + degree + 1, count)
            cv = np.concatenate((cv,) * factor + (cv[:fraction],))
            count = len(cv)
            degree = np.clip(degree, 1, degree)

        # If opened, prevent degree from exceeding count-1
        else:
            degree = np.clip(degree, 1, count - 1)

        # Calculate knot vector
        kv = None
        if periodic:
            kv = np.arange(0 - degree, count + degree + degree - 1, dtype='int')
        else:
            kv = np.concatenate(([0] * degree, np.arange(count - degree + 1), [count - degree] * degree))

        # Calculate query range
        u = np.linspace(periodic, (count - degree), n)

        # Calculate result
        self.points = np.array(si.splev(u, (kv, cv.T, degree))).T

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
