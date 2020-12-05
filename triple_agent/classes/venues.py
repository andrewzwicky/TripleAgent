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
        stringify_map = {
            Venue.HighRise: "High-Rise",
            Venue.DoubleModern: "Double Modern",
            Venue.OldGallery: "Old Gallery",
            Venue.CrowdedPub: "Crowded Pub",
            Venue.OldBalcony: "Old Balcony",
            Venue.OldBallroom: "Old Ballroom",
            Venue.OldVeranda: "Old Veranda",
            Venue.Courtyard1: "Old Courtyard",
            Venue.Courtyard2: "Old Courtyard 2",
        }

        try:
            return stringify_map[self]
        except KeyError:
            return self.name
