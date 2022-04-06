import pygame

from game.game import Badugi


def test_game():
    players = ["Player1", "AI"]
    max_hands = 1
    pygame.display.set_caption("Badugi")
    width, height = 1400, 800
    window = pygame.display.set_mode((width, height))
    badugi = Badugi(players, 1000, max_hands, window, width, height)
    badugi.test_game()
    pygame.quit()


if __name__ == "__main__":
    test_game()
