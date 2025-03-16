# mrc_controller
import socket

# UDP Configuration
UDP_IP = "0.0.0.0"
UDP_PORT = 6000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Manipulator controller ready")

while True:
    data, addr = sock.recvfrom(1024)
    command = data.decode().strip()
    if command.startswith("p:"):
        parts = command[2:-1].split(':')
       # print(parts)
        x, y, z, v = parts 
        print(f"Moving to X:{x} Y:{y} Z:{z} | Grabber:{v}")
        sock.sendto(b"DONE", addr)
