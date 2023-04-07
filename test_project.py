import pytest

from db import *
from habit import Habit, delete_habit
from db import is_habit_there, get_habits_data
from analysis import all_habits_same_frequency, longest_streak_of_all, longest_streak_of_habit


class TestHabit:
    def setup_method(self):
        self.db = get_db("test.db")
        add_habit(self.db, "piano", "weekly", "2014-12-11")
        increment_habit(self.db, "piano", 2, "2014-12-18")
        increment_habit(self.db, "piano", 3, "2014-12-25")
        increment_habit(self.db, "piano", 1, "2015-01-10")
        increment_habit(self.db, "piano", 1, "2015-01-18")
        increment_habit(self.db, "piano", 1, "2015-02-01")
        increment_habit(self.db, "piano", 2, "2015-02-08")


        add_habit(self.db, "writing", "daily", "2014-09-08")
        increment_habit(self.db, "writing", 2, "2014-09-09")
        increment_habit(self.db, "writing", 3, "2014-12-10")
        increment_habit(self.db, "writing", 4, "2014-12-11")
        increment_habit(self.db, "writing", 5, "2014-12-12")
        increment_habit(self.db, "writing", 1, "2014-12-14")
        increment_habit(self.db, "writing", 1, "2015-01-08")

        add_habit(self.db, "jogging", "daily", "2014-08-07")
        increment_habit(self.db, "jogging", 1, "2014-08-09")
        increment_habit(self.db, "jogging", 1, "2014-12-11")
        increment_habit(self.db, "jogging", 2, "2014-12-12")
        increment_habit(self.db, "jogging", 3, "2014-12-13")
        increment_habit(self.db, "jogging", 1, "2014-12-29")
        increment_habit(self.db, "jogging", 1, "2015-01-08")

        add_habit(self.db, "reading", "daily", "2014-10-09")
        increment_habit(self.db, "reading", 2, "2014-10-10")
        increment_habit(self.db, "reading", 1, "2014-12-12")
        increment_habit(self.db, "reading", 1, "2014-12-14")
        increment_habit(self.db, "reading", 1, "2014-12-26")
        increment_habit(self.db, "reading", 1, "2015-01-07")
        increment_habit(self.db, "reading", 1, "2015-02-02")


        add_habit(self.db, "ballet", "weekly", "2014-11-10")
        increment_habit(self.db, "ballet", 2, "2014-11-17")
        increment_habit(self.db, "ballet", 3, "2014-11-24")
        increment_habit(self.db, "ballet", 4, "2014-12-01")
        increment_habit(self.db, "ballet", 5, "2014-12-08")
        increment_habit(self.db, "ballet", 6, "2014-12-15")
        increment_habit(self.db, "ballet", 7, "2014-12-22")

    def test_habit(self):
        habit1 = Habit("test_1", "weekly", "2015-12-12")  # With date
        habit2 = Habit("test_2", "daily", None)  # Without date
        habit1.increment(self.db)
        assert habit1.streak == 1
        habit1.reset()
        assert habit1.streak == 0
        habit2.increment(self.db)
        assert habit2.streak == 1

    def test_delete_habit(self):
        with pytest.raises(NameError):
            delete_habit(self.db, "reading")
            is_habit_there(self.db, "reading")


    def test_db_habit(self):
        """
        Tests the analysis module on the habit table.
        :return:
        """
        assert len(get_habits_data(self.db)) == 5
        assert len(all_habits_same_frequency(self.db, 'daily')) == 3
        assert len(all_habits_same_frequency(self.db, 'weekly')) == 2


    def test_db_tracker(self):
        """
        Tests the analysis module on the tracker table.
        :return:
        """
        assert longest_streak_of_all(self.db) == ("ballet", 7)
        assert longest_streak_of_habit(self.db, "piano") == ("piano", 3)
        assert longest_streak_of_habit(self.db, "writing") == ("writing", 5)


    def teardown_method(self):
        import os
        os.remove("test.db")