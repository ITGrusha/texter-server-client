import socket as so
import tkinter as tk
import tkinter.messagebox
from settings import *
import logging.config

logging.config.fileConfig('logger.conf')
logger = logging.getLogger(name='Texter.TexterClient')


class Texter(object):
    def __init__(self, host: str, port: int):
        self.s = so.socket()
        self.host = host
        self.port = port

        self.connect()

        self.__text = ''
        self.__lines_count = 0
        self.__max_len = 0
        self.get_file()

        self.__window = tk.Tk()
        self.__window.bind('<Control-s>', self.check_and_save)

        tk.Label(self.__window, text='To send edited version to server, press <Ctrl+S>').pack()
        self.__text_box = tk.Text(self.__window, height=self.__lines_count, width=self.__max_len)
        self.__text_box.pack()
        self.show_contents()

        self.__window.mainloop()

    def __del__(self):
        self.disconnect()

    def connect(self):
        logger.debug(f'Trying to connect to {(self.host, self.port)}')
        try:
            self.s.connect((self.host, self.port))
            logger.info(f'Socket successfully connected to {self.host}:{self.port}')
        except so.error as e:
            logger.info(f'Connection refused({e})!')
            if tkinter.messagebox.askyesno(
                    'Connection refused!',
                    f'Connection refused\n{e}\nDo you want to try again?'
            ):
                self.connect()
            else:
                self.__window.destroy()

    def adjust_text(self):
        logger.debug(f'Adjusting file string before sending to server')
        text: str = self.__text_box.get(1., tk.END)
        result = ''

        start = 0
        for i in range(self.__lines_count):
            end = min(start + self.__max_len + 1, len(text))
            endl = text.find('\n', start, end)
            if endl != -1:
                end = endl
            elif end != len(text):
                end -= 1
            result += text[start: end] + ('\n' if i < self.__lines_count - 1 else '')
            if endl == -1:
                start = end
                continue
            start = end + 1

        self.__text = result

    def get_file(self):
        logger.info(f'Getting file size from server')

        file_size = int.from_bytes(self.s.recv(16), "big")
        logger.info(f'Going to receive {file_size} bytes of data')

        lines_str = self.s.recv(file_size).decode('utf-8')
        logger.info('Successfully got file')

        lines = lines_str.split('\n')
        self.__lines_count = len(lines)

        max_len = 0

        for line in lines:
            if max_len < len(line):
                max_len = len(line)

        self.__text = lines_str
        self.__max_len = max_len
        self.__lines_count = len(lines)

    def show_contents(self):
        self.__text_box.delete(1., tk.END)
        self.__text_box.insert(tk.END, self.__text)

    def check_and_save(self, *args):
        self.adjust_text()

        encoded = self.__text.encode('utf-8')
        logger.info('Sending our version to server...')

        self.s.send(SAVE_BYTE)
        self.s.send(len(encoded).to_bytes(16, 'big'))
        self.s.send(encoded)
        logger.info(f'Successfully sent {len(encoded)} bytes od data!')

    def who(self):
        logger.info(f'Sent who command')
        data = 'who'.encode('utf-8')
        data += bytes(255)
        data = data[0:255]
        self.s.send(COMMAND_BYTE)
        self.s.send(data)
        response = self.s.recv(256).decode('utf-8').replace('\x00', '')
        print(response)
        logger.info(f'Received who response')

    def disconnect(self):
        logger.info(f'Disconnected from {self.host}:{self.port}')
        self.s.send(END_BYTE)
        self.s.close()
