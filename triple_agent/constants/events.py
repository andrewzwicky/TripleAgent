from triple_agent.classes.game import Game
from triple_agent.classes.venues import Venue

SCL5_VENUE_MODES = {
    Venue.Ballroom: "a4/8",
    Venue.Library: "a5/8",
    Venue.Moderne: "a5/8",
    Venue.Balcony: "a2/3",
    Venue.Terrace: "a3/5",
    Venue.Pub: "a3/5",
    Venue.HighRise: "a3/5",
    Venue.Courtyard: "a4/7",
    Venue.Gallery: "a4/8",
    Venue.Veranda: "a5/8",
    Venue.Teien: "a4/8",
    Venue.Aquarium: "a4/8",
}

SCL6_VENUE_MODES = {
    Venue.Aquarium: "a4/8",
    Venue.Balcony: "a2/3",
    Venue.Ballroom: "a4/8",
    Venue.Courtyard: "a4/7",
    Venue.Gallery: "a4/8",
    Venue.HighRise: "a3/5",
    Venue.Library: "a5/8",
    Venue.Moderne: "a4/8",
    Venue.Pub: "a3/6",
    Venue.Redwoods: "a4/8",
    Venue.Teien: "a4/8",
    Venue.Terrace: "a3/6",
    Venue.Veranda: "a5/8",
}


SCL5_MISSION_PICK_MAPS = {Venue.Pub, Venue.HighRise, Venue.Terrace, Venue.Balcony}

SCL5_PICK_MODES = {
    venue: mode
    for venue, mode in SCL5_VENUE_MODES.items()
    if venue in SCL5_MISSION_PICK_MAPS
}

SCL5_DROPPED_PLAYERS = {
    # Silver
    "ml726",
    "mintyrug",
    "baldrick",
    # Bronze
    "brskaylor",
    "Hectic/steam",
    "bitbandingpig",
    # Copper
    "frostie",
    "belial",
    "tristram",
    # Iron
    "rta",
    "the_usual_toaster/steam",
    # Obsidian
    "juliusb",
    "sergioc89",
    "Vlady/steam",
    "PixelBandit/steam",
    "gasol",
    "kevino",
    # Oak
    "umbertofinito",
    "Libro/steam",
    "ThatOdinaryPlayer/steam",
    "tge",
    "Tortuga-Man/steam",
    # Challenger
    "Rai/steam",
    "linkvanyali",
}

SCL6_DROPPED_PLAYERS = {
    "Max Edward Snax/steam",
}

SCL5_DIVISIONS = [
    "Diamond",
    "Platinum",
    "Gold",
    "Silver",
    "Bronze",
    "Copper",
    "Iron",
    "Obsidian",
    "Oak",
    "Challenger",
]

SCL6_DIVISIONS = [
    # TODO: clear this up after placements
    "Diamond",
    "Platinum",
    "Gold",
    "Silver",
    "Bronze",
    "Copper",
    "Iron",
    "Obsidian",
    "Oak",
    "Challenger",
]


def select_scl5(game: Game) -> bool:  # pragma: no cover
    return (
        game.event == "SCL5"
        and game.spy not in SCL5_DROPPED_PLAYERS
        and game.sniper not in SCL5_DROPPED_PLAYERS
    )


def select_scl5_regular_season(game: Game) -> bool:  # pragma: no cover
    return (
        game.event == "SCL5"
        and game.division in SCL5_DIVISIONS
        and game.spy not in SCL5_DROPPED_PLAYERS
        and game.sniper not in SCL5_DROPPED_PLAYERS
    )


def select_scl5_with_drops(game: Game) -> bool:  # pragma: no cover
    return game.event == "SCL5"


def select_scl6(game: Game) -> bool:  # pragma: no cover
    return (
        game.event == "SCL6"
        and game.spy not in SCL6_DROPPED_PLAYERS
        and game.sniper not in SCL6_DROPPED_PLAYERS
    )


def select_scl6_regular_season(game: Game) -> bool:  # pragma: no cover
    return (
        game.event == "SCL6"
        and game.division in SCL6_DIVISIONS
        and game.spy not in SCL6_DROPPED_PLAYERS
        and game.sniper not in SCL6_DROPPED_PLAYERS
    )


def select_scl6_with_drops(game: Game) -> bool:  # pragma: no cover
    return game.event == "SCL6"


def select_sc19(game: Game) -> bool:  # pragma: no cover
    return game.event == "Summer Cup 2019"
