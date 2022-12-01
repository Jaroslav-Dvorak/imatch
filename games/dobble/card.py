from .generators import generate_pictures, generate_points


class Card:
    def __init__(self, set_of_picts, other_cards=()):
        other_cards_pictures = [picts.picts_on_cards for picts in other_cards]
        self.picts_on_cards = generate_pictures(other_cards_pictures=other_cards_pictures,
                                                all_pictures=set_of_picts)
        points = generate_points()
        self.arragement = {}
        for idx, pict in enumerate(self.picts_on_cards):
            coords = {}
            for k, v in points.items():
                coords[k] = v[idx]
            self.arragement[pict] = coords

    # def populate(self):
    #     rest_of_images = set(self.picts)
    #     for making_card, making_restricted in zip(self.cards, self.restricted):
    #         for idx, (looked_card, looked_restricted) in enumerate(zip(self.cards, self.restricted)):
    #             if not looked_card or (making_card is looked_card):
    #                 continue
    #             choosen = {choice(list(looked_card - looked_restricted))}
    #
    #             making_restricted.update(choosen)
    #             if idx:
    #                 looked_restricted.update(choosen)
    #
    #             if looked_card & making_card:
    #                 continue
    #
    #             making_card.update(choosen)
    #
    #         rest_to_fill = (PICTS_PER_CARD - len(making_card))
    #         to_fill = set(sample(rest_of_images, rest_to_fill))
    #         making_card.update(to_fill)
    #
    #         rest_of_images = rest_of_images - making_card
