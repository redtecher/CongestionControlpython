# -*- coding: UTF-8 -*-
import socket
import optparse
import Packet
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
class Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        logger.info(f"UDP服务器已启动，正在监听 {self.host}:{self.port}...")

    def receive_data(self):
        data, client_address = self.socket.recvfrom(1024)
        received_data = data.decode('utf-8','ignore')
        return received_data, client_address  

    def send_response(self, client_address, message):
        
        self.socket.sendto(message.encode('utf-8'), client_address)

    def receive_file(self):
        payload_content = ""
        while(payload_content!="ENDOFALL"):
            rec_data = self.receive_data()
            logger.info(rec_data)
            packet = Packet.Packet()
            packet.parseMessage(rec_data[0])
            logger.info('receive the packet'+str(packet.seqNo))
            payload_content = packet.payload
            # print(payload_content)
            if(packet.validateMessage()):
                server.send_response(client_address=rec_data[1],message="I have receive the data:"+str(packet.seqNo))
            else:
                server.send_response(client_address=rec_data[1],message="found error packet")
    
    def send_ACK(self,receive_packet:Packet.Packet):
        send_packet = Packet.Packet()
        ACK_num = receive_packet.ACKnum
        send_packet.createPacket("ACK"+str(receive_packet.ACKnum),ACK_num)

        

    def close(self):
        self.socket.close()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--ip', dest='ip', default='127.0.0.1')
    parser.add_option('--port', dest='port', type='int', default=8888)
    (options, args) = parser.parse_args()
    server = Server(host=options.ip,port=options.port)
    server.receive_file()
    server.close()