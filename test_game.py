from game.game import Badugi


def test_game():
    max_hands = 4
    badugi = Badugi(["Player 1", "Pelaaja 2"], 1000, max_hands)
    badugi.test_game()


if __name__ == "__main__":
    test_game()
