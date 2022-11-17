from random import randint
import math


def generate8points(size):
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
    points = []

    for i in reversed(range(slices)):
        i += 1

        # x = math.cos(math.radians(angle + tilted)) * radius + xs
        # y = math.sin(math.radians(angle + tilted)) * radius + ys

        deviation = ((randint(max_angle_deviation // -2, max_angle_deviation // 2)) / 100) + 1
        curr_angle = step / i * deviation
        step -= curr_angle
        angle += curr_angle

        if i > 1:
            last_angle = angle
        else:
            curr_angle = 360.0 - last_angle
            angle = 360.0

        fromcenter = randint(radius * 0.5, radius * 0.75)

        x = math.cos(math.radians(angle + tilted - curr_angle / 2)) * fromcenter + xs
        y = math.sin(math.radians(angle + tilted - curr_angle / 2)) * fromcenter + ys

        xpoints.append(x)
        ypoints.append(y)
        p_size = curr_angle
        points.append(((x, y), p_size))

    x, y = sum(xpoints) / slices, sum(ypoints) / slices
    p_size = size//3
    points.append(((x, y), p_size))

    return points
