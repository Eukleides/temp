from grid_sim.run_batch import Grid
NUM_NODES = 128
NUM_TRADES = 100000

g = Grid(NUM_NODES, NUM_TRADES)

# run the original batch
# g.check_batch(verbose=True)
# max_time = g.run_batch(bname='batches.json', verbose=True)

# create trivial batches, one per 1000 trades
tid = 0
f = open('calc_times.txt', 'w')

while tid<NUM_TRADES:
    batch_id = f'b_{tid}'
    bname = f'b\{batch_id}.json'

    g.create_batch(bname=bname, uitids=[tid])
    max_time = g.run_batch(bname=bname, verbose=False)

    f.write(f'Trade: {tid} Time: {max_time:,.0f}\n')
    tid += 1

f.close()