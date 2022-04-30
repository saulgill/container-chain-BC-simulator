# Container-Chain Blockchain Simulator
---
Allows the use of containerchain to create a blockchain to create a chain of arbitrary size

---
## Installation
### Containernet
1. Clone the repo.
```
$ git clone https://gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-BC-simulator.git
```
2. Install containernet dependencies.
Go to the folder go-ethereum/containernet
```
$ sudo apt-get install ansible git aptitude
$ git clone https://github.com/containernet/containernet.git
$ cd ./ansible
$ sudo ansible-playbook -i "localhost," -c local install.yml
$ cd ..
```
This may take a little time. Then...
```
$ sudo make develop
$ # or 
$ sudo make install
```
and test out that it has installed correctly. Mininet needs root - so sudo must be used.
```
$ sudo python3 examples/containernet_example.py
```
This will leave you in a command prompt similar to mininet but if you "docker ps" on another terminal, you will see that several containers have been brought up. After you stop and delete these containers, we can proceed to the next step.

---
### Ethereum Private Chain
You must install the latest version of go. Details [here](https://www.vultr.com/docs/install-the-latest-version-of-golang-on-ubuntu)
Once installation is complete, we can build and install go-ethereum (geth) from the go-ethereum folder.
```
$ make all
```
---
## Use Containernet with Private Ethereum
Specific docker images are required to create the chain. These have been provided in the gitlab registry and you can pull them from [here](registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image). You will, of course need to login to the registry in Gitlab. You should just pull all these images

Alternatively, you can build the images yourself. All of the Dockerfiles are present in the [Dockerfiles](https://gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-BC-simulator/-/tree/master/go-ethereum/Dockerfiles) directory.

A unix password should be configured for your user. Mininet needs root so this is required. You will need to use this to start the chain in the script.

Finally copy the "ethdata" directory into the go-ethereum directory. This directory contains a couple of pre-made account private keys. The corresponding accounts will be prefunded with some Ether on creation of the chain. The prefunding is done in the genesis.json [files](https://gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-BC-simulator/-/tree/master/go-ethereum/GenesisFiles). There are several of these files associated with different types of nodes (bootnode, main node...) and there are different genesis files for different types of consensus - that is where the type of consensus used is specified in Ethereum.
```
cp -r ./ethdata ./go-ethereum
```
At this stage, you are ready to start the Blockchain. Here is an example command.
```
./start-chain.sh -p YOUR_PASSWORD -cs SIZE_OF_DESIRED_CHAIN -c CONSENSUS_ALGORITHM (pow - default, or poa)
```
You can then see the containers running in the background if you query Docker. And you can get a console into the chain if you wish to run commands by executing the following:
```
./geth_to_chain.sh
```
Finally, you can stop the chain and delete all the containers with the stop script
```
./stop-chain.sh
```
---
# Soon Adding Eth2 Info