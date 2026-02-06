"""
Shared helper functions for testing algorithms.
"""

from student_society_event_planner.classes import Activity, Event


def _names(chosen):
    """Return sorted activity names for order-independent assertions.

    Args:
        chosen: List of Activity objects

    Returns:
        Sorted list of activity names

    Example:
        >>> activities = [Activity("B", 1, 10, 20), Activity("A", 2, 15, 30)]
        >>> names(activities)
        ['A', 'B']
    """
    return sorted(a.name for a in chosen)


def _reference_exhaustive(event: Event) -> tuple[list[Activity], int, int]:
    """Small, clear reference implementation for correctness checks.

    Enumerates all subsets and returns (chosen, enjoyment, time_used).
    Tie-break: prefer smaller time_used, then lexicographically smaller names.

    Note: This is intentionally different from the recursive solver's tie-break.
    Tests that use this compare only the objective value unless a
    specific tie-break is being checked.

    Args:
        event: Event object containing activities and constraints

    Returns:
        Tuple of (chosen_activities, total_enjoyment, time_used)

    Warning:
        This function has O(2^n) complexity and should only be used
        for testing with small values of n (typically n <= 20).
    """
    best_chosen: list[Activity] = []
    best_enjoyment = 0
    best_time = 0

    n = len(event.activities)
    for mask in range(1 << n):
        time_used = 0
        enjoyment = 0
        chosen: list[Activity] = []
        for i in range(n):
            if mask & (1 << i):
                a = event.activities[i]
                time_used += a.time
                enjoyment += a.enjoyment
                chosen.append(a)

        if time_used <= event.max_time:
            if enjoyment > best_enjoyment:
                best_chosen, best_enjoyment, best_time = chosen, enjoyment, time_used
            elif enjoyment == best_enjoyment:
                # Stable tie-break to make the reference deterministic.
                if time_used < best_time:
                    best_chosen, best_enjoyment, best_time = chosen, enjoyment, time_used
                elif time_used == best_time:
                    if _names(chosen) < _names(best_chosen):
                        best_chosen, best_enjoyment, best_time = chosen, enjoyment, time_used

    return best_chosen, best_enjoyment, best_time


def _reference_optimum(event: Event) -> tuple[list[Activity], int, int]:
    """Compute the true optimum via explicit subset enumeration.

    This is an alternative reference implementation with slightly different
    tie-breaking behavior than reference_exhaustive. Used for validation
    in some tests.

    Args:
        event: Event object containing activities and constraints

    Returns:
        Tuple of (chosen_activities, total_enjoyment, time_used)
    """
    best_choice: list[Activity] = []
    best_enjoyment = 0
    best_time = 0

    n = len(event.activities)
    for mask in range(1 << n):
        time_used = 0
        enjoyment = 0
        chosen: list[Activity] = []
        for i in range(n):
            if (mask >> i) & 1:
                a = event.activities[i]
                time_used += a.time
                if time_used > event.max_time:
                    break
                enjoyment += a.enjoyment
                chosen.append(a)
        else:
            if enjoyment > best_enjoyment:
                best_choice = chosen
                best_enjoyment = enjoyment
                best_time = time_used

    return best_choice, best_enjoyment, best_time