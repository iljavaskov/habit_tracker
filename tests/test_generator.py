import pytest
import Generator

class TestGenerator:

	# Setting up example habits
	def setup_method(self):
		Generator.example_habit_data_generator()

	# Testing internal function that generates random dates within the last 4 weeks
	def test_random_past_dates(self):
		random_number = Generator.random.randint(0,20)
		dates_list = Generator.random_past_dates(random_number)
		assert len(dates_list) == random_number

		for date in dates_list:
			assert Generator.today_four_weeks_ago <= date < Generator.today

	# Testing internal function that it generates exactly 5 pre-defined example habits
	def test_example_habit_data_generator(self):
		count = 0
		for example in Generator.HabitManager.Habit_Manager.habits_list:
			example.display_habit()
			count += 1
		assert count == 5

	# Testing internal function that it removes the 5 pre-defined example habits
	def test_remove_example_habits(self):
		Generator.remove_example_habits()
		count = len(Generator.HabitManager.Habit_Manager.habits_list)
		assert count == 0

	# Removing any created objects and clearing the habits_list
	def teardown_method(self):
		count = len(Generator.HabitManager.Habit_Manager.habits_list)
		while count != 0:
			example = Generator.HabitManager.Habit_Manager.habits_list[0]
			Generator.HabitManager.Habit_Manager.habits_list.remove(example)
			del example
			count -= 1

pytest.main()