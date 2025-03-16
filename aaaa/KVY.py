# import pygame
import serial.tools.list_ports
from time import time
import socket

locaklIP = socket.gethostbyname(socket.gethostname())
locaklIP = "127.0.0.1"
#locaklIP = "192.168.221.107"
localPort = 10000
adr = (locaklIP, localPort)
addressKNY = (locaklIP, 5005)
#addressRob = ("192.168.221.182", 6000) # Определение манипулятора
addressRob = ("127.0.0.1", 6000) # Определение манипулятора
print((locaklIP, localPort))
mainSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mainSocket.settimeout(0.01)
mainSocket.bind(adr)
i_com = -1
i_block = 0
time_move = 0
mainSocket.sendto(b"l:1:0:0#", addressKNY)


class Robot():
    def __init__(self,adr):
        self.adr = adr
        self.x = 210
        self.y = 0
        self.z = 50
        self.newX = 210
        self.newY = 0
        self.newZ = 50
        self.pnev = 0
        self.speed = 10

        self.minR = 120 ** 2
        self.maxR = 350 ** 2
        self.minZ = 20
        self.maxZ = 350


        self.lastMes = ""
        self.timeLastMes = 0
        self.activ = False

    def move(self, x=None, y=None, z=None):
        if x != None:
            x += self.newX
        else:
            x = self.newX
        if y != None:
            y += self.newY
        else:
            y = self.newY
        if z != None:
            z += self.newZ
        else:
            z = self.newZ
        self.moveTo(x, y, z)

    def moveTo(self, x=None, y=None, z=None):
        # print(x,y,z)
        a = lambda x: 1 if x > 0 else -1
        if x != None and y != None:
            if not(self.minR < x ** 2 + y ** 2 < self.maxR):
                if self.minR > x ** 2 + y ** 2:
                    print(73, self.minR, x ** 2 + y ** 2)
                    while self.minR > x ** 2 + y ** 2:
                        x += a(x)
                        y += a(y)
                elif x ** 2 + y ** 2 > self.maxR:
                    while x ** 2 + y ** 2 > self.maxR:
                        x -= a(x)
                        y -= a(y)

        elif x != None:
            if self.minR < x ** 2 + self.y ** 2:
                while not(self.minR < x ** 2 + self.y ** 2):
                    x += 2
            elif x ** 2 + self.y ** 2 < self.maxR:
                while not(x ** 2 + self.y ** 2 < self.maxR):
                    x -= 2
            self.newX = x
        

        elif y != None:
            if self.minR < x ** 2 + self.y ** 2:
                while not(self.minR < self.x ** 2 + y ** 2):
                    y += 2
            elif self.x ** 2 + y ** 2 < self.maxR:
                while not(x ** 2 + self.y ** 2 < self.maxR):
                    y -= 2
            self.newY = y

        if z != None:
            if self.minZ < z < self.maxZ:
                self.newZ = z
        else:
            z = self.z
        self.newX, self.newY, self.newZ = x, y, z
        # print(self.newX, self.newY, self.newZ)

    def zachvat(self, pn=None):
        if pn != None:
            self.pnev = pn
        else:
            self.pnev = [1, 0][self.pnev]

    def update(self):
        st = f"p:{self.newX}:{self.newY}:{self.newZ}:{self.pnev}#"
        # print(st)
        if self.lastMes != st and (time() - self.timeLastMes > 1.5 or self.activ):
            print(st)
            mainSocket.sendto(st.encode(), self.adr)
            self.x = self.newX
            self.y = self.newY
            self.z = self.newZ
            self.lastMes = st
            self.timeLastMes = time()

robot = Robot(addressRob)
# Commands = [0, 0, 0, 0]
t = 1
Commands = [
    [
        {"type": "lamp", "r": 0, "y": 1, "g": 0, "time": 0},

        {"type": "man", "x": 100, "y": 200, "z": 100, "p": 0, "time": t},
        {"type": "man", "x": 100, "y": 200, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 100, "y": 200, "z": 50, "p": 1, "time": t},
        {"type": "man", "x": 100, "y": 200, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 100, "y": 200, "z": 100, "p": 0, "time": t},

        {"type": "lamp", "r": 0, "y": 0, "g": 1, "time": 0}

    ],
    [
        {"type": "lamp", "r": 0, "y": 1, "g": 0, "time": 0},

        {"type": "man", "x": 200, "y": 200, "z": 100, "p": 0, "time": t},
        {"type": "man", "x": 200, "y": 200, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 200, "y": 200, "z": 50, "p": 1, "time": t},
        {"type": "man", "x": 200, "y": 200, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 200, "y": 200, "z": 100, "p": 0, "time": t},

        {"type": "lamp", "r": 0, "y": 0, "g": 1, "time": 0}

    ],
    [
        {"type": "lamp", "r": 0, "y": 1, "g": 0, "time": 0},

        {"type": "man", "x": 200, "y": 100, "z": 100, "p": 0, "time": t},
        {"type": "man", "x": 200, "y": 100, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 200, "y": 100, "z": 50, "p": 1, "time": t},
        {"type": "man", "x": 200, "y": 100, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 200, "y": 100, "z": 100, "p": 0, "time": t},

        {"type": "lamp", "r": 0, "y": 0, "g": 1, "time": 0}

    ],
    [
        {"type": "lamp", "r": 0, "y": 1, "g": 0, "time": 0},


        {"type": "man", "x": 100, "y": 100, "z": 100, "p": 0, "time": t},
        {"type": "man", "x": 100, "y": 100, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 100, "y": 100, "z": 50, "p": 1, "time": t},
        {"type": "man", "x": 100, "y": 100, "z": 50, "p": 0, "time": t},
        {"type": "man", "x": 100, "y": 100, "z": 100, "p": 0, "time": t},

        {"type": "lamp", "r": 1, "y": 0, "g": 0, "time": 0}

    ]
]

butTime = None
RUN = True
while RUN:

    try:
        response, addr = mainSocket.recvfrom(1024)
        response = response.decode()
        if response == "B:1#":
            print("start")
            i_com = 0
            if butTime == None:
                butTime = time()
        elif response == "B:0#":
            if time() - butTime > 1.5:
                RUN = False
            butTime = None
    except:
        pass

    robot.update()
    if i_com != -1:
#        print(1, i_block)
        if i_com == len(Commands[i_block]):
            i_com = -1
            i_block += 1
            if i_block == 4:
                i_block = 0
            print("Complite", i_block)
        elif time() - time_move > 0:
            com = Commands[i_block][i_com]

            if com["type"] == "man":
                robot.moveTo(com["x"], com["y"], com["z"])
                robot.zachvat(com["p"])
            elif com["type"] == "lamp":
                r, g, y = com["r"], com["g"], com["y"]
                st = f"l:{r}:{y}:{g}#"
                print(st)
                mainSocket.sendto(st.encode(), addressKNY)
                # ser.write(st.encode())
            time_move = time() + com["time"]
            i_com += 1
    else:
        pass

