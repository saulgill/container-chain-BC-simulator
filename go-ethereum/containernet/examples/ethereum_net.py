#!/usr/bin/python

"""
This example shows how to create a simple network and
how to create docker containers (based on existing images)
to it.
"""

from mininet.net import Containernet
from mininet.node import Controller, Docker, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Link


def topology():

    "Create a network with some docker containers acting as hosts."

    net = Containernet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
#    h1 = net.addHost('h1')
#    h2 = net.addHost('h2')
#    volumes=["/home/ubuntu/container-chain/ethdata:/app/ethdata"]
    info('*** Adding docker containers\n')
    info('*** Setting up bootnode for BC nodes to discover eachother\n')
    boot = net.addDocker( 'boot', ip='10.0.0.2', dimage="custom-ethereum-image:bootnode", volumes=["/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts"], port_bindings={8545:8547,30301:30301}, cpu_shares=20, publish_all_ports=False)
    boot.cmdPrint('bootnode -genkey boot.key')
    boot.cmdPrint('echo -n "enode://" > eth-scripts/node_join_id')
    boot.cmdPrint('bootnode -nodekeyhex $(cat boot.key) -writeaddress | tr -d "\n" >> eth-scripts/node_join_id')
    boot.cmdPrint('echo -n "@10.0.0.2:0?discport=30301" >> eth-scripts/node_join_id')
    boot.cmdPrint('bootnode -nodekey boot.key &')

    info('*** Starting the Ethereum docker containers for the private network')
    d1 = net.addDocker( 'd1', ip='10.0.0.5', dimage="custom-ethereum-image:master", volumes=["/home/ubuntu/container-chain/go-ethereum/ethdata:/app/ethdata", "/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts"], port_bindings={8545:8545,30303:30303}, cpu_shares=20, publish_all_ports=False)
    d2 = net.addDocker( 'd2', ip='10.0.0.6', dimage="custom-ethereum-image:node", volumes=["/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts"], port_bindings={8545:8546,30303:30304}, cpu_shares=20, publish_all_ports=False)
    # using advanced features like volumes and exposed ports
    #d2 = net.addDocker('d2', dimage="ubuntu:trusty", volumes=["/:/mnt/vol1:rw"], ports=[9999], port_bindings={9999:9999}, publish_all_ports=True)
    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    #s2 = net.addSwitch('s2', cls=OVSSwitch)
    #s3 = net.addSwitch('s3')

    info('*** Creating links\n')
    net.addLink(d1, s1)
    net.addLink(s1, d2)
    net.addLink(s1, boot)
#    net.addLink(h2, s2)
#    net.addLink(d2, s2)
#    net.addLink(s1, s2)
#    #net.addLink(s1, s2, cls=TCLink, delay="100ms", bw=1, loss=10)
    # try to add a second interface to a docker container
#    net.addLink(d2, s3, params1={"ip": "10.0.0.254/8"})
#    net.addLink(d3, s3)

    info('*** Starting network\n')
#    net.start()
    net.start()
    info('*** Testing connectivity\n')
    net.ping([d1, d2])
    d1.cmdPrint('./eth-scripts/start-new-bc.sh &')
    d2.cmdPrint('./eth-scripts/start-new-bc.sh &')
#    d1.sendCmd('geth --datadir="ethdata" --rpc --rpcport "8000" init /app/genesis.json')
#    d1.sendCmd('geth --datadir="ethdata" --networkid 15 --nodiscover --rpc --rpcport "8000" --rpcaddr "0.0.0.0" --rpccorsdomain "*" --rpcapi "eth,net,web3,miner,debug,personal,rpc" --allow-insecure-unlock')
#    d2.sendCmd('geth init /app/genesis.json &')
#    d2.sendCmd('geth --datadir="ethdata1" --networkid 15 --nodiscover --rpc --rpcport "8000" --rpcaddr "0.0.0.0" --rpccorsdomain "*" --rpcapi "eth,net,web3,miner,debug,personal,rpc" --allow-insecure-unlock &')
    info('*** Running CLI\n')
    CLI(net)
    info('*** Stopping network')
    net.stop()
#    net.ping([d1, d2])

    # our extended ping functionality
 #   net.ping([d1], manualdestip="10.0.0.252")
 #   net.ping([d2, d3], manualdestip="11.0.0.254")

  #  info('*** Dynamically add a container at runtime\n')
  #  d4 = net.addDocker('d4', dimage="ubuntu:trusty")
    # we have to specify a manual ip when we add a link at runtime
   # net.addLink(d4, s1, params1={"ip": "10.0.0.254/8"})
    # other options to do this
    #d4.defaultIntf().ifconfig("10.0.0.254 up")
    #d4.setIP("10.0.0.254")

    # if this ping keeps failing, use some waiting
    # time.sleep(2)

    #net.ping([d1], manualdestip="10.0.0.254")

#    info('*** Running CLI\n')
 #   CLI(net)

  #  info('*** Stopping network')
   # net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
