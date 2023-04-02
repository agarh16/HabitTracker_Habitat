import sqlite3
import datetime


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
        name TEXT,
        streak INT,
        event_date DATE NOT NULL,
        PRIMARY KEY (name, event_date),
        FOREIGN KEY (name) REFERENCES habit(name))""")

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
        date_created = datetime.date.today()
    else:
        try:
            date_created = datetime.datetime.strptime(date_created, '%Y-%m-%d')
            date_created = date_created.date() #To return a date instance without the time
        except ValueError:
            print("Not a valid date. Try this format: YYYY-MM-DD.")
            raise ValueError
    cur.execute("INSERT INTO habit VALUES(?, ?, ?)", (name, frequency, date_created))
    db.commit()


def increment_habit(db, name, streak: int, event_date: datetime.date = None ):
    """

    :param db: An initialized sqlite3 database connection.
    :param name:
    :param streak:
    :param event_date:
    :return:
    """
    cur = db.cursor()
    if not event_date:
        event_date = datetime.date.today()
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


def get_streak_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM streak WHERE name=?", (name,))
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
