from enum import IntFlag, auto


class WinType(IntFlag):
    TimeOut = auto()
    SpyShot = auto()
    SniperWin = TimeOut | SpyShot
    MissionsWin = auto()
    CivilianShot = auto()
    SpyWin = MissionsWin | CivilianShot


WINTYPES_TO_COLORS = {
    WinType.TimeOut: "xkcd:sea blue",
    WinType.SpyShot: "xkcd:green",
    WinType.MissionsWin: "xkcd:red orange",
    WinType.CivilianShot: "xkcd:pumpkin",
}


WINTYPE_PREFERRED_PIE_CHART_ORDER = [
    WinType.TimeOut,
    WinType.SpyShot,
    WinType.MissionsWin,
    WinType.CivilianShot,
]

WINTYPE_PREFERRED_PIE_CHART_COLOR = [
    WINTYPES_TO_COLORS[w_type] for w_type in WINTYPE_PREFERRED_PIE_CHART_ORDER
]
