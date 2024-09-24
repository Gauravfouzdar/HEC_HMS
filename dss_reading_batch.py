from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import pandas as pd
import os

# Set start and end date for time window
startDate = "31DEC1980 24:00:00"
endDate = "31DEC1982 24:00:00"
# Path to the CSV file containing project directory, compute name, and outlet name
csv_file = r"C:\Users\gaurav.fouzdar\Desktop\links and data.csv"

# Read the CSV file into a DataFrame
df_csv = pd.read_csv(csv_file)

def generate_dss_file_list(df):
    dss_files = []
    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        project_directory = row['Project directory']
        compute_name = row['compute Name']
        compute_name_dss= row['Compute_name_dss']
        
        # Generate the .dss file path
        dss_file_path = os.path.join(project_directory, f"{compute_name_dss}.dss")
        dss_files.append(dss_file_path)  # No need for raw string notation here
    
    return dss_files

# Generate the formatted list of .dss file paths
dss_file_list = generate_dss_file_list(df_csv)

print(dss_file_list)

def generate_pathnames(df):
    pathnames = []
    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        outlet_name = row['outlet name']  # The outlet name (e.g., "SINK-1" or "J6")
        compute_name = row['compute Name']  # The compute name (e.g., "Run 1" or "Run 2")
        
        # Generate the pathname string
        pathname = f"//{outlet_name}/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:{compute_name}/"
        pathnames.append(pathname)
    
    return pathnames

# Generate the list of pathnames
pathname_list = generate_pathnames(df_csv)

# Define the Excel file that will store multiple sheets
excel_file = 'Model.xlsx'

# Create an ExcelWriter object using openpyxl (default engine)
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    # Loop through each DSS file and pathname
    for dss_file, pathname in zip(dss_file_list, pathname_list):
        # Extract the second-to-last folder name from the DSS file path for the sheet name
        sheet_name = os.path.basename(os.path.dirname(dss_file))

        # Ensure the sheet name is <= 31 characters
        if len(sheet_name) > 31:
            sheet_name = sheet_name[:31]

        try:
            # Open the DSS file and read the time series
            with HecDss.Open(dss_file) as fid:
                ts = fid.read_ts(pathname, window=(startDate, endDate), trim_missing=True)

            # Convert to pandas DataFrame
            df = pd.DataFrame({'Date': ts.pytimes, 'Value': ts.values})
            df['Date'] = pd.to_datetime(df['Date'])
            df = df[~ts.nodata]  # Remove rows with missing data

            # Set Date as index
            df.set_index('Date', inplace=True)

            # Resample to monthly average
            monthly_avg = df.resample('M').mean()

            # Reset index and set date to 1st of each month
            monthly_avg.reset_index(inplace=True)
            monthly_avg['Date'] = monthly_avg['Date'].apply(lambda x: x.replace(day=1))

            # Rename columns
            monthly_avg.columns = ['Date', 'Mean Monthly Value']

            # Write the monthly average DataFrame to a new sheet in the Excel file
            monthly_avg.to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"Data for {sheet_name} written to Excel file '{excel_file}'.")

            # Optional: Plot the monthly average values
            plt.figure(figsize=(12, 6))
            plt.plot(monthly_avg['Date'], monthly_avg['Mean Monthly Value'], 'o-')
            plt.title(f'Monthly Average Values - {sheet_name}')
            plt.xlabel('Date')
            plt.ylabel('Mean Monthly Value')
            plt.grid(True)
            plt.show()

        except Exception as e:
            print(f"Error processing {dss_file} for {sheet_name}: {e}")

print(f"Excel file '{excel_file}' has been created with multiple sheets.")
