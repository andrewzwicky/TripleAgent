from dataclasses import dataclass, fields
from typing import Optional, List, Callable, Any, Dict, Union
from enum import Enum, auto

import pandas

from triple_agent.constants.colors import PlotColorsBase
from triple_agent.classes.game import Game
from triple_agent.classes.scl_set import SCLSet


class PlotLabelStyle(Enum):
    NoLabels = auto()
    Plain = auto()
    Full = auto()


@dataclass
# pylint: disable=too-many-instance-attributes
class AxisProperties:
    title: Optional[str] = None
    x_axis_label: Optional[str] = None
    y_axis_label: Optional[str] = None

    y_axis_percentage: bool = False
    x_axis_portrait: bool = False

    cumulative_histogram: bool = False

    savefig: Optional[str] = None

    force_bar: bool = False
    force_line: bool = False

    data_label_style: PlotLabelStyle = PlotLabelStyle.NoLabels
    primary_label_dict: Optional[Dict[Any, str]] = None
    secondary_label_dict: Optional[Dict[Any, str]] = None
    primary_hatch_dict: Optional[Dict[Any, Optional[str]]] = None
    primary_color_dict: Optional[Dict[Any, Optional[str]]] = None
    plot_colors: PlotColorsBase = PlotColorsBase()

    def update(self, suggested_axis_properties):
        if suggested_axis_properties is not None:
            if isinstance(suggested_axis_properties, AxisProperties):
                for field_obj in fields(self):
                    value = getattr(self, field_obj.name)
                    if value == field_obj.default:
                        sugg_value = getattr(suggested_axis_properties, field_obj.name)
                        if sugg_value != field_obj.default:
                            setattr(self, field_obj.name, sugg_value)


@dataclass
class DataPlotProperties:
    frame: pandas.DataFrame = None
    stacks_are_categories: bool = False


@dataclass
# pylint: disable=too-many-instance-attributes
class DataQueryProperties:
    # DataQueryProperties are things that are used to group, sort, collect
    # filter, etc. the data PRIOR to plotting.  These items are used to create the
    # data stacks and data labels, but shouldn't be needed in actual plotting routines.

    # query_function is the function that will be called for each game to collect the data.
    # default to just counting games, but this should be overridden to do anything useful
    query_function: Callable[
        [Union[List[Game], List[SCLSet]], Any], None
    ] = lambda _, __: None

    # groupby can be used to group the data into buckets, by spy or by sniper for example.
    groupby: Optional[Callable] = None

    # primary_order and secondary_order can be used to control the order that the data appears in.
    # If they are a function, they take in either a pandas Series or pandas Index and return an int.
    # If they are a list, they will replace the existing column or index completely (retaining old data).
    primary_order: Optional[Union[Callable[[Any, pandas.Index], int], List[Any]]] = None
    secondary_order: Optional[
        Union[Callable[[Any, pandas.Series], int], List[Any]]
    ] = None

    reverse_primary_order: bool = False
    reverse_secondary_order: bool = False

    limit: Optional[int] = None

    percent_normalized_data: bool = False

    def update(self, suggested_data_query):
        if suggested_data_query is not None:
            if isinstance(suggested_data_query, DataQueryProperties):
                for field_obj in fields(self):
                    value = getattr(self, field_obj.name)
                    if value == field_obj.default:
                        sugg_value = getattr(suggested_data_query, field_obj.name)
                        if sugg_value != field_obj.default:
                            setattr(self, field_obj.name, sugg_value)


def initialize_properties(
    axis_properties: AxisProperties,
    data_query: DataQueryProperties,
    suggested_axis_properties: AxisProperties = None,
    suggested_data_query: DataQueryProperties = None,
):
    axis_properties.update(suggested_axis_properties)
    data_query.update(suggested_data_query)

    return axis_properties, data_query
