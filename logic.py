from os import path
from typing import Optional

class BinaryTree:
    def __init__(self, data: tuple[int or float, any], layer: int = 0):
        self.left = None
        self.right = None
        self.data = data
        self.layer = layer

    def add_node(self, data: tuple[int or float, any]):
        if self.data[0]:
            if data[0] < self.data[0]:
                if self.left is None:
                    self.left = BinaryTree(data, layer=self.layer + 1)
                else:
                    self.left.add_node(data)

            elif data[0] > self.data[0]:
                if self.right is None:
                    self.right = BinaryTree(data, layer=self.layer + 1)
                else:
                    self.right.add_node(data)
        else:
            self.data = data

    def show(self):
        if self.left:
            self.left.show()
        print(str(self.data))
        if self.right:
            self.right.show()

    def walk(self):
        pass


class CheckPath:
    def __init__(self, path):
        self.path = path

    def existance(self):
        return path.exists(self.path)

    def isfile(self):
        return path.isfile(self.path)

    def isdir(self):
        return path.isdir(self.path)