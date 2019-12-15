import os
import pickle
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
import jsonpickle.handlers

from triple_agent.classes.missions import Missions
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.roles import Roles
from triple_agent.classes.timeline import TimelineCategory, TimelineCoherency, Timeline
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER


@dataclass
# pylint: disable=too-many-instance-attributes
class Game:
    spy: str
    sniper: str
    spy_username: str
    sniper_username: str
    venue: str
    win_type: WinType
    game_type: str
    picked_missions: Missions
    selected_missions: Missions
    completed_missions: Missions
    # UTC timestamp
    start_time: datetime = None
    guest_count: Optional[int] = None
    start_clock_seconds: Optional[int] = None
    duration: Optional[int] = None
    uuid: str = None
    file: str = None
    event: str = None
    division: str = None
    week: str = None
    initial_pickle: bool = True
    pickle_folder: str = REPLAY_PICKLE_FOLDER
    timeline: Optional[Timeline] = None
    winner: str = field(init=False)

    def __post_init__(self):
        self.spy = self.spy if not self.spy.endswith("/steam") else self.spy[:-6]
        self.sniper = (
            self.sniper if not self.sniper.endswith("/steam") else self.sniper[:-6]
        )
        self.winner = self.spy if self.win_type & WinType.SpyWin else self.sniper
        if self.initial_pickle:
            self.repickle(pickle_folder=self.pickle_folder)

    def repickle(self, pickle_folder: str = REPLAY_PICKLE_FOLDER):
        with open(get_game_expected_pkl(self.uuid, pickle_folder), "wb") as pik:
            pickle.dump(self, pik)

    def collect_general_timeline_info(self):
        timeline_picked_missions = Missions.NoMission
        timeline_selected_missions = Missions.NoMission
        timeline_completed_missions = Missions.NoMission
        timeline_guest_count = 0
        ending_included = False
        start_included = False

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

            if event.category & TimelineCategory.GameStart:
                start_included = True

        return (
            timeline_picked_missions,
            timeline_selected_missions,
            timeline_completed_missions,
            timeline_guest_count,
            ending_included,
            start_included,
        )

    def check_time_adds(self, coherency: TimelineCoherency) -> TimelineCoherency:
        previous_time = None
        previous_timeadd = False

        for event in self.timeline:
            if previous_time is not None:
                if event.time > previous_time and not previous_timeadd:
                    coherency |= TimelineCoherency.TimeRewind

            previous_time = event.time

            previous_timeadd = event.event == "45 seconds added to match."

        return coherency

    def check_book_colors(self, coherency: TimelineCoherency) -> TimelineCoherency:
        for event in self.timeline:
            if len(event.books) > 1:
                for book in event.books:
                    if book is None:
                        coherency |= TimelineCoherency.BookMissingColor

        return coherency

    def check_role_character_match(
        self, coherency: TimelineCoherency
    ) -> TimelineCoherency:
        for event in self.timeline:
            if None in event.role and event.cast_name != (None,):
                coherency |= TimelineCoherency.CharacterNotAssignedRole

            if None in event.cast_name and event.role != (None,):
                coherency |= TimelineCoherency.RoleWithNoCharacter

        return coherency

    def is_timeline_coherent(self) -> TimelineCoherency:
        coherency = TimelineCoherency.Coherent

        if self.timeline is None:
            return TimelineCoherency.NoTimeline

        (
            timeline_picked_missions,
            timeline_selected_missions,
            timeline_completed_missions,
            timeline_guest_count,
            ending_included,
            start_included,
        ) = self.collect_general_timeline_info()

        if not ending_included:
            coherency |= TimelineCoherency.NoGameEnding

        if not start_included:
            coherency |= TimelineCoherency.NoGameStart

        coherency = self.check_time_adds(coherency)

        coherency = self.check_book_colors(coherency)

        coherency = self.check_start_clock(coherency)

        coherency = self.check_picked_missions(coherency, timeline_picked_missions)

        coherency = self.check_completed_missions(
            coherency, timeline_completed_missions
        )

        coherency = self.check_selected_missions(coherency, timeline_selected_missions)

        coherency = self.check_guest_count(coherency, timeline_guest_count)

        coherency = self.check_role_character_match(coherency)

        # TODO: figure out why I added this
        # if len(self.timeline[0].role) != 1:
        #     coherent = False

        coherency = self.check_spy_in_beginning(coherency)

        return coherency

    def check_spy_in_beginning(self, coherency: TimelineCoherency) -> TimelineCoherency:
        # It's possible for sniper lights to appear as up to the first 4! things in the timeline
        for event in self.timeline:
            if isinstance(event.role, tuple) and event.role[0] == Roles.Spy:
                break

            if event.category != TimelineCategory.SniperLights:
                coherency |= TimelineCoherency.SpyNotCastInBeginning
                break

        return coherency

    def check_guest_count(
        self, coherency: TimelineCoherency, timeline_guest_count: int
    ) -> TimelineCoherency:
        if timeline_guest_count != self.guest_count and self.guest_count is not None:
            coherency |= TimelineCoherency.GuestCountMismatch
        return coherency

    def check_selected_missions(
        self, coherency: TimelineCoherency, timeline_selected_missions
    ) -> TimelineCoherency:
        if timeline_selected_missions != self.selected_missions:
            coherency |= TimelineCoherency.SelectedMissionsMismatch
        return coherency

    def check_completed_missions(
        self, coherency: TimelineCoherency, timeline_completed_missions
    ) -> TimelineCoherency:
        if timeline_completed_missions != self.completed_missions:
            coherency |= TimelineCoherency.CompletedMissionsMismatch
        return coherency

    def check_picked_missions(
        self, coherency: TimelineCoherency, timeline_picked_missions
    ) -> TimelineCoherency:
        if timeline_picked_missions != self.picked_missions:
            coherency |= TimelineCoherency.PickedMissionsMismatch
        return coherency

    def check_start_clock(self, coherency: TimelineCoherency):
        if (
            self.timeline[0].time != self.start_clock_seconds
            and self.start_clock_seconds is not None
        ):
            coherency |= TimelineCoherency.StartClockMismatch

        return coherency

    def serialize(self):
        print(jsonpickle.encode(self, unpicklable=False))


@jsonpickle.handlers.register(Game, base=True)
class GameHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj: Game, data: dict):
        assert isinstance(obj, Game)
        data["spy"] = obj.spy
        data["sniper"] = obj.sniper
        data["venue"] = obj.venue
        data["win_type"] = obj.win_type.serialize()
        data["game_type"] = obj.game_type
        data["picked_missions"] = obj.picked_missions.serialize()
        data["selected_missions"] = obj.selected_missions.serialize()
        data["completed_missions"] = obj.completed_missions.serialize()
        data["start_time"] = obj.start_time.isoformat()
        data["guest_count"] = obj.guest_count
        data["start_clock_seconds"] = obj.start_clock_seconds
        data["duration"] = obj.duration
        data["uuid"] = obj.uuid
        # data['file']= str = None
        data["event"] = obj.event
        data["division"] = obj.division
        data["week"] = obj.week
        # data['initial_pickle']= bool = True
        # data['pickle_folder']= str = REPLAY_PICKLE_FOLDER
        data["timeline"] = obj.timeline.serialize()
        data["winner"] = obj.winner

        return data

    def restore(self, obj):
        pass


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
