from enum import IntEnum, auto


class Books(IntEnum):
    NoColor = 0
    Red = auto()
    Yellow = auto()
    Green = auto()
    Blue = auto()


# Book colors are not consistent between venues in replays.
COLORS_TO_BOOKS_ENUM = {
    (27, 26, 185): Books.Red,
    (18, 18, 125): Books.Red,
    (60, 133, 60): Books.Green,
    (85, 153, 73): Books.Green,
    (135, 208, 140): Books.Green,
    (32, 107, 39): Books.Green,
    (149, 87, 56): Books.Blue,
    (166, 99, 90): Books.Blue,
    (185, 119, 83): Books.Blue,
    (190, 92, 66): Books.Blue,
    (165, 48, 22): Books.Blue,
    (35, 115, 151): Books.Yellow,
}

BOOKS_ENUM_TO_COLORS = {
    Books.Red: "xkcd:red",
    Books.Blue: "xkcd:blue",
    Books.Green: "xkcd:green",
    Books.Yellow: "xkcd:yellow",
}
