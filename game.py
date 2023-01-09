from vectors import *
from consts import *
import numpy as np

class Game:
    def __init__(self, screen): 
        self.width = W
        self.height = H
        self.apple = Pos()
        self.apple.random_pos()
        self.snake = [Pos(int(W / 2), int(H / 2)), 
                      Pos(int(W / 2), int(H / 2)+1), 
                      Pos(int(W / 2), int(H / 2)+2)]
        self.apple_counter = 0
        self.direction = UP
        self.score = 0
        self.step_counter = 0
        self.screen = screen

    def next_step(self): # Returns (reward, everything alright?, score)
        reward = 0
        self.step_counter += 1
        self.apple_counter += 1

        self.snake.insert(0, self.snake[0] + self.direction)
        if self.snake[0].x < 0 or self.snake[0].y < 0 or self.snake[
                0].x >= W or self.snake[0].y >= H or self.snake[0] in self.snake[1:] or self.apple_counter > 25:
            reward = -10
            return (reward, False, self.score)
        if self.snake[0] == self.apple:
            # Wąż się nie kurczy!
            # Wylosuj nową pozycję dla jabłka
            self.score += 1
            reward += 10
            self.apple.random_pos()
            self.apple_counter = 0
            # Póki wylosowana wartość jest "w" wężu, losuj znowu
            while self.apple in self.snake:
                self.apple.random_pos()
        else:
            self.snake.pop()
        return (reward, True, self.score)

    def display(self):
        self.screen.fill((0, 0, 0))

        pygame.draw.rect(
            self.screen, (255, 0, 0),
            pygame.Rect(self.apple.x * SCALE, self.apple.y * SCALE, SCALE,
                        SCALE))

        for element in self.snake:
            pygame.draw.rect(
                self.screen, (0, 255, 0),
                pygame.Rect(element.x * SCALE, element.y * SCALE, SCALE,
                            SCALE))

        pygame.display.flip()

    def get_field(self, pos):
        # 1 - Apple
        # 2 - Snake
        # 3 - Out of bounds
        if self.apple == pos:
            return 1
        elif pos in self.snake:
            return 2
        elif pos.x < 0 or pos.x >= W or pos.y < 0 or pos.y >= H:
            return 3
        return 0

    def get_qstate(self):
        # Create an empty state array
        state = np.empty(0)
        clockwise = [UP, RIGHT, DOWN, LEFT]
        cnt = 0
        if self.direction == UP:
            cnt = 0
        elif self.direction == RIGHT:
            cnt = 1
        elif self.direction == DOWN:
            cnt = 2
        elif self.direction == LEFT:
            cnt = 3
        
        fwd = clockwise[cnt%4]
        right = clockwise[(cnt+1)%4]
        left = clockwise[(cnt+3)%4]

        '''if fwd == UP:
            state = np.append(state, [
                True, False, False, False,
                
            ])'''
        state = np.append(state, [
            fwd == UP,
            fwd == DOWN,
            fwd == RIGHT,
            fwd == LEFT
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
            self.snake[0].x < 0 or self.snake[0].y-1 < 0 or self.snake[0].x >= W or self.snake[0].y-1 >= H
        ])

        state = np.append(state, [
            self.apple == Pos(self.snake[0].x, self.snake[0].y+1),
            Pos(self.snake[0].x, self.snake[0].y+1) in self.snake,
            self.snake[0].x < 0 or self.snake[0].y+1 < 0 or self.snake[0].x >= W or self.snake[0].y+1 >= H
        ])
        
        state = np.append(state, [
            self.apple == Pos(self.snake[0].x+1, self.snake[0].y),
            Pos(self.snake[0].x+1, self.snake[0].y) in self.snake,
            self.snake[0].x+1 < 0 or self.snake[0].y < 0 or self.snake[0].x+1 >= W or self.snake[0].y >= H
        ])

        state = np.append(state, [
            self.apple == Pos(self.snake[0].x-1, self.snake[0].y),
            Pos(self.snake[0].x-1, self.snake[0].y) in self.snake,
            self.snake[0].x-1 < 0 or self.snake[0].y < 0 or self.snake[0].x-1 >= W or self.snake[0].y >= H
        ])
        return state.reshape((1, 22))
