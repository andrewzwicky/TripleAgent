import re
from collections.abc import Sequence
from datetime import datetime
from enum import IntFlag, auto
from typing import Optional, List, Tuple

from triple_agent.classes.action_tests import ActionTest, assign_color
from triple_agent.classes.books import Books
from triple_agent.classes.characters import Characters, CHARACTERS_TO_STRING
from triple_agent.classes.missions import (
    MISSION_COMPLETE_TIMELINE_TO_ENUM,
    MISSION_GENERIC_TIMELINE_TO_ENUM,
    MISSION_PARTIAL_TO_ENUM,
    Missions,
)
from triple_agent.classes.roles import Roles


class TimelineCategory(IntFlag):
    NoCategory = 0
    ActionTest = auto()
    ActionTriggered = auto()
    MissionPartial = auto()
    SniperLights = auto()
    MissionComplete = auto()
    MissionCountdown = auto()
    GameEnd = auto()
    GameStart = auto()
    TimeAdd = auto()
    Cast = auto()
    # selected means that the sniper can see it as a possible mission
    MissionSelected = auto()
    # enabled means that the spy can complete it, this will be smaller than
    # selected in pick modes.
    MissionEnabled = auto()
    SniperShot = auto()

    # Modifiers
    BananaBread = auto()
    Briefcase = auto()
    Statues = auto()
    Books = auto()
    Drinks = auto()
    Conversation = auto()
    Watch = auto()

    Overtime = auto()


