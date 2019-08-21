import os
import json

from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl5_with_drops
from triple_agent.constants.paths import CASTER_DATA_FOLDER
from triple_agent.reports.specific.action_tests import _at_rates_excluding_difficults
from triple_agent.reports.generation.generic_query import populate_data_properties
from triple_agent.reports.generation.plot_specs import DataQueryProperties


def caster_report_action_tests():
    scl5_replays = get_parsed_replays(select_scl5_with_drops)
    # all_replays = get_parsed_replays(lambda x: True)

    _, scl5_props = populate_data_properties(
        scl5_replays,
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy)
    )
    #
    # _, all_props = populate_data_properties(
    #     all_replays,
    #     DataQueryProperties(
    #         query_function=_at_rates_excluding_difficults,
    #         groupby=lambda game: game.spy)
    # )

    # https://github.com/pandas-dev/pandas/issues/15273
    scl5_props.frame.to_json(os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.json"))

    # with open(
    #     os.path.join(CASTER_DATA_FOLDER, "action_test_all.json"), "w"
    # ) as at_json_out:
    #     json.dump(all_props.frame.to_json(), at_json_out, indent=4)
    #
    scl5_props.frame.T.to_html(os.path.join(CASTER_DATA_FOLDER, "action_test_scl5.html"))

    #
    # with open(
    #     os.path.join(CASTER_DATA_FOLDER, "action_test_all.html"), "w"
    # ) as at_text_out:
    #     at_text_out.write(all_props.frame.to_html())


if __name__ == "__main__":
    caster_report_action_tests()
