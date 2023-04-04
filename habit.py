from db import add_habit, increment_habit, delete_habit, get_streak_data
from datetime import datetime, date


class Habit:

    def __init__(self, name: str, frequency: str, date_created: date):
        """Habit class to create habits. It has a name, frequency, date of creation and a count(checked) that is
        initialized in 0.

        :param name: Name of the habit
        :param frequency: Periodicity of the habit (daily or weekly).
        :param date_created: Date of creation of habit.
        """
        self.name = name
        self.frequency = frequency
        self.date_created = date_created
        self.streak = 0

    def increment(self, db):
        """
        This function increments the checked attribute by 1.

        """
        data = get_streak_data(db, self.name)
        self.streak = data[-1][-1]
        print(">>>self.streak", self.streak)
        self.streak += 1
        return self.streak
        print(">>>increment", self.streak)

    def reset(self):
        """
        Sets the streak count to 0.
        :return:
        """
        self.streak = 0

    def __str__(self):
        return f"{self.name}: {self.streak}, date created: {self.date_created}"

    def store(self, db):
        """
        Stores the static information of the habits such as name, frequency,
        and date created.
        :param db: An initialized sqlite3 database connection.
        """
        add_habit(db, self.name, self.frequency, self.date_created)

    def add_event(self, db, event_date: date = None):
        """
        If the habit was not broken then the increment_streak will be added to the one logged in the tracker table.
        If the habit is broken then the streak will result in 1 and it will be logged as such in the tracker table.
        A broken daily habit means that the habit was not logged on a consecutive day.
        A broken weekly habit means that the habit was not logged in the consecutive week.
        The information is logged in the tracker table.
        :param db: An initialized sqlite3 database connection.
        :param event_date: The date in which a habit is checked off.

        """
        increment_habit(db, self.name, self.streak, event_date)


    def delete_habit(self, db, name):
        """
        Deletes a habit.
        :param db: An initialized sqlite3 database connection.
        :param name: Name of the habit that will be deleted.
        """
        delete_habit(db, name)


