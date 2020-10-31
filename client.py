import socket as so
import tkinter as tk

s = so.socket()

port = 1026

s.connect(('localhost', 1026))

w = tk.Tk()

lines_count = int.from_bytes(s.recv(8), "big")
print(f'There are {lines_count} lines in file on server')

lines = list()

max_len = 0
for i in range(lines_count):
    line = s.recv(1024).decode()
    if max_len < len(line):
        max_len = len(line)
    lines.append(line)
    print(line, end='')
# print()

textbox = tk.Text(w, height=lines_count, width=max_len)
textbox.pack()
textbox.insert(tk.END, *lines)

print(s.recv(1024).decode())
print(s.recv(1024).decode())
s.close()


tk.mainloop()
