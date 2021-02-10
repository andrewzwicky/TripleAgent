import pytest
import numpy as np
from triple_agent.classes.game import Game
from typing import List, Iterator, Tuple
import cv2
import time
from pathlib import Path

from triple_agent.parsing.timeline.parse_full_timeline import (
    parse_full_timeline,
)
from triple_agent.parsing.replay.parse_replays import parse_replays
from triple_agent.classes.characters import Characters
from triple_agent.classes.roles import Roles
from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.classes.books import Books
from triple_agent.tests.test_mock_screenshot_iterator import mock_screenshot_iterator
import random

TEST_FOLDER = Path(__file__).resolve().parent


@pytest.mark.parsing
def test_parse_exception_timeline(get_unparsed_test_games, tmp_path, monkeypatch):
    games = get_unparsed_test_games
    games[0].uuid = games[0].uuid + "_exception"

    monkeypatch.setattr("builtins.input", lambda x: None)
    monkeypatch.setattr(time, "sleep", lambda x: None)

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_exception.pkl").exists()

    parse_full_timeline(
        [games[0]],
        mock_screenshot_iterator,
        tmp_path,
        tmp_path,
    )

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_exception.pkl").exists()


@pytest.mark.parsing
def test_parse_incoherent_timeline(get_unparsed_test_games, tmp_path, monkeypatch):
    games = get_unparsed_test_games
    games[0].uuid = games[0].uuid + "_incoherent"

    monkeypatch.setattr("builtins.input", lambda x: None)
    monkeypatch.setattr(time, "sleep", lambda x: None)

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_incoherent.pkl").exists()

    parse_full_timeline(
        [games[0]],
        mock_screenshot_iterator,
        tmp_path,
        tmp_path,
    )

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_incoherent.pkl").exists()


@pytest.mark.parsing
def test_parse_not_matching_timeline(get_unparsed_test_games, tmp_path, monkeypatch):
    games = get_unparsed_test_games
    games[0].uuid = games[0].uuid + "_unmatched"

    monkeypatch.setattr("builtins.input", lambda x: None)
    monkeypatch.setattr(time, "sleep", lambda x: None)

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_unmatched.pkl").exists()

    parse_full_timeline(
        [games[0]],
        mock_screenshot_iterator,
        tmp_path,
        tmp_path,
    )

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_unmatched.pkl").exists()


@pytest.mark.parsing
def test_parse_odd_ss_timeline(get_unparsed_test_games, tmp_path, monkeypatch):
    games = get_unparsed_test_games
    games[0].uuid = games[0].uuid + "_odd"

    monkeypatch.setattr("builtins.input", lambda x: None)
    monkeypatch.setattr(time, "sleep", lambda x: None)

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_odd.pkl").exists()

    parse_full_timeline(
        [games[0]],
        mock_screenshot_iterator,
        tmp_path,
        tmp_path,
    )

    assert not tmp_path.joinpath("OiG7qvC9QOaSKVGlesdpWQ_odd.pkl").exists()


@pytest.mark.parsing
def test_parse_timeline_normal(
    tmp_path,
    get_test_events_folder,
    get_test_unparsed_folder,
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda x: None)
    monkeypatch.setattr(time, "sleep", lambda x: None)

    relevant_uuids = [
        "OiG7qvC9QOaSKVGlesdpWQ",
        "8uf6pUK7TFegBD8Cbr2qMw",
        "TPWiwN2aQc6EHEf6jKDKaA",
        "as-RnR1RQruzhRDZr7JP9A",
        "jhx6e7UpTmeKueggeGcAKg",
        "k415gCwtS3ml9_EzUPpWFw",
        "k8x3n_zfTtiw9FSS6rM13w",
        "lOGf7W_MSlu1RRYxW2MMsA",
        "vgAlD77AQw2XKTZq3H4NTg",
    ]

    relevant_pkl_files = [tmp_path.joinpath(f"{u}.pkl") for u in relevant_uuids]
    for pkl_file in relevant_pkl_files:
        assert not pkl_file.exists()

    games = parse_replays(
        lambda game: game.division == "Copper" and game.uuid in relevant_uuids,
        unparsed_folder=get_test_unparsed_folder,
        events_folder=get_test_events_folder,
        pickle_folder=tmp_path,
        screenshot_iterator=mock_screenshot_iterator,
        json_folder=tmp_path,
    )

    for pkl_file in relevant_pkl_files:
        assert pkl_file.exists()

    games.sort(key=lambda g: g.start_time)

    assert len(games[0].timeline) == 119
    assert len(games[1].timeline) == 74
    assert len(games[2].timeline) == 136
    assert len(games[3].timeline) == 129
    assert len(games[4].timeline) == 49
    assert len(games[5].timeline) == 56
    assert len(games[6].timeline) == 76
    assert len(games[7].timeline) == 85
    assert len(games[8].timeline) == 112

    assert games[0].uuid == "OiG7qvC9QOaSKVGlesdpWQ"
    assert games[0].timeline[0].action_test == ActionTest.NoAT
    assert games[0].timeline[0].actor == "spy"
    assert games[0].timeline[0].books == (None,)
    assert games[0].timeline[0].cast_name == (Characters.Irish,)
    assert games[0].timeline[0].category == TimelineCategory.Cast
    assert games[0].timeline[0].elapsed_time == 0.0
    assert games[0].timeline[0].event == "spy cast."
    assert games[0].timeline[0].mission == Missions.NoMission
    assert games[0].timeline[0].role == (Roles.Spy,)
    assert games[0].timeline[0].time == 225.0

    assert games[0].timeline[1].action_test == ActionTest.NoAT
    assert games[0].timeline[1].actor == "spy"
    assert games[0].timeline[1].books == (None,)
    assert games[0].timeline[1].cast_name == (Characters.Carlos,)
    assert games[0].timeline[1].category == TimelineCategory.Cast
    assert games[0].timeline[1].elapsed_time == 0.0
    assert games[0].timeline[1].event == "ambassador cast."
    assert games[0].timeline[1].mission == Missions.NoMission
    assert games[0].timeline[1].role == (Roles.Ambassador,)
    assert games[0].timeline[1].time == 225.0

    assert games[0].timeline[2].action_test == ActionTest.NoAT
    assert games[0].timeline[2].actor == "spy"
    assert games[0].timeline[2].books == (None,)
    assert games[0].timeline[2].cast_name == (Characters.Boots,)
    assert games[0].timeline[2].category == TimelineCategory.Cast
    assert games[0].timeline[2].elapsed_time == 0.0
    assert games[0].timeline[2].event == "double agent cast."
    assert games[0].timeline[2].mission == Missions.NoMission
    assert games[0].timeline[2].role == (Roles.DoubleAgent,)
    assert games[0].timeline[2].time == 225.0

    assert games[0].timeline[3].action_test == ActionTest.NoAT
    assert games[0].timeline[3].actor == "spy"
    assert games[0].timeline[3].books == (None,)
    assert games[0].timeline[3].cast_name == (Characters.Wheels,)
    assert games[0].timeline[3].category == TimelineCategory.Cast
    assert games[0].timeline[3].elapsed_time == 0.0
    assert games[0].timeline[3].event == "suspected double agent cast."
    assert games[0].timeline[3].mission == Missions.NoMission
    assert games[0].timeline[3].role == (Roles.SuspectedDoubleAgent,)
    assert games[0].timeline[3].time == 225.0

    assert games[0].timeline[4].action_test == ActionTest.NoAT
    assert games[0].timeline[4].actor == "spy"
    assert games[0].timeline[4].books == (None,)
    assert games[0].timeline[4].cast_name == (Characters.Morgan,)
    assert games[0].timeline[4].category == TimelineCategory.Cast
    assert games[0].timeline[4].elapsed_time == 0.0
    assert games[0].timeline[4].event == "seduction target cast."
    assert games[0].timeline[4].mission == Missions.NoMission
    assert games[0].timeline[4].role == (Roles.SeductionTarget,)
    assert games[0].timeline[4].time == 225.0

    assert games[0].timeline[5].action_test == ActionTest.NoAT
    assert games[0].timeline[5].actor == "spy"
    assert games[0].timeline[5].books == (None,)
    assert games[0].timeline[5].cast_name == (Characters.Queen,)
    assert games[0].timeline[5].category == TimelineCategory.Cast
    assert games[0].timeline[5].elapsed_time == 0.0
    assert games[0].timeline[5].event == "civilian cast."
    assert games[0].timeline[5].mission == Missions.NoMission
    assert games[0].timeline[5].role == (Roles.Civilian,)
    assert games[0].timeline[5].time == 225.0

    assert games[0].timeline[6].action_test == ActionTest.NoAT
    assert games[0].timeline[6].actor == "spy"
    assert games[0].timeline[6].books == (None,)
    assert games[0].timeline[6].cast_name == (Characters.Duke,)
    assert games[0].timeline[6].category == TimelineCategory.Cast
    assert games[0].timeline[6].elapsed_time == 0.0
    assert games[0].timeline[6].event == "civilian cast."
    assert games[0].timeline[6].mission == Missions.NoMission
    assert games[0].timeline[6].role == (Roles.Civilian,)
    assert games[0].timeline[6].time == 225.0

    assert games[0].timeline[7].action_test == ActionTest.NoAT
    assert games[0].timeline[7].actor == "spy"
    assert games[0].timeline[7].books == (None,)
    assert games[0].timeline[7].cast_name == (Characters.Oprah,)
    assert games[0].timeline[7].category == TimelineCategory.Cast
    assert games[0].timeline[7].elapsed_time == 0.0
    assert games[0].timeline[7].event == "civilian cast."
    assert games[0].timeline[7].mission == Missions.NoMission
    assert games[0].timeline[7].role == (Roles.Civilian,)
    assert games[0].timeline[7].time == 225.0

    assert games[0].timeline[8].action_test == ActionTest.NoAT
    assert games[0].timeline[8].actor == "spy"
    assert games[0].timeline[8].books == (None,)
    assert games[0].timeline[8].cast_name == (Characters.Sari,)
    assert games[0].timeline[8].category == TimelineCategory.Cast
    assert games[0].timeline[8].elapsed_time == 0.0
    assert games[0].timeline[8].event == "civilian cast."
    assert games[0].timeline[8].mission == Missions.NoMission
    assert games[0].timeline[8].role == (Roles.Civilian,)
    assert games[0].timeline[8].time == 225.0

    assert games[0].timeline[9].action_test == ActionTest.NoAT
    assert games[0].timeline[9].actor == "spy"
    assert games[0].timeline[9].books == (None,)
    assert games[0].timeline[9].cast_name == (Characters.Bling,)
    assert games[0].timeline[9].category == TimelineCategory.Cast
    assert games[0].timeline[9].elapsed_time == 0.0
    assert games[0].timeline[9].event == "civilian cast."
    assert games[0].timeline[9].mission == Missions.NoMission
    assert games[0].timeline[9].role == (Roles.Civilian,)
    assert games[0].timeline[9].time == 225.0

    assert games[0].timeline[10].action_test == ActionTest.NoAT
    assert games[0].timeline[10].actor == "spy"
    assert games[0].timeline[10].books == (None,)
    assert games[0].timeline[10].cast_name == (Characters.Disney,)
    assert games[0].timeline[10].category == TimelineCategory.Cast
    assert games[0].timeline[10].elapsed_time == 0.0
    assert games[0].timeline[10].event == "civilian cast."
    assert games[0].timeline[10].mission == Missions.NoMission
    assert games[0].timeline[10].role == (Roles.Civilian,)
    assert games[0].timeline[10].time == 225.0

    assert games[0].timeline[11].action_test == ActionTest.NoAT
    assert games[0].timeline[11].actor == "spy"
    assert games[0].timeline[11].books == (None,)
    assert games[0].timeline[11].cast_name == (Characters.Salmon,)
    assert games[0].timeline[11].category == TimelineCategory.Cast
    assert games[0].timeline[11].elapsed_time == 0.0
    assert games[0].timeline[11].event == "civilian cast."
    assert games[0].timeline[11].mission == Missions.NoMission
    assert games[0].timeline[11].role == (Roles.Civilian,)
    assert games[0].timeline[11].time == 225.0

    assert games[0].timeline[12].action_test == ActionTest.NoAT
    assert games[0].timeline[12].actor == "spy"
    assert games[0].timeline[12].books == (None,)
    assert games[0].timeline[12].cast_name == (Characters.General,)
    assert games[0].timeline[12].category == TimelineCategory.Cast
    assert games[0].timeline[12].elapsed_time == 0.0
    assert games[0].timeline[12].event == "civilian cast."
    assert games[0].timeline[12].mission == Missions.NoMission
    assert games[0].timeline[12].role == (Roles.Civilian,)
    assert games[0].timeline[12].time == 225.0

    assert games[0].timeline[13].action_test == ActionTest.NoAT
    assert games[0].timeline[13].actor == "spy"
    assert games[0].timeline[13].books == (None,)
    assert games[0].timeline[13].cast_name == (Characters.Rocker,)
    assert games[0].timeline[13].category == TimelineCategory.Cast
    assert games[0].timeline[13].elapsed_time == 0.0
    assert games[0].timeline[13].event == "civilian cast."
    assert games[0].timeline[13].mission == Missions.NoMission
    assert games[0].timeline[13].role == (Roles.Civilian,)
    assert games[0].timeline[13].time == 225.0

    assert games[0].timeline[14].action_test == ActionTest.NoAT
    assert games[0].timeline[14].actor == "spy"
    assert games[0].timeline[14].books == (None,)
    assert games[0].timeline[14].cast_name == (Characters.Teal,)
    assert games[0].timeline[14].category == TimelineCategory.Cast
    assert games[0].timeline[14].elapsed_time == 0.0
    assert games[0].timeline[14].event == "civilian cast."
    assert games[0].timeline[14].mission == Missions.NoMission
    assert games[0].timeline[14].role == (Roles.Civilian,)
    assert games[0].timeline[14].time == 225.0

    assert games[0].timeline[15].action_test == ActionTest.NoAT
    assert games[0].timeline[15].actor == "spy"
    assert games[0].timeline[15].books == (None,)
    assert games[0].timeline[15].cast_name == (Characters.Alice,)
    assert games[0].timeline[15].category == TimelineCategory.Cast
    assert games[0].timeline[15].elapsed_time == 0.0
    assert games[0].timeline[15].event == "civilian cast."
    assert games[0].timeline[15].mission == Missions.NoMission
    assert games[0].timeline[15].role == (Roles.Civilian,)
    assert games[0].timeline[15].time == 225.0

    assert games[0].timeline[16].action_test == ActionTest.NoAT
    assert games[0].timeline[16].actor == "spy"
    assert games[0].timeline[16].books == (None,)
    assert games[0].timeline[16].cast_name == (Characters.Smallman,)
    assert games[0].timeline[16].category == TimelineCategory.Cast
    assert games[0].timeline[16].elapsed_time == 0.0
    assert games[0].timeline[16].event == "civilian cast."
    assert games[0].timeline[16].mission == Missions.NoMission
    assert games[0].timeline[16].role == (Roles.Civilian,)
    assert games[0].timeline[16].time == 225.0

    assert games[0].timeline[17].action_test == ActionTest.NoAT
    assert games[0].timeline[17].actor == "spy"
    assert games[0].timeline[17].books == (None,)
    assert games[0].timeline[17].cast_name == (Characters.Sikh,)
    assert games[0].timeline[17].category == TimelineCategory.Cast
    assert games[0].timeline[17].elapsed_time == 0.0
    assert games[0].timeline[17].event == "civilian cast."
    assert games[0].timeline[17].mission == Missions.NoMission
    assert games[0].timeline[17].role == (Roles.Civilian,)
    assert games[0].timeline[17].time == 225.0

    assert games[0].timeline[18].action_test == ActionTest.NoAT
    assert games[0].timeline[18].actor == "spy"
    assert games[0].timeline[18].books == (None,)
    assert games[0].timeline[18].cast_name == (Characters.Plain,)
    assert games[0].timeline[18].category == TimelineCategory.Cast
    assert games[0].timeline[18].elapsed_time == 0.0
    assert games[0].timeline[18].event == "civilian cast."
    assert games[0].timeline[18].mission == Missions.NoMission
    assert games[0].timeline[18].role == (Roles.Civilian,)
    assert games[0].timeline[18].time == 225.0

    assert games[0].timeline[19].action_test == ActionTest.NoAT
    assert games[0].timeline[19].actor == "spy"
    assert games[0].timeline[19].books == (None,)
    assert games[0].timeline[19].cast_name == (Characters.Helen,)
    assert games[0].timeline[19].category == TimelineCategory.Cast
    assert games[0].timeline[19].elapsed_time == 0.0
    assert games[0].timeline[19].event == "civilian cast."
    assert games[0].timeline[19].mission == Missions.NoMission
    assert games[0].timeline[19].role == (Roles.Civilian,)
    assert games[0].timeline[19].time == 225.0

    assert games[0].timeline[20].action_test == ActionTest.NoAT
    assert games[0].timeline[20].actor == "spy"
    assert games[0].timeline[20].books == (None,)
    assert games[0].timeline[20].cast_name == (Characters.Taft,)
    assert games[0].timeline[20].category == TimelineCategory.Cast
    assert games[0].timeline[20].elapsed_time == 0.0
    assert games[0].timeline[20].event == "civilian cast."
    assert games[0].timeline[20].mission == Missions.NoMission
    assert games[0].timeline[20].role == (Roles.Civilian,)
    assert games[0].timeline[20].time == 225.0

    assert games[0].timeline[21].action_test == ActionTest.NoAT
    assert games[0].timeline[21].actor == "spy"
    assert games[0].timeline[21].books == (None,)
    assert games[0].timeline[21].cast_name == (None,)
    assert games[0].timeline[21].category == TimelineCategory.MissionSelected
    assert games[0].timeline[21].elapsed_time == 0.0
    assert games[0].timeline[21].event == "bug ambassador selected."
    assert games[0].timeline[21].mission == Missions.Bug
    assert games[0].timeline[21].role == (None,)
    assert games[0].timeline[21].time == 225.0

    assert games[0].timeline[22].action_test == ActionTest.NoAT
    assert games[0].timeline[22].actor == "spy"
    assert games[0].timeline[22].books == (None,)
    assert games[0].timeline[22].cast_name == (None,)
    assert games[0].timeline[22].category == TimelineCategory.MissionSelected
    assert games[0].timeline[22].elapsed_time == 0.0
    assert games[0].timeline[22].event == "contact double agent selected."
    assert games[0].timeline[22].mission == Missions.Contact
    assert games[0].timeline[22].role == (None,)
    assert games[0].timeline[22].time == 225.0

    assert games[0].timeline[23].action_test == ActionTest.NoAT
    assert games[0].timeline[23].actor == "spy"
    assert games[0].timeline[23].books == (None,)
    assert games[0].timeline[23].cast_name == (None,)
    assert games[0].timeline[23].category == TimelineCategory.MissionSelected
    assert games[0].timeline[23].elapsed_time == 0.0
    assert games[0].timeline[23].event == "transfer microfilm selected."
    assert games[0].timeline[23].mission == Missions.Transfer
    assert games[0].timeline[23].role == (None,)
    assert games[0].timeline[23].time == 225.0

    assert games[0].timeline[24].action_test == ActionTest.NoAT
    assert games[0].timeline[24].actor == "spy"
    assert games[0].timeline[24].books == (None,)
    assert games[0].timeline[24].cast_name == (None,)
    assert games[0].timeline[24].category == TimelineCategory.MissionSelected
    assert games[0].timeline[24].elapsed_time == 0.0
    assert games[0].timeline[24].event == "swap statue selected."
    assert games[0].timeline[24].mission == Missions.Swap
    assert games[0].timeline[24].role == (None,)
    assert games[0].timeline[24].time == 225.0

    assert games[0].timeline[25].action_test == ActionTest.NoAT
    assert games[0].timeline[25].actor == "spy"
    assert games[0].timeline[25].books == (None,)
    assert games[0].timeline[25].cast_name == (None,)
    assert games[0].timeline[25].category == TimelineCategory.MissionSelected
    assert games[0].timeline[25].elapsed_time == 0.0
    assert games[0].timeline[25].event == "inspect 3 statues selected."
    assert games[0].timeline[25].mission == Missions.Inspect
    assert games[0].timeline[25].role == (None,)
    assert games[0].timeline[25].time == 225.0

    assert games[0].timeline[26].action_test == ActionTest.NoAT
    assert games[0].timeline[26].actor == "spy"
    assert games[0].timeline[26].books == (None,)
    assert games[0].timeline[26].cast_name == (None,)
    assert games[0].timeline[26].category == TimelineCategory.MissionSelected
    assert games[0].timeline[26].elapsed_time == 0.0
    assert games[0].timeline[26].event == "seduce target selected."
    assert games[0].timeline[26].mission == Missions.Seduce
    assert games[0].timeline[26].role == (None,)
    assert games[0].timeline[26].time == 225.0

    assert games[0].timeline[27].action_test == ActionTest.NoAT
    assert games[0].timeline[27].actor == "spy"
    assert games[0].timeline[27].books == (None,)
    assert games[0].timeline[27].cast_name == (None,)
    assert games[0].timeline[27].category == TimelineCategory.MissionSelected
    assert games[0].timeline[27].elapsed_time == 0.0
    assert games[0].timeline[27].event == "purloin guest list selected."
    assert games[0].timeline[27].mission == Missions.Purloin
    assert games[0].timeline[27].role == (None,)
    assert games[0].timeline[27].time == 225.0

    assert games[0].timeline[28].action_test == ActionTest.NoAT
    assert games[0].timeline[28].actor == "spy"
    assert games[0].timeline[28].books == (None,)
    assert games[0].timeline[28].cast_name == (None,)
    assert games[0].timeline[28].category == TimelineCategory.MissionSelected
    assert games[0].timeline[28].elapsed_time == 0.0
    assert games[0].timeline[28].event == "fingerprint ambassador selected."
    assert games[0].timeline[28].mission == Missions.Fingerprint
    assert games[0].timeline[28].role == (None,)
    assert games[0].timeline[28].time == 225.0

    assert games[0].timeline[29].action_test == ActionTest.NoAT
    assert games[0].timeline[29].actor == "spy"
    assert games[0].timeline[29].books == (None,)
    assert games[0].timeline[29].cast_name == (None,)
    assert games[0].timeline[29].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[29].elapsed_time == 0.0
    assert games[0].timeline[29].event == "bug ambassador enabled."
    assert games[0].timeline[29].mission == Missions.Bug
    assert games[0].timeline[29].role == (None,)
    assert games[0].timeline[29].time == 225.0

    assert games[0].timeline[30].action_test == ActionTest.NoAT
    assert games[0].timeline[30].actor == "spy"
    assert games[0].timeline[30].books == (None,)
    assert games[0].timeline[30].cast_name == (None,)
    assert games[0].timeline[30].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[30].elapsed_time == 0.0
    assert games[0].timeline[30].event == "contact double agent enabled."
    assert games[0].timeline[30].mission == Missions.Contact
    assert games[0].timeline[30].role == (None,)
    assert games[0].timeline[30].time == 225.0

    assert games[0].timeline[31].action_test == ActionTest.NoAT
    assert games[0].timeline[31].actor == "spy"
    assert games[0].timeline[31].books == (None,)
    assert games[0].timeline[31].cast_name == (None,)
    assert games[0].timeline[31].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[31].elapsed_time == 0.0
    assert games[0].timeline[31].event == "transfer microfilm enabled."
    assert games[0].timeline[31].mission == Missions.Transfer
    assert games[0].timeline[31].role == (None,)
    assert games[0].timeline[31].time == 225.0

    assert games[0].timeline[32].action_test == ActionTest.NoAT
    assert games[0].timeline[32].actor == "spy"
    assert games[0].timeline[32].books == (None,)
    assert games[0].timeline[32].cast_name == (None,)
    assert games[0].timeline[32].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[32].elapsed_time == 0.0
    assert games[0].timeline[32].event == "swap statue enabled."
    assert games[0].timeline[32].mission == Missions.Swap
    assert games[0].timeline[32].role == (None,)
    assert games[0].timeline[32].time == 225.0

    assert games[0].timeline[33].action_test == ActionTest.NoAT
    assert games[0].timeline[33].actor == "spy"
    assert games[0].timeline[33].books == (None,)
    assert games[0].timeline[33].cast_name == (None,)
    assert games[0].timeline[33].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[33].elapsed_time == 0.0
    assert games[0].timeline[33].event == "inspect 3 statues enabled."
    assert games[0].timeline[33].mission == Missions.Inspect
    assert games[0].timeline[33].role == (None,)
    assert games[0].timeline[33].time == 225.0

    assert games[0].timeline[34].action_test == ActionTest.NoAT
    assert games[0].timeline[34].actor == "spy"
    assert games[0].timeline[34].books == (None,)
    assert games[0].timeline[34].cast_name == (None,)
    assert games[0].timeline[34].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[34].elapsed_time == 0.0
    assert games[0].timeline[34].event == "seduce target enabled."
    assert games[0].timeline[34].mission == Missions.Seduce
    assert games[0].timeline[34].role == (None,)
    assert games[0].timeline[34].time == 225.0

    assert games[0].timeline[35].action_test == ActionTest.NoAT
    assert games[0].timeline[35].actor == "spy"
    assert games[0].timeline[35].books == (None,)
    assert games[0].timeline[35].cast_name == (None,)
    assert games[0].timeline[35].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[35].elapsed_time == 0.0
    assert games[0].timeline[35].event == "purloin guest list enabled."
    assert games[0].timeline[35].mission == Missions.Purloin
    assert games[0].timeline[35].role == (None,)
    assert games[0].timeline[35].time == 225.0

    assert games[0].timeline[36].action_test == ActionTest.NoAT
    assert games[0].timeline[36].actor == "spy"
    assert games[0].timeline[36].books == (None,)
    assert games[0].timeline[36].cast_name == (None,)
    assert games[0].timeline[36].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[36].elapsed_time == 0.0
    assert games[0].timeline[36].event == "fingerprint ambassador enabled."
    assert games[0].timeline[36].mission == Missions.Fingerprint
    assert games[0].timeline[36].role == (None,)
    assert games[0].timeline[36].time == 225.0

    assert games[0].timeline[37].action_test == ActionTest.NoAT
    assert games[0].timeline[37].actor == "game"
    assert games[0].timeline[37].books == (None,)
    assert games[0].timeline[37].cast_name == (None,)
    assert games[0].timeline[37].category == TimelineCategory.GameStart
    assert games[0].timeline[37].elapsed_time == 0.0
    assert games[0].timeline[37].event == "game started."
    assert games[0].timeline[37].mission == Missions.NoMission
    assert games[0].timeline[37].role == (None,)
    assert games[0].timeline[37].time == 225.0

    assert games[0].timeline[38].action_test == ActionTest.NoAT
    assert games[0].timeline[38].actor == "spy"
    assert games[0].timeline[38].books == (None,)
    assert games[0].timeline[38].cast_name == (None,)
    assert games[0].timeline[38].category == TimelineCategory.NoCategory
    assert games[0].timeline[38].elapsed_time == 1.31
    assert games[0].timeline[38].event == "spy player takes control from ai."
    assert games[0].timeline[38].mission == Missions.NoMission
    assert games[0].timeline[38].role == (None,)
    assert games[0].timeline[38].time == 223.6

    assert games[0].timeline[39].action_test == ActionTest.NoAT
    assert games[0].timeline[39].actor == "sniper"
    assert games[0].timeline[39].books == (None,)
    assert games[0].timeline[39].cast_name == (Characters.Carlos,)
    assert games[0].timeline[39].category == TimelineCategory.SniperLights
    assert games[0].timeline[39].elapsed_time == 3.88
    assert games[0].timeline[39].event == "marked suspicious."
    assert games[0].timeline[39].mission == Missions.NoMission
    assert games[0].timeline[39].role == (Roles.Ambassador,)
    assert games[0].timeline[39].time == 221.1

    assert games[0].timeline[40].action_test == ActionTest.NoAT
    assert games[0].timeline[40].actor == "sniper"
    assert games[0].timeline[40].books == (None,)
    assert games[0].timeline[40].cast_name == (Characters.Damon,)
    assert games[0].timeline[40].category == TimelineCategory.SniperLights
    assert games[0].timeline[40].elapsed_time == 5.25
    assert games[0].timeline[40].event == "marked less suspicious."
    assert games[0].timeline[40].mission == Missions.NoMission
    assert games[0].timeline[40].role == (Roles.Staff,)
    assert games[0].timeline[40].time == 219.7

    assert games[0].timeline[41].action_test == ActionTest.NoAT
    assert games[0].timeline[41].actor == "sniper"
    assert games[0].timeline[41].books == (None,)
    assert games[0].timeline[41].cast_name == (Characters.Toby,)
    assert games[0].timeline[41].category == TimelineCategory.SniperLights
    assert games[0].timeline[41].elapsed_time == 6.38
    assert games[0].timeline[41].event == "marked suspicious."
    assert games[0].timeline[41].mission == Missions.NoMission
    assert games[0].timeline[41].role == (Roles.Staff,)
    assert games[0].timeline[41].time == 218.6

    assert games[0].timeline[42].action_test == ActionTest.NoAT
    assert games[0].timeline[42].actor == "sniper"
    assert games[0].timeline[42].books == (None,)
    assert games[0].timeline[42].cast_name == (Characters.Boots,)
    assert games[0].timeline[42].category == TimelineCategory.SniperLights
    assert games[0].timeline[42].elapsed_time == 8.81
    assert games[0].timeline[42].event == "marked less suspicious."
    assert games[0].timeline[42].mission == Missions.NoMission
    assert games[0].timeline[42].role == (Roles.DoubleAgent,)
    assert games[0].timeline[42].time == 216.1

    assert games[0].timeline[43].action_test == ActionTest.NoAT
    assert games[0].timeline[43].actor == "sniper"
    assert games[0].timeline[43].books == (None,)
    assert games[0].timeline[43].cast_name == (Characters.Wheels,)
    assert games[0].timeline[43].category == TimelineCategory.SniperLights
    assert games[0].timeline[43].elapsed_time == 9.81
    assert games[0].timeline[43].event == "marked less suspicious."
    assert games[0].timeline[43].mission == Missions.NoMission
    assert games[0].timeline[43].role == (Roles.SuspectedDoubleAgent,)
    assert games[0].timeline[43].time == 215.1

    assert games[0].timeline[44].action_test == ActionTest.NoAT
    assert games[0].timeline[44].actor == "spy"
    assert games[0].timeline[44].books == (None,)
    assert games[0].timeline[44].cast_name == (None,)
    assert games[0].timeline[44].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[44].elapsed_time == 10.0
    assert games[0].timeline[44].event == "action triggered: seduce target"
    assert games[0].timeline[44].mission == Missions.Seduce
    assert games[0].timeline[44].role == (None,)
    assert games[0].timeline[44].time == 214.9

    assert games[0].timeline[45].action_test == ActionTest.NoAT
    assert games[0].timeline[45].actor == "spy"
    assert games[0].timeline[45].books == (None,)
    assert games[0].timeline[45].cast_name == (Characters.Morgan,)
    assert games[0].timeline[45].category == TimelineCategory.NoCategory
    assert games[0].timeline[45].elapsed_time == 10.0
    assert games[0].timeline[45].event == "begin flirtation with seduction target."
    assert games[0].timeline[45].mission == Missions.Seduce
    assert games[0].timeline[45].role == (Roles.SeductionTarget,)
    assert games[0].timeline[45].time == 214.9

    assert games[0].timeline[46].action_test == ActionTest.White
    assert games[0].timeline[46].actor == "spy"
    assert games[0].timeline[46].books == (None,)
    assert games[0].timeline[46].cast_name == (None,)
    assert games[0].timeline[46].category == TimelineCategory.ActionTest
    assert games[0].timeline[46].elapsed_time == 10.94
    assert games[0].timeline[46].event == "action test white: seduce target"
    assert games[0].timeline[46].mission == Missions.Seduce
    assert games[0].timeline[46].role == (None,)
    assert games[0].timeline[46].time == 214.0

    assert games[0].timeline[47].action_test == ActionTest.NoAT
    assert games[0].timeline[47].actor == "sniper"
    assert games[0].timeline[47].books == (Books.Blue,)
    assert games[0].timeline[47].cast_name == (Characters.Disney,)
    assert (
        games[0].timeline[47].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[47].elapsed_time == 11.06
    assert games[0].timeline[47].event == "marked book."
    assert games[0].timeline[47].mission == Missions.NoMission
    assert games[0].timeline[47].role == (Roles.Civilian,)
    assert games[0].timeline[47].time == 213.9

    assert games[0].timeline[48].action_test == ActionTest.NoAT
    assert games[0].timeline[48].actor == "spy"
    assert games[0].timeline[48].books == (None,)
    assert games[0].timeline[48].cast_name == (Characters.Morgan,)
    assert games[0].timeline[48].category == TimelineCategory.MissionPartial
    assert games[0].timeline[48].elapsed_time == 12.44
    assert games[0].timeline[48].event == "flirt with seduction target: 34%"
    assert games[0].timeline[48].mission == Missions.Seduce
    assert games[0].timeline[48].role == (Roles.SeductionTarget,)
    assert games[0].timeline[48].time == 212.5

    assert games[0].timeline[49].action_test == ActionTest.NoAT
    assert games[0].timeline[49].actor == "sniper"
    assert games[0].timeline[49].books == (Books.Green,)
    assert games[0].timeline[49].cast_name == (Characters.Morgan,)
    assert (
        games[0].timeline[49].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[49].elapsed_time == 13.75
    assert games[0].timeline[49].event == "marked book."
    assert games[0].timeline[49].mission == Missions.NoMission
    assert games[0].timeline[49].role == (Roles.SeductionTarget,)
    assert games[0].timeline[49].time == 211.2

    assert games[0].timeline[50].action_test == ActionTest.NoAT
    assert games[0].timeline[50].actor == "spy"
    assert games[0].timeline[50].books == (Books.Green,)
    assert games[0].timeline[50].cast_name == (None,)
    assert games[0].timeline[50].category == TimelineCategory.Books
    assert games[0].timeline[50].elapsed_time == 15.50
    assert games[0].timeline[50].event == "get book from bookcase."
    assert games[0].timeline[50].mission == Missions.NoMission
    assert games[0].timeline[50].role == (None,)
    assert games[0].timeline[50].time == 209.4

    assert games[0].timeline[51].action_test == ActionTest.NoAT
    assert games[0].timeline[51].actor == "sniper"
    assert games[0].timeline[51].books == (None,)
    assert games[0].timeline[51].cast_name == (Characters.Rocker,)
    assert games[0].timeline[51].category == TimelineCategory.SniperLights
    assert games[0].timeline[51].elapsed_time == 20.88
    assert games[0].timeline[51].event == "marked suspicious."
    assert games[0].timeline[51].mission == Missions.NoMission
    assert games[0].timeline[51].role == (Roles.Civilian,)
    assert games[0].timeline[51].time == 204.1

    assert games[0].timeline[52].action_test == ActionTest.NoAT
    assert games[0].timeline[52].actor == "sniper"
    assert games[0].timeline[52].books == (None,)
    assert games[0].timeline[52].cast_name == (Characters.Smallman,)
    assert games[0].timeline[52].category == TimelineCategory.SniperLights
    assert games[0].timeline[52].elapsed_time == 21.25
    assert games[0].timeline[52].event == "marked suspicious."
    assert games[0].timeline[52].mission == Missions.NoMission
    assert games[0].timeline[52].role == (Roles.Civilian,)
    assert games[0].timeline[52].time == 203.7

    assert games[0].timeline[53].action_test == ActionTest.NoAT
    assert games[0].timeline[53].actor == "sniper"
    assert games[0].timeline[53].books == (None,)
    assert games[0].timeline[53].cast_name == (Characters.Sari,)
    assert games[0].timeline[53].category == TimelineCategory.SniperLights
    assert games[0].timeline[53].elapsed_time == 21.69
    assert games[0].timeline[53].event == "marked suspicious."
    assert games[0].timeline[53].mission == Missions.NoMission
    assert games[0].timeline[53].role == (Roles.Civilian,)
    assert games[0].timeline[53].time == 203.3

    assert games[0].timeline[54].action_test == ActionTest.NoAT
    assert games[0].timeline[54].actor == "spy"
    assert games[0].timeline[54].books == (None,)
    assert games[0].timeline[54].cast_name == (None,)
    assert games[0].timeline[54].category == TimelineCategory.NoCategory
    assert games[0].timeline[54].elapsed_time == 29.06
    assert games[0].timeline[54].event == "flirtation cooldown expired."
    assert games[0].timeline[54].mission == Missions.Seduce
    assert games[0].timeline[54].role == (None,)
    assert games[0].timeline[54].time == 195.9

    assert games[0].timeline[55].action_test == ActionTest.NoAT
    assert games[0].timeline[55].actor == "spy"
    assert games[0].timeline[55].books == (Books.Green, Books.Green)
    assert games[0].timeline[55].cast_name == (None,)
    assert games[0].timeline[55].category == TimelineCategory.Books
    assert games[0].timeline[55].elapsed_time == 37.13
    assert games[0].timeline[55].event == "put book in bookcase."
    assert games[0].timeline[55].mission == Missions.NoMission
    assert games[0].timeline[55].role == (None,)
    assert games[0].timeline[55].time == 187.8

    assert games[0].timeline[56].action_test == ActionTest.NoAT
    assert games[0].timeline[56].actor == "sniper"
    assert games[0].timeline[56].books == (Books.Blue,)
    assert games[0].timeline[56].cast_name == (Characters.Salmon,)
    assert (
        games[0].timeline[56].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[56].elapsed_time == 37.31
    assert games[0].timeline[56].event == "marked book."
    assert games[0].timeline[56].mission == Missions.NoMission
    assert games[0].timeline[56].role == (Roles.Civilian,)
    assert games[0].timeline[56].time == 187.6

    assert games[0].timeline[57].action_test == ActionTest.NoAT
    assert games[0].timeline[57].actor == "sniper"
    assert games[0].timeline[57].books == (None,)
    assert games[0].timeline[57].cast_name == (Characters.Helen,)
    assert games[0].timeline[57].category == TimelineCategory.SniperLights
    assert games[0].timeline[57].elapsed_time == 40.06
    assert games[0].timeline[57].event == "marked suspicious."
    assert games[0].timeline[57].mission == Missions.NoMission
    assert games[0].timeline[57].role == (Roles.Civilian,)
    assert games[0].timeline[57].time == 184.9

    assert games[0].timeline[58].action_test == ActionTest.NoAT
    assert games[0].timeline[58].actor == "spy"
    assert games[0].timeline[58].books == (None,)
    assert games[0].timeline[58].cast_name == (None,)
    assert games[0].timeline[58].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[58].elapsed_time == 41.00
    assert games[0].timeline[58].event == "action triggered: bug ambassador"
    assert games[0].timeline[58].mission == Missions.Bug
    assert games[0].timeline[58].role == (None,)
    assert games[0].timeline[58].time == 183.9

    assert games[0].timeline[59].action_test == ActionTest.NoAT
    assert games[0].timeline[59].actor == "spy"
    assert games[0].timeline[59].books == (None,)
    assert games[0].timeline[59].cast_name == (Characters.Carlos,)
    assert games[0].timeline[59].category == TimelineCategory.NoCategory
    assert games[0].timeline[59].elapsed_time == 41.00
    assert games[0].timeline[59].event == "begin planting bug while walking."
    assert games[0].timeline[59].mission == Missions.Bug
    assert games[0].timeline[59].role == (Roles.Ambassador,)
    assert games[0].timeline[59].time == 183.9

    assert games[0].timeline[60].action_test == ActionTest.NoAT
    assert games[0].timeline[60].actor == "spy"
    assert games[0].timeline[60].books == (None,)
    assert games[0].timeline[60].cast_name == (Characters.Carlos,)
    assert games[0].timeline[60].category == TimelineCategory.MissionComplete
    assert games[0].timeline[60].elapsed_time == 41.94
    assert games[0].timeline[60].event == "bugged ambassador while walking."
    assert games[0].timeline[60].mission == Missions.Bug
    assert games[0].timeline[60].role == (Roles.Ambassador,)
    assert games[0].timeline[60].time == 183.0

    assert games[0].timeline[61].action_test == ActionTest.NoAT
    assert games[0].timeline[61].actor == "sniper"
    assert games[0].timeline[61].books == (None,)
    assert games[0].timeline[61].cast_name == (Characters.Irish,)
    assert games[0].timeline[61].category == TimelineCategory.SniperLights
    assert games[0].timeline[61].elapsed_time == 46.75
    assert games[0].timeline[61].event == "marked spy suspicious."
    assert games[0].timeline[61].mission == Missions.NoMission
    assert games[0].timeline[61].role == (Roles.Spy,)
    assert games[0].timeline[61].time == 178.2

    assert games[0].timeline[62].action_test == ActionTest.NoAT
    assert games[0].timeline[62].actor == "spy"
    assert games[0].timeline[62].books == (None,)
    assert games[0].timeline[62].cast_name == (None,)
    assert games[0].timeline[62].category == TimelineCategory.Conversation
    assert games[0].timeline[62].elapsed_time == 54.56
    assert games[0].timeline[62].event == "spy enters conversation."
    assert games[0].timeline[62].mission == Missions.NoMission
    assert games[0].timeline[62].role == (None,)
    assert games[0].timeline[62].time == 170.4

    assert games[0].timeline[63].action_test == ActionTest.NoAT
    assert games[0].timeline[63].actor == "spy"
    assert games[0].timeline[63].books == (None,)
    assert games[0].timeline[63].cast_name == (None,)
    assert games[0].timeline[63].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[63].elapsed_time == 59.75
    assert games[0].timeline[63].event == "action triggered: seduce target"
    assert games[0].timeline[63].mission == Missions.Seduce
    assert games[0].timeline[63].role == (None,)
    assert games[0].timeline[63].time == 165.2

    assert games[0].timeline[64].action_test == ActionTest.NoAT
    assert games[0].timeline[64].actor == "spy"
    assert games[0].timeline[64].books == (None,)
    assert games[0].timeline[64].cast_name == (Characters.Morgan,)
    assert games[0].timeline[64].category == TimelineCategory.NoCategory
    assert games[0].timeline[64].elapsed_time == 59.75
    assert games[0].timeline[64].event == "begin flirtation with seduction target."
    assert games[0].timeline[64].mission == Missions.Seduce
    assert games[0].timeline[64].role == (Roles.SeductionTarget,)
    assert games[0].timeline[64].time == 165.2

    assert games[0].timeline[65].action_test == ActionTest.White
    assert games[0].timeline[65].actor == "spy"
    assert games[0].timeline[65].books == (None,)
    assert games[0].timeline[65].cast_name == (None,)
    assert games[0].timeline[65].category == TimelineCategory.ActionTest
    assert games[0].timeline[65].elapsed_time == 60.56
    assert games[0].timeline[65].event == "action test white: seduce target"
    assert games[0].timeline[65].mission == Missions.Seduce
    assert games[0].timeline[65].role == (None,)
    assert games[0].timeline[65].time == 164.4

    assert games[0].timeline[66].action_test == ActionTest.NoAT
    assert games[0].timeline[66].actor == "spy"
    assert games[0].timeline[66].books == (None,)
    assert games[0].timeline[66].cast_name == (Characters.Morgan,)
    assert games[0].timeline[66].category == TimelineCategory.MissionPartial
    assert games[0].timeline[66].elapsed_time == 60.56
    assert games[0].timeline[66].event == "flirt with seduction target: 68%"
    assert games[0].timeline[66].mission == Missions.Seduce
    assert games[0].timeline[66].role == (Roles.SeductionTarget,)
    assert games[0].timeline[66].time == 164.4

    assert games[0].timeline[67].action_test == ActionTest.NoAT
    assert games[0].timeline[67].actor == "sniper"
    assert games[0].timeline[67].books == (None,)
    assert games[0].timeline[67].cast_name == (Characters.Oprah,)
    assert games[0].timeline[67].category == TimelineCategory.SniperLights
    assert games[0].timeline[67].elapsed_time == 89.81
    assert games[0].timeline[67].event == "marked suspicious."
    assert games[0].timeline[67].mission == Missions.NoMission
    assert games[0].timeline[67].role == (Roles.Civilian,)
    assert games[0].timeline[67].time == 135.1

    assert games[0].timeline[68].action_test == ActionTest.NoAT
    assert games[0].timeline[68].actor == "spy"
    assert games[0].timeline[68].books == (None,)
    assert games[0].timeline[68].cast_name == (None,)
    assert games[0].timeline[68].category == TimelineCategory.NoCategory
    assert games[0].timeline[68].elapsed_time == 105.63
    assert games[0].timeline[68].event == "flirtation cooldown expired."
    assert games[0].timeline[68].mission == Missions.Seduce
    assert games[0].timeline[68].role == (None,)
    assert games[0].timeline[68].time == 119.3

    assert games[0].timeline[69].action_test == ActionTest.NoAT
    assert games[0].timeline[69].actor == "spy"
    assert games[0].timeline[69].books == (None,)
    assert games[0].timeline[69].cast_name == (None,)
    assert games[0].timeline[69].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[69].elapsed_time == 106.19
    assert games[0].timeline[69].event == "action triggered: seduce target"
    assert games[0].timeline[69].mission == Missions.Seduce
    assert games[0].timeline[69].role == (None,)
    assert games[0].timeline[69].time == 118.8

    assert games[0].timeline[70].action_test == ActionTest.NoAT
    assert games[0].timeline[70].actor == "spy"
    assert games[0].timeline[70].books == (None,)
    assert games[0].timeline[70].cast_name == (Characters.Morgan,)
    assert games[0].timeline[70].category == TimelineCategory.NoCategory
    assert games[0].timeline[70].elapsed_time == 106.19
    assert games[0].timeline[70].event == "begin flirtation with seduction target."
    assert games[0].timeline[70].mission == Missions.Seduce
    assert games[0].timeline[70].role == (Roles.SeductionTarget,)
    assert games[0].timeline[70].time == 118.8

    assert games[0].timeline[71].action_test == ActionTest.White
    assert games[0].timeline[71].actor == "spy"
    assert games[0].timeline[71].books == (None,)
    assert games[0].timeline[71].cast_name == (None,)
    assert games[0].timeline[71].category == TimelineCategory.ActionTest
    assert games[0].timeline[71].elapsed_time == 107.13
    assert games[0].timeline[71].event == "action test white: seduce target"
    assert games[0].timeline[71].mission == Missions.Seduce
    assert games[0].timeline[71].role == (None,)
    assert games[0].timeline[71].time == 117.8

    assert games[0].timeline[72].action_test == ActionTest.NoAT
    assert games[0].timeline[72].actor == "spy"
    assert games[0].timeline[72].books == (None,)
    assert games[0].timeline[72].cast_name == (Characters.Morgan,)
    assert games[0].timeline[72].category == TimelineCategory.MissionPartial
    assert games[0].timeline[72].elapsed_time == 107.13
    assert games[0].timeline[72].event == "flirt with seduction target: 100%"
    assert games[0].timeline[72].mission == Missions.Seduce
    assert games[0].timeline[72].role == (Roles.SeductionTarget,)
    assert games[0].timeline[72].time == 117.8

    assert games[0].timeline[73].action_test == ActionTest.NoAT
    assert games[0].timeline[73].actor == "spy"
    assert games[0].timeline[73].books == (None,)
    assert games[0].timeline[73].cast_name == (Characters.Morgan,)
    assert games[0].timeline[73].category == TimelineCategory.MissionComplete
    assert games[0].timeline[73].elapsed_time == 107.13
    assert games[0].timeline[73].event == "target seduced."
    assert games[0].timeline[73].mission == Missions.Seduce
    assert games[0].timeline[73].role == (Roles.SeductionTarget,)
    assert games[0].timeline[73].time == 117.8

    assert games[0].timeline[74].action_test == ActionTest.NoAT
    assert games[0].timeline[74].actor == "spy"
    assert games[0].timeline[74].books == (None,)
    assert games[0].timeline[74].cast_name == (None,)
    assert games[0].timeline[74].category == TimelineCategory.Conversation
    assert games[0].timeline[74].elapsed_time == 123.56
    assert games[0].timeline[74].event == "spy leaves conversation."
    assert games[0].timeline[74].mission == Missions.NoMission
    assert games[0].timeline[74].role == (None,)
    assert games[0].timeline[74].time == 101.4

    assert games[0].timeline[75].action_test == ActionTest.NoAT
    assert games[0].timeline[75].actor == "sniper"
    assert games[0].timeline[75].books == (Books.Blue,)
    assert games[0].timeline[75].cast_name == (Characters.General,)
    assert (
        games[0].timeline[75].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[75].elapsed_time == 126.31
    assert games[0].timeline[75].event == "marked book."
    assert games[0].timeline[75].mission == Missions.NoMission
    assert games[0].timeline[75].role == (Roles.Civilian,)
    assert games[0].timeline[75].time == 98.6

    assert games[0].timeline[76].action_test == ActionTest.NoAT
    assert games[0].timeline[76].actor == "sniper"
    assert games[0].timeline[76].books == (None,)
    assert games[0].timeline[76].cast_name == (Characters.Plain,)
    assert games[0].timeline[76].category == TimelineCategory.SniperLights
    assert games[0].timeline[76].elapsed_time == 128.75
    assert games[0].timeline[76].event == "marked suspicious."
    assert games[0].timeline[76].mission == Missions.NoMission
    assert games[0].timeline[76].role == (Roles.Civilian,)
    assert games[0].timeline[76].time == 96.2

    assert games[0].timeline[77].action_test == ActionTest.NoAT
    assert games[0].timeline[77].actor == "spy"
    assert games[0].timeline[77].books == (None,)
    assert games[0].timeline[77].cast_name == (Characters.Irish,)
    assert games[0].timeline[77].category == TimelineCategory.Drinks
    assert games[0].timeline[77].elapsed_time == 139.44
    assert games[0].timeline[77].event == "waiter offered drink."
    assert games[0].timeline[77].mission == Missions.NoMission
    assert games[0].timeline[77].role == (Roles.Spy,)
    assert games[0].timeline[77].time == 85.5

    assert games[0].timeline[78].action_test == ActionTest.NoAT
    assert games[0].timeline[78].actor == "spy"
    assert games[0].timeline[78].books == (None,)
    assert games[0].timeline[78].cast_name == (Characters.Irish,)
    assert games[0].timeline[78].category == TimelineCategory.Drinks
    assert games[0].timeline[78].elapsed_time == 142.94
    assert games[0].timeline[78].event == "rejected drink from waiter."
    assert games[0].timeline[78].mission == Missions.NoMission
    assert games[0].timeline[78].role == (Roles.Spy,)
    assert games[0].timeline[78].time == 82.0

    assert games[0].timeline[79].action_test == ActionTest.NoAT
    assert games[0].timeline[79].actor == "spy"
    assert games[0].timeline[79].books == (None,)
    assert games[0].timeline[79].cast_name == (Characters.Irish,)
    assert games[0].timeline[79].category == TimelineCategory.Drinks
    assert games[0].timeline[79].elapsed_time == 142.94
    assert games[0].timeline[79].event == "waiter stopped offering drink."
    assert games[0].timeline[79].mission == Missions.NoMission
    assert games[0].timeline[79].role == (Roles.Spy,)
    assert games[0].timeline[79].time == 82.0

    assert games[0].timeline[80].action_test == ActionTest.NoAT
    assert games[0].timeline[80].actor == "spy"
    assert games[0].timeline[80].books == (None,)
    assert games[0].timeline[80].cast_name == (None,)
    assert games[0].timeline[80].category == TimelineCategory.Statues
    assert games[0].timeline[80].elapsed_time == 150.63
    assert games[0].timeline[80].event == "picked up statue."
    assert games[0].timeline[80].mission == Missions.NoMission
    assert games[0].timeline[80].role == (None,)
    assert games[0].timeline[80].time == 74.3

    assert games[0].timeline[81].action_test == ActionTest.NoAT
    assert games[0].timeline[81].actor == "spy"
    assert games[0].timeline[81].books == (None,)
    assert games[0].timeline[81].cast_name == (None,)
    assert games[0].timeline[81].category == TimelineCategory.Statues
    assert games[0].timeline[81].elapsed_time == 153.25
    assert games[0].timeline[81].event == "picked up fingerprintable statue."
    assert games[0].timeline[81].mission == Missions.Fingerprint
    assert games[0].timeline[81].role == (None,)
    assert games[0].timeline[81].time == 71.7

    assert games[0].timeline[82].action_test == ActionTest.NoAT
    assert games[0].timeline[82].actor == "spy"
    assert games[0].timeline[82].books == (None,)
    assert games[0].timeline[82].cast_name == (None,)
    assert (
        games[0].timeline[82].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[0].timeline[82].elapsed_time == 153.63
    assert games[0].timeline[82].event == "action triggered: inspect statues"
    assert games[0].timeline[82].mission == Missions.Inspect
    assert games[0].timeline[82].role == (None,)
    assert games[0].timeline[82].time == 71.3

    assert games[0].timeline[83].action_test == ActionTest.White
    assert games[0].timeline[83].actor == "spy"
    assert games[0].timeline[83].books == (None,)
    assert games[0].timeline[83].cast_name == (None,)
    assert (
        games[0].timeline[83].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[0].timeline[83].elapsed_time == 154.81
    assert games[0].timeline[83].event == "action test white: inspect statues"
    assert games[0].timeline[83].mission == Missions.Inspect
    assert games[0].timeline[83].role == (None,)
    assert games[0].timeline[83].time == 70.1

    assert games[0].timeline[84].action_test == ActionTest.NoAT
    assert games[0].timeline[84].actor == "spy"
    assert games[0].timeline[84].books == (None,)
    assert games[0].timeline[84].cast_name == (None,)
    assert (
        games[0].timeline[84].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[0].timeline[84].elapsed_time == 158.63
    assert games[0].timeline[84].event == "left statue inspected."
    assert games[0].timeline[84].mission == Missions.Inspect
    assert games[0].timeline[84].role == (None,)
    assert games[0].timeline[84].time == 66.3

    assert games[0].timeline[85].action_test == ActionTest.NoAT
    assert games[0].timeline[85].actor == "spy"
    assert games[0].timeline[85].books == (None,)
    assert games[0].timeline[85].cast_name == (None,)
    assert (
        games[0].timeline[85].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[0].timeline[85].elapsed_time == 159.00
    assert games[0].timeline[85].event == "action triggered: inspect statues"
    assert games[0].timeline[85].mission == Missions.Inspect
    assert games[0].timeline[85].role == (None,)
    assert games[0].timeline[85].time == 66.0

    assert games[0].timeline[86].action_test == ActionTest.Green
    assert games[0].timeline[86].actor == "spy"
    assert games[0].timeline[86].books == (None,)
    assert games[0].timeline[86].cast_name == (None,)
    assert (
        games[0].timeline[86].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[0].timeline[86].elapsed_time == 160.13
    assert games[0].timeline[86].event == "action test green: inspect statues"
    assert games[0].timeline[86].mission == Missions.Inspect
    assert games[0].timeline[86].role == (None,)
    assert games[0].timeline[86].time == 64.8

    assert games[0].timeline[87].action_test == ActionTest.NoAT
    assert games[0].timeline[87].actor == "spy"
    assert games[0].timeline[87].books == (None,)
    assert games[0].timeline[87].cast_name == (None,)
    assert (
        games[0].timeline[87].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[0].timeline[87].elapsed_time == 161.50
    assert games[0].timeline[87].event == "held statue inspected."
    assert games[0].timeline[87].mission == Missions.Inspect
    assert games[0].timeline[87].role == (None,)
    assert games[0].timeline[87].time == 63.4

    assert games[0].timeline[88].action_test == ActionTest.NoAT
    assert games[0].timeline[88].actor == "spy"
    assert games[0].timeline[88].books == (None,)
    assert games[0].timeline[88].cast_name == (None,)
    assert games[0].timeline[88].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[88].elapsed_time == 162.00
    assert games[0].timeline[88].event == "action triggered: fingerprint ambassador"
    assert games[0].timeline[88].mission == Missions.Fingerprint
    assert games[0].timeline[88].role == (None,)
    assert games[0].timeline[88].time == 62.9

    assert games[0].timeline[89].action_test == ActionTest.NoAT
    assert games[0].timeline[89].actor == "spy"
    assert games[0].timeline[89].books == (None,)
    assert games[0].timeline[89].cast_name == (None,)
    assert games[0].timeline[89].category == TimelineCategory.Statues
    assert games[0].timeline[89].elapsed_time == 162.00
    assert games[0].timeline[89].event == "started fingerprinting statue."
    assert games[0].timeline[89].mission == Missions.Fingerprint
    assert games[0].timeline[89].role == (None,)
    assert games[0].timeline[89].time == 62.9

    assert games[0].timeline[90].action_test == ActionTest.NoAT
    assert games[0].timeline[90].actor == "spy"
    assert games[0].timeline[90].books == (None,)
    assert games[0].timeline[90].cast_name == (None,)
    assert (
        games[0].timeline[90].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[0].timeline[90].elapsed_time == 163.00
    assert games[0].timeline[90].event == "fingerprinted statue."
    assert games[0].timeline[90].mission == Missions.Fingerprint
    assert games[0].timeline[90].role == (None,)
    assert games[0].timeline[90].time == 61.9

    assert games[0].timeline[91].action_test == ActionTest.NoAT
    assert games[0].timeline[91].actor == "spy"
    assert games[0].timeline[91].books == (None,)
    assert games[0].timeline[91].cast_name == (None,)
    assert games[0].timeline[91].category == TimelineCategory.Statues
    assert games[0].timeline[91].elapsed_time == 164.00
    assert games[0].timeline[91].event == "put back statue."
    assert games[0].timeline[91].mission == Missions.NoMission
    assert games[0].timeline[91].role == (None,)
    assert games[0].timeline[91].time == 60.9

    assert games[0].timeline[92].action_test == ActionTest.NoAT
    assert games[0].timeline[92].actor == "spy"
    assert games[0].timeline[92].books == (None,)
    assert games[0].timeline[92].cast_name == (Characters.Irish,)
    assert games[0].timeline[92].category == TimelineCategory.Drinks
    assert games[0].timeline[92].elapsed_time == 172.19
    assert games[0].timeline[92].event == "waiter offered drink."
    assert games[0].timeline[92].mission == Missions.NoMission
    assert games[0].timeline[92].role == (Roles.Spy,)
    assert games[0].timeline[92].time == 52.8

    assert games[0].timeline[93].action_test == ActionTest.NoAT
    assert games[0].timeline[93].actor == "spy"
    assert games[0].timeline[93].books == (None,)
    assert games[0].timeline[93].cast_name == (Characters.Irish,)
    assert games[0].timeline[93].category == TimelineCategory.Drinks
    assert games[0].timeline[93].elapsed_time == 176.69
    assert games[0].timeline[93].event == "rejected drink from waiter."
    assert games[0].timeline[93].mission == Missions.NoMission
    assert games[0].timeline[93].role == (Roles.Spy,)
    assert games[0].timeline[93].time == 48.3

    assert games[0].timeline[94].action_test == ActionTest.NoAT
    assert games[0].timeline[94].actor == "spy"
    assert games[0].timeline[94].books == (None,)
    assert games[0].timeline[94].cast_name == (Characters.Irish,)
    assert games[0].timeline[94].category == TimelineCategory.Drinks
    assert games[0].timeline[94].elapsed_time == 176.69
    assert games[0].timeline[94].event == "waiter stopped offering drink."
    assert games[0].timeline[94].mission == Missions.NoMission
    assert games[0].timeline[94].role == (Roles.Spy,)
    assert games[0].timeline[94].time == 48.3

    assert games[0].timeline[95].action_test == ActionTest.NoAT
    assert games[0].timeline[95].actor == "sniper"
    assert games[0].timeline[95].books == (None,)
    assert games[0].timeline[95].cast_name == (Characters.Duke,)
    assert games[0].timeline[95].category == TimelineCategory.SniperLights
    assert games[0].timeline[95].elapsed_time == 181.00
    assert games[0].timeline[95].event == "marked less suspicious."
    assert games[0].timeline[95].mission == Missions.NoMission
    assert games[0].timeline[95].role == (Roles.Civilian,)
    assert games[0].timeline[95].time == 44.0

    assert games[0].timeline[96].action_test == ActionTest.NoAT
    assert games[0].timeline[96].actor == "sniper"
    assert games[0].timeline[96].books == (None,)
    assert games[0].timeline[96].cast_name == (Characters.Teal,)
    assert games[0].timeline[96].category == TimelineCategory.SniperLights
    assert games[0].timeline[96].elapsed_time == 198.56
    assert games[0].timeline[96].event == "marked suspicious."
    assert games[0].timeline[96].mission == Missions.NoMission
    assert games[0].timeline[96].role == (Roles.Civilian,)
    assert games[0].timeline[96].time == 26.4

    assert games[0].timeline[97].action_test == ActionTest.NoAT
    assert games[0].timeline[97].actor == "spy"
    assert games[0].timeline[97].books == (Books.Blue,)
    assert games[0].timeline[97].cast_name == (None,)
    assert games[0].timeline[97].category == TimelineCategory.Books
    assert games[0].timeline[97].elapsed_time == 202.06
    assert games[0].timeline[97].event == "get book from bookcase."
    assert games[0].timeline[97].mission == Missions.NoMission
    assert games[0].timeline[97].role == (None,)
    assert games[0].timeline[97].time == 22.9

    assert games[0].timeline[98].action_test == ActionTest.NoAT
    assert games[0].timeline[98].actor == "spy"
    assert games[0].timeline[98].books == (None,)
    assert games[0].timeline[98].cast_name == (None,)
    assert games[0].timeline[98].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[98].elapsed_time == 202.56
    assert games[0].timeline[98].event == "action triggered: fingerprint ambassador"
    assert games[0].timeline[98].mission == Missions.Fingerprint
    assert games[0].timeline[98].role == (None,)
    assert games[0].timeline[98].time == 22.4

    assert games[0].timeline[99].action_test == ActionTest.NoAT
    assert games[0].timeline[99].actor == "spy"
    assert games[0].timeline[99].books == (None,)
    assert games[0].timeline[99].cast_name == (None,)
    assert games[0].timeline[99].category == TimelineCategory.Books
    assert games[0].timeline[99].elapsed_time == 202.56
    assert games[0].timeline[99].event == "started fingerprinting book."
    assert games[0].timeline[99].mission == Missions.Fingerprint
    assert games[0].timeline[99].role == (None,)
    assert games[0].timeline[99].time == 22.4

    assert games[0].timeline[100].action_test == ActionTest.Red
    assert games[0].timeline[100].actor == "spy"
    assert games[0].timeline[100].books == (None,)
    assert games[0].timeline[100].cast_name == (None,)
    assert games[0].timeline[100].category == TimelineCategory.ActionTest
    assert games[0].timeline[100].elapsed_time == 203.56
    assert games[0].timeline[100].event == "action test red: fingerprint ambassador"
    assert games[0].timeline[100].mission == Missions.Fingerprint
    assert games[0].timeline[100].role == (None,)
    assert games[0].timeline[100].time == 21.4

    assert games[0].timeline[101].action_test == ActionTest.NoAT
    assert games[0].timeline[101].actor == "spy"
    assert games[0].timeline[101].books == (None,)
    assert games[0].timeline[101].cast_name == (None,)
    assert games[0].timeline[101].category == TimelineCategory.NoCategory
    assert games[0].timeline[101].elapsed_time == 203.56
    assert games[0].timeline[101].event == "fingerprinting failed."
    assert games[0].timeline[101].mission == Missions.Fingerprint
    assert games[0].timeline[101].role == (None,)
    assert games[0].timeline[101].time == 21.4

    assert games[0].timeline[102].action_test == ActionTest.NoAT
    assert games[0].timeline[102].actor == "spy"
    assert games[0].timeline[102].books == (None,)
    assert games[0].timeline[102].cast_name == (None,)
    assert games[0].timeline[102].category == TimelineCategory.Conversation
    assert games[0].timeline[102].elapsed_time == 207.31
    assert games[0].timeline[102].event == "spy enters conversation."
    assert games[0].timeline[102].mission == Missions.NoMission
    assert games[0].timeline[102].role == (None,)
    assert games[0].timeline[102].time == 17.6

    assert games[0].timeline[103].action_test == ActionTest.NoAT
    assert games[0].timeline[103].actor == "spy"
    assert games[0].timeline[103].books == (None,)
    assert games[0].timeline[103].cast_name == (Characters.Boots,)
    assert games[0].timeline[103].category == TimelineCategory.Conversation
    assert games[0].timeline[103].elapsed_time == 207.31
    assert games[0].timeline[103].event == "spy joined conversation with double agent."
    assert games[0].timeline[103].mission == Missions.NoMission
    assert games[0].timeline[103].role == (Roles.DoubleAgent,)
    assert games[0].timeline[103].time == 17.6

    assert games[0].timeline[104].action_test == ActionTest.NoAT
    assert games[0].timeline[104].actor == "spy"
    assert games[0].timeline[104].books == (None,)
    assert games[0].timeline[104].cast_name == (None,)
    assert games[0].timeline[104].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[104].elapsed_time == 207.63
    assert games[0].timeline[104].event == "action triggered: contact double agent"
    assert games[0].timeline[104].mission == Missions.Contact
    assert games[0].timeline[104].role == (None,)
    assert games[0].timeline[104].time == 17.3

    assert games[0].timeline[105].action_test == ActionTest.NoAT
    assert games[0].timeline[105].actor == "spy"
    assert games[0].timeline[105].books == (None,)
    assert games[0].timeline[105].cast_name == (None,)
    assert games[0].timeline[105].category == TimelineCategory.BananaBread
    assert games[0].timeline[105].elapsed_time == 207.63
    assert games[0].timeline[105].event == "real banana bread started."
    assert games[0].timeline[105].mission == Missions.Contact
    assert games[0].timeline[105].role == (None,)
    assert games[0].timeline[105].time == 17.3

    assert games[0].timeline[106].action_test == ActionTest.White
    assert games[0].timeline[106].actor == "spy"
    assert games[0].timeline[106].books == (None,)
    assert games[0].timeline[106].cast_name == (None,)
    assert games[0].timeline[106].category == TimelineCategory.ActionTest
    assert games[0].timeline[106].elapsed_time == 208.44
    assert games[0].timeline[106].event == "action test white: contact double agent"
    assert games[0].timeline[106].mission == Missions.Contact
    assert games[0].timeline[106].role == (None,)
    assert games[0].timeline[106].time == 16.5

    assert games[0].timeline[107].action_test == ActionTest.NoAT
    assert games[0].timeline[107].actor == "spy"
    assert games[0].timeline[107].books == (None,)
    assert games[0].timeline[107].cast_name == (None,)
    assert games[0].timeline[107].category == TimelineCategory.BananaBread
    assert games[0].timeline[107].elapsed_time == 210.25
    assert games[0].timeline[107].event == "banana bread uttered."
    assert games[0].timeline[107].mission == Missions.Contact
    assert games[0].timeline[107].role == (None,)
    assert games[0].timeline[107].time == 14.7

    assert games[0].timeline[108].action_test == ActionTest.NoAT
    assert games[0].timeline[108].actor == "spy"
    assert games[0].timeline[108].books == (None,)
    assert games[0].timeline[108].cast_name == (Characters.Boots,)
    assert games[0].timeline[108].category == TimelineCategory.MissionComplete
    assert games[0].timeline[108].elapsed_time == 210.81
    assert games[0].timeline[108].event == "double agent contacted."
    assert games[0].timeline[108].mission == Missions.Contact
    assert games[0].timeline[108].role == (Roles.DoubleAgent,)
    assert games[0].timeline[108].time == 14.1

    assert games[0].timeline[109].action_test == ActionTest.NoAT
    assert games[0].timeline[109].actor == "sniper"
    assert games[0].timeline[109].books == (None,)
    assert games[0].timeline[109].cast_name == (Characters.Sari,)
    assert games[0].timeline[109].category == TimelineCategory.SniperLights
    assert games[0].timeline[109].elapsed_time == 213.50
    assert games[0].timeline[109].event == "marked less suspicious."
    assert games[0].timeline[109].mission == Missions.NoMission
    assert games[0].timeline[109].role == (Roles.Civilian,)
    assert games[0].timeline[109].time == 11.5

    assert games[0].timeline[110].action_test == ActionTest.NoAT
    assert games[0].timeline[110].actor == "sniper"
    assert games[0].timeline[110].books == (None,)
    assert games[0].timeline[110].cast_name == (Characters.Smallman,)
    assert games[0].timeline[110].category == TimelineCategory.SniperLights
    assert games[0].timeline[110].elapsed_time == 213.81
    assert games[0].timeline[110].event == "marked less suspicious."
    assert games[0].timeline[110].mission == Missions.NoMission
    assert games[0].timeline[110].role == (Roles.Civilian,)
    assert games[0].timeline[110].time == 11.1

    assert games[0].timeline[111].action_test == ActionTest.NoAT
    assert games[0].timeline[111].actor == "sniper"
    assert games[0].timeline[111].books == (None,)
    assert games[0].timeline[111].cast_name == (Characters.Bling,)
    assert games[0].timeline[111].category == TimelineCategory.SniperLights
    assert games[0].timeline[111].elapsed_time == 214.25
    assert games[0].timeline[111].event == "marked less suspicious."
    assert games[0].timeline[111].mission == Missions.NoMission
    assert games[0].timeline[111].role == (Roles.Civilian,)
    assert games[0].timeline[111].time == 10.7

    assert games[0].timeline[112].action_test == ActionTest.NoAT
    assert games[0].timeline[112].actor == "sniper"
    assert games[0].timeline[112].books == (None,)
    assert games[0].timeline[112].cast_name == (Characters.Disney,)
    assert games[0].timeline[112].category == TimelineCategory.SniperLights
    assert games[0].timeline[112].elapsed_time == 216.0
    assert games[0].timeline[112].event == "marked less suspicious."
    assert games[0].timeline[112].mission == Missions.NoMission
    assert games[0].timeline[112].role == (Roles.Civilian,)
    assert games[0].timeline[112].time == 9.0

    assert games[0].timeline[113].action_test == ActionTest.NoAT
    assert games[0].timeline[113].actor == "sniper"
    assert games[0].timeline[113].books == (None,)
    assert games[0].timeline[113].cast_name == (Characters.Salmon,)
    assert games[0].timeline[113].category == TimelineCategory.SniperLights
    assert games[0].timeline[113].elapsed_time == 216.38
    assert games[0].timeline[113].event == "marked less suspicious."
    assert games[0].timeline[113].mission == Missions.NoMission
    assert games[0].timeline[113].role == (Roles.Civilian,)
    assert games[0].timeline[113].time == 8.6

    assert games[0].timeline[114].action_test == ActionTest.NoAT
    assert games[0].timeline[114].actor == "sniper"
    assert games[0].timeline[114].books == (None,)
    assert games[0].timeline[114].cast_name == (Characters.Rocker,)
    assert games[0].timeline[114].category == TimelineCategory.SniperLights
    assert games[0].timeline[114].elapsed_time == 216.69
    assert games[0].timeline[114].event == "marked less suspicious."
    assert games[0].timeline[114].mission == Missions.NoMission
    assert games[0].timeline[114].role == (Roles.Civilian,)
    assert games[0].timeline[114].time == 8.3

    assert games[0].timeline[115].action_test == ActionTest.NoAT
    assert games[0].timeline[115].actor == "spy"
    assert games[0].timeline[115].books == (None,)
    assert games[0].timeline[115].cast_name == (None,)
    assert games[0].timeline[115].category == TimelineCategory.Conversation
    assert games[0].timeline[115].elapsed_time == 217.50
    assert games[0].timeline[115].event == "spy leaves conversation."
    assert games[0].timeline[115].mission == Missions.NoMission
    assert games[0].timeline[115].role == (None,)
    assert games[0].timeline[115].time == 7.5

    assert games[0].timeline[116].action_test == ActionTest.NoAT
    assert games[0].timeline[116].actor == "spy"
    assert games[0].timeline[116].books == (None,)
    assert games[0].timeline[116].cast_name == (Characters.Boots,)
    assert games[0].timeline[116].category == TimelineCategory.Conversation
    assert games[0].timeline[116].elapsed_time == 217.50
    assert games[0].timeline[116].event == "spy left conversation with double agent."
    assert games[0].timeline[116].mission == Missions.NoMission
    assert games[0].timeline[116].role == (Roles.DoubleAgent,)
    assert games[0].timeline[116].time == 7.5

    assert games[0].timeline[117].action_test == ActionTest.NoAT
    assert games[0].timeline[117].actor == "sniper"
    assert games[0].timeline[117].books == (None,)
    assert games[0].timeline[117].cast_name == (Characters.Irish,)
    assert games[0].timeline[117].category == TimelineCategory.SniperShot
    assert games[0].timeline[117].elapsed_time == 220.25
    assert games[0].timeline[117].event == "took shot."
    assert games[0].timeline[117].mission == Missions.NoMission
    assert games[0].timeline[117].role == (Roles.Spy,)
    assert games[0].timeline[117].time == 4.7

    assert games[0].timeline[118].action_test == ActionTest.NoAT
    assert games[0].timeline[118].actor == "game"
    assert games[0].timeline[118].books == (None,)
    assert games[0].timeline[118].cast_name == (Characters.Irish,)
    assert games[0].timeline[118].category == TimelineCategory.GameEnd
    assert games[0].timeline[118].elapsed_time == 223.81
    assert games[0].timeline[118].event == "sniper shot spy."
    assert games[0].timeline[118].mission == Missions.NoMission
    assert games[0].timeline[118].role == (Roles.Spy,)
    assert games[0].timeline[118].time == 1.1

    assert games[0].timeline.get_next_spy_action(games[0].timeline[118]) is None

    assert games[1].uuid == "vgAlD77AQw2XKTZq3H4NTg"
    assert games[1].timeline[0].action_test == ActionTest.NoAT
    assert games[1].timeline[0].actor == "spy"
    assert games[1].timeline[0].books == (None,)
    assert games[1].timeline[0].cast_name == (Characters.Queen,)
    assert games[1].timeline[0].category == TimelineCategory.Cast
    assert games[1].timeline[0].elapsed_time == 0.0
    assert games[1].timeline[0].event == "spy cast."
    assert games[1].timeline[0].mission == Missions.NoMission
    assert games[1].timeline[0].role == (Roles.Spy,)
    assert games[1].timeline[0].time == 225.0

    assert games[1].timeline[1].action_test == ActionTest.NoAT
    assert games[1].timeline[1].actor == "spy"
    assert games[1].timeline[1].books == (None,)
    assert games[1].timeline[1].cast_name == (Characters.Disney,)
    assert games[1].timeline[1].category == TimelineCategory.Cast
    assert games[1].timeline[1].elapsed_time == 0.0
    assert games[1].timeline[1].event == "ambassador cast."
    assert games[1].timeline[1].mission == Missions.NoMission
    assert games[1].timeline[1].role == (Roles.Ambassador,)
    assert games[1].timeline[1].time == 225.0

    assert games[1].timeline[2].action_test == ActionTest.NoAT
    assert games[1].timeline[2].actor == "spy"
    assert games[1].timeline[2].books == (None,)
    assert games[1].timeline[2].cast_name == (Characters.Wheels,)
    assert games[1].timeline[2].category == TimelineCategory.Cast
    assert games[1].timeline[2].elapsed_time == 0.0
    assert games[1].timeline[2].event == "double agent cast."
    assert games[1].timeline[2].mission == Missions.NoMission
    assert games[1].timeline[2].role == (Roles.DoubleAgent,)
    assert games[1].timeline[2].time == 225.0

    assert games[1].timeline[3].action_test == ActionTest.NoAT
    assert games[1].timeline[3].actor == "spy"
    assert games[1].timeline[3].books == (None,)
    assert games[1].timeline[3].cast_name == (Characters.Bling,)
    assert games[1].timeline[3].category == TimelineCategory.Cast
    assert games[1].timeline[3].elapsed_time == 0.0
    assert games[1].timeline[3].event == "suspected double agent cast."
    assert games[1].timeline[3].mission == Missions.NoMission
    assert games[1].timeline[3].role == (Roles.SuspectedDoubleAgent,)
    assert games[1].timeline[3].time == 225.0

    assert games[1].timeline[4].action_test == ActionTest.NoAT
    assert games[1].timeline[4].actor == "spy"
    assert games[1].timeline[4].books == (None,)
    assert games[1].timeline[4].cast_name == (Characters.Irish,)
    assert games[1].timeline[4].category == TimelineCategory.Cast
    assert games[1].timeline[4].elapsed_time == 0.0
    assert games[1].timeline[4].event == "seduction target cast."
    assert games[1].timeline[4].mission == Missions.NoMission
    assert games[1].timeline[4].role == (Roles.SeductionTarget,)
    assert games[1].timeline[4].time == 225.0

    assert games[1].timeline[5].action_test == ActionTest.NoAT
    assert games[1].timeline[5].actor == "spy"
    assert games[1].timeline[5].books == (None,)
    assert games[1].timeline[5].cast_name == (Characters.Boots,)
    assert games[1].timeline[5].category == TimelineCategory.Cast
    assert games[1].timeline[5].elapsed_time == 0.0
    assert games[1].timeline[5].event == "civilian cast."
    assert games[1].timeline[5].mission == Missions.NoMission
    assert games[1].timeline[5].role == (Roles.Civilian,)
    assert games[1].timeline[5].time == 225.0

    assert games[1].timeline[6].action_test == ActionTest.NoAT
    assert games[1].timeline[6].actor == "spy"
    assert games[1].timeline[6].books == (None,)
    assert games[1].timeline[6].cast_name == (Characters.Sikh,)
    assert games[1].timeline[6].category == TimelineCategory.Cast
    assert games[1].timeline[6].elapsed_time == 0.0
    assert games[1].timeline[6].event == "civilian cast."
    assert games[1].timeline[6].mission == Missions.NoMission
    assert games[1].timeline[6].role == (Roles.Civilian,)
    assert games[1].timeline[6].time == 225.0

    assert games[1].timeline[7].action_test == ActionTest.NoAT
    assert games[1].timeline[7].actor == "spy"
    assert games[1].timeline[7].books == (None,)
    assert games[1].timeline[7].cast_name == (Characters.Rocker,)
    assert games[1].timeline[7].category == TimelineCategory.Cast
    assert games[1].timeline[7].elapsed_time == 0.0
    assert games[1].timeline[7].event == "civilian cast."
    assert games[1].timeline[7].mission == Missions.NoMission
    assert games[1].timeline[7].role == (Roles.Civilian,)
    assert games[1].timeline[7].time == 225.0

    assert games[1].timeline[8].action_test == ActionTest.NoAT
    assert games[1].timeline[8].actor == "spy"
    assert games[1].timeline[8].books == (None,)
    assert games[1].timeline[8].cast_name == (Characters.Helen,)
    assert games[1].timeline[8].category == TimelineCategory.Cast
    assert games[1].timeline[8].elapsed_time == 0.0
    assert games[1].timeline[8].event == "civilian cast."
    assert games[1].timeline[8].mission == Missions.NoMission
    assert games[1].timeline[8].role == (Roles.Civilian,)
    assert games[1].timeline[8].time == 225.0

    assert games[1].timeline[9].action_test == ActionTest.NoAT
    assert games[1].timeline[9].actor == "spy"
    assert games[1].timeline[9].books == (None,)
    assert games[1].timeline[9].cast_name == (Characters.Alice,)
    assert games[1].timeline[9].category == TimelineCategory.Cast
    assert games[1].timeline[9].elapsed_time == 0.0
    assert games[1].timeline[9].event == "civilian cast."
    assert games[1].timeline[9].mission == Missions.NoMission
    assert games[1].timeline[9].role == (Roles.Civilian,)
    assert games[1].timeline[9].time == 225.0

    assert games[1].timeline[10].action_test == ActionTest.NoAT
    assert games[1].timeline[10].actor == "spy"
    assert games[1].timeline[10].books == (None,)
    assert games[1].timeline[10].cast_name == (Characters.Oprah,)
    assert games[1].timeline[10].category == TimelineCategory.Cast
    assert games[1].timeline[10].elapsed_time == 0.0
    assert games[1].timeline[10].event == "civilian cast."
    assert games[1].timeline[10].mission == Missions.NoMission
    assert games[1].timeline[10].role == (Roles.Civilian,)
    assert games[1].timeline[10].time == 225.0

    assert games[1].timeline[11].action_test == ActionTest.NoAT
    assert games[1].timeline[11].actor == "spy"
    assert games[1].timeline[11].books == (None,)
    assert games[1].timeline[11].cast_name == (Characters.Morgan,)
    assert games[1].timeline[11].category == TimelineCategory.Cast
    assert games[1].timeline[11].elapsed_time == 0.0
    assert games[1].timeline[11].event == "civilian cast."
    assert games[1].timeline[11].mission == Missions.NoMission
    assert games[1].timeline[11].role == (Roles.Civilian,)
    assert games[1].timeline[11].time == 225.0

    assert games[1].timeline[12].action_test == ActionTest.NoAT
    assert games[1].timeline[12].actor == "spy"
    assert games[1].timeline[12].books == (None,)
    assert games[1].timeline[12].cast_name == (Characters.Plain,)
    assert games[1].timeline[12].category == TimelineCategory.Cast
    assert games[1].timeline[12].elapsed_time == 0.0
    assert games[1].timeline[12].event == "civilian cast."
    assert games[1].timeline[12].mission == Missions.NoMission
    assert games[1].timeline[12].role == (Roles.Civilian,)
    assert games[1].timeline[12].time == 225.0

    assert games[1].timeline[13].action_test == ActionTest.NoAT
    assert games[1].timeline[13].actor == "spy"
    assert games[1].timeline[13].books == (None,)
    assert games[1].timeline[13].cast_name == (Characters.Sari,)
    assert games[1].timeline[13].category == TimelineCategory.Cast
    assert games[1].timeline[13].elapsed_time == 0.0
    assert games[1].timeline[13].event == "civilian cast."
    assert games[1].timeline[13].mission == Missions.NoMission
    assert games[1].timeline[13].role == (Roles.Civilian,)
    assert games[1].timeline[13].time == 225.0

    assert games[1].timeline[14].action_test == ActionTest.NoAT
    assert games[1].timeline[14].actor == "spy"
    assert games[1].timeline[14].books == (None,)
    assert games[1].timeline[14].cast_name == (Characters.Taft,)
    assert games[1].timeline[14].category == TimelineCategory.Cast
    assert games[1].timeline[14].elapsed_time == 0.0
    assert games[1].timeline[14].event == "civilian cast."
    assert games[1].timeline[14].mission == Missions.NoMission
    assert games[1].timeline[14].role == (Roles.Civilian,)
    assert games[1].timeline[14].time == 225.0

    assert games[1].timeline[15].action_test == ActionTest.NoAT
    assert games[1].timeline[15].actor == "spy"
    assert games[1].timeline[15].books == (None,)
    assert games[1].timeline[15].cast_name == (Characters.Carlos,)
    assert games[1].timeline[15].category == TimelineCategory.Cast
    assert games[1].timeline[15].elapsed_time == 0.0
    assert games[1].timeline[15].event == "civilian cast."
    assert games[1].timeline[15].mission == Missions.NoMission
    assert games[1].timeline[15].role == (Roles.Civilian,)
    assert games[1].timeline[15].time == 225.0

    assert games[1].timeline[16].action_test == ActionTest.NoAT
    assert games[1].timeline[16].actor == "spy"
    assert games[1].timeline[16].books == (None,)
    assert games[1].timeline[16].cast_name == (Characters.Smallman,)
    assert games[1].timeline[16].category == TimelineCategory.Cast
    assert games[1].timeline[16].elapsed_time == 0.0
    assert games[1].timeline[16].event == "civilian cast."
    assert games[1].timeline[16].mission == Missions.NoMission
    assert games[1].timeline[16].role == (Roles.Civilian,)
    assert games[1].timeline[16].time == 225.0

    assert games[1].timeline[17].action_test == ActionTest.NoAT
    assert games[1].timeline[17].actor == "spy"
    assert games[1].timeline[17].books == (None,)
    assert games[1].timeline[17].cast_name == (Characters.Teal,)
    assert games[1].timeline[17].category == TimelineCategory.Cast
    assert games[1].timeline[17].elapsed_time == 0.0
    assert games[1].timeline[17].event == "civilian cast."
    assert games[1].timeline[17].mission == Missions.NoMission
    assert games[1].timeline[17].role == (Roles.Civilian,)
    assert games[1].timeline[17].time == 225.0

    assert games[1].timeline[18].action_test == ActionTest.NoAT
    assert games[1].timeline[18].actor == "spy"
    assert games[1].timeline[18].books == (None,)
    assert games[1].timeline[18].cast_name == (Characters.General,)
    assert games[1].timeline[18].category == TimelineCategory.Cast
    assert games[1].timeline[18].elapsed_time == 0.0
    assert games[1].timeline[18].event == "civilian cast."
    assert games[1].timeline[18].mission == Missions.NoMission
    assert games[1].timeline[18].role == (Roles.Civilian,)
    assert games[1].timeline[18].time == 225.0

    assert games[1].timeline[19].action_test == ActionTest.NoAT
    assert games[1].timeline[19].actor == "spy"
    assert games[1].timeline[19].books == (None,)
    assert games[1].timeline[19].cast_name == (Characters.Duke,)
    assert games[1].timeline[19].category == TimelineCategory.Cast
    assert games[1].timeline[19].elapsed_time == 0.0
    assert games[1].timeline[19].event == "civilian cast."
    assert games[1].timeline[19].mission == Missions.NoMission
    assert games[1].timeline[19].role == (Roles.Civilian,)
    assert games[1].timeline[19].time == 225.0

    assert games[1].timeline[20].action_test == ActionTest.NoAT
    assert games[1].timeline[20].actor == "spy"
    assert games[1].timeline[20].books == (None,)
    assert games[1].timeline[20].cast_name == (Characters.Salmon,)
    assert games[1].timeline[20].category == TimelineCategory.Cast
    assert games[1].timeline[20].elapsed_time == 0.0
    assert games[1].timeline[20].event == "civilian cast."
    assert games[1].timeline[20].mission == Missions.NoMission
    assert games[1].timeline[20].role == (Roles.Civilian,)
    assert games[1].timeline[20].time == 225.0

    assert games[1].timeline[21].action_test == ActionTest.NoAT
    assert games[1].timeline[21].actor == "spy"
    assert games[1].timeline[21].books == (None,)
    assert games[1].timeline[21].cast_name == (None,)
    assert games[1].timeline[21].category == TimelineCategory.MissionSelected
    assert games[1].timeline[21].elapsed_time == 0.0
    assert games[1].timeline[21].event == "bug ambassador selected."
    assert games[1].timeline[21].mission == Missions.Bug
    assert games[1].timeline[21].role == (None,)
    assert games[1].timeline[21].time == 225.0

    assert games[1].timeline[22].action_test == ActionTest.NoAT
    assert games[1].timeline[22].actor == "spy"
    assert games[1].timeline[22].books == (None,)
    assert games[1].timeline[22].cast_name == (None,)
    assert games[1].timeline[22].category == TimelineCategory.MissionSelected
    assert games[1].timeline[22].elapsed_time == 0.0
    assert games[1].timeline[22].event == "contact double agent selected."
    assert games[1].timeline[22].mission == Missions.Contact
    assert games[1].timeline[22].role == (None,)
    assert games[1].timeline[22].time == 225.0

    assert games[1].timeline[23].action_test == ActionTest.NoAT
    assert games[1].timeline[23].actor == "spy"
    assert games[1].timeline[23].books == (None,)
    assert games[1].timeline[23].cast_name == (None,)
    assert games[1].timeline[23].category == TimelineCategory.MissionSelected
    assert games[1].timeline[23].elapsed_time == 0.0
    assert games[1].timeline[23].event == "transfer microfilm selected."
    assert games[1].timeline[23].mission == Missions.Transfer
    assert games[1].timeline[23].role == (None,)
    assert games[1].timeline[23].time == 225.0

    assert games[1].timeline[24].action_test == ActionTest.NoAT
    assert games[1].timeline[24].actor == "spy"
    assert games[1].timeline[24].books == (None,)
    assert games[1].timeline[24].cast_name == (None,)
    assert games[1].timeline[24].category == TimelineCategory.MissionSelected
    assert games[1].timeline[24].elapsed_time == 0.0
    assert games[1].timeline[24].event == "swap statue selected."
    assert games[1].timeline[24].mission == Missions.Swap
    assert games[1].timeline[24].role == (None,)
    assert games[1].timeline[24].time == 225.0

    assert games[1].timeline[25].action_test == ActionTest.NoAT
    assert games[1].timeline[25].actor == "spy"
    assert games[1].timeline[25].books == (None,)
    assert games[1].timeline[25].cast_name == (None,)
    assert games[1].timeline[25].category == TimelineCategory.MissionSelected
    assert games[1].timeline[25].elapsed_time == 0.0
    assert games[1].timeline[25].event == "inspect 3 statues selected."
    assert games[1].timeline[25].mission == Missions.Inspect
    assert games[1].timeline[25].role == (None,)
    assert games[1].timeline[25].time == 225.0

    assert games[1].timeline[26].action_test == ActionTest.NoAT
    assert games[1].timeline[26].actor == "spy"
    assert games[1].timeline[26].books == (None,)
    assert games[1].timeline[26].cast_name == (None,)
    assert games[1].timeline[26].category == TimelineCategory.MissionSelected
    assert games[1].timeline[26].elapsed_time == 0.0
    assert games[1].timeline[26].event == "seduce target selected."
    assert games[1].timeline[26].mission == Missions.Seduce
    assert games[1].timeline[26].role == (None,)
    assert games[1].timeline[26].time == 225.0

    assert games[1].timeline[27].action_test == ActionTest.NoAT
    assert games[1].timeline[27].actor == "spy"
    assert games[1].timeline[27].books == (None,)
    assert games[1].timeline[27].cast_name == (None,)
    assert games[1].timeline[27].category == TimelineCategory.MissionSelected
    assert games[1].timeline[27].elapsed_time == 0.0
    assert games[1].timeline[27].event == "purloin guest list selected."
    assert games[1].timeline[27].mission == Missions.Purloin
    assert games[1].timeline[27].role == (None,)
    assert games[1].timeline[27].time == 225.0

    assert games[1].timeline[28].action_test == ActionTest.NoAT
    assert games[1].timeline[28].actor == "spy"
    assert games[1].timeline[28].books == (None,)
    assert games[1].timeline[28].cast_name == (None,)
    assert games[1].timeline[28].category == TimelineCategory.MissionSelected
    assert games[1].timeline[28].elapsed_time == 0.0
    assert games[1].timeline[28].event == "fingerprint ambassador selected."
    assert games[1].timeline[28].mission == Missions.Fingerprint
    assert games[1].timeline[28].role == (None,)
    assert games[1].timeline[28].time == 225.0

    assert games[1].timeline[29].action_test == ActionTest.NoAT
    assert games[1].timeline[29].actor == "spy"
    assert games[1].timeline[29].books == (None,)
    assert games[1].timeline[29].cast_name == (None,)
    assert games[1].timeline[29].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[29].elapsed_time == 0.0
    assert games[1].timeline[29].event == "bug ambassador enabled."
    assert games[1].timeline[29].mission == Missions.Bug
    assert games[1].timeline[29].role == (None,)
    assert games[1].timeline[29].time == 225.0

    assert games[1].timeline[30].action_test == ActionTest.NoAT
    assert games[1].timeline[30].actor == "spy"
    assert games[1].timeline[30].books == (None,)
    assert games[1].timeline[30].cast_name == (None,)
    assert games[1].timeline[30].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[30].elapsed_time == 0.0
    assert games[1].timeline[30].event == "contact double agent enabled."
    assert games[1].timeline[30].mission == Missions.Contact
    assert games[1].timeline[30].role == (None,)
    assert games[1].timeline[30].time == 225.0

    assert games[1].timeline[31].action_test == ActionTest.NoAT
    assert games[1].timeline[31].actor == "spy"
    assert games[1].timeline[31].books == (None,)
    assert games[1].timeline[31].cast_name == (None,)
    assert games[1].timeline[31].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[31].elapsed_time == 0.0
    assert games[1].timeline[31].event == "transfer microfilm enabled."
    assert games[1].timeline[31].mission == Missions.Transfer
    assert games[1].timeline[31].role == (None,)
    assert games[1].timeline[31].time == 225.0

    assert games[1].timeline[32].action_test == ActionTest.NoAT
    assert games[1].timeline[32].actor == "spy"
    assert games[1].timeline[32].books == (None,)
    assert games[1].timeline[32].cast_name == (None,)
    assert games[1].timeline[32].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[32].elapsed_time == 0.0
    assert games[1].timeline[32].event == "swap statue enabled."
    assert games[1].timeline[32].mission == Missions.Swap
    assert games[1].timeline[32].role == (None,)
    assert games[1].timeline[32].time == 225.0

    assert games[1].timeline[33].action_test == ActionTest.NoAT
    assert games[1].timeline[33].actor == "spy"
    assert games[1].timeline[33].books == (None,)
    assert games[1].timeline[33].cast_name == (None,)
    assert games[1].timeline[33].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[33].elapsed_time == 0.0
    assert games[1].timeline[33].event == "inspect 3 statues enabled."
    assert games[1].timeline[33].mission == Missions.Inspect
    assert games[1].timeline[33].role == (None,)
    assert games[1].timeline[33].time == 225.0

    assert games[1].timeline[34].action_test == ActionTest.NoAT
    assert games[1].timeline[34].actor == "spy"
    assert games[1].timeline[34].books == (None,)
    assert games[1].timeline[34].cast_name == (None,)
    assert games[1].timeline[34].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[34].elapsed_time == 0.0
    assert games[1].timeline[34].event == "seduce target enabled."
    assert games[1].timeline[34].mission == Missions.Seduce
    assert games[1].timeline[34].role == (None,)
    assert games[1].timeline[34].time == 225.0

    assert games[1].timeline[35].action_test == ActionTest.NoAT
    assert games[1].timeline[35].actor == "spy"
    assert games[1].timeline[35].books == (None,)
    assert games[1].timeline[35].cast_name == (None,)
    assert games[1].timeline[35].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[35].elapsed_time == 0.0
    assert games[1].timeline[35].event == "purloin guest list enabled."
    assert games[1].timeline[35].mission == Missions.Purloin
    assert games[1].timeline[35].role == (None,)
    assert games[1].timeline[35].time == 225.0

    assert games[1].timeline[36].action_test == ActionTest.NoAT
    assert games[1].timeline[36].actor == "spy"
    assert games[1].timeline[36].books == (None,)
    assert games[1].timeline[36].cast_name == (None,)
    assert games[1].timeline[36].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[36].elapsed_time == 0.0
    assert games[1].timeline[36].event == "fingerprint ambassador enabled."
    assert games[1].timeline[36].mission == Missions.Fingerprint
    assert games[1].timeline[36].role == (None,)
    assert games[1].timeline[36].time == 225.0

    assert games[1].timeline[37].action_test == ActionTest.NoAT
    assert games[1].timeline[37].actor == "game"
    assert games[1].timeline[37].books == (None,)
    assert games[1].timeline[37].cast_name == (None,)
    assert games[1].timeline[37].category == TimelineCategory.GameStart
    assert games[1].timeline[37].elapsed_time == 0.0
    assert games[1].timeline[37].event == "game started."
    assert games[1].timeline[37].mission == Missions.NoMission
    assert games[1].timeline[37].role == (None,)
    assert games[1].timeline[37].time == 225.0

    assert games[1].timeline[38].action_test == ActionTest.NoAT
    assert games[1].timeline[38].actor == "spy"
    assert games[1].timeline[38].books == (None,)
    assert games[1].timeline[38].cast_name == (None,)
    assert games[1].timeline[38].category == TimelineCategory.NoCategory
    assert games[1].timeline[38].elapsed_time == 1.31
    assert games[1].timeline[38].event == "spy player takes control from ai."
    assert games[1].timeline[38].mission == Missions.NoMission
    assert games[1].timeline[38].role == (None,)
    assert games[1].timeline[38].time == 223.6

    assert games[1].timeline[39].action_test == ActionTest.NoAT
    assert games[1].timeline[39].actor == "sniper"
    assert games[1].timeline[39].books == (None,)
    assert games[1].timeline[39].cast_name == (Characters.Disney,)
    assert games[1].timeline[39].category == TimelineCategory.SniperLights
    assert games[1].timeline[39].elapsed_time == 9.69
    assert games[1].timeline[39].event == "marked suspicious."
    assert games[1].timeline[39].mission == Missions.NoMission
    assert games[1].timeline[39].role == (Roles.Ambassador,)
    assert games[1].timeline[39].time == 215.3

    assert games[1].timeline[40].action_test == ActionTest.NoAT
    assert games[1].timeline[40].actor == "sniper"
    assert games[1].timeline[40].books == (None,)
    assert games[1].timeline[40].cast_name == (Characters.Toby,)
    assert games[1].timeline[40].category == TimelineCategory.SniperLights
    assert games[1].timeline[40].elapsed_time == 10.81
    assert games[1].timeline[40].event == "marked suspicious."
    assert games[1].timeline[40].mission == Missions.NoMission
    assert games[1].timeline[40].role == (Roles.Staff,)
    assert games[1].timeline[40].time == 214.1

    assert games[1].timeline[41].action_test == ActionTest.NoAT
    assert games[1].timeline[41].actor == "sniper"
    assert games[1].timeline[41].books == (None,)
    assert games[1].timeline[41].cast_name == (Characters.Sikh,)
    assert games[1].timeline[41].category == TimelineCategory.SniperLights
    assert games[1].timeline[41].elapsed_time == 11.44
    assert games[1].timeline[41].event == "marked suspicious."
    assert games[1].timeline[41].mission == Missions.NoMission
    assert games[1].timeline[41].role == (Roles.Civilian,)
    assert games[1].timeline[41].time == 213.5

    assert games[1].timeline[42].action_test == ActionTest.NoAT
    assert games[1].timeline[42].actor == "sniper"
    assert games[1].timeline[42].books == (None,)
    assert games[1].timeline[42].cast_name == (Characters.Duke,)
    assert games[1].timeline[42].category == TimelineCategory.SniperLights
    assert games[1].timeline[42].elapsed_time == 12.25
    assert games[1].timeline[42].event == "marked suspicious."
    assert games[1].timeline[42].mission == Missions.NoMission
    assert games[1].timeline[42].role == (Roles.Civilian,)
    assert games[1].timeline[42].time == 212.7

    assert games[1].timeline[43].action_test == ActionTest.NoAT
    assert games[1].timeline[43].actor == "spy"
    assert games[1].timeline[43].books == (None,)
    assert games[1].timeline[43].cast_name == (Characters.Queen,)
    assert games[1].timeline[43].category == TimelineCategory.Drinks
    assert games[1].timeline[43].elapsed_time == 12.63
    assert games[1].timeline[43].event == "took last sip of drink."
    assert games[1].timeline[43].mission == Missions.NoMission
    assert games[1].timeline[43].role == (Roles.Spy,)
    assert games[1].timeline[43].time == 212.3

    assert games[1].timeline[44].action_test == ActionTest.NoAT
    assert games[1].timeline[44].actor == "sniper"
    assert games[1].timeline[44].books == (None,)
    assert games[1].timeline[44].cast_name == (Characters.Bling,)
    assert games[1].timeline[44].category == TimelineCategory.SniperLights
    assert games[1].timeline[44].elapsed_time == 16.00
    assert games[1].timeline[44].event == "marked less suspicious."
    assert games[1].timeline[44].mission == Missions.NoMission
    assert games[1].timeline[44].role == (Roles.SuspectedDoubleAgent,)
    assert games[1].timeline[44].time == 209.0

    assert games[1].timeline[45].action_test == ActionTest.NoAT
    assert games[1].timeline[45].actor == "spy"
    assert games[1].timeline[45].books == (None,)
    assert games[1].timeline[45].cast_name == (None,)
    assert games[1].timeline[45].category == TimelineCategory.Conversation
    assert games[1].timeline[45].elapsed_time == 22.69
    assert games[1].timeline[45].event == "spy enters conversation."
    assert games[1].timeline[45].mission == Missions.NoMission
    assert games[1].timeline[45].role == (None,)
    assert games[1].timeline[45].time == 202.3

    assert games[1].timeline[46].action_test == ActionTest.NoAT
    assert games[1].timeline[46].actor == "sniper"
    assert games[1].timeline[46].books == (None,)
    assert games[1].timeline[46].cast_name == (Characters.Sari,)
    assert games[1].timeline[46].category == TimelineCategory.SniperLights
    assert games[1].timeline[46].elapsed_time == 27.69
    assert games[1].timeline[46].event == "marked suspicious."
    assert games[1].timeline[46].mission == Missions.NoMission
    assert games[1].timeline[46].role == (Roles.Civilian,)
    assert games[1].timeline[46].time == 197.3

    assert games[1].timeline[47].action_test == ActionTest.NoAT
    assert games[1].timeline[47].actor == "spy"
    assert games[1].timeline[47].books == (None,)
    assert games[1].timeline[47].cast_name == (None,)
    assert games[1].timeline[47].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[47].elapsed_time == 28.31
    assert games[1].timeline[47].event == "action triggered: seduce target"
    assert games[1].timeline[47].mission == Missions.Seduce
    assert games[1].timeline[47].role == (None,)
    assert games[1].timeline[47].time == 196.6

    assert games[1].timeline[48].action_test == ActionTest.NoAT
    assert games[1].timeline[48].actor == "spy"
    assert games[1].timeline[48].books == (None,)
    assert games[1].timeline[48].cast_name == (Characters.Irish,)
    assert games[1].timeline[48].category == TimelineCategory.NoCategory
    assert games[1].timeline[48].elapsed_time == 28.31
    assert games[1].timeline[48].event == "begin flirtation with seduction target."
    assert games[1].timeline[48].mission == Missions.Seduce
    assert games[1].timeline[48].role == (Roles.SeductionTarget,)
    assert games[1].timeline[48].time == 196.6

    assert games[1].timeline[49].action_test == ActionTest.Green
    assert games[1].timeline[49].actor == "spy"
    assert games[1].timeline[49].books == (None,)
    assert games[1].timeline[49].cast_name == (None,)
    assert games[1].timeline[49].category == TimelineCategory.ActionTest
    assert games[1].timeline[49].elapsed_time == 29.25
    assert games[1].timeline[49].event == "action test green: seduce target"
    assert games[1].timeline[49].mission == Missions.Seduce
    assert games[1].timeline[49].role == (None,)
    assert games[1].timeline[49].time == 195.7

    assert games[1].timeline[50].action_test == ActionTest.NoAT
    assert games[1].timeline[50].actor == "spy"
    assert games[1].timeline[50].books == (None,)
    assert games[1].timeline[50].cast_name == (Characters.Irish,)
    assert games[1].timeline[50].category == TimelineCategory.MissionPartial
    assert games[1].timeline[50].elapsed_time == 29.25
    assert games[1].timeline[50].event == "flirt with seduction target: 51%"
    assert games[1].timeline[50].mission == Missions.Seduce
    assert games[1].timeline[50].role == (Roles.SeductionTarget,)
    assert games[1].timeline[50].time == 195.7

    assert games[1].timeline[51].action_test == ActionTest.NoAT
    assert games[1].timeline[51].actor == "sniper"
    assert games[1].timeline[51].books == (None,)
    assert games[1].timeline[51].cast_name == (Characters.Wheels,)
    assert games[1].timeline[51].category == TimelineCategory.SniperLights
    assert games[1].timeline[51].elapsed_time == 37.81
    assert games[1].timeline[51].event == "marked less suspicious."
    assert games[1].timeline[51].mission == Missions.NoMission
    assert games[1].timeline[51].role == (Roles.DoubleAgent,)
    assert games[1].timeline[51].time == 187.1

    assert games[1].timeline[52].action_test == ActionTest.NoAT
    assert games[1].timeline[52].actor == "spy"
    assert games[1].timeline[52].books == (None,)
    assert games[1].timeline[52].cast_name == (None,)
    assert games[1].timeline[52].category == TimelineCategory.Conversation
    assert games[1].timeline[52].elapsed_time == 40.63
    assert games[1].timeline[52].event == "spy leaves conversation."
    assert games[1].timeline[52].mission == Missions.NoMission
    assert games[1].timeline[52].role == (None,)
    assert games[1].timeline[52].time == 184.3

    assert games[1].timeline[53].action_test == ActionTest.NoAT
    assert games[1].timeline[53].actor == "spy"
    assert games[1].timeline[53].books == (None,)
    assert games[1].timeline[53].cast_name == (None,)
    assert games[1].timeline[53].category == TimelineCategory.NoCategory
    assert games[1].timeline[53].elapsed_time == 46.0
    assert games[1].timeline[53].event == "flirtation cooldown expired."
    assert games[1].timeline[53].mission == Missions.Seduce
    assert games[1].timeline[53].role == (None,)
    assert games[1].timeline[53].time == 179.0

    assert games[1].timeline[54].action_test == ActionTest.NoAT
    assert games[1].timeline[54].actor == "sniper"
    assert games[1].timeline[54].books == (None,)
    assert games[1].timeline[54].cast_name == (Characters.Damon,)
    assert games[1].timeline[54].category == TimelineCategory.SniperLights
    assert games[1].timeline[54].elapsed_time == 53.94
    assert games[1].timeline[54].event == "marked less suspicious."
    assert games[1].timeline[54].mission == Missions.NoMission
    assert games[1].timeline[54].role == (Roles.Staff,)
    assert games[1].timeline[54].time == 171.0

    assert games[1].timeline[55].action_test == ActionTest.NoAT
    assert games[1].timeline[55].actor == "spy"
    assert games[1].timeline[55].books == (None,)
    assert games[1].timeline[55].cast_name == (None,)
    assert (
        games[1].timeline[55].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Watch
    )
    assert games[1].timeline[55].elapsed_time == 59.5
    assert games[1].timeline[55].event == "action triggered: check watch"
    assert games[1].timeline[55].mission == Missions.NoMission
    assert games[1].timeline[55].role == (None,)
    assert games[1].timeline[55].time == 165.5

    assert games[1].timeline[56].action_test == ActionTest.NoAT
    assert games[1].timeline[56].actor == "spy"
    assert games[1].timeline[56].books == (None,)
    assert games[1].timeline[56].cast_name == (None,)
    assert (
        games[1].timeline[56].category
        == TimelineCategory.TimeAdd | TimelineCategory.Watch
    )
    assert games[1].timeline[56].elapsed_time == 59.5
    assert games[1].timeline[56].event == "watch checked to add time."
    assert games[1].timeline[56].mission == Missions.NoMission
    assert games[1].timeline[56].role == (None,)
    assert games[1].timeline[56].time == 165.5

    assert games[1].timeline[57].action_test == ActionTest.White
    assert games[1].timeline[57].actor == "spy"
    assert games[1].timeline[57].books == (None,)
    assert games[1].timeline[57].cast_name == (None,)
    assert (
        games[1].timeline[57].category
        == TimelineCategory.ActionTest
        | TimelineCategory.TimeAdd
        | TimelineCategory.Watch
    )
    assert games[1].timeline[57].elapsed_time == 60.50
    assert games[1].timeline[57].event == "action test white: check watch"
    assert games[1].timeline[57].mission == Missions.NoMission
    assert games[1].timeline[57].role == (None,)
    assert games[1].timeline[57].time == 164.4

    assert games[1].timeline[58].action_test == ActionTest.NoAT
    assert games[1].timeline[58].actor == "sniper"
    assert games[1].timeline[58].books == (None,)
    assert games[1].timeline[58].cast_name == (Characters.Alice,)
    assert games[1].timeline[58].category == TimelineCategory.SniperLights
    assert games[1].timeline[58].elapsed_time == 61.81
    assert games[1].timeline[58].event == "marked less suspicious."
    assert games[1].timeline[58].mission == Missions.NoMission
    assert games[1].timeline[58].role == (Roles.Civilian,)
    assert games[1].timeline[58].time == 163.1

    assert games[1].timeline[59].action_test == ActionTest.NoAT
    assert games[1].timeline[59].actor == "spy"
    assert games[1].timeline[59].books == (None,)
    assert games[1].timeline[59].cast_name == (None,)
    assert games[1].timeline[59].category == TimelineCategory.TimeAdd
    assert games[1].timeline[59].elapsed_time == 61.94
    assert games[1].timeline[59].event == "45 seconds added to match."
    assert games[1].timeline[59].mission == Missions.NoMission
    assert games[1].timeline[59].role == (None,)
    assert games[1].timeline[59].time == 163.0

    assert games[1].timeline[60].action_test == ActionTest.NoAT
    assert games[1].timeline[60].actor == "spy"
    assert games[1].timeline[60].books == (None,)
    assert games[1].timeline[60].cast_name == (None,)
    assert games[1].timeline[60].category == TimelineCategory.Conversation
    assert games[1].timeline[60].elapsed_time == 67.94
    assert games[1].timeline[60].event == "spy enters conversation."
    assert games[1].timeline[60].mission == Missions.NoMission
    assert games[1].timeline[60].role == (None,)
    assert games[1].timeline[60].time == 202.0

    assert games[1].timeline[61].action_test == ActionTest.NoAT
    assert games[1].timeline[61].actor == "spy"
    assert games[1].timeline[61].books == (None,)
    assert games[1].timeline[61].cast_name == (None,)
    assert games[1].timeline[61].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[61].elapsed_time == 71.75
    assert games[1].timeline[61].event == "action triggered: seduce target"
    assert games[1].timeline[61].mission == Missions.Seduce
    assert games[1].timeline[61].role == (None,)
    assert games[1].timeline[61].time == 198.2

    assert games[1].timeline[62].action_test == ActionTest.NoAT
    assert games[1].timeline[62].actor == "spy"
    assert games[1].timeline[62].books == (None,)
    assert games[1].timeline[62].cast_name == (Characters.Irish,)
    assert games[1].timeline[62].category == TimelineCategory.NoCategory
    assert games[1].timeline[62].elapsed_time == 71.75
    assert games[1].timeline[62].event == "begin flirtation with seduction target."
    assert games[1].timeline[62].mission == Missions.Seduce
    assert games[1].timeline[62].role == (Roles.SeductionTarget,)
    assert games[1].timeline[62].time == 198.2

    assert games[1].timeline[63].action_test == ActionTest.White
    assert games[1].timeline[63].actor == "spy"
    assert games[1].timeline[63].books == (None,)
    assert games[1].timeline[63].cast_name == (None,)
    assert games[1].timeline[63].category == TimelineCategory.ActionTest
    assert games[1].timeline[63].elapsed_time == 72.88
    assert games[1].timeline[63].event == "action test white: seduce target"
    assert games[1].timeline[63].mission == Missions.Seduce
    assert games[1].timeline[63].role == (None,)
    assert games[1].timeline[63].time == 197.1

    assert games[1].timeline[64].action_test == ActionTest.NoAT
    assert games[1].timeline[64].actor == "spy"
    assert games[1].timeline[64].books == (None,)
    assert games[1].timeline[64].cast_name == (Characters.Irish,)
    assert games[1].timeline[64].category == TimelineCategory.MissionPartial
    assert games[1].timeline[64].elapsed_time == 72.88
    assert games[1].timeline[64].event == "flirt with seduction target: 79%"
    assert games[1].timeline[64].mission == Missions.Seduce
    assert games[1].timeline[64].role == (Roles.SeductionTarget,)
    assert games[1].timeline[64].time == 197.1

    assert games[1].timeline[65].action_test == ActionTest.NoAT
    assert games[1].timeline[65].actor == "spy"
    assert games[1].timeline[65].books == (None,)
    assert games[1].timeline[65].cast_name == (None,)
    assert games[1].timeline[65].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[65].elapsed_time == 89.56
    assert games[1].timeline[65].event == "action triggered: bug ambassador"
    assert games[1].timeline[65].mission == Missions.Bug
    assert games[1].timeline[65].role == (None,)
    assert games[1].timeline[65].time == 180.4

    assert games[1].timeline[66].action_test == ActionTest.NoAT
    assert games[1].timeline[66].actor == "spy"
    assert games[1].timeline[66].books == (None,)
    assert games[1].timeline[66].cast_name == (Characters.Disney,)
    assert games[1].timeline[66].category == TimelineCategory.NoCategory
    assert games[1].timeline[66].elapsed_time == 89.56
    assert games[1].timeline[66].event == "begin planting bug while walking."
    assert games[1].timeline[66].mission == Missions.Bug
    assert games[1].timeline[66].role == (Roles.Ambassador,)
    assert games[1].timeline[66].time == 180.4

    assert games[1].timeline[67].action_test == ActionTest.NoAT
    assert games[1].timeline[67].actor == "spy"
    assert games[1].timeline[67].books == (None,)
    assert games[1].timeline[67].cast_name == (Characters.Disney,)
    assert games[1].timeline[67].category == TimelineCategory.NoCategory
    assert games[1].timeline[67].elapsed_time == 90.69
    assert games[1].timeline[67].event == "failed planting bug while walking."
    assert games[1].timeline[67].mission == Missions.Bug
    assert games[1].timeline[67].role == (Roles.Ambassador,)
    assert games[1].timeline[67].time == 179.3

    assert games[1].timeline[68].action_test == ActionTest.NoAT
    assert games[1].timeline[68].actor == "sniper"
    assert games[1].timeline[68].books == (None,)
    assert games[1].timeline[68].cast_name == (Characters.Carlos,)
    assert games[1].timeline[68].category == TimelineCategory.SniperLights
    assert games[1].timeline[68].elapsed_time == 91.56
    assert games[1].timeline[68].event == "marked less suspicious."
    assert games[1].timeline[68].mission == Missions.NoMission
    assert games[1].timeline[68].role == (Roles.Civilian,)
    assert games[1].timeline[68].time == 178.4

    assert games[1].timeline[69].action_test == ActionTest.NoAT
    assert games[1].timeline[69].actor == "spy"
    assert games[1].timeline[69].books == (None,)
    assert games[1].timeline[69].cast_name == (None,)
    assert games[1].timeline[69].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[69].elapsed_time == 100.00
    assert games[1].timeline[69].event == "action triggered: bug ambassador"
    assert games[1].timeline[69].mission == Missions.Bug
    assert games[1].timeline[69].role == (None,)
    assert games[1].timeline[69].time == 169.9

    assert games[1].timeline[70].action_test == ActionTest.NoAT
    assert games[1].timeline[70].actor == "spy"
    assert games[1].timeline[70].books == (None,)
    assert games[1].timeline[70].cast_name == (Characters.Disney,)
    assert games[1].timeline[70].category == TimelineCategory.NoCategory
    assert games[1].timeline[70].elapsed_time == 100.00
    assert games[1].timeline[70].event == "begin planting bug while standing."
    assert games[1].timeline[70].mission == Missions.Bug
    assert games[1].timeline[70].role == (Roles.Ambassador,)
    assert games[1].timeline[70].time == 169.9

    assert games[1].timeline[71].action_test == ActionTest.NoAT
    assert games[1].timeline[71].actor == "spy"
    assert games[1].timeline[71].books == (None,)
    assert games[1].timeline[71].cast_name == (Characters.Disney,)
    assert games[1].timeline[71].category == TimelineCategory.MissionComplete
    assert games[1].timeline[71].elapsed_time == 101.63
    assert games[1].timeline[71].event == "bugged ambassador while standing."
    assert games[1].timeline[71].mission == Missions.Bug
    assert games[1].timeline[71].role == (Roles.Ambassador,)
    assert games[1].timeline[71].time == 168.3

    assert games[1].timeline[72].action_test == ActionTest.NoAT
    assert games[1].timeline[72].actor == "sniper"
    assert games[1].timeline[72].books == (None,)
    assert games[1].timeline[72].cast_name == (Characters.Queen,)
    assert games[1].timeline[72].category == TimelineCategory.SniperShot
    assert games[1].timeline[72].elapsed_time == 103.88
    assert games[1].timeline[72].event == "took shot."
    assert games[1].timeline[72].mission == Missions.NoMission
    assert games[1].timeline[72].role == (Roles.Spy,)
    assert games[1].timeline[72].time == 166.1

    assert games[1].timeline[73].action_test == ActionTest.NoAT
    assert games[1].timeline[73].actor == "game"
    assert games[1].timeline[73].books == (None,)
    assert games[1].timeline[73].cast_name == (Characters.Queen,)
    assert games[1].timeline[73].category == TimelineCategory.GameEnd
    assert games[1].timeline[73].elapsed_time == 109.88
    assert games[1].timeline[73].event == "sniper shot spy."
    assert games[1].timeline[73].mission == Missions.NoMission
    assert games[1].timeline[73].role == (Roles.Spy,)
    assert games[1].timeline[73].time == 160.1

    assert games[1].timeline.get_next_spy_action(games[1].timeline[73]) is None

    assert games[2].uuid == "k8x3n_zfTtiw9FSS6rM13w"
    assert games[2].timeline[0].action_test == ActionTest.NoAT
    assert games[2].timeline[0].actor == "spy"
    assert games[2].timeline[0].books == (None,)
    assert games[2].timeline[0].cast_name == (Characters.General,)
    assert games[2].timeline[0].category == TimelineCategory.Cast
    assert games[2].timeline[0].elapsed_time == 0.0
    assert games[2].timeline[0].event == "spy cast."
    assert games[2].timeline[0].mission == Missions.NoMission
    assert games[2].timeline[0].role == (Roles.Spy,)
    assert games[2].timeline[0].time == 225.0

    assert games[2].timeline[1].action_test == ActionTest.NoAT
    assert games[2].timeline[1].actor == "spy"
    assert games[2].timeline[1].books == (None,)
    assert games[2].timeline[1].cast_name == (Characters.Wheels,)
    assert games[2].timeline[1].category == TimelineCategory.Cast
    assert games[2].timeline[1].elapsed_time == 0.0
    assert games[2].timeline[1].event == "ambassador cast."
    assert games[2].timeline[1].mission == Missions.NoMission
    assert games[2].timeline[1].role == (Roles.Ambassador,)
    assert games[2].timeline[1].time == 225.0

    assert games[2].timeline[2].action_test == ActionTest.NoAT
    assert games[2].timeline[2].actor == "spy"
    assert games[2].timeline[2].books == (None,)
    assert games[2].timeline[2].cast_name == (Characters.Queen,)
    assert games[2].timeline[2].category == TimelineCategory.Cast
    assert games[2].timeline[2].elapsed_time == 0.0
    assert games[2].timeline[2].event == "double agent cast."
    assert games[2].timeline[2].mission == Missions.NoMission
    assert games[2].timeline[2].role == (Roles.DoubleAgent,)
    assert games[2].timeline[2].time == 225.0

    assert games[2].timeline[3].action_test == ActionTest.NoAT
    assert games[2].timeline[3].actor == "spy"
    assert games[2].timeline[3].books == (None,)
    assert games[2].timeline[3].cast_name == (Characters.Morgan,)
    assert games[2].timeline[3].category == TimelineCategory.Cast
    assert games[2].timeline[3].elapsed_time == 0.0
    assert games[2].timeline[3].event == "suspected double agent cast."
    assert games[2].timeline[3].mission == Missions.NoMission
    assert games[2].timeline[3].role == (Roles.SuspectedDoubleAgent,)
    assert games[2].timeline[3].time == 225.0

    assert games[2].timeline[4].action_test == ActionTest.NoAT
    assert games[2].timeline[4].actor == "spy"
    assert games[2].timeline[4].books == (None,)
    assert games[2].timeline[4].cast_name == (Characters.Rocker,)
    assert games[2].timeline[4].category == TimelineCategory.Cast
    assert games[2].timeline[4].elapsed_time == 0.0
    assert games[2].timeline[4].event == "seduction target cast."
    assert games[2].timeline[4].mission == Missions.NoMission
    assert games[2].timeline[4].role == (Roles.SeductionTarget,)
    assert games[2].timeline[4].time == 225.0

    assert games[2].timeline[5].action_test == ActionTest.NoAT
    assert games[2].timeline[5].actor == "spy"
    assert games[2].timeline[5].books == (None,)
    assert games[2].timeline[5].cast_name == (Characters.Taft,)
    assert games[2].timeline[5].category == TimelineCategory.Cast
    assert games[2].timeline[5].elapsed_time == 0.0
    assert games[2].timeline[5].event == "civilian cast."
    assert games[2].timeline[5].mission == Missions.NoMission
    assert games[2].timeline[5].role == (Roles.Civilian,)
    assert games[2].timeline[5].time == 225.0

    assert games[2].timeline[6].action_test == ActionTest.NoAT
    assert games[2].timeline[6].actor == "spy"
    assert games[2].timeline[6].books == (None,)
    assert games[2].timeline[6].cast_name == (Characters.Oprah,)
    assert games[2].timeline[6].category == TimelineCategory.Cast
    assert games[2].timeline[6].elapsed_time == 0.0
    assert games[2].timeline[6].event == "civilian cast."
    assert games[2].timeline[6].mission == Missions.NoMission
    assert games[2].timeline[6].role == (Roles.Civilian,)
    assert games[2].timeline[6].time == 225.0

    assert games[2].timeline[7].action_test == ActionTest.NoAT
    assert games[2].timeline[7].actor == "spy"
    assert games[2].timeline[7].books == (None,)
    assert games[2].timeline[7].cast_name == (Characters.Bling,)
    assert games[2].timeline[7].category == TimelineCategory.Cast
    assert games[2].timeline[7].elapsed_time == 0.0
    assert games[2].timeline[7].event == "civilian cast."
    assert games[2].timeline[7].mission == Missions.NoMission
    assert games[2].timeline[7].role == (Roles.Civilian,)
    assert games[2].timeline[7].time == 225.0

    assert games[2].timeline[8].action_test == ActionTest.NoAT
    assert games[2].timeline[8].actor == "spy"
    assert games[2].timeline[8].books == (None,)
    assert games[2].timeline[8].cast_name == (Characters.Alice,)
    assert games[2].timeline[8].category == TimelineCategory.Cast
    assert games[2].timeline[8].elapsed_time == 0.0
    assert games[2].timeline[8].event == "civilian cast."
    assert games[2].timeline[8].mission == Missions.NoMission
    assert games[2].timeline[8].role == (Roles.Civilian,)
    assert games[2].timeline[8].time == 225.0

    assert games[2].timeline[9].action_test == ActionTest.NoAT
    assert games[2].timeline[9].actor == "spy"
    assert games[2].timeline[9].books == (None,)
    assert games[2].timeline[9].cast_name == (Characters.Duke,)
    assert games[2].timeline[9].category == TimelineCategory.Cast
    assert games[2].timeline[9].elapsed_time == 0.0
    assert games[2].timeline[9].event == "civilian cast."
    assert games[2].timeline[9].mission == Missions.NoMission
    assert games[2].timeline[9].role == (Roles.Civilian,)
    assert games[2].timeline[9].time == 225.0

    assert games[2].timeline[10].action_test == ActionTest.NoAT
    assert games[2].timeline[10].actor == "spy"
    assert games[2].timeline[10].books == (None,)
    assert games[2].timeline[10].cast_name == (Characters.Boots,)
    assert games[2].timeline[10].category == TimelineCategory.Cast
    assert games[2].timeline[10].elapsed_time == 0.0
    assert games[2].timeline[10].event == "civilian cast."
    assert games[2].timeline[10].mission == Missions.NoMission
    assert games[2].timeline[10].role == (Roles.Civilian,)
    assert games[2].timeline[10].time == 225.0

    assert games[2].timeline[11].action_test == ActionTest.NoAT
    assert games[2].timeline[11].actor == "spy"
    assert games[2].timeline[11].books == (None,)
    assert games[2].timeline[11].cast_name == (Characters.Teal,)
    assert games[2].timeline[11].category == TimelineCategory.Cast
    assert games[2].timeline[11].elapsed_time == 0.0
    assert games[2].timeline[11].event == "civilian cast."
    assert games[2].timeline[11].mission == Missions.NoMission
    assert games[2].timeline[11].role == (Roles.Civilian,)
    assert games[2].timeline[11].time == 225.0

    assert games[2].timeline[12].action_test == ActionTest.NoAT
    assert games[2].timeline[12].actor == "spy"
    assert games[2].timeline[12].books == (None,)
    assert games[2].timeline[12].cast_name == (Characters.Smallman,)
    assert games[2].timeline[12].category == TimelineCategory.Cast
    assert games[2].timeline[12].elapsed_time == 0.0
    assert games[2].timeline[12].event == "civilian cast."
    assert games[2].timeline[12].mission == Missions.NoMission
    assert games[2].timeline[12].role == (Roles.Civilian,)
    assert games[2].timeline[12].time == 225.0

    assert games[2].timeline[13].action_test == ActionTest.NoAT
    assert games[2].timeline[13].actor == "spy"
    assert games[2].timeline[13].books == (None,)
    assert games[2].timeline[13].cast_name == (Characters.Helen,)
    assert games[2].timeline[13].category == TimelineCategory.Cast
    assert games[2].timeline[13].elapsed_time == 0.0
    assert games[2].timeline[13].event == "civilian cast."
    assert games[2].timeline[13].mission == Missions.NoMission
    assert games[2].timeline[13].role == (Roles.Civilian,)
    assert games[2].timeline[13].time == 225.0

    assert games[2].timeline[14].action_test == ActionTest.NoAT
    assert games[2].timeline[14].actor == "spy"
    assert games[2].timeline[14].books == (None,)
    assert games[2].timeline[14].cast_name == (Characters.Carlos,)
    assert games[2].timeline[14].category == TimelineCategory.Cast
    assert games[2].timeline[14].elapsed_time == 0.0
    assert games[2].timeline[14].event == "civilian cast."
    assert games[2].timeline[14].mission == Missions.NoMission
    assert games[2].timeline[14].role == (Roles.Civilian,)
    assert games[2].timeline[14].time == 225.0

    assert games[2].timeline[15].action_test == ActionTest.NoAT
    assert games[2].timeline[15].actor == "spy"
    assert games[2].timeline[15].books == (None,)
    assert games[2].timeline[15].cast_name == (Characters.Disney,)
    assert games[2].timeline[15].category == TimelineCategory.Cast
    assert games[2].timeline[15].elapsed_time == 0.0
    assert games[2].timeline[15].event == "civilian cast."
    assert games[2].timeline[15].mission == Missions.NoMission
    assert games[2].timeline[15].role == (Roles.Civilian,)
    assert games[2].timeline[15].time == 225.0

    assert games[2].timeline[16].action_test == ActionTest.NoAT
    assert games[2].timeline[16].actor == "spy"
    assert games[2].timeline[16].books == (None,)
    assert games[2].timeline[16].cast_name == (Characters.Plain,)
    assert games[2].timeline[16].category == TimelineCategory.Cast
    assert games[2].timeline[16].elapsed_time == 0.0
    assert games[2].timeline[16].event == "civilian cast."
    assert games[2].timeline[16].mission == Missions.NoMission
    assert games[2].timeline[16].role == (Roles.Civilian,)
    assert games[2].timeline[16].time == 225.0

    assert games[2].timeline[17].action_test == ActionTest.NoAT
    assert games[2].timeline[17].actor == "spy"
    assert games[2].timeline[17].books == (None,)
    assert games[2].timeline[17].cast_name == (Characters.Irish,)
    assert games[2].timeline[17].category == TimelineCategory.Cast
    assert games[2].timeline[17].elapsed_time == 0.0
    assert games[2].timeline[17].event == "civilian cast."
    assert games[2].timeline[17].mission == Missions.NoMission
    assert games[2].timeline[17].role == (Roles.Civilian,)
    assert games[2].timeline[17].time == 225.0

    assert games[2].timeline[18].action_test == ActionTest.NoAT
    assert games[2].timeline[18].actor == "spy"
    assert games[2].timeline[18].books == (None,)
    assert games[2].timeline[18].cast_name == (Characters.Salmon,)
    assert games[2].timeline[18].category == TimelineCategory.Cast
    assert games[2].timeline[18].elapsed_time == 0.0
    assert games[2].timeline[18].event == "civilian cast."
    assert games[2].timeline[18].mission == Missions.NoMission
    assert games[2].timeline[18].role == (Roles.Civilian,)
    assert games[2].timeline[18].time == 225.0

    assert games[2].timeline[19].action_test == ActionTest.NoAT
    assert games[2].timeline[19].actor == "spy"
    assert games[2].timeline[19].books == (None,)
    assert games[2].timeline[19].cast_name == (Characters.Sari,)
    assert games[2].timeline[19].category == TimelineCategory.Cast
    assert games[2].timeline[19].elapsed_time == 0.0
    assert games[2].timeline[19].event == "civilian cast."
    assert games[2].timeline[19].mission == Missions.NoMission
    assert games[2].timeline[19].role == (Roles.Civilian,)
    assert games[2].timeline[19].time == 225.0

    assert games[2].timeline[20].action_test == ActionTest.NoAT
    assert games[2].timeline[20].actor == "spy"
    assert games[2].timeline[20].books == (None,)
    assert games[2].timeline[20].cast_name == (Characters.Sikh,)
    assert games[2].timeline[20].category == TimelineCategory.Cast
    assert games[2].timeline[20].elapsed_time == 0.0
    assert games[2].timeline[20].event == "civilian cast."
    assert games[2].timeline[20].mission == Missions.NoMission
    assert games[2].timeline[20].role == (Roles.Civilian,)
    assert games[2].timeline[20].time == 225.0

    assert games[2].timeline[21].action_test == ActionTest.NoAT
    assert games[2].timeline[21].actor == "spy"
    assert games[2].timeline[21].books == (None,)
    assert games[2].timeline[21].cast_name == (None,)
    assert games[2].timeline[21].category == TimelineCategory.MissionSelected
    assert games[2].timeline[21].elapsed_time == 0.0
    assert games[2].timeline[21].event == "bug ambassador selected."
    assert games[2].timeline[21].mission == Missions.Bug
    assert games[2].timeline[21].role == (None,)
    assert games[2].timeline[21].time == 225.0

    assert games[2].timeline[22].action_test == ActionTest.NoAT
    assert games[2].timeline[22].actor == "spy"
    assert games[2].timeline[22].books == (None,)
    assert games[2].timeline[22].cast_name == (None,)
    assert games[2].timeline[22].category == TimelineCategory.MissionSelected
    assert games[2].timeline[22].elapsed_time == 0.0
    assert games[2].timeline[22].event == "contact double agent selected."
    assert games[2].timeline[22].mission == Missions.Contact
    assert games[2].timeline[22].role == (None,)
    assert games[2].timeline[22].time == 225.0

    assert games[2].timeline[23].action_test == ActionTest.NoAT
    assert games[2].timeline[23].actor == "spy"
    assert games[2].timeline[23].books == (None,)
    assert games[2].timeline[23].cast_name == (None,)
    assert games[2].timeline[23].category == TimelineCategory.MissionSelected
    assert games[2].timeline[23].elapsed_time == 0.0
    assert games[2].timeline[23].event == "transfer microfilm selected."
    assert games[2].timeline[23].mission == Missions.Transfer
    assert games[2].timeline[23].role == (None,)
    assert games[2].timeline[23].time == 225.0

    assert games[2].timeline[24].action_test == ActionTest.NoAT
    assert games[2].timeline[24].actor == "spy"
    assert games[2].timeline[24].books == (None,)
    assert games[2].timeline[24].cast_name == (None,)
    assert games[2].timeline[24].category == TimelineCategory.MissionSelected
    assert games[2].timeline[24].elapsed_time == 0.0
    assert games[2].timeline[24].event == "swap statue selected."
    assert games[2].timeline[24].mission == Missions.Swap
    assert games[2].timeline[24].role == (None,)
    assert games[2].timeline[24].time == 225.0

    assert games[2].timeline[25].action_test == ActionTest.NoAT
    assert games[2].timeline[25].actor == "spy"
    assert games[2].timeline[25].books == (None,)
    assert games[2].timeline[25].cast_name == (None,)
    assert games[2].timeline[25].category == TimelineCategory.MissionSelected
    assert games[2].timeline[25].elapsed_time == 0.0
    assert games[2].timeline[25].event == "inspect 3 statues selected."
    assert games[2].timeline[25].mission == Missions.Inspect
    assert games[2].timeline[25].role == (None,)
    assert games[2].timeline[25].time == 225.0

    assert games[2].timeline[26].action_test == ActionTest.NoAT
    assert games[2].timeline[26].actor == "spy"
    assert games[2].timeline[26].books == (None,)
    assert games[2].timeline[26].cast_name == (None,)
    assert games[2].timeline[26].category == TimelineCategory.MissionSelected
    assert games[2].timeline[26].elapsed_time == 0.0
    assert games[2].timeline[26].event == "seduce target selected."
    assert games[2].timeline[26].mission == Missions.Seduce
    assert games[2].timeline[26].role == (None,)
    assert games[2].timeline[26].time == 225.0

    assert games[2].timeline[27].action_test == ActionTest.NoAT
    assert games[2].timeline[27].actor == "spy"
    assert games[2].timeline[27].books == (None,)
    assert games[2].timeline[27].cast_name == (None,)
    assert games[2].timeline[27].category == TimelineCategory.MissionSelected
    assert games[2].timeline[27].elapsed_time == 0.0
    assert games[2].timeline[27].event == "purloin guest list selected."
    assert games[2].timeline[27].mission == Missions.Purloin
    assert games[2].timeline[27].role == (None,)
    assert games[2].timeline[27].time == 225.0

    assert games[2].timeline[28].action_test == ActionTest.NoAT
    assert games[2].timeline[28].actor == "spy"
    assert games[2].timeline[28].books == (None,)
    assert games[2].timeline[28].cast_name == (None,)
    assert games[2].timeline[28].category == TimelineCategory.MissionSelected
    assert games[2].timeline[28].elapsed_time == 0.0
    assert games[2].timeline[28].event == "fingerprint ambassador selected."
    assert games[2].timeline[28].mission == Missions.Fingerprint
    assert games[2].timeline[28].role == (None,)
    assert games[2].timeline[28].time == 225.0

    assert games[2].timeline[29].action_test == ActionTest.NoAT
    assert games[2].timeline[29].actor == "spy"
    assert games[2].timeline[29].books == (None,)
    assert games[2].timeline[29].cast_name == (None,)
    assert games[2].timeline[29].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[29].elapsed_time == 0.0
    assert games[2].timeline[29].event == "bug ambassador enabled."
    assert games[2].timeline[29].mission == Missions.Bug
    assert games[2].timeline[29].role == (None,)
    assert games[2].timeline[29].time == 225.0

    assert games[2].timeline[30].action_test == ActionTest.NoAT
    assert games[2].timeline[30].actor == "spy"
    assert games[2].timeline[30].books == (None,)
    assert games[2].timeline[30].cast_name == (None,)
    assert games[2].timeline[30].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[30].elapsed_time == 0.0
    assert games[2].timeline[30].event == "contact double agent enabled."
    assert games[2].timeline[30].mission == Missions.Contact
    assert games[2].timeline[30].role == (None,)
    assert games[2].timeline[30].time == 225.0

    assert games[2].timeline[31].action_test == ActionTest.NoAT
    assert games[2].timeline[31].actor == "spy"
    assert games[2].timeline[31].books == (None,)
    assert games[2].timeline[31].cast_name == (None,)
    assert games[2].timeline[31].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[31].elapsed_time == 0.0
    assert games[2].timeline[31].event == "transfer microfilm enabled."
    assert games[2].timeline[31].mission == Missions.Transfer
    assert games[2].timeline[31].role == (None,)
    assert games[2].timeline[31].time == 225.0

    assert games[2].timeline[32].action_test == ActionTest.NoAT
    assert games[2].timeline[32].actor == "spy"
    assert games[2].timeline[32].books == (None,)
    assert games[2].timeline[32].cast_name == (None,)
    assert games[2].timeline[32].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[32].elapsed_time == 0.0
    assert games[2].timeline[32].event == "swap statue enabled."
    assert games[2].timeline[32].mission == Missions.Swap
    assert games[2].timeline[32].role == (None,)
    assert games[2].timeline[32].time == 225.0

    assert games[2].timeline[33].action_test == ActionTest.NoAT
    assert games[2].timeline[33].actor == "spy"
    assert games[2].timeline[33].books == (None,)
    assert games[2].timeline[33].cast_name == (None,)
    assert games[2].timeline[33].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[33].elapsed_time == 0.0
    assert games[2].timeline[33].event == "inspect 3 statues enabled."
    assert games[2].timeline[33].mission == Missions.Inspect
    assert games[2].timeline[33].role == (None,)
    assert games[2].timeline[33].time == 225.0

    assert games[2].timeline[34].action_test == ActionTest.NoAT
    assert games[2].timeline[34].actor == "spy"
    assert games[2].timeline[34].books == (None,)
    assert games[2].timeline[34].cast_name == (None,)
    assert games[2].timeline[34].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[34].elapsed_time == 0.0
    assert games[2].timeline[34].event == "seduce target enabled."
    assert games[2].timeline[34].mission == Missions.Seduce
    assert games[2].timeline[34].role == (None,)
    assert games[2].timeline[34].time == 225.0

    assert games[2].timeline[35].action_test == ActionTest.NoAT
    assert games[2].timeline[35].actor == "spy"
    assert games[2].timeline[35].books == (None,)
    assert games[2].timeline[35].cast_name == (None,)
    assert games[2].timeline[35].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[35].elapsed_time == 0.0
    assert games[2].timeline[35].event == "purloin guest list enabled."
    assert games[2].timeline[35].mission == Missions.Purloin
    assert games[2].timeline[35].role == (None,)
    assert games[2].timeline[35].time == 225.0

    assert games[2].timeline[36].action_test == ActionTest.NoAT
    assert games[2].timeline[36].actor == "spy"
    assert games[2].timeline[36].books == (None,)
    assert games[2].timeline[36].cast_name == (None,)
    assert games[2].timeline[36].category == TimelineCategory.MissionEnabled
    assert games[2].timeline[36].elapsed_time == 0.0
    assert games[2].timeline[36].event == "fingerprint ambassador enabled."
    assert games[2].timeline[36].mission == Missions.Fingerprint
    assert games[2].timeline[36].role == (None,)
    assert games[2].timeline[36].time == 225.0

    assert games[2].timeline[37].action_test == ActionTest.NoAT
    assert games[2].timeline[37].actor == "game"
    assert games[2].timeline[37].books == (None,)
    assert games[2].timeline[37].cast_name == (None,)
    assert games[2].timeline[37].category == TimelineCategory.GameStart
    assert games[2].timeline[37].elapsed_time == 0.0
    assert games[2].timeline[37].event == "game started."
    assert games[2].timeline[37].mission == Missions.NoMission
    assert games[2].timeline[37].role == (None,)
    assert games[2].timeline[37].time == 225.0

    assert games[2].timeline[38].action_test == ActionTest.NoAT
    assert games[2].timeline[38].actor == "sniper"
    assert games[2].timeline[38].books == (None,)
    assert games[2].timeline[38].cast_name == (Characters.Wheels,)
    assert games[2].timeline[38].category == TimelineCategory.SniperLights
    assert games[2].timeline[38].elapsed_time == 0.63
    assert games[2].timeline[38].event == "marked suspicious."
    assert games[2].timeline[38].mission == Missions.NoMission
    assert games[2].timeline[38].role == (Roles.Ambassador,)
    assert games[2].timeline[38].time == 224.3

    assert games[2].timeline[39].action_test == ActionTest.NoAT
    assert games[2].timeline[39].actor == "spy"
    assert games[2].timeline[39].books == (None,)
    assert games[2].timeline[39].cast_name == (None,)
    assert games[2].timeline[39].category == TimelineCategory.NoCategory
    assert games[2].timeline[39].elapsed_time == 0.81
    assert games[2].timeline[39].event == "spy player takes control from ai."
    assert games[2].timeline[39].mission == Missions.NoMission
    assert games[2].timeline[39].role == (None,)
    assert games[2].timeline[39].time == 224.1

    assert games[2].timeline[40].action_test == ActionTest.NoAT
    assert games[2].timeline[40].actor == "spy"
    assert games[2].timeline[40].books == (None,)
    assert games[2].timeline[40].cast_name == (None,)
    assert games[2].timeline[40].category == TimelineCategory.Conversation
    assert games[2].timeline[40].elapsed_time == 3.88
    assert games[2].timeline[40].event == "spy enters conversation."
    assert games[2].timeline[40].mission == Missions.NoMission
    assert games[2].timeline[40].role == (None,)
    assert games[2].timeline[40].time == 221.1

    assert games[2].timeline[41].action_test == ActionTest.NoAT
    assert games[2].timeline[41].actor == "sniper"
    assert games[2].timeline[41].books == (None,)
    assert games[2].timeline[41].cast_name == (Characters.Sikh,)
    assert games[2].timeline[41].category == TimelineCategory.SniperLights
    assert games[2].timeline[41].elapsed_time == 4.38
    assert games[2].timeline[41].event == "marked suspicious."
    assert games[2].timeline[41].mission == Missions.NoMission
    assert games[2].timeline[41].role == (Roles.Civilian,)
    assert games[2].timeline[41].time == 220.6

    assert games[2].timeline[42].action_test == ActionTest.NoAT
    assert games[2].timeline[42].actor == "spy"
    assert games[2].timeline[42].books == (None,)
    assert games[2].timeline[42].cast_name == (None,)
    assert games[2].timeline[42].category == TimelineCategory.ActionTriggered
    assert games[2].timeline[42].elapsed_time == 4.44
    assert games[2].timeline[42].event == "action triggered: seduce target"
    assert games[2].timeline[42].mission == Missions.Seduce
    assert games[2].timeline[42].role == (None,)
    assert games[2].timeline[42].time == 220.5

    assert games[2].timeline[43].action_test == ActionTest.NoAT
    assert games[2].timeline[43].actor == "spy"
    assert games[2].timeline[43].books == (None,)
    assert games[2].timeline[43].cast_name == (Characters.Rocker,)
    assert games[2].timeline[43].category == TimelineCategory.NoCategory
    assert games[2].timeline[43].elapsed_time == 4.44
    assert games[2].timeline[43].event == "begin flirtation with seduction target."
    assert games[2].timeline[43].mission == Missions.Seduce
    assert games[2].timeline[43].role == (Roles.SeductionTarget,)
    assert games[2].timeline[43].time == 220.5

    assert games[2].timeline[44].action_test == ActionTest.White
    assert games[2].timeline[44].actor == "spy"
    assert games[2].timeline[44].books == (None,)
    assert games[2].timeline[44].cast_name == (None,)
    assert games[2].timeline[44].category == TimelineCategory.ActionTest
    assert games[2].timeline[44].elapsed_time == 5.19
    assert games[2].timeline[44].event == "action test white: seduce target"
    assert games[2].timeline[44].mission == Missions.Seduce
    assert games[2].timeline[44].role == (None,)
    assert games[2].timeline[44].time == 219.8

    assert games[2].timeline[45].action_test == ActionTest.NoAT
    assert games[2].timeline[45].actor == "spy"
    assert games[2].timeline[45].books == (None,)
    assert games[2].timeline[45].cast_name == (Characters.Rocker,)
    assert games[2].timeline[45].category == TimelineCategory.MissionPartial
    assert games[2].timeline[45].elapsed_time == 5.19
    assert games[2].timeline[45].event == "flirt with seduction target: 34%"
    assert games[2].timeline[45].mission == Missions.Seduce
    assert games[2].timeline[45].role == (Roles.SeductionTarget,)
    assert games[2].timeline[45].time == 219.8

    assert games[2].timeline[46].action_test == ActionTest.NoAT
    assert games[2].timeline[46].actor == "sniper"
    assert games[2].timeline[46].books == (None,)
    assert games[2].timeline[46].cast_name == (Characters.Toby,)
    assert games[2].timeline[46].category == TimelineCategory.SniperLights
    assert games[2].timeline[46].elapsed_time == 6.63
    assert games[2].timeline[46].event == "marked suspicious."
    assert games[2].timeline[46].mission == Missions.NoMission
    assert games[2].timeline[46].role == (Roles.Staff,)
    assert games[2].timeline[46].time == 218.3

    assert games[2].timeline[47].action_test == ActionTest.NoAT
    assert games[2].timeline[47].actor == "sniper"
    assert games[2].timeline[47].books == (None,)
    assert games[2].timeline[47].cast_name == (Characters.Queen,)
    assert games[2].timeline[47].category == TimelineCategory.SniperLights
    assert games[2].timeline[47].elapsed_time == 8.69
    assert games[2].timeline[47].event == "marked less suspicious."
    assert games[2].timeline[47].mission == Missions.NoMission
    assert games[2].timeline[47].role == (Roles.DoubleAgent,)
    assert games[2].timeline[47].time == 216.3

    assert games[2].timeline[48].action_test == ActionTest.NoAT
    assert games[2].timeline[48].actor == "sniper"
    assert games[2].timeline[48].books == (Books.Green,)
    assert games[2].timeline[48].cast_name == (Characters.Plain,)
    assert (
        games[2].timeline[48].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[48].elapsed_time == 17.81
    assert games[2].timeline[48].event == "marked book."
    assert games[2].timeline[48].mission == Missions.NoMission
    assert games[2].timeline[48].role == (Roles.Civilian,)
    assert games[2].timeline[48].time == 207.1

    assert games[2].timeline[49].action_test == ActionTest.NoAT
    assert games[2].timeline[49].actor == "sniper"
    assert games[2].timeline[49].books == (Books.Green,)
    assert games[2].timeline[49].cast_name == (Characters.Irish,)
    assert (
        games[2].timeline[49].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[49].elapsed_time == 22.06
    assert games[2].timeline[49].event == "marked book."
    assert games[2].timeline[49].mission == Missions.NoMission
    assert games[2].timeline[49].role == (Roles.Civilian,)
    assert games[2].timeline[49].time == 202.9

    assert games[2].timeline[50].action_test == ActionTest.NoAT
    assert games[2].timeline[50].actor == "sniper"
    assert games[2].timeline[50].books == (Books.Blue,)
    assert games[2].timeline[50].cast_name == (Characters.Disney,)
    assert (
        games[2].timeline[50].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[50].elapsed_time == 23.69
    assert games[2].timeline[50].event == "marked book."
    assert games[2].timeline[50].mission == Missions.NoMission
    assert games[2].timeline[50].role == (Roles.Civilian,)
    assert games[2].timeline[50].time == 201.3

    assert games[2].timeline[51].action_test == ActionTest.NoAT
    assert games[2].timeline[51].actor == "spy"
    assert games[2].timeline[51].books == (None,)
    assert games[2].timeline[51].cast_name == (None,)
    assert games[2].timeline[51].category == TimelineCategory.Conversation
    assert games[2].timeline[51].elapsed_time == 26.25
    assert games[2].timeline[51].event == "spy leaves conversation."
    assert games[2].timeline[51].mission == Missions.NoMission
    assert games[2].timeline[51].role == (None,)
    assert games[2].timeline[51].time == 198.7

    assert games[2].timeline[52].action_test == ActionTest.NoAT
    assert games[2].timeline[52].actor == "spy"
    assert games[2].timeline[52].books == (None,)
    assert games[2].timeline[52].cast_name == (None,)
    assert games[2].timeline[52].category == TimelineCategory.NoCategory
    assert games[2].timeline[52].elapsed_time == 26.44
    assert games[2].timeline[52].event == "flirtation cooldown expired."
    assert games[2].timeline[52].mission == Missions.Seduce
    assert games[2].timeline[52].role == (None,)
    assert games[2].timeline[52].time == 198.5

    assert games[2].timeline[53].action_test == ActionTest.NoAT
    assert games[2].timeline[53].actor == "sniper"
    assert games[2].timeline[53].books == (None,)
    assert games[2].timeline[53].cast_name == (Characters.Boots,)
    assert games[2].timeline[53].category == TimelineCategory.SniperLights
    assert games[2].timeline[53].elapsed_time == 26.63
    assert games[2].timeline[53].event == "marked suspicious."
    assert games[2].timeline[53].mission == Missions.NoMission
    assert games[2].timeline[53].role == (Roles.Civilian,)
    assert games[2].timeline[53].time == 198.3

    assert games[2].timeline[54].action_test == ActionTest.NoAT
    assert games[2].timeline[54].actor == "sniper"
    assert games[2].timeline[54].books == (None,)
    assert games[2].timeline[54].cast_name == (Characters.Damon,)
    assert games[2].timeline[54].category == TimelineCategory.SniperLights
    assert games[2].timeline[54].elapsed_time == 37.63
    assert games[2].timeline[54].event == "marked less suspicious."
    assert games[2].timeline[54].mission == Missions.NoMission
    assert games[2].timeline[54].role == (Roles.Staff,)
    assert games[2].timeline[54].time == 187.3

    assert games[2].timeline[55].action_test == ActionTest.NoAT
    assert games[2].timeline[55].actor == "sniper"
    assert games[2].timeline[55].books == (None,)
    assert games[2].timeline[55].cast_name == (Characters.Disney,)
    assert games[2].timeline[55].category == TimelineCategory.SniperLights
    assert games[2].timeline[55].elapsed_time == 41.5
    assert games[2].timeline[55].event == "marked suspicious."
    assert games[2].timeline[55].mission == Missions.NoMission
    assert games[2].timeline[55].role == (Roles.Civilian,)
    assert games[2].timeline[55].time == 183.5

    assert games[2].timeline[56].action_test == ActionTest.NoAT
    assert games[2].timeline[56].actor == "sniper"
    assert games[2].timeline[56].books == (None,)
    assert games[2].timeline[56].cast_name == (Characters.Morgan,)
    assert games[2].timeline[56].category == TimelineCategory.SniperLights
    assert games[2].timeline[56].elapsed_time == 42.63
    assert games[2].timeline[56].event == "marked less suspicious."
    assert games[2].timeline[56].mission == Missions.NoMission
    assert games[2].timeline[56].role == (Roles.SuspectedDoubleAgent,)
    assert games[2].timeline[56].time == 182.3

    assert games[2].timeline[57].action_test == ActionTest.NoAT
    assert games[2].timeline[57].actor == "spy"
    assert games[2].timeline[57].books == (None,)
    assert games[2].timeline[57].cast_name == (Characters.General,)
    assert games[2].timeline[57].category == TimelineCategory.Drinks
    assert games[2].timeline[57].elapsed_time == 44.0
    assert games[2].timeline[57].event == "took last sip of drink."
    assert games[2].timeline[57].mission == Missions.NoMission
    assert games[2].timeline[57].role == (Roles.Spy,)
    assert games[2].timeline[57].time == 180.9

    assert games[2].timeline[58].action_test == ActionTest.NoAT
    assert games[2].timeline[58].actor == "sniper"
    assert games[2].timeline[58].books == (Books.Blue,)
    assert games[2].timeline[58].cast_name == (Characters.Duke,)
    assert (
        games[2].timeline[58].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[58].elapsed_time == 58.56
    assert games[2].timeline[58].event == "marked book."
    assert games[2].timeline[58].mission == Missions.NoMission
    assert games[2].timeline[58].role == (Roles.Civilian,)
    assert games[2].timeline[58].time == 166.4

    assert games[2].timeline[59].action_test == ActionTest.NoAT
    assert games[2].timeline[59].actor == "spy"
    assert games[2].timeline[59].books == (None,)
    assert games[2].timeline[59].cast_name == (None,)
    assert games[2].timeline[59].category == TimelineCategory.Conversation
    assert games[2].timeline[59].elapsed_time == 64.88
    assert games[2].timeline[59].event == "spy enters conversation."
    assert games[2].timeline[59].mission == Missions.NoMission
    assert games[2].timeline[59].role == (None,)
    assert games[2].timeline[59].time == 160.1

    assert games[2].timeline[60].action_test == ActionTest.NoAT
    assert games[2].timeline[60].actor == "spy"
    assert games[2].timeline[60].books == (None,)
    assert games[2].timeline[60].cast_name == (Characters.Queen,)
    assert games[2].timeline[60].category == TimelineCategory.Conversation
    assert games[2].timeline[60].elapsed_time == 64.88
    assert games[2].timeline[60].event == "spy joined conversation with double agent."
    assert games[2].timeline[60].mission == Missions.NoMission
    assert games[2].timeline[60].role == (Roles.DoubleAgent,)
    assert games[2].timeline[60].time == 160.1

    assert games[2].timeline[61].action_test == ActionTest.NoAT
    assert games[2].timeline[61].actor == "spy"
    assert games[2].timeline[61].books == (None,)
    assert games[2].timeline[61].cast_name == (Characters.Queen,)
    assert games[2].timeline[61].category == TimelineCategory.Conversation
    assert games[2].timeline[61].elapsed_time == 70.81
    assert games[2].timeline[61].event == "double agent left conversation with spy."
    assert games[2].timeline[61].mission == Missions.NoMission
    assert games[2].timeline[61].role == (Roles.DoubleAgent,)
    assert games[2].timeline[61].time == 154.1

    assert games[2].timeline[62].action_test == ActionTest.NoAT
    assert games[2].timeline[62].actor == "spy"
    assert games[2].timeline[62].books == (None,)
    assert games[2].timeline[62].cast_name == (Characters.General,)
    assert games[2].timeline[62].category == TimelineCategory.Drinks
    assert games[2].timeline[62].elapsed_time == 72.56
    assert games[2].timeline[62].event == "waiter offered drink."
    assert games[2].timeline[62].mission == Missions.NoMission
    assert games[2].timeline[62].role == (Roles.Spy,)
    assert games[2].timeline[62].time == 152.4

    assert games[2].timeline[63].action_test == ActionTest.NoAT
    assert games[2].timeline[63].actor == "sniper"
    assert games[2].timeline[63].books == (Books.Blue,)
    assert games[2].timeline[63].cast_name == (Characters.Taft,)
    assert (
        games[2].timeline[63].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[63].elapsed_time == 72.63
    assert games[2].timeline[63].event == "marked book."
    assert games[2].timeline[63].mission == Missions.NoMission
    assert games[2].timeline[63].role == (Roles.Civilian,)
    assert games[2].timeline[63].time == 152.3

    assert games[2].timeline[64].action_test == ActionTest.NoAT
    assert games[2].timeline[64].actor == "spy"
    assert games[2].timeline[64].books == (None,)
    assert games[2].timeline[64].cast_name == (Characters.General,)
    assert games[2].timeline[64].category == TimelineCategory.Drinks
    assert games[2].timeline[64].elapsed_time == 76.06
    assert games[2].timeline[64].event == "rejected drink from waiter."
    assert games[2].timeline[64].mission == Missions.NoMission
    assert games[2].timeline[64].role == (Roles.Spy,)
    assert games[2].timeline[64].time == 148.9

    assert games[2].timeline[65].action_test == ActionTest.NoAT
    assert games[2].timeline[65].actor == "spy"
    assert games[2].timeline[65].books == (None,)
    assert games[2].timeline[65].cast_name == (Characters.General,)
    assert games[2].timeline[65].category == TimelineCategory.Drinks
    assert games[2].timeline[65].elapsed_time == 76.06
    assert games[2].timeline[65].event == "waiter stopped offering drink."
    assert games[2].timeline[65].mission == Missions.NoMission
    assert games[2].timeline[65].role == (Roles.Spy,)
    assert games[2].timeline[65].time == 148.9

    assert games[2].timeline[66].action_test == ActionTest.NoAT
    assert games[2].timeline[66].actor == "sniper"
    assert games[2].timeline[66].books == (None,)
    assert games[2].timeline[66].cast_name == (Characters.Helen,)
    assert games[2].timeline[66].category == TimelineCategory.SniperLights
    assert games[2].timeline[66].elapsed_time == 93.44
    assert games[2].timeline[66].event == "marked suspicious."
    assert games[2].timeline[66].mission == Missions.NoMission
    assert games[2].timeline[66].role == (Roles.Civilian,)
    assert games[2].timeline[66].time == 131.5

    assert games[2].timeline[67].action_test == ActionTest.NoAT
    assert games[2].timeline[67].actor == "sniper"
    assert games[2].timeline[67].books == (None,)
    assert games[2].timeline[67].cast_name == (Characters.Taft,)
    assert games[2].timeline[67].category == TimelineCategory.SniperLights
    assert games[2].timeline[67].elapsed_time == 94.25
    assert games[2].timeline[67].event == "marked suspicious."
    assert games[2].timeline[67].mission == Missions.NoMission
    assert games[2].timeline[67].role == (Roles.Civilian,)
    assert games[2].timeline[67].time == 130.7

    assert games[2].timeline[68].action_test == ActionTest.NoAT
    assert games[2].timeline[68].actor == "sniper"
    assert games[2].timeline[68].books == (None,)
    assert games[2].timeline[68].cast_name == (Characters.Helen,)
    assert games[2].timeline[68].category == TimelineCategory.SniperLights
    assert games[2].timeline[68].elapsed_time == 94.56
    assert games[2].timeline[68].event == "marked neutral suspicion."
    assert games[2].timeline[68].mission == Missions.NoMission
    assert games[2].timeline[68].role == (Roles.Civilian,)
    assert games[2].timeline[68].time == 130.4

    assert games[2].timeline[69].action_test == ActionTest.NoAT
    assert games[2].timeline[69].actor == "sniper"
    assert games[2].timeline[69].books == (None,)
    assert games[2].timeline[69].cast_name == (Characters.Morgan,)
    assert games[2].timeline[69].category == TimelineCategory.SniperLights
    assert games[2].timeline[69].elapsed_time == 97.38
    assert games[2].timeline[69].event == "marked neutral suspicion."
    assert games[2].timeline[69].mission == Missions.NoMission
    assert games[2].timeline[69].role == (Roles.SuspectedDoubleAgent,)
    assert games[2].timeline[69].time == 127.6

    assert games[2].timeline[70].action_test == ActionTest.NoAT
    assert games[2].timeline[70].actor == "sniper"
    assert games[2].timeline[70].books == (None,)
    assert games[2].timeline[70].cast_name == (Characters.Morgan,)
    assert games[2].timeline[70].category == TimelineCategory.SniperLights
    assert games[2].timeline[70].elapsed_time == 97.94
    assert games[2].timeline[70].event == "marked less suspicious."
    assert games[2].timeline[70].mission == Missions.NoMission
    assert games[2].timeline[70].role == (Roles.SuspectedDoubleAgent,)
    assert games[2].timeline[70].time == 127.0

    assert games[2].timeline[71].action_test == ActionTest.NoAT
    assert games[2].timeline[71].actor == "spy"
    assert games[2].timeline[71].books == (None,)
    assert games[2].timeline[71].cast_name == (None,)
    assert games[2].timeline[71].category == TimelineCategory.ActionTriggered
    assert games[2].timeline[71].elapsed_time == 111.31
    assert games[2].timeline[71].event == "action triggered: seduce target"
    assert games[2].timeline[71].mission == Missions.Seduce
    assert games[2].timeline[71].role == (None,)
    assert games[2].timeline[71].time == 113.6

    assert games[2].timeline[72].action_test == ActionTest.NoAT
    assert games[2].timeline[72].actor == "spy"
    assert games[2].timeline[72].books == (None,)
    assert games[2].timeline[72].cast_name == (Characters.Rocker,)
    assert games[2].timeline[72].category == TimelineCategory.NoCategory
    assert games[2].timeline[72].elapsed_time == 111.31
    assert games[2].timeline[72].event == "begin flirtation with seduction target."
    assert games[2].timeline[72].mission == Missions.Seduce
    assert games[2].timeline[72].role == (Roles.SeductionTarget,)
    assert games[2].timeline[72].time == 113.6

    assert games[2].timeline[73].action_test == ActionTest.White
    assert games[2].timeline[73].actor == "spy"
    assert games[2].timeline[73].books == (None,)
    assert games[2].timeline[73].cast_name == (None,)
    assert games[2].timeline[73].category == TimelineCategory.ActionTest
    assert games[2].timeline[73].elapsed_time == 112.56
    assert games[2].timeline[73].event == "action test white: seduce target"
    assert games[2].timeline[73].mission == Missions.Seduce
    assert games[2].timeline[73].role == (None,)
    assert games[2].timeline[73].time == 112.4

    assert games[2].timeline[74].action_test == ActionTest.NoAT
    assert games[2].timeline[74].actor == "spy"
    assert games[2].timeline[74].books == (None,)
    assert games[2].timeline[74].cast_name == (Characters.Rocker,)
    assert games[2].timeline[74].category == TimelineCategory.MissionPartial
    assert games[2].timeline[74].elapsed_time == 112.56
    assert games[2].timeline[74].event == "flirt with seduction target: 61%"
    assert games[2].timeline[74].mission == Missions.Seduce
    assert games[2].timeline[74].role == (Roles.SeductionTarget,)
    assert games[2].timeline[74].time == 112.4

    assert games[2].timeline[75].action_test == ActionTest.NoAT
    assert games[2].timeline[75].actor == "spy"
    assert games[2].timeline[75].books == (None,)
    assert games[2].timeline[75].cast_name == (Characters.Queen,)
    assert games[2].timeline[75].category == TimelineCategory.Conversation
    assert games[2].timeline[75].elapsed_time == 113.19
    assert games[2].timeline[75].event == "double agent joined conversation with spy."
    assert games[2].timeline[75].mission == Missions.NoMission
    assert games[2].timeline[75].role == (Roles.DoubleAgent,)
    assert games[2].timeline[75].time == 111.8

    assert games[2].timeline[76].action_test == ActionTest.NoAT
    assert games[2].timeline[76].actor == "sniper"
    assert games[2].timeline[76].books == (Books.Blue,)
    assert games[2].timeline[76].cast_name == (Characters.Sari,)
    assert (
        games[2].timeline[76].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[76].elapsed_time == 114.25
    assert games[2].timeline[76].event == "marked book."
    assert games[2].timeline[76].mission == Missions.NoMission
    assert games[2].timeline[76].role == (Roles.Civilian,)
    assert games[2].timeline[76].time == 110.7

    assert games[2].timeline[77].action_test == ActionTest.NoAT
    assert games[2].timeline[77].actor == "spy"
    assert games[2].timeline[77].books == (None,)
    assert games[2].timeline[77].cast_name == (Characters.General,)
    assert games[2].timeline[77].category == TimelineCategory.Drinks
    assert games[2].timeline[77].elapsed_time == 119.50
    assert games[2].timeline[77].event == "waiter offered drink."
    assert games[2].timeline[77].mission == Missions.NoMission
    assert games[2].timeline[77].role == (Roles.Spy,)
    assert games[2].timeline[77].time == 105.5

    assert games[2].timeline[78].action_test == ActionTest.NoAT
    assert games[2].timeline[78].actor == "spy"
    assert games[2].timeline[78].books == (None,)
    assert games[2].timeline[78].cast_name == (None,)
    assert games[2].timeline[78].category == TimelineCategory.Conversation
    assert games[2].timeline[78].elapsed_time == 122.63
    assert games[2].timeline[78].event == "spy leaves conversation."
    assert games[2].timeline[78].mission == Missions.NoMission
    assert games[2].timeline[78].role == (None,)
    assert games[2].timeline[78].time == 102.3

    assert games[2].timeline[79].action_test == ActionTest.NoAT
    assert games[2].timeline[79].actor == "spy"
    assert games[2].timeline[79].books == (None,)
    assert games[2].timeline[79].cast_name == (Characters.Queen,)
    assert games[2].timeline[79].category == TimelineCategory.Conversation
    assert games[2].timeline[79].elapsed_time == 122.63
    assert games[2].timeline[79].event == "spy left conversation with double agent."
    assert games[2].timeline[79].mission == Missions.NoMission
    assert games[2].timeline[79].role == (Roles.DoubleAgent,)
    assert games[2].timeline[79].time == 102.3

    assert games[2].timeline[80].action_test == ActionTest.NoAT
    assert games[2].timeline[80].actor == "spy"
    assert games[2].timeline[80].books == (None,)
    assert games[2].timeline[80].cast_name == (Characters.General,)
    assert games[2].timeline[80].category == TimelineCategory.Drinks
    assert games[2].timeline[80].elapsed_time == 122.63
    assert games[2].timeline[80].event == "rejected drink from waiter."
    assert games[2].timeline[80].mission == Missions.NoMission
    assert games[2].timeline[80].role == (Roles.Spy,)
    assert games[2].timeline[80].time == 102.3

    assert games[2].timeline[81].action_test == ActionTest.NoAT
    assert games[2].timeline[81].actor == "spy"
    assert games[2].timeline[81].books == (None,)
    assert games[2].timeline[81].cast_name == (Characters.General,)
    assert games[2].timeline[81].category == TimelineCategory.Drinks
    assert games[2].timeline[81].elapsed_time == 122.63
    assert games[2].timeline[81].event == "waiter stopped offering drink."
    assert games[2].timeline[81].mission == Missions.NoMission
    assert games[2].timeline[81].role == (Roles.Spy,)
    assert games[2].timeline[81].time == 102.3

    assert games[2].timeline[82].action_test == ActionTest.NoAT
    assert games[2].timeline[82].actor == "spy"
    assert games[2].timeline[82].books == (Books.Green,)
    assert games[2].timeline[82].cast_name == (None,)
    assert games[2].timeline[82].category == TimelineCategory.Books
    assert games[2].timeline[82].elapsed_time == 129.25
    assert games[2].timeline[82].event == "get book from bookcase."
    assert games[2].timeline[82].mission == Missions.NoMission
    assert games[2].timeline[82].role == (None,)
    assert games[2].timeline[82].time == 95.7

    assert games[2].timeline[83].action_test == ActionTest.NoAT
    assert games[2].timeline[83].actor == "sniper"
    assert games[2].timeline[83].books == (None,)
    assert games[2].timeline[83].cast_name == (Characters.General,)
    assert games[2].timeline[83].category == TimelineCategory.SniperLights
    assert games[2].timeline[83].elapsed_time == 134.63
    assert games[2].timeline[83].event == "marked spy suspicious."
    assert games[2].timeline[83].mission == Missions.NoMission
    assert games[2].timeline[83].role == (Roles.Spy,)
    assert games[2].timeline[83].time == 90.3

    assert games[2].timeline[84].action_test == ActionTest.NoAT
    assert games[2].timeline[84].actor == "sniper"
    assert games[2].timeline[84].books == (Books.Blue,)
    assert games[2].timeline[84].cast_name == (Characters.General,)
    assert (
        games[2].timeline[84].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[84].elapsed_time == 135.31
    assert games[2].timeline[84].event == "marked book."
    assert games[2].timeline[84].mission == Missions.NoMission
    assert games[2].timeline[84].role == (Roles.Spy,)
    assert games[2].timeline[84].time == 89.6

    assert games[2].timeline[85].action_test == ActionTest.NoAT
    assert games[2].timeline[85].actor == "spy"
    assert games[2].timeline[85].books == (None,)
    assert games[2].timeline[85].cast_name == (None,)
    assert games[2].timeline[85].category == TimelineCategory.NoCategory
    assert games[2].timeline[85].elapsed_time == 135.56
    assert games[2].timeline[85].event == "flirtation cooldown expired."
    assert games[2].timeline[85].mission == Missions.Seduce
    assert games[2].timeline[85].role == (None,)
    assert games[2].timeline[85].time == 89.4

    assert games[2].timeline[86].action_test == ActionTest.NoAT
    assert games[2].timeline[86].actor == "sniper"
    assert games[2].timeline[86].books == (None,)
    assert games[2].timeline[86].cast_name == (Characters.General,)
    assert games[2].timeline[86].category == TimelineCategory.SniperLights
    assert games[2].timeline[86].elapsed_time == 137.0
    assert games[2].timeline[86].event == "marked spy neutral suspicion."
    assert games[2].timeline[86].mission == Missions.NoMission
    assert games[2].timeline[86].role == (Roles.Spy,)
    assert games[2].timeline[86].time == 88.0

    assert games[2].timeline[87].action_test == ActionTest.NoAT
    assert games[2].timeline[87].actor == "spy"
    assert games[2].timeline[87].books == (Books.Green, Books.Green)
    assert games[2].timeline[87].cast_name == (None,)
    assert games[2].timeline[87].category == TimelineCategory.Books
    assert games[2].timeline[87].elapsed_time == 138.0
    assert games[2].timeline[87].event == "put book in bookcase."
    assert games[2].timeline[87].mission == Missions.NoMission
    assert games[2].timeline[87].role == (None,)
    assert games[2].timeline[87].time == 87.0

    assert games[2].timeline[88].action_test == ActionTest.NoAT
    assert games[2].timeline[88].actor == "spy"
    assert games[2].timeline[88].books == (None,)
    assert games[2].timeline[88].cast_name == (None,)
    assert games[2].timeline[88].category == TimelineCategory.Statues
    assert games[2].timeline[88].elapsed_time == 151.88
    assert games[2].timeline[88].event == "picked up statue."
    assert games[2].timeline[88].mission == Missions.NoMission
    assert games[2].timeline[88].role == (None,)
    assert games[2].timeline[88].time == 73.1

    assert games[2].timeline[89].action_test == ActionTest.NoAT
    assert games[2].timeline[89].actor == "sniper"
    assert games[2].timeline[89].books == (Books.Green,)
    assert games[2].timeline[89].cast_name == (Characters.Duke,)
    assert (
        games[2].timeline[89].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[89].elapsed_time == 153.25
    assert games[2].timeline[89].event == "marked book."
    assert games[2].timeline[89].mission == Missions.NoMission
    assert games[2].timeline[89].role == (Roles.Civilian,)
    assert games[2].timeline[89].time == 71.7

    assert games[2].timeline[90].action_test == ActionTest.NoAT
    assert games[2].timeline[90].actor == "spy"
    assert games[2].timeline[90].books == (None,)
    assert games[2].timeline[90].cast_name == (None,)
    assert (
        games[2].timeline[90].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[2].timeline[90].elapsed_time == 155.0
    assert games[2].timeline[90].event == "action triggered: inspect statues"
    assert games[2].timeline[90].mission == Missions.Inspect
    assert games[2].timeline[90].role == (None,)
    assert games[2].timeline[90].time == 69.9

    assert games[2].timeline[91].action_test == ActionTest.Green
    assert games[2].timeline[91].actor == "spy"
    assert games[2].timeline[91].books == (None,)
    assert games[2].timeline[91].cast_name == (None,)
    assert (
        games[2].timeline[91].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[2].timeline[91].elapsed_time == 156.06
    assert games[2].timeline[91].event == "action test green: inspect statues"
    assert games[2].timeline[91].mission == Missions.Inspect
    assert games[2].timeline[91].role == (None,)
    assert games[2].timeline[91].time == 68.9

    assert games[2].timeline[92].action_test == ActionTest.NoAT
    assert games[2].timeline[92].actor == "spy"
    assert games[2].timeline[92].books == (None,)
    assert games[2].timeline[92].cast_name == (None,)
    assert (
        games[2].timeline[92].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[2].timeline[92].elapsed_time == 158.5
    assert games[2].timeline[92].event == "right statue inspected."
    assert games[2].timeline[92].mission == Missions.Inspect
    assert games[2].timeline[92].role == (None,)
    assert games[2].timeline[92].time == 66.5

    assert games[2].timeline[93].action_test == ActionTest.NoAT
    assert games[2].timeline[93].actor == "spy"
    assert games[2].timeline[93].books == (None,)
    assert games[2].timeline[93].cast_name == (None,)
    assert (
        games[2].timeline[93].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[2].timeline[93].elapsed_time == 158.81
    assert games[2].timeline[93].event == "action triggered: inspect statues"
    assert games[2].timeline[93].mission == Missions.Inspect
    assert games[2].timeline[93].role == (None,)
    assert games[2].timeline[93].time == 66.1

    assert games[2].timeline[94].action_test == ActionTest.White
    assert games[2].timeline[94].actor == "spy"
    assert games[2].timeline[94].books == (None,)
    assert games[2].timeline[94].cast_name == (None,)
    assert (
        games[2].timeline[94].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[2].timeline[94].elapsed_time == 159.88
    assert games[2].timeline[94].event == "action test white: inspect statues"
    assert games[2].timeline[94].mission == Missions.Inspect
    assert games[2].timeline[94].role == (None,)
    assert games[2].timeline[94].time == 65.1

    assert games[2].timeline[95].action_test == ActionTest.NoAT
    assert games[2].timeline[95].actor == "sniper"
    assert games[2].timeline[95].books == (None,)
    assert games[2].timeline[95].cast_name == (Characters.General,)
    assert games[2].timeline[95].category == TimelineCategory.SniperLights
    assert games[2].timeline[95].elapsed_time == 161.75
    assert games[2].timeline[95].event == "marked spy suspicious."
    assert games[2].timeline[95].mission == Missions.NoMission
    assert games[2].timeline[95].role == (Roles.Spy,)
    assert games[2].timeline[95].time == 63.2

    assert games[2].timeline[96].action_test == ActionTest.NoAT
    assert games[2].timeline[96].actor == "spy"
    assert games[2].timeline[96].books == (None,)
    assert games[2].timeline[96].cast_name == (None,)
    assert (
        games[2].timeline[96].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[2].timeline[96].elapsed_time == 162.81
    assert games[2].timeline[96].event == "held statue inspected."
    assert games[2].timeline[96].mission == Missions.Inspect
    assert games[2].timeline[96].role == (None,)
    assert games[2].timeline[96].time == 62.1

    assert games[2].timeline[97].action_test == ActionTest.NoAT
    assert games[2].timeline[97].actor == "sniper"
    assert games[2].timeline[97].books == (Books.Green,)
    assert games[2].timeline[97].cast_name == (Characters.Sari,)
    assert (
        games[2].timeline[97].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[2].timeline[97].elapsed_time == 164.06
    assert games[2].timeline[97].event == "marked book."
    assert games[2].timeline[97].mission == Missions.NoMission
    assert games[2].timeline[97].role == (Roles.Civilian,)
    assert games[2].timeline[97].time == 60.9

    assert games[2].timeline[98].action_test == ActionTest.NoAT
    assert games[2].timeline[98].actor == "spy"
    assert games[2].timeline[98].books == (None,)
    assert games[2].timeline[98].cast_name == (None,)
    assert games[2].timeline[98].category == TimelineCategory.Statues
    assert games[2].timeline[98].elapsed_time == 165.69
    assert games[2].timeline[98].event == "put back statue."
    assert games[2].timeline[98].mission == Missions.NoMission
    assert games[2].timeline[98].role == (None,)
    assert games[2].timeline[98].time == 59.3

    assert games[2].timeline[99].action_test == ActionTest.NoAT
    assert games[2].timeline[99].actor == "spy"
    assert games[2].timeline[99].books == (None,)
    assert games[2].timeline[99].cast_name == (None,)
    assert games[2].timeline[99].category == TimelineCategory.Conversation
    assert games[2].timeline[99].elapsed_time == 174.06
    assert games[2].timeline[99].event == "spy enters conversation."
    assert games[2].timeline[99].mission == Missions.NoMission
    assert games[2].timeline[99].role == (None,)
    assert games[2].timeline[99].time == 50.9

    assert games[2].timeline[100].action_test == ActionTest.NoAT
    assert games[2].timeline[100].actor == "spy"
    assert games[2].timeline[100].books == (None,)
    assert games[2].timeline[100].cast_name == (Characters.Queen,)
    assert games[2].timeline[100].category == TimelineCategory.Conversation
    assert games[2].timeline[100].elapsed_time == 174.06
    assert games[2].timeline[100].event == "spy joined conversation with double agent."
    assert games[2].timeline[100].mission == Missions.NoMission
    assert games[2].timeline[100].role == (Roles.DoubleAgent,)
    assert games[2].timeline[100].time == 50.9

    assert games[2].timeline[101].action_test == ActionTest.NoAT
    assert games[2].timeline[101].actor == "spy"
    assert games[2].timeline[101].books == (None,)
    assert games[2].timeline[101].cast_name == (None,)
    assert games[2].timeline[101].category == TimelineCategory.ActionTriggered
    assert games[2].timeline[101].elapsed_time == 174.44
    assert games[2].timeline[101].event == "action triggered: contact double agent"
    assert games[2].timeline[101].mission == Missions.Contact
    assert games[2].timeline[101].role == (None,)
    assert games[2].timeline[101].time == 50.5

    assert games[2].timeline[102].action_test == ActionTest.NoAT
    assert games[2].timeline[102].actor == "spy"
    assert games[2].timeline[102].books == (None,)
    assert games[2].timeline[102].cast_name == (None,)
    assert games[2].timeline[102].category == TimelineCategory.BananaBread
    assert games[2].timeline[102].elapsed_time == 174.44
    assert games[2].timeline[102].event == "real banana bread started."
    assert games[2].timeline[102].mission == Missions.Contact
    assert games[2].timeline[102].role == (None,)
    assert games[2].timeline[102].time == 50.5

    assert games[2].timeline[103].action_test == ActionTest.White
    assert games[2].timeline[103].actor == "spy"
    assert games[2].timeline[103].books == (None,)
    assert games[2].timeline[103].cast_name == (None,)
    assert games[2].timeline[103].category == TimelineCategory.ActionTest
    assert games[2].timeline[103].elapsed_time == 175.0
    assert games[2].timeline[103].event == "action test white: contact double agent"
    assert games[2].timeline[103].mission == Missions.Contact
    assert games[2].timeline[103].role == (None,)
    assert games[2].timeline[103].time == 50.0

    assert games[2].timeline[104].action_test == ActionTest.NoAT
    assert games[2].timeline[104].actor == "sniper"
    assert games[2].timeline[104].books == (None,)
    assert games[2].timeline[104].cast_name == (Characters.Salmon,)
    assert games[2].timeline[104].category == TimelineCategory.SniperLights
    assert games[2].timeline[104].elapsed_time == 175.56
    assert games[2].timeline[104].event == "marked suspicious."
    assert games[2].timeline[104].mission == Missions.NoMission
    assert games[2].timeline[104].role == (Roles.Civilian,)
    assert games[2].timeline[104].time == 49.4

    assert games[2].timeline[105].action_test == ActionTest.NoAT
    assert games[2].timeline[105].actor == "spy"
    assert games[2].timeline[105].books == (None,)
    assert games[2].timeline[105].cast_name == (None,)
    assert games[2].timeline[105].category == TimelineCategory.BananaBread
    assert games[2].timeline[105].elapsed_time == 176.13
    assert games[2].timeline[105].event == "banana bread uttered."
    assert games[2].timeline[105].mission == Missions.Contact
    assert games[2].timeline[105].role == (None,)
    assert games[2].timeline[105].time == 48.8

    assert games[2].timeline[106].action_test == ActionTest.NoAT
    assert games[2].timeline[106].actor == "spy"
    assert games[2].timeline[106].books == (None,)
    assert games[2].timeline[106].cast_name == (Characters.Queen,)
    assert games[2].timeline[106].category == TimelineCategory.MissionComplete
    assert games[2].timeline[106].elapsed_time == 176.63
    assert games[2].timeline[106].event == "double agent contacted."
    assert games[2].timeline[106].mission == Missions.Contact
    assert games[2].timeline[106].role == (Roles.DoubleAgent,)
    assert games[2].timeline[106].time == 48.3

    assert games[2].timeline[107].action_test == ActionTest.NoAT
    assert games[2].timeline[107].actor == "sniper"
    assert games[2].timeline[107].books == (None,)
    assert games[2].timeline[107].cast_name == (Characters.Salmon,)
    assert games[2].timeline[107].category == TimelineCategory.SniperLights
    assert games[2].timeline[107].elapsed_time == 177.0
    assert games[2].timeline[107].event == "marked less suspicious."
    assert games[2].timeline[107].mission == Missions.NoMission
    assert games[2].timeline[107].role == (Roles.Civilian,)
    assert games[2].timeline[107].time == 48.0

    assert games[2].timeline[108].action_test == ActionTest.NoAT
    assert games[2].timeline[108].actor == "sniper"
    assert games[2].timeline[108].books == (None,)
    assert games[2].timeline[108].cast_name == (Characters.Oprah,)
    assert games[2].timeline[108].category == TimelineCategory.SniperLights
    assert games[2].timeline[108].elapsed_time == 177.25
    assert games[2].timeline[108].event == "marked less suspicious."
    assert games[2].timeline[108].mission == Missions.NoMission
    assert games[2].timeline[108].role == (Roles.Civilian,)
    assert games[2].timeline[108].time == 47.7

    assert games[2].timeline[109].action_test == ActionTest.NoAT
    assert games[2].timeline[109].actor == "sniper"
    assert games[2].timeline[109].books == (None,)
    assert games[2].timeline[109].cast_name == (Characters.Helen,)
    assert games[2].timeline[109].category == TimelineCategory.SniperLights
    assert games[2].timeline[109].elapsed_time == 178.38
    assert games[2].timeline[109].event == "marked less suspicious."
    assert games[2].timeline[109].mission == Missions.NoMission
    assert games[2].timeline[109].role == (Roles.Civilian,)
    assert games[2].timeline[109].time == 46.6

    assert games[2].timeline[110].action_test == ActionTest.NoAT
    assert games[2].timeline[110].actor == "sniper"
    assert games[2].timeline[110].books == (None,)
    assert games[2].timeline[110].cast_name == (Characters.Teal,)
    assert games[2].timeline[110].category == TimelineCategory.SniperLights
    assert games[2].timeline[110].elapsed_time == 178.75
    assert games[2].timeline[110].event == "marked less suspicious."
    assert games[2].timeline[110].mission == Missions.NoMission
    assert games[2].timeline[110].role == (Roles.Civilian,)
    assert games[2].timeline[110].time == 46.2

    assert games[2].timeline[111].action_test == ActionTest.NoAT
    assert games[2].timeline[111].actor == "sniper"
    assert games[2].timeline[111].books == (None,)
    assert games[2].timeline[111].cast_name == (Characters.Plain,)
    assert games[2].timeline[111].category == TimelineCategory.SniperLights
    assert games[2].timeline[111].elapsed_time == 179.69
    assert games[2].timeline[111].event == "marked less suspicious."
    assert games[2].timeline[111].mission == Missions.NoMission
    assert games[2].timeline[111].role == (Roles.Civilian,)
    assert games[2].timeline[111].time == 45.3

    assert games[2].timeline[112].action_test == ActionTest.NoAT
    assert games[2].timeline[112].actor == "sniper"
    assert games[2].timeline[112].books == (None,)
    assert games[2].timeline[112].cast_name == (Characters.Sari,)
    assert games[2].timeline[112].category == TimelineCategory.SniperLights
    assert games[2].timeline[112].elapsed_time == 180.94
    assert games[2].timeline[112].event == "marked less suspicious."
    assert games[2].timeline[112].mission == Missions.NoMission
    assert games[2].timeline[112].role == (Roles.Civilian,)
    assert games[2].timeline[112].time == 44.0

    assert games[2].timeline[113].action_test == ActionTest.NoAT
    assert games[2].timeline[113].actor == "sniper"
    assert games[2].timeline[113].books == (None,)
    assert games[2].timeline[113].cast_name == (Characters.Taft,)
    assert games[2].timeline[113].category == TimelineCategory.SniperLights
    assert games[2].timeline[113].elapsed_time == 181.75
    assert games[2].timeline[113].event == "marked less suspicious."
    assert games[2].timeline[113].mission == Missions.NoMission
    assert games[2].timeline[113].role == (Roles.Civilian,)
    assert games[2].timeline[113].time == 43.2

    assert games[2].timeline[114].action_test == ActionTest.NoAT
    assert games[2].timeline[114].actor == "sniper"
    assert games[2].timeline[114].books == (None,)
    assert games[2].timeline[114].cast_name == (Characters.Boots,)
    assert games[2].timeline[114].category == TimelineCategory.SniperLights
    assert games[2].timeline[114].elapsed_time == 182.38
    assert games[2].timeline[114].event == "marked less suspicious."
    assert games[2].timeline[114].mission == Missions.NoMission
    assert games[2].timeline[114].role == (Roles.Civilian,)
    assert games[2].timeline[114].time == 42.6

    assert games[2].timeline[115].action_test == ActionTest.NoAT
    assert games[2].timeline[115].actor == "sniper"
    assert games[2].timeline[115].books == (None,)
    assert games[2].timeline[115].cast_name == (Characters.Carlos,)
    assert games[2].timeline[115].category == TimelineCategory.SniperLights
    assert games[2].timeline[115].elapsed_time == 183.63
    assert games[2].timeline[115].event == "marked less suspicious."
    assert games[2].timeline[115].mission == Missions.NoMission
    assert games[2].timeline[115].role == (Roles.Civilian,)
    assert games[2].timeline[115].time == 41.3

    assert games[2].timeline[116].action_test == ActionTest.NoAT
    assert games[2].timeline[116].actor == "sniper"
    assert games[2].timeline[116].books == (None,)
    assert games[2].timeline[116].cast_name == (Characters.Sikh,)
    assert games[2].timeline[116].category == TimelineCategory.SniperLights
    assert games[2].timeline[116].elapsed_time == 184.69
    assert games[2].timeline[116].event == "marked less suspicious."
    assert games[2].timeline[116].mission == Missions.NoMission
    assert games[2].timeline[116].role == (Roles.Civilian,)
    assert games[2].timeline[116].time == 40.3

    assert games[2].timeline[117].action_test == ActionTest.NoAT
    assert games[2].timeline[117].actor == "sniper"
    assert games[2].timeline[117].books == (None,)
    assert games[2].timeline[117].cast_name == (Characters.Duke,)
    assert games[2].timeline[117].category == TimelineCategory.SniperLights
    assert games[2].timeline[117].elapsed_time == 185.19
    assert games[2].timeline[117].event == "marked less suspicious."
    assert games[2].timeline[117].mission == Missions.NoMission
    assert games[2].timeline[117].role == (Roles.Civilian,)
    assert games[2].timeline[117].time == 39.8

    assert games[2].timeline[118].action_test == ActionTest.NoAT
    assert games[2].timeline[118].actor == "sniper"
    assert games[2].timeline[118].books == (None,)
    assert games[2].timeline[118].cast_name == (Characters.Duke,)
    assert games[2].timeline[118].category == TimelineCategory.SniperLights
    assert games[2].timeline[118].elapsed_time == 185.94
    assert games[2].timeline[118].event == "marked suspicious."
    assert games[2].timeline[118].mission == Missions.NoMission
    assert games[2].timeline[118].role == (Roles.Civilian,)
    assert games[2].timeline[118].time == 39.0

    assert games[2].timeline[119].action_test == ActionTest.NoAT
    assert games[2].timeline[119].actor == "sniper"
    assert games[2].timeline[119].books == (None,)
    assert games[2].timeline[119].cast_name == (Characters.Smallman,)
    assert games[2].timeline[119].category == TimelineCategory.SniperLights
    assert games[2].timeline[119].elapsed_time == 188.63
    assert games[2].timeline[119].event == "marked suspicious."
    assert games[2].timeline[119].mission == Missions.NoMission
    assert games[2].timeline[119].role == (Roles.Civilian,)
    assert games[2].timeline[119].time == 36.3

    assert games[2].timeline[120].action_test == ActionTest.NoAT
    assert games[2].timeline[120].actor == "spy"
    assert games[2].timeline[120].books == (None,)
    assert games[2].timeline[120].cast_name == (None,)
    assert games[2].timeline[120].category == TimelineCategory.ActionTriggered
    assert games[2].timeline[120].elapsed_time == 192.44
    assert games[2].timeline[120].event == "action triggered: seduce target"
    assert games[2].timeline[120].mission == Missions.Seduce
    assert games[2].timeline[120].role == (None,)
    assert games[2].timeline[120].time == 32.5

    assert games[2].timeline[121].action_test == ActionTest.NoAT
    assert games[2].timeline[121].actor == "spy"
    assert games[2].timeline[121].books == (None,)
    assert games[2].timeline[121].cast_name == (Characters.Rocker,)
    assert games[2].timeline[121].category == TimelineCategory.NoCategory
    assert games[2].timeline[121].elapsed_time == 192.44
    assert games[2].timeline[121].event == "begin flirtation with seduction target."
    assert games[2].timeline[121].mission == Missions.Seduce
    assert games[2].timeline[121].role == (Roles.SeductionTarget,)
    assert games[2].timeline[121].time == 32.5

    assert games[2].timeline[122].action_test == ActionTest.NoAT
    assert games[2].timeline[122].actor == "spy"
    assert games[2].timeline[122].books == (None,)
    assert games[2].timeline[122].cast_name == (None,)
    assert games[2].timeline[122].category == TimelineCategory.Conversation
    assert games[2].timeline[122].elapsed_time == 192.44
    assert games[2].timeline[122].event == "spy leaves conversation."
    assert games[2].timeline[122].mission == Missions.NoMission
    assert games[2].timeline[122].role == (None,)
    assert games[2].timeline[122].time == 32.5

    assert games[2].timeline[123].action_test == ActionTest.NoAT
    assert games[2].timeline[123].actor == "spy"
    assert games[2].timeline[123].books == (None,)
    assert games[2].timeline[123].cast_name == (Characters.Queen,)
    assert games[2].timeline[123].category == TimelineCategory.Conversation
    assert games[2].timeline[123].elapsed_time == 192.44
    assert games[2].timeline[123].event == "spy left conversation with double agent."
    assert games[2].timeline[123].mission == Missions.NoMission
    assert games[2].timeline[123].role == (Roles.DoubleAgent,)
    assert games[2].timeline[123].time == 32.5

    assert games[2].timeline[124].action_test == ActionTest.Canceled
    assert games[2].timeline[124].actor == "spy"
    assert games[2].timeline[124].books == (None,)
    assert games[2].timeline[124].cast_name == (None,)
    assert games[2].timeline[124].category == TimelineCategory.ActionTest
    assert games[2].timeline[124].elapsed_time == 192.44
    assert games[2].timeline[124].event == "action test canceled: seduce target"
    assert games[2].timeline[124].mission == Missions.Seduce
    assert games[2].timeline[124].role == (None,)
    assert games[2].timeline[124].time == 32.5

    assert games[2].timeline[125].action_test == ActionTest.NoAT
    assert games[2].timeline[125].actor == "spy"
    assert games[2].timeline[125].books == (None,)
    assert games[2].timeline[125].cast_name == (Characters.Rocker,)
    assert games[2].timeline[125].category == TimelineCategory.NoCategory
    assert games[2].timeline[125].elapsed_time == 192.44
    assert games[2].timeline[125].event == "seduction canceled."
    assert games[2].timeline[125].mission == Missions.Seduce
    assert games[2].timeline[125].role == (Roles.SeductionTarget,)
    assert games[2].timeline[125].time == 32.5

    assert games[2].timeline[126].action_test == ActionTest.NoAT
    assert games[2].timeline[126].actor == "spy"
    assert games[2].timeline[126].books == (None,)
    assert games[2].timeline[126].cast_name == (None,)
    assert games[2].timeline[126].category == TimelineCategory.Conversation
    assert games[2].timeline[126].elapsed_time == 200.13
    assert games[2].timeline[126].event == "spy enters conversation."
    assert games[2].timeline[126].mission == Missions.NoMission
    assert games[2].timeline[126].role == (None,)
    assert games[2].timeline[126].time == 24.8

    assert games[2].timeline[127].action_test == ActionTest.NoAT
    assert games[2].timeline[127].actor == "spy"
    assert games[2].timeline[127].books == (None,)
    assert games[2].timeline[127].cast_name == (None,)
    assert games[2].timeline[127].category == TimelineCategory.ActionTriggered
    assert games[2].timeline[127].elapsed_time == 205.13
    assert games[2].timeline[127].event == "action triggered: seduce target"
    assert games[2].timeline[127].mission == Missions.Seduce
    assert games[2].timeline[127].role == (None,)
    assert games[2].timeline[127].time == 19.8

    assert games[2].timeline[128].action_test == ActionTest.NoAT
    assert games[2].timeline[128].actor == "spy"
    assert games[2].timeline[128].books == (None,)
    assert games[2].timeline[128].cast_name == (Characters.Rocker,)
    assert games[2].timeline[128].category == TimelineCategory.NoCategory
    assert games[2].timeline[128].elapsed_time == 205.13
    assert games[2].timeline[128].event == "begin flirtation with seduction target."
    assert games[2].timeline[128].mission == Missions.Seduce
    assert games[2].timeline[128].role == (Roles.SeductionTarget,)
    assert games[2].timeline[128].time == 19.8

    assert games[2].timeline[129].action_test == ActionTest.White
    assert games[2].timeline[129].actor == "spy"
    assert games[2].timeline[129].books == (None,)
    assert games[2].timeline[129].cast_name == (None,)
    assert games[2].timeline[129].category == TimelineCategory.ActionTest
    assert games[2].timeline[129].elapsed_time == 205.94
    assert games[2].timeline[129].event == "action test white: seduce target"
    assert games[2].timeline[129].mission == Missions.Seduce
    assert games[2].timeline[129].role == (None,)
    assert games[2].timeline[129].time == 19.0

    assert games[2].timeline[130].action_test == ActionTest.NoAT
    assert games[2].timeline[130].actor == "spy"
    assert games[2].timeline[130].books == (None,)
    assert games[2].timeline[130].cast_name == (Characters.Rocker,)
    assert games[2].timeline[130].category == TimelineCategory.MissionPartial
    assert games[2].timeline[130].elapsed_time == 205.94
    assert games[2].timeline[130].event == "flirt with seduction target: 95%"
    assert games[2].timeline[130].mission == Missions.Seduce
    assert games[2].timeline[130].role == (Roles.SeductionTarget,)
    assert games[2].timeline[130].time == 19.0

    assert games[2].timeline[131].action_test == ActionTest.NoAT
    assert games[2].timeline[131].actor == "spy"
    assert games[2].timeline[131].books == (None,)
    assert games[2].timeline[131].cast_name == (Characters.General,)
    assert games[2].timeline[131].category == TimelineCategory.Drinks
    assert games[2].timeline[131].elapsed_time == 210.06
    assert games[2].timeline[131].event == "request drink from waiter."
    assert games[2].timeline[131].mission == Missions.NoMission
    assert games[2].timeline[131].role == (Roles.Spy,)
    assert games[2].timeline[131].time == 14.9

    assert games[2].timeline[132].action_test == ActionTest.NoAT
    assert games[2].timeline[132].actor == "spy"
    assert games[2].timeline[132].books == (None,)
    assert games[2].timeline[132].cast_name == (None,)
    assert games[2].timeline[132].category == TimelineCategory.Conversation
    assert games[2].timeline[132].elapsed_time == 213.0
    assert games[2].timeline[132].event == "spy leaves conversation."
    assert games[2].timeline[132].mission == Missions.NoMission
    assert games[2].timeline[132].role == (None,)
    assert games[2].timeline[132].time == 12.0

    assert games[2].timeline[133].action_test == ActionTest.NoAT
    assert games[2].timeline[133].actor == "spy"
    assert games[2].timeline[133].books == (None,)
    assert games[2].timeline[133].cast_name == (None,)
    assert games[2].timeline[133].category == TimelineCategory.NoCategory
    assert games[2].timeline[133].elapsed_time == 222.0
    assert games[2].timeline[133].event == "flirtation cooldown expired."
    assert games[2].timeline[133].mission == Missions.Seduce
    assert games[2].timeline[133].role == (None,)
    assert games[2].timeline[133].time == 3.0

    assert games[2].timeline[134].action_test == ActionTest.NoAT
    assert games[2].timeline[134].actor == "spy"
    assert games[2].timeline[134].books == (None,)
    assert games[2].timeline[134].cast_name == (None,)
    assert games[2].timeline[134].category == TimelineCategory.Statues
    assert games[2].timeline[134].elapsed_time == 223.38
    assert games[2].timeline[134].event == "picked up statue."
    assert games[2].timeline[134].mission == Missions.NoMission
    assert games[2].timeline[134].role == (None,)
    assert games[2].timeline[134].time == 1.6

    assert games[2].timeline[135].action_test == ActionTest.NoAT
    assert games[2].timeline[135].actor == "game"
    assert games[2].timeline[135].books == (None,)
    assert games[2].timeline[135].cast_name == (None,)
    assert games[2].timeline[135].category == TimelineCategory.GameEnd
    assert games[2].timeline[135].elapsed_time == 225.0
    assert games[2].timeline[135].event == "spy ran out of time."
    assert games[2].timeline[135].mission == Missions.NoMission
    assert games[2].timeline[135].role == (None,)
    assert games[2].timeline[135].time == 0.0

    assert games[2].timeline.get_next_spy_action(games[2].timeline[135]) is None

    assert games[3].uuid == "lOGf7W_MSlu1RRYxW2MMsA"
    assert games[3].timeline[0].action_test == ActionTest.NoAT
    assert games[3].timeline[0].actor == "spy"
    assert games[3].timeline[0].books == (None,)
    assert games[3].timeline[0].cast_name == (Characters.Plain,)
    assert games[3].timeline[0].category == TimelineCategory.Cast
    assert games[3].timeline[0].elapsed_time == 0.0
    assert games[3].timeline[0].event == "spy cast."
    assert games[3].timeline[0].mission == Missions.NoMission
    assert games[3].timeline[0].role == (Roles.Spy,)
    assert games[3].timeline[0].time == 225.0

    assert games[3].timeline[1].action_test == ActionTest.NoAT
    assert games[3].timeline[1].actor == "spy"
    assert games[3].timeline[1].books == (None,)
    assert games[3].timeline[1].cast_name == (Characters.Taft,)
    assert games[3].timeline[1].category == TimelineCategory.Cast
    assert games[3].timeline[1].elapsed_time == 0.0
    assert games[3].timeline[1].event == "ambassador cast."
    assert games[3].timeline[1].mission == Missions.NoMission
    assert games[3].timeline[1].role == (Roles.Ambassador,)
    assert games[3].timeline[1].time == 225.0

    assert games[3].timeline[2].action_test == ActionTest.NoAT
    assert games[3].timeline[2].actor == "spy"
    assert games[3].timeline[2].books == (None,)
    assert games[3].timeline[2].cast_name == (Characters.Disney,)
    assert games[3].timeline[2].category == TimelineCategory.Cast
    assert games[3].timeline[2].elapsed_time == 0.0
    assert games[3].timeline[2].event == "double agent cast."
    assert games[3].timeline[2].mission == Missions.NoMission
    assert games[3].timeline[2].role == (Roles.DoubleAgent,)
    assert games[3].timeline[2].time == 225.0

    assert games[3].timeline[3].action_test == ActionTest.NoAT
    assert games[3].timeline[3].actor == "spy"
    assert games[3].timeline[3].books == (None,)
    assert games[3].timeline[3].cast_name == (Characters.Duke,)
    assert games[3].timeline[3].category == TimelineCategory.Cast
    assert games[3].timeline[3].elapsed_time == 0.0
    assert games[3].timeline[3].event == "suspected double agent cast."
    assert games[3].timeline[3].mission == Missions.NoMission
    assert games[3].timeline[3].role == (Roles.SuspectedDoubleAgent,)
    assert games[3].timeline[3].time == 225.0

    assert games[3].timeline[4].action_test == ActionTest.NoAT
    assert games[3].timeline[4].actor == "spy"
    assert games[3].timeline[4].books == (None,)
    assert games[3].timeline[4].cast_name == (Characters.Smallman,)
    assert games[3].timeline[4].category == TimelineCategory.Cast
    assert games[3].timeline[4].elapsed_time == 0.0
    assert games[3].timeline[4].event == "seduction target cast."
    assert games[3].timeline[4].mission == Missions.NoMission
    assert games[3].timeline[4].role == (Roles.SeductionTarget,)
    assert games[3].timeline[4].time == 225.0

    assert games[3].timeline[5].action_test == ActionTest.NoAT
    assert games[3].timeline[5].actor == "spy"
    assert games[3].timeline[5].books == (None,)
    assert games[3].timeline[5].cast_name == (Characters.Boots,)
    assert games[3].timeline[5].category == TimelineCategory.Cast
    assert games[3].timeline[5].elapsed_time == 0.0
    assert games[3].timeline[5].event == "civilian cast."
    assert games[3].timeline[5].mission == Missions.NoMission
    assert games[3].timeline[5].role == (Roles.Civilian,)
    assert games[3].timeline[5].time == 225.0

    assert games[3].timeline[6].action_test == ActionTest.NoAT
    assert games[3].timeline[6].actor == "spy"
    assert games[3].timeline[6].books == (None,)
    assert games[3].timeline[6].cast_name == (Characters.Wheels,)
    assert games[3].timeline[6].category == TimelineCategory.Cast
    assert games[3].timeline[6].elapsed_time == 0.0
    assert games[3].timeline[6].event == "civilian cast."
    assert games[3].timeline[6].mission == Missions.NoMission
    assert games[3].timeline[6].role == (Roles.Civilian,)
    assert games[3].timeline[6].time == 225.0

    assert games[3].timeline[7].action_test == ActionTest.NoAT
    assert games[3].timeline[7].actor == "spy"
    assert games[3].timeline[7].books == (None,)
    assert games[3].timeline[7].cast_name == (Characters.Sikh,)
    assert games[3].timeline[7].category == TimelineCategory.Cast
    assert games[3].timeline[7].elapsed_time == 0.0
    assert games[3].timeline[7].event == "civilian cast."
    assert games[3].timeline[7].mission == Missions.NoMission
    assert games[3].timeline[7].role == (Roles.Civilian,)
    assert games[3].timeline[7].time == 225.0

    assert games[3].timeline[8].action_test == ActionTest.NoAT
    assert games[3].timeline[8].actor == "spy"
    assert games[3].timeline[8].books == (None,)
    assert games[3].timeline[8].cast_name == (Characters.Bling,)
    assert games[3].timeline[8].category == TimelineCategory.Cast
    assert games[3].timeline[8].elapsed_time == 0.0
    assert games[3].timeline[8].event == "civilian cast."
    assert games[3].timeline[8].mission == Missions.NoMission
    assert games[3].timeline[8].role == (Roles.Civilian,)
    assert games[3].timeline[8].time == 225.0

    assert games[3].timeline[9].action_test == ActionTest.NoAT
    assert games[3].timeline[9].actor == "spy"
    assert games[3].timeline[9].books == (None,)
    assert games[3].timeline[9].cast_name == (Characters.Helen,)
    assert games[3].timeline[9].category == TimelineCategory.Cast
    assert games[3].timeline[9].elapsed_time == 0.0
    assert games[3].timeline[9].event == "civilian cast."
    assert games[3].timeline[9].mission == Missions.NoMission
    assert games[3].timeline[9].role == (Roles.Civilian,)
    assert games[3].timeline[9].time == 225.0

    assert games[3].timeline[10].action_test == ActionTest.NoAT
    assert games[3].timeline[10].actor == "spy"
    assert games[3].timeline[10].books == (None,)
    assert games[3].timeline[10].cast_name == (Characters.Salmon,)
    assert games[3].timeline[10].category == TimelineCategory.Cast
    assert games[3].timeline[10].elapsed_time == 0.0
    assert games[3].timeline[10].event == "civilian cast."
    assert games[3].timeline[10].mission == Missions.NoMission
    assert games[3].timeline[10].role == (Roles.Civilian,)
    assert games[3].timeline[10].time == 225.0

    assert games[3].timeline[11].action_test == ActionTest.NoAT
    assert games[3].timeline[11].actor == "spy"
    assert games[3].timeline[11].books == (None,)
    assert games[3].timeline[11].cast_name == (Characters.Queen,)
    assert games[3].timeline[11].category == TimelineCategory.Cast
    assert games[3].timeline[11].elapsed_time == 0.0
    assert games[3].timeline[11].event == "civilian cast."
    assert games[3].timeline[11].mission == Missions.NoMission
    assert games[3].timeline[11].role == (Roles.Civilian,)
    assert games[3].timeline[11].time == 225.0

    assert games[3].timeline[12].action_test == ActionTest.NoAT
    assert games[3].timeline[12].actor == "spy"
    assert games[3].timeline[12].books == (None,)
    assert games[3].timeline[12].cast_name == (Characters.Rocker,)
    assert games[3].timeline[12].category == TimelineCategory.Cast
    assert games[3].timeline[12].elapsed_time == 0.0
    assert games[3].timeline[12].event == "civilian cast."
    assert games[3].timeline[12].mission == Missions.NoMission
    assert games[3].timeline[12].role == (Roles.Civilian,)
    assert games[3].timeline[12].time == 225.0

    assert games[3].timeline[13].action_test == ActionTest.NoAT
    assert games[3].timeline[13].actor == "spy"
    assert games[3].timeline[13].books == (None,)
    assert games[3].timeline[13].cast_name == (Characters.General,)
    assert games[3].timeline[13].category == TimelineCategory.Cast
    assert games[3].timeline[13].elapsed_time == 0.0
    assert games[3].timeline[13].event == "civilian cast."
    assert games[3].timeline[13].mission == Missions.NoMission
    assert games[3].timeline[13].role == (Roles.Civilian,)
    assert games[3].timeline[13].time == 225.0

    assert games[3].timeline[14].action_test == ActionTest.NoAT
    assert games[3].timeline[14].actor == "spy"
    assert games[3].timeline[14].books == (None,)
    assert games[3].timeline[14].cast_name == (Characters.Irish,)
    assert games[3].timeline[14].category == TimelineCategory.Cast
    assert games[3].timeline[14].elapsed_time == 0.0
    assert games[3].timeline[14].event == "civilian cast."
    assert games[3].timeline[14].mission == Missions.NoMission
    assert games[3].timeline[14].role == (Roles.Civilian,)
    assert games[3].timeline[14].time == 225.0

    assert games[3].timeline[15].action_test == ActionTest.NoAT
    assert games[3].timeline[15].actor == "spy"
    assert games[3].timeline[15].books == (None,)
    assert games[3].timeline[15].cast_name == (Characters.Morgan,)
    assert games[3].timeline[15].category == TimelineCategory.Cast
    assert games[3].timeline[15].elapsed_time == 0.0
    assert games[3].timeline[15].event == "civilian cast."
    assert games[3].timeline[15].mission == Missions.NoMission
    assert games[3].timeline[15].role == (Roles.Civilian,)
    assert games[3].timeline[15].time == 225.0

    assert games[3].timeline[16].action_test == ActionTest.NoAT
    assert games[3].timeline[16].actor == "spy"
    assert games[3].timeline[16].books == (None,)
    assert games[3].timeline[16].cast_name == (Characters.Carlos,)
    assert games[3].timeline[16].category == TimelineCategory.Cast
    assert games[3].timeline[16].elapsed_time == 0.0
    assert games[3].timeline[16].event == "civilian cast."
    assert games[3].timeline[16].mission == Missions.NoMission
    assert games[3].timeline[16].role == (Roles.Civilian,)
    assert games[3].timeline[16].time == 225.0

    assert games[3].timeline[17].action_test == ActionTest.NoAT
    assert games[3].timeline[17].actor == "spy"
    assert games[3].timeline[17].books == (None,)
    assert games[3].timeline[17].cast_name == (Characters.Sari,)
    assert games[3].timeline[17].category == TimelineCategory.Cast
    assert games[3].timeline[17].elapsed_time == 0.0
    assert games[3].timeline[17].event == "civilian cast."
    assert games[3].timeline[17].mission == Missions.NoMission
    assert games[3].timeline[17].role == (Roles.Civilian,)
    assert games[3].timeline[17].time == 225.0

    assert games[3].timeline[18].action_test == ActionTest.NoAT
    assert games[3].timeline[18].actor == "spy"
    assert games[3].timeline[18].books == (None,)
    assert games[3].timeline[18].cast_name == (Characters.Teal,)
    assert games[3].timeline[18].category == TimelineCategory.Cast
    assert games[3].timeline[18].elapsed_time == 0.0
    assert games[3].timeline[18].event == "civilian cast."
    assert games[3].timeline[18].mission == Missions.NoMission
    assert games[3].timeline[18].role == (Roles.Civilian,)
    assert games[3].timeline[18].time == 225.0

    assert games[3].timeline[19].action_test == ActionTest.NoAT
    assert games[3].timeline[19].actor == "spy"
    assert games[3].timeline[19].books == (None,)
    assert games[3].timeline[19].cast_name == (Characters.Alice,)
    assert games[3].timeline[19].category == TimelineCategory.Cast
    assert games[3].timeline[19].elapsed_time == 0.0
    assert games[3].timeline[19].event == "civilian cast."
    assert games[3].timeline[19].mission == Missions.NoMission
    assert games[3].timeline[19].role == (Roles.Civilian,)
    assert games[3].timeline[19].time == 225.0

    assert games[3].timeline[20].action_test == ActionTest.NoAT
    assert games[3].timeline[20].actor == "spy"
    assert games[3].timeline[20].books == (None,)
    assert games[3].timeline[20].cast_name == (Characters.Oprah,)
    assert games[3].timeline[20].category == TimelineCategory.Cast
    assert games[3].timeline[20].elapsed_time == 0.0
    assert games[3].timeline[20].event == "civilian cast."
    assert games[3].timeline[20].mission == Missions.NoMission
    assert games[3].timeline[20].role == (Roles.Civilian,)
    assert games[3].timeline[20].time == 225.0

    assert games[3].timeline[21].action_test == ActionTest.NoAT
    assert games[3].timeline[21].actor == "spy"
    assert games[3].timeline[21].books == (None,)
    assert games[3].timeline[21].cast_name == (None,)
    assert games[3].timeline[21].category == TimelineCategory.MissionSelected
    assert games[3].timeline[21].elapsed_time == 0.0
    assert games[3].timeline[21].event == "bug ambassador selected."
    assert games[3].timeline[21].mission == Missions.Bug
    assert games[3].timeline[21].role == (None,)
    assert games[3].timeline[21].time == 225.0

    assert games[3].timeline[22].action_test == ActionTest.NoAT
    assert games[3].timeline[22].actor == "spy"
    assert games[3].timeline[22].books == (None,)
    assert games[3].timeline[22].cast_name == (None,)
    assert games[3].timeline[22].category == TimelineCategory.MissionSelected
    assert games[3].timeline[22].elapsed_time == 0.0
    assert games[3].timeline[22].event == "contact double agent selected."
    assert games[3].timeline[22].mission == Missions.Contact
    assert games[3].timeline[22].role == (None,)
    assert games[3].timeline[22].time == 225.0

    assert games[3].timeline[23].action_test == ActionTest.NoAT
    assert games[3].timeline[23].actor == "spy"
    assert games[3].timeline[23].books == (None,)
    assert games[3].timeline[23].cast_name == (None,)
    assert games[3].timeline[23].category == TimelineCategory.MissionSelected
    assert games[3].timeline[23].elapsed_time == 0.0
    assert games[3].timeline[23].event == "transfer microfilm selected."
    assert games[3].timeline[23].mission == Missions.Transfer
    assert games[3].timeline[23].role == (None,)
    assert games[3].timeline[23].time == 225.0

    assert games[3].timeline[24].action_test == ActionTest.NoAT
    assert games[3].timeline[24].actor == "spy"
    assert games[3].timeline[24].books == (None,)
    assert games[3].timeline[24].cast_name == (None,)
    assert games[3].timeline[24].category == TimelineCategory.MissionSelected
    assert games[3].timeline[24].elapsed_time == 0.0
    assert games[3].timeline[24].event == "swap statue selected."
    assert games[3].timeline[24].mission == Missions.Swap
    assert games[3].timeline[24].role == (None,)
    assert games[3].timeline[24].time == 225.0

    assert games[3].timeline[25].action_test == ActionTest.NoAT
    assert games[3].timeline[25].actor == "spy"
    assert games[3].timeline[25].books == (None,)
    assert games[3].timeline[25].cast_name == (None,)
    assert games[3].timeline[25].category == TimelineCategory.MissionSelected
    assert games[3].timeline[25].elapsed_time == 0.0
    assert games[3].timeline[25].event == "inspect 3 statues selected."
    assert games[3].timeline[25].mission == Missions.Inspect
    assert games[3].timeline[25].role == (None,)
    assert games[3].timeline[25].time == 225.0

    assert games[3].timeline[26].action_test == ActionTest.NoAT
    assert games[3].timeline[26].actor == "spy"
    assert games[3].timeline[26].books == (None,)
    assert games[3].timeline[26].cast_name == (None,)
    assert games[3].timeline[26].category == TimelineCategory.MissionSelected
    assert games[3].timeline[26].elapsed_time == 0.0
    assert games[3].timeline[26].event == "seduce target selected."
    assert games[3].timeline[26].mission == Missions.Seduce
    assert games[3].timeline[26].role == (None,)
    assert games[3].timeline[26].time == 225.0

    assert games[3].timeline[27].action_test == ActionTest.NoAT
    assert games[3].timeline[27].actor == "spy"
    assert games[3].timeline[27].books == (None,)
    assert games[3].timeline[27].cast_name == (None,)
    assert games[3].timeline[27].category == TimelineCategory.MissionSelected
    assert games[3].timeline[27].elapsed_time == 0.0
    assert games[3].timeline[27].event == "purloin guest list selected."
    assert games[3].timeline[27].mission == Missions.Purloin
    assert games[3].timeline[27].role == (None,)
    assert games[3].timeline[27].time == 225.0

    assert games[3].timeline[28].action_test == ActionTest.NoAT
    assert games[3].timeline[28].actor == "spy"
    assert games[3].timeline[28].books == (None,)
    assert games[3].timeline[28].cast_name == (None,)
    assert games[3].timeline[28].category == TimelineCategory.MissionSelected
    assert games[3].timeline[28].elapsed_time == 0.0
    assert games[3].timeline[28].event == "fingerprint ambassador selected."
    assert games[3].timeline[28].mission == Missions.Fingerprint
    assert games[3].timeline[28].role == (None,)
    assert games[3].timeline[28].time == 225.0

    assert games[3].timeline[29].action_test == ActionTest.NoAT
    assert games[3].timeline[29].actor == "spy"
    assert games[3].timeline[29].books == (None,)
    assert games[3].timeline[29].cast_name == (None,)
    assert games[3].timeline[29].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[29].elapsed_time == 0.0
    assert games[3].timeline[29].event == "bug ambassador enabled."
    assert games[3].timeline[29].mission == Missions.Bug
    assert games[3].timeline[29].role == (None,)
    assert games[3].timeline[29].time == 225.0

    assert games[3].timeline[30].action_test == ActionTest.NoAT
    assert games[3].timeline[30].actor == "spy"
    assert games[3].timeline[30].books == (None,)
    assert games[3].timeline[30].cast_name == (None,)
    assert games[3].timeline[30].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[30].elapsed_time == 0.0
    assert games[3].timeline[30].event == "contact double agent enabled."
    assert games[3].timeline[30].mission == Missions.Contact
    assert games[3].timeline[30].role == (None,)
    assert games[3].timeline[30].time == 225.0

    assert games[3].timeline[31].action_test == ActionTest.NoAT
    assert games[3].timeline[31].actor == "spy"
    assert games[3].timeline[31].books == (None,)
    assert games[3].timeline[31].cast_name == (None,)
    assert games[3].timeline[31].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[31].elapsed_time == 0.0
    assert games[3].timeline[31].event == "transfer microfilm enabled."
    assert games[3].timeline[31].mission == Missions.Transfer
    assert games[3].timeline[31].role == (None,)
    assert games[3].timeline[31].time == 225.0

    assert games[3].timeline[32].action_test == ActionTest.NoAT
    assert games[3].timeline[32].actor == "spy"
    assert games[3].timeline[32].books == (None,)
    assert games[3].timeline[32].cast_name == (None,)
    assert games[3].timeline[32].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[32].elapsed_time == 0.0
    assert games[3].timeline[32].event == "swap statue enabled."
    assert games[3].timeline[32].mission == Missions.Swap
    assert games[3].timeline[32].role == (None,)
    assert games[3].timeline[32].time == 225.0

    assert games[3].timeline[33].action_test == ActionTest.NoAT
    assert games[3].timeline[33].actor == "spy"
    assert games[3].timeline[33].books == (None,)
    assert games[3].timeline[33].cast_name == (None,)
    assert games[3].timeline[33].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[33].elapsed_time == 0.0
    assert games[3].timeline[33].event == "inspect 3 statues enabled."
    assert games[3].timeline[33].mission == Missions.Inspect
    assert games[3].timeline[33].role == (None,)
    assert games[3].timeline[33].time == 225.0

    assert games[3].timeline[34].action_test == ActionTest.NoAT
    assert games[3].timeline[34].actor == "spy"
    assert games[3].timeline[34].books == (None,)
    assert games[3].timeline[34].cast_name == (None,)
    assert games[3].timeline[34].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[34].elapsed_time == 0.0
    assert games[3].timeline[34].event == "seduce target enabled."
    assert games[3].timeline[34].mission == Missions.Seduce
    assert games[3].timeline[34].role == (None,)
    assert games[3].timeline[34].time == 225.0

    assert games[3].timeline[35].action_test == ActionTest.NoAT
    assert games[3].timeline[35].actor == "spy"
    assert games[3].timeline[35].books == (None,)
    assert games[3].timeline[35].cast_name == (None,)
    assert games[3].timeline[35].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[35].elapsed_time == 0.0
    assert games[3].timeline[35].event == "purloin guest list enabled."
    assert games[3].timeline[35].mission == Missions.Purloin
    assert games[3].timeline[35].role == (None,)
    assert games[3].timeline[35].time == 225.0

    assert games[3].timeline[36].action_test == ActionTest.NoAT
    assert games[3].timeline[36].actor == "spy"
    assert games[3].timeline[36].books == (None,)
    assert games[3].timeline[36].cast_name == (None,)
    assert games[3].timeline[36].category == TimelineCategory.MissionEnabled
    assert games[3].timeline[36].elapsed_time == 0.0
    assert games[3].timeline[36].event == "fingerprint ambassador enabled."
    assert games[3].timeline[36].mission == Missions.Fingerprint
    assert games[3].timeline[36].role == (None,)
    assert games[3].timeline[36].time == 225.0

    assert games[3].timeline[37].action_test == ActionTest.NoAT
    assert games[3].timeline[37].actor == "game"
    assert games[3].timeline[37].books == (None,)
    assert games[3].timeline[37].cast_name == (None,)
    assert games[3].timeline[37].category == TimelineCategory.GameStart
    assert games[3].timeline[37].elapsed_time == 0.0
    assert games[3].timeline[37].event == "game started."
    assert games[3].timeline[37].mission == Missions.NoMission
    assert games[3].timeline[37].role == (None,)
    assert games[3].timeline[37].time == 225.0

    assert games[3].timeline[38].action_test == ActionTest.NoAT
    assert games[3].timeline[38].actor == "sniper"
    assert games[3].timeline[38].books == (None,)
    assert games[3].timeline[38].cast_name == (Characters.Salmon,)
    assert games[3].timeline[38].category == TimelineCategory.SniperLights
    assert games[3].timeline[38].elapsed_time == 3.31
    assert games[3].timeline[38].event == "marked suspicious."
    assert games[3].timeline[38].mission == Missions.NoMission
    assert games[3].timeline[38].role == (Roles.Civilian,)
    assert games[3].timeline[38].time == 221.6

    assert games[3].timeline[39].action_test == ActionTest.NoAT
    assert games[3].timeline[39].actor == "sniper"
    assert games[3].timeline[39].books == (None,)
    assert games[3].timeline[39].cast_name == (Characters.Taft,)
    assert games[3].timeline[39].category == TimelineCategory.SniperLights
    assert games[3].timeline[39].elapsed_time == 4.06
    assert games[3].timeline[39].event == "marked suspicious."
    assert games[3].timeline[39].mission == Missions.NoMission
    assert games[3].timeline[39].role == (Roles.Ambassador,)
    assert games[3].timeline[39].time == 220.9

    assert games[3].timeline[40].action_test == ActionTest.NoAT
    assert games[3].timeline[40].actor == "spy"
    assert games[3].timeline[40].books == (None,)
    assert games[3].timeline[40].cast_name == (None,)
    assert games[3].timeline[40].category == TimelineCategory.NoCategory
    assert games[3].timeline[40].elapsed_time == 4.81
    assert games[3].timeline[40].event == "spy player takes control from ai."
    assert games[3].timeline[40].mission == Missions.NoMission
    assert games[3].timeline[40].role == (None,)
    assert games[3].timeline[40].time == 220.1

    assert games[3].timeline[41].action_test == ActionTest.NoAT
    assert games[3].timeline[41].actor == "sniper"
    assert games[3].timeline[41].books == (None,)
    assert games[3].timeline[41].cast_name == (Characters.Salmon,)
    assert games[3].timeline[41].category == TimelineCategory.SniperLights
    assert games[3].timeline[41].elapsed_time == 4.94
    assert games[3].timeline[41].event == "marked neutral suspicion."
    assert games[3].timeline[41].mission == Missions.NoMission
    assert games[3].timeline[41].role == (Roles.Civilian,)
    assert games[3].timeline[41].time == 220.0

    assert games[3].timeline[42].action_test == ActionTest.NoAT
    assert games[3].timeline[42].actor == "spy"
    assert games[3].timeline[42].books == (None,)
    assert games[3].timeline[42].cast_name == (None,)
    assert games[3].timeline[42].category == TimelineCategory.Conversation
    assert games[3].timeline[42].elapsed_time == 9.5
    assert games[3].timeline[42].event == "spy enters conversation."
    assert games[3].timeline[42].mission == Missions.NoMission
    assert games[3].timeline[42].role == (None,)
    assert games[3].timeline[42].time == 215.5

    assert games[3].timeline[43].action_test == ActionTest.NoAT
    assert games[3].timeline[43].actor == "sniper"
    assert games[3].timeline[43].books == (None,)
    assert games[3].timeline[43].cast_name == (Characters.Duke,)
    assert games[3].timeline[43].category == TimelineCategory.SniperLights
    assert games[3].timeline[43].elapsed_time == 10.25
    assert games[3].timeline[43].event == "marked less suspicious."
    assert games[3].timeline[43].mission == Missions.NoMission
    assert games[3].timeline[43].role == (Roles.SuspectedDoubleAgent,)
    assert games[3].timeline[43].time == 214.7

    assert games[3].timeline[44].action_test == ActionTest.NoAT
    assert games[3].timeline[44].actor == "sniper"
    assert games[3].timeline[44].books == (None,)
    assert games[3].timeline[44].cast_name == (Characters.Damon,)
    assert games[3].timeline[44].category == TimelineCategory.SniperLights
    assert games[3].timeline[44].elapsed_time == 11.81
    assert games[3].timeline[44].event == "marked less suspicious."
    assert games[3].timeline[44].mission == Missions.NoMission
    assert games[3].timeline[44].role == (Roles.Staff,)
    assert games[3].timeline[44].time == 213.1

    assert games[3].timeline[45].action_test == ActionTest.NoAT
    assert games[3].timeline[45].actor == "sniper"
    assert games[3].timeline[45].books == (None,)
    assert games[3].timeline[45].cast_name == (Characters.Damon,)
    assert games[3].timeline[45].category == TimelineCategory.SniperLights
    assert games[3].timeline[45].elapsed_time == 12.69
    assert games[3].timeline[45].event == "marked neutral suspicion."
    assert games[3].timeline[45].mission == Missions.NoMission
    assert games[3].timeline[45].role == (Roles.Staff,)
    assert games[3].timeline[45].time == 212.3

    assert games[3].timeline[46].action_test == ActionTest.NoAT
    assert games[3].timeline[46].actor == "sniper"
    assert games[3].timeline[46].books == (None,)
    assert games[3].timeline[46].cast_name == (Characters.Toby,)
    assert games[3].timeline[46].category == TimelineCategory.SniperLights
    assert games[3].timeline[46].elapsed_time == 13.06
    assert games[3].timeline[46].event == "marked suspicious."
    assert games[3].timeline[46].mission == Missions.NoMission
    assert games[3].timeline[46].role == (Roles.Staff,)
    assert games[3].timeline[46].time == 211.9

    assert games[3].timeline[47].action_test == ActionTest.NoAT
    assert games[3].timeline[47].actor == "spy"
    assert games[3].timeline[47].books == (None,)
    assert games[3].timeline[47].cast_name == (Characters.Plain,)
    assert games[3].timeline[47].category == TimelineCategory.Drinks
    assert games[3].timeline[47].elapsed_time == 20.31
    assert games[3].timeline[47].event == "took last sip of drink."
    assert games[3].timeline[47].mission == Missions.NoMission
    assert games[3].timeline[47].role == (Roles.Spy,)
    assert games[3].timeline[47].time == 204.6

    assert games[3].timeline[48].action_test == ActionTest.NoAT
    assert games[3].timeline[48].actor == "sniper"
    assert games[3].timeline[48].books == (None,)
    assert games[3].timeline[48].cast_name == (Characters.Helen,)
    assert games[3].timeline[48].category == TimelineCategory.SniperLights
    assert games[3].timeline[48].elapsed_time == 23.31
    assert games[3].timeline[48].event == "marked less suspicious."
    assert games[3].timeline[48].mission == Missions.NoMission
    assert games[3].timeline[48].role == (Roles.Civilian,)
    assert games[3].timeline[48].time == 201.6

    assert games[3].timeline[49].action_test == ActionTest.NoAT
    assert games[3].timeline[49].actor == "spy"
    assert games[3].timeline[49].books == (None,)
    assert games[3].timeline[49].cast_name == (None,)
    assert games[3].timeline[49].category == TimelineCategory.ActionTriggered
    assert games[3].timeline[49].elapsed_time == 26.69
    assert games[3].timeline[49].event == "action triggered: seduce target"
    assert games[3].timeline[49].mission == Missions.Seduce
    assert games[3].timeline[49].role == (None,)
    assert games[3].timeline[49].time == 198.3

    assert games[3].timeline[50].action_test == ActionTest.NoAT
    assert games[3].timeline[50].actor == "spy"
    assert games[3].timeline[50].books == (None,)
    assert games[3].timeline[50].cast_name == (Characters.Smallman,)
    assert games[3].timeline[50].category == TimelineCategory.NoCategory
    assert games[3].timeline[50].elapsed_time == 26.69
    assert games[3].timeline[50].event == "begin flirtation with seduction target."
    assert games[3].timeline[50].mission == Missions.Seduce
    assert games[3].timeline[50].role == (Roles.SeductionTarget,)
    assert games[3].timeline[50].time == 198.3

    assert games[3].timeline[51].action_test == ActionTest.White
    assert games[3].timeline[51].actor == "spy"
    assert games[3].timeline[51].books == (None,)
    assert games[3].timeline[51].cast_name == (None,)
    assert games[3].timeline[51].category == TimelineCategory.ActionTest
    assert games[3].timeline[51].elapsed_time == 27.5
    assert games[3].timeline[51].event == "action test white: seduce target"
    assert games[3].timeline[51].mission == Missions.Seduce
    assert games[3].timeline[51].role == (None,)
    assert games[3].timeline[51].time == 197.5

    assert games[3].timeline[52].action_test == ActionTest.NoAT
    assert games[3].timeline[52].actor == "spy"
    assert games[3].timeline[52].books == (None,)
    assert games[3].timeline[52].cast_name == (Characters.Smallman,)
    assert games[3].timeline[52].category == TimelineCategory.MissionPartial
    assert games[3].timeline[52].elapsed_time == 27.5
    assert games[3].timeline[52].event == "flirt with seduction target: 22%"
    assert games[3].timeline[52].mission == Missions.Seduce
    assert games[3].timeline[52].role == (Roles.SeductionTarget,)
    assert games[3].timeline[52].time == 197.5

    assert games[3].timeline[53].action_test == ActionTest.NoAT
    assert games[3].timeline[53].actor == "sniper"
    assert games[3].timeline[53].books == (None,)
    assert games[3].timeline[53].cast_name == (Characters.Disney,)
    assert games[3].timeline[53].category == TimelineCategory.SniperLights
    assert games[3].timeline[53].elapsed_time == 32.44
    assert games[3].timeline[53].event == "marked less suspicious."
    assert games[3].timeline[53].mission == Missions.NoMission
    assert games[3].timeline[53].role == (Roles.DoubleAgent,)
    assert games[3].timeline[53].time == 192.5

    assert games[3].timeline[54].action_test == ActionTest.NoAT
    assert games[3].timeline[54].actor == "spy"
    assert games[3].timeline[54].books == (None,)
    assert games[3].timeline[54].cast_name == (None,)
    assert games[3].timeline[54].category == TimelineCategory.NoCategory
    assert games[3].timeline[54].elapsed_time == 41.13
    assert games[3].timeline[54].event == "flirtation cooldown expired."
    assert games[3].timeline[54].mission == Missions.Seduce
    assert games[3].timeline[54].role == (None,)
    assert games[3].timeline[54].time == 183.8

    assert games[3].timeline[55].action_test == ActionTest.NoAT
    assert games[3].timeline[55].actor == "spy"
    assert games[3].timeline[55].books == (None,)
    assert games[3].timeline[55].cast_name == (None,)
    assert games[3].timeline[55].category == TimelineCategory.ActionTriggered
    assert games[3].timeline[55].elapsed_time == 50.19
    assert games[3].timeline[55].event == "action triggered: seduce target"
    assert games[3].timeline[55].mission == Missions.Seduce
    assert games[3].timeline[55].role == (None,)
    assert games[3].timeline[55].time == 174.8

    assert games[3].timeline[56].action_test == ActionTest.NoAT
    assert games[3].timeline[56].actor == "spy"
    assert games[3].timeline[56].books == (None,)
    assert games[3].timeline[56].cast_name == (Characters.Smallman,)
    assert games[3].timeline[56].category == TimelineCategory.NoCategory
    assert games[3].timeline[56].elapsed_time == 50.19
    assert games[3].timeline[56].event == "begin flirtation with seduction target."
    assert games[3].timeline[56].mission == Missions.Seduce
    assert games[3].timeline[56].role == (Roles.SeductionTarget,)
    assert games[3].timeline[56].time == 174.8

    assert games[3].timeline[57].action_test == ActionTest.Green
    assert games[3].timeline[57].actor == "spy"
    assert games[3].timeline[57].books == (None,)
    assert games[3].timeline[57].cast_name == (None,)
    assert games[3].timeline[57].category == TimelineCategory.ActionTest
    assert games[3].timeline[57].elapsed_time == 50.88
    assert games[3].timeline[57].event == "action test green: seduce target"
    assert games[3].timeline[57].mission == Missions.Seduce
    assert games[3].timeline[57].role == (None,)
    assert games[3].timeline[57].time == 174.1

    assert games[3].timeline[58].action_test == ActionTest.NoAT
    assert games[3].timeline[58].actor == "spy"
    assert games[3].timeline[58].books == (None,)
    assert games[3].timeline[58].cast_name == (Characters.Smallman,)
    assert games[3].timeline[58].category == TimelineCategory.MissionPartial
    assert games[3].timeline[58].elapsed_time == 50.88
    assert games[3].timeline[58].event == "flirt with seduction target: 58%"
    assert games[3].timeline[58].mission == Missions.Seduce
    assert games[3].timeline[58].role == (Roles.SeductionTarget,)
    assert games[3].timeline[58].time == 174.1

    assert games[3].timeline[59].action_test == ActionTest.NoAT
    assert games[3].timeline[59].actor == "sniper"
    assert games[3].timeline[59].books == (None,)
    assert games[3].timeline[59].cast_name == (Characters.Damon,)
    assert games[3].timeline[59].category == TimelineCategory.SniperLights
    assert games[3].timeline[59].elapsed_time == 53.44
    assert games[3].timeline[59].event == "marked less suspicious."
    assert games[3].timeline[59].mission == Missions.NoMission
    assert games[3].timeline[59].role == (Roles.Staff,)
    assert games[3].timeline[59].time == 171.5

    assert games[3].timeline[60].action_test == ActionTest.NoAT
    assert games[3].timeline[60].actor == "spy"
    assert games[3].timeline[60].books == (None,)
    assert games[3].timeline[60].cast_name == (None,)
    assert games[3].timeline[60].category == TimelineCategory.Conversation
    assert games[3].timeline[60].elapsed_time == 64.06
    assert games[3].timeline[60].event == "spy leaves conversation."
    assert games[3].timeline[60].mission == Missions.NoMission
    assert games[3].timeline[60].role == (None,)
    assert games[3].timeline[60].time == 160.9

    assert games[3].timeline[61].action_test == ActionTest.NoAT
    assert games[3].timeline[61].actor == "spy"
    assert games[3].timeline[61].books == (None,)
    assert games[3].timeline[61].cast_name == (None,)
    assert games[3].timeline[61].category == TimelineCategory.NoCategory
    assert games[3].timeline[61].elapsed_time == 70.25
    assert games[3].timeline[61].event == "flirtation cooldown expired."
    assert games[3].timeline[61].mission == Missions.Seduce
    assert games[3].timeline[61].role == (None,)
    assert games[3].timeline[61].time == 154.7

    assert games[3].timeline[62].action_test == ActionTest.NoAT
    assert games[3].timeline[62].actor == "spy"
    assert games[3].timeline[62].books == (None,)
    assert games[3].timeline[62].cast_name == (None,)
    assert games[3].timeline[62].category == TimelineCategory.Briefcase
    assert games[3].timeline[62].elapsed_time == 81.94
    assert games[3].timeline[62].event == "spy picks up briefcase."
    assert games[3].timeline[62].mission == Missions.NoMission
    assert games[3].timeline[62].role == (None,)
    assert games[3].timeline[62].time == 143.0

    assert games[3].timeline[63].action_test == ActionTest.NoAT
    assert games[3].timeline[63].actor == "spy"
    assert games[3].timeline[63].books == (None,)
    assert games[3].timeline[63].cast_name == (None,)
    assert games[3].timeline[63].category == TimelineCategory.Briefcase
    assert games[3].timeline[63].elapsed_time == 81.94
    assert games[3].timeline[63].event == "picked up fingerprintable briefcase."
    assert games[3].timeline[63].mission == Missions.Fingerprint
    assert games[3].timeline[63].role == (None,)
    assert games[3].timeline[63].time == 143.0

    assert games[3].timeline[64].action_test == ActionTest.NoAT
    assert games[3].timeline[64].actor == "spy"
    assert games[3].timeline[64].books == (None,)
    assert games[3].timeline[64].cast_name == (None,)
    assert games[3].timeline[64].category == TimelineCategory.ActionTriggered
    assert games[3].timeline[64].elapsed_time == 84.94
    assert games[3].timeline[64].event == "action triggered: fingerprint ambassador"
    assert games[3].timeline[64].mission == Missions.Fingerprint
    assert games[3].timeline[64].role == (None,)
    assert games[3].timeline[64].time == 140.0

    assert games[3].timeline[65].action_test == ActionTest.NoAT
    assert games[3].timeline[65].actor == "spy"
    assert games[3].timeline[65].books == (None,)
    assert games[3].timeline[65].cast_name == (None,)
    assert games[3].timeline[65].category == TimelineCategory.Briefcase
    assert games[3].timeline[65].elapsed_time == 84.94
    assert games[3].timeline[65].event == "started fingerprinting briefcase."
    assert games[3].timeline[65].mission == Missions.Fingerprint
    assert games[3].timeline[65].role == (None,)
    assert games[3].timeline[65].time == 140.0

    assert games[3].timeline[66].action_test == ActionTest.NoAT
    assert games[3].timeline[66].actor == "spy"
    assert games[3].timeline[66].books == (None,)
    assert games[3].timeline[66].cast_name == (None,)
    assert (
        games[3].timeline[66].category
        == TimelineCategory.MissionPartial | TimelineCategory.Briefcase
    )
    assert games[3].timeline[66].elapsed_time == 85.94
    assert games[3].timeline[66].event == "fingerprinted briefcase."
    assert games[3].timeline[66].mission == Missions.Fingerprint
    assert games[3].timeline[66].role == (None,)
    assert games[3].timeline[66].time == 139.0

    assert games[3].timeline[67].action_test == ActionTest.NoAT
    assert games[3].timeline[67].actor == "spy"
    assert games[3].timeline[67].books == (None,)
    assert games[3].timeline[67].cast_name == (None,)
    assert games[3].timeline[67].category == TimelineCategory.Briefcase
    assert games[3].timeline[67].elapsed_time == 94.19
    assert games[3].timeline[67].event == "spy returns briefcase."
    assert games[3].timeline[67].mission == Missions.NoMission
    assert games[3].timeline[67].role == (None,)
    assert games[3].timeline[67].time == 130.8

    assert games[3].timeline[68].action_test == ActionTest.NoAT
    assert games[3].timeline[68].actor == "sniper"
    assert games[3].timeline[68].books == (None,)
    assert games[3].timeline[68].cast_name == (Characters.Boots,)
    assert games[3].timeline[68].category == TimelineCategory.SniperLights
    assert games[3].timeline[68].elapsed_time == 95.13
    assert games[3].timeline[68].event == "marked suspicious."
    assert games[3].timeline[68].mission == Missions.NoMission
    assert games[3].timeline[68].role == (Roles.Civilian,)
    assert games[3].timeline[68].time == 129.8

    assert games[3].timeline[69].action_test == ActionTest.NoAT
    assert games[3].timeline[69].actor == "spy"
    assert games[3].timeline[69].books == (None,)
    assert games[3].timeline[69].cast_name == (None,)
    assert games[3].timeline[69].category == TimelineCategory.Statues
    assert games[3].timeline[69].elapsed_time == 101.06
    assert games[3].timeline[69].event == "picked up statue."
    assert games[3].timeline[69].mission == Missions.NoMission
    assert games[3].timeline[69].role == (None,)
    assert games[3].timeline[69].time == 123.9

    assert games[3].timeline[70].action_test == ActionTest.NoAT
    assert games[3].timeline[70].actor == "spy"
    assert games[3].timeline[70].books == (None,)
    assert games[3].timeline[70].cast_name == (None,)
    assert (
        games[3].timeline[70].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[3].timeline[70].elapsed_time == 105.13
    assert games[3].timeline[70].event == "action triggered: inspect statues"
    assert games[3].timeline[70].mission == Missions.Inspect
    assert games[3].timeline[70].role == (None,)
    assert games[3].timeline[70].time == 119.8

    assert games[3].timeline[71].action_test == ActionTest.White
    assert games[3].timeline[71].actor == "spy"
    assert games[3].timeline[71].books == (None,)
    assert games[3].timeline[71].cast_name == (None,)
    assert (
        games[3].timeline[71].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[3].timeline[71].elapsed_time == 105.94
    assert games[3].timeline[71].event == "action test white: inspect statues"
    assert games[3].timeline[71].mission == Missions.Inspect
    assert games[3].timeline[71].role == (None,)
    assert games[3].timeline[71].time == 119.0

    assert games[3].timeline[72].action_test == ActionTest.NoAT
    assert games[3].timeline[72].actor == "spy"
    assert games[3].timeline[72].books == (None,)
    assert games[3].timeline[72].cast_name == (None,)
    assert (
        games[3].timeline[72].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[3].timeline[72].elapsed_time == 110.13
    assert games[3].timeline[72].event == "right statue inspected."
    assert games[3].timeline[72].mission == Missions.Inspect
    assert games[3].timeline[72].role == (None,)
    assert games[3].timeline[72].time == 114.8

    assert games[3].timeline[73].action_test == ActionTest.NoAT
    assert games[3].timeline[73].actor == "spy"
    assert games[3].timeline[73].books == (None,)
    assert games[3].timeline[73].cast_name == (None,)
    assert (
        games[3].timeline[73].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[3].timeline[73].elapsed_time == 110.81
    assert games[3].timeline[73].event == "action triggered: inspect statues"
    assert games[3].timeline[73].mission == Missions.Inspect
    assert games[3].timeline[73].role == (None,)
    assert games[3].timeline[73].time == 114.1

    assert games[3].timeline[74].action_test == ActionTest.White
    assert games[3].timeline[74].actor == "spy"
    assert games[3].timeline[74].books == (None,)
    assert games[3].timeline[74].cast_name == (None,)
    assert (
        games[3].timeline[74].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[3].timeline[74].elapsed_time == 111.75
    assert games[3].timeline[74].event == "action test white: inspect statues"
    assert games[3].timeline[74].mission == Missions.Inspect
    assert games[3].timeline[74].role == (None,)
    assert games[3].timeline[74].time == 113.2

    assert games[3].timeline[75].action_test == ActionTest.NoAT
    assert games[3].timeline[75].actor == "sniper"
    assert games[3].timeline[75].books == (None,)
    assert games[3].timeline[75].cast_name == (Characters.Smallman,)
    assert games[3].timeline[75].category == TimelineCategory.SniperLights
    assert games[3].timeline[75].elapsed_time == 113.25
    assert games[3].timeline[75].event == "marked suspicious."
    assert games[3].timeline[75].mission == Missions.NoMission
    assert games[3].timeline[75].role == (Roles.SeductionTarget,)
    assert games[3].timeline[75].time == 111.7

    assert games[3].timeline[76].action_test == ActionTest.NoAT
    assert games[3].timeline[76].actor == "sniper"
    assert games[3].timeline[76].books == (None,)
    assert games[3].timeline[76].cast_name == (Characters.Plain,)
    assert games[3].timeline[76].category == TimelineCategory.SniperLights
    assert games[3].timeline[76].elapsed_time == 113.75
    assert games[3].timeline[76].event == "marked spy suspicious."
    assert games[3].timeline[76].mission == Missions.NoMission
    assert games[3].timeline[76].role == (Roles.Spy,)
    assert games[3].timeline[76].time == 111.2

    assert games[3].timeline[77].action_test == ActionTest.NoAT
    assert games[3].timeline[77].actor == "sniper"
    assert games[3].timeline[77].books == (None,)
    assert games[3].timeline[77].cast_name == (Characters.Alice,)
    assert games[3].timeline[77].category == TimelineCategory.SniperLights
    assert games[3].timeline[77].elapsed_time == 114.06
    assert games[3].timeline[77].event == "marked suspicious."
    assert games[3].timeline[77].mission == Missions.NoMission
    assert games[3].timeline[77].role == (Roles.Civilian,)
    assert games[3].timeline[77].time == 110.9

    assert games[3].timeline[78].action_test == ActionTest.NoAT
    assert games[3].timeline[78].actor == "spy"
    assert games[3].timeline[78].books == (None,)
    assert games[3].timeline[78].cast_name == (None,)
    assert (
        games[3].timeline[78].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[3].timeline[78].elapsed_time == 114.81
    assert games[3].timeline[78].event == "held statue inspected."
    assert games[3].timeline[78].mission == Missions.Inspect
    assert games[3].timeline[78].role == (None,)
    assert games[3].timeline[78].time == 110.1

    assert games[3].timeline[79].action_test == ActionTest.NoAT
    assert games[3].timeline[79].actor == "spy"
    assert games[3].timeline[79].books == (None,)
    assert games[3].timeline[79].cast_name == (None,)
    assert games[3].timeline[79].category == TimelineCategory.Statues
    assert games[3].timeline[79].elapsed_time == 117.13
    assert games[3].timeline[79].event == "put back statue."
    assert games[3].timeline[79].mission == Missions.NoMission
    assert games[3].timeline[79].role == (None,)
    assert games[3].timeline[79].time == 107.8

    assert games[3].timeline[80].action_test == ActionTest.NoAT
    assert games[3].timeline[80].actor == "spy"
    assert games[3].timeline[80].books == (None,)
    assert games[3].timeline[80].cast_name == (Characters.Plain,)
    assert games[3].timeline[80].category == TimelineCategory.Drinks
    assert games[3].timeline[80].elapsed_time == 133.63
    assert games[3].timeline[80].event == "waiter offered drink."
    assert games[3].timeline[80].mission == Missions.NoMission
    assert games[3].timeline[80].role == (Roles.Spy,)
    assert games[3].timeline[80].time == 91.3

    assert games[3].timeline[81].action_test == ActionTest.NoAT
    assert games[3].timeline[81].actor == "spy"
    assert games[3].timeline[81].books == (None,)
    assert games[3].timeline[81].cast_name == (Characters.Plain,)
    assert games[3].timeline[81].category == TimelineCategory.Drinks
    assert games[3].timeline[81].elapsed_time == 135.56
    assert games[3].timeline[81].event == "rejected drink from waiter."
    assert games[3].timeline[81].mission == Missions.NoMission
    assert games[3].timeline[81].role == (Roles.Spy,)
    assert games[3].timeline[81].time == 89.4

    assert games[3].timeline[82].action_test == ActionTest.NoAT
    assert games[3].timeline[82].actor == "spy"
    assert games[3].timeline[82].books == (None,)
    assert games[3].timeline[82].cast_name == (Characters.Plain,)
    assert games[3].timeline[82].category == TimelineCategory.Drinks
    assert games[3].timeline[82].elapsed_time == 135.56
    assert games[3].timeline[82].event == "waiter stopped offering drink."
    assert games[3].timeline[82].mission == Missions.NoMission
    assert games[3].timeline[82].role == (Roles.Spy,)
    assert games[3].timeline[82].time == 89.4

    assert games[3].timeline[83].action_test == ActionTest.NoAT
    assert games[3].timeline[83].actor == "spy"
    assert games[3].timeline[83].books == (None,)
    assert games[3].timeline[83].cast_name == (None,)
    assert games[3].timeline[83].category == TimelineCategory.Conversation
    assert games[3].timeline[83].elapsed_time == 138.5
    assert games[3].timeline[83].event == "spy enters conversation."
    assert games[3].timeline[83].mission == Missions.NoMission
    assert games[3].timeline[83].role == (None,)
    assert games[3].timeline[83].time == 86.5

    assert games[3].timeline[84].action_test == ActionTest.NoAT
    assert games[3].timeline[84].actor == "spy"
    assert games[3].timeline[84].books == (None,)
    assert games[3].timeline[84].cast_name == (None,)
    assert games[3].timeline[84].category == TimelineCategory.ActionTriggered
    assert games[3].timeline[84].elapsed_time == 141.75
    assert games[3].timeline[84].event == "action triggered: seduce target"
    assert games[3].timeline[84].mission == Missions.Seduce
    assert games[3].timeline[84].role == (None,)
    assert games[3].timeline[84].time == 83.2

    assert games[3].timeline[85].action_test == ActionTest.NoAT
    assert games[3].timeline[85].actor == "spy"
    assert games[3].timeline[85].books == (None,)
    assert games[3].timeline[85].cast_name == (Characters.Smallman,)
    assert games[3].timeline[85].category == TimelineCategory.NoCategory
    assert games[3].timeline[85].elapsed_time == 141.75
    assert games[3].timeline[85].event == "begin flirtation with seduction target."
    assert games[3].timeline[85].mission == Missions.Seduce
    assert games[3].timeline[85].role == (Roles.SeductionTarget,)
    assert games[3].timeline[85].time == 83.2

    assert games[3].timeline[86].action_test == ActionTest.White
    assert games[3].timeline[86].actor == "spy"
    assert games[3].timeline[86].books == (None,)
    assert games[3].timeline[86].cast_name == (None,)
    assert games[3].timeline[86].category == TimelineCategory.ActionTest
    assert games[3].timeline[86].elapsed_time == 142.63
    assert games[3].timeline[86].event == "action test white: seduce target"
    assert games[3].timeline[86].mission == Missions.Seduce
    assert games[3].timeline[86].role == (None,)
    assert games[3].timeline[86].time == 82.3

    assert games[3].timeline[87].action_test == ActionTest.NoAT
    assert games[3].timeline[87].actor == "spy"
    assert games[3].timeline[87].books == (None,)
    assert games[3].timeline[87].cast_name == (Characters.Smallman,)
    assert games[3].timeline[87].category == TimelineCategory.MissionPartial
    assert games[3].timeline[87].elapsed_time == 142.63
    assert games[3].timeline[87].event == "flirt with seduction target: 92%"
    assert games[3].timeline[87].mission == Missions.Seduce
    assert games[3].timeline[87].role == (Roles.SeductionTarget,)
    assert games[3].timeline[87].time == 82.3

    assert games[3].timeline[88].action_test == ActionTest.NoAT
    assert games[3].timeline[88].actor == "spy"
    assert games[3].timeline[88].books == (None,)
    assert games[3].timeline[88].cast_name == (Characters.Disney,)
    assert games[3].timeline[88].category == TimelineCategory.Conversation
    assert games[3].timeline[88].elapsed_time == 152.69
    assert games[3].timeline[88].event == "double agent joined conversation with spy."
    assert games[3].timeline[88].mission == Missions.NoMission
    assert games[3].timeline[88].role == (Roles.DoubleAgent,)
    assert games[3].timeline[88].time == 72.3

    assert games[3].timeline[89].action_test == ActionTest.NoAT
    assert games[3].timeline[89].actor == "spy"
    assert games[3].timeline[89].books == (None,)
    assert games[3].timeline[89].cast_name == (None,)
    assert games[3].timeline[89].category == TimelineCategory.ActionTriggered
    assert games[3].timeline[89].elapsed_time == 154.81
    assert games[3].timeline[89].event == "action triggered: contact double agent"
    assert games[3].timeline[89].mission == Missions.Contact
    assert games[3].timeline[89].role == (None,)
    assert games[3].timeline[89].time == 70.1

    assert games[3].timeline[90].action_test == ActionTest.NoAT
    assert games[3].timeline[90].actor == "spy"
    assert games[3].timeline[90].books == (None,)
    assert games[3].timeline[90].cast_name == (None,)
    assert games[3].timeline[90].category == TimelineCategory.BananaBread
    assert games[3].timeline[90].elapsed_time == 154.81
    assert games[3].timeline[90].event == "real banana bread started."
    assert games[3].timeline[90].mission == Missions.Contact
    assert games[3].timeline[90].role == (None,)
    assert games[3].timeline[90].time == 70.1

    assert games[3].timeline[91].action_test == ActionTest.Green
    assert games[3].timeline[91].actor == "spy"
    assert games[3].timeline[91].books == (None,)
    assert games[3].timeline[91].cast_name == (None,)
    assert games[3].timeline[91].category == TimelineCategory.ActionTest
    assert games[3].timeline[91].elapsed_time == 155.94
    assert games[3].timeline[91].event == "action test green: contact double agent"
    assert games[3].timeline[91].mission == Missions.Contact
    assert games[3].timeline[91].role == (None,)
    assert games[3].timeline[91].time == 69.0

    assert games[3].timeline[92].action_test == ActionTest.NoAT
    assert games[3].timeline[92].actor == "spy"
    assert games[3].timeline[92].books == (None,)
    assert games[3].timeline[92].cast_name == (None,)
    assert games[3].timeline[92].category == TimelineCategory.BananaBread
    assert games[3].timeline[92].elapsed_time == 155.94
    assert games[3].timeline[92].event == "banana bread uttered."
    assert games[3].timeline[92].mission == Missions.Contact
    assert games[3].timeline[92].role == (None,)
    assert games[3].timeline[92].time == 69.0

    assert games[3].timeline[93].action_test == ActionTest.NoAT
    assert games[3].timeline[93].actor == "spy"
    assert games[3].timeline[93].books == (None,)
    assert games[3].timeline[93].cast_name == (Characters.Disney,)
    assert games[3].timeline[93].category == TimelineCategory.MissionComplete
    assert games[3].timeline[93].elapsed_time == 156.5
    assert games[3].timeline[93].event == "double agent contacted."
    assert games[3].timeline[93].mission == Missions.Contact
    assert games[3].timeline[93].role == (Roles.DoubleAgent,)
    assert games[3].timeline[93].time == 68.4

    assert games[3].timeline[94].action_test == ActionTest.NoAT
    assert games[3].timeline[94].actor == "sniper"
    assert games[3].timeline[94].books == (None,)
    assert games[3].timeline[94].cast_name == (Characters.Morgan,)
    assert games[3].timeline[94].category == TimelineCategory.SniperLights
    assert games[3].timeline[94].elapsed_time == 157.5
    assert games[3].timeline[94].event == "marked less suspicious."
    assert games[3].timeline[94].mission == Missions.NoMission
    assert games[3].timeline[94].role == (Roles.Civilian,)
    assert games[3].timeline[94].time == 67.5

    assert games[3].timeline[95].action_test == ActionTest.NoAT
    assert games[3].timeline[95].actor == "sniper"
    assert games[3].timeline[95].books == (None,)
    assert games[3].timeline[95].cast_name == (Characters.Salmon,)
    assert games[3].timeline[95].category == TimelineCategory.SniperLights
    assert games[3].timeline[95].elapsed_time == 158.44
    assert games[3].timeline[95].event == "marked less suspicious."
    assert games[3].timeline[95].mission == Missions.NoMission
    assert games[3].timeline[95].role == (Roles.Civilian,)
    assert games[3].timeline[95].time == 66.5

    assert games[3].timeline[96].action_test == ActionTest.NoAT
    assert games[3].timeline[96].actor == "sniper"
    assert games[3].timeline[96].books == (None,)
    assert games[3].timeline[96].cast_name == (Characters.Oprah,)
    assert games[3].timeline[96].category == TimelineCategory.SniperLights
    assert games[3].timeline[96].elapsed_time == 158.88
    assert games[3].timeline[96].event == "marked less suspicious."
    assert games[3].timeline[96].mission == Missions.NoMission
    assert games[3].timeline[96].role == (Roles.Civilian,)
    assert games[3].timeline[96].time == 66.1

    assert games[3].timeline[97].action_test == ActionTest.NoAT
    assert games[3].timeline[97].actor == "sniper"
    assert games[3].timeline[97].books == (None,)
    assert games[3].timeline[97].cast_name == (Characters.Bling,)
    assert games[3].timeline[97].category == TimelineCategory.SniperLights
    assert games[3].timeline[97].elapsed_time == 161.44
    assert games[3].timeline[97].event == "marked less suspicious."
    assert games[3].timeline[97].mission == Missions.NoMission
    assert games[3].timeline[97].role == (Roles.Civilian,)
    assert games[3].timeline[97].time == 63.5

    assert games[3].timeline[98].action_test == ActionTest.NoAT
    assert games[3].timeline[98].actor == "spy"
    assert games[3].timeline[98].books == (None,)
    assert games[3].timeline[98].cast_name == (Characters.Plain,)
    assert games[3].timeline[98].category == TimelineCategory.Drinks
    assert games[3].timeline[98].elapsed_time == 161.88
    assert games[3].timeline[98].event == "request drink from waiter."
    assert games[3].timeline[98].mission == Missions.NoMission
    assert games[3].timeline[98].role == (Roles.Spy,)
    assert games[3].timeline[98].time == 63.1

    assert games[3].timeline[99].action_test == ActionTest.NoAT
    assert games[3].timeline[99].actor == "sniper"
    assert games[3].timeline[99].books == (None,)
    assert games[3].timeline[99].cast_name == (Characters.Helen,)
    assert games[3].timeline[99].category == TimelineCategory.SniperLights
    assert games[3].timeline[99].elapsed_time == 163.81
    assert games[3].timeline[99].event == "marked neutral suspicion."
    assert games[3].timeline[99].mission == Missions.NoMission
    assert games[3].timeline[99].role == (Roles.Civilian,)
    assert games[3].timeline[99].time == 61.1

    assert games[3].timeline[100].action_test == ActionTest.NoAT
    assert games[3].timeline[100].actor == "sniper"
    assert games[3].timeline[100].books == (None,)
    assert games[3].timeline[100].cast_name == (Characters.Queen,)
    assert games[3].timeline[100].category == TimelineCategory.SniperLights
    assert games[3].timeline[100].elapsed_time == 165.06
    assert games[3].timeline[100].event == "marked less suspicious."
    assert games[3].timeline[100].mission == Missions.NoMission
    assert games[3].timeline[100].role == (Roles.Civilian,)
    assert games[3].timeline[100].time == 59.9

    assert games[3].timeline[101].action_test == ActionTest.NoAT
    assert games[3].timeline[101].actor == "sniper"
    assert games[3].timeline[101].books == (None,)
    assert games[3].timeline[101].cast_name == (Characters.Sikh,)
    assert games[3].timeline[101].category == TimelineCategory.SniperLights
    assert games[3].timeline[101].elapsed_time == 165.38
    assert games[3].timeline[101].event == "marked less suspicious."
    assert games[3].timeline[101].mission == Missions.NoMission
    assert games[3].timeline[101].role == (Roles.Civilian,)
    assert games[3].timeline[101].time == 59.6

    assert games[3].timeline[102].action_test == ActionTest.NoAT
    assert games[3].timeline[102].actor == "spy"
    assert games[3].timeline[102].books == (None,)
    assert games[3].timeline[102].cast_name == (Characters.Plain,)
    assert games[3].timeline[102].category == TimelineCategory.Drinks
    assert games[3].timeline[102].elapsed_time == 167.69
    assert games[3].timeline[102].event == "waiter offered drink."
    assert games[3].timeline[102].mission == Missions.NoMission
    assert games[3].timeline[102].role == (Roles.Spy,)
    assert games[3].timeline[102].time == 57.3

    assert games[3].timeline[103].action_test == ActionTest.NoAT
    assert games[3].timeline[103].actor == "spy"
    assert games[3].timeline[103].books == (None,)
    assert games[3].timeline[103].cast_name == (Characters.Plain,)
    assert games[3].timeline[103].category == TimelineCategory.Drinks
    assert games[3].timeline[103].elapsed_time == 172.63
    assert games[3].timeline[103].event == "got drink from waiter."
    assert games[3].timeline[103].mission == Missions.NoMission
    assert games[3].timeline[103].role == (Roles.Spy,)
    assert games[3].timeline[103].time == 52.3

    assert games[3].timeline[104].action_test == ActionTest.NoAT
    assert games[3].timeline[104].actor == "spy"
    assert games[3].timeline[104].books == (None,)
    assert games[3].timeline[104].cast_name == (Characters.Plain,)
    assert games[3].timeline[104].category == TimelineCategory.Drinks
    assert games[3].timeline[104].elapsed_time == 172.63
    assert games[3].timeline[104].event == "waiter stopped offering drink."
    assert games[3].timeline[104].mission == Missions.NoMission
    assert games[3].timeline[104].role == (Roles.Spy,)
    assert games[3].timeline[104].time == 52.3

    assert games[3].timeline[105].action_test == ActionTest.NoAT
    assert games[3].timeline[105].actor == "spy"
    assert games[3].timeline[105].books == (None,)
    assert games[3].timeline[105].cast_name == (None,)
    assert games[3].timeline[105].category == TimelineCategory.ActionTriggered
    assert games[3].timeline[105].elapsed_time == 175.13
    assert games[3].timeline[105].event == "action triggered: fingerprint ambassador"
    assert games[3].timeline[105].mission == Missions.Fingerprint
    assert games[3].timeline[105].role == (None,)
    assert games[3].timeline[105].time == 49.8

    assert games[3].timeline[106].action_test == ActionTest.NoAT
    assert games[3].timeline[106].actor == "spy"
    assert games[3].timeline[106].books == (None,)
    assert games[3].timeline[106].cast_name == (None,)
    assert games[3].timeline[106].category == TimelineCategory.Drinks
    assert games[3].timeline[106].elapsed_time == 175.13
    assert games[3].timeline[106].event == "started fingerprinting drink."
    assert games[3].timeline[106].mission == Missions.Fingerprint
    assert games[3].timeline[106].role == (None,)
    assert games[3].timeline[106].time == 49.8

    assert games[3].timeline[107].action_test == ActionTest.NoAT
    assert games[3].timeline[107].actor == "spy"
    assert games[3].timeline[107].books == (None,)
    assert games[3].timeline[107].cast_name == (None,)
    assert (
        games[3].timeline[107].category
        == TimelineCategory.MissionPartial | TimelineCategory.Drinks
    )
    assert games[3].timeline[107].elapsed_time == 176.13
    assert games[3].timeline[107].event == "fingerprinted drink."
    assert games[3].timeline[107].mission == Missions.Fingerprint
    assert games[3].timeline[107].role == (None,)
    assert games[3].timeline[107].time == 48.8

    assert games[3].timeline[108].action_test == ActionTest.NoAT
    assert games[3].timeline[108].actor == "spy"
    assert games[3].timeline[108].books == (None,)
    assert games[3].timeline[108].cast_name == (None,)
    assert games[3].timeline[108].category == TimelineCategory.MissionComplete
    assert games[3].timeline[108].elapsed_time == 176.13
    assert games[3].timeline[108].event == "fingerprinted ambassador."
    assert games[3].timeline[108].mission == Missions.Fingerprint
    assert games[3].timeline[108].role == (None,)
    assert games[3].timeline[108].time == 48.8

    assert games[3].timeline[109].action_test == ActionTest.NoAT
    assert games[3].timeline[109].actor == "spy"
    assert games[3].timeline[109].books == (None,)
    assert games[3].timeline[109].cast_name == (Characters.Plain,)
    assert games[3].timeline[109].category == TimelineCategory.Drinks
    assert games[3].timeline[109].elapsed_time == 185.0
    assert games[3].timeline[109].event == "sipped drink."
    assert games[3].timeline[109].mission == Missions.NoMission
    assert games[3].timeline[109].role == (Roles.Spy,)
    assert games[3].timeline[109].time == 40.0

    assert games[3].timeline[110].action_test == ActionTest.NoAT
    assert games[3].timeline[110].actor == "spy"
    assert games[3].timeline[110].books == (None,)
    assert games[3].timeline[110].cast_name == (None,)
    assert games[3].timeline[110].category == TimelineCategory.NoCategory
    assert games[3].timeline[110].elapsed_time == 187.69
    assert games[3].timeline[110].event == "flirtation cooldown expired."
    assert games[3].timeline[110].mission == Missions.Seduce
    assert games[3].timeline[110].role == (None,)
    assert games[3].timeline[110].time == 37.3

    assert games[3].timeline[111].action_test == ActionTest.NoAT
    assert games[3].timeline[111].actor == "spy"
    assert games[3].timeline[111].books == (None,)
    assert games[3].timeline[111].cast_name == (None,)
    assert games[3].timeline[111].category == TimelineCategory.ActionTriggered
    assert games[3].timeline[111].elapsed_time == 189.25
    assert games[3].timeline[111].event == "action triggered: seduce target"
    assert games[3].timeline[111].mission == Missions.Seduce
    assert games[3].timeline[111].role == (None,)
    assert games[3].timeline[111].time == 35.7

    assert games[3].timeline[112].action_test == ActionTest.NoAT
    assert games[3].timeline[112].actor == "spy"
    assert games[3].timeline[112].books == (None,)
    assert games[3].timeline[112].cast_name == (Characters.Smallman,)
    assert games[3].timeline[112].category == TimelineCategory.NoCategory
    assert games[3].timeline[112].elapsed_time == 189.25
    assert games[3].timeline[112].event == "begin flirtation with seduction target."
    assert games[3].timeline[112].mission == Missions.Seduce
    assert games[3].timeline[112].role == (Roles.SeductionTarget,)
    assert games[3].timeline[112].time == 35.7

    assert games[3].timeline[113].action_test == ActionTest.Ignored
    assert games[3].timeline[113].actor == "spy"
    assert games[3].timeline[113].books == (None,)
    assert games[3].timeline[113].cast_name == (None,)
    assert games[3].timeline[113].category == TimelineCategory.ActionTest
    assert games[3].timeline[113].elapsed_time == 190.63
    assert games[3].timeline[113].event == "action test ignored: seduce target"
    assert games[3].timeline[113].mission == Missions.Seduce
    assert games[3].timeline[113].role == (None,)
    assert games[3].timeline[113].time == 34.3

    assert games[3].timeline[114].action_test == ActionTest.NoAT
    assert games[3].timeline[114].actor == "spy"
    assert games[3].timeline[114].books == (None,)
    assert games[3].timeline[114].cast_name == (Characters.Smallman,)
    assert games[3].timeline[114].category == TimelineCategory.MissionPartial
    assert games[3].timeline[114].elapsed_time == 190.63
    assert games[3].timeline[114].event == "flirt with seduction target: 100%"
    assert games[3].timeline[114].mission == Missions.Seduce
    assert games[3].timeline[114].role == (Roles.SeductionTarget,)
    assert games[3].timeline[114].time == 34.3

    assert games[3].timeline[115].action_test == ActionTest.NoAT
    assert games[3].timeline[115].actor == "spy"
    assert games[3].timeline[115].books == (None,)
    assert games[3].timeline[115].cast_name == (Characters.Smallman,)
    assert games[3].timeline[115].category == TimelineCategory.MissionComplete
    assert games[3].timeline[115].elapsed_time == 190.63
    assert games[3].timeline[115].event == "target seduced."
    assert games[3].timeline[115].mission == Missions.Seduce
    assert games[3].timeline[115].role == (Roles.SeductionTarget,)
    assert games[3].timeline[115].time == 34.3

    assert games[3].timeline[116].action_test == ActionTest.NoAT
    assert games[3].timeline[116].actor == "spy"
    assert games[3].timeline[116].books == (None,)
    assert games[3].timeline[116].cast_name == (None,)
    assert games[3].timeline[116].category == TimelineCategory.Conversation
    assert games[3].timeline[116].elapsed_time == 203.06
    assert games[3].timeline[116].event == "spy leaves conversation."
    assert games[3].timeline[116].mission == Missions.NoMission
    assert games[3].timeline[116].role == (None,)
    assert games[3].timeline[116].time == 21.9

    assert games[3].timeline[117].action_test == ActionTest.NoAT
    assert games[3].timeline[117].actor == "spy"
    assert games[3].timeline[117].books == (None,)
    assert games[3].timeline[117].cast_name == (Characters.Disney,)
    assert games[3].timeline[117].category == TimelineCategory.Conversation
    assert games[3].timeline[117].elapsed_time == 203.06
    assert games[3].timeline[117].event == "spy left conversation with double agent."
    assert games[3].timeline[117].mission == Missions.NoMission
    assert games[3].timeline[117].role == (Roles.DoubleAgent,)
    assert games[3].timeline[117].time == 21.9

    assert games[3].timeline[118].action_test == ActionTest.NoAT
    assert games[3].timeline[118].actor == "spy"
    assert games[3].timeline[118].books == (None,)
    assert games[3].timeline[118].cast_name == (Characters.Plain,)
    assert games[3].timeline[118].category == TimelineCategory.Drinks
    assert games[3].timeline[118].elapsed_time == 209.19
    assert games[3].timeline[118].event == "gulped drink."
    assert games[3].timeline[118].mission == Missions.NoMission
    assert games[3].timeline[118].role == (Roles.Spy,)
    assert games[3].timeline[118].time == 15.8

    assert games[3].timeline[119].action_test == ActionTest.NoAT
    assert games[3].timeline[119].actor == "spy"
    assert games[3].timeline[119].books == (None,)
    assert games[3].timeline[119].cast_name == (None,)
    assert games[3].timeline[119].category == TimelineCategory.Statues
    assert games[3].timeline[119].elapsed_time == 212.13
    assert games[3].timeline[119].event == "picked up statue."
    assert games[3].timeline[119].mission == Missions.NoMission
    assert games[3].timeline[119].role == (None,)
    assert games[3].timeline[119].time == 12.8

    assert games[3].timeline[120].action_test == ActionTest.NoAT
    assert games[3].timeline[120].actor == "spy"
    assert games[3].timeline[120].books == (None,)
    assert games[3].timeline[120].cast_name == (None,)
    assert (
        games[3].timeline[120].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[3].timeline[120].elapsed_time == 215.69
    assert games[3].timeline[120].event == "action triggered: inspect statues"
    assert games[3].timeline[120].mission == Missions.Inspect
    assert games[3].timeline[120].role == (None,)
    assert games[3].timeline[120].time == 9.3

    assert games[3].timeline[121].action_test == ActionTest.White
    assert games[3].timeline[121].actor == "spy"
    assert games[3].timeline[121].books == (None,)
    assert games[3].timeline[121].cast_name == (None,)
    assert (
        games[3].timeline[121].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[3].timeline[121].elapsed_time == 216.56
    assert games[3].timeline[121].event == "action test white: inspect statues"
    assert games[3].timeline[121].mission == Missions.Inspect
    assert games[3].timeline[121].role == (None,)
    assert games[3].timeline[121].time == 8.4

    assert games[3].timeline[122].action_test == ActionTest.NoAT
    assert games[3].timeline[122].actor == "spy"
    assert games[3].timeline[122].books == (None,)
    assert games[3].timeline[122].cast_name == (None,)
    assert (
        games[3].timeline[122].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[3].timeline[122].elapsed_time == 220.69
    assert games[3].timeline[122].event == "left statue inspected."
    assert games[3].timeline[122].mission == Missions.Inspect
    assert games[3].timeline[122].role == (None,)
    assert games[3].timeline[122].time == 4.3

    assert games[3].timeline[123].action_test == ActionTest.NoAT
    assert games[3].timeline[123].actor == "spy"
    assert games[3].timeline[123].books == (None,)
    assert games[3].timeline[123].cast_name == (None,)
    assert (
        games[3].timeline[123].category
        == TimelineCategory.MissionComplete | TimelineCategory.Statues
    )
    assert games[3].timeline[123].elapsed_time == 220.69
    assert games[3].timeline[123].event == "all statues inspected."
    assert games[3].timeline[123].mission == Missions.Inspect
    assert games[3].timeline[123].role == (None,)
    assert games[3].timeline[123].time == 4.3

    assert games[3].timeline[124].action_test == ActionTest.NoAT
    assert games[3].timeline[124].actor == "game"
    assert games[3].timeline[124].books == (None,)
    assert games[3].timeline[124].cast_name == (None,)
    assert games[3].timeline[124].category == TimelineCategory.MissionCountdown
    assert games[3].timeline[124].elapsed_time == 220.69
    assert games[3].timeline[124].event == "missions completed. 10 second countdown."
    assert games[3].timeline[124].mission == Missions.NoMission
    assert games[3].timeline[124].role == (None,)
    assert games[3].timeline[124].time == 4.3

    assert games[3].timeline[125].action_test == ActionTest.NoAT
    assert games[3].timeline[125].actor == "game"
    assert games[3].timeline[125].books == (None,)
    assert games[3].timeline[125].cast_name == (None,)
    assert games[3].timeline[125].category == TimelineCategory.Overtime
    assert games[3].timeline[125].elapsed_time == 224.56
    assert games[3].timeline[125].event == "overtime!"
    assert games[3].timeline[125].mission == Missions.NoMission
    assert games[3].timeline[125].role == (None,)
    assert games[3].timeline[125].time == 0.4

    assert games[3].timeline[126].action_test == ActionTest.NoAT
    assert games[3].timeline[126].actor == "spy"
    assert games[3].timeline[126].books == (None,)
    assert games[3].timeline[126].cast_name == (None,)
    assert games[3].timeline[126].category == TimelineCategory.Statues
    assert games[3].timeline[126].elapsed_time == 224.94
    assert games[3].timeline[126].event == "put back statue."
    assert games[3].timeline[126].mission == Missions.NoMission
    assert games[3].timeline[126].role == (None,)
    assert games[3].timeline[126].time == 0.0

    assert games[3].timeline[127].action_test == ActionTest.NoAT
    assert games[3].timeline[127].actor == "sniper"
    assert games[3].timeline[127].books == (None,)
    assert games[3].timeline[127].cast_name == (Characters.Rocker,)
    assert games[3].timeline[127].category == TimelineCategory.SniperShot
    assert games[3].timeline[127].elapsed_time == 225.06
    assert games[3].timeline[127].event == "took shot."
    assert games[3].timeline[127].mission == Missions.NoMission
    assert games[3].timeline[127].role == (Roles.Civilian,)
    assert games[3].timeline[127].time == 0.0

    assert games[3].timeline[128].action_test == ActionTest.NoAT
    assert games[3].timeline[128].actor == "game"
    assert games[3].timeline[128].books == (None,)
    assert games[3].timeline[128].cast_name == (Characters.Rocker,)
    assert games[3].timeline[128].category == TimelineCategory.GameEnd
    assert games[3].timeline[128].elapsed_time == 228.31
    assert games[3].timeline[128].event == "sniper shot civilian."
    assert games[3].timeline[128].mission == Missions.NoMission
    assert games[3].timeline[128].role == (Roles.Civilian,)
    assert games[3].timeline[128].time == -3.3

    assert games[3].timeline.get_next_spy_action(games[3].timeline[128]) is None

    assert games[4].uuid == "jhx6e7UpTmeKueggeGcAKg"
    assert games[4].timeline[0].action_test == ActionTest.NoAT
    assert games[4].timeline[0].actor == "spy"
    assert games[4].timeline[0].books == (None,)
    assert games[4].timeline[0].cast_name == (Characters.General,)
    assert games[4].timeline[0].category == TimelineCategory.Cast
    assert games[4].timeline[0].elapsed_time == 0.0
    assert games[4].timeline[0].event == "spy cast."
    assert games[4].timeline[0].mission == Missions.NoMission
    assert games[4].timeline[0].role == (Roles.Spy,)
    assert games[4].timeline[0].time == 120.0

    assert games[4].timeline[1].action_test == ActionTest.NoAT
    assert games[4].timeline[1].actor == "spy"
    assert games[4].timeline[1].books == (None,)
    assert games[4].timeline[1].cast_name == (Characters.Taft,)
    assert games[4].timeline[1].category == TimelineCategory.Cast
    assert games[4].timeline[1].elapsed_time == 0.0
    assert games[4].timeline[1].event == "ambassador cast."
    assert games[4].timeline[1].mission == Missions.NoMission
    assert games[4].timeline[1].role == (Roles.Ambassador,)
    assert games[4].timeline[1].time == 120.0

    assert games[4].timeline[2].action_test == ActionTest.NoAT
    assert games[4].timeline[2].actor == "spy"
    assert games[4].timeline[2].books == (None,)
    assert games[4].timeline[2].cast_name == (Characters.Sari,)
    assert games[4].timeline[2].category == TimelineCategory.Cast
    assert games[4].timeline[2].elapsed_time == 0.0
    assert games[4].timeline[2].event == "double agent cast."
    assert games[4].timeline[2].mission == Missions.NoMission
    assert games[4].timeline[2].role == (Roles.DoubleAgent,)
    assert games[4].timeline[2].time == 120.0

    assert games[4].timeline[3].action_test == ActionTest.NoAT
    assert games[4].timeline[3].actor == "spy"
    assert games[4].timeline[3].books == (None,)
    assert games[4].timeline[3].cast_name == (Characters.Smallman,)
    assert games[4].timeline[3].category == TimelineCategory.Cast
    assert games[4].timeline[3].elapsed_time == 0.0
    assert games[4].timeline[3].event == "seduction target cast."
    assert games[4].timeline[3].mission == Missions.NoMission
    assert games[4].timeline[3].role == (Roles.SeductionTarget,)
    assert games[4].timeline[3].time == 120.0

    assert games[4].timeline[4].action_test == ActionTest.NoAT
    assert games[4].timeline[4].actor == "spy"
    assert games[4].timeline[4].books == (None,)
    assert games[4].timeline[4].cast_name == (Characters.Queen,)
    assert games[4].timeline[4].category == TimelineCategory.Cast
    assert games[4].timeline[4].elapsed_time == 0.0
    assert games[4].timeline[4].event == "civilian cast."
    assert games[4].timeline[4].mission == Missions.NoMission
    assert games[4].timeline[4].role == (Roles.Civilian,)
    assert games[4].timeline[4].time == 120.0

    assert games[4].timeline[5].action_test == ActionTest.NoAT
    assert games[4].timeline[5].actor == "spy"
    assert games[4].timeline[5].books == (None,)
    assert games[4].timeline[5].cast_name == (Characters.Morgan,)
    assert games[4].timeline[5].category == TimelineCategory.Cast
    assert games[4].timeline[5].elapsed_time == 0.0
    assert games[4].timeline[5].event == "civilian cast."
    assert games[4].timeline[5].mission == Missions.NoMission
    assert games[4].timeline[5].role == (Roles.Civilian,)
    assert games[4].timeline[5].time == 120.0

    assert games[4].timeline[6].action_test == ActionTest.NoAT
    assert games[4].timeline[6].actor == "spy"
    assert games[4].timeline[6].books == (None,)
    assert games[4].timeline[6].cast_name == (Characters.Irish,)
    assert games[4].timeline[6].category == TimelineCategory.Cast
    assert games[4].timeline[6].elapsed_time == 0.0
    assert games[4].timeline[6].event == "civilian cast."
    assert games[4].timeline[6].mission == Missions.NoMission
    assert games[4].timeline[6].role == (Roles.Civilian,)
    assert games[4].timeline[6].time == 120.0

    assert games[4].timeline[7].action_test == ActionTest.NoAT
    assert games[4].timeline[7].actor == "spy"
    assert games[4].timeline[7].books == (None,)
    assert games[4].timeline[7].cast_name == (None,)
    assert games[4].timeline[7].category == TimelineCategory.MissionSelected
    assert games[4].timeline[7].elapsed_time == 0.0
    assert games[4].timeline[7].event == "bug ambassador selected."
    assert games[4].timeline[7].mission == Missions.Bug
    assert games[4].timeline[7].role == (None,)
    assert games[4].timeline[7].time == 120.0

    assert games[4].timeline[8].action_test == ActionTest.NoAT
    assert games[4].timeline[8].actor == "spy"
    assert games[4].timeline[8].books == (None,)
    assert games[4].timeline[8].cast_name == (None,)
    assert games[4].timeline[8].category == TimelineCategory.MissionSelected
    assert games[4].timeline[8].elapsed_time == 0.0
    assert games[4].timeline[8].event == "contact double agent selected."
    assert games[4].timeline[8].mission == Missions.Contact
    assert games[4].timeline[8].role == (None,)
    assert games[4].timeline[8].time == 120.0

    assert games[4].timeline[9].action_test == ActionTest.NoAT
    assert games[4].timeline[9].actor == "spy"
    assert games[4].timeline[9].books == (None,)
    assert games[4].timeline[9].cast_name == (None,)
    assert games[4].timeline[9].category == TimelineCategory.MissionSelected
    assert games[4].timeline[9].elapsed_time == 0.0
    assert games[4].timeline[9].event == "seduce target selected."
    assert games[4].timeline[9].mission == Missions.Seduce
    assert games[4].timeline[9].role == (None,)
    assert games[4].timeline[9].time == 120.0

    assert games[4].timeline[10].action_test == ActionTest.NoAT
    assert games[4].timeline[10].actor == "spy"
    assert games[4].timeline[10].books == (None,)
    assert games[4].timeline[10].cast_name == (None,)
    assert games[4].timeline[10].category == TimelineCategory.MissionEnabled
    assert games[4].timeline[10].elapsed_time == 0.0
    assert games[4].timeline[10].event == "bug ambassador enabled."
    assert games[4].timeline[10].mission == Missions.Bug
    assert games[4].timeline[10].role == (None,)
    assert games[4].timeline[10].time == 120.0

    assert games[4].timeline[11].action_test == ActionTest.NoAT
    assert games[4].timeline[11].actor == "spy"
    assert games[4].timeline[11].books == (None,)
    assert games[4].timeline[11].cast_name == (None,)
    assert games[4].timeline[11].category == TimelineCategory.MissionEnabled
    assert games[4].timeline[11].elapsed_time == 0.0
    assert games[4].timeline[11].event == "contact double agent enabled."
    assert games[4].timeline[11].mission == Missions.Contact
    assert games[4].timeline[11].role == (None,)
    assert games[4].timeline[11].time == 120.0

    assert games[4].timeline[12].action_test == ActionTest.NoAT
    assert games[4].timeline[12].actor == "spy"
    assert games[4].timeline[12].books == (None,)
    assert games[4].timeline[12].cast_name == (None,)
    assert games[4].timeline[12].category == TimelineCategory.MissionEnabled
    assert games[4].timeline[12].elapsed_time == 0.0
    assert games[4].timeline[12].event == "seduce target enabled."
    assert games[4].timeline[12].mission == Missions.Seduce
    assert games[4].timeline[12].role == (None,)
    assert games[4].timeline[12].time == 120.0

    assert games[4].timeline[13].action_test == ActionTest.NoAT
    assert games[4].timeline[13].actor == "game"
    assert games[4].timeline[13].books == (None,)
    assert games[4].timeline[13].cast_name == (None,)
    assert games[4].timeline[13].category == TimelineCategory.GameStart
    assert games[4].timeline[13].elapsed_time == 0.0
    assert games[4].timeline[13].event == "game started."
    assert games[4].timeline[13].mission == Missions.NoMission
    assert games[4].timeline[13].role == (None,)
    assert games[4].timeline[13].time == 120.0

    assert games[4].timeline[14].action_test == ActionTest.NoAT
    assert games[4].timeline[14].actor == "sniper"
    assert games[4].timeline[14].books == (None,)
    assert games[4].timeline[14].cast_name == (Characters.Taft,)
    assert games[4].timeline[14].category == TimelineCategory.SniperLights
    assert games[4].timeline[14].elapsed_time == 0.25
    assert games[4].timeline[14].event == "marked less suspicious."
    assert games[4].timeline[14].mission == Missions.NoMission
    assert games[4].timeline[14].role == (Roles.Ambassador,)
    assert games[4].timeline[14].time == 119.7

    assert games[4].timeline[15].action_test == ActionTest.NoAT
    assert games[4].timeline[15].actor == "sniper"
    assert games[4].timeline[15].books == (None,)
    assert games[4].timeline[15].cast_name == (Characters.General,)
    assert games[4].timeline[15].category == TimelineCategory.SniperLights
    assert games[4].timeline[15].elapsed_time == 6.13
    assert games[4].timeline[15].event == "marked spy suspicious."
    assert games[4].timeline[15].mission == Missions.NoMission
    assert games[4].timeline[15].role == (Roles.Spy,)
    assert games[4].timeline[15].time == 113.8

    assert games[4].timeline[16].action_test == ActionTest.NoAT
    assert games[4].timeline[16].actor == "spy"
    assert games[4].timeline[16].books == (None,)
    assert games[4].timeline[16].cast_name == (Characters.General,)
    assert games[4].timeline[16].category == TimelineCategory.Drinks
    assert games[4].timeline[16].elapsed_time == 13.63
    assert games[4].timeline[16].event == "waiter offered drink."
    assert games[4].timeline[16].mission == Missions.NoMission
    assert games[4].timeline[16].role == (Roles.Spy,)
    assert games[4].timeline[16].time == 106.3

    assert games[4].timeline[17].action_test == ActionTest.NoAT
    assert games[4].timeline[17].actor == "spy"
    assert games[4].timeline[17].books == (None,)
    assert games[4].timeline[17].cast_name == (None,)
    assert games[4].timeline[17].category == TimelineCategory.NoCategory
    assert games[4].timeline[17].elapsed_time == 15.94
    assert games[4].timeline[17].event == "spy player takes control from ai."
    assert games[4].timeline[17].mission == Missions.NoMission
    assert games[4].timeline[17].role == (None,)
    assert games[4].timeline[17].time == 104.0

    assert games[4].timeline[18].action_test == ActionTest.NoAT
    assert games[4].timeline[18].actor == "spy"
    assert games[4].timeline[18].books == (None,)
    assert games[4].timeline[18].cast_name == (Characters.General,)
    assert games[4].timeline[18].category == TimelineCategory.Drinks
    assert games[4].timeline[18].elapsed_time == 17.81
    assert games[4].timeline[18].event == "rejected drink from waiter."
    assert games[4].timeline[18].mission == Missions.NoMission
    assert games[4].timeline[18].role == (Roles.Spy,)
    assert games[4].timeline[18].time == 102.1

    assert games[4].timeline[19].action_test == ActionTest.NoAT
    assert games[4].timeline[19].actor == "spy"
    assert games[4].timeline[19].books == (None,)
    assert games[4].timeline[19].cast_name == (Characters.General,)
    assert games[4].timeline[19].category == TimelineCategory.Drinks
    assert games[4].timeline[19].elapsed_time == 17.81
    assert games[4].timeline[19].event == "waiter stopped offering drink."
    assert games[4].timeline[19].mission == Missions.NoMission
    assert games[4].timeline[19].role == (Roles.Spy,)
    assert games[4].timeline[19].time == 102.1

    assert games[4].timeline[20].action_test == ActionTest.NoAT
    assert games[4].timeline[20].actor == "sniper"
    assert games[4].timeline[20].books == (None,)
    assert games[4].timeline[20].cast_name == (Characters.Smallman,)
    assert games[4].timeline[20].category == TimelineCategory.SniperLights
    assert games[4].timeline[20].elapsed_time == 20.5
    assert games[4].timeline[20].event == "marked suspicious."
    assert games[4].timeline[20].mission == Missions.NoMission
    assert games[4].timeline[20].role == (Roles.SeductionTarget,)
    assert games[4].timeline[20].time == 99.5

    assert games[4].timeline[21].action_test == ActionTest.NoAT
    assert games[4].timeline[21].actor == "sniper"
    assert games[4].timeline[21].books == (None,)
    assert games[4].timeline[21].cast_name == (Characters.Morgan,)
    assert games[4].timeline[21].category == TimelineCategory.SniperLights
    assert games[4].timeline[21].elapsed_time == 23.06
    assert games[4].timeline[21].event == "marked suspicious."
    assert games[4].timeline[21].mission == Missions.NoMission
    assert games[4].timeline[21].role == (Roles.Civilian,)
    assert games[4].timeline[21].time == 96.9

    assert games[4].timeline[22].action_test == ActionTest.NoAT
    assert games[4].timeline[22].actor == "spy"
    assert games[4].timeline[22].books == (None,)
    assert games[4].timeline[22].cast_name == (None,)
    assert games[4].timeline[22].category == TimelineCategory.ActionTriggered
    assert games[4].timeline[22].elapsed_time == 27.06
    assert games[4].timeline[22].event == "action triggered: seduce target"
    assert games[4].timeline[22].mission == Missions.Seduce
    assert games[4].timeline[22].role == (None,)
    assert games[4].timeline[22].time == 92.9

    assert games[4].timeline[23].action_test == ActionTest.NoAT
    assert games[4].timeline[23].actor == "spy"
    assert games[4].timeline[23].books == (None,)
    assert games[4].timeline[23].cast_name == (Characters.Smallman,)
    assert games[4].timeline[23].category == TimelineCategory.NoCategory
    assert games[4].timeline[23].elapsed_time == 27.06
    assert games[4].timeline[23].event == "begin flirtation with seduction target."
    assert games[4].timeline[23].mission == Missions.Seduce
    assert games[4].timeline[23].role == (Roles.SeductionTarget,)
    assert games[4].timeline[23].time == 92.9

    assert games[4].timeline[24].action_test == ActionTest.White
    assert games[4].timeline[24].actor == "spy"
    assert games[4].timeline[24].books == (None,)
    assert games[4].timeline[24].cast_name == (None,)
    assert games[4].timeline[24].category == TimelineCategory.ActionTest
    assert games[4].timeline[24].elapsed_time == 27.81
    assert games[4].timeline[24].event == "action test white: seduce target"
    assert games[4].timeline[24].mission == Missions.Seduce
    assert games[4].timeline[24].role == (None,)
    assert games[4].timeline[24].time == 92.1

    assert games[4].timeline[25].action_test == ActionTest.NoAT
    assert games[4].timeline[25].actor == "spy"
    assert games[4].timeline[25].books == (None,)
    assert games[4].timeline[25].cast_name == (Characters.Smallman,)
    assert games[4].timeline[25].category == TimelineCategory.MissionPartial
    assert games[4].timeline[25].elapsed_time == 27.81
    assert games[4].timeline[25].event == "flirt with seduction target: 32%"
    assert games[4].timeline[25].mission == Missions.Seduce
    assert games[4].timeline[25].role == (Roles.SeductionTarget,)
    assert games[4].timeline[25].time == 92.1

    assert games[4].timeline[26].action_test == ActionTest.NoAT
    assert games[4].timeline[26].actor == "spy"
    assert games[4].timeline[26].books == (None,)
    assert games[4].timeline[26].cast_name == (Characters.Sari,)
    assert games[4].timeline[26].category == TimelineCategory.Conversation
    assert games[4].timeline[26].elapsed_time == 35.13
    assert games[4].timeline[26].event == "double agent joined conversation with spy."
    assert games[4].timeline[26].mission == Missions.NoMission
    assert games[4].timeline[26].role == (Roles.DoubleAgent,)
    assert games[4].timeline[26].time == 84.8

    assert games[4].timeline[27].action_test == ActionTest.NoAT
    assert games[4].timeline[27].actor == "spy"
    assert games[4].timeline[27].books == (None,)
    assert games[4].timeline[27].cast_name == (None,)
    assert games[4].timeline[27].category == TimelineCategory.Conversation
    assert games[4].timeline[27].elapsed_time == 45.75
    assert games[4].timeline[27].event == "spy leaves conversation."
    assert games[4].timeline[27].mission == Missions.NoMission
    assert games[4].timeline[27].role == (None,)
    assert games[4].timeline[27].time == 74.2

    assert games[4].timeline[28].action_test == ActionTest.NoAT
    assert games[4].timeline[28].actor == "spy"
    assert games[4].timeline[28].books == (None,)
    assert games[4].timeline[28].cast_name == (Characters.Sari,)
    assert games[4].timeline[28].category == TimelineCategory.Conversation
    assert games[4].timeline[28].elapsed_time == 45.75
    assert games[4].timeline[28].event == "spy left conversation with double agent."
    assert games[4].timeline[28].mission == Missions.NoMission
    assert games[4].timeline[28].role == (Roles.DoubleAgent,)
    assert games[4].timeline[28].time == 74.2

    assert games[4].timeline[29].action_test == ActionTest.NoAT
    assert games[4].timeline[29].actor == "sniper"
    assert games[4].timeline[29].books == (None,)
    assert games[4].timeline[29].cast_name == (Characters.Damon,)
    assert games[4].timeline[29].category == TimelineCategory.SniperLights
    assert games[4].timeline[29].elapsed_time == 47.44
    assert games[4].timeline[29].event == "marked less suspicious."
    assert games[4].timeline[29].mission == Missions.NoMission
    assert games[4].timeline[29].role == (Roles.Staff,)
    assert games[4].timeline[29].time == 72.5

    assert games[4].timeline[30].action_test == ActionTest.NoAT
    assert games[4].timeline[30].actor == "sniper"
    assert games[4].timeline[30].books == (None,)
    assert games[4].timeline[30].cast_name == (Characters.Damon,)
    assert games[4].timeline[30].category == TimelineCategory.SniperLights
    assert games[4].timeline[30].elapsed_time == 49.19
    assert games[4].timeline[30].event == "marked neutral suspicion."
    assert games[4].timeline[30].mission == Missions.NoMission
    assert games[4].timeline[30].role == (Roles.Staff,)
    assert games[4].timeline[30].time == 70.8

    assert games[4].timeline[31].action_test == ActionTest.NoAT
    assert games[4].timeline[31].actor == "sniper"
    assert games[4].timeline[31].books == (None,)
    assert games[4].timeline[31].cast_name == (Characters.Damon,)
    assert games[4].timeline[31].category == TimelineCategory.SniperLights
    assert games[4].timeline[31].elapsed_time == 49.31
    assert games[4].timeline[31].event == "marked suspicious."
    assert games[4].timeline[31].mission == Missions.NoMission
    assert games[4].timeline[31].role == (Roles.Staff,)
    assert games[4].timeline[31].time == 70.6

    assert games[4].timeline[32].action_test == ActionTest.NoAT
    assert games[4].timeline[32].actor == "spy"
    assert games[4].timeline[32].books == (None,)
    assert games[4].timeline[32].cast_name == (None,)
    assert (
        games[4].timeline[32].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Watch
    )
    assert games[4].timeline[32].elapsed_time == 56.38
    assert games[4].timeline[32].event == "action triggered: check watch"
    assert games[4].timeline[32].mission == Missions.NoMission
    assert games[4].timeline[32].role == (None,)
    assert games[4].timeline[32].time == 63.6

    assert games[4].timeline[33].action_test == ActionTest.NoAT
    assert games[4].timeline[33].actor == "spy"
    assert games[4].timeline[33].books == (None,)
    assert games[4].timeline[33].cast_name == (Characters.General,)
    assert games[4].timeline[33].category == TimelineCategory.Watch
    assert games[4].timeline[33].elapsed_time == 56.38
    assert games[4].timeline[33].event == "watch checked."
    assert games[4].timeline[33].mission == Missions.NoMission
    assert games[4].timeline[33].role == (Roles.Spy,)
    assert games[4].timeline[33].time == 63.6

    assert games[4].timeline[34].action_test == ActionTest.NoAT
    assert games[4].timeline[34].actor == "spy"
    assert games[4].timeline[34].books == (None,)
    assert games[4].timeline[34].cast_name == (None,)
    assert games[4].timeline[34].category == TimelineCategory.NoCategory
    assert games[4].timeline[34].elapsed_time == 56.94
    assert games[4].timeline[34].event == "flirtation cooldown expired."
    assert games[4].timeline[34].mission == Missions.Seduce
    assert games[4].timeline[34].role == (None,)
    assert games[4].timeline[34].time == 63.0

    assert games[4].timeline[35].action_test == ActionTest.NoAT
    assert games[4].timeline[35].actor == "spy"
    assert games[4].timeline[35].books == (None,)
    assert games[4].timeline[35].cast_name == (None,)
    assert games[4].timeline[35].category == TimelineCategory.ActionTriggered
    assert games[4].timeline[35].elapsed_time == 64.25
    assert games[4].timeline[35].event == "action triggered: seduce target"
    assert games[4].timeline[35].mission == Missions.Seduce
    assert games[4].timeline[35].role == (None,)
    assert games[4].timeline[35].time == 55.7

    assert games[4].timeline[36].action_test == ActionTest.NoAT
    assert games[4].timeline[36].actor == "spy"
    assert games[4].timeline[36].books == (None,)
    assert games[4].timeline[36].cast_name == (Characters.Smallman,)
    assert games[4].timeline[36].category == TimelineCategory.NoCategory
    assert games[4].timeline[36].elapsed_time == 64.25
    assert games[4].timeline[36].event == "begin flirtation with seduction target."
    assert games[4].timeline[36].mission == Missions.Seduce
    assert games[4].timeline[36].role == (Roles.SeductionTarget,)
    assert games[4].timeline[36].time == 55.7

    assert games[4].timeline[37].action_test == ActionTest.Green
    assert games[4].timeline[37].actor == "spy"
    assert games[4].timeline[37].books == (None,)
    assert games[4].timeline[37].cast_name == (None,)
    assert games[4].timeline[37].category == TimelineCategory.ActionTest
    assert games[4].timeline[37].elapsed_time == 65.56
    assert games[4].timeline[37].event == "action test green: seduce target"
    assert games[4].timeline[37].mission == Missions.Seduce
    assert games[4].timeline[37].role == (None,)
    assert games[4].timeline[37].time == 54.4

    assert games[4].timeline[38].action_test == ActionTest.NoAT
    assert games[4].timeline[38].actor == "spy"
    assert games[4].timeline[38].books == (None,)
    assert games[4].timeline[38].cast_name == (Characters.Smallman,)
    assert games[4].timeline[38].category == TimelineCategory.NoCategory
    assert games[4].timeline[38].elapsed_time == 66.25
    assert games[4].timeline[38].event == "seduction canceled."
    assert games[4].timeline[38].mission == Missions.Seduce
    assert games[4].timeline[38].role == (Roles.SeductionTarget,)
    assert games[4].timeline[38].time == 53.7

    assert games[4].timeline[39].action_test == ActionTest.NoAT
    assert games[4].timeline[39].actor == "spy"
    assert games[4].timeline[39].books == (None,)
    assert games[4].timeline[39].cast_name == (None,)
    assert games[4].timeline[39].category == TimelineCategory.Conversation
    assert games[4].timeline[39].elapsed_time == 73.13
    assert games[4].timeline[39].event == "spy enters conversation."
    assert games[4].timeline[39].mission == Missions.NoMission
    assert games[4].timeline[39].role == (None,)
    assert games[4].timeline[39].time == 46.8

    assert games[4].timeline[40].action_test == ActionTest.NoAT
    assert games[4].timeline[40].actor == "spy"
    assert games[4].timeline[40].books == (None,)
    assert games[4].timeline[40].cast_name == (Characters.Sari,)
    assert games[4].timeline[40].category == TimelineCategory.Conversation
    assert games[4].timeline[40].elapsed_time == 73.13
    assert games[4].timeline[40].event == "spy joined conversation with double agent."
    assert games[4].timeline[40].mission == Missions.NoMission
    assert games[4].timeline[40].role == (Roles.DoubleAgent,)
    assert games[4].timeline[40].time == 46.8

    assert games[4].timeline[41].action_test == ActionTest.NoAT
    assert games[4].timeline[41].actor == "spy"
    assert games[4].timeline[41].books == (None,)
    assert games[4].timeline[41].cast_name == (None,)
    assert games[4].timeline[41].category == TimelineCategory.ActionTriggered
    assert games[4].timeline[41].elapsed_time == 92.81
    assert games[4].timeline[41].event == "action triggered: contact double agent"
    assert games[4].timeline[41].mission == Missions.Contact
    assert games[4].timeline[41].role == (None,)
    assert games[4].timeline[41].time == 27.1

    assert games[4].timeline[42].action_test == ActionTest.NoAT
    assert games[4].timeline[42].actor == "spy"
    assert games[4].timeline[42].books == (None,)
    assert games[4].timeline[42].cast_name == (None,)
    assert games[4].timeline[42].category == TimelineCategory.BananaBread
    assert games[4].timeline[42].elapsed_time == 92.81
    assert games[4].timeline[42].event == "real banana bread started."
    assert games[4].timeline[42].mission == Missions.Contact
    assert games[4].timeline[42].role == (None,)
    assert games[4].timeline[42].time == 27.1

    assert games[4].timeline[43].action_test == ActionTest.White
    assert games[4].timeline[43].actor == "spy"
    assert games[4].timeline[43].books == (None,)
    assert games[4].timeline[43].cast_name == (None,)
    assert games[4].timeline[43].category == TimelineCategory.ActionTest
    assert games[4].timeline[43].elapsed_time == 93.5
    assert games[4].timeline[43].event == "action test white: contact double agent"
    assert games[4].timeline[43].mission == Missions.Contact
    assert games[4].timeline[43].role == (None,)
    assert games[4].timeline[43].time == 26.5

    assert games[4].timeline[44].action_test == ActionTest.NoAT
    assert games[4].timeline[44].actor == "spy"
    assert games[4].timeline[44].books == (None,)
    assert games[4].timeline[44].cast_name == (None,)
    assert games[4].timeline[44].category == TimelineCategory.BananaBread
    assert games[4].timeline[44].elapsed_time == 96.88
    assert games[4].timeline[44].event == "banana bread uttered."
    assert games[4].timeline[44].mission == Missions.Contact
    assert games[4].timeline[44].role == (None,)
    assert games[4].timeline[44].time == 23.1

    assert games[4].timeline[45].action_test == ActionTest.NoAT
    assert games[4].timeline[45].actor == "spy"
    assert games[4].timeline[45].books == (None,)
    assert games[4].timeline[45].cast_name == (Characters.Sari,)
    assert games[4].timeline[45].category == TimelineCategory.MissionComplete
    assert games[4].timeline[45].elapsed_time == 97.38
    assert games[4].timeline[45].event == "double agent contacted."
    assert games[4].timeline[45].mission == Missions.Contact
    assert games[4].timeline[45].role == (Roles.DoubleAgent,)
    assert games[4].timeline[45].time == 22.6

    assert games[4].timeline[46].action_test == ActionTest.NoAT
    assert games[4].timeline[46].actor == "sniper"
    assert games[4].timeline[46].books == (None,)
    assert games[4].timeline[46].cast_name == (Characters.Queen,)
    assert games[4].timeline[46].category == TimelineCategory.SniperLights
    assert games[4].timeline[46].elapsed_time == 98.38
    assert games[4].timeline[46].event == "marked less suspicious."
    assert games[4].timeline[46].mission == Missions.NoMission
    assert games[4].timeline[46].role == (Roles.Civilian,)
    assert games[4].timeline[46].time == 21.6

    assert games[4].timeline[47].action_test == ActionTest.NoAT
    assert games[4].timeline[47].actor == "sniper"
    assert games[4].timeline[47].books == (None,)
    assert games[4].timeline[47].cast_name == (Characters.General,)
    assert games[4].timeline[47].category == TimelineCategory.SniperShot
    assert games[4].timeline[47].elapsed_time == 105.31
    assert games[4].timeline[47].event == "took shot."
    assert games[4].timeline[47].mission == Missions.NoMission
    assert games[4].timeline[47].role == (Roles.Spy,)
    assert games[4].timeline[47].time == 14.6

    assert games[4].timeline[48].action_test == ActionTest.NoAT
    assert games[4].timeline[48].actor == "game"
    assert games[4].timeline[48].books == (None,)
    assert games[4].timeline[48].cast_name == (Characters.General,)
    assert games[4].timeline[48].category == TimelineCategory.GameEnd
    assert games[4].timeline[48].elapsed_time == 110.0
    assert games[4].timeline[48].event == "sniper shot spy."
    assert games[4].timeline[48].mission == Missions.NoMission
    assert games[4].timeline[48].role == (Roles.Spy,)
    assert games[4].timeline[48].time == 10.0

    assert games[4].timeline.get_next_spy_action(games[4].timeline[48]) is None

    assert games[5].uuid == "k415gCwtS3ml9_EzUPpWFw"
    assert games[5].timeline[0].action_test == ActionTest.NoAT
    assert games[5].timeline[0].actor == "spy"
    assert games[5].timeline[0].books == (None,)
    assert games[5].timeline[0].cast_name == (Characters.Irish,)
    assert games[5].timeline[0].category == TimelineCategory.Cast
    assert games[5].timeline[0].elapsed_time == 0.0
    assert games[5].timeline[0].event == "spy cast."
    assert games[5].timeline[0].mission == Missions.NoMission
    assert games[5].timeline[0].role == (Roles.Spy,)
    assert games[5].timeline[0].time == 120.0

    assert games[5].timeline[1].action_test == ActionTest.NoAT
    assert games[5].timeline[1].actor == "spy"
    assert games[5].timeline[1].books == (None,)
    assert games[5].timeline[1].cast_name == (Characters.Wheels,)
    assert games[5].timeline[1].category == TimelineCategory.Cast
    assert games[5].timeline[1].elapsed_time == 0.0
    assert games[5].timeline[1].event == "ambassador cast."
    assert games[5].timeline[1].mission == Missions.NoMission
    assert games[5].timeline[1].role == (Roles.Ambassador,)
    assert games[5].timeline[1].time == 120.0

    assert games[5].timeline[2].action_test == ActionTest.NoAT
    assert games[5].timeline[2].actor == "spy"
    assert games[5].timeline[2].books == (None,)
    assert games[5].timeline[2].cast_name == (Characters.Taft,)
    assert games[5].timeline[2].category == TimelineCategory.Cast
    assert games[5].timeline[2].elapsed_time == 0.0
    assert games[5].timeline[2].event == "double agent cast."
    assert games[5].timeline[2].mission == Missions.NoMission
    assert games[5].timeline[2].role == (Roles.DoubleAgent,)
    assert games[5].timeline[2].time == 120.0

    assert games[5].timeline[3].action_test == ActionTest.NoAT
    assert games[5].timeline[3].actor == "spy"
    assert games[5].timeline[3].books == (None,)
    assert games[5].timeline[3].cast_name == (Characters.Morgan,)
    assert games[5].timeline[3].category == TimelineCategory.Cast
    assert games[5].timeline[3].elapsed_time == 0.0
    assert games[5].timeline[3].event == "seduction target cast."
    assert games[5].timeline[3].mission == Missions.NoMission
    assert games[5].timeline[3].role == (Roles.SeductionTarget,)
    assert games[5].timeline[3].time == 120.0

    assert games[5].timeline[4].action_test == ActionTest.NoAT
    assert games[5].timeline[4].actor == "spy"
    assert games[5].timeline[4].books == (None,)
    assert games[5].timeline[4].cast_name == (Characters.Smallman,)
    assert games[5].timeline[4].category == TimelineCategory.Cast
    assert games[5].timeline[4].elapsed_time == 0.0
    assert games[5].timeline[4].event == "civilian cast."
    assert games[5].timeline[4].mission == Missions.NoMission
    assert games[5].timeline[4].role == (Roles.Civilian,)
    assert games[5].timeline[4].time == 120.0

    assert games[5].timeline[5].action_test == ActionTest.NoAT
    assert games[5].timeline[5].actor == "spy"
    assert games[5].timeline[5].books == (None,)
    assert games[5].timeline[5].cast_name == (Characters.Sari,)
    assert games[5].timeline[5].category == TimelineCategory.Cast
    assert games[5].timeline[5].elapsed_time == 0.0
    assert games[5].timeline[5].event == "civilian cast."
    assert games[5].timeline[5].mission == Missions.NoMission
    assert games[5].timeline[5].role == (Roles.Civilian,)
    assert games[5].timeline[5].time == 120.0

    assert games[5].timeline[6].action_test == ActionTest.NoAT
    assert games[5].timeline[6].actor == "spy"
    assert games[5].timeline[6].books == (None,)
    assert games[5].timeline[6].cast_name == (Characters.General,)
    assert games[5].timeline[6].category == TimelineCategory.Cast
    assert games[5].timeline[6].elapsed_time == 0.0
    assert games[5].timeline[6].event == "civilian cast."
    assert games[5].timeline[6].mission == Missions.NoMission
    assert games[5].timeline[6].role == (Roles.Civilian,)
    assert games[5].timeline[6].time == 120.0

    assert games[5].timeline[7].action_test == ActionTest.NoAT
    assert games[5].timeline[7].actor == "spy"
    assert games[5].timeline[7].books == (None,)
    assert games[5].timeline[7].cast_name == (None,)
    assert games[5].timeline[7].category == TimelineCategory.MissionSelected
    assert games[5].timeline[7].elapsed_time == 0.0
    assert games[5].timeline[7].event == "bug ambassador selected."
    assert games[5].timeline[7].mission == Missions.Bug
    assert games[5].timeline[7].role == (None,)
    assert games[5].timeline[7].time == 120.0

    assert games[5].timeline[8].action_test == ActionTest.NoAT
    assert games[5].timeline[8].actor == "spy"
    assert games[5].timeline[8].books == (None,)
    assert games[5].timeline[8].cast_name == (None,)
    assert games[5].timeline[8].category == TimelineCategory.MissionSelected
    assert games[5].timeline[8].elapsed_time == 0.0
    assert games[5].timeline[8].event == "contact double agent selected."
    assert games[5].timeline[8].mission == Missions.Contact
    assert games[5].timeline[8].role == (None,)
    assert games[5].timeline[8].time == 120.0

    assert games[5].timeline[9].action_test == ActionTest.NoAT
    assert games[5].timeline[9].actor == "spy"
    assert games[5].timeline[9].books == (None,)
    assert games[5].timeline[9].cast_name == (None,)
    assert games[5].timeline[9].category == TimelineCategory.MissionSelected
    assert games[5].timeline[9].elapsed_time == 0.0
    assert games[5].timeline[9].event == "seduce target selected."
    assert games[5].timeline[9].mission == Missions.Seduce
    assert games[5].timeline[9].role == (None,)
    assert games[5].timeline[9].time == 120.0

    assert games[5].timeline[10].action_test == ActionTest.NoAT
    assert games[5].timeline[10].actor == "spy"
    assert games[5].timeline[10].books == (None,)
    assert games[5].timeline[10].cast_name == (None,)
    assert games[5].timeline[10].category == TimelineCategory.MissionEnabled
    assert games[5].timeline[10].elapsed_time == 0.0
    assert games[5].timeline[10].event == "bug ambassador enabled."
    assert games[5].timeline[10].mission == Missions.Bug
    assert games[5].timeline[10].role == (None,)
    assert games[5].timeline[10].time == 120.0

    assert games[5].timeline[11].action_test == ActionTest.NoAT
    assert games[5].timeline[11].actor == "spy"
    assert games[5].timeline[11].books == (None,)
    assert games[5].timeline[11].cast_name == (None,)
    assert games[5].timeline[11].category == TimelineCategory.MissionEnabled
    assert games[5].timeline[11].elapsed_time == 0.0
    assert games[5].timeline[11].event == "contact double agent enabled."
    assert games[5].timeline[11].mission == Missions.Contact
    assert games[5].timeline[11].role == (None,)
    assert games[5].timeline[11].time == 120.0

    assert games[5].timeline[12].action_test == ActionTest.NoAT
    assert games[5].timeline[12].actor == "spy"
    assert games[5].timeline[12].books == (None,)
    assert games[5].timeline[12].cast_name == (None,)
    assert games[5].timeline[12].category == TimelineCategory.MissionEnabled
    assert games[5].timeline[12].elapsed_time == 0.0
    assert games[5].timeline[12].event == "seduce target enabled."
    assert games[5].timeline[12].mission == Missions.Seduce
    assert games[5].timeline[12].role == (None,)
    assert games[5].timeline[12].time == 120.0

    assert games[5].timeline[13].action_test == ActionTest.NoAT
    assert games[5].timeline[13].actor == "game"
    assert games[5].timeline[13].books == (None,)
    assert games[5].timeline[13].cast_name == (None,)
    assert games[5].timeline[13].category == TimelineCategory.GameStart
    assert games[5].timeline[13].elapsed_time == 0.0
    assert games[5].timeline[13].event == "game started."
    assert games[5].timeline[13].mission == Missions.NoMission
    assert games[5].timeline[13].role == (None,)
    assert games[5].timeline[13].time == 120.0

    assert games[5].timeline[14].action_test == ActionTest.NoAT
    assert games[5].timeline[14].actor == "sniper"
    assert games[5].timeline[14].books == (None,)
    assert games[5].timeline[14].cast_name == (Characters.Damon,)
    assert games[5].timeline[14].category == TimelineCategory.SniperLights
    assert games[5].timeline[14].elapsed_time == 2.75
    assert games[5].timeline[14].event == "marked less suspicious."
    assert games[5].timeline[14].mission == Missions.NoMission
    assert games[5].timeline[14].role == (Roles.Staff,)
    assert games[5].timeline[14].time == 117.2

    assert games[5].timeline[15].action_test == ActionTest.NoAT
    assert games[5].timeline[15].actor == "spy"
    assert games[5].timeline[15].books == (None,)
    assert games[5].timeline[15].cast_name == (None,)
    assert games[5].timeline[15].category == TimelineCategory.NoCategory
    assert games[5].timeline[15].elapsed_time == 2.94
    assert games[5].timeline[15].event == "spy player takes control from ai."
    assert games[5].timeline[15].mission == Missions.NoMission
    assert games[5].timeline[15].role == (None,)
    assert games[5].timeline[15].time == 117.0

    assert games[5].timeline[16].action_test == ActionTest.NoAT
    assert games[5].timeline[16].actor == "sniper"
    assert games[5].timeline[16].books == (None,)
    assert games[5].timeline[16].cast_name == (Characters.Toby,)
    assert games[5].timeline[16].category == TimelineCategory.SniperLights
    assert games[5].timeline[16].elapsed_time == 4.25
    assert games[5].timeline[16].event == "marked less suspicious."
    assert games[5].timeline[16].mission == Missions.NoMission
    assert games[5].timeline[16].role == (Roles.Staff,)
    assert games[5].timeline[16].time == 115.7

    assert games[5].timeline[17].action_test == ActionTest.NoAT
    assert games[5].timeline[17].actor == "sniper"
    assert games[5].timeline[17].books == (None,)
    assert games[5].timeline[17].cast_name == (Characters.Smallman,)
    assert games[5].timeline[17].category == TimelineCategory.SniperLights
    assert games[5].timeline[17].elapsed_time == 5.88
    assert games[5].timeline[17].event == "marked suspicious."
    assert games[5].timeline[17].mission == Missions.NoMission
    assert games[5].timeline[17].role == (Roles.Civilian,)
    assert games[5].timeline[17].time == 114.1

    assert games[5].timeline[18].action_test == ActionTest.NoAT
    assert games[5].timeline[18].actor == "spy"
    assert games[5].timeline[18].books == (None,)
    assert games[5].timeline[18].cast_name == (None,)
    assert games[5].timeline[18].category == TimelineCategory.Conversation
    assert games[5].timeline[18].elapsed_time == 15.19
    assert games[5].timeline[18].event == "spy enters conversation."
    assert games[5].timeline[18].mission == Missions.NoMission
    assert games[5].timeline[18].role == (None,)
    assert games[5].timeline[18].time == 104.8

    assert games[5].timeline[19].action_test == ActionTest.NoAT
    assert games[5].timeline[19].actor == "spy"
    assert games[5].timeline[19].books == (None,)
    assert games[5].timeline[19].cast_name == (Characters.Taft,)
    assert games[5].timeline[19].category == TimelineCategory.Conversation
    assert games[5].timeline[19].elapsed_time == 15.19
    assert games[5].timeline[19].event == "spy joined conversation with double agent."
    assert games[5].timeline[19].mission == Missions.NoMission
    assert games[5].timeline[19].role == (Roles.DoubleAgent,)
    assert games[5].timeline[19].time == 104.8

    assert games[5].timeline[20].action_test == ActionTest.NoAT
    assert games[5].timeline[20].actor == "sniper"
    assert games[5].timeline[20].books == (None,)
    assert games[5].timeline[20].cast_name == (Characters.Morgan,)
    assert games[5].timeline[20].category == TimelineCategory.SniperLights
    assert games[5].timeline[20].elapsed_time == 21.81
    assert games[5].timeline[20].event == "marked suspicious."
    assert games[5].timeline[20].mission == Missions.NoMission
    assert games[5].timeline[20].role == (Roles.SeductionTarget,)
    assert games[5].timeline[20].time == 98.1

    assert games[5].timeline[21].action_test == ActionTest.NoAT
    assert games[5].timeline[21].actor == "spy"
    assert games[5].timeline[21].books == (None,)
    assert games[5].timeline[21].cast_name == (None,)
    assert games[5].timeline[21].category == TimelineCategory.ActionTriggered
    assert games[5].timeline[21].elapsed_time == 22.63
    assert games[5].timeline[21].event == "action triggered: contact double agent"
    assert games[5].timeline[21].mission == Missions.Contact
    assert games[5].timeline[21].role == (None,)
    assert games[5].timeline[21].time == 97.3

    assert games[5].timeline[22].action_test == ActionTest.NoAT
    assert games[5].timeline[22].actor == "spy"
    assert games[5].timeline[22].books == (None,)
    assert games[5].timeline[22].cast_name == (None,)
    assert games[5].timeline[22].category == TimelineCategory.BananaBread
    assert games[5].timeline[22].elapsed_time == 22.63
    assert games[5].timeline[22].event == "real banana bread started."
    assert games[5].timeline[22].mission == Missions.Contact
    assert games[5].timeline[22].role == (None,)
    assert games[5].timeline[22].time == 97.3

    assert games[5].timeline[23].action_test == ActionTest.NoAT
    assert games[5].timeline[23].actor == "sniper"
    assert games[5].timeline[23].books == (None,)
    assert games[5].timeline[23].cast_name == (Characters.Taft,)
    assert games[5].timeline[23].category == TimelineCategory.SniperLights
    assert games[5].timeline[23].elapsed_time == 23.0
    assert games[5].timeline[23].event == "marked suspicious."
    assert games[5].timeline[23].mission == Missions.NoMission
    assert games[5].timeline[23].role == (Roles.DoubleAgent,)
    assert games[5].timeline[23].time == 97.0

    assert games[5].timeline[24].action_test == ActionTest.Green
    assert games[5].timeline[24].actor == "spy"
    assert games[5].timeline[24].books == (None,)
    assert games[5].timeline[24].cast_name == (None,)
    assert games[5].timeline[24].category == TimelineCategory.ActionTest
    assert games[5].timeline[24].elapsed_time == 23.75
    assert games[5].timeline[24].event == "action test green: contact double agent"
    assert games[5].timeline[24].mission == Missions.Contact
    assert games[5].timeline[24].role == (None,)
    assert games[5].timeline[24].time == 96.2

    assert games[5].timeline[25].action_test == ActionTest.NoAT
    assert games[5].timeline[25].actor == "spy"
    assert games[5].timeline[25].books == (None,)
    assert games[5].timeline[25].cast_name == (None,)
    assert games[5].timeline[25].category == TimelineCategory.BananaBread
    assert games[5].timeline[25].elapsed_time == 23.75
    assert games[5].timeline[25].event == "banana bread uttered."
    assert games[5].timeline[25].mission == Missions.Contact
    assert games[5].timeline[25].role == (None,)
    assert games[5].timeline[25].time == 96.2

    assert games[5].timeline[26].action_test == ActionTest.NoAT
    assert games[5].timeline[26].actor == "spy"
    assert games[5].timeline[26].books == (None,)
    assert games[5].timeline[26].cast_name == (Characters.Taft,)
    assert games[5].timeline[26].category == TimelineCategory.MissionComplete
    assert games[5].timeline[26].elapsed_time == 24.31
    assert games[5].timeline[26].event == "double agent contacted."
    assert games[5].timeline[26].mission == Missions.Contact
    assert games[5].timeline[26].role == (Roles.DoubleAgent,)
    assert games[5].timeline[26].time == 95.6

    assert games[5].timeline[27].action_test == ActionTest.NoAT
    assert games[5].timeline[27].actor == "spy"
    assert games[5].timeline[27].books == (None,)
    assert games[5].timeline[27].cast_name == (None,)
    assert games[5].timeline[27].category == TimelineCategory.ActionTriggered
    assert games[5].timeline[27].elapsed_time == 28.56
    assert games[5].timeline[27].event == "action triggered: seduce target"
    assert games[5].timeline[27].mission == Missions.Seduce
    assert games[5].timeline[27].role == (None,)
    assert games[5].timeline[27].time == 91.4

    assert games[5].timeline[28].action_test == ActionTest.NoAT
    assert games[5].timeline[28].actor == "spy"
    assert games[5].timeline[28].books == (None,)
    assert games[5].timeline[28].cast_name == (Characters.Morgan,)
    assert games[5].timeline[28].category == TimelineCategory.NoCategory
    assert games[5].timeline[28].elapsed_time == 28.56
    assert games[5].timeline[28].event == "begin flirtation with seduction target."
    assert games[5].timeline[28].mission == Missions.Seduce
    assert games[5].timeline[28].role == (Roles.SeductionTarget,)
    assert games[5].timeline[28].time == 91.4

    assert games[5].timeline[29].action_test == ActionTest.Green
    assert games[5].timeline[29].actor == "spy"
    assert games[5].timeline[29].books == (None,)
    assert games[5].timeline[29].cast_name == (None,)
    assert games[5].timeline[29].category == TimelineCategory.ActionTest
    assert games[5].timeline[29].elapsed_time == 29.63
    assert games[5].timeline[29].event == "action test green: seduce target"
    assert games[5].timeline[29].mission == Missions.Seduce
    assert games[5].timeline[29].role == (None,)
    assert games[5].timeline[29].time == 90.3

    assert games[5].timeline[30].action_test == ActionTest.NoAT
    assert games[5].timeline[30].actor == "spy"
    assert games[5].timeline[30].books == (None,)
    assert games[5].timeline[30].cast_name == (Characters.Morgan,)
    assert games[5].timeline[30].category == TimelineCategory.MissionPartial
    assert games[5].timeline[30].elapsed_time == 29.63
    assert games[5].timeline[30].event == "flirt with seduction target: 51%"
    assert games[5].timeline[30].mission == Missions.Seduce
    assert games[5].timeline[30].role == (Roles.SeductionTarget,)
    assert games[5].timeline[30].time == 90.3

    assert games[5].timeline[31].action_test == ActionTest.NoAT
    assert games[5].timeline[31].actor == "sniper"
    assert games[5].timeline[31].books == (None,)
    assert games[5].timeline[31].cast_name == (Characters.Sari,)
    assert games[5].timeline[31].category == TimelineCategory.SniperLights
    assert games[5].timeline[31].elapsed_time == 37.94
    assert games[5].timeline[31].event == "marked less suspicious."
    assert games[5].timeline[31].mission == Missions.NoMission
    assert games[5].timeline[31].role == (Roles.Civilian,)
    assert games[5].timeline[31].time == 82.0

    assert games[5].timeline[32].action_test == ActionTest.NoAT
    assert games[5].timeline[32].actor == "spy"
    assert games[5].timeline[32].books == (None,)
    assert games[5].timeline[32].cast_name == (Characters.Irish,)
    assert games[5].timeline[32].category == TimelineCategory.Drinks
    assert games[5].timeline[32].elapsed_time == 43.06
    assert games[5].timeline[32].event == "waiter offered drink."
    assert games[5].timeline[32].mission == Missions.NoMission
    assert games[5].timeline[32].role == (Roles.Spy,)
    assert games[5].timeline[32].time == 76.9

    assert games[5].timeline[33].action_test == ActionTest.NoAT
    assert games[5].timeline[33].actor == "spy"
    assert games[5].timeline[33].books == (None,)
    assert games[5].timeline[33].cast_name == (Characters.Irish,)
    assert games[5].timeline[33].category == TimelineCategory.Drinks
    assert games[5].timeline[33].elapsed_time == 48.63
    assert games[5].timeline[33].event == "got drink from waiter."
    assert games[5].timeline[33].mission == Missions.NoMission
    assert games[5].timeline[33].role == (Roles.Spy,)
    assert games[5].timeline[33].time == 71.3

    assert games[5].timeline[34].action_test == ActionTest.NoAT
    assert games[5].timeline[34].actor == "spy"
    assert games[5].timeline[34].books == (None,)
    assert games[5].timeline[34].cast_name == (Characters.Irish,)
    assert games[5].timeline[34].category == TimelineCategory.Drinks
    assert games[5].timeline[34].elapsed_time == 48.63
    assert games[5].timeline[34].event == "waiter stopped offering drink."
    assert games[5].timeline[34].mission == Missions.NoMission
    assert games[5].timeline[34].role == (Roles.Spy,)
    assert games[5].timeline[34].time == 71.3

    assert games[5].timeline[35].action_test == ActionTest.NoAT
    assert games[5].timeline[35].actor == "spy"
    assert games[5].timeline[35].books == (None,)
    assert games[5].timeline[35].cast_name == (None,)
    assert games[5].timeline[35].category == TimelineCategory.NoCategory
    assert games[5].timeline[35].elapsed_time == 57.56
    assert games[5].timeline[35].event == "flirtation cooldown expired."
    assert games[5].timeline[35].mission == Missions.Seduce
    assert games[5].timeline[35].role == (None,)
    assert games[5].timeline[35].time == 62.4

    assert games[5].timeline[36].action_test == ActionTest.NoAT
    assert games[5].timeline[36].actor == "spy"
    assert games[5].timeline[36].books == (None,)
    assert games[5].timeline[36].cast_name == (None,)
    assert games[5].timeline[36].category == TimelineCategory.ActionTriggered
    assert games[5].timeline[36].elapsed_time == 74.06
    assert games[5].timeline[36].event == "action triggered: seduce target"
    assert games[5].timeline[36].mission == Missions.Seduce
    assert games[5].timeline[36].role == (None,)
    assert games[5].timeline[36].time == 45.9

    assert games[5].timeline[37].action_test == ActionTest.NoAT
    assert games[5].timeline[37].actor == "spy"
    assert games[5].timeline[37].books == (None,)
    assert games[5].timeline[37].cast_name == (Characters.Morgan,)
    assert games[5].timeline[37].category == TimelineCategory.NoCategory
    assert games[5].timeline[37].elapsed_time == 74.06
    assert games[5].timeline[37].event == "begin flirtation with seduction target."
    assert games[5].timeline[37].mission == Missions.Seduce
    assert games[5].timeline[37].role == (Roles.SeductionTarget,)
    assert games[5].timeline[37].time == 45.9

    assert games[5].timeline[38].action_test == ActionTest.NoAT
    assert games[5].timeline[38].actor == "sniper"
    assert games[5].timeline[38].books == (None,)
    assert games[5].timeline[38].cast_name == (Characters.Irish,)
    assert games[5].timeline[38].category == TimelineCategory.SniperLights
    assert games[5].timeline[38].elapsed_time == 74.31
    assert games[5].timeline[38].event == "marked spy less suspicious."
    assert games[5].timeline[38].mission == Missions.NoMission
    assert games[5].timeline[38].role == (Roles.Spy,)
    assert games[5].timeline[38].time == 45.6

    assert games[5].timeline[39].action_test == ActionTest.White
    assert games[5].timeline[39].actor == "spy"
    assert games[5].timeline[39].books == (None,)
    assert games[5].timeline[39].cast_name == (None,)
    assert games[5].timeline[39].category == TimelineCategory.ActionTest
    assert games[5].timeline[39].elapsed_time == 75.0
    assert games[5].timeline[39].event == "action test white: seduce target"
    assert games[5].timeline[39].mission == Missions.Seduce
    assert games[5].timeline[39].role == (None,)
    assert games[5].timeline[39].time == 45.0

    assert games[5].timeline[40].action_test == ActionTest.NoAT
    assert games[5].timeline[40].actor == "spy"
    assert games[5].timeline[40].books == (None,)
    assert games[5].timeline[40].cast_name == (Characters.Morgan,)
    assert games[5].timeline[40].category == TimelineCategory.MissionPartial
    assert games[5].timeline[40].elapsed_time == 75.0
    assert games[5].timeline[40].event == "flirt with seduction target: 72%"
    assert games[5].timeline[40].mission == Missions.Seduce
    assert games[5].timeline[40].role == (Roles.SeductionTarget,)
    assert games[5].timeline[40].time == 45.0

    assert games[5].timeline[41].action_test == ActionTest.NoAT
    assert games[5].timeline[41].actor == "spy"
    assert games[5].timeline[41].books == (None,)
    assert games[5].timeline[41].cast_name == (Characters.Taft,)
    assert games[5].timeline[41].category == TimelineCategory.Conversation
    assert games[5].timeline[41].elapsed_time == 75.06
    assert games[5].timeline[41].event == "double agent left conversation with spy."
    assert games[5].timeline[41].mission == Missions.NoMission
    assert games[5].timeline[41].role == (Roles.DoubleAgent,)
    assert games[5].timeline[41].time == 44.9

    assert games[5].timeline[42].action_test == ActionTest.NoAT
    assert games[5].timeline[42].actor == "spy"
    assert games[5].timeline[42].books == (None,)
    assert games[5].timeline[42].cast_name == (None,)
    assert games[5].timeline[42].category == TimelineCategory.Conversation
    assert games[5].timeline[42].elapsed_time == 84.88
    assert games[5].timeline[42].event == "spy leaves conversation."
    assert games[5].timeline[42].mission == Missions.NoMission
    assert games[5].timeline[42].role == (None,)
    assert games[5].timeline[42].time == 35.1

    assert games[5].timeline[43].action_test == ActionTest.NoAT
    assert games[5].timeline[43].actor == "spy"
    assert games[5].timeline[43].books == (None,)
    assert games[5].timeline[43].cast_name == (Characters.Irish,)
    assert games[5].timeline[43].category == TimelineCategory.Drinks
    assert games[5].timeline[43].elapsed_time == 91.31
    assert games[5].timeline[43].event == "sipped drink."
    assert games[5].timeline[43].mission == Missions.NoMission
    assert games[5].timeline[43].role == (Roles.Spy,)
    assert games[5].timeline[43].time == 28.6

    assert games[5].timeline[44].action_test == ActionTest.NoAT
    assert games[5].timeline[44].actor == "spy"
    assert games[5].timeline[44].books == (None,)
    assert games[5].timeline[44].cast_name == (None,)
    assert games[5].timeline[44].category == TimelineCategory.NoCategory
    assert games[5].timeline[44].elapsed_time == 93.56
    assert games[5].timeline[44].event == "flirtation cooldown expired."
    assert games[5].timeline[44].mission == Missions.Seduce
    assert games[5].timeline[44].role == (None,)
    assert games[5].timeline[44].time == 26.4

    assert games[5].timeline[45].action_test == ActionTest.NoAT
    assert games[5].timeline[45].actor == "spy"
    assert games[5].timeline[45].books == (None,)
    assert games[5].timeline[45].cast_name == (None,)
    assert games[5].timeline[45].category == TimelineCategory.Conversation
    assert games[5].timeline[45].elapsed_time == 101.19
    assert games[5].timeline[45].event == "spy enters conversation."
    assert games[5].timeline[45].mission == Missions.NoMission
    assert games[5].timeline[45].role == (None,)
    assert games[5].timeline[45].time == 18.8

    assert games[5].timeline[46].action_test == ActionTest.NoAT
    assert games[5].timeline[46].actor == "spy"
    assert games[5].timeline[46].books == (None,)
    assert games[5].timeline[46].cast_name == (Characters.Taft,)
    assert games[5].timeline[46].category == TimelineCategory.Conversation
    assert games[5].timeline[46].elapsed_time == 101.19
    assert games[5].timeline[46].event == "spy joined conversation with double agent."
    assert games[5].timeline[46].mission == Missions.NoMission
    assert games[5].timeline[46].role == (Roles.DoubleAgent,)
    assert games[5].timeline[46].time == 18.8

    assert games[5].timeline[47].action_test == ActionTest.NoAT
    assert games[5].timeline[47].actor == "spy"
    assert games[5].timeline[47].books == (None,)
    assert games[5].timeline[47].cast_name == (None,)
    assert games[5].timeline[47].category == TimelineCategory.ActionTriggered
    assert games[5].timeline[47].elapsed_time == 107.63
    assert games[5].timeline[47].event == "action triggered: seduce target"
    assert games[5].timeline[47].mission == Missions.Seduce
    assert games[5].timeline[47].role == (None,)
    assert games[5].timeline[47].time == 12.3

    assert games[5].timeline[48].action_test == ActionTest.NoAT
    assert games[5].timeline[48].actor == "spy"
    assert games[5].timeline[48].books == (None,)
    assert games[5].timeline[48].cast_name == (Characters.Morgan,)
    assert games[5].timeline[48].category == TimelineCategory.NoCategory
    assert games[5].timeline[48].elapsed_time == 107.63
    assert games[5].timeline[48].event == "begin flirtation with seduction target."
    assert games[5].timeline[48].mission == Missions.Seduce
    assert games[5].timeline[48].role == (Roles.SeductionTarget,)
    assert games[5].timeline[48].time == 12.3

    assert games[5].timeline[49].action_test == ActionTest.White
    assert games[5].timeline[49].actor == "spy"
    assert games[5].timeline[49].books == (None,)
    assert games[5].timeline[49].cast_name == (None,)
    assert games[5].timeline[49].category == TimelineCategory.ActionTest
    assert games[5].timeline[49].elapsed_time == 108.88
    assert games[5].timeline[49].event == "action test white: seduce target"
    assert games[5].timeline[49].mission == Missions.Seduce
    assert games[5].timeline[49].role == (None,)
    assert games[5].timeline[49].time == 11.1

    assert games[5].timeline[50].action_test == ActionTest.NoAT
    assert games[5].timeline[50].actor == "spy"
    assert games[5].timeline[50].books == (None,)
    assert games[5].timeline[50].cast_name == (Characters.Morgan,)
    assert games[5].timeline[50].category == TimelineCategory.MissionPartial
    assert games[5].timeline[50].elapsed_time == 108.88
    assert games[5].timeline[50].event == "flirt with seduction target: 100%"
    assert games[5].timeline[50].mission == Missions.Seduce
    assert games[5].timeline[50].role == (Roles.SeductionTarget,)
    assert games[5].timeline[50].time == 11.1

    assert games[5].timeline[51].action_test == ActionTest.NoAT
    assert games[5].timeline[51].actor == "spy"
    assert games[5].timeline[51].books == (None,)
    assert games[5].timeline[51].cast_name == (Characters.Morgan,)
    assert games[5].timeline[51].category == TimelineCategory.MissionComplete
    assert games[5].timeline[51].elapsed_time == 108.88
    assert games[5].timeline[51].event == "target seduced."
    assert games[5].timeline[51].mission == Missions.Seduce
    assert games[5].timeline[51].role == (Roles.SeductionTarget,)
    assert games[5].timeline[51].time == 11.1

    assert games[5].timeline[52].action_test == ActionTest.NoAT
    assert games[5].timeline[52].actor == "game"
    assert games[5].timeline[52].books == (None,)
    assert games[5].timeline[52].cast_name == (None,)
    assert games[5].timeline[52].category == TimelineCategory.MissionCountdown
    assert games[5].timeline[52].elapsed_time == 108.88
    assert games[5].timeline[52].event == "missions completed. 10 second countdown."
    assert games[5].timeline[52].mission == Missions.NoMission
    assert games[5].timeline[52].role == (None,)
    assert games[5].timeline[52].time == 11.1

    assert games[5].timeline[53].action_test == ActionTest.NoAT
    assert games[5].timeline[53].actor == "spy"
    assert games[5].timeline[53].books == (None,)
    assert games[5].timeline[53].cast_name == (None,)
    assert games[5].timeline[53].category == TimelineCategory.Conversation
    assert games[5].timeline[53].elapsed_time == 117.19
    assert games[5].timeline[53].event == "spy leaves conversation."
    assert games[5].timeline[53].mission == Missions.NoMission
    assert games[5].timeline[53].role == (None,)
    assert games[5].timeline[53].time == 2.8

    assert games[5].timeline[54].action_test == ActionTest.NoAT
    assert games[5].timeline[54].actor == "spy"
    assert games[5].timeline[54].books == (None,)
    assert games[5].timeline[54].cast_name == (Characters.Taft,)
    assert games[5].timeline[54].category == TimelineCategory.Conversation
    assert games[5].timeline[54].elapsed_time == 117.19
    assert games[5].timeline[54].event == "spy left conversation with double agent."
    assert games[5].timeline[54].mission == Missions.NoMission
    assert games[5].timeline[54].role == (Roles.DoubleAgent,)
    assert games[5].timeline[54].time == 2.8

    assert games[5].timeline[55].action_test == ActionTest.NoAT
    assert games[5].timeline[55].actor == "game"
    assert games[5].timeline[55].books == (None,)
    assert games[5].timeline[55].cast_name == (None,)
    assert games[5].timeline[55].category == TimelineCategory.GameEnd
    assert games[5].timeline[55].elapsed_time == 118.94
    assert games[5].timeline[55].event == "missions completed successfully."
    assert games[5].timeline[55].mission == Missions.NoMission
    assert games[5].timeline[55].role == (None,)
    assert games[5].timeline[55].time == 1.0

    assert games[5].timeline.get_next_spy_action(games[5].timeline[55]) is None

    assert games[6].uuid == "8uf6pUK7TFegBD8Cbr2qMw"
    assert games[6].timeline[0].action_test == ActionTest.NoAT
    assert games[6].timeline[0].actor == "spy"
    assert games[6].timeline[0].books == (None,)
    assert games[6].timeline[0].cast_name == (Characters.Alice,)
    assert games[6].timeline[0].category == TimelineCategory.Cast
    assert games[6].timeline[0].elapsed_time == 0.0
    assert games[6].timeline[0].event == "spy cast."
    assert games[6].timeline[0].mission == Missions.NoMission
    assert games[6].timeline[0].role == (Roles.Spy,)
    assert games[6].timeline[0].time == 120.0

    assert games[6].timeline[1].action_test == ActionTest.NoAT
    assert games[6].timeline[1].actor == "spy"
    assert games[6].timeline[1].books == (None,)
    assert games[6].timeline[1].cast_name == (Characters.General,)
    assert games[6].timeline[1].category == TimelineCategory.Cast
    assert games[6].timeline[1].elapsed_time == 0.0
    assert games[6].timeline[1].event == "ambassador cast."
    assert games[6].timeline[1].mission == Missions.NoMission
    assert games[6].timeline[1].role == (Roles.Ambassador,)
    assert games[6].timeline[1].time == 120.0

    assert games[6].timeline[2].action_test == ActionTest.NoAT
    assert games[6].timeline[2].actor == "spy"
    assert games[6].timeline[2].books == (None,)
    assert games[6].timeline[2].cast_name == (Characters.Sikh,)
    assert games[6].timeline[2].category == TimelineCategory.Cast
    assert games[6].timeline[2].elapsed_time == 0.0
    assert games[6].timeline[2].event == "double agent cast."
    assert games[6].timeline[2].mission == Missions.NoMission
    assert games[6].timeline[2].role == (Roles.DoubleAgent,)
    assert games[6].timeline[2].time == 120.0

    assert games[6].timeline[3].action_test == ActionTest.NoAT
    assert games[6].timeline[3].actor == "spy"
    assert games[6].timeline[3].books == (None,)
    assert games[6].timeline[3].cast_name == (Characters.Disney,)
    assert games[6].timeline[3].category == TimelineCategory.Cast
    assert games[6].timeline[3].elapsed_time == 0.0
    assert games[6].timeline[3].event == "seduction target cast."
    assert games[6].timeline[3].mission == Missions.NoMission
    assert games[6].timeline[3].role == (Roles.SeductionTarget,)
    assert games[6].timeline[3].time == 120.0

    assert games[6].timeline[4].action_test == ActionTest.NoAT
    assert games[6].timeline[4].actor == "spy"
    assert games[6].timeline[4].books == (None,)
    assert games[6].timeline[4].cast_name == (Characters.Wheels,)
    assert games[6].timeline[4].category == TimelineCategory.Cast
    assert games[6].timeline[4].elapsed_time == 0.0
    assert games[6].timeline[4].event == "civilian cast."
    assert games[6].timeline[4].mission == Missions.NoMission
    assert games[6].timeline[4].role == (Roles.Civilian,)
    assert games[6].timeline[4].time == 120.0

    assert games[6].timeline[5].action_test == ActionTest.NoAT
    assert games[6].timeline[5].actor == "spy"
    assert games[6].timeline[5].books == (None,)
    assert games[6].timeline[5].cast_name == (Characters.Morgan,)
    assert games[6].timeline[5].category == TimelineCategory.Cast
    assert games[6].timeline[5].elapsed_time == 0.0
    assert games[6].timeline[5].event == "civilian cast."
    assert games[6].timeline[5].mission == Missions.NoMission
    assert games[6].timeline[5].role == (Roles.Civilian,)
    assert games[6].timeline[5].time == 120.0

    assert games[6].timeline[6].action_test == ActionTest.NoAT
    assert games[6].timeline[6].actor == "spy"
    assert games[6].timeline[6].books == (None,)
    assert games[6].timeline[6].cast_name == (Characters.Boots,)
    assert games[6].timeline[6].category == TimelineCategory.Cast
    assert games[6].timeline[6].elapsed_time == 0.0
    assert games[6].timeline[6].event == "civilian cast."
    assert games[6].timeline[6].mission == Missions.NoMission
    assert games[6].timeline[6].role == (Roles.Civilian,)
    assert games[6].timeline[6].time == 120.0

    assert games[6].timeline[7].action_test == ActionTest.NoAT
    assert games[6].timeline[7].actor == "spy"
    assert games[6].timeline[7].books == (None,)
    assert games[6].timeline[7].cast_name == (None,)
    assert games[6].timeline[7].category == TimelineCategory.MissionSelected
    assert games[6].timeline[7].elapsed_time == 0.0
    assert games[6].timeline[7].event == "bug ambassador selected."
    assert games[6].timeline[7].mission == Missions.Bug
    assert games[6].timeline[7].role == (None,)
    assert games[6].timeline[7].time == 120.0

    assert games[6].timeline[8].action_test == ActionTest.NoAT
    assert games[6].timeline[8].actor == "spy"
    assert games[6].timeline[8].books == (None,)
    assert games[6].timeline[8].cast_name == (None,)
    assert games[6].timeline[8].category == TimelineCategory.MissionSelected
    assert games[6].timeline[8].elapsed_time == 0.0
    assert games[6].timeline[8].event == "contact double agent selected."
    assert games[6].timeline[8].mission == Missions.Contact
    assert games[6].timeline[8].role == (None,)
    assert games[6].timeline[8].time == 120.0

    assert games[6].timeline[9].action_test == ActionTest.NoAT
    assert games[6].timeline[9].actor == "spy"
    assert games[6].timeline[9].books == (None,)
    assert games[6].timeline[9].cast_name == (None,)
    assert games[6].timeline[9].category == TimelineCategory.MissionSelected
    assert games[6].timeline[9].elapsed_time == 0.0
    assert games[6].timeline[9].event == "seduce target selected."
    assert games[6].timeline[9].mission == Missions.Seduce
    assert games[6].timeline[9].role == (None,)
    assert games[6].timeline[9].time == 120.0

    assert games[6].timeline[10].action_test == ActionTest.NoAT
    assert games[6].timeline[10].actor == "spy"
    assert games[6].timeline[10].books == (None,)
    assert games[6].timeline[10].cast_name == (None,)
    assert games[6].timeline[10].category == TimelineCategory.MissionEnabled
    assert games[6].timeline[10].elapsed_time == 0.0
    assert games[6].timeline[10].event == "bug ambassador enabled."
    assert games[6].timeline[10].mission == Missions.Bug
    assert games[6].timeline[10].role == (None,)
    assert games[6].timeline[10].time == 120.0

    assert games[6].timeline[11].action_test == ActionTest.NoAT
    assert games[6].timeline[11].actor == "spy"
    assert games[6].timeline[11].books == (None,)
    assert games[6].timeline[11].cast_name == (None,)
    assert games[6].timeline[11].category == TimelineCategory.MissionEnabled
    assert games[6].timeline[11].elapsed_time == 0.0
    assert games[6].timeline[11].event == "contact double agent enabled."
    assert games[6].timeline[11].mission == Missions.Contact
    assert games[6].timeline[11].role == (None,)
    assert games[6].timeline[11].time == 120.0

    assert games[6].timeline[12].action_test == ActionTest.NoAT
    assert games[6].timeline[12].actor == "spy"
    assert games[6].timeline[12].books == (None,)
    assert games[6].timeline[12].cast_name == (None,)
    assert games[6].timeline[12].category == TimelineCategory.MissionEnabled
    assert games[6].timeline[12].elapsed_time == 0.0
    assert games[6].timeline[12].event == "seduce target enabled."
    assert games[6].timeline[12].mission == Missions.Seduce
    assert games[6].timeline[12].role == (None,)
    assert games[6].timeline[12].time == 120.0

    assert games[6].timeline[13].action_test == ActionTest.NoAT
    assert games[6].timeline[13].actor == "game"
    assert games[6].timeline[13].books == (None,)
    assert games[6].timeline[13].cast_name == (None,)
    assert games[6].timeline[13].category == TimelineCategory.GameStart
    assert games[6].timeline[13].elapsed_time == 0.0
    assert games[6].timeline[13].event == "game started."
    assert games[6].timeline[13].mission == Missions.NoMission
    assert games[6].timeline[13].role == (None,)
    assert games[6].timeline[13].time == 120.0

    assert games[6].timeline[14].action_test == ActionTest.NoAT
    assert games[6].timeline[14].actor == "sniper"
    assert games[6].timeline[14].books == (None,)
    assert games[6].timeline[14].cast_name == (Characters.General,)
    assert games[6].timeline[14].category == TimelineCategory.SniperLights
    assert games[6].timeline[14].elapsed_time == 0.5
    assert games[6].timeline[14].event == "marked less suspicious."
    assert games[6].timeline[14].mission == Missions.NoMission
    assert games[6].timeline[14].role == (Roles.Ambassador,)
    assert games[6].timeline[14].time == 119.5

    assert games[6].timeline[15].action_test == ActionTest.NoAT
    assert games[6].timeline[15].actor == "spy"
    assert games[6].timeline[15].books == (None,)
    assert games[6].timeline[15].cast_name == (None,)
    assert games[6].timeline[15].category == TimelineCategory.NoCategory
    assert games[6].timeline[15].elapsed_time == 3.13
    assert games[6].timeline[15].event == "spy player takes control from ai."
    assert games[6].timeline[15].mission == Missions.NoMission
    assert games[6].timeline[15].role == (None,)
    assert games[6].timeline[15].time == 116.8

    assert games[6].timeline[16].action_test == ActionTest.NoAT
    assert games[6].timeline[16].actor == "sniper"
    assert games[6].timeline[16].books == (None,)
    assert games[6].timeline[16].cast_name == (Characters.Toby,)
    assert games[6].timeline[16].category == TimelineCategory.SniperLights
    assert games[6].timeline[16].elapsed_time == 5.25
    assert games[6].timeline[16].event == "marked suspicious."
    assert games[6].timeline[16].mission == Missions.NoMission
    assert games[6].timeline[16].role == (Roles.Staff,)
    assert games[6].timeline[16].time == 114.7

    assert games[6].timeline[17].action_test == ActionTest.NoAT
    assert games[6].timeline[17].actor == "sniper"
    assert games[6].timeline[17].books == (None,)
    assert games[6].timeline[17].cast_name == (Characters.Damon,)
    assert games[6].timeline[17].category == TimelineCategory.SniperLights
    assert games[6].timeline[17].elapsed_time == 7.19
    assert games[6].timeline[17].event == "marked suspicious."
    assert games[6].timeline[17].mission == Missions.NoMission
    assert games[6].timeline[17].role == (Roles.Staff,)
    assert games[6].timeline[17].time == 112.8

    assert games[6].timeline[18].action_test == ActionTest.NoAT
    assert games[6].timeline[18].actor == "sniper"
    assert games[6].timeline[18].books == (None,)
    assert games[6].timeline[18].cast_name == (Characters.Morgan,)
    assert games[6].timeline[18].category == TimelineCategory.SniperLights
    assert games[6].timeline[18].elapsed_time == 10.13
    assert games[6].timeline[18].event == "marked suspicious."
    assert games[6].timeline[18].mission == Missions.NoMission
    assert games[6].timeline[18].role == (Roles.Civilian,)
    assert games[6].timeline[18].time == 109.8

    assert games[6].timeline[19].action_test == ActionTest.NoAT
    assert games[6].timeline[19].actor == "spy"
    assert games[6].timeline[19].books == (None,)
    assert games[6].timeline[19].cast_name == (Characters.Sikh,)
    assert games[6].timeline[19].category == TimelineCategory.Conversation
    assert games[6].timeline[19].elapsed_time == 10.94
    assert games[6].timeline[19].event == "double agent joined conversation with spy."
    assert games[6].timeline[19].mission == Missions.NoMission
    assert games[6].timeline[19].role == (Roles.DoubleAgent,)
    assert games[6].timeline[19].time == 109.0

    assert games[6].timeline[20].action_test == ActionTest.NoAT
    assert games[6].timeline[20].actor == "spy"
    assert games[6].timeline[20].books == (None,)
    assert games[6].timeline[20].cast_name == (None,)
    assert games[6].timeline[20].category == TimelineCategory.Conversation
    assert games[6].timeline[20].elapsed_time == 11.13
    assert games[6].timeline[20].event == "spy leaves conversation."
    assert games[6].timeline[20].mission == Missions.NoMission
    assert games[6].timeline[20].role == (None,)
    assert games[6].timeline[20].time == 108.8

    assert games[6].timeline[21].action_test == ActionTest.NoAT
    assert games[6].timeline[21].actor == "spy"
    assert games[6].timeline[21].books == (None,)
    assert games[6].timeline[21].cast_name == (Characters.Sikh,)
    assert games[6].timeline[21].category == TimelineCategory.Conversation
    assert games[6].timeline[21].elapsed_time == 11.13
    assert games[6].timeline[21].event == "spy left conversation with double agent."
    assert games[6].timeline[21].mission == Missions.NoMission
    assert games[6].timeline[21].role == (Roles.DoubleAgent,)
    assert games[6].timeline[21].time == 108.8

    assert games[6].timeline[22].action_test == ActionTest.NoAT
    assert games[6].timeline[22].actor == "spy"
    assert games[6].timeline[22].books == (None,)
    assert games[6].timeline[22].cast_name == (None,)
    assert (
        games[6].timeline[22].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Watch
    )
    assert games[6].timeline[22].elapsed_time == 20.06
    assert games[6].timeline[22].event == "action triggered: check watch"
    assert games[6].timeline[22].mission == Missions.NoMission
    assert games[6].timeline[22].role == (None,)
    assert games[6].timeline[22].time == 99.9

    assert games[6].timeline[23].action_test == ActionTest.NoAT
    assert games[6].timeline[23].actor == "spy"
    assert games[6].timeline[23].books == (None,)
    assert games[6].timeline[23].cast_name == (Characters.Alice,)
    assert games[6].timeline[23].category == TimelineCategory.Watch
    assert games[6].timeline[23].elapsed_time == 20.06
    assert games[6].timeline[23].event == "watch checked."
    assert games[6].timeline[23].mission == Missions.NoMission
    assert games[6].timeline[23].role == (Roles.Spy,)
    assert games[6].timeline[23].time == 99.9

    assert games[6].timeline[24].action_test == ActionTest.NoAT
    assert games[6].timeline[24].actor == "spy"
    assert games[6].timeline[24].books == (None,)
    assert games[6].timeline[24].cast_name == (Characters.Alice,)
    assert games[6].timeline[24].category == TimelineCategory.Drinks
    assert games[6].timeline[24].elapsed_time == 28.63
    assert games[6].timeline[24].event == "took last sip of drink."
    assert games[6].timeline[24].mission == Missions.NoMission
    assert games[6].timeline[24].role == (Roles.Spy,)
    assert games[6].timeline[24].time == 91.3

    assert games[6].timeline[25].action_test == ActionTest.NoAT
    assert games[6].timeline[25].actor == "spy"
    assert games[6].timeline[25].books == (None,)
    assert games[6].timeline[25].cast_name == (Characters.Alice,)
    assert games[6].timeline[25].category == TimelineCategory.Drinks
    assert games[6].timeline[25].elapsed_time == 31.44
    assert games[6].timeline[25].event == "waiter offered drink."
    assert games[6].timeline[25].mission == Missions.NoMission
    assert games[6].timeline[25].role == (Roles.Spy,)
    assert games[6].timeline[25].time == 88.5

    assert games[6].timeline[26].action_test == ActionTest.NoAT
    assert games[6].timeline[26].actor == "spy"
    assert games[6].timeline[26].books == (None,)
    assert games[6].timeline[26].cast_name == (Characters.Alice,)
    assert games[6].timeline[26].category == TimelineCategory.Drinks
    assert games[6].timeline[26].elapsed_time == 31.88
    assert games[6].timeline[26].event == "rejected drink from waiter."
    assert games[6].timeline[26].mission == Missions.NoMission
    assert games[6].timeline[26].role == (Roles.Spy,)
    assert games[6].timeline[26].time == 88.1

    assert games[6].timeline[27].action_test == ActionTest.NoAT
    assert games[6].timeline[27].actor == "spy"
    assert games[6].timeline[27].books == (None,)
    assert games[6].timeline[27].cast_name == (Characters.Alice,)
    assert games[6].timeline[27].category == TimelineCategory.Drinks
    assert games[6].timeline[27].elapsed_time == 31.88
    assert games[6].timeline[27].event == "waiter stopped offering drink."
    assert games[6].timeline[27].mission == Missions.NoMission
    assert games[6].timeline[27].role == (Roles.Spy,)
    assert games[6].timeline[27].time == 88.1

    assert games[6].timeline[28].action_test == ActionTest.NoAT
    assert games[6].timeline[28].actor == "sniper"
    assert games[6].timeline[28].books == (None,)
    assert games[6].timeline[28].cast_name == (Characters.Wheels,)
    assert games[6].timeline[28].category == TimelineCategory.SniperLights
    assert games[6].timeline[28].elapsed_time == 33.06
    assert games[6].timeline[28].event == "marked suspicious."
    assert games[6].timeline[28].mission == Missions.NoMission
    assert games[6].timeline[28].role == (Roles.Civilian,)
    assert games[6].timeline[28].time == 86.9

    assert games[6].timeline[29].action_test == ActionTest.NoAT
    assert games[6].timeline[29].actor == "spy"
    assert games[6].timeline[29].books == (None,)
    assert games[6].timeline[29].cast_name == (None,)
    assert games[6].timeline[29].category == TimelineCategory.Conversation
    assert games[6].timeline[29].elapsed_time == 33.44
    assert games[6].timeline[29].event == "spy enters conversation."
    assert games[6].timeline[29].mission == Missions.NoMission
    assert games[6].timeline[29].role == (None,)
    assert games[6].timeline[29].time == 86.5

    assert games[6].timeline[30].action_test == ActionTest.NoAT
    assert games[6].timeline[30].actor == "sniper"
    assert games[6].timeline[30].books == (None,)
    assert games[6].timeline[30].cast_name == (Characters.Sikh,)
    assert games[6].timeline[30].category == TimelineCategory.SniperLights
    assert games[6].timeline[30].elapsed_time == 35.19
    assert games[6].timeline[30].event == "marked suspicious."
    assert games[6].timeline[30].mission == Missions.NoMission
    assert games[6].timeline[30].role == (Roles.DoubleAgent,)
    assert games[6].timeline[30].time == 84.8

    assert games[6].timeline[31].action_test == ActionTest.NoAT
    assert games[6].timeline[31].actor == "spy"
    assert games[6].timeline[31].books == (None,)
    assert games[6].timeline[31].cast_name == (None,)
    assert games[6].timeline[31].category == TimelineCategory.ActionTriggered
    assert games[6].timeline[31].elapsed_time == 36.63
    assert games[6].timeline[31].event == "action triggered: seduce target"
    assert games[6].timeline[31].mission == Missions.Seduce
    assert games[6].timeline[31].role == (None,)
    assert games[6].timeline[31].time == 83.3

    assert games[6].timeline[32].action_test == ActionTest.NoAT
    assert games[6].timeline[32].actor == "spy"
    assert games[6].timeline[32].books == (None,)
    assert games[6].timeline[32].cast_name == (Characters.Disney,)
    assert games[6].timeline[32].category == TimelineCategory.NoCategory
    assert games[6].timeline[32].elapsed_time == 36.63
    assert games[6].timeline[32].event == "begin flirtation with seduction target."
    assert games[6].timeline[32].mission == Missions.Seduce
    assert games[6].timeline[32].role == (Roles.SeductionTarget,)
    assert games[6].timeline[32].time == 83.3

    assert games[6].timeline[33].action_test == ActionTest.NoAT
    assert games[6].timeline[33].actor == "sniper"
    assert games[6].timeline[33].books == (None,)
    assert games[6].timeline[33].cast_name == (Characters.Wheels,)
    assert games[6].timeline[33].category == TimelineCategory.SniperLights
    assert games[6].timeline[33].elapsed_time == 36.94
    assert games[6].timeline[33].event == "marked neutral suspicion."
    assert games[6].timeline[33].mission == Missions.NoMission
    assert games[6].timeline[33].role == (Roles.Civilian,)
    assert games[6].timeline[33].time == 83.0

    assert games[6].timeline[34].action_test == ActionTest.Green
    assert games[6].timeline[34].actor == "spy"
    assert games[6].timeline[34].books == (None,)
    assert games[6].timeline[34].cast_name == (None,)
    assert games[6].timeline[34].category == TimelineCategory.ActionTest
    assert games[6].timeline[34].elapsed_time == 37.31
    assert games[6].timeline[34].event == "action test green: seduce target"
    assert games[6].timeline[34].mission == Missions.Seduce
    assert games[6].timeline[34].role == (None,)
    assert games[6].timeline[34].time == 82.6

    assert games[6].timeline[35].action_test == ActionTest.NoAT
    assert games[6].timeline[35].actor == "spy"
    assert games[6].timeline[35].books == (None,)
    assert games[6].timeline[35].cast_name == (Characters.Disney,)
    assert games[6].timeline[35].category == TimelineCategory.MissionPartial
    assert games[6].timeline[35].elapsed_time == 37.31
    assert games[6].timeline[35].event == "flirt with seduction target: 51%"
    assert games[6].timeline[35].mission == Missions.Seduce
    assert games[6].timeline[35].role == (Roles.SeductionTarget,)
    assert games[6].timeline[35].time == 82.6

    assert games[6].timeline[36].action_test == ActionTest.NoAT
    assert games[6].timeline[36].actor == "sniper"
    assert games[6].timeline[36].books == (None,)
    assert games[6].timeline[36].cast_name == (Characters.Alice,)
    assert games[6].timeline[36].category == TimelineCategory.SniperLights
    assert games[6].timeline[36].elapsed_time == 37.81
    assert games[6].timeline[36].event == "marked spy less suspicious."
    assert games[6].timeline[36].mission == Missions.NoMission
    assert games[6].timeline[36].role == (Roles.Spy,)
    assert games[6].timeline[36].time == 82.1

    assert games[6].timeline[37].action_test == ActionTest.NoAT
    assert games[6].timeline[37].actor == "sniper"
    assert games[6].timeline[37].books == (None,)
    assert games[6].timeline[37].cast_name == (Characters.Wheels,)
    assert games[6].timeline[37].category == TimelineCategory.SniperLights
    assert games[6].timeline[37].elapsed_time == 38.25
    assert games[6].timeline[37].event == "marked suspicious."
    assert games[6].timeline[37].mission == Missions.NoMission
    assert games[6].timeline[37].role == (Roles.Civilian,)
    assert games[6].timeline[37].time == 81.7

    assert games[6].timeline[38].action_test == ActionTest.NoAT
    assert games[6].timeline[38].actor == "sniper"
    assert games[6].timeline[38].books == (None,)
    assert games[6].timeline[38].cast_name == (Characters.Sikh,)
    assert games[6].timeline[38].category == TimelineCategory.SniperLights
    assert games[6].timeline[38].elapsed_time == 39.38
    assert games[6].timeline[38].event == "marked neutral suspicion."
    assert games[6].timeline[38].mission == Missions.NoMission
    assert games[6].timeline[38].role == (Roles.DoubleAgent,)
    assert games[6].timeline[38].time == 80.6

    assert games[6].timeline[39].action_test == ActionTest.NoAT
    assert games[6].timeline[39].actor == "sniper"
    assert games[6].timeline[39].books == (None,)
    assert games[6].timeline[39].cast_name == (Characters.Alice,)
    assert games[6].timeline[39].category == TimelineCategory.SniperLights
    assert games[6].timeline[39].elapsed_time == 44.88
    assert games[6].timeline[39].event == "marked spy neutral suspicion."
    assert games[6].timeline[39].mission == Missions.NoMission
    assert games[6].timeline[39].role == (Roles.Spy,)
    assert games[6].timeline[39].time == 75.1

    assert games[6].timeline[40].action_test == ActionTest.NoAT
    assert games[6].timeline[40].actor == "spy"
    assert games[6].timeline[40].books == (None,)
    assert games[6].timeline[40].cast_name == (Characters.Alice,)
    assert games[6].timeline[40].category == TimelineCategory.Drinks
    assert games[6].timeline[40].elapsed_time == 45.69
    assert games[6].timeline[40].event == "request drink from waiter."
    assert games[6].timeline[40].mission == Missions.NoMission
    assert games[6].timeline[40].role == (Roles.Spy,)
    assert games[6].timeline[40].time == 74.3

    assert games[6].timeline[41].action_test == ActionTest.NoAT
    assert games[6].timeline[41].actor == "spy"
    assert games[6].timeline[41].books == (None,)
    assert games[6].timeline[41].cast_name == (Characters.Alice,)
    assert games[6].timeline[41].category == TimelineCategory.Drinks
    assert games[6].timeline[41].elapsed_time == 45.88
    assert games[6].timeline[41].event == "waiter offered drink."
    assert games[6].timeline[41].mission == Missions.NoMission
    assert games[6].timeline[41].role == (Roles.Spy,)
    assert games[6].timeline[41].time == 74.1

    assert games[6].timeline[42].action_test == ActionTest.NoAT
    assert games[6].timeline[42].actor == "sniper"
    assert games[6].timeline[42].books == (None,)
    assert games[6].timeline[42].cast_name == (Characters.Alice,)
    assert games[6].timeline[42].category == TimelineCategory.SniperLights
    assert games[6].timeline[42].elapsed_time == 46.06
    assert games[6].timeline[42].event == "marked spy suspicious."
    assert games[6].timeline[42].mission == Missions.NoMission
    assert games[6].timeline[42].role == (Roles.Spy,)
    assert games[6].timeline[42].time == 73.9

    assert games[6].timeline[43].action_test == ActionTest.NoAT
    assert games[6].timeline[43].actor == "spy"
    assert games[6].timeline[43].books == (None,)
    assert games[6].timeline[43].cast_name == (Characters.Alice,)
    assert games[6].timeline[43].category == TimelineCategory.Drinks
    assert games[6].timeline[43].elapsed_time == 50.56
    assert games[6].timeline[43].event == "got drink from waiter."
    assert games[6].timeline[43].mission == Missions.NoMission
    assert games[6].timeline[43].role == (Roles.Spy,)
    assert games[6].timeline[43].time == 69.4

    assert games[6].timeline[44].action_test == ActionTest.NoAT
    assert games[6].timeline[44].actor == "spy"
    assert games[6].timeline[44].books == (None,)
    assert games[6].timeline[44].cast_name == (Characters.Alice,)
    assert games[6].timeline[44].category == TimelineCategory.Drinks
    assert games[6].timeline[44].elapsed_time == 50.56
    assert games[6].timeline[44].event == "waiter stopped offering drink."
    assert games[6].timeline[44].mission == Missions.NoMission
    assert games[6].timeline[44].role == (Roles.Spy,)
    assert games[6].timeline[44].time == 69.4

    assert games[6].timeline[45].action_test == ActionTest.NoAT
    assert games[6].timeline[45].actor == "spy"
    assert games[6].timeline[45].books == (None,)
    assert games[6].timeline[45].cast_name == (Characters.Sikh,)
    assert games[6].timeline[45].category == TimelineCategory.Conversation
    assert games[6].timeline[45].elapsed_time == 50.81
    assert games[6].timeline[45].event == "double agent joined conversation with spy."
    assert games[6].timeline[45].mission == Missions.NoMission
    assert games[6].timeline[45].role == (Roles.DoubleAgent,)
    assert games[6].timeline[45].time == 69.1
    assert games[6].timeline[46].action_test == ActionTest.NoAT
    assert games[6].timeline[46].actor == "spy"
    assert games[6].timeline[46].books == (None,)
    assert games[6].timeline[46].cast_name == (Characters.Alice,)
    assert games[6].timeline[46].category == TimelineCategory.Drinks
    assert games[6].timeline[46].elapsed_time == 63.81
    assert games[6].timeline[46].event == "sipped drink."
    assert games[6].timeline[46].mission == Missions.NoMission
    assert games[6].timeline[46].role == (Roles.Spy,)
    assert games[6].timeline[46].time == 56.1

    assert games[6].timeline[47].action_test == ActionTest.NoAT
    assert games[6].timeline[47].actor == "sniper"
    assert games[6].timeline[47].books == (None,)
    assert games[6].timeline[47].cast_name == (Characters.Boots,)
    assert games[6].timeline[47].category == TimelineCategory.SniperLights
    assert games[6].timeline[47].elapsed_time == 66.69
    assert games[6].timeline[47].event == "marked suspicious."
    assert games[6].timeline[47].mission == Missions.NoMission
    assert games[6].timeline[47].role == (Roles.Civilian,)
    assert games[6].timeline[47].time == 53.3

    assert games[6].timeline[48].action_test == ActionTest.NoAT
    assert games[6].timeline[48].actor == "sniper"
    assert games[6].timeline[48].books == (None,)
    assert games[6].timeline[48].cast_name == (Characters.Boots,)
    assert games[6].timeline[48].category == TimelineCategory.SniperLights
    assert games[6].timeline[48].elapsed_time == 67.56
    assert games[6].timeline[48].event == "marked neutral suspicion."
    assert games[6].timeline[48].mission == Missions.NoMission
    assert games[6].timeline[48].role == (Roles.Civilian,)
    assert games[6].timeline[48].time == 52.4

    assert games[6].timeline[49].action_test == ActionTest.NoAT
    assert games[6].timeline[49].actor == "spy"
    assert games[6].timeline[49].books == (None,)
    assert games[6].timeline[49].cast_name == (None,)
    assert games[6].timeline[49].category == TimelineCategory.ActionTriggered
    assert games[6].timeline[49].elapsed_time == 69.0
    assert games[6].timeline[49].event == "action triggered: contact double agent"
    assert games[6].timeline[49].mission == Missions.Contact
    assert games[6].timeline[49].role == (None,)
    assert games[6].timeline[49].time == 51.0

    assert games[6].timeline[50].action_test == ActionTest.NoAT
    assert games[6].timeline[50].actor == "spy"
    assert games[6].timeline[50].books == (None,)
    assert games[6].timeline[50].cast_name == (None,)
    assert games[6].timeline[50].category == TimelineCategory.BananaBread
    assert games[6].timeline[50].elapsed_time == 69.0
    assert games[6].timeline[50].event == "real banana bread started."
    assert games[6].timeline[50].mission == Missions.Contact
    assert games[6].timeline[50].role == (None,)
    assert games[6].timeline[50].time == 51.0

    assert games[6].timeline[51].action_test == ActionTest.Green
    assert games[6].timeline[51].actor == "spy"
    assert games[6].timeline[51].books == (None,)
    assert games[6].timeline[51].cast_name == (None,)
    assert games[6].timeline[51].category == TimelineCategory.ActionTest
    assert games[6].timeline[51].elapsed_time == 70.38
    assert games[6].timeline[51].event == "action test green: contact double agent"
    assert games[6].timeline[51].mission == Missions.Contact
    assert games[6].timeline[51].role == (None,)
    assert games[6].timeline[51].time == 49.6

    assert games[6].timeline[52].action_test == ActionTest.NoAT
    assert games[6].timeline[52].actor == "spy"
    assert games[6].timeline[52].books == (None,)
    assert games[6].timeline[52].cast_name == (None,)
    assert games[6].timeline[52].category == TimelineCategory.BananaBread
    assert games[6].timeline[52].elapsed_time == 70.38
    assert games[6].timeline[52].event == "banana bread uttered."
    assert games[6].timeline[52].mission == Missions.Contact
    assert games[6].timeline[52].role == (None,)
    assert games[6].timeline[52].time == 49.6

    assert games[6].timeline[53].action_test == ActionTest.NoAT
    assert games[6].timeline[53].actor == "spy"
    assert games[6].timeline[53].books == (None,)
    assert games[6].timeline[53].cast_name == (Characters.Sikh,)
    assert games[6].timeline[53].category == TimelineCategory.MissionComplete
    assert games[6].timeline[53].elapsed_time == 70.94
    assert games[6].timeline[53].event == "double agent contacted."
    assert games[6].timeline[53].mission == Missions.Contact
    assert games[6].timeline[53].role == (Roles.DoubleAgent,)
    assert games[6].timeline[53].time == 49.0

    assert games[6].timeline[54].action_test == ActionTest.NoAT
    assert games[6].timeline[54].actor == "sniper"
    assert games[6].timeline[54].books == (None,)
    assert games[6].timeline[54].cast_name == (Characters.Boots,)
    assert games[6].timeline[54].category == TimelineCategory.SniperLights
    assert games[6].timeline[54].elapsed_time == 71.5
    assert games[6].timeline[54].event == "marked suspicious."
    assert games[6].timeline[54].mission == Missions.NoMission
    assert games[6].timeline[54].role == (Roles.Civilian,)
    assert games[6].timeline[54].time == 48.5

    assert games[6].timeline[55].action_test == ActionTest.NoAT
    assert games[6].timeline[55].actor == "spy"
    assert games[6].timeline[55].books == (None,)
    assert games[6].timeline[55].cast_name == (Characters.General, Characters.Alice)
    assert games[6].timeline[55].category == TimelineCategory.NoCategory
    assert games[6].timeline[55].elapsed_time == 82.06
    assert games[6].timeline[55].event == "ambassador's personal space violated."
    assert games[6].timeline[55].mission == Missions.NoMission
    assert games[6].timeline[55].role == (Roles.Ambassador, Roles.Spy)
    assert games[6].timeline[55].time == 37.9

    assert games[6].timeline[56].action_test == ActionTest.NoAT
    assert games[6].timeline[56].actor == "spy"
    assert games[6].timeline[56].books == (None,)
    assert games[6].timeline[56].cast_name == (None,)
    assert games[6].timeline[56].category == TimelineCategory.NoCategory
    assert games[6].timeline[56].elapsed_time == 82.31
    assert games[6].timeline[56].event == "flirtation cooldown expired."
    assert games[6].timeline[56].mission == Missions.Seduce
    assert games[6].timeline[56].role == (None,)
    assert games[6].timeline[56].time == 37.6

    assert games[6].timeline[57].action_test == ActionTest.NoAT
    assert games[6].timeline[57].actor == "spy"
    assert games[6].timeline[57].books == (None,)
    assert games[6].timeline[57].cast_name == (None,)
    assert games[6].timeline[57].category == TimelineCategory.ActionTriggered
    assert games[6].timeline[57].elapsed_time == 84.5
    assert games[6].timeline[57].event == "action triggered: seduce target"
    assert games[6].timeline[57].mission == Missions.Seduce
    assert games[6].timeline[57].role == (None,)
    assert games[6].timeline[57].time == 35.5

    assert games[6].timeline[58].action_test == ActionTest.NoAT
    assert games[6].timeline[58].actor == "spy"
    assert games[6].timeline[58].books == (None,)
    assert games[6].timeline[58].cast_name == (Characters.Disney,)
    assert games[6].timeline[58].category == TimelineCategory.NoCategory
    assert games[6].timeline[58].elapsed_time == 84.5
    assert games[6].timeline[58].event == "begin flirtation with seduction target."
    assert games[6].timeline[58].mission == Missions.Seduce
    assert games[6].timeline[58].role == (Roles.SeductionTarget,)
    assert games[6].timeline[58].time == 35.5

    assert games[6].timeline[59].action_test == ActionTest.White
    assert games[6].timeline[59].actor == "spy"
    assert games[6].timeline[59].books == (None,)
    assert games[6].timeline[59].cast_name == (None,)
    assert games[6].timeline[59].category == TimelineCategory.ActionTest
    assert games[6].timeline[59].elapsed_time == 85.56
    assert games[6].timeline[59].event == "action test white: seduce target"
    assert games[6].timeline[59].mission == Missions.Seduce
    assert games[6].timeline[59].role == (None,)
    assert games[6].timeline[59].time == 34.4

    assert games[6].timeline[60].action_test == ActionTest.NoAT
    assert games[6].timeline[60].actor == "spy"
    assert games[6].timeline[60].books == (None,)
    assert games[6].timeline[60].cast_name == (Characters.Disney,)
    assert games[6].timeline[60].category == TimelineCategory.MissionPartial
    assert games[6].timeline[60].elapsed_time == 85.56
    assert games[6].timeline[60].event == "flirt with seduction target: 85%"
    assert games[6].timeline[60].mission == Missions.Seduce
    assert games[6].timeline[60].role == (Roles.SeductionTarget,)
    assert games[6].timeline[60].time == 34.4

    assert games[6].timeline[61].action_test == ActionTest.NoAT
    assert games[6].timeline[61].actor == "spy"
    assert games[6].timeline[61].books == (None,)
    assert games[6].timeline[61].cast_name == (None,)
    assert games[6].timeline[61].category == TimelineCategory.Conversation
    assert games[6].timeline[61].elapsed_time == 98.44
    assert games[6].timeline[61].event == "spy leaves conversation."
    assert games[6].timeline[61].mission == Missions.NoMission
    assert games[6].timeline[61].role == (None,)
    assert games[6].timeline[61].time == 21.5

    assert games[6].timeline[62].action_test == ActionTest.NoAT
    assert games[6].timeline[62].actor == "spy"
    assert games[6].timeline[62].books == (None,)
    assert games[6].timeline[62].cast_name == (Characters.Sikh,)
    assert games[6].timeline[62].category == TimelineCategory.Conversation
    assert games[6].timeline[62].elapsed_time == 98.44
    assert games[6].timeline[62].event == "spy left conversation with double agent."
    assert games[6].timeline[62].mission == Missions.NoMission
    assert games[6].timeline[62].role == (Roles.DoubleAgent,)
    assert games[6].timeline[62].time == 21.5

    assert games[6].timeline[63].action_test == ActionTest.NoAT
    assert games[6].timeline[63].actor == "spy"
    assert games[6].timeline[63].books == (None,)
    assert games[6].timeline[63].cast_name == (None,)
    assert games[6].timeline[63].category == TimelineCategory.NoCategory
    assert games[6].timeline[63].elapsed_time == 109.31
    assert games[6].timeline[63].event == "flirtation cooldown expired."
    assert games[6].timeline[63].mission == Missions.Seduce
    assert games[6].timeline[63].role == (None,)
    assert games[6].timeline[63].time == 10.6

    assert games[6].timeline[64].action_test == ActionTest.NoAT
    assert games[6].timeline[64].actor == "spy"
    assert games[6].timeline[64].books == (None,)
    assert games[6].timeline[64].cast_name == (Characters.Alice,)
    assert games[6].timeline[64].category == TimelineCategory.Drinks
    assert games[6].timeline[64].elapsed_time == 109.38
    assert games[6].timeline[64].event == "sipped drink."
    assert games[6].timeline[64].mission == Missions.NoMission
    assert games[6].timeline[64].role == (Roles.Spy,)
    assert games[6].timeline[64].time == 10.6

    assert games[6].timeline[65].action_test == ActionTest.NoAT
    assert games[6].timeline[65].actor == "spy"
    assert games[6].timeline[65].books == (None,)
    assert games[6].timeline[65].cast_name == (None,)
    assert games[6].timeline[65].category == TimelineCategory.Conversation
    assert games[6].timeline[65].elapsed_time == 113.44
    assert games[6].timeline[65].event == "spy enters conversation."
    assert games[6].timeline[65].mission == Missions.NoMission
    assert games[6].timeline[65].role == (None,)
    assert games[6].timeline[65].time == 6.5

    assert games[6].timeline[66].action_test == ActionTest.NoAT
    assert games[6].timeline[66].actor == "spy"
    assert games[6].timeline[66].books == (None,)
    assert games[6].timeline[66].cast_name == (Characters.Sikh,)
    assert games[6].timeline[66].category == TimelineCategory.Conversation
    assert games[6].timeline[66].elapsed_time == 114.25
    assert games[6].timeline[66].event == "double agent joined conversation with spy."
    assert games[6].timeline[66].mission == Missions.NoMission
    assert games[6].timeline[66].role == (Roles.DoubleAgent,)
    assert games[6].timeline[66].time == 5.7

    assert games[6].timeline[67].action_test == ActionTest.NoAT
    assert games[6].timeline[67].actor == "spy"
    assert games[6].timeline[67].books == (None,)
    assert games[6].timeline[67].cast_name == (None,)
    assert games[6].timeline[67].category == TimelineCategory.ActionTriggered
    assert games[6].timeline[67].elapsed_time == 115.69
    assert games[6].timeline[67].event == "action triggered: seduce target"
    assert games[6].timeline[67].mission == Missions.Seduce
    assert games[6].timeline[67].role == (None,)
    assert games[6].timeline[67].time == 4.3

    assert games[6].timeline[68].action_test == ActionTest.NoAT
    assert games[6].timeline[68].actor == "spy"
    assert games[6].timeline[68].books == (None,)
    assert games[6].timeline[68].cast_name == (Characters.Disney,)
    assert games[6].timeline[68].category == TimelineCategory.NoCategory
    assert games[6].timeline[68].elapsed_time == 115.69
    assert games[6].timeline[68].event == "begin flirtation with seduction target."
    assert games[6].timeline[68].mission == Missions.Seduce
    assert games[6].timeline[68].role == (Roles.SeductionTarget,)
    assert games[6].timeline[68].time == 4.3

    assert games[6].timeline[69].action_test == ActionTest.Ignored
    assert games[6].timeline[69].actor == "spy"
    assert games[6].timeline[69].books == (None,)
    assert games[6].timeline[69].cast_name == (None,)
    assert games[6].timeline[69].category == TimelineCategory.ActionTest
    assert games[6].timeline[69].elapsed_time == 117.13
    assert games[6].timeline[69].event == "action test ignored: seduce target"
    assert games[6].timeline[69].mission == Missions.Seduce
    assert games[6].timeline[69].role == (None,)
    assert games[6].timeline[69].time == 2.8

    assert games[6].timeline[70].action_test == ActionTest.NoAT
    assert games[6].timeline[70].actor == "spy"
    assert games[6].timeline[70].books == (None,)
    assert games[6].timeline[70].cast_name == (Characters.Disney,)
    assert games[6].timeline[70].category == TimelineCategory.MissionPartial
    assert games[6].timeline[70].elapsed_time == 117.13
    assert games[6].timeline[70].event == "flirt with seduction target: 100%"
    assert games[6].timeline[70].mission == Missions.Seduce
    assert games[6].timeline[70].role == (Roles.SeductionTarget,)
    assert games[6].timeline[70].time == 2.8

    assert games[6].timeline[71].action_test == ActionTest.NoAT
    assert games[6].timeline[71].actor == "spy"
    assert games[6].timeline[71].books == (None,)
    assert games[6].timeline[71].cast_name == (Characters.Disney,)
    assert games[6].timeline[71].category == TimelineCategory.MissionComplete
    assert games[6].timeline[71].elapsed_time == 117.13
    assert games[6].timeline[71].event == "target seduced."
    assert games[6].timeline[71].mission == Missions.Seduce
    assert games[6].timeline[71].role == (Roles.SeductionTarget,)
    assert games[6].timeline[71].time == 2.8

    assert games[6].timeline[72].action_test == ActionTest.NoAT
    assert games[6].timeline[72].actor == "game"
    assert games[6].timeline[72].books == (None,)
    assert games[6].timeline[72].cast_name == (None,)
    assert games[6].timeline[72].category == TimelineCategory.MissionCountdown
    assert games[6].timeline[72].elapsed_time == 117.13
    assert games[6].timeline[72].event == "missions completed. 10 second countdown."
    assert games[6].timeline[72].mission == Missions.NoMission
    assert games[6].timeline[72].role == (None,)
    assert games[6].timeline[72].time == 2.8

    assert games[6].timeline[73].action_test == ActionTest.NoAT
    assert games[6].timeline[73].actor == "game"
    assert games[6].timeline[73].books == (None,)
    assert games[6].timeline[73].cast_name == (None,)
    assert games[6].timeline[73].category == TimelineCategory.Overtime
    assert games[6].timeline[73].elapsed_time == 119.38
    assert games[6].timeline[73].event == "overtime!"
    assert games[6].timeline[73].mission == Missions.NoMission
    assert games[6].timeline[73].role == (None,)
    assert games[6].timeline[73].time == 0.6

    assert games[6].timeline[74].action_test == ActionTest.NoAT
    assert games[6].timeline[74].actor == "sniper"
    assert games[6].timeline[74].books == (None,)
    assert games[6].timeline[74].cast_name == (Characters.Boots,)
    assert games[6].timeline[74].category == TimelineCategory.SniperShot
    assert games[6].timeline[74].elapsed_time == 120.38
    assert games[6].timeline[74].event == "took shot."
    assert games[6].timeline[74].mission == Missions.NoMission
    assert games[6].timeline[74].role == (Roles.Civilian,)
    assert games[6].timeline[74].time == -0.3

    assert games[6].timeline[75].action_test == ActionTest.NoAT
    assert games[6].timeline[75].actor == "game"
    assert games[6].timeline[75].books == (None,)
    assert games[6].timeline[75].cast_name == (Characters.Boots,)
    assert games[6].timeline[75].category == TimelineCategory.GameEnd
    assert games[6].timeline[75].elapsed_time == 124.13
    assert games[6].timeline[75].event == "sniper shot civilian."
    assert games[6].timeline[75].mission == Missions.NoMission
    assert games[6].timeline[75].role == (Roles.Civilian,)
    assert games[6].timeline[75].time == -4.1

    assert games[6].timeline.get_next_spy_action(games[6].timeline[75]) is None

    assert games[7].uuid == "TPWiwN2aQc6EHEf6jKDKaA"
    assert games[7].timeline[0].action_test == ActionTest.NoAT
    assert games[7].timeline[0].actor == "spy"
    assert games[7].timeline[0].books == (None,)
    assert games[7].timeline[0].cast_name == (Characters.Bling,)
    assert games[7].timeline[0].category == TimelineCategory.Cast
    assert games[7].timeline[0].elapsed_time == 0.0
    assert games[7].timeline[0].event == "spy cast."
    assert games[7].timeline[0].mission == Missions.NoMission
    assert games[7].timeline[0].role == (Roles.Spy,)
    assert games[7].timeline[0].time == 210.0

    assert games[7].timeline[1].action_test == ActionTest.NoAT
    assert games[7].timeline[1].actor == "spy"
    assert games[7].timeline[1].books == (None,)
    assert games[7].timeline[1].cast_name == (Characters.Salmon,)
    assert games[7].timeline[1].category == TimelineCategory.Cast
    assert games[7].timeline[1].elapsed_time == 0.0
    assert games[7].timeline[1].event == "ambassador cast."
    assert games[7].timeline[1].mission == Missions.NoMission
    assert games[7].timeline[1].role == (Roles.Ambassador,)
    assert games[7].timeline[1].time == 210.0

    assert games[7].timeline[2].action_test == ActionTest.NoAT
    assert games[7].timeline[2].actor == "spy"
    assert games[7].timeline[2].books == (None,)
    assert games[7].timeline[2].cast_name == (Characters.Alice,)
    assert games[7].timeline[2].category == TimelineCategory.Cast
    assert games[7].timeline[2].elapsed_time == 0.0
    assert games[7].timeline[2].event == "double agent cast."
    assert games[7].timeline[2].mission == Missions.NoMission
    assert games[7].timeline[2].role == (Roles.DoubleAgent,)
    assert games[7].timeline[2].time == 210.0

    assert games[7].timeline[3].action_test == ActionTest.NoAT
    assert games[7].timeline[3].actor == "spy"
    assert games[7].timeline[3].books == (None,)
    assert games[7].timeline[3].cast_name == (Characters.Sari,)
    assert games[7].timeline[3].category == TimelineCategory.Cast
    assert games[7].timeline[3].elapsed_time == 0.0
    assert games[7].timeline[3].event == "seduction target cast."
    assert games[7].timeline[3].mission == Missions.NoMission
    assert games[7].timeline[3].role == (Roles.SeductionTarget,)
    assert games[7].timeline[3].time == 210.0

    assert games[7].timeline[4].action_test == ActionTest.NoAT
    assert games[7].timeline[4].actor == "spy"
    assert games[7].timeline[4].books == (None,)
    assert games[7].timeline[4].cast_name == (Characters.Carlos,)
    assert games[7].timeline[4].category == TimelineCategory.Cast
    assert games[7].timeline[4].elapsed_time == 0.0
    assert games[7].timeline[4].event == "civilian cast."
    assert games[7].timeline[4].mission == Missions.NoMission
    assert games[7].timeline[4].role == (Roles.Civilian,)
    assert games[7].timeline[4].time == 210.0

    assert games[7].timeline[5].action_test == ActionTest.NoAT
    assert games[7].timeline[5].actor == "spy"
    assert games[7].timeline[5].books == (None,)
    assert games[7].timeline[5].cast_name == (Characters.Smallman,)
    assert games[7].timeline[5].category == TimelineCategory.Cast
    assert games[7].timeline[5].elapsed_time == 0.0
    assert games[7].timeline[5].event == "civilian cast."
    assert games[7].timeline[5].mission == Missions.NoMission
    assert games[7].timeline[5].role == (Roles.Civilian,)
    assert games[7].timeline[5].time == 210.0

    assert games[7].timeline[6].action_test == ActionTest.NoAT
    assert games[7].timeline[6].actor == "spy"
    assert games[7].timeline[6].books == (None,)
    assert games[7].timeline[6].cast_name == (Characters.General,)
    assert games[7].timeline[6].category == TimelineCategory.Cast
    assert games[7].timeline[6].elapsed_time == 0.0
    assert games[7].timeline[6].event == "civilian cast."
    assert games[7].timeline[6].mission == Missions.NoMission
    assert games[7].timeline[6].role == (Roles.Civilian,)
    assert games[7].timeline[6].time == 210.0

    assert games[7].timeline[7].action_test == ActionTest.NoAT
    assert games[7].timeline[7].actor == "spy"
    assert games[7].timeline[7].books == (None,)
    assert games[7].timeline[7].cast_name == (Characters.Sikh,)
    assert games[7].timeline[7].category == TimelineCategory.Cast
    assert games[7].timeline[7].elapsed_time == 0.0
    assert games[7].timeline[7].event == "civilian cast."
    assert games[7].timeline[7].mission == Missions.NoMission
    assert games[7].timeline[7].role == (Roles.Civilian,)
    assert games[7].timeline[7].time == 210.0

    assert games[7].timeline[8].action_test == ActionTest.NoAT
    assert games[7].timeline[8].actor == "spy"
    assert games[7].timeline[8].books == (None,)
    assert games[7].timeline[8].cast_name == (Characters.Queen,)
    assert games[7].timeline[8].category == TimelineCategory.Cast
    assert games[7].timeline[8].elapsed_time == 0.0
    assert games[7].timeline[8].event == "civilian cast."
    assert games[7].timeline[8].mission == Missions.NoMission
    assert games[7].timeline[8].role == (Roles.Civilian,)
    assert games[7].timeline[8].time == 210.0

    assert games[7].timeline[9].action_test == ActionTest.NoAT
    assert games[7].timeline[9].actor == "spy"
    assert games[7].timeline[9].books == (None,)
    assert games[7].timeline[9].cast_name == (Characters.Taft,)
    assert games[7].timeline[9].category == TimelineCategory.Cast
    assert games[7].timeline[9].elapsed_time == 0.0
    assert games[7].timeline[9].event == "civilian cast."
    assert games[7].timeline[9].mission == Missions.NoMission
    assert games[7].timeline[9].role == (Roles.Civilian,)
    assert games[7].timeline[9].time == 210.0

    assert games[7].timeline[10].action_test == ActionTest.NoAT
    assert games[7].timeline[10].actor == "spy"
    assert games[7].timeline[10].books == (None,)
    assert games[7].timeline[10].cast_name == (Characters.Oprah,)
    assert games[7].timeline[10].category == TimelineCategory.Cast
    assert games[7].timeline[10].elapsed_time == 0.0
    assert games[7].timeline[10].event == "civilian cast."
    assert games[7].timeline[10].mission == Missions.NoMission
    assert games[7].timeline[10].role == (Roles.Civilian,)
    assert games[7].timeline[10].time == 210.0

    assert games[7].timeline[11].action_test == ActionTest.NoAT
    assert games[7].timeline[11].actor == "spy"
    assert games[7].timeline[11].books == (None,)
    assert games[7].timeline[11].cast_name == (Characters.Plain,)
    assert games[7].timeline[11].category == TimelineCategory.Cast
    assert games[7].timeline[11].elapsed_time == 0.0
    assert games[7].timeline[11].event == "civilian cast."
    assert games[7].timeline[11].mission == Missions.NoMission
    assert games[7].timeline[11].role == (Roles.Civilian,)
    assert games[7].timeline[11].time == 210.0

    assert games[7].timeline[12].action_test == ActionTest.NoAT
    assert games[7].timeline[12].actor == "spy"
    assert games[7].timeline[12].books == (None,)
    assert games[7].timeline[12].cast_name == (None,)
    assert games[7].timeline[12].category == TimelineCategory.MissionSelected
    assert games[7].timeline[12].elapsed_time == 0.0
    assert games[7].timeline[12].event == "bug ambassador selected."
    assert games[7].timeline[12].mission == Missions.Bug
    assert games[7].timeline[12].role == (None,)
    assert games[7].timeline[12].time == 210.0

    assert games[7].timeline[13].action_test == ActionTest.NoAT
    assert games[7].timeline[13].actor == "spy"
    assert games[7].timeline[13].books == (None,)
    assert games[7].timeline[13].cast_name == (None,)
    assert games[7].timeline[13].category == TimelineCategory.MissionSelected
    assert games[7].timeline[13].elapsed_time == 0.0
    assert games[7].timeline[13].event == "contact double agent selected."
    assert games[7].timeline[13].mission == Missions.Contact
    assert games[7].timeline[13].role == (None,)
    assert games[7].timeline[13].time == 210.0

    assert games[7].timeline[14].action_test == ActionTest.NoAT
    assert games[7].timeline[14].actor == "spy"
    assert games[7].timeline[14].books == (None,)
    assert games[7].timeline[14].cast_name == (None,)
    assert games[7].timeline[14].category == TimelineCategory.MissionSelected
    assert games[7].timeline[14].elapsed_time == 0.0
    assert games[7].timeline[14].event == "seduce target selected."
    assert games[7].timeline[14].mission == Missions.Seduce
    assert games[7].timeline[14].role == (None,)
    assert games[7].timeline[14].time == 210.0

    assert games[7].timeline[15].action_test == ActionTest.NoAT
    assert games[7].timeline[15].actor == "spy"
    assert games[7].timeline[15].books == (None,)
    assert games[7].timeline[15].cast_name == (None,)
    assert games[7].timeline[15].category == TimelineCategory.MissionSelected
    assert games[7].timeline[15].elapsed_time == 0.0
    assert games[7].timeline[15].event == "purloin guest list selected."
    assert games[7].timeline[15].mission == Missions.Purloin
    assert games[7].timeline[15].role == (None,)
    assert games[7].timeline[15].time == 210.0

    assert games[7].timeline[16].action_test == ActionTest.NoAT
    assert games[7].timeline[16].actor == "spy"
    assert games[7].timeline[16].books == (None,)
    assert games[7].timeline[16].cast_name == (None,)
    assert games[7].timeline[16].category == TimelineCategory.MissionSelected
    assert games[7].timeline[16].elapsed_time == 0.0
    assert games[7].timeline[16].event == "fingerprint ambassador selected."
    assert games[7].timeline[16].mission == Missions.Fingerprint
    assert games[7].timeline[16].role == (None,)
    assert games[7].timeline[16].time == 210.0

    assert games[7].timeline[17].action_test == ActionTest.NoAT
    assert games[7].timeline[17].actor == "spy"
    assert games[7].timeline[17].books == (None,)
    assert games[7].timeline[17].cast_name == (None,)
    assert games[7].timeline[17].category == TimelineCategory.MissionEnabled
    assert games[7].timeline[17].elapsed_time == 0.0
    assert games[7].timeline[17].event == "bug ambassador enabled."
    assert games[7].timeline[17].mission == Missions.Bug
    assert games[7].timeline[17].role == (None,)
    assert games[7].timeline[17].time == 210.0

    assert games[7].timeline[18].action_test == ActionTest.NoAT
    assert games[7].timeline[18].actor == "spy"
    assert games[7].timeline[18].books == (None,)
    assert games[7].timeline[18].cast_name == (None,)
    assert games[7].timeline[18].category == TimelineCategory.MissionEnabled
    assert games[7].timeline[18].elapsed_time == 0.0
    assert games[7].timeline[18].event == "contact double agent enabled."
    assert games[7].timeline[18].mission == Missions.Contact
    assert games[7].timeline[18].role == (None,)
    assert games[7].timeline[18].time == 210.0

    assert games[7].timeline[19].action_test == ActionTest.NoAT
    assert games[7].timeline[19].actor == "spy"
    assert games[7].timeline[19].books == (None,)
    assert games[7].timeline[19].cast_name == (None,)
    assert games[7].timeline[19].category == TimelineCategory.MissionEnabled
    assert games[7].timeline[19].elapsed_time == 0.0
    assert games[7].timeline[19].event == "seduce target enabled."
    assert games[7].timeline[19].mission == Missions.Seduce
    assert games[7].timeline[19].role == (None,)
    assert games[7].timeline[19].time == 210.0

    assert games[7].timeline[20].action_test == ActionTest.NoAT
    assert games[7].timeline[20].actor == "spy"
    assert games[7].timeline[20].books == (None,)
    assert games[7].timeline[20].cast_name == (None,)
    assert games[7].timeline[20].category == TimelineCategory.MissionEnabled
    assert games[7].timeline[20].elapsed_time == 0.0
    assert games[7].timeline[20].event == "purloin guest list enabled."
    assert games[7].timeline[20].mission == Missions.Purloin
    assert games[7].timeline[20].role == (None,)
    assert games[7].timeline[20].time == 210.0

    assert games[7].timeline[21].action_test == ActionTest.NoAT
    assert games[7].timeline[21].actor == "spy"
    assert games[7].timeline[21].books == (None,)
    assert games[7].timeline[21].cast_name == (None,)
    assert games[7].timeline[21].category == TimelineCategory.MissionEnabled
    assert games[7].timeline[21].elapsed_time == 0.0
    assert games[7].timeline[21].event == "fingerprint ambassador enabled."
    assert games[7].timeline[21].mission == Missions.Fingerprint
    assert games[7].timeline[21].role == (None,)
    assert games[7].timeline[21].time == 210.0

    assert games[7].timeline[22].action_test == ActionTest.NoAT
    assert games[7].timeline[22].actor == "game"
    assert games[7].timeline[22].books == (None,)
    assert games[7].timeline[22].cast_name == (None,)
    assert games[7].timeline[22].category == TimelineCategory.GameStart
    assert games[7].timeline[22].elapsed_time == 0.0
    assert games[7].timeline[22].event == "game started."
    assert games[7].timeline[22].mission == Missions.NoMission
    assert games[7].timeline[22].role == (None,)
    assert games[7].timeline[22].time == 210.0

    assert games[7].timeline[23].action_test == ActionTest.NoAT
    assert games[7].timeline[23].actor == "sniper"
    assert games[7].timeline[23].books == (None,)
    assert games[7].timeline[23].cast_name == (Characters.Alice,)
    assert games[7].timeline[23].category == TimelineCategory.SniperLights
    assert games[7].timeline[23].elapsed_time == 0.63
    assert games[7].timeline[23].event == "marked less suspicious."
    assert games[7].timeline[23].mission == Missions.NoMission
    assert games[7].timeline[23].role == (Roles.DoubleAgent,)
    assert games[7].timeline[23].time == 209.3

    assert games[7].timeline[24].action_test == ActionTest.NoAT
    assert games[7].timeline[24].actor == "sniper"
    assert games[7].timeline[24].books == (None,)
    assert games[7].timeline[24].cast_name == (Characters.Salmon,)
    assert games[7].timeline[24].category == TimelineCategory.SniperLights
    assert games[7].timeline[24].elapsed_time == 1.31
    assert games[7].timeline[24].event == "marked less suspicious."
    assert games[7].timeline[24].mission == Missions.NoMission
    assert games[7].timeline[24].role == (Roles.Ambassador,)
    assert games[7].timeline[24].time == 208.6

    assert games[7].timeline[25].action_test == ActionTest.NoAT
    assert games[7].timeline[25].actor == "spy"
    assert games[7].timeline[25].books == (None,)
    assert games[7].timeline[25].cast_name == (None,)
    assert games[7].timeline[25].category == TimelineCategory.NoCategory
    assert games[7].timeline[25].elapsed_time == 1.63
    assert games[7].timeline[25].event == "spy player takes control from ai."
    assert games[7].timeline[25].mission == Missions.NoMission
    assert games[7].timeline[25].role == (None,)
    assert games[7].timeline[25].time == 208.3

    assert games[7].timeline[26].action_test == ActionTest.NoAT
    assert games[7].timeline[26].actor == "spy"
    assert games[7].timeline[26].books == (None,)
    assert games[7].timeline[26].cast_name == (None,)
    assert games[7].timeline[26].category == TimelineCategory.Conversation
    assert games[7].timeline[26].elapsed_time == 2.44
    assert games[7].timeline[26].event == "spy enters conversation."
    assert games[7].timeline[26].mission == Missions.NoMission
    assert games[7].timeline[26].role == (None,)
    assert games[7].timeline[26].time == 207.5

    assert games[7].timeline[27].action_test == ActionTest.NoAT
    assert games[7].timeline[27].actor == "sniper"
    assert games[7].timeline[27].books == (None,)
    assert games[7].timeline[27].cast_name == (Characters.Damon,)
    assert games[7].timeline[27].category == TimelineCategory.SniperLights
    assert games[7].timeline[27].elapsed_time == 2.94
    assert games[7].timeline[27].event == "marked less suspicious."
    assert games[7].timeline[27].mission == Missions.NoMission
    assert games[7].timeline[27].role == (Roles.Staff,)
    assert games[7].timeline[27].time == 207.0

    assert games[7].timeline[28].action_test == ActionTest.NoAT
    assert games[7].timeline[28].actor == "spy"
    assert games[7].timeline[28].books == (None,)
    assert games[7].timeline[28].cast_name == (None,)
    assert games[7].timeline[28].category == TimelineCategory.ActionTriggered
    assert games[7].timeline[28].elapsed_time == 4.19
    assert games[7].timeline[28].event == "action triggered: seduce target"
    assert games[7].timeline[28].mission == Missions.Seduce
    assert games[7].timeline[28].role == (None,)
    assert games[7].timeline[28].time == 205.8

    assert games[7].timeline[29].action_test == ActionTest.NoAT
    assert games[7].timeline[29].actor == "spy"
    assert games[7].timeline[29].books == (None,)
    assert games[7].timeline[29].cast_name == (Characters.Sari,)
    assert games[7].timeline[29].category == TimelineCategory.NoCategory
    assert games[7].timeline[29].elapsed_time == 4.19
    assert games[7].timeline[29].event == "begin flirtation with seduction target."
    assert games[7].timeline[29].mission == Missions.Seduce
    assert games[7].timeline[29].role == (Roles.SeductionTarget,)
    assert games[7].timeline[29].time == 205.8

    assert games[7].timeline[30].action_test == ActionTest.White
    assert games[7].timeline[30].actor == "spy"
    assert games[7].timeline[30].books == (None,)
    assert games[7].timeline[30].cast_name == (None,)
    assert games[7].timeline[30].category == TimelineCategory.ActionTest
    assert games[7].timeline[30].elapsed_time == 5.38
    assert games[7].timeline[30].event == "action test white: seduce target"
    assert games[7].timeline[30].mission == Missions.Seduce
    assert games[7].timeline[30].role == (None,)
    assert games[7].timeline[30].time == 204.6

    assert games[7].timeline[31].action_test == ActionTest.NoAT
    assert games[7].timeline[31].actor == "spy"
    assert games[7].timeline[31].books == (None,)
    assert games[7].timeline[31].cast_name == (Characters.Sari,)
    assert games[7].timeline[31].category == TimelineCategory.MissionPartial
    assert games[7].timeline[31].elapsed_time == 5.38
    assert games[7].timeline[31].event == "flirt with seduction target: 34%"
    assert games[7].timeline[31].mission == Missions.Seduce
    assert games[7].timeline[31].role == (Roles.SeductionTarget,)
    assert games[7].timeline[31].time == 204.6

    assert games[7].timeline[32].action_test == ActionTest.NoAT
    assert games[7].timeline[32].actor == "sniper"
    assert games[7].timeline[32].books == (None,)
    assert games[7].timeline[32].cast_name == (Characters.Toby,)
    assert games[7].timeline[32].category == TimelineCategory.SniperLights
    assert games[7].timeline[32].elapsed_time == 6.0
    assert games[7].timeline[32].event == "marked less suspicious."
    assert games[7].timeline[32].mission == Missions.NoMission
    assert games[7].timeline[32].role == (Roles.Staff,)
    assert games[7].timeline[32].time == 204.0

    assert games[7].timeline[33].action_test == ActionTest.NoAT
    assert games[7].timeline[33].actor == "sniper"
    assert games[7].timeline[33].books == (None,)
    assert games[7].timeline[33].cast_name == (Characters.Sikh,)
    assert games[7].timeline[33].category == TimelineCategory.SniperLights
    assert games[7].timeline[33].elapsed_time == 6.31
    assert games[7].timeline[33].event == "marked suspicious."
    assert games[7].timeline[33].mission == Missions.NoMission
    assert games[7].timeline[33].role == (Roles.Civilian,)
    assert games[7].timeline[33].time == 203.6

    assert games[7].timeline[34].action_test == ActionTest.NoAT
    assert games[7].timeline[34].actor == "spy"
    assert games[7].timeline[34].books == (None,)
    assert games[7].timeline[34].cast_name == (Characters.Bling,)
    assert games[7].timeline[34].category == TimelineCategory.Drinks
    assert games[7].timeline[34].elapsed_time == 21.0
    assert games[7].timeline[34].event == "took last sip of drink."
    assert games[7].timeline[34].mission == Missions.NoMission
    assert games[7].timeline[34].role == (Roles.Spy,)
    assert games[7].timeline[34].time == 189.0

    assert games[7].timeline[35].action_test == ActionTest.NoAT
    assert games[7].timeline[35].actor == "sniper"
    assert games[7].timeline[35].books == (None,)
    assert games[7].timeline[35].cast_name == (Characters.Oprah,)
    assert games[7].timeline[35].category == TimelineCategory.SniperLights
    assert games[7].timeline[35].elapsed_time == 33.06
    assert games[7].timeline[35].event == "marked suspicious."
    assert games[7].timeline[35].mission == Missions.NoMission
    assert games[7].timeline[35].role == (Roles.Civilian,)
    assert games[7].timeline[35].time == 176.9

    assert games[7].timeline[36].action_test == ActionTest.NoAT
    assert games[7].timeline[36].actor == "spy"
    assert games[7].timeline[36].books == (None,)
    assert games[7].timeline[36].cast_name == (None,)
    assert games[7].timeline[36].category == TimelineCategory.Conversation
    assert games[7].timeline[36].elapsed_time == 36.69
    assert games[7].timeline[36].event == "spy leaves conversation."
    assert games[7].timeline[36].mission == Missions.NoMission
    assert games[7].timeline[36].role == (None,)
    assert games[7].timeline[36].time == 173.3

    assert games[7].timeline[37].action_test == ActionTest.NoAT
    assert games[7].timeline[37].actor == "spy"
    assert games[7].timeline[37].books == (None,)
    assert games[7].timeline[37].cast_name == (None,)
    assert games[7].timeline[37].category == TimelineCategory.NoCategory
    assert games[7].timeline[37].elapsed_time == 37.19
    assert games[7].timeline[37].event == "flirtation cooldown expired."
    assert games[7].timeline[37].mission == Missions.Seduce
    assert games[7].timeline[37].role == (None,)
    assert games[7].timeline[37].time == 172.8

    assert games[7].timeline[38].action_test == ActionTest.NoAT
    assert games[7].timeline[38].actor == "spy"
    assert games[7].timeline[38].books == (None,)
    assert games[7].timeline[38].cast_name == (None,)
    assert games[7].timeline[38].category == TimelineCategory.Briefcase
    assert games[7].timeline[38].elapsed_time == 43.25
    assert games[7].timeline[38].event == "spy picks up briefcase."
    assert games[7].timeline[38].mission == Missions.NoMission
    assert games[7].timeline[38].role == (None,)
    assert games[7].timeline[38].time == 166.7

    assert games[7].timeline[39].action_test == ActionTest.NoAT
    assert games[7].timeline[39].actor == "spy"
    assert games[7].timeline[39].books == (None,)
    assert games[7].timeline[39].cast_name == (None,)
    assert games[7].timeline[39].category == TimelineCategory.Briefcase
    assert games[7].timeline[39].elapsed_time == 43.25
    assert games[7].timeline[39].event == "picked up fingerprintable briefcase."
    assert games[7].timeline[39].mission == Missions.Fingerprint
    assert games[7].timeline[39].role == (None,)
    assert games[7].timeline[39].time == 166.7

    assert games[7].timeline[40].action_test == ActionTest.NoAT
    assert games[7].timeline[40].actor == "spy"
    assert games[7].timeline[40].books == (None,)
    assert games[7].timeline[40].cast_name == (None,)
    assert games[7].timeline[40].category == TimelineCategory.ActionTriggered
    assert games[7].timeline[40].elapsed_time == 45.69
    assert games[7].timeline[40].event == "action triggered: fingerprint ambassador"
    assert games[7].timeline[40].mission == Missions.Fingerprint
    assert games[7].timeline[40].role == (None,)
    assert games[7].timeline[40].time == 164.3

    assert games[7].timeline[41].action_test == ActionTest.NoAT
    assert games[7].timeline[41].actor == "spy"
    assert games[7].timeline[41].books == (None,)
    assert games[7].timeline[41].cast_name == (None,)
    assert games[7].timeline[41].category == TimelineCategory.Briefcase
    assert games[7].timeline[41].elapsed_time == 45.69
    assert games[7].timeline[41].event == "started fingerprinting briefcase."
    assert games[7].timeline[41].mission == Missions.Fingerprint
    assert games[7].timeline[41].role == (None,)
    assert games[7].timeline[41].time == 164.3

    assert games[7].timeline[42].action_test == ActionTest.NoAT
    assert games[7].timeline[42].actor == "spy"
    assert games[7].timeline[42].books == (None,)
    assert games[7].timeline[42].cast_name == (None,)
    assert (
        games[7].timeline[42].category
        == TimelineCategory.MissionPartial | TimelineCategory.Briefcase
    )
    assert games[7].timeline[42].elapsed_time == 46.69
    assert games[7].timeline[42].event == "fingerprinted briefcase."
    assert games[7].timeline[42].mission == Missions.Fingerprint
    assert games[7].timeline[42].role == (None,)
    assert games[7].timeline[42].time == 163.3

    assert games[7].timeline[43].action_test == ActionTest.NoAT
    assert games[7].timeline[43].actor == "spy"
    assert games[7].timeline[43].books == (None,)
    assert games[7].timeline[43].cast_name == (None,)
    assert games[7].timeline[43].category == TimelineCategory.Briefcase
    assert games[7].timeline[43].elapsed_time == 50.88
    assert games[7].timeline[43].event == "spy puts down briefcase."
    assert games[7].timeline[43].mission == Missions.NoMission
    assert games[7].timeline[43].role == (None,)
    assert games[7].timeline[43].time == 159.1

    assert games[7].timeline[44].action_test == ActionTest.NoAT
    assert games[7].timeline[44].actor == "spy"
    assert games[7].timeline[44].books == (None,)
    assert games[7].timeline[44].cast_name == (None,)
    assert (
        games[7].timeline[44].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Watch
    )
    assert games[7].timeline[44].elapsed_time == 58.56
    assert games[7].timeline[44].event == "action triggered: check watch"
    assert games[7].timeline[44].mission == Missions.NoMission
    assert games[7].timeline[44].role == (None,)
    assert games[7].timeline[44].time == 151.4

    assert games[7].timeline[45].action_test == ActionTest.NoAT
    assert games[7].timeline[45].actor == "spy"
    assert games[7].timeline[45].books == (None,)
    assert games[7].timeline[45].cast_name == (Characters.Bling,)
    assert games[7].timeline[45].category == TimelineCategory.Watch
    assert games[7].timeline[45].elapsed_time == 58.56
    assert games[7].timeline[45].event == "watch checked."
    assert games[7].timeline[45].mission == Missions.NoMission
    assert games[7].timeline[45].role == (Roles.Spy,)
    assert games[7].timeline[45].time == 151.4

    assert games[7].timeline[46].action_test == ActionTest.NoAT
    assert games[7].timeline[46].actor == "sniper"
    assert games[7].timeline[46].books == (None,)
    assert games[7].timeline[46].cast_name == (Characters.Queen,)
    assert games[7].timeline[46].category == TimelineCategory.SniperLights
    assert games[7].timeline[46].elapsed_time == 58.75
    assert games[7].timeline[46].event == "marked suspicious."
    assert games[7].timeline[46].mission == Missions.NoMission
    assert games[7].timeline[46].role == (Roles.Civilian,)
    assert games[7].timeline[46].time == 151.2

    assert games[7].timeline[47].action_test == ActionTest.NoAT
    assert games[7].timeline[47].actor == "sniper"
    assert games[7].timeline[47].books == (None,)
    assert games[7].timeline[47].cast_name == (Characters.Oprah,)
    assert games[7].timeline[47].category == TimelineCategory.SniperLights
    assert games[7].timeline[47].elapsed_time == 60.88
    assert games[7].timeline[47].event == "marked neutral suspicion."
    assert games[7].timeline[47].mission == Missions.NoMission
    assert games[7].timeline[47].role == (Roles.Civilian,)
    assert games[7].timeline[47].time == 149.1

    assert games[7].timeline[48].action_test == ActionTest.NoAT
    assert games[7].timeline[48].actor == "spy"
    assert games[7].timeline[48].books == (None,)
    assert games[7].timeline[48].cast_name == (None,)
    assert games[7].timeline[48].category == TimelineCategory.Conversation
    assert games[7].timeline[48].elapsed_time == 65.44
    assert games[7].timeline[48].event == "spy enters conversation."
    assert games[7].timeline[48].mission == Missions.NoMission
    assert games[7].timeline[48].role == (None,)
    assert games[7].timeline[48].time == 144.5

    assert games[7].timeline[49].action_test == ActionTest.NoAT
    assert games[7].timeline[49].actor == "spy"
    assert games[7].timeline[49].books == (None,)
    assert games[7].timeline[49].cast_name == (Characters.Alice,)
    assert games[7].timeline[49].category == TimelineCategory.Conversation
    assert games[7].timeline[49].elapsed_time == 65.44
    assert games[7].timeline[49].event == "spy joined conversation with double agent."
    assert games[7].timeline[49].mission == Missions.NoMission
    assert games[7].timeline[49].role == (Roles.DoubleAgent,)
    assert games[7].timeline[49].time == 144.5

    assert games[7].timeline[50].action_test == ActionTest.NoAT
    assert games[7].timeline[50].actor == "spy"
    assert games[7].timeline[50].books == (None,)
    assert games[7].timeline[50].cast_name == (None,)
    assert games[7].timeline[50].category == TimelineCategory.ActionTriggered
    assert games[7].timeline[50].elapsed_time == 69.38
    assert games[7].timeline[50].event == "action triggered: contact double agent"
    assert games[7].timeline[50].mission == Missions.Contact
    assert games[7].timeline[50].role == (None,)
    assert games[7].timeline[50].time == 140.6

    assert games[7].timeline[51].action_test == ActionTest.NoAT
    assert games[7].timeline[51].actor == "spy"
    assert games[7].timeline[51].books == (None,)
    assert games[7].timeline[51].cast_name == (None,)
    assert games[7].timeline[51].category == TimelineCategory.BananaBread
    assert games[7].timeline[51].elapsed_time == 69.38
    assert games[7].timeline[51].event == "real banana bread started."
    assert games[7].timeline[51].mission == Missions.Contact
    assert games[7].timeline[51].role == (None,)
    assert games[7].timeline[51].time == 140.6

    assert games[7].timeline[52].action_test == ActionTest.White
    assert games[7].timeline[52].actor == "spy"
    assert games[7].timeline[52].books == (None,)
    assert games[7].timeline[52].cast_name == (None,)
    assert games[7].timeline[52].category == TimelineCategory.ActionTest
    assert games[7].timeline[52].elapsed_time == 70.06
    assert games[7].timeline[52].event == "action test white: contact double agent"
    assert games[7].timeline[52].mission == Missions.Contact
    assert games[7].timeline[52].role == (None,)
    assert games[7].timeline[52].time == 139.9

    assert games[7].timeline[53].action_test == ActionTest.NoAT
    assert games[7].timeline[53].actor == "spy"
    assert games[7].timeline[53].books == (None,)
    assert games[7].timeline[53].cast_name == (None,)
    assert games[7].timeline[53].category == TimelineCategory.BananaBread
    assert games[7].timeline[53].elapsed_time == 74.13
    assert games[7].timeline[53].event == "banana bread uttered."
    assert games[7].timeline[53].mission == Missions.Contact
    assert games[7].timeline[53].role == (None,)
    assert games[7].timeline[53].time == 135.8

    assert games[7].timeline[54].action_test == ActionTest.NoAT
    assert games[7].timeline[54].actor == "spy"
    assert games[7].timeline[54].books == (None,)
    assert games[7].timeline[54].cast_name == (Characters.Alice,)
    assert games[7].timeline[54].category == TimelineCategory.MissionComplete
    assert games[7].timeline[54].elapsed_time == 74.63
    assert games[7].timeline[54].event == "double agent contacted."
    assert games[7].timeline[54].mission == Missions.Contact
    assert games[7].timeline[54].role == (Roles.DoubleAgent,)
    assert games[7].timeline[54].time == 135.3

    assert games[7].timeline[55].action_test == ActionTest.NoAT
    assert games[7].timeline[55].actor == "sniper"
    assert games[7].timeline[55].books == (None,)
    assert games[7].timeline[55].cast_name == (Characters.Smallman,)
    assert games[7].timeline[55].category == TimelineCategory.SniperLights
    assert games[7].timeline[55].elapsed_time == 78.31
    assert games[7].timeline[55].event == "marked suspicious."
    assert games[7].timeline[55].mission == Missions.NoMission
    assert games[7].timeline[55].role == (Roles.Civilian,)
    assert games[7].timeline[55].time == 131.6

    assert games[7].timeline[56].action_test == ActionTest.NoAT
    assert games[7].timeline[56].actor == "sniper"
    assert games[7].timeline[56].books == (None,)
    assert games[7].timeline[56].cast_name == (Characters.Oprah,)
    assert games[7].timeline[56].category == TimelineCategory.SniperLights
    assert games[7].timeline[56].elapsed_time == 79.25
    assert games[7].timeline[56].event == "marked suspicious."
    assert games[7].timeline[56].mission == Missions.NoMission
    assert games[7].timeline[56].role == (Roles.Civilian,)
    assert games[7].timeline[56].time == 130.7

    assert games[7].timeline[57].action_test == ActionTest.NoAT
    assert games[7].timeline[57].actor == "sniper"
    assert games[7].timeline[57].books == (None,)
    assert games[7].timeline[57].cast_name == (Characters.Plain,)
    assert games[7].timeline[57].category == TimelineCategory.SniperLights
    assert games[7].timeline[57].elapsed_time == 80.31
    assert games[7].timeline[57].event == "marked suspicious."
    assert games[7].timeline[57].mission == Missions.NoMission
    assert games[7].timeline[57].role == (Roles.Civilian,)
    assert games[7].timeline[57].time == 129.6

    assert games[7].timeline[58].action_test == ActionTest.NoAT
    assert games[7].timeline[58].actor == "sniper"
    assert games[7].timeline[58].books == (None,)
    assert games[7].timeline[58].cast_name == (Characters.Bling,)
    assert games[7].timeline[58].category == TimelineCategory.SniperLights
    assert games[7].timeline[58].elapsed_time == 80.88
    assert games[7].timeline[58].event == "marked spy suspicious."
    assert games[7].timeline[58].mission == Missions.NoMission
    assert games[7].timeline[58].role == (Roles.Spy,)
    assert games[7].timeline[58].time == 129.1

    assert games[7].timeline[59].action_test == ActionTest.NoAT
    assert games[7].timeline[59].actor == "sniper"
    assert games[7].timeline[59].books == (None,)
    assert games[7].timeline[59].cast_name == (Characters.Sari,)
    assert games[7].timeline[59].category == TimelineCategory.SniperLights
    assert games[7].timeline[59].elapsed_time == 81.25
    assert games[7].timeline[59].event == "marked suspicious."
    assert games[7].timeline[59].mission == Missions.NoMission
    assert games[7].timeline[59].role == (Roles.SeductionTarget,)
    assert games[7].timeline[59].time == 128.7

    assert games[7].timeline[60].action_test == ActionTest.NoAT
    assert games[7].timeline[60].actor == "spy"
    assert games[7].timeline[60].books == (None,)
    assert games[7].timeline[60].cast_name == (None,)
    assert games[7].timeline[60].category == TimelineCategory.ActionTriggered
    assert games[7].timeline[60].elapsed_time == 84.94
    assert games[7].timeline[60].event == "action triggered: seduce target"
    assert games[7].timeline[60].mission == Missions.Seduce
    assert games[7].timeline[60].role == (None,)
    assert games[7].timeline[60].time == 125.0

    assert games[7].timeline[61].action_test == ActionTest.NoAT
    assert games[7].timeline[61].actor == "spy"
    assert games[7].timeline[61].books == (None,)
    assert games[7].timeline[61].cast_name == (Characters.Sari,)
    assert games[7].timeline[61].category == TimelineCategory.NoCategory
    assert games[7].timeline[61].elapsed_time == 84.94
    assert games[7].timeline[61].event == "begin flirtation with seduction target."
    assert games[7].timeline[61].mission == Missions.Seduce
    assert games[7].timeline[61].role == (Roles.SeductionTarget,)
    assert games[7].timeline[61].time == 125.0

    assert games[7].timeline[62].action_test == ActionTest.White
    assert games[7].timeline[62].actor == "spy"
    assert games[7].timeline[62].books == (None,)
    assert games[7].timeline[62].cast_name == (None,)
    assert games[7].timeline[62].category == TimelineCategory.ActionTest
    assert games[7].timeline[62].elapsed_time == 85.94
    assert games[7].timeline[62].event == "action test white: seduce target"
    assert games[7].timeline[62].mission == Missions.Seduce
    assert games[7].timeline[62].role == (None,)
    assert games[7].timeline[62].time == 124.0

    assert games[7].timeline[63].action_test == ActionTest.NoAT
    assert games[7].timeline[63].actor == "spy"
    assert games[7].timeline[63].books == (None,)
    assert games[7].timeline[63].cast_name == (Characters.Sari,)
    assert games[7].timeline[63].category == TimelineCategory.MissionPartial
    assert games[7].timeline[63].elapsed_time == 85.94
    assert games[7].timeline[63].event == "flirt with seduction target: 68%"
    assert games[7].timeline[63].mission == Missions.Seduce
    assert games[7].timeline[63].role == (Roles.SeductionTarget,)
    assert games[7].timeline[63].time == 124.0

    assert games[7].timeline[64].action_test == ActionTest.NoAT
    assert games[7].timeline[64].actor == "spy"
    assert games[7].timeline[64].books == (None,)
    assert games[7].timeline[64].cast_name == (None,)
    assert games[7].timeline[64].category == TimelineCategory.Conversation
    assert games[7].timeline[64].elapsed_time == 99.75
    assert games[7].timeline[64].event == "spy leaves conversation."
    assert games[7].timeline[64].mission == Missions.NoMission
    assert games[7].timeline[64].role == (None,)
    assert games[7].timeline[64].time == 110.2

    assert games[7].timeline[65].action_test == ActionTest.NoAT
    assert games[7].timeline[65].actor == "spy"
    assert games[7].timeline[65].books == (None,)
    assert games[7].timeline[65].cast_name == (Characters.Alice,)
    assert games[7].timeline[65].category == TimelineCategory.Conversation
    assert games[7].timeline[65].elapsed_time == 99.75
    assert games[7].timeline[65].event == "spy left conversation with double agent."
    assert games[7].timeline[65].mission == Missions.NoMission
    assert games[7].timeline[65].role == (Roles.DoubleAgent,)
    assert games[7].timeline[65].time == 110.2

    assert games[7].timeline[66].action_test == ActionTest.NoAT
    assert games[7].timeline[66].actor == "spy"
    assert games[7].timeline[66].books == (None,)
    assert games[7].timeline[66].cast_name == (None,)
    assert games[7].timeline[66].category == TimelineCategory.Statues
    assert games[7].timeline[66].elapsed_time == 107.25
    assert games[7].timeline[66].event == "picked up statue."
    assert games[7].timeline[66].mission == Missions.NoMission
    assert games[7].timeline[66].role == (None,)
    assert games[7].timeline[66].time == 102.7

    assert games[7].timeline[67].action_test == ActionTest.NoAT
    assert games[7].timeline[67].actor == "spy"
    assert games[7].timeline[67].books == (None,)
    assert games[7].timeline[67].cast_name == (None,)
    assert games[7].timeline[67].category == TimelineCategory.NoCategory
    assert games[7].timeline[67].elapsed_time == 107.25
    assert games[7].timeline[67].event == "flirtation cooldown expired."
    assert games[7].timeline[67].mission == Missions.Seduce
    assert games[7].timeline[67].role == (None,)
    assert games[7].timeline[67].time == 102.7

    assert games[7].timeline[68].action_test == ActionTest.NoAT
    assert games[7].timeline[68].actor == "spy"
    assert games[7].timeline[68].books == (None,)
    assert games[7].timeline[68].cast_name == (None,)
    assert games[7].timeline[68].category == TimelineCategory.Statues
    assert games[7].timeline[68].elapsed_time == 109.88
    assert games[7].timeline[68].event == "picked up fingerprintable statue."
    assert games[7].timeline[68].mission == Missions.Fingerprint
    assert games[7].timeline[68].role == (None,)
    assert games[7].timeline[68].time == 100.1

    assert games[7].timeline[69].action_test == ActionTest.NoAT
    assert games[7].timeline[69].actor == "spy"
    assert games[7].timeline[69].books == (None,)
    assert games[7].timeline[69].cast_name == (None,)
    assert games[7].timeline[69].category == TimelineCategory.ActionTriggered
    assert games[7].timeline[69].elapsed_time == 110.81
    assert games[7].timeline[69].event == "action triggered: fingerprint ambassador"
    assert games[7].timeline[69].mission == Missions.Fingerprint
    assert games[7].timeline[69].role == (None,)
    assert games[7].timeline[69].time == 99.1

    assert games[7].timeline[70].action_test == ActionTest.NoAT
    assert games[7].timeline[70].actor == "spy"
    assert games[7].timeline[70].books == (None,)
    assert games[7].timeline[70].cast_name == (None,)
    assert games[7].timeline[70].category == TimelineCategory.Statues
    assert games[7].timeline[70].elapsed_time == 110.81
    assert games[7].timeline[70].event == "started fingerprinting statue."
    assert games[7].timeline[70].mission == Missions.Fingerprint
    assert games[7].timeline[70].role == (None,)
    assert games[7].timeline[70].time == 99.1

    assert games[7].timeline[71].action_test == ActionTest.NoAT
    assert games[7].timeline[71].actor == "spy"
    assert games[7].timeline[71].books == (None,)
    assert games[7].timeline[71].cast_name == (None,)
    assert (
        games[7].timeline[71].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[7].timeline[71].elapsed_time == 111.81
    assert games[7].timeline[71].event == "fingerprinted statue."
    assert games[7].timeline[71].mission == Missions.Fingerprint
    assert games[7].timeline[71].role == (None,)
    assert games[7].timeline[71].time == 98.1

    assert games[7].timeline[72].action_test == ActionTest.NoAT
    assert games[7].timeline[72].actor == "spy"
    assert games[7].timeline[72].books == (None,)
    assert games[7].timeline[72].cast_name == (None,)
    assert games[7].timeline[72].category == TimelineCategory.MissionComplete
    assert games[7].timeline[72].elapsed_time == 111.81
    assert games[7].timeline[72].event == "fingerprinted ambassador."
    assert games[7].timeline[72].mission == Missions.Fingerprint
    assert games[7].timeline[72].role == (None,)
    assert games[7].timeline[72].time == 98.1

    assert games[7].timeline[73].action_test == ActionTest.NoAT
    assert games[7].timeline[73].actor == "spy"
    assert games[7].timeline[73].books == (None,)
    assert games[7].timeline[73].cast_name == (Characters.Salmon, Characters.Bling)
    assert games[7].timeline[73].category == TimelineCategory.NoCategory
    assert games[7].timeline[73].elapsed_time == 114.94
    assert games[7].timeline[73].event == "ambassador's personal space violated."
    assert games[7].timeline[73].mission == Missions.NoMission
    assert games[7].timeline[73].role == (Roles.Ambassador, Roles.Spy)
    assert games[7].timeline[73].time == 95.0

    assert games[7].timeline[74].action_test == ActionTest.NoAT
    assert games[7].timeline[74].actor == "spy"
    assert games[7].timeline[74].books == (None,)
    assert games[7].timeline[74].cast_name == (None,)
    assert games[7].timeline[74].category == TimelineCategory.Statues
    assert games[7].timeline[74].elapsed_time == 116.69
    assert games[7].timeline[74].event == "put back statue."
    assert games[7].timeline[74].mission == Missions.NoMission
    assert games[7].timeline[74].role == (None,)
    assert games[7].timeline[74].time == 93.3

    assert games[7].timeline[75].action_test == ActionTest.NoAT
    assert games[7].timeline[75].actor == "spy"
    assert games[7].timeline[75].books == (None,)
    assert games[7].timeline[75].cast_name == (None,)
    assert (
        games[7].timeline[75].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Watch
    )
    assert games[7].timeline[75].elapsed_time == 129.88
    assert games[7].timeline[75].event == "action triggered: check watch"
    assert games[7].timeline[75].mission == Missions.NoMission
    assert games[7].timeline[75].role == (None,)
    assert games[7].timeline[75].time == 80.1

    assert games[7].timeline[76].action_test == ActionTest.NoAT
    assert games[7].timeline[76].actor == "spy"
    assert games[7].timeline[76].books == (None,)
    assert games[7].timeline[76].cast_name == (Characters.Bling,)
    assert games[7].timeline[76].category == TimelineCategory.Watch
    assert games[7].timeline[76].elapsed_time == 129.88
    assert games[7].timeline[76].event == "watch checked."
    assert games[7].timeline[76].mission == Missions.NoMission
    assert games[7].timeline[76].role == (Roles.Spy,)
    assert games[7].timeline[76].time == 80.1

    assert games[7].timeline[77].action_test == ActionTest.NoAT
    assert games[7].timeline[77].actor == "spy"
    assert games[7].timeline[77].books == (None,)
    assert games[7].timeline[77].cast_name == (None,)
    assert games[7].timeline[77].category == TimelineCategory.Conversation
    assert games[7].timeline[77].elapsed_time == 139.44
    assert games[7].timeline[77].event == "spy enters conversation."
    assert games[7].timeline[77].mission == Missions.NoMission
    assert games[7].timeline[77].role == (None,)
    assert games[7].timeline[77].time == 70.5

    assert games[7].timeline[78].action_test == ActionTest.NoAT
    assert games[7].timeline[78].actor == "spy"
    assert games[7].timeline[78].books == (None,)
    assert games[7].timeline[78].cast_name == (None,)
    assert games[7].timeline[78].category == TimelineCategory.ActionTriggered
    assert games[7].timeline[78].elapsed_time == 145.38
    assert games[7].timeline[78].event == "action triggered: seduce target"
    assert games[7].timeline[78].mission == Missions.Seduce
    assert games[7].timeline[78].role == (None,)
    assert games[7].timeline[78].time == 64.6

    assert games[7].timeline[79].action_test == ActionTest.NoAT
    assert games[7].timeline[79].actor == "spy"
    assert games[7].timeline[79].books == (None,)
    assert games[7].timeline[79].cast_name == (Characters.Sari,)
    assert games[7].timeline[79].category == TimelineCategory.NoCategory
    assert games[7].timeline[79].elapsed_time == 145.38
    assert games[7].timeline[79].event == "begin flirtation with seduction target."
    assert games[7].timeline[79].mission == Missions.Seduce
    assert games[7].timeline[79].role == (Roles.SeductionTarget,)
    assert games[7].timeline[79].time == 64.6

    assert games[7].timeline[80].action_test == ActionTest.Green
    assert games[7].timeline[80].actor == "spy"
    assert games[7].timeline[80].books == (None,)
    assert games[7].timeline[80].cast_name == (None,)
    assert games[7].timeline[80].category == TimelineCategory.ActionTest
    assert games[7].timeline[80].elapsed_time == 146.5
    assert games[7].timeline[80].event == "action test green: seduce target"
    assert games[7].timeline[80].mission == Missions.Seduce
    assert games[7].timeline[80].role == (None,)
    assert games[7].timeline[80].time == 63.4

    assert games[7].timeline[81].action_test == ActionTest.NoAT
    assert games[7].timeline[81].actor == "spy"
    assert games[7].timeline[81].books == (None,)
    assert games[7].timeline[81].cast_name == (Characters.Sari,)
    assert games[7].timeline[81].category == TimelineCategory.MissionPartial
    assert games[7].timeline[81].elapsed_time == 146.5
    assert games[7].timeline[81].event == "flirt with seduction target: 100%"
    assert games[7].timeline[81].mission == Missions.Seduce
    assert games[7].timeline[81].role == (Roles.SeductionTarget,)
    assert games[7].timeline[81].time == 63.4

    assert games[7].timeline[82].action_test == ActionTest.NoAT
    assert games[7].timeline[82].actor == "spy"
    assert games[7].timeline[82].books == (None,)
    assert games[7].timeline[82].cast_name == (Characters.Sari,)
    assert games[7].timeline[82].category == TimelineCategory.MissionComplete
    assert games[7].timeline[82].elapsed_time == 146.5
    assert games[7].timeline[82].event == "target seduced."
    assert games[7].timeline[82].mission == Missions.Seduce
    assert games[7].timeline[82].role == (Roles.SeductionTarget,)
    assert games[7].timeline[82].time == 63.4

    assert games[7].timeline[83].action_test == ActionTest.NoAT
    assert games[7].timeline[83].actor == "game"
    assert games[7].timeline[83].books == (None,)
    assert games[7].timeline[83].cast_name == (None,)
    assert games[7].timeline[83].category == TimelineCategory.MissionCountdown
    assert games[7].timeline[83].elapsed_time == 146.5
    assert games[7].timeline[83].event == "missions completed. 10 second countdown."
    assert games[7].timeline[83].mission == Missions.NoMission
    assert games[7].timeline[83].role == (None,)
    assert games[7].timeline[83].time == 63.4

    assert games[7].timeline[84].action_test == ActionTest.NoAT
    assert games[7].timeline[84].actor == "game"
    assert games[7].timeline[84].books == (None,)
    assert games[7].timeline[84].cast_name == (None,)
    assert games[7].timeline[84].category == TimelineCategory.GameEnd
    assert games[7].timeline[84].elapsed_time == 156.5
    assert games[7].timeline[84].event == "missions completed successfully."
    assert games[7].timeline[84].mission == Missions.NoMission
    assert games[7].timeline[84].role == (None,)
    assert games[7].timeline[84].time == 53.5

    assert games[7].timeline.get_next_spy_action(games[7].timeline[84]) is None

    assert games[8].uuid == "as-RnR1RQruzhRDZr7JP9A"
    assert games[8].timeline[0].action_test == ActionTest.NoAT
    assert games[8].timeline[0].actor == "spy"
    assert games[8].timeline[0].books == (None,)
    assert games[8].timeline[0].cast_name == (Characters.Irish,)
    assert games[8].timeline[0].category == TimelineCategory.Cast
    assert games[8].timeline[0].elapsed_time == 0.0
    assert games[8].timeline[0].event == "spy cast."
    assert games[8].timeline[0].mission == Missions.NoMission
    assert games[8].timeline[0].role == (Roles.Spy,)
    assert games[8].timeline[0].time == 210.0

    assert games[8].timeline[1].action_test == ActionTest.NoAT
    assert games[8].timeline[1].actor == "spy"
    assert games[8].timeline[1].books == (None,)
    assert games[8].timeline[1].cast_name == (Characters.Carlos,)
    assert games[8].timeline[1].category == TimelineCategory.Cast
    assert games[8].timeline[1].elapsed_time == 0.0
    assert games[8].timeline[1].event == "ambassador cast."
    assert games[8].timeline[1].mission == Missions.NoMission
    assert games[8].timeline[1].role == (Roles.Ambassador,)
    assert games[8].timeline[1].time == 210.0

    assert games[8].timeline[2].action_test == ActionTest.NoAT
    assert games[8].timeline[2].actor == "spy"
    assert games[8].timeline[2].books == (None,)
    assert games[8].timeline[2].cast_name == (Characters.Salmon,)
    assert games[8].timeline[2].category == TimelineCategory.Cast
    assert games[8].timeline[2].elapsed_time == 0.0
    assert games[8].timeline[2].event == "double agent cast."
    assert games[8].timeline[2].mission == Missions.NoMission
    assert games[8].timeline[2].role == (Roles.DoubleAgent,)
    assert games[8].timeline[2].time == 210.0

    assert games[8].timeline[3].action_test == ActionTest.NoAT
    assert games[8].timeline[3].actor == "spy"
    assert games[8].timeline[3].books == (None,)
    assert games[8].timeline[3].cast_name == (Characters.Helen,)
    assert games[8].timeline[3].category == TimelineCategory.Cast
    assert games[8].timeline[3].elapsed_time == 0.0
    assert games[8].timeline[3].event == "suspected double agent cast."
    assert games[8].timeline[3].mission == Missions.NoMission
    assert games[8].timeline[3].role == (Roles.SuspectedDoubleAgent,)
    assert games[8].timeline[3].time == 210.0

    assert games[8].timeline[4].action_test == ActionTest.NoAT
    assert games[8].timeline[4].actor == "spy"
    assert games[8].timeline[4].books == (None,)
    assert games[8].timeline[4].cast_name == (Characters.General,)
    assert games[8].timeline[4].category == TimelineCategory.Cast
    assert games[8].timeline[4].elapsed_time == 0.0
    assert games[8].timeline[4].event == "seduction target cast."
    assert games[8].timeline[4].mission == Missions.NoMission
    assert games[8].timeline[4].role == (Roles.SeductionTarget,)
    assert games[8].timeline[4].time == 210.0

    assert games[8].timeline[5].action_test == ActionTest.NoAT
    assert games[8].timeline[5].actor == "spy"
    assert games[8].timeline[5].books == (None,)
    assert games[8].timeline[5].cast_name == (Characters.Plain,)
    assert games[8].timeline[5].category == TimelineCategory.Cast
    assert games[8].timeline[5].elapsed_time == 0.0
    assert games[8].timeline[5].event == "civilian cast."
    assert games[8].timeline[5].mission == Missions.NoMission
    assert games[8].timeline[5].role == (Roles.Civilian,)
    assert games[8].timeline[5].time == 210.0

    assert games[8].timeline[6].action_test == ActionTest.NoAT
    assert games[8].timeline[6].actor == "spy"
    assert games[8].timeline[6].books == (None,)
    assert games[8].timeline[6].cast_name == (Characters.Sikh,)
    assert games[8].timeline[6].category == TimelineCategory.Cast
    assert games[8].timeline[6].elapsed_time == 0.0
    assert games[8].timeline[6].event == "civilian cast."
    assert games[8].timeline[6].mission == Missions.NoMission
    assert games[8].timeline[6].role == (Roles.Civilian,)
    assert games[8].timeline[6].time == 210.0

    assert games[8].timeline[7].action_test == ActionTest.NoAT
    assert games[8].timeline[7].actor == "spy"
    assert games[8].timeline[7].books == (None,)
    assert games[8].timeline[7].cast_name == (Characters.Alice,)
    assert games[8].timeline[7].category == TimelineCategory.Cast
    assert games[8].timeline[7].elapsed_time == 0.0
    assert games[8].timeline[7].event == "civilian cast."
    assert games[8].timeline[7].mission == Missions.NoMission
    assert games[8].timeline[7].role == (Roles.Civilian,)
    assert games[8].timeline[7].time == 210.0

    assert games[8].timeline[8].action_test == ActionTest.NoAT
    assert games[8].timeline[8].actor == "spy"
    assert games[8].timeline[8].books == (None,)
    assert games[8].timeline[8].cast_name == (Characters.Morgan,)
    assert games[8].timeline[8].category == TimelineCategory.Cast
    assert games[8].timeline[8].elapsed_time == 0.0
    assert games[8].timeline[8].event == "civilian cast."
    assert games[8].timeline[8].mission == Missions.NoMission
    assert games[8].timeline[8].role == (Roles.Civilian,)
    assert games[8].timeline[8].time == 210.0

    assert games[8].timeline[9].action_test == ActionTest.NoAT
    assert games[8].timeline[9].actor == "spy"
    assert games[8].timeline[9].books == (None,)
    assert games[8].timeline[9].cast_name == (Characters.Teal,)
    assert games[8].timeline[9].category == TimelineCategory.Cast
    assert games[8].timeline[9].elapsed_time == 0.0
    assert games[8].timeline[9].event == "civilian cast."
    assert games[8].timeline[9].mission == Missions.NoMission
    assert games[8].timeline[9].role == (Roles.Civilian,)
    assert games[8].timeline[9].time == 210.0

    assert games[8].timeline[10].action_test == ActionTest.NoAT
    assert games[8].timeline[10].actor == "spy"
    assert games[8].timeline[10].books == (None,)
    assert games[8].timeline[10].cast_name == (Characters.Smallman,)
    assert games[8].timeline[10].category == TimelineCategory.Cast
    assert games[8].timeline[10].elapsed_time == 0.0
    assert games[8].timeline[10].event == "civilian cast."
    assert games[8].timeline[10].mission == Missions.NoMission
    assert games[8].timeline[10].role == (Roles.Civilian,)
    assert games[8].timeline[10].time == 210.0

    assert games[8].timeline[11].action_test == ActionTest.NoAT
    assert games[8].timeline[11].actor == "spy"
    assert games[8].timeline[11].books == (None,)
    assert games[8].timeline[11].cast_name == (Characters.Bling,)
    assert games[8].timeline[11].category == TimelineCategory.Cast
    assert games[8].timeline[11].elapsed_time == 0.0
    assert games[8].timeline[11].event == "civilian cast."
    assert games[8].timeline[11].mission == Missions.NoMission
    assert games[8].timeline[11].role == (Roles.Civilian,)
    assert games[8].timeline[11].time == 210.0

    assert games[8].timeline[12].action_test == ActionTest.NoAT
    assert games[8].timeline[12].actor == "spy"
    assert games[8].timeline[12].books == (None,)
    assert games[8].timeline[12].cast_name == (Characters.Wheels,)
    assert games[8].timeline[12].category == TimelineCategory.Cast
    assert games[8].timeline[12].elapsed_time == 0.0
    assert games[8].timeline[12].event == "civilian cast."
    assert games[8].timeline[12].mission == Missions.NoMission
    assert games[8].timeline[12].role == (Roles.Civilian,)
    assert games[8].timeline[12].time == 210.0

    assert games[8].timeline[13].action_test == ActionTest.NoAT
    assert games[8].timeline[13].actor == "spy"
    assert games[8].timeline[13].books == (None,)
    assert games[8].timeline[13].cast_name == (Characters.Sari,)
    assert games[8].timeline[13].category == TimelineCategory.Cast
    assert games[8].timeline[13].elapsed_time == 0.0
    assert games[8].timeline[13].event == "civilian cast."
    assert games[8].timeline[13].mission == Missions.NoMission
    assert games[8].timeline[13].role == (Roles.Civilian,)
    assert games[8].timeline[13].time == 210.0

    assert games[8].timeline[14].action_test == ActionTest.NoAT
    assert games[8].timeline[14].actor == "spy"
    assert games[8].timeline[14].books == (None,)
    assert games[8].timeline[14].cast_name == (Characters.Taft,)
    assert games[8].timeline[14].category == TimelineCategory.Cast
    assert games[8].timeline[14].elapsed_time == 0.0
    assert games[8].timeline[14].event == "civilian cast."
    assert games[8].timeline[14].mission == Missions.NoMission
    assert games[8].timeline[14].role == (Roles.Civilian,)
    assert games[8].timeline[14].time == 210.0

    assert games[8].timeline[15].action_test == ActionTest.NoAT
    assert games[8].timeline[15].actor == "spy"
    assert games[8].timeline[15].books == (None,)
    assert games[8].timeline[15].cast_name == (None,)
    assert games[8].timeline[15].category == TimelineCategory.MissionSelected
    assert games[8].timeline[15].elapsed_time == 0.0
    assert games[8].timeline[15].event == "bug ambassador selected."
    assert games[8].timeline[15].mission == Missions.Bug
    assert games[8].timeline[15].role == (None,)
    assert games[8].timeline[15].time == 210.0

    assert games[8].timeline[16].action_test == ActionTest.NoAT
    assert games[8].timeline[16].actor == "spy"
    assert games[8].timeline[16].books == (None,)
    assert games[8].timeline[16].cast_name == (None,)
    assert games[8].timeline[16].category == TimelineCategory.MissionSelected
    assert games[8].timeline[16].elapsed_time == 0.0
    assert games[8].timeline[16].event == "contact double agent selected."
    assert games[8].timeline[16].mission == Missions.Contact
    assert games[8].timeline[16].role == (None,)
    assert games[8].timeline[16].time == 210.0

    assert games[8].timeline[17].action_test == ActionTest.NoAT
    assert games[8].timeline[17].actor == "spy"
    assert games[8].timeline[17].books == (None,)
    assert games[8].timeline[17].cast_name == (None,)
    assert games[8].timeline[17].category == TimelineCategory.MissionSelected
    assert games[8].timeline[17].elapsed_time == 0.0
    assert games[8].timeline[17].event == "transfer microfilm selected."
    assert games[8].timeline[17].mission == Missions.Transfer
    assert games[8].timeline[17].role == (None,)
    assert games[8].timeline[17].time == 210.0

    assert games[8].timeline[18].action_test == ActionTest.NoAT
    assert games[8].timeline[18].actor == "spy"
    assert games[8].timeline[18].books == (None,)
    assert games[8].timeline[18].cast_name == (None,)
    assert games[8].timeline[18].category == TimelineCategory.MissionSelected
    assert games[8].timeline[18].elapsed_time == 0.0
    assert games[8].timeline[18].event == "swap statue selected."
    assert games[8].timeline[18].mission == Missions.Swap
    assert games[8].timeline[18].role == (None,)
    assert games[8].timeline[18].time == 210.0

    assert games[8].timeline[19].action_test == ActionTest.NoAT
    assert games[8].timeline[19].actor == "spy"
    assert games[8].timeline[19].books == (None,)
    assert games[8].timeline[19].cast_name == (None,)
    assert games[8].timeline[19].category == TimelineCategory.MissionSelected
    assert games[8].timeline[19].elapsed_time == 0.0
    assert games[8].timeline[19].event == "inspect 3 statues selected."
    assert games[8].timeline[19].mission == Missions.Inspect
    assert games[8].timeline[19].role == (None,)
    assert games[8].timeline[19].time == 210.0

    assert games[8].timeline[20].action_test == ActionTest.NoAT
    assert games[8].timeline[20].actor == "spy"
    assert games[8].timeline[20].books == (None,)
    assert games[8].timeline[20].cast_name == (None,)
    assert games[8].timeline[20].category == TimelineCategory.MissionSelected
    assert games[8].timeline[20].elapsed_time == 0.0
    assert games[8].timeline[20].event == "seduce target selected."
    assert games[8].timeline[20].mission == Missions.Seduce
    assert games[8].timeline[20].role == (None,)
    assert games[8].timeline[20].time == 210.0

    assert games[8].timeline[21].action_test == ActionTest.NoAT
    assert games[8].timeline[21].actor == "spy"
    assert games[8].timeline[21].books == (None,)
    assert games[8].timeline[21].cast_name == (None,)
    assert games[8].timeline[21].category == TimelineCategory.MissionSelected
    assert games[8].timeline[21].elapsed_time == 0.0
    assert games[8].timeline[21].event == "purloin guest list selected."
    assert games[8].timeline[21].mission == Missions.Purloin
    assert games[8].timeline[21].role == (None,)
    assert games[8].timeline[21].time == 210.0

    assert games[8].timeline[22].action_test == ActionTest.NoAT
    assert games[8].timeline[22].actor == "spy"
    assert games[8].timeline[22].books == (None,)
    assert games[8].timeline[22].cast_name == (None,)
    assert games[8].timeline[22].category == TimelineCategory.MissionSelected
    assert games[8].timeline[22].elapsed_time == 0.0
    assert games[8].timeline[22].event == "fingerprint ambassador selected."
    assert games[8].timeline[22].mission == Missions.Fingerprint
    assert games[8].timeline[22].role == (None,)
    assert games[8].timeline[22].time == 210.0

    assert games[8].timeline[23].action_test == ActionTest.NoAT
    assert games[8].timeline[23].actor == "spy"
    assert games[8].timeline[23].books == (None,)
    assert games[8].timeline[23].cast_name == (None,)
    assert games[8].timeline[23].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[23].elapsed_time == 0.0
    assert games[8].timeline[23].event == "bug ambassador enabled."
    assert games[8].timeline[23].mission == Missions.Bug
    assert games[8].timeline[23].role == (None,)
    assert games[8].timeline[23].time == 210.0

    assert games[8].timeline[24].action_test == ActionTest.NoAT
    assert games[8].timeline[24].actor == "spy"
    assert games[8].timeline[24].books == (None,)
    assert games[8].timeline[24].cast_name == (None,)
    assert games[8].timeline[24].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[24].elapsed_time == 0.0
    assert games[8].timeline[24].event == "contact double agent enabled."
    assert games[8].timeline[24].mission == Missions.Contact
    assert games[8].timeline[24].role == (None,)
    assert games[8].timeline[24].time == 210.0

    assert games[8].timeline[25].action_test == ActionTest.NoAT
    assert games[8].timeline[25].actor == "spy"
    assert games[8].timeline[25].books == (None,)
    assert games[8].timeline[25].cast_name == (None,)
    assert games[8].timeline[25].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[25].elapsed_time == 0.0
    assert games[8].timeline[25].event == "transfer microfilm enabled."
    assert games[8].timeline[25].mission == Missions.Transfer
    assert games[8].timeline[25].role == (None,)
    assert games[8].timeline[25].time == 210.0

    assert games[8].timeline[26].action_test == ActionTest.NoAT
    assert games[8].timeline[26].actor == "spy"
    assert games[8].timeline[26].books == (None,)
    assert games[8].timeline[26].cast_name == (None,)
    assert games[8].timeline[26].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[26].elapsed_time == 0.0
    assert games[8].timeline[26].event == "swap statue enabled."
    assert games[8].timeline[26].mission == Missions.Swap
    assert games[8].timeline[26].role == (None,)
    assert games[8].timeline[26].time == 210.0

    assert games[8].timeline[27].action_test == ActionTest.NoAT
    assert games[8].timeline[27].actor == "spy"
    assert games[8].timeline[27].books == (None,)
    assert games[8].timeline[27].cast_name == (None,)
    assert games[8].timeline[27].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[27].elapsed_time == 0.0
    assert games[8].timeline[27].event == "inspect 3 statues enabled."
    assert games[8].timeline[27].mission == Missions.Inspect
    assert games[8].timeline[27].role == (None,)
    assert games[8].timeline[27].time == 210.0

    assert games[8].timeline[28].action_test == ActionTest.NoAT
    assert games[8].timeline[28].actor == "spy"
    assert games[8].timeline[28].books == (None,)
    assert games[8].timeline[28].cast_name == (None,)
    assert games[8].timeline[28].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[28].elapsed_time == 0.0
    assert games[8].timeline[28].event == "seduce target enabled."
    assert games[8].timeline[28].mission == Missions.Seduce
    assert games[8].timeline[28].role == (None,)
    assert games[8].timeline[28].time == 210.0

    assert games[8].timeline[29].action_test == ActionTest.NoAT
    assert games[8].timeline[29].actor == "spy"
    assert games[8].timeline[29].books == (None,)
    assert games[8].timeline[29].cast_name == (None,)
    assert games[8].timeline[29].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[29].elapsed_time == 0.0
    assert games[8].timeline[29].event == "purloin guest list enabled."
    assert games[8].timeline[29].mission == Missions.Purloin
    assert games[8].timeline[29].role == (None,)
    assert games[8].timeline[29].time == 210.0

    assert games[8].timeline[30].action_test == ActionTest.NoAT
    assert games[8].timeline[30].actor == "spy"
    assert games[8].timeline[30].books == (None,)
    assert games[8].timeline[30].cast_name == (None,)
    assert games[8].timeline[30].category == TimelineCategory.MissionEnabled
    assert games[8].timeline[30].elapsed_time == 0.0
    assert games[8].timeline[30].event == "fingerprint ambassador enabled."
    assert games[8].timeline[30].mission == Missions.Fingerprint
    assert games[8].timeline[30].role == (None,)
    assert games[8].timeline[30].time == 210.0

    assert games[8].timeline[31].action_test == ActionTest.NoAT
    assert games[8].timeline[31].actor == "game"
    assert games[8].timeline[31].books == (None,)
    assert games[8].timeline[31].cast_name == (None,)
    assert games[8].timeline[31].category == TimelineCategory.GameStart
    assert games[8].timeline[31].elapsed_time == 0.0
    assert games[8].timeline[31].event == "game started."
    assert games[8].timeline[31].mission == Missions.NoMission
    assert games[8].timeline[31].role == (None,)
    assert games[8].timeline[31].time == 210.0

    assert games[8].timeline[32].action_test == ActionTest.NoAT
    assert games[8].timeline[32].actor == "spy"
    assert games[8].timeline[32].books == (None,)
    assert games[8].timeline[32].cast_name == (None,)
    assert games[8].timeline[32].category == TimelineCategory.NoCategory
    assert games[8].timeline[32].elapsed_time == 1.06
    assert games[8].timeline[32].event == "spy player takes control from ai."
    assert games[8].timeline[32].mission == Missions.NoMission
    assert games[8].timeline[32].role == (None,)
    assert games[8].timeline[32].time == 208.9

    assert games[8].timeline[33].action_test == ActionTest.NoAT
    assert games[8].timeline[33].actor == "sniper"
    assert games[8].timeline[33].books == (None,)
    assert games[8].timeline[33].cast_name == (Characters.Carlos,)
    assert games[8].timeline[33].category == TimelineCategory.SniperLights
    assert games[8].timeline[33].elapsed_time == 3.69
    assert games[8].timeline[33].event == "marked suspicious."
    assert games[8].timeline[33].mission == Missions.NoMission
    assert games[8].timeline[33].role == (Roles.Ambassador,)
    assert games[8].timeline[33].time == 206.3

    assert games[8].timeline[34].action_test == ActionTest.NoAT
    assert games[8].timeline[34].actor == "sniper"
    assert games[8].timeline[34].books == (None,)
    assert games[8].timeline[34].cast_name == (Characters.Salmon,)
    assert games[8].timeline[34].category == TimelineCategory.SniperLights
    assert games[8].timeline[34].elapsed_time == 4.25
    assert games[8].timeline[34].event == "marked less suspicious."
    assert games[8].timeline[34].mission == Missions.NoMission
    assert games[8].timeline[34].role == (Roles.DoubleAgent,)
    assert games[8].timeline[34].time == 205.7

    assert games[8].timeline[35].action_test == ActionTest.NoAT
    assert games[8].timeline[35].actor == "spy"
    assert games[8].timeline[35].books == (None,)
    assert games[8].timeline[35].cast_name == (None,)
    assert games[8].timeline[35].category == TimelineCategory.ActionTriggered
    assert games[8].timeline[35].elapsed_time == 6.81
    assert games[8].timeline[35].event == "action triggered: seduce target"
    assert games[8].timeline[35].mission == Missions.Seduce
    assert games[8].timeline[35].role == (None,)
    assert games[8].timeline[35].time == 203.1

    assert games[8].timeline[36].action_test == ActionTest.NoAT
    assert games[8].timeline[36].actor == "spy"
    assert games[8].timeline[36].books == (None,)
    assert games[8].timeline[36].cast_name == (Characters.General,)
    assert games[8].timeline[36].category == TimelineCategory.NoCategory
    assert games[8].timeline[36].elapsed_time == 6.81
    assert games[8].timeline[36].event == "begin flirtation with seduction target."
    assert games[8].timeline[36].mission == Missions.Seduce
    assert games[8].timeline[36].role == (Roles.SeductionTarget,)
    assert games[8].timeline[36].time == 203.1

    assert games[8].timeline[37].action_test == ActionTest.NoAT
    assert games[8].timeline[37].actor == "sniper"
    assert games[8].timeline[37].books == (None,)
    assert games[8].timeline[37].cast_name == (Characters.Helen,)
    assert games[8].timeline[37].category == TimelineCategory.SniperLights
    assert games[8].timeline[37].elapsed_time == 7.5
    assert games[8].timeline[37].event == "marked less suspicious."
    assert games[8].timeline[37].mission == Missions.NoMission
    assert games[8].timeline[37].role == (Roles.SuspectedDoubleAgent,)
    assert games[8].timeline[37].time == 202.5

    assert games[8].timeline[38].action_test == ActionTest.Green
    assert games[8].timeline[38].actor == "spy"
    assert games[8].timeline[38].books == (None,)
    assert games[8].timeline[38].cast_name == (None,)
    assert games[8].timeline[38].category == TimelineCategory.ActionTest
    assert games[8].timeline[38].elapsed_time == 7.69
    assert games[8].timeline[38].event == "action test green: seduce target"
    assert games[8].timeline[38].mission == Missions.Seduce
    assert games[8].timeline[38].role == (None,)
    assert games[8].timeline[38].time == 202.3

    assert games[8].timeline[39].action_test == ActionTest.NoAT
    assert games[8].timeline[39].actor == "sniper"
    assert games[8].timeline[39].books == (None,)
    assert games[8].timeline[39].cast_name == (Characters.Damon,)
    assert games[8].timeline[39].category == TimelineCategory.SniperLights
    assert games[8].timeline[39].elapsed_time == 8.88
    assert games[8].timeline[39].event == "marked less suspicious."
    assert games[8].timeline[39].mission == Missions.NoMission
    assert games[8].timeline[39].role == (Roles.Staff,)
    assert games[8].timeline[39].time == 201.1

    assert games[8].timeline[40].action_test == ActionTest.NoAT
    assert games[8].timeline[40].actor == "spy"
    assert games[8].timeline[40].books == (None,)
    assert games[8].timeline[40].cast_name == (Characters.General,)
    assert games[8].timeline[40].category == TimelineCategory.MissionPartial
    assert games[8].timeline[40].elapsed_time == 9.31
    assert games[8].timeline[40].event == "flirt with seduction target: 51%"
    assert games[8].timeline[40].mission == Missions.Seduce
    assert games[8].timeline[40].role == (Roles.SeductionTarget,)
    assert games[8].timeline[40].time == 200.6

    assert games[8].timeline[41].action_test == ActionTest.NoAT
    assert games[8].timeline[41].actor == "sniper"
    assert games[8].timeline[41].books == (None,)
    assert games[8].timeline[41].cast_name == (Characters.Toby,)
    assert games[8].timeline[41].category == TimelineCategory.SniperLights
    assert games[8].timeline[41].elapsed_time == 10.06
    assert games[8].timeline[41].event == "marked suspicious."
    assert games[8].timeline[41].mission == Missions.NoMission
    assert games[8].timeline[41].role == (Roles.Staff,)
    assert games[8].timeline[41].time == 199.9

    assert games[8].timeline[42].action_test == ActionTest.NoAT
    assert games[8].timeline[42].actor == "sniper"
    assert games[8].timeline[42].books == (None,)
    assert games[8].timeline[42].cast_name == (Characters.Bling,)
    assert games[8].timeline[42].category == TimelineCategory.SniperLights
    assert games[8].timeline[42].elapsed_time == 11.0
    assert games[8].timeline[42].event == "marked suspicious."
    assert games[8].timeline[42].mission == Missions.NoMission
    assert games[8].timeline[42].role == (Roles.Civilian,)
    assert games[8].timeline[42].time == 198.9

    assert games[8].timeline[43].action_test == ActionTest.NoAT
    assert games[8].timeline[43].actor == "sniper"
    assert games[8].timeline[43].books == (None,)
    assert games[8].timeline[43].cast_name == (Characters.Sari,)
    assert games[8].timeline[43].category == TimelineCategory.SniperLights
    assert games[8].timeline[43].elapsed_time == 11.5
    assert games[8].timeline[43].event == "marked suspicious."
    assert games[8].timeline[43].mission == Missions.NoMission
    assert games[8].timeline[43].role == (Roles.Civilian,)
    assert games[8].timeline[43].time == 198.5

    assert games[8].timeline[44].action_test == ActionTest.NoAT
    assert games[8].timeline[44].actor == "spy"
    assert games[8].timeline[44].books == (None,)
    assert games[8].timeline[44].cast_name == (Characters.Irish,)
    assert games[8].timeline[44].category == TimelineCategory.Drinks
    assert games[8].timeline[44].elapsed_time == 11.88
    assert games[8].timeline[44].event == "took last sip of drink."
    assert games[8].timeline[44].mission == Missions.NoMission
    assert games[8].timeline[44].role == (Roles.Spy,)
    assert games[8].timeline[44].time == 198.1

    assert games[8].timeline[45].action_test == ActionTest.NoAT
    assert games[8].timeline[45].actor == "sniper"
    assert games[8].timeline[45].books == (None,)
    assert games[8].timeline[45].cast_name == (Characters.Wheels,)
    assert games[8].timeline[45].category == TimelineCategory.SniperLights
    assert games[8].timeline[45].elapsed_time == 14.0
    assert games[8].timeline[45].event == "marked suspicious."
    assert games[8].timeline[45].mission == Missions.NoMission
    assert games[8].timeline[45].role == (Roles.Civilian,)
    assert games[8].timeline[45].time == 195.9

    assert games[8].timeline[46].action_test == ActionTest.NoAT
    assert games[8].timeline[46].actor == "spy"
    assert games[8].timeline[46].books == (None,)
    assert games[8].timeline[46].cast_name == (None,)
    assert games[8].timeline[46].category == TimelineCategory.NoCategory
    assert games[8].timeline[46].elapsed_time == 20.06
    assert games[8].timeline[46].event == "flirtation cooldown expired."
    assert games[8].timeline[46].mission == Missions.Seduce
    assert games[8].timeline[46].role == (None,)
    assert games[8].timeline[46].time == 189.9

    assert games[8].timeline[47].action_test == ActionTest.NoAT
    assert games[8].timeline[47].actor == "spy"
    assert games[8].timeline[47].books == (None,)
    assert games[8].timeline[47].cast_name == (Characters.Irish,)
    assert games[8].timeline[47].category == TimelineCategory.Drinks
    assert games[8].timeline[47].elapsed_time == 28.63
    assert games[8].timeline[47].event == "waiter offered drink."
    assert games[8].timeline[47].mission == Missions.NoMission
    assert games[8].timeline[47].role == (Roles.Spy,)
    assert games[8].timeline[47].time == 181.3

    assert games[8].timeline[48].action_test == ActionTest.NoAT
    assert games[8].timeline[48].actor == "sniper"
    assert games[8].timeline[48].books == (Books.Green,)
    assert games[8].timeline[48].cast_name == (Characters.Taft,)
    assert (
        games[8].timeline[48].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[8].timeline[48].elapsed_time == 31.06
    assert games[8].timeline[48].event == "marked book."
    assert games[8].timeline[48].mission == Missions.NoMission
    assert games[8].timeline[48].role == (Roles.Civilian,)
    assert games[8].timeline[48].time == 178.9

    assert games[8].timeline[49].action_test == ActionTest.NoAT
    assert games[8].timeline[49].actor == "spy"
    assert games[8].timeline[49].books == (None,)
    assert games[8].timeline[49].cast_name == (Characters.Irish,)
    assert games[8].timeline[49].category == TimelineCategory.Drinks
    assert games[8].timeline[49].elapsed_time == 31.69
    assert games[8].timeline[49].event == "rejected drink from waiter."
    assert games[8].timeline[49].mission == Missions.NoMission
    assert games[8].timeline[49].role == (Roles.Spy,)
    assert games[8].timeline[49].time == 178.3

    assert games[8].timeline[50].action_test == ActionTest.NoAT
    assert games[8].timeline[50].actor == "spy"
    assert games[8].timeline[50].books == (None,)
    assert games[8].timeline[50].cast_name == (Characters.Irish,)
    assert games[8].timeline[50].category == TimelineCategory.Drinks
    assert games[8].timeline[50].elapsed_time == 31.69
    assert games[8].timeline[50].event == "waiter stopped offering drink."
    assert games[8].timeline[50].mission == Missions.NoMission
    assert games[8].timeline[50].role == (Roles.Spy,)
    assert games[8].timeline[50].time == 178.3

    assert games[8].timeline[51].action_test == ActionTest.NoAT
    assert games[8].timeline[51].actor == "sniper"
    assert games[8].timeline[51].books == (None,)
    assert games[8].timeline[51].cast_name == (Characters.Teal,)
    assert games[8].timeline[51].category == TimelineCategory.SniperLights
    assert games[8].timeline[51].elapsed_time == 35.38
    assert games[8].timeline[51].event == "marked suspicious."
    assert games[8].timeline[51].mission == Missions.NoMission
    assert games[8].timeline[51].role == (Roles.Civilian,)
    assert games[8].timeline[51].time == 174.6

    assert games[8].timeline[52].action_test == ActionTest.NoAT
    assert games[8].timeline[52].actor == "sniper"
    assert games[8].timeline[52].books == (None,)
    assert games[8].timeline[52].cast_name == (Characters.Teal,)
    assert games[8].timeline[52].category == TimelineCategory.SniperLights
    assert games[8].timeline[52].elapsed_time == 36.13
    assert games[8].timeline[52].event == "marked neutral suspicion."
    assert games[8].timeline[52].mission == Missions.NoMission
    assert games[8].timeline[52].role == (Roles.Civilian,)
    assert games[8].timeline[52].time == 173.8

    assert games[8].timeline[53].action_test == ActionTest.NoAT
    assert games[8].timeline[53].actor == "sniper"
    assert games[8].timeline[53].books == (Books.Blue,)
    assert games[8].timeline[53].cast_name == (Characters.Teal,)
    assert (
        games[8].timeline[53].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[8].timeline[53].elapsed_time == 37.13
    assert games[8].timeline[53].event == "marked book."
    assert games[8].timeline[53].mission == Missions.NoMission
    assert games[8].timeline[53].role == (Roles.Civilian,)
    assert games[8].timeline[53].time == 172.8

    assert games[8].timeline[54].action_test == ActionTest.NoAT
    assert games[8].timeline[54].actor == "spy"
    assert games[8].timeline[54].books == (None,)
    assert games[8].timeline[54].cast_name == (None,)
    assert games[8].timeline[54].category == TimelineCategory.Conversation
    assert games[8].timeline[54].elapsed_time == 39.75
    assert games[8].timeline[54].event == "spy enters conversation."
    assert games[8].timeline[54].mission == Missions.NoMission
    assert games[8].timeline[54].role == (None,)
    assert games[8].timeline[54].time == 170.2

    assert games[8].timeline[55].action_test == ActionTest.NoAT
    assert games[8].timeline[55].actor == "spy"
    assert games[8].timeline[55].books == (None,)
    assert games[8].timeline[55].cast_name == (None,)
    assert games[8].timeline[55].category == TimelineCategory.ActionTriggered
    assert games[8].timeline[55].elapsed_time == 43.31
    assert games[8].timeline[55].event == "action triggered: seduce target"
    assert games[8].timeline[55].mission == Missions.Seduce
    assert games[8].timeline[55].role == (None,)
    assert games[8].timeline[55].time == 166.6

    assert games[8].timeline[56].action_test == ActionTest.NoAT
    assert games[8].timeline[56].actor == "spy"
    assert games[8].timeline[56].books == (None,)
    assert games[8].timeline[56].cast_name == (Characters.General,)
    assert games[8].timeline[56].category == TimelineCategory.NoCategory
    assert games[8].timeline[56].elapsed_time == 43.31
    assert games[8].timeline[56].event == "begin flirtation with seduction target."
    assert games[8].timeline[56].mission == Missions.Seduce
    assert games[8].timeline[56].role == (Roles.SeductionTarget,)
    assert games[8].timeline[56].time == 166.6

    assert games[8].timeline[57].action_test == ActionTest.White
    assert games[8].timeline[57].actor == "spy"
    assert games[8].timeline[57].books == (None,)
    assert games[8].timeline[57].cast_name == (None,)
    assert games[8].timeline[57].category == TimelineCategory.ActionTest
    assert games[8].timeline[57].elapsed_time == 44.63
    assert games[8].timeline[57].event == "action test white: seduce target"
    assert games[8].timeline[57].mission == Missions.Seduce
    assert games[8].timeline[57].role == (None,)
    assert games[8].timeline[57].time == 165.3

    assert games[8].timeline[58].action_test == ActionTest.NoAT
    assert games[8].timeline[58].actor == "spy"
    assert games[8].timeline[58].books == (None,)
    assert games[8].timeline[58].cast_name == (Characters.General,)
    assert games[8].timeline[58].category == TimelineCategory.MissionPartial
    assert games[8].timeline[58].elapsed_time == 44.63
    assert games[8].timeline[58].event == "flirt with seduction target: 85%"
    assert games[8].timeline[58].mission == Missions.Seduce
    assert games[8].timeline[58].role == (Roles.SeductionTarget,)
    assert games[8].timeline[58].time == 165.3

    assert games[8].timeline[59].action_test == ActionTest.NoAT
    assert games[8].timeline[59].actor == "sniper"
    assert games[8].timeline[59].books == (None,)
    assert games[8].timeline[59].cast_name == (Characters.Morgan,)
    assert games[8].timeline[59].category == TimelineCategory.SniperLights
    assert games[8].timeline[59].elapsed_time == 47.94
    assert games[8].timeline[59].event == "marked suspicious."
    assert games[8].timeline[59].mission == Missions.NoMission
    assert games[8].timeline[59].role == (Roles.Civilian,)
    assert games[8].timeline[59].time == 162.0

    assert games[8].timeline[60].action_test == ActionTest.NoAT
    assert games[8].timeline[60].actor == "spy"
    assert games[8].timeline[60].books == (None,)
    assert games[8].timeline[60].cast_name == (None,)
    assert games[8].timeline[60].category == TimelineCategory.Conversation
    assert games[8].timeline[60].elapsed_time == 54.25
    assert games[8].timeline[60].event == "spy leaves conversation."
    assert games[8].timeline[60].mission == Missions.NoMission
    assert games[8].timeline[60].role == (None,)
    assert games[8].timeline[60].time == 155.7

    assert games[8].timeline[61].action_test == ActionTest.NoAT
    assert games[8].timeline[61].actor == "spy"
    assert games[8].timeline[61].books == (None,)
    assert games[8].timeline[61].cast_name == (Characters.Irish,)
    assert games[8].timeline[61].category == TimelineCategory.Drinks
    assert games[8].timeline[61].elapsed_time == 60.31
    assert games[8].timeline[61].event == "request drink from waiter."
    assert games[8].timeline[61].mission == Missions.NoMission
    assert games[8].timeline[61].role == (Roles.Spy,)
    assert games[8].timeline[61].time == 149.6

    assert games[8].timeline[62].action_test == ActionTest.NoAT
    assert games[8].timeline[62].actor == "sniper"
    assert games[8].timeline[62].books == (Books.Green,)
    assert games[8].timeline[62].cast_name == (Characters.Sikh,)
    assert (
        games[8].timeline[62].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[8].timeline[62].elapsed_time == 61.13
    assert games[8].timeline[62].event == "marked book."
    assert games[8].timeline[62].mission == Missions.NoMission
    assert games[8].timeline[62].role == (Roles.Civilian,)
    assert games[8].timeline[62].time == 148.8

    assert games[8].timeline[63].action_test == ActionTest.NoAT
    assert games[8].timeline[63].actor == "spy"
    assert games[8].timeline[63].books == (None,)
    assert games[8].timeline[63].cast_name == (None,)
    assert games[8].timeline[63].category == TimelineCategory.NoCategory
    assert games[8].timeline[63].elapsed_time == 62.13
    assert games[8].timeline[63].event == "flirtation cooldown expired."
    assert games[8].timeline[63].mission == Missions.Seduce
    assert games[8].timeline[63].role == (None,)
    assert games[8].timeline[63].time == 147.8

    assert games[8].timeline[64].action_test == ActionTest.NoAT
    assert games[8].timeline[64].actor == "spy"
    assert games[8].timeline[64].books == (Books.Blue,)
    assert games[8].timeline[64].cast_name == (None,)
    assert games[8].timeline[64].category == TimelineCategory.Books
    assert games[8].timeline[64].elapsed_time == 65.38
    assert games[8].timeline[64].event == "get book from bookcase."
    assert games[8].timeline[64].mission == Missions.NoMission
    assert games[8].timeline[64].role == (None,)
    assert games[8].timeline[64].time == 144.6

    assert games[8].timeline[65].action_test == ActionTest.NoAT
    assert games[8].timeline[65].actor == "spy"
    assert games[8].timeline[65].books == (None,)
    assert games[8].timeline[65].cast_name == (None,)
    assert games[8].timeline[65].category == TimelineCategory.ActionTriggered
    assert games[8].timeline[65].elapsed_time == 65.94
    assert games[8].timeline[65].event == "action triggered: fingerprint ambassador"
    assert games[8].timeline[65].mission == Missions.Fingerprint
    assert games[8].timeline[65].role == (None,)
    assert games[8].timeline[65].time == 144.0

    assert games[8].timeline[66].action_test == ActionTest.NoAT
    assert games[8].timeline[66].actor == "spy"
    assert games[8].timeline[66].books == (None,)
    assert games[8].timeline[66].cast_name == (None,)
    assert games[8].timeline[66].category == TimelineCategory.Books
    assert games[8].timeline[66].elapsed_time == 65.94
    assert games[8].timeline[66].event == "started fingerprinting book."
    assert games[8].timeline[66].mission == Missions.Fingerprint
    assert games[8].timeline[66].role == (None,)
    assert games[8].timeline[66].time == 144.0

    assert games[8].timeline[67].action_test == ActionTest.NoAT
    assert games[8].timeline[67].actor == "spy"
    assert games[8].timeline[67].books == (None,)
    assert games[8].timeline[67].cast_name == (None,)
    assert (
        games[8].timeline[67].category
        == TimelineCategory.MissionPartial | TimelineCategory.Books
    )
    assert games[8].timeline[67].elapsed_time == 66.94
    assert games[8].timeline[67].event == "fingerprinted book."
    assert games[8].timeline[67].mission == Missions.Fingerprint
    assert games[8].timeline[67].role == (None,)
    assert games[8].timeline[67].time == 143.0

    assert games[8].timeline[68].action_test == ActionTest.NoAT
    assert games[8].timeline[68].actor == "sniper"
    assert games[8].timeline[68].books == (Books.Blue,)
    assert games[8].timeline[68].cast_name == (Characters.Irish,)
    assert (
        games[8].timeline[68].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[8].timeline[68].elapsed_time == 75.06
    assert games[8].timeline[68].event == "marked book."
    assert games[8].timeline[68].mission == Missions.NoMission
    assert games[8].timeline[68].role == (Roles.Spy,)
    assert games[8].timeline[68].time == 134.9

    assert games[8].timeline[69].action_test == ActionTest.NoAT
    assert games[8].timeline[69].actor == "spy"
    assert games[8].timeline[69].books == (Books.Blue, Books.Blue)
    assert games[8].timeline[69].cast_name == (None,)
    assert games[8].timeline[69].category == TimelineCategory.Books
    assert games[8].timeline[69].elapsed_time == 77.19
    assert games[8].timeline[69].event == "put book in bookcase."
    assert games[8].timeline[69].mission == Missions.NoMission
    assert games[8].timeline[69].role == (None,)
    assert games[8].timeline[69].time == 132.8

    assert games[8].timeline[70].action_test == ActionTest.NoAT
    assert games[8].timeline[70].actor == "spy"
    assert games[8].timeline[70].books == (None,)
    assert games[8].timeline[70].cast_name == (None,)
    assert games[8].timeline[70].category == TimelineCategory.ActionTriggered
    assert games[8].timeline[70].elapsed_time == 87.88
    assert games[8].timeline[70].event == "action triggered: bug ambassador"
    assert games[8].timeline[70].mission == Missions.Bug
    assert games[8].timeline[70].role == (None,)
    assert games[8].timeline[70].time == 122.1

    assert games[8].timeline[71].action_test == ActionTest.NoAT
    assert games[8].timeline[71].actor == "spy"
    assert games[8].timeline[71].books == (None,)
    assert games[8].timeline[71].cast_name == (Characters.Carlos,)
    assert games[8].timeline[71].category == TimelineCategory.NoCategory
    assert games[8].timeline[71].elapsed_time == 87.88
    assert games[8].timeline[71].event == "begin planting bug while walking."
    assert games[8].timeline[71].mission == Missions.Bug
    assert games[8].timeline[71].role == (Roles.Ambassador,)
    assert games[8].timeline[71].time == 122.1

    assert games[8].timeline[72].action_test == ActionTest.NoAT
    assert games[8].timeline[72].actor == "spy"
    assert games[8].timeline[72].books == (None,)
    assert games[8].timeline[72].cast_name == (Characters.Carlos,)
    assert games[8].timeline[72].category == TimelineCategory.MissionComplete
    assert games[8].timeline[72].elapsed_time == 88.81
    assert games[8].timeline[72].event == "bugged ambassador while walking."
    assert games[8].timeline[72].mission == Missions.Bug
    assert games[8].timeline[72].role == (Roles.Ambassador,)
    assert games[8].timeline[72].time == 121.1

    assert games[8].timeline[73].action_test == ActionTest.NoAT
    assert games[8].timeline[73].actor == "spy"
    assert games[8].timeline[73].books == (None,)
    assert games[8].timeline[73].cast_name == (None,)
    assert games[8].timeline[73].category == TimelineCategory.Conversation
    assert games[8].timeline[73].elapsed_time == 88.94
    assert games[8].timeline[73].event == "spy enters conversation."
    assert games[8].timeline[73].mission == Missions.NoMission
    assert games[8].timeline[73].role == (None,)
    assert games[8].timeline[73].time == 121.0

    assert games[8].timeline[74].action_test == ActionTest.NoAT
    assert games[8].timeline[74].actor == "spy"
    assert games[8].timeline[74].books == (None,)
    assert games[8].timeline[74].cast_name == (Characters.Salmon,)
    assert games[8].timeline[74].category == TimelineCategory.Conversation
    assert games[8].timeline[74].elapsed_time == 88.94
    assert games[8].timeline[74].event == "spy joined conversation with double agent."
    assert games[8].timeline[74].mission == Missions.NoMission
    assert games[8].timeline[74].role == (Roles.DoubleAgent,)
    assert games[8].timeline[74].time == 121.0

    assert games[8].timeline[75].action_test == ActionTest.NoAT
    assert games[8].timeline[75].actor == "sniper"
    assert games[8].timeline[75].books == (None,)
    assert games[8].timeline[75].cast_name == (Characters.Irish,)
    assert games[8].timeline[75].category == TimelineCategory.SniperLights
    assert games[8].timeline[75].elapsed_time == 90.0
    assert games[8].timeline[75].event == "marked spy suspicious."
    assert games[8].timeline[75].mission == Missions.NoMission
    assert games[8].timeline[75].role == (Roles.Spy,)
    assert games[8].timeline[75].time == 120.0

    assert games[8].timeline[76].action_test == ActionTest.NoAT
    assert games[8].timeline[76].actor == "sniper"
    assert games[8].timeline[76].books == (None,)
    assert games[8].timeline[76].cast_name == (Characters.Plain,)
    assert games[8].timeline[76].category == TimelineCategory.SniperLights
    assert games[8].timeline[76].elapsed_time == 92.81
    assert games[8].timeline[76].event == "marked suspicious."
    assert games[8].timeline[76].mission == Missions.NoMission
    assert games[8].timeline[76].role == (Roles.Civilian,)
    assert games[8].timeline[76].time == 117.1

    assert games[8].timeline[77].action_test == ActionTest.NoAT
    assert games[8].timeline[77].actor == "spy"
    assert games[8].timeline[77].books == (None,)
    assert games[8].timeline[77].cast_name == (Characters.Salmon,)
    assert games[8].timeline[77].category == TimelineCategory.Conversation
    assert games[8].timeline[77].elapsed_time == 93.5
    assert games[8].timeline[77].event == "double agent left conversation with spy."
    assert games[8].timeline[77].mission == Missions.NoMission
    assert games[8].timeline[77].role == (Roles.DoubleAgent,)
    assert games[8].timeline[77].time == 116.5

    assert games[8].timeline[78].action_test == ActionTest.NoAT
    assert games[8].timeline[78].actor == "sniper"
    assert games[8].timeline[78].books == (None,)
    assert games[8].timeline[78].cast_name == (Characters.Alice,)
    assert games[8].timeline[78].category == TimelineCategory.SniperLights
    assert games[8].timeline[78].elapsed_time == 94.19
    assert games[8].timeline[78].event == "marked suspicious."
    assert games[8].timeline[78].mission == Missions.NoMission
    assert games[8].timeline[78].role == (Roles.Civilian,)
    assert games[8].timeline[78].time == 115.8

    assert games[8].timeline[79].action_test == ActionTest.NoAT
    assert games[8].timeline[79].actor == "spy"
    assert games[8].timeline[79].books == (None,)
    assert games[8].timeline[79].cast_name == (Characters.Irish,)
    assert games[8].timeline[79].category == TimelineCategory.Drinks
    assert games[8].timeline[79].elapsed_time == 94.19
    assert games[8].timeline[79].event == "waiter offered drink."
    assert games[8].timeline[79].mission == Missions.NoMission
    assert games[8].timeline[79].role == (Roles.Spy,)
    assert games[8].timeline[79].time == 115.8

    assert games[8].timeline[80].action_test == ActionTest.NoAT
    assert games[8].timeline[80].actor == "spy"
    assert games[8].timeline[80].books == (None,)
    assert games[8].timeline[80].cast_name == (Characters.Carlos, Characters.Irish)
    assert games[8].timeline[80].category == TimelineCategory.NoCategory
    assert games[8].timeline[80].elapsed_time == 95.88
    assert games[8].timeline[80].event == "ambassador's personal space violated."
    assert games[8].timeline[80].mission == Missions.NoMission
    assert games[8].timeline[80].role == (Roles.Ambassador, Roles.Spy)
    assert games[8].timeline[80].time == 114.1

    assert games[8].timeline[81].action_test == ActionTest.NoAT
    assert games[8].timeline[81].actor == "spy"
    assert games[8].timeline[81].books == (None,)
    assert games[8].timeline[81].cast_name == (None,)
    assert games[8].timeline[81].category == TimelineCategory.Conversation
    assert games[8].timeline[81].elapsed_time == 96.31
    assert games[8].timeline[81].event == "started talking."
    assert games[8].timeline[81].mission == Missions.NoMission
    assert games[8].timeline[81].role == (None,)
    assert games[8].timeline[81].time == 113.6

    assert games[8].timeline[82].action_test == ActionTest.NoAT
    assert games[8].timeline[82].actor == "spy"
    assert games[8].timeline[82].books == (None,)
    assert games[8].timeline[82].cast_name == (Characters.Irish,)
    assert games[8].timeline[82].category == TimelineCategory.Drinks
    assert games[8].timeline[82].elapsed_time == 99.63
    assert games[8].timeline[82].event == "rejected drink from waiter."
    assert games[8].timeline[82].mission == Missions.NoMission
    assert games[8].timeline[82].role == (Roles.Spy,)
    assert games[8].timeline[82].time == 110.3

    assert games[8].timeline[83].action_test == ActionTest.NoAT
    assert games[8].timeline[83].actor == "spy"
    assert games[8].timeline[83].books == (None,)
    assert games[8].timeline[83].cast_name == (Characters.Irish,)
    assert games[8].timeline[83].category == TimelineCategory.Drinks
    assert games[8].timeline[83].elapsed_time == 99.63
    assert games[8].timeline[83].event == "waiter stopped offering drink."
    assert games[8].timeline[83].mission == Missions.NoMission
    assert games[8].timeline[83].role == (Roles.Spy,)
    assert games[8].timeline[83].time == 110.3

    assert games[8].timeline[84].action_test == ActionTest.NoAT
    assert games[8].timeline[84].actor == "sniper"
    assert games[8].timeline[84].books == (None,)
    assert games[8].timeline[84].cast_name == (Characters.Smallman,)
    assert games[8].timeline[84].category == TimelineCategory.SniperLights
    assert games[8].timeline[84].elapsed_time == 101.75
    assert games[8].timeline[84].event == "marked less suspicious."
    assert games[8].timeline[84].mission == Missions.NoMission
    assert games[8].timeline[84].role == (Roles.Civilian,)
    assert games[8].timeline[84].time == 108.2

    assert games[8].timeline[85].action_test == ActionTest.NoAT
    assert games[8].timeline[85].actor == "spy"
    assert games[8].timeline[85].books == (None,)
    assert games[8].timeline[85].cast_name == (None,)
    assert games[8].timeline[85].category == TimelineCategory.Conversation
    assert games[8].timeline[85].elapsed_time == 102.75
    assert games[8].timeline[85].event == "spy leaves conversation."
    assert games[8].timeline[85].mission == Missions.NoMission
    assert games[8].timeline[85].role == (None,)
    assert games[8].timeline[85].time == 107.2

    assert games[8].timeline[86].action_test == ActionTest.NoAT
    assert games[8].timeline[86].actor == "spy"
    assert games[8].timeline[86].books == (None,)
    assert games[8].timeline[86].cast_name == (None,)
    assert games[8].timeline[86].category == TimelineCategory.Conversation
    assert games[8].timeline[86].elapsed_time == 103.19
    assert games[8].timeline[86].event == "spy enters conversation."
    assert games[8].timeline[86].mission == Missions.NoMission
    assert games[8].timeline[86].role == (None,)
    assert games[8].timeline[86].time == 106.8

    assert games[8].timeline[87].action_test == ActionTest.NoAT
    assert games[8].timeline[87].actor == "sniper"
    assert games[8].timeline[87].books == (None,)
    assert games[8].timeline[87].cast_name == (Characters.Teal,)
    assert games[8].timeline[87].category == TimelineCategory.SniperLights
    assert games[8].timeline[87].elapsed_time == 104.13
    assert games[8].timeline[87].event == "marked less suspicious."
    assert games[8].timeline[87].mission == Missions.NoMission
    assert games[8].timeline[87].role == (Roles.Civilian,)
    assert games[8].timeline[87].time == 105.8

    assert games[8].timeline[88].action_test == ActionTest.NoAT
    assert games[8].timeline[88].actor == "spy"
    assert games[8].timeline[88].books == (None,)
    assert games[8].timeline[88].cast_name == (None,)
    assert games[8].timeline[88].category == TimelineCategory.Conversation
    assert games[8].timeline[88].elapsed_time == 104.19
    assert games[8].timeline[88].event == "spy leaves conversation."
    assert games[8].timeline[88].mission == Missions.NoMission
    assert games[8].timeline[88].role == (None,)
    assert games[8].timeline[88].time == 105.8

    assert games[8].timeline[89].action_test == ActionTest.NoAT
    assert games[8].timeline[89].actor == "spy"
    assert games[8].timeline[89].books == (None,)
    assert games[8].timeline[89].cast_name == (None,)
    assert games[8].timeline[89].category == TimelineCategory.ActionTriggered
    assert games[8].timeline[89].elapsed_time == 110.69
    assert games[8].timeline[89].event == "action triggered: seduce target"
    assert games[8].timeline[89].mission == Missions.Seduce
    assert games[8].timeline[89].role == (None,)
    assert games[8].timeline[89].time == 99.3

    assert games[8].timeline[90].action_test == ActionTest.NoAT
    assert games[8].timeline[90].actor == "spy"
    assert games[8].timeline[90].books == (None,)
    assert games[8].timeline[90].cast_name == (Characters.General,)
    assert games[8].timeline[90].category == TimelineCategory.NoCategory
    assert games[8].timeline[90].elapsed_time == 110.69
    assert games[8].timeline[90].event == "begin flirtation with seduction target."
    assert games[8].timeline[90].mission == Missions.Seduce
    assert games[8].timeline[90].role == (Roles.SeductionTarget,)
    assert games[8].timeline[90].time == 99.3

    assert games[8].timeline[91].action_test == ActionTest.White
    assert games[8].timeline[91].actor == "spy"
    assert games[8].timeline[91].books == (None,)
    assert games[8].timeline[91].cast_name == (None,)
    assert games[8].timeline[91].category == TimelineCategory.ActionTest
    assert games[8].timeline[91].elapsed_time == 111.56
    assert games[8].timeline[91].event == "action test white: seduce target"
    assert games[8].timeline[91].mission == Missions.Seduce
    assert games[8].timeline[91].role == (None,)
    assert games[8].timeline[91].time == 98.4

    assert games[8].timeline[92].action_test == ActionTest.NoAT
    assert games[8].timeline[92].actor == "spy"
    assert games[8].timeline[92].books == (None,)
    assert games[8].timeline[92].cast_name == (Characters.General,)
    assert games[8].timeline[92].category == TimelineCategory.MissionPartial
    assert games[8].timeline[92].elapsed_time == 113.19
    assert games[8].timeline[92].event == "flirt with seduction target: 100%"
    assert games[8].timeline[92].mission == Missions.Seduce
    assert games[8].timeline[92].role == (Roles.SeductionTarget,)
    assert games[8].timeline[92].time == 96.8

    assert games[8].timeline[93].action_test == ActionTest.NoAT
    assert games[8].timeline[93].actor == "spy"
    assert games[8].timeline[93].books == (None,)
    assert games[8].timeline[93].cast_name == (Characters.General,)
    assert games[8].timeline[93].category == TimelineCategory.MissionComplete
    assert games[8].timeline[93].elapsed_time == 113.19
    assert games[8].timeline[93].event == "target seduced."
    assert games[8].timeline[93].mission == Missions.Seduce
    assert games[8].timeline[93].role == (Roles.SeductionTarget,)
    assert games[8].timeline[93].time == 96.8

    assert games[8].timeline[94].action_test == ActionTest.NoAT
    assert games[8].timeline[94].actor == "spy"
    assert games[8].timeline[94].books == (Books.Blue,)
    assert games[8].timeline[94].cast_name == (None,)
    assert games[8].timeline[94].category == TimelineCategory.Books
    assert games[8].timeline[94].elapsed_time == 116.31
    assert games[8].timeline[94].event == "get book from bookcase."
    assert games[8].timeline[94].mission == Missions.NoMission
    assert games[8].timeline[94].role == (None,)
    assert games[8].timeline[94].time == 93.6

    assert games[8].timeline[95].action_test == ActionTest.NoAT
    assert games[8].timeline[95].actor == "sniper"
    assert games[8].timeline[95].books == (None,)
    assert games[8].timeline[95].cast_name == (Characters.General,)
    assert games[8].timeline[95].category == TimelineCategory.SniperLights
    assert games[8].timeline[95].elapsed_time == 120.38
    assert games[8].timeline[95].event == "marked suspicious."
    assert games[8].timeline[95].mission == Missions.NoMission
    assert games[8].timeline[95].role == (Roles.SeductionTarget,)
    assert games[8].timeline[95].time == 89.6

    assert games[8].timeline[96].action_test == ActionTest.NoAT
    assert games[8].timeline[96].actor == "spy"
    assert games[8].timeline[96].books == (Books.Blue, Books.Blue)
    assert games[8].timeline[96].cast_name == (None,)
    assert games[8].timeline[96].category == TimelineCategory.Books
    assert games[8].timeline[96].elapsed_time == 133.06
    assert games[8].timeline[96].event == "put book in bookcase."
    assert games[8].timeline[96].mission == Missions.NoMission
    assert games[8].timeline[96].role == (None,)
    assert games[8].timeline[96].time == 76.9

    assert games[8].timeline[97].action_test == ActionTest.NoAT
    assert games[8].timeline[97].actor == "spy"
    assert games[8].timeline[97].books == (Books.Blue,)
    assert games[8].timeline[97].cast_name == (None,)
    assert games[8].timeline[97].category == TimelineCategory.Books
    assert games[8].timeline[97].elapsed_time == 183.06
    assert games[8].timeline[97].event == "get book from bookcase."
    assert games[8].timeline[97].mission == Missions.NoMission
    assert games[8].timeline[97].role == (None,)
    assert games[8].timeline[97].time == 26.9

    assert games[8].timeline[98].action_test == ActionTest.NoAT
    assert games[8].timeline[98].actor == "spy"
    assert games[8].timeline[98].books == (None,)
    assert games[8].timeline[98].cast_name == (None,)
    assert games[8].timeline[98].category == TimelineCategory.ActionTriggered
    assert games[8].timeline[98].elapsed_time == 183.56
    assert games[8].timeline[98].event == "action triggered: fingerprint ambassador"
    assert games[8].timeline[98].mission == Missions.Fingerprint
    assert games[8].timeline[98].role == (None,)
    assert games[8].timeline[98].time == 26.4

    assert games[8].timeline[99].action_test == ActionTest.NoAT
    assert games[8].timeline[99].actor == "spy"
    assert games[8].timeline[99].books == (None,)
    assert games[8].timeline[99].cast_name == (None,)
    assert games[8].timeline[99].category == TimelineCategory.Books
    assert games[8].timeline[99].elapsed_time == 183.56
    assert games[8].timeline[99].event == "started fingerprinting book."
    assert games[8].timeline[99].mission == Missions.Fingerprint
    assert games[8].timeline[99].role == (None,)
    assert games[8].timeline[99].time == 26.4

    assert games[8].timeline[100].action_test == ActionTest.NoAT
    assert games[8].timeline[100].actor == "spy"
    assert games[8].timeline[100].books == (None,)
    assert games[8].timeline[100].cast_name == (None,)
    assert (
        games[8].timeline[100].category
        == TimelineCategory.MissionPartial | TimelineCategory.Books
    )
    assert games[8].timeline[100].elapsed_time == 184.56
    assert games[8].timeline[100].event == "fingerprinted book."
    assert games[8].timeline[100].mission == Missions.Fingerprint
    assert games[8].timeline[100].role == (None,)
    assert games[8].timeline[100].time == 25.4

    assert games[8].timeline[101].action_test == ActionTest.NoAT
    assert games[8].timeline[101].actor == "spy"
    assert games[8].timeline[101].books == (None,)
    assert games[8].timeline[101].cast_name == (None,)
    assert games[8].timeline[101].category == TimelineCategory.MissionComplete
    assert games[8].timeline[101].elapsed_time == 184.56
    assert games[8].timeline[101].event == "fingerprinted ambassador."
    assert games[8].timeline[101].mission == Missions.Fingerprint
    assert games[8].timeline[101].role == (None,)
    assert games[8].timeline[101].time == 25.4

    assert games[8].timeline[102].action_test == ActionTest.NoAT
    assert games[8].timeline[102].actor == "spy"
    assert games[8].timeline[102].books == (Books.Blue, Books.Blue)
    assert games[8].timeline[102].cast_name == (None,)
    assert games[8].timeline[102].category == TimelineCategory.Books
    assert games[8].timeline[102].elapsed_time == 192.69
    assert games[8].timeline[102].event == "put book in bookcase."
    assert games[8].timeline[102].mission == Missions.NoMission
    assert games[8].timeline[102].role == (None,)
    assert games[8].timeline[102].time == 17.3

    assert games[8].timeline[103].action_test == ActionTest.NoAT
    assert games[8].timeline[103].actor == "spy"
    assert games[8].timeline[103].books == (None,)
    assert games[8].timeline[103].cast_name == (None,)
    assert games[8].timeline[103].category == TimelineCategory.Statues
    assert games[8].timeline[103].elapsed_time == 200.0
    assert games[8].timeline[103].event == "picked up statue."
    assert games[8].timeline[103].mission == Missions.NoMission
    assert games[8].timeline[103].role == (None,)
    assert games[8].timeline[103].time == 10.0

    assert games[8].timeline[104].action_test == ActionTest.NoAT
    assert games[8].timeline[104].actor == "spy"
    assert games[8].timeline[104].books == (None,)
    assert games[8].timeline[104].cast_name == (None,)
    assert (
        games[8].timeline[104].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[8].timeline[104].elapsed_time == 202.81
    assert games[8].timeline[104].event == "action triggered: swap statue"
    assert games[8].timeline[104].mission == Missions.Swap
    assert games[8].timeline[104].role == (None,)
    assert games[8].timeline[104].time == 7.1

    assert games[8].timeline[105].action_test == ActionTest.White
    assert games[8].timeline[105].actor == "spy"
    assert games[8].timeline[105].books == (None,)
    assert games[8].timeline[105].cast_name == (None,)
    assert (
        games[8].timeline[105].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[8].timeline[105].elapsed_time == 203.75
    assert games[8].timeline[105].event == "action test white: swap statue"
    assert games[8].timeline[105].mission == Missions.Swap
    assert games[8].timeline[105].role == (None,)
    assert games[8].timeline[105].time == 6.2

    assert games[8].timeline[106].action_test == ActionTest.NoAT
    assert games[8].timeline[106].actor == "spy"
    assert games[8].timeline[106].books == (None,)
    assert games[8].timeline[106].cast_name == (None,)
    assert (
        games[8].timeline[106].category
        == TimelineCategory.MissionComplete | TimelineCategory.Statues
    )
    assert games[8].timeline[106].elapsed_time == 203.75
    assert games[8].timeline[106].event == "statue swapped."
    assert games[8].timeline[106].mission == Missions.Swap
    assert games[8].timeline[106].role == (None,)
    assert games[8].timeline[106].time == 6.2

    assert games[8].timeline[107].action_test == ActionTest.NoAT
    assert games[8].timeline[107].actor == "game"
    assert games[8].timeline[107].books == (None,)
    assert games[8].timeline[107].cast_name == (None,)
    assert games[8].timeline[107].category == TimelineCategory.MissionCountdown
    assert games[8].timeline[107].elapsed_time == 203.75
    assert games[8].timeline[107].event == "missions completed. 10 second countdown."
    assert games[8].timeline[107].mission == Missions.NoMission
    assert games[8].timeline[107].role == (None,)
    assert games[8].timeline[107].time == 6.2

    assert games[8].timeline[108].action_test == ActionTest.NoAT
    assert games[8].timeline[108].actor == "sniper"
    assert games[8].timeline[108].books == (None,)
    assert games[8].timeline[108].cast_name == (Characters.Irish,)
    assert games[8].timeline[108].category == TimelineCategory.SniperShot
    assert games[8].timeline[108].elapsed_time == 206.5
    assert games[8].timeline[108].event == "took shot."
    assert games[8].timeline[108].mission == Missions.NoMission
    assert games[8].timeline[108].role == (Roles.Spy,)
    assert games[8].timeline[108].time == 3.5

    assert games[8].timeline[109].action_test == ActionTest.NoAT
    assert games[8].timeline[109].actor == "spy"
    assert games[8].timeline[109].books == (None,)
    assert games[8].timeline[109].cast_name == (None,)
    assert games[8].timeline[109].category == TimelineCategory.Statues
    assert games[8].timeline[109].elapsed_time == 206.88
    assert games[8].timeline[109].event == "put back statue."
    assert games[8].timeline[109].mission == Missions.NoMission
    assert games[8].timeline[109].role == (None,)
    assert games[8].timeline[109].time == 3.1

    assert games[8].timeline[110].action_test == ActionTest.NoAT
    assert games[8].timeline[110].actor == "spy"
    assert games[8].timeline[110].books == (None,)
    assert games[8].timeline[110].cast_name == (None,)
    assert games[8].timeline[110].category == TimelineCategory.Statues
    assert games[8].timeline[110].elapsed_time == 207.44
    assert games[8].timeline[110].event == "dropped statue."
    assert games[8].timeline[110].mission == Missions.NoMission
    assert games[8].timeline[110].role == (None,)
    assert games[8].timeline[110].time == 2.5

    assert games[8].timeline[111].action_test == ActionTest.NoAT
    assert games[8].timeline[111].actor == "game"
    assert games[8].timeline[111].books == (None,)
    assert games[8].timeline[111].cast_name == (Characters.Irish,)
    assert games[8].timeline[111].category == TimelineCategory.GameEnd
    assert games[8].timeline[111].elapsed_time == 210.06
    assert games[8].timeline[111].event == "sniper shot spy."
    assert games[8].timeline[111].mission == Missions.NoMission
    assert games[8].timeline[111].role == (Roles.Spy,)
    assert games[8].timeline[111].time == 0.0

    assert games[8].timeline.get_next_spy_action(games[8].timeline[111]) is None


@pytest.mark.parsing
def test_parse_timeline_normal_with_limit(
    tmp_path,
    get_test_events_folder,
    get_test_unparsed_folder,
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda x: None)
    monkeypatch.setattr(time, "sleep", lambda x: None)

    relevant_uuids = [
        "OiG7qvC9QOaSKVGlesdpWQ",
        "vgAlD77AQw2XKTZq3H4NTg",
    ]

    relevant_pkl_files = [tmp_path.joinpath(f"{u}.pkl") for u in relevant_uuids]

    for pkl_file in relevant_pkl_files:
        assert not pkl_file.exists()

    games = parse_replays(
        lambda game: game.division == "Copper" and game.uuid in relevant_uuids,
        unparsed_folder=get_test_unparsed_folder,
        events_folder=get_test_events_folder,
        pickle_folder=tmp_path,
        screenshot_iterator=mock_screenshot_iterator,
        limit=2,
        json_folder=tmp_path,
    )

    for pkl_file in relevant_pkl_files:
        assert pkl_file.exists()

    games.sort(key=lambda g: g.start_time)

    assert len(games[0].timeline) == 119
    assert len(games[1].timeline) == 74

    assert games[0].uuid == "OiG7qvC9QOaSKVGlesdpWQ"
    assert games[0].timeline[0].action_test == ActionTest.NoAT
    assert games[0].timeline[0].actor == "spy"
    assert games[0].timeline[0].books == (None,)
    assert games[0].timeline[0].cast_name == (Characters.Irish,)
    assert games[0].timeline[0].category == TimelineCategory.Cast
    assert games[0].timeline[0].elapsed_time == 0.0
    assert games[0].timeline[0].event == "spy cast."
    assert games[0].timeline[0].mission == Missions.NoMission
    assert games[0].timeline[0].role == (Roles.Spy,)
    assert games[0].timeline[0].time == 225.0

    assert games[0].timeline[1].action_test == ActionTest.NoAT
    assert games[0].timeline[1].actor == "spy"
    assert games[0].timeline[1].books == (None,)
    assert games[0].timeline[1].cast_name == (Characters.Carlos,)
    assert games[0].timeline[1].category == TimelineCategory.Cast
    assert games[0].timeline[1].elapsed_time == 0.0
    assert games[0].timeline[1].event == "ambassador cast."
    assert games[0].timeline[1].mission == Missions.NoMission
    assert games[0].timeline[1].role == (Roles.Ambassador,)
    assert games[0].timeline[1].time == 225.0

    assert games[0].timeline[2].action_test == ActionTest.NoAT
    assert games[0].timeline[2].actor == "spy"
    assert games[0].timeline[2].books == (None,)
    assert games[0].timeline[2].cast_name == (Characters.Boots,)
    assert games[0].timeline[2].category == TimelineCategory.Cast
    assert games[0].timeline[2].elapsed_time == 0.0
    assert games[0].timeline[2].event == "double agent cast."
    assert games[0].timeline[2].mission == Missions.NoMission
    assert games[0].timeline[2].role == (Roles.DoubleAgent,)
    assert games[0].timeline[2].time == 225.0

    assert games[0].timeline[3].action_test == ActionTest.NoAT
    assert games[0].timeline[3].actor == "spy"
    assert games[0].timeline[3].books == (None,)
    assert games[0].timeline[3].cast_name == (Characters.Wheels,)
    assert games[0].timeline[3].category == TimelineCategory.Cast
    assert games[0].timeline[3].elapsed_time == 0.0
    assert games[0].timeline[3].event == "suspected double agent cast."
    assert games[0].timeline[3].mission == Missions.NoMission
    assert games[0].timeline[3].role == (Roles.SuspectedDoubleAgent,)
    assert games[0].timeline[3].time == 225.0

    assert games[0].timeline[4].action_test == ActionTest.NoAT
    assert games[0].timeline[4].actor == "spy"
    assert games[0].timeline[4].books == (None,)
    assert games[0].timeline[4].cast_name == (Characters.Morgan,)
    assert games[0].timeline[4].category == TimelineCategory.Cast
    assert games[0].timeline[4].elapsed_time == 0.0
    assert games[0].timeline[4].event == "seduction target cast."
    assert games[0].timeline[4].mission == Missions.NoMission
    assert games[0].timeline[4].role == (Roles.SeductionTarget,)
    assert games[0].timeline[4].time == 225.0

    assert games[0].timeline[5].action_test == ActionTest.NoAT
    assert games[0].timeline[5].actor == "spy"
    assert games[0].timeline[5].books == (None,)
    assert games[0].timeline[5].cast_name == (Characters.Queen,)
    assert games[0].timeline[5].category == TimelineCategory.Cast
    assert games[0].timeline[5].elapsed_time == 0.0
    assert games[0].timeline[5].event == "civilian cast."
    assert games[0].timeline[5].mission == Missions.NoMission
    assert games[0].timeline[5].role == (Roles.Civilian,)
    assert games[0].timeline[5].time == 225.0

    assert games[0].timeline[6].action_test == ActionTest.NoAT
    assert games[0].timeline[6].actor == "spy"
    assert games[0].timeline[6].books == (None,)
    assert games[0].timeline[6].cast_name == (Characters.Duke,)
    assert games[0].timeline[6].category == TimelineCategory.Cast
    assert games[0].timeline[6].elapsed_time == 0.0
    assert games[0].timeline[6].event == "civilian cast."
    assert games[0].timeline[6].mission == Missions.NoMission
    assert games[0].timeline[6].role == (Roles.Civilian,)
    assert games[0].timeline[6].time == 225.0

    assert games[0].timeline[7].action_test == ActionTest.NoAT
    assert games[0].timeline[7].actor == "spy"
    assert games[0].timeline[7].books == (None,)
    assert games[0].timeline[7].cast_name == (Characters.Oprah,)
    assert games[0].timeline[7].category == TimelineCategory.Cast
    assert games[0].timeline[7].elapsed_time == 0.0
    assert games[0].timeline[7].event == "civilian cast."
    assert games[0].timeline[7].mission == Missions.NoMission
    assert games[0].timeline[7].role == (Roles.Civilian,)
    assert games[0].timeline[7].time == 225.0

    assert games[0].timeline[8].action_test == ActionTest.NoAT
    assert games[0].timeline[8].actor == "spy"
    assert games[0].timeline[8].books == (None,)
    assert games[0].timeline[8].cast_name == (Characters.Sari,)
    assert games[0].timeline[8].category == TimelineCategory.Cast
    assert games[0].timeline[8].elapsed_time == 0.0
    assert games[0].timeline[8].event == "civilian cast."
    assert games[0].timeline[8].mission == Missions.NoMission
    assert games[0].timeline[8].role == (Roles.Civilian,)
    assert games[0].timeline[8].time == 225.0

    assert games[0].timeline[9].action_test == ActionTest.NoAT
    assert games[0].timeline[9].actor == "spy"
    assert games[0].timeline[9].books == (None,)
    assert games[0].timeline[9].cast_name == (Characters.Bling,)
    assert games[0].timeline[9].category == TimelineCategory.Cast
    assert games[0].timeline[9].elapsed_time == 0.0
    assert games[0].timeline[9].event == "civilian cast."
    assert games[0].timeline[9].mission == Missions.NoMission
    assert games[0].timeline[9].role == (Roles.Civilian,)
    assert games[0].timeline[9].time == 225.0

    assert games[0].timeline[10].action_test == ActionTest.NoAT
    assert games[0].timeline[10].actor == "spy"
    assert games[0].timeline[10].books == (None,)
    assert games[0].timeline[10].cast_name == (Characters.Disney,)
    assert games[0].timeline[10].category == TimelineCategory.Cast
    assert games[0].timeline[10].elapsed_time == 0.0
    assert games[0].timeline[10].event == "civilian cast."
    assert games[0].timeline[10].mission == Missions.NoMission
    assert games[0].timeline[10].role == (Roles.Civilian,)
    assert games[0].timeline[10].time == 225.0

    assert games[0].timeline[11].action_test == ActionTest.NoAT
    assert games[0].timeline[11].actor == "spy"
    assert games[0].timeline[11].books == (None,)
    assert games[0].timeline[11].cast_name == (Characters.Salmon,)
    assert games[0].timeline[11].category == TimelineCategory.Cast
    assert games[0].timeline[11].elapsed_time == 0.0
    assert games[0].timeline[11].event == "civilian cast."
    assert games[0].timeline[11].mission == Missions.NoMission
    assert games[0].timeline[11].role == (Roles.Civilian,)
    assert games[0].timeline[11].time == 225.0

    assert games[0].timeline[12].action_test == ActionTest.NoAT
    assert games[0].timeline[12].actor == "spy"
    assert games[0].timeline[12].books == (None,)
    assert games[0].timeline[12].cast_name == (Characters.General,)
    assert games[0].timeline[12].category == TimelineCategory.Cast
    assert games[0].timeline[12].elapsed_time == 0.0
    assert games[0].timeline[12].event == "civilian cast."
    assert games[0].timeline[12].mission == Missions.NoMission
    assert games[0].timeline[12].role == (Roles.Civilian,)
    assert games[0].timeline[12].time == 225.0

    assert games[0].timeline[13].action_test == ActionTest.NoAT
    assert games[0].timeline[13].actor == "spy"
    assert games[0].timeline[13].books == (None,)
    assert games[0].timeline[13].cast_name == (Characters.Rocker,)
    assert games[0].timeline[13].category == TimelineCategory.Cast
    assert games[0].timeline[13].elapsed_time == 0.0
    assert games[0].timeline[13].event == "civilian cast."
    assert games[0].timeline[13].mission == Missions.NoMission
    assert games[0].timeline[13].role == (Roles.Civilian,)
    assert games[0].timeline[13].time == 225.0

    assert games[0].timeline[14].action_test == ActionTest.NoAT
    assert games[0].timeline[14].actor == "spy"
    assert games[0].timeline[14].books == (None,)
    assert games[0].timeline[14].cast_name == (Characters.Teal,)
    assert games[0].timeline[14].category == TimelineCategory.Cast
    assert games[0].timeline[14].elapsed_time == 0.0
    assert games[0].timeline[14].event == "civilian cast."
    assert games[0].timeline[14].mission == Missions.NoMission
    assert games[0].timeline[14].role == (Roles.Civilian,)
    assert games[0].timeline[14].time == 225.0

    assert games[0].timeline[15].action_test == ActionTest.NoAT
    assert games[0].timeline[15].actor == "spy"
    assert games[0].timeline[15].books == (None,)
    assert games[0].timeline[15].cast_name == (Characters.Alice,)
    assert games[0].timeline[15].category == TimelineCategory.Cast
    assert games[0].timeline[15].elapsed_time == 0.0
    assert games[0].timeline[15].event == "civilian cast."
    assert games[0].timeline[15].mission == Missions.NoMission
    assert games[0].timeline[15].role == (Roles.Civilian,)
    assert games[0].timeline[15].time == 225.0

    assert games[0].timeline[16].action_test == ActionTest.NoAT
    assert games[0].timeline[16].actor == "spy"
    assert games[0].timeline[16].books == (None,)
    assert games[0].timeline[16].cast_name == (Characters.Smallman,)
    assert games[0].timeline[16].category == TimelineCategory.Cast
    assert games[0].timeline[16].elapsed_time == 0.0
    assert games[0].timeline[16].event == "civilian cast."
    assert games[0].timeline[16].mission == Missions.NoMission
    assert games[0].timeline[16].role == (Roles.Civilian,)
    assert games[0].timeline[16].time == 225.0

    assert games[0].timeline[17].action_test == ActionTest.NoAT
    assert games[0].timeline[17].actor == "spy"
    assert games[0].timeline[17].books == (None,)
    assert games[0].timeline[17].cast_name == (Characters.Sikh,)
    assert games[0].timeline[17].category == TimelineCategory.Cast
    assert games[0].timeline[17].elapsed_time == 0.0
    assert games[0].timeline[17].event == "civilian cast."
    assert games[0].timeline[17].mission == Missions.NoMission
    assert games[0].timeline[17].role == (Roles.Civilian,)
    assert games[0].timeline[17].time == 225.0

    assert games[0].timeline[18].action_test == ActionTest.NoAT
    assert games[0].timeline[18].actor == "spy"
    assert games[0].timeline[18].books == (None,)
    assert games[0].timeline[18].cast_name == (Characters.Plain,)
    assert games[0].timeline[18].category == TimelineCategory.Cast
    assert games[0].timeline[18].elapsed_time == 0.0
    assert games[0].timeline[18].event == "civilian cast."
    assert games[0].timeline[18].mission == Missions.NoMission
    assert games[0].timeline[18].role == (Roles.Civilian,)
    assert games[0].timeline[18].time == 225.0

    assert games[0].timeline[19].action_test == ActionTest.NoAT
    assert games[0].timeline[19].actor == "spy"
    assert games[0].timeline[19].books == (None,)
    assert games[0].timeline[19].cast_name == (Characters.Helen,)
    assert games[0].timeline[19].category == TimelineCategory.Cast
    assert games[0].timeline[19].elapsed_time == 0.0
    assert games[0].timeline[19].event == "civilian cast."
    assert games[0].timeline[19].mission == Missions.NoMission
    assert games[0].timeline[19].role == (Roles.Civilian,)
    assert games[0].timeline[19].time == 225.0

    assert games[0].timeline[20].action_test == ActionTest.NoAT
    assert games[0].timeline[20].actor == "spy"
    assert games[0].timeline[20].books == (None,)
    assert games[0].timeline[20].cast_name == (Characters.Taft,)
    assert games[0].timeline[20].category == TimelineCategory.Cast
    assert games[0].timeline[20].elapsed_time == 0.0
    assert games[0].timeline[20].event == "civilian cast."
    assert games[0].timeline[20].mission == Missions.NoMission
    assert games[0].timeline[20].role == (Roles.Civilian,)
    assert games[0].timeline[20].time == 225.0

    assert games[0].timeline[21].action_test == ActionTest.NoAT
    assert games[0].timeline[21].actor == "spy"
    assert games[0].timeline[21].books == (None,)
    assert games[0].timeline[21].cast_name == (None,)
    assert games[0].timeline[21].category == TimelineCategory.MissionSelected
    assert games[0].timeline[21].elapsed_time == 0.0
    assert games[0].timeline[21].event == "bug ambassador selected."
    assert games[0].timeline[21].mission == Missions.Bug
    assert games[0].timeline[21].role == (None,)
    assert games[0].timeline[21].time == 225.0

    assert games[0].timeline[22].action_test == ActionTest.NoAT
    assert games[0].timeline[22].actor == "spy"
    assert games[0].timeline[22].books == (None,)
    assert games[0].timeline[22].cast_name == (None,)
    assert games[0].timeline[22].category == TimelineCategory.MissionSelected
    assert games[0].timeline[22].elapsed_time == 0.0
    assert games[0].timeline[22].event == "contact double agent selected."
    assert games[0].timeline[22].mission == Missions.Contact
    assert games[0].timeline[22].role == (None,)
    assert games[0].timeline[22].time == 225.0

    assert games[0].timeline[23].action_test == ActionTest.NoAT
    assert games[0].timeline[23].actor == "spy"
    assert games[0].timeline[23].books == (None,)
    assert games[0].timeline[23].cast_name == (None,)
    assert games[0].timeline[23].category == TimelineCategory.MissionSelected
    assert games[0].timeline[23].elapsed_time == 0.0
    assert games[0].timeline[23].event == "transfer microfilm selected."
    assert games[0].timeline[23].mission == Missions.Transfer
    assert games[0].timeline[23].role == (None,)
    assert games[0].timeline[23].time == 225.0

    assert games[0].timeline[24].action_test == ActionTest.NoAT
    assert games[0].timeline[24].actor == "spy"
    assert games[0].timeline[24].books == (None,)
    assert games[0].timeline[24].cast_name == (None,)
    assert games[0].timeline[24].category == TimelineCategory.MissionSelected
    assert games[0].timeline[24].elapsed_time == 0.0
    assert games[0].timeline[24].event == "swap statue selected."
    assert games[0].timeline[24].mission == Missions.Swap
    assert games[0].timeline[24].role == (None,)
    assert games[0].timeline[24].time == 225.0

    assert games[0].timeline[25].action_test == ActionTest.NoAT
    assert games[0].timeline[25].actor == "spy"
    assert games[0].timeline[25].books == (None,)
    assert games[0].timeline[25].cast_name == (None,)
    assert games[0].timeline[25].category == TimelineCategory.MissionSelected
    assert games[0].timeline[25].elapsed_time == 0.0
    assert games[0].timeline[25].event == "inspect 3 statues selected."
    assert games[0].timeline[25].mission == Missions.Inspect
    assert games[0].timeline[25].role == (None,)
    assert games[0].timeline[25].time == 225.0

    assert games[0].timeline[26].action_test == ActionTest.NoAT
    assert games[0].timeline[26].actor == "spy"
    assert games[0].timeline[26].books == (None,)
    assert games[0].timeline[26].cast_name == (None,)
    assert games[0].timeline[26].category == TimelineCategory.MissionSelected
    assert games[0].timeline[26].elapsed_time == 0.0
    assert games[0].timeline[26].event == "seduce target selected."
    assert games[0].timeline[26].mission == Missions.Seduce
    assert games[0].timeline[26].role == (None,)
    assert games[0].timeline[26].time == 225.0

    assert games[0].timeline[27].action_test == ActionTest.NoAT
    assert games[0].timeline[27].actor == "spy"
    assert games[0].timeline[27].books == (None,)
    assert games[0].timeline[27].cast_name == (None,)
    assert games[0].timeline[27].category == TimelineCategory.MissionSelected
    assert games[0].timeline[27].elapsed_time == 0.0
    assert games[0].timeline[27].event == "purloin guest list selected."
    assert games[0].timeline[27].mission == Missions.Purloin
    assert games[0].timeline[27].role == (None,)
    assert games[0].timeline[27].time == 225.0

    assert games[0].timeline[28].action_test == ActionTest.NoAT
    assert games[0].timeline[28].actor == "spy"
    assert games[0].timeline[28].books == (None,)
    assert games[0].timeline[28].cast_name == (None,)
    assert games[0].timeline[28].category == TimelineCategory.MissionSelected
    assert games[0].timeline[28].elapsed_time == 0.0
    assert games[0].timeline[28].event == "fingerprint ambassador selected."
    assert games[0].timeline[28].mission == Missions.Fingerprint
    assert games[0].timeline[28].role == (None,)
    assert games[0].timeline[28].time == 225.0

    assert games[0].timeline[29].action_test == ActionTest.NoAT
    assert games[0].timeline[29].actor == "spy"
    assert games[0].timeline[29].books == (None,)
    assert games[0].timeline[29].cast_name == (None,)
    assert games[0].timeline[29].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[29].elapsed_time == 0.0
    assert games[0].timeline[29].event == "bug ambassador enabled."
    assert games[0].timeline[29].mission == Missions.Bug
    assert games[0].timeline[29].role == (None,)
    assert games[0].timeline[29].time == 225.0

    assert games[0].timeline[30].action_test == ActionTest.NoAT
    assert games[0].timeline[30].actor == "spy"
    assert games[0].timeline[30].books == (None,)
    assert games[0].timeline[30].cast_name == (None,)
    assert games[0].timeline[30].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[30].elapsed_time == 0.0
    assert games[0].timeline[30].event == "contact double agent enabled."
    assert games[0].timeline[30].mission == Missions.Contact
    assert games[0].timeline[30].role == (None,)
    assert games[0].timeline[30].time == 225.0

    assert games[0].timeline[31].action_test == ActionTest.NoAT
    assert games[0].timeline[31].actor == "spy"
    assert games[0].timeline[31].books == (None,)
    assert games[0].timeline[31].cast_name == (None,)
    assert games[0].timeline[31].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[31].elapsed_time == 0.0
    assert games[0].timeline[31].event == "transfer microfilm enabled."
    assert games[0].timeline[31].mission == Missions.Transfer
    assert games[0].timeline[31].role == (None,)
    assert games[0].timeline[31].time == 225.0

    assert games[0].timeline[32].action_test == ActionTest.NoAT
    assert games[0].timeline[32].actor == "spy"
    assert games[0].timeline[32].books == (None,)
    assert games[0].timeline[32].cast_name == (None,)
    assert games[0].timeline[32].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[32].elapsed_time == 0.0
    assert games[0].timeline[32].event == "swap statue enabled."
    assert games[0].timeline[32].mission == Missions.Swap
    assert games[0].timeline[32].role == (None,)
    assert games[0].timeline[32].time == 225.0

    assert games[0].timeline[33].action_test == ActionTest.NoAT
    assert games[0].timeline[33].actor == "spy"
    assert games[0].timeline[33].books == (None,)
    assert games[0].timeline[33].cast_name == (None,)
    assert games[0].timeline[33].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[33].elapsed_time == 0.0
    assert games[0].timeline[33].event == "inspect 3 statues enabled."
    assert games[0].timeline[33].mission == Missions.Inspect
    assert games[0].timeline[33].role == (None,)
    assert games[0].timeline[33].time == 225.0

    assert games[0].timeline[34].action_test == ActionTest.NoAT
    assert games[0].timeline[34].actor == "spy"
    assert games[0].timeline[34].books == (None,)
    assert games[0].timeline[34].cast_name == (None,)
    assert games[0].timeline[34].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[34].elapsed_time == 0.0
    assert games[0].timeline[34].event == "seduce target enabled."
    assert games[0].timeline[34].mission == Missions.Seduce
    assert games[0].timeline[34].role == (None,)
    assert games[0].timeline[34].time == 225.0

    assert games[0].timeline[35].action_test == ActionTest.NoAT
    assert games[0].timeline[35].actor == "spy"
    assert games[0].timeline[35].books == (None,)
    assert games[0].timeline[35].cast_name == (None,)
    assert games[0].timeline[35].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[35].elapsed_time == 0.0
    assert games[0].timeline[35].event == "purloin guest list enabled."
    assert games[0].timeline[35].mission == Missions.Purloin
    assert games[0].timeline[35].role == (None,)
    assert games[0].timeline[35].time == 225.0

    assert games[0].timeline[36].action_test == ActionTest.NoAT
    assert games[0].timeline[36].actor == "spy"
    assert games[0].timeline[36].books == (None,)
    assert games[0].timeline[36].cast_name == (None,)
    assert games[0].timeline[36].category == TimelineCategory.MissionEnabled
    assert games[0].timeline[36].elapsed_time == 0.0
    assert games[0].timeline[36].event == "fingerprint ambassador enabled."
    assert games[0].timeline[36].mission == Missions.Fingerprint
    assert games[0].timeline[36].role == (None,)
    assert games[0].timeline[36].time == 225.0

    assert games[0].timeline[37].action_test == ActionTest.NoAT
    assert games[0].timeline[37].actor == "game"
    assert games[0].timeline[37].books == (None,)
    assert games[0].timeline[37].cast_name == (None,)
    assert games[0].timeline[37].category == TimelineCategory.GameStart
    assert games[0].timeline[37].elapsed_time == 0.0
    assert games[0].timeline[37].event == "game started."
    assert games[0].timeline[37].mission == Missions.NoMission
    assert games[0].timeline[37].role == (None,)
    assert games[0].timeline[37].time == 225.0

    assert games[0].timeline[38].action_test == ActionTest.NoAT
    assert games[0].timeline[38].actor == "spy"
    assert games[0].timeline[38].books == (None,)
    assert games[0].timeline[38].cast_name == (None,)
    assert games[0].timeline[38].category == TimelineCategory.NoCategory
    assert games[0].timeline[38].elapsed_time == 1.31
    assert games[0].timeline[38].event == "spy player takes control from ai."
    assert games[0].timeline[38].mission == Missions.NoMission
    assert games[0].timeline[38].role == (None,)
    assert games[0].timeline[38].time == 223.6

    assert games[0].timeline[39].action_test == ActionTest.NoAT
    assert games[0].timeline[39].actor == "sniper"
    assert games[0].timeline[39].books == (None,)
    assert games[0].timeline[39].cast_name == (Characters.Carlos,)
    assert games[0].timeline[39].category == TimelineCategory.SniperLights
    assert games[0].timeline[39].elapsed_time == 3.88
    assert games[0].timeline[39].event == "marked suspicious."
    assert games[0].timeline[39].mission == Missions.NoMission
    assert games[0].timeline[39].role == (Roles.Ambassador,)
    assert games[0].timeline[39].time == 221.1

    assert games[0].timeline[40].action_test == ActionTest.NoAT
    assert games[0].timeline[40].actor == "sniper"
    assert games[0].timeline[40].books == (None,)
    assert games[0].timeline[40].cast_name == (Characters.Damon,)
    assert games[0].timeline[40].category == TimelineCategory.SniperLights
    assert games[0].timeline[40].elapsed_time == 5.25
    assert games[0].timeline[40].event == "marked less suspicious."
    assert games[0].timeline[40].mission == Missions.NoMission
    assert games[0].timeline[40].role == (Roles.Staff,)
    assert games[0].timeline[40].time == 219.7

    assert games[0].timeline[41].action_test == ActionTest.NoAT
    assert games[0].timeline[41].actor == "sniper"
    assert games[0].timeline[41].books == (None,)
    assert games[0].timeline[41].cast_name == (Characters.Toby,)
    assert games[0].timeline[41].category == TimelineCategory.SniperLights
    assert games[0].timeline[41].elapsed_time == 6.38
    assert games[0].timeline[41].event == "marked suspicious."
    assert games[0].timeline[41].mission == Missions.NoMission
    assert games[0].timeline[41].role == (Roles.Staff,)
    assert games[0].timeline[41].time == 218.6

    assert games[0].timeline[42].action_test == ActionTest.NoAT
    assert games[0].timeline[42].actor == "sniper"
    assert games[0].timeline[42].books == (None,)
    assert games[0].timeline[42].cast_name == (Characters.Boots,)
    assert games[0].timeline[42].category == TimelineCategory.SniperLights
    assert games[0].timeline[42].elapsed_time == 8.81
    assert games[0].timeline[42].event == "marked less suspicious."
    assert games[0].timeline[42].mission == Missions.NoMission
    assert games[0].timeline[42].role == (Roles.DoubleAgent,)
    assert games[0].timeline[42].time == 216.1

    assert games[0].timeline[43].action_test == ActionTest.NoAT
    assert games[0].timeline[43].actor == "sniper"
    assert games[0].timeline[43].books == (None,)
    assert games[0].timeline[43].cast_name == (Characters.Wheels,)
    assert games[0].timeline[43].category == TimelineCategory.SniperLights
    assert games[0].timeline[43].elapsed_time == 9.81
    assert games[0].timeline[43].event == "marked less suspicious."
    assert games[0].timeline[43].mission == Missions.NoMission
    assert games[0].timeline[43].role == (Roles.SuspectedDoubleAgent,)
    assert games[0].timeline[43].time == 215.1

    assert games[0].timeline[44].action_test == ActionTest.NoAT
    assert games[0].timeline[44].actor == "spy"
    assert games[0].timeline[44].books == (None,)
    assert games[0].timeline[44].cast_name == (None,)
    assert games[0].timeline[44].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[44].elapsed_time == 10.0
    assert games[0].timeline[44].event == "action triggered: seduce target"
    assert games[0].timeline[44].mission == Missions.Seduce
    assert games[0].timeline[44].role == (None,)
    assert games[0].timeline[44].time == 214.9

    assert games[0].timeline[45].action_test == ActionTest.NoAT
    assert games[0].timeline[45].actor == "spy"
    assert games[0].timeline[45].books == (None,)
    assert games[0].timeline[45].cast_name == (Characters.Morgan,)
    assert games[0].timeline[45].category == TimelineCategory.NoCategory
    assert games[0].timeline[45].elapsed_time == 10.0
    assert games[0].timeline[45].event == "begin flirtation with seduction target."
    assert games[0].timeline[45].mission == Missions.Seduce
    assert games[0].timeline[45].role == (Roles.SeductionTarget,)
    assert games[0].timeline[45].time == 214.9

    assert games[0].timeline[46].action_test == ActionTest.White
    assert games[0].timeline[46].actor == "spy"
    assert games[0].timeline[46].books == (None,)
    assert games[0].timeline[46].cast_name == (None,)
    assert games[0].timeline[46].category == TimelineCategory.ActionTest
    assert games[0].timeline[46].elapsed_time == 10.94
    assert games[0].timeline[46].event == "action test white: seduce target"
    assert games[0].timeline[46].mission == Missions.Seduce
    assert games[0].timeline[46].role == (None,)
    assert games[0].timeline[46].time == 214.0

    assert games[0].timeline[47].action_test == ActionTest.NoAT
    assert games[0].timeline[47].actor == "sniper"
    assert games[0].timeline[47].books == (Books.Blue,)
    assert games[0].timeline[47].cast_name == (Characters.Disney,)
    assert (
        games[0].timeline[47].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[47].elapsed_time == 11.06
    assert games[0].timeline[47].event == "marked book."
    assert games[0].timeline[47].mission == Missions.NoMission
    assert games[0].timeline[47].role == (Roles.Civilian,)
    assert games[0].timeline[47].time == 213.9

    assert games[0].timeline[48].action_test == ActionTest.NoAT
    assert games[0].timeline[48].actor == "spy"
    assert games[0].timeline[48].books == (None,)
    assert games[0].timeline[48].cast_name == (Characters.Morgan,)
    assert games[0].timeline[48].category == TimelineCategory.MissionPartial
    assert games[0].timeline[48].elapsed_time == 12.44
    assert games[0].timeline[48].event == "flirt with seduction target: 34%"
    assert games[0].timeline[48].mission == Missions.Seduce
    assert games[0].timeline[48].role == (Roles.SeductionTarget,)
    assert games[0].timeline[48].time == 212.5

    assert games[0].timeline[49].action_test == ActionTest.NoAT
    assert games[0].timeline[49].actor == "sniper"
    assert games[0].timeline[49].books == (Books.Green,)
    assert games[0].timeline[49].cast_name == (Characters.Morgan,)
    assert (
        games[0].timeline[49].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[49].elapsed_time == 13.75
    assert games[0].timeline[49].event == "marked book."
    assert games[0].timeline[49].mission == Missions.NoMission
    assert games[0].timeline[49].role == (Roles.SeductionTarget,)
    assert games[0].timeline[49].time == 211.2

    assert games[0].timeline[50].action_test == ActionTest.NoAT
    assert games[0].timeline[50].actor == "spy"
    assert games[0].timeline[50].books == (Books.Green,)
    assert games[0].timeline[50].cast_name == (None,)
    assert games[0].timeline[50].category == TimelineCategory.Books
    assert games[0].timeline[50].elapsed_time == 15.50
    assert games[0].timeline[50].event == "get book from bookcase."
    assert games[0].timeline[50].mission == Missions.NoMission
    assert games[0].timeline[50].role == (None,)
    assert games[0].timeline[50].time == 209.4

    assert games[0].timeline[51].action_test == ActionTest.NoAT
    assert games[0].timeline[51].actor == "sniper"
    assert games[0].timeline[51].books == (None,)
    assert games[0].timeline[51].cast_name == (Characters.Rocker,)
    assert games[0].timeline[51].category == TimelineCategory.SniperLights
    assert games[0].timeline[51].elapsed_time == 20.88
    assert games[0].timeline[51].event == "marked suspicious."
    assert games[0].timeline[51].mission == Missions.NoMission
    assert games[0].timeline[51].role == (Roles.Civilian,)
    assert games[0].timeline[51].time == 204.1

    assert games[0].timeline[52].action_test == ActionTest.NoAT
    assert games[0].timeline[52].actor == "sniper"
    assert games[0].timeline[52].books == (None,)
    assert games[0].timeline[52].cast_name == (Characters.Smallman,)
    assert games[0].timeline[52].category == TimelineCategory.SniperLights
    assert games[0].timeline[52].elapsed_time == 21.25
    assert games[0].timeline[52].event == "marked suspicious."
    assert games[0].timeline[52].mission == Missions.NoMission
    assert games[0].timeline[52].role == (Roles.Civilian,)
    assert games[0].timeline[52].time == 203.7

    assert games[0].timeline[53].action_test == ActionTest.NoAT
    assert games[0].timeline[53].actor == "sniper"
    assert games[0].timeline[53].books == (None,)
    assert games[0].timeline[53].cast_name == (Characters.Sari,)
    assert games[0].timeline[53].category == TimelineCategory.SniperLights
    assert games[0].timeline[53].elapsed_time == 21.69
    assert games[0].timeline[53].event == "marked suspicious."
    assert games[0].timeline[53].mission == Missions.NoMission
    assert games[0].timeline[53].role == (Roles.Civilian,)
    assert games[0].timeline[53].time == 203.3

    assert games[0].timeline[54].action_test == ActionTest.NoAT
    assert games[0].timeline[54].actor == "spy"
    assert games[0].timeline[54].books == (None,)
    assert games[0].timeline[54].cast_name == (None,)
    assert games[0].timeline[54].category == TimelineCategory.NoCategory
    assert games[0].timeline[54].elapsed_time == 29.06
    assert games[0].timeline[54].event == "flirtation cooldown expired."
    assert games[0].timeline[54].mission == Missions.Seduce
    assert games[0].timeline[54].role == (None,)
    assert games[0].timeline[54].time == 195.9

    assert games[0].timeline[55].action_test == ActionTest.NoAT
    assert games[0].timeline[55].actor == "spy"
    assert games[0].timeline[55].books == (Books.Green, Books.Green)
    assert games[0].timeline[55].cast_name == (None,)
    assert games[0].timeline[55].category == TimelineCategory.Books
    assert games[0].timeline[55].elapsed_time == 37.13
    assert games[0].timeline[55].event == "put book in bookcase."
    assert games[0].timeline[55].mission == Missions.NoMission
    assert games[0].timeline[55].role == (None,)
    assert games[0].timeline[55].time == 187.8

    assert games[0].timeline[56].action_test == ActionTest.NoAT
    assert games[0].timeline[56].actor == "sniper"
    assert games[0].timeline[56].books == (Books.Blue,)
    assert games[0].timeline[56].cast_name == (Characters.Salmon,)
    assert (
        games[0].timeline[56].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[56].elapsed_time == 37.31
    assert games[0].timeline[56].event == "marked book."
    assert games[0].timeline[56].mission == Missions.NoMission
    assert games[0].timeline[56].role == (Roles.Civilian,)
    assert games[0].timeline[56].time == 187.6

    assert games[0].timeline[57].action_test == ActionTest.NoAT
    assert games[0].timeline[57].actor == "sniper"
    assert games[0].timeline[57].books == (None,)
    assert games[0].timeline[57].cast_name == (Characters.Helen,)
    assert games[0].timeline[57].category == TimelineCategory.SniperLights
    assert games[0].timeline[57].elapsed_time == 40.06
    assert games[0].timeline[57].event == "marked suspicious."
    assert games[0].timeline[57].mission == Missions.NoMission
    assert games[0].timeline[57].role == (Roles.Civilian,)
    assert games[0].timeline[57].time == 184.9

    assert games[0].timeline[58].action_test == ActionTest.NoAT
    assert games[0].timeline[58].actor == "spy"
    assert games[0].timeline[58].books == (None,)
    assert games[0].timeline[58].cast_name == (None,)
    assert games[0].timeline[58].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[58].elapsed_time == 41.00
    assert games[0].timeline[58].event == "action triggered: bug ambassador"
    assert games[0].timeline[58].mission == Missions.Bug
    assert games[0].timeline[58].role == (None,)
    assert games[0].timeline[58].time == 183.9

    assert games[0].timeline[59].action_test == ActionTest.NoAT
    assert games[0].timeline[59].actor == "spy"
    assert games[0].timeline[59].books == (None,)
    assert games[0].timeline[59].cast_name == (Characters.Carlos,)
    assert games[0].timeline[59].category == TimelineCategory.NoCategory
    assert games[0].timeline[59].elapsed_time == 41.00
    assert games[0].timeline[59].event == "begin planting bug while walking."
    assert games[0].timeline[59].mission == Missions.Bug
    assert games[0].timeline[59].role == (Roles.Ambassador,)
    assert games[0].timeline[59].time == 183.9

    assert games[0].timeline[60].action_test == ActionTest.NoAT
    assert games[0].timeline[60].actor == "spy"
    assert games[0].timeline[60].books == (None,)
    assert games[0].timeline[60].cast_name == (Characters.Carlos,)
    assert games[0].timeline[60].category == TimelineCategory.MissionComplete
    assert games[0].timeline[60].elapsed_time == 41.94
    assert games[0].timeline[60].event == "bugged ambassador while walking."
    assert games[0].timeline[60].mission == Missions.Bug
    assert games[0].timeline[60].role == (Roles.Ambassador,)
    assert games[0].timeline[60].time == 183.0

    assert games[0].timeline[61].action_test == ActionTest.NoAT
    assert games[0].timeline[61].actor == "sniper"
    assert games[0].timeline[61].books == (None,)
    assert games[0].timeline[61].cast_name == (Characters.Irish,)
    assert games[0].timeline[61].category == TimelineCategory.SniperLights
    assert games[0].timeline[61].elapsed_time == 46.75
    assert games[0].timeline[61].event == "marked spy suspicious."
    assert games[0].timeline[61].mission == Missions.NoMission
    assert games[0].timeline[61].role == (Roles.Spy,)
    assert games[0].timeline[61].time == 178.2

    assert games[0].timeline[62].action_test == ActionTest.NoAT
    assert games[0].timeline[62].actor == "spy"
    assert games[0].timeline[62].books == (None,)
    assert games[0].timeline[62].cast_name == (None,)
    assert games[0].timeline[62].category == TimelineCategory.Conversation
    assert games[0].timeline[62].elapsed_time == 54.56
    assert games[0].timeline[62].event == "spy enters conversation."
    assert games[0].timeline[62].mission == Missions.NoMission
    assert games[0].timeline[62].role == (None,)
    assert games[0].timeline[62].time == 170.4

    assert games[0].timeline[63].action_test == ActionTest.NoAT
    assert games[0].timeline[63].actor == "spy"
    assert games[0].timeline[63].books == (None,)
    assert games[0].timeline[63].cast_name == (None,)
    assert games[0].timeline[63].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[63].elapsed_time == 59.75
    assert games[0].timeline[63].event == "action triggered: seduce target"
    assert games[0].timeline[63].mission == Missions.Seduce
    assert games[0].timeline[63].role == (None,)
    assert games[0].timeline[63].time == 165.2

    assert games[0].timeline[64].action_test == ActionTest.NoAT
    assert games[0].timeline[64].actor == "spy"
    assert games[0].timeline[64].books == (None,)
    assert games[0].timeline[64].cast_name == (Characters.Morgan,)
    assert games[0].timeline[64].category == TimelineCategory.NoCategory
    assert games[0].timeline[64].elapsed_time == 59.75
    assert games[0].timeline[64].event == "begin flirtation with seduction target."
    assert games[0].timeline[64].mission == Missions.Seduce
    assert games[0].timeline[64].role == (Roles.SeductionTarget,)
    assert games[0].timeline[64].time == 165.2

    assert games[0].timeline[65].action_test == ActionTest.White
    assert games[0].timeline[65].actor == "spy"
    assert games[0].timeline[65].books == (None,)
    assert games[0].timeline[65].cast_name == (None,)
    assert games[0].timeline[65].category == TimelineCategory.ActionTest
    assert games[0].timeline[65].elapsed_time == 60.56
    assert games[0].timeline[65].event == "action test white: seduce target"
    assert games[0].timeline[65].mission == Missions.Seduce
    assert games[0].timeline[65].role == (None,)
    assert games[0].timeline[65].time == 164.4

    assert games[0].timeline[66].action_test == ActionTest.NoAT
    assert games[0].timeline[66].actor == "spy"
    assert games[0].timeline[66].books == (None,)
    assert games[0].timeline[66].cast_name == (Characters.Morgan,)
    assert games[0].timeline[66].category == TimelineCategory.MissionPartial
    assert games[0].timeline[66].elapsed_time == 60.56
    assert games[0].timeline[66].event == "flirt with seduction target: 68%"
    assert games[0].timeline[66].mission == Missions.Seduce
    assert games[0].timeline[66].role == (Roles.SeductionTarget,)
    assert games[0].timeline[66].time == 164.4

    assert games[0].timeline[67].action_test == ActionTest.NoAT
    assert games[0].timeline[67].actor == "sniper"
    assert games[0].timeline[67].books == (None,)
    assert games[0].timeline[67].cast_name == (Characters.Oprah,)
    assert games[0].timeline[67].category == TimelineCategory.SniperLights
    assert games[0].timeline[67].elapsed_time == 89.81
    assert games[0].timeline[67].event == "marked suspicious."
    assert games[0].timeline[67].mission == Missions.NoMission
    assert games[0].timeline[67].role == (Roles.Civilian,)
    assert games[0].timeline[67].time == 135.1

    assert games[0].timeline[68].action_test == ActionTest.NoAT
    assert games[0].timeline[68].actor == "spy"
    assert games[0].timeline[68].books == (None,)
    assert games[0].timeline[68].cast_name == (None,)
    assert games[0].timeline[68].category == TimelineCategory.NoCategory
    assert games[0].timeline[68].elapsed_time == 105.63
    assert games[0].timeline[68].event == "flirtation cooldown expired."
    assert games[0].timeline[68].mission == Missions.Seduce
    assert games[0].timeline[68].role == (None,)
    assert games[0].timeline[68].time == 119.3

    assert games[0].timeline[69].action_test == ActionTest.NoAT
    assert games[0].timeline[69].actor == "spy"
    assert games[0].timeline[69].books == (None,)
    assert games[0].timeline[69].cast_name == (None,)
    assert games[0].timeline[69].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[69].elapsed_time == 106.19
    assert games[0].timeline[69].event == "action triggered: seduce target"
    assert games[0].timeline[69].mission == Missions.Seduce
    assert games[0].timeline[69].role == (None,)
    assert games[0].timeline[69].time == 118.8

    assert games[0].timeline[70].action_test == ActionTest.NoAT
    assert games[0].timeline[70].actor == "spy"
    assert games[0].timeline[70].books == (None,)
    assert games[0].timeline[70].cast_name == (Characters.Morgan,)
    assert games[0].timeline[70].category == TimelineCategory.NoCategory
    assert games[0].timeline[70].elapsed_time == 106.19
    assert games[0].timeline[70].event == "begin flirtation with seduction target."
    assert games[0].timeline[70].mission == Missions.Seduce
    assert games[0].timeline[70].role == (Roles.SeductionTarget,)
    assert games[0].timeline[70].time == 118.8

    assert games[0].timeline[71].action_test == ActionTest.White
    assert games[0].timeline[71].actor == "spy"
    assert games[0].timeline[71].books == (None,)
    assert games[0].timeline[71].cast_name == (None,)
    assert games[0].timeline[71].category == TimelineCategory.ActionTest
    assert games[0].timeline[71].elapsed_time == 107.13
    assert games[0].timeline[71].event == "action test white: seduce target"
    assert games[0].timeline[71].mission == Missions.Seduce
    assert games[0].timeline[71].role == (None,)
    assert games[0].timeline[71].time == 117.8

    assert games[0].timeline[72].action_test == ActionTest.NoAT
    assert games[0].timeline[72].actor == "spy"
    assert games[0].timeline[72].books == (None,)
    assert games[0].timeline[72].cast_name == (Characters.Morgan,)
    assert games[0].timeline[72].category == TimelineCategory.MissionPartial
    assert games[0].timeline[72].elapsed_time == 107.13
    assert games[0].timeline[72].event == "flirt with seduction target: 100%"
    assert games[0].timeline[72].mission == Missions.Seduce
    assert games[0].timeline[72].role == (Roles.SeductionTarget,)
    assert games[0].timeline[72].time == 117.8

    assert games[0].timeline[73].action_test == ActionTest.NoAT
    assert games[0].timeline[73].actor == "spy"
    assert games[0].timeline[73].books == (None,)
    assert games[0].timeline[73].cast_name == (Characters.Morgan,)
    assert games[0].timeline[73].category == TimelineCategory.MissionComplete
    assert games[0].timeline[73].elapsed_time == 107.13
    assert games[0].timeline[73].event == "target seduced."
    assert games[0].timeline[73].mission == Missions.Seduce
    assert games[0].timeline[73].role == (Roles.SeductionTarget,)
    assert games[0].timeline[73].time == 117.8

    assert games[0].timeline[74].action_test == ActionTest.NoAT
    assert games[0].timeline[74].actor == "spy"
    assert games[0].timeline[74].books == (None,)
    assert games[0].timeline[74].cast_name == (None,)
    assert games[0].timeline[74].category == TimelineCategory.Conversation
    assert games[0].timeline[74].elapsed_time == 123.56
    assert games[0].timeline[74].event == "spy leaves conversation."
    assert games[0].timeline[74].mission == Missions.NoMission
    assert games[0].timeline[74].role == (None,)
    assert games[0].timeline[74].time == 101.4

    assert games[0].timeline[75].action_test == ActionTest.NoAT
    assert games[0].timeline[75].actor == "sniper"
    assert games[0].timeline[75].books == (Books.Blue,)
    assert games[0].timeline[75].cast_name == (Characters.General,)
    assert (
        games[0].timeline[75].category
        == TimelineCategory.SniperLights | TimelineCategory.Books
    )
    assert games[0].timeline[75].elapsed_time == 126.31
    assert games[0].timeline[75].event == "marked book."
    assert games[0].timeline[75].mission == Missions.NoMission
    assert games[0].timeline[75].role == (Roles.Civilian,)
    assert games[0].timeline[75].time == 98.6

    assert games[0].timeline[76].action_test == ActionTest.NoAT
    assert games[0].timeline[76].actor == "sniper"
    assert games[0].timeline[76].books == (None,)
    assert games[0].timeline[76].cast_name == (Characters.Plain,)
    assert games[0].timeline[76].category == TimelineCategory.SniperLights
    assert games[0].timeline[76].elapsed_time == 128.75
    assert games[0].timeline[76].event == "marked suspicious."
    assert games[0].timeline[76].mission == Missions.NoMission
    assert games[0].timeline[76].role == (Roles.Civilian,)
    assert games[0].timeline[76].time == 96.2

    assert games[0].timeline[77].action_test == ActionTest.NoAT
    assert games[0].timeline[77].actor == "spy"
    assert games[0].timeline[77].books == (None,)
    assert games[0].timeline[77].cast_name == (Characters.Irish,)
    assert games[0].timeline[77].category == TimelineCategory.Drinks
    assert games[0].timeline[77].elapsed_time == 139.44
    assert games[0].timeline[77].event == "waiter offered drink."
    assert games[0].timeline[77].mission == Missions.NoMission
    assert games[0].timeline[77].role == (Roles.Spy,)
    assert games[0].timeline[77].time == 85.5

    assert games[0].timeline[78].action_test == ActionTest.NoAT
    assert games[0].timeline[78].actor == "spy"
    assert games[0].timeline[78].books == (None,)
    assert games[0].timeline[78].cast_name == (Characters.Irish,)
    assert games[0].timeline[78].category == TimelineCategory.Drinks
    assert games[0].timeline[78].elapsed_time == 142.94
    assert games[0].timeline[78].event == "rejected drink from waiter."
    assert games[0].timeline[78].mission == Missions.NoMission
    assert games[0].timeline[78].role == (Roles.Spy,)
    assert games[0].timeline[78].time == 82.0

    assert games[0].timeline[79].action_test == ActionTest.NoAT
    assert games[0].timeline[79].actor == "spy"
    assert games[0].timeline[79].books == (None,)
    assert games[0].timeline[79].cast_name == (Characters.Irish,)
    assert games[0].timeline[79].category == TimelineCategory.Drinks
    assert games[0].timeline[79].elapsed_time == 142.94
    assert games[0].timeline[79].event == "waiter stopped offering drink."
    assert games[0].timeline[79].mission == Missions.NoMission
    assert games[0].timeline[79].role == (Roles.Spy,)
    assert games[0].timeline[79].time == 82.0

    assert games[0].timeline[80].action_test == ActionTest.NoAT
    assert games[0].timeline[80].actor == "spy"
    assert games[0].timeline[80].books == (None,)
    assert games[0].timeline[80].cast_name == (None,)
    assert games[0].timeline[80].category == TimelineCategory.Statues
    assert games[0].timeline[80].elapsed_time == 150.63
    assert games[0].timeline[80].event == "picked up statue."
    assert games[0].timeline[80].mission == Missions.NoMission
    assert games[0].timeline[80].role == (None,)
    assert games[0].timeline[80].time == 74.3

    assert games[0].timeline[81].action_test == ActionTest.NoAT
    assert games[0].timeline[81].actor == "spy"
    assert games[0].timeline[81].books == (None,)
    assert games[0].timeline[81].cast_name == (None,)
    assert games[0].timeline[81].category == TimelineCategory.Statues
    assert games[0].timeline[81].elapsed_time == 153.25
    assert games[0].timeline[81].event == "picked up fingerprintable statue."
    assert games[0].timeline[81].mission == Missions.Fingerprint
    assert games[0].timeline[81].role == (None,)
    assert games[0].timeline[81].time == 71.7

    assert games[0].timeline[82].action_test == ActionTest.NoAT
    assert games[0].timeline[82].actor == "spy"
    assert games[0].timeline[82].books == (None,)
    assert games[0].timeline[82].cast_name == (None,)
    assert (
        games[0].timeline[82].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[0].timeline[82].elapsed_time == 153.63
    assert games[0].timeline[82].event == "action triggered: inspect statues"
    assert games[0].timeline[82].mission == Missions.Inspect
    assert games[0].timeline[82].role == (None,)
    assert games[0].timeline[82].time == 71.3

    assert games[0].timeline[83].action_test == ActionTest.White
    assert games[0].timeline[83].actor == "spy"
    assert games[0].timeline[83].books == (None,)
    assert games[0].timeline[83].cast_name == (None,)
    assert (
        games[0].timeline[83].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[0].timeline[83].elapsed_time == 154.81
    assert games[0].timeline[83].event == "action test white: inspect statues"
    assert games[0].timeline[83].mission == Missions.Inspect
    assert games[0].timeline[83].role == (None,)
    assert games[0].timeline[83].time == 70.1

    assert games[0].timeline[84].action_test == ActionTest.NoAT
    assert games[0].timeline[84].actor == "spy"
    assert games[0].timeline[84].books == (None,)
    assert games[0].timeline[84].cast_name == (None,)
    assert (
        games[0].timeline[84].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[0].timeline[84].elapsed_time == 158.63
    assert games[0].timeline[84].event == "left statue inspected."
    assert games[0].timeline[84].mission == Missions.Inspect
    assert games[0].timeline[84].role == (None,)
    assert games[0].timeline[84].time == 66.3

    assert games[0].timeline[85].action_test == ActionTest.NoAT
    assert games[0].timeline[85].actor == "spy"
    assert games[0].timeline[85].books == (None,)
    assert games[0].timeline[85].cast_name == (None,)
    assert (
        games[0].timeline[85].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Statues
    )
    assert games[0].timeline[85].elapsed_time == 159.00
    assert games[0].timeline[85].event == "action triggered: inspect statues"
    assert games[0].timeline[85].mission == Missions.Inspect
    assert games[0].timeline[85].role == (None,)
    assert games[0].timeline[85].time == 66.0

    assert games[0].timeline[86].action_test == ActionTest.Green
    assert games[0].timeline[86].actor == "spy"
    assert games[0].timeline[86].books == (None,)
    assert games[0].timeline[86].cast_name == (None,)
    assert (
        games[0].timeline[86].category
        == TimelineCategory.ActionTest | TimelineCategory.Statues
    )
    assert games[0].timeline[86].elapsed_time == 160.13
    assert games[0].timeline[86].event == "action test green: inspect statues"
    assert games[0].timeline[86].mission == Missions.Inspect
    assert games[0].timeline[86].role == (None,)
    assert games[0].timeline[86].time == 64.8

    assert games[0].timeline[87].action_test == ActionTest.NoAT
    assert games[0].timeline[87].actor == "spy"
    assert games[0].timeline[87].books == (None,)
    assert games[0].timeline[87].cast_name == (None,)
    assert (
        games[0].timeline[87].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[0].timeline[87].elapsed_time == 161.50
    assert games[0].timeline[87].event == "held statue inspected."
    assert games[0].timeline[87].mission == Missions.Inspect
    assert games[0].timeline[87].role == (None,)
    assert games[0].timeline[87].time == 63.4

    assert games[0].timeline[88].action_test == ActionTest.NoAT
    assert games[0].timeline[88].actor == "spy"
    assert games[0].timeline[88].books == (None,)
    assert games[0].timeline[88].cast_name == (None,)
    assert games[0].timeline[88].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[88].elapsed_time == 162.00
    assert games[0].timeline[88].event == "action triggered: fingerprint ambassador"
    assert games[0].timeline[88].mission == Missions.Fingerprint
    assert games[0].timeline[88].role == (None,)
    assert games[0].timeline[88].time == 62.9

    assert games[0].timeline[89].action_test == ActionTest.NoAT
    assert games[0].timeline[89].actor == "spy"
    assert games[0].timeline[89].books == (None,)
    assert games[0].timeline[89].cast_name == (None,)
    assert games[0].timeline[89].category == TimelineCategory.Statues
    assert games[0].timeline[89].elapsed_time == 162.00
    assert games[0].timeline[89].event == "started fingerprinting statue."
    assert games[0].timeline[89].mission == Missions.Fingerprint
    assert games[0].timeline[89].role == (None,)
    assert games[0].timeline[89].time == 62.9

    assert games[0].timeline[90].action_test == ActionTest.NoAT
    assert games[0].timeline[90].actor == "spy"
    assert games[0].timeline[90].books == (None,)
    assert games[0].timeline[90].cast_name == (None,)
    assert (
        games[0].timeline[90].category
        == TimelineCategory.MissionPartial | TimelineCategory.Statues
    )
    assert games[0].timeline[90].elapsed_time == 163.00
    assert games[0].timeline[90].event == "fingerprinted statue."
    assert games[0].timeline[90].mission == Missions.Fingerprint
    assert games[0].timeline[90].role == (None,)
    assert games[0].timeline[90].time == 61.9

    assert games[0].timeline[91].action_test == ActionTest.NoAT
    assert games[0].timeline[91].actor == "spy"
    assert games[0].timeline[91].books == (None,)
    assert games[0].timeline[91].cast_name == (None,)
    assert games[0].timeline[91].category == TimelineCategory.Statues
    assert games[0].timeline[91].elapsed_time == 164.00
    assert games[0].timeline[91].event == "put back statue."
    assert games[0].timeline[91].mission == Missions.NoMission
    assert games[0].timeline[91].role == (None,)
    assert games[0].timeline[91].time == 60.9

    assert games[0].timeline[92].action_test == ActionTest.NoAT
    assert games[0].timeline[92].actor == "spy"
    assert games[0].timeline[92].books == (None,)
    assert games[0].timeline[92].cast_name == (Characters.Irish,)
    assert games[0].timeline[92].category == TimelineCategory.Drinks
    assert games[0].timeline[92].elapsed_time == 172.19
    assert games[0].timeline[92].event == "waiter offered drink."
    assert games[0].timeline[92].mission == Missions.NoMission
    assert games[0].timeline[92].role == (Roles.Spy,)
    assert games[0].timeline[92].time == 52.8

    assert games[0].timeline[93].action_test == ActionTest.NoAT
    assert games[0].timeline[93].actor == "spy"
    assert games[0].timeline[93].books == (None,)
    assert games[0].timeline[93].cast_name == (Characters.Irish,)
    assert games[0].timeline[93].category == TimelineCategory.Drinks
    assert games[0].timeline[93].elapsed_time == 176.69
    assert games[0].timeline[93].event == "rejected drink from waiter."
    assert games[0].timeline[93].mission == Missions.NoMission
    assert games[0].timeline[93].role == (Roles.Spy,)
    assert games[0].timeline[93].time == 48.3

    assert games[0].timeline[94].action_test == ActionTest.NoAT
    assert games[0].timeline[94].actor == "spy"
    assert games[0].timeline[94].books == (None,)
    assert games[0].timeline[94].cast_name == (Characters.Irish,)
    assert games[0].timeline[94].category == TimelineCategory.Drinks
    assert games[0].timeline[94].elapsed_time == 176.69
    assert games[0].timeline[94].event == "waiter stopped offering drink."
    assert games[0].timeline[94].mission == Missions.NoMission
    assert games[0].timeline[94].role == (Roles.Spy,)
    assert games[0].timeline[94].time == 48.3

    assert games[0].timeline[95].action_test == ActionTest.NoAT
    assert games[0].timeline[95].actor == "sniper"
    assert games[0].timeline[95].books == (None,)
    assert games[0].timeline[95].cast_name == (Characters.Duke,)
    assert games[0].timeline[95].category == TimelineCategory.SniperLights
    assert games[0].timeline[95].elapsed_time == 181.00
    assert games[0].timeline[95].event == "marked less suspicious."
    assert games[0].timeline[95].mission == Missions.NoMission
    assert games[0].timeline[95].role == (Roles.Civilian,)
    assert games[0].timeline[95].time == 44.0

    assert games[0].timeline[96].action_test == ActionTest.NoAT
    assert games[0].timeline[96].actor == "sniper"
    assert games[0].timeline[96].books == (None,)
    assert games[0].timeline[96].cast_name == (Characters.Teal,)
    assert games[0].timeline[96].category == TimelineCategory.SniperLights
    assert games[0].timeline[96].elapsed_time == 198.56
    assert games[0].timeline[96].event == "marked suspicious."
    assert games[0].timeline[96].mission == Missions.NoMission
    assert games[0].timeline[96].role == (Roles.Civilian,)
    assert games[0].timeline[96].time == 26.4

    assert games[0].timeline[97].action_test == ActionTest.NoAT
    assert games[0].timeline[97].actor == "spy"
    assert games[0].timeline[97].books == (Books.Blue,)
    assert games[0].timeline[97].cast_name == (None,)
    assert games[0].timeline[97].category == TimelineCategory.Books
    assert games[0].timeline[97].elapsed_time == 202.06
    assert games[0].timeline[97].event == "get book from bookcase."
    assert games[0].timeline[97].mission == Missions.NoMission
    assert games[0].timeline[97].role == (None,)
    assert games[0].timeline[97].time == 22.9

    assert games[0].timeline[98].action_test == ActionTest.NoAT
    assert games[0].timeline[98].actor == "spy"
    assert games[0].timeline[98].books == (None,)
    assert games[0].timeline[98].cast_name == (None,)
    assert games[0].timeline[98].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[98].elapsed_time == 202.56
    assert games[0].timeline[98].event == "action triggered: fingerprint ambassador"
    assert games[0].timeline[98].mission == Missions.Fingerprint
    assert games[0].timeline[98].role == (None,)
    assert games[0].timeline[98].time == 22.4

    assert games[0].timeline[99].action_test == ActionTest.NoAT
    assert games[0].timeline[99].actor == "spy"
    assert games[0].timeline[99].books == (None,)
    assert games[0].timeline[99].cast_name == (None,)
    assert games[0].timeline[99].category == TimelineCategory.Books
    assert games[0].timeline[99].elapsed_time == 202.56
    assert games[0].timeline[99].event == "started fingerprinting book."
    assert games[0].timeline[99].mission == Missions.Fingerprint
    assert games[0].timeline[99].role == (None,)
    assert games[0].timeline[99].time == 22.4

    assert games[0].timeline[100].action_test == ActionTest.Red
    assert games[0].timeline[100].actor == "spy"
    assert games[0].timeline[100].books == (None,)
    assert games[0].timeline[100].cast_name == (None,)
    assert games[0].timeline[100].category == TimelineCategory.ActionTest
    assert games[0].timeline[100].elapsed_time == 203.56
    assert games[0].timeline[100].event == "action test red: fingerprint ambassador"
    assert games[0].timeline[100].mission == Missions.Fingerprint
    assert games[0].timeline[100].role == (None,)
    assert games[0].timeline[100].time == 21.4

    assert games[0].timeline[101].action_test == ActionTest.NoAT
    assert games[0].timeline[101].actor == "spy"
    assert games[0].timeline[101].books == (None,)
    assert games[0].timeline[101].cast_name == (None,)
    assert games[0].timeline[101].category == TimelineCategory.NoCategory
    assert games[0].timeline[101].elapsed_time == 203.56
    assert games[0].timeline[101].event == "fingerprinting failed."
    assert games[0].timeline[101].mission == Missions.Fingerprint
    assert games[0].timeline[101].role == (None,)
    assert games[0].timeline[101].time == 21.4

    assert games[0].timeline[102].action_test == ActionTest.NoAT
    assert games[0].timeline[102].actor == "spy"
    assert games[0].timeline[102].books == (None,)
    assert games[0].timeline[102].cast_name == (None,)
    assert games[0].timeline[102].category == TimelineCategory.Conversation
    assert games[0].timeline[102].elapsed_time == 207.31
    assert games[0].timeline[102].event == "spy enters conversation."
    assert games[0].timeline[102].mission == Missions.NoMission
    assert games[0].timeline[102].role == (None,)
    assert games[0].timeline[102].time == 17.6

    assert games[0].timeline[103].action_test == ActionTest.NoAT
    assert games[0].timeline[103].actor == "spy"
    assert games[0].timeline[103].books == (None,)
    assert games[0].timeline[103].cast_name == (Characters.Boots,)
    assert games[0].timeline[103].category == TimelineCategory.Conversation
    assert games[0].timeline[103].elapsed_time == 207.31
    assert games[0].timeline[103].event == "spy joined conversation with double agent."
    assert games[0].timeline[103].mission == Missions.NoMission
    assert games[0].timeline[103].role == (Roles.DoubleAgent,)
    assert games[0].timeline[103].time == 17.6

    assert games[0].timeline[104].action_test == ActionTest.NoAT
    assert games[0].timeline[104].actor == "spy"
    assert games[0].timeline[104].books == (None,)
    assert games[0].timeline[104].cast_name == (None,)
    assert games[0].timeline[104].category == TimelineCategory.ActionTriggered
    assert games[0].timeline[104].elapsed_time == 207.63
    assert games[0].timeline[104].event == "action triggered: contact double agent"
    assert games[0].timeline[104].mission == Missions.Contact
    assert games[0].timeline[104].role == (None,)
    assert games[0].timeline[104].time == 17.3

    assert games[0].timeline[105].action_test == ActionTest.NoAT
    assert games[0].timeline[105].actor == "spy"
    assert games[0].timeline[105].books == (None,)
    assert games[0].timeline[105].cast_name == (None,)
    assert games[0].timeline[105].category == TimelineCategory.BananaBread
    assert games[0].timeline[105].elapsed_time == 207.63
    assert games[0].timeline[105].event == "real banana bread started."
    assert games[0].timeline[105].mission == Missions.Contact
    assert games[0].timeline[105].role == (None,)
    assert games[0].timeline[105].time == 17.3

    assert games[0].timeline[106].action_test == ActionTest.White
    assert games[0].timeline[106].actor == "spy"
    assert games[0].timeline[106].books == (None,)
    assert games[0].timeline[106].cast_name == (None,)
    assert games[0].timeline[106].category == TimelineCategory.ActionTest
    assert games[0].timeline[106].elapsed_time == 208.44
    assert games[0].timeline[106].event == "action test white: contact double agent"
    assert games[0].timeline[106].mission == Missions.Contact
    assert games[0].timeline[106].role == (None,)
    assert games[0].timeline[106].time == 16.5

    assert games[0].timeline[107].action_test == ActionTest.NoAT
    assert games[0].timeline[107].actor == "spy"
    assert games[0].timeline[107].books == (None,)
    assert games[0].timeline[107].cast_name == (None,)
    assert games[0].timeline[107].category == TimelineCategory.BananaBread
    assert games[0].timeline[107].elapsed_time == 210.25
    assert games[0].timeline[107].event == "banana bread uttered."
    assert games[0].timeline[107].mission == Missions.Contact
    assert games[0].timeline[107].role == (None,)
    assert games[0].timeline[107].time == 14.7

    assert games[0].timeline[108].action_test == ActionTest.NoAT
    assert games[0].timeline[108].actor == "spy"
    assert games[0].timeline[108].books == (None,)
    assert games[0].timeline[108].cast_name == (Characters.Boots,)
    assert games[0].timeline[108].category == TimelineCategory.MissionComplete
    assert games[0].timeline[108].elapsed_time == 210.81
    assert games[0].timeline[108].event == "double agent contacted."
    assert games[0].timeline[108].mission == Missions.Contact
    assert games[0].timeline[108].role == (Roles.DoubleAgent,)
    assert games[0].timeline[108].time == 14.1

    assert games[0].timeline[109].action_test == ActionTest.NoAT
    assert games[0].timeline[109].actor == "sniper"
    assert games[0].timeline[109].books == (None,)
    assert games[0].timeline[109].cast_name == (Characters.Sari,)
    assert games[0].timeline[109].category == TimelineCategory.SniperLights
    assert games[0].timeline[109].elapsed_time == 213.50
    assert games[0].timeline[109].event == "marked less suspicious."
    assert games[0].timeline[109].mission == Missions.NoMission
    assert games[0].timeline[109].role == (Roles.Civilian,)
    assert games[0].timeline[109].time == 11.5

    assert games[0].timeline[110].action_test == ActionTest.NoAT
    assert games[0].timeline[110].actor == "sniper"
    assert games[0].timeline[110].books == (None,)
    assert games[0].timeline[110].cast_name == (Characters.Smallman,)
    assert games[0].timeline[110].category == TimelineCategory.SniperLights
    assert games[0].timeline[110].elapsed_time == 213.81
    assert games[0].timeline[110].event == "marked less suspicious."
    assert games[0].timeline[110].mission == Missions.NoMission
    assert games[0].timeline[110].role == (Roles.Civilian,)
    assert games[0].timeline[110].time == 11.1

    assert games[0].timeline[111].action_test == ActionTest.NoAT
    assert games[0].timeline[111].actor == "sniper"
    assert games[0].timeline[111].books == (None,)
    assert games[0].timeline[111].cast_name == (Characters.Bling,)
    assert games[0].timeline[111].category == TimelineCategory.SniperLights
    assert games[0].timeline[111].elapsed_time == 214.25
    assert games[0].timeline[111].event == "marked less suspicious."
    assert games[0].timeline[111].mission == Missions.NoMission
    assert games[0].timeline[111].role == (Roles.Civilian,)
    assert games[0].timeline[111].time == 10.7

    assert games[0].timeline[112].action_test == ActionTest.NoAT
    assert games[0].timeline[112].actor == "sniper"
    assert games[0].timeline[112].books == (None,)
    assert games[0].timeline[112].cast_name == (Characters.Disney,)
    assert games[0].timeline[112].category == TimelineCategory.SniperLights
    assert games[0].timeline[112].elapsed_time == 216.0
    assert games[0].timeline[112].event == "marked less suspicious."
    assert games[0].timeline[112].mission == Missions.NoMission
    assert games[0].timeline[112].role == (Roles.Civilian,)
    assert games[0].timeline[112].time == 9.0

    assert games[0].timeline[113].action_test == ActionTest.NoAT
    assert games[0].timeline[113].actor == "sniper"
    assert games[0].timeline[113].books == (None,)
    assert games[0].timeline[113].cast_name == (Characters.Salmon,)
    assert games[0].timeline[113].category == TimelineCategory.SniperLights
    assert games[0].timeline[113].elapsed_time == 216.38
    assert games[0].timeline[113].event == "marked less suspicious."
    assert games[0].timeline[113].mission == Missions.NoMission
    assert games[0].timeline[113].role == (Roles.Civilian,)
    assert games[0].timeline[113].time == 8.6

    assert games[0].timeline[114].action_test == ActionTest.NoAT
    assert games[0].timeline[114].actor == "sniper"
    assert games[0].timeline[114].books == (None,)
    assert games[0].timeline[114].cast_name == (Characters.Rocker,)
    assert games[0].timeline[114].category == TimelineCategory.SniperLights
    assert games[0].timeline[114].elapsed_time == 216.69
    assert games[0].timeline[114].event == "marked less suspicious."
    assert games[0].timeline[114].mission == Missions.NoMission
    assert games[0].timeline[114].role == (Roles.Civilian,)
    assert games[0].timeline[114].time == 8.3

    assert games[0].timeline[115].action_test == ActionTest.NoAT
    assert games[0].timeline[115].actor == "spy"
    assert games[0].timeline[115].books == (None,)
    assert games[0].timeline[115].cast_name == (None,)
    assert games[0].timeline[115].category == TimelineCategory.Conversation
    assert games[0].timeline[115].elapsed_time == 217.50
    assert games[0].timeline[115].event == "spy leaves conversation."
    assert games[0].timeline[115].mission == Missions.NoMission
    assert games[0].timeline[115].role == (None,)
    assert games[0].timeline[115].time == 7.5

    assert games[0].timeline[116].action_test == ActionTest.NoAT
    assert games[0].timeline[116].actor == "spy"
    assert games[0].timeline[116].books == (None,)
    assert games[0].timeline[116].cast_name == (Characters.Boots,)
    assert games[0].timeline[116].category == TimelineCategory.Conversation
    assert games[0].timeline[116].elapsed_time == 217.50
    assert games[0].timeline[116].event == "spy left conversation with double agent."
    assert games[0].timeline[116].mission == Missions.NoMission
    assert games[0].timeline[116].role == (Roles.DoubleAgent,)
    assert games[0].timeline[116].time == 7.5

    assert games[0].timeline[117].action_test == ActionTest.NoAT
    assert games[0].timeline[117].actor == "sniper"
    assert games[0].timeline[117].books == (None,)
    assert games[0].timeline[117].cast_name == (Characters.Irish,)
    assert games[0].timeline[117].category == TimelineCategory.SniperShot
    assert games[0].timeline[117].elapsed_time == 220.25
    assert games[0].timeline[117].event == "took shot."
    assert games[0].timeline[117].mission == Missions.NoMission
    assert games[0].timeline[117].role == (Roles.Spy,)
    assert games[0].timeline[117].time == 4.7

    assert games[0].timeline[118].action_test == ActionTest.NoAT
    assert games[0].timeline[118].actor == "game"
    assert games[0].timeline[118].books == (None,)
    assert games[0].timeline[118].cast_name == (Characters.Irish,)
    assert games[0].timeline[118].category == TimelineCategory.GameEnd
    assert games[0].timeline[118].elapsed_time == 223.81
    assert games[0].timeline[118].event == "sniper shot spy."
    assert games[0].timeline[118].mission == Missions.NoMission
    assert games[0].timeline[118].role == (Roles.Spy,)
    assert games[0].timeline[118].time == 1.1

    assert games[0].timeline.get_next_spy_action(games[0].timeline[118]) is None

    assert games[1].uuid == "vgAlD77AQw2XKTZq3H4NTg"
    assert games[1].timeline[0].action_test == ActionTest.NoAT
    assert games[1].timeline[0].actor == "spy"
    assert games[1].timeline[0].books == (None,)
    assert games[1].timeline[0].cast_name == (Characters.Queen,)
    assert games[1].timeline[0].category == TimelineCategory.Cast
    assert games[1].timeline[0].elapsed_time == 0.0
    assert games[1].timeline[0].event == "spy cast."
    assert games[1].timeline[0].mission == Missions.NoMission
    assert games[1].timeline[0].role == (Roles.Spy,)
    assert games[1].timeline[0].time == 225.0

    assert games[1].timeline[1].action_test == ActionTest.NoAT
    assert games[1].timeline[1].actor == "spy"
    assert games[1].timeline[1].books == (None,)
    assert games[1].timeline[1].cast_name == (Characters.Disney,)
    assert games[1].timeline[1].category == TimelineCategory.Cast
    assert games[1].timeline[1].elapsed_time == 0.0
    assert games[1].timeline[1].event == "ambassador cast."
    assert games[1].timeline[1].mission == Missions.NoMission
    assert games[1].timeline[1].role == (Roles.Ambassador,)
    assert games[1].timeline[1].time == 225.0

    assert games[1].timeline[2].action_test == ActionTest.NoAT
    assert games[1].timeline[2].actor == "spy"
    assert games[1].timeline[2].books == (None,)
    assert games[1].timeline[2].cast_name == (Characters.Wheels,)
    assert games[1].timeline[2].category == TimelineCategory.Cast
    assert games[1].timeline[2].elapsed_time == 0.0
    assert games[1].timeline[2].event == "double agent cast."
    assert games[1].timeline[2].mission == Missions.NoMission
    assert games[1].timeline[2].role == (Roles.DoubleAgent,)
    assert games[1].timeline[2].time == 225.0

    assert games[1].timeline[3].action_test == ActionTest.NoAT
    assert games[1].timeline[3].actor == "spy"
    assert games[1].timeline[3].books == (None,)
    assert games[1].timeline[3].cast_name == (Characters.Bling,)
    assert games[1].timeline[3].category == TimelineCategory.Cast
    assert games[1].timeline[3].elapsed_time == 0.0
    assert games[1].timeline[3].event == "suspected double agent cast."
    assert games[1].timeline[3].mission == Missions.NoMission
    assert games[1].timeline[3].role == (Roles.SuspectedDoubleAgent,)
    assert games[1].timeline[3].time == 225.0

    assert games[1].timeline[4].action_test == ActionTest.NoAT
    assert games[1].timeline[4].actor == "spy"
    assert games[1].timeline[4].books == (None,)
    assert games[1].timeline[4].cast_name == (Characters.Irish,)
    assert games[1].timeline[4].category == TimelineCategory.Cast
    assert games[1].timeline[4].elapsed_time == 0.0
    assert games[1].timeline[4].event == "seduction target cast."
    assert games[1].timeline[4].mission == Missions.NoMission
    assert games[1].timeline[4].role == (Roles.SeductionTarget,)
    assert games[1].timeline[4].time == 225.0

    assert games[1].timeline[5].action_test == ActionTest.NoAT
    assert games[1].timeline[5].actor == "spy"
    assert games[1].timeline[5].books == (None,)
    assert games[1].timeline[5].cast_name == (Characters.Boots,)
    assert games[1].timeline[5].category == TimelineCategory.Cast
    assert games[1].timeline[5].elapsed_time == 0.0
    assert games[1].timeline[5].event == "civilian cast."
    assert games[1].timeline[5].mission == Missions.NoMission
    assert games[1].timeline[5].role == (Roles.Civilian,)
    assert games[1].timeline[5].time == 225.0

    assert games[1].timeline[6].action_test == ActionTest.NoAT
    assert games[1].timeline[6].actor == "spy"
    assert games[1].timeline[6].books == (None,)
    assert games[1].timeline[6].cast_name == (Characters.Sikh,)
    assert games[1].timeline[6].category == TimelineCategory.Cast
    assert games[1].timeline[6].elapsed_time == 0.0
    assert games[1].timeline[6].event == "civilian cast."
    assert games[1].timeline[6].mission == Missions.NoMission
    assert games[1].timeline[6].role == (Roles.Civilian,)
    assert games[1].timeline[6].time == 225.0

    assert games[1].timeline[7].action_test == ActionTest.NoAT
    assert games[1].timeline[7].actor == "spy"
    assert games[1].timeline[7].books == (None,)
    assert games[1].timeline[7].cast_name == (Characters.Rocker,)
    assert games[1].timeline[7].category == TimelineCategory.Cast
    assert games[1].timeline[7].elapsed_time == 0.0
    assert games[1].timeline[7].event == "civilian cast."
    assert games[1].timeline[7].mission == Missions.NoMission
    assert games[1].timeline[7].role == (Roles.Civilian,)
    assert games[1].timeline[7].time == 225.0

    assert games[1].timeline[8].action_test == ActionTest.NoAT
    assert games[1].timeline[8].actor == "spy"
    assert games[1].timeline[8].books == (None,)
    assert games[1].timeline[8].cast_name == (Characters.Helen,)
    assert games[1].timeline[8].category == TimelineCategory.Cast
    assert games[1].timeline[8].elapsed_time == 0.0
    assert games[1].timeline[8].event == "civilian cast."
    assert games[1].timeline[8].mission == Missions.NoMission
    assert games[1].timeline[8].role == (Roles.Civilian,)
    assert games[1].timeline[8].time == 225.0

    assert games[1].timeline[9].action_test == ActionTest.NoAT
    assert games[1].timeline[9].actor == "spy"
    assert games[1].timeline[9].books == (None,)
    assert games[1].timeline[9].cast_name == (Characters.Alice,)
    assert games[1].timeline[9].category == TimelineCategory.Cast
    assert games[1].timeline[9].elapsed_time == 0.0
    assert games[1].timeline[9].event == "civilian cast."
    assert games[1].timeline[9].mission == Missions.NoMission
    assert games[1].timeline[9].role == (Roles.Civilian,)
    assert games[1].timeline[9].time == 225.0

    assert games[1].timeline[10].action_test == ActionTest.NoAT
    assert games[1].timeline[10].actor == "spy"
    assert games[1].timeline[10].books == (None,)
    assert games[1].timeline[10].cast_name == (Characters.Oprah,)
    assert games[1].timeline[10].category == TimelineCategory.Cast
    assert games[1].timeline[10].elapsed_time == 0.0
    assert games[1].timeline[10].event == "civilian cast."
    assert games[1].timeline[10].mission == Missions.NoMission
    assert games[1].timeline[10].role == (Roles.Civilian,)
    assert games[1].timeline[10].time == 225.0

    assert games[1].timeline[11].action_test == ActionTest.NoAT
    assert games[1].timeline[11].actor == "spy"
    assert games[1].timeline[11].books == (None,)
    assert games[1].timeline[11].cast_name == (Characters.Morgan,)
    assert games[1].timeline[11].category == TimelineCategory.Cast
    assert games[1].timeline[11].elapsed_time == 0.0
    assert games[1].timeline[11].event == "civilian cast."
    assert games[1].timeline[11].mission == Missions.NoMission
    assert games[1].timeline[11].role == (Roles.Civilian,)
    assert games[1].timeline[11].time == 225.0

    assert games[1].timeline[12].action_test == ActionTest.NoAT
    assert games[1].timeline[12].actor == "spy"
    assert games[1].timeline[12].books == (None,)
    assert games[1].timeline[12].cast_name == (Characters.Plain,)
    assert games[1].timeline[12].category == TimelineCategory.Cast
    assert games[1].timeline[12].elapsed_time == 0.0
    assert games[1].timeline[12].event == "civilian cast."
    assert games[1].timeline[12].mission == Missions.NoMission
    assert games[1].timeline[12].role == (Roles.Civilian,)
    assert games[1].timeline[12].time == 225.0

    assert games[1].timeline[13].action_test == ActionTest.NoAT
    assert games[1].timeline[13].actor == "spy"
    assert games[1].timeline[13].books == (None,)
    assert games[1].timeline[13].cast_name == (Characters.Sari,)
    assert games[1].timeline[13].category == TimelineCategory.Cast
    assert games[1].timeline[13].elapsed_time == 0.0
    assert games[1].timeline[13].event == "civilian cast."
    assert games[1].timeline[13].mission == Missions.NoMission
    assert games[1].timeline[13].role == (Roles.Civilian,)
    assert games[1].timeline[13].time == 225.0

    assert games[1].timeline[14].action_test == ActionTest.NoAT
    assert games[1].timeline[14].actor == "spy"
    assert games[1].timeline[14].books == (None,)
    assert games[1].timeline[14].cast_name == (Characters.Taft,)
    assert games[1].timeline[14].category == TimelineCategory.Cast
    assert games[1].timeline[14].elapsed_time == 0.0
    assert games[1].timeline[14].event == "civilian cast."
    assert games[1].timeline[14].mission == Missions.NoMission
    assert games[1].timeline[14].role == (Roles.Civilian,)
    assert games[1].timeline[14].time == 225.0

    assert games[1].timeline[15].action_test == ActionTest.NoAT
    assert games[1].timeline[15].actor == "spy"
    assert games[1].timeline[15].books == (None,)
    assert games[1].timeline[15].cast_name == (Characters.Carlos,)
    assert games[1].timeline[15].category == TimelineCategory.Cast
    assert games[1].timeline[15].elapsed_time == 0.0
    assert games[1].timeline[15].event == "civilian cast."
    assert games[1].timeline[15].mission == Missions.NoMission
    assert games[1].timeline[15].role == (Roles.Civilian,)
    assert games[1].timeline[15].time == 225.0

    assert games[1].timeline[16].action_test == ActionTest.NoAT
    assert games[1].timeline[16].actor == "spy"
    assert games[1].timeline[16].books == (None,)
    assert games[1].timeline[16].cast_name == (Characters.Smallman,)
    assert games[1].timeline[16].category == TimelineCategory.Cast
    assert games[1].timeline[16].elapsed_time == 0.0
    assert games[1].timeline[16].event == "civilian cast."
    assert games[1].timeline[16].mission == Missions.NoMission
    assert games[1].timeline[16].role == (Roles.Civilian,)
    assert games[1].timeline[16].time == 225.0

    assert games[1].timeline[17].action_test == ActionTest.NoAT
    assert games[1].timeline[17].actor == "spy"
    assert games[1].timeline[17].books == (None,)
    assert games[1].timeline[17].cast_name == (Characters.Teal,)
    assert games[1].timeline[17].category == TimelineCategory.Cast
    assert games[1].timeline[17].elapsed_time == 0.0
    assert games[1].timeline[17].event == "civilian cast."
    assert games[1].timeline[17].mission == Missions.NoMission
    assert games[1].timeline[17].role == (Roles.Civilian,)
    assert games[1].timeline[17].time == 225.0

    assert games[1].timeline[18].action_test == ActionTest.NoAT
    assert games[1].timeline[18].actor == "spy"
    assert games[1].timeline[18].books == (None,)
    assert games[1].timeline[18].cast_name == (Characters.General,)
    assert games[1].timeline[18].category == TimelineCategory.Cast
    assert games[1].timeline[18].elapsed_time == 0.0
    assert games[1].timeline[18].event == "civilian cast."
    assert games[1].timeline[18].mission == Missions.NoMission
    assert games[1].timeline[18].role == (Roles.Civilian,)
    assert games[1].timeline[18].time == 225.0

    assert games[1].timeline[19].action_test == ActionTest.NoAT
    assert games[1].timeline[19].actor == "spy"
    assert games[1].timeline[19].books == (None,)
    assert games[1].timeline[19].cast_name == (Characters.Duke,)
    assert games[1].timeline[19].category == TimelineCategory.Cast
    assert games[1].timeline[19].elapsed_time == 0.0
    assert games[1].timeline[19].event == "civilian cast."
    assert games[1].timeline[19].mission == Missions.NoMission
    assert games[1].timeline[19].role == (Roles.Civilian,)
    assert games[1].timeline[19].time == 225.0

    assert games[1].timeline[20].action_test == ActionTest.NoAT
    assert games[1].timeline[20].actor == "spy"
    assert games[1].timeline[20].books == (None,)
    assert games[1].timeline[20].cast_name == (Characters.Salmon,)
    assert games[1].timeline[20].category == TimelineCategory.Cast
    assert games[1].timeline[20].elapsed_time == 0.0
    assert games[1].timeline[20].event == "civilian cast."
    assert games[1].timeline[20].mission == Missions.NoMission
    assert games[1].timeline[20].role == (Roles.Civilian,)
    assert games[1].timeline[20].time == 225.0

    assert games[1].timeline[21].action_test == ActionTest.NoAT
    assert games[1].timeline[21].actor == "spy"
    assert games[1].timeline[21].books == (None,)
    assert games[1].timeline[21].cast_name == (None,)
    assert games[1].timeline[21].category == TimelineCategory.MissionSelected
    assert games[1].timeline[21].elapsed_time == 0.0
    assert games[1].timeline[21].event == "bug ambassador selected."
    assert games[1].timeline[21].mission == Missions.Bug
    assert games[1].timeline[21].role == (None,)
    assert games[1].timeline[21].time == 225.0

    assert games[1].timeline[22].action_test == ActionTest.NoAT
    assert games[1].timeline[22].actor == "spy"
    assert games[1].timeline[22].books == (None,)
    assert games[1].timeline[22].cast_name == (None,)
    assert games[1].timeline[22].category == TimelineCategory.MissionSelected
    assert games[1].timeline[22].elapsed_time == 0.0
    assert games[1].timeline[22].event == "contact double agent selected."
    assert games[1].timeline[22].mission == Missions.Contact
    assert games[1].timeline[22].role == (None,)
    assert games[1].timeline[22].time == 225.0

    assert games[1].timeline[23].action_test == ActionTest.NoAT
    assert games[1].timeline[23].actor == "spy"
    assert games[1].timeline[23].books == (None,)
    assert games[1].timeline[23].cast_name == (None,)
    assert games[1].timeline[23].category == TimelineCategory.MissionSelected
    assert games[1].timeline[23].elapsed_time == 0.0
    assert games[1].timeline[23].event == "transfer microfilm selected."
    assert games[1].timeline[23].mission == Missions.Transfer
    assert games[1].timeline[23].role == (None,)
    assert games[1].timeline[23].time == 225.0

    assert games[1].timeline[24].action_test == ActionTest.NoAT
    assert games[1].timeline[24].actor == "spy"
    assert games[1].timeline[24].books == (None,)
    assert games[1].timeline[24].cast_name == (None,)
    assert games[1].timeline[24].category == TimelineCategory.MissionSelected
    assert games[1].timeline[24].elapsed_time == 0.0
    assert games[1].timeline[24].event == "swap statue selected."
    assert games[1].timeline[24].mission == Missions.Swap
    assert games[1].timeline[24].role == (None,)
    assert games[1].timeline[24].time == 225.0

    assert games[1].timeline[25].action_test == ActionTest.NoAT
    assert games[1].timeline[25].actor == "spy"
    assert games[1].timeline[25].books == (None,)
    assert games[1].timeline[25].cast_name == (None,)
    assert games[1].timeline[25].category == TimelineCategory.MissionSelected
    assert games[1].timeline[25].elapsed_time == 0.0
    assert games[1].timeline[25].event == "inspect 3 statues selected."
    assert games[1].timeline[25].mission == Missions.Inspect
    assert games[1].timeline[25].role == (None,)
    assert games[1].timeline[25].time == 225.0

    assert games[1].timeline[26].action_test == ActionTest.NoAT
    assert games[1].timeline[26].actor == "spy"
    assert games[1].timeline[26].books == (None,)
    assert games[1].timeline[26].cast_name == (None,)
    assert games[1].timeline[26].category == TimelineCategory.MissionSelected
    assert games[1].timeline[26].elapsed_time == 0.0
    assert games[1].timeline[26].event == "seduce target selected."
    assert games[1].timeline[26].mission == Missions.Seduce
    assert games[1].timeline[26].role == (None,)
    assert games[1].timeline[26].time == 225.0

    assert games[1].timeline[27].action_test == ActionTest.NoAT
    assert games[1].timeline[27].actor == "spy"
    assert games[1].timeline[27].books == (None,)
    assert games[1].timeline[27].cast_name == (None,)
    assert games[1].timeline[27].category == TimelineCategory.MissionSelected
    assert games[1].timeline[27].elapsed_time == 0.0
    assert games[1].timeline[27].event == "purloin guest list selected."
    assert games[1].timeline[27].mission == Missions.Purloin
    assert games[1].timeline[27].role == (None,)
    assert games[1].timeline[27].time == 225.0

    assert games[1].timeline[28].action_test == ActionTest.NoAT
    assert games[1].timeline[28].actor == "spy"
    assert games[1].timeline[28].books == (None,)
    assert games[1].timeline[28].cast_name == (None,)
    assert games[1].timeline[28].category == TimelineCategory.MissionSelected
    assert games[1].timeline[28].elapsed_time == 0.0
    assert games[1].timeline[28].event == "fingerprint ambassador selected."
    assert games[1].timeline[28].mission == Missions.Fingerprint
    assert games[1].timeline[28].role == (None,)
    assert games[1].timeline[28].time == 225.0

    assert games[1].timeline[29].action_test == ActionTest.NoAT
    assert games[1].timeline[29].actor == "spy"
    assert games[1].timeline[29].books == (None,)
    assert games[1].timeline[29].cast_name == (None,)
    assert games[1].timeline[29].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[29].elapsed_time == 0.0
    assert games[1].timeline[29].event == "bug ambassador enabled."
    assert games[1].timeline[29].mission == Missions.Bug
    assert games[1].timeline[29].role == (None,)
    assert games[1].timeline[29].time == 225.0

    assert games[1].timeline[30].action_test == ActionTest.NoAT
    assert games[1].timeline[30].actor == "spy"
    assert games[1].timeline[30].books == (None,)
    assert games[1].timeline[30].cast_name == (None,)
    assert games[1].timeline[30].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[30].elapsed_time == 0.0
    assert games[1].timeline[30].event == "contact double agent enabled."
    assert games[1].timeline[30].mission == Missions.Contact
    assert games[1].timeline[30].role == (None,)
    assert games[1].timeline[30].time == 225.0

    assert games[1].timeline[31].action_test == ActionTest.NoAT
    assert games[1].timeline[31].actor == "spy"
    assert games[1].timeline[31].books == (None,)
    assert games[1].timeline[31].cast_name == (None,)
    assert games[1].timeline[31].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[31].elapsed_time == 0.0
    assert games[1].timeline[31].event == "transfer microfilm enabled."
    assert games[1].timeline[31].mission == Missions.Transfer
    assert games[1].timeline[31].role == (None,)
    assert games[1].timeline[31].time == 225.0

    assert games[1].timeline[32].action_test == ActionTest.NoAT
    assert games[1].timeline[32].actor == "spy"
    assert games[1].timeline[32].books == (None,)
    assert games[1].timeline[32].cast_name == (None,)
    assert games[1].timeline[32].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[32].elapsed_time == 0.0
    assert games[1].timeline[32].event == "swap statue enabled."
    assert games[1].timeline[32].mission == Missions.Swap
    assert games[1].timeline[32].role == (None,)
    assert games[1].timeline[32].time == 225.0

    assert games[1].timeline[33].action_test == ActionTest.NoAT
    assert games[1].timeline[33].actor == "spy"
    assert games[1].timeline[33].books == (None,)
    assert games[1].timeline[33].cast_name == (None,)
    assert games[1].timeline[33].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[33].elapsed_time == 0.0
    assert games[1].timeline[33].event == "inspect 3 statues enabled."
    assert games[1].timeline[33].mission == Missions.Inspect
    assert games[1].timeline[33].role == (None,)
    assert games[1].timeline[33].time == 225.0

    assert games[1].timeline[34].action_test == ActionTest.NoAT
    assert games[1].timeline[34].actor == "spy"
    assert games[1].timeline[34].books == (None,)
    assert games[1].timeline[34].cast_name == (None,)
    assert games[1].timeline[34].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[34].elapsed_time == 0.0
    assert games[1].timeline[34].event == "seduce target enabled."
    assert games[1].timeline[34].mission == Missions.Seduce
    assert games[1].timeline[34].role == (None,)
    assert games[1].timeline[34].time == 225.0

    assert games[1].timeline[35].action_test == ActionTest.NoAT
    assert games[1].timeline[35].actor == "spy"
    assert games[1].timeline[35].books == (None,)
    assert games[1].timeline[35].cast_name == (None,)
    assert games[1].timeline[35].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[35].elapsed_time == 0.0
    assert games[1].timeline[35].event == "purloin guest list enabled."
    assert games[1].timeline[35].mission == Missions.Purloin
    assert games[1].timeline[35].role == (None,)
    assert games[1].timeline[35].time == 225.0

    assert games[1].timeline[36].action_test == ActionTest.NoAT
    assert games[1].timeline[36].actor == "spy"
    assert games[1].timeline[36].books == (None,)
    assert games[1].timeline[36].cast_name == (None,)
    assert games[1].timeline[36].category == TimelineCategory.MissionEnabled
    assert games[1].timeline[36].elapsed_time == 0.0
    assert games[1].timeline[36].event == "fingerprint ambassador enabled."
    assert games[1].timeline[36].mission == Missions.Fingerprint
    assert games[1].timeline[36].role == (None,)
    assert games[1].timeline[36].time == 225.0

    assert games[1].timeline[37].action_test == ActionTest.NoAT
    assert games[1].timeline[37].actor == "game"
    assert games[1].timeline[37].books == (None,)
    assert games[1].timeline[37].cast_name == (None,)
    assert games[1].timeline[37].category == TimelineCategory.GameStart
    assert games[1].timeline[37].elapsed_time == 0.0
    assert games[1].timeline[37].event == "game started."
    assert games[1].timeline[37].mission == Missions.NoMission
    assert games[1].timeline[37].role == (None,)
    assert games[1].timeline[37].time == 225.0

    assert games[1].timeline[38].action_test == ActionTest.NoAT
    assert games[1].timeline[38].actor == "spy"
    assert games[1].timeline[38].books == (None,)
    assert games[1].timeline[38].cast_name == (None,)
    assert games[1].timeline[38].category == TimelineCategory.NoCategory
    assert games[1].timeline[38].elapsed_time == 1.31
    assert games[1].timeline[38].event == "spy player takes control from ai."
    assert games[1].timeline[38].mission == Missions.NoMission
    assert games[1].timeline[38].role == (None,)
    assert games[1].timeline[38].time == 223.6

    assert games[1].timeline[39].action_test == ActionTest.NoAT
    assert games[1].timeline[39].actor == "sniper"
    assert games[1].timeline[39].books == (None,)
    assert games[1].timeline[39].cast_name == (Characters.Disney,)
    assert games[1].timeline[39].category == TimelineCategory.SniperLights
    assert games[1].timeline[39].elapsed_time == 9.69
    assert games[1].timeline[39].event == "marked suspicious."
    assert games[1].timeline[39].mission == Missions.NoMission
    assert games[1].timeline[39].role == (Roles.Ambassador,)
    assert games[1].timeline[39].time == 215.3

    assert games[1].timeline[40].action_test == ActionTest.NoAT
    assert games[1].timeline[40].actor == "sniper"
    assert games[1].timeline[40].books == (None,)
    assert games[1].timeline[40].cast_name == (Characters.Toby,)
    assert games[1].timeline[40].category == TimelineCategory.SniperLights
    assert games[1].timeline[40].elapsed_time == 10.81
    assert games[1].timeline[40].event == "marked suspicious."
    assert games[1].timeline[40].mission == Missions.NoMission
    assert games[1].timeline[40].role == (Roles.Staff,)
    assert games[1].timeline[40].time == 214.1

    assert games[1].timeline[41].action_test == ActionTest.NoAT
    assert games[1].timeline[41].actor == "sniper"
    assert games[1].timeline[41].books == (None,)
    assert games[1].timeline[41].cast_name == (Characters.Sikh,)
    assert games[1].timeline[41].category == TimelineCategory.SniperLights
    assert games[1].timeline[41].elapsed_time == 11.44
    assert games[1].timeline[41].event == "marked suspicious."
    assert games[1].timeline[41].mission == Missions.NoMission
    assert games[1].timeline[41].role == (Roles.Civilian,)
    assert games[1].timeline[41].time == 213.5

    assert games[1].timeline[42].action_test == ActionTest.NoAT
    assert games[1].timeline[42].actor == "sniper"
    assert games[1].timeline[42].books == (None,)
    assert games[1].timeline[42].cast_name == (Characters.Duke,)
    assert games[1].timeline[42].category == TimelineCategory.SniperLights
    assert games[1].timeline[42].elapsed_time == 12.25
    assert games[1].timeline[42].event == "marked suspicious."
    assert games[1].timeline[42].mission == Missions.NoMission
    assert games[1].timeline[42].role == (Roles.Civilian,)
    assert games[1].timeline[42].time == 212.7

    assert games[1].timeline[43].action_test == ActionTest.NoAT
    assert games[1].timeline[43].actor == "spy"
    assert games[1].timeline[43].books == (None,)
    assert games[1].timeline[43].cast_name == (Characters.Queen,)
    assert games[1].timeline[43].category == TimelineCategory.Drinks
    assert games[1].timeline[43].elapsed_time == 12.63
    assert games[1].timeline[43].event == "took last sip of drink."
    assert games[1].timeline[43].mission == Missions.NoMission
    assert games[1].timeline[43].role == (Roles.Spy,)
    assert games[1].timeline[43].time == 212.3

    assert games[1].timeline[44].action_test == ActionTest.NoAT
    assert games[1].timeline[44].actor == "sniper"
    assert games[1].timeline[44].books == (None,)
    assert games[1].timeline[44].cast_name == (Characters.Bling,)
    assert games[1].timeline[44].category == TimelineCategory.SniperLights
    assert games[1].timeline[44].elapsed_time == 16.00
    assert games[1].timeline[44].event == "marked less suspicious."
    assert games[1].timeline[44].mission == Missions.NoMission
    assert games[1].timeline[44].role == (Roles.SuspectedDoubleAgent,)
    assert games[1].timeline[44].time == 209.0

    assert games[1].timeline[45].action_test == ActionTest.NoAT
    assert games[1].timeline[45].actor == "spy"
    assert games[1].timeline[45].books == (None,)
    assert games[1].timeline[45].cast_name == (None,)
    assert games[1].timeline[45].category == TimelineCategory.Conversation
    assert games[1].timeline[45].elapsed_time == 22.69
    assert games[1].timeline[45].event == "spy enters conversation."
    assert games[1].timeline[45].mission == Missions.NoMission
    assert games[1].timeline[45].role == (None,)
    assert games[1].timeline[45].time == 202.3

    assert games[1].timeline[46].action_test == ActionTest.NoAT
    assert games[1].timeline[46].actor == "sniper"
    assert games[1].timeline[46].books == (None,)
    assert games[1].timeline[46].cast_name == (Characters.Sari,)
    assert games[1].timeline[46].category == TimelineCategory.SniperLights
    assert games[1].timeline[46].elapsed_time == 27.69
    assert games[1].timeline[46].event == "marked suspicious."
    assert games[1].timeline[46].mission == Missions.NoMission
    assert games[1].timeline[46].role == (Roles.Civilian,)
    assert games[1].timeline[46].time == 197.3

    assert games[1].timeline[47].action_test == ActionTest.NoAT
    assert games[1].timeline[47].actor == "spy"
    assert games[1].timeline[47].books == (None,)
    assert games[1].timeline[47].cast_name == (None,)
    assert games[1].timeline[47].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[47].elapsed_time == 28.31
    assert games[1].timeline[47].event == "action triggered: seduce target"
    assert games[1].timeline[47].mission == Missions.Seduce
    assert games[1].timeline[47].role == (None,)
    assert games[1].timeline[47].time == 196.6

    assert games[1].timeline[48].action_test == ActionTest.NoAT
    assert games[1].timeline[48].actor == "spy"
    assert games[1].timeline[48].books == (None,)
    assert games[1].timeline[48].cast_name == (Characters.Irish,)
    assert games[1].timeline[48].category == TimelineCategory.NoCategory
    assert games[1].timeline[48].elapsed_time == 28.31
    assert games[1].timeline[48].event == "begin flirtation with seduction target."
    assert games[1].timeline[48].mission == Missions.Seduce
    assert games[1].timeline[48].role == (Roles.SeductionTarget,)
    assert games[1].timeline[48].time == 196.6

    assert games[1].timeline[49].action_test == ActionTest.Green
    assert games[1].timeline[49].actor == "spy"
    assert games[1].timeline[49].books == (None,)
    assert games[1].timeline[49].cast_name == (None,)
    assert games[1].timeline[49].category == TimelineCategory.ActionTest
    assert games[1].timeline[49].elapsed_time == 29.25
    assert games[1].timeline[49].event == "action test green: seduce target"
    assert games[1].timeline[49].mission == Missions.Seduce
    assert games[1].timeline[49].role == (None,)
    assert games[1].timeline[49].time == 195.7

    assert games[1].timeline[50].action_test == ActionTest.NoAT
    assert games[1].timeline[50].actor == "spy"
    assert games[1].timeline[50].books == (None,)
    assert games[1].timeline[50].cast_name == (Characters.Irish,)
    assert games[1].timeline[50].category == TimelineCategory.MissionPartial
    assert games[1].timeline[50].elapsed_time == 29.25
    assert games[1].timeline[50].event == "flirt with seduction target: 51%"
    assert games[1].timeline[50].mission == Missions.Seduce
    assert games[1].timeline[50].role == (Roles.SeductionTarget,)
    assert games[1].timeline[50].time == 195.7

    assert games[1].timeline[51].action_test == ActionTest.NoAT
    assert games[1].timeline[51].actor == "sniper"
    assert games[1].timeline[51].books == (None,)
    assert games[1].timeline[51].cast_name == (Characters.Wheels,)
    assert games[1].timeline[51].category == TimelineCategory.SniperLights
    assert games[1].timeline[51].elapsed_time == 37.81
    assert games[1].timeline[51].event == "marked less suspicious."
    assert games[1].timeline[51].mission == Missions.NoMission
    assert games[1].timeline[51].role == (Roles.DoubleAgent,)
    assert games[1].timeline[51].time == 187.1

    assert games[1].timeline[52].action_test == ActionTest.NoAT
    assert games[1].timeline[52].actor == "spy"
    assert games[1].timeline[52].books == (None,)
    assert games[1].timeline[52].cast_name == (None,)
    assert games[1].timeline[52].category == TimelineCategory.Conversation
    assert games[1].timeline[52].elapsed_time == 40.63
    assert games[1].timeline[52].event == "spy leaves conversation."
    assert games[1].timeline[52].mission == Missions.NoMission
    assert games[1].timeline[52].role == (None,)
    assert games[1].timeline[52].time == 184.3

    assert games[1].timeline[53].action_test == ActionTest.NoAT
    assert games[1].timeline[53].actor == "spy"
    assert games[1].timeline[53].books == (None,)
    assert games[1].timeline[53].cast_name == (None,)
    assert games[1].timeline[53].category == TimelineCategory.NoCategory
    assert games[1].timeline[53].elapsed_time == 46.0
    assert games[1].timeline[53].event == "flirtation cooldown expired."
    assert games[1].timeline[53].mission == Missions.Seduce
    assert games[1].timeline[53].role == (None,)
    assert games[1].timeline[53].time == 179.0

    assert games[1].timeline[54].action_test == ActionTest.NoAT
    assert games[1].timeline[54].actor == "sniper"
    assert games[1].timeline[54].books == (None,)
    assert games[1].timeline[54].cast_name == (Characters.Damon,)
    assert games[1].timeline[54].category == TimelineCategory.SniperLights
    assert games[1].timeline[54].elapsed_time == 53.94
    assert games[1].timeline[54].event == "marked less suspicious."
    assert games[1].timeline[54].mission == Missions.NoMission
    assert games[1].timeline[54].role == (Roles.Staff,)
    assert games[1].timeline[54].time == 171.0

    assert games[1].timeline[55].action_test == ActionTest.NoAT
    assert games[1].timeline[55].actor == "spy"
    assert games[1].timeline[55].books == (None,)
    assert games[1].timeline[55].cast_name == (None,)
    assert (
        games[1].timeline[55].category
        == TimelineCategory.ActionTriggered | TimelineCategory.Watch
    )
    assert games[1].timeline[55].elapsed_time == 59.5
    assert games[1].timeline[55].event == "action triggered: check watch"
    assert games[1].timeline[55].mission == Missions.NoMission
    assert games[1].timeline[55].role == (None,)
    assert games[1].timeline[55].time == 165.5

    assert games[1].timeline[56].action_test == ActionTest.NoAT
    assert games[1].timeline[56].actor == "spy"
    assert games[1].timeline[56].books == (None,)
    assert games[1].timeline[56].cast_name == (None,)
    assert (
        games[1].timeline[56].category
        == TimelineCategory.TimeAdd | TimelineCategory.Watch
    )
    assert games[1].timeline[56].elapsed_time == 59.5
    assert games[1].timeline[56].event == "watch checked to add time."
    assert games[1].timeline[56].mission == Missions.NoMission
    assert games[1].timeline[56].role == (None,)
    assert games[1].timeline[56].time == 165.5

    assert games[1].timeline[57].action_test == ActionTest.White
    assert games[1].timeline[57].actor == "spy"
    assert games[1].timeline[57].books == (None,)
    assert games[1].timeline[57].cast_name == (None,)
    assert (
        games[1].timeline[57].category
        == TimelineCategory.ActionTest
        | TimelineCategory.TimeAdd
        | TimelineCategory.Watch
    )
    assert games[1].timeline[57].elapsed_time == 60.50
    assert games[1].timeline[57].event == "action test white: check watch"
    assert games[1].timeline[57].mission == Missions.NoMission
    assert games[1].timeline[57].role == (None,)
    assert games[1].timeline[57].time == 164.4

    assert games[1].timeline[58].action_test == ActionTest.NoAT
    assert games[1].timeline[58].actor == "sniper"
    assert games[1].timeline[58].books == (None,)
    assert games[1].timeline[58].cast_name == (Characters.Alice,)
    assert games[1].timeline[58].category == TimelineCategory.SniperLights
    assert games[1].timeline[58].elapsed_time == 61.81
    assert games[1].timeline[58].event == "marked less suspicious."
    assert games[1].timeline[58].mission == Missions.NoMission
    assert games[1].timeline[58].role == (Roles.Civilian,)
    assert games[1].timeline[58].time == 163.1

    assert games[1].timeline[59].action_test == ActionTest.NoAT
    assert games[1].timeline[59].actor == "spy"
    assert games[1].timeline[59].books == (None,)
    assert games[1].timeline[59].cast_name == (None,)
    assert games[1].timeline[59].category == TimelineCategory.TimeAdd
    assert games[1].timeline[59].elapsed_time == 61.94
    assert games[1].timeline[59].event == "45 seconds added to match."
    assert games[1].timeline[59].mission == Missions.NoMission
    assert games[1].timeline[59].role == (None,)
    assert games[1].timeline[59].time == 163.0

    assert games[1].timeline[60].action_test == ActionTest.NoAT
    assert games[1].timeline[60].actor == "spy"
    assert games[1].timeline[60].books == (None,)
    assert games[1].timeline[60].cast_name == (None,)
    assert games[1].timeline[60].category == TimelineCategory.Conversation
    assert games[1].timeline[60].elapsed_time == 67.94
    assert games[1].timeline[60].event == "spy enters conversation."
    assert games[1].timeline[60].mission == Missions.NoMission
    assert games[1].timeline[60].role == (None,)
    assert games[1].timeline[60].time == 202.0

    assert games[1].timeline[61].action_test == ActionTest.NoAT
    assert games[1].timeline[61].actor == "spy"
    assert games[1].timeline[61].books == (None,)
    assert games[1].timeline[61].cast_name == (None,)
    assert games[1].timeline[61].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[61].elapsed_time == 71.75
    assert games[1].timeline[61].event == "action triggered: seduce target"
    assert games[1].timeline[61].mission == Missions.Seduce
    assert games[1].timeline[61].role == (None,)
    assert games[1].timeline[61].time == 198.2

    assert games[1].timeline[62].action_test == ActionTest.NoAT
    assert games[1].timeline[62].actor == "spy"
    assert games[1].timeline[62].books == (None,)
    assert games[1].timeline[62].cast_name == (Characters.Irish,)
    assert games[1].timeline[62].category == TimelineCategory.NoCategory
    assert games[1].timeline[62].elapsed_time == 71.75
    assert games[1].timeline[62].event == "begin flirtation with seduction target."
    assert games[1].timeline[62].mission == Missions.Seduce
    assert games[1].timeline[62].role == (Roles.SeductionTarget,)
    assert games[1].timeline[62].time == 198.2

    assert games[1].timeline[63].action_test == ActionTest.White
    assert games[1].timeline[63].actor == "spy"
    assert games[1].timeline[63].books == (None,)
    assert games[1].timeline[63].cast_name == (None,)
    assert games[1].timeline[63].category == TimelineCategory.ActionTest
    assert games[1].timeline[63].elapsed_time == 72.88
    assert games[1].timeline[63].event == "action test white: seduce target"
    assert games[1].timeline[63].mission == Missions.Seduce
    assert games[1].timeline[63].role == (None,)
    assert games[1].timeline[63].time == 197.1

    assert games[1].timeline[64].action_test == ActionTest.NoAT
    assert games[1].timeline[64].actor == "spy"
    assert games[1].timeline[64].books == (None,)
    assert games[1].timeline[64].cast_name == (Characters.Irish,)
    assert games[1].timeline[64].category == TimelineCategory.MissionPartial
    assert games[1].timeline[64].elapsed_time == 72.88
    assert games[1].timeline[64].event == "flirt with seduction target: 79%"
    assert games[1].timeline[64].mission == Missions.Seduce
    assert games[1].timeline[64].role == (Roles.SeductionTarget,)
    assert games[1].timeline[64].time == 197.1

    assert games[1].timeline[65].action_test == ActionTest.NoAT
    assert games[1].timeline[65].actor == "spy"
    assert games[1].timeline[65].books == (None,)
    assert games[1].timeline[65].cast_name == (None,)
    assert games[1].timeline[65].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[65].elapsed_time == 89.56
    assert games[1].timeline[65].event == "action triggered: bug ambassador"
    assert games[1].timeline[65].mission == Missions.Bug
    assert games[1].timeline[65].role == (None,)
    assert games[1].timeline[65].time == 180.4

    assert games[1].timeline[66].action_test == ActionTest.NoAT
    assert games[1].timeline[66].actor == "spy"
    assert games[1].timeline[66].books == (None,)
    assert games[1].timeline[66].cast_name == (Characters.Disney,)
    assert games[1].timeline[66].category == TimelineCategory.NoCategory
    assert games[1].timeline[66].elapsed_time == 89.56
    assert games[1].timeline[66].event == "begin planting bug while walking."
    assert games[1].timeline[66].mission == Missions.Bug
    assert games[1].timeline[66].role == (Roles.Ambassador,)
    assert games[1].timeline[66].time == 180.4

    assert games[1].timeline[67].action_test == ActionTest.NoAT
    assert games[1].timeline[67].actor == "spy"
    assert games[1].timeline[67].books == (None,)
    assert games[1].timeline[67].cast_name == (Characters.Disney,)
    assert games[1].timeline[67].category == TimelineCategory.NoCategory
    assert games[1].timeline[67].elapsed_time == 90.69
    assert games[1].timeline[67].event == "failed planting bug while walking."
    assert games[1].timeline[67].mission == Missions.Bug
    assert games[1].timeline[67].role == (Roles.Ambassador,)
    assert games[1].timeline[67].time == 179.3

    assert games[1].timeline[68].action_test == ActionTest.NoAT
    assert games[1].timeline[68].actor == "sniper"
    assert games[1].timeline[68].books == (None,)
    assert games[1].timeline[68].cast_name == (Characters.Carlos,)
    assert games[1].timeline[68].category == TimelineCategory.SniperLights
    assert games[1].timeline[68].elapsed_time == 91.56
    assert games[1].timeline[68].event == "marked less suspicious."
    assert games[1].timeline[68].mission == Missions.NoMission
    assert games[1].timeline[68].role == (Roles.Civilian,)
    assert games[1].timeline[68].time == 178.4

    assert games[1].timeline[69].action_test == ActionTest.NoAT
    assert games[1].timeline[69].actor == "spy"
    assert games[1].timeline[69].books == (None,)
    assert games[1].timeline[69].cast_name == (None,)
    assert games[1].timeline[69].category == TimelineCategory.ActionTriggered
    assert games[1].timeline[69].elapsed_time == 100.00
    assert games[1].timeline[69].event == "action triggered: bug ambassador"
    assert games[1].timeline[69].mission == Missions.Bug
    assert games[1].timeline[69].role == (None,)
    assert games[1].timeline[69].time == 169.9

    assert games[1].timeline[70].action_test == ActionTest.NoAT
    assert games[1].timeline[70].actor == "spy"
    assert games[1].timeline[70].books == (None,)
    assert games[1].timeline[70].cast_name == (Characters.Disney,)
    assert games[1].timeline[70].category == TimelineCategory.NoCategory
    assert games[1].timeline[70].elapsed_time == 100.00
    assert games[1].timeline[70].event == "begin planting bug while standing."
    assert games[1].timeline[70].mission == Missions.Bug
    assert games[1].timeline[70].role == (Roles.Ambassador,)
    assert games[1].timeline[70].time == 169.9

    assert games[1].timeline[71].action_test == ActionTest.NoAT
    assert games[1].timeline[71].actor == "spy"
    assert games[1].timeline[71].books == (None,)
    assert games[1].timeline[71].cast_name == (Characters.Disney,)
    assert games[1].timeline[71].category == TimelineCategory.MissionComplete
    assert games[1].timeline[71].elapsed_time == 101.63
    assert games[1].timeline[71].event == "bugged ambassador while standing."
    assert games[1].timeline[71].mission == Missions.Bug
    assert games[1].timeline[71].role == (Roles.Ambassador,)
    assert games[1].timeline[71].time == 168.3

    assert games[1].timeline[72].action_test == ActionTest.NoAT
    assert games[1].timeline[72].actor == "sniper"
    assert games[1].timeline[72].books == (None,)
    assert games[1].timeline[72].cast_name == (Characters.Queen,)
    assert games[1].timeline[72].category == TimelineCategory.SniperShot
    assert games[1].timeline[72].elapsed_time == 103.88
    assert games[1].timeline[72].event == "took shot."
    assert games[1].timeline[72].mission == Missions.NoMission
    assert games[1].timeline[72].role == (Roles.Spy,)
    assert games[1].timeline[72].time == 166.1

    assert games[1].timeline[73].action_test == ActionTest.NoAT
    assert games[1].timeline[73].actor == "game"
    assert games[1].timeline[73].books == (None,)
    assert games[1].timeline[73].cast_name == (Characters.Queen,)
    assert games[1].timeline[73].category == TimelineCategory.GameEnd
    assert games[1].timeline[73].elapsed_time == 109.88
    assert games[1].timeline[73].event == "sniper shot spy."
    assert games[1].timeline[73].mission == Missions.NoMission
    assert games[1].timeline[73].role == (Roles.Spy,)
    assert games[1].timeline[73].time == 160.1

    assert games[1].timeline.get_next_spy_action(games[1].timeline[73]) is None
