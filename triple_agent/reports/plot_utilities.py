import itertools
from collections import Counter, defaultdict
from typing import List, Optional, Any, Union, Callable
from copy import copy


def limit_categories(categories, percentile_categories, limit):
    if limit is not None:
        if limit < len(categories):
            categories = categories[:limit]
            percentile_categories = percentile_categories[:limit]
    return categories, percentile_categories


def create_sorted_categories(
    data_dictionary: Union[Counter, defaultdict],
    data_sum: Counter,
    category_data_order: Any = None,
    reversed_data_sort: bool = False,
    category_name_order: Callable[[str], int] = None,
):
    categories = list(data_dictionary.keys())
    percentile_categories = copy(categories)
    # sort the categories
    if isinstance(data_dictionary, Counter):
        # pie chart or regular bar plot
        if category_data_order is not None:
            if category_data_order is sum:
                categories.sort(key=lambda c: data_sum[c])
            elif callable(category_data_order):
                categories.sort(
                    key=lambda c: category_data_order(data_dictionary[c], data_sum[c])
                )
        elif category_name_order is not None:
            categories.sort(key=category_name_order)
            percentile_categories.sort(key=category_name_order)

        percentile_categories = copy(categories)

    elif isinstance(data_dictionary, defaultdict):
        # stacked bar
        if category_data_order is not None:
            if category_data_order is sum:
                categories.sort(
                    key=lambda c: 0
                    if not data_sum[c]
                    else -sum(data_dictionary[c].values())
                )
                percentile_categories.sort(
                    key=lambda c: 0
                    if not data_sum[c]
                    else -sum(data_dictionary[c].values())
                )
            elif callable(category_data_order):
                categories.sort(
                    key=lambda c: category_data_order(data_dictionary[c], None)
                )
                percentile_categories.sort(
                    key=lambda c: category_data_order(data_dictionary[c], data_sum[c])
                )
            else:
                categories.sort(
                    key=lambda c: 0
                    if not data_sum[c]
                    else -data_dictionary[c][category_data_order]
                )
                percentile_categories.sort(
                    key=lambda c: 0
                    if not data_sum[c]
                    else -data_dictionary[c][category_data_order] / data_sum[c]
                )

        elif category_name_order is not None:
            categories.sort(key=category_name_order)
            percentile_categories.sort(key=category_name_order)
    else:
        raise ValueError

    if reversed_data_sort:
        categories = list(reversed(categories))
        percentile_categories = list(reversed(percentile_categories))

    return categories, percentile_categories


def create_data_dictionary(games, query_function, groupby):
    """
    This function will create the data used for the plots.  The expected formats are either:
    -A defaultdict(Counter), with the 1st level keys being the groupby categories and the 2nd level keys
    are the data categories.  This is for stacked bar plots.
    -A plain Counter, representing a possible pie chart / unstacked bar plot.
    """
    data_sum = Counter()

    if groupby is None:
        data_dictionary = Counter()
        query_function(games, data_dictionary)
        data_sum = copy(data_dictionary)

    else:
        data_dictionary = defaultdict(Counter)
        for category, cat_games in itertools.groupby(
            sorted(games, key=groupby), key=groupby
        ):
            query_function(cat_games, data_dictionary[category])
            data_sum[category] = sum(data_dictionary[category].values())

    return data_dictionary, data_sum
