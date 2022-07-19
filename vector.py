import math


class PositionVectorError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Vector2D:
    def __init__(self, x: float, y: float):
        """Creates a 2 Dimensional Vector."""
        self.x = x
        self.y = y
        self.magnitude = self._length()
        self.direction = self._direction()

    def __repr__(self):
        rep = f'Vector2D(x:{self.x}, y:{self.y}, magnitude: {self.magnitude}, direction: {self.direction})'
        return rep

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

    def to_tuple(self):
        """Returns tuple representation of Vector."""
        return self.x, self.y


class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        """Creates a 3 Dimensional Vector. Note: The direction is a Tuple."""
        self.x = x
        self.y = y
        self.z = z
        self.magnitude = self._length()
        self.direction = self._direction()

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        return Vector3D(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        return Vector3D(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)
        return Vector3D(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(other.x * self.x, other.y * self.y, other.z * self.z)
        return Vector3D(other * self.x, other * self.y, other * self.z)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x / other.x, self.y / other.y, self.z / other.z)
        return Vector3D(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x // other.x, self.y // other.y, self.z // other.z)
        return Vector3D(self.x // other, self.y // other, self.z // other)

    def __pow__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        return Vector3D(self.x ** other, self.y ** other, self.z ** other)

    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def __abs__(self):
        return Vector3D(abs(self.x), abs(self.y), abs(self.z))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x == other.x, self.y == other.y, self.z == other.z)
        return Vector3D(self.x == other, self.y == other, self.z == other)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return Vector3D(self.x != other.x, self.y != other.y, self.z != other.z)
        return Vector3D(self.x != other, self.y != other, self.z != other)

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            if self.x >= other.x and self.y >= other.y and self.z >= other.z:
                return True
            else:
                return False
        else:
            if self.x >= other and self.y >= other and self.z >= other:
                return True
            else:
                return False

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            if self.x > other.x and self.y > other.y and self.z > other.z:
                return True
            else:
                return False
        else:
            if self.x > other and self.y > other and self.z > other:
                return True
            else:
                return False

    def __le__(self, other):
        if isinstance(other, self.__class__):
            if self.x <= other.x and self.y <= other.y and self.z <= other.z:
                return True
            else:
                return False
        else:
            if self.x <= other and self.y <= other and self.z <= other:
                return True
            else:
                return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.x < other.x and self.y < other.y and self.z < other.z:
                return True
            else:
                return False
        else:
            if self.x < other and self.y < other and self.z < other:
                return True
            else:
                return False

    def _length(self) -> float:
        """Returns the length of the current Vector."""
        return (self.x**2 + self.y**2 + self.z**2)**(1/2)

    def _direction(self) -> tuple:
        """Returns the Direction in wich the Vector is facing in Radians."""
        return math.radians(math.cos(self.x/self.magnitude)), math.radians(math.cos(self.y/self.magnitude)), math.radians(math.cos(self.z/self.magnitude))

    def magsq(self):
        """Returns the squared magnitude of the current Vector."""
        return self.x**2 + self.y**2 + self.z**2

    def scale(self, ammount):
        """Scales the current Vector by a Scalar."""
        self.x *= ammount
        self.y *= ammount
        self.z *= ammount
        self.magnitude = self._length()

    def normalize(self):
        """Normalizes current Vector to a Unit vector with magnitude of 1."""
        try:
            x = self.x
            y = self.y
            z = self.z
            mag_temp = 1 / self.magnitude
            x *= mag_temp
            y *= mag_temp
            z *= mag_temp
            return Vector3D(x, y, z)

        except ZeroDivisionError:  # this makes sure that the current vector is not the origin vector
            raise PositionVectorError("Cant Normalize Position Vector due to ZeroDivisionError.")

    def dot(self, other) -> float:
        """Returns the dot product of the current Vector with another.
        (Returns the angle between them in Radians.)"""
        return math.acos((self.x * other.x + self.y * other.y + self.z * other.z)/(self.magnitude * other.magnitude))

    def interpolate(self, other, t):
        """Interpolates between current Vector and given Vector. Returns Vector3D"""
        n_x = self.x + (other.x - self.x) * t
        n_y = self.y + (other.y - self.y) * t
        n_z = self.z + (other.z - self.z) * t
        return Vector3D(n_x, n_y, n_z)

    def rotate(self, angle: float, axis: str):
        """Rotate Vector around a specific angle given in degrees. (Valid axes are: x, y, z, X, Y, Z)"""
        valid_axes = ['x', 'y', 'z', 'X', 'Y', 'Z']
        angle = math.radians(angle)

        if axis in valid_axes:
            if axis == 'x' or axis == 'X':
                self.x = self.x
                self.y = self.y * math.cos(angle) - self.z * math.sin(angle)
                self.z = self.y * math.sin(angle) + self.z * math.cos(angle)

            if axis == 'y' or axis == 'Y':
                self.x = self.x * math.cos(angle) + self.z * math.sin(angle)
                self.y = self.y
                self.z = -self.x * math.sin(angle) + self.z * math.cos(angle)

            if axis == 'z' or axis == 'Z':
                self.x = self.x * math.cos(angle) - self.y * math.sin(angle)
                self.y = self.x * math.sin(angle) + self.y * math.cos(angle)
                self.z = self.z

        else:
            raise Exception('Please specify an axis to rotate around. (Valid axes are: x, y, z, X, Y, Z)')

    def dist(self, vec2):
        """Returns the Distance between current Vector and given Vector."""
        return ((vec2.y - self.x)**2 + (vec2.y - self.y)**2 + (vec2.z - self.z)**2)**(1/2)

    def to_tuple(self):
        """Returns tuple representation of Vector."""
        return self.x, self.y, self.z
