import socket
import os

# 监听的主机
host = "172.16.69.62"

# 创建一个原始套接字，然后绑定在公开接口上
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol) 

sniffer.bind((host,0))

# 设置在捕获的数据包中包含IP头
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# 在Windows平台上，需要设置IOCTL以启用混杂模式
if os.name == "nt": 
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# 读取单个数据包
print(sniffer.recvfrom(65565))

# 在Windows平台下关闭混杂模式
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

