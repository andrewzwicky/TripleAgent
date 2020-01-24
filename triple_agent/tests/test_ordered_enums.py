import pytest
from triple_agent.classes.characters import Characters
from triple_agent.classes.lights import Lights
from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.venues import Venue


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
def test_character_order_lt():
    assert Characters.Disney < Characters.Oprah


@pytest.mark.quick
def test_character_order_gt():
    assert Characters.Sari > Characters.Oprah


@pytest.mark.quick
def test_character_order_le_1():
    assert Characters.Disney <= Characters.Oprah


@pytest.mark.quick
def test_character_order_le_2():
    assert Characters.Disney <= Characters.Disney


@pytest.mark.quick
def test_character_order_ge_1():
    assert Characters.Oprah >= Characters.Oprah


@pytest.mark.quick
def test_character_order_ge_2():
    assert Characters.Sari >= Characters.Disney


@pytest.mark.quick
def test_action_test_order_gt():
    assert ActionTest.Green > ActionTest.Ignored


@pytest.mark.quick
def test_action_test_order_lt():
    assert ActionTest.Canceled < ActionTest.Ignored


@pytest.mark.quick
def test_action_test_order_ge_1():
    assert ActionTest.Green >= ActionTest.Ignored


@pytest.mark.quick
def test_action_test_order_ge_2():
    assert ActionTest.Green >= ActionTest.Green


@pytest.mark.quick
def test_action_test_order_le_1():
    assert ActionTest.Ignored <= ActionTest.Ignored


@pytest.mark.quick
def test_action_test_order_le_2():
    assert ActionTest.Canceled <= ActionTest.Green


@pytest.mark.quick
def test_action_test_mismatch_order_gt():
    with pytest.raises(TypeError):
        assert Characters.Sari > ActionTest.Ignored


@pytest.mark.quick
def test_action_test_mismatch_order_lt():
    with pytest.raises(TypeError):
        assert Characters.Sari < ActionTest.Ignored


@pytest.mark.quick
def test_action_test_mismatch_order_ge():
    with pytest.raises(TypeError):
        assert Characters.Sari >= ActionTest.Green


@pytest.mark.quick
def test_action_test_mismatch_order_le():
    with pytest.raises(TypeError):
        assert Characters.Sari <= ActionTest.Green


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


@pytest.mark.quick
def test_venue_order_lt():
    assert Venue.Balcony < Venue.Gallery


@pytest.mark.quick
def test_venue_order_gt():
    assert Venue.Pub > Venue.Gallery


@pytest.mark.quick
def test_venue_order_le_1():
    assert Venue.Balcony <= Venue.Gallery


@pytest.mark.quick
def test_venue_order_le_2():
    assert Venue.Balcony <= Venue.Balcony


@pytest.mark.quick
def test_venue_order_ge_1():
    assert Venue.Gallery >= Venue.Gallery


@pytest.mark.quick
def test_venue_order_ge_2():
    assert Venue.Pub >= Venue.Balcony


@pytest.mark.quick
def test_mismatch_order_lt():
    with pytest.raises(TypeError):
        assert Characters.Sari < Venue.Gallery


@pytest.mark.quick
def test_mismatch_order_gt():
    with pytest.raises(TypeError):
        assert Characters.Sari > Venue.Gallery


@pytest.mark.quick
def test_mismatch_order_le():
    with pytest.raises(TypeError):
        assert Characters.Sari <= Venue.Balcony


@pytest.mark.quick
def test_mismatch_order_ge():
    with pytest.raises(TypeError):
        assert Characters.Sari >= Venue.Balcony


@pytest.mark.quick
def test_mismatch_order_lt_str():
    with pytest.raises(TypeError):
        assert Characters.Sari < "test"


@pytest.mark.quick
def test_mismatch_order_gt_int():
    with pytest.raises(TypeError):
        assert Characters.Sari > 1
