# -*- coding: UTF-8 -*-
import socket
import optparse
import Packet
class Server:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"UDP服务器已启动，正在监听 {self.host}:{self.port}...")

    def receive_data(self):
        data, client_address = self.socket.recvfrom(1024)
        received_data = data.decode('utf-8')
        return received_data, client_address  

    def send_response(self, client_address, message):
        """
        向客户端发送响应消息
        :param client_address: 客户端地址
        :param message: 要发送的响应消息（字符串）
        """
        self.socket.sendto(message.encode('utf-8'), client_address)
        
    def close(self):
        
        self.socket.close()


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--ip', dest='ip', default='127.0.0.1')
    parser.add_option('--port', dest='port', type='int', default=8888)
    (options, args) = parser.parse_args()
    server = Server(host=options.ip,port=options.port)
    rec_data = server.receive_data()
    packet = Packet.Packet()
    packet.parseMessage(rec_data[0])
    print(packet.payload)
    server.send_response(client_address=rec_data[1],message="I have receive the data")
    server.close()