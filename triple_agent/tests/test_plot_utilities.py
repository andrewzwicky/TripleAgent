from collections import defaultdict, Counter

import pytest

from triple_agent.reports.plot_utilities import (
    create_data_dictionary,
    create_sorted_categories,
    create_data_stacks,
    create_data_label,
)
from triple_agent.replays.get_parsed_replays import get_parsed_replays
from triple_agent.utilities.action_tests import ActionTest
from triple_agent.utilities.timeline import TimelineCategory


@pytest.fixture(scope="session")
def init_test_games():
    test_game_uuids = [
        "8uf6pUK7TFegBD8Cbr2qMw",
        "as-RnR1RQruzhRDZr7JP9A",
        "h_fNkizcR0mBFlokph3yEw",
        "jhx6e7UpTmeKueggeGcAKg",
        "k415gCwtS3ml9_EzUPpWFw",
        "k8x3n_zfTtiw9FSS6rM13w",
        "lOGf7W_MSlu1RRYxW2MMsA",
        "OiG7qvC9QOaSKVGlesdpWQ",
        "TPWiwN2aQc6EHEf6jKDKaA",
        "UgPZ7k1cQoCT9c6a_oG46w",
        "vgAlD77AQw2XKTZq3H4NTg",
    ]

    return get_parsed_replays(lambda game: game.uuid in test_game_uuids)


# This is a generic test query so that dependencies from
# other modules aren't brought into this module.
def __test_at_count(games, data_dictionary):
    for game in games:
        for event in game.timeline:
            if event.category & TimelineCategory.ActionTest:
                data_dictionary[event.action_test] += 1


CREATE_DATA_LABEL_TEST_CASES = [
    (5, 10, "  5/ 10\n50.0%"),
    (200, 400, "200/400\n50.0%"),
    (100, 400, "100/400\n25.0%"),
    (100, 0, "100/  0\n 0.0%"),
    (100, 100, "100\n100.0%"),
    (20, 20, " 20\n100.0%"),
]


@pytest.mark.parametrize("count,total,expected_string", CREATE_DATA_LABEL_TEST_CASES)
def test_create_labels(count, total, expected_string):
    actual_string = create_data_label(count, total)

    assert actual_string == expected_string


CREATE_DATA_DICTIONARY_TEST_CASES = [
    (
        __test_at_count,
        None,
        Counter(
            {
                ActionTest.Green: 14,
                ActionTest.White: 34,
                ActionTest.Red: 2,
                ActionTest.Ignored: 2,
                ActionTest.Canceled: 1,
            }
        ),
        Counter(
            {
                ActionTest.Green: 14 / 53,
                ActionTest.White: 34 / 53,
                ActionTest.Red: 2 / 53,
                ActionTest.Ignored: 2 / 53,
                ActionTest.Canceled: 1 / 53,
            }
        ),
    ),
    (
        __test_at_count,
        lambda x: x.spy,
        defaultdict(
            Counter,
            {
                "Calvin Schoolidge": Counter(
                    {ActionTest.Green: 7, ActionTest.White: 13, ActionTest.Ignored: 2}
                ),
                "Max Edward Snax": Counter(
                    {
                        ActionTest.Green: 7,
                        ActionTest.White: 21,
                        ActionTest.Red: 2,
                        ActionTest.Canceled: 1,
                    }
                ),
            },
        ),
        defaultdict(
            Counter,
            {
                "Calvin Schoolidge": Counter(
                    {
                        ActionTest.Green: 7 / 22,
                        ActionTest.White: 13 / 22,
                        ActionTest.Ignored: 2 / 22,
                    }
                ),
                "Max Edward Snax": Counter(
                    {
                        ActionTest.Green: 7 / 31,
                        ActionTest.White: 21 / 31,
                        ActionTest.Red: 2 / 31,
                        ActionTest.Canceled: 1 / 31,
                    }
                ),
            },
        ),
    ),
    (
        __test_at_count,
        lambda x: x.sniper,
        defaultdict(
            Counter,
            {
                "Max Edward Snax": Counter(
                    {ActionTest.Green: 7, ActionTest.White: 13, ActionTest.Ignored: 2}
                ),
                "Calvin Schoolidge": Counter(
                    {
                        ActionTest.Green: 7,
                        ActionTest.White: 21,
                        ActionTest.Red: 2,
                        ActionTest.Canceled: 1,
                    }
                ),
            },
        ),
        defaultdict(
            Counter,
            {
                "Max Edward Snax": Counter(
                    {
                        ActionTest.Green: 7 / 22,
                        ActionTest.White: 13 / 22,
                        ActionTest.Ignored: 2 / 22,
                    }
                ),
                "Calvin Schoolidge": Counter(
                    {
                        ActionTest.Green: 7 / 31,
                        ActionTest.White: 21 / 31,
                        ActionTest.Red: 2 / 31,
                        ActionTest.Canceled: 1 / 31,
                    }
                ),
            },
        ),
    ),
    (
        __test_at_count,
        lambda x: x.venue,
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
        defaultdict(
            Counter,
            {
                "Balcony": Counter(
                    {
                        ActionTest.Green: 6 / 14,
                        ActionTest.White: 7 / 14,
                        ActionTest.Ignored: 1 / 14,
                    }
                ),
                "Terrace": Counter(
                    {
                        ActionTest.Green: 2 / 10,
                        ActionTest.White: 7 / 10,
                        ActionTest.Red: 1 / 10,
                    }
                ),
                "Gallery": Counter(
                    {
                        ActionTest.Green: 5 / 25,
                        ActionTest.White: 17 / 25,
                        ActionTest.Ignored: 1 / 25,
                        ActionTest.Canceled: 1 / 25,
                        ActionTest.Red: 1 / 25,
                    }
                ),
                "Ballroom": Counter({ActionTest.Green: 1 / 4, ActionTest.White: 3 / 4}),
            },
        ),
    ),
]


@pytest.mark.parametrize(
    "query_function,groupby,expected_data_dict,expected_data_dict_percent",
    CREATE_DATA_DICTIONARY_TEST_CASES,
)
def test_create_data_dictionaries(
    query_function,
    groupby,
    expected_data_dict,
    expected_data_dict_percent,
    init_test_games,
):
    data_dict, data_dict_percent = create_data_dictionary(
        init_test_games, query_function, groupby
    )

    assert data_dict == expected_data_dict
    assert data_dict_percent == expected_data_dict_percent


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
