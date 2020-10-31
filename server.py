import socket as so
from settings import *

s = so.socket()

print('Socket successfully crated')

port = 1026

s.bind(('', port))
print(f'Socket binded to {port} port')

s.listen()
print('Socket is listening')

while True:
    conn, address = s.accept()
    print(f'Got a connection from {address}')
    with open(FILENAME, 'r') as file:
        lines = file.readlines()
        print(f'File contains {len(lines)} lines')
        conn.send(len(lines).to_bytes(8, 'big'))
        for line in lines:
            conn.send(line.encode())
        # conn.send(bytes(lines))

    conn.send(b'Thank You')
    conn.send(b'Goodbye')
    conn.close()
