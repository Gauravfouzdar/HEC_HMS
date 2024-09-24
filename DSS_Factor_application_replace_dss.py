from pydsstools.heclib.dss import HecDss
from pydsstools.core import TimeSeriesContainer
import pandas as pd
import matplotlib.pyplot as plt

def process_dss_data(input_dss, pathname, start_date, end_date, monthly_factors):
    # Open the input DSS file and read the data
    try:
        with HecDss.Open(input_dss) as fid:
            ts = fid.read_ts(pathname, window=(start_date, end_date), trim_missing=True)
    except Exception as e:
        print(f"Error reading DSS file: {e}")
        return

    # Check if we got any data
    if ts is None:
        print(f"No data found for pathname: {pathname}")
        return

    # Print information about the time series
    print(f"Time series info:")
    print(f"  Start date: {ts.startDateTime}")
    print(f"  Number of values: {ts.numberValues}")
    print(f"  Units: {ts.units}")
    print(f"  Type: {ts.type}")
    print(f"  Interval: {ts.interval}")

    # Convert to pandas DataFrame
    df = pd.DataFrame({'Date': ts.pytimes, 'Original Value': ts.values})
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[~ts.nodata]  # Remove rows with missing data

    if df.empty:
        print("No valid data after removing missing values")
        return

    df.set_index('Date', inplace=True)
    
    # Apply monthly factors and calculate adjusted values
    df['Month'] = df.index.month
    df['Adjusted Value'] = df.apply(lambda row: row['Original Value'] * monthly_factors.get(row['Month'], 1), axis=1)
    
    # Plotting the impact before and after adjustment
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Original Value'], label='Original Data', color='blue')
    plt.plot(df.index, df['Adjusted Value'], label='Adjusted Data', color='red', linestyle='--')
    
    # Formatting the plot
    plt.title('Impact of Monthly Factors on Time Series Data')
    plt.xlabel('Date')
    plt.ylabel(f"Value ({ts.units})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

    # Prepare the new time series for writing
    new_ts = TimeSeriesContainer()
    new_ts.pathname = pathname
    new_ts.startDateTime = df.index[0].strftime("%d%b%Y %H:%M:%S")
    new_ts.numberValues = len(df)
    new_ts.units = ts.units
    new_ts.type = ts.type
    new_ts.interval = ts.interval
    new_ts.values = df['Adjusted Value'].tolist()
    
    # Write back to the same DSS file
    try:
        with HecDss.Open(input_dss, mode="w") as fid:
            fid.put_ts(new_ts)
        print(f"Data processed and written to {input_dss}")
    except Exception as e:
        print(f"Error writing to DSS file: {e}")

# Example usage
input_dss = r"D:\Nile project\Lake Victoria\01 HEC HMS models\Lake_Victoria\Run_2.dss"
pathname = "//SINK-1/FLOW/31Dec1980 - 31Dec1982/1DAY/RUN:RUN 2/"
start_date = "31DEC1980 24:00:00"
end_date = "31DEC2010 24:00:00"

# Define monthly factors (adjust as needed)
monthly_factors = {
    1:0.93875,
    2:0.954543648,
    3:1.098681006,
    4:0.787622788,
    5:0.682171875,
    6:0.72791601,
    7:0.725327296,
    8:0.7569918,
    10:0.8127638,
    11:0.789964259,
    12:0.656811835
}

process_dss_data(input_dss, pathname, start_date, end_date, monthly_factors)




