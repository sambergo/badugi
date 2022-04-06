import pygame


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, window, text, pos, font, bg="black"):
        self.window = window
        self.x, self.y = pos
        self.font = font
        self.on_click(text, bg)

    def on_click(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, True, pygame.Color("White"))
        self.size = (100, 40)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        self.window.blit(self.surface, (self.x, self.y))

    def any_click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False
