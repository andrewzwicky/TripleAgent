import pytest

from triple_agent.classes.characters import Characters
from triple_agent.classes.roles import Roles
from triple_agent.classes.timeline import TimelineEvent, Timeline


@pytest.mark.quick
def test_calculate_elapsed_time():
    events = [
        (
            "spy",
            "01:54.1",
            "sipped drink.",
            (Characters.Salmon,),
            (Roles.Spy,),
            (None,),
        ),
        ("spy", "01:46.8", "spy leaves conversation.", (None,), (None,), (None,)),
        ("spy", "01:42.4", "flirtation cooldown expired.", (None,), (None,), (None,)),
        (
            "spy",
            "01:34.1",
            "delegated purloin timer expired.",
            (None,),
            (None,),
            (None,),
        ),
        (
            "spy",
            "01:33.6",
            "took last sip of drink.",
            (Characters.Salmon,),
            (Roles.Spy,),
            (None,),
        ),
        ("spy", "01:30.8", "picked up statue.", (None,), (None,), (None,)),
        (
            "spy",
            "01:28.1",
            "picked up fingerprintable statue.",
            (None,),
            (None,),
            (None,),
        ),
        (
            "spy",
            "01:27.3",
            "action triggered: inspect statues",
            (None,),
            (None,),
            (None,),
        ),
        (
            "spy",
            "01:26.0",
            "action test white: inspect statues",
            (None,),
            (None,),
            (None,),
        ),
        ("spy", "01:22.3", "held statue inspected.", (None,), (None,), (None,)),
        ("spy", "01:22.3", "all statues inspected.", (None,), (None,), (None,)),
        (
            "spy",
            "01:21.6",
            "action triggered: fingerprint ambassador",
            (None,),
            (None,),
            (None,),
        ),
        ("spy", "01:21.6", "started fingerprinting statue.", (None,), (None,), (None,)),
        ("spy", "01:20.6", "fingerprinted statue.", (None,), (None,), (None,)),
        ("spy", "01:20.4", "put back statue.", (None,), (None,), (None,)),
        (
            "sniper",
            "01:11.1",
            "marked suspicious.",
            (Characters.Sari,),
            (None,),
            (None,),
        ),
        ("spy", "01:07.7", "spy enters conversation.", (None,), (None,), (None,)),
        ("spy", "00:59.3", "spy leaves conversation.", (None,), (None,), (None,)),
        ("spy", "00:56.8", "spy enters conversation.", (None,), (None,), (None,)),
        ("spy", "00:43.0", "spy leaves conversation.", (None,), (None,), (None,)),
        (
            "sniper",
            "00:41.1",
            "marked suspicious.",
            (Characters.Alice,),
            (None,),
            (None,),
        ),
        ("spy", "00:35.6", "action triggered: check watch", (None,), (None,), (None,)),
        ("spy", "00:35.6", "watch checked to add time.", (None,), (None,), (None,)),
        ("spy", "00:34.5", "action test green: check watch", (None,), (None,), (None,)),
        ("spy", "00:33.1", "45 seconds added to match.", (None,), (None,), (None,)),
        (
            "sniper",
            "01:17.6",
            "marked suspicious.",
            (Characters.Wheels,),
            (None,),
            (None,),
        ),
        ("spy", "01:12.1", "spy enters conversation.", (None,), (None,), (None,)),
        (
            "spy",
            "01:12.1",
            "spy joined conversation with double agent.",
            (Characters.Duke,),
            (Roles.DoubleAgents,),
            (None,),
        ),
        ("sniper", "00:58.0", "took shot.", (Characters.Sari,), (None,), (None,)),
        (
            "game",
            "00:54.3",
            "sniper shot civilian.",
            (Characters.Sari,),
            (None,),
            (None,),
        ),
    ]

    expected_elapseds = [
        0,
        7.3,
        11.7,
        20,
        20.5,
        23.3,
        26,
        26.8,
        28.1,
        31.8,
        31.8,
        32.5,
        32.5,
        33.5,
        33.7,
        43,
        46.4,
        54.8,
        57.3,
        71.1,
        73,
        78.5,
        78.5,
        79.6,
        81,
        81.5,
        87,
        87,
        101.1,
        104.8,
    ]

    t_events = [TimelineEvent(*args) for args in events]

    t_line = Timeline(t_events)

    t_line.calculate_elapsed_times()

    for t_event, expected_elapsed in zip(t_line.lines, expected_elapseds):
        assert t_event.elapsed_time == pytest.approx(expected_elapsed, 0.001)
