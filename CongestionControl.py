# -*- coding: UTF-8 -*-
# 拥塞控制
class CongestionControl:
    def __init__(self, initial_cwnd=1, max_cwnd=1000, ssthresh=64):
        self.cwnd = initial_cwnd  # 拥塞窗口
        self.ssthresh = ssthresh  # 慢启动阈值
        self.max_cwnd = max_cwnd  # 最大拥塞窗口大小
        self.duplicate_acks = 0   # 重复ACK计数器

    def on_ack(self, acked_packets):
        if self.cwnd < self.ssthresh:
            # 慢启动，每收到一个ACK，拥塞窗口增加1
            self.cwnd += acked_packets
            # logger.info(f"慢启动状态，cwnd变为: {self.cwnd}")
        else:
            # 拥塞避免阶段，每收到一个ACK，拥塞窗口增加1/cwnd
            self.cwnd += acked_packets / self.cwnd
            # logger.info(f"拥塞避免状态，cwnd变为: {self.cwnd}")

        self.cwnd = min(self.cwnd, self.max_cwnd)
        self.duplicate_acks = 0
        
    def on_duplicate_ack(self):
        self.duplicate_acks += 1
        if self.duplicate_acks == 3:
            # 快速重传
            self.ssthresh = max(self.cwnd / 2, 1)
            self.cwnd = self.ssthresh
            self.duplicate_acks = 0

    def on_timeout(self):
        # 超时进入慢启动
        self.ssthresh = max(self.cwnd / 2, 1)
        self.cwnd = 1
        self.duplicate_acks = 0
        # logger.info(f"慢启动状态开始，cwnd变为: {self.cwnd}")

    def get_send_rate(self):
        # 根据cwnd计算发送速率
        return self.cwnd
    
    
