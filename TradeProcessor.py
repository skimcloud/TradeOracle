import pandas as pd
from datetime import datetime

# Constants
INPUT_DIRECTORY = 'raw_trade_data.csv'
CLOSED_OUTPUT_DIRECTORY = 'processed_trade_data.csv'
OPEN_OUTPUT_DIRECTORY = 'open_trades.csv'

def process_trades(input_file, closed_output_file, open_output_file):
    # Load the raw trade data
    raw_trade_data = pd.read_csv(input_file)

    # Process 'contract_details' to remove the 'C' value after the contract strike
    raw_trade_data['contract_details'] = raw_trade_data['contract_details'].str.replace('C', '')

    # Prepare the dataframes for the output files
    closed_trades = pd.DataFrame(columns=['order_execution_datetime', 'trader', 'ticker', 'expiration', 
                                          'contract_details', 'entry_price', 'exit_price', 'profit', 'success'])
    open_trades = pd.DataFrame(columns=['order_execution_datetime', 'trader', 'ticker', 'expiration', 
                                        'contract_details', 'contract_price', 'timeframe', 'comment'])

    # Loop through the data
    for index, row in raw_trade_data.iterrows():
        if row['direction'] == 'IN':
            # Find the corresponding 'OUT' entries
            exit_rows = raw_trade_data[(raw_trade_data['ticker'] == row['ticker']) &
                                       (raw_trade_data['contract_details'] == row['contract_details']) &
                                       (raw_trade_data['expiration'] == row['expiration']) &
                                       (raw_trade_data['direction'] == 'OUT')]

            if not exit_rows.empty:
                # Calculate average exit price and profit
                average_exit_price = round(exit_rows['contract_price'].mean(), 2)
                profit = round(average_exit_price - row['contract_price'], 2)
                success = profit > 0

                # Add to closed_trades dataframe
                new_row = pd.DataFrame([{
                    'order_execution_datetime': row['order_execution_datetime'],
                    'trader': row['trader'],
                    'ticker': row['ticker'],
                    'expiration': row['expiration'],
                    'contract_details': row['contract_details'],
                    'entry_price': row['contract_price'],
                    'exit_price': average_exit_price,
                    'profit': profit,
                    'success': success
                }])
                closed_trades = pd.concat([closed_trades, new_row], ignore_index=True)
            else:
                # Check if the contract has expired
                expiration_date = datetime.strptime(row['expiration'], '%m/%d/%Y')
                if expiration_date > datetime.now():
                    # Trade is still open, add to open_trades dataframe
                    new_row = pd.DataFrame([row])
                    open_trades = pd.concat([open_trades, new_row], ignore_index=True)
                else:
                    # Contract expired, assume profit is negative of the entry price
                    profit = -row['contract_price']
                    success = False

                    # Add to closed_trades dataframe
                    new_row = pd.DataFrame([{
                        'order_execution_datetime': row['order_execution_datetime'],
                        'trader': row['trader'],
                        'ticker': row['ticker'],
                        'expiration': row['expiration'],
                        'contract_details': row['contract_details'],
                        'entry_price': row['contract_price'],
                        'exit_price': 0,
                        'profit': profit,
                        'success': success
                    }])
                    closed_trades = pd.concat([closed_trades, new_row], ignore_index=True)

    # Save the output files
    closed_trades.to_csv(closed_output_file, index=False)
    open_trades.to_csv(open_output_file, index=False)

# Run the process
process_trades(INPUT_DIRECTORY, CLOSED_OUTPUT_DIRECTORY, OPEN_OUTPUT_DIRECTORY)
