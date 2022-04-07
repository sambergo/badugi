import os
import pickle

import neat
import pygame

from game.game import Badugi

pygame.init()


def eval_genomes(genomes, config):
    # pygame
    pygame.display.set_caption("Badugi")
    width, height = 1400, 800
    window = pygame.display.set_mode((width, height))
    for i, (genome1_id, genome1) in enumerate(genomes):
        print("i:", i)
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome2_id, genome2 in genomes[i + 1 :]:
            print("j", i + 1)
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            badugi = Badugi(
                [str(genome1_id), str(genome2_id)], 10000, 10, window, width, height
            )
            badugi.train_only_swap(genome1, genome2, config)


def init_ai(swap_config):
    p = neat.Population(swap_config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    max_generations = 40
    swap_winner = p.run(eval_genomes, max_generations)
    print("\nBest genome:\n{!s}".format(swap_winner))
    with open("betting.pickle", "wb") as f:
        pickle.dump(swap_winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path_swap = os.path.join(local_dir, "config-swap.txt")
    swap_config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path_swap,
    )
    init_ai(swap_config)
    # run_betting_training(bet_config)
