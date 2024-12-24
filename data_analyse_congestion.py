import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.optimize import curve_fit
matplotlib.use('Qt5Agg')
class Data_Analyse:

    def __init__(self,lamuda_in=[],lamda_out=[]):
        self.x1 = []
        self.y1 = []
        self.x3 = []
        self.y3 = []
    
    def read_file(self,filename):
        # 打开文件
        encoding='utf-8'
        # with open(filename, 'r',encoding=encoding,errors='replace') as file:
        with open(filename, 'r',encoding=encoding) as file:
            # 读取文件内容
            content = file.read()
            return content

    def plot_pic(self):
        # 绘制折线图
        plt.plot(self.x1, self.y1, label='h1')
        plt.plot(self.x3, self.y3, label='h3')
        # 添加标题和标签
        plt.title('CNWD-Times Chart')
        plt.xlabel('Times')
        plt.ylabel('CNWD')
        plt.legend()
        # 显示图表
        plt.show()


    def generate_data(self):
        
        content = self.read_file("congestion_record.txt")
        splited = content.split("\n")
        pattern_host = r'congestion_record - INFO - h(\d+):'
        cnwd_pattern = r'times CWND: (\d+\.\d+)'
        times_pattern = r':(\d+) times'
        for i in range(len(splited)):
            if(re.findall(pattern_host,splited[i])!=[]):
                host = re.findall(pattern_host,splited[i])[0]
            else:
                print("pattern error")
            if(re.findall(cnwd_pattern,splited[i])!=[]):
                print(re.findall(cnwd_pattern,splited[i])[0])
                cnwd = round(float(re.findall(cnwd_pattern,splited[i])[0]),2)
            else:
                print("cnwd error")
            if(re.findall(times_pattern,splited[i])!=[]):
                times = int(re.findall(times_pattern,splited[i])[0])
            else:
                print("times error")
            if(host == '1'):
                self.x1.append(times)
                self.y1.append(cnwd)
            elif(host == '3'):
                self.x3.append(times)
                self.y3.append(cnwd)



if __name__=='__main__':
    da = Data_Analyse()
    da.generate_data()
    da.plot_pic()

