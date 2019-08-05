import itertools
from collections import Counter, defaultdict
from typing import Any, Union, Callable


def limit_categories(categories, limit):
    if limit is not None:
        if limit < len(categories):
            categories = categories[:limit]
    return categories


def create_data_stacks(categories, data_dictionary, data_stack_order):
    """
    this function rearranges the data to stack in the proper order.  For example,
    if the data is grouped by venue, and each stack includes each win type (mission win,
    spy shot, timeout, and civ shot).  It makes sense to stack spy shot and timeout next
    to each other visually.

    This is still relevant even for pie charts, because it will change the order the
    slices appear in.

    data_stack_order that's missing things can omit data from the result.
    """
    # TODO: data stack order in defaultdict (stacked bar) will omit data
    stacked_data = []

    if isinstance(data_dictionary, defaultdict):
        # if nothing is supplied, use the given data_part names and sort them.
        if data_stack_order is None:
            data_parts = set()
            for value in data_dictionary.values():
                for inner_key in value.keys():
                    data_parts.add(inner_key)

            data_stack_order = sorted(data_parts)

        for data_part in data_stack_order:
            stacked_data.append([data_dictionary[cat][data_part] for cat in categories])
    elif isinstance(data_dictionary, Counter):
        # In the simple counter case, the categories are also the data_parts
        if data_stack_order is None:
            data_stack_order = categories

        # KeyError not an issue here, as these will be Counter classes, so 0 will be returned.
        # This also means that misspelled args in data_stack_order might be difficult to find.
        stacked_data = [data_dictionary[data_part] for data_part in data_stack_order]
    else:
        raise ValueError

    return data_stack_order, stacked_data


def create_data_label(count, total):
    percent = 0 if total == 0 else (count / total)
    if count == total and total != 0:
        return f"{total:>3}\n{percent:>5.1%}"

    return f"{count:>3}/{total:>3}\n{percent:>5.1%}"


def create_sorted_categories(
    data_dictionary: Union[Counter, defaultdict],
    category_data_order: Any = None,
    reversed_data_sort: bool = False,
    category_name_order: Callable[[str], int] = None,
):
    categories = list(data_dictionary.keys())
    category_lambdas = dict()
    category_lambdas["callable"] = lambda c: category_data_order(data_dictionary[c])

    if isinstance(data_dictionary, Counter):
        category_lambdas["sum"] = lambda c: data_dictionary[c]
        category_lambdas["none"] = lambda c: True
    elif isinstance(data_dictionary, defaultdict):
        category_lambdas["sum"] = lambda c: -sum(data_dictionary[c].values())
        category_lambdas["none"] = lambda c: -data_dictionary[c][category_data_order]
    else:
        raise ValueError

    # sort the categories
    if category_data_order is not None:
        if category_data_order is sum:
            categories.sort(key=category_lambdas["sum"])
        elif callable(category_data_order):
            categories.sort(key=category_lambdas["callable"])
        else:
            categories.sort(key=category_lambdas["none"])

    elif category_name_order is not None:
        categories.sort(key=category_name_order)

    if reversed_data_sort:
        categories = list(reversed(categories))

    return categories


def create_data_dictionaries(games, query_function, groupby):
    """
    This function will create the data used for the plots.  The expected formats are either:
    -A defaultdict(Counter), with the 1st level keys being the groupby categories and the 2nd level keys
    are the data categories.  This is for stacked bar plots.
    -A plain Counter, representing a possible pie chart / unstacked bar plot.
    This method will return both a counts based data_dictionary and a percentile_based_data_dictionary.
    """
    # TODO: data_dictionary_percent being a counter doesn't really make much sense
    if groupby is None:
        data_dictionary = Counter()
        data_dictionary_percent = Counter()

        populate_individual_counter(
            games, data_dictionary, data_dictionary_percent, query_function
        )

    else:
        data_dictionary = defaultdict(Counter)
        data_dictionary_percent = defaultdict(Counter)

        for category, cat_games in itertools.groupby(
            sorted(games, key=groupby), key=groupby
        ):
            populate_individual_counter(
                cat_games,
                data_dictionary[category],
                data_dictionary_percent[category],
                query_function,
            )

    return data_dictionary, data_dictionary_percent


def populate_individual_counter(
    games, data_dictionary, data_dictionary_percent, query_function
):
    query_function(games, data_dictionary)
    data_sum = sum(data_dictionary.values())
    data_dictionary_percent.update(
        {k: 0 if data_sum == 0 else v / data_sum for k, v in data_dictionary.items()}
    )


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
