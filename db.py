import sqlite3
from datetime import date


def get_db(name="main.db"):
    """

    :param name: Name of the main database.
    :return:
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """

    :param db: An initialized sqlite3 database connection.
    :return:
    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        name TEXT PRIMARY KEY, 
        frequency TEXT,
        created DATE)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        date TEXT,
        habit_name TEXT,
        FOREIGN KEY (habit_name) REFERENCES habit(name))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS streak (
        habit_name TEXT,
        streak INT,
        FOREIGN KEY (habit_name) REFERENCES tracker(habit_name))""")

    db.commit()


def add_habit(db, name, frequency, created):
    """

    :param db: An initialized sqlite3 database connection.
    :param name:
    :param frequency:
    :param created:
    :return:
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habit VALUES(?, ?, ?)", (name, frequency, created))
    db.commit()


def increment_habit(db, name, event_date=None):
    """

    :param db: An initialized sqlite3 database connection.
    :param name:
    :param event_date:
    :return:
    """
    cur = db.cursor()
    if not event_date:
        event_date = str(date.today())
    cur.execute("INSERT INTO tracker VALUES(?, ?)", (event_date, name))
    db.commit()


def get_habits_data(db, name):
    """

    :param db: An initialized sqlite3 database connection.
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit WHERE name=?", (name,))
    return cur.fetchall()

def get_tracker_data(db, habit_name):
    """

    :param db: An initialized sqlite3 database connection.
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE habit_name=?", (habit_name,))
    return cur.fetchall()


# def get_same_frequency_data(db, frequency):
#     """
#
#     :param db: An initialized sqlite3 database connection.
#     :param frequency:
#     :return:
#     """
#     cur = db.cursor()
#     cur.execute("SELECT * FROM tracker WHERE frequency=?", (frequency,))
#     return cur.fetchall()


# def get_longest_streak_of_all(db, date):
#     """
#
#     :param db: An initialized sqlite3 database connection.
#     :param name:
#     :return: returns the
#     """
#     cur = db.cursor()
#     cur.execute("SELECT * FROM tracker WHERE date==", (date,))
#     return cur.fetchall()
#
# def get_longest_streak_of_habit(db, date, habit_name):
#     cur = db.cursor()
#     cur.execute("SELECT * FROM tracker WHERE date==", (date, habit_name))
#     return cur.fetchall()