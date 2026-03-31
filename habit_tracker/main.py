# Importing the "HabitManager.py" file
import HabitManager

# Defining necessary variables
reply = "0"
status_CLI = 1

def start_menu():
    """The starting menu also known as status_CLI 1"""
    global reply
    print("\n\n|---------------------------------------------------|")
    print("|Choose an option from the start menu:              |") 
    print("|[1] Enter 1 to List all habits                     |")
    print("|[2] Enter 2 to Add, Manage, and Delete habits      |") 
    print("|[3] Enter 3 to Mark a habit Completed              |") 
    print("|[4] Enter 4 to Analyse your habits                 |")
    print("|[5] Enter 5 to Generate and Load Example Habits    |")
    print("|[6] Enter 6 to Remove the Example Habits           |")
    print("|[Q] Enter Q to Quit the Habit Tracker Application  |")
    print("|---------------------------------------------------|")
    reply = input("\n\nEnter an option:")

def habit_manager_menu():
    """The habit manager menu also known as status_CLI 2"""
    global reply
    print("\n\n|---------------------------------------------------|")
    print("|Choose an option from the habit manager menu:      |")
    print("|[1] Enter 1 to List all habits                     |") 
    print("|[2] Enter 2 to Add a new habit                     |") 
    print("|[3] Enter 3 to Delete an existing habit            |") 
    print("|[4] Enter 4 to Change existing habits              |") 
    print("|[B] Enter B to Go Back to the Start Menu           |")
    print("|[Q] Enter Q to Quit Habit Tracker Application      |")
    print("|---------------------------------------------------|")
    reply = input("\n\nEnter an option:")

def analytics_menu(): 
    """The analytics menu also known as status_CLI 3"""
    global reply
    print("\n\n|----------------------------------------------------------------|")
    print("|Choose an option from the analytics functions:                  |") 
    print("|[1] Enter 1 to List all habits                                  |") 
    print("|[2] Enter 2 to List all habits by periodicity                   |") 
    print("|[3] Enter 3 to Return the longest run streak of all habits      |")  
    print("|[4] Enter 4 to Return the longest run streak for a given habit  |")  
    print("|[B] Enter B to Go Back to the Start Menu                        |")
    print("|[Q] Enter Q to Quit Habit Tracker Application                   |")
    print("|----------------------------------------------------------------|")
    reply = input("\n\nEnter an option:")

welcome = "\n\nWelcome to your Habit Tracker Application!"
print(welcome)

# Initializing the database
HabitManager.SQLiteStorage.initialize_db()
print("Database intialized")

# Downloading habits from the database to the temporary operational storage habits list
HabitManager.SQLiteStorage.load_all_habits_from_db()
print("Habits downloaded from the database to the operational habits list (or not if the database was empty)")

#CLI Menu
while __name__ == "__main__": 
    
    if status_CLI == 0:
        print("\nClearing some data..")
        # Removes the example habits with their data from the operational storage and database before closure
        HabitManager.Generator.remove_example_habits()
        HabitManager.Habit_Manager.habits_list.clear()
        print("\nRemember to come back! See you soon!")
        break
        
    elif status_CLI == 1:
        
        while True:
            start_menu()
            if reply == "1":
                # Lists all habits
                HabitManager.Analytics_module.list_habits()
                
            elif reply == "2":
                # Moving to the HabitManager menu
                status_CLI = 2
                break
                
            elif reply == "3":
                
                #Checks for habits that need to be marked completed today, and tells the user that otherwise the streak will be lost.
                HabitManager.Habit_Manager.reminder()
                
                reply_habit_name = input("\nEnter the name of a habit to check off:")
                
                # Check if there is such an object with such a name 
                match = next((habit for habit in HabitManager.Habit_Manager.habits_list if habit.name == reply_habit_name), None)
                if match:
                    checking_off_habit = match
                    checking_off_habit.mark_completed()
                    HabitManager.SQLiteStorage.save_to_db(checking_off_habit)
                else: 
                    print(f"\nNo habit with such a name {reply_habit_name} was found. Try again!")
                
            elif reply == "4":
                # Moving to the Analytics menu
                status_CLI = 3
                break
                
            elif reply == "5":
                
                # Checks for the keyword "Example" in the habit description
                match = next((habit for habit in HabitManager.Habit_Manager.habits_list if "Example" in habit.description.split(" ")), None)
                if match == None:
                    # Creates 5 pre-defined habits with relatively random dates data and stores them into the operational storage
                    HabitManager.Generator.example_habit_data_generator()
                else:
                    print("You already generated some example habit data.")
                    print("Or some of your habits with the keyword \'Example\' in the description conflict with the data generator code.")
                
            elif reply == "6":
                # Removes the 5 example habits with their data from the operational storage and database 
                HabitManager.Generator.remove_example_habits()
                      
            elif reply in ["Q","q","quit","Quit","exit","Exit"]:
                status_CLI = 0
                break
                
            else:
                print("\n\nYou typed a non-existing option.")
                print(f"Why would you even try {reply}?! Try again!")

    elif status_CLI == 2:
        
        while True:
            habit_manager_menu()
            if reply == "1":
                # List all the habits (from the temporary list)
                HabitManager.Analytics_module.list_habits()
                
            elif reply == "2":
                # Habit Tracker class "add method"
                HabitManager.Habit_Manager.add_habit()
                
            elif reply == "3":
                # Habit Tracker class "delete method"
                HabitManager.Habit_Manager.delete_habit()
                
            elif reply == "4":
                # Habit Tracker class "update method"
                HabitManager.Habit_Manager.update_habit()
                      
            elif reply in ["B", "b","Back","back","cancel","Cancel"]:
                # Switching back to the start menu
                print("\n\nGoing back to the start menu..")
                status_CLI = 1
                break
                
            elif reply in ["Q","q","quit","Quit","exit","Exit"]:
                status_CLI = 0
                break
                
            else:
                print("\n\nYou typed a non-existing option.")
                print(f"Why would you even try {reply}?! Try again!")

    elif status_CLI == 3:
        
        while True:
            analytics_menu()
            if reply == "1":
                # List all the habits (from the temporary list)
                HabitManager.Analytics_module.list_habits()
                
            elif reply == "2":
                # List all habits depending on the choosen periodicity
                HabitManager.Analytics_module.list_habits_by_periodicity()
                
            elif reply == "3":
                # Gives the habit with the longest streak between all the current streaks of all habits
                HabitManager.Analytics_module.longest_streak()
                
            elif reply == "4":
                # Gives longest run streak of a requested habit
                reply_name = input("\n\nEnter the name of the habit you want to see the longest run streak:")
                match = next((habit for habit in HabitManager.Habit_Manager.habits_list if habit.name == reply_name), None)
                if match:
                    HabitManager.Analytics_module.longest_streak_of_a_habit(match)
                else: 
                    print(f"There is no habit with the name {reply_name}. Maybe you mistyped something. Pay attention to capital letters. Try again!")
                      
            elif reply in ["B", "b","Back","back","cancel","Cancel"]:
                # Switching back to the start menu
                print("\n\nGoing back to the start menu..")
                status_CLI = 1
                break
                
            elif reply in ["Q","q","quit","Quit","exit","Exit"]:
                status_CLI = 0
                break
                
            else:
                print("\n\nYou typed a non-existing option.")
                print(f"Why would you even try {reply}?! Try again!")