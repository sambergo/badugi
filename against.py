import os
import pickle
from random import random, shuffle

import neat

from game.game import Badugi
from game.tools.get_winners import get_hand_rank
from game.tools.sort_hand import sort_badugi_hand


def eval_genomes(genomes, config):
    for i, (genome1_id, genome1) in enumerate(genomes):
        print("i:", i)
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome2_id, genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            badugi = Badugi([str(genome1_id), str(genome2_id)], 10000, 100)
            badugi.train_ai(genome1, genome2, config)


def run(config):
    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-7")
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(10))

    max_generations = 40
    winner = p.run(eval_genomes, max_generations)
    # Display the winning genome.
    print("\nBest genome:\n{!s}".format(winner))
    # Show output of the most fit genome against training data.
    # print("\nOutput:")
    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")
    # p.run(eval_genomes, 10)


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    badugi = Badugi(["Player", "AI"], 10000, 10)
    badugi.test_ai(winner_net)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-against.txt")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    # run(config)
    test_ai(config)
