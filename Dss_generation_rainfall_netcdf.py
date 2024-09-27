import os
import subprocess
import sys

# Set environment variables
VORTEX_HOME = r"C:\Users\gaurav.fouzdar\Downloads\vortex-0.11.15-rc.6-win-x64\vortex-0.11.15-rc.6"
os.environ["VORTEX_HOME"] = VORTEX_HOME
os.environ["PATH"] = f"{VORTEX_HOME}\\bin;{VORTEX_HOME}\\bin\\gdal;{VORTEX_HOME}\\bin\\netcdf;" + os.environ["PATH"]
os.environ["GDAL_DATA"] = f"{VORTEX_HOME}\\bin\\gdal\\gdal-data"
os.environ["PROJ_LIB"] = f"{VORTEX_HOME}\\bin\\gdal\\projlib"
os.environ["CLASSPATH"] = r"C:\Users\gaurav.fouzdar\Downloads\jython-standalone-2.7.4rc1.jar;" + f"{VORTEX_HOME}\\lib\\*"

# Specify the location for the batch file and Python script
script_directory = r"E:\New folder_3"  # Update this path accordingly
batch_file_path = os.path.join(script_directory, "run_script.bat")
python_script_path = os.path.join(script_directory, "dss_run.py")

# Create or overwrite the batch file
print("Creating batch file...")
batch_file_content = f'''@echo on
set "VORTEX_HOME={VORTEX_HOME}"
set "PATH=%VORTEX_HOME%\\bin;%VORTEX_HOME%\\bin\\gdal;%VORTEX_HOME%\\bin\\netcdf;%PATH%"
set "GDAL_DATA=%VORTEX_HOME%\\bin\\gdal\\gdal-data"
set "PROJ_LIB=%VORTEX_HOME%\\bin\\gdal\\projlib"
set "CLASSPATH=C:\\Users\\gaurav.fouzdar\\Downloads\\jython-standalone-2.7.4rc1.jar;%VORTEX_HOME%\\lib\\*"
echo Running Java command...
%VORTEX_HOME%\\jre\\bin\\java.exe -Xmx2g -Djava.library.path=%VORTEX_HOME%\\bin;%VORTEX_HOME%\\bin\\gdal org.python.util.jython dss_run.py
'''

with open(batch_file_path, 'w') as batch_file:
    batch_file.write(batch_file_content)

print(f"Batch file created at {batch_file_path}")
print("Batch file contents:")
print(batch_file_content)

# Create or overwrite the Python script
print("\nCreating Python script...")
python_script_content = '''
from mil.army.usace.hec.vortex.io import BatchImporter
from mil.army.usace.hec.vortex.geo import WktFactory

# File paths
in_files = ['D:/NIle Files/Rainfall_nc/BN_Aleltu East_clipped.nc']
variables = ['precip']
clip_shp = 'D:/NIle Files/Blue Nile/Blue nile subbasin files/Blue Nile/BN_Aletu_East/BN_Aletu_East.shp'
destination = 'C:/Users/gaurav.fouzdar/Desktop/New.dss'

# Geo options for clipping
geo_options = {
    'pathToShp': clip_shp,
    'targetCellSize': '2000',
    'targetWkt': WktFactory.shg(),
    'resamplingMethod': 'Bilinear'
}

# Write options
write_options = {'partF': 'my script import'}
write_options['partA'] = 'SHG'
write_options['partB'] = 'basin'

# Build the importer
myImport = BatchImporter.builder() \\
    .inFiles(in_files) \\
    .variables(variables) \\
    .geoOptions(geo_options) \\
    .destination(destination) \\
    .writeOptions(write_options) \\
    .build()

# Process the import
print("Starting import process...")
myImport.process()
print("Import process completed.")
'''

with open(python_script_path, 'w') as python_file:
    python_file.write(python_script_content)

print(f"Python script created at {python_script_path}")
print("Python script contents:")
print(python_script_content)

# Function to run the batch process and display output in real-time
def run_batch_process():
    print("\nExecuting batch file...")
    os.chdir(script_directory)
    
    process = subprocess.Popen(batch_file_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    for line in process.stdout:
        print(line, end='')
        sys.stdout.flush()  # Ensure output is displayed immediately
    
    process.wait()
    
    if process.returncode != 0:
        print(f"Batch process exited with error code {process.returncode}")
    else:
        print("Batch process completed successfully")

# Run the batch process
if __name__ == "__main__":
    run_batch_process()
