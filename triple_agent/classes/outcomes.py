from enum import Flag, auto
from triple_agent.constants.colors import PlotColorsBase


class WinType(Flag):
    TimeOut = auto()
    SpyShot = auto()
    SniperWin = TimeOut | SpyShot
    MissionsWin = auto()
    CivilianShot = auto()
    SpyWin = MissionsWin | CivilianShot

    def serialize(self):
        return [win_type.name for win_type in WinType if win_type & self]


def create_wintypes_color_dict(plot_colors: PlotColorsBase):
    return {
        WinType.TimeOut: plot_colors.color_1_light,
        WinType.SpyShot: plot_colors.color_1,
        WinType.MissionsWin: plot_colors.color_2,
        WinType.CivilianShot: plot_colors.color_2_light,
    }


WINTYPE_PREFERRED_PIE_CHART_ORDER = [
    WinType.TimeOut,
    WinType.SpyShot,
    WinType.MissionsWin,
    WinType.CivilianShot,
]
