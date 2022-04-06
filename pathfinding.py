import pygame
from .vector import Vector

class Node:
    def __init__(self, index: int, pos: Vector):
        self.index = index
        self.x = pos.x
        self.y = pos.y

    def get_index(self):
        return self.index

class AStar:
    def __init__(self, start_node: Node.index, goal_node: Node.index, nodes: list):
        self.start_node = start_node
        self.goal_node = goal_node
        self.nodes = nodes

    def g(self, next_node):
        return next_node.index - self.start_node.index

    def h(self, next_node):
        return next_node.index - self.goal_node.index

    def f(self, next_node):
        return self.g(next_node) + self.h(next_node)

    def generate(self):
        open_nodes = self.nodes
        closed_nodes = []

        check_least_f = []
        for node in open_nodes:
            check_least_f.append(self.f(node))

        check_least_f.sort(key=Node.get_index)

        current_node = check_least_f[0]
        open_nodes.remove(current_node)
        closed_nodes.append(current_node)

        if current_node == self.goal_node:
            print('u have found the exit great job')

        chldren_of_current_node = [self.nodes[current_node.index - 1], self.nodes[current_node.index + 1]] # implement top and bottom nodes too

        for child in children_of_current_node:
            if child in closed_nodes:
                continue

            child_g = self.g(current_node) + (child.index - current_node.index)
            child_h = self.h(child)
            child_f = child_g + child_h

            if child in open_nodes:
                for node in open_nodes:
                    if child_g == node:
                        if child_g >= node:
                            continue

                open_nodes.append(child)
