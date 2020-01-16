from enum import auto
from triple_agent.classes.ordered_enum import OrderedStringifyEnum


class Venue(OrderedStringifyEnum):
    Aquarium = auto()
    Balcony = auto()
    Ballroom = auto()
    Courtyard = auto()
    Gallery = auto()
    HighRise = auto()
    Library = auto()
    Moderne = auto()
    Pub = auto()
    Redwoods = auto()
    Teien = auto()
    Terrace = auto()
    Veranda = auto()

    def stringify(self):
        if self == Venue.HighRise:
            return "High-Rise"

        return self.name
