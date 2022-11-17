import pygame

from logic import Logic

if __name__ == '__main__':
    pygame.init()
    fps = pygame.time.Clock()
    logic = Logic()
    quit_game = False
    while not quit_game:
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                winner = logic.click(event.pos)
                if winner:
                    logic.action(winner)
            if event.type == pygame.MOUSEMOTION:
                logic.cursor_change(event.pos)

        logic.layout_update()
        pygame.display.update()
