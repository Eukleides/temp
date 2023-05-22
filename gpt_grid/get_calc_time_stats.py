from grid_sim.run_batch import Grid
NUM_NODES = 64
NUM_TRADES = 100000

g = Grid(NUM_NODES, NUM_TRADES)

# run the original batch
g.check_batch(fname='batch_selection3.json', verbose=True)
exit(0)

# max_time = g.run_batch(bname='batches.json', verbose=True)


# This loop calculates the time to run each trade individually
# f = open('calc_times.txt', 'w')
# tid = 0
# while tid<NUM_TRADES:
#     batch_id = f'b_{tid}'
#     bname = f'b\{batch_id}.json'
#
#     g.create_batch(bname=bname, uitids=[tid])
#     max_time = g.run_batch(bname=bname, verbose=False)
#
#     f.write(f'Trade: {tid} Time: {max_time:,.0f}\n')
#     tid += 1

# f = open('batch_calc_times.txt', 'w')
# node_id = 0
# while node_id<NUM_NODES:
#     bname = f'batches_{node_id}.json'
#
#     max_time = g.run_batch(bname=bname, verbose=False)
#
#     f.write(f'Batch: {node_id} Time: {max_time:,.0f}\n')
#     node_id += 1
#
# f.close()

