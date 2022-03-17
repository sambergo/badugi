from random import shuffle


class Deck:
    """
    docstring for Deck.
    """

    def __init__(self):
        self.cards = create_deck()

    def shuffle_deck(self):
        shuffle(self.cards)


def create_deck():
    suits = ["c", "d", "h", "s"]
    cards = []
    for suit in suits:
        for i in range(1, 14):
            cards.append({"suit": suit, "number": i})
    return cards
