import time
import random

import pytest

from student_society_event_planner.algorithms import bottom_up, bruteforce
from student_society_event_planner.classes import Activity, Event
from student_society_event_planner.utils import load_event_file

from .helpers import _names, _reference_exhaustive, _reference_optimum

def test_bottom_up_finds_known_optimum_for_sample_small_time_constraint():
    """input_small.txt has a unique best set when using time as the constraint."""
    event = load_event_file("input_small.txt")

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    # Verified by hand/exhaustive enumeration: max enjoyment under T=10 is 370.
    assert enjoyment == 370, f"Expected enjoyment 370, got {enjoyment}"
    assert time_used == 9, f"Expected time_used 9, got {time_used}"
    assert _names(chosen) == ["Game-Night", "Museum-Trip", "Pizza-Workshop"], \
        f"Expected specific activities, got {_names(chosen)}"
    assert sum(a.time for a in chosen) <= event.max_time, \
        f"Time constraint violated: {sum(a.time for a in chosen)} > {event.max_time}"


@pytest.mark.parametrize(
    "fname,max_time",
    [
        ("input_small.txt", 10),
        ("input_medium.txt", 15),
        ("input_large.txt", 20),
    ],
)
def test_bottom_up_returns_feasible_solution_on_provided_inputs(fname, max_time):
    """Sanity checks on the provided files."""
    event = load_event_file(fname)
    chosen, enjoyment, time_used = bottom_up(event, time_limit=5.0)

    assert time_used == sum(a.time for a in chosen), \
        f"Time used mismatch: reported {time_used}, actual {sum(a.time for a in chosen)}"
    assert enjoyment == sum(a.enjoyment for a in chosen), \
        f"Enjoyment mismatch: reported {enjoyment}, actual {sum(a.enjoyment for a in chosen)}"
    assert time_used <= max_time, \
        f"Time constraint violated: {time_used} > {max_time}"
    # Chosen activities must be unique instances from the event.
    assert len(chosen) == len(set(id(a) for a in chosen)), \
        "Duplicate activities in solution"
    assert all(a in event.activities for a in chosen), \
        "Unknown activity in solution"


