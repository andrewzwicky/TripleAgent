import pickle
from datetime import datetime
from typing import Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import jsonpickle.handlers

from triple_agent.classes.missions import Missions
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.venues import Venue
from triple_agent.classes.roles import Roles
from triple_agent.classes.timeline import TimelineCategory, TimelineCoherency, Timeline
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER, JSON_GAMES_FOLDER

jsonpickle.set_encoder_options("simplejson", sort_keys=True, indent=4)
jsonpickle.set_preferred_backend("simplejson")


@dataclass
# pylint: disable=too-many-instance-attributes
class Game:
    spy: str
    sniper: str
    spy_username: str
    sniper_username: str
    venue: Venue
    win_type: WinType
    game_type: str
    picked_missions: Missions
    selected_missions: Missions
    completed_missions: Missions
    # UTC timestamp
    start_time: datetime
    uuid: str
    duration: int
    file: Path
    guest_count: Optional[int] = None
    start_clock_seconds: Optional[int] = None
    event: Optional[str] = None
    division: Optional[str] = None
    week: Optional[str] = None
    timeline: Timeline = Timeline([])
    winner: str = field(init=False)

    def __post_init__(self):
        self.winner = self.spy if self.win_type & WinType.SpyWin else self.sniper

    def pickle(self, pickle_folder: Path):
        with open(get_game_expected_pkl(self.uuid, pickle_folder), "wb") as pik:
            pickle.dump(self, pik)

    def collect_general_timeline_info(
        self,
    ) -> Tuple[Missions, Missions, Missions, int, bool, bool]:
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

            # In older replays, the missions selected and enabled are at the front of the cast selection.
            if event.category not in (
                TimelineCategory.SniperLights,
                TimelineCategory.MissionEnabled,
                TimelineCategory.MissionSelected,
            ):
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
        self, coherency: TimelineCoherency, timeline_selected_missions: Missions
    ) -> TimelineCoherency:
        if timeline_selected_missions != self.selected_missions:
            coherency |= TimelineCoherency.SelectedMissionsMismatch
        return coherency

    def check_completed_missions(
        self, coherency: TimelineCoherency, timeline_completed_missions: Missions
    ) -> TimelineCoherency:
        if timeline_completed_missions != self.completed_missions:
            coherency |= TimelineCoherency.CompletedMissionsMismatch
        return coherency

    def check_picked_missions(
        self, coherency: TimelineCoherency, timeline_picked_missions: Missions
    ) -> TimelineCoherency:
        if timeline_picked_missions != self.picked_missions:
            coherency |= TimelineCoherency.PickedMissionsMismatch
        return coherency

    def check_start_clock(self, coherency: TimelineCoherency) -> TimelineCoherency:
        assert len(self.timeline) >= 1

        if (
            self.timeline[0].time != self.start_clock_seconds
            and self.start_clock_seconds is not None
        ):
            coherency |= TimelineCoherency.StartClockMismatch

        return coherency

    def serialize_to_json(self, json_folder: Path):
        json_game = jsonpickle.encode(self, unpicklable=True)
        with open(get_game_expected_json(self.uuid, json_folder), "w") as json_out:
            json_out.write(json_game)

    def add_start_clock_seconds(self):
        if self.start_clock_seconds is None:
            self.start_clock_seconds = int(self.timeline[0].time)

    def __eq__(self, other: Any) -> bool:
        if self.__class__ is other.__class__:
            return (
                self.spy,
                self.sniper,
                self.spy_username,
                self.sniper_username,
                self.venue,
                self.win_type,
                self.game_type,
                self.picked_missions,
                self.selected_missions,
                self.completed_missions,
                self.start_time,
                self.guest_count,
                self.start_clock_seconds,
                self.duration,
                self.uuid,
                self.event,
                self.division,
                self.week,
                self.timeline,
                self.winner,
            ) == (
                other.spy,
                other.sniper,
                other.spy_username,
                other.sniper_username,
                other.venue,
                other.win_type,
                other.game_type,
                other.picked_missions,
                other.selected_missions,
                other.completed_missions,
                other.start_time,
                other.guest_count,
                other.start_clock_seconds,
                other.duration,
                other.uuid,
                other.event,
                other.division,
                other.week,
                other.timeline,
                other.winner,
            )

        return NotImplemented


@jsonpickle.handlers.register(Game, base=True)
class GameHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj: Game, data: dict) -> dict:
        assert isinstance(obj, Game)
        data["spy"] = obj.spy
        data["sniper"] = obj.sniper
        data["spy_username"] = obj.spy_username
        data["sniper_username"] = obj.sniper_username
        data["venue"] = obj.venue.stringify()
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
        data["event"] = obj.event
        data["division"] = obj.division
        data["week"] = obj.week
        data["timeline"] = (
            obj.timeline.serialize() if obj.timeline is not None else None
        )
        data["winner"] = obj.winner

        return data

    # this method is never used because the JSON are only output, never re-parsed into games
    def restore(self, obj: Any):  # pragma: no cover
        raise NotImplementedError


def insert_alias_name(game: Game, alias_list: dict) -> Game:
    if game.spy_username in alias_list.keys():
        game.spy = alias_list[game.spy_username]

    if game.sniper_username in alias_list.keys():
        game.sniper = alias_list[game.sniper_username]

    return game


def game_unpickle(
    expected_file: Path, alias_list: Optional[dict] = None
) -> Optional[Game]:
    if expected_file.exists():
        with open(expected_file, "rb") as pik:
            game = pickle.load(pik)

            if alias_list is not None:
                game = insert_alias_name(game, alias_list)

            return game

    return None


def game_load_or_new(
    replay_dict: dict,
    replay_file: Optional[Path] = None,
    pickle_folder: Path = REPLAY_PICKLE_FOLDER,
    **kwargs,
) -> Game:
    expected_file = get_game_expected_pkl(replay_dict["uuid"], pickle_folder)
    unpickled_game = game_unpickle(expected_file)

    if unpickled_game is not None:
        return unpickled_game

    if replay_file is None:
        raise ValueError("Pickled game not found and no replay file supplied")

    return create_game_from_replay_info(
        replay_dict, replay_file, pickle_folder=pickle_folder, **kwargs
    )


def get_game_expected_pkl(
    uuid: str, pickle_folder: Path = REPLAY_PICKLE_FOLDER
) -> Path:
    return pickle_folder.joinpath(f"{uuid}.pkl")


def get_game_expected_json(uuid: str, json_folder: Path = JSON_GAMES_FOLDER) -> Path:
    return json_folder.joinpath(f"{uuid}.json")


def create_game_from_replay_info(
    replay_dict: dict,
    replay_file: Path,
    pickle_folder: Path = REPLAY_PICKLE_FOLDER,
    **kwargs,
) -> Game:
    # this method only exists to fix lint errors from repeated lines
    return Game(
        replay_dict["spy_displayname"],
        replay_dict["sniper_displayname"],
        replay_dict["spy_username"],
        replay_dict["sniper_username"],
        replay_dict["level"],
        replay_dict["result"],
        replay_dict["game_type"],
        replay_dict["picked_missions"],
        replay_dict["selected_missions"],
        replay_dict["completed_missions"],
        replay_dict["start_time"],
        replay_dict["uuid"],
        replay_dict["duration"],
        replay_file,
        guest_count=replay_dict["guest_count"],
        start_clock_seconds=replay_dict["start_clock_seconds"],
        **kwargs,
    )
