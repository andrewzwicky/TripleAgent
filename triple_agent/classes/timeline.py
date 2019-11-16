# pylint: disable=too-many-lines
import re
from collections.abc import Sequence
from datetime import datetime
from enum import auto, Flag
from typing import Optional, List, Tuple
from dataclasses import dataclass, field

from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.books import Books
from triple_agent.classes.characters import Characters, CHARACTERS_TO_STRING
from triple_agent.classes.missions import Missions
from triple_agent.classes.roles import Roles


class TimelineCoherency(Flag):
    Coherent = 0
    NoTimeline = auto()
    TimeRewind = auto()
    BookMissingColor = auto()
    NoGameStart = auto()
    NoGameEnding = auto()
    StartClockMismatch = auto()
    PickedMissionsMismatch = auto()
    CompletedMissionsMismatch = auto()
    SelectedMissionsMismatch = auto()
    GuestCountMismatch = auto()
    SpyNotCastInBeginning = auto()
    CharacterNotAssignedRole = auto()
    RoleWithNoCharacter = auto()


class TimelineCategory(Flag):
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


CATEGORIZATION_DICTIONARY = {
    ("game", "game started."): (
        TimelineCategory.GameStart,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "missions completed successfully."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "missions completed. 10 second countdown."): (
        TimelineCategory.MissionCountdown,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "missions completed. countdown pending."): (
        TimelineCategory.MissionCountdown,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "overtime!"): (
        TimelineCategory.Overtime,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "sniper shot civilian."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "sniper shot spy."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "sniper shot too late for sync."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "spy ran out of time."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked book."): (
        TimelineCategory.Books | TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked less suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked neutral suspicion."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked spy less suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked spy neutral suspicion."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked spy suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "took shot."): (
        TimelineCategory.SniperShot,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "45 seconds added to match."): (
        TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "aborted watch check to add time."): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "action test canceled: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Canceled,
    ),
    ("spy", "action test green: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Green,
    ),
    ("spy", "action test green: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Green,
    ),
    ("spy", "action test green: fingerprint ambassador"): (
        TimelineCategory.ActionTest,
        Missions.Fingerprint,
        ActionTest.Green,
    ),
    ("spy", "action test green: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.Green,
    ),
    ("spy", "action test green: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Green,
    ),
    ("spy", "action test green: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Green,
    ),
    ("spy", "action test green: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.Green,
    ),
    ("spy", "action test green: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Green,
    ),
    ("spy", "action test ignored: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: fingerprint ambassador"): (
        TimelineCategory.ActionTest,
        Missions.Fingerprint,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Ignored,
    ),
    ("spy", "action test red: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Red,
    ),
    ("spy", "action test red: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Red,
    ),
    ("spy", "action test red: fingerprint ambassador"): (
        TimelineCategory.ActionTest,
        Missions.Fingerprint,
        ActionTest.Red,
    ),
    ("spy", "action test red: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.Red,
    ),
    ("spy", "action test red: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Red,
    ),
    ("spy", "action test red: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Red,
    ),
    ("spy", "action test red: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.Red,
    ),
    ("spy", "action test red: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Red,
    ),
    ("spy", "action test white: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.White,
    ),
    ("spy", "action test white: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.White,
    ),
    ("spy", "action test white: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.White,
    ),
    ("spy", "action test white: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.White,
    ),
    ("spy", "action test white: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.White,
    ),
    ("spy", "action test white: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.White,
    ),
    ("spy", "action test white: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.White,
    ),
    ("spy", "action triggered: bug ambassador"): (
        TimelineCategory.ActionTriggered,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: check watch"): (
        TimelineCategory.Watch | TimelineCategory.ActionTriggered,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: contact double agent"): (
        TimelineCategory.ActionTriggered,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: fingerprint ambassador"): (
        TimelineCategory.ActionTriggered,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTriggered,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: purloin guest list"): (
        TimelineCategory.ActionTriggered,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: seduce target"): (
        TimelineCategory.ActionTriggered,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTriggered,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTriggered,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "all statues inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionComplete,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "ambassador cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "ambassador's personal space violated."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "banana bread aborted."): (
        TimelineCategory.NoCategory,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "banana bread uttered."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "bartender offered drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "bartender offered cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "bartender picked next customer."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "begin flirtation with seduction target."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "begin planting bug while standing."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "begin planting bug while walking."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bug ambassador enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bug ambassador selected."): (
        TimelineCategory.MissionSelected,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bug transitioned from standing to walking."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bugged ambassador while standing."): (
        TimelineCategory.MissionComplete,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bugged ambassador while walking."): (
        TimelineCategory.MissionComplete,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "cast member picked up pending statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "character picked up pending statue."): (
        TimelineCategory.Statues,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "civilian cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "contact double agent enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "contact double agent selected."): (
        TimelineCategory.MissionSelected,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin timer expired."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to dr. m."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to dr. n."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. 5."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. a."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. c."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. d."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. g."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. i."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. k."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. p."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. q."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. s."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. u."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. 0."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. b."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. e."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. f."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. h."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. j."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. l."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. o."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. r."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. t."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegating purloin guest list"): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegating purloin guest list."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "demand drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "demand cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "double agent cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "double agent contacted."): (
        TimelineCategory.MissionComplete,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "double agent joined conversation with spy."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "double agent left conversation with spy."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "dropped statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "failed flirt with seduction target."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "failed planting bug while walking."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "fake banana bread started."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "fake banana bread uttered."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprint ambassador enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprint ambassador selected."): (
        TimelineCategory.MissionSelected,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted ambassador."): (
        TimelineCategory.MissionComplete,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted book."): (
        TimelineCategory.Books | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted briefcase."): (
        TimelineCategory.Briefcase | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted drink."): (
        TimelineCategory.Drinks | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted cupcake."): (
        TimelineCategory.Drinks | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted statue."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinting failed."): (
        TimelineCategory.NoCategory,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 100%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 15%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 16%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 17%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 18%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 19%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 20%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 21%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 22%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 23%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 24%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 25%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 26%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 27%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 28%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 29%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 30%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 31%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 32%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 33%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 34%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 35%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 36%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 37%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 38%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 39%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 40%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 41%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 42%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 43%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 44%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 45%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 46%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 47%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 48%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 49%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 50%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 51%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 52%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 53%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 54%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 55%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 56%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 57%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 58%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 59%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 60%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 61%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 62%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 63%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 64%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 65%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 66%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 67%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 68%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 69%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 70%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 71%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 72%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 73%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 74%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 75%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 76%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 77%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 78%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 79%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 80%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 81%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 82%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 83%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 84%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 85%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 86%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 87%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 88%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 89%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 90%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 91%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 92%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 93%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 94%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 95%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 96%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 97%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 98%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 99%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirtation cooldown expired."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "gave up on bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "get book from bookcase."): (
        TimelineCategory.Books,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got drink from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got cupcake from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "guest list purloin pending."): (
        TimelineCategory.NoCategory,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "guest list purloined."): (
        TimelineCategory.MissionComplete,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "guest list return pending."): (
        TimelineCategory.NoCategory,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "guest list returned."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "gulped drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "chomped cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "held statue inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "hide microfilm in book."): (
        TimelineCategory.Books | TimelineCategory.MissionPartial,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 1 statue enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 1 statue selected."): (
        TimelineCategory.MissionSelected,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 2 statues enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 2 statues selected."): (
        TimelineCategory.MissionSelected,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 3 statues enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 3 statues selected."): (
        TimelineCategory.MissionSelected,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "statue inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "interrupted speaker."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "left alone while attempting banana bread."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "left statue inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "left statue inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "right statue inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "left statue inspection cancelled."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "right statue inspection cancelled."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "missions reset."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable briefcase (difficult)."): (
        TimelineCategory.Briefcase,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable briefcase."): (
        TimelineCategory.Briefcase,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable statue (difficult)."): (
        TimelineCategory.Statues,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable statue."): (
        TimelineCategory.Statues,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "purloin guest list aborted."): (
        TimelineCategory.NoCategory,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "purloin guest list enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "purloin guest list selected."): (
        TimelineCategory.MissionSelected,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "put back statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "put book in bookcase."): (
        TimelineCategory.Books,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "read book."): (
        TimelineCategory.Books,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "real banana bread started."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "rejected drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "rejected cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "rejected drink from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "rejected cupcake from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "remove microfilm from book."): (
        TimelineCategory.Books | TimelineCategory.MissionPartial,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "request drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "request cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "request drink from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "request cupcake from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "right statue inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "seduce target enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "seduce target selected."): (
        TimelineCategory.MissionSelected,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "seduction canceled."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "seduction target cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "sipped drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "bit cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy cast."): (TimelineCategory.Cast, Missions.NoMission, ActionTest.NoAT),
    ("spy", "spy enters conversation."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy joined conversation with double agent."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy leaves conversation."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy left conversation with double agent."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy picks up briefcase."): (
        TimelineCategory.Briefcase,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy player takes control from ai."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy puts down briefcase."): (
        TimelineCategory.Briefcase,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy returns briefcase."): (
        TimelineCategory.Briefcase,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting book."): (
        TimelineCategory.Books,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting briefcase."): (
        TimelineCategory.Briefcase,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting drink."): (
        TimelineCategory.Drinks,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting cupcake."): (
        TimelineCategory.Drinks,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting statue."): (
        TimelineCategory.Statues,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started talking."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "statue swap pending."): (
        TimelineCategory.Statues,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "statue swapped."): (
        TimelineCategory.Statues | TimelineCategory.MissionComplete,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "stopped talking."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "suspected double agent cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "swap statue enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "swap statue selected."): (
        TimelineCategory.MissionSelected,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "target seduced."): (
        TimelineCategory.MissionComplete,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "took last sip of drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "took last bite of cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "transfer microfilm enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "transfer microfilm selected."): (
        TimelineCategory.MissionSelected,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "transferred microfilm."): (
        TimelineCategory.Books | TimelineCategory.MissionComplete,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "waiter gave up."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter offered drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter offered cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter stopped offering drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter stopped offering cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "watch checked to add time"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "watch checked to add time."): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "watch checked."): (
        TimelineCategory.Watch,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
}
int


