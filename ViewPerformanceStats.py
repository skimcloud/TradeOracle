import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tkinter import Tk, Frame, Label, Scrollbar, Listbox

# Read the CSV file
data = pd.read_csv('raw_orders_2023.csv')

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
    exit_prices = [float(exit_price) for exit_price in exit_prices if pd.notnull(exit_price)]  # Convert exit prices to float
    exits[trade_key] = sum(exit_prices) / len(exit_prices) if len(exit_prices) > 0 else None  # Mark as None if no exit

# Calculate instantaneous profitable trade rate over time and profit over time
instantaneous_win_rates = []
profit_over_time = []
total_trades = 0
total_profit = 0
for _, in_order in in_orders.iterrows():
    trade_key = (
        in_order['trader'],
        in_order['ticker'],
        in_order['expiration'],
        in_order['contract_details']
    )
    three_months_ago = datetime.now() - timedelta(days=90)  # 3 months ago
    execution_datetime = pd.to_datetime(in_order['order_execution_datetime'])
    if trade_key in exits:
        entry_price = float(in_order['contract_price'])  # Convert entry price to float
        exit_price = exits[trade_key]
        is_profitable = exit_price is not None and exit_price > entry_price
        instantaneous_win_rates.append((pd.to_datetime(in_order['order_execution_datetime']), is_profitable))

        if is_profitable:
            total_profit += exit_price - entry_price  # Calculate profit
        else:
            total_profit -= (entry_price * 0.8)  # Apply 80% stop loss on losing positions
        profit_over_time.append((execution_datetime, total_profit))  # Update profit over time
        total_trades += 1
    elif execution_datetime < three_months_ago:
        is_profitable = False
        instantaneous_win_rates.append((pd.to_datetime(in_order['order_execution_datetime']), is_profitable))

# Calculate consecutive wins
consecutive_wins = 0
max_consecutive_wins = 0
for _, is_win in instantaneous_win_rates:
    if is_win:
        consecutive_wins += 1
        max_consecutive_wins = max(max_consecutive_wins, consecutive_wins)
    else:
        consecutive_wins = 0

# Calculate the average number of consecutive wins
average_consecutive_wins = max_consecutive_wins / len(instantaneous_win_rates) if len(instantaneous_win_rates) > 0 else 0
print(f"Average number of consecutive wins: {average_consecutive_wins:.2f}")

# Sort trades by datetime
instantaneous_win_rates.sort(key=lambda x: x[0])
profit_over_time.sort(key=lambda x: x[0])

# Calculate cumulative profitable trade rate over time
dates, rates = zip(*instantaneous_win_rates)
cumulative_rates = [sum(rates[:i + 1]) / (i + 1) for i in range(len(rates))]

# Calculate the average return per winning trade
average_return_per_winning_trade = total_profit / total_trades if total_trades > 0 else 0
print(f"Average return per winning trade: {average_return_per_winning_trade * 100:.2f}%")

# Calculate cumulative profit over time
dates_profit, profits = zip(*profit_over_time)

# Split the data into three segments
total_length = len(instantaneous_win_rates)
last_third_start = total_length // 3 * 2
last_two_thirds_start = total_length // 3

# Plotting for entire dataset
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(dates, cumulative_rates, color='blue')
ax1.set_xlabel('Time')
ax1.set_ylabel('Profitability Ratio', color='blue')
ax1.tick_params('y', colors='blue')
ax1.set_title('Profitability Ratio and Cumulative Profit Over Time - 2023')
ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
ax1.xaxis.set_minor_locator(plt.MaxNLocator(50))

ax2 = ax1.twinx()
ax2.plot(dates_profit, profits, color='red')
ax2.set_ylabel('Cumulative Profit', color='red')
ax2.tick_params('y', colors='red')

plt.tight_layout()
plt.show()


# Create a list to store order details
order_details = []

# Populate the list with order details
for _, in_order in in_orders.iterrows():
    trade_key = (
        in_order['trader'],
        in_order['ticker'],
        in_order['expiration'],
        in_order['contract_details']
    )
    three_months_ago = datetime.now() - timedelta(days=60)  # 3 months ago
    execution_datetime = pd.to_datetime(in_order['order_execution_datetime'])
    if trade_key in exits or execution_datetime < three_months_ago:
        entry_price = float(in_order['contract_price'])  # Convert entry price to float
        exit_price = exits.get(trade_key)
        if exit_price is not None:
            is_profitable = exit_price > entry_price
        else:
            is_profitable = False
        order_details.append((execution_datetime, is_profitable, entry_price, exit_price))

# Sort order details by datetime
order_details.sort(key=lambda x: x[0])

# Create a tkinter window
root = Tk()
root.title("List of Orders")

# Create a frame and a scrollbar
frame = Frame(root)
frame.pack(fill='both', expand=True)

scrollbar = Scrollbar(frame, orient='vertical')
scrollbar.pack(side='right', fill='y')

# Create a listbox
listbox = Listbox(frame, yscrollcommand=scrollbar.set)
listbox.pack(fill='both', expand=True)

# Configure scrollbar
scrollbar.config(command=listbox.yview)

# Function to color orders based on profitability
def color_order(is_profitable):
    return 'green' if is_profitable else 'red'

# Populate the listbox with orders
for order in order_details:
    execution_date = order[0].strftime('%Y-%m-%d %H:%M:%S')
    is_profitable = order[1]
    entry_price = order[2]
    exit_price = order[3] if order[3] is not None else "No exit"

    color = color_order(is_profitable)
    listbox.insert('end', f"Date: {execution_date}, Entry Price: {entry_price}, Exit Price: {exit_price}")
    listbox.itemconfig('end', {'bg': color, 'fg': 'white'})  # Set background color for the row

root.mainloop()