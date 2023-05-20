import csv
import matplotlib.pyplot as plt

def calculate_batch(trades, num_batches):
    # Sort the trades in descending order based on their calculation time
    sorted_trades = sorted(trades, key=lambda x: x[1], reverse=True)

    # Initialize an empty list of batches
    batches = [[] for _ in range(num_batches)]

    # Assign each trade to the batch with the shortest total processing time
    for trade in sorted_trades:
        min_batch = min(batches, key=lambda batch: sum(trade[1] for trade in batch))
        min_batch.append(trade)

    return batches

# Read the trade data from the CSV file
trades = []
with open('trades.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        trade_id, time = int(row[0]), int(row[1])
        trades.append((trade_id, time))

# Define the number of batches (nodes)
num_batches = 128

# Calculate the batches using the Largest Processing Time algorithm
batches = calculate_batch(trades, num_batches)

# Save the results in a CSV file
with open('batches.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Batch', 'Trade', 'Time'])
    for i, batch in enumerate(batches):
        total_time = sum(trade[1] for trade in batch)
        for trade in batch:
            writer.writerow([i, trade[0], trade[1]])
        writer.writerow(['', 'Total Calculation Time', total_time])
        writer.writerow([])  # Empty line between batches

# Plot the total calculation time against the batch number
batch_numbers = []
total_times = []
for i, batch in enumerate(batches):
    batch_numbers.append(i)
    total_time = sum(trade[1] for trade in batch)
    total_times.append(total_time)

plt.plot(batch_numbers, total_times)
plt.xlabel('Batch Number')
plt.ylabel('Total Calculation Time')
plt.title('Total Calculation Time vs. Batch Number')
plt.show()