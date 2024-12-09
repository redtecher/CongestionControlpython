#!/usr/bin/python
# -*- coding: UTF-8 -*-
from mininet.topo import Topo, SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.cli import CLI
import threading
import time

def server_run(threadName,host):
    print(f"【线程开始】{threadName}")
    print(host.IP())
    print(host.cmd('python3 Server.py --ip %s' % host.IP()))
    print(f"【线程结束】{threadName}")

def client_run(threadName,host,ip):
    print(f"【线程开始】{threadName}")
    print(host.cmd('python3 Client.py --ip %s --msg "hello world"' % ip))
    print(host.IP())
    print(f"【线程结束】{threadName}")


def main():
    lg.setLogLevel('info')

    net = Mininet(SingleSwitchTopo(k=2))
    net.start()

    h1 = net.get('h1')
    thread1 = threading.Thread(target=server_run,args=("thread1",h1))
    # print(h1.cmd('python3 Server.py --ip %s' % h1.IP()))
    h2 = net.get('h2')
    thread2 = threading.Thread(target=client_run,args=("thread2",h2,h1.IP()))
    # print(h2.cmd('python3 Client.py --ip %s --msg "hello world"' % h1.IP()))
    thread1.start()
    print("thread1 is running")
    time.sleep(2)
    thread2.start()
    print("thread2 is running")
    thread1.join()
    thread2.join()

    # h2.monitor()
    # CLI( net )
    # p1.terminate()
    net.stop()

if __name__ == '__main__':
    main()