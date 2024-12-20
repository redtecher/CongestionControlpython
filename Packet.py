# -*- coding: UTF-8 -*-
import re

class Packet:

    # 构造器初始化包
    def __init__(self):
        self.seqNo = 1  #包序号  
        self.ACKnum = 0  #确认号   0-收到包有误  1-收到包成功
        self.checksum = 0 #检验和  
        self.payload = ""  #负载
    
    def __str__(self):

        # 包序列格式Packet: seqNo=1, ACKnum=0, checksum=0, payload=0
        return f"Packet: seqNo={self.seqNo}, ACKnum={self.ACKnum}, checksum={self.checksum}, payload={self.payload}"

    def createPacket(self,input_Content,input_seqNo):
        self.payload = input_Content
        self.seqNo = input_seqNo
        self.checksum = self.generateChecksum(self.payload)     
        return True                                

    # 帮助发送者生成统一格式的信息
    def generateMessage(self):
        return f"Packet: seqNo={self.seqNo}, ACKnum={self.ACKnum}, checksum={self.checksum}, payload={self.payload}"

    #生成检验和的函数，原本算法就是将前面3个16位相加，但是这里没有源端口和目的端口
    #因此，我们对发送的信息做一个处理，将其转换为ascii码作为检验和
    def generateChecksum(self,s):
        sum = 0
        # print(s)
        for i in range(0,len(s)):
            asciiInt  = ord(s[i])
            sum = sum+asciiInt
        # print('\n')
        return sum
    
    def onACK(self):
        pass 
    

    def onNAK(self):
        pass

    #这个方法是帮助接收者解析从套接字获取的data
    def parseMessage(self,pContent):
        pattern_seqNo = r'Packet: seqNo=(\d+),'
        pattern_ACKnum = r'ACKnum=(\d+)'
        pattern_checksum =r'checksum=(\d+)'
        pattern_payload = r'payload=(.+)'
        if(re.findall(pattern_seqNo,pContent)!=[]):
            self.seqNo =int(re.findall(pattern_seqNo,pContent)[0])

        else:
            print("seqNo is not matching in re")

        if(re.findall(pattern_ACKnum,pContent)!=[]):
            self.ACKnum = int(re.findall(pattern_ACKnum,pContent)[0])
        else:
            print("ACKnum is not matching in re")

        if(re.findall(pattern_checksum,pContent)!=[]):
            self.checksum =  int(re.findall(pattern_checksum,pContent)[0])
        else:
            print("checksum is not matching in re")

        if(re.findall(pattern_payload,pContent)!=[]):
            self.payload = re.findall(pattern_payload,pContent)[0]
        else:
            print("payload is not matching in re")
        return True


    #模拟包出错，可以将checksum+1
    def corruptChecksum(self):
        self.checksum = self.checksum + 1


    #个方法是帮助接收者判断包裹的信息是否出错的，也就是将计算得到的checksum和发送来的checksum作比较
    def validateMessage(self):
        validate_sum = 0
        for i in range(0,len(self.payload)):
            asciiInt  = ord(self.payload[i])
            # print(ord(self.payload[i]),end=' ')
            validate_sum = validate_sum+asciiInt
        
        if validate_sum == self.checksum:
            return True
        else:
            return False

        