from enum import Flag, auto


class WinType(Flag):
    TimeOut = auto()
    SpyShot = auto()
    SniperWin = TimeOut | SpyShot
    MissionsWin = auto()
    CivilianShot = auto()
    SpyWin = MissionsWin | CivilianShot


WINTYPES_TO_COLORS = {
    WinType.TimeOut: "xkcd:sea blue",
    WinType.SpyShot: "xkcd:green",
    WinType.MissionsWin: "xkcd:red",
    WinType.CivilianShot: "xkcd:pumpkin",
}

WINTYPE_PREFERRED_PIE_CHART_ORDER = [
    WinType.TimeOut,
    WinType.SpyShot,
    WinType.MissionsWin,
    WinType.CivilianShot,
]
