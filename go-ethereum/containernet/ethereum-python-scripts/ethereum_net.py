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


def topology(args):
    '''Create a network with some docker containers acting as nodes in an Ethereum Blockchain.'''

    n = args.num_nodes[0]
    info('*** Number of nodes will be:', n)
    info('\n')

    c = args.consensus[0]
    info('*** Consensus algorithm used will be:', c)
    info('\n')

    net = Containernet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    info('*** Adding docker containers\n')
    info('*** Setting up bootnode for BC nodes to discover eachother\n')

    if c == 'pow':

        info('*** POW consensus is executing')
        boot = net.addDocker(
            'boot',
            ip='10.0.0.2',
            dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:boot',
            volumes=['/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts'
                     ],
            port_bindings={8545: 8547, 30301: 30301},
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

        info('*** Starting the Ethereum docker containers for the private network'
             )
        d0 = net.addDocker(
            'd0',
            ip='10.0.0.5',
            dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:master',
            volumes=['/home/ubuntu/container-chain/go-ethereum/ethdata:/app/ethdata'
                     ,
                     '/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts'
                     ],
            port_bindings={8545: 8545, 30303: 30303},
            cpu_shares=20,
            publish_all_ports=False,
            )
        info('*** Adding switch\n')
        s1 = net.addSwitch('s1')

        info('*** Creating links\n')
        net.addLink(d0, s1)
        net.addLink(s1, boot)

        if n > 1:
            info('*** n is greater than one so the loop will spin up the remaining nodes'
                 )
            for h in range(n)[1:]:
                d1 = net.addDocker(
                    'd%s' % h,
                    ip='10.0.0.%s' % (h + 6),
                    dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:node',
                    volumes=['/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts'
                             ],
                    cpu_shares=20,
                    publish_all_ports=False,
                    )
                net.addLink(s1, d1)

        info('*** Starting network\n')
        net.start()
        info('*** Testing connectivity\n')
        net.ping([boot, d0])

        for h in net.hosts[1:]:
            h.cmdPrint('./eth-scripts/start-new-bc.sh &')

        info('*** Chain is running...\n')
    else:

        boot = net.addDocker(
            'boot',
            ip='10.0.0.2',
            dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:boot-poa',
            volumes=['/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts'
                     ],
            port_bindings={8545: 8547, 30301: 30301},
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

        info('*** Starting the Ethereum docker containers for the private network'
             )
        d0 = net.addDocker(
            'd0',
            ip='10.0.0.5',
            dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:master-poa',
            volumes=['/home/ubuntu/container-chain/go-ethereum/ethdata:/app/ethdata'
                     ,
                     '/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts'
                     ],
            port_bindings={8545: 8545, 30303: 30303},
            cpu_shares=20,
            publish_all_ports=False,
            )
        info('*** Adding switch\n')
        s1 = net.addSwitch('s1')

        info('*** Creating links\n')
        net.addLink(d0, s1)
        net.addLink(s1, boot)

        if n > 1:
            info('*** n is greater than one so the loop will spin up the remaining nodes'
                 )
            for h in range(n)[1:]:
                d1 = net.addDocker(
                    'd%s' % h,
                    ip='10.0.0.%s' % (h + 6),
                    dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:node-poa',
                    volumes=['/home/ubuntu/container-chain/go-ethereum/eth-scripts:/app/eth-scripts'
                             ],
                    cpu_shares=20,
                    publish_all_ports=False,
                    )
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
    parser = \
        argparse.ArgumentParser(description='Create an Ethereum Blockchain'
                                )
    parser.add_argument('num_nodes', metavar='n', type=int, nargs='+',
                        help='the number of nodes in the chain')
    parser.add_argument('consensus', metavar='c', type=str, nargs='+'
                        ,
                        help='the type of consensus algorithm to be used'
                        )
    args = parser.parse_args()
    topology(args)

