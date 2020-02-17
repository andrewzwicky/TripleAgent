import pytest

from triple_agent.classes.characters import Characters
from triple_agent.classes.roles import Roles
from triple_agent.classes.timeline import TimelineEvent, Timeline


@pytest.mark.parsing
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
            (Roles.DoubleAgent,),
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
        pytest.approx(0),
        pytest.approx(7.3),
        pytest.approx(11.7),
        pytest.approx(20),
        pytest.approx(20.5),
        pytest.approx(23.3),
        pytest.approx(26),
        pytest.approx(26.8),
        pytest.approx(28.1),
        pytest.approx(31.8),
        pytest.approx(31.8),
        pytest.approx(32.5),
        pytest.approx(32.5),
        pytest.approx(33.5),
        pytest.approx(33.7),
        pytest.approx(43),
        pytest.approx(46.4),
        pytest.approx(54.8),
        pytest.approx(57.3),
        pytest.approx(71.1),
        pytest.approx(73),
        pytest.approx(78.5),
        pytest.approx(78.5),
        pytest.approx(79.6),
        pytest.approx(81),
        pytest.approx(81.5),
        pytest.approx(87),
        pytest.approx(87),
        pytest.approx(101.1),
        pytest.approx(104.8),
    ]

    t_events = [TimelineEvent(*args) for args in events]

    t_line = Timeline(t_events)

    t_line.calculate_elapsed_times()

    for t_event, expected_elapsed in zip(t_line.lines, expected_elapseds):
        assert t_event.elapsed_time == expected_elapsed
