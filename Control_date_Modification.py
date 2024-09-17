import os
import re
import pandas as pd
from datetime import datetime

def update_control_file(file_path, new_start_date, new_end_date, new_start_time, new_end_time):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Update the Start Date
    content = re.sub(r'Start Date: .*', f'Start Date: {new_start_date}', content)
    # Update the End Date
    content = re.sub(r'End Date: .*', f'End Date: {new_end_date}', content)
    
    # Update the Start Time
    content = re.sub(r'Start Time: .*', f'Start Time: {new_start_time}', content)
    # Update the End Time
    content = re.sub(r'End Time: .*', f'End Time: {new_end_time}', content)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

# Get user input
csv_path = r"C:\Users\gaurav.fouzdar\Desktop\links and data.csv"
new_start_date = r"01 January 1981"
new_start_time = r"00:00"
new_end_date = r"31 December 2023"
new_end_time = r"00:00"

# Read the CSV file
df = pd.read_csv(csv_path)

# Validate the date format
date_format = "%d %B %Y"
try:
    datetime.strptime(new_start_date, date_format)
    datetime.strptime(new_end_date, date_format)
except ValueError:
    print("Invalid date format. Please use DD Month YYYY (e.g., 31 December 1980)")
else:
    # Iterate through each row in the CSV file
    for index, row in df.iterrows():
        directory = row['Project directory']
        file_name = row['Control name']
        
        # Ensure the file has a .control extension
        if not file_name.lower().endswith('.control'):
            file_name += '.control'
        
        # Construct the full file path
        file_path = os.path.join(directory, file_name)
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Update the file
            update_control_file(file_path, new_start_date, new_end_date, new_start_time, new_end_time)
            print(f"File {file_name} has been updated successfully.")
        else:
            print(f"File {file_name} not found in {directory}.")

print("All files have been processed.")
