from random import randrange

import pygame

from .dealer import Dealer
from .player import Player
from .tools.get_winners import get_hand_rank, get_winners
from .tools.sort_hand import sort_badugi_hand

pygame.init()


class Badugi:
    """
    docstring for Badugi.
    """

    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 128, 0)
    BIG_BLIND = 10
    MAX_HANDS = 3

    def __init__(self, window, width, height, player_names, starting_chips, max_hands):
        self.window = window
        self.width = width
        self.height = height
        self.starting_chips = starting_chips
        self.players = create_players(player_names, starting_chips)
        self.button = randrange(0, len(player_names))
        self.MAX_HANDS = max_hands
        self.bb = self.BIG_BLIND
        self.sb = self.BIG_BLIND / 2
        self.hands_played = 0
        self.hand_active = False
        self.dealer = Dealer(self.players, self.button, self.bb)

    def main_loop(self):
        """
        Runs one:
            - deal_new_hand
            - finish_hand
            - next_street
            - hand_loop
        and updates drawnings
        """
        # Loop
        if self.hands_played >= self.MAX_HANDS:
            return False
        elif self.hand_active:
            if self.dealer.stage > 2:
                self.finish_hand()
            elif self.dealer.stage % 2 == 0:
                only_one_left = (
                    len([player for player in self.players if not player.folded]) == 1
                )
                if only_one_left:
                    self.finish_hand()
                else:
                    # self.hand_loop()
                    self.dealer.next_turn(self.players, new_street=True)  # flip
            elif self.dealer.stage % 2 == 1:
                self.draw_cards_loop()
        else:
            if self.hands_played < self.MAX_HANDS:
                self.deal_new_hand()
            else:
                pass

        return f"{self.hand_active} {self.hands_played} {self.dealer.turn} {self.dealer.stage} "

    def hand_loop(self):
        # Betting rounds
        only_one_left = (
            len([player for player in self.players if not player.folded]) == 1
        )
        players_to_act = len([player for player in self.players if not player.acted])
        keys = pygame.key.get_pressed()
        if only_one_left:
            self.finish_hand()
        elif players_to_act == 0:
            self.next_street()
            print("hand loop all")
        elif keys[pygame.K_LEFT]:
            self.players[self.dealer.turn].fold()
            if players_to_act != 1:
                self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_DOWN]:
            self.players[self.dealer.turn].call(self.dealer)
            if players_to_act != 1:
                self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_RIGHT]:
            self.players[self.dealer.turn].bet(self.dealer, self.players)
            self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_UP]:
            self.print_info()

    def draw_cards_loop(self):
        keys = pygame.key.get_pressed()
        turns_left = len([player for player in self.players if player.draw])
        if turns_left == 0:
            self.next_street()
        elif keys[pygame.K_1]:
            # self.main_delay = True
            # self.players[self.dealer.turn].select_card(0)
            self.players[self.dealer.turn].draw_number_of_cards(self.dealer, 1)
            if turns_left != 1:
                self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_2]:
            # self.main_delay = True
            # self.players[self.dealer.turn].select_card(1)
            self.players[self.dealer.turn].draw_number_of_cards(self.dealer, 2)
            if turns_left != 1:
                self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_3]:
            # self.main_delay = True
            # self.players[self.dealer.turn].select_card(2)
            self.players[self.dealer.turn].draw_number_of_cards(self.dealer, 3)
            if turns_left != 1:
                self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_4]:
            # self.main_delay = True
            # self.players[self.dealer.turn].select_card(3)
            self.players[self.dealer.turn].draw_number_of_cards(self.dealer, 4)
            if turns_left != 1:
                self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_SPACE]:
            print("DRAW CARDS")
            # self.main_delay = True
            self.players[self.dealer.turn].draw_cards(self.dealer)
            if turns_left != 1:
                self.dealer.next_turn(self.players, new_street=False)
        elif keys[pygame.K_UP]:
            self.print_info()

    def next_street(self):
        self.dealer.next_turn(self.players, new_street=True)
        self.dealer.to_call = 0
        for player in self.players:
            if not player.folded:
                player.acted = False
                player.draw = True
        self.dealer.all_acted = False

    def deal_new_hand(self):
        """
        Plays a single hand:
            - create dealer
            - shuffle_deck
            - blinds
            - deal cards
            - preflop
            - change cards
            - award pot
            - move button
        :returns: Amount of chips of each player.
        """
        # Dealer
        self.dealer = Dealer(self.players, self.button, self.bb)
        self.dealer.shuffle_deck()
        self.hand_active = True
        # Blinds
        sb_index = (self.button + 1) % len(self.players)
        bb_index = (self.button + 2) % len(self.players)
        self.players[sb_index].post_sb(self.dealer)
        self.players[bb_index].post_bb(self.dealer)
        # Deal cards
        for player in self.players:
            player.reset()
            player_hand = []
            for i in range(4):  # type: ignore
                player_hand.append(self.dealer.deck.pop())
            player.hand = sort_badugi_hand(player_hand)
            player.hand.sort(key=lambda x: x["number"])
            player.hand_rank = get_hand_rank(player.hand)

    def finish_hand(self):
        # print("FINISH")
        winners = get_winners([player for player in self.players if not player.folded])
        for player in self.players:
            if player.name in winners:
                # print(f"WINNER: {player.name} amount_ {self.dealer.pot/len(winners)}")
                player.chips += self.dealer.pot / len(winners)
            player.reset()

        self.button = (self.button + 1) % len(self.players)
        self.hands_played += 1
        self.hand_active = False

    def print_info(self):
        print("INFO")
        print("turn:", self.players[self.dealer.turn].name)
        print(
            "DEALER:",
            "self.dealer.pot",
            self.dealer.pot,
            "self.dealer.stage",
            self.dealer.stage,
            "self.dealer.button",
            self.dealer.button,
            "self.dealer.turn",
            self.dealer.turn,
            "self.dealer.to_call",
            self.dealer.to_call,
        )
        for player in self.players:
            print(
                player.name,
                player.chips,
                player.chips_in_front,
                player.acted,
                player.folded,
            )
        print(f"hands played {self.hands_played}")

    def move_button(self):
        self.button = 0 if self.button == len(self.players) - 1 else self.button + 1

    def _draw_dealer(self):
        just_text = f"POT: {self.dealer.pot} To call: {self.dealer.to_call}"
        pot_text = self.SCORE_FONT.render(
            f"{just_text}",
            True,
            self.WHITE,
        )
        self.window.blit(pot_text, (20, self.height - 75))

    def _draw_players(self):
        for i, player in enumerate(self.players):
            plr_score_text = self.SCORE_FONT.render(
                f"{'(D)' if self.button == i else ''}{player.name}: {player.chips} | {player.chips_in_front}",
                True,
                self.WHITE if self.dealer.turn != i else self.GREEN,
            )
            # hand = " ".join(
            #     map(str, [str(x["number"]) + x["suit"] for x in player.hand])
            # )
            # plr_hand_text = self.SCORE_FONT.render(hand, True, self.WHITE)
            self.window.blit(plr_score_text, (20, (i + 1) * 100))
            # self.window.blit(plr_hand_text, (425, (i + 1) * 50))
            for j, card in enumerate(player.hand, start=1):
                self.window.blit(card["img"], (400 + (j * 45), (i + 1) * 100))

    def draw(self):
        self.window.fill(self.BLACK)
        self._draw_dealer()
        self._draw_players()


def create_players(player_names, starting_chips):
    player_list = []
    for name in player_names:
        new_player = Player(name, starting_chips)
        player_list.append(new_player)
    return player_list


if __name__ == "__main__":
    players = ["Player1", "Player2", "Player3"]
    width, height = 1400, 800
    max_hands = 3
    window = pygame.display.set_mode((width, height))
    badugi = Badugi(window, width, height, players, 20000, max_hands)
    clock = pygame.time.Clock()

    badugi.main_loop()
    for player in badugi.players:
        print(player.name)
        print(player.chips)
    pygame.quit()
