from enum import Flag, auto
from typing import Set
from triple_agent.constants.colors import PlotColorsBase
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


def create_missions_color_dict(plot_colors: PlotColorsBase):
    return {
        Missions.Seduce: plot_colors.color_1,
        Missions.Inspect: plot_colors.color_1_light,
        Missions.Fingerprint: plot_colors.color_5,
        Missions.Contact: plot_colors.color_2,
        Missions.Bug: plot_colors.grey,
        Missions.Swap: plot_colors.color_2_light,
        Missions.Purloin: plot_colors.color_3,
        Missions.Transfer: plot_colors.color_4,
        Missions.NoMission: plot_colors.light_grey,
    }


def create_bug_color_dict(plot_colors: PlotColorsBase):
    return {
        ("Walking", True): plot_colors.color_1,
        ("Walking", False): plot_colors.color_1,
        ("Standing", True): plot_colors.color_2,
        ("Standing", False): plot_colors.color_2,
    }


_FAKE = "fake"
_REAL = "real"


def create_banana_bread_color_dict(plot_colors: PlotColorsBase):
    return {_FAKE: plot_colors.color_2, _REAL: plot_colors.color_1}


_DIRECT = "direct"
_AT = "action test"


def create_microfilm_color_dict(plot_colors: PlotColorsBase):
    return {_DIRECT: plot_colors.color_1, _AT: plot_colors.color_2}


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
