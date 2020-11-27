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
    DoubleModern = auto()
    OldGallery = auto()
    Panopticon = auto()
    Modern = auto()
    CrowdedPub = auto()
    OldBalcony = auto()
    Courtyard1 = auto()
    Courtyard2 = auto()
    OldVeranda = auto()
    OldBallroom = auto()

    def stringify(self):
        if self == Venue.HighRise:
            return "High-Rise"

        if self == Venue.DoubleModern:
            return "Double Modern"

        if self == Venue.OldGallery:
            return "Old Gallery"

        if self == Venue.CrowdedPub:
            return "Crowded Pub"

        if self == Venue.OldBalcony:
            return "Old Balcony"

        if self == Venue.OldBallroom:
            return "Old Ballroom"

        if self == Venue.OldVeranda:
            return "Old Veranda"

        if self == Venue.Courtyard1:
            return "Old Courtyard"

        if self == Venue.Courtyard2:
            return "Old Courtyard 2"

        return self.name
