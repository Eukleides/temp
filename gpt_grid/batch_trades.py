import csv

def calculate_trade_batches(trades, num_nodes):
    # Sort trades in descending order based on their calculation time
    trades.sort(key=lambda x: x[1], reverse=True)

    # Initialize an array to track the remaining capacity of each node
    node_capacity = [0] * num_nodes

    # Initialize an array to store the assigned batches for each trade
    trade_batches = [-1] * len(trades)

    # Assign trades to batches
    for trade_id, trade_time in trades:
        # Find the node with the minimum remaining capacity
        min_capacity_node = min(range(num_nodes), key=lambda x: node_capacity[x])

        # Assign the trade to the selected node
        trade_batches[trade_id] = min_capacity_node

        # Update the remaining capacity of the selected node
        node_capacity[min_capacity_node] += trade_time

    return trade_batches

# Read trade times from the CSV file
trades = []
with open('results\\trade_times.csv', 'r') as file:
    csv_reader = csv.reader(file)
    # next(csv_reader)  # Skip header
    for row in csv_reader:
        trade_id, trade_time = int(row[1]), int(row[3])
        trades.append((trade_id, trade_time))

# Define the number of nodes
num_nodes = 128

# Calculate trade batches
trade_batches = calculate_trade_batches(trades, num_nodes)

# Print the assigned batches for each trade
for trade_id, batch_id in enumerate(trade_batches):
    print(f"Trade {trade_id}: Batch {batch_id}")
