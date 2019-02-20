import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_server = 'localhost'
port_server = 10000
server_address = (ip_server, port_server)
print >>sys.stderr, 'Starting up on %s port %s' % server_address

sock.bind(server_address)
sock.listen(1)

while True:
	print >>sys.stderr, 'Waiting for a connection...'
	connection, client_address = sock.accept()
	print >>sys.stderr, 'Connection from', client_address
	while True:
		data = connection.recv(32)
		print >>sys.stderr, 'Received "%s"' % data
		if data:
			print >>sys.stderr, 'Sending data back to the client'
			connection.sendall(data)
		else:
			print >>sys.stderr, 'No more data received from', client_address
			break
	connection.close()