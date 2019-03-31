from scapy.all import *
from scapy.layers.inet import TCP, IP


# 回调函数
def packet_callback(packet):
    print packet.show()

# 开启嗅探器
sniff(prn=packet_callback,count=1)
