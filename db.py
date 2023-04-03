import sqlite3
from datetime import datetime, date

def get_db(name="main.db"):
    """
    Creates the database. As a default it creates the "main" database.
    :param name: Name of the database.
    :return: A database
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Created two tables. The habit and the tracker tables.
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        name TEXT PRIMARY KEY, 
        frequency TEXT,
        created DATE)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        name TEXT,
        streak INT,
        event_date DATE NOT NULL,
        PRIMARY KEY (name, event_date),
        FOREIGN KEY (name) REFERENCES habit(name)
            ON DELETE CASCADE)""")

    # cur.execute("""CREATE TABLE IF NOT EXISTS streak (
    #     name TEXT,
    #     streak INT,
    #     FOREIGN KEY (name) REFERENCES tracker(name))""")

    db.commit()


def add_habit(db, name, frequency, date_created):
    """

    :param db: An initialized sqlite3 database connection.
    :param name:
    :param frequency:
    :param date_created:
    :return:
    """
    cur = db.cursor()
    if not name:
        raise NameError
    elif not date_created:
        date_created = date.today()
    else:
        check_date_format(date_created)
    cur.execute("INSERT INTO habit VALUES(?, ?, ?)", (name, frequency, date_created))
    db.commit()


def increment_habit(db, name, streak: int, event_date: date = None ):
    """

    :param db: An initialized sqlite3 database connection.
    :param name:
    :param streak:
    :param event_date:
    :return:
    """
    cur = db.cursor()
    if not event_date:
        event_date = date.today()
    else:
        check_date_format(event_date)

    cur.execute("INSERT INTO tracker VALUES(?, ?, ?)", (name, streak, event_date))
    db.commit()


# def increment_streak(db, name, event_date=None)
#     cur = db.cursor()
#     if not event_date:
#         event_date = str(date.today())
#     cur.execute("INSERT INTO streak VALUES(?, ?)", (name, event_date))
#     db.commit()

def get_habits_data(db):
    """

    :param name:
    :param db: An initialized sqlite3 database connection.
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit")
    return cur.fetchall()

def get_tracker_data(db, name):
    """

    :param db: An initialized sqlite3 database connection.
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE name=?", (name,))
    return cur.fetchall()


# def get_streak_data(db, name):
#     cur = db.cursor()
#     cur.execute("SELECT * FROM streak WHERE name=?", (name,))
#     return cur.fetchall()

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
#     cur.execute("SELECT * FROM tracker WHERE date=?", (date,))
#     return cur.fetchall()
#
# def get_longest_streak_of_habit(db, date, habit_name):
#     cur = db.cursor()
#     cur.execute("SELECT * FROM tracker WHERE date=?", (date, habit_name))
#     return cur.fetchall()

def delete_habit(db, name):
    """

    :param db: An initialized sqlite3 database connection.
    :param name:
    :return:
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE name=?", (name,))
    db.commit()


def check_date_format(event_date):
    """

    :param event_date:
    :return:
    """
    try:
        event_date = datetime.strptime(event_date, '%Y-%m-%d')
        event_date = event_date.date()  # To return a date instance without the time
        return event_date
    except ValueError:
        print("Not a valid date. Try this format: YYYY-MM-DD.")
        raise ValueError