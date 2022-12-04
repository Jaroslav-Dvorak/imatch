from time import time


class Player:
    def __init__(self, card, color):
        self.card = card
        self.color = color
        self.score = 0
        self.multiplay_score = 0
        self.start_time = time()

    def play(self, adj_score):
        self.score += adj_score
        self.multiplay_score += adj_score
        if self.score < 0:
            self.score = 0
        if self.multiplay_score < 0:
            self.multiplay_score = 0

    def percentage(self):
        play_time = (time() - self.start_time) / 60
        card_per_minute = self.score / play_time
        percentage = card_per_minute / 60 * 100
        return percentage
