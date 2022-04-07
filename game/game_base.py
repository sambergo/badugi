from random import randrange
from typing import List

import neat

from .dealer_base import (
    DealerBase,
    create_deck_base,
    deal_new_hand,
    finish_hand_base,
    update_street,
)
from .player_base import PlayerBase
from .tools.get_winners import get_hand_rank


class BadugiBase:
    """
    Train AI:
        - train_swap
        - train_betting
    *_base.py files are for AI evolving and do not load pygame, images or other heavy stuff.
    """

    BIG_BLIND = 10

    def __init__(
        self,
        player_names: List[str],
        starting_chips: float,
        max_hands: int,
    ):
        self.STARTING_CHIPS = starting_chips
        self.players = [PlayerBase(name, starting_chips) for name in player_names]
        self.button = randrange(0, len(player_names))
        self.MAX_HANDS = max_hands
        self.BB = float(self.BIG_BLIND)
        self.SB = float(self.BIG_BLIND / 2)
        self.hands_played = 0
        self.hand_active = False
        self.dealer = DealerBase(self.players, self.button, self.BB, create_deck_base())
        self.is_not_training = False
        self.MAX_STAGES = 7
        self.finish_hand = finish_hand_base
        self.update_street = update_street
        self.deal_new_hand = deal_new_hand

    def train_only_swap(self, genome1, genome2, config):
        """
        Train the AI by passing two NEAT neural networks and the NEAt config object.
        AI needs to be tought how swap cards first when starting to evolve AI from zero.
        """
        self.genome1 = genome1
        self.genome2 = genome2
        net0 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net1 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.is_not_training = False
        run = True
        while run:
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage % 2 == 0:
                self.dealer.stage += 1
            elif self.hand_active and self.dealer.stage < self.MAX_STAGES:
                if self.dealer.turn == 0:
                    self.make_ai_swap_decision(self.players[0], net0)
                elif self.dealer.turn == 1:
                    self.make_ai_swap_decision(self.players[1], net1)
            elif self.dealer.stage >= self.MAX_STAGES and self.hand_active:
                self.finish_hand(self)
            else:
                self.deal_new_hand(self)
        self.calculate_fitness()
        return False

    def train_swap(self, genome1, genome2, config, ai_bet_net):
        """
        These AI's will play against eachother to determine their fitness.
        Takes evolved ai_bet_net: neat.nn.FeedForwardNetwork.create()
        Only for HU atm.
        """
        self.genome1 = genome1
        self.genome2 = genome2
        net0 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net1 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.is_not_training = False
        run = True
        while run:
            is_swap_stage = self.dealer.stage % 2 == 1
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage >= self.MAX_STAGES:
                self.finish_hand(self)
            elif self.hand_active and is_swap_stage:
                if self.dealer.turn == 0:
                    self.make_ai_swap_decision(self.players[0], net0)
                elif self.dealer.turn == 1:
                    self.make_ai_swap_decision(self.players[1], net1)
            elif self.hand_active and not is_swap_stage:
                if self.dealer.turn == 0:
                    self.make_ai_bet_decision(self.players[0], ai_bet_net)
                elif self.dealer.turn == 1:
                    self.make_ai_bet_decision(self.players[1], ai_bet_net)
            else:
                self.deal_new_hand(self)
        self.calculate_fitness()
        return False

    def train_betting(self, genome1, genome2, config, ai_swap_net):
        """
        These AI's will play against eachother to determine their fitness.
        :input:
            - 2 neat-python genomes
            - neat-python config
            - evolved ai_swap_net: neat.nn.FeedForwardNetwork.create()
        """
        self.genome1 = genome1
        self.genome2 = genome2
        net0 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net1 = neat.nn.FeedForwardNetwork.create(genome2, config)
        run = True
        while run:
            is_betting_stage = self.dealer.stage % 2 == 0
            if self.hands_played >= self.MAX_HANDS:
                run = False
            elif self.hand_active and self.dealer.stage >= self.MAX_STAGES:
                self.finish_hand(self)
            elif self.hand_active and is_betting_stage:  # TODO: Not only HU
                if self.dealer.turn == 0:
                    self.make_ai_bet_decision(self.players[0], net0)
                elif self.dealer.turn == 1:
                    self.make_ai_bet_decision(self.players[1], net1)
            elif self.hand_active and not is_betting_stage:
                if self.dealer.turn == 0:
                    self.make_ai_swap_decision(self.players[0], ai_swap_net)
                elif self.dealer.turn == 1:
                    self.make_ai_swap_decision(self.players[1], ai_swap_net)
            else:
                self.deal_new_hand(self)
        self.calculate_fitness()
        return False

    def make_ai_bet_decision(self, player, net):
        is_not_capped = self.dealer.cap > self.dealer.street_bets
        hand_rank = get_hand_rank(player.hand)
        output = net.activate(
            (hand_rank, self.dealer.stage, self.dealer.pot, player.chips_in_front)
        )
        decision = output.index(max(output))
        if decision == 0:
            player.fold()
        elif decision == 2 and is_not_capped:
            player.bet(self.dealer, self.players)
        else:
            player.call(self.dealer)
        self.update_street(self)

    def make_ai_swap_decision(self, player, net):
        old_rank = get_hand_rank(player.hand)
        rank_with_3 = get_hand_rank(player.hand[:3])
        rank_with_2 = get_hand_rank(player.hand[:2])
        rank_with_1 = get_hand_rank(player.hand[:1])
        output = net.activate(
            (self.dealer.stage, old_rank, rank_with_3, rank_with_2, rank_with_1)
        )
        decision = output.index(max(output))
        player.swap_for_ai(self.dealer, decision)
        self.update_street(self)

    def calculate_fitness(self):
        """
        Update neat-python genomes
        """
        self.genome1.fitness += self.players[0].chips - self.STARTING_CHIPS
        self.genome2.fitness += self.players[1].chips - self.STARTING_CHIPS
