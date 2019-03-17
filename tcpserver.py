import socket
import threading

bind_ip = '172.16.69.156' #本机IP
bind_port = 4396

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print('[*] Listening on %s:%d' % (bind_ip,bind_port))


def handle_client(client_socket):
	client_socket.send("Connected!".encode())

	request = client_socket.recv(1024)
	
	print('[*] Received: %s' % request)

	client_socket.send("ACK!".encode())
	client_socket.close()

while True:
	client,addr = server.accept()
	print('[*] Accepted connection from: %s:%d' % (addr[0],addr[1]))

	client_handler = threading.Thread(target=handle_client,args=(client,))
	client_handler.start()