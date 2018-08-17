import json
import sys

if len(sys.argv) < 1:
    raise 'Missing genesis transaction path'
path = sys.argv[1]

lc = 0
with open(path) as genesis:
    for line in genesis:
        txn = json.loads(line)
        assert 'txn' in txn
        lc += 1

assert lc == 4
