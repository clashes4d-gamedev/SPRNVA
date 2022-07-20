import random
import math
from .vector import Vector2D

class Room2D:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = ((self.x, self.y), (self.x, self.y + self.height))
        self.right = ((self.x + self.width, self.y), (self.x + self.width, self.y + self.height))
        self.top = ((self.x, self.y), (self.x + self.width, self.y))
        self.bottom = ((self.x, self.y + self.height), (self.x + self.width, self.y + self.height))
        self.rect = (self.left, self.right, self.top, self.bottom)
        self.center = (self.width//2 + self.x, self.height//2 + self.y)

    def overlaps(self, room):
        if self.rect <= room.rect:
            return True
        else:
            return False

    def __repr__(self):
        return f'Room2D(x: {self.x}, y: {self.y}, width: {self.width}, height: {self.height})'


class TKBased:
    def __init__(self, size: tuple[int, int], tile_size: int, max_rooms: int = 20,
                 min_room_size: tuple[int, int] = (5, 5), max_room_size: tuple[int, int] = (10, 10)):
        #self.grid = []
        self.size = size
        self.tile_size = tile_size

        self.max_room_size = max_room_size
        self.min_room_size = min_room_size
        self.max_rooms = max_rooms

        self.rooms = self.generate_rooms()
        self.seperate_rooms()
        self.main_rooms = self.pick_main_rooms()
        self.triangulate_main_rooms()


        #for row in range(self.size[1]):
        #    curr_row = []
        #    for cell in range(self.size[0]):
        #        curr_row.append('0')
        #    self.grid.append(curr_row)

    def cross_product(self, p1: tuple, p2: tuple, p3: tuple):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    def area_of_triangle(self, trip0: tuple[int, int], trip1: tuple[int, int], trip2: tuple[int, int]):
        return abs((trip0[0] * (trip1[1] - trip2[1]) + trip1[0] * (trip2[1] - trip0[1]) + trip2[0] * (trip0[1] - trip1[1])) / 2)

    def point_in_triangle(self, trip0: tuple[int, int], trip1: tuple[int, int], trip2: tuple[int, int], main_p: tuple[int, int]):
        A = self.area_of_triangle(trip0, trip1, trip2)
        A1 = self.area_of_triangle(main_p, trip1, trip2)
        A2 = self.area_of_triangle(trip0, main_p, trip2)
        A3 = self.area_of_triangle(trip0, trip1, main_p)

        if A == A1 + A2 + A3:
            return True
        else:
            return False

    def get_convex_hull(self, points: list[tuple[int, int]]):
        if len(points) >= 2:
            convex_hull = []

            def find_hull(sk: list[tuple[int, int]], p0: tuple[int, int], p1: tuple[int, int]):
                if len(sk) == 0:
                    return
                else:
                    farthest_point = min([(self.cross_product(p0, p1, point), point) for point in sk])[1]
                    if farthest_point not in convex_hull:
                        convex_hull.insert(convex_hull.index(p0) + 1, farthest_point)
                    S1 = []
                    S2 = []
                    for point in sk:
                        if self.point_in_triangle(p0, farthest_point, p1, point):
                            continue
                        else:
                            if self.cross_product(p0, farthest_point, point) < 0:
                                S1.append(point)

                            if self.cross_product(farthest_point, p1, point) < 0:
                                S2.append(point)

                    find_hull(S1, p0, farthest_point)
                    find_hull(S2, farthest_point, p1)


            left_side = []
            right_side = []
            left_most_point = min(points)
            right_most_point = max(points)

            convex_hull.append(left_most_point)
            convex_hull.append(right_most_point)

            for point in points:
                if point == left_most_point or point == right_most_point:
                    continue
                else:
                    check_side = self.cross_product(left_most_point, right_most_point, point)
                    if check_side < 0:
                        right_side.append(point)

                    else:
                        if check_side > 0:
                            left_side.append(point)

                    find_hull(right_side, left_most_point, right_most_point)
                    find_hull(left_side, right_most_point, left_most_point)

            return convex_hull
        else:
            return

    def triangulate_main_rooms(self):
        room_centers = [room.center for room in self.main_rooms]
        convex_hull = self.get_convex_hull(room_centers)

        print(room_centers, '\n', convex_hull)

    def pick_main_rooms(self, size_threshold: float = 0.75):
        main_rooms = []
        for room in self.rooms:
            if room.width >= (self.max_room_size[0] * size_threshold) and room.width >= (self.max_room_size[0] * size_threshold):
                main_rooms.append(room)
        return main_rooms

    def seperate_rooms(self):
        # TODO test if this actually works
        c = self.get_bounding_box(self.rooms).center
        for room in self.rooms:
            next_room = self.rooms[self.rooms.index(room)-1]
            if room.overlaps(next_room):
                overlapping_rooms = []
                for temp_room in self.rooms:
                    if temp_room.overlaps(room):
                        overlapping_rooms.append(temp_room)

                overlapping_rooms_center = self.get_bounding_box(overlapping_rooms).center

                dist_center_overlapping_rooms = Vector2D(overlapping_rooms_center[0], overlapping_rooms_center[1]) - Vector2D(room.center[0], room.center[1])
                dist_center_rooms = Vector2D(c[0], c[1]) - Vector2D(room.center[0], room.center[1])

                move_vec = dist_center_overlapping_rooms + dist_center_rooms
                room.x -= move_vec.x
                room.y -= move_vec.y
                continue
            else:
                pass

    def get_bounding_box(self, rooms: list[Room2D]):
        min_pos = min([(room.x, room.y) for room in rooms])
        max_pos = max([(room.x + room.width, room.y + room.height) for room in rooms])
        bounds = Room2D(min_pos[0], min_pos[1], max_pos[0], max_pos[1])
        return bounds

    def generate_rooms(self):
        rooms = []
        for i in range(self.max_rooms):
            room_pos = self.gen_point_in_circle()
            room_size = (random.randint(self.min_room_size[0], self.max_room_size[0]),
                         random.randint(self.min_room_size[1], self.max_room_size[1]))
            rooms.append(Room2D(room_pos[0], room_pos[1], room_size[0], room_size[1]))
        return rooms

    def gen_point_in_circle(self):
        # TODO replace the 'SPAWN CIRCLE' with a spawn rect or an spawn ellipse
        radius = (self.size[0] + self.size[1]) / 4
        r = radius * (random.random())**(1/2)
        theta = random.random() * 2 * math.pi
        return int(self.size[0]//2 + r * math.cos(theta)), int(self.size[1]//2 + r * math.sin(theta))
