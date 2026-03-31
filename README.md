# Habit Tracking Application

## Description
The application allows users to create habits, track their completion, and analyse their progress over time.

## Demonstration 
(TODO / Adding later)

## Installation
Step-by-step instructions to get the project running.

macOs:
1. Install Xcode Command Line Tools (git, curl, build):
```
xcode-select --install
```

2. Install Homebrew (makes installing python easy)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

3. Install Python 3 and Git via Homebrew
```
brew update
brew install python git
```
-> If you skipped Homebrew, step 1 already gave you git; install Python from python.org instead.

4. Clone my habit tracker repository 
```
git clone https://github.com/iljavaskov/habit_tracker.git
```

5. Create and active a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

6. Install the app dependencies and pytest:
```
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
```

## Usage
Run the app from the /habit_tracker directory:
```
python3 main.py
```
After the welcoming texts, the Start Menu will appear:
```
|---------------------------------------------------|
|Choose an option from the start menu:              |
|[1] Enter 1 to List all habits                     |
|[2] Enter 2 to Add, Manage, and Delete habits      |
|[3] Enter 3 to Mark a habit Completed              |
|[4] Enter 4 to Analyse your habits                 |
|[5] Enter 5 to Generate and Load Example Habits    |
|[6] Enter 6 to Remove the Example Habits           |
|[Q] Enter Q to Quit the Habit Tracker Application  |
|---------------------------------------------------|
```
Now, you can choose between multiple options from the Start Menu.
1. List all habits: 
	- This will return all the currently tracked habits

2. Add, Manage, and Delete habits:
	- This will forward you to the Habit Manager Menu (see the Menu below)

3. Mark a habit Completed:
	- This returns some reminders about habits, that need to be completed today in order to keep or establish a streak
	- Enter the name of the habit that needs to be marked completed
	- If it is not completed, it will add the today's date to the completion dates
	- If there are multiple habits with the same name, it will always check off the first one in the habits list
	- It will save the new date into the database

4. Analyze your habits:
	- This will forward you to the Analytics Menu (see the Menu below)

5. Generate and Load Example Habits:
	- This will generate 5 example habits with random completion dates within the past 4 weeks
	- It will not allow you to generate them again, while you have any habits with the keyword "Example" in their description

6. Remove the Example Habits:
	- This will remove all habits containing the keyword "Example" in their description
	- Including the deletion from the database as well

7. Option Quit:
	- Enter "Q","q","quit","Quit","exit","Exit"
	- Removing Example habits
	- App termination

If you chose 2 from the Start Menu, the Habit Manager Menu will appear:
```
|---------------------------------------------------|
|Choose an option from the habit manager menu:      |
|[1] Enter 1 to List all habits                     |
|[2] Enter 2 to Add a new habit                     |
|[3] Enter 3 to Delete an existing habit            |
|[4] Enter 4 to Change existing habits              |
|[B] Enter B to Go Back to the Start Menu           |
|[Q] Enter Q to Quit Habit Tracker Application      |
|---------------------------------------------------|
```
1. List all habits: 
	- This will return all the currently tracked habits

2. Add a new habit:
	- This will request inputs for the name, description and periodicity
	- Note: The keyword "Example" in the description will lead to automatic deletion.
	- Only daily and weekly periodicity supported
	- It will save the new habit into the database

3. Delete an existing habit:
	- Enter the name of the habit that needs to be deleted from everywhere
	- Note: If there are multiple habits with the same name, the first one will be deleted from the list. It is recommended to change some habits' names before deleting the wrong habit accidentally.

4. Change existing habits:
	- Enter the name of the habit that needs to be changed
	- Follow questionnaire and answer the questions regarding the what to change.
	- Note: The keyword "Example" in the description will lead to automatic deletion.
	- It will save the updated habit into the database

5. Option Back:
	- Enter "B", "b","Back","back","cancel",or "Cancel"
	- Retuns you to the Start Menu

6. Option Quit:
	- Enter "Q","q","quit","Quit","exit","Exit"
	- Removing Example habits
	- App termination


If you chose 4 from the Start Menu, the Analytics Menu will appear:
```
|----------------------------------------------------------------|
|Choose an option from the analytics functions:                  |
|[1] Enter 1 to List all habits                                  |
|[2] Enter 2 to List all habits by periodicity                   |
|[3] Enter 3 to Return the longest run streak of all habits      |
|[4] Enter 4 to Return the longest run streak for a given habit  |
|[B] Enter B to Go Back to the Start Menu                        |
|[Q] Enter Q to Quit Habit Tracker Application                   |
|----------------------------------------------------------------|
```
Note: 
Weekly habits calculation set's the first check off date as a start date and a deadline date +7 days from the start date. 
It needs to be completed within this week. After, the deadline date is set to be next start date. 
If the check off was missed, the streak is resetted and the new date is the start date.
Multiple check offs within the start date and deadline date will not result in streak increase.

1. List all habits: 
	- This will return all the currently tracked habits

2. List all habits by periodicity:
	- Enter the periodicity type of the habits that needs to be listed
	- This will return all the currently tracked habits of the choosen periodicity

3. Return the longest run streak of all habits:
	- This returns the best-performing habit and its current longest streak

4. Return the longest run streak for a given habit:
	- Enter the name of the habit to calculate it's current streak and overall longest streak (highscore)
	- This returns the habit's current streak (and longest streak)

5. Option Back:
	- Enter "B", "b","Back","back","cancel",or "Cancel"
	- Retuns you to the Start Menu

6. Option Quit:
	- Enter "Q","q","quit","Quit","exit","Exit"
	- Removing Example habits
	- App termination

## Testing 
1. Run the pytest tests inside the /tests directory:
```
pytest
```
Last Testing: 31st of March 2026. 
Results: 24 passed in 0.58s

## Features
- Command-line interface
- Creating and Removing Example habits with random completion dates (for the past 4 weeks)
- Listing tracked habits data
- Adding, Updating, and Deleting habits
- Daily and weekly habits
- Marking habit completed
- Reminder about potential streak loss
- Analyzing habit's current and longest streaks 

## Tech Stack / Built With
Python 3.13.9
SQLite
pytest 8.4.2


## Contributing
Donation Options:
LTC Address: ltc1qurgav8kwdy5mve2fhpd2xz8rx8sascd07ez2ff
XRP Address: rLNmmcNEizWaygypRVTKaWoZG6RrqfsJpi
- Destination Tag: 1132595107


## License
Free for personal use.
