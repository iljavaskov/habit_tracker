#Importing "HabitManger.py" file and the "random" library 
import random
import datetime
import HabitManager


# Defining some reusable variables
today = datetime.datetime.today().date()
today_four_weeks_ago = today - datetime.timedelta(days=28)

def random_past_dates(number_of_dates):
    """
    This function returns a list with random dates within the last 4 weeks depending on the number of dates specified
    This list might also include duplicate dates, unfortunately, which need later to be filtered out
    """
    return [today_four_weeks_ago + datetime.timedelta(days=random.randint(0,27)) for i in range(number_of_dates)]

# Creates 5 pre-defined habits with relatively random dates data, and saves it to the temporary list (operational storage)
def example_habit_data_generator():
    """
    This function creates 5 pre-defined habits and relatively randomly created completion dates
    It saves the habits into the operational habits_list of the Habit_Manager class.
    It is recommended to use a big integer number as parameter for the random_past_dates in order to get enough unique dates. 
    """
    
    example_habit_1 = HabitManager.Habit.Habit(name="Study",description="Example Habit: Study something for at least 2 hours",periodicity="daily",creation_date=today_four_weeks_ago)
    example_habit_1.completion_dates = sorted(set(random_past_dates(50)))
    HabitManager.Habit_Manager.habits_list.append(example_habit_1)
    
    example_habit_2 = HabitManager.Habit.Habit(name="Workout",description="Example Habit: Do some exercises from your exercise week plan",periodicity="daily",creation_date=today_four_weeks_ago)
    example_habit_2.completion_dates = sorted(set(random_past_dates(10)))
    HabitManager.Habit_Manager.habits_list.append(example_habit_2)
    
    example_habit_3 = HabitManager.Habit.Habit(name="Walk",description="Example Habit: Walk about 10k steps",periodicity="daily",creation_date=today_four_weeks_ago)
    example_habit_3.completion_dates = sorted(set(random_past_dates(17)))
    HabitManager.Habit_Manager.habits_list.append(example_habit_3)
    
    example_habit_4 = HabitManager.Habit.Habit(name="Digital Detox",description="Example Habit: Watch some birds or dogs in the park for a couple of hours",periodicity="weekly",creation_date=today_four_weeks_ago)
    example_habit_4.completion_dates = sorted(set(random_past_dates(5)))
    HabitManager.Habit_Manager.habits_list.append(example_habit_4)
    
    example_habit_5 = HabitManager.Habit.Habit(name="Read",description="Example Habit: Read something unrelated to your studies",periodicity="weekly",creation_date=today_four_weeks_ago)
    example_habit_5.completion_dates = sorted(set(random_past_dates(5)))
    HabitManager.Habit_Manager.habits_list.append(example_habit_5)
    
    print("\nExample habit data generated successfully!")
    
def remove_example_habits():
    """
    The deletion of the example habits from the operational habits_list of the Habit_Manager class and from the stored_habits.db database
    It checks if the habit_list contains habits wiht the keyword "Example" in their discription, which will be deleted. 
    If a user uses the word "Example" in their habit description, this function will also delete it when the user closes/quits the app.
    """

    # A loop inorder to the delete all the Example habits
    while True:
        
        # Checks for the keyword "Example" in the habit description, otherwise returns None
        match = next((habit for habit in HabitManager.Habit_Manager.habits_list if "Example" in habit.description.split(" ")), None)
        if match != None:
            try:
                # if the habits had an habit_id assgined, it will also be deleted from the database.
                if match.habit_id:
                    HabitManager.Habit_Manager.habits_list.remove(match)
                    HabitManager.SQLiteStorage.delete_habit_from_db(match.habit_id)
                    print(f"The Example habit {match.name} was deleted everywhere.")
                else:
                    HabitManager.Habit_Manager.habits_list.remove(match)
                    print(f"The Example habit {match.name} was deleted from the operational storage.")
            except:
                print(f"The Example habit {match.name} couldn't be deleted..")
        else:
            break
            
    print("All example habit data should have been deleted from the storages and databases")