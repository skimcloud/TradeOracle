import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Read the CSV file
data = pd.read_csv('maria_orders_processed.csv')

# Filter IN and OUT orders separately
in_orders = data[data['direction'] == 'IN']
out_orders = data[data['direction'] == 'OUT']

# Create a dictionary to store exits for each trade
exits = {}

# Match exits to corresponding entries
for _, out_order in out_orders.iterrows():
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

# Calculate instantaneous profitable trade rate over time
instantaneous_win_rates = []
for _, in_order in in_orders.iterrows():
    trade_key = (
        in_order['trader'],
        in_order['ticker'],
        in_order['expiration'],
        in_order['contract_details']
    )
    six_months_ago = datetime.now() - timedelta(days=90)  # 6 months ago
    execution_datetime = pd.to_datetime(in_order['order_execution_datetime'])
    if trade_key in exits:
        entry_price = float(in_order['contract_price'])  # Convert entry price to float
        exit_price = exits[trade_key]
        is_profitable = exit_price is not None and exit_price > entry_price
        instantaneous_win_rates.append((pd.to_datetime(in_order['order_execution_datetime']), is_profitable))
    elif execution_datetime < six_months_ago:
        print(trade_key)
        is_profitable = False
        instantaneous_win_rates.append((pd.to_datetime(in_order['order_execution_datetime']), is_profitable))



# Sort trades by datetime
instantaneous_win_rates.sort(key=lambda x: x[0])

# Calculate cumulative profitable trade rate over time
dates, rates = zip(*instantaneous_win_rates)
cumulative_rates = [sum(rates[:i + 1]) / (i + 1) for i in range(len(rates))]

# Calculate the current profitability ratio
current_profit_ratio = cumulative_rates[-1]

# Print the current profitability ratio
print("Current Profitability Ratio:", current_profit_ratio)

# Plotting the cumulative profitable trade rate over time
plt.figure(figsize=(10, 6))
plt.plot(dates, cumulative_rates)
plt.xlabel('Time')
plt.ylabel('Profitability Ratio (Considering Expirations)')
plt.title('MariaC82\'s Profitability Ratio Over Time')
plt.xticks(rotation=45)
plt.yticks([i/100 for i in range(0, 101, 5)])  # Adjust range and step size as needed (100 for 1.0)
# Adding more ticks to the x-axis (adjust frequency as needed)
plt.xticks(pd.date_range(min(dates), max(dates), freq='1M'), rotation=45)  # For example, every 2 weeks]
plt.tight_layout()
plt.show()