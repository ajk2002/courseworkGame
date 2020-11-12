import pygame

class Menu():
    def __init__(self,game):
        self.game = game
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.dhjj