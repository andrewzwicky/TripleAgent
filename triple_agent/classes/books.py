from enum import Enum, auto


class Books(Enum):
    Red = auto()
    Yellow = auto()
    Green = auto()
    Blue = auto()

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


# Book colors are not consistent between venues in replays.
# Colors are BGR
COLORS_TO_BOOKS_ENUM = {
    (27, 26, 185): Books.Red,
    (18, 18, 125): Books.Red,
    (42, 48, 194): Books.Red,
    (0, 0, 255): Books.Red,
    (11, 0, 255): Books.Red,
    (60, 133, 60): Books.Green,
    (85, 153, 73): Books.Green,
    (135, 208, 140): Books.Green,
    (32, 107, 39): Books.Green,
    (17, 127, 10): Books.Green,
    (149, 87, 56): Books.Blue,
    (255, 0, 0): Books.Blue,
    (166, 99, 90): Books.Blue,
    (185, 119, 83): Books.Blue,
    (190, 92, 66): Books.Blue,
    (165, 48, 22): Books.Blue,
    (35, 115, 151): Books.Yellow,
    (0, 255, 255): Books.Yellow,
}
