from random import shuffle


class Dealer:
    """
    docstring for Dealer.
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
        self.turn = (button + 3) % len(players)
        self.to_call = bb
        self.all_acted = False
        print(
            f"BUTTON: {self.button} btnplr: {players[self.button].name} turn: {self.turn}"
        )

    def collect(self, players):
        for player in players:
            self.pot += player.chips_in_front
            player.chips_in_front = 0

    # def award(self, winners, players):
    #     for winner in winners:
    #         winner.move_chips(self.pot / len(winners))
    #     for player in players:
    #         player.reset()

    def shuffle_deck(self):
        shuffle(self.deck)

    def get_next_turn_index(self, players, start):
        end = start + len(players)
        for i in range(start, end):
            if not players[i % end].folded:
                return i
        print("ERROR AT nextturn")
        return 0

    def next_turn(self, players, new_street=False):
        if new_street:
            start = (self.button + 1) % self.players_length
            self.turn = self.get_next_turn_index(players, start)
            self.to_call = 0
            for player in players:
                player.chips_in_front = 0
        else:
            start = (self.turn + 1) % self.players_length
            self.turn = self.get_next_turn_index(players, start)


def create_deck():
    suits = ["c", "d", "h", "s"]
    deck = []
    for suit in suits:
        for i in range(1, 14):
            deck.append({"suit": suit, "number": i, "replace": False})
    return deck
