from datetime import date
from db import get_db, add_habit, increment_habit
from habit import Habit
import analyse


class Test_Habit:

    def setup_method(self):
        """

        :return:
        """
        self.db = get_db("test.db")
        add_habit(self.db, "test_habit_1", "daily", "2023-02-03")
        increment_habit(self.db, "test_habit_1", "2023-02-04")
        increment_habit(self.db, "test_habit_1", "2023-02-05")

        increment_habit(self.db, "test_habit_1", "2023-02-07")
        increment_habit(self.db, "test_habit_1", "2023-02-08")

    def test_habit(self):
        """

        :return:
        """
        habit = Habit("test_habit_1", "daily")

        habit.increment()
        habit.reset()
        habit.increment()

    def test_db_habit(self):

        pass

    def test_db_tracker(self):

        pass

    def teardown_method(self):
        """

        :return:
        """
        import os
        os.remove("test.db")