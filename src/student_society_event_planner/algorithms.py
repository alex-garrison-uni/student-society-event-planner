import time
import sys

from .classes import Activity, Event

# Recursion limit increased to handle larger numbers of activities
sys.setrecursionlimit(1000)

def bruteforce(event: Event, time_limit: float) -> tuple[list[Activity], int, int]:
    """Return the optimal activity choices using a brute-force approach."""
    activities_count = len(event.activities)
    start = time.perf_counter()

    # Recursive sub-function
    def recursive_bruteforce(
        i: int,
        time_used: int,
        enjoyment: int,
        chosen_activities: list[Activity]
    ) -> tuple[list[Activity], int, int]:
        current_time = time.perf_counter()
        elapsed_time = current_time - start

        # Base case for when all activities are evaluated or the time limit is reached
        if elapsed_time >= time_limit or i == activities_count:
            return chosen_activities.copy(), enjoyment, time_used

        # Skip activity i
        best = recursive_bruteforce(i + 1, time_used, enjoyment, chosen_activities)

        # Check that taking activity i will not exceed the time limit
        activity = event.activities[i]
        new_time_used = time_used + activity.time
        if new_time_used <= event.max_time:
            # Take activity i
            chosen_activities.append(activity)

            take = recursive_bruteforce(
                i + 1,
                new_time_used,
                enjoyment + activity.enjoyment,
                chosen_activities
            )

            chosen_activities.pop()

            # Check if taking activity i results in more enjoyment
            if take[1] > best[1]:
                best = take

        # Return the optimal activity choices, and the time used and the enjoyment score
        return best

    # Call the recursive sub-function
    return recursive_bruteforce(0, 0, 0, [])
