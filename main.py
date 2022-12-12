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
        self.score = 0

    def next_step(self):
        self.snake.insert(0, self.snake[0] + self.direction)
        if self.snake[0].x < 0 or self.snake[0].y < 0 or self.snake[
                0].x > W or self.snake[0].y > H:
            return False
        if self.snake[0] == self.apple:
            # Wąż się nie kurczy!
            # Wylosuj nową pozycję dla jabłka
            self.score += 1
            self.apple.random_pos()
            # Póki wylosowana wartość jest "w" wężu, losuj znowu
            print("WOO: " + str(self.score))
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
time_elapsed_since_last_action = 0
clock = pygame.time.Clock()
req_dir = UP

while True:
    delta = clock.tick()
    time_elapsed_since_last_action += delta
    if time_elapsed_since_last_action > 100:
        example_game.direction = req_dir
        time_elapsed_since_last_action = 0
        example_game.display()
        if not example_game.next_step():
            break

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN and event.key in KEY_TO_M.keys():
            if example_game.direction not in KEY_TO_M[event.key]:
                if event.key == pygame.K_w:
                    req_dir = UP
                elif event.key == pygame.K_s:
                    req_dir = DOWN
                elif event.key == pygame.K_d:
                    req_dir = RIGHT
                elif event.key == pygame.K_a:
                    req_dir = LEFT

pygame.quit()

# https://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
