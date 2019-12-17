import json
from enum import Enum

from triple_agent.reports.generation.generic_query import populate_data_properties


def generate_external_reports(
    games, data_query_properties, json_file_path, html_file_path
):
    _, data_props = populate_data_properties(games, data_query_properties)

    # https://github.com/pandas-dev/pandas/issues/15273
    # This means the normal .to_json doesn't work for a dataframe.
    if isinstance(data_props.frame.columns[0], Enum):
        data_props.frame.columns = data_props.frame.columns.map(lambda x: x.name)

    if isinstance(data_props.frame.index[0], Enum):
        data_props.frame.index = data_props.frame.index.map(lambda x: x.name)

    with open(json_file_path, "w") as at_json_out:
        json.dump(data_props.frame.to_dict(), at_json_out, indent=4)

    data_props.frame.T.to_html(html_file_path)
