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

    r = args.root[0]
    info('*** Project r is:', r)
    info('\n')

    net = Containernet(controller=Controller)

    info('*** Adding controller\n')
    net.addController('c0')

    # info('*** Adding switch\n')
    # s1 = net.addSwitch('s1')

    info('*** Adding hosts\n')
    info('*** Adding docker containers\n')
    info('*** Setting up bootnode for BC nodes to discover eachother\n')

    if c == 'pow':

        info('*** POW consensus is executing')
        netflow = net.addDocker(
            'netflow',
            ip='10.0.0.1',
            dimage='netflow:test',
            port_bindings={9995: 9995},
            cpu_shares=20,
            publish_all_ports=False,
        )
        netflow.cmdPrint('service nfdump restart &')
        netflow.cmdPrint('nfcapd -b 10.0.0.1 -l /opt/flowexport/nfcapd &')

        boot = net.addDocker(
            'boot',
            ip='10.0.0.2',
            dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:boot',
            volumes=[str(r) + '/go-ethereum/eth-scripts:/app/eth-scripts'
                     ],
            port_bindings={8545: 8545, 30301: 30301, 8888: 8888},
            cpu_shares=20,
            publish_all_ports=False,
        )
        boot.cmdPrint('bootnode -genkey boot.key')
        boot.cmdPrint('echo -n "enode://" > eth-scripts/node_join_id')
        boot.cmdPrint(
            'bootnode -nodekeyhex $(cat boot.key) -writeaddress | tr -d "\n" >> eth-scripts/node_join_id')
        boot.cmdPrint(
            'echo -n "@10.0.0.2:0?discport=30301" >> eth-scripts/node_join_id')
        boot.cmdPrint('bootnode -nodekey boot.key &')

        info('*** Starting the Ethereum docker containers for the private network'
             )
        d0 = net.addDocker(
            'd0',
            ip='10.0.0.5',
            dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:master',
            volumes=[str(r) + '/go-ethereum/ethdata:/app/ethdata',
                     str(r) + '/go-ethereum/eth-scripts:/app/eth-scripts'
                     ],
            port_bindings={8545: 8543, 30303: 30303},
            cpu_shares=20,
            publish_all_ports=False,
        )
        info('*** Adding switch\n')
        s1 = net.addSwitch('s1')

        info('*** Creating links\n')
        net.addLink(d0, s1)
        net.addLink(s1, netflow)
        net.addLink(s1, boot)

        d0.cmdPrint('fprobe -p -f "host 10.0.0.5" -i d0-eth0 -x 0 -c /var/empty -u nobody -l 1: 10.0.0.1:9995 &')

        # The actual object associated with d1 changes every time this loop runs
        # But, each time, it creates a new container and adds it to the switch
        if n > 1:
            info('*** n is greater than one so the loop will spin up the remaining nodes\n'
                 )
            for h in range(n)[1:]:
                
                ipAddress = '10.0.0.%s' % (h + 6)
                info('*** IP ADDRESS IS *** : ' + ipAddress + '\n')
                interface = 'd%s' % h + '-eth0'
                info('*** INTERFACE IS *** :' + interface + '\n')
                d1 = net.addDocker(
                    'd%s' % h,
                    ip='10.0.0.%s' % (h + 6),
                    dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:node',
                    volumes=[str(r) + '/go-ethereum/eth-scripts:/app/eth-scripts'
                             ],
                    port_bindings={8545: (8545 + h), 30303: (30303 + h)},
                    cpu_shares=20,
                    publish_all_ports=False,
                )
                net.addLink(s1, d1)
                d1.cmdPrint('fprobe -p -f "host ' + str(ipAddress) + '" -i ' + str(interface) + ' -x 0 -c /var/empty -u nobody -l 1: 10.0.0.1:9995 &')

        info('*** Starting network\n')
        net.start()
        info('*** Testing connectivity\n')
        net.ping([boot, d0])

        for h in net.hosts[1:]:
            h.cmdPrint('./eth-scripts/start-new-bc.sh &')

        info('*** Chain is running...\n')
        info('*** Running CLI\n')
        # This seems to be needed to maintain connectivity between nodes
        # It causes a mininet CLI to be launched. Terminating the CLI will
        # stop and remove the containers. In a separate terminal, we can access
        # the geth CLI to interact with the Blockchain. Bash scripts are provided.
        CLI(net)
        info('*** Stopping network')
        net.stop()
    else:

        boot = net.addDocker(
            'boot',
            ip='10.0.0.2',
            dimage='registry.gitlab.com/sri-ait-ie/phd-projects/saul-gill/container-chain-bc-simulator/custom-ethereum-image:boot-poa',
            volumes=[str(r) + '/go-ethereum/eth-scripts:/app/eth-scripts'
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
            volumes=[str(r) + '/go-ethereum/ethdata:/app/ethdata',
                     str(r) + '/go-ethereum/eth-scripts:/app/eth-scripts'
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
                    volumes=[str(r) + '/go-ethereum/eth-scripts:/app/eth-scripts'
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
        info('*** Running CLI\n')
        # This seems to be needed to maintain connectivity between nodes
        # It causes a mininet CLI to be launched. Terminating the CLI will
        # stop and remove the containers. In a separate terminal, we can access
        # the geth CLI to interact with the Blockchain. Bash scripts are provided.
        CLI(net)
        info('*** Stopping network')
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    info('*** Entering main method...\n')
    parser = \
        argparse.ArgumentParser(description='Create an Ethereum Blockchain'
                                )
    parser.add_argument('num_nodes', metavar='n', type=int, nargs='+',
                        help='the number of nodes in the chain')
    parser.add_argument('consensus', metavar='c', type=str, nargs='+',
                        help='the type of consensus algorithm to be used'
                        )
    parser.add_argument('root', metavar='r', type=str, nargs='+',
                        help='the root directory of the project')
    args = parser.parse_args()
    topology(args)
