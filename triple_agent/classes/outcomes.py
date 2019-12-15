from enum import Flag, auto


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
