from os import listdir, path
import random
import pygame
from parameters import PICT_PER_CARD


class Pictures:
    def __init__(self, theme):
        self.pics_path = path.join("themes", theme)
        self.pics_files = listdir(self.pics_path)
        self.pictures = set()
        self.pict_packages = [set() for _ in range(3)]
        self.load_pics()
        self.unhide()

    def load_pics(self):
        pictures = []
        for index, pic_file in enumerate(self.pics_files):
            pic_path = path.join(self.pics_path, pic_file)
            try:
                loaded_picture = pygame.image.load(pic_path).convert_alpha()
            except pygame.error:
                continue
            else:
                pictures.append(loaded_picture)

        self.pictures = set(pictures)

        package = [p for p in self.pictures]
        random.shuffle(package)
        self.pict_packages[0] = set(package[:PICT_PER_CARD])

    def unhide(self):
        what_left = self.pictures - self.pict_packages[0]
        for index, player in enumerate(self.pict_packages):
            if index > 0 and not player:
                common_picts = set()
                number_of_common = 0
                for cmmn in range(index):
                    common_picts = common_picts | {random.choice(list(self.pict_packages[cmmn]))}
                    number_of_common = cmmn
                self.pict_packages[index] = common_picts | set(list(what_left)[:PICT_PER_CARD - number_of_common - 1])

            what_left = what_left - self.pict_packages[index]
