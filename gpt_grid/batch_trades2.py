"""
PROMPT 2 (to GPT-4)

Each trade depends on a number of MarketKeys being calculated first.
Each MarketKey may depend on other MarketKeys being calculated first.

The total time to calculate a trade is the sum of the trades's own calculation time plus the sum of all the calculation times of the MarketKeys the trade depends on (unless those keys have already been calculated within that batch).

If two or more trades within the same batch depend on the same MarketKey, then that key only needs to be calculated once for the first trade that requires it.

Subsequent trades that depend on the same MarketKey can use it without having to wait for it to be calculated again. This will reduce the calculation time of these trades.


The file trades.json contains the set of MarketKeys each trade depends on.
For example, trades.json contains information like:
 {
    "Uid": 100,
    "CalcSec": 4,
    "MarketKeys": [
      388,
      449
    ]
  }
which says that trade with Uid 100 takes 4 ms to calculate and depends on keys 338 and 449 to be calculated first.

The file marketkeys.json contains the set of MarketKeys each MarketKey depends on.
For example, marketkeys.json contains information like:
{
    "Uid": 10,
    "Dependencies": [
      6,
      7
    ],
    "CalcSec": 3
  }
which says that MarketKey with Uid 10 takes 3 ms to calculate and depends on MarketKeys 6 and 7 to be calculated first.

I would like you to use this information to modify the python script that determines how to group the trades into 64 batches such that the overall calculation time is minimised.

Please save the batch results into a json file with the same format as before.
"""

import pandas as pd
import json


# Function to calculate the total time including dependencies
def calc_total_time(key, keys_dict, cache):
    # If the total time of this key has been calculated before, return it
    if key in cache:
        return cache[key]

    # Calculate the total time
    total_time = keys_dict[key]['CalcSec']
    for dep in keys_dict[key]['Dependencies']:
        total_time += calc_total_time(dep, keys_dict, cache)

    # Cache the total time of this key
    cache[key] = total_time
    return total_time


# Load the data
with open('grid_sim/trades.json') as f:
    trades = json.load(f)
with open('grid_sim/marketkeys.json') as f:
    market_keys = json.load(f)

# Convert the market keys list to a dictionary for faster access
market_keys_dict = {k['Uid']: k for k in market_keys}

# Calculate the total time for each trade
cache = {}
for trade in trades:
    trade['TotalTime'] = trade['CalcSec']
    for key in trade['MarketKeys']:
        trade['TotalTime'] += calc_total_time(key, market_keys_dict, cache)

# Sort trades in descending order of total time
trades.sort(key=lambda x: -x['TotalTime'])

# Initialize the batches
batches = [{'Uid': i, 'TradeUids': [], 'TotalTime': 0} for i in range(64)]

# Assign each trade to the batch with the least total calculation time so far
for trade in trades:
    # Find the batch with the least total calculation time
    min_batch = min(batches, key=lambda x: x['TotalTime'])

    # Add the trade to this batch
    min_batch['TradeUids'].append(trade['Uid'])

    # Update the total calculation time of this batch
    min_batch['TotalTime'] += trade['TotalTime']

# Remove 'TotalTime' from batches as it's not needed in the output
for batch in batches:
    del batch['TotalTime']

# Save the batches to a JSON file
with open('grid_sim/batch_selection2.json', 'w') as f:
    json.dump(batches, f, indent=2)
