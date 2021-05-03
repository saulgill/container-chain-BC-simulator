#!/bin/bash
rm -r /app/ethdata/geth
rm /app/ethdata/geth.ipc
geth --rpc --rpcport "8080" --datadir "/app/ethdata" init "/app/genesis.json"
geth --datadir="ethdata" --networkid 15 --bootnodes $(echo -n $(cat eth-scripts/node_join_id)) --rpc --rpcport "8000" --rpcaddr "0.0.0.0" --rpccorsdomain "*" --rpcapi "eth,net,web3,miner,debug,personal,rpc" --allow-insecure-unlock --syncmode 'full'
