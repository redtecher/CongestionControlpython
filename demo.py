import threading
import time
import random
import queue
import matplotlib.pyplot as plt

# 参数设置
BUFFER_SIZE = 10  # BuFFER规则
SIMULATION_TIME = 30  # 延长模拟时间（秒）
PACKET_GEN_RATE_START = 2  # 初始数据包生成率（每秒）
PACKET_GEN_RATE_INCREMENT = 2  # 每秒增加的数据包生成率
DELAY_MEAN = 0.1  # 网络延迟的数学期望（秒）
DELAY_STDDEV = 0.05  # 网络延迟的震荡幅度（标准差）

# 全局变量
packets_sent = 0
packets_received = 0
packets_dropped = 0
lock = threading.Lock()

# 转发节点缓冲区
forward_buffer = queue.Queue(maxsize=BUFFER_SIZE)

# 统计数据
stats_time = []
stats_throughput = []
stats_packet_loss = []

def sender():
    global packets_sent, packets_dropped
    packet_id = 0
    start_time = time.time()
    
    while time.time() - start_time < SIMULATION_TIME:
        current_gen_rate = PACKET_GEN_RATE_START + PACKET_GEN_RATE_INCREMENT * (time.time() - start_time)
        with lock:
            if not forward_buffer.full():
                packet = (packet_id, time.time())
                forward_buffer.put(packet)
                packets_sent += 1
                packet_id += 1
            else:
                packets_dropped += 1
        time.sleep(1 / current_gen_rate)

def forwarder():
    global packets_received
    while time.time() - start_time < SIMULATION_TIME or not forward_buffer.empty():
        try:
            packet = forward_buffer.get(timeout=0.1)
            delay = max(0, random.gauss(DELAY_MEAN, DELAY_STDDEV))
            time.sleep(delay)
            with lock:
                packets_received += 1
        except queue.Empty:
            continue

def receiver():
    print("接收线程启动。")
    while time.time() - start_time < SIMULATION_TIME:
        # 模拟接收处理
        time.sleep(0.01)
    print("接收线程结束。")
    
def collect_stats():
    global stats_time, stats_throughput, stats_packet_loss
    start_time = time.time()
    
    while time.time() - start_time < SIMULATION_TIME:
        with lock:
            current_time = time.time() - start_time
            current_sent = packets_sent
            current_received = packets_received
            current_dropped = packets_dropped
        
        throughput = current_received / current_time if current_time > 0 else 0
        packet_loss = current_dropped / current_sent if current_sent > 0 else 0
        
        stats_time.append(current_time)
        stats_throughput.append(throughput)
        stats_packet_loss.append(packet_loss)
        
        print(f"Time: {current_time:.2f}s, Sent: {current_sent}, Received: {current_received}, Dropped: {current_dropped}")
        
        time.sleep(1)  # 每秒输出一次

# 启动线程
start_time = time.time()
print("开始模拟...")
sender_thread = threading.Thread(target=sender)
forwarder_thread = threading.Thread(target=forwarder)
receiver_thread = threading.Thread(target=receiver)
stats_thread = threading.Thread(target=collect_stats)

sender_thread.start()
forwarder_thread.start()
receiver_thread.start()
stats_thread.start()

# 等待线程结束
sender_thread.join()
forwarder_thread.join()
receiver_thread.join()
stats_thread.join()

# 绘制图形
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(stats_time, stats_throughput)
plt.title('Throughput Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Throughput (packets/s)')

plt.subplot(1, 2, 2)
plt.plot(stats_time, stats_packet_loss)
plt.title('Packet Loss Rate Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Packet Loss Rate')

plt.tight_layout()
plt.show()
