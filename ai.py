import os

import neat
import pygame

from game import Badugi

# width, height = 1400, 800
# max_hands = 3
# window = pygame.display.set_mode((width, height))


class BadugiAI:
    def __init__(self, window, width, height, players, max_hands):
        self.game = Badugi(window, width, height, players, 20000, max_hands)
        self.players = self.game.players
        self.dealer = self.game.dealer

        def test_ai(self):
            run = True
            while run:
                clock.tick(3)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break
                run = badugi.main_loop()
                badugi.draw()
                pygame.display.update()
            for player in badugi.players:
                print(player.name)
                print(player.chips)
            print("LOPPU")
            pygame.quit()

        players = ["Player1", "Player2", "Player3"]
        width, height = 1400, 800
        max_hands = 3
        window = pygame.display.set_mode((width, height))
        badugi = Badugi(window, width, height, players, 20000, max_hands)
        clock = pygame.time.Clock()

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

            # hand rank, state
            output1 = net1.activate((self.players[0].hand_rank, self.dealer.stage))
            decision1 = output1.index(max(output1))
            output2 = net2.activate((self.players[1].hand_rank, self.dealer.stage))
            decision2 = output2.index(max(output2))
            print(output1, output2)
            game_info = self.game.main_loop()
            self.game.draw()
            pygame.display.update()
            if self.game.hand_active >= 3:
                print(game_info)
                # calculate_fitness
                break

    def calculate_fitness(self, genome1, genome2):
        pass


def eval_genomes(genomes, config):
    width, height = 1400, 800
    max_hands = 3
    window = pygame.display.set_mode((width, height))

    # width, height = 700, 500
    # window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i + 1 :]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = BadugiAI(window, width, height, ["ai1", "ai2"], max_hands)
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
