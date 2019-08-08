import numpy as np
from triple_agent.classes.game import Game
from typing import List, Iterator, Tuple
import cv2
import os
from triple_agent.parsing.timeline.parse_game_timelines_parallel import (
    parse_timeline_parallel,
)
from triple_agent.classes.characters import Characters

from triple_agent.classes.timeline import TimelineEvent

TEST_FOLDER = os.path.abspath(os.path.dirname(__file__))


def mock_screenshot_iterator(
    games: List[Game]
) -> Iterator[Tuple[int, int, np.ndarray, bool]]:
    for game_index, game in enumerate(games):
        ss_files = sorted(
            os.listdir(
                os.path.join(TEST_FOLDER, "test_parallel_replay_screenshots", game.uuid)
            )
        )

        for screenshot_index, f in enumerate(ss_files, start=1):
            yield (
                game_index,
                screenshot_index,
                cv2.imread(
                    os.path.join(
                        TEST_FOLDER, "test_parallel_replay_screenshots", game.uuid, f
                    )
                ),
                screenshot_index == len(ss_files),
            )


def test_parse_timeline_parallel(get_test_games, monkeypatch):
    games = get_test_games
    for g in games:
        g.timeline = None

    monkeypatch.setattr("builtins.input", lambda x: None)

    parse_timeline_parallel(games, mock_screenshot_iterator)

    games.sort(key=lambda g: g.start_time)

    assert games[0].uuid == "OiG7qvC9QOaSKVGlesdpWQ"
    assert games[0].timeline[0].actor == "spy"
    assert games[0].timeline[0].event == "spy cast."
    assert games[0].timeline[0].time == 3 * 60 + 45
    assert games[0].timeline[0].cast_name == (Characters.Irish,)
