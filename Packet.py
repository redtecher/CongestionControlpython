class Packet:

    # 构造器初始化包
    def __init__(self):
        self.seqNo = 1
        self.ACKnum = 0
        self.checksum = 0
        self.payload = ""
    
    #这个方法教给发送者调用，可以将读取的信息封装到 packet当中
    def createPacket(self,input_Content,input_seqNo):
        self.payload = input_Content
        self.seqNo = input_seqNo
        self.checksum = self.generateChecksum(self.payload)     
        return True                                

    # 帮助发送者生成统一格式的信息
    def generateMessage(self):
        return self.seqNo+""+self.checksum+""+self.payload;

    #生成检验和的函数，原本算法就是将前面3个16位相加，但是这里没有源端口和目的端口
    #因此，我们对发送的信息做一个处理，将其转换为ascii码作为检验和
    def generateChecksum():
        pass

    #这个方法是帮助接收者解析从套接字获取的data
    def parseMessage():
        pass

    #模拟包出错，可以将checksum+1
    def corruptChecksum():
        pass

    #个方法是帮助接收者判断包裹的信息是否出错的，也就是将计算得到的checksum和发送来的checksum作比较
    def validateMessage():
        pass

        