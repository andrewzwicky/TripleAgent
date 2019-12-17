from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.outcomes import WinType

# These methods were used to query a set of replays for curated replay sets
# They aren't used throughout TripleAgent otherwise.


def curated_many_green_ats(game):
    if game.venue != "Balcony" and game.win_type in [
        WinType.TimeOut,
        WinType.MissionsWin,
    ]:
        if game.timeline is not None:
            this_game_green_tests = 0
            for event in game.timeline:
                if event.action_test == ActionTest.Green:
                    this_game_green_tests += 1

            if this_game_green_tests >= 7:
                return True

    return False


def cough_clank_crash(game):
    if game.venue != "Balcony" and game.win_type in [
        WinType.TimeOut,
        WinType.MissionsWin,
    ]:
        if game.game_type.startswith("a4") or game.game_type.startswith("a5"):
            if game.timeline is not None:
                for event in game.timeline:
                    if (
                        event.event
                        in [
                            # clank
                            "dropped statue.",
                            # cough
                            "banana bread aborted.",
                            "action test red: contact double agent",
                            # crash
                            "purloin guest list aborted.",
                        ]
                        and (game.duration - event.elapsed_time) > 10
                    ):
                        return True

    return False
