import matplotlib.pyplot as plt


# Takes a txt file and returns a graph


def main():
    # Set task start and finish time
    if str(input("TIMESTAMP? ")) in ["YES", "yes", "Y", "y"]:
        task_start = int(input("Enter task start time (TIMESTAMP): "))
        task_end = int(input("Enter task end time (TIMESTAMP): "))
    else:
        task_start = None
        task_end = None 
    start_reading_pos = None
    end_reading_pos = None
    watt_values = []
    readings = []
    timestamps = []
    counter = 1
    with open("power_consumption.txt", encoding="utf-8") as f:
        for row in f:
            # Check not a timestamp
            if "^" not in row:
                # Y AXIS
                char_pos = row.find("W")
                # We only want everything before the first "W"
                sliced_row = row[:char_pos]
                space_pos = sliced_row.find(" ")
                # we only want things after the first space
                # replace remaining spaces with ""
                watts = sliced_row[space_pos:].replace(" ", "")
                # Add to array
                watt_values.append(float(watts))
            else:
                timestamp = int(row[12:])
                if timestamp == task_start:
                    start_reading_pos = counter
                elif timestamp == task_end:
                    end_reading_pos = counter
                timestamps.append(timestamp)
                readings.append(counter)
                counter += 1
                # Starting and ending time stamp to work out seconds
    initial_timestamp = int(timestamps[0])
    final_timestamp = int(timestamps[-1])
    execution_time = final_timestamp - initial_timestamp
    # seconds it was running seconds
    # Create graph
    plt.plot(readings, watt_values)
    plt.ylabel("Power Consumption (Watts)")
    plt.xlabel(f"Number of readings over {execution_time} seconds")
    # Plot task start and end times
    if start_reading_pos is not None:
        plt.plot(readings[start_reading_pos], watt_values[start_reading_pos], ">", label="Task Start")
        plt.plot(readings[end_reading_pos], watt_values[end_reading_pos], "s", label="Task End")
        plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
