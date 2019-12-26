import socket
import threading
port = 9090


def received_mes(conn):
    while True:
        try:
            print(conn.recv(512).decode())
        except Exception:
            break


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('localhost', port))
name = input("Welcome to our best tcp chat! What is your name?\n")
if name:
    conn.send(name.encode())

threading.Thread(target=received_mes, args=(conn,)).start()

while True:
    data = input()
    if data == 'quit':
        conn.send(data.encode())
        conn.close()
        break
    conn.send(data.encode())
