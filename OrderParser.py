from datetime import datetime
import csv
import re
from decimal import Decimal

def extract_trades(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    trade_blocks = text.split('@everyone')
    
    with open(output_file, 'w') as output:
        for block in trade_blocks:
            lines = block.split('\n')  # Split each block into lines
            for line in lines:
                output.write(line + '\n')  # Write each line to the output file

#extract_trades('data.txt', 'output_lines.txt')


def truncate_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Process each line to truncate after 'BBS-TRADE-BOT BOT'
    truncated_lines = []
    for line in lines:
        index = line.find('BBS-TRADE-BOT BOT')
        if index != -1:
            truncated_lines.append(line[:index])
        else:
            truncated_lines.append(line)

    # Write the truncated content back to the file
    with open(output_file, 'w') as file:
        for line in truncated_lines:
            file.write(line)

# Example usage:
# truncate_file('output_lines.txt', 'output_processed.txt')

# Function to extract order_execution_datetime column from a CSV file
def extract_order_execution_datetime(file_path):
    order_execution_datetime = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            order_execution_datetime.append(row['order_execution_datetime'])
    return order_execution_datetime

# File paths for the modified and output CSV files
modified_file_path = 'maria_orders_processed.csv'
output_file_path = 'output.csv'

# Extract 'order_execution_datetime' columns from both CSV files
modified_order_execution_datetime = extract_order_execution_datetime(modified_file_path)
output_order_execution_datetime = extract_order_execution_datetime(output_file_path)

# Check if the columns are the same
if modified_order_execution_datetime == output_order_execution_datetime:
    print("The 'order_execution_datetime' columns in modified_output.csv and maria_orders_processed.csv are the same.")
else:
    print("The 'order_execution_datetime' columns in modified_output.csv and maria_orders_processed.csv are different.")
