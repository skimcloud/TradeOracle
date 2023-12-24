import pandas as pd
from datetime import datetime

# Function to convert date strings to a common format
def convert_date(date_str, has_time):
    if has_time:
        # Convert from 'MM/DD/YYYY HH:MM AM/PM' to 'YYYY-MM-DD'
        return datetime.strptime(date_str, '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%d')
    else:
        # Already in 'YYYY-MM-DD' format
        return date_str

# Read the two CSV files
file_path1 = r'C:\Users\ShaneKim\Desktop\Oracle\Playground\merged_index.csv'
file_path2 = r'C:\Users\ShaneKim\Desktop\Oracle\Playground\entries_matched.csv'

df1 = pd.read_csv(file_path1)
df2 = pd.read_csv(file_path2)

# Apply conversion to the 'Date' column of df1 and 'order_execution_datetime' of df2
df1['Date'] = df1['Date'].apply(lambda x: convert_date(x, False))
df2['order_execution_datetime'] = pd.to_datetime(df2['order_execution_datetime'].apply(lambda x: convert_date(x, True)))

# Adjusting the date in df2 to be one day ahead for the merge
df2['Adjusted Date'] = (df2['order_execution_datetime'] - pd.Timedelta(days=1)).dt.strftime('%Y-%m-%d')

# Merge the dataframes with the adjusted date
merged_df_adjusted = pd.merge(df2, df1, left_on='Adjusted Date', right_on='Date')
merged_df_adjusted_dropped = merged_df_adjusted.drop(columns=['Date', 'Adjusted Date', 'trader', 'direction'])


# Saving the adjusted merged DataFrame to a new CSV file
dir = r'Playground\entries_lagged_index_data.csv'
merged_df_adjusted_dropped.to_csv(dir, index=False)