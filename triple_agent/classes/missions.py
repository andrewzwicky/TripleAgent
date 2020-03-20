from enum import Flag, auto
from typing import Set
from triple_agent.constants.colors import PLOT_COLORS
from triple_agent.classes.ordered_enum import ReverseOrderedEnum


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


class MissionStatus(ReverseOrderedEnum):
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
    Missions.Seduce: PLOT_COLORS.color_1,
    Missions.Inspect: PLOT_COLORS.color_1_light,
    Missions.Fingerprint: PLOT_COLORS.color_5,
    Missions.Contact: PLOT_COLORS.color_2,
    Missions.Bug: PLOT_COLORS.grey,
    Missions.Swap: PLOT_COLORS.color_2_light,
    Missions.Purloin: PLOT_COLORS.color_3,
    Missions.Transfer: PLOT_COLORS.color_4,
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
