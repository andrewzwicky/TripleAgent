import os
from pathlib import Path

from triple_agent.reports.external_reports.player_reports.action_tests import (
    generate_player_action_test_reports,
)
from triple_agent.reports.external_reports.player_reports.spy_selection import (
    generate_player_spy_selection_report,
)
from triple_agent.reports.generation.ipython_notebook import execute_single_notebook
from triple_agent.constants.paths import (
    EXAMPLES_FOLDER,
    EVENT_REPORT_FOLDER,
    OVERALL_REPORT_FOLDER,
)
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.constants.events import select_scl5_with_drops
from triple_agent.reports.external_reports.spy_party_fans.character_selection import (
    spf_character_selection_report,
)
from triple_agent.reports.external_reports.spy_party_fans.action_tests import (
    spf_action_test_report,
)
from triple_agent.reports.external_reports.spy_party_fans.sniper_lights import (
    spf_lights_report,
)

EVENT_REPORT_SOURCE = Path(__file__).parents[0].joinpath("event_reports")
OVERALL_REPORT_SOURCE = Path(__file__).parents[0].joinpath("overall_reports")


def refresh_example_notebooks():
    os.chdir(EXAMPLES_FOLDER)
    for potential_notebook in os.listdir(EXAMPLES_FOLDER):
        if potential_notebook.endswith(".ipynb"):
            execute_single_notebook(potential_notebook)


def refresh_event_reports():
    for potential_notebook in os.listdir(EVENT_REPORT_SOURCE):
        if potential_notebook.endswith(".ipynb"):
            potential_path = os.path.join(EVENT_REPORT_SOURCE, potential_notebook)
            execute_single_notebook(potential_path)
            os.system(
                f'jupyter nbconvert --to html "{potential_path}" --output-dir="{EVENT_REPORT_FOLDER}"'
            )


def refresh_overall_reports():
    for potential_notebook in os.listdir(OVERALL_REPORT_SOURCE):
        if potential_notebook.endswith(".ipynb"):
            potential_path = os.path.join(OVERALL_REPORT_SOURCE, potential_notebook)
            execute_single_notebook(potential_path)
            os.system(
                f'jupyter nbconvert --to html "{potential_path}" --output-dir="{OVERALL_REPORT_FOLDER}"'
            )


def refresh_all_reports():
    ALL_REPLAYS = get_parsed_replays(lambda x: True)
    SCL5_REPLAYS = get_parsed_replays(select_scl5_with_drops)

    refresh_overall_reports()
    refresh_event_reports()
    generate_player_action_test_reports(ALL_REPLAYS, SCL5_REPLAYS)
    generate_player_spy_selection_report(ALL_REPLAYS, SCL5_REPLAYS)
    refresh_example_notebooks()
    spf_lights_report(ALL_REPLAYS)
    spf_action_test_report(ALL_REPLAYS)
    spf_character_selection_report(ALL_REPLAYS)


if __name__ == "__main__":
    refresh_all_reports()
