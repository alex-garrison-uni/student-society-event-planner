import pytest
from pathlib import Path

from student_society_event_planner.utils import load_event_file

input_files =[
    "input_10.txt",
    "input_100.txt",
    "input_1000.txt",
    "input_200.txt",
    "input_500.txt",
    "input_large.txt",
    "input_medium.txt",
    "input_small.txt"
]

invalid_input_files = [
    "input_invalid_1.txt",
    "input_invalid_2.txt",
    "input_invalid_3.txt",
    "input_invalid_4.txt"
]

@pytest.mark.parametrize("input_file", input_files)
def test_load_file(input_file):
    event = load_event_file(input_file)

    assert event.max_budget is not None
    assert event.max_time is not None
    assert all(activity is not None for activity in event.activities)

@pytest.mark.parametrize("invalid_input_file", invalid_input_files)
def test_invalid_load_file_errors(invalid_input_file):
    with pytest.raises(ValueError):
        load_event_file(Path("invalid") / invalid_input_file)
