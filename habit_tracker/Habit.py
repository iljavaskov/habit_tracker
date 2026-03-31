# Importing the "datetime" library
import datetime

class Habit:
    """
    Represents a habit
    Attributes: habit_id (int), name (string), description (string), periodicity (string), creation_date(datetime), completion_dates (list with datetime values)
    """
    
    def __init__(self, name, description, periodicity, creation_date):
        """
        Initializes a new instance of the habit class
        Args: 
            name (string): Name of the habit.
            description (string): Short detailed description about the task. Must not contain the word \'Example\'
            periodicity (string): Periodicity of the task. Must be either daily or weekly.
            creation_date(datetime): Date of the habit creation. Must be datetime type format.
        """
        self.habit_id = int()
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completion_dates = []
        
    def mark_completed(self):
        """This method that marks a habit completed by adding the current date into the completion dates list of the relevant habit"""
        today = datetime.datetime.today().date()
        # Checks if the current date is already in the completion dates list of the relevant habit
        if today not in self.completion_dates:
            self.completion_dates.append(today)
            print(f"\nYou checked of the habit {self.name} with the current date {today}!")
        else:
            print("\nWoops, you already did this task today! No double checks allowed!")
    
    def get_completion_history(self): 
        """This method returns a list with all the completion dates of the relevant habit"""
        completion_dates = []
        completion_dates = [str(date) for date in sorted(set(self.completion_dates))]
        return completion_dates

    def display_habit(self): 
        """This method that displays the habit data of the relevant habit"""
        print("\n\nName:", self.name,"| Description:", self.description,"| Periodicity:", self.periodicity,"| Creation date:", self.creation_date)
        print("\nCompletion Dates:",self.get_completion_history())