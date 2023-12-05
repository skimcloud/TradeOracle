import pandas as pd
from datetime import datetime, timedelta

# Read the CSV file
data = pd.read_csv('maria_orders_processed.csv')

# Filter IN orders
in_orders = data[data['direction'] == 'IN'].copy()  # Create a copy of the filtered data

# Create a dictionary to store exits for each trade
exits = {}

# Match exits to corresponding entries
for _, out_order in data[data['direction'] == 'OUT'].iterrows():
    trade_key = (
        out_order['trader'],
        out_order['ticker'],
        out_order['expiration'],
        out_order['contract_details']
    )
    if trade_key not in exits:
        exits[trade_key] = []
    exits[trade_key].append(out_order['contract_price'])

# Calculate average exit price for each trade
for trade_key, exit_prices in exits.items():
    exit_prices = [float(exit_price) for exit_price in exit_prices]  # Convert exit prices to float
    exits[trade_key] = sum(exit_prices) / len(exit_prices) if len(exit_prices) > 0 else None  # Mark as None if no exit

# Add 'success' column to the 'IN' orders
success_list = []
for _, in_order in in_orders.iterrows():
    trade_key = (
        in_order['trader'],
        in_order['ticker'],
        in_order['expiration'],
        in_order['contract_details']
    )
    if trade_key in exits:
        entry_price = float(in_order['contract_price'])  # Convert entry price to float
        exit_price = exits[trade_key]
        is_profitable = exit_price is not None and exit_price > entry_price
        success_list.append(1 if is_profitable else 0)
    else:
        success_list.append(0)

# Add the 'success' column to the 'IN' orders dataframe
in_orders['success'] = success_list

# Save the new version of the CSV file with only 'IN' orders and the 'success' column
in_orders.to_csv('new_maria_orders_processed.csv', index=False)
