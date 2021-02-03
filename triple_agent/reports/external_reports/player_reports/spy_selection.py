from triple_agent.constants.paths import PLAYER_REPORT_FOLDER
from triple_agent.reports.specific.character_selection import _determine_spy
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from triple_agent.reports.generation.generate_external_reports import (
    generate_external_reports,
)


def player_spy_selection_report(replays, report_name):
    generate_external_reports(
        replays,
        DataQueryProperties(
            query_function=_determine_spy,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        PLAYER_REPORT_FOLDER.joinpath(f"{report_name}.json"),
        PLAYER_REPORT_FOLDER.joinpath(f"{report_name}.html"),
    )
