import os
import pickle

import neat
import pygame

from game import Badugi

# width, height = 1400, 800
# max_hands = 3
# window = pygame.display.set_mode((width, height))
STARTING_CHIPS = 10000


class BadugiAI:
    def __init__(self, window, width, height, players, max_hands):
        self.game = Badugi(window, width, height, players, STARTING_CHIPS, max_hands)
        self.players = self.game.players
        self.dealer = self.game.dealer
        self.max_hands = max_hands

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        # clock = pygame.time.Clock()
        while run:
            # clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

            # hand rank, state
            output1 = net1.activate((self.players[0].hand_rank, self.dealer.stage))
            decision1 = output1.index(max(output1))
            output2 = net2.activate((self.players[1].hand_rank, self.dealer.stage))
            decision2 = output2.index(max(output2))
            turns_left = len([player for player in self.players if player.draw])
            if not self.game.hand_active:
                # print("noot")
                pass
            elif self.dealer.turn == 0 and self.dealer.stage % 2 != 1:
                self.players[0].draw_number_of_cards(self.dealer, decision1)
                if turns_left != 1:
                    self.dealer.next_turn(self.players, new_street=False)
            elif self.dealer.turn == 1 and self.dealer.stage % 2 != 1:
                self.players[1].draw_number_of_cards(self.dealer, decision2)
                if turns_left != 1:
                    self.dealer.next_turn(self.players, new_street=False)
            # print(output1, output2)
            game_info = self.game.main_loop()
            # print(game_info)
            # self.game.draw()
            # pygame.display.update()
            if self.game.hands_played >= self.max_hands:
                # print(game_info)
                # print("LOPPPUUUUUUUUUUUUUUU" * 99)
                self.game.hand_active = False
                self.calculate_fitness(genome1, genome2, self.game)
                break

    def calculate_fitness(self, genome1, genome2, game):
        genome1.fitness += game.players[0].chips - STARTING_CHIPS
        genome2.fitness += game.players[1].chips - STARTING_CHIPS
        print("fitness", genome1.fitness, genome2.fitness)


def eval_genomes(genomes, config):
    width, height = 1400, 800
    max_hands = 100
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        print("eval", i)
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = BadugiAI(
                window,
                width,
                height,
                [f"AI-{genome_id1}", f"AI-{genome_id2}"],
                max_hands,
            )
            game.train_ai(genome1, genome2, config)


def run_neat(config):
    p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1')
    # ↑ Toinen kommentoidaan pois. Aloitetaanko alusta vai jatketaanko checkpointista.
    p.add_reporter(
        neat.StdOutReporter(True)
    )  # Raportoi: best fitness, avg fitness etc...
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(
        neat.Checkpointer(1)
    )  # Tallentaa checkpointin n-sukupolven jälkeen, ettei tarvi alottaa alusta.
    winner = p.run(eval_genomes, 3)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    run_neat(config)
    # test_ai(config)
