from triple_agent.classes.outcomes import WinType


def sort_by_spy_wins(name_series):
    _, series = name_series
    return series.filter(items=[WinType.MissionsWin, WinType.CivilianShot]).sum()


def sort_by_sniper_wins(name_series):
    _, series = name_series
    return series.filter(items=[WinType.SpyShot, WinType.TimeOut]).sum()
