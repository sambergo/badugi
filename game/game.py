from random import randrange

from .dealer import Dealer
from .player import Player
from .tools.get_winners import get_hand_rank, get_winners
from .tools.sort_hand import sort_badugi_hand


# testiin
class Badugi:
    """
    docstring for Badugi.
    """

    BIG_BLIND = 10
    MAX_HANDS = 3

    def __init__(self, player_names, starting_chips, max_hands):
        self.starting_chips = starting_chips
        self.players = create_players(player_names, starting_chips)
        self.button = randrange(0, len(player_names))
        self.MAX_HANDS = max_hands
        self.bb = self.BIG_BLIND
        self.sb = self.BIG_BLIND / 2
        self.hands_played = 0
        self.hand_active = False
        self.dealer = Dealer(self.players, self.button, self.bb)

    def main_loop(self):
        """
        Runs one:
            - deal_new_hand
            - finish_hand
            - next_street
            - hand_loop
        and updates drawnings
        """
        # Loop
        if self.hands_played >= self.MAX_HANDS:
            return False
        elif self.hand_active:
            self.draw_cards_loop()
        else:
            if self.hands_played < self.MAX_HANDS:
                self.deal_new_hand()
            else:
                pass

        return f"{self.hand_active} {self.hands_played} {self.dealer.turn} {self.dealer.stage} "

    def draw_cards_loop(self):
        x = input(f"{self.players[self.dealer.turn].name}: Montako vaihdetaan")
        self.players[self.dealer.turn].draw_number_of_cards(self.dealer, int(x))
        turns_left = len([player for player in self.players if player.draw])
        if turns_left == 0:
            self.next_street()
        # if turns_left != 1:
        self.dealer.next_turn(self.players, new_street=False)

    def next_street(self):
        self.dealer.next_turn(self.players, new_street=True)
        self.dealer.to_call = 0
        for player in self.players:
            if not player.folded:
                player.acted = False
                player.draw = True
        self.dealer.all_acted = False

    def deal_new_hand(self):
        """
        Plays a single hand:
            - create dealer
            - shuffle_deck
            - blinds
            - deal cards
            - preflop
            - change cards
            - award pot
            - move button
        :returns: Amount of chips of each player.
        """
        # Dealer
        self.dealer = Dealer(self.players, self.button, self.bb)
        self.dealer.shuffle_deck()
        self.hand_active = True
        # Blinds
        sb_index = (self.button + 1) % len(self.players)
        bb_index = (self.button + 2) % len(self.players)
        self.players[sb_index].post_sb(self.dealer)
        self.players[bb_index].post_bb(self.dealer)
        # Deal cards
        for player in self.players:
            player.reset()
            player_hand = []
            for i in range(4):  # type: ignore
                player_hand.append(self.dealer.deck.pop())
            player.hand = sort_badugi_hand(player_hand)
            player.hand.sort(key=lambda x: x["number"])
            player.hand_rank = get_hand_rank(player.hand)

    def finish_hand(self):
        # print("FINISH")
        winners = get_winners([player for player in self.players if not player.folded])
        for player in self.players:
            if player.name in winners:
                # print(f"WINNER: {player.name} amount_ {self.dealer.pot/len(winners)}")
                player.chips += self.dealer.pot / len(winners)
            player.reset()

        self.button = (self.button + 1) % len(self.players)
        self.hands_played += 1
        self.hand_active = False

    def print_info(self):
        print("INFO")
        print("turn:", self.players[self.dealer.turn].name)
        print(
            "DEALER:",
            "self.dealer.pot",
            self.dealer.pot,
            "self.dealer.stage",
            self.dealer.stage,
            "self.dealer.button",
            self.dealer.button,
            "self.dealer.turn",
            self.dealer.turn,
            "self.dealer.to_call",
            self.dealer.to_call,
        )
        for player in self.players:
            print(
                player.name,
                player.chips,
                player.chips_in_front,
                player.acted,
                player.folded,
            )
        print(f"hands played {self.hands_played}")

    def move_button(self):
        self.button = 0 if self.button == len(self.players) - 1 else self.button + 1


def create_players(player_names, starting_chips):
    player_list = []
    for name in player_names:
        new_player = Player(name, starting_chips)
        player_list.append(new_player)
    return player_list


if __name__ == "__main__":
    players = ["Player1", "Player2"]
    max_hands = 3
    badugi = Badugi(players, 20000, max_hands)

    badugi.main_loop()
    for player in badugi.players:
        print(player.name)
        print(player.chips)
