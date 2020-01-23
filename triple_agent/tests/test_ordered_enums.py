import pytest
import os
from triple_agent.classes.characters import Characters


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
