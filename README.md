# Habitat

Welcome to **Habitat**, the place for your habits to call home. 

This  *little habit tracker*  lets you manage your habits.
It also offers a way to see how serious you are about maintaining them. 
Building good habits is hard and hopefully this program will help you.

## Features
Habitat lets you:

- Create new habit.
- Increment your habits for the day or the week.
- Analyse your habits:
  - Lists all your habits.
  - Show all habits with the same frequency.
  - Show the longest streak of all habits.
  - Show the longest streak of a given habit.
- Delete habit.

## Instalation

Open your Terminal/Command window and check if you have the latest pip version installed. 
On Mac, for example, type on your Terminal:

```
python3 -m pip --version 
```
To upgrade pip to the latest version type:

```
python -m pip install --upgrade pip
```

Once you have your latest pip version, go to the downloaded folder through your Terminal and type:

```
pip3 install -r requirements.txt
```

This should download the two packages to run the program:
- Pytest - To run some tests
- Questionary - For a cleaner CLI

## Usage 

After installing the packages type:
```
python3 main.py
```
and follow the instructions on screen. 

## Test suite

To run the tests go to the downloaded HabitTracker_Habitat-master folder through your terminal and type:  
```
python3 -m pytest . 
```