import socket
target_host = "172.16.69.156" #本机IP
target_port = 4396

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#client.connect((target_host,target_port))

client.sendto("AAABBBCCC".encode(),(target_host, target_port))

data,addr = client.recvfrom(4096)

print(data)