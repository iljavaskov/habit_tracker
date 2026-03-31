import pytest
from datetime import datetime, timedelta
import SQLiteStorage

today = datetime.today().date()
yesterday = today - timedelta(days=1)

class TestSQLiteStorage:

	# Setting up by intializing a database and creating some test habits
	def setup_method(self):
		SQLiteStorage.initialize_db()
		SQLiteStorage.HabitManager.Habit_Manager.habits_list.clear()
		self.new_habit = SQLiteStorage.HabitManager.Habit.Habit("TryHackMe", "Do some tasks and rooms", "daily", today)
		self.first_habit = SQLiteStorage.HabitManager.Habit.Habit("Code", "Do some coding", "daily", yesterday)
		self.second_habit = SQLiteStorage.HabitManager.Habit.Habit("Meditate", "Get under some tree and take a nap", "weekly", yesterday)
		self.third_habit = SQLiteStorage.HabitManager.Habit.Habit("Water plants", "Water your house plants", "weekly", today)
		self.loaded_habit = SQLiteStorage.HabitManager.Habit.Habit("test", "test", "test", yesterday)
		self.updated_new_habit = SQLiteStorage.HabitManager.Habit.Habit("TryHackMe", "Do some tasks and rooms", "daily", today)

	# Testing internal function that takes string type dates and converts them to the datetime data type
	def test_formatting_date(self):
		string_date = str(today)
		formatted_date = SQLiteStorage.formatting_date(string_date)
		assert formatted_date == today

	# Testing the saving habits to the database
	# Note: The habits don't have an habit_id assigned, until they are saved to the database for the first time
	def test_save_new_habit(self):
		assert self.new_habit.habit_id == 0
		assert self.first_habit.habit_id == 0
		SQLiteStorage.save_to_db(self.new_habit)
		SQLiteStorage.save_to_db(self.first_habit)
		assert self.new_habit.habit_id != 0
		assert self.first_habit.habit_id != 0
		assert self.new_habit.habit_id != self.first_habit.habit_id
		

	# Testing the loading of a habit from the database and comparing the attributes
	def test_load_new_habit(self):
		SQLiteStorage.save_to_db(self.new_habit)
		self.loaded_habit = SQLiteStorage.load_habit_from_db(self.new_habit.habit_id)
		assert self.new_habit.habit_id == self.loaded_habit.habit_id
		assert self.new_habit.name == self.loaded_habit.name
		assert self.new_habit.description == self.loaded_habit.description
		assert self.new_habit.periodicity == self.loaded_habit.periodicity
		assert self.new_habit.creation_date == self.loaded_habit.creation_date

	# Testing the updating of a habit in the database and comparing the habit attributes after
	# Note: during updating the habit id remains unchanged
	def test_updating_habit(self):
		SQLiteStorage.save_to_db(self.new_habit)
		self.new_habit.name = self.second_habit.name
		self.new_habit.description = self.second_habit.description
		self.new_habit.periodicity = self.second_habit.periodicity
		self.new_habit.creation_date = self.second_habit.creation_date
		SQLiteStorage.save_to_db(self.new_habit)
		self.updated_new_habit = SQLiteStorage.load_habit_from_db(self.new_habit.habit_id)
		assert self.updated_new_habit.habit_id != 0
		assert self.updated_new_habit.habit_id == self.new_habit.habit_id
		assert self.updated_new_habit.name != "TryHackMe"
		assert self.updated_new_habit.description != "Do some tasks and rooms"
		assert self.updated_new_habit.periodicity != "daily"
		assert self.updated_new_habit.creation_date != today

	# Testing the saving and loading of the completion dates of a habit
	def test_saving_and_loading_completion_dates(self):
		dates = ["2026-03-01","2026-03-07","2026-03-15","2026-03-20","2026-03-25"]
		for date in dates:
			self.third_habit.completion_dates.append(SQLiteStorage.formatting_date(date))
		SQLiteStorage.save_to_db(self.third_habit)
		self.loaded_habit = SQLiteStorage.load_habit_from_db(self.third_habit.habit_id)
		count = 0
		for date in self.loaded_habit.completion_dates:
			assert date == SQLiteStorage.formatting_date(dates[count])
			count +=1
		
		assert count == 5

	# Testing if the coompletion dates are updated inside the database
	def test_saving_new_completion_date(self):
		dates = ["2026-03-01","2026-03-07","2026-03-15","2026-03-20","2026-03-25"]
		for date in dates:
			self.third_habit.completion_dates.append(SQLiteStorage.formatting_date(date))
		SQLiteStorage.save_to_db(self.third_habit)
		self.loaded_habit = SQLiteStorage.load_habit_from_db(self.third_habit.habit_id)
		last_date = self.loaded_habit.completion_dates[len(self.loaded_habit.completion_dates)-1]
		assert last_date == SQLiteStorage.formatting_date("2026-03-25")

		# Adding the today's date to the completion list and saving it
		self.third_habit.completion_dates.append(today)
		SQLiteStorage.save_to_db(self.third_habit)
		self.loaded_habit = SQLiteStorage.load_habit_from_db(self.third_habit.habit_id)
		last_date = self.loaded_habit.completion_dates[len(self.loaded_habit.completion_dates)-1]
		assert last_date == today


	# Testing the deletion of a habit from the database
	def test_delete_habit_from_db(self):
		SQLiteStorage.save_to_db(self.new_habit)
		SQLiteStorage.delete_habit_from_db(self.new_habit.habit_id)
		self.loaded_habit = SQLiteStorage.load_habit_from_db(self.new_habit.habit_id)
		assert self.loaded_habit != 0

	# Testing the function that all habits from the database are loaded (into the operational habits_list)
	def test_load_all_habits(self):
		SQLiteStorage.save_to_db(self.new_habit)
		SQLiteStorage.save_to_db(self.first_habit)
		SQLiteStorage.save_to_db(self.second_habit)
		SQLiteStorage.save_to_db(self.third_habit)
		SQLiteStorage.load_all_habits_from_db()
		assert SQLiteStorage.HabitManager.Habit_Manager.habits_list[0].name == "TryHackMe"
		assert SQLiteStorage.HabitManager.Habit_Manager.habits_list[1].name == "Code"
		assert SQLiteStorage.HabitManager.Habit_Manager.habits_list[2].name == "Meditate"
		assert SQLiteStorage.HabitManager.Habit_Manager.habits_list[3].name == "Water plants"

		for habit in SQLiteStorage.HabitManager.Habit_Manager.habits_list:
			assert habit.habit_id != 0
		assert len(SQLiteStorage.HabitManager.Habit_Manager.habits_list) == 4

	# Removing the file-based database, any created objects and clearing the habits_list
	def teardown_method(self):
		import os
		os.remove("stored_habits.db")
		del self.new_habit
		del self.first_habit
		del self.second_habit
		del self.third_habit
		del self.loaded_habit
		del self.updated_new_habit
		SQLiteStorage.HabitManager.Habit_Manager.habits_list.clear()
pytest.main()