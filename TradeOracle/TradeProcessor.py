import pandas as pd
from datetime import datetime, timedelta

INPUT_DIRECTORY = 'raw_trade_data.csv'
OUTPUT_DIRECTORY = 'processed_trade_data.csv'

# Define a function to check if the contract has expired
def has_contract_expired(expiration_date, current_date):
    expiration_date = datetime.strptime(expiration_date, '%m/%d')
    current_date = datetime.strptime(current_date, '%m/%d')
    return current_date > expiration_date

def match_entries(csv_path):
    # Read the CSV file
    data = pd.read_csv(csv_path)

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

    # Calculate average exit price for each trade and determine success
    for trade_key, exit_prices in exits.items():
        # Convert exit prices to float
        exit_prices = [float(exit_price) for exit_price in exit_prices]

        # Determine if the trade is successful
        if len(exit_prices) > 0:
            success = True
        else:
            # Check if the contract has expired
            expiration_date = trade_key[2]
            current_date = datetime.today().strftime('%m/%d/%y')
            success = not has_contract_expired(expiration_date, current_date)

        # Update the exits dictionary with the success status
        exits[trade_key] = {
            'average_exit_price': sum(exit_prices) / len(exit_prices) if len(exit_prices) > 0 else None,
            'success': success
        }

    # Add the success status to the in_orders DataFrame and ensure correct dtype
    in_orders['success'] = False  # Initialize column with default value and correct dtype
    for idx, in_order in in_orders.iterrows():
        trade_key = (
            in_order['trader'],
            in_order['ticker'],
            in_order['expiration'],
            in_order['contract_details']
        )
        in_orders.at[idx, 'success'] = exits.get(trade_key, {}).get('success', False)

    return in_orders

matched_entries = match_entries(INPUT_DIRECTORY)
matched_entries.to_csv(OUTPUT_DIRECTORY, index=False)