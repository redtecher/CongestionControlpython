# -*- coding: UTF-8 -*-
import socket
import optparse
import Packet
import logging
import asyncio

# 日志配置
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# 每秒发送的消息数量
SEND_RATE = 10  # 每秒 10 条消息
INTERVAL = 1 / SEND_RATE  # 每条消息的时间间隔

class Client:
    def __init__(self, host='127.0.0.1', port=8888):
        #初始化
        #host: 目标服务器的IP地址，默认本地回环地址
        #port: 目标服务器的端口号，默认8888
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(3)
    
    async def send_data(self, packet):
        loop = asyncio.get_event_loop()
        server_address=(self.host,self.port)
        await loop.sock_sendto(self.socket, packet, server_address)
        # await self.loop.sock_sendall(self.socket, packet.encode('utf-8'))

    async def receive_response(self):
        loop = asyncio.get_event_loop()
        data, _ = await loop.sock_recv(self.socket, 1024)
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


    async def send_packet(self,packet,app_msg,seqno):
        try:
            packet = self.make_packet(app_msg,seqno)
            # logger.info(f"packet: {packet}")
            await self.send_data(packet=packet.generateMessage())
            rec_data = await self.receive_response()
            logger.info("receive:"+rec_data)
        except Exception as e:
            logger.info('%d socket timeout! Resend!' % seqno)
            await self.send_packet(packet,app_msg,seqno)

    async def startsender(self,filename):   
        #发送核心逻辑
        # self.read_file('')
        content = self.read_file(filename)
        splited = content.split("\n\n")
        # logger.info(f"splited: {splited}")
        for i in range(len(splited)):
            packet =Packet.Packet()     
            await self.send_packet(packet,splited[i],i+1)
            await asyncio.sleep(INTERVAL)

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
    asyncio.run(client.startsender("in.txt"))
    client.close()