class TimelineEvent:
    # this is needed for getting rid of commands and extra stuff from the OCR
    time_re = re.compile(r"(\d{2}:\d{2}.\d)")

    def __init__(
        self,
        actor: str,
        time_str: str,
        event: str,
        cast_name: Tuple[Optional[Characters]],
        role: Tuple[Optional[Roles]],
        books: Tuple[Optional[Books]],
    ):
        self.actor = actor
        self._raw_time_str = time_str
        try:
            self.time = (
                datetime.strptime(time_str, "%M:%S.%f")
                - datetime.strptime("00:00.0", "%M:%S.%f")
            ).total_seconds()
        except ValueError:
            self.time = (
                datetime.strptime("00:00.0", "%M:%S.%f")
                - datetime.strptime(time_str, "-%M:%S.%f")
            ).total_seconds()
        self.event = event
        self.elapsed_time = None
        self.cast_name = cast_name
        self.role = role
        self.books = books
        self.category = TimelineCategory.NoCategory
        self.mission = Missions.Zero
        self.action_test = ActionTest.NoAT
        self.categorize()

        assert len(self.cast_name) == len(self.role)

    def categorize(self):
        if self.event == "took shot." and self.actor == "sniper":
            self.category = TimelineCategory.SniperShot
            return

        if self.event.endswith("cast."):
            self.category = TimelineCategory.Cast
            return

        if self.actor == "game":
            if self.event == "game started.":
                self.category = TimelineCategory.GameStart
            elif self.event.startswith("missions completed."):
                self.category = TimelineCategory.MissionCountdown
            elif "overtime" in self.event:
                self.category |= TimelineCategory.Overtime
            elif "sync" in self.event:
                return
            else:
                self.category = TimelineCategory.GameEnd
            return

        if self.event.endswith(" enabled."):
            self.mission = MISSION_GENERIC_TIMELINE_TO_ENUM[
                self.event[: -len(" enabled.")]
            ]
            self.category = TimelineCategory.MissionEnabled
            return

        if self.event.endswith(" selected."):
            self.mission = MISSION_GENERIC_TIMELINE_TO_ENUM[
                self.event[: -len(" selected.")]
            ]
            self.category = TimelineCategory.MissionSelected
            return

        if self.event.endswith(" pending."):
            self.mission = MISSION_GENERIC_TIMELINE_TO_ENUM[
                self.event[: -len(" pending.")]
            ]
            if self.mission == Missions.Swap:
                self.category |= TimelineCategory.Statues

            return

        if self.event == "character picked up pending statue.":
            self.category |= TimelineCategory.Statues
            self.mission = Missions.Swap

        if self.event.endswith(" aborted."):
            self.mission = MISSION_GENERIC_TIMELINE_TO_ENUM[
                self.event[: -len(" aborted.")]
            ]

            return

        if "flirt" in self.event or "seduc" in self.event:
            self.mission = Missions.Seduce

            if self.event.endswith("%"):
                self.category = TimelineCategory.MissionPartial
            elif "expired" in self.event:
                self.category = TimelineCategory.NoCategory

        if "bug" in self.event:
            self.mission = Missions.Bug

        if "purloin" in self.event or "guest list" in self.event:
            self.mission = Missions.Purloin
            self.category |= TimelineCategory.Drinks
            if self.event.startswith("delegated purloin to "):
                # assume there will be a single a character here, use that for the name
                self.event = "delegated purloin to {}.".format(
                    CHARACTERS_TO_STRING[self.cast_name[0]].lower()
                )

        if "fingerprint" in self.event:
            self.mission = Missions.Fingerprint

        if "45 seconds" in self.event:
            self.category |= TimelineCategory.TimeAdd

        if "banana bread" in self.event:
            self.mission = Missions.Contact
            self.category |= TimelineCategory.BananaBread

        if self.event.startswith("action"):
            if self.event.startswith("action test"):
                self.category = TimelineCategory.ActionTest
                self.action_test = assign_color(self.event)
                if "watch" in self.event:
                    self.category |= TimelineCategory.TimeAdd

            if self.event.startswith("action triggered:"):
                self.category = TimelineCategory.ActionTriggered

            self.mission = MISSION_GENERIC_TIMELINE_TO_ENUM[
                self.event.split(":")[1].strip()
            ]

        if self.event in MISSION_COMPLETE_TIMELINE_TO_ENUM.keys():
            self.category = TimelineCategory.MissionComplete
            self.mission = MISSION_COMPLETE_TIMELINE_TO_ENUM[self.event]

        if self.event in MISSION_PARTIAL_TO_ENUM.keys():
            self.category = TimelineCategory.MissionPartial
            self.mission = MISSION_PARTIAL_TO_ENUM[self.event]

        if self.actor == "sniper" and self.event.startswith("marked"):
            self.category |= TimelineCategory.SniperLights

        # Assign Objects
        if "watch" in self.event:
            self.category |= TimelineCategory.Watch
            if "to add time" in self.event:
                self.category |= TimelineCategory.TimeAdd

        if (
            "conversation" in self.event
            or "talking" in self.event
            or ("interrupted" in self.event and "inspect" not in self.event)
        ):
            self.category |= TimelineCategory.Conversation

        if "briefcase" in self.event:
            self.category |= TimelineCategory.Briefcase

        if "statue" in self.event:
            self.category |= TimelineCategory.Statues
            if (
                self.event.startswith("left")
                or self.event.startswith("held")
                or self.event.startswith("right")
            ):
                self.category |= TimelineCategory.MissionPartial

        if "inspect" in self.event:
            self.mission = Missions.Inspect

        if "book" in self.event or "microfilm" in self.event:
            self.category |= TimelineCategory.Books

        if "drink" in self.event or "waiter" in self.event or "bartender" in self.event:
            self.category |= TimelineCategory.Drinks

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.actor:<7} {self.time} {self.event}"

    def __hash__(self):
        return hash(
            (
                self.actor,
                self.time,
                self.event,
                self.cast_name,
                self.books,
                self.role,
                self.category,
                self.mission,
                self.action_test,
            )
        )

    def __eq__(self, other):
        return (
            self.actor,
            self.time,
            self.event,
            self.cast_name,
            self.books,
            self.role,
            self.category,
            self.mission,
            self.action_test,
        ) == (
            other.actor,
            other.time,
            other.event,
            other.cast_name,
            other.books,
            other.role,
            other.category,
            other.mission,
            other.action_test,
        )


class Timeline(Sequence):
    def __init__(self, lines: List[TimelineEvent]):
        self.lines = lines

        super().__init__()

    def __getitem__(self, i):
        return self.lines[i]

    def __len__(self):
        return len(self.lines)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n".join(str(line) for line in self.lines)

    def get_next_spy_action(self, event: TimelineEvent) -> Optional[TimelineEvent]:
        start_found = False

        for possible in self.lines:
            if start_found:
                if possible.actor == "spy":
                    return possible
            else:
                if possible == event:
                    start_found = True

        return None

    def calculate_elapsed_times(self):
        num_time_adds = 0
        start_time = self.lines[0].time

        for line in self.lines:
            line.elapsed_time = start_time - (line.time - (45 * num_time_adds))

            if line.category == TimelineCategory.TimeAdd and line.event.startswith(
                "45 seconds"
            ):
                num_time_adds += 1
