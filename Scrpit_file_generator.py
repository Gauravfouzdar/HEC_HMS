import pandas as pd
import os
import subprocess

def generate_hms_script(excel_path, output_path):
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Extract the arrays
    project_names = df['.hms name'].tolist()
    project_paths = df['Project directory'].tolist()
    compute_names = df['compute Name'].tolist()
    
    # Create the content of the .script file
    script_content = f"""from hms.model.JythonHms import *
import os
import time

# Arrays to store project information
project_names = {project_names}
project_paths = {project_paths}
compute_names = {compute_names}

# Ensure all arrays have the same length
if len(project_names) == len(project_paths) == len(compute_names):
    # Iterate through the projects
    for i in range(len(project_names)):
        project_name = project_names[i]
        project_path = project_paths[i]
        compute_name = compute_names[i]
        
        # Delete the .dss file with the corresponding compute name
        dss_file_path = os.path.join(project_path, "%s.dss" % compute_name)
        if os.path.exists(dss_file_path):
            os.remove(dss_file_path)
            print("Deleted file: %s" % dss_file_path)
            
            # Add a delay of 2 seconds
            time.sleep(2)
        
        # Open the project
        OpenProject(project_name, project_path)
        
        # Perform the computation
        Compute(compute_name)
        
        # Optional: Add a print statement to show progress
        print("Completed run for project: " + project_name + ", compute: " + compute_name)
    
    # Optional: Add a completion message
    print("All HEC-HMS runs completed.")
else:
    print("Error: Arrays must have the same length.")
"""
    
    # Write the content to the .script file
    with open(output_path, 'w') as f:
        f.write(script_content)
    
    print(f"Script file generated successfully at: {output_path}")

# Get input from user
excel_path = r"C:\Users\gaurav.fouzdar\Desktop\links and data.xlsx"
output_path = r"D:\Nile project\TRIAL_2"

# Ensure the output file has .script extension
if not output_path.endswith('.script'):
    output_path += '.script'

# Generate the script
generate_hms_script(excel_path, output_path)

#function to run the cmd
def run_hec_hms_script(working_directory, script_path):
    try:
        # Change to the directory where hec-hms.cmd is located
        os.chdir(working_directory)
        
        # Command to run HEC-HMS with the script
        command = f'hec-hms.cmd -s "{script_path}"'
        
        # Execute the command and open it in a new Command Prompt window
        subprocess.run(f'start cmd /K "{command}"', shell=True)
        
    except Exception as e:
        print(f"An exception occurred: {e}")

# Path to the working directory where hec-hms.cmd is located
working_directory = r"C:\Users\gaurav.fouzdar\HEC\HEC-HMS\4.10"

# Path to the script you want to run
script_path = output_path

# Run the HEC-HMS script
run_hec_hms_script(working_directory, script_path)
