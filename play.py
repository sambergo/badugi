import os
import pickle

import neat
import pygame

from game.game import Badugi


def play_badugi(bet_config, swap_config):
    with open("swap.pickle", "rb") as f:
        swap_winner = pickle.load(f)
    ai_swap_net = neat.nn.FeedForwardNetwork.create(swap_winner, swap_config)
    with open("bet.pickle", "rb") as f:
        bet_winner = pickle.load(f)
    ai_bet_net = neat.nn.FeedForwardNetwork.create(bet_winner, bet_config)
    max_hands = 100
    players = ["Player1", "AI"]
    pygame.display.set_caption("Badugi")
    width, height = 1400, 800
    window = pygame.display.set_mode((width, height))
    badugi = Badugi(players, 1000, max_hands, window, width, height)
    badugi.play_ai(ai_bet_net, ai_swap_net)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path_betting = os.path.join(local_dir, "config-bet.txt")
    bet_config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path_betting,
    )
    config_path_swap = os.path.join(local_dir, "config-swap.txt")
    swap_config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path_swap,
    )
    play_badugi(bet_config, swap_config)
