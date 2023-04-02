from db import add_habit, increment_habit
import datetime

class Habit:

    def __init__(self, name: str, frequency: str, date_created: datetime.date):
        """Habit class to create habits. It has a name, frequency, date of creation and a count(checked)
        once it is checked off. The checked will be added to the tracker table.

        :param name: Name of the habit
        :param frequency: Periodicity of the habit (daily or weekly).
        :param created: Date of creation of habit.
        """
        self.name = name
        self.frequency = frequency
        self.date_created = date_created
        self.checked_date = datetime.date.today().strftime("Y%/%m/%d")
        self.streak = 0

    def increment(self):
        """
        This function increments the checked attribute by 1 if the habit was not broken.
        It logs the information in the tracker table.
        """
        # if the habit was not broken (iterate through list of habits and the dates):
        #     then add one to the steak att in the tracker table.

        return self.streak + 1

    def reset(self):
        self.streak = 0

    def __str__(self):
        return f"{self.name}: {self.streak}, date created: {self.date_created}"

    def store(self, db):
        """
        Stores the static information of the habits such as name, frequency,
        and date created.
        :param db: Connection to the DB.
        """
        add_habit(db, self.name, self.frequency, self.date_created)

    def add_event(self, db, streak, event_date: datetime.date = None):
        increment_habit(db, self.name, streak, event_date)


