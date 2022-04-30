/tmp/beacon --datadir /tmp/chaindata \
--force-clear-db --interop-genesis-state /tmp/genesis.ssz \
--interop-eth1data-votes --min-sync-peers=0 \
--http-web3provider=/home/saul/container-chain-BC-simulator/go-ethereum/ethdata/geth.ipc \
--deposit-contract 0x51d9c3ac566eaa8edcb45a6fc602d6412dea2e12 \
--bootstrap-node= ${ENR}
--chain-id=2019 --network-id=15