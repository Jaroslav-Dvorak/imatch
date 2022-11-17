import pygame
from parameters import BG_COLOR, CARD_COLOR, CARD_SIZE, SCR_WIDTH, SCR_HEIGHT
from random import randint
from helpers import generate8points


class Card(pygame.sprite.Sprite):
    def __init__(self, pos, pictures):
        super().__init__()
        self.image = pygame.Surface((CARD_SIZE, CARD_SIZE))
        self.image.fill(BG_COLOR)
        self.image.set_colorkey(BG_COLOR)
        self.rect = self.image.get_rect()
        self.pictures = {}

        self.move(pos)

        # if pos == 0:
        #     self.rect.x = SCR_WIDTH//2 - CARD_SIZE//2
        #     self.rect.y = 0 + SCR_HEIGHT*border_coef
        # elif pos == 1:
        #     self.rect.x = 0 + SCR_WIDTH*border_coef
        #     self.rect.y = SCR_HEIGHT - CARD_SIZE - SCR_HEIGHT*border_coef
        # elif pos == 2:
        #     self.rect.x = SCR_WIDTH - CARD_SIZE - SCR_WIDTH*border_coef
        #     self.rect.y = SCR_HEIGHT - CARD_SIZE - SCR_HEIGHT*border_coef

        pygame.draw.circle(self.image, CARD_COLOR, (CARD_SIZE//2, CARD_SIZE//2), CARD_SIZE//2)

        self.points = generate8points(CARD_SIZE//2)

        # pygame.draw.line(self.image, (0, 0, 0), (xs, ys), (x, y))
        #
        # pygame.draw.line(self.image, (255, 0, 0), (xs, ys), (x, y))

        for index, picture in enumerate(pictures):
            self.pictures[picture] = index
            new_size_w = self.points[index][1]*2*0.90
            ratio = new_size_w / picture.get_rect().w
            new_size_h = picture.get_rect().h * ratio
            picture = pygame.transform.scale(picture, (new_size_w, new_size_h))
            picture = pygame.transform.rotate(picture, randint(0, 359))

            self.image.blit(picture, picture.get_rect(center=self.points[index][0]))
            # pygame.draw.rect(self.image, "red", picture.get_rect(center=points[index][0]), width=3)

        # for point in self.points:
        #     coord = point[0]
        #     radius = point[1]

            # self.crcls = pygame.draw.circle(self.image, (0, 255, 0), coord, radius, width=1)

        # pygame.draw.circle(surface, (0, 255, 0), centroid, CARD_SIZE // 6, width=3)

        self.card = pygame.sprite.Group()
        self.card.add(self)

    def move(self, pos):
        border_coef = 0.01

        if pos == 0:
            self.rect.x = SCR_WIDTH//2 - CARD_SIZE//2
            self.rect.y = 0 + SCR_HEIGHT*border_coef
        elif pos == 1:
            self.rect.x = 0 + SCR_WIDTH*border_coef
            self.rect.y = SCR_HEIGHT - CARD_SIZE - SCR_HEIGHT*border_coef
        elif pos == 2:
            self.rect.x = SCR_WIDTH - CARD_SIZE - SCR_WIDTH*border_coef
            self.rect.y = SCR_HEIGHT - CARD_SIZE - SCR_HEIGHT*border_coef
