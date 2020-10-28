import socket as so

s = so.socket()

port = 1026

s.connect(('localhost', 1026))
print(s.recv(1024).decode('utf-8'))
print(s.recv(1024).decode())
s.close()

