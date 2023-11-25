# Module imports
import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable


# Constants definition
TIME_POSITION = 1
HEIGHTS_ACCURACY_POSITION = 8
HEIGHTS_POSITION = 9
CUSTOM_DPI = 400
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60
FIGSIZE = 20

# Upload file and read data from it
#
# Returns parsed data from file
def upload_file(path="./data_14.txt"):
    # GPGGA sentence provides information about the time, latitude, longitude, fix quality,
    # number of satellites, GPS accuracy, altitude, and other GPS-related data.

    # Open the file and read its lines into an array
    with open(path, "r") as file:
        lines = file.readlines()

    # Returns parsed data
    return lines


# Extract times, heights and heights_accuracy info from data
#
# Returns array of times, heights and heights_accuracy
def extract_data(data):
    # Split each line only once and store the result for reuse
    split_lines = [line.split(",") for line in data]

    # Extract the desired data using list comprehensions
    times = [line[TIME_POSITION] for line in split_lines]
    heights = [line[HEIGHTS_POSITION] for line in split_lines]
    heights_accuracy = [line[HEIGHTS_ACCURACY_POSITION] for line in split_lines]

    return times, heights, heights_accuracy


# Convert data
#
# Returns converted time, height and height_accuracy
def convert_data(times, heights, heights_accuracy):
    times_conv = np.array([convert_to_seconds(time) for time in times])
    heights_conv = np.array([float(h) for h in heights])
    heights_accuracy_conv = np.array([float(hc) for hc in heights_accuracy])

    return times_conv, heights_conv, heights_accuracy_conv


# Perform calculations and prints results to STDOUT
#
# Returns speed and t_distance
def calculate_info(times_cv, heights_cv, h_accuracy_cv):
    # General calculations
    time_diff = np.diff(times_cv)
    speed = np.array(h_accuracy_cv[:-1] / time_diff)
    t_distance = np.cumsum(h_accuracy_cv[:-1] * time_diff)

    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["Metric", "Value"]

    # Total flight route length:
    total_distance = np.sum(h_accuracy_cv[:-1] * time_diff)
    table.add_row(["Total flight route length", f"{total_distance:.2f} meters"])

    # Average flight speed
    average_speed = total_distance / (times_cv[-1] - times_cv[0])
    table.add_row(["Average flight speed", f"{average_speed:.2f} m/s"])

    # Min and max flight speed
    min_speed = np.min(speed)
    table.add_row(["Minimal speed", f"{min_speed} m/s"])

    max_speed = np.max(speed)
    table.add_row(["Maximum speed", f"{max_speed} m/s"])

    # Min and max flight height
    min_height = np.min(heights_cv)
    table.add_row(["Minimal height", f"{min_height} m"])

    max_height = np.max(heights_cv)
    table.add_row(["Maximum height", f"{max_height} m"])

    # Total flight time
    total_flight_time = times_cv[-1] - times_cv[0]
    human_readable_time = convert_seconds_to_time(total_flight_time)
    table.add_row(["Total flight time", human_readable_time])

    # Print the table
    print(table)

    return speed, t_distance


def generate_charts(times_cv, heights_cv, speed, t_distance):
    time = np.array([convert_seconds_to_time(t) for t in times_cv])

    # Flight speed / time chart
    plt.figure(figsize=(FIGSIZE, plt.gcf().get_figheight()))
    plt.plot(time[1:], speed)
    plt.title('Flight speed')
    plt.xlabel('time')
    plt.ylabel('flight speed (m/s)')

    save_chart_to_file(plt, './output_1')

    # FLight height / time chart
    plt.figure(figsize=(FIGSIZE, plt.gcf().get_figheight()))
    plt.plot(time, heights_cv)
    plt.title('Flight height')
    plt.xlabel('time')
    plt.ylabel('flight height (m)')

    save_chart_to_file(plt, './output_2')

    # Flight distance chart
    plt.figure(figsize=(FIGSIZE, plt.gcf().get_figheight()))
    plt.plot(time[1:], t_distance)
    plt.title('Flight distance')
    plt.xlabel('time')
    plt.ylabel('Flight distance (m)')

    save_chart_to_file(plt, './output_3')


## Helpers


# Convert seconds string format
#
# Returns string in HH-MM-SS format
def convert_seconds_to_time(seconds):
    hours, remainder = divmod(int(seconds), SECONDS_IN_HOUR)
    minutes, seconds = divmod(remainder, SECONDS_IN_MINUTE)

    return f'{hours:02}:{minutes:02}:{seconds:02}'


# Save chat to the given path.
# It's required since the docker project setup
def save_chart_to_file(plt, out_path):
    plt.savefig(out_path, dpi=CUSTOM_DPI)


# Convert string to seconds format
#
# Returns seconds
def convert_to_seconds(time_str):
    hours = int(time_str[0:2])
    minutes = int(time_str[2:4])
    seconds = int(time_str[4:6])
    fractions = int(time_str[7:])

    return hours * SECONDS_IN_HOUR + minutes * SECONDS_IN_MINUTE + seconds + fractions / 100


## Application entrypoint
def _main():
    # Data preparation
    data = upload_file()
    times, heights, h_accuracy = extract_data(data)

    # Data conversion
    times_conv, heights_conv, heights_accuracy_conv = convert_data(times, heights, h_accuracy)

    # Calculations
    speed, t_distance = calculate_info(times_conv, heights_conv, heights_accuracy_conv)

    # Generate charts based on the data
    generate_charts(times_conv, heights_conv, speed, t_distance)


_main()
