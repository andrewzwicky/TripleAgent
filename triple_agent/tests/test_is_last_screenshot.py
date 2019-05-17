import cv2
import pytest

from triple_agent.timeline.parse_timeline import is_last_screenshot

SCREENSHOT_TEST_CASES = [
    ("671152956268014896", False),
    ("1572372555002699956", False),
    ("3759441015284876045", False),
    ("6173092994452987597", False),
    ("8346478285034783689", False),
    ("-3070462071415144270", False),
    ("-5205483914183321949", True),
    ("-5381334556900546672", False),
    ("-6996172267372142000", True),
    ("-4284672900785851911", False),
    ("-3717661638173477014", False),
    ("2409467229694115669", True),
    ("4863254294007289095", False),
    ("highlight_and_bad_time", True),
    ("-4198543829091342944", True),
    ("bad_time", True),
    ("duke_spy", False),
    ("short_game", True),
]


def id_func(val):
    if isinstance(val, str):
        return val
    return ""


@pytest.mark.parametrize("image_name, expected_is_last", SCREENSHOT_TEST_CASES)
def test_is_last_screenshot(image_name: str, expected_is_last: bool):
    screenshot_img = cv2.imread(f"test_screenshots/{image_name}.png")
    is_last = is_last_screenshot(screenshot_img)

    assert is_last == expected_is_last
