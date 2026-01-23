import os
import argparse

class Activity:
    def __init__(self, name, time, cost, enjoyment):
        self.name = name
        self.time = time
        self.cost = cost
        self.enjoyment = enjoyment

class Event:
    def __init__(self, max_time, max_budget, activities):
        self.max_time = max_time
        self.max_budget = max_budget
        self.activities = activities

def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("input_file")
    return arg_parser.parse_args()

def load_event_file(file_name):
    """Loads an event from a given file"""
    path = os.path.join("input_files", file_name)

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.read().splitlines()]

        activity_count = int(lines[0])
        max_time, max_budget = map(int, lines[1].split())

        activities = []
        for activity_line in lines[2:activity_count+2]:
            name, time, cost, enjoyment = activity_line.split()

            activities.append(Activity(name, int(time), int(cost), int(enjoyment)))
        
        return Event(max_time, max_budget, activities)