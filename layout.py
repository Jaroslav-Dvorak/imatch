import pygame
from parameters import SCR_WIDTH, SCR_HEIGHT, BG_COLOR
from card import Card
from pictures import Pictures

resolution = (SCR_WIDTH, SCR_HEIGHT)


class Layout(Pictures):
    def __init__(self, theme="computer", players=2):
        self.canvas = pygame.display.set_mode(resolution)
        pygame.display.set_caption("Dobble")
        Pictures.__init__(self, theme)

        self.packages = []
        for idx_package in range(players+1):
            self.packages.append(Card(pos=idx_package, pictures=self.pict_packages[idx_package]))

    def action(self, winner):
        self.packages[winner].move(0)
        self.pict_packages[0] = self.pict_packages[winner]
        self.pict_packages[winner] = None
        self.packages[0] = self.packages[winner]
        self.unhide()
        self.packages[winner] = Card(pos=winner, pictures=self.pict_packages[winner])

    def layout_update(self):
        self.canvas.fill(BG_COLOR)
        for package in self.packages:
            package.card.draw(self.canvas)
