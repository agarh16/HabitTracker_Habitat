import pytest

from db import *
from habit import Habit, delete_habit
from db import is_habit_there, get_tracker_data, get_habits_data
from analysis import all_habits, all_habits_same_frequency, longest_streak_of_all, longest_streak_of_habit


class TestHabit:

    def setup_method(self):
        self.db = get_db("test.db")


    def test_habit(self):
        habit1 = Habit("jogging", "weekly", "2014-12-12")
        habit.store(self.db)
        assert is_habit_there(self.db, "jogging")
        add_habit(self.db, "reading", "daily", "2023-02-03")
        assert is_habit_there(self.db, "reading")

    def test_habit_increment_reset(self):
        habit = Habit("writing", "daily", "2023-01-01")
        habit.increment(self.db)
        assert habit.streak == 1
        habit.reset()
        assert habit.streak == 0


    def test_delete_habit(self):
        with pytest.raises(NameError):
            delete_habit(self.db, "reading")
            is_habit_there(self.db, "reading")

    def test_db_habit(self):
        """
        Tests the analysis module
        :return:
        """
        habit = Habit("jogging", "weekly", "2014-12-12")
        habit.store(self.db)
        habit = Habit("writing", "weekly", "2017-11-09")
        habit.store(self.db)
        habit = Habit("ballet", "daily", "2020-10-14")
        habit.store(self.db)
        assert len(get_habits_data(self.db)) == 3
        assert len(all_habits_same_frequency(self.db, 'daily')) == 1
        assert len(all_habits_same_frequency(self.db, 'weekly')) == 2


    def test_db_tracker(self):
         pass

    # increment_habit(self.db, "test_habit_1", 1, "2023-02-04")
    #     increment_habit(self.db, "test_habit_1", 2, "2023-02-05")
    #     increment_habit(self.db, "test_habit_1", 3, "2023-02-06")
    #     increment_habit(self.db, "test_habit_1", 4, "2023-02-07")
    #     increment_habit(self.db, "test_habit_1", 5, "2023-02-08")
    #     increment_habit(self.db, "test_habit_1", 6, "2023-02-09")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-02-11")
    #     increment_habit(self.db, "test_habit_1", 2, "2023-02-12")
    #     increment_habit(self.db, "test_habit_1", 3, "2023-02-13")
    #     increment_habit(self.db, "test_habit_1", 4, "2023-02-14")
    #     increment_habit(self.db, "test_habit_1", 5, "2023-02-15")
    #     increment_habit(self.db, "test_habit_1", 6, "2023-02-16")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-02-23")
    #     increment_habit(self.db, "test_habit_1", 2, "2023-02-24")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-02-27")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-03-01")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-03-04")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-03-06")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-03-10")
    #     increment_habit(self.db, "test_habit_1", 2, "2023-03-11")
    #     increment_habit(self.db, "test_habit_1", 3, "2023-03-12")
    #     increment_habit(self.db, "test_habit_1", 1, "2023-03-13")
    #     """
    #     Tests the analysis module.
    #     :return:
    #     """
    #     all_habits(self.db)
    #     all_habits_same_frequency(self.db, "daily")
    #     all_habits_same_frequency(self.db, "weekly")

    #
    #     add_habit(self.db, "test_habit_3", "weekly", "2013-12-12")
    #     increment_habit(self.db, "test_habit_3", 1, "2013-12-15")
    #     increment_habit(self.db, "test_habit_3", 2, "2013-12-19")
    #     increment_habit(self.db, "test_habit_3", 3, "2013-12-27")
    #     # increment_habit(self.db, "test_habit_2", 1, "2013-12-12")
    #     # increment_habit(self.db, "test_habit_2", 1, "2013-12-12")
    #     # increment_habit(self.db, "test_habit_2", 1, "2013-12-12")
    #     # increment_habit(self.db, "test_habit_2", 1, "2013-12-12")
    #     # increment_habit(self.db, "test_habit_2", 1, "2013-12-12")
    #     # increment_habit(self.db, "test_habit_2", 1, "2013-12-12")
    #     # increment_habit(self.db, "test_habit_2", 1, "2013-12-12")
    #     habit = Habit("test_habit_2", "daily", "2024-02-03")
    #     habit.add_event(self.db, "2024-02-05")
    #     habit.add_event(self.db)  # No date necessary
    #     habit.store(self.db)
    #     habit.increment(self.db)
    #     habit.reset()
    #     habit.increment(self.db)
    #     habit.delete_habit(self.db, "test_habit_2")
    #
    #
    def teardown_method(self):
        import os
        os.remove("test.db")