import os
import pickle
from random import random, shuffle

import neat

from game.game import Badugi
from game.tools.get_winners import get_hand_rank
from game.tools.sort_hand import sort_badugi_hand


def eval_genomes(genomes, config):
    local_dir = os.path.dirname(__file__)
    config_path_swap = os.path.join(local_dir, "config-swap.txt")
    config_swap = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path_swap,
    )
    with open("best.pickle", "rb") as f:
        swap_winner = pickle.load(f)
    swap_net = neat.nn.FeedForwardNetwork.create(swap_winner, config_swap)
    for i, (genome1_id, genome1) in enumerate(genomes):
        print("i:", i)
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome2_id, genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            badugi = Badugi([str(genome1_id), str(genome2_id)], 10000, 100)
            badugi.train_betting(genome1, genome2, config, swap_net)


def test_ai(bet_config, swap_config):
    with open("best.pickle", "rb") as f:
        swap_winner = pickle.load(f)
    ai_swap_net = neat.nn.FeedForwardNetwork.create(swap_winner, swap_config)
    with open("betting.pickle", "rb") as f:
        bet_winner = pickle.load(f)
    ai_bet_net = neat.nn.FeedForwardNetwork.create(bet_winner, bet_config)
    max_hands = 10
    badugi = Badugi(["Player", "AI"], 1000, max_hands)
    badugi.test_ai(ai_bet_net, ai_swap_net)


def run_betting_training(bet_config):
    p = neat.Population(bet_config)
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-7")
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(10))

    max_generations = 40
    swap_winner = p.run(eval_genomes, max_generations)
    print("\nBest genome:\n{!s}".format(swap_winner))

    with open("betting.pickle", "wb") as f:
        pickle.dump(swap_winner, f)


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
    test_ai(bet_config, swap_config)
    # run_betting_training(bet_config)
