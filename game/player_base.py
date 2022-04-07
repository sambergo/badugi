from .tools.get_winners import get_hand_rank
from .tools.sort_hand import sort_badugi_hand


class PlayerBase:
    """
    Badugi player.
    AI swaps x cards from sorted hand.
    """

    def __init__(self, name: str, chips: float):
        self.name = name
        self.chips = chips
        self.hand = []
        self.hand_rank: int = 1
        self.chips_in_front: float = 0
        self.folded: bool = False
        self.acted: bool = False
        self.swapped: bool = False

    def reset(self):
        self.hand = []
        self.chips_in_front = 0
        self.acted = False
        self.folded = False
        self.swapped = False
        self.hand_rank = 1

    def post_sb(self, dealer):
        self.chips_in_front += dealer.sb
        self.chips -= dealer.sb
        dealer.pot += dealer.sb

    def post_bb(self, dealer):
        self.chips_in_front += dealer.bb
        self.chips -= dealer.bb
        dealer.pot += dealer.bb

    def fold(self):
        self.chips_in_front = 0
        self.folded = True
        self.acted = True
        self.swapped = True

    def call(self, dealer):  # check/call
        cost_plr_to_call = dealer.to_call - self.chips_in_front
        self.chips_in_front += cost_plr_to_call
        self.chips -= cost_plr_to_call
        dealer.pot += cost_plr_to_call
        self.acted = True

    def bet(self, dealer, players):
        cost_plr_to_call = dealer.to_call - self.chips_in_front
        bet_size = dealer.bb if dealer.stage < 3 else dealer.bb * 2
        to_bet = cost_plr_to_call + bet_size
        self.chips_in_front += to_bet
        self.chips -= to_bet
        dealer.pot += to_bet
        dealer.to_call += bet_size
        dealer.street_bets += 1
        for player in players:
            if player.name != self.name and not player.folded:
                player.acted = False
        self.acted = True

    def swap_for_ai(self, dealer, n):
        for i in range(n):
            self.hand[3 - i] = dealer.deck.pop()
        self.hand = sort_badugi_hand(self.hand)
        self.hand_rank = get_hand_rank(self.hand)
        self.swapped = True
