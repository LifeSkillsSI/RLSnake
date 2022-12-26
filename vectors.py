import random
from consts import W, H

class Pos:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Pos(self.x + o.x, self.y + o.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def random_pos(self):
        self.x = random.randint(0, W-1)
        self.y = random.randint(0, H-1)
