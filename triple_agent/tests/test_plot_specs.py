import pytest
from triple_agent.reports.generation.plot_specs import DataQueryProperties

DATA_QUERY_CASES = [
    (DataQueryProperties(), DataQueryProperties(), DataQueryProperties()),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        DataQueryProperties(),
        DataQueryProperties(stack_order=[1, 2, 3]),
    ),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        5,
        DataQueryProperties(stack_order=[1, 2, 3]),
    ),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        DataQueryProperties(limit=20),
        DataQueryProperties(stack_order=[1, 2, 3], limit=20),
    ),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        DataQueryProperties(stack_order=[4, 5, 6]),
        DataQueryProperties(stack_order=[1, 2, 3]),
    ),
]


@pytest.mark.parametrize("initial,suggested,expected", DATA_QUERY_CASES)
def test_data_query_properties(initial, suggested, expected):
    initial.update(suggested)

    assert initial == expected
