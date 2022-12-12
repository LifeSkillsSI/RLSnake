import pygame, sys
from pygame.locals import QUIT
import random
import time
from vectors import Pos
from consts import W, H, SCALE

pygame.init()
SCREEN = pygame.display.set_mode([W * SCALE, H * SCALE])



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

        pygame.draw.rect(
            SCREEN, (255, 0, 0),
            pygame.Rect(self.apple.x * SCALE, self.apple.y * SCALE, SCALE,
                        SCALE))

        for element in self.snake:
            pygame.draw.rect(
                SCREEN, (0, 255, 0),
                pygame.Rect(element.x * SCALE, element.y * SCALE, SCALE,
                            SCALE))

        pygame.display.flip()


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
}

example_game = Game()

while True:
    example_game.display()
    if not example_game.next_step():
        break
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
          if example_game.direction not in KEY_TO_M[event.key]:
            if event.key == pygame.K_w:
              example_game.direction = UP
            elif event.key == pygame.K_s:
              example_game.direction = DOWN
            elif event.key == pygame.K_d:
              example_game.direction = RIGHT
            elif event.key == pygame.K_a:
              example_game.direcion = LEFT
    time.sleep(0.1)
pygame.quit()

# https://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
