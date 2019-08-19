import itertools
from collections import Counter, defaultdict
from typing import Any, Union, Callable, List, Tuple, Optional, DefaultDict

import pandas
from triple_agent.classes.game import Game
from triple_agent.classes.scl_set import SCLSet


def sort_frame_stacks(
    frame: pandas.DataFrame,
    stack_order: Optional[List[Any]] = None,
    stacks_are_categories: bool = False,
) -> pandas.DataFrame:
    if stacks_are_categories:
        return frame

    # if nothing is supplied, use the given data_part names and sort them.
    if stack_order is None:
        return frame.sort_index(axis="rows")

    return frame.reindex(stack_order, axis="rows")


def sort_and_limit_frame_categories(
    frame: pandas.DataFrame,
    category_data_order: Optional[Any] = None,
    category_name_order: Optional[Callable[[Any], int]] = None,
    reversed_categories: bool = False,
    limit: Optional[int] = None,
) -> pandas.DataFrame:
    # sort the categories
    # data_order takes priority if both are provided
    if category_data_order is not None:
        if category_data_order is sum:
            frame = frame.reindex(
                frame.sum().sort_values(ascending=False, kind="stable").index,
                axis="columns",
            )
        elif callable(category_data_order):
            sorted_categories = sorted(
                frame.columns, key=category_data_order, reverse=False
            )
            frame = frame.reindex(sorted_categories, axis="columns")
        else:
            frame = frame.reindex(
                frame.loc[category_data_order, :]
                .sort_values(ascending=False, kind="stable")
                .index,
                axis="columns",
            )

    elif category_name_order is not None:
        frame = frame.reindex(category_name_order, axis="columns", fill_value=0)

    # limit categories, None is OK here, and larger than the number of columns
    frame = frame.iloc[:, :limit]

    if reversed_categories:
        frame = frame[frame.columns[::-1]]

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


def create_initial_data_frame(
    data_dictionary: DefaultDict[Any, Counter]
) -> Tuple[pandas.DataFrame, bool]:
    stacks_are_categories = False

    categories = list(data_dictionary.keys())

    data_parts = set()
    for inner_dict in data_dictionary.values():
        for inner_key in inner_dict.keys():
            data_parts.add(inner_key)

    # TODO: This is preventing going to normal Enum instead of IntEnum
    stacks = sorted(list(data_parts))

    # Something needs to enumerate all the possibilities so the frame doesn't end up with NaN values in it.
    frame = pandas.DataFrame(
        data={cat: [data_dictionary[cat][s] for s in stacks] for cat in categories},
        columns=categories,
        index=stacks,
    )

    _, num_columns = frame.shape

    if num_columns == 1:
        stacks_are_categories = True
        frame = frame.transpose()

    return frame, stacks_are_categories


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
