from dataclasses import dataclass
import pygame, sys
from pygame.locals import QUIT
import random
import time
from vectors import *
from consts import *
import numpy as np
from agent import Agent

class Game:
    def __init__(self): # Returns (reward, everything alright?, score)
        self.width = W
        self.height = H
        self.apple = Pos()
        self.apple.random_pos()
        self.snake = [Pos(int(W / 2), int(H / 2)), 
                      Pos(int(W / 2), int(H / 2)+1), 
                      Pos(int(W / 2), int(H / 2)+2)]
        self.direction = UP
        self.score = 0

    def next_step(self):
        reward = 0

        self.snake.insert(0, self.snake[0] + self.direction)
        if self.snake[0].x < 0 or self.snake[0].y < 0 or self.snake[
                0].x > W or self.snake[0].y > H or self.snake[0] in self.snake[1:]:
            reward = -10
            return (reward, False, self.score)
        if self.snake[0] == self.apple:
            # Wąż się nie kurczy!
            # Wylosuj nową pozycję dla jabłka
            self.score += 1
            reward = 10
            self.apple.random_pos()
            # Póki wylosowana wartość jest "w" wężu, losuj znowu
            while self.apple in self.snake:
                self.apple.random_pos()
        else:
            self.snake.pop()
        return (reward, True, self.score)

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
        state = np.append(state, [
            self.direction == UP,
            self.direction == DOWN,
            self.direction == RIGHT,
            self.direction == LEFT
        ])

        state = np.append(state, [
            self.snake[0].x > self.apple.x,
            self.snake[0].x < self.apple.x,
            self.snake[0].x == self.apple.x
        ])

        state = np.append(state, [
            self.snake[0].y > self.apple.y,
            self.snake[0].y < self.apple.y,
            self.snake[0].y == self.apple.y
        ])

        state = np.append(state, [
            self.apple == Pos(self.snake[0].x, self.snake[0].y-1),
            Pos(self.snake[0].x, self.snake[0].y-1) in self.snake,
            self.snake[0].x < 0 or self.snake[0].y-1 < 0 or self.snake[0].x > W or self.snake[0].y-1 > H
        ])

        state = np.append(state, [
            self.apple == Pos(self.snake[0].x, self.snake[0].y+1),
            Pos(self.snake[0].x, self.snake[0].y+1) in self.snake,
            self.snake[0].x < 0 or self.snake[0].y+1 < 0 or self.snake[0].x > W or self.snake[0].y+1 > H
        ])
        
        state = np.append(state, [
            self.apple == Pos(self.snake[0].x+1, self.snake[0].y),
            Pos(self.snake[0].x+1, self.snake[0].y) in self.snake,
            self.snake[0].x+1 < 0 or self.snake[0].y < 0 or self.snake[0].x+1 > W or self.snake[0].y > H
        ])

        state = np.append(state, [
            self.apple == Pos(self.snake[0].x-1, self.snake[0].y),
            Pos(self.snake[0].x-1, self.snake[0].y) in self.snake,
            self.snake[0].x-1 < 0 or self.snake[0].y < 0 or self.snake[0].x-1 > W or self.snake[0].y > H
        ])
        return state



def manual_control():
    game = Game()
    time_elapsed_since_last_action = 0
    clock = pygame.time.Clock()
    req_dir = UP

    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in KEY_TO_M.keys():
                if game.direction not in KEY_TO_M[event.key]:
                    req_dir = KEY_TO_M[event.key][0]
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        delta = clock.tick()
        time_elapsed_since_last_action += delta
        if time_elapsed_since_last_action > 100:
            game.direction = req_dir
            time_elapsed_since_last_action = 0

            (reward, game_alright, score) = game.next_step()
            print(score, reward)
            game.display()
            if not game_alright:
                break

def train():
    game = Game()
    agent = Agent()

    while True:
        current_state = game.get_qstate()
        action = agent.get_action(current_state)

        game.direction = action
        (reward, game_alright, score) = game.next_step()
        game.display()

        new_state = game.get_qstate()
        
        # train short memory

        # append memory
        agent.memory.append((current_state, action, reward, new_state, game_alright))

        if not game_alright:
            game = Game()
            # train long memory


    pass

if __name__ == "__main__":
    option = input("Manual control? (y/n) ")
    pygame.init()
    SCREEN = pygame.display.set_mode([W * SCALE, H * SCALE])
    if option == "y":
        manual_control()
    else:
        train()

    pygame.quit()
