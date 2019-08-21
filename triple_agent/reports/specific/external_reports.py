from collections import defaultdict
import os
import json
from enum import Enum

from triple_agent.reports.specific.action_tests import _at_rates_excluding_difficults
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl5_with_drops
from triple_agent.constants.paths import CASTER_DATA_FOLDER, SPF_DATA_FOLDER
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.specific.character_selection import _determine_spy
from triple_agent.reports.generation.generic_query import populate_data_properties
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from triple_agent.classes.roles import Roles


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


def spf_character_selection_report():
    output_dictionary = {}

    all_replays = get_parsed_replays(lambda x: True)

    for game in all_replays:
        output_dictionary[game.uuid] = defaultdict(list)
        for event in game.timeline:
            if event.category & TimelineCategory.Cast:
                # assume there will only be one role in the cast portion
                output_dictionary[game.uuid][
                    event.role[0].name if event.role[0] else Roles.Civilian.name
                ].append(event.cast_name[0].name)

    with open(
        os.path.join(SPF_DATA_FOLDER, "character_selection.json"), "w"
    ) as at_json_out:
        json.dump(output_dictionary, at_json_out, indent=4)


if __name__ == "__main__":
    generate_external_reports(
        get_parsed_replays(select_scl5_with_drops),
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.json"),
        os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.html"),
    )

    generate_external_reports(
        get_parsed_replays(lambda x: True),
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(CASTER_DATA_FOLDER, "action_test_all.json"),
        os.path.join(CASTER_DATA_FOLDER, "action_test_all.html"),
    )

    generate_external_reports(
        get_parsed_replays(select_scl5_with_drops),
        DataQueryProperties(
            query_function=_determine_spy,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_scl5.json"),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_scl5.html"),
    )

    generate_external_reports(
        get_parsed_replays(lambda x: True),
        DataQueryProperties(
            query_function=_determine_spy,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_all.json"),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_all.html"),
    )

    spf_character_selection_report()
