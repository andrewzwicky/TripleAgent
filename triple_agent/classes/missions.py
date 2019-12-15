from enum import Flag, auto
from typing import Set, List
import jsonpickle.handlers


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

    def serialize(self):
        return [mission.name for mission in Missions if mission & self]


class MissionStatus(Flag):
    Disabled = 0
    Incomplete = auto()
    Complete = auto()


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

MISSION_STATUS_PLOT_ORDER = [
    MissionStatus.Disabled,
    MissionStatus.Incomplete,
    MissionStatus.Complete,
]


def convert_mission_set_to_enum(missions_set: Set[str]) -> Missions:
    missions_enum = Missions.NoMission

    for mission_string in filter(lambda x: x != "None", missions_set):
        missions_enum |= Missions[mission_string]

    return missions_enum

