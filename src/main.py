import os
import argparse
import time

class Activity:
    """Class for activities."""
    def __init__(self, name, time, cost, enjoyment):
        self.name = name
        self.time = time
        self.cost = cost
        self.enjoyment = enjoyment

    # Custom __str__ method
    def __str__(self):
        return f"{self.name} ({self.time} hours, £{self.cost}, enjoyment {self.enjoyment})"

class Event:
    """Class for events."""
    def __init__(self, max_time, max_budget, activities):
        self.max_time = max_time
        self.max_budget = max_budget
        self.activities = activities

def parse_args():
    """Parses the command line input."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input_file")
    return arg_parser.parse_args()

def load_event_file(file_name):
    """Loads an event from a given file."""
    path = os.path.join("input_files", file_name)

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.read().splitlines()]

        # Read the activity count, and constraints
        activity_count = int(lines[0])
        max_time, max_budget = map(int, lines[1].split())

        # Read in all the activities
        activities = []
        for activity_line in lines[2:activity_count+2]:
            name, time, cost, enjoyment = activity_line.split()

            # Create an Activity object for each activity line
            activities.append(Activity(name, int(time), int(cost), int(enjoyment)))

        # Return an Event object
        return Event(max_time, max_budget, activities)

def bruteforce(event):
    """Return the optimal activity choices using a brute-force approach."""
    activities_count = len(event.activities)

    # Recursive sub-function
    def recursive_bruteforce(i, time_used, enjoyment, chosen_activities):
        # Base case for when all activities are evaluated
        if i == activities_count:
            return chosen_activities, enjoyment, time_used

        # Skip activity i
        best = recursive_bruteforce(i + 1, time_used, enjoyment, chosen_activities)

        # Check that taking activity i will not exceed the time limit
        activity = event.activities[i]
        new_time_used = time_used + activity.time
        if new_time_used <= event.max_time:
            # Take activity i
            take = recursive_bruteforce(i + 1, new_time_used, enjoyment + activity.enjoyment, chosen_activities + [activity])

            # Check if taking activity i results in more enjoyment
            if take[1] > best[1]:
                best = take

        # Return the optimal activity choices, and the time used and the enjoyment score
        return best

    # Call the recursive sub-function
    return recursive_bruteforce(0, 0, 0, [])

def main():
    args = parse_args()

    event = load_event_file(args.input_file)

    print(
        "========================================\n"
        "EVENT PLANNER - RESULTS\n"
        "========================================\n\n"
        f"Input File: {args.input_file}\n"
        f"Available Time: {event.max_time} hours\n"
        f"Available Budget: £{event.max_budget}\n"
        "Constraint: Time"
    )

    start = time.time()
    optimal_choices = bruteforce(event)
    end = time.time()

    bruteforce_time = end - start

    print(
        "\n--- BRUTE FORCE ALGORITHM ---\n"
        "Selected Activities:\n"
        + '\n'.join([f"- {str(activity)}" for activity in optimal_choices[0]]) +
        f"\n\nTotal Enjoyment: {optimal_choices[1]}\n"
        f"Total Time Used: {optimal_choices[2]} hours\n\n"
        f"Execution Time: {bruteforce_time:.5f} seconds"
    )

if __name__ == "__main__":
    main()