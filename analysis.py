from db import get_habits_data, get_all_streaks, get_streak_data


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
    result = list(filter(lambda x: frequency in x, data))
    return result


def longest_streak_of_all(db):
    """
    Returns the longest streak of all defined habits.
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    data = get_all_streaks(db)
    max_streak = max(data, key=lambda x: x[1])
    return max_streak


def longest_streak_of_habit(db, habit_name):
    """
    Returns the longest streak of a given habit.
    :param db: An initialized sqlite3 database connection.
    :param habit_name: Name of the habit for search.
    :return:
    """
    data = get_streak_data(db, habit_name)
    max_streak = max(data, key=lambda x: x[1])
    return max_streak
