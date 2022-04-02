# from __future__ import print_function
import os
import pickle
import random
from random import shuffle

import neat

from game.tools.get_winners import get_hand_rank
from game.tools.sort_hand import sort_badugi_hand

# 2-input XOR inputs and expected outputs.
xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

ekat = [4, 4, 2, 4, 2]
tokat = [3, 3, 5, 3, 1]


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 1.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        my_input1 = random.randint(1, 2)
        my_input2 = random.randint(1, 2)
        output = net.activate((my_input1, my_input2))

        # output: [1.0, 1.0, 1.0, 8.75651076269652e-27]
        # (self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
        decision = output.index(max(output))
        total = 1
        genome.fitness += 2 if my_num > my_opponent else 1


def run(config):
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 300)

    print("\nBest genome:\n{!s}".format(winner))

    # Show output of the most fit genome against training data.
    print("\nOutput:")
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # node_names = {-1: "A", -2: "B", 0: "A XOR B"}
    # visualize.draw_net(config, winner, True, node_names=node_names)
    # visualize.plot_stats(stats, ylog=False, view=True)
    # visualize.plot_species(stats, view=True)
    print("winner:", winner)
    print("winner_net:", winner_net)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")
    # p.run(eval_genomes, 10)


def test_ai(config):
    with open("best.pickle", "rb") as f:
        genome = pickle.load(f)
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    output = net.activate((1, 2))
    print("output:", output)
    decision = output.index(max(output))
    print("decision:", decision)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, "config_nums.txt")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    # run(config)
    test_ai(config)
