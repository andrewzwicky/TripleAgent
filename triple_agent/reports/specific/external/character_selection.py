import os
import json
from collections import defaultdict

from tabulate import tabulate

from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl5_with_drops
from triple_agent.constants.paths import CASTER_DATA_FOLDER, SPF_DATA_FOLDER
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.specific.character_selection import _determine_spy
from triple_agent.reports.generation.plot_utilities import (
    create_data_dictionary,
    tableize_data_dict,
)
from triple_agent.classes.characters import Characters
from triple_agent.classes.roles import Roles


def caster_report_spy_selection():
    scl5_replays = get_parsed_replays(select_scl5_with_drops)
    all_replays = get_parsed_replays(lambda x: True)

    _, scl5_data_dict_percent = create_data_dictionary(
        scl5_replays, _determine_spy, lambda game: game.spy
    )
    _, all_data_dict_percent = create_data_dictionary(
        all_replays, _determine_spy, lambda game: game.spy
    )

    scl5_data_table, scl5_headers = tableize_data_dict(
        scl5_data_dict_percent,
        Characters,
        title="Spy Character Selection",
        excluded_header_values=[Characters.Toby, Characters.Damon],
    )

    all_data_table, all_headers = tableize_data_dict(
        all_data_dict_percent,
        Characters,
        title="Spy Character Selection",
        excluded_header_values=[Characters.Toby, Characters.Damon],
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
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_scl5.json"), "w"
    ) as at_json_out:
        json.dump(scl5_nice_name_character_dict, at_json_out, indent=4)

    with open(
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_all.json"), "w"
    ) as at_json_out:
        json.dump(all_nice_name_character_dict, at_json_out, indent=4)

    with open(
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_scl5.txt"), "w"
    ) as at_text_out:
        at_text_out.write(tabulate(scl5_data_table, scl5_headers, floatfmt="0.2%"))

    with open(
        os.path.join(CASTER_DATA_FOLDER, "spy_selection_all.txt"), "w"
    ) as at_text_out:
        at_text_out.write(tabulate(all_data_table, all_headers, floatfmt="0.2%"))


def spf_character_selection_report():
    output_dictionary = {}

    all_replays = get_parsed_replays(lambda x: True)

    for game in all_replays:
        output_dictionary[game.uuid] = defaultdict(list)
        for event in game.timeline:
            if event.category & TimelineCategory.Cast:
                # assume there will only be one role in the cast portion
                output_dictionary[game.uuid][
                    event.role[0].name if event.role[0] else Roles.NoRole.name
                ].append(event.cast_name[0].name)

    with open(
        os.path.join(SPF_DATA_FOLDER, "character_selection.json"), "w"
    ) as at_json_out:
        json.dump(output_dictionary, at_json_out, indent=4)


if __name__ == "__main__":
    caster_report_spy_selection()
    spf_character_selection_report()
