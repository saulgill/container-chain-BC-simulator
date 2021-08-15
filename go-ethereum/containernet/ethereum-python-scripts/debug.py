#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import argparse
import sys


def topology():
    '''Create a network with some docker containers acting as nodes in an Ethereum Blockchain.'''


    net = Containernet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    info('*** Adding docker containers\n')

    info('*** POW consensus is executing')
    boot = net.addDocker(
        'boot',
        ip='10.0.0.2',
        dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:boot',
        volumes=['/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts'
                 ],
        port_bindings={8545: 8544, 8888: 8888},
        cpu_shares=20,
        publish_all_ports=False,
        )
    boot.cmdPrint('bootnode -genkey boot.key')
    boot.cmdPrint('echo -n "enode://" > eth-scripts/node_join_id')
    boot.cmdPrint('bootnode -nodekeyhex $(cat boot.key) -writeaddress | tr -d "\n" >> eth-scripts/node_join_id'
                  )
    boot.cmdPrint('echo -n "@10.0.0.2:0?discport=30301" >> eth-scripts/node_join_id'
                  )
    boot.cmdPrint('bootnode -nodekey boot.key &')

#    info('*** Creating links\n')

#    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    net.addLink(s1, boot)


if __name__ == '__main__':
    setLogLevel('info')
    topology()

