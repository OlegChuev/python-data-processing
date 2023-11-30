# Module imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from prettytable import PrettyTable


# Constants
STEP_10 = 10
STEP_20 = 20
CUSTOM_DPI = 400


# Upload file and read data from it
#
# Parameters:
# - path (str): Path to the CSV file (default: "./data_4.csv").
#
# Returns time, heading, and pitch arrays.
def upload_file(path="./data_4.csv"):
    data = pd.read_csv(path)

    # Returns parsed data
    return data['time'], data['head'], data['pitch']


# Generate graphical dependencies for tasks 1 and 2.
#
# Parameters:
# - time (numpy array): Array of time values.
# - heading (numpy array): Array of heading angles.
# - pitch (numpy array): Array of pitch angles.
#
# Returns:
# None
def generate_and_save_figures(time, heading, pitch):
    # Graphs without step
    print_figure(time, heading, 'Dependence of course angles on time')
    print_figure(time, pitch, 'Dependence of roll angles on time')

    # Averaged graphs with a step of 10 seconds
    avr_time_10_step, avr_heading_10_step, avr_pitch_10_step = averaged_with_step(time, heading, pitch, STEP_10)
    print_figure(avr_time_10_step, avr_heading_10_step, f'Dependence of averaged course angles on time (step {STEP_10} seconds)')
    print_figure(avr_time_10_step, avr_pitch_10_step, f'Dependence of averaged roll angles on time (step {STEP_10} seconds)')

    # Averaged graphs with a step of 20 seconds
    avr_time_20_step, avr_heading_20_step, avr_pitch_20_step = averaged_with_step(time, heading, pitch, STEP_20)
    print_figure(avr_time_20_step, avr_heading_20_step, f'Dependence of averaged course angles on time (step {STEP_20} seconds)')
    print_figure(avr_time_20_step, avr_pitch_20_step, f'Dependence of averaged roll angles on time (step {STEP_20} seconds)')



# Calculate statistical data for heading and pitch angles.
#
# Parameters:
# - heading (numpy array): Array of heading angles.
# - pitch (numpy array): Array of pitch angles.
#
# Returns:
# None
def stats_data(heading, pitch):
    # Average values
    mean_heading = np.mean(heading)
    mean_pitch = np.mean(pitch)

    # Calculate RMS deviations
    std_heading = np.std(heading)
    std_pitch = np.std(pitch)

    # Calculate maximum deviations from the mean
    max_dev_heading = np.max(np.abs(heading - mean_heading))
    max_dev_pitch = np.max(np.abs(pitch - mean_pitch))

    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["Metric", "Value"]

    table.add_row(["The average value of the course angle", f"{mean_heading} °"])
    table.add_row(["RMS deviation of the course angle", f"{std_heading} °"])
    table.add_row(["RMS deviation of roll angle", f"{std_pitch} °"])
    table.add_row(["The maximum deviation of the course angle", f"{max_dev_heading} °"])
    table.add_row(["Maximum roll angle deviation", f"{max_dev_pitch} °"])

    # Print the table
    print(table)


# Calculate averaged data for the specified step.
#
# Parameters:
# - time (numpy array): Array of time values.
# - heading (numpy array): Array of heading angles.
# - pitch (numpy array): Array of pitch angles.
# - step (float): Step for averaging.
#
# Returns:
# Tuple of averaged time, heading, and pitch arrays.
def averaged_with_step(time, heading, pitch, step):
    min_time, max_time = min(time), max(time)
    averaged_time_step = np.arange(min_time, max_time, step)

    def calculate_averages(data):
        return [np.mean(data[(time >= t) & (time < t + step)]) for t in averaged_time_step]

    averaged_heading_step = calculate_averages(heading)
    averaged_pitch_step = calculate_averages(pitch)

    return averaged_time_step, averaged_heading_step, averaged_pitch_step


#  Plot and print a figure.
#
#  Parameters:
#  - x_data (list): X-axis data.
#  - y_data (list): Y-axis data.
#  - string (str): Title of the plot.
#
#   Returns:
#   None
def print_figure(x_data, y_data, string):
    plt.figure(figsize=(12, 6))
    plt.plot(x_data, y_data)
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (°)')
    plt.title(string)
    time.sleep(1)
    save_chart_to_file(plt)


# Save the given Matplotlib plot to a file. It's required since the docker project setup
#  Parameters:
#  - plt (matplotlib.pyplot): Matplotlib plot to be saved.
#  - out_path (str): Output path for the saved chart (default: './chart_').
#
#  Returns:
#  None
def save_chart_to_file(plt, out_path = './chart_'):
    file_name = out_path + str(int(time.time()))
    plt.savefig(file_name, dpi=CUSTOM_DPI)


## Application entrypoint
def _main():
    time, heading, pitch = upload_file()
    generate_and_save_figures(time, heading, pitch)
    stats_data(heading, pitch)


if __name__ == '__main__':
    _main()
