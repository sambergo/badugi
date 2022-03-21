from random import randrange

import pygame
from dealer import Dealer
from player import Player
from tools.get_winners import get_winners

pygame.init()


def create_players(players, starting_chips):
    player_list = []
    for player in players:
        new_player = Player(player, starting_chips)
        player_list.append(new_player)
    return player_list


class Badugi:
    """
    docstring for Badugi.
    """

    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BIG_BLIND = 10
    MAX_HANDS = 3

    def __init__(self, window, width, height, player_names, starting_chips, max_hands):
        # def __init__(self, players, starting_chips):
        self.window = window
        self.width = width
        self.height = height
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
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            # Loop
            only_one_left = (
                len([player for player in self.players if not player.folded]) == 1
            )
            if not self.hand_active and not self.hands_played >= self.MAX_HANDS:
                print("NEW HAND")
                self.deal_new_hand()
            elif self.hands_played >= self.MAX_HANDS:
                run = False
                break
            elif self.dealer.all_acted or only_one_left:
                if self.dealer.stage > 2:
                    self.finish_hand()
                else:
                    self.next_street()
            elif self.hand_active:
                self.hand_loop()
            else:
                print("ERROR")
            self.draw()
            pygame.display.update()

    # def get_next_turn(self):

    def next_street(self):
        self.dealer.stage += 1
        self.dealer.next_turn(self.players, new_street=True)
        self.dealer.to_call = 0
        for player in self.players:
            player.acted = False if not player.folded else True
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
            player_hand = []
            for i in range(4):  # type: ignore
                player_hand.append(self.dealer.deck.pop())
            player.hand = player_hand
            player.hand.sort(key=lambda x: x["number"])

    def hand_loop(self):
        # Betting rounds
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.players[self.dealer.turn].fold(self.dealer, self.players)
        elif keys[pygame.K_DOWN]:
            self.players[self.dealer.turn].call(self.dealer, self.players)
        elif keys[pygame.K_RIGHT]:
            self.players[self.dealer.turn].bet(self.dealer, self.players)
        elif keys[pygame.K_UP]:
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
        only_one_left = (
            len([player for player in self.players if not player.folded]) == 1
        )
        all_player_acted = all([player.acted for player in self.players])
        if all_player_acted or only_one_left:
            print("ALL ACTED")
            self.dealer.all_acted = True

    def finish_hand(self):
        print("FINISH")
        winners = get_winners([player for player in self.players if not player.folded])
        for player in self.players:
            if player.name in winners:
                print(f"WINNER: {player.name} amount_ {self.dealer.pot/len(winners)}")
                player.chips += self.dealer.pot / len(winners)
            player.reset()

        self.button = (self.button + 1) % len(self.players)
        self.hands_played += 1
        self.hand_active = False

    def move_button(self):
        self.button = 0 if self.button == len(self.players) - 1 else self.button + 1

    def _draw_dealer(self):
        just_text = f"POT: {self.dealer.pot} Turn: {self.players[self.dealer.turn].name}  To call: {self.dealer.to_call}"
        pot_text = self.SCORE_FONT.render(
            f"{just_text}",
            True,
            self.WHITE,
        )
        self.window.blit(pot_text, (20, 250))

    def _draw_player(self):
        for i, player in enumerate(self.players):
            plr_score_text = self.SCORE_FONT.render(
                f"{'(D)' if self.button == i else ''}{player.name}: {player.chips}",
                True,
                self.WHITE,
            )
            hand = " ".join(
                map(str, [str(x["number"]) + x["suit"] for x in player.hand])
            )
            plr_hand_text = self.SCORE_FONT.render(hand, True, self.WHITE)
            self.window.blit(plr_score_text, (20, (i + 1) * 50))
            self.window.blit(plr_hand_text, (425, (i + 1) * 50))

    def draw(self):
        self.window.fill(self.BLACK)

        self._draw_player()
        self._draw_dealer()


if __name__ == "__main__":
    players = ["Player1", "Player2", "Player3"]
    width, height = 700, 500
    max_hands = 1
    window = pygame.display.set_mode((width, height))
    badugi = Badugi(window, width, height, players, 20000, max_hands)
    clock = pygame.time.Clock()

    badugi.main_loop()
    for player in badugi.players:
        print(player.name)
        print(player.chips)
    pygame.quit()
