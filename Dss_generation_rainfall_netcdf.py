import os
import subprocess

# Set environment variables
VORTEX_HOME = r"C:\Users\gaurav.fouzdar\Downloads\vortex-0.11.15-rc.6-win-x64\vortex-0.11.15-rc.6"
os.environ["VORTEX_HOME"] = VORTEX_HOME
os.environ["PATH"] = f"{VORTEX_HOME}\\bin;{VORTEX_HOME}\\bin\\gdal;" + os.environ["PATH"]
os.environ["GDAL_DATA"] = f"{VORTEX_HOME}\\bin\\gdal\\gdal-data"
os.environ["PROJ_LIB"] = f"{VORTEX_HOME}\\bin\\gdal\\projlib"
os.environ["CLASSPATH"] = r"C:\Users\gaurav.fouzdar\Downloads\jython-standalone-2.7.2.jar;" + f"{VORTEX_HOME}\\lib\\*"

# Specify the location for the batch file and Python script
script_directory = r"E:\New folder_3"  # Update this path accordingly
batch_file_path = os.path.join(script_directory, "run_script.bat")
python_script_path = os.path.join(script_directory, "dss_run.py")

# Create or overwrite the batch file
with open(batch_file_path, 'w') as batch_file:
    batch_file.write(f'@echo off\n')
    batch_file.write(f'set "VORTEX_HOME={VORTEX_HOME}"\n')
    batch_file.write(f'set "PATH=%VORTEX_HOME%\\bin;%VORTEX_HOME%\\bin\\gdal;%PATH%"\n')
    batch_file.write(f'set "GDAL_DATA=%VORTEX_HOME%\\bin\\gdal\\gdal-data"\n')
    batch_file.write(f'set "PROJ_LIB=%VORTEX_HOME%\\bin\\gdal\\projlib"\n')
    batch_file.write(f'set "CLASSPATH=C:\\Users\\gaurav.fouzdar\\Downloads\\jython-standalone-2.7.2.jar;%VORTEX_HOME%\\lib\\*"\n')
    batch_file.write(f'%VORTEX_HOME%\\jre\\bin\\java.exe -Xmx2g -Djava.library.path=%VORTEX_HOME%\\bin;%VORTEX_HOME%\\bin\\gdal org.python.util.jython dss_run.py\n')
print(f'Batch file created or overwritten at {batch_file_path}')

# Create or overwrite the Python script
with open(python_script_path, 'w') as python_file:
    python_file.write('''
from mil.army.usace.hec.vortex.io import BatchImporter
from mil.army.usace.hec.vortex.geo import WktFactory

# File paths
in_files = ['D:/NIle Files/Rainfall_nc/BN_Beles_clipped.nc']
variables = ['precip']
clip_shp = 'D:/NIle Files/Blue Nile/Blue nile subbasin files/Blue Nile/BN_Beles/BN_Beles.shp'
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

# Build the importer
myImport = BatchImporter.builder() \
    .inFiles(in_files) \
    .variables(variables) \
    .geoOptions(geo_options) \
    .destination(destination) \
    .writeOptions(write_options) \
    .build()

# Process the import
myImport.process()
''')  # Replace with your actual script content
print(f'Python script created or overwritten at {python_script_path}')

# Function to run the batch process for Java execution
def run_batch_process():
    # Change directory to the location of the batch file
    os.chdir(script_directory)

    # Execute the batch file
    process = subprocess.Popen(batch_file_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Print the output and errors (if any)
    print(stdout.decode())
    if stderr:
        print("Error:", stderr.decode())

# Run the batch process
if __name__ == "__main__":
    run_batch_process()
