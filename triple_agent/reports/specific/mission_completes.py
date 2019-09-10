from collections import defaultdict, Counter
from typing import List

from triple_agent.reports.generation.plot_types import create_bar_plot
from triple_agent.reports.generation.generic_query import (
    query,
    create_initial_data_frame,
    sort_and_limit_frame_categories,
    sort_frame_stacks,
)
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
    initialize_properties,
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
            if mission & game.selected_missions and mission != Missions.NoMission:
                if mission & game.completed_missions:
                    data_dictionary[mission][1] += 1
                else:
                    data_dictionary[mission][2] += 1
            else:
                data_dictionary[mission][3] += 1


def mission_completion_query(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(primary_color_dict=MISSIONS_ENUM_TO_COLOR),
        DataQueryProperties(
            query_function=_mission_completes, primary_order=MISSION_PLOT_ORDER
        ),
    )

    query(games, data_query, axis_properties)


def mission_completion(games: List[Game], title: str):
    """
    This report is slightly different, because the desire is to sort the data
    by mission, rather than by an attribute of the game itself.  This means
    it doesn't exactly fit into the existing report workflow
    """
    data_dictionary = defaultdict(Counter)

    _mission_completes_details(games, data_dictionary)

    frame = create_initial_data_frame(data_dictionary)

    frame = sort_and_limit_frame_categories(frame, secondary_order=MISSION_PLOT_ORDER)

    frame = sort_frame_stacks(frame)

    frame = frame / frame.sum()

    # total_games = len(games)
    # complete_labels = []
    # incomplete_labels = []
    #
    # complete_percentage = []
    # incomplete_percentage = []
    #
    # for mission in Missions:
    #     if mission != Missions.Zero:
    #         completed = data_dictionary[mission][True]
    #         available = data_dictionary[mission][False] + completed
    #         perc_avail = 0 if total_games == 0 else (available / total_games)
    #         perc_complete_bar = 0 if available == 0 else (completed / total_games)
    #         perc_complete_label = 0 if available == 0 else (completed / available)
    #
    #         complete_percentage.append(perc_complete_bar)
    #         complete_labels.append(
    #             f"{completed:>3}/{available:>3}\n{perc_complete_label:>5.1%}"
    #         )
    #
    #         incomplete_percentage.append(perc_avail - perc_complete_bar)
    #         incomplete_labels.append(
    #             f"{available:>3}/{total_games:>3}\n{perc_avail:>5.1%}"
    #         )

    create_bar_plot(
        AxisProperties(
            title=title,
            # TODO: make the data percentage based.
            y_axis_percentage=True,
            primary_color_dict={
                1: "xkcd:green",
                2: "xkcd:eggshell",
                3: "xkcd:light grey",
            },
            primary_label_dict={1: "Complete", 2: "Incomplete", 3: "Disabled"},
        ),
        DataPlotProperties(frame=frame),
    )
