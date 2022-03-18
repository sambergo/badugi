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

    def move_chips(self, amount):
        self.chips += amount

    def post_sb(self, dealer):
        self.chips_in_front = dealer.sb
        dealer.pot += dealer.sb
        print("posted sb:", self.name)

    def post_bb(self, dealer):
        self.chips_in_front = dealer.sb
        dealer.pot += dealer.bb
        print("posted bb:", self.name)

    def fold(self, dealer):
        dealer.pot += self.chips_in_front
        self.chips_in_front = 0
        self.acted = True
        self.folded = True
        dealer.turn += 1
        print(self.name, " folded.")

    def call(self, dealer):
        to_call = dealer.to_call - self.chips_in_front
        self.chips_in_front += to_call
        self.chips -= to_call
        self.acted = True
        dealer.pot += to_call
        dealer.turn += 1
        print(self.name, " call:", self.chips_in_front)

    def bet(self, dealer):
        new_to_call = dealer.to_call + dealer.bb if dealer.stage < 2 else dealer.bb * 2
        to_complete_bet = new_to_call - self.chips_in_front
        self.chips_in_front += to_complete_bet
        self.chips -= to_complete_bet
        self.acted = True
        dealer.pot += to_complete_bet
        dealer.bet(self)
        print(self.name, " raise to:", self.chips_in_front, "cost:", to_complete_bet)


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
