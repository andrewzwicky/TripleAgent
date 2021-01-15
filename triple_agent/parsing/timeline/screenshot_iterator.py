import os
import ctypes
import logging
from time import sleep
from typing import Optional, Iterator, Tuple, List

import cv2
import numpy as np
import pyautogui
from mss import mss
from triple_agent.classes.game import Game
from triple_agent.classes.capture_debug_pictures import capture_debug_picture
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
from triple_agent.constants.paths import DEBUG_CAPTURES

logger = logging.getLogger("triple_agent")


def get_app_handles() -> Tuple[Optional[int], Optional[int]]:
    other_handle = None
    spyparty_handle = None

    enum_windows_process = ctypes.WINFUNCTYPE(
        ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
    )

    def foreach_window(hwnd, _):
        nonlocal other_handle
        nonlocal spyparty_handle
        title = window__get_title(hwnd)
        # TODO: err handling here, not very robust way to detect SP window
        if title.startswith("Windows PowerShell"):
            other_handle = hwnd
        if title == "SpyParty v0.1.7269.0":
            spyparty_handle = hwnd

        return True

    ctypes.windll.user32.EnumWindows(enum_windows_process(foreach_window), 0)

    if spyparty_handle is None or other_handle is None:
        raise OSError

    return spyparty_handle, other_handle


def window__get_title(hwnd_handle):
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd_handle)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd_handle, buff, length + 1)
        return buff.value
    return ""


def is_game_loaded(
    spy_party_handle: Optional[int],
    other_handle: Optional[int],
):
    total_time = 0

    while True:
        p_button = get_latest_loading_screenshot(spy_party_handle, other_handle)

        # if the game isn't loaded, there will be a blue P,
        # use those colors to detect whether the game is loaded
        r_mask = p_button[..., 0] == SPY_MISSIONS_COLOR[0]
        g_mask = p_button[..., 1] == SPY_MISSIONS_COLOR[1]
        b_mask = p_button[..., 2] == SPY_MISSIONS_COLOR[2]

        if not (np.all(r_mask) and np.all(g_mask) and np.all(b_mask)):
            logger.debug("is_game_loaded returns True")
            return True

        sleep(TIME_STEP)
        total_time += TIME_STEP

        if total_time > TIMEOUT:
            logger.error("is_game_loaded returns False")
            capture_debug_picture(
                os.path.join(DEBUG_CAPTURES, "game_not_loaded"), p_button
            )
            return False

        logger.debug(f"game loading [{total_time} sec.]")


def get_latest_loading_screenshot(
    spy_party_handle: Optional[int], other_handle: Optional[int]
):
    logger.debug("get_latest_loading_screenshot called")
    refresh_window(spy_party_handle, other_handle)
    sleep(0.25)

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

    return p_button


def refresh_window(spy_party_handle, other_handle):
    logger.debug("refresh_window called")
    ctypes.windll.user32.SetForegroundWindow(other_handle)
    sleep(0.5)
    logger.debug(ctypes.windll.user32.GetForegroundWindow())
    ctypes.windll.user32.SetForegroundWindow(spy_party_handle)
    sleep(0.5)
    logger.debug(ctypes.windll.user32.GetForegroundWindow())


def get_mss_screenshots(
    games: List[Game],
) -> Iterator[Tuple[int, int, np.ndarray, bool]]:
    # this is the pyautogui version
    spyparty_handle, other_handle = get_app_handles()

    logger.debug(spyparty_handle)
    logger.debug(other_handle)

    for game_index, game in enumerate(games):
        logger.info(
            f"[{game.uuid}, {game_index + 1}/{len(games)}]: {game.venue}, {game.spy} vs. {game.sniper}"
        )
        screenshot_index = 1

        while True:
            refresh_window(spyparty_handle, other_handle)
            sleep(0.2)

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

            yield (game_index, screenshot_index, screenshot, False)
            screenshot_index += 1

            pyautogui.keyDown("shiftleft")
            sleep(0.2)

            refresh_window(spyparty_handle, other_handle)

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

            pyautogui.keyUp("shiftleft")

            if is_last_screenshot(screenshot):
                yield (game_index, screenshot_index, screenshot, True)

                if game_index != (len(games) - 1):
                    go_to_next_game(spyparty_handle, other_handle)

                break

            yield (game_index, screenshot_index, screenshot, False)
            scroll_lines()

            screenshot_index += 1


def scroll_lines():
    for _ in range(30):
        pyautogui.scroll(-1)
        sleep(0.01)


def go_to_next_game(spyparty_handle, other_handle) -> bool:
    logger.debug("going to next game")
    pyautogui.hotkey("ctrl", "n")
    sleep(0.2)
    if is_game_loaded(spyparty_handle, other_handle):
        sleep(0.2)
        refresh_window(spyparty_handle, other_handle)
        sleep(0.4)
        pyautogui.press("f11")
        sleep(0.2)
        # Starting in "SpyParty v0.1.6729.0", the timeline does not open to the start,
        # but it opens to the start of game instead, which means that a scroll up in needed
        # to capture everything.
        for _ in range(30):
            pyautogui.scroll(1)
            sleep(0.01)
        sleep(0.25)
        return True

    return False


def is_last_screenshot(screenshot: np.ndarray):
    arrow_location = screenshot[
        ARROW_ROW : ARROW_ROW + ARROW_HEIGHT, ARROW_COL : ARROW_COL + ARROW_WIDTH
    ]

    # arrow is still present, indicating more in the timeline
    if np.all(arrow_location == ARROW_COLOR[0]):
        logger.debug("is_last_screenshot returns False")
        return False

    logger.debug("is_last_screenshot returns True")
    return True
