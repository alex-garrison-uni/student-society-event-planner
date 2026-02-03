from student_society_event_planner.utils import parse_args, load_event_file
from student_society_event_planner.algorithms import bruteforce

import time

def main() -> None:
    """Program entrypoint."""
    # Parse command line arguments
    args = parse_args()

    # Try to load the passed file
    try:
        event = load_event_file(args.input_file)
    except ValueError as e:
        print(f"Error with loading event file {args.input_file}: {str(e)}")
        return

    print(
        "========================================\n"
        "EVENT PLANNER - RESULTS\n"
        "========================================\n\n"
        f"Input File: {args.input_file}\n"
        f"Available Time: {event.max_time} hours\n"
        f"Available Budget: £{event.max_budget}\n"
        "Constraint: Time"
    )

    start = time.perf_counter()
    optimal_choices = bruteforce(event, 600)
    end = time.perf_counter()

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
