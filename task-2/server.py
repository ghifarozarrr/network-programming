import socket
import threading
import os

host = '127.0.0.1'
port = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host,port))

print 'Server is running'

def sendImage(data, addr):
    images = ['gambar-1.png','gambar-2.png','gambar-3.png', 'gambar-4.png','gambar-5.png']
    if 'ready' in data:
        for filename in images:
            sock.sendto("Start sending " + str(filename) + str(os.path.getsize(filename)), addr)
            f = open(filename, 'rb')
            imageBytes = f.read()
            for i in imageBytes:
                sock.sendto(i, (addr))
            sock.sendto('Finish sending' + str(filename), addr)
        sock.sendto('All files are sent', addr)
    else:
        sock.sendto('Type "ready" to start receiving images from server', addr)

while True:
    data, addr = sock.recvfrom(1024)
    print 'Client connected, ip: ' + str(addr)
    #thread is used for handling multiple clients at the same time
    thread = threading.Thread(target=sendImage, args=(data, addr))
    thread.start()
     
sock.close()