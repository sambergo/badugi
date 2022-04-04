import os
from random import shuffle


class Dealer:
    """
    New dealer is created for each hand.
    """

    def __init__(self, players, button, bb):
        self.deck = create_deck()
        self.bb = bb
        self.sb = bb / 2
        self.pot = 0
        self.stage = 0
        self.players_length = len(players)
        self.cap = 4
        self.to_cap = self.cap
        self.button = button
        # self.turn = (button + 3) % len(players) if len(players) != 2 else button
        self.turn = (self.button + 1) % 2
        self.to_call = bb
        self.all_acted = False
        self.vaihtajat = []

    def shuffle_deck(self):
        shuffle(self.deck)

    def next_turn(
        self,
        players,
        new_street=False,
    ):
        # HUOM! muutettu kun vaan vaihdellaan kortteja
        if new_street:
            self.turn = (self.button + 1) % 2
            self.to_call = 0
            self.stage += 1
            for player in players:
                player.chips_in_front = 0
        else:
            self.turn = self.button

        # if new_street:
        #     start = (self.button + 1) % self.players_length
        #     self.turn = get_next_turn_index(players, start)
        #     self.to_call = 0
        #     self.stage += 1
        #     # print("NEW STREET", self.stage)
        #     for player in players:
        #         player.chips_in_front = 0
        # else:
        #     start = (self.turn + 1) % self.players_length
        #     self.turn = get_next_turn_index(players, start)


def get_next_turn_index(players, start):
    pl = len(players)
    for i in range(start, start + pl):
        if not players[i % pl].folded:
            return i % pl
    return -1


def create_deck():

    # suits = ["C", "D", "H", "S"]
    # deck = []
    # for suit in suits:
    #     for i in range(1, 14):
    #         img_src = pygame.image.load(os.path.join("PNG", f"{str(i)}{suit}.png"))
    #         img = pygame.transform.scale(img_src, (100, 175))
    #         deck.append({"suit": suit, "number": i, "selected": False, "img": img})

    deck = [
        {"suit": suit, "number": number}
        for suit in ["C", "D", "H", "S"]
        for number in range(1, 14)
    ]

    return deck
