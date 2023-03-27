from db import add_habit, increment_habit
from datetime import date


class Habit:

    def __init__(self, name: str, frequency: str, created: str(date)):
        """Habit class to create habits.

        :param name: Name of the habit
        :param frequency: Periodicity of the habit (daily or weekly).
        """
        self.name = name
        self.frequency = frequency
        self.created = created
        self.checked = 0

    def increment(self):
        self.checked += 1

    def reset(self):
        self.checked = 0

    def __str__(self):
        return f"{self.name}: {self.checked}, created on: {self.created}"

    def store(self, db):
        """
        Stores the static information of the habits such as name, frequency,
        and date created.
        :param db: Connection to the DB.
        """
        add_habit(db, self.name, self.frequency, self.created)

    def add_event(self, db, date: str = None):
        increment_habit(db, self.name, date)