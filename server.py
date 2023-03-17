import socket, threading
import sqlite3
import time
import matplotlib.pyplot as plt
import xlsxwriter



#инициализируем порт и адресс сервера
localhost = '192.168.11.119'
port = 2023

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #создаём сокет
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)    #устанавливаем значение опций сокета

server.bind((localhost, port))  #привязываем сокет к адресс

def archiving(dat, fil):

    try:
        fil += '.xlsx'

        workbook = xlsxwriter.Workbook(fil)
        worksheet = workbook.add_worksheet()

        j = -1

        con = sqlite3.connect('drift.db')  # подключаемся к базе данных

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM дрифт")
            rows = cur.fetchall()

            for row in rows:
                if dat[1] == row[4] and dat[2] == row[2] and dat[0] == row[3] and dat[-2] == row[5] and dat[-1] == row[6]:
                    j+=1
                    for i in range(len(row)):
                        worksheet.write(j, i, row[i])
                        #print()

            workbook.close()
            print(f"""Запись завершена в файл {fil}""")

    except:
        print("Такой файл уже существует")
        return


class Schedule():
    def __init__(self, data, time,  db_ag, data2, time2,  db_ag2, angle):
        self.data = data
        self.db_ag = db_ag
        self.angle = angle
        self.time = time
        self.data2 = data2
        self.db_ag2 = db_ag2
        self.time2 = time2

    def reade(self):
        con = sqlite3.connect('drift.db')  # подключаемся к базе данных

        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM дрифт")
            rows = cur.fetchall()


            for row in rows:

                if self.data[1] == row[4] and self.data[2] == row[2] and self.data[0] == row[3] and self.data[-2] == row[5] and row[6] == self.data[-1]:

                    if self.angle.lower() == 'x':
                        self.db_ag.append(row[-3])

                    elif self.angle.lower() == 'y':
                        self.db_ag.append(row[-2])

                    elif self.angle.lower() == 'z':
                        self.db_ag.append(row[-1])

                    self.time.append(float(row[9]))

                if self.data2 != []:

                    if self.data2[1] == row[4] and self.data2[2] == row[2] and self.data2[0] == row[3] and self.data2[-2] == row[5] and row[6] == self.data2[-1]:

                        if self.angle.lower() == 'x':
                            self.db_ag2.append(row[-3])

                        elif self.angle.lower() == 'y':
                            self.db_ag2.append(row[-2])

                        elif self.angle.lower() == 'z':
                            self.db_ag2.append(row[-1])

                        self.time2.append(float(row[9]))
        plot.pl()

    def pl(self):

        fig, ax = plt.subplots()

        for l in range(len(self.time)):
            plt.scatter(self.time[l]-min(self.time), self.db_ag[l], color='red', s=4)

        if self.time2 != []:

            for l in range(len(self.time2)):
                plt.scatter(self.time2[l] - min(self.time2), self.db_ag2[l], color='blue', s=4)
            print("Синий - второй гонщик,\nКрасный - первый")

        plt.xlabel('Время')
        plt.ylabel(f"""угол по оси {agl}""")
        plt.title(f"""График угла по оси {agl} от времени""")
        plt.ylim(0, 100)
        plt.grid(True)
        plt.show()
        pass


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        #print("Новое подключение: ", clientAddress)

    def run(self):
        #print("Подключение с клиента : ", clientAddress)

        conn = sqlite3.connect('drift.db') #подключаемся к базе данных
        cur = conn.cursor() #устанавливаем курсор

        cur.execute("""CREATE TABLE IF NOT EXISTS дрифт(
           'id' INT PRIMARY KEY,
           'Название соревнования' TEXT,
           'дата' TEXT,
           'организатор' TEXT,
           'место' TEXT,
           'номер машины' TEXT,
           'тип заезда' TEXT,
           'время' TEXT,
           'ip устройства' TEXT,
           'время от начала соревнования' TEXT,
           'угол по оси ox' INT,
           'угол по оси oy' INT,
           'угол по оси oz' INT
           );
        """)

        msg = ''

        while True:
            data2 = self.csocket.recv(4096) # получаем сообщение от клиента

            msg = data2.decode()    # декодируем его
            #print(msg.split('/'))

            if msg != """\r\n""":    # если оно не пустое
                data2 = msg.split("/") # разбиваем сообщение
                db = [0]*13
                if msg == '':
                    #print("Отключение")
                    break

                else:

                    #если ip совпадает с необходимым, то заносим его в базу данных
                    if clientAddress[0] == data[-1]:
                        db[0], db[1], db[2], db[3], db[4], db[5], db[6], db[7], db[8], db[9] = int(time.time()*100), data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], time.time() - time_start
                        db[-3] = (data2[0])
                        db[-2] = (data2[1])
                        db[-1] = (data2[2])

                    elif dat != []:
                        db[0], db[1], db[2], db[3], db[4], db[5], db[6], db[7], db[8], db[9] = int(time.time()*100), dat[0], dat[1], dat[2], dat[3], dat[4], dat[5], dat[6], dat[7], time.time() - time_start
                        db[-3] = data2[-1]
                        db[-2] = data2[-2]
                        db[-1] = data2[-3]

                    #print(len(db))
                    if len(set(db)) == 13:
                        try:
                            cur.execute("INSERT INTO дрифт VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", db)
                            conn.commit()
                        except:
                            pass

                cur.close()

            else:
                cur.close()
                return


