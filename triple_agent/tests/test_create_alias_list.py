from datetime import datetime

from triple_agent.classes.game import Game
from triple_agent.reports.generation.create_alias_list import create_alias_list
from triple_agent.classes.venues import Venue
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.missions import Missions


def test_create_alias_list():
    mock_games = list()

    mock_games.append(
        Game(
            "spy1",
            "sniper1",
            "spy1_user",
            "sniper1_user",
            Venue.Balcony,
            WinType.SpyShot,
            "a3/4",
            Missions.Inspect,
            Missions.Inspect,
            Missions.Inspect,
            datetime(2021, 7, 16),
            "nothing_uuid",
            10,
            "no_file",
        )
    )
    mock_games.append(
        Game(
            "spy1_early",
            "sniper1_early",
            "spy1_user",
            "sniper1_user",
            Venue.Balcony,
            WinType.SpyShot,
            "a3/4",
            Missions.Inspect,
            Missions.Inspect,
            Missions.Inspect,
            datetime(2021, 7, 15),
            "nothing_uuid",
            10,
            "no_file",
        )
    )
    mock_games.append(
        Game(
            "spy2",
            "sniper2",
            "spy2_user",
            "sniper2_user",
            Venue.Balcony,
            WinType.SpyShot,
            "a3/4",
            Missions.Inspect,
            Missions.Inspect,
            Missions.Inspect,
            datetime(2021, 7, 14),
            "nothing_uuid",
            10,
            "no_file",
        )
    )
    mock_games.append(
        Game(
            "spy1",
            "sniper1ababa",
            "spy1_user",
            "sniper1_user",
            Venue.Balcony,
            WinType.SpyShot,
            "a3/4",
            Missions.Inspect,
            Missions.Inspect,
            Missions.Inspect,
            datetime(2021, 7, 20),
            "nothing_uuid",
            10,
            "no_file",
        )
    )
    mock_games.append(
        Game(
            "spy111",
            "sniper45",
            "spy1_user",
            "sniper3_user",
            Venue.Balcony,
            WinType.SpyShot,
            "a3/4",
            Missions.Inspect,
            Missions.Inspect,
            Missions.Inspect,
            datetime(2021, 7, 25),
            "nothing_uuid",
            10,
            "no_file",
        )
    )
    mock_games.append(
        Game(
            "spy2222",
            "sniper2",
            "spy2_user",
            "sniper2_user",
            Venue.Balcony,
            WinType.SpyShot,
            "a3/4",
            Missions.Inspect,
            Missions.Inspect,
            Missions.Inspect,
            datetime(2021, 7, 29),
            "nothing_uuid",
            10,
            "no_file",
        )
    )

    assert create_alias_list(mock_games) == {
        "spy1_user": "spy111",
        "sniper1_user": "sniper1ababa",
        "spy2_user": "spy2222",
        "sniper2_user": "sniper2",
        "sniper3_user": "sniper45",
    }
