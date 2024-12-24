import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.optimize import curve_fit
matplotlib.use('Qt5Agg')
class Data_Analyse:

    def __init__(self,lamuda_in=[],lamda_out=[]):
        self.x = lamuda_in
        self.y = lamda_out
    
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
        
        # plt.plot(self.x, self.y)
        coefficients = np.polyfit(self.x, self.x, 1)
        # fit_line = np.polyval(coefficients, self.x)
        plt.scatter(self.x, self.y, color='red',label='data point')
        # 添加标题和标签
        # plt.plot(self.x, fit_line, label='拟合曲线', color='blue')
        plt.title('λin-λout Chart')
        plt.xlabel('λin(bytes/s)')
        plt.ylabel('λout(bytes/s)')
        plt.legend()
        # 显示图表
        plt.show()


    def calculate_average(self,temp_list):
        sum = 0
        for i in range(len(temp_list)):
            sum =sum + temp_list[i]
        return round(sum/len(temp_list),2)


    def generate_data(self):
        receive_temp =[]
        sent_temp = []
        
        content = self.read_file("no_cc_data_record.txt")
        splited = content.split("\n")
        pattern_received = r'Send Rate (\d+):Received'
        pattern_sent = r'Send Rate (\d+):Sent'
        throughput =r'throughput: (\d*\.\d+|\d+) bytes/second' 
        for i in range(len(splited)):
            if(re.findall(pattern_received,splited[i])!=[]):
                # print(re.findall(throughput,splited[i]))
                receive_temp.append(round(float(re.findall(throughput,splited[i])[0]),2))
            elif(re.findall(pattern_sent,splited[i])!=[]):
                    sent_temp.append(round(float(re.findall(throughput,splited[i])[0]),2))
            else:
                pass  
            if(len(receive_temp)==2):
                self.y.append(self.calculate_average(receive_temp))
                receive_temp=[]
            if(len(sent_temp)==2):
                self.x.append(self.calculate_average(sent_temp))   
                sent_temp=[]


        print(len(self.x))
        print(len(self.y))



if __name__=='__main__':
    da = Data_Analyse()
    da.generate_data()
    da.plot_pic()

