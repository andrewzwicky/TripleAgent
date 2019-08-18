import os
import pickle
import re
from typing import List

import pytest
from triple_agent.classes.timeline import TimelineEvent

with open(os.path.join(os.path.dirname(__file__), "all_messages.pkl"), "rb") as pik:
    ALL_MESSAGES = pickle.load(pik)


@pytest.mark.plotting
def confirm_categorizations(timeline_events: List[TimelineEvent]):

    new_events = []
    fields = [
        "actor",
        "_raw_time_str",
        "event",
        "cast_name",
        "role",
        "books",
        "category",
        "mission",
        "action_test",
    ]

    spaced_print_str = "\n{:<6} {:<8} {:<45} {:<12} {:<23} {:<25} {:<45} {:<23} {:<20}"

    for line_no, event in enumerate(timeline_events, start=1):
        if (event.actor, event.event) not in ALL_MESSAGES:

            this_event_exp = [getattr(event, field) for field in fields]

            new_events.append(tuple(this_event_exp))
            ALL_MESSAGES.add((this_event_exp[0], this_event_exp[2]))

            print(
                spaced_print_str.format(
                    *[str(getattr(event, field)) for field in fields]
                )
            )

            trimmed_category_str = str(this_event_exp).lstrip("[").rstrip("]")
            new_category_str = trimmed_category_str

            for overall, enum, values in re.findall(
                r"(<(.*?)\.((?:\w+\|?)+):\s+\d+>)", trimmed_category_str
            ):
                replacement = " | ".join([enum + "." + v for v in values.split("|")])
                new_category_str = new_category_str.replace(overall, replacement)

            with open(
                os.path.join(
                    os.path.dirname(__file__), "expected_category_test_cases.txt"
                ),
                "a",
            ) as test_cases:
                test_cases.write(new_category_str + "," + "\n")

    if new_events:
        for new_e in new_events:
            ALL_MESSAGES.add((new_e[0], new_e[2]))
        with open(
            os.path.join(os.path.dirname(__file__), "all_messages.pkl"), "wb"
        ) as loop_pik:
            pickle.dump(ALL_MESSAGES, loop_pik)
