import os
import pickle
from random import random, shuffle

import neat

from game.tools.get_winners import get_hand_rank
from game.tools.sort_hand import sort_badugi_hand


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for i in range(99):
            deck = [
                {"suit": suit, "number": number}
                for suit in ["c", "d", "h", "s"]
                for number in range(1, 14)
            ]
            shuffle(deck)
            hands = [sort_badugi_hand(deck[i : i + 4]) for i in range(0, 10 * 4, 4)]

            # hands = [
            #     [
            #         {"suit": "c", "number": 1},
            #         {"suit": "h", "number": 2},
            #         {"suit": "d", "number": 3},
            #         {"suit": "s", "number": 4},
            #     ],
            #     [
            #         {"suit": "d", "number": 9},
            #         {"suit": "h", "number": 10},
            #         {"suit": "c", "number": 12},
            #         {"suit": "c", "number": 13},
            #     ],
            #     [
            #         {"suit": "c", "number": 9},
            #         {"suit": "d", "number": 10},
            #         {"suit": "h", "number": 11},
            #         {"suit": "s", "number": 13},
            #     ],
            # ]

            for hand in hands:
                old_rank = get_hand_rank(hand)
                rank_without_last = get_hand_rank(hand[:3])
                output = net.activate((old_rank, rank_without_last))
                if output[0] > 0.5:
                    hand.pop()
                    hand.append(deck.pop())
                    hand = sort_badugi_hand(hand)
                new_rank = get_hand_rank(hand)
                x = new_rank - old_rank
                if x < 0:
                    genome.fitness += x * 10
                else:
                    genome.fitness += x

        # idxs = [i for i in range(4)]
        # shuffle(idxs)
        # # zippi = zip(xor_inputs, xor_outputs)
        # for i in idxs:
        #     output = net.activate((nums1[i], nums2[i]))
        #     # valivar = (output[0] - xor_outputs[i][0]) ** 2
        #     add_one = 1 if output[0] > 0.5 else 0
        #     is_even = (nums1[i] + nums2[i] + add_one) % 2 == 0
        #     genome.fitness += 0.1 if is_even else -0.1


def run(config):
    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-7")

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 30)

    # Display the winning genome.
    print("\nBest genome:\n{!s}".format(winner))

    # Show output of the most fit genome against training data.
    print("\nOutput:")
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    hands = [
        [
            {"suit": "c", "number": 1},
            {"suit": "h", "number": 2},
            {"suit": "d", "number": 3},
            {"suit": "s", "number": 4},
        ],
        [
            {"suit": "d", "number": 9},
            {"suit": "h", "number": 10},
            {"suit": "c", "number": 12},
            {"suit": "c", "number": 13},
        ],
        [
            {"suit": "c", "number": 9},
            {"suit": "d", "number": 10},
            {"suit": "h", "number": 11},
            {"suit": "s", "number": 13},
        ],
    ]
    for hand in hands:
        old_rank = get_hand_rank(hand)
        rank_without_last = get_hand_rank(hand[:3])
        output = winner_net.activate((old_rank, rank_without_last))
        print(
            f"old rank: {old_rank}, without last: {rank_without_last}. vaihdetaanko: {output[0]} "
        )

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

    # idxs = [i for i in range(4)]
    # shuffle(idxs)
    # print("idxs:", idxs)
    # # zippi = zip(xor_inputs, xor_outputs)
    # for i in idxs:
    #     output = winner_net.activate((nums1[i], nums2[i]))
    #     is_even = (nums1[i] + nums2[i]) % 2 == 0
    #     print("is_even:", is_even)
    #     print(
    #         "input {!r}, expected output {!r}, got {!r}".format(
    #             (nums1[i], nums2[i]), 0 if is_even else 1, output
    #         )
    #     )

    # for xi, xo in zip(xor_inputs, xor_outputs):
    #     output = winner_net.activate(xi)
    #     print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")
    # p.run(eval_genomes, 10)


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    # hands = [
    #     [
    #         {"suit": "c", "number": 1},
    #         {"suit": "d", "number": 2},
    #         {"suit": "h", "number": 3},
    #         {"suit": "s", "number": 4},
    #     ],
    #     [
    #         {"suit": "d", "number": 9},
    #         {"suit": "h", "number": 10},
    #         {"suit": "c", "number": 12},
    #         {"suit": "c", "number": 13},
    #     ],
    #     [
    #         {"suit": "c", "number": 9},
    #         {"suit": "d", "number": 10},
    #         {"suit": "h", "number": 11},
    #         {"suit": "s", "number": 13},
    #     ],
    # ]
    deck = [
        {"suit": suit, "number": number}
        for suit in ["c", "d", "h", "s"]
        for number in range(1, 14)
    ]
    shuffle(deck)
    hands = [sort_badugi_hand(deck[i : i + 4]) for i in range(0, 10 * 4, 4)]
    for hand in hands:
        hand = sort_badugi_hand(hand)
        old_rank = get_hand_rank(hand)
        rank_without_last = get_hand_rank(hand[:3])
        output = winner_net.activate((old_rank, rank_without_last))
        print(
            f"old rank: {old_rank}, without last: {rank_without_last}. vaihdetaanko: {output[0]} "
        )


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_single.txt")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    # run(config)
    test_ai(config)
