from typing import List, Union, Optional

from triple_agent.reports.generation.plot_types import (
    create_line_plot,
    create_bar_plot,
    create_pie_chart,
)
from triple_agent.reports.generation.plot_utilities import (
    create_data_dictionary,
    create_initial_data_frame,
    sort_and_limit_frame_categories,
    sort_frame_stacks,
)
from triple_agent.classes.game import Game
from triple_agent.classes.scl_set import SCLSet
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
    DataQueryProperties,
)


def query(
    games: Union[List[Game], List[SCLSet]],
    data_query: DataQueryProperties,
    axis_properties: AxisProperties = None,
):
    """
    query is the default plotting interface.  Given a list of games/sets, and a function to
    classidy them, it will plot either a pie chart, bar plot, or stacked bar plot.  Can be used to
    created simple queries quickly.
    """

    axis_properties, data_props = populate_data_properties(
        games, data_query, axis_properties
    )

    if axis_properties.force_line:
        create_line_plot(axis_properties, data_props)
    elif axis_properties.force_bar or data_props.category_order != [None]:
        create_bar_plot(axis_properties, data_props)
    else:
        create_pie_chart(axis_properties, data_props)


def populate_data_properties(
    games: Union[List[Game], List[SCLSet]],
    data_query: DataQueryProperties,
    axis_properties: Optional[AxisProperties] = None,
):
    if axis_properties is None:
        axis_properties = AxisProperties()

    if data_query.percent_normalized_data:
        axis_properties.y_axis_percentage = True

    data_props = DataPlotProperties()

    # create data dictionary
    data_dictionary = create_data_dictionary(
        games,
        data_query.query_function,
        data_query.groupby,
        data_query.percent_normalized_data,
    )

    data_props.frame, data_props.stacks_are_categories = create_initial_data_frame(
        data_dictionary
    )
    data_props.frame = sort_and_limit_frame_categories(
        data_props.frame,
        data_query.category_data_order,
        data_query.category_name_order,
        data_query.reversed_categories,
        data_query.limit,
    )

    data_props.frame = sort_frame_stacks(data_props.frame, data_query.stack_order)

    # # create the list of x-axis categories. percentile needs to be it's own list
    # # so it can be separately sorted between the counts plot and the percentile plot
    # data_props.category_order = create_sorted_categories(
    #     data_dictionary,
    #     data_query.category_data_order,
    #     data_query.category_name_order,
    #     data_query.reversed_categories,
    # )
    #
    # # limit categories to reduce clutter
    # data_props.category_order = limit_categories(
    #     data_props.category_order, data_query.limit
    # )
    #
    # # sort
    # data_props.stack_order, data_props.data = create_data_stacks(
    #     data_props.category_order, data_dictionary, data_query.stack_order
    # )

    return axis_properties, data_props
