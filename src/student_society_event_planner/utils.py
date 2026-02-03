from pathlib import Path
import argparse

from .classes import Activity, Event

def parse_args() -> argparse.Namespace:
    """Parse the command line input."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input_file")
    return arg_parser.parse_args()

def load_event_file(file_name: str) -> Event:
    """Load an event from a given file."""
    path = Path("input_files") / file_name

    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")

    with open(path) as f:
        lines = [line.strip() for line in f.read().splitlines()]

        # Read the activity count and check it is positive
        try:
            activity_count = int(lines[0])
        except ValueError or TypeError as e:
            raise ValueError("Invalid activity count.") from e
        else:
            if activity_count <= 0:
                raise ValueError("Non-positive activity count.")

        try:
            max_time, max_budget = map(int, lines[1].split())
        except ValueError or TypeError as e:
            raise ValueError("Invalid constraints.") from e
        else:
            if max_time < 0 or max_budget < 0:
                raise ValueError("Non-positive constraint(s).")

        # Read in all the activities
        try:
            activities = []

            # Check that there are the correct number of activities
            if len(lines[2:activity_count+2]) == activity_count:
                for activity_line in lines[2:activity_count+2]:
                    name, time, cost, enjoyment = activity_line.split()

                    # Create an Activity object for each activity line
                    activities.append(
                        Activity(name, int(time), int(cost), int(enjoyment))
                    )
            else:
                raise ValueError
        except ValueError or TypeError as e:
            raise ValueError("Invalid activities.") from e

        # Return an Event object
        return Event(max_time, max_budget, activities)
