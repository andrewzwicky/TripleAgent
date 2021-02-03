import numpy as np
import os
from pathlib import Path
from triple_agent.classes.game import Game
from typing import Iterator, Tuple, List
import cv2

TEST_FOLDER = Path(__file__).resolve().parent


def mock_screenshot_iterator(
    games: List[Game],
) -> Iterator[Tuple[int, int, np.ndarray, bool]]:

    outputs = []

    for game_index, game in enumerate(games):
        ss_files = sorted(
            os.listdir(
                TEST_FOLDER.joinpath("test_parallel_replay_screenshots", game.uuid)
            ),
            # because we can now have double digit ss_indices, must parse as index, otherwise sort order is 1 10 2, etc.
            key=lambda x: int(x.replace(".png", "")),
        )

        for screenshot_index, f in enumerate(ss_files, start=1):
            outputs.append(
                (
                    game_index,
                    screenshot_index,
                    cv2.imread(
                        str(
                            TEST_FOLDER.joinpath(
                                "test_parallel_replay_screenshots",
                                game.uuid,
                                f,
                            ).resolve()
                        )
                    ),
                    screenshot_index == len(ss_files),
                )
            )

    for output in outputs:
        yield output
