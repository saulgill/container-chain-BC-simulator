cd prysm
go run ./tools/genesis-state-gen --num-validators=256 --output-ssz=genesis.ssz --mainnet-config
mv genesis.ssz ../go-ethereum/eth-scripts/