# Module imports
import statistics
from prettytable import PrettyTable


# Calculates and prints statistical measures for the given data.

# Parameters:
# - data (list): List of numerical data.
# - title (str): Title for the table.

# Returns:
# None
def calculate_and_print(data, title):
  table = PrettyTable()
  table.align = "l"
  table.title = title
  table.field_names = ["Data", "Value"]

  table.add_row(["Mean", f'{statistics.mean(data)}'])
  table.add_row(["Mode", f'{statistics.mode(data)}'])
  table.add_row(["Median", f'{statistics.median(data)}'])
  table.add_row(["St_deviation", f'{statistics.stdev(data)}'])
  table.add_row(["Variance", f'{statistics.variance(data)}'])

  print(table)


# Runs statistical calculations and prints the results for degree, velocity, and time data.
def run():
    degree_data = [156, 158, 148, 50, 60, 45, 10, 12, 44, 16]
    calculate_and_print(degree_data, 'Degree')

    velocity_data = [36, 250, 58, 100, 160, 163, 240, 158, 165, 50]
    calculate_and_print(velocity_data, 'Velocity')

    time_data = [20, 19, 24, 56, 28, 16, 18, 22, 16, 16]
    calculate_and_print(time_data, 'Time')


run()