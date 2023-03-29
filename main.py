import questionary
from db import get_db
from habit import Habit
from analyse import *
import sys


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
    sys.exit(print("Bye."))


def main_menu():
    db = get_db()
    choice = questionary.select("What do you want to do today?",
                                choices=["Create habit", "Increment habit", "Analyse habit(s)",
                                         "Exit the program"]).ask()
    if choice == "Create habit":
        habit_type = questionary.select("Would you like to create a new habit or choose from existing ones?",
                                        choices=["New Habit", "Predetermined habits", "Back to main menu"]).ask()
        if habit_type == "New Habit":
            name = questionary.text("What's the name of your habit?").ask()
            frequency = questionary.select("What is the frequency of your habit?",
                                           choices=["daily", "weekly"]).ask()
            created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
            habit = Habit(name, frequency, created)
            habit.store(db)
        elif habit_type == "Predetermined habits":
            predetermined_habit = questionary.select("Select one:", choices=["Exercising", "Reading",
                                                                             "Writing", "Coding",
                                                                             "Grocery Shopping", "Back to main menu"]).ask()
            if predetermined_habit == "Grocery Shopping":
                frequency = "weekly"
                print("You chose a weekly habit.")
            elif predetermined_habit == "Exercising" or predetermined_habit == "Reading" or \
                    predetermined_habit == "Writing" or predetermined_habit == "Coding":
                frequency = "daily"
                print("You chose a daily habit.")
                created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                habit = Habit(predetermined_habit, frequency, created)
                habit.store(db)
            else:
                main_menu()
        else:
            main_menu()
        print("Your habit has being saved.")
        main_menu()

    elif choice == "Increment habit":
        habit = Habit(name, "no description")
        habit.increment()
        habit.add_event(db, date = None)
    elif choice == "Analyse habit(s)":
        analyse = questionary.select("What do you want to see?",
                                     choices=["List of all habits", "All habits with the same frequency",
                                              "Longest streak of all habits",
                                              "Longest streak of a given habit"]).ask()
        if analyse == "List of all habits":
            all_habits(db)
        if analyse == "All habits with the same frequency":
            all_habits_same_frequency(db)
        if analyse == "Longest streak of all habits":
            longest_streak_of_all(db)
        if analyse == "Longest streak of a given habit":
            longest_streak_of_habit(db)
    else:
        stop = True
        exit_habitat()


def return_to_main():
    main_menu()


if __name__ == '__main__':
    cli()

