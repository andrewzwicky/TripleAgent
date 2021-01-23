import datetime
import base64
import struct

from triple_agent.parsing.replay.replay_header_offsets import (
    HEADER_OFFSET_DICT,
    HeaderOffsetBase,
    HeaderInfo,
)

from triple_agent.classes.missions import Missions
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.venues import Venue

# Provide one broad exception for all SpyPartyParse specific exceptions.
# Others inherit from this so that consumers can catch either
# the overall exception or more detailed ones if desired.
class RplyParseException(Exception):
    pass


class FileTooShortException(RplyParseException):
    pass


class UnknownFileVersion(RplyParseException):
    pass


class UnknownFileException(RplyParseException):
    pass


class UnknownVenueException(RplyParseException):
    pass


class UnknownResultException(RplyParseException):
    pass


RESULT_MAP = {
    0: WinType.MissionsWin,
    1: WinType.TimeOut,
    2: WinType.SpyShot,
    3: WinType.CivilianShot
    # 4 is "In Progress", which likely shouldn't be
    # parsed (data could be messed up in any number of ways)
}

VARIANT_MAP = {
    Venue.Teien: [
        "BooksBooksBooks",
        "BooksStatuesBooks",
        "StatuesBooksBooks",
        "StatuesStatuesBooks",
        "BooksBooksStatues",
        "BooksStatuesStatues",
        "StatuesBooksStatues",
        "StatuesStatuesStatues",
    ],
    Venue.Aquarium: ["Bottom", "Top"],
}

LEVEL_MAP = {
    # 0x3A30C326: "BvB High-Rise",
    # 0x5996FAAA: "BvB (New Art) Ballroom",
    0x5B121925: Venue.Ballroom,
    0x1A56C5A1: Venue.HighRise,
    0x28B3AA5E: Venue.OldGallery,
    0x290A0C75: Venue.Courtyard2,
    0x3695F583: Venue.Panopticon,
    0xA8BEA091: Venue.OldVeranda,
    0xB8891FBC: Venue.OldBalcony,
    0x0D027340: Venue.CrowdedPub,
    0x3B85FFF3: Venue.Pub,
    0x09C2E7B0: Venue.OldBallroom,
    0xB4CF686B: Venue.Courtyard1,
    0x7076E38F: Venue.DoubleModern,
    0xE6146120: Venue.Modern,
    0xF3E61461: Venue.Modern,
    0x6F81A558: Venue.Veranda,
    0x9DC5BB5E: Venue.Courtyard,
    0x168F4F62: Venue.Library,
    0x1DBD8E41: Venue.Balcony,
    0x7173B8BF: Venue.Gallery,
    0x9032CE22: Venue.Terrace,
    0x2E37F15B: Venue.Moderne,
    0x79DFA0CF: Venue.Teien,
    0x98E45D99: Venue.Aquarium,
    0x35AC5135: Venue.Redwoods,
}

MODE_MAP = {0: "k", 1: "p", 2: "a"}

HEADER_DATA_MINIMUM_BYTES = 416


def parse_mission_bitpack(mission_bytes):
    rply_missions = Missions.NoMission
    if mission_bytes & (1 << 0):
        rply_missions |= Missions.Bug
    if mission_bytes & (1 << 1):
        rply_missions |= Missions.Contact
    if mission_bytes & (1 << 2):
        rply_missions |= Missions.Transfer
    if mission_bytes & (1 << 3):
        rply_missions |= Missions.Swap
    if mission_bytes & (1 << 4):
        rply_missions |= Missions.Inspect
    if mission_bytes & (1 << 5):
        rply_missions |= Missions.Seduce
    if mission_bytes & (1 << 6):
        rply_missions |= Missions.Purloin
    if mission_bytes & (1 << 7):
        rply_missions |= Missions.Fingerprint

    return rply_missions


def parse_game_type_info(info_bytes):
    mode = info_bytes >> 28
    available = (info_bytes & 0x0FFFC000) >> 14
    required = info_bytes & 0x00003FFF

    real_mode = MODE_MAP[mode]
    if real_mode == "k":
        return f"k{required}"

    return f"{real_mode}{required}/{available}"


def unpack(header_info: HeaderInfo, replay_bytes):
    if header_info is None:
        return False

    return struct.unpack(
        header_info.unpack,
        replay_bytes[header_info.offset : header_info.offset + header_info.size],
    )[0]


