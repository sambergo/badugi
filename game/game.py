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


def get_blind_position(button, players_length, sb=True):
    return button + 1 if sb else 2 % players_length
    # if players_length == 2:
    #     if sb:
    #         return button
    #     else:
    #         return 1 if button == 0 else 0
    # elif sb and button + 1 == players_length:
    #     return 0
    # elif sb:
    #     return button + 1
    # elif button + 2 == players_length:
    #     return 0
    # elif button + 1 == players_length:
    #     return 1
    # else:
    #     return button + 2


class Badugi:
    """
    docstring for Badugi.
    """

    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BIG_BLIND = 10

    def __init__(self, window, width, height, players, starting_chips):
        # def __init__(self, players, starting_chips):
        self.window = window
        self.width = width
        self.height = height
        self.starting_chips = starting_chips
        self.players = create_players(players, starting_chips)
        self.button = randrange(0, len(players))
        self.bb = self.BIG_BLIND
        self.sb = self.BIG_BLIND / 2
        self.hands_played = 0

    def deal_hand(self):
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
        dealer = Dealer(self.players, self.button, self.bb)
        dealer.shuffle_deck()

        print("self.button:", self.button)
        # Blinds
        # sb = get_blind_position(self.button, len(self.players), sb=True)
        # bb = get_blind_position(self.button, len(self.players), sb=False)
        sb = (self.button + 1) % len(self.players)
        print("sb:", sb)
        bb = (self.button + 2) % len(self.players)
        print("bb:", bb)
        self.players[sb].post_sb(dealer)
        self.players[bb].post_bb(dealer)

        # Deal cards
        for player in self.players:
            player_hand = []
            for i in range(4):
                player_hand.append(dealer.deck.pop())
            player.hand = player_hand
            player.hand.sort(key=lambda x: x["number"])

        # Betting rounds
        run = True
        while run:
            for player in self.players:
                if "1" in player.name:
                    player.bet(dealer)
                else:
                    player.call(dealer)
            if not any([player.acted for player in self.players]):
                run = False
            run = False

        # Find winner
        dealer.collect()
        winners = get_winners(self.players)

        # Award pot
        dealer.award(winners)
        self.button = self.button + 1 % len(self.players)
        self.hands_played += 1

    def move_button(self):
        self.button = 0 if self.button == len(self.players) - 1 else self.button + 1

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

    # def _draw_divider(self):
    #     for i in range(10, self.window_height, self.window_height//20):
    #         if i % 2 == 1:
    #             continue
    #         pygame.draw.rect(
    #             self.window, self.WHITE, (self.window_width//2 - 5, i, 10, self.window_height//20))

    def draw(self):
        self.window.fill(self.BLACK)

        # self._draw_divider()

        self._draw_player()

        # if draw_hits:
        #     self._draw_hits()

        # for paddle in [self.left_paddle, self.right_paddle]:
        #     paddle.draw(self.window)

        # self.ball.draw(self.window)


if __name__ == "__main__":
    players = ["Player1", "Player2"]
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    badugi = Badugi(window, width, height, players, 20000)
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        badugi.draw()
        badugi.deal_hand()
        badugi.draw()
        pygame.display.update()
        if badugi.hands_played > 9:
            run = False
        if not run:
            break
    for player in badugi.players:
        print(player.name)
        print(player.chips)
    pygame.quit()
