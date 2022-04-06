import pygame


class Card:
    """
    Signel card
    """

    def __init__(self, window, suit, number, img_src):
        self.suit = suit
        self.number = number
        self.size = (100, 175)
        self.img = pygame.transform.scale(img_src, self.size)
        self.window = window
        self.selected = False
        self.surface = pygame.Surface(self.size)

    # def on_click(self):
    #     """Change the text whe you click"""
    #     # self.surface.fill(bg)
    #     # self.surface.blit(self.text, (0, 0))
    #     # self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, pos):
        self.window.blit(self.img, pos)
        self.rect = pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])
        # self.window.blit(self.surface, (self.x, self.y))

    def any_click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.selected = not self.selected
                    print("osu korttiin")
                    return True
        return False
