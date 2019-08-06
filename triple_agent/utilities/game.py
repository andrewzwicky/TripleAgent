import os
import pickle
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from triple_agent.utilities.missions import Missions
from triple_agent.utilities.outcomes import WinType
from triple_agent.utilities.roles import Roles
from triple_agent.utilities.timeline import TimelineCategory, Timeline
from triple_agent.utilities.paths import REPLAY_PICKLE_FOLDER


@dataclass
class Game:
    spy: str
    sniper: str
    venue: str
    win_type: WinType
    game_type: str
    # picked missions are for pick mode
    # this is 'enabled' in replay
    picked_missions: Missions
    selected_missions: Missions
    completed_missions: Missions
    start_time: datetime
    uuid: str
    file: str
    guest_count: Optional[int] = None
    start_clock_seconds: Optional[int] = None
    duration: Optional[int] = None
    event: Optional[str] = field(default=None, init=False)
    division: Optional[str] = field(default=None, init=False)
    week: Optional[str] = field(default=None, init=False)
    initial_pickle: bool = True
    winner: str = field(init=False)
    timeline: Optional[Timeline] = field(default=None, init=False)

    def __post_init__(self):
        self.spy = self.spy if not self.spy.endswith("/steam") else self.spy[:-6]
        self.sniper = (
            self.sniper if not self.sniper.endswith("/steam") else self.sniper[:-6]
        )
        self.winner = self.spy if self.win_type & WinType.SpyWin else self.sniper

        if self.initial_pickle:
            self.repickle()

    def repickle(self):
        with open(get_game_expected_pkl(self.uuid), "wb") as pik:
            pickle.dump(self, pik)

    def collect_general_timeline_info(self):
        timeline_picked_missions = Missions.Zero
        timeline_selected_missions = Missions.Zero
        timeline_completed_missions = Missions.Zero
        timeline_guest_count = 0
        ending_included = False

        for event in self.timeline:
            if event.category & TimelineCategory.MissionEnabled:
                timeline_picked_missions |= event.mission

            if event.category & TimelineCategory.MissionSelected:
                timeline_selected_missions |= event.mission

            if event.category & TimelineCategory.MissionComplete:
                timeline_completed_missions |= event.mission

            if event.category & TimelineCategory.Cast:
                timeline_guest_count += 1

            if event.category & TimelineCategory.GameEnd:
                ending_included = True

        return (
            timeline_picked_missions,
            timeline_selected_missions,
            timeline_completed_missions,
            timeline_guest_count,
            ending_included,
        )

    def check_time_adds(self, coherent, coherent_reasons):
        previous_time = None
        previous_timeadd = False

        for event in self.timeline:
            if previous_time is not None:
                if event.time > previous_time and not previous_timeadd:
                    coherent = False
                    coherent_reasons.append("TIME REWIND WITHOUT TIMEADD")

            previous_time = event.time

            previous_timeadd = event.event == "45 seconds added to match."

        return coherent

    def check_book_colors(self, coherent, coherent_reasons):
        for event in self.timeline:
            if len(event.books) > 1:
                for book in event.books:
                    if book is None:
                        coherent = False
                        coherent_reasons.append("BOOK MISSING COLOR")

        return coherent

    def is_timeline_coherent(self):
        coherent = True
        coherent_reasons = []

        if self.timeline is None:
            coherent_reasons.append("NO TIMELINE")
            coherent = False
            return coherent, ", ".join(coherent_reasons)

        timeline_picked_missions, timeline_selected_missions, timeline_completed_missions, timeline_guest_count, ending_included = (
            self.collect_general_timeline_info()
        )

        if not ending_included:
            coherent = False
            coherent_reasons.append("NO GAME ENDING")

        coherent = self.check_time_adds(coherent, coherent_reasons)

        coherent = self.check_book_colors(coherent, coherent_reasons)

        coherent = self.check_start_clock(coherent, coherent_reasons)

        coherent = self.check_picked_missions(
            coherent, coherent_reasons, timeline_picked_missions
        )

        coherent = self.check_completed_missions(
            coherent, coherent_reasons, timeline_completed_missions
        )

        coherent = self.check_selected_missions(
            coherent, coherent_reasons, timeline_selected_missions
        )

        coherent = self.check_guest_count(
            coherent, coherent_reasons, timeline_guest_count
        )

        # TODO: figure out why I added this
        if len(self.timeline[0].role) != 1:
            coherent = False

        coherent = self.check_spy_in_beginning(coherent, coherent_reasons)

        return coherent, ", ".join(coherent_reasons)

    def check_spy_in_beginning(self, coherent, coherent_reasons):
        # It's possible for sniper lights to appear as the first thing in the timeline,
        # so check the first two items in the timeline
        if self.timeline[0].role == tuple or self.timeline[0].role[0] != Roles.Spy:
            if self.timeline[1].role == tuple or self.timeline[1].role[0] != Roles.Spy:
                if (
                    self.timeline[2].role == tuple
                    or self.timeline[2].role[0] != Roles.Spy
                ):
                    coherent = False
                    coherent_reasons.append(
                        "SPY CAST NOT IN FIRST THREE TIMELINE ITEMS"
                    )
        return coherent

    def check_guest_count(self, coherent, coherent_reasons, timeline_guest_count):
        if timeline_guest_count != self.guest_count and self.guest_count is not None:
            coherent_reasons.append(
                "GUEST COUNT MISMATCH {} != {}".format(
                    timeline_guest_count, self.guest_count
                )
            )
            coherent = False
        return coherent

    def check_selected_missions(
        self, coherent, coherent_reasons, timeline_selected_missions
    ):
        if timeline_selected_missions != self.selected_missions:
            coherent_reasons.append(
                "SELECTED MISSIONS MISMATCH {} != {}".format(
                    timeline_selected_missions, self.selected_missions
                )
            )
            coherent = False
        return coherent

    def check_completed_missions(
        self, coherent, coherent_reasons, timeline_completed_missions
    ):
        if timeline_completed_missions != self.completed_missions:
            coherent_reasons.append(
                "COMPLETED MISSIONS MISMATCH {} != {}".format(
                    timeline_completed_missions, self.completed_missions
                )
            )
            coherent = False
        return coherent

    def check_picked_missions(
        self, coherent, coherent_reasons, timeline_picked_missions
    ):
        if timeline_picked_missions != self.picked_missions:
            coherent_reasons.append(
                "PICKED MISSIONS MISMATCH {} != {}".format(
                    timeline_picked_missions, self.picked_missions
                )
            )
            coherent = False
        return coherent

    def check_start_clock(self, coherent, coherent_reasons):
        if (
            self.timeline[0].time != self.start_clock_seconds
            and self.start_clock_seconds is not None
        ):
            coherent_reasons.append(
                "START CLOCK MISMATCH {} != {}".format(
                    self.timeline[0].time, self.start_clock_seconds
                )
            )
            coherent = False
        return coherent

    def __repr__(self):
        # TODO: this should contain more information
        return (
            f"{self.spy} vs {self.sniper} on {self.venue} | {self.winner} wins | "
            f"{str(self.win_type)} | {str(self.completed_missions)}"
        )


def game_unpickle(expected_file: str) -> Optional[Game]:
    if os.path.exists(expected_file):
        with open(expected_file, "rb") as pik:
            return pickle.load(pik)

    return None


def game_load_or_new(*args, **kwargs) -> Game:
    expected_file = get_game_expected_pkl(kwargs["uuid"])
    unpickled_game = game_unpickle(expected_file)

    if unpickled_game is not None:
        return unpickled_game

    return Game(*args, **kwargs)


def get_game_expected_pkl(uuid: str) -> str:
    return os.path.join(REPLAY_PICKLE_FOLDER, f"{uuid}.pkl")