def test_bottom_up_returns_empty_when_no_activity_fits():
    """Testing that the algorithm returns empty when no actviity fits."""
    event = Event(
        max_time=1,
        max_budget=999,
        activities=[
            Activity("Too-Long-1", 2, 10, 10),
            Activity("Too-Long-2", 3, 20, 100),
        ],
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    assert chosen == [], f"Expected empty list, got {chosen}"
    assert enjoyment == 0, f"Expected enjoyment 0, got {enjoyment}"
    assert time_used == 0, f"Expected time_used 0, got {time_used}"


def test_bottom_up_matches_reference_exhaustive_on_random_small_instances():
    """Bottom-up DP should hit the true optimum for small n."""
    rng = random.Random(1337)

    for trial in range(50):
        n = rng.randint(1, 12)
        max_time = rng.randint(0, 15)
        activities: list[Activity] = []
        for i in range(n):
            activities.append(
                Activity(
                    name=f"A{i}",
                    time=rng.randint(1, 6),
                    cost=rng.randint(0, 200),
                    enjoyment=rng.randint(0, 250),
                )
            )
        event = Event(max_time=max_time, max_budget=0, activities=activities)

        ref_chosen, ref_enjoyment, ref_time = _reference_exhaustive(event)
        chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

        # Must match the optimum enjoyment and be feasible.
        assert enjoyment == ref_enjoyment, \
            f"Trial {trial}: Expected enjoyment {ref_enjoyment}, got {enjoyment}"
        assert time_used == sum(a.time for a in chosen), \
            f"Trial {trial}: Time used mismatch"
        assert time_used <= max_time, \
            f"Trial {trial}: Time constraint violated"

        # If it matches enjoyment, it should also match some optimal time used
        # (not necessarily the same subset because tie-break rules can differ).
        assert time_used == ref_time, \
            f"Trial {trial}: Expected time {ref_time}, got {time_used}"


def test_bottom_up_matches_bruteforce_on_small_input():
    """Bottom-up DP and brute-force should produce identical results."""
    event = load_event_file("input_small.txt")

    bf_chosen, bf_enjoyment, bf_time = bruteforce(event, time_limit=10.0)
    dp_chosen, dp_enjoyment, dp_time = bottom_up(event, time_limit=10.0)

    assert dp_enjoyment == bf_enjoyment, \
        f"Enjoyment mismatch: BF={bf_enjoyment}, DP={dp_enjoyment}"
    assert dp_time == bf_time, \
        f"Time used mismatch: BF={bf_time}, DP={dp_time}"
    assert _names(dp_chosen) == _names(bf_chosen), \
        f"Activity sets differ: BF={_names(bf_chosen)}, DP={_names(dp_chosen)}"


def test_bottom_up_matches_bruteforce_on_medium_input():
    """Bottom-up DP and brute-force should produce identical results."""
    event = load_event_file("input_medium.txt")

    bf_chosen, bf_enjoyment, bf_time = bruteforce(event, time_limit=10.0)
    dp_chosen, dp_enjoyment, dp_time = bottom_up(event, time_limit=10.0)

    assert dp_enjoyment == bf_enjoyment, \
        f"Enjoyment mismatch: BF={bf_enjoyment}, DP={dp_enjoyment}"
    assert dp_time == bf_time, \
        f"Time used mismatch: BF={bf_time}, DP={dp_time}"
    # Note: activities might be in different order, so compare sorted names
    assert _names(dp_chosen) == _names(bf_chosen), \
        f"Activity sets differ: BF={_names(bf_chosen)}, DP={_names(dp_chosen)}"


def test_bottom_up_matches_bruteforce_on_random_instances():
    """Bottom-up DP = bruteforce optimum."""
    rng = random.Random(42)

    for trial in range(25):
        n = rng.randint(1, 14)  # Keep small so brute-force is fast
        activities = [
            Activity(
                name=f"A{i}",
                time=rng.randint(1, 7),
                cost=rng.randint(0, 200),
                enjoyment=rng.randint(1, 250),
            )
            for i in range(n)
        ]
        max_time = rng.randint(5, 20)
        event = Event(max_time=max_time, max_budget=9999, activities=activities)

        bf_chosen, bf_enjoyment, bf_time = bruteforce(event, time_limit=10.0)
        dp_chosen, dp_enjoyment, dp_time = bottom_up(event, time_limit=10.0)

        assert dp_enjoyment == bf_enjoyment, \
            f"Trial {trial}: Enjoyment mismatch: BF={bf_enjoyment}, DP={dp_enjoyment}"
        assert dp_time == bf_time, \
            f"Trial {trial}: Time used mismatch: BF={bf_time}, DP={dp_time}"
        assert _names(dp_chosen) == _names(bf_chosen), \
            f"Trial {trial}: Activity sets differ: BF={_names(bf_chosen)}, DP={_names(dp_chosen)}"


def test_bottom_up_does_not_mutate_event_activities_list():
    """The algorithm should not mutate the event activities list."""
    event = load_event_file("input_small.txt")
    snapshot = list(event.activities)

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    assert event.activities == snapshot, "Event activities list was mutated"
    # Returned activities should be drawn from the original list, not copies.
    assert all(a in snapshot for a in chosen), \
        "Returned activities not from original list"


def test_bottom_up_single_activity_that_fits():
    """Test with a single activity that fits within the constraint."""
    event = Event(
        max_time=5,
        max_budget=100,
        activities=[Activity("A", 3, 50, 100)]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    assert enjoyment == 100, f"Expected enjoyment 100, got {enjoyment}"
    assert time_used == 3, f"Expected time_used 3, got {time_used}"
    assert _names(chosen) == ["A"], f"Expected ['A'], got {_names(chosen)}"


def test_bottom_up_single_activity_that_doesnt_fit():
    """Test with a single activity that doesn't fit within the constraint."""
    event = Event(
        max_time=2,
        max_budget=100,
        activities=[Activity("A", 3, 50, 100)]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    assert enjoyment == 0, f"Expected enjoyment 0, got {enjoyment}"
    assert time_used == 0, f"Expected time_used 0, got {time_used}"
    assert chosen == [], f"Expected empty list, got {chosen}"


def test_bottom_up_all_activities_fit():
    """Test when all activities fit within the constraint."""
    event = Event(
        max_time=20,
        max_budget=500,
        activities=[
            Activity("A", 2, 10, 50),
            Activity("B", 3, 20, 80),
            Activity("C", 4, 30, 100),
        ]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    assert enjoyment == 230, f"Expected enjoyment 230, got {enjoyment}"
    assert time_used == 9, f"Expected time_used 9, got {time_used}"
    assert _names(chosen) == ["A", "B", "C"], f"Expected all activities, got {_names(chosen)}"


def test_bottom_up_must_choose_subset():
    """Test where not all activities can fit, must choose optimal subset."""
    event = Event(
        max_time=5,
        max_budget=500,
        activities=[
            Activity("A", 2, 10, 50),
            Activity("B", 3, 20, 80),
            Activity("C", 4, 30, 100),
        ]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    # Best is B + A = 130 enjoyment in 5 hours
    assert enjoyment == 130, f"Expected enjoyment 130, got {enjoyment}"
    assert time_used == 5, f"Expected time_used 5, got {time_used}"
    assert _names(chosen) == ["A", "B"], f"Expected ['A', 'B'], got {_names(chosen)}"


def test_bottom_up_identical_activities():
    """Test with identical activities (tie-breaking scenario)."""
    event = Event(
        max_time=5,
        max_budget=100,
        activities=[
            Activity("A", 2, 10, 50),
            Activity("B", 2, 10, 50),
            Activity("C", 2, 10, 50),
        ]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    # Can fit 2 activities in 5 hours (4 hours total)
    assert enjoyment == 100, f"Expected enjoyment 100, got {enjoyment}"
    assert time_used == 4, f"Expected time_used 4, got {time_used}"
    assert len(chosen) == 2, f"Expected 2 activities, got {len(chosen)}"


def test_bottom_up_backtracking_correctness():
    """Test that backtracking correctly identifies selected activities.

    This test is designed to expose bugs in the backtracking logic,
    particularly the use of wrong variables.
    """
    event = Event(
        max_time=10,
        max_budget=500,
        activities=[
            Activity("A", 2, 10, 30),
            Activity("B", 3, 20, 50),
            Activity("C", 4, 30, 70),
            Activity("D", 5, 40, 90),
            Activity("E", 2, 15, 40),
        ]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    # Verify that the activities we selected actually sum to the reported values
    actual_enjoyment = sum(a.enjoyment for a in chosen)
    actual_time = sum(a.time for a in chosen)

    assert enjoyment == actual_enjoyment, \
        f"Reported enjoyment {enjoyment} != actual {actual_enjoyment}. " \
        f"Activities: {[(a.name, a.enjoyment) for a in chosen]}"
    assert time_used == actual_time, \
        f"Reported time {time_used} != actual {actual_time}. " \
        f"Activities: {[(a.name, a.time) for a in chosen]}"

    # Also verify it matches brute force
    bf_chosen, bf_enjoyment, bf_time = bruteforce(event, time_limit=10.0)
    assert enjoyment == bf_enjoyment, \
        f"DP enjoyment {enjoyment} != BF enjoyment {bf_enjoyment}"


def test_bottom_up_large_time_constraint():
    """Test with a very large time constraint (all activities should fit)."""
    event = Event(
        max_time=1000,
        max_budget=500,
        activities=[
            Activity("A", 2, 10, 50),
            Activity("B", 3, 20, 80),
            Activity("C", 4, 30, 100),
            Activity("D", 5, 40, 120),
        ]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    # All activities should be selected
    assert enjoyment == 350, f"Expected enjoyment 350, got {enjoyment}"
    assert time_used == 14, f"Expected time_used 14, got {time_used}"
    assert len(chosen) == 4, f"Expected 4 activities, got {len(chosen)}"


def test_bottom_up_zero_time_constraint():
    """Test with zero time constraint (no activities can fit)."""
    event = Event(
        max_time=0,
        max_budget=500,
        activities=[
            Activity("A", 2, 10, 50),
            Activity("B", 3, 20, 80),
        ]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    assert enjoyment == 0, f"Expected enjoyment 0, got {enjoyment}"
    assert time_used == 0, f"Expected time_used 0, got {time_used}"
    assert chosen == [], f"Expected empty list, got {chosen}"


def test_bottom_up_activities_with_zero_enjoyment():
    """Test handling of activities with zero enjoyment value."""
    event = Event(
        max_time=10,
        max_budget=500,
        activities=[
            Activity("A", 2, 10, 0),
            Activity("B", 3, 20, 50),
            Activity("C", 4, 30, 0),
        ]
    )

    chosen, enjoyment, time_used = bottom_up(event, time_limit=10.0)

    # Should only select B
    assert enjoyment == 50, f"Expected enjoyment 50, got {enjoyment}"
    assert _names(chosen) == ["B"], f"Expected ['B'], got {_names(chosen)}"

