import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

while True:
    data, addr = sock.recvfrom(1024) #buffer size 1024
    print 'Diterima', data
    print 'Dikirim oleh ', addr