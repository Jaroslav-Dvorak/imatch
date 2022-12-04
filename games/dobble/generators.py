from random import sample, choice, randint
import math

PICTS_PER_CARD = 8


def generate_points(size=50):
    slices = 7
    x = size
    y = size
    radius = size
    xs = x
    ys = y
    angle = 0
    step = 360
    max_angle_deviation = 40
    tilted = randint(0, 360 // slices)
    last_angle = 0

    xpoints = []
    ypoints = []
    points = {"x": [], "y": [], "h": [], "r": []}

    for i in reversed(range(slices)):
        i += 1

        deviation = ((randint(max_angle_deviation // -2, max_angle_deviation // 2)) / 100) + 1
        curr_angle = step / i * deviation
        step -= curr_angle
        angle += curr_angle

        if i > 1:
            last_angle = angle
        else:
            curr_angle = 360.0 - last_angle
            angle = 360.0

        fromcenter = randint(int(radius * 0.5), int(radius * 0.75))

        x = math.cos(math.radians(angle + tilted - curr_angle / 2)) * fromcenter + xs
        y = math.sin(math.radians(angle + tilted - curr_angle / 2)) * fromcenter + ys

        xpoints.append(x)
        ypoints.append(y)
        h = curr_angle / 2.2

        points["x"].append(x)
        points["y"].append(y)
        points["h"].append(h)
        points["r"].append(randint(0, 359))

    x, y = sum(xpoints) / slices, sum(ypoints) / slices
    h = size / 2.2

    points["x"].append(x)
    points["y"].append(y)
    points["h"].append(h)
    points["r"].append(randint(0, 359))

    return points


def generate_pictures(other_cards_pictures, all_pictures):
    if not other_cards_pictures:
        return set(sample(all_pictures, PICTS_PER_CARD))
    rest_of_images = set(all_pictures) - set.union(*other_cards_pictures)
    common_images = []
    for index_observed, card_observed in enumerate(other_cards_pictures):
        common_images.append(set())
        for card_compared in other_cards_pictures:
            if card_observed is card_compared:
                continue
            if index_observed == 0:
                break
            common_images[index_observed].update(card_observed & card_compared)

    new_card = set()
    idx = 0
    for card, common_image in zip(other_cards_pictures, common_images):
        if card:
            choosen = {choice(list(card - common_image))}
            if card & new_card:
                continue
            new_card.update(choosen)
        idx += 1

    rest_to_fill = (PICTS_PER_CARD - len(new_card))
    to_fill = set(sample(rest_of_images, rest_to_fill))
    new_card.update(to_fill)

    return new_card
