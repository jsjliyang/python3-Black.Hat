import socket
target_host = "192.168.11.131" #本机IP
target_port = 7776

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((target_host,target_port))

#client.send("GET / HTTP/1.1\r\nHost:baidu.com\r\n\r\n".encode())
client.send("aaaaaacccc".encode())

response = client.recv(4096).decode('utf-8')

print(response)