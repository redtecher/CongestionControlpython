import socket
class Server:
    def __init__(self, host='127.0.0.1', port=8888):
        """
        初始化UDP服务器
        :param host: 服务器监听的IP地址，默认本地回环地址
        :param port: 服务器监听的端口号，默认8888
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"UDP服务器已启动，正在监听 {self.host}:{self.port}...")

    def receive_data(self):
        """
        接收客户端发送的数据，返回接收到的数据和客户端地址
        :return: (接收到的数据（解码后的字符串），客户端地址)
        """
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
        """
        关闭服务器套接字
        """
        self.socket.close()


if __name__ == '__main__':
    server = Server()
    rec_data = server.receive_data()
    print(rec_data)
    server.close()