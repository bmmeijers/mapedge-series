from itertools import chain

black_pixels__intervals = [
    (196, 203),  # thick black
    (208, 209),  # thin black
    (263, 265),  # thin black at map border
    (315, 316),
    (334, 337),
    (342, 343),
    (362, 369),
    (380, 382),
    (387, 395),
    (399, 404),
    (417, 418),
    (419, 420),
]
white_pixels__intervals = [
    (0, 97),
    (111, 122),
    (136, 196),
    (203, 208),  # white between thick black, thin black
    (210, 263),  # white next to thin black
    (271, 272),
    (274, 276),
]


def left(interval):
    return interval[0]


def center(interval):
    return size(interval) / 2 + interval[0]


def right(interval):
    return interval[1]


def size(interval):
    return interval[1] - interval[0]


for interval in sorted(chain(black_pixels__intervals, white_pixels__intervals)):
    print(
        interval,
        f"Δ{size(interval)}",
        left(interval),
        right(interval),
        center(interval),
    )