@dataclass
class TimelineEvent:
    actor: str
    _raw_time_str: str
    event: str
    cast_name: Tuple[Optional[Characters], ...]
    role: Tuple[Optional[Roles], ...]
    books: Tuple[Optional[Books], ...]
    elapsed_time: float = field(default=0, init=False)
    time: float = field(default=0, init=False)
    category: TimelineCategory = field(default=TimelineCategory.NoCategory, init=False)
    mission: Missions = field(default=Missions.NoMission, init=False)
    action_test: ActionTest = field(default=ActionTest.NoAT, init=False)

    # this is needed for getting rid of commands and extra stuff from the OCR
    time_re = re.compile(r"(\d{2}:\d{2}.\d)")

    def __post_init__(self):
        try:
            self.time = (
                datetime.strptime(self._raw_time_str, "%M:%S.%f")
                - datetime.strptime("00:00.0", "%M:%S.%f")
            ).total_seconds()
        except ValueError:
            self.time = (
                datetime.strptime("00:00.0", "%M:%S.%f")
                - datetime.strptime(self._raw_time_str, "-%M:%S.%f")
            ).total_seconds()
        self.category, self.mission, self.action_test = CATEGORIZATION_DICTIONARY[
            (self.actor, self.event)
        ]

        if self.event.startswith("delegated purloin to "):
            # assume there will be a single a character here, use that for the name
            self.event = "delegated purloin to {}.".format(
                CHARACTERS_TO_STRING[self.cast_name[0]].lower()
            )

        assert len(self.cast_name) == len(self.role)

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
        self.parse_suspected_double_agents()

        super().__init__()

    def __getitem__(self, i):
        return self.lines[i]

    def __len__(self):
        return len(self.lines)

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    def __str__(self):  # pragma: no cover
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

    def parse_suspected_double_agents(self):
        # Games are parsed with all the yellow bars being assumed to be DoubleAgent.
        # Only after the game are the the suspected double agents identified and classified.
        suspected_das = set()

        for event in self:
            if (event.category & TimelineCategory.Cast) and (
                Roles.DoubleAgent in event.role
            ):
                assert len(event.role) == 1
                assert len(event.cast_name) == 1

                if event.event.startswith("suspected"):
                    suspected_das.add(event.cast_name[0])

        # iterate again in case there were sniper lights before cast assignment.
        for event in self:
            if set(event.cast_name) & suspected_das:
                event.role = tuple(
                    [
                        Roles.SuspectedDoubleAgent if cast in suspected_das else role
                        for cast, role in zip(event.cast_name, event.role)
                    ]
                )
