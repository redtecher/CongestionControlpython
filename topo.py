#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')
    # s1 = net.addSwitch('s1')
    # s2 = net.addSwitch('s2')
    # s3 = net.addSwitch('s3')
    # s4 = net.addSwitch('s4')
    r5 = net.addHost('r5', cls=Node, ip='0.0.0.0')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    r6 = net.addHost('r6', cls=Node, ip='0.0.0.0')
    r6.cmd('sysctl -w net.ipv4.ip_forward=1')
    r7 = net.addHost('r7', cls=Node, ip='0.0.0.0')
    r7.cmd('sysctl -w net.ipv4.ip_forward=1')
    r8 = net.addHost('r8', cls=Node, ip='0.0.0.0')
    r8.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='192.168.2.1', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.3.1', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.4.1', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)
    net.addLink(h4, s4)
    net.addLink(s1, r6)
    net.addLink(r6, s2)
    net.addLink(s2, r7)
    net.addLink(s1, r5)
    net.addLink(r5, s3)
    net.addLink(s3, r8)
    net.addLink(r8, s4)
    net.addLink(s4, r7)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])
    net.get('s4').start([])

    info( '*** Post configure switches and hosts\n')
    # 接口配置
    h1.cmd('ifconfig h1-eth0 192.168.1.1/24')
    h2.cmd('ifconfig h2-eth0 192.168.2.1/24')
    h3.cmd('ifconfig h3-eth0 192.168.3.1/24')
    h4.cmd('ifconfig h4-eth0 192.168.4.1/24')
    r5.cmd('ifconfig r5-eth0 192.168.1.2/24')
    r5.cmd('ifconfig r5-eth1 192.168.3.2/24')
    r6.cmd('ifconfig r6-eth0 192.168.1.3/24')
    r6.cmd('ifconfig r6-eth1 192.168.2.3/24')
    r7.cmd('ifconfig r7-eth0 192.168.2.2/24')
    r7.cmd('ifconfig r7-eth1 192.168.4.2/24')
    r8.cmd('ifconfig r8-eth0 192.168.3.3/24')
    r8.cmd('ifconfig r8-eth1 192.168.4.3/24')
    # 网关配置
    h1.cmd('route add default gw 192.168.1.2')
    h2.cmd('route add default gw 192.168.2.3')
    h3.cmd('route add default gw 192.168.3.3')
    h4.cmd('route add default gw 192.168.4.2')

    # 路由配置
    r5.cmd('route add -net 192.168.4.0/24 gw 192.168.3.3')
    r5.cmd('route add -net 192.168.2.0/24 gw 192.168.3.3')

    r6.cmd('route add -net 192.168.3.0/24 gw 192.168.1.2')
    r6.cmd('route add -net 192.168.4.0/24 gw 192.168.1.2')

    r7.cmd('route add -net 192.168.1.0/24 gw 192.168.2.3')
    r7.cmd('route add -net 192.168.3.0/24 gw 192.168.2.3')

    r8.cmd('route add -net 192.168.1.0/24 gw 192.168.4.2')
    r8.cmd('route add -net 192.168.2.0/24 gw 192.168.4.2')

    # h1.cmd('traceroute 192.168.3.1')
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
