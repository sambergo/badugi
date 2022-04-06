from .tools.get_winners import get_hand_rank
from .tools.sort_hand import sort_badugi_hand


class Player:
    """
    docstring for Player.
    """

    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.hand_rank = 1
        self.chips_in_front = 0
        self.folded = False
        self.acted = False
        self.swapped = False
        self.vaihdot = 0

    def reset(self):
        self.hand = []
        self.chips_in_front = 0
        self.acted = False
        self.folded = False
        self.swapped = False
        self.vaihdot = 0
        self.hand_rank = 1

    def move_chips(self, amount):
        self.chips += amount

    def post_sb(self, dealer):
        self.chips_in_front += dealer.sb
        self.chips -= dealer.sb
        dealer.pot += dealer.sb
        action_msg = f"{self.name} posts {dealer.sb}."
        dealer.actions.append(action_msg)

    def post_bb(self, dealer):
        self.chips_in_front += dealer.bb
        self.chips -= dealer.bb
        dealer.pot += dealer.bb
        action_msg = f"{self.name} posts {dealer.bb}."
        dealer.actions.append(action_msg)

    def fold(self, dealer):
        self.chips_in_front = 0
        self.folded = True
        self.acted = True
        self.swapped = True
        action_msg = f"{self.name} folds."
        dealer.actions.append(action_msg)

    def call(self, dealer):  # check/call
        is_call = dealer.to_call > self.chips_in_front
        cost_plr_to_call = dealer.to_call - self.chips_in_front
        self.chips_in_front += cost_plr_to_call
        self.chips -= cost_plr_to_call
        dealer.pot += cost_plr_to_call
        self.acted = True
        action_msg = (
            f"{self.name} calls {dealer.to_call}."
            if is_call
            else f"{self.name} checks."
        )
        dealer.actions.append(action_msg)

    def bet(self, dealer, players):
        print("self.chips_in_front:", self.chips_in_front)
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
        action_msg = f"{self.name} raises to {dealer.to_call}."
        dealer.actions.append(action_msg)
        self.acted = True

    def draw_number_of_cards(self, dealer, n):
        if self.vaihdot > 4:
            print("ERROR", self.vaihdot)
        if len(dealer.deck) < 15:
            print("ERROR deck", len(dealer.deck), dealer.actions)
        for i in range(n):
            try:
                self.hand[3 - i] = dealer.deck.pop()
            except:
                print("kortit loppu", dealer.deck)
                raise
        self.vaihdot += 1
        action_msg = f"Player {self.name} draws {n}."
        dealer.actions.append(action_msg)
        self.hand = sort_badugi_hand(self.hand)
        self.hand_rank = get_hand_rank(self.hand)
        self.swapped = True

    def select_card(self, card):
        old_bool = self.hand[card]["selected"]
        self.hand[card]["selected"] = not old_bool
        # print("selected", card)
