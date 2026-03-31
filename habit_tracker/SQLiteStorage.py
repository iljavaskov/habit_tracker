# Importing "sqlite3" library, "datetime" library, and the "HabitManager.py" file
import sqlite3
import datetime
import HabitManager

def formatting_date(input_date):
    """This funtion formats the string type dates to the datetime type format"""
    def deconstructing_date(input_date):
        global year, month, day
        year = int(input_date.split("-")[0])
        month = int(input_date.split("-")[1])
        day = int(input_date.split("-")[2])
        
    deconstructing_date(input_date)
    date = (year, month, day)
    formatted_date = datetime.datetime(*date).date()
    return formatted_date

def initialize_db():
    """This function creates a database and two tables in it, if not created yet"""
    conn = sqlite3.connect("stored_habits.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            periodicity TEXT NOT NULL, 
            creation_date TEXT NOT NULL
        ) 
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completion_dates TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        ) 
    ''')
    conn.commit()
    conn.close()

def save_to_db(habit):
    """This function saves the habit (new or updated) and its' completion dates (incl. marked completed) to the database"""
    conn = sqlite3.connect("stored_habits.db")
    cursor = conn.cursor()
    if habit.habit_id:
        # Update existing habit data
        cursor.execute('''
            UPDATE habits SET name= ?, description = ?, periodicity = ?, creation_date = ? WHERE id = ?
        ''',(habit.name, habit.description, habit.periodicity, habit.creation_date.isoformat(), habit.habit_id,))
    else:
        # Insert new habit data, that's also the moment when the habit gets it's habit_id assigned for the first time.
        cursor.execute('''
            INSERT INTO habits (name, description, periodicity, creation_date) VALUES (?, ?, ?, ?)
        ''', (habit.name, habit.description, habit.periodicity, habit.creation_date.isoformat()))
        habit.habit_id = cursor.lastrowid

    
    if not habit.completion_dates:
        # Delete the habit completions dates from the database if the object was modified and the completion dates cleared
        cursor.execute('''
        UPDATE tracking SET completion_dates = NULL WHERE habit_id = ?
        ''', (habit.habit_id,))
        
    else:
        # Get existing completions for this habit
        cursor.execute('''
            SELECT completion_dates FROM tracking WHERE habit_id = ?
        ''', (habit.habit_id,))
        existing_dates = {row[0] for row in cursor.fetchall()}
    
        # Insert new completions that don't already exist in the database
        for date in [date.isoformat() for date in habit.completion_dates if date.isoformat() not in existing_dates]:
            cursor.execute('''
                INSERT INTO tracking (habit_id, completion_dates) VALUES (?, ?)
            ''', (habit.habit_id, date))
    conn.commit()
    conn.close()

def delete_habit_from_db(habit_id):
    """Deletes the habit by ID with all the completion dates from the database"""
    conn = sqlite3.connect("stored_habits.db")
    cursor = conn.cursor()
    
    # Deletes the habit data
    cursor.execute('''
        DELETE FROM habits WHERE id = ?
    ''', (habit_id,))

    # Deletes the habit completions dates
    cursor.execute('''
        DELETE FROM tracking WHERE habit_id = ?
    ''', (habit_id,))

    conn.commit()
    conn.close()

def load_habit_from_db(habit_id):
    """Retrieve a habit by ID with the completion dates from the database"""
    conn = sqlite3.connect("stored_habits.db")
    cursor = conn.cursor()

    # Fetch habit data
    cursor.execute('''
        SELECT id, name, description, periodicity, creation_date FROM habits WHERE id = ?
    ''', (habit_id,))
    result = cursor.fetchone()
    
    if not result:
        return None
        
    # Creates the habit object
    habit = HabitManager.Habit.Habit(name=result[1], description=result[2], periodicity=result[3], creation_date=formatting_date(result[4]))
    habit.habit_id = habit_id 

    #Fetch completions dates of the habit
    cursor.execute('''
    SELECT completion_dates FROM tracking WHERE habit_id = ?
    ''', (habit_id,))

    habit.completion_dates = [datetime.datetime.fromisoformat(row[0]).date() for row in cursor.fetchall()]  

    conn.close()
    return habit

def load_all_habits_from_db():
    """Retrieves all stored objects (habits) from the database and stores them in the operational habits_list of the Habit_Manager class"""
    conn = sqlite3.connect("stored_habits.db")
    cursor = conn.cursor()
    
    cursor.execute(''' SELECT COUNT(id) FROM habits''')
    number_of_entries = cursor.fetchone()[0]

    habit_id = 1
    while number_of_entries > 0:
        loading_habit = load_habit_from_db(habit_id)
        if loading_habit is not None:
            HabitManager.Habit_Manager.habits_list.append(loading_habit)
            number_of_entries -= 1
            habit_id += 1
        else: 
            habit_id += 1 
    
    conn.close()