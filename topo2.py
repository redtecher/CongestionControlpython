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
from data_analyse import Data_Analyse
import optparse
import threading
import time
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
parser = optparse.OptionParser()
parser.add_option('--sr', dest='send_rate', type='int',default='50') 
# parser.add_option()
(options, args) = parser.parse_args()


def server_run(threadName,host):
    logger.info(f"【%s线程开始】{threadName}"%host.name)
    # print(f"【%s线程开始】{threadName}"%host.name)
    record =host.cmd('python3 UDPServer.py --ip %s' % host.IP())
    print(record)
    logger.info(f"【%s线程结束】{threadName}"%host.name)

def client_run(threadName,host,ip,send_rate):
    logger.info(f"【%s线程开始】{threadName}"%host.name)
    record1=host.cmd('python3 UDPClient.py --ip %s --sr %s' % (ip,send_rate))
    print(record1)
    logger.info(f"【%s线程结束】{threadName}"%host.name)

# 禁用拥塞控制
def disable_congestion_control(net):
    for host in net.hosts:
        host.cmd('sysctl -w net.ipv4.tcp_congestion_control=none')


def myNetwork():
    send_rate = []
    bandwidth =[]

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('sysctl -w net.ipv4.route.flush=1')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.2', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='192.168.1.3', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.2.2', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.2.3', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h1, s1,delay="20ms", max_queue_size=5,bw=10, cls=TCLink,loss=0)
    net.addLink(s1, h2,delay="20ms", max_queue_size=5,bw=10, cls=TCLink,loss=0)
    net.addLink(h3, s3,delay="20ms", max_queue_size=5,bw=10, cls=TCLink,loss=0)
    net.addLink(s3, h4,delay="20ms", max_queue_size=5,bw=10, cls=TCLink,loss=0)
    net.addLink(s1, r2,delay="20ms", max_queue_size=5,bw=10, cls=TCLink,loss=0)
    net.addLink(r2, s3,delay="20ms", max_queue_size=5,bw=10, cls=TCLink,loss=0)
    
    info( '*** Starting network\n')
    net.build()

    disable_congestion_control(net)
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s3').start([])

    info( '*** Post configure switches and hosts\n')
    h1.cmd('ifconfig h1-eth0 192.168.1.2/24')
    h2.cmd('ifconfig h2-eth0 192.168.1.3/24')
    h3.cmd('ifconfig h3-eth0 192.168.2.2/24')
    h4.cmd('ifconfig h4-eth0 192.168.2.3/24')
    r2.cmd('ifconfig r2-eth0 192.168.1.1/24')
    r2.cmd('ifconfig r2-eth1 192.168.2.1/24')

    h1.cmd('route add default gw 192.168.1.1')
    h2.cmd('route add default gw 192.168.1.1')
    h3.cmd('route add default gw 192.168.2.1')
    h4.cmd('route add default gw 192.168.2.1')
    
    threadh2 = threading.Thread(target=server_run,args=("threadh2",h2))
    threadh4 = threading.Thread(target=server_run,args=("threadh4",h4))
    threadh2.start()
    logger.info("h2 is running")
    threadh4.start()
    logger.info("h4 is running")
    for send_rate in range(100):
        threadh1 = threading.Thread(target=client_run,args=("threadh1",h1,h4.IP(),send_rate))
        threadh3 = threading.Thread(target=client_run,args=("threadh3",h3,h2.IP(),send_rate))
        time.sleep(2)
        threadh1.start()
        logger.info("h1 is running")
        threadh3.start()
        logger.info("h1 is running")
        threadh1.join()
        logger.info("h1 stop")
        threadh3.join()
        logger.info("h3 stop")

        # data analyse
        



    threadh2.join()
    logger.info("h2 stop")
    threadh4.join()
    logger.info("h4 stop")
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()