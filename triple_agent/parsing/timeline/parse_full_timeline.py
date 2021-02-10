import itertools
import logging
import time
from typing import List, Callable
from pathlib import Path

from triple_agent.constants.paths import (
    REPLAY_PICKLE_FOLDER,
    JSON_GAMES_FOLDER,
    DEBUG_CAPTURES,
)
from triple_agent.classes.capture_debug_pictures import capture_debug_picture
from triple_agent.classes.timeline import TimelineCoherency
from triple_agent.parsing.timeline.parse_timeline import (
    TimelineParseException,
    TimelineOddNumberScreenshots,
    TimelineMismatchedElapsedScreenshots,
    parse_screenshot,
    remove_overlap,
)
from triple_agent.classes.game import Game
from triple_agent.classes.timeline import Timeline, TimelineEvent

logger = logging.getLogger("triple_agent")


def merge_elapsed_screenshots(
    events: List[List[TimelineEvent]],
) -> List[List[TimelineEvent]]:
    if len(events) % 2 != 0:
        # If there is an odd number, no way for them to be matched up
        logger.warning("TimelineParseException odd number of screenshots supplied")
        raise TimelineOddNumberScreenshots("Odd number of screenshots supplied")

    possible_remaining = events[::2]
    possible_elapsed = events[1::2]

    for rem, elapse in zip(possible_remaining, possible_elapsed):
        for _r, _e in zip(rem, elapse):
            if (
                _r.event != _e.event
                or _r.actor != _e.actor
                or _r.cast_name != _e.cast_name
                and _r.elapsed_time is None
                and _e.time is None
            ):
                logger.warning(
                    "TimelineParseException mismatch between remaining and elapsed screenshots"
                )
                raise TimelineMismatchedElapsedScreenshots(
                    "Mismatch between remaining and elapsed screenshots"
                )

    # everything matches, proceed with merging
    for rem, elapse in zip(possible_remaining, possible_elapsed):
        for _r, _e in zip(rem, elapse):
            _r.elapsed_time = _e.elapsed_time

    return possible_remaining


def parse_full_timeline(
    games: List[Game],
    screenshot_iterator: Callable,
    pickle_folder: Path,
    json_folder: Path,
):
    this_game_events = []

    input("Hit Enter when ready, parsing begins 10 seconds later\n")
    time.sleep(10)

    for game_index, ss_index, screenshot, is_last in screenshot_iterator(games):
        try:
            this_game_events.append(parse_screenshot(screenshot))
            if is_last:
                if len(this_game_events) == ss_index:
                    this_game_events = merge_elapsed_screenshots(this_game_events)
                    flattened_lines = itertools.chain.from_iterable(this_game_events)
                    events = remove_overlap(flattened_lines)
                    timeline = Timeline(events)
                    games[game_index].timeline = timeline
                    coherency = games[game_index].is_timeline_coherent()
                    games[game_index].add_start_clock_seconds()

                    if coherency != TimelineCoherency.Coherent:
                        logger.error(
                            f"INCOHERENT TIMELINE: {games[game_index].uuid} {str(coherency)}\n"
                        )
                    else:
                        games[game_index].pickle(pickle_folder)
                        games[game_index].serialize_to_json(json_folder)

                this_game_events = []
        except TimelineParseException:
            capture_debug_picture(
                DEBUG_CAPTURES.joinpath("overall_failures"),
                screenshot,
                filename=f"{games[game_index].uuid}_{ss_index}.png",
            )
            this_game_events = []

    return games
