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

def bottom_up(event: Event, time_limit: float) -> tuple[list[Activity], int, int]:
    activities_count = len(event.activities)
    max_time = event.max_time

    #Create a DP table for the bottom-up approach
    dp = [[0 for _ in range(max_time + 1)] for _ in range(activities_count + 1)]

    #Fill the DP table
    for i in range(1, activities_count + 1):
        activity = event.activities[i - 1]
        for j in range(max_time + 1):
            dp[i][j] = dp[i - 1][j]

            if activity.time <= j:
                enjoyment_count = dp[i - 1][j - activity.time] + activity.enjoyment
                dp[i][j] = max(dp[i][j], enjoyment_count)

    max_enjoyment = 0
    time_used = 0
    for i in range(max_time + 1):
        if dp[activities_count][i] > max_enjoyment:
            max_enjoyment = dp[activities_count][i]
            time_used = i

    #backtracking the activities chosen
    chosen_activites = []
    i = activities_count
    t = time_used

    while i > 0 and max_enjoyment > 0:
        #if the value is different from the previous row, we don't take it
        if dp[i][t] != dp[i - 1][t]:
            choose = event.activities[i - 1]
            chosen_activites.append(choose)
            max_enjoyment -= activity.enjoyment
            t -= activity.time
        i -= 1

    return chosen_activites, dp[activities_count][time_used], time_used