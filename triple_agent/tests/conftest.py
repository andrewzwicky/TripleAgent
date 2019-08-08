from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
import pytest


@pytest.fixture(scope="session")
def get_test_games():
    test_game_uuids = [
        "8uf6pUK7TFegBD8Cbr2qMw",
        "as-RnR1RQruzhRDZr7JP9A",
        "h_fNkizcR0mBFlokph3yEw",
        "jhx6e7UpTmeKueggeGcAKg",
        "k415gCwtS3ml9_EzUPpWFw",
        "k8x3n_zfTtiw9FSS6rM13w",
        "lOGf7W_MSlu1RRYxW2MMsA",
        "OiG7qvC9QOaSKVGlesdpWQ",
        "TPWiwN2aQc6EHEf6jKDKaA",
        "UgPZ7k1cQoCT9c6a_oG46w",
        "vgAlD77AQw2XKTZq3H4NTg",
    ]

    return get_parsed_replays(lambda game: game.uuid in test_game_uuids)
