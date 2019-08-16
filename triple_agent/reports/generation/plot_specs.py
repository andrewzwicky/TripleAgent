from dataclasses import dataclass, fields
from typing import Optional, List, Union, Callable, Any, Dict
from enum import Enum, auto


class PlotLabelStyle(Enum):
    NoLabels = auto()
    Plain = auto()
    Full = auto()


@dataclass
class AxisProperties:
    title: Optional[str] = None
    x_axis_label: Optional[str] = None
    y_axis_label: Optional[str] = None
    y_axis_percentage: bool = False
    x_axis_portrait: bool = False
    savefig: Optional[str] = None
    force_bar: bool = False
    force_line: bool = False
    data_label_style: PlotLabelStyle = PlotLabelStyle.NoLabels
    data_stack_label_dict: Optional[Dict[Any, str]] = None
    data_hatch_dict: Optional[Dict[Any, Optional[str]]] = None
    data_color_dict: Optional[Dict[Any, Optional[str]]] = None

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
    data: List[List[Union[int, float]]] = None
    category_order: List[Any] = None
    stack_order: List[Any] = None


@dataclass
class DataQueryProperties:
    # DataQueryProperties are things that are used to group, sort, collect
    # filter, etc. the data PRIOR to plotting.  These items are used to create the
    # data stacks and data labels, but shouldn't be needed in actual plotting routines.
    query_function: Callable = None
    stack_order: List[Any] = None
    groupby: Callable = None
    category_name_order: Callable[[str], int] = None
    category_data_order: Any = None
    reversed_data_sort: bool = False
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
    axis_properties: Optional[AxisProperties],
    data_query: Optional[DataQueryProperties],
    suggested_axis_properties: AxisProperties = None,
    suggested_data_query: DataQueryProperties = None,
):
    axis_properties = AxisProperties() if axis_properties is None else axis_properties
    data_query = DataQueryProperties() if data_query is None else data_query

    axis_properties.update(suggested_axis_properties)
    data_query.update(suggested_data_query)

    return axis_properties, data_query
