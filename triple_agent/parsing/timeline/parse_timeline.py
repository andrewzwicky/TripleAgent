import hashlib
from multiprocessing import Pool
from typing import List, Tuple, Optional, Iterator

import cv2
import numpy as np
import pytesseract
from triple_agent.tests.create_screenshot_expecteds import confirm_categorizations
from triple_agent.classes.books import Books, COLORS_TO_BOOKS_ENUM
from triple_agent.classes.characters import Characters, PORTRAIT_MD5_DICT
from triple_agent.classes.roles import ROLE_COLORS_TO_ENUM, Roles
from triple_agent.classes.timeline import TimelineEvent

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

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
WHITE = (255, 255, 255)
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

TIMER_OFFSET = 59
TEXT_OFFSET = 125

ROLE_BORDER_SIZE = 2

SPY_P_TOP = 668
SPY_P_LEFT = 633
SPY_P_WIDTH = 2
SPY_P_HEIGHT = 25
TIMEOUT = 12  # seconds
TIME_STEP = 0.5


class TimelineParseException(Exception):
    pass


def ocr_core(
    line_image: np.ndarray, time_parse: bool, second_attempt: bool = False
) -> str:
    if time_parse:
        text = pytesseract.image_to_string(
            cv2.resize(line_image, None, fx=1.05, fy=1.05)
        )
        if ":" not in text:
            text = pytesseract.image_to_string(line_image)
    else:
        text = pytesseract.image_to_string(line_image)
    text = text.strip().lower()

    if not text and not second_attempt:
        second_try = ocr_core(line_image[:, :120], False, second_attempt=True)
        # TODO: resolve ugly special case for the word civilian.
        # For some reason 'sniper shot' and 'civilian' can be parsed on their own
        # but not together.
        if second_try == "sniper shot civ":
            return "sniper shot civilian."

    if not np.array_equal(line_image[13, 0], WHITE) and ":" in text:
        text = "-" + text

    return text


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

        try:
            characters.append(
                PORTRAIT_MD5_DICT[hashlib.md5(portrait.tostring()).hexdigest()]
            )
        except KeyError:
            raise TimelineParseException("character portrait not found")

    # noinspection PyTypeChecker
    return tuple(characters)


def remove_overlap(events: Iterator[TimelineEvent]) -> List[TimelineEvent]:
    all_events_list = list(events)

    if len(all_events_list) > 30:
        # if full pages, there must be a number evenly divisible by 30
        assert len(all_events_list) % 30 == 0

        last_page_hashes = [hash(event) for event in all_events_list[-30:]]
        second_last_page_hashes = [hash(event) for event in all_events_list[-60:-30]]

        # iterating backwards over second to last page, look for the first event of the last page
        overlap = False
        last_page_index = 30

        for index, this_hash in enumerate(reversed(second_last_page_hashes), start=1):
            if this_hash == last_page_hashes[0]:
                last_page_index = 30 - index
                overlap = True
                break

        # if there is overlap, but not equal, the timeline should fail
        # coherency check
        if overlap:
            if np.array_equal(
                last_page_hashes[:-last_page_index],
                second_last_page_hashes[last_page_index:],
            ):
                del all_events_list[-30:-last_page_index]

    return all_events_list


def separate_time_digits(time_pic: np.ndarray) -> np.ndarray:
    offsets = [12, 23, 28, 38, 49, 54]
    for start in offsets:
        time_pic[:, start + 1 :] = time_pic[:, start:-1]
    return time_pic


def process_line_image(line_image: np.ndarray) -> Optional[TimelineEvent]:
    is_blank = np.all(line_image == BACKGROUND_COLOR[0])
    if is_blank:
        return None

    line_image = remove_highlighted_background(line_image)
    words, portraits, roles, books = separate_portraits(line_image)
    characters = name_portrait(portraits)
    actor_pic, time_pic, event_pic = split_into_parts(
        convert_black_white(add_borders(words))
    )
    separated_time_pic = separate_time_digits(time_pic)
    actor = ocr_core(actor_pic, False)
    time = ocr_core(separated_time_pic, True)
    event = ocr_core(event_pic, False)
    return TimelineEvent(actor, time, event, characters, roles, books)


def parse_screenshot(
    screenshot: np.ndarray, test_output_disable: bool = False
) -> List[TimelineEvent]:
    lines = separate_line_images(screenshot)

    # https://github.com/pytest-dev/pytest-cov/issues/250

    pool = Pool(processes=2)

    try:
        events = pool.map(process_line_image, lines)
    finally:
        pool.close()
        pool.join()

    while events and events[-1] is None:
        events.pop()

    if not test_output_disable:
        confirm_categorizations(events)

    return events


if __name__ == "__main__":
    pass
