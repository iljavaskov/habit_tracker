#Importing the "Habit.py", "SQLiteStorage.py", "Generator.py", and "Analytics_module.py" files
import Habit
import SQLiteStorage
import Generator
import Analytics_module

class Habit_Manager:
    """
    Represents the Habit Manager
    Attributes: habits_list (list) for the habit objects. An operational storage.
    """ 
    habits_list = []
    
    @staticmethod
    def add_habit():
        """
        This static method creates a new habit object, and saves it to the database and the habits_list
        It requests the user to give it a name, description, and periodicity.
        """
        reply_name = input("\nEnter the name for your habit:")
        print("Note: If you add the keyword \'Example\', it will be deleted automatically once you quit the app.")
        reply_description = input("Enter a short description for your habit:")
        reply_periodicity = input("Choose a periodicity for your habit.\nEnter daily or weekly:")
        if reply_periodicity in ["daily", "weekly"]:
            new_habit = Habit.Habit(reply_name,reply_description,reply_periodicity,Analytics_module.today)
            # Stores the new habit to the database
            SQLiteStorage.save_to_db(new_habit)
            # Stores new habit in the habit dictionary
            Habit_Manager.habits_list.append(new_habit)
            print(f"\nDone! You successfully added a new habit task called - {reply_name}!")
        else:
            print("You choose an incorrect input. Try again!")  

    @staticmethod
    def delete_habit():
        """
        This static method deletes a habit object from the database and the habits_list. 
        It requires a user to give the name of the relevant habit object. 
        If there are habit_objects with the same name, the first one inside the database and habits_list will be deleted.
        """
        print("Note: If there are multiple habits with the exact same name, the first one will be deleted from the list.")
        print("To avoid the wrong the deletion, it is recommended to change some names before that.")
        reply_name = input("\nEnter the name of the habit you want to delete:")

        # Checks for a match between the user input and the habit objects names.
        match = next((habit for habit in Habit_Manager.habits_list if habit.name == reply_name), None)
        if match:
            try: 
                SQLiteStorage.delete_habit_from_db(match.habit_id)
                Habit_Manager.habits_list.remove(match)
                print(f"The habit {match.name} and its completion dates were successfully deleted from the database and the temporary storage list!")
            except: 
                print("The habit couldn't be deleted or found. Try again!")

        else: 
            print(f"There is no habit with such a name {reply_name}. Try again!")


    # Updates data of a habit object and saves it to the db
    @staticmethod
    def update_habit():
        """
        This static method updates a habit object in the database and the habits_list. 
        It requires a user to decide whether to:
            - change the name, description, periodicity,
            - update the creation date to today,
            - clear the previous completion dates.
        If there user adds the keyword \'Example\' to the habit description it will be deleted from the database automatically later.
        """
        reply_name = input("\nEnter the name of the habit you want to update:")

        # Checks if there is such a habit in the list
        match = next((habit for habit in Habit_Manager.habits_list if habit.name == reply_name), None)
        if match:
            # Deletes the object from the habit temporary list and stores tha habit object temporary as updating_habit
            match.display_habit()
            updating_habit = match
            Habit_Manager.habits_list.remove(match)

            #Questionnaire what to change/update in the habit object
            while True:
                reply = input("\nDo you want to change the name of this habit?\nEnter Y for Yes, or N for No:")
                if reply in ["Y","y"]:
                    new_name = input("Enter the new name:")
                    updating_habit.name = new_name
                    break
                elif reply in ["N","n"]:
                    break
                else:
                    print("You entered an incorrect input. Try again!")
                
            while True:        
                reply = input("\nDo you want to change the description of this habit?\nEnter Y for Yes, or N for No:")
                if reply in ["Y","y"]:
                    print("Note: If you add the keyword \'Example\', it will be deleted automatically once you quit the app.")
                    new_description = input("Enter the new description:")
                    updating_habit.description = new_description
                    break
                elif reply in ["N","n"]:
                    break
                else:
                    print("You entered an incorrect input. Try again!")
                
            while True:
                reply = input("\nDo you want to change the periodicity of this habit?\nEnter Y for Yes, or N for No:")
                if reply in ["Y","y"]:
                    while True:
                        new_periodicity = input("Choose a periodicity for your habit.\n Enter daily or weekly:")
                        if new_periodicity in ["daily","weekly"]:
                            updating_habit.periodicity = new_periodicity
                            break
                        else:
                            print("You choose an incorrect input. Try again!")
                    break
                elif reply in ["N","n"]:
                    break
                else:
                    print("You entered an incorrect input. Try again!")
                
            while True:
                reply = input("\nDo you want to update the creation date of this habit?\nEnter Y for Yes, or N for No:")
                if reply in ["Y","y"]:
                    updating_habit.creation_date = Analytics_module.today
                    break
                elif reply in ["N","n"]:
                    break
                else:
                    print("You entered an incorrect input. Try again!")
                
            while True:        
                reply = input("\nDo you want to clear the dates of completion of this habit?\nEnter Y for Yes, or N for No:")
                if reply in ["Y","y"]:
                    updating_habit.completion_dates.clear()
                    break
                elif reply in ["N","n"]:
                    break
                else:
                    print("You entered an incorrect input. Try again!")
    
            # Saves new habit data into the database  
            SQLiteStorage.save_to_db(updating_habit)
    
            # Stores new habit in the habit dictionary
            Habit_Manager.habits_list.append(updating_habit)
            print("Your habit was successfully updated!")

        else: 
            print(f"There is no habit with the name {reply_name}. Maybe you mistyped something. Pay attention to capital letters. Try again!")


    @staticmethod
    def reminder():
        """
        This static method checks if the habits were marked completed today. 
        It reminds the user about the habits that need to be checked off today in order to keep the streak or starting a streak
        """
        while True:
            match = next((habit for habit in Habit_Manager.habits_list if Analytics_module.today not in habit.completion_dates), None)
            if match == None:
                print("All habit tasks checked off today!")
                break
            else:
                for habit in Habit_Manager.habits_list:
                    if not habit.completion_dates:
                        print(f"You haven't completed the habit task {habit.name} yet.")
                    elif Analytics_module.today not in habit.completion_dates:
                        if habit.periodicity == "daily":
                            last_completion_date = sorted(habit.completion_dates)[len(habit.completion_dates) - 1]
                            if Analytics_module.today - last_completion_date == Analytics_module.datetime.timedelta(days=1):
                                print(f"You need to do your daily habit task {habit.name} today, otherwise you will lose your current streak!")
                            elif Analytics_module.today - last_completion_date > Analytics_module.datetime.timedelta(days=1):
                                print(f"You haven't completed your daily habit task {habit.name} for some days..")
        
                        elif habit.periodicity == "weekly":
                            last_completion_date = sorted(habit.completion_dates)[len(habit.completion_dates) - 1]
                            next_deadline = sorted(habit.completion_dates)[0] + Analytics_module.datetime.timedelta(days=7)
                            for i in range(1, len(habit.completion_dates)):
                                previous_deadline = next_deadline - Analytics_module.datetime.timedelta(days=7)
                                if previous_deadline < sorted(habit.completion_dates)[i] <= next_deadline:
                                    # Setting new date for the next deadline for the check off
                                    next_deadline += Analytics_module.datetime.timedelta(days=7)
                                elif previous_deadline >= sorted(habit.completion_dates)[i]:
                                    continue
                                elif next_deadline < sorted(habit.completion_dates)[i]:
                                    # Setting new date for the start week
                                    previous_deadline = sorted(habit.completion_dates)[i]
                                    # Setting new next deadline for the check off
                                    next_deadline = previous_deadline + Analytics_module.datetime.timedelta(days=7)
                            if Analytics_module.today == next_deadline:
                                print(f"You need to do the weekly habit task {habit.name} today, otherwise you might lose your current streak!")
                            elif Analytics_module.today > next_deadline:
                                print(f"You haven't completed your weekly habit task {habit.name} for a while..")
                            else:
                                continue
                    else: 
                        continue
                # Stop after gone through the habit list
                break
                