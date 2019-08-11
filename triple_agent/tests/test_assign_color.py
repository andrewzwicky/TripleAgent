import pytest
from triple_agent.classes.action_tests import assign_color, ActionTest

AT_TEST_CASES = [
    ("action test red: contact double agent", ActionTest.Red),
    ("action test green: contact double agent", ActionTest.Green),
    ("action test white: contact double agent", ActionTest.White),
    ("action test ignored: seduce target", ActionTest.Ignored),
    ("action test canceled: transfer microfilm", ActionTest.Canceled),
    ("test", ActionTest.NoAT),
]


@pytest.mark.parametrize("in_string, expected_at", AT_TEST_CASES)
def test_assign_color(in_string, expected_at):
    assert assign_color(in_string) == expected_at
