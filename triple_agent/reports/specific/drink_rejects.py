from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)

TAKE_ORDER = ["purloin", "fingerprint", "take", "gave up", "reject"]


def _drink_takes(games, data_dictionary):
    for game in games:
        tracking_drink = False
        waiting_for_fp = False
        for timeline_event in game.timeline:
            if timeline_event.event == "waiter offered drink.":
                tracking_drink = True
                waiting_for_fp = False
                continue

            if tracking_drink:
                # look for next thing
                # could be problematic if this is the absolute last item?  seems unlikely.
                if (timeline_event.category & TimelineCategory.ActionTest) and (
                    timeline_event.mission & Missions.Purloin
                ):
                    data_dictionary["purloin"] += 1
                    tracking_drink = False
                    waiting_for_fp = False
                    continue

                if timeline_event.event == "rejected drink from waiter.":
                    data_dictionary["reject"] += 1
                    tracking_drink = False
                    waiting_for_fp = False
                    continue

                if timeline_event.event == "got drink from waiter.":
                    # need to wait for possible fingerprint
                    # this is sketchy because missed AT on drink are not different from any other object
                    waiting_for_fp = True
                    continue

                if timeline_event.event == "fingerprinted drink.":
                    data_dictionary["fingerprint"] += 1
                    tracking_drink = False
                    waiting_for_fp = False
                    continue

                if timeline_event.event in (
                    "waiter offered drink.",
                    "took last sip of drink.",
                    "took last bite of cupcake.",
                    "gulped drink.",
                    "chomped cupcake.",
                ):
                    if waiting_for_fp:
                        data_dictionary["take"] += 1
                    tracking_drink = False
                    waiting_for_fp = False
                    continue

                if timeline_event.event == "waiter gave up.":
                    data_dictionary["gave up"] += 1
                    tracking_drink = False
                    waiting_for_fp = False
                    continue

        if tracking_drink:
            # timeline ran out of events, no FP, just call it a take.
            data_dictionary["take"] += 1


def drink_takes(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties=axis_properties,
        data_query=data_query,
        suggested_data_query=DataQueryProperties(
            query_function=_drink_takes, primary_order=TAKE_ORDER
        ),
    )

    return query(games, data_query, axis_properties)
