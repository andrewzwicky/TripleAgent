import os

from triple_agent.classes.action_tests import AT_PREFERRED_PIE_CHART_ORDER
from triple_agent.reports.specific.action_tests import _at_rates_excluding_difficults
from triple_agent.constants.paths import PLAYER_REPORT_FOLDER
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from reports.generation.generate_external_reports import generate_external_reports


def generate_player_action_test_reports(all_replays, scl5_replays):
    generate_external_reports(
        scl5_replays,
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
            primary_order=AT_PREFERRED_PIE_CHART_ORDER,
        ),
        os.path.join(PLAYER_REPORT_FOLDER, "action_test_scl5.json"),
        os.path.join(PLAYER_REPORT_FOLDER, "action_test_scl5.html"),
    )

    generate_external_reports(
        all_replays,
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
            primary_order=AT_PREFERRED_PIE_CHART_ORDER,
        ),
        os.path.join(PLAYER_REPORT_FOLDER, "action_test_all.json"),
        os.path.join(PLAYER_REPORT_FOLDER, "action_test_all.html"),
    )
