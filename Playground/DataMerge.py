import pandas as pd
import os

# Define the directory path
directory_path = r"C:\Users\ShaneKim\Desktop\Oracle\Playground\Index_Feature_Data"

# Check if the directory exists
if os.path.exists(directory_path):
    files = os.listdir(directory_path)
    merged_df = pd.DataFrame()
    for file in files:
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(directory_path, file))
            if merged_df.empty:
                merged_df = df
            else:
                merged_df = pd.merge(merged_df, df, on='Date', how='outer')
    # Sort the dataframe by date
    merged_df = merged_df.sort_values(by='Date')

    # Specify the output file path
    output_file_path = r"C:\Users\ShaneKim\Desktop\Oracle\Playground\merged_data.csv"

    # Save the merged dataframe to a CSV file
    merged_df.to_csv(output_file_path, index=False)
    print(f"Data has been merged and saved to {output_file_path}")
else:
    print("Directory not found")
