import itertools
import os
import threading
from collections import defaultdict
from queue import Queue
from shutil import move
from time import sleep
from typing import List
from typing import Callable
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER

from triple_agent.classes.timeline import TimelineCoherency
from triple_agent.parsing.timeline.parse_timeline import (
    TimelineParseException,
    parse_screenshot,
    remove_overlap,
)

from triple_agent.classes.game import Game, get_game_expected_pkl
from triple_agent.constants.paths import LONG_FILE_HEADER, PICKLE_ISOLATION, PARSE_LOG
from triple_agent.classes.timeline import Timeline


def parse_timeline_parallel(
    games: List[Game],
    screenshot_iterator: Callable,
    pickle_folder: str = REPLAY_PICKLE_FOLDER,
):

    mutex = threading.Lock()
    num_worker_threads = 2
    queue = Queue()
    threads = []

    timeline_pieces = defaultdict(dict)

    def screenshot_consumer():
        while True:
            game_index, ss_index, screenshot, is_last = queue.get()

            # None is the signal that all screenshots have been processed
            if game_index is None:
                break

            try:
                # noinspection PyTypeChecker
                timeline_pieces[game_index][(ss_index, is_last)] = parse_screenshot(
                    screenshot
                )
            except TimelineParseException:
                # all pieces won't make it into dict, so it'll never get pickled.
                queue.task_done()
                continue

            # all the pieces are present, finish the parse and pickle the game
            if all_timeline_pieces_present(timeline_pieces[game_index]):
                ordered_line_items = sorted(
                    timeline_pieces[game_index].items(), key=lambda x: x[0]
                )
                this_events = [v for k, v in ordered_line_items]
                flattened_lines = itertools.chain.from_iterable(this_events)
                events = remove_overlap(flattened_lines)
                timeline = Timeline(events)
                timeline.calculate_elapsed_times()

                mutex.acquire()
                try:
                    games[game_index].timeline = timeline
                    coherency = games[game_index].is_timeline_coherent()
                    games[game_index].repickle(pickle_folder=pickle_folder)
                    if coherency != TimelineCoherency.Coherent:
                        print(games[game_index], str(coherency))
                        with open(PARSE_LOG, "a+") as parse_log:
                            parse_log.write(
                                f"incoherent timeline {games[game_index].spy} vs. {games[game_index].sniper} on {games[game_index].venue} {games[game_index].uuid} : {coh_reasons}\n"
                            )

                        # TODO: find a way to get this to allow for passing the pickle folder argument.
                        pkl_loc = get_game_expected_pkl(games[game_index].uuid)
                        pkl_name = os.path.split(pkl_loc)[1]
                        move(
                            LONG_FILE_HEADER + pkl_loc,
                            LONG_FILE_HEADER + os.path.join(PICKLE_ISOLATION, pkl_name),
                        )

                finally:
                    mutex.release()

            queue.task_done()

    def all_timeline_pieces_present(pieces_dict: dict) -> bool:
        num_parsed_pieces = 0
        last_num = 0
        last_seen = False

        for (_n, _l) in pieces_dict.keys():
            num_parsed_pieces += 1
            if _l:
                last_seen = True
                last_num = _n

        return last_seen and num_parsed_pieces == last_num

    for _ in range(num_worker_threads):
        thread = threading.Thread(target=screenshot_consumer)
        thread.start()
        threads.append(thread)

    input("Hit Enter when ready, parsing begins 10 seconds later")
    sleep(10)

    for screenshot_information in screenshot_iterator(games):
        queue.put(screenshot_information)

    queue.join()

    for _ in range(num_worker_threads):
        queue.put((None, None, None, None))

    for thread in threads:
        thread.join()

    return games
