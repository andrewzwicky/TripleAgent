from enum import Flag, auto
from triple_agent.constants.colors import PLOT_COLORS


class WinType(Flag):
    TimeOut = auto()
    SpyShot = auto()
    SniperWin = TimeOut | SpyShot
    MissionsWin = auto()
    CivilianShot = auto()
    SpyWin = MissionsWin | CivilianShot

    def serialize(self):
        return [win_type.name for win_type in WinType if win_type & self]


WINTYPES_TO_COLORS = {
    WinType.TimeOut: PLOT_COLORS.color_1_light,
    WinType.SpyShot: PLOT_COLORS.color_1,
    WinType.MissionsWin: PLOT_COLORS.color_2,
    WinType.CivilianShot: PLOT_COLORS.color_2_light,
}

WINTYPE_PREFERRED_PIE_CHART_ORDER = [
    WinType.TimeOut,
    WinType.SpyShot,
    WinType.MissionsWin,
    WinType.CivilianShot,
]
