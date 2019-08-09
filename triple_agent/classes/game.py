import os
import pickle
from datetime import datetime
from typing import Set, Optional, Tuple

from triple_agent.classes.missions import convert_mission_set_to_enum, Missions
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.roles import Roles
from triple_agent.classes.timeline import TimelineCategory, TimelineCoherency
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER


class Game:
    def __init__(
        self,
        spy: str,
        sniper: str,
        venue: str,
        win_type: str,
        game_type: str,
        picked_missions: Set[str],
        selected_missions: Set[str],
        completed_missions: Set[str],
        start_time: datetime = None,
        guest_count: Optional[int] = None,
        start_clock_seconds: Optional[int] = None,
        duration: Optional[int] = None,
        uuid: str = None,
        file: str = None,
        event: str = None,
        division: str = None,
        week: str = None,
        initial_pickle=True,
        pickle_folder=REPLAY_PICKLE_FOLDER,
    ):
        self.spy = spy if not spy.endswith("/steam") else spy[:-6]
        self.sniper = sniper if not sniper.endswith("/steam") else sniper[:-6]
        self.venue = venue
        self.win_type = WinType[win_type]
        self.game_type = game_type
        self.winner = self.spy if self.win_type & WinType.SpyWin else self.sniper
        # picked missions are for pick mode
        # this is 'enabled' in replay
        self.picked_missions = convert_mission_set_to_enum(picked_missions)
        self.selected_missions = convert_mission_set_to_enum(selected_missions)
        self.completed_missions = convert_mission_set_to_enum(completed_missions)
        self.start_time = start_time
        self.guest_count = guest_count
        self.start_clock_seconds = start_clock_seconds
        self.duration = duration
        self.uuid = uuid
        self.event = event
        self.division = division
        self.week = week
        self.file = file
        self.timeline = None
        if initial_pickle:
            self.repickle(pickle_folder=pickle_folder)

    def repickle(self, pickle_folder: str = REPLAY_PICKLE_FOLDER):
        with open(get_game_expected_pkl(self.uuid, pickle_folder), "wb") as pik:
            pickle.dump(self, pik)

    def is_timeline_coherent(self) -> TimelineCoherency:
        coherency = TimelineCoherency.Coherent

        timeline_picked_missions = Missions.Zero
        timeline_selected_missions = Missions.Zero
        timeline_completed_missions = Missions.Zero
        timeline_guest_count = 0
        timeline_time_adds = 0
        previous_time = None
        previous_timeadd = False
        ending_included = False
        start_included = False

        if self.timeline is None:
            return TimelineCoherency.NoTimeline

        for event in self.timeline:
            if event.category & TimelineCategory.MissionEnabled:
                timeline_picked_missions |= event.mission

            if event.category & TimelineCategory.MissionSelected:
                timeline_selected_missions |= event.mission

            if event.category & TimelineCategory.MissionComplete:
                timeline_completed_missions |= event.mission

            if event.category & TimelineCategory.Cast:
                timeline_guest_count += 1

            if previous_time is not None:
                if event.time > previous_time and not previous_timeadd:
                    coherency |= TimelineCoherency.TimeRewind

            previous_time = event.time

            if event.event == "45 seconds added to match.":
                timeline_time_adds += 1
                previous_timeadd = True
            else:
                previous_timeadd = False

            if len(event.books) > 1:
                for book in event.books:
                    if book is None:
                        coherency |= TimelineCoherency.BookMissingColor

            if event.category & TimelineCategory.GameEnd:
                ending_included = True

            if event.category & TimelineCategory.GameStart:
                start_included = True

        if not ending_included:
            coherency |= TimelineCoherency.NoGameEnding

        if not start_included:
            coherency |= TimelineCoherency.NoGameStart

        if (
            self.timeline[0].time != self.start_clock_seconds
            and self.start_clock_seconds is not None
        ):
            coherency |= TimelineCoherency.StartClockMismatch

        if timeline_picked_missions != self.picked_missions:
            coherency |= TimelineCoherency.PickedMissionsMismatch

        if timeline_completed_missions != self.completed_missions:
            coherency |= TimelineCoherency.CompletedMissionsMismatch

        if timeline_selected_missions != self.selected_missions:
            coherency |= TimelineCoherency.SelectedMissionsMismatch

        if timeline_guest_count != self.guest_count and self.guest_count is not None:
            coherency |= TimelineCoherency.GuestCountMismatch

        # TODO: unsure what this was checking for.
        # if len(self.timeline[0].role) != 1:
        #     coherent = False

        # It's possible for sniper lights to appear as the first thing in the timeline,
        # so check the first two items in the timeline
        if self.timeline[0].role == tuple or self.timeline[0].role[0] != Roles.Spy:
            if self.timeline[1].role == tuple or self.timeline[1].role[0] != Roles.Spy:
                if (
                    self.timeline[2].role == tuple
                    or self.timeline[2].role[0] != Roles.Spy
                ):
                    coherency |= TimelineCoherency.SpyNotCastInBeginning

        return coherency

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


def game_load_or_new(
    *args, pickle_folder: str = REPLAY_PICKLE_FOLDER, **kwargs
) -> Game:
    expected_file = get_game_expected_pkl(kwargs["uuid"], pickle_folder)
    unpickled_game = game_unpickle(expected_file)

    if unpickled_game is not None:
        return unpickled_game

    return Game(*args, pickle_folder=pickle_folder, **kwargs)


def get_game_expected_pkl(uuid: str, pickle_folder: str = REPLAY_PICKLE_FOLDER) -> str:
    return os.path.join(pickle_folder, f"{uuid}.pkl")
