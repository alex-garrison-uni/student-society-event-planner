import time
import random

import pytest

from student_society_event_planner.algorithms import bruteforce
from student_society_event_planner.classes import Activity, Event
from student_society_event_planner.utils import load_event_file

from .helpers import _names, _reference_exhaustive, _reference_optimum


def test_bruteforce_finds_known_optimum_for_sample_small_time_constraint():
    """input_small.txt has a unique best set when using time as the constraint."""
    event = load_event_file("input_small.txt")

    chosen, enjoyment, time_used = bruteforce(event, time_limit=10.0)

    # Verified by hand/exhaustive enumeration: max enjoyment under T=10 is 370.
    assert enjoyment == 370
    assert time_used == 9
    assert _names(chosen) == ["Game-Night", "Museum-Trip", "Pizza-Workshop"]
    assert sum(a.time for a in chosen) <= event.max_time


@pytest.mark.parametrize(
    "fname,max_time",
    [
        ("input_small.txt", 10),
        ("input_medium.txt", 15),
        ("input_large.txt", 20),
    ],
)
def test_bruteforce_returns_feasible_solution_on_provided_inputs(fname, max_time):
    """Sanity checks on the provided files (doesn't assert optimality for large)."""
    event = load_event_file(fname)
    chosen, enjoyment, time_used = bruteforce(event, time_limit=5.0)

    assert time_used == sum(a.time for a in chosen)
    assert enjoyment == sum(a.enjoyment for a in chosen)
    assert time_used <= max_time
    # Chosen activities must be unique instances from the event.
    assert len(chosen) == len(set(id(a) for a in chosen))
    assert all(a in event.activities for a in chosen)


def test_bruteforce_returns_empty_when_no_activity_fits():
    """Testing that the algorithm returns empty when no actviity fits."""
    event = Event(
        max_time=1,
        max_budget=999,
        activities=[
            Activity("Too-Long-1", 2, 10, 10),
            Activity("Too-Long-2", 3, 20, 100),
        ],
    )

    chosen, enjoyment, time_used = bruteforce(event, time_limit=10.0)

    assert chosen == []
    assert enjoyment == 0
    assert time_used == 0


def test_bruteforce_matches_reference_exhaustive_on_random_small_instances():
    """Brute force should hit the true optimum for small n."""
    rng = random.Random(1337)

    for _ in range(50):
        n = rng.randint(1, 12)  # keep tiny so reference is fast
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
        chosen, enjoyment, time_used = bruteforce(event, time_limit=10.0)

        # Must match the optimum enjoyment and be feasible.
        assert enjoyment == ref_enjoyment
        assert time_used == sum(a.time for a in chosen)
        assert time_used <= max_time

        # If it matches enjoyment, it should also match some optimal time used
        # (not necessarily the same subset because tie-break rules can differ).
        assert time_used == ref_time


def test_bruteforce_matches_reference_on_medium_sample_time_constraint():
    """For input_medium, validate correctness against an independent enumerator."""
    event = load_event_file("input_medium.txt")

    expected_chosen, expected_enjoyment, expected_time = _reference_optimum(event)
    chosen, enjoyment, time_used = bruteforce(event, time_limit=10.0)

    assert enjoyment == expected_enjoyment
    assert time_used == expected_time
    assert _names(chosen) == _names(expected_chosen)


def test_bruteforce_is_optimal_on_random_small_instances():
    """Property-style check: brute force equals reference optimum.

    We keep n small so the reference enumeration stays fast.
    """
    rng = random.Random(1337)
    for _ in range(25):
        n = rng.randint(1, 14)
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

        expected_chosen, expected_enjoyment, expected_time = _reference_optimum(event)
        chosen, enjoyment, time_used = bruteforce(event, time_limit=10.0)

        assert enjoyment == expected_enjoyment
        assert time_used == expected_time
        assert _names(chosen) == _names(expected_chosen)


def test_bruteforce_tie_break_prefers_skipping_earlier_activity():
    """When enjoyment ties, implementation keeps the 'skip' branch (strict >).

    With two identical activities and max_time=1, either activity is optimal.
    The recursion explores "skip first" then "take first"; since tie uses strict
    greater than, the best remains the solution that skips the first and takes the
    second.
    """
    event = Event(
        max_time=1,
        max_budget=0,
        activities=[
            Activity("A", 1, 0, 10),
            Activity("B", 1, 0, 10),
        ],
    )

    chosen, enjoyment, time_used = bruteforce(event, time_limit=10.0)

    assert enjoyment == 10
    assert time_used == 1
    assert _names(chosen) == ["B"]


def test_bruteforce_does_not_mutate_event_activities_list():
    """The algorithm should not mutate the event activities list."""
    event = load_event_file("input_small.txt")
    snapshot = list(event.activities)

    chosen, enjoyment, time_used = bruteforce(event, time_limit=10.0)

    assert event.activities == snapshot
    # Returned activities should be drawn from the original list, not copies.
    assert all(a in snapshot for a in chosen)


def test_bruteforce_does_not_mutate_event_or_activities_list():
    """The algorithm should not reorder or replace activities."""
    activities = [
        Activity("A", 1, 0, 10),
        Activity("B", 2, 0, 20),
        Activity("C", 3, 0, 30),
    ]
    event = Event(max_time=3, max_budget=0, activities=list(activities))

    _ = bruteforce(event, time_limit=10.0)

    assert event.activities == activities
