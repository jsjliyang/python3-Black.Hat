import socket
import os
import struct
import threading
import time

from netaddr import IPNetwork,IPAddress
from ctypes import *

# 监听的主机
host   = "172.16.69.62"

# 扫描的目标子网
subnet = "172.16.69.0/24"

# 自定义的字符串，将在ICMP响应中进行核对
magic_message = "PYTHONRULES!"

# 批量发送UDP数据包
def udp_sender(subnet,magic_message):

    time.sleep(5)
    sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    for ip in IPNetwork(subnet):

        try:
            sender.sendto(bytes (magic_message,encoding="utf-8"),(str(ip),65212))
        except:
            print("error")
            #pass

class IP(Structure):
    
    _fields_ = [
        ("ihl",           c_ubyte, 4),
        ("version",       c_ubyte, 4),
        ("tos",           c_ubyte),
        ("len",           c_ushort),
        ("id",            c_ushort),
        ("offset",        c_ushort),
        ("ttl",           c_ubyte),
        ("protocol_num",  c_ubyte),
        ("sum",           c_ushort),
        ("src",           c_ulong),
        ("dst",           c_ulong)
    ]
    
    def __new__(self, socket_buffer=None):
            return self.from_buffer_copy(socket_buffer)    
        
    def __init__(self, socket_buffer=None):

        # 协议字段与协议名称对应
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
        
        # 可读性更强的IP地址
        self.src_address = socket.inet_ntoa(struct.pack("<f",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<f",self.dst))
    
        # 可读性更强的协议类型
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
            


class ICMP(Structure):
    
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)
        ]
    
    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)    

    def __init__(self, socket_buffer):
        pass

# 创建一个原始套接字，然后绑定在公开接口上
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP 
else:
    socket_protocol = socket.IPPROTO_ICMP
    
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# 设置在不活的数据包中包含IP头
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# 在Windows平台上，需要设置IOCTL以启用混杂模式
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# 开始发送数据包
t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()

try:
    while True:
        
        # 读取数据包
        raw_buffer = sniffer.recvfrom(65565)[0]
        
        # 将缓冲区的前32个字节按照IP头进行解析
        ip_header = IP(raw_buffer[0:32])
      
        print ("Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
    
        # 如果为ICMP，进行处理
        if ip_header.protocol == "ICMP":
            
            # 计算ICMP包的起始位置
            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + sizeof(ICMP)]
            
            # 解析ICMP数据
            icmp_header = ICMP(buf)
            
            #print ("ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code))

            # 检查类型和代码值是否为3
            if icmp_header.code == 3 and icmp_header.type == 3:

                # 确认响应的主机在目标子网之内
                if IPAddress(ip_header.src_address) in IPNetwork(subnet):

                    #确认ICMP数据中包含我们发送的自定义的字符串
                    if str(raw_buffer[len(raw_buffer)-len(magic_message):])[2:-1] == magic_message:
                        print("Host Up: %s" % ip_header.src_address)
            
# handle CTRL-C
except KeyboardInterrupt:
    # 在Windows平台下关闭混杂模式
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

