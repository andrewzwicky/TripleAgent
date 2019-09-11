from collections import defaultdict
import os
import json
from enum import Enum

from triple_agent.classes.action_tests import AT_PREFERRED_PIE_CHART_ORDER
from triple_agent.classes.missions import Missions
from triple_agent.classes.outcomes import WinType
from triple_agent.reports.specific.action_tests import _at_rates_excluding_difficults
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl5_with_drops
from triple_agent.constants.paths import CASTER_DATA_FOLDER, SPF_DATA_FOLDER
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.specific.character_selection import _determine_spy
from triple_agent.reports.generation.generic_query import populate_data_properties
from triple_agent.reports.generation.plot_specs import DataQueryProperties


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


def spf_character_selection_report(games):
    output_dictionary = {}

    for game in games:
        output_dictionary[game.uuid] = defaultdict(list)
        output_dictionary[game.uuid]["Shot"] = [None]
        for event in game.timeline:
            if event.category & TimelineCategory.Cast:
                # assume there will only be one role in the cast portion
                # assume there will be a role in the Cast timeline events.
                output_dictionary[game.uuid][event.role[0].name].append(
                    event.cast_name[0].name
                )

            if event.category & TimelineCategory.GameEnd and game.win_type in (
                WinType.SpyShot,
                WinType.CivilianShot,
            ):
                output_dictionary[game.uuid]["Shot"] = [event.cast_name[0].name]

    with open(os.path.join(SPF_DATA_FOLDER, "character_data.json"), "w") as at_json_out:
        json.dump(output_dictionary, at_json_out, indent=4)


def spf_action_test_report(games):
    output_dictionary = {}

    for game in games:
        output_dictionary[game.uuid] = []
        for event in game.timeline:
            if event.category & TimelineCategory.ActionTest:
                to_add = {
                    "action": event.mission.name,
                    "elapsed_time": event.elapsed_time,
                    "spy_time": event.time,
                    "action_test": event.action_test.name,
                    "difficult": False,
                }
                if event.category & TimelineCategory.TimeAdd:
                    to_add["action"] = "TimeAdd"

                if event.mission == Missions.Fingerprint:
                    to_add["difficult"] = True

                output_dictionary[game.uuid].append(to_add)

    with open(os.path.join(SPF_DATA_FOLDER, "action_test.json"), "w") as at_json_out:
        json.dump(output_dictionary, at_json_out, indent=4)


if __name__ == "__main__":
    ALL_REPLAYS = get_parsed_replays(lambda x: True)
    SCL5_REPLAYS = get_parsed_replays(select_scl5_with_drops)

    generate_external_reports(
        SCL5_REPLAYS,
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
            primary_order=AT_PREFERRED_PIE_CHART_ORDER,
        ),
        os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.json"),
        os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.html"),
    )

    generate_external_reports(
        ALL_REPLAYS,
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
            primary_order=AT_PREFERRED_PIE_CHART_ORDER,
        ),
        os.path.join(CASTER_DATA_FOLDER, "action_test_all.json"),
        os.path.join(CASTER_DATA_FOLDER, "action_test_all.html"),
    )

    generate_external_reports(
        SCL5_REPLAYS,
        DataQueryProperties(
            query_function=_determine_spy,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_scl5.json"),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_scl5.html"),
    )

    generate_external_reports(
        ALL_REPLAYS,
        DataQueryProperties(
            query_function=_determine_spy,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_all.json"),
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_all.html"),
    )

    spf_character_selection_report(ALL_REPLAYS)
    spf_action_test_report(ALL_REPLAYS)
