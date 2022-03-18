from random import randrange

import pygame
from dealer import Dealer
from player import Player
from tools.get_winners import get_winners

pygame.init()


def create_players(players, starting_chips):
    player_list = []
    for player in players:
        new_player = Player(player, starting_chips)
        player_list.append(new_player)
    return player_list


def get_blind_position(button, players_length, sb=True):
    if players_length == 2:
        if sb:
            return button
        else:
            return 1 if button == 0 else 0
    elif sb and button + 1 == players_length:
        return 0
    elif sb:
        return button + 1
    elif button + 2 == players_length:
        return 0
    elif button + 1 == players_length:
        return 1
    else:
        return button + 2


# def get_winner(players):
#     """
#     Ac 2d 3h 4s
#     """
#     best_badugi = 0
#     best_high = [14]
#     winners = []
#     for player in players:
#         badugi_hand = []
#         for card in player.hand:
#             has_suit = card["suit"] in [bhc["suit"] for bhc in badugi_hand]
#             has_number = card["number"] in [bhc["number"] for bhc in badugi_hand]
#             if not has_suit and not has_number:
#                 badugi_hand.insert(0, card)
#         if len(badugi_hand) > best_badugi:
#             winners = [player]
#             best_badugi = len(badugi_hand)
#             best_high = [bhc["number"] for bhc in badugi_hand]
#         elif len(badugi_hand) == best_badugi:
#             same_hand = True
#             for i, card in enumerate(badugi_hand):
#                 if card["number"] < best_high[i]:
#                     winners = [player]
#                     new_best_high = [bhc["number"] for bhc in badugi_hand]
#                     best_high = new_best_high
#                     same_hand = False
#                     break
#                 elif card["number"] > best_high[i]:
#                     same_hand = False
#                     break
#             if same_hand:
#                 winners.append(player)
#     return winners


class Badugi:
    """
    docstring for Badugi.
    """

    # def __init__(self, window, width, height, players, starting_chips):
    def __init__(self, players, starting_chips):
        # self.window = window
        # self.width = width
        # self.height = height
        self.starting_chips = starting_chips
        self.players = create_players(players, starting_chips)
        self.button = randrange(0, len(players))
        self.sb = 5
        self.bb = 10

    def deal_hand(self):
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
        dealer = Dealer(self.players)
        dealer.shuffle_deck()

        # Blinds
        sb = get_blind_position(self.button, len(self.players), sb=True)
        bb = get_blind_position(self.button, len(self.players), sb=False)
        self.players[sb].bet(self.sb)
        self.players[bb].bet(self.bb)

        # Deal cards
        for player in self.players:
            player_hand = []
            for i in range(4):
                player_hand.append(dealer.deck.pop())
            player.hand = player_hand
            player.hand.sort(key=lambda x: x["number"])

        # Find winner
        dealer.collect()
        winners = get_winners(self.players)

        # Award pot
        dealer.award(winners)
        self.move_button()

    def move_button(self):
        self.button = 0 if self.button == len(self.players) - 1 else self.button + 1


if __name__ == "__main__":
    players = ["Player1", "Player2"]
    badugi = Badugi(players, 1000)
    for i in range(20000):
        badugi.deal_hand()
    for player in badugi.players:
        print(player.name)
        print(player.chips)
