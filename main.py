# main.py
import socket
import time

# Настройки UDP
UDP_IP = "0.0.0.0"  # IP-адрес КВУ
UDP_PORT_KNU = 6006  # Порт для связи с КНУ
UDP_PORT_KMR = 6000  # Порт для связи с КМР
KMR_IP = "127.0.0.1"

# Создаем сокет UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT_KNU))
sock.settimeout(0.1)

# Создаем сокет для КМР
sock_kmr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Функция отправки команды КМР
def send_command_to_kmr(x, y, z, v):
    command = f"p:{x}:{y}:{z}:{v}#".encode()
    sock_kmr.sendto(command, (KMR_IP, UDP_PORT_KMR))
    print(f"КВУ -> КМР: {command.decode()}")

# Функция для получения данных от КНУ
def receive_from_knu():
    try:
        data, addr = sock.recvfrom(1024)
        message = data.decode().strip()
        print(f"КНУ -> КВУ: {message}")
        return message
    except socket.timeout:
        return None

# Координаты вершин квадрата
square_vertices = [
    (100, 100, 50),
    (200, 100, 50),
    (200, 200, 50),
    (100, 200, 50)
]
current_vertex_index = 0

# Состояние захвата (0 - выкл, 1 - вкл)
grabber_state = 0

# Основной цикл
try:
    while True:
        # Получаем данные от КНУ (кнопка)
        knu_data = receive_from_knu()

        if knu_data and knu_data.startswith("B:"):
            button_state = int(knu_data[2:].replace("#", ""))
            print(f"Состояние кнопки: {button_state}")

            # Обработка нажатия кнопки
            if button_state == 1:
                # Отправляем координаты следующей вершины КМР
                x, y, z = square_vertices[current_vertex_index]
                send_command_to_kmr(x, y, z, grabber_state)
                print(f"Отправка координат: x={x}, y={y}, z={z}")
                current_vertex_index = (current_vertex_index + 1) % len(square_vertices)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Прерывание работы")

finally:
    sock.close()
    sock_kmr.close()
