import socket
import threading

users = {}
port = 9090
help_text = """
==
users - show online users
to_user hi man - send direct to "user" with "hi man" message
help - show this help text if you forget something
quit - exit from chat
=="""


def handle_client(client, addr):
    name = client.recv(512).decode()
    new_user_mess = name + " connected to chat"
    print(new_user_mess)
    if addr not in users:
        users[addr] = {}
        users[addr]['client'] = client
        users[addr]['name'] = name
        # RKN Watching You
        users[addr]['messages'] = []
        client.send(b"Hello, " + name.encode() + b'!')
        client.send(b" Here is a commands you can run:" + help_text.encode())
        for user in users:
            if user != addr:
                users[user]['client'].send(new_user_mess.encode())

    while True:
        data = client.recv(512).decode().strip()
        # RKN Watching You
        users[addr]['messages'].append(data)
        if data == 'quit':
            client.close()
            print("Client quits", addr)
            for user in users:
                if user != addr:
                    mess = users[addr]['name'] + ' exit chat'
                    users[user]['client'].send(mess.encode())
            users.pop(addr)
            return None
        elif data == 'help':
            users[addr]['client'].send(help_text.encode())
        elif data == 'users':
            mess = '\n'.join(user['name'] for user in users.values())
            users[addr]['client'].send(b'==\n' + mess.encode() + b'\n==')
        elif data.startswith('to_'):
            name = data.split()[0][3:]
            to_addr = [k for k, v in users.items() if v['name'] == name]
            if to_addr:
                mess = users[addr]['name'] + "(private): " + \
                    ' '.join(data.split()[1:])
                users[to_addr[0]]['client'].send(mess.encode())

            else:
                users[addr]['client'].send(b'There is no such user online')
        else:
            for user in users:
                if user != addr:
                    mess = users[addr]['name'].encode() + b": " + data.encode()
                    users[user]['client'].send(mess)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', port))
s.listen(10)
print(f"Server is running on port {port}:")

while True:
    client, addr = s.accept()
    print(f"Accepted connection from {addr}")
    threading.Thread(target=handle_client, args=(client, addr)).start()
