import socket
import random
import csv
import threading
import os
import time
from hashlib import sha256

block = threading.Lock()
LOGGING = True


def hash_passwd(password):
    return sha256(bytes(password, 'utf-8')).hexdigest()


def send_message(sock, data):
    sock.send(data.encode())


def receive_message(sock, zn):
    data = sock.recv(zn).decode()
    return data


socket.socket.send_message = send_message
socket.socket.receive_message = receive_message


def logging(*data):
    data = ' '.join((str(item) for item in data))
    global block, LOGGING
    if LOGGING:
        with block:
            print(data)
            with open("log.txt", 'a+') as file:
                file.write(data + '\n')


logging("Сервер запускается")
sock = socket.socket()
port = 8080

while True:
    try:
        sock.bind(('', port))
        logging(f"Сервер запущен и прослушивает порт {port}")
        break
    except OSError as oserr:
        port = random.randint(1024, 65535)

sock.listen(0)


def listening(conn, addr):
    global users_list, block, history
    login_file = "user_data.csv"
    try:
        with block:
            with open(login_file, 'a+', newline='') as f:
                f.seek(0, 0)
                reader = csv.reader(f, delimiter=';')
                for row in reader:
                    if row[0] == addr[0]:
                        password = row[2]
                        login = row[1]
                        break
                else:
                    conn.send_message("Введите логин: ")
                    login = conn.receive_message(1024)
                    conn.send_message("Введите пароль: ")
                    password = hash_passwd(conn.receive_message(1024))
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow([addr[0], login, password])

        while True:
            conn.send_message("Ваш ip известен серверу. Введите пароль, чтобы начать диалог: ")
            password_inp = conn.receive_message(1024)
            if hash_passwd(password_inp) == password:
                conn.send_message((f"Добро пожаловать {login}"))
                break
            else:
                conn.send_message("Вы ввели неверный пароль")

        while True:
            data = conn.receive_message(1024)
            logging(login, " : ", data)
            with block:
                with open(history, "a+") as file:
                    file.write(login + ": " + data + "\n")
            for conn1 in users_list:
                if conn1 != conn:
                    conn1.send_message(login + ": " + data)
    except:
        users_list.remove(conn)
        raise


def connecting():
    global users_list, CON_FLAG
    while True:
        if CON_FLAG:
            conn, addr = sock.accept()
            logging(f"Подключение клиента {addr[0]}:{addr[1]}")
            users_list.append(conn)
            threading.Thread(target=listening, args=(conn, addr), daemon=True).start()


users_list = []
CON_FLAG = True
history = f"message_log_{time.time()}.txt"
threading.Thread(target=connecting, daemon=True).start()


def show_logs():
    global LOGGING
    LOGGING = True


def hide_logs():
    global LOGGING
    LOGGING = False


def clear_logs():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    with block:
        with open("log.txt", "w"):
            pass


def pause():
    global CON_FLAG
    CON_FLAG = False


def resume():
    global CON_FLAG
    CON_FLAG = True


def clear_login():
    with block:
        with open("logins.csv", "w"):
            pass


def help_menu():
    print(commands.keys())

commands = {
    'выводить логгирование': show_logs,
    'не выводить логгирование': hide_logs,
    'очистить лог': clear_logs,
    'очистить пароли': clear_login,
    'пауза': pause,
    'пуск': resume,
    'help': help_menu,
}

while True:
    text = input()
    if text == "выключить":
        break
    if text in commands.keys():
        commands[text]()
logging("Выключение сервера")