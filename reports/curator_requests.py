from triple_agent.organization.extract_spectation_replays import (
    extract_spectate_replays,
)
from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.outcomes import WinType

def curated_many_green_ats(r):
    if r.venue != 'Balcony' and r.win_type in [WinType.TimeOut, WinType.MissionsWin]:
        if r.timeline is not None:
            this_game_green_tests = 0
            for e in r.timeline:
                if e.action_test == ActionTest.Green:
                    this_game_green_tests += 1

            if this_game_green_tests >= 7:
                return True

    return False

def cough_clank_crash(r):
    if r.venue != 'Balcony' and r.win_type in [WinType.TimeOut, WinType.MissionsWin]:
        if r.game_type.startswith('a4') or r.game_type.startswith('a5'):
            if r.timeline is not None:
                for e in r.timeline:
                    if e.event in [
                        # clank
                        "dropped statue.",
                        # cough
                        "banana bread aborted.", "action test red: contact double agent",
                        # crash
                        "purloin guest list aborted."
                    ] and (r.duration - e.elapsed_time) > 10:
                        return True

    return False

if __name__ == "__main__":
    extract_spectate_replays(cough_clank_crash)
