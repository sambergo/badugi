import os
import pickle
from random import random, shuffle

import neat

from game.tools.get_winners import get_hand_rank
from game.tools.sort_hand import sort_badugi_hand


def eval_genomes(genomes, config):
    for _, genome in genomes:
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        for _ in range(99):
            deck = [
                {"suit": suit, "number": number}
                for suit in ["c", "d", "h", "s"]
                for number in range(1, 14)
            ]
            shuffle(deck)
            # 6 hands
            hands = [sort_badugi_hand(deck[i : i + 4]) for i in range(0, 6 * 4, 4)]
            for hand in hands:
                old_rank = get_hand_rank(hand)
                rank_with_3 = get_hand_rank(hand[:3])
                rank_with_2 = get_hand_rank(hand[:2])
                rank_with_1 = get_hand_rank(hand[:1])
                output = net.activate((old_rank, rank_with_3, rank_with_2, rank_with_1))
                decision = output.index(max(output))
                if decision > 0:
                    hand = hand[: 4 - decision]
                    for _ in range(decision):
                        hand.append(deck.pop())
                    hand = sort_badugi_hand(hand)
                new_rank = get_hand_rank(hand)
                x = new_rank - old_rank
                if x < 0:
                    genome.fitness += x * 2
                else:
                    genome.fitness += x


def run(config):
    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-7")
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

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
            {"suit": "c", "number": 3},
            {"suit": "h", "number": 4},
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

    # hands = [sort_badugi_hand(deck[i : i + 4]) for i in range(0, 6 * 4, 4)]
    for hand in hands:
        old_rank = get_hand_rank(hand)
        rank_with_3 = get_hand_rank(hand[:3])
        rank_with_2 = get_hand_rank(hand[:2])
        rank_with_1 = get_hand_rank(hand[:1])
        output = winner_net.activate((old_rank, rank_with_3, rank_with_2, rank_with_1))
        decision = output.index(max(output))
        print(
            f"{','.join([str(c['number'])+c['suit'] for c in hand])} rank: {old_rank} decision: {decision}"
        )

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")
    # p.run(eval_genomes, 10)


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    deck = [
        {"suit": suit, "number": number}
        for suit in ["c", "d", "h", "s"]
        for number in range(1, 14)
    ]
    shuffle(deck)
    hands = [sort_badugi_hand(deck[i : i + 4]) for i in range(0, 6 * 4, 4)]
    for hand in hands:
        old_rank = get_hand_rank(hand)
        rank_with_3 = get_hand_rank(hand[:3])
        rank_with_2 = get_hand_rank(hand[:2])
        rank_with_1 = get_hand_rank(hand[:1])
        output = winner_net.activate((old_rank, rank_with_3, rank_with_2, rank_with_1))
        decision = output.index(max(output))
        print(
            f"{','.join([str(c['number'])+c['suit'] for c in hand])} rank: {old_rank} decision: {decision}"
        )


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_multi.txt")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    # run(config)
    test_ai(config)
