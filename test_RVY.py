import socket
import time

# UDP конфиги
UDP_IP = "0.0.0.0"
UDP_PORT = 6000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.01)
print("Manipulator controller ready")


def process_command(command):
    parts = command[2:-1].split(':')
    x, y, z, v = map(float, parts)
    print(f"Moving to X:{x} Y:{y} Z:{z} | Grabber:{v}")
    # Здесь должна быть логика управления манипулятором
    time.sleep(1) # Имитируем движение
    return "DONE"


# Основной цикл
if __name__ == "__main__":
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            command = data.decode().strip()
            if command.startswith("p:"):
                result = process_command(command)
                sock.sendto(result.encode(), addr)
            else:
                print(f"Unknown command: {command}")
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Error processing command: {e}")
