import socket
target_host = "127.0.0.1" #本机IP
target_port = 7776 #连接端口号

#建立一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#连接客户端
client.connect((target_host,target_port))

#发送一些数据
#client.send("GET / HTTP/1.1\r\nHost:baidu.com\r\n\r\n".encode())
client.send("aaaaaacccc".encode())

#接收一些数据并打印出来
response = client.recv(4096).decode('utf-8') #client.recv括号里面是buffer size

print(response)
