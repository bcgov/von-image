#!/bin/sh


### Checks for von-network ###

cd $HOME

# generate a transaction file
generate_indy_pool_transactions --nodes 4 --clients 0 > /dev/null
if [ $? -ne 0 ]; then
    echo 'Generation of transactions file failed'
    exit 1
fi

if ! python test/check_txn.py .indy-cli/networks/sandbox/pool_transactions_genesis; then
    echo 'Genesis transaction file failed validation'
    exit 1
fi


### Run tests for von-agent ###

if ! python test/check_agent.py; then
    echo 'von_agent import test failed'
    exit 1
fi


### Run tests for didauth ###

git clone https://github.com/PSPC-SPAC-buyandsell/didauth.git
cd didauth
git checkout v1.0
pytest
