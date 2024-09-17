from pydsstools.heclib.dss import HecDss
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

dss_file = r"D:\Nile project\Blue Nile\Blue _nile _Hec_Hms_model\BN_Blue_Nile_at_Khartoum_and_soba\Run_1.dss"
pathname = "//SINK-1/FLOW/31Dec1980 - 30Dec2018/1DAY/RUN:RUN 1/"
startDate = "31DEC1980 24:00:00"
endDate = "31DEC1982 24:00:00"

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

# Create Excel file
excel_file = 'Mongalla.xlsx'
monthly_avg.to_excel(excel_file, index=False)

print(f"Excel file '{excel_file}' has been created with monthly average values.")

# Optional: Plot the monthly average values
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg['Date'], monthly_avg['Mean Monthly Value'], 'o-')
plt.title('Monthly Average Values')
plt.xlabel('Date')
plt.ylabel('Mean Monthly Value')
plt.grid(True)
plt.show()


