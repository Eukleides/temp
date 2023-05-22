"""
PROMPT 4 (to GPT-4)

The lines

    total_times = []
    for batch in batches:
        total_time = trade['CalcSec']
        for key in trade['MarketKeys']:
            total_time += calc_total_time(key, market_keys_dict, batch['CalculatedKeys'])
        total_times.append(total_time)

look wrong as they do not result in total_times being an array of all trades allocated to batches so far plus the additional trade we want to add.

Can you rewrite these lines please?

"""

import pandas as pd
import json


# Function to calculate the total time including dependencies
def calc_total_time(key, keys_dict, calculated_keys):
    # If this key has already been calculated, return 0
    if key in calculated_keys:
        return 0

    # Calculate the total time
    total_time = keys_dict[key]['CalcSec']
    for dep in keys_dict[key]['Dependencies']:
        total_time += calc_total_time(dep, keys_dict, calculated_keys)

    return total_time


# Load the data
with open('grid_sim/trades.json') as f:
    trades = json.load(f)
with open('grid_sim/marketkeys.json') as f:
    market_keys = json.load(f)

# Convert the market keys list to a dictionary for faster access
market_keys_dict = {k['Uid']: k for k in market_keys}

# Initialize the batches
batches = [{'Uid': i, 'TradeUids': [], 'TotalTime': 0, 'CalculatedKeys': set()} for i in range(64)]

# Sort trades in descending order of their own calculation time (excluding dependencies)
trades.sort(key=lambda x: -x['CalcSec'])

# Assign each trade to the batch with the least total calculation time so far
for trade in trades:
    # Calculate the total time for this trade including dependencies for each batch
    total_times = []
    for batch in batches:
        total_time = batch['TotalTime'] + trade['CalcSec']
        for key in trade['MarketKeys']:
            total_time += calc_total_time(key, market_keys_dict, batch['CalculatedKeys'])
        total_times.append(total_time)

    # Find the batch with the least total calculation time if this trade is assigned to it
    min_index = total_times.index(min(total_times))
    min_batch = batches[min_index]

    # Add the trade to this batch
    min_batch['TradeUids'].append(trade['Uid'])

    # Update the total calculation time and the calculated keys of this batch
    min_batch['TotalTime'] = total_times[min_index]
    min_batch['CalculatedKeys'].update(trade['MarketKeys'])

# Remove 'TotalTime' and 'CalculatedKeys' from batches as they're not needed in the output
for batch in batches:
    del batch['TotalTime']
    del batch['CalculatedKeys']

# Save the batches to a JSON file
with open('grid_sim/batch_selection4.json', 'w') as f:
    json.dump(batches, f, indent=2)
