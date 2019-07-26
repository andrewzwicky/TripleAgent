from triple_agent.utilities.outcomes import WinType


def sort_by_spy_wins(data_dictionary):
    return sum([x for c, x in data_dictionary.items() if c & WinType.SpyWin])


def sort_by_sniper_wins(data_dictionary):
    return sum([x for c, x in data_dictionary.items() if c & WinType.SniperWin])
