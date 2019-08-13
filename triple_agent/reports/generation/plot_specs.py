from dataclasses import dataclass
from typing import Optional, List, Union, Callable, Any, Dict


@dataclass
class AxisProperties:
    title: Optional[str] = None
    x_axis_label: Optional[str] = None
    y_axis_label: Optional[str] = None
    y_axis_percentage: bool = False
    x_axis_portrait: bool = False
    savefig: Optional[str] = None


@dataclass
class DataPlotProperties:
    data: List[List[Union[int, float]]] = None
    category_labels: List[str] = None
    stack_labels: Optional[List[str]] = None
    bar_labels: List[List[Union[int, float]]] = None
    colors: Optional[List[str]] = None
    data_hatching: Optional[List[Optional[str]]] = None


@dataclass
class DataQueryProperties:
    # DataQueryProperties are things that are used to group, sort, collect
    # filter, etc. the data PRIOR to plotting.  These items are used to create the
    # data stacks and data labels, but shouldn't be needed in actual plotting routines.
    query_function: Callable = None
    data_stack_order: List[Any] = None
    data_stack_label_dict: Dict[Any, str] = None
    data_color_dict: Dict[str, str] = None
    groupby: Callable = None
    category_name_order: Callable[[str], int] = None
    category_data_order: Any = None
    reversed_data_sort: bool = False
    limit: Optional[int] = None
    force_bar: bool = False
    force_line: bool = False
    percent_data: bool = False
