import os

from triple_agent.reports.specific.action_tests import _at_rates_excluding_difficults
from triple_agent.constants.paths import PLAYER_REPORT_FOLDER
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from triple_agent.reports.generation.generate_external_reports import (
    generate_external_reports,
)


def player_at_reports(replays, report_name):
    generate_external_reports(
        replays,
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(PLAYER_REPORT_FOLDER, f"{report_name}.json"),
        os.path.join(PLAYER_REPORT_FOLDER, f"{report_name}.html"),
    )
