class Activity:
    """Class for activities."""

    def __init__(self, name: str, time: int, cost: int, enjoyment: int):
        self.name = name
        self.time = time
        self.cost = cost
        self.enjoyment = enjoyment

    # Custom __str__ method
    def __str__(self):
        return (
            f"{self.name} ({self.time} hours, "
            f"£{self.cost}, enjoyment {self.enjoyment})"
        )

class Event:
    """Class for events."""

    def __init__(self, max_time: int, max_budget: int, activities: list[Activity]):
        self.max_time = max_time
        self.max_budget = max_budget
        self.activities = activities
