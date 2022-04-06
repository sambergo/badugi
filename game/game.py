from random import randrange

import neat
import pygame

from .button import Button
from .dealer import Dealer, create_deck
from .player import Player
from .tools.get_winners import get_hand_rank, get_winners
from .tools.sort_hand import sort_badugi_hand
from .player import create_players

pygame.init()


class Badugi:
    """
    docstring for Badugi.
    """

    BIG_FONT = pygame.font.SysFont("comicsans", 50)
    FONT = pygame.font.SysFont("comicsans", 22)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 128, 0)
    BIG_BLIND = 10
    BG = pygame.image.load("./PNG/table.png")
    AVATAR1 = pygame.transform.scale(
        pygame.image.load("./PNG/bear-face.png"), (100, 100)
    )
    AVATAR2 = pygame.transform.scale(
        pygame.image.load("./PNG/tiger-head.png"), (100, 100)
    )
    DEALER_BUTTON = pygame.transform.scale(
        pygame.image.load("./PNG/dealer_button.png"), (50, 50)
    )

    def __init__(self, player_names, starting_chips, max_hands, window, width, height):
        self.WINDOW: pygame.Surface = window
        self.WIDTH = width
        self.HEIGHT = height
        self.STARTING_CHIPS = starting_chips
        self.players = create_players(player_names, starting_chips)
        self.button = randrange(0, len(player_names))
        self.MAX_HANDS = max_hands
        self.BB = float(self.BIG_BLIND)
        self.SB = float(self.BIG_BLIND / 2)
        self.hands_played = 0
        self.hand_active = False
        self.dealer = Dealer(
            self.players, self.button, self.BB, create_deck(self.WINDOW)
        )
        self.is_not_training = True
        self.MAX_STAGES = 7
        self.clock = pygame.time.Clock()
        self.p1x = self.WIDTH // 4
        self.p1y = 50
        self.p2x = self.WIDTH // 4
        self.p2y = 600

    def test_game(self):
        """
        Test Game
        """
        run = True
        # clock = pygame.time.Clock()
        while run:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            self.print_info()
            is_betting_stage = self.dealer.stage % 2 == 0
            # Main loop
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage >= self.MAX_STAGES:
                self.finish_hand()
            elif self.hand_active and is_betting_stage:  # TODO: Not only HU
                if self.dealer.turn == 0:
                    self.make_player_bet(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_player_bet(self.players[1])
                else:
                    print("ERROR" * 99)
            elif self.hand_active and not is_betting_stage:
                if self.dealer.turn == 0:
                    self.make_player_swap(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_player_swap(self.players[1])
                else:
                    print("ERROR" * 99)
            else:
                self.deal_new_hand()
            self.draw_game()
            pygame.display.update()
        return False

    def draw_game(self):
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blit(self.BG, (0, 0))
        self._draw_dealer()
        self._draw_players()

    def _draw_dealer(self):
        dx = self.WIDTH // 3
        dy = self.HEIGHT // 2.6
        text = self.BIG_FONT.render(f"Pot: {self.dealer.pot}", True, self.WHITE)
        self.WINDOW.blit(text, (dx, dy))
        text = self.BIG_FONT.render(
            f"Draws left: {3 - self.dealer.stage // 2}", True, self.WHITE
        )
        self.WINDOW.blit(text, (dx, dy + 50))
        # Actions on left side
        for i, msg in enumerate(self.dealer.actions[-10:]):
            text = self.FONT.render(msg, True, self.WHITE)
            self.WINDOW.blit(text, (20, 50 + (i * 30)))

    def _draw_players(self):  # TODO: multiplayer
        # Player 1
        text = self.BIG_FONT.render(
            self.players[0].name,
            True,
            "yellow" if self.dealer.turn == 0 else self.WHITE,
        )
        self.WINDOW.blit(text, (self.p1x, self.p1y))
        text = self.FONT.render(str(self.players[0].chips), True, self.WHITE)
        self.WINDOW.blit(text, (self.p1x, self.p1y + 40))
        self.WINDOW.blit(self.AVATAR1, (self.p1x, self.p1y + 70))
        for i, card in enumerate(self.players[0].hand):
            card.show(((self.p1x + 200) + (i * 100), self.p1y))

        # Player 2
        text = self.BIG_FONT.render(
            self.players[1].name,
            True,
            self.GREEN if self.dealer.turn == 1 else self.WHITE,
        )
        self.WINDOW.blit(text, (self.p2x, self.p2y))
        text = self.FONT.render(str(self.players[1].chips), True, self.WHITE)
        self.WINDOW.blit(text, (self.p2x, self.p2y + 40))
        self.WINDOW.blit(self.AVATAR2, (self.p2x, self.p2y + 70))
        for i, card in enumerate(self.players[1].hand):
            card.show(((self.p2x + 200) + (i * 100), self.p2y))
        # Dealer button
        self.WINDOW.blit(
            self.DEALER_BUTTON,
            (self.p1x + 120, self.p1y + 150 if self.button == 0 else self.p2y - 40),
        )

    def test_ai(self, ai_bet_net, ai_swap_net):
        """
        Test AI
        """
        run = True
        while run:
            self.print_info()
            is_betting_stage = self.dealer.stage % 2 == 0
            # Main loop
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage >= self.MAX_STAGES:
                self.finish_hand()
            elif self.hand_active and is_betting_stage:  # TODO: Not only HU
                if self.dealer.turn == 0:
                    self.make_player_bet(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_ai_bet_decision(self.players[1], ai_bet_net)
                else:
                    print("ERROR" * 99)
            elif self.hand_active and not is_betting_stage:
                if self.dealer.turn == 0:
                    self.make_player_swap(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_ai_swap_decision(self.players[1], ai_swap_net)
                else:
                    print("ERROR" * 99)
            else:
                self.deal_new_hand()
            self.draw_game()
            pygame.display.update()
        return False

    def train_swap(self, genome1, genome2, config):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        These AI's will play against eachother to determine their fitness.
        """
        self.genome1 = genome1
        self.genome2 = genome2
        net0 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net1 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.is_not_training = False
        run = True
        while run:
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage < self.MAX_STAGES:
                if self.dealer.turn == 0:
                    self.make_ai_swap_decision(self.players[0], net0)
                elif self.dealer.turn == 1:
                    self.make_ai_swap_decision(self.players[1], net1)
                else:
                    print("ERROR" * 99)
            elif self.dealer.stage >= self.MAX_STAGES and self.hand_active:
                self.finish_hand()
            else:
                self.deal_new_hand()
        self.calculate_fitness()
        return False

    def train_betting(self, genome1, genome2, config, swap_net):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        These AI's will play against eachother to determine their fitness.
        """
        self.genome1 = genome1
        self.genome2 = genome2
        net0 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net1 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.is_not_training = False
        run = True
        while run:
            is_betting_stage = self.dealer.stage % 2 == 0
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage >= self.MAX_STAGES:
                self.finish_hand()
            elif self.hand_active and is_betting_stage:  # TODO: Not only HU
                if self.dealer.turn == 0:
                    self.make_ai_bet_decision(self.players[0], net0)
                elif self.dealer.turn == 1:
                    self.make_ai_bet_decision(self.players[1], net1)
                else:
                    print("ERROR" * 99)
            elif self.hand_active and not is_betting_stage:
                if self.dealer.turn == 0:
                    self.make_ai_swap_decision(self.players[0], swap_net)
                elif self.dealer.turn == 1:
                    self.make_ai_swap_decision(self.players[1], swap_net)
                else:
                    print("ERROR" * 99)
            else:
                self.deal_new_hand()
        self.calculate_fitness()
        return False

    def make_ai_bet_decision(self, player, net):
        hand_rank = get_hand_rank(player.hand)
        output = net.activate(
            (hand_rank, self.dealer.stage, self.dealer.pot, player.chips_in_front)
        )
        decision = output.index(max(output))
        if self.is_not_training:
            print(f"player {player.name} making bet decision: {decision} ")
        if decision == 0:
            player.fold(self.dealer)
        elif decision == 1:
            player.call(self.dealer)
        elif decision == 2:
            player.bet(self.dealer, self.players)
        else:
            print("TURN ERROR")
        self.update_street()

    def make_ai_swap_decision(self, player, net):
        old_rank = get_hand_rank(player.hand)
        rank_with_3 = get_hand_rank(player.hand[:3])
        rank_with_2 = get_hand_rank(player.hand[:2])
        rank_with_1 = get_hand_rank(player.hand[:1])
        output = net.activate(
            (self.dealer.stage, old_rank, rank_with_3, rank_with_2, rank_with_1)
        )
        decision = output.index(max(output))
        if self.is_not_training:
            print(f"player {player.name} swaps cards: {decision} ")
        player.swap_number_of_cards(self.dealer, decision)
        self.update_street()

    def calculate_fitness(self):
        self.genome1.fitness += self.players[0].chips - self.STARTING_CHIPS
        self.genome2.fitness += self.players[1].chips - self.STARTING_CHIPS

    def wait_for_player_bet(self, player, is_not_capped) -> int:
        waiting_decision = True
        is_call = player.chips_in_front < self.dealer.to_call
        button_texts = ["Fold", "Call" if is_call else "Check"]
        if is_not_capped:
            button_texts.append("Raise" if self.dealer.street_bets != 0 else "Bet")
        buttons = []
        dis_from_x = 700
        dis_from_y = 20
        bx = self.p1x + dis_from_x if self.dealer.turn == 0 else self.p2x + dis_from_x
        by = self.p1y + dis_from_y if self.dealer.turn == 0 else self.p2y + dis_from_y
        for i, btn_text in enumerate(button_texts):
            button = Button(self.WINDOW, btn_text, (bx, by + (i * 43)), self.BIG_FONT)
            button.show()
            buttons.append(button)
        pygame.display.update()
        decision = 1
        while waiting_decision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                for i, btn in enumerate(buttons, start=1):
                    if btn.any_click(event):
                        decision = i
                        waiting_decision = False
            self.clock.tick(30)
        for btn in buttons:
            btn.show()
        pygame.display.update()
        return decision

    def wait_for_player_swap(self, player):
        waiting_decision = True
        dis_from_x = 800
        dis_from_y = 50
        bx = self.p1x + dis_from_x if self.dealer.turn == 0 else self.p2x + dis_from_x
        by = self.p1y + dis_from_y if self.dealer.turn == 0 else self.p2y + dis_from_y
        confirm_button = Button(self.WINDOW, "Ready", (bx, by), self.BIG_FONT)
        confirm_button.show()
        pygame.display.update()
        while waiting_decision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                for i, card in enumerate(player.hand):
                    if card.any_click(event):
                        print("jep")
                if confirm_button.any_click(event):
                    waiting_decision = False
            self.clock.tick(30)

    def make_player_bet(self, player):
        is_not_capped = self.dealer.street_bets < self.dealer.cap
        decision = self.wait_for_player_bet(player, is_not_capped)
        print("decision:", decision)
        # decision = int(input("1. Fold, 2. Check/call, 3. Raise"))
        # decision = randrange(1, 4)
        if self.is_not_training:
            print(f"player {player.name} bet decision: {decision} ")
        if decision == 1:
            player.fold(self.dealer)
        if decision == 3 and is_not_capped:
            player.bet(self.dealer, self.players)
        else:
            player.call(self.dealer)
        self.update_street()

    def make_player_swap(self, player):
        self.wait_for_player_swap(player)
        player.swap_selected_cards(self.dealer)
        self.update_street()

    def update_street(self):
        is_swap = self.dealer.stage % 2 == 1
        all_acted = all([p.acted for p in self.players])
        no_turns_left = all([p.swapped for p in self.players]) if is_swap else all_acted
        no_showdown = len([p for p in self.players if not p.folded]) == 1
        if no_turns_left and self.dealer.stage >= self.MAX_STAGES or no_showdown:
            self.finish_hand()
        elif no_turns_left and self.dealer.stage < self.MAX_STAGES or all_acted:
            self.next_street()
        else:
            self.dealer.next_turn(self.players, new_street=False)

    def next_street(self):
        self.dealer.next_turn(self.players, new_street=True)
        self.dealer.to_call = 0
        for player in self.players:
            if not player.folded:
                player.acted = False
                player.swapped = False
        self.dealer.all_acted = False

    def deal_new_hand(self):
        """
        - Creates new dealer
        - Resets players
        - Posts blinds
        """
        if self.is_not_training:
            print(f"dealing new hand")
        new_deck = create_deck(self.WINDOW)
        self.dealer = Dealer(self.players, self.button, self.BB, new_deck)
        self.dealer.shuffle_deck()
        self.hand_active = True
        # Deal cards
        for player in self.players:
            player.reset()
            player_hand = []
            for _ in range(4):
                player_hand.append(self.dealer.deck.pop())
            player.hand = sort_badugi_hand(player_hand)
            player.hand_rank = get_hand_rank(player.hand)
        pl = len(self.players)
        # Blinds
        sb_index = self.button if pl == 2 else (self.button + 1) % pl
        bb_index = (self.button + 1) % pl if pl == 2 else (self.button + 2) % pl
        self.players[sb_index].post_sb(self.dealer)
        self.players[bb_index].post_bb(self.dealer)

    def finish_hand(self):
        if self.is_not_training:
            print("FINISH")
        winners = get_winners([player for player in self.players if not player.folded])
        for player in self.players:
            if player.name in winners:
                if self.is_not_training:
                    print(
                        f"WINNER: {player.name} amount_ {self.dealer.pot/len(winners)}"
                    )
                player.chips += self.dealer.pot / len(winners)
            player.reset()

        self.button = (self.button + 1) % len(self.players)
        self.hands_played += 1
        self.hand_active = False

    def print_info(self):
        print(
            f"""
            INFO:
            Hands played: {self.hands_played}
            Button: {self.dealer.button}
            Turn: {self.dealer.turn}
            Pot: {self.dealer.pot}
            Stage: {self.dealer.stage}
            {"-"*20}
            Player stack: {self.players[0].chips}
            AI stack: {self.players[1].chips}
            {"-"*20}
            AI hand:
            {[str(c.number)+c.suit for c in  self.players[1].hand]}
            Player hand:
            {[str(c.number)+c.suit for c in  self.players[0].hand]}
            {"-"*20}

                """
        )


def create_players(player_names, starting_chips):
    player_list = []
    for name in player_names:
        new_player = Player(name, starting_chips)
        player_list.append(new_player)
    return player_list


if __name__ == "__main__":
    players = ["Player1", "AI"]
    max_hands = 4
    # pygame.display.set_caption("Badugi")
    # width, height = 1400, 800
    # window = pygame.display.set_mode((width, height))
    # badugi = Badugi(players, 1000, max_hands, window, width, height)
    # badugi.test_game()
    # pygame.quit()
