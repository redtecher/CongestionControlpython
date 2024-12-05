import Packet
if __name__=='__main__':
    packet = Packet.Packet()
    packet.createPacket("Hello_World",1)
    print(packet.checksum)
    str=packet.generateMessage()
    print(str)
    recv_packet = Packet.Packet()
    recv_packet.parseMessage(str)
    print(recv_packet.seqNo)
    print(recv_packet.ACKnum)
    print(recv_packet.checksum)
    print(recv_packet.payload)


