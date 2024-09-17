from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

# List of DSS files and corresponding pathnames
dss_files = [
    r"D:\Nile project\Main Nile\Main_Nile_HECHMS_Model\MN_Assuit_Cario\Run_1.dss",
    r"D:\Nile project\Main Nile\Main_Nile_HECHMS_Model\MN_Wadi_Halfa_Aswan\Run_1.dss",
    r"D:\Nile project\Blue Nile\Blue _nile _Hec_Hms_model\BN_Blue_Nile_at_Khartoum_and_soba\Run_1.dss",
    r"D:\Nile project\white nile\white _nile _Hec_Hms_model\WN_Morgen_Khartoum\Run_1.dss",
    r"D:\Nile project\white nile\white _nile _Hec_Hms_model\WN_Malakal_Triangle_COP30\Run_1.dss",
    r"D:\Nile project\Lake Victoria\01 HEC HMS models\Lake_Victoria\Run_2.dss"
]

# List of corresponding pathnames for each DSS file
pathnames = [
    "//SINK-1/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:RUN 1/",
    "//SINK-1/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:RUN 1/",
    "//SINK-1/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:RUN 1/",
    "//SINK-1/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:RUN 1/",
    "//J6/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:RUN 1/",
    "//SINK-1/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:RUN 2/"
]

# Set start and end date for time window
startDate = "31DEC1980 24:00:00"
endDate = "31DEC1982 24:00:00"

# Define the Excel file that will store multiple sheets
excel_file = 'Model.xlsx'

# Create an ExcelWriter object using openpyxl (default engine)
with pd.ExcelWriter(excel_file) as writer:
    # Loop through each DSS file and pathname
    for dss_file, pathname in zip(dss_files, pathnames):
        # Extract the second-to-last folder name from the DSS file path for the sheet name
        sheet_name = os.path.basename(os.path.dirname(dss_file))

        # Ensure the sheet name is <= 31 characters
        if len(sheet_name) > 31:
            sheet_name = sheet_name[:31]

        # Open the DSS file and read the time series
        fid = HecDss.Open(dss_file)
        ts = fid.read_ts(pathname, window=(startDate, endDate), trim_missing=True)
        fid.close()

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

print(f"Excel file '{excel_file}' has been created with multiple sheets.")
