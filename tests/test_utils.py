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


def test_load_event_file_missing_file_raises_file_not_found():
    """Loading a file that doesn't exist raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_event_file("this_file_does_not_exist.txt")


@pytest.mark.parametrize(
    "content, expected_exc",
    [
        # n must be a single int
        ("not-an-int\n10 200\nA 1 1 1\n", ValueError),
        # constraints must be two ints
        ("1\n10\nA 1 1 1\n", ValueError),
        # negative constraints are rejected
        ("1\n-1 10\nA 1 1 1\n", ValueError),
        ("1\n10 -1\nA 1 1 1\n", ValueError),
        # activity line must have 4 fields
        ("1\n10 200\nA 1 2\n", ValueError),
    ],
)
def test_load_event_file_validation_errors(tmp_path, monkeypatch, content, expected_exc):
    """Validate we fail fast with clear exceptions on bad file formats."""
    (tmp_path / "input_files").mkdir()
    (tmp_path / "input_files" / "temp.txt").write_text(content)
    monkeypatch.chdir(tmp_path)

    with pytest.raises(expected_exc):
        load_event_file("temp.txt")


def test_activity_count_zero_is_rejected(tmp_path, monkeypatch):
    """The spec states n >= 1, this test encodes that expectation."""
    (tmp_path / "input_files").mkdir()
    (tmp_path / "input_files" / "temp.txt").write_text("0\n10 200\n")
    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError):
        load_event_file("temp.txt")


def test_load_event_file_rejects_too_few_activity_lines(tmp_path, monkeypatch):
    """If the header says n activities, there must be n activity lines."""
    (tmp_path / "input_files").mkdir()
    # Header declares 2 activities but only 1 line follows.
    (tmp_path / "input_files" / "temp.txt").write_text(
        "2\n10 200\nA 1 1 1\n"
    )
    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError):
        load_event_file("temp.txt")


def test_load_event_file_ignores_extra_trailing_lines(tmp_path, monkeypatch):
    """Extra lines after the n activities should not break loading."""
    (tmp_path / "input_files").mkdir()
    (tmp_path / "input_files" / "temp.txt").write_text(
        "1\n10 200\nA 1 1 1\nTHIS-LINE-SHOULD-BE-IGNORED\n"
    )
    monkeypatch.chdir(tmp_path)

    event = load_event_file("temp.txt")
    assert len(event.activities) == 1
    assert event.activities[0].name == "A"
