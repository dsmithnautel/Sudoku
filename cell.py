# Imports pygame
import pygame


class Cell:
    # initializes the attribues for the cell class
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = None
        self.row = row
        self.col = col
        self.screen = screen
        self.cell_rect = None

    # Sets the cell and sketched values
    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    # Defines the draw function that draws all the cells on the board
    def draw(self, sketched):
        color_font = (150, 150, 150) if sketched else (0, 0, 0)
        cell_difference = 3 if sketched else 1
        num_text = ""
        if self.value != 0:
            num_text = f"{self.value}"
        elif self.sketched_value and sketched:
            num_text = f"{self.sketched_value}"
        x = 0 + int(self.row * (450/9)) + (2 if self.row % 3 == 0 else 1)
        y = 0 + int(self.col * (450/9)) + (2 if self.col % 3 == 0 else 1)
        self.cell_rect = pygame.Rect(y, x, 450/9 - cell_difference, 450/9 - cell_difference)
        num_font = pygame.font.SysFont("verdana", 32)
        pygame.draw.rect(self.screen, "light blue", self.cell_rect, 2)
        self.screen.blit(
            num_font.render(num_text, True, color_font, None),
            (y + 13, x + 3)
        )

    # Outlines the selected cell with a red border so the user knows it is selected
    def draw_select(self):
        pygame.draw.rect(self.screen, "red", self.cell_rect, 2)
