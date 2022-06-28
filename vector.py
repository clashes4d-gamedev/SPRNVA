import math

class PositionVectorError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.magnitude = self._length()
        self.direction = self._direction()

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x + other.x, self.y + other.y)
        return Vector2D(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x - other.x, self.y - other.y)
        return Vector2D(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x * other.x, self.y * other.y)
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(other.x * self.x, other.y * self.y)
        return Vector2D(other * self.x, other * self.y)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x / other.x, self.y / other.y)
        return Vector2D(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x // other.x, self.y // other.y)
        return Vector2D(self.x // other, self.y // other)

    def __pow__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x ** other.x, self.y ** other.y)
        return Vector2D(self.x ** other, self.y ** other)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __abs__(self):
        return Vector2D(abs(self.x), abs(self.y))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x == other.x, self.y == other.y)
        return Vector2D(self.x == other, self.y == other)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return Vector2D(self.x != other.x, self.y != other.y)
        return Vector2D(self.x != other, self.y != other)

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

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            if self.x > other.x and self.y > other.y:
                return True
            else:
                return False
        else:
            if self.x > other and self.y > other:
                return True
            else:
                return False

    def __le__(self, other):
        if isinstance(other, self.__class__):
            if self.x <= other.x and self.y <= other.y:
                return True
            else:
                return False
        else:
            if self.x <= other and self.y <= other:
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

    def _length(self) -> float:
        """Returns the length of the current Vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def _direction(self) -> float:
        """Returns the Direction in wich the Vector is facing in Radians relative to the X-axis."""
        try:
            return math.atan(self.x / self.y) - math.radians(90)
        except ZeroDivisionError:
            return math.radians(90) - math.radians(90)

    def magsq(self):
        """Returns the squared magnitude of the current Vector."""
        return self.x**2 + self.y**2

    def scale(self, ammount):
        """Scales the current Vector by a Scalar."""
        self.x *= ammount
        self.y *= ammount
        self.magnitude = self._length()

    def normalize(self):
        """Normalizes current Vector to a Unit vector with magnitude of 1."""
        try:
            x = self.x
            y = self.y
            mag_temp = 1 / self.magnitude
            x *= mag_temp
            y *= mag_temp
            #magnitude = round(self._length())  # Round because of floating point errors
            return Vector2D(x, y)

        except ZeroDivisionError:  # this makes sure that the current vector is not the origin vector
            raise PositionVectorError("Cant Normalize Position Vector due to ZeroDivisionError.")

    def dot(self, other) -> float:
        """Returns the dot product of the current Vector with another.
        (Returns the angle between them in Radians.)"""
        return math.acos((self.x * other.x + self.y * other.y)/(self.magnitude * other.magnitude))

    def interpolate(self, other, t):
        """Interpolates between current Vector and given Vector. Returns Vector2D"""
        n_x = self.x + (other.x - self.x) * t
        n_y = self.y + (other.y - self.y) * t
        return Vector2D(n_x, n_y)

    def rotate(self, angle: float):
        """Rotate Vector around a specific angle given in degrees."""
        angle = math.radians(angle)
        self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        self.y = self.x * math.sin(angle) + self.y * math.cos(angle)

    def dist(self, vec2):
        """Returns the Distance between current Vector and given Vector."""
        return ((vec2.y - self.x)**2 + (vec2.y - self.y)**2)**(1/2)

# TODO This is deprecated and will be removed in future releases
class VectorOperations:
    def __init__(self, ori=Vector2D(0,0)):
        pass

    def interpolate(self, vec1, vec2, t):
        n_x = vec1.x + (vec2.x - vec1.x) * t
        n_y = vec1.y + (vec2.y - vec1.y) * t
        return Vector2D(n_x, n_y)

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
        return Vector2D(n_x, n_y)

    def normalize(self, vec):
        return Vector2D(vec.x/math.sqrt(vec.x**2 + vec.y**2), vec.y/math.sqrt(vec.x**2 + vec.y**2))

    def vec_to_tuple(self, vec):
        return (vec.x, vec.y)

    def tuple_to_vec(self, tuple_in: tuple):
        '''Converts a Tuple with length 2 in a Vector2D.'''
        if len(tuple_in) == 2:
            return Vector2D(tuple_in[0], tuple_in[1])
        else:
            return None

    def get_vec_from_point(self, origin, dist):
        return Vector2D(origin.x, origin.y) + dist
