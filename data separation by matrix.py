import pandas as pd

# Define the input and output file names
input_file = "gaze_positions_on_surface_Surface 1.csv"
output_file_prefix = "output_"

# Define the 20x2 matrix with the custom interval start and end times
# Example matrix: (You should provide your own matrix)
intervals = [
    [353,778],
    [991,1403],
    [1615,2030],
    [2238,2659],
    [2872,3285],
    [3500,3921],
    [4135,4556],
    [4773,5192],
    [5409,5828],
    [6042,6468],
    [6687,7113],
    [7331,7760],
    [7974,8393],
    [8611,9042],
    [9260,9686],
    [9903,10311],
    [10515,10935],
    [11157,11581], 
    [11800,12234],
    [12453,12881]
]

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(input_file)

# Find the column with time in seconds, replace 'frame_column' with the actual column name
frame_column = 'world_index'
if frame_column not in df.columns:
    print(f"Time column '{frame_column}' not found in the CSV file.")
else:
    # Convert the time column to integers (assuming it's in seconds)
    df[frame_column] = df[frame_column].astype(int)

    # Create 20 different CSV files based on the custom intervals
    num_intervals = len(intervals)

    for i in range(num_intervals):
        # Get the custom interval start and end times for the current row
        interval_start = intervals[i][0]
        interval_end = intervals[i][1]

        # Select rows within the current custom interval
        interval_data = df[(df[frame_column] >= interval_start) & (df[frame_column] <= interval_end)]

        # Create the output file name
        output_file_name = f"{output_file_prefix}{i + 1}.csv"

        # Save the interval data to a new CSV file
        interval_data.to_csv(output_file_name, index=False)

        print(f"File '{output_file_name}' created with data from {interval_start} to {interval_end} seconds.")