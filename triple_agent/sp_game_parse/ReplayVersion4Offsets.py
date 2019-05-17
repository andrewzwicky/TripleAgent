from .ReplayOffsets import ReplayOffsets


class ReplayVersion4Offsets(ReplayOffsets):
    def get_magic_number_offset(self):
        return 0x00

    def get_file_version_offset(self):
        return 0x04

    def get_protocol_version_offset(self):
        return 0x08

    def get_spy_party_version_offset(self):
        return 0x0C

    def get_duration_offset(self):
        return 0x14

    def get_uuid_offset(self):
        return 0x18

    def get_timestamp_offset(self):
        return 0x28

    def get_sequence_number_offset(self):
        return 0x2C

    def extract_spy_username(self, bytes):
        spy_username_length = bytes[0x2E]
        return self._read_bytes(bytes, 0x54, spy_username_length)

    def extract_sniper_username(self, bytes):
        spy_username_length = bytes[0x2E]
        sniper_username_length = bytes[0x2F]
        return self._read_bytes(
            bytes, 0x54 + spy_username_length, sniper_username_length
        )

    def contains_display_names(self):
        return False

    def contains_guest_count(self):
        return False

    def contains_start_clock(self):
        return False

    def get_game_result_offset(self):
        return 0x34

    def get_game_type_offset(self):
        return 0x38

    def get_level_offset(self):
        return 0x3C

    def get_selected_missions_offset(self):
        return 0x40

    def get_picked_missions_offset(self):
        return 0x44

    def get_completed_missions_offset(self):
        return 0x48
