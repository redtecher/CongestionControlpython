# -*- coding: UTF-8 -*-
import Packet
import Client
import chardet
if __name__=='__main__':
    packet = Packet.Packet()
    packet.createPacket("我是你的什么",1)
    print(packet.checksum)

    

    


