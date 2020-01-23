import pytest
from triple_agent.classes.characters import Characters
from triple_agent.classes.lights import Lights
from triple_agent.classes.action_tests import ActionTest


@pytest.mark.quick
def test_character_order():
    # Mr. S, Ms. B, Mr. P
    char_list = [Characters.Smallman, Characters.Boots, Characters.Carlos]

    assert sorted(char_list) == [
        Characters.Boots,
        Characters.Carlos,
        Characters.Smallman,
    ]


@pytest.mark.quick
def test_character_order_toby_damon():
    # Mr. S, Ms. B, Mr. P
    char_list = [
        Characters.Smallman,
        Characters.Toby,
        Characters.Damon,
        Characters.Boots,
        Characters.Carlos,
    ]

    assert sorted(char_list) == [
        Characters.Boots,
        Characters.Carlos,
        Characters.Smallman,
        Characters.Damon,
        Characters.Toby,
    ]


@pytest.mark.quick
def test_reverse_order_enum():
    lights_list = [Lights.Neutral, Lights.Highlight, Lights.Lowlight]

    assert sorted(lights_list) == [
        Lights.Highlight,
        Lights.Neutral,
        Lights.Lowlight,
    ]


@pytest.mark.quick
def test_reverse_order_enum_at():
    lights_list = [
        ActionTest.Green,
        ActionTest.NoAT,
        ActionTest.Green.Ignored,
        ActionTest.Green,
        ActionTest.White,
    ]

    assert sorted(lights_list) == [
        ActionTest.Ignored,
        ActionTest.White,
        ActionTest.Green,
        ActionTest.Green,
        ActionTest.NoAT,
    ]
