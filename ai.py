import pygame

from game import Badugi

players = ["Player1", "Player2", "Player3"]
width, height = 1400, 800
max_hands = 3
window = pygame.display.set_mode((width, height))
badugi = Badugi(window, width, height, players, 20000, max_hands)
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    badugi.main_loop()
    badugi.draw()
    pygame.display.update()

for player in badugi.players:
    print(player.name)
    print(player.chips)
pygame.quit()
