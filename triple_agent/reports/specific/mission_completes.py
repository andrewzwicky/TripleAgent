from collections import defaultdict, Counter
from typing import List

from triple_agent.reports.generation.report_utilities import create_bar_plot
from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.missions import (
    MISSIONS_ENUM_TO_COLOR,
    MISSION_PLOT_ORDER,
    Missions,
)
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    DataPlotProperties,
    create_properties_if_none,
)


def _mission_completes(games: List[Game], data_dictionary: Counter):
    for game in games:
        for mission in Missions:
            if mission & game.completed_missions:
                data_dictionary[mission] += 1


# not a generic query_function, special case
def _mission_completes_details(games: List[Game], data_dictionary: defaultdict):
    for game in games:
        # TODO: doesn't really for for pick modes
        for mission in Missions:
            if mission & game.selected_missions and mission != Missions.Zero:
                if mission & game.completed_missions:
                    data_dictionary[mission][True] += 1
                else:
                    data_dictionary[mission][False] += 1


def mission_completion_query(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    create_properties_if_none(axis_properties, data_query)

    data_query.query_function = _mission_completes
    data_query.data_stack_order = MISSION_PLOT_ORDER
    data_query.data_color_dict = MISSIONS_ENUM_TO_COLOR

    query(games, data_query, axis_properties)


def mission_completion(games: List[Game], title: str):
    """
    This report is slightly different, because the desire is to sort the data
    by mission, rather than by an attribute of the game itself.  This means
    it doesn't exactly fit into the existing report workflow
    """

    total_games = len(games)

    data_dictionary = defaultdict(Counter)

    _mission_completes_details(games, data_dictionary)

    complete_labels = []
    incomplete_labels = []

    complete_percentage = []
    incomplete_percentage = []

    for mission in Missions:
        if mission != Missions.Zero:
            completed = data_dictionary[mission][True]
            available = data_dictionary[mission][False] + completed
            perc_avail = 0 if total_games == 0 else (available / total_games)
            perc_complete_bar = 0 if available == 0 else (completed / total_games)
            perc_complete_label = 0 if available == 0 else (completed / available)

            complete_percentage.append(perc_complete_bar)
            complete_labels.append(
                f"{completed:>3}/{available:>3}\n{perc_complete_label:>5.1%}"
            )

            incomplete_percentage.append(perc_avail - perc_complete_bar)
            incomplete_labels.append(
                f"{available:>3}/{total_games:>3}\n{perc_avail:>5.1%}"
            )

    create_bar_plot(
        AxisProperties(title=title, y_axis_percentage=True),
        DataPlotProperties(
            data=[complete_percentage, incomplete_percentage],
            colors=["xkcd:green", "xkcd:light grey"],
            category_labels=[m.name for m in Missions if m is not Missions.Zero]
            # bar_labels = [complete_labels, incomplete_labels]
        ),
    )