def parse_rply_file(file_path):
    offsets = HeaderOffsetBase()
    result = dict()

    with open(file_path, "rb") as rply_file:
        replay_bytes = rply_file.read()

    if len(replay_bytes) < HEADER_DATA_MINIMUM_BYTES:
        raise FileTooShortException(
            f"We require a minimum of {HEADER_DATA_MINIMUM_BYTES} bytes for replay parsing"
        )

    # confirm that this is an actual replay file
    if unpack(offsets.magic_string, replay_bytes) != b"RPLY":
        raise UnknownFileException()

    file_version = unpack(offsets.replay_file_version, replay_bytes)

    try:
        offsets = HEADER_OFFSET_DICT[file_version]()
    except IndexError as upper_exception:
        raise UnknownFileVersion() from upper_exception

    # TODO: why int instead of float here?
    result["duration"] = int(unpack(offsets.duration, replay_bytes))

    # = can show up at the end of the UUID, trim those off
    result["uuid"] = (
        base64.urlsafe_b64encode(unpack(offsets.uuid, replay_bytes))
        .decode()
        .rstrip("=")
    )

    result["start_time"] = datetime.datetime.fromtimestamp(
        unpack(offsets.timestamp, replay_bytes)
    )
    result["sequence_number"] = unpack(offsets.sequence_number, replay_bytes)

    spy_username_length = unpack(offsets.spy_uname_len, replay_bytes)
    sniper_username_length = unpack(offsets.sniper_uname_len, replay_bytes)

    spy_username_header_info = HeaderInfo(
        offsets.username_starts, spy_username_length, f"{spy_username_length}s"
    )
    sniper_username_header_info = HeaderInfo(
        offsets.username_starts + spy_username_length,
        sniper_username_length,
        f"{sniper_username_length}s",
    )

    result["spy_username"] = unpack(spy_username_header_info, replay_bytes).decode()
    result["sniper_username"] = unpack(
        sniper_username_header_info, replay_bytes
    ).decode()

    this_result = unpack(offsets.game_result, replay_bytes)
    try:
        result["result"] = RESULT_MAP[this_result]
    except KeyError as upper_exception:
        raise UnknownResultException(
            f"Unknown game result {this_result}"
        ) from upper_exception

    result["game_type"] = parse_game_type_info(unpack(offsets.game_type, replay_bytes))

    try:
        this_result = unpack(offsets.level, replay_bytes)
        result["level"] = LEVEL_MAP[this_result]
    except KeyError as upper_exception:
        raise UnknownVenueException(
            f"Unknown map hash {this_result}"
        ) from upper_exception

    if (this_result := unpack(offsets.map_variant, replay_bytes)) :
        try:
            result["map_variant"] = VARIANT_MAP[result["level"]][this_result]
        except KeyError:
            pass

    result["selected_missions"] = parse_mission_bitpack(
        unpack(offsets.selected_missions, replay_bytes)
    )
    result["picked_missions"] = parse_mission_bitpack(
        unpack(offsets.picked_missions, replay_bytes)
    )
    result["completed_missions"] = parse_mission_bitpack(
        unpack(offsets.completed_missions, replay_bytes)
    )

    if (
        spy_displayname_length := unpack(offsets.spy_display_name_length, replay_bytes)
    ) :
        spy_displayname_header_info = HeaderInfo(
            offsets.username_starts + spy_username_length + sniper_username_length,
            spy_displayname_length,
            f"{spy_displayname_length}s",
        )
        result["spy_displayname"] = unpack(
            spy_displayname_header_info, replay_bytes
        ).decode()
    else:
        result["spy_displayname"] = result["spy_username"]

    if (
        sniper_displayname_length := unpack(
            offsets.sniper_display_name_length, replay_bytes
        )
    ) :
        sniper_displayname_header_info = HeaderInfo(
            offsets.username_starts
            + spy_username_length
            + sniper_username_length
            + spy_displayname_length,
            sniper_displayname_length,
            f"{sniper_displayname_length}s",
        )
        result["sniper_displayname"] = unpack(
            sniper_displayname_header_info, replay_bytes
        ).decode()
    else:
        result["sniper_displayname"] = result["sniper_username"]

    if (this_result := unpack(offsets.guest_count, replay_bytes)) :
        result["guest_count"] = this_result

    if (this_result := unpack(offsets.start_duration, replay_bytes)) :
        result["start_clock_seconds"] = this_result

    return result
