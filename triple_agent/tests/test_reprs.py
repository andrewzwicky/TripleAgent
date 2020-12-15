import pytest
from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.books import Books
from triple_agent.classes.characters import Characters
from triple_agent.classes.roles import Roles


@pytest.mark.quick
def test_repr_AT_green():
    assert repr(ActionTest.Green) == "ActionTest.Green"


@pytest.mark.quick
def test_repr_AT_ignored():
    assert repr(ActionTest.Ignored) == "ActionTest.Ignored"


@pytest.mark.quick
def test_repr_books_green():
    assert repr(Books.Green) == "Books.Green"


@pytest.mark.quick
def test_repr_books_blue():
    assert repr(Books.Blue) == "Books.Blue"


@pytest.mark.quick
def test_repr_chars_sue():
    assert repr(Characters.Sue) == "Characters.Sue"


@pytest.mark.quick
def test_repr_chars_wheels():
    assert repr(Characters.Wheels) == "Characters.Wheels"


@pytest.mark.quick
def test_repr_chars_djackson():
    assert repr(Characters.DJackson) == "Characters.DJackson"


@pytest.mark.quick
def test_repr_roles_spy():
    assert repr(Roles.Spy) == "Roles.Spy"


@pytest.mark.quick
def test_repr_roles_spy():
    assert repr(Roles.DoubleAgent) == "Roles.DoubleAgent"
