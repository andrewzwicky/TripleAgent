
SCL5_VENUE_MODES = {
    "Ballroom": "a4/8",
    "Library": "a5/8",
    "Moderne": "a5/8",
    "Balcony": "a2/3",
    "Terrace": "a3/5",
    "Pub": "a3/5",
    "High-Rise": "a3/5",
    "Courtyard": "a4/7",
    "Gallery": "a4/8",
    "Veranda": "a5/8",
    "Teien": "a4/8",
    "Aquarium": "a4/8",
}

SCL5_MISSION_PICK_MAPS = {"Pub", "High-Rise", "Terrace", "Balcony"}
SCL5_MISSION_NO_PICK_MAPS = set(SCL5_VENUE_MODES.keys()) - SCL5_MISSION_PICK_MAPS

SCL5_PICK_MODES = {
    venue: mode
    for venue, mode in SCL5_VENUE_MODES.items()
    if venue in SCL5_MISSION_PICK_MAPS
}

SCL5_DROPPED_PLAYERS = {
    "baldrick",
    "brskaylor",
    "rta",
    "Hectic",
    "bitbandingpig",
    "frostie",
    "belial",
    "tristram",
    "the_usual_toaster",
    "ThatOdinaryPlayer",
    "PixelBandit",
    "gasol",
    "kevino",
    "tge",
    "Tortuga-Man",
    "Vlady",
    "sergioc89",
    "mintyrug",
    "ml726",
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


def select_scl5(game):
    return (
        game.event == 'SCL5' and
        game.division != 'Challenger' and
        game.spy not in SCL5_DROPPED_PLAYERS and
        game.sniper not in SCL5_DROPPED_PLAYERS
    )