import subprocess
import os
import json

class Grid:
    def __init__(self, num_nodes, num_trades):
        self.num_nodes = num_nodes
        self.num_trades = num_trades
        self.set_path()

    def set_path(self):
        os.chdir('grid_sim')

    def check_batch(self, fname='batches.json', verbose=False):
        f = open(fname)
        data = json.load(f)

        uids = set()
        uitids = set()

        for node in data:
            uids.add(node['Uid'])

            for uid in node['TradeUids']:
                uitids.add(uid)

        assert len(uids) == self.num_nodes, 'Missing trades from batch'
        assert len(uitids) == self.num_trades, 'Missing trades from batch'

        if verbose:
            print('Batch check ok')

        return

    def create_batch(self, bname='batches1.json', uitids=[]):
        data = []

        for i in range(len(uitids)):
            json_item = {}
            json_item['Uid'] = i
            json_item['TradeUids'] = [uitids[i]]
            data.append(json_item)

        with open(bname, "w") as outfile:
            json.dump(data, outfile)

    def run_batch(self, bname='batches.json', verbose=False):
        cmd = "main.exe"
        res = subprocess.run([cmd, '-b', bname], capture_output=True)
        txt = str(res.stdout)
        max_time = float(txt[txt.find('Max time'):].split(' ')[2])

        if verbose:
            print(f'Max time: {max_time}')

        return max_time