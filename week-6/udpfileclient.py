import socket
import os

TARGET_IP = '127.0.0.1'
TARGET_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

filename = 'pic-' + str(1) + '.png'
ukuran = os.stat(filename).st_size

fp = open(filename, 'rb')
k = fp.read()
terkirim = 0
#untuk tugas sock.sendto('--awal--{}--'.format(namafile),(targetip, targetserver),
for i in k:
	sock.sendto(i, (TARGET_IP, TARGET_PORT))
	terkirim = terkirim + 1
	print '\r terkirim {} dari {} '.format(terkirim, ukuran)
#untuk tugas sock.sendto('akhir')