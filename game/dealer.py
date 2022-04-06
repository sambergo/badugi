import os
from random import shuffle
from typing import List

import pygame


class Dealer:
    """
    New dealer is created for each hand.
    """

    def __init__(self, players, button, bb):
        self.deck = create_deck()
        self.bb = bb
        self.sb = bb / 2
        self.pot = 0
        self.stage = 0
        self.players_length = len(players)
        self.cap = 4
        self.street_bets = 1
        self.button = button
        self.turn = (
            button if self.players_length == 2 else (button + 3) % self.players_length
        )
        self.to_call = bb
        self.all_acted = False
        self.actions: List[str] = []

    def shuffle_deck(self):
        shuffle(self.deck)

    def next_turn(
        self,
        players,
        new_street=False,
    ):
        if new_street:
            start = (self.button + 1) % self.players_length
            self.turn = get_next_turn_index(players, start)
            self.to_call = 0
            self.stage += 1
            self.street_bets = 0
            for player in players:
                player.chips_in_front = 0
        else:
            start = (self.turn + 1) % self.players_length
            self.turn = get_next_turn_index(players, start)


def get_next_turn_index(players, start):
    pl = len(players)
    for i in range(start, start + pl):
        if not players[i % pl].folded:
            return i % pl
    return -1


def create_deck():

    suits = ["C", "D", "H", "S"]
    deck = []
    for suit in suits:
        for i in range(1, 14):
            img_src = pygame.image.load(os.path.join("PNG", f"{str(i)}{suit}.png"))
            img = pygame.transform.scale(img_src, (100, 175))
            deck.append({"suit": suit, "number": i, "selected": False, "img": img})

    # deck = [
    #     {"suit": suit, "number": number}
    #     for suit in ["C", "D", "H", "S"]
    #     for number in range(1, 14)
    # ]

    return deck
