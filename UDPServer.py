import asyncio
import optparse
import Packet
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("logserver.txt")
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
logger.info("This is an info message from the main logger.")  # 记录到 logserver.txt
data_logger.info("This is an info message from the data logger.")  # 记录到 data_record.txt

class UDPServerProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.received_bytes = 0
        self.start_time = asyncio.get_event_loop().time()

    def connection_made(self, transport):
        self.transport = transport
        logger.info("UDP Server started.")
        asyncio.create_task(self.calculate_throughput())

    def datagram_received(self, data, addr):
        message = data.decode()
        logger.info(f"Received {message} from {addr},data_num :{len(message)}")
        self.received_bytes += len(message)
        # receive_message_num = len(message)
        packet = Packet.Packet()
        packet.parseMessage(message)
        newpacket = Packet.Packet()
        newpacket.createPacket("Server ACK",packet.seqNo)
        newpacket.ACKnum = 1
        # response = f"Hello {addr}, message received: {message}"
        logger.info(f"message send to {addr}")
        self.transport.sendto(newpacket.generateMessage().encode(), addr)

    async def calculate_throughput(self):
        send_rate_init = 1
        while True:
            await asyncio.sleep(10)  # Wait for 10 seconds
            elapsed_time = asyncio.get_event_loop().time() - self.start_time
            bytes_per_second = self.received_bytes / elapsed_time
            data_logger.info(f"Send Rate {send_rate_init}:Received {self.received_bytes} bytes in {elapsed_time:.2f} seconds, throughput: {bytes_per_second:.2f} bytes/second")
            # Reset counters
            self.received_bytes = 0
            self.start_time = asyncio.get_event_loop().time()
            send_rate_init += 1 

    def error_received(self, exc):
        logger.info(f"Error received: {exc}")

    def connection_lost(self, exc):
        logger.info("UDP Server stopped.")

async def main():
    parser = optparse.OptionParser()
    parser.add_option('--ip', dest='ip', default='127.0.0.1')
    parser.add_option('--port', dest='port', type='int', default=8888)
    (options, args) = parser.parse_args()
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(), local_addr=(options.ip, options.port)
    )
    transport, protocol = await listen

    logger.info(f"UDP server running on {options.ip}:{options.port}")
    try:
        await asyncio.Event().wait()  # Keep the server running
    except asyncio.CancelledError:
        transport.close()
        logger.info("Server stopped.")

if __name__ == "__main__":
    asyncio.run(main())
