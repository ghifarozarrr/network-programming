import socket
import os
import datetime

host = '127.0.0.1'
port = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Type "ready" to start receiving images from server'
def makeFolder():
    #This function is used for making a new folder to store image files from server
    #Timestamp is used as the folder name
    now = str(datetime.datetime.now())[:19]
    now = now.replace(":","_")
    os.makedirs(str(now))
    return now

while True:
    try:
        msg = raw_input("Message: ")
        sock.sendto(msg,(host, port))
        if 'ready' in msg:        
            foldername = makeFolder()
            while True:
                data, addr = sock.recvfrom(1024)
                if 'Start sending' in data:
                    fileSize = long(data[26:])
                    totalRecv = 0
                    f = open(os.path.join(str(foldername),str(data[14:26])), 'wb')
                    print 'Start receiving '+ str(data[14:26] + ' ' + str(data[26:]+' bytes'))
                elif 'Finish sending' in data:
                    print 'Finish receiving '+ str(data[14:26])
                    f.close()
                elif 'All files are sent' in data:
                    break
                else:
                    f.write(data)
                    totalRecv = totalRecv + len(data)
                    if totalRecv%1024==0:
                        print '{}/{} bytes'.format(totalRecv, fileSize)

            print "Download Complete! Files are saved in "+str(foldername)+" folder"
            break
        else:
            data, addr = sock.recvfrom(1024)
            print data
    except:
        print 'Server is down'