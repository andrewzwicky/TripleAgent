import os
from triple_agent.organization.replay_file_iterator import iterate_over_replays
import triple_agent

TEST_FOLDER = os.path.abspath(os.path.dirname(__file__))


def test_iterate_over_replays(monkeypatch):

    games = list(iterate_over_replays(lambda g: True))
    print(games)
