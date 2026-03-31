import pytest
import Analytics_module # This test file differs a little bit from the prod Analytics_module.py (freezed today's date to "2026-03-28")
from datetime import datetime,  timedelta
from freezegun import freeze_time
from SQLiteStorage import formatting_date

class Test_analytics_module:

	# Setting up 5 test habits with 4 weeks of data
	def setup_method(self):
		self.first_daily_habit = Analytics_module.HabitManager.Habit.Habit(name="TryHackMe", description="Do some tasks and rooms", periodicity="daily", creation_date=formatting_date("2026-03-01"))
		# Test scenario with current_streak 13 and longest_streak 14
		first_daily_habit_dates = ["2026-03-01","2026-03-02","2026-03-03","2026-03-04","2026-03-05","2026-03-06","2026-03-07","2026-03-08","2026-03-09","2026-03-10","2026-03-11","2026-03-12","2026-03-13","2026-03-14","2026-03-16","2026-03-17","2026-03-18","2026-03-19","2026-03-20","2026-03-21","2026-03-22","2026-03-23","2026-03-24","2026-03-25","2026-03-26","2026-03-27","2026-03-28"]
		for date in first_daily_habit_dates:
			self.first_daily_habit.completion_dates.append(formatting_date(date))

		self.second_daily_habit = Analytics_module.HabitManager.Habit.Habit(name="Workout",description="Example Habit: Do some exercises from your exercise week plan",periodicity="daily",creation_date=formatting_date("2026-03-01"))
		# Test scenario with current_streak and longest_streak 9
		second_daily_habit_dates = ["2026-03-02","2026-03-03","2026-03-04","2026-03-07","2026-03-08","2026-03-10","2026-03-11","2026-03-13","2026-03-19","2026-03-20","2026-03-21","2026-03-22","2026-03-23","2026-03-24","2026-03-25","2026-03-26","2026-03-27"]
		for date in second_daily_habit_dates:
			self.second_daily_habit.completion_dates.append(formatting_date(date))

		self.third_daily_habit = Analytics_module.HabitManager.Habit.Habit(name="Walk",description="Example Habit: Walk about 10k steps",periodicity="daily",creation_date=formatting_date("2026-03-01"))
		# Test scenario with current_streak 0 and longest_streak 4
		third_daily_habit_dates = ["2026-03-04","2026-03-07","2026-03-08","2026-03-10","2026-03-11","2026-03-13","2026-03-19","2026-03-20","2026-03-21","2026-03-23","2026-03-24","2026-03-25","2026-03-26"]
		for date in third_daily_habit_dates:
			self.third_daily_habit.completion_dates.append(formatting_date(date))

		self.first_weekly_habit = Analytics_module.HabitManager.Habit.Habit(name="Water plants", description="Water the house plants", periodicity="weekly", creation_date=formatting_date("2026-03-01"))
		# Test scenario with current_streak 1 and longest_streak 3
		first_weekly_habit_dates = ["2026-03-01","2026-03-03","2026-03-14","2026-03-27"]
		for date in first_weekly_habit_dates:
			self.first_weekly_habit.completion_dates.append(formatting_date(date))

		self.second_weekly_habit = Analytics_module.HabitManager.Habit.Habit(name="Digital Detox",description="Example Habit: Watch some birds or dogs in the park for a couple of hours",periodicity="weekly",creation_date=formatting_date("2026-03-01"))
		# Test scenario with current_streak 0 and longest_streak 3
		second_weekly_habit_dates = ["2026-03-01","2026-03-02","2026-03-09"]
		for date in second_weekly_habit_dates:
			self.second_weekly_habit.completion_dates.append(formatting_date(date))

		# Adding them to the operational list
		Analytics_module.HabitManager.Habit_Manager.habits_list.append(self.first_daily_habit)
		Analytics_module.HabitManager.Habit_Manager.habits_list.append(self.second_daily_habit)
		Analytics_module.HabitManager.Habit_Manager.habits_list.append(self.third_daily_habit)
		Analytics_module.HabitManager.Habit_Manager.habits_list.append(self.first_weekly_habit)
		Analytics_module.HabitManager.Habit_Manager.habits_list.append(self.second_weekly_habit)

	# Testing the streak calculation for daily habits #freezing today's date to the 28th of March 2026
	@freeze_time("2026-03-28")
	def test_calculate_streak_daily(self):

		today = datetime.today().date()
		yesterday = today - timedelta(days=1)
		assert str(yesterday) == "2026-03-27", str(today) == "2026-03-28"

		# Test scenario with current_streak 13 and longest_streak 14
		result = Analytics_module.calculate_streak(self.first_daily_habit) #returns a tuple (current_streak, longest_streak)
		assert int(result[0]) == 13, int(result[1]) == 14

		# Test scenario with current_streak and longest_streak 9
		result = Analytics_module.calculate_streak(self.second_daily_habit) #returns a tuple (current_streak, longest_streak)
		assert int(result[0]) == 9, int(result[1]) == 9

		# Test scenario with current_streak 0 and longest_streak 4
		result = Analytics_module.calculate_streak(self.third_daily_habit) #returns a tuple (current_streak, longest_streak)
		assert int(result[0]) == 0, int(result[1]) == 4


	# Testing the streak calculation for daily habits #freezing today's date to the 28th of March 2026
	# Note: If the streak break, the current_streak resets to 1 and the new starting date(previous_deadline) will be set to the last check_off.
	@freeze_time("2026-03-28")
	def test_calculate_streak_weekly(self):
		today = datetime.today().date()
		yesterday = today - timedelta(days=1)
		assert str(yesterday) == "2026-03-27", str(today) == "2026-03-28"

		# Test scenario with current_streak 1 and longest_streak 3
		result = Analytics_module.calculate_streak(self.first_weekly_habit) #returns a tuple (current_streak, longest_streak)
		assert int(result[0]) == 1, int(result[1]) == 3
		self.first_weekly_habit.completion_dates.clear()

		# Test scenario with current_streak 0 and longest_streak 3
		result = Analytics_module.calculate_streak(self.second_weekly_habit) #returns a tuple (current_streak, longest_streak)
		assert int(result[0]) == 0, int(result[1]) == 3
		self.second_weekly_habit.completion_dates.clear()

		# Test scenario with the current_streak 5 is also the longest_streak
		dates = ["2026-03-01","2026-03-02","2026-03-06","2026-03-09","2026-03-17",str(yesterday)]
		for date in dates:
			self.first_weekly_habit.completion_dates.append(formatting_date(date))

		#returns a tuple with current_streak and longest_streak
		result = Analytics_module.calculate_streak(self.first_weekly_habit) 
		assert int(result[0]) == 5, int(result[1]) == 5
		self.first_weekly_habit.completion_dates.clear()

		
		# Test scenario with the current_streak 2 is also the longest_streak
		dates = ["2026-03-01","2026-03-21","2026-03-23",str(today)]
		for date in dates:
			self.second_weekly_habit.completion_dates.append(formatting_date(date))
		result = Analytics_module.calculate_streak(self.second_weekly_habit) #returns a tuple (current_streak, longest_streak)
		assert int(result[0]) == 2, int(result[1]) == 2
		self.second_weekly_habit.completion_dates.clear()

	# Testing the list all habits function & asserting if all the attributes are mentioned
	def test_list_all_habits(self, capsys):

		Analytics_module.list_habits()
		captured = capsys.readouterr().out
		list_of_output_paragraphs = captured.split("\n")
		list_of_output_words = []
		for phrase in list_of_output_paragraphs:
			list_of_output_words.extend(phrase.split(" "))

		# Testing output of the display habit method of the first_daily_habit
		for name_word in self.first_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.first_daily_habit.description.split(" "):
			assert description_word in list_of_output_words
		assert self.first_daily_habit.periodicity in list_of_output_words
		assert str(self.first_daily_habit.creation_date) in list_of_output_words

		# Testing output of the display habit method of the second_daily_habit
		for name_word in self.second_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.second_daily_habit.description.split(" "):
			assert description_word in list_of_output_words

		# Testing output of the display habit method of the third_daily_habit
		for name_word in self.third_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.third_daily_habit.description.split(" "):
			assert description_word in list_of_output_words

		# Testing output of the display habit method of the first_weekly_habit
		for name_word in self.first_weekly_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.first_weekly_habit.description.split(" "):
			assert description_word in list_of_output_words
		assert self.first_weekly_habit.periodicity in list_of_output_words
		assert str(self.first_weekly_habit.creation_date) in list_of_output_words

		# Testing output of the display habit method of the second_weekly_habit
		for name_word in self.second_weekly_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.second_weekly_habit.description.split(" "):
			assert description_word in list_of_output_words

	# Testing the list habits by period function & asserting if all the attributes are mentioned
	# Additionally testing any other incorret input
	def test_list_habits_by_periodicity(self, capsys, monkeypatch):

		monkeypatch.setattr("builtins.input", lambda prompt="": "daily")
		Analytics_module.list_habits_by_periodicity()
		captured = capsys.readouterr().out
		list_of_output_paragraphs = captured.split("\n")
		list_of_output_words = []
		for phrase in list_of_output_paragraphs:
			list_of_output_words.extend(phrase.split(" "))

		# Testing output of the display habit method of the first_daily_habit
		for name_word in self.first_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.first_daily_habit.description.split(" "):
			assert description_word in list_of_output_words
		assert self.first_daily_habit.periodicity in list_of_output_words
		assert str(self.first_daily_habit.creation_date) in list_of_output_words

		# Testing output of the display habit method of the second_daily_habit
		for name_word in self.second_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.second_daily_habit.description.split(" "):
			assert description_word in list_of_output_words

		# Testing output of the display habit method of the third_daily_habit
		for name_word in self.third_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.third_daily_habit.description.split(" "):
			assert description_word in list_of_output_words

		# Testing output of the display habit method of the first_weekly_habit (not)
		for name_word in self.first_weekly_habit.name.split(" "):
			assert name_word not in list_of_output_words

		# Testing output of the display habit method of the second_weekly_habit (not)
		for name_word in self.second_weekly_habit.name.split(" "):
			assert name_word not in list_of_output_words

		monkeypatch.setattr("builtins.input", lambda prompt="": "weekly")
		Analytics_module.list_habits_by_periodicity()
		captured = capsys.readouterr().out
		list_of_output_paragraphs = captured.split("\n")
		list_of_output_words = []
		for phrase in list_of_output_paragraphs:
			list_of_output_words.extend(phrase.split(" "))

		# Testing output of the display habit method of the first_weekly_habit
		for name_word in self.first_weekly_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.first_weekly_habit.description.split(" "):
			assert description_word in list_of_output_words
		assert self.first_weekly_habit.periodicity in list_of_output_words
		assert str(self.first_weekly_habit.creation_date) in list_of_output_words

		# Testing output of the display habit method of the second_weekly_habit
		for name_word in self.second_weekly_habit.name.split(" "):
			assert name_word in list_of_output_words
		for description_word in self.second_weekly_habit.description.split(" "):
			assert description_word in list_of_output_words

		# Testing output of the display habit method of the first_daily_habit
		for name_word in self.first_daily_habit.name.split(" "):
			assert name_word not in list_of_output_words

		# Testing output of the display habit method of the second_daily_habit
		for name_word in self.second_daily_habit.name.split(" "):
			assert name_word not in list_of_output_words

		# Testing output of the display habit method of the third_daily_habit
		for name_word in self.third_daily_habit.name.split(" "):
			assert name_word not in list_of_output_words

		incorret_inputs = iter(["wrong", "test", "anything else"])
		monkeypatch.setattr("builtins.input", lambda prompt="": next(incorret_inputs))
		Analytics_module.list_habits_by_periodicity()
		captured = capsys.readouterr().out
		list_of_output_paragraphs = captured.split("\n")
		list_of_output_words = []
		for phrase in list_of_output_paragraphs:
			list_of_output_words.extend(phrase.split(" "))
		assert "incorrect" in list_of_output_words
	
	# Testing output of the longest streak of all habits function (first_daily_habit: Study & 13)
	def test_longest_streak(self, capsys):
		Analytics_module.longest_streak()
		captured = capsys.readouterr().out
		list_of_output_words = captured.split(" ")
		for name_word in self.first_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		assert "13!\n" in list_of_output_words 

	# Testing each habit for output about its' longest current streak and longest streak in the past (highscore)
	def test_longest_streak_of_a_habit(self, capsys):
		# Study & current 13, longest 14
		Analytics_module.longest_streak_of_a_habit(self.first_daily_habit)
		captured = capsys.readouterr().out
		list_of_output_words = captured.split(" ")
		for name_word in self.first_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		assert "13" in list_of_output_words
		assert "14" in list_of_output_words 

		# Workout & current and longest 9
		Analytics_module.longest_streak_of_a_habit(self.second_daily_habit)
		captured = capsys.readouterr().out
		list_of_output_words = captured.split(" ")
		for name_word in self.second_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		assert "9!\n" in list_of_output_words 

		# Walk & current 0 and longest 4
		Analytics_module.longest_streak_of_a_habit(self.third_daily_habit)
		captured = capsys.readouterr().out
		list_of_output_words = captured.split(" ")
		for name_word in self.third_daily_habit.name.split(" "):
			assert name_word in list_of_output_words
		assert "0" in list_of_output_words 
		assert "4" in list_of_output_words  

		# Water plants & current 1 and longest 3
		Analytics_module.longest_streak_of_a_habit(self.first_weekly_habit)
		captured = capsys.readouterr().out
		list_of_output_words = captured.split(" ")
		for name_word in self.first_weekly_habit.name.split(" "):
			assert name_word in list_of_output_words
		assert "1" in list_of_output_words 
		assert "3" in list_of_output_words

		# Digital Detox & current 0 and longest 3
		Analytics_module.longest_streak_of_a_habit(self.second_weekly_habit)
		captured = capsys.readouterr().out
		list_of_output_words = captured.split(" ")
		for name_word in self.second_weekly_habit.name.split(" "):
			assert name_word in list_of_output_words
		assert "0" in list_of_output_words 
		assert "3" in list_of_output_words  

	# Clearing the habits_list and deleting all the habit objects
	def teardown_method(self):
		Analytics_module.HabitManager.Habit_Manager.habits_list.clear()
		del self.first_daily_habit
		del self.second_daily_habit
		del self.third_daily_habit
		del self.first_weekly_habit
		del self.second_weekly_habit

pytest.main()