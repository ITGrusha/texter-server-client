import math
import socket as so
import time
from settings import *
from sys import getsizeof

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
        lines_str = ''.join(file.readlines())
        file.close()

        to_send = lines_str.encode('utf-8')

        print(f'File contains {len(to_send)} bytes of data')

        conn.send(len(to_send).to_bytes(16, 'big'))
        conn.send(to_send)

        while True:
            try:
                byte_data = conn.recv(1)
            except so.error as e:
                byte_data = END_BYTE
            if byte_data == SAVE_BYTE:
                print('Updating file')
                data_size = int.from_bytes(conn.recv(16), 'big')
                data = conn.recv(data_size)
                data_str = data.decode('utf-8')
                with open(FILENAME, 'w') as file:
                    file.write(data_str)
            elif byte_data == END_BYTE:
                print('Connection closed by remote')
                break

    # conn.send(b'Thank You\n')
    # conn.send(b'Goodbye')
    conn.close()
