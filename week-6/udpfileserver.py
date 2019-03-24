import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
FILENAME = 'data.out'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

fp = open(FILENAME, 'wb+')
ditulis = 0

while True:
    data, addr = sock.recvfrom(1024) #buffer size 1024
    print 'Blok ', len(data), data[0:10]
    fp.write(data)

fp.close()