import itertools
import logging
from time import sleep
from typing import List
from typing import Callable

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER, JSON_GAMES_FOLDER
from triple_agent.classes.timeline import TimelineCoherency
from triple_agent.parsing.timeline.parse_timeline import (
    TimelineParseException,
    parse_screenshot,
    remove_overlap,
)
from triple_agent.classes.game import Game
from triple_agent.classes.timeline import Timeline

logger = logging.getLogger("triple_agent")


def parse_timeline_parallel(
    games: List[Game],
    screenshot_iterator: Callable,
    pickle_folder: str = REPLAY_PICKLE_FOLDER,
    json_folder: str = JSON_GAMES_FOLDER,
):
    this_game_events = []

    input("Hit Enter when ready, parsing begins 10 seconds later\n")
    sleep(10)

    for game_index, ss_index, screenshot, is_last in screenshot_iterator(games):
        try:
            this_game_events.append(parse_screenshot(screenshot))
            if is_last:
                if len(this_game_events) == ss_index:
                    flattened_lines = itertools.chain.from_iterable(this_game_events)
                    events = remove_overlap(flattened_lines)
                    timeline = Timeline(events)
                    timeline.calculate_elapsed_times()
                    games[game_index].timeline = timeline
                    coherency = games[game_index].is_timeline_coherent()

                    if coherency != TimelineCoherency.Coherent:
                        logger.error(
                            f"INCOHERENT TIMELINE: {games[game_index].uuid} {str(coherency)}\n"
                        )
                    else:
                        games[game_index].repickle(pickle_folder=pickle_folder)
                        games[game_index].serialize_to_json(json_folder=json_folder)

                this_game_events = []
        except TimelineParseException:
            this_game_events = []

    return games
