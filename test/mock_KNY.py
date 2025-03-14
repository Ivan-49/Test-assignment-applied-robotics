# mock_KNY.py
import socket
import time

# Настройки UDP
UDP_IP = "127.0.0.1"  # IP-адрес КНУ
UDP_PORT = 5006  # Порт для прослушивания
KVU_IP = "127.0.0.1"  # IP-адрес КВУ
KVU_PORT = 6006  # Порт для отправки данных на КВУ

# Создаем сокет для приема данных
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.1)

def send_to_kvu(message):
    sock_to_kvu = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_to_kvu.sendto(message.encode(), (KVU_IP, KVU_PORT))
    sock_to_kvu.close()
    print(f"КНУ (Имитация) -> КВУ: {message}")

def receive_from_pk():
    try:
        print("Ожидание данных от ПК...")
        data, addr = sock.recvfrom(1024)
        message = data.decode().strip()
        print(f"Получено от ПК: {message}")
        return message
    except socket.timeout:
        print("Timeout: Нет данных от ПК.")
        return None

# Основной цикл
if __name__ == "__main__":
    try:
        while True:
            # Принимаем данные от ПК
            pk_data = receive_from_pk()

            if pk_data:
                # Отправляем данные КВУ
                send_to_kvu(pk_data)

            # Даем время другим процессам
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Программа завершена.")
    finally:
        sock.close()
        print("Сокет закрыт.")
