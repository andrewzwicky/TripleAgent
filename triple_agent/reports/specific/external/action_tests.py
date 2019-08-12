import os
import json

from tabulate import tabulate

from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl5_with_drops
from triple_agent.constants.paths import CASTER_DATA_FOLDER
from triple_agent.reports.specific.action_tests import _at_rates_excluding_difficults
from triple_agent.reports.generation.plot_utilities import (
    create_data_dictionaries,
    tableize_data_dict,
)
from triple_agent.classes.action_tests import ActionTest


def caster_report_action_tests():
    scl5_replays = get_parsed_replays(select_scl5_with_drops)
    all_replays = get_parsed_replays(lambda x: True)

    _, scl5_data_dict_percent = create_data_dictionaries(
        scl5_replays, _at_rates_excluding_difficults, lambda game: game.spy
    )
    _, all_data_dict_percent = create_data_dictionaries(
        all_replays, _at_rates_excluding_difficults, lambda game: game.spy
    )

    scl5_data_table, scl5_headers = tableize_data_dict(
        scl5_data_dict_percent,
        ActionTest,
        title="SCL5 Spy Action Test %",
        excluded_header_values=[ActionTest.NoAT],
    )

    all_data_table, all_headers = tableize_data_dict(
        all_data_dict_percent,
        ActionTest,
        title="All Games Spy Action Test %",
        excluded_header_values=[ActionTest.NoAT],
    )

    scl5_nice_name_character_dict = {
        player: {character.name: rate for character, rate in sub_dict.items()}
        for player, sub_dict in scl5_data_dict_percent.items()
    }
    all_nice_name_character_dict = {
        player: {character.name: rate for character, rate in sub_dict.items()}
        for player, sub_dict in all_data_dict_percent.items()
    }

    with open(
        os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.json"), "w"
    ) as at_json_out:
        json.dump(scl5_nice_name_character_dict, at_json_out, indent=4)

    with open(
        os.path.join(CASTER_DATA_FOLDER, "action_test_all.json"), "w"
    ) as at_json_out:
        json.dump(all_nice_name_character_dict, at_json_out, indent=4)

    with open(
        os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.txt"), "w"
    ) as at_text_out:
        at_text_out.write(tabulate(scl5_data_table, scl5_headers, floatfmt="0.2%"))

    with open(
        os.path.join(CASTER_DATA_FOLDER, "action_test_all.txt"), "w"
    ) as at_text_out:
        at_text_out.write(tabulate(all_data_table, all_headers, floatfmt="0.2%"))


if __name__ == "__main__":
    caster_report_action_tests()
