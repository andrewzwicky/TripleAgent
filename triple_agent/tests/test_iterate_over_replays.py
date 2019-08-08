from triple_agent.organization.replay_file_iterator import iterate_over_replays


def test_iterate_over_replays(get_test_events_folder, get_test_replay_pickle_folder):
    # this test is to confirm that replays can be successfully found in the folder structure
    # and assigned the correct event, week, division, etc.
    games = list(
        iterate_over_replays(
            lambda g: "kcmmmmm" in [g.spy, g.sniper],
            events_folder=get_test_events_folder,
            pickle_folder=get_test_replay_pickle_folder,
        )
    )
    games.sort(key=lambda g: g.start_time)

    assert games[0].uuid == "-wj1l-oaQRS25PYWbN9DLw"
    assert games[1].uuid == "YXXnB3cVRVCHSXUKWWleeQ"
    assert games[2].uuid == "wG5eWfuKTMWt9FQtfxkexQ"
    assert games[3].uuid == "IoY6dxc5Qh25yPx6f4gQbw"
    assert games[4].uuid == "w04KWeaHRCK6s3C06AzQaA"
    assert games[5].uuid == "jhIlv7roRR-gOObcd1BcFQ"
    assert games[6].uuid == "oua8JMz-R5yNpHs9kUU0dA"
    assert games[7].uuid == "r_XWMspjT9aSGx9ckxuXrw"

    assert games[0].event is None
    assert games[1].event is None
    assert games[2].event is None
    assert games[3].event == "BatchEvent"
    assert games[4].event == "BatchEvent"
    assert games[5].event == "DetailedEvent"
    assert games[6].event == "DetailedEvent"
    assert games[7].event == "DetailedEvent"

    assert games[0].division is None
    assert games[1].division is None
    assert games[2].division is None
    assert games[3].division is None
    assert games[4].division is None
    assert games[5].division == "BestGroup"
    assert games[6].division == "BestGroup"
    assert games[7].division == "BestGroup"

    assert games[0].week is None
    assert games[1].week is None
    assert games[2].week is None
    assert games[3].week is None
    assert games[4].week is None
    assert games[5].week == 6
    assert games[6].week == 6
    assert games[7].week == 6

    # ensure we're using the unprocessed replays
    # (haven't loaded a pickled by accident)
    assert games[0].timeline is None
    assert games[1].timeline is None
    assert games[2].timeline is None
    assert games[3].timeline is None
    assert games[4].timeline is None
    assert games[5].timeline is None
    assert games[6].timeline is None
    assert games[7].timeline is None
