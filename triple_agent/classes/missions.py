from enum import Flag, auto

from typing import Set


class Missions(Flag):
    NoMission = 0
    Seduce = auto()
    Inspect = auto()
    Fingerprint = auto()
    Contact = auto()
    Bug = auto()
    Swap = auto()
    Purloin = auto()
    Transfer = auto()


MISSION_LETTERS_TO_ENUM = {
    "S": Missions.Seduce,
    "I": Missions.Inspect,
    "F": Missions.Fingerprint,
    "C": Missions.Contact,
    "B": Missions.Bug,
    "W": Missions.Swap,
    "P": Missions.Purloin,
    "T": Missions.Transfer,
}

MISSIONS_ENUM_TO_LETTER = {
    Missions.Seduce: "S",
    Missions.Inspect: "I",
    Missions.Fingerprint: "F",
    Missions.Contact: "C",
    Missions.Bug: "B",
    Missions.Swap: "W",
    Missions.Purloin: "P",
    Missions.Transfer: "T",
}

MISSIONS_ENUM_TO_COLOR = {
    Missions.Seduce: "xkcd:sea blue",
    Missions.Inspect: "xkcd:pumpkin",
    Missions.Fingerprint: "xkcd:purplish",
    Missions.Contact: "xkcd:golden yellow",
    Missions.Bug: "xkcd:grey",
    Missions.Swap: "xkcd:greenish blue",
    Missions.Purloin: "xkcd:deep pink",
    Missions.Transfer: "xkcd:green",
}

MISSION_PLOT_ORDER = list(MISSIONS_ENUM_TO_LETTER.keys())

MISSION_COMPLETE_TIMELINE_TO_ENUM = {
    "target seduced.": Missions.Seduce,
    "all statues inspected.": Missions.Inspect,
    "fingerprinted ambassador.": Missions.Fingerprint,
    "double agent contacted.": Missions.Contact,
    "bugged ambassador while walking.": Missions.Bug,
    "bugged ambassador while standing.": Missions.Bug,
    "statue swapped.": Missions.Swap,
    "guest list purloined.": Missions.Purloin,
    "transferred microfilm.": Missions.Transfer,
}

MISSION_GENERIC_TIMELINE_TO_ENUM = {
    "seduce target": Missions.Seduce,
    "inspect statues": Missions.Inspect,
    "inspect 1 statue": Missions.Inspect,
    "inspect 2 statues": Missions.Inspect,
    "inspect 3 statues": Missions.Inspect,
    "fingerprint ambassador": Missions.Fingerprint,
    "contact double agent": Missions.Contact,
    "banana bread": Missions.Contact,
    "bug ambassador": Missions.Bug,
    "swap statue": Missions.Swap,
    "statue swap": Missions.Swap,
    "purloin guest list": Missions.Purloin,
    "guest list purloin": Missions.Purloin,
    "guest list return": Missions.Purloin,
    "transfer microfilm": Missions.Transfer,
    "check watch": Missions.NoMission,
}

MISSION_PARTIAL_TO_ENUM = {
    "fingerprinted statue.": Missions.Fingerprint,
    "fingerprinted drink.": Missions.Fingerprint,
    "fingerprinted book.": Missions.Fingerprint,
    "fingerprinted briefcase.": Missions.Fingerprint,
    "hide microfilm in book.": Missions.Transfer,
    "remove microfilm from book.": Missions.Transfer,
    "left statue inspected.": Missions.Inspect,
    "held statue inspected.": Missions.Inspect,
    "right statue inspected.": Missions.Inspect,
}


def convert_mission_set_to_enum(missions_set: Set[str]) -> Missions:
    missions_enum = Missions.NoMission

    for mission_string in filter(lambda x: x != "None", missions_set):
        missions_enum |= Missions[mission_string]

    return missions_enum
