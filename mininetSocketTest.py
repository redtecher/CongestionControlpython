#!/usr/bin/python

from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI

def main():
    lg.setLogLevel('info')

    net = Mininet(SingleSwitchTopo(k=2))
    net.start()

    h1 = net.get('h1')
    p1 = h1.popen('python3 Server.py --ip %s &' % h1.IP())
    
    h2 = net.get('h2')
    gettext = h2.cmd('python3 Client.py --ip %s --msg "hello world"' % h1.IP())
    print(gettext)
    # CLI( net )
    p1.terminate()
    net.stop()

if __name__ == '__main__':
    main()