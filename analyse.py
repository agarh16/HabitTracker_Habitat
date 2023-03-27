from db import get_tracker_data, get_habits_data

def all_habits(db):
    """
    Returns a list of all currently tracked habits.
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    data = get_habits_data(db)
    return data


def all_habits_same_frequency(db):
    """
    Returns all the habits with the same frequency (daily, weekly or monthly).
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    pass


def longest_streak_of_all(db):
    """
    Returns the longest streak of all defined habits.
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    pass


def longest_streak_of_habit(db):
    """
    Returns the longest streak of a given habit.
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    pass