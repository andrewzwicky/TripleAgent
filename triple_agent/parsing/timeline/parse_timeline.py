import logging
import hashlib
from typing import List, Tuple, Optional, Iterator, Any

import cv2
import numpy as np
from triple_agent.classes.books import Books, COLORS_TO_BOOKS_ENUM
from triple_agent.classes.characters import Characters, PORTRAIT_MD5_DICT
from triple_agent.classes.roles import ROLE_COLORS_TO_ENUM, Roles
from triple_agent.classes.timeline import (
    TimelineEvent,
    EVENT_IMAGE_HASH_DICT,
    ACTOR_IMAGE_HASH_DICT,
    DIGIT_DICT,
)
from triple_agent.classes.capture_debug_pictures import capture_debug_picture
from triple_agent.constants.paths import DEBUG_CAPTURES

logger = logging.getLogger("triple_agent")

LINE_SPACING = 20
LINE_HEIGHT = 19

TIMELINE_TOP = 388
TIMELINE_LEFT = 42

TIMELINE_HEIGHT = 596
TIMELINE_WIDTH = 700

OVERALL_CAPTURE_BORDER = 10
LINE_BORDER = 4
BACKGROUND_COLOR = (38, 38, 38)
HIGHLIGHTED_BACKGROUND = (255, 255, 255)
SPY_MISSIONS_COLOR = (255, 204, 0)

ARROW_COLOR = (178, 178, 178)
NUM_LINES = 30

ARROW_ROW = 613
ARROW_COL = 160
ARROW_WIDTH = 18
ARROW_HEIGHT = 2

PORTRAIT_SPACING = 22
SINGLE_PORTRAIT_WIDTH = 22  # 22 accounts for background removed single portraits
PORTRAIT_BACKGROUND_BORDER = 2

SINGLE_BOOK_WIDTH = 17
BOOK_SPACING = 18

TIMER_OFFSET = 54
TEXT_OFFSET = 125

ROLE_BORDER_SIZE = 2

SPY_P_TOP = 668
SPY_P_LEFT = 633
SPY_P_WIDTH = 2
SPY_P_HEIGHT = 25
TIMEOUT = 12  # seconds
TIME_STEP = 1


class TimelineParseException(Exception):
    pass


class TimelineDigitNotMatchedException(TimelineParseException):
    pass


class TimelinePortraitNotMatchedException(TimelineParseException):
    pass


class TimelineActorNotMatchedException(TimelineParseException):
    pass


class TimelineEventNotMatchedException(TimelineParseException):
    pass


class TimelineOddNumberScreenshots(TimelineParseException):
    pass


class TimelineMismatchedElapsedScreenshots(TimelineParseException):
    pass


def separate_line_images(screenshot: np.ndarray) -> List[np.ndarray]:
    line_images = []

    for line_no in range(NUM_LINES):
        top_of_line = OVERALL_CAPTURE_BORDER + (line_no * LINE_SPACING)

        crop_img = screenshot[
            top_of_line : top_of_line + LINE_HEIGHT,
            OVERALL_CAPTURE_BORDER : OVERALL_CAPTURE_BORDER + TIMELINE_WIDTH,
        ]

        line_images.append(crop_img)

    return line_images


