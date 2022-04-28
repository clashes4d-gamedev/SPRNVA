import math
import sys
import random
import json

class Main:
    def __init__(self, rgb_values: list):
        self.rgb_values = rgb_values

        with open('colors.json', 'r') as color_info:
            col_dt = color_info.read()
        self.color_groups = json.loads(col_dt)

        for k, v in self.color_groups.items():
            self.color_groups[k] = eval(self.color_groups[k])

        self.color_groups_sorted = self.color_groups.copy()
        for CGk, CGv in self.color_groups_sorted.items():
            self.color_groups_sorted[CGk] = list()

    def dist_rgb(self, color1: tuple, color2: tuple):
        return math.sqrt((color2[0] - color1[0]) ** 2 + (color2[1] - color1[1]) ** 2 + (color2[2] - color1[2]) ** 2)

    def get_dist_to_color(self, org_color: tuple, clist: dict):
        cl_dists = clist.copy()
        for CKey, CValue in cl_dists.items():
            cl_dists[CKey] = self.dist_rgb(CValue, org_color)
        return cl_dists

    def group_colors(self, color_values, color_groups):
        """Groups together given list of colors based on distance in 3D-RGB space.
            Grouped values can be accessed trough the color_groups_sorted variable."""
        for rgbValue in color_values:
            color_dist = self.get_dist_to_color(rgbValue, color_groups)
            act_color = min(color_dist, key=color_dist.get)
            self.color_groups_sorted[act_color].append(rgbValue)