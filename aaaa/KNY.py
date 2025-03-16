import serial.tools.list_ports
import serial
import socket
import time

ports = list(serial.tools.list_ports.comports())
for iport in ports:
    print(f"\tПорт: {iport.device}")
    print(f"\tОписание: {iport.description}")
    print(f"\tПроизводитель: {iport.manufacturer}\n")
    port = iport.device

baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=0.1)

UDP_IP = "127.0.0.1"
#UDP_IP = "192.168.221.107"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
adr = (UDP_IP, UDP_PORT)
addressKVY = (UDP_IP, 10000)
sock.settimeout(0.01)
sock.bind(adr)

def send_udp(state):
    sock.sendto(state.encode(), addressKVY)


def set_led(state):
    states = [
        b'SET_LED:1:1:0:0',
        b'SET_LED:3:0:0:1',
        b'SET_LED:2:0:1:0'
    ]
    ser.write(states[state] + b'\n')


prev_state = 0
current_state = 0

while True:
    response = ser.readline().decode('utf-8', "ignore")[:4]
    send_udp(response)
    if response != "":
        print(response)
    try:
        data, addr = sock.recvfrom(1024)
        if data.decode() != "":
            print(data)
        ser.write(data)
    except:
        pass

