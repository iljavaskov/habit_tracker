import pytest
import HabitManager

class Test_HabitManager:

	# Setting up with intitializing the database, clearing and objects in the habits_list, and creating 5 pre-defined habit objects for tests
	def setup_method(self):
		HabitManager.SQLiteStorage.initialize_db()
		HabitManager.Habit_Manager.habits_list.clear()

		self.first_daily_habit = HabitManager.Habit.Habit(name="TryHackMe", description="Do some tasks and rooms", periodicity="daily", creation_date=HabitManager.SQLiteStorage.formatting_date("2026-03-01"))
		# Test scenario with current_streak 13 and longest_streak 14
		first_daily_habit_dates = ["2026-03-01","2026-03-02","2026-03-03","2026-03-04","2026-03-05","2026-03-06","2026-03-07","2026-03-08","2026-03-09","2026-03-10","2026-03-11","2026-03-12","2026-03-13","2026-03-14","2026-03-16","2026-03-17","2026-03-18","2026-03-19","2026-03-20","2026-03-21","2026-03-22","2026-03-23","2026-03-24","2026-03-25","2026-03-26","2026-03-27","2026-03-28"]
		for date in first_daily_habit_dates:
			self.first_daily_habit.completion_dates.append(HabitManager.SQLiteStorage.formatting_date(date))

		self.second_daily_habit = HabitManager.Habit.Habit(name="Workout",description="Do some exercises from your exercise week plan",periodicity="daily",creation_date=HabitManager.SQLiteStorage.formatting_date("2026-03-01"))
		# Test scenario with current_streak and longest_streak 9
		second_daily_habit_dates = ["2026-03-02","2026-03-03","2026-03-04","2026-03-07","2026-03-08","2026-03-10","2026-03-11","2026-03-13","2026-03-19","2026-03-20","2026-03-21","2026-03-22","2026-03-23","2026-03-24","2026-03-25","2026-03-26","2026-03-27"]
		for date in second_daily_habit_dates:
			self.second_daily_habit.completion_dates.append(HabitManager.SQLiteStorage.formatting_date(date))

		self.third_daily_habit = HabitManager.Habit.Habit(name="Walk",description="Walk about 10k steps",periodicity="daily",creation_date=HabitManager.SQLiteStorage.formatting_date("2026-03-01"))
		# Test scenario with current_streak 0 and longest_streak 4
		third_daily_habit_dates = ["2026-03-04","2026-03-07","2026-03-08","2026-03-10","2026-03-11","2026-03-13","2026-03-19","2026-03-20","2026-03-21","2026-03-23","2026-03-24","2026-03-25","2026-03-26"]
		for date in third_daily_habit_dates:
			self.third_daily_habit.completion_dates.append(HabitManager.SQLiteStorage.formatting_date(date))

		self.first_weekly_habit = HabitManager.Habit.Habit(name="Water plants", description="Water the house plants", periodicity="weekly", creation_date=HabitManager.SQLiteStorage.formatting_date("2026-03-01"))
		# Test scenario with current_streak 1 and longest_streak 3
		first_weekly_habit_dates = ["2026-03-01","2026-03-03","2026-03-14","2026-03-27"]
		for date in first_weekly_habit_dates:
			self.first_weekly_habit.completion_dates.append(HabitManager.SQLiteStorage.formatting_date(date))

		self.second_weekly_habit = HabitManager.Habit.Habit(name="Digital Detox",description="Watch some birds or dogs in the park for a couple of hours",periodicity="weekly",creation_date=HabitManager.SQLiteStorage.formatting_date("2026-03-01"))
		# Test scenario with current_streak 0 and longest_streak 3
		second_weekly_habit_dates = ["2026-03-01","2026-03-02","2026-03-09"]
		for date in second_weekly_habit_dates:
			self.second_weekly_habit.completion_dates.append(HabitManager.SQLiteStorage.formatting_date(date))

	# Testing add_habit static method 
	def test_add_habit(self, capsys, monkeypatch):
		# Testing loading from db -> should return None, because it is was not saved to the db yet, and therefore no habit_id assigned
		assert self.first_daily_habit.habit_id == 0
		load_habit = HabitManager.SQLiteStorage.load_habit_from_db(self.first_daily_habit.habit_id)
		assert load_habit is None

		# Inputing the attributes of the first daily habit
		first_habit_inputs = iter([self.first_daily_habit.name, self.first_daily_habit.description, self.first_daily_habit.periodicity])
		monkeypatch.setattr("builtins.input", lambda prompt="": next(first_habit_inputs))
		HabitManager.Habit_Manager.add_habit()

		# Asserting the output and the habits_list first element object attributes
		raw_output = capsys.readouterr().out
		words_output = raw_output.split(" ")
		assert "TryHackMe!\n" in words_output
		assert HabitManager.Habit_Manager.habits_list[0].name == self.first_daily_habit.name
		assert HabitManager.Habit_Manager.habits_list[0].description == self.first_daily_habit.description
		assert HabitManager.Habit_Manager.habits_list[0].periodicity == self.first_daily_habit.periodicity
		assert HabitManager.Habit_Manager.habits_list[0].creation_date == HabitManager.Analytics_module.today
		assert HabitManager.Habit_Manager.habits_list[0].habit_id != 0

		# Testing loading from db -> should now return the habit from the database, because it is was saved to the db during add_habit method
		load_habit = HabitManager.SQLiteStorage.load_habit_from_db(HabitManager.Habit_Manager.habits_list[0].habit_id)
		assert load_habit is not None

		# Inputing random data, and especially incorrect data for the habit.periodicity, which results in output with the keyword "incorret" and no habit creation
		test_inputs_with_wrong_period = iter(["Wrong", "Whatever", "Whenever"])
		monkeypatch.setattr("builtins.input", lambda prompt="": next(test_inputs_with_wrong_period))
		HabitManager.Habit_Manager.add_habit()

		# Asserting the output and the habits attributes of habits_list
		raw_output = capsys.readouterr().out
		words_output = raw_output.split(" ")
		assert "incorrect" in words_output
		for habit in HabitManager.Habit_Manager.habits_list:
			assert habit.name != "Wrong"
			assert habit.description != "Whatever"
			assert habit.periodicity != "Whenever"


	# Testing delete_habit method 
	def test_delete_habit(self, capsys, monkeypatch):
		HabitManager.Habit_Manager.habits_list.append(self.second_daily_habit)
		HabitManager.Habit_Manager.habits_list.append(self.third_daily_habit)
		HabitManager.Habit_Manager.habits_list.append(self.first_weekly_habit)

		# Deleting habit from habit_list and database
		monkeypatch.setattr("builtins.input", lambda prompt="": self.second_daily_habit.name)
		HabitManager.Habit_Manager.delete_habit()
		raw_output = capsys.readouterr().out
		words_output = raw_output.split(" ")

		# Asserting if keyword successfully is part of the output and checking the habits_list for the absence of the deleted habit
		assert "successfully" in words_output
		for habit in HabitManager.Habit_Manager.habits_list:
			assert habit.name != self.second_daily_habit.name

		# Testing random input / name of non-existing habit
		monkeypatch.setattr("builtins.input", lambda prompt="": "whawhawha")
		HabitManager.Habit_Manager.delete_habit()
		raw_output = capsys.readouterr().out
		words_output = raw_output.split(" ")
		# Asserting output for negative reply keywords
		assert "no" in words_output
		assert "such" in words_output
		assert "whawhawha." in words_output

	# Testing the update_habit method
	def test_update_habit(self, capsys, monkeypatch):
		HabitManager.Habit_Manager.habits_list.append(self.first_daily_habit)
		HabitManager.Habit_Manager.habits_list.append(self.third_daily_habit)
		HabitManager.Habit_Manager.habits_list.append(self.second_weekly_habit)

		updating_inputs = iter([self.third_daily_habit.name,"Y","Call parents","y","Check with your parents","y","weekly","y","Y"])
		# Deleting habit from habit_list and database
		monkeypatch.setattr("builtins.input", lambda prompt="": next(updating_inputs))
		HabitManager.Habit_Manager.update_habit()
		raw_output = capsys.readouterr().out
		words_output = raw_output.split(" ")

		# Asserting if keyword successfully is part of the output
		assert "Walk" in words_output
		assert "successfully" in words_output
		assert "updated!\n" in words_output

		# Checking the habits_list for the absence of the deleted habit, and the existence of the new habit object
		for habit in HabitManager.Habit_Manager.habits_list:
			assert habit.name != "Walk"
			if habit.name == "Call parents":
				assert habit.description == "Check with your parents"
				assert habit.periodicity == "weekly"
				assert habit.creation_date == HabitManager.Analytics_module.today
				assert len(habit.completion_dates) == 0
				assert habit.habit_id == 1 # because it's the first one saved to the database via update in this scenario

	# Tests the remineder method
	def test_reminder(self, capsys):
		HabitManager.Habit_Manager.habits_list.append(self.first_daily_habit)
		HabitManager.Habit_Manager.habits_list.append(self.second_daily_habit)
		HabitManager.Habit_Manager.habits_list.append(self.third_daily_habit)
		HabitManager.Habit_Manager.habits_list.append(self.first_weekly_habit)
		HabitManager.Habit_Manager.habits_list.append(self.second_weekly_habit)

		# Testing reminder what habits need and are recommended to check off to not lose the streak.
		HabitManager.Habit_Manager.reminder()
		raw_output = capsys.readouterr().out
		words_output = raw_output.split(" ")

		assert "TryHackMe" not in words_output
		assert "Workout" in words_output
		assert "lose" in words_output
		assert "current" in words_output
		assert "Walk" in words_output
		assert "some" in words_output
		assert "Water" not in words_output
		assert "plants" not in words_output
		assert "Digital" in words_output
		assert "Detox" in words_output
		assert "while..\n" in words_output

		#Test all completed
		self.first_daily_habit.mark_completed()
		self.second_daily_habit.mark_completed()
		self.third_daily_habit.mark_completed()
		self.first_weekly_habit.mark_completed()
		self.second_weekly_habit.mark_completed()
		raw_output = capsys.readouterr().out

		HabitManager.Habit_Manager.reminder()
		raw_output = capsys.readouterr().out
		words_output = raw_output.split(" ")
		assert "habit" in words_output
		assert "checked" in words_output
		assert "off" in words_output 
		assert "today!\n" in words_output

	# 
	def teardown_method(self):
		import os
		os.remove("stored_habits.db")
		HabitManager.Habit_Manager.habits_list.clear()
		del self.first_daily_habit
		del self.second_daily_habit
		del self.third_daily_habit
		del self.first_weekly_habit
		del self.second_weekly_habit

pytest.main()