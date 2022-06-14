import pygame
from os import path

class WatchValue:
    def __init__(self, value: any):
        self.value = value

    def check_change(self, value: any):
        if self.value != value:
            return False
        else:
            return True

class CheckPath:
    def __init__(self, path):
        self.path = path

    def existance(self):
        return path.exists(self.path)

    def isfile(self):
        return path.isfile(self.path)

    def isdir(self):
        return path.isdir(self.path)