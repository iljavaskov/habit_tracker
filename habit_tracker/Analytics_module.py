# Importing the datetime library, and the "HabitManager.py" file
import datetime
import HabitManager

today = datetime.datetime.today().date()
yesterday = today - datetime.timedelta(days=1)
last_week = [today - datetime.timedelta(days=i) for i in range(0,7)]

def calculate_streak(habit): 
    """This function that calculates the longest streak (high score) and current streak of the relevant habit"""
    #global longest_streak
    #global current_streak
    
    longest_streak = 1
    current_streak = 1

    # Sorting the dates in the completion dates list
    sorted_dates = sorted(habit.completion_dates)

    def calculate_daily():
        """This nested function calculates the longest streak (high score) and current streak for daily habits"""
        nonlocal longest_streak
        nonlocal current_streak
        nonlocal sorted_dates
            
        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] - sorted_dates[i - 1] == datetime.timedelta(days=1):
                current_streak += 1
                # Saving the current streak as the longest streak if there is a new highscore
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
                     
    def calculate_weekly():
        """This nested function calculates the longest streak (high score) and current streak for weekly habits"""
        nonlocal longest_streak
        nonlocal current_streak
        nonlocal sorted_dates

        # Setting the next deadline for the check off
        next_deadline = sorted_dates[0] + datetime.timedelta(days=7)
        for i in range(1, len(sorted_dates)):
            # Setting new date for the start week
            previous_deadline = next_deadline - datetime.timedelta(days=7)
                 
            if previous_deadline < sorted_dates[i] <= next_deadline:
                current_streak += 1
                # Saving the current streak as the longest streak if there is a new highscore
                longest_streak = max(longest_streak, current_streak)
                # Setting new date for the next deadline for the check off
                next_deadline += datetime.timedelta(days=7)
    
            elif previous_deadline >= sorted_dates[i]:
                continue
                        
            elif next_deadline < sorted_dates[i]:
                current_streak = 1
                # Setting new date for the start week
                previous_deadline = sorted_dates[i]
                # Setting new date for the next deadline for the check off
                next_deadline = previous_deadline + datetime.timedelta(days=7)
        
    # If there are dates in the completion dates the streak is set to 0
    if not sorted_dates:
        current_streak = 0
        longest_streak = 0
        return current_streak, longest_streak

    # Calculating the streaks by counting the consecutive dates for daily habits
    if habit.periodicity == "daily":
            
        # Calculates just the longest streak and sets the current_streak to 0, if the last date is not today or yesterday.
        if sorted_dates[len(sorted_dates) - 1] not in [today, yesterday]:
            calculate_daily()
            current_streak = 0
                
        # Calculates the current and longest streak
        else:
            calculate_daily()
                
        return current_streak, longest_streak

    # Calculating the streaks for weekly habits            
    elif habit.periodicity == "weekly":
            
        # Calculates just the longest streak and sets the current_streak to 0, if the last date is not within the last week.
        if sorted_dates[len(sorted_dates) - 1] not in last_week:
            calculate_weekly()
            current_streak = 0
            
        # Calculates the current and longest streak
        else:
            calculate_weekly()
            
        return current_streak, longest_streak

def list_habits():
    """This function list all the habits stored inside the operational storage habits_list"""
    if len(HabitManager.Habit_Manager.habits_list) >= 1:
        print("\nHere are all your tracked habits:")
        for habit in HabitManager.Habit_Manager.habits_list:
            habit.display_habit()
        print("\nDone! All habits (from the temporary/operational list) listed!")
    else: 
        print("\nOops! There are no habits in the operational list. Generate the example habits or create your first habit tasks!")

def list_habits_by_periodicity():
    """This function list all the habits of a specified periodicity stored inside the operational storage habits_list"""
    reply = input("\nWhat kind of habits do you want to list?\nEnter daily, or weekly:")
    if reply in ["daily","weekly"]:
        for habit in HabitManager.Habit_Manager.habits_list:
            if habit.periodicity == reply:
                habit.display_habit()
            else: 
                continue
        print(f"Done! All habits (from the temporary/operational list) with the {reply} periodicity are listed!")
    else:            
        print("You choose an incorrect input. Try again later!")

def longest_streak():
    """This function checks for the longest current streak of all the tracked habits stored inside the operational storage habits_list"""
    habit_streaks = ()
    habit_name = ""
    habit_streak = 0
    for habit in HabitManager.Habit_Manager.habits_list:
        habit_streaks = calculate_streak(habit) 
        current_streak = int(habit_streaks[0])
        longest_streak = int(habit_streaks[1])
        if current_streak > habit_streak:
            habit_name = habit.name
            habit_streak = current_streak
        else: 
            continue
    print(f"Your best habit is {habit_name} with the longest current streak of {habit_streak}!")

def longest_streak_of_a_habit(habit):
    """This function checks for the current streak and longest streak of a specified habit"""
    habit_streaks = ()
    habit_streaks = calculate_streak(habit) 
    current_streak = int(habit_streaks[0])
    longest_streak = int(habit_streaks[1])
    if current_streak == longest_streak:
        print(f"Your habit {habit.name} has the current longest streak of {current_streak}!")
    else: 
        print(f"Your habit {habit.name} has the current streak of {current_streak} and the longest streak was {longest_streak} so far! Go break a new high score!")