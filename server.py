import socket as so
from settings import *
import logging.config
import threading

logging.config.fileConfig('logger.conf')
logger = logging.getLogger(name='Texter.TexterServer')

s = so.socket()
logger.info('Socket successfully crated')

port = 1026

s.bind(('', port))
logger.info(f'Socket binded to {port} port')

s.listen()
logger.info('Socket is listening')


def accept_connection(conn, addr):
    logger.info(f'Got a connection from {addr}')
    with open(FILENAME, 'r') as file:
        lines_str = ''.join(file.readlines())
        file.close()

        to_send = lines_str.encode('utf-8')
        logger.info(f'File contains {len(to_send)} bytes of data. Sending to remote socket')
        conn.send(len(to_send).to_bytes(16, 'big'))
        conn.send(to_send)

        logger.info('Successfully sent file to remote')

        logger.info(f'Waiting for response from {addr}')
        while True:
            try:
                byte_data = conn.recv(1)
            except so.error as e:
                byte_data = END_BYTE
                logger.error(f'Lost connection with {addr}')
            if byte_data == SAVE_BYTE:
                logger.info(f'Updating file from {addr}')
                data_size = int.from_bytes(conn.recv(16), 'big')
                data = conn.recv(data_size)
                data_str = data.decode('utf-8')
                logger.info(f'Got {len(data)} / {data_size} bytes of data')
                with open(FILENAME, 'w') as file_:
                    file_.write(data_str)
                    logger.info(f'Wrote data from {addr} to file')
            elif byte_data == COMMAND_BYTE:
                commands_str = conn.recv(255).decode().replace('\x00', '')
                commands = [x.strip() for x in commands_str.strip().split(';')]
                for command in commands:
                    if command.lower() == 'who':
                        logger.info(f'Got Who command form {addr}')
                        response = WHO_STR.encode('utf-8')
                        response += bytes(256)
                        response = response[0:256]
                        conn.send(response)
                        logger.info(f'Send who response to {addr}')
            elif byte_data == END_BYTE:
                logger.info(f'Connection with {addr} is closing by remote')
                break

    conn.close()
    logger.info(f'Connection with {addr} closed')


while True:
    connection, address = s.accept()
    t = threading.Thread(None, accept_connection, args=[connection, address])
    t.start()
