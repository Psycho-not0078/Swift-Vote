#!/bin/bash

if [ ! -d /.ethereum/keystore ]; then
    echo "/.ethereum/keystore not found, running 'geth init'..."
    geth init /files/genesis.json
    echo "...done!"
fi
sleep 10 
geth --datadir=/.ethereum/devchain --networkid 4444 --http --http.addr 0.0.0.0 --http.corsdomain "*" --http.api "admin,debug,web3,eth,txpool,personal,ethash,miner,net" --allow-insecure-unlock