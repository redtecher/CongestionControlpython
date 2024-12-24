

# CongestionControl

用Python复现网络拥塞现象，并实现拥塞控制算法控制网络拥塞。

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/redtecher/CongestionControlpython/">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">CongestionControl</h3>
  <p align="center">
    一个用mininet复现网络拥塞的项目
    <br />
    <a href="https://github.com/redtecher/CongestionControlpython"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/redtecher/CongestionControlpython/issues">报告Bug</a>
    ·
    <a href="https://github.com/redtecher/CongestionControlpython/issues">提出新特性</a>
  </p>

</p>
 
## 目录

- [上手指南](#上手指南)
  - [开发前的配置要求](#开发前的配置要求)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [开发的架构](#开发的架构)
- [部署](#部署)
- [使用到的框架](#使用到的框架)
- [贡献者](#贡献者)
  - [如何参与开源项目](#如何参与开源项目)
- [版本控制](#版本控制)
- [作者](#作者)
- [鸣谢](#鸣谢)




### 文件目录说明
eg:

```
filetree 
├── Client.py                   # 初始用socket实现的Client类
├── Server.py                   # 初始用socket实现的Server类
├── LICENSE.txt                 #  LICENSE.txt文件
├── README.md                   #  Readme文件
├── CongestionControl.py        # 拥塞控制类
├── Test.py                     # 测试文件
├── /images/
│  ├── 拓扑图.jpg                #死锁复现网络拓扑图
│  ├── logo.png                 #项目logo
│  ├── topo2.jpg                #实验拓扑图
├── data_analyse_conges_data.py #拥塞控制后分析吞吐量并绘制图表
├── data_analyse_congestion.py  #拥塞控制后分析cnwd并绘制图表
├── data_analyse.py             #拥塞控制前分析吞吐量并绘制图表 复现拥塞
├── mininetSocketTest.py        #mininet内使用socket编程测试文件
├── Packet.py                   #可靠传输协议Packet类的实现
├── topo_congescontrol.py       #使用了拥塞控制的mininet模拟及运行文件，生成数据
├── topo_nocontrol.py           #没有拥塞控制下的mininet模拟及运行文件，复现网络拥塞
├── topo.mn                     #mininet下miniedit生成的拓扑图
├── topo.py                     #最简单的拓扑模拟
├── UDPClient.py                #异步并发的客户端实现
├── UDPServer.py                #异步并发的服务端端实现
├── data_record.txt             #每10秒记录吞吐率数据
├── in.txt                      #输入的文章
├── log.txt                     #记录线程情况
├── logclient.txt               #客户端发包收包记录
├── logserver.txt               #客户端接受包及发送包记录
├── no_cc_data_record.txt       #没有拥塞控制的一次数据记录
```

### 运行

```

Python3 topo2.py

```





#### 如何参与开源项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

### 作者

洪川/Redtecher 

### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE.txt](https://github.com/shaojintian/Best_README_template/blob/master/LICENSE.txt)



<!-- links -->
[your-project-path]:shaojintian/Best_README_template
[contributors-shield]: https://img.shields.io/github/contributors/shaojintian/Best_README_template.svg?style=flat-square
[contributors-url]: https://github.com/shaojintian/Best_README_template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/shaojintian/Best_README_template.svg?style=flat-square
[forks-url]: https://github.com/shaojintian/Best_README_template/network/members
[stars-shield]: https://img.shields.io/github/stars/shaojintian/Best_README_template.svg?style=flat-square
[stars-url]: https://github.com/shaojintian/Best_README_template/stargazers
[issues-shield]: https://img.shields.io/github/issues/shaojintian/Best_README_template.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/shaojintian/Best_README_template.svg
[license-shield]: https://img.shields.io/github/license/shaojintian/Best_README_template.svg?style=flat-square
[license-url]: https://github.com/shaojintian/Best_README_template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/shaojintian




