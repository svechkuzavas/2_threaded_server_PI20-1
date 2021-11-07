import socket
import sys
import threading
import queue

socket.setdefaulttimeout(0.01)


class ScanningThread(threading.Thread):
    def __init__(self, t_num, ip):
        threading.Thread.__init__(self, name=f"thread_{t_num}")
        self.t_num = t_num
        self.ip = ip

    def run(self):
        global scanned_data
        while True:
            try:
                scanning_port = q.get_nowait()
                sock = socket.socket()
                try:
                    sock.connect((self.ip, scanning_port))
                    with threading.Lock():
                        scanned_data.append(scanning_port)
                except ConnectionRefusedError:
                    continue
                except socket.timeout:
                    continue
                finally:
                    # it's necessary to close connection
                    sock.close()
                    q.task_done()
            except queue.Empty:
                # leaving loop when all ports are checked
                break


class PortScanner:
    def __init__(self, ip, thread_amount):
        self.ip = ip
        self.add_to_queue()
        # starting scanning
        for i in range(thread_amount):
            thr = ScanningThread(i, self.ip)
            thr.start()

        progress_bar = ProgressBar(range(N + 1), 50)
        for i in progress_bar.process():
            while (N - q.unfinished_tasks) < i:
                continue
        print(self)

    def add_to_queue(self):
        for new_port in range(1, N+1):
            q.put(new_port)

    def __str__(self):
        return 'Свободные порты:\n'+'\n'.join([str(port) for port in scanned_data])


class ProgressBar:
    def __init__(self, seq, size):
        self.seq = seq
        self.size = size

    def show(self, n):
        complete = int(self.size * n / len(self.seq))
        percent = round(n / len(self.seq) * 100, 0)
        sys.stdout.write(f"[{'*'*complete}{' '*(self.size-complete)}] {percent}/100%\r")
        sys.stdout.flush()

    def process(self):
        self.show(0)
        for i, item in enumerate(self.seq):
            yield item
            self.show(i + 1)
        sys.stdout.write("\n")
        sys.stdout.flush()


if __name__ == '__main__':
    N = 2 ** 16 - 1
    scanned_data = []
    q = queue.Queue()
    ip = str(input('Введите ipv4 адрес для сканирования(127.0.0.1): '))
    ports_n = int(input('Введите количество сканирующих потоков: '))
    scnnr = PortScanner(ip, ports_n)