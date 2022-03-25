    def draw_catmull_rom_spline(self, points: list, t: float):
        p1 = math.floor(t) + 1
        p2 = p1 + 1
        p3 = p1 + 2
        p0 = p1 - 1

        q1 = -t**3 + 2 * t**2 - t
        q2 = 3 * t**3 - 5* t**2 + 2
        q3 = -3 * t**3 + 4 * t**2 + t
        q4 = t**3 - t**2

        # make this a for loop because there a n points and not just 4
        tx = 0.5 * (self.points[0].x * q1 + self.points[1].x * q2 + self.points[2].x * q3 + self.points[3].x * q4)
        ty = 0.5 * (self.points[0].y * q1 + self.points[1].y * q2 + self.points[2].y * q3 + self.points[3].y * q4)

        return Vector(tx, ty)