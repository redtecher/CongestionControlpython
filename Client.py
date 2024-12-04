import socket


class Client:
    def __init__(self, host='127.0.0.1', port=8888):
        """
        初始化UDP客户端
        :param host: 目标服务器的IP地址，默认本地回环地址
        :param port: 目标服务器的端口号，默认8888
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, message):
        """
        向服务器发送数据
        :param message: 要发送的数据（字符串）
        """
        self.socket.sendto(message.encode('utf-8'), (self.host, self.port))

    def receive_response(self):
        """
        接收服务器返回的响应消息
        :return: 接收到的响应消息（解码后的字符串）
        """
        data, _ = self.socket.recvfrom(1024)
        received_data = data.decode('utf-8')
        return received_data



    def rdt_send(self):
        pass

    def make_packet(self):
        pass

    

    

    def close(self):
        """
        关闭客户端套接字
        """
        self.socket.close()

if __name__ == '__main__':
    client = Client()
    client.send_data("good to see you")
    client.close()
