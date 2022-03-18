from random import shuffle


class Dealer:
    """
    docstring for Dealer.
    """

    def __init__(self, players):
        self.players = players
        self.pot = 0
        self.deck = create_deck()

    def collect(self):
        for player in self.players:
            self.pot += player.chips_in_front
            player.chips_in_front = 0

    def award(self, winners):
        for winner in winners:
            winner.move_chips(self.pot / len(winners))
        self.pot = 0

    def shuffle_deck(self):
        shuffle(self.deck)


def create_deck():
    suits = ["c", "d", "h", "s"]
    cards = []
    for suit in suits:
        for i in range(1, 14):
            cards.append({"suit": suit, "number": i})
    return cards
