import sqlite3
import questionary
from habit import Habit
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
    from sys import exit
    exit(print("Bye."))


def main_menu():
    from db import get_db, get_habits_data, get_tracker_data, get_streak_data
    db = get_db()
    choice = questionary.select("What do you want to do today?",
                                choices=["Create habit", "Increment habit", "Analyse habit(s)",
                                         "Exit the program"]).ask()

    if choice == "Create habit":
        habit_type = questionary.select("Would you like to create a new habit or choose from existing ones?",
                                        choices=["New Habit", "Predetermined habits", "Back to main menu"]).ask()
        try:
            if habit_type == "New Habit":
                try:
                    name = questionary.text("What's the name of your habit?").ask()
                    name = name.casefold()
                    frequency = questionary.select("What is the frequency of your habit?",
                                                   choices=["daily", "weekly"]).ask()
                    created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask() # I need to rais exception for it to be a date type
                    habit = Habit(name, frequency, created)
                    habit.store(db)
                except ValueError:
                    print("Your habit was not saved because it doesn't have a name.")
                    main_menu()

            elif habit_type == "Predetermined habits":
                predetermined_habit = questionary.select("Select one:", choices=["exercising", "reading",
                                                                                 "writing", "coding",
                                                                                 "grocery shopping",
                                                                                 "Back to main menu"]).ask()
                if predetermined_habit == "grocery shopping":
                    frequency = "weekly"
                    print("You chose a weekly habit.")
                    created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                    habit = Habit(predetermined_habit, frequency, created)
                    habit.store(db)
                    print("Your habit has been saved.")
                elif predetermined_habit == "exercising" or predetermined_habit == "reading" or \
                        predetermined_habit == "writing" or predetermined_habit == "coding":
                    frequency = "daily"
                    print("You chose a daily habit.")
                    created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                    habit = Habit(predetermined_habit, frequency, created)
                    habit.store(db)
                    print("Your habit has been saved.")
                else:
                    main_menu()
            else:
                main_menu()
        except sqlite3.IntegrityError:
            print("You already have a habit with this name. Try again.")

    elif choice == "Increment habit":
        name = questionary.text("What's the name of your habit?").ask() #this
        data = get_habits_data(db) #list of all tuples
        habit_to_increment = (list(filter(lambda x: x[0] == name.casefold(), data)))
        habit_to_increment = habit_to_increment[0]
        print(">>>", habit_to_increment)
        habit = Habit(habit_to_increment[0], habit_to_increment[1], habit_to_increment[2])
        streak = habit.increment()
        print(">>>", streak)
        date_checked = questionary.text("Type the date you completed the habit (YYYY-MM-DD)").ask()
        habit.add_event(db, streak, date_checked)

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
    else:
        stop = True
        exit_habitat()


def return_to_main():
    main_menu()


if __name__ == '__main__':
    cli()
