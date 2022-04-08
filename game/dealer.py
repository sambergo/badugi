from __future__ import annotations

import os
from typing import TYPE_CHECKING, List

import pygame

from .card import Card
from .dealer_base import DealerBase
from .draw_pygame import draw_finish_game
from .tools.get_winners import get_hand_rank, get_winners
from .tools.sort_hand import sort_badugi_hand

if TYPE_CHECKING:
    from .game import Badugi


class Dealer(DealerBase):
    """
    New dealer is created for each hand.
    """

    def __init__(self, players, button, bb, deck, actions=[]):
        super().__init__(players, button, bb, deck)
        self.actions: List[str] = actions


def create_deck(window) -> List[Card]:
    return [
        Card(
            window,
            suit,
            i,
            pygame.image.load(os.path.join("PNG", f"{str(i)}{suit}.png")),
        )
        for suit in ["C", "D", "H", "S"]
        for i in range(1, 14)
    ]


# TODO : Parempi tapa ettei tulis toistoa?
def finish_hand(badugi: "Badugi"):
    draw_finish_game(badugi)
    winners = get_winners([player for player in badugi.players if not player.folded])
    for player in badugi.players:
        if player.name in winners:
            amount = {badugi.dealer.pot / len(winners)}
            hand = {", ".join([str(c.number) + c.suit for c in player.hand])}
            badugi.dealer.actions.append(f"{player.name} won {amount} ({hand})")
            player.chips += badugi.dealer.pot / len(winners)
        elif not player.folded:
            hand = {", ".join([str(c.number) + c.suit for c in player.hand])}
            badugi.dealer.actions.append(f"{player.name} mucked {hand} ")
        # player.reset()
    badugi.button = (badugi.button + 1) % len(badugi.players)
    badugi.hands_played += 1
    badugi.hand_active = False


def deal_new_hand(badugi: "Badugi"):
    """
    - Creates new dealer
    - Resets players
    - Posts blinds
    """
    badugi.dealer.actions.append(f"Hand #{badugi.hands_played+1}")
    new_deck = create_deck(badugi.WINDOW)
    badugi.dealer = Dealer(badugi.players, badugi.button, badugi.BB, new_deck)
    badugi.dealer.shuffle_deck()
    badugi.hand_active = True
    # Deal cards
    for player in badugi.players:
        player.reset()
        player_hand = []
        for _ in range(4):
            player_hand.append(badugi.dealer.deck.pop())
        player.hand = sort_badugi_hand(player_hand)
        player.hand_rank = get_hand_rank(player.hand)
    # Blinds
    pl = len(badugi.players)
    sb_index = badugi.button if pl == 2 else (badugi.button + 1) % pl
    bb_index = (badugi.button + 1) % pl if pl == 2 else (badugi.button + 2) % pl
    badugi.players[sb_index].post_sb(badugi.dealer)
    badugi.players[bb_index].post_bb(badugi.dealer)
