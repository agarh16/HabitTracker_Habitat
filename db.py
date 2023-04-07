import sqlite3
from datetime import date, datetime


def get_db(name="main.db"):
    """
    Creates the database and tables (habit and tracker). As a default it creates the "main" database.
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
    Stores the habit in the habit table. If there is no date given, the program enters the present day.
    :param db: An initialized sqlite3 database connection.
    :param name: Habit name
    :param frequency: Habit frequency (daily or weekly)
    :param date_created: Date given by the user or set automatically if there is no user input.
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
    Logs the streak and date of the habits. If there is no date given, the program enters the present day.
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
        check_date_format(event_date) # To check if the user gave the correct date format

    cur.execute("INSERT INTO tracker VALUES(?, ?, ?)", (name, streak, event_date))
    db.commit()


def get_habits_data(db):
    """
    Gets the all the habits, frequency and date created from the table habit.
    :param db: An initialized sqlite3 database connection.
    :return: A list with all the habits, frequencies and dates created as a tuple for each.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit")
    return cur.fetchall()


def get_tracker_data(db, name):
    """
    Gets the logs from the tracker table from a given habit.
    :param db: An initialized sqlite3 database connection.
    :param name: Name of the habit for the search
    :return: A list of all the logs of  a given habit.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE name=?", (name,))
    return cur.fetchall()

def get_streak_data(db, name):
    """
    Gets the logged streaks from the tracker table.
    :param db: An initialized sqlite3 database connection.
    :param name: Name of the habit for the search.
    :return: A list of tuples. One for each logged increment.
    """
    cur = db.cursor()
    cur.execute("SELECT name, streak FROM tracker WHERE name=?", (name, ))
    return cur.fetchall()


def get_frequency(db, name):
    """
    Gets the logged frequency of the habits from the habit table.
    :param db: An initialized sqlite3 database connection.
    :param name: Name of the habit for the search.
    :return:
    """
    cur = db.cursor()
    cur.execute("SELECT frequency FROM habit WHERE name=?", (name,))
    return cur.fetchall()


def get_all_streaks(db):
    """
        Gets the logged streaks of all habits from the tracker table.
        :param db: An initialized sqlite3 database connection.
        :param : Name of the habit for the search.
        :return:
        """
    cur = db.cursor()
    cur.execute("SELECT name, streak FROM tracker")
    return cur.fetchall()


def delete_habit(db, name):
    """
    Deletes a selected habit from the habit and tracker tables.
    :param db: An initialized sqlite3 database connection.
    :param name: Name of the habit for the search.
    :return:
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE name=?", (name,))
    cur.execute("DELETE FROM tracker WHERE name=?", (name,))
    db.commit()
    cur.close()


def check_date_format(event_date=None):
    """

    :param event_date:
    :return:
    """
    if not event_date:
        event_date = datetime.today().strftime('%Y-%m-%d')
        return event_date
    else:
        try:
            event_date = datetime.strptime(event_date, '%Y-%m-%d')
            event_date_string = event_date.strftime('%Y-%m-%d')
            return event_date_string
        except ValueError:
            print("Not a valid date. Try this format: YYYY-MM-DD.")
            raise ValueError


def is_habit_there(db, name):
    """
    Checks it the habit exists in the habit table.
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


