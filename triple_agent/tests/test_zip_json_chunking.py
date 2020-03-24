import pytest
from triple_agent.reports.external_reports.refresh_all_external_reports import (
    create_zip_start_end_indices,
)

JSON_CHUNK_CASES = [
    ([(1, 0, 25), (2, 25, 50), (3, 50, 55)], 56, 25),
    ([(1, 0, 25), (2, 25, 50), (3, 50, 74)], 75, 25),
    ([(1, 0, 11)], 12, 25),
]


@pytest.mark.quick
@pytest.mark.parametrize("expected_series, num_files, chunk_size", JSON_CHUNK_CASES)
def test_simple_chunks(expected_series, num_files, chunk_size):
    assert expected_series == list(create_zip_start_end_indices(num_files, chunk_size))
