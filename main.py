import sqlite3
from datetime import datetime

import questionary
from analyse import *


def cli():
    answer = questionary.select("""Welcome to Habitat, the place for your habits to call home.
    Are you ready to start?""", choices=["Yes", "No"]).ask()
    if answer == "No":
        exit_habitat()
    else:
        stop = False
        while not stop:
            main_menu()


def exit_habitat():
    """
    Exits the program.

    """
    from sys import exit
    exit(print("Bye."))


def main_menu():
    """
    The main menu of the program. It contains the four main tasks of the program:
        -Create habit (New or predetermined habit)
        -Increment habit
        -Analyse habit(s)
        -Delete habit
    The program connects to the main database to get the habit and tracker tables.
    """
    from habit import Habit, delete_habit
    from db import get_db, get_habits_data, get_tracker_data, check_date_format, is_habit_there

    db = get_db()
    choice = questionary.select("What do you want to do today?",
                                choices=["Create habit", "Increment habit", "Analyse habit(s)", "Delete habit",
                                         "Exit the program"]).ask()

    if choice == "Create habit":
        habit_type = questionary.select("Would you like to create a new habit or choose from existing ones?",
                                        choices=["New Habit", "Predetermined habits", "Back to main menu"]).ask()
        try:
            if habit_type == "New Habit":
                try:
                    name = questionary.text("What's the name of your habit?",
                                            validate=lambda text: True if text.isalpha()
                                            else "Not a valid name. Please only letters.").ask()
                    frequency = questionary.select("What is the frequency of your habit?",
                                                   choices=["daily", "weekly"]).ask()
                    date_created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                    habit = Habit(name.casefold(), frequency,
                                  date_created)  # Casefold to keep all names lower case letters
                    habit.store(db)
                    habit.add_event(db, date_created)
                    print("Your habit was saved.")
                    print(get_habits_data(db))
                    print(get_tracker_data(db, name))
                except NameError:  # In case the user doesn't input a name
                    print("Your habit was not saved because it doesn't have a name.")
                    main_menu()
                except ValueError:  # In case the date_created doesn't match the format YYYY-MM-DD
                    main_menu()

            elif habit_type == "Predetermined habits":
                predetermined_habit = questionary.select("Select one:", choices=["exercising", "reading",
                                                                                 "writing", "coding",
                                                                                 "grocery shopping",
                                                                                 "Back to main menu"]).ask()
                if predetermined_habit == "grocery shopping":
                    frequency = "weekly"
                    print("You chose a weekly habit.")
                    try:
                        date_created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                        habit = Habit(predetermined_habit, frequency, date_created)
                        habit.store(db)
                        habit.add_event(db, date_created)
                        print(">>>habit table", get_habits_data(db))
                        print(">>>tracker", get_tracker_data(db, habit.name))
                        print("Your habit has been saved.")
                    except ValueError:  # In case the date_created doesn't match the format YYYY-MM-DD
                        main_menu()
                elif predetermined_habit == "exercising" or predetermined_habit == "reading" or \
                        predetermined_habit == "writing" or predetermined_habit == "coding":
                    frequency = "daily"
                    print("You chose a daily habit.")
                    try:
                        date_created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                        habit = Habit(predetermined_habit, frequency, date_created)
                        habit.store(db)
                        habit.add_event(db, date_created)
                        print(">>>habit table", get_habits_data(db))
                        print(">>>tracker", get_tracker_data(db, habit.name))
                        print("Your habit has been saved.")
                    except ValueError: # In case the date_created doesn't match the format YYYY-MM-DD
                        main_menu()
                else:
                    main_menu()
            else:
                main_menu()
        except sqlite3.IntegrityError:  # Does not allow two habits with the same name
            print("You already have a habit with this name. Try again.")

    elif choice == "Increment habit":
        name = questionary.text("What's the name of your habit?").ask()
        try:
            habit_to_increment = is_habit_there(db, name) # To check if habit exists
            print(">>>", habit_to_increment)
            habit = Habit(habit_to_increment[0][0], habit_to_increment[0][1], habit_to_increment[0][2])
            print(">>>name", habit)
            if habit_to_increment[0][1] == "daily":  # If True and frequency is daily
                event_date = questionary.text("Type your date (YYYY-MM-DD)").ask()
                print(">>>event_dateincrement", event_date)
                checked_date = check_date_format(event_date) # To check the date format
                print(">>>event_dateincrement2", checked_date)
                day_difference = compare_dates(db, name, checked_date)
                print(">>>daydiff", day_difference)
                if day_difference == 1:
                    streak = habit.increment(db)
                    print("streak", streak)
                    habit.add_event(db, event_date)
                    data = get_tracker_data(db, name)
                    print(">>>", data)
                    print("You completed a daily habit!")
                elif day_difference > 1:
                    habit.reset()
                    habit.streak = 1
                    print("habitstreak", habit.streak)
                    habit.add_event(db, event_date)
                    data = get_tracker_data(db, name)
                    print(">>>", data)
                elif day_difference == 0:
                    print("Oops. It looks like you checked off your habit today.")
                else:
                    print("Oops. Not a valid date.")

            elif habit_to_increment[0][1] == "weekly": # If frequency is "weekly"
                print(">>>habitfreq", habit_to_increment[0][1])
                event_date = questionary.text("Type your date (YYYY-MM-DD)").ask()
                print(">>>event_dateincrement", event_date)
                checked_date = check_date_format(event_date)  # To check the date format
                print(">>>event_dateincrement2", checked_date)
                day_difference = compare_dates(db, name, checked_date)
                print(">>>daydiff", day_difference)
                if 7 <= day_difference < 14:
                    streak = habit.increment(db)
                    print("streak", streak)
                    habit.add_event(db, event_date)
                    data = get_tracker_data(db, name)
                    print(">>>", data)
                    print("You completed a weekly habit!")
                elif day_difference >= 14:
                    habit.reset()
                    habit.streak = 1
                    habit.add_event(db, event_date)
                elif day_difference == 0 or day_difference < 7:
                    print("Looks like you already completed your habit this week.")
                else:
                    print("Not a valid date.")

        except ValueError:
            main_menu()
        except NameError:
            main_menu()

        else:
            main_menu()

    elif choice == "Analyse habit(s)":
        analyse = questionary.select("What do you want to see?",
                                     choices=["List of all habits", "All habits with the same frequency",
                                              "Longest streak of all habits",
                                              "Longest streak of a given habit", "Back to main menu"]).ask()
        if analyse == "List of all habits":
            print(*all_habits(db), sep='\n')
        elif analyse == "All habits with the same frequency":
            print(all_habits_same_frequency(db))
        elif analyse == "Longest streak of all habits":
            habit_name = questionary.text("Type the name of your habit.").ask()
            print(*longest_streak_of_all(db, habit_name), sep='\n')
        elif analyse == "Longest streak of a given habit":
            habit_name = questionary.text("Type the name of your habit.").ask()
            print(longest_streak_of_habit(db, habit_name))
        else:
            main_menu()

    elif choice == "Delete habit":
        name = questionary.text("Type the name of the habit you want to delete.",
                                validate=lambda text: True if text.isalpha()
                                else "Not a valid name. Please only letters.").ask()
        try:
            habit_to_delete = is_habit_there(db, name)
            if habit_to_delete:
                delete_habit(db, name.casefold())
                print(f"Habit {name} deleted.")
        except NameError:
            main_menu()

    else:
        stop = True
        exit_habitat()


def compare_dates(db, name, event_date):

    data = get_tracker_data(db, name)
    date_to_compare = data[-1][2]  # Gets the last day logged
    print(">>>datetocompare", date_to_compare)
    d1 = datetime.strptime(event_date, '%Y-%m-%d')
    print("d1", d1)
    d2 = datetime.strptime(date_to_compare, '%Y-%m-%d')
    day_difference = (d1 - d2).days
    return day_difference

def return_to_main():
    main_menu()


if __name__ == '__main__':
    cli()
