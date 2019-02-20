import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_server = 'localhost'
port_server = 10000
server_address = (ip_server, port_server)
print >>sys.stderr, 'Connecting to %s port %s' % server_address

sock.connect(server_address)

try:
    message = raw_input("Enter message : ")
    print >>sys.stderr, 'Sending "%s"' % message
    sock.sendall(message)
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'Received "%s"' % data
finally:
    print >>sys.stderr, 'Closing socket...'
    sock.close()