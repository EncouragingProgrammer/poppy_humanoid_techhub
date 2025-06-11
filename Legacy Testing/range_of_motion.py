import json
import pandas as pd

# Load the JSON data from file
with open('position_recordings/range_of_motion.json', 'r') as file:
    data = json.load(file)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
df.to_csv('position_recordings/range_of_motion_pivoted.csv', index=False)
