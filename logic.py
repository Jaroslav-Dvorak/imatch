from layout import Layout
import pygame


class Logic(Layout):
    def __init__(self):
        Layout.__init__(self)

    def click(self, mouse_pos):
        click = self.pointing(mouse_pos)
        if not click:
            return None
        player, pict = click
        player_pictures = set(self.packages[player].pictures)
        winning_picture = player_pictures.intersection(set(self.packages[0].pictures))
        for win in winning_picture:
            winning_picture = win
        if self.packages[player].pictures[winning_picture] == pict:
            return player

    def pointing(self, mouse_pos):
        for player, pack in enumerate(self.packages):
            if player == 0:
                continue
            if pack.rect.collidepoint(mouse_pos):
                for pict, point in enumerate(pack.points):
                    x = mouse_pos[0]
                    y = mouse_pos[1]
                    lf = pack.rect.x + point[0][0] - point[1]
                    rg = pack.rect.x + point[0][0] + point[1]
                    up = pack.rect.y + point[0][1] - point[1]
                    dw = pack.rect.y + point[0][1] + point[1]
                    if lf < x < rg and up < y < dw:
                        return player, pict

    def cursor_change(self, mouse_pos):
        if self.pointing(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
