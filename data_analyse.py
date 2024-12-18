import matplotlib
import matplotlib.pyplot as plt
import numpy
matplotlib.use('Qt5Agg')
class Data_Analyse():

    def __init__(self,send_rate:list,bandwidth:list):
        self.send_rate = send_rate
        self.bandwidth = bandwidth
    

    def plot_pic(self):
        # 绘制折线图
        plt.plot(self.send_rate, self.bandwidth)

        # 添加标题和标签
        plt.title('Simple Line Chart')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')

        # 显示图表
        plt.show()

if __name__=='__main__':
    da =Data_Analyse([1, 2, 3, 4, 5],[1, 4, 9, 16, 25])
    da.plot_pic()

