import socket
import threading

bind_ip = '127.0.0.1' #本机IP
bind_port = 7776

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

#开始监听TCP传入连接，括号中的5表示tcp连接队列的大小，即连接数
server.listen(5)

print('[*] Listening on %s:%d' % (bind_ip,bind_port))

#客户处理线程
def handle_client(client_socket):
	client_socket.send("private".encode(encoding='utf-8'))
        #打印客户端发送得到的内容
	request = client_socket.recv(1024)
	
	print('[*] Received: %s' % request)
        
        #返还一个数据包
	client_socket.send("ACK!".encode())
	client_socket.close()

while True:
	client,addr = server.accept()
	print('[*] Accepted connection from: %s:%d' % (addr[0],addr[1]))

        #挂起客户端线程，处理传入的数据
	client_handler = threading.Thread(target=handle_client,args=(client,))
	client_handler.start()