#запускаем бесконечный цикл, чтобы не перезапускать программу
while True:
    time.sleep(1)
    print("\n1) Добавить соревнование \n2) Построить график\n3) Скачать файл заезда")

    action = input("Действие № ")

    # если добавление заезда, то выполняется код, который написан ниже
    if action == "1":
        print("Данные вводить через '/', Название/Дата/организатор/место/Номер машины/Тип заезда/время")

        data = [(elem) for elem in input("введите данные заезда: ").split('/')]
        data.append(input('ip: '))
        dat = []

        time_limit = int(input("Введите максимальную длительность соревнований в секундах: "))

        ok = input("Парный ли заезд? ")

        # если заезд парный, то добавляется второе устройство, создав индентичный массив
        if ok.lower() == "да":
            dat = [elem for elem in input("введите данные заезда: ").split('/')]
            dat.append(input('ip: '))

        time_start = time.time()    # записываем время начала процесса

        # проверяем правильно ли заполнен массив(ы)
        if (len(dat) == 0 and len(data) == 8) or (len(dat) == 8 and len(data) == 8):

            while time.time()-time_start < time_limit:

                server.listen(1)    # переводим сервер в режим постоянной ожидания подключения
                clientsock, clientAddress = server.accept() # принимаем соединение

                if clientAddress[0] == data[-1] or (dat!= [] and clientAddress[0] == dat[-1]):

                    newthread = ClientThread(clientAddress, clientsock) # создаём объект данного класса (начинаем новый поток)
                    newthread.start() # вызываем его

        else:
            print("Пожалуйста, повторите ввод")

    elif action == "2":

        data = input("Введите для первой машины: организатора/место/дата/номер машины/тип заезда\n").split('/')
        agl = input("Введите ось, по которой построить график: ")
        ok = input("Парный ли заезд?: ")
        data2 =[]

        if ok.lower() == "да":
            data2 = input("Введите для второй машины: организатора/место/дата/номер машины/тип заезда\n").split('/')

        plot = Schedule(data, [], [], data2, [], [], agl)
        plot.reade()

    elif action == "3":
        data = [elem for elem in input("Введите для первой машины: организатора/место/дата/номер машины/тип заезда\n").split('/')]

        if len(data) == 5:
            file = input("Введите название файла: ")
            archiving(data, file)

        else:
            print("Введена не коректная информация")


    else:
        print("Данные не верны. Повторите попытку ввода.")



# b''
