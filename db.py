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
        created TIMESTAMP)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker (
        name TEXT,
        streak INT,
        event_date TIMESTAMP NOT NULL,
        PRIMARY KEY (name, event_date),
        FOREIGN KEY (name) REFERENCES habit(name)
            ON DELETE CASCADE)""")

    db.commit()


def add_habit(db, name, frequency, date_created: date):
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


def increment_habit(db, name, streak: int, event_date: date = None):
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


def get_habits_data(db):
    """

    :param db: An initialized sqlite3 database connection.
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit")
    return cur.fetchall()


def get_tracker_data(db, name):
    """

    :param db: An initialized sqlite3 database connection.
    :param name:
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
    cur.execute("DELETE FROM tracker WHERE name=?", (name,))
    db.commit()
    cur.close()


def check_date_format(event_date=None):
    if not event_date:
        event_date = datetime.today().strftime('%Y-%m-%d')

        #event_date = event_date.date()
        print("eventdate", event_date)
        return event_date
    else:
        try:
            print("eventdate", event_date)
            event_date = datetime.strptime(event_date, '%Y-%m-%d')
            event_date = event_date.date()  # To return a date instance without the time
            return event_date
        except ValueError:
            print("Not a valid date. Try this format: YYYY-MM-DD.")
            raise ValueError
    return event_date

def is_habit_there(db, name):
    """

    :param db: An initialized sqlite3 database connection.
    :param name: Name of the habit to check if exists.
    :return: The habit that matches with the name as a tuple inside a list.
    """
    data = get_habits_data(db)  # list of all tuples
    habit_to_search = (list(filter(lambda x: x[0] == name.casefold(),
                                       data)))  # Compares all habits names in the table with the name variable
    if habit_to_search:
        return habit_to_search
    else:
        print("There is no habit with this name.")
        raise NameError


def get_streak_data(db, name):
    """
    Gets the streaks from the tracker table
    :param db:
    :param name:
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT streak FROM tracker WHERE name=?", (name, ))
    return cur.fetchall()


def get_frequency(db, name):
    cur = db.cursor()
    cur.execute("SELECT frequency FROM habit WHERE name=?", (name,))
    return cur.fetchall()