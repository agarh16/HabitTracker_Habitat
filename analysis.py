from db import get_tracker_data, get_habits_data, get_db


def all_habits(db):
    """
    Makes the items on the list to be printed one in its own line.
    :param db: An initialized sqlite3 database connection.
    :return: A list of all saved habits. Their names and frequency.
    """

    data = get_habits_data(db)
    return data


def all_habits_same_frequency(db, frequency):
    """
    Returns all the habits with the same frequency from the habits table (daily or weekly).
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    data = get_habits_data(db)
    print(">>>get_habits_data", get_habits_data(db))
    result = list(filter(lambda x: frequency in x, data))
    print(">>>", result)
    return result

def longest_streak_of_all(db):
    """
    Returns the longest streak of all defined habits.
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    data = get_tracker_data(db)
    return data

def longest_streak_of_habit(db, habit_name):
    """
    Returns the longest streak of a given habit.
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    data = get_tracker_data(db, habit_name)
    return data