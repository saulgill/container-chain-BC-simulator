#!/bin/bash
geth --datadir="ethdata" --networkid 15 --nodiscover console --unlock 0xBDdA7Db745E56f7B0c01186C3932375d115A4183 --rpc --rpcport "8000" --rpcaddr "0.0.0.0" --rpccorsdomain "*" --rpcapi "eth,net,web3,miner,debug,personal,rpc" --allow-insecure-unlock
