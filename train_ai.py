import os
import pickle

import neat

from game.game_base import BadugiBase

MAX_HANDS = 100
MAX_GENERATIONS = 40


def get_config(config_name: str):
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, config_name)
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    return config


def eval_genomes_init(genomes, config):
    for i, (genome1_id, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome2_id, genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            badugi = BadugiBase([str(genome1_id), str(genome2_id)], 10000, MAX_HANDS)
            badugi.train_only_swap(genome1, genome2, config)


def init_ai(swap_config):
    p = neat.Population(swap_config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    swap_winner = p.run(eval_genomes_init, MAX_GENERATIONS)
    print("\nBest genome:\n{!s}".format(swap_winner))
    with open("swap.pickle", "wb") as f:
        pickle.dump(swap_winner, f)


def eval_bet_genomes(genomes, config):
    swap_config = get_config("config-swap.txt")
    with open("swap.pickle", "rb") as f:
        swap_winner = pickle.load(f)
    swap_net = neat.nn.FeedForwardNetwork.create(swap_winner, swap_config)
    for i, (genome1_id, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome2_id, genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            badugi = BadugiBase([str(genome1_id), str(genome2_id)], 1000, MAX_HANDS)
            badugi.train_bet(genome1, genome2, config, swap_net)


def train_bet(bet_config):
    p = neat.Population(bet_config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    bet_winner = p.run(eval_bet_genomes, MAX_GENERATIONS)
    print("\nBest genome:\n{!s}".format(bet_winner))
    with open("bet.pickle", "wb") as f:
        pickle.dump(bet_winner, f)


def eval_swap_genomes(genomes, config):
    bet_config = get_config("config-bet.txt")
    with open("bet.pickle", "rb") as f:
        bet_winner = pickle.load(f)
    bet_net = neat.nn.FeedForwardNetwork.create(bet_winner, bet_config)
    for i, (genome1_id, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome2_id, genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            badugi = BadugiBase([str(genome1_id), str(genome2_id)], 1000, MAX_HANDS)
            badugi.train_swap(genome1, genome2, config, bet_net)


def train_swap(swap_config):
    p = neat.Population(swap_config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    swap_winner = p.run(eval_swap_genomes, MAX_GENERATIONS)
    print("\nBest genome:\n{!s}".format(swap_winner))
    with open("swap.pickle", "wb") as f:
        pickle.dump(swap_winner, f)


if __name__ == "__main__":
    import sys

    if "init" in sys.argv:
        init_config = get_config("config-swap.txt")
        init_ai(init_config)
    if "bet" in sys.argv:
        bet_config = get_config("config-bet.txt")
        train_bet(bet_config)
    if "swap" in sys.argv:
        swap_config = get_config("config-swap.txt")
        train_swap(swap_config)
    if not any([s in sys.argv for s in ["init", "bet", "swap"]]):
        print("try: ./train_ai.py init / bet / swap")
