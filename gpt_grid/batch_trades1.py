"""
PROMPT 1 (to GPT-4)

We have a grid of 64 nodes and are trying to find out how to use it to calculate 100,000 trades in the shortest time.
The trades are to be grouped into batches.
Each batch will run on one node.
So if a batch contains 150 trades, they will all run one after another on the chosen node for that batch.
We need to find how to allocate which batch to run on each of the 64 nodes such that the overall calculation time is minimised.

Each trade takes a different time to calculate and its calculation time is shown in a table like the one below which is saved in the trades.csv file under the grid_sim directory:

Trade	Time
0	18
1	19
2	52
3	50
4	29
5	23
6	45
7	43
8	49
9	40


I would like you to advise me on the best way to use this table to determine how to group the trades into 64 batches such that the overall calculation time is minimised.

Can you suggest some python code to help me determine the best way to group the trades into batches?

Please save the result of the batch selection into a json file under the grid_sim directory.
The contents of the json file should be like:

[
  {
    "Uid": 0,
    "TradeUids": [100, 101]
  },
  {
    "Uid": 1,
    "TradeUids": [102, 103]
  }
]

where "Uid" is the batch number (from 0 to 63) and "TradeUids" are the trades within that batch.
"""
import pandas as pd
import json

# Read the trades.csv file
trades = pd.read_csv("grid_sim/trades.csv")

# Sort trades in descending order of calculation time
trades = trades.sort_values(by='Time', ascending=False)

# Initialize the batches
batches = [{'Uid': i, 'TradeUids': [], 'TotalTime': 0} for i in range(64)]

# Assign each trade to the batch with the least total calculation time so far
for index, row in trades.iterrows():
    # Find the batch with the least total calculation time
    min_batch = min(batches, key=lambda x: x['TotalTime'])

    # Add the trade to this batch
    min_batch['TradeUids'].append(int(row['Trade']))

    # Update the total calculation time of this batch
    min_batch['TotalTime'] += row['Time']

# Remove 'TotalTime' from batches as it's not needed in the output
for batch in batches:
    del batch['TotalTime']

# Save the batches to a JSON file
with open('grid_sim/batch_selection1.json', 'w') as f:
    json.dump(batches, f, indent=2)
