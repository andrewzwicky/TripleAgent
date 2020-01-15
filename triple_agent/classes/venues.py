from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum


class Venue(ReverseOrderedEnum):
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

    def is_tray_purloin(self):
        return self in (
            Venue.Balcony,
            Venue.Ballroom,
            Venue.Courtyard,
            Venue.Gallery,
            Venue.HighRise,
            Venue.Library,
            Venue.Teien,
            Venue.Veranda,
        )

    def stringify(self):
        if self == Venue.HighRise:
            return "High-Rise"

        return self.name


def get_venue_setup(game):
    return (game.venue, game.guest_count, game.start_clock_seconds, game.game_type)
