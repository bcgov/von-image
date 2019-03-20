#!/bin/sh


### Checks for von-network ###

cd $HOME

# generate a transaction file
generate_indy_pool_transactions --nodes 4 --clients 0 > /dev/null
if [ $? -ne 0 ]; then
    echo 'Generation of transactions file failed'
    exit 1
fi

if ! python test/check_txn.py ledger/sandbox/pool_transactions_genesis; then
    echo 'Genesis transaction file failed validation'
    exit 1
fi

if ! python -c "from indy import crypto, did, pairwise, wallet"; then
    echo "Importing indy module failed"
fi
