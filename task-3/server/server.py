import socket
import threading
import os

current_dir = os.getcwd()

def ls(sock):
    path = current_dir
    entries = os.listdir(path)
    for dir in entries:
        sock.send(dir+'/n')
    sock.send('stop')

def cd(sock, path):
    global current_dir
    new_dir = os.path.join(current_dir, path)
    if os.path.isdir(new_dir) != False:
        current_dir = new_dir
        sock.send('Directory changed to ' + new_dir)
    else:
        sock.send('Directory ' + new_dir + ' not found')

def download(sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")

def upload(s):
    filename = s.recv(1024)
    f = open(os.path.join('upload',filename), 'wb')
    s.send("OKK")
    data = s.recv(1024)
    if data[:6] == 'EXISTS':
            filesize = long(data[6:])
    s.send("OK")
    data = s.recv(1024)
    totalRecv = len(data)
    f.write(data)
    while totalRecv < filesize:
        data = s.recv(1024)
        totalRecv += len(data)
        f.write(data)
        print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
    print 'Download Complete! Files are saved in upload folder'
    f.close()

def handleRequest(name, sock):
    while True:
        cmd = sock.recv(1024)
        if "ls" in cmd:
            ls(sock)
        elif "cd" in cmd:
            cd(sock, cmd.split(' ')[1])
        elif 'download' in cmd:
            download(sock)
        elif 'upload' in cmd:
            upload(sock)

def Main():
    host = '127.0.0.1'
    port = 9000

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print "Server Started."
    while True:
        c, addr = s.accept()
        print "client connected ip:<" + str(addr) + ">"
        t = threading.Thread(target=handleRequest, args=("handleRequest", c))
        t.start()
         
    s.close()

if __name__ == '__main__':
    Main()