from collections import defaultdict, Counter

import pytest

from triple_agent.reports.plot_utilities import create_sorted_categories

SORTED_CATEGORY_TEST_CASES = [
    (
        Counter({"player_a": 10, "player_b": 15, "player_c": 6, "player_d": 22}),
        None,
        False,
        None,
        ["player_a", "player_b", "player_c", "player_d"],
    ),
    (
        Counter({"player_b": 10, "player_x": 15, "player_c": 6, "player_d": 22}),
        None,
        False,
        None,
        ["player_b", "player_x", "player_c", "player_d"],
    ),
    (
        Counter({"player_b": 10, "player_x": 15, "player_c": 6, "player_d": 22}),
        None,
        False,
        lambda s: s,
        ["player_b", "player_c", "player_d", "player_x"],
    ),
    (
        Counter({"player_b": 10, "player_x": 15, "player_c": 6, "player_d": 22}),
        None,
        True,
        lambda s: s,
        ["player_x", "player_d", "player_c", "player_b"],
    ),
    (
        Counter({"player_a": 10, "player_b": 15, "player_c": 6, "player_d": 22}),
        None,
        True,
        None,
        ["player_d", "player_c", "player_b", "player_a"],
    ),
    (
        Counter({"player_a": 10, "player_b": 15, "player_c": 6, "player_d": 22}),
        sum,
        False,
        None,
        ["player_c", "player_a", "player_b", "player_d"],
    ),
    (
        Counter({"player_a": 10, "player_b": 15, "player_c": 6, "player_d": 22}),
        sum,
        True,
        None,
        ["player_d", "player_b", "player_a", "player_c"],
    ),
    (
        Counter({"player_a": 10, "player_b": -15, "player_c": 6, "player_d": 22}),
        sum,
        True,
        None,
        ["player_d", "player_a", "player_c", "player_b"],
    ),
    (
        Counter({"player_a": 10, "player_b": -15, "player_c": 6, "player_d": 22}),
        lambda x: abs(x),
        True,
        None,
        ["player_d", "player_b", "player_a", "player_c"],
    ),
    (
        Counter({"player_a": 10, "player_b": -15, "player_c": 6, "player_d": 22}),
        lambda x: abs(x),
        False,
        None,
        ["player_c", "player_a", "player_b", "player_d"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_b": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter({"green": 7, "red": 3, "cancel": 3}),
            },
        ),
        None,
        False,
        None,
        ["player_a", "player_b", "player_c", "player_d"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_x": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter({"green": 7, "red": 3, "cancel": 3}),
            },
        ),
        None,
        False,
        None,
        ["player_a", "player_x", "player_c", "player_d"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_x": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter(),
            },
        ),
        None,
        False,
        None,
        ["player_a", "player_x", "player_c", "player_d"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_b": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter(),
            },
        ),
        sum,
        True,
        None,
        ["player_d", "player_a", "player_c", "player_b"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_b": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter(),
            },
        ),
        sum,
        True,
        lambda s: s,
        ["player_d", "player_a", "player_c", "player_b"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_x": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter({"green": 7, "red": 3, "cancel": 3}),
            },
        ),
        "green",
        False,
        None,
        ["player_c", "player_d", "player_x", "player_a"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_x": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter({"green": 7, "red": 3, "cancel": 3}),
            },
        ),
        "red",
        False,
        None,
        ["player_x", "player_a", "player_d", "player_c"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_x": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter({"green": 7, "red": 3, "cancel": 3}),
            },
        ),
        None,
        False,
        lambda s: s,
        ["player_a", "player_c", "player_d", "player_x"],
    ),
    (
        defaultdict(
            Counter,
            {
                "player_a": Counter({"green": 5, "red": 10, "cancel": 1}),
                "player_x": Counter({"green": 6, "red": 11, "cancel": 2}),
                "player_c": Counter({"green": 8, "red": 0, "cancel": 10}),
                "player_d": Counter({"green": 10, "red": 3, "cancel": 3}),
            },
        ),
        lambda x: (x["green"] - x["cancel"], x["red"]),
        True,
        lambda s: s,
        ["player_d", "player_x", "player_a", "player_c"],
    ),
]

@pytest.mark.quick
@pytest.mark.parametrize(
    "input_data_dict, sort_data_item, reversed_data_sort, static_order, expected_categories",
    SORTED_CATEGORY_TEST_CASES,
)
def test_create_sorted_categories(
    input_data_dict,
    sort_data_item,
    reversed_data_sort,
    static_order,
    expected_categories,
):
    actual_categories = create_sorted_categories(
        input_data_dict,
        sort_data_item,
        reversed_data_sort,
        static_order,
    )

    assert actual_categories == expected_categories
