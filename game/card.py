import os

import pygame


class Card:
    """
    Clickable card with pygame blit function.
    """

    card_back_src = pygame.image.load(os.path.join("PNG", "gray_back.png"))
    swap_img_src = pygame.image.load(os.path.join("PNG", "swap.png"))

    def __init__(self, window, suit, number, img_src):
        self.suit = suit
        self.number = number
        self.size = (100, 175)
        self.img = pygame.transform.scale(img_src, self.size)
        self.img_back = pygame.transform.scale(self.card_back_src, self.size)
        self.img_swap = pygame.transform.scale(self.swap_img_src, (25, 25))
        self.rect = self.img.get_rect()
        self.window = window
        self.selected = False
        self.surface = pygame.Surface(self.size)

    def show(self, pos, show_back=False):
        self.pos = pos
        self.window.blit(self.img_back if show_back else self.img, pos)
        self.rect = pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])
        if self.selected:
            self.window.blit(self.img_swap, pos)

    def any_click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.selected = not self.selected
                    self.show(self.pos, show_back=False)
                    pygame.display.update()
                    return True
        return False
