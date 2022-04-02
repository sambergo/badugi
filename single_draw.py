# from __future__ import print_function
import os
import pickle
from random import shuffle

import neat

from game.tools.get_winners import get_hand_rank
from game.tools.sort_hand import sort_badugi_hand


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 1.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        deck = [
            {"suit": suit, "number": number}
            for suit in ["C", "D", "H", "S"]
            for number in range(1, 14)
        ]
        # deck.insert(0, {"suit": "H", "number": 2})
        shuffle(deck)
        hand = sort_badugi_hand(deck[48:])
        # hand = sort_badugi_hand(
        #     [
        #         {"suit": "S", "number": 3},
        #         {"suit": "D", "number": 4},
        #         {"suit": "H", "number": 9},
        #         {"suit": "S", "number": 13},
        #     ]
        # )
        hand_rank = get_hand_rank(sort_badugi_hand(hand))
        output = net.activate((hand_rank, 1))
        # output: [1.0, 1.0, 1.0, 8.75651076269652e-27]
        # (self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
        decision = output.index(max(output))
        for i in range(decision):
            hand.pop()
            hand.insert(0, deck[i])

        new_rank = get_hand_rank(sort_badugi_hand(hand))
        rank_diff = new_rank - hand_rank
        if rank_diff > 666:
            print(decision, new_rank, hand)
        genome.fitness += rank_diff

        # for xi, xo in zip(xor_inputs, xor_outputs):
        #     output = net.activate(xi)
        #     genome.fitness -= (output[0] - xo[0]) ** 2


def run(config):
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 1000)

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

    deck = [
        {"suit": suit, "number": number}
        for suit in ["C", "D", "H", "S"]
        for number in range(1, 14)
    ]
    shuffle(deck)
    # hand = sort_badugi_hand(
    #     [
    #         {"suit": "S", "number": 3},
    #         {"suit": "D", "number": 4},
    #         {"suit": "H", "number": 9},
    #         {"suit": "S", "number": 13},
    #     ]
    # )
    hand = sort_badugi_hand(deck[48:])
    print(hand)
    hand_rank = get_hand_rank(sort_badugi_hand(hand))
    print("hand_rank:", hand_rank)
    # output = net.activate([hand_rank])
    output = net.activate((hand_rank, 1))
    # output = net.activate((1, 2))
    print("output:", output)
    # output: [1.0, 1.0, 1.0, 8.75651076269652e-27]
    # (self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
    decision = output.index(max(output))
    print("decision:", decision)

    # output = net.activate(
    #     (self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
    # decision = output.index(max(output))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, "config_single.txt")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )
    # run(config)
    test_ai(config)
