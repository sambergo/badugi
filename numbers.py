"""
2-input XOR example -- this is most likely the simplest possible example.
"""


import os
from random import random, shuffle

import neat

# 2-input XOR inputs and expected outputs.
xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]

nums1 = [1, 2, 3, 4]
nums2 = [2, 1, 3, 2]


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        idxs = [i for i in range(4)]
        shuffle(idxs)
        # zippi = zip(xor_inputs, xor_outputs)
        for i in idxs:
            output = net.activate((nums1[i], nums2[i]))
            # valivar = (output[0] - xor_outputs[i][0]) ** 2
            add_one = 1 if output[0] > 0.5 else 0
            is_even = (nums1[i] + nums2[i] + add_one) % 2 == 0
            genome.fitness += 0.1 if is_even else -0.1


def run(config_file):
    # Load configuration.
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print("\nBest genome:\n{!s}".format(winner))

    # Show output of the most fit genome against training data.
    print("\nOutput:")
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    idxs = [i for i in range(4)]
    shuffle(idxs)
    print("idxs:", idxs)
    # zippi = zip(xor_inputs, xor_outputs)
    for i in idxs:
        output = winner_net.activate((nums1[i], nums2[i]))
        is_even = (nums1[i] + nums2[i]) % 2 == 0
        print("is_even:", is_even)
        print(
            "input {!r}, expected output {!r}, got {!r}".format(
                (nums1[i], nums2[i]), 0 if is_even else 1, output
            )
        )

    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")
    # p.run(eval_genomes, 10)


if __name__ == "__main__":
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_nums.txt")
    run(config_path)
