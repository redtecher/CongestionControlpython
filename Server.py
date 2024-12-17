# -*- coding: UTF-8 -*-
import socket
import optparse
import Packet
import logging
import asyncio
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
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.setblocking(False)
        logger.info(f"UDP服务器已启动，正在监听 {self.host}:{self.port}...")
    
    def connection_made(self, transport):
        self.transport = transport

    async def receive_data(self):
        loop = asyncio.get_event_loop()
        data, client_address = await loop.sock_recvfrom(self.socket, 1024)
        logger.info(f"data: {data}")
        received_data = data.decode('utf-8', 'ignore')
        logger.info(f"received_data: {received_data}")
        return received_data, client_address

    async def send_response(self, client_address, message):
        # loop = asyncio.get_event_loop()
        await self.loop.sock_sendall(self.socket, message.encode('utf-8'))

    async def receive_file(self):
        payload_content = ""
        while payload_content != "ENDOFALL":
            try:
                rec_data, client_address = await self.receive_data()
                logger.info(f"Received data from {client_address}: {rec_data}")
                packet = Packet.Packet()
                packet.parseMessage(rec_data)
                logger.info('Received the packet with seqNo: ' + str(packet.seqNo))
                payload_content = packet.payload
                if packet.validateMessage():
                    await self.send_response(client_address=client_address, message="I have received the data:" + str(packet.seqNo))
                else:
                    await self.send_response(client_address=client_address, message="Found error in packet")
            except Exception as e:
                logger.error(f"Error receiving data: {e}")
    
    def send_ACK(self,receive_packet:Packet.Packet):
        send_packet = Packet.Packet()
        ACK_num = receive_packet.ACKnum
        send_packet.createPacket("ACK"+str(receive_packet.ACKnum),ACK_num)

        

    def close(self):
        self.socket.close()

async def main():
    parser = optparse.OptionParser()
    parser.add_option('--ip', dest='ip', default='127.0.0.1')
    parser.add_option('--port', dest='port', type='int', default=8888)
    (options, args) = parser.parse_args()
    server = Server(host=options.ip, port=options.port)
    try:
        await server.receive_file()
    except Exception as e:
        logger.error(f"Error in server operation: {e}")
    finally:
        server.close()

if __name__ == '__main__':
    asyncio.run(main())