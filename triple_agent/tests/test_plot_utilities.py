from collections import defaultdict, Counter

import pytest

from triple_agent.reports.generation.plot_utilities import (
    create_sorted_categories,
    create_data_stacks,
)

from triple_agent.classes.action_tests import ActionTest


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
        input_data_dict, sort_data_item, reversed_data_sort, static_order
    )

    assert actual_categories == expected_categories


CREATE_DATA_STACKS_TEST_CASES = [
    (
        ["cat_a", "cat_b", "cat_c"],
        Counter({"cat_a": 10, "cat_b": 11, "cat_c": 2}),
        None,
        ["cat_a", "cat_b", "cat_c"],
        [10, 11, 2],
    ),
    (
        ["cat_a", "cat_b", "cat_c"],
        Counter({"cat_a": 10, "cat_b": 11, "cat_c": 2}),
        ["cat_a"],
        ["cat_a"],
        [10],
    ),
    (
        ["cat_a", "cat_b", "cat_c"],
        Counter({"cat_a": 10, "cat_b": 11, "cat_c": 2}),
        ["cat_b"],
        ["cat_b"],
        [11],
    ),
    (
        ["cat_a", "cat_b", "cat_c"],
        Counter({"cat_a": 10, "cat_b": 11, "cat_c": 2}),
        ["cat_b", "cat_c", "cat_a"],
        ["cat_b", "cat_c", "cat_a"],
        [11, 2, 10],
    ),
    (
        ["Balcony", "Terrace", "Gallery", "Ballroom"],
        defaultdict(
            Counter,
            {
                "Balcony": Counter(
                    {ActionTest.Green: 6, ActionTest.White: 7, ActionTest.Ignored: 1}
                ),
                "Terrace": Counter(
                    {ActionTest.Green: 2, ActionTest.White: 7, ActionTest.Red: 1}
                ),
                "Gallery": Counter(
                    {
                        ActionTest.Green: 5,
                        ActionTest.White: 17,
                        ActionTest.Ignored: 1,
                        ActionTest.Canceled: 1,
                        ActionTest.Red: 1,
                    }
                ),
                "Ballroom": Counter({ActionTest.Green: 1, ActionTest.White: 3}),
            },
        ),
        None,
        [
            ActionTest.Green,
            ActionTest.White,
            ActionTest.Ignored,
            ActionTest.Red,
            ActionTest.Canceled,
        ],
        [[6, 2, 5, 1], [7, 7, 17, 3], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0]],
    ),
    (
        ["Balcony", "Terrace", "Gallery", "Ballroom"],
        defaultdict(
            Counter,
            {
                "Balcony": Counter(
                    {ActionTest.Green: 6, ActionTest.White: 7, ActionTest.Ignored: 1}
                ),
                "Terrace": Counter(
                    {ActionTest.Green: 2, ActionTest.White: 7, ActionTest.Red: 1}
                ),
                "Gallery": Counter(
                    {
                        ActionTest.Green: 5,
                        ActionTest.White: 17,
                        ActionTest.Ignored: 1,
                        ActionTest.Canceled: 1,
                        ActionTest.Red: 1,
                    }
                ),
                "Ballroom": Counter({ActionTest.Green: 1, ActionTest.White: 3}),
            },
        ),
        [ActionTest.Green, ActionTest.White],
        [ActionTest.Green, ActionTest.White],
        [[6, 2, 5, 1], [7, 7, 17, 3]],
    ),
    (
        ["Balcony", "Terrace", "Gallery", "Ballroom"],
        defaultdict(
            Counter,
            {
                "Balcony": Counter(
                    {ActionTest.Green: 6, ActionTest.White: 7, ActionTest.Ignored: 1}
                ),
                "Terrace": Counter(
                    {ActionTest.Green: 2, ActionTest.White: 7, ActionTest.Red: 1}
                ),
                "Gallery": Counter(
                    {
                        ActionTest.Green: 5,
                        ActionTest.White: 17,
                        ActionTest.Ignored: 1,
                        ActionTest.Canceled: 1,
                        ActionTest.Red: 1,
                    }
                ),
                "Ballroom": Counter({ActionTest.Green: 1, ActionTest.White: 3}),
            },
        ),
        [ActionTest.Green, ActionTest.White, 450],
        [ActionTest.Green, ActionTest.White, 450],
        [[6, 2, 5, 1], [7, 7, 17, 3], [0, 0, 0, 0]],
    ),
]


@pytest.mark.parametrize(
    "categories, data_dictionary, data_stack_order, expected_data_stack_order, expected_stacked_data",
    CREATE_DATA_STACKS_TEST_CASES,
)
def test_create_data_stacks(
    categories,
    data_dictionary,
    data_stack_order,
    expected_data_stack_order,
    expected_stacked_data,
):
    data_stack_order, stacked_data = create_data_stacks(
        categories, data_dictionary, data_stack_order
    )

    assert data_stack_order == expected_data_stack_order
    assert stacked_data == expected_stacked_data


def test_data_stacks_raise_value():
    with pytest.raises(ValueError):
        create_data_stacks(["a"], [1, 2, 3], None)
