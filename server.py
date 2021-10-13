import socket
from _thread import *

sock = socket.socket()
host = '127.0.0.1'
port = 9090
conn_amount = 0
try:
    sock.bind((host, port))
except socket.error as e:
    print(e)

print('[sever] socket is listening..')
sock.listen(5)


def connection_thread(conn, addr):
    conn.send(str.encode('Server is working:'))
    while True:
        data = conn.recv(1024)
        response = f"[server] receieved '{data.decode()}'"
        print(f"[{addr}] {data}")
        if not data:
            break
        conn.sendall(str.encode(response))
    conn.close()


while True:
    conn, addr = sock.accept()
    print('[server] new connection: ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(connection_thread, (conn, addr))
    conn_amount += 1
    print('[server] connected clients: ' + str(conn_amount))
sock.close()
