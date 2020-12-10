#!/bin/sh

cd $HOME

if ! python -c "from indy import crypto, did, pairwise, wallet"; then
    echo "Importing indy module failed"
fi

if ! python -c "__import__('aries_askar').bindings.get_library()"; then
    echo "Importing aries_askar module failed"
fi

if ! python -c "__import__('indy_credx').bindings.get_library()"; then
    echo "Importing indy_credx module failed"
fi

if ! python -c "__import__('indy_vdr').bindings.get_library()"; then
    echo "Importing indy_vdr module failed"
fi
