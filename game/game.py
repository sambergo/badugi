from typing import List

import pygame

from .button import Button
from .dealer import Dealer, create_deck, deal_new_hand, finish_hand
from .draw_pygame import draw_game
from .game_base import BadugiBase
from .player import Player

pygame.init()


class Badugi(BadugiBase):
    """
    Play the game: play_ai()
    Pygame testing: test_without_ai()
    :intput:
        - player_names: List[str]
        - starting_chips: int
        - max_hands: int
        - window: pygame.display.set_mode()
        - width: int
        - height: int
    """

    BIG_FONT = pygame.font.SysFont("comicsans", 50)
    FONT = pygame.font.SysFont("comicsans", 22)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 128, 0)
    BIG_BLIND = 10
    BG = pygame.image.load("./PNG/table.png")
    AVATAR1 = pygame.transform.scale(
        pygame.image.load("./PNG/bear-face.png"), (100, 100)
    )
    AVATAR2 = pygame.transform.scale(
        pygame.image.load("./PNG/tiger-head.png"), (100, 100)
    )
    DEALER_BUTTON = pygame.transform.scale(
        pygame.image.load("./PNG/dealer_button.png"), (50, 50)
    )

    def __init__(
        self,
        player_names: List[str],
        starting_chips: float,
        max_hands: int,
        window: pygame.surface.Surface,
        width: int,
        height: int,
    ):
        super().__init__(player_names, starting_chips, max_hands)
        self.WINDOW = window
        self.WIDTH = width
        self.HEIGHT = height
        self.players = [Player(name, starting_chips) for name in player_names]
        self.dealer = Dealer(
            self.players, self.button, self.BB, create_deck(self.WINDOW)
        )
        self.clock = pygame.time.Clock()
        self.p1x = self.WIDTH // 4
        self.p1y = 50
        self.p2x = self.WIDTH // 4
        self.p2y = 600
        self.finish_hand = finish_hand
        self.deal_new_hand = deal_new_hand
        self.draw_game = draw_game

    def test_without_ai(self):
        """
        Test pygame with 2 human players.
        """
        run = True
        while run:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            # self.print_info()
            is_betting_stage = self.dealer.stage % 2 == 0
            # Main loop
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage >= self.MAX_STAGES:
                self.finish_hand(self)
            elif self.hand_active and is_betting_stage:  # TODO: Not only HU
                if self.dealer.turn == 0:
                    self.make_human_bet(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_human_bet(self.players[1])
                else:
                    print("ERROR" * 99)
            elif self.hand_active and not is_betting_stage:
                if self.dealer.turn == 0:
                    self.make_human_swap(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_human_swap(self.players[1])
                else:
                    print("ERROR" * 99)
            else:
                self.deal_new_hand(self)
            self.draw_game(self)
            pygame.display.update()
        return False

    def play_ai(self, ai_bet_net, ai_swap_net):
        """
        Play badugi against AI.
        :input:
            - ai_bet_net: neat.nn.FeedForwardNetwork.create()
            - ai_swap_net: neat.nn.FeedForwardNetwork.create()
        """
        run = True
        while run:
            is_betting_stage = self.dealer.stage % 2 == 0
            # Main loop
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage >= self.MAX_STAGES:
                self.finish_hand(self)
            elif self.hand_active and is_betting_stage:  # TODO: Not only HU
                if self.dealer.turn == 0:
                    self.make_human_bet(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_ai_bet_decision(self.players[1], ai_bet_net)
                else:
                    print("ERROR" * 99)
            elif self.hand_active and not is_betting_stage:
                if self.dealer.turn == 0:
                    self.make_human_swap(self.players[0])
                elif self.dealer.turn == 1:
                    self.make_ai_swap_decision(self.players[1], ai_swap_net)
                else:
                    print("ERROR" * 99)
            else:
                self.deal_new_hand(self)
            self.draw_game(self)
            pygame.display.update()
        return False

    def wait_for_human_bet(self, player, is_not_capped) -> int:
        """
        While loop waits until button is clicked. Returns decision: int.
        Updates pygame buttons.
        """
        waiting_decision = True
        is_call = player.chips_in_front < self.dealer.to_call
        button_texts = ["Fold", "Call" if is_call else "Check"]
        if is_not_capped:
            button_texts.append("Raise" if self.dealer.street_bets != 0 else "Bet")
        buttons = []
        dis_from_x = 700
        dis_from_y = 20
        bx = self.p1x + dis_from_x if self.dealer.turn == 0 else self.p2x + dis_from_x
        by = self.p1y + dis_from_y if self.dealer.turn == 0 else self.p2y + dis_from_y
        padding = 80
        for i, btn_text in enumerate(button_texts):
            button = Button(
                self.WINDOW, btn_text, (bx, by + (i * padding)), self.BIG_FONT
            )
            button.show()
            buttons.append(button)
        pygame.display.update()
        decision = 1
        while waiting_decision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                for i, btn in enumerate(buttons, start=1):
                    if btn.any_click(event):
                        decision = i
                        waiting_decision = False
            self.clock.tick(30)
        for btn in buttons:
            btn.show()
        pygame.display.update()
        return decision

    def wait_for_human_swap(self, player):
        """
        While loop waits until cards are selected and confirmed.
        Updates pygame buttons.
        """
        waiting_decision = True
        dis_from_x = 700
        dis_from_y = 50
        bx = self.p1x + dis_from_x if self.dealer.turn == 0 else self.p2x + dis_from_x
        by = self.p1y + dis_from_y if self.dealer.turn == 0 else self.p2y + dis_from_y
        confirm_button = Button(self.WINDOW, "Ready", (bx, by), self.BIG_FONT)
        confirm_button.show()
        pygame.display.update()
        while waiting_decision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                for card in player.hand:
                    card.any_click(event)
                if confirm_button.any_click(event):
                    waiting_decision = False
            self.clock.tick(30)

    def make_human_bet(self, player):
        is_not_capped = self.dealer.street_bets < self.dealer.cap
        decision = self.wait_for_human_bet(player, is_not_capped)
        if decision == 1:
            player.fold(self.dealer)
        elif decision == 3 and is_not_capped:
            player.bet(self.dealer, self.players)
        else:
            player.call(self.dealer)
        self.update_street(self)

    def make_human_swap(self, player):
        self.wait_for_human_swap(player)
        player.swap_for_human(self.dealer)
        self.update_street(self)

    # def print_info(self):
    #     print(
    #         f"""
    #         INFO:
    #         Hands played: {self.hands_played}
    #         Button: {self.dealer.button}
    #         Turn: {self.dealer.turn}
    #         Pot: {self.dealer.pot}
    #         Stage: {self.dealer.stage}
    #         {"-"*20}
    #         Player stack: {self.players[0].chips}
    #         AI stack: {self.players[1].chips}
    #         {"-"*20}
    #         AI hand:
    #         {[str(c.number)+c.suit for c in  self.players[1].hand]}
    #         Player hand:
    #         {[str(c.number)+c.suit for c in  self.players[0].hand]}
    #         {"-"*20}
    #             """
    #     )
