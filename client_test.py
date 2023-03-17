import os
import platform
import threading
import socket


localhost = '127.0.0.1'
port = 2023

print('Server start. ip:', localhost)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 4)

server.bind(('192.168.118.119', port))


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("Новое подключение: ", clientAddress)

    def run(self):
        msg = ''
        while True:
            if clientAddress in data_cnt:
                data = self.csocket.recv(4096)
                msg = data.decode()
                print(msg)
                if msg == '':
                    print("Отключение")
                    break
                else:
                    print(msg)
                    data = msg.split("/")
                    self.csocket.sendall(bytes(str('srart'), 'UTF-8')) #отправка данных клиенту












def scan_ip_in_WIFI():
    global net, ping_com
    net = getMyIp()
    print('You IP :', net)
    net_split = net.split('.')
    a = '.'
    net = net_split[0] + a + net_split[1] + a + net_split[2] + a
    start_point = int(input("Введите начальный номер: "))
    end_point = int(input("Введите конечный номер: "))

    oc = platform.system()
    if (oc == "Windows"):
        ping_com = "ping -n 1 "
    else:
        ping_com = "ping -c 1 "

    print("Прогресс: ")

    for ip in range(start_point, end_point):
        if ip == int(net_split[3]):
            continue
        potoc = threading.Thread(target=scan_Ip, args=[ip])
        potoc.start()

    potoc.join()

    print("Все ip найдены")


def getMyIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Создаем сокет (UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Настраиваем сокет на BROADCAST вещание.
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def scan_Ip(ip):
    addr = net + str(ip)
    comm = ping_com + addr
    response = os.popen(comm)
    data = response.readlines()
    for line in data:
        if 'TTL' in line:
            print(addr, "Присутствует в сети")
            break


while True:
    server.listen(1)
    func = (input("Действие: "))
    if func == 'scan':
        scan_ip_in_WIFI()
    elif func == 'start':
        race_count = int(input("Введите количество участников: "))
        data_cnt = []
        for _ in range(race_count):
            data_cnt.append([elem for elem in input("номер участника и ip его устройства: ").split('/')])
        type = input("Введите данные о заезде, при вводе используйте / : ")
        print(data_cnt, type)



while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()

    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
