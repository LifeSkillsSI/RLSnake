import pygame, sys
from pygame.locals import QUIT
import random
import time

W = 100 # "Logiczna" szerokość
H = 100 # "Logiczna" wysokość
SCALE = 4 # Skala ekran-logika

pygame.init()
SCREEN = pygame.display.set_mode([W*SCALE, H*SCALE])

class Pos:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def random_pos(self):
        self.x = random.randint(0, W)
        self.y = random.randint(0, H)

    def __add__(self, o):
      return Pos(self.x + o.x, self.y + o.y)

    def __eq__(self, other):
      return self.x == other.x and self.y == other.y


class Game:
    def __init__(self):
        self.width = W
        self.height = H
        self.apple = Pos()
        self.apple.random_pos()
        self.snake = [Pos(int(W / 2), int(H / 2))]
        self.direction = M[random.randint(0, 3)]

    def next_step(self):
        self.snake.insert(0, self.snake[0] + self.direction)
        if self.snake[0].x < 0 or self.snake[0].y < 0 or self.snake[
                0].x > W or self.snake[0].y > H:
            return False
        if self.snake[0] == self.apple:
            # Wąż się nie kurczy!
            # Wylosuj nową pozycję dla jabłka
            self.apple.random_pos()
            # Póki wylosowana wartość jest "w" wężu, losuj znowu
            while self.apple in self.snake:
                self.apple.random_pos()
        else:
            self.snake.pop()
        return True
    
    def display(self):
        SCREEN.fill((0, 0, 0))

        pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(self.apple.x*SCALE, self.apple.y*SCALE, SCALE, SCALE))

        for element in self.snake:
            pygame.draw.rect(SCREEN, (0, 255, 0), pygame.Rect(element.x*SCALE, element.y*SCALE, SCALE, SCALE))


        pygame.display.flip()

UP = Pos(0, -1)
DOWN = Pos(0, 1)
RIGHT = Pos(1, 0)
LEFT = Pos(-1, 0)

M = [UP, DOWN, RIGHT, LEFT]

example_game = Game()

while True:
  example_game.display()
  if not example_game.next_step():
    break
  time.sleep(0.1)
pygame.quit()
