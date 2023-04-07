import sqlite3
from datetime import datetime
import questionary
from analysis import *
from db import get_tracker_data


def cli():
    print("Welcome to Habitat, the place for your habits to call home.")
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
    The core of the program. Habitat is a habit tracker that allows a user to manage daily and weekly habits.
    The following options to choose from are:
        -Create habit
            - When creating a habit there is an option to choose its frequency and date of creation. If there is no
                creation date then it will automatically save the present date.
        -Increment habit. Takes the option of a user input to increment or check off a daily or weekly habit.
        If there is no input, the program will save the present date.
        -Analyse habit(s).
            - Lists all habits.
            - All habits with the same frequency.
            - Shows the longest streak among all habits.
            - Shows the longest streak of a given habit.
        -Delete habit. Deletes a habit chosen by the user.
        -Exit Habitat. Exits the program.
    The program connects to the main database to get the habit and tracker tables.
    """
    from habit import Habit, delete_habit
    from db import get_db, get_habits_data, get_tracker_data, is_habit_there, check_date_format

    db = get_db()  # Creates the main database
    choice = questionary.select("What do you want to do today?",
                                choices=["Create habit", "Increment habit", "Analyse habit(s)", "Delete habit",
                                         "Exit Habitat"]).ask()

    if choice == "Create habit":
        habit_type = questionary.select("Would you like to create a new habit?", choices=["New Habit", "Back to main "
                                                                                                       "menu"]).ask()

        if habit_type == "New Habit":
            try:
                name = questionary.text("What's the name of your habit?",
                                        validate=lambda text: True if text.isalpha()
                                        else "Not a valid name. Please only letters.").ask()
                frequency = questionary.select("What is the frequency of your habit?",
                                               choices=["daily", "weekly"]).ask()
                date_created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD) or use the "
                                                "Return key to save the present date.").ask()
                habit = Habit(name.casefold(), frequency,
                              date_created)  # Casefold to keep all names lower case letters
                habit.store(db)
                habit.increment(db)
                habit.add_event(db, date_created)
                print("Your habit was saved.")
                #print(">>> get_habits_data(db)", get_habits_data(db))
                #print(">>> get_tracker_data(db, name)", get_tracker_data(db, name))
            except NameError:  # In case the user doesn't input a name
                print("Your habit was not saved because it doesn't have a name.")
                main_menu()
            except ValueError:  # In case the date_created doesn't match the format YYYY-MM-DD
                main_menu()
            except sqlite3.IntegrityError:  # Does not allow two habits with the same name
                print("You already have a habit with this name. Try again.")
                main_menu()
        else:
            main_menu()

    elif choice == "Increment habit":
        print("Here are your habits:", *get_habits_data(db), sep='\n')
        name = questionary.text("Type the name of the habit to increment or 'back' to go back to the main menu").ask()
        if name == "back":
            main_menu()
        else:
            try:
                habit_to_increment = is_habit_there(db, name)  # To check if habit exists
                #print(">>> habit_to_increment", habit_to_increment)
                habit = Habit(habit_to_increment[0][0], habit_to_increment[0][1], habit_to_increment[0][2])
                #print(">>> habit name", habit)
                if habit_to_increment[0][1] == "daily":  # If True and frequency is daily
                    event_date = questionary.text("Type your date (YYYY-MM-DD) or use the Return key to add the present "
                                                  "day.").ask()
                    #print(">>> event_date_increment", event_date)
                    checked_date = check_date_format(event_date)  # To check the date format
                    #print(">>> event_date increment2", checked_date)
                    day_difference = compare_dates(db, name, checked_date)
                    #print(">>> daydiff", day_difference)
                    if day_difference == 1:
                        habit.increment(db)
                        habit.add_event(db, checked_date)
                        print("You completed a daily habit!. Looks like you are on a streak...")
                        print(get_tracker_data(db, name)[-1])
                    elif day_difference > 1:
                        habit.reset()
                        habit.streak = 1
                        habit.add_event(db, checked_date)
                        print("You completed a daily habit!")
                        print(get_tracker_data(db, name)[-1])
                    elif day_difference == 0:
                        print("Oops. It looks like you checked off your habit today.")
                    else:
                        print("Oops. Not a valid date.")

                elif habit_to_increment[0][1] == "weekly": # If frequency is "weekly"
                    event_date = questionary.text("Type your date (YYYY-MM-DD) or use the Return key to add the present"
                                                  "day.").ask()
                    checked_date = check_date_format(event_date)  # To check the date format

                    day_difference = compare_dates(db, name, checked_date)

                    if 7 <= day_difference < 14:
                        habit.increment(db)
                        habit.add_event(db, checked_date)
                        print("You completed a weekly habit! Looks like are on a streak...", get_tracker_data(db, name)[-1])
                    elif day_difference >= 14:
                        habit.reset()
                        habit.streak = 1
                        habit.add_event(db, checked_date)
                        print("You completed a weekly habit!", get_tracker_data(db, name)[-1])
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
            frequency = questionary.select("Which habits do you want to see?", choices=["daily", "weekly"]).ask()
            print(*all_habits_same_frequency(db, frequency), sep='\n')
        elif analyse == "Longest streak of all habits":
            print(longest_streak_of_all(db))
        elif analyse == "Longest streak of a given habit":
            habit_name = questionary.text("Type the name of your habit.").ask()
            print(longest_streak_of_habit(db, habit_name))
        else:
            main_menu()

    elif choice == "Delete habit":
        print("Here are your habits:", *get_habits_data(db), sep='\n')
        name = questionary.text("Type the name of the habit you want to delete or 'back' to go back to the main menu",
                                validate=lambda text: True if text.isalpha()
                                else "Not a valid name. Please only letters.").ask()
        if name == "back":
            main_menu()
        else:
            try:
                habit_to_delete = is_habit_there(db, name)
                if habit_to_delete:
                    delete_habit(db, name.casefold())
                    print(f"Habit {name} deleted.")
            except NameError:
                main_menu()

    else:
        exit_habitat()


def compare_dates(db, name, event_date):
    """
    Compares the date of the last logged increment with the date given by the user for the new log.
    :param db: An initialized sqlite3 database connection.
    :param name: Name of the habit to check.
    :param event_date: Date given by the user or the present date added by the program if the user gives no input.
    :return: day difference in INT.
    """

    data = get_tracker_data(db, name)
    date_to_compare = data[-1][2]  # Gets the last day logged
    #print(">>>datetocompare", date_to_compare)
    d1 = datetime.strptime(event_date, '%Y-%m-%d')
    #print("d1", d1)
    d2 = datetime.strptime(date_to_compare, '%Y-%m-%d')
    day_difference = (d1 - d2).days
    return day_difference


def return_to_main():
    """
    Returns to the main_menu().
    :return:
    """
    main_menu()


if __name__ == '__main__':
    cli()
