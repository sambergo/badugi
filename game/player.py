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
        self.draw = True
        self.chips_in_front = 0
        self.acted = False
        self.folded = False
        self.vaihdot = 0

    def reset(self):
        self.hand = []
        self.chips_in_front = 0
        self.acted = False
        self.folded = False
        self.draw = True
        self.vaihdot = 0
        self.hand_rank = 1

    def move_chips(self, amount):
        self.chips += amount

    def post_sb(self, dealer):
        self.chips_in_front = dealer.sb
        self.chips -= dealer.sb
        dealer.pot += dealer.sb
        # print("posted sb:", self.name, dealer.sb)

    def post_bb(self, dealer):
        self.chips_in_front = dealer.bb
        self.chips -= dealer.bb
        dealer.pot += dealer.bb
        # print("posted bb:", self.name, dealer.bb)

    def fold(self):
        self.chips_in_front = 0
        self.folded = True
        self.acted = True
        self.draw = False
        print(self.name, " folded.")

    def call(self, dealer):
        to_call = dealer.to_call - self.chips_in_front
        self.chips_in_front += to_call
        self.chips -= to_call
        dealer.pot += to_call
        self.acted = True
        print(self.name, " call:", self.chips_in_front)

    def bet(self, dealer, players):
        to_call = dealer.to_call - self.chips_in_front
        bet_size = dealer.bb if dealer.stage < 3 else dealer.bb * 2
        to_bet = to_call + bet_size
        self.chips_in_front += to_bet
        self.chips -= to_bet
        dealer.pot += to_bet
        dealer.to_call += bet_size
        for player in players:
            if player.name != self.name and not player.folded:
                player.acted = False
        print(self.name, " raise to:", self.chips_in_front, "cost:", dealer.to_call)
        self.acted = True

    def draw_number_of_cards(self, dealer, n):
        if self.vaihdot > 4:
            print("ERROR", self.vaihdot)
        if len(dealer.deck) < 15:
            print("ERROR deck", len(dealer.deck), dealer.vaihtajat)
        for i in range(n):
            try:
                self.hand[3 - i] = dealer.deck.pop()
            except:
                print("kortit loppu", dealer.deck)
                raise
        self.vaihdot += 1
        vaihto = f"Stage: {dealer.stage}, Vaihtaja: {self.name}, N:{n}"
        dealer.vaihtajat.append(vaihto)
        self.hand = sort_badugi_hand(self.hand)
        self.hand_rank = get_hand_rank(self.hand)
        self.draw = False

    def select_card(self, card):
        old_bool = self.hand[card]["selected"]
        self.hand[card]["selected"] = not old_bool
        # print("selected", card)

    def draw_cards(self, dealer):
        for i, card in enumerate(self.hand):
            if card["selected"]:
                self.hand[i] = dealer.deck.pop()
        self.hand.sort(key=lambda x: x["number"])
        self.hand_rank = get_hand_rank(self.hand)
        self.draw = False
