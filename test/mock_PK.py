# mock_PK.py
import time
import socket

# Настройки UDP для имитации отправки данных на КНУ
UDP_IP = "127.0.0.1"  # IP-адрес КНУ
UDP_PORT = 5006  # Порт, который слушает КНУ

# Функция для имитации чтения состояния кнопки
def read_button_state():
    user_input = input("Имитация нажатия кнопки? (y/n): ")
    if user_input.lower() == 'y':
        return 1  # Кнопка нажата
    else:
        return 0  # Кнопка отжата

# Функция для имитации управления светодиодами
def set_leds(led1, led2, led3):
    print(f"Светодиоды: Ожидание={led1}, Завершение={led2}, Запущен={led3}")

# Функция для отправки данных на КНУ (имитация Serial.print)
def send_to_knu(message):
    print(f"ПК (Имитация) -> КНУ: {message}")
    # Отправляем данные на КНУ по UDP (если необходимо)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
    sock.close()

# Основной цикл
if __name__ == "__main__":
    try:
        while True:
            # Имитируем чтение состояния кнопки
            button_state = read_button_state()

            # Отправляем статус кнопки на КНУ
            message = f"B:{button_state}#"
            send_to_knu(message)

            # Управляем светодиодами (вместо Arduino)
            if button_state:
                set_leds(False, False, True)  # Запущен
            else:
                set_leds(True, False, False)  # Ожидание

            time.sleep(1)  # Небольшая задержка
    except KeyboardInterrupt:
        print("Программа завершена.")
