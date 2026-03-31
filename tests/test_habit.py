import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
from Habit import Habit

# This part was added for the test units to work..
@freeze_time("2026-03-28")
def current_date():
    """This function returns the current date in the datetime type format"""
    today = datetime.today().date()
    return today

today = current_date()
yesterday = today - timedelta(days=1)

class TestHabit:
	# Setting up a test habit
	def setup_method(self):
		self.habit = Habit("TryHackMe", "Do some tasks and rooms", "daily", today)

	# Checking the mark_completed method
	def test_mark_completed(self):
		self.habit.mark_completed()
		assert self.habit.completion_dates[0] == today

	# Checking that mark completed works only once a day per habit (no duplicate dates)
	def test_no_double_mark_completed(self):
		self.habit.completion_dates.append(today)
		self.habit.mark_completed()
		assert len(self.habit.completion_dates) == 1

	# Checking the method that returns a list with all the dates
	# The duplicate dates will be "filtered out" due to sorted(set()) inside the get completion history method
	def test_get_completion_history(self):
		self.habit.completion_dates.append(today)
		self.habit.completion_dates.append(yesterday)
		self.habit.completion_dates.append(today) 
		completion_dates_list = self.habit.get_completion_history()
		assert len(completion_dates_list) == 2

	# Deleting habit after test
	def teardown_method(self):
		del self.habit

pytest.main()