import ctypes
import itertools
import os
import threading
from collections import defaultdict
from queue import Queue
from shutil import move
from time import sleep
from typing import List
from typing import Tuple, Optional

import pyautogui

from triple_agent.parsing.timeline.parse_timeline import TimelineParseException
from triple_agent.parsing.timeline.parse_timeline import (
    parse_single_screenshot,
    get_screenshots,
    remove_overlap,
    is_game_loaded,
)
from triple_agent.classes.game import Game, get_game_expected_pkl
from triple_agent.constants.paths import LONG_FILE_HEADER, PICKLE_ISOLATION, PARSE_LOG
from triple_agent.classes.timeline import Timeline


def get_app_handles() -> Tuple[Optional[int], Optional[int]]:
    _pycharm_handle = None
    _spy_party_handle = None

    enum_windows_process = ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
    )

    def foreach_window(hwnd, _):
        nonlocal _pycharm_handle
        nonlocal _spy_party_handle
        title = window__get_title(hwnd)
        # TODO: err handling here, not very robust way to detect SP window
        if "PyCharm" in title:
            _pycharm_handle = hwnd
        if "SpyParty v0.1.6729.0" in title:
            _spy_party_handle = hwnd

        return True

    ctypes.windll.user32.EnumWindows(enum_windows_process(foreach_window), 0)

    if _spy_party_handle is None or _pycharm_handle is None:
        raise OSError

    return _spy_party_handle, _pycharm_handle


def window__get_title(hwnd_handle):
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd_handle)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd_handle, buff, length + 1)
        return buff.value
    return ""


def parse_timeline_parallel(games: List[Game]):

    if not games:
        return

    spy_party_handle, pycharm_handle = get_app_handles()

    mutex = threading.Lock()
    num_worker_threads = 2
    queue = Queue()
    threads = []

    timeline_pieces = defaultdict(dict)

    def screenshot_consumer():
        while True:
            _game_index, (_number, _screenshot, _last) = queue.get()

            if _game_index is None:
                break

            try:
                # noinspection PyTypeChecker
                timeline_pieces[_game_index][
                    (_number, _last)
                ] = parse_single_screenshot(_screenshot)
            except TimelineParseException:
                # all pieces won't make it into dict, so it'll never get pickled.
                queue.task_done()
                continue

            num_parsed_pieces = 0
            last_num = 0
            last_seen = False

            for (_n, _l) in timeline_pieces[_game_index].keys():
                num_parsed_pieces += 1
                if _l:
                    last_seen = True
                    last_num = _n

            # all the pieces are present, finish the parse and pickle the game
            if last_seen and num_parsed_pieces == last_num:
                ordered_line_items = sorted(
                    timeline_pieces[_game_index].items(), key=lambda x: x[0]
                )
                this_events = [v for k, v in ordered_line_items]
                flattened_lines = itertools.chain.from_iterable(this_events)
                events = remove_overlap(flattened_lines)
                timeline = Timeline(events)
                timeline.calculate_elapsed_times()

                mutex.acquire()
                try:
                    games[_game_index].timeline = timeline
                    coh_bool, coh_reasons = games[_game_index].is_timeline_coherent()
                    games[_game_index].repickle()
                    if not coh_bool:
                        print(games[_game_index], coh_reasons)
                        with open(PARSE_LOG, "a+") as parse_log:
                            parse_log.write(
                                f"incoherent timeline {games[_game_index].spy} vs. {games[_game_index].sniper} on {games[_game_index].venue} {games[_game_index].uuid} : {coh_reasons}\n"
                            )

                        pkl_loc = get_game_expected_pkl(games[_game_index].uuid)
                        pkl_name = os.path.split(pkl_loc)[1]
                        move(
                            LONG_FILE_HEADER + pkl_loc,
                            LONG_FILE_HEADER + os.path.join(PICKLE_ISOLATION, pkl_name),
                        )

                finally:
                    mutex.release()

            queue.task_done()

    for _ in range(num_worker_threads):
        thread = threading.Thread(target=screenshot_consumer)
        thread.start()
        threads.append(thread)

    for game_index, game in enumerate(games):
        if game_index == 0:
            input("Hit Enter when ready, parsing begins 10 seconds later")
            sleep(10)
        print(
            f"{game.spy} vs. {game.sniper} on {game.venue} [{game.uuid}, {game_index + 1}/{len(games)}]"
        )
        for (number, screenshot, last) in get_screenshots(
            spy_party_handle, pycharm_handle
        ):
            queue.put((game_index, (number, screenshot, last)))

            if last and game_index != (len(games) - 1):
                pyautogui.hotkey("ctrl", "n")
                sleep(0.250)

                if is_game_loaded(spy_party_handle, pycharm_handle):
                    sleep(0.250)
                    pyautogui.press("f11")

                # Starting in "SpyParty v0.1.6729.0", the timeline does not open to the start,
                # but it opens to the start of game instead, which means that a scroll up in needed
                # to capture everything.
                for _ in range(30):
                    pyautogui.scroll(1)
                    sleep(0.02)

                sleep(0.5)

    queue.join()

    for _ in range(num_worker_threads):
        queue.put((None, (None, None, None)))

    for thread in threads:
        thread.join()
