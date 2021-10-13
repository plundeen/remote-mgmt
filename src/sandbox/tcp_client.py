import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 7005
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT))

while 1:
    data = s.recv(BUFFER_SIZE)
    if not data: break
    print ('received data: ', data)

s.close()