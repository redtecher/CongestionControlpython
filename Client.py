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

class Client:
    def __init__(self, host='127.0.0.1', port=8888):
        #初始化
        #host: 目标服务器的IP地址，默认本地回环地址
        #port: 目标服务器的端口号，默认8888
        
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(4)

    def send_data(self, packet):
        #发送数据
        self.socket.sendto(packet.encode('utf-8'), (self.host, self.port))

    def receive_response(self):
        #接收服务器返回的响应消息
        #:return: 接收到的响应消息（解码后的字符串）
        data, _ = self.socket.recvfrom(1024)
        received_data = data.decode('utf-8')
        return received_data

    def read_file(self,filename):
        # 打开文件
        encoding='utf-8'
        # with open(filename, 'r',encoding=encoding,errors='replace') as file:
        with open(filename, 'r',encoding=encoding) as file:
            # 读取文件内容
            content = file.read()
            return content


    def send_packet(self,packet,app_msg,seqno):
        try:
            packet = self.make_packet(app_msg,seqno)
            self.send_data(packet=packet.generateMessage())
            rec_data = self.receive_response()
            logger.info("receive:"+rec_data)
        except Exception as e:
            logger.info('%d socket timeout! Resend!' % seqno)
            self.send_packet(packet,app_msg,seqno)

    def startsender(self,filename):   
        #发送核心逻辑
        # self.read_file('')
        content = client.read_file(filename)
        splited = content.split("\n\n")
        for i in range(len(splited)):
            packet =Packet.Packet()     
            self.send_packet(packet,splited[i],i+1)

    def make_packet(self,msg,seqno):
        #根据msg生成包
        packet = Packet.Packet()
        packet.createPacket(msg,seqno)
        return packet
        
    def validateACK(seqNo,ACKfromNetwork):
        #检验ACK函数
        getack = "ACK" + seqNo.toString()
        if getack == ACKfromNetwork:
            return True
        else:
            return False
 

    def close(self):
        #关闭客户端套接字
        self.socket.close()

if __name__ == '__main__':
    #解析参数
    parser = optparse.OptionParser()
    parser.add_option('--ip', dest='ip', default='127.0.0.1')
    parser.add_option('--port', dest='port', type='int', default=8888)
    parser.add_option('--msg', dest='msg')
    parser.add_option('--file',dest='file')
    (options, args) = parser.parse_args()
    client = Client(host=options.ip,port=options.port)
    client.startsender("in.txt")
    client.close()
