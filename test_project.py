
from db import get_db, add_habit, increment_habit
from habit import Habit
from datetime import date


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")

        add_habit(self.db, "test_habit_1", "daily", "2023-02-03")
        increment_habit(self.db, "test_habit_1", 1, "2023-02-04")
        increment_habit(self.db, "test_habit_1", 2, "2023-02-05")
        increment_habit(self.db, "test_habit_1", 3, "2023-02-06")
        increment_habit(self.db, "test_habit_1", 4, "2023-02-07")
        increment_habit(self.db, "test_habit_1", 5, "2023-02-08")
        increment_habit(self.db, "test_habit_1", 6, "2023-02-09")
        increment_habit(self.db, "test_habit_1", 1, "2023-02-11")
        increment_habit(self.db, "test_habit_1", 2, "2023-02-12")
        increment_habit(self.db, "test_habit_1", 3, "2023-02-13")
        increment_habit(self.db, "test_habit_1", 4, "2023-02-14")
        increment_habit(self.db, "test_habit_1", 5, "2023-02-15")
        increment_habit(self.db, "test_habit_1", 6, "2023-02-16")
        increment_habit(self.db, "test_habit_1", 1, "2023-02-23")
        increment_habit(self.db, "test_habit_1", 2, "2023-02-24")
        increment_habit(self.db, "test_habit_1", 1, "2023-02-27")
        increment_habit(self.db, "test_habit_1", 1, "2023-03-01")
        increment_habit(self.db, "test_habit_1", 1, "2023-03-04")
        increment_habit(self.db, "test_habit_1", 1, "2023-03-06")
        increment_habit(self.db, "test_habit_1", 1, "2023-03-10")
        increment_habit(self.db, "test_habit_1", 2, "2023-03-11")
        increment_habit(self.db, "test_habit_1", 3, "2023-03-12")
        increment_habit(self.db, "test_habit_1", 1, "2023-03-13")

    def test_habit(self):
        """

        :return:
        """
        habit = Habit("test_habit_2", "daily", "2024-02-03")
        habit.add_event(self.db, "2023-02-03")
        habit.store(self.db)
        habit.increment(self.db)
        habit.reset()
        habit.increment(self.db)
        habit.delete_habit(self.db, "test_habit_2")

    def test_db_habit(self):
        pass

    def test_db_tracker(self):

        pass
    def teardown_method(self):
        import os
        os.remove("test.db")