#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This starts the Ethereum 2.0 Blockchain.
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

def topology(args):
    '''Create a network with some docker containers acting as beacon nodes and validators in an Ethereum 2.0 Blockchain.'''


if __name__ == '__main__':
    setLogLevel('info')
    info('*** Entering main method...\n')
    parser = \
        argparse.ArgumentParser(description='Create an Ethereum 2.0 Proof of Stake Blockchain'
                                )
    parser.add_argument('num_nodes', metavar='n', type=int, nargs='+',
                        help='the number of beacon nodes in the chain')
    parser.add_argument('root', metavar='r', type=str, nargs='+',
                        help='the root directory of the project')
    args = parser.parse_args()
    topology(args)
