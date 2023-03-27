from dataclasses import dataclass
import pygame
from pygame.locals import QUIT
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

def train(model_path = "", save_path="", use_pygame = False, screen = None):
    running = True

    game = Game(screen)
    agent = Agent()
    if model_path != "":
        agent.load_model(model_path)
    print("Starting game no", agent.game_count)

    while running:
        if use_pygame:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
        
        current_state = game.get_qstate()
        (action, pred) = agent.get_action(current_state)

        game.direction = action
        (reward, game_alright, score) = game.next_step()
        game.display()

        new_state = game.get_qstate()
        
        # train short memory
        agent.train_short_memory(current_state, pred, reward, new_state, game_alright)
        # append memory
        agent.memory.append((current_state, pred, reward, new_state, game_alright))

        if not game_alright or game.step_counter > 80*(game.score+3):
            game = Game(screen)
            # train long memory
            agent.replay_mem(1000)
            print("Starting game no", agent.game_count)
            if agent.game_count % 10 == 0:
                agent.model.save(save_path + str(agent.game_count))

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
        evaluation("/home/przebot/Projects/Python/RLSnake/saves/10", SCREEN)
    else:
        train("", "./saves/", SCREEN)

    pygame.quit()
