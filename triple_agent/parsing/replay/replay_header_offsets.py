from dataclasses import dataclass


@dataclass
class HeaderInfo:
    """Class for keeping track of an item in inventory."""

    offset: int
    size: int
    unpack: str


class HeaderOffsetBase:
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.magic_string = HeaderInfo(0x00, 4, "4s")
        self.replay_file_version = HeaderInfo(0x04, 1, "B")
        self.duration = HeaderInfo(0x14, 4, "f")
        self.uuid = HeaderInfo(0x18, 16, "16s")
        self.timestamp = HeaderInfo(0x28, 4, "I")
        self.sequence_number = HeaderInfo(0x2C, 2, "H")
        self.spy_uname_len = HeaderInfo(0x2E, 1, "B")
        self.sniper_uname_len = HeaderInfo(0x2F, 1, "B")
        self.map_variant = None
        self.selected_missions = None
        self.picked_missions = None
        self.completed_missions = None
        self.spy_display_name_length = None
        self.sniper_display_name_length = None
        self.guest_count = None
        self.start_duration = None
        self.game_result = None
        self.game_type = None
        self.level = None


class HeaderOffsetV3(HeaderOffsetBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.username_starts = 0x50
        self.game_result = HeaderInfo(0x30, 4, "I")
        self.game_type = HeaderInfo(0x34, 4, "I")
        self.level = HeaderInfo(0x38, 4, "I")
        self.selected_missions = HeaderInfo(0x3C, 4, "I")
        self.picked_missions = HeaderInfo(0x40, 4, "I")
        self.completed_missions = HeaderInfo(0x44, 4, "I")


class HeaderOffsetV4(HeaderOffsetBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.username_starts = 0x54
        self.game_result = HeaderInfo(0x34, 4, "I")
        self.game_type = HeaderInfo(0x38, 4, "I")
        self.level = HeaderInfo(0x3C, 4, "I")
        self.selected_missions = HeaderInfo(0x40, 4, "I")
        self.picked_missions = HeaderInfo(0x44, 4, "I")
        self.completed_missions = HeaderInfo(0x48, 4, "I")


class HeaderOffsetV5(HeaderOffsetBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.username_starts = 0x60
        self.game_result = HeaderInfo(0x38, 4, "I")
        self.game_type = HeaderInfo(0x3C, 4, "I")
        self.level = HeaderInfo(0x40, 4, "I")
        self.selected_missions = HeaderInfo(0x44, 4, "I")
        self.picked_missions = HeaderInfo(0x48, 4, "I")
        self.completed_missions = HeaderInfo(0x4C, 4, "I")
        self.spy_display_name_length = HeaderInfo(0x30, 1, "B")
        self.sniper_display_name_length = HeaderInfo(0x31, 1, "B")
        self.guest_count = HeaderInfo(0x50, 4, "I")
        self.start_duration = HeaderInfo(0x54, 4, "I")


class HeaderOffsetV6(HeaderOffsetBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.username_starts = 0x64
        self.game_result = HeaderInfo(0x38, 4, "I")
        self.game_type = HeaderInfo(0x3C, 4, "I")
        self.level = HeaderInfo(0x40, 4, "I")
        self.map_variant = HeaderInfo(0x44, 4, "I")
        self.selected_missions = HeaderInfo(0x48, 4, "I")
        self.picked_missions = HeaderInfo(0x4C, 4, "I")
        self.completed_missions = HeaderInfo(0x50, 4, "I")
        self.spy_display_name_length = HeaderInfo(0x30, 1, "B")
        self.sniper_display_name_length = HeaderInfo(0x31, 1, "B")
        self.guest_count = HeaderInfo(0x54, 4, "I")
        self.start_duration = HeaderInfo(0x58, 4, "I")


HEADER_OFFSET_DICT = {
    3: HeaderOffsetV3,
    4: HeaderOffsetV4,
    5: HeaderOffsetV5,
    6: HeaderOffsetV6,
}
