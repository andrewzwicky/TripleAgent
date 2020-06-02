import re
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
    create_missions_color_dict,
    MISSION_PLOT_ORDER,
    MISSION_STATUS_PLOT_ORDER,
    Missions,
    MissionStatus,
    HARD_TELLS,
)
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    DataPlotProperties,
    initialize_properties,
)
from triple_agent.constants.colors import PlotColorsBase
from triple_agent.classes.timeline import TimelineCategory


PICK_UP_STATUE_RE = re.compile(r"picked up( fingerprintable)? statue( \(difficult\))?.")


def _mission_completes(games: List[Game], data_dictionary: Counter):
    for game in games:
        for mission in Missions:
            if mission & game.completed_missions:
                data_dictionary[mission] += 1


def _count_final_missions(games: List[Game], data_dictionary: Counter):
    for game in games:
        final_mission = Missions.NoMission
        for event in game.timeline:
            if event.category & TimelineCategory.MissionComplete:
                final_mission = event.mission

        data_dictionary[final_mission] += 1


def _average_hard_tells_per_game(games: List[Game], data_dictionary: Counter):
    num_hard_tells = 0
    for game in games:
        for event in game.timeline:
            if (event.category & TimelineCategory.MissionComplete) and (
                event.mission in HARD_TELLS
            ):
                num_hard_tells += 1

    data_dictionary[None] = num_hard_tells / len(games)


def _num_visits_to_finish_inspects(games: List[Game], data_dictionary: Counter):
    for game in games:
        num_pickups = 0
        for event in game.timeline:
            if PICK_UP_STATUE_RE.match(event.event):
                num_pickups += 1

        data_dictionary[num_pickups] += 1


# not a generic query_function, special case
def _mission_completes_details(games: List[Game], data_dictionary: defaultdict):
    for game in games:
        # TODO: doesn't really for for pick modes
        for mission in Missions:
            if mission & game.selected_missions and mission != Missions.NoMission:
                if mission & game.completed_missions:
                    data_dictionary[mission][MissionStatus.Complete] += 1
                else:
                    data_dictionary[mission][MissionStatus.Incomplete] += 1
            else:
                data_dictionary[mission][MissionStatus.Disabled] += 1


def mission_completion_query(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=create_missions_color_dict(axis_properties.plot_colors)
        ),
        DataQueryProperties(
            query_function=_mission_completes, secondary_order=MISSION_PLOT_ORDER
        ),
    )

    return query(games, data_query, axis_properties)


def final_mission_completion_query(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=create_missions_color_dict(axis_properties.plot_colors)
        ),
        DataQueryProperties(
            query_function=_count_final_missions, primary_order=MISSION_PLOT_ORDER
        ),
    )

    return query(games, data_query, axis_properties)


def average_hard_tell_count(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(force_bar=True),
        DataQueryProperties(query_function=_average_hard_tells_per_game),
    )

    return query(games, data_query, axis_properties)


def num_visits_to_finish_inspects(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    # TODO: This needs to be based on number of inspects required as well, not just visits per game
    # TODO: This also needs to account for venues without statues
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(),
        DataQueryProperties(query_function=_num_visits_to_finish_inspects),
    )

    return query(games, data_query, axis_properties)


def mission_completion(
    games: List[Game], title: str, plot_colors: PlotColorsBase = PlotColorsBase()
):
    """
    This report is slightly different, because the desire is to sort the data
    by mission, rather than by an attribute of the game itself.  This means
    it doesn't exactly fit into the existing report workflow
    """
    data_dictionary = defaultdict(Counter)

    _mission_completes_details(games, data_dictionary)

    frame = create_initial_data_frame(data_dictionary)

    frame = sort_and_limit_frame_categories(frame, secondary_order=MISSION_PLOT_ORDER)

    frame = sort_frame_stacks(frame, primary_order=MISSION_STATUS_PLOT_ORDER)

    frame = frame / frame.sum()

    create_bar_plot(
        AxisProperties(
            title=title,
            # TODO: make the data percentage based.
            y_axis_percentage=True,
            primary_color_dict={
                MissionStatus.Complete: plot_colors.color_1,
                MissionStatus.Incomplete: plot_colors.color_2,
                MissionStatus.Disabled: plot_colors.light_grey,
            },
        ),
        DataPlotProperties(frame=frame),
    )
