# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = ''
    while True:
        data = s.recv(1024).decode('utf-8')
        print("Received", data)
        if data == 'Perdiste':
            break
        print("Escribe la accion:")
        entrada = input()
        s.sendall(bytearray(entrada.encode('utf-8')))
    s.close()