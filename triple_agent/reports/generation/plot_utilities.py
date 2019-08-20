import itertools
from collections import Counter, defaultdict
from typing import Any, Union, Callable, List, Optional, DefaultDict

import pandas
from triple_agent.classes.game import Game
from triple_agent.classes.scl_set import SCLSet


def sort_frame_stacks(
    frame: pandas.DataFrame,
    stack_order: Union[Callable[[Any, pandas.Index], int], List[Any]] = None,
    reverse_stack_order: bool = False,
) -> pandas.DataFrame:

    if callable(stack_order):
        if stack_order is sum:
            frame = frame.reindex(
                frame.T.sum().sort_values(kind="stable").index, axis="index"
            )
        else:
            sorted_items = sorted(frame.T.items(), key=stack_order)
            sorted_index, _ = zip(*sorted_items)
            frame = frame.reindex(sorted_index, axis="index")

    elif isinstance(stack_order, list):
        frame = frame.reindex(stack_order, axis="index", fill_value=0)

    else:
        try:
            frame = frame.sort_index(axis="index")
        except TypeError:
            # unsortable and nothing supplied, leave as-is
            pass

    if reverse_stack_order:
        frame = frame.iloc[::-1, :]

    return frame


def sort_and_limit_frame_categories(
    frame: pandas.DataFrame,
    category_order: Union[Callable[[Any, pandas.Series], int], List[Any]] = None,
    reverse_category_order: bool = False,
    limit: Optional[int] = None,
) -> pandas.DataFrame:
    # sort the categories
    # data_order takes priority if both are provided
    if callable(category_order):
        if category_order is sum:
            frame = frame.reindex(
                frame.sum().sort_values(kind="stable").index, axis="columns"
            )
        else:
            sorted_items = sorted(frame.items(), key=category_order)
            sorted_colums, _ = zip(*sorted_items)
            frame = frame.reindex(sorted_colums, axis="columns")

    elif isinstance(category_order, list):
        frame = frame.reindex(category_order, axis="columns", fill_value=0)

    else:
        try:
            frame = frame.sort_index(axis="columns")
        except TypeError:
            # unsortable and nothing supplied, leave as-is
            pass

    # limit categories, None is OK here, and larger than the number of columns
    frame = frame.iloc[:, :limit]

    if reverse_category_order:
        frame = frame.iloc[:, ::-1]

    return frame


def create_data_dictionary(
    games: Union[List[Game], List[SCLSet]],
    query_function: Callable,
    groupby: Optional[Callable] = None,
    percent_normalized_data: bool = False,
) -> DefaultDict[Any, Counter]:
    """
    This function will create the data used for the plots.  The expected formats are either:
    -A defaultdict(Counter), with the 1st level keys being the groupby categories and the 2nd level keys
    are the data categories.  This is for stacked bar plots.
    -A plain Counter, representing a possible pie chart / unstacked bar plot.
    This method will return both a counts based data_dictionary and a percentile_based_data_dictionary.
    """
    # TODO: data_dictionary_percent being a counter doesn't really make much sense
    data_dictionary = defaultdict(Counter)

    if groupby is None:
        data_dictionary[None] = populate_individual_counter(
            games, data_dictionary[None], query_function, percent_normalized_data
        )

    else:
        for category, cat_games in itertools.groupby(
            sorted(games, key=groupby), key=groupby
        ):
            data_dictionary[category] = populate_individual_counter(
                list(cat_games),
                data_dictionary[category],
                query_function,
                percent_normalized_data,
            )

    return data_dictionary


def populate_individual_counter(
    games: Union[List[Game], List[SCLSet]],
    category_dictionary: Counter,
    query_function: Callable,
    percent_normalized_data: bool = False,
) -> Counter:
    query_function(games, category_dictionary)

    if percent_normalized_data:
        data_sum = sum(category_dictionary.values())
        category_dictionary = Counter(
            {
                k: 0 if data_sum == 0 else v / data_sum
                for k, v in category_dictionary.items()
            }
        )

    return category_dictionary


def tableize_data_dict(
    data_dict, header_enum_type, title="", excluded_header_values=None
):
    if excluded_header_values is None:
        excluded_header_values = []

    data_table = []

    header_values = [
        val for val in header_enum_type if val not in excluded_header_values
    ]
    header_strings = [val.name for val in header_values]

    for player, count_info in data_dict.items():
        data_row = [player] + [count_info[val] for val in header_values]
        data_table.append(data_row)

    # sort by first item in data lists
    data_table.sort(key=lambda row: row[0].lower())
    header_row = [title] + header_strings

    return data_table, header_row


def create_initial_data_frame(
    data_dictionary: DefaultDict[Any, Counter]
) -> pandas.DataFrame:
    categories = list(data_dictionary.keys())

    data_parts = set()
    for inner_dict in data_dictionary.values():
        for inner_key in inner_dict.keys():
            data_parts.add(inner_key)

    stacks = list(data_parts)

    # Something needs to enumerate all the possibilities so the frame doesn't end up with NaN values in it.
    frame = pandas.DataFrame(
        data={cat: [data_dictionary[cat][s] for s in stacks] for cat in categories},
        columns=categories,
        index=stacks,
    )

    return frame
