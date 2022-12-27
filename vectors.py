import random
from consts import W, H
import pygame

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
    
    def euq_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

UP = Pos(0, -1)
DOWN = Pos(0, 1)
RIGHT = Pos(1, 0)
LEFT = Pos(-1, 0)

M = [UP, DOWN, RIGHT, LEFT]
KEY_TO_M = {
    pygame.K_w: [UP, DOWN],
    pygame.K_s: [DOWN, UP],
    pygame.K_d: [RIGHT, LEFT],
    pygame.K_a: [LEFT, RIGHT],

    pygame.K_UP: [UP, DOWN],
    pygame.K_DOWN: [DOWN, UP],
    pygame.K_RIGHT: [RIGHT, LEFT],
    pygame.K_LEFT: [LEFT, RIGHT],
}