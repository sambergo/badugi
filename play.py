import pygame

from game import Badugi

players = ["Player1", "Player2"]
width, height = 1400, 800
max_hands = 10
window = pygame.display.set_mode((width, height))
badugi = Badugi(window, width, height, players, 20000, max_hands)
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    run = badugi.main_loop()
    badugi.draw()
    pygame.display.update()

for player in badugi.players:
    print(player.name)
    print(player.chips)
print("LOPPU")
pygame.quit()
