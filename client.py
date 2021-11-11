import socket, threading


def send_message(sock, data):
    sock.send(data.encode())


def receive_message(sock, zn):
    data = sock.recv(zn).decode()
    return data


socket.socket.send_message = send_message
socket.socket.receive_message = receive_message


def recieving():
    while True:
        data = sock.receive_message(1024)
        with block:
            print(data)


block = threading.Lock()
sock = socket.socket()
sock.setblocking(1)

port_inp = int(input('Введите порт: '))
host, port = 'localhost', port_inp
print(f"Подключение к порту {port}")
sock.connect((host, port))
print("Успешно подключено к серверу")

threading.Thread(target = recieving, daemon = True).start()
while True:
    msg = input()
    sock.send_message(msg)
    if msg == "exit":
        break

print("Отключение от сервера")
sock.close()