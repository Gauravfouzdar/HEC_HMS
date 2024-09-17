import re
import os
import pandas as pd

def modify_groundwater_parameters(file_path, factors):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Define the parameters and their corresponding regex patterns
    parameters = [
        "GW-1 Baseflow Fraction:",
        "GW-1 Number Reservoirs:",
        "GW-1 Routing Coefficient:",
        "GW-2 Baseflow Fraction:",
        "GW-2 Number Reservoirs:",
        "GW-2 Routing Coefficient:"
    ]

    total_changes = 0

    # Modify each parameter
    for param in parameters:
        pattern = fr'({re.escape(param)})\s*(\d+(\.\d+)?)'
        
        def replace_func(match):
            original_value = float(match.group(2))
            new_value = original_value * factors[param]
            return f"{match.group(1)} {new_value:.6f}"

        new_content, count = re.subn(pattern, replace_func, content)
        content = new_content
        total_changes += count

        print(f"Updated {count} instances of {param}")

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Total updates: {total_changes} in {file_path}")

# Get user input for Excel file
excel_file = input("Enter the full path to the Excel file containing basin information: ")

# Read the Excel file
df = pd.read_excel(excel_file)

# Get factors for each parameter
factors = {}
for param in [
    "GW-1 Baseflow Fraction:",
    "GW-1 Number Reservoirs:",
    "GW-1 Routing Coefficient:",
    "GW-2 Baseflow Fraction:",
    "GW-2 Number Reservoirs:",
    "GW-2 Routing Coefficient:"
]:
    factor = float(input(f"Enter the multiplication factor for {param}: "))
    factors[param] = factor

# Process each basin file
for index, row in df.iterrows():
    project_dir = row['Project directory']
    basin_name = row['Basin name']
    file_path = os.path.join(project_dir, f"{basin_name}.basin")
    
    if os.path.exists(file_path):
        print(f"\nProcessing: {file_path}")
        modify_groundwater_parameters(file_path, factors)
    else:
        print(f"\nError: File not found - {file_path}")

print("\nAll basin files have been processed.")