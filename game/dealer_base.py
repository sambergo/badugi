from __future__ import annotations

from random import shuffle
from typing import TYPE_CHECKING, List

from .card_base import CardBase
from .tools.get_winners import get_hand_rank, get_winners
from .tools.sort_hand import sort_badugi_hand

if TYPE_CHECKING:
    from .game_base import BadugiBase


class DealerBase:
    """
    New dealer is created for each hand.
    """

    def __init__(self, players, button: int, bb: float, deck):
        self.deck = deck
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
        self.prev_swap = 4

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


def create_deck_base() -> List[CardBase]:
    return [CardBase(suit, i) for suit in ["C", "D", "H", "S"] for i in range(1, 14)]


def finish_hand_base(badugi: "BadugiBase"):
    winners = get_winners([player for player in badugi.players if not player.folded])
    for player in badugi.players:
        if player.name in winners:
            player.chips += badugi.dealer.pot / len(winners)
        # player.reset()
    badugi.button = (badugi.button + 1) % len(badugi.players)
    badugi.hands_played += 1
    badugi.hand_active = False


def deal_new_hand(badugi: "BadugiBase"):
    """
    - Creates new dealer
    - Resets players
    - Posts blinds
    """
    new_deck = create_deck_base()
    badugi.dealer = DealerBase(badugi.players, badugi.button, badugi.BB, new_deck)
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


def next_street(badugi: "BadugiBase"):
    badugi.dealer.next_turn(badugi.players, new_street=True)
    badugi.dealer.to_call = 0
    for player in badugi.players:
        if not player.folded:
            player.acted = False
            player.swapped = False


def update_street(badugi: "BadugiBase"):
    """After player decision"""
    is_swap = badugi.dealer.stage % 2 == 1
    all_acted = all([p.acted for p in badugi.players])
    no_turns_left = all([p.swapped for p in badugi.players]) if is_swap else all_acted
    no_showdown = len([p for p in badugi.players if not p.folded]) == 1
    if no_turns_left and badugi.dealer.stage >= badugi.MAX_STAGES or no_showdown:
        badugi.finish_hand(badugi)
    elif no_turns_left and badugi.dealer.stage < badugi.MAX_STAGES or all_acted:
        next_street(badugi)
    else:
        badugi.dealer.next_turn(badugi.players, new_street=False)
