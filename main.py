from dataclasses import dataclass
import pygame
from pygame.locals import QUIT
from train import train
from vectors import *
from consts import *
import numpy as np
from agent import Agent
from game import Game

def manual_control(screen = None):
    game = Game(screen)
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
            game.display()
            print(reward)
            if not game_alright:
                break

def evaluation(model_path = "", screen = None):
    running = True

    game = Game(screen)
    agent = Agent()
    agent.load_model(model_path)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        current_state = game.get_qstate()
        (action, pred) = agent.get_action(current_state)

        game.direction = action
        (reward, game_alright, score) = game.next_step()
        game.display()

        if not game_alright or game.step_counter > 80*(game.score+3):
            game = Game(screen)
            print(score)

if __name__ == "__main__":
    option = input("Manual control? (y/n/e) ")
    pygame.init()
    SCREEN = pygame.display.set_mode([W * SCALE, H * SCALE])
    if option == "y":
        manual_control(SCREEN)
    if option == "e":
        evaluation("./saves/30", SCREEN)
    else:
        train("", SCREEN)

    pygame.quit()
