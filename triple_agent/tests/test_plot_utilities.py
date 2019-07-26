from collections import defaultdict, Counter

import pytest

from triple_agent.reports.plot_utilities import create_data_dictionaries
from triple_agent.replays.get_parsed_replays import get_parsed_replays
from triple_agent.utilities.action_tests import ActionTest
from triple_agent.utilities.timeline import TimelineCategory

TEST_GAME_UUIDS = [
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

TEST_GAMES = get_parsed_replays(lambda game: game.uuid in TEST_GAME_UUIDS)

# This is a generic test query so that dependencies from
# other modules aren't brought into this module.
def TEST_AT_COUNT(games, data_dictionary):
    for game in games:
        for event in game.timeline:
            if event.category & TimelineCategory.ActionTest:
                data_dictionary[event.action_test] += 1


CREATE_DATA_DICTIONARY_TEST_CASES = [
    (
        TEST_AT_COUNT,
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
        TEST_AT_COUNT,
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
        TEST_AT_COUNT,
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
        TEST_AT_COUNT,
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
    query_function, groupby, expected_data_dict, expected_data_dict_percent
):
    data_dict, data_dict_percent = create_data_dictionaries(
        TEST_GAMES, query_function, groupby
    )

    assert data_dict == expected_data_dict
    assert data_dict_percent == expected_data_dict_percent
