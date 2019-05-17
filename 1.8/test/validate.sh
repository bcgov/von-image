#!/bin/sh

cd $HOME

if ! python -c "from indy import crypto, did, pairwise, wallet"; then
    echo "Importing indy module failed"
fi
