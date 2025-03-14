# test_KNY.py
import serial
import time

# Настройки последовательного порта
SERIAL_PORT = "COM3"  # Замените на ваш порт
SERIAL_BAUD = 9600

try:
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=0.1)
except serial.SerialException as e:
    print(f"Ошибка открытия последовательного порта: {e}")
    exit()

def send_command(command):
    """Отправляет команду на Arduino через последовательный порт."""
    ser.write((command + "#").encode())
    print(f"Отправлено: {command}#")

def receive_data():
    """Принимает данные от Arduino через последовательный порт."""
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        print(f"Получено: {data}")
        return data
    return None

if __name__ == "__main__":
    try:
        while True:
            command = input("Введите команду для отправки (или 'q' для выхода): ")
            if command.lower() == 'q':
                break

            send_command(command)
            time.sleep(0.1)  # Даём время Arduino обработать команду

            data = receive_data()
            if data:
                print(f"Ответ Arduino: {data}")

    except KeyboardInterrupt:
        print("Программа завершена пользователем.")

    finally:
        ser.close()
        print("Последовательный порт закрыт.")
