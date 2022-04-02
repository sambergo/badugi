from game import Badugi

players = ["Player1", "Player2"]
max_hands = 3
badugi = Badugi(players, 20000, max_hands)

run = True
while run:
    run = badugi.main_loop()

for player in badugi.players:
    print(player.name)
    print(player.chips)
