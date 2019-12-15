import pytest
from triple_agent.classes.missions import Missions


MISSION_SERIALIZE_CASES = [
    (Missions.Inspect | Missions.Seduce, ["Seduce", "Inspect"]),
    (Missions.Seduce, ["Seduce"]),
    (Missions.NoMission, []),
    (
        Missions.Fingerprint | Missions.Inspect | Missions.Bug | Missions.Purloin,
        ["Inspect", "Fingerprint", "Bug", "Purloin"],
    ),
]


@pytest.mark.parametrize("mission_enum, expected_list", MISSION_SERIALIZE_CASES)
def test_mission_serialize(mission_enum, expected_list):
    assert mission_enum.serialize() == expected_list
