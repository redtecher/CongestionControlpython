# -*- coding: UTF-8 -*-
import Packet
import Client
import chardet
if __name__=='__main__':
    with open('in.txt', 'rb') as f:
        result = chardet.detect(f.read())  # 读取一定量的数据进行编码检测
    print(result['encoding'])  # 打印检测到的编码

    

    