def remove_books(line_image: np.ndarray) -> Tuple[Tuple[Optional[Books]], np.ndarray]:
    first_row = line_image[0]

    no_book = np.all(np.all(first_row == BACKGROUND_COLOR, axis=1))
    if no_book:
        # no book found
        books = (None,)
    else:
        book_mask = np.any(first_row != BACKGROUND_COLOR, axis=1)
        first_book_index = np.argmax(book_mask)
        last_book_index = len(book_mask) - np.argmax(book_mask[::-1])

        if (last_book_index - first_book_index) > SINGLE_BOOK_WIDTH:
            book_colors = [
                tuple(
                    line_image[
                        0, ((last_book_index - BOOK_SPACING) + first_book_index) // 2
                    ]
                ),
                tuple(
                    line_image[
                        0, (last_book_index + (first_book_index + BOOK_SPACING)) // 2
                    ]
                ),
            ]
        else:
            book_colors = [
                tuple(line_image[0, (last_book_index + first_book_index) // 2])
            ]

        books = tuple(COLORS_TO_BOOKS_ENUM[color] for color in book_colors)

        line_image[:, first_book_index:last_book_index] = BACKGROUND_COLOR

    return books, line_image


def separate_portraits(
    line_image: np.ndarray,
) -> Tuple[
    np.ndarray,
    Tuple[Optional[np.ndarray]],
    Tuple[Optional[Roles]],
    Tuple[Optional[Books]],
]:
    last_row = line_image[-1]

    no_portrait = np.all(np.all(last_row == BACKGROUND_COLOR, axis=1))

    if no_portrait:
        # no portrait found
        portraits = (None,)
        roles = (None,)
    else:
        portrait_mask = np.any(last_row != BACKGROUND_COLOR, axis=1)
        first_portrait_index = np.argmax(portrait_mask)
        last_portrait_index = len(portrait_mask) - np.argmax(portrait_mask[::-1])

        if (last_portrait_index - first_portrait_index) > SINGLE_PORTRAIT_WIDTH:
            #  multiple portraits
            portraits = (
                np.copy(
                    line_image[
                        :-ROLE_BORDER_SIZE,
                        first_portrait_index
                        + PORTRAIT_BACKGROUND_BORDER : last_portrait_index
                        - PORTRAIT_SPACING
                        - PORTRAIT_BACKGROUND_BORDER,
                    ]
                ),
                np.copy(
                    line_image[
                        :-ROLE_BORDER_SIZE,
                        first_portrait_index
                        + PORTRAIT_SPACING
                        + PORTRAIT_BACKGROUND_BORDER : last_portrait_index
                        - PORTRAIT_BACKGROUND_BORDER,
                    ]
                ),
            )
        else:
            portraits = (
                np.copy(
                    line_image[
                        :-ROLE_BORDER_SIZE,
                        first_portrait_index
                        + PORTRAIT_BACKGROUND_BORDER : last_portrait_index
                        - PORTRAIT_BACKGROUND_BORDER,
                    ]
                ),
            )

        if (last_portrait_index - first_portrait_index) > SINGLE_PORTRAIT_WIDTH:
            role_colors = (
                tuple(
                    line_image[
                        -1,
                        (
                            (last_portrait_index - PORTRAIT_SPACING)
                            + first_portrait_index
                        )
                        // 2,
                    ]
                ),
                tuple(
                    line_image[
                        -1,
                        (
                            last_portrait_index
                            + (first_portrait_index + PORTRAIT_SPACING)
                        )
                        // 2,
                    ]
                ),
            )
        else:
            role_colors = (
                tuple(
                    line_image[-1, (last_portrait_index + first_portrait_index) // 2]
                ),
            )

        roles = tuple(
            ROLE_COLORS_TO_ENUM.get(color, Roles.Civilian) for color in role_colors
        )

        line_image[:, first_portrait_index:last_portrait_index] = BACKGROUND_COLOR

    books, line_image = remove_books(line_image)

    return line_image, portraits, roles, books


def add_borders(line_image: np.ndarray) -> np.ndarray:
    bordered = cv2.copyMakeBorder(
        line_image,
        LINE_BORDER,
        LINE_BORDER,
        LINE_BORDER,
        LINE_BORDER,
        cv2.BORDER_CONSTANT,
        value=BACKGROUND_COLOR,
    )

    return bordered


def convert_black_white(line_image: np.ndarray) -> np.ndarray:
    decolored = cv2.threshold(line_image, 40, 255, cv2.THRESH_BINARY)[1]
    decolored = cv2.bitwise_not(decolored)

    return decolored


def remove_highlighted_background(line_image: np.ndarray) -> np.ndarray:
    if np.array_equal(line_image[0, 0], HIGHLIGHTED_BACKGROUND):
        blue, green, red = line_image.T
        idx = ((red == 255) & (green == 255) & (blue == 255)).T
        line_image[idx] = BACKGROUND_COLOR[0]

        gradient_mask = np.any(line_image[-1] != BACKGROUND_COLOR, axis=1)
        gradient_column_index = len(gradient_mask) - np.argmax(gradient_mask[::-1])
        line_image[:, gradient_column_index - 1] = BACKGROUND_COLOR[0]

    return line_image


def split_into_parts(
    line_image: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    actor = np.copy(line_image[:, :TIMER_OFFSET])
    time = np.copy(line_image[:, TIMER_OFFSET:TEXT_OFFSET])
    text = np.copy(line_image[:, TEXT_OFFSET:])

    return actor, time, text


def name_portrait(
    portraits: Tuple[Optional[np.ndarray]],
) -> Tuple[Optional[Characters]]:
    characters = []
    for portrait in portraits:
        if portrait is None:
            return (None,)

        portrait_md5 = hashlib.md5(portrait.tobytes()).hexdigest()

        try:
            characters.append(PORTRAIT_MD5_DICT[portrait_md5])
        except KeyError as key_exec:
            logger.warning("TimelineParseException character portrait not found")
            capture_debug_picture(DEBUG_CAPTURES.joinpath("portraits"), portrait)
            raise TimelinePortraitNotMatchedException(
                "character portrait not found"
            ) from key_exec

    # noinspection PyTypeChecker
    return tuple(characters)


def remove_overlap(events: Iterator[TimelineEvent]) -> List[TimelineEvent]:
    all_events_list = list(events)

    num_overlapping_events = find_overlap_last_page_index(
        [hash(e) for e in all_events_list]
    )

    return trim_overlapped_list(all_events_list, num_overlapping_events)


def trim_overlapped_list(events: List[Any], num_overlapping_events: int) -> List[Any]:
    if num_overlapping_events == 0:
        return events

    if num_overlapping_events == NUM_LINES:
        return events[:-NUM_LINES]

    return events[:-NUM_LINES] + events[(-NUM_LINES + num_overlapping_events) :]


def find_overlap_last_page_index(hashes: List[int]) -> int:
    # can't contain overlap with less than one page of results
    if len(hashes) > NUM_LINES:

        # if full pages, assume a number evenly divisible by 30
        # otherwise, we can't know where the last page break is
        assert len(hashes) % NUM_LINES == 0

        last_page_hashes = hashes[-NUM_LINES:]
        second_last_page_hashes = hashes[-(NUM_LINES * 2) : -NUM_LINES]

        # starting with the maximum possible overlap, continuously check
        # smaller and smaller sections, until an overlap range is found

        # This does mean that there is no discernable difference between a
        # doubled event (same hash) that spans the last page boundary
        # and the same even showing up twice because of overlap

        # TODO: Consider using shift to get absolute times to avoid these edge cases
        for num_overlapping_events in range(NUM_LINES, 0, -1):
            if np.array_equal(
                last_page_hashes[:num_overlapping_events],
                second_last_page_hashes[-num_overlapping_events:],
            ):
                # it is possible to return a full page worth of overlap here
                # if the last two pages are identical
                # this seems highly unlikely
                return num_overlapping_events

    # if nothing is returned, it means there's no overlap
    return 0


def parse_time_digits(time_pic: np.ndarray) -> str:

    digit_width = 8
    digit_height = 12
    digit_top = 5

    elapsed_decimal_top = 13
    elapsed_decimal_left = 41
    elapsed_decimal_size = 5

    possible_decimal = time_pic[
        elapsed_decimal_top : elapsed_decimal_top + elapsed_decimal_size,
        elapsed_decimal_left : elapsed_decimal_left + elapsed_decimal_size,
    ]

    # both red and black hash for period location
    if hashlib.md5(possible_decimal.tobytes()).hexdigest() in (
        "0b4aa16ffb116f1b8cc4c0d940b6859f",
        "c8b5048bcbc949fff21066780a5ebb4e",
    ):
        # elapsed mode
        digit_offsets = [14, 23, 32, 46, 55]
        elapsed = True
    else:
        digit_offsets = [0, 9, 18, 32, 41, 55]
        elapsed = False

    digits = []

    for start in digit_offsets:
        digit = time_pic[
            digit_top : digit_top + digit_height, start : start + digit_width
        ]

        digit_hash = hashlib.md5(digit.tobytes()).hexdigest()
        try:
            digits.append(DIGIT_DICT[digit_hash])
        except KeyError as key_exec:
            logger.warning("TimelineParseException digit not found")
            capture_debug_picture(DEBUG_CAPTURES.joinpath("digits"), time_pic)
            raise TimelineDigitNotMatchedException("digit not found") from key_exec

    if elapsed:
        return "{}{}{}.{}{}".format(*digits).lstrip()

    return "{}{}{}:{}{}.{}".format(*digits).lstrip()


def process_line_image(line_image: np.ndarray) -> Optional[TimelineEvent]:
    if np.all(line_image == BACKGROUND_COLOR[0]):
        return None

    line_image = remove_highlighted_background(line_image)
    words, portraits, roles, books = separate_portraits(line_image)
    characters = name_portrait(portraits)
    actor_pic, time_pic, event_pic = split_into_parts(
        convert_black_white(add_borders(words))
    )

    time = parse_time_digits(time_pic)

    event_image_hash = hashlib.md5(event_pic.tobytes()).hexdigest()
    actor_image_hash = hashlib.md5(actor_pic.tobytes()).hexdigest()

    try:
        event = EVENT_IMAGE_HASH_DICT[event_image_hash]
    except KeyError as key_exec:
        logger.warning("TimelineParseException event not found")
        capture_debug_picture(DEBUG_CAPTURES.joinpath("events"), line_image)
        raise TimelineEventNotMatchedException("event not found") from key_exec

    try:
        actor = ACTOR_IMAGE_HASH_DICT[actor_image_hash]
    except KeyError as key_exec:
        logger.warning("TimelineParseException actor not found")
        capture_debug_picture(DEBUG_CAPTURES.joinpath("actors"), line_image)
        raise TimelineActorNotMatchedException("actor not found") from key_exec

    return TimelineEvent(actor, time, event, characters, roles, books)


def parse_screenshot(screenshot: np.ndarray) -> List[TimelineEvent]:
    lines = separate_line_images(screenshot)

    events = list(
        filter(lambda x: x is not None, [process_line_image(line) for line in lines])
    )

    return events


if __name__ == "__main__":
    pass
