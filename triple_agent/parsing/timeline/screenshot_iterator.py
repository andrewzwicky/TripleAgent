import ctypes
from time import sleep
from typing import Optional, Iterator, Tuple, List

import cv2
import numpy as np
import pyautogui
from mss import mss

from triple_agent.classes.game import Game

from triple_agent.parsing.timeline.parse_timeline import (
    SPY_P_TOP,
    SPY_P_LEFT,
    SPY_P_WIDTH,
    SPY_P_HEIGHT,
    SPY_MISSIONS_COLOR,
    TIME_STEP,
    TIMEOUT,
    TIMELINE_TOP,
    OVERALL_CAPTURE_BORDER,
    TIMELINE_LEFT,
    TIMELINE_WIDTH,
    TIMELINE_HEIGHT,
    ARROW_ROW,
    ARROW_HEIGHT,
    ARROW_COL,
    ARROW_WIDTH,
    ARROW_COLOR,
)


def get_app_handles() -> Tuple[Optional[int], Optional[int]]:
    pycharm_handle = None
    spyparty_handle = None

    enum_windows_process = ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
    )

    def foreach_window(hwnd, _):
        nonlocal pycharm_handle
        nonlocal spyparty_handle
        title = window__get_title(hwnd)
        # TODO: err handling here, not very robust way to detect SP window
        if "PyCharm" in title:
            pycharm_handle = hwnd
        if "SpyParty v0.1.6729.0" in title:
            spyparty_handle = hwnd

        return True

    ctypes.windll.user32.EnumWindows(enum_windows_process(foreach_window), 0)

    if spyparty_handle is None or pycharm_handle is None:
        raise OSError

    return spyparty_handle, pycharm_handle


def window__get_title(hwnd_handle):
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd_handle)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd_handle, buff, length + 1)
        return buff.value
    return ""


def is_game_loaded(spy_party_handle: Optional[int], pycharm_handle: Optional[int]):
    total_time = 0

    while True:
        refresh_window(spy_party_handle, pycharm_handle)

        with mss() as sct:
            p_button = cv2.cvtColor(
                np.asarray(
                    sct.grab(
                        monitor={
                            "top": SPY_P_TOP,
                            "left": SPY_P_LEFT,
                            "width": SPY_P_WIDTH,
                            "height": SPY_P_HEIGHT,
                        }
                    )
                ),
                cv2.COLOR_BGRA2BGR,
            )

        # if the game isn't loaded, there will be a blue P,
        # use those colors to detect whether the game is loaded
        r_mask = p_button[..., 0] == SPY_MISSIONS_COLOR[0]
        g_mask = p_button[..., 1] == SPY_MISSIONS_COLOR[1]
        b_mask = p_button[..., 2] == SPY_MISSIONS_COLOR[2]

        if not (np.all(r_mask) and np.all(g_mask) and np.all(b_mask)):
            return True

        sleep(TIME_STEP)
        total_time += TIME_STEP
        if total_time > TIMEOUT:
            return False


def refresh_window(spy_party_handle, pycharm_handle):
    ctypes.windll.user32.SetForegroundWindow(pycharm_handle)
    sleep(0.2)
    ctypes.windll.user32.SetForegroundWindow(spy_party_handle)
    sleep(0.2)


def get_mss_screenshots(
    games: List[Game]
) -> Iterator[Tuple[int, int, np.ndarray, bool]]:
    # this is the pyautogui version
    spyparty_handle, pycharm_handle = get_app_handles()

    for game_index, game in enumerate(games):
        print(
            f"{game.spy} vs. {game.sniper} on {game.venue} [{game.uuid}, {game_index + 1}/{len(games)}]"
        )
        screenshot_index = 1

        while True:
            refresh_window(spyparty_handle, pycharm_handle)

            with mss() as sct:
                screenshot = cv2.cvtColor(
                    np.asarray(
                        sct.grab(
                            monitor={
                                "top": TIMELINE_TOP - OVERALL_CAPTURE_BORDER,
                                "left": TIMELINE_LEFT - OVERALL_CAPTURE_BORDER,
                                "width": TIMELINE_WIDTH + (2 * OVERALL_CAPTURE_BORDER),
                                "height": TIMELINE_HEIGHT
                                + (2 * OVERALL_CAPTURE_BORDER),
                            }
                        )
                    ),
                    cv2.COLOR_BGRA2BGR,
                )

            # need a way to communicate through the queue that
            # all screenshots for this file have been processed,
            # starts with identifying the last one.
            print(f"{game_index} {screenshot_index} taken")

            if is_last_screenshot(screenshot):
                yield (game_index, screenshot_index, screenshot, True)

                if game_index != (len(games) - 1):
                    go_to_next_game(pycharm_handle, spyparty_handle)

                break

            else:
                yield (game_index, screenshot_index, screenshot, False)
                scroll_lines()

            screenshot_index += 1


def scroll_lines():
    for _ in range(30):
        pyautogui.scroll(-1)
        sleep(0.02)


def go_to_next_game(pycharm_handle, spyparty_handle):
    pyautogui.hotkey("ctrl", "n")
    sleep(0.250)
    if is_game_loaded(spyparty_handle, pycharm_handle):
        sleep(0.250)
        pyautogui.press("f11")
    # Starting in "SpyParty v0.1.6729.0", the timeline does not open to the start,
    # but it opens to the start of game instead, which means that a scroll up in needed
    # to capture everything.
    for _ in range(30):
        pyautogui.scroll(1)
        sleep(0.02)
    sleep(0.5)


def is_last_screenshot(screenshot: np.ndarray):
    arrow_location = screenshot[
        ARROW_ROW : ARROW_ROW + ARROW_HEIGHT, ARROW_COL : ARROW_COL + ARROW_WIDTH
    ]

    # arrow is still present, indicating more in the timeline
    if np.all(arrow_location == ARROW_COLOR[0]):
        return False

    return True
