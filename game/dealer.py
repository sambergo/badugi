from random import shuffle


class Dealer:
    """
    docstring for Dealer.
    """

    def __init__(self, players, button, bb):
        self.players = players
        self.deck = create_deck()
        self.bb = bb
        self.sb = bb / 2
        self.pot = 0
        self.stage = 0
        self.cap = 4
        self.to_cap = self.cap
        self.button = button
        self.turn = (button + 2) % len(players)
        self.to_call = bb

    def collect(self):
        for player in self.players:
            self.pot += player.chips_in_front
            player.chips_in_front = 0

    def award(self, winners):
        for winner in winners:
            winner.move_chips(self.pot / len(winners))
        self.pot = 0
        self.stage = 0
        for player in self.players:
            player.reset()

    def shuffle_deck(self):
        shuffle(self.deck)

    # def fold(self, chips_in_front):
    #     self.pot += chips_in_front
    #     self.turn = (self.turn + 1) % len(self.players)

    # def call(self):
    #     self.turn = (self.turn + 1) % len(self.players)

    def bet(self, bettor):
        for player in self.players:
            if player.name != bettor.name and not player.folded:
                player.acted = True
        self.turn = (self.turn + 1) % len(self.players)


def create_deck():
    suits = ["c", "d", "h", "s"]
    cards = []
    for suit in suits:
        for i in range(1, 14):
            cards.append({"suit": suit, "number": i})
    return cards
