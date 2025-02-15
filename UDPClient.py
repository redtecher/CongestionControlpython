import asyncio
import optparse
import Packet
import logging
import math
from CongestionControl import CongestionControl
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("logclient.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


data_logger = logging.getLogger("data_record")
data_logger.setLevel(level = logging.INFO)
data_handler = logging.FileHandler("data_record.txt")
data_handler.setLevel(logging.INFO)
data_handler.setFormatter(formatter)
data_logger.addHandler(data_handler)

conges_logger = logging.getLogger("congestion_record")
conges_logger.setLevel(level = logging.INFO)
conges_handler = logging.FileHandler("congestion_record.txt")
conges_handler.setLevel(logging.INFO)
conges_handler.setFormatter(formatter)
conges_logger.addHandler(conges_handler)
# conges_logger.info("thisis")
#解析参数
parser = optparse.OptionParser()
parser.add_option('--ip', dest='ip', default='127.0.0.1')
parser.add_option('--name',dest='hostname',default='h')
parser.add_option('--port', dest='port', type='int', default=8888)
parser.add_option('--msg', dest='msg')
parser.add_option('--file',dest='file')
parser.add_option('--sr',dest='send_rate',type='int')
(options, args) = parser.parse_args()

# 每秒发送的消息数量
SEND_RATE = options.send_rate  # 每秒 10 条消息
INTERVAL = 1 / SEND_RATE  # 每条消息的时间间隔
TOTAL_TIME = 600 # 总共发送时间
RETRANSMISSION_TIMEOUT = 1 # 重传超时时间
FLUSH_RATE = 0.0001 #等待时的刷新率
# sent_bytes=0
class UDPClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, message, on_response):
        self.message = message
        self.on_response = on_response
        self.pending_acks = {}
        # self.pass_byte=0
        self.sent_bytes = 0 
        self.throughput_start_time = asyncio.get_event_loop().time()
        self.cwnd_start_time = asyncio.get_event_loop().time()
        self.congestion_control = CongestionControl()

    def make_packet(self,msg,seqno):
        #根据msg生成包
        packet = Packet.Packet()
        packet.createPacket(msg,seqno)
        return packet

    def connection_made(self, transport):
        self.transport = transport
        asyncio.create_task(self.send_udp_packet())
        asyncio.create_task(self.calculate_send_throughput())
        asyncio.create_task(self.monitor_send_cwnd())

    async def send_udp_packet(self):   
        content = self.read_file("in.txt")
        splited = content.split("\n\n")
        while(True):
            for i in range(len(splited)):
                packet=self.make_packet(splited[i],i)
                self.pending_acks[i] = packet # Store packet for potential retransmission
                # self.transport.sendto(packet.generateMessage().encode())
                asyncio.create_task(self.send_with_retransmission(packet, i))
                send_rate = math.floor(self.congestion_control.get_send_rate())
                await asyncio.sleep(1/send_rate)

    async def calculate_send_throughput(self):
        while True:
            await asyncio.sleep(10)  # Wait for 10 seconds
            elapsed_time = asyncio.get_event_loop().time() - self.throughput_start_time
            bytes_per_second = self.sent_bytes / elapsed_time
            data_logger.info(f"Send Rate {SEND_RATE}:Sent {self.sent_bytes} bytes in {elapsed_time:.2f} seconds, throughput: {bytes_per_second:.2f} bytes/second")
            # Reset counters
            self.sent_bytes = 0
            self.throughput_start_time = asyncio.get_event_loop().time() 
            
    async def monitor_send_cwnd(self):
        flag = 1
        while True:
            await asyncio.sleep(1)  # Wait for 1 seconds
            elapsed_time = asyncio.get_event_loop().time() - self.cwnd_start_time
            send_rate=self.congestion_control.get_send_rate()
            # print(send_rate)
            conges_logger.info(f"{options.hostname}:{flag} times CWND: {send_rate:.2f}")
            # Reset counters
            self.cwnd_start_time = asyncio.get_event_loop().time() 
            flag+=1


    async def send_with_retransmission(self, packet, seqno):
        flag=1
        while seqno in self.pending_acks:
            logger.info(f"The {flag} time Sending message: {packet}")
            message_send = packet.generateMessage()
            self.transport.sendto(message_send.encode())
            self.sent_bytes += len(message_send)
            flag+=1
            try:
                await asyncio.wait_for(self.wait_for_ack(seqno), timeout=RETRANSMISSION_TIMEOUT)
                break
            except asyncio.TimeoutError:
                logger.warning(f"Timeout for packet {seqno} , retransmitting...")
                self.congestion_control.on_timeout()

    async def wait_for_ack(self, seqno):
        while seqno in self.pending_acks:
            await asyncio.sleep(FLUSH_RATE)

    def read_file(self,filename):
        # 打开文件
        encoding='utf-8'
        with open(filename, 'r',encoding=encoding) as file:
            # 读取文件内容
            content = file.read()
            return content

    def datagram_received(self, data, addr):
        response = data.decode()
        logger.info(response)
        packet = Packet.Packet()
        packet.parseMessage(response)
        seqno = packet.seqNo
        if seqno in self.pending_acks:
            logger.info(f"delete")
            del self.pending_acks[seqno]
            self.congestion_control.on_ack(1)
        self.on_response(response)

    def error_received(self, exc):
        logger.info(f"Error received: {exc}")

    def connection_lost(self, exc):
        logger.info(f"UDP Client stopped.")
        asyncio.get_event_loop().stop()

async def udp_client(host,port,message):
    loop = asyncio.get_event_loop()

    
    def on_response(response):
        pass
    
    
    connect = loop.create_datagram_endpoint(
        lambda: UDPClientProtocol(message, on_response), remote_addr=(host, port)
    )
    transport, protocol = await connect
    await asyncio.sleep(TOTAL_TIME)


if __name__ == "__main__":
    asyncio.run(udp_client(host=options.ip,port=options.port,message=options.msg))