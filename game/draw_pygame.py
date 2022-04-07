from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .game import Badugi


def draw_game(badugi: "Badugi"):
    badugi.WINDOW.fill(badugi.BLACK)
    badugi.WINDOW.blit(badugi.BG, (0, 0))
    draw_dealer(badugi)
    draw_players(badugi)


def draw_finish_game(badugi: "Badugi"):
    if badugi.is_not_training:
        draw_players(badugi, False)
        pygame.display.update()
        pygame.time.wait(2000)


def draw_dealer(badugi: "Badugi"):
    dx = badugi.WIDTH // 3
    dy = badugi.HEIGHT // 2.6
    text = badugi.BIG_FONT.render(f"Pot: {badugi.dealer.pot}", True, badugi.WHITE)
    badugi.WINDOW.blit(text, (dx, dy))
    text = badugi.BIG_FONT.render(
        f"Draws left: {3 - badugi.dealer.stage // 2}", True, badugi.WHITE
    )
    badugi.WINDOW.blit(text, (dx, dy + 50))
    # Actions on left side
    for i, msg in enumerate(badugi.dealer.actions[-10:]):
        text = badugi.FONT.render(msg, True, badugi.WHITE)
        badugi.WINDOW.blit(text, (20, 50 + (i * 30)))


def draw_players(badugi: "Badugi", not_showdown=True):  # TODO: multiplayer
    # Player 1
    text = badugi.BIG_FONT.render(
        badugi.players[0].name,
        True,
        "yellow" if badugi.dealer.turn == 0 else badugi.WHITE,
    )
    badugi.WINDOW.blit(text, (badugi.p1x, badugi.p1y))
    text = badugi.FONT.render(str(badugi.players[0].chips), True, badugi.WHITE)
    badugi.WINDOW.blit(text, (badugi.p1x, badugi.p1y + 40))
    badugi.WINDOW.blit(badugi.AVATAR1, (badugi.p1x, badugi.p1y + 70))
    for i, card in enumerate(badugi.players[0].hand):
        card.show(((badugi.p1x + 200) + (i * 100), badugi.p1y), show_back=False)
    if badugi.players[0].chips_in_front != 0:
        text = badugi.BIG_FONT.render(
            str(int(badugi.players[0].chips_in_front)), True, badugi.WHITE
        )
        pygame.draw.circle(
            badugi.WINDOW, "white", (badugi.p1x + 500, badugi.p1y + 230), 12
        )  # Here <<<
        badugi.WINDOW.blit(text, (badugi.p1x + 520, badugi.p1y + 215))

    # Player 2
    text = badugi.BIG_FONT.render(
        badugi.players[1].name,
        True,
        badugi.GREEN if badugi.dealer.turn == 1 else badugi.WHITE,
    )
    badugi.WINDOW.blit(text, (badugi.p2x, badugi.p2y))
    text = badugi.FONT.render(str(badugi.players[1].chips), True, badugi.WHITE)
    badugi.WINDOW.blit(text, (badugi.p2x, badugi.p2y + 40))
    badugi.WINDOW.blit(badugi.AVATAR2, (badugi.p2x, badugi.p2y + 70))
    for i, card in enumerate(badugi.players[1].hand):
        card.show(((badugi.p2x + 200) + (i * 100), badugi.p2y), show_back=not_showdown)
    if badugi.players[1].chips_in_front != 0:
        text = badugi.BIG_FONT.render(
            str(int(badugi.players[1].chips_in_front)), True, badugi.WHITE
        )
        pygame.draw.circle(
            badugi.WINDOW, "white", (badugi.p2x + 500, badugi.p2y - 50), 12
        )
        badugi.WINDOW.blit(text, (badugi.p2x + 520, badugi.p2y - 65))
    # Dealer button
    badugi.WINDOW.blit(
        badugi.DEALER_BUTTON,
        (badugi.p1x + 120, badugi.p1y + 150 if badugi.button == 0 else badugi.p2y - 40),
    )
