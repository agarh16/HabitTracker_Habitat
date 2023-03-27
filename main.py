import questionary
from db import get_db
from habit import Habit
from analyse import *


def cli():
    db = get_db()
    questionary.confirm("""Welcome to Habit@, the place for your habits to call home.
    Are you ready to start?""").ask()

    stop = False
    while not stop:

        choice = questionary.select("What do you want to do today?",
                                    choices=["Create habit", "Increment habit", "Analyse habit(s)",
                                             "Exit the program"]).ask()
        if choice == "Create habit":
            habit_type = questionary.select("Would you like to create a new habit or choose from existing ones?", choices=["New Habit", "Predetermined habits"]).ask()
            if habit_type == "New Habit":
                name = questionary.text("What's the name of your habit?").ask()
                frequency = questionary.select("What is the frequency of your habit?",
                                             choices=["daily", "weekly"]).ask()
                created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                habit = Habit(name, frequency, created)
                habit.store(db)
            else:
                predetermined_habit = questionary.select("Select one:", choices=["Exercising", "Reading",
                                                                               "Writing", "Coding",
                                                                               "Grocery Shopping"]).ask()
                frequency = questionary.select("What is the frequency of your habit?",
                                             choices=["daily", "weekly"]).ask()
                created = questionary.text("Type the first date of your new habit: (YYYY-MM-DD)").ask()
                habit = Habit(predetermined_habit, frequency, created)
                habit.store(db)
        elif choice == "Increment habit":
            habit = Habit(name, "no description")
            habit.increment()
            habit.add_event(db)
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
            print("Bye")
            stop = True


if __name__ == '__main__':
    cli()
