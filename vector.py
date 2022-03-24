import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x + other.x, self.y + other.y)
        return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x * other.x, self.y * other.y)
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x / other.x, self.y / other.y)
        return Vector(self.x / other, self.y / other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return Vector(self.x == other.x, self.y == other.y)
        return Vector(self.x == other, self.y == other)

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            if self.x >= other.x and self.y >= other.y:
                return True
            else:
                return False
        else:
            if self.x >= other and self.y >= other:
                return True
            else:
                return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.x < other.x and self.y < other.y:
                return True
            else:
                return False
        else:
            if self.x < other and self.y < other:
                return True
            else:
                return False

    def len(self):
        return math.sqrt(self.x**2 + self.y**2)

class VectorOperations:
    def __init__(self, ori=Vector(0,0)):
        pass

    def interpolate(self, vec1, vec2, t):
        n_x = vec1.x + (vec2.x - vec1.x) * t
        n_y = vec1.y + (vec2.y - vec1.y) * t
        return Vector(n_x, n_y)

    def dot(self, vec1, vec2):
        return vec1.x * vec2.x + vec1.y * vec2.y

    def len_sqrt(self, vec):
        return math.sqrt(vec.x**2 + vec.y**2)

    def dist_from_vec(self, vec1, vec2):
        dist_1 = self.len_sqrt(vec1)
        dist_2 = self.len_sqrt(vec2)
        return abs(dist_2 - dist_1)

    def rotate_vec(self, vec_trans, vec_ori, angle):
        angle = math.radians(angle)
        n_x = ((vec_trans.x - vec_ori.x) * math.cos(angle)) - ((vec_ori.y - vec_trans.y) * math.sin(angle)) + vec_ori.x
        n_y = vec_ori.y - ((vec_ori.y - vec_trans.y) * math.cos(angle)) + ((vec_trans.x - vec_ori.x) * math.sin(angle))
        return Vector(n_x, n_y)

    def normalize(self, vec):
        return Vector(vec.x/math.sqrt(vec.x**2 + vec.y**2), vec.y/math.sqrt(vec.x**2 + vec.y**2))

    def vec_to_tuple(self, vec):
        return (vec.x, vec.y)

    def tuple_to_vec(self, tuple_in: tuple):
        '''Converts a Tuple with length 2 in a Vector.'''
        if len(tuple_in) == 2:
            return Vector(tuple_in[0], tuple_in[1])
        else:
            return None

    def get_vec_from_point(self, origin, dist):
        return Vector(origin.x, origin.y) + dist
