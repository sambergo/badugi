from .tools.get_winners import get_hand_rank
from .tools.sort_hand import sort_badugi_hand


class Player:
    """
    Badugi player.
    AI swaps x cards from sorted hand.
    Humans swap selected cards.
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

    def reset(self):
        self.hand = []
        self.chips_in_front = 0
        self.acted = False
        self.folded = False
        self.swapped = False
        self.hand_rank = 1

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
        action_msg = f"{self.name} {'raises' if dealer.street_bets != 0 else 'bets' } to {dealer.to_call}."
        dealer.actions.append(action_msg)
        self.acted = True

    def swap_for_ai(self, dealer, n):
        for i in range(n):
            self.hand[3 - i] = dealer.deck.pop()
        action_msg = f"Player {self.name} draws {n}."
        dealer.actions.append(action_msg)
        self.hand = sort_badugi_hand(self.hand)
        self.hand_rank = get_hand_rank(self.hand)
        self.swapped = True

    def swap_for_human(self, dealer):
        n = 0
        for i, card in enumerate(self.hand):
            if card.selected:
                self.hand[i] = dealer.deck.pop()
                n += 1
        action_msg = f"Player {self.name} draws {n}."
        dealer.actions.append(action_msg)
        self.hand = sort_badugi_hand(self.hand)
        self.hand_rank = get_hand_rank(self.hand)
        self.swapped = True


def create_players(player_names, starting_chips):
    player_list = []
    for name in player_names:
        new_player = Player(name, starting_chips)
        player_list.append(new_player)
    return player_list
