import socket

sock = socket.socket()
host = '127.0.0.1'
port = 9090

try:
    sock.connect((host, port))
except socket.error as e:
    print(str(e))

res = sock.recv(1024)
while True:
    mes = input('Type your message here: ')
    sock.send(str.encode(mes))
    res = sock.recv(1024)
    print(res.decode())
sock.close()
