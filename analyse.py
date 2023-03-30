from db import get_tracker_data, get_habits_data, get_db


def all_habits(db):
    """
    Makes the items on the list to be printed one in its own line.
    :param db: An initialized sqlite3 database connection.
    :return: A list of all saved habits. Their names and frequency.
    """

    data = get_habits_data(db)
    return data


def all_habits_same_frequency(db):
    """
    Returns all the habits with the same frequency (daily or weekly).
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    data = list(filter(get_habits_data()))


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