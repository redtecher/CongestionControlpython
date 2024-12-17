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
class UDPServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        logger.info("UDP Server started.")

    def datagram_received(self, data, addr):
        message = data.decode()
        logger.info(f"Received {message} from {addr}")
        packet = Packet.Packet()
        packet.parseMessage(message)
        
        newpacket = Packet.Packet()
        newpacket.createPacket("Server ACK",packet.seqNo)
        newpacket.ACKnum = 1
        # response = f"Hello {addr}, message received: {message}"
        logger.info(f"message send to {addr}")
        self.transport.sendto(newpacket.generateMessage().encode(), addr)

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
