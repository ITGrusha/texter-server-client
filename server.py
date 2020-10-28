import socket as so
FILENAME = 'test.txt'

s = so.socket()

print('Socket successfully crated')

port = 1026

s.bind(('', port))
print(f'Socket binded to {port} port')

s.listen()
print('Socket is listening')

while True:
    conn, address = s.accept()
    print(f'Gor a connection from {address}')

    conn.send(b'Thank You')
    conn.send(b'Goodbye')
    conn.close()
