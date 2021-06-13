#!/usr/bin/python

"""
This starts the Ethereum Blockchain.
The number of nodes started depends on the  parameters provided.
The nodes are automatically joined using the bootnode
"""

from mininet.net import Containernet
from mininet.node import Controller, Docker, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Link
import argparse, sys


def topology(args):

    "Create a network with some docker containers acting as nodes in an Ethereum Blockchain."
    n = args.num_nodes[0]
    info('*** Number of nodes will be:', n)
    info('\n')
    net = Containernet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    info('*** Adding docker containers\n')
    info('*** Setting up bootnode for BC nodes to discover eachother\n')
    boot = net.addDocker( 'boot', ip='10.0.0.2', dimage="custom-ethereum-image:bootnode", volumes=["/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts"], port_bindings={8545:8547,30301:30301}, cpu_shares=20, publish_all_ports=False)
    boot.cmdPrint('bootnode -genkey boot.key')
    boot.cmdPrint('echo -n "enode://" > eth-scripts/node_join_id')
    boot.cmdPrint('bootnode -nodekeyhex $(cat boot.key) -writeaddress | tr -d "\n" >> eth-scripts/node_join_id')
    boot.cmdPrint('echo -n "@10.0.0.2:0?discport=30301" >> eth-scripts/node_join_id')
    boot.cmdPrint('bootnode -nodekey boot.key &')

    info('*** Starting the Ethereum docker containers for the private network')
    d0 = net.addDocker( 'd0', ip='10.0.0.5', dimage="custom-ethereum-image:master", volumes=["/home/ubuntu/container-chain/go-ethereum/ethdata:/app/ethdata", "/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts"], port_bindings={8545:8545,30303:30303}, cpu_shares=20, publish_all_ports=False)
    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')

    info('*** Creating links\n')
    net.addLink(d0, s1)
    net.addLink(s1, boot)

    if n > 1:
        info('*** n is greater than one so the loop will spin up the remaining nodes')
        for h in range(n)[1:]:
            d1 = net.addDocker('d%s' % (h), ip='10.0.0.%s' % (h+6), dimage="custom-ethereum-image:node", volumes=["/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts"], cpu_shares=20, publish_all_ports=False)
            net.addLink(s1, d1)

    info('*** Starting network\n')
    net.start()
    info('*** Testing connectivity\n')
    net.ping([boot, d0])

    for h in net.hosts[1:]:
        h.cmdPrint('./eth-scripts/start-new-bc.sh &')

    info('*** Chain is running...\n')

#    info('*** Running CLI\n')
#    CLI(net)
#    info('*** Stopping network')
#    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    info('*** Entering main method...\n')
    parser = argparse.ArgumentParser(description='Create an Ethereum Blockchain')
    parser.add_argument('num_nodes', metavar='n', type=int, nargs='+', help='the number of nodes in the chain')
    args = parser.parse_args()
    topology(args)
