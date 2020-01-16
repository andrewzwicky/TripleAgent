from enum import Flag, auto
from typing import Set
from triple_agent.constants.colors import PlotColors


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
    Missions.Seduce: PlotColors.Color1,
    Missions.Inspect: PlotColors.Color1Light,
    Missions.Fingerprint: PlotColors.Color5,
    Missions.Contact: PlotColors.Color2,
    Missions.Bug: PlotColors.Grey,
    Missions.Swap: PlotColors.Color2Light,
    Missions.Purloin: PlotColors.Color3,
    Missions.Transfer: PlotColors.Color4,
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
