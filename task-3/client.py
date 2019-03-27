import socket
import os
import datetime

def ls(sock):
    x = True
    while x:
        dirs = sock.recv(1024)
        print(dirs)
        if 'stop' in dirs:
            x = False

def cd(sock):
    dir = sock.recv(1024)
    print(dir)
        
def download(s):
    filename = raw_input("Filename? -> ")
    filename = '.\\' + filename
    b = os.path.basename(filename)
    if filename != 'q':
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                foldername = str(datetime.datetime.now())[:19]
                foldername = foldername.replace(':','_')
                os.makedirs(str(foldername))

                s.send("OK")
                f = open(os.path.join(str(foldername),b), 'wb')
                
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                print 'Download Complete! Files are saved in '+str(foldername)+' folder'
                f.close()
        else:
            print "File Does Not Exist!"

def upload(s):
    filename = raw_input("Filename? -> ")
    s.send(filename)
    data = s.recv(1024)
    if 'OKK' in data:
        s.send("EXISTS " + str(os.path.getsize(filename)))
    userResponse = s.recv(1024)
    if userResponse[:2] == 'OK':
        with open(filename, 'rb') as f:
            bytesToSend = f.read(1024)
            s.send(bytesToSend)
            while bytesToSend != "":
                bytesToSend = f.read(1024)
                s.send(bytesToSend)

def Main():
    host = '127.0.0.1'
    port = 9000

    s = socket.socket()
    s.connect((host, port))

    print '---Command---\n1. ls\t\t\t\t: melihat daftar files dan folder pada direktori saat ini\n2. cd\t\t\t\t: pindah direktori\n3. download [direktori_file]\t: download file\n4. upload [nama_file]\t\t: upload file ke server\n5. quit\t\t\t\t: untuk keluar'
    while True:
        cmd = raw_input("Command: ")
        s.send(cmd)
        s.settimeout(3.0)
        if 'ls' in cmd:
            ls(s)
        elif 'cd' in cmd:
            cd(s)
        elif 'download' in cmd:
            download(s)
        elif 'upload' in cmd:
            upload(s)
        elif 'quit' in cmd:
            break

    s.close()  
        
if __name__ == '__main__':
    Main()