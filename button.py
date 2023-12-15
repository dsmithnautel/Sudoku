import pygame


class Button(pygame.Rect):  # makes a generic class for every button with changeable width, height, and text attributes
    def __init__(self, x, y, width, height, text):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.button_font = pygame.font.SysFont("verdana", 16)

    def draw(self, screen):
        pygame.draw.rect(screen, (230, 110, 0), self)
        pygame.draw.rect(screen, (179, 98, 0), self, width=4)
        pygame.draw.rect(screen, (255, 140, 0), (self.x + 4, self.y + 3, self.width - 8, self.height - 6))
        pygame.draw.rect(screen, (255, 255, 255), (self.x + 5, self.y + 4, self.width - 9, self.height - 7), width=4)
        screen.blit(self.button_font.render(self.text, True, (255, 255, 255)),
                    # equation of a rational function to determine text spacing on the button relative to the button's edges
                    dest=(self.x + 9 + int(5000 * 1/(len(self.text) ** 4)), self.y + 6))
