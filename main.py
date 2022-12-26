from dataclasses import dataclass
import pygame, sys
from pygame.locals import QUIT
import random
import time
from vectors import Pos
from consts import W, H, SCALE
import numpy as np
import agent

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
                0].x > W or self.snake[0].y > H or self.snake[0] in self.snake[1:]:
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

    def get_qstate(self):
        # Create an empty state array
        state = np.empty(0)

        # Add the snake's direction to the array (one-hot encoded)
        if self.direction == UP:
            state = np.append(state, [1, 0, 0, 0])
        elif self.direction == DOWN:
            state = np.append(state, [0, 1, 0, 0])
        elif self.direction == RIGHT:
            state = np.append(state, [0, 0, 1, 0])
        elif self.direction == LEFT:
            state = np.append(state, [0, 0, 0, 1])

        if self.snake[0].x > self.apple.x:
            state = np.append(state, [1, 0, 0])
        elif self.snake[0].x < self.apple.x:
            state = np.append(state, [0, 0, 1])
        elif self.snake[0].x == self.apple.x:
            state = np.append(state, [0, 1, 0])

        if self.snake[0].y > self.apple.y:
            state = np.append(state, [1, 0, 0])
        elif self.snake[0].y < self.apple.y:
            state = np.append(state, [0, 0, 1])
        elif self.snake[0].y == self.apple.y:
            state = np.append(state, [0, 1, 0])

        if self.apple == Pos(self.snake[0].x, self.snake[0].y-1):
            state = np.append(state, [1, 0, 0])
        elif Pos(self.snake[0].x, self.snake[0].y-1) in self.snake:
            state = np.append(state, [0, 1, 0])
        elif self.snake[0].x < 0 or self.snake[0].y-1 < 0 or self.snake[0].x > W or self.snake[0].y-1 > H:
            state = np.append(state, [0, 0, 1])
        else:
            state = np.append(state, [0, 0, 0])
        
        if self.apple == Pos(self.snake[0].x, self.snake[0].y+1):
            state = np.append(state, [1, 0, 0])
        elif Pos(self.snake[0].x, self.snake[0].y+1) in self.snake:
            state = np.append(state, [0, 1, 0])
        elif self.snake[0].x < 0 or self.snake[0].y+1 < 0 or self.snake[0].x > W or self.snake[0].y+1 > H:
            state = np.append(state, [0, 0, 1])
        else:
            state = np.append(state, [0, 0, 0])
        
        if self.apple == Pos(self.snake[0].x+1, self.snake[0].y):
            state = np.append(state, [1, 0, 0])
        elif Pos(self.snake[0].x+1, self.snake[0].y) in self.snake:
            state = np.append(state, [0, 1, 0])
        elif self.snake[0].x+1 < 0 or self.snake[0].y < 0 or self.snake[0].x+1 > W or self.snake[0].y > H:
            state = np.append(state, [0, 0, 1])
        else:
            state = np.append(state, [0, 0, 0])
        
        if self.apple == Pos(self.snake[0].x-1, self.snake[0].y):
            state = np.append(state, [1, 0, 0])
        elif Pos(self.snake[0].x-1, self.snake[0].y) in self.snake:
            state = np.append(state, [0, 1, 0])
        elif self.snake[0].x-1 < 0 or self.snake[0].y < 0 or self.snake[0].x-1 > W or self.snake[0].y > H:
            state = np.append(state, [0, 0, 1])
        else:
            state = np.append(state, [0, 0, 0])


        print(state)
        
        return state

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

example_game = Game()
time_elapsed_since_last_action = 0
clock = pygame.time.Clock()
req_dir = UP

agent = agent.Agent()

running = True

while running:
    delta = clock.tick()
    time_elapsed_since_last_action += delta
    if time_elapsed_since_last_action > 100:
        example_game.direction = req_dir
        time_elapsed_since_last_action = 0
        example_game.display()
        example_game.get_qstate()
        if not example_game.next_step():
            break

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN and event.key in KEY_TO_M.keys():
            if example_game.direction not in KEY_TO_M[event.key]:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    req_dir = UP
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    req_dir = DOWN
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    req_dir = RIGHT
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    req_dir = LEFT
        elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

pygame.quit()
