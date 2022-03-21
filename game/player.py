class Player:
    """
    docstring for Player.
    """

    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.chips_in_front = 0
        self.acted = False
        self.folded = False

    def reset(self):
        self.hand = []
        self.chips_in_front = 0
        self.acted = False
        self.folded = False

    def move_chips(self, amount):
        self.chips += amount

    def post_sb(self, dealer):
        self.chips_in_front = dealer.sb
        self.chips -= dealer.sb
        dealer.pot += dealer.sb
        print("posted sb:", self.name, dealer.sb)

    def post_bb(self, dealer):
        self.chips_in_front = dealer.bb
        self.chips -= dealer.bb
        dealer.pot += dealer.bb
        print("posted bb:", self.name, dealer.bb)

    def fold(self, dealer, players):
        self.chips_in_front = 0
        self.folded = True
        self.acted = True
        dealer.next_turn(players)
        print(self.name, " folded.")

    def call(self, dealer, players):
        to_call = dealer.to_call - self.chips_in_front
        self.chips_in_front += to_call
        self.chips -= to_call
        dealer.pot += to_call
        dealer.next_turn(players)
        self.acted = True
        print(self.name, " call:", self.chips_in_front)

    def bet(self, dealer, players):
        to_call = dealer.to_call - self.chips_in_front
        print("to_call:", to_call)
        bet_size = dealer.bb if dealer.stage < 2 else dealer.bb * 2
        print("bet_size:", bet_size)
        to_bet = to_call + bet_size
        print("to_bet:", to_bet)
        self.chips_in_front += to_bet
        self.chips -= to_bet
        dealer.pot += to_bet
        # dealer.bet(self)
        dealer.to_call += bet_size
        dealer.next_turn(players)
        for player in players:
            if player.name != self.name and not player.folded:
                player.acted = False
        print(self.name, " raise to:", self.chips_in_front, "cost:", dealer.to_call)
        self.acted = True


# def act(self, dealer, action, amount):
#     if action == 0:
#         dealer.fold(self.chips_in_front)
#         self.acted = True
#         self.folded = True
#         self.chips_in_front = 0
#         print(self.name, " folded.")
#     elif action == 1:
#         dealer.call()
#         self.chips_in_front += amount
#         self.chips -= amount
#         self.acted = True
#         print(self.name, " call:", self.chips_in_front)
#     elif action == 2:
#         dealer.bet(self)
#         self.chips_in_front += amount
#         self.chips -= amount
#         self.acted = True
