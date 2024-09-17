import re

def modify_percolation_rates(file_path, new_rate):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Use regex to find and replace all instances of percolation rate
    pattern = r'(Percolation Rate:)\s*(\d+(\.\d+)?)'
    new_content, count = re.subn(pattern, f'\\1 {new_rate}', content)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)

    print(f"Updated {count} instances of percolation rate to {new_rate} in {file_path}")

# Get user input
file_path = input("Enter the full path to the .basin file: ")
new_rate = input("Enter the new percolation rate: ")

# Call the function to modify the file
modify_percolation_rates(file_path, new_rate)